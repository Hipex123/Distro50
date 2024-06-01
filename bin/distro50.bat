@echo off

python -m pip install --upgrade pip >nul

set "origin=%cd%"

cd %~dp0..

pip show gradio >nul
if %errorlevel% neq 0 (
    pip install -r requirements.txt
)

pip show qrcode >nul
if %errorlevel% neq 0 (
    pip install -r requirements.txt
)

pip show pillow >nul
if %errorlevel% neq 0 (
    pip install -r requirements.txt
)

cd src

cmd /k "python main.py %1 %2 %3 & cd %origin%"
