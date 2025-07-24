@echo off

echo Running main.py to download and exctract data...
py main.py

if %ERRORLEVEL% neq 0 (
    echo Error occurred running main.py
    pause
    exit /b %ERRORLEVEL%
)

echo Launching Streamlit data viz...
py -m streamlit run dataviz.py

pause
