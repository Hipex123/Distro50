@echo off

::set "origin=%cd%"
cd %~dp0..\src
::set "filePath=%cd%"
::cd %origin%

IF "%1" == "" cmd /k "python main.py -h"

IF "%1" == "--share" IF "%2" =="--help" cmd /k "python main.py -s"
IF "%1" == "--help" IF "%2" =="--share" cmd /k "python main.py -s"

IF "%1" == "--run" IF "%2" =="--share" cmd /k "python main.py -rs"
IF "%1" == "--share" IF "%2" =="--run" cmd /k "python main.py -sr"

IF "%1" == "--help" IF "%2" =="--run" cmd /k "python main.py -r"
IF "%1" == "--run" IF "%2" =="--help" cmd /k "python main.py -r"


IF "%1" == "-s" IF "%2" =="-h" cmd /k "python main.py -s"
IF "%1" == "-h" IF "%2" =="-s" cmd /k "python main.py -s"

IF "%1" == "-r" IF "%2" =="-s" cmd /k "python main.py -rs"
IF "%1" == "-s" IF "%2" =="-r" cmd /k "python main.py -sr"

IF "%1" == "-h" IF "%2" =="-r" cmd /k "python main.py -r"
IF "%1" == "-r" IF "%2" =="-h" cmd /k "python main.py -r"


IF "%1" == "-s" cmd /k "python main.py -s"
IF "%1" == "-h" cmd /k "python main.py -h"
IF "%1" == "-r" cmd /k "python main.py -r"

IF "%1" == "--share" cmd /k "python main.py -s"
IF "%1" == "--help" cmd /k "python main.py -h"
IF "%1" == "--run" cmd /k "python main.py -r"


IF "%1" == "-rh" cmd /k "python main.py -r"
IF "%1" == "-hr" cmd /k "python main.py -r"

IF "%1" == "-sr" cmd /k "python main.py -sr"
IF "%1" == "-rs" (
    cmd /k "python main.py -rs"
) ELSE (
    cmd /k "python main.py -h"
)