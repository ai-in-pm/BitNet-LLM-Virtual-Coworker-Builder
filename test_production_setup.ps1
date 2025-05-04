# Test script for BitNet_LLM_Virtual_Coworker_Builder production setup
# This script checks if the production environment is set up correctly

# Configuration
$InstallDir = "C:\BitNet-VC-Builder"
$CurrentDir = "C:\Users\djjme\OneDrive\Desktop\CC-Directory\BitNet-main\BitNet_LLM_Virtual_Coworker_Builder"

Write-Host "=== BitNet Virtual Co-worker Builder Production Setup Test ===" -ForegroundColor Cyan
Write-Host "Current Directory: $CurrentDir" -ForegroundColor Cyan
Write-Host "Install Directory: $InstallDir" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Check if the installation directory exists
if (Test-Path $InstallDir) {
    Write-Host "✓ Installation directory exists: $InstallDir" -ForegroundColor Green
} else {
    Write-Host "✗ Installation directory does not exist: $InstallDir" -ForegroundColor Red
    Write-Host "  Please run the setup_production.ps1 script first" -ForegroundColor Yellow
}

# Check if the configuration file exists
if (Test-Path "$InstallDir\config\config.yaml") {
    Write-Host "✓ Configuration file exists: $InstallDir\config\config.yaml" -ForegroundColor Green
} else {
    Write-Host "✗ Configuration file does not exist: $InstallDir\config\config.yaml" -ForegroundColor Red
}

# Check if the virtual environment exists
if (Test-Path "$InstallDir\venv") {
    Write-Host "✓ Virtual environment exists: $InstallDir\venv" -ForegroundColor Green
} else {
    Write-Host "✗ Virtual environment does not exist: $InstallDir\venv" -ForegroundColor Red
}

# Check if the Python executable exists in the virtual environment
if (Test-Path "$InstallDir\venv\Scripts\python.exe") {
    Write-Host "✓ Python executable exists: $InstallDir\venv\Scripts\python.exe" -ForegroundColor Green
} else {
    Write-Host "✗ Python executable does not exist: $InstallDir\venv\Scripts\python.exe" -ForegroundColor Red
}

# Check if the desktop shortcuts exist
$DesktopPath = [Environment]::GetFolderPath("Desktop")
if (Test-Path "$DesktopPath\BitNet VC Builder - API Server.lnk") {
    Write-Host "✓ API Server shortcut exists: $DesktopPath\BitNet VC Builder - API Server.lnk" -ForegroundColor Green
} else {
    Write-Host "✗ API Server shortcut does not exist: $DesktopPath\BitNet VC Builder - API Server.lnk" -ForegroundColor Red
}

if (Test-Path "$DesktopPath\BitNet VC Builder - Web UI.lnk") {
    Write-Host "✓ Web UI shortcut exists: $DesktopPath\BitNet VC Builder - Web UI.lnk" -ForegroundColor Green
} else {
    Write-Host "✗ Web UI shortcut does not exist: $DesktopPath\BitNet VC Builder - Web UI.lnk" -ForegroundColor Red
}

if (Test-Path "$DesktopPath\Start BitNet VC Builder.lnk") {
    Write-Host "✓ Start shortcut exists: $DesktopPath\Start BitNet VC Builder.lnk" -ForegroundColor Green
} else {
    Write-Host "✗ Start shortcut does not exist: $DesktopPath\Start BitNet VC Builder.lnk" -ForegroundColor Red
}

# Check if the startup script exists
if (Test-Path "$InstallDir\start.bat") {
    Write-Host "✓ Startup script exists: $InstallDir\start.bat" -ForegroundColor Green
} else {
    Write-Host "✗ Startup script does not exist: $InstallDir\start.bat" -ForegroundColor Red
}

# Check if the Tauri application exists
if (Test-Path "$InstallDir\BitNet-VC-Builder.exe") {
    Write-Host "✓ Tauri application exists: $InstallDir\BitNet-VC-Builder.exe" -ForegroundColor Green
} else {
    Write-Host "✗ Tauri application does not exist: $InstallDir\BitNet-VC-Builder.exe" -ForegroundColor Red
    Write-Host "  This is normal if you haven't built the Tauri application yet" -ForegroundColor Yellow
}

# Check if the API server can be started
Write-Host "Testing API server..." -ForegroundColor Yellow
try {
    $process = Start-Process -FilePath "$InstallDir\venv\Scripts\python.exe" -ArgumentList "-c", "import bitnet_vc_builder; print('BitNet VC Builder version:', bitnet_vc_builder.__version__)" -NoNewWindow -PassThru -Wait
    if ($process.ExitCode -eq 0) {
        Write-Host "✓ API server package is installed correctly" -ForegroundColor Green
    } else {
        Write-Host "✗ API server package is not installed correctly" -ForegroundColor Red
    }
} catch {
    Write-Host "✗ Failed to test API server: $_" -ForegroundColor Red
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Production Setup Test Complete" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Instructions for manual testing
Write-Host "To manually test the production setup:" -ForegroundColor Yellow
Write-Host "1. Run the API server: Double-click the 'BitNet VC Builder - API Server' shortcut on your desktop" -ForegroundColor Yellow
Write-Host "2. Run the Web UI: Double-click the 'BitNet VC Builder - Web UI' shortcut on your desktop" -ForegroundColor Yellow
Write-Host "3. Or run both using the startup script: Double-click the 'Start BitNet VC Builder' shortcut on your desktop" -ForegroundColor Yellow
Write-Host "4. Access the API server at: http://localhost:8000" -ForegroundColor Yellow
Write-Host "5. Access the Web UI at: http://localhost:8501" -ForegroundColor Yellow
Write-Host "6. If the Tauri application is built, run it by double-clicking the 'BitNet VC Builder - Desktop App' shortcut on your desktop" -ForegroundColor Yellow
