# File 12 历史残留登记（模块收尾预检）

2026-08-31，在正常推进 Seg-10 时执行模块级预收尾扫描，发现当前模块共有143个自动标签定义；其中136个已纳入Seg-10，另有7个位于历史Seg-2。

以下7个标签全部存在于本轮开始前的 `baseline-modules/12_equip_activation_scan.s`，不是Seg-6..9改动引入。旧Seg-2完成记录中的“DAT_/DWORD_=0”与当前源码不一致。此处只登记事实，不重新命名、不修改Ghidra或汇编。

| 地址 | 当前标签 | 当前表达式 | ROM u32 | 当前asm行 |
|---|---|---|---|---|
| 0x08095280 | DWORD_08095280 | ELIGIB_ACT_TYPE_OFF | 0x00001d5c | 2392 |
| 0x080952cc | DWORD_080952cc | ELIGIB_ANIM_STATE_OFF | 0x00001d6c | 2433 |
| 0x080952d0 | DWORD_080952d0 | ELIGIB_SPRITE_CTRL_OFF | 0x00001d68 | 2435 |
| 0x08095328 | DWORD_08095328 | ELIGIB_SPRITE_CTRL_OFF | 0x00001d68 | 2477 |
| 0x0809532c | DWORD_0809532c | ELIGIB_ANIM_STATE_OFF | 0x00001d6c | 2479 |
| 0x08095330 | DWORD_08095330 | ELIGIB_STATE_CTRL_OFF | 0x00001d54 | 2481 |
| 0x0809565c | DAT_0809565c | 0x0201b870 | 0x0201b870 | 2860 |

预检时源码为 `asm/12_equip_activation_scan.s`，SHA256为 `d4cbe738e5ec9934fe033547dbf1ef379a17bbeb72fcb9274eec8802c6f73cc8`。计数及初始基线交叉检查见 `output/refine-run-20260831-194634/root-module12-preclosure.json`。

预检时Seg-10继续按地址序执行。模块最终收尾不能在这7项未处理时宣称自动名清零。`refine-loop`和项目规则要求“不回头不跳号”；回补这批历史地址将改变正常推进顺序，须明确这批补漏的授权与范围后再进入executor/reviewer/fixer。尚未启动补漏分析或落地。

## 完整文本预检补充

另确认下列历史残留；全部在本轮初始基线，未启动补漏分析或修改。

- `0x080952fc..0x08095304`：8字节 `.byte 0x00,0x20,0x00,0xf0,0x53,0xfc,0x1b,0xe0`，当前asm行2458；段内 `0x080952b6` 的bcc和 `0x080952ba` 的bhi均跳至 `LAB_080952fc`，需要正式ref-scan/反汇编提案与独立review。
- 20行注释仍含旧自动名，其中14行含FUN_/SUB_旧函数引用；具体行号/符号如下。这里只做源码清点，不用旧名猜测新语义。

| 当前asm行 | 注释旧名 |
|---|---|
| 108 | `FUN_080d2ef4` |
| 161 | `FUN_08057874`, `FUN_080598d8`, `FUN_08059b4c` |
| 174 | `FUN_080bb414` |
| 207 | `DAT_0809431c`, `FUN_08057c28`, `FUN_080bb414` |
| 523 | `FUN_0809457c` |
| 666 | `FUN_0809457c` |
| 689 | `FUN_08031668`, `FUN_08031d44`, `FUN_08037c20` |
| 776 | `DAT_0809474c` |
| 831 | `DAT_0809479c`, `FUN_0801e984`, `FUN_080a06bc` |
| 1482 | `FUN_08093660` |
| 1513 | `DWORD_08094c8c`, `DWORD_08094cc8`, `FUN_08094cd4`, `FUN_0809e6f4` |
| 1577 | `FUN_08094c10` |
| 1591 | `FUN_080a0b14` |
| 1703 | `FUN_0803c3b4`, `FUN_0810e5c8` |
| 1971 | `FUN_08095a18` |
| 2346 | `PTR_PTR_08095248` |
| 2537 | `DAT_080953bc`, `DAT_080953c0` |
| 2756 | `DAT_08095550` |
| 6518 | `DAT_0809717c` |
| 7078 | `DAT_080975b0` |

四块 `ROM_INCBIN` 仍对应既有§5.1登记：0x0809437c/0x1c、0x08094c3e/0x22、0x08095b28/0x14、0x08096eec/0x34；此处未变更其分类。模块头中文说明属于文件头，不是Ghidra新设EOL/plate。

已向用户补充请求：Seg-10完成后统一补漏7槽、1个8字节块、20行注释，仍走executor/reviewer/fixer和完整byte-identical验证；当前等待明确回复，Seg-10继续。

## 2026-09-01 最新状态

Seg-10已完成第二轮PASS、写回、构建及主线程独立验收；本轮Seg-6..10共685槽，ROM全字节一致。主线程按完整前缀对照确认上述历史范围原文未动，7槽/8字节块/20行注释仍然存在。

补漏批次的明确授权尚未收到，当前停在该边界；尚未启动补漏executor或模块13。收到允许后，先按这些历史地址递增完成独立executor→reviewer→fixer补漏与模块12收尾，再恢复模块13及后续模块的正常地址顺序。

## 补漏授权与恢复

2026-09-01，用户回复“可以”，明确允许上述历史补漏。批次命名为 `F12-Historical-Closure`，按地址递增走executor→reviewer→fixer；完成后执行模块12全局收尾并自动推进模块13。前述“待授权”段落为当时的历史状态，不再是当前阻塞。

## 历史补漏闭合（2026-09-01）

`F12-Historical-Closure` 已在明确授权后完成第二轮正式PASS、事务落地、完整重导/构建和保存后只读检查。上文各“待授权”“尚未启动”及残留清单均为预检时的历史记录，不再表示当前状态。

- 七个自动槽全部闭合：六DWORD改为审定USER池标签并保留原ELIGIB equate/空refs；9565c建立到既有gSpriteAttrBuf的USER DATA引用。另处理既有具名95550依赖槽，复用95554的id31014仅提升primary，保留id4244及95550原USER引用，32表项/30case不变。
- `0x080952fc`八字节已精确解码为2/4/2字节的movs、BL95ba8、B9533c，原LABEL/两旧跳转保留，callee/epilogue仅增加这两条flow引用；未新增函数或扩body，全局函数数5209不变。
- 20行旧注释经19个完整ASCII PLATE及8个槽EOL同步闭合。全模块自动数据标签、旧自动名注释、`.byte`均为0；四个§5.1块共134 B原样保留，96eec的raw=1来自未压缩6bpp卡图像素巧合，有效引用=0。
- ROM33554432 B全字节一致，SHA1 `9689337d6aac1ce9699ab60aac73fc2cfdccad9b`。25模块仅asm12发生批准的文本变化，其他24模块、constants及所有正式命名文件不变。最终asm12 SHA256 `fd1f3a7138ef1f1076c52930479e5101e764a59fed6f47a4e26a69b3a406bfb0`。
- 主线程独立验收四项全PASS：`root-closure-verification.json`、`root-closure-scope-verification.json`、`root-closure-state-verification.json`、`root-closure-slots-verification.json`；自身记录为`closure-landing-gates.json`和`closure-persisted-check.json`。证据在`output/refine-run-20260831-194634/`，完整计数/备份/脚本见活动文档§4.11。

本批已完成，未stage、未commit；保留原历史记录与先前改动。模块12收尾闭合，驱动器自动继续模块13；本批未预析模块13。
