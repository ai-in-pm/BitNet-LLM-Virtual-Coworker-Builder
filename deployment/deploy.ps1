# Production deployment script for BitNet_LLM_Virtual_Coworker_Builder on Windows
param (
    [string]$Branch = "main",
    [string]$ConfigFile = "windows-production.yaml",
    [string]$InstallDir = "C:\BitNet-VC-Builder"
)

# Configuration
$AppName = "bitnet-vc-builder"
$DeployDir = $InstallDir
$LogDir = "$DeployDir\logs"
$ConfigDir = "$DeployDir\config"
$DataDir = "$DeployDir\data"
$VenvDir = "$DeployDir\venv"
$RepoUrl = "https://github.com/ai-in-pm/BitNet-LLM-Virtual-Coworker-Builder.git"
$CurrentDir = "C:\Users\djjme\OneDrive\Desktop\CC-Directory\BitNet-main\BitNet_LLM_Virtual_Coworker_Builder"

Write-Host "=== BitNet Virtual Co-worker Builder Deployment ===" -ForegroundColor Cyan
Write-Host "Branch: $Branch" -ForegroundColor Cyan
Write-Host "Config: $ConfigFile" -ForegroundColor Cyan
Write-Host "Install Directory: $DeployDir" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Check if running as administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "This script must be run as Administrator" -ForegroundColor Red
    exit 1
}

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Git is not installed. Please install Git and try again." -ForegroundColor Red
    exit 1
}

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Python is installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python is not installed. Please install Python and try again." -ForegroundColor Red
    exit 1
}

# Create directories
Write-Host "Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $DeployDir | Out-Null
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
New-Item -ItemType Directory -Force -Path $ConfigDir | Out-Null
New-Item -ItemType Directory -Force -Path $DataDir | Out-Null
New-Item -ItemType Directory -Force -Path "$DataDir\models" | Out-Null
New-Item -ItemType Directory -Force -Path "$DataDir\cache" | Out-Null
New-Item -ItemType Directory -Force -Path "$DataDir\memory" | Out-Null

# Use existing repository or clone a new one
$RepoDir = "$DeployDir\repo"
if (Test-Path $CurrentDir) {
    Write-Host "Using existing repository..." -ForegroundColor Yellow
    if (-not (Test-Path $RepoDir)) {
        Write-Host "Copying repository to deployment directory..." -ForegroundColor Yellow
        Copy-Item -Path $CurrentDir -Destination $RepoDir -Recurse -Force
    } else {
        Write-Host "Repository already exists in deployment directory..." -ForegroundColor Yellow
    }
} else {
    # Clone or update repository
    if (Test-Path $RepoDir) {
        Write-Host "Updating repository..." -ForegroundColor Yellow
        Set-Location $RepoDir
        git fetch --all
        git checkout $Branch
        git pull
    } else {
        Write-Host "Cloning repository..." -ForegroundColor Yellow
        git clone $RepoUrl $RepoDir
        Set-Location $RepoDir
        git checkout $Branch
    }
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path $VenvDir)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $VenvDir
}

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& "$VenvDir\Scripts\pip" install --upgrade pip
& "$VenvDir\Scripts\pip" install -e "$RepoDir[ui]"

# Copy configuration
Write-Host "Copying configuration..." -ForegroundColor Yellow
Copy-Item "$RepoDir\config\$ConfigFile" -Destination "$ConfigDir\config.yaml" -Force

