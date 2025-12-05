@echo off
echo Building Vue Frontend...
cd frontend
call npm install
call npm run build
if %errorlevel% neq 0 exit /b %errorlevel%

echo Creating backend static directory...
cd ..
if not exist "backend\static" mkdir "backend\static"

echo Copying build files to backend...
xcopy "frontend\dist\*" "backend\static\" /E /I /Y

echo Done! You can now deploy the 'backend' folder to Vercel.
