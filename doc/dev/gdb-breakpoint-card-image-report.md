# GDB 断点验证报告：卡牌大图加载函数链

**日期**：2026-04-16
**状态**：实验完成，全部断点命中

---

## 背景

在卡牌大图导出完成后（`card-image-export.md`），方法论总结（`locate-rom-asset-from-vram-diff.md`）将"GDB 下断"完全排除在推荐路径之外，理由是之前的断点实验（`gdb-watchpoint-card-image.md`）全部失败。

本次实验验证：**如果从已知的正确函数地址出发**，GDB 硬件断点完全可以断到有用的代码。之前失败的原因是断错了函数（BIOS SWI 路径 vs 实际的 6bpp 解码路径）。

---

## 实验方法

### 工具链

- mGBA MCP（`mgba_live_start`）+ GDB MCP 双 MCP 并用
- GDB batch 脚本（`--batch -x script.gdb`）绕过 GDB MCP 的异步通知限制
- mGBA MCP `input_set` 注入按键触发卡牌详情页转场

### 流程

```
1. mgba_live_start (rom + ss1 存档) → 游戏暂停在 stub
2. GDB batch 连接 → 设 3 个 hbreak → continue → 游戏放行
3. mGBA MCP input_set(["A"]) → 触发卡牌列表→详情页转场
4. 断点依次命中 → GDB 打印寄存器/反汇编/内存 → kill 退出
```

### 关键发现：GDB batch 优于 GDB MCP 交互模式

| 方面 | GDB MCP 交互 | GDB batch |
|------|-------------|-----------|
| 设断点（暂停态） | ✅ | ✅ |
| continue 后设断点 | ❌ 超时 | N/A |
| 检测断点命中 | ❌ 超时（异步通知问题） | ✅ 自动 |
| 命中后读寄存器 | ❌ 超时 | ✅ `info registers` |
| 命中后 continue 到下一个 BP | ❌ | ✅ |
| 与 mGBA MCP 并用 | 需复杂时序 | ✅ 后台运行 + MCP 按键 |

**结论**：涉及断点的调试场景，应优先使用 GDB batch 脚本，将 GDB MCP 限制在不需要 continue/断点的场景（如暂停态读寄存器、单步执行）。

---

## 断点命中详情

### 调用链验证

```
card_info_page_entry (0x0801E440)      ← 按 A 触发
  ├── bl card_info_page_init_bg0 (0x0801D45C)   [HIT 1]
  └── bl card_image_decode_wrapper (0x0801D998)  [HIT 2]
         └── bl decode_card_image_6bpp (0x0801D290)  [HIT 3]
```

LR 寄存器验证：
- HIT 1 的 LR = `0x0801E447`（card_info_page_entry + 0x07，即 `bl 0x801d45c` 下一条指令）✅
- HIT 2 的 LR = `0x0801E457`（card_info_page_entry + 0x17）✅
- HIT 3 的 LR = `0x0801DA0D`（card_image_decode_wrapper + 0x75）✅

### HIT 1：card_info_page_init_bg0 (0x0801D45C)

| 寄存器 | 值 | 含义 |
|--------|-----|------|
| PC | 0x0801D45C | BG0 初始化函数入口 |
| r4 | 0x0201AFB0 | 卡选择数据结构指针 |
| LR | 0x0801E447 | 返回到 card_info_page_entry |

反汇编摘要：
```arm
push  {r4, lr}
ldr   r0, [pc, #132]   ; 加载 IO 基址
movs  r1, #0xBA
lsls  r1, r1, #1       ; r1 = 0x174（WININ 偏移）
adds  r0, r0, r1
movs  r1, #0x21
strh  r1, [r0, #0]     ; 写 WININ
movs  r1, #128
lsls  r1, r1, #19      ; r1 = 0x04000000（IO 基址）
movs  r0, #0x40
strh  r0, [r1, #0]     ; DISPCNT |= BIT6（启用 WIN0）
```

### HIT 2：card_image_decode_wrapper (0x0801D998)

