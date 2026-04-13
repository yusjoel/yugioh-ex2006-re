# 启动 mGBA（GDB stub 模式，不加载存档，从头冷启动）
# 端口: 2345
# 用途: 需要拦截游戏启动/初始化过程时使用，或 watchpoint 实验不能预加载存档时使用
#
# 启动前自动检查：
#   - 关闭已有 mGBA 实例
#   - 确认端口 2345 未被占用
# 启动后等待：
#   - 等待端口 2345 进入 LISTENING 状态
#   - 额外等待 8 秒，确保游戏 CPU 进入 RSP 循环（见 mgba-gdb-stub-pitfalls.md 坑2）

. "$PSScriptRoot\_preflight-mgba.ps1"   # 加载 local-settings.ps1 + 预检

$rom = "$projectRoot\roms\2343.gba"

# UseShellExecute=$true 使进程独立于 PowerShell job object，session 退出后不被杀死
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName  = $mgba
$psi.Arguments = "-g `"$rom`""
$psi.UseShellExecute = $true
$p = [System.Diagnostics.Process]::Start($psi)
Write-Host "[start] mGBA 已启动，PID: $($p.Id)"

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
        Write-Host "[start] 错误：mGBA 进程已退出！检查 ROM 路径或 mGBA 版本。"
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
