set pagination off
set print pretty off

target remote localhost:2345

echo === VRAM Write Watchpoint v2 ===\n
echo Target: 0x06004040 (charblock 1, tile 1 - decoder literal pool points to 0x06004000)\n

watch *(unsigned char*)0x06004040

echo === Watchpoint set. Continuing... ===\n
continue

echo \n=== HIT 1 ===\n
echo PC:\n
info registers pc lr
echo \nAll registers:\n
info registers
echo \nDisassembly:\n
x/16i $pc-10
echo \nContinue to hit 2...\n
continue

echo \n=== HIT 2 ===\n
info registers pc lr
echo \nAll registers:\n
info registers
echo \nDisassembly:\n
x/16i $pc-10
echo \nContinue to hit 3...\n
continue

echo \n=== HIT 3 ===\n
info registers pc lr
echo \nAll registers:\n
info registers
echo \nDisassembly:\n
x/16i $pc-10

echo \n=== Done ===\n
kill
quit
