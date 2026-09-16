@echo off
echo Stopping CivicQuest servers (Frontend on port 3000, Backend on port 8000)...

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ports = @(3000, 8000); $pids = (Get-NetTCPConnection -LocalPort $ports -State Listen -ErrorAction SilentlyContinue).OwningProcess | Select-Object -Unique; foreach ($p in $pids) { if ($p -gt 0) { taskkill.exe /F /T /PID $p 2>$null } }; Get-Process cmd -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like '*CivicQuest*' } | ForEach-Object { taskkill.exe /F /T /PID $_.Id 2>$null }"

echo CivicQuest servers stopped successfully!
