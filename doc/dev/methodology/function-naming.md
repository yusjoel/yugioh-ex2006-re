# 方法论：函数语义命名（FUN_xxxxxxxx → 语义名）

**用途**：把 Ghidra 工程里成千上万的 `FUN_xxxxxxxx` 占位符转成有语义的名字，让 decompiler 输出可读、call graph 自解释、后续逆向有上下文。

承接 [`asset-location.md`](asset-location.md)（数据段已识别）+ [`symbolization.md`](symbolization.md)（数据 label 已落到 Ghidra 和 asm 双边）后的下一层：函数代码的语义还原。

---

## 一、定位：不要追求 100%

典型 GBA 反汇编工程在自动分析后会有 2000-5000 个函数，**逐个看是不可行的**。命名工作的 ROI 是非线性的——给"枢纽"函数命名能解锁大片 decomp 可读性，给叶子函数命名只解锁一行。

**合理目标**：

- 60-70% 命名率
- 100% 命名调用图前 ~200（按 caller 数排序）
- 100% 命名已知模块入口（UI 页 / FS / 渲染管线 / 存档 / 音频）
- 长尾的 30-40% callbacks/helpers 留作 `FUN_*`，按需逆向时再命名

**反模式**：

- 不要按地址顺序"扫荡式"命名——浪费精力
- 不要给一次性 helper 起冗长描述名——`FUN_*` 比错的名字更好
- 不要在没读 decomp 的情况下基于"猜测语义"命名——错命名比无命名更难纠

---

## 二、方法分层（按 ROI 从高到低）

```
1. FID 编译器/libc 匹配   ────  外部数据库, libc/libgcc 全收
2. 硬件寄存器簇           ────  无脑批量, 一脚本 tag 上千函数
3. 数据 label 反向查询    ────  已有锚的扩展, 中等批量
4. 字符串/源码泄漏锚      ────  锚强但稀疏, 高质量精确命名
5. 状态机表反推           ────  结构化模块入口
6. 调用图前 N 手工命名    ────  最贵但最高价值
```

每一层都建议跑完再进下一层——上层产生的 tag 会给下层提供更好的上下文。

---

## 三、方法 1：FID 编译器 / libc 静态匹配

### 信号

`memcpy/memset/strcmp` 等 libc 函数、libgcc 软件除法 `__divsi3`/`__udivsi3`、ARM EABI helper `__aeabi_*`、编译器自动生成的常用模板——这些函数在不同项目里**指令字节几乎一致**（除了 relocation 处的 BL/ABS32），是 byte-pattern + mask 匹配的高 ROI 目标。

### 现实约束：Ghidra 的内置 FID 不够用

Ghidra 12.0.3 自带的 FID 数据库（`Features/FunctionID/data/*.fidbf`）**只覆盖 MSVC x86/x64**，没有 ARM。GBA / NDS 项目想用 FID，**必须自建**——靠手头的静态库 `.a` 抽 .o 现造 pattern。

### 自建 FID 流水线（推荐）

不必走 Ghidra 的 FID 框架，直接用 byte-pattern + relocation mask + ROM 搜索的轻量流水线即可，**得到的命中比 fidb 还更直观**（直接拿到 ROM 地址 + 符号名）。

#### 1. 找匹配的工具链产物

GBA 工程：

- **agbcc**（Pokemon 系列等用的 GBA gcc 4.x 修改版）→ `libc.a / libgcc.a` 含 newlib + gcc runtime
- **devkitARM**（更现代 toolchain）→ 不同版本的 `libc.a`
- 已知用某 toolchain 编译的开源 GBA 项目（如 pokeruby/pokeemerald）→ 它的 `libs/m4a.c / agb_flash*.c / libagbsyscall.s` 编译产物

#### 2. 抽 .o + 提取符号 / 字节 / relocation

每个 `.a` 内是若干 `.o`（ELF ARM relocatable）。每个 .o 通常一个或多个全局函数：

