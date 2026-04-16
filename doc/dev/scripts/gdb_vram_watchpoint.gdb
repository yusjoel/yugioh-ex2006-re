set pagination off
set print pretty off

target remote localhost:2345

echo === VRAM Write Watchpoint Experiment ===\n
echo Target: 0x06008040 (card image VRAM start, from VRAM diff)\n

# Write watchpoint on the first byte of card image VRAM area
# mGBA stub only watches 1 byte, but that's enough to catch the writer
watch *(unsigned char*)0x06008040

echo === Watchpoint set. Continuing... ===\n
continue

echo \n=== Watchpoint triggered! ===\n
echo --- Registers ---\n
info registers
echo \n--- Disassembly around PC ---\n
x/16i $pc-8
echo \n--- Stack (possible return addresses) ---\n
x/8x $sp
echo \n--- VRAM around watched address ---\n
x/8x 0x06008040

echo \n=== Trying second hit (continue again) ===\n
continue

echo \n=== Second hit! ===\n
info registers
echo \n--- Disassembly around PC ---\n
x/16i $pc-8

echo \n=== Done ===\n
kill
quit
