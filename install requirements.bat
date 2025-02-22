@echo off
echo Installing required Python packages...
REM Install ollama, gradio, and psutil (if not already installed)
python -m pip install ollama gradio psutil
echo.
echo Installation complete.
pause
