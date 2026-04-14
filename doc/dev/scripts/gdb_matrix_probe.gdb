set pagination off

target remote localhost:2345

# ===== T01: break (软件断点) on ROM =====
# 软件断点需要写入 BKPT 指令，ROM 只读，预期失败
echo \n=== T01: break ROM 0x080F4EB6 ===\n
break *0x080F4EB6
continue
echo T01 TRIGGERED\n
info registers pc lr
delete

# ===== T02: hbreak (硬件断点) on ROM =====
echo \n=== T02: hbreak ROM 0x080F4EB6 ===\n
hbreak *0x080F4EB6
continue
echo T02 TRIGGERED\n
info registers pc lr
delete

# ===== T03: break (软件断点) on IWRAM code =====
# IWRAM 可写，软件断点应可用
echo \n=== T03: break IWRAM 0x03004DB4 ===\n
break *0x03004DB4
continue
echo T03 TRIGGERED\n
info registers pc lr
delete

# ===== T04: hbreak (硬件断点) on IWRAM code =====
echo \n=== T04: hbreak IWRAM 0x03004DB4 ===\n
hbreak *0x03004DB4
continue
echo T04 TRIGGERED\n
info registers pc lr
delete

# ===== T05: watch (写监视点) on IO DMA3SAD =====
# P0-1 已确认可触发，最快触发
echo \n=== T05: watch IO 0x040000D0 (DMA3SAD) ===\n
watch *(unsigned int*)0x040000D0
continue
echo T05 TRIGGERED\n
info registers pc lr
delete

# ===== T06: rwatch (读监视点) on IO DMA3SAD =====
echo \n=== T06: rwatch IO 0x040000D0 (DMA3SAD) ===\n
rwatch *(unsigned int*)0x040000D0
continue
echo T06 TRIGGERED\n
info registers pc lr
delete

# ===== T07: awatch (读写监视点) on IO DMA3SAD =====
echo \n=== T07: awatch IO 0x040000D0 (DMA3SAD) ===\n
awatch *(unsigned int*)0x040000D0
continue
echo T07 TRIGGERED\n
info registers pc lr
delete

# ===== T08: watch (写监视点) on VRAM BG tile data =====
# 使用 0x06000000 (BG Tile Data，每帧渲染都写入)
# 0x06000040 仅在卡图加载时写入，deck editor 中不会触发
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

# ===== T10: rwatch on EWRAM (存档头 YWCT2006) =====
echo \n=== T10: rwatch EWRAM 0x02000000 ===\n
rwatch *(unsigned int*)0x02000000
continue
echo T10 TRIGGERED\n
info registers pc lr
delete

# ===== T11: watch (写) on EWRAM =====
# 仅在游戏存档时写入，可能不触发；验证能否设置
echo \n=== T11: watch EWRAM 0x02000000 (set only) ===\n
watch *(unsigned int*)0x02000000
echo T11 SET OK (no continue - save-only write)\n
delete

# ===== T12: rwatch on IWRAM data (函数指针表) =====
echo \n=== T12: rwatch IWRAM 0x03000808 ===\n
rwatch *(unsigned int*)0x03000808
continue
echo T12 TRIGGERED\n
info registers pc lr
delete

# ===== T13: rwatch on ROM (仅验证设置，不 continue) =====
# ROM 被频繁读取，continue 会立即触发形成"packet error 风暴"，跳过 continue
echo \n=== T13: rwatch ROM 0x08000000 (set only, skip continue) ===\n
rwatch *(unsigned int*)0x08000000
echo T13 SET OK (skipping continue - every insn fetch triggers)\n
delete

echo \n=== ALL TESTS COMPLETE ===\n
quit
