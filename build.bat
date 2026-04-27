@echo off
if not exist output mkdir output

@rem 从 6 lang UTF-8 源生成 data/card-descriptions.s
python tools\card-desc\encode_txt_to_s.py
if errorlevel 1 goto :err

as.exe -mcpu=arm7tdmi -o output\rom.o asm\rom.s
if errorlevel 1 goto :err
ld.exe -T ld_script.txt -o output\2343.elf output\rom.o
if errorlevel 1 goto :err
objcopy.exe -O binary output\2343.elf output\2343.gba
if errorlevel 1 goto :err
goto :ok

:err
echo BUILD FAILED
exit /b 1
:ok
pause