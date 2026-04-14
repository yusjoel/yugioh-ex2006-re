# PowerShell Job Object 导致 mGBA 被意外杀死

## 问题现象

在工具环境（GitHub Copilot CLI 等）中通过 PowerShell 启动 mGBA 后，
mGBA 进程在脚本执行完毕后随即退出，无论使用以下哪种方式：

```powershell
# 方式 A：Start-Process（默认）
Start-Process -FilePath $mgba -ArgumentList "..."

# 方式 B：ProcessStartInfo + UseShellExecute=$true
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.UseShellExecute = $true
[System.Diagnostics.Process]::Start($psi)
```

---

## 根本原因：Windows Job Object

### 什么是 Job Object

Windows Job Object 是一种内核对象，用于将一组进程绑定在一起统一管理。
Job Object 最常见的用途之一是设置 **"在 Job Object 关闭时杀死所有关联进程"**（`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`）。

### 为什么 PowerShell 脚本受影响

GitHub Copilot CLI 等工具环境在执行 PowerShell 脚本时，
会将 PowerShell 进程本身加入一个 Job Object（用于超时控制、资源隔离等）。

```
[工具环境（Job Object 所有者）]
    └── pwsh.exe（PowerShell 会话）     ← 被加入 Job Object
            └── mGBA.exe               ← 默认继承父进程的 Job Object 关联
```

当 PowerShell 脚本执行完毕退出后，如果 Job Object 的引用计数归零，
系统会杀死该 Job Object 内所有进程——包括 mGBA。

### 为什么 `UseShellExecute=$true` 不够

`UseShellExecute=$true` 的设计目的是通过 Shell（Explorer）启动进程，
使其不继承父进程的句柄。这在普通情况下足以使子进程独立存活。

但当父进程本身已经被加入一个设置了 `KILL_ON_JOB_CLOSE` 的 Job Object 时，
子进程在 Windows Vista+ 默认会**继承同一个 Job Object**（除非父 Job Object 允许嵌套）。
即便 Shell 启动也无法绕过这一继承，因为继承发生在内核层面。

```
Job Object (KILL_ON_JOB_CLOSE=true)
    ├── pwsh.exe
    └── mGBA.exe   ← UseShellExecute=$true 仍在同一 Job Object 内
```

---

## 解决方案：`cmd /c start`

Windows `cmd.exe` 的 `start` 命令有一个特殊行为：
它通过 `CreateProcess` 创建进程时会传入 `CREATE_BREAKAWAY_FROM_JOB` 标志（或等效机制），
使新进程**脱离当前 Job Object**，成为独立进程。

```powershell
# 解法：通过 cmd /c start 启动 mGBA
$args = "/c start `"`" `"$mgba`" -g `"$rom`""
Start-Process -FilePath "cmd.exe" -ArgumentList $args -PassThru
```

启动后的进程关系：

```
[工具环境 Job Object]
    └── pwsh.exe
            └── cmd.exe（cmd /c start，立即退出）
                    └── mGBA.exe   ← 已脱离 Job Object，独立存活 ✅
```

`cmd.exe` 在 `start` 之后立即退出，mGBA 成为独立进程，
不再受任何 Job Object 约束，PowerShell 会话退出后不受影响。

---

## 验证方法

```powershell
# 启动后，在新的 PowerShell 命令中确认 mGBA 进程存活
Get-Process -Name "mGBA" -ErrorAction SilentlyContinue | Select-Object Id, Name

# 确认端口 2345 正在监听
(netstat -ano) | Where-Object { $_ -match "2345" }
```

---

## 相关规则

> **规则：在工具环境的 PowerShell 中启动需要长时间存活的 GUI 进程（如 mGBA），
> 必须通过 `cmd /c start` 启动，而不是直接 `Start-Process` 或 `ProcessStartInfo`。**

此规则适用于所有需要在 PowerShell 脚本退出后仍然存活的子进程。

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `tools/mgba-scripts/start-mgba-gdb-nosave.ps1` | 使用 `cmd /c start` 启动 mGBA（无存档） |
| `tools/mgba-scripts/start-mgba-gdb-ss1.ps1` | 使用 `cmd /c start` 启动 mGBA（带存档） |
| `tools/mgba-scripts/wait-mgba-ready.ps1` | 独立等待端口 2345 就绪（必须在新命令中执行） |
| `doc/dev/mgba-gdb-stub-pitfalls.md` | 坑 4：启动与等待必须分两步 |
