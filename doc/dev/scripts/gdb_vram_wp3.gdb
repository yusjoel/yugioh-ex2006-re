set pagination off
set print pretty off

target remote localhost:2345

echo === VRAM Watchpoint + hbreak comparison ===\n

# watchpoint on decoder's first VRAM write target
watch *(unsigned char*)0x06004040

# hbreak as control: if decoder runs, this MUST fire
hbreak *0x0801d290

echo === 1 watchpoint + 1 hbreak set. Continuing... ===\n
continue

echo \n=== HIT ===\n
echo Breakpoint type tells us what fired:\n
info breakpoints
echo \nRegisters:\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6
echo \nDisassembly:\n
x/8i $pc-4

echo \nContinue to next hit...\n
continue

echo \n=== HIT 2 ===\n
info breakpoints
echo \nRegisters:\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6
echo \nDisassembly:\n
x/8i $pc-4

echo \n=== Done ===\n
kill
quit
