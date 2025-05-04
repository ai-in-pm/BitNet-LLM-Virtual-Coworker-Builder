# Monitoring script for BitNet_LLM_Virtual_Coworker_Builder
# This script checks the health of the production environment and sends alerts if needed

param (
    [string]$InstallDir = "C:\BitNet-VC-Builder",
    [string]$LogDir = "C:\BitNet-VC-Builder\logs",
    [string]$AlertEmail = $null,
    [switch]$Silent = $false
)

# Create monitoring directory if it doesn't exist
$MonitoringDir = "$InstallDir\monitoring"
if (-not (Test-Path $MonitoringDir)) {
    New-Item -ItemType Directory -Force -Path $MonitoringDir | Out-Null
}

# Initialize log file
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$MonitoringLog = "$MonitoringDir\monitoring_$timestamp.log"

function Write-Log {
    param (
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    # Write to log file
    Add-Content -Path $MonitoringLog -Value $logMessage
    
    # Write to console if not silent
    if (-not $Silent) {
        switch ($Level) {
            "ERROR" { Write-Host $logMessage -ForegroundColor Red }
            "WARNING" { Write-Host $logMessage -ForegroundColor Yellow }
            "SUCCESS" { Write-Host $logMessage -ForegroundColor Green }
            default { Write-Host $logMessage }
        }
    }
}

function Send-Alert {
    param (
        [string]$Subject,
        [string]$Body
    )
    
    Write-Log "ALERT: $Subject - $Body" -Level "ERROR"
    
    # Send email alert if email is provided
    if ($AlertEmail) {
        try {
            $SmtpServer = "smtp.office365.com"
            $SmtpPort = 587
            $Username = $AlertEmail
            $Password = ConvertTo-SecureString $env:EMAIL_PASSWORD -AsPlainText -Force
            $Credential = New-Object System.Management.Automation.PSCredential ($Username, $Password)
            
            Send-MailMessage -From $AlertEmail -To $AlertEmail -Subject "BitNet VC Builder Alert: $Subject" -Body $Body -SmtpServer $SmtpServer -Port $SmtpPort -UseSsl -Credential $Credential
            
            Write-Log "Alert email sent to $AlertEmail" -Level "INFO"
        } catch {
            Write-Log "Failed to send alert email: $_" -Level "ERROR"
        }
    }
}

# Start monitoring
Write-Log "Starting BitNet VC Builder monitoring" -Level "INFO"
Write-Log "Install Directory: $InstallDir" -Level "INFO"
Write-Log "Log Directory: $LogDir" -Level "INFO"

# Check if the installation directory exists
if (-not (Test-Path $InstallDir)) {
    Send-Alert "Installation Directory Missing" "The installation directory does not exist: $InstallDir"
    exit 1
}

# Check if the API server is running
$apiServerRunning = $false
try {
    $apiProcess = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*bitnet_vc_builder.api.server*" }
    if ($apiProcess) {
        $apiServerRunning = $true
        Write-Log "API server is running (PID: $($apiProcess.Id))" -Level "SUCCESS"
    } else {
        Write-Log "API server is not running" -Level "WARNING"
    }
} catch {
    Write-Log "Failed to check API server status: $_" -Level "ERROR"
}

# Check if the Web UI is running
$webUiRunning = $false
try {
    $webUiProcess = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*bitnet_vc_builder.ui.web.app*" }
    if ($webUiProcess) {
        $webUiRunning = $true
        Write-Log "Web UI is running (PID: $($webUiProcess.Id))" -Level "SUCCESS"
    } else {
        Write-Log "Web UI is not running" -Level "WARNING"
    }
} catch {
    Write-Log "Failed to check Web UI status: $_" -Level "ERROR"
}

# Check if the API server is responding
$apiServerResponding = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $apiServerResponding = $true
        Write-Log "API server is responding (Status: $($response.StatusCode))" -Level "SUCCESS"
    } else {
        Write-Log "API server is not responding properly (Status: $($response.StatusCode))" -Level "WARNING"
    }
} catch {
    Write-Log "API server is not responding: $_" -Level "ERROR"
}

# Check if the Web UI is responding
$webUiResponding = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8501" -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $webUiResponding = $true
        Write-Log "Web UI is responding (Status: $($response.StatusCode))" -Level "SUCCESS"
    } else {
        Write-Log "Web UI is not responding properly (Status: $($response.StatusCode))" -Level "WARNING"
    }
} catch {
    Write-Log "Web UI is not responding: $_" -Level "ERROR"
}

# Check disk space
try {
    $drive = Get-PSDrive -Name C
    $freeSpaceGB = [math]::Round($drive.Free / 1GB, 2)
    $totalSpaceGB = [math]::Round(($drive.Used + $drive.Free) / 1GB, 2)
    $freeSpacePercentage = [math]::Round(($drive.Free / ($drive.Used + $drive.Free)) * 100, 2)
    
    Write-Log "Disk space: $freeSpaceGB GB free of $totalSpaceGB GB ($freeSpacePercentage%)" -Level "INFO"
    
    if ($freeSpacePercentage -lt 10) {
        Send-Alert "Low Disk Space" "Disk space is critically low: $freeSpaceGB GB free ($freeSpacePercentage%)"
    } elseif ($freeSpacePercentage -lt 20) {
        Write-Log "Disk space is running low: $freeSpaceGB GB free ($freeSpacePercentage%)" -Level "WARNING"
    }
} catch {
    Write-Log "Failed to check disk space: $_" -Level "ERROR"
}

