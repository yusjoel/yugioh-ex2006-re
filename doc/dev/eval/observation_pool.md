# Observation Pool

> 一次性观察候选。同主题 ≥ 2 次后晋升为 `~/.claude/projects/E--Workspace-yugioh-ex2006-re/memory/feedback_*.md`。
> 格式: `topic=<X>, scope=<ADDR>, date=YYYY-MM-DD, observation=<一句>`

---

- topic=unbounded-wrapper-pattern, scope=0x08014470, date=2026-05-02, observation=5 条指令的 thin wrapper 将大哨兵常量（0x05F5E0FF = 99,999,999）硬编码为 max 参数转发给 bounded callee；命名惯例 `<bounded_verb_obj>_unbounded`，置信度 high 可由函数体长度 + 哨兵魔数识别触发
- topic=rubric-role-boundary, scope=0x08014470, date=2026-05-02, observation=评分标准（R 条）若要求 executor 执行其角色边界外的动作（如 Ghidra rename），则首轮 PASSED 在结构上不可能；应将该类动作移至 fixer 落地 phase 作独立 pass/fail 红线，而非计入 R 评分
- topic=r7-module-prefix-instead-of-symbol, scope=0x0801455c, date=2026-05-02, observation=executor 在 plate 首句写了模块名前缀列表（"banlist、font_jp、game_str、settings 等多个模块…"）而非具体 caller 符号；R7 评分以 0 命中，fixer 改写为 `settings_080145bc`（muls r0,r4）+ `banlist_0801990c`（bl __modsi3）两个具名 caller；规则候选：plate 首句须出现 ≥ 1 个 `<symbol>_<hex>` 形式的具名 caller
- topic=sibling-cluster-fingerprint, scope=0x0801455c, date=2026-05-02, observation=三个兄弟函数（banlist_password_enter_char/copy_str_unbounded/count_str_charlen）共享完全相同的 EWRAM+0x6c2c 区域标志 + 0x0202348c 附加标志双检测序列及 bit7 双字节跳转逻辑；executor 在 R8 置信度证据中将"兄弟簇共享 IO/状态标志指纹"作为独立 L3 证据列出，有效提升 high 置信度的可信度
- topic=assert-path-cluster-anchor, scope=0x08014eb4, date=2026-05-02, observation=当 assert 字符串泄漏 `<module>/<file>.c` 路径时，同文件内的所有函数共享模块命名空间；`GL/GL_File.c` 锚点同时确定了 fs_load / find_substr_offset / measure_str_bytelen / suppress_assert_report 四函数的归属；模式：assert 路径形如 `<dir>/<file>.c` → 先 grep 全 ROM 找到所有引用该路径的函数 → 视为同一逻辑模块
- topic=lib-prefix-function-naming, scope=0x08014eb4, date=2026-05-02, observation=函数内 assert 字符串显示源文件为 GL/GL_File.c（类似 SDK 或内部 library 的模块前缀），但 executor 正确拒绝使用 `gl_strstr` 命名：(a) 返回值是整数偏移不是指针（与 libc strstr 语义不同）；(b) peer 函数均不使用 GL 前缀；规则候选：library 命名空间前缀属于模块层，不应下推到单函数名，除非该前缀在整个 ROM 内被系统性使用
- topic=libc-name-disambiguation, scope=0x08014ea0, date=2026-05-02, observation=ROM 同时存在两个 strlen 实现：字对齐优化版 0x0810f0dc（已占用符号名 strlen）和朴素字节循环版 0x08014ea0；命名策略：用 `measure_*` / `naive_*` 前缀修饰语区分，确保两个实现都有唯一符号；模式：提案 libc 形函数名前应先 grep 确认标准符号未被更优化的 peer 占用
- topic=release-noop-assert-fingerprint, scope=0x080fa4dc, date=2026-05-02, observation=函数体仅 `bx lr`（2 字节）+ indeg=137 + 所有 callsite 均在条件失败分支传入 (file_path_str, line_no, expr_str, severity) 四参数 → release build 空断言处理器指纹；executor 识别模式：FID `bx lr` + indeg ≥ 30 + r0/r2 为 ROM 字符串指针（源文件路径 + 表达式串）→ 提议 `suppress_*` / `discard_*` / `noop_assert_*` 族名
- topic=local-sb-passed-pattern, scope=0x080fa4dc, date=2026-05-02, observation=函数整体 PASSED (45/45, confidence: high)，但参数 r3 的枚举语义在 release no-op 实现下静态不可验证，登记 SB-080fa4dc-1 仅限定于该参数行；SB 不等于函数级 BLOCKED——局部不确定性可用 "call-site 静态观察 / release no-op / 置信度 med" 格式隔离在参数行内，函数照常 PASSED
- topic=r3-noop-param-enum-qualification, scope=0x080fa4dc, date=2026-05-02, observation=当函数实现为 no-op (bx lr) 时，其参数所携带的枚举值在函数体内无可区分效果；正确的 R3 写法：类型 + call-site 静态枚举描述 + 限定语 "release build 下行为无差异 (均 no-op)" + 置信度 med；reviewer 首轮因缺此限定语扣 R3/R8 共 10 分，fixer 补全后两项均满分
