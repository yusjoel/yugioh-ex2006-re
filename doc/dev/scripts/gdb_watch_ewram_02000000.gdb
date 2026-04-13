# GDB 脚本：监听 EWRAM 起始地址写入（0x02000000）
# 用途：若卡图解压先缓存到 EWRAM 再 DMA 到 VRAM，可捕获到中间步骤
#
# 结论（2026-04-13）：mGBA GDB stub 不支持 EWRAM 地址（0x02xxxxxx）的 watchpoint
# 脚本能成功设置 watchpoint，但按 A 打开详情页后从未触发
# （注意：旧版本脚本在游戏启动时曾触发一次，lr=0x080f4db0，属于初始化写入，与卡图无关）
#
# 使用方法：
#   tools/arm-none-eabi-gdb.exe --batch -x gdb_watch_ewram.gdb
#   连接后在 mGBA 中按 A 打开卡牌详情页

set architecture armv4t
set pagination off
set print pretty off

target remote localhost:2345

echo \n[GDB] Connected\n
info registers pc

# 监听 EWRAM 起始区域
watch *(unsigned int*)0x02000000

echo \n[GDB] Watchpoint on EWRAM 0x02000000\n
echo [GDB] RUNNING - press A to open card detail page\n

define hook-stop
  echo \n--- EWRAM WRITE ---\n
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

echo \n[GDB] 10 triggers captured. Done.\n
quit
