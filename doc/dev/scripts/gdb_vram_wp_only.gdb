set pagination off
set print pretty off

target remote localhost:2345

echo === Watchpoint ONLY - no hbreak ===\n
watch *(unsigned char*)0x06004040

echo === Continuing... ===\n
continue

echo \n=== HIT 1 ===\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6
x/4i $pc-2
echo \n--- continue ---\n
continue

echo \n=== HIT 2 ===\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6
x/4i $pc-2
echo \n--- continue ---\n
continue

echo \n=== HIT 3 ===\n
info registers pc lr r0 r1 r2 r3 r4 r5 r6
x/4i $pc-2

echo \n=== Done ===\n
kill
quit
