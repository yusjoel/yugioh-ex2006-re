# Refine Review: F06-Seg-2

## 段信息

- 段范围: `0x080541cc .. 0x08054ba0` (23 fn, 含 disasm 后新增 1)
- 模块: `asm/06_equip_eligibility_b.s`
- Proposal: `doc/dev/refine/F06-Seg-2.proposal.md`
- ROM: `roms/2343.gba` (base 0x08000000)
- 活动 doc: `doc/dev/p5-refine-06-equip-eligibility-b.md` §五 Seg-2
- Reviewer: 独立复核 (自主 ref-scan + python 字节核对)
- iter: 2 (iter-1 NEEDS_FIX C2+C3 已由 fixer mode A 改判 disasm)

---

## 核验矩阵 (C1-C13) — iter-2

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致，未跳号/回头 | PASS | roadmap Seg-2 = 0x541cc..0x54ba0，与 proposal 一致；Seg-1 已完成 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块都有归宿 | PASS | 唯一块 0x08054614/0x48 → disasm 计划已具体给出；§5.1 清零 |
| C3 Rule3 | §5.1 块确 0 引用 | PASS | 独立重跑 ref-scan: ROM[0x09e421d4]=0x08054615 (THUMB+1) 命中，fn-ptr 真实，不入 §5.1；改判 disasm 正确 |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | PASS | python 核对全 52 槽: STRIDE×21=0x868 ✓, gDuelFieldSlots×22=0x0201c510 ✓, scrollbar×4 ✓, 5 new 全 MATCH |
| C5 R1 复用 | 新建常量前确无现有可复用 | PASS | 4 个复用常量均在对应 .inc 中确认存在；5 个新建常量 grep constants/*.inc 无同名 |
| C6 R2 名 | 槽名格式合法，无碰撞 | PASS | 新函数名 check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight 通过 `^[a-z][a-z0-9_]+$`；槽名 *_stride/*_slots 同格式；asm/06 无同名碰撞 |
| C7 R3 接通 | carve/全局槽 USER-label + DATA-ref | N/A | REF_SLOTS=0，carve=0 |
| C8 R5 现名 | plate 引用全用现名，无残留旧 FUN_ | PASS | 唯一残留 FUN_0809077c → invoke_count_zone_pair_hits_full_range (0x0809077c,) 计划正确；asm/11_effect_slot_puzzletext.s:12026 确认现名 |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | 新函数 plate 纯 ASCII；FUN_ 替换前后文本均 ASCII；proposal 中无 CJK |
| C10 carve | carve=0, N/A | N/A | — |
| C11 误名 | 函数名无矛盾 | PASS | 22 已命名 + 1 新命名，均 check_equip_slot_eligible_* 谓词语义一致 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | PASS | 5 new: TRICKYS_MAGIC_4/GILFORD/SERIAL_SPELL CID 均 data/card-stats.s line 坐实 high-conf; THE_TRICKY_TARGET_SLOT_PATTERN python (0x1806<<19)==0xc0300000 验证 high-conf; EQUIP_FLAG_TARGET_ICID_TABLE_OFF med-conf 结构推断标注 |
| C13 残留 | 段内所有残留自动名槽被覆盖，无遗漏 | PASS | 当前 asm Seg-2 (lines 1494..2960): 50 个 DAT_/DWORD_ 定义；disasm 后新增 2 个 literal pool 槽 → 52 个；proposal EQ 21+22+4+5=52 全覆盖，自洽 |

**总判: PASS**

---

## 状态: PASS

---

## iter-2 关键复核结果

### C3 ref-scan (独立重跑)

- ROM[0x09e421d4] = 0x08054615: MATCH (THUMB+1 指向 0x08054614)
- 周边结构: CID 0x000017b4 (Desert Sunlight) @ 0x09e421cc, fn-ptr1 0x08079595 @ 0x09e421d0
- 结论: 真实 card effect handler dispatch table 条目，non-zero 引用，disasm 改判正确

### C4 块边界核对 (python)

- ROM[0x0805465a] hword = 0x4770 = bx lr: MATCH，块边界正确
- ROM[0x0805465c] hword = 0xb530 = push {r4,r5,lr}: 下一函数 check_equip_slot_type_and_score_match 有效 THUMB prologue
- ROM[0x08054650] = 0x00000868 (PLAYER_BLOCK_STRIDE): MATCH
- ROM[0x08054654] = 0x0201c510 (gDuelFieldSlots): MATCH
- ROM[0x08054658] hword = 0x2001 (movs r0,#1): MATCH
- 块结构: 60B 代码 (0x14..0x4f) + 8B literal pool (0x50..0x57) + 4B epilogue (0x58..0x5b) = 72B = 0x48 自洽

### C13 统计自洽

- 现有 Seg-2 auto-name defs: 46 DAT_ + 4 DWORD_ = 50
- disasm 后新增 literal pool 标签: 2 (_stride + _slots)
- 后 EQ 总数: 50 + 2 = 52 = proposal "47 reuse + 5 new = 52"

---

## 附: iter-1 修改清单 (已由 fixer mode A 完成)

- #1 C2/C3: ROM_INCBIN 0x08054614/0x48 改判 disasm，函数命名 check_equip_slot_eligible_by_side_and_zone_for_desert_sunlight，新增 EQ×2 (PLAYER_BLOCK_STRIDE + gDuelFieldSlots)，§5.1 清零
