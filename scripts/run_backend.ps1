$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$existing = Get-NetTCPConnection -State Listen -LocalPort 8000 -ErrorAction SilentlyContinue
if ($existing) {
    $owned = Get-CimInstance Win32_Process | Where-Object {
        $_.ProcessId -eq $existing.OwningProcess -and $_.CommandLine -like "*uvicorn backend.app.main:app*"
    }
    if (-not $owned) {
        throw "Port 8000 is already in use by another process. Stop it before starting backend."
    }
}

python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