```
ar x lib*.a                       # 解 archive
nm --print-size <obj>             # T 符号 + 大小
objdump -r <obj>                  # relocation 表 (R_ARM_THM_CALL / R_ARM_ABS32 等)
objcopy -O binary -j .text <obj>  # .text 段裸字节  (单 .text 段时)
```

如果用了 `--function-sections`（每函数独立 `.text`），多 section 同名时 `objcopy -j .text` 只取第一段；改用 **pyelftools** 或 `objcopy --only-section=.text.<func>` 按 section 名提。

#### 3. 构造 pattern + mask

pattern = 函数完整字节序列。mask = 等长 byte 数组，1 = 必须等，0 = 忽略。
对每条 relocation，把目标 4 字节标 mask=0（保守覆盖 ARM/THUMB BL 4B + ABS32 4B）：

```
relocation                                       覆盖
─────────────────────────────────────────────────────
R_ARM_THM_CALL / R_ARM_THM_PC22 / R_ARM_THM_JUMP24    BL/B 4B 全 mask
R_ARM_CALL / R_ARM_PC24 / R_ARM_JUMP24                 同
R_ARM_ABS32 / R_ARM_REL32 / R_ARM_GOT32                literal pool 4B 全 mask
```

#### 4. ROM 搜索（带 anchor 加速）

朴素扫 32 MB × N 模式 太慢。优化：每个 pattern 找最长**连续未 mask 段**作 anchor，
用 `bytes.find(anchor)` 定位候选，再做 mask-aware 完整比对。

#### 5. 落地 score

每个 (pattern, ROM\_addr) 唯一匹配 → score=5（字节级证据足够强）。

### 关键陷阱：trampoline 同 byte 多名

newlib 风格的 wrapper：

```c
void *calloc(size_t a, size_t b)  { return _calloc_r(_REENT, a, b); }
void *realloc(void *p, size_t s)  { return _realloc_r(_REENT, p, s); }
FILE *fopen(const char *f, ...)   { return _fopen_r(_REENT, f, ...); }
```

编译出的 `.o` **字节完全一致**，仅 `bl _xxx_r` 的 reloc target 不同（mask 后等价）。
ROM 里如果只链了其中一个 wrapper，多个 .o pattern 都会命中同一地址——**信息不足以区分**。

处理：检测"同地址 ≥ 2 个 sym 命中" → tag 为 `fid_trampoline:name1|name2|...`，
proposed_name 留空（score≠5），等读 ROM 中实际 `bl` target 反查后 disambiguate。

### 反例：toolchain 不匹配 → 0 命中

NitroSDK（NDS SDK）原版用 **CodeWarrior for ARM (Metrowerks CW)** 编译，输出 .a 是 ARM ELF
但**指令选择 / 寄存器分配 / inline 决策跟 gcc/agbcc 完全不一样**。

实测在 GBA 工程上扫了 NitroSDK 1.0 + 2.0 RC3 共 ~9000 个全局函数（ARM7 + ARM9 多 flavor），
**唯一命中 1 个 12 字节小函数**，且高度疑似巧合。

教训：FID 之前先核对 toolchain 家族（compiler 厂商 + 主版本）。**不同家族编译出的 .a 互相不可 FID**——
连 gcc 3.x 与 gcc 4.x 都常常对不上，更不用说跨厂商。

### ROM 头路径泄漏 ≠ 链接库

ROM 里出现 `inc/<sdk>/foo.h` 这种 assert 字符串，**只能证明**：

- 那个头文件被 `#include` 进至少一个编译单元
- 编译时启用了 assert（保留 `__FILE__`）

**不能证明** SDK 的 `libfoo.a` 被链接。如果 `foo.h` 全是 `static inline`，函数会在 caller
里展开（连同 assert 字符串），但**没有独立的 `.text` 入口供 FID 匹配**。

