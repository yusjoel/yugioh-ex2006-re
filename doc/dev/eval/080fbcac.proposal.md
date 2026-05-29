# Naming Proposal: 080fbcac

## 提案
- **proposed_name**: render_starter_deck_cursor_oam_pair
- **confidence**: med

## plate comment (中文, ASCII 标点)
为 starter_deck 选择界面渲染两个光标 OAM 条目 (左/右指示器).
首先检查 [0x020297e4] bit0: 若为 0 则进入备用路径 (4 个固定位置 OAM 写入); 若为 1 则执行主路径.
主路径: 循环 slot_idx=0,1 (共 2 次); 每次以 slot_idx*15 + 0x200 计算 x 坐标基址,
读 [0x020297e4] bit1 决定是否追加 0x40 x 偏移 (当 slot_idx != bit1 时);
循环 4 次 write_oam_entry_from_packed_args 写相同 OAM 内容, 每次 y 偏移 +0x20.
备用路径 (bit0==0): 循环 slot_idx=0..3, 以固定 y=0x38+slot_idx*0x20 和
x=0x020f0000 基址 + slot_idx*0x40000 写 4 个占位 OAM.
退出: pop{r4,r5,r6,r7}; pop{r0}; bx r0 (Pattern B void).
Constants:
  CURSOR_STATE_ADDR = 0x020297e4 (starter_deck 光标控制状态字节地址)
  X_BASE_OFFSCREEN = 0x80<<2 = 0x200 (OAM attr1 x 基址: 屏外初始位置)
  X_PLAYER_OFFSET = 0x40 (非当前玩家光标 x 偏移)
  Y_STEP = 0x20 (OAM 条目 y 间距)
  Y_ALT_BASE = 0x38 (备用路径 y 起始值)
  Y_OAM_STEP_PACKED = 0x80<<0xb = 0x40000 (打包 OAM y+0x20 步长高位)

## 参数签名
- r0: void (入口 ldr r1,[DWORD_080fbd0c] 立即覆盖; 非独立参数)
- 返回: void (pop {r0}; bx r0 = Pattern B void)

## 副作用
- OAM (通过 write_oam_entry_from_packed_args): 写 2*4=8 个 OAM 条目 (主路径) 或 4 个 (备用路径)

## 行级注释 (<=30 行精华)
- @ 080fbcb2: ldrb r1,[r1,#0] -- 读 [0x020297e4] 控制字节
- @ 080fbcb4: ands r0,r1; cmp r0,#0; beq -- bit0==0 -> 备用路径
- @ 080fbcbc: LAB_080fbcbc 循环 slot_idx=0..1
- @ 080fbcc0: 0x80<<2=0x200 -- x 坐标基址 0x200 (屏幕外初始位置)
- @ 080fbcce: lsls r0,r0,#0x1e; lsrs r0,r0,#0x1f -- 提取 [0x020297e4] bit1 (active player)
- @ 080fbcd6: adds r0,#0x40 -- x += 0x40 偏移 (非当前玩家光标位置)
- @ 080fbce4: movs r6,#3 -- 内层循环 4 次 (0..3)
- @ 080fbcf2: write_oam_entry_from_packed_args -- 写一个 OAM 条目
- @ 080fbcf8: 0x80<<0xb=0x40000 -- 每次 y 偏移 + 0x20 (高 halfword)
- @ 080fbd14: 备用路径 y=0x38, 步长 0x20
- @ 080fbd26: write_oam_entry_from_packed_args -- 备用占位 OAM

## 调用图
CALLEE-COLUMN GREP: grepping callee=0x080fbcac
- caller: indeg=0; form(c): grep ".word 0x080fbcad" asm/all.s => 0 hits => Sub-type A; 由 game_str/starter_deck 步分发链间接触发
- callee: write_oam_entry_from_packed_args (x2 路径)

## 置信度证据
- 层 L1: asm lines 434783-434857; 函数体完整可读
- 层 L2: [0x020297e4] bit0/bit1 读取 + 双槽循环 + write_oam_entry 模式明确为 "光标对渲染" 语义
- 层 L3: 备用路径 4 个固定位置与主路径 2 槽模式形成 active/inactive 分支对

## 置信度 / 升级路径
- 待验证 1: 确认 0x020297e4 结构体含义 (starter_deck 选择状态?) -- 追踪该地址的其他写入者
- 待验证 2: x 基址 0x200 是否为 "屏幕外隐藏" 初始值 -- 确认 OAM attr1 x 字段语义 (9-bit 有符号)
