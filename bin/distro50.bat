@echo off

set "origin=%cd%"

py --version >nul
if %ERRORLEVEL% neq 0 (
    echo Python not found
    echo Go on https://www.python.org/downloads/ and download newer version of python (3.10.11 or higher)
)

for /f "tokens=2" %%G in ('py --version 2^>^&1') do (
    set "pythonVersion=%%G"
)

if %pythonVersion% lss 3.10.11 (
    echo Python is not up to date
    echo Go on https://www.python.org/downloads/ and download newer version of python (3.10.11 or higher)
)

py --version >nul
if %ERRORLEVEL% neq 0 (
    echo Python installation failed.
    exit /b %errorlevel%
)

pip --version >nul
if %ERRORLEVEL% neq 0 (
    echo Pip not found.
    set /p "userInputTh=Would you like to install pip (y/n):"
)

if %userInputTh%==y (
    echo Installing pip...
    py -3 -m ensurepip
) else if %userInputTh%00n (
    exit
) else (
    echo Option not recognised. Exiting...
    exit
)

for /f "tokens=*" %%i in ('pip --version') do (
    set "pip_version=%%i"
)

for /f "tokens=2 delims= " %%a in ("%pip_version%") do (
    set "pipVersion=%%a"
)


if "%pipVersion%" lss "24.0" (
    echo Pip may not be compatible.
    set /p "userInputF=Would you like to install pip (y/n):"

    if "%userInputF%"==y (
        echo Upgrading pip...
        py -3 -m ensurepip
    ) else if "%userInputF%"==n (
        echo
    ) else (
        echo Option not recognised. Exiting...
        exit
    )
)


pip --version > nul
if %ERRORLEVEL% neq 0 (
    echo Pip installation failed.
    exit /b %errorlevel%
)

cd %~dp0..

for /f "usebackq tokens=*" %%a in ("requirements.txt") do (
    pip show %%a >nul 2>&1
    if %errorlevel% equ 0 (
        REM pass
    ) else (
        pip install %%a --user
    )
)

cd src

cmd /k "python main.py %1 %2 %3 & cd %origin%"
