Write-Host "Starting CivicQuest Backend and Frontend..." -ForegroundColor Green

# Start Backend in a new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\Backend'; & .\venv\Scripts\python.exe -m uvicorn app.main:app --port 8000 --reload"

# Start Frontend in a new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\Frontend'; npm run dev"

Write-Host "Both servers launched in separate windows!" -ForegroundColor Cyan
Write-Host "Backend:  http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Yellow
