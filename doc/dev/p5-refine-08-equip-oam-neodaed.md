# 函数/数据细化计划 — `asm/08_equip_oam_neodaed.s`

> 阶段目标: 把 `asm/08_equip_oam_neodaed.s` (ROM `0x080643E0 ~ 0x0806E76C`, 装备 OAM sprite 提交 +
> Neo Daedalus 效果 + effect-zone LP/sprite 派发 + field-spell placement display) **逐段地址序细化完成**,
> 全程 byte-identical (`SHA1 9689337d6aac1ce9699ab60aac73fc2cfdccad9b`)。
>
> 这是 refine 第 **9** 个文件 (file 00..07 已全 10 段完成)。方法论 + R1-R9 + 三条硬规则见
> `doc/dev/methodology/refine-loop.md` 与 file 00 doc §一。

---

## 一、细化要求 (checklist)

沿用 file 00..07 doc §一 的 **R1-R9** + **三条硬规则** (严格地址序不回头 / 函数间 ROM_INCBIN 必
carve/disasm 或 §5.1 / 全 ROM 0 引用→§5.1)。**R1-R9 详版**见 `p5-refine-00-system-str-vija.md` §一。
复用资产清单见 `p5-refine-05-equip-eligibility-a.md` §一。

**跨文件踩坑沿用** (file 00..07 沉淀, 务必遵守):
- Ghidra EOL/plate **一律 ASCII**; **段内常残留命名期 CJK mojibake plate, executor 必 grep 段内非 ASCII 逐个整段 ASCII 重写**。
- **⚠ ROM_INCBIN 分类核心 (file 06/07 已确认 N 次)**: 函数间 ROM_INCBIN 块 ref-scan (raw + THUMB|1 穷举 2B-step):
  - **`0x09e4xxxx`/`0x09e3xxxx` = card effect handler dispatch table** (entry 0x18B = `[CID, fn_activate(+1), pad, fn_eligible(+1), pad, pad]`,
    FS 运行时加载); **fn_eligible 块的 CID 在 fn_ptr 地址 -0xc 位置** (别取错下一 entry, file 07 Seg-5 教训); THUMB+1 命中核 fn_ptr-0xc 处 CID
    (python 实读, card-stats.s 坐实) → 真引用 → R4 disasm。
  - **file 08 特征 (OAM/sprite)**: 部分大 ROM_INCBIN 块 (0x374/0x298/0x27c/0x25c/0x19c/0x3d0 等) 可能是 **OAM sprite 属性数据表** (被代码 ldr/表索引引用 → carve 进 rom.s 结构化)
    而非 handler 代码。ref-scan 命中点是 ldr 字面量池/表基址 → carve (label + 结构化 + round-trip); 命中是 THUMB|1 fn-ptr → disasm。逐块据实判。
  - 块内可能多 sub-fn (经 dispatch raw 指针/mov pc,r0/switchD 到达); 仅 raw=0 且 THUMB+1=0 → §5.1。
  详见 memory `feedback-card-effect-handler-table-thumb-ref` + `refine-carve-rom-tables-immediately`。
- **switchD 跳转表 (file 08 含 5: 0x65a44/0x66f02/0x686a2/0x69edc/0x6ac1e)**: jump table 目标裸 THUMB 地址 → R4 disasm 逐 stub
  (file 00 Seg-5c 范式); case stub 可级联 bl ROM_INCBIN helper (file 06 Seg-6/8)。
- **R4 disasm 范式**: clearListing 整 range → setTMode → 逐 stub DisassembleCommand; literal pool createDWord 强制 split。
- **机器码核 (file 07 Seg-8/9 教训, 必做)**: disasm fn 比较+分支指令独立解码 (0x3801=subs#1, 0xd0xx=beq/0xd1xx=bne/0xd8xx=bhi/0xd9xx=bls, 0x4048=EOR≠AND, 0x4002=ands r2,r0,
  ldrh imm5×2 偏移); 函数名运算符/偏移/卡名与机器码一致; **literal pool pc-relative 地址 = (PC&~2)+8+offset python 实算勿差 2 字节**。