### 典型命中（agbcc 全套）

- libc: `memcpy / memset / strlen / strcmp / strcpy / strcat / strncmp / strncpy / memcmp / qsort / sscanf`
- libc 数值：`_strtod_r / _strtol_r / _strtoul_r / __sccl / __srefill / fread / fflush / ungetc`
- libc 内存：`_malloc_r / _free_r / _malloc_trim_r / _Balloc / _Bfree / _multadd / _multiply / _s2b / _i2b`
- libgcc 整数：`__divsi3 / __udivsi3 / __modsi3 / __umodsi3 / __muldi3 / __lshrdi3 / __negdi2 / __cmpdi2`
- libgcc 浮点：`__adddf3 / __cmpdf2 / __divdf3 / __muldf3 / __addsf3 / __divsf3 / __mulsf3 / __subsf3 / __fixdfsi / __fixsfsi / __floatsidf`

### 局限

- 找不到匹配 toolchain 的产物就跳过这步
- 编译器版本 / 优化级别不同的会 miss（同 toolchain 不同版本也常常对不上）
- 自定义修改过 libgcc 的项目会大量 miss
- 内联的 libc 调用（`memcpy` 被编译成内联 ldm/stm）没有独立函数体可匹配
- `static inline` 头文件的函数在 caller 内展开，没法匹配

### 适用阶段

放在最前面。命中的函数从一开始就是"已知"的，不用再聚类。**先验证 toolchain 兼容**（小 POC 单函数试一遍），再扩到全套。

---

## 四、方法 2：硬件寄存器簇

### 信号

每个函数读写哪些 GBA IO 寄存器（`0x04000000-0x040003FE`）。GBA 硬件功能高度集中在 IO MMIO，因此函数的 "IO 触碰集" 强烈关联其语义角色。

### 操作

```
walk all functions:
    for each instruction in function body:
        if operand is memory ref to [0x04000000, 0x04000400):
            tag function with reg name
output: addr,name,io_tags  CSV
```

实现要点：

- `Listing.getInstructionsInFunction()` 拿指令，扫每条的 operand reference
- IO 寄存器名靠 `gba_io.inc`（标准化的 96 个 MMIO 名字表）做地址→名字映射
- 每个函数得到一个 tag 集，例如 `{DISPCNT, BG0CNT, BG1CNT}`

### 命名规则

按 tag 集的**主导寄存器家族**决定前缀：

| 主导触碰 | 前缀建议 | 推断角色 |
|---------|---------|---------|
| `DISPCNT, BGxCNT, BGxHOFS/VOFS` | `bg_*` / `display_*` | 显示模式 / BG 配置 / 滚动 |
| `OAM 0x07000000-0x070003FF` | `obj_*` | sprite (OBJ) |
| `PALRAM 0x05000000-0x050003FF` | `pal_*` | 调色板 |
| `DMAxSAD/DAD/CNT` | `dma_*` | DMA 调度 |
| `SOUNDxCNT_L/H, SOUNDCNT_*` | `snd_*` | 音频 |
| `KEYINPUT, KEYCNT` | `input_*` | 按键采样 |
| `WAITCNT, IME, IE, IF` | `sys_*` / `irq_*` | 系统 / 中断 |
| `TM0-3CNT_L/H` | `timer_*` | 定时器 |
| `SIOCNT 等` | `sio_*` | 通信 |

**命名只到家族级，不到具体功能**——`bg_setup_2`、`bg_clear_screenblock` 这种细分不要瞎填，只标 `bg_*` 前缀；具体语义留到方法 4-6 精化。

### 局限

- 不区分相邻寄存器的语义差异（`BG0CNT` vs `BG3CNT`）——但作为聚类已足够
- 函数体内可能没有直接 IO 触碰，但通过 helper 间接触碰——这种漏掉，需要 caller 传播
- 同一个函数可能触碰多个家族（"页面 init" 一次写所有 BG/OAM/PAL）——保留全 tag 集，命名规则按"出现次数最多"裁

