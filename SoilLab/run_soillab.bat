@echo off
cd /d "%~dp0"
echo ==========================================
echo             Starting SoilLab
echo ==========================================

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m streamlit run app.py
) else (
    echo Project environment not found. Trying the Python launcher...
    py -3.12 -m streamlit run app.py
    if errorlevel 1 (
        echo.
        echo Could not start SoilLab. Follow the README setup instructions.
    )
)
pause
