@echo off
echo InfluenceOS - LinkedIn Agent
echo ========================
echo.
echo Starting Backend Server...
start "Backend Server" cmd /k "cd Backend && python working_server.py"
echo.
echo Starting Frontend Development Server...
start "Frontend Server" cmd /k "cd Frontend && npm run dev"
echo.
echo Both servers are starting...
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:8080
echo.
pause
