set pagination off

target remote localhost:2345

# ===== T08: watch (写监视点) on VRAM BG tile data =====
echo \n=== T08: watch VRAM 0x06000000 ===\n
watch *(unsigned int*)0x06000000
continue
echo T08 TRIGGERED\n
info registers pc lr
delete

# ===== T09: rwatch (读监视点) on VRAM =====
echo \n=== T09: rwatch VRAM 0x06000000 ===\n
rwatch *(unsigned int*)0x06000000
continue
echo T09 TRIGGERED\n
info registers pc lr
delete

# ===== T10: rwatch on EWRAM =====
echo \n=== T10: rwatch EWRAM 0x02000000 ===\n
rwatch *(unsigned int*)0x02000000
continue
echo T10 TRIGGERED\n
info registers pc lr
delete

# ===== T11: watch (写) on EWRAM - set only =====
echo \n=== T11: watch EWRAM 0x02000000 (set only) ===\n
watch *(unsigned int*)0x02000000
echo T11 SET OK\n
delete

# ===== T12: rwatch on IWRAM data =====
echo \n=== T12: rwatch IWRAM 0x03000808 ===\n
rwatch *(unsigned int*)0x03000808
continue
echo T12 TRIGGERED\n
info registers pc lr
delete

# ===== T13: rwatch on ROM - set only =====
echo \n=== T13: rwatch ROM 0x08000000 (set only) ===\n
rwatch *(unsigned int*)0x08000000
echo T13 SET OK\n
delete

echo \n=== T08-T13 COMPLETE ===\n
quit
