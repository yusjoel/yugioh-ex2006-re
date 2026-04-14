# 下一个 session 的提示词：批量导出全部卡牌大图

把下面方框内的内容作为 session 开头的首条 user message，让 Claude 有完整上下文。

---

## 提示词（复制以下内容）

```
目标：实现 `tools/rom-export/export_card_images.py`，批量导出《游戏王 EX2006》(roms/2343.gba) 全部卡牌的详情页大卡图为 PNG。对应 PLAN.md 的 P1-5。

## 上下文：必读的前置文档

按此顺序读：
1. `doc/dev/p1-phase-b2-findings.md` ⭐ 核心：FUN_0801d290 的静态分析 + 6bpp 解码公式 + card_id 查表流程 + 80×80 像素 + 验证状态（已通过单卡实测）
2. `doc/dev/card-data-structure.md` §3.2：大卡图与列表小图是两批独立数据（别搞混）；整体 ROM 布局
3. `tools/ad-hoc/decode_card_6bpp.py`：已验证的单卡解码器，直接拿来改造成批量导出
4. `PLAN.md` 里的 P1 部分（看 P1-3/P1-4/P1-5 的约束）

## 已确认的事实（勿质疑，findings 已实测验证）

- 大卡图基址：`0x08510640`（GBA 指针），ROM 文件偏移 `0x00510640`
- 公式：`src = 0x08510640 + tile_block × 4800`
- 尺寸：**80×80 像素 = 10×10 tiles × 8×8**（每 tile 64 像素，行优先）
- 每张卡 ROM 占用 **4800 字节**（800 次循环，每次消耗 6 字节产出 8 像素）
- 6bpp 解码公式见 findings §3.4（decode_card_6bpp.py 已实现并验证正确）
- card_id 查表：
  - 索引表起 `0x095B5C00`（ROM 文件偏移 `0x015B5C00`），每项 u16 LE
  - 公式：`byte_offset = (card_id × 2 + flag) × 2`
  - flag 来自 ROM[0x080000AF] 高 8 位判断：== 0x4A 则 flag=0（日版），否则 flag=1
  - 本 ROM 是 BY6E（USA），`flag=1`
- 第二循环（findings §3.5）：`final_palette_index = raw_6bit + 0x10`（第 5 参数）
- 调色板基址：`0x084C76C0`（256 色 BG 调色板，BGR555）
- **单卡已验证**：DESPAIR FROM THE DARK (card_id=1323, tile_block=1476, src=0x08BD2140) 的灰度解码清晰可辨（见 `doc/temp/despair_tiles_10x10.png`，该文件本地存在但 doc/temp 不入库）

## 未解决的问题（本任务要解决的重点）

### 问题 1 ⭐：card_id 的可遍历范围与 slot_id 映射

- findings 里的 card_id=1323 是**从 EWRAM 卡片对象计算出来的运行时值**（`word0 >> 3 & 0x1FFF`），不等于 `data/card-stats.s` 里的 slot_id。
- `data/card-stats.s` 有 5170 条 × 22 字节，其中 copy_index=0 的"主记录"共 2054 个（唯一槽位）。
- `card-data-structure.md` 提到索引表 `0x0183885C` 有 2098 条（日语卡名索引），`0x015BB5AC` 是欧洲卡名。
- **需要做的事**：
  - 扫描 `0x015B5C00` 起的索引表，找出它的长度（u16 条目数）
  - 对每个 index 读出 tile_block，再计算 `src = 0x08510640 + tile_block × 4800`
  - 重复的 tile_block（异画共享）要识别出来，避免重复导出
  - 搞清楚 index ↔ slot_id 的映射（用于生成有意义的文件名，例如 `card_0FA7_blue_eyes.png`）
  - 如果映射不通，先用 `card_{index:04d}_tile{tile_block}.png` 的中性命名

### 问题 2 ⭐：调色板

- 单卡调色板在 `0x084C76C0`（256 色 BG palette，见 findings §3.1 DAT_0801d430）
- **每张卡是否共用同一调色板？** 不清楚——可能每卡一张、可能每批共用
- 如果每卡独立，索引方式未知，findings 没给
- **建议调查方法**：
  - 先用**单一共享调色板**（0x084C76C0 读 512 字节，展开 256 色 RGBA）试试
  - 导出几张已知卡（Blue-Eyes slot 0x0FA7、Kuriboh、DESPAIR card_id=1323）
  - 肉眼比对 mGBA 截图颜色是否正确；如果只有部分卡对得上，说明调色板按卡切换
  - 若需要调查，对 FUN_0801d998（findings §2 调用链）的 `bl FUN_080ee010` 看是否写调色板
- **回退方案**：如果调色板映射搞不定，先导出灰度 PNG（把 6bit 值 ×4 当 Y）也算成果，至少所有卡的几何/形状都能看

### 问题 3：多区版本差异

- 索引表偏移会因 `flag` 改变：`(card_id × 2 + flag) × 2`
- 本项目 ROM 是 BY6E（flag=1），只处理这一版即可
- 不要试图兼容多区，硬编码 flag=1

## 具体要做的事

### 步骤 1：扫描索引表边界
- 读 ROM[0x015B5C00:] 若干字节，以 u16 LE 解析
- 找出索引表结束条件：连续 0、或到已知下个区段起始、或长度与 2098（card-data-structure 里提的另一个表条目数）吻合
- 报告：索引表长度、tile_block 的值域、是否有重复 tile_block（异画）
- 验证节点：`xxd -s 0x15B70AE -l 2 roms/2343.gba` 应得 `c4 05`（=1476，card_id=1323 的 tile_block，见 findings §6 验证状态）

### 步骤 2：写批量导出主循环
- 基于 `tools/ad-hoc/decode_card_6bpp.py`，加外层 index 遍历
- 对每个有效 index 读 tile_block → 计算 src → 读 4800 字节 → 6bpp 解码 → 10×10 tile 重排 → 写 PNG
- 先用灰度输出（无调色板）验证几何正确
- 输出目录：`graphics/card-images/`（已 .gitignore 的 graphics/ 下）

### 步骤 3：接入调色板
- 尝试共享调色板 `0x084C76C0`（512 字节 BGR555→RGBA）
- 输出彩色 PNG，比对几张已知卡
- 若颜色对不上，在 findings / asm/all.s 里继续追查每卡调色板位置

### 步骤 4：文件命名
- 若能建立 index↔slot_id 映射：`{slot_id:04X}_{english_name}.png`
  - english_name 从 `data/card-names.s` 读（每张卡第一个字符串是 EN，含 null）
- 否则：`card_{index:04d}_tile_{tile_block}.png`

### 步骤 5：验证
- 用 mGBA MCP 启动游戏到卡牌详情页（可用 ss1 存档）
- 截图几张卡，与本次导出的 PNG 视觉对比
- 至少验证 3 张：DESPAIR FROM THE DARK（已知 card_id=1323）、Blue-Eyes（slot 0x0FA7）、Kuriboh（slot 0x0FCE？ 需查 data.md）

### 步骤 6：更新文档
- 在 `doc/dev/p1-phase-b2-findings.md` 末尾补充"批量导出状态"一节
- `PLAN.md` 里 P1-5 改为 `[x]`
- 新增 `doc/dev/card-image-export.md`（如果有必要），记录索引表扫描结果、调色板策略、未解决的异常（如解码失败的卡）

## 约束与注意事项

- **不要自动 commit**（CLAUDE.md 规则），每个阶段完成后等用户确认
- 路径用正斜杠（Git Bash harness）
- 本地机器路径（mGBA/pwsh/Ghidra 等）在 `LOCAL.md`，不要硬编码
- 如果需要 mGBA/GDB 动态验证，两套 MCP 都已就绪（`~/.claude.json` 的 project scope 已配，直接用）
- 导出产物放 `graphics/` 下（已 .gitignore），不要入库
- 脚本放 `tools/rom-export/export_card_images.py`（正式位置），`tools/ad-hoc/decode_card_6bpp.py` 留作历史参考

## 输出风格

- 简体中文
- 每完成一个步骤先报告发现再继续
- 遇到公式或地址与 findings 不符，**先停下来报告**，不要自行修正——有可能是 findings 本身有遗漏，需要你一起判断
```

---

## 为什么这样写

- **把已验证事实和未解决问题分开**：findings 的 6bpp 公式 + card_id=1323 已实测，可以直接相信；但调色板、card_id↔slot_id 映射、索引表长度都是未解决项，分开列出避免模型在已验证的地方重新试错。
- **给了具体验证节点**：`xxd -s 0x15B70AE -l 2` 出 `c4 05` 是一个秒级验证，能立即判断公式链路是否还通（例如 ROM 文件是否被改过）。
- **回退方案**：调色板可能搞不定，允许先出灰度版本；别让整个任务因为颜色问题卡死。
- **脚本命名分层**：`tools/ad-hoc/decode_card_6bpp.py` 是历史验证产物，正式导出走 `tools/rom-export/export_card_images.py`，与现有 `export_gfx.py` / `export_card_data.py` 结构一致。

## 用完后

批量导出验证通过后把本文件删掉（`doc/temp/` 下不留临时文档）。
