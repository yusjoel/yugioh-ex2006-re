@ =============================================================================
@ 汇编宏定义
@ 文件: include/macros.inc
@ =============================================================================

@ -----------------------------------------------------------------------------
@ 卡牌属性代码（attr 字段，位于卡牌属性数据表 +0E 处）
@ -----------------------------------------------------------------------------
.equ ATTR_LIGHT,    1   @ 光
.equ ATTR_DARK,     2   @ 闇
.equ ATTR_WATER,    3   @ 水
.equ ATTR_FIRE,     4   @ 炎
.equ ATTR_EARTH,    5   @ 地
.equ ATTR_WIND,     6   @ 风
.equ ATTR_DIVINE,   7   @ 神
.equ ATTR_SPELL,    8   @ 魔法卡
.equ ATTR_TRAP,     9   @ 陷阱卡

@ -----------------------------------------------------------------------------
@ 种族代码（race 字段，位于卡牌属性数据表 +0C 处）
@ -----------------------------------------------------------------------------
.equ RACE_DRAGON,         1   @ 龙
.equ RACE_ZOMBIE,         2   @ 不死
.equ RACE_FIEND,          3   @ 恶魔
.equ RACE_PYRO,           4   @ 炎
.equ RACE_SEA_SERPENT,    5   @ 海龙
.equ RACE_ROCK,           6   @ 岩石
.equ RACE_MACHINE,        7   @ 机械
.equ RACE_FISH,           8   @ 鱼
.equ RACE_DINOSAUR,       9   @ 恐龙
.equ RACE_INSECT,        10   @ 昆虫
.equ RACE_BEAST,         11   @ 兽
.equ RACE_BEAST_WARRIOR, 12   @ 兽战士
.equ RACE_PLANT,         13   @ 植物
.equ RACE_AQUA,          14   @ 水
.equ RACE_WARRIOR,       15   @ 战士
.equ RACE_WINGED_BEAST,  16   @ 鸟兽
.equ RACE_FAIRY,         17   @ 天使
.equ RACE_SPELLCASTER,   18   @ 魔法使
.equ RACE_THUNDER,       19   @ 雷
.equ RACE_REPTILE,       20   @ 爬虫
.equ RACE_DIVINE_BEAST,  21   @ 幻神兽
.equ RACE_SPELL,         22   @ 魔法卡（等同 ATTR_SPELL，表中重复存储）
.equ RACE_TRAP,          23   @ 陷阱卡（等同 ATTR_TRAP，表中重复存储）

@ -----------------------------------------------------------------------------
@ 卡种类代码（subtype 字段，位于卡牌属性数据表 +10 处）
@ -----------------------------------------------------------------------------
.equ SUBTYPE_NORMAL,          0   @ 通常怪兽 / 通常魔法 / 通常陷阱
.equ SUBTYPE_EFFECT,          1   @ 效果怪兽
.equ SUBTYPE_FUSION,          2   @ 融合怪兽（通常）
.equ SUBTYPE_FUSION_EFFECT,   3   @ 融合/效果怪兽
.equ SUBTYPE_RITUAL,          4   @ 仪式怪兽
.equ SUBTYPE_RITUAL_EFFECT,   5   @ 仪式/效果怪兽
.equ SUBTYPE_TOON,            6   @ 动画版怪兽
.equ SUBTYPE_SPIRIT,          7   @ 灵魂怪兽
.equ SUBTYPE_UNION,           8   @ 同盟怪兽
.equ SUBTYPE_TOKEN,           9   @ 代币
.equ SUBTYPE_SPELL_CARD,     13   @ 魔法卡
.equ SUBTYPE_TRAP_CARD,      14   @ 陷阱卡

@ -----------------------------------------------------------------------------
@ 魔法/陷阱细分代码（spsub 字段，位于卡牌属性数据表 +14 处）
@ 对怪兽恒为 0
@ -----------------------------------------------------------------------------
.equ SPSUB_NORMAL,       0   @ 通常（怪兽 / 通常魔法 / 通常陷阱）
.equ SPSUB_COUNTER,      1   @ 反击陷阱
.equ SPSUB_FIELD,        2   @ 场地魔法
.equ SPSUB_EQUIP,        3   @ 装备魔法
.equ SPSUB_CONTINUOUS,   4   @ 永续魔法 / 永续陷阱
.equ SPSUB_QUICK_PLAY,   5   @ 速攻魔法
.equ SPSUB_RITUAL,       6   @ 仪式魔法