### 适用阶段

工程一上来。无任何前置知识依赖。

---

## 五、方法 3：数据 label 反向查询

### 信号

工程已经手动 label 了关键数据结构（卡数据表、字体表、状态表、FS master struct 等）。**所有读 / 写这些地址的函数都是该模块的成员**。

### 操作

```
for each known data label L:
    refs = ReferenceManager.getReferencesTo(L)
    for ref in refs:
        if ref.from is in a function F:
            tag F with module name from L
```

实现要点：

- 数据 label 必须先打到 Ghidra（参见 `symbolization.md`）
- 对每个 label，`ReferenceManager.getReferencesTo()` 返回所有引用点
- 每个引用点回查所在函数 → 函数和该 label 同模块
- 一个函数可能被多个 label 标多次，按出现频率裁

### 命名规则

| label 锚类型 | 函数前缀 |
|---------|---------|
| `<table>_table` (任何枚举/查找表) | `<table>_*` |
| `<font>_table` 字体表 | `font_*` |
| `<fs>_master_struct` | `fs_*` |
| `<module>_state_table[]` | `<module>_page_*` |

### 局限

- 只覆盖直接读 / 写 label 的函数；间接通过 helper 的覆盖不到
- label 锚的命名前缀质量决定了反推命名质量（垃圾进垃圾出）

### 适用阶段

`ImportProjectLabels.py` 之类的脚本跑过、关键数据 label 已落地之后。

---

## 六、方法 4：字符串 / 源码泄漏锚

### 信号

未 strip 的 ROM 里常残留：

- C 源文件路径（`"src/gl/gl_common.c"`）
- assert 消息（`"i < ARRAYSIZE(table)"`、`"bright >= -16 && bright <= 16"`）
- printf / log 格式串（`"loaded %s, size=%d"`）
- 函数签名残片（`"void update_status(int)"`）

这些字符串会被它的所属函数 `ldr =<addr>` 或 `adr` 引用，因此**"哪个函数指向这条字符串"几乎等价于"这条字符串属于哪个函数"**。

### 操作

```
1. 全 ROM 扫 ASCII 区间 [0x20, 0x7E], 收集 >= 4 字符的连续串
2. 过滤候选: 只留含 ".c"/".cpp" / "assert" / "%" / "/" 或 snake_case 单词
3. 对每个候选串 S:
    - 找 ROM 内所有 .word 指向 S 的位置
    - 这些位置所在函数 → 候选命名锚
4. 读 decomp, 确认串与函数行为吻合后命名
```

### 命名规则

字符串的**类型决定提取方式**：

- **源文件名** (`"GL/GL_Common.c"`)：该单元里所有函数 → `gl_*` 前缀
- **assert 消息**：透露参数语义和约束
  - `"bright >= -16 && bright <= 16"` → 函数有 `bright` 参数，范围 `[-16, 16]` → `set_brightness`
- **printf 格式串**：透露函数行为
  - `"deck %s saved with %d cards"` → `deck_save` / `deck_serialize`
- **panic / log 前缀**：透露模块归属
  - `"[SaveMgr] failed to commit"` → `save_mgr_*`

### 局限

- 字符串密度因 ROM 而异；商业游戏常 strip
- assert 在 release build 里可能被宏掉（保留在 debug build）
- 需要人工读 decomp 确认，不能纯自动
- 函数可能引用多个串，需要选最语义化的

### 适用阶段

任何阶段都可以跑。建议在方法 2-3 给函数打完家族 tag 后跑——能精确细化 tag 内的具体函数。

---

## 七、方法 5：状态机表反推

### 信号

GBA 游戏的页面 / UI 大量使用**函数指针表**实现状态机：

