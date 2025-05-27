@echo off
echo ============================================
echo       CMS Deployment Script for Linux
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

echo Step 3: Creating Linux deployment package...
if exist "deploy_linux" rmdir /s /q deploy_linux
mkdir deploy_linux

echo Copying backend files...
xcopy backend deploy_linux\backend\ /e /i /h /y
if not exist "deploy_linux\backend" mkdir deploy_linux\backend

echo Copying frontend build...
xcopy frontend\build deploy_linux\ /e /i /h /y

echo Copying Linux configuration files...
copy .htaccess deploy_linux\
copy make_executable.sh deploy_linux\

echo ============================================
echo Linux deployment package created in 'deploy_linux' folder!
echo ============================================

echo Next steps for Linux hosting:
echo 1. Upload the 'deploy_linux' folder contents to your web root
echo 2. Run: chmod +x backend/wsgi.py backend/app.py
echo 3. Set environment variables in hosting control panel:
echo    - SECRET_KEY=your-secure-key-here
echo    - JWT_SECRET_KEY=your-jwt-key-here
echo    - FLASK_ENV=production
echo 4. Create admin user (see README_DEPLOY.md)
echo.
pause 