- **C5 双向核 (file 07 反复抓误标)**: 标 **new** CID 逐一 grep 0 命中; 标 **reuse** 逐一 grep 确存在; 记证据。
  **C5 偏移放宽** (不同 base `*_OFF` 各建独立); **卡 ID/掩码/位域/阈值非偏移严格去重** (值碰撞必复用, 语义截然不同的两实体 [sprite param vs card_id] 各建独立, 读消费者裁定)。
- **C13 残留 100% 覆盖**: python 精确清点段内全部 DAT_/DWORD_/PTR_ 槽 (别漏 DWORD_); 三表并集 == 全集 (穷举对账); 严防越界。
- **卡牌 ID**: 查 `data/card-stats.s` 坐实 (card record# != slot_id); passcode 逐一 python 核对; 未分配→中性 `cid_<hex>`, 勿臆造 (红线 3)。
- **误名警觉 (file 06/07 高频)**: 函数名/plate 称的卡名/全局与函数体矛盾即误名 (已抓 Otohime/Crimson Ninja/Banisher of Light/Uria/DUEL_STATE_PTR);
  gEquipChainSlotRefs=0x0201bb90 常被误称; 误名走 FUNC_RENAME/CONST_RENAME/plate 订正。
- **C8 stale FUN_**: 穷举 `FUN_[0-9a-f]{8}` 扫段内全部 asm 行 (含跨模块); 每个 FUN_ 地址查现名替换; 落地后 grep == 0。
- **fn-ptr +1 周期性修复**: re-export 后重补 asm/03 (0x37884/0x389dc/0x389f8/0x3aa74) / asm/04 (0x40ab4/0x42638/0x45efc/0x478f0/0x0201d5b4) / asm/05 Seg-8 6 槽 / asm/06/07 各段 fn-ptr。
- **executor 不自撰 review.md** (reviewer 独立职责; file 07 Seg-9 executor 越界自评无效)。

**file 02..07 已建可复用资产** (新建前必 grep): 见 `p5-refine-05-equip-eligibility-a.md` §一 (ewram/duel_field/card_info ~510+ CID/oam_attr/gl_scrollbar/bitops/全局)。

---

## 二、落地工作流 (pipeline)

同 file 00..07 doc §二:
```
备份 .rep → Ghidra 脚本 (RefineF08Seg<N>*.py: equate/label/ref/rename/plate/disasm) + rom.s carve(若有数据表)
→ ghidra-export-range.bat 080000c0 084c7637 → inject_modes.py → split_all_s.py
→ build + byte-identical SHA1 9689337d → (改/建函数名才) ExportFunctionInventory + sync CSV → commit
```
3-agent: executor → reviewer (C1-C13) → fixer (模式A/模式B)。重段按函数边界拆 Seg-Na/Nb (地址序不回头)。

---

## 三、当前进度 (08_equip_oam_neodaed.s)

| Seg | 范围 | ~fn | ~slots | ROM_INCBIN/switch | 状态 | commit |
|-----|------|-----|--------|-------------------|------|--------|
| 1 | 0x643e0..0x6544c | 20 | 87 | 2 (0x6456c/2c, 0x645ee/1e) | ⬜ | — |
| 2 | 0x6544c..0x66448 | 20 | 72 | 3 (0x65d78/3c, 0x65e3c/29c, 0x662a4/68) + switchD_08065a44 | ⬜ | — |
| 3 | 0x66448..0x67160 | 20 | 56 | 1 (0x668c0/1cc) + switchD_08066f02 | ⬜ | — |
| 4 | 0x67160..0x67fa4 | 20 | 74 | 0 | ⬜ | — |
| 5 | 0x67fa4..0x690dc | 20 | 65 | 0 + switchD_080686a2 | ⬜ | — |
| 6 | 0x690dc..0x6a118 | 20 | 90 | 1 (0x696d8/1c) + switchD_08069edc | ⬜ | — |
| 7 | 0x6a118..0x6ab0c | 20 | 47 | 0 | ⬜ | — |
| 8 | 0x6ab0c..0x6cbe8 | 20 | 85 | 11 (大表簇, 见 §五) + switchD_0806ac1e | ⬜ | — |
| 9 | 0x6cbe8..0x6d960 | 20 | 52 | 0 | ⬜ | — |
| 10 | 0x6d960..0x6e76c | 11 | 46 | 4 (0x6dbcc/44, 0x6dc3c/3d0, 0x6e3fa/4e, 0x6e460/1cc) | ⬜ | — |

图例: ✅ 完成 / 🟡 进行中 / ⬜ 未开始。
**22 ROM_INCBIN + 5 switchD** — 逐块 ref-scan 按 §一 分类 (handler-table THUMB+1→disasm / OAM 数据表 ldr-ref→carve / switchD→R4 disasm / 0 引用→§5.1)。
**重段提示**: Seg-8 (85 槽 + **11 ROM_INCBIN 含大表 0x374/0x298/0x27c/0x25c/0x19c/0x110**, OAM sprite 数据表/dispatch 簇) 最重, 必拆 Seg-8a/8b/8c;
Seg-6 (90 槽) / Seg-1 (87 槽) / Seg-10 (4 块含 0x3d0=976B) 次重。

---

## 四、逐段完成记录

(各段落地后由 fixer 追加 4.0N 小节)

---

## 五、批次路线图 (地址序, Seg-1..Seg-10)

> 按 file 08 范围 `[0x080643e0, 0x0806e76c)` (191 named fn, ~674 槽, 22 ROM_INCBIN, 5 switchD)
> 按**函数数**均分 10 段 (~20 fn/段, 边界=函数结束处)。

| Seg | 地址范围 | ~fn | ~slots | 块数 | 主题 (初判) |
|---|---|---|---|---|---|
| Seg-1 | 0x643e0..0x6544c | 20 | 87 | 2 inc | check_equip_slot_eligible_neo_daedalus + Neo Daedalus 资格簇 |
| Seg-2 | 0x6544c..0x66448 | 20 | 72 | 3 inc + 1 sw | write_equip_lp_delta_goblin_thief + LP delta + switchD_08065a44 |
| Seg-3 | 0x66448..0x67160 | 20 | 56 | 1 inc + 1 sw | dispatch_equip_zone_sprite_by_slot_state + switchD_08066f02 |
| Seg-4 | 0x67160..0x67fa4 | 20 | 74 | 0 | dispatch_effect_zone_lp_sprites_by_slot_flags 簇 |
| Seg-5 | 0x67fa4..0x690dc | 20 | 65 | 0 + 1 sw | scan_effect_slots_for_equip_sprite_field6 + switchD_080686a2 |
| Seg-6 | 0x690dc..0x6a118 | 20 | 90 | 1 inc + 1 sw | tick_dragon_summon_display + switchD_08069edc |
| Seg-7 | 0x6a118..0x6ab0c | 20 | 47 | 0 | dispatch_equip_zone_sprite_by_lp_state_with_placement 簇 |
| Seg-8 | 0x6ab0c..0x6cbe8 | 20 | 85 | 11 inc + 1 sw | 重: dispatch_lp_row_or_banisher_sprite + OAM sprite 数据表/dispatch 大簇 (拆 8a/8b/8c) |
| Seg-9 | 0x6cbe8..0x6d960 | 20 | 52 | 0 | tick_equip_target_query_display_seq 簇 |
| Seg-10 | 0x6d960..0x6e76c | 11 | 46 | 4 inc | dispatch_field_spell_placement_display (文件末) |

执行约定同 file 00..07: 每段走 §二 pipeline; 地址序不回头; 每完成一段更新 §三 + §四 + refine-progress。

### 5.1 未引用数据登记表 (规则 3)

| 地址 | 大小 | 所在 Seg | 初判内容 | 状态 |
|---|---|---|---|---|
| (各段 ref-scan 0 引用块由 executor/fixer 追加) | | | | |

---

## 六、相关文档
- `doc/dev/methodology/refine-loop.md` (方法论)
- `doc/dev/p5-refine-00-system-str-vija.md` (file 00 完整记录 + §一 R1-R9 详版)
- `doc/dev/p5-refine-07-equip-effect-chain.md` (file 07: handler-table disasm 大批量 / CID@fn_ptr-0xc / 机器码核 / 误名订正 / CONST_RENAME)
- `doc/dev/refine-progress.md` (25 文件跨文件总进度)
