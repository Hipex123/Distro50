@echo off
::IF "%1" == "-r" cmd /k "python main.py -r & set EXITCODE=%ERRORLEVEL% & cd %origin%" IF %EXITCODE% == 1 cmd /k "cd %~dp0..\src & python main.py -r & cd %origin%"
set "origin=%cd%"
cd %~dp0..\src

IF "%1" == "" cmd /k "python main.py -h & cd %origin%"

IF "%1" == "--share" IF "%2" =="--help" cmd /k "python main.py -s & cd %origin%"
IF "%1" == "--help" IF "%2" =="--share" cmd /k "python main.py -s & cd %origin%"

IF "%1" == "--run" IF "%2" =="--share" cmd /k "python main.py -rs & cd %origin%"
IF "%1" == "--share" IF "%2" =="--run" cmd /k "python main.py -sr & cd %origin%"

IF "%1" == "--help" IF "%2" =="--run" cmd /k "python main.py -r & cd %origin%"
IF "%1" == "--run" IF "%2" =="--help" cmd /k "python main.py -r & cd %origin%"


IF "%1" == "-s" IF "%2" =="-h" cmd /k "python main.py -s & cd %origin%"
IF "%1" == "-h" IF "%2" =="-s" cmd /k "python main.py -s & cd %origin%"

IF "%1" == "-r" IF "%2" =="-s" cmd /k "python main.py -rs & cd %origin%"
IF "%1" == "-s" IF "%2" =="-r" cmd /k "python main.py -sr & cd %origin%"

IF "%1" == "-h" IF "%2" =="-r" cmd /k "python main.py -r & cd %origin%"
IF "%1" == "-r" IF "%2" =="-h" cmd /k "python main.py -r & cd %origin%"


IF "%1" == "-s" cmd /k "python main.py -s & cd %origin%"
IF "%1" == "-h" cmd /k "python main.py -h & cd %origin%"
IF "%1" == "-r" cmd /k "python main.py -r & cd %origin%"

IF "%1" == "--share" cmd /k "python main.py -s & cd %origin%"
IF "%1" == "--help" cmd /k "python main.py -h & cd %origin%"
IF "%1" == "--run" cmd /k "python main.py -r & cd %origin%"


IF "%1" == "-rh" cmd /k "python main.py -r & cd %origin%"
IF "%1" == "-hr" cmd /k "python main.py -r & cd %origin%"

IF "%1" == "-sr" cmd /k "python main.py -sr & cd %origin%"
IF "%1" == "-rs" (
    cmd /k "python main.py -rs & cd %origin%"
) ELSE (
    cmd /k "python main.py -h & cd %origin%"
)
