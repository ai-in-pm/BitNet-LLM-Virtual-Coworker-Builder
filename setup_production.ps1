# BitNet_LLM_Virtual_Coworker_Builder Production Setup Script
# This script sets up the BitNet_LLM_Virtual_Coworker_Builder for production use

# Configuration
$CurrentDir = "C:\Users\djjme\OneDrive\Desktop\CC-Directory\BitNet-main\BitNet_LLM_Virtual_Coworker_Builder"
$InstallDir = "C:\BitNet-VC-Builder"
$ConfigFile = "windows-production.yaml"

Write-Host "=== BitNet Virtual Co-worker Builder Production Setup ===" -ForegroundColor Cyan
Write-Host "Current Directory: $CurrentDir" -ForegroundColor Cyan
Write-Host "Install Directory: $InstallDir" -ForegroundColor Cyan
Write-Host "Config File: $ConfigFile" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Check if running as administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Please restart the script with administrator privileges" -ForegroundColor Red
    exit 1
}

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Python is installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python is not installed. Please install Python 3.8 or higher and try again." -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed (for Tauri)
try {
    $nodeVersion = node --version
    Write-Host "Node.js is installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "Node.js is not installed. Please install Node.js 14 or higher and try again." -ForegroundColor Red
    exit 1
}

# Check if npm is installed (for Tauri)
try {
    $npmVersion = npm --version
    Write-Host "npm is installed: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "npm is not installed. Please install npm and try again." -ForegroundColor Red
    exit 1
}

# Create production directories
Write-Host "Creating production directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
New-Item -ItemType Directory -Force -Path "$InstallDir\logs" | Out-Null
New-Item -ItemType Directory -Force -Path "$InstallDir\config" | Out-Null
New-Item -ItemType Directory -Force -Path "$InstallDir\data" | Out-Null
New-Item -ItemType Directory -Force -Path "$InstallDir\data\models" | Out-Null
New-Item -ItemType Directory -Force -Path "$InstallDir\data\cache" | Out-Null
New-Item -ItemType Directory -Force -Path "$InstallDir\data\memory" | Out-Null

# Copy configuration file
Write-Host "Copying configuration file..." -ForegroundColor Yellow
Copy-Item -Path "$CurrentDir\config\$ConfigFile" -Destination "$InstallDir\config\config.yaml" -Force

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv "$InstallDir\venv"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& "$InstallDir\venv\Scripts\pip" install --upgrade pip
& "$InstallDir\venv\Scripts\pip" install -e "$CurrentDir[ui]"

# Build Tauri application
Write-Host "Building Tauri application..." -ForegroundColor Yellow
Set-Location "$CurrentDir\tauri-ui"
npm install
npm run tauri build

# Copy Tauri application to install directory
Write-Host "Copying Tauri application to install directory..." -ForegroundColor Yellow
$TauriAppPath = "$CurrentDir\tauri-ui\src-tauri\target\release\BitNet Virtual Co-worker Builder.exe"
if (Test-Path $TauriAppPath) {
    Copy-Item -Path $TauriAppPath -Destination "$InstallDir\BitNet-VC-Builder.exe" -Force
    Write-Host "Tauri application copied successfully" -ForegroundColor Green
} else {
    Write-Host "Tauri application build failed or not found at $TauriAppPath" -ForegroundColor Red
}

# Create desktop shortcuts
Write-Host "Creating desktop shortcuts..." -ForegroundColor Yellow
$WshShell = New-Object -ComObject WScript.Shell

# API Server shortcut
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\BitNet VC Builder - API Server.lnk")
$Shortcut.TargetPath = "$InstallDir\venv\Scripts\python.exe"
$Shortcut.Arguments = "-m bitnet_vc_builder.api.server --config $InstallDir\config\config.yaml"
$Shortcut.WorkingDirectory = $CurrentDir
$Shortcut.Save()

# Web UI shortcut
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\BitNet VC Builder - Web UI.lnk")
$Shortcut.TargetPath = "$InstallDir\venv\Scripts\python.exe"
$Shortcut.Arguments = "-m bitnet_vc_builder.ui.web.app --config $InstallDir\config\config.yaml"
$Shortcut.WorkingDirectory = $CurrentDir
$Shortcut.Save()

# Desktop App shortcut
if (Test-Path "$InstallDir\BitNet-VC-Builder.exe") {
    $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\BitNet VC Builder - Desktop App.lnk")
    $Shortcut.TargetPath = "$InstallDir\BitNet-VC-Builder.exe"
    $Shortcut.WorkingDirectory = $InstallDir
    $Shortcut.Save()
}

# Create startup script
Write-Host "Creating startup script..." -ForegroundColor Yellow
$StartupScript = @"
@echo off
echo Starting BitNet Virtual Co-worker Builder API Server...
start "" "$InstallDir\venv\Scripts\python.exe" -m bitnet_vc_builder.api.server --config "$InstallDir\config\config.yaml"
echo API Server started!
echo.
echo Starting BitNet Virtual Co-worker Builder Web UI...
start "" "$InstallDir\venv\Scripts\python.exe" -m bitnet_vc_builder.ui.web.app --config "$InstallDir\config\config.yaml"
echo Web UI started!
echo.
echo BitNet Virtual Co-worker Builder is now running!
echo API Server: http://localhost:8000
echo Web UI: http://localhost:8501
echo.
echo Press any key to exit...
pause > nul
"@
$StartupScript | Out-File -FilePath "$InstallDir\start.bat" -Encoding ASCII

# Create startup shortcut
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Start BitNet VC Builder.lnk")
$Shortcut.TargetPath = "$InstallDir\start.bat"
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.Save()

# Add to startup folder (optional)
$StartupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$Shortcut = $WshShell.CreateShortcut("$StartupFolder\BitNet VC Builder.lnk")
$Shortcut.TargetPath = "$InstallDir\start.bat"
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.Save()

Write-Host "=== Production Setup Complete ===" -ForegroundColor Green
Write-Host "BitNet Virtual Co-worker Builder has been set up for production use." -ForegroundColor Green
Write-Host "Installation Directory: $InstallDir" -ForegroundColor Green
Write-Host "API Server: http://localhost:8000" -ForegroundColor Green
Write-Host "Web UI: http://localhost:8501" -ForegroundColor Green
Write-Host "Desktop App: $InstallDir\BitNet-VC-Builder.exe" -ForegroundColor Green
Write-Host "Startup Script: $InstallDir\start.bat" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host "To start the application, double-click the 'Start BitNet VC Builder' shortcut on your desktop." -ForegroundColor Yellow
Write-Host "The application will also start automatically when you log in to Windows." -ForegroundColor Yellow
