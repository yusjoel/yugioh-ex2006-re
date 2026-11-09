# F13-Seg-9 Exporter Projection Review

## 范围与输入

本review只评审`0x080a5fac -> 0x080a5fb0`这一条已批准REF动作的持久化GAS投影方案，不修改F13-Seg-9的proposal、slots、plates、C1-C13 review、Ghidra DB、正式源码或进度文档。

- Exporter前态：`tools/asm-regen/ghidra/ExportRangeToGas.py`，SHA256 `a46f8efae54994e58f5b067a34f16f7fe751df46b155b67fd0449e6c53db9fdb`。
- C1-C13 PASS review：`doc/dev/refine/F13-Seg-9.review.md`，SHA256 `960a18c6b0ff08e3d6d1d2f8bbcb062d114e0599203eaf7fe18276bc056e4fa3`。
- proposal：SHA256 `3d6fc06bbf6b51c1c74b59aa71fc8a020d57b14d5a40b35687b67ca544a13bbf`。
- slots：SHA256 `2e1ddfd1d7896b39decd2884c1067276519106e98e72a0b074d02d7885050e6d`。
- DB落地回执：`output/refine-run-20261011-103530/f13-seg9-apply-receipt.json`，SHA256 `1a65c100007d82ab1ee503842dfb3baf7bad435af9781f504fe9820b2a250ee6`。
- 待执行patch脚本：`output/refine-run-20261011-103530/root_patch_seg9_exporter.py`，SHA256 `9fec3b3c0eaa1e436872d2b3c3b338d8a657ae2fdf8cbaa83636a7224dc9a101`。评审时Exporter正式文件仍保持前态hash。

## 独立事实核对

### 1. 槽、引用与目标合同

`f13-seg9-apply-receipt.json`的落地后快照给出：

- source `0x080a5fac`：4-byte `/undefined4`，ROM bytes=`b05f0a08`，little-endian值=`0x080a5fb0`；primary USER label为`equip_phase_switch_table_ptr_080a5fac`。
- source outgoing refs精确为1条：from=`0x080a5fac`、to=`0x080a5fb0`、operand=0、type=DATA、source=USER_DEFINED、primary=true。
- target `0x080a5fb0`：4-byte `/pointer`，symbol_count=1；唯一primary symbol ID=5291、source=ANALYSIS、type=Label、qualified name=`switchD_080a5fa2::switchdataD_080a5fb0`。
- target自身的word值为`0x080a6038`，其现有outgoing DEFAULT DATA ref和三条incoming refs均不属于本修补的写入范围。

这些字段与`F13-Seg-9.slots.tsv:47`、proposal:176,237,450及段内switch-word冻结合同一致。

### 2. 消费者与源码定义

`asm/13_equip_placement.s:18900`的`ldr r1, equip_phase_switch_table_ptr_080a5fac`读取该槽；当前投影行在`:18910`为：

```asm
    .word  switchD_080a5fa2__switchdataD_080a5fb0
```

目标在紧邻的`:18911`定义为同名label，随后34个pointer words覆盖`[0x080a5fb0,0x080a6038)`。函数按组合索引选取该表项并执行间接switch dispatch，因此`0x080a5fac`的语义确为switch-table base pointer。

### 3. 当前Exporter失配原因

`ExportRangeToGas.py:527-562`先选择outgoing primary ref，再读取目标primary symbol；`:552-553`只放行`SourceType.USER_DEFINED`。ID5291必须保持ANALYSIS，因此当前路径在`:552`返回`None`，`:612-617`随后输出裸值`0x080a5fb0`。

`resolve_unique_label_for_addr()`经`getName(True)`取得qualified name；`sanitize_label()`把两个`:`分别替换为`_`，结果精确为`switchD_080a5fa2__switchdataD_080a5fb0`。该helper还把地址与名称写入`addr_to_label/label_to_addr`，所以后续遍历到`0x080a5fb0`时，`emit_label_if_any_or_forced()`会输出相同label定义。完整ROM导出范围包含source与紧邻target，GAS符号可解析。

### 4. 具体patch代码核对

`root_patch_seg9_exporter.py`先要求正式Exporter逐字节等于本run冻结基线，再要求旧USER判断片段只出现一次；它在内存中生成新内容、通过Python语法编译后才写文件，并保留现有CRLF。插入块之后原USER判断及后续prefix过滤文本原样拼回，因此其他地址的resolver路径保持字节级相同。

具体API与守卫检查结果：

