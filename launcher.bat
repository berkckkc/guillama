@echo off
REM Check if Ollama is running
tasklist /FI "IMAGENAME eq ollama*.exe" | find /I "ollama" >nul
if errorlevel 1 (
    echo Ollama is not running. Launching Ollama...
    start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Ollama\ollama app.exe"
    timeout /t 5 /nobreak >nul
) else (
    echo Ollama is already running.
)

REM Start the Gradio app by running start.py
echo Starting the Gradio app...
start "" python start.py
timeout /t 5 /nobreak >nul

REM Open the default browser to http://127.0.0.1:7860
echo Opening browser...
start "" "http://127.0.0.1:7860"
pause
