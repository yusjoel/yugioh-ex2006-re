# Refine Review: F03-Seg-5

> 段范围 0x0803a7f0..0x0803b3a8 | 审核日期 2026-06-12 (fix iter 1 re-review)
> proposal: doc/dev/refine/F03-Seg-5.proposal.md

---

## 核验矩阵 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|------|------|------|
| C1 Rule1 | 段范围与路线图一致 | ✅ | refine-progress.md 下一任务 = F03 Seg-5 (0x3a7f0..0x3b3a8); proposal 头行一致; 无跳号/回头 |
| C2 Rule2 | 每个 ROM_INCBIN/.byte 块都有归宿 | ✅ | 唯一块 0x3b24e/0x66 -> §5.1 (独立 ref-scan 0 refs); get_zone_slot_ptr 13 个函数已覆盖 |
| C3 Rule3 | §5.1 块确 0 引用 | ✅ | 独立重跑: d.count(pack('<I',a)) + d.count(pack('<I',a|1)) for all even a in [0x3b24e,0x3b2b4) -> 0 hits; wide-scan 4B-aligned 亦 0 |
| C4 R1 值 | 每个 EQ slot == ROM 4B 小端 | ✅ | 独立 python 核对: 全 11 个新槽 (b30c/b310/b324/b328/b33c/b340/b354/b358/b380/b3a0/b3a4) + 10 原有代表槽 全部 OK |
| C5 R1 复用 | 新建 8 个常量前确无现有同值 | ✅ | grep constants/ 全目录: 0x15e3/0x12a1/0x1357/0x15ae/0x183b/0x145b/0x171f/0xb8f80000 全 0 命中 |
| C6 R2 名 | 槽名 ^[a-z][a-z0-9_]+$, 无碰撞 | ✅ | 34 个槽标签 (31 REF + 3 RENAME) 全部通过正则; 无重复; abac/ad80 已从 REF_SLOTS 删除, RENAME_SLOTS 独占 |
| C7 R3 接通 | carve/全局槽有 USER-label + DATA-ref 计划 | ✅ | DAT_0803b2cc (ROM table ptr) 在 REF_SLOTS 有 slot_label; 所有 EQ/REF 槽均有命名计划 |
| C8 R5 现名 | 无残留 stale FUN_ | ✅ | grep asm lines 10171..11740 (含 get_zone_slot_ptr 全体): FUN_ = 0 hits |
| C9 ASCII | plate/EOL 纯 ASCII | ✅ | 3 条 RENAME EOL 文本逐字符检验全 ASCII; proposal 正文中文在 doc/ 可接受 |
| C10 carve | 指针表 THUMB fn-ptr +1 | ✅ | DAT_0803aa74 = 0x0803777d (奇地址 THUMB+1), ROM 字节 7d 77 03 08 确认 |
| C11 误名 | 函数名与体语义无矛盾 | ✅ | 13 个函数名全部复核; get_zone_slot_ptr 体: 纯地址计算, 无副作用; 名字与体一致; 无误名信号 |
| C12 R6 | 关键槽语义有 file:line + 置信度证据 | ✅ | 消费者节 10 条: 均有 asm 行号 + card-stats.s 槽号坐实; med-conf 2 条 (1-ref 地址推导) 有明确计算证据 |
| C13 残留 | 段内所有 DAT_ 槽 100% 覆盖 | ✅ | 独立 grep asm: [0x3a7f0,0x3b3a8) 内 DAT_ 标签 = 79; proposal EQ(45)+REF(31)+RENAME(3) = 79; 无地址重复 |

---

## 独立核验记录

### C3 ref-scan (自跑)

```python
d = open('roms/2343.gba','rb').read()
block_start = 0x0803b24e; block_end = 0x0803b2b4
hits = []
for a in range(block_start, block_end, 2):
    raw   = d.count(struct.pack('<I', a))
    thumb = d.count(struct.pack('<I', a|1))
    if raw > 0 or thumb > 0: hits.append((hex(a), raw, thumb))
# -> hits = []  (0 references, confirmed)
# Wide-scan 4B-aligned: also 0 hits
```

### C4 ROM 值核对 (11 新槽全量 + 原有 10 槽抽查)

```
0x803b30c: 0x00000868 OK   0x803b310: 0x0201c740 OK
0x803b324: 0x00000868 OK   0x803b328: 0x0201c8f8 OK
0x803b33c: 0x00000868 OK   0x803b340: 0x0201cab0 OK
0x803b354: 0x00000868 OK   0x803b358: 0x0201c600 OK
0x803b380: 0x0201bc54 OK   0x803b3a0: 0x00000868 OK
0x803b3a4: 0x0201c510 OK
(原有) aa74=0x803777d / aa78=0x201d9c0 / abac=0x201c5e8
       ad80=0x201c574 / b030=0xb8f80000 / b2cc=0x803b2d0 全 OK
```

### C6 label 检查

34 个槽标签全部匹配 `^[a-z][a-z0-9_]+$`; 无重复地址; abac/ad80 仅在 RENAME_SLOTS 出现 (REF_SLOTS 已删除).

### C13 独立计数

独立 grep asm/03_equip_chain_hand.s 正则 `^(DAT_|DWORD_|UNK_|PTR_DAT_)(08[0-9a-fA-F]{6})` 在地址 [0x3a7f0,0x3b3a8) 命中 **79** 个. EQ(45)+REF(31)+RENAME(3) = 79. 无遗漏.

### C5 dedup

grep constants/ 全目录: 8 个新建 card_info.inc 常量值全部 0 命中. 安全.

---

## 状态: PASS

所有 3 项 fix 均已正确落地:

1. **C2/C13 resolved**: get_zone_slot_ptr (0x0803b2b4) 已作为第 13 函数加入函数表; 11 个字面量池槽 (b30c/b310/b324/b328/b33c/b340/b354/b358/b380/b3a0/b3a4) 全部入 master slot table 并分类为 EQ/REF 复用; ROM 值独立核对全通过; 总覆盖 79/79.
2. **C6 resolved**: DAT_0803abac 和 DAT_0803ad80 仅出现在 RENAME_SLOTS (各 1 次), REF_SLOTS 对应行已删除; 无重复标签; query_state_code_magic_zone_p0_base 标签统一.
3. **计数 reconciled**: EQ=45 REF=31 RENAME=3 total=79; 自检节算式正确; Executor Report 已更新.

无回归: C1 bounds 全在 [0x3a7f0,0x3b3a8); C3 §5.1 0-ref 成立; C5 无新冲突; C8 FUN_=0; C9 全 ASCII.
