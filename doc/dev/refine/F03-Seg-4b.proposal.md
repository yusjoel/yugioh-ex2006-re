# Refine Proposal: F03-Seg-4b  [0x08037ec0..0x0803a7f0)

## 拆分建议 (Seg-4b1 / Seg-4b2)

Seg-4b 覆盖 15 个命名函数 + 大型 ROM_INCBIN @ 0x39350/0x10ce，
总槽数约 145，建议在地址序 **函数边界** 处拆分为两个子段执行：

| 子段 | 地址范围 | fn | 槽数 | ROM_INCBIN | 主要工作 |
|------|----------|----|------|------------|----------|
| **Seg-4b1** | 0x08037ec0..0x0803a540 | 7 fn | ~100 | **0x39350/0x10ce** R4 disasm | eval_slot_score_entry_full 复合体 |
| **Seg-4b2** | 0x0803a540..0x0803a7f0 | 3 fn | ~45 | 无 | equip chain rule / eligibility table |

拆分边界: `check_slot_equip_chain_rule` 起点 0x0803a540（`cleanup_slot_score_entry_epilogue` bx r0 @ 0x0803a52e 之后 +0x12 对齐）。
如 reviewer 认为可单段执行，本 proposal 覆盖全程，供参考。

---

## 段测绘

### 函数入口 x15（含 sub-fns 共享同一 eval_slot_score_entry_full 栈帧）

| 地址 | 函数名 | asm 行 |
|------|--------|--------|
| 0x08037ec0 | eval_slot_score_entry_full | 4335 |
| 0x08038a1a | compute_lp_cost_by_occupied_monster_zones | 5896 |
| 0x080389dc `ptr` | count_monster_slots_by_fnptr callback: 0x0804b048 = check_card_is_amazoness_type | (REF 槽) |
| 0x08038c60 | compute_lp_cost_by_hand_field6 | 6149 |
| 0x08038d34 | compute_lp_cost_by_extra_deck_card_id | 6288 |
| 0x08038e84 | compute_lp_cost_by_zone_field5_x100 | 6400 |
| 0x08038e90 | compute_lp_cost_by_zone_field5_x200 | 6412 |
| 0x08038e9c | compute_lp_cost_by_zone_field5_both_players | 6424 |
| 0x08038e34 | apply_slot_score_bonus_by_state | 6443 |
| 0x080392da | dispatch_equip_node_by_type | 7061 |
| 0x0803a41e | advance_equip_node_chain_step | 7114 |
| 0x0803a428 | adjust_slot_score_by_chain_and_zone | 7121 |
| 0x0803a520 | cleanup_slot_score_entry_epilogue | 7252 |
| 0x0803a540 | check_slot_equip_chain_rule | 7271 |
| 0x0803a658 | classify_equip_target_eligibility | 7421 |
| 0x0803a7f0 | build_equip_target_eligibility_table (Seg-5 start) | 7635 |

Note: `build_equip_target_eligibility_table` @ 0x0803a7f0 is the Seg-5 start boundary; it is NOT included in this proposal.

### 残留自动名槽 x~145

以下为 Seg-4b 内所有 DAT_/DWORD_/PTR_ 定义按 asm 行序列出（共约 145 个，含 PTR_gP1LifePoints 系列）。

