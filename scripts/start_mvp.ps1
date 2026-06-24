$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$BackendCommand = "`$env:PYTHONPATH='02_src'; python -m uvicorn backend.app.api.main:app --reload --port 8000"
$FrontendCommand = "cd 02_src/frontend; npm.cmd install; npm.cmd run dev"

Write-Host "Project root: $Root"
Write-Host ""
Write-Host "Backend:"
Write-Host "  $BackendCommand"
Write-Host ""
Write-Host "Frontend:"
Write-Host "  $FrontendCommand"
Write-Host ""
Write-Host "Swagger:  http://127.0.0.1:8000/docs"
Write-Host "Frontend: http://localhost:3000"
