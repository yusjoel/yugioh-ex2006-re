# Observation Pool

> 一次性观察候选。同主题 ≥ 2 次后晋升为 `~/.claude/projects/E--Workspace-yugioh-ex2006-re/memory/feedback_*.md`。
> 格式: `topic=<X>, scope=<ADDR>, date=YYYY-MM-DD, observation=<一句>`

---

- topic=unbounded-wrapper-pattern, scope=0x08014470, date=2026-05-02, observation=5 条指令的 thin wrapper 将大哨兵常量（0x05F5E0FF = 99,999,999）硬编码为 max 参数转发给 bounded callee；命名惯例 `<bounded_verb_obj>_unbounded`，置信度 high 可由函数体长度 + 哨兵魔数识别触发
- topic=rubric-role-boundary, scope=0x08014470, date=2026-05-02, observation=评分标准（R 条）若要求 executor 执行其角色边界外的动作（如 Ghidra rename），则首轮 PASSED 在结构上不可能；应将该类动作移至 fixer 落地 phase 作独立 pass/fail 红线，而非计入 R 评分
- topic=r7-module-prefix-instead-of-symbol, scope=0x0801455c, date=2026-05-02, observation=executor 在 plate 首句写了模块名前缀列表（"banlist、font_jp、game_str、settings 等多个模块…"）而非具体 caller 符号；R7 评分以 0 命中，fixer 改写为 `settings_080145bc`（muls r0,r4）+ `banlist_0801990c`（bl __modsi3）两个具名 caller；规则候选：plate 首句须出现 ≥ 1 个 `<symbol>_<hex>` 形式的具名 caller
- topic=sibling-cluster-fingerprint, scope=0x0801455c, date=2026-05-02, observation=三个兄弟函数（banlist_password_enter_char/copy_str_unbounded/count_str_charlen）共享完全相同的 EWRAM+0x6c2c 区域标志 + 0x0202348c 附加标志双检测序列及 bit7 双字节跳转逻辑；executor 在 R8 置信度证据中将"兄弟簇共享 IO/状态标志指纹"作为独立 L3 证据列出，有效提升 high 置信度的可信度
- topic=assert-struct-field-name-leak, scope=0x08016afc, date=2026-05-02, observation=assert 条件串 `"pDst->nameID"` 直接泄露结构体字段名（含指针变量名 `pDst` + 字段名 `nameID`）；与路径串 `"GL/PRH_Main.c"` 配合精确定位参数类型为 PRH 条目指针、返回值语义为该字段索引的名称字符串；规则候选：assert 条件形如 `"ptr->field"` 或 `"struct.field"` → 即为免费的参数/字段名称锚，直接写入 R3 参数签名
- topic=resolve-indirection-ptr-naming, scope=0x08016afc, date=2026-05-02, observation=函数语义为"通过结构体字段 ID → 间接表查找 → 返回字符串指针"，命名为 `resolve_<scope>_<field>_ptr`；此命名范式适用于所有"读结构体字段作索引、走查找表、返回指针"的 leaf 查询函数；规则候选：动词 `resolve_` 比 `get_` 更准确表达"经过间接层解引用"语义
- topic=lib-prefix-function-naming, scope=0x08014eb4, date=2026-05-02, observation=函数内 assert 字符串显示源文件为 GL/GL_File.c（类似 SDK 或内部 library 的模块前缀），但 executor 正确拒绝使用 `gl_strstr` 命名：(a) 返回值是整数偏移不是指针（与 libc strstr 语义不同）；(b) peer 函数均不使用 GL 前缀；规则候选：library 命名空间前缀属于模块层，不应下推到单函数名，除非该前缀在整个 ROM 内被系统性使用
- topic=libc-name-disambiguation, scope=0x08014ea0, date=2026-05-02, observation=ROM 同时存在两个 strlen 实现：字对齐优化版 0x0810f0dc（已占用符号名 strlen）和朴素字节循环版 0x08014ea0；命名策略：用 `measure_*` / `naive_*` 前缀修饰语区分，确保两个实现都有唯一符号；模式：提案 libc 形函数名前应先 grep 确认标准符号未被更优化的 peer 占用
- topic=release-noop-assert-fingerprint, scope=0x080fa4dc, date=2026-05-02, observation=函数体仅 `bx lr`（2 字节）+ indeg=137 + 所有 callsite 均在条件失败分支传入 (file_path_str, line_no, expr_str, severity) 四参数 → release build 空断言处理器指纹；executor 识别模式：FID `bx lr` + indeg ≥ 30 + r0/r2 为 ROM 字符串指针（源文件路径 + 表达式串）→ 提议 `suppress_*` / `discard_*` / `noop_assert_*` 族名
- topic=local-sb-passed-pattern, scope=0x080fa4dc, date=2026-05-02, observation=函数整体 PASSED (45/45, confidence: high)，但参数 r3 的枚举语义在 release no-op 实现下静态不可验证，登记 SB-080fa4dc-1 仅限定于该参数行；SB 不等于函数级 BLOCKED——局部不确定性可用 "call-site 静态观察 / release no-op / 置信度 med" 格式隔离在参数行内，函数照常 PASSED
- topic=r3-noop-param-enum-qualification, scope=0x080fa4dc, date=2026-05-02, observation=当函数实现为 no-op (bx lr) 时，其参数所携带的枚举值在函数体内无可区分效果；正确的 R3 写法：类型 + call-site 静态枚举描述 + 限定语 "release build 下行为无差异 (均 no-op)" + 置信度 med；reviewer 首轮因缺此限定语扣 R3/R8 共 10 分，fixer 补全后两项均满分
- topic=med-confidence-r8-valid-grade, scope=0x080f1720, date=2026-05-02, observation=首个 med 置信度 one-shot PASSED (45/45)；reviewer 正确给 R8=5/5 因为 "诚实匹配" 原则成立——置信度字段的要求是与实际证据层级吻合，high 不是唯一能满分的答案；静态三层证据（数据 label + caller + 兄弟结构对比）无矛盾但缺 runtime，med 诚实且准确；规则候选：reviewer 不得因置信度是 med 而非 high 就扣 R8 分
- topic=plate-length-self-cap, scope=0x080f1440, date=2026-05-02, observation=executor 为 4 变体渲染函数写了 541 字 plate（硬限 500），R2=0；fixer 裁至 362 字仍保留三要素；规则候选：plate 实际安全上限约 400 字（留 100 字余量），complex 函数越复杂越应主动截短，而不是把每条分支路径都塞进 plate
- topic=symmetric-flag-bit-dispatch, scope=0x080f1440, date=2026-05-02, observation=caller `font_jp_080f21e8` 在 0x080f2930-0x080f2958 和 0x080f2644-0x080f266c 两段对称地测试同一 flag_bit（`[0x02006ed0+0x15] & 0x10`），为 0 调 8bpp 变体、为 1 调 4bpp 变体；规则候选：当 caller 内存在"单 flag_bit → 两个相邻 callee"的对称分支时，两个 callee 几乎必然是"同操作、不同渲染模式"变体，可作为 L6 兄弟对称证据直接提升置信度