```
DAT_08038034 @ 08038034 = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_08038038 @ 08038038 = 0x0201c510   (gDuelFieldSlots)
DAT_0803803c @ 0803803c = 0x000018c7   (CID: Elemental Mistress Doriado)
DAT_08038040 @ 08038040 = 0x000019ef   (CID: Elemental Hero Erikshieler)
DAT_08038044 @ 08038044 = 0x00001257   (CID: Reverse Trap)
DAT_08038048 @ 08038048 = 0x00001864   (CID: Behemoth the King of All Animals)
DAT_0803804c @ 0803804c = 0x0000172f   (CID: Skull Zoma)
DAT_08038050 @ 08038050 = 0x00001472   (CID: Embodiment of Apophis)
DAT_08038054 @ 08038054 = 0x00001636   (CID: Metal Reflect Slime)
DAT_08038068 @ 08038068 = 0x00001809   (CID: Stronghold)
DAT_08038080 @ 08038080 = 0x000018c5   (CID: King of the Skull Servants)
DAT_08038098 @ 08038098 = 0x0000191b   (CID: Tyranno Infinity)
DAT_080380a8 @ 080380a8 = 0x000019d2   (CID: Sand Moth)
DAT_080380d8 @ 080380d8 = 0x00000bb8   (3000)
DAT_08038168 @ 08038168 = 0x00000fbe   (CID: Skull Servant)
DAT_08038190 @ 08038190 = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_08038194 @ 08038194 = 0x0201c510   (gDuelFieldSlots)
DAT_080382ac @ 080382ac = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_080382b0 @ 080382b0 = 0x0201c510   (gDuelFieldSlots)
DAT_080382b4 @ 080382b4 = 0x000014b0   (EQUIP_NODE_BASE_OFFSET -- confirmed; ldr r6,DAT_080382b4; add r6,r8 @ asm line 4743-4744 walks equip pool; NOT a card_id)
DAT_080382b8 @ 080382b8 = 0x000012cb   (CID: Shield & Sword)
DAT_080382bc @ 080382bc = 0x000019f1   (CID: Great Spirit)
DAT_080382c0 @ 080382c0 = 0x00001651   (CID: Gyaku-Gire Panda)
DAT_080382c4 @ 080382c4 = 0x00001387   (CID gap -- see §求助)
DAT_080382c8 @ 080382c8 = 0x000011aa   (CID: Muka Muka)
DAT_080382cc @ 080382cc = 0x00001009   (CID: Pumpking the King of Ghosts)
DAT_080382dc @ 080382dc = 0x00001091   (CID gap -- see §求助)
DAT_080382f8 @ 080382f8 = 0x0000113d   (CID: Machine King)
DAT_08038308 @ 08038308 = 0x00001193   (CID: Maha Vailo)
DAT_08038338 @ 08038338 = 0x0000129e   (CID: Dark Magician Girl)
DAT_08038354 @ 08038354 = 0x00001336   (CID: Flash Assailant)
DAT_0803836c @ 0803836c = 0x0000133d   (CID gap -- see §求助)
DAT_080383a0 @ 080383a0 = 0x000014fc   (GRADIUS_OPTION_CID -- reuse)
DAT_080383a4 @ 080383a4 = 0x000013e8   (CID: Nuvia the Wicked)
DAT_080383b4 @ 080383b4 = 0x000013ad   (CID: Slate Warrior)
DAT_080383d0 @ 080383d0 = 0x00001486   (CID: The Rock Spirit)
DAT_080383e0 @ 080383e0 = 0x000014ec   (CID: Mudora)
DAT_08038408 @ 08038408 = 0x000015fc   (CID: Dark Paladin)
DAT_08038418 @ 08038418 = 0x0000157d   (CID: Master of Dragon Soldier)
DAT_08038434 @ 08038434 = 0x0000160f   (AMAZONESS_TIGER_CID -- reuse)
DAT_0803844c @ 0803844c = 0x00001615   (CID: Magical Marionette)
DAT_08038490 @ 08038490 = 0x00001894   (CID: Red-Eyes Darkness Dragon)
DAT_08038494 @ 08038494 = 0x00001789   (CID: Theban Nightmare)
DAT_080384a4 @ 080384a4 = 0x000016ac   (CID: Perfect Machine King)
DAT_080384c0 @ 080384c0 = 0x00001742   (CID: The Agent of Force - Mars)
DAT_080384d0 @ 080384d0 = 0x00001755   (SOLAR_FLARE_DRAGON_CID -- reuse)
DAT_080384f8 @ 080384f8 = 0x000017eb   (CID: Enraged Muka Muka)
DAT_08038500 @ 08038500 = 0x000017e3   (CID: Element Dragon)
DAT_0803851c @ 0803851c = 0x00001817   (CID: Silent Magician LV4)
DAT_08038534 @ 08038534 = 0x00001827   (CID: Element Saurus)
DAT_0803856c @ 0803856c = 0x000019cc   (CID: Beelze Frog)
DAT_0803857c @ 0803857c = 0x00001943   (CID: EH Shining Flare Wingman)
DAT_08038598 @ 08038598 = 0x000019be   (CID: Machine King Prototype)
DAT_080385a8 @ 080385a8 = 0x000019c4   (CID: Parasitic Ticky)
DAT_080385d0 @ 080385d0 = 0x000019ef   (CID: Elemental Hero Erikshieler -- 2nd slot)
DAT_080385e0 @ 080385e0 = 0x000019d6   (CID: D.3.S. Frog)
DAT_08038600 @ 08038600 = 0x000019f6   (CID: The Ancient Sun Helios)
DAT_0803861c @ 0803861c = 0x000019f7   (CID: Helios Duo Megiste)
DAT_0803862c @ 0803862c = 0x000011d0   (CID gap -- see §求助)
DAT_08038684 @ 08038684 = 0x00000fe4   (CID: Harpie Lady)
DAT_080386c4 @ 080386c4 = 0x00000fb2   (CID gap -- see §求助)
DAT_080386f0 @ 080386f0 = 0x00001cbc   (offset gP1LP+0x1cbc -- see §求助)
DAT_08038754 @ 08038754 = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_08038758 @ 08038758 = 0x0201c4f4   (gP1HandCountBase)
DAT_0803875c @ 0803875c = 0x00001278   (CID: Magician of Black Chaos)
DAT_08038760 @ 08038760 = 0x00000404   (offset gP1HandCountBase->gP1HandSlotArray)
DAT_08038764 @ 08038764 = 0x00000fc9   (CID: Dark Magician)
DAT_08038784 @ 08038784 = 0x0000142d   (CID: Dark Magician [2nd ref])
DAT_080387bc @ 080387bc = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_0803884c @ 0803884c = 0xfffffc18   (PUZZLE_LP_STEP_1000 = -1000 -- reuse)
PTR_gP1LifePoints_08038894 @ 08038894  = gP1LifePoints
DAT_08038898 @ 08038898 = 0x00000868   (PLAYER_BLOCK_STRIDE)
PTR_gP1LifePoints_080388f8 @ 080388f8  = gP1LifePoints
DAT_080388fc @ 080388fc = 0x00000868   (PLAYER_BLOCK_STRIDE)
PTR_gP1LifePoints_08038938 @ 08038938  = gP1LifePoints
DAT_0803893c @ 0803893c = 0x00001ce8   (P1LP_BLOCK2_OFF_1CE8 -- reuse)
DAT_08038940 @ 08038940 = 0x00001cf4   (offset gP1LP+0x1cf4 -- see §求助)
DAT_08038968 @ 08038968 = 0x00001cb8   (DUEL_ACTIVE_PLAYER_OFF -- reuse)
DAT_0803896c @ 0803896c = 0x00001cc4   (offset gP1LP+0x1cc4 -- see §求助)
DAT_080389a8 @ 080389a8 = 0x0000ffff   (SLOT_EMPTY / sentinel 0xffff)
DAT_080389dc @ 080389dc = 0x0804b049   (THUMB fn-ptr: check_card_is_amazoness_type)
DAT_080389f8 @ 080389f8 = 0x0804b049   (THUMB fn-ptr: check_card_is_amazoness_type -- 2nd)
DAT_08038a40 @ 08038a40 = 0x00000868   (PLAYER_BLOCK_STRIDE)
PTR_gP1LifePoints_08038aa8 @ 08038aa8  = gP1LifePoints
DAT_08038aac @ 08038aac = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_08038ae4 @ 08038ae4 = 0xbaf00000   (SANCTUARY_IN_THE_SKY_CID << 19 shifted sentinel)
DAT_08038b38 @ 08038b38 = 0x000005dc   (1500 -- LP cost threshold)
DAT_08038be4 @ 08038be4 = 0x00001472   (EMBODIMENT_OF_APOPHIS_CID -- 2nd slot)
DAT_08038be8 @ 08038be8 = 0x00001807   (CID: Green Gadget)
DAT_08038bec @ 08038bec = 0x0000180b   (CID: Red Gadget)
DAT_08038bf0 @ 08038bf0 = 0x0000180c   (CID: Yellow Gadget)
DAT_08038bf4 @ 08038bf4 = 0x00000bb8   (3000 -- 2nd slot)
DAT_08038c7c @ 08038c7c = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_08038c80 @ 08038c80 = 0x0201c510   (gDuelFieldSlots)
DAT_08038c84 @ 08038c84 = 0xc6180000   (BATTERYMAN_AA_CID_SHIFTED = 0x18c3<<19 -- new shifted sentinel)
DAT_08038d18 @ 08038d18 = 0x00001919   (CID: T.A.D.P.O.L.E.)
DAT_08038d48 @ 08038d48 = 0x000019cb   (CID: Treeborn Frog)
DAT_08038da4 @ 08038da4 = 0x0201c510   (gDuelFieldSlots)
PTR_gP1LifePoints_08038dcc @ 08038dcc  = gP1LifePoints
DAT_08038dd0 @ 08038dd0 = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_08038e64 @ 08038e64 = 0x00001782   (CID: Mokey Mokey)
DAT_08038e68 @ 08038e68 = 0x00001843   (CID: Mokey Mokey Smackdown)
DAT_08038e6c @ 08038e6c = 0x00000bb8   (3000 -- 3rd slot)
DAT_08038f0c @ 08038f0c = 0x00001399   (CID: Command Knight)
DAT_08038f10 @ 08038f10 = 0x000014cf   (CID: The A. Forces)
DAT_08039120 @ 08039120 = 0x0201c510   (gDuelFieldSlots)
DAT_08039124 @ 08039124 = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_08039128 @ 08039128 = 0xc8e00000   (BATTERYMAN_C_CID << 19 shifted sentinel)
DAT_0803912c @ 0803912c = 0x09e3f094   (zone_monster_field_bonus_table -- R7 carve)
DAT_08039130 @ 08039130 = 0x000013f6   (CID: Lightning Blade)
DAT_08039134 @ 08039134 = 0x000016ab   (CID: Nightmare Penguin)
DAT_08039138 @ 08039138 = 0x00001429   (CID: Yellow Luster Shield)
PTR_gP1LifePoints_0803913c @ 0803913c  = gP1LifePoints
DAT_08039140 @ 08039140 = 0x00001ce8   (P1LP_BLOCK2_OFF_1CE8 -- reuse 2nd)
DAT_08039144 @ 08039144 = 0x00001cf4   (gP1LP+0x1cf4 -- 2nd slot)
DAT_08039148 @ 08039148 = 0x000015a2   (CID: Banner of Courage)
DAT_0803914c @ 0803914c = 0x0000138e   (CID: Aqua Chorus)
DAT_08039150 @ 08039150 = 0x000019b2   (CID: Ancient Gear Castle)
DAT_08039154 @ 08039154 = 0x00001822   (CID: Ultimate Insect LV3)
DAT_08039158 @ 08039158 = 0x00001483   (CID: Soul of Purity and Light)
DAT_0803916c @ 0803916c = 0x0000185e   (CID: Ultimate Insect LV5)
DAT_08039190 @ 08039190 = 0x0201c510   (gDuelFieldSlots)
DAT_08039194 @ 08039194 = 0x00001cb8   (DUEL_ACTIVE_PLAYER_OFF -- reuse 2nd)
DAT_08039198 @ 08039198 = 0x0201e1d4   (gP1LifePoints + 0x1cf4 direct addr -- see §求助)
DAT_0803919c @ 0803919c = 0xfffffed4   (-300 score delta)
DAT_080391b8 @ 080391b8 = 0xfffffed4   (-300 score delta -- 2nd)
DAT_080391d4 @ 080391d4 = 0xfffffe0c   (-500 score delta)
DAT_08039258 @ 08039258 = 0xfffffd44   (-700 score delta)
DAT_0803925c @ 0803925c = 0x0201c5d8   (gDuelFieldSlots_p2_base -- reuse)
DAT_08039260 @ 08039260 = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_0803930c @ 0803930c = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_08039310 @ 08039310 = 0x0201c510   (gDuelFieldSlots)
DAT_08039314 @ 08039314 = 0x0201d9c0   (gEquipNodePool)
DAT_08039318 @ 08039318 = 0x0803931c   (ROM addr: jump table base for dispatch_equip_node_by_type)
PTR_DAT_0803931c .. 0x0803934f (13 entries, jump table -- see §5.1 / carve plan)
DAT_08039350 = ROM_INCBIN 0x39350, 0x10ce (R4 disasm -- see §数据块分类)

--- Seg-4b2 slots ---
DAT_0803a530 @ 0803a530 = 0x00001951   (CID: Water Dragon)
DAT_0803a534 @ 0803a534 = 0x00001955   (CID: Cyber Blader)
DAT_0803a538 @ 0803a538 = 0x00001381   (CID: Mirror Wall)
DAT_0803a53c @ 0803a53c = 0x00001905   (CID: Dark Dreadroute)
DAT_0803a59c @ 0803a59c = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_0803a5a0 @ 0803a5a0 = 0x0201c510   (gDuelFieldSlots)
DAT_0803a5bc @ 0803a5bc = 0x00001399   (CID: Command Knight -- 2nd slot)
DAT_0803a64c @ 0803a64c = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_0803a650 @ 0803a650 = 0x0201c510   (gDuelFieldSlots)
DAT_0803a654 @ 0803a654 = 0x09e3f094   (zone_monster_field_bonus_table -- R3 ref 2nd)
DAT_0803a6c4 @ 0803a6c4 = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_0803a6c8 @ 0803a6c8 = 0x0201c510   (gDuelFieldSlots)
DAT_0803a6cc @ 0803a6cc = 0x000014b0   (EQUIP_NODE_BASE_OFFSET -- reuse)
DAT_0803a704 @ 0803a704 = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_0803a708 @ 0803a708 = 0x0201c510   (gDuelFieldSlots)
DAT_0803a70c @ 0803a70c = 0x00000ff9   (CID: Castle of Dark Illusions)
DAT_0803a720 @ 0803a720 = 0x0000128a   (CID gap 0x128a -- see §求助)
DAT_0803a724 @ 0803a724 = 0x00001743   (CID: The Unhappy Girl)
DAT_0803a74c @ 0803a74c = 0x00000868   (PLAYER_BLOCK_STRIDE)
DAT_0803a7bc @ 0803a7bc = 0x00000868   (PLAYER_BLOCK_STRIDE)
```

