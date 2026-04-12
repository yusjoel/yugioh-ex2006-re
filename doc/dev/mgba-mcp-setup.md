# mGBA MCP 动态调试环境搭建

本文记录为《游戏王 EX2006》反汇编项目配置 mGBA MCP 动态调试环境的过程。

---

## 一、背景

静态反汇编分析遇到瓶颈时，需要借助模拟器进行动态分析，验证内存布局、寄存器状态、
函数调用流程等。通过 [mgba-live-mcp](https://github.com/penandlim/mgba-live-mcp)，
可以将 mGBA 模拟器接入 MCP（Model Context Protocol），使 AI 工具能够直接控制模拟器
进行动态分析。

---

## 二、工具说明

### mGBA

- **版本**：0.10.5 (win64)
- **安装路径**：`D:\Software\mGBA-0.10.5-win64\mGBA.exe`
- **Lua 脚本支持**：官方预编译包已内置，可在 `scripts/` 目录下找到示例 `.lua` 文件

### mgba-live-mcp

- **项目地址**：https://github.com/penandlim/mgba-live-mcp
- **运行方式**：通过 `uvx` 启动，以 stdio 模式运行的 MCP 服务器
- **依赖**：[uv](https://docs.astral.sh/uv/)（Python 包管理器）

### 提供的 MCP 工具（共 15 个）

| 类别 | 工具名 | 说明 |
|------|--------|------|
| 会话管理 | `mgba_live_start` | 启动 mGBA 并加载 ROM |
| | `mgba_live_start_with_lua` | 启动并立即执行 Lua 脚本 |
| | `mgba_live_attach` | 连接已有会话 |
| | `mgba_live_status` | 查看会话状态（含截图） |
| | `mgba_live_stop` | 停止会话 |
| 输入控制 | `mgba_live_input_tap` | 模拟按键（A/B/START 等） |
| | `mgba_live_input_set` | 持续按住按键 |
| | `mgba_live_input_clear` | 释放按键 |
| 内存读取 | `mgba_live_read_memory` | 读取指定地址列表 |
| | `mgba_live_read_range` | 读取连续内存区间 |
| | `mgba_live_dump_pointers` | 转储指针表 |
| | `mgba_live_dump_oam` | 转储 OAM 精灵表 |
| | `mgba_live_dump_entities` | 转储实体结构 |
| Lua 脚本 | `mgba_live_run_lua` | 在运行中的会话执行 Lua |
| 截图 | `mgba_live_export_screenshot` | 导出截图到文件 |

---

## 三、安装步骤

### 前提条件

- 已安装 mGBA 0.10.5（含 Lua 脚本支持）
- 已安装 `uv`（验证：`uv --version`）

### 安装 mgba-live-mcp

mgba-live-mcp 通过 `uvx` 按需运行，无需手动 `install`，直接在 MCP 配置中引用即可。

```bash
# 可选：验证包可访问（会挂起等待 stdio 输入，Ctrl+C 退出即为正常）
uvx mgba-live-mcp
```

### 配置 MCP 服务器

GitHub Copilot CLI 从 `~/.copilot/mcp-config.json` 读取 MCP 服务器配置。
创建该文件（若已存在则合并 `mcpServers` 字段）：

**`C:\Users\<用户名>\.copilot\mcp-config.json`**

```json
{
  "mcpServers": {
    "mgba": {
      "command": "uvx",
      "args": ["mgba-live-mcp"]
    }
  }
}
```

配置完成后**重启 Copilot CLI** 使其生效。

---

## 四、使用方法

### 启动 ROM

由于 mGBA 不在系统 PATH 中，首次启动需手动指定路径：

```json
{
  "rom": "E:\\Workspace\\yugioh-ex2006-re\\roms\\2343.gba",
  "mgba_path": "D:\\Software\\mGBA-0.10.5-win64\\mGBA.exe"
}
```

> 会话 ID 由服务器自动生成（如 `20260412-120000`），后续操作通过 `session` 字段引用。

### 读取内存

```json
{
  "session": "<session_id>",
  "start": 134217728,
  "length": 256
}
```

> GBA ROM 基址为 `0x08000000`（十进制 `134217728`）。
> IWRAM 基址为 `0x03000000`，EWRAM 基址为 `0x02000000`。

### 执行 Lua 脚本

```lua
-- 示例：读取当前帧号
return emu:currentFrame()
```

```lua
-- 示例：读取指定地址的 32 位值
return emu:read32(0x03001234)
```

### 快速运行（加速模式）

```json
{
  "rom": "E:\\Workspace\\yugioh-ex2006-re\\roms\\2343.gba",
  "mgba_path": "D:\\Software\\mGBA-0.10.5-win64\\mGBA.exe",
  "fast": true
}
```

`fast: true` 等同于 `fps_target: 600`，适合快速跳过片头等场景。

---

## 五、运行时说明

- 会话文件存储于 `~/.mgba-live-mcp/runtime/`
- 崩溃的会话自动归档到 `~/.mgba-live-mcp/runtime/archived_sessions/`
- 大多数工具调用会自动返回截图（内嵌于响应中）
- 需要持久化截图时使用 `mgba_live_export_screenshot` 并指定 `out` 路径
