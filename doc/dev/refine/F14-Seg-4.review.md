# Refine Review: F14-Seg-4（第六轮，最终）

## 复核对象与冻结连续性

- 范围：`asm/14_equip_ai_scoring.s [0x080aba78,0x080acc30)`，4536 bytes；活动路线图中Seg-3已完成，Seg-4地址连续。
- proposal / slots / plates SHA256：`277144e362b814b15fe2dfa664a7f33e5004ffc308c5d37fdff04e8378f4b235` / `7f81b84a8be33ac59af2e8e46f5cbdb7ae9190130b28b93bed44fa48e889fb0d` / `32e09209ef3b8eebb89cf1e92d61345f8af4f1ebbd33c5509983be7f5261fcc1`。
- machine contract / freeze manifest SHA256：`d15843de31170644b3da779325fa3412e64fc3a146589293773ed37b44dd8c7f` / `ad7c79c888332ceff484ebc1c70facaf0f798c50bd0ce2acafc8b7d6f7842124`。
- 独立重算manifest全部20个`review_basis`，0 drift；prior review SHA256 `488f126ae8202d1a300c435211522d458639ac1c46496ac1e2c4b0bad45b4983`精确匹配。
- 独立重算103份保护source，103/103与前态相等；重算15个物理DB文件的current与backup，30/30与前态相等。
- 第五轮完整语义证据保持：`f14-seg4-review-round5-independent-audit.json`，SHA256 `e1904b7d193e553dc15bd33a20187f9473adf273dff8c9e7b8d4b0bf6eb8ced3`。本轮最终计数证据：`f14-seg4-review-round6-independent-audit.json`，SHA256 `45e1db3e82e5a6d0357f09a7e20327c7840ac4a209956ef0161e980734cd98ce`。

P0通过：正式输入存在且非空，没有占位/跳过标记。本轮未运行headless、build、stage或commit。

## 第四轮三项问题已独立关闭

### 1. `0x080aba7a`高寄存器恢复PLATE

ROM 16 bytes为`06b038bc9846a146aa46f0bc02bc0847`。THUMB high-register MOV位解码为：

| 地址 | opcode | 正确语义 |
|---|---:|---|
| `0x080aba7e` | `0x4698` | `r8 <- r3` |
| `0x080aba80` | `0x46a1` | `r9 <- r4` |
| `0x080aba82` | `0x46aa` | `r10 <- r5` |

当前`PLATE_REWRITE`全文324个ASCII字符，SHA256 `bca13a4be2d8837f4ed58e71b4437919c4f2a10df843738d9cf3d15672240cf5`，准确描述`add sp,#0x18`、`pop r3-r5`、三条高寄存器恢复、`pop r4-r7`及返回；Function ID16960、16-byte body、接口和incoming均保持。C8原问题关闭。

### 2. `0x080aba78`返回零出口误名

完整body bytes为`0020`，仅执行`movs r0,#0`，没有phase或entry内存写入；唯一CALL来自`0x080ab240`，随后fall through到共享epilogue。`tick_equip_activation_main_sequence@0x08094d3a-0x08094d4e`在该dispatcher返回0时继续后续update checks。

当前最终名`return_zero_from_equip_entry_dispatch`与406-char ASCII PLATE（SHA256 `fc06eaf49e2f03a68d2562c2466d22921496ab7454610957687b09a7d9ae8cd9`）均与body/caller一致。独立full-ROM unaligned scan对`0x080aba78/79/7a/7b`全部0命中；无pointer projection、odd alias或Equate。Function ID16959、2-byte body、接口及incoming CORE6保持，只改Function name与derived target-primary name。CSV保持5079 rows；canonical inventory保持5214/5124/90，仅`080aba78`和既有`080acbf0`两个name cells变化。C11原问题关闭。

### 3. `0xfffffe3f`位域掩码名称

四个slot `0x080abca8/0x080abd5c/0x080abe3c/0x080abf10`的ROM bytes均为`3ffeffff`。低16位`0xfe3f`的反掩码为`0x01c0`，清除bits `[8:6]`。四个16-bit消费者分别在`0x080abc6c/0x080abd1c/0x080abdec/0x080abebc`执行`ldrh -> AND -> OR 0x40/0x80/0xc0/0x100 -> strh`，写selector 1/2/3/4；`dispatch_equip_entry_slot_by_mode@0x080ab284-0x080ab288`以`lsls #0x17; lsrs #0x1d`读取同一bits `[8:6]`。

