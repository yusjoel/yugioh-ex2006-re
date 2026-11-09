# Refine Review: F15-Seg-5（Round 3）

## 状态: PASS

范围 `[080babd4,080bb3dc)`。本轮批准最终冻结 manifest SHA-256 `1a3f3ef7255c81b1f15906cbb77222e2089bf28682ed1fb019bf34b3f5dbeb29`。独立证据 `f15-seg5-review-round3-independent.json` SHA-256 `c7314c3abe4b580bdddb0cb6b85472f63cc4d030e7ab01231ff610d3f4d06919`。

开始前逐项验证24份round2归档，包含正式review SHA `0c4928662dc0bd39a6c33650dfe69bb0df053ae76496d6eedb183dcc22571dfb`及独立审计 SHA `1a09f9f60e27d77d44b3704c5289577c401450430c97ba633e4a9c2e0ab27442`，归档清单SHA `49655f20f9b7eb2351d90c68e4f1a4c4ebee7d68cb191e1be20527bb1e4d1fb3`。本轮仅检查唯一窄修及不变量，不重复无变化的深度分析。

## 核验 (C1–C13)

| # | 检查 | 结果 | 依据 |
|---|---|---|---|
| C1 | 地址序 | PASS | Seg-5范围与活动路线图一致 |
| C2 | 原始块归宿 | PASS | 48B R4及24B carve计划精确不变，无遗漏 |
| C3 | 全ROM引用 | PASS | 前两轮独立raw/odd/内点滑窗证据有效，相关扫描与引用计划本轮字节不变 |
| C4 | 值/几何 | PASS | 50槽字节和值、20指令40B+2池8B、carve6词及bookends合同不变 |
| C5 | 常量复用 | PASS | 复用已有DESCOVERY及04BBD0绑定，两个新增GAS定义计划和17pins保持 |
| C6 | 名称 | PASS | 50池/6carve及Function名称不变，格式与唯一性已通过 |
| C7 | after-rich闭合 | PASS | 上轮独立62节点图、两PC+BLS、holder/odd及BC71C的完整投影均字节不变 |
| C8 | 现名 | PASS | 无旧after名回归，现名与批准Symbol图一致 |
| C9 | ASCII | PASS | 全14 PLATE纯ASCII且≤500；BAED0新文本485字符及所有长度字段准确 |
| C10 | carve/THUMB | PASS | 三CID/三个odd callback、24B边界及最后pending回调迁移不变 |
| C11 | 名称/ABI | PASS | 两rename语义方向准确，旧ID/body/ABI与只读段外派生范围不变 |
| C12 | 语义 | PASS | BAED0最后提交域和selector/fallback修正已闭合，其他13行全文不变 |
| C13 | 残留/交接 | PASS | 48旧槽+2新池全部覆盖；历史84B正引用交接及17pins保持 |

## 唯一剩余项闭合

BAED0正式文本与第二轮已核准候选逐字符相同，485个ASCII字符，文本SHA-256 `d9d78f3b46086e816a3f928208ac9cc5cdd6a3136cd8db62bdba481b45fa885e`。对照未变更原指令确认：

- slot+8非零选eval gate，为零选blocked gate；结果须非零，summon须零，row callback须非零。
- 首轮槽扫描未提交后，fallback要求index≥0、unavailable非零，并固定使用blocked非零、summon零、callback非零。
- 首路径写 `gP1LifePoints+0x1d64=player`、`+0x1d58=1` activation count及target `(player,slot,0,3)`。
- fallback写 `gP1FieldArrayCBase+0x1c44=player`、`+0x1c38=1` ready及target `(player,11,index,3)`。成功给1，失败给0。

proposal仅BAED0同条说明改变并精确区分count/ready。formal仅BAED0的new_plate/new_plate_chars改变，Function plan仅同两字段，semantic plan仅同一plate改变；全部13个其它PLATE行和50槽精确不变。11份其余机器计划（含完整global、R4、carve、callback、holder、BC71C和17pins）与上轮字节完全一致。

## 批准输入与实施边界

- proposal SHA `770dc2329c60a2b898388e415a0e15e2a408ec4fcc00e437445db4feee75d257`。
- slots SHA `2a1ecac7afdb3ce776d0ad81748d72e94f4fe6906fa883c90cefb7722fe14b9a`。
- plates SHA `349ccf9651196cdf9dba8ba0678d7441e00e679e1e102fe7ce9890687c53309a`。

本轮再次独立核验34个摘要记录（32个不同路径）、161个当前及快照源码、15个当前及备份DB文件均一致。全局计划保持先前完整重算的2429对象/12359绑定/new5。持久化实施仍须绑定此冻结和准确fresh前态，执行受限事务、完整后验、保存后重读及ROM逐字节验证。本review只完成静态批准，未运行headless、修改DB/source、build、stage或commit。

## Reviewer Verdict: F15-Seg-5 = PASS
