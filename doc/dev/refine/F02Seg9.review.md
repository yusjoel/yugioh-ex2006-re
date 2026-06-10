# Refine Review: F02Seg9

> 段范围: `[0x08033654, 0x0803407c)`, 23 fn, 63 slots, 2 carve, 0 disasm, 0 §5.1
> proposal: `doc/dev/refine/F02Seg9.proposal.md`
> reviewer: 独立复核 (ref-scan / ROM 字节 / 残留计数全自主重跑)

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 | 段范围与 §五 路线图一致 | ✅ | Seg-8 end=0x08033654, Seg-9=[0x33654,0x3407c), Seg-10 start=0x3407c, 严格连续无跳号 |
| C2 | 每个 ROM_INCBIN/.byte 块有归宿 | ✅ | 段内 0 个 incbin 块; 2 个 carve 表嵌在 rom.s L1221 宿主 incbin 中 (被引用故 carve, 非静默保留) |
| C3 | §5.1 块确 0 引用 | ✅ N/A | 本段无 §5.1 登记; 两个 carve 表各有 1 raw ref (独立重跑 struct.pack 全 ROM 扫描确认) |
| C4 | EQ value == ROM 4 字节小端 | ✅ | 全部 63 个槽独立 python 读 ROM 字节核对: 63/63 匹配 (MISMATCH=0) |
| C5 | 新建常量前无可复用 | ✅ | 13 个新 EQUIP_* 常量扫全 19 个 constants/*.inc 无同值; SPATIAL_COLLAPSE_CARD_ID(Seg-8 已建) 正确复用 |
| C6 | 槽名格式合规无碰撞 | ✅ | 45+18=63 个 slot_label 全满足 `^[a-z][a-z0-9_]+$`, 无重复 label |
| C7 | carve/全局槽有 USER-label + DATA-ref 计划 | ✅ | DAT_08033670 → `.word monster_slot_order_table`; DAT_08033c40 → `.word available_slot_order_table`; 两处 carve 均在 proposal §carve 节明确写出 rom.s 切割 + 代码侧 RENAME |
| C8 | plate 引用全用现名, 无残留 FUN_ | ✅ | 3 个 ASCII 重写 plate 文本均无 `FUN_` 串; 当前 asm 文件已有 3 处 CJK plate 待替换 (plan 正确) |
| C9 | 所有 plate/EOL 文本纯 ASCII | ✅ | 3 个 plate 重写文本独立检查: 无 U+0080 以上字符; proposal 文档体 CJK 属中文说明 (doc/ 层级允许) |
| C10 | 指针表条目 +1 判断 | ✅ | 两表内容 [2,3,1,4,0] 均为槽 index (0-4), 非 GBA 地址; 无 0x08xxxxxx 模式; 正确用 `.word N` 不加 +1 |
| C11 | 函数体全局 vs 函数名矛盾 | ✅ | 抽查 9 个函数 plate: 名字与 plate 描述一致; 23 个函数名无语义矛盾信号; 无 FUNC_RENAME 遗漏 |
| C12 | 关键槽语义有 file:line + 置信度, 无零容忍词 | ✅ | 18 个关键槽均有 file:line (asm/02.s L1xxxx) + 置信度 high; 无零容忍词 |
| C13 | 段内全部残留自动名槽被覆盖 | ✅ | grep 实测 63 个 DAT_/DWORD_/PTR_ 定义; proposal EQ(45)+RENAME(18) 并集 = 63, 覆盖率 100% |

---

## 独立复核细节

### ref-scan (自主重跑, 不信 proposal)

```
monster_slot_order_table   (0x09e3ef4c): raw=1 @ [0x8033670], THUMB=0
available_slot_order_table (0x09e3ef60): raw=1 @ [0x8033c40], THUMB=0
```

两表均有且仅有 1 raw ref, 分别在段内代码中, 无 THUMB 引用. C3/C10 双重确认.

### carve 字节等式核对

```
host: .incbin "roms/2343.gba", 0x1E3DA18, 0xC2F4
split: 0x1534 + 0x14 + 0x14 + 0xAD98 = 0xC2F4  ✅
monster_slot_order_table  ROM offset: 0x1e3ef4c = host_off + 0x1534  ✅
available_slot_order_table ROM offset: 0x1e3ef60 = host_off + 0x1548  ✅
suffix start: 0x1e3ef74 (proposal: 0x1E3EF74)  ✅
```

### ROM 字节核对 (C4, 全 63 槽)

全部 63 个 slot 独立读 ROM 小端 4 字节: 63/63 `OK`, `MISMATCH=0`.

代表性核对:
- 0x080337d8 → 0x000013f2 (EQUIP_LOCKDOWN_CID) ✅
- 0x080337dc → 0x000013eb (EQUIP_ZONE_BLOCKER_CID) ✅
- 0x080338a4 → 0x00001874 (EQUIP_PAIR_RANGE_MAX) ✅
- 0x08033670 → 0x09e3ef4c (monster_slot_order_table) ✅
- 0x08033c40 → 0x09e3ef60 (available_slot_order_table) ✅

### C5 重复值扫描

扫描全 19 个 `constants/*.inc` 文件的 `.equ` 定义, 13 个新常量值均无已有条目. 复用常量:
- `PLAYER_BLOCK_STRIDE=0x868` (ewram.inc) ✅
- `gDuelFieldSlots=0x0201c510` (ewram.inc) ✅
- `gDuelFieldSlots_p2_base=0x0201c5d8` (ewram.inc, Seg-7 建) ✅
- `gP1HandSlotArray=0x0201c8f8` (ewram.inc, Seg-5 建) ✅
- `SPATIAL_COLLAPSE_CARD_ID=0x000016df` (card_info.inc, Seg-8 建) ✅

### C13 残留计数

`grep` asm/02_text_lp_fieldspell.s 段内 `DAT_|DWORD_|PTR_` 定义: **63 条**.
proposal EQ(45) ∪ RENAME(18) = **63 条**, 完全覆盖.

---

## 状态: PASS

## 修改清单

无修改项. Proposal 可直接进入 fixer 落地阶段.

### 落地注意事项 (reviewer 提示 fixer)

1. **card_info.inc 新建 13 个常量** 时需确认写入顺序不打乱现有结构; 建议在 Seg-8 注释块之后追加独立 `Seg-9 additions` 注释块.
2. **carve 落地**: rom.s L1221 宿主 incbin 切割为 4 spans; 切割后务必 `sum(spans)==0xC2F4` 并做 build + byte-identical SHA1 验收.
3. **3 个 plate ASCII 重写**: `setPlateComment` 整段覆盖 (非 substring replace); 写入后 readback re 扫描确认无非 ASCII 残留; 导出后 grep asm/02_text_lp_fieldspell.s 段范围无 CJK.
4. **EQUIP_LOCKDOWN_CID** 在 4 个槽中出现 (0x080337d8/0x080338dc/0x080339fc/0x08033a90); 第一个槽用 `createEquate` 建常量, 其余 3 个用 `setEquate` 复用同一常量.
