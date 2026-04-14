# P2（卡牌列表小图）调查进度 — 2026-04-15

## 本次 session 进展

### 已尝试（静态）

扫描 `asm/all.s` 查找小卡图 ROM 基址 `0x01000000`（GBA 指针 `0x09000000`）的字面量，**未命中**：

- `grep '\.word 0x09000000'` → 0 hits
- `grep '\.word 0x0900[0-3]...'` → 最近的命中是 `0x09326280`（在 `0x080BEC04` 附近，属其他资源指针，落在 ROM 0x01326280 区）
- `grep '\.word 0x0000 08c0'` / `\.word 0x8c0`（stride 2240）→ 0 hits

**结论**：小卡图加载代码**没有以 `0x09000000` 为字面量**作为基址使用。可能的原因：

1. 加载函数通过另一个常量 + 偏移计算（例如 ROM 整体基址 `0x08000000` + 子偏移）
2. Ghidra 反汇编把这些字面量解码为数据（`.incbin` 段）而非 `.word`
3. 实际加载走 DMA，源地址由某张表（类似卡图索引表 `0x095B5C00`）提供

### 未尝试（需下次 session）

所有动态路径都需 mGBA，本次未启动：

- **P2-1**（mGBA 动态）：进入卡选界面读 DISPCNT/BGxCNT/tilemap/char base
- **P2-2**（静态 + 动态）：从 VRAM 地址在 all.s 搜立即数
- **P2-3**（调色板）：候选三区仍未验证
- **P2-4**（批量 PNG 导出脚本）
- **P2-5**（UI entry 占用数）

## 下次 session 推进建议

1. 启动 `pwsh tools/mgba-scripts/start-mgba-gdb-ss1.ps1`，加载存档进入卡组构筑界面
2. 用 Lua 读 DISPCNT + 所有 BGxCNT + 关键 tilemap + VRAM char base
3. 确认小卡图写入的 VRAM 地址后，在 `asm/all.s` 搜那个 VRAM 立即数（例如 `0x06004000`）
4. 从命中的函数字面量池反向找 ROM 源 + palette 基址（照抄 P1 Phase B2 方法）

## 其他发现

- `0x0901A422` / `0x0901AA1C` / `0x0901AF18` / `0x0901B11C`（`asm/all.s` L374150/L374833/L374163/L374739）
  是 ROM 区 `0x01A1A422..0x01A1B11C` 范围，恰好落在 **Theme Duel 大图调色板**
  `0x1A1A52C`（见 Exarion Universe Top/Bottom）附近；可能是 T-THEME 相关加载函数的
  字面量池。**与小卡图无关**，但可作 T-THEME 静态追踪切入点。
