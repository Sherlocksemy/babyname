$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location (Join-Path $root "frontend")

$existing = Get-NetTCPConnection -State Listen -LocalPort 3000 -ErrorAction SilentlyContinue
if ($existing) {
    $owned = Get-CimInstance Win32_Process | Where-Object {
        $_.ProcessId -eq $existing.OwningProcess -and $_.CommandLine -like "*baby-name-system*frontend*"
    }
    if (-not $owned) {
        throw "Port 3000 is already in use by another process. Stop it before starting frontend."
    }
}

npm.cmd run dev
