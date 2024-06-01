@echo off

python -m pip install --upgrade pip
pip install -r requirements.txt

set "origin=%cd%"

cd %~dp0..
cd src

cmd /k "python main.py %1 %2 %3 & cd %origin%"
