# Refine Review: F07-Seg-9  [0x08062d28..0x08063830)

> 本 review 由独立 reviewer 自主复核撰写，覆写 executor 自评。
> executor 自评无效 (memory: refine-fixer-overstep-self-review)。

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | OK | §三 Seg-8 ✅, Seg-9 ⬜ 确认下一段 |
| C2 Rule2 | 全部 ROM_INCBIN 有归宿 | OK | 3 块全部 R4 disasm; §5.1=0, carve=0 |
| C3 Rule3 | §5.1=0; 引用块确非 0 引用 | OK | 独立 ref-scan 重跑; 3 块均有 0x09e4xxxx handler table THUMB+1 引用 |
| C4 R1 值 | EQ value == ROM 4 字节小端 | OK | 50 槽全部 python 核对通过 (43 现有 + 7 disasm litpool) |
| C5 R1 复用 | 新建 4 CID 确无现有可复用 | OK | grep card_info.inc 0x1886/0x195f/0x188b/0x1918 全 0 命中; reuse 8 CID 确存在 |
| C6 R2 名 | 槽名 ^[a-z][a-z0-9_]+$, 无碰撞 | OK | 所有 EQ/RENAME/disasm-fn 名称格式合规 |
| C7 R3 接通 | carve/全局槽有 USER-label | N/A | 无 carve; 3 PTR_ 为 RENAME 型 (Seg-1..8 惯例) |
| C8 R5 现名 | 无残留 FUN_ | OK | grep 行 17403-18919 = 0 匹配 |
| C9 ASCII | plate/EOL 纯 ASCII | OK | asm 行范围 non-ASCII = 0; 3 plate 文本 python 验证全 ASCII |
| C10 carve | 无指针表 (+1 核) | N/A | 3 块均为 THUMB code disasm, 无数据指针表 |
| C11 误名 | 函数名无语义矛盾 | OK | 3 disasm 函数名与机器码语义一致 (见下详) |
| C12 R6 | 关键槽有 file:line + 置信度 | OK | 全部 high confidence; 消费者节逐一有证据 |
| C13 残留 | 43 自动名槽 100% 覆盖 | OK | python 精确清点 7 DAT_+33 DWORD_+3 PTR_=43; EQ40+RENAME3=43; missing=0, extra=0 |

---

## 详细核验记录

### C3: ref-scan 独立重跑

**Block A: 0x08062ebe / 0x3e**

```
raw(0x08062ebe) hits: 0
THUMB+1 hits for fn_start 0x08062ec0+1=0x08062ec1: [0x9e42358, 0x9e426e8, 0x9e42ce8]
THUMB+1 hits for mid-code 0x08062ee6+1=0x08062ee7: [0x883aef1]
```

3 real handler table hits confirmed:
- `0x9e42358`: [-12]=0x000017fd (ABSOLUTE_END_CID), [-8]=0x08071489, [-4]=0x00, [+0]=0x08062ec1, [+4]=0x00, [+8]=0x00 -- structure valid
- `0x9e426e8`: [-12]=0x00001886 (THREATENING_ROAR_CID), [-8]=0x08071489, [-4]=0x00, [+0]=0x08062ec1 -- structure valid
- `0x9e42ce8`: [-12]=0x0000195f (HERO_BARRIER_CID), [-8]=0x0807d701, [-4]=0x00, [+0]=0x08062ec1 -- structure valid

4th hit at 0x883aef1: context[-4]=0xdffc0028 (not a valid CID, not a GBA ROM address) -> confirmed compression artifact, not a real handler table reference.

**Block B: 0x08062f38 / 0x28**

```
raw(0x08062f38) hits: 0
THUMB+1 hits for fn_start 0x08062f38+1=0x08062f39: [0x9e42760]
```

Hit at `0x9e42760`: [-12]=0x0000188b (D_D_DYNAMITE_CID), [-8]=0x080655ed, [-4]=0x00, [+0]=0x08062f39, [+4]=0x00, [+8]=0x08081db1 -- structure valid.

Note: proposal line 105 states `fn_next=0x08061db1` but actual ROM byte at [+8] = `0x08081db1`. This is a transcription typo in the proposal (6 vs 8 in 5th hex digit). Non-blocking: CID and fn_elig are correct and classification is unaffected.

**Block C: 0x080636f8 / 0x38**

```
raw(0x080636f8) hits: 0
THUMB+1 hits for fn_start 0x080636f8+1=0x080636f9: [0x9e45268]
```

Hit at `0x9e45268`: [-12]=0x00001911 (CYBER_ARCHFIEND_CID), [-8]=0x0807c7f1, [-4]=0x00, [+0]=0x080636f9, [+4]=0x00, [+8]=0x00 -- structure valid.

All 3 blocks: raw=0, confirmed handler table THUMB+1 refs -> R4 disasm, §5.1=0. C3 PASS.

