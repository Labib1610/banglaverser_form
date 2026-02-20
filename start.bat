@echo off
REM BanglaVerse Evaluation Form - Windows Startup Script

echo.
echo Starting BanglaVerse Evaluation Form...
echo.

REM Check if manage.py exists
if not exist manage.py (
    echo Error: manage.py not found!
    echo Please run this script from the banglaverser_form directory.
    pause
    exit /b 1
)

REM Check if Django is installed
python -c "import django" 2>nul
if errorlevel 1 (
    echo Django not found! Installing Django...
    pip install django
)

REM Check if database exists
if not exist db.sqlite3 (
    echo Database not found. Running migrations...
    python manage.py migrate
    echo.
    echo Creating superuser account...
    python manage.py createsuperuser
)

echo.
echo Starting development server...
echo.
echo Access the application at:
echo   - Main form: http://127.0.0.1:8000/
echo   - Admin panel: http://127.0.0.1:8000/admin/
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

pause
