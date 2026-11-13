# Refine Review: F16-Seg-9

第二轮完整C1–C13语义复审：PASS。范围 [080c9c94,080cad78)，4324B。首轮仅有F16S9-R1/R2两项语义错误，现已全部闭合。

权威semantic FINAL：f16-seg9-semantic-firststage-final-v2.json，6025B，SHA256 02db3b1a0950940d9fb2a8c724ec3d1817e948237e88d64612f99017be586160；12条fixed记录已独立逐条核验。Root complete-before仍为732ac462bdc2d6bf38d24e856449273b4c29bfa7c6845192dde38050d0085a0c，对应Core-v2/Properties-v2/Tiny-v2及23条记录均保持。

原首轮NEEDS_FIX文档与v1正式文件已经Root按27项映射逐字归档；CAS更新前核对原review为8639B、SHA256 d180fdb4a5e71fe9e9ccdb4b007a9f41b728c52adb5950e86adb7dda0a3b6322并与归档相等。下列未变检查沿用首轮独立证据，全部记录再验size/SHA；未重复R8像素或通用矩阵。

本结论只通过分析质量与静态语义计划。完整POST模型、生产脚本、实际事务/保存及整ROM验收留后续ModeB。未操作Program/Ghidra、源文件、build或Git，不授予持久写入许可。

## 核验（C1–C13）

| # | 检查 | 结果 | 独立证据与结论 |
|---|---|---|---|
| C1 | Rule1 地址序 | ✅ | 活动文档已完成8/10，下一段本范围；13Fn/167word/158auto，下一边界cad78。 |
| C2 | Rule2 raw归宿 | ✅ | 独立扫实际段内ROM_INCBIN/.incbin/.byte均0，R4/R7为空；未静默保留raw。 |
| C3 | Rule3 引用分类 | ✅ | 独立全ROM非对齐重叠扫描13入口raw/+1，全部odd无命中；仅CA28C even值命中08511c7b，完整4800B tb0001.bin与ROM相等、offset891为图像像素且native incoming无该源。26个ROM资源指针也独立raw/+1重扫，不建立新callback表或§5.1。 |
| C4 | R1 数值 | ✅ | 167池字逐槽重读ROM小端；39EQ值逐一相等，9个even CASE保留原值与namespace表达式。 |
| C5 | R1 复用 | ✅ | 全constants表达式独立求值；11新numeric、43新address与两既有地址alias复用核对。0x8080旧名限定card-image列，0xfffff000旧名限定scene-slot clear，新增格式语义有明确区分；其余新numeric确无同值既有alias。 |
| C6 | R2 名与碰撞 | ✅ | 158新槽名与9新函数名符合形式，212个显式primary地址/名字各自唯一；已有全局/硬件名称按既有约定，两个DEFAULT派生节点不计USER。 |
| C7 | R3 接通 | ✅ | 89新增DATA、30既有DATA保持；158槽+45目标USER，共203新USER。全部before与实际完整state一致，正式TSV与primitives逐字段核对；无type/namespace/ABI动作。 |
| C8 | R5 现名 | ✅ | 16新PLATE用现名，无旧FUN/DAT/DWORD；全模块源PLATE中9个旧函数名依赖均在本次重写集合。registry12替换与4个实际缺席追加逐项AST核验。 |
| C9 | ASCII | ✅ | 16PLATE及210EOL全部ASCII，PLATE≤500；下述建议文本303/299字符，均ASCII。 |
| C10 | carve/Thumb | ✅ | 无carve动作；9个switch CASE为原even地址，全部Function+1扫描无正引用，不把图像even偶合作R7。 |
| C11 | 误名订正 | ✅ | 9rename由13Fn本体/消费者与字形支持：说明窗口、倒计时、区域计数、turn、phase、result历史、HUD、比较stat合成和HUD初始化；没有card-image decode误名残留。 |
| C12 | R6 消费者语义 | ✅ | 首轮13Fn/3context与117条高寄存器独立解码证据保持；CA348现为固定x31、y=8+22*phase，CA3A4现为八位count/跳过state0且保留非零index0。两项PLATE/EOL/消费者说明与registry after来源已同步。 |
| C13 | 自动名覆盖 | ✅ | 实际DAT128+PTR30共158个定义全部对应USER槽；167word全覆盖，9CASE不改其核心；不存在新增raw/自动名遗漏。 |

## 关键语义与保护事实

