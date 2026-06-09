@ =============================================================================
@ IWRAM 变量符号常量
@ 数据来源: refs/datacrystal-um2006/ram-map.md
@ =============================================================================

.equ gIntrTable,      0x03000000  @ 中断函数指针表 (IntrMain 据中断优先级取槽; 13 槽)
.equ gPrng,           0x03000040  @ 4 B  伪随机数发生器状态
.equ gFrameCounter,   0x03000240  @ 4 B  帧计数器
.equ gDemoSceneInitPhase, 0x03000244  @ 4 B  demo 场景 init 阶段打包字 (bits[21:14]=phase idx)
                                  @ step_demo_scene_phase 经 gPrng+0x204 访问 (无直接字面量槽; 参考用)
.equ INTR_VECTOR,     0x03007ffc  @ BIOS IRQ handler 向量槽 (crt0 写入 IntrMain 地址)
.equ pack_ui_state,   0x03005850  @ pack scene state struct; offset 0x10 = u16 state field
.equ gOamAttrBuildBuf,0x030007f8  @ OAM 属性构建暂存缓冲 (128 项 × 8 B = 0x400 B, 紧邻 gIg2dUsedCellAnm)
                                  @ setup_isd_cell_anim_oam_entry/setup_decimal_digit_oam_batch 构建

@ -----------------------------------------------------------------------------
@ NNS G2D (IG2D) 资源加载管理器 (源 GL/IG2D_Main.c)
@ used-count 计数器 + 缓冲池基址; reset_ig2d_load_counters 清 3 个计数器
@ -----------------------------------------------------------------------------
.equ gIg2dUsedCellAnm, 0x03000bf8  @ s32 已用 CellAnm 槽数 (max NELEMS(CellAnmBank)=0x40)
.equ gIg2dUsedNceBuff, 0x03000bfc  @ s32 已用 NceBuff 槽数 (max IG2D_LOAD_ANM_MAX=2)
.equ gIg2dUsedNanBuff, 0x03000c00  @ s32 已用 NanBuff/char-data 槽数 (max IG2D_LOAD_ANM_MAX=2)
.equ gIg2dNceBuffBase, 0x03000c08  @ NceBuff 缓冲池基址 (slot = base + count*0x1000)
.equ gIg2dCharPoolBase,0x03002c08  @ char-data 缓冲池基址 (slot = base + count*0x1000)

@ Seg-8 addition: IWRAM OBJ attribute scratch buffer
.equ IWRAM_OBJ_SCRATCH_BUF,       0x03000288  @ IWRAM OBJ attribute scratch buffer (0x118 bytes); 4 ROM refs
@ Seg-9 addition: campaign OAM attribute buffer mid-point (gPrng+0x20c absolute)
.equ tick_campaign_card_selector_oam_attr_buf, 0x0300024c  @ gPrng+0x20c; OAM attr buf accessed as table base; 1 ROM ref
