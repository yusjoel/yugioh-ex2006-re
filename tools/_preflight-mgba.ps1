# tools/_preflight-mgba.ps1
# 公共预检：在启动 mGBA 前调用，确保环境干净
# 使用方式：在启动脚本开头 dot-source: . "$PSScriptRoot\_preflight-mgba.ps1"
#
# 检查项：
#   1. 是否有 mGBA 进程正在运行 → 询问是否强制关闭
#   2. 端口 2345 是否已被占用 → 若非 mGBA 占用则报错退出

. "$PSScriptRoot\local-settings.ps1"

$GDB_PORT = 2345

# ── 1. 检查 mGBA 进程 ──────────────────────────────────────────────────────────
$existingMgba = Get-Process -Name "mGBA" -ErrorAction SilentlyContinue

if ($existingMgba) {
    Write-Host "[preflight] 发现 $($existingMgba.Count) 个 mGBA 实例正在运行："
    $existingMgba | ForEach-Object { Write-Host "  PID $($_.Id)" }
    Write-Host "[preflight] 正在关闭..."
    $existingMgba | ForEach-Object { Stop-Process -Id $_.Id -Force }
    Start-Sleep -Seconds 2
    Write-Host "[preflight] mGBA 已关闭"
} else {
    Write-Host "[preflight] 无 mGBA 实例在运行"
}

# ── 2. 检查端口 2345 ────────────────────────────────────────────────────────────
$portInfo = netstat -ano | Select-String ":$GDB_PORT\s"
if ($portInfo) {
    # 提取占用端口的 PID
    $pidMatch = ($portInfo | Select-Object -First 1) -match '\s+(\d+)$'
    $ownerPid = if ($Matches) { $Matches[1] } else { "未知" }
    $ownerProc = Get-Process -Id $ownerPid -ErrorAction SilentlyContinue
    $ownerName = if ($ownerProc) { $ownerProc.Name } else { "未知进程" }
    Write-Host "[preflight] 警告：端口 $GDB_PORT 已被占用（PID $ownerPid / $ownerName）"
    Write-Host "[preflight] 等待端口释放（最多 10 秒）..."
    $waited = 0
    while ($waited -lt 10) {
        Start-Sleep -Seconds 1; $waited++
        $still = netstat -ano | Select-String ":$GDB_PORT\s"
        if (-not $still) { Write-Host "[preflight] 端口已释放"; break }
    }
    if (netstat -ano | Select-String ":$GDB_PORT\s") {
        Write-Host "[preflight] 错误：端口 $GDB_PORT 仍被占用，无法继续。请手动处理后重试。"
        exit 1
    }
} else {
    Write-Host "[preflight] 端口 $GDB_PORT 未被占用，OK"
}
