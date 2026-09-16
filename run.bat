@echo off
echo Starting CivicQuest Backend and Frontend...

start "CivicQuest Backend (FastAPI)" cmd /k "cd /d %~dp0Backend && .\venv\Scripts\python.exe -m uvicorn app.main:app --port 8000 --reload"

start "CivicQuest Frontend (Next.js)" cmd /k "cd /d %~dp0Frontend && npm run dev"

echo Both servers launched in separate windows!
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:3000
