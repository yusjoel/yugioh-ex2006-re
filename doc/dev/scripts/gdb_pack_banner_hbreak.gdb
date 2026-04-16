set pagination off
set print pretty off

target remote localhost:2345

echo === Pack banner hbreak script ===\n

# FUN_080d971c = pack list page initializer (found via approach C)
hbreak *0x080d971c
# FUN_080db860 = pack image loader (copies tile data to OBJ VRAM)
hbreak *0x080db860

echo === 2 hbreaks set. Continuing... ===\n
continue

echo \n=== HIT 1 ===\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6 r7
echo \nDisassembly:\n
x/10i $pc

echo \nContinue...\n
continue

echo \n=== HIT 2 ===\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6 r7
echo \nDisassembly:\n
x/10i $pc
echo \nCheck OBJ VRAM 0x06014000 before load:\n
x/4xw 0x06014000

echo \nContinue...\n
continue

echo \n=== HIT 3 ===\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6 r7
echo \nCheck OBJ VRAM 0x06014000:\n
x/4xw 0x06014000

echo \nContinue...\n
continue

echo \n=== HIT 4 ===\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6 r7
echo \nCheck OBJ VRAM 0x06014000:\n
x/4xw 0x06014000

echo \nContinue...\n
continue

echo \n=== HIT 5 ===\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6 r7
echo \nCheck OBJ VRAM 0x06014000:\n
x/4xw 0x06014000

echo \nContinue...\n
continue

echo \n=== HIT 6 ===\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6 r7
echo \nCheck OBJ VRAM 0x06014000:\n
x/4xw 0x06014000

echo \n=== Done (6 hits) ===\n
kill
quit
