$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

Start-Process -FilePath powershell.exe -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-File", (Join-Path $PSScriptRoot "run_backend.ps1")
) -WorkingDirectory $root

Start-Process -FilePath powershell.exe -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-File", (Join-Path $PSScriptRoot "run_frontend.ps1")
) -WorkingDirectory $root
