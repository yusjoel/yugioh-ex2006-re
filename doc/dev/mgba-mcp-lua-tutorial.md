# mGBA MCP 动态调试教学

本文档说明如何使用 mgba-live-mcp 工具与 mGBA 模拟器交互，对 GBA ROM 进行动态分析。

---

## 一、工具概述

[mgba-live-mcp](https://github.com/penandlim/mgba-live-mcp) 是一套将 mGBA 暴露为 MCP（Model Context Protocol）服务的工具，允许 AI Agent 通过工具调用直接控制 mGBA 实例：

- 启动/停止模拟器
- 截图
- 模拟按键
- 执行 Lua 脚本（读写内存、注册回调）
- 读取内存范围

---

## 二、主要 MCP 工具

| 工具 | 说明 |
|------|------|
| `mgba_live_start` | 启动 mGBA 并加载 ROM |
| `mgba_live_stop` | 停止当前 mGBA 实例 |
| `mgba_live_status` | 查询当前 session 状态（帧号、pid）|
| `mgba_live_export_screenshot` | 截取当前画面 |
| `mgba_live_input_tap` | 按下并释放一个按键（A/B/UP/DOWN/LEFT/RIGHT/L/R/START/SELECT） |
| `mgba_live_input_set` / `mgba_live_input_clear` | 持续按住/释放按键 |
| `mgba_live_run_lua` | 在 mGBA 中执行一段 Lua 代码，返回 `return` 的值 |
| `mgba_live_read_memory` | 读取一组离散地址的字节值 |
| `mgba_live_read_range` | 读取连续内存范围 |
| `mgba_live_dump_oam` | 读取 OAM（精灵属性内存） |

### 启动示例

```
mgba_live_start(rom="E:\\Workspace\\yugioh-ex2006-re\\roms\\2343.gba")
```

返回 `session_id` 和 `pid`，后续操作需使用同一 session。

---

## 三、Lua 脚本基础

### 3.1 执行环境说明

每次 `mgba_live_run_lua` 调用在 mGBA Lua 解释器中**一次性执行**，但全局变量（`_G` 表）在多次调用之间**持久保留**。

```lua
-- 第一次调用：存储数据
_G._my_data = {frame = emu:currentFrame(), value = 42}
return "saved"

-- 第二次调用：读取数据
return _G._my_data.frame  -- 返回之前存的帧号
```

> ⚠️ MCP server 重启后全局变量清零。

### 3.2 常用 API

```lua
-- 读取内存（字节/16位/32位）
local b  = emu:read8(addr)
local hw = emu:read16(addr)
local w  = emu:read32(addr)

-- 写入内存
emu:write8(addr, value)
emu:write16(addr, value)
emu:write32(addr, value)

-- 当前帧号
emu:currentFrame()

-- 按键模拟（bitmask：A=1, B=2, SELECT=4, START=8, RIGHT=16, LEFT=32, UP=64, DOWN=128, R=256, L=512）
emu:setKeys(bitmask)

-- 注册帧回调（有效！每帧触发）
callbacks:add("frame", function()
    _G._frame_count = (_G._frame_count or 0) + 1
end)
```

### 3.3 帧回调的正确使用

`callbacks:add("write", ...)` 对 DMA 写入**无效**，不要依赖它监控 VRAM 变化。
`callbacks:add("frame", ...)` **有效**，可以用于每帧轮询或监控内存。

```lua
-- 注册帧监控（保存基准快照）
_G._watch_active = true
_G._base_ewram = {}
for i = 0, 100 do
    _G._base_ewram[i] = emu:read32(0x02000000 + i * 4)
end
callbacks:add("frame", function()
    if not _G._watch_active then return end
    for i = 0, 100 do
        local v = emu:read32(0x02000000 + i * 4)
        if v ~= _G._base_ewram[i] then
            _G._changes = _G._changes or {}
            table.insert(_G._changes, string.format("0x%08X: %08X -> %08X",
                0x02000000 + i * 4, _G._base_ewram[i], v))
            _G._base_ewram[i] = v
        end
    end
end)
return "监控已启动"
```

---

## 四、典型分析流程

### 4.1 分析页面切换时的 VRAM 变化

**目标**：按下 A 键进入卡牌详情页时，记录 VRAM 发生了什么变化。

**步骤一：读取 DISPCNT 确定显示模式**

```lua
local dispcnt = emu:read16(0x04000000)
local mode = dispcnt & 0x7
local bg_enable = (dispcnt >> 8) & 0xF
return string.format("DISPCNT=0x%04X mode=%d BG(0-3)=%s%s%s%s",
    dispcnt, mode,
    (bg_enable&1)>0 and "0" or "-",
    (bg_enable&2)>0 and "1" or "-",
    (bg_enable&4)>0 and "2" or "-",
    (bg_enable&8)>0 and "3" or "-")
```

**步骤二：记录按键前 BG map 快照**

```lua
_G._before_map = {}
for i = 0, 8191 do
    _G._before_map[i] = emu:read16(0x06000000 + i * 2)
end
return "快照已保存，共 " .. #_G._before_map .. " 条目"
```

**步骤三：按下 A 键并等待**

（通过 `mgba_live_input_tap` 工具，按 A 并等待 120 帧）

**步骤四：对比 VRAM 变化**

```lua
local changes = {bg0=0, bg1=0, bg2=0, bg3=0}
local samples = {}
for i = 0, 8191 do
    local addr = 0x06000000 + i * 2
    local after = emu:read16(addr)
    if after ~= _G._before_map[i] then
        local region = math.floor(i / 2048)
        local keys = {"bg0","bg1","bg2","bg3"}
        changes[keys[region+1]] = changes[keys[region+1]] + 1
        if #samples < 5 then
            table.insert(samples, string.format("0x%08X: %04X->%04X", addr, _G._before_map[i], after))
        end
    end
end
return string.format("BG0:%d BG1:%d BG2:%d BG3:%d\nSamples: %s",
    changes.bg0, changes.bg1, changes.bg2, changes.bg3,
    table.concat(samples, "\n"))
```

### 4.2 读取 BG 控制寄存器

```lua
local result = {}
local bgnames = {"BG0","BG1","BG2","BG3"}
for i = 0, 3 do
    local bgcnt = emu:read16(0x04000008 + i * 2)
    local priority  = bgcnt & 0x3
    local char_block = (bgcnt >> 2) & 0x3   -- 每块 16KB，tile 数据起始
    local mosaic    = (bgcnt >> 6) & 0x1
    local color256  = (bgcnt >> 7) & 0x1    -- 0=16色, 1=256色
    local map_block = (bgcnt >> 8) & 0x1F   -- 每块 2KB，地图数据起始
    local overflow  = (bgcnt >> 13) & 0x1
    local size      = (bgcnt >> 14) & 0x3
    local tile_base = 0x06000000 + char_block * 0x4000
    local map_base  = 0x06000000 + map_block * 0x800
    table.insert(result, string.format(
        "%s CNT=0x%04X pri=%d tiles@0x%08X map@0x%08X %s size=%d",
        bgnames[i+1], bgcnt, priority, tile_base, map_base,
        color256==1 and "256色" or "16色", size))
end
return table.concat(result, "\n")
```

### 4.3 读取 BG 地图并可视化

```lua
-- 读取 BG3 地图（30列×20行，分析文字布局）
local map_base = 0x0600F800
local result = {"BG3 Map (tile index, rows 0-19):"}
for row = 0, 19 do
    local tiles = {}
    for col = 0, 29 do
        local entry = emu:read16(map_base + (row * 32 + col) * 2)
        local tile_idx = entry & 0x3FF  -- 低10位是 tile 编号
        table.insert(tiles, string.format("%3d", tile_idx))
    end
    table.insert(result, string.format("row%02d: %s", row, table.concat(tiles, " ")))
end
return table.concat(result, "\n")
```

### 4.4 读取 tile 像素数据

```lua
-- 读取 BG3 tile 16（16色，32字节/tile）
local function read_tile_4bpp(tile_idx, char_block_addr)
    local addr = char_block_addr + tile_idx * 32
    local rows = {}
    for row = 0, 7 do
        local pixels = {}
        for b = 0, 3 do
            local byte = emu:read8(addr + row * 4 + b)
            table.insert(pixels, string.format("%X%X", byte & 0xF, (byte >> 4) & 0xF))
        end
        table.insert(rows, table.concat(pixels))
    end
    return table.concat(rows, "|")
end

local result = {}
for i = 16, 27 do
    table.insert(result, string.format("tile%d: %s", i, read_tile_4bpp(i, 0x06008000)))
end
return table.concat(result, "\n")
```

### 4.5 分析 OAM（精灵）

```lua
-- 读取前 32 个精灵的 OAM 条目
local result = {"OAM Entries:"}
for i = 0, 31 do
    local base = 0x07000000 + i * 8
    local attr0 = emu:read16(base)
    local attr1 = emu:read16(base + 2)
    local attr2 = emu:read16(base + 4)

    local y      = attr0 & 0xFF
    local mode   = (attr0 >> 8) & 0x3   -- 0=正常 2=隐藏
    local shape  = (attr0 >> 14) & 0x3  -- 0=方形 1=横向 2=纵向
    local x      = attr1 & 0x1FF
    local size   = (attr1 >> 14) & 0x3
    local tile   = attr2 & 0x3FF
    local pal    = (attr2 >> 12) & 0xF

    if mode ~= 2 then  -- 只显示可见精灵
        -- shape/size 对照表（方形）: 0,0=8x8 0,1=16x16 0,2=32x32 0,3=64x64
        -- 横向: 1,0=16x8 1,1=32x8 1,2=32x16 1,3=64x32
        table.insert(result, string.format(
            "spr%02d: y=%3d x=%3d tile=%4d pal=%d shape=%d size=%d",
            i, y, x, tile, pal, shape, size))
    end
end
return table.concat(result, "\n")
```

### 4.6 搜索 ROM 中的原始数据

```lua
-- 在 ROM 中搜索特定字节序列（用于定位未压缩数据）
local function search_rom(pattern, start_addr, length)
    local plen = #pattern
    local results = {}
    local rom_base = 0x08000000
    for offset = 0, length - plen, 2 do
        local addr = rom_base + start_addr + offset
        local match = true
        for i = 1, plen do
            if emu:read8(addr + i - 1) ~= pattern[i] then
                match = false
                break
            end
        end
        if match then
            table.insert(results, string.format("ROM+0x%X (GBA 0x%08X)", start_addr + offset, addr))
            if #results >= 5 then break end
        end
    end
    return #results > 0 and table.concat(results, "\n") or "未找到"
end

-- 示例：搜索 tile 16 前4字节（作为特征）
-- pattern = {0xXX, 0xXX, 0xXX, 0xXX}
-- 注意：若数据是压缩存储的，此方法无效
return search_rom({0x22, 0x22, 0x22, 0x22}, 0, 0x200000)
```

---

## 五、GBA 内存地址速查

| 地址 | 区域 | 说明 |
|------|------|------|
| `0x04000000` | IO | DISPCNT（显示控制） |
| `0x04000008` | IO | BG0CNT（+2=BG1, +4=BG2, +6=BG3） |
| `0x05000000` | Palette RAM | BG 调色板（0x200字节） |
| `0x05000200` | Palette RAM | OBJ 调色板（0x200字节） |
| `0x06000000` | VRAM | 视显存（96KB，char/map/bitmap）|
| `0x07000000` | OAM | 精灵属性内存（1KB，128个精灵）|
| `0x02000000` | EWRAM | 外部工作RAM（256KB，游戏状态）|
| `0x03000000` | IWRAM | 内部工作RAM（32KB，栈/临时数据）|
| `0x08000000` | ROM | 游戏 ROM（镜像，只读）|

### VRAM 布局（BG 模式 0 下）

| char_block | 地址 | map_block | 地址 |
|-----------|------|-----------|------|
| 0 | `0x06000000` | 0 | `0x06000000` |
| 1 | `0x06004000` | 8 | `0x06010000`（危险：与 char_block 2 重叠）|
| 2 | `0x06008000` | 28 | `0x06037000` |
| 3 | `0x0600C000` | 30 | `0x0600F000` |
| - | - | 31 | `0x0600F800` |

> 计算公式：tile_base = `0x06000000 + char_block × 0x4000`；map_base = `0x06000000 + map_block × 0x800`

### BG Map 条目格式（16位）

```
Bits 15-14: 纵向/横向翻转标志
Bits 13-12: 调色板编号（16色模式）
Bits  9-0 : tile 编号
```

---

## 六、常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `callbacks:add("write",...)` 无效 | GBA DMA 写 VRAM 不触发 CPU 内存回调 | 改用 frame 回调，每帧主动读取并对比 |
| `emu:step()` 不推进帧 | 在 `run_lua` 一次性执行环境中无效 | 用 `input_tap` 或 `input_set` 推进帧 |
| 在 ROM 中搜不到 tile 数据 | 数据在 ROM 中是压缩存储的（LZ77/Huffman） | 找压缩块起始地址（magic=0x10/0x20/0x30），用 BIOS SWI 解压后追踪 |
| 全局变量丢失 | MCP server 或 mGBA 进程重启 | 重新初始化所需全局状态 |
