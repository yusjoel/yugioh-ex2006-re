# Observation Pool

> 一次性观察候选。同主题 ≥ 2 次后晋升为 `~/.claude/projects/E--Workspace-yugioh-ex2006-re/memory/feedback_*.md`。
> 格式: `topic=<X>, scope=<ADDR>, date=YYYY-MM-DD, observation=<一句>`

---

- topic=unbounded-wrapper-pattern, scope=0x08014470, date=2026-05-02, observation=5 条指令的 thin wrapper 将大哨兵常量（0x05F5E0FF = 99,999,999）硬编码为 max 参数转发给 bounded callee；命名惯例 `<bounded_verb_obj>_unbounded`，置信度 high 可由函数体长度 + 哨兵魔数识别触发
- topic=rubric-role-boundary, scope=0x08014470, date=2026-05-02, observation=评分标准（R 条）若要求 executor 执行其角色边界外的动作（如 Ghidra rename），则首轮 PASSED 在结构上不可能；应将该类动作移至 fixer 落地 phase 作独立 pass/fail 红线，而非计入 R 评分
- topic=r7-module-prefix-instead-of-symbol, scope=0x0801455c, date=2026-05-02, observation=executor 在 plate 首句写了模块名前缀列表（"banlist、font_jp、game_str、settings 等多个模块…"）而非具体 caller 符号；R7 评分以 0 命中，fixer 改写为 `settings_080145bc`（muls r0,r4）+ `banlist_0801990c`（bl __modsi3）两个具名 caller；规则候选：plate 首句须出现 ≥ 1 个 `<symbol>_<hex>` 形式的具名 caller
- topic=sibling-cluster-fingerprint, scope=0x0801455c, date=2026-05-02, observation=三个兄弟函数（banlist_password_enter_char/copy_str_unbounded/count_str_charlen）共享完全相同的 EWRAM+0x6c2c 区域标志 + 0x0202348c 附加标志双检测序列及 bit7 双字节跳转逻辑；executor 在 R8 置信度证据中将"兄弟簇共享 IO/状态标志指纹"作为独立 L3 证据列出，有效提升 high 置信度的可信度
- topic=leaf-utility-oneshot-pattern, scope=0x08014ea0, date=2026-05-02, observation=已确认第 2 次一次性 45/45：0x08014470 (copy_str_unbounded) 和 0x08014ea0 (measure_str_bytelen) 均在首轮无迭代通过；共性是"命名兄弟簇可见 + caller 含泄露字符串锚 + 纯叶子无副作用"；小叶子工具函数在具备上述三要素时极大概率 one-shot PASSED
- topic=libc-name-disambiguation, scope=0x08014ea0, date=2026-05-02, observation=ROM 同时存在两个 strlen 实现：字对齐优化版 0x0810f0dc（已占用符号名 strlen）和朴素字节循环版 0x08014ea0；命名策略：用 `measure_*` / `naive_*` 前缀修饰语区分，确保两个实现都有唯一符号；模式：提案 libc 形函数名前应先 grep 确认标准符号未被更优化的 peer 占用
