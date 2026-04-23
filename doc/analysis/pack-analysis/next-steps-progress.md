# §六 下一步计划 — 静态执行进度

**日期**: 2026-04-16
**接续**: `README.md` §六

## 已尝试

### A. ROM 中静态定位 `pack_cost_table`

脚本: `tools/ad-hoc/find_pack_cost_table.py`, `find_pack_record.py`

- 全 ROM 搜 u16=`0x05DC` (1500): 共 **611 处**
- 试以 0x05DC 为表头扫连续 50 项 plausible u16 cost (整百, 100..50000): **0 命中**
- 试 record 数组结构 (record_size R=4..64, cost 在 offset 0): 大量 **假阳性集中在 `card-stats.s` 区域 (R=22, ROM 0x0181..0x0183)** — 因为 ATK/DEF 数值范围与 cost 重合
- 试在已知 "未结构化" 段 `0x1DFF9D2-0x1E58D0E`: 4 处, 但都是 ROM 代码指针的中段字节 (e.g. `0x0805DC01`), 非 cost

**结论**: 未能锁定 pack cost 表. 推测原因:
1. Pack cost 不一定按 plausible 整百倍数存储 (可能 1500/1200/1500/1000/2000 等任意值)
2. 可能 pack 数据是 struct 数组, cost 不在 offset 0
3. 或 cost 按位字段编码而非 plain u16

### B. ROM 中静态定位 pack name 字符串引用

- "LEGEND OF B.E.W.D" 在 ROM 出现 4 处:
  - `0x09DCBCDC` (EN), `0x09DCC10C` (EN 第二份), `0x09DD76F4` (DE), `0x09DD7B1A` (FR)
- 全 ROM 搜 u32 指针指向上述 4 个地址: **0 处**
- 全 ROM 搜 ≥64 项连续 string-pointer 表: **未找到**

**结论**: 字符串通过 **ID-索引顺序遍历** 访问 (无 flat pointer table). 无法用纯字符串地址反查 pack 数据结构.

### C. 卡牌库存 SRAM 编码反推

- 假设 SRAM `0x0E000008` 起为 packed-nibble (每字节 2 张卡 × 4 位计数), 起始 slot_id = 0x0FA7 (Blue-Eyes White Dragon)
- state1→state7 4 个字节 diff 推断的 slot_id (低/高 nibble 两种解释):
  - 低 nibble 解释: slot_ids 0x1203 (Liquid Beast), 0x129B (Beta The Magnet Warrior), 0x138B (Alligator's Sword Dragon), 0x1443 (无)
  - 高 nibble 解释: 0x1204 (Twin Long Rods #2), 0x129C (Big Shield Gardna), 0x138C (Vorse Raider), 0x1444 (无)
- 0x1443/0x1444 在 `card-names.s` 中**不存在** (槽位号有跳号), 与 slot_id 线性映射假设矛盾

**结论**: SRAM nibble→slot_id 映射 **不是简单的线性偏移**. 需后续核对 `card-stats.s` 中 slot_id→sequential_index 对照表; 或在游戏运行时单步观察 SRAM 写入指令的源寄存器值.

## 未做 (建议下次)

参见 `README.md` §六, 仍待:

1. **Watchpoint 验证 DP 单位** — 需 mGBA + GDB 联合 (本次 mGBA-live-mcp 与 GDB stub 互斥, `-g` 标志已被改掉, 若需 GDB 则要先停 live, 重启带 `-g`)
2. **运行时读 pack cost** — 在 state2/3/4 EWRAM 中应该有 1500 这个 u16 / u32 (本地分析未做; 之前的 `pack_search_dp_v2.py` 只搜了 state7)
3. **Ghidra headless XREF** — 给 SRAM 0x6C38 / 0x6E40 EWRAM 镜像 0x02006C38 等地址做 XREF, 找写入函数; 复用 `tools/ghidra-labeling/` 框架

## 产物

- `tools/ad-hoc/find_pack_cost_table.py`
- `tools/ad-hoc/find_pack_record.py`
- 本文件
