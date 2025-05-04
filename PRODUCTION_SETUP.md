# BitNet Virtual Co-worker Builder Production Setup

This document provides instructions for setting up BitNet Virtual Co-worker Builder for production use on Windows.

## Prerequisites

Before setting up the production environment, ensure you have the following prerequisites installed:

- **Python 3.8 or higher**
- **Node.js 14 or higher** (for building the Tauri desktop application)
- **npm** (comes with Node.js)
- **Git** (optional, only needed if you're cloning the repository)

## Production Setup Options

There are two ways to set up BitNet Virtual Co-worker Builder for production:

### Option 1: Using the Automated Setup Script (Recommended)

1. Open PowerShell as Administrator
2. Navigate to the BitNet_LLM_Virtual_Coworker_Builder directory
3. Run the setup script:

```powershell
.\setup_production.ps1
```

This script will:
- Create the production directory structure at `C:\BitNet-VC-Builder`
- Copy the configuration file
- Create a virtual environment and install dependencies
- Build the Tauri desktop application
- Create desktop shortcuts for the API server, web UI, and desktop application
- Create a startup script
- Add the application to the Windows startup folder

### Option 2: Manual Setup

If you prefer to set up the production environment manually, follow these steps:

1. Create the production directory structure:

```powershell
New-Item -ItemType Directory -Force -Path "C:\BitNet-VC-Builder"
New-Item -ItemType Directory -Force -Path "C:\BitNet-VC-Builder\logs"
New-Item -ItemType Directory -Force -Path "C:\BitNet-VC-Builder\config"
New-Item -ItemType Directory -Force -Path "C:\BitNet-VC-Builder\data"
New-Item -ItemType Directory -Force -Path "C:\BitNet-VC-Builder\data\models"
New-Item -ItemType Directory -Force -Path "C:\BitNet-VC-Builder\data\cache"
New-Item -ItemType Directory -Force -Path "C:\BitNet-VC-Builder\data\memory"
```

2. Copy the configuration file:

```powershell
Copy-Item -Path "config\windows-production.yaml" -Destination "C:\BitNet-VC-Builder\config\config.yaml" -Force
```

3. Create a virtual environment and install dependencies:

```powershell
python -m venv "C:\BitNet-VC-Builder\venv"
& "C:\BitNet-VC-Builder\venv\Scripts\pip" install --upgrade pip
& "C:\BitNet-VC-Builder\venv\Scripts\pip" install -e ".[ui]"
```

4. Build the Tauri desktop application:

```powershell
cd tauri-ui
npm install
npm run tauri build
```

5. Copy the Tauri application to the production directory:

```powershell
Copy-Item -Path "tauri-ui\src-tauri\target\release\BitNet Virtual Co-worker Builder.exe" -Destination "C:\BitNet-VC-Builder\BitNet-VC-Builder.exe" -Force
```

## Starting the Application

After setting up the production environment, you can start the application in several ways:

### Using the Desktop Shortcuts

- **API Server**: Double-click the "BitNet VC Builder - API Server" shortcut on your desktop
- **Web UI**: Double-click the "BitNet VC Builder - Web UI" shortcut on your desktop
- **Desktop App**: Double-click the "BitNet VC Builder - Desktop App" shortcut on your desktop

### Using the Startup Script

Double-click the "Start BitNet VC Builder" shortcut on your desktop to start both the API server and web UI.

### Automatic Startup

If you used the automated setup script, the application will start automatically when you log in to Windows.

## Accessing the Application

- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Web UI**: http://localhost:8501
- **Desktop App**: Launch from the desktop shortcut

## Configuration

The production configuration file is located at `C:\BitNet-VC-Builder\config\config.yaml`. You can modify this file to change the application settings.

## Logs

Logs are stored in the `C:\BitNet-VC-Builder\logs` directory:

- **API Server**: `C:\BitNet-VC-Builder\logs\api.log`
- **Web UI**: `C:\BitNet-VC-Builder\logs\ui.log`

## Monitoring

The production environment includes a comprehensive monitoring system:

### Setting Up Monitoring

1. Open PowerShell as Administrator
2. Navigate to the BitNet_LLM_Virtual_Coworker_Builder\monitoring directory
3. Run the setup script:

```powershell
.\setup_monitoring.ps1
```

This will:
- Set up scheduled monitoring of the production environment
- Create a monitoring dashboard
- Configure email alerts for critical issues
- Monitor system resources, service status, and application logs

### Using the Monitoring Dashboard

1. Double-click the "BitNet VC Builder - Monitoring Dashboard" shortcut on your desktop
2. The dashboard will show the current status of the production environment, including:
   - Service status (API server, web UI)
   - System resources (CPU, memory, disk space)
   - Recent errors
   - Performance metrics

### Web-Based Monitoring Dashboard

You can also access the web-based monitoring dashboard:

```powershell
cd monitoring
python web_dashboard.py
```

The web dashboard will be available at http://localhost:8502.

## Backup and Recovery

The production environment includes a robust backup and recovery system:

### Setting Up Backups

1. Open PowerShell as Administrator
2. Navigate to the BitNet_LLM_Virtual_Coworker_Builder\backup directory
3. Run the setup script:

```powershell
.\setup_backup.ps1
```

This will:
- Set up scheduled backups of the production environment
- Configure retention policies for backups
- Create a backup management interface
- Set up restore capabilities for disaster recovery

### Managing Backups

1. Double-click the "BitNet VC Builder - Backup Management" shortcut on your desktop
2. The backup management interface will allow you to:
   - Create new backups
   - List available backups
   - Restore from a backup
   - Delete old backups

### Manual Backup

You can also create a backup manually:

```powershell
cd backup
.\backup.ps1
```

### Restoring from Backup

To restore from a backup:

1. Open the backup management interface
2. Select the backup to restore
3. Follow the prompts to restore the backup

## Troubleshooting

If you encounter any issues with the production setup, check the following:

1. **API Server Not Starting**:
   - Check the API server log at `C:\BitNet-VC-Builder\logs\api.log`
   - Ensure that port 8000 is not in use by another application

2. **Web UI Not Starting**:
   - Check the web UI log at `C:\BitNet-VC-Builder\logs\ui.log`
   - Ensure that port 8501 is not in use by another application

3. **Desktop App Not Starting**:
   - Try running the desktop app from the command line to see any error messages:
     ```powershell
     & "C:\BitNet-VC-Builder\BitNet-VC-Builder.exe"
     ```

4. **Dependencies Issues**:
   - Ensure that all dependencies are installed correctly:
     ```powershell
     & "C:\BitNet-VC-Builder\venv\Scripts\pip" install -e ".[ui]" --force-reinstall
     ```

5. **Monitoring Issues**:
   - Check the monitoring logs in the `C:\BitNet-VC-Builder\monitoring` directory
   - Ensure that the monitoring service is running

6. **Backup Issues**:
   - Check the backup logs in the `C:\BitNet-VC-Builder\backup` directory
   - Ensure that the backup directory exists and is writable

## Updating the Application

To update the application:

1. Get the latest code (either by pulling from the repository or copying the updated files)
2. Run the setup script again:
   ```powershell
   .\setup_production.ps1
   ```

This will update the application while preserving your configuration and data.

## Security Considerations

When deploying BitNet Virtual Co-worker Builder in a production environment, consider the following security best practices:

1. **Network Security**:
   - Use a firewall to restrict access to the API server and web UI
   - Consider using HTTPS for the API server and web UI
   - Limit access to the production environment to authorized users only

2. **Authentication and Authorization**:
   - Enable authentication for the API server and web UI
   - Configure user accounts with appropriate permissions
   - Use strong passwords for all accounts

3. **Data Security**:
   - Encrypt sensitive data in the database
   - Use secure connections for database access
   - Regularly backup the database and store backups securely

4. **System Security**:
   - Keep the operating system and all software up to date
   - Use antivirus software and keep it updated
   - Implement a security monitoring system

5. **Physical Security**:
   - Secure the physical server or workstation running the application
   - Restrict physical access to authorized personnel only
   - Implement disaster recovery procedures

## Performance Tuning

To optimize the performance of BitNet Virtual Co-worker Builder in a production environment:

1. **Hardware Recommendations**:
   - CPU: 4+ cores
   - RAM: 8+ GB
   - Disk: SSD with at least 100 GB free space

2. **Configuration Tuning**:
   - Adjust the number of worker processes based on available CPU cores
   - Optimize the database connection pool size
   - Configure appropriate cache sizes

3. **Model Optimization**:
   - Use the optimized BitNet models for production
   - Adjust the number of threads based on available CPU cores
   - Configure appropriate context size and generation parameters

4. **Monitoring and Scaling**:
   - Monitor system resource usage and application performance
   - Scale horizontally by adding more instances if needed
   - Implement load balancing for high-availability deployments

## Support

If you need assistance with the production setup, please contact the BitNet Virtual Co-worker Builder support team or open an issue on GitHub.
