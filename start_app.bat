@echo off
REM Sentiment Analyzer Startup Script for Windows
REM This batch file provides an alternative way to start the application on Windows

echo 🎭 Sentiment Analyzer - Windows Startup Script
echo =============================================

REM Check if we're in the right directory
if not exist "backend\main.py" (
    echo ❌ backend\main.py not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

if not exist "frontend\app.py" (
    echo ❌ frontend\app.py not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ⚠️ Virtual environment not found
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

echo 🔄 Installing/updating requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

echo 🔍 Testing setup...
python test_setup.py
if errorlevel 1 (
    echo ⚠️ Setup test had issues, but continuing...
    timeout /t 3
)

echo.
echo 🚀 Starting application...
echo.
echo Choose startup method:
echo 1. Automatic startup (recommended)
echo 2. Manual startup (two separate windows)
echo 3. Exit
echo.
set /p choice=Enter your choice (1-3): 

if "%choice%"=="1" goto automatic
if "%choice%"=="2" goto manual
if "%choice%"=="3" goto end
echo Invalid choice, using automatic startup...

:automatic
echo.
echo 🤖 Starting automatic mode...
python start_app.py
goto end

:manual
echo.
echo 📝 Manual startup mode
echo Opening two command windows...
echo.
echo Starting backend in new window...
start "Sentiment Analyzer Backend" cmd /k "call venv\Scripts\activate.bat && uvicorn backend.main:app --reload"

echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak

echo Starting frontend in new window...
start "Sentiment Analyzer Frontend" cmd /k "call venv\Scripts\activate.bat && streamlit run frontend\app.py"

echo.
echo ✅ Both services should be starting in separate windows
echo 🌐 Frontend: http://localhost:8501
echo 🔧 Backend: http://localhost:8000
echo.
echo Press any key to exit this window...
pause > nul
goto end

:end
echo.
echo 👋 Goodbye!
pause