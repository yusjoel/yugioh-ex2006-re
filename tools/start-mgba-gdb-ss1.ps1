# 启动 mGBA（GDB stub 模式，加载 ss1 存档）
# 端口: 2345
# 用途: 带存档快照的 GDB 调试会话，适合在卡片列表页设置断点/watchpoint

$mgba = "D:\Software\mGBA-build-latest-win64\mGBA.exe"
$rom  = "E:\Workspace\yugioh-ex2006-re\roms\2343.gba"
$save = "E:\Workspace\yugioh-ex2006-re\roms\2343.ss1"

# UseShellExecute=$true 使进程独立于 PowerShell job object，session 退出后不被杀死
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $mgba
$psi.Arguments = "-g -t `"$save`" `"$rom`""
$psi.UseShellExecute = $true
$p = [System.Diagnostics.Process]::Start($psi)
Write-Host "mGBA started, PID: $($p.Id)"
