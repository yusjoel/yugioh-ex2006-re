# Refine Review: F03-Seg-7

范围: `asm/03_equip_chain_hand.s` 0x0803bba4..0x0803c774  
reviewer: 独立复核 (不信 executor 结论，自主 ref-scan + ROM 字节核对)  
review iteration: 2 (after fix-iter-1)

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与 §五 路线图一致 | ✅ | 活动 doc §五 Seg-7=0x3bba4..0x3c774 完全吻合; Seg-6 PASS 在 0x3bba4 结束; Seg-8 从 tick_equip_chain_slot_ref_scan_seq@0x3c774 (asm line 14346) 开始; 无越界 |
| C2 Rule2 | 每个 ROM_INCBIN 块都有归宿 | ✅ | 段内仅 1 个 ROM_INCBIN @ 0x3be38/0x14; 归入 §5.1; 合规 |
| C3 Rule3 | §5.1 块确 0 引用 | ✅ | **独立重跑 ref-scan**: raw 0x0803be38=0 refs; THUMB+1 0x0803be39=0 refs; 块内所有 2B 对齐地址均无 raw 或 THUMB+1 引用 |
| C4 R1 值 | 每个 EQ value == ROM 4 字节小端 | ✅ | DAT_0803bd00 ROM 值独立核对 = 0x00001d4c; 现在正确映射为新建 ACTIVATION_STATE_C_OFF=0x1d4c (非 ACTIVATION_STATE_A_OFF=0x1d48); 其余 54 个 slot 值全部匹配 |
| C5 R1 复用 | 新建常量前确无现有可复用 | ✅ | (1) 0x814 → 复用 DUEL_FIELD_OAM_TILE_IDX_A (duel_field.inc line 80) ✓; (2) 0xfff → 复用 SCENE_SLOT_MASK_LO (duel_field.inc line 56) ✓; (3) ACTIVATION_STATE_C_OFF=0x1d4c 独立 grep 全 19 constants/*.inc 确认无同值 ✓; 5 new duel_field.inc offsets (0x808/0x80c/0x1d10/0x1d38/0x1d4c) 全部 grep 确认无冲突 ✓; 1 new card_info.inc (0x1846) grep 确认无冲突 ✓; 2 sprite offsets (0x306/0x30a) grep 确认无冲突 ✓ |
| C6 R2 名 | 槽名 `^[a-z][a-z0-9_]+$`, 无碰撞 | ✅ | RENAME label dispatch_event_switch_table_ptr 合规; 28 个 REF slot label 均通过格式检查; 8 个新建常量名均通过 `^[A-Z][A-Z0-9_]+$` 检查; 无重复 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | ✅ N/A | 段内无 carve; 28 个 REF 槽各有 slot_label + 对应全局名 |
| C8 R5 现名 | plate 引用全用现名, 无残留 FUN_ | ✅ | 独立 grep asm lines 12838..14327 得 FUN_ 出现 8 处; proposal fix-iter-1 后 PLATE=8 完整覆盖所有 8 处 (lines 12931/13101/13191×2/13791/14003/14028/14188/14268); line 14328 属 Seg-8 (> Seg-7 上界 14327) 正确排除; FUN_ 后缀均有对应现名 |
| C9 ASCII | plate/EOL 文本纯 ASCII | ✅ | proposal 中 ASCII 替换板文本 (lines 333-347) 独立字节验证全 ASCII; 已有 CJK 板 (asm line 12931) 已计划 setPlateComment 全文替换为 ASCII; proposal 自身文档中的 CJK 为 doc/ 中文说明，合规 |
| C10 carve | 指针表条目 `+1` (THUMB) | ✅ N/A | 段内无函数指针表 carve; switch table ptr 指向同段内 ROM 数据非 THUMB fn-ptr |
| C11 误名 | 函数体全局 vs 函数名无矛盾 | ✅ | 抽查 dispatch_duel_event_display_seq / tick_duel_anim_event_hub / tick_equip_chain_link_display_seq: 函数体操作与名称语义一致; 无 FUNC_RENAME 信号 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据, 无零容忍词 | ✅ | BALLISTA_OF_RAMPART_SMASHING_CID=0x1846 由 data/card-stats.s card_4305 坐实 (pw=00242146); gDuelDisplaySeqState/gSpriteAttrBuf 有 178/52 raw refs + plate 佐证; ACTIVATION_STATE_C_OFF 有 asm 13044 read + ==0 check before play_ui_effect(0x31/0x32) 证据; 无零容忍词 |
| C13 残留 | 段内所有残留自动名槽均已覆盖 | ✅ | 独立 grep: asm lines 12838..14327 内 DAT_/PTR_ 定义总数=56; EQ(27)+REF(28)+RENAME(1)=56; 全覆盖 |

---

## 独立复核记录

### C3 ref-scan 重跑

```
python -c "
import struct
d = open('roms/2343.gba','rb').read()
raw=0x0803be38; thumb=raw|1
print(d.count(struct.pack('<I',raw)))   # 0
print(d.count(struct.pack('<I',thumb))) # 0
# all intermediate 2B-aligned addrs: 0 matches
"
```

结论: §5.1 判定有效，raw=0 THUMB=0。

### C4 独立字节核对 (fix-iter-1 重核)

```
python -c "
import struct
d = open('roms/2343.gba','rb').read()
addr = 0x0803bd00
off = addr - 0x08000000
v = struct.unpack('<I', d[off:off+4])[0]
print('0x%08x => 0x%08x' % (addr, v))  # => 0x00001d4c
"
```

ROM 值 = 0x00001d4c。现在正确归为新建 ACTIVATION_STATE_C_OFF=0x1d4c，不再错误复用 ACTIVATION_STATE_A_OFF=0x1d48。

### C5 独立扫描 (fix-iter-1 重核)

- `grep -r "0x1d4c" constants/` → 无命中 (仅 rom_data.inc 中 0x0981D4CA 为不同值)
- `grep -r "equ.*0x00001d4c" constants/` → 无命中
- ACTIVATION_STATE_A_OFF=0x1d48 (line 172), ACTIVATION_STATE_B_OFF=0x1d78 (line 174): 均与 0x1d4c 不同
- DUEL_FIELD_OAM_TILE_IDX_A=0x814 (duel_field.inc line 80): 复用确认 ✓
- SCENE_SLOT_MASK_LO=0xfff (duel_field.inc line 56): 复用确认 ✓
- 0x808/0x80c/0x1d10/0x1d38/0x306/0x30a/0x1846: 全部 grep 确认无现有 .equ 定义

### C8 FUN_ 完整清单 (fix-iter-1 重核)

独立 awk asm lines 12838..14327 统计 FUN_ 行:

| asm 行 | 所属函数 plate | FUN_ | fix-iter-1 后 |
|--------|--------------|------|--------------|
| 12931 | check_card_play_condition_eligible | FUN_080c9f50 | ✅ 已覆盖 (全文 ASCII 改写) |
| 13101 | write_sprite_attrs_to_seq_buf | FUN_08094c10 | ✅ 已覆盖 |
| 13191 | dispatch_duel_event_display_seq | FUN_0803c318, FUN_0803c3b4 | ✅ 已覆盖 |
| 13791 | tick_duel_anim_event_hub | FUN_0803c318 | ✅ 已覆盖 |
| 14003 | tick_display_op09_seq | FUN_0803be4c | ✅ 已补加 |
| 14028 | tick_equip_chain_link_display_seq | FUN_0803be4c | ✅ 已补加 |
| 14188 | tick_equip_set_display_sequence | FUN_0803be4c | ✅ 已补加 |
| 14268 | tick_equip_candidate_scan_with_display | FUN_0803be4c | ✅ 已补加 |

line 14328 (tick_equip_chain_slot_ref_scan_seq plate, Seg-8 函数) 正确排除于 Seg-7 范围外。

PLATE 总数 = 8; 目标: 落地后 grep FUN_ in lines 12838..14327 == 0 hits。

### C13 残留计数

```
awk 'NR>=12838 && NR<=14327' asm/03_equip_chain_hand.s | grep -cE '^(DAT_|PTR_)'
# => 56
```

EQ(27) + REF(28) + RENAME(1) = 56. 全覆盖。

---

## 状态: PASS

所有 4 条 NEEDS_FIX 已在 fix-iter-1 中正确解决:
1. C4 DAT_0803bd00=0x1d4c → 新建 ACTIVATION_STATE_C_OFF ✅ (ROM 独立验证 0x1d4c 确认)
2. C5 DAT_0803c528=0x814 → 复用 DUEL_FIELD_OAM_TILE_IDX_A; DAT_0803be80=0xfff → 复用 SCENE_SLOT_MASK_LO ✅
3. C8 PLATE=8 (补加 4 个 FUN_0803be4c→dispatch_duel_event_display_seq at lines 14003/14028/14188/14268) ✅
4. BALLISTA_OF_RAMPART_SMASHING_CID=0x1846 维持 ✅

C1-C13 全部 ✅，无回归。