| 寄存器 | 值 | 含义 |
|--------|-----|------|
| PC | 0x0801D998 | wrapper 入口 |
| **r0** | **0x052B = 1323** | **card_id**（Despair from the Dark） |
| r1 | 0x0AF0 = 2800 | 参数（用途待确认） |
| r2 | 0x0BB8 = 3000 | 参数（用途待确认） |
| r4 | 0x0201AFB0 | 卡选择结构指针 |
| LR | 0x0801E457 | 返回到 card_info_page_entry |

反汇编摘要：
```arm
push  {r4, r5, r6, r7, lr}
mov   r7, r10 / r6, r9 / r5, r8    ; 保存高寄存器
push  {r5, r6, r7}
sub   sp, #12
lsls  r0, r0, #16
lsrs  r5, r0, #16     ; r5 = card_id（清零高 16 位）
lsls  r1, r1, #16
lsrs  r1, r1, #16     ; 清零高 16 位
str   r1, [sp, #4]     ; 保存到栈
```

### HIT 3：decode_card_image_6bpp (0x0801D290)

| 寄存器 | 值 | 含义 |
|--------|-----|------|
| PC | 0x0801D290 | 6bpp 解码器入口 |
| **r0** | **0x06000000** | **VRAM 目标基址** |
| **r1** | **0x82 = 130** | **调色板偏移**（6bpp 像素索引 += 130；最终索引范围 130–193） |
| **r2** | **0x052B = 1323** | **card_id** |
| **r3** | **0x02** | **flag**（=2，意义待确认，可能是 TCG 版标记） |
| r12 | 0x098509A4 | 中间计算值 |
| LR | 0x0801DA0D | 返回到 wrapper |

反汇编摘要：
```arm
push  {r4, r5, r6, r7, lr}
mov   r7/r6/r5, r10/r9/r8    ; 保存高寄存器
push  {r5, r6, r7}
sub   sp, #8
adds  r4, r0, #0      ; r4 = VRAM 目标地址
ldr   r0, [sp, #40]   ; 从栈上读取额外参数
lsls  r1, r1, #16     ; 清零高 16 位
lsls  r2, r2, #16
lsls  r3, r3, #16
lsls  r0, r0, #16
```

### 内存验证

```
0x0201AFB0: 0x00002958 → card_id = (0x2958 << 15) >> 18 = 0x052B = 1323 ✅
BG0CNT:     0x0086 (8bpp, charblock 1, screenblock 0, priority 2) ✅
VRAM 0x06004000: 全零（解码刚开始，尚未写入）✅
```

---

## 新发现：decode_card_image_6bpp 的参数签名

基于断点数据，解码器完整签名（之前未完全确认）：

```c
// r0 = VRAM 目标基址（通常 0x06000000，非 0x06004000）
// r1 = 调色板偏移（6bpp 索引加上此值后得到最终 8bpp 索引）
// r2 = card_id
// r3 = flag（0=OCG? 2=TCG?）
// [sp+0x28] = 额外参数（从栈上读取）
void decode_card_image_6bpp(u32 vram_base, u16 pal_offset, u16 card_id, u16 flag, ...);
```

**r1=0x82=130 的含义**：
- 之前文档记录 r1=0x10（调色板从 pal[16:80]）
- 本次实测 r1=0x82=130（调色板从 pal[130:193]）
- 这意味着 BG palette 的前 128 色留给 UI/BG1-3 使用，卡图使用 pal[130:193]（64 色）
- 8bpp 模式下 256 色调色板中 [130..193] 这一段是卡图专用

**r3=2 flag 的含义**：
- 之前文档 `flag=0` OCG, `flag=1` TCG
- 实测 `flag=2`，可能是第三种变体或编码方式不同
- 需要进一步实验（在不同卡上断点对比）

---

## VRAM Watchpoint 追加实验

在 hbreak 实验成功后，追加验证 VRAM write watchpoint 能否**在不知道函数地址的前提下**定位解码器。

### 实验设计

同时设 1 个 watchpoint（`0x06004040`，解码器首次 VRAM 写入地址）和 1 个 hbreak（`0x0801D290`，已知解码器入口）作为对照。

### 结果

