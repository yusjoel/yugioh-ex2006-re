# 函数/数据细化计划 -- `asm/10_equip_effect_dispatch.s`

> 阶段目标: 把 `asm/10_equip_effect_dispatch.s` (ROM `0x08079e60 ~ 0x080850d8`, neo daedalus
> zone OAM + 装备判据/效果按类型派发) **逐段地址序细化完成**,
> 全程 byte-identical (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **11** 个文件 (file 00..09 已全 10 段完成)。方法论 + R1-R9 + 三条硬规则见
> `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

---

## 一、细化要求 (checklist)

沿用 file 00..09 doc §一 的 **R1-R9** + **三条硬规则** (严格地址序不回头 / 函数间 ROM_INCBIN 必
carve/disasm 或 §5.1 / 全 ROM 0 引用->§5.1)。**R1-R9 详版**见 `p5-refine-00-system-str-vija.md` §一。
复用资产清单见 `p5-refine-05-equip-eligibility-a.md` §一。

**跨文件踩坑沿用** (file 00..09 沉淀, 务必遵守):
- Ghidra EOL/plate **一律 ASCII**; **段内常残留命名期 CJK mojibake plate, executor 必 grep 段内非 ASCII 逐个整段 ASCII 重写**。
- **ROM_INCBIN 分类核心 (file 06..09 已确认多次)**: 函数间 ROM_INCBIN 块 ref-scan (raw + THUMB|1 穷举 2B-step):
  - **`0x09e4xxxx`/`0x09e3xxxx` = card effect handler dispatch table** (entry 0x18B = `[CID, fn_activate(+1), pad, fn_eligible(+1), pad, pad]`,
    FS 运行时加载); **fn_eligible 块的 CID 在 fn_ptr 地址 -0xc 位置** (别取错下一 entry); THUMB+1 命中 -> R4 disasm。
  - **file 10 特征**: 39 ROM_INCBIN 块 + 6 switchD。大量块属于 **跳转表** (raw-ref -> carve 进 rom.s) 或 **fn_eligible THUMB stubs** (THUMB+1 ref -> R4 disasm)。ref-scan 必做, 逐块据实判定。
  - 块内可能含多 sub-fn (经 dispatch raw 指针 / MOV PC,r0 / switchD 到达); raw=0 且 THUMB+1=0 -> §5.1。
- **switchD 跳转表 (file 10 含 6: 0x7d126/0xed22/0xee92/0xfe22/0x806cc/0x81e2c)**: 目标裸 THUMB 地址 -> R4 disasm 逐 stub (file 00 Seg-5c 范式); case stub 可级联 bl ROM_INCBIN helper。注意: switchD 地址属某段, 其目标块可能落在本段内也可能属下一段 -- 逐段 ref-scan 确认。
- **R4 disasm 范式**: clearListing 整 range -> setTMode -> 逐 stub DisassembleCommand; literal pool createDWord 强制 split。
- **机器码核 (必做)**: disasm fn 比较+分支指令独立解码; 函数名运算符/偏移/卡名与机器码一致; **literal pool pc-relative 地址 = (PC&~2)+8+offset python 实算勿差 2 字节**。
- **C5 双向核**: 标 new CID 逐一 grep 0 命中; 标 reuse 逐一 grep 确存在; 记证据。
- **C13 残留 100% 覆盖**: python 精确清点段内全部 DAT_/DWORD_/PTR_ 槽 (别漏 DWORD_); 三表并集 == 全集 (穷举对账); 严防越界。
- **卡牌 ID**: 查 `data/card-stats.s` 坐实; 未分配->中性 `cid_<hex>`, 勿臆造。
- **误名警觉**: 函数名/plate 称的卡名/全局与函数体矛盾即误名信号; 走 FUNC_RENAME/plate 订正。
- **C8 stale FUN_**: 穷举 `FUN_[0-9a-f]{8}` 扫段内全部 asm 行 (含跨模块); 每个 FUN_ 地址查现名替换; 落地后 grep == 0。
- **fn-ptr +1 周期性修复**: re-export 后重补 asm/03 (0x37884/0x389dc/0x389f8/0x3aa74) / asm/04 (0x40ab4/0x42638/0x45efc/0x478f0/0x0201d5b4) / asm/05 Seg-8 6 槽 / asm/06/07/08/09 各段 fn-ptr。
- **executor 不自撰 review.md** (reviewer 独立职责)。
- **disasm 必须完全消除每个 sub-stub** (file 09 教训: 逐 stub per-4B DisassembleCommand; 重跑前先 clearListing 整 range 再 setTMode; 否则 ContextChangeException)。

**file 02..09 已建可复用资产** (新建前必 grep): 见 `p5-refine-05-equip-eligibility-a.md` §一 + file 06/07/08/09 新增 (card_info.inc ~600+ CID / ewram.inc / duel_field.inc / oam_attr.inc / gfx_resource.inc / g2d_tags.inc / gl_scrollbar.inc / gl_blend.inc 等)。

---

## 二、落地工作流 (pipeline)

同 file 00..09 doc §二:
```
备份 .rep -> Ghidra 脚本 (RefineF10Seg<N>*.py: equate/label/ref/rename/plate/disasm) + rom.s carve(若有数据表)
-> ghidra-export-range.bat 080000c0 084c7637 -> inject_modes.py -> split_all_s.py
-> build + byte-identical SHA1 9689337d -> (改/建函数名才) ExportFunctionInventory + sync CSV -> commit
```
3-agent: executor -> reviewer (C1-C13) -> fixer (模式A改proposal / 模式B落地)。重段按函数边界拆 Seg-Na/Nb (地址序不回头)。

---

## 三、当前进度 (10_equip_effect_dispatch.s)

| Seg | 范围 | ~fn | ~slots | ROM_INCBIN / switchD | 状态 | commit |
|-----|------|-----|--------|----------------------|------|--------|
| 1  | 0x79e60..0x7ae84 | 19 | 61  | 8 inc (0x79fac/30, 0xa00c/e8, 0xa138/28, 0xa178/14c, 0xa3b8/38, 0xa464/11c, 0xa688/44, 0xa71c/f8) | ✅ | aa53bf0 |
| 2  | 0x7ae84..0x7be2c | 18 | 47  | 8 inc (0xaf66/3a, 0xafb8/110, 0xb4d4/2c, 0xb574/144, 0xb7dc/28, 0xb878/e0, 0xb9f4/28, 0xba30/100) | ⬜ | |
| 3  | 0x7be2c..0x7cd68 | 19 | 68  | 2 inc (0xc87a/3e, 0xc92c/158) | ⬜ | |
| 4  | 0x7cd68..0x7db20 | 19 | 53  | 2 inc (0xd7e8/2c, 0xd830/fc) + 1 sw (0xd126) | ⬜ | |
| 5  | 0x7db20..0x7f730 | 19 | 64  | 8 inc (0xdd68/30, 0xddac/16c, 0xdf90/2bc, 0xe398/2c, 0xe438/16c, 0xe5d4/63c, 0xf280/3c, 0xf330/128) + 2 sw (0xed22, 0xee92) | ⬜ | |
| 6  | 0x7f730..0x80ba0 | 18 | 123 | 0 inc + 2 sw (0xfe22, 0x806cc) | ⬜ | |
| 7  | 0x80ba0..0x82290 | 19 | 152 | 2 inc (0x82046/fa, 0x82158/138) + 1 sw (0x81e2c) | ⬜ | |
| 8  | 0x82290..0x83450 | 19 | 113 | 2 inc (0x827d4/d8, 0x828c4/f8) | ⬜ | |
| 9  | 0x83450..0x84318 | 18 | 89  | 2 inc (0x8420e/26, 0x8424c/cc) | ⬜ | |
| 10 | 0x84318..0x850d8 | 19 | 55  | 5 inc (0x8474e/2a, 0x84790/164, 0x84918/180, 0x84af2/2a, 0x84b34/10c) | ⬜ | |

**总计**: 187 fn (全部已命名) / 825 DWORD_/DAT_ 槽 / 39 ROM_INCBIN + 6 switchD。
**重段提示**: Seg-7 (152 槽) 和 Seg-6 (123 槽) 最重, 含大型 switchD 派发族; Seg-8 (113 槽) 次重。
Seg-5 含最多 ROM_INCBIN (8 inc + 2 switchD) 且有 0xe5d4/0x63c 超大块 (1596 B), 须仔细 ref-scan 分类。

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。

---

## 四、逐段完成记录

### 4.01 Seg-1 完成记录

- **范围**: [0x08079e60, 0x0807ae84), 19 fn, 61 slots, 8 ROM_INCBIN
- **落地日期**: 2026-06-21
- **SHA1**: 9689337d6aac1ce9699ab60aac73fc2cfdccad9b (byte-identical)
- **EQ_SLOTS**: 47 (43 REUSE + 4 NEW: NEO_DAEDALUS_OAM_SPRITE_BASE/CARD_DISPLAY_OP_ID_137/EQUIP_PAIRED_SLOT_PRED/MAGICIANS_CIRCLE_CID + zone_query_hand_tag_12a1)
- **RENAME_SLOTS**: 9 (gP1LifePoints already-symbolic slots)
- **REF_SLOTS**: 5 (ROM_INCBIN entry bases + dispatch table label)
- **R4 disasm**: 8 blocks (BLK1/3/5/7 = fn_eligible THUMB stubs; BLK2/4/6/8 = dispatch sub-stubs)
  - BLK1 fn_eligible Abyssal Designator (CID=0x17f4); BLK3 Big Wave Small Wave (0x17f9)
  - BLK5 shared CID 0x1803 (unassigned) + equip_cid_15de (0x15de)
  - BLK7 Magician's Circle (MAGICIANS_CIRCLE_CID=0x1818)
  - Pool fix pass: 21 additional createDWord calls (sub-stub inline literal pools)
- **NEW constants**: NEO_DAEDALUS_OAM_SPRITE_BASE=0x180d (equip_lp_delta.inc); CARD_DISPLAY_OP_ID_137=0x137, EQUIP_PAIRED_SLOT_PRED=0x181e, zone_query_hand_tag_12a1=0x12a1 (duel_field.inc); MAGICIANS_CIRCLE_CID=0x1818 (card_info.inc)
- **carve**: 0
- **§5.1**: 0
- **残留**: 0 ROM_INCBIN / 0 DAT_/DWORD_ in [0x79e60, 0x7ae84)
- **Ghidra scripts**: RefineF10Seg1Slots.py, DisassembleF10Seg1Blocks.py, RefineF10Seg1PoolFix.py
- **commit**: aa53bf0

---

## 五、段路线图 (Seg-1..10 细节)

按照三条硬规则 (地址序 / 函数间必处理 / 0引用->§5.1) 逐段执行。

### Seg-1 [0x08079e60, 0x0807ae84) -- 19 fn, ~61 slots
- 8 ROM_INCBIN 块 (均在函数间或函数体内): 须 ref-scan 逐块分类
  - 0x08079fac/0x30, 0x0807a00c/0xe8, 0x0807a138/0x28, 0x0807a178/0x14c
  - 0x0807a3b8/0x38, 0x0807a464/0x11c, 0x0807a688/0x44, 0x0807a71c/0xf8
- **注意**: 0xa178/0x14c (332B) 和 0xa464/0x11c (284B) 较大; 0xa00c/0xe8 (232B) 次之
- 旧覆盖: 无 (新文件)

### Seg-2 [0x0807ae84, 0x0807be2c) -- 18 fn, ~47 slots
- 8 ROM_INCBIN 块 (密集):
  - 0x0807af66/0x3a, 0x0807afb8/0x110, 0x0807b4d4/0x2c, 0x0807b574/0x144
  - 0x0807b7dc/0x28, 0x0807b878/0xe0, 0x0807b9f4/0x28, 0x0807ba30/0x100
- **注意**: 0xafb8/0x110 (272B) + 0xb574/0x144 (324B) + 0xba30/0x100 (256B) 大块; 同 Seg-1 须 ref-scan
- 旧覆盖: 无

### Seg-3 [0x0807be2c, 0x0807cd68) -- 19 fn, ~68 slots
- 2 ROM_INCBIN 块:
  - 0x0807c87a/0x3e (62B), 0x0807c92c/0x158 (344B)
- **注意**: 0xc92c/0x158 是本段最大块 (344B)
- 旧覆盖: 无

### Seg-4 [0x0807cd68, 0x0807db20) -- 19 fn, ~53 slots
- 2 ROM_INCBIN + 1 switchD:
  - 0x0807d7e8/0x2c (44B), 0x0807d830/0xfc (252B)
  - switchD_0807d126 (属函数 tick_equip_activation_display_state_machine@0x0807d104; 其代码 + switchD 均在本段)
- **注意**: switchD_0807d126 的目标块可能在本段内亦可能越界至 Seg-5; 需在 disasm 前先 ref-scan 逐目标确认
- 旧覆盖: 无

### Seg-5 [0x0807db20, 0x0807f730) -- 19 fn, ~64 slots
- **最多 ROM_INCBIN** (8 inc + 2 switchD):
  - 0x0807dd68/0x30, 0x0807ddac/0x16c (364B), 0x0807df90/0x2bc (**700B! 最大**), 0x0807e398/0x2c
  - 0x0807e438/0x16c (364B), 0x0807e5d4/0x63c (**1596B! 超大**), 0x0807f280/0x3c, 0x0807f330/0x128 (296B)
  - switchD_0807ed22, switchD_0807ee92
- **注意**: 0xe5d4/0x63c (1596B) 是全文件最大 ROM_INCBIN; 须精细 ref-scan (raw + THUMB+1 每 2B step 穷举); 压缩资产偶合要剔除
- 旧覆盖: 无

### Seg-6 [0x0807f730, 0x08080ba0) -- 18 fn, ~123 slots
- 0 ROM_INCBIN + 2 switchD:
  - switchD_0807fe22, switchD_080806cc
- **注意**: 123 DAT_/DWORD_ 槽密集; switchD 目标块须 ref-scan 确认是否在本段内
- 旧覆盖: 无

### Seg-7 [0x08080ba0, 0x08082290) -- 19 fn, ~152 slots
- 2 ROM_INCBIN + 1 switchD:
  - 0x08082046/0xfa (250B), 0x08082158/0x138 (312B)
  - switchD_08081e2c
- **注意**: 152 槽是全文件最重; 0x82158/0x138 较大; switchD_08081e2c 目标可能含 fn_eligible stubs
- 旧覆盖: 无

### Seg-8 [0x08082290, 0x08083450) -- 19 fn, ~113 slots
- 2 ROM_INCBIN:
  - 0x080827d4/0xd8 (216B), 0x080828c4/0xf8 (248B)
- 旧覆盖: 无

### Seg-9 [0x08083450, 0x08084318) -- 18 fn, ~89 slots
- 2 ROM_INCBIN:
  - 0x0808420e/0x26 (38B), 0x0808424c/0xcc (204B)
- 旧覆盖: 无

### Seg-10 [0x08084318, 0x080850d8) -- 19 fn, ~55 slots
- 5 ROM_INCBIN (fn-eligible 特征):
  - 0x0808474e/0x2a (42B), 0x08084790/0x164 (356B), 0x08084918/0x180 (384B)
  - 0x08084af2/0x2a (42B), 0x08084b34/0x10c (268B)
- **注意**: 5 块集中在末尾 [0x8474e..0x84c40); 模式类似 file 09 Seg-10 fn_eligible stubs; THUMB+1 ref-scan 判定
- 旧覆盖: 无

---

## §5.1 零引用孤儿块登记

(待各段 ref-scan 确认后在此登记 0-引用块)

| 块地址 | 大小 | ref-scan raw | ref-scan THUMB+1 | 判定 | 备注 |
|--------|------|-------------|-----------------|------|------|
| (空)   |      |             |                 |      |      |

---

## 六、相关文档

| 文档 | 说明 |
|------|------|
| `doc/dev/methodology/refine-loop.md` | 完整方法论 R1-R9 + 三条硬规则 |
| `doc/dev/p5-refine-00-system-str-vija.md` | R1-R9 详版 + §一 全文 |
| `doc/dev/p5-refine-05-equip-eligibility-a.md` | 复用资产完整清单 |
| `doc/dev/p5-refine-09-equip-lp-display.md` | file 09 全记录 (fn_eligible stub 分类范式) |
| `doc/dev/refine-progress.md` | 25 文件总进度 |
| `doc/dev/refine/` | 各段 proposal.md + review.md |
| `asm/10_equip_effect_dispatch.s` | 目标文件 (19983 行) |
