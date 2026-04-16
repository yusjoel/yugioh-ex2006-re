@ =============================================================================
@ 卡包封面条幅图 (Pack Banners)
@ ROM偏移: 0x1CCE960 - 0x1CE822C (共 0x198CC = 104652 字节)
@
@ 格式: 8bpp raw OBJ tile, 32x64 像素 (4x8 tiles), 每 pack 0x800 字节
@ 加载函数: FUN_080db860 (mode 1, 2D stride copy: src 0x100/row, dest 0x400/row)
@ 初始化链: FUN_080d971c -> FUN_080d8e98 -> FUN_080d8f48 -> FUN_080db860
@ 图形文件由 tools/rom-export/export_pack_banners.py 从 ROM 导出 (不入库)
@ =============================================================================

@ -----------------------------------------------------------------------------
@ 指针表: 51 条目, 每条 4 字节 (GBA 绝对地址)
@ GBA地址: 0x09CCE960  ROM偏移: 0x1CCE960
@ -----------------------------------------------------------------------------
pack_banner_ptr_table:
        .word  pack_banner_00                       @ [ 0] LEGEND OF B.E.W.D.
        .word  pack_banner_01                       @ [ 1] RED MILLENIUM
        .word  pack_banner_02                       @ [ 2] BLUE MILLENIUM
        .word  pack_banner_03                       @ [ 3] BUSTER RANCHER
        .word  pack_banner_04                       @ [ 4] DARK MAGICIAN GIRL
        .word  pack_banner_05                       @ [ 5] HERO OF THE WIND
        .word  pack_banner_06                       @ [ 6] EMPEROR OF DARKNESS
        .word  pack_banner_07                       @ [ 7] GUARDIAN ANGEL
        .word  pack_banner_08                       @ [ 8] ARMOR OF LIGHT
        .word  pack_banner_09                       @ [ 9] DRAGONS OF FIRE
        .word  pack_banner_10                       @ [10] REVIVAL OF THE DEAD
        .word  pack_banner_11                       @ [11] MESSENGER OF PEACE
        .word  pack_banner_12                       @ [12] WARRIORS OF GLORY
        .word  pack_banner_13                       @ [13] CHAOTIC FIEND
        .word  pack_banner_14                       @ [14] DRAGONS OF LEGEND
        .word  pack_banner_15                       @ [15] SOUL OF THE WILD
        .word  pack_banner_16                       @ [16] FORCE OF NATURE
        .word  pack_banner_17                       @ [17] AQUA FORCES
        .word  pack_banner_18                       @ [18] DESTRUCTION KING
        .word  pack_banner_19                       @ [19] STALWART OGRE
        .word  pack_banner_20                       @ [20] LIGHT OF WISDOM
        .word  pack_banner_21                       @ [21] SHADOW OF POWER
        .word  pack_banner_22                       @ [22] DARK ENTITY
        .word  pack_banner_23                       @ [23] DARKNESS OF HELL
        .word  pack_banner_24                       @ [24] SWARM OF LOCUSTS
        .word  pack_banner_25                       @ [25] ANCIENT WEAPONS
        .word  pack_banner_26                       @ [26] ETERNAL WARRIOR
        .word  pack_banner_27                       @ [27] FORBIDDEN BEAST
        .word  pack_banner_28                       @ [28] KEEPER OF THE TOMB
        .word  pack_banner_29                       @ [29] DIMENSION OF CHAOS
        .word  pack_banner_30                       @ [30] MYSTICAL ARTS
        .word  pack_banner_31                       @ [31] THUNDER EMPEROR
        .word  pack_banner_32                       @ [32] INSECT KINGDOM
        .word  pack_banner_33                       @ [33] BLAZE OF FURY
        .word  pack_banner_34                       @ [34] GALE OF THE WIND
        .word  pack_banner_35                       @ [35] TIDAL SURGE
        .word  pack_banner_36                       @ [36] MASTER OF PUPPETS
        .word  pack_banner_37                       @ [37] HEAVENLY LIGHT
        .word  pack_banner_38                       @ [38] WICKED SHADOW
        .word  pack_banner_39                       @ [39] SEALED BEAST
        .word  pack_banner_40                       @ [40] SAVAGE BEAST
        .word  pack_banner_41                       @ [41] IRON FORTRESS
        .word  pack_banner_42                       @ [42] PHANTOM KNIGHT
        .word  pack_banner_43                       @ [43] CRYSTAL DRAGON
        .word  pack_banner_44                       @ [44] PRIMORDIAL FORCE
        .word  pack_banner_45                       @ [45] YU-GI-OH! GX
        .word  pack_banner_46                       @ [46] ELEMENTAL HERO
        .word  pack_banner_47                       @ [47] CHRYSALIS
        .word  pack_banner_48                       @ [48] ALIEN
        .word  pack_banner_49                       @ [49] CYBER LEGACY
        .word  pack_banner_50                       @ [50] ANCIENT GEAR

