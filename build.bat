@echo off
if not exist output mkdir output
as.exe -mcpu=arm7tdmi -o output\rom.o asm\rom.s
ld.exe -T ld_script.txt -o output\2343.elf output\rom.o
objcopy.exe -O binary output\2343.elf output\2343.gba
pause