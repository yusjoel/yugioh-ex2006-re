@echo off
as.exe -mcpu=arm7tdmi -o rom.o asm\rom.s
ld.exe -T ld_script.txt -o 2343.elf rom.o
objcopy.exe -O binary 2343.elf 2343.gba
pause