# Check CPU usage
try {
    $cpuUsage = Get-Counter '\Processor(_Total)\% Processor Time' -ErrorAction SilentlyContinue
    $cpuUsageValue = [math]::Round($cpuUsage.CounterSamples.CookedValue, 2)
    
    Write-Log "CPU usage: $cpuUsageValue%" -Level "INFO"
    
    if ($cpuUsageValue -gt 90) {
        Send-Alert "High CPU Usage" "CPU usage is critically high: $cpuUsageValue%"
    } elseif ($cpuUsageValue -gt 80) {
        Write-Log "CPU usage is high: $cpuUsageValue%" -Level "WARNING"
    }
} catch {
    Write-Log "Failed to check CPU usage: $_" -Level "ERROR"
}

# Check memory usage
try {
    $memoryInfo = Get-CimInstance -ClassName Win32_OperatingSystem
    $totalMemoryGB = [math]::Round($memoryInfo.TotalVisibleMemorySize / 1MB, 2)
    $freeMemoryGB = [math]::Round($memoryInfo.FreePhysicalMemory / 1MB, 2)
    $usedMemoryGB = $totalMemoryGB - $freeMemoryGB
    $memoryUsagePercentage = [math]::Round(($usedMemoryGB / $totalMemoryGB) * 100, 2)
    
    Write-Log "Memory usage: $usedMemoryGB GB of $totalMemoryGB GB ($memoryUsagePercentage%)" -Level "INFO"
    
    if ($memoryUsagePercentage -gt 90) {
        Send-Alert "High Memory Usage" "Memory usage is critically high: $memoryUsagePercentage%"
    } elseif ($memoryUsagePercentage -gt 80) {
        Write-Log "Memory usage is high: $memoryUsagePercentage%" -Level "WARNING"
    }
} catch {
    Write-Log "Failed to check memory usage: $_" -Level "ERROR"
}

# Check log file sizes
try {
    $logFiles = Get-ChildItem -Path $LogDir -Filter "*.log" -ErrorAction SilentlyContinue
    foreach ($logFile in $logFiles) {
        $logSizeMB = [math]::Round($logFile.Length / 1MB, 2)
        Write-Log "Log file size: $($logFile.Name) - $logSizeMB MB" -Level "INFO"
        
        if ($logSizeMB -gt 1000) {
            Send-Alert "Large Log File" "Log file is very large: $($logFile.Name) - $logSizeMB MB"
        } elseif ($logSizeMB -gt 500) {
            Write-Log "Log file is large: $($logFile.Name) - $logSizeMB MB" -Level "WARNING"
        }
    }
} catch {
    Write-Log "Failed to check log file sizes: $_" -Level "ERROR"
}

# Check for errors in the logs
try {
    $recentErrors = Select-String -Path "$LogDir\*.log" -Pattern "ERROR|CRITICAL|FATAL" -Context 0,0 -ErrorAction SilentlyContinue | Select-Object -Last 10
    
    if ($recentErrors) {
        $errorCount = $recentErrors.Count
        Write-Log "Found $errorCount recent errors in the logs" -Level "WARNING"
        
        foreach ($error in $recentErrors) {
            Write-Log "Log error: $($error.Line)" -Level "WARNING"
        }
        
        if ($errorCount -gt 20) {
            Send-Alert "Many Errors in Logs" "Found $errorCount recent errors in the logs"
        }
    } else {
        Write-Log "No recent errors found in the logs" -Level "SUCCESS"
    }
} catch {
    Write-Log "Failed to check for errors in the logs: $_" -Level "ERROR"
}

# Send alerts if services are not running
if (-not $apiServerRunning -or -not $apiServerResponding) {
    Send-Alert "API Server Down" "The API server is not running or not responding"
}

if (-not $webUiRunning -or -not $webUiResponding) {
    Send-Alert "Web UI Down" "The Web UI is not running or not responding"
}

# Create monitoring summary
$summary = @{
    Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    ApiServerRunning = $apiServerRunning
    ApiServerResponding = $apiServerResponding
    WebUiRunning = $webUiRunning
    WebUiResponding = $webUiResponding
    DiskSpaceFreeGB = $freeSpaceGB
    DiskSpaceFreePercentage = $freeSpacePercentage
    CpuUsagePercentage = $cpuUsageValue
    MemoryUsagePercentage = $memoryUsagePercentage
    ErrorCount = if ($recentErrors) { $recentErrors.Count } else { 0 }
}

# Save monitoring summary to JSON file
$summaryJson = ConvertTo-Json $summary
$summaryFile = "$MonitoringDir\summary.json"
$summaryJson | Out-File -FilePath $summaryFile -Force

Write-Log "Monitoring summary saved to $summaryFile" -Level "INFO"
Write-Log "Monitoring complete" -Level "INFO"

# Return monitoring status
if (-not $apiServerRunning -or -not $apiServerResponding -or -not $webUiRunning -or -not $webUiResponding) {
    exit 1
} else {
    exit 0
}
