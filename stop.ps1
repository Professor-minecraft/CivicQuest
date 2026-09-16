Write-Host "Stopping CivicQuest servers (ports 3000 and 8000)..." -ForegroundColor Yellow

$ports = @(3000, 8000)
$pids = (Get-NetTCPConnection -LocalPort $ports -State Listen -ErrorAction SilentlyContinue).OwningProcess | Select-Object -Unique

foreach ($p in $pids) {
    if ($p -gt 0) {
        taskkill.exe /F /T /PID $p 2>$null
    }
}

Get-Process cmd -ErrorAction SilentlyContinue | Where-Object {
    $_.MainWindowTitle -like '*CivicQuest*'
} | ForEach-Object {
    taskkill.exe /F /T /PID $_.Id 2>$null
}

Write-Host "CivicQuest servers stopped successfully!" -ForegroundColor Green
