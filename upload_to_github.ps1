<#
upload_to_github.ps1

PowerShell helper to initialize (if needed), add, commit, add remote (if missing) and push to GitHub.

Defaults are set using the repository info available in the workspace: owner 'aimee-bridges' and repo 'Cryptography'.

Usage examples:
  # push using SSH (default)
  .\upload_to_github.ps1 -Branch main -CommitMessage "Initial commit"

  # push using HTTPS (will prompt for credentials if needed)
  .\upload_to_github.ps1 -UseHttps -Branch main -CommitMessage "Add files"
#>
param(
    [string]$RemoteName = 'origin',
    [string]$RemoteUrl = 'git@github.com:aimee-bridges/Cryptography.git',
    [string]$Branch = 'main',
    [string]$CommitMessage = 'Add project files',
    [switch]$UseHttps
)

function Fail([string]$msg){
    Write-Error $msg
    exit 1
}

# Switch remote url to HTTPS if requested
if ($UseHttps) {
    $RemoteUrl = 'https://github.com/aimee-bridges/Cryptography.git'
}

# Ensure git is present
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Fail 'Git is not installed or not on PATH. Please install Git before running this script.'
}

# Move to script's directory by default (so the script works when run from elsewhere)
Push-Location (Get-Location)
try {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
    if ($scriptDir -and (Test-Path $scriptDir)) { Set-Location $scriptDir }
} catch { }

# Check if inside a git repo
$inside = & git rev-parse --is-inside-work-tree 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Output 'Not a git repository. Initializing a new git repository...'
    & git init || Fail 'git init failed.'
} else {
    Write-Output 'Repository detected.'
}

# Stage all files
Write-Output 'Staging files...'
& git add .
if ($LASTEXITCODE -ne 0) { Fail 'git add failed.' }

# Commit if there are staged changes
$porcelain = & git status --porcelain
if ($porcelain) {
    Write-Output 'Committing changes...'
    & git commit -m $CommitMessage || Fail 'git commit failed. You may need to set user.name/user.email.'
} else {
    Write-Output 'No changes to commit.'
}

# Ensure the remote is configured
$existingRemote = $null
try {
    $existingRemote = (& git remote get-url $RemoteName 2>$null).Trim()
} catch { }

if (-not $existingRemote) {
    Write-Output "Adding remote '$RemoteName' -> $RemoteUrl"
    & git remote add $RemoteName $RemoteUrl || Fail "git remote add failed. Check the provided remote URL: $RemoteUrl"
} else {
    Write-Output "Remote '$RemoteName' already set to: $existingRemote"
}

# Push to remote
Write-Output "Pushing branch '$Branch' to '$RemoteName' (this may prompt for credentials)..."
# Use -u to set upstream if needed
& git push -u $RemoteName $Branch
if ($LASTEXITCODE -ne 0) {
    Write-Error "git push failed. Common causes: authentication required, branch protection, or remote mismatch."
    Write-Output 'If you are using HTTPS and need a Personal Access Token (PAT), you can configure credentials with Git Credential Manager or use an SSH key.'
    exit 1
}

Write-Output 'Push complete.'

# Return to previous location
Pop-Location
