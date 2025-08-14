@echo off
echo 🚀 LinkedIn Auto Agent - Push to GitHub
echo =====================================
echo.

echo 📋 Make sure you have created the GitHub repository first:
echo    Repository name: LinkedIn-Auto-Agent
echo    URL: https://github.com/Abhijeet-077/LinkedIn-Auto-Agent
echo.

echo 🔄 Pushing to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ Successfully pushed to GitHub!
    echo.
    echo 🌐 Your repository is now available at:
    echo    https://github.com/Abhijeet-077/LinkedIn-Auto-Agent
    echo.
    echo 📚 Next steps:
    echo    1. Enable GitHub Pages in repository settings
    echo    2. Deploy to Vercel for full-stack hosting
    echo    3. Add any additional collaborators
    echo    4. Set up branch protection rules
    echo.
) else (
    echo.
    echo ❌ Push failed! Please check:
    echo    1. Repository exists on GitHub
    echo    2. You have push permissions
    echo    3. Internet connection is stable
    echo.
)

pause