```c
typedef void (*PageFn)(void);
struct PageState {
    PageFn init;
    PageFn load_assets;
    PageFn tick;
    PageFn exit;
};
struct PageState g_some_page = { some_init, some_load, some_tick, some_exit };
```

ROM 里表现为**连续的 4 字节 word，全部是 Thumb 函数指针** (`0x08xxxxxx | 1`)。识别出表的起点 + 长度，就解出一组结构化的函数家族。

### 操作

```
1. 扫 ROM 找"连续 N 个 word, 全部是合法的 Thumb 函数指针"
   合法 = target 在代码段, target 首指令是 prologue (push {...,lr})
2. N 通常 4 (init/load/tick/exit) 或 4 的倍数 (多页面共表)
3. 每张表起点登记为"状态表入口", 长度按 prologue-连续 启发式判定
4. 表内每个 entry 按位置语义命名
```

### 命名规则

按表所在位置 / 上下文（caller、临近字符串、IO tag）推断模块名 `<module>`，然后表的 4-entry 标准命名：

| entry index | 命名建议 |
|------------|------|
| `[0]` | `<module>_init` 或 `<module>_page_init` |
| `[1]` | `<module>_load_assets` 或 `<module>_setup` |
| `[2]` | `<module>_tick` 或 `<module>_main_loop` |
| `[3]` | `<module>_exit` 或 `<module>_cleanup` |

如果是 `n × 4` 多页面共表，每 4 个为一组分别命名（`<page>_init/load/tick/exit`），表本身命名 `<game>_page_state_table`。

### 局限

- 只对采用此模式的页面有效；不是所有 UI 都用状态表
- 表长度推断靠"连续 prologue 指针"启发式，可能过短 / 过长——需要人工核对
- 命名 `<module>` 还要靠其他线索（字符串、IO tag、caller chain）

### 适用阶段

方法 1-4 跑完后，背景 tag 已足以推断 `<module>` 名。也可以倒过来用——发现一张状态表后，从 entry 函数体里读 IO/字符串再回填 `<module>`。

---

## 八、方法 6：调用图前 N 手工命名

### 信号

调用图里**入度高（被到处调用）的函数 = 基础设施**。一个 `memcpy_aligned` 的命名能让上百处调用方的 decomp 立即可读。给前 ~200 个 hub 函数命名，覆盖 80% 的调用流量。

### 操作

```
1. 对每个 FUN_*, 数 incoming BL/BLX ref 数量 (caller_count)
2. 同时数 outgoing call 数 (callee_count), 形成函数角色画像:
    - caller_count 高 + callee_count 低  ──  叶子 helper (lib-like)
    - caller_count 低 + callee_count 高  ──  顶层 orchestrator
    - 都高                                ──  中层 dispatcher / state root
3. 按 caller_count 倒序输出 top N (典型 N=200)
4. 对每个 top 函数: 读 decomp, 起名, 写到批量 rename 脚本
```

### 命名原则

不可纯算法化，需要读 decomp。但有几条惯例：

- **Hub 函数命名要短**：`memcpy_u32` / `get_card_id` / `vblank_wait` 这种，被频繁出现
- **不要前缀过载**：`gl_pal_dma_safe_copy_with_check` 比 `pal_dma_copy` 难读
- **先打 tag 再放回去**：如果一时难命名，加 plate comment `// TODO: BG VRAM helper`，别强行命名
- **保留 FUN_xxxxxxxx 后缀如果不确定**：`bg_helper_FUN_080xxxxx` 比错的名字诚实

### 局限

- 时间成本最高（人工 decomp + 命名）
- 错误命名比 `FUN_*` 更糟——会误导后续逆向
- 只适合"看一眼就懂"的函数；复杂逻辑留到模块级专项逆向

### 适用阶段

放最后。前 5 个方法已经把背景 tag 打满了，这一步只命名 "显然是 hub 但 tag 不足以决定具体语义" 的函数。

---

## 九、组合策略

### 推荐顺序

```
0. 工程导入 + 默认分析跑完, 函数总数稳定后再开始
1. FID 匹配             ──  50-200 个标准库函数立即命名
2. IO 寄存器簇          ──  几乎所有函数获得家族 tag
3. 数据 label 反推      ──  tag 强化, 模块边界清晰
4. 字符串/源码泄漏锚    ──  高质量精确命名
5. 状态机表扫           ──  结构化模块入口
6. 手工前 N             ──  收尾, 命名 hub
```

### 上下层互喂

每一层都把已落地的 tag 带给下一层：

```
方法 2 给函数 X 标 {bg_*}
方法 4 找到字符串 "setup_bg2_2bpp" 在 X 旁边
最终命名为 bg2_setup_2bpp  →  既知道家族 (bg)
                              又知道具体功能 (setup, 2bpp)
                              又知道目标 BG (2)
```

### 退化场景

如果某层 yield 远低于预期（比如 FID 找不到匹配的数据库），跳过下一层。每层都是独立可复用的，没有强依赖。

---

## 十、反模式：候选地址提升的最后防线

任何"自动把候选地址提升为函数"的脚本（pointer table 反推、orphan code 提升、call graph 补齐）都应该套**至少 5 重过滤**：

1. target 在代码段（避开数据区）
2. target 已被反汇编（`getInstructionAt != None`）
3. target 不是已知函数入口（去重）
4. target 不在既有函数体内（避免劈裂）
5. **target 首指令必须是 prologue**（`push {...,lr}` 或 `stmfd sp! {...,lr}`）

第 5 条最关键。**`getFunctionContaining == None` 不等于 "这是函数入口"**——orphan disassembly（已反汇编但未归属任何函数的代码片段，典型如 IRQ handler 尾段）会绕过前 4 条而通过；只有 prologue 检查能识别出"这其实是函数中段不是入口"。

历史教训：跨数 MB 的随机数据 word 偶然碰到形如 `0x080002xx | 1` 的字节序列时，前 4 条检查都通过；如果没有 prologue 检查，会把一段连续函数（如 IRQ handler）切成多个假函数，每个假函数都"看起来合法"但实际上是同一个真函数的中段。

### ARM Aggressive Instruction Finder 的危险

Ghidra 的 `ARM Aggressive Instruction Finder` 分析器**不受 `reAnalyzeAll(addressSet)` 约束**，会扫整个 executable memory。在数据段被标记 `EXECUTE` 的 ROM 上跑这个，会把卡数据 / 图形 / 音频数据按字节模式当 ARM 指令反汇编，触发连锁污染。

**安全前提**：要跑 AAIF，必须先确保数据段 memory block 的 `EXECUTE` 标志为 `False`。否则禁用此分析器。

---

## 十一、何时停止

```
检查指标:
  - 命名率       = named / total_funcs
  - 调用图覆盖   = sum(callers of named funcs) / sum(all callers)
```

**停止条件**（任一满足）：

- 命名率达 60-70%（剩下都是长尾 helper / callbacks）
- 调用图覆盖达 90% 以上
- 进入 "需要读 decomp 才能命名" 的阶段，每个函数 5-10 分钟，ROI 已显著下降

剩下的长尾留作 `FUN_*`，等具体逆向某模块时按需补命名。**改动 ROM 后跑一次函数清单脚本看新增 `FUN_*` 列表，按需补回**——这是常态化维护，不是一次性目标。

---

## 十二、参考

- [`asset-location.md`](asset-location.md)：数据段定位（命名工作的前置）
- [`symbolization.md`](symbolization.md)：数据 label 落地（方法 3 的前置）
- [`build-pipeline.md`](build-pipeline.md)：Ghidra 改动后重导 asm/all.s + 构建 round-trip
- [`font-glyph-ocr.md`](font-glyph-ocr.md)：字符串泄漏锚的特殊场景（字模识别）
