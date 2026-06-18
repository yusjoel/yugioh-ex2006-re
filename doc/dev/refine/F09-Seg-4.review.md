# Refine Review: F09-Seg-4a  [0x080719fc..0x08072404)

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段序号与路线图一致 | PASS | Seg-4 在 Seg-3 (commit c1c490d) 之后，范围 [0x719fc..0x72404) 与 §五 roadmap 一致 |
| C2 | 所有 ROM_INCBIN/`.byte` 块有归宿 | PASS | B1-B4 全部判 DISASM，无静默保留 |
| C3 | §5.1 块 0 引用 | PASS (N/A) | 无 §5.1 块；所有 4 块有真实引用 |
| C4 | EQ value == ROM 4 字节小端 | PASS | python 实读 38 个 EQ 槽，全部匹配 |
| C5 | 新建常量无现有复用；REUSE 确存在 | PASS | 5 个 NEW 常量在 constants/*.inc 全 0 命中；16 个 REUSE 全部确认存在 |
| C6 | 槽名 `^[a-z][a-z0-9_]+$`，无碰撞 | PASS | 22 个 label 全符合规则，无重复 |
| C7 | carve/全局槽有 USER-label+DATA-ref 计划 | PASS (N/A) | carve=0；dispatch 表已在 asm 作 `.word`，无 carve 需要 |
| C8 | plate 无残留旧 `FUN_/DAT_/DWORD_` | PASS | grep `FUN_[0-9a-f]{8}` 在 L6770..L8440 段内：0 命中 |
| C9 | plate/EOL 文本纯 ASCII | PASS | RENAME EOL 两条均纯 ASCII；proposal 未新增 PLATE |
| C10 | 指针表 `+1` (THUMB)，`.word fn+1` == ROM raw | PASS | B1: FS[0x9e43c88]=0x08071a95=fn+1 OK；B3: FS[0x9e40f58]=0x08071f59=fn+1 OK；CID 均在 fn_ptr-0x4（非 -0xc，但 proposal 给出的地址正确） |
| C11 | 函数名/全局无误名 | PASS | FUNC_RENAME=0，无矛盾信号 |
| C12 | 关键槽语义有 file:line + 置信度，无零容忍词 | NEEDS_FIX | 见下 #1 |
| C13 | 段内全部残留自动名槽被覆盖 | PASS | 独立 grep：28 DWORD_ + 12 DAT_ = 40，全在 [0x719fc..0x72404)；38 EQ + 2 RENAME = 40，完整覆盖 |

---

## 状态: NEEDS_FIX (1 item)

---

## 修改清单

### #1 — C12 — YAMATA_DRAGON_CID (DAT_08071e0c=0x1501) 消费者证据写错 callee

**问题描述:**

proposal §8 consumer evidence 写道：
```
DAT_08071e0c=0x1501 | asm/09 L7176: cmp r1,r0 -> beq LAB_08071e54 -> enqueue_spirit_zone_sprite_with_lp_check
                     | YAMATA_DRAGON_CID (also 0x1502=Great Long Nose shares same callee)
```

但实际 BST 代码（reviewer 独立从 asm 追踪）：
- `0x1501 Yamata Dragon` -> `LAB_08071e4a` -> `bl dispatch_equip_draw_counter_sprite_tick`
- `0x1502 Great Long Nose` -> `LAB_08071e54` -> `bl enqueue_spirit_zone_sprite_with_lp_check`

两者 callee **不同**，proposal 错写为"同 callee"。完整 BST 真实映射：

| card_id | 卡名 | branch target | callee |
|---------|------|---------------|--------|
| 0x14fd | Maharaghi | LAB_08071e40 | enqueue_spirit_monster_zone_sprite_otohime |
| 0x14ff | Yata-Garasu | LAB_08071e54 | enqueue_spirit_zone_sprite_with_lp_check |
| 0x1501 | Yamata Dragon | LAB_08071e4a | dispatch_equip_draw_counter_sprite_tick |
| 0x1502 | Great Long Nose | LAB_08071e54 | enqueue_spirit_zone_sprite_with_lp_check |
| 0x1503 | Otohime | LAB_08071e5e | apply_equip_activation_with_aqua_spirit_guard |
| 0x1504 | Hino-Kagu-Tsuchi | LAB_08071e68 | enqueue_spirit_zone_sprite_type11 |
| 0x1506 | Fushi No Tori | LAB_08071e72 | submit_equip_lp_indicators_with_bar |
| 0x1526 | Dark Dust Spirit | LAB_08071e7c | submit_equip_zone_bitmap_pair_update |
| 0x1694 | Tsukuyomi | LAB_08071e86 | dispatch_equip_slot_sprite_if_zone_entry_active |

**附带注意 (不阻塞但需 fixer 知晓):** `dispatch_spirit_monster_zone_sprite_by_card_id` 函数的 pre-existing plate 注释（asm L7081）也存在 0x14ff 与 0x1501 对应 callee 对调的错误。该 plate 系命名期已存在（不是 Seg-4a proposal 新增的 PLATE action），但后续 Seg 细化或 FUNC_RENAME 时应一并订正。

**要求改动 (仅改 proposal doc，不动 Ghidra/asm/build):**

在 `doc/dev/refine/F09-Seg-4.proposal.md` §8 中将 `DAT_08071e0c=0x1501` 的 consumer evidence 更正为：

```
| DAT_08071e0c=0x1501 | asm/09 L7167: ldr r0, DAT_08071e0c; L7168: cmp r1,r0; L7169: beq LAB_08071e4a -> bl dispatch_equip_draw_counter_sprite_tick | YAMATA_DRAGON_CID = 0x1501; 0x1502 Great Long Nose goes to LAB_08071e54 (different callee: enqueue_spirit_zone_sprite_with_lp_check) | high |
```

---

## 审核备注 (informational, PASS 项)

**NEW 常量数量 "2 vs 5" 不一致已解决:**

- EQ_SLOTS 表中真正新建常量的槽：2 个（YAMATA_DRAGON_CID / DARK_DUST_SPIRIT_CID，均是 DWORD/DAT literal-pool 槽）
- card_info.inc 实际新增：5 个（额外 3 个：FENGSHENG_MIRROR_CID 用于 fn_eligible 命名，YATA_GARASU_CID / HINO_KAGU_TSUCHI_CID 出现于 BST 相对算术，非 literal-pool 槽）
- 两个数字均正确；不一致来自语境不同（"槽级别新建"vs"inc 文件新增条目"）。无误

**ref-scan 独立复核:**

- B1 raw=0 THUMB+1=1 (0x9e43c88)，CID 在 fn_ptr-0x4=0x9e43c84=0x14fb (Fiber Jar). PASS
- B2 raw=7 (6 来自 dispatch table 0x71abc..0x71ad0，1 来自 0x81343e2 非对齐/FS 数据可忽略)，THUMB+1=1 (同一非对齐地址可忽略). PASS
- B3 raw=0 THUMB+1=1 (0x9e40f58)，CID 在 fn_ptr-0x4=0x9e40f54=0x1509 (Fengsheng Mirror). PASS
- B4 raw=34 (32 来自 dispatch table 0x71f88..0x72000 + 2 FS 压缩数据巧合，含 3 个非 table 的 raw ref 均在 FS/压缩区可忽略)，THUMB+1=0. PASS

**sub-stub 条目数轻微偏差 (不影响正确性):**

- B2：proposal 列 7 个入口点，但 dispatch table 只引用 6 个真实入口；0x08071b24 是 field_spell_sub_1b02 尾部的无条件跳转 (e055)，不是独立 dispatch 入口。DisassembleCommand 在已反汇编范围内调用为 no-op，不影响结果。
- B4：proposal 列 11 个入口点，dispatch table 仅 6 个真实入口；其余 5 个 (0x8072036/204a/204e/207e/2082) 是 stub 内部分支目标，无 dispatch ref。同样 harmless。

**CID 结构说明:**

本段两个 FS handler table 的 entry 结构实测为 `[..., CID, fn_eligible+1, ...]`，CID 在 fn_ptr-0x4（非 methodology 文档描述的 -0xc）。proposal 给出的 CID 地址 (0x9e43c84, 0x9e40f54) 是正确的实测值，methodology 文档的 `-0xc` 说明适用于其他 table 类型。

---

## Reviewer Verdict: F09-Seg-4a = NEEDS_FIX(1 items)
