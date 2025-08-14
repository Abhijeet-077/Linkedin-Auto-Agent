@echo off
echo InfluenceOS - LinkedIn Agent
echo ============================
echo.
echo Checking for busy ports and killing processes...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8080"') do taskkill /PID %%a /F >nul 2>&1
echo.
echo Starting Backend Server (FastAPI)...
start "InfluenceOS Backend" cmd /k "cd Backend && python working_server.py"
echo.
echo Starting Frontend Development Server (React + Vite)...
start "InfluenceOS Frontend" cmd /k "cd Frontend && npm run dev"
echo.
echo ✅ Both servers are starting...
echo 🔗 Backend API: http://localhost:8000
echo 🔗 Frontend App: http://localhost:8080
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause
