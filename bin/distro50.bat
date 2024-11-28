@echo off

pushd %~dp0..

set missingPackages=0

pip show gradio >nul
if %errorlevel% neq 0 set missingPackages=1

pip show qrcode >nul
if %errorlevel% neq 0 set missingPackages=1

pip show pillow >nul
if %errorlevel% neq 0 set missingPackages=1

if %missingPackages% equ 1 pip install -r requirements.txt --user

cd src

python main.py %1 %2 %3

popd
