@echo off
REM tools/asm-regen/ghidra-export-range.bat
REM Run Ghidra's ExportRangeToGas.py in headless mode (no GUI).
REM
REM Usage:
REM   tools\asm-regen\ghidra-export-range.bat <start_hex> <end_hex> <output_path> [xrefs 0|1]
REM
REM Example:
REM   tools\asm-regen\ghidra-export-range.bat 080000c0 080001ff asm\all.s.raw

setlocal

if "%GHIDRA_HOME%"=="" set GHIDRA_HOME=D:\Software\ghidra_12.0.3_PUBLIC
set HEADLESS=%GHIDRA_HOME%\support\analyzeHeadless.bat

set REPO_ROOT=%~dp0..\..
set PROJECT_DIR=%REPO_ROOT%\ghidra
set PROJECT_NAME=Yu-Gi-Oh WCT 2006
set SCRIPT_DIR=%REPO_ROOT%\tools\asm-regen\ghidra
set PROCESS_NAME=2343.gba

if "%~3"=="" (
    echo Usage: %~nx0 ^<start_hex^> ^<end_hex^> ^<output_path^> [xrefs 0^|1]
    exit /b 2
)

set START=%~1
set END=%~2
set OUT=%~3
set XREFS=%~4
if "%XREFS%"=="" set XREFS=0

if not exist "%HEADLESS%" (
    echo ERROR: %HEADLESS% not found
    echo Set GHIDRA_HOME or check LOCAL.md
    exit /b 1
)

echo [ghidra-export] project=%PROJECT_NAME% range=%START%-%END% out=%OUT%

call "%HEADLESS%" "%PROJECT_DIR%" "%PROJECT_NAME%" ^
    -process "%PROCESS_NAME%" ^
    -noanalysis ^
    -readOnly ^
    -scriptPath "%SCRIPT_DIR%" ^
    -postScript ExportRangeToGas.py %START% %END% "%OUT%" %XREFS%

endlocal
