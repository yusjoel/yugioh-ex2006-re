# 启动 mGBA（GDB stub 模式，不加载存档，从头冷启动）
# 端口: 2345
# 用途: 需要拦截游戏启动/初始化过程时使用，或 watchpoint 实验不能预加载存档时使用

. "$PSScriptRoot\local-settings.ps1"
$rom  = "$projectRoot\roms\2343.gba"

# UseShellExecute=$true 使进程独立于 PowerShell job object，session 退出后不被杀死
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $mgba
$psi.Arguments = "-g `"$rom`""
$psi.UseShellExecute = $true
$p = [System.Diagnostics.Process]::Start($psi)
Write-Host "mGBA started, PID: $($p.Id)"
