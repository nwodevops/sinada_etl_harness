@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "ENV=%~1"
if "%ENV%"=="" set "ENV=remote"

set "LOGDIR=%~dp0logs"
if not exist "%LOGDIR%" mkdir "%LOGDIR%"
for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd"') do set "STAMP=%%a"
set "LOGFILE=%LOGDIR%\init_%STAMP%.log"
set "STEP=%TEMP%\sinada_init_step.txt"

call :log === init %ENV% %date% %time% ===

where java >nul 2>&1
if errorlevel 1 goto :fail
if not exist "h2\lib\h2-2.4.240.jar" goto :fail
if not exist ".venv\Scripts\python.exe" goto :fail
if not exist "client_secret.json" goto :fail

call :log ==> Entorno %ENV%
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0switch-env.ps1" %ENV% > "%STEP%" 2>&1
set "RC=%ERRORLEVEL%"
call :append
if not "%RC%"=="0" goto :fail

call :log ==> Reset H2
call scripts\step_reset_h2.bat > "%STEP%" 2>&1
set "RC=%ERRORLEVEL%"
call :append
if not "%RC%"=="0" goto :fail

call :log ==> Python create STG
call scripts\step_create_stg.bat > "%STEP%" 2>&1
set "RC=%ERRORLEVEL%"
call :append
if not "%RC%"=="0" goto :fail

call :log ==> Cargar Sheets
call scripts\step_cargar_sheets.bat > "%STEP%" 2>&1
set "RC=%ERRORLEVEL%"
call :append
if not "%RC%"=="0" goto :fail

call :log ==> Python main
call scripts\step_main.bat > "%STEP%" 2>&1
set "RC=%ERRORLEVEL%"
call :append
if not "%RC%"=="0" goto :fail

findstr /C:"STG_GS1_SINADA_DERIV: " "%LOGFILE%" >nul || goto :fail
findstr /C:"STG_GS2_SINADA_DERIV: " "%LOGFILE%" >nul || goto :fail
findstr /C:"STG_GS1_SINADA_DERIV: 0 filas" "%LOGFILE%" >nul && goto :fail
findstr /C:"STG_GS2_SINADA_DERIV: 0 filas" "%LOGFILE%" >nul && goto :fail
findstr /C:"Salida RESULTADO" "%LOGFILE%" >nul || goto :fail
findstr /C:"Excel:" "%LOGFILE%" >nul || goto :fail
findstr /C:"Oracle RP_SINADA_DENUNCIAS_DERIVACIONES: " "%LOGFILE%" >nul || goto :fail
findstr /C:"${" "%LOGFILE%" >nul && goto :fail

echo HARNESS OK — ver CHECKPOINTS.md
echo HARNESS OK — ver CHECKPOINTS.md>> "%LOGFILE%"
exit /b 0

:append
type "%STEP%"
type "%STEP%" >> "%LOGFILE%"
exit /b 0

:log
echo %*
echo %*>> "%LOGFILE%"
exit /b 0

:fail
echo FAIL
echo FAIL>> "%LOGFILE%"
exit /b 1
