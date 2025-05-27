@echo off
echo ============================================
echo       CMS Deployment Script for Windows
echo ============================================

echo Step 1: Building React Frontend...
cd frontend
call npm install
set GENERATE_SOURCEMAP=false
call npm run build
cd ..

echo Step 2: Preparing Backend...
cd backend
pip install -r requirements.txt
cd ..

echo Step 3: Creating deployment package...
if exist "deploy" rmdir /s /q deploy
mkdir deploy

echo Copying backend files...
xcopy backend deploy\backend\ /e /i /h /y
if not exist "deploy\backend\instance" mkdir deploy\backend\instance

echo Copying frontend build...
xcopy frontend\build deploy\ /e /i /h /y

echo Copying configuration files...
copy web.config deploy\
copy README_DEPLOY.md deploy\

echo ============================================
echo Deployment package created in 'deploy' folder!
echo ============================================

echo Next steps:
echo 1. Upload the 'deploy' folder contents to your hosting provider
echo 2. Configure your hosting environment variables
echo 3. Update database settings if needed
echo.
pause 