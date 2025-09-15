@echo off
echo ⚛️ Starting Ocean Hazard Platform Frontend...

:: Navigate to frontend directory
cd frontend

:: Install dependencies
echo Installing dependencies...
yarn install

:: Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from example...
    copy .env.example .env
)

:: Start the frontend development server
echo Starting React development server...
yarn start

pause
