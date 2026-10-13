@echo off
setlocal EnableExtensions
cd /d "%~dp0.."
call h2\scripts\reset_and_create.bat
exit /b %ERRORLEVEL%
