# Observation Pool

> 一次性观察候选。同主题 ≥ 2 次后晋升为 `~/.claude/projects/E--Workspace-yugioh-ex2006-re/memory/feedback_*.md`。
> 格式: `topic=<X>, scope=<ADDR>, date=YYYY-MM-DD, observation=<一句>`

---

- topic=unbounded-wrapper-pattern, scope=0x08014470, date=2026-05-02, observation=5 条指令的 thin wrapper 将大哨兵常量（0x05F5E0FF = 99,999,999）硬编码为 max 参数转发给 bounded callee；命名惯例 `<bounded_verb_obj>_unbounded`，置信度 high 可由函数体长度 + 哨兵魔数识别触发
- topic=rubric-role-boundary, scope=0x08014470, date=2026-05-02, observation=评分标准（R 条）若要求 executor 执行其角色边界外的动作（如 Ghidra rename），则首轮 PASSED 在结构上不可能；应将该类动作移至 fixer 落地 phase 作独立 pass/fail 红线，而非计入 R 评分
- topic=r7-module-prefix-instead-of-symbol, scope=0x0801455c, date=2026-05-02, observation=executor 在 plate 首句写了模块名前缀列表（"banlist、font_jp、game_str、settings 等多个模块…"）而非具体 caller 符号；R7 评分以 0 命中，fixer 改写为 `settings_080145bc`（muls r0,r4）+ `banlist_0801990c`（bl __modsi3）两个具名 caller；规则候选：plate 首句须出现 ≥ 1 个 `<symbol>_<hex>` 形式的具名 caller
- topic=sibling-cluster-fingerprint, scope=0x0801455c, date=2026-05-02, observation=三个兄弟函数（banlist_password_enter_char/copy_str_unbounded/count_str_charlen）共享完全相同的 EWRAM+0x6c2c 区域标志 + 0x0202348c 附加标志双检测序列及 bit7 双字节跳转逻辑；executor 在 R8 置信度证据中将"兄弟簇共享 IO/状态标志指纹"作为独立 L3 证据列出，有效提升 high 置信度的可信度
