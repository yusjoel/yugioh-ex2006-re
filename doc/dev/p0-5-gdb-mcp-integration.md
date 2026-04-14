# P0-5: GDB MCP 集成验证报告

## 概述

本阶段目标：验证通过 GDB MCP（Model Context Protocol）工具直接调用 GDB 进行调试，
替代手写 `.gdb` 脚本，为后续 P1 卡图定位任务提供更便捷的交互式调试能力。

**最终结论**：核心功能全部验证通过，修复了 GDB MCP 中三个解析器 bug。

---

## 环境

| 组件 | 路径/版本 |
|------|----------|
| GDB | `tools/arm-none-eabi-gdb.exe` (GDB 10.2) |
| GDB MCP 源码 | `D:\Software\gdb-mcp\src\` |
| GDB MCP dist | `D:\Software\gdb-mcp\dist\` |
| mGBA | 通过 `tools/start-mgba-gdb-ss1.ps1` 启动，GDB stub 端口 2345 |
| MCP 配置 | `C:\Users\yushj\.copilot\mcp-config.json` |

---

## 发现与修复的 Bug

### Bug 1: token 前缀导致连接超时（主要 Bug）

**现象**：`gdb_connect` 超时，30 秒后报错。

**原因**：GDB MI 协议中，发送带 token 的命令（如 `20-target-select remote ...`），
GDB 响应为 `20^connected`（token 前缀格式）。`parseMiLine()` 只识别以 `^` 开头的行，
`20^connected` 被当作普通 console 输出忽略，命令永远得不到响应。

**修复**：`D:\Software\gdb-mcp\src\gdb\mi-parser.ts` 的 `parseMiLine()`：
```typescript
// 修复前：只检查 line.startsWith("^")
// 修复后：查找 ^ 位置，支持 N^result-class 格式
const caretIdx = line.indexOf("^");
if (caretIdx > 0 && /^\d+$/.test(line.slice(0, caretIdx))) {
  const token = parseInt(line.slice(0, caretIdx), 10);
  const response = parseResultRecord(line.slice(caretIdx));
  response.token = token;
  return response;
}
```

---

### Bug 2: `split(",", 2)` 截断值（导致 bkpt 解析为空对象）

**现象**：`gdb_set_breakpoint` 返回"断点已设置: undefined"，`bkpt` 为空对象 `{}`。

**原因**：JavaScript 的 `"done,bkpt={n=1,type=bp}".split(",", 2)` 返回
`["done", "bkpt={n"]`（limit 参数在找到第一个 `,` 后继续找直到达到 limit），
导致 `parseMiTuple` 只收到截断的字符串。

同一问题存在于：
- `parseResultRecord`：`rest.split(",", 2)` 截断了 result 参数
- `parseAsyncRecord`：同上

**修复**：改用 `indexOf(",")` 只在第一个逗号处分割：
```typescript
// 修复前
const parts = rest.split(",", 2);
const resultClass = parts[0];
result = parseMiTuple(parts[1]);