# Create Windows services using NSSM (Non-Sucking Service Manager)
# Check if NSSM is installed
$nssmPath = "C:\Program Files\nssm\nssm.exe"
if (-not (Test-Path $nssmPath)) {
    Write-Host "NSSM is not installed. Please install NSSM and try again." -ForegroundColor Red
    Write-Host "You can download NSSM from https://nssm.cc/" -ForegroundColor Yellow
    Write-Host "Alternatively, you can run the services manually:" -ForegroundColor Yellow
    Write-Host "API Server: $VenvDir\Scripts\python -m bitnet_vc_builder.api.server --config $ConfigDir\config.yaml" -ForegroundColor Yellow
    Write-Host "Web UI: $VenvDir\Scripts\python -m bitnet_vc_builder.ui.web.app --config $ConfigDir\config.yaml" -ForegroundColor Yellow
} else {
    # Create Windows service for API server
    Write-Host "Creating Windows service for API server..." -ForegroundColor Yellow
    & $nssmPath install "$AppName-api" "$VenvDir\Scripts\python.exe"
    & $nssmPath set "$AppName-api" AppParameters "-m bitnet_vc_builder.api.server --config $ConfigDir\config.yaml"
    & $nssmPath set "$AppName-api" AppDirectory "$RepoDir"
    & $nssmPath set "$AppName-api" AppEnvironmentExtra "CONFIG_PATH=$ConfigDir\config.yaml" "PYTHONPATH=$RepoDir"
    & $nssmPath set "$AppName-api" DisplayName "BitNet Virtual Co-worker Builder API Server"
    & $nssmPath set "$AppName-api" Description "API server for BitNet Virtual Co-worker Builder"
    & $nssmPath set "$AppName-api" Start SERVICE_AUTO_START
    & $nssmPath set "$AppName-api" AppStdout "$LogDir\api.log"
    & $nssmPath set "$AppName-api" AppStderr "$LogDir\api.error.log"

    # Create Windows service for Web UI
    Write-Host "Creating Windows service for Web UI..." -ForegroundColor Yellow
    & $nssmPath install "$AppName-ui" "$VenvDir\Scripts\python.exe"
    & $nssmPath set "$AppName-ui" AppParameters "-m bitnet_vc_builder.ui.web.app --config $ConfigDir\config.yaml"
    & $nssmPath set "$AppName-ui" AppDirectory "$RepoDir"
    & $nssmPath set "$AppName-ui" AppEnvironmentExtra "CONFIG_PATH=$ConfigDir\config.yaml" "PYTHONPATH=$RepoDir"
    & $nssmPath set "$AppName-ui" DisplayName "BitNet Virtual Co-worker Builder Web UI"
    & $nssmPath set "$AppName-ui" Description "Web UI for BitNet Virtual Co-worker Builder"
    & $nssmPath set "$AppName-ui" Start SERVICE_AUTO_START
    & $nssmPath set "$AppName-ui" AppStdout "$LogDir\ui.log"
    & $nssmPath set "$AppName-ui" AppStderr "$LogDir\ui.error.log"

    # Start services
    Write-Host "Starting services..." -ForegroundColor Yellow
    Start-Service "$AppName-api"
    Start-Service "$AppName-ui"

    # Check service status
    Write-Host "Checking service status..." -ForegroundColor Yellow
    Get-Service "$AppName-api"
    Get-Service "$AppName-ui"
}

# Create desktop shortcuts
Write-Host "Creating desktop shortcuts..." -ForegroundColor Yellow
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\$AppName-api.lnk")
$Shortcut.TargetPath = "$VenvDir\Scripts\python.exe"
$Shortcut.Arguments = "-m bitnet_vc_builder.api.server --config $ConfigDir\config.yaml"
$Shortcut.WorkingDirectory = "$RepoDir"
$Shortcut.Save()

$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\$AppName-ui.lnk")
$Shortcut.TargetPath = "$VenvDir\Scripts\python.exe"
$Shortcut.Arguments = "-m bitnet_vc_builder.ui.web.app --config $ConfigDir\config.yaml"
$Shortcut.WorkingDirectory = "$RepoDir"
$Shortcut.Save()

Write-Host "=== Deployment Complete ===" -ForegroundColor Green
Write-Host "API Server: http://localhost:8000" -ForegroundColor Green
Write-Host "Web UI: http://localhost:8501" -ForegroundColor Green
Write-Host "Logs: $LogDir" -ForegroundColor Green
Write-Host "Configuration: $ConfigDir\config.yaml" -ForegroundColor Green
Write-Host "==========================" -ForegroundColor Green
