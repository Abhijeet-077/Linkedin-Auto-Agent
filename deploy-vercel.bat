@echo off
echo 🚀 LinkedIn Auto Agent - Vercel Deployment
echo ==========================================
echo.

echo 📋 Deployment Options:
echo.
echo 1. Frontend Only (Recommended for first deployment)
echo 2. Full-Stack (Frontend + Backend)
echo 3. Backend Only
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo 🎨 Deploying Frontend to Vercel...
    echo.
    cd Frontend
    vercel --prod
    cd ..
) else if "%choice%"=="2" (
    echo.
    echo 🔧 Deploying Full-Stack to Vercel...
    echo.
    vercel --prod
) else if "%choice%"=="3" (
    echo.
    echo ⚙️ Deploying Backend to Vercel...
    echo.
    cd Backend
    vercel --prod
    cd ..
) else (
    echo.
    echo ❌ Invalid choice. Please run the script again.
    goto :end
)

echo.
echo ✅ Deployment initiated!
echo.
echo 📋 Next steps:
echo 1. Check the Vercel dashboard for deployment status
echo 2. Configure custom domain if needed
echo 3. Set up environment variables in Vercel dashboard
echo 4. Test the deployed application
echo.
echo 🔗 Vercel Dashboard: https://vercel.com/dashboard
echo.

:end
pause
