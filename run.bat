@echo off & title %~nx0 & color 5F

goto :DOES_PYTHON_EXIST

:DOES_PYTHON_EXIST
python -V | find /v "Python" >NUL 2>NUL && (goto :PYTHON_DOES_NOT_EXIST)
python -V | find "Python"    >NUL 2>NUL && (goto :PYTHON_DOES_EXIST)
goto :PauseClosing

:PYTHON_DOES_NOT_EXIST
echo Python is not installed on your system.
echo Now opeing the download URL.
start "" "https://www.python.org/downloads/windows/"
goto :PauseClosing

:PYTHON_DOES_EXIST
:: This will retrieve Python 3.8.0 for example.
for /f "delims=" %%V in ('python -V') do @set ver=%%V
echo Congrats, %ver% is installed...
goto :VENV_SETUP

:VENV_SETUP
if exist .venv\ (
    call .venv\Scripts\activate
    call python detectPose.py

) else (
    echo Setting up venv
    call py -m pip install virtualenv
    call py -m venv .venv
    goto :VENV_SETUP
)

@REM if exist .venv\ (
@REM     .venv\Scripts\activate 

@REM ) else (
@REM     echo Setting up venv
@REM     pip install virtualenv
@REM     python -m venv .venv
@REM )
:PauseClosing
pause