# BitNet Virtual Co-worker Builder Backup System

This directory contains scripts for backing up and restoring the BitNet Virtual Co-worker Builder production environment.

## Backup Scripts

### backup.ps1

This script creates a backup of the production environment.

```powershell
.\backup.ps1 -InstallDir "C:\BitNet-VC-Builder" -BackupDir "C:\BitNet-VC-Builder-Backups" [-IncludeModels] [-Compress] [-KeepBackups 7]
```

Parameters:
- `-InstallDir`: The installation directory of BitNet Virtual Co-worker Builder (default: `C:\BitNet-VC-Builder`)
- `-BackupDir`: The directory where backups will be stored (default: `C:\BitNet-VC-Builder-Backups`)
- `-IncludeModels`: Include model files in the backup (default: false)
- `-Compress`: Compress the backup into a ZIP file (default: true)
- `-KeepBackups`: Number of backups to keep (default: 7)

### setup_backup.ps1

This script sets up scheduled backups using Windows Task Scheduler.

```powershell
.\setup_backup.ps1 -InstallDir "C:\BitNet-VC-Builder" -BackupDir "C:\BitNet-VC-Builder-Backups" [-IncludeModels] [-Compress] [-KeepBackups 7] [-BackupFrequency "Daily"] [-BackupHour 3] [-BackupMinute 0]
```

Parameters:
- `-InstallDir`: The installation directory of BitNet Virtual Co-worker Builder (default: `C:\BitNet-VC-Builder`)
- `-BackupDir`: The directory where backups will be stored (default: `C:\BitNet-VC-Builder-Backups`)
- `-IncludeModels`: Include model files in the backup (default: false)
- `-Compress`: Compress the backup into a ZIP file (default: true)
- `-KeepBackups`: Number of backups to keep (default: 7)
- `-BackupFrequency`: Frequency of backups (Daily, Weekly, Monthly) (default: Daily)
- `-BackupHour`: Hour of the day to run the backup (0-23) (default: 3)
- `-BackupMinute`: Minute of the hour to run the backup (0-59) (default: 0)

### restore.ps1

This script restores a backup of the production environment.

```powershell
.\restore.ps1 -BackupPath "C:\BitNet-VC-Builder-Backups\BitNet-VC-Builder_Backup_2023-01-01_00-00-00" -InstallDir "C:\BitNet-VC-Builder" [-RestoreConfig] [-RestoreData] [-RestoreLogs]
```

Parameters:
- `-BackupPath`: The path to the backup to restore (required)
- `-InstallDir`: The installation directory of BitNet Virtual Co-worker Builder (default: `C:\BitNet-VC-Builder`)
- `-RestoreConfig`: Restore configuration files (default: true)
- `-RestoreData`: Restore data files (default: true)
- `-RestoreLogs`: Restore log files (default: false)

### manage_backups.ps1

This script provides a menu-driven interface for managing backups.

```powershell
.\manage_backups.ps1 -InstallDir "C:\BitNet-VC-Builder" -BackupDir "C:\BitNet-VC-Builder-Backups"
```

Parameters:
- `-InstallDir`: The installation directory of BitNet Virtual Co-worker Builder (default: `C:\BitNet-VC-Builder`)
- `-BackupDir`: The directory where backups are stored (default: `C:\BitNet-VC-Builder-Backups`)

## Backup Strategy

The backup strategy for BitNet Virtual Co-worker Builder includes:

1. **Regular Automated Backups**: Daily backups are scheduled to run at 3:00 AM by default.
2. **Retention Policy**: By default, the 7 most recent backups are kept, and older backups are automatically deleted.
3. **Selective Backup**: You can choose whether to include model files in the backup. Model files can be large, so they are excluded by default.
4. **Compression**: Backups are compressed by default to save disk space.
5. **Backup Management**: A user-friendly interface is provided for managing backups.

## Backup Contents

Each backup includes:

- **Configuration Files**: All configuration files in the `config` directory
- **Data Files**: All data files in the `data` directory (excluding models by default)
- **Log Files**: All log files in the `logs` directory
- **Metadata**: A metadata file containing information about the backup

## Restoring from Backup

To restore from a backup:

1. Run the `manage_backups.ps1` script
2. Select option 3 (Restore from backup)
3. Select the backup to restore
4. Confirm the restore operation
5. Select which components to restore (configuration, data, logs)

## Best Practices

1. **Regular Backups**: Ensure that backups are running regularly by checking the Task Scheduler.
2. **Backup Verification**: Periodically verify that backups are being created correctly by checking the backup directory.
3. **Test Restores**: Periodically test the restore process to ensure that backups can be successfully restored.
4. **External Storage**: Consider copying backups to an external storage device or cloud storage for additional protection.
5. **Documentation**: Keep track of any changes to the backup configuration or restore procedures.

## Troubleshooting

If you encounter issues with the backup system:

1. **Check Logs**: Check the backup log file in the backup directory for error messages.
2. **Check Permissions**: Ensure that the account running the backup has sufficient permissions to access the installation directory and backup directory.
3. **Check Disk Space**: Ensure that there is sufficient disk space available for backups.
4. **Check Task Scheduler**: Ensure that the backup task is properly configured in Task Scheduler.
5. **Manual Backup**: Try running the backup script manually to see if there are any errors.

## Support

If you need assistance with the backup system, please contact the BitNet Virtual Co-worker Builder support team.