@ -----------------------------------------------------------------------------
@ 卡牌属性数据表记录宏
@ ROM 偏移: 0x018169B6，每条 22 字节（11 × uint16 LE），共 5170 条
@
@ 字段布局（括号内为字节偏移）：
@   zero0   (+00)  保留，恒 0（首条记录例外，为 0x0020）
@   slot_id (+02)  卡槽编号
@   copy    (+04)  異画索引（0=主图，1/2/3=异画）
@   flags   (+06)  标志（通常为 1；为 0 时表示哑元槽位；为 3 时含义待定）
@   atk     (+08)  攻击力（魔法/陷阱卡为 0）
@   def     (+0A)  守备力（魔法/陷阱卡为 0）
@   level   (+0C)  星数（魔法/陷阱卡为 0）
@   race    (+0E)  种族（RACE_DRAGON 等；魔法=RACE_SPELL, 陷阱=RACE_TRAP）
@   attr    (+10)  属性（ATTR_LIGHT 等；魔法=ATTR_SPELL, 陷阱=ATTR_TRAP）
@   subtype (+12)  卡种类（SUBTYPE_NORMAL/EFFECT/FUSION...SPELL_CARD/TRAP_CARD）
@   spsub   (+14)  魔法/陷阱细分（SPSUB_NORMAL/EQUIP/FIELD/CONTINUOUS 等）
@ -----------------------------------------------------------------------------
.macro card_stat zero0, slot_id, copy, flags, atk, def, level, race, attr, subtype, spsub
    .hword \zero0, \slot_id, \copy, \flags, \atk, \def, \level, \race, \attr, \subtype, \spsub
.endm

@ card_stat_zero - 全零/哑元槽位记录（slot_id=0）
@ 参数 zero0 默认为 0，首条记录特殊值为 0x0020
.macro card_stat_zero zero0=0
    .hword \zero0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
.endm

@ 预组条目宏
@ 参数:
@   so_code - 卡牌内部编号（十进制整数，如 4088 = 真红眼黑龙）
@   qty     - 副本数量（1、2 或 3）
@ 编码格式: [so_code * 4 | qty][0x0000]（共 4 字节，小端序）
@ 示例: deck_entry 4088, 1    @ Red-Eyes B. Dragon
.macro deck_entry so_code:req, qty:req
    .hword (\so_code * 4) | \qty, 0
.endm

@ 禁卡表条目宏
@ 参数:
@   so_code - 卡牌内部编号（十进制整数）
@   limit   - 限制数量（0 = 禁止，1 = 限制，2 = 准限制）
@ 编码格式: [so_code][limit]（各 2 字节，小端序）
@ 示例: banlist_entry 4088, 1    @ Red-Eyes B. Dragon 限制
.macro banlist_entry so_code:req, limit:req
    .hword \so_code, \limit
.endm

@ 对手/初始卡组条目宏
@ 参数:
@   so_code - 卡牌内部编号（十进制整数）
@ 编码格式: [so_code]（2 字节，小端序）
@ 重复多次表示多张副本
@ 示例: deck_card 4088    @ Red-Eyes B. Dragon
.macro deck_card so_code:req
    .hword \so_code
.endm

@ 卡包卡牌列表条目宏
@ 参数:
@   slot_id - 卡槽编号（十六进制，与 card-names.s 标签一致）
@   rarity  - 稀有度编码
@             0x00=Common, 0x04=Secret, 0x05=Secret(alt art),
@             0x08=Ultra, 0x0C=Super, 0x10=Rare
@ 编码格式: [slot_id(u16)][rarity(u8)][0x00]（共 4 字节，小端序）
@ 示例: pack_card_entry 0x0FA7, 0x08    @ Blue-Eyes White Dragon (Ultra)
.macro pack_card_entry slot_id:req, rarity:req
    .hword \slot_id
    .byte  \rarity, 0
.endm
