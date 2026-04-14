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

# 使用 cmd /c start 启动，彻底脱离当前 PowerShell Job Object
$args = "/c start `"`" `"$mgba`" -g -t `"$save`" `"$rom`""
$p = Start-Process -FilePath "cmd.exe" -ArgumentList $args -PassThru
Write-Host "[start] mGBA 已启动（+ss1 存档，通过 cmd /c start），启动器 PID: $($p.Id)"
Write-Host "[start] 脚本立即退出（保持 mGBA 独立存活）"
Write-Host "[start] 下一步（新命令）：& tools\mgba-scripts\wait-mgba-ready.ps1"
