# Refine Review: F07-Seg-8 (iter-2)

段范围: ROM `0x08061eb4..0x08062d28`  模块: `asm/07_equip_effect_chain.s` (L15231..L17234)

---

## 核验矩阵 (C1-C13) — iter-2

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | PASS | Seg-8: 0x61eb4..0x62d28, 与 roadmap 完全一致; Seg-7 已完成 commit 45be161 |
| C2 Rule2 | 所有 ROM_INCBIN/.byte 块均有归宿 | PASS | 5 块全判 R4 disasm; 6 sub-fn; 0 静默保留; 0 §5.1 块 |
| C3 Rule3 | §5.1 块确 0 引用 | N/A | 无 §5.1 块; 5 块均有 THUMB+1 真引用 |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | FAIL | iter-2 修复了 Block2-F1 (eq2 ✓); 但 Block1 机器码解码显示语义描述有误 (subs #1 非 #2, bhi 非 bls, above4 错误) — 见 #3 |
| C5 R1 复用 | 新建前确无现有可复用 | PASS | ATK_THRESHOLD_2999=0xbb7, 4 新 CID: grep 均 0 命中; 标 reuse 常量逐一 grep 确存在 |
| C6 R2 名 | 槽名合规无碰撞 | PASS | iter-2 修复: `field_array_c_0806220c` 无空格 ✓; 所有 69 个 slot_label 符合 `^[a-z][a-z0-9_]+$` |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | PASS | 3 REF 槽 (gp1lp_ptr_*) 有 DATA-ref gP1LifePoints; gEquipChainSlotRefs 3 槽有 EQ label |
| C8 R5 现名 | plate 引用全用现名, 无残留旧 FUN_/DAT_/DWORD_ | PASS | L15350 FUN_08059110 -> tick_equip_activation_if_field_spell_hand_ok; L15867 FUN_080619c0 -> check_equip_slot_eligible_by_active_ctx_score_threshold; 均在 PLATE 计划中 |
| C9 ASCII | plate/EOL 文本纯 ASCII | PASS | L15515/L15519/L15520 CJK 三行均在 PLATE 3 提供纯 ASCII 重写; 重写内容无 CJK |
| C10 carve | 指针表 +1 核对 | N/A | 无 carve; fn-ptr 槽 0x08062bc8=0x080507ad / 0x08062bcc=0x08051abd ROM 独立核对吻合 |
| C11 误名 | 全局 vs 函数名矛盾 | PASS | 无 FUNC_RENAME; 旧 plate gDuelActivation 误称由 PLATE 重写订正至 gEquipChainSlotRefs |
| C12 R6 | 关键槽语义有证据, 无零容忍词 | FAIL | Block1 fn 名/plate 与机器码不符 (见 #3); 其余 5 sub-fn 证据正确 |
| C13 残留 | 段内所有残留自动名槽覆盖完整 | PASS | 55 原始槽 + 14 disasm lit-pool 槽 = 69; EQ(64)+REF(3)+RENAME(2)=69; 范围内全覆盖 |

---

## 独立复核 — iter-2 核验

### iter-2 修复项 #1 (C4/C12/R1): Block2-F1 bne 确认

ROM @ 0x0806240a = 0xd107。解码:
- bits[15:12]=1101 (条件分支), bits[11:8]=0001 (NE条件), bits[7:0]=0x07 (imm=7)
- 指令: `bne -> (0x0806240a+4) + 7*2 = 0x0806241c`
- pass 条件: field_state == 2 (bne 跳走表示不等于2时失败)
- iter-2 改名: `field_eq2` -> **CORRECT** ✓

### iter-2 修复项 #2 (C6/R2): slot label 空格

- DAT_0806220c: proposal 现为 `field_array_c_0806220c` (无空格) ✓
- ROM @ 0x0806220c = 0x0201c600 = gP1FieldArrayCBase, 值正确 ✓

### 防同类错独立核: 全 6 sub-fn 比较运算符逐一验证

| Sub-fn | 函数入口 | CID | cmp 指令 addr | 机器码 | 分支条件 | 通过条件 | 函数名运算符 | 判定 |
|---|---|---|---|---|---|---|---|---|
| Block1 | 0x08062378 | 0x17f3 Mind Wipe | 0x08062390+0x08062392+0x08062394 | 0x3801+0x2802+0xd800 | subs r0,#1; cmp r0,#2; **bhi** | zone_count in {1,2,3} -> 1 (bhi=branch if unsigned higher -> taken when zone_count>=4) | `above4` | **WRONG** — 见 #3 |
| Block2-F1 | 0x080623ec | 0x17fc Taunt | 0x08062408+0x0806240a | 0x2802+0xd107 | cmp r0,#2; **bne** | field_state **== 2** | `eq2` (iter-2 fixed) | CORRECT ✓ |
| Block2-F2 | 0x08062420 | 0x1801 Heavy Slump | 0x08062438+0x0806243a | 0x2807+0xd900 | cmp r0,#7; **bls** | zone_count **> 7** | `above7` | CORRECT ✓ |
| Block3 | 0x08062470 | 0x1804 Cemetary Bomb | 0x08062486+0x08062488 | 0x2800+0xd000 | cmp r0,#0; **beq**->bx lr | field[+0x14] **!= 0** | `nonzero` | CORRECT ✓ |
| Block4 | 0x08062a9c | 0x184d Mind Haxorz | 0x08062ab2+0x08062ab4 | 0x2800+0xd106 | cmp r0,#0; **bne**->return 2 | zone_count **== 0** -> return 1 | `field0c_zero` | CORRECT ✓ |
| Block5 | 0x08062c54 | 0x1853 Covering Fire | 多重 cmp | 0xd001/0xd127/... | 区段类型双层过滤 (0xd/0x14) | 通用链检查 | `chain_refs_slot_status` (无方向语义) | CORRECT ✓ |

结论: iter-2 #1 (eq2) 正确; **Block1 (above4) 发现新错误 #3**。

---

## 状态: NEEDS_FIX

## 修改清单 (NEEDS_FIX, 共 1 项)

### #3 — C4/C12/R1 — Block1 fn 名和 plate 含错误比较语义 "above4" / "> 4"

**位置**: Block1 (CID 0x17f3 Mind Wipe, fn 入口 0x08062378)

**机器码独立解码**:
```
0x08062390: 0x3801 = subs r0,#1      (zone_count - 1)
0x08062392: 0x2802 = cmp r0,#2       (compare zone_count-1 vs 2)
0x08062394: 0xd800 = bhi -> 0x08062398  (branch if unsigned higher: zone_count-1 > 2)
0x08062396: 0x2301 = movs r3,#1      (fall-through: zone_count-1 <= 2 -> r3=1)
0x08062398: 0x1c18 = adds r0,r3,#0   (r0=r3)
0x0806239a: 0x4770 = bx lr           (return)
```

注: `subs r0,#1` 当 r0=0 时产生借位 (C=0), 结果为 0xFFFFFFFF, bhi 判定为 > 2 (unsigned), 故 zone_count=0 也走 bhi 分支。

**精确逻辑**:
- zone_count = 0: bhi taken (0xFFFFFFFF > 2) -> r3=0 -> return 0
- zone_count = 1,2,3: bhi NOT taken (0,1,2 不高于 2) -> r3=1 -> return 1
- zone_count >= 4: bhi taken -> r3=0 -> return 0
- **通过条件**: zone_count in {1, 2, 3}

**错误内容**:
- proposal L294: 描述写 `subs r0,#2` (实为 `subs r0,#1`) 和 `bls fail` (实为 `bhi`)
- proposal L295: 描述 `if zone_count-2 <= 2 (i.e. count <= 4) returns 0, else returns 1` (错误)
- proposal L297: fn 名 `check_equip_slot_eligible_opp_lp_zone_count_above4_for_cid_17f3`
- proposal L298: plate `returns 1 if opp_zone_count > 4, else 0` (错误)

**正确内容**:
- fn 名应改为: `check_equip_slot_eligible_opp_lp_zone_count_lte3_for_cid_17f3`
- plate 应将 `returns 1 if opp_zone_count > 4, else 0` 改为 `returns 1 if opp_zone_count in {1,2,3} (zone_count-1 <= 2 unsigned), else 0`
- 机器码注记应更正: `subs r0,#1` + `cmp r0,#2` + `bhi` (0xd800)

**证据**: 机器码 `0xd800` bits[11:8]=1000=HI -> `bhi` (unsigned higher, cond C=1&&Z=0). 前序 `0x3801` = `subs r0,#1`. ROM addr 验证: 0x08062390=0x3801, 0x08062392=0x2802, 0x08062394=0xd800.

---

## 附: 通过项核验摘要 (iter-2 完整)

- **ref-scan** (iter-1 已复核): 5 blocks, 6 THUMB+1 命中, CID+fn_elig 全部独立 python 核对 OK
- **EQ 值**: 55 原始槽 + 14 lit-pool 槽, struct.unpack 逐一比对, 全部 MATCH
- **RENAME fn-ptr**: 0x08062bc8=0x080507ad / 0x08062bcc=0x08051abd, ROM 实读 MATCH
- **C5 双向**: ATK_THRESHOLD_2999 + 4 CID grep 0 命中; TAUNT_CID/CEMETARY_BOMB_CID/所有 reuse 常量 grep 确存在
- **C8**: L15350 FUN_08059110 / L15867 FUN_080619c0 识别并提供正确现名 (naming-proposals.csv L1373/L1700 确认)
- **C9**: L15515/L15519/L15520 CJK 行的 ASCII 重写文本无非 ASCII 字符
- **Block2-F1 eq2**: ROM @ 0x0806240a = 0xd107 (bne, NE 条件) ✓ iter-2 修复正确
- **C6 空格**: `field_array_c_0806220c` 无空格 ✓ iter-2 修复正确
- **Block2-F2 above7**: 0x2807+0xd900 = cmp r0,#7 + bls -> 通过条件 r0 > 7 -> CORRECT
- **Block3 nonzero**: 0x2800+0xd000 = cmp r0,#0 + beq->bx lr -> 通过条件 r0!=0 -> CORRECT
- **Block4 field0c_zero**: 0x2800+0xd106 = cmp r0,#0 + bne->return 2 -> 通过条件 r0==0 -> CORRECT
- **Block5 chain_refs_slot_status**: 无单一方向运算符, 名称保守 -> CORRECT

---

## Reviewer Verdict: F07-Seg-8 = NEEDS_FIX(1 items)
