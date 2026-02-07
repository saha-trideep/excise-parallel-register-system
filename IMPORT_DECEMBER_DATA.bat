@echo off
echo Importing December Data...
echo.
cd /d "%~dp0"
python import_december_data.py
echo.
echo Done! Press any key to continue...
pause
