# GDB 脚本：监听 VRAM BG2 起始地址写入（0x06000000）
# 用途：捕获卡图解压后写入 BG2 tile 区的时机，记录写入来源（PC/LR/r0）
#
# 结论（2026-04-13）：mGBA GDB stub 不支持 VRAM 地址（0x06xxxxxx）的 watchpoint
# 脚本能成功设置 watchpoint，但按 A 打开详情页后从未触发
#
# 使用方法：
#   tools/arm-none-eabi-gdb.exe --batch -x gdb_watch_vram_bg2.gdb
#   连接后在 mGBA 中按 A 打开卡牌详情页

set architecture armv4t
set pagination off
set print pretty off

target remote localhost:2345

echo \n[GDB] Connected\n
info registers pc

# 监听 BG2 tile 数据区起始（卡图解压目标地址）
watch *(unsigned int*)0x06000000

echo \n[GDB] Watchpoint on VRAM BG2 0x06000000\n
echo [GDB] RUNNING - press A to open card detail page\n

define hook-stop
  echo \n--- VRAM BG2 WRITE ---\n
  info registers pc lr r0 r1 r2 r3
end

continue
continue
continue
continue
continue
continue
continue
continue
continue
continue

echo \n[GDB] 10 BG2 write triggers captured. Done.\n
quit
