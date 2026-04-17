@ Cards IDs Array（internal_card_id → card_id 反向映射表）
@ 由 tools/rom-export/export_card_images.py 自动生成
@ ROM 范围: 0x15B7CCC - 0x15B94CC  (6144 B = 3072 × u16)
@
@ Lookup（per Data Crystal ROM map, function 0x080EE76C）:
@   index = (internal_card_id - 4007) << 1
@   card_id = cards_ids_array[index]
@   若 card_id == 0xFFFF 则该 internal_card_id 无对应卡。
@
@ internal_card_id 范围: 0x0FA7..0x1BA6 (4007..7078)

    .section .rodata
    .balign 2
    .global cards_ids_array
cards_ids_array:

    .hword 0x0001  @ icid=0x0FA7 ( 4007)  -> cid=1 slot=0x0FA7  Blue-Eyes White Dragon
    .hword 0x0005  @ icid=0x0FA8 ( 4008)  -> cid=5 slot=0x0FA8  Mystical Elf
    .hword 0x0006  @ icid=0x0FA9 ( 4009)  -> cid=6 slot=0x0FA9  Hitotsu-Me Giant
    .hword 0x0007  @ icid=0x0FAA ( 4010)  -> cid=7 slot=0x0FAA  Baby Dragon
    .hword 0x0008  @ icid=0x0FAB ( 4011)  -> cid=8 slot=0x0FAB  Ryu-Kishin
    .hword 0x0009  @ icid=0x0FAC ( 4012)  -> cid=9 slot=0x0FAC  Feral Imp
    .hword 0x000A  @ icid=0x0FAD ( 4013)  -> cid=10 slot=0x0FAD  Winged Dragon, Guardian of the Fortress #1
    .hword 0x000B  @ icid=0x0FAE ( 4014)  -> cid=11 slot=0x0FAE  Mushroom Man
    .hword 0xFFFF  @ icid=0x0FAF ( 4015)  -> (none)
    .hword 0x000C  @ icid=0x0FB0 ( 4016)  -> cid=12 slot=0x0FB0  Blackland Fire Dragon
    .hword 0xFFFF  @ icid=0x0FB1 ( 4017)  -> (none)
    .hword 0xFFFF  @ icid=0x0FB2 ( 4018)  -> (none)
    .hword 0x000D  @ icid=0x0FB3 ( 4019)  -> cid=13 slot=0x0FB3  Tyhone
    .hword 0xFFFF  @ icid=0x0FB4 ( 4020)  -> (none)
    .hword 0x000E  @ icid=0x0FB5 ( 4021)  -> cid=14 slot=0x0FB5  Flame Swordsman
    .hword 0x0010  @ icid=0x0FB6 ( 4022)  -> cid=16 slot=0x0FB6  Time Wizard
    .hword 0x0011  @ icid=0x0FB7 ( 4023)  -> cid=17 slot=0x0FB7  Right Leg of the Forbidden One
    .hword 0x0012  @ icid=0x0FB8 ( 4024)  -> cid=18 slot=0x0FB8  Left Leg of the Forbidden One
    .hword 0x0013  @ icid=0x0FB9 ( 4025)  -> cid=19 slot=0x0FB9  Right Arm of the Forbidden One
    .hword 0x0014  @ icid=0x0FBA ( 4026)  -> cid=20 slot=0x0FBA  Left Arm of the Forbidden One
    .hword 0x0015  @ icid=0x0FBB ( 4027)  -> cid=21 slot=0x0FBB  Exodia the Forbidden One
    .hword 0x0016  @ icid=0x0FBC ( 4028)  -> cid=22 slot=0x0FBC  Summoned Skull
    .hword 0x0019  @ icid=0x0FBD ( 4029)  -> cid=25 slot=0x0FBD  The Wicked Worm Beast
    .hword 0x001A  @ icid=0x0FBE ( 4030)  -> cid=26 slot=0x0FBE  Skull Servant
    .hword 0x001B  @ icid=0x0FBF ( 4031)  -> cid=27 slot=0x0FBF  Horn Imp
    .hword 0x001C  @ icid=0x0FC0 ( 4032)  -> cid=28 slot=0x0FC0  Battle Ox
    .hword 0x001D  @ icid=0x0FC1 ( 4033)  -> cid=29 slot=0x0FC1  Beaver Warrior
    .hword 0x001E  @ icid=0x0FC2 ( 4034)  -> cid=30 slot=0x0FC2  Rock Ogre Grotto #1
    .hword 0x001F  @ icid=0x0FC3 ( 4035)  -> cid=31 slot=0x0FC3  Mountain Warrior
    .hword 0x0020  @ icid=0x0FC4 ( 4036)  -> cid=32 slot=0x0FC4  Zombie Warrior
    .hword 0x0021  @ icid=0x0FC5 ( 4037)  -> cid=33 slot=0x0FC5  Koumori Dragon
    .hword 0x0022  @ icid=0x0FC6 ( 4038)  -> cid=34 slot=0x0FC6  Two-Headed King Rex
    .hword 0x0023  @ icid=0x0FC7 ( 4039)  -> cid=35 slot=0x0FC7  Judge Man
    .hword 0x0024  @ icid=0x0FC8 ( 4040)  -> cid=36 slot=0x0FC8  Saggi the Dark Clown
    .hword 0x0025  @ icid=0x0FC9 ( 4041)  -> cid=37 slot=0x0FC9  Dark Magician
    .hword 0x0028  @ icid=0x0FCA ( 4042)  -> cid=40 slot=0x0FCA  The Snake Hair
    .hword 0x0029  @ icid=0x0FCB ( 4043)  -> cid=41 slot=0x0FCB  Gaia the Dragon Champion
    .hword 0x002A  @ icid=0x0FCC ( 4044)  -> cid=42 slot=0x0FCC  Gaia The Fierce Knight
    .hword 0x002C  @ icid=0x0FCD ( 4045)  -> cid=44 slot=0x0FCD  Curse of Dragon
    .hword 0xFFFF  @ icid=0x0FCE ( 4046)  -> (none)
    .hword 0x002D  @ icid=0x0FCF ( 4047)  -> cid=45 slot=0x0FCF  Celtic Guardian
    .hword 0x002F  @ icid=0x0FD0 ( 4048)  -> cid=47 slot=0x0FD0  Illusionist Faceless Mage
    .hword 0x0030  @ icid=0x0FD1 ( 4049)  -> cid=48 slot=0x0FD1  Karbonala Warrior
    .hword 0x0031  @ icid=0x0FD2 ( 4050)  -> cid=49 slot=0x0FD2  Rogue Doll
    .hword 0x0032  @ icid=0x0FD3 ( 4051)  -> cid=50 slot=0x0FD3  Oscillo Hero #2
    .hword 0x0033  @ icid=0x0FD4 ( 4052)  -> cid=51 slot=0x0FD4  Griffore
    .hword 0x0034  @ icid=0x0FD5 ( 4053)  -> cid=52 slot=0x0FD5  Torike
    .hword 0x0035  @ icid=0x0FD6 ( 4054)  -> cid=53 slot=0x0FD6  Sangan
    .hword 0x0036  @ icid=0x0FD7 ( 4055)  -> cid=54 slot=0x0FD7  Big Insect
    .hword 0x0037  @ icid=0x0FD8 ( 4056)  -> cid=55 slot=0x0FD8  Basic Insect
    .hword 0x0038  @ icid=0x0FD9 ( 4057)  -> cid=56 slot=0x0FD9  Armored Lizard
    .hword 0xFFFF  @ icid=0x0FDA ( 4058)  -> (none)
    .hword 0x0039  @ icid=0x0FDB ( 4059)  -> cid=57 slot=0x0FDB  Killer Needle
    .hword 0x003A  @ icid=0x0FDC ( 4060)  -> cid=58 slot=0x0FDC  Gokibore
    .hword 0x003B  @ icid=0x0FDD ( 4061)  -> cid=59 slot=0x0FDD  Giant Flea
    .hword 0x003C  @ icid=0x0FDE ( 4062)  -> cid=60 slot=0x0FDE  Larvae Moth
    .hword 0x003D  @ icid=0x0FDF ( 4063)  -> cid=61 slot=0x0FDF  Great Moth
    .hword 0x003E  @ icid=0x0FE0 ( 4064)  -> cid=62 slot=0x0FE0  Kuriboh
    .hword 0x0041  @ icid=0x0FE1 ( 4065)  -> cid=65 slot=0x0FE1  Mammoth Graveyard
    .hword 0x0042  @ icid=0x0FE2 ( 4066)  -> cid=66 slot=0x0FE2  Great White
    .hword 0x0043  @ icid=0x0FE3 ( 4067)  -> cid=67 slot=0x0FE3  Wolf
    .hword 0x0044  @ icid=0x0FE4 ( 4068)  -> cid=68 slot=0x0FE4  Harpie Lady
    .hword 0x0045  @ icid=0x0FE5 ( 4069)  -> cid=69 slot=0x0FE5  Harpie Lady Sisters
    .hword 0x0046  @ icid=0x0FE6 ( 4070)  -> cid=70 slot=0x0FE6  Tiger Axe
    .hword 0x0048  @ icid=0x0FE7 ( 4071)  -> cid=72 slot=0x0FE7  Silver Fang
    .hword 0x0049  @ icid=0x0FE8 ( 4072)  -> cid=73 slot=0x0FE8  Kojikocy
    .hword 0x004A  @ icid=0x0FE9 ( 4073)  -> cid=74 slot=0x0FE9  Perfectly Ultimate Great Moth
    .hword 0xFFFF  @ icid=0x0FEA ( 4074)  -> (none)
    .hword 0x004B  @ icid=0x0FEB ( 4075)  -> cid=75 slot=0x0FEB  Thousand Dragon
    .hword 0x004D  @ icid=0x0FEC ( 4076)  -> cid=77 slot=0x0FEC  Fiend Kraken
    .hword 0x004E  @ icid=0x0FED ( 4077)  -> cid=78 slot=0x0FED  Jellyfish
    .hword 0x004F  @ icid=0x0FEE ( 4078)  -> cid=79 slot=0x0FEE  Cocoon of Evolution
    .hword 0xFFFF  @ icid=0x0FEF ( 4079)  -> (none)
    .hword 0x0050  @ icid=0x0FF0 ( 4080)  -> cid=80 slot=0x0FF0  Giant Soldier of Stone
    .hword 0x0051  @ icid=0x0FF1 ( 4081)  -> cid=81 slot=0x0FF1  Man-Eating Plant
    .hword 0x0052  @ icid=0x0FF2 ( 4082)  -> cid=82 slot=0x0FF2  Krokodilus
    .hword 0x0053  @ icid=0x0FF3 ( 4083)  -> cid=83 slot=0x0FF3  Grappler
    .hword 0x0054  @ icid=0x0FF4 ( 4084)  -> cid=84 slot=0x0FF4  Axe Raider
    .hword 0x0055  @ icid=0x0FF5 ( 4085)  -> cid=85 slot=0x0FF5  Megazowler
    .hword 0x0056  @ icid=0x0FF6 ( 4086)  -> cid=86 slot=0x0FF6  Uraby
    .hword 0x0057  @ icid=0x0FF7 ( 4087)  -> cid=87 slot=0x0FF7  Crawling Dragon #2
    .hword 0x0058  @ icid=0x0FF8 ( 4088)  -> cid=88 slot=0x0FF8  Red-Eyes B. Dragon
    .hword 0x005C  @ icid=0x0FF9 ( 4089)  -> cid=92 slot=0x0FF9  Castle of Dark Illusions
    .hword 0x005D  @ icid=0x0FFA ( 4090)  -> cid=93 slot=0x0FFA  Reaper of the Cards
    .hword 0x005E  @ icid=0x0FFB ( 4091)  -> cid=94 slot=0x0FFB  King of Yamimakai
    .hword 0x005F  @ icid=0x0FFC ( 4092)  -> cid=95 slot=0x0FFC  Barox
    .hword 0xFFFF  @ icid=0x0FFD ( 4093)  -> (none)
    .hword 0x0060  @ icid=0x0FFE ( 4094)  -> cid=96 slot=0x0FFE  Metal Guardian
    .hword 0x0061  @ icid=0x0FFF ( 4095)  -> cid=97 slot=0x0FFF  Catapult Turtle
    .hword 0x0062  @ icid=0x1000 ( 4096)  -> cid=98 slot=0x1000  Gyakutenno Megami
    .hword 0x0063  @ icid=0x1001 ( 4097)  -> cid=99 slot=0x1001  Mystic Horseman
    .hword 0x0064  @ icid=0x1002 ( 4098)  -> cid=100 slot=0x1002  Rabid Horseman
    .hword 0xFFFF  @ icid=0x1003 ( 4099)  -> (none)
    .hword 0xFFFF  @ icid=0x1004 ( 4100)  -> (none)
    .hword 0x0065  @ icid=0x1005 ( 4101)  -> cid=101 slot=0x1005  Crass Clown
    .hword 0x0066  @ icid=0x1006 ( 4102)  -> cid=102 slot=0x1006  Armored Zombie
    .hword 0x0067  @ icid=0x1007 ( 4103)  -> cid=103 slot=0x1007  Dragon Zombie
    .hword 0x0068  @ icid=0x1008 ( 4104)  -> cid=104 slot=0x1008  Clown Zombie
    .hword 0x0069  @ icid=0x1009 ( 4105)  -> cid=105 slot=0x1009  Pumpking the King of Ghosts
    .hword 0x006A  @ icid=0x100A ( 4106)  -> cid=106 slot=0x100A  Battle Warrior
    .hword 0x006B  @ icid=0x100B ( 4107)  -> cid=107 slot=0x100B  Wings of Wicked Flame
    .hword 0x006C  @ icid=0x100C ( 4108)  -> cid=108 slot=0x100C  Mask of Darkness
    .hword 0x006D  @ icid=0x100D ( 4109)  -> cid=109 slot=0x100D  Job-Change Mirror
    .hword 0x006E  @ icid=0x100E ( 4110)  -> cid=110 slot=0x100E  Curtain of the Dark Ones
    .hword 0xFFFF  @ icid=0x100F ( 4111)  -> (none)
    .hword 0xFFFF  @ icid=0x1010 ( 4112)  -> (none)
    .hword 0x006F  @ icid=0x1011 ( 4113)  -> cid=111 slot=0x1011  Kageningen
    .hword 0x0070  @ icid=0x1012 ( 4114)  -> cid=112 slot=0x1012  Graveyard and the Hand of Invitation
    .hword 0x0071  @ icid=0x1013 ( 4115)  -> cid=113 slot=0x1013  Goddess with the Third Eye
    .hword 0x0072  @ icid=0x1014 ( 4116)  -> cid=114 slot=0x1014  Hero of the East
    .hword 0xFFFF  @ icid=0x1015 ( 4117)  -> (none)
    .hword 0x0073  @ icid=0x1016 ( 4118)  -> cid=115 slot=0x1016  That Which Feeds on Life
    .hword 0x0074  @ icid=0x1017 ( 4119)  -> cid=116 slot=0x1017  Dark Gray
    .hword 0x0075  @ icid=0x1018 ( 4120)  -> cid=117 slot=0x1018  White Magical Hat
    .hword 0x0076  @ icid=0x1019 ( 4121)  -> cid=118 slot=0x1019  Kamionwizard
    .hword 0x0077  @ icid=0x101A ( 4122)  -> cid=119 slot=0x101A  Nightmare Scorpion
    .hword 0x0078  @ icid=0x101B ( 4123)  -> cid=120 slot=0x101B  Spirit of the Books
    .hword 0x0079  @ icid=0x101C ( 4124)  -> cid=121 slot=0x101C  Supporter in the Shadows
    .hword 0x007A  @ icid=0x101D ( 4125)  -> cid=122 slot=0x101D  Trial of Nightmare
    .hword 0x007B  @ icid=0x101E ( 4126)  -> cid=123 slot=0x101E  Dream Clown
    .hword 0x007C  @ icid=0x101F ( 4127)  -> cid=124 slot=0x101F  Sleeping Lion
    .hword 0x007D  @ icid=0x1020 ( 4128)  -> cid=125 slot=0x1020  Yamatano Dragon Scroll
    .hword 0xFFFF  @ icid=0x1021 ( 4129)  -> (none)
    .hword 0xFFFF  @ icid=0x1022 ( 4130)  -> (none)
    .hword 0x007E  @ icid=0x1023 ( 4131)  -> cid=126 slot=0x1023  Faith Bird
    .hword 0xFFFF  @ icid=0x1024 ( 4132)  -> (none)
    .hword 0xFFFF  @ icid=0x1025 ( 4133)  -> (none)
    .hword 0xFFFF  @ icid=0x1026 ( 4134)  -> (none)
    .hword 0x007F  @ icid=0x1027 ( 4135)  -> cid=127 slot=0x1027  Nemuriko
    .hword 0x0080  @ icid=0x1028 ( 4136)  -> cid=128 slot=0x1028  Weather Control
    .hword 0xFFFF  @ icid=0x1029 ( 4137)  -> (none)
    .hword 0x0081  @ icid=0x102A ( 4138)  -> cid=129 slot=0x102A  The 13th Grave
    .hword 0x0082  @ icid=0x102B ( 4139)  -> cid=130 slot=0x102B  Charubin the Fire Knight
    .hword 0x0083  @ icid=0x102C ( 4140)  -> cid=131 slot=0x102C  Mystical Capture Chain
    .hword 0x0084  @ icid=0x102D ( 4141)  -> cid=132 slot=0x102D  Fiend's Hand
    .hword 0x0085  @ icid=0x102E ( 4142)  -> cid=133 slot=0x102E  Witty Phantom
    .hword 0xFFFF  @ icid=0x102F ( 4143)  -> (none)
    .hword 0x0086  @ icid=0x1030 ( 4144)  -> cid=134 slot=0x1030  Dragon Statue
    .hword 0x0087  @ icid=0x1031 ( 4145)  -> cid=135 slot=0x1031  Blue-Eyed Silver Zombie
    .hword 0x0088  @ icid=0x1032 ( 4146)  -> cid=136 slot=0x1032  Toad Master
    .hword 0x0089  @ icid=0x1033 ( 4147)  -> cid=137 slot=0x1033  Spiked Snail
    .hword 0x008A  @ icid=0x1034 ( 4148)  -> cid=138 slot=0x1034  Flame Manipulator
    .hword 0x008B  @ icid=0x1035 ( 4149)  -> cid=139 slot=0x1035  Necrolancer the Timelord
    .hword 0x008C  @ icid=0x1036 ( 4150)  -> cid=140 slot=0x1036  Djinn the Watcher of the Wind
    .hword 0x008D  @ icid=0x1037 ( 4151)  -> cid=141 slot=0x1037  The Bewitching Phantom Thief
    .hword 0x008E  @ icid=0x1038 ( 4152)  -> cid=142 slot=0x1038  Temple of Skulls
    .hword 0x008F  @ icid=0x1039 ( 4153)  -> cid=143 slot=0x1039  Monster Egg
    .hword 0x0090  @ icid=0x103A ( 4154)  -> cid=144 slot=0x103A  The Shadow Who Controls the Dark
    .hword 0x0091  @ icid=0x103B ( 4155)  -> cid=145 slot=0x103B  Lord of the Lamp
    .hword 0xFFFF  @ icid=0x103C ( 4156)  -> (none)
    .hword 0x0092  @ icid=0x103D ( 4157)  -> cid=146 slot=0x103D  Rhaimundos of the Red Sword
    .hword 0x0093  @ icid=0x103E ( 4158)  -> cid=147 slot=0x103E  The Melting Red Shadow
    .hword 0x0094  @ icid=0x103F ( 4159)  -> cid=148 slot=0x103F  Dokuroizo the Grim Reaper
    .hword 0x0095  @ icid=0x1040 ( 4160)  -> cid=149 slot=0x1040  Fire Reaper
    .hword 0x0096  @ icid=0x1041 ( 4161)  -> cid=150 slot=0x1041  Larvas
    .hword 0x0097  @ icid=0x1042 ( 4162)  -> cid=151 slot=0x1042  Hard Armor
    .hword 0x0098  @ icid=0x1043 ( 4163)  -> cid=152 slot=0x1043  Firegrass
    .hword 0x0099  @ icid=0x1044 ( 4164)  -> cid=153 slot=0x1044  Man Eater
    .hword 0x009A  @ icid=0x1045 ( 4165)  -> cid=154 slot=0x1045  Dig Beak
    .hword 0x009B  @ icid=0x1046 ( 4166)  -> cid=155 slot=0x1046  M-Warrior #1
    .hword 0x009C  @ icid=0x1047 ( 4167)  -> cid=156 slot=0x1047  M-Warrior #2
    .hword 0xFFFF  @ icid=0x1048 ( 4168)  -> (none)
    .hword 0x009D  @ icid=0x1049 ( 4169)  -> cid=157 slot=0x1049  Lisark
    .hword 0x009E  @ icid=0x104A ( 4170)  -> cid=158 slot=0x104A  Lord of Zemia
    .hword 0x009F  @ icid=0x104B ( 4171)  -> cid=159 slot=0x104B  The Judgement Hand
    .hword 0x00A0  @ icid=0x104C ( 4172)  -> cid=160 slot=0x104C  Mysterious Puppeteer
    .hword 0xFFFF  @ icid=0x104D ( 4173)  -> (none)
    .hword 0x00A1  @ icid=0x104E ( 4174)  -> cid=161 slot=0x104E  Darkfire Dragon
    .hword 0x00A2  @ icid=0x104F ( 4175)  -> cid=162 slot=0x104F  Dark King of the Abyss
    .hword 0x00A3  @ icid=0x1050 ( 4176)  -> cid=163 slot=0x1050  Spirit of the Harp
    .hword 0xFFFF  @ icid=0x1051 ( 4177)  -> (none)
    .hword 0x00A4  @ icid=0x1052 ( 4178)  -> cid=164 slot=0x1052  Armaill
    .hword 0x00A5  @ icid=0x1053 ( 4179)  -> cid=165 slot=0x1053  Dark Prisoner
    .hword 0x00A6  @ icid=0x1054 ( 4180)  -> cid=166 slot=0x1054  Hurricail
    .hword 0xFFFF  @ icid=0x1055 ( 4181)  -> (none)
    .hword 0x00A7  @ icid=0x1056 ( 4182)  -> cid=167 slot=0x1056  Fire Eye
    .hword 0x00A8  @ icid=0x1057 ( 4183)  -> cid=168 slot=0x1057  Monsturtle
    .hword 0x00A9  @ icid=0x1058 ( 4184)  -> cid=169 slot=0x1058  Claw Reacher
    .hword 0x00AA  @ icid=0x1059 ( 4185)  -> cid=170 slot=0x1059  Phantom Dewan
    .hword 0x00AB  @ icid=0x105A ( 4186)  -> cid=171 slot=0x105A  Arlownay
    .hword 0x00AC  @ icid=0x105B ( 4187)  -> cid=172 slot=0x105B  Dark Shade
    .hword 0x00AD  @ icid=0x105C ( 4188)  -> cid=173 slot=0x105C  Masked Clown
    .hword 0x00AE  @ icid=0x105D ( 4189)  -> cid=174 slot=0x105D  Lucky Trinket
    .hword 0x00AF  @ icid=0x105E ( 4190)  -> cid=175 slot=0x105E  Genin
    .hword 0x00B0  @ icid=0x105F ( 4191)  -> cid=176 slot=0x105F  Eyearmor
    .hword 0x00B1  @ icid=0x1060 ( 4192)  -> cid=177 slot=0x1060  Fiend Reflection #2
    .hword 0x00B2  @ icid=0x1061 ( 4193)  -> cid=178 slot=0x1061  Gate Deeg
    .hword 0x00B3  @ icid=0x1062 ( 4194)  -> cid=179 slot=0x1062  Synchar
    .hword 0x00B4  @ icid=0x1063 ( 4195)  -> cid=180 slot=0x1063  Fusionist
    .hword 0x00B5  @ icid=0x1064 ( 4196)  -> cid=181 slot=0x1064  Akakieisu
    .hword 0x00B6  @ icid=0x1065 ( 4197)  -> cid=182 slot=0x1065  LaLa Li-oon
    .hword 0xFFFF  @ icid=0x1066 ( 4198)  -> (none)
    .hword 0x00B7  @ icid=0x1067 ( 4199)  -> cid=183 slot=0x1067  Turtle Tiger
    .hword 0x00B8  @ icid=0x1068 ( 4200)  -> cid=184 slot=0x1068  Terra the Terrible
    .hword 0x00B9  @ icid=0x1069 ( 4201)  -> cid=185 slot=0x1069  Doron
    .hword 0x00BA  @ icid=0x106A ( 4202)  -> cid=186 slot=0x106A  Arma Knight
    .hword 0xFFFF  @ icid=0x106B ( 4203)  -> (none)
    .hword 0x00BB  @ icid=0x106C ( 4204)  -> cid=187 slot=0x106C  Happy Lover
    .hword 0x00BC  @ icid=0x106D ( 4205)  -> cid=188 slot=0x106D  Penguin Knight
    .hword 0x00BD  @ icid=0x106E ( 4206)  -> cid=189 slot=0x106E  Petit Dragon
    .hword 0x00BE  @ icid=0x106F ( 4207)  -> cid=190 slot=0x106F  Frenzied Panda
    .hword 0x00BF  @ icid=0x1070 ( 4208)  -> cid=191 slot=0x1070  Archfiend Marmot of Nefariousness
    .hword 0x00C0  @ icid=0x1071 ( 4209)  -> cid=192 slot=0x1071  Phantom Ghost
    .hword 0xFFFF  @ icid=0x1072 ( 4210)  -> (none)
    .hword 0x00C1  @ icid=0x1073 ( 4211)  -> cid=193 slot=0x1073  Dorover
    .hword 0x00C2  @ icid=0x1074 ( 4212)  -> cid=194 slot=0x1074  Twin Long Rods #1
    .hword 0x00C3  @ icid=0x1075 ( 4213)  -> cid=195 slot=0x1075  Droll Bird
    .hword 0x00C4  @ icid=0x1076 ( 4214)  -> cid=196 slot=0x1076  Petit Angel
    .hword 0x00C5  @ icid=0x1077 ( 4215)  -> cid=197 slot=0x1077  Winged Cleaver
    .hword 0x00C6  @ icid=0x1078 ( 4216)  -> cid=198 slot=0x1078  Hinotama Soul
    .hword 0x00C7  @ icid=0x1079 ( 4217)  -> cid=199 slot=0x1079  Kaminarikozou
    .hword 0x00C8  @ icid=0x107A ( 4218)  -> cid=200 slot=0x107A  Meotoko
    .hword 0x00C9  @ icid=0x107B ( 4219)  -> cid=201 slot=0x107B  Aqua Madoor
    .hword 0x00CA  @ icid=0x107C ( 4220)  -> cid=202 slot=0x107C  Kagemusha of the Blue Flame
    .hword 0x00CB  @ icid=0x107D ( 4221)  -> cid=203 slot=0x107D  Flame Ghost
    .hword 0x00CC  @ icid=0x107E ( 4222)  -> cid=204 slot=0x107E  Dryad
    .hword 0x00CD  @ icid=0x107F ( 4223)  -> cid=205 slot=0x107F  B. Skull Dragon
    .hword 0x00CE  @ icid=0x1080 ( 4224)  -> cid=206 slot=0x1080  Two-Mouth Darkruler
    .hword 0x00CF  @ icid=0x1081 ( 4225)  -> cid=207 slot=0x1081  Solitude
    .hword 0x00D0  @ icid=0x1082 ( 4226)  -> cid=208 slot=0x1082  Masked Sorcerer
    .hword 0x00D1  @ icid=0x1083 ( 4227)  -> cid=209 slot=0x1083  Kumootoko
    .hword 0x00D2  @ icid=0x1084 ( 4228)  -> cid=210 slot=0x1084  Midnight Fiend
    .hword 0xFFFF  @ icid=0x1085 ( 4229)  -> (none)
    .hword 0x00D3  @ icid=0x1086 ( 4230)  -> cid=211 slot=0x1086  Trap Master
    .hword 0x00D4  @ icid=0x1087 ( 4231)  -> cid=212 slot=0x1087  Fiend Sword
    .hword 0x00D5  @ icid=0x1088 ( 4232)  -> cid=213 slot=0x1088  Skull Stalker
    .hword 0x00D6  @ icid=0x1089 ( 4233)  -> cid=214 slot=0x1089  Hitodenchak
    .hword 0x00D7  @ icid=0x108A ( 4234)  -> cid=215 slot=0x108A  Wood Remains
    .hword 0x00D8  @ icid=0x108B ( 4235)  -> cid=216 slot=0x108B  Hourglass of Life
    .hword 0x00D9  @ icid=0x108C ( 4236)  -> cid=217 slot=0x108C  Rare Fish
    .hword 0x00DA  @ icid=0x108D ( 4237)  -> cid=218 slot=0x108D  Wood Clown
    .hword 0x00DB  @ icid=0x108E ( 4238)  -> cid=219 slot=0x108E  Madjinn Gunn
    .hword 0x00DC  @ icid=0x108F ( 4239)  -> cid=220 slot=0x108F  Dark Titan of Terror
    .hword 0x00DD  @ icid=0x1090 ( 4240)  -> cid=221 slot=0x1090  Beautiful Headhuntress
    .hword 0xFFFF  @ icid=0x1091 ( 4241)  -> (none)
    .hword 0x00DE  @ icid=0x1092 ( 4242)  -> cid=222 slot=0x1092  Guardian of the Labyrinth
    .hword 0xFFFF  @ icid=0x1093 ( 4243)  -> (none)
    .hword 0x00DF  @ icid=0x1094 ( 4244)  -> cid=223 slot=0x1094  Yashinoki
    .hword 0x00E0  @ icid=0x1095 ( 4245)  -> cid=224 slot=0x1095  Vishwar Randi
    .hword 0x00E1  @ icid=0x1096 ( 4246)  -> cid=225 slot=0x1096  The Drdek
    .hword 0x00E2  @ icid=0x1097 ( 4247)  -> cid=226 slot=0x1097  Dark Assailant
    .hword 0x00E3  @ icid=0x1098 ( 4248)  -> cid=227 slot=0x1098  Candle of Fate
    .hword 0x00E4  @ icid=0x1099 ( 4249)  -> cid=228 slot=0x1099  Water Element
    .hword 0x00E5  @ icid=0x109A ( 4250)  -> cid=229 slot=0x109A  Dissolverock
    .hword 0x00E6  @ icid=0x109B ( 4251)  -> cid=230 slot=0x109B  Meda Bat
    .hword 0x00E7  @ icid=0x109C ( 4252)  -> cid=231 slot=0x109C  One Who Hunts Souls
    .hword 0x00E8  @ icid=0x109D ( 4253)  -> cid=232 slot=0x109D  Root Water
    .hword 0x00E9  @ icid=0x109E ( 4254)  -> cid=233 slot=0x109E  Master & Expert
    .hword 0x00EA  @ icid=0x109F ( 4255)  -> cid=234 slot=0x109F  Water Omotics
    .hword 0x00EB  @ icid=0x10A0 ( 4256)  -> cid=235 slot=0x10A0  Hyo
    .hword 0x00EC  @ icid=0x10A1 ( 4257)  -> cid=236 slot=0x10A1  Enchanting Mermaid
    .hword 0x00ED  @ icid=0x10A2 ( 4258)  -> cid=237 slot=0x10A2  Nekogal #1
    .hword 0x00EE  @ icid=0x10A3 ( 4259)  -> cid=238 slot=0x10A3  Fairywitch
    .hword 0x00EF  @ icid=0x10A4 ( 4260)  -> cid=239 slot=0x10A4  Embryonic Beast
    .hword 0x00F0  @ icid=0x10A5 ( 4261)  -> cid=240 slot=0x10A5  Prevent Rat
    .hword 0x00F1  @ icid=0x10A6 ( 4262)  -> cid=241 slot=0x10A6  Dimensional Warrior
    .hword 0x00F2  @ icid=0x10A7 ( 4263)  -> cid=242 slot=0x10A7  Stone Armadiller
    .hword 0x00F3  @ icid=0x10A8 ( 4264)  -> cid=243 slot=0x10A8  Beastking of the Swamps
    .hword 0x00F4  @ icid=0x10A9 ( 4265)  -> cid=244 slot=0x10A9  Ancient Sorcerer
    .hword 0x00F5  @ icid=0x10AA ( 4266)  -> cid=245 slot=0x10AA  Lunar Queen Elzaim
    .hword 0x00F6  @ icid=0x10AB ( 4267)  -> cid=246 slot=0x10AB  Wicked Mirror
    .hword 0x00F7  @ icid=0x10AC ( 4268)  -> cid=247 slot=0x10AC  The Little Swordsman of Aile
    .hword 0x00F8  @ icid=0x10AD ( 4269)  -> cid=248 slot=0x10AD  Rock Ogre Grotto #2
    .hword 0x00F9  @ icid=0x10AE ( 4270)  -> cid=249 slot=0x10AE  Wing Egg Elf
    .hword 0x00FA  @ icid=0x10AF ( 4271)  -> cid=250 slot=0x10AF  The Furious Sea King
    .hword 0x00FB  @ icid=0x10B0 ( 4272)  -> cid=251 slot=0x10B0  Princess of Tsurugi
    .hword 0x00FC  @ icid=0x10B1 ( 4273)  -> cid=252 slot=0x10B1  Unknown Warrior of Fiend
    .hword 0x00FD  @ icid=0x10B2 ( 4274)  -> cid=253 slot=0x10B2  Sectarian of Secrets
    .hword 0x00FE  @ icid=0x10B3 ( 4275)  -> cid=254 slot=0x10B3  Versago the Destroyer
    .hword 0x00FF  @ icid=0x10B4 ( 4276)  -> cid=255 slot=0x10B4  Wetha
    .hword 0x0100  @ icid=0x10B5 ( 4277)  -> cid=256 slot=0x10B5  Megirus Light
    .hword 0x0101  @ icid=0x10B6 ( 4278)  -> cid=257 slot=0x10B6  Mavelus
    .hword 0x0102  @ icid=0x10B7 ( 4279)  -> cid=258 slot=0x10B7  Ancient Tree of Enlightenment
    .hword 0x0103  @ icid=0x10B8 ( 4280)  -> cid=259 slot=0x10B8  Green Phantom King
    .hword 0x0104  @ icid=0x10B9 ( 4281)  -> cid=260 slot=0x10B9  Ground Attacker Bugroth
    .hword 0x0105  @ icid=0x10BA ( 4282)  -> cid=261 slot=0x10BA  Ray & Temperature
    .hword 0x0106  @ icid=0x10BB ( 4283)  -> cid=262 slot=0x10BB  Gorgon Egg
    .hword 0x0107  @ icid=0x10BC ( 4284)  -> cid=263 slot=0x10BC  Petit Moth
    .hword 0x0108  @ icid=0x10BD ( 4285)  -> cid=264 slot=0x10BD  King Fog
    .hword 0x0109  @ icid=0x10BE ( 4286)  -> cid=265 slot=0x10BE  Protector of the Throne
    .hword 0x010A  @ icid=0x10BF ( 4287)  -> cid=266 slot=0x10BF  Mystic Clown
    .hword 0x010B  @ icid=0x10C0 ( 4288)  -> cid=267 slot=0x10C0  Mystical Sheep #2
    .hword 0x010C  @ icid=0x10C1 ( 4289)  -> cid=268 slot=0x10C1  Holograh
    .hword 0x010D  @ icid=0x10C2 ( 4290)  -> cid=269 slot=0x10C2  Tao the Chanter
    .hword 0x010E  @ icid=0x10C3 ( 4291)  -> cid=270 slot=0x10C3  Serpent Marauder
    .hword 0xFFFF  @ icid=0x10C4 ( 4292)  -> (none)
    .hword 0x010F  @ icid=0x10C5 ( 4293)  -> cid=271 slot=0x10C5  Ogre of the Black Shadow
    .hword 0xFFFF  @ icid=0x10C6 ( 4294)  -> (none)
    .hword 0xFFFF  @ icid=0x10C7 ( 4295)  -> (none)
    .hword 0x0110  @ icid=0x10C8 ( 4296)  -> cid=272 slot=0x10C8  Moon Envoy
    .hword 0x0111  @ icid=0x10C9 ( 4297)  -> cid=273 slot=0x10C9  Fireyarou
    .hword 0x0112  @ icid=0x10CA ( 4298)  -> cid=274 slot=0x10CA  Psychic Kappa
    .hword 0x0113  @ icid=0x10CB ( 4299)  -> cid=275 slot=0x10CB  Masaki the Legendary Swordsman
    .hword 0x0114  @ icid=0x10CC ( 4300)  -> cid=276 slot=0x10CC  Dragoness the Wicked Knight
    .hword 0x0115  @ icid=0x10CD ( 4301)  -> cid=277 slot=0x10CD  Bio Plant
    .hword 0x0116  @ icid=0x10CE ( 4302)  -> cid=278 slot=0x10CE  One-Eyed Shield Dragon
    .hword 0x0117  @ icid=0x10CF ( 4303)  -> cid=279 slot=0x10CF  Cyber Soldier of Darkworld
    .hword 0x0118  @ icid=0x10D0 ( 4304)  -> cid=280 slot=0x10D0  Wicked Dragon with the Ersatz Head
    .hword 0x0119  @ icid=0x10D1 ( 4305)  -> cid=281 slot=0x10D1  Sonic Maid
    .hword 0x011A  @ icid=0x10D2 ( 4306)  -> cid=282 slot=0x10D2  Kurama
    .hword 0xFFFF  @ icid=0x10D3 ( 4307)  -> (none)
    .hword 0xFFFF  @ icid=0x10D4 ( 4308)  -> (none)
    .hword 0xFFFF  @ icid=0x10D5 ( 4309)  -> (none)
    .hword 0x011B  @ icid=0x10D6 ( 4310)  -> cid=283 slot=0x10D6  Axe of Despair
    .hword 0xFFFF  @ icid=0x10D7 ( 4311)  -> (none)
    .hword 0x011C  @ icid=0x10D8 ( 4312)  -> cid=284 slot=0x10D8  Insect Armor with Laser Cannon
    .hword 0xFFFF  @ icid=0x10D9 ( 4313)  -> (none)
    .hword 0xFFFF  @ icid=0x10DA ( 4314)  -> (none)
    .hword 0xFFFF  @ icid=0x10DB ( 4315)  -> (none)
    .hword 0xFFFF  @ icid=0x10DC ( 4316)  -> (none)
    .hword 0x011D  @ icid=0x10DD ( 4317)  -> cid=285 slot=0x10DD  Black Pendant
    .hword 0xFFFF  @ icid=0x10DE ( 4318)  -> (none)
    .hword 0x011E  @ icid=0x10DF ( 4319)  -> cid=286 slot=0x10DF  Horn of Light
    .hword 0x011F  @ icid=0x10E0 ( 4320)  -> cid=287 slot=0x10E0  Horn of the Unicorn
    .hword 0xFFFF  @ icid=0x10E1 ( 4321)  -> (none)
    .hword 0xFFFF  @ icid=0x10E2 ( 4322)  -> (none)
    .hword 0xFFFF  @ icid=0x10E3 ( 4323)  -> (none)
    .hword 0x0120  @ icid=0x10E4 ( 4324)  -> cid=288 slot=0x10E4  Elegant Egotist
    .hword 0xFFFF  @ icid=0x10E5 ( 4325)  -> (none)
    .hword 0x0121  @ icid=0x10E6 ( 4326)  -> cid=289 slot=0x10E6  Stop Defense
    .hword 0x0122  @ icid=0x10E7 ( 4327)  -> cid=290 slot=0x10E7  Malevolent Nuzzler
    .hword 0xFFFF  @ icid=0x10E8 ( 4328)  -> (none)
    .hword 0xFFFF  @ icid=0x10E9 ( 4329)  -> (none)
    .hword 0xFFFF  @ icid=0x10EA ( 4330)  -> (none)
    .hword 0xFFFF  @ icid=0x10EB ( 4331)  -> (none)
    .hword 0xFFFF  @ icid=0x10EC ( 4332)  -> (none)
    .hword 0xFFFF  @ icid=0x10ED ( 4333)  -> (none)
    .hword 0xFFFF  @ icid=0x10EE ( 4334)  -> (none)
    .hword 0x0123  @ icid=0x10EF ( 4335)  -> cid=291 slot=0x10EF  Dragon Capture Jar
    .hword 0x0124  @ icid=0x10F0 ( 4336)  -> cid=292 slot=0x10F0  Forest
    .hword 0x0125  @ icid=0x10F1 ( 4337)  -> cid=293 slot=0x10F1  Wasteland
    .hword 0x0126  @ icid=0x10F2 ( 4338)  -> cid=294 slot=0x10F2  Mountain
    .hword 0x0127  @ icid=0x10F3 ( 4339)  -> cid=295 slot=0x10F3  Sogen
    .hword 0x0128  @ icid=0x10F4 ( 4340)  -> cid=296 slot=0x10F4  Umi
    .hword 0x0129  @ icid=0x10F5 ( 4341)  -> cid=297 slot=0x10F5  Yami
    .hword 0x012A  @ icid=0x10F6 ( 4342)  -> cid=298 slot=0x10F6  Dark Hole
    .hword 0x012B  @ icid=0x10F7 ( 4343)  -> cid=299 slot=0x10F7  Raigeki
    .hword 0x012C  @ icid=0x10F8 ( 4344)  -> cid=300 slot=0x10F8  Mooyan Curry
    .hword 0x012D  @ icid=0x10F9 ( 4345)  -> cid=301 slot=0x10F9  Red Medicine
    .hword 0x012E  @ icid=0x10FA ( 4346)  -> cid=302 slot=0x10FA  Goblin's Secret Remedy
    .hword 0x012F  @ icid=0x10FB ( 4347)  -> cid=303 slot=0x10FB  Soul of the Pure
    .hword 0x0130  @ icid=0x10FC ( 4348)  -> cid=304 slot=0x10FC  Dian Keto the Cure Master
    .hword 0x0131  @ icid=0x10FD ( 4349)  -> cid=305 slot=0x10FD  Sparks
    .hword 0xFFFF  @ icid=0x10FE ( 4350)  -> (none)
    .hword 0xFFFF  @ icid=0x10FF ( 4351)  -> (none)
    .hword 0x0132  @ icid=0x1100 ( 4352)  -> cid=306 slot=0x1100  Ookazi
    .hword 0x0133  @ icid=0x1101 ( 4353)  -> cid=307 slot=0x1101  Tremendous Fire
    .hword 0x0134  @ icid=0x1102 ( 4354)  -> cid=308 slot=0x1102  Swords of Revealing Light
    .hword 0x0135  @ icid=0x1103 ( 4355)  -> cid=309 slot=0x1103  Spellbinding Circle
    .hword 0x0136  @ icid=0x1104 ( 4356)  -> cid=310 slot=0x1104  Dark-Piercing Light
    .hword 0x0137  @ icid=0x1105 ( 4357)  -> cid=311 slot=0x1105  Yaranzo
    .hword 0x0138  @ icid=0x1106 ( 4358)  -> cid=312 slot=0x1106  Kanan the Swordmistress
    .hword 0x0139  @ icid=0x1107 ( 4359)  -> cid=313 slot=0x1107  Takriminos
    .hword 0x013A  @ icid=0x1108 ( 4360)  -> cid=314 slot=0x1108  Stuffed Animal
    .hword 0xFFFF  @ icid=0x1109 ( 4361)  -> (none)
    .hword 0x013B  @ icid=0x110A ( 4362)  -> cid=315 slot=0x110A  Super War-Lion
    .hword 0xFFFF  @ icid=0x110B ( 4363)  -> (none)
    .hword 0xFFFF  @ icid=0x110C ( 4364)  -> (none)
    .hword 0x013C  @ icid=0x110D ( 4365)  -> cid=316 slot=0x110D  Three-Legged Zombies
    .hword 0x013D  @ icid=0x110E ( 4366)  -> cid=317 slot=0x110E  Zera The Mant
    .hword 0x013E  @ icid=0x110F ( 4367)  -> cid=318 slot=0x110F  Flying Penguin
    .hword 0x013F  @ icid=0x1110 ( 4368)  -> cid=319 slot=0x1110  Millennium Shield
    .hword 0x0141  @ icid=0x1111 ( 4369)  -> cid=321 slot=0x1111  Fairy's Gift
    .hword 0x0142  @ icid=0x1112 ( 4370)  -> cid=322 slot=0x1112  Black Luster Soldier
    .hword 0x0143  @ icid=0x1113 ( 4371)  -> cid=323 slot=0x1113  Fiend's Mirror
    .hword 0x0144  @ icid=0x1114 ( 4372)  -> cid=324 slot=0x1114  Labyrinth Wall
    .hword 0x0145  @ icid=0x1115 ( 4373)  -> cid=325 slot=0x1115  Jirai Gumo
    .hword 0x0146  @ icid=0x1116 ( 4374)  -> cid=326 slot=0x1116  Shadow Ghoul
    .hword 0x0147  @ icid=0x1117 ( 4375)  -> cid=327 slot=0x1117  Wall Shadow
    .hword 0x0148  @ icid=0x1118 ( 4376)  -> cid=328 slot=0x1118  Labyrinth Tank
    .hword 0x0149  @ icid=0x1119 ( 4377)  -> cid=329 slot=0x1119  Sanga of the Thunder
    .hword 0x014A  @ icid=0x111A ( 4378)  -> cid=330 slot=0x111A  Kazejin
    .hword 0x014B  @ icid=0x111B ( 4379)  -> cid=331 slot=0x111B  Suijin
    .hword 0x014C  @ icid=0x111C ( 4380)  -> cid=332 slot=0x111C  Gate Guardian
    .hword 0xFFFF  @ icid=0x111D ( 4381)  -> (none)
    .hword 0xFFFF  @ icid=0x111E ( 4382)  -> (none)
    .hword 0x014D  @ icid=0x111F ( 4383)  -> cid=333 slot=0x111F  Ryu-Kishin Powered
    .hword 0x014E  @ icid=0x1120 ( 4384)  -> cid=334 slot=0x1120  Swordstalker
    .hword 0x014F  @ icid=0x1121 ( 4385)  -> cid=335 slot=0x1121  La Jinn the Mystical Genie of the Lamp
    .hword 0x0151  @ icid=0x1122 ( 4386)  -> cid=337 slot=0x1122  Blue-Eyes Ultimate Dragon
    .hword 0x0153  @ icid=0x1123 ( 4387)  -> cid=339 slot=0x1123  Toon Alligator
    .hword 0xFFFF  @ icid=0x1124 ( 4388)  -> (none)
    .hword 0x0154  @ icid=0x1125 ( 4389)  -> cid=340 slot=0x1125  Parrot Dragon
    .hword 0x0155  @ icid=0x1126 ( 4390)  -> cid=341 slot=0x1126  Dark Rabbit
    .hword 0x0156  @ icid=0x1127 ( 4391)  -> cid=342 slot=0x1127  Bickuribox
    .hword 0x0157  @ icid=0x1128 ( 4392)  -> cid=343 slot=0x1128  Harpie's Pet Dragon
    .hword 0xFFFF  @ icid=0x1129 ( 4393)  -> (none)
    .hword 0x0158  @ icid=0x112A ( 4394)  -> cid=344 slot=0x112A  Pendulum Machine
    .hword 0x015A  @ icid=0x112B ( 4395)  -> cid=346 slot=0x112B  Giltia the D. Knight
    .hword 0x015B  @ icid=0x112C ( 4396)  -> cid=347 slot=0x112C  Launcher Spider
    .hword 0x015D  @ icid=0x112D ( 4397)  -> cid=349 slot=0x112D  Zoa
    .hword 0x015E  @ icid=0x112E ( 4398)  -> cid=350 slot=0x112E  Metalzoa
    .hword 0xFFFF  @ icid=0x112F ( 4399)  -> (none)
    .hword 0xFFFF  @ icid=0x1130 ( 4400)  -> (none)
    .hword 0xFFFF  @ icid=0x1131 ( 4401)  -> (none)
    .hword 0x015F  @ icid=0x1132 ( 4402)  -> cid=351 slot=0x1132  Ocubeam
    .hword 0xFFFF  @ icid=0x1133 ( 4403)  -> (none)
    .hword 0xFFFF  @ icid=0x1134 ( 4404)  -> (none)
    .hword 0xFFFF  @ icid=0x1135 ( 4405)  -> (none)
    .hword 0xFFFF  @ icid=0x1136 ( 4406)  -> (none)
    .hword 0xFFFF  @ icid=0x1137 ( 4407)  -> (none)
    .hword 0x0160  @ icid=0x1138 ( 4408)  -> cid=352 slot=0x1138  Monster Eye
    .hword 0xFFFF  @ icid=0x1139 ( 4409)  -> (none)
    .hword 0xFFFF  @ icid=0x113A ( 4410)  -> (none)
    .hword 0xFFFF  @ icid=0x113B ( 4411)  -> (none)
    .hword 0x0161  @ icid=0x113C ( 4412)  -> cid=353 slot=0x113C  Yaiba Robo
    .hword 0x0162  @ icid=0x113D ( 4413)  -> cid=354 slot=0x113D  Machine King
    .hword 0xFFFF  @ icid=0x113E ( 4414)  -> (none)
    .hword 0x0163  @ icid=0x113F ( 4415)  -> cid=355 slot=0x113F  Metal Dragon
    .hword 0xFFFF  @ icid=0x1140 ( 4416)  -> (none)
    .hword 0xFFFF  @ icid=0x1141 ( 4417)  -> (none)
    .hword 0x0164  @ icid=0x1142 ( 4418)  -> cid=356 slot=0x1142  Giga-Tech Wolf
    .hword 0xFFFF  @ icid=0x1143 ( 4419)  -> (none)
    .hword 0x0165  @ icid=0x1144 ( 4420)  -> cid=357 slot=0x1144  Shovel Crusher
    .hword 0x0166  @ icid=0x1145 ( 4421)  -> cid=358 slot=0x1145  Mechanicalchaser
    .hword 0x0167  @ icid=0x1146 ( 4422)  -> cid=359 slot=0x1146  Blocker
    .hword 0xFFFF  @ icid=0x1147 ( 4423)  -> (none)
    .hword 0x0168  @ icid=0x1148 ( 4424)  -> cid=360 slot=0x1148  Golgoil
    .hword 0xFFFF  @ icid=0x1149 ( 4425)  -> (none)
    .hword 0x0169  @ icid=0x114A ( 4426)  -> cid=361 slot=0x114A  Cyber-Stein
    .hword 0x016A  @ icid=0x114B ( 4427)  -> cid=362 slot=0x114B  Cyber Commander
    .hword 0x016B  @ icid=0x114C ( 4428)  -> cid=363 slot=0x114C  Jinzo #7
    .hword 0xFFFF  @ icid=0x114D ( 4429)  -> (none)
    .hword 0xFFFF  @ icid=0x114E ( 4430)  -> (none)
    .hword 0x016C  @ icid=0x114F ( 4431)  -> cid=364 slot=0x114F  Thunder Dragon
    .hword 0xFFFF  @ icid=0x1150 ( 4432)  -> (none)
    .hword 0x016D  @ icid=0x1151 ( 4433)  -> cid=365 slot=0x1151  Kaiser Dragon
    .hword 0x016E  @ icid=0x1152 ( 4434)  -> cid=366 slot=0x1152  Magician of Faith
    .hword 0x016F  @ icid=0x1153 ( 4435)  -> cid=367 slot=0x1153  Goddess of Whim
    .hword 0x0170  @ icid=0x1154 ( 4436)  -> cid=368 slot=0x1154  Water Magician
    .hword 0x0171  @ icid=0x1155 ( 4437)  -> cid=369 slot=0x1155  Ice Water
    .hword 0x0172  @ icid=0x1156 ( 4438)  -> cid=370 slot=0x1156  Waterdragon Fairy
    .hword 0x0173  @ icid=0x1157 ( 4439)  -> cid=371 slot=0x1157  Ancient Elf
    .hword 0xFFFF  @ icid=0x1158 ( 4440)  -> (none)
    .hword 0x0174  @ icid=0x1159 ( 4441)  -> cid=372 slot=0x1159  Water Girl
    .hword 0xFFFF  @ icid=0x115A ( 4442)  -> (none)
    .hword 0x0175  @ icid=0x115B ( 4443)  -> cid=373 slot=0x115B  Deepsea Shark
    .hword 0xFFFF  @ icid=0x115C ( 4444)  -> (none)
    .hword 0x0176  @ icid=0x115D ( 4445)  -> cid=374 slot=0x115D  Bottom Dweller
    .hword 0x0177  @ icid=0x115E ( 4446)  -> cid=375 slot=0x115E  7 Colored Fish
    .hword 0xFFFF  @ icid=0x115F ( 4447)  -> (none)
    .hword 0xFFFF  @ icid=0x1160 ( 4448)  -> (none)
    .hword 0xFFFF  @ icid=0x1161 ( 4449)  -> (none)
    .hword 0xFFFF  @ icid=0x1162 ( 4450)  -> (none)
    .hword 0x0178  @ icid=0x1163 ( 4451)  -> cid=376 slot=0x1163  Guardian of the Sea
    .hword 0x0179  @ icid=0x1164 ( 4452)  -> cid=377 slot=0x1164  Aqua Snake
    .hword 0x017A  @ icid=0x1165 ( 4453)  -> cid=378 slot=0x1165  Giant Red Seasnake
    .hword 0xFFFF  @ icid=0x1166 ( 4454)  -> (none)
    .hword 0xFFFF  @ icid=0x1167 ( 4455)  -> (none)
    .hword 0x017B  @ icid=0x1168 ( 4456)  -> cid=379 slot=0x1168  Kappa Avenger
    .hword 0x017C  @ icid=0x1169 ( 4457)  -> cid=380 slot=0x1169  Kanikabuto
    .hword 0x017D  @ icid=0x116A ( 4458)  -> cid=381 slot=0x116A  Zarigun
    .hword 0x017E  @ icid=0x116B ( 4459)  -> cid=382 slot=0x116B  Millennium Golem
    .hword 0x017F  @ icid=0x116C ( 4460)  -> cid=383 slot=0x116C  Destroyer Golem
    .hword 0x0180  @ icid=0x116D ( 4461)  -> cid=384 slot=0x116D  Barrel Rock
    .hword 0x0181  @ icid=0x116E ( 4462)  -> cid=385 slot=0x116E  Minomushi Warrior
    .hword 0x0182  @ icid=0x116F ( 4463)  -> cid=386 slot=0x116F  Stone Ghost
    .hword 0x0183  @ icid=0x1170 ( 4464)  -> cid=387 slot=0x1170  Kaminari Attack
    .hword 0x0184  @ icid=0x1171 ( 4465)  -> cid=388 slot=0x1171  Tripwire Beast
    .hword 0xFFFF  @ icid=0x1172 ( 4466)  -> (none)
    .hword 0x0185  @ icid=0x1173 ( 4467)  -> cid=389 slot=0x1173  Bolt Penguin
    .hword 0x0186  @ icid=0x1174 ( 4468)  -> cid=390 slot=0x1174  The Immortal of Thunder
    .hword 0x0187  @ icid=0x1175 ( 4469)  -> cid=391 slot=0x1175  Electric Snake
    .hword 0xFFFF  @ icid=0x1176 ( 4470)  -> (none)
    .hword 0x0188  @ icid=0x1177 ( 4471)  -> cid=392 slot=0x1177  Punished Eagle
    .hword 0x0189  @ icid=0x1178 ( 4472)  -> cid=393 slot=0x1178  Skull Red Bird
    .hword 0x018A  @ icid=0x1179 ( 4473)  -> cid=394 slot=0x1179  Crimson Sunbird
    .hword 0xFFFF  @ icid=0x117A ( 4474)  -> (none)
    .hword 0x018B  @ icid=0x117B ( 4475)  -> cid=395 slot=0x117B  Armed Ninja
    .hword 0x018C  @ icid=0x117C ( 4476)  -> cid=396 slot=0x117C  Magical Ghost
    .hword 0x018D  @ icid=0x117D ( 4477)  -> cid=397 slot=0x117D  Soul Hunter
    .hword 0xFFFF  @ icid=0x117E ( 4478)  -> (none)
    .hword 0x018E  @ icid=0x117F ( 4479)  -> cid=398 slot=0x117F  Vermillion Sparrow
    .hword 0x018F  @ icid=0x1180 ( 4480)  -> cid=399 slot=0x1180  Sea Kamen
    .hword 0x0190  @ icid=0x1181 ( 4481)  -> cid=400 slot=0x1181  Sinister Serpent
    .hword 0x0191  @ icid=0x1182 ( 4482)  -> cid=401 slot=0x1182  Ganigumo
    .hword 0x0192  @ icid=0x1183 ( 4483)  -> cid=402 slot=0x1183  Alinsection
    .hword 0x0193  @ icid=0x1184 ( 4484)  -> cid=403 slot=0x1184  Insect Soldiers of the Sky
    .hword 0x0194  @ icid=0x1185 ( 4485)  -> cid=404 slot=0x1185  Cockroach Knight
    .hword 0xFFFF  @ icid=0x1186 ( 4486)  -> (none)
    .hword 0x0195  @ icid=0x1187 ( 4487)  -> cid=405 slot=0x1187  Burglar
    .hword 0x0196  @ icid=0x1188 ( 4488)  -> cid=406 slot=0x1188  Pragtical
    .hword 0xFFFF  @ icid=0x1189 ( 4489)  -> (none)
    .hword 0x0197  @ icid=0x118A ( 4490)  -> cid=407 slot=0x118A  Ameba
    .hword 0x0198  @ icid=0x118B ( 4491)  -> cid=408 slot=0x118B  Korogashi
    .hword 0x0199  @ icid=0x118C ( 4492)  -> cid=409 slot=0x118C  Boo Koo
    .hword 0x019A  @ icid=0x118D ( 4493)  -> cid=410 slot=0x118D  Flower Wolf
    .hword 0x019B  @ icid=0x118E ( 4494)  -> cid=411 slot=0x118E  Rainbow Flower
    .hword 0x019C  @ icid=0x118F ( 4495)  -> cid=412 slot=0x118F  Barrel Lily
    .hword 0xFFFF  @ icid=0x1190 ( 4496)  -> (none)
    .hword 0xFFFF  @ icid=0x1191 ( 4497)  -> (none)
    .hword 0x019D  @ icid=0x1192 ( 4498)  -> cid=413 slot=0x1192  Hoshiningen
    .hword 0x019E  @ icid=0x1193 ( 4499)  -> cid=414 slot=0x1193  Maha Vailo
    .hword 0xFFFF  @ icid=0x1194 ( 4500)  -> (none)
    .hword 0x019F  @ icid=0x1195 ( 4501)  -> cid=415 slot=0x1195  Musician King
    .hword 0x01A0  @ icid=0x1196 ( 4502)  -> cid=416 slot=0x1196  Wilmee
    .hword 0xFFFF  @ icid=0x1197 ( 4503)  -> (none)
    .hword 0xFFFF  @ icid=0x1198 ( 4504)  -> (none)
    .hword 0xFFFF  @ icid=0x1199 ( 4505)  -> (none)
    .hword 0x01A1  @ icid=0x119A ( 4506)  -> cid=417 slot=0x119A  Dragon Seeker
    .hword 0x01A2  @ icid=0x119B ( 4507)  -> cid=418 slot=0x119B  Man-Eater Bug
    .hword 0x01A3  @ icid=0x119C ( 4508)  -> cid=419 slot=0x119C  D. Human
    .hword 0x01A4  @ icid=0x119D ( 4509)  -> cid=420 slot=0x119D  Turtle Raccoon
    .hword 0xFFFF  @ icid=0x119E ( 4510)  -> (none)
    .hword 0x01A5  @ icid=0x119F ( 4511)  -> cid=421 slot=0x119F  Prisman
    .hword 0xFFFF  @ icid=0x11A0 ( 4512)  -> (none)
    .hword 0x01A6  @ icid=0x11A1 ( 4513)  -> cid=422 slot=0x11A1  Crazy Fish
    .hword 0xFFFF  @ icid=0x11A2 ( 4514)  -> (none)
    .hword 0x01A7  @ icid=0x11A3 ( 4515)  -> cid=423 slot=0x11A3  Bracchio-raidus
    .hword 0x01A8  @ icid=0x11A4 ( 4516)  -> cid=424 slot=0x11A4  Laughing Flower
    .hword 0x01A9  @ icid=0x11A5 ( 4517)  -> cid=425 slot=0x11A5  Bean Soldier
    .hword 0x01AA  @ icid=0x11A6 ( 4518)  -> cid=426 slot=0x11A6  Cannon Soldier
    .hword 0x01AB  @ icid=0x11A7 ( 4519)  -> cid=427 slot=0x11A7  Guardian of the Throne Room
    .hword 0x01AC  @ icid=0x11A8 ( 4520)  -> cid=428 slot=0x11A8  Brave Scizzar
    .hword 0x01AD  @ icid=0x11A9 ( 4521)  -> cid=429 slot=0x11A9  The Statue of Easter Island
    .hword 0x01AE  @ icid=0x11AA ( 4522)  -> cid=430 slot=0x11AA  Muka Muka
    .hword 0xFFFF  @ icid=0x11AB ( 4523)  -> (none)
    .hword 0x01AF  @ icid=0x11AC ( 4524)  -> cid=431 slot=0x11AC  Boulder Tortoise
    .hword 0x01B0  @ icid=0x11AD ( 4525)  -> cid=432 slot=0x11AD  Fire Kraken
    .hword 0x01B1  @ icid=0x11AE ( 4526)  -> cid=433 slot=0x11AE  Turtle Bird
    .hword 0x01B2  @ icid=0x11AF ( 4527)  -> cid=434 slot=0x11AF  Skullbird
    .hword 0x01B3  @ icid=0x11B0 ( 4528)  -> cid=435 slot=0x11B0  Monstrous Bird
    .hword 0x01B4  @ icid=0x11B1 ( 4529)  -> cid=436 slot=0x11B1  The Bistro Butcher
    .hword 0x01B5  @ icid=0x11B2 ( 4530)  -> cid=437 slot=0x11B2  Star Boy
    .hword 0xFFFF  @ icid=0x11B3 ( 4531)  -> (none)
    .hword 0xFFFF  @ icid=0x11B4 ( 4532)  -> (none)
    .hword 0x01B6  @ icid=0x11B5 ( 4533)  -> cid=438 slot=0x11B5  Milus Radiant
    .hword 0xFFFF  @ icid=0x11B6 ( 4534)  -> (none)
    .hword 0x01B7  @ icid=0x11B7 ( 4535)  -> cid=439 slot=0x11B7  Flame Cerebrus
    .hword 0x01B8  @ icid=0x11B8 ( 4536)  -> cid=440 slot=0x11B8  Eldeen
    .hword 0x01B9  @ icid=0x11B9 ( 4537)  -> cid=441 slot=0x11B9  Mystical Sand
    .hword 0x01BA  @ icid=0x11BA ( 4538)  -> cid=442 slot=0x11BA  Gemini Elf
    .hword 0xFFFF  @ icid=0x11BB ( 4539)  -> (none)
    .hword 0x01BC  @ icid=0x11BC ( 4540)  -> cid=444 slot=0x11BC  Minar
    .hword 0x01BD  @ icid=0x11BD ( 4541)  -> cid=445 slot=0x11BD  Kamakiriman
    .hword 0x01BE  @ icid=0x11BE ( 4542)  -> cid=446 slot=0x11BE  Mechaleon
    .hword 0x01BF  @ icid=0x11BF ( 4543)  -> cid=447 slot=0x11BF  Mega Thunderball
    .hword 0x01C0  @ icid=0x11C0 ( 4544)  -> cid=448 slot=0x11C0  Niwatori
    .hword 0x01C1  @ icid=0x11C1 ( 4545)  -> cid=449 slot=0x11C1  Corroding Shark
    .hword 0x01C2  @ icid=0x11C2 ( 4546)  -> cid=450 slot=0x11C2  Skelengel
    .hword 0x01C3  @ icid=0x11C3 ( 4547)  -> cid=451 slot=0x11C3  Hane-Hane
    .hword 0xFFFF  @ icid=0x11C4 ( 4548)  -> (none)
    .hword 0x01C4  @ icid=0x11C5 ( 4549)  -> cid=452 slot=0x11C5  Tongyo
    .hword 0x01C5  @ icid=0x11C6 ( 4550)  -> cid=453 slot=0x11C6  Dharma Cannon
    .hword 0x01C6  @ icid=0x11C7 ( 4551)  -> cid=454 slot=0x11C7  Skelgon
    .hword 0x01C7  @ icid=0x11C8 ( 4552)  -> cid=455 slot=0x11C8  Wow Warrior
    .hword 0x01C8  @ icid=0x11C9 ( 4553)  -> cid=456 slot=0x11C9  Griggle
    .hword 0xFFFF  @ icid=0x11CA ( 4554)  -> (none)
    .hword 0x01C9  @ icid=0x11CB ( 4555)  -> cid=457 slot=0x11CB  Frog the Jam
    .hword 0x01CA  @ icid=0x11CC ( 4556)  -> cid=458 slot=0x11CC  Behegon
    .hword 0x01CB  @ icid=0x11CD ( 4557)  -> cid=459 slot=0x11CD  Dark Elf
    .hword 0x01CC  @ icid=0x11CE ( 4558)  -> cid=460 slot=0x11CE  Winged Dragon, Guardian of the Fortress #2
    .hword 0xFFFF  @ icid=0x11CF ( 4559)  -> (none)
    .hword 0xFFFF  @ icid=0x11D0 ( 4560)  -> (none)
    .hword 0xFFFF  @ icid=0x11D1 ( 4561)  -> (none)
    .hword 0x01CD  @ icid=0x11D2 ( 4562)  -> cid=461 slot=0x11D2  The Wandering Doomed
    .hword 0x01CE  @ icid=0x11D3 ( 4563)  -> cid=462 slot=0x11D3  Steel Ogre Grotto #1
    .hword 0xFFFF  @ icid=0x11D4 ( 4564)  -> (none)
    .hword 0x01CF  @ icid=0x11D5 ( 4565)  -> cid=463 slot=0x11D5  Oscillo Hero
    .hword 0x01D0  @ icid=0x11D6 ( 4566)  -> cid=464 slot=0x11D6  Invader from Another Dimension
    .hword 0x01D1  @ icid=0x11D7 ( 4567)  -> cid=465 slot=0x11D7  Lesser Dragon
    .hword 0x01D2  @ icid=0x11D8 ( 4568)  -> cid=466 slot=0x11D8  Needle Worm
    .hword 0x01D3  @ icid=0x11D9 ( 4569)  -> cid=467 slot=0x11D9  Wretched Ghost of the Attic
    .hword 0x01D4  @ icid=0x11DA ( 4570)  -> cid=468 slot=0x11DA  Great Mammoth of Goldfine
    .hword 0x01D5  @ icid=0x11DB ( 4571)  -> cid=469 slot=0x11DB  Man-eating Black Shark
    .hword 0x01D6  @ icid=0x11DC ( 4572)  -> cid=470 slot=0x11DC  Yormungarde
    .hword 0x01D7  @ icid=0x11DD ( 4573)  -> cid=471 slot=0x11DD  Darkworld Thorns
    .hword 0x01D8  @ icid=0x11DE ( 4574)  -> cid=472 slot=0x11DE  Anthrosaurus
    .hword 0x01D9  @ icid=0x11DF ( 4575)  -> cid=473 slot=0x11DF  Drooling Lizard
    .hword 0x01DA  @ icid=0x11E0 ( 4576)  -> cid=474 slot=0x11E0  Trakadon
    .hword 0x01DB  @ icid=0x11E1 ( 4577)  -> cid=475 slot=0x11E1  B. Dragon Jungle King
    .hword 0xFFFF  @ icid=0x11E2 ( 4578)  -> (none)
    .hword 0x01DC  @ icid=0x11E3 ( 4579)  -> cid=476 slot=0x11E3  Little D
    .hword 0x01DD  @ icid=0x11E4 ( 4580)  -> cid=477 slot=0x11E4  Witch of the Black Forest
    .hword 0xFFFF  @ icid=0x11E5 ( 4581)  -> (none)
    .hword 0x01DE  @ icid=0x11E6 ( 4582)  -> cid=478 slot=0x11E6  Giant Scorpion of the Tundra
    .hword 0xFFFF  @ icid=0x11E7 ( 4583)  -> (none)
    .hword 0xFFFF  @ icid=0x11E8 ( 4584)  -> (none)
    .hword 0x01DF  @ icid=0x11E9 ( 4585)  -> cid=479 slot=0x11E9  Abyss Flower
    .hword 0xFFFF  @ icid=0x11EA ( 4586)  -> (none)
    .hword 0x01E0  @ icid=0x11EB ( 4587)  -> cid=480 slot=0x11EB  Takuhee
    .hword 0xFFFF  @ icid=0x11EC ( 4588)  -> (none)
    .hword 0xFFFF  @ icid=0x11ED ( 4589)  -> (none)
    .hword 0x01E1  @ icid=0x11EE ( 4590)  -> cid=481 slot=0x11EE  Binding Chain
    .hword 0x01E2  @ icid=0x11EF ( 4591)  -> cid=482 slot=0x11EF  Mechanical Snail
    .hword 0x01E3  @ icid=0x11F0 ( 4592)  -> cid=483 slot=0x11F0  Greenkappa
    .hword 0x01E4  @ icid=0x11F1 ( 4593)  -> cid=484 slot=0x11F1  Mon Larvas
    .hword 0x01E5  @ icid=0x11F2 ( 4594)  -> cid=485 slot=0x11F2  Living Vase
    .hword 0x01E6  @ icid=0x11F3 ( 4595)  -> cid=486 slot=0x11F3  Tentacle Plant
    .hword 0x01E7  @ icid=0x11F4 ( 4596)  -> cid=487 slot=0x11F4  Beaked Snake
    .hword 0x01E8  @ icid=0x11F5 ( 4597)  -> cid=488 slot=0x11F5  Morphing Jar
    .hword 0x01E9  @ icid=0x11F6 ( 4598)  -> cid=489 slot=0x11F6  Muse-A
    .hword 0xFFFF  @ icid=0x11F7 ( 4599)  -> (none)
    .hword 0x01EA  @ icid=0x11F8 ( 4600)  -> cid=490 slot=0x11F8  Rose Spectre of Dunn
    .hword 0x01EB  @ icid=0x11F9 ( 4601)  -> cid=491 slot=0x11F9  Fiend Reflection #1
    .hword 0x01EC  @ icid=0x11FA ( 4602)  -> cid=492 slot=0x11FA  Ghoul with an Appetite
    .hword 0x01ED  @ icid=0x11FB ( 4603)  -> cid=493 slot=0x11FB  Pale Beast
    .hword 0x01EE  @ icid=0x11FC ( 4604)  -> cid=494 slot=0x11FC  Little Chimera
    .hword 0x01EF  @ icid=0x11FD ( 4605)  -> cid=495 slot=0x11FD  Violent Rain
    .hword 0x01F0  @ icid=0x11FE ( 4606)  -> cid=496 slot=0x11FE  Key Mace #2
    .hword 0x01F1  @ icid=0x11FF ( 4607)  -> cid=497 slot=0x11FF  Tenderness
    .hword 0x01F2  @ icid=0x1200 ( 4608)  -> cid=498 slot=0x1200  Penguin Soldier
    .hword 0x01F3  @ icid=0x1201 ( 4609)  -> cid=499 slot=0x1201  Fairy Dragon
    .hword 0x01F4  @ icid=0x1202 ( 4610)  -> cid=500 slot=0x1202  Obese Marmot of Nefariousness
    .hword 0x01F5  @ icid=0x1203 ( 4611)  -> cid=501 slot=0x1203  Liquid Beast
    .hword 0x01F6  @ icid=0x1204 ( 4612)  -> cid=502 slot=0x1204  Twin Long Rods #2
    .hword 0x01F7  @ icid=0x1205 ( 4613)  -> cid=503 slot=0x1205  Great Bill
    .hword 0x01F8  @ icid=0x1206 ( 4614)  -> cid=504 slot=0x1206  Shining Friendship
    .hword 0x01F9  @ icid=0x1207 ( 4615)  -> cid=505 slot=0x1207  Bladefly
    .hword 0xFFFF  @ icid=0x1208 ( 4616)  -> (none)
    .hword 0x01FA  @ icid=0x1209 ( 4617)  -> cid=506 slot=0x1209  Hiro's Shadow Scout
    .hword 0x01FB  @ icid=0x120A ( 4618)  -> cid=507 slot=0x120A  Lady of Faith
    .hword 0x01FC  @ icid=0x120B ( 4619)  -> cid=508 slot=0x120B  Twin-Headed Thunder Dragon
    .hword 0xFFFF  @ icid=0x120C ( 4620)  -> (none)
    .hword 0x01FD  @ icid=0x120D ( 4621)  -> cid=509 slot=0x120D  Armored Starfish
    .hword 0xFFFF  @ icid=0x120E ( 4622)  -> (none)
    .hword 0x01FE  @ icid=0x120F ( 4623)  -> cid=510 slot=0x120F  Marine Beast
    .hword 0x01FF  @ icid=0x1210 ( 4624)  -> cid=511 slot=0x1210  Warrior of Tradition
    .hword 0xFFFF  @ icid=0x1211 ( 4625)  -> (none)
    .hword 0x0200  @ icid=0x1212 ( 4626)  -> cid=512 slot=0x1212  Snakeyashi
    .hword 0xFFFF  @ icid=0x1213 ( 4627)  -> (none)
    .hword 0xFFFF  @ icid=0x1214 ( 4628)  -> (none)
    .hword 0x0201  @ icid=0x1215 ( 4629)  -> cid=513 slot=0x1215  The Thing That Hides in the Mud
    .hword 0x0202  @ icid=0x1216 ( 4630)  -> cid=514 slot=0x1216  High Tide Gyojin
    .hword 0x0203  @ icid=0x1217 ( 4631)  -> cid=515 slot=0x1217  Fairy of the Fountain
    .hword 0x0204  @ icid=0x1218 ( 4632)  -> cid=516 slot=0x1218  Amazon of the Seas
    .hword 0x0205  @ icid=0x1219 ( 4633)  -> cid=517 slot=0x1219  Nekogal #2
    .hword 0x0206  @ icid=0x121A ( 4634)  -> cid=518 slot=0x121A  Witch's Apprentice
    .hword 0x0207  @ icid=0x121B ( 4635)  -> cid=519 slot=0x121B  Armored Rat
    .hword 0x0208  @ icid=0x121C ( 4636)  -> cid=520 slot=0x121C  Ancient Lizard Warrior
    .hword 0x0209  @ icid=0x121D ( 4637)  -> cid=521 slot=0x121D  Maiden of the Moonlight
    .hword 0xFFFF  @ icid=0x121E ( 4638)  -> (none)
    .hword 0xFFFF  @ icid=0x121F ( 4639)  -> (none)
    .hword 0x020A  @ icid=0x1220 ( 4640)  -> cid=522 slot=0x1220  Night Lizard
    .hword 0xFFFF  @ icid=0x1221 ( 4641)  -> (none)
    .hword 0x020B  @ icid=0x1222 ( 4642)  -> cid=523 slot=0x1222  Blue-Winged Crown
    .hword 0xFFFF  @ icid=0x1223 ( 4643)  -> (none)
    .hword 0xFFFF  @ icid=0x1224 ( 4644)  -> (none)
    .hword 0x020C  @ icid=0x1225 ( 4645)  -> cid=524 slot=0x1225  Amphibious Bugroth
    .hword 0x020D  @ icid=0x1226 ( 4646)  -> cid=525 slot=0x1226  Acid Crawler
    .hword 0x020E  @ icid=0x1227 ( 4647)  -> cid=526 slot=0x1227  Invader of the Throne
    .hword 0x020F  @ icid=0x1228 ( 4648)  -> cid=527 slot=0x1228  Mystical Sheep #1
    .hword 0x0210  @ icid=0x1229 ( 4649)  -> cid=528 slot=0x1229  Disk Magician
    .hword 0x0211  @ icid=0x122A ( 4650)  -> cid=529 slot=0x122A  Flame Viper
    .hword 0x0212  @ icid=0x122B ( 4651)  -> cid=530 slot=0x122B  Royal Guard
    .hword 0x0213  @ icid=0x122C ( 4652)  -> cid=531 slot=0x122C  Gruesome Goo
    .hword 0xFFFF  @ icid=0x122D ( 4653)  -> (none)
    .hword 0xFFFF  @ icid=0x122E ( 4654)  -> (none)
    .hword 0xFFFF  @ icid=0x122F ( 4655)  -> (none)
    .hword 0x0214  @ icid=0x1230 ( 4656)  -> cid=532 slot=0x1230  Whiptail Crow
    .hword 0x0215  @ icid=0x1231 ( 4657)  -> cid=533 slot=0x1231  Kunai with Chain
    .hword 0x0217  @ icid=0x1232 ( 4658)  -> cid=535 slot=0x1232  Magical Labyrinth
    .hword 0xFFFF  @ icid=0x1233 ( 4659)  -> (none)
    .hword 0x0218  @ icid=0x1234 ( 4660)  -> cid=536 slot=0x1234  Salamandra
    .hword 0xFFFF  @ icid=0x1235 ( 4661)  -> (none)
    .hword 0x0219  @ icid=0x1236 ( 4662)  -> cid=537 slot=0x1236  Eternal Rest
    .hword 0x021A  @ icid=0x1237 ( 4663)  -> cid=538 slot=0x1237  Megamorph
    .hword 0x021B  @ icid=0x1238 ( 4664)  -> cid=539 slot=0x1238  Metalmorph
    .hword 0xFFFF  @ icid=0x1239 ( 4665)  -> (none)
    .hword 0xFFFF  @ icid=0x123A ( 4666)  -> (none)
    .hword 0x021D  @ icid=0x123B ( 4667)  -> cid=541 slot=0x123B  Crush Card
    .hword 0xFFFF  @ icid=0x123C ( 4668)  -> (none)
    .hword 0xFFFF  @ icid=0x123D ( 4669)  -> (none)
    .hword 0xFFFF  @ icid=0x123E ( 4670)  -> (none)
    .hword 0xFFFF  @ icid=0x123F ( 4671)  -> (none)
    .hword 0xFFFF  @ icid=0x1240 ( 4672)  -> (none)
    .hword 0xFFFF  @ icid=0x1241 ( 4673)  -> (none)
    .hword 0x021F  @ icid=0x1242 ( 4674)  -> cid=543 slot=0x1242  Bright Castle
    .hword 0x0220  @ icid=0x1243 ( 4675)  -> cid=544 slot=0x1243  Shadow Spell
    .hword 0x0221  @ icid=0x1244 ( 4676)  -> cid=545 slot=0x1244  Black Luster Ritual
    .hword 0x0222  @ icid=0x1245 ( 4677)  -> cid=546 slot=0x1245  Zera Ritual
    .hword 0x0223  @ icid=0x1246 ( 4678)  -> cid=547 slot=0x1246  Harpie's Feather Duster
    .hword 0x0225  @ icid=0x1247 ( 4679)  -> cid=549 slot=0x1247  War-Lion Ritual
    .hword 0x0226  @ icid=0x1248 ( 4680)  -> cid=550 slot=0x1248  Beastly Mirror Ritual
    .hword 0xFFFF  @ icid=0x1249 ( 4681)  -> (none)
    .hword 0x0227  @ icid=0x124A ( 4682)  -> cid=551 slot=0x124A  Commencement Dance
    .hword 0x0228  @ icid=0x124B ( 4683)  -> cid=552 slot=0x124B  Hamburger Recipe
    .hword 0xFFFF  @ icid=0x124C ( 4684)  -> (none)
    .hword 0x0229  @ icid=0x124D ( 4685)  -> cid=553 slot=0x124D  Novox's Prayer
    .hword 0xFFFF  @ icid=0x124E ( 4686)  -> (none)
    .hword 0x022A  @ icid=0x124F ( 4687)  -> cid=554 slot=0x124F  House of Adhesive Tape
    .hword 0xFFFF  @ icid=0x1250 ( 4688)  -> (none)
    .hword 0xFFFF  @ icid=0x1251 ( 4689)  -> (none)
    .hword 0xFFFF  @ icid=0x1252 ( 4690)  -> (none)
    .hword 0x022B  @ icid=0x1253 ( 4691)  -> cid=555 slot=0x1253  Acid Trap Hole
    .hword 0x022D  @ icid=0x1254 ( 4692)  -> cid=557 slot=0x1254  Widespread Ruin
    .hword 0xFFFF  @ icid=0x1255 ( 4693)  -> (none)
    .hword 0x022F  @ icid=0x1256 ( 4694)  -> cid=559 slot=0x1256  Bad Reaction to Simochi
    .hword 0x0230  @ icid=0x1257 ( 4695)  -> cid=560 slot=0x1257  Reverse Trap
    .hword 0xFFFF  @ icid=0x1258 ( 4696)  -> (none)
    .hword 0xFFFF  @ icid=0x1259 ( 4697)  -> (none)
    .hword 0x0231  @ icid=0x125A ( 4698)  -> cid=561 slot=0x125A  Turtle Oath
    .hword 0xFFFF  @ icid=0x125B ( 4699)  -> (none)
    .hword 0x0232  @ icid=0x125C ( 4700)  -> cid=562 slot=0x125C  Resurrection of Chakra
    .hword 0xFFFF  @ icid=0x125D ( 4701)  -> (none)
    .hword 0x0233  @ icid=0x125E ( 4702)  -> cid=563 slot=0x125E  Javelin Beetle Pact
    .hword 0x0234  @ icid=0x125F ( 4703)  -> cid=564 slot=0x125F  Garma Sword Oath
    .hword 0xFFFF  @ icid=0x1260 ( 4704)  -> (none)
    .hword 0x0235  @ icid=0x1261 ( 4705)  -> cid=565 slot=0x1261  Revival of Dokurorider
    .hword 0x0236  @ icid=0x1262 ( 4706)  -> cid=566 slot=0x1262  Fortress Whale's Oath
    .hword 0x0237  @ icid=0x1263 ( 4707)  -> cid=567 slot=0x1263  Performance of Sword
    .hword 0x0238  @ icid=0x1264 ( 4708)  -> cid=568 slot=0x1264  Hungry Burger
    .hword 0x0239  @ icid=0x1265 ( 4709)  -> cid=569 slot=0x1265  Sengenjin
    .hword 0x023A  @ icid=0x1266 ( 4710)  -> cid=570 slot=0x1266  Skull Guardian
    .hword 0x023B  @ icid=0x1267 ( 4711)  -> cid=571 slot=0x1267  Tri-Horned Dragon
    .hword 0x023C  @ icid=0x1268 ( 4712)  -> cid=572 slot=0x1268  Serpent Night Dragon
    .hword 0xFFFF  @ icid=0x1269 ( 4713)  -> (none)
    .hword 0x023D  @ icid=0x126A ( 4714)  -> cid=573 slot=0x126A  Cosmo Queen
    .hword 0x023E  @ icid=0x126B ( 4715)  -> cid=574 slot=0x126B  Chakra
    .hword 0x023F  @ icid=0x126C ( 4716)  -> cid=575 slot=0x126C  Crab Turtle
    .hword 0x0240  @ icid=0x126D ( 4717)  -> cid=576 slot=0x126D  Mikazukinoyaiba
    .hword 0x0241  @ icid=0x126E ( 4718)  -> cid=577 slot=0x126E  Meteor Dragon
    .hword 0x0242  @ icid=0x126F ( 4719)  -> cid=578 slot=0x126F  Meteor B. Dragon
    .hword 0x0243  @ icid=0x1270 ( 4720)  -> cid=579 slot=0x1270  Firewing Pegasus
    .hword 0xFFFF  @ icid=0x1271 ( 4721)  -> (none)
    .hword 0x0244  @ icid=0x1272 ( 4722)  -> cid=580 slot=0x1272  Garma Sword
    .hword 0x0245  @ icid=0x1273 ( 4723)  -> cid=581 slot=0x1273  Javelin Beetle
    .hword 0x0246  @ icid=0x1274 ( 4724)  -> cid=582 slot=0x1274  Fortress Whale
    .hword 0x0247  @ icid=0x1275 ( 4725)  -> cid=583 slot=0x1275  Dokurorider
    .hword 0xFFFF  @ icid=0x1276 ( 4726)  -> (none)
    .hword 0x0248  @ icid=0x1277 ( 4727)  -> cid=584 slot=0x1277  Dark Magic Ritual
    .hword 0x0249  @ icid=0x1278 ( 4728)  -> cid=585 slot=0x1278  Magician of Black Chaos
    .hword 0x024A  @ icid=0x1279 ( 4729)  -> cid=586 slot=0x1279  Slot Machine
    .hword 0xFFFF  @ icid=0x127A ( 4730)  -> (none)
    .hword 0x024B  @ icid=0x127B ( 4731)  -> cid=587 slot=0x127B  Red Archery Girl
    .hword 0x024C  @ icid=0x127C ( 4732)  -> cid=588 slot=0x127C  Ryu-Ran
    .hword 0x024D  @ icid=0x127D ( 4733)  -> cid=589 slot=0x127D  Manga Ryu-Ran
    .hword 0x024E  @ icid=0x127E ( 4734)  -> cid=590 slot=0x127E  Toon Mermaid
    .hword 0x024F  @ icid=0x127F ( 4735)  -> cid=591 slot=0x127F  Toon Summoned Skull
    .hword 0xFFFF  @ icid=0x1280 ( 4736)  -> (none)
    .hword 0x0250  @ icid=0x1281 ( 4737)  -> cid=592 slot=0x1281  Relinquished
    .hword 0xFFFF  @ icid=0x1282 ( 4738)  -> (none)
    .hword 0x0251  @ icid=0x1283 ( 4739)  -> cid=593 slot=0x1283  Thousand-Eyes Idol
    .hword 0x0252  @ icid=0x1284 ( 4740)  -> cid=594 slot=0x1284  Thousand-Eyes Restrict
    .hword 0x0253  @ icid=0x1285 ( 4741)  -> cid=595 slot=0x1285  Steel Ogre Grotto #2
    .hword 0x0254  @ icid=0x1286 ( 4742)  -> cid=596 slot=0x1286  Blast Sphere
    .hword 0x0255  @ icid=0x1287 ( 4743)  -> cid=597 slot=0x1287  Hyozanryu
    .hword 0x0256  @ icid=0x1288 ( 4744)  -> cid=598 slot=0x1288  Alpha The Magnet Warrior
    .hword 0xFFFF  @ icid=0x1289 ( 4745)  -> (none)
    .hword 0xFFFF  @ icid=0x128A ( 4746)  -> (none)
    .hword 0x0257  @ icid=0x128B ( 4747)  -> cid=599 slot=0x128B  Lord of D.
    .hword 0x0258  @ icid=0x128C ( 4748)  -> cid=600 slot=0x128C  Red-Eyes Black Metal Dragon
    .hword 0x025A  @ icid=0x128D ( 4749)  -> cid=602 slot=0x128D  Barrel Dragon
    .hword 0x025B  @ icid=0x128E ( 4750)  -> cid=603 slot=0x128E  Hannibal Necromancer
    .hword 0x025C  @ icid=0x128F ( 4751)  -> cid=604 slot=0x128F  Panther Warrior
    .hword 0x025E  @ icid=0x1290 ( 4752)  -> cid=606 slot=0x1290  Three-Headed Geedo
    .hword 0x025F  @ icid=0x1291 ( 4753)  -> cid=607 slot=0x1291  Gazelle the King of Mythical Beasts
    .hword 0x0260  @ icid=0x1292 ( 4754)  -> cid=608 slot=0x1292  Stone Statue of the Aztecs
    .hword 0x0261  @ icid=0x1293 ( 4755)  -> cid=609 slot=0x1293  Berfomet
    .hword 0x0262  @ icid=0x1294 ( 4756)  -> cid=610 slot=0x1294  Chimera the Flying Mythical Beast
    .hword 0x0263  @ icid=0x1295 ( 4757)  -> cid=611 slot=0x1295  Gear Golem the Moving Fortress
    .hword 0x0264  @ icid=0x1296 ( 4758)  -> cid=612 slot=0x1296  Jinzo
    .hword 0x0265  @ icid=0x1297 ( 4759)  -> cid=613 slot=0x1297  Swordsman of Landstar
    .hword 0x0266  @ icid=0x1298 ( 4760)  -> cid=614 slot=0x1298  Cyber Raider
    .hword 0x0267  @ icid=0x1299 ( 4761)  -> cid=615 slot=0x1299  The Fiend Megacyber
    .hword 0x0268  @ icid=0x129A ( 4762)  -> cid=616 slot=0x129A  Reflect Bounder
    .hword 0x0269  @ icid=0x129B ( 4763)  -> cid=617 slot=0x129B  Beta The Magnet Warrior
    .hword 0x026A  @ icid=0x129C ( 4764)  -> cid=618 slot=0x129C  Big Shield Gardna
    .hword 0xFFFF  @ icid=0x129D ( 4765)  -> (none)
    .hword 0x026C  @ icid=0x129E ( 4766)  -> cid=620 slot=0x129E  Dark Magician Girl
    .hword 0x026F  @ icid=0x129F ( 4767)  -> cid=623 slot=0x129F  Alligator's Sword
    .hword 0x0270  @ icid=0x12A0 ( 4768)  -> cid=624 slot=0x12A0  Insect Queen
    .hword 0x0271  @ icid=0x12A1 ( 4769)  -> cid=625 slot=0x12A1  Parasite Paracide
    .hword 0x0272  @ icid=0x12A2 ( 4770)  -> cid=626 slot=0x12A2  Skull-Mark Ladybug
    .hword 0x0273  @ icid=0x12A3 ( 4771)  -> cid=627 slot=0x12A3  Little-Winguard
    .hword 0x0274  @ icid=0x12A4 ( 4772)  -> cid=628 slot=0x12A4  Pinch Hopper
    .hword 0x0275  @ icid=0x12A5 ( 4773)  -> cid=629 slot=0x12A5  Blue-Eyes Toon Dragon
    .hword 0x0276  @ icid=0x12A6 ( 4774)  -> cid=630 slot=0x12A6  Sword Hunter
    .hword 0x0277  @ icid=0x12A7 ( 4775)  -> cid=631 slot=0x12A7  Drill Bug
    .hword 0x0278  @ icid=0x12A8 ( 4776)  -> cid=632 slot=0x12A8  Deepsea Warrior
    .hword 0xFFFF  @ icid=0x12A9 ( 4777)  -> (none)
    .hword 0xFFFF  @ icid=0x12AA ( 4778)  -> (none)
    .hword 0xFFFF  @ icid=0x12AB ( 4779)  -> (none)
    .hword 0x0279  @ icid=0x12AC ( 4780)  -> cid=633 slot=0x12AC  Satellite Cannon
    .hword 0xFFFF  @ icid=0x12AD ( 4781)  -> (none)
    .hword 0xFFFF  @ icid=0x12AE ( 4782)  -> (none)
    .hword 0xFFFF  @ icid=0x12AF ( 4783)  -> (none)
    .hword 0xFFFF  @ icid=0x12B0 ( 4784)  -> (none)
    .hword 0x027A  @ icid=0x12B1 ( 4785)  -> cid=634 slot=0x12B1  The Last Warrior from Another Planet
    .hword 0x027B  @ icid=0x12B2 ( 4786)  -> cid=635 slot=0x12B2  Dunames Dark Witch
    .hword 0x027C  @ icid=0x12B3 ( 4787)  -> cid=636 slot=0x12B3  Garnecia Elefantis
    .hword 0x027D  @ icid=0x12B4 ( 4788)  -> cid=637 slot=0x12B4  Total Defense Shogun
    .hword 0x027E  @ icid=0x12B5 ( 4789)  -> cid=638 slot=0x12B5  Beast of Talwar
    .hword 0x027F  @ icid=0x12B6 ( 4790)  -> cid=639 slot=0x12B6  Cyber-Tech Alligator
    .hword 0xFFFF  @ icid=0x12B7 ( 4791)  -> (none)
    .hword 0x0280  @ icid=0x12B8 ( 4792)  -> cid=640 slot=0x12B8  Gamma The Magnet Warrior
    .hword 0xFFFF  @ icid=0x12B9 ( 4793)  -> (none)
    .hword 0x0281  @ icid=0x12BA ( 4794)  -> cid=641 slot=0x12BA  Time Machine
    .hword 0x0282  @ icid=0x12BB ( 4795)  -> cid=642 slot=0x12BB  Copycat
    .hword 0xFFFF  @ icid=0x12BC ( 4796)  -> (none)
    .hword 0xFFFF  @ icid=0x12BD ( 4797)  -> (none)
    .hword 0x0283  @ icid=0x12BE ( 4798)  -> cid=643 slot=0x12BE  Toon World
    .hword 0x0285  @ icid=0x12BF ( 4799)  -> cid=645 slot=0x12BF  Gorgon's Eye
    .hword 0xFFFF  @ icid=0x12C0 ( 4800)  -> (none)
    .hword 0xFFFF  @ icid=0x12C1 ( 4801)  -> (none)
    .hword 0x0286  @ icid=0x12C2 ( 4802)  -> cid=646 slot=0x12C2  Black Illusion Ritual
    .hword 0x0287  @ icid=0x12C3 ( 4803)  -> cid=647 slot=0x12C3  Brain Control
    .hword 0x0288  @ icid=0x12C4 ( 4804)  -> cid=648 slot=0x12C4  Negate Attack
    .hword 0x0289  @ icid=0x12C5 ( 4805)  -> cid=649 slot=0x12C5  Multiply
    .hword 0xFFFF  @ icid=0x12C6 ( 4806)  -> (none)
    .hword 0xFFFF  @ icid=0x12C7 ( 4807)  -> (none)
    .hword 0x028A  @ icid=0x12C8 ( 4808)  -> cid=650 slot=0x12C8  Lightforce Sword
    .hword 0xFFFF  @ icid=0x12C9 ( 4809)  -> (none)
    .hword 0x028B  @ icid=0x12CA ( 4810)  -> cid=651 slot=0x12CA  The Flute of Summoning Dragon
    .hword 0x028C  @ icid=0x12CB ( 4811)  -> cid=652 slot=0x12CB  Shield & Sword
    .hword 0x028D  @ icid=0x12CC ( 4812)  -> cid=653 slot=0x12CC  Graceful Charity
    .hword 0x028E  @ icid=0x12CD ( 4813)  -> cid=654 slot=0x12CD  Chain Destruction
    .hword 0x028F  @ icid=0x12CE ( 4814)  -> cid=655 slot=0x12CE  Mesmeric Control
    .hword 0x0290  @ icid=0x12CF ( 4815)  -> cid=656 slot=0x12CF  Graceful Dice
    .hword 0x0291  @ icid=0x12D0 ( 4816)  -> cid=657 slot=0x12D0  Skull Dice
    .hword 0x0292  @ icid=0x12D1 ( 4817)  -> cid=658 slot=0x12D1  Mind Control
    .hword 0x0293  @ icid=0x12D2 ( 4818)  -> cid=659 slot=0x12D2  Scapegoat
    .hword 0x0294  @ icid=0x12D3 ( 4819)  -> cid=660 slot=0x12D3  Amplifier
    .hword 0xFFFF  @ icid=0x12D4 ( 4820)  -> (none)
    .hword 0x0295  @ icid=0x12D5 ( 4821)  -> cid=661 slot=0x12D5  Card Destruction
    .hword 0xFFFF  @ icid=0x12D6 ( 4822)  -> (none)
    .hword 0x0296  @ icid=0x12D7 ( 4823)  -> cid=662 slot=0x12D7  Tragedy
    .hword 0xFFFF  @ icid=0x12D8 ( 4824)  -> (none)
    .hword 0xFFFF  @ icid=0x12D9 ( 4825)  -> (none)
    .hword 0xFFFF  @ icid=0x12DA ( 4826)  -> (none)
    .hword 0xFFFF  @ icid=0x12DB ( 4827)  -> (none)
    .hword 0x0297  @ icid=0x12DC ( 4828)  -> cid=663 slot=0x12DC  Ectoplasmer
    .hword 0xFFFF  @ icid=0x12DD ( 4829)  -> (none)
    .hword 0x0298  @ icid=0x12DE ( 4830)  -> cid=664 slot=0x12DE  Dark Magic Curtain
    .hword 0xFFFF  @ icid=0x12DF ( 4831)  -> (none)
    .hword 0x0299  @ icid=0x12E0 ( 4832)  -> cid=665 slot=0x12E0  Insect Barrier
    .hword 0xFFFF  @ icid=0x12E1 ( 4833)  -> (none)
    .hword 0x029A  @ icid=0x12E2 ( 4834)  -> cid=666 slot=0x12E2  Magic-Arm Shield
    .hword 0x029B  @ icid=0x12E3 ( 4835)  -> cid=667 slot=0x12E3  Fissure
    .hword 0x029C  @ icid=0x12E4 ( 4836)  -> cid=668 slot=0x12E4  Trap Hole
    .hword 0x029D  @ icid=0x12E5 ( 4837)  -> cid=669 slot=0x12E5  Polymerization
    .hword 0x029E  @ icid=0x12E6 ( 4838)  -> cid=670 slot=0x12E6  Remove Trap
    .hword 0x029F  @ icid=0x12E7 ( 4839)  -> cid=671 slot=0x12E7  Two-Pronged Attack
    .hword 0xFFFF  @ icid=0x12E8 ( 4840)  -> (none)
    .hword 0xFFFF  @ icid=0x12E9 ( 4841)  -> (none)
    .hword 0x02A0  @ icid=0x12EA ( 4842)  -> cid=672 slot=0x12EA  Monster Reborn
    .hword 0x02A1  @ icid=0x12EB ( 4843)  -> cid=673 slot=0x12EB  De-Spell
    .hword 0x02A2  @ icid=0x12EC ( 4844)  -> cid=674 slot=0x12EC  Pot of Greed
    .hword 0x02A3  @ icid=0x12ED ( 4845)  -> cid=675 slot=0x12ED  Gravedigger Ghoul
    .hword 0xFFFF  @ icid=0x12EE ( 4846)  -> (none)
    .hword 0xFFFF  @ icid=0x12EF ( 4847)  -> (none)
    .hword 0xFFFF  @ icid=0x12F0 ( 4848)  -> (none)
    .hword 0x02A4  @ icid=0x12F1 ( 4849)  -> cid=676 slot=0x12F1  Reinforcements
    .hword 0x02A5  @ icid=0x12F2 ( 4850)  -> cid=677 slot=0x12F2  Castle Walls
    .hword 0x02A6  @ icid=0x12F3 ( 4851)  -> cid=678 slot=0x12F3  Ultimate Offering
    .hword 0xFFFF  @ icid=0x12F4 ( 4852)  -> (none)
    .hword 0xFFFF  @ icid=0x12F5 ( 4853)  -> (none)
    .hword 0xFFFF  @ icid=0x12F6 ( 4854)  -> (none)
    .hword 0xFFFF  @ icid=0x12F7 ( 4855)  -> (none)
    .hword 0x02A7  @ icid=0x12F8 ( 4856)  -> cid=679 slot=0x12F8  Tribute to The Doomed
    .hword 0x02A8  @ icid=0x12F9 ( 4857)  -> cid=680 slot=0x12F9  Soul Release
    .hword 0x02A9  @ icid=0x12FA ( 4858)  -> cid=681 slot=0x12FA  The Cheerful Coffin
    .hword 0xFFFF  @ icid=0x12FB ( 4859)  -> (none)
    .hword 0x02AA  @ icid=0x12FC ( 4860)  -> cid=682 slot=0x12FC  Change of Heart
    .hword 0x02AB  @ icid=0x12FD ( 4861)  -> cid=683 slot=0x12FD  Solemn Judgment
    .hword 0x02AC  @ icid=0x12FE ( 4862)  -> cid=684 slot=0x12FE  Magic Jammer
    .hword 0x02AD  @ icid=0x12FF ( 4863)  -> cid=685 slot=0x12FF  Seven Tools of the Bandit
    .hword 0x02AE  @ icid=0x1300 ( 4864)  -> cid=686 slot=0x1300  Horn of Heaven
    .hword 0x02AF  @ icid=0x1301 ( 4865)  -> cid=687 slot=0x1301  Just Desserts
    .hword 0x02B0  @ icid=0x1302 ( 4866)  -> cid=688 slot=0x1302  Royal Decree
    .hword 0x02B1  @ icid=0x1303 ( 4867)  -> cid=689 slot=0x1303  Polymerization
    .hword 0xFFFF  @ icid=0x1304 ( 4868)  -> (none)
    .hword 0xFFFF  @ icid=0x1305 ( 4869)  -> (none)
    .hword 0x02B2  @ icid=0x1306 ( 4870)  -> cid=690 slot=0x1306  Magical Thorn
    .hword 0x02B3  @ icid=0x1307 ( 4871)  -> cid=691 slot=0x1307  Restructer Revolution
    .hword 0x02B4  @ icid=0x1308 ( 4872)  -> cid=692 slot=0x1308  Fusion Sage
    .hword 0x02B5  @ icid=0x1309 ( 4873)  -> cid=693 slot=0x1309  Sword of Deep-Seated
    .hword 0x02B6  @ icid=0x130A ( 4874)  -> cid=694 slot=0x130A  Block Attack
    .hword 0x02B7  @ icid=0x130B ( 4875)  -> cid=695 slot=0x130B  The Unhappy Maiden
    .hword 0x02B8  @ icid=0x130C ( 4876)  -> cid=696 slot=0x130C  Robbin' Goblin
    .hword 0x02B9  @ icid=0x130D ( 4877)  -> cid=697 slot=0x130D  Germ Infection
    .hword 0xFFFF  @ icid=0x130E ( 4878)  -> (none)
    .hword 0xFFFF  @ icid=0x130F ( 4879)  -> (none)
    .hword 0x02BA  @ icid=0x1310 ( 4880)  -> cid=698 slot=0x1310  Wall of Illusion
    .hword 0x02BB  @ icid=0x1311 ( 4881)  -> cid=699 slot=0x1311  Neo the Magic Swordsman
    .hword 0x02BC  @ icid=0x1312 ( 4882)  -> cid=700 slot=0x1312  Baron of the Fiend Sword
    .hword 0x02BD  @ icid=0x1313 ( 4883)  -> cid=701 slot=0x1313  Man-Eating Treasure Chest
    .hword 0x02BE  @ icid=0x1314 ( 4884)  -> cid=702 slot=0x1314  Sorcerer of the Doomed
    .hword 0x02BF  @ icid=0x1315 ( 4885)  -> cid=703 slot=0x1315  Last Will
    .hword 0x02C0  @ icid=0x1316 ( 4886)  -> cid=704 slot=0x1316  Waboku
    .hword 0x02C1  @ icid=0x1317 ( 4887)  -> cid=705 slot=0x1317  Mirror Force
    .hword 0x02C2  @ icid=0x1318 ( 4888)  -> cid=706 slot=0x1318  Ring of Magnetism
    .hword 0x02C3  @ icid=0x1319 ( 4889)  -> cid=707 slot=0x1319  Share the Pain
    .hword 0x02C4  @ icid=0x131A ( 4890)  -> cid=708 slot=0x131A  Stim-Pack
    .hword 0x02C5  @ icid=0x131B ( 4891)  -> cid=709 slot=0x131B  Heavy Storm
    .hword 0xFFFF  @ icid=0x131C ( 4892)  -> (none)
    .hword 0x02C6  @ icid=0x131D ( 4893)  -> cid=710 slot=0x131D  Gravekeeper's Servant
    .hword 0xFFFF  @ icid=0x131E ( 4894)  -> (none)
    .hword 0x02C7  @ icid=0x131F ( 4895)  -> cid=711 slot=0x131F  Upstart Goblin
    .hword 0x02C8  @ icid=0x1320 ( 4896)  -> cid=712 slot=0x1320  Toll
    .hword 0x02C9  @ icid=0x1321 ( 4897)  -> cid=713 slot=0x1321  Final Destiny
    .hword 0x02CA  @ icid=0x1322 ( 4898)  -> cid=714 slot=0x1322  Snatch Steal
    .hword 0x02CB  @ icid=0x1323 ( 4899)  -> cid=715 slot=0x1323  Chorus of Sanctuary
    .hword 0x02CC  @ icid=0x1324 ( 4900)  -> cid=716 slot=0x1324  Confiscation
    .hword 0x02CD  @ icid=0x1325 ( 4901)  -> cid=717 slot=0x1325  Delinquent Duo
    .hword 0xFFFF  @ icid=0x1326 ( 4902)  -> (none)
    .hword 0x02CE  @ icid=0x1327 ( 4903)  -> cid=718 slot=0x1327  Fairy's Hand Mirror
    .hword 0x02CF  @ icid=0x1328 ( 4904)  -> cid=719 slot=0x1328  Tailor of the Fickle
    .hword 0x02D0  @ icid=0x1329 ( 4905)  -> cid=720 slot=0x1329  Rush Recklessly
    .hword 0x02D1  @ icid=0x132A ( 4906)  -> cid=721 slot=0x132A  The Reliable Guardian
    .hword 0x02D2  @ icid=0x132B ( 4907)  -> cid=722 slot=0x132B  The Forceful Sentry
    .hword 0x02D3  @ icid=0x132C ( 4908)  -> cid=723 slot=0x132C  Chain Energy
    .hword 0x02D4  @ icid=0x132D ( 4909)  -> cid=724 slot=0x132D  Mystical Space Typhoon
    .hword 0x02D5  @ icid=0x132E ( 4910)  -> cid=725 slot=0x132E  Giant Trunade
    .hword 0x02D6  @ icid=0x132F ( 4911)  -> cid=726 slot=0x132F  Painful Choice
    .hword 0x02D7  @ icid=0x1330 ( 4912)  -> cid=727 slot=0x1330  Snake Fang
    .hword 0x02D8  @ icid=0x1331 ( 4913)  -> cid=728 slot=0x1331  Cyber Jar
    .hword 0x02D9  @ icid=0x1332 ( 4914)  -> cid=729 slot=0x1332  Banisher of the Light
    .hword 0x02DA  @ icid=0x1333 ( 4915)  -> cid=730 slot=0x1333  Giant Rat
    .hword 0x02DB  @ icid=0x1334 ( 4916)  -> cid=731 slot=0x1334  Senju of the Thousand Hands
    .hword 0x02DC  @ icid=0x1335 ( 4917)  -> cid=732 slot=0x1335  UFO Turtle
    .hword 0x02DD  @ icid=0x1336 ( 4918)  -> cid=733 slot=0x1336  Flash Assailant
    .hword 0x02DE  @ icid=0x1337 ( 4919)  -> cid=734 slot=0x1337  Karate Man
    .hword 0xFFFF  @ icid=0x1338 ( 4920)  -> (none)
    .hword 0x02DF  @ icid=0x1339 ( 4921)  -> cid=735 slot=0x1339  Giant Germ
    .hword 0x02E0  @ icid=0x133A ( 4922)  -> cid=736 slot=0x133A  Nimble Momonga
    .hword 0x02E1  @ icid=0x133B ( 4923)  -> cid=737 slot=0x133B  Spear Cretin
    .hword 0x02E2  @ icid=0x133C ( 4924)  -> cid=738 slot=0x133C  Shining Angel
    .hword 0xFFFF  @ icid=0x133D ( 4925)  -> (none)
    .hword 0x02E3  @ icid=0x133E ( 4926)  -> cid=739 slot=0x133E  Mother Grizzly
    .hword 0x02E4  @ icid=0x133F ( 4927)  -> cid=740 slot=0x133F  Flying Kamakiri #1
    .hword 0x02E5  @ icid=0x1340 ( 4928)  -> cid=741 slot=0x1340  Ceremonial Bell
    .hword 0x02E6  @ icid=0x1341 ( 4929)  -> cid=742 slot=0x1341  Sonic Bird
    .hword 0x02E7  @ icid=0x1342 ( 4930)  -> cid=743 slot=0x1342  Mystic Tomato
    .hword 0x02E8  @ icid=0x1343 ( 4931)  -> cid=744 slot=0x1343  Kotodama
    .hword 0x02E9  @ icid=0x1344 ( 4932)  -> cid=745 slot=0x1344  Gaia Power
    .hword 0x02EA  @ icid=0x1345 ( 4933)  -> cid=746 slot=0x1345  Umiiruka
    .hword 0x02EB  @ icid=0x1346 ( 4934)  -> cid=747 slot=0x1346  Molten Destruction
    .hword 0x02EC  @ icid=0x1347 ( 4935)  -> cid=748 slot=0x1347  Rising Air Current
    .hword 0x02ED  @ icid=0x1348 ( 4936)  -> cid=749 slot=0x1348  Luminous Spark
    .hword 0x02EE  @ icid=0x1349 ( 4937)  -> cid=750 slot=0x1349  Mystic Plasma Zone
    .hword 0x02EF  @ icid=0x134A ( 4938)  -> cid=751 slot=0x134A  Messenger of Peace
    .hword 0x02F0  @ icid=0x134B ( 4939)  -> cid=752 slot=0x134B  Michizure
    .hword 0x02F1  @ icid=0x134C ( 4940)  -> cid=753 slot=0x134C  Gust
    .hword 0x02F2  @ icid=0x134D ( 4941)  -> cid=754 slot=0x134D  Driving Snow
    .hword 0xFFFF  @ icid=0x134E ( 4942)  -> (none)
    .hword 0xFFFF  @ icid=0x134F ( 4943)  -> (none)
    .hword 0xFFFF  @ icid=0x1350 ( 4944)  -> (none)
    .hword 0xFFFF  @ icid=0x1351 ( 4945)  -> (none)
    .hword 0x02F3  @ icid=0x1352 ( 4946)  -> cid=755 slot=0x1352  Numinous Healer
    .hword 0x02F4  @ icid=0x1353 ( 4947)  -> cid=756 slot=0x1353  Appropriate
    .hword 0x02F5  @ icid=0x1354 ( 4948)  -> cid=757 slot=0x1354  Forced Requisition
    .hword 0x02F6  @ icid=0x1355 ( 4949)  -> cid=758 slot=0x1355  Minor Goblin Official
    .hword 0x02F7  @ icid=0x1356 ( 4950)  -> cid=759 slot=0x1356  Gamble
    .hword 0x02F8  @ icid=0x1357 ( 4951)  -> cid=760 slot=0x1357  DNA Surgery
    .hword 0x02F9  @ icid=0x1358 ( 4952)  -> cid=761 slot=0x1358  The Regulation of Tribe
    .hword 0x02FA  @ icid=0x1359 ( 4953)  -> cid=762 slot=0x1359  Backup Soldier
    .hword 0x02FB  @ icid=0x135A ( 4954)  -> cid=763 slot=0x135A  Attack and Receive
    .hword 0xFFFF  @ icid=0x135B ( 4955)  -> (none)
    .hword 0x02FC  @ icid=0x135C ( 4956)  -> cid=764 slot=0x135C  Ceasefire
    .hword 0x02FD  @ icid=0x135D ( 4957)  -> cid=765 slot=0x135D  Light of Intervention
    .hword 0x02FE  @ icid=0x135E ( 4958)  -> cid=766 slot=0x135E  Respect Play
    .hword 0xFFFF  @ icid=0x135F ( 4959)  -> (none)
    .hword 0x02FF  @ icid=0x1360 ( 4960)  -> cid=767 slot=0x1360  Imperial Order
    .hword 0x0300  @ icid=0x1361 ( 4961)  -> cid=768 slot=0x1361  Skull Invitation
    .hword 0x0301  @ icid=0x1362 ( 4962)  -> cid=769 slot=0x1362  Magical Hats
    .hword 0x0302  @ icid=0x1363 ( 4963)  -> cid=770 slot=0x1363  Nobleman of Crossout
    .hword 0x0303  @ icid=0x1364 ( 4964)  -> cid=771 slot=0x1364  Nobleman of Extermination
    .hword 0x0304  @ icid=0x1365 ( 4965)  -> cid=772 slot=0x1365  The Shallow Grave
    .hword 0x0305  @ icid=0x1366 ( 4966)  -> cid=773 slot=0x1366  Premature Burial
    .hword 0xFFFF  @ icid=0x1367 ( 4967)  -> (none)
    .hword 0xFFFF  @ icid=0x1368 ( 4968)  -> (none)
    .hword 0x0306  @ icid=0x1369 ( 4969)  -> cid=774 slot=0x1369  Morphing Jar #2
    .hword 0x0307  @ icid=0x136A ( 4970)  -> cid=775 slot=0x136A  Bubonic Vermin
    .hword 0xFFFF  @ icid=0x136B ( 4971)  -> (none)
    .hword 0x0308  @ icid=0x136C ( 4972)  -> cid=776 slot=0x136C  Twin-Headed Fire Dragon
    .hword 0x0309  @ icid=0x136D ( 4973)  -> cid=777 slot=0x136D  Darkfire Soldier #1
    .hword 0x030A  @ icid=0x136E ( 4974)  -> cid=778 slot=0x136E  Mr. Volcano
    .hword 0x030B  @ icid=0x136F ( 4975)  -> cid=779 slot=0x136F  Darkfire Soldier #2
    .hword 0x030C  @ icid=0x1370 ( 4976)  -> cid=780 slot=0x1370  Kiseitai
    .hword 0x030D  @ icid=0x1371 ( 4977)  -> cid=781 slot=0x1371  Cyber Falcon
    .hword 0x030E  @ icid=0x1372 ( 4978)  -> cid=782 slot=0x1372  Dark Bat
    .hword 0x030F  @ icid=0x1373 ( 4979)  -> cid=783 slot=0x1373  Flying Kamakiri #2
    .hword 0x0310  @ icid=0x1374 ( 4980)  -> cid=784 slot=0x1374  Harpie's Brother
    .hword 0x0311  @ icid=0x1375 ( 4981)  -> cid=785 slot=0x1375  Oni Tank T-34
    .hword 0x0312  @ icid=0x1376 ( 4982)  -> cid=786 slot=0x1376  Overdrive
    .hword 0x0313  @ icid=0x1377 ( 4983)  -> cid=787 slot=0x1377  Buster Blader
    .hword 0x0314  @ icid=0x1378 ( 4984)  -> cid=788 slot=0x1378  Time Seal
    .hword 0x0315  @ icid=0x1379 ( 4985)  -> cid=789 slot=0x1379  Graverobber
    .hword 0x0316  @ icid=0x137A ( 4986)  -> cid=790 slot=0x137A  Gift of The Mystical Elf
    .hword 0x0317  @ icid=0x137B ( 4987)  -> cid=791 slot=0x137B  The Eye of Truth
    .hword 0x0318  @ icid=0x137C ( 4988)  -> cid=792 slot=0x137C  Dust Tornado
    .hword 0x0319  @ icid=0x137D ( 4989)  -> cid=793 slot=0x137D  Call of the Haunted
    .hword 0x031A  @ icid=0x137E ( 4990)  -> cid=794 slot=0x137E  Solomon's Lawbook
    .hword 0xFFFF  @ icid=0x137F ( 4991)  -> (none)
    .hword 0x031B  @ icid=0x1380 ( 4992)  -> cid=795 slot=0x1380  Enchanted Javelin
    .hword 0x031C  @ icid=0x1381 ( 4993)  -> cid=796 slot=0x1381  Mirror Wall
    .hword 0xFFFF  @ icid=0x1382 ( 4994)  -> (none)
    .hword 0xFFFF  @ icid=0x1383 ( 4995)  -> (none)
    .hword 0xFFFF  @ icid=0x1384 ( 4996)  -> (none)
    .hword 0xFFFF  @ icid=0x1385 ( 4997)  -> (none)
    .hword 0xFFFF  @ icid=0x1386 ( 4998)  -> (none)
    .hword 0xFFFF  @ icid=0x1387 ( 4999)  -> (none)
    .hword 0xFFFF  @ icid=0x1388 ( 5000)  -> (none)
    .hword 0x031D  @ icid=0x1389 ( 5001)  -> cid=797 slot=0x1389  Windstorm of Etaqua
    .hword 0x031E  @ icid=0x138A ( 5002)  -> cid=798 slot=0x138A  Valkyrion the Magna Warrior
    .hword 0x031F  @ icid=0x138B ( 5003)  -> cid=799 slot=0x138B  Alligator's Sword Dragon
    .hword 0x0320  @ icid=0x138C ( 5004)  -> cid=800 slot=0x138C  Vorse Raider
    .hword 0x0322  @ icid=0x138D ( 5005)  -> cid=802 slot=0x138D  Ring of Destruction
    .hword 0x0323  @ icid=0x138E ( 5006)  -> cid=803 slot=0x138E  Aqua Chorus
    .hword 0x0324  @ icid=0x138F ( 5007)  -> cid=804 slot=0x138F  Sebek's Blessing
    .hword 0x0325  @ icid=0x1390 ( 5008)  -> cid=805 slot=0x1390  Anti-Spell Fragrance
    .hword 0x0326  @ icid=0x1391 ( 5009)  -> cid=806 slot=0x1391  Riryoku
    .hword 0x0327  @ icid=0x1392 ( 5010)  -> cid=807 slot=0x1392  Sword of Dragon's Soul
    .hword 0xFFFF  @ icid=0x1393 ( 5011)  -> (none)
    .hword 0xFFFF  @ icid=0x1394 ( 5012)  -> (none)
    .hword 0xFFFF  @ icid=0x1395 ( 5013)  -> (none)
    .hword 0xFFFF  @ icid=0x1396 ( 5014)  -> (none)
    .hword 0x0328  @ icid=0x1397 ( 5015)  -> cid=808 slot=0x1397  Luminous Soldier
    .hword 0x0329  @ icid=0x1398 ( 5016)  -> cid=809 slot=0x1398  King Tiger Wanghu
    .hword 0x032A  @ icid=0x1399 ( 5017)  -> cid=810 slot=0x1399  Command Knight
    .hword 0x032B  @ icid=0x139A ( 5018)  -> cid=811 slot=0x139A  Wolf Axwielder
    .hword 0x032C  @ icid=0x139B ( 5019)  -> cid=812 slot=0x139B  The Illusory Gentleman
    .hword 0x032D  @ icid=0x139C ( 5020)  -> cid=813 slot=0x139C  Patrician of Darkness
    .hword 0x032E  @ icid=0x139D ( 5021)  -> cid=814 slot=0x139D  Birdface
    .hword 0x032F  @ icid=0x139E ( 5022)  -> cid=815 slot=0x139E  Kryuel
    .hword 0x0330  @ icid=0x139F ( 5023)  -> cid=816 slot=0x139F  Airknight Parshath
    .hword 0x0331  @ icid=0x13A0 ( 5024)  -> cid=817 slot=0x13A0  Fairy King Truesdale
    .hword 0x0332  @ icid=0x13A1 ( 5025)  -> cid=818 slot=0x13A1  Serpentine Princess
    .hword 0x0333  @ icid=0x13A2 ( 5026)  -> cid=819 slot=0x13A2  Maiden of the Aqua
    .hword 0x0334  @ icid=0x13A3 ( 5027)  -> cid=820 slot=0x13A3  Robotic Knight
    .hword 0x0335  @ icid=0x13A4 ( 5028)  -> cid=821 slot=0x13A4  Thunder Nyan Nyan
    .hword 0x0336  @ icid=0x13A5 ( 5029)  -> cid=822 slot=0x13A5  Molten Behemoth
    .hword 0x0337  @ icid=0x13A6 ( 5030)  -> cid=823 slot=0x13A6  Twin-Headed Behemoth
    .hword 0x0338  @ icid=0x13A7 ( 5031)  -> cid=824 slot=0x13A7  Injection Fairy Lily
    .hword 0x0339  @ icid=0x13A8 ( 5032)  -> cid=825 slot=0x13A8  Woodland Sprite
    .hword 0x033A  @ icid=0x13A9 ( 5033)  -> cid=826 slot=0x13A9  Arsenal Bug
    .hword 0x033B  @ icid=0x13AA ( 5034)  -> cid=827 slot=0x13AA  Kinetic Soldier
    .hword 0x033C  @ icid=0x13AB ( 5035)  -> cid=828 slot=0x13AB  Jowls of Dark Demise
    .hword 0x033D  @ icid=0x13AC ( 5036)  -> cid=829 slot=0x13AC  Souleater
    .hword 0x033E  @ icid=0x13AD ( 5037)  -> cid=830 slot=0x13AD  Slate Warrior
    .hword 0xFFFF  @ icid=0x13AE ( 5038)  -> (none)
    .hword 0xFFFF  @ icid=0x13AF ( 5039)  -> (none)
    .hword 0xFFFF  @ icid=0x13B0 ( 5040)  -> (none)
    .hword 0x033F  @ icid=0x13B1 ( 5041)  -> cid=831 slot=0x13B1  Timeater
    .hword 0x0340  @ icid=0x13B2 ( 5042)  -> cid=832 slot=0x13B2  Mucus Yolk
    .hword 0x0341  @ icid=0x13B3 ( 5043)  -> cid=833 slot=0x13B3  Servant of Catabolism
    .hword 0x0342  @ icid=0x13B4 ( 5044)  -> cid=834 slot=0x13B4  Rigras Leever
    .hword 0x0343  @ icid=0x13B5 ( 5045)  -> cid=835 slot=0x13B5  Moisture Creature
    .hword 0x0344  @ icid=0x13B6 ( 5046)  -> cid=836 slot=0x13B6  Boneheimer
    .hword 0xFFFF  @ icid=0x13B7 ( 5047)  -> (none)
    .hword 0x0345  @ icid=0x13B8 ( 5048)  -> cid=837 slot=0x13B8  Flame Dancer
    .hword 0xFFFF  @ icid=0x13B9 ( 5049)  -> (none)
    .hword 0xFFFF  @ icid=0x13BA ( 5050)  -> (none)
    .hword 0xFFFF  @ icid=0x13BB ( 5051)  -> (none)
    .hword 0xFFFF  @ icid=0x13BC ( 5052)  -> (none)
    .hword 0x0346  @ icid=0x13BD ( 5053)  -> cid=838 slot=0x13BD  Sonic Jammer
    .hword 0xFFFF  @ icid=0x13BE ( 5054)  -> (none)
    .hword 0xFFFF  @ icid=0x13BF ( 5055)  -> (none)
    .hword 0xFFFF  @ icid=0x13C0 ( 5056)  -> (none)
    .hword 0xFFFF  @ icid=0x13C1 ( 5057)  -> (none)
    .hword 0xFFFF  @ icid=0x13C2 ( 5058)  -> (none)
    .hword 0x0347  @ icid=0x13C3 ( 5059)  -> cid=839 slot=0x13C3  Gearfried the Iron Knight
    .hword 0x0348  @ icid=0x13C4 ( 5060)  -> cid=840 slot=0x13C4  Humanoid Slime
    .hword 0x0349  @ icid=0x13C5 ( 5061)  -> cid=841 slot=0x13C5  Worm Drake
    .hword 0x034A  @ icid=0x13C6 ( 5062)  -> cid=842 slot=0x13C6  Humanoid Worm Drake
    .hword 0x034B  @ icid=0x13C7 ( 5063)  -> cid=843 slot=0x13C7  Revival Jam
    .hword 0xFFFF  @ icid=0x13C8 ( 5064)  -> (none)
    .hword 0x034C  @ icid=0x13C9 ( 5065)  -> cid=844 slot=0x13C9  Flying Fish
    .hword 0x034D  @ icid=0x13CA ( 5066)  -> cid=845 slot=0x13CA  Amphibian Beast
    .hword 0x034E  @ icid=0x13CB ( 5067)  -> cid=846 slot=0x13CB  Rocket Warrior
    .hword 0xFFFF  @ icid=0x13CC ( 5068)  -> (none)
    .hword 0x034F  @ icid=0x13CD ( 5069)  -> cid=847 slot=0x13CD  The Legendary Fisherman
    .hword 0xFFFF  @ icid=0x13CE ( 5070)  -> (none)
    .hword 0xFFFF  @ icid=0x13CF ( 5071)  -> (none)
    .hword 0x0350  @ icid=0x13D0 ( 5072)  -> cid=848 slot=0x13D0  Robolady
    .hword 0x0351  @ icid=0x13D1 ( 5073)  -> cid=849 slot=0x13D1  Roboyarou
    .hword 0xFFFF  @ icid=0x13D2 ( 5074)  -> (none)
    .hword 0xFFFF  @ icid=0x13D3 ( 5075)  -> (none)
    .hword 0xFFFF  @ icid=0x13D4 ( 5076)  -> (none)
    .hword 0xFFFF  @ icid=0x13D5 ( 5077)  -> (none)
    .hword 0xFFFF  @ icid=0x13D6 ( 5078)  -> (none)
    .hword 0x0352  @ icid=0x13D7 ( 5079)  -> cid=850 slot=0x13D7  Lightning Conger
    .hword 0xFFFF  @ icid=0x13D8 ( 5080)  -> (none)
    .hword 0xFFFF  @ icid=0x13D9 ( 5081)  -> (none)
    .hword 0xFFFF  @ icid=0x13DA ( 5082)  -> (none)
    .hword 0xFFFF  @ icid=0x13DB ( 5083)  -> (none)
    .hword 0xFFFF  @ icid=0x13DC ( 5084)  -> (none)
    .hword 0xFFFF  @ icid=0x13DD ( 5085)  -> (none)
    .hword 0x0353  @ icid=0x13DE ( 5086)  -> cid=851 slot=0x13DE  Spherous Lady
    .hword 0xFFFF  @ icid=0x13DF ( 5087)  -> (none)
    .hword 0xFFFF  @ icid=0x13E0 ( 5088)  -> (none)
    .hword 0xFFFF  @ icid=0x13E1 ( 5089)  -> (none)
    .hword 0x0354  @ icid=0x13E2 ( 5090)  -> cid=852 slot=0x13E2  Shining Abyss
    .hword 0x0355  @ icid=0x13E3 ( 5091)  -> cid=853 slot=0x13E3  Archfiend of Gilfer
    .hword 0x0356  @ icid=0x13E4 ( 5092)  -> cid=854 slot=0x13E4  Gadget Soldier
    .hword 0x0357  @ icid=0x13E5 ( 5093)  -> cid=855 slot=0x13E5  Grand Tiki Elder
    .hword 0x0358  @ icid=0x13E6 ( 5094)  -> cid=856 slot=0x13E6  The Masked Beast
    .hword 0x0359  @ icid=0x13E7 ( 5095)  -> cid=857 slot=0x13E7  Melchid the Four-Face Beast
    .hword 0x035A  @ icid=0x13E8 ( 5096)  -> cid=858 slot=0x13E8  Nuvia the Wicked
    .hword 0xFFFF  @ icid=0x13E9 ( 5097)  -> (none)
    .hword 0xFFFF  @ icid=0x13EA ( 5098)  -> (none)
    .hword 0x035B  @ icid=0x13EB ( 5099)  -> cid=859 slot=0x13EB  Soul Exchange
    .hword 0xFFFF  @ icid=0x13EC ( 5100)  -> (none)
    .hword 0xFFFF  @ icid=0x13ED ( 5101)  -> (none)
    .hword 0x035C  @ icid=0x13EE ( 5102)  -> cid=860 slot=0x13EE  Mask of Weakness
    .hword 0x035D  @ icid=0x13EF ( 5103)  -> cid=861 slot=0x13EF  Curse of the Masked Beast
    .hword 0x035E  @ icid=0x13F0 ( 5104)  -> cid=862 slot=0x13F0  Mask of Dispel
    .hword 0xFFFF  @ icid=0x13F1 ( 5105)  -> (none)
    .hword 0x035F  @ icid=0x13F2 ( 5106)  -> cid=863 slot=0x13F2  Mask of Restrict
    .hword 0x0360  @ icid=0x13F3 ( 5107)  -> cid=864 slot=0x13F3  Mask of the Accursed
    .hword 0x0361  @ icid=0x13F4 ( 5108)  -> cid=865 slot=0x13F4  Mask of Brutality
    .hword 0x0362  @ icid=0x13F5 ( 5109)  -> cid=866 slot=0x13F5  Return of the Doomed
    .hword 0x0363  @ icid=0x13F6 ( 5110)  -> cid=867 slot=0x13F6  Lightning Blade
    .hword 0x0364  @ icid=0x13F7 ( 5111)  -> cid=868 slot=0x13F7  Tornado Wall
    .hword 0x0365  @ icid=0x13F8 ( 5112)  -> cid=869 slot=0x13F8  Infinite Dismissal
    .hword 0x0366  @ icid=0x13F9 ( 5113)  -> cid=870 slot=0x13F9  Fairy Box
    .hword 0x0367  @ icid=0x13FA ( 5114)  -> cid=871 slot=0x13FA  Torrential Tribute
    .hword 0x0821  @ icid=0x13FB ( 5115)  -> cid=2081 slot=0x13FB
    .hword 0x0368  @ icid=0x13FC ( 5116)  -> cid=872 slot=0x13FC  Multiplication of Ants
    .hword 0xFFFF  @ icid=0x13FD ( 5117)  -> (none)
    .hword 0x0369  @ icid=0x13FE ( 5118)  -> cid=873 slot=0x13FE  De-Fusion
    .hword 0x036A  @ icid=0x13FF ( 5119)  -> cid=874 slot=0x13FF  Jam Breeding Machine
    .hword 0x036B  @ icid=0x1400 ( 5120)  -> cid=875 slot=0x1400  Nightmare's Steelcage
    .hword 0x036C  @ icid=0x1401 ( 5121)  -> cid=876 slot=0x1401  Infinite Cards
    .hword 0x036D  @ icid=0x1402 ( 5122)  -> cid=877 slot=0x1402  Jam Defender
    .hword 0x036E  @ icid=0x1403 ( 5123)  -> cid=878 slot=0x1403  Card of Safe Return
    .hword 0x036F  @ icid=0x1404 ( 5124)  -> cid=879 slot=0x1404  Magic Cylinder
    .hword 0x0370  @ icid=0x1405 ( 5125)  -> cid=880 slot=0x1405  Solemn Wishes
    .hword 0x0371  @ icid=0x1406 ( 5126)  -> cid=881 slot=0x1406  Burning Land
    .hword 0x0372  @ icid=0x1407 ( 5127)  -> cid=882 slot=0x1407  Cold Wave
    .hword 0x0373  @ icid=0x1408 ( 5128)  -> cid=883 slot=0x1408  Fairy Meteor Crush
    .hword 0x0374  @ icid=0x1409 ( 5129)  -> cid=884 slot=0x1409  Limiter Removal
    .hword 0x0375  @ icid=0x140A ( 5130)  -> cid=885 slot=0x140A  Shift
    .hword 0x0376  @ icid=0x140B ( 5131)  -> cid=886 slot=0x140B  Insect Imitation
    .hword 0x0377  @ icid=0x140C ( 5132)  -> cid=887 slot=0x140C  Dimensionhole
    .hword 0x0378  @ icid=0x140D ( 5133)  -> cid=888 slot=0x140D  Magic Drain
    .hword 0x0379  @ icid=0x140E ( 5134)  -> cid=889 slot=0x140E  Gravity Bind
    .hword 0x037A  @ icid=0x140F ( 5135)  -> cid=890 slot=0x140F  Shadow of Eyes
    .hword 0x037B  @ icid=0x1410 ( 5136)  -> cid=891 slot=0x1410  Girochin Kuwagata
    .hword 0x037C  @ icid=0x1411 ( 5137)  -> cid=892 slot=0x1411  Hayabusa Knight
    .hword 0x037D  @ icid=0x1412 ( 5138)  -> cid=893 slot=0x1412  Bombardment Beetle
    .hword 0x037E  @ icid=0x1413 ( 5139)  -> cid=894 slot=0x1413  4-Starred Ladybug of Doom
    .hword 0x037F  @ icid=0x1414 ( 5140)  -> cid=895 slot=0x1414  Gradius
    .hword 0x0380  @ icid=0x1415 ( 5141)  -> cid=896 slot=0x1415  Red-Moon Baby
    .hword 0x0381  @ icid=0x1416 ( 5142)  -> cid=897 slot=0x1416  Mad Sword Beast
    .hword 0x0382  @ icid=0x1417 ( 5143)  -> cid=898 slot=0x1417  Skull Mariner
    .hword 0x0383  @ icid=0x1418 ( 5144)  -> cid=899 slot=0x1418  The All-Seeing White Tiger
    .hword 0x0384  @ icid=0x1419 ( 5145)  -> cid=900 slot=0x1419  Goblin Attack Force
    .hword 0x0385  @ icid=0x141A ( 5146)  -> cid=901 slot=0x141A  Island Turtle
    .hword 0x0386  @ icid=0x141B ( 5147)  -> cid=902 slot=0x141B  Wingweaver
    .hword 0x0387  @ icid=0x141C ( 5148)  -> cid=903 slot=0x141C  Science Soldier
    .hword 0x0388  @ icid=0x141D ( 5149)  -> cid=904 slot=0x141D  Souls of the Forgotten
    .hword 0x0389  @ icid=0x141E ( 5150)  -> cid=905 slot=0x141E  Dokuroyaiba
    .hword 0x038A  @ icid=0x141F ( 5151)  -> cid=906 slot=0x141F  Rain of Mercy
    .hword 0x038B  @ icid=0x1420 ( 5152)  -> cid=907 slot=0x1420  Monster Recovery
    .hword 0x038C  @ icid=0x1421 ( 5153)  -> cid=908 slot=0x1421  Type Zero Magic Crusher
    .hword 0x0824  @ icid=0x1422 ( 5154)  -> cid=2084 slot=0x1422
    .hword 0xFFFF  @ icid=0x1423 ( 5155)  -> (none)
    .hword 0xFFFF  @ icid=0x1424 ( 5156)  -> (none)
    .hword 0xFFFF  @ icid=0x1425 ( 5157)  -> (none)
    .hword 0xFFFF  @ icid=0x1426 ( 5158)  -> (none)
    .hword 0xFFFF  @ icid=0x1427 ( 5159)  -> (none)
    .hword 0xFFFF  @ icid=0x1428 ( 5160)  -> (none)
    .hword 0x038D  @ icid=0x1429 ( 5161)  -> cid=909 slot=0x1429  Yellow Luster Shield
    .hword 0x038E  @ icid=0x142A ( 5162)  -> cid=910 slot=0x142A  Creature Swap
    .hword 0xFFFF  @ icid=0x142B ( 5163)  -> (none)
    .hword 0xFFFF  @ icid=0x142C ( 5164)  -> (none)
    .hword 0x038F  @ icid=0x142D ( 5165)  -> cid=911 slot=0x142D  Dark Magician
    .hword 0x0390  @ icid=0x142E ( 5166)  -> cid=912 slot=0x142E  Thousand Knives
    .hword 0xFFFF  @ icid=0x142F ( 5167)  -> (none)
    .hword 0x0391  @ icid=0x1430 ( 5168)  -> cid=913 slot=0x1430  Mystic Box
    .hword 0xFFFF  @ icid=0x1431 ( 5169)  -> (none)
    .hword 0x0392  @ icid=0x1432 ( 5170)  -> cid=914 slot=0x1432  Ground Collapse
    .hword 0xFFFF  @ icid=0x1433 ( 5171)  -> (none)
    .hword 0xFFFF  @ icid=0x1434 ( 5172)  -> (none)
    .hword 0xFFFF  @ icid=0x1435 ( 5173)  -> (none)
    .hword 0xFFFF  @ icid=0x1436 ( 5174)  -> (none)
    .hword 0xFFFF  @ icid=0x1437 ( 5175)  -> (none)
    .hword 0xFFFF  @ icid=0x1438 ( 5176)  -> (none)
    .hword 0xFFFF  @ icid=0x1439 ( 5177)  -> (none)
    .hword 0xFFFF  @ icid=0x143A ( 5178)  -> (none)
    .hword 0xFFFF  @ icid=0x143B ( 5179)  -> (none)
    .hword 0xFFFF  @ icid=0x143C ( 5180)  -> (none)
    .hword 0xFFFF  @ icid=0x143D ( 5181)  -> (none)
    .hword 0xFFFF  @ icid=0x143E ( 5182)  -> (none)
    .hword 0xFFFF  @ icid=0x143F ( 5183)  -> (none)
    .hword 0xFFFF  @ icid=0x1440 ( 5184)  -> (none)
    .hword 0xFFFF  @ icid=0x1441 ( 5185)  -> (none)
    .hword 0xFFFF  @ icid=0x1442 ( 5186)  -> (none)
    .hword 0xFFFF  @ icid=0x1443 ( 5187)  -> (none)
    .hword 0xFFFF  @ icid=0x1444 ( 5188)  -> (none)
    .hword 0xFFFF  @ icid=0x1445 ( 5189)  -> (none)
    .hword 0xFFFF  @ icid=0x1446 ( 5190)  -> (none)
    .hword 0xFFFF  @ icid=0x1447 ( 5191)  -> (none)
    .hword 0xFFFF  @ icid=0x1448 ( 5192)  -> (none)
    .hword 0xFFFF  @ icid=0x1449 ( 5193)  -> (none)
    .hword 0xFFFF  @ icid=0x144A ( 5194)  -> (none)
    .hword 0x0393  @ icid=0x144B ( 5195)  -> cid=915 slot=0x144B  Amazon Archer
    .hword 0xFFFF  @ icid=0x144C ( 5196)  -> (none)
    .hword 0x0394  @ icid=0x144D ( 5197)  -> cid=916 slot=0x144D  Fire Princess
    .hword 0xFFFF  @ icid=0x144E ( 5198)  -> (none)
    .hword 0xFFFF  @ icid=0x144F ( 5199)  -> (none)
    .hword 0x0395  @ icid=0x1450 ( 5200)  -> cid=917 slot=0x1450  Spirit of the Breeze
    .hword 0x0396  @ icid=0x1451 ( 5201)  -> cid=918 slot=0x1451  Dancing Fairy
    .hword 0xFFFF  @ icid=0x1452 ( 5202)  -> (none)
    .hword 0x0397  @ icid=0x1453 ( 5203)  -> cid=919 slot=0x1453  Empress Mantis
    .hword 0x0398  @ icid=0x1454 ( 5204)  -> cid=920 slot=0x1454  Cure Mermaid
    .hword 0x0399  @ icid=0x1455 ( 5205)  -> cid=921 slot=0x1455  Hysteric Fairy
    .hword 0x039A  @ icid=0x1456 ( 5206)  -> cid=922 slot=0x1456  Bio-Mage
    .hword 0x039B  @ icid=0x1457 ( 5207)  -> cid=923 slot=0x1457  The Forgiving Maiden
    .hword 0x039C  @ icid=0x1458 ( 5208)  -> cid=924 slot=0x1458  St. Joan
    .hword 0x039D  @ icid=0x1459 ( 5209)  -> cid=925 slot=0x1459  Marie the Fallen One
    .hword 0x039E  @ icid=0x145A ( 5210)  -> cid=926 slot=0x145A  Jar of Greed
    .hword 0x039F  @ icid=0x145B ( 5211)  -> cid=927 slot=0x145B  Scroll of Bewitchment
    .hword 0x03A0  @ icid=0x145C ( 5212)  -> cid=928 slot=0x145C  United We Stand
    .hword 0x03A1  @ icid=0x145D ( 5213)  -> cid=929 slot=0x145D  Mage Power
    .hword 0x03A2  @ icid=0x145E ( 5214)  -> cid=930 slot=0x145E  Offerings to the Doomed
    .hword 0xFFFF  @ icid=0x145F ( 5215)  -> (none)
    .hword 0x03A3  @ icid=0x1460 ( 5216)  -> cid=931 slot=0x1460  Meteor of Destruction
    .hword 0x03A4  @ icid=0x1461 ( 5217)  -> cid=932 slot=0x1461  Lightning Vortex
    .hword 0x03A5  @ icid=0x1462 ( 5218)  -> cid=933 slot=0x1462  Exchange
    .hword 0x03A6  @ icid=0x1463 ( 5219)  -> cid=934 slot=0x1463  The Portrait's Secret
    .hword 0x03A7  @ icid=0x1464 ( 5220)  -> cid=935 slot=0x1464  The Gross Ghost of Fled Dreams
    .hword 0x03A8  @ icid=0x1465 ( 5221)  -> cid=936 slot=0x1465  Headless Knight
    .hword 0x03A9  @ icid=0x1466 ( 5222)  -> cid=937 slot=0x1466  Dark Necrofear
    .hword 0x03AA  @ icid=0x1467 ( 5223)  -> cid=938 slot=0x1467  Dark Magician's Tome of Black Magic
    .hword 0x03AB  @ icid=0x1468 ( 5224)  -> cid=939 slot=0x1468  Destiny Board
    .hword 0x03AC  @ icid=0x1469 ( 5225)  -> cid=940 slot=0x1469  The Dark Door
    .hword 0x03AD  @ icid=0x146A ( 5226)  -> cid=941 slot=0x146A  Earthbound Spirit
    .hword 0x03AE  @ icid=0x146B ( 5227)  -> cid=942 slot=0x146B  Dark Spirit of the Silent
    .hword 0xFFFF  @ icid=0x146C ( 5228)  -> (none)
    .hword 0x03AF  @ icid=0x146D ( 5229)  -> cid=943 slot=0x146D  The Earl of Demise
    .hword 0x03B0  @ icid=0x146E ( 5230)  -> cid=944 slot=0x146E  Dark Sage
    .hword 0x03B1  @ icid=0x146F ( 5231)  -> cid=945 slot=0x146F  Cathedral of Nobles
    .hword 0x03B2  @ icid=0x1470 ( 5232)  -> cid=946 slot=0x1470  Judgment of Anubis
    .hword 0xFFFF  @ icid=0x1471 ( 5233)  -> (none)
    .hword 0x03B3  @ icid=0x1472 ( 5234)  -> cid=947 slot=0x1472  Embodiment of Apophis
    .hword 0xFFFF  @ icid=0x1473 ( 5235)  -> (none)
    .hword 0x03B4  @ icid=0x1474 ( 5236)  -> cid=948 slot=0x1474  Foolish Burial
    .hword 0x03B5  @ icid=0x1475 ( 5237)  -> cid=949 slot=0x1475  Makiu
    .hword 0x03B6  @ icid=0x1476 ( 5238)  -> cid=950 slot=0x1476  Ancient Lamp
    .hword 0x03B7  @ icid=0x1477 ( 5239)  -> cid=951 slot=0x1477  Cyber Harpie Lady
    .hword 0xFFFF  @ icid=0x1478 ( 5240)  -> (none)
    .hword 0xFFFF  @ icid=0x1479 ( 5241)  -> (none)
    .hword 0x03B8  @ icid=0x147A ( 5242)  -> cid=952 slot=0x147A  Mystical Beast Serket
    .hword 0x03B9  @ icid=0x147B ( 5243)  -> cid=953 slot=0x147B  Swift Gaia the Fierce Knight
    .hword 0x03BA  @ icid=0x147C ( 5244)  -> cid=954 slot=0x147C  Obnoxious Celtic Guard
    .hword 0x03BB  @ icid=0x147D ( 5245)  -> cid=955 slot=0x147D  Zombyra the Dark
    .hword 0x03BC  @ icid=0x147E ( 5246)  -> cid=956 slot=0x147E  Spiritualism
    .hword 0x03BD  @ icid=0x147F ( 5247)  -> cid=957 slot=0x147F  Jowgen the Spiritualist
    .hword 0x03BE  @ icid=0x1480 ( 5248)  -> cid=958 slot=0x1480  Kycoo the Ghost Destroyer
    .hword 0x03BF  @ icid=0x1481 ( 5249)  -> cid=959 slot=0x1481  Summoner of Illusions
    .hword 0x03C0  @ icid=0x1482 ( 5250)  -> cid=960 slot=0x1482  Bazoo the Soul-Eater
    .hword 0x03C1  @ icid=0x1483 ( 5251)  -> cid=961 slot=0x1483  Soul of Purity and Light
    .hword 0x03C2  @ icid=0x1484 ( 5252)  -> cid=962 slot=0x1484  Spirit of Flames
    .hword 0x03C3  @ icid=0x1485 ( 5253)  -> cid=963 slot=0x1485  Aqua Spirit
    .hword 0x03C4  @ icid=0x1486 ( 5254)  -> cid=964 slot=0x1486  The Rock Spirit
    .hword 0x03C5  @ icid=0x1487 ( 5255)  -> cid=965 slot=0x1487  Garuda the Wind Spirit
    .hword 0x03C6  @ icid=0x1488 ( 5256)  -> cid=966 slot=0x1488  Gilasaurus
    .hword 0x03C7  @ icid=0x1489 ( 5257)  -> cid=967 slot=0x1489  Tornado Bird
    .hword 0x03C8  @ icid=0x148A ( 5258)  -> cid=968 slot=0x148A  Dreamsprite
    .hword 0x03C9  @ icid=0x148B ( 5259)  -> cid=969 slot=0x148B  Supply
    .hword 0x03CA  @ icid=0x148C ( 5260)  -> cid=970 slot=0x148C  Maryokutai
    .hword 0x03CB  @ icid=0x148D ( 5261)  -> cid=971 slot=0x148D  Collected Power
    .hword 0x03CC  @ icid=0x148E ( 5262)  -> cid=972 slot=0x148E  Royal Command
    .hword 0x03CD  @ icid=0x148F ( 5263)  -> cid=973 slot=0x148F  Riryoku Field
    .hword 0x03CE  @ icid=0x1490 ( 5264)  -> cid=974 slot=0x1490  Skull Lair
    .hword 0x03CF  @ icid=0x1491 ( 5265)  -> cid=975 slot=0x1491  Graverobber's Retribution
    .hword 0x03D0  @ icid=0x1492 ( 5266)  -> cid=976 slot=0x1492  Deal of Phantom
    .hword 0x03D1  @ icid=0x1493 ( 5267)  -> cid=977 slot=0x1493  Destruction Punch
    .hword 0x03D2  @ icid=0x1494 ( 5268)  -> cid=978 slot=0x1494  Blind Destruction
    .hword 0x03D3  @ icid=0x1495 ( 5269)  -> cid=979 slot=0x1495  The Emperor's Holiday
    .hword 0x03D4  @ icid=0x1496 ( 5270)  -> cid=980 slot=0x1496  Cyclon Laser
    .hword 0x03D5  @ icid=0x1497 ( 5271)  -> cid=981 slot=0x1497  Spirit Message "I"
    .hword 0x03D6  @ icid=0x1498 ( 5272)  -> cid=982 slot=0x1498  Spirit Message "N"
    .hword 0x03D7  @ icid=0x1499 ( 5273)  -> cid=983 slot=0x1499  Spirit Message "A"
    .hword 0x03D8  @ icid=0x149A ( 5274)  -> cid=984 slot=0x149A  Spirit Message "L"
    .hword 0x03D9  @ icid=0x149B ( 5275)  -> cid=985 slot=0x149B  Bait Doll
    .hword 0x03DA  @ icid=0x149C ( 5276)  -> cid=986 slot=0x149C  Fusion Gate
    .hword 0x03DB  @ icid=0x149D ( 5277)  -> cid=987 slot=0x149D  Ekibyo Drakmord
    .hword 0x03DC  @ icid=0x149E ( 5278)  -> cid=988 slot=0x149E  Miracle Dig
    .hword 0xFFFF  @ icid=0x149F ( 5279)  -> (none)
    .hword 0xFFFF  @ icid=0x14A0 ( 5280)  -> (none)
    .hword 0x03DD  @ icid=0x14A1 ( 5281)  -> cid=989 slot=0x14A1  Vengeful Bog Spirit
    .hword 0xFFFF  @ icid=0x14A2 ( 5282)  -> (none)
    .hword 0xFFFF  @ icid=0x14A3 ( 5283)  -> (none)
    .hword 0x03DE  @ icid=0x14A4 ( 5284)  -> cid=990 slot=0x14A4  Amazoness Swords Woman
    .hword 0x03DF  @ icid=0x14A5 ( 5285)  -> cid=991 slot=0x14A5  Makyura the Destructor
    .hword 0x03E0  @ icid=0x14A6 ( 5286)  -> cid=992 slot=0x14A6  Amazoness Archers
    .hword 0x03E1  @ icid=0x14A7 ( 5287)  -> cid=993 slot=0x14A7  Rope of Life
    .hword 0xFFFF  @ icid=0x14A8 ( 5288)  -> (none)
    .hword 0xFFFF  @ icid=0x14A9 ( 5289)  -> (none)
    .hword 0x03E2  @ icid=0x14AA ( 5290)  -> cid=994 slot=0x14AA  Enchanted Arrow
    .hword 0x03E3  @ icid=0x14AB ( 5291)  -> cid=995 slot=0x14AB  Amazoness Chain Master
    .hword 0x03E4  @ icid=0x14AC ( 5292)  -> cid=996 slot=0x14AC  Viser Des
    .hword 0xFFFF  @ icid=0x14AD ( 5293)  -> (none)
    .hword 0xFFFF  @ icid=0x14AE ( 5294)  -> (none)
    .hword 0x03E6  @ icid=0x14AF ( 5295)  -> cid=998 slot=0x14AF  Amazoness Fighter
    .hword 0xFFFF  @ icid=0x14B0 ( 5296)  -> (none)
    .hword 0xFFFF  @ icid=0x14B1 ( 5297)  -> (none)
    .hword 0x03E7  @ icid=0x14B2 ( 5298)  -> cid=999 slot=0x14B2  Nightmare Wheel
    .hword 0xFFFF  @ icid=0x14B3 ( 5299)  -> (none)
    .hword 0x03E8  @ icid=0x14B4 ( 5300)  -> cid=1000 slot=0x14B4  Byser Shock
    .hword 0x03E9  @ icid=0x14B5 ( 5301)  -> cid=1001 slot=0x14B5  Dark Ruler Ha Des
    .hword 0x03EA  @ icid=0x14B6 ( 5302)  -> cid=1002 slot=0x14B6  Dark Balter the Terrible
    .hword 0x03EB  @ icid=0x14B7 ( 5303)  -> cid=1003 slot=0x14B7  Lesser Fiend
    .hword 0x03EC  @ icid=0x14B8 ( 5304)  -> cid=1004 slot=0x14B8  Possessed Dark Soul
    .hword 0x03ED  @ icid=0x14B9 ( 5305)  -> cid=1005 slot=0x14B9  Winged Minion
    .hword 0xFFFF  @ icid=0x14BA ( 5306)  -> (none)
    .hword 0x03EE  @ icid=0x14BB ( 5307)  -> cid=1006 slot=0x14BB  Ryu-Kishin Clown
    .hword 0x03EF  @ icid=0x14BC ( 5308)  -> cid=1007 slot=0x14BC  Twin-Headed Wolf
    .hword 0x03F0  @ icid=0x14BD ( 5309)  -> cid=1008 slot=0x14BD  Opticlops
    .hword 0x03F1  @ icid=0x14BE ( 5310)  -> cid=1009 slot=0x14BE  Bark of Dark Ruler
    .hword 0x03F2  @ icid=0x14BF ( 5311)  -> cid=1010 slot=0x14BF  Fatal Abacus
    .hword 0x03F3  @ icid=0x14C0 ( 5312)  -> cid=1011 slot=0x14C0  Life Absorbing Machine
    .hword 0xFFFF  @ icid=0x14C1 ( 5313)  -> (none)
    .hword 0xFFFF  @ icid=0x14C2 ( 5314)  -> (none)
    .hword 0x03F4  @ icid=0x14C3 ( 5315)  -> cid=1012 slot=0x14C3  Double Snare
    .hword 0x03F5  @ icid=0x14C4 ( 5316)  -> cid=1013 slot=0x14C4  Freed the Matchless General
    .hword 0x03F6  @ icid=0x14C5 ( 5317)  -> cid=1014 slot=0x14C5  Throwstone Unit
    .hword 0x03F7  @ icid=0x14C6 ( 5318)  -> cid=1015 slot=0x14C6  Marauding Captain
    .hword 0x03F8  @ icid=0x14C7 ( 5319)  -> cid=1016 slot=0x14C7  Ryu Senshi
    .hword 0x03F9  @ icid=0x14C8 ( 5320)  -> cid=1017 slot=0x14C8  Warrior Dai Grepher
    .hword 0xFFFF  @ icid=0x14C9 ( 5321)  -> (none)
    .hword 0x03FA  @ icid=0x14CA ( 5322)  -> cid=1018 slot=0x14CA  Frontier Wiseman
    .hword 0x03FB  @ icid=0x14CB ( 5323)  -> cid=1019 slot=0x14CB  Exiled Force
    .hword 0x03FC  @ icid=0x14CC ( 5324)  -> cid=1020 slot=0x14CC  The Hunter with 7 Weapons
    .hword 0x03FD  @ icid=0x14CD ( 5325)  -> cid=1021 slot=0x14CD  Shadow Tamer
    .hword 0x03FE  @ icid=0x14CE ( 5326)  -> cid=1022 slot=0x14CE  Dragon Manipulator
    .hword 0x03FF  @ icid=0x14CF ( 5327)  -> cid=1023 slot=0x14CF  The A. Forces
    .hword 0x0400  @ icid=0x14D0 ( 5328)  -> cid=1024 slot=0x14D0  Reinforcement of the Army
    .hword 0x0401  @ icid=0x14D1 ( 5329)  -> cid=1025 slot=0x14D1  Array of Revealing Light
    .hword 0x0402  @ icid=0x14D2 ( 5330)  -> cid=1026 slot=0x14D2  The Warrior Returning Alive
    .hword 0x0403  @ icid=0x14D3 ( 5331)  -> cid=1027 slot=0x14D3  Ready for Intercepting
    .hword 0x0404  @ icid=0x14D4 ( 5332)  -> cid=1028 slot=0x14D4  A Feint Plan
    .hword 0x0405  @ icid=0x14D5 ( 5333)  -> cid=1029 slot=0x14D5  Tyrant Dragon
    .hword 0x0406  @ icid=0x14D6 ( 5334)  -> cid=1030 slot=0x14D6  Spear Dragon
    .hword 0x0407  @ icid=0x14D7 ( 5335)  -> cid=1031 slot=0x14D7  Spirit Ryu
    .hword 0x0408  @ icid=0x14D8 ( 5336)  -> cid=1032 slot=0x14D8  The Dragon dwelling in the Cave
    .hword 0x0409  @ icid=0x14D9 ( 5337)  -> cid=1033 slot=0x14D9  Lizard Soldier
    .hword 0x040A  @ icid=0x14DA ( 5338)  -> cid=1034 slot=0x14DA  Fiend Skull Dragon
    .hword 0x040B  @ icid=0x14DB ( 5339)  -> cid=1035 slot=0x14DB  Cave Dragon
    .hword 0x040C  @ icid=0x14DC ( 5340)  -> cid=1036 slot=0x14DC  Gray Wing
    .hword 0x040D  @ icid=0x14DD ( 5341)  -> cid=1037 slot=0x14DD  Troop Dragon
    .hword 0x040E  @ icid=0x14DE ( 5342)  -> cid=1038 slot=0x14DE  The Dragon's Bead
    .hword 0x040F  @ icid=0x14DF ( 5343)  -> cid=1039 slot=0x14DF  A Wingbeat of Giant Dragon
    .hword 0x0410  @ icid=0x14E0 ( 5344)  -> cid=1040 slot=0x14E0  Dragon's Gunfire
    .hword 0x0411  @ icid=0x14E1 ( 5345)  -> cid=1041 slot=0x14E1  Stamping Destruction
    .hword 0x0412  @ icid=0x14E2 ( 5346)  -> cid=1042 slot=0x14E2  Super Rejuvenation
    .hword 0x0413  @ icid=0x14E3 ( 5347)  -> cid=1043 slot=0x14E3  Dragon's Rage
    .hword 0x0414  @ icid=0x14E4 ( 5348)  -> cid=1044 slot=0x14E4  Burst Breath
    .hword 0x0415  @ icid=0x14E5 ( 5349)  -> cid=1045 slot=0x14E5  Luster Dragon #2
    .hword 0x0416  @ icid=0x14E6 ( 5350)  -> cid=1046 slot=0x14E6  Emergency Provisions
    .hword 0x0417  @ icid=0x14E7 ( 5351)  -> cid=1047 slot=0x14E7  Keldo
    .hword 0x0418  @ icid=0x14E8 ( 5352)  -> cid=1048 slot=0x14E8  Dragged Down into the Grave
    .hword 0x0419  @ icid=0x14E9 ( 5353)  -> cid=1049 slot=0x14E9  Kaiser Glider
    .hword 0x041A  @ icid=0x14EA ( 5354)  -> cid=1050 slot=0x14EA  Spell Reproduction
    .hword 0x041B  @ icid=0x14EB ( 5355)  -> cid=1051 slot=0x14EB  Collapse
    .hword 0x041C  @ icid=0x14EC ( 5356)  -> cid=1052 slot=0x14EC  Mudora
    .hword 0x041D  @ icid=0x14ED ( 5357)  -> cid=1053 slot=0x14ED  Cestus of Dagla
    .hword 0x041E  @ icid=0x14EE ( 5358)  -> cid=1054 slot=0x14EE  De-Spell Germ Weapon
    .hword 0x041F  @ icid=0x14EF ( 5359)  -> cid=1055 slot=0x14EF  Des Feral Imp
    .hword 0x0420  @ icid=0x14F0 ( 5360)  -> cid=1056 slot=0x14F0  Reversal of Graves
    .hword 0x0421  @ icid=0x14F1 ( 5361)  -> cid=1057 slot=0x14F1  Kelbek
    .hword 0xFFFF  @ icid=0x14F2 ( 5362)  -> (none)
    .hword 0x0422  @ icid=0x14F3 ( 5363)  -> cid=1058 slot=0x14F3  Zolga
    .hword 0xFFFF  @ icid=0x14F4 ( 5364)  -> (none)
    .hword 0x0423  @ icid=0x14F5 ( 5365)  -> cid=1059 slot=0x14F5  Blast Held by a Tribute
    .hword 0x0424  @ icid=0x14F6 ( 5366)  -> cid=1060 slot=0x14F6  Agido
    .hword 0x0425  @ icid=0x14F7 ( 5367)  -> cid=1061 slot=0x14F7  Silent Fiend
    .hword 0x0822  @ icid=0x14F8 ( 5368)  -> cid=2082 slot=0x14F8
    .hword 0x0823  @ icid=0x14F9 ( 5369)  -> cid=2083 slot=0x14F9
    .hword 0x0825  @ icid=0x14FA ( 5370)  -> cid=2085 slot=0x14FA
    .hword 0x0426  @ icid=0x14FB ( 5371)  -> cid=1062 slot=0x14FB  Fiber Jar
    .hword 0x0427  @ icid=0x14FC ( 5372)  -> cid=1063 slot=0x14FC  Gradius' Option
    .hword 0x0428  @ icid=0x14FD ( 5373)  -> cid=1064 slot=0x14FD  Maharaghi
    .hword 0x0429  @ icid=0x14FE ( 5374)  -> cid=1065 slot=0x14FE  Inaba White Rabbit
    .hword 0x042A  @ icid=0x14FF ( 5375)  -> cid=1066 slot=0x14FF  Yata-Garasu
    .hword 0x042B  @ icid=0x1500 ( 5376)  -> cid=1067 slot=0x1500  Susa Soldier
    .hword 0x042C  @ icid=0x1501 ( 5377)  -> cid=1068 slot=0x1501  Yamata Dragon
    .hword 0x042D  @ icid=0x1502 ( 5378)  -> cid=1069 slot=0x1502  Great Long Nose
    .hword 0x042E  @ icid=0x1503 ( 5379)  -> cid=1070 slot=0x1503  Otohime
    .hword 0x042F  @ icid=0x1504 ( 5380)  -> cid=1071 slot=0x1504  Hino-Kagu-Tsuchi
    .hword 0x0430  @ icid=0x1505 ( 5381)  -> cid=1072 slot=0x1505  Asura Priest
    .hword 0x0431  @ icid=0x1506 ( 5382)  -> cid=1073 slot=0x1506  Fushi No Tori
    .hword 0x0432  @ icid=0x1507 ( 5383)  -> cid=1074 slot=0x1507  Super Robolady
    .hword 0x0433  @ icid=0x1508 ( 5384)  -> cid=1075 slot=0x1508  Super Roboyarou
    .hword 0x0434  @ icid=0x1509 ( 5385)  -> cid=1076 slot=0x1509  Fengsheng Mirror
    .hword 0x0435  @ icid=0x150A ( 5386)  -> cid=1077 slot=0x150A  Heart of Clear Water
    .hword 0x0436  @ icid=0x150B ( 5387)  -> cid=1078 slot=0x150B  A Legendary Ocean
    .hword 0x0437  @ icid=0x150C ( 5388)  -> cid=1079 slot=0x150C  Fusion Sword Murasame Blade
    .hword 0x0438  @ icid=0x150D ( 5389)  -> cid=1080 slot=0x150D  Smoke Grenade of the Thief
    .hword 0x0439  @ icid=0x150E ( 5390)  -> cid=1081 slot=0x150E  Spiritual Energy Settle Machine
    .hword 0x043A  @ icid=0x150F ( 5391)  -> cid=1082 slot=0x150F  Second Coin Toss
    .hword 0x043B  @ icid=0x1510 ( 5392)  -> cid=1083 slot=0x1510  Convulsion of Nature
    .hword 0x043C  @ icid=0x1511 ( 5393)  -> cid=1084 slot=0x1511  The Secret of the Bandit
    .hword 0x043D  @ icid=0x1512 ( 5394)  -> cid=1085 slot=0x1512  After the Struggle
    .hword 0xFFFF  @ icid=0x1513 ( 5395)  -> (none)
    .hword 0x043E  @ icid=0x1514 ( 5396)  -> cid=1086 slot=0x1514  Blast with Chain
    .hword 0x043F  @ icid=0x1515 ( 5397)  -> cid=1087 slot=0x1515  Disappear
    .hword 0xFFFF  @ icid=0x1516 ( 5398)  -> (none)
    .hword 0xFFFF  @ icid=0x1517 ( 5399)  -> (none)
    .hword 0x0440  @ icid=0x1518 ( 5400)  -> cid=1088 slot=0x1518  Bottomless Trap Hole
    .hword 0x0441  @ icid=0x1519 ( 5401)  -> cid=1089 slot=0x1519  Ominous Fortunetelling
    .hword 0xFFFF  @ icid=0x151A ( 5402)  -> (none)
    .hword 0x0442  @ icid=0x151B ( 5403)  -> cid=1090 slot=0x151B  Nutrient Z
    .hword 0x0443  @ icid=0x151C ( 5404)  -> cid=1091 slot=0x151C  Drop Off
    .hword 0x0444  @ icid=0x151D ( 5405)  -> cid=1092 slot=0x151D  Fiend Comedian
    .hword 0x0445  @ icid=0x151E ( 5406)  -> cid=1093 slot=0x151E  Last Turn
    .hword 0xFFFF  @ icid=0x151F ( 5407)  -> (none)
    .hword 0x0446  @ icid=0x1520 ( 5408)  -> cid=1094 slot=0x1520  Des Volstgalph
    .hword 0x0447  @ icid=0x1521 ( 5409)  -> cid=1095 slot=0x1521  Kaiser Sea Horse
    .hword 0x0448  @ icid=0x1522 ( 5410)  -> cid=1096 slot=0x1522  Vampire Lord
    .hword 0x0449  @ icid=0x1523 ( 5411)  -> cid=1097 slot=0x1523  Gora Turtle
    .hword 0x044A  @ icid=0x1524 ( 5412)  -> cid=1098 slot=0x1524  Sasuke Samurai
    .hword 0x044B  @ icid=0x1525 ( 5413)  -> cid=1099 slot=0x1525  Poison Mummy
    .hword 0x044C  @ icid=0x1526 ( 5414)  -> cid=1100 slot=0x1526  Dark Dust Spirit
    .hword 0x044D  @ icid=0x1527 ( 5415)  -> cid=1101 slot=0x1527  Royal Keeper
    .hword 0x044E  @ icid=0x1528 ( 5416)  -> cid=1102 slot=0x1528  Wandering Mummy
    .hword 0x044F  @ icid=0x1529 ( 5417)  -> cid=1103 slot=0x1529  Great Dezard
    .hword 0x0450  @ icid=0x152A ( 5418)  -> cid=1104 slot=0x152A  Swarm of Scarabs
    .hword 0x0451  @ icid=0x152B ( 5419)  -> cid=1105 slot=0x152B  Swarm of Locusts
    .hword 0x0452  @ icid=0x152C ( 5420)  -> cid=1106 slot=0x152C  Giant Axe Mummy
    .hword 0xFFFF  @ icid=0x152D ( 5421)  -> (none)
    .hword 0x0453  @ icid=0x152E ( 5422)  -> cid=1107 slot=0x152E  Guardian Sphinx
    .hword 0x0454  @ icid=0x152F ( 5423)  -> cid=1108 slot=0x152F  Pyramid Turtle
    .hword 0x0455  @ icid=0x1530 ( 5424)  -> cid=1109 slot=0x1530  Dice Jar
    .hword 0x0456  @ icid=0x1531 ( 5425)  -> cid=1110 slot=0x1531  Dark Scorpion Burglars
    .hword 0x0457  @ icid=0x1532 ( 5426)  -> cid=1111 slot=0x1532  Don Zaloog
    .hword 0x0458  @ icid=0x1533 ( 5427)  -> cid=1112 slot=0x1533  Des Lacooda
    .hword 0x0459  @ icid=0x1534 ( 5428)  -> cid=1113 slot=0x1534  Fushioh Richie
    .hword 0x045A  @ icid=0x1535 ( 5429)  -> cid=1114 slot=0x1535  Cobraman Sakuzy
    .hword 0x045B  @ icid=0x1536 ( 5430)  -> cid=1115 slot=0x1536  Book of Life
    .hword 0x045C  @ icid=0x1537 ( 5431)  -> cid=1116 slot=0x1537  Book of Taiyou
    .hword 0x045D  @ icid=0x1538 ( 5432)  -> cid=1117 slot=0x1538  Book of Moon
    .hword 0x045E  @ icid=0x1539 ( 5433)  -> cid=1118 slot=0x1539  Mirage of Nightmare
    .hword 0xFFFF  @ icid=0x153A ( 5434)  -> (none)
    .hword 0x045F  @ icid=0x153B ( 5435)  -> cid=1119 slot=0x153B  Call of the Mummy
    .hword 0x0460  @ icid=0x153C ( 5436)  -> cid=1120 slot=0x153C  Timidity
    .hword 0x0461  @ icid=0x153D ( 5437)  -> cid=1121 slot=0x153D  Pyramid Energy
    .hword 0x0462  @ icid=0x153E ( 5438)  -> cid=1122 slot=0x153E  Tutan Mask
    .hword 0x0463  @ icid=0x153F ( 5439)  -> cid=1123 slot=0x153F  Ordeal of a Traveler
    .hword 0x0464  @ icid=0x1540 ( 5440)  -> cid=1124 slot=0x1540  Bottomless Shifting Sand
    .hword 0x0465  @ icid=0x1541 ( 5441)  -> cid=1125 slot=0x1541  Curse of Royal
    .hword 0x0466  @ icid=0x1542 ( 5442)  -> cid=1126 slot=0x1542  Needle Ceiling
    .hword 0x0467  @ icid=0x1543 ( 5443)  -> cid=1127 slot=0x1543  Statue of the Wicked
    .hword 0x0468  @ icid=0x1544 ( 5444)  -> cid=1128 slot=0x1544  Dark Coffin
    .hword 0x0469  @ icid=0x1545 ( 5445)  -> cid=1129 slot=0x1545  Needle Wall
    .hword 0x046A  @ icid=0x1546 ( 5446)  -> cid=1130 slot=0x1546  Trap Dustshoot
    .hword 0xFFFF  @ icid=0x1547 ( 5447)  -> (none)
    .hword 0x046B  @ icid=0x1548 ( 5448)  -> cid=1131 slot=0x1548  Reckless Greed
    .hword 0xFFFF  @ icid=0x1549 ( 5449)  -> (none)
    .hword 0x046C  @ icid=0x154A ( 5450)  -> cid=1132 slot=0x154A  Toon Dark Magician Girl
    .hword 0x046D  @ icid=0x154B ( 5451)  -> cid=1133 slot=0x154B  Gilford the Lightning
    .hword 0x046F  @ icid=0x154C ( 5452)  -> cid=1135 slot=0x154C  Exarion Universe
    .hword 0x0470  @ icid=0x154D ( 5453)  -> cid=1136 slot=0x154D  Legendary Fiend
    .hword 0x0826  @ icid=0x154E ( 5454)  -> cid=2086 slot=0x154E
    .hword 0xFFFF  @ icid=0x154F ( 5455)  -> (none)
    .hword 0xFFFF  @ icid=0x1550 ( 5456)  -> (none)
    .hword 0xFFFF  @ icid=0x1551 ( 5457)  -> (none)
    .hword 0xFFFF  @ icid=0x1552 ( 5458)  -> (none)
    .hword 0xFFFF  @ icid=0x1553 ( 5459)  -> (none)
    .hword 0xFFFF  @ icid=0x1554 ( 5460)  -> (none)
    .hword 0xFFFF  @ icid=0x1555 ( 5461)  -> (none)
    .hword 0xFFFF  @ icid=0x1556 ( 5462)  -> (none)
    .hword 0xFFFF  @ icid=0x1557 ( 5463)  -> (none)
    .hword 0xFFFF  @ icid=0x1558 ( 5464)  -> (none)
    .hword 0xFFFF  @ icid=0x1559 ( 5465)  -> (none)
    .hword 0xFFFF  @ icid=0x155A ( 5466)  -> (none)
    .hword 0xFFFF  @ icid=0x155B ( 5467)  -> (none)
    .hword 0xFFFF  @ icid=0x155C ( 5468)  -> (none)
    .hword 0xFFFF  @ icid=0x155D ( 5469)  -> (none)
    .hword 0xFFFF  @ icid=0x155E ( 5470)  -> (none)
    .hword 0xFFFF  @ icid=0x155F ( 5471)  -> (none)
    .hword 0xFFFF  @ icid=0x1560 ( 5472)  -> (none)
    .hword 0x0471  @ icid=0x1561 ( 5473)  -> cid=1137 slot=0x1561  Toon Defense
    .hword 0x0472  @ icid=0x1562 ( 5474)  -> cid=1138 slot=0x1562  Toon Table of Contents
    .hword 0x0473  @ icid=0x1563 ( 5475)  -> cid=1139 slot=0x1563  Toon Masked Sorcerer
    .hword 0x0474  @ icid=0x1564 ( 5476)  -> cid=1140 slot=0x1564  Toon Gemini Elf
    .hword 0x0475  @ icid=0x1565 ( 5477)  -> cid=1141 slot=0x1565  Toon Cannon Soldier
    .hword 0x0476  @ icid=0x1566 ( 5478)  -> cid=1142 slot=0x1566  Toon Goblin Attack Force
    .hword 0x0477  @ icid=0x1567 ( 5479)  -> cid=1143 slot=0x1567  Card of Sanctity
    .hword 0xFFFF  @ icid=0x1568 ( 5480)  -> (none)
    .hword 0xFFFF  @ icid=0x1569 ( 5481)  -> (none)
    .hword 0x0478  @ icid=0x156A ( 5482)  -> cid=1144 slot=0x156A  Puppet Master
    .hword 0xFFFF  @ icid=0x156B ( 5483)  -> (none)
    .hword 0x0479  @ icid=0x156C ( 5484)  -> cid=1145 slot=0x156C  Newdoria
    .hword 0x047A  @ icid=0x156D ( 5485)  -> cid=1146 slot=0x156D  Lord Poison
    .hword 0xFFFF  @ icid=0x156E ( 5486)  -> (none)
    .hword 0xFFFF  @ icid=0x156F ( 5487)  -> (none)
    .hword 0x047B  @ icid=0x1570 ( 5488)  -> cid=1147 slot=0x1570  Blade Knight
    .hword 0x047C  @ icid=0x1571 ( 5489)  -> cid=1148 slot=0x1571  Helpoemer
    .hword 0x047D  @ icid=0x1572 ( 5490)  -> cid=1149 slot=0x1572  Hidden Soldier
    .hword 0x047E  @ icid=0x1573 ( 5491)  -> cid=1150 slot=0x1573  Gil Garth
    .hword 0xFFFF  @ icid=0x1574 ( 5492)  -> (none)
    .hword 0x047F  @ icid=0x1575 ( 5493)  -> cid=1151 slot=0x1575  Calamity of the Wicked
    .hword 0xFFFF  @ icid=0x1576 ( 5494)  -> (none)
    .hword 0xFFFF  @ icid=0x1577 ( 5495)  -> (none)
    .hword 0x0480  @ icid=0x1578 ( 5496)  -> cid=1152 slot=0x1578  Lava Golem
    .hword 0x0481  @ icid=0x1579 ( 5497)  -> cid=1153 slot=0x1579  Monster Relief
    .hword 0x0482  @ icid=0x157A ( 5498)  -> cid=1154 slot=0x157A  Machine Duplication
    .hword 0x0483  @ icid=0x157B ( 5499)  -> cid=1155 slot=0x157B  Dark Jeroid
    .hword 0xFFFF  @ icid=0x157C ( 5500)  -> (none)
    .hword 0x0484  @ icid=0x157D ( 5501)  -> cid=1156 slot=0x157D  Master of Dragon Soldier
    .hword 0x0485  @ icid=0x157E ( 5502)  -> cid=1157 slot=0x157E  F.G.D.
    .hword 0x0486  @ icid=0x157F ( 5503)  -> cid=1158 slot=0x157F  Queen's Knight
    .hword 0x0487  @ icid=0x1580 ( 5504)  -> cid=1159 slot=0x1580  X-Head Cannon
    .hword 0x0488  @ icid=0x1581 ( 5505)  -> cid=1160 slot=0x1581  Enemy Controller
    .hword 0x0489  @ icid=0x1582 ( 5506)  -> cid=1161 slot=0x1582  Master Kyonshee
    .hword 0x048A  @ icid=0x1583 ( 5507)  -> cid=1162 slot=0x1583  Kabazauls
    .hword 0x048B  @ icid=0x1584 ( 5508)  -> cid=1163 slot=0x1584  Inpachi
    .hword 0x048C  @ icid=0x1585 ( 5509)  -> cid=1164 slot=0x1585  Gravekeeper's Spy
    .hword 0x048D  @ icid=0x1586 ( 5510)  -> cid=1165 slot=0x1586  Gravekeeper's Curse
    .hword 0x048E  @ icid=0x1587 ( 5511)  -> cid=1166 slot=0x1587  Gravekeeper's Guard
    .hword 0x048F  @ icid=0x1588 ( 5512)  -> cid=1167 slot=0x1588  Gravekeeper's Spear Soldier
    .hword 0xFFFF  @ icid=0x1589 ( 5513)  -> (none)
    .hword 0xFFFF  @ icid=0x158A ( 5514)  -> (none)
    .hword 0xFFFF  @ icid=0x158B ( 5515)  -> (none)
    .hword 0x0490  @ icid=0x158C ( 5516)  -> cid=1168 slot=0x158C  Gravekeeper's Cannonholder
    .hword 0x0491  @ icid=0x158D ( 5517)  -> cid=1169 slot=0x158D  Gravekeeper's Assailant
    .hword 0x0492  @ icid=0x158E ( 5518)  -> cid=1170 slot=0x158E  A Man with Wdjat
    .hword 0x0493  @ icid=0x158F ( 5519)  -> cid=1171 slot=0x158F  Mystical Knight of Jackal
    .hword 0x0494  @ icid=0x1590 ( 5520)  -> cid=1172 slot=0x1590  A Cat of Ill Omen
    .hword 0x0495  @ icid=0x1591 ( 5521)  -> cid=1173 slot=0x1591  Yomi Ship
    .hword 0x0496  @ icid=0x1592 ( 5522)  -> cid=1174 slot=0x1592  Winged Sage Falcos
    .hword 0x0497  @ icid=0x1593 ( 5523)  -> cid=1175 slot=0x1593  An Owl of Luck
    .hword 0x0498  @ icid=0x1594 ( 5524)  -> cid=1176 slot=0x1594  Charm of Shabti
    .hword 0x0499  @ icid=0x1595 ( 5525)  -> cid=1177 slot=0x1595  Cobra Jar
    .hword 0x049A  @ icid=0x1596 ( 5526)  -> cid=1178 slot=0x1596  Spirit Reaper
    .hword 0x049B  @ icid=0x1597 ( 5527)  -> cid=1179 slot=0x1597  Nightmare Horse
    .hword 0x049C  @ icid=0x1598 ( 5528)  -> cid=1180 slot=0x1598  Reaper on the Nightmare
    .hword 0x049D  @ icid=0x1599 ( 5529)  -> cid=1181 slot=0x1599  Card Shuffle
    .hword 0x049E  @ icid=0x159A ( 5530)  -> cid=1182 slot=0x159A  Reasoning
    .hword 0x049F  @ icid=0x159B ( 5531)  -> cid=1183 slot=0x159B  Dark Room of Nightmare
    .hword 0x04A0  @ icid=0x159C ( 5532)  -> cid=1184 slot=0x159C  Different Dimension Capsule
    .hword 0x04A1  @ icid=0x159D ( 5533)  -> cid=1185 slot=0x159D  Necrovalley
    .hword 0x04A2  @ icid=0x159E ( 5534)  -> cid=1186 slot=0x159E  Buster Rancher
    .hword 0x04A3  @ icid=0x159F ( 5535)  -> cid=1187 slot=0x159F  Hieroglyph Lithograph
    .hword 0x04A4  @ icid=0x15A0 ( 5536)  -> cid=1188 slot=0x15A0  Dark Snake Syndrome
    .hword 0x04A5  @ icid=0x15A1 ( 5537)  -> cid=1189 slot=0x15A1  Terraforming
    .hword 0x04A6  @ icid=0x15A2 ( 5538)  -> cid=1190 slot=0x15A2  Banner of Courage
    .hword 0x04A7  @ icid=0x15A3 ( 5539)  -> cid=1191 slot=0x15A3  Metamorphosis
    .hword 0x04A8  @ icid=0x15A4 ( 5540)  -> cid=1192 slot=0x15A4  Royal Tribute
    .hword 0x04A9  @ icid=0x15A5 ( 5541)  -> cid=1193 slot=0x15A5  Reversal Quiz
    .hword 0x04AA  @ icid=0x15A6 ( 5542)  -> cid=1194 slot=0x15A6  Curse of Aging
    .hword 0xFFFF  @ icid=0x15A7 ( 5543)  -> (none)
    .hword 0x04AB  @ icid=0x15A8 ( 5544)  -> cid=1195 slot=0x15A8  Raigeki Break
    .hword 0xFFFF  @ icid=0x15A9 ( 5545)  -> (none)
    .hword 0x04AC  @ icid=0x15AA ( 5546)  -> cid=1196 slot=0x15AA  Disturbance Strategy
    .hword 0xFFFF  @ icid=0x15AB ( 5547)  -> (none)
    .hword 0x04AD  @ icid=0x15AC ( 5548)  -> cid=1197 slot=0x15AC  Rite of Spirit
    .hword 0x04AE  @ icid=0x15AD ( 5549)  -> cid=1198 slot=0x15AD  Non Aggression Area
    .hword 0x04AF  @ icid=0x15AE ( 5550)  -> cid=1199 slot=0x15AE  D. Tribe
    .hword 0xFFFF  @ icid=0x15AF ( 5551)  -> (none)
    .hword 0x04B0  @ icid=0x15B0 ( 5552)  -> cid=1200 slot=0x15B0  Y-Dragon Head
    .hword 0x04B1  @ icid=0x15B1 ( 5553)  -> cid=1201 slot=0x15B1  XY-Dragon Cannon
    .hword 0xFFFF  @ icid=0x15B2 ( 5554)  -> (none)
    .hword 0x04B2  @ icid=0x15B3 ( 5555)  -> cid=1202 slot=0x15B3  Z-Metal Tank
    .hword 0x04B3  @ icid=0x15B4 ( 5556)  -> cid=1203 slot=0x15B4  XYZ-Dragon Cannon
    .hword 0x04B6  @ icid=0x15B5 ( 5557)  -> cid=1206 slot=0x15B5  Rope of Spirit
    .hword 0x04B7  @ icid=0x15B6 ( 5558)  -> cid=1207 slot=0x15B6  King's Knight
    .hword 0x04B8  @ icid=0x15B7 ( 5559)  -> cid=1208 slot=0x15B7  Jack's Knight
    .hword 0x04B9  @ icid=0x15B8 ( 5560)  -> cid=1209 slot=0x15B8  Interdimensional Matter Transporter
    .hword 0x04BA  @ icid=0x15B9 ( 5561)  -> cid=1210 slot=0x15B9  Goblin Zombie
    .hword 0x04BB  @ icid=0x15BA ( 5562)  -> cid=1211 slot=0x15BA  Drillago
    .hword 0xFFFF  @ icid=0x15BB ( 5563)  -> (none)
    .hword 0x04BC  @ icid=0x15BC ( 5564)  -> cid=1212 slot=0x15BC  Lekunga
    .hword 0x0827  @ icid=0x15BD ( 5565)  -> cid=2087 slot=0x15BD
    .hword 0x0828  @ icid=0x15BE ( 5566)  -> cid=2088 slot=0x15BE
    .hword 0xFFFF  @ icid=0x15BF ( 5567)  -> (none)
    .hword 0xFFFF  @ icid=0x15C0 ( 5568)  -> (none)
    .hword 0xFFFF  @ icid=0x15C1 ( 5569)  -> (none)
    .hword 0xFFFF  @ icid=0x15C2 ( 5570)  -> (none)
    .hword 0xFFFF  @ icid=0x15C3 ( 5571)  -> (none)
    .hword 0xFFFF  @ icid=0x15C4 ( 5572)  -> (none)
    .hword 0xFFFF  @ icid=0x15C5 ( 5573)  -> (none)
    .hword 0xFFFF  @ icid=0x15C6 ( 5574)  -> (none)
    .hword 0x04BD  @ icid=0x15C7 ( 5575)  -> cid=1213 slot=0x15C7  Cost Down
    .hword 0xFFFF  @ icid=0x15C8 ( 5576)  -> (none)
    .hword 0xFFFF  @ icid=0x15C9 ( 5577)  -> (none)
    .hword 0x04BE  @ icid=0x15CA ( 5578)  -> cid=1214 slot=0x15CA  People Running About
    .hword 0x04BF  @ icid=0x15CB ( 5579)  -> cid=1215 slot=0x15CB  Oppressed People
    .hword 0x04C0  @ icid=0x15CC ( 5580)  -> cid=1216 slot=0x15CC  United Resistance
    .hword 0x04C1  @ icid=0x15CD ( 5581)  -> cid=1217 slot=0x15CD  Dark Blade
    .hword 0x04C2  @ icid=0x15CE ( 5582)  -> cid=1218 slot=0x15CE  Pitch-Dark Dragon
    .hword 0x04C3  @ icid=0x15CF ( 5583)  -> cid=1219 slot=0x15CF  Kiryu
    .hword 0x04C4  @ icid=0x15D0 ( 5584)  -> cid=1220 slot=0x15D0  Decayed Commander
    .hword 0x04C5  @ icid=0x15D1 ( 5585)  -> cid=1221 slot=0x15D1  Zombie Tiger
    .hword 0x04C6  @ icid=0x15D2 ( 5586)  -> cid=1222 slot=0x15D2  Giant Orc
    .hword 0x04C7  @ icid=0x15D3 ( 5587)  -> cid=1223 slot=0x15D3  Second Goblin
    .hword 0x04C8  @ icid=0x15D4 ( 5588)  -> cid=1224 slot=0x15D4  Vampire Orchis
    .hword 0x04C9  @ icid=0x15D5 ( 5589)  -> cid=1225 slot=0x15D5  Des Dendle
    .hword 0x04CA  @ icid=0x15D6 ( 5590)  -> cid=1226 slot=0x15D6  Burning Beast
    .hword 0x04CB  @ icid=0x15D7 ( 5591)  -> cid=1227 slot=0x15D7  Freezing Beast
    .hword 0xFFFF  @ icid=0x15D8 ( 5592)  -> (none)
    .hword 0x04CC  @ icid=0x15D9 ( 5593)  -> cid=1228 slot=0x15D9  D.D. Crazy Beast
    .hword 0x04CD  @ icid=0x15DA ( 5594)  -> cid=1229 slot=0x15DA  Spell Canceller
    .hword 0xFFFF  @ icid=0x15DB ( 5595)  -> (none)
    .hword 0x04CE  @ icid=0x15DC ( 5596)  -> cid=1230 slot=0x15DC  Helping Robo For Combat
    .hword 0x04CF  @ icid=0x15DD ( 5597)  -> cid=1231 slot=0x15DD  Dimension Jar
    .hword 0xFFFF  @ icid=0x15DE ( 5598)  -> (none)
    .hword 0x04D0  @ icid=0x15DF ( 5599)  -> cid=1232 slot=0x15DF  Roulette Barrel
    .hword 0x04D1  @ icid=0x15E0 ( 5600)  -> cid=1233 slot=0x15E0  Paladin of White Dragon
    .hword 0x04D2  @ icid=0x15E1 ( 5601)  -> cid=1234 slot=0x15E1  White Dragon Ritual
    .hword 0x04D3  @ icid=0x15E2 ( 5602)  -> cid=1235 slot=0x15E2  Frontline Base
    .hword 0x04D4  @ icid=0x15E3 ( 5603)  -> cid=1236 slot=0x15E3  Demotion
    .hword 0x04D5  @ icid=0x15E4 ( 5604)  -> cid=1237 slot=0x15E4  Combination Attack
    .hword 0xFFFF  @ icid=0x15E5 ( 5605)  -> (none)
    .hword 0x04D6  @ icid=0x15E6 ( 5606)  -> cid=1238 slot=0x15E6  Autonomous Action Unit
    .hword 0x04D7  @ icid=0x15E7 ( 5607)  -> cid=1239 slot=0x15E7  Poison of the Old Man
    .hword 0xFFFF  @ icid=0x15E8 ( 5608)  -> (none)
    .hword 0x04D8  @ icid=0x15E9 ( 5609)  -> cid=1240 slot=0x15E9  Dark Core
    .hword 0x04D9  @ icid=0x15EA ( 5610)  -> cid=1241 slot=0x15EA  Raregold Armor
    .hword 0xFFFF  @ icid=0x15EB ( 5611)  -> (none)
    .hword 0x04DA  @ icid=0x15EC ( 5612)  -> cid=1242 slot=0x15EC  Kishido Spirit
    .hword 0x04DB  @ icid=0x15ED ( 5613)  -> cid=1243 slot=0x15ED  Tribute Doll
    .hword 0x04DC  @ icid=0x15EE ( 5614)  -> cid=1244 slot=0x15EE  Wave-Motion Cannon
    .hword 0x04DD  @ icid=0x15EF ( 5615)  -> cid=1245 slot=0x15EF  Huge Revolution
    .hword 0x04DE  @ icid=0x15F0 ( 5616)  -> cid=1246 slot=0x15F0  Thunder of Ruler
    .hword 0x04DF  @ icid=0x15F1 ( 5617)  -> cid=1247 slot=0x15F1  Spell Shield Type-8
    .hword 0x04E0  @ icid=0x15F2 ( 5618)  -> cid=1248 slot=0x15F2  Meteorain
    .hword 0x04E1  @ icid=0x15F3 ( 5619)  -> cid=1249 slot=0x15F3  Pineapple Blast
    .hword 0x04E2  @ icid=0x15F4 ( 5620)  -> cid=1250 slot=0x15F4  Secret Barrel
    .hword 0xFFFF  @ icid=0x15F5 ( 5621)  -> (none)
    .hword 0xFFFF  @ icid=0x15F6 ( 5622)  -> (none)
    .hword 0x04E3  @ icid=0x15F7 ( 5623)  -> cid=1251 slot=0x15F7  Formation Union
    .hword 0x04E4  @ icid=0x15F8 ( 5624)  -> cid=1252 slot=0x15F8  Adhesion Trap Hole
    .hword 0x04E5  @ icid=0x15F9 ( 5625)  -> cid=1253 slot=0x15F9  XZ-Tank Cannon
    .hword 0x04E6  @ icid=0x15FA ( 5626)  -> cid=1254 slot=0x15FA  YZ-Tank Dragon
    .hword 0x04E7  @ icid=0x15FB ( 5627)  -> cid=1255 slot=0x15FB  Final Attack Orders
    .hword 0x04E8  @ icid=0x15FC ( 5628)  -> cid=1256 slot=0x15FC  Dark Paladin
    .hword 0xFFFF  @ icid=0x15FD ( 5629)  -> (none)
    .hword 0x04EB  @ icid=0x15FE ( 5630)  -> cid=1259 slot=0x15FE  Spell Absorption
    .hword 0x04EC  @ icid=0x15FF ( 5631)  -> cid=1260 slot=0x15FF  Diffusion Wave-Motion
    .hword 0x04ED  @ icid=0x1600 ( 5632)  -> cid=1261 slot=0x1600  Fiend's Sanctuary
    .hword 0xFFFF  @ icid=0x1601 ( 5633)  -> (none)
    .hword 0xFFFF  @ icid=0x1602 ( 5634)  -> (none)
    .hword 0x0829  @ icid=0x1603 ( 5635)  -> cid=2089 slot=0x1603
    .hword 0xFFFF  @ icid=0x1604 ( 5636)  -> (none)
    .hword 0xFFFF  @ icid=0x1605 ( 5637)  -> (none)
    .hword 0xFFFF  @ icid=0x1606 ( 5638)  -> (none)
    .hword 0xFFFF  @ icid=0x1607 ( 5639)  -> (none)
    .hword 0xFFFF  @ icid=0x1608 ( 5640)  -> (none)
    .hword 0x04EE  @ icid=0x1609 ( 5641)  -> cid=1262 slot=0x1609  Great Angus
    .hword 0x04EF  @ icid=0x160A ( 5642)  -> cid=1263 slot=0x160A  Aitsu
    .hword 0x04F0  @ icid=0x160B ( 5643)  -> cid=1264 slot=0x160B  Sonic Duck
    .hword 0x04F1  @ icid=0x160C ( 5644)  -> cid=1265 slot=0x160C  Luster Dragon
    .hword 0x04F2  @ icid=0x160D ( 5645)  -> cid=1266 slot=0x160D  Amazoness Paladin
    .hword 0x04F3  @ icid=0x160E ( 5646)  -> cid=1267 slot=0x160E  Amazoness Blowpiper
    .hword 0x04F4  @ icid=0x160F ( 5647)  -> cid=1268 slot=0x160F  Amazoness Tiger
    .hword 0x04F5  @ icid=0x1610 ( 5648)  -> cid=1269 slot=0x1610  Skilled White Magician
    .hword 0x04F6  @ icid=0x1611 ( 5649)  -> cid=1270 slot=0x1611  Skilled Dark Magician
    .hword 0x04F7  @ icid=0x1612 ( 5650)  -> cid=1271 slot=0x1612  Apprentice Magician
    .hword 0x04F8  @ icid=0x1613 ( 5651)  -> cid=1272 slot=0x1613  Old Vindictive Magician
    .hword 0x04F9  @ icid=0x1614 ( 5652)  -> cid=1273 slot=0x1614  Chaos Command Magician
    .hword 0x04FA  @ icid=0x1615 ( 5653)  -> cid=1274 slot=0x1615  Magical Marionette
    .hword 0xFFFF  @ icid=0x1616 ( 5654)  -> (none)
    .hword 0x04FB  @ icid=0x1617 ( 5655)  -> cid=1275 slot=0x1617  Breaker the Magical Warrior
    .hword 0x04FC  @ icid=0x1618 ( 5656)  -> cid=1276 slot=0x1618  Magical Plant Mandragola
    .hword 0x04FD  @ icid=0x1619 ( 5657)  -> cid=1277 slot=0x1619  Magical Scientist
    .hword 0x04FE  @ icid=0x161A ( 5658)  -> cid=1278 slot=0x161A  Royal Magical Library
    .hword 0x04FF  @ icid=0x161B ( 5659)  -> cid=1279 slot=0x161B  Armor Exe
    .hword 0x0500  @ icid=0x161C ( 5660)  -> cid=1280 slot=0x161C  Tribe-Infecting Virus
    .hword 0x0501  @ icid=0x161D ( 5661)  -> cid=1281 slot=0x161D  Des Koala
    .hword 0x0502  @ icid=0x161E ( 5662)  -> cid=1282 slot=0x161E  Cliff the Trap Remover
    .hword 0x0503  @ icid=0x161F ( 5663)  -> cid=1283 slot=0x161F  Magical Merchant
    .hword 0x0504  @ icid=0x1620 ( 5664)  -> cid=1284 slot=0x1620  Koitsu
    .hword 0x0505  @ icid=0x1621 ( 5665)  -> cid=1285 slot=0x1621  Cat's Ear Tribe
    .hword 0x0506  @ icid=0x1622 ( 5666)  -> cid=1286 slot=0x1622  Ultimate Obedient Fiend
    .hword 0xFFFF  @ icid=0x1623 ( 5667)  -> (none)
    .hword 0x0507  @ icid=0x1624 ( 5668)  -> cid=1287 slot=0x1624  Pitch-Black Power Stone
    .hword 0x0508  @ icid=0x1625 ( 5669)  -> cid=1288 slot=0x1625  Big Bang Shot
    .hword 0x0509  @ icid=0x1626 ( 5670)  -> cid=1289 slot=0x1626  Gather Your Mind
    .hword 0x050A  @ icid=0x1627 ( 5671)  -> cid=1290 slot=0x1627  Mass Driver
    .hword 0x050B  @ icid=0x1628 ( 5672)  -> cid=1291 slot=0x1628  Senri Eye
    .hword 0x050C  @ icid=0x1629 ( 5673)  -> cid=1292 slot=0x1629  Emblem of Dragon Destroyer
    .hword 0x050D  @ icid=0x162A ( 5674)  -> cid=1293 slot=0x162A  Jar Robber
    .hword 0xFFFF  @ icid=0x162B ( 5675)  -> (none)
    .hword 0xFFFF  @ icid=0x162C ( 5676)  -> (none)
    .hword 0x050E  @ icid=0x162D ( 5677)  -> cid=1294 slot=0x162D  Mega Ton Magical Cannon
    .hword 0x050F  @ icid=0x162E ( 5678)  -> cid=1295 slot=0x162E  Continuous Destruction Punch
    .hword 0x0510  @ icid=0x162F ( 5679)  -> cid=1296 slot=0x162F  Exhausting Spell
    .hword 0x0511  @ icid=0x1630 ( 5680)  -> cid=1297 slot=0x1630  Hidden Book of Spell
    .hword 0x0512  @ icid=0x1631 ( 5681)  -> cid=1298 slot=0x1631  Miracle Restoring
    .hword 0xFFFF  @ icid=0x1632 ( 5682)  -> (none)
    .hword 0x0513  @ icid=0x1633 ( 5683)  -> cid=1299 slot=0x1633  Disarmament
    .hword 0x0514  @ icid=0x1634 ( 5684)  -> cid=1300 slot=0x1634  Anti-Spell
    .hword 0x0515  @ icid=0x1635 ( 5685)  -> cid=1301 slot=0x1635  The Spell Absorbing Life
    .hword 0x0516  @ icid=0x1636 ( 5686)  -> cid=1302 slot=0x1636  Metal Reflect Slime
    .hword 0x0517  @ icid=0x1637 ( 5687)  -> cid=1303 slot=0x1637  Bowganian
    .hword 0x0518  @ icid=0x1638 ( 5688)  -> cid=1304 slot=0x1638  Excavation of Mage Stones
    .hword 0x082A  @ icid=0x1639 ( 5689)  -> cid=2090 slot=0x1639
    .hword 0xFFFF  @ icid=0x163A ( 5690)  -> (none)
    .hword 0xFFFF  @ icid=0x163B ( 5691)  -> (none)
    .hword 0xFFFF  @ icid=0x163C ( 5692)  -> (none)
    .hword 0xFFFF  @ icid=0x163D ( 5693)  -> (none)
    .hword 0xFFFF  @ icid=0x163E ( 5694)  -> (none)
    .hword 0x0519  @ icid=0x163F ( 5695)  -> cid=1305 slot=0x163F  Granadora
    .hword 0xFFFF  @ icid=0x1640 ( 5696)  -> (none)
    .hword 0x051A  @ icid=0x1641 ( 5697)  -> cid=1306 slot=0x1641  Shinato, King of a Higher Plane
    .hword 0x051B  @ icid=0x1642 ( 5698)  -> cid=1307 slot=0x1642  Dark Flare Knight
    .hword 0x051C  @ icid=0x1643 ( 5699)  -> cid=1308 slot=0x1643  Mirage Knight
    .hword 0x051D  @ icid=0x1644 ( 5700)  -> cid=1309 slot=0x1644  Berserk Dragon
    .hword 0x051E  @ icid=0x1645 ( 5701)  -> cid=1310 slot=0x1645  Exodia Necross
    .hword 0x051F  @ icid=0x1646 ( 5702)  -> cid=1311 slot=0x1646  Battle Footballer
    .hword 0x0520  @ icid=0x1647 ( 5703)  -> cid=1312 slot=0x1647  Arsenal Summoner
    .hword 0x0521  @ icid=0x1648 ( 5704)  -> cid=1313 slot=0x1648  Nin-Ken Dog
    .hword 0x0522  @ icid=0x1649 ( 5705)  -> cid=1314 slot=0x1649  Acrobat Monkey
    .hword 0x0523  @ icid=0x164A ( 5706)  -> cid=1315 slot=0x164A  Guardian Elma
    .hword 0x0524  @ icid=0x164B ( 5707)  -> cid=1316 slot=0x164B  Guardian Ceal
    .hword 0x0525  @ icid=0x164C ( 5708)  -> cid=1317 slot=0x164C  Guardian Grarl
    .hword 0x0526  @ icid=0x164D ( 5709)  -> cid=1318 slot=0x164D  Guardian Baou
    .hword 0x0527  @ icid=0x164E ( 5710)  -> cid=1319 slot=0x164E  Guardian Kay'est
    .hword 0x0528  @ icid=0x164F ( 5711)  -> cid=1320 slot=0x164F  Guardian Tryce
    .hword 0xFFFF  @ icid=0x1650 ( 5712)  -> (none)
    .hword 0x0529  @ icid=0x1651 ( 5713)  -> cid=1321 slot=0x1651  Gyaku-Gire Panda
    .hword 0x052A  @ icid=0x1652 ( 5714)  -> cid=1322 slot=0x1652  Blindly Loyal Goblin
    .hword 0x052B  @ icid=0x1653 ( 5715)  -> cid=1323 slot=0x1653  Despair from the Dark
    .hword 0x052C  @ icid=0x1654 ( 5716)  -> cid=1324 slot=0x1654  Maju Garzett
    .hword 0x052D  @ icid=0x1655 ( 5717)  -> cid=1325 slot=0x1655  Fear from the Dark
    .hword 0x052E  @ icid=0x1656 ( 5718)  -> cid=1326 slot=0x1656  Dark Scorpion - Chick the Yellow
    .hword 0x052F  @ icid=0x1657 ( 5719)  -> cid=1327 slot=0x1657  D.D. Warrior Lady
    .hword 0x0530  @ icid=0x1658 ( 5720)  -> cid=1328 slot=0x1658  Thousand Needles
    .hword 0x0531  @ icid=0x1659 ( 5721)  -> cid=1329 slot=0x1659  Shinato's Ark
    .hword 0x0532  @ icid=0x165A ( 5722)  -> cid=1330 slot=0x165A  A Deal with Dark Ruler
    .hword 0x0533  @ icid=0x165B ( 5723)  -> cid=1331 slot=0x165B  Contract with Exodia
    .hword 0x0534  @ icid=0x165C ( 5724)  -> cid=1332 slot=0x165C  Butterfly Dagger - Elma
    .hword 0x0535  @ icid=0x165D ( 5725)  -> cid=1333 slot=0x165D  Shooting Star Bow - Ceal
    .hword 0x0536  @ icid=0x165E ( 5726)  -> cid=1334 slot=0x165E  Gravity Axe - Grarl
    .hword 0x0537  @ icid=0x165F ( 5727)  -> cid=1335 slot=0x165F  Wicked-Breaking Flamberge - Baou
    .hword 0x0538  @ icid=0x1660 ( 5728)  -> cid=1336 slot=0x1660  Rod of Silence - Kay'est
    .hword 0x0539  @ icid=0x1661 ( 5729)  -> cid=1337 slot=0x1661  Twin Swords of Flashing Light - Tryce
    .hword 0x053A  @ icid=0x1662 ( 5730)  -> cid=1338 slot=0x1662  Precious Cards from Beyond
    .hword 0x053B  @ icid=0x1663 ( 5731)  -> cid=1339 slot=0x1663  Rod of the Mind's Eye
    .hword 0x053C  @ icid=0x1664 ( 5732)  -> cid=1340 slot=0x1664  Fairy of the Spring
    .hword 0x053D  @ icid=0x1665 ( 5733)  -> cid=1341 slot=0x1665  Token Thanksgiving
    .hword 0xFFFF  @ icid=0x1666 ( 5734)  -> (none)
    .hword 0x053E  @ icid=0x1667 ( 5735)  -> cid=1342 slot=0x1667  Non-Spellcasting Area
    .hword 0xFFFF  @ icid=0x1668 ( 5736)  -> (none)
    .hword 0x053F  @ icid=0x1669 ( 5737)  -> cid=1343 slot=0x1669  Staunch Defender
    .hword 0x0540  @ icid=0x166A ( 5738)  -> cid=1344 slot=0x166A  Ojama Trio
    .hword 0x0541  @ icid=0x166B ( 5739)  -> cid=1345 slot=0x166B  Arsenal Robber
    .hword 0x0542  @ icid=0x166C ( 5740)  -> cid=1346 slot=0x166C  Skill Drain
    .hword 0x0543  @ icid=0x166D ( 5741)  -> cid=1347 slot=0x166D  Really Eternal Rest
    .hword 0xFFFF  @ icid=0x166E ( 5742)  -> (none)
    .hword 0x0544  @ icid=0x166F ( 5743)  -> cid=1348 slot=0x166F  Soul Taker
    .hword 0x082B  @ icid=0x1670 ( 5744)  -> cid=2091 slot=0x1670
    .hword 0xFFFF  @ icid=0x1671 ( 5745)  -> (none)
    .hword 0xFFFF  @ icid=0x1672 ( 5746)  -> (none)
    .hword 0xFFFF  @ icid=0x1673 ( 5747)  -> (none)
    .hword 0xFFFF  @ icid=0x1674 ( 5748)  -> (none)
    .hword 0xFFFF  @ icid=0x1675 ( 5749)  -> (none)
    .hword 0xFFFF  @ icid=0x1676 ( 5750)  -> (none)
    .hword 0xFFFF  @ icid=0x1677 ( 5751)  -> (none)
    .hword 0x0545  @ icid=0x1678 ( 5752)  -> cid=1349 slot=0x1678  Magical Dimension
    .hword 0x0546  @ icid=0x1679 ( 5753)  -> cid=1350 slot=0x1679  Judgement of Pharaoh
    .hword 0x0547  @ icid=0x167A ( 5754)  -> cid=1351 slot=0x167A  Friendship
    .hword 0x0548  @ icid=0x167B ( 5755)  -> cid=1352 slot=0x167B  Unity
    .hword 0x0549  @ icid=0x167C ( 5756)  -> cid=1353 slot=0x167C  Dark Magician Knight
    .hword 0x054A  @ icid=0x167D ( 5757)  -> cid=1354 slot=0x167D  Knight's Title
    .hword 0x054B  @ icid=0x167E ( 5758)  -> cid=1355 slot=0x167E  Sage's Stone
    .hword 0x054C  @ icid=0x167F ( 5759)  -> cid=1356 slot=0x167F  Gagagigo
    .hword 0x054D  @ icid=0x1680 ( 5760)  -> cid=1357 slot=0x1680  D. D. Trainer
    .hword 0x054E  @ icid=0x1681 ( 5761)  -> cid=1358 slot=0x1681  Ojama Green
    .hword 0x054F  @ icid=0x1682 ( 5762)  -> cid=1359 slot=0x1682  Archfiend Soldier
    .hword 0x0550  @ icid=0x1683 ( 5763)  -> cid=1360 slot=0x1683  Pandemonium Watchbear
    .hword 0x0551  @ icid=0x1684 ( 5764)  -> cid=1361 slot=0x1684  Sasuke Samurai #2
    .hword 0x0552  @ icid=0x1685 ( 5765)  -> cid=1362 slot=0x1685  Dark Scorpion - Gorg the Strong
    .hword 0x0553  @ icid=0x1686 ( 5766)  -> cid=1363 slot=0x1686  Dark Scorpion - Meanae the Thorn
    .hword 0x0554  @ icid=0x1687 ( 5767)  -> cid=1364 slot=0x1687  Outstanding Dog Marron
    .hword 0x0555  @ icid=0x1688 ( 5768)  -> cid=1365 slot=0x1688  Great Maju Garzett
    .hword 0x0556  @ icid=0x1689 ( 5769)  -> cid=1366 slot=0x1689  Iron Blacksmith Kotetsu
    .hword 0xFFFF  @ icid=0x168A ( 5770)  -> (none)
    .hword 0x0557  @ icid=0x168B ( 5771)  -> cid=1367 slot=0x168B  Mefist the Infernal General
    .hword 0x0558  @ icid=0x168C ( 5772)  -> cid=1368 slot=0x168C  Vilepawn Archfiend
    .hword 0x0559  @ icid=0x168D ( 5773)  -> cid=1369 slot=0x168D  Shadowknight Archfiend
    .hword 0x055A  @ icid=0x168E ( 5774)  -> cid=1370 slot=0x168E  Darkbishop Archfiend
    .hword 0x055B  @ icid=0x168F ( 5775)  -> cid=1371 slot=0x168F  Desrook Archfiend
    .hword 0x055C  @ icid=0x1690 ( 5776)  -> cid=1372 slot=0x1690  Infernalqueen Archfiend
    .hword 0x055D  @ icid=0x1691 ( 5777)  -> cid=1373 slot=0x1691  Terrorking Archfiend
    .hword 0x055E  @ icid=0x1692 ( 5778)  -> cid=1374 slot=0x1692  Skull Archfiend of Lightning
    .hword 0x055F  @ icid=0x1693 ( 5779)  -> cid=1375 slot=0x1693  Metallizing Parasite - Lunatite
    .hword 0x0560  @ icid=0x1694 ( 5780)  -> cid=1376 slot=0x1694  Tsukuyomi
    .hword 0x0561  @ icid=0x1695 ( 5781)  -> cid=1377 slot=0x1695  Legendary Flame Lord
    .hword 0x0562  @ icid=0x1696 ( 5782)  -> cid=1378 slot=0x1696  Dark Master - Zorc
    .hword 0x0563  @ icid=0x1697 ( 5783)  -> cid=1379 slot=0x1697  Incandescent Ordeal
    .hword 0x0564  @ icid=0x1698 ( 5784)  -> cid=1380 slot=0x1698  Contract with the Abyss
    .hword 0x0565  @ icid=0x1699 ( 5785)  -> cid=1381 slot=0x1699  Contract with the Dark Master
    .hword 0x0566  @ icid=0x169A ( 5786)  -> cid=1382 slot=0x169A  Falling Down
    .hword 0x0567  @ icid=0x169B ( 5787)  -> cid=1383 slot=0x169B  Checkmate
    .hword 0x0568  @ icid=0x169C ( 5788)  -> cid=1384 slot=0x169C  Final Countdown
    .hword 0xFFFF  @ icid=0x169D ( 5789)  -> (none)
    .hword 0x0569  @ icid=0x169E ( 5790)  -> cid=1385 slot=0x169E  Mustering of the Dark Scorpions
    .hword 0x056A  @ icid=0x169F ( 5791)  -> cid=1386 slot=0x169F  Pandemonium
    .hword 0x056B  @ icid=0x16A0 ( 5792)  -> cid=1387 slot=0x16A0  Altar for Tribute
    .hword 0x056C  @ icid=0x16A1 ( 5793)  -> cid=1388 slot=0x16A1  Frozen Soul
    .hword 0x056D  @ icid=0x16A2 ( 5794)  -> cid=1389 slot=0x16A2  Battle-Scarred
    .hword 0x056E  @ icid=0x16A3 ( 5795)  -> cid=1390 slot=0x16A3  Dark Scorpion Combination
    .hword 0x056F  @ icid=0x16A4 ( 5796)  -> cid=1391 slot=0x16A4  Archfiend's Roar
    .hword 0x0570  @ icid=0x16A5 ( 5797)  -> cid=1392 slot=0x16A5  Dice Re-Roll
    .hword 0x0571  @ icid=0x16A6 ( 5798)  -> cid=1393 slot=0x16A6  Spell Vanishing
    .hword 0x0572  @ icid=0x16A7 ( 5799)  -> cid=1394 slot=0x16A7  Sakuretsu Armor
    .hword 0x0573  @ icid=0x16A8 ( 5800)  -> cid=1395 slot=0x16A8  Ray of Hope
    .hword 0xFFFF  @ icid=0x16A9 ( 5801)  -> (none)
    .hword 0xFFFF  @ icid=0x16AA ( 5802)  -> (none)
    .hword 0x0574  @ icid=0x16AB ( 5803)  -> cid=1396 slot=0x16AB  Nightmare Penguin
    .hword 0x0575  @ icid=0x16AC ( 5804)  -> cid=1397 slot=0x16AC  Perfect Machine King
    .hword 0xFFFF  @ icid=0x16AD ( 5805)  -> (none)
    .hword 0xFFFF  @ icid=0x16AE ( 5806)  -> (none)
    .hword 0xFFFF  @ icid=0x16AF ( 5807)  -> (none)
    .hword 0xFFFF  @ icid=0x16B0 ( 5808)  -> (none)
    .hword 0xFFFF  @ icid=0x16B1 ( 5809)  -> (none)
    .hword 0x0576  @ icid=0x16B2 ( 5810)  -> cid=1398 slot=0x16B2  Chiron the Mage
    .hword 0x0577  @ icid=0x16B3 ( 5811)  -> cid=1399 slot=0x16B3  Ojama Yellow
    .hword 0x0578  @ icid=0x16B4 ( 5812)  -> cid=1400 slot=0x16B4  Ojama Black
    .hword 0x0579  @ icid=0x16B5 ( 5813)  -> cid=1401 slot=0x16B5  Soul Tiger
    .hword 0x057A  @ icid=0x16B6 ( 5814)  -> cid=1402 slot=0x16B6  Big Koala
    .hword 0x057B  @ icid=0x16B7 ( 5815)  -> cid=1403 slot=0x16B7  Des Kangaroo
    .hword 0x057C  @ icid=0x16B8 ( 5816)  -> cid=1404 slot=0x16B8  Crimson Ninja
    .hword 0x057D  @ icid=0x16B9 ( 5817)  -> cid=1405 slot=0x16B9  Strike Ninja
    .hword 0x057E  @ icid=0x16BA ( 5818)  -> cid=1406 slot=0x16BA  Gale Lizard
    .hword 0xFFFF  @ icid=0x16BB ( 5819)  -> (none)
    .hword 0x057F  @ icid=0x16BC ( 5820)  -> cid=1407 slot=0x16BC  Chopman the Desperate Outlaw
    .hword 0x0580  @ icid=0x16BD ( 5821)  -> cid=1408 slot=0x16BD  Sasuke Samurai #3
    .hword 0x0581  @ icid=0x16BE ( 5822)  -> cid=1409 slot=0x16BE  D. D. Scout Plane
    .hword 0x0582  @ icid=0x16BF ( 5823)  -> cid=1410 slot=0x16BF  Berserk Gorilla
    .hword 0x0583  @ icid=0x16C0 ( 5824)  -> cid=1411 slot=0x16C0  Freed the Brave Wanderer
    .hword 0xFFFF  @ icid=0x16C1 ( 5825)  -> (none)
    .hword 0x0584  @ icid=0x16C2 ( 5826)  -> cid=1412 slot=0x16C2  Witch Doctor of Chaos
    .hword 0x0585  @ icid=0x16C3 ( 5827)  -> cid=1413 slot=0x16C3  Chaos Necromancer
    .hword 0x0586  @ icid=0x16C4 ( 5828)  -> cid=1414 slot=0x16C4  Chaosrider Gustaph
    .hword 0x0587  @ icid=0x16C5 ( 5829)  -> cid=1415 slot=0x16C5  Inferno
    .hword 0x0588  @ icid=0x16C6 ( 5830)  -> cid=1416 slot=0x16C6  Fenrir
    .hword 0x0589  @ icid=0x16C7 ( 5831)  -> cid=1417 slot=0x16C7  Gigantes
    .hword 0x058A  @ icid=0x16C8 ( 5832)  -> cid=1418 slot=0x16C8  Silpheed
    .hword 0x058B  @ icid=0x16C9 ( 5833)  -> cid=1419 slot=0x16C9  Chaos Sorcerer
    .hword 0x058C  @ icid=0x16CA ( 5834)  -> cid=1420 slot=0x16CA  Gren Maju Da Eiza
    .hword 0x058D  @ icid=0x16CB ( 5835)  -> cid=1421 slot=0x16CB  Black Luster Soldier - Envoy of the Beginning
    .hword 0x058E  @ icid=0x16CC ( 5836)  -> cid=1422 slot=0x16CC  Fuhma Shuriken
    .hword 0x058F  @ icid=0x16CD ( 5837)  -> cid=1423 slot=0x16CD  Heart of the Underdog
    .hword 0x0590  @ icid=0x16CE ( 5838)  -> cid=1424 slot=0x16CE  Wild Nature's Release
    .hword 0x0591  @ icid=0x16CF ( 5839)  -> cid=1425 slot=0x16CF  Ojama Delta Hurricane!!
    .hword 0x0592  @ icid=0x16D0 ( 5840)  -> cid=1426 slot=0x16D0  Stumbling
    .hword 0x0593  @ icid=0x16D1 ( 5841)  -> cid=1427 slot=0x16D1  Chaos End
    .hword 0x0594  @ icid=0x16D2 ( 5842)  -> cid=1428 slot=0x16D2  Chaos Greed
    .hword 0xFFFF  @ icid=0x16D3 ( 5843)  -> (none)
    .hword 0x0595  @ icid=0x16D4 ( 5844)  -> cid=1429 slot=0x16D4  D. D. Borderline
    .hword 0x0596  @ icid=0x16D5 ( 5845)  -> cid=1430 slot=0x16D5  Recycle
    .hword 0x0597  @ icid=0x16D6 ( 5846)  -> cid=1431 slot=0x16D6  Primal Seed
    .hword 0x0598  @ icid=0x16D7 ( 5847)  -> cid=1432 slot=0x16D7  Thunder Crash
    .hword 0x0599  @ icid=0x16D8 ( 5848)  -> cid=1433 slot=0x16D8  Dimension Distortion
    .hword 0x059A  @ icid=0x16D9 ( 5849)  -> cid=1434 slot=0x16D9  Reload
    .hword 0x059B  @ icid=0x16DA ( 5850)  -> cid=1435 slot=0x16DA  Soul Absorption
    .hword 0x059C  @ icid=0x16DB ( 5851)  -> cid=1436 slot=0x16DB  Big Burn
    .hword 0x059D  @ icid=0x16DC ( 5852)  -> cid=1437 slot=0x16DC  Blasting the Ruins
    .hword 0x059E  @ icid=0x16DD ( 5853)  -> cid=1438 slot=0x16DD  Cursed Seal of the Forbidden Spell
    .hword 0x059F  @ icid=0x16DE ( 5854)  -> cid=1439 slot=0x16DE  Tower of Babel
    .hword 0x05A0  @ icid=0x16DF ( 5855)  -> cid=1440 slot=0x16DF  Spatial Collapse
    .hword 0x05A1  @ icid=0x16E0 ( 5856)  -> cid=1441 slot=0x16E0  Chain Disappearance
    .hword 0x05A2  @ icid=0x16E1 ( 5857)  -> cid=1442 slot=0x16E1  Zero Gravity
    .hword 0x05A3  @ icid=0x16E2 ( 5858)  -> cid=1443 slot=0x16E2  Dark Mirror Force
    .hword 0x05A4  @ icid=0x16E3 ( 5859)  -> cid=1444 slot=0x16E3  Energy Drain
    .hword 0x05A5  @ icid=0x16E4 ( 5860)  -> cid=1445 slot=0x16E4  Chaos Emperor Dragon - Envoy of the End
    .hword 0xFFFF  @ icid=0x16E5 ( 5861)  -> (none)
    .hword 0xFFFF  @ icid=0x16E6 ( 5862)  -> (none)
    .hword 0xFFFF  @ icid=0x16E7 ( 5863)  -> (none)
    .hword 0xFFFF  @ icid=0x16E8 ( 5864)  -> (none)
    .hword 0xFFFF  @ icid=0x16E9 ( 5865)  -> (none)
    .hword 0xFFFF  @ icid=0x16EA ( 5866)  -> (none)
    .hword 0xFFFF  @ icid=0x16EB ( 5867)  -> (none)
    .hword 0x05A6  @ icid=0x16EC ( 5868)  -> cid=1446 slot=0x16EC  Victory D.
    .hword 0x05A7  @ icid=0x16ED ( 5869)  -> cid=1447 slot=0x16ED  Magician's Valkyrie
    .hword 0xFFFF  @ icid=0x16EE ( 5870)  -> (none)
    .hword 0x05A8  @ icid=0x16EF ( 5871)  -> cid=1448 slot=0x16EF  Giga Gagagigo
    .hword 0x05A9  @ icid=0x16F0 ( 5872)  -> cid=1449 slot=0x16F0  Mad Dog of Darkness
    .hword 0x05AA  @ icid=0x16F1 ( 5873)  -> cid=1450 slot=0x16F1  Neo Bug
    .hword 0x05AB  @ icid=0x16F2 ( 5874)  -> cid=1451 slot=0x16F2  Sea Serpent Warrior of Darkness
    .hword 0x05AC  @ icid=0x16F3 ( 5875)  -> cid=1452 slot=0x16F3  Terrorking Salmon
    .hword 0x05AD  @ icid=0x16F4 ( 5876)  -> cid=1453 slot=0x16F4  Blazing Inpachi
    .hword 0x05AE  @ icid=0x16F5 ( 5877)  -> cid=1454 slot=0x16F5  Burning Algae
    .hword 0x05AF  @ icid=0x16F6 ( 5878)  -> cid=1455 slot=0x16F6  The Thing in the Crater
    .hword 0x05B0  @ icid=0x16F7 ( 5879)  -> cid=1456 slot=0x16F7  Molten Zombie
    .hword 0x05B1  @ icid=0x16F8 ( 5880)  -> cid=1457 slot=0x16F8  Dark Magician of Chaos
    .hword 0x05B2  @ icid=0x16F9 ( 5881)  -> cid=1458 slot=0x16F9  Manticore of Darkness
    .hword 0x05B3  @ icid=0x16FA ( 5882)  -> cid=1459 slot=0x16FA  Stealth Bird
    .hword 0x05B4  @ icid=0x16FB ( 5883)  -> cid=1460 slot=0x16FB  Sacred Crane
    .hword 0x05B5  @ icid=0x16FC ( 5884)  -> cid=1461 slot=0x16FC  Enraged Battle Ox
    .hword 0x05B6  @ icid=0x16FD ( 5885)  -> cid=1462 slot=0x16FD  Don Turtle
    .hword 0xFFFF  @ icid=0x16FE ( 5886)  -> (none)
    .hword 0x05B7  @ icid=0x16FF ( 5887)  -> cid=1463 slot=0x16FF  Dark Driceratops
    .hword 0x05B8  @ icid=0x1700 ( 5888)  -> cid=1464 slot=0x1700  Hyper Hammerhead
    .hword 0x05B9  @ icid=0x1701 ( 5889)  -> cid=1465 slot=0x1701  Black Tyranno
    .hword 0x05BA  @ icid=0x1702 ( 5890)  -> cid=1466 slot=0x1702  Anti-Aircraft Flower
    .hword 0x05BB  @ icid=0x1703 ( 5891)  -> cid=1467 slot=0x1703  Prickle Fairy
    .hword 0x05BC  @ icid=0x1704 ( 5892)  -> cid=1468 slot=0x1704  Insect Princess
    .hword 0x05BD  @ icid=0x1705 ( 5893)  -> cid=1469 slot=0x1705  Amphibious Bugroth MK-3
    .hword 0x05BE  @ icid=0x1706 ( 5894)  -> cid=1470 slot=0x1706  Torpedo Fish
    .hword 0x05BF  @ icid=0x1707 ( 5895)  -> cid=1471 slot=0x1707  Levia-Dragon - Daedalus
    .hword 0x05C0  @ icid=0x1708 ( 5896)  -> cid=1472 slot=0x1708  Orca Mega-Fortress of Darkness
    .hword 0x05C1  @ icid=0x1709 ( 5897)  -> cid=1473 slot=0x1709  Cannonball Spear Shellfish
    .hword 0x05C2  @ icid=0x170A ( 5898)  -> cid=1474 slot=0x170A  Mataza the Zapper
    .hword 0x05C3  @ icid=0x170B ( 5899)  -> cid=1475 slot=0x170B  Guardian Angel Joan
    .hword 0x05C4  @ icid=0x170C ( 5900)  -> cid=1476 slot=0x170C  Manju of the Ten Thousand Hands
    .hword 0x05C5  @ icid=0x170D ( 5901)  -> cid=1477 slot=0x170D  Getsu Fuhma
    .hword 0x05C6  @ icid=0x170E ( 5902)  -> cid=1478 slot=0x170E  Ryu Kokki
    .hword 0x05C7  @ icid=0x170F ( 5903)  -> cid=1479 slot=0x170F  Gryphon's Feather Duster
    .hword 0x05C8  @ icid=0x1710 ( 5904)  -> cid=1480 slot=0x1710  Stray Lambs
    .hword 0x05C9  @ icid=0x1711 ( 5905)  -> cid=1481 slot=0x1711  Smashing Ground
    .hword 0x05CA  @ icid=0x1712 ( 5906)  -> cid=1482 slot=0x1712  Dimension Fusion
    .hword 0x05CB  @ icid=0x1713 ( 5907)  -> cid=1483 slot=0x1713  Dedication through Light and Darkness
    .hword 0x05CC  @ icid=0x1714 ( 5908)  -> cid=1484 slot=0x1714  Salvage
    .hword 0x05CD  @ icid=0x1715 ( 5909)  -> cid=1485 slot=0x1715  Ultra Evolution Pill
    .hword 0x05CE  @ icid=0x1716 ( 5910)  -> cid=1486 slot=0x1716  Earth Chant
    .hword 0x05CF  @ icid=0x1717 ( 5911)  -> cid=1487 slot=0x1717  Jade Insect Whistle
    .hword 0x05D0  @ icid=0x1718 ( 5912)  -> cid=1488 slot=0x1718  Destruction Ring
    .hword 0x05D1  @ icid=0x1719 ( 5913)  -> cid=1489 slot=0x1719  Fiend's Hand Mirror
    .hword 0x05D2  @ icid=0x171A ( 5914)  -> cid=1490 slot=0x171A  Compulsory Evacuation Device
    .hword 0x05D3  @ icid=0x171B ( 5915)  -> cid=1491 slot=0x171B  A Hero Emerges
    .hword 0x05D4  @ icid=0x171C ( 5916)  -> cid=1492 slot=0x171C  Self-Destruct Button
    .hword 0x05D5  @ icid=0x171D ( 5917)  -> cid=1493 slot=0x171D  Curse of Darkness
    .hword 0x05D6  @ icid=0x171E ( 5918)  -> cid=1494 slot=0x171E  Begone, Knave!
    .hword 0x05D7  @ icid=0x171F ( 5919)  -> cid=1495 slot=0x171F  DNA Transplant
    .hword 0x05D8  @ icid=0x1720 ( 5920)  -> cid=1496 slot=0x1720  Robbin' Zombie
    .hword 0x05D9  @ icid=0x1721 ( 5921)  -> cid=1497 slot=0x1721  Trap Jammer
    .hword 0x05DA  @ icid=0x1722 ( 5922)  -> cid=1498 slot=0x1722  Invader of Darkness
    .hword 0x05DB  @ icid=0x1723 ( 5923)  -> cid=1499 slot=0x1723  Twinheaded Beast
    .hword 0xFFFF  @ icid=0x1724 ( 5924)  -> (none)
    .hword 0xFFFF  @ icid=0x1725 ( 5925)  -> (none)
    .hword 0xFFFF  @ icid=0x1726 ( 5926)  -> (none)
    .hword 0x05DC  @ icid=0x1727 ( 5927)  -> cid=1500 slot=0x1727  Abyss Soldier
    .hword 0xFFFF  @ icid=0x1728 ( 5928)  -> (none)
    .hword 0xFFFF  @ icid=0x1729 ( 5929)  -> (none)
    .hword 0x05DD  @ icid=0x172A ( 5930)  -> cid=1501 slot=0x172A  Inferno Hammer
    .hword 0x05DE  @ icid=0x172B ( 5931)  -> cid=1502 slot=0x172B  Emes the Infinity
    .hword 0x05DF  @ icid=0x172C ( 5932)  -> cid=1503 slot=0x172C  D. D. Assailant
    .hword 0x05E0  @ icid=0x172D ( 5933)  -> cid=1504 slot=0x172D  Teva
    .hword 0xFFFF  @ icid=0x172E ( 5934)  -> (none)
    .hword 0x05E1  @ icid=0x172F ( 5935)  -> cid=1505 slot=0x172F  Skull Zoma
    .hword 0x082C  @ icid=0x1730 ( 5936)  -> cid=2092 slot=0x1730
    .hword 0xFFFF  @ icid=0x1731 ( 5937)  -> (none)
    .hword 0xFFFF  @ icid=0x1732 ( 5938)  -> (none)
    .hword 0xFFFF  @ icid=0x1733 ( 5939)  -> (none)
    .hword 0xFFFF  @ icid=0x1734 ( 5940)  -> (none)
    .hword 0xFFFF  @ icid=0x1735 ( 5941)  -> (none)
    .hword 0xFFFF  @ icid=0x1736 ( 5942)  -> (none)
    .hword 0x05E2  @ icid=0x1737 ( 5943)  -> cid=1506 slot=0x1737  Maximum Six
    .hword 0x05E3  @ icid=0x1738 ( 5944)  -> cid=1507 slot=0x1738  Dangerous Machine TYPE-6
    .hword 0x05E4  @ icid=0x1739 ( 5945)  -> cid=1508 slot=0x1739  Sixth Sense
    .hword 0x05E5  @ icid=0x173A ( 5946)  -> cid=1509 slot=0x173A  Gogiga Gagagigo
    .hword 0x05E6  @ icid=0x173B ( 5947)  -> cid=1510 slot=0x173B  Warrior of Zera
    .hword 0x05E7  @ icid=0x173C ( 5948)  -> cid=1511 slot=0x173C  Sealmaster Meisei
    .hword 0x05E8  @ icid=0x173D ( 5949)  -> cid=1512 slot=0x173D  Mystical Shine Ball
    .hword 0x05E9  @ icid=0x173E ( 5950)  -> cid=1513 slot=0x173E  Metal Armored Bug
    .hword 0x05EA  @ icid=0x173F ( 5951)  -> cid=1514 slot=0x173F  The Agent of Judgment - Saturn
    .hword 0x05EB  @ icid=0x1740 ( 5952)  -> cid=1515 slot=0x1740  The Agent of Wisdom - Mercury
    .hword 0x05EC  @ icid=0x1741 ( 5953)  -> cid=1516 slot=0x1741  The Agent of Creation - Venus
    .hword 0x05ED  @ icid=0x1742 ( 5954)  -> cid=1517 slot=0x1742  The Agent of Force - Mars
    .hword 0x05EE  @ icid=0x1743 ( 5955)  -> cid=1518 slot=0x1743  The Unhappy Girl
    .hword 0x05EF  @ icid=0x1744 ( 5956)  -> cid=1519 slot=0x1744  Soul-Absorbing Bone Tower
    .hword 0x05F0  @ icid=0x1745 ( 5957)  -> cid=1520 slot=0x1745  The Kick Man
    .hword 0x05F1  @ icid=0x1746 ( 5958)  -> cid=1521 slot=0x1746  Vampire Lady
    .hword 0x05F2  @ icid=0x1747 ( 5959)  -> cid=1522 slot=0x1747  Rocket Jumper
    .hword 0x05F3  @ icid=0x1748 ( 5960)  -> cid=1523 slot=0x1748  Avatar of The Pot
    .hword 0x05F4  @ icid=0x1749 ( 5961)  -> cid=1524 slot=0x1749  Legendary Jujitsu Master
    .hword 0x05F5  @ icid=0x174A ( 5962)  -> cid=1525 slot=0x174A  KA-2 Des Scissors
    .hword 0x05F6  @ icid=0x174B ( 5963)  -> cid=1526 slot=0x174B  Needle Burrower
    .hword 0x05F7  @ icid=0x174C ( 5964)  -> cid=1527 slot=0x174C  Blowback Dragon
    .hword 0x05F8  @ icid=0x174D ( 5965)  -> cid=1528 slot=0x174D  Zaborg the Thunder Monarch
    .hword 0x05F9  @ icid=0x174E ( 5966)  -> cid=1529 slot=0x174E  Atomic Firefly
    .hword 0x05FA  @ icid=0x174F ( 5967)  -> cid=1530 slot=0x174F  Mermaid Knight
    .hword 0x05FB  @ icid=0x1750 ( 5968)  -> cid=1531 slot=0x1750  Piranha Army
    .hword 0x05FC  @ icid=0x1751 ( 5969)  -> cid=1532 slot=0x1751  Two Thousand Needles
    .hword 0x05FD  @ icid=0x1752 ( 5970)  -> cid=1533 slot=0x1752  Disc Fighter
    .hword 0x05FE  @ icid=0x1753 ( 5971)  -> cid=1534 slot=0x1753  Arcane Archer of the Forest
    .hword 0x05FF  @ icid=0x1754 ( 5972)  -> cid=1535 slot=0x1754  Lady Ninja Yae
    .hword 0x0600  @ icid=0x1755 ( 5973)  -> cid=1536 slot=0x1755  Goblin King
    .hword 0x0601  @ icid=0x1756 ( 5974)  -> cid=1537 slot=0x1756  Solar Flare Dragon
    .hword 0x0602  @ icid=0x1757 ( 5975)  -> cid=1538 slot=0x1757  White Magician Pikeru
    .hword 0x0603  @ icid=0x1758 ( 5976)  -> cid=1539 slot=0x1758  Archlord Zerato
    .hword 0x0604  @ icid=0x1759 ( 5977)  -> cid=1540 slot=0x1759  Opti-Camouflage Armor
    .hword 0x0605  @ icid=0x175A ( 5978)  -> cid=1541 slot=0x175A  Mystik Wok
    .hword 0x0606  @ icid=0x175B ( 5979)  -> cid=1542 slot=0x175B  Burst Stream of Destruction
    .hword 0x0607  @ icid=0x175C ( 5980)  -> cid=1543 slot=0x175C  Monster Gate
    .hword 0xFFFF  @ icid=0x175D ( 5981)  -> (none)
    .hword 0x0608  @ icid=0x175E ( 5982)  -> cid=1544 slot=0x175E  The Sanctuary in the Sky
    .hword 0x0609  @ icid=0x175F ( 5983)  -> cid=1545 slot=0x175F  Earthquake
    .hword 0xFFFF  @ icid=0x1760 ( 5984)  -> (none)
    .hword 0x060A  @ icid=0x1761 ( 5985)  -> cid=1546 slot=0x1761  Goblin Thief
    .hword 0x060B  @ icid=0x1762 ( 5986)  -> cid=1547 slot=0x1762  Backfire
    .hword 0x060C  @ icid=0x1763 ( 5987)  -> cid=1548 slot=0x1763  Micro Ray
    .hword 0x060D  @ icid=0x1764 ( 5988)  -> cid=1549 slot=0x1764  Light of Judgment
    .hword 0xFFFF  @ icid=0x1765 ( 5989)  -> (none)
    .hword 0x060E  @ icid=0x1766 ( 5990)  -> cid=1550 slot=0x1766  Wall of Revealing Light
    .hword 0x060F  @ icid=0x1767 ( 5991)  -> cid=1551 slot=0x1767  Solar Ray
    .hword 0x0610  @ icid=0x1768 ( 5992)  -> cid=1552 slot=0x1768  Ninjitsu Art of Transformation
    .hword 0x0611  @ icid=0x1769 ( 5993)  -> cid=1553 slot=0x1769  Beckoning Light
    .hword 0x0612  @ icid=0x176A ( 5994)  -> cid=1554 slot=0x176A  Draining Shield
    .hword 0x0613  @ icid=0x176B ( 5995)  -> cid=1555 slot=0x176B  Armor Break
    .hword 0x0614  @ icid=0x176C ( 5996)  -> cid=1556 slot=0x176C  Mazera DeVille
    .hword 0xFFFF  @ icid=0x176D ( 5997)  -> (none)
    .hword 0xFFFF  @ icid=0x176E ( 5998)  -> (none)
    .hword 0xFFFF  @ icid=0x176F ( 5999)  -> (none)
    .hword 0x0615  @ icid=0x1770 ( 6000)  -> cid=1557 slot=0x1770  Marshmallon
    .hword 0x0616  @ icid=0x1771 ( 6001)  -> cid=1558 slot=0x1771  Skull Descovery Knight
    .hword 0xFFFF  @ icid=0x1772 ( 6002)  -> (none)
    .hword 0x0617  @ icid=0x1773 ( 6003)  -> cid=1559 slot=0x1773  Shield Crash
    .hword 0xFFFF  @ icid=0x1774 ( 6004)  -> (none)
    .hword 0x0618  @ icid=0x1775 ( 6005)  -> cid=1560 slot=0x1775  Return Zombie
    .hword 0x0619  @ icid=0x1776 ( 6006)  -> cid=1561 slot=0x1776  Corpse of Yata-Garasu
    .hword 0x061A  @ icid=0x1777 ( 6007)  -> cid=1562 slot=0x1777  Marshmallon glasses
    .hword 0xFFFF  @ icid=0x1778 ( 6008)  -> (none)
    .hword 0xFFFF  @ icid=0x1779 ( 6009)  -> (none)
    .hword 0x061B  @ icid=0x177A ( 6010)  -> cid=1563 slot=0x177A  Earthbound Spirit's Invitation
    .hword 0xFFFF  @ icid=0x177B ( 6011)  -> (none)
    .hword 0xFFFF  @ icid=0x177C ( 6012)  -> (none)
    .hword 0xFFFF  @ icid=0x177D ( 6013)  -> (none)
    .hword 0xFFFF  @ icid=0x177E ( 6014)  -> (none)
    .hword 0xFFFF  @ icid=0x177F ( 6015)  -> (none)
    .hword 0xFFFF  @ icid=0x1780 ( 6016)  -> (none)
    .hword 0xFFFF  @ icid=0x1781 ( 6017)  -> (none)
    .hword 0x061C  @ icid=0x1782 ( 6018)  -> cid=1564 slot=0x1782  Mokey Mokey
    .hword 0x061D  @ icid=0x1783 ( 6019)  -> cid=1565 slot=0x1783  Gigobyte
    .hword 0x061E  @ icid=0x1784 ( 6020)  -> cid=1566 slot=0x1784  Kozaky
    .hword 0x061F  @ icid=0x1785 ( 6021)  -> cid=1567 slot=0x1785  Fiend Scorpion
    .hword 0x0620  @ icid=0x1786 ( 6022)  -> cid=1568 slot=0x1786  Pharaoh's Servant
    .hword 0x0621  @ icid=0x1787 ( 6023)  -> cid=1569 slot=0x1787  Pharaonic Protector
    .hword 0x0622  @ icid=0x1788 ( 6024)  -> cid=1570 slot=0x1788  Spirit of the Pharaoh
    .hword 0x0623  @ icid=0x1789 ( 6025)  -> cid=1571 slot=0x1789  Theban Nightmare
    .hword 0x0624  @ icid=0x178A ( 6026)  -> cid=1572 slot=0x178A  Aswan Apparition
    .hword 0x0625  @ icid=0x178B ( 6027)  -> cid=1573 slot=0x178B  Protector of the Sanctuary
    .hword 0x0626  @ icid=0x178C ( 6028)  -> cid=1574 slot=0x178C  Nubian Guard
    .hword 0xFFFF  @ icid=0x178D ( 6029)  -> (none)
    .hword 0x0627  @ icid=0x178E ( 6030)  -> cid=1575 slot=0x178E  Desertapir
    .hword 0x0628  @ icid=0x178F ( 6031)  -> cid=1576 slot=0x178F  Sand Gambler
    .hword 0xFFFF  @ icid=0x1790 ( 6032)  -> (none)
    .hword 0x0629  @ icid=0x1791 ( 6033)  -> cid=1577 slot=0x1791  Ghost Knight of Jackal
    .hword 0x062A  @ icid=0x1792 ( 6034)  -> cid=1578 slot=0x1792  Absorbing Kid from the Sky
    .hword 0x062B  @ icid=0x1793 ( 6035)  -> cid=1579 slot=0x1793  Elephant Statue of Blessing
    .hword 0x062C  @ icid=0x1794 ( 6036)  -> cid=1580 slot=0x1794  Elephant Statue of Disaster
    .hword 0x062D  @ icid=0x1795 ( 6037)  -> cid=1581 slot=0x1795  Spirit Caller
    .hword 0x062E  @ icid=0x1796 ( 6038)  -> cid=1582 slot=0x1796  Emissary of the Afterlife
    .hword 0xFFFF  @ icid=0x1797 ( 6039)  -> (none)
    .hword 0x062F  @ icid=0x1798 ( 6040)  -> cid=1583 slot=0x1798  Double Coston
    .hword 0x0630  @ icid=0x1799 ( 6041)  -> cid=1584 slot=0x1799  Regenerating Mummy
    .hword 0x0631  @ icid=0x179A ( 6042)  -> cid=1585 slot=0x179A  Night Assailant
    .hword 0x0632  @ icid=0x179B ( 6043)  -> cid=1586 slot=0x179B  Man-Thro' Tro'
    .hword 0x0633  @ icid=0x179C ( 6044)  -> cid=1587 slot=0x179C  King of the Swamp
    .hword 0x0634  @ icid=0x179D ( 6045)  -> cid=1588 slot=0x179D  Emissary of the Oasis
    .hword 0x0635  @ icid=0x179E ( 6046)  -> cid=1589 slot=0x179E  Special Hurricane
    .hword 0x0636  @ icid=0x179F ( 6047)  -> cid=1590 slot=0x179F  Order to Charge
    .hword 0x0637  @ icid=0x17A0 ( 6048)  -> cid=1591 slot=0x17A0  Sword of the Soul-Eater
    .hword 0x0638  @ icid=0x17A1 ( 6049)  -> cid=1592 slot=0x17A1  Dust Barrier
    .hword 0x0639  @ icid=0x17A2 ( 6050)  -> cid=1593 slot=0x17A2  Soul Reversal
    .hword 0x063A  @ icid=0x17A3 ( 6051)  -> cid=1594 slot=0x17A3  Spell Economics
    .hword 0xFFFF  @ icid=0x17A4 ( 6052)  -> (none)
    .hword 0x063B  @ icid=0x17A5 ( 6053)  -> cid=1595 slot=0x17A5  7
    .hword 0x063C  @ icid=0x17A6 ( 6054)  -> cid=1596 slot=0x17A6  Level Limit - Area B
    .hword 0x063D  @ icid=0x17A7 ( 6055)  -> cid=1597 slot=0x17A7  Enchanting Fitting Room
    .hword 0x063E  @ icid=0x17A8 ( 6056)  -> cid=1598 slot=0x17A8  The Law of the Normal
    .hword 0x063F  @ icid=0x17A9 ( 6057)  -> cid=1599 slot=0x17A9  Dark Magic Attack
    .hword 0x0640  @ icid=0x17AA ( 6058)  -> cid=1600 slot=0x17AA  Delta Attacker
    .hword 0x0641  @ icid=0x17AB ( 6059)  -> cid=1601 slot=0x17AB  Thousand Energy
    .hword 0x0642  @ icid=0x17AC ( 6060)  -> cid=1602 slot=0x17AC  Triangle Power
    .hword 0x0643  @ icid=0x17AD ( 6061)  -> cid=1603 slot=0x17AD  The Third Sarcophagus
    .hword 0x0644  @ icid=0x17AE ( 6062)  -> cid=1604 slot=0x17AE  The Second Sarcophagus
    .hword 0x0645  @ icid=0x17AF ( 6063)  -> cid=1605 slot=0x17AF  The First Sarcophagus
    .hword 0xFFFF  @ icid=0x17B0 ( 6064)  -> (none)
    .hword 0xFFFF  @ icid=0x17B1 ( 6065)  -> (none)
    .hword 0x0646  @ icid=0x17B2 ( 6066)  -> cid=1606 slot=0x17B2  Human-Wave Tactics
    .hword 0x0647  @ icid=0x17B3 ( 6067)  -> cid=1607 slot=0x17B3  Curse of Anubis
    .hword 0x0648  @ icid=0x17B4 ( 6068)  -> cid=1608 slot=0x17B4  Desert Sunlight
    .hword 0x0649  @ icid=0x17B5 ( 6069)  -> cid=1609 slot=0x17B5  Des Counterblow
    .hword 0x064A  @ icid=0x17B6 ( 6070)  -> cid=1610 slot=0x17B6  Labyrinth of Nightmare
    .hword 0x064B  @ icid=0x17B7 ( 6071)  -> cid=1611 slot=0x17B7  Soul Resurrection
    .hword 0x064C  @ icid=0x17B8 ( 6072)  -> cid=1612 slot=0x17B8  Order to Smash
    .hword 0x064D  @ icid=0x17B9 ( 6073)  -> cid=1613 slot=0x17B9  The End of Anubis
    .hword 0xFFFF  @ icid=0x17BA ( 6074)  -> (none)
    .hword 0xFFFF  @ icid=0x17BB ( 6075)  -> (none)
    .hword 0x064E  @ icid=0x17BC ( 6076)  -> cid=1614 slot=0x17BC  Crush D. Gandra
    .hword 0xFFFF  @ icid=0x17BD ( 6077)  -> (none)
    .hword 0x064F  @ icid=0x17BE ( 6078)  -> cid=1615 slot=0x17BE  Return from the Different Dimension
    .hword 0x0650  @ icid=0x17BF ( 6079)  -> cid=1616 slot=0x17BF  Pyramid of Light
    .hword 0xFFFF  @ icid=0x17C0 ( 6080)  -> (none)
    .hword 0xFFFF  @ icid=0x17C1 ( 6081)  -> (none)
    .hword 0x0651  @ icid=0x17C2 ( 6082)  -> cid=1617 slot=0x17C2  Blue-Eyes Shining Dragon
    .hword 0x0652  @ icid=0x17C3 ( 6083)  -> cid=1618 slot=0x17C3  Familiar Knight
    .hword 0x0653  @ icid=0x17C4 ( 6084)  -> cid=1619 slot=0x17C4  Rare Metal Dragon
    .hword 0x0654  @ icid=0x17C5 ( 6085)  -> cid=1620 slot=0x17C5  Peten the Dark Clown
    .hword 0x0655  @ icid=0x17C6 ( 6086)  -> cid=1621 slot=0x17C6  Sorcerer of Dark Magic
    .hword 0x0656  @ icid=0x17C7 ( 6087)  -> cid=1622 slot=0x17C7  Andro Sphinx
    .hword 0x0657  @ icid=0x17C8 ( 6088)  -> cid=1623 slot=0x17C8  Sphinx Teleia
    .hword 0x0658  @ icid=0x17C9 ( 6089)  -> cid=1624 slot=0x17C9  Theinen the Great Sphinx
    .hword 0x0659  @ icid=0x17CA ( 6090)  -> cid=1625 slot=0x17CA  Inferno Tempest
    .hword 0xFFFF  @ icid=0x17CB ( 6091)  -> (none)
    .hword 0x065A  @ icid=0x17CC ( 6092)  -> cid=1626 slot=0x17CC  Watapon
    .hword 0x065B  @ icid=0x17CD ( 6093)  -> cid=1627 slot=0x17CD  Charcoal Inpachi
    .hword 0x065C  @ icid=0x17CE ( 6094)  -> cid=1628 slot=0x17CE  Neo Aqua Madoor
    .hword 0x065D  @ icid=0x17CF ( 6095)  -> cid=1629 slot=0x17CF  Skull Dog Marron
    .hword 0x065E  @ icid=0x17D0 ( 6096)  -> cid=1630 slot=0x17D0  Goblin Calligrapher
    .hword 0x065F  @ icid=0x17D1 ( 6097)  -> cid=1631 slot=0x17D1  Ultimate Insect LV1
    .hword 0x0660  @ icid=0x17D2 ( 6098)  -> cid=1632 slot=0x17D2  Horus the Black Flame Dragon LV4
    .hword 0x0661  @ icid=0x17D3 ( 6099)  -> cid=1633 slot=0x17D3  Horus the Black Flame Dragon LV6
    .hword 0x0662  @ icid=0x17D4 ( 6100)  -> cid=1634 slot=0x17D4  Horus the Black Flame Dragon LV8
    .hword 0x0663  @ icid=0x17D5 ( 6101)  -> cid=1635 slot=0x17D5  Dark Mimic LV1
    .hword 0x0664  @ icid=0x17D6 ( 6102)  -> cid=1636 slot=0x17D6  Dark Mimic LV3
    .hword 0x0665  @ icid=0x17D7 ( 6103)  -> cid=1637 slot=0x17D7  Mystic Swordsman LV2
    .hword 0x0666  @ icid=0x17D8 ( 6104)  -> cid=1638 slot=0x17D8  Mystic Swordsman LV4
    .hword 0x0667  @ icid=0x17D9 ( 6105)  -> cid=1639 slot=0x17D9  Armed Dragon LV3
    .hword 0x0668  @ icid=0x17DA ( 6106)  -> cid=1640 slot=0x17DA  Armed Dragon LV5
    .hword 0x0669  @ icid=0x17DB ( 6107)  -> cid=1641 slot=0x17DB  Armed Dragon LV7
    .hword 0x066A  @ icid=0x17DC ( 6108)  -> cid=1642 slot=0x17DC  Horus' Servant
    .hword 0x066B  @ icid=0x17DD ( 6109)  -> cid=1643 slot=0x17DD  Red-Eyes B. Chick
    .hword 0xFFFF  @ icid=0x17DE ( 6110)  -> (none)
    .hword 0x066C  @ icid=0x17DF ( 6111)  -> cid=1644 slot=0x17DF  Ninja Grandmaster Sasuke
    .hword 0x066D  @ icid=0x17E0 ( 6112)  -> cid=1645 slot=0x17E0  Rafflesia Seduction
    .hword 0x066E  @ icid=0x17E1 ( 6113)  -> cid=1646 slot=0x17E1  Ultimate Baseball Kid
    .hword 0x066F  @ icid=0x17E2 ( 6114)  -> cid=1647 slot=0x17E2  Mobius the Frost Monarch
    .hword 0x0670  @ icid=0x17E3 ( 6115)  -> cid=1648 slot=0x17E3  Element Dragon
    .hword 0x0671  @ icid=0x17E4 ( 6116)  -> cid=1649 slot=0x17E4  Element Soldier
    .hword 0x0672  @ icid=0x17E5 ( 6117)  -> cid=1650 slot=0x17E5  Howling Insect
    .hword 0x0673  @ icid=0x17E6 ( 6118)  -> cid=1651 slot=0x17E6  Masked Dragon
    .hword 0x0674  @ icid=0x17E7 ( 6119)  -> cid=1652 slot=0x17E7  Mind on Air
    .hword 0x0675  @ icid=0x17E8 ( 6120)  -> cid=1653 slot=0x17E8  Unshaven Angler
    .hword 0x0676  @ icid=0x17E9 ( 6121)  -> cid=1654 slot=0x17E9  The Trojan Horse
    .hword 0x0677  @ icid=0x17EA ( 6122)  -> cid=1655 slot=0x17EA  Nobleman-Eater Bug
    .hword 0x0678  @ icid=0x17EB ( 6123)  -> cid=1656 slot=0x17EB  Enraged Muka Muka
    .hword 0x0679  @ icid=0x17EC ( 6124)  -> cid=1657 slot=0x17EC  Hade-Hane
    .hword 0x067A  @ icid=0x17ED ( 6125)  -> cid=1658 slot=0x17ED  Penumbral Soldier Lady
    .hword 0x067B  @ icid=0x17EE ( 6126)  -> cid=1659 slot=0x17EE  Ojama King
    .hword 0x067C  @ icid=0x17EF ( 6127)  -> cid=1660 slot=0x17EF  Master of Oz
    .hword 0x067D  @ icid=0x17F0 ( 6128)  -> cid=1661 slot=0x17F0  Sanwitch
    .hword 0x067E  @ icid=0x17F1 ( 6129)  -> cid=1662 slot=0x17F1  Dark Factory of Mass Production
    .hword 0x067F  @ icid=0x17F2 ( 6130)  -> cid=1663 slot=0x17F2  Hammer Shot
    .hword 0x0680  @ icid=0x17F3 ( 6131)  -> cid=1664 slot=0x17F3  Mind Wipe
    .hword 0x0681  @ icid=0x17F4 ( 6132)  -> cid=1665 slot=0x17F4  Abyssal Designator
    .hword 0x0682  @ icid=0x17F5 ( 6133)  -> cid=1666 slot=0x17F5  Level Up!
    .hword 0x0683  @ icid=0x17F6 ( 6134)  -> cid=1667 slot=0x17F6  Inferno Fire Blast
    .hword 0x0684  @ icid=0x17F7 ( 6135)  -> cid=1668 slot=0x17F7  The Graveyard in the Fourth Dimension
    .hword 0x0685  @ icid=0x17F8 ( 6136)  -> cid=1669 slot=0x17F8  Two-Man Cell Battle
    .hword 0x0686  @ icid=0x17F9 ( 6137)  -> cid=1670 slot=0x17F9  Big Wave Small Wave
    .hword 0x0687  @ icid=0x17FA ( 6138)  -> cid=1671 slot=0x17FA  Fusion Weapon
    .hword 0x0688  @ icid=0x17FB ( 6139)  -> cid=1672 slot=0x17FB  Ritual Weapon
    .hword 0x0689  @ icid=0x17FC ( 6140)  -> cid=1673 slot=0x17FC  Taunt
    .hword 0x068A  @ icid=0x17FD ( 6141)  -> cid=1674 slot=0x17FD  Absolute End
    .hword 0x068B  @ icid=0x17FE ( 6142)  -> cid=1675 slot=0x17FE  Spirit Barrier
    .hword 0x068C  @ icid=0x17FF ( 6143)  -> cid=1676 slot=0x17FF  Ninjitsu Art of Decoy
    .hword 0x068D  @ icid=0x1800 ( 6144)  -> cid=1677 slot=0x1800  Enervating Mist
    .hword 0x068E  @ icid=0x1801 ( 6145)  -> cid=1678 slot=0x1801  Heavy Slump
    .hword 0x068F  @ icid=0x1802 ( 6146)  -> cid=1679 slot=0x1802  Greed
    .hword 0xFFFF  @ icid=0x1803 ( 6147)  -> (none)
    .hword 0x0690  @ icid=0x1804 ( 6148)  -> cid=1680 slot=0x1804  Cemetary Bomb
    .hword 0x0691  @ icid=0x1805 ( 6149)  -> cid=1681 slot=0x1805  Hallowed Life Barrier
    .hword 0x0692  @ icid=0x1806 ( 6150)  -> cid=1682 slot=0x1806  The Tricky
    .hword 0x0693  @ icid=0x1807 ( 6151)  -> cid=1683 slot=0x1807  Green Gadget
    .hword 0xFFFF  @ icid=0x1808 ( 6152)  -> (none)
    .hword 0x0694  @ icid=0x1809 ( 6153)  -> cid=1684 slot=0x1809  Stronghold
    .hword 0xFFFF  @ icid=0x180A ( 6154)  -> (none)
    .hword 0x0696  @ icid=0x180B ( 6155)  -> cid=1686 slot=0x180B  Red Gadget
    .hword 0x0697  @ icid=0x180C ( 6156)  -> cid=1687 slot=0x180C  Yellow Gadget
    .hword 0x082D  @ icid=0x180D ( 6157)  -> cid=2093 slot=0x180D
    .hword 0x0698  @ icid=0x180E ( 6158)  -> cid=1688 slot=0x180E  Tricky's Magic 4
    .hword 0xFFFF  @ icid=0x180F ( 6159)  -> (none)
    .hword 0x0699  @ icid=0x1810 ( 6160)  -> cid=1689 slot=0x1810  The Blockman
    .hword 0xFFFF  @ icid=0x1811 ( 6161)  -> (none)
    .hword 0x069A  @ icid=0x1812 ( 6162)  -> cid=1690 slot=0x1812  Silent Swordsman LV3
    .hword 0x082E  @ icid=0x1813 ( 6163)  -> cid=2094 slot=0x1813
    .hword 0x069B  @ icid=0x1814 ( 6164)  -> cid=1691 slot=0x1814  Silent Swordsman LV5
    .hword 0xFFFF  @ icid=0x1815 ( 6165)  -> (none)
    .hword 0x069C  @ icid=0x1816 ( 6166)  -> cid=1692 slot=0x1816  Silent Swordsman LV7
    .hword 0x069D  @ icid=0x1817 ( 6167)  -> cid=1693 slot=0x1817  Silent Magician LV4
    .hword 0x069E  @ icid=0x1818 ( 6168)  -> cid=1694 slot=0x1818  Magician's Circle
    .hword 0x069F  @ icid=0x1819 ( 6169)  -> cid=1695 slot=0x1819  Magician's Unite
    .hword 0x06A0  @ icid=0x181A ( 6170)  -> cid=1696 slot=0x181A  Silent Magician LV8
    .hword 0xFFFF  @ icid=0x181B ( 6171)  -> (none)
    .hword 0x06A1  @ icid=0x181C ( 6172)  -> cid=1697 slot=0x181C  Woodborg Inpachi
    .hword 0x06A2  @ icid=0x181D ( 6173)  -> cid=1698 slot=0x181D  Mighty Guard
    .hword 0x06A3  @ icid=0x181E ( 6174)  -> cid=1699 slot=0x181E  Bokoichi the Freightening Car
    .hword 0x06A4  @ icid=0x181F ( 6175)  -> cid=1700 slot=0x181F  Harpie Girl
    .hword 0x06A5  @ icid=0x1820 ( 6176)  -> cid=1701 slot=0x1820  The Creator
    .hword 0x06A6  @ icid=0x1821 ( 6177)  -> cid=1702 slot=0x1821  The Creator Incarnate
    .hword 0x06A7  @ icid=0x1822 ( 6178)  -> cid=1703 slot=0x1822  Ultimate Insect LV3
    .hword 0x06A8  @ icid=0x1823 ( 6179)  -> cid=1704 slot=0x1823  Mystic Swordsman LV6
    .hword 0xFFFF  @ icid=0x1824 ( 6180)  -> (none)
    .hword 0x06A9  @ icid=0x1825 ( 6181)  -> cid=1705 slot=0x1825  Heavy Mech Support Platform
    .hword 0x06AA  @ icid=0x1826 ( 6182)  -> cid=1706 slot=0x1826  Element Magician
    .hword 0x06AB  @ icid=0x1827 ( 6183)  -> cid=1707 slot=0x1827  Element Saurus
    .hword 0x06AC  @ icid=0x1828 ( 6184)  -> cid=1708 slot=0x1828  Roc from the Valley of Haze
    .hword 0x06AD  @ icid=0x1829 ( 6185)  -> cid=1709 slot=0x1829  Sasuke Samurai #4
    .hword 0x06AE  @ icid=0x182A ( 6186)  -> cid=1710 slot=0x182A  Harpie Lady 1
    .hword 0x06AF  @ icid=0x182B ( 6187)  -> cid=1711 slot=0x182B  Harpie Lady 2
    .hword 0x06B0  @ icid=0x182C ( 6188)  -> cid=1712 slot=0x182C  Harpie Lady 3
    .hword 0x06B1  @ icid=0x182D ( 6189)  -> cid=1713 slot=0x182D  Raging Flame Sprite
    .hword 0x06B2  @ icid=0x182E ( 6190)  -> cid=1714 slot=0x182E  Thestalos the Firestorm Monarch
    .hword 0x06B3  @ icid=0x182F ( 6191)  -> cid=1715 slot=0x182F  Eagle Eye
    .hword 0x06B4  @ icid=0x1830 ( 6192)  -> cid=1716 slot=0x1830  Tactical Espionage Expert
    .hword 0x06B5  @ icid=0x1831 ( 6193)  -> cid=1717 slot=0x1831  Invasion of Flames
    .hword 0x06B6  @ icid=0x1832 ( 6194)  -> cid=1718 slot=0x1832  Creeping Doom Manta
    .hword 0x06B7  @ icid=0x1833 ( 6195)  -> cid=1719 slot=0x1833  Pitch-Black Warwolf
    .hword 0x06B8  @ icid=0x1834 ( 6196)  -> cid=1720 slot=0x1834  Mirage Dragon
    .hword 0x06B9  @ icid=0x1835 ( 6197)  -> cid=1721 slot=0x1835  Gaia Soul the Combustible Collective
    .hword 0x06BA  @ icid=0x1836 ( 6198)  -> cid=1722 slot=0x1836  Fox Fire
    .hword 0x06BB  @ icid=0x1837 ( 6199)  -> cid=1723 slot=0x1837  Big Core
    .hword 0x06BC  @ icid=0x1838 ( 6200)  -> cid=1724 slot=0x1838  Fusilier Dragon, the Dual-Mode Beast
    .hword 0x06BD  @ icid=0x1839 ( 6201)  -> cid=1725 slot=0x1839  Dekoichi the Battlechanted Locomotive
    .hword 0x06BE  @ icid=0x183A ( 6202)  -> cid=1726 slot=0x183A  A-Team: Trap Disposal Unit
    .hword 0x06BF  @ icid=0x183B ( 6203)  -> cid=1727 slot=0x183B  Homunculus the Alchemic Being
    .hword 0x06C0  @ icid=0x183C ( 6204)  -> cid=1728 slot=0x183C  Dark Blade the Dragon Knight
    .hword 0x06C1  @ icid=0x183D ( 6205)  -> cid=1729 slot=0x183D  Mokey Mokey King
    .hword 0x06C2  @ icid=0x183E ( 6206)  -> cid=1730 slot=0x183E  Serial Spell
    .hword 0x06C3  @ icid=0x183F ( 6207)  -> cid=1731 slot=0x183F  Harpies' Hunting Ground
    .hword 0x06C4  @ icid=0x1840 ( 6208)  -> cid=1732 slot=0x1840  Triangle Ecstasy Spark
    .hword 0x06C5  @ icid=0x1841 ( 6209)  -> cid=1733 slot=0x1841  Necklace of Command
    .hword 0x06C6  @ icid=0x1842 ( 6210)  -> cid=1734 slot=0x1842  Flint
    .hword 0x06C7  @ icid=0x1843 ( 6211)  -> cid=1735 slot=0x1843  Mokey Mokey Smackdown
    .hword 0x06C8  @ icid=0x1844 ( 6212)  -> cid=1736 slot=0x1844  Back to Square One
    .hword 0x06C9  @ icid=0x1845 ( 6213)  -> cid=1737 slot=0x1845  Monster Reincarnation
    .hword 0x06CA  @ icid=0x1846 ( 6214)  -> cid=1738 slot=0x1846  Ballista of Rampart Smashing
    .hword 0x06CB  @ icid=0x1847 ( 6215)  -> cid=1739 slot=0x1847  Lighten the Load
    .hword 0x06CC  @ icid=0x1848 ( 6216)  -> cid=1740 slot=0x1848  Malice Dispersion
    .hword 0x06CD  @ icid=0x1849 ( 6217)  -> cid=1741 slot=0x1849  Divine Wrath
    .hword 0x06CE  @ icid=0x184A ( 6218)  -> cid=1742 slot=0x184A  Xing Zhen Hu
    .hword 0x06CF  @ icid=0x184B ( 6219)  -> cid=1743 slot=0x184B  Rare Metalmorph
    .hword 0xFFFF  @ icid=0x184C ( 6220)  -> (none)
    .hword 0x06D0  @ icid=0x184D ( 6221)  -> cid=1744 slot=0x184D  Mind Haxorz
    .hword 0x06D1  @ icid=0x184E ( 6222)  -> cid=1745 slot=0x184E  Fuh-Rin-Ka-Zan
    .hword 0x06D2  @ icid=0x184F ( 6223)  -> cid=1746 slot=0x184F  Chain Burst
    .hword 0x06D3  @ icid=0x1850 ( 6224)  -> cid=1747 slot=0x1850  Pikeru's Circle of Enchantment
    .hword 0x06D4  @ icid=0x1851 ( 6225)  -> cid=1748 slot=0x1851  Spell Purification
    .hword 0x06D5  @ icid=0x1852 ( 6226)  -> cid=1749 slot=0x1852  Astral Barrier
    .hword 0x06D6  @ icid=0x1853 ( 6227)  -> cid=1750 slot=0x1853  Covering Fire
    .hword 0xFFFF  @ icid=0x1854 ( 6228)  -> (none)
    .hword 0x06D7  @ icid=0x1855 ( 6229)  -> cid=1751 slot=0x1855  Castle Gate
    .hword 0xFFFF  @ icid=0x1856 ( 6230)  -> (none)
    .hword 0x06D8  @ icid=0x1857 ( 6231)  -> cid=1752 slot=0x1857  Owner's Seal
    .hword 0x06D9  @ icid=0x1858 ( 6232)  -> cid=1753 slot=0x1858  Space Mambo
    .hword 0x06DA  @ icid=0x1859 ( 6233)  -> cid=1754 slot=0x1859  Divine Dragon Ragnarok
    .hword 0x06DB  @ icid=0x185A ( 6234)  -> cid=1755 slot=0x185A  Chu-Ske the Mouse Fighter
    .hword 0x06DC  @ icid=0x185B ( 6235)  -> cid=1756 slot=0x185B  Insect Knight
    .hword 0x06DD  @ icid=0x185C ( 6236)  -> cid=1757 slot=0x185C  Sacred Phoenix of Nephthys
    .hword 0x06DE  @ icid=0x185D ( 6237)  -> cid=1758 slot=0x185D  Hand of Nephthys
    .hword 0x06DF  @ icid=0x185E ( 6238)  -> cid=1759 slot=0x185E  Ultimate Insect LV5
    .hword 0x06E0  @ icid=0x185F ( 6239)  -> cid=1760 slot=0x185F  Granmarg the Rock Monarch
    .hword 0x06E1  @ icid=0x1860 ( 6240)  -> cid=1761 slot=0x1860  Element Valkyrie
    .hword 0x06E2  @ icid=0x1861 ( 6241)  -> cid=1762 slot=0x1861  Element Doom
    .hword 0x06E3  @ icid=0x1862 ( 6242)  -> cid=1763 slot=0x1862  Maji-Gire Panda
    .hword 0x06E4  @ icid=0x1863 ( 6243)  -> cid=1764 slot=0x1863  Catnipped Kitty
    .hword 0x06E5  @ icid=0x1864 ( 6244)  -> cid=1765 slot=0x1864  Behemoth the King of All Animals
    .hword 0x06E6  @ icid=0x1865 ( 6245)  -> cid=1766 slot=0x1865  Big-Tusked Mammoth
    .hword 0x06E7  @ icid=0x1866 ( 6246)  -> cid=1767 slot=0x1866  Kangaroo Champ
    .hword 0x06E8  @ icid=0x1867 ( 6247)  -> cid=1768 slot=0x1867  Hyena
    .hword 0x06E9  @ icid=0x1868 ( 6248)  -> cid=1769 slot=0x1868  Blade Rabbit
    .hword 0x06EA  @ icid=0x1869 ( 6249)  -> cid=1770 slot=0x1869  Mecha-Dog Marron
    .hword 0x06EB  @ icid=0x186A ( 6250)  -> cid=1771 slot=0x186A  Blast Magician
    .hword 0x06EC  @ icid=0x186B ( 6251)  -> cid=1772 slot=0x186B  Gearfried the Swordmaster
    .hword 0x06ED  @ icid=0x186C ( 6252)  -> cid=1773 slot=0x186C  Armed Samurai - Ben Kei
    .hword 0x06EE  @ icid=0x186D ( 6253)  -> cid=1774 slot=0x186D  Shadowslayer
    .hword 0x06EF  @ icid=0x186E ( 6254)  -> cid=1775 slot=0x186E  Golem Sentry
    .hword 0x06F0  @ icid=0x186F ( 6255)  -> cid=1776 slot=0x186F  Abare Ushioni
    .hword 0x06F1  @ icid=0x1870 ( 6256)  -> cid=1777 slot=0x1870  The Light - Hex-Sealed Fusion
    .hword 0x06F2  @ icid=0x1871 ( 6257)  -> cid=1778 slot=0x1871  The Dark - Hex-Sealed Fusion
    .hword 0x06F3  @ icid=0x1872 ( 6258)  -> cid=1779 slot=0x1872  The Earth - Hex-Sealed Fusion
    .hword 0x06F4  @ icid=0x1873 ( 6259)  -> cid=1780 slot=0x1873  Whirlwind Prodigy
    .hword 0x06F5  @ icid=0x1874 ( 6260)  -> cid=1781 slot=0x1874  Flame Ruler
    .hword 0x06F6  @ icid=0x1875 ( 6261)  -> cid=1782 slot=0x1875  Firebird
    .hword 0x06F7  @ icid=0x1876 ( 6262)  -> cid=1783 slot=0x1876  Rescue Cat
    .hword 0x06F8  @ icid=0x1877 ( 6263)  -> cid=1784 slot=0x1877  Brain Jacker
    .hword 0x06F9  @ icid=0x1878 ( 6264)  -> cid=1785 slot=0x1878  Gatling Dragon
    .hword 0x06FA  @ icid=0x1879 ( 6265)  -> cid=1786 slot=0x1879  King Dragun
    .hword 0x06FB  @ icid=0x187A ( 6266)  -> cid=1787 slot=0x187A  A Feather of the Phoenix
    .hword 0x06FC  @ icid=0x187B ( 6267)  -> cid=1788 slot=0x187B  Poison Fangs
    .hword 0x06FD  @ icid=0x187C ( 6268)  -> cid=1789 slot=0x187C  Swords of Concealing Light
    .hword 0x06FE  @ icid=0x187D ( 6269)  -> cid=1790 slot=0x187D  Spiral Spear Strike
    .hword 0x06FF  @ icid=0x187E ( 6270)  -> cid=1791 slot=0x187E  Release Restraint
    .hword 0x0700  @ icid=0x187F ( 6271)  -> cid=1792 slot=0x187F  Centrifugal Field
    .hword 0x0701  @ icid=0x1880 ( 6272)  -> cid=1793 slot=0x1880  Fulfillment of the Contract
    .hword 0x0702  @ icid=0x1881 ( 6273)  -> cid=1794 slot=0x1881  Re-Fusion
    .hword 0x0703  @ icid=0x1882 ( 6274)  -> cid=1795 slot=0x1882  The Big March of Animals
    .hword 0x0704  @ icid=0x1883 ( 6275)  -> cid=1796 slot=0x1883  Cross Counter
    .hword 0xFFFF  @ icid=0x1884 ( 6276)  -> (none)
    .hword 0xFFFF  @ icid=0x1885 ( 6277)  -> (none)
    .hword 0x0705  @ icid=0x1886 ( 6278)  -> cid=1797 slot=0x1886  Threatening Roar
    .hword 0x0706  @ icid=0x1887 ( 6279)  -> cid=1798 slot=0x1887  Phoenix Wing Wind Blast
    .hword 0x0707  @ icid=0x1888 ( 6280)  -> cid=1799 slot=0x1888  Good Goblin Housekeeping
    .hword 0x0708  @ icid=0x1889 ( 6281)  -> cid=1800 slot=0x1889  Beast Soul Swap
    .hword 0x0709  @ icid=0x188A ( 6282)  -> cid=1801 slot=0x188A  Assault on GHQ
    .hword 0x070A  @ icid=0x188B ( 6283)  -> cid=1802 slot=0x188B  D.D. Dynamite
    .hword 0x070B  @ icid=0x188C ( 6284)  -> cid=1803 slot=0x188C  Deck Devastation Virus
    .hword 0x070C  @ icid=0x188D ( 6285)  -> cid=1804 slot=0x188D  Elemental Burst
    .hword 0x070D  @ icid=0x188E ( 6286)  -> cid=1805 slot=0x188E  Forced Ceasefire
    .hword 0x070E  @ icid=0x188F ( 6287)  -> cid=1806 slot=0x188F  Curse of Vampire
    .hword 0x070F  @ icid=0x1890 ( 6288)  -> cid=1807 slot=0x1890  Union Attack
    .hword 0x0710  @ icid=0x1891 ( 6289)  -> cid=1808 slot=0x1891  Blood Sucker
    .hword 0xFFFF  @ icid=0x1892 ( 6290)  -> (none)
    .hword 0x0711  @ icid=0x1893 ( 6291)  -> cid=1809 slot=0x1893  Overpowering Eye
    .hword 0x0712  @ icid=0x1894 ( 6292)  -> cid=1810 slot=0x1894  Red-Eyes Darkness Dragon
    .hword 0x0713  @ icid=0x1895 ( 6293)  -> cid=1811 slot=0x1895  Vampire Genesis
    .hword 0xFFFF  @ icid=0x1896 ( 6294)  -> (none)
    .hword 0xFFFF  @ icid=0x1897 ( 6295)  -> (none)
    .hword 0xFFFF  @ icid=0x1898 ( 6296)  -> (none)
    .hword 0xFFFF  @ icid=0x1899 ( 6297)  -> (none)
    .hword 0x0714  @ icid=0x189A ( 6298)  -> cid=1812 slot=0x189A  Kaibaman
    .hword 0xFFFF  @ icid=0x189B ( 6299)  -> (none)
    .hword 0xFFFF  @ icid=0x189C ( 6300)  -> (none)
    .hword 0xFFFF  @ icid=0x189D ( 6301)  -> (none)
    .hword 0xFFFF  @ icid=0x189E ( 6302)  -> (none)
    .hword 0xFFFF  @ icid=0x189F ( 6303)  -> (none)
    .hword 0xFFFF  @ icid=0x18A0 ( 6304)  -> (none)
    .hword 0xFFFF  @ icid=0x18A1 ( 6305)  -> (none)
    .hword 0xFFFF  @ icid=0x18A2 ( 6306)  -> (none)
    .hword 0xFFFF  @ icid=0x18A3 ( 6307)  -> (none)
    .hword 0xFFFF  @ icid=0x18A4 ( 6308)  -> (none)
    .hword 0xFFFF  @ icid=0x18A5 ( 6309)  -> (none)
    .hword 0x0715  @ icid=0x18A6 ( 6310)  -> cid=1813 slot=0x18A6  Elemental Hero Avian
    .hword 0x0716  @ icid=0x18A7 ( 6311)  -> cid=1814 slot=0x18A7  Elemental Hero Burstinatrix
    .hword 0x0717  @ icid=0x18A8 ( 6312)  -> cid=1815 slot=0x18A8  Elemental Hero Clayman
    .hword 0x0718  @ icid=0x18A9 ( 6313)  -> cid=1816 slot=0x18A9  Elemental Hero Sparkman
    .hword 0x0719  @ icid=0x18AA ( 6314)  -> cid=1817 slot=0x18AA  Winged Kuriboh
    .hword 0x071B  @ icid=0x18AB ( 6315)  -> cid=1819 slot=0x18AB  Ancient Gear Golem
    .hword 0x071C  @ icid=0x18AC ( 6316)  -> cid=1820 slot=0x18AC  Ancient Gear Beast
    .hword 0x071D  @ icid=0x18AD ( 6317)  -> cid=1821 slot=0x18AD  Ancient Gear Soldier
    .hword 0x071E  @ icid=0x18AE ( 6318)  -> cid=1822 slot=0x18AE  Millennium Scorpion
    .hword 0x071F  @ icid=0x18AF ( 6319)  -> cid=1823 slot=0x18AF  Ultimate Insect LV7
    .hword 0x0720  @ icid=0x18B0 ( 6320)  -> cid=1824 slot=0x18B0  Lost Guardian
    .hword 0x0721  @ icid=0x18B1 ( 6321)  -> cid=1825 slot=0x18B1  Hieracosphinx
    .hword 0x0722  @ icid=0x18B2 ( 6322)  -> cid=1826 slot=0x18B2  Criosphinx
    .hword 0x0723  @ icid=0x18B3 ( 6323)  -> cid=1827 slot=0x18B3  Moai Interceptor Cannons
    .hword 0x0724  @ icid=0x18B4 ( 6324)  -> cid=1828 slot=0x18B4  Megarock Dragon
    .hword 0x0725  @ icid=0x18B5 ( 6325)  -> cid=1829 slot=0x18B5  Dummy Golem
    .hword 0x0726  @ icid=0x18B6 ( 6326)  -> cid=1830 slot=0x18B6  Grave Ohja
    .hword 0x0727  @ icid=0x18B7 ( 6327)  -> cid=1831 slot=0x18B7  Mine Golem
    .hword 0x0728  @ icid=0x18B8 ( 6328)  -> cid=1832 slot=0x18B8  Monk Fighter
    .hword 0x0729  @ icid=0x18B9 ( 6329)  -> cid=1833 slot=0x18B9  Master Monk
    .hword 0x072A  @ icid=0x18BA ( 6330)  -> cid=1834 slot=0x18BA  Guardian Statue
    .hword 0x072B  @ icid=0x18BB ( 6331)  -> cid=1835 slot=0x18BB  Medusa Worm
    .hword 0x072C  @ icid=0x18BC ( 6332)  -> cid=1836 slot=0x18BC  D.D. Survivor
    .hword 0x072D  @ icid=0x18BD ( 6333)  -> cid=1837 slot=0x18BD  Mid Shield Gardna
    .hword 0x072E  @ icid=0x18BE ( 6334)  -> cid=1838 slot=0x18BE  White Ninja
    .hword 0x072F  @ icid=0x18BF ( 6335)  -> cid=1839 slot=0x18BF  Aussa the Earth Charmer
    .hword 0x0730  @ icid=0x18C0 ( 6336)  -> cid=1840 slot=0x18C0  Eria the Water Charmer
    .hword 0x0731  @ icid=0x18C1 ( 6337)  -> cid=1841 slot=0x18C1  Hiita the Fire Charmer
    .hword 0x0732  @ icid=0x18C2 ( 6338)  -> cid=1842 slot=0x18C2  Wynn the Wind Charmer
    .hword 0x0733  @ icid=0x18C3 ( 6339)  -> cid=1843 slot=0x18C3  Batteryman AA
    .hword 0x0734  @ icid=0x18C4 ( 6340)  -> cid=1844 slot=0x18C4  Des Wombat
    .hword 0x0735  @ icid=0x18C5 ( 6341)  -> cid=1845 slot=0x18C5  King of the Skull Servants
    .hword 0x0736  @ icid=0x18C6 ( 6342)  -> cid=1846 slot=0x18C6  Reshef the Dark Being
    .hword 0x0737  @ icid=0x18C7 ( 6343)  -> cid=1847 slot=0x18C7  Elemental Mistress Doriado
    .hword 0x0738  @ icid=0x18C8 ( 6344)  -> cid=1848 slot=0x18C8  Elemental Hero Flame Wingman
    .hword 0x0739  @ icid=0x18C9 ( 6345)  -> cid=1849 slot=0x18C9  Elemental Hero Thunder Giant
    .hword 0x073A  @ icid=0x18CA ( 6346)  -> cid=1850 slot=0x18CA  Gift of the Martyr
    .hword 0x073B  @ icid=0x18CB ( 6347)  -> cid=1851 slot=0x18CB  Double Attack
    .hword 0x073C  @ icid=0x18CC ( 6348)  -> cid=1852 slot=0x18CC  Battery Charger
    .hword 0x073D  @ icid=0x18CD ( 6349)  -> cid=1853 slot=0x18CD  Kaminote Blow
    .hword 0x073E  @ icid=0x18CE ( 6350)  -> cid=1854 slot=0x18CE  Doriado's Blessing
    .hword 0x073F  @ icid=0x18CF ( 6351)  -> cid=1855 slot=0x18CF  Final Ritual of the Ancients
    .hword 0x0740  @ icid=0x18D0 ( 6352)  -> cid=1856 slot=0x18D0  Legendary Black Belt
    .hword 0x0741  @ icid=0x18D1 ( 6353)  -> cid=1857 slot=0x18D1  Nitro Unit
    .hword 0x0742  @ icid=0x18D2 ( 6354)  -> cid=1858 slot=0x18D2  Shifting Shadows
    .hword 0x0743  @ icid=0x18D3 ( 6355)  -> cid=1859 slot=0x18D3  Impenetrable Formation
    .hword 0x0744  @ icid=0x18D4 ( 6356)  -> cid=1860 slot=0x18D4  Hero Signal
    .hword 0x0745  @ icid=0x18D5 ( 6357)  -> cid=1861 slot=0x18D5  Pikeru's Second Sight
    .hword 0x0746  @ icid=0x18D6 ( 6358)  -> cid=1862 slot=0x18D6  Minefield Eruption
    .hword 0x0747  @ icid=0x18D7 ( 6359)  -> cid=1863 slot=0x18D7  Kozaky's Self-Destruct Button
    .hword 0x0748  @ icid=0x18D8 ( 6360)  -> cid=1864 slot=0x18D8  Mispolymerization
    .hword 0x0749  @ icid=0x18D9 ( 6361)  -> cid=1865 slot=0x18D9  Level Conversion Lab
    .hword 0x074A  @ icid=0x18DA ( 6362)  -> cid=1866 slot=0x18DA  Rock Bombardment
    .hword 0xFFFF  @ icid=0x18DB ( 6363)  -> (none)
    .hword 0x074B  @ icid=0x18DC ( 6364)  -> cid=1867 slot=0x18DC  Token Feastevil
    .hword 0x074C  @ icid=0x18DD ( 6365)  -> cid=1868 slot=0x18DD  Spell-Stopping Statute
    .hword 0x074D  @ icid=0x18DE ( 6366)  -> cid=1869 slot=0x18DE  Royal Surrender
    .hword 0xFFFF  @ icid=0x18DF ( 6367)  -> (none)
    .hword 0x074E  @ icid=0x18E0 ( 6368)  -> cid=1870 slot=0x18E0  Infernal Flame Emperor
    .hword 0xFFFF  @ icid=0x18E1 ( 6369)  -> (none)
    .hword 0xFFFF  @ icid=0x18E2 ( 6370)  -> (none)
    .hword 0xFFFF  @ icid=0x18E3 ( 6371)  -> (none)
    .hword 0xFFFF  @ icid=0x18E4 ( 6372)  -> (none)
    .hword 0xFFFF  @ icid=0x18E5 ( 6373)  -> (none)
    .hword 0x074F  @ icid=0x18E6 ( 6374)  -> cid=1871 slot=0x18E6  Holy Knight Ishzark
    .hword 0xFFFF  @ icid=0x18E7 ( 6375)  -> (none)
    .hword 0x0750  @ icid=0x18E8 ( 6376)  -> cid=1872 slot=0x18E8  Ocean Dragon Lord - Neo-Daedalus
    .hword 0xFFFF  @ icid=0x18E9 ( 6377)  -> (none)
    .hword 0xFFFF  @ icid=0x18EA ( 6378)  -> (none)
    .hword 0xFFFF  @ icid=0x18EB ( 6379)  -> (none)
    .hword 0xFFFF  @ icid=0x18EC ( 6380)  -> (none)
    .hword 0xFFFF  @ icid=0x18ED ( 6381)  -> (none)
    .hword 0xFFFF  @ icid=0x18EE ( 6382)  -> (none)
    .hword 0x0751  @ icid=0x18EF ( 6383)  -> cid=1873 slot=0x18EF  Cycroid
    .hword 0x0752  @ icid=0x18F0 ( 6384)  -> cid=1874 slot=0x18F0  Patroid
    .hword 0x0753  @ icid=0x18F1 ( 6385)  -> cid=1875 slot=0x18F1  Gyroid
    .hword 0x0754  @ icid=0x18F2 ( 6386)  -> cid=1876 slot=0x18F2  Steamroid
    .hword 0x0755  @ icid=0x18F3 ( 6387)  -> cid=1877 slot=0x18F3  Drillroid
    .hword 0x0756  @ icid=0x18F4 ( 6388)  -> cid=1878 slot=0x18F4  UFOroid
    .hword 0x0757  @ icid=0x18F5 ( 6389)  -> cid=1879 slot=0x18F5  Jetroid
    .hword 0x0758  @ icid=0x18F6 ( 6390)  -> cid=1880 slot=0x18F6  Cyber Dragon
    .hword 0x0759  @ icid=0x18F7 ( 6391)  -> cid=1881 slot=0x18F7  Wroughtweiler
    .hword 0xFFFF  @ icid=0x18F8 ( 6392)  -> (none)
    .hword 0x075A  @ icid=0x18F9 ( 6393)  -> cid=1882 slot=0x18F9  Elemental Hero Bubbleman
    .hword 0x075B  @ icid=0x18FA ( 6394)  -> cid=1883 slot=0x18FA  Steam Gyroid
    .hword 0x075C  @ icid=0x18FB ( 6395)  -> cid=1884 slot=0x18FB  UFOroid Fighter
    .hword 0x075D  @ icid=0x18FC ( 6396)  -> cid=1885 slot=0x18FC  Cyber Twin Dragon
    .hword 0x075E  @ icid=0x18FD ( 6397)  -> cid=1886 slot=0x18FD  Cyber End Dragon
    .hword 0x075F  @ icid=0x18FE ( 6398)  -> cid=1887 slot=0x18FE  Power Bond
    .hword 0x0760  @ icid=0x18FF ( 6399)  -> cid=1888 slot=0x18FF  Skyscraper
    .hword 0x0761  @ icid=0x1900 ( 6400)  -> cid=1889 slot=0x1900  Summon Priest
    .hword 0xFFFF  @ icid=0x1901 ( 6401)  -> (none)
    .hword 0xFFFF  @ icid=0x1902 ( 6402)  -> (none)
    .hword 0xFFFF  @ icid=0x1903 ( 6403)  -> (none)
    .hword 0xFFFF  @ icid=0x1904 ( 6404)  -> (none)
    .hword 0x0762  @ icid=0x1905 ( 6405)  -> cid=1890 slot=0x1905  Dark Dreadroute
    .hword 0x0763  @ icid=0x1906 ( 6406)  -> cid=1891 slot=0x1906  Winged Kuriboh LV10
    .hword 0x0764  @ icid=0x1907 ( 6407)  -> cid=1892 slot=0x1907  Transcendent Wings
    .hword 0x0765  @ icid=0x1908 ( 6408)  -> cid=1893 slot=0x1908  Bubble Shuffle
    .hword 0x0766  @ icid=0x1909 ( 6409)  -> cid=1894 slot=0x1909  Spark Blaster
    .hword 0x0767  @ icid=0x190A ( 6410)  -> cid=1895 slot=0x190A  Dark Ruler Vandalgyon
    .hword 0x0768  @ icid=0x190B ( 6411)  -> cid=1896 slot=0x190B  Soitsu
    .hword 0x0769  @ icid=0x190C ( 6412)  -> cid=1897 slot=0x190C  Mad Lobster
    .hword 0x076A  @ icid=0x190D ( 6413)  -> cid=1898 slot=0x190D  Jerry Beans Man
    .hword 0x076B  @ icid=0x190E ( 6414)  -> cid=1899 slot=0x190E  Cybernetic Magician
    .hword 0x076C  @ icid=0x190F ( 6415)  -> cid=1900 slot=0x190F  Cybernetic Cyclopean
    .hword 0x076D  @ icid=0x1910 ( 6416)  -> cid=1901 slot=0x1910  Mechanical Hound
    .hword 0x076E  @ icid=0x1911 ( 6417)  -> cid=1902 slot=0x1911  Cyber Archfiend
    .hword 0x076F  @ icid=0x1912 ( 6418)  -> cid=1903 slot=0x1912  Goblin Elite Attack Force
    .hword 0x0770  @ icid=0x1913 ( 6419)  -> cid=1904 slot=0x1913  B.E.S. Crystal Core
    .hword 0x0771  @ icid=0x1914 ( 6420)  -> cid=1905 slot=0x1914  Giant Kozaky
    .hword 0x0772  @ icid=0x1915 ( 6421)  -> cid=1906 slot=0x1915  Indomitable Fighter Lei Lei
    .hword 0x0773  @ icid=0x1916 ( 6422)  -> cid=1907 slot=0x1916  Protective Soul Ailin
    .hword 0x0774  @ icid=0x1917 ( 6423)  -> cid=1908 slot=0x1917  Doitsu
    .hword 0x0775  @ icid=0x1918 ( 6424)  -> cid=1909 slot=0x1918  Des Frog
    .hword 0x0776  @ icid=0x1919 ( 6425)  -> cid=1910 slot=0x1919  T.A.D.P.O.L.E.
    .hword 0x0777  @ icid=0x191A ( 6426)  -> cid=1911 slot=0x191A  Poison Draw Frog
    .hword 0x0778  @ icid=0x191B ( 6427)  -> cid=1912 slot=0x191B  Tyranno Infinity
    .hword 0x0779  @ icid=0x191C ( 6428)  -> cid=1913 slot=0x191C  Batteryman C
    .hword 0x077A  @ icid=0x191D ( 6429)  -> cid=1914 slot=0x191D  Ebon Magician Curran
    .hword 0x077B  @ icid=0x191E ( 6430)  -> cid=1915 slot=0x191E  D.D.M. - Different Dimension Master
    .hword 0x077C  @ icid=0x191F ( 6431)  -> cid=1916 slot=0x191F  Fusion Recovery
    .hword 0x077D  @ icid=0x1920 ( 6432)  -> cid=1917 slot=0x1920  Miracle Fusion
    .hword 0x077E  @ icid=0x1921 ( 6433)  -> cid=1918 slot=0x1921  Dragon's Mirror
    .hword 0x077F  @ icid=0x1922 ( 6434)  -> cid=1919 slot=0x1922  System Down
    .hword 0x0780  @ icid=0x1923 ( 6435)  -> cid=1920 slot=0x1923  Des Croaking
    .hword 0x0781  @ icid=0x1924 ( 6436)  -> cid=1921 slot=0x1924  Pot of Generosity
    .hword 0x0782  @ icid=0x1925 ( 6437)  -> cid=1922 slot=0x1925  Shien's Spy
    .hword 0x0783  @ icid=0x1926 ( 6438)  -> cid=1923 slot=0x1926  Fire Darts
    .hword 0x0784  @ icid=0x1927 ( 6439)  -> cid=1924 slot=0x1927  Spiritual Earth Art - Kurogane
    .hword 0x0785  @ icid=0x1928 ( 6440)  -> cid=1925 slot=0x1928  Spiritual Water Art - Aoi
    .hword 0x0786  @ icid=0x1929 ( 6441)  -> cid=1926 slot=0x1929  Spiritual Fire Art - Kurenai
    .hword 0x0787  @ icid=0x192A ( 6442)  -> cid=1927 slot=0x192A  Spiritual Wind Art - Miyabi
    .hword 0x0788  @ icid=0x192B ( 6443)  -> cid=1928 slot=0x192B  A Rival Appears!
    .hword 0x0789  @ icid=0x192C ( 6444)  -> cid=1929 slot=0x192C  Magical Explosion
    .hword 0x078A  @ icid=0x192D ( 6445)  -> cid=1930 slot=0x192D  Rising Energy
    .hword 0x078B  @ icid=0x192E ( 6446)  -> cid=1931 slot=0x192E  D.D. Trap Hole
    .hword 0x078C  @ icid=0x192F ( 6447)  -> cid=1932 slot=0x192F  Conscription
    .hword 0x078D  @ icid=0x1930 ( 6448)  -> cid=1933 slot=0x1930  Dimension Wall
    .hword 0x078E  @ icid=0x1931 ( 6449)  -> cid=1934 slot=0x1931  Prepare to Strike Back
    .hword 0x078F  @ icid=0x1932 ( 6450)  -> cid=1935 slot=0x1932  Triage
    .hword 0xFFFF  @ icid=0x1933 ( 6451)  -> (none)
    .hword 0xFFFF  @ icid=0x1934 ( 6452)  -> (none)
    .hword 0xFFFF  @ icid=0x1935 ( 6453)  -> (none)
    .hword 0x0790  @ icid=0x1936 ( 6454)  -> cid=1936 slot=0x1936  Alkana Knight Joker
    .hword 0xFFFF  @ icid=0x1937 ( 6455)  -> (none)
    .hword 0x0791  @ icid=0x1938 ( 6456)  -> cid=1937 slot=0x1938  Gilford the Legend
    .hword 0x0792  @ icid=0x1939 ( 6457)  -> cid=1938 slot=0x1939  Warrior Lady of the Wasteland
    .hword 0x0793  @ icid=0x193A ( 6458)  -> cid=1939 slot=0x193A  Divine Sword - Phoenix Blade
    .hword 0xFFFF  @ icid=0x193B ( 6459)  -> (none)
    .hword 0xFFFF  @ icid=0x193C ( 6460)  -> (none)
    .hword 0xFFFF  @ icid=0x193D ( 6461)  -> (none)
    .hword 0xFFFF  @ icid=0x193E ( 6462)  -> (none)
    .hword 0xFFFF  @ icid=0x193F ( 6463)  -> (none)
    .hword 0xFFFF  @ icid=0x1940 ( 6464)  -> (none)
    .hword 0xFFFF  @ icid=0x1941 ( 6465)  -> (none)
    .hword 0xFFFF  @ icid=0x1942 ( 6466)  -> (none)
    .hword 0x0794  @ icid=0x1943 ( 6467)  -> cid=1940 slot=0x1943  Elemental Hero Shining Flare Wingman
    .hword 0x0795  @ icid=0x1944 ( 6468)  -> cid=1941 slot=0x1944  Level Modulation
    .hword 0x0796  @ icid=0x1945 ( 6469)  -> cid=1942 slot=0x1945  Ojamuscle
    .hword 0x0797  @ icid=0x1946 ( 6470)  -> cid=1943 slot=0x1946  Ojamagic
    .hword 0x0798  @ icid=0x1947 ( 6471)  -> cid=1944 slot=0x1947  V-Tiger Jet
    .hword 0x0799  @ icid=0x1948 ( 6472)  -> cid=1945 slot=0x1948  Blade Skater
    .hword 0x079A  @ icid=0x1949 ( 6473)  -> cid=1946 slot=0x1949  Reborn Zombie
    .hword 0xFFFF  @ icid=0x194A ( 6474)  -> (none)
    .hword 0x079B  @ icid=0x194B ( 6475)  -> cid=1947 slot=0x194B  W-Wing Catapult
    .hword 0xFFFF  @ icid=0x194C ( 6476)  -> (none)
    .hword 0x079C  @ icid=0x194D ( 6477)  -> cid=1948 slot=0x194D  Elemental Hero Bladedge
    .hword 0x079D  @ icid=0x194E ( 6478)  -> cid=1949 slot=0x194E  Elemental Hero Wildheart
    .hword 0x079E  @ icid=0x194F ( 6479)  -> cid=1950 slot=0x194F  Hydrogeddon
    .hword 0x079F  @ icid=0x1950 ( 6480)  -> cid=1951 slot=0x1950  Oxygeddon
    .hword 0x07A0  @ icid=0x1951 ( 6481)  -> cid=1952 slot=0x1951  Water Dragon
    .hword 0x07A1  @ icid=0x1952 ( 6482)  -> cid=1953 slot=0x1952  Etoile Cyber
    .hword 0x07A2  @ icid=0x1953 ( 6483)  -> cid=1954 slot=0x1953  VW-Tiger Catapult
    .hword 0x07A3  @ icid=0x1954 ( 6484)  -> cid=1955 slot=0x1954  VWXYZ-Dragon Catapult Cannon
    .hword 0x07A4  @ icid=0x1955 ( 6485)  -> cid=1956 slot=0x1955  Cyber Blader
    .hword 0x07A5  @ icid=0x1956 ( 6486)  -> cid=1957 slot=0x1956  Elemental Hero Rampart Blaster
    .hword 0x07A6  @ icid=0x1957 ( 6487)  -> cid=1958 slot=0x1957  Elemental Hero Tempest
    .hword 0x07A7  @ icid=0x1958 ( 6488)  -> cid=1959 slot=0x1958  Elemental Hero Wildedge
    .hword 0x07A8  @ icid=0x1959 ( 6489)  -> cid=1960 slot=0x1959  Chthonian Alliance
    .hword 0x082F  @ icid=0x195A ( 6490)  -> cid=2095 slot=0x195A
    .hword 0x07A9  @ icid=0x195B ( 6491)  -> cid=1961 slot=0x195B  Feather Shot
    .hword 0x07AA  @ icid=0x195C ( 6492)  -> cid=1962 slot=0x195C  Bonding - H2O
    .hword 0x07AB  @ icid=0x195D ( 6493)  -> cid=1963 slot=0x195D  Chthonian Polymer
    .hword 0x07AC  @ icid=0x195E ( 6494)  -> cid=1964 slot=0x195E  Chthonian Blast
    .hword 0x07AD  @ icid=0x195F ( 6495)  -> cid=1965 slot=0x195F  Hero Barrier
    .hword 0x07AE  @ icid=0x1960 ( 6496)  -> cid=1966 slot=0x1960  Feather Wind
    .hword 0x07AF  @ icid=0x1961 ( 6497)  -> cid=1967 slot=0x1961  Zure, Knight of Dark World
    .hword 0x07B0  @ icid=0x1962 ( 6498)  -> cid=1968 slot=0x1962  B.E.S. Tetran
    .hword 0x07B1  @ icid=0x1963 ( 6499)  -> cid=1969 slot=0x1963  Nanobreaker
    .hword 0x07B2  @ icid=0x1964 ( 6500)  -> cid=1970 slot=0x1964  Rapid-Fire Magician
    .hword 0x07B3  @ icid=0x1965 ( 6501)  -> cid=1971 slot=0x1965  Beiige, Vanguard of Dark World
    .hword 0x07B4  @ icid=0x1966 ( 6502)  -> cid=1972 slot=0x1966  Broww, Huntsman of Dark World
    .hword 0x07B5  @ icid=0x1967 ( 6503)  -> cid=1973 slot=0x1967  Brron, Mad King of Dark World
    .hword 0x07B6  @ icid=0x1968 ( 6504)  -> cid=1974 slot=0x1968  Sillva, Warlord of Dark World
    .hword 0x07B7  @ icid=0x1969 ( 6505)  -> cid=1975 slot=0x1969  Goldd, Wu-Lord of Dark World
    .hword 0x07B8  @ icid=0x196A ( 6506)  -> cid=1976 slot=0x196A  Scarr, Scout of Dark World
    .hword 0x07B9  @ icid=0x196B ( 6507)  -> cid=1977 slot=0x196B  Familiar-Possessed - Aussa
    .hword 0x07BA  @ icid=0x196C ( 6508)  -> cid=1978 slot=0x196C  Familiar-Possessed - Eria
    .hword 0x07BB  @ icid=0x196D ( 6509)  -> cid=1979 slot=0x196D  Familiar-Possessed - Hiita
    .hword 0x07BC  @ icid=0x196E ( 6510)  -> cid=1980 slot=0x196E  Familiar-Possessed - Wynn
    .hword 0x07BD  @ icid=0x196F ( 6511)  -> cid=1981 slot=0x196F  Pot of Avarice
    .hword 0x07BE  @ icid=0x1970 ( 6512)  -> cid=1982 slot=0x1970  Dark World Lightning
    .hword 0xFFFF  @ icid=0x1971 ( 6513)  -> (none)
    .hword 0x07BF  @ icid=0x1972 ( 6514)  -> cid=1983 slot=0x1972  Boss Rush
    .hword 0x07C0  @ icid=0x1973 ( 6515)  -> cid=1984 slot=0x1973  Gateway to Dark World
    .hword 0x07C1  @ icid=0x1974 ( 6516)  -> cid=1985 slot=0x1974  The Forces of Darkness
    .hword 0x07C2  @ icid=0x1975 ( 6517)  -> cid=1986 slot=0x1975  Dark Deal
    .hword 0x07C3  @ icid=0x1976 ( 6518)  -> cid=1987 slot=0x1976  Simultaneous Loss
    .hword 0x07C4  @ icid=0x1977 ( 6519)  -> cid=1988 slot=0x1977  Weed Out
    .hword 0x07C5  @ icid=0x1978 ( 6520)  -> cid=1989 slot=0x1978  The League of Uniform Nomenclature
    .hword 0x07C6  @ icid=0x1979 ( 6521)  -> cid=1990 slot=0x1979  Roll Out!
    .hword 0x07C7  @ icid=0x197A ( 6522)  -> cid=1991 slot=0x197A  Non-Fusion Area
    .hword 0x07C8  @ icid=0x197B ( 6523)  -> cid=1992 slot=0x197B  Level Limit - Area A
    .hword 0x07C9  @ icid=0x197C ( 6524)  -> cid=1993 slot=0x197C  Armed Changer
    .hword 0xFFFF  @ icid=0x197D ( 6525)  -> (none)
    .hword 0xFFFF  @ icid=0x197E ( 6526)  -> (none)
    .hword 0x07CA  @ icid=0x197F ( 6527)  -> cid=1994 slot=0x197F  Elemental Hero Necroshade
    .hword 0x07CB  @ icid=0x1980 ( 6528)  -> cid=1995 slot=0x1980  Hero Heyro
    .hword 0x07CC  @ icid=0x1981 ( 6529)  -> cid=1996 slot=0x1981  Elemental Hero Madballman
    .hword 0x07CD  @ icid=0x1982 ( 6530)  -> cid=1997 slot=0x1982  Dark Eradicator Warlock
    .hword 0x07CE  @ icid=0x1983 ( 6531)  -> cid=1998 slot=0x1983  Mythical Beast Cerberus
    .hword 0x07CF  @ icid=0x1984 ( 6532)  -> cid=1999 slot=0x1984  Magical Blast
    .hword 0xFFFF  @ icid=0x1985 ( 6533)  -> (none)
    .hword 0xFFFF  @ icid=0x1986 ( 6534)  -> (none)
    .hword 0x07D0  @ icid=0x1987 ( 6535)  -> cid=2000 slot=0x1987  Elemental Hero Steam Healer
    .hword 0x07D1  @ icid=0x1988 ( 6536)  -> cid=2001 slot=0x1988  Burst Return
    .hword 0x07D2  @ icid=0x1989 ( 6537)  -> cid=2002 slot=0x1989  Bubble Blaster
    .hword 0x07D3  @ icid=0x198A ( 6538)  -> cid=2003 slot=0x198A  Bubble Illusion
    .hword 0x07D4  @ icid=0x198B ( 6539)  -> cid=2004 slot=0x198B  Clay Charge
    .hword 0x07D5  @ icid=0x198C ( 6540)  -> cid=2005 slot=0x198C  Armed Dragon LV10
    .hword 0x07D6  @ icid=0x198D ( 6541)  -> cid=2006 slot=0x198D  Magical Mallet
    .hword 0x07D7  @ icid=0x198E ( 6542)  -> cid=2007 slot=0x198E  Inferno Reckless Summon
    .hword 0xFFFF  @ icid=0x198F ( 6543)  -> (none)
    .hword 0xFFFF  @ icid=0x1990 ( 6544)  -> (none)
    .hword 0x07D8  @ icid=0x1991 ( 6545)  -> cid=2008 slot=0x1991  Rancer Dragonute
    .hword 0x07D9  @ icid=0x1992 ( 6546)  -> cid=2009 slot=0x1992  Mistobody
    .hword 0x07DA  @ icid=0x1993 ( 6547)  -> cid=2010 slot=0x1993  Axe Dragonute
    .hword 0xFFFF  @ icid=0x1994 ( 6548)  -> (none)
    .hword 0xFFFF  @ icid=0x1995 ( 6549)  -> (none)
    .hword 0x07DB  @ icid=0x1996 ( 6550)  -> cid=2011 slot=0x1996  White Horns D.
    .hword 0xFFFF  @ icid=0x1997 ( 6551)  -> (none)
    .hword 0xFFFF  @ icid=0x1998 ( 6552)  -> (none)
    .hword 0xFFFF  @ icid=0x1999 ( 6553)  -> (none)
    .hword 0xFFFF  @ icid=0x199A ( 6554)  -> (none)
    .hword 0xFFFF  @ icid=0x199B ( 6555)  -> (none)
    .hword 0xFFFF  @ icid=0x199C ( 6556)  -> (none)
    .hword 0xFFFF  @ icid=0x199D ( 6557)  -> (none)
    .hword 0xFFFF  @ icid=0x199E ( 6558)  -> (none)
    .hword 0xFFFF  @ icid=0x199F ( 6559)  -> (none)
    .hword 0xFFFF  @ icid=0x19A0 ( 6560)  -> (none)
    .hword 0xFFFF  @ icid=0x19A1 ( 6561)  -> (none)
    .hword 0xFFFF  @ icid=0x19A2 ( 6562)  -> (none)
    .hword 0x07DC  @ icid=0x19A3 ( 6563)  -> cid=2012 slot=0x19A3  Uria, Lord of Searing Flames
    .hword 0x07DD  @ icid=0x19A4 ( 6564)  -> cid=2013 slot=0x19A4  Hamon, Lord of Striking Thunder
    .hword 0x07DE  @ icid=0x19A5 ( 6565)  -> cid=2014 slot=0x19A5  Raviel, Lord of Phantasms
    .hword 0x07DF  @ icid=0x19A6 ( 6566)  -> cid=2015 slot=0x19A6  Elemental Hero Neo Bubbleman
    .hword 0x07E0  @ icid=0x19A7 ( 6567)  -> cid=2016 slot=0x19A7  Hero Kid
    .hword 0x07E1  @ icid=0x19A8 ( 6568)  -> cid=2017 slot=0x19A8  Cyber Barrier Dragon
    .hword 0x07E2  @ icid=0x19A9 ( 6569)  -> cid=2018 slot=0x19A9  Cyber Laser Dragon
    .hword 0x07E3  @ icid=0x19AA ( 6570)  -> cid=2019 slot=0x19AA  Ancient Gear
    .hword 0x07E4  @ icid=0x19AB ( 6571)  -> cid=2020 slot=0x19AB  Hero Heart
    .hword 0x07E5  @ icid=0x19AC ( 6572)  -> cid=2021 slot=0x19AC  Magnet Circle LV2
    .hword 0xFFFF  @ icid=0x19AD ( 6573)  -> (none)
    .hword 0x07E6  @ icid=0x19AE ( 6574)  -> cid=2022 slot=0x19AE  Ancient Gear Drill
    .hword 0x07E7  @ icid=0x19AF ( 6575)  -> cid=2023 slot=0x19AF  Phantasmal Martyrs
    .hword 0x07E8  @ icid=0x19B0 ( 6576)  -> cid=2024 slot=0x19B0  Cyclone Boomerang
    .hword 0x07E9  @ icid=0x19B1 ( 6577)  -> cid=2025 slot=0x19B1  Photon Generator Unit
    .hword 0x07EA  @ icid=0x19B2 ( 6578)  -> cid=2026 slot=0x19B2  Ancient Gear Castle
    .hword 0xFFFF  @ icid=0x19B3 ( 6579)  -> (none)
    .hword 0x07EB  @ icid=0x19B4 ( 6580)  -> cid=2027 slot=0x19B4  Miracle Kids
    .hword 0x07EC  @ icid=0x19B5 ( 6581)  -> cid=2028 slot=0x19B5  Attack Reflector Unit
    .hword 0x07ED  @ icid=0x19B6 ( 6582)  -> cid=2029 slot=0x19B6  Damage Condenser
    .hword 0xFFFF  @ icid=0x19B7 ( 6583)  -> (none)
    .hword 0xFFFF  @ icid=0x19B8 ( 6584)  -> (none)
    .hword 0xFFFF  @ icid=0x19B9 ( 6585)  -> (none)
    .hword 0x0830  @ icid=0x19BA ( 6586)  -> cid=2096 slot=0x19BA
    .hword 0x07EE  @ icid=0x19BB ( 6587)  -> cid=2030 slot=0x19BB  Ancient Gear Cannon
    .hword 0x07EF  @ icid=0x19BC ( 6588)  -> cid=2031 slot=0x19BC  Proto-Cyber Dragon
    .hword 0x07F0  @ icid=0x19BD ( 6589)  -> cid=2032 slot=0x19BD  Adhesive Explosive
    .hword 0x07F1  @ icid=0x19BE ( 6590)  -> cid=2033 slot=0x19BE  Machine King Prototype
    .hword 0x07F2  @ icid=0x19BF ( 6591)  -> cid=2034 slot=0x19BF  B.E.S. Covered Core
    .hword 0x07F3  @ icid=0x19C0 ( 6592)  -> cid=2035 slot=0x19C0  D.D. Guide
    .hword 0x07F4  @ icid=0x19C1 ( 6593)  -> cid=2036 slot=0x19C1  Chain Thrasher
    .hword 0x07F5  @ icid=0x19C2 ( 6594)  -> cid=2037 slot=0x19C2  Disciple of the Forbidden Spell
    .hword 0x07F6  @ icid=0x19C3 ( 6595)  -> cid=2038 slot=0x19C3  Tenkabito Shien
    .hword 0x07F7  @ icid=0x19C4 ( 6596)  -> cid=2039 slot=0x19C4  Parasitic Ticky
    .hword 0x07F8  @ icid=0x19C5 ( 6597)  -> cid=2040 slot=0x19C5  Gokipon
    .hword 0x07F9  @ icid=0x19C6 ( 6598)  -> cid=2041 slot=0x19C6  Silent Insect
    .hword 0x07FA  @ icid=0x19C7 ( 6599)  -> cid=2042 slot=0x19C7  Chainsaw Insect
    .hword 0x07FB  @ icid=0x19C8 ( 6600)  -> cid=2043 slot=0x19C8  Anteatereatingant
    .hword 0x07FC  @ icid=0x19C9 ( 6601)  -> cid=2044 slot=0x19C9  Saber Beetle
    .hword 0x07FD  @ icid=0x19CA ( 6602)  -> cid=2045 slot=0x19CA  Doom Dozer
    .hword 0x07FE  @ icid=0x19CB ( 6603)  -> cid=2046 slot=0x19CB  Treeborn Frog
    .hword 0x07FF  @ icid=0x19CC ( 6604)  -> cid=2047 slot=0x19CC  Beelze Frog
    .hword 0x0800  @ icid=0x19CD ( 6605)  -> cid=2048 slot=0x19CD  Princess Pikeru
    .hword 0x0801  @ icid=0x19CE ( 6606)  -> cid=2049 slot=0x19CE  Princess Curran
    .hword 0x0802  @ icid=0x19CF ( 6607)  -> cid=2050 slot=0x19CF  Memory Crusher
    .hword 0x0803  @ icid=0x19D0 ( 6608)  -> cid=2051 slot=0x19D0  Malice Ascendant
    .hword 0x0804  @ icid=0x19D1 ( 6609)  -> cid=2052 slot=0x19D1  Grass Phantom
    .hword 0x0805  @ icid=0x19D2 ( 6610)  -> cid=2053 slot=0x19D2  Sand Moth
    .hword 0x0806  @ icid=0x19D3 ( 6611)  -> cid=2054 slot=0x19D3  Divine Dragon - Excelion
    .hword 0x0807  @ icid=0x19D4 ( 6612)  -> cid=2055 slot=0x19D4  Ruin, Queen of Oblivion
    .hword 0x0808  @ icid=0x19D5 ( 6613)  -> cid=2056 slot=0x19D5  Demise, King of Armageddon
    .hword 0x0809  @ icid=0x19D6 ( 6614)  -> cid=2057 slot=0x19D6  D.3.S. Frog
    .hword 0x080A  @ icid=0x19D7 ( 6615)  -> cid=2058 slot=0x19D7  Symbol of Heritage
    .hword 0x080B  @ icid=0x19D8 ( 6616)  -> cid=2059 slot=0x19D8  Trial of the Princesses
    .hword 0x080C  @ icid=0x19D9 ( 6617)  -> cid=2060 slot=0x19D9  End of the World
    .hword 0x080D  @ icid=0x19DA ( 6618)  -> cid=2061 slot=0x19DA  Samsara
    .hword 0x080E  @ icid=0x19DB ( 6619)  -> cid=2062 slot=0x19DB  Karma Cut
    .hword 0x080F  @ icid=0x19DC ( 6620)  -> cid=2063 slot=0x19DC  Next to be Lost
    .hword 0x0810  @ icid=0x19DD ( 6621)  -> cid=2064 slot=0x19DD  Generation Shift
    .hword 0x0811  @ icid=0x19DE ( 6622)  -> cid=2065 slot=0x19DE  Full Salvo
    .hword 0x0812  @ icid=0x19DF ( 6623)  -> cid=2066 slot=0x19DF  Success Probability 0%
    .hword 0x0813  @ icid=0x19E0 ( 6624)  -> cid=2067 slot=0x19E0  Option Hunter
    .hword 0x0814  @ icid=0x19E1 ( 6625)  -> cid=2068 slot=0x19E1  Goblin Out of the Frying Pan
    .hword 0x0815  @ icid=0x19E2 ( 6626)  -> cid=2069 slot=0x19E2  Malfunction
    .hword 0xFFFF  @ icid=0x19E3 ( 6627)  -> (none)
    .hword 0xFFFF  @ icid=0x19E4 ( 6628)  -> (none)
    .hword 0xFFFF  @ icid=0x19E5 ( 6629)  -> (none)
    .hword 0xFFFF  @ icid=0x19E6 ( 6630)  -> (none)
    .hword 0xFFFF  @ icid=0x19E7 ( 6631)  -> (none)
    .hword 0xFFFF  @ icid=0x19E8 ( 6632)  -> (none)
    .hword 0xFFFF  @ icid=0x19E9 ( 6633)  -> (none)
    .hword 0xFFFF  @ icid=0x19EA ( 6634)  -> (none)
    .hword 0xFFFF  @ icid=0x19EB ( 6635)  -> (none)
    .hword 0x0816  @ icid=0x19EC ( 6636)  -> cid=2070 slot=0x19EC  The Flute of Summoning Kuriboh
    .hword 0xFFFF  @ icid=0x19ED ( 6637)  -> (none)
    .hword 0x0831  @ icid=0x19EE ( 6638)  -> cid=2097 slot=0x19EE
    .hword 0x0817  @ icid=0x19EF ( 6639)  -> cid=2071 slot=0x19EF  Elemental Hero Erikshieler
    .hword 0x0818  @ icid=0x19F0 ( 6640)  -> cid=2072 slot=0x19F0  Guardian Exode
    .hword 0x0819  @ icid=0x19F1 ( 6641)  -> cid=2073 slot=0x19F1  Great Spirit
    .hword 0x081A  @ icid=0x19F2 ( 6642)  -> cid=2074 slot=0x19F2  Fault Zone
    .hword 0xFFFF  @ icid=0x19F3 ( 6643)  -> (none)
    .hword 0xFFFF  @ icid=0x19F4 ( 6644)  -> (none)
    .hword 0x081B  @ icid=0x19F5 ( 6645)  -> cid=2075 slot=0x19F5  Homunculus Gold
    .hword 0x081C  @ icid=0x19F6 ( 6646)  -> cid=2076 slot=0x19F6  The Ancient Sun Helios
    .hword 0x081D  @ icid=0x19F7 ( 6647)  -> cid=2077 slot=0x19F7  Helios Duo Megiste
    .hword 0x081E  @ icid=0x19F8 ( 6648)  -> cid=2078 slot=0x19F8  Helios Tris Megiste
    .hword 0xFFFF  @ icid=0x19F9 ( 6649)  -> (none)
    .hword 0xFFFF  @ icid=0x19FA ( 6650)  -> (none)
    .hword 0xFFFF  @ icid=0x19FB ( 6651)  -> (none)
    .hword 0xFFFF  @ icid=0x19FC ( 6652)  -> (none)
    .hword 0x081F  @ icid=0x19FD ( 6653)  -> cid=2079 slot=0x19FD  Elemental Hero Neos
    .hword 0x0820  @ icid=0x19FE ( 6654)  -> cid=2080 slot=0x19FE  Dandylion
    .hword 0xFFFF  @ icid=0x19FF ( 6655)  -> (none)
    .hword 0xFFFF  @ icid=0x1A00 ( 6656)  -> (none)
    .hword 0xFFFF  @ icid=0x1A01 ( 6657)  -> (none)
    .hword 0xFFFF  @ icid=0x1A02 ( 6658)  -> (none)
    .hword 0xFFFF  @ icid=0x1A03 ( 6659)  -> (none)
    .hword 0xFFFF  @ icid=0x1A04 ( 6660)  -> (none)
    .hword 0xFFFF  @ icid=0x1A05 ( 6661)  -> (none)
    .hword 0xFFFF  @ icid=0x1A06 ( 6662)  -> (none)
    .hword 0xFFFF  @ icid=0x1A07 ( 6663)  -> (none)
    .hword 0xFFFF  @ icid=0x1A08 ( 6664)  -> (none)
    .hword 0xFFFF  @ icid=0x1A09 ( 6665)  -> (none)
    .hword 0xFFFF  @ icid=0x1A0A ( 6666)  -> (none)
    .hword 0xFFFF  @ icid=0x1A0B ( 6667)  -> (none)
    .hword 0xFFFF  @ icid=0x1A0C ( 6668)  -> (none)
    .hword 0xFFFF  @ icid=0x1A0D ( 6669)  -> (none)
    .hword 0xFFFF  @ icid=0x1A0E ( 6670)  -> (none)
    .hword 0xFFFF  @ icid=0x1A0F ( 6671)  -> (none)
    .hword 0xFFFF  @ icid=0x1A10 ( 6672)  -> (none)
    .hword 0xFFFF  @ icid=0x1A11 ( 6673)  -> (none)
    .hword 0xFFFF  @ icid=0x1A12 ( 6674)  -> (none)
    .hword 0xFFFF  @ icid=0x1A13 ( 6675)  -> (none)
    .hword 0xFFFF  @ icid=0x1A14 ( 6676)  -> (none)
    .hword 0xFFFF  @ icid=0x1A15 ( 6677)  -> (none)
    .hword 0xFFFF  @ icid=0x1A16 ( 6678)  -> (none)
    .hword 0xFFFF  @ icid=0x1A17 ( 6679)  -> (none)
    .hword 0xFFFF  @ icid=0x1A18 ( 6680)  -> (none)
    .hword 0xFFFF  @ icid=0x1A19 ( 6681)  -> (none)
    .hword 0xFFFF  @ icid=0x1A1A ( 6682)  -> (none)
    .hword 0xFFFF  @ icid=0x1A1B ( 6683)  -> (none)
    .hword 0xFFFF  @ icid=0x1A1C ( 6684)  -> (none)
    .hword 0xFFFF  @ icid=0x1A1D ( 6685)  -> (none)
    .hword 0xFFFF  @ icid=0x1A1E ( 6686)  -> (none)
    .hword 0xFFFF  @ icid=0x1A1F ( 6687)  -> (none)
    .hword 0xFFFF  @ icid=0x1A20 ( 6688)  -> (none)
    .hword 0xFFFF  @ icid=0x1A21 ( 6689)  -> (none)
    .hword 0xFFFF  @ icid=0x1A22 ( 6690)  -> (none)
    .hword 0xFFFF  @ icid=0x1A23 ( 6691)  -> (none)
    .hword 0xFFFF  @ icid=0x1A24 ( 6692)  -> (none)
    .hword 0xFFFF  @ icid=0x1A25 ( 6693)  -> (none)
    .hword 0xFFFF  @ icid=0x1A26 ( 6694)  -> (none)
    .hword 0xFFFF  @ icid=0x1A27 ( 6695)  -> (none)
    .hword 0xFFFF  @ icid=0x1A28 ( 6696)  -> (none)
    .hword 0xFFFF  @ icid=0x1A29 ( 6697)  -> (none)
    .hword 0xFFFF  @ icid=0x1A2A ( 6698)  -> (none)
    .hword 0xFFFF  @ icid=0x1A2B ( 6699)  -> (none)
    .hword 0xFFFF  @ icid=0x1A2C ( 6700)  -> (none)
    .hword 0xFFFF  @ icid=0x1A2D ( 6701)  -> (none)
    .hword 0xFFFF  @ icid=0x1A2E ( 6702)  -> (none)
    .hword 0xFFFF  @ icid=0x1A2F ( 6703)  -> (none)
    .hword 0xFFFF  @ icid=0x1A30 ( 6704)  -> (none)
    .hword 0xFFFF  @ icid=0x1A31 ( 6705)  -> (none)
    .hword 0xFFFF  @ icid=0x1A32 ( 6706)  -> (none)
    .hword 0xFFFF  @ icid=0x1A33 ( 6707)  -> (none)
    .hword 0xFFFF  @ icid=0x1A34 ( 6708)  -> (none)
    .hword 0xFFFF  @ icid=0x1A35 ( 6709)  -> (none)
    .hword 0xFFFF  @ icid=0x1A36 ( 6710)  -> (none)
    .hword 0xFFFF  @ icid=0x1A37 ( 6711)  -> (none)
    .hword 0xFFFF  @ icid=0x1A38 ( 6712)  -> (none)
    .hword 0xFFFF  @ icid=0x1A39 ( 6713)  -> (none)
    .hword 0xFFFF  @ icid=0x1A3A ( 6714)  -> (none)
    .hword 0xFFFF  @ icid=0x1A3B ( 6715)  -> (none)
    .hword 0xFFFF  @ icid=0x1A3C ( 6716)  -> (none)
    .hword 0xFFFF  @ icid=0x1A3D ( 6717)  -> (none)
    .hword 0xFFFF  @ icid=0x1A3E ( 6718)  -> (none)
    .hword 0xFFFF  @ icid=0x1A3F ( 6719)  -> (none)
    .hword 0xFFFF  @ icid=0x1A40 ( 6720)  -> (none)
    .hword 0xFFFF  @ icid=0x1A41 ( 6721)  -> (none)
    .hword 0xFFFF  @ icid=0x1A42 ( 6722)  -> (none)
    .hword 0xFFFF  @ icid=0x1A43 ( 6723)  -> (none)
    .hword 0xFFFF  @ icid=0x1A44 ( 6724)  -> (none)
    .hword 0xFFFF  @ icid=0x1A45 ( 6725)  -> (none)
    .hword 0xFFFF  @ icid=0x1A46 ( 6726)  -> (none)
    .hword 0xFFFF  @ icid=0x1A47 ( 6727)  -> (none)
    .hword 0xFFFF  @ icid=0x1A48 ( 6728)  -> (none)
    .hword 0xFFFF  @ icid=0x1A49 ( 6729)  -> (none)
    .hword 0xFFFF  @ icid=0x1A4A ( 6730)  -> (none)
    .hword 0xFFFF  @ icid=0x1A4B ( 6731)  -> (none)
    .hword 0xFFFF  @ icid=0x1A4C ( 6732)  -> (none)
    .hword 0xFFFF  @ icid=0x1A4D ( 6733)  -> (none)
    .hword 0xFFFF  @ icid=0x1A4E ( 6734)  -> (none)
    .hword 0xFFFF  @ icid=0x1A4F ( 6735)  -> (none)
    .hword 0xFFFF  @ icid=0x1A50 ( 6736)  -> (none)
    .hword 0xFFFF  @ icid=0x1A51 ( 6737)  -> (none)
    .hword 0xFFFF  @ icid=0x1A52 ( 6738)  -> (none)
    .hword 0xFFFF  @ icid=0x1A53 ( 6739)  -> (none)
    .hword 0xFFFF  @ icid=0x1A54 ( 6740)  -> (none)
    .hword 0xFFFF  @ icid=0x1A55 ( 6741)  -> (none)
    .hword 0xFFFF  @ icid=0x1A56 ( 6742)  -> (none)
    .hword 0xFFFF  @ icid=0x1A57 ( 6743)  -> (none)
    .hword 0xFFFF  @ icid=0x1A58 ( 6744)  -> (none)
    .hword 0xFFFF  @ icid=0x1A59 ( 6745)  -> (none)
    .hword 0xFFFF  @ icid=0x1A5A ( 6746)  -> (none)
    .hword 0xFFFF  @ icid=0x1A5B ( 6747)  -> (none)
    .hword 0xFFFF  @ icid=0x1A5C ( 6748)  -> (none)
    .hword 0xFFFF  @ icid=0x1A5D ( 6749)  -> (none)
    .hword 0xFFFF  @ icid=0x1A5E ( 6750)  -> (none)
    .hword 0xFFFF  @ icid=0x1A5F ( 6751)  -> (none)
    .hword 0xFFFF  @ icid=0x1A60 ( 6752)  -> (none)
    .hword 0xFFFF  @ icid=0x1A61 ( 6753)  -> (none)
    .hword 0xFFFF  @ icid=0x1A62 ( 6754)  -> (none)
    .hword 0xFFFF  @ icid=0x1A63 ( 6755)  -> (none)
    .hword 0xFFFF  @ icid=0x1A64 ( 6756)  -> (none)
    .hword 0xFFFF  @ icid=0x1A65 ( 6757)  -> (none)
    .hword 0xFFFF  @ icid=0x1A66 ( 6758)  -> (none)
    .hword 0xFFFF  @ icid=0x1A67 ( 6759)  -> (none)
    .hword 0xFFFF  @ icid=0x1A68 ( 6760)  -> (none)
    .hword 0xFFFF  @ icid=0x1A69 ( 6761)  -> (none)
    .hword 0xFFFF  @ icid=0x1A6A ( 6762)  -> (none)
    .hword 0xFFFF  @ icid=0x1A6B ( 6763)  -> (none)
    .hword 0xFFFF  @ icid=0x1A6C ( 6764)  -> (none)
    .hword 0xFFFF  @ icid=0x1A6D ( 6765)  -> (none)
    .hword 0xFFFF  @ icid=0x1A6E ( 6766)  -> (none)
    .hword 0xFFFF  @ icid=0x1A6F ( 6767)  -> (none)
    .hword 0xFFFF  @ icid=0x1A70 ( 6768)  -> (none)
    .hword 0xFFFF  @ icid=0x1A71 ( 6769)  -> (none)
    .hword 0xFFFF  @ icid=0x1A72 ( 6770)  -> (none)
    .hword 0xFFFF  @ icid=0x1A73 ( 6771)  -> (none)
    .hword 0xFFFF  @ icid=0x1A74 ( 6772)  -> (none)
    .hword 0xFFFF  @ icid=0x1A75 ( 6773)  -> (none)
    .hword 0xFFFF  @ icid=0x1A76 ( 6774)  -> (none)
    .hword 0xFFFF  @ icid=0x1A77 ( 6775)  -> (none)
    .hword 0xFFFF  @ icid=0x1A78 ( 6776)  -> (none)
    .hword 0xFFFF  @ icid=0x1A79 ( 6777)  -> (none)
    .hword 0xFFFF  @ icid=0x1A7A ( 6778)  -> (none)
    .hword 0xFFFF  @ icid=0x1A7B ( 6779)  -> (none)
    .hword 0xFFFF  @ icid=0x1A7C ( 6780)  -> (none)
    .hword 0xFFFF  @ icid=0x1A7D ( 6781)  -> (none)
    .hword 0xFFFF  @ icid=0x1A7E ( 6782)  -> (none)
    .hword 0xFFFF  @ icid=0x1A7F ( 6783)  -> (none)
    .hword 0xFFFF  @ icid=0x1A80 ( 6784)  -> (none)
    .hword 0xFFFF  @ icid=0x1A81 ( 6785)  -> (none)
    .hword 0xFFFF  @ icid=0x1A82 ( 6786)  -> (none)
    .hword 0xFFFF  @ icid=0x1A83 ( 6787)  -> (none)
    .hword 0xFFFF  @ icid=0x1A84 ( 6788)  -> (none)
    .hword 0xFFFF  @ icid=0x1A85 ( 6789)  -> (none)
    .hword 0xFFFF  @ icid=0x1A86 ( 6790)  -> (none)
    .hword 0xFFFF  @ icid=0x1A87 ( 6791)  -> (none)
    .hword 0xFFFF  @ icid=0x1A88 ( 6792)  -> (none)
    .hword 0xFFFF  @ icid=0x1A89 ( 6793)  -> (none)
    .hword 0xFFFF  @ icid=0x1A8A ( 6794)  -> (none)
    .hword 0xFFFF  @ icid=0x1A8B ( 6795)  -> (none)
    .hword 0xFFFF  @ icid=0x1A8C ( 6796)  -> (none)
    .hword 0xFFFF  @ icid=0x1A8D ( 6797)  -> (none)
    .hword 0xFFFF  @ icid=0x1A8E ( 6798)  -> (none)
    .hword 0xFFFF  @ icid=0x1A8F ( 6799)  -> (none)
    .hword 0xFFFF  @ icid=0x1A90 ( 6800)  -> (none)
    .hword 0xFFFF  @ icid=0x1A91 ( 6801)  -> (none)
    .hword 0xFFFF  @ icid=0x1A92 ( 6802)  -> (none)
    .hword 0xFFFF  @ icid=0x1A93 ( 6803)  -> (none)
    .hword 0xFFFF  @ icid=0x1A94 ( 6804)  -> (none)
    .hword 0xFFFF  @ icid=0x1A95 ( 6805)  -> (none)
    .hword 0xFFFF  @ icid=0x1A96 ( 6806)  -> (none)
    .hword 0xFFFF  @ icid=0x1A97 ( 6807)  -> (none)
    .hword 0xFFFF  @ icid=0x1A98 ( 6808)  -> (none)
    .hword 0xFFFF  @ icid=0x1A99 ( 6809)  -> (none)
    .hword 0xFFFF  @ icid=0x1A9A ( 6810)  -> (none)
    .hword 0xFFFF  @ icid=0x1A9B ( 6811)  -> (none)
    .hword 0xFFFF  @ icid=0x1A9C ( 6812)  -> (none)
    .hword 0xFFFF  @ icid=0x1A9D ( 6813)  -> (none)
    .hword 0xFFFF  @ icid=0x1A9E ( 6814)  -> (none)
    .hword 0xFFFF  @ icid=0x1A9F ( 6815)  -> (none)
    .hword 0xFFFF  @ icid=0x1AA0 ( 6816)  -> (none)
    .hword 0xFFFF  @ icid=0x1AA1 ( 6817)  -> (none)
    .hword 0xFFFF  @ icid=0x1AA2 ( 6818)  -> (none)
    .hword 0xFFFF  @ icid=0x1AA3 ( 6819)  -> (none)
    .hword 0xFFFF  @ icid=0x1AA4 ( 6820)  -> (none)
    .hword 0xFFFF  @ icid=0x1AA5 ( 6821)  -> (none)
    .hword 0xFFFF  @ icid=0x1AA6 ( 6822)  -> (none)
    .hword 0xFFFF  @ icid=0x1AA7 ( 6823)  -> (none)
    .hword 0xFFFF  @ icid=0x1AA8 ( 6824)  -> (none)
    .hword 0xFFFF  @ icid=0x1AA9 ( 6825)  -> (none)
    .hword 0xFFFF  @ icid=0x1AAA ( 6826)  -> (none)
    .hword 0xFFFF  @ icid=0x1AAB ( 6827)  -> (none)
    .hword 0xFFFF  @ icid=0x1AAC ( 6828)  -> (none)
    .hword 0xFFFF  @ icid=0x1AAD ( 6829)  -> (none)
    .hword 0xFFFF  @ icid=0x1AAE ( 6830)  -> (none)
    .hword 0xFFFF  @ icid=0x1AAF ( 6831)  -> (none)
    .hword 0xFFFF  @ icid=0x1AB0 ( 6832)  -> (none)
    .hword 0xFFFF  @ icid=0x1AB1 ( 6833)  -> (none)
    .hword 0xFFFF  @ icid=0x1AB2 ( 6834)  -> (none)
    .hword 0xFFFF  @ icid=0x1AB3 ( 6835)  -> (none)
    .hword 0xFFFF  @ icid=0x1AB4 ( 6836)  -> (none)
    .hword 0xFFFF  @ icid=0x1AB5 ( 6837)  -> (none)
    .hword 0xFFFF  @ icid=0x1AB6 ( 6838)  -> (none)
    .hword 0xFFFF  @ icid=0x1AB7 ( 6839)  -> (none)
    .hword 0xFFFF  @ icid=0x1AB8 ( 6840)  -> (none)
    .hword 0xFFFF  @ icid=0x1AB9 ( 6841)  -> (none)
    .hword 0xFFFF  @ icid=0x1ABA ( 6842)  -> (none)
    .hword 0xFFFF  @ icid=0x1ABB ( 6843)  -> (none)
    .hword 0xFFFF  @ icid=0x1ABC ( 6844)  -> (none)
    .hword 0xFFFF  @ icid=0x1ABD ( 6845)  -> (none)
    .hword 0xFFFF  @ icid=0x1ABE ( 6846)  -> (none)
    .hword 0xFFFF  @ icid=0x1ABF ( 6847)  -> (none)
    .hword 0xFFFF  @ icid=0x1AC0 ( 6848)  -> (none)
    .hword 0xFFFF  @ icid=0x1AC1 ( 6849)  -> (none)
    .hword 0xFFFF  @ icid=0x1AC2 ( 6850)  -> (none)
    .hword 0xFFFF  @ icid=0x1AC3 ( 6851)  -> (none)
    .hword 0xFFFF  @ icid=0x1AC4 ( 6852)  -> (none)
    .hword 0xFFFF  @ icid=0x1AC5 ( 6853)  -> (none)
    .hword 0xFFFF  @ icid=0x1AC6 ( 6854)  -> (none)
    .hword 0xFFFF  @ icid=0x1AC7 ( 6855)  -> (none)
    .hword 0xFFFF  @ icid=0x1AC8 ( 6856)  -> (none)
    .hword 0xFFFF  @ icid=0x1AC9 ( 6857)  -> (none)
    .hword 0xFFFF  @ icid=0x1ACA ( 6858)  -> (none)
    .hword 0xFFFF  @ icid=0x1ACB ( 6859)  -> (none)
    .hword 0xFFFF  @ icid=0x1ACC ( 6860)  -> (none)
    .hword 0xFFFF  @ icid=0x1ACD ( 6861)  -> (none)
    .hword 0xFFFF  @ icid=0x1ACE ( 6862)  -> (none)
    .hword 0xFFFF  @ icid=0x1ACF ( 6863)  -> (none)
    .hword 0xFFFF  @ icid=0x1AD0 ( 6864)  -> (none)
    .hword 0xFFFF  @ icid=0x1AD1 ( 6865)  -> (none)
    .hword 0xFFFF  @ icid=0x1AD2 ( 6866)  -> (none)
    .hword 0xFFFF  @ icid=0x1AD3 ( 6867)  -> (none)
    .hword 0xFFFF  @ icid=0x1AD4 ( 6868)  -> (none)
    .hword 0xFFFF  @ icid=0x1AD5 ( 6869)  -> (none)
    .hword 0xFFFF  @ icid=0x1AD6 ( 6870)  -> (none)
    .hword 0xFFFF  @ icid=0x1AD7 ( 6871)  -> (none)
    .hword 0xFFFF  @ icid=0x1AD8 ( 6872)  -> (none)
    .hword 0xFFFF  @ icid=0x1AD9 ( 6873)  -> (none)
    .hword 0xFFFF  @ icid=0x1ADA ( 6874)  -> (none)
    .hword 0xFFFF  @ icid=0x1ADB ( 6875)  -> (none)
    .hword 0xFFFF  @ icid=0x1ADC ( 6876)  -> (none)
    .hword 0xFFFF  @ icid=0x1ADD ( 6877)  -> (none)
    .hword 0xFFFF  @ icid=0x1ADE ( 6878)  -> (none)
    .hword 0xFFFF  @ icid=0x1ADF ( 6879)  -> (none)
    .hword 0xFFFF  @ icid=0x1AE0 ( 6880)  -> (none)
    .hword 0xFFFF  @ icid=0x1AE1 ( 6881)  -> (none)
    .hword 0xFFFF  @ icid=0x1AE2 ( 6882)  -> (none)
    .hword 0xFFFF  @ icid=0x1AE3 ( 6883)  -> (none)
    .hword 0xFFFF  @ icid=0x1AE4 ( 6884)  -> (none)
    .hword 0xFFFF  @ icid=0x1AE5 ( 6885)  -> (none)
    .hword 0xFFFF  @ icid=0x1AE6 ( 6886)  -> (none)
    .hword 0xFFFF  @ icid=0x1AE7 ( 6887)  -> (none)
    .hword 0xFFFF  @ icid=0x1AE8 ( 6888)  -> (none)
    .hword 0xFFFF  @ icid=0x1AE9 ( 6889)  -> (none)
    .hword 0xFFFF  @ icid=0x1AEA ( 6890)  -> (none)
    .hword 0xFFFF  @ icid=0x1AEB ( 6891)  -> (none)
    .hword 0xFFFF  @ icid=0x1AEC ( 6892)  -> (none)
    .hword 0xFFFF  @ icid=0x1AED ( 6893)  -> (none)
    .hword 0xFFFF  @ icid=0x1AEE ( 6894)  -> (none)
    .hword 0xFFFF  @ icid=0x1AEF ( 6895)  -> (none)
    .hword 0xFFFF  @ icid=0x1AF0 ( 6896)  -> (none)
    .hword 0xFFFF  @ icid=0x1AF1 ( 6897)  -> (none)
    .hword 0xFFFF  @ icid=0x1AF2 ( 6898)  -> (none)
    .hword 0xFFFF  @ icid=0x1AF3 ( 6899)  -> (none)
    .hword 0xFFFF  @ icid=0x1AF4 ( 6900)  -> (none)
    .hword 0xFFFF  @ icid=0x1AF5 ( 6901)  -> (none)
    .hword 0xFFFF  @ icid=0x1AF6 ( 6902)  -> (none)
    .hword 0xFFFF  @ icid=0x1AF7 ( 6903)  -> (none)
    .hword 0xFFFF  @ icid=0x1AF8 ( 6904)  -> (none)
    .hword 0xFFFF  @ icid=0x1AF9 ( 6905)  -> (none)
    .hword 0xFFFF  @ icid=0x1AFA ( 6906)  -> (none)
    .hword 0xFFFF  @ icid=0x1AFB ( 6907)  -> (none)
    .hword 0xFFFF  @ icid=0x1AFC ( 6908)  -> (none)
    .hword 0xFFFF  @ icid=0x1AFD ( 6909)  -> (none)
    .hword 0xFFFF  @ icid=0x1AFE ( 6910)  -> (none)
    .hword 0xFFFF  @ icid=0x1AFF ( 6911)  -> (none)
    .hword 0xFFFF  @ icid=0x1B00 ( 6912)  -> (none)
    .hword 0xFFFF  @ icid=0x1B01 ( 6913)  -> (none)
    .hword 0xFFFF  @ icid=0x1B02 ( 6914)  -> (none)
    .hword 0xFFFF  @ icid=0x1B03 ( 6915)  -> (none)
    .hword 0xFFFF  @ icid=0x1B04 ( 6916)  -> (none)
    .hword 0xFFFF  @ icid=0x1B05 ( 6917)  -> (none)
    .hword 0xFFFF  @ icid=0x1B06 ( 6918)  -> (none)
    .hword 0xFFFF  @ icid=0x1B07 ( 6919)  -> (none)
    .hword 0xFFFF  @ icid=0x1B08 ( 6920)  -> (none)
    .hword 0xFFFF  @ icid=0x1B09 ( 6921)  -> (none)
    .hword 0xFFFF  @ icid=0x1B0A ( 6922)  -> (none)
    .hword 0xFFFF  @ icid=0x1B0B ( 6923)  -> (none)
    .hword 0xFFFF  @ icid=0x1B0C ( 6924)  -> (none)
    .hword 0xFFFF  @ icid=0x1B0D ( 6925)  -> (none)
    .hword 0xFFFF  @ icid=0x1B0E ( 6926)  -> (none)
    .hword 0xFFFF  @ icid=0x1B0F ( 6927)  -> (none)
    .hword 0xFFFF  @ icid=0x1B10 ( 6928)  -> (none)
    .hword 0xFFFF  @ icid=0x1B11 ( 6929)  -> (none)
    .hword 0xFFFF  @ icid=0x1B12 ( 6930)  -> (none)
    .hword 0xFFFF  @ icid=0x1B13 ( 6931)  -> (none)
    .hword 0xFFFF  @ icid=0x1B14 ( 6932)  -> (none)
    .hword 0xFFFF  @ icid=0x1B15 ( 6933)  -> (none)
    .hword 0xFFFF  @ icid=0x1B16 ( 6934)  -> (none)
    .hword 0xFFFF  @ icid=0x1B17 ( 6935)  -> (none)
    .hword 0xFFFF  @ icid=0x1B18 ( 6936)  -> (none)
    .hword 0xFFFF  @ icid=0x1B19 ( 6937)  -> (none)
    .hword 0xFFFF  @ icid=0x1B1A ( 6938)  -> (none)
    .hword 0xFFFF  @ icid=0x1B1B ( 6939)  -> (none)
    .hword 0xFFFF  @ icid=0x1B1C ( 6940)  -> (none)
    .hword 0xFFFF  @ icid=0x1B1D ( 6941)  -> (none)
    .hword 0xFFFF  @ icid=0x1B1E ( 6942)  -> (none)
    .hword 0xFFFF  @ icid=0x1B1F ( 6943)  -> (none)
    .hword 0xFFFF  @ icid=0x1B20 ( 6944)  -> (none)
    .hword 0xFFFF  @ icid=0x1B21 ( 6945)  -> (none)
    .hword 0xFFFF  @ icid=0x1B22 ( 6946)  -> (none)
    .hword 0xFFFF  @ icid=0x1B23 ( 6947)  -> (none)
    .hword 0xFFFF  @ icid=0x1B24 ( 6948)  -> (none)
    .hword 0xFFFF  @ icid=0x1B25 ( 6949)  -> (none)
    .hword 0xFFFF  @ icid=0x1B26 ( 6950)  -> (none)
    .hword 0xFFFF  @ icid=0x1B27 ( 6951)  -> (none)
    .hword 0xFFFF  @ icid=0x1B28 ( 6952)  -> (none)
    .hword 0xFFFF  @ icid=0x1B29 ( 6953)  -> (none)
    .hword 0xFFFF  @ icid=0x1B2A ( 6954)  -> (none)
    .hword 0xFFFF  @ icid=0x1B2B ( 6955)  -> (none)
    .hword 0xFFFF  @ icid=0x1B2C ( 6956)  -> (none)
    .hword 0xFFFF  @ icid=0x1B2D ( 6957)  -> (none)
    .hword 0xFFFF  @ icid=0x1B2E ( 6958)  -> (none)
    .hword 0xFFFF  @ icid=0x1B2F ( 6959)  -> (none)
    .hword 0xFFFF  @ icid=0x1B30 ( 6960)  -> (none)
    .hword 0xFFFF  @ icid=0x1B31 ( 6961)  -> (none)
    .hword 0xFFFF  @ icid=0x1B32 ( 6962)  -> (none)
    .hword 0xFFFF  @ icid=0x1B33 ( 6963)  -> (none)
    .hword 0xFFFF  @ icid=0x1B34 ( 6964)  -> (none)
    .hword 0xFFFF  @ icid=0x1B35 ( 6965)  -> (none)
    .hword 0xFFFF  @ icid=0x1B36 ( 6966)  -> (none)
    .hword 0xFFFF  @ icid=0x1B37 ( 6967)  -> (none)
    .hword 0xFFFF  @ icid=0x1B38 ( 6968)  -> (none)
    .hword 0xFFFF  @ icid=0x1B39 ( 6969)  -> (none)
    .hword 0xFFFF  @ icid=0x1B3A ( 6970)  -> (none)
    .hword 0xFFFF  @ icid=0x1B3B ( 6971)  -> (none)
    .hword 0xFFFF  @ icid=0x1B3C ( 6972)  -> (none)
    .hword 0xFFFF  @ icid=0x1B3D ( 6973)  -> (none)
    .hword 0xFFFF  @ icid=0x1B3E ( 6974)  -> (none)
    .hword 0xFFFF  @ icid=0x1B3F ( 6975)  -> (none)
    .hword 0xFFFF  @ icid=0x1B40 ( 6976)  -> (none)
    .hword 0xFFFF  @ icid=0x1B41 ( 6977)  -> (none)
    .hword 0xFFFF  @ icid=0x1B42 ( 6978)  -> (none)
    .hword 0xFFFF  @ icid=0x1B43 ( 6979)  -> (none)
    .hword 0xFFFF  @ icid=0x1B44 ( 6980)  -> (none)
    .hword 0xFFFF  @ icid=0x1B45 ( 6981)  -> (none)
    .hword 0xFFFF  @ icid=0x1B46 ( 6982)  -> (none)
    .hword 0xFFFF  @ icid=0x1B47 ( 6983)  -> (none)
    .hword 0xFFFF  @ icid=0x1B48 ( 6984)  -> (none)
    .hword 0xFFFF  @ icid=0x1B49 ( 6985)  -> (none)
    .hword 0xFFFF  @ icid=0x1B4A ( 6986)  -> (none)
    .hword 0xFFFF  @ icid=0x1B4B ( 6987)  -> (none)
    .hword 0xFFFF  @ icid=0x1B4C ( 6988)  -> (none)
    .hword 0xFFFF  @ icid=0x1B4D ( 6989)  -> (none)
    .hword 0xFFFF  @ icid=0x1B4E ( 6990)  -> (none)
    .hword 0xFFFF  @ icid=0x1B4F ( 6991)  -> (none)
    .hword 0xFFFF  @ icid=0x1B50 ( 6992)  -> (none)
    .hword 0xFFFF  @ icid=0x1B51 ( 6993)  -> (none)
    .hword 0xFFFF  @ icid=0x1B52 ( 6994)  -> (none)
    .hword 0xFFFF  @ icid=0x1B53 ( 6995)  -> (none)
    .hword 0xFFFF  @ icid=0x1B54 ( 6996)  -> (none)
    .hword 0xFFFF  @ icid=0x1B55 ( 6997)  -> (none)
    .hword 0xFFFF  @ icid=0x1B56 ( 6998)  -> (none)
    .hword 0xFFFF  @ icid=0x1B57 ( 6999)  -> (none)
    .hword 0xFFFF  @ icid=0x1B58 ( 7000)  -> (none)
    .hword 0xFFFF  @ icid=0x1B59 ( 7001)  -> (none)
    .hword 0xFFFF  @ icid=0x1B5A ( 7002)  -> (none)
    .hword 0xFFFF  @ icid=0x1B5B ( 7003)  -> (none)
    .hword 0xFFFF  @ icid=0x1B5C ( 7004)  -> (none)
    .hword 0xFFFF  @ icid=0x1B5D ( 7005)  -> (none)
    .hword 0xFFFF  @ icid=0x1B5E ( 7006)  -> (none)
    .hword 0xFFFF  @ icid=0x1B5F ( 7007)  -> (none)
    .hword 0xFFFF  @ icid=0x1B60 ( 7008)  -> (none)
    .hword 0xFFFF  @ icid=0x1B61 ( 7009)  -> (none)
    .hword 0xFFFF  @ icid=0x1B62 ( 7010)  -> (none)
    .hword 0xFFFF  @ icid=0x1B63 ( 7011)  -> (none)
    .hword 0xFFFF  @ icid=0x1B64 ( 7012)  -> (none)
    .hword 0xFFFF  @ icid=0x1B65 ( 7013)  -> (none)
    .hword 0xFFFF  @ icid=0x1B66 ( 7014)  -> (none)
    .hword 0xFFFF  @ icid=0x1B67 ( 7015)  -> (none)
    .hword 0xFFFF  @ icid=0x1B68 ( 7016)  -> (none)
    .hword 0xFFFF  @ icid=0x1B69 ( 7017)  -> (none)
    .hword 0xFFFF  @ icid=0x1B6A ( 7018)  -> (none)
    .hword 0xFFFF  @ icid=0x1B6B ( 7019)  -> (none)
    .hword 0xFFFF  @ icid=0x1B6C ( 7020)  -> (none)
    .hword 0xFFFF  @ icid=0x1B6D ( 7021)  -> (none)
    .hword 0xFFFF  @ icid=0x1B6E ( 7022)  -> (none)
    .hword 0xFFFF  @ icid=0x1B6F ( 7023)  -> (none)
    .hword 0xFFFF  @ icid=0x1B70 ( 7024)  -> (none)
    .hword 0xFFFF  @ icid=0x1B71 ( 7025)  -> (none)
    .hword 0xFFFF  @ icid=0x1B72 ( 7026)  -> (none)
    .hword 0xFFFF  @ icid=0x1B73 ( 7027)  -> (none)
    .hword 0xFFFF  @ icid=0x1B74 ( 7028)  -> (none)
    .hword 0xFFFF  @ icid=0x1B75 ( 7029)  -> (none)
    .hword 0xFFFF  @ icid=0x1B76 ( 7030)  -> (none)
    .hword 0xFFFF  @ icid=0x1B77 ( 7031)  -> (none)
    .hword 0xFFFF  @ icid=0x1B78 ( 7032)  -> (none)
    .hword 0xFFFF  @ icid=0x1B79 ( 7033)  -> (none)
    .hword 0xFFFF  @ icid=0x1B7A ( 7034)  -> (none)
    .hword 0xFFFF  @ icid=0x1B7B ( 7035)  -> (none)
    .hword 0xFFFF  @ icid=0x1B7C ( 7036)  -> (none)
    .hword 0xFFFF  @ icid=0x1B7D ( 7037)  -> (none)
    .hword 0xFFFF  @ icid=0x1B7E ( 7038)  -> (none)
    .hword 0xFFFF  @ icid=0x1B7F ( 7039)  -> (none)
    .hword 0xFFFF  @ icid=0x1B80 ( 7040)  -> (none)
    .hword 0xFFFF  @ icid=0x1B81 ( 7041)  -> (none)
    .hword 0xFFFF  @ icid=0x1B82 ( 7042)  -> (none)
    .hword 0xFFFF  @ icid=0x1B83 ( 7043)  -> (none)
    .hword 0xFFFF  @ icid=0x1B84 ( 7044)  -> (none)
    .hword 0xFFFF  @ icid=0x1B85 ( 7045)  -> (none)
    .hword 0xFFFF  @ icid=0x1B86 ( 7046)  -> (none)
    .hword 0xFFFF  @ icid=0x1B87 ( 7047)  -> (none)
    .hword 0xFFFF  @ icid=0x1B88 ( 7048)  -> (none)
    .hword 0xFFFF  @ icid=0x1B89 ( 7049)  -> (none)
    .hword 0xFFFF  @ icid=0x1B8A ( 7050)  -> (none)
    .hword 0xFFFF  @ icid=0x1B8B ( 7051)  -> (none)
    .hword 0xFFFF  @ icid=0x1B8C ( 7052)  -> (none)
    .hword 0xFFFF  @ icid=0x1B8D ( 7053)  -> (none)
    .hword 0xFFFF  @ icid=0x1B8E ( 7054)  -> (none)
    .hword 0xFFFF  @ icid=0x1B8F ( 7055)  -> (none)
    .hword 0xFFFF  @ icid=0x1B90 ( 7056)  -> (none)
    .hword 0xFFFF  @ icid=0x1B91 ( 7057)  -> (none)
    .hword 0xFFFF  @ icid=0x1B92 ( 7058)  -> (none)
    .hword 0xFFFF  @ icid=0x1B93 ( 7059)  -> (none)
    .hword 0xFFFF  @ icid=0x1B94 ( 7060)  -> (none)
    .hword 0xFFFF  @ icid=0x1B95 ( 7061)  -> (none)
    .hword 0xFFFF  @ icid=0x1B96 ( 7062)  -> (none)
    .hword 0xFFFF  @ icid=0x1B97 ( 7063)  -> (none)
    .hword 0xFFFF  @ icid=0x1B98 ( 7064)  -> (none)
    .hword 0xFFFF  @ icid=0x1B99 ( 7065)  -> (none)
    .hword 0xFFFF  @ icid=0x1B9A ( 7066)  -> (none)
    .hword 0xFFFF  @ icid=0x1B9B ( 7067)  -> (none)
    .hword 0xFFFF  @ icid=0x1B9C ( 7068)  -> (none)
    .hword 0xFFFF  @ icid=0x1B9D ( 7069)  -> (none)
    .hword 0xFFFF  @ icid=0x1B9E ( 7070)  -> (none)
    .hword 0xFFFF  @ icid=0x1B9F ( 7071)  -> (none)
    .hword 0xFFFF  @ icid=0x1BA0 ( 7072)  -> (none)
    .hword 0xFFFF  @ icid=0x1BA1 ( 7073)  -> (none)
    .hword 0xFFFF  @ icid=0x1BA2 ( 7074)  -> (none)
    .hword 0xFFFF  @ icid=0x1BA3 ( 7075)  -> (none)
    .hword 0xFFFF  @ icid=0x1BA4 ( 7076)  -> (none)
    .hword 0xFFFF  @ icid=0x1BA5 ( 7077)  -> (none)
    .hword 0xFFFF  @ icid=0x1BA6 ( 7078)  -> (none)

cards_ids_array_end:

