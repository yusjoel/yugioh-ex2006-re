# Refine Review: F09-Seg-3

Segment range: `[0x0807104c, 0x080719fc)` — `asm/09_equip_lp_display.s` lines 5342..6675

---

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与 §五 路线图一致 | PASS | Seg-3 = [0x7104c..0x719fc), 20 fn, 39 slots, 2 ROM_INCBIN — 与路线图完全匹配; Seg-2 已在 0x7104c 结束 |
| C2 | 每个 ROM_INCBIN 块都有归宿 | PASS | Block1 0x716fa/0x42 -> DISASM; Block2 0x71754/0x9c -> DISASM; 共 2 块全覆盖 |
| C3 | §5.1 块确 0 引用 | PASS | §5.1=0; Block1 有 THUMB+1 引用 @0x09e40e98; Block2 有 5 个 raw 引用 @PTR_DAT_08071740[0..4] — 自主重跑 ref-scan 确认 |
| C4 | R1 值 == ROM 4 字节小端 | PASS | 独立 python 验证 21 个槽 (含 dispatch table 5 条目 + 全部关键 EQ 槽) 全部与 ROM 字节一致 |
| C5 | 新建 constants 前确无现有可复用 | PASS | EQUIP_ZONE_WORD_MASK=0x00f0ffff: grep 0 命中; FREED_THE_MATCHLESS_GENERAL_CID=0x000014c4: grep 0 命中; DRAGGED_DOWN_INTO_GRAVE_CID=0x000014e8: grep 0 命中 |
| C6 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | NEEDS_FIX | **#1**: DWORD_08071538 提议标签 `invoke_effect_node_with_active_flag_3arg_ptr` 无地址后缀; Seg-2 同值槽已命名 `invoke_effect_node_with_active_flag_3arg_ptr_0a64` (带 `_0a64`), 应统一加 `_1538` 后缀以区分 |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | carve=0; REF_SLOTS=0; 全部 RAM global 走 EQ_REUSE (.equ 方式); gP1LifePoints 槽 .word 已含符号 (非裸地址) |
| C8 | plate 引用全用现名, 无残留旧 FUN_ | NEEDS_FIX | **#2**: RENAME_SLOTS 中 DWORD_08071538 的 EOL 写 "same as DAT_08070a64 in Seg-2" — `DAT_08070a64` 是旧自动名; Seg-2 已将该槽改名为 `invoke_effect_node_with_active_flag_3arg_ptr_0a64`; EOL 必须引用现名 |
| C9 | ASCII-only 注释 | PASS | Seg-3 仅 L6141 含 CJK (已被 PLATE-1 计划覆盖); 提议的所有 plate/EOL 文本经 python 逐字符验证为纯 ASCII |
| C10 | 指针表条目 `+1` (THUMB), `.word <fn>+1` == ROM raw 值 | PASS | DWORD_0807129c=0x08071259=check_effect_slot_equip_zone_pattern+1 (fn push{lr} @ 0x08071258 确认); DWORD_08071538=0x08090625=invoke_effect_node_with_active_flag_3arg+1 (fn push{r4,r5,r6,lr} @ 0x08090624 确认); Block1 THUMB+1 ref 0x080716fd=0x80716fc+1 确认 |
| C11 | 函数体全局 vs 函数名矛盾时已标 FUNC_RENAME | PASS | 扫描 20 fn: FUNC_RENAME=0 合理; `eligible_dragged_down_into_grave_16fc` 标签对应 FS handler table 的 fn_eligible 槽 (+4 from CID), 命名一致 |
| C12 | 关键槽语义有 file:line + 置信度, 无零容忍词 | PASS | 所有 EQ_NEW + RENAME 槽有 asm/09 具体行号 + conf:high; card-stats.s passcode 逐一核对; 无零容忍词 |
| C13 | 段内所有残留自动名槽被覆盖 | PASS | 独立 python 精确清点: 39 个 DWORD_/DAT_/PTR_DAT_ 槽; 提议 EQ_REUSE(33)+EQ_NEW(2)+RENAME_fnptr(2)+RENAME_dispatch(1)+RENAME_block(1)=39; 完美匹配无遗漏无重复 |

---

## 自主 ref-scan 结果

### Block1: 0x080716fa/0x42

独立扫描 4B 对齐步进全 ROM:

- raw 命中 4 处: @0x84318e4 (-> 0x80716fc), @0x841f624 (-> 0x8071710), @0x8453ce0 (-> 0x8071704), @0x9e40e98 (-> 0x80716fd)
- 0x084xxxxx 三处 (0x84318e4/0x841f624/0x8453ce0): 均在压缩图形数据区 (ROM offset 0x41xxxx..0x45xxxx), 周边字节为高熵随机数据, 确认为压缩数据误中假阳性 — 非有效引用
- THUMB+1 命中 1 处: @0x9e40e98 -> fn = 0x80716fc (与提议一致)
- FS handler table 结构确认: entry 0x9e40e94..0x9e40ea8 = [CID=0x14e8, fn_eligible+1=0x80716fd, pad, fn_activate+1=0x0805f645, pad, pad]; 0x18B 标准结构, CID 在 fn_ptr-4 (0x9e40e94)
- CID = 0x000014e8 = Dragged Down into the Grave (card-stats.s card_1048, pw=16435215) 确认
- 函数体追踪确认: push {r4,r5,lr} @ 0x80716fc; BHI 分支 @ 0x807171e 目标 0x80717e8 (block2 sub-stub 5 的公共返回路径); 通过 LDR r1,[pc,#0x18] @ 0x8071722 加载 PTR_DAT_08071740 并 MOV PC,r0 跳转至 sub-stub — block1 fn 与 block2 sub-stubs 构成同一函数逻辑单元, DISASM 分类正确

**verdict: DISASM 正确** (THUMB+1 真引用 @0x9e40e98; raw hits 全为压缩数据假阳性)

### Block2: 0x08071754/0x9c

独立扫描:

- raw 命中 5 处: @0x8071740(->0x80717c4), @0x8071744(->0x80717a4), @0x8071748(->0x807178a), @0x807174c(->0x807177c), @0x8071750(->0x8071754)
- 全部 5 个引用来自同段 PTR_DAT_08071740 dispatch table (L6364-6368), 均为有效 raw code 地址
- THUMB+1 命中 0 处 (确认)
- 5 个 sub-stub 入口验证: 均无 push 序言 (因通过 MOV PC,r0 到达, 共享 block1 fn 的栈帧); 出口均跳转至 block2 末尾的公共返回路径 (0x80717e8/0x80717ec)

**verdict: DISASM 正确** (5 raw 引用全部来自有效 dispatch table; 无 THUMB+1)

---

## ROM 字节核对 (C4)

独立 python 验证 32 个槽 (21 关键槽 + 11 追加样本) 全部 OK:

- gDuelPhaseFlags 0x0201b290 x6: 全部 OK
- gP1LifePoints 0x0201c4e0 x6: 全部 OK
- EQUIP_ZONE_WORD_MASK 0x00f0ffff @ 0x08071280: OK
- FREED_THE_MATCHLESS_GENERAL_CID 0x000014c4 @ 0x08071344: OK
- dispatch table PTR_DAT_08071740[0..4]: 全部 OK (0x80717c4/a4/8a/7c/54)
- THUMB+1 slots DWORD_0807129c=0x08071259, DWORD_08071538=0x08090625: OK

---

## 状态: NEEDS_FIX (2 items)

---

## 修改清单

### #1 — C6 — DWORD_08071538 rename label 缺 `_1538` 后缀

**问题**: 提议将 DWORD_08071538 (值=0x08090625) 命名为 `invoke_effect_node_with_active_flag_3arg_ptr`。Seg-2 中同值同函数槽 (DWORD/DAT_08070a64) 已被命名为 `invoke_effect_node_with_active_flag_3arg_ptr_0a64`。无后缀版与有 `_0a64` 后缀版并存, 违反同类多实例加后缀的命名约定。

**要求**: 将 proposal 中 RENAME_SLOTS 表的 `new_label` 字段从:
```
invoke_effect_node_with_active_flag_3arg_ptr
```
改为:
```
invoke_effect_node_with_active_flag_3arg_ptr_1538
```

影响范围: RENAME_SLOTS 表 + Disasm Plan Block2 第 6 步提到的 EOL + Consumer Evidence 表中对应行。

---

### #2 — C8 — DWORD_08071538 EOL 含旧自动名 `DAT_08070a64`

**问题**: RENAME_SLOTS 表中 DWORD_08071538 的 `eol_comment` 字段写:
```
... same as DAT_08070a64 in Seg-2; ...
```
`DAT_08070a64` 是 Seg-2 落地前的旧自动名。Seg-2 完成后该槽已改名为 `invoke_effect_node_with_active_flag_3arg_ptr_0a64` (见 §四.02 完成记录)。EOL 中引用旧名违反 C8 (stale 自动名) 精神。

**要求**: 将 EOL 中 `DAT_08070a64` 替换为 `invoke_effect_node_with_active_flag_3arg_ptr_0a64`, 具体:
```
invoke_effect_node_with_active_flag_3arg+1 (THUMB fn-ptr; same as invoke_effect_node_with_active_flag_3arg_ptr_0a64 in Seg-2 at 0x08070a64; passed to set_equip_activation_state_by_mode__08096a4c as mode/fn param)
```

---

## 附记

以下为正向核验 (不影响状态, 记录供参考):

- **CID 核验**: FREED_THE_MATCHLESS_GENERAL_CID=0x14C4 (card_1013, pw=49681811) 与 DRAGGED_DOWN_INTO_GRAVE_CID=0x14E8 (card_1048, pw=16435215) 均经 data/card-stats.s 坐实
- **C5 NEW 全 0 命中**: 3 个新常量 (0x00f0ffff, 0x000014c4, 0x000014e8) 在全部 20 个 constants/*.inc 文件中 grep by value = 0 命中, 可新建
- **C5 REUSE 全命中**: 12 个 REUSE 值均在 ewram.inc/card_info.inc/duel_field.inc 找到对应 .equ 定义
- **C13 独立清点**: python 在 L5342..6675 范围独立扫描到 39 个 DWORD_/DAT_/PTR_DAT_ 定义; 与提议 partition 完全一致 (33+2+2+1+1=39), 无遗漏无重复
- **Block1 raw 假阳性说明**: 0x084xxxxx 区的 3 个 raw hit (@0x84318e4/0x841f624/0x8453ce0) 均处于高熵压缩数据区域, 非有效代码指针; 提议虽未列出所有假阳性但结论正确
- **fn 函数结构**: 0x80716fc fn 体实际通过 MOV PC,r0 跳转到 block2 sub-stubs, BHI 分支目标 0x80717e8 = block2 sub-stub 5 公共返回路径; 两块共用栈帧, DISASM 正确; 分类不受影响
