RomHeaderNintendoLogo:
	.incbin "roms/2343.gba", 0x4, 0xA0 - 0x4

@ 游戏标题，固定长度 12 字节
RomHeaderGameTitle:
	.string "YUGIOHWCT06"

@ 游戏代码，固定长度 4 字节
RomHeaderGameCode:
	.ascii "BY6E"

@ 制造商代码，固定长度 2 字节
RomHeaderMakerCode:
	.ascii "A4"

@ 固定值 0x96，表示 GBA ROM
RomHeaderMagic:
	.byte 0x96

RomHeaderMainUnitCode:
	.byte 0

RomHeaderDeviceType:
	.byte 0

RomHeaderReserved1:
	.rept 7
	.byte 0
	.endr

RomHeaderSoftwareVersion:
	.byte 0

RomHeaderChecksum:
	.byte 0x9D

RomHeaderReserved2:
	.rept 2
	.byte 0
	.endr
