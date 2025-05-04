# Setup script for BitNet_LLM_Virtual_Coworker_Builder backups
# This script sets up scheduled tasks to run the backup script at regular intervals

param (
    [string]$InstallDir = "C:\BitNet-VC-Builder",
    [string]$BackupDir = "C:\BitNet-VC-Builder-Backups",
    [switch]$IncludeModels = $false,
    [switch]$Compress = $true,
    [int]$KeepBackups = 7,
    [string]$BackupFrequency = "Daily",  # Daily, Weekly, Monthly
    [int]$BackupHour = 3,                # Hour of the day to run the backup (0-23)
    [int]$BackupMinute = 0               # Minute of the hour to run the backup (0-59)
)

# Check if running as administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "This script must be run as Administrator" -ForegroundColor Red
    exit 1
}

# Create backup directory if it doesn't exist
if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
}

# Create backup script directory if it doesn't exist
$BackupScriptDir = "$InstallDir\backup"
if (-not (Test-Path $BackupScriptDir)) {
    New-Item -ItemType Directory -Force -Path $BackupScriptDir | Out-Null
}

# Copy backup script to the backup directory
$SourceScript = "$PSScriptRoot\backup.ps1"
$DestScript = "$BackupScriptDir\backup.ps1"
Copy-Item -Path $SourceScript -Destination $DestScript -Force

Write-Host "Backup script copied to $DestScript" -ForegroundColor Green

# Create a scheduled task to run the backup script
$TaskName = "BitNetVCBuilderBackup"
$TaskDescription = "Backs up the BitNet Virtual Co-worker Builder production environment"
$TaskCommand = "powershell.exe"

# Build the arguments for the backup script
$TaskArguments = "-ExecutionPolicy Bypass -File `"$DestScript`" -InstallDir `"$InstallDir`" -BackupDir `"$BackupDir`""

if ($IncludeModels) {
    $TaskArguments += " -IncludeModels"
}

if ($Compress) {
    $TaskArguments += " -Compress"
}

$TaskArguments += " -KeepBackups $KeepBackups"

# Create a trigger for the scheduled task
$TriggerParams = @{
    Daily = $false
    Weekly = $false
    Monthly = $false
    At = [DateTime]::Parse("$BackupHour`:$BackupMinute")
}

switch ($BackupFrequency) {
    "Daily" {
        $TriggerParams.Daily = $true
        $TriggerParams.DaysInterval = 1
    }
    "Weekly" {
        $TriggerParams.Weekly = $true
        $TriggerParams.WeeksInterval = 1
        $TriggerParams.DaysOfWeek = "Sunday"
    }
    "Monthly" {
        $TriggerParams.Monthly = $true
        $TriggerParams.DaysOfMonth = 1
    }
    default {
        Write-Host "Invalid backup frequency: $BackupFrequency. Using Daily." -ForegroundColor Yellow
        $TriggerParams.Daily = $true
        $TriggerParams.DaysInterval = 1
    }
}

$Trigger = New-ScheduledTaskTrigger @TriggerParams

# Create an action for the scheduled task
$Action = New-ScheduledTaskAction -Execute $TaskCommand -Argument $TaskArguments

# Create a principal for the scheduled task (run with highest privileges)
$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

# Create the scheduled task
$Task = New-ScheduledTask -Action $Action -Trigger $Trigger -Principal $Principal -Description $TaskDescription

# Register the scheduled task
Register-ScheduledTask -TaskName $TaskName -InputObject $Task -Force

Write-Host "Scheduled task '$TaskName' created successfully" -ForegroundColor Green
Write-Host "The backup script will run $BackupFrequency at $BackupHour`:$($BackupMinute.ToString('00'))" -ForegroundColor Green

# Create a restore script
$RestoreScript = @"
# Restore script for BitNet_LLM_Virtual_Coworker_Builder
# This script restores a backup of the production environment