| 命中顺序 | 类型 | PC | 函数 | 说明 |
|---------|------|-----|------|------|
| HIT 1 | **watchpoint** | `0x080F4E86` | `memset/memclear` | VRAM 清零（Old=16→New=0），LR=`0x0801D47D`（init_bg0 内部） |
| HIT 2 | **hbreak** | `0x0801D290` | `decode_card_image_6bpp` | 紧接清零之后，解码器入口 |

### 分析

**Watchpoint 确实能工作**，但第一个抓到的不是解码器，而是 **VRAM 清零函数**（`FUN_080F4E74`）。清零函数的 **LR=`0x0801D47D`** 指向 `card_info_page_init_bg0`，从这里向上追溯 1-2 步即可到达 `card_info_page_entry` 和 `decode_card_image_6bpp`。

**纯动态路径已验证成功**（追加实验：仅 watchpoint，无 hbreak）：

```
watch *(unsigned char*)0x06004040

HIT 1 (continue ①):
  PC = 0x080F4E86 (memclear), LR = 0x0801D47D (init_bg0)
  Old=16 → New=0 (清零)

HIT 2 (continue ②):
  PC = 0x0801D406 (decode_card_image_6bpp 内部, 第二循环 palette offset 调整)
  Old=0 → New=16 (解码后像素索引)
  r4 = 0x06004042 (VRAM 写指针, 刚写完 0x06004040)
  LR = 0x0801D331 (函数体内跳转点)
```

**2 次 continue 即可直接命中解码器内部**。从 PC=`0x0801D406` 向上找 `push {r4,r5,r6,r7,lr}` 即可定位函数入口 `0x0801D290`。

之前实验未能断到写入的原因：hbreak 在解码器**入口**就拦截了，解码器尚未执行到 VRAM 写指令。去掉 hbreak 后，watchpoint 自然在第二次 continue 时命中解码器的 `strh`。

### 操作要点（ss1 存档界面）

- ss1 存档在**卡组编辑列表页**——**需要按两次 A**：第一次 A 选中卡牌，第二次 A 打开详情页
- `input_set(["A"])` → `sleep 2` → `input_clear` → `sleep 2` → 再次 `input_set(["A"])`

---

## 方法论修正

### 之前的结论（`locate-rom-asset-from-vram-diff.md`）

> GDB watchpoint 反复向上溯源在本项目不可靠，用 IO 寄存器配置值或其它强语义指纹做全 ROM 搜索才是主路径。

### 修正后

上述结论仍然正确作为**首选路径**，但 GDB 能力被严重低估。三种场景各有最佳工具：

| 场景 | 推荐方法 |
|------|---------|
| 从零定位未知资产的加载函数 | **静态分析**（VRAM diff → IO 指纹 → 全 ROM 搜索），效率最高，一步到位 |
| 同上，备选路径 | **VRAM watchpoint**（watch 写入地址 → 2 次 continue → 直接命中解码器内部），需 2 轮调试 |
| 已知函数地址，验证参数/调用链 | **GDB hbreak**（batch 脚本，一次性捕获全部寄存器） |

### GDB batch 最佳实践（本次实验总结）

```
1. mgba_live_start (rom + savestate, -g patch) → 游戏暂停
2. GDB --batch -x script.gdb（后台运行）：
   - target remote localhost:2345
   - hbreak *<addr1> / hbreak *<addr2> / ...
   - continue（阻塞等待）
3. mGBA MCP input_set 触发转场
4. 断点命中 → info registers / x/Ni $pc / x/Nx <addr> → kill + quit
5. 读 GDB 输出文件提取数据
```

**注意**：GDB batch 的 `kill` 会消耗 stub（mGBA 不再接受 GDB 连接），需要 `mgba_live_stop` + 重新 `mgba_live_start` 才能开始下一轮调试。

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `doc/dev/scripts/gdb_card_bp_full.gdb` | 本次实验使用的 GDB batch 脚本 |
| `doc/dev/scripts/gdb_card_image_bp.gdb` | 首次验证用脚本（仅 card_info_page_entry） |
| `doc/dev/analysis-card-image-loading-function.md` | 静态分析记录（含错误路径） |
| `doc/dev/locate-rom-asset-from-vram-diff.md` | 方法论总结（需参照本文修正） |
| `doc/dev/gdb-watchpoint-card-image.md` | 早期 watchpoint 实验（全部失败） |