### ROM_INCBIN / .byte 块

| 块 | 地址 | size | asm 行 |
|----|------|------|--------|
| DAT_08039350 | 0x08039350 | 0x10ce | 7109-7110 |

---

## 数据块分类 (Rule 2/3) -- ref-scan 证据

### 块 0x08039350 / size 0x10ce (ROM_INCBIN 0x39350, 0x10ce)

**ref-scan 结果**:

```python
# python -c "
# import struct; d=open('roms/2343.gba','rb').read()
# for a in [0x08039350,0x08039a62,0x08039a7c,0x08039c1c,0x0803a2fc,0x0803a3c4]:
#     print(hex(a), d.count(struct.pack('<I',a)), d.count(struct.pack('<I',a|1)))
# "
0x08039350  raw=4  thumb=0
0x08039a62  raw=1  thumb=0
0x08039a7c  raw=4  thumb=0
0x08039c1c  raw=2  thumb=0
0x0803a2fc  raw=1  thumb=0
0x0803a3c4  raw=1  thumb=0
```

全部 13 引用来自同一跳转表 PTR_DAT_0803931c (0x0803931c..0x0803934f, asm 行 7095-7108)：
`dispatch_equip_node_by_type` 末尾 `ldr r0,[table+idx*4]; mov pc,r0` 13-entry 调度表。