param (
    [Parameter(Mandatory=`$true)]
    [string]`$BackupPath,
    [string]`$InstallDir = "$InstallDir",
    [switch]`$RestoreConfig = `$true,
    [switch]`$RestoreData = `$true,
    [switch]`$RestoreLogs = `$false
)

# Check if running as administrator
`$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not `$currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "This script must be run as Administrator" -ForegroundColor Red
    exit 1
}

# Check if the backup path exists
if (-not (Test-Path `$BackupPath)) {
    Write-Host "Backup path does not exist: `$BackupPath" -ForegroundColor Red
    exit 1
}

# Check if the backup is compressed
`$isCompressed = `$BackupPath -like "*.zip"
`$tempDir = `$null

if (`$isCompressed) {
    # Create a temporary directory for extraction
    `$tempDir = Join-Path -Path `$env:TEMP -ChildPath "BitNetVCBuilderRestore_`$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    New-Item -ItemType Directory -Force -Path `$tempDir | Out-Null
    
    # Extract the backup
    Write-Host "Extracting backup..." -ForegroundColor Yellow
    Expand-Archive -Path `$BackupPath -DestinationPath `$tempDir -Force
    
    # Update the backup path to the extracted directory
    `$BackupPath = `$tempDir
}

# Check if the installation directory exists
if (-not (Test-Path `$InstallDir)) {
    Write-Host "Installation directory does not exist: `$InstallDir" -ForegroundColor Red
    exit 1
}

# Stop services
Write-Host "Stopping services..." -ForegroundColor Yellow
Stop-Service -Name "bitnet-vc-builder-api" -ErrorAction SilentlyContinue
Stop-Service -Name "bitnet-vc-builder-ui" -ErrorAction SilentlyContinue

# Restore configuration files
if (`$RestoreConfig) {
    Write-Host "Restoring configuration files..." -ForegroundColor Yellow
    if (Test-Path "`$BackupPath\config") {
        Copy-Item -Path "`$BackupPath\config\*" -Destination "`$InstallDir\config" -Recurse -Force
        Write-Host "Configuration files restored successfully" -ForegroundColor Green
    } else {
        Write-Host "No configuration files found in the backup" -ForegroundColor Yellow
    }
}

# Restore data files
if (`$RestoreData) {
    Write-Host "Restoring data files..." -ForegroundColor Yellow
    if (Test-Path "`$BackupPath\data") {
        Copy-Item -Path "`$BackupPath\data\*" -Destination "`$InstallDir\data" -Recurse -Force
        Write-Host "Data files restored successfully" -ForegroundColor Green
    } else {
        Write-Host "No data files found in the backup" -ForegroundColor Yellow
    }
}

# Restore log files
if (`$RestoreLogs) {
    Write-Host "Restoring log files..." -ForegroundColor Yellow
    if (Test-Path "`$BackupPath\logs") {
        Copy-Item -Path "`$BackupPath\logs\*" -Destination "`$InstallDir\logs" -Recurse -Force
        Write-Host "Log files restored successfully" -ForegroundColor Green
    } else {
        Write-Host "No log files found in the backup" -ForegroundColor Yellow
    }
}

