@echo off
echo 🌊 Starting Ocean Hazard Platform Backend...

:: Navigate to backend directory
cd backend

:: Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

:: Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from example...
    copy .env.example .env
)

:: Start the backend server
echo Starting FastAPI server...
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload

pause
