@echo off
REM tools/asm-regen/ghidra-run-script.bat
REM  通用 headless 驱动：跑 ghidra_scripts/ 下的 Jython 脚本。
REM  注意：默认不加 -readOnly，脚本改动会被 Ghidra 保存进工程。
REM
REM  Usage:
REM    tools\asm-regen\ghidra-run-script.bat <ScriptName.py> [args...]
REM
REM  Example:
REM    tools\asm-regen\ghidra-run-script.bat ImportProjectLabels.py
REM    tools\asm-regen\ghidra-run-script.bat CreateCardStatsType.py

setlocal

if "%GHIDRA_HOME%"=="" set GHIDRA_HOME=D:\Software\ghidra_12.0.3_PUBLIC
set HEADLESS=%GHIDRA_HOME%\support\analyzeHeadless.bat

set REPO_ROOT=%~dp0..\..
set PROJECT_DIR=%REPO_ROOT%\ghidra
set PROJECT_NAME=Yu-Gi-Oh WCT 2006
set SCRIPT_DIR=%REPO_ROOT%\tools\ghidra-labeling
set PROCESS_NAME=2343.gba

if "%~1"=="" (
    echo Usage: %~nx0 ^<ScriptName.py^> [args...]
    exit /b 2
)

set SCRIPT_NAME=%~1
shift
set SCRIPT_ARGS=
:collect_args
if "%~1"=="" goto run
set SCRIPT_ARGS=%SCRIPT_ARGS% "%~1"
shift
goto collect_args

:run
if not exist "%HEADLESS%" (
    echo ERROR: %HEADLESS% not found. Set GHIDRA_HOME or check LOCAL.md
    exit /b 1
)

echo [ghidra-run] script=%SCRIPT_NAME% args=%SCRIPT_ARGS%

call "%HEADLESS%" "%PROJECT_DIR%" "%PROJECT_NAME%" ^
    -process "%PROCESS_NAME%" ^
    -noanalysis ^
    -scriptPath "%SCRIPT_DIR%" ^
    -postScript %SCRIPT_NAME% %SCRIPT_ARGS%

endlocal
