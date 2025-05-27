@echo off
echo Building React application for production...

REM Install dependencies
echo Installing dependencies...
npm install

REM Build the application
echo Building application...
set GENERATE_SOURCEMAP=false
npm run build

echo Build completed! Files are in the 'build' directory.
pause 