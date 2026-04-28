@echo off
@rem 纯汇编流程: data/*.s → output/2343.gba
@rem 前置: data/*.s 必须已就绪 (跑 export_all.py 或 build-all.bat 准备)
if not exist output mkdir output

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
if not defined NOPAUSE pause
