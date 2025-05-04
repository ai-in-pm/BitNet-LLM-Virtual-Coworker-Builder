# Backup script for BitNet_LLM_Virtual_Coworker_Builder
# This script creates backups of the production environment

param (
    [string]$InstallDir = "C:\BitNet-VC-Builder",
    [string]$BackupDir = "C:\BitNet-VC-Builder-Backups",
    [switch]$IncludeModels = $false,  # Models can be large, so they're excluded by default
    [switch]$Compress = $true,        # Compress the backup
    [int]$KeepBackups = 7             # Number of backups to keep
)

# Create backup directory if it doesn't exist
if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
}

# Create timestamp for backup
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$backupName = "BitNet-VC-Builder_Backup_$timestamp"
$backupPath = Join-Path -Path $BackupDir -ChildPath $backupName

# Create backup directory
New-Item -ItemType Directory -Force -Path $backupPath | Out-Null

# Log file
$logFile = Join-Path -Path $backupPath -ChildPath "backup.log"

function Write-Log {
    param (
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    # Write to log file
    Add-Content -Path $logFile -Value $logMessage
    
    # Write to console
    switch ($Level) {
        "ERROR" { Write-Host $logMessage -ForegroundColor Red }
        "WARNING" { Write-Host $logMessage -ForegroundColor Yellow }
        "SUCCESS" { Write-Host $logMessage -ForegroundColor Green }
        default { Write-Host $logMessage }
    }
}

# Start backup
Write-Log "Starting backup of BitNet Virtual Co-worker Builder" -Level "INFO"
Write-Log "Install Directory: $InstallDir" -Level "INFO"
Write-Log "Backup Directory: $BackupDir" -Level "INFO"
Write-Log "Backup Path: $backupPath" -Level "INFO"
Write-Log "Include Models: $IncludeModels" -Level "INFO"
Write-Log "Compress Backup: $Compress" -Level "INFO"

# Check if the installation directory exists
if (-not (Test-Path $InstallDir)) {
    Write-Log "Installation directory does not exist: $InstallDir" -Level "ERROR"
    exit 1
}

# Create directories in the backup
New-Item -ItemType Directory -Force -Path "$backupPath\config" | Out-Null
New-Item -ItemType Directory -Force -Path "$backupPath\data" | Out-Null
New-Item -ItemType Directory -Force -Path "$backupPath\logs" | Out-Null

# Backup configuration files
Write-Log "Backing up configuration files..." -Level "INFO"
try {
    Copy-Item -Path "$InstallDir\config\*" -Destination "$backupPath\config" -Recurse -Force
    Write-Log "Configuration files backed up successfully" -Level "SUCCESS"
} catch {
    Write-Log "Failed to backup configuration files: $_" -Level "ERROR"
}

# Backup data files (excluding models if not specified)
Write-Log "Backing up data files..." -Level "INFO"
try {
    if ($IncludeModels) {
        Copy-Item -Path "$InstallDir\data\*" -Destination "$backupPath\data" -Recurse -Force
        Write-Log "Data files (including models) backed up successfully" -Level "SUCCESS"
    } else {
        # Create models directory in the backup
        New-Item -ItemType Directory -Force -Path "$backupPath\data\models" | Out-Null
        
        # Copy everything except the models directory
        Get-ChildItem -Path "$InstallDir\data" -Exclude "models" | Copy-Item -Destination "$backupPath\data" -Recurse -Force
        
        # Create a file to indicate that models were not backed up
        "Models were not included in this backup. Use the --include-models flag to include them." | Out-File -FilePath "$backupPath\data\models\README.txt"
        
        Write-Log "Data files (excluding models) backed up successfully" -Level "SUCCESS"
    }
} catch {
    Write-Log "Failed to backup data files: $_" -Level "ERROR"
}

# Backup log files
Write-Log "Backing up log files..." -Level "INFO"
try {
    Copy-Item -Path "$InstallDir\logs\*" -Destination "$backupPath\logs" -Recurse -Force
    Write-Log "Log files backed up successfully" -Level "SUCCESS"
} catch {
    Write-Log "Failed to backup log files: $_" -Level "ERROR"
}

# Create a metadata file
$metadata = @{
    Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    InstallDir = $InstallDir
    BackupDir = $BackupDir
    IncludeModels = $IncludeModels
    Compress = $Compress
    KeepBackups = $KeepBackups
}

$metadataJson = ConvertTo-Json $metadata
$metadataJson | Out-File -FilePath "$backupPath\metadata.json" -Force

Write-Log "Metadata file created" -Level "INFO"

# Compress the backup if specified
if ($Compress) {
    Write-Log "Compressing backup..." -Level "INFO"
    try {
        $compressedFile = "$BackupDir\$backupName.zip"
        Compress-Archive -Path "$backupPath\*" -DestinationPath $compressedFile -Force
        Write-Log "Backup compressed successfully: $compressedFile" -Level "SUCCESS"
        
        # Remove the uncompressed backup
        Remove-Item -Path $backupPath -Recurse -Force
        Write-Log "Uncompressed backup removed" -Level "INFO"
        
        # Update backup path to the compressed file
        $backupPath = $compressedFile
    } catch {
        Write-Log "Failed to compress backup: $_" -Level "ERROR"
    }
}

# Clean up old backups
Write-Log "Cleaning up old backups..." -Level "INFO"
try {
    $backups = Get-ChildItem -Path $BackupDir | Where-Object { $_.Name -like "BitNet-VC-Builder_Backup_*" } | Sort-Object -Property LastWriteTime -Descending
    
    if ($backups.Count -gt $KeepBackups) {
        $backupsToRemove = $backups | Select-Object -Skip $KeepBackups
        
        foreach ($backup in $backupsToRemove) {
            Remove-Item -Path $backup.FullName -Recurse -Force
            Write-Log "Removed old backup: $($backup.Name)" -Level "INFO"
        }
        
        Write-Log "Old backups cleaned up successfully" -Level "SUCCESS"
    } else {
        Write-Log "No old backups to clean up" -Level "INFO"
    }
} catch {
    Write-Log "Failed to clean up old backups: $_" -Level "ERROR"
}

Write-Log "Backup completed successfully: $backupPath" -Level "SUCCESS"

# Return the backup path
return $backupPath