当前四行仅`const_or_target/final_slot_label/gas_expression/new_eol_ascii/after_equates_json.name`改为`EQUIP_STATE_CLEAR_BITS_8_6_MASK`，其他字段逐字节保持；其余127行完整相等。`constants/*.inc`无同值同域既有定义，相关`8_1`/`16_9`掩码值和位域不同。新常量总数仍15，四个相关PLATE无额外变化。C5原问题关闭。

## 连续合同复核

- 131 slots与前态131-word地址集合精确一致；131/131 ROM value和bytes匹配。action为104 `EQ_ADD`、20 `REF_ADD`、7 `REF_PRESERVE`；104 after Equates、27 after DATA refs、136 PC READ refs精确。7条PRESERVE前后ref CORE6一致，20条ADD均从空source ref变成唯一批准DATA ref。
- 131 final labels均匹配`^[a-z][a-z0-9_]+$`且唯一；131 EOL为ASCII。
- 21个PLATE rows全部写入：17 `PLATE_REWRITE`、2 `RENAME_PLATE`、2 `EXTERNAL_PLATE_PROJECTION`、0 `PRESERVE`。全部ASCII、字符计数准确且`<=500`，最大仍为`0x080bc168`的458；其全文SHA256保持`afa19fe76d4faa895f17ddf73cef8c8ca0faa73ef1490d74638e0d516fb0d1a0`。
- 21条新PLATE没有`FUN_/DAT_/DWORD_/UNK_/PTR_DAT_`或两个已批准旧Function名残留。Function/registry合同为8 ADD、12 PLATE-only UPDATE、1 rename+PLATE UPDATE。
- layout保持1873 InstructionDB（1734 mnemonic + 139 `.hword`）、131 words、90B padding；raw/carve/disasm/Section5.1均为0。独立full-ROM scan对另一改名入口`0x080acbf0/0x080acbf1`也为0命中。

## 第五轮唯一metadata问题已关闭

当前`f14-seg4-freeze-manifest.json`相对第五轮归档只修改三个顶层JSON叶：

| 字段 | 第五轮值 | 当前值 |
|---|---:|---:|
| `FUNC_RENAME` | 1 | 2 |
| `plate_writes` | 20 | 21 |
| `plate_preserve` | 1 | 0 |

独立JSON diff确认仅这三叶变化；status、prior review、review chain、20个review-basis记录及其他counts完全相等。当前20个basis hash再次重算为0 drift。实际`plates.tsv`为17 `PLATE_REWRITE` + 2 `RENAME_PLATE` + 2 `EXTERNAL_PLATE_PROJECTION` = 21 writes、0 preserve，function plan为2 renames，故新值与正式合同一致。第五轮C12问题关闭。

## 核验（C1-C13）

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | Rule1地址序 | ✅ | Seg-4为`[080aba78,080acc30)`，紧接已完成Seg-3。 |
| C2 | Rule2 raw块归宿 | ✅ | raw=0；InstructionDB/words/padding精确覆盖4536B。 |
| C3 | Rule3/full-ROM ref-scan | ✅ | Section5.1=0；两个改名入口及ABA78 epilogue family的raw/THUMB值均0命中。 |
| C4 | R1槽值 | ✅ | 131/131 slot ROM value与4-byte little-endian bytes匹配。 |
| C5 | R1常量复用/身份 | ✅ | bits `[8:6]`掩码名称已订正；15个新常量合同成立，同值同域无遗漏复用。 |
| C6 | R2槽名 | ✅ | 131 labels合法、唯一、无同址alias。 |
| C7 | R3 DATA ref接通 | ✅ | 20 ADD + 7 PRESERVE、104 Equates、27 DATA refs、136 PC READs精确。 |
| C8 | R5 PLATE现名与事实 | ✅ | ABA7A寄存器恢复已修正；21条全文无自动名或批准旧名残留。 |
| C9 | ASCII | ✅ | 21条PLATE和131 EOL均为ASCII；PLATE均`<=500`。 |
| C10 | carve/THUMB `+1` | ✅ | carve=0；无ROM Function pointer slot或odd projection。 |
| C11 | Function误名 | ✅ | ABA78与ACBF0两项rename均有body/caller/card证据和完整投影合同。 |
| C12 | R6证据与实施合同 | ✅ | manifest顶层计数已订正为2 rename / 21 writes / 0 preserve，且与TSV/plan/machine合同一致。 |
| C13 | 自动槽覆盖 | ✅ | baseline 131 words与131 slots地址集合精确相等。 |

## 状态：PASS

无剩余修改项。第四至第五轮的三项语义修订和一项metadata计数修订均已独立关闭；正式source、DB与Mode B脚本尚未改写。

## Reviewer Verdict: F14-Seg-4 = PASS
