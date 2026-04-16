set pagination off
set print pretty off

target remote localhost:2345

echo === Pack banner OBJ tile watchpoint ===\n
echo Target: 0x06014000 (OBJ VRAM tile 512, first pack banner)\n

watch *(unsigned int*)0x06014000

echo === Watchpoint set. Continuing... ===\n
continue

echo \n=== HIT 1 ===\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6 r7
echo \nMemory at 0x06014000:\n
x/8xw 0x06014000
echo \nDisassembly around PC:\n
x/10i $pc-8
echo \nStack (LR chain):\n
x/8xw $sp

echo \nContinue to next hit...\n
continue

echo \n=== HIT 2 ===\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6 r7
echo \nMemory at 0x06014000:\n
x/8xw 0x06014000
echo \nDisassembly around PC:\n
x/10i $pc-8

echo \nContinue to next hit...\n
continue

echo \n=== HIT 3 ===\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6 r7
echo \nMemory at 0x06014000:\n
x/8xw 0x06014000
echo \nDisassembly around PC:\n
x/10i $pc-8

echo \nContinue to next hit...\n
continue

echo \n=== HIT 4 ===\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6 r7
echo \nMemory at 0x06014000:\n
x/8xw 0x06014000
echo \nDisassembly around PC:\n
x/10i $pc-8

echo \nContinue to next hit...\n
continue

echo \n=== HIT 5 ===\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6 r7
echo \nMemory at 0x06014000:\n
x/8xw 0x06014000
echo \nDisassembly around PC:\n
x/10i $pc-8

echo \n=== Done (5 hits captured) ===\n
kill
quit
