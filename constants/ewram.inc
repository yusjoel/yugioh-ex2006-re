@ =============================================================================
@ EWRAM 变量符号常量
@ 数据来源: refs/datacrystal-um2006/ram-map.md
@           （TCRF Data Crystal wiki 的反汇编结论）
@
@ 用法: 在汇编里改写裸 .word 0x02029810 → ldr rN, =gBanlistPasswordBuffer
@      （或新代码里直接 ldr rN, =符号名）
@ =============================================================================

@ -----------------------------------------------------------------------------
@ 系统设置
@ -----------------------------------------------------------------------------
.equ gSettings,                  0x02006C2C  @ 1 B  各种设置；低 3 位为语言 ID
                                             @ language_id: 0=JP 1=EN 2=DE 3=FR 4=IT 5=ES

@ -----------------------------------------------------------------------------
@ 进度 / 数据
@ -----------------------------------------------------------------------------
.equ gMoneyDp,                   0x02006C38  @ 4 B  Money (DP)

.equ gDuelPuzzleProgress,        0x02006C3C  @ 140 B  35 × 4B
                                             @ byte0 bit1=Completed bit2=Failed
                                             @ 全 0 = sentinel 0x34BB13 (未完成)

.equ gLimitedDuelProgress,       0x02006CC8  @ 164 B  41 × 4B
                                             @ 0 = 未解锁；其余同上

.equ gThemeDuelScores,           0x02006D6C  @ 200 B  50 × 4B
                                             @ byte0 低 2 位为完成标志，其他位 + byte1..3 = high score

@ -----------------------------------------------------------------------------
@ 玩家 / 对手
@ -----------------------------------------------------------------------------
.equ gPlayerName,                0x02006E48  @ 14 B  玩家名（CP1252）
.equ gPlayerIcon,                0x02006E57  @ 1 B   玩家图标 ID（见 refs Notes）

.equ gUnlockedDuelists,          0x02006E5C  @ 8 B   已解锁对手位图

@ 对各 CPU 胜场（4 B 各，连续 27 项 = 108 B 总长，从 0x02006E60）
.equ gWinsBase,                  0x02006E60
.equ gWinsKuriboh,               0x02006E60
.equ gWinsScapegoat,             0x02006E64
.equ gWinsSkullServant,          0x02006E68
.equ gWinsWatapon,               0x02006E6C
.equ gWinsWhiteMagicianPikeru,   0x02006E70
.equ gWinsBatterymanC,           0x02006E74
.equ gWinsOjamaYellow,           0x02006E78
.equ gWinsGoblinKing,            0x02006E7C
.equ gWinsDesFrog,               0x02006E80
.equ gWinsWaterDragon,           0x02006E84
.equ gWinsRedEyesDarknessDragon, 0x02006E88
.equ gWinsVampireGenesis,        0x02006E8C
.equ gWinsInfernalFlameEmperor,  0x02006E90
.equ gWinsOceanDragonLord,       0x02006E94
.equ gWinsHeliosDuoMegiste,      0x02006E98
.equ gWinsGilfordTheLegend,      0x02006E9C
.equ gWinsDarkEradicatorWarlock, 0x02006EA0
.equ gWinsGuardianExode,         0x02006EA4
.equ gWinsGoldd,                 0x02006EA8
.equ gWinsElementalHeroErikshieler, 0x02006EAC
.equ gWinsRavielLordOfPhantasms, 0x02006EB0
.equ gWinsHorusLv8,              0x02006EB4
.equ gWinsStronghold,            0x02006EB8
.equ gWinsSacredPhoenix,         0x02006EBC
.equ gWinsCyberEndDragon,        0x02006EC0
.equ gWinsPlayer,                0x02006EC4
.equ gWinsCopycat,               0x02006EC8

@ -----------------------------------------------------------------------------
@ 决斗运行时
@ -----------------------------------------------------------------------------
.equ gP1LifePoints,              0x0201C4E0  @ 2 B  P1 LP
.equ gP2LifePoints,              0x0201CD48  @ 2 B  P2 LP

@ -----------------------------------------------------------------------------
@ 输入 / Banlist
@ -----------------------------------------------------------------------------
.equ gPlayerNameEntry,           0x02029512  @ 14 B  名字输入缓冲

.equ gBanlistPasswordBuffer,     0x02029810  @ 1440 B  禁卡密码输入
                                             @ 每 2 B 一项: [charset][character_id]
