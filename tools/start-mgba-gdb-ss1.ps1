# 启动 mGBA（GDB stub 模式，加载 ss1 存档）
# 端口: 2345
# 用途: 带存档快照的 GDB 调试会话，适合在卡片列表页设置断点/watchpoint
#
# 注意：使用存档快照时卡图可能已预加载，watchpoint 可能不触发。
#       若需要捕获卡图加载过程，请改用 start-mgba-gdb-nosave.ps1。
#
# 启动前自动检查：
#   - 关闭已有 mGBA 实例
#   - 确认端口 2345 未被占用
# 启动后等待：
#   - 等待端口 2345 进入 LISTENING 状态
#   - 额外等待 8 秒，确保游戏 CPU 进入 RSP 循环（见 mgba-gdb-stub-pitfalls.md 坑2）

. "$PSScriptRoot\_preflight-mgba.ps1"   # 加载 local-settings.ps1 + 预检

$rom  = "$projectRoot\roms\2343.gba"
$save = "$projectRoot\roms\2343.ss1"

# UseShellExecute=$true 使进程独立于 PowerShell job object，session 退出后不被杀死
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName  = $mgba
$psi.Arguments = "-g -t `"$save`" `"$rom`""
$psi.UseShellExecute = $true
$p = [System.Diagnostics.Process]::Start($psi)
Write-Host "[start] mGBA 已启动（+ss1 存档），PID: $($p.Id)"

# 等待端口 2345 LISTENING
Write-Host "[start] 等待端口 2345..."
$timeout = 15; $elapsed = 0
while ($elapsed -lt $timeout) {
    Start-Sleep -Seconds 1; $elapsed++
    if (netstat -ano | Select-String ":2345\s.*LISTEN") {
        Write-Host "[start] 端口 2345 已就绪（${elapsed}s）"
        break
    }
    if (-not (Get-Process -Id $p.Id -ErrorAction SilentlyContinue)) {
        Write-Host "[start] 错误：mGBA 进程已退出！检查 ROM/存档路径或 mGBA 版本。"
        exit 1
    }
}
if (-not (netstat -ano | Select-String ":2345\s.*LISTEN")) {
    Write-Host "[start] 警告：超时后端口 2345 仍未就绪"
}

# 额外等待 CPU 热身
Write-Host "[start] 等待 8 秒，让游戏 CPU 进入 RSP 循环..."
Start-Sleep -Seconds 8
Write-Host "[start] 就绪！可运行 GDB：`n  tools\arm-none-eabi-gdb.exe --batch -x output\gdb_dma_watch.gdb"
