# 关闭所有 mGBA 实例（不包括 mgba-live-mcp）

$procs = Get-Process | Where-Object { $_.Name -eq "mGBA" }

if ($procs) {
    $procs | ForEach-Object {
        Write-Host "关闭 mGBA PID $($_.Id)"
        Stop-Process -Id $_.Id -Force
    }
    Write-Host "完成"
} else {
    Write-Host "没有运行中的 mGBA 实例"
}
