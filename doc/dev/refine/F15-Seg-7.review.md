# Refine Review: F15-Seg-7（最终窄复审）

最终冻结manifest SHA256：c3bdcbf6e59a1f6d8d95541417d398491ecdfd8f307c00b02531c586423da36d。
正式proposal/slots/plates：4666d2134c0101d990c1ceff6747fef3deca55cf859ca2335a1c36fa0c731cf2 / 459754ac49f6b4257588e84332937ab9ed1fe3a35a000cfbd193f1be953fe97d / 7eb2bc1ef9ed0ec3719bf0fdac7af93408e190ad529e0ece274130420d87e3c7。

第三轮review/audit已按原SHA保留于root-f15-seg7-review3-archive；归档receipt d0079933bc2520d2138413e29fc3d931e88221d37a77d5387d115e46f37b9d66。此前31条PLATE的逐路径语义、ROM扫描和值、metadata及native能力审计均继续有效；本轮只核唯一证据更正及全部冻结合同不变。

## 核验 (C1-C13)

| # | 检查 | 结果 | 备注 |
|---|---|---|---|
| C1 | 地址顺序/roadmap | ✅ | [080bc71c,080bda7c)，Seg-6已闭合，无回头/跳号。 |
| C2 | 完整布局/Rule2 | ✅ | 1880指令3950B+235word940B+35padding70B=4960B，无raw/carve/R4遗漏。 |
| C3 | 自主全ROM扫描 | ✅ | 独立滑动非对齐raw/odd扫描48targets/11entries的结果及证据未变；11入口even/odd holders均0，无5.1。 |
| C4 | ROM字节/值 | ✅ | 235slot和45标量独立原ROM核验保持，slots TSV字节精确不变。 |
| C5 | 常量复用/域 | ✅ | 1d30复用EQUIP_CHAIN_CANCEL_OFF，7fff为BGR555_WHITE；8new/2446objects、12510bindings完整map不变。 |
| C6 | 标签/碰撞 | ✅ | 170源标签形式/唯一性、204最终primary及命名域均保持。 |
| C7 | 完整metadata/接通 | ✅ | 62新增DATA、63旧identity/source保留、65switch保留；275states/48targets/31Fn与6746完整rich合同保持，静态ID/namespace/ABI不变。 |
| C8 | 当前名/持久来源 | ✅ | 5stable-ID rename/CSV5namecells/4canonical inventories/32registry闭包保持；C728仅registry，历史eval/closure和legacy快照只读。 |
| C9 | ASCII/长度 | ✅ | 31条PLATE/170EOL的ASCII和<=500审计保持；本轮plates TSV字节不变。 |
| C10 | native/指针/source投影 | ✅ | 40pins=19继承+8ANALYSISswitch+13PAL/VRAM，原生resolver/fallback实际27次执行证据保持；exporter不改，13槽无Equate兜底，偶数switch值保持。 |
| C11 | Function名与数量 | ✅ | init_banner_state等5新名成立；D870真实3 OAM，配对pack的6/12写入已正确，Function总数不增加。 |
| C12 | 全31PLATE语义/证据 | ✅ | 三轮已审的所有门槛、mask、return、phase、count/OAM数量闭合；本轮D870两处证据更正准确，见下。 |
| C13 | 残留/范围 | ✅ | 235槽/170auto/65switch完全覆盖，source171/current+copies及correctDB15/current+backup精确；84B旧正引用backlog不变。 |

## 状态: PASS

## 唯一剩余项的关闭证明

本轮独立读取原ROM与当前未改的汇编：

- D870 phase0 D8A8..D8F4仅在D8E8向BLDCNT写0xfd<<6=0x3f40。D918池字=0x04000050；其后推进phase并返回1，不写BLDALPHA。
- phase1的table entry为D920，D934向BLDALPHA写入；D980池字=0x04000052。
- phase3的table entry为D9D4，D9E8向BLDALPHA写入；DA38池字=0x04000052。

proposal第112行和semantic entry080bd870.evidence均已按此归属；decisions唯一同义evidence叶同步。未把证据更正扩大成任何运行/DB行为。

## 窄差异与既有证据保持

独立核验全部43个冻结记录的size/SHA。与第三轮归档逐字节比较：9个typed plans、full-ROM scan/function-holds证据、slots/plates两个TSV均不变；31PLATE、31Function-after、32registry、275state/204graph、globals、40pins、5rename闭包全保持。

semantic仅D870一条evidence变更；decisions仅相同evidence叶；proposal仅第112行替换，其他字节相等。source171当前与副本、correctDB15当前与备份再次逐文件精确相等。

既有独立证据包括round1 ROM/ref-identity审计、round2完整机械及原生能力执行、round2/round3全部31PLATE语义与窄差异审计。没有剩余修正项。此次PASS仅针对该冻结分析方案，后续ModeB实施、保存后独立检查及ROM逐字节验证按驱动流程执行。

未运行headless/build，未改proposal/TSV/plans/source/DB/progress/staging/commit。正式review及独立审计写毕后STOP。

## Reviewer Verdict: F15-Seg-7 = PASS