@ -----------------------------------------------------------------------------
@ Tile 数据: 51 x 0x800 字节
@ -----------------------------------------------------------------------------
pack_banner_00:                                     @ LEGEND OF B.E.W.D.
        .incbin "graphics/pack-banners/pack_00_banner.bin"
pack_banner_01:                                     @ RED MILLENIUM
        .incbin "graphics/pack-banners/pack_01_banner.bin"
pack_banner_02:                                     @ BLUE MILLENIUM
        .incbin "graphics/pack-banners/pack_02_banner.bin"
pack_banner_03:                                     @ BUSTER RANCHER
        .incbin "graphics/pack-banners/pack_03_banner.bin"
pack_banner_04:                                     @ DARK MAGICIAN GIRL
        .incbin "graphics/pack-banners/pack_04_banner.bin"
pack_banner_05:                                     @ HERO OF THE WIND
        .incbin "graphics/pack-banners/pack_05_banner.bin"
pack_banner_06:                                     @ EMPEROR OF DARKNESS
        .incbin "graphics/pack-banners/pack_06_banner.bin"
pack_banner_07:                                     @ GUARDIAN ANGEL
        .incbin "graphics/pack-banners/pack_07_banner.bin"
pack_banner_08:                                     @ ARMOR OF LIGHT
        .incbin "graphics/pack-banners/pack_08_banner.bin"
pack_banner_09:                                     @ DRAGONS OF FIRE
        .incbin "graphics/pack-banners/pack_09_banner.bin"
pack_banner_10:                                     @ REVIVAL OF THE DEAD
        .incbin "graphics/pack-banners/pack_10_banner.bin"
pack_banner_11:                                     @ MESSENGER OF PEACE
        .incbin "graphics/pack-banners/pack_11_banner.bin"
pack_banner_12:                                     @ WARRIORS OF GLORY
        .incbin "graphics/pack-banners/pack_12_banner.bin"
pack_banner_13:                                     @ CHAOTIC FIEND
        .incbin "graphics/pack-banners/pack_13_banner.bin"
pack_banner_14:                                     @ DRAGONS OF LEGEND
        .incbin "graphics/pack-banners/pack_14_banner.bin"
pack_banner_15:                                     @ SOUL OF THE WILD
        .incbin "graphics/pack-banners/pack_15_banner.bin"
pack_banner_16:                                     @ FORCE OF NATURE
        .incbin "graphics/pack-banners/pack_16_banner.bin"
pack_banner_17:                                     @ AQUA FORCES
        .incbin "graphics/pack-banners/pack_17_banner.bin"
pack_banner_18:                                     @ DESTRUCTION KING
        .incbin "graphics/pack-banners/pack_18_banner.bin"
pack_banner_19:                                     @ STALWART OGRE
        .incbin "graphics/pack-banners/pack_19_banner.bin"
pack_banner_20:                                     @ LIGHT OF WISDOM
        .incbin "graphics/pack-banners/pack_20_banner.bin"
