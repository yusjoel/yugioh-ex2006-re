# mGBA GDB Stub 调试经验

记录通过 GDB 连接 mGBA GDB stub 过程中踩过的坑，供后续调试参考。

---

## 工具选择

**必须使用 `tools/arm-none-eabi-gdb.exe`（GDB 10.2）**，不能用 devkitARM 自带的 GDB 14.1。

GDB 14.1 与 mGBA stub 之间存在 7 处 RSP 协议不兼容（详见 `doc/gdb-mgba-watchpoint.md`），握手阶段就会失败。GDB 10.2 可直接连接，无需代理。

---

## 正确的启动流程

**必须分步操作**，不能把启动、等待、GDB 连接全写在同一个 PowerShell 命令块里：

```
1. 手动启动 mGBA（单独执行一条命令）
2. 等待 netstat 显示 :2345 LISTENING
3. 再额外等待 5-8 秒（游戏 CPU 需要时间进入 RSP 循环）
4. 运行 GDB
```

---

## 已知坑

### 坑 1：`-g` 不接受端口号

```powershell
# ❌ 错误：2345 被当作 ROM 路径，mGBA 立即退出
Start-Process mGBA.exe -ArgumentList @("-g", "2345", "rom.gba")

# ✅ 正确：端口固定 2345，-g 只是开关
Start-Process mGBA.exe -ArgumentList @("-g", "rom.gba")
```

### 坑 2：端口就绪 ≠ 游戏 CPU 就绪

端口 2345 出现在 netstat 后，mGBA 仍需几秒才进入 RSP 命令循环。过早连接 GDB 会得到 `Connection timed out`。

**解决**：端口出现后再等 5-8 秒，或观察游戏画面已正常显示后再连接。

### 坑 3：GDB stub 一次性消耗

GDB 连接后断开（包括 `quit`、`--batch` 脚本结束），stub **永久关闭**，端口停止监听。后续连接一律被拒绝。

**解决**：每次调试前必须完整重启 mGBA。

### 坑 4：Start-Process + Sleep + GDB 不能混写在同一命令块

在同一 PowerShell 命令块里 `Start-Process mGBA` 然后 `Sleep` 再连接 GDB，脚本块结束时可能影响 mGBA 进程的存活（Windows job object）。

**解决**：启动 mGBA 用一条独立命令，等待和 GDB 连接用另一条命令。

### 坑 5：GDB 脚本 `echo` 中文会乱码

GDB 的 `echo` 命令处理中文字符时显示乱码。

**解决**：GDB 脚本（`.gdb` 文件）里的 `echo` 和注释全部使用英文/ASCII。

### 坑 6：Ghidra 将 GBA SWI 输出为 `svc`，不要搜 `swi`

ARM 架构 v7 起将 SWI 指令重命名为 SVC（SuperVisor Call），编码完全相同。Ghidra 统一使用新助记符，因此在 `asm/all.s` 中：

```
# ❌ 找不到任何结果
grep "swi" all.s

# ✅ 正确
grep "svc 0x11" all.s   # LZ77UnCompVram
grep "svc 0x12" all.s   # LZ77UnCompWram
grep "svc 0x13" all.s   # HuffUnCompReadNormal
```

### 坑 7：加载存档快照的参数格式

ROM 文件和存档快照需分开传，ROM 路径放最后：

```powershell
Start-Process mGBA.exe -ArgumentList @("-g", "-t", "2343.ss1", "2343.gba")
```

---

## GDB 脚本模板

```gdb
set architecture armv4t
set pagination off
set print pretty off

target remote localhost:2345

info registers pc sp

# 示例：监听 DMA3 源地址寄存器（捕获从 ROM 搬运数据的时机）
watch *(unsigned int*)0x040000D8

continue
```

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `doc/gdb-mgba-watchpoint.md` | RSP 协议不兼容问题完整分析 |
| `tools/arm-none-eabi-gdb.exe` | GDB 10.2（可直连 mGBA stub） |
| `output/gdb_watch_dma.gdb` | DMA3 watchpoint 脚本 |
