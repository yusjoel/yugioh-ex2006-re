# tools/wait-mgba-ready.ps1
# 等待 mGBA GDB stub 完全就绪（端口 2345 LISTENING + 游戏 CPU 热身）
#
# 使用方式：
#   第一步：& tools\start-mgba-gdb-nosave.ps1   （或 ss1 版本）
#   第二步：& tools\wait-mgba-ready.ps1          （本脚本）
#   第三步：& tools\arm-none-eabi-gdb.exe --batch -x doc\dev\scripts\gdb_dma_watch.gdb
#
# 等待逻辑（见 mgba-gdb-stub-pitfalls.md 坑2）：
#   1. 轮询 netstat 直到端口 2345 LISTENING
#   2. 额外等待 8 秒（游戏 CPU 需要时间进入 RSP 循环，光有端口不够）

$GDB_PORT   = 2345
$PORT_TIMEOUT = 20   # 等待端口最多 20 秒
$CPU_WARMUP   = 8    # 端口就绪后再等 8 秒

Write-Host "[wait] 等待端口 $GDB_PORT LISTENING（最多 ${PORT_TIMEOUT}s）..."
$elapsed = 0
$ready = $false
while ($elapsed -lt $PORT_TIMEOUT) {
    Start-Sleep -Seconds 1; $elapsed++
    if (netstat -ano | Select-String ":$GDB_PORT\s.*LISTEN") {
        Write-Host "[wait] 端口 $GDB_PORT 已就绪（${elapsed}s）"
        $ready = $true
        break
    }
}

if (-not $ready) {
    Write-Host "[wait] 错误：超过 ${PORT_TIMEOUT}s 后端口 $GDB_PORT 仍未就绪。"
    Write-Host "[wait] 请检查 mGBA 是否正在运行：Get-Process -Name mGBA"
    exit 1
}

Write-Host "[wait] 等待 ${CPU_WARMUP}s，让游戏 CPU 进入 RSP 循环..."
Start-Sleep -Seconds $CPU_WARMUP

Write-Host "[wait] 就绪！现在可以连接 GDB："
Write-Host "  tools\arm-none-eabi-gdb.exe --batch -x doc\dev\scripts\gdb_dma_watch.gdb"
