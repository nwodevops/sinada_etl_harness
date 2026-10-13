@echo off
setlocal EnableExtensions
cd /d "%~dp0.."
call "%~dp0_py.bat"
if errorlevel 1 exit /b 1
"%PY%" python\create_stg.py
exit /b %ERRORLEVEL%
