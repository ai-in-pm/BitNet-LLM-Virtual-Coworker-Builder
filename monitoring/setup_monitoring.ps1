# Setup script for BitNet_LLM_Virtual_Coworker_Builder monitoring
# This script sets up scheduled tasks to run the monitoring script at regular intervals

param (
    [string]$InstallDir = "C:\BitNet-VC-Builder",
    [string]$AlertEmail = $null,
    [int]$IntervalMinutes = 15
)

# Check if running as administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "This script must be run as Administrator" -ForegroundColor Red
    exit 1
}

# Create monitoring directory if it doesn't exist
$MonitoringDir = "$InstallDir\monitoring"
if (-not (Test-Path $MonitoringDir)) {
    New-Item -ItemType Directory -Force -Path $MonitoringDir | Out-Null
}

# Copy monitoring script to the monitoring directory
$SourceScript = "$PSScriptRoot\monitor.ps1"
$DestScript = "$MonitoringDir\monitor.ps1"
Copy-Item -Path $SourceScript -Destination $DestScript -Force

Write-Host "Monitoring script copied to $DestScript" -ForegroundColor Green

# Create a scheduled task to run the monitoring script
$TaskName = "BitNetVCBuilderMonitoring"
$TaskDescription = "Monitors the BitNet Virtual Co-worker Builder production environment"
$TaskCommand = "powershell.exe"
$TaskArguments = "-ExecutionPolicy Bypass -File `"$DestScript`" -InstallDir `"$InstallDir`""

if ($AlertEmail) {
    $TaskArguments += " -AlertEmail `"$AlertEmail`""
}

# Create a trigger for the scheduled task
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes) -RepetitionDuration ([TimeSpan]::MaxValue)

# Create an action for the scheduled task
$Action = New-ScheduledTaskAction -Execute $TaskCommand -Argument $TaskArguments

# Create a principal for the scheduled task (run with highest privileges)
$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

# Create the scheduled task
$Task = New-ScheduledTask -Action $Action -Trigger $Trigger -Principal $Principal -Description $TaskDescription

# Register the scheduled task
Register-ScheduledTask -TaskName $TaskName -InputObject $Task -Force

Write-Host "Scheduled task '$TaskName' created successfully" -ForegroundColor Green
Write-Host "The monitoring script will run every $IntervalMinutes minutes" -ForegroundColor Green

# Create a dashboard script
$DashboardScript = @"
# BitNet Virtual Co-worker Builder Monitoring Dashboard
# This script displays the current status of the production environment

param (
    [string]`$InstallDir = "$InstallDir"
)

`$MonitoringDir = "`$InstallDir\monitoring"
`$SummaryFile = "`$MonitoringDir\summary.json"

function Show-Dashboard {
    Clear-Host
    Write-Host "=== BitNet Virtual Co-worker Builder Monitoring Dashboard ===" -ForegroundColor Cyan
    Write-Host "Time: `$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
    Write-Host "=======================================================" -ForegroundColor Cyan
    
    if (Test-Path `$SummaryFile) {
        `$summary = Get-Content -Path `$SummaryFile | ConvertFrom-Json
        
        Write-Host "Last Update: `$(`$summary.Timestamp)" -ForegroundColor Yellow
        Write-Host ""
        
        # Display service status
        Write-Host "Service Status:" -ForegroundColor White
        if (`$summary.ApiServerRunning -and `$summary.ApiServerResponding) {
            Write-Host "  API Server: Running" -ForegroundColor Green
        } else {
            Write-Host "  API Server: Not Running" -ForegroundColor Red
        }
        
        if (`$summary.WebUiRunning -and `$summary.WebUiResponding) {
            Write-Host "  Web UI: Running" -ForegroundColor Green
        } else {
            Write-Host "  Web UI: Not Running" -ForegroundColor Red
        }
        
        Write-Host ""
        
        # Display system resources
        Write-Host "System Resources:" -ForegroundColor White
        
        # Disk space
        `$diskColor = if (`$summary.DiskSpaceFreePercentage -lt 10) { "Red" } elseif (`$summary.DiskSpaceFreePercentage -lt 20) { "Yellow" } else { "Green" }
        Write-Host "  Disk Space: `$(`$summary.DiskSpaceFreeGB) GB free (`$(`$summary.DiskSpaceFreePercentage)%)" -ForegroundColor `$diskColor
        
        # CPU usage
        `$cpuColor = if (`$summary.CpuUsagePercentage -gt 90) { "Red" } elseif (`$summary.CpuUsagePercentage -gt 80) { "Yellow" } else { "Green" }
        Write-Host "  CPU Usage: `$(`$summary.CpuUsagePercentage)%" -ForegroundColor `$cpuColor
        
        # Memory usage
        `$memoryColor = if (`$summary.MemoryUsagePercentage -gt 90) { "Red" } elseif (`$summary.MemoryUsagePercentage -gt 80) { "Yellow" } else { "Green" }
        Write-Host "  Memory Usage: `$(`$summary.MemoryUsagePercentage)%" -ForegroundColor `$memoryColor
        
        Write-Host ""
        
        # Display error count
        `$errorColor = if (`$summary.ErrorCount -gt 20) { "Red" } elseif (`$summary.ErrorCount -gt 0) { "Yellow" } else { "Green" }
        Write-Host "Recent Errors: `$(`$summary.ErrorCount)" -ForegroundColor `$errorColor
        
        # Display recent log entries
        Write-Host ""
        Write-Host "Recent Log Entries:" -ForegroundColor White
        `$recentLogs = Get-Content -Path "`$MonitoringDir\monitoring_*.log" -ErrorAction SilentlyContinue | Select-Object -Last 10
        if (`$recentLogs) {
            foreach (`$log in `$recentLogs) {
                if (`$log -match "ERROR") {
                    Write-Host "  `$log" -ForegroundColor Red
                } elseif (`$log -match "WARNING") {
                    Write-Host "  `$log" -ForegroundColor Yellow
                } elseif (`$log -match "SUCCESS") {
                    Write-Host "  `$log" -ForegroundColor Green
                } else {
                    Write-Host "  `$log" -ForegroundColor Gray
                }
            }
        } else {
            Write-Host "  No recent log entries found" -ForegroundColor Gray
        }
    } else {
        Write-Host "No monitoring data available. Please run the monitoring script first." -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "Press Ctrl+C to exit or wait for automatic refresh..." -ForegroundColor Yellow
}

# Main loop
while (`$true) {
    Show-Dashboard
    Start-Sleep -Seconds 10
}
"@

$DashboardScriptPath = "$MonitoringDir\dashboard.ps1"
$DashboardScript | Out-File -FilePath $DashboardScriptPath -Force

Write-Host "Dashboard script created at $DashboardScriptPath" -ForegroundColor Green

# Create a shortcut for the dashboard
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\BitNet VC Builder - Monitoring Dashboard.lnk")
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$DashboardScriptPath`""
$Shortcut.WorkingDirectory = $MonitoringDir
$Shortcut.Save()

Write-Host "Dashboard shortcut created on the desktop" -ForegroundColor Green
Write-Host "Monitoring setup complete" -ForegroundColor Green
