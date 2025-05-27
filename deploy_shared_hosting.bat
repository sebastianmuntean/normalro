@echo off
echo ================================================
echo     CMS Deployment for Shared Hosting (No SSH)
echo ================================================

echo Step 1: Building React Frontend...
cd frontend
call npm install
set GENERATE_SOURCEMAP=false
call npm run build
cd ..

echo Step 2: Creating shared hosting deployment package...
if exist "deploy_shared" rmdir /s /q deploy_shared
mkdir deploy_shared

echo Copying backend files...
xcopy backend deploy_shared\backend\ /e /i /h /y

echo Copying frontend build...
xcopy frontend\build deploy_shared\ /e /i /h /y

echo Copying shared hosting configuration...
copy .htaccess deploy_shared\

echo ================================================
echo   Shared hosting deployment package created!
echo ================================================

echo.
echo MANUAL DEPLOYMENT STEPS:
echo ========================
echo.
echo 1. Upload 'deploy_shared' folder contents to your website root
echo    (usually public_html or www folder)
echo.
echo 2. In your hosting control panel:
echo    - Go to "Environment Variables" or "PHP/Python Config"
echo    - Set these variables:
echo      SECRET_KEY = your-secure-random-key-here
echo      JWT_SECRET_KEY = your-jwt-secure-key-here
echo      FLASK_ENV = production
echo.
echo 3. If your host supports Python app setup:
echo    - Enable Python/CGI execution
echo    - Set Python version to 3.x
echo.
echo 4. Create admin user by visiting:
echo    https://your-domain.com/api/init-admin
echo.
echo 5. Test the site:
echo    - Frontend: https://your-domain.com
echo    - API test: https://your-domain.com/api/pages
echo.
echo NOTE: Some hosts may need the Python path updated in .htaccess
echo       Change '/home/your-username/public_html/backend' to your actual path
echo.
pause 