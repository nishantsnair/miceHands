@echo off & title %~nx0 & color 5F
@REM        BG              FG
    @REM 0 = Black       8 = Gray
    @REM 1 = Blue        9 = Light Blue
    @REM 2 = Green       A = Light Green
    @REM 3 = Aqua        B = Light Aqua
    @REM 4 = Red         C = Light Red
    @REM 5 = Purple      D = Light Purple
    @REM 6 = Yellow      E = Light Yellow
    @REM 7 = White       F = Bright White
@REM @set pithon = .venv\Scripts\python
@REM @set pyp = .venv\l\Scripts\pip
goto :DOES_PYTHON_EXIST

:DOES_PYTHON_EXIST
py -V | find /v "Python" >NUL 2>NUL && (goto :PYTHON_DOES_NOT_EXIST)
py -V | find "Python"    >NUL 2>NUL && (goto :PYTHON_DOES_EXIST)
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
    echo virtual environment detected, Activating
    call .venv\Scripts\activate
    echo virtual environment activated
    call python gui.py

) else (
    echo virtual environment not found
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