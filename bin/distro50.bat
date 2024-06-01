@echo off

python -m pip install --upgrade pip

set "origin=%cd%"

cd %~dp0..

pip install -r requirements.txt

cd src

cmd /k "python main.py %1 %2 %3 & cd %origin%"
