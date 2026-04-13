# GDB 脚本：监听 DMA3 源地址寄存器写入（DMA3SAD = 0x040000D4）
# 用途：捕获从 ROM 发起的 DMA3 传输，记录源地址（ROM 压缩数据位置）
#
# 结论（2026-04-13）：卡牌大图加载不走 DMA3，此脚本无法捕获卡图来源
# DMA3 触发来自 VBlank 背景填充，与卡牌图像无关
#
# 使用方法：
#   tools/arm-none-eabi-gdb.exe --batch -x gdb_watch_dma3sad.gdb
#   连接后在 mGBA 中按 A 打开卡牌详情页

set architecture armv4t
set pagination off
set print pretty off

target remote localhost:2345

echo \n[GDB] Connected\n
info registers pc

# DMA3SAD = 0x040000D4，写入时触发 watchpoint
# 过滤掉背景 VBlank DMA（来自 0x080f4ff0）
watch *(unsigned int*)0x040000D4

echo \n[GDB] Watchpoint on DMA3SAD (0x040000D4)\n
echo [GDB] RUNNING - press A to open card detail page\n

define hook-stop
  echo \n--- DMA3SAD WRITE ---\n
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

echo \n[GDB] 10 DMA3 triggers captured. Done.\n
quit
