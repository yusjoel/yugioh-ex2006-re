# Naming Proposal: 0x080efeec

CALLEE-COLUMN GREP: grepping callee=0x080efeec => 1 hit (indeg=1)

## R4 EPILOGUE PRESCAN
- Epilogue @ 080f00c4..080f00c8: `pop {r4,r5,r6,r7}; pop {r1}; bx r1` => Sub-case E (r0 not overwritten)
- Last r0 write paths:
  - LAB_080f00b8 `movs r0,#0` -- SIOCNT phase > 0x10 (link busy or error)
  - LAB_080f00ba falls through from `ldrh r0,[r0,#0x0]` (DAT_080f00b4 slot value) -- slot halfword read
- Return: r0 = u16 0=busy/error or last slot halfword value

## 提案
- **proposed_name**: recv_sio_deck_sync_packets
- **confidence**: med

## plate comment (中文, ASCII 标点)
SIO 甲板同步协议的接收侧驱动. r0=unused (内部以 DAT_080f008c 0x030007d6 作为状态指针), r1=dest_ptr (存 sp+0x4). 调用 tick_sio_deck_sync_state 后读 SIOCNT bits[5:4]: 若 > 0x10 (链路忙) 则立即返回 0. 检查 bits[5:4] == 0 (player 0) => [sp+0]:=1. 读 IWRAM [base-2] bits[3:0] 确认协议阶段 == 3 (接收就绪); 若不符则返回 0. 主循环: 遍历 slot [0..N-1], 对每个 slot 读入口包头状态 (0x030003a0 偏移), 按状态 (0x0002/0x0003 等) 决定是否 bios_cpu_set 将 card block 数据复制到 dest_ptr+偏移. 写计数器 [base+0x9*4] 递增. 最终返回最后读取的 slot halfword 值. 被 1 个 caller 以 deck-sync 接收阶段调用.

Constants:
- SYNC_STATE_BASE = 0x030007d6 (IWRAM SIO 接收状态指针, DAT_080f008c)
- RECV_PHASE_MASK = 0x30 (SIOCNT bits[5:4])
- READY_PHASE = 3 (协议接收就绪值, bits[3:0]==3)
- SLOT_ENTRY_STRIDE = 2 (lsls slot_index*1 = halfword stride)
- CARD_BLOCK_OFF_A = 0x436 (DAT_080f0098)
- FIELD_MASK = 0x1ff (DAT_080f009c = 0x000001ff)

## 参数签名
- r0: u32 (入口被 DAT_080f008c 覆盖; 实质无 APCS 输入 -- ldr r5,DAT_080f008c 在入口 bl 前加载基址)
- r1: ptr dest_ptr [EWRAM ptr] (bios_cpu_set 写入目标; saved to sp+0x4 @ 080efef8)
- 返回: r0 = u16 0=link_busy/phase_mismatch; nonzero=last slot halfword value

## 副作用
- [dest_ptr + slot_offset]: := card block data via bios_cpu_set (LAB_080effd4 路径)
- [0x030007d2]: halfword := last slot value (DAT_080f00a8 路径, strh @ 080efff6)
- [base + 0xce*4 + slot_offset]: byte counter incremented (strb @ 080f0006)
- [base + 0x9*4 offset]: recv counter byte incremented (strb @ 080effa0)

## 行级注释 (<= 30 行精華)
- @ 080efefe: bl tick_sio_deck_sync_state -- 轮询 SIO 链路状态
- @ 080eff0e: bls LAB_080eff12 -- SIOCNT phase <= 0x10: 继续处理
- @ 080eff10: b LAB_080f00b8 -- phase > 0x10: 链路忙, return 0
- @ 080eff36: cmp r0,#0x3 -- 检查协议阶段 == 3 (接收就绪)
- @ 080eff3a: b LAB_080f00b8 -- phase != 3: return 0
- @ 080effd4: bl bios_cpu_set -- 复制 card block 到 dest_ptr
- @ 080efff6: strh r0,[r7] -- 写最后 slot 值到 0x030007d2
- @ 080f007e: ldr r0,DAT_080f00b4 -- 读最终返回 slot halfword
- @ 080f00b8: movs r0,#0 -- return 0 (busy/error)
- @ 080f00ba: add sp,#0x8 -- epilogue begin

## 调用图
- caller: addr 0x080eda30 (tags: [sio,deck_sync]; role: SIO deck sync 接收主驱动, 在接收阶段调用本函数)
- callee: tick_sio_deck_sync_state, bios_cpu_set

## 置信度证据
- L1 (全静态函数体, asm lines 412766-413012): SIO 接收循环 + bios_cpu_set + 返回路径静态可读
- L6 (命名 callee): tick_sio_deck_sync_state + compute_sio_link_checksum 已命名; SIO deck sync 接收语义明确

## 置信度 / 升级路径
- slot 计数上界 N 需 runtime 验证 (SIOCNT bits[5:4] player count)
- dest_ptr r1 的具体写入结构 (deck slot array vs. EWRAM card array) 需 caller 0x080eda30 asm 追踪
- 如需升级 high: 读 0x080eda30 函数体确认 r1 参数构造; 在 0x080efeec 断点捕获 r1 值
