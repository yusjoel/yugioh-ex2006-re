# Refine Review: F07-Seg-7

段范围: ROM `0x080613b4..0x08061eb4`, `asm/07_equip_effect_chain.s` L13519..L15283

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | PASS | p5-refine-07 §五 Seg-7: 0x613b4..0x61eb4 与 proposal 精确一致; 未跳号/回头 |
| C2 Rule2 | 所有 ROM_INCBIN 块有归宿 | PASS | 段内 1 块 (0x61c66/0x2a), proposal 归 R4 disasm; 独立计数 ROM_INCBIN=1, 处理数=1 |
| C3 Rule3 | §5.1 块确 0 引用 | PASS | 段内无 §5.1 块; 唯一 ROM_INCBIN 确认有真 THUMB+1 引用 (见下 ref-scan) |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | PASS | 独立 python 核验 25 个代表槽 (含全部 NEW 项) + 18 REF 槽 + 6 PTR 槽, 全部一致 |
| C5 R1 复用 | 新建 constants 前无现有可复用 | PASS | 7 新 CID 均 grep 0 命中; SANCTUARY_IN_THE_SKY_CID 仅以注释形式出现于 SANCTUARY_CID_SHIFTED 定义行, 非独立 .equ, 正确新建; LP_GAP_THRESHOLD_7000 grep 0 命中 |
| C6 R2 名 | 槽名格式 + 无碰撞 | PASS | 65 个 slot labels 全匹配 `^[a-z][a-z0-9_]+$`; 无重复; fn-ptr 槽用地址后缀区分 |
| C7 R3 接通 | REF 槽有 USER-label + DATA-ref | PASS | 18 gP1LP REF + 1 gP1ZoneHandCount DAT-REF; gP1LifePoints/gP1ZoneHandCount/gP1FieldArrayCBase 均在 ewram.inc 有定义 |
| C8 R5 现名 | 段内无残留 stale `FUN_[0-9a-f]{8}` | PASS | grep 段范围 L13519..L15283 = 0 命中 |
| C9 ASCII | 段内 plate/EOL 规划文本纯 ASCII | PASS | 段内实测 20 行非 ASCII (全属 7 个函数的 CJK plate); 逐一对照 proposal 的 7 个 CJK 全改写 (plate 1/3/4/5/7/8/9) 均已收录; proposal 中 plate/EOL 正文无非 ASCII 字符 (python encode 验证) |
| C10 carve | fn-ptr `+1` 正确 | PASS | DWORD_08061d74=0x080507ad: ROM 0x080507ac 机器码 b570 (push, THUMB fn 入口) + 1 = 0x080507ad; DWORD_08061eb0=0x08051e95: ROM 0x08051e94 机器码 b570 + 1 = 0x08051e95; disasm block fn_eligible+1=0x08061c69: ROM 0x08061c68 机器码 4a06 (ldr r2,[pc,#24], THUMB 入口) |
| C11 误名 | FUNC_RENAME 正确标记 | PASS | check_zera_ritual_absent_from_field @0x08061d40 加载 DAT_08061d50=0x1332; ROM 独立验证 0x08061d50: 值 0x00001332; card-stats.s L9492: slot=0x1332 pw=61528025 = Banisher of the Light; L7113: slot=0x1245 pw=81756897 = Zera Ritual; 新名 check_banisher_of_light_absent_from_field 符合 R1 |
| C12 R6 | 关键槽语义有 file:line + 置信度 | PASS | 9 个关键槽均标 high confidence + 证据 (card-stats.s 行号 / ewram.inc 行号 / ROM 地址 / handler table python 实读) |
| C13 残留 | 段内全部残留自动名槽覆盖 | PASS | asm grep: 14 DAT_ + 43 DWORD_ + 6 PTR_ = 63 pre-existing; EQ(44) + REF(18) + RENAME(2) + 新增 disasm(2) = 全覆盖; 无越界; 无漏项 |

## 独立 ref-scan 结果

**块 0x08061c66/0x2a** (block start 0x08061c66, fn entry 0x08061c68):
- raw=0 命中
- THUMB+1 穷举: 0x08061c69 命中 1 处 @ file_offset 0x01e42058 (ROM 0x09e42058)
- context: `e1 56 06 08 71 3c 05 08 69 1c 06 08 c5 6b 05 08`
  - +0x0c: 0x08061c69 = fn_eligible+1
  - +0x00: 0x080656e1 = fn_activate+1 (在 file 07 范围内)
  - handler table base: 0x09e4204c; +0=0x1776 (CID), +4=fn_activate+1, +8=pad, +c=fn_eligible+1, +10=pad, +14=0 (terminator)
- 0x08061c73 在 file 0x00d54793 (ROM 0x08d54793) 命中 1 处: 地址不在 0x09e4xxxx 范围, 上下文字节 `10 93 41 10 c1 91 61 d7 73 1c 06 08` 为压缩数据, 非 handler table 结构 -> 确为误报
- 判定: R4 disasm (1 真引用), §5.1=0

## disasm 机器码解读核验

fn entry 0x08061c68, 指令序列:
- `4a06`: ldr r2,[pc,#24] -> gP1LifePoints (0x0201c4e0) at 0x08061c84
- `7880`: ldrb r0,[r0,#2] -> player_id byte from slot
- `07c0/0fc0`: lsls r0,#31 / lsrs r0,#31 -> bit0 isolation
- `4905`: ldr r1,[pc,#20] -> PLAYER_BLOCK_STRIDE (0x868) at 0x08061c88
- `4348`: muls r0,r1 -> player_offset
- `3210`: adds r2,#0x10 -> gP1LP+LP_SLOT_ACTIVE_OFF
- `1880/6800`: adds r0,r0,r2; ldr r0,[r0] -> LP status word
- `2800/d106`: cmp r0,#0; bne -> 0x08061c8c (movs r0,#2 / bx lr) if nonzero -> return 2
- zero path: `2000/e005` -> bx lr -> return 0
- Proposal 描述"nonzero->return 2, zero->return 0"与机器码完全一致

## FUNC_RENAME 独立验证

`check_zera_ritual_absent_from_field` @0x08061d40:
- ROM 0x08061d40: `b500` (push {lr}), `4803` (ldr r0,[pc,#12]), `f7d0 fd2a` (bl count_field_copies_of_card)
- 0x08061d50 (DAT_08061d50): ROM 读值 = 0x00001332
- card-stats.s L9492: slot=0x1332 pw=61528025 = Banisher of the Light
- card-stats.s L7113: slot=0x1245 pw=81756897 = Zera Ritual (命名期板 plate 误用此 passcode 标注 0x1332)
- 新名 `check_banisher_of_light_absent_from_field` 语义准确

## gEquipChainSlotRefs (0x0201bb90) 独立验证

5 个 DWORD 槽 (0x08061578/080617e8/080619e0/08061cbc + 1 in disasm 无 DWORD 标签):
- ROM 独立读值全部 = 0x0201bb90
- ewram.inc:315: `.equ gEquipChainSlotRefs, 0x0201bb90`
- 原 plate 称 `gDuelEffectCtx` 为误名, proposal 正确规划全部订正

## CJK plate 完整性核验 (C9)

实测段内 7 个函数共 20 行非 ASCII:
1. L13928 -> 前置注释属于 check_equip_slot_eligible_neo_daedalus_with_lp_slot_effect -> 对应 plate 1
2. L14114-14124 -> 前置注释属于 check_equip_slot_eligible_type480_with_neo_daedalus_field5_loop -> 对应 plate 3
3. L14363, L14367 -> 前置注释属于 check_equip_slot_eligible_neo_daedalus_with_lp_status_lookup -> 对应 plate 4
4. L14446-14452 -> 前置注释属于 check_equip_slot_eligible_by_active_ctx_score_threshold -> 对应 plate 5
5. L14949 -> 前置注释属于 check_equip_slot_eligible_zone_e_type580_with_neo_daedalus -> 对应 plate 7
6. L15119-15124 -> 前置注释属于 check_equip_slot_eligible_by_lp_status_tier3_neo_daedalus -> 对应 plate 8
7. L15210-15213 -> 前置注释属于 check_equip_slot_eligible_chain_present_with_lp_status_neo_daedalus -> 对应 plate 9

全部 20 行非 ASCII 均对应 proposal plates 中已规划的 7 个 CJK 全改写。proposal plate 2 (commit_equip_effect_node_zone_match) 声称无 CJK 正确——该函数自身 plate 为 ASCII，L14114-14124 属于其后继函数的前置注释。

## 附注

- INFERNO_FIRE_BLAST_CID (0x17f6): 确认为 inline 计算 (0x175b + adds r0,#0x9b = 0x17f6), 无 literal pool 槽, 仅 plate 引用; 算术核验 0x175b+0x9b=0x17f6 正确
- SANCTUARY_IN_THE_SKY_CID: card_info.inc:367 已有 SANCTUARY_CID_SHIFTED(0xbaf00000 = 0x175e<<19), 与 raw CID 0x175e 为不同语义, 新建正确
- dispatch_effect_via_hand_slot_setcode 与 check_zera_ritual_absent_from_field 的 ASCII plate 均将 0x1332 错标为"Zera Ritual" (passcode=81756897); 正确为 Banisher of the Light (pw=61528025); proposal plate 6+11 均已规划订正

## 状态: PASS

所有 C1-C13 检查通过。无 NEEDS_FIX 项。

## 修改清单

无。
