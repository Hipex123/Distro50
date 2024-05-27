@echo off

set "origin=%cd%"

where powershell >nul 2>&1
if %errorlevel% neq 0 (
    echo PowerShell is not available. Cannot proceed with installation.
    exit /b %errorlevel%
)

py --version > nul
if %ERRORLEVEL% neq 0 (
    echo Python not found.
    set /p "userInputO=Would you like to install python 3.10.11 (y/n):"
    
    if "%userinputO%"==y (
        powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe -OutFile python-installer.exe"

        if not exist python-installer.exe (
            echo Failed to download Python installer.
            exit /b 1
        )
        echo Installing Python...
        python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    ) else if "%userinputO%"==n (
        exit
    ) else (
        echo Option not recognised. Exiting...
        exit
    )
)

for /f "tokens=2" %%G in ('py --version 2^>^&1') do (
    set "pythonVersion=%%G"
)

if %pythonVersion% lss 3.10.11 (
    echo Python is not up to date.
    set /p "userInputT=Would you like to install python 3.10.11 (y/n):"

    if "%userInputT%"==y (
        powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe -OutFile python-installer.exe"

        if not exist python-installer.exe (
            echo Failed to download Python installer.
            exit /b 1
        )
        echo Installing Python...
        python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    ) else if "%userInputT%"==n (
        echo
    ) else (
        echo Option not recognised. Exiting...
        exit
    )
)

py --version > nul
if %ERRORLEVEL% neq 0 (
    echo Python installation failed.
    exit /b %errorlevel%
)

pip --version > nul
if %ERRORLEVEL% neq 0 (
    echo Pip not found.
    set /p "userInputTh=Would you like to install pip 24.0 (y/n):"

    if "%userInputTh%"==y (
        echo Installing pip...
        python -m pip install pip==24.0
    ) else if "%userInputTh%"==n (
        exit
    ) else (
        echo Option not recognised. Exiting...
        exit
    )
)

for /f "tokens=*" %%i in ('pip --version') do (
    set "pip_version=%%i"
)

for /f "tokens=2 delims= " %%a in ("%pip_version%") do (
    set "pipVersion=%%a"
)


if "%pipVersion%" lss "24.0" (
    echo Pip may not be compatible.
    set /p "userInputF=Would you like to install pip 24.0 (y/n):"

    if "%userInputF%"==y (
        echo Upgrading pip...
        python -m pip install pip==24.0
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
