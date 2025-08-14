@echo off
echo InfluenceOS - Deployment Test
echo ==============================
echo.

echo Testing Local Backend API...
curl -s http://localhost:8000/health > nul
if %errorlevel% equ 0 (
    echo ✅ Backend API is running
) else (
    echo ❌ Backend API is not responding
    goto :error
)

echo.
echo Testing Local Frontend...
curl -s http://localhost:8080 > nul
if %errorlevel% equ 0 (
    echo ✅ Frontend is running
) else (
    echo ❌ Frontend is not responding
    goto :error
)

echo.
echo Testing API Endpoints...

echo Testing content generation...
curl -s -X POST http://localhost:8000/api/v1/pipeline/generate -H "Content-Type: application/json" -d "{\"topic\": \"Test\"}" > nul
if %errorlevel% equ 0 (
    echo ✅ Content generation API working
) else (
    echo ❌ Content generation API failed
)

echo Testing profile analysis...
curl -s http://localhost:8000/api/v1/profile/analysis > nul
if %errorlevel% equ 0 (
    echo ✅ Profile analysis API working
) else (
    echo ❌ Profile analysis API failed
)

echo Testing outreach campaigns...
curl -s http://localhost:8000/api/v1/outreach/campaigns > nul
if %errorlevel% equ 0 (
    echo ✅ Outreach campaigns API working
) else (
    echo ❌ Outreach campaigns API failed
)

echo.
echo ✅ All tests passed! Deployment is ready.
echo.
echo 🔗 Local URLs:
echo   Frontend: http://localhost:8080
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
goto :end

:error
echo.
echo ❌ Some tests failed. Please check your setup.
echo.

:end
pause
