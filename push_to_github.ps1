# Script to push changes to GitHub
# Run this script as Administrator

# Configuration
$RepoDir = "C:\Users\djjme\OneDrive\Desktop\CC-Directory\BitNet-main\BitNet_LLM_Virtual_Coworker_Builder"
$RemoteUrl = "https://github.com/ai-in-pm/BitNet-LLM-Virtual-Coworker-Builder.git"
$Branch = "main"
$CommitMessage = "Add production setup, monitoring, and backup systems"

# Navigate to the repository directory
Set-Location $RepoDir

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Git is not installed. Please install Git and try again." -ForegroundColor Red
    exit 1
}

# Check if the directory is a Git repository
if (-not (Test-Path -Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    
    # Add the remote
    git remote add origin $RemoteUrl
    
    # Create a .gitignore file if it doesn't exist
    if (-not (Test-Path -Path ".gitignore")) {
        Write-Host "Creating .gitignore file..." -ForegroundColor Yellow
        Copy-Item -Path "C:\Users\djjme\OneDrive\Desktop\CC-Directory\BitNet-main\BitNet_LLM_Virtual_Coworker_Builder\.gitignore" -Destination ".gitignore"
    }
}

# Check remote
$remotes = git remote -v
if ($remotes -notcontains "origin") {
    Write-Host "Adding remote origin..." -ForegroundColor Yellow
    git remote add origin $RemoteUrl
}

# Stage all changes
Write-Host "Staging changes..." -ForegroundColor Yellow
git add .

# Commit changes
Write-Host "Committing changes..." -ForegroundColor Yellow
git commit -m $CommitMessage

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin $Branch

Write-Host "Changes pushed to GitHub successfully!" -ForegroundColor Green