- `iter_any()`的每个出口都是Python list：`None -> []`、Java iterator -> `out`、其他iterable -> `list(it)`，因此`len(iter_any(getSymbols(to))) == 1`合法并精确约束target唯一Symbol。
- `Listing.getDefinedDataAt(Address)`、`Data.getDataType().getPathName()`已由`tools/ghidra-labeling/RefineF13Seg9.py:226,242,356`在同一工程工具链使用；当前回执给出的目标path为`/pointer`，代码比较值正确。
- `Memory.getInt(Address)`按当前GBA program的little-endian读取4-byte signed int；`& 0xffffffff`后与`to_off`比较，能精确验证`b05f0a08 -> 0x080a5fb0`。
- `str(primary.getReferenceType()) == "DATA"`与本工程回执和既有审计脚本的Ghidra字符串表示一致；source、operand、primary均读取reference本体，未混用target symbol属性。
- 目标ID、source、type、qualified name、Data path或唯一性任一漂移时，代码抛出`RuntimeError`，不会输出未经批准的ANALYSIS名称。resolved GAS label不逐字相等时也同样中止。

## 修补方案评审

| 检查 | 结果 | 证据与约束 |
|---|---|---|
| 插入位置 | PASS | 在`:549-551`取得`primary`、`to`、`sym`后，并在`:552`的通用USER判断前处理，能读取全部守卫且不改变原通用路径的顺序。 |
| source地址隔离 | PASS | 只接受`data_obj.getAddress().getOffset()==0x080a5fac`；结构字段或其他word不会命中。 |
| source值隔离 | PASS | 代码要求长度精确为4，并用`Memory.getInt() & 0xffffffff`核对值为`0x080a5fb0`，没有只凭ref目标返回符号。 |
| ref隔离 | PASS | 代码选取现有resolver已经确定的primary ref，并要求该ref同时满足USER_DEFINED、DATA、operand 0、primary；`to_off`在内层严格等于`0x080a5fb0`。当前DB的outgoing refs精确为这一条。 |
| target Symbol隔离 | PASS | 要求目标symbol总数为1，并逐项核对ID5291、ANALYSIS、LABEL、primary及完整qualified name。不能只核对短名或地址。 |
| target Data隔离 | PASS | `listing.getDefinedDataAt(to)`必须存在，长度4、datatype path=`/pointer`；这对应合同记法`/pointer:4`。 |
| GAS label解析 | PASS | 只调用现有`resolve_unique_label_for_addr(program,to)`，并要求返回值逐字等于批准名；任何缓存碰撞、namespace变化或清洗差异都不能放行。 |
| byte-identical | PASS | `.word switchD_080a5fa2__switchdataD_080a5fb0`解析值为`0x080a5fb0`，字节仍为`b0 5f 0a 08`，与ROM word相等。 |
| 作用域 | PASS | 不改变ID5291的source、namespace或primary状态，不创建global label，不把ANALYSIS加入通用白名单，不触碰target的Data/ref或34个switch words。 |
| 失败行为 | PASS | source地址与ref外层条件命中后，任一value/target守卫失败均抛出`RuntimeError`；满足全部守卫才返回批准名。其他地址继续执行原`SourceType.USER_DEFINED`、ROM LABEL、auto-prefix过滤路径。 |

## 实现与验收合同

已提供代码在`resolve_word_symbol()`内联窄分支。落地与验收必须满足以下合同：

1. 地址比较使用数值offset，不依赖`Address.toString()`大小写。
2. DATA类型使用当前Ghidra API的`ReferenceType.toString()`精确比较`DATA`；source检查使用reference的`getSource()`，不得误用target symbol source。
3. source word以`Memory.getInt(Address) & 0xffffffff`读取并核对；正式只读headless导出是该API路径的运行时验收。
4. target唯一Symbol检查枚举`getSymbols(to)`，不得只调用`getPrimarySymbol(to)`后省略唯一性断言。
5. `resolve_unique_label_for_addr()`返回值必须与`switchD_080a5fa2__switchdataD_080a5fb0`逐字相等后才可返回。
6. 不修改`:552-562`现有通用resolver条件；不向其他ANALYSIS label扩展能力。
7. canonical只读全量导出后，与未修补Exporter输出相比，只允许`0x080a5fac` operand从`0x080a5fb0`变为批准GAS名；label、指令、其余data行、注释和行数均应相等。
8. `inject_modes -> split_all_s`后，`asm/13_equip_placement.s`必须恰有一个批准`.word`引用和一个同名label定义；不得保留该槽裸值或产生重复label。
9. 汇编后的`output/2343.gba`必须与`roms/2343.gba` byte-identical。再次从同一DB全量导出必须保持该符号行，证明修补已消除手工投影依赖。

当前方案不要求修改DB语义，也不改变原C1-C13 PASS输入或哈希合同。

## 状态: PASS

## Export Reviewer Verdict: F13-Seg-9 per-slot exporter projection = PASS