- 9C94不读取输入r0：全局field+1为phase，+2为counter，+0x21c为cardID；phase0..8返回0，完成清bit2/ID与混合状态后重置phase并返回1。
- 9EB8的r0/r1为x/y，r2为value，r3为minimum_digits，第五stack参数为palette；signed除余10，至少绘一位并补零。9F50两个计时器先去掉帧计数signbit，60frames/sec，时限分别180和300*k秒，条件分支与blink bit已核。
- A160两player循环与PLAYER_BLOCK_STRIDE、Deck/Graveyard/Removed Cards三字段成立；A28C默认turn+1与alternate差值、x23/y11或115和两位数字成立。A42C的三个context bit0会阻止后续计数/计时器路径。
- A4F4真实0x468a保存r1到r10，r2先被覆写；3×3 map、0x120字节tiles及0x40字节palette copy成立。A5F8固定五位、上限99999与signed除余成立。
- A660先清128B scratch，比较clamped value与baseline选三bank，(-1,-1)选unknown glyph；四像素窄数字按五像素间距交错打包，六像素prefix后转为四个8×8 4bpp tiles。CB1CC实际调用的value/baseline/selector与signed ATK/DEF读取支持新名。
- A8EC的6×4 aux、两组2×4 stat、2×30 name maps和15×12 palette10 inner map均核；outer mode和inner选择分支、0x141e lowbyte30/highbyte20经EE3A8实际callee核对。F74D4按width*32字节、height行、目标stride0x400复制OBJ tiles。
- ACE8先清0x800 name区域；field+8非零才清其他detail区域并reset。3BC58局部玩家/UI effect判定与sprite bit0、CAE84 low13 CID/slot20B/反向计数与999上限均核。
- R8已目视PNG并从原ROM独立解码15个bank/palette样本、14400像素，最大通道差0。阶段六字形为纵排DP/SP/M1/BP/M2/EP；合成灰度的BG只确认字形，不赋予未证实颜色。
- D70CC typed DEFAULT派生与0985117E offcut DEFAULT均来自实际Tiny-v2，保留ID4611686018562486476/4611686018587103614及完整原state/ref/namespace；不加USER或未知DEFAULT。D70CC RHS保持raw0x0600e000，不加outside pin；两处派生名和incoming名称投影已列计划。
- Root完整前态保护254个Function DTO、1962word/4332state、34748Properties、17649Tiny/1957edges。DDE1C入口无instruction的事实保持，不强制反汇编。

## 状态：PASS

## 已闭合 F16S9-R1 / F16S9-R2

CA348的r0高16来自8+22*phase，低16固定31；实际F616C helper以高16低8写attr0 Y、低9写attr1 X。CA3A4只合成首byte bits7:1与次byte bit0，count为0..255；循环从index0起，只跳过state0。原ROM/源行与helper字节已重核，首轮领域反例仍由同一实际路径支持。置信度high。

修正后的303字符ASCII PLATE与CA35E EOL：

> Append the current duel-phase highlight sprite. Read the phase from gP1LifePoints+0x1cf4 and the turn player from+0x1ce8. Use x31,y=8+22*phase, a16x32 shape, and tile0x14+2*phase. Select palette2 when the turn player equals local_player XOR1, otherwise palette1. No inputs; writes the active OAM buffer.

> Phase-highlight y=8+22*phase; fixed x31.

修正后的299字符ASCII PLATE与CA418 EOL：

> Render result-history bytes at gPrng+0x241, including index0 when nonzero. The eight-bit count is(gPrng[0x23f]>>1)|((gPrng[0x240]&1)<<7). Skip state0. For each other state append tiles0xf7+state and0xf7+mapped_state at x8*index,y128 and24. Map1->2,2->1,3->3; other nonzero states map to0. No inputs.

> Reconstruct the eight-bit result-history count from gPrng+0x23f bits7:1 and+0x240 bit0.

四段文字均与本人首轮建议逐字相等，并同步至authoring、primitives、正式plates.tsv/proposal与producer中的同一消费者说明。两个future registry动作均保持APPEND_MISSING，after文本直接取修正后的plate_after；registry_before未变。

authoring严格只变schema及上述两个PLATE/两个EOL，共5叶。primitives严格只变schema、author proof的path/size/hash及两个PLATE/两个EOL，共8叶。plates.tsv只变两处plate_ASCII，slots.tsv全部字节不变；proposal只变四段对应文本及同一条消费者说明。所有before、列表顺序/长度/类型、名称、scope、DEFAULT IDs和其他14PLATE/50指令EOL保持。

producer全部函数AST相等，只有三个版本路径替换及一条相同语义的消费者说明替换。本人独立将write/record输出I/O捕获到内存，保留全部生成表达式与断言执行：v1五输出与Root归档逐字相等；v2两次五输出彼此相等并与冻结的proposal/slots/plates/primitives/selfcheck相等。没有执行源文件或Program实施动作。

所有counts保持：13Fn/167word/158auto、39EQ/89REF_ADD/30REF_PRESERVE/9CASE、203新USER/9rename/212显式primary、16PLATE/210EOL、54新GNU与2既有地址alias复用；无R4/R7/type/body/ABI/override。两个既有DEFAULT派生节点仍保持原ID与前态，D70CC RHS raw0x0600e000及无outside pin的计划保持。

## 独立证据

- f16-seg9-semantic-rereview-evidence-v2.json：12新记录/27归档映射、严格字段差异、原ROM事实重核及独立v1/v2 producer回放。
- f16-seg9-semantic-review-structural-v1.json：首轮167word/158槽、全部常量表达式、DEFAULT依赖、117解码、独立全ROM raw/+1扫描和16body等事实；原字节保持。
- f16-seg9-semantic-review-consumers-v1.json：首轮领域反例/两项准确修正建议与15样本14400像素R8独立结果；错误结论作为历史依据保留，现已闭合。
- root-f16-seg9-semantic-v1-cas-archive-v1.json：原27项字节归档与旧review的CAS映射。
- 统一结论与精确size/SHA见f16-seg9-semantic-review-final-v2.json。

## Reviewer Verdict: F16-Seg-9 = PASS
