@echo off
set proj_command=%1
set arg1=%2

IF '%arg1%' NEQ 'app' goto cont

call %~dp0get_app.bat
set arg1=%curapp%

:cont 

@echo on
%python3% "%~dp0..\manage.py" %proj_command% %arg1% %3 %4 %5 %6
@echo.
@pause