# Clean up temporary directory if created
if (`$tempDir -and (Test-Path `$tempDir)) {
    Remove-Item -Path `$tempDir -Recurse -Force
    Write-Host "Temporary directory cleaned up" -ForegroundColor Yellow
}

# Start services
Write-Host "Starting services..." -ForegroundColor Yellow
Start-Service -Name "bitnet-vc-builder-api" -ErrorAction SilentlyContinue
Start-Service -Name "bitnet-vc-builder-ui" -ErrorAction SilentlyContinue

Write-Host "Restore completed successfully" -ForegroundColor Green
"@

$RestoreScriptPath = "$BackupScriptDir\restore.ps1"
$RestoreScript | Out-File -FilePath $RestoreScriptPath -Force

Write-Host "Restore script created at $RestoreScriptPath" -ForegroundColor Green

# Create a backup management script
$BackupManagementScript = @"
# Backup Management script for BitNet_LLM_Virtual_Coworker_Builder
# This script provides a menu for managing backups

param (
    [string]`$InstallDir = "$InstallDir",
    [string]`$BackupDir = "$BackupDir"
)

function Show-Menu {
    Clear-Host
    Write-Host "=== BitNet Virtual Co-worker Builder Backup Management ===" -ForegroundColor Cyan
    Write-Host "1. Create a new backup"
    Write-Host "2. List available backups"
    Write-Host "3. Restore from backup"
    Write-Host "4. Delete a backup"
    Write-Host "5. Exit"
    Write-Host "=======================================================" -ForegroundColor Cyan
}

function Create-Backup {
    Write-Host "Creating a new backup..." -ForegroundColor Yellow
    
    `$includeModels = Read-Host "Include models? (y/n)"
    `$includeModelsFlag = if (`$includeModels -eq "y") { "-IncludeModels" } else { "" }
    
    `$compress = Read-Host "Compress backup? (y/n)"
    `$compressFlag = if (`$compress -eq "y") { "-Compress" } else { "" }
    
    `$command = "powershell.exe -ExecutionPolicy Bypass -File `"`$InstallDir\backup\backup.ps1`" -InstallDir `"`$InstallDir`" -BackupDir `"`$BackupDir`" `$includeModelsFlag `$compressFlag"
    
    Invoke-Expression `$command
    
    Write-Host "Backup created successfully" -ForegroundColor Green
    Read-Host "Press Enter to continue"
}

function List-Backups {
    Write-Host "Available backups:" -ForegroundColor Yellow
    
    `$backups = Get-ChildItem -Path `$BackupDir | Where-Object { `$_.Name -like "BitNet-VC-Builder_Backup_*" } | Sort-Object -Property LastWriteTime -Descending
    
    if (`$backups.Count -eq 0) {
        Write-Host "No backups found" -ForegroundColor Red
    } else {
        `$i = 1
        foreach (`$backup in `$backups) {
            `$size = if (`$backup -is [System.IO.DirectoryInfo]) {
                `$size = (Get-ChildItem `$backup.FullName -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
                "{0:N2} MB" -f `$size
            } else {
                "{0:N2} MB" -f (`$backup.Length / 1MB)
            }
            
            Write-Host "`$i. `$(`$backup.Name) - `$(`$backup.LastWriteTime) - `$size"
            `$i++
        }
    }
    
    Read-Host "Press Enter to continue"
}

function Restore-Backup {
    Write-Host "Restore from backup:" -ForegroundColor Yellow
    
    `$backups = Get-ChildItem -Path `$BackupDir | Where-Object { `$_.Name -like "BitNet-VC-Builder_Backup_*" } | Sort-Object -Property LastWriteTime -Descending
    
    if (`$backups.Count -eq 0) {
        Write-Host "No backups found" -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return
    }
    
    `$i = 1
    foreach (`$backup in `$backups) {
        `$size = if (`$backup -is [System.IO.DirectoryInfo]) {
            `$size = (Get-ChildItem `$backup.FullName -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
            "{0:N2} MB" -f `$size
        } else {
            "{0:N2} MB" -f (`$backup.Length / 1MB)
        }
        
        Write-Host "`$i. `$(`$backup.Name) - `$(`$backup.LastWriteTime) - `$size"
        `$i++
    }
    
    `$selection = Read-Host "Enter the number of the backup to restore (or 0 to cancel)"
    
    if (`$selection -eq "0" -or `$selection -eq "") {
        return
    }
    
    `$index = [int]`$selection - 1
    
    if (`$index -ge 0 -and `$index -lt `$backups.Count) {
        `$selectedBackup = `$backups[`$index]
        
        Write-Host "You selected: `$(`$selectedBackup.Name)" -ForegroundColor Yellow
        `$confirm = Read-Host "Are you sure you want to restore this backup? (y/n)"
        
        if (`$confirm -eq "y") {
            `$restoreConfig = Read-Host "Restore configuration files? (y/n)"
            `$restoreConfigFlag = if (`$restoreConfig -eq "y") { "-RestoreConfig" } else { "-RestoreConfig:`$false" }
            
            `$restoreData = Read-Host "Restore data files? (y/n)"
            `$restoreDataFlag = if (`$restoreData -eq "y") { "-RestoreData" } else { "-RestoreData:`$false" }
            
            `$restoreLogs = Read-Host "Restore log files? (y/n)"
            `$restoreLogsFlag = if (`$restoreLogs -eq "y") { "-RestoreLogs" } else { "-RestoreLogs:`$false" }
            
            `$command = "powershell.exe -ExecutionPolicy Bypass -File `"`$InstallDir\backup\restore.ps1`" -BackupPath `"`$(`$selectedBackup.FullName)`" -InstallDir `"`$InstallDir`" `$restoreConfigFlag `$restoreDataFlag `$restoreLogsFlag"
            
            Invoke-Expression `$command
            
            Write-Host "Restore completed" -ForegroundColor Green
        }
    } else {
        Write-Host "Invalid selection" -ForegroundColor Red
    }
    
    Read-Host "Press Enter to continue"
}

function Delete-Backup {
    Write-Host "Delete a backup:" -ForegroundColor Yellow
    
    `$backups = Get-ChildItem -Path `$BackupDir | Where-Object { `$_.Name -like "BitNet-VC-Builder_Backup_*" } | Sort-Object -Property LastWriteTime -Descending
    
    if (`$backups.Count -eq 0) {
        Write-Host "No backups found" -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return
    }
    
    `$i = 1
    foreach (`$backup in `$backups) {
        `$size = if (`$backup -is [System.IO.DirectoryInfo]) {
            `$size = (Get-ChildItem `$backup.FullName -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
            "{0:N2} MB" -f `$size
        } else {
            "{0:N2} MB" -f (`$backup.Length / 1MB)
        }
        
        Write-Host "`$i. `$(`$backup.Name) - `$(`$backup.LastWriteTime) - `$size"
        `$i++
    }
    
    `$selection = Read-Host "Enter the number of the backup to delete (or 0 to cancel)"
    
    if (`$selection -eq "0" -or `$selection -eq "") {
        return
    }
    
    `$index = [int]`$selection - 1
    
    if (`$index -ge 0 -and `$index -lt `$backups.Count) {
        `$selectedBackup = `$backups[`$index]
        
        Write-Host "You selected: `$(`$selectedBackup.Name)" -ForegroundColor Yellow
        `$confirm = Read-Host "Are you sure you want to delete this backup? (y/n)"
        
        if (`$confirm -eq "y") {
            Remove-Item -Path `$selectedBackup.FullName -Recurse -Force
            Write-Host "Backup deleted successfully" -ForegroundColor Green
        }
    } else {
        Write-Host "Invalid selection" -ForegroundColor Red
    }
    
    Read-Host "Press Enter to continue"
}

# Main loop
while (`$true) {
    Show-Menu
    `$selection = Read-Host "Enter your selection"
    
    switch (`$selection) {
        "1" { Create-Backup }
        "2" { List-Backups }
        "3" { Restore-Backup }
        "4" { Delete-Backup }
        "5" { exit }
        default { Write-Host "Invalid selection" -ForegroundColor Red; Read-Host "Press Enter to continue" }
    }
}
"@

$BackupManagementScriptPath = "$BackupScriptDir\manage_backups.ps1"
$BackupManagementScript | Out-File -FilePath $BackupManagementScriptPath -Force

Write-Host "Backup management script created at $BackupManagementScriptPath" -ForegroundColor Green

# Create a shortcut for the backup management script
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\BitNet VC Builder - Backup Management.lnk")
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$BackupManagementScriptPath`""
$Shortcut.WorkingDirectory = $BackupScriptDir
$Shortcut.Save()

Write-Host "Backup management shortcut created on the desktop" -ForegroundColor Green
Write-Host "Backup setup complete" -ForegroundColor Green
