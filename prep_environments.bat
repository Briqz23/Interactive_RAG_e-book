@echo off
REM Ensure the script exits on any error
setlocal enabledelayedexpansion
set "errorlevel="
call :SetupEnvironment || exit /b 1
goto :End

:SetupEnvironment
REM Create a virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 exit /b 1

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 exit /b 1

REM Install dependencies
echo Installing dependencies from requirements_diffusion.txt
pip install -r requirements_diffusion.txt
if errorlevel 1 exit /b 1

echo Installing dependencies from requirements_LLM.txt
pip install -r requirements_LLM.txt
if errorlevel 1 exit /b 1

REM Instructions for running the project
echo.
echo ### How to run
echo.
echo Activate the virtual environment:
echo.
echo     call venv\Scripts\activate
echo.
echo Navigate to the correct directory:
echo.
echo     cd agentapi
echo.
echo Then, run the FastAPI server:
echo.
echo     uvicorn app.main:app --reload
echo.
echo Finally, run the Streamlit client:
echo.
echo     streamlit run client.py
echo.

goto :End

:End
endlocal
