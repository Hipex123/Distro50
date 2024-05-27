@echo off

set "origin=%cd%"
cd %~dp0..\src

set EXITCODE=0

cmd /k "python main.py %1 %2 %3 & set EXITCODE=%ERRORLEVEL% & cd %origin%"

IF %EXITCODE% == 1337 cmd /k "cd %~dp0..\src & python main.py %1 %2 %3 & cd %origin%"
