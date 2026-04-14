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

# 使用 cmd /c start 启动，彻底脱离当前 PowerShell Job Object
# UseShellExecute 不足以保证在工具调用环境下子进程不被杀死
# cmd start 会创建独立的新进程组，不受父 PS 会话 Job Object 约束
$args = "/c start `"`" `"$mgba`" -g `"$rom`""
$p = Start-Process -FilePath "cmd.exe" -ArgumentList $args -PassThru
Write-Host "[start] mGBA 已启动（通过 cmd /c start），启动器 PID: $($p.Id)"
Write-Host "[start] 脚本立即退出（保持 mGBA 独立存活）"
Write-Host "[start] 下一步（新命令）：& tools\mgba-scripts\wait-mgba-ready.ps1"
