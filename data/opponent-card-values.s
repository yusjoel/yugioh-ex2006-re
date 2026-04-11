@ =============================================================================
@ 对手卡值块数据（Opponent Card Values）
@ ROM偏移: 0x1E58D0E - 0x1E5906D（共 27 条目 × 32 字节 = 864 字节）
@
@ 每条目结构（32 字节）:
@   +0x00  2字节  card_value（卡牌实力值，SO code）
@   +0x02  2字节  unk（0x1F40 起递增，用途不明）
@   +0x04  20字节 文件路径字符串（null-padded，如 deck/LV1_kuriboh.ydc）
@   +0x18  6字节  全零填充
@   +0x1E  2字节  unk_b（= unk + 1）
@
@ 来源文档: doc/um06-romhacking-resource/opponents-coinflip-screen.md
@ =============================================================================

opponent_card_values:
    @ --- Kuriboh ---
    .hword  4064    @ card_value: Kuriboh (密码: 40640057)
    .hword 0x1F40    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 49, 95, 107, 117, 114, 105, 98, 111, 104, 46, 121, 100, 99    @ "deck/LV1_kuriboh.ydc"
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F41    @ unk_b

    @ --- Scapegoat ---
    .hword  4818    @ card_value: Scapegoat (密码: 73915051)
    .hword 0x1F41    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 49, 95, 115, 117, 107, 101, 103, 111, 46, 121, 100, 99, 0    @ "deck/LV1_sukego.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F42    @ unk_b

    @ --- Skull Servant ---
    .hword  4030    @ card_value: Skull Servant (密码: 32274490)
    .hword 0x1F42    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 49, 95, 119, 97, 105, 116, 111, 46, 121, 100, 99, 0, 0    @ "deck/LV1_waito.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F43    @ unk_b

    @ --- Watapon ---
    .hword  6092    @ card_value: Watapon (密码: 87774234)
    .hword 0x1F43    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 49, 95, 119, 97, 116, 97, 112, 111, 110, 46, 121, 100, 99    @ "deck/LV1_watapon.ydc"
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F44    @ unk_b

    @ --- Pikeru ---
    .hword  5975    @ card_value: White Magician Pikeru (密码: 81383947)
    .hword 0x1F44    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 49, 95, 112, 105, 107, 101, 114, 117, 46, 121, 100, 99, 0    @ "deck/LV1_pikeru.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F45    @ unk_b

    @ --- Batteryman C ---
    .hword  6428    @ card_value: Batteryman C (密码: 19733961)
    .hword 0x1F45    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 50, 95, 100, 101, 110, 116, 105, 46, 121, 100, 99, 0, 0    @ "deck/LV2_denti.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F46    @ unk_b

    @ --- Ojama Yellow ---
    .hword  5811    @ card_value: Ojama Yellow (密码: 42941100)
    .hword 0x1F46    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 50, 95, 111, 106, 97, 109, 97, 46, 121, 100, 99, 0, 0    @ "deck/LV2_ojama.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F47    @ unk_b

    @ --- Goblin King ---
    .hword  5973    @ card_value: Goblin King (密码: 18590133)
    .hword 0x1F47    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 50, 95, 107, 105, 110, 103, 71, 46, 121, 100, 99, 0, 0    @ "deck/LV2_kingG.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F48    @ unk_b

    @ --- Des Frog ---
    .hword  6424    @ card_value: Des Frog (密码: 84451804)
    .hword 0x1F48    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 50, 95, 107, 97, 101, 114, 117, 46, 121, 100, 99, 0, 0    @ "deck/LV2_kaeru.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F49    @ unk_b

    @ --- Water Dragon ---
    .hword  6481    @ card_value: Water Dragon (密码: 85066822)
    .hword 0x1F49    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 50, 95, 119, 97, 116, 101, 114, 68, 46, 121, 100, 99, 0    @ "deck/LV2_waterD.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F4A    @ unk_b

    @ --- Red Eyes Darkness Dragon ---
    .hword  6292    @ card_value: Red-Eyes Darkness Dragon (密码: 96561011)
    .hword 0x1F4A    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 51, 95, 82, 101, 100, 69, 121, 101, 115, 46, 121, 100, 99    @ "deck/LV3_RedEyes.ydc"
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F4B    @ unk_b

    @ --- Vampire Genesis ---
    .hword  6293    @ card_value: Vampire Genesis (密码: 22056710)
    .hword 0x1F4B    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 51, 95, 118, 97, 109, 112, 46, 121, 100, 99, 0, 0, 0    @ "deck/LV3_vamp.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F4C    @ unk_b

    @ --- Infernal Flame Emperor ---
    .hword  6368    @ card_value: Infernal Flame Emperor (密码: 19847532)
    .hword 0x1F4C    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 51, 95, 102, 108, 97, 109, 101, 46, 121, 100, 99, 0, 0    @ "deck/LV3_flame.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F4D    @ unk_b

    @ --- Ocean Dragon Lord Neo D ---
    .hword  6376    @ card_value: Ocean Dragon Lord - Neo-Daedalus (密码: 10485110)
    .hword 0x1F4D    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 51, 95, 100, 97, 105, 100, 97, 114, 111, 115, 46, 121, 100    @ "deck/LV3_daidaros.yd"
    .byte 99, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F4E    @ unk_b

    @ --- Helios Duo Megiste ---
    .hword  6647    @ card_value: Helios Duo Megiste (密码: 80887952)
    .hword 0x1F4E    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 51, 95, 104, 101, 114, 105, 111, 115, 117, 46, 121, 100, 99    @ "deck/LV3_heriosu.ydc"
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F4F    @ unk_b

    @ --- Gilford the Legend ---
    .hword  6456    @ card_value: Gilford the Legend (密码: 69933858)
    .hword 0x1F4F    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 52, 95, 103, 105, 108, 102, 111, 46, 121, 100, 99, 0, 0    @ "deck/LV4_gilfo.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F50    @ unk_b

    @ --- Dark Eradicator Warlock ---
    .hword  6530    @ card_value: Dark Eradicator Warlock (密码: 29436665)
    .hword 0x1F50    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 52, 95, 107, 117, 114, 111, 109, 97, 100, 111, 117, 46, 121    @ "deck/LV4_kuromadou.y"
    .byte 100, 99, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F51    @ unk_b

    @ --- Guardian Exode ---
    .hword  6640    @ card_value: Guardian Exode (密码: 55737443)
    .hword 0x1F51    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 52, 95, 101, 120, 111, 100, 111, 46, 121, 100, 99, 0, 0    @ "deck/LV4_exodo.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F52    @ unk_b

    @ --- Goldd Wu-Lord of Dark ---
    .hword  6505    @ card_value: Goldd, Wu-Lord of Dark World (密码: 78004197)
    .hword 0x1F52    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 52, 95, 97, 110, 107, 111, 107, 117, 107, 97, 105, 46, 121    @ "deck/LV4_ankokukai.y"
    .byte 100, 99, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F53    @ unk_b

    @ --- Elemental Hero Electrum ---
    .hword  6639    @ card_value: Elemental Hero Erikshieler (密码: 29343734)
    .hword 0x1F53    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 52, 95, 69, 104, 101, 114, 111, 46, 121, 100, 99, 0, 0    @ "deck/LV4_Ehero.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F54    @ unk_b

    @ --- Raviel Lord of Phantasms ---
    .hword  6565    @ card_value: Raviel, Lord of Phantasms (密码: 69890967)
    .hword 0x1F54    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 53, 95, 114, 97, 118, 105, 101, 114, 117, 46, 121, 100, 99    @ "deck/LV5_ravieru.ydc"
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F55    @ unk_b

    @ --- Horus the Black Flame D ---
    .hword  6100    @ card_value: Horus the Black Flame Dragon LV8 (密码: 48229808)
    .hword 0x1F55    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 53, 95, 104, 111, 114, 117, 115, 46, 121, 100, 99, 0, 0    @ "deck/LV5_horus.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F56    @ unk_b

    @ --- Stronghold ---
    .hword  6153    @ card_value: Stronghold (密码: 13955608)
    .hword 0x1F56    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 53, 95, 103, 97, 100, 103, 101, 116, 46, 121, 100, 99, 0    @ "deck/LV5_gadget.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F57    @ unk_b

    @ --- Sacred Phoenix of N ---
    .hword  6236    @ card_value: Sacred Phoenix of Nephthys (密码: 61441708)
    .hword 0x1F57    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 53, 95, 110, 101, 112, 104, 116, 104, 121, 115, 46, 121, 100    @ "deck/LV5_nephthys.yd"
    .byte 99, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F58    @ unk_b

    @ --- Cyber End Dragon ---
    .hword  6397    @ card_value: Cyber End Dragon (密码: 01546123)
    .hword 0x1F58    @ unk
    .byte 100, 101, 99, 107, 47, 76, 86, 53, 95, 99, 121, 98, 101, 114, 46, 121, 100, 99, 0, 0    @ "deck/LV5_cyber.ydc" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F59    @ unk_b

    @ --- Mirror Match ---
    .hword  4007    @ card_value: Mirror Match
    .hword 0x0000    @ unk
    .byte 100, 117, 109, 109, 121, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0    @ "dummy" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x1F5A    @ unk_b

    @ --- Copycat ---
    .hword  4795    @ card_value: Copycat (密码: 26376390)
    .hword 0x0000    @ unk
    .byte 100, 117, 109, 109, 121, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0    @ "dummy" + null-pad
    .byte 0, 0, 0, 0, 0, 0    @ 6字节填充
    .hword 0x2711    @ unk_b