pack_banner_21:                                     @ SHADOW OF POWER
        .incbin "graphics/pack-banners/pack_21_banner.bin"
pack_banner_22:                                     @ DARK ENTITY
        .incbin "graphics/pack-banners/pack_22_banner.bin"
pack_banner_23:                                     @ DARKNESS OF HELL
        .incbin "graphics/pack-banners/pack_23_banner.bin"
pack_banner_24:                                     @ SWARM OF LOCUSTS
        .incbin "graphics/pack-banners/pack_24_banner.bin"
pack_banner_25:                                     @ ANCIENT WEAPONS
        .incbin "graphics/pack-banners/pack_25_banner.bin"
pack_banner_26:                                     @ ETERNAL WARRIOR
        .incbin "graphics/pack-banners/pack_26_banner.bin"
pack_banner_27:                                     @ FORBIDDEN BEAST
        .incbin "graphics/pack-banners/pack_27_banner.bin"
pack_banner_28:                                     @ KEEPER OF THE TOMB
        .incbin "graphics/pack-banners/pack_28_banner.bin"
pack_banner_29:                                     @ DIMENSION OF CHAOS
        .incbin "graphics/pack-banners/pack_29_banner.bin"
pack_banner_30:                                     @ MYSTICAL ARTS
        .incbin "graphics/pack-banners/pack_30_banner.bin"
pack_banner_31:                                     @ THUNDER EMPEROR
        .incbin "graphics/pack-banners/pack_31_banner.bin"
pack_banner_32:                                     @ INSECT KINGDOM
        .incbin "graphics/pack-banners/pack_32_banner.bin"
pack_banner_33:                                     @ BLAZE OF FURY
        .incbin "graphics/pack-banners/pack_33_banner.bin"
pack_banner_34:                                     @ GALE OF THE WIND
        .incbin "graphics/pack-banners/pack_34_banner.bin"
pack_banner_35:                                     @ TIDAL SURGE
        .incbin "graphics/pack-banners/pack_35_banner.bin"
pack_banner_36:                                     @ MASTER OF PUPPETS
        .incbin "graphics/pack-banners/pack_36_banner.bin"
pack_banner_37:                                     @ HEAVENLY LIGHT
        .incbin "graphics/pack-banners/pack_37_banner.bin"
pack_banner_38:                                     @ WICKED SHADOW
        .incbin "graphics/pack-banners/pack_38_banner.bin"
pack_banner_39:                                     @ SEALED BEAST
        .incbin "graphics/pack-banners/pack_39_banner.bin"
pack_banner_40:                                     @ SAVAGE BEAST
        .incbin "graphics/pack-banners/pack_40_banner.bin"
pack_banner_41:                                     @ IRON FORTRESS
        .incbin "graphics/pack-banners/pack_41_banner.bin"
pack_banner_42:                                     @ PHANTOM KNIGHT
        .incbin "graphics/pack-banners/pack_42_banner.bin"
pack_banner_43:                                     @ CRYSTAL DRAGON
        .incbin "graphics/pack-banners/pack_43_banner.bin"
pack_banner_44:                                     @ PRIMORDIAL FORCE
        .incbin "graphics/pack-banners/pack_44_banner.bin"
pack_banner_45:                                     @ YU-GI-OH! GX
        .incbin "graphics/pack-banners/pack_45_banner.bin"
pack_banner_46:                                     @ ELEMENTAL HERO
        .incbin "graphics/pack-banners/pack_46_banner.bin"
pack_banner_47:                                     @ CHRYSALIS
        .incbin "graphics/pack-banners/pack_47_banner.bin"
pack_banner_48:                                     @ ALIEN
        .incbin "graphics/pack-banners/pack_48_banner.bin"
pack_banner_49:                                     @ CYBER LEGACY
        .incbin "graphics/pack-banners/pack_49_banner.bin"
pack_banner_50:                                     @ ANCIENT GEAR
        .incbin "graphics/pack-banners/pack_50_banner.bin"