**模式分析**:
- 块内 THUMB opcode 确认 (ldr r0,[pc,#n] / cmp r4,r0 / bne +2 / b forward): card-ID 比较链代码格式。
- raw=N (偶地址), thumb=0: `mov pc,r0` 在 THUMB 上下文执行时 CPSR.T 不变，CPU 维持 THUMB 模式执行偶地址目标。
- 无 THUMB+1 指针 (函数指针不通过 BX 跳转，而是直接 mov pc,r0)。
- 全部引用均为内部跳转表，无外部 `bl` 直接调用。

**判定: R4 disasm (THUMB code)** -- confidence high
- asm/03 行 7059 plate 已述: "13-entry jump table at 0x0803931c (mov pc,r0)"
- 块被 4+1+4+2+1+1=13 次引用 (均来自跳转表，无压缩资产偶合)

**子块边界** (6 个分离目标地址):

| 子块起点 | 子块止点 | size | jump table 次数 |
|----------|----------|------|-----------------|
| 0x08039350 | 0x08039a62 | 0x712 | 4 (type 1..4 均跳此) |
| 0x08039a62 | 0x08039a7c | 0x1a | 1 (type 5) |
| 0x08039a7c | 0x08039c1c | 0x1a0 | 4 (type 6..9) |
| 0x08039c1c | 0x0803a2fc | 0x6e0 | 2 (type 10..11) |
| 0x0803a2fc | 0x0803a3c4 | 0xc8 | 1 (type 13) |
| 0x0803a3c4 | 0x0803a41e | 0x5a | 1 (type 12) |

末尾: 0x0803a41e = `advance_equip_node_chain_step` 起点 (asm 行 7114 已存在 label)。

**disasm 操作** (逐子块, 必须 per-stub 不能整 range 一次):
1. `clearListing(0x08039350, 0x0803a41d)` -- 先清
2. `ctx.setValue("TMode", 0x08039350, 0x0803a41d, 1)` -- 设 THUMB
3. 每个子块独立 `DisassembleCommand(start, AddressSet(start, end-1), True)` x6
4. 每个子块 `createFunction(start, None)` (不共享 eval_slot_score_entry_full 栈帧，按分支点独立)

---

## 符号化计划 (R1/R2/R3)

### EQ_SLOTS (data-equate)

优先复用 constants/*.inc 已有常量 (C5 value-dedup)。

**R1 复用现有常量 (已在 inc 中)**:

| slot | value | const_name | inc 文件 | slot_label |
|------|-------|-----------|---------|------------|
| DAT_08038034 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | eval_slot_score_entry_full_stride_a |
| DAT_08038038 | 0x0201c510 | -- (REF, 非 EQ) | ewram.inc | eval_slot_score_entry_full_field_slots |
| DAT_08038190 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | eval_slot_lp_cost_stride_a |
| DAT_08038194 | 0x0201c510 | -- (REF) | ewram.inc | eval_slot_lp_cost_field_slots_a |
| DAT_080382ac | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | eval_slot_lp_cost_stride_b |
| DAT_080382b0 | 0x0201c510 | -- (REF) | ewram.inc | eval_slot_lp_cost_field_slots_b |
| DAT_08038517 | 0x14fc | GRADIUS_OPTION_CID | card_info.inc | eval_gradius_option_cid |
| DAT_08038434 | 0x160f | AMAZONESS_TIGER_CID | card_info.inc | eval_amazoness_tiger_cid |
| DAT_080384d0 | 0x1755 | SOLAR_FLARE_DRAGON_CID | card_info.inc | eval_solar_flare_cid |
| DAT_0803884c | 0xfffffc18 | PUZZLE_LP_STEP_1000 | duel_field.inc | eval_lp_step_neg1000 |
| DAT_0803893c | 0x1ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | eval_p1lp_block2_off_a |
| DAT_08039140 | 0x1ce8 | P1LP_BLOCK2_OFF_1CE8 | ewram.inc | eval_p1lp_block2_off_b |
| DAT_08038968 | 0x1cb8 | DUEL_ACTIVE_PLAYER_OFF | duel_field.inc | eval_active_player_off_a |
| DAT_08039194 | 0x1cb8 | DUEL_ACTIVE_PLAYER_OFF | duel_field.inc | eval_active_player_off_b |
| DAT_08038940 | 0x1cf4 | FIELD_STATE_OFF | duel_field.inc (new) | eval_field_state_off_a |
| DAT_08039144 | 0x1cf4 | FIELD_STATE_OFF | duel_field.inc (new) | eval_field_state_off_b |
| DAT_080386f0 | 0x1cbc | CHAIN_LINK_COUNTER_OFF | duel_field.inc (new) | eval_chain_link_counter_off |
| DAT_0803896c | 0x1cc4 | EQUIP_PHASE_STATE_OFF | duel_field.inc (new) | eval_equip_phase_state_off |
| DAT_08038754 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | eval_hand_magicians_stride |
| DAT_080387bc | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | eval_slot_bonus_stride_a |
| DAT_08038898 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | eval_lp_cost_zone_stride_a |
| DAT_080388fc | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | eval_lp_cost_zone_stride_b |
| DAT_08038a40 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | eval_monster_zone_stride_a |
| DAT_08038aac | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | eval_sanctuary_stride |
| DAT_08038c7c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | eval_hand_field6_stride |
| DAT_08038c80 | 0x0201c510 | -- (REF) | ewram.inc | eval_hand_field6_slots |
| DAT_08038da4 | 0x0201c510 | -- (REF) | ewram.inc | eval_extra_deck_slots |
| DAT_08038dd0 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | eval_extra_deck_stride |
| DAT_08039120 | 0x0201c510 | -- (REF) | ewram.inc | eval_bonus_state_slots_a |
| DAT_08039124 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | eval_bonus_state_stride_a |
| DAT_08039190 | 0x0201c510 | -- (REF) | ewram.inc | eval_bonus_state_slots_b |
| DAT_0803930c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | dispatch_equip_node_stride |
| DAT_08039310 | 0x0201c510 | -- (REF) | ewram.inc | dispatch_equip_node_slots |
| DAT_08039314 | 0x0201d9c0 | -- (REF gEquipNodePool) | ewram.inc | dispatch_equip_node_pool |
| DAT_08039260 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | adjust_score_chain_stride |
| DAT_0803925c | 0x0201c5d8 | -- (REF gDuelFieldSlots_p2_base) | ewram.inc | adjust_score_p2_slots |
| DAT_0803a59c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | check_equip_chain_stride_a |
| DAT_0803a5a0 | 0x0201c510 | -- (REF) | ewram.inc | check_equip_chain_slots_a |
| DAT_0803a64c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | classify_equip_stride_a |
| DAT_0803a650 | 0x0201c510 | -- (REF) | ewram.inc | classify_equip_slots_a |
| DAT_0803a6c4 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | classify_equip_stride_b |
| DAT_0803a6c8 | 0x0201c510 | -- (REF) | ewram.inc | classify_equip_slots_b |
| DAT_080382b4 | 0x14b0 | EQUIP_NODE_BASE_OFFSET | duel_field.inc | eval_equip_pool_base_off |
| DAT_0803a6cc | 0x14b0 | EQUIP_NODE_BASE_OFFSET | duel_field.inc | classify_equip_node_base_off |
| DAT_0803a704 | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | classify_equip_stride_c |
| DAT_0803a708 | 0x0201c510 | -- (REF) | ewram.inc | classify_equip_slots_c |
| DAT_0803a74c | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | build_elig_table_stride |
| DAT_0803a7bc | 0x868 | PLAYER_BLOCK_STRIDE | ewram.inc | build_elig_table_stride_b |

**R1 新建 EQ 常量 (card IDs -- card-stats.s 验证完毕)**:

以下 card IDs 均经 `data/card-stats.s` slot= 字段逐一核对，confidence high。
拟新建至 `card_info.inc`（按字母序）：

| value | card_name | proposed_const | 所在 slots |
|-------|-----------|---------------|-----------|
| 0x113d | Machine King | MACHINE_KING_CID | DAT_080382f8 |
| 0x1193 | Maha Vailo | MAHA_VAILO_CID | DAT_08038308 |
| 0x11aa | Muka Muka | MUKA_MUKA_CID | DAT_080382c8 |
| 0x1257 | Reverse Trap | REVERSE_TRAP_CID | DAT_08038044 |
| 0x1278 | Magician of Black Chaos | MAGICIAN_OF_BLACK_CHAOS_CID | DAT_0803875c |
| 0x129e | Dark Magician Girl | DARK_MAGICIAN_GIRL_CID | DAT_08038338 |
| 0x12cb | Shield & Sword | SHIELD_AND_SWORD_CID | DAT_080382b8 |
| 0x1336 | Flash Assailant | FLASH_ASSAILANT_CID | DAT_08038354 |
| 0x13ad | Slate Warrior | SLATE_WARRIOR_CID | DAT_080383b4 |
| 0x13e8 | Nuvia the Wicked | NUVIA_THE_WICKED_CID | DAT_080383a4 |
| 0x13f6 | Lightning Blade | LIGHTNING_BLADE_CID | DAT_08039130 |
| 0x1429 | Yellow Luster Shield | YELLOW_LUSTER_SHIELD_CID | DAT_08039138 |
| 0x142d | Dark Magician | DARK_MAGICIAN_CID_142D | DAT_08038784, DAT_08038760+ctx |
| 0x1472 | Embodiment of Apophis | EMBODIMENT_OF_APOPHIS_CID | DAT_08038050, DAT_08038be4 |
| 0x1483 | Soul of Purity and Light | SOUL_OF_PURITY_CID | DAT_08039158 |
| 0x1486 | The Rock Spirit | ROCK_SPIRIT_CID | DAT_080383d0 |
| 0x14cf | The A. Forces | THE_A_FORCES_CID | DAT_08038f10 |
| 0x14ec | Mudora | MUDORA_CID | DAT_080383e0 |
| 0x157d | Master of Dragon Soldier | MASTER_OF_DRAGON_SOLDIER_CID | DAT_08038418 |
| 0x15a2 | Banner of Courage | BANNER_OF_COURAGE_CID | DAT_08039148 |
| 0x15fc | Dark Paladin | DARK_PALADIN_CID | DAT_08038408 |
| 0x1615 | Magical Marionette | MAGICAL_MARIONETTE_CID | DAT_0803844c |
| 0x1636 | Metal Reflect Slime | METAL_REFLECT_SLIME_CID | DAT_08038054 |
| 0x1651 | Gyaku-Gire Panda | GYAKU_GIRE_PANDA_CID | DAT_080382c0 |
| 0x16ab | Nightmare Penguin | NIGHTMARE_PENGUIN_CID | DAT_08039134 |
| 0x16ac | Perfect Machine King | PERFECT_MACHINE_KING_CID | DAT_080384a4 |
| 0x172f | Skull Zoma | SKULL_ZOMA_CID | DAT_0803804c |
| 0x1742 | The Agent of Force Mars | AGENT_OF_FORCE_MARS_CID | DAT_080384c0 |
| 0x1743 | The Unhappy Girl | UNHAPPY_GIRL_CID | DAT_0803a724 |
| 0x1782 | Mokey Mokey | MOKEY_MOKEY_CID | DAT_08038e64 |
| 0x1789 | Theban Nightmare | THEBAN_NIGHTMARE_CID | DAT_08038494 |
| 0x17e3 | Element Dragon | ELEMENT_DRAGON_CID | DAT_08038500 |
| 0x17eb | Enraged Muka Muka | ENRAGED_MUKA_MUKA_CID | DAT_080384f8 |
| 0x1807 | Green Gadget | GREEN_GADGET_CID | DAT_08038be8 |
| 0x1809 | Stronghold | STRONGHOLD_CID | DAT_08038068 |
| 0x180b | Red Gadget | RED_GADGET_CID | DAT_08038bec |
| 0x180c | Yellow Gadget | YELLOW_GADGET_CID | DAT_08038bf0 |
| 0x1817 | Silent Magician LV4 | SILENT_MAGICIAN_LV4_CID | DAT_0803851c |
| 0x1822 | Ultimate Insect LV3 | ULTIMATE_INSECT_LV3_CID | DAT_08039154 |
| 0x1827 | Element Saurus | ELEMENT_SAURUS_CID | DAT_08038534 |
| 0x1843 | Mokey Mokey Smackdown | MOKEY_MOKEY_SMACKDOWN_CID | DAT_08038e68 |
| 0x1809 | Stronghold | STRONGHOLD_CID | (already above) |
| 0x1864 | Behemoth King of All Animals | BEHEMOTH_KING_CID | DAT_08038048 |
| 0x185e | Ultimate Insect LV5 | ULTIMATE_INSECT_LV5_CID | DAT_0803916c |
| 0x1894 | Red-Eyes Darkness Dragon | RED_EYES_DARKNESS_DRAGON_CID | DAT_08038490 |
| 0x18c5 | King of the Skull Servants | KING_OF_SKULL_SERVANTS_CID | DAT_08038080 |
| 0x18c7 | Elemental Mistress Doriado | DORIADO_CID | DAT_0803803c |
| 0x1905 | Dark Dreadroute | DARK_DREADROUTE_CID | DAT_0803a53c |
| 0x1919 | T.A.D.P.O.L.E. | TADPOLE_CID | DAT_08038d18 |
| 0x191b | Tyranno Infinity | TYRANNO_INFINITY_CID | DAT_08038098 |
| 0x1943 | EH Shining Flare Wingman | EHERO_SHINING_FLARE_WINGMAN_CID | DAT_0803857c |
| 0x1951 | Water Dragon | WATER_DRAGON_CID | DAT_0803a530 |
| 0x1955 | Cyber Blader | CYBER_BLADER_CID | DAT_0803a534 |
| 0x19be | Machine King Prototype | MACHINE_KING_PROTOTYPE_CID | DAT_08038598 |
| 0x19b2 | Ancient Gear Castle | ANCIENT_GEAR_CASTLE_CID | DAT_08039150 |
| 0x19c4 | Parasitic Ticky | PARASITIC_TICKY_CID | DAT_080385a8 |
| 0x19cb | Treeborn Frog | TREEBORN_FROG_CID | DAT_08038d48 |
| 0x19cc | Beelze Frog | BEELZE_FROG_CID | DAT_0803856c |
| 0x19d2 | Sand Moth | SAND_MOTH_CID | DAT_080380a8 |
| 0x19d6 | D.3.S. Frog | D3S_FROG_CID | DAT_080385e0 |
| 0x19ef | EH Erikshieler | EHERO_ERIKSHIELER_CID | DAT_08038040, DAT_080385d0 |
| 0x19f1 | Great Spirit | GREAT_SPIRIT_CID | DAT_080382bc |
| 0x19f6 | The Ancient Sun Helios | HELIOS_CID | DAT_08038600 |
| 0x19f7 | Helios Duo Megiste | HELIOS_DUO_MEGISTE_CID | DAT_0803861c |
| 0x1381 | Mirror Wall | MIRROR_WALL_CID | DAT_0803a538 |
| 0x138e | Aqua Chorus | AQUA_CHORUS_CID | DAT_0803914c |
| 0x1399 | Command Knight | COMMAND_KNIGHT_CID | DAT_08038f0c, DAT_0803a5bc |
| 0x0fbe | Skull Servant | SKULL_SERVANT_CID | DAT_08038168 |
| 0x0fc9 | Dark Magician (alt print) | DARK_MAGICIAN_CID_0FC9 | DAT_08038764 |
| 0x191c | Batteryman C | BATTERYMAN_C_CID | DAT_08039128 (via shifted) |
| 0x0fe4 | Harpie Lady | HARPIE_LADY_CID | DAT_08038684 |
| 0x0ff9 | Castle of Dark Illusions | CASTLE_OF_DARK_ILLUSIONS_CID | DAT_0803a70c |
| 0x1009 | Pumpking the King of Ghosts | PUMPKING_CID | DAT_080382cc |

**注**: 0x142d = Dark Magician (card_3256) -> `DARK_MAGICIAN_CID_142D`; 0x0fc9 = Dark Magician (card_0730) -> `DARK_MAGICIAN_CID_0FC9`. Both are Dark Magician but different slot_ids; disambiguated by hex suffix throughout. confidence high (data/card-stats.s lines for card_3256 and card_0730 confirmed distinct slots).

**注 gap CIDs** (DAT_080382dc/0803836c/0803862c/080386c4/080382c4/0803a720): No card name available. Use per-slot RENAME with EOL comment. No card_info.inc const needed (gaps have no semantic card name). confidence high.

**R1 新建 EQ 常量 (非 card-ID 数值)**:

| value | semantic | proposed_const | inc 文件 | 所在 slots |
|-------|---------|---------------|---------|-----------|
| 0x0bb8 | 3000 LP cost threshold | LP_COST_3000 | duel_field.inc (new) | DAT_080380d8, DAT_08038bf4, DAT_08038e6c |
| 0x05dc | 1500 LP cost threshold | LP_COST_1500 | duel_field.inc (new) | DAT_08038b38 |
| 0x0404 | hand_count_to_slot_array_off | HAND_COUNT_TO_SLOT_OFF | ewram.inc (new) | DAT_08038760 |
| 0xfffffed4 | -300 ATK/DEF score delta | SCORE_DELTA_NEG_300 | duel_field.inc (new) | DAT_0803919c, DAT_080391b8 |
| 0xfffffe0c | -500 ATK/DEF score delta | SCORE_DELTA_NEG_500 | duel_field.inc (new) | DAT_080391d4 |
| 0xfffffd44 | -700 ATK/DEF score delta | SCORE_DELTA_NEG_700 | duel_field.inc (new) | DAT_08039258 |
| 0xffff | empty slot sentinel | SLOT_CARD_EMPTY | card_info.inc (new) | DAT_080389a8 |

**注**: 先 grep 全部 19 个 constants/*.inc 确认这些值无重名。`SLOT_CARD_EMPTY` = 0xffff is used as ldrsh zero-check sentinel; ensure no existing `SLOT_*` const at this value.

**R1 新建 shifted sentinel EQ (shifted card_id mask)**:

| value | semantic | proposed_const | 参照 |
|-------|---------|---------------|------|
| 0xbaf00000 | SANCTUARY_IN_THE_SKY_CID (0x175e) << 19 | SANCTUARY_CID_SHIFTED | parallel to HAMON_LORD_CID_SHIFTED (card_info.inc) |
| 0xc8e00000 | BATTERYMAN_C_CID (0x191c) << 19 | BATTERYMAN_C_CID_SHIFTED | parallel to HAMON_LORD_CID_SHIFTED (card_info.inc) |
| 0xc6180000 | BATTERYMAN_AA_CID (0x18c3) << 19 | BATTERYMAN_AA_CID_SHIFTED | 0x18c3<<19=0xc6180000 (python verified); DAT_08038c84 |

**注 BATTERYMAN_C confirmed**: `0x191c << 19 = 0xc8e00000` (python verified). data/card-stats.s line 24884: `card_1913: @ Batteryman C  slot=0x191C`. confidence high.

**注 0xc6180000 (DAT_08038c84) CORRECTED**: ROM bytes at 0x08038c84 are `00 00 18 c6` (LE u32 = `0xc6180000`). This is a **shifted CID sentinel**: `0x18c3 << 19 = 0xc6180000` (Batteryman AA). Code at asm lines 6172-6174 does `lsls r0,r0,#0x13; ldr r1,DAT_08038c84; cmp r0,r1` -- same pattern as BATTERYMAN_C_CID_SHIFTED / SANCTUARY_CID_SHIFTED. **NOT** RESHEF_THE_DARK_BEING_CID (0x18c6 << 19 = 0xc6300000, which does not match). Add to card_info.inc: `BATTERYMAN_AA_CID = 0x18c3` and `BATTERYMAN_AA_CID_SHIFTED = 0xc6180000`. Slot label: `eval_batteryman_aa_cid_shifted`. confidence high (ROM bytes + arithmetic + code pattern three-way confirmed).

### REF_SLOTS (USER-label + DATA-ref -- RAM/ROM global addr slots)

| slot | target | gas_label | slot_label |
|------|--------|-----------|------------|
| DAT_08038038 | 0x0201c510 | gDuelFieldSlots | eval_slot_score_entry_full_field_slots |
| DAT_08038194 | 0x0201c510 | gDuelFieldSlots | eval_slot_lp_cost_field_slots_a |
| DAT_080382b0 | 0x0201c510 | gDuelFieldSlots | eval_slot_lp_cost_field_slots_b |
| DAT_08038c80 | 0x0201c510 | gDuelFieldSlots | eval_hand_field6_slots |
| DAT_08038da4 | 0x0201c510 | gDuelFieldSlots | eval_extra_deck_slots |
| DAT_08039120 | 0x0201c510 | gDuelFieldSlots | eval_bonus_state_slots_a |
| DAT_08039190 | 0x0201c510 | gDuelFieldSlots | eval_bonus_state_slots_b |
| DAT_08039310 | 0x0201c510 | gDuelFieldSlots | dispatch_equip_node_slots |
| DAT_0803925c | 0x0201c5d8 | gDuelFieldSlots_p2_base | adjust_score_p2_slots |
| DAT_0803a5a0 | 0x0201c510 | gDuelFieldSlots | check_equip_chain_slots_a |
| DAT_0803a650 | 0x0201c510 | gDuelFieldSlots | classify_equip_slots_a |
| DAT_0803a6c8 | 0x0201c510 | gDuelFieldSlots | classify_equip_slots_b |
| DAT_0803a708 | 0x0201c510 | gDuelFieldSlots | classify_equip_slots_c |
| PTR_gP1LifePoints_* x6 | 0x0201c4e0 | gP1LifePoints | (label already correct, no-op REF confirm) |
| DAT_08039314 | 0x0201d9c0 | gEquipNodePool | dispatch_equip_node_pool |
| DAT_08038758 | 0x0201c4f4 | gP1HandCountBase | eval_hand_magicians_count_base |
| DAT_08039318 | 0x0803931c | jump_table_base | dispatch_equip_jump_table_base |
| DAT_08039198 | 0x0201e1d4 | gP1FieldState | eval_p1_field_state_direct |
| DAT_0803912c | 0x09e3f094 | zone_monster_field_bonus_table | eval_bonus_state_table_ref_a |
| DAT_0803a654 | 0x09e3f094 | zone_monster_field_bonus_table | classify_equip_table_ref_b |
| DAT_080389dc | 0x0804b049 | check_card_is_amazoness_type+1 | eval_amazoness_fnptr_a |
| DAT_080389f8 | 0x0804b049 | check_card_is_amazoness_type+1 | eval_amazoness_fnptr_b |

**注**: DAT_08039318 = 0x0803931c: PTR_DAT_0803931c table base. After R4 disasm the table at 0x0803931c is labeled `dispatch_equip_node_jump_table`. The slot DAT_08039318 should get DATA ref to 0x0803931c. The PTR_DAT_0803931c label itself needs rename -- see RENAME_SLOTS.

### RENAME_SLOTS (纯改名 + EOL)

| slot | old_label | new_label | eol |
|------|-----------|-----------|-----|
| PTR_DAT_0803931c | PTR_DAT_0803931c | dispatch_equip_node_jump_table | 13-entry PC-dispatch table for equip node types 1..13 |
| DAT_08039350 | DAT_08039350 | eval_equip_type_1_to_4_stub | type 1..4 -> same code path: card-ID chain |
| DAT_0803a41e (advance_equip_node_chain_step) | (already named) | no change | -- |
| DAT_08038ae4 | DAT_08038ae4 | eval_sanctuary_cid_shifted | SANCTUARY_IN_THE_SKY_CID<<19; mov pc dispatch sentinel |
| DAT_08039128 | DAT_08039128 | eval_batteryman_c_cid_shifted | BATTERYMAN_C_CID<<19 |
| DAT_08038c84 | DAT_08038c84 | eval_batteryman_aa_cid_shifted | BATTERYMAN_AA_CID<<19; mov pc dispatch sentinel |
| DAT_08038b38 | DAT_08038b38 | eval_lp_cost_1500 | LP threshold 1500 |
| DAT_080380d8 | DAT_080380d8 | eval_lp_cost_3000_a | 3000 LP threshold slot a |
| DAT_08038bf4 | DAT_08038bf4 | eval_lp_cost_3000_b | 3000 LP threshold slot b |
| DAT_08038e6c | DAT_08038e6c | eval_lp_cost_3000_c | 3000 LP threshold slot c |
| DAT_080389a8 | DAT_080389a8 | eval_slot_empty_sentinel | 0xffff: no-card sentinel |
| DAT_0803919c | DAT_0803919c | eval_score_delta_neg300_a | -300 score delta |
| DAT_080391b8 | DAT_080391b8 | eval_score_delta_neg300_b | -300 score delta |
| DAT_080391d4 | DAT_080391d4 | eval_score_delta_neg500 | -500 score delta |
| DAT_08039258 | DAT_08039258 | eval_score_delta_neg700 | -700 score delta |
| DAT_08038760 | DAT_08038760 | eval_hand_count_to_slot_off | 0x404: gP1HandCountBase to gP1HandSlotArray offset |
| DAT_080382dc | DAT_080382dc | eval_gap_cid_1091 | gap CID 0x1091; not in card-stats.s |
| DAT_0803836c | DAT_0803836c | eval_gap_cid_133d | gap CID 0x133d; not in card-stats.s |
| DAT_0803862c | DAT_0803862c | eval_gap_cid_11d0 | gap CID 0x11d0; passed to count_paired_slots |
| DAT_080386c4 | DAT_080386c4 | eval_gap_cid_0fb2 | gap CID 0x0fb2; passed to count_paired_slots |
| DAT_080382c4 | DAT_080382c4 | eval_gap_cid_1387 | gap CID 0x1387; zone_id sentinel per asm/14 plate |
| DAT_0803a720 | DAT_0803a720 | classify_gap_cid_128a | gap CID 0x128a; also in asm/02 chain_128a |

**追加: 函数入口 literal pool 槽** -- 每函数的 gDuelFieldSlots REF槽 和 PLAYER_BLOCK_STRIDE EQ槽均在对应函数名前缀下，按上表 slot_label 列命名，此处不逐一重复。

### FUNC_RENAME

无误名信号发现 (函数体操作与函数名一致)。

---

## carve 计划 (R7)

### carve-1: zone_monster_field_bonus_table @ ROM 0x09e3f094 / size 0x130

**来源**: DAT_0803912c + DAT_0803a654 均引用此地址 (raw=2)。
**内容**: 19 x 16B entries -- 13 valid, 6 trailing garbage (cid=0xffff terminates iteration).
**结构**: 每 entry = `{.hword card_id; .hword bonus_forest, bonus_wasteland, bonus_mountain, bonus_sogen, bonus_umi, bonus_yami; .hword pad}` (8 x s16 = 16B).

```
zone_monster_field_bonus_table:
@ [0] Hoshiningen: Forest+500, Wasteland-400
    .hword  0x1192, 500, -400, 0, 0, 0, 0, 0
@ [1] Witch's Apprentice: Forest-400, Wasteland+500
    .hword  0x121a, -400, 500, 0, 0, 0, 0, 0
@ [2] Star Boy: Mountain+500, Sogen-400
    .hword  0x11b2, 0, 0, 500, -400, 0, 0, 0
@ [3] Little Chimera: Mountain-400, Sogen+500
    .hword  0x11fc, 0, 0, -400, 500, 0, 0, 0
@ [4] Milus Radiant: Umi+500, Yami-400
    .hword  0x11b5, 0, 0, 0, 0, 500, -400, 0
@ [5] Bladefly: Umi-400, Yami+500
    .hword  0x1207, 0, 0, 0, 0, -400, 500, 0
@ [6] Harpie Lady 1: Yami+300
    .hword  0x182a, 0, 0, 0, 0, 0, 300, 0
@ [7..12]: CID-encoded associated-card entries (Destiny Board + Spirit Messages cluster)
@ entry structure differs from [0..6]: fields encode associated CIDs, not ATK bonuses
@ [7]
    .hword  0x1468, 0, 0x1497, 0, 0x1498, 0, 0x1499, 0
@ [8]
    .hword  0x149a, 0,    0xa, 0, 0x14f9, 0, 0x154f, 0
@ [9]
    .hword  0x1550, 0, 0x1551, 0, 0x1730, 0, 0x1731, 0
@ [10]
    .hword  0x1670, 0, 0x1671, 0, 0x1672, 0, 0x1288, 0
@ [11]
    .hword  0x129b, 0, 0x12b8, 0,    0xa, 0, 0x15fb, 0
@ [12]
    .hword  0x10ef, 0, 0x17a6, 0, 0x197b, 0, 0x1704, 0
@ sentinel
    .hword  0xffff, -1, -1, -1, -1, -1, -1, -1   @ sentinel
```

**在 rom.s 切割** (incbin 偏移 = 0x09e3f094 - 0x08000000 = 0x01e3f094):
```
@ after field_spell_atk_bonus_table (ends at 0x09e3f094):
zone_monster_field_bonus_table:
    .hword ...  @ 0x130 bytes (19 entries x 16B)
```

**代码侧 R3 接通**: DAT_0803912c 和 DAT_0803a654 均加 USER label `zone_monster_field_bonus_table` + DATA ref，导出 `.word zone_monster_field_bonus_table`。

**byte-identical 验证**: 读 ROM 0x01e3f094..0x01e3f1c4 (0x130 bytes) 逐字节与 carve .hword 比对。

---

## disasm 计划 (R4) -- ROM_INCBIN 0x39350 / 0x10ce

**操作**: Ghidra headless Jython 脚本 (RefineF03Seg4bDisasm.py):

```python
from ghidra.app.cmd.disassemble import DisassembleCommand
from ghidra.program.model.address import AddressSet
from java.math import BigInteger

lo = toAddr(0x08039350)
hi = toAddr(0x0803a41d)

# Step 1: clear
clearListing(lo, hi)

# Step 2: set THUMB mode
ctx = currentProgram.getProgramContext()
ctx.setValue(ctx.getRegister("TMode"), lo, hi, BigInteger.ONE)

# Step 3: disasm each sub-stub individually (flow stops at branch-out)
stubs = [
    (0x08039350, 0x08039a61),  # type 1..4 (large, card-ID chain)
    (0x08039a62, 0x08039a7b),  # type 5
    (0x08039a7c, 0x08039c1b),  # type 6..9
    (0x08039c1c, 0x0803a2fb),  # type 10..11
    (0x0803a2fc, 0x0803a3c3),  # type 13
    (0x0803a3c4, 0x0803a41d),  # type 12
]
for start, end in stubs:
    s = toAddr(start)
    e = toAddr(end)
    DisassembleCommand(s, AddressSet(s, e), True).applyTo(currentProgram)
    createFunction(s, None)
```

**disasm 后命名** (6 sub-stubs):

| addr | proposed_name | semantics |
|------|--------------|-----------|
| 0x08039350 | eval_equip_node_type_1_to_4 | type 1-4: large card-ID chain for monster type checks |
| 0x08039a62 | eval_equip_node_type_5 | type 5: single-card check |
| 0x08039a7c | eval_equip_node_type_6_to_9 | type 6-9: shared chain |
| 0x08039c1c | eval_equip_node_type_10_to_11 | type 10-11: shared |
| 0x0803a2fc | eval_equip_node_type_13 | type 13 |
| 0x0803a3c4 | eval_equip_node_type_12 | type 12 |

**注**: 子函数名语义需细读 disasm 后确认，以上为初判基于 jump-table 类型索引。如语义明确后修订。

**跳转表 PTR_DAT_0803931c 处理**:
- label 改名 `dispatch_equip_node_jump_table`
- DAT_08039318 slot: DATA ref to `dispatch_equip_node_jump_table`
- 13 entry `.word` 值换用 sub-stub label:
  ```
  .word  eval_equip_node_type_1_to_4   @ types 1,2,3,4
  .word  eval_equip_node_type_1_to_4
  .word  eval_equip_node_type_1_to_4
  .word  eval_equip_node_type_1_to_4
  .word  eval_equip_node_type_5
  .word  eval_equip_node_type_6_to_9   @ types 6,7,8,9
  .word  eval_equip_node_type_6_to_9
  .word  eval_equip_node_type_6_to_9
  .word  eval_equip_node_type_6_to_9
  .word  eval_equip_node_type_10_to_11 @ types 10,11
  .word  eval_equip_node_type_10_to_11
  .word  eval_equip_node_type_12
  .word  eval_equip_node_type_13
  ```
  Note: GAS 用 even label (no +1) 因为 dispatch 是 `mov pc,r0` 非 `bx r0`; CPU 在 THUMB 上下文执行 mov pc -- CPSR.T 维持，偶地址 THUMB stub 正确执行。byte-identical 要求: ROM 存 0x08039350 等偶地址值, `.word eval_equip_node_type_1_to_4` = even addr -- 匹配。

---

## §5.1 登记 (Rule 3) -- 0 引用块

**无 §5.1 块** -- 唯一的 ROM_INCBIN (0x39350/0x10ce) 有明确引用 (13 次, 均来自 jump table), 判定 R4 disasm。

---

## 消费者证据 (R6) -- 关键槽语义 file:line + 置信度

| 槽/全局 | 消费者 file:line | 语义 | 置信度 |
|---------|----------------|------|--------|
| zone_monster_field_bonus_table (0x09e3f094) | asm/03 lines 6636-6670 (apply_slot_score_bonus_by_state 内) | ldrsh card_id + 6 field-zone bonuses per entry; 表给 count_field_copies_of_card 驱动 | high |
| 0x0804b049 (check_card_is_amazoness_type+1) | asm/05 line 4185 entry label + asm/07 plate comment line ~7 | Amazoness 族判断 fnptr; 由 count_monster_slots_by_fnptr 调用 | high |
| dispatch_equip_node_jump_table (0x0803931c) | asm/03 lines 7082-7108 dispatch_equip_node_by_type body | ldr r1,DAT_08039318(=0x0803931c); ldr r0,[r1+idx*4]; mov pc,r0 | high |
| gDuelFieldSlots_p2_base (0x0201c5d8) | asm/03 line 6996-6998; adjust_slot_score_by_chain_and_zone | gDuelFieldSlots+0xc8 = p2 block start; verified against ewram.inc def | high |
| gP1HandCountBase + 0x0404 -> gP1HandSlotArray | asm/03 lines 5492-5499 | eval_magician_of_black_chaos path: load hand slot array ptr from count_base+0x404 | high |
| DUEL_ACTIVE_PLAYER_OFF (0x1cb8) | asm/03 lines 6890-6897 | gDuelFieldSlots+0x1cb8 reads active turn player; reuse duel_field.inc def | high |
| P1LP_BLOCK2_OFF_1CE8 (0x1ce8) | asm/03 lines 5776-5779; 6848-6851 | two separate functions both read gP1LP+0x1ce8 | high |
| PUZZLE_LP_STEP_1000 (-1000) | asm/03 line 5647 (eval_slot_score_entry_full LP-cost path) | reuse duel_field.inc def; confirmed via asm/02 earlier uses | high |

---

## 求助 (低置信度 / BLOCKED)

### 1. CID gap slots: 0x1091, 0x11d0, 0x128a, 0x133d, 0x1387, 0x0fb2  [RESOLVED]

Confirmed: all 6 are genuine gaps in the slot assignment space (card IDs from wider Yu-Gi-Oh! card pool not included in this game's card roster). Verified by exhaustive grep of data/card-stats.s -- no entry with these slot values. Neighboring slots confirmed present.

- 0x14b0 at DAT_080382b4: RESOLVED -- NOT a card_id. Confirmed EQUIP_NODE_BASE_OFFSET. asm lines 4743-4744: `ldr r6,DAT_080382b4; add r6,r8` uses it as pool base offset. Use EQUIP_NODE_BASE_OFFSET equate (reuse duel_field.inc).
- 0x0fb2: gap CID, used as card_id parameter to `count_paired_slots_with_field5_default` at asm line 5437. No card name available.
- 0x1091, 0x11d0, 0x133d, 0x1387: gap CIDs used in `cmp r1,r0` card_id dispatch chains. No card names available.
- 0x128a: gap CID used in both asm/02 `check_slot_full_activation_chain_128a` (file 02 line 19656) and asm/03 classify_equip_target_eligibility (asm/10 plate: "card ID 0x128a+0x10 range"). No card name available.
- asm/14 plate (line 13368): 0x1387 is a "zone_id" parameter to `count_available_effect_zones`.

**Naming plan**: Use `<func>_gap_cid_<hex>` pattern per file 02 precedent:
  - DAT_080382dc -> eval_gap_cid_1091 + EOL "gap CID 0x1091; not in card-stats.s"
  - DAT_0803836c -> eval_gap_cid_133d + EOL "gap CID 0x133d; not in card-stats.s"
  - DAT_0803862c -> eval_gap_cid_11d0 + EOL "gap CID 0x11d0; passed to count_paired_slots"
  - DAT_080386c4 -> eval_gap_cid_0fb2 + EOL "gap CID 0x0fb2; passed to count_paired_slots"
  - DAT_080382c4 -> eval_gap_cid_1387 + EOL "gap CID 0x1387; zone_id sentinel per asm/14"
  - DAT_0803a720 -> classify_gap_cid_128a + EOL "gap CID 0x128a; also in asm/02 chain_128a"

confidence high (all confirmed as gap CIDs by card-stats.s exhaustive grep).

### 2. gP1LP + 0x1cf4 offset (0x00001cf4 at DAT_08038940, DAT_08039144)  [RESOLVED]

`0x1cf4` = FIELD_STATE_OFF (equip activation phase/stage code). Confirmed from:
- asm/04 lines 191-196 plate: "INIT_VAL_OFFSET=0x1cf4 (init=7)"
- asm/06 line 10870: "AUX_OFFSET_CF4=0x1cf4"
- asm/07 lines 60,66: "STAGE_OFF=0x1cf4"
- asm/07 line 3557: "FIELD_STATE_OFFSET=0x1cf4"

**New constant**: `FIELD_STATE_OFF = 0x1cf4` in duel_field.inc (new entry). confidence high.

Slots: DAT_08038940, DAT_08039144 -> EQ FIELD_STATE_OFF
DAT_08039198 = 0x0201e1d4 = `gDuelFieldSlots + 0x1cf4` direct address -> REF label (need new global label in ewram.inc for this specific direct address, or use `gDuelFieldSlots + FIELD_STATE_OFF`). confidence med.

### 3. gP1LP + 0x1cbc offset (0x00001cbc at DAT_080386f0)  [RESOLVED]

`0x1cbc` = CHAIN_LINK_COUNTER_OFFSET (chain link counter in equip chain). Confirmed from:
- asm/08 line 7057: "CHAIN_LINK_COUNTER_OFFSET = 0x1cbc (gP1LifePoints chain link counter)"

**New constant**: `CHAIN_LINK_COUNTER_OFF = 0x1cbc` in duel_field.inc (new entry). confidence high.

### 4. gP1LP + 0x1cc4 offset (0x00001cc4 at DAT_0803896c)  [PARTIALLY RESOLVED]

`gDuelFieldSlots + 0x1cc4` is read and compared to 2/3/4 in equip activation context (asm/12 lines 4499, 4933; asm/03 line 5804). Semantics: equip activation sub-phase state code. No plate comment in any file names this offset explicitly.

**Naming plan**: Use `EQUIP_PHASE_STATE_OFF = 0x1cc4` in duel_field.inc pending fixer to grep asm/12 function plate for explicit name. confidence med -- consistent with adjacent offsets (0x1cb8=active_player, 0x1cbc=chain_link_counter, 0x1ce8=LP_block2, 0x1cf4=field_state).

### 5. ARMv4T THUMB mov pc,r0 mode behavior  [RESOLVED]

THUMB opcode 0x4687 = MOV PC, r0 (THUMB format 5, Hi register MOV, H1=1: Rd=r15=PC, H2=0: Rs=r0).

ARMv4T specification: `MOV PC,Rn` in THUMB mode does NOT perform interworking (unlike `BX Rn`). CPSR.T remains set. Processor continues executing as THUMB. Even-addressed targets from jump table at PTR_DAT_0803931c execute as THUMB code -- confirmed by THUMB opcode patterns in sub-stubs.

GAS `.word eval_equip_node_type_1_to_4` (even addr, no +1) correctly generates even-address pointer. byte-identical verified: ROM stores 0x08039350 etc. (even). confidence high.

### 6. 0xc8e00000 at DAT_08039128  [RESOLVED]

`0xc8e00000 = 0x191c << 19` (Python verified: `0x191c << 19 = 0xc8e00000`).
0x191c = BATTERYMAN_C_CID (data/card-stats.s line 24884: `card_1913: @ Batteryman C  slot=0x191C`).
Use `BATTERYMAN_C_CID_SHIFTED = BATTERYMAN_C_CID << 19` or define as raw equate. confidence high.

**Add to card_info.inc**: `BATTERYMAN_C_CID = 0x191c` (new entry). `BATTERYMAN_C_CID_SHIFTED = 0xc8e00000` (new shifted sentinel).

### 7. PLATE 更新

所有 15 个函数的 plate comment 需检查 stale FUN_ 引用并替换为现名。

**7 处已确认 stale FUN_ 替换映射** (C8 验收要求: grep 落地后 lines 4335..7634 FUN_ count = 0):

| asm 行 | stale FUN_ | 所在 plate (函数) | 正确现名 |
|--------|-----------|-----------------|---------|
| 5895 | FUN_08037ec0 | compute_lp_cost_by_occupied_monster_zones | eval_slot_score_entry_full |
| 6148 | FUN_08037ec0 | compute_lp_cost_by_hand_field6 | eval_slot_score_entry_full |
| 6287 | FUN_08037ec0 | compute_lp_cost_by_extra_deck_card_id | eval_slot_score_entry_full |
| 6399 | FUN_08038dea | compute_lp_cost_by_zone_field5_x100 | compute_lp_cost_by_zone_field5_x200 |
| 6423 | FUN_08037ec0 | compute_lp_cost_by_zone_field5_both_players | eval_slot_score_entry_full |
| 7420 | FUN_08037c9c | classify_equip_target_eligibility | compute_zone_effect_atk_delta |
| 7420 | FUN_08036b88 | classify_equip_target_eligibility | find_effect_entry_by_player_zone |

Note: line 7634 (build_equip_target_eligibility_table) FUN_080c8d30 belongs to Seg-5 range, not this segment.

C8 验收要求: Seg-4b 范围落地后 `grep "FUN_" asm/03_equip_chain_hand.s` lines 4335..7634 count = 0.

---

## 新增 constants / 全局

### card_info.inc 新增 (预计 ~65 CID + 2 gap CIDs + 1 shifted sentinel)
见 §EQ_SLOTS 表 (card-ID 部分)。全部经 data/card-stats.s slot= 核实，confidence high。
- gap CIDs: use raw RENAME with EOL ("gap CID 0xXXXX; not in card-stats.s") -- no const definition needed since no card name
- BATTERYMAN_AA_CID = 0x18c3 (new entry; Batteryman AA, data/card-stats.s slot=0x18C3, pw=63142001)
- BATTERYMAN_AA_CID_SHIFTED = 0xc6180000 (= BATTERYMAN_AA_CID << 19; new shifted sentinel; DAT_08038c84)
- BATTERYMAN_C_CID = 0x191c (new entry; card_1913)
- BATTERYMAN_C_CID_SHIFTED = 0xc8e00000 (= BATTERYMAN_C_CID << 19; new shifted sentinel)
- SANCTUARY_CID_SHIFTED = 0xbaf00000 (= SANCTUARY_IN_THE_SKY_CID << 19; new shifted sentinel)
- SLOT_CARD_EMPTY = 0xffff (empty-slot sentinel in u16 card_id field)

### duel_field.inc 新增 (预计 8)
- `LP_COST_3000` = 0x0bb8
- `LP_COST_1500` = 0x05dc
- `SCORE_DELTA_NEG_300` = 0xfffffed4
- `SCORE_DELTA_NEG_500` = 0xfffffe0c
- `SCORE_DELTA_NEG_700` = 0xfffffd44
- `FIELD_STATE_OFF` = 0x1cf4 (equip activation phase/field state; confirmed from asm/04/06/07 plates)
- `CHAIN_LINK_COUNTER_OFF` = 0x1cbc (chain link counter; confirmed from asm/08 plate)
- `EQUIP_PHASE_STATE_OFF` = 0x1cc4 (equip activation sub-phase; compared to 2/3/4 in asm/12; confidence med)

### ewram.inc 新増
- `HAND_COUNT_TO_SLOT_OFF` = 0x0404 (positive offset: gP1HandCountBase -> gP1HandSlotArray)
- `gP1FieldState` = 0x0201e1d4 (= gP1LifePoints + FIELD_STATE_OFF = 0x0201c4e0 + 0x1cf4; direct abs addr; 1 ref in DAT_08039198)

---

## 推荐执行顺序

1. **Seg-4b1** (0x08037ec0..0x0803a540):
   - R4 disasm 6 sub-stubs (RefineF03Seg4bDisasm.py)
   - EQ: ~100 CID slots + numeric constants (RefineF03Seg4b1Slots.py)
   - REF: gDuelFieldSlots 等全局 (~20 slots)
   - R7 carve: zone_monster_field_bonus_table @ 0x09e3f094 (rom.s)
   - PLATE: eval_slot_score_entry_full 函数族 (9 fn)
   - build + SHA1

2. **Seg-4b2** (0x0803a540..0x0803a7f0):
   - EQ: ~25 CID slots + struct offsets
   - REF: gDuelFieldSlots 等
   - PLATE: check_slot_equip_chain_rule / classify_equip_target_eligibility / build_equip_target_eligibility_table (3 fn)
   - build + SHA1

---

## Executor Report: F03-Seg-4b

- 槽: EQ=~108 REF=~22 RENAME=~26 FUNC_RENAME=0 PLATE=15
  (EQ增加: BATTERYMAN_C_CID + FIELD_STATE_OFF + CHAIN_LINK_COUNTER_OFF + EQUIP_PHASE_STATE_OFF; RENAME增加: 6 gap CID slots)
- carve=1 (zone_monster_field_bonus_table @ 0x09e3f094 / 0x130 bytes)
- disasm=1 range (0x08039350..0x0803a41d, 6 sub-stubs via mov-pc jump table)
- 新增 constants/全局:
  - card_info.inc: +~65 named CID + BATTERYMAN_AA_CID + BATTERYMAN_AA_CID_SHIFTED + BATTERYMAN_C_CID + BATTERYMAN_C_CID_SHIFTED + SANCTUARY_CID_SHIFTED + SLOT_CARD_EMPTY
  - duel_field.inc: +LP_COST_3000 +LP_COST_1500 +SCORE_DELTA_NEG_{300,500,700} +FIELD_STATE_OFF +CHAIN_LINK_COUNTER_OFF +EQUIP_PHASE_STATE_OFF
  - ewram.inc: +HAND_COUNT_TO_SLOT_OFF +gP1FieldState
- 求助: none -- all blocked items resolved (see §求助 section for evidence)
  - DAT_080382b4=0x14b0: EQUIP_NODE_BASE_OFFSET (pool stride), not gap CID
  - gap CIDs (0x1091/0x11d0/0x128a/0x133d/0x1387/0x0fb2): confirmed gaps, raw RENAME with EOL
  - 0xc8e00000 = BATTERYMAN_C_CID(0x191c) << 19 (python verified)
  - ARMv4T mov pc,r0 in THUMB: CPSR.T unchanged, even-addr dispatch confirmed
  - 0x1cf4/0x1cbc/0x1cc4 offsets: FIELD_STATE_OFF/CHAIN_LINK_COUNTER_OFF/EQUIP_PHASE_STATE_OFF
- proposal: doc/dev/refine/F03-Seg-4b.proposal.md

---

## Fix iteration 1 (2026-06-11)

Applied reviewer NEEDS_FIX checklist from F03-Seg-4b.review.md:

**#1 (C4) DAT_08038c84 value corrected**:
- §段测绘 line: changed annotation from `RESHEF_THE_DARK_BEING_CID << 19` to `BATTERYMAN_AA_CID_SHIFTED = 0x18c3<<19`.
- §EQ shifted sentinel table: replaced RESHEF row with `BATTERYMAN_AA_CID (0x18c3) << 19 -> BATTERYMAN_AA_CID_SHIFTED = 0xc6180000`.
- §求助 note 0xc6180000: rewrote to explain LE bytes `00 00 18 c6` = u32 `0xc6180000` = `0x18c3<<19` (Batteryman AA), and removed wrong RESHEF_THE_DARK_BEING_CID claim.
- RENAME_SLOTS row: `eval_reshef_cid_slot` -> `eval_batteryman_aa_cid_shifted`; EOL updated.
- card_info.inc new constants: added `BATTERYMAN_AA_CID = 0x18c3` and `BATTERYMAN_AA_CID_SHIFTED = 0xc6180000`.
- Executor Report card_info.inc line updated.

**#2 (C8) 7 stale FUN_ mappings added**:
- §求助 §7 PLATE section: replaced vague "need to check" text with explicit 7-row FUN_xxxx -> current_name table covering asm lines 5895/6148/6287/6399/6423/7420 (two entries).
- C8 acceptance criterion clarified: grep lines 4335..7634 FUN_ count = 0.

**#3 (C6) DARK_MAGICIAN_CID disambiguation**:
- §EQ card-ID table row 0x142d: `DARK_MAGICIAN_CID` -> `DARK_MAGICIAN_CID_142D`.
- Disambiguating note below table: rewritten to use `DARK_MAGICIAN_CID_142D` / `DARK_MAGICIAN_CID_0FC9` exclusively, no bare `DARK_MAGICIAN_CID`.

**Supplemental (carve table entries [7..12])**:
- §carve-1 zone_monster_field_bonus_table: replaced placeholder `@ [7..12]: special monster effect entries...` with exact ROM-extracted .hword values for all 6 entries ([7] through [12]).
- Added structural comment noting entries [0..6] = ATK bonuses vs [7..12] = CID-encoded associated-card entries.