// 修复后
const commaIdx = rest.indexOf(",");
const resultClass = commaIdx >= 0 ? rest.slice(0, commaIdx) : rest;
if (commaIdx >= 0) result = parseMiTuple(rest.slice(commaIdx + 1));
```

同理在 `parseMiTuple` 的 pair 分割也存在 `pair.split("=", 2)` 的问题，也一并修复为
`indexOf("=")` 方式。

---

### Bug 3: `parseMiOutput` 按 `\n` 切行导致 bkpt 解析失败

**现象**：即使修复了 Bug 2，`gdb_list_breakpoints` 仍解析不到断点字段。

**原因**：GDB 在 `-break-list` 响应中，`thread-groups=["i1\n"]` 包含**字面换行符**。
`parseMiOutput` 直接按 `\n` 切行，把一条完整的 MI 记录切成两段。

**修复**：`parseMiOutput` 改为跟踪括号深度和字符串状态，只在 depth=0 且不在字符串内时才切行：
```typescript
for (let i = 0; i < buffer.length; i++) {
  if (char === '"' && prevChar !== "\\") inString = !inString;
  if (!inString) {
    if ("{[(".includes(char)) depth++;
    else if ("}])".includes(char)) depth--;
    else if (char === "\n" && depth === 0) {
      // 提取完整行，调用 parseMiLine
    }
  }
}
```

---

### Bug 4: `parseBreakpointList` 路径错误（gdb_list_breakpoints 显示空）

**现象**：`gdb_list_breakpoints` 总是显示"当前没有设置断点"。

**原因**：`parseBreakpointList` 读取 `result?.breakpoints`，但 `-break-list` 实际返回结构为：
```
{BreakpointTable: {nr_rows: ..., body: [bkpt={...}]}}
```

另外 `body` 中的元素是 `bkpt={...}` 格式（key=value），`parseMiList` 未处理此格式。

**修复**：
1. `mi-commands.ts`：`parseBreakpointList` 改为读取 `result?.BreakpointTable?.body`
2. `mi-parser.ts`：`parseMiList` 增加对 `key=value` 格式 item 的处理（取 value 部分）

---

## 验证结果

| 工具 | 状态 | 备注 |
|------|------|------|
| `gdb_init` | ✅ | 使用 `tools/arm-none-eabi-gdb.exe`（GDB 10.2），**不能用** `architecture:"arm"` 参数（会选 GDB 14.1，与 mGBA 不兼容） |
| `gdb_connect` | ✅ | `localhost:2345` |
| `gdb_disconnect` | ✅ | |
| `gdb_set_breakpoint` | ✅ | 返回断点编号和地址 |
| `gdb_list_breakpoints` | ✅ | 正确显示断点地址、状态 |
| `gdb_delete_breakpoint` | ✅ | |
| `gdb_continue` | ✅ | |
| `gdb_interrupt` | ✅ | |
| `gdb_evaluate_expression` | ✅ | 读取 `*(unsigned int*)0x040000D4` 成功 |
| `gdb_list_locals` | ✅ | 无符号表时返回空（正常） |
| `gdb_list_frames` | ⚠️ | mGBA THUMB 调试不支持栈回溯（"Reply contains invalid hex digit 83"），已知限制 |
| `gdb_read_memory` | ⚠️ | `memory.contents.join is not a function`，parser 处理返回格式有误，待修复 |
| `gdb_read_registers` | ⚠️ | 高层 API 将寄存器名转换为编号有问题；可用 `gdb_command("-data-list-register-values x 0 1 15")` 代替 |

---

## 关键经验

### mGBA GDB Stub 限制
- **一次性连接**：GDB 断开后 stub 永久关闭，每次需重启 mGBA
- `monitor help` 返回 "Target does not support this command"，不支持 monitor 扩展命令
- ROM 区域被标记为 rw（实际只读），不影响使用
- THUMB 代码栈回溯不支持（`-stack-list-frames` 失败）

### GDB 版本选择
- `tools/arm-none-eabi-gdb.exe` = GDB 10.2 ✅ 兼容 mGBA
- `D:\devkitPro\devkitARM\bin\arm-none-eabi-gdb.exe` = GDB 14.1 ❌ 与 mGBA 不兼容
- **调用 `gdb_init` 时必须指定完整路径，不能使用 `architecture` 参数**

### MCP 进程生命周期
- GDB MCP dist 修改后，**必须重启 Claude CLI** 才会加载新代码
- 重启顺序：修改源码 → `npm run build` → 重启 CLI → 重启 mGBA → 验证

### Windows GDB CRLF 问题
- GDB on Windows 输出 `\r\n` 换行
- `parseMiOutput` 的 `.trim()` 会消除 `\r`，基本没问题
- 但 `thread-groups=["i1\r\n"]` 中内嵌的 `\r\n` 会造成解析问题（与 Bug 3 相关）

---

## 后续

P0-5 核心功能验证完成，P0 全部子任务收尾。

**下一步：P1 — 卡图 ROM 定位**（利用 MCP 工具链进行交互式调试）