### C4: ROM 字节核对 (50 槽)

Python `struct.unpack_from('<I', data, addr-base)` 验证全部 50 槽 (43 现有 + 7 disasm litpool):

- 43 现有槽: 全部 OK (包含 3 PTR_gP1LifePoints_ 槽值 = 0x0201c4e0)
- 7 disasm litpool: 0x08062edc=0x0201c4e0, 0x08062ee0=0x00001ce8, 0x08062ef8=0x00001cf4, 0x08062f58=0x0201c4e0, 0x08062f5c=0x00000868, 0x08063724=0x0201c4e0, 0x08063728=0x00000868 -- 全部 OK

### C4 附: 机器码关键指令独立解码

**Block A (`check_opp_active_player_duel_phase_leq3`):**

| 地址 | 机器码 | 解码 | 验证 |
|------|--------|------|------|
| 0x08062ec0 | 0x4b06 | ldr r3,[pc,#0x18] -> target=0x08062edc (gP1LifePoints) | OK |
| 0x08062ec2 | 0x4907 | ldr r1,[pc,#0x1c] -> target=0x08062ee0 (P1LP_BLOCK2_OFF_1CE8) | OK |
| 0x08062ec6 | 0x7880 | ldrb r0,[r0,#2] (imm5=2) | OK |
| 0x08062ece | 0x1a09 | subs r1,r1,r0 -> r1=1-player_id=opp_player | OK |
| 0x08062ed4 | 0xd006 | beq target=0x08062ee4 | OK |
| 0x08062ed8 | 0xe00c | b target=0x08062ef4 (bx lr, return 0) | OK |
| 0x08062eec | 0x2803 | cmp r0,#3 | OK |
| 0x08062eee | 0xd800 | bhi target=0x08062ef2 (phase>3 -> adds r0,r0,r1; r1=0 -> return 0) | OK |
| 0x08062ee6 | 0x4a04 | ldr r2,[pc,#0x10] -> target=0x08062ef8 (FIELD_STATE_OFF) | OK |
| 0x08062ef4 | 0x4770 | bx lr | OK |

名称 `leq3` 与 bhi (taken if >3) 方向一致: 未 taken (phase<=3) 返回 1。

**Block B (`check_opp_alt_hand_count_nonzero_for_cid_188b`):**

| 地址 | 机器码 | 解码 | 验证 |
|------|--------|------|------|
| 0x08062f38 | 0x4a07 | ldr r2,[pc,#0x1c] -> target=0x08062f58 (gP1LifePoints) | OK |
| 0x08062f3a | 0x7880 | ldrb r0,[r0,#2] | OK |
| 0x08062f42 | 0x4048 | eors r0,r1 (bits[9:6]=0001=EOR, NOT AND) -> r0=player_id XOR 1=opp | OK |
| 0x08062f44 | 0x4905 | ldr r1,[pc,#0x14] -> target=0x08062f5c (PLAYER_BLOCK_STRIDE) | OK |
| 0x08062f46 | 0x4348 | muls r0,r1 -> opp*0x868 | OK |
| 0x08062f48 | 0x321c | adds r2,#0x1c -> r2=gP1LP+0x1c=gP1AltHandCountBase | OK |
| 0x08062f50 | 0xd000 | beq target=0x08062f54 (bx lr, return 0) | OK |
| 0x08062f54 | 0x4770 | bx lr | OK |

0x4048 = EOR 确认: ALU op bits[9:6]=0001=EOR (0000=AND). 函数读 OPPONENT 的 banished 区计数。

**Block C (`check_zone_non_field_type_or_has_monsters_for_cid_1911`):**

| 地址 | 机器码 | 解码 | 验证 |
|------|--------|------|------|
| 0x080636fc | 0x0100 | lsls r0,r0,#4 -> r0=0xfc<<4=0xfc0 (ZONE_TYPE_MASK) | OK |
| 0x080636fe | 0x8859 | ldrh r1,[r3,#2] (imm5=1, offset=imm5*2=2) -> slot[+2] | OK |
| 0x08063704 | 0x0049 | lsls r1,r1,#1 -> r1=0xa0<<1=0x140 (FIELD_ZONE_TYPE) | OK |
| 0x08063708 | 0xd110 | bne target=0x0806372c (zone_type!=0x140 -> return 1) | OK |
| 0x0806370a | 0x4a06 | ldr r2,[pc,#0x18] -> target=0x08063724 (gP1LifePoints) | OK |
| 0x08063712 | 0x4905 | ldr r1,[pc,#0x14] -> target=0x08063728 (PLAYER_BLOCK_STRIDE) | OK |
| 0x08063716 | 0x320c | adds r2,#0x0c -> r2=gP1LP+0x0c=gP1ZoneHandCount base | OK |
| 0x0806371e | 0xd006 | beq target=0x0806372e (monster_count=0 -> return 0) | OK |
| 0x08063722 | 0xe004 | b target=0x0806372e (fall-through to bx lr) | OK |
| 0x0806372e | 0x4770 | bx lr | OK |

ldrh slot[+2] offset=imm5*2=1*2=2 确认; 与 Seg-9 asm lines 17523/18215/18288/18339 一致。

### C5: CID 双向核

**新建 (4):** grep `card_info.inc` 精确值 0 命中:
- 0x00001886 -> 0 hits; card-stats.s L23376 `Threatening Roar slot=0x1886 pw=36361633` 坐实
- 0x0000195f -> 0 hits; card-stats.s L54103 (L25560) `Hero Barrier slot=0x195F pw=44676200` 坐实
- 0x0000188b -> 0 hits; card-stats.s L23441 `D.D. Dynamite slot=0x188B pw=08628798` 坐实
- 0x00001918 -> 0 hits; card-stats.s L24832 `Des Frog slot=0x1918 pw=84451804` 坐实

**Reuse (8+) 确认存在:** ABSOLUTE_END_CID(0x17fd), CYBER_ARCHFIEND_CID(0x1911), RING_OF_MAGNETISM_CID(0x1318), PROTECTOR_OF_SANCTUARY_CID(0x178b), DARK_RULER_VANDALGYON_CID(0x190a), TADPOLE_CID(0x1919), POLYMERIZATION_CID(0x12e5), BANISHER_OF_THE_LIGHT_CID(0x1332) -- 全部在 card_info.inc 有对应行。

### C11: 函数名语义核

- `check_opp_active_player_duel_phase_leq3`: 机器码 bhi (phase>3 -> return 0, phase<=3 -> return 1) + eop is active player 判断。名称准确。
- `check_opp_alt_hand_count_nonzero_for_cid_188b`: 0x4048=EOR -> opp player; adds r2,#0x1c -> gP1AltHandCountBase; ldr+cmp r0,#0 -> nonzero=1。名称与机器码一致。
- `check_zone_non_field_type_or_has_monsters_for_cid_1911`: bne (zone_type!=0x140 -> return 1); if 0x140: check gP1LP+player*0x868+0x0c (gP1ZoneHandCount) nonzero -> return 1。名称与逻辑一致。

FUNC_RENAME=None 无误。

### C13: 穷举对账

Python 宽化正则 `^(DAT_|DWORD_|PTR_)` 扫行 17403-18919:
- DAT_: 7 个 (08062de8/08062df0/080632f0/080636ec/08063784/08063788/080637b4)
- DWORD_: 33 个
- PTR_: 3 个 (PTR_gP1LifePoints_08062dec/080632ec/08063780)
- 合计: 43

Proposal EQ 表: 40 槽 (43 - 3 PTR_); RENAME 表: 3 PTR_ 槽。总集 = 43 = asm 清点数。missing=0, extra=0。越界: 最低 0x08062de8 >= Seg-9 start 0x08062d28, 最高 0x08063810 < Seg-9 end 0x08063830。全部 OK。

---

## 发现的问题

### 非阻塞 -- 提案注释拼写错误

**Block B ref-scan 上下文 (proposal 第 105 行):** fn_next 值标注为 `0x08061db1`, 但 ROM 实际读值为 `0x08081db1` (6→8 的一位打字错误)。该值仅为 ref-scan 上下文记录, 不影响 CID(0x188b)、fn_elig(0x08062f39)、分类(disasm R4) 的任何核心结论。

**可选修正:** fixer 可在落地后顺手在 proposal 中将 `fn_next=0x08061db1` 改为 `fn_next=0x08081db1`, 但不是必须。

---

## 状态: PASS

所有 C1-C13 全部通过。无阻塞问题。

---

## Reviewer 独立复核总结

1. **ref-scan 自主重跑**: 3 块均独立穷举 raw + THUMB+1, 结果与 proposal 主体一致。mid-code 第 4 hit (0x883aef1) 经上下文 ([-4]=0xdffc0028) 确认为压缩偶合非真引用。
2. **机器码独立解码**: Block A 分支方向 (bhi phase>3 -> return 0) / Block B EOR 0x4048 / Block C ldrh offset=2 全部机器码自算确认, 与 proposal 一致。
3. **ROM 字节核对**: 50 槽全部 python 读值核实, 无误差。
4. **CID 身份**: 4 新 CID 均有 card-stats.s 行号锚定。
5. **C13**: 宽化正则精确清点 43 槽, EQ+RENAME=43=43, 无遗漏无越界。
6. **C8/C9**: 段内 asm 无 stale FUN_, 无 CJK/非 ASCII。
7. **唯一发现**: proposal 行 105 fn_next 值小笔误 (0x08061db1→0x08081db1), 非阻塞。

**Fixer 可直接进入 mode B (落地)**。
