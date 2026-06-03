@ ==== 24_libc_runtime.s ====
@ 编译器运行时 (__muldi3/__negdi2/_sbrk 等 newlib/libgcc)
.thumb
__submore:
    push {r4,r5,r6,r7,lr}                    @ 08110dc8 f0b5
    .hword 0x4647    @ 08110dca 4746
    push {r7}                                @ 08110dcc 80b4
    adds r7,r0,#0x0    @ 08110dce 071c
    adds r0,#0x40    @ 08110dd0 4030
    ldr r4,[r7,#0x30]                        @ 08110dd2 3c6b
    cmp r4,r0                                @ 08110dd4 8442
    bne LAB_08110e10                         @ 08110dd6 1bd1
    ldr r0,[r7,#0x54]                        @ 08110dd8 786d
    movs r6,#0x80    @ 08110dda 8026
    lsls r6,r6,#0x3    @ 08110ddc f600
    adds r1,r6,#0x0    @ 08110dde 311c
    bl _malloc_r                             @ 08110de0 00f016fc
    adds r5,r0,#0x0    @ 08110de4 051c
    cmp r5,#0x0                              @ 08110de6 002d
    beq LAB_08110e3e                         @ 08110de8 29d0
    str r5,[r7,#0x30]                        @ 08110dea 3d63
    str r6,[r7,#0x34]                        @ 08110dec 7e63
    ldr r0, DAT_08110e0c                     @ 08110dee 0748
    adds r5,r5,r0    @ 08110df0 2d18
    movs r6,#0x2    @ 08110df2 0226
    adds r2,r4,#0x0    @ 08110df4 221c
LAB_08110df6:
    adds r0,r5,r6    @ 08110df6 a819
    adds r1,r2,r6    @ 08110df8 9119
    ldrb r1,[r1,#0x0]                        @ 08110dfa 0978
    strb r1,[r0,#0x0]                        @ 08110dfc 0170
    subs r6,#0x1    @ 08110dfe 013e
    cmp r6,#0x0                              @ 08110e00 002e
    bge LAB_08110df6                         @ 08110e02 f8da
    str r5,[r7,#0x0]                         @ 08110e04 3d60
    movs r0,#0x0    @ 08110e06 0020
    b LAB_08110e42                           @ 08110e08 1be0
    .zero  0x2
DAT_08110e0c:
    .word  0x000003fd                     @ 08110e0c fd030000
LAB_08110e10:
    ldr r6,[r7,#0x34]                        @ 08110e10 7e6b
    ldr r0,[r7,#0x54]                        @ 08110e12 786d
    lsls r1,r6,#0x1    @ 08110e14 7100
    .hword 0x4688    @ 08110e16 8846
    adds r1,r4,#0x0    @ 08110e18 211c
    .hword 0x4642    @ 08110e1a 4246
    bl _realloc_r                            @ 08110e1c 01f044fa
    adds r5,r0,#0x0    @ 08110e20 051c
    cmp r5,#0x0                              @ 08110e22 002d
    beq LAB_08110e3e                         @ 08110e24 0bd0
    adds r4,r5,r6    @ 08110e26 ac19
    adds r0,r4,#0x0    @ 08110e28 201c
    adds r1,r5,#0x0    @ 08110e2a 291c
    adds r2,r6,#0x0    @ 08110e2c 321c
    bl memcpy                                @ 08110e2e fdf795fd
    str r4,[r7,#0x0]                         @ 08110e32 3c60
    str r5,[r7,#0x30]                        @ 08110e34 3d63
    .hword 0x4640    @ 08110e36 4046
    str r0,[r7,#0x34]                        @ 08110e38 7863
    movs r0,#0x0    @ 08110e3a 0020
    b LAB_08110e42                           @ 08110e3c 01e0
LAB_08110e3e:
    movs r0,#0x1    @ 08110e3e 0120
    rsbs r0,r0,#0    @ 08110e40 4042
LAB_08110e42:
    pop {r3}                                 @ 08110e42 08bc
    .hword 0x4698    @ 08110e44 9846
    pop {r4,r5,r6,r7,pc}                     @ 08110e46 f0bd
ungetc:
    push {r4,r5,r6,lr}                       @ 08110e48 70b5
    adds r5,r0,#0x0    @ 08110e4a 051c
    adds r4,r1,#0x0    @ 08110e4c 0c1c
    movs r6,#0x1    @ 08110e4e 0126
    rsbs r6,r6,#0    @ 08110e50 7642
    cmp r5,r6                                @ 08110e52 b542
    beq LAB_08110f24                         @ 08110e54 66d0
    ldr r0,[r4,#0x54]                        @ 08110e56 606d
    cmp r0,#0x0                              @ 08110e58 0028
    bne LAB_08110e62                         @ 08110e5a 02d1
    ldr r0, DAT_08110ed8                     @ 08110e5c 1e48
    ldr r0,[r0,#0x0]                         @ 08110e5e 0068
    str r0,[r4,#0x54]                        @ 08110e60 6065
LAB_08110e62:
    ldr r1,[r4,#0x54]                        @ 08110e62 616d
    ldr r0,[r1,#0x38]                        @ 08110e64 886b
    cmp r0,#0x0                              @ 08110e66 0028
    bne LAB_08110e70                         @ 08110e68 02d1
    adds r0,r1,#0x0    @ 08110e6a 081c
    bl __sinit                               @ 08110e6c 00f024f9
LAB_08110e70:
    movs r1,#0x21    @ 08110e70 2121
    rsbs r1,r1,#0    @ 08110e72 4942
    ldrh r0,[r4,#0xc]                        @ 08110e74 a089
    ands r1,r0    @ 08110e76 0140
    strh r1,[r4,#0xc]                        @ 08110e78 a181
    movs r0,#0x4    @ 08110e7a 0420
    ands r0,r1    @ 08110e7c 0840
    cmp r0,#0x0                              @ 08110e7e 0028
    bne LAB_08110eb4                         @ 08110e80 18d1
    movs r0,#0x10    @ 08110e82 1020
    ands r0,r1    @ 08110e84 0840
    cmp r0,#0x0                              @ 08110e86 0028
    beq LAB_08110ed0                         @ 08110e88 22d0
    movs r0,#0x8    @ 08110e8a 0820
    ands r1,r0    @ 08110e8c 0140
    cmp r1,#0x0                              @ 08110e8e 0029
    beq LAB_08110eac                         @ 08110e90 0cd0
    adds r0,r4,#0x0    @ 08110e92 201c
    bl fflush                                @ 08110e94 00f048f8
    adds r1,r0,#0x0    @ 08110e98 011c
    cmp r1,#0x0                              @ 08110e9a 0029
    bne LAB_08110ed0                         @ 08110e9c 18d1
    movs r0,#0x9    @ 08110e9e 0920
    rsbs r0,r0,#0    @ 08110ea0 4042
    ldrh r2,[r4,#0xc]                        @ 08110ea2 a289
    ands r0,r2    @ 08110ea4 1040
    strh r0,[r4,#0xc]                        @ 08110ea6 a081
    str r1,[r4,#0x8]                         @ 08110ea8 a160
    str r1,[r4,#0x18]                        @ 08110eaa a161
LAB_08110eac:
    movs r0,#0x4    @ 08110eac 0420
    ldrh r1,[r4,#0xc]                        @ 08110eae a189
    orrs r0,r1    @ 08110eb0 0843
    strh r0,[r4,#0xc]                        @ 08110eb2 a081
LAB_08110eb4:
    lsls r0,r5,#0x18    @ 08110eb4 2806
    lsrs r5,r0,#0x18    @ 08110eb6 050e
    ldr r0,[r4,#0x30]                        @ 08110eb8 206b
    cmp r0,#0x0                              @ 08110eba 0028
    beq LAB_08110eea                         @ 08110ebc 15d0
    ldr r1,[r4,#0x4]                         @ 08110ebe 6168
    ldr r0,[r4,#0x34]                        @ 08110ec0 606b
    cmp r1,r0                                @ 08110ec2 8142
    blt LAB_08110edc                         @ 08110ec4 0adb
    adds r0,r4,#0x0    @ 08110ec6 201c
    bl __submore                             @ 08110ec8 fff77eff
    cmp r0,#0x0                              @ 08110ecc 0028
    beq LAB_08110edc                         @ 08110ece 05d0
LAB_08110ed0:
    movs r0,#0x1    @ 08110ed0 0120
    rsbs r0,r0,#0    @ 08110ed2 4042
    b LAB_08110f24                           @ 08110ed4 26e0
    .zero  0x2
DAT_08110ed8:
    .word  0x09ed4d94                     @ 08110ed8 944ded09
LAB_08110edc:
    ldr r0,[r4,#0x0]                         @ 08110edc 2068
    subs r0,#0x1    @ 08110ede 0138
    str r0,[r4,#0x0]                         @ 08110ee0 2060
    strb r5,[r0,#0x0]                        @ 08110ee2 0570
    ldr r0,[r4,#0x4]                         @ 08110ee4 6068
    adds r0,#0x1    @ 08110ee6 0130
    b LAB_08110f20                           @ 08110ee8 1ae0
LAB_08110eea:
    ldr r0,[r4,#0x10]                        @ 08110eea 2069
    ldr r1,[r4,#0x0]                         @ 08110eec 2168
    cmp r0,#0x0                              @ 08110eee 0028
    beq LAB_08110f06                         @ 08110ef0 09d0
    cmp r1,r0                                @ 08110ef2 8142
    bls LAB_08110f06                         @ 08110ef4 07d9
    subs r2,r1,#0x1    @ 08110ef6 4a1e
    ldrb r0,[r2,#0x0]                        @ 08110ef8 1078
    cmp r0,r5                                @ 08110efa a842
    bne LAB_08110f06                         @ 08110efc 03d1
    str r2,[r4,#0x0]                         @ 08110efe 2260
    ldr r0,[r4,#0x4]                         @ 08110f00 6068
    adds r0,#0x1    @ 08110f02 0130
    b LAB_08110f20                           @ 08110f04 0ce0
LAB_08110f06:
    ldr r0,[r4,#0x4]                         @ 08110f06 6068
    str r0,[r4,#0x3c]                        @ 08110f08 e063
    str r1,[r4,#0x38]                        @ 08110f0a a163
    adds r0,r4,#0x0    @ 08110f0c 201c
    adds r0,#0x40    @ 08110f0e 4030
    str r0,[r4,#0x30]                        @ 08110f10 2063
    movs r0,#0x3    @ 08110f12 0320
    str r0,[r4,#0x34]                        @ 08110f14 6063
    adds r0,r4,#0x0    @ 08110f16 201c
    adds r0,#0x42    @ 08110f18 4230
    strb r5,[r0,#0x0]                        @ 08110f1a 0570
    str r0,[r4,#0x0]                         @ 08110f1c 2060
    movs r0,#0x1    @ 08110f1e 0120
LAB_08110f20:
    str r0,[r4,#0x4]                         @ 08110f20 6060
    adds r0,r5,#0x0    @ 08110f22 281c
LAB_08110f24:
    pop {r4,r5,r6,pc}                        @ 08110f24 70bd
    .zero  0x2
fflush:
    push {r4,r5,r6,lr}                       @ 08110f28 70b5
    adds r4,r0,#0x0    @ 08110f2a 041c
    cmp r4,#0x0                              @ 08110f2c 002c
    bne LAB_08110f44                         @ 08110f2e 09d1
    ldr r0, DAT_08110f3c                     @ 08110f30 0248
    ldr r0,[r0,#0x0]                         @ 08110f32 0068
    ldr r1, DAT_08110f40                     @ 08110f34 0249
    bl _fwalk                                @ 08110f36 00f02ffa
    b LAB_08110fba                           @ 08110f3a 3ee0
DAT_08110f3c:
    .word  0x09ed4d94                     @ 08110f3c 944ded09
DAT_08110f40:
    .word  0x08110f29                     @ 08110f40 290f1108
LAB_08110f44:
    ldr r0,[r4,#0x54]                        @ 08110f44 606d
    cmp r0,#0x0                              @ 08110f46 0028
    bne LAB_08110f50                         @ 08110f48 02d1
    ldr r0, DAT_08110f84                     @ 08110f4a 0e48
    ldr r0,[r0,#0x0]                         @ 08110f4c 0068
    str r0,[r4,#0x54]                        @ 08110f4e 6065
LAB_08110f50:
    ldr r1,[r4,#0x54]                        @ 08110f50 616d
    ldr r0,[r1,#0x38]                        @ 08110f52 886b
    cmp r0,#0x0                              @ 08110f54 0028
    bne LAB_08110f5e                         @ 08110f56 02d1
    adds r0,r1,#0x0    @ 08110f58 081c
    bl __sinit                               @ 08110f5a 00f0adf8
LAB_08110f5e:
    movs r0,#0xc    @ 08110f5e 0c20
    ldrsh r1,[r4,r0]                         @ 08110f60 215e
    movs r0,#0x8    @ 08110f62 0820
    ands r0,r1    @ 08110f64 0840
    cmp r0,#0x0                              @ 08110f66 0028
    beq LAB_08110fb8                         @ 08110f68 26d0
    ldr r6,[r4,#0x10]                        @ 08110f6a 2669
    cmp r6,#0x0                              @ 08110f6c 002e
    beq LAB_08110fb8                         @ 08110f6e 23d0
    ldr r0,[r4,#0x0]                         @ 08110f70 2068
    subs r5,r0,r6    @ 08110f72 851b
    str r6,[r4,#0x0]                         @ 08110f74 2660
    movs r0,#0x3    @ 08110f76 0320
    ands r0,r1    @ 08110f78 0840
    cmp r0,#0x0                              @ 08110f7a 0028
    bne LAB_08110f96                         @ 08110f7c 0bd1
    ldr r0,[r4,#0x14]                        @ 08110f7e 6069
    b LAB_08110f98                           @ 08110f80 0ae0
    .zero  0x2
DAT_08110f84:
    .word  0x09ed4d94                     @ 08110f84 944ded09
LAB_08110f88:
    movs r0,#0x40    @ 08110f88 4020
    ldrh r1,[r4,#0xc]                        @ 08110f8a a189
    orrs r0,r1    @ 08110f8c 0843
    strh r0,[r4,#0xc]                        @ 08110f8e a081
    movs r0,#0x1    @ 08110f90 0120
    rsbs r0,r0,#0    @ 08110f92 4042
    b LAB_08110fba                           @ 08110f94 11e0
LAB_08110f96:
    movs r0,#0x0    @ 08110f96 0020
LAB_08110f98:
    str r0,[r4,#0x8]                         @ 08110f98 a060
    cmp r5,#0x0                              @ 08110f9a 002d
    ble LAB_08110fb8                         @ 08110f9c 0cdd
LAB_08110f9e:
    ldr r0,[r4,#0x1c]                        @ 08110f9e e069
    ldr r3,[r4,#0x24]                        @ 08110fa0 636a
    adds r1,r6,#0x0    @ 08110fa2 311c
    adds r2,r5,#0x0    @ 08110fa4 2a1c
    bl invoke_r3                             @ 08110fa6 fdf715fb
    adds r1,r0,#0x0    @ 08110faa 011c
    cmp r1,#0x0                              @ 08110fac 0029
    ble LAB_08110f88                         @ 08110fae ebdd
    adds r6,r6,r1    @ 08110fb0 7618
    subs r5,r5,r1    @ 08110fb2 6d1a
    cmp r5,#0x0                              @ 08110fb4 002d
    bgt LAB_08110f9e                         @ 08110fb6 f2dc
LAB_08110fb8:
    movs r0,#0x0    @ 08110fb8 0020
LAB_08110fba:
    pop {r4,r5,r6,pc}                        @ 08110fba 70bd

@ Initializes a single stdio __sFILE (FILE) struct entry: zeroes [+0x0..+0x8] (data/read-ptr/count), writes flags to [+0xc], fd (file descriptor number) to [+0xe], zeroes [+0x10]/[+0x18], writes self-reference [+0x1c]=r0 (ungetc buffer base), sets 4 function pointers ([+0x20]=_sread / [+0x24]=_swrite / [+0x28]=_sseek / [+0x2c]=_sclose), and writes reent pointer to [+0x54]. Called 3 times by __sinit (0x081110b8) to initialize stdin (fd=0)/stdout (fd=1)/stderr (fd=2) standard stream entries.
@ 
@ Constants:
@ - _SREAD=0x081125cd (_sread read method function pointer)
@ - _SWRITE=0x08112601 (_swrite write method function pointer)
@ - _SSEEK=0x08112641 (_sseek seek method function pointer)
@ - _SCLOSE=0x08112681 (_sclose close method function pointer)
init_sfp_entry:
    push {r4,lr}                             @ 08110fbc 10b5
    movs r4,#0x0    @ 08110fbe 0024
    str r4,[r0,#0x0]                         @ 08110fc0 0460
    str r4,[r0,#0x4]                         @ 08110fc2 4460
    str r4,[r0,#0x8]                         @ 08110fc4 8460
    strh r1,[r0,#0xc]                        @ 08110fc6 8181
    strh r2,[r0,#0xe]                        @ 08110fc8 c281
    str r4,[r0,#0x10]                        @ 08110fca 0461
    str r4,[r0,#0x18]                        @ 08110fcc 8461
    str r0,[r0,#0x1c]                        @ 08110fce c061
    ldr r1, DAT_08110fe4                     @ 08110fd0 0449
    str r1,[r0,#0x20]                        @ 08110fd2 0162
    ldr r1, DAT_08110fe8                     @ 08110fd4 0449
    str r1,[r0,#0x24]                        @ 08110fd6 4162
    ldr r1, DAT_08110fec                     @ 08110fd8 0449
    str r1,[r0,#0x28]                        @ 08110fda 8162
    ldr r1, DAT_08110ff0                     @ 08110fdc 0449
    str r1,[r0,#0x2c]                        @ 08110fde c162
    str r3,[r0,#0x54]                        @ 08110fe0 4365
    pop {r4,pc}                              @ 08110fe2 10bd
DAT_08110fe4:
    .word  0x081125cd                     @ 08110fe4 cd251108
DAT_08110fe8:
    .word  0x08112601                     @ 08110fe8 01261108
DAT_08110fec:
    .word  0x08112641                     @ 08110fec 41261108
DAT_08110ff0:
    .word  0x08112681                     @ 08110ff0 81261108
__sfmoreglue:
    push {r4,r5,r6,lr}                       @ 08110ff4 70b5
    adds r5,r1,#0x0    @ 08110ff6 0d1c
    movs r1,#0x58    @ 08110ff8 5821
    adds r6,r5,#0x0    @ 08110ffa 2e1c
    muls r6,r1    @ 08110ffc 4e43
    adds r1,r6,#0x0    @ 08110ffe 311c
    adds r1,#0xc    @ 08111000 0c31
    bl _malloc_r                             @ 08111002 00f005fb
    adds r4,r0,#0x0    @ 08111006 041c
    cmp r4,#0x0                              @ 08111008 002c
    beq LAB_08111020                         @ 0811100a 09d0
    adds r0,#0xc    @ 0811100c 0c30
    movs r1,#0x0    @ 0811100e 0021
    str r1,[r4,#0x0]                         @ 08111010 2160
    str r5,[r4,#0x4]                         @ 08111012 6560
    str r0,[r4,#0x8]                         @ 08111014 a060
    adds r2,r6,#0x0    @ 08111016 321c
    bl memset                                @ 08111018 fdf7d0fc
    adds r0,r4,#0x0    @ 0811101c 201c
    b LAB_08111022                           @ 0811101e 00e0
LAB_08111020:
    movs r0,#0x0    @ 08111020 0020
LAB_08111022:
    pop {r4,r5,r6,pc}                        @ 08111022 70bd
__sfp:
    push {r4,r5,lr}                          @ 08111024 30b5
    adds r5,r0,#0x0    @ 08111026 051c
    ldr r0,[r5,#0x38]                        @ 08111028 a86b
    cmp r0,#0x0                              @ 0811102a 0028
    bne LAB_08111034                         @ 0811102c 02d1
    adds r0,r5,#0x0    @ 0811102e 281c
    bl __sinit                               @ 08111030 00f042f8
LAB_08111034:
    movs r0,#0xec    @ 08111034 ec20
    lsls r0,r0,#0x1    @ 08111036 4000
    adds r4,r5,r0    @ 08111038 2c18
    b LAB_0811103e                           @ 0811103a 00e0
LAB_0811103c:
    ldr r4,[r4,#0x0]                         @ 0811103c 2468
LAB_0811103e:
    ldr r2,[r4,#0x8]                         @ 0811103e a268
    ldr r0,[r4,#0x4]                         @ 08111040 6068
    b LAB_0811104e                           @ 08111042 04e0
LAB_08111044:
    movs r3,#0xc    @ 08111044 0c23
    ldrsh r1,[r2,r3]                         @ 08111046 d15e
    cmp r1,#0x0                              @ 08111048 0029
    beq LAB_08111070                         @ 0811104a 11d0
    adds r2,#0x58    @ 0811104c 5832
LAB_0811104e:
    subs r0,#0x1    @ 0811104e 0138
    cmp r0,#0x0                              @ 08111050 0028
    bge LAB_08111044                         @ 08111052 f7da
    ldr r0,[r4,#0x0]                         @ 08111054 2068
    cmp r0,#0x0                              @ 08111056 0028
    bne LAB_0811103c                         @ 08111058 f0d1
    adds r0,r5,#0x0    @ 0811105a 281c
    movs r1,#0x4    @ 0811105c 0421
    bl __sfmoreglue                          @ 0811105e fff7c9ff
    str r0,[r4,#0x0]                         @ 08111062 2060
    cmp r0,#0x0                              @ 08111064 0028
    bne LAB_0811103c                         @ 08111066 e9d1
    movs r0,#0xc    @ 08111068 0c20
    str r0,[r5,#0x0]                         @ 0811106a 2860
    movs r0,#0x0    @ 0811106c 0020
    b LAB_08111090                           @ 0811106e 0fe0
LAB_08111070:
    movs r0,#0x1    @ 08111070 0120
    strh r0,[r2,#0xc]                        @ 08111072 9081
    str r1,[r2,#0x0]                         @ 08111074 1160
    str r1,[r2,#0x8]                         @ 08111076 9160
    str r1,[r2,#0x4]                         @ 08111078 5160
    str r1,[r2,#0x10]                        @ 0811107a 1161
    str r1,[r2,#0x14]                        @ 0811107c 5161
    str r1,[r2,#0x18]                        @ 0811107e 9161
    ldr r0, DAT_08111094                     @ 08111080 0448
    strh r0,[r2,#0xe]                        @ 08111082 d081
    str r1,[r2,#0x30]                        @ 08111084 1163
    str r1,[r2,#0x34]                        @ 08111086 5163
    str r1,[r2,#0x44]                        @ 08111088 5164
    str r1,[r2,#0x48]                        @ 0811108a 9164
    str r5,[r2,#0x54]                        @ 0811108c 5565
    adds r0,r2,#0x0    @ 0811108e 101c
LAB_08111090:
    pop {r4,r5,pc}                           @ 08111090 30bd
    .zero  0x2
DAT_08111094:
    .word  0x0000ffff                     @ 08111094 ffff0000
_cleanup_r:
    push {lr}                                @ 08111098 00b5
    ldr r1, DAT_081110a4                     @ 0811109a 0249
    bl _fwalk                                @ 0811109c 00f07cf9
    pop {pc}                                 @ 081110a0 00bd
    .zero  0x2
DAT_081110a4:
    .word  0x08110f29                     @ 081110a4 290f1108

@ newlib stdio atexit cleanup entry: binds global reent ptr then calls _cleanup_r to flush and close all open stdio FILE buffers.
@ Trigger: called back via atexit mechanism when process exits; registered as function pointer during __sinit (0x081110b8) stdio initialization.
@ Side effects: forwarded to _cleanup_r -> flush all __sFILE write buffers, close non-standard streams.
@ 
@ Constants:
@ - IMPURE_PTR=0x09ed4d94 (_impure_ptr, newlib global reent structure pointer)
invoke_cleanup_r:
    push {lr}                                @ 081110a8 00b5
    ldr r0, DAT_081110b4                     @ 081110aa 0248
    ldr r0,[r0,#0x0]                         @ 081110ac 0068
    bl _cleanup_r                            @ 081110ae fff7f3ff
    pop {pc}                                 @ 081110b2 00bd
DAT_081110b4:
    .word  0x09ed4d94                     @ 081110b4 944ded09
__sinit:
    push {r4,r5,lr}                          @ 081110b8 30b5
    adds r5,r0,#0x0    @ 081110ba 051c
    ldr r0, DAT_08111114                     @ 081110bc 1548
    str r0,[r5,#0x3c]                        @ 081110be e863
    movs r0,#0x1    @ 081110c0 0120
    str r0,[r5,#0x38]                        @ 081110c2 a863
    movs r0,#0xf2    @ 081110c4 f220
    lsls r0,r0,#0x1    @ 081110c6 4000
    adds r4,r5,r0    @ 081110c8 2c18
    adds r0,r4,#0x0    @ 081110ca 201c
    movs r1,#0x4    @ 081110cc 0421
    movs r2,#0x0    @ 081110ce 0022
    adds r3,r5,#0x0    @ 081110d0 2b1c
    bl init_sfp_entry                        @ 081110d2 fff773ff
    movs r1,#0x8f    @ 081110d6 8f21
    lsls r1,r1,#0x2    @ 081110d8 8900
    adds r0,r5,r1    @ 081110da 6818
    movs r1,#0x9    @ 081110dc 0921
    movs r2,#0x1    @ 081110de 0122
    adds r3,r5,#0x0    @ 081110e0 2b1c
    bl init_sfp_entry                        @ 081110e2 fff76bff
    movs r1,#0xa5    @ 081110e6 a521
    lsls r1,r1,#0x2    @ 081110e8 8900
    adds r0,r5,r1    @ 081110ea 6818
    movs r1,#0xa    @ 081110ec 0a21
    movs r2,#0x2    @ 081110ee 0222
    adds r3,r5,#0x0    @ 081110f0 2b1c
    bl init_sfp_entry                        @ 081110f2 fff763ff
    movs r0,#0xec    @ 081110f6 ec20
    lsls r0,r0,#0x1    @ 081110f8 4000
    adds r1,r5,r0    @ 081110fa 2918
    movs r0,#0x0    @ 081110fc 0020
    str r0,[r1,#0x0]                         @ 081110fe 0860
    movs r0,#0xee    @ 08111100 ee20
    lsls r0,r0,#0x1    @ 08111102 4000
    adds r1,r5,r0    @ 08111104 2918
    movs r0,#0x3    @ 08111106 0320
    str r0,[r1,#0x0]                         @ 08111108 0860
    movs r1,#0xf0    @ 0811110a f021
    lsls r1,r1,#0x1    @ 0811110c 4900
    adds r0,r5,r1    @ 0811110e 6818
    str r4,[r0,#0x0]                         @ 08111110 0460
    pop {r4,r5,pc}                           @ 08111112 30bd
DAT_08111114:
    .word  0x08111099                     @ 08111114 99101108
_free_r:
    push {r4,r5,r6,r7,lr}                    @ 08111118 f0b5
    .hword 0x464f    @ 0811111a 4f46
    .hword 0x4646    @ 0811111c 4646
    push {r6,r7}                             @ 0811111e c0b4
    .hword 0x4681    @ 08111120 8146
    adds r4,r1,#0x0    @ 08111122 0c1c
    cmp r4,#0x0                              @ 08111124 002c
    bne LAB_0811112a                         @ 08111126 00d1
    b LAB_081112ce                           @ 08111128 d1e0
LAB_0811112a:
    bl stub_malloc_lock                      @ 0811112a 00f051fc
    adds r5,r4,#0x0    @ 0811112e 251c
    subs r5,#0x8    @ 08111130 083d
    ldr r1,[r5,#0x4]                         @ 08111132 6968
    movs r6,#0x2    @ 08111134 0226
    rsbs r6,r6,#0    @ 08111136 7642
    ands r6,r1    @ 08111138 0e40
    adds r7,r5,r6    @ 0811113a af19
    ldr r4,[r7,#0x4]                         @ 0811113c 7c68
    movs r0,#0x4    @ 0811113e 0420
    rsbs r0,r0,#0    @ 08111140 4042
    ands r4,r0    @ 08111142 0440
    ldr r0, DAT_0811118c                     @ 08111144 1148
    .hword 0x4684    @ 08111146 8446
    ldr r0,[r0,#0x8]                         @ 08111148 8068
    cmp r7,r0                                @ 0811114a 8742
    bne LAB_08111198                         @ 0811114c 24d1
    adds r6,r6,r4    @ 0811114e 3619
    movs r4,#0x1    @ 08111150 0124
    ands r1,r4    @ 08111152 2140
    cmp r1,#0x0                              @ 08111154 0029
    bne LAB_08111166                         @ 08111156 06d1
    ldr r0,[r5,#0x0]                         @ 08111158 2868
    subs r5,r5,r0    @ 0811115a 2d1a
    adds r6,r6,r0    @ 0811115c 3618
    ldr r3,[r5,#0xc]                         @ 0811115e eb68
    ldr r2,[r5,#0x8]                         @ 08111160 aa68
    str r3,[r2,#0xc]                         @ 08111162 d360
    str r2,[r3,#0x8]                         @ 08111164 9a60
LAB_08111166:
    adds r0,r6,#0x0    @ 08111166 301c
    orrs r0,r4    @ 08111168 2043
    str r0,[r5,#0x4]                         @ 0811116a 6860
    .hword 0x4662    @ 0811116c 6246
    str r5,[r2,#0x8]                         @ 0811116e 9560
    ldr r0, DAT_08111190                     @ 08111170 0748
    ldr r0,[r0,#0x0]                         @ 08111172 0068
    cmp r6,r0                                @ 08111174 8642
    bcc LAB_08111182                         @ 08111176 04d3
    ldr r0, DAT_08111194                     @ 08111178 0648
    ldr r1,[r0,#0x0]                         @ 0811117a 0168
    .hword 0x4648    @ 0811117c 4846
    bl _malloc_trim_r                        @ 0811117e 00f0abf8
LAB_08111182:
    .hword 0x4648    @ 08111182 4846
    bl stub_malloc_unlock                    @ 08111184 00f026fc
    b LAB_081112ce                           @ 08111188 a1e0
    .zero  0x2
DAT_0811118c:
    .word  0x09ed4d98                     @ 0811118c 984ded09
DAT_08111190:
    .word  0x09ed51a0                     @ 08111190 a051ed09
DAT_08111194:
    .word  0x09ed51a4                     @ 08111194 a451ed09
LAB_08111198:
    str r4,[r7,#0x4]                         @ 08111198 7c60
    movs r0,#0x0    @ 0811119a 0020
    .hword 0x4680    @ 0811119c 8046
    movs r0,#0x1    @ 0811119e 0120
    ands r1,r0    @ 081111a0 0140
    cmp r1,#0x0                              @ 081111a2 0029
    bne LAB_081111c4                         @ 081111a4 0ed1
    ldr r0,[r5,#0x0]                         @ 081111a6 2868
    subs r5,r5,r0    @ 081111a8 2d1a
    adds r6,r6,r0    @ 081111aa 3618
    ldr r1,[r5,#0x8]                         @ 081111ac a968
    .hword 0x4660    @ 081111ae 6046
    adds r0,#0x8    @ 081111b0 0830
    cmp r1,r0                                @ 081111b2 8142
    bne LAB_081111bc                         @ 081111b4 02d1
    movs r2,#0x1    @ 081111b6 0122
    .hword 0x4690    @ 081111b8 9046
    b LAB_081111c4                           @ 081111ba 03e0
LAB_081111bc:
    ldr r3,[r5,#0xc]                         @ 081111bc eb68
    adds r2,r1,#0x0    @ 081111be 0a1c
    str r3,[r2,#0xc]                         @ 081111c0 d360
    str r2,[r3,#0x8]                         @ 081111c2 9a60
LAB_081111c4:
    adds r0,r7,r4    @ 081111c4 3819
    ldr r0,[r0,#0x4]                         @ 081111c6 4068
    movs r1,#0x1    @ 081111c8 0121
    ands r0,r1    @ 081111ca 0840
    cmp r0,#0x0                              @ 081111cc 0028
    bne LAB_081111fc                         @ 081111ce 15d1
    adds r6,r6,r4    @ 081111d0 3619
    ldr r1,[r7,#0x8]                         @ 081111d2 b968
    .hword 0x4640    @ 081111d4 4046
    cmp r0,#0x0                              @ 081111d6 0028
    bne LAB_081111f4                         @ 081111d8 0cd1
    ldr r0, DAT_081111f0                     @ 081111da 0548
    cmp r1,r0                                @ 081111dc 8142
    bne LAB_081111f4                         @ 081111de 09d1
    movs r2,#0x1    @ 081111e0 0122
    .hword 0x4690    @ 081111e2 9046
    str r5,[r1,#0xc]                         @ 081111e4 cd60
    str r5,[r1,#0x8]                         @ 081111e6 8d60
    str r1,[r5,#0xc]                         @ 081111e8 e960
    str r1,[r5,#0x8]                         @ 081111ea a960
    b LAB_081111fc                           @ 081111ec 06e0
    .zero  0x2
DAT_081111f0:
    .word  0x09ed4da0                     @ 081111f0 a04ded09
LAB_081111f4:
    ldr r3,[r7,#0xc]                         @ 081111f4 fb68
    adds r2,r1,#0x0    @ 081111f6 0a1c
    str r3,[r2,#0xc]                         @ 081111f8 d360
    str r2,[r3,#0x8]                         @ 081111fa 9a60
LAB_081111fc:
    movs r1,#0x1    @ 081111fc 0121
    adds r0,r6,#0x0    @ 081111fe 301c
    orrs r0,r1    @ 08111200 0843
    str r0,[r5,#0x4]                         @ 08111202 6860
    adds r0,r5,r6    @ 08111204 a819
    str r6,[r0,#0x0]                         @ 08111206 0660
    .hword 0x4640    @ 08111208 4046
    cmp r0,#0x0                              @ 0811120a 0028
    bne LAB_081112c8                         @ 0811120c 5cd1
    ldr r0, DAT_0811122c                     @ 0811120e 0748
    cmp r6,r0                                @ 08111210 8642
    bhi LAB_08111234                         @ 08111212 0fd8
    lsrs r4,r6,#0x3    @ 08111214 f408
    ldr r2, DAT_08111230                     @ 08111216 064a
    adds r0,r4,#0x0    @ 08111218 201c
    asrs r0,r0,#0x2    @ 0811121a 8010
    lsls r1,r0    @ 0811121c 8140
    ldr r0,[r2,#0x4]                         @ 0811121e 5068
    orrs r0,r1    @ 08111220 0843
    str r0,[r2,#0x4]                         @ 08111222 5060
    lsls r0,r4,#0x3    @ 08111224 e000
    adds r3,r0,r2    @ 08111226 8318
    ldr r2,[r3,#0x8]                         @ 08111228 9a68
    b LAB_081112c0                           @ 0811122a 49e0
DAT_0811122c:
    .word  0x000001ff                     @ 0811122c ff010000
DAT_08111230:
    .word  0x09ed4d98                     @ 08111230 984ded09
LAB_08111234:
    lsrs r1,r6,#0x9    @ 08111234 710a
    cmp r1,#0x0                              @ 08111236 0029
    bne LAB_0811123e                         @ 08111238 01d1
    lsrs r4,r6,#0x3    @ 0811123a f408
    b LAB_08111286                           @ 0811123c 23e0
LAB_0811123e:
    cmp r1,#0x4                              @ 0811123e 0429
    bhi LAB_0811124a                         @ 08111240 03d8
    lsrs r0,r6,#0x6    @ 08111242 b009
    adds r4,r0,#0x0    @ 08111244 041c
    adds r4,#0x38    @ 08111246 3834
    b LAB_08111286                           @ 08111248 1de0
LAB_0811124a:
    cmp r1,#0x14                             @ 0811124a 1429
    bhi LAB_08111254                         @ 0811124c 02d8
    adds r4,r1,#0x0    @ 0811124e 0c1c
    adds r4,#0x5b    @ 08111250 5b34
    b LAB_08111286                           @ 08111252 18e0
LAB_08111254:
    cmp r1,#0x54                             @ 08111254 5429
    bhi LAB_08111260                         @ 08111256 03d8
    lsrs r0,r6,#0xc    @ 08111258 300b
    adds r4,r0,#0x0    @ 0811125a 041c
    adds r4,#0x6e    @ 0811125c 6e34
    b LAB_08111286                           @ 0811125e 12e0
LAB_08111260:
    movs r0,#0xaa    @ 08111260 aa20
    lsls r0,r0,#0x1    @ 08111262 4000
    cmp r1,r0                                @ 08111264 8142
    bhi LAB_08111270                         @ 08111266 03d8
    lsrs r0,r6,#0xf    @ 08111268 f00b
    adds r4,r0,#0x0    @ 0811126a 041c
    adds r4,#0x77    @ 0811126c 7734
    b LAB_08111286                           @ 0811126e 0ae0
LAB_08111270:
    ldr r0, DAT_08111280                     @ 08111270 0348
    cmp r1,r0                                @ 08111272 8142
    bhi LAB_08111284                         @ 08111274 06d8
    lsrs r0,r6,#0x12    @ 08111276 b00c
    adds r4,r0,#0x0    @ 08111278 041c
    adds r4,#0x7c    @ 0811127a 7c34
    b LAB_08111286                           @ 0811127c 03e0
    .zero  0x2
DAT_08111280:
    .word  0x00000554                     @ 08111280 54050000
LAB_08111284:
    movs r4,#0x7e    @ 08111284 7e24
LAB_08111286:
    lsls r0,r4,#0x3    @ 08111286 e000
    ldr r7, DAT_081112a4                     @ 08111288 064f
    adds r3,r0,r7    @ 0811128a c319
    ldr r2,[r3,#0x8]                         @ 0811128c 9a68
    cmp r2,r3                                @ 0811128e 9a42
    bne LAB_081112a8                         @ 08111290 0ad1
    adds r0,r4,#0x0    @ 08111292 201c
    asrs r0,r0,#0x2    @ 08111294 8010
    movs r1,#0x1    @ 08111296 0121
    lsls r1,r0    @ 08111298 8140
    ldr r0,[r7,#0x4]                         @ 0811129a 7868
    orrs r0,r1    @ 0811129c 0843
    str r0,[r7,#0x4]                         @ 0811129e 7860
    b LAB_081112c0                           @ 081112a0 0ee0
    .zero  0x2
DAT_081112a4:
    .word  0x09ed4d98                     @ 081112a4 984ded09
LAB_081112a8:
    ldr r0,[r2,#0x4]                         @ 081112a8 5068
    movs r1,#0x4    @ 081112aa 0421
    rsbs r1,r1,#0    @ 081112ac 4942
    b LAB_081112b8                           @ 081112ae 03e0
LAB_081112b0:
    ldr r2,[r2,#0x8]                         @ 081112b0 9268
    cmp r2,r3                                @ 081112b2 9a42
    beq LAB_081112be                         @ 081112b4 03d0
    ldr r0,[r2,#0x4]                         @ 081112b6 5068
LAB_081112b8:
    ands r0,r1    @ 081112b8 0840
    cmp r6,r0                                @ 081112ba 8642
    bcc LAB_081112b0                         @ 081112bc f8d3
LAB_081112be:
    ldr r3,[r2,#0xc]                         @ 081112be d368
LAB_081112c0:
    str r3,[r5,#0xc]                         @ 081112c0 eb60
    str r2,[r5,#0x8]                         @ 081112c2 aa60
    str r5,[r3,#0x8]                         @ 081112c4 9d60
    str r5,[r2,#0xc]                         @ 081112c6 d560
LAB_081112c8:
    .hword 0x4648    @ 081112c8 4846
    bl stub_malloc_unlock                    @ 081112ca 00f083fb
LAB_081112ce:
    pop {r3,r4}                              @ 081112ce 18bc
    .hword 0x4698    @ 081112d0 9846
    .hword 0x46a1    @ 081112d2 a146
    pop {r4,r5,r6,r7,pc}                     @ 081112d4 f0bd
    .zero  0x2
_malloc_trim_r:
    push {r4,r5,r6,r7,lr}                    @ 081112d8 f0b5
    .hword 0x4647    @ 081112da 4746
    push {r7}                                @ 081112dc 80b4
    adds r7,r0,#0x0    @ 081112de 071c
    adds r4,r1,#0x0    @ 081112e0 0c1c
    bl stub_malloc_lock                      @ 081112e2 00f075fb
    ldr r0, DAT_08111360                     @ 081112e6 1e48
    .hword 0x4680    @ 081112e8 8046
    ldr r0,[r0,#0x8]                         @ 081112ea 8068
    ldr r6,[r0,#0x4]                         @ 081112ec 4668
    movs r0,#0x4    @ 081112ee 0420
    rsbs r0,r0,#0    @ 081112f0 4042
    ands r6,r0    @ 081112f2 0640
    subs r4,r6,r4    @ 081112f4 341b
    movs r5,#0x80    @ 081112f6 8025
    lsls r5,r5,#0x5    @ 081112f8 6d01
    ldr r1, DAT_08111364                     @ 081112fa 1a49
    adds r4,r4,r1    @ 081112fc 6418
    adds r0,r4,#0x0    @ 081112fe 201c
    adds r1,r5,#0x0    @ 08111300 291c
    bl __udivsi3                             @ 08111302 fdf76bfa
    subs r0,#0x1    @ 08111306 0138
    lsls r4,r0,#0xc    @ 08111308 0403
    cmp r4,r5                                @ 0811130a ac42
    blt LAB_08111356                         @ 0811130c 23db
    adds r0,r7,#0x0    @ 0811130e 381c
    movs r1,#0x0    @ 08111310 0021
    bl wrap_sbrk_r                           @ 08111312 01f045f9
    adds r2,r0,#0x0    @ 08111316 021c
    .hword 0x4641    @ 08111318 4146
    ldr r0,[r1,#0x8]                         @ 0811131a 8868
    adds r0,r0,r6    @ 0811131c 8019
    cmp r2,r0                                @ 0811131e 8242
    bne LAB_08111356                         @ 08111320 19d1
    rsbs r1,r4,#0    @ 08111322 6142
    adds r0,r7,#0x0    @ 08111324 381c
    bl wrap_sbrk_r                           @ 08111326 01f03bf9
    movs r1,#0x1    @ 0811132a 0121
    rsbs r1,r1,#0    @ 0811132c 4942
    cmp r0,r1                                @ 0811132e 8842
    bne LAB_08111370                         @ 08111330 1ed1
    adds r0,r7,#0x0    @ 08111332 381c
    movs r1,#0x0    @ 08111334 0021
    bl wrap_sbrk_r                           @ 08111336 01f033f9
    adds r2,r0,#0x0    @ 0811133a 021c
    .hword 0x4640    @ 0811133c 4046
    ldr r3,[r0,#0x8]                         @ 0811133e 8368
    subs r6,r2,r3    @ 08111340 d61a
    cmp r6,#0xf                              @ 08111342 0f2e
    ble LAB_08111356                         @ 08111344 07dd
    ldr r1, DAT_08111368                     @ 08111346 0849
    ldr r0, DAT_0811136c                     @ 08111348 0848
    ldr r0,[r0,#0x0]                         @ 0811134a 0068
    subs r0,r2,r0    @ 0811134c 101a
    str r0,[r1,#0x0]                         @ 0811134e 0860
    movs r0,#0x1    @ 08111350 0120
    orrs r6,r0    @ 08111352 0643
    str r6,[r3,#0x4]                         @ 08111354 5e60
LAB_08111356:
    adds r0,r7,#0x0    @ 08111356 381c
    bl stub_malloc_unlock                    @ 08111358 00f03cfb
    movs r0,#0x0    @ 0811135c 0020
    b LAB_0811138c                           @ 0811135e 15e0
DAT_08111360:
    .word  0x09ed4d98                     @ 08111360 984ded09
DAT_08111364:
    .word  0x00000fef                     @ 08111364 ef0f0000
DAT_08111368:
    .word  0x09ed51b4                     @ 08111368 b451ed09
DAT_0811136c:
    .word  0x09ed51a8                     @ 0811136c a851ed09
LAB_08111370:
    .hword 0x4641    @ 08111370 4146
    ldr r2,[r1,#0x8]                         @ 08111372 8a68
    subs r0,r6,r4    @ 08111374 301b
    movs r1,#0x1    @ 08111376 0121
    orrs r0,r1    @ 08111378 0843
    str r0,[r2,#0x4]                         @ 0811137a 5060
    ldr r1, DAT_08111394                     @ 0811137c 0549
    ldr r0,[r1,#0x0]                         @ 0811137e 0868
    subs r0,r0,r4    @ 08111380 001b
    str r0,[r1,#0x0]                         @ 08111382 0860
    adds r0,r7,#0x0    @ 08111384 381c
    bl stub_malloc_unlock                    @ 08111386 00f025fb
    movs r0,#0x1    @ 0811138a 0120
LAB_0811138c:
    pop {r3}                                 @ 0811138c 08bc
    .hword 0x4698    @ 0811138e 9846
    pop {r4,r5,r6,r7,pc}                     @ 08111390 f0bd
    .zero  0x2
DAT_08111394:
    .word  0x09ed51b4                     @ 08111394 b451ed09
_fwalk:
    push {r4,r5,r6,r7,lr}                    @ 08111398 f0b5
    .hword 0x4647    @ 0811139a 4746
    push {r7}                                @ 0811139c 80b4
    .hword 0x4688    @ 0811139e 8846
    movs r7,#0x0    @ 081113a0 0027
    movs r1,#0xec    @ 081113a2 ec21
    lsls r1,r1,#0x1    @ 081113a4 4900
    adds r6,r0,r1    @ 081113a6 4618
    cmp r6,#0x0                              @ 081113a8 002e
    beq LAB_081113d0                         @ 081113aa 11d0
LAB_081113ac:
    ldr r5,[r6,#0x8]                         @ 081113ac b568
    ldr r4,[r6,#0x4]                         @ 081113ae 7468
    b LAB_081113c4                           @ 081113b0 08e0
LAB_081113b2:
    movs r1,#0xc    @ 081113b2 0c21
    ldrsh r0,[r5,r1]                         @ 081113b4 685e
    cmp r0,#0x0                              @ 081113b6 0028
    beq LAB_081113c2                         @ 081113b8 03d0
    adds r0,r5,#0x0    @ 081113ba 281c
    bl invoke_r8                             @ 081113bc fdf714f9
    orrs r7,r0    @ 081113c0 0743
LAB_081113c2:
    adds r5,#0x58    @ 081113c2 5835
LAB_081113c4:
    subs r4,#0x1    @ 081113c4 013c
    cmp r4,#0x0                              @ 081113c6 002c
    bge LAB_081113b2                         @ 081113c8 f3da
    ldr r6,[r6,#0x0]                         @ 081113ca 3668
    cmp r6,#0x0                              @ 081113cc 002e
    bne LAB_081113ac                         @ 081113ce edd1
LAB_081113d0:
    adds r0,r7,#0x0    @ 081113d0 381c
    pop {r3}                                 @ 081113d2 08bc
    .hword 0x4698    @ 081113d4 9846
    pop {r4,r5,r6,r7,pc}                     @ 081113d6 f0bd
__smakebuf:
    push {r4,r5,r6,r7,lr}                    @ 081113d8 f0b5
    sub sp,#0x3c                             @ 081113da 8fb0
    adds r4,r0,#0x0    @ 081113dc 041c
    movs r0,#0x2    @ 081113de 0220
    ldrh r1,[r4,#0xc]                        @ 081113e0 a189
    ands r0,r1    @ 081113e2 0840
    cmp r0,#0x0                              @ 081113e4 0028
    bne LAB_0811146e                         @ 081113e6 42d1
    movs r2,#0xe    @ 081113e8 0e22
    ldrsh r0,[r4,r2]                         @ 081113ea a05e
    cmp r0,#0x0                              @ 081113ec 0028
    blt LAB_08111400                         @ 081113ee 07db
    ldr r0,[r4,#0x54]                        @ 081113f0 606d
    movs r2,#0xe    @ 081113f2 0e22
    ldrsh r1,[r4,r2]                         @ 081113f4 a15e
    .hword 0x466a    @ 081113f6 6a46
    bl wrap_sclose_r                         @ 081113f8 01f0dcfb
    cmp r0,#0x0                              @ 081113fc 0028
    bge LAB_08111412                         @ 081113fe 08da
LAB_08111400:
    movs r7,#0x0    @ 08111400 0027
    movs r6,#0x80    @ 08111402 8026
    lsls r6,r6,#0x3    @ 08111404 f600
    movs r1,#0x80    @ 08111406 8021
    lsls r1,r1,#0x4    @ 08111408 0901
    adds r0,r1,#0x0    @ 0811140a 081c
    ldrh r2,[r4,#0xc]                        @ 0811140c a289
    orrs r0,r2    @ 0811140e 1043
    b LAB_08111456                           @ 08111410 21e0
LAB_08111412:
    movs r7,#0x0    @ 08111412 0027
    ldr r1,[sp,#0x4]                         @ 08111414 0199
    movs r0,#0xf0    @ 08111416 f020
    lsls r0,r0,#0x8    @ 08111418 0002
    ands r1,r0    @ 0811141a 0140
    movs r0,#0x80    @ 0811141c 8020
    lsls r0,r0,#0x6    @ 0811141e 8001
    cmp r1,r0                                @ 08111420 8142
    bne LAB_08111426                         @ 08111422 00d1
    movs r7,#0x1    @ 08111424 0127
LAB_08111426:
    movs r6,#0x80    @ 08111426 8026
    lsls r6,r6,#0x3    @ 08111428 f600
    movs r0,#0x80    @ 0811142a 8020
    lsls r0,r0,#0x8    @ 0811142c 0002
    cmp r1,r0                                @ 0811142e 8142
    bne LAB_0811144c                         @ 08111430 0cd1
    ldr r1,[r4,#0x28]                        @ 08111432 a16a
    ldr r0, DAT_08111448                     @ 08111434 0448
    cmp r1,r0                                @ 08111436 8142
    bne LAB_0811144c                         @ 08111438 08d1
    adds r0,r6,#0x0    @ 0811143a 301c
    ldrh r1,[r4,#0xc]                        @ 0811143c a189
    orrs r0,r1    @ 0811143e 0843
    strh r0,[r4,#0xc]                        @ 08111440 a081
    str r6,[r4,#0x4c]                        @ 08111442 e664
    b LAB_08111458                           @ 08111444 08e0
    .zero  0x2
DAT_08111448:
    .word  0x08112641                     @ 08111448 41261108
LAB_0811144c:
    movs r2,#0x80    @ 0811144c 8022
    lsls r2,r2,#0x4    @ 0811144e 1201
    adds r0,r2,#0x0    @ 08111450 101c
    ldrh r1,[r4,#0xc]                        @ 08111452 a189
    orrs r0,r1    @ 08111454 0843
LAB_08111456:
    strh r0,[r4,#0xc]                        @ 08111456 a081
LAB_08111458:
    ldr r0,[r4,#0x54]                        @ 08111458 606d
    adds r1,r6,#0x0    @ 0811145a 311c
    bl _malloc_r                             @ 0811145c 00f0d8f8
    adds r2,r0,#0x0    @ 08111460 021c
    cmp r2,#0x0                              @ 08111462 002a
    bne LAB_0811147c                         @ 08111464 0ad1
    movs r0,#0x2    @ 08111466 0220
    ldrh r2,[r4,#0xc]                        @ 08111468 a289
    orrs r0,r2    @ 0811146a 1043
    strh r0,[r4,#0xc]                        @ 0811146c a081
LAB_0811146e:
    adds r0,r4,#0x0    @ 0811146e 201c
    adds r0,#0x43    @ 08111470 4330
    str r0,[r4,#0x0]                         @ 08111472 2060
    str r0,[r4,#0x10]                        @ 08111474 2061
    movs r0,#0x1    @ 08111476 0120
    str r0,[r4,#0x14]                        @ 08111478 6061
    b LAB_081114aa                           @ 0811147a 16e0
LAB_0811147c:
    ldr r1,[r4,#0x54]                        @ 0811147c 616d
    ldr r0, DAT_081114b0                     @ 0811147e 0c48
    str r0,[r1,#0x3c]                        @ 08111480 c863
    movs r0,#0x80    @ 08111482 8020
    movs r5,#0x0    @ 08111484 0025
    ldrh r1,[r4,#0xc]                        @ 08111486 a189
    orrs r0,r1    @ 08111488 0843
    strh r0,[r4,#0xc]                        @ 0811148a a081
    str r2,[r4,#0x0]                         @ 0811148c 2260
    str r2,[r4,#0x10]                        @ 0811148e 2261
    str r6,[r4,#0x14]                        @ 08111490 6661
    cmp r7,#0x0                              @ 08111492 002f
    beq LAB_081114aa                         @ 08111494 09d0
    movs r2,#0xe    @ 08111496 0e22
    ldrsh r0,[r4,r2]                         @ 08111498 a05e
    bl stub_isatty_true                      @ 0811149a 01f0b1fb
    cmp r0,#0x0                              @ 0811149e 0028
    beq LAB_081114aa                         @ 081114a0 03d0
    movs r0,#0x1    @ 081114a2 0120
    ldrh r1,[r4,#0xc]                        @ 081114a4 a189
    orrs r0,r1    @ 081114a6 0843
    strh r0,[r4,#0xc]                        @ 081114a8 a081
LAB_081114aa:
    add sp,#0x3c                             @ 081114aa 0fb0
    pop {r4,r5,r6,r7,pc}                     @ 081114ac f0bd
    .zero  0x2
DAT_081114b0:
    .word  0x08111099                     @ 081114b0 99101108

@ dlmalloc internal heap expansion function. Takes reent_ptr (r0) and size_request (r1), calls wrap_sbrk_r twice to request more memory from the OS, and updates heap footprint/size statistics fields in the newlib reent struct (0x09ed4d98 region): 0x09ed51b4=footprint, 0x09ed51ac=max_footprint_a, 0x09ed51b0=max_footprint_b.
@ 
@ First wrap_sbrk_r probes available contiguous address; returns if result is -1 (failure). After alignment adjustment, second wrap_sbrk_r obtains the aligned base. Updates footprint field and writes chunk header (prev_foot/size). If predecessor chunk exceeds threshold (r7>0xf), may call _free_r to release predecessor block.
@ 
@ Call context: _malloc_r (0x08111610) calls this function to expand the heap via the GBA semihosting environment when dlmalloc cannot find a sufficient free block internally.
@ 
@ Constants:
@ REENT_BASE=0x09ed4d98 (newlib reent struct pointer)
@ HEAP_SIZE_PTR=0x09ed51a4 (current heap size field pointer)
@ HEAP_BASE_PTR=0x09ed51a8 (heap base pointer)
@ FOOTPRINT=0x09ed51b4 (current footprint field)
@ MAX_FOOTPRINT_A=0x09ed51ac (max footprint field A)
@ MAX_FOOTPRINT_B=0x09ed51b0 (max footprint field B)
@ ALIGN_MASK=0xfffff000 (4KB page alignment mask)
@ ALIGN_BUMP=0x100f (pre-alignment addend, rounds up to 4KB page)
grow_heap_via_sbrk:
    push {r4,r5,r6,r7,lr}                    @ 081114b4 f0b5
    .hword 0x4657    @ 081114b6 5746
    .hword 0x464e    @ 081114b8 4e46
    .hword 0x4645    @ 081114ba 4546
    push {r5,r6,r7}                          @ 081114bc e0b4
    sub sp,#0x4                              @ 081114be 81b0
    str r0,[sp,#0x0]                         @ 081114c0 0090
    ldr r0, DAT_08111528                     @ 081114c2 1948
    ldr r0,[r0,#0x8]                         @ 081114c4 8068
    .hword 0x4680    @ 081114c6 8046
    ldr r7,[r0,#0x4]                         @ 081114c8 4768
    movs r0,#0x4    @ 081114ca 0420
    rsbs r0,r0,#0    @ 081114cc 4042
    ands r7,r0    @ 081114ce 0740
    .hword 0x4642    @ 081114d0 4246
    adds r4,r2,r7    @ 081114d2 d419
    ldr r0, DAT_0811152c                     @ 081114d4 1548
    ldr r0,[r0,#0x0]                         @ 081114d6 0068
    adds r1,r1,r0    @ 081114d8 0918
    adds r6,r1,#0x0    @ 081114da 0e1c
    adds r6,#0x10    @ 081114dc 1036
    ldr r3, DAT_08111530                     @ 081114de 144b
    .hword 0x469a    @ 081114e0 9a46
    ldr r0,[r3,#0x0]                         @ 081114e2 1868
    movs r2,#0x1    @ 081114e4 0122
    rsbs r2,r2,#0    @ 081114e6 5242
    .hword 0x4691    @ 081114e8 9146
    cmp r0,r9                                @ 081114ea 4845
    beq LAB_081114f6                         @ 081114ec 03d0
    ldr r3, DAT_08111534                     @ 081114ee 114b
    adds r6,r1,r3    @ 081114f0 ce18
    ldr r0, DAT_08111538                     @ 081114f2 1148
    ands r6,r0    @ 081114f4 0640
LAB_081114f6:
    ldr r0,[sp,#0x0]                         @ 081114f6 0098
    adds r1,r6,#0x0    @ 081114f8 311c
    bl wrap_sbrk_r                           @ 081114fa 01f051f8
    adds r5,r0,#0x0    @ 081114fe 051c
    cmp r5,r9                                @ 08111500 4d45
    beq LAB_081115f8                         @ 08111502 79d0
    cmp r5,r4                                @ 08111504 a542
    bcs LAB_0811150e                         @ 08111506 02d2
    ldr r0, DAT_08111528                     @ 08111508 0748
    cmp r8,r0                                @ 0811150a 8045
    bne LAB_081115f8                         @ 0811150c 74d1
LAB_0811150e:
    ldr r1, DAT_0811153c                     @ 0811150e 0b49
    ldr r0,[r1,#0x0]                         @ 08111510 0868
    adds r2,r0,r6    @ 08111512 8219
    str r2,[r1,#0x0]                         @ 08111514 0a60
    cmp r5,r4                                @ 08111516 a542
    bne LAB_08111540                         @ 08111518 12d1
    adds r2,r6,r7    @ 0811151a f219
    ldr r3, DAT_08111528                     @ 0811151c 024b
    ldr r1,[r3,#0x8]                         @ 0811151e 9968
    movs r0,#0x1    @ 08111520 0120
    orrs r2,r0    @ 08111522 0243
    str r2,[r1,#0x4]                         @ 08111524 4a60
    b LAB_081115e0                           @ 08111526 5be0
DAT_08111528:
    .word  0x09ed4d98                     @ 08111528 984ded09
DAT_0811152c:
    .word  0x09ed51a4                     @ 0811152c a451ed09
DAT_08111530:
    .word  0x09ed51a8                     @ 08111530 a851ed09
DAT_08111534:
    .word  0x0000100f                     @ 08111534 0f100000
DAT_08111538:
    .word  0xfffff000                     @ 08111538 00f0ffff
DAT_0811153c:
    .word  0x09ed51b4                     @ 0811153c b451ed09
LAB_08111540:
    .hword 0x4653    @ 08111540 5346
    ldr r0,[r3,#0x0]                         @ 08111542 1868
    cmp r0,r9                                @ 08111544 4845
    bne LAB_0811154c                         @ 08111546 01d1
    str r5,[r3,#0x0]                         @ 08111548 1d60
    b LAB_08111552                           @ 0811154a 02e0
LAB_0811154c:
    subs r0,r5,r4    @ 0811154c 281b
    adds r0,r2,r0    @ 0811154e 1018
    str r0,[r1,#0x0]                         @ 08111550 0860
LAB_08111552:
    adds r1,r5,#0x0    @ 08111552 291c
    adds r1,#0x8    @ 08111554 0831
    movs r0,#0x7    @ 08111556 0720
    ands r1,r0    @ 08111558 0140
    cmp r1,#0x0                              @ 0811155a 0029
    beq LAB_08111566                         @ 0811155c 03d0
    movs r0,#0x8    @ 0811155e 0820
    subs r4,r0,r1    @ 08111560 441a
    adds r5,r5,r4    @ 08111562 2d19
    b LAB_08111568                           @ 08111564 00e0
LAB_08111566:
    movs r4,#0x0    @ 08111566 0024
LAB_08111568:
    adds r0,r5,r6    @ 08111568 a819
    movs r1,#0x80    @ 0811156a 8021
    lsls r1,r1,#0x5    @ 0811156c 4901
    subs r1,#0x1    @ 0811156e 0139
    ands r0,r1    @ 08111570 0840
    movs r1,#0x80    @ 08111572 8021
    lsls r1,r1,#0x5    @ 08111574 4901
    subs r0,r1,r0    @ 08111576 081a
    adds r4,r4,r0    @ 08111578 2418
    ldr r0,[sp,#0x0]                         @ 0811157a 0098
    adds r1,r4,#0x0    @ 0811157c 211c
    bl wrap_sbrk_r                           @ 0811157e 01f00ff8
    adds r2,r0,#0x0    @ 08111582 021c
    movs r0,#0x1    @ 08111584 0120
    rsbs r0,r0,#0    @ 08111586 4042
    cmp r2,r0                                @ 08111588 8242
    beq LAB_081115f8                         @ 0811158a 35d0
    ldr r1, DAT_081115b0                     @ 0811158c 0849
    ldr r0,[r1,#0x0]                         @ 0811158e 0868
    adds r0,r0,r4    @ 08111590 0019
    str r0,[r1,#0x0]                         @ 08111592 0860
    ldr r1, DAT_081115b4                     @ 08111594 0749
    str r5,[r1,#0x8]                         @ 08111596 8d60
    subs r0,r2,r5    @ 08111598 501b
    adds r2,r0,r4    @ 0811159a 0219
    movs r3,#0x1    @ 0811159c 0123
    orrs r2,r3    @ 0811159e 1a43
    str r2,[r5,#0x4]                         @ 081115a0 6a60
    cmp r8,r1                                @ 081115a2 8845
    beq LAB_081115e0                         @ 081115a4 1cd0
    cmp r7,#0xf                              @ 081115a6 0f2f
    bhi LAB_081115b8                         @ 081115a8 06d8
    str r3,[r5,#0x4]                         @ 081115aa 6b60
    b LAB_081115f8                           @ 081115ac 24e0
    .zero  0x2
DAT_081115b0:
    .word  0x09ed51b4                     @ 081115b0 b451ed09
DAT_081115b4:
    .word  0x09ed4d98                     @ 081115b4 984ded09
LAB_081115b8:
    subs r7,#0xc    @ 081115b8 0c3f
    movs r0,#0x8    @ 081115ba 0820
    rsbs r0,r0,#0    @ 081115bc 4042
    ands r7,r0    @ 081115be 0740
    .hword 0x4642    @ 081115c0 4246
    ldr r0,[r2,#0x4]                         @ 081115c2 5068
    ands r0,r3    @ 081115c4 1840
    orrs r0,r7    @ 081115c6 3843
    str r0,[r2,#0x4]                         @ 081115c8 5060
    adds r1,r2,r7    @ 081115ca d119
    movs r0,#0x5    @ 081115cc 0520
    str r0,[r1,#0x4]                         @ 081115ce 4860
    str r0,[r1,#0x8]                         @ 081115d0 8860
    cmp r7,#0xf                              @ 081115d2 0f2f
    bls LAB_081115e0                         @ 081115d4 04d9
    .hword 0x4641    @ 081115d6 4146
    adds r1,#0x8    @ 081115d8 0831
    ldr r0,[sp,#0x0]                         @ 081115da 0098
    bl _free_r                               @ 081115dc fff79cfd
LAB_081115e0:
    ldr r0, DAT_08111604                     @ 081115e0 0848
    ldr r2, DAT_08111608                     @ 081115e2 094a
    ldr r1,[r0,#0x0]                         @ 081115e4 0168
    ldr r0,[r2,#0x0]                         @ 081115e6 1068
    cmp r1,r0                                @ 081115e8 8142
    bls LAB_081115ee                         @ 081115ea 00d9
    str r1,[r2,#0x0]                         @ 081115ec 1160
LAB_081115ee:
    ldr r2, DAT_0811160c                     @ 081115ee 074a
    ldr r0,[r2,#0x0]                         @ 081115f0 1068
    cmp r1,r0                                @ 081115f2 8142
    bls LAB_081115f8                         @ 081115f4 00d9
    str r1,[r2,#0x0]                         @ 081115f6 1160
LAB_081115f8:
    add sp,#0x4                              @ 081115f8 01b0
    pop {r3,r4,r5}                           @ 081115fa 38bc
    .hword 0x4698    @ 081115fc 9846
    .hword 0x46a1    @ 081115fe a146
    .hword 0x46aa    @ 08111600 aa46
    pop {r4,r5,r6,r7,pc}                     @ 08111602 f0bd
DAT_08111604:
    .word  0x09ed51b4                     @ 08111604 b451ed09
DAT_08111608:
    .word  0x09ed51ac                     @ 08111608 ac51ed09
DAT_0811160c:
    .word  0x09ed51b0                     @ 0811160c b051ed09
_malloc_r:
    push {r4,r5,r6,r7,lr}                    @ 08111610 f0b5
    .hword 0x4657    @ 08111612 5746
    .hword 0x464e    @ 08111614 4e46
    .hword 0x4645    @ 08111616 4546
    push {r5,r6,r7}                          @ 08111618 e0b4
    sub sp,#0x8                              @ 0811161a 82b0
    str r0,[sp,#0x0]                         @ 0811161c 0090
    adds r1,#0xb    @ 0811161e 0b31
    cmp r1,#0x16                             @ 08111620 1629
    ble LAB_08111632                         @ 08111622 06dd
    movs r0,#0x8    @ 08111624 0820
    rsbs r0,r0,#0    @ 08111626 4042
    .hword 0x4680    @ 08111628 8046
    .hword 0x4642    @ 0811162a 4246
    ands r2,r1    @ 0811162c 0a40
    .hword 0x4690    @ 0811162e 9046
    b LAB_08111636                           @ 08111630 01e0
LAB_08111632:
    movs r3,#0x10    @ 08111632 1023
    .hword 0x4698    @ 08111634 9846
LAB_08111636:
    ldr r0,[sp,#0x0]                         @ 08111636 0098
    bl stub_malloc_lock                      @ 08111638 00f0caf9
    ldr r0, DAT_0811167c                     @ 0811163c 0f48
    cmp r8,r0                                @ 0811163e 8045
    bhi LAB_0811168a                         @ 08111640 23d8
    .hword 0x4644    @ 08111642 4446
    lsrs r4,r4,#0x3    @ 08111644 e408
    .hword 0x46a4    @ 08111646 a446
    ldr r0, DAT_08111680                     @ 08111648 0d48
    .hword 0x4647    @ 0811164a 4746
    adds r2,r7,r0    @ 0811164c 3a18
    ldr r5,[r2,#0xc]                         @ 0811164e d568
    cmp r5,r2                                @ 08111650 9542
    bne LAB_0811165e                         @ 08111652 04d1
    adds r2,r5,#0x0    @ 08111654 2a1c
    adds r2,#0x8    @ 08111656 0832
    ldr r5,[r2,#0xc]                         @ 08111658 d568
    cmp r5,r2                                @ 0811165a 9542
    beq LAB_08111684                         @ 0811165c 12d0
LAB_0811165e:
    ldr r2,[r5,#0x4]                         @ 0811165e 6a68
    movs r0,#0x4    @ 08111660 0420
    rsbs r0,r0,#0    @ 08111662 4042
    ands r2,r0    @ 08111664 0240
    ldr r6,[r5,#0xc]                         @ 08111666 ee68
    ldr r4,[r5,#0x8]                         @ 08111668 ac68
    str r6,[r4,#0xc]                         @ 0811166a e660
    str r4,[r6,#0x8]                         @ 0811166c b460
    adds r2,r5,r2    @ 0811166e aa18
    ldr r0,[r2,#0x4]                         @ 08111670 5068
    movs r1,#0x1    @ 08111672 0121
    orrs r0,r1    @ 08111674 0843
    str r0,[r2,#0x4]                         @ 08111676 5060
    b LAB_081119b6                           @ 08111678 9de1
    .zero  0x2
DAT_0811167c:
    .word  0x000001f7                     @ 0811167c f7010000
DAT_08111680:
    .word  0x09ed4d98                     @ 08111680 984ded09
LAB_08111684:
    movs r0,#0x2    @ 08111684 0220
    add r12,r0                               @ 08111686 8444
    b LAB_08111736                           @ 08111688 55e0
LAB_0811168a:
    .hword 0x4642    @ 0811168a 4246
    lsrs r1,r2,#0x9    @ 0811168c 510a
    cmp r1,#0x0                              @ 0811168e 0029
    bne LAB_08111696                         @ 08111690 01d1
    lsrs r2,r2,#0x3    @ 08111692 d208
    b LAB_081116e6                           @ 08111694 27e0
LAB_08111696:
    cmp r1,#0x4                              @ 08111696 0429
    bhi LAB_081116a4                         @ 08111698 04d8
    .hword 0x4643    @ 0811169a 4346
    lsrs r0,r3,#0x6    @ 0811169c 9809
    adds r0,#0x38    @ 0811169e 3830
    .hword 0x4684    @ 081116a0 8446
    b LAB_081116e8                           @ 081116a2 21e0
LAB_081116a4:
    cmp r1,#0x14                             @ 081116a4 1429
    bhi LAB_081116ae                         @ 081116a6 02d8
    adds r1,#0x5b    @ 081116a8 5b31
    .hword 0x468c    @ 081116aa 8c46
    b LAB_081116e8                           @ 081116ac 1ce0
LAB_081116ae:
    cmp r1,#0x54                             @ 081116ae 5429
    bhi LAB_081116bc                         @ 081116b0 04d8
    .hword 0x4644    @ 081116b2 4446
    lsrs r0,r4,#0xc    @ 081116b4 200b
    adds r0,#0x6e    @ 081116b6 6e30
    .hword 0x4684    @ 081116b8 8446
    b LAB_081116e8                           @ 081116ba 15e0
LAB_081116bc:
    movs r0,#0xaa    @ 081116bc aa20
    lsls r0,r0,#0x1    @ 081116be 4000
    cmp r1,r0                                @ 081116c0 8142
    bhi LAB_081116ce                         @ 081116c2 04d8
    .hword 0x4647    @ 081116c4 4746
    lsrs r0,r7,#0xf    @ 081116c6 f80b
    adds r0,#0x77    @ 081116c8 7730
    .hword 0x4684    @ 081116ca 8446
    b LAB_081116e8                           @ 081116cc 0ce0
LAB_081116ce:
    ldr r0, DAT_081116e0                     @ 081116ce 0448
    cmp r1,r0                                @ 081116d0 8142
    bhi LAB_081116e4                         @ 081116d2 07d8
    .hword 0x4641    @ 081116d4 4146
    lsrs r0,r1,#0x12    @ 081116d6 880c
    adds r0,#0x7c    @ 081116d8 7c30
    .hword 0x4684    @ 081116da 8446
    b LAB_081116e8                           @ 081116dc 04e0
    .zero  0x2
DAT_081116e0:
    .word  0x00000554                     @ 081116e0 54050000
LAB_081116e4:
    movs r2,#0x7e    @ 081116e4 7e22
LAB_081116e6:
    .hword 0x4694    @ 081116e6 9446
LAB_081116e8:
    .hword 0x4663    @ 081116e8 6346
    lsls r0,r3,#0x3    @ 081116ea d800
    ldr r1, DAT_0811170c                     @ 081116ec 0749
    adds r4,r0,r1    @ 081116ee 4418
    ldr r5,[r4,#0xc]                         @ 081116f0 e568
    cmp r5,r4                                @ 081116f2 a542
    beq LAB_08111732                         @ 081116f4 1dd0
    ldr r1,[r5,#0x4]                         @ 081116f6 6968
    movs r0,#0x4    @ 081116f8 0420
    rsbs r0,r0,#0    @ 081116fa 4042
    ands r1,r0    @ 081116fc 0140
    .hword 0x4647    @ 081116fe 4746
    subs r3,r1,r7    @ 08111700 cb1b
    cmp r3,#0xf                              @ 08111702 0f2b
    ble LAB_08111710                         @ 08111704 04dd
    adds r0,#0x3    @ 08111706 0330
    add r12,r0                               @ 08111708 8444
    b LAB_08111732                           @ 0811170a 12e0
DAT_0811170c:
    .word  0x09ed4d98                     @ 0811170c 984ded09
LAB_08111710:
    cmp r3,#0x0                              @ 08111710 002b
    blt LAB_08111716                         @ 08111712 00db
    b LAB_08111950                           @ 08111714 1ce1
LAB_08111716:
    ldr r5,[r5,#0xc]                         @ 08111716 ed68
    cmp r5,r4                                @ 08111718 a542
    beq LAB_08111732                         @ 0811171a 0ad0
    ldr r1,[r5,#0x4]                         @ 0811171c 6968
    movs r0,#0x4    @ 0811171e 0420
    rsbs r0,r0,#0    @ 08111720 4042
    ands r1,r0    @ 08111722 0140
    .hword 0x4642    @ 08111724 4246
    subs r3,r1,r2    @ 08111726 8b1a
    cmp r3,#0xf                              @ 08111728 0f2b
    ble LAB_08111710                         @ 0811172a f1dd
    movs r3,#0x1    @ 0811172c 0123
    rsbs r3,r3,#0    @ 0811172e 5b42
    add r12,r3                               @ 08111730 9c44
LAB_08111732:
    movs r4,#0x1    @ 08111732 0124
    add r12,r4                               @ 08111734 a444
LAB_08111736:
    ldr r0, DAT_08111774                     @ 08111736 0f48
    ldr r5,[r0,#0x8]                         @ 08111738 8568
    .hword 0x4682    @ 0811173a 8246
    cmp r5,r10                               @ 0811173c 5545
    bne LAB_08111742                         @ 0811173e 00d1
    b LAB_08111844                           @ 08111740 80e0
LAB_08111742:
    ldr r1,[r5,#0x4]                         @ 08111742 6968
    movs r0,#0x4    @ 08111744 0420
    rsbs r0,r0,#0    @ 08111746 4042
    ands r1,r0    @ 08111748 0140
    .hword 0x4647    @ 0811174a 4746
    subs r3,r1,r7    @ 0811174c cb1b
    cmp r3,#0xf                              @ 0811174e 0f2b
    ble LAB_08111778                         @ 08111750 12dd
    adds r2,r5,r7    @ 08111752 ea19
    movs r1,#0x1    @ 08111754 0121
    adds r0,r7,#0x0    @ 08111756 381c
    orrs r0,r1    @ 08111758 0843
    str r0,[r5,#0x4]                         @ 0811175a 6860
    .hword 0x4654    @ 0811175c 5446
    str r2,[r4,#0xc]                         @ 0811175e e260
    str r2,[r4,#0x8]                         @ 08111760 a260
    str r4,[r2,#0xc]                         @ 08111762 d460
    str r4,[r2,#0x8]                         @ 08111764 9460
    adds r0,r3,#0x0    @ 08111766 181c
    orrs r0,r1    @ 08111768 0843
    str r0,[r2,#0x4]                         @ 0811176a 5060
    adds r0,r2,r3    @ 0811176c d018
    str r3,[r0,#0x0]                         @ 0811176e 0360
    b LAB_081119b6                           @ 08111770 21e1
    .zero  0x2
DAT_08111774:
    .word  0x09ed4da0                     @ 08111774 a04ded09
LAB_08111778:
    .hword 0x4657    @ 08111778 5746
    str r7,[r7,#0xc]                         @ 0811177a ff60
    str r7,[r7,#0x8]                         @ 0811177c bf60
    cmp r3,#0x0                              @ 0811177e 002b
    blt LAB_0811178e                         @ 08111780 05db
    adds r2,r5,r1    @ 08111782 6a18
    ldr r0,[r2,#0x4]                         @ 08111784 5068
    movs r1,#0x1    @ 08111786 0121
    orrs r0,r1    @ 08111788 0843
    str r0,[r2,#0x4]                         @ 0811178a 5060
    b LAB_081119b6                           @ 0811178c 13e1
LAB_0811178e:
    ldr r0, DAT_081117b0                     @ 0811178e 0848
    cmp r1,r0                                @ 08111790 8142
    bhi LAB_081117b4                         @ 08111792 0fd8
    lsrs r2,r1,#0x3    @ 08111794 ca08
    .hword 0x4653    @ 08111796 5346
    subs r3,#0x8    @ 08111798 083b
    adds r0,r2,#0x0    @ 0811179a 101c
    asrs r0,r0,#0x2    @ 0811179c 8010
    movs r1,#0x1    @ 0811179e 0121
    lsls r1,r0    @ 081117a0 8140
    ldr r0,[r3,#0x4]                         @ 081117a2 5868
    orrs r0,r1    @ 081117a4 0843
    str r0,[r3,#0x4]                         @ 081117a6 5860
    lsls r0,r2,#0x3    @ 081117a8 d000
    adds r6,r0,r3    @ 081117aa c618
    ldr r4,[r6,#0x8]                         @ 081117ac b468
    b LAB_0811183c                           @ 081117ae 45e0
DAT_081117b0:
    .word  0x000001ff                     @ 081117b0 ff010000
LAB_081117b4:
    lsrs r2,r1,#0x9    @ 081117b4 4a0a
    cmp r2,#0x0                              @ 081117b6 002a
    bne LAB_081117be                         @ 081117b8 01d1
    lsrs r2,r1,#0x3    @ 081117ba ca08
    b LAB_08111802                           @ 081117bc 21e0
LAB_081117be:
    cmp r2,#0x4                              @ 081117be 042a
    bhi LAB_081117ca                         @ 081117c0 03d8
    lsrs r0,r1,#0x6    @ 081117c2 8809
    adds r2,r0,#0x0    @ 081117c4 021c
    adds r2,#0x38    @ 081117c6 3832
    b LAB_08111802                           @ 081117c8 1be0
LAB_081117ca:
    cmp r2,#0x14                             @ 081117ca 142a
    bhi LAB_081117d2                         @ 081117cc 01d8
    adds r2,#0x5b    @ 081117ce 5b32
    b LAB_08111802                           @ 081117d0 17e0
LAB_081117d2:
    cmp r2,#0x54                             @ 081117d2 542a
    bhi LAB_081117de                         @ 081117d4 03d8
    lsrs r0,r1,#0xc    @ 081117d6 080b
    adds r2,r0,#0x0    @ 081117d8 021c
    adds r2,#0x6e    @ 081117da 6e32
    b LAB_08111802                           @ 081117dc 11e0
LAB_081117de:
    movs r0,#0xaa    @ 081117de aa20
    lsls r0,r0,#0x1    @ 081117e0 4000
    cmp r2,r0                                @ 081117e2 8242
    bhi LAB_081117ee                         @ 081117e4 03d8
    lsrs r0,r1,#0xf    @ 081117e6 c80b
    adds r2,r0,#0x0    @ 081117e8 021c
    adds r2,#0x77    @ 081117ea 7732
    b LAB_08111802                           @ 081117ec 09e0
LAB_081117ee:
    ldr r0, DAT_081117fc                     @ 081117ee 0348
    cmp r2,r0                                @ 081117f0 8242
    bhi LAB_08111800                         @ 081117f2 05d8
    lsrs r0,r1,#0x12    @ 081117f4 880c
    adds r2,r0,#0x0    @ 081117f6 021c
    adds r2,#0x7c    @ 081117f8 7c32
    b LAB_08111802                           @ 081117fa 02e0
DAT_081117fc:
    .word  0x00000554                     @ 081117fc 54050000
LAB_08111800:
    movs r2,#0x7e    @ 08111800 7e22
LAB_08111802:
    lsls r0,r2,#0x3    @ 08111802 d000
    ldr r3, DAT_08111820                     @ 08111804 064b
    adds r6,r0,r3    @ 08111806 c618
    ldr r4,[r6,#0x8]                         @ 08111808 b468
    cmp r4,r6                                @ 0811180a b442
    bne LAB_08111824                         @ 0811180c 0ad1
    adds r0,r2,#0x0    @ 0811180e 101c
    asrs r0,r0,#0x2    @ 08111810 8010
    movs r1,#0x1    @ 08111812 0121
    lsls r1,r0    @ 08111814 8140
    ldr r7, DAT_08111820                     @ 08111816 024f
    ldr r0,[r7,#0x4]                         @ 08111818 7868
    orrs r0,r1    @ 0811181a 0843
    str r0,[r7,#0x4]                         @ 0811181c 7860
    b LAB_0811183c                           @ 0811181e 0de0
DAT_08111820:
    .word  0x09ed4d98                     @ 08111820 984ded09
LAB_08111824:
    ldr r0,[r4,#0x4]                         @ 08111824 6068
    movs r2,#0x4    @ 08111826 0422
    rsbs r2,r2,#0    @ 08111828 5242
    b LAB_08111834                           @ 0811182a 03e0
LAB_0811182c:
    ldr r4,[r4,#0x8]                         @ 0811182c a468
    cmp r4,r6                                @ 0811182e b442
    beq LAB_0811183a                         @ 08111830 03d0
    ldr r0,[r4,#0x4]                         @ 08111832 6068
LAB_08111834:
    ands r0,r2    @ 08111834 1040
    cmp r1,r0                                @ 08111836 8142
    bcc LAB_0811182c                         @ 08111838 f8d3
LAB_0811183a:
    ldr r6,[r4,#0xc]                         @ 0811183a e668
LAB_0811183c:
    str r6,[r5,#0xc]                         @ 0811183c ee60
    str r4,[r5,#0x8]                         @ 0811183e ac60
    str r5,[r6,#0x8]                         @ 08111840 b560
    str r5,[r4,#0xc]                         @ 08111842 e560
LAB_08111844:
    .hword 0x4660    @ 08111844 6046
    cmp r0,#0x0                              @ 08111846 0028
    bge LAB_0811184c                         @ 08111848 00da
    adds r0,#0x3    @ 0811184a 0330
LAB_0811184c:
    asrs r0,r0,#0x2    @ 0811184c 8010
    movs r6,#0x1    @ 0811184e 0126
    lsls r6,r0    @ 08111850 8640
    ldr r0, DAT_08111870                     @ 08111852 0748
    ldr r1,[r0,#0x4]                         @ 08111854 4168
    cmp r6,r1                                @ 08111856 8e42
    bhi LAB_0811190e                         @ 08111858 59d8
    adds r0,r6,#0x0    @ 0811185a 301c
    ands r0,r1    @ 0811185c 0840
    cmp r0,#0x0                              @ 0811185e 0028
    bne LAB_08111882                         @ 08111860 0fd1
    movs r0,#0x4    @ 08111862 0420
    rsbs r0,r0,#0    @ 08111864 4042
    .hword 0x4662    @ 08111866 6246
    ands r0,r2    @ 08111868 1040
    adds r0,#0x4    @ 0811186a 0430
    .hword 0x4684    @ 0811186c 8446
    b LAB_08111878                           @ 0811186e 03e0
DAT_08111870:
    .word  0x09ed4d98                     @ 08111870 984ded09
LAB_08111874:
    movs r3,#0x4    @ 08111874 0423
    add r12,r3                               @ 08111876 9c44
LAB_08111878:
    lsls r6,r6,#0x1    @ 08111878 7600
    adds r0,r6,#0x0    @ 0811187a 301c
    ands r0,r1    @ 0811187c 0840
    cmp r0,#0x0                              @ 0811187e 0028
    beq LAB_08111874                         @ 08111880 f8d0
LAB_08111882:
    ldr r4, DAT_08111900                     @ 08111882 1f4c
    .hword 0x46a1    @ 08111884 a146
LAB_08111886:
    .hword 0x4667    @ 08111886 6746
    str r7,[sp,#0x4]                         @ 08111888 0197
    .hword 0x4661    @ 0811188a 6146
    lsls r0,r1,#0x3    @ 0811188c c800
    .hword 0x464b    @ 0811188e 4b46
    adds r2,r0,r3    @ 08111890 c218
    adds r4,r2,#0x0    @ 08111892 141c
LAB_08111894:
    ldr r5,[r4,#0xc]                         @ 08111894 e568
    cmp r5,r4                                @ 08111896 a542
    beq LAB_081118b4                         @ 08111898 0cd0
    movs r0,#0x4    @ 0811189a 0420
    rsbs r0,r0,#0    @ 0811189c 4042
LAB_0811189e:
    ldr r1,[r5,#0x4]                         @ 0811189e 6968
    ands r1,r0    @ 081118a0 0140
    .hword 0x4647    @ 081118a2 4746
    subs r3,r1,r7    @ 081118a4 cb1b
    cmp r3,#0xf                              @ 081118a6 0f2b
    bgt LAB_08111964                         @ 081118a8 5cdc
    cmp r3,#0x0                              @ 081118aa 002b
    bge LAB_0811198c                         @ 081118ac 6eda
    ldr r5,[r5,#0xc]                         @ 081118ae ed68
    cmp r5,r4                                @ 081118b0 a542
    bne LAB_0811189e                         @ 081118b2 f4d1
LAB_081118b4:
    adds r4,#0x8    @ 081118b4 0834
    movs r0,#0x1    @ 081118b6 0120
    add r12,r0                               @ 081118b8 8444
    .hword 0x4660    @ 081118ba 6046
    movs r1,#0x3    @ 081118bc 0321
    ands r0,r1    @ 081118be 0840
    cmp r0,#0x0                              @ 081118c0 0028
    bne LAB_08111894                         @ 081118c2 e7d1
LAB_081118c4:
    ldr r0,[sp,#0x4]                         @ 081118c4 0198
    ands r0,r1    @ 081118c6 0840
    cmp r0,#0x0                              @ 081118c8 0028
    beq LAB_08111904                         @ 081118ca 1bd0
    ldr r3,[sp,#0x4]                         @ 081118cc 019b
    subs r3,#0x1    @ 081118ce 013b
    str r3,[sp,#0x4]                         @ 081118d0 0193
    subs r2,#0x8    @ 081118d2 083a
    ldr r0,[r2,#0x8]                         @ 081118d4 9068
    cmp r0,r2                                @ 081118d6 9042
    beq LAB_081118c4                         @ 081118d8 f4d0
LAB_081118da:
    lsls r6,r6,#0x1    @ 081118da 7600
    .hword 0x464c    @ 081118dc 4c46
    ldr r1,[r4,#0x4]                         @ 081118de 6168
    cmp r6,r1                                @ 081118e0 8e42
    bhi LAB_0811190e                         @ 081118e2 14d8
    cmp r6,#0x0                              @ 081118e4 002e
    beq LAB_0811190e                         @ 081118e6 12d0
    adds r0,r6,#0x0    @ 081118e8 301c
    ands r0,r1    @ 081118ea 0840
    cmp r0,#0x0                              @ 081118ec 0028
    bne LAB_08111886                         @ 081118ee cad1
LAB_081118f0:
    movs r7,#0x4    @ 081118f0 0427
    add r12,r7                               @ 081118f2 bc44
    lsls r6,r6,#0x1    @ 081118f4 7600
    adds r0,r6,#0x0    @ 081118f6 301c
    ands r0,r1    @ 081118f8 0840
    cmp r0,#0x0                              @ 081118fa 0028
    beq LAB_081118f0                         @ 081118fc f8d0
    b LAB_08111886                           @ 081118fe c2e7
DAT_08111900:
    .word  0x09ed4d98                     @ 08111900 984ded09
LAB_08111904:
    .hword 0x4649    @ 08111904 4946
    ldr r0,[r1,#0x4]                         @ 08111906 4868
    bics r0,r6    @ 08111908 b043
    str r0,[r1,#0x4]                         @ 0811190a 4860
    b LAB_081118da                           @ 0811190c e5e7
LAB_0811190e:
    ldr r2, DAT_0811194c                     @ 0811190e 0f4a
    ldr r0,[r2,#0x8]                         @ 08111910 9068
    ldr r0,[r0,#0x4]                         @ 08111912 4068
    movs r4,#0x4    @ 08111914 0424
    rsbs r4,r4,#0    @ 08111916 6442
    ands r0,r4    @ 08111918 2040
    .hword 0x4647    @ 0811191a 4746
    subs r3,r0,r7    @ 0811191c c31b
    cmp r0,r8                                @ 0811191e 4045
    bcc LAB_08111926                         @ 08111920 01d3
    cmp r3,#0xf                              @ 08111922 0f2b
    bgt LAB_081119a0                         @ 08111924 3cdc
LAB_08111926:
    ldr r0,[sp,#0x0]                         @ 08111926 0098
    .hword 0x4641    @ 08111928 4146
    bl grow_heap_via_sbrk                    @ 0811192a fff7c3fd
    ldr r1, DAT_0811194c                     @ 0811192e 0749
    ldr r0,[r1,#0x8]                         @ 08111930 8868
    ldr r0,[r0,#0x4]                         @ 08111932 4068
    ands r0,r4    @ 08111934 2040
    .hword 0x4642    @ 08111936 4246
    subs r3,r0,r2    @ 08111938 831a
    cmp r0,r8                                @ 0811193a 4045
    bcc LAB_08111942                         @ 0811193c 01d3
    cmp r3,#0xf                              @ 0811193e 0f2b
    bgt LAB_081119a0                         @ 08111940 2edc
LAB_08111942:
    ldr r0,[sp,#0x0]                         @ 08111942 0098
    bl stub_malloc_unlock                    @ 08111944 00f046f8
    movs r0,#0x0    @ 08111948 0020
    b LAB_081119c0                           @ 0811194a 39e0
DAT_0811194c:
    .word  0x09ed4d98                     @ 0811194c 984ded09
LAB_08111950:
    ldr r6,[r5,#0xc]                         @ 08111950 ee68
    ldr r4,[r5,#0x8]                         @ 08111952 ac68
    str r6,[r4,#0xc]                         @ 08111954 e660
    str r4,[r6,#0x8]                         @ 08111956 b460
    adds r2,r5,r1    @ 08111958 6a18
    ldr r0,[r2,#0x4]                         @ 0811195a 5068
    movs r1,#0x1    @ 0811195c 0121
    orrs r0,r1    @ 0811195e 0843
    str r0,[r2,#0x4]                         @ 08111960 5060
    b LAB_081119b6                           @ 08111962 28e0
LAB_08111964:
    .hword 0x4644    @ 08111964 4446
    adds r2,r5,r4    @ 08111966 2a19
    movs r1,#0x1    @ 08111968 0121
    orrs r4,r1    @ 0811196a 0c43
    str r4,[r5,#0x4]                         @ 0811196c 6c60
    ldr r6,[r5,#0xc]                         @ 0811196e ee68
    ldr r4,[r5,#0x8]                         @ 08111970 ac68
    str r6,[r4,#0xc]                         @ 08111972 e660
    str r4,[r6,#0x8]                         @ 08111974 b460
    .hword 0x4657    @ 08111976 5746
    str r2,[r7,#0xc]                         @ 08111978 fa60
    str r2,[r7,#0x8]                         @ 0811197a ba60
    str r7,[r2,#0xc]                         @ 0811197c d760
    str r7,[r2,#0x8]                         @ 0811197e 9760
    adds r0,r3,#0x0    @ 08111980 181c
    orrs r0,r1    @ 08111982 0843
    str r0,[r2,#0x4]                         @ 08111984 5060
    adds r0,r2,r3    @ 08111986 d018
    str r3,[r0,#0x0]                         @ 08111988 0360
    b LAB_081119b6                           @ 0811198a 14e0
LAB_0811198c:
    adds r2,r5,r1    @ 0811198c 6a18
    ldr r0,[r2,#0x4]                         @ 0811198e 5068
    movs r1,#0x1    @ 08111990 0121
    orrs r0,r1    @ 08111992 0843
    str r0,[r2,#0x4]                         @ 08111994 5060
    ldr r6,[r5,#0xc]                         @ 08111996 ee68
    ldr r4,[r5,#0x8]                         @ 08111998 ac68
    str r6,[r4,#0xc]                         @ 0811199a e660
    str r4,[r6,#0x8]                         @ 0811199c b460
    b LAB_081119b6                           @ 0811199e 0ae0
LAB_081119a0:
    ldr r2, DAT_081119cc                     @ 081119a0 0a4a
    ldr r5,[r2,#0x8]                         @ 081119a2 9568
    movs r1,#0x1    @ 081119a4 0121
    .hword 0x4640    @ 081119a6 4046
    orrs r0,r1    @ 081119a8 0843
    str r0,[r5,#0x4]                         @ 081119aa 6860
    .hword 0x4644    @ 081119ac 4446
    adds r0,r5,r4    @ 081119ae 2819
    str r0,[r2,#0x8]                         @ 081119b0 9060
    orrs r3,r1    @ 081119b2 0b43
    str r3,[r0,#0x4]                         @ 081119b4 4360
LAB_081119b6:
    ldr r0,[sp,#0x0]                         @ 081119b6 0098
    bl stub_malloc_unlock                    @ 081119b8 00f00cf8
    adds r0,r5,#0x0    @ 081119bc 281c
    adds r0,#0x8    @ 081119be 0830
LAB_081119c0:
    add sp,#0x8                              @ 081119c0 02b0
    pop {r3,r4,r5}                           @ 081119c2 38bc
    .hword 0x4698    @ 081119c4 9846
    .hword 0x46a1    @ 081119c6 a146
    .hword 0x46aa    @ 081119c8 aa46
    pop {r4,r5,r6,r7,pc}                     @ 081119ca f0bd
DAT_081119cc:
    .word  0x09ed4d98                     @ 081119cc 984ded09

@ dlmalloc mutex stub (lock): function body is bx lr only, performs no operation.
@ Called before _free_r / _malloc_r / _malloc_trim_r / _realloc_r enters critical section; replaces real mutex acquire in single-threaded embedded environment.
@ GBA has no RTOS context so locking is a no-op; paired with stub_malloc_unlock (0x081119d4).
stub_malloc_lock:
    bx lr                                    @ 081119d0 7047
    .zero  0x2

@ dlmalloc mutex stub (unlock): function body is bx lr only, performs no operation.
@ Called after _free_r / _malloc_r / _malloc_trim_r / _realloc_r exits critical section; replaces real mutex release in single-threaded embedded environment.
@ GBA has no RTOS context so unlocking is a no-op; paired with stub_malloc_lock (0x081119d0).
stub_malloc_unlock:
    bx lr                                    @ 081119d4 7047
    .zero  0x2
_Balloc:
    push {r4,r5,r6,lr}                       @ 081119d8 70b5
    adds r4,r0,#0x0    @ 081119da 041c
    adds r6,r1,#0x0    @ 081119dc 0e1c
    ldr r0,[r4,#0x4c]                        @ 081119de e06c
    cmp r0,#0x0                              @ 081119e0 0028
    bne LAB_081119f4                         @ 081119e2 07d1
    adds r0,r4,#0x0    @ 081119e4 201c
    movs r1,#0x4    @ 081119e6 0421
    movs r2,#0x10    @ 081119e8 1022
    bl _calloc_r                             @ 081119ea 01f09bf8
    str r0,[r4,#0x4c]                        @ 081119ee e064
    cmp r0,#0x0                              @ 081119f0 0028
    beq LAB_08111a1c                         @ 081119f2 13d0
LAB_081119f4:
    ldr r1,[r4,#0x4c]                        @ 081119f4 e16c
    lsls r0,r6,#0x2    @ 081119f6 b000
    adds r2,r0,r1    @ 081119f8 4218
    ldr r1,[r2,#0x0]                         @ 081119fa 1168
    cmp r1,#0x0                              @ 081119fc 0029
    beq LAB_08111a06                         @ 081119fe 02d0
    ldr r0,[r1,#0x0]                         @ 08111a00 0868
    str r0,[r2,#0x0]                         @ 08111a02 1060
    b LAB_08111a24                           @ 08111a04 0ee0
LAB_08111a06:
    movs r5,#0x1    @ 08111a06 0125
    lsls r5,r6    @ 08111a08 b540
    lsls r2,r5,#0x2    @ 08111a0a aa00
    adds r2,#0x14    @ 08111a0c 1432
    adds r0,r4,#0x0    @ 08111a0e 201c
    movs r1,#0x1    @ 08111a10 0121
    bl _calloc_r                             @ 08111a12 01f087f8
    adds r1,r0,#0x0    @ 08111a16 011c
    cmp r1,#0x0                              @ 08111a18 0029
    bne LAB_08111a20                         @ 08111a1a 01d1
LAB_08111a1c:
    movs r0,#0x0    @ 08111a1c 0020
    b LAB_08111a2c                           @ 08111a1e 05e0
LAB_08111a20:
    str r6,[r1,#0x4]                         @ 08111a20 4e60
    str r5,[r1,#0x8]                         @ 08111a22 8d60
LAB_08111a24:
    movs r0,#0x0    @ 08111a24 0020
    str r0,[r1,#0x10]                        @ 08111a26 0861
    str r0,[r1,#0xc]                         @ 08111a28 c860
    adds r0,r1,#0x0    @ 08111a2a 081c
LAB_08111a2c:
    pop {r4,r5,r6,pc}                        @ 08111a2c 70bd
    .zero  0x2
_Bfree:
    adds r3,r0,#0x0    @ 08111a30 031c
    adds r2,r1,#0x0    @ 08111a32 0a1c
    cmp r2,#0x0                              @ 08111a34 002a
    beq LAB_08111a46                         @ 08111a36 06d0
    ldr r0,[r2,#0x4]                         @ 08111a38 5068
    ldr r1,[r3,#0x4c]                        @ 08111a3a d96c
    lsls r0,r0,#0x2    @ 08111a3c 8000
    adds r0,r0,r1    @ 08111a3e 4018
    ldr r1,[r0,#0x0]                         @ 08111a40 0168
    str r1,[r2,#0x0]                         @ 08111a42 1160
    str r2,[r0,#0x0]                         @ 08111a44 0260
LAB_08111a46:
    bx lr                                    @ 08111a46 7047
_multadd:
    push {r4,r5,r6,r7,lr}                    @ 08111a48 f0b5
    .hword 0x464f    @ 08111a4a 4f46
    .hword 0x4646    @ 08111a4c 4646
    push {r6,r7}                             @ 08111a4e c0b4
    .hword 0x4681    @ 08111a50 8146
    adds r5,r1,#0x0    @ 08111a52 0d1c
    adds r4,r2,#0x0    @ 08111a54 141c
    .hword 0x4698    @ 08111a56 9846
    ldr r6,[r5,#0x10]                        @ 08111a58 2e69
    adds r3,r5,#0x0    @ 08111a5a 2b1c
    adds r3,#0x14    @ 08111a5c 1433
    movs r7,#0x0    @ 08111a5e 0027
    ldr r0, DAT_08111adc                     @ 08111a60 1e48
    .hword 0x4684    @ 08111a62 8446
LAB_08111a64:
    ldr r1,[r3,#0x0]                         @ 08111a64 1968
    adds r0,r1,#0x0    @ 08111a66 081c
    .hword 0x4662    @ 08111a68 6246
    ands r0,r2    @ 08111a6a 1040
    adds r2,r0,#0x0    @ 08111a6c 021c
    muls r2,r4    @ 08111a6e 6243
    add r2,r8                                @ 08111a70 4244
    lsrs r1,r1,#0x10    @ 08111a72 090c
    adds r0,r1,#0x0    @ 08111a74 081c
    muls r0,r4    @ 08111a76 6043
    lsrs r1,r2,#0x10    @ 08111a78 110c
    adds r0,r0,r1    @ 08111a7a 4018
    lsrs r1,r0,#0x10    @ 08111a7c 010c
    .hword 0x4688    @ 08111a7e 8846
    lsls r0,r0,#0x10    @ 08111a80 0004
    .hword 0x4661    @ 08111a82 6146
    ands r2,r1    @ 08111a84 0a40
    adds r0,r0,r2    @ 08111a86 8018
    stmia r3!,{r0}                           @ 08111a88 01c3
    adds r7,#0x1    @ 08111a8a 0137
    cmp r7,r6                                @ 08111a8c b742
    blt LAB_08111a64                         @ 08111a8e e9db
    .hword 0x4642    @ 08111a90 4246
    cmp r2,#0x0                              @ 08111a92 002a
    beq LAB_08111ad2                         @ 08111a94 1dd0
    ldr r0,[r5,#0x8]                         @ 08111a96 a868
    cmp r6,r0                                @ 08111a98 8642
    blt LAB_08111ac2                         @ 08111a9a 12db
    ldr r1,[r5,#0x4]                         @ 08111a9c 6968
    adds r1,#0x1    @ 08111a9e 0131
    .hword 0x4648    @ 08111aa0 4846
    bl _Balloc                               @ 08111aa2 fff799ff
    adds r4,r0,#0x0    @ 08111aa6 041c
    adds r0,#0xc    @ 08111aa8 0c30
    adds r1,r5,#0x0    @ 08111aaa 291c
    adds r1,#0xc    @ 08111aac 0c31
    ldr r2,[r5,#0x10]                        @ 08111aae 2a69
    lsls r2,r2,#0x2    @ 08111ab0 9200
    adds r2,#0x8    @ 08111ab2 0832
    bl memcpy                                @ 08111ab4 fcf752ff
    .hword 0x4648    @ 08111ab8 4846
    adds r1,r5,#0x0    @ 08111aba 291c
    bl _Bfree                                @ 08111abc fff7b8ff
    adds r5,r4,#0x0    @ 08111ac0 251c
LAB_08111ac2:
    lsls r1,r6,#0x2    @ 08111ac2 b100
    adds r0,r5,#0x0    @ 08111ac4 281c
    adds r0,#0x14    @ 08111ac6 1430
    adds r0,r0,r1    @ 08111ac8 4018
    .hword 0x4641    @ 08111aca 4146
    str r1,[r0,#0x0]                         @ 08111acc 0160
    adds r6,#0x1    @ 08111ace 0136
    str r6,[r5,#0x10]                        @ 08111ad0 2e61
LAB_08111ad2:
    adds r0,r5,#0x0    @ 08111ad2 281c
    pop {r3,r4}                              @ 08111ad4 18bc
    .hword 0x4698    @ 08111ad6 9846
    .hword 0x46a1    @ 08111ad8 a146
    pop {r4,r5,r6,r7,pc}                     @ 08111ada f0bd
DAT_08111adc:
    .word  0x0000ffff                     @ 08111adc ffff0000
_s2b:
    push {r4,r5,r6,r7,lr}                    @ 08111ae0 f0b5
    .hword 0x4647    @ 08111ae2 4746
    push {r7}                                @ 08111ae4 80b4
    adds r7,r0,#0x0    @ 08111ae6 071c
    adds r4,r1,#0x0    @ 08111ae8 0c1c
    adds r6,r2,#0x0    @ 08111aea 161c
    .hword 0x4698    @ 08111aec 9846
    .hword 0x4640    @ 08111aee 4046
    adds r0,#0x8    @ 08111af0 0830
    movs r1,#0x9    @ 08111af2 0921
    bl __divsi3                              @ 08111af4 fcf786fd
    movs r1,#0x0    @ 08111af8 0021
    movs r2,#0x1    @ 08111afa 0122
    cmp r0,#0x1                              @ 08111afc 0128
    ble LAB_08111b08                         @ 08111afe 03dd
LAB_08111b00:
    lsls r2,r2,#0x1    @ 08111b00 5200
    adds r1,#0x1    @ 08111b02 0131
    cmp r0,r2                                @ 08111b04 9042
    bgt LAB_08111b00                         @ 08111b06 fbdc
LAB_08111b08:
    adds r0,r7,#0x0    @ 08111b08 381c
    bl _Balloc                               @ 08111b0a fff765ff
    adds r1,r0,#0x0    @ 08111b0e 011c
    ldr r0,[sp,#0x18]                        @ 08111b10 0698
    str r0,[r1,#0x14]                        @ 08111b12 4861
    movs r0,#0x1    @ 08111b14 0120
    str r0,[r1,#0x10]                        @ 08111b16 0861
    movs r5,#0x9    @ 08111b18 0925
    cmp r6,#0x9                              @ 08111b1a 092e
    ble LAB_08111b3a                         @ 08111b1c 0ddd
    adds r4,#0x9    @ 08111b1e 0934
LAB_08111b20:
    ldrb r3,[r4,#0x0]                        @ 08111b20 2378
    subs r3,#0x30    @ 08111b22 303b
    adds r4,#0x1    @ 08111b24 0134
    adds r0,r7,#0x0    @ 08111b26 381c
    movs r2,#0xa    @ 08111b28 0a22
    bl _multadd                              @ 08111b2a fff78dff
    adds r1,r0,#0x0    @ 08111b2e 011c
    adds r5,#0x1    @ 08111b30 0135
    cmp r5,r6                                @ 08111b32 b542
    blt LAB_08111b20                         @ 08111b34 f4db
    adds r4,#0x1    @ 08111b36 0134
    b LAB_08111b3c                           @ 08111b38 00e0
LAB_08111b3a:
    adds r4,#0xa    @ 08111b3a 0a34
LAB_08111b3c:
    cmp r5,r8                                @ 08111b3c 4545
    bge LAB_08111b5a                         @ 08111b3e 0cda
    .hword 0x4640    @ 08111b40 4046
    subs r5,r0,r5    @ 08111b42 451b
LAB_08111b44:
    ldrb r3,[r4,#0x0]                        @ 08111b44 2378
    subs r3,#0x30    @ 08111b46 303b
    adds r4,#0x1    @ 08111b48 0134
    adds r0,r7,#0x0    @ 08111b4a 381c
    movs r2,#0xa    @ 08111b4c 0a22
    bl _multadd                              @ 08111b4e fff77bff
    adds r1,r0,#0x0    @ 08111b52 011c
    subs r5,#0x1    @ 08111b54 013d
    cmp r5,#0x0                              @ 08111b56 002d
    bne LAB_08111b44                         @ 08111b58 f4d1
LAB_08111b5a:
    adds r0,r1,#0x0    @ 08111b5a 081c
    pop {r3}                                 @ 08111b5c 08bc
    .hword 0x4698    @ 08111b5e 9846
    pop {r4,r5,r6,r7,pc}                     @ 08111b60 f0bd
    .zero  0x2
_hi0bits:
    adds r1,r0,#0x0    @ 08111b64 011c
    movs r2,#0x0    @ 08111b66 0022
    ldr r0, DAT_08111bb4                     @ 08111b68 1248
    ands r0,r1    @ 08111b6a 0840
    cmp r0,#0x0                              @ 08111b6c 0028
    bne LAB_08111b74                         @ 08111b6e 01d1
    movs r2,#0x10    @ 08111b70 1022
    lsls r1,r1,#0x10    @ 08111b72 0904
LAB_08111b74:
    movs r0,#0xff    @ 08111b74 ff20
    lsls r0,r0,#0x18    @ 08111b76 0006
    ands r0,r1    @ 08111b78 0840
    cmp r0,#0x0                              @ 08111b7a 0028
    bne LAB_08111b82                         @ 08111b7c 01d1
    adds r2,#0x8    @ 08111b7e 0832
    lsls r1,r1,#0x8    @ 08111b80 0902
LAB_08111b82:
    movs r0,#0xf0    @ 08111b82 f020
    lsls r0,r0,#0x18    @ 08111b84 0006
    ands r0,r1    @ 08111b86 0840
    cmp r0,#0x0                              @ 08111b88 0028
    bne LAB_08111b90                         @ 08111b8a 01d1
    adds r2,#0x4    @ 08111b8c 0432
    lsls r1,r1,#0x4    @ 08111b8e 0901
LAB_08111b90:
    movs r0,#0xc0    @ 08111b90 c020
    lsls r0,r0,#0x18    @ 08111b92 0006
    ands r0,r1    @ 08111b94 0840
    cmp r0,#0x0                              @ 08111b96 0028
    bne LAB_08111b9e                         @ 08111b98 01d1
    adds r2,#0x2    @ 08111b9a 0232
    lsls r1,r1,#0x2    @ 08111b9c 8900
LAB_08111b9e:
    cmp r1,#0x0                              @ 08111b9e 0029
    blt LAB_08111bb8                         @ 08111ba0 0adb
    adds r2,#0x1    @ 08111ba2 0132
    movs r0,#0x80    @ 08111ba4 8020
    lsls r0,r0,#0x17    @ 08111ba6 c005
    ands r0,r1    @ 08111ba8 0840
    cmp r0,#0x0                              @ 08111baa 0028
    bne LAB_08111bb8                         @ 08111bac 04d1
    movs r0,#0x20    @ 08111bae 2020
    b LAB_08111bba                           @ 08111bb0 03e0
    .zero  0x2
DAT_08111bb4:
    .word  0xffff0000                     @ 08111bb4 0000ffff
LAB_08111bb8:
    adds r0,r2,#0x0    @ 08111bb8 101c
LAB_08111bba:
    bx lr                                    @ 08111bba 7047
_lo0bits:
    adds r3,r0,#0x0    @ 08111bbc 031c
    ldr r1,[r3,#0x0]                         @ 08111bbe 1968
    movs r0,#0x7    @ 08111bc0 0720
    ands r0,r1    @ 08111bc2 0840
    cmp r0,#0x0                              @ 08111bc4 0028
    beq LAB_08111bec                         @ 08111bc6 11d0
    movs r0,#0x1    @ 08111bc8 0120
    ands r0,r1    @ 08111bca 0840
    cmp r0,#0x0                              @ 08111bcc 0028
    beq LAB_08111bd4                         @ 08111bce 01d0
    movs r0,#0x0    @ 08111bd0 0020
    b LAB_08111c3c                           @ 08111bd2 33e0
LAB_08111bd4:
    movs r0,#0x2    @ 08111bd4 0220
    ands r0,r1    @ 08111bd6 0840
    cmp r0,#0x0                              @ 08111bd8 0028
    beq LAB_08111be4                         @ 08111bda 03d0
    lsrs r0,r1,#0x1    @ 08111bdc 4808
    str r0,[r3,#0x0]                         @ 08111bde 1860
    movs r0,#0x1    @ 08111be0 0120
    b LAB_08111c3c                           @ 08111be2 2be0
LAB_08111be4:
    lsrs r0,r1,#0x2    @ 08111be4 8808
    str r0,[r3,#0x0]                         @ 08111be6 1860
    movs r0,#0x2    @ 08111be8 0220
    b LAB_08111c3c                           @ 08111bea 27e0
LAB_08111bec:
    movs r2,#0x0    @ 08111bec 0022
    ldr r0, DAT_08111c34                     @ 08111bee 1148
    ands r0,r1    @ 08111bf0 0840
    cmp r0,#0x0                              @ 08111bf2 0028
    bne LAB_08111bfa                         @ 08111bf4 01d1
    movs r2,#0x10    @ 08111bf6 1022
    lsrs r1,r1,#0x10    @ 08111bf8 090c
LAB_08111bfa:
    movs r0,#0xff    @ 08111bfa ff20
    ands r0,r1    @ 08111bfc 0840
    cmp r0,#0x0                              @ 08111bfe 0028
    bne LAB_08111c06                         @ 08111c00 01d1
    adds r2,#0x8    @ 08111c02 0832
    lsrs r1,r1,#0x8    @ 08111c04 090a
LAB_08111c06:
    movs r0,#0xf    @ 08111c06 0f20
    ands r0,r1    @ 08111c08 0840
    cmp r0,#0x0                              @ 08111c0a 0028
    bne LAB_08111c12                         @ 08111c0c 01d1
    adds r2,#0x4    @ 08111c0e 0432
    lsrs r1,r1,#0x4    @ 08111c10 0909
LAB_08111c12:
    movs r0,#0x3    @ 08111c12 0320
    ands r0,r1    @ 08111c14 0840
    cmp r0,#0x0                              @ 08111c16 0028
    bne LAB_08111c1e                         @ 08111c18 01d1
    adds r2,#0x2    @ 08111c1a 0232
    lsrs r1,r1,#0x2    @ 08111c1c 8908
LAB_08111c1e:
    movs r0,#0x1    @ 08111c1e 0120
    ands r0,r1    @ 08111c20 0840
    cmp r0,#0x0                              @ 08111c22 0028
    bne LAB_08111c38                         @ 08111c24 08d1
    adds r2,#0x1    @ 08111c26 0132
    lsrs r1,r1,#0x1    @ 08111c28 4908
    cmp r1,#0x0                              @ 08111c2a 0029
    bne LAB_08111c38                         @ 08111c2c 04d1
    movs r0,#0x20    @ 08111c2e 2020
    b LAB_08111c3c                           @ 08111c30 04e0
    .zero  0x2
DAT_08111c34:
    .word  0x0000ffff                     @ 08111c34 ffff0000
LAB_08111c38:
    str r1,[r3,#0x0]                         @ 08111c38 1960
    adds r0,r2,#0x0    @ 08111c3a 101c
LAB_08111c3c:
    bx lr                                    @ 08111c3c 7047
    .zero  0x2
_i2b:
    push {r4,lr}                             @ 08111c40 10b5
    adds r4,r1,#0x0    @ 08111c42 0c1c
    movs r1,#0x1    @ 08111c44 0121
    bl _Balloc                               @ 08111c46 fff7c7fe
    str r4,[r0,#0x14]                        @ 08111c4a 4461
    movs r1,#0x1    @ 08111c4c 0121
    str r1,[r0,#0x10]                        @ 08111c4e 0161
    pop {r4,pc}                              @ 08111c50 10bd
    .zero  0x2
_multiply:
    push {r4,r5,r6,r7,lr}                    @ 08111c54 f0b5
    .hword 0x4657    @ 08111c56 5746
    .hword 0x464e    @ 08111c58 4e46
    .hword 0x4645    @ 08111c5a 4546
    push {r5,r6,r7}                          @ 08111c5c e0b4
    sub sp,#0x24                             @ 08111c5e 89b0
    adds r3,r0,#0x0    @ 08111c60 031c
    adds r4,r1,#0x0    @ 08111c62 0c1c
    adds r5,r2,#0x0    @ 08111c64 151c
    ldr r1,[r4,#0x10]                        @ 08111c66 2169
    ldr r0,[r5,#0x10]                        @ 08111c68 2869
    cmp r1,r0                                @ 08111c6a 8142
    bge LAB_08111c74                         @ 08111c6c 02da
    str r4,[sp,#0x0]                         @ 08111c6e 0094
    adds r4,r5,#0x0    @ 08111c70 2c1c
    ldr r5,[sp,#0x0]                         @ 08111c72 009d
LAB_08111c74:
    ldr r1,[r4,#0x4]                         @ 08111c74 6168
    ldr r6,[r4,#0x10]                        @ 08111c76 2669
    ldr r0,[r5,#0x10]                        @ 08111c78 2869
    .hword 0x4680    @ 08111c7a 8046
    .hword 0x4642    @ 08111c7c 4246
    adds r2,r6,r2    @ 08111c7e b218
    str r2,[sp,#0x4]                         @ 08111c80 0192
    ldr r0,[r4,#0x8]                         @ 08111c82 a068
    cmp r2,r0                                @ 08111c84 8242
    ble LAB_08111c8a                         @ 08111c86 00dd
    adds r1,#0x1    @ 08111c88 0131
LAB_08111c8a:
    adds r0,r3,#0x0    @ 08111c8a 181c
    bl _Balloc                               @ 08111c8c fff7a4fe
    str r0,[sp,#0x0]                         @ 08111c90 0090
    adds r7,r0,#0x0    @ 08111c92 071c
    adds r7,#0x14    @ 08111c94 1437
    ldr r1,[sp,#0x4]                         @ 08111c96 0199
    lsls r0,r1,#0x2    @ 08111c98 8800
    adds r2,r7,r0    @ 08111c9a 3a18
    str r2,[sp,#0x8]                         @ 08111c9c 0292
    str r0,[sp,#0x18]                        @ 08111c9e 0690
    adds r1,r4,#0x0    @ 08111ca0 211c
    adds r1,#0x14    @ 08111ca2 1431
    lsls r3,r6,#0x2    @ 08111ca4 b300
    adds r2,r5,#0x0    @ 08111ca6 2a1c
    adds r2,#0x14    @ 08111ca8 1432
    .hword 0x4645    @ 08111caa 4546
    lsls r4,r5,#0x2    @ 08111cac ac00
    ldr r0,[sp,#0x8]                         @ 08111cae 0298
    cmp r7,r0                                @ 08111cb0 8742
    bcs LAB_08111cbe                         @ 08111cb2 04d2
    movs r0,#0x0    @ 08111cb4 0020
LAB_08111cb6:
    stmia r7!,{r0}                           @ 08111cb6 01c7
    ldr r5,[sp,#0x8]                         @ 08111cb8 029d
    cmp r7,r5                                @ 08111cba af42
    bcc LAB_08111cb6                         @ 08111cbc fbd3
LAB_08111cbe:
    str r1,[sp,#0x8]                         @ 08111cbe 0291
    adds r3,r1,r3    @ 08111cc0 cb18
    str r3,[sp,#0xc]                         @ 08111cc2 0393
    .hword 0x4690    @ 08111cc4 9046
    add r4,r8                                @ 08111cc6 4444
    str r4,[sp,#0x10]                        @ 08111cc8 0494
    ldr r0,[sp,#0x0]                         @ 08111cca 0098
    adds r0,#0x14    @ 08111ccc 1430
    .hword 0x4681    @ 08111cce 8146
    .hword 0x4649    @ 08111cd0 4946
    str r1,[sp,#0x20]                        @ 08111cd2 0891
    cmp r8,r4                                @ 08111cd4 a045
    bcs LAB_08111d86                         @ 08111cd6 56d2
LAB_08111cd8:
    .hword 0x4642    @ 08111cd8 4246
    ldmia r2!,{r6}                           @ 08111cda 40ca
    str r2,[sp,#0x14]                        @ 08111cdc 0592
    ldr r0, DAT_08111d94                     @ 08111cde 2d48
    ands r6,r0    @ 08111ce0 0640
    .hword 0x464c    @ 08111ce2 4c46
    adds r4,#0x4    @ 08111ce4 0434
    str r4,[sp,#0x1c]                        @ 08111ce6 0794
    cmp r6,#0x0                              @ 08111ce8 002e
    beq LAB_08111d30                         @ 08111cea 21d0
    ldr r7,[sp,#0x8]                         @ 08111cec 029f
    .hword 0x464d    @ 08111cee 4d46
    movs r1,#0x0    @ 08111cf0 0021
    .hword 0x468c    @ 08111cf2 8c46
    .hword 0x4682    @ 08111cf4 8246
LAB_08111cf6:
    ldmia r7!,{r3}                           @ 08111cf6 08cf
    adds r0,r3,#0x0    @ 08111cf8 181c
    .hword 0x4652    @ 08111cfa 5246
    ands r0,r2    @ 08111cfc 1040
    adds r1,r0,#0x0    @ 08111cfe 011c
    muls r1,r6    @ 08111d00 7143
    ldr r2,[r5,#0x0]                         @ 08111d02 2a68
    adds r0,r2,#0x0    @ 08111d04 101c
    .hword 0x4654    @ 08111d06 5446
    ands r0,r4    @ 08111d08 2040
    adds r1,r1,r0    @ 08111d0a 0918
    .hword 0x4660    @ 08111d0c 6046
    adds r4,r1,r0    @ 08111d0e 0c18
    lsrs r1,r4,#0x10    @ 08111d10 210c
    lsrs r3,r3,#0x10    @ 08111d12 1b0c
    adds r0,r3,#0x0    @ 08111d14 181c
    muls r0,r6    @ 08111d16 7043
    lsrs r2,r2,#0x10    @ 08111d18 120c
    adds r0,r0,r2    @ 08111d1a 8018
    adds r2,r0,r1    @ 08111d1c 4218
    lsrs r0,r2,#0x10    @ 08111d1e 100c
    .hword 0x4684    @ 08111d20 8446
    strh r2,[r5,#0x0]                        @ 08111d22 2a80
    strh r4,[r5,#0x2]                        @ 08111d24 6c80
    adds r5,#0x4    @ 08111d26 0435
    ldr r1,[sp,#0xc]                         @ 08111d28 0399
    cmp r7,r1                                @ 08111d2a 8f42
    bcc LAB_08111cf6                         @ 08111d2c e3d3
    str r0,[r5,#0x0]                         @ 08111d2e 2860
LAB_08111d30:
    .hword 0x4642    @ 08111d30 4246
    ldrh r6,[r2,#0x2]                        @ 08111d32 5688
    cmp r6,#0x0                              @ 08111d34 002e
    beq LAB_08111d78                         @ 08111d36 1fd0
    ldr r7,[sp,#0x8]                         @ 08111d38 029f
    .hword 0x464d    @ 08111d3a 4d46
    movs r4,#0x0    @ 08111d3c 0024
    .hword 0x46a4    @ 08111d3e a446
    ldr r2,[r5,#0x0]                         @ 08111d40 2a68
    ldr r3, DAT_08111d94                     @ 08111d42 144b
LAB_08111d44:
    ldmia r7!,{r1}                           @ 08111d44 02cf
    adds r0,r1,#0x0    @ 08111d46 081c
    ands r0,r3    @ 08111d48 1840
    muls r0,r6    @ 08111d4a 7043
    ldrh r4,[r5,#0x2]                        @ 08111d4c 6c88
    adds r4,r4,r0    @ 08111d4e 2418
    .hword 0x46a0    @ 08111d50 a046
    add r4,r12                               @ 08111d52 6444
    lsrs r0,r4,#0x10    @ 08111d54 200c
    .hword 0x4684    @ 08111d56 8446
    strh r4,[r5,#0x0]                        @ 08111d58 2c80
    strh r2,[r5,#0x2]                        @ 08111d5a 6a80
    adds r5,#0x4    @ 08111d5c 0435
    lsrs r1,r1,#0x10    @ 08111d5e 090c
    muls r1,r6    @ 08111d60 7143
    ldr r0,[r5,#0x0]                         @ 08111d62 2868
    ands r0,r3    @ 08111d64 1840
    adds r1,r1,r0    @ 08111d66 0918
    .hword 0x4664    @ 08111d68 6446
    adds r2,r1,r4    @ 08111d6a 0a19
    lsrs r0,r2,#0x10    @ 08111d6c 100c
    .hword 0x4684    @ 08111d6e 8446
    ldr r1,[sp,#0xc]                         @ 08111d70 0399
    cmp r7,r1                                @ 08111d72 8f42
    bcc LAB_08111d44                         @ 08111d74 e6d3
    str r2,[r5,#0x0]                         @ 08111d76 2a60
LAB_08111d78:
    ldr r2,[sp,#0x14]                        @ 08111d78 059a
    .hword 0x4690    @ 08111d7a 9046
    ldr r4,[sp,#0x1c]                        @ 08111d7c 079c
    .hword 0x46a1    @ 08111d7e a146
    ldr r5,[sp,#0x10]                        @ 08111d80 049d
    cmp r8,r5                                @ 08111d82 a845
    bcc LAB_08111cd8                         @ 08111d84 a8d3
LAB_08111d86:
    ldr r0,[sp,#0x20]                        @ 08111d86 0898
    ldr r1,[sp,#0x18]                        @ 08111d88 0699
    adds r5,r0,r1    @ 08111d8a 4518
    ldr r2,[sp,#0x4]                         @ 08111d8c 019a
    cmp r2,#0x0                              @ 08111d8e 002a
    ble LAB_08111daa                         @ 08111d90 0bdd
    b LAB_08111da2                           @ 08111d92 06e0
DAT_08111d94:
    .word  0x0000ffff                     @ 08111d94 ffff0000
LAB_08111d98:
    ldr r4,[sp,#0x4]                         @ 08111d98 019c
    subs r4,#0x1    @ 08111d9a 013c
    str r4,[sp,#0x4]                         @ 08111d9c 0194
    cmp r4,#0x0                              @ 08111d9e 002c
    ble LAB_08111daa                         @ 08111da0 03dd
LAB_08111da2:
    subs r5,#0x4    @ 08111da2 043d
    ldr r0,[r5,#0x0]                         @ 08111da4 2868
    cmp r0,#0x0                              @ 08111da6 0028
    beq LAB_08111d98                         @ 08111da8 f6d0
LAB_08111daa:
    ldr r5,[sp,#0x4]                         @ 08111daa 019d
    ldr r0,[sp,#0x0]                         @ 08111dac 0098
    str r5,[r0,#0x10]                        @ 08111dae 0561
    ldr r0,[sp,#0x0]                         @ 08111db0 0098
    add sp,#0x24                             @ 08111db2 09b0
    pop {r3,r4,r5}                           @ 08111db4 38bc
    .hword 0x4698    @ 08111db6 9846
    .hword 0x46a1    @ 08111db8 a146
    .hword 0x46aa    @ 08111dba aa46
    pop {r4,r5,r6,r7,pc}                     @ 08111dbc f0bd
    .zero  0x2
_pow5mult:
    push {r4,r5,r6,r7,lr}                    @ 08111dc0 f0b5
    .hword 0x4647    @ 08111dc2 4746
    push {r7}                                @ 08111dc4 80b4
    .hword 0x4680    @ 08111dc6 8046
    adds r7,r1,#0x0    @ 08111dc8 0f1c
    adds r6,r2,#0x0    @ 08111dca 161c
    movs r1,#0x3    @ 08111dcc 0321
    ands r1,r6    @ 08111dce 3140
    cmp r1,#0x0                              @ 08111dd0 0029
    beq LAB_08111dea                         @ 08111dd2 0ad0
    ldr r0, DAT_08111e0c                     @ 08111dd4 0d48
    subs r1,#0x1    @ 08111dd6 0139
    lsls r1,r1,#0x2    @ 08111dd8 8900
    adds r1,r1,r0    @ 08111dda 0918
    ldr r2,[r1,#0x0]                         @ 08111ddc 0a68
    .hword 0x4640    @ 08111dde 4046
    adds r1,r7,#0x0    @ 08111de0 391c
    movs r3,#0x0    @ 08111de2 0023
    bl _multadd                              @ 08111de4 fff730fe
    adds r7,r0,#0x0    @ 08111de8 071c
LAB_08111dea:
    asrs r6,r6,#0x2    @ 08111dea b610
    cmp r6,#0x0                              @ 08111dec 002e
    beq LAB_08111e50                         @ 08111dee 2fd0
    .hword 0x4640    @ 08111df0 4046
    ldr r5,[r0,#0x48]                        @ 08111df2 856c
    adds r4,r5,#0x0    @ 08111df4 2c1c
    cmp r5,#0x0                              @ 08111df6 002d
    bne LAB_08111e2c                         @ 08111df8 18d1
    ldr r1, DAT_08111e10                     @ 08111dfa 0549
    bl _i2b                                  @ 08111dfc fff720ff
    .hword 0x4641    @ 08111e00 4146
    str r0,[r1,#0x48]                        @ 08111e02 8864
    adds r5,r0,#0x0    @ 08111e04 051c
    str r4,[r5,#0x0]                         @ 08111e06 2c60
    b LAB_08111e2c                           @ 08111e08 10e0
    .zero  0x2
DAT_08111e0c:
    .word  0x09e58680                     @ 08111e0c 8086e509
DAT_08111e10:
    .word  0x00000271                     @ 08111e10 71020000
LAB_08111e14:
    ldr r0,[r5,#0x0]                         @ 08111e14 2868
    adds r4,r0,#0x0    @ 08111e16 041c
    cmp r0,#0x0                              @ 08111e18 0028
    bne LAB_08111e2a                         @ 08111e1a 06d1
    .hword 0x4640    @ 08111e1c 4046
    adds r1,r5,#0x0    @ 08111e1e 291c
    adds r2,r5,#0x0    @ 08111e20 2a1c
    bl _multiply                             @ 08111e22 fff717ff
    str r0,[r5,#0x0]                         @ 08111e26 2860
    str r4,[r0,#0x0]                         @ 08111e28 0460
LAB_08111e2a:
    adds r5,r0,#0x0    @ 08111e2a 051c
LAB_08111e2c:
    movs r0,#0x1    @ 08111e2c 0120
    ands r0,r6    @ 08111e2e 3040
    cmp r0,#0x0                              @ 08111e30 0028
    beq LAB_08111e4a                         @ 08111e32 0ad0
    .hword 0x4640    @ 08111e34 4046
    adds r1,r7,#0x0    @ 08111e36 391c
    adds r2,r5,#0x0    @ 08111e38 2a1c
    bl _multiply                             @ 08111e3a fff70bff
    adds r4,r0,#0x0    @ 08111e3e 041c
    .hword 0x4640    @ 08111e40 4046
    adds r1,r7,#0x0    @ 08111e42 391c
    bl _Bfree                                @ 08111e44 fff7f4fd
    adds r7,r4,#0x0    @ 08111e48 271c
LAB_08111e4a:
    asrs r6,r6,#0x1    @ 08111e4a 7610
    cmp r6,#0x0                              @ 08111e4c 002e
    bne LAB_08111e14                         @ 08111e4e e1d1
LAB_08111e50:
    adds r0,r7,#0x0    @ 08111e50 381c
    pop {r3}                                 @ 08111e52 08bc
    .hword 0x4698    @ 08111e54 9846
    pop {r4,r5,r6,r7,pc}                     @ 08111e56 f0bd
_lshift:
    push {r4,r5,r6,r7,lr}                    @ 08111e58 f0b5
    .hword 0x4657    @ 08111e5a 5746
    .hword 0x464e    @ 08111e5c 4e46
    .hword 0x4645    @ 08111e5e 4546
    push {r5,r6,r7}                          @ 08111e60 e0b4
    .hword 0x4682    @ 08111e62 8246
    .hword 0x4688    @ 08111e64 8846
    adds r5,r2,#0x0    @ 08111e66 151c
    asrs r6,r5,#0x5    @ 08111e68 6e11
    ldr r1,[r1,#0x4]                         @ 08111e6a 4968
    .hword 0x4642    @ 08111e6c 4246
    ldr r0,[r2,#0x10]                        @ 08111e6e 1069
    adds r0,r6,r0    @ 08111e70 3018
    adds r7,r0,#0x1    @ 08111e72 471c
    ldr r2,[r2,#0x8]                         @ 08111e74 9268
    cmp r7,r2                                @ 08111e76 9742
    ble LAB_08111e82                         @ 08111e78 03dd
LAB_08111e7a:
    adds r1,#0x1    @ 08111e7a 0131
    lsls r2,r2,#0x1    @ 08111e7c 5200
    cmp r7,r2                                @ 08111e7e 9742
    bgt LAB_08111e7a                         @ 08111e80 fbdc
LAB_08111e82:
    .hword 0x4650    @ 08111e82 5046
    bl _Balloc                               @ 08111e84 fff7a8fd
    .hword 0x4681    @ 08111e88 8146
    .hword 0x464c    @ 08111e8a 4c46
    adds r4,#0x14    @ 08111e8c 1434
    .hword 0x4640    @ 08111e8e 4046
    adds r0,#0x14    @ 08111e90 1430
    cmp r6,#0x0                              @ 08111e92 002e
    ble LAB_08111ea2                         @ 08111e94 05dd
    movs r1,#0x0    @ 08111e96 0021
    adds r2,r6,#0x0    @ 08111e98 321c
LAB_08111e9a:
    stmia r4!,{r1}                           @ 08111e9a 02c4
    subs r2,#0x1    @ 08111e9c 013a
    cmp r2,#0x0                              @ 08111e9e 002a
    bne LAB_08111e9a                         @ 08111ea0 fbd1
LAB_08111ea2:
    adds r3,r0,#0x0    @ 08111ea2 031c
    .hword 0x4641    @ 08111ea4 4146
    ldr r0,[r1,#0x10]                        @ 08111ea6 0869
    lsls r0,r0,#0x2    @ 08111ea8 8000
    adds r6,r3,r0    @ 08111eaa 1e18
    movs r0,#0x1f    @ 08111eac 1f20
    ands r5,r0    @ 08111eae 0540
    cmp r5,#0x0                              @ 08111eb0 002d
    beq LAB_08111ed4                         @ 08111eb2 0fd0
    movs r0,#0x20    @ 08111eb4 2020
    subs r1,r0,r5    @ 08111eb6 411b
    movs r2,#0x0    @ 08111eb8 0022
LAB_08111eba:
    ldr r0,[r3,#0x0]                         @ 08111eba 1868
    lsls r0,r5    @ 08111ebc a840
    orrs r0,r2    @ 08111ebe 1043
    stmia r4!,{r0}                           @ 08111ec0 01c4
    ldmia r3!,{r2}                           @ 08111ec2 04cb
    lsrs r2,r1    @ 08111ec4 ca40
    cmp r3,r6                                @ 08111ec6 b342
    bcc LAB_08111eba                         @ 08111ec8 f7d3
    str r2,[r4,#0x0]                         @ 08111eca 2260
    cmp r2,#0x0                              @ 08111ecc 002a
    beq LAB_08111edc                         @ 08111ece 05d0
    adds r7,#0x1    @ 08111ed0 0137
    b LAB_08111edc                           @ 08111ed2 03e0
LAB_08111ed4:
    ldmia r3!,{r0}                           @ 08111ed4 01cb
    stmia r4!,{r0}                           @ 08111ed6 01c4
    cmp r3,r6                                @ 08111ed8 b342
    bcc LAB_08111ed4                         @ 08111eda fbd3
LAB_08111edc:
    subs r0,r7,#0x1    @ 08111edc 781e
    .hword 0x464a    @ 08111ede 4a46
    str r0,[r2,#0x10]                        @ 08111ee0 1061
    .hword 0x4650    @ 08111ee2 5046
    .hword 0x4641    @ 08111ee4 4146
    bl _Bfree                                @ 08111ee6 fff7a3fd
    .hword 0x4648    @ 08111eea 4846
    pop {r3,r4,r5}                           @ 08111eec 38bc
    .hword 0x4698    @ 08111eee 9846
    .hword 0x46a1    @ 08111ef0 a146
    .hword 0x46aa    @ 08111ef2 aa46
    pop {r4,r5,r6,r7,pc}                     @ 08111ef4 f0bd
    .zero  0x2
__mcmp:
    push {r4,r5,lr}                          @ 08111ef8 30b5
    adds r2,r0,#0x0    @ 08111efa 021c
    adds r5,r1,#0x0    @ 08111efc 0d1c
    ldr r0,[r2,#0x10]                        @ 08111efe 1069
    ldr r1,[r5,#0x10]                        @ 08111f00 2969
    subs r0,r0,r1    @ 08111f02 401a
    cmp r0,#0x0                              @ 08111f04 0028
    bne LAB_08111f34                         @ 08111f06 15d1
    adds r4,r2,#0x0    @ 08111f08 141c
    adds r4,#0x14    @ 08111f0a 1434
    lsls r1,r1,#0x2    @ 08111f0c 8900
    adds r3,r4,r1    @ 08111f0e 6318
    adds r0,r5,#0x0    @ 08111f10 281c
    adds r0,#0x14    @ 08111f12 1430
    adds r1,r0,r1    @ 08111f14 4118
LAB_08111f16:
    subs r3,#0x4    @ 08111f16 043b
    subs r1,#0x4    @ 08111f18 0439
    ldr r0,[r3,#0x0]                         @ 08111f1a 1868
    ldr r2,[r1,#0x0]                         @ 08111f1c 0a68
    cmp r0,r2                                @ 08111f1e 9042
    beq LAB_08111f2e                         @ 08111f20 05d0
    movs r1,#0x1    @ 08111f22 0121
    cmp r0,r2                                @ 08111f24 9042
    bcs LAB_08111f2a                         @ 08111f26 00d2
    subs r1,#0x2    @ 08111f28 0239
LAB_08111f2a:
    adds r0,r1,#0x0    @ 08111f2a 081c
    b LAB_08111f34                           @ 08111f2c 02e0
LAB_08111f2e:
    cmp r3,r4                                @ 08111f2e a342
    bhi LAB_08111f16                         @ 08111f30 f1d8
    movs r0,#0x0    @ 08111f32 0020
LAB_08111f34:
    pop {r4,r5,pc}                           @ 08111f34 30bd
    .zero  0x2
__mdiff:
    push {r4,r5,r6,r7,lr}                    @ 08111f38 f0b5
    .hword 0x4657    @ 08111f3a 5746
    .hword 0x464e    @ 08111f3c 4e46
    .hword 0x4645    @ 08111f3e 4546
    push {r5,r6,r7}                          @ 08111f40 e0b4
    sub sp,#0x8                              @ 08111f42 82b0
    adds r6,r0,#0x0    @ 08111f44 061c
    adds r5,r1,#0x0    @ 08111f46 0d1c
    .hword 0x4690    @ 08111f48 9046
    adds r0,r5,#0x0    @ 08111f4a 281c
    .hword 0x4641    @ 08111f4c 4146
    bl __mcmp                                @ 08111f4e fff7d3ff
    adds r4,r0,#0x0    @ 08111f52 041c
    cmp r4,#0x0                              @ 08111f54 002c
    bne LAB_08111f6a                         @ 08111f56 08d1
    adds r0,r6,#0x0    @ 08111f58 301c
    movs r1,#0x0    @ 08111f5a 0021
    bl _Balloc                               @ 08111f5c fff73cfd
    adds r7,r0,#0x0    @ 08111f60 071c
    movs r0,#0x1    @ 08111f62 0120
    str r0,[r7,#0x10]                        @ 08111f64 3861
    str r4,[r7,#0x14]                        @ 08111f66 7c61
    b LAB_0811201a                           @ 08111f68 57e0
LAB_08111f6a:
    cmp r4,#0x0                              @ 08111f6a 002c
    bge LAB_08111f78                         @ 08111f6c 04da
    adds r7,r5,#0x0    @ 08111f6e 2f1c
    .hword 0x4645    @ 08111f70 4546
    .hword 0x46b8    @ 08111f72 b846
    movs r4,#0x1    @ 08111f74 0124
    b LAB_08111f7a                           @ 08111f76 00e0
LAB_08111f78:
    movs r4,#0x0    @ 08111f78 0024
LAB_08111f7a:
    ldr r1,[r5,#0x4]                         @ 08111f7a 6968
    adds r0,r6,#0x0    @ 08111f7c 301c
    bl _Balloc                               @ 08111f7e fff72bfd
    adds r7,r0,#0x0    @ 08111f82 071c
    str r4,[r7,#0xc]                         @ 08111f84 fc60
    ldr r0,[r5,#0x10]                        @ 08111f86 2869
    .hword 0x4681    @ 08111f88 8146
    adds r6,r5,#0x0    @ 08111f8a 2e1c
    adds r6,#0x14    @ 08111f8c 1436
    lsls r0,r0,#0x2    @ 08111f8e 8000
    adds r0,r0,r6    @ 08111f90 8019
    .hword 0x4682    @ 08111f92 8246
    .hword 0x4641    @ 08111f94 4146
    ldr r0,[r1,#0x10]                        @ 08111f96 0869
    movs r3,#0x14    @ 08111f98 1423
    add r3,r8                                @ 08111f9a 4344
    .hword 0x469c    @ 08111f9c 9c46
    lsls r0,r0,#0x2    @ 08111f9e 8000
    add r0,r12                               @ 08111fa0 6044
    str r0,[sp,#0x0]                         @ 08111fa2 0090
    adds r4,r7,#0x0    @ 08111fa4 3c1c
    adds r4,#0x14    @ 08111fa6 1434
    movs r5,#0x0    @ 08111fa8 0025
    ldr r0, DAT_08112004                     @ 08111faa 1648
    .hword 0x4680    @ 08111fac 8046
LAB_08111fae:
    ldmia r6!,{r1}                           @ 08111fae 02ce
    str r1,[sp,#0x4]                         @ 08111fb0 0191
    .hword 0x4643    @ 08111fb2 4346
    ands r1,r3    @ 08111fb4 1940
    .hword 0x4660    @ 08111fb6 6046
    adds r0,#0x4    @ 08111fb8 0430
    .hword 0x4684    @ 08111fba 8446
    subs r0,#0x4    @ 08111fbc 0438
    ldmia r0!,{r2}                           @ 08111fbe 04c8
    adds r0,r2,#0x0    @ 08111fc0 101c
    ands r0,r3    @ 08111fc2 1840
    subs r1,r1,r0    @ 08111fc4 091a
    adds r0,r1,r5    @ 08111fc6 4819
    asrs r5,r0,#0x10    @ 08111fc8 0514
    ldr r1,[sp,#0x4]                         @ 08111fca 0199
    lsrs r3,r1,#0x10    @ 08111fcc 0b0c
    lsrs r2,r2,#0x10    @ 08111fce 120c
    subs r3,r3,r2    @ 08111fd0 9b1a
    adds r1,r3,r5    @ 08111fd2 5919
    asrs r5,r1,#0x10    @ 08111fd4 0d14
    strh r1,[r4,#0x0]                        @ 08111fd6 2180
    strh r0,[r4,#0x2]                        @ 08111fd8 6080
    adds r4,#0x4    @ 08111fda 0434
    ldr r3,[sp,#0x0]                         @ 08111fdc 009b
    cmp r12,r3                               @ 08111fde 9c45
    bcc LAB_08111fae                         @ 08111fe0 e5d3
    cmp r6,r10                               @ 08111fe2 5645
    bcs LAB_0811200e                         @ 08111fe4 13d2
    ldr r2, DAT_08112004                     @ 08111fe6 074a
LAB_08111fe8:
    ldmia r6!,{r1}                           @ 08111fe8 02ce
    adds r0,r1,#0x0    @ 08111fea 081c
    ands r0,r2    @ 08111fec 1040
    adds r0,r0,r5    @ 08111fee 4019
    asrs r5,r0,#0x10    @ 08111ff0 0514
    lsrs r1,r1,#0x10    @ 08111ff2 090c
    adds r1,r1,r5    @ 08111ff4 4919
    asrs r5,r1,#0x10    @ 08111ff6 0d14
    strh r1,[r4,#0x0]                        @ 08111ff8 2180
    strh r0,[r4,#0x2]                        @ 08111ffa 6080
    adds r4,#0x4    @ 08111ffc 0434
    cmp r6,r10                               @ 08111ffe 5645
    bcc LAB_08111fe8                         @ 08112000 f2d3
    b LAB_0811200e                           @ 08112002 04e0
DAT_08112004:
    .word  0x0000ffff                     @ 08112004 ffff0000
LAB_08112008:
    movs r0,#0x1    @ 08112008 0120
    rsbs r0,r0,#0    @ 0811200a 4042
    add r9,r0                                @ 0811200c 8144
LAB_0811200e:
    subs r4,#0x4    @ 0811200e 043c
    ldr r0,[r4,#0x0]                         @ 08112010 2068
    cmp r0,#0x0                              @ 08112012 0028
    beq LAB_08112008                         @ 08112014 f8d0
    .hword 0x4649    @ 08112016 4946
    str r1,[r7,#0x10]                        @ 08112018 3961
LAB_0811201a:
    adds r0,r7,#0x0    @ 0811201a 381c
    add sp,#0x8                              @ 0811201c 02b0
    pop {r3,r4,r5}                           @ 0811201e 38bc
    .hword 0x4698    @ 08112020 9846
    .hword 0x46a1    @ 08112022 a146
    .hword 0x46aa    @ 08112024 aa46
    pop {r4,r5,r6,r7,pc}                     @ 08112026 f0bd
_ulp:
    push {r4,lr}                             @ 08112028 10b5
    ldr r2, DAT_0811203c                     @ 0811202a 044a
    ands r2,r0    @ 0811202c 0240
    ldr r0, DAT_08112040                     @ 0811202e 0448
    adds r2,r2,r0    @ 08112030 1218
    cmp r2,#0x0                              @ 08112032 002a
    ble LAB_08112044                         @ 08112034 06dd
    adds r3,r2,#0x0    @ 08112036 131c
    movs r4,#0x0    @ 08112038 0024
    b LAB_0811206e                           @ 0811203a 18e0
DAT_0811203c:
    .word  0x7ff00000                     @ 0811203c 0000f07f
DAT_08112040:
    .word  0xfcc00000                     @ 08112040 0000c0fc
LAB_08112044:
    rsbs r0,r2,#0    @ 08112044 5042
    asrs r2,r0,#0x14    @ 08112046 0215
    cmp r2,#0x13                             @ 08112048 132a
    bgt LAB_08112058                         @ 0811204a 05dc
    movs r0,#0x80    @ 0811204c 8020
    lsls r0,r0,#0xc    @ 0811204e 0003
    adds r3,r0,#0x0    @ 08112050 031c
    asrs r3,r2    @ 08112052 1341
    movs r4,#0x0    @ 08112054 0024
    b LAB_0811206e                           @ 08112056 0ae0
LAB_08112058:
    movs r3,#0x0    @ 08112058 0023
    subs r2,#0x14    @ 0811205a 143a
    cmp r2,#0x1e                             @ 0811205c 1e2a
    bgt LAB_0811206a                         @ 0811205e 04dc
    movs r0,#0x1f    @ 08112060 1f20
    subs r0,r0,r2    @ 08112062 801a
    movs r1,#0x1    @ 08112064 0121
    lsls r1,r0    @ 08112066 8140
    b LAB_0811206c                           @ 08112068 00e0
LAB_0811206a:
    movs r1,#0x1    @ 0811206a 0121
LAB_0811206c:
    adds r4,r1,#0x0    @ 0811206c 0c1c
LAB_0811206e:
    adds r1,r4,#0x0    @ 0811206e 211c
    adds r0,r3,#0x0    @ 08112070 181c
    pop {r4,pc}                              @ 08112072 10bd
_b2d:
    push {r4,r5,r6,r7,lr}                    @ 08112074 f0b5
    .hword 0x4647    @ 08112076 4746
    push {r7}                                @ 08112078 80b4
    sub sp,#0x4                              @ 0811207a 81b0
    adds r4,r1,#0x0    @ 0811207c 0c1c
    movs r1,#0x14    @ 0811207e 1421
    adds r1,r1,r0    @ 08112080 0918
    .hword 0x4688    @ 08112082 8846
    ldr r0,[r0,#0x10]                        @ 08112084 0069
    lsls r0,r0,#0x2    @ 08112086 8000
    adds r5,r1,r0    @ 08112088 0d18
    subs r5,#0x4    @ 0811208a 043d
    ldr r2,[r5,#0x0]                         @ 0811208c 2a68
    adds r0,r2,#0x0    @ 0811208e 101c
    str r2,[sp,#0x0]                         @ 08112090 0092
    bl _hi0bits                              @ 08112092 fff767fd
    adds r3,r0,#0x0    @ 08112096 031c
    movs r0,#0x20    @ 08112098 2020
    subs r0,r0,r3    @ 0811209a c01a
    str r0,[r4,#0x0]                         @ 0811209c 2060
    ldr r2,[sp,#0x0]                         @ 0811209e 009a
    cmp r3,#0xa                              @ 081120a0 0a2b
    bgt LAB_081120d4                         @ 081120a2 17dc
    movs r0,#0xb    @ 081120a4 0b20
    subs r0,r0,r3    @ 081120a6 c01a
    adds r1,r2,#0x0    @ 081120a8 111c
    lsrs r1,r0    @ 081120aa c140
    ldr r0, DAT_081120bc                     @ 081120ac 0348
    adds r6,r1,#0x0    @ 081120ae 0e1c
    orrs r6,r0    @ 081120b0 0643
    cmp r5,r8                                @ 081120b2 4545
    bls LAB_081120c0                         @ 081120b4 04d9
    subs r5,#0x4    @ 081120b6 043d
    ldr r1,[r5,#0x0]                         @ 081120b8 2968
    b LAB_081120c2                           @ 081120ba 02e0
DAT_081120bc:
    .word  0x3ff00000                     @ 081120bc 0000f03f
LAB_081120c0:
    movs r1,#0x0    @ 081120c0 0021
LAB_081120c2:
    adds r0,r3,#0x0    @ 081120c2 181c
    adds r0,#0x15    @ 081120c4 1530
    lsls r2,r0    @ 081120c6 8240
    movs r0,#0xb    @ 081120c8 0b20
    subs r0,r0,r3    @ 081120ca c01a
    lsrs r1,r0    @ 081120cc c140
    adds r7,r2,#0x0    @ 081120ce 171c
    orrs r7,r1    @ 081120d0 0f43
    b LAB_08112120                           @ 081120d2 25e0
LAB_081120d4:
    cmp r5,r8                                @ 081120d4 4545
    bls LAB_081120de                         @ 081120d6 02d9
    subs r5,#0x4    @ 081120d8 043d
    ldr r4,[r5,#0x0]                         @ 081120da 2c68
    b LAB_081120e0                           @ 081120dc 00e0
LAB_081120de:
    movs r4,#0x0    @ 081120de 0024
LAB_081120e0:
    subs r3,#0xb    @ 081120e0 0b3b
    cmp r3,#0x0                              @ 081120e2 002b
    beq LAB_08112118                         @ 081120e4 18d0
    lsls r2,r3    @ 081120e6 9a40
    movs r0,#0x20    @ 081120e8 2020
    subs r0,r0,r3    @ 081120ea c01a
    adds r1,r4,#0x0    @ 081120ec 211c
    lsrs r1,r0    @ 081120ee c140
    ldr r0, DAT_08112104                     @ 081120f0 0448
    orrs r1,r0    @ 081120f2 0143
    adds r6,r2,#0x0    @ 081120f4 161c
    orrs r6,r1    @ 081120f6 0e43
    cmp r5,r8                                @ 081120f8 4545
    bls LAB_08112108                         @ 081120fa 05d9
    subs r5,#0x4    @ 081120fc 043d
    ldr r2,[r5,#0x0]                         @ 081120fe 2a68
    b LAB_0811210a                           @ 08112100 03e0
    .zero  0x2
DAT_08112104:
    .word  0x3ff00000                     @ 08112104 0000f03f
LAB_08112108:
    movs r2,#0x0    @ 08112108 0022
LAB_0811210a:
    lsls r4,r3    @ 0811210a 9c40
    movs r0,#0x20    @ 0811210c 2020
    subs r0,r0,r3    @ 0811210e c01a
    lsrs r2,r0    @ 08112110 c240
    adds r7,r4,#0x0    @ 08112112 271c
    orrs r7,r2    @ 08112114 1743
    b LAB_08112120                           @ 08112116 03e0
LAB_08112118:
    ldr r0, DAT_0811212c                     @ 08112118 0448
    adds r6,r2,#0x0    @ 0811211a 161c
    orrs r6,r0    @ 0811211c 0643
    adds r7,r4,#0x0    @ 0811211e 271c
LAB_08112120:
    adds r1,r7,#0x0    @ 08112120 391c
    adds r0,r6,#0x0    @ 08112122 301c
    add sp,#0x4                              @ 08112124 01b0
    pop {r3}                                 @ 08112126 08bc
    .hword 0x4698    @ 08112128 9846
    pop {r4,r5,r6,r7,pc}                     @ 0811212a f0bd
DAT_0811212c:
    .word  0x3ff00000                     @ 0811212c 0000f03f
_d2b:
    push {r4,r5,r6,r7,lr}                    @ 08112130 f0b5
    .hword 0x4657    @ 08112132 5746
    .hword 0x464e    @ 08112134 4e46
    .hword 0x4645    @ 08112136 4546
    push {r5,r6,r7}                          @ 08112138 e0b4
    sub sp,#0x8                              @ 0811213a 82b0
    .hword 0x4699    @ 0811213c 9946
    ldr r3,[sp,#0x28]                        @ 0811213e 0a9b
    .hword 0x469a    @ 08112140 9a46
    adds r5,r2,#0x0    @ 08112142 151c
    adds r4,r1,#0x0    @ 08112144 0c1c
    movs r1,#0x1    @ 08112146 0121
    bl _Balloc                               @ 08112148 fff746fc
    adds r6,r0,#0x0    @ 0811214c 061c
    movs r0,#0x14    @ 0811214e 1420
    adds r0,r0,r6    @ 08112150 8019
    .hword 0x4680    @ 08112152 8046
    ldr r2, DAT_08112198                     @ 08112154 104a
    adds r1,r4,#0x0    @ 08112156 211c
    ands r2,r1    @ 08112158 0a40
    str r2,[sp,#0x4]                         @ 0811215a 0192
    ldr r0, DAT_0811219c                     @ 0811215c 0f48
    ands r4,r0    @ 0811215e 0440
    lsrs r7,r4,#0x14    @ 08112160 270d
    cmp r7,#0x0                              @ 08112162 002f
    beq LAB_0811216e                         @ 08112164 03d0
    movs r0,#0x80    @ 08112166 8020
    lsls r0,r0,#0xd    @ 08112168 4003
    orrs r0,r2    @ 0811216a 1043
    str r0,[sp,#0x4]                         @ 0811216c 0190
LAB_0811216e:
    str r5,[sp,#0x0]                         @ 0811216e 0095
    cmp r5,#0x0                              @ 08112170 002d
    beq LAB_081121b8                         @ 08112172 21d0
    .hword 0x4668    @ 08112174 6846
    bl _lo0bits                              @ 08112176 fff721fd
    adds r2,r0,#0x0    @ 0811217a 021c
    cmp r2,#0x0                              @ 0811217c 002a
    beq LAB_081121a0                         @ 0811217e 0fd0
    movs r0,#0x20    @ 08112180 2020
    subs r0,r0,r2    @ 08112182 801a
    ldr r1,[sp,#0x4]                         @ 08112184 0199
    lsls r1,r0    @ 08112186 8140
    ldr r0,[sp,#0x0]                         @ 08112188 0098
    orrs r0,r1    @ 0811218a 0843
    str r0,[r6,#0x14]                        @ 0811218c 7061
    ldr r0,[sp,#0x4]                         @ 0811218e 0198
    lsrs r0,r2    @ 08112190 d040
    str r0,[sp,#0x4]                         @ 08112192 0190
    b LAB_081121a4                           @ 08112194 06e0
    .zero  0x2
DAT_08112198:
    .word  0x000fffff                     @ 08112198 ffff0f00
DAT_0811219c:
    .word  0x7fffffff                     @ 0811219c ffffff7f
LAB_081121a0:
    ldr r0,[sp,#0x0]                         @ 081121a0 0098
    str r0,[r6,#0x14]                        @ 081121a2 7061
LAB_081121a4:
    ldr r0,[sp,#0x4]                         @ 081121a4 0198
    .hword 0x4641    @ 081121a6 4146
    str r0,[r1,#0x4]                         @ 081121a8 4860
    movs r1,#0x1    @ 081121aa 0121
    cmp r0,#0x0                              @ 081121ac 0028
    beq LAB_081121b2                         @ 081121ae 00d0
    movs r1,#0x2    @ 081121b0 0221
LAB_081121b2:
    str r1,[r6,#0x10]                        @ 081121b2 3161
    adds r4,r1,#0x0    @ 081121b4 0c1c
    b LAB_081121cc                           @ 081121b6 09e0
LAB_081121b8:
    add r0,sp,#0x4                           @ 081121b8 01a8
    bl _lo0bits                              @ 081121ba fff7fffc
    adds r2,r0,#0x0    @ 081121be 021c
    ldr r0,[sp,#0x4]                         @ 081121c0 0198
    str r0,[r6,#0x14]                        @ 081121c2 7061
    movs r0,#0x1    @ 081121c4 0120
    str r0,[r6,#0x10]                        @ 081121c6 3061
    movs r4,#0x1    @ 081121c8 0124
    adds r2,#0x20    @ 081121ca 2032
LAB_081121cc:
    cmp r7,#0x0                              @ 081121cc 002f
    beq LAB_081121e8                         @ 081121ce 0bd0
    ldr r3, DAT_081121e4                     @ 081121d0 044b
    adds r0,r2,r3    @ 081121d2 d018
    adds r0,r7,r0    @ 081121d4 3818
    .hword 0x4649    @ 081121d6 4946
    str r0,[r1,#0x0]                         @ 081121d8 0860
    movs r0,#0x35    @ 081121da 3520
    subs r0,r0,r2    @ 081121dc 801a
    .hword 0x4653    @ 081121de 5346
    str r0,[r3,#0x0]                         @ 081121e0 1860
    b LAB_08112204                           @ 081121e2 0fe0
DAT_081121e4:
    .word  0xfffffbcd                     @ 081121e4 cdfbffff
LAB_081121e8:
    ldr r1, DAT_08112214                     @ 081121e8 0a49
    adds r0,r2,r1    @ 081121ea 5018
    .hword 0x464b    @ 081121ec 4b46
    str r0,[r3,#0x0]                         @ 081121ee 1860
    lsls r0,r4,#0x2    @ 081121f0 a000
    add r0,r8                                @ 081121f2 4044
    subs r0,#0x4    @ 081121f4 0438
    ldr r0,[r0,#0x0]                         @ 081121f6 0068
    bl _hi0bits                              @ 081121f8 fff7b4fc
    lsls r1,r4,#0x5    @ 081121fc 6101
    subs r1,r1,r0    @ 081121fe 091a
    .hword 0x4650    @ 08112200 5046
    str r1,[r0,#0x0]                         @ 08112202 0160
LAB_08112204:
    adds r0,r6,#0x0    @ 08112204 301c
    add sp,#0x8                              @ 08112206 02b0
    pop {r3,r4,r5}                           @ 08112208 38bc
    .hword 0x4698    @ 0811220a 9846
    .hword 0x46a1    @ 0811220c a146
    .hword 0x46aa    @ 0811220e aa46
    pop {r4,r5,r6,r7,pc}                     @ 08112210 f0bd
    .zero  0x2
DAT_08112214:
    .word  0xfffffbce                     @ 08112214 cefbffff
_ratio:
    push {r4,r5,r6,r7,lr}                    @ 08112218 f0b5
    sub sp,#0x10                             @ 0811221a 84b0
    adds r4,r0,#0x0    @ 0811221c 041c
    adds r5,r1,#0x0    @ 0811221e 0d1c
    .hword 0x4669    @ 08112220 6946
    bl _b2d                                  @ 08112222 fff727ff
    str r0,[sp,#0x8]                         @ 08112226 0290
    str r1,[sp,#0xc]                         @ 08112228 0391
    add r1,sp,#0x4                           @ 0811222a 01a9
    adds r0,r5,#0x0    @ 0811222c 281c
    bl _b2d                                  @ 0811222e fff721ff
    adds r7,r1,#0x0    @ 08112232 0f1c
    adds r6,r0,#0x0    @ 08112234 061c
    ldr r2,[sp,#0x0]                         @ 08112236 009a
    ldr r0,[sp,#0x4]                         @ 08112238 0198
    subs r2,r2,r0    @ 0811223a 121a
    ldr r0,[r4,#0x10]                        @ 0811223c 2069
    ldr r1,[r5,#0x10]                        @ 0811223e 2969
    subs r0,r0,r1    @ 08112240 401a
    lsls r0,r0,#0x5    @ 08112242 4001
    adds r0,r2,r0    @ 08112244 1018
    cmp r0,#0x0                              @ 08112246 0028
    ble LAB_08112254                         @ 08112248 04dd
    lsls r0,r0,#0x14    @ 0811224a 0005
    ldr r1,[sp,#0x8]                         @ 0811224c 0299
    adds r0,r1,r0    @ 0811224e 0818
    str r0,[sp,#0x8]                         @ 08112250 0290
    b LAB_08112258                           @ 08112252 01e0
LAB_08112254:
    lsls r0,r0,#0x14    @ 08112254 0005
    subs r6,r6,r0    @ 08112256 361a
LAB_08112258:
    ldr r0,[sp,#0x8]                         @ 08112258 0298
    ldr r1,[sp,#0xc]                         @ 0811225a 0399
    adds r3,r7,#0x0    @ 0811225c 3b1c
    adds r2,r6,#0x0    @ 0811225e 321c
    bl __divdf3                              @ 08112260 01f0d0f8
    add sp,#0x10                             @ 08112264 04b0
    pop {r4,r5,r6,r7,pc}                     @ 08112266 f0bd
_mprec_log10:
    push {r4,lr}                             @ 08112268 10b5
    adds r4,r0,#0x0    @ 0811226a 041c
    ldr r1, DAT_08112284                     @ 0811226c 0549
    ldr r0, DAT_08112280                     @ 0811226e 0448
    cmp r4,#0x17                             @ 08112270 172c
    bgt LAB_0811228c                         @ 08112272 0bdc
    ldr r0, DAT_08112288                     @ 08112274 0448
    lsls r1,r4,#0x3    @ 08112276 e100
    adds r1,r1,r0    @ 08112278 0918
    ldr r0,[r1,#0x0]                         @ 0811227a 0868
    ldr r1,[r1,#0x4]                         @ 0811227c 4968
    b LAB_0811229e                           @ 0811227e 0ee0
DAT_08112280:
    .word  0x3ff00000                     @ 08112280 0000f03f
DAT_08112284:
    .word  0x00000000                     @ 08112284 00000000
DAT_08112288:
    .word  0x09e5868c                     @ 08112288 8c86e509
LAB_0811228c:
    cmp r4,#0x0                              @ 0811228c 002c
    ble LAB_0811229e                         @ 0811228e 06dd
LAB_08112290:
    ldr r3, DAT_081122a4                     @ 08112290 044b
    ldr r2, DAT_081122a0                     @ 08112292 034a
    bl __muldf3                              @ 08112294 00f062ff
    subs r4,#0x1    @ 08112298 013c
    cmp r4,#0x0                              @ 0811229a 002c
    bgt LAB_08112290                         @ 0811229c f8dc
LAB_0811229e:
    pop {r4,pc}                              @ 0811229e 10bd
DAT_081122a0:
    .word  0x40240000                     @ 081122a0 00002440
DAT_081122a4:
    .word  0x00000000                     @ 081122a4 00000000
_realloc_r:
    push {r4,r5,r6,r7,lr}                    @ 081122a8 f0b5
    .hword 0x4657    @ 081122aa 5746
    .hword 0x464e    @ 081122ac 4e46
    .hword 0x4645    @ 081122ae 4546
    push {r5,r6,r7}                          @ 081122b0 e0b4
    sub sp,#0x8                              @ 081122b2 82b0
    str r0,[sp,#0x0]                         @ 081122b4 0090
    adds r5,r1,#0x0    @ 081122b6 0d1c
    str r2,[sp,#0x4]                         @ 081122b8 0192
    cmp r5,#0x0                              @ 081122ba 002d
    bne LAB_081122c6                         @ 081122bc 03d1
    adds r1,r2,#0x0    @ 081122be 111c
    bl _malloc_r                             @ 081122c0 fff7a6f9
    b LAB_08112592                           @ 081122c4 65e1
LAB_081122c6:
    ldr r0,[sp,#0x0]                         @ 081122c6 0098
    bl stub_malloc_lock                      @ 081122c8 fff782fb
    adds r4,r5,#0x0    @ 081122cc 2c1c
    subs r4,#0x8    @ 081122ce 083c
    adds r7,r4,#0x0    @ 081122d0 271c
    ldr r0,[r4,#0x4]                         @ 081122d2 6068
    .hword 0x4681    @ 081122d4 8146
    movs r0,#0x4    @ 081122d6 0420
    rsbs r0,r0,#0    @ 081122d8 4042
    .hword 0x4649    @ 081122da 4946
    ands r1,r0    @ 081122dc 0140
    .hword 0x4689    @ 081122de 8946
    .hword 0x46c8    @ 081122e0 c846
    ldr r0,[sp,#0x4]                         @ 081122e2 0198
    adds r0,#0xb    @ 081122e4 0b30
    cmp r0,#0x16                             @ 081122e6 1628
    ble LAB_081122f8                         @ 081122e8 06dd
    movs r3,#0x8    @ 081122ea 0823
    rsbs r3,r3,#0    @ 081122ec 5b42
    .hword 0x469a    @ 081122ee 9a46
    .hword 0x4651    @ 081122f0 5146
    ands r1,r0    @ 081122f2 0140
    .hword 0x468a    @ 081122f4 8a46
    b LAB_081122fc                           @ 081122f6 01e0
LAB_081122f8:
    movs r3,#0x10    @ 081122f8 1023
    .hword 0x469a    @ 081122fa 9a46
LAB_081122fc:
    cmp r8,r10                               @ 081122fc d045
    blt LAB_08112302                         @ 081122fe 00db
    b LAB_08112544                           @ 08112300 20e1
LAB_08112302:
    .hword 0x4640    @ 08112302 4046
    adds r6,r7,r0    @ 08112304 3e18
    ldr r0, DAT_08112360                     @ 08112306 1648
    ldr r2,[r0,#0x8]                         @ 08112308 8268
    .hword 0x4684    @ 0811230a 8446
    cmp r6,r2                                @ 0811230c 9642
    beq LAB_08112324                         @ 0811230e 09d0
    ldr r0,[r6,#0x4]                         @ 08112310 7068
    movs r1,#0x2    @ 08112312 0221
    rsbs r1,r1,#0    @ 08112314 4942
    ands r0,r1    @ 08112316 0840
    adds r0,r6,r0    @ 08112318 3018
    ldr r0,[r0,#0x4]                         @ 0811231a 4068
    movs r1,#0x1    @ 0811231c 0121
    ands r0,r1    @ 0811231e 0840
    cmp r0,#0x0                              @ 08112320 0028
    bne LAB_08112378                         @ 08112322 29d1
LAB_08112324:
    ldr r3,[r6,#0x4]                         @ 08112324 7368
    movs r0,#0x4    @ 08112326 0420
    rsbs r0,r0,#0    @ 08112328 4042
    ands r3,r0    @ 0811232a 0340
    cmp r6,r2                                @ 0811232c 9642
    bne LAB_08112364                         @ 0811232e 19d1
    .hword 0x464c    @ 08112330 4c46
    adds r1,r3,r4    @ 08112332 1919
    .hword 0x4650    @ 08112334 5046
    adds r0,#0x10    @ 08112336 1030
    cmp r1,r0                                @ 08112338 8142
    blt LAB_0811237c                         @ 0811233a 1fdb
    .hword 0x4655    @ 0811233c 5546
    adds r2,r7,r5    @ 0811233e 7a19
    .hword 0x4660    @ 08112340 6046
    str r2,[r0,#0x8]                         @ 08112342 8260
    subs r0,r1,r5    @ 08112344 481b
    movs r1,#0x1    @ 08112346 0121
    orrs r0,r1    @ 08112348 0843
    str r0,[r2,#0x4]                         @ 0811234a 5060
    ldr r0,[r7,#0x4]                         @ 0811234c 7868
    ands r0,r1    @ 0811234e 0840
    orrs r0,r5    @ 08112350 2843
    str r0,[r7,#0x4]                         @ 08112352 7860
    ldr r0,[sp,#0x0]                         @ 08112354 0098
    bl stub_malloc_unlock                    @ 08112356 fff73dfb
    adds r0,r7,#0x0    @ 0811235a 381c
    b LAB_08112590                           @ 0811235c 18e1
    .zero  0x2
DAT_08112360:
    .word  0x09ed4d98                     @ 08112360 984ded09
LAB_08112364:
    .hword 0x4649    @ 08112364 4946
    adds r2,r3,r1    @ 08112366 5a18
    cmp r2,r10                               @ 08112368 5245
    blt LAB_0811237c                         @ 0811236a 07db
    ldr r1,[r6,#0xc]                         @ 0811236c f168
    ldr r0,[r6,#0x8]                         @ 0811236e b068
    str r1,[r0,#0xc]                         @ 08112370 c160
    str r0,[r1,#0x8]                         @ 08112372 8860
    .hword 0x4691    @ 08112374 9146
    b LAB_08112544                           @ 08112376 e5e0
LAB_08112378:
    movs r6,#0x0    @ 08112378 0026
    movs r3,#0x0    @ 0811237a 0023
LAB_0811237c:
    ldr r0,[r7,#0x4]                         @ 0811237c 7868
    movs r1,#0x1    @ 0811237e 0121
    ands r0,r1    @ 08112380 0840
    cmp r0,#0x0                              @ 08112382 0028
    beq LAB_08112388                         @ 08112384 00d0
    b LAB_081124b2                           @ 08112386 94e0
LAB_08112388:
    ldr r0,[r7,#0x0]                         @ 08112388 3868
    subs r2,r7,r0    @ 0811238a 3a1a
    ldr r1,[r2,#0x4]                         @ 0811238c 5168
    movs r0,#0x4    @ 0811238e 0420
    rsbs r0,r0,#0    @ 08112390 4042
    ands r1,r0    @ 08112392 0140
    cmp r6,#0x0                              @ 08112394 002e
    beq LAB_08112444                         @ 08112396 55d0
    .hword 0x4664    @ 08112398 6446
    ldr r0,[r4,#0x8]                         @ 0811239a a068
    cmp r6,r0                                @ 0811239c 8642
    bne LAB_08112430                         @ 0811239e 47d1
    adds r0,r3,r1    @ 081123a0 5818
    .hword 0x464c    @ 081123a2 4c46
    adds r3,r0,r4    @ 081123a4 0319
    .hword 0x4650    @ 081123a6 5046
    adds r0,#0x10    @ 081123a8 1030
    cmp r3,r0                                @ 081123aa 8342
    blt LAB_08112444                         @ 081123ac 4adb
    ldr r1,[r2,#0xc]                         @ 081123ae d168
    ldr r0,[r2,#0x8]                         @ 081123b0 9068
    str r1,[r0,#0xc]                         @ 081123b2 c160
    str r0,[r1,#0x8]                         @ 081123b4 8860
    adds r4,r2,#0x0    @ 081123b6 141c
    .hword 0x4699    @ 081123b8 9946
    adds r6,r4,#0x0    @ 081123ba 261c
    adds r6,#0x8    @ 081123bc 0836
    .hword 0x4642    @ 081123be 4246
    subs r2,#0x4    @ 081123c0 043a
    cmp r2,#0x24                             @ 081123c2 242a
    bhi LAB_08112406                         @ 081123c4 1fd8
    adds r1,r5,#0x0    @ 081123c6 291c
    adds r3,r6,#0x0    @ 081123c8 331c
    cmp r2,#0x13                             @ 081123ca 132a
    bls LAB_081123f8                         @ 081123cc 14d9
    ldmia r1!,{r0}                           @ 081123ce 01c9
    str r0,[r4,#0x8]                         @ 081123d0 a060
    ldr r0,[r5,#0x4]                         @ 081123d2 6868
    str r0,[r4,#0xc]                         @ 081123d4 e060
    adds r1,#0x4    @ 081123d6 0431
    adds r3,r4,#0x0    @ 081123d8 231c
    adds r3,#0x10    @ 081123da 1033
    cmp r2,#0x1b                             @ 081123dc 1b2a
    bls LAB_081123f8                         @ 081123de 0bd9
    ldmia r1!,{r0}                           @ 081123e0 01c9
    str r0,[r4,#0x10]                        @ 081123e2 2061
    ldmia r1!,{r0}                           @ 081123e4 01c9
    str r0,[r4,#0x14]                        @ 081123e6 6061
    adds r3,#0x8    @ 081123e8 0833
    cmp r2,#0x23                             @ 081123ea 232a
    bls LAB_081123f8                         @ 081123ec 04d9
    ldmia r1!,{r0}                           @ 081123ee 01c9
    str r0,[r4,#0x18]                        @ 081123f0 a061
    ldmia r1!,{r0}                           @ 081123f2 01c9
    str r0,[r4,#0x1c]                        @ 081123f4 e061
    adds r3,#0x8    @ 081123f6 0833
LAB_081123f8:
    ldmia r1!,{r0}                           @ 081123f8 01c9
    stmia r3!,{r0}                           @ 081123fa 01c3
    ldmia r1!,{r0}                           @ 081123fc 01c9
    stmia r3!,{r0}                           @ 081123fe 01c3
    ldr r0,[r1,#0x0]                         @ 08112400 0868
    str r0,[r3,#0x0]                         @ 08112402 1860
    b LAB_0811240e                           @ 08112404 03e0
LAB_08112406:
    adds r0,r6,#0x0    @ 08112406 301c
    adds r1,r5,#0x0    @ 08112408 291c
    bl memcpy                                @ 0811240a fcf7a7fa
LAB_0811240e:
    ldr r0, DAT_0811242c                     @ 0811240e 0748
    .hword 0x4655    @ 08112410 5546
    adds r2,r4,r5    @ 08112412 6219
    str r2,[r0,#0x8]                         @ 08112414 8260
    .hword 0x4649    @ 08112416 4946
    subs r0,r1,r5    @ 08112418 481b
    movs r1,#0x1    @ 0811241a 0121
    orrs r0,r1    @ 0811241c 0843
    str r0,[r2,#0x4]                         @ 0811241e 5060
    ldr r0,[r4,#0x4]                         @ 08112420 6068
    ands r0,r1    @ 08112422 0840
    orrs r0,r5    @ 08112424 2843
    str r0,[r4,#0x4]                         @ 08112426 6060
    b LAB_0811253a                           @ 08112428 87e0
    .zero  0x2
DAT_0811242c:
    .word  0x09ed4d98                     @ 0811242c 984ded09
LAB_08112430:
    adds r0,r3,r1    @ 08112430 5818
    .hword 0x464c    @ 08112432 4c46
    adds r3,r0,r4    @ 08112434 0319
    cmp r3,r10                               @ 08112436 5345
    blt LAB_08112444                         @ 08112438 04db
    ldr r1,[r6,#0xc]                         @ 0811243a f168
    ldr r0,[r6,#0x8]                         @ 0811243c b068
    str r1,[r0,#0xc]                         @ 0811243e c160
    str r0,[r1,#0x8]                         @ 08112440 8860
    b LAB_08112450                           @ 08112442 05e0
LAB_08112444:
    cmp r2,#0x0                              @ 08112444 002a
    beq LAB_081124b2                         @ 08112446 34d0
    .hword 0x4648    @ 08112448 4846
    adds r3,r1,r0    @ 0811244a 0b18
    cmp r3,r10                               @ 0811244c 5345
    blt LAB_081124b2                         @ 0811244e 30db
LAB_08112450:
    ldr r1,[r2,#0xc]                         @ 08112450 d168
    ldr r0,[r2,#0x8]                         @ 08112452 9068
    str r1,[r0,#0xc]                         @ 08112454 c160
    str r0,[r1,#0x8]                         @ 08112456 8860
    adds r4,r2,#0x0    @ 08112458 141c
    .hword 0x4699    @ 0811245a 9946
    adds r6,r4,#0x0    @ 0811245c 261c
    adds r6,#0x8    @ 0811245e 0836
    .hword 0x4642    @ 08112460 4246
    subs r2,#0x4    @ 08112462 043a
    cmp r2,#0x24                             @ 08112464 242a
    bhi LAB_081124a8                         @ 08112466 1fd8
    adds r1,r5,#0x0    @ 08112468 291c
    adds r3,r6,#0x0    @ 0811246a 331c
    cmp r2,#0x13                             @ 0811246c 132a
    bls LAB_0811249a                         @ 0811246e 14d9
    ldmia r1!,{r0}                           @ 08112470 01c9
    str r0,[r4,#0x8]                         @ 08112472 a060
    ldr r0,[r5,#0x4]                         @ 08112474 6868
    str r0,[r4,#0xc]                         @ 08112476 e060
    adds r1,#0x4    @ 08112478 0431
    adds r3,r4,#0x0    @ 0811247a 231c
    adds r3,#0x10    @ 0811247c 1033
    cmp r2,#0x1b                             @ 0811247e 1b2a
    bls LAB_0811249a                         @ 08112480 0bd9
    ldmia r1!,{r0}                           @ 08112482 01c9
    str r0,[r4,#0x10]                        @ 08112484 2061
    ldmia r1!,{r0}                           @ 08112486 01c9
    str r0,[r4,#0x14]                        @ 08112488 6061
    adds r3,#0x8    @ 0811248a 0833
    cmp r2,#0x23                             @ 0811248c 232a
    bls LAB_0811249a                         @ 0811248e 04d9
    ldmia r1!,{r0}                           @ 08112490 01c9
    str r0,[r4,#0x18]                        @ 08112492 a061
    ldmia r1!,{r0}                           @ 08112494 01c9
    str r0,[r4,#0x1c]                        @ 08112496 e061
    adds r3,#0x8    @ 08112498 0833
LAB_0811249a:
    ldmia r1!,{r0}                           @ 0811249a 01c9
    stmia r3!,{r0}                           @ 0811249c 01c3
    ldmia r1!,{r0}                           @ 0811249e 01c9
    stmia r3!,{r0}                           @ 081124a0 01c3
    ldr r0,[r1,#0x0]                         @ 081124a2 0868
    str r0,[r3,#0x0]                         @ 081124a4 1860
    b LAB_08112544                           @ 081124a6 4de0
LAB_081124a8:
    adds r0,r6,#0x0    @ 081124a8 301c
    adds r1,r5,#0x0    @ 081124aa 291c
    bl memcpy                                @ 081124ac fcf756fa
    b LAB_08112544                           @ 081124b0 48e0
LAB_081124b2:
    ldr r0,[sp,#0x0]                         @ 081124b2 0098
    ldr r1,[sp,#0x4]                         @ 081124b4 0199
    bl _malloc_r                             @ 081124b6 fff7abf8
    adds r6,r0,#0x0    @ 081124ba 061c
    cmp r6,#0x0                              @ 081124bc 002e
    bne LAB_081124ca                         @ 081124be 04d1
    ldr r0,[sp,#0x0]                         @ 081124c0 0098
    bl stub_malloc_unlock                    @ 081124c2 fff787fa
    movs r0,#0x0    @ 081124c6 0020
    b LAB_08112592                           @ 081124c8 63e0
LAB_081124ca:
    adds r4,r6,#0x0    @ 081124ca 341c
    subs r4,#0x8    @ 081124cc 083c
    ldr r0,[r7,#0x4]                         @ 081124ce 7868
    movs r1,#0x2    @ 081124d0 0221
    rsbs r1,r1,#0    @ 081124d2 4942
    ands r0,r1    @ 081124d4 0840
    adds r0,r7,r0    @ 081124d6 3818
    cmp r4,r0                                @ 081124d8 8442
    bne LAB_081124e8                         @ 081124da 05d1
    ldr r0,[r4,#0x4]                         @ 081124dc 6068
    subs r1,#0x2    @ 081124de 0239
    ands r0,r1    @ 081124e0 0840
    add r9,r0                                @ 081124e2 8144
    adds r4,r7,#0x0    @ 081124e4 3c1c
    b LAB_08112544                           @ 081124e6 2de0
LAB_081124e8:
    .hword 0x4642    @ 081124e8 4246
    subs r2,#0x4    @ 081124ea 043a
    cmp r2,#0x24                             @ 081124ec 242a
    bhi LAB_0811252a                         @ 081124ee 1cd8
    adds r1,r5,#0x0    @ 081124f0 291c
    adds r3,r6,#0x0    @ 081124f2 331c
    cmp r2,#0x13                             @ 081124f4 132a
    bls LAB_0811251c                         @ 081124f6 11d9
    ldmia r1!,{r0}                           @ 081124f8 01c9
    stmia r3!,{r0}                           @ 081124fa 01c3
    ldr r0,[r5,#0x4]                         @ 081124fc 6868
    str r0,[r6,#0x4]                         @ 081124fe 7060
    adds r1,#0x4    @ 08112500 0431
    adds r3,#0x4    @ 08112502 0433
    cmp r2,#0x1b                             @ 08112504 1b2a
    bls LAB_0811251c                         @ 08112506 09d9
    ldmia r1!,{r0}                           @ 08112508 01c9
    stmia r3!,{r0}                           @ 0811250a 01c3
    ldmia r1!,{r0}                           @ 0811250c 01c9
    stmia r3!,{r0}                           @ 0811250e 01c3
    cmp r2,#0x23                             @ 08112510 232a
    bls LAB_0811251c                         @ 08112512 03d9
    ldmia r1!,{r0}                           @ 08112514 01c9
    stmia r3!,{r0}                           @ 08112516 01c3
    ldmia r1!,{r0}                           @ 08112518 01c9
    stmia r3!,{r0}                           @ 0811251a 01c3
LAB_0811251c:
    ldmia r1!,{r0}                           @ 0811251c 01c9
    stmia r3!,{r0}                           @ 0811251e 01c3
    ldmia r1!,{r0}                           @ 08112520 01c9
    stmia r3!,{r0}                           @ 08112522 01c3
    ldr r0,[r1,#0x0]                         @ 08112524 0868
    str r0,[r3,#0x0]                         @ 08112526 1860
    b LAB_08112532                           @ 08112528 03e0
LAB_0811252a:
    adds r0,r6,#0x0    @ 0811252a 301c
    adds r1,r5,#0x0    @ 0811252c 291c
    bl memcpy                                @ 0811252e fcf715fa
LAB_08112532:
    ldr r0,[sp,#0x0]                         @ 08112532 0098
    adds r1,r5,#0x0    @ 08112534 291c
    bl _free_r                               @ 08112536 fef7effd
LAB_0811253a:
    ldr r0,[sp,#0x0]                         @ 0811253a 0098
    bl stub_malloc_unlock                    @ 0811253c fff74afa
    adds r0,r6,#0x0    @ 08112540 301c
    b LAB_08112592                           @ 08112542 26e0
LAB_08112544:
    .hword 0x4649    @ 08112544 4946
    .hword 0x4653    @ 08112546 5346
    subs r2,r1,r3    @ 08112548 ca1a
    cmp r2,#0xf                              @ 0811254a 0f2a
    bls LAB_08112574                         @ 0811254c 12d9
    adds r1,r4,r3    @ 0811254e e118
    ldr r0,[r4,#0x4]                         @ 08112550 6068
    movs r3,#0x1    @ 08112552 0123
    ands r0,r3    @ 08112554 1840
    .hword 0x4655    @ 08112556 5546
    orrs r0,r5    @ 08112558 2843
    str r0,[r4,#0x4]                         @ 0811255a 6060
    adds r0,r2,#0x0    @ 0811255c 101c
    orrs r0,r3    @ 0811255e 1843
    str r0,[r1,#0x4]                         @ 08112560 4860
    adds r2,r1,r2    @ 08112562 8a18
    ldr r0,[r2,#0x4]                         @ 08112564 5068
    orrs r0,r3    @ 08112566 1843
    str r0,[r2,#0x4]                         @ 08112568 5060
    adds r1,#0x8    @ 0811256a 0831
    ldr r0,[sp,#0x0]                         @ 0811256c 0098
    bl _free_r                               @ 0811256e fef7d3fd
    b LAB_08112588                           @ 08112572 09e0
LAB_08112574:
    ldr r0,[r4,#0x4]                         @ 08112574 6068
    movs r2,#0x1    @ 08112576 0122
    ands r0,r2    @ 08112578 1040
    .hword 0x4649    @ 0811257a 4946
    orrs r0,r1    @ 0811257c 0843
    str r0,[r4,#0x4]                         @ 0811257e 6060
    adds r1,r4,r1    @ 08112580 6118
    ldr r0,[r1,#0x4]                         @ 08112582 4868
    orrs r0,r2    @ 08112584 1043
    str r0,[r1,#0x4]                         @ 08112586 4860
LAB_08112588:
    ldr r0,[sp,#0x0]                         @ 08112588 0098
    bl stub_malloc_unlock                    @ 0811258a fff723fa
    adds r0,r4,#0x0    @ 0811258e 201c
LAB_08112590:
    adds r0,#0x8    @ 08112590 0830
LAB_08112592:
    add sp,#0x8                              @ 08112592 02b0
    pop {r3,r4,r5}                           @ 08112594 38bc
    .hword 0x4698    @ 08112596 9846
    .hword 0x46a1    @ 08112598 a146
    .hword 0x46aa    @ 0811259a aa46
    pop {r4,r5,r6,r7,pc}                     @ 0811259c f0bd
    .zero  0x2

@ newlib _sbrk_r reentrant wrapper: clears global errno cache (EWRAM 0x02029ea8), then calls _sbrk(nbytes) to expand heap.
@ If _sbrk returns -1 (failure) and errno is nonzero, writes errno back to caller-provided error-code pointer.
@ Called by dlmalloc internals (0x081112d8 _malloc_trim_r / 0x081114b4 / 0x081113d8 __smakebuf) to request more memory from OS.
@ 
@ Constants:
@ - ERRNO_CACHE=0x02029ea8 (newlib global errno staging address, EWRAM)
@ - SBRK_FAIL=-1 (0xFFFFFFFF, _sbrk failure return value)
wrap_sbrk_r:
    push {r4,r5,lr}                          @ 081125a0 30b5
    adds r5,r0,#0x0    @ 081125a2 051c
    adds r0,r1,#0x0    @ 081125a4 081c
    ldr r4, DAT_081125c8                     @ 081125a6 084c
    movs r1,#0x0    @ 081125a8 0021
    str r1,[r4,#0x0]                         @ 081125aa 2160
    bl _sbrk                                 @ 081125ac 00f050fa
    adds r1,r0,#0x0    @ 081125b0 011c
    movs r0,#0x1    @ 081125b2 0120
    rsbs r0,r0,#0    @ 081125b4 4042
    cmp r1,r0                                @ 081125b6 8142
    bne LAB_081125c2                         @ 081125b8 03d1
    ldr r0,[r4,#0x0]                         @ 081125ba 2068
    cmp r0,#0x0                              @ 081125bc 0028
    beq LAB_081125c2                         @ 081125be 00d0
    str r0,[r5,#0x0]                         @ 081125c0 2860
LAB_081125c2:
    adds r0,r1,#0x0    @ 081125c2 081c
    pop {r4,r5,pc}                           @ 081125c4 30bd
    .zero  0x2
DAT_081125c8:
    .word  0x02029ea8                     @ 081125c8 a89e0202
__sread:
    push {r4,r5,lr}                          @ 081125cc 30b5
    adds r5,r0,#0x0    @ 081125ce 051c
    adds r4,r1,#0x0    @ 081125d0 0c1c
    adds r3,r2,#0x0    @ 081125d2 131c
    ldr r0,[r5,#0x54]                        @ 081125d4 686d
    movs r2,#0xe    @ 081125d6 0e22
    ldrsh r1,[r5,r2]                         @ 081125d8 a95e
    adds r2,r4,#0x0    @ 081125da 221c
    bl wrap_read_r                           @ 081125dc 00f02cfb
    adds r1,r0,#0x0    @ 081125e0 011c
    cmp r1,#0x0                              @ 081125e2 0029
    blt LAB_081125ee                         @ 081125e4 03db
    ldr r0,[r5,#0x50]                        @ 081125e6 286d
    adds r0,r0,r1    @ 081125e8 4018
    str r0,[r5,#0x50]                        @ 081125ea 2865
    b LAB_081125f6                           @ 081125ec 03e0
LAB_081125ee:
    ldr r0, DAT_081125fc                     @ 081125ee 0348
    ldrh r2,[r5,#0xc]                        @ 081125f0 aa89
    ands r0,r2    @ 081125f2 1040
    strh r0,[r5,#0xc]                        @ 081125f4 a881
LAB_081125f6:
    adds r0,r1,#0x0    @ 081125f6 081c
    pop {r4,r5,pc}                           @ 081125f8 30bd
    .zero  0x2
DAT_081125fc:
    .word  0xffffefff                     @ 081125fc ffefffff
__swrite:
    push {r4,r5,r6,lr}                       @ 08112600 70b5
    adds r4,r0,#0x0    @ 08112602 041c
    adds r5,r1,#0x0    @ 08112604 0d1c
    adds r6,r2,#0x0    @ 08112606 161c
    movs r0,#0x80    @ 08112608 8020
    lsls r0,r0,#0x1    @ 0811260a 4000
    ldrh r1,[r4,#0xc]                        @ 0811260c a189
    ands r0,r1    @ 0811260e 0840
    cmp r0,#0x0                              @ 08112610 0028
    beq LAB_08112622                         @ 08112612 06d0
    ldr r0,[r4,#0x54]                        @ 08112614 606d
    movs r2,#0xe    @ 08112616 0e22
    ldrsh r1,[r4,r2]                         @ 08112618 a15e
    movs r2,#0x0    @ 0811261a 0022
    movs r3,#0x2    @ 0811261c 0223
    bl lseek_fd_reentrant                    @ 0811261e 00f0f3fa
LAB_08112622:
    ldr r0, DAT_0811263c                     @ 08112622 0648
    ldrh r1,[r4,#0xc]                        @ 08112624 a189
    ands r0,r1    @ 08112626 0840
    strh r0,[r4,#0xc]                        @ 08112628 a081
    ldr r0,[r4,#0x54]                        @ 0811262a 606d
    movs r2,#0xe    @ 0811262c 0e22
    ldrsh r1,[r4,r2]                         @ 0811262e a15e
    adds r2,r5,#0x0    @ 08112630 2a1c
    adds r3,r6,#0x0    @ 08112632 331c
    bl wrap_write_r                          @ 08112634 00f05efa
    pop {r4,r5,r6,pc}                        @ 08112638 70bd
    .zero  0x2
DAT_0811263c:
    .word  0xffffefff                     @ 0811263c ffefffff
__sseek:
    push {r4,r5,lr}                          @ 08112640 30b5
    adds r5,r0,#0x0    @ 08112642 051c
    adds r4,r1,#0x0    @ 08112644 0c1c
    adds r3,r2,#0x0    @ 08112646 131c
    ldr r0,[r5,#0x54]                        @ 08112648 686d
    movs r2,#0xe    @ 0811264a 0e22
    ldrsh r1,[r5,r2]                         @ 0811264c a95e
    adds r2,r4,#0x0    @ 0811264e 221c
    bl lseek_fd_reentrant                    @ 08112650 00f0dafa
    adds r1,r0,#0x0    @ 08112654 011c
    movs r0,#0x1    @ 08112656 0120
    rsbs r0,r0,#0    @ 08112658 4042
    cmp r1,r0                                @ 0811265a 8142
    bne LAB_0811266c                         @ 0811265c 06d1
    ldr r0, DAT_08112668                     @ 0811265e 0248
    ldrh r2,[r5,#0xc]                        @ 08112660 aa89
    ands r0,r2    @ 08112662 1040
    strh r0,[r5,#0xc]                        @ 08112664 a881
    b LAB_0811267a                           @ 08112666 08e0
DAT_08112668:
    .word  0xffffefff                     @ 08112668 ffefffff
LAB_0811266c:
    movs r2,#0x80    @ 0811266c 8022
    lsls r2,r2,#0x5    @ 0811266e 5201
    adds r0,r2,#0x0    @ 08112670 101c
    ldrh r2,[r5,#0xc]                        @ 08112672 aa89
    orrs r0,r2    @ 08112674 1043
    strh r0,[r5,#0xc]                        @ 08112676 a881
    str r1,[r5,#0x50]                        @ 08112678 2965
LAB_0811267a:
    adds r0,r1,#0x0    @ 0811267a 081c
    pop {r4,r5,pc}                           @ 0811267c 30bd
    .zero  0x2
__sclose:
    push {lr}                                @ 08112680 00b5
    ldr r2,[r0,#0x54]                        @ 08112682 426d
    movs r3,#0xe    @ 08112684 0e23
    ldrsh r1,[r0,r3]                         @ 08112686 c15e
    adds r0,r2,#0x0    @ 08112688 101c
    bl close_fd_reentrant                    @ 0811268a 00f077fa
    pop {pc}                                 @ 0811268e 00bd

@ Linear search in semihosting file handle table (IWRAM 0x03005788, 20 entries, 8 bytes each) for entry matching specified fd.
@ Iterates index 0..19; returns matching index [0..19] if found, or 20 if not found.
@ Called by _read / _write / _lseek / _close and similar semihosting I/O functions to map file descriptor to IWRAM handle slot.
@ 
@ Constants:
@ - HANDLE_TABLE=0x03005788 (semihosting handle table base, IWRAM)
@ - MAX_HANDLES=20 (maximum handle count, 0x13+1)
@ - ENTRY_STRIDE=8 (bytes per entry)
find_semihost_handle_slot:
    adds r3,r0,#0x0    @ 08112690 031c
    movs r1,#0x0    @ 08112692 0021
    ldr r2, DAT_08112698                     @ 08112694 004a
    b LAB_081126a4                           @ 08112696 05e0
DAT_08112698:
    .word  0x03005788                     @ 08112698 88570003
LAB_0811269c:
    adds r2,#0x8    @ 0811269c 0832
    adds r1,#0x1    @ 0811269e 0131
    cmp r1,#0x13                             @ 081126a0 1329
    bgt LAB_081126aa                         @ 081126a2 02dc
LAB_081126a4:
    ldr r0,[r2,#0x0]                         @ 081126a4 1068
    cmp r0,r3                                @ 081126a6 9842
    bne LAB_0811269c                         @ 081126a8 f8d1
LAB_081126aa:
    adds r0,r1,#0x0    @ 081126aa 081c
    bx lr                                    @ 081126ac 7047
    .zero  0x2

@ Resolves file descriptor fd to corresponding standard stream FILE pointer or computed offset.
@ Compares fd field (FILE+0xe, ldrsh 16-bit signed) of stdin/stdout/stderr in sequence; on match returns pointer stored at corresponding buffer address (stdin=0x0300577c / stdout=0x03005780 / stderr=0x03005784).
@ If no match and fd differs from third entry by 0x20, returns adjusted value; unknown fd takes r0=r2-0x20 path.
@ Called by _swiread / _read / _swiwrite / _write / _swilseek as fd-to-FILE mapping.
@ 
@ Constants:
@ - STDIN_PTR_LOC=0x0300577c (stdin FILE* storage address, IWRAM)
@ - STDOUT_PTR_LOC=0x03005780 (stdout FILE* storage address, IWRAM)
@ - STDERR_PTR_LOC=0x03005784 (stderr FILE* storage address, IWRAM)
@ - IMPURE_PTR=0x09ed4d94 (_impure_ptr)
@ - FD_FIELD_OFFSET=0xe (fd field offset within FILE struct)
resolve_stdio_file_by_fd:
    adds r2,r0,#0x0    @ 081126b0 021c
    ldr r0, DAT_081126c4                     @ 081126b2 0448
    ldr r1,[r0,#0x0]                         @ 081126b4 0168
    ldr r0,[r1,#0x4]                         @ 081126b6 4868
    movs r3,#0xe    @ 081126b8 0e23
    ldrsh r0,[r0,r3]                         @ 081126ba c05e
    cmp r2,r0                                @ 081126bc 8242
    bne LAB_081126cc                         @ 081126be 05d1
    ldr r0, DAT_081126c8                     @ 081126c0 0148
    b LAB_081126f2                           @ 081126c2 16e0
DAT_081126c4:
    .word  0x09ed4d94                     @ 081126c4 944ded09
DAT_081126c8:
    .word  0x0300577c                     @ 081126c8 7c570003
LAB_081126cc:
    ldr r0,[r1,#0x8]                         @ 081126cc 8868
    movs r3,#0xe    @ 081126ce 0e23
    ldrsh r0,[r0,r3]                         @ 081126d0 c05e
    cmp r2,r0                                @ 081126d2 8242
    bne LAB_081126e0                         @ 081126d4 04d1
    ldr r0, DAT_081126dc                     @ 081126d6 0148
    b LAB_081126f2                           @ 081126d8 0be0
    .zero  0x2
DAT_081126dc:
    .word  0x03005780                     @ 081126dc 80570003
LAB_081126e0:
    ldr r0,[r1,#0xc]                         @ 081126e0 c868
    movs r1,#0xe    @ 081126e2 0e21
    ldrsh r0,[r0,r1]                         @ 081126e4 405e
    cmp r2,r0                                @ 081126e6 8242
    beq LAB_081126f0                         @ 081126e8 02d0
    adds r0,r2,#0x0    @ 081126ea 101c
    subs r0,#0x20    @ 081126ec 2038
    b LAB_081126f4                           @ 081126ee 01e0
LAB_081126f0:
    ldr r0, DAT_081126f8                     @ 081126f0 0148
LAB_081126f2:
    ldr r0,[r0,#0x0]                         @ 081126f2 0068
LAB_081126f4:
    bx lr                                    @ 081126f4 7047
    .zero  0x2
DAT_081126f8:
    .word  0x03005784                     @ 081126f8 84570003
initialise_monitor_handles:
    push {r4,r5,lr}                          @ 081126fc 30b5
    sub sp,#0xc                              @ 081126fe 83b0
    ldr r4, DAT_08112758                     @ 08112700 154c
    str r4,[sp,#0x0]                         @ 08112702 0094
    movs r3,#0x3    @ 08112704 0323
    str r3,[sp,#0x8]                         @ 08112706 0293
    movs r0,#0x0    @ 08112708 0020
    str r0,[sp,#0x4]                         @ 0811270a 0190
    movs r5,#0x1    @ 0811270c 0125
    adds r0,r5,#0x0    @ 0811270e 281c
    .hword 0x4669    @ 08112710 6946
    svc 0xab                                 @ 08112712 abdf
    adds r2,r0,#0x0    @ 08112714 021c
    ldr r5, DAT_0811275c                     @ 08112716 114d
    str r2,[r5,#0x0]                         @ 08112718 2a60
    str r4,[sp,#0x0]                         @ 0811271a 0094
    str r3,[sp,#0x8]                         @ 0811271c 0293
    movs r0,#0x4    @ 0811271e 0420
    str r0,[sp,#0x4]                         @ 08112720 0190
    ldr r3, DAT_08112760                     @ 08112722 0f4b
    movs r4,#0x1    @ 08112724 0124
    adds r0,r4,#0x0    @ 08112726 201c
    .hword 0x4669    @ 08112728 6946
    svc 0xab                                 @ 0811272a abdf
    adds r2,r0,#0x0    @ 0811272c 021c
    ldr r0, DAT_08112764                     @ 0811272e 0d48
    str r2,[r0,#0x0]                         @ 08112730 0260
    str r2,[r3,#0x0]                         @ 08112732 1a60
    ldr r2, DAT_08112768                     @ 08112734 0c4a
    adds r1,r2,#0x0    @ 08112736 111c
    subs r4,#0x2    @ 08112738 023c
    adds r0,r2,#0x0    @ 0811273a 101c
    adds r0,#0x98    @ 0811273c 9830
LAB_0811273e:
    str r4,[r0,#0x0]                         @ 0811273e 0460
    subs r0,#0x8    @ 08112740 0838
    cmp r0,r1                                @ 08112742 8842
    bge LAB_0811273e                         @ 08112744 fbda
    movs r0,#0x0    @ 08112746 0020
    ldr r1,[r5,#0x0]                         @ 08112748 2968
    str r1,[r2,#0x0]                         @ 0811274a 1160
    str r0,[r2,#0x4]                         @ 0811274c 5060
    ldr r1,[r3,#0x0]                         @ 0811274e 1968
    str r1,[r2,#0x8]                         @ 08112750 9160
    str r0,[r2,#0xc]                         @ 08112752 d060
    add sp,#0xc                              @ 08112754 03b0
    pop {r4,r5,pc}                           @ 08112756 30bd
DAT_08112758:
    .word  0x09e587ac                     @ 08112758 ac87e509
DAT_0811275c:
    .word  0x0300577c                     @ 0811275c 7c570003
DAT_08112760:
    .word  0x03005780                     @ 08112760 80570003
DAT_08112764:
    .word  0x03005784                     @ 08112764 84570003
DAT_08112768:
    .word  0x03005788                     @ 08112768 88570003

@ Issues ARM semihosting SVC 0xAB call for SYS_HEAPINFO (opcode 0x13) to query heap/stack layout reported by debug host.
@ r0=0x13, r1=0 (no parameter block); after svc 0xab returns host-reported heap info pointer.
@ Called by FUN_08112780 to initialize semihosting heap tracking structure.
@ 
@ Constants:
@ - SYS_HEAPINFO=0x13 (ARM semihosting opcode: query heap info)
query_semihost_heap_info:
    push {r4,lr}                             @ 0811276c 10b5
    movs r3,#0x13    @ 0811276e 1323
    movs r4,#0x0    @ 08112770 0024
    adds r0,r3,#0x0    @ 08112772 181c
    adds r1,r4,#0x0    @ 08112774 211c
    svc 0xab                                 @ 08112776 abdf
    adds r2,r0,#0x0    @ 08112778 021c
    adds r0,r2,#0x0    @ 0811277a 101c
    pop {r4,pc}                              @ 0811277c 10bd
    .zero  0x2

@ Initializes the heap pointer field in the newlib reent struct via the semihosting interface. Calls get_global_reent to get the global reent pointer (r4), then calls query_semihost_heap_info to query heap layout information from the host (SYS_HEAPINFO, opcode 0x13), and stores the query result into reent[+0x0] (heap info pointer field). Returns the input r0 (original passed-in value, transparently passed through to the caller for error path use).
@ 
@ Call context: semihosting I/O functions such as _read / _write / _swiopen call this function (directly or via FUN_08112794) to re-synchronize the newlib reent heap tracking state when a bottom-level operation returns -1 error, then exit along the error path.
init_reent_heap_ptr_via_semihost:
    push {r4,r5,lr}                          @ 08112780 30b5
    adds r5,r0,#0x0    @ 08112782 051c
    bl get_global_reent                      @ 08112784 00f010fa
    adds r4,r0,#0x0    @ 08112788 041c
    bl query_semihost_heap_info              @ 0811278a fff7efff
    str r0,[r4,#0x0]                         @ 0811278e 2060
    adds r0,r5,#0x0    @ 08112790 281c
    pop {r4,r5,pc}                           @ 08112792 30bd

@ newlib semihosting I/O layer error-path forwarding function. Receives semihosting bottom-level operation return value (r0); if -1 (error flag), calls init_reent_heap_ptr_via_semihost to re-synchronize newlib reent heap pointer state, then returns -1; if non-(-1), passes value through directly. Called by _swilseek wrapper (0x0811289c) and _swiclose wrapper (0x08112a00) as the unified error-handling exit after semihosting syscall return.
@ 
@ Constants:
@ ERROR_SENTINEL=-1 (0xffffffff, semihosting operation failure flag)
@ 
@ Params: r0=semihost_result [any] (-1=error, >=0=success)
@ Returns: r0=semihost_result (passthrough; -1 path also triggers init_reent_heap_ptr_via_semihost side effect)
@ Side effects: if r0==-1: calls init_reent_heap_ptr_via_semihost(-1), re-syncing newlib reent heap pointer [reent_struct+0x0]
handle_semihost_io_result:
    push {lr}                                @ 08112794 00b5
    adds r1,r0,#0x0    @ 08112796 011c
    movs r0,#0x1    @ 08112798 0120
    rsbs r0,r0,#0    @ 0811279a 4042
    cmp r1,r0                                @ 0811279c 8142
    beq LAB_081127a4                         @ 0811279e 01d0
    adds r0,r1,#0x0    @ 081127a0 081c
    b LAB_081127aa                           @ 081127a2 02e0
LAB_081127a4:
    adds r0,r1,#0x0    @ 081127a4 081c
    bl init_reent_heap_ptr_via_semihost      @ 081127a6 fff7ebff
LAB_081127aa:
    pop {pc}                                 @ 081127aa 00bd
_swiread:
    push {r4,r5,lr}                          @ 081127ac 30b5
    sub sp,#0xc                              @ 081127ae 83b0
    adds r4,r1,#0x0    @ 081127b0 0c1c
    adds r5,r2,#0x0    @ 081127b2 151c
    bl resolve_stdio_file_by_fd              @ 081127b4 fff77cff
    str r0,[sp,#0x0]                         @ 081127b8 0090
    str r4,[sp,#0x4]                         @ 081127ba 0194
    str r5,[sp,#0x8]                         @ 081127bc 0295
    movs r3,#0x6    @ 081127be 0623
    adds r0,r3,#0x0    @ 081127c0 181c
    .hword 0x4669    @ 081127c2 6946
    svc 0xab                                 @ 081127c4 abdf
    adds r2,r0,#0x0    @ 081127c6 021c
    adds r0,r2,#0x0    @ 081127c8 101c
    add sp,#0xc                              @ 081127ca 03b0
    pop {r4,r5,pc}                           @ 081127cc 30bd
    .zero  0x2
_read:
    push {r4,r5,r6,r7,lr}                    @ 081127d0 f0b5
    adds r4,r0,#0x0    @ 081127d2 041c
    adds r5,r1,#0x0    @ 081127d4 0d1c
    adds r7,r2,#0x0    @ 081127d6 171c
    bl resolve_stdio_file_by_fd              @ 081127d8 fff76aff
    bl find_semihost_handle_slot             @ 081127dc fff758ff
    adds r6,r0,#0x0    @ 081127e0 061c
    adds r0,r4,#0x0    @ 081127e2 201c
    adds r1,r5,#0x0    @ 081127e4 291c
    adds r2,r7,#0x0    @ 081127e6 3a1c
    bl _swiread                              @ 081127e8 fff7e0ff
    cmp r0,#0x0                              @ 081127ec 0028
    bge LAB_081127fa                         @ 081127ee 04da
    movs r0,#0x1    @ 081127f0 0120
    rsbs r0,r0,#0    @ 081127f2 4042
    bl init_reent_heap_ptr_via_semihost      @ 081127f4 fff7c4ff
    b LAB_08112810                           @ 081127f8 0ae0
LAB_081127fa:
    subs r2,r7,r0    @ 081127fa 3a1a
    cmp r6,#0x14                             @ 081127fc 142e
    beq LAB_0811280e                         @ 081127fe 06d0
    ldr r0, DAT_08112814                     @ 08112800 0448
    lsls r1,r6,#0x3    @ 08112802 f100
    adds r0,#0x4    @ 08112804 0430
    adds r1,r1,r0    @ 08112806 0918
    ldr r0,[r1,#0x0]                         @ 08112808 0868
    adds r0,r0,r2    @ 0811280a 8018
    str r0,[r1,#0x0]                         @ 0811280c 0860
LAB_0811280e:
    adds r0,r2,#0x0    @ 0811280e 101c
LAB_08112810:
    pop {r4,r5,r6,r7,pc}                     @ 08112810 f0bd
    .zero  0x2
DAT_08112814:
    .word  0x03005788                     @ 08112814 88570003
_swilseek:
    push {r4,r5,r6,r7,lr}                    @ 08112818 f0b5
    .hword 0x4647    @ 0811281a 4746
    push {r7}                                @ 0811281c 80b4
    sub sp,#0x8                              @ 0811281e 82b0
    .hword 0x4680    @ 08112820 8046
    adds r5,r1,#0x0    @ 08112822 0d1c
    adds r4,r2,#0x0    @ 08112824 141c
    bl resolve_stdio_file_by_fd              @ 08112826 fff743ff
    adds r7,r0,#0x0    @ 0811282a 071c
    bl find_semihost_handle_slot             @ 0811282c fff730ff
    adds r6,r0,#0x0    @ 08112830 061c
    cmp r4,#0x1                              @ 08112832 012c
    bne LAB_0811284e                         @ 08112834 0bd1
    cmp r6,#0x14                             @ 08112836 142e
    bne LAB_08112840                         @ 08112838 02d1
    movs r0,#0x1    @ 0811283a 0120
    rsbs r0,r0,#0    @ 0811283c 4042
    b LAB_08112890                           @ 0811283e 27e0
LAB_08112840:
    ldr r0, DAT_08112898                     @ 08112840 1548
    lsls r1,r6,#0x3    @ 08112842 f100
    adds r0,#0x4    @ 08112844 0430
    adds r1,r1,r0    @ 08112846 0918
    ldr r0,[r1,#0x0]                         @ 08112848 0868
    adds r5,r5,r0    @ 0811284a 2d18
    movs r4,#0x0    @ 0811284c 0024
LAB_0811284e:
    cmp r4,#0x2                              @ 0811284e 022c
    bne LAB_08112860                         @ 08112850 06d1
    str r7,[sp,#0x0]                         @ 08112852 0097
    movs r3,#0xc    @ 08112854 0c23
    adds r0,r3,#0x0    @ 08112856 181c
    .hword 0x4669    @ 08112858 6946
    svc 0xab                                 @ 0811285a abdf
    adds r2,r0,#0x0    @ 0811285c 021c
    adds r5,r5,r2    @ 0811285e ad18
LAB_08112860:
    .hword 0x4640    @ 08112860 4046
    bl resolve_stdio_file_by_fd              @ 08112862 fff725ff
    str r0,[sp,#0x0]                         @ 08112866 0090
    str r5,[sp,#0x4]                         @ 08112868 0195
    movs r3,#0xa    @ 0811286a 0a23
    adds r0,r3,#0x0    @ 0811286c 181c
    .hword 0x4669    @ 0811286e 6946
    svc 0xab                                 @ 08112870 abdf
    adds r2,r0,#0x0    @ 08112872 021c
    cmp r6,#0x14                             @ 08112874 142e
    beq LAB_08112886                         @ 08112876 06d0
    cmp r2,#0x0                              @ 08112878 002a
    bne LAB_08112886                         @ 0811287a 04d1
    ldr r0, DAT_08112898                     @ 0811287c 0648
    lsls r1,r6,#0x3    @ 0811287e f100
    adds r0,#0x4    @ 08112880 0430
    adds r1,r1,r0    @ 08112882 0918
    str r5,[r1,#0x0]                         @ 08112884 0d60
LAB_08112886:
    movs r0,#0x1    @ 08112886 0120
    rsbs r0,r0,#0    @ 08112888 4042
    cmp r2,#0x0                              @ 0811288a 002a
    bne LAB_08112890                         @ 0811288c 00d1
    adds r0,r5,#0x0    @ 0811288e 281c
LAB_08112890:
    add sp,#0x8                              @ 08112890 02b0
    pop {r3}                                 @ 08112892 08bc
    .hword 0x4698    @ 08112894 9846
    pop {r4,r5,r6,r7,pc}                     @ 08112896 f0bd
DAT_08112898:
    .word  0x03005788                     @ 08112898 88570003

@ newlib semihosting lseek 重入包装器, 与 wrap_write_r(0x08112af4)/wrap_read_r(0x08112c38)/wrap_sclose_r(0x08112bb4) 构成对称四元组.
@ 调用链: _swilseek (svc 0xab SYS_SEEK) -> handle_semihost_io_result (错误路径调用 init_reent_heap_ptr_via_semihost, 同步 reent 堆指针; 非错误路径透传结果).
@ 调用方 FUN_08112c08(0x08112c08) 在调用前清零 EWRAM errno 缓存(0x02029ea8), 调用后若返回 -1 且 errno 非零则写回 errno 至调用方 reent 结构体; 本函数自身不持有 errno 逻辑, 仅封装 lseek + 统一错误处理.
wrap_lseek_r:
    push {lr}                                @ 0811289c 00b5
    bl _swilseek                             @ 0811289e fff7bbff
    bl handle_semihost_io_result             @ 081128a2 fff777ff
    pop {pc}                                 @ 081128a6 00bd
_swiwrite:
    push {r4,r5,lr}                          @ 081128a8 30b5
    sub sp,#0xc                              @ 081128aa 83b0
    adds r4,r1,#0x0    @ 081128ac 0c1c
    adds r5,r2,#0x0    @ 081128ae 151c
    bl resolve_stdio_file_by_fd              @ 081128b0 fff7fefe
    str r0,[sp,#0x0]                         @ 081128b4 0090
    str r4,[sp,#0x4]                         @ 081128b6 0194
    str r5,[sp,#0x8]                         @ 081128b8 0295
    movs r3,#0x5    @ 081128ba 0523
    adds r0,r3,#0x0    @ 081128bc 181c
    .hword 0x4669    @ 081128be 6946
    svc 0xab                                 @ 081128c0 abdf
    adds r2,r0,#0x0    @ 081128c2 021c
    adds r0,r2,#0x0    @ 081128c4 101c
    add sp,#0xc                              @ 081128c6 03b0
    pop {r4,r5,pc}                           @ 081128c8 30bd
    .zero  0x2
_write:
    push {r4,r5,r6,r7,lr}                    @ 081128cc f0b5
    adds r4,r0,#0x0    @ 081128ce 041c
    adds r5,r1,#0x0    @ 081128d0 0d1c
    adds r6,r2,#0x0    @ 081128d2 161c
    bl resolve_stdio_file_by_fd              @ 081128d4 fff7ecfe
    bl find_semihost_handle_slot             @ 081128d8 fff7dafe
    adds r7,r0,#0x0    @ 081128dc 071c
    adds r0,r4,#0x0    @ 081128de 201c
    adds r1,r5,#0x0    @ 081128e0 291c
    adds r2,r6,#0x0    @ 081128e2 321c
    bl _swiwrite                             @ 081128e4 fff7e0ff
    movs r1,#0x1    @ 081128e8 0121
    rsbs r1,r1,#0    @ 081128ea 4942
    cmp r0,r1                                @ 081128ec 8842
    beq LAB_081128f4                         @ 081128ee 01d0
    cmp r0,r6                                @ 081128f0 b042
    bne LAB_081128fc                         @ 081128f2 03d1
LAB_081128f4:
    adds r0,r1,#0x0    @ 081128f4 081c
    bl init_reent_heap_ptr_via_semihost      @ 081128f6 fff743ff
    b LAB_08112912                           @ 081128fa 0ae0
LAB_081128fc:
    subs r2,r6,r0    @ 081128fc 321a
    cmp r7,#0x14                             @ 081128fe 142f
    beq LAB_08112910                         @ 08112900 06d0
    ldr r0, DAT_08112914                     @ 08112902 0448
    lsls r1,r7,#0x3    @ 08112904 f900
    adds r0,#0x4    @ 08112906 0430
    adds r1,r1,r0    @ 08112908 0918
    ldr r0,[r1,#0x0]                         @ 0811290a 0868
    adds r0,r0,r2    @ 0811290c 8018
    str r0,[r1,#0x0]                         @ 0811290e 0860
LAB_08112910:
    adds r0,r2,#0x0    @ 08112910 101c
LAB_08112912:
    pop {r4,r5,r6,r7,pc}                     @ 08112912 f0bd
DAT_08112914:
    .word  0x03005788                     @ 08112914 88570003
_swiopen:
    push {r4,r5,r6,r7,lr}                    @ 08112918 f0b5
    .hword 0x4647    @ 0811291a 4746
    push {r7}                                @ 0811291c 80b4
    sub sp,#0xc                              @ 0811291e 83b0
    adds r7,r0,#0x0    @ 08112920 071c
    adds r4,r1,#0x0    @ 08112922 0c1c
    movs r5,#0x0    @ 08112924 0025
    movs r6,#0x1    @ 08112926 0126
    rsbs r6,r6,#0    @ 08112928 7642
    adds r0,r6,#0x0    @ 0811292a 301c
    bl find_semihost_handle_slot             @ 0811292c fff7b0fe
    .hword 0x4680    @ 08112930 8046
    cmp r0,#0x14                             @ 08112932 1428
    bne LAB_0811293a                         @ 08112934 01d1
    adds r0,r6,#0x0    @ 08112936 301c
    b LAB_081129ae                           @ 08112938 39e0
LAB_0811293a:
    movs r0,#0x2    @ 0811293a 0220
    ands r0,r4    @ 0811293c 2040
    cmp r0,#0x0                              @ 0811293e 0028
    beq LAB_08112944                         @ 08112940 00d0
    movs r5,#0x2    @ 08112942 0225
LAB_08112944:
    movs r0,#0x80    @ 08112944 8020
    lsls r0,r0,#0x2    @ 08112946 8000
    ands r0,r4    @ 08112948 2040
    cmp r0,#0x0                              @ 0811294a 0028
    beq LAB_08112952                         @ 0811294c 01d0
    movs r0,#0x4    @ 0811294e 0420
    orrs r5,r0    @ 08112950 0543
LAB_08112952:
    movs r0,#0x80    @ 08112952 8020
    lsls r0,r0,#0x3    @ 08112954 c000
    ands r0,r4    @ 08112956 2040
    cmp r0,#0x0                              @ 08112958 0028
    beq LAB_08112960                         @ 0811295a 01d0
    movs r0,#0x4    @ 0811295c 0420
    orrs r5,r0    @ 0811295e 0543
LAB_08112960:
    movs r1,#0x8    @ 08112960 0821
    ands r4,r1    @ 08112962 0c40
    cmp r4,#0x0                              @ 08112964 002c
    beq LAB_08112970                         @ 08112966 03d0
    movs r0,#0x5    @ 08112968 0520
    rsbs r0,r0,#0    @ 0811296a 4042
    ands r5,r0    @ 0811296c 0540
    orrs r5,r1    @ 0811296e 0d43
LAB_08112970:
    str r7,[sp,#0x0]                         @ 08112970 0097
    adds r0,r7,#0x0    @ 08112972 381c
    bl strlen                                @ 08112974 fcf7b2fb
    str r0,[sp,#0x8]                         @ 08112978 0290
    str r5,[sp,#0x4]                         @ 0811297a 0195
    movs r2,#0x1    @ 0811297c 0122
    adds r0,r2,#0x0    @ 0811297e 101c
    .hword 0x4669    @ 08112980 6946
    svc 0xab                                 @ 08112982 abdf
    adds r3,r0,#0x0    @ 08112984 031c
    cmp r3,#0x0                              @ 08112986 002b
    blt LAB_081129a8                         @ 08112988 0edb
    ldr r0, DAT_081129a4                     @ 0811298a 0648
    .hword 0x4641    @ 0811298c 4146
    lsls r2,r1,#0x3    @ 0811298e ca00
    adds r1,r2,r0    @ 08112990 1118
    str r3,[r1,#0x0]                         @ 08112992 0b60
    adds r0,#0x4    @ 08112994 0430
    adds r2,r2,r0    @ 08112996 1218
    movs r0,#0x0    @ 08112998 0020
    str r0,[r2,#0x0]                         @ 0811299a 1060
    adds r0,r3,#0x0    @ 0811299c 181c
    adds r0,#0x20    @ 0811299e 2030
    b LAB_081129ae                           @ 081129a0 05e0
    .zero  0x2
DAT_081129a4:
    .word  0x03005788                     @ 081129a4 88570003
LAB_081129a8:
    adds r0,r3,#0x0    @ 081129a8 181c
    bl init_reent_heap_ptr_via_semihost      @ 081129aa fff7e9fe
LAB_081129ae:
    add sp,#0xc                              @ 081129ae 03b0
    pop {r3}                                 @ 081129b0 08bc
    .hword 0x4698    @ 081129b2 9846
    pop {r4,r5,r6,r7,pc}                     @ 081129b4 f0bd
    ROM_INCBIN 0x1129b6, 0x16
_swiclose:
    push {lr}                                @ 081129cc 00b5
    sub sp,#0x4                              @ 081129ce 81b0
    bl resolve_stdio_file_by_fd              @ 081129d0 fff76efe
    str r0,[sp,#0x0]                         @ 081129d4 0090
    bl find_semihost_handle_slot             @ 081129d6 fff75bfe
    adds r1,r0,#0x0    @ 081129da 011c
    cmp r1,#0x14                             @ 081129dc 1429
    beq LAB_081129ec                         @ 081129de 05d0
    ldr r0, DAT_081129fc                     @ 081129e0 0648
    lsls r1,r1,#0x3    @ 081129e2 c900
    adds r1,r1,r0    @ 081129e4 0918
    movs r0,#0x1    @ 081129e6 0120
    rsbs r0,r0,#0    @ 081129e8 4042
    str r0,[r1,#0x0]                         @ 081129ea 0860
LAB_081129ec:
    movs r3,#0x2    @ 081129ec 0223
    adds r0,r3,#0x0    @ 081129ee 181c
    .hword 0x4669    @ 081129f0 6946
    svc 0xab                                 @ 081129f2 abdf
    adds r2,r0,#0x0    @ 081129f4 021c
    adds r0,r2,#0x0    @ 081129f6 101c
    add sp,#0x4                              @ 081129f8 01b0
    pop {pc}                                 @ 081129fa 00bd
DAT_081129fc:
    .word  0x03005788                     @ 081129fc 88570003

@ newlib semihosting close 重入包装器, 与 wrap_write_r(0x08112af4)/wrap_read_r(0x08112c38)/wrap_lseek_r(0x0811289c) 构成对称四元组.
@ 调用链: _swiclose (解析 stdio fd -> semihosting handle slot, 清无效标记, svc 0xab SYS_CLOSE) -> handle_semihost_io_result (错误路径调用 init_reent_heap_ptr_via_semihost 同步 reent 堆指针; 非错误路径透传结果 0=成功).
@ 调用方 FUN_08112b7c(0x08112b7c) 在调用前清零 EWRAM errno 缓存(0x02029ea8), 调用后若返回 -1 且 errno 非零则回写 errno 至调用方 reent 结构体; 本函数自身不持有 errno 逻辑, 仅封装 close + 统一错误处理.
wrap_close_r:
    push {lr}                                @ 08112a00 00b5
    bl _swiclose                             @ 08112a02 fff7e3ff
    bl handle_semihost_io_result             @ 08112a06 fff7c5fe
    pop {pc}                                 @ 08112a0a 00bd
    ROM_INCBIN 0x112a0c, 0x44
_sbrk:
    push {r4,r5,r6,lr}                       @ 08112a50 70b5
    adds r6,r0,#0x0    @ 08112a52 061c
    ldr r4, DAT_08112a80                     @ 08112a54 0a4c
    ldr r0,[r4,#0x0]                         @ 08112a56 2068
    cmp r0,#0x0                              @ 08112a58 0028
    bne LAB_08112a60                         @ 08112a5a 01d1
    ldr r0, DAT_08112a84                     @ 08112a5c 0948
    str r0,[r4,#0x0]                         @ 08112a5e 2060
LAB_08112a60:
    ldr r5,[r4,#0x0]                         @ 08112a60 2568
    adds r0,r5,r6    @ 08112a62 a819
    cmp r0,sp                                @ 08112a64 6845
    bls LAB_08112a76                         @ 08112a66 06d9
    ldr r1, DAT_08112a88                     @ 08112a68 0749
    movs r0,#0x1    @ 08112a6a 0120
    movs r2,#0x20    @ 08112a6c 2022
    bl _write                                @ 08112a6e fff72dff
    bl abort                                 @ 08112a72 00f0b5f8
LAB_08112a76:
    ldr r0,[r4,#0x0]                         @ 08112a76 2068
    adds r0,r0,r6    @ 08112a78 8019
    str r0,[r4,#0x0]                         @ 08112a7a 2060
    adds r0,r5,#0x0    @ 08112a7c 281c
    pop {r4,r5,r6,pc}                        @ 08112a7e 70bd
DAT_08112a80:
    .word  0x03005778                     @ 08112a80 78570003
DAT_08112a84:
    .word  0x03005f78                     @ 08112a84 785f0003
DAT_08112a88:
    .word  0x09e587b0                     @ 08112a88 b087e509

@ Semihosting close stub implementation: writes 0x2000 (signifying 0 bytes not transferred / close success) to [r1+4] of result struct, then returns 0 (success).
@ In GBA semihosting environment, close has no real filesystem resources to release, so only writes sentinel value and returns success.
@ Called by FUN_08112bb4 (_sclose wrapper path).
@ 
@ Constants:
@ - CLOSE_SENTINEL=0x2000 (0x80<<6; semihosting result struct "bytes not transferred" field set to 0)
stub_semihost_close:
    movs r0,#0x80    @ 08112a8c 8020
    lsls r0,r0,#0x6    @ 08112a8e 8001
    str r0,[r1,#0x4]                         @ 08112a90 4860
    movs r0,#0x0    @ 08112a92 0020
    bx lr                                    @ 08112a94 7047
    .byte  0x00, 0x00, 0x01, 0x20, 0x40, 0x42, 0x70, 0x47, 0x00, 0x00, 0x70, 0x47, 0x00, 0x00
_gettimeofday:
    push {r4,r5,lr}                          @ 08112aa4 30b5
    adds r2,r0,#0x0    @ 08112aa6 021c
    adds r3,r1,#0x0    @ 08112aa8 0b1c
    cmp r2,#0x0                              @ 08112aaa 002a
    beq LAB_08112ac2                         @ 08112aac 09d0
    movs r4,#0x11    @ 08112aae 1124
    movs r5,#0x0    @ 08112ab0 0025
    adds r0,r4,#0x0    @ 08112ab2 201c
    adds r1,r5,#0x0    @ 08112ab4 291c
    svc 0xab                                 @ 08112ab6 abdf
    adds r5,r0,#0x0    @ 08112ab8 051c
    adds r4,r5,#0x0    @ 08112aba 2c1c
    str r4,[r2,#0x0]                         @ 08112abc 1460
    movs r0,#0x0    @ 08112abe 0020
    str r0,[r2,#0x4]                         @ 08112ac0 5060
LAB_08112ac2:
    cmp r3,#0x0                              @ 08112ac2 002b
    beq LAB_08112acc                         @ 08112ac4 02d0
    movs r0,#0x0    @ 08112ac6 0020
    str r0,[r3,#0x0]                         @ 08112ac8 1860
    str r0,[r3,#0x4]                         @ 08112aca 5860
LAB_08112acc:
    movs r0,#0x0    @ 08112acc 0020
    pop {r4,r5,pc}                           @ 08112ace 30bd
_times:
    push {r4,r5,lr}                          @ 08112ad0 30b5
    adds r2,r0,#0x0    @ 08112ad2 021c
    movs r4,#0x10    @ 08112ad4 1024
    movs r5,#0x0    @ 08112ad6 0025
    adds r0,r4,#0x0    @ 08112ad8 201c
    adds r1,r5,#0x0    @ 08112ada 291c
    svc 0xab                                 @ 08112adc abdf
    adds r3,r0,#0x0    @ 08112ade 031c
    cmp r2,#0x0                              @ 08112ae0 002a
    beq LAB_08112aee                         @ 08112ae2 04d0
    str r3,[r2,#0x0]                         @ 08112ae4 1360
    movs r0,#0x0    @ 08112ae6 0020
    str r0,[r2,#0x4]                         @ 08112ae8 5060
    str r0,[r2,#0x8]                         @ 08112aea 9060
    str r0,[r2,#0xc]                         @ 08112aec d060
LAB_08112aee:
    adds r0,r3,#0x0    @ 08112aee 181c
    pop {r4,r5,pc}                           @ 08112af0 30bd
    .zero  0x2

@ newlib _write_r reentrant wrapper: clears EWRAM errno cache, then forwards r1=fd / r2=buf / r3=len to _write.
@ If _write returns -1 and errno is nonzero, writes errno back to caller-provided r0 pointer.
@ Called by __swrite (0x08112600) on semihosting write path; symmetric with wrap_read_r (0x08112c38).
@ 
@ Constants:
@ - ERRNO_CACHE=0x02029ea8 (newlib global errno staging address, EWRAM)
wrap_write_r:
    push {r4,r5,lr}                          @ 08112af4 30b5
    adds r5,r0,#0x0    @ 08112af6 051c
    adds r0,r1,#0x0    @ 08112af8 081c
    adds r1,r2,#0x0    @ 08112afa 111c
    adds r2,r3,#0x0    @ 08112afc 1a1c
    ldr r4, DAT_08112b20                     @ 08112afe 084c
    movs r3,#0x0    @ 08112b00 0023
    str r3,[r4,#0x0]                         @ 08112b02 2360
    bl _write                                @ 08112b04 fff7e2fe
    adds r1,r0,#0x0    @ 08112b08 011c
    movs r0,#0x1    @ 08112b0a 0120
    rsbs r0,r0,#0    @ 08112b0c 4042
    cmp r1,r0                                @ 08112b0e 8142
    bne LAB_08112b1a                         @ 08112b10 03d1
    ldr r0,[r4,#0x0]                         @ 08112b12 2068
    cmp r0,#0x0                              @ 08112b14 0028
    beq LAB_08112b1a                         @ 08112b16 00d0
    str r0,[r5,#0x0]                         @ 08112b18 2860
LAB_08112b1a:
    adds r0,r1,#0x0    @ 08112b1a 081c
    pop {r4,r5,pc}                           @ 08112b1c 30bd
    .zero  0x2
DAT_08112b20:
    .word  0x02029ea8                     @ 08112b20 a89e0202
_calloc_r:
    push {r4,lr}                             @ 08112b24 10b5
    muls r1,r2    @ 08112b26 5143
    bl _malloc_r                             @ 08112b28 fef772fd
    adds r4,r0,#0x0    @ 08112b2c 041c
    cmp r4,#0x0                              @ 08112b2e 002c
    bne LAB_08112b36                         @ 08112b30 01d1
    movs r0,#0x0    @ 08112b32 0020
    b LAB_08112b7a                           @ 08112b34 21e0
LAB_08112b36:
    adds r0,r4,#0x0    @ 08112b36 201c
    subs r0,#0x8    @ 08112b38 0838
    ldr r0,[r0,#0x4]                         @ 08112b3a 4068
    movs r1,#0x4    @ 08112b3c 0421
    rsbs r1,r1,#0    @ 08112b3e 4942
    ands r0,r1    @ 08112b40 0840
    subs r2,r0,#0x4    @ 08112b42 021f
    cmp r2,#0x24                             @ 08112b44 242a
    bhi LAB_08112b70                         @ 08112b46 13d8
    adds r1,r4,#0x0    @ 08112b48 211c
    cmp r2,#0x13                             @ 08112b4a 132a
    bls LAB_08112b66                         @ 08112b4c 0bd9
    movs r0,#0x0    @ 08112b4e 0020
    stmia r1!,{r0}                           @ 08112b50 01c1
    str r0,[r4,#0x4]                         @ 08112b52 6060
    adds r1,#0x4    @ 08112b54 0431
    cmp r2,#0x1b                             @ 08112b56 1b2a
    bls LAB_08112b66                         @ 08112b58 05d9
    stmia r1!,{r0}                           @ 08112b5a 01c1
    stmia r1!,{r0}                           @ 08112b5c 01c1
    cmp r2,#0x23                             @ 08112b5e 232a
    bls LAB_08112b66                         @ 08112b60 01d9
    stmia r1!,{r0}                           @ 08112b62 01c1
    stmia r1!,{r0}                           @ 08112b64 01c1
LAB_08112b66:
    movs r0,#0x0    @ 08112b66 0020
    stmia r1!,{r0}                           @ 08112b68 01c1
    stmia r1!,{r0}                           @ 08112b6a 01c1
    str r0,[r1,#0x0]                         @ 08112b6c 0860
    b LAB_08112b78                           @ 08112b6e 03e0
LAB_08112b70:
    adds r0,r4,#0x0    @ 08112b70 201c
    movs r1,#0x0    @ 08112b72 0021
    bl memset                                @ 08112b74 fbf722ff
LAB_08112b78:
    adds r0,r4,#0x0    @ 08112b78 201c
LAB_08112b7a:
    pop {r4,pc}                              @ 08112b7a 10bd

@ newlib reentrant close 分派层. 接收 reent 指针(r0)和文件描述符 fd(r1), 先将 EWRAM errno 缓存(0x02029ea8)清零, 再调用 wrap_close_r(fd) 执行底层 _swiclose 关闭操作. 若 wrap_close_r 返回 -1(失败)且 errno 缓存非零, 则将 errno 回写至调用方提供的 reent 结构体(*r0 := errno), 最终透传 wrap_close_r 的原始返回值. 与 close_fd_reentrant(本函数)/lseek_fd_reentrant(0x08112c08)/wrap_write_r/wrap_read_r/wrap_sclose_r 构成对称 errno 传播五元组, 均实现"清零 errno 缓存 -> 调用底层 _swi 层 -> 条件回写 errno"的标准 newlib _r 接口语义. 由 __sclose(0x08112680) 唯一调用.
@ 
@ Constants:
@ - ERRNO_CACHE=0x02029ea8 (newlib errno 暂存地址, EWRAM)
@ - ERR_FLAG=-1 (rsbs r0,r0,#0 of movs r0,#1 构造 -1 用于比较)
close_fd_reentrant:
    push {r4,r5,lr}                          @ 08112b7c 30b5
    adds r5,r0,#0x0    @ 08112b7e 051c
    adds r0,r1,#0x0    @ 08112b80 081c
    ldr r4, DAT_08112ba4                     @ 08112b82 084c
    movs r1,#0x0    @ 08112b84 0021
    str r1,[r4,#0x0]                         @ 08112b86 2160
    bl wrap_close_r                          @ 08112b88 fff73aff
    adds r1,r0,#0x0    @ 08112b8c 011c
    movs r0,#0x1    @ 08112b8e 0120
    rsbs r0,r0,#0    @ 08112b90 4042
    cmp r1,r0                                @ 08112b92 8142
    bne LAB_08112b9e                         @ 08112b94 03d1
    ldr r0,[r4,#0x0]                         @ 08112b96 2068
    cmp r0,#0x0                              @ 08112b98 0028
    beq LAB_08112b9e                         @ 08112b9a 00d0
    str r0,[r5,#0x0]                         @ 08112b9c 2860
LAB_08112b9e:
    adds r0,r1,#0x0    @ 08112b9e 081c
    pop {r4,r5,pc}                           @ 08112ba0 30bd
    .zero  0x2
DAT_08112ba4:
    .word  0x02029ea8                     @ 08112ba4 a89e0202

@ Retrieves newlib global reent structure pointer: double-dereferences _impure_ptr (0x09ed4d94) to obtain current thread's struct _reent*.
@ Function body is only ldr/ldr/bx lr; helper for reading global _impure_ptr.
@ Called by FUN_08112780 (semihosting heap init) to obtain reent structure.
@ 
@ Constants:
@ - IMPURE_PTR=0x09ed4d94 (_impure_ptr, address of newlib global reent structure pointer variable)
get_global_reent:
    ldr r0, DAT_08112bb0                     @ 08112ba8 0148
    ldr r0,[r0,#0x0]                         @ 08112baa 0068
    bx lr                                    @ 08112bac 7047
    .zero  0x2
DAT_08112bb0:
    .word  0x09ed4d94                     @ 08112bb0 944ded09

@ Reentrant newlib _sclose wrapper function, forming a symmetric triplet with wrap_write_r (0x08112af4) / wrap_read_r (0x08112c38). Clears EWRAM errno cache (0x02029ea8), calls stub_semihost_close (r1=fd, r2=flags) to perform the close operation. If stub_semihost_close returns -1 (failure) and errno cache is non-zero, writes errno to the pointer provided by r0 (*reent_errno := errno). Returns the raw result of stub_semihost_close.
@ 
@ Call context: __smakebuf (0x081113d8) calls this function to safely close a file descriptor while initializing stdio buffers; in the semihosting environment stub_semihost_close always succeeds (returns 0), so the errno write-back path is not triggered.
@ 
@ Constants:
@ ERRNO_CACHE=0x02029ea8 (newlib global errno staging address, EWRAM)
wrap_sclose_r:
    push {r4,r5,lr}                          @ 08112bb4 30b5
    adds r5,r0,#0x0    @ 08112bb6 051c
    adds r0,r1,#0x0    @ 08112bb8 081c
    adds r1,r2,#0x0    @ 08112bba 111c
    ldr r4, DAT_08112bdc                     @ 08112bbc 074c
    movs r2,#0x0    @ 08112bbe 0022
    str r2,[r4,#0x0]                         @ 08112bc0 2260
    bl stub_semihost_close                   @ 08112bc2 fff763ff
    adds r1,r0,#0x0    @ 08112bc6 011c
    movs r0,#0x1    @ 08112bc8 0120
    rsbs r0,r0,#0    @ 08112bca 4042
    cmp r1,r0                                @ 08112bcc 8142
    bne LAB_08112bd8                         @ 08112bce 03d1
    ldr r0,[r4,#0x0]                         @ 08112bd0 2068
    cmp r0,#0x0                              @ 08112bd2 0028
    beq LAB_08112bd8                         @ 08112bd4 00d0
    str r0,[r5,#0x0]                         @ 08112bd6 2860
LAB_08112bd8:
    adds r0,r1,#0x0    @ 08112bd8 081c
    pop {r4,r5,pc}                           @ 08112bda 30bd
DAT_08112bdc:
    .word  0x02029ea8                     @ 08112bdc a89e0202
abort:
    .hword 0x469c    @ 08112be0 9c46
    .hword 0x4643    @ 08112be2 4346
    push {r3}                                @ 08112be4 08b4
    .hword 0x4663    @ 08112be6 6346
    movs r2,#0x18    @ 08112be8 1822
    ldr r3, DAT_08112bfc                     @ 08112bea 044b
    adds r0,r2,#0x0    @ 08112bec 101c
    adds r1,r3,#0x0    @ 08112bee 191c
    svc 0xab                                 @ 08112bf0 abdf
    .hword 0x4680    @ 08112bf2 8046
    pop {r3}                                 @ 08112bf4 08bc
    .hword 0x4698    @ 08112bf6 9846
    bx lr                                    @ 08112bf8 7047
    .zero  0x2
DAT_08112bfc:
    .word  0x00020022                     @ 08112bfc 22000200

@ isatty stub that always returns 1: function body is only movs r0,#1; bx lr, declaring any fd as a terminal device.
@ In GBA semihosting environment all fds are treated as interactive terminal; no actual device type detection needed.
@ Called by __smakebuf (0x081113d8) to decide whether to enable line buffering.
stub_isatty_true:
    movs r0,#0x1    @ 08112c00 0120
    bx lr                                    @ 08112c02 7047
    .byte  0x70, 0x47, 0x00, 0x00

@ newlib reentrant lseek 分派层. 接收 reent 指针(r0), 文件描述符 fd(r1), 偏移量 offset(r2), 定位模式 whence(r3), 先将 EWRAM errno 缓存(0x02029ea8)清零, 再调用 wrap_lseek_r(fd, offset, whence) 执行底层 _swilseek 定位操作. 若 wrap_lseek_r 返回 -1(失败)且 errno 缓存非零, 则将 errno 回写至 *reent_ptr, 最终透传 wrap_lseek_r 原始返回值. 与 close_fd_reentrant(0x08112b7c)/wrap_write_r(0x08112af4)/wrap_read_r(0x08112c38)/wrap_sclose_r(0x08112bb4) 构成对称 errno 传播五元组. 由 __swrite(0x08112600) 在追加模式下定位到文件末尾, 由 __sseek(0x08112640) 在通用定位场景中调用.
@ 
@ Constants:
@ - ERRNO_CACHE=0x02029ea8 (newlib errno 暂存地址, EWRAM)
@ - ERR_FLAG=-1 (rsbs r0,r0,#0 of movs r0,#1 构造 -1 用于比较)
lseek_fd_reentrant:
    push {r4,r5,lr}                          @ 08112c08 30b5
    adds r5,r0,#0x0    @ 08112c0a 051c
    adds r0,r1,#0x0    @ 08112c0c 081c
    adds r1,r2,#0x0    @ 08112c0e 111c
    adds r2,r3,#0x0    @ 08112c10 1a1c
    ldr r4, DAT_08112c34                     @ 08112c12 084c
    movs r3,#0x0    @ 08112c14 0023
    str r3,[r4,#0x0]                         @ 08112c16 2360
    bl wrap_lseek_r                          @ 08112c18 fff740fe
    adds r1,r0,#0x0    @ 08112c1c 011c
    movs r0,#0x1    @ 08112c1e 0120
    rsbs r0,r0,#0    @ 08112c20 4042
    cmp r1,r0                                @ 08112c22 8142
    bne LAB_08112c2e                         @ 08112c24 03d1
    ldr r0,[r4,#0x0]                         @ 08112c26 2068
    cmp r0,#0x0                              @ 08112c28 0028
    beq LAB_08112c2e                         @ 08112c2a 00d0
    str r0,[r5,#0x0]                         @ 08112c2c 2860
LAB_08112c2e:
    adds r0,r1,#0x0    @ 08112c2e 081c
    pop {r4,r5,pc}                           @ 08112c30 30bd
    .zero  0x2
DAT_08112c34:
    .word  0x02029ea8                     @ 08112c34 a89e0202

@ newlib _read_r reentrant wrapper: clears EWRAM errno cache, then forwards r1=fd / r2=buf / r3=len to _read.
@ If _read returns -1 and errno is nonzero, writes errno back to caller-provided r0 pointer.
@ Called by __sread (0x081125cc) on semihosting read path; symmetric with wrap_write_r (0x08112af4).
@ 
@ Constants:
@ - ERRNO_CACHE=0x02029ea8 (newlib global errno staging address, EWRAM)
wrap_read_r:
    push {r4,r5,lr}                          @ 08112c38 30b5
    adds r5,r0,#0x0    @ 08112c3a 051c
    adds r0,r1,#0x0    @ 08112c3c 081c
    adds r1,r2,#0x0    @ 08112c3e 111c
    adds r2,r3,#0x0    @ 08112c40 1a1c
    ldr r4, DAT_08112c64                     @ 08112c42 084c
    movs r3,#0x0    @ 08112c44 0023
    str r3,[r4,#0x0]                         @ 08112c46 2360
    bl _read                                 @ 08112c48 fff7c2fd
    adds r1,r0,#0x0    @ 08112c4c 011c
    movs r0,#0x1    @ 08112c4e 0120
    rsbs r0,r0,#0    @ 08112c50 4042
    cmp r1,r0                                @ 08112c52 8142
    bne LAB_08112c5e                         @ 08112c54 03d1
    ldr r0,[r4,#0x0]                         @ 08112c56 2068
    cmp r0,#0x0                              @ 08112c58 0028
    beq LAB_08112c5e                         @ 08112c5a 00d0
    str r0,[r5,#0x0]                         @ 08112c5c 2860
LAB_08112c5e:
    adds r0,r1,#0x0    @ 08112c5e 081c
    pop {r4,r5,pc}                           @ 08112c60 30bd
    .zero  0x2
DAT_08112c64:
    .word  0x02029ea8                     @ 08112c64 a89e0202
__pack_d:
    push {r4,r5,r6,r7,lr}                    @ 08112c68 f0b5
    sub sp,#0x8                              @ 08112c6a 82b0
    adds r1,r0,#0x0    @ 08112c6c 011c
    ldr r4,[r1,#0xc]                         @ 08112c6e cc68
    ldr r5,[r1,#0x10]                        @ 08112c70 0d69
    ldr r7,[r1,#0x4]                         @ 08112c72 4f68
    movs r6,#0x0    @ 08112c74 0026
    movs r2,#0x0    @ 08112c76 0022
    ldr r0,[r1,#0x0]                         @ 08112c78 0868
    cmp r0,#0x1                              @ 08112c7a 0128
    bhi LAB_08112c80                         @ 08112c7c 00d8
    movs r2,#0x1    @ 08112c7e 0122
LAB_08112c80:
    cmp r2,#0x0                              @ 08112c80 002a
    beq LAB_08112ca0                         @ 08112c82 0dd0
    ldr r6, DAT_08112c94                     @ 08112c84 034e
    ldr r2, DAT_08112c98                     @ 08112c86 044a
    ldr r3, DAT_08112c9c                     @ 08112c88 044b
    adds r0,r4,#0x0    @ 08112c8a 201c
    adds r1,r5,#0x0    @ 08112c8c 291c
    orrs r1,r3    @ 08112c8e 1943
    b LAB_08112d58                           @ 08112c90 62e0
    .zero  0x2
DAT_08112c94:
    .word  0x000007ff                     @ 08112c94 ff070000
DAT_08112c98:
    .word  0x00000000                     @ 08112c98 00000000
DAT_08112c9c:
    .word  0x00080000                     @ 08112c9c 00000800
LAB_08112ca0:
    movs r2,#0x0    @ 08112ca0 0022
    cmp r0,#0x4                              @ 08112ca2 0428
    bne LAB_08112ca8                         @ 08112ca4 00d1
    movs r2,#0x1    @ 08112ca6 0122
LAB_08112ca8:
    cmp r2,#0x0                              @ 08112ca8 002a
    bne LAB_08112cf4                         @ 08112caa 23d1
    movs r2,#0x0    @ 08112cac 0022
    cmp r0,#0x2                              @ 08112cae 0228
    bne LAB_08112cb4                         @ 08112cb0 00d1
    movs r2,#0x1    @ 08112cb2 0122
LAB_08112cb4:
    cmp r2,#0x0                              @ 08112cb4 002a
    beq LAB_08112cbe                         @ 08112cb6 02d0
    movs r4,#0x0    @ 08112cb8 0024
    movs r5,#0x0    @ 08112cba 0025
    b LAB_08112d5c                           @ 08112cbc 4ee0
LAB_08112cbe:
    adds r0,r5,#0x0    @ 08112cbe 281c
    orrs r0,r4    @ 08112cc0 2043
    cmp r0,#0x0                              @ 08112cc2 0028
    beq LAB_08112d5c                         @ 08112cc4 4ad0
    ldr r2,[r1,#0x8]                         @ 08112cc6 8a68
    ldr r0, DAT_08112cdc                     @ 08112cc8 0448
    cmp r2,r0                                @ 08112cca 8242
    bge LAB_08112cee                         @ 08112ccc 0fda
    subs r2,r0,r2    @ 08112cce 821a
    cmp r2,#0x38                             @ 08112cd0 382a
    ble LAB_08112ce0                         @ 08112cd2 05dd
    movs r4,#0x0    @ 08112cd4 0024
    movs r5,#0x0    @ 08112cd6 0025
    b LAB_08112d4e                           @ 08112cd8 39e0
    .zero  0x2
DAT_08112cdc:
    .word  0xfffffc02                     @ 08112cdc 02fcffff
LAB_08112ce0:
    adds r1,r5,#0x0    @ 08112ce0 291c
    adds r0,r4,#0x0    @ 08112ce2 201c
    bl __lshrdi3                             @ 08112ce4 01f034fb
    adds r5,r1,#0x0    @ 08112ce8 0d1c
    adds r4,r0,#0x0    @ 08112cea 041c
    b LAB_08112d4e                           @ 08112cec 2fe0
LAB_08112cee:
    ldr r0, DAT_08112cfc                     @ 08112cee 0348
    cmp r2,r0                                @ 08112cf0 8242
    ble LAB_08112d04                         @ 08112cf2 07dd
LAB_08112cf4:
    ldr r6, DAT_08112d00                     @ 08112cf4 024e
    movs r4,#0x0    @ 08112cf6 0024
    movs r5,#0x0    @ 08112cf8 0025
    b LAB_08112d5c                           @ 08112cfa 2fe0
DAT_08112cfc:
    .word  0x000003ff                     @ 08112cfc ff030000
DAT_08112d00:
    .word  0x000007ff                     @ 08112d00 ff070000
LAB_08112d04:
    ldr r0, DAT_08112d2c                     @ 08112d04 0948
    adds r6,r2,r0    @ 08112d06 1618
    movs r0,#0xff    @ 08112d08 ff20
    adds r1,r4,#0x0    @ 08112d0a 211c
    ands r1,r0    @ 08112d0c 0140
    movs r2,#0x0    @ 08112d0e 0022
    cmp r1,#0x80                             @ 08112d10 8029
    bne LAB_08112d30                         @ 08112d12 0dd1
    cmp r2,#0x0                              @ 08112d14 002a
    bne LAB_08112d30                         @ 08112d16 0bd1
    adds r0,#0x1    @ 08112d18 0130
    adds r1,r4,#0x0    @ 08112d1a 211c
    ands r1,r0    @ 08112d1c 0140
    adds r0,r2,#0x0    @ 08112d1e 101c
    orrs r0,r1    @ 08112d20 0843
    cmp r0,#0x0                              @ 08112d22 0028
    beq LAB_08112d38                         @ 08112d24 08d0
    movs r0,#0x80    @ 08112d26 8020
    movs r1,#0x0    @ 08112d28 0021
    b LAB_08112d34                           @ 08112d2a 03e0
DAT_08112d2c:
    .word  0x000003ff                     @ 08112d2c ff030000
LAB_08112d30:
    movs r0,#0x7f    @ 08112d30 7f20
    movs r1,#0x0    @ 08112d32 0021
LAB_08112d34:
    adds r4,r4,r0    @ 08112d34 2418
    adcs r5,r1    @ 08112d36 4d41
LAB_08112d38:
    ldr r0, DAT_08112d9c                     @ 08112d38 1848
    cmp r5,r0                                @ 08112d3a 8542
    bls LAB_08112d4e                         @ 08112d3c 07d9
    lsls r3,r5,#0x1f    @ 08112d3e eb07
    lsrs r2,r4,#0x1    @ 08112d40 6208
    adds r0,r3,#0x0    @ 08112d42 181c
    orrs r0,r2    @ 08112d44 1043
    lsrs r1,r5,#0x1    @ 08112d46 6908
    adds r5,r1,#0x0    @ 08112d48 0d1c
    adds r4,r0,#0x0    @ 08112d4a 041c
    adds r6,#0x1    @ 08112d4c 0136
LAB_08112d4e:
    lsls r3,r5,#0x18    @ 08112d4e 2b06
    lsrs r2,r4,#0x8    @ 08112d50 220a
    adds r0,r3,#0x0    @ 08112d52 181c
    orrs r0,r2    @ 08112d54 1043
    lsrs r1,r5,#0x8    @ 08112d56 290a
LAB_08112d58:
    adds r5,r1,#0x0    @ 08112d58 0d1c
    adds r4,r0,#0x0    @ 08112d5a 041c
LAB_08112d5c:
    str r4,[sp,#0x0]                         @ 08112d5c 0094
    ldr r2, DAT_08112da0                     @ 08112d5e 104a
    ands r2,r5    @ 08112d60 2a40
    ldr r0,[sp,#0x4]                         @ 08112d62 0198
    ldr r1, DAT_08112da4                     @ 08112d64 0f49
    ands r0,r1    @ 08112d66 0840
    orrs r0,r2    @ 08112d68 1043
    str r0,[sp,#0x4]                         @ 08112d6a 0190
    .hword 0x466a    @ 08112d6c 6a46
    ldr r1, DAT_08112da8                     @ 08112d6e 0e49
    adds r0,r1,#0x0    @ 08112d70 081c
    ands r6,r0    @ 08112d72 0640
    lsls r1,r6,#0x4    @ 08112d74 3101
    ldr r0, DAT_08112dac                     @ 08112d76 0d48
    ldrh r3,[r2,#0x6]                        @ 08112d78 d388
    ands r0,r3    @ 08112d7a 1840
    orrs r0,r1    @ 08112d7c 0843
    strh r0,[r2,#0x6]                        @ 08112d7e d080
    lsls r1,r7,#0x7    @ 08112d80 f901
    movs r0,#0x7f    @ 08112d82 7f20
    ldrb r3,[r2,#0x7]                        @ 08112d84 d379
    ands r0,r3    @ 08112d86 1840
    orrs r0,r1    @ 08112d88 0843
    strb r0,[r2,#0x7]                        @ 08112d8a d071
    ldr r1,[sp,#0x0]                         @ 08112d8c 0099
    ldr r0,[sp,#0x4]                         @ 08112d8e 0198
    str r0,[sp,#0x0]                         @ 08112d90 0090
    str r1,[sp,#0x4]                         @ 08112d92 0191
    ldr r0,[sp,#0x0]                         @ 08112d94 0098
    ldr r1,[sp,#0x4]                         @ 08112d96 0199
    add sp,#0x8                              @ 08112d98 02b0
    pop {r4,r5,r6,r7,pc}                     @ 08112d9a f0bd
DAT_08112d9c:
    .word  0x1fffffff                     @ 08112d9c ffffff1f
DAT_08112da0:
    .word  0x000fffff                     @ 08112da0 ffff0f00
DAT_08112da4:
    .word  0xfff00000                     @ 08112da4 0000f0ff
DAT_08112da8:
    .word  0x000007ff                     @ 08112da8 ff070000
DAT_08112dac:
    .word  0xffff800f                     @ 08112dac 0f80ffff
__unpack_d:
    push {r4,r5,r6,r7,lr}                    @ 08112db0 f0b5
    sub sp,#0x8                              @ 08112db2 82b0
    adds r2,r0,#0x0    @ 08112db4 021c
    adds r6,r1,#0x0    @ 08112db6 0e1c
    ldr r1,[r2,#0x4]                         @ 08112db8 5168
    str r1,[sp,#0x0]                         @ 08112dba 0091
    ldr r0,[r2,#0x0]                         @ 08112dbc 1068
    str r0,[sp,#0x4]                         @ 08112dbe 0190
    .hword 0x466a    @ 08112dc0 6a46
    adds r4,r1,#0x0    @ 08112dc2 0c1c
    lsls r0,r0,#0xc    @ 08112dc4 0003
    lsrs r5,r0,#0xc    @ 08112dc6 050b
    ldrh r3,[r2,#0x6]                        @ 08112dc8 d388
    lsls r0,r3,#0x11    @ 08112dca 5804
    lsrs r3,r0,#0x15    @ 08112dcc 430d
    ldrb r2,[r2,#0x7]                        @ 08112dce d279
    lsrs r0,r2,#0x7    @ 08112dd0 d009
    str r0,[r6,#0x4]                         @ 08112dd2 7060
    cmp r3,#0x0                              @ 08112dd4 002b
    bne LAB_08112e24                         @ 08112dd6 25d1
    orrs r1,r5    @ 08112dd8 2943
    cmp r1,#0x0                              @ 08112dda 0029
    bne LAB_08112de4                         @ 08112ddc 02d1
    movs r0,#0x2    @ 08112dde 0220
    str r0,[r6,#0x0]                         @ 08112de0 3060
    b LAB_08112e78                           @ 08112de2 49e0
LAB_08112de4:
    ldr r0, DAT_08112e1c                     @ 08112de4 0d48
    str r0,[r6,#0x8]                         @ 08112de6 b060
    lsrs r3,r4,#0x18    @ 08112de8 230e
    lsls r2,r5,#0x8    @ 08112dea 2a02
    adds r1,r3,#0x0    @ 08112dec 191c
    orrs r1,r2    @ 08112dee 1143
    lsls r0,r4,#0x8    @ 08112df0 2002
    adds r5,r1,#0x0    @ 08112df2 0d1c
    adds r4,r0,#0x0    @ 08112df4 041c
    movs r0,#0x3    @ 08112df6 0320
    str r0,[r6,#0x0]                         @ 08112df8 3060
    ldr r0, DAT_08112e20                     @ 08112dfa 0948
    cmp r5,r0                                @ 08112dfc 8542
    bhi LAB_08112e54                         @ 08112dfe 29d8
    adds r7,r0,#0x0    @ 08112e00 071c
LAB_08112e02:
    lsrs r3,r4,#0x1f    @ 08112e02 e30f
    lsls r2,r5,#0x1    @ 08112e04 6a00
    adds r1,r3,#0x0    @ 08112e06 191c
    orrs r1,r2    @ 08112e08 1143
    lsls r0,r4,#0x1    @ 08112e0a 6000
    adds r5,r1,#0x0    @ 08112e0c 0d1c
    adds r4,r0,#0x0    @ 08112e0e 041c
    ldr r0,[r6,#0x8]                         @ 08112e10 b068
    subs r0,#0x1    @ 08112e12 0138
    str r0,[r6,#0x8]                         @ 08112e14 b060
    cmp r5,r7                                @ 08112e16 bd42
    bls LAB_08112e02                         @ 08112e18 f3d9
    b LAB_08112e54                           @ 08112e1a 1be0
DAT_08112e1c:
    .word  0xfffffc02                     @ 08112e1c 02fcffff
DAT_08112e20:
    .word  0x0fffffff                     @ 08112e20 ffffff0f
LAB_08112e24:
    ldr r0, DAT_08112e38                     @ 08112e24 0448
    cmp r3,r0                                @ 08112e26 8342
    bne LAB_08112e5a                         @ 08112e28 17d1
    orrs r1,r5    @ 08112e2a 2943
    cmp r1,#0x0                              @ 08112e2c 0029
    bne LAB_08112e3c                         @ 08112e2e 05d1
    movs r0,#0x4    @ 08112e30 0420
    str r0,[r6,#0x0]                         @ 08112e32 3060
    b LAB_08112e78                           @ 08112e34 20e0
    .zero  0x2
DAT_08112e38:
    .word  0x000007ff                     @ 08112e38 ff070000
LAB_08112e3c:
    movs r2,#0x80    @ 08112e3c 8022
    lsls r2,r2,#0xc    @ 08112e3e 1203
    movs r0,#0x0    @ 08112e40 0020
    adds r1,r5,#0x0    @ 08112e42 291c
    ands r1,r2    @ 08112e44 1140
    orrs r1,r0    @ 08112e46 0143
    cmp r1,#0x0                              @ 08112e48 0029
    beq LAB_08112e52                         @ 08112e4a 02d0
    movs r0,#0x1    @ 08112e4c 0120
    str r0,[r6,#0x0]                         @ 08112e4e 3060
    b LAB_08112e54                           @ 08112e50 00e0
LAB_08112e52:
    str r1,[r6,#0x0]                         @ 08112e52 3160
LAB_08112e54:
    str r4,[r6,#0xc]                         @ 08112e54 f460
    str r5,[r6,#0x10]                        @ 08112e56 3561
    b LAB_08112e78                           @ 08112e58 0ee0
LAB_08112e5a:
    ldr r1, DAT_08112e7c                     @ 08112e5a 0849
    adds r0,r3,r1    @ 08112e5c 5818
    str r0,[r6,#0x8]                         @ 08112e5e b060
    movs r0,#0x3    @ 08112e60 0320
    str r0,[r6,#0x0]                         @ 08112e62 3060
    lsrs r3,r4,#0x18    @ 08112e64 230e
    lsls r2,r5,#0x8    @ 08112e66 2a02
    adds r1,r3,#0x0    @ 08112e68 191c
    orrs r1,r2    @ 08112e6a 1143
    lsls r0,r4,#0x8    @ 08112e6c 2002
    ldr r2, DAT_08112e80                     @ 08112e6e 044a
    ldr r3, DAT_08112e84                     @ 08112e70 044b
    orrs r1,r3    @ 08112e72 1943
    str r0,[r6,#0xc]                         @ 08112e74 f060
    str r1,[r6,#0x10]                        @ 08112e76 3161
LAB_08112e78:
    add sp,#0x8                              @ 08112e78 02b0
    pop {r4,r5,r6,r7,pc}                     @ 08112e7a f0bd
DAT_08112e7c:
    .word  0xfffffc01                     @ 08112e7c 01fcffff
DAT_08112e80:
    .word  0x00000000                     @ 08112e80 00000000
DAT_08112e84:
    .word  0x10000000                     @ 08112e84 00000010

@ newlib/libgcc double-precision floating-point add/subtract core: receives two unpacked double component structs (r0=operand A ptr, r1=operand B ptr, r2=result ptr), performs NaN/Inf/zero propagation checks, aligns mantissas by exponent difference (max 0x3f shift), executes 64-bit signed add/sub with carry and normalization, writes result components.
@ Called by __adddf3 (0x081130f4) and __subdf3 (0x08113124); both share this core after unpacking.
@ Exit LAB_081130e4 -> pop returns to caller.
@ 
@ Constants:
@ - MAX_EXP_DIFF=0x3f (exponent difference threshold; operand with smaller exponent is zeroed if exceeded)
@ - EXP_BOUND=0x0fffffff (exponent overflow detection upper limit)
exec_addsubdf3_core:
    push {r4,r5,r6,r7,lr}                    @ 08112e88 f0b5
    .hword 0x4657    @ 08112e8a 5746
    .hword 0x464e    @ 08112e8c 4e46
    .hword 0x4645    @ 08112e8e 4546
    push {r5,r6,r7}                          @ 08112e90 e0b4
    sub sp,#0xc                              @ 08112e92 83b0
    adds r3,r0,#0x0    @ 08112e94 031c
    adds r4,r1,#0x0    @ 08112e96 0c1c
    .hword 0x4692    @ 08112e98 9246
    movs r0,#0x0    @ 08112e9a 0020
    ldr r2,[r3,#0x0]                         @ 08112e9c 1a68
    cmp r2,#0x1                              @ 08112e9e 012a
    bhi LAB_08112ea4                         @ 08112ea0 00d8
    movs r0,#0x1    @ 08112ea2 0120
LAB_08112ea4:
    cmp r0,#0x0                              @ 08112ea4 0028
    beq LAB_08112eac                         @ 08112ea6 01d0
LAB_08112ea8:
    adds r0,r3,#0x0    @ 08112ea8 181c
    b LAB_081130e4                           @ 08112eaa 1be1
LAB_08112eac:
    movs r1,#0x0    @ 08112eac 0021
    ldr r0,[r4,#0x0]                         @ 08112eae 2068
    cmp r0,#0x1                              @ 08112eb0 0128
    bhi LAB_08112eb6                         @ 08112eb2 00d8
    movs r1,#0x1    @ 08112eb4 0121
LAB_08112eb6:
    cmp r1,#0x0                              @ 08112eb6 0029
    bne LAB_08112f2e                         @ 08112eb8 39d1
    movs r1,#0x0    @ 08112eba 0021
    cmp r2,#0x4                              @ 08112ebc 042a
    bne LAB_08112ec2                         @ 08112ebe 00d1
    movs r1,#0x1    @ 08112ec0 0121
LAB_08112ec2:
    cmp r1,#0x0                              @ 08112ec2 0029
    beq LAB_08112ee4                         @ 08112ec4 0ed0
    movs r1,#0x0    @ 08112ec6 0021
    cmp r0,#0x4                              @ 08112ec8 0428
    bne LAB_08112ece                         @ 08112eca 00d1
    movs r1,#0x1    @ 08112ecc 0121
LAB_08112ece:
    cmp r1,#0x0                              @ 08112ece 0029
    beq LAB_08112ea8                         @ 08112ed0 ead0
    ldr r1,[r3,#0x4]                         @ 08112ed2 5968
    ldr r0,[r4,#0x4]                         @ 08112ed4 6068
    cmp r1,r0                                @ 08112ed6 8142
    beq LAB_08112ea8                         @ 08112ed8 e6d0
    ldr r0, DAT_08112ee0                     @ 08112eda 0148
    b LAB_081130e4                           @ 08112edc 02e1
    .zero  0x2
DAT_08112ee0:
    .word  0x03005828                     @ 08112ee0 28580003
LAB_08112ee4:
    movs r1,#0x0    @ 08112ee4 0021
    cmp r0,#0x4                              @ 08112ee6 0428
    bne LAB_08112eec                         @ 08112ee8 00d1
    movs r1,#0x1    @ 08112eea 0121
LAB_08112eec:
    cmp r1,#0x0                              @ 08112eec 0029
    bne LAB_08112f2e                         @ 08112eee 1ed1
    movs r1,#0x0    @ 08112ef0 0021
    cmp r0,#0x2                              @ 08112ef2 0228
    bne LAB_08112ef8                         @ 08112ef4 00d1
    movs r1,#0x1    @ 08112ef6 0121
LAB_08112ef8:
    cmp r1,#0x0                              @ 08112ef8 0029
    beq LAB_08112f20                         @ 08112efa 11d0
    movs r0,#0x0    @ 08112efc 0020
    cmp r2,#0x2                              @ 08112efe 022a
    bne LAB_08112f04                         @ 08112f00 00d1
    movs r0,#0x1    @ 08112f02 0120
LAB_08112f04:
    cmp r0,#0x0                              @ 08112f04 0028
    beq LAB_08112ea8                         @ 08112f06 cfd0
    .hword 0x4651    @ 08112f08 5146
    adds r0,r3,#0x0    @ 08112f0a 181c
    ldmia r0!,{r2,r5,r6}                     @ 08112f0c 64c8
    stmia r1!,{r2,r5,r6}                     @ 08112f0e 64c1
    ldmia r0!,{r2,r5}                        @ 08112f10 24c8
    stmia r1!,{r2,r5}                        @ 08112f12 24c1
    ldr r0,[r3,#0x4]                         @ 08112f14 5868
    ldr r1,[r4,#0x4]                         @ 08112f16 6168
    ands r0,r1    @ 08112f18 0840
    .hword 0x4656    @ 08112f1a 5646
    str r0,[r6,#0x4]                         @ 08112f1c 7060
    b LAB_081130e2                           @ 08112f1e e0e0
LAB_08112f20:
    movs r1,#0x0    @ 08112f20 0021
    ldr r0,[r3,#0x0]                         @ 08112f22 1868
    cmp r0,#0x2                              @ 08112f24 0228
    bne LAB_08112f2a                         @ 08112f26 00d1
    movs r1,#0x1    @ 08112f28 0121
LAB_08112f2a:
    cmp r1,#0x0                              @ 08112f2a 0029
    beq LAB_08112f32                         @ 08112f2c 01d0
LAB_08112f2e:
    adds r0,r4,#0x0    @ 08112f2e 201c
    b LAB_081130e4                           @ 08112f30 d8e0
LAB_08112f32:
    ldr r0,[r3,#0x8]                         @ 08112f32 9868
    .hword 0x4681    @ 08112f34 8146
    ldr r1,[r4,#0x8]                         @ 08112f36 a168
    .hword 0x4688    @ 08112f38 8846
    ldr r6,[r3,#0xc]                         @ 08112f3a de68
    ldr r7,[r3,#0x10]                        @ 08112f3c 1f69
    ldr r0,[r4,#0xc]                         @ 08112f3e e068
    ldr r1,[r4,#0x10]                        @ 08112f40 2169
    str r0,[sp,#0x0]                         @ 08112f42 0090
    str r1,[sp,#0x4]                         @ 08112f44 0191
    .hword 0x4649    @ 08112f46 4946
    .hword 0x4642    @ 08112f48 4246
    subs r0,r1,r2    @ 08112f4a 881a
    cmp r0,#0x0                              @ 08112f4c 0028
    bge LAB_08112f52                         @ 08112f4e 00da
    rsbs r0,r0,#0    @ 08112f50 4042
LAB_08112f52:
    cmp r0,#0x3f                             @ 08112f52 3f28
    bgt LAB_08112fd0                         @ 08112f54 3cdc
    ldr r3,[r3,#0x4]                         @ 08112f56 5b68
    .hword 0x469c    @ 08112f58 9c46
    ldr r4,[r4,#0x4]                         @ 08112f5a 6468
    str r4,[sp,#0x8]                         @ 08112f5c 0294
    cmp r9,r8                                @ 08112f5e c145
    ble LAB_08112f9c                         @ 08112f60 1cdd
    .hword 0x464b    @ 08112f62 4b46
    .hword 0x4644    @ 08112f64 4446
    subs r3,r3,r4    @ 08112f66 1b1b
    .hword 0x4698    @ 08112f68 9846
LAB_08112f6a:
    movs r5,#0x1    @ 08112f6a 0125
    rsbs r5,r5,#0    @ 08112f6c 6d42
    add r8,r5                                @ 08112f6e a844
    ldr r2,[sp,#0x0]                         @ 08112f70 009a
    movs r0,#0x1    @ 08112f72 0120
    ands r2,r0    @ 08112f74 0240
    movs r3,#0x0    @ 08112f76 0023
    ldr r1,[sp,#0x4]                         @ 08112f78 0199
    lsls r5,r1,#0x1f    @ 08112f7a cd07
    ldr r0,[sp,#0x0]                         @ 08112f7c 0098
    lsrs r4,r0,#0x1    @ 08112f7e 4408
    adds r0,r5,#0x0    @ 08112f80 281c
    orrs r0,r4    @ 08112f82 2043
    adds r4,r1,#0x0    @ 08112f84 0c1c
    lsrs r1,r4,#0x1    @ 08112f86 6108
    adds r5,r2,#0x0    @ 08112f88 151c
    orrs r5,r0    @ 08112f8a 0543
    str r5,[sp,#0x0]                         @ 08112f8c 0095
    adds r4,r3,#0x0    @ 08112f8e 1c1c
    orrs r4,r1    @ 08112f90 0c43
    str r4,[sp,#0x4]                         @ 08112f92 0194
    .hword 0x4645    @ 08112f94 4546
    cmp r5,#0x0                              @ 08112f96 002d
    bne LAB_08112f6a                         @ 08112f98 e7d1
    .hword 0x46c8    @ 08112f9a c846
LAB_08112f9c:
    cmp r8,r9                                @ 08112f9c c845
    ble LAB_08112fec                         @ 08112f9e 25dd
    .hword 0x4640    @ 08112fa0 4046
    .hword 0x4649    @ 08112fa2 4946
    subs r0,r0,r1    @ 08112fa4 401a
    .hword 0x4681    @ 08112fa6 8146
LAB_08112fa8:
    movs r2,#0x1    @ 08112fa8 0122
    rsbs r2,r2,#0    @ 08112faa 5242
    add r9,r2                                @ 08112fac 9144
    movs r2,#0x1    @ 08112fae 0122
    ands r2,r6    @ 08112fb0 3240
    movs r3,#0x0    @ 08112fb2 0023
    lsls r5,r7,#0x1f    @ 08112fb4 fd07
    lsrs r4,r6,#0x1    @ 08112fb6 7408
    adds r0,r5,#0x0    @ 08112fb8 281c
    orrs r0,r4    @ 08112fba 2043
    lsrs r1,r7,#0x1    @ 08112fbc 7908
    adds r6,r2,#0x0    @ 08112fbe 161c
    orrs r6,r0    @ 08112fc0 0643
    adds r7,r3,#0x0    @ 08112fc2 1f1c
    orrs r7,r1    @ 08112fc4 0f43
    .hword 0x464b    @ 08112fc6 4b46
    cmp r3,#0x0                              @ 08112fc8 002b
    bne LAB_08112fa8                         @ 08112fca edd1
    .hword 0x46c1    @ 08112fcc c146
    b LAB_08112fec                           @ 08112fce 0de0
LAB_08112fd0:
    cmp r9,r8                                @ 08112fd0 c145
    ble LAB_08112fde                         @ 08112fd2 04dd
    movs r0,#0x0    @ 08112fd4 0020
    movs r1,#0x0    @ 08112fd6 0021
    str r0,[sp,#0x0]                         @ 08112fd8 0090
    str r1,[sp,#0x4]                         @ 08112fda 0191
    b LAB_08112fe4                           @ 08112fdc 02e0
LAB_08112fde:
    .hword 0x46c1    @ 08112fde c146
    movs r6,#0x0    @ 08112fe0 0026
    movs r7,#0x0    @ 08112fe2 0027
LAB_08112fe4:
    ldr r3,[r3,#0x4]                         @ 08112fe4 5b68
    .hword 0x469c    @ 08112fe6 9c46
    ldr r4,[r4,#0x4]                         @ 08112fe8 6468
    str r4,[sp,#0x8]                         @ 08112fea 0294
LAB_08112fec:
    ldr r1,[sp,#0x8]                         @ 08112fec 0299
    cmp r12,r1                               @ 08112fee 8c45
    beq LAB_08113094                         @ 08112ff0 50d0
    .hword 0x4662    @ 08112ff2 6246
    cmp r2,#0x0                              @ 08112ff4 002a
    beq LAB_0811300e                         @ 08112ff6 0ad0
    adds r1,r7,#0x0    @ 08112ff8 391c
    adds r0,r6,#0x0    @ 08112ffa 301c
    bl __negdi2                              @ 08112ffc 01f0c2f9
    adds r3,r1,#0x0    @ 08113000 0b1c
    adds r2,r0,#0x0    @ 08113002 021c
    ldr r4,[sp,#0x0]                         @ 08113004 009c
    ldr r5,[sp,#0x4]                         @ 08113006 019d
    adds r2,r2,r4    @ 08113008 1219
    adcs r3,r5    @ 0811300a 6b41
    b LAB_0811301a                           @ 0811300c 05e0
LAB_0811300e:
    adds r3,r7,#0x0    @ 0811300e 3b1c
    adds r2,r6,#0x0    @ 08113010 321c
    ldr r0,[sp,#0x0]                         @ 08113012 0098
    ldr r1,[sp,#0x4]                         @ 08113014 0199
    subs r2,r2,r0    @ 08113016 121a
    sbcs r3,r1    @ 08113018 8b41
LAB_0811301a:
    cmp r3,#0x0                              @ 0811301a 002b
    blt LAB_08113030                         @ 0811301c 08db
    movs r0,#0x0    @ 0811301e 0020
    .hword 0x4651    @ 08113020 5146
    str r0,[r1,#0x4]                         @ 08113022 4860
    .hword 0x464c    @ 08113024 4c46
    str r4,[r1,#0x8]                         @ 08113026 8c60
    .hword 0x4655    @ 08113028 5546
    str r2,[r5,#0xc]                         @ 0811302a ea60
    str r3,[r5,#0x10]                        @ 0811302c 2b61
    b LAB_08113048                           @ 0811302e 0be0
LAB_08113030:
    movs r0,#0x1    @ 08113030 0120
    .hword 0x4656    @ 08113032 5646
    str r0,[r6,#0x4]                         @ 08113034 7060
    .hword 0x4648    @ 08113036 4846
    str r0,[r6,#0x8]                         @ 08113038 b060
    adds r1,r3,#0x0    @ 0811303a 191c
    adds r0,r2,#0x0    @ 0811303c 101c
    bl __negdi2                              @ 0811303e 01f0a1f9
    .hword 0x4652    @ 08113042 5246
    str r0,[r2,#0xc]                         @ 08113044 d060
    str r1,[r2,#0x10]                        @ 08113046 1161
LAB_08113048:
    .hword 0x4654    @ 08113048 5446
    ldr r2,[r4,#0xc]                         @ 0811304a e268
    ldr r3,[r4,#0x10]                        @ 0811304c 2369
    movs r0,#0x1    @ 0811304e 0120
    rsbs r0,r0,#0    @ 08113050 4042
    asrs r1,r0,#0x1f    @ 08113052 c117
LAB_08113054:
    adds r2,r2,r0    @ 08113054 1218
    adcs r3,r1    @ 08113056 4b41
    ldr r0, DAT_08113090                     @ 08113058 0d48
    cmp r3,r0                                @ 0811305a 8342
    bhi LAB_081130ac                         @ 0811305c 26d8
    cmp r3,r0                                @ 0811305e 8342
    bne LAB_0811306a                         @ 08113060 03d1
    movs r0,#0x2    @ 08113062 0220
    rsbs r0,r0,#0    @ 08113064 4042
    cmp r2,r0                                @ 08113066 8242
    bhi LAB_081130ac                         @ 08113068 20d8
LAB_0811306a:
    .hword 0x4655    @ 0811306a 5546
    ldr r0,[r5,#0xc]                         @ 0811306c e868
    ldr r1,[r5,#0x10]                        @ 0811306e 2969
    lsrs r3,r0,#0x1f    @ 08113070 c30f
    lsls r2,r1,#0x1    @ 08113072 4a00
    adds r1,r3,#0x0    @ 08113074 191c
    orrs r1,r2    @ 08113076 1143
    lsls r0,r0,#0x1    @ 08113078 4000
    .hword 0x4656    @ 0811307a 5646
    str r0,[r6,#0xc]                         @ 0811307c f060
    str r1,[r6,#0x10]                        @ 0811307e 3161
    ldr r2,[r6,#0x8]                         @ 08113080 b268
    subs r2,#0x1    @ 08113082 013a
    str r2,[r6,#0x8]                         @ 08113084 b260
    movs r2,#0x1    @ 08113086 0122
    rsbs r2,r2,#0    @ 08113088 5242
    asrs r3,r2,#0x1f    @ 0811308a d317
    b LAB_08113054                           @ 0811308c e2e7
    .zero  0x2
DAT_08113090:
    .word  0x0fffffff                     @ 08113090 ffffff0f
LAB_08113094:
    .hword 0x4660    @ 08113094 6046
    .hword 0x4651    @ 08113096 5146
    str r0,[r1,#0x4]                         @ 08113098 4860
    .hword 0x464a    @ 0811309a 4a46
    str r2,[r1,#0x8]                         @ 0811309c 8a60
    ldr r3,[sp,#0x0]                         @ 0811309e 009b
    ldr r4,[sp,#0x4]                         @ 081130a0 019c
    adds r6,r6,r3    @ 081130a2 f618
    adcs r7,r4    @ 081130a4 6741
    .hword 0x4654    @ 081130a6 5446
    str r6,[r4,#0xc]                         @ 081130a8 e660
    str r7,[r4,#0x10]                        @ 081130aa 2761
LAB_081130ac:
    movs r0,#0x3    @ 081130ac 0320
    .hword 0x4655    @ 081130ae 5546
    str r0,[r5,#0x0]                         @ 081130b0 2860
    ldr r1,[r5,#0x10]                        @ 081130b2 2969
    ldr r0, DAT_081130f0                     @ 081130b4 0e48
    cmp r1,r0                                @ 081130b6 8142
    bls LAB_081130e2                         @ 081130b8 13d9
    ldr r4,[r5,#0xc]                         @ 081130ba ec68
    ldr r5,[r5,#0x10]                        @ 081130bc 2d69
    movs r2,#0x1    @ 081130be 0122
    adds r0,r4,#0x0    @ 081130c0 201c
    ands r0,r2    @ 081130c2 1040
    movs r1,#0x0    @ 081130c4 0021
    lsls r6,r5,#0x1f    @ 081130c6 ee07
    .hword 0x46b0    @ 081130c8 b046
    lsrs r6,r4,#0x1    @ 081130ca 6608
    .hword 0x4642    @ 081130cc 4246
    orrs r2,r6    @ 081130ce 3243
    lsrs r3,r5,#0x1    @ 081130d0 6b08
    orrs r0,r2    @ 081130d2 1043
    orrs r1,r3    @ 081130d4 1943
    .hword 0x4652    @ 081130d6 5246
    str r0,[r2,#0xc]                         @ 081130d8 d060
    str r1,[r2,#0x10]                        @ 081130da 1161
    ldr r0,[r2,#0x8]                         @ 081130dc 9068
    adds r0,#0x1    @ 081130de 0130
    str r0,[r2,#0x8]                         @ 081130e0 9060
LAB_081130e2:
    .hword 0x4650    @ 081130e2 5046
LAB_081130e4:
    add sp,#0xc                              @ 081130e4 03b0
    pop {r3,r4,r5}                           @ 081130e6 38bc
    .hword 0x4698    @ 081130e8 9846
    .hword 0x46a1    @ 081130ea a146
    .hword 0x46aa    @ 081130ec aa46
    pop {r4,r5,r6,r7,pc}                     @ 081130ee f0bd
DAT_081130f0:
    .word  0x1fffffff                     @ 081130f0 ffffff1f
__adddf3:
    push {r4,lr}                             @ 081130f4 10b5
    sub sp,#0x4c                             @ 081130f6 93b0
    str r0,[sp,#0x3c]                        @ 081130f8 0f90
    str r1,[sp,#0x40]                        @ 081130fa 1091
    str r2,[sp,#0x44]                        @ 081130fc 1192
    str r3,[sp,#0x48]                        @ 081130fe 1293
    add r0,sp,#0x3c                          @ 08113100 0fa8
    .hword 0x4669    @ 08113102 6946
    bl __unpack_d                            @ 08113104 fff754fe
    add r0,sp,#0x44                          @ 08113108 11a8
    add r4,sp,#0x14                          @ 0811310a 05ac
    adds r1,r4,#0x0    @ 0811310c 211c
    bl __unpack_d                            @ 0811310e fff74ffe
    add r2,sp,#0x28                          @ 08113112 0aaa
    .hword 0x4668    @ 08113114 6846
    adds r1,r4,#0x0    @ 08113116 211c
    bl exec_addsubdf3_core                   @ 08113118 fff7b6fe
    bl __pack_d                              @ 0811311c fff7a4fd
    add sp,#0x4c                             @ 08113120 13b0
    pop {r4,pc}                              @ 08113122 10bd
__subdf3:
    push {r4,lr}                             @ 08113124 10b5
    sub sp,#0x4c                             @ 08113126 93b0
    str r0,[sp,#0x3c]                        @ 08113128 0f90
    str r1,[sp,#0x40]                        @ 0811312a 1091
    str r2,[sp,#0x44]                        @ 0811312c 1192
    str r3,[sp,#0x48]                        @ 0811312e 1293
    add r0,sp,#0x3c                          @ 08113130 0fa8
    .hword 0x4669    @ 08113132 6946
    bl __unpack_d                            @ 08113134 fff73cfe
    add r0,sp,#0x44                          @ 08113138 11a8
    add r4,sp,#0x14                          @ 0811313a 05ac
    adds r1,r4,#0x0    @ 0811313c 211c
    bl __unpack_d                            @ 0811313e fff737fe
    ldr r0,[r4,#0x4]                         @ 08113142 6068
    movs r1,#0x1    @ 08113144 0121
    eors r0,r1    @ 08113146 4840
    str r0,[r4,#0x4]                         @ 08113148 6060
    add r2,sp,#0x28                          @ 0811314a 0aaa
    .hword 0x4668    @ 0811314c 6846
    adds r1,r4,#0x0    @ 0811314e 211c
    bl exec_addsubdf3_core                   @ 08113150 fff79afe
    bl __pack_d                              @ 08113154 fff788fd
    add sp,#0x4c                             @ 08113158 13b0
    pop {r4,pc}                              @ 0811315a 10bd
__muldf3:
    push {r4,r5,r6,r7,lr}                    @ 0811315c f0b5
    .hword 0x4657    @ 0811315e 5746
    .hword 0x464e    @ 08113160 4e46
    .hword 0x4645    @ 08113162 4546
    push {r5,r6,r7}                          @ 08113164 e0b4
    sub sp,#0x74                             @ 08113166 9db0
    str r0,[sp,#0x3c]                        @ 08113168 0f90
    str r1,[sp,#0x40]                        @ 0811316a 1091
    str r2,[sp,#0x44]                        @ 0811316c 1192
    str r3,[sp,#0x48]                        @ 0811316e 1293
    add r0,sp,#0x3c                          @ 08113170 0fa8
    .hword 0x4669    @ 08113172 6946
    bl __unpack_d                            @ 08113174 fff71cfe
    add r0,sp,#0x44                          @ 08113178 11a8
    add r4,sp,#0x14                          @ 0811317a 05ac
    adds r1,r4,#0x0    @ 0811317c 211c
    bl __unpack_d                            @ 0811317e fff717fe
    .hword 0x46e8    @ 08113182 e846
    add r0,sp,#0x28                          @ 08113184 0aa8
    .hword 0x4682    @ 08113186 8246
    movs r0,#0x0    @ 08113188 0020
    ldr r1,[sp,#0x0]                         @ 0811318a 0099
    cmp r1,#0x1                              @ 0811318c 0129
    bhi LAB_08113192                         @ 0811318e 00d8
    movs r0,#0x1    @ 08113190 0120
LAB_08113192:
    cmp r0,#0x0                              @ 08113192 0028
    bne LAB_081131f6                         @ 08113194 2fd1
    movs r2,#0x0    @ 08113196 0022
    ldr r0,[sp,#0x14]                        @ 08113198 0598
    cmp r0,#0x1                              @ 0811319a 0128
    bhi LAB_081131a0                         @ 0811319c 00d8
    movs r2,#0x1    @ 0811319e 0122
LAB_081131a0:
    cmp r2,#0x0                              @ 081131a0 002a
    beq LAB_081131a8                         @ 081131a2 01d0
    ldr r0,[sp,#0x4]                         @ 081131a4 0198
    b LAB_08113218                           @ 081131a6 37e0
LAB_081131a8:
    movs r2,#0x0    @ 081131a8 0022
    cmp r1,#0x4                              @ 081131aa 0429
    bne LAB_081131b0                         @ 081131ac 00d1
    movs r2,#0x1    @ 081131ae 0122
LAB_081131b0:
    cmp r2,#0x0                              @ 081131b0 002a
    beq LAB_081131c2                         @ 081131b2 06d0
    movs r1,#0x0    @ 081131b4 0021
    cmp r0,#0x2                              @ 081131b6 0228
    bne LAB_081131bc                         @ 081131b8 00d1
    movs r1,#0x1    @ 081131ba 0121
LAB_081131bc:
    cmp r1,#0x0                              @ 081131bc 0029
    bne LAB_081131da                         @ 081131be 0cd1
    b LAB_081131f6                           @ 081131c0 19e0
LAB_081131c2:
    movs r2,#0x0    @ 081131c2 0022
    cmp r0,#0x4                              @ 081131c4 0428
    bne LAB_081131ca                         @ 081131c6 00d1
    movs r2,#0x1    @ 081131c8 0122
LAB_081131ca:
    cmp r2,#0x0                              @ 081131ca 002a
    beq LAB_081131ea                         @ 081131cc 0dd0
    movs r0,#0x0    @ 081131ce 0020
    cmp r1,#0x2                              @ 081131d0 0229
    bne LAB_081131d6                         @ 081131d2 00d1
    movs r0,#0x1    @ 081131d4 0120
LAB_081131d6:
    cmp r0,#0x0                              @ 081131d6 0028
    beq LAB_081131e4                         @ 081131d8 04d0
LAB_081131da:
    ldr r0, DAT_081131e0                     @ 081131da 0148
    b LAB_081133e2                           @ 081131dc 01e1
    .zero  0x2
DAT_081131e0:
    .word  0x03005828                     @ 081131e0 28580003
LAB_081131e4:
    .hword 0x4641    @ 081131e4 4146
    ldr r0,[r1,#0x4]                         @ 081131e6 4868
    b LAB_08113218                           @ 081131e8 16e0
LAB_081131ea:
    movs r2,#0x0    @ 081131ea 0022
    cmp r1,#0x2                              @ 081131ec 0229
    bne LAB_081131f2                         @ 081131ee 00d1
    movs r2,#0x1    @ 081131f0 0122
LAB_081131f2:
    cmp r2,#0x0                              @ 081131f2 002a
    beq LAB_08113208                         @ 081131f4 08d0
LAB_081131f6:
    ldr r0,[sp,#0x4]                         @ 081131f6 0198
    ldr r1,[sp,#0x18]                        @ 081131f8 0699
    eors r0,r1    @ 081131fa 4840
    rsbs r1,r0,#0    @ 081131fc 4142
    orrs r1,r0    @ 081131fe 0143
    lsrs r1,r1,#0x1f    @ 08113200 c90f
    str r1,[sp,#0x4]                         @ 08113202 0191
    .hword 0x4668    @ 08113204 6846
    b LAB_081133e2                           @ 08113206 ece0
LAB_08113208:
    movs r1,#0x0    @ 08113208 0021
    cmp r0,#0x2                              @ 0811320a 0228
    bne LAB_08113210                         @ 0811320c 00d1
    movs r1,#0x1    @ 0811320e 0121
LAB_08113210:
    cmp r1,#0x0                              @ 08113210 0029
    beq LAB_08113228                         @ 08113212 09d0
    .hword 0x4642    @ 08113214 4246
    ldr r0,[r2,#0x4]                         @ 08113216 5068
LAB_08113218:
    ldr r1,[sp,#0x18]                        @ 08113218 0699
    eors r0,r1    @ 0811321a 4840
    rsbs r1,r0,#0    @ 0811321c 4142
    orrs r1,r0    @ 0811321e 0143
    lsrs r1,r1,#0x1f    @ 08113220 c90f
    str r1,[sp,#0x18]                        @ 08113222 0691
    adds r0,r4,#0x0    @ 08113224 201c
    b LAB_081133e2                           @ 08113226 dce0
LAB_08113228:
    .hword 0x4644    @ 08113228 4446
    ldr r0,[r4,#0xc]                         @ 0811322a e068
    ldr r1,[r4,#0x10]                        @ 0811322c 2169
    adds r6,r0,#0x0    @ 0811322e 061c
    movs r7,#0x0    @ 08113230 0027
    str r1,[sp,#0x4c]                        @ 08113232 1391
    movs r5,#0x0    @ 08113234 0025
    str r5,[sp,#0x50]                        @ 08113236 1495
    ldr r0,[sp,#0x20]                        @ 08113238 0898
    ldr r1,[sp,#0x24]                        @ 0811323a 0999
    adds r4,r0,#0x0    @ 0811323c 041c
    str r1,[sp,#0x54]                        @ 0811323e 1591
    movs r0,#0x0    @ 08113240 0020
    str r0,[sp,#0x58]                        @ 08113242 1690
    adds r1,r5,#0x0    @ 08113244 291c
    adds r0,r4,#0x0    @ 08113246 201c
    adds r3,r7,#0x0    @ 08113248 3b1c
    adds r2,r6,#0x0    @ 0811324a 321c
    bl __muldi3                              @ 0811324c fbf78efa
    str r0,[sp,#0x5c]                        @ 08113250 1790
    str r1,[sp,#0x60]                        @ 08113252 1891
    ldr r0,[sp,#0x54]                        @ 08113254 1598
    ldr r1,[sp,#0x58]                        @ 08113256 1699
    adds r3,r7,#0x0    @ 08113258 3b1c
    adds r2,r6,#0x0    @ 0811325a 321c
    bl __muldi3                              @ 0811325c fbf786fa
    adds r7,r1,#0x0    @ 08113260 0f1c
    adds r6,r0,#0x0    @ 08113262 061c
    adds r1,r5,#0x0    @ 08113264 291c
    adds r0,r4,#0x0    @ 08113266 201c
    ldr r2,[sp,#0x4c]                        @ 08113268 139a
    ldr r3,[sp,#0x50]                        @ 0811326a 149b
    bl __muldi3                              @ 0811326c fbf77efa
    adds r5,r1,#0x0    @ 08113270 0d1c
    adds r4,r0,#0x0    @ 08113272 041c
    ldr r0,[sp,#0x54]                        @ 08113274 1598
    ldr r1,[sp,#0x58]                        @ 08113276 1699
    ldr r2,[sp,#0x4c]                        @ 08113278 139a
    ldr r3,[sp,#0x50]                        @ 0811327a 149b
    bl __muldi3                              @ 0811327c fbf776fa
    str r0,[sp,#0x64]                        @ 08113280 1990
    str r1,[sp,#0x68]                        @ 08113282 1a91
    movs r1,#0x0    @ 08113284 0021
    movs r2,#0x0    @ 08113286 0022
    str r1,[sp,#0x6c]                        @ 08113288 1b91
    str r2,[sp,#0x70]                        @ 0811328a 1c92
    adds r3,r7,#0x0    @ 0811328c 3b1c
    adds r2,r6,#0x0    @ 0811328e 321c
    adds r2,r2,r4    @ 08113290 1219
    adcs r3,r5    @ 08113292 6b41
    cmp r7,r3                                @ 08113294 9f42
    bhi LAB_081132a0                         @ 08113296 03d8
    cmp r7,r3                                @ 08113298 9f42
    bne LAB_081132a8                         @ 0811329a 05d1
    cmp r6,r2                                @ 0811329c 9642
    bls LAB_081132a8                         @ 0811329e 03d9
LAB_081132a0:
    ldr r5, DAT_081133f8                     @ 081132a0 554d
    ldr r4, DAT_081133f4                     @ 081132a2 544c
    str r4,[sp,#0x6c]                        @ 081132a4 1b94
    str r5,[sp,#0x70]                        @ 081132a6 1c95
LAB_081132a8:
    adds r1,r2,#0x0    @ 081132a8 111c
    movs r6,#0x0    @ 081132aa 0026
    adds r7,r1,#0x0    @ 081132ac 0f1c
    ldr r0,[sp,#0x5c]                        @ 081132ae 1798
    ldr r1,[sp,#0x60]                        @ 081132b0 1899
    adds r6,r6,r0    @ 081132b2 3618
    adcs r7,r1    @ 081132b4 4f41
    cmp r1,r7                                @ 081132b6 b942
    bhi LAB_081132c4                         @ 081132b8 04d8
    ldr r1,[sp,#0x60]                        @ 081132ba 1899
    cmp r1,r7                                @ 081132bc b942
    bne LAB_081132d4                         @ 081132be 09d1
    cmp r0,r6                                @ 081132c0 b042
    bls LAB_081132d4                         @ 081132c2 07d9
LAB_081132c4:
    movs r0,#0x1    @ 081132c4 0120
    movs r1,#0x0    @ 081132c6 0021
    ldr r4,[sp,#0x6c]                        @ 081132c8 1b9c
    ldr r5,[sp,#0x70]                        @ 081132ca 1c9d
    adds r4,r4,r0    @ 081132cc 2418
    adcs r5,r1    @ 081132ce 4d41
    str r4,[sp,#0x6c]                        @ 081132d0 1b94
    str r5,[sp,#0x70]                        @ 081132d2 1c95
LAB_081132d4:
    adds r0,r3,#0x0    @ 081132d4 181c
    adds r2,r0,#0x0    @ 081132d6 021c
    movs r3,#0x0    @ 081132d8 0023
    adds r5,r3,#0x0    @ 081132da 1d1c
    adds r4,r2,#0x0    @ 081132dc 141c
    ldr r0,[sp,#0x64]                        @ 081132de 1998
    ldr r1,[sp,#0x68]                        @ 081132e0 1a99
    adds r4,r4,r0    @ 081132e2 2418
    adcs r5,r1    @ 081132e4 4d41
    ldr r1,[sp,#0x6c]                        @ 081132e6 1b99
    ldr r2,[sp,#0x70]                        @ 081132e8 1c9a
    adds r4,r4,r1    @ 081132ea 6418
    adcs r5,r2    @ 081132ec 5541
    .hword 0x4640    @ 081132ee 4046
    ldr r2,[r0,#0x8]                         @ 081132f0 8268
    ldr r0,[sp,#0x1c]                        @ 081132f2 0798
    adds r2,r2,r0    @ 081132f4 1218
    str r2,[sp,#0x30]                        @ 081132f6 0c92
    .hword 0x4640    @ 081132f8 4046
    ldr r1,[r0,#0x4]                         @ 081132fa 4168
    ldr r0,[sp,#0x18]                        @ 081132fc 0698
    eors r1,r0    @ 081132fe 4140
    rsbs r0,r1,#0    @ 08113300 4842
    orrs r0,r1    @ 08113302 0843
    lsrs r0,r0,#0x1f    @ 08113304 c00f
    str r0,[sp,#0x2c]                        @ 08113306 0b90
    adds r2,#0x4    @ 08113308 0432
    str r2,[sp,#0x30]                        @ 0811330a 0c92
    ldr r0, DAT_081133fc                     @ 0811330c 3b48
    cmp r5,r0                                @ 0811330e 8542
    bls LAB_08113356                         @ 08113310 21d9
    movs r1,#0x1    @ 08113312 0121
    .hword 0x4689    @ 08113314 8946
    .hword 0x4680    @ 08113316 8046
    .hword 0x4694    @ 08113318 9446
LAB_0811331a:
    movs r2,#0x1    @ 0811331a 0122
    add r12,r2                               @ 0811331c 9444
    .hword 0x4648    @ 0811331e 4846
    ands r0,r4    @ 08113320 2040
    cmp r0,#0x0                              @ 08113322 0028
    beq LAB_08113340                         @ 08113324 0cd0
    lsls r3,r7,#0x1f    @ 08113326 fb07
    lsrs r2,r6,#0x1    @ 08113328 7208
    adds r0,r3,#0x0    @ 0811332a 181c
    orrs r0,r2    @ 0811332c 1043
    lsrs r1,r7,#0x1    @ 0811332e 7908
    adds r7,r1,#0x0    @ 08113330 0f1c
    adds r6,r0,#0x0    @ 08113332 061c
    adds r0,r6,#0x0    @ 08113334 301c
    movs r1,#0x80    @ 08113336 8021
    lsls r1,r1,#0x18    @ 08113338 0906
    orrs r1,r7    @ 0811333a 3943
    adds r7,r1,#0x0    @ 0811333c 0f1c
    adds r6,r0,#0x0    @ 0811333e 061c
LAB_08113340:
    lsls r3,r5,#0x1f    @ 08113340 eb07
    lsrs r2,r4,#0x1    @ 08113342 6208
    adds r0,r3,#0x0    @ 08113344 181c
    orrs r0,r2    @ 08113346 1043
    lsrs r1,r5,#0x1    @ 08113348 6908
    adds r5,r1,#0x0    @ 0811334a 0d1c
    adds r4,r0,#0x0    @ 0811334c 041c
    cmp r5,r8                                @ 0811334e 4545
    bhi LAB_0811331a                         @ 08113350 e3d8
    .hword 0x4660    @ 08113352 6046
    str r0,[sp,#0x30]                        @ 08113354 0c90
LAB_08113356:
    ldr r0, DAT_08113400                     @ 08113356 2a48
    cmp r5,r0                                @ 08113358 8542
    bhi LAB_081133a8                         @ 0811335a 25d8
    movs r1,#0x80    @ 0811335c 8021
    lsls r1,r1,#0x18    @ 0811335e 0906
    .hword 0x4689    @ 08113360 8946
    .hword 0x4680    @ 08113362 8046
    ldr r2,[sp,#0x30]                        @ 08113364 0c9a
    .hword 0x4694    @ 08113366 9446
LAB_08113368:
    movs r0,#0x1    @ 08113368 0120
    rsbs r0,r0,#0    @ 0811336a 4042
    add r12,r0                               @ 0811336c 8444
    lsrs r3,r4,#0x1f    @ 0811336e e30f
    lsls r2,r5,#0x1    @ 08113370 6a00
    adds r1,r3,#0x0    @ 08113372 191c
    orrs r1,r2    @ 08113374 1143
    lsls r0,r4,#0x1    @ 08113376 6000
    adds r5,r1,#0x0    @ 08113378 0d1c
    adds r4,r0,#0x0    @ 0811337a 041c
    movs r0,#0x0    @ 0811337c 0020
    .hword 0x4649    @ 0811337e 4946
    ands r1,r7    @ 08113380 3940
    orrs r0,r1    @ 08113382 0843
    cmp r0,#0x0                              @ 08113384 0028
    beq LAB_08113392                         @ 08113386 04d0
    movs r0,#0x1    @ 08113388 0120
    orrs r0,r4    @ 0811338a 2043
    adds r1,r5,#0x0    @ 0811338c 291c
    adds r5,r1,#0x0    @ 0811338e 0d1c
    adds r4,r0,#0x0    @ 08113390 041c
LAB_08113392:
    lsrs r3,r6,#0x1f    @ 08113392 f30f
    lsls r2,r7,#0x1    @ 08113394 7a00
    adds r1,r3,#0x0    @ 08113396 191c
    orrs r1,r2    @ 08113398 1143
    lsls r0,r6,#0x1    @ 0811339a 7000
    adds r7,r1,#0x0    @ 0811339c 0f1c
    adds r6,r0,#0x0    @ 0811339e 061c
    cmp r5,r8                                @ 081133a0 4545
    bls LAB_08113368                         @ 081133a2 e1d9
    .hword 0x4661    @ 081133a4 6146
    str r1,[sp,#0x30]                        @ 081133a6 0c91
LAB_081133a8:
    movs r0,#0xff    @ 081133a8 ff20
    adds r1,r4,#0x0    @ 081133aa 211c
    ands r1,r0    @ 081133ac 0140
    movs r2,#0x0    @ 081133ae 0022
    cmp r1,#0x80                             @ 081133b0 8029
    bne LAB_081133d6                         @ 081133b2 10d1
    cmp r2,#0x0                              @ 081133b4 002a
    bne LAB_081133d6                         @ 081133b6 0ed1
    adds r0,#0x1    @ 081133b8 0130
    adds r1,r4,#0x0    @ 081133ba 211c
    ands r1,r0    @ 081133bc 0140
    adds r0,r2,#0x0    @ 081133be 101c
    orrs r0,r1    @ 081133c0 0843
    cmp r0,#0x0                              @ 081133c2 0028
    bne LAB_081133ce                         @ 081133c4 03d1
    adds r0,r7,#0x0    @ 081133c6 381c
    orrs r0,r6    @ 081133c8 3043
    cmp r0,#0x0                              @ 081133ca 0028
    beq LAB_081133d6                         @ 081133cc 03d0
LAB_081133ce:
    movs r0,#0x80    @ 081133ce 8020
    movs r1,#0x0    @ 081133d0 0021
    adds r4,r4,r0    @ 081133d2 2418
    adcs r5,r1    @ 081133d4 4d41
LAB_081133d6:
    str r4,[sp,#0x34]                        @ 081133d6 0d94
    str r5,[sp,#0x38]                        @ 081133d8 0e95
    movs r0,#0x3    @ 081133da 0320
    .hword 0x4652    @ 081133dc 5246
    str r0,[r2,#0x0]                         @ 081133de 1060
    add r0,sp,#0x28                          @ 081133e0 0aa8
LAB_081133e2:
    bl __pack_d                              @ 081133e2 fff741fc
    add sp,#0x74                             @ 081133e6 1db0
    pop {r3,r4,r5}                           @ 081133e8 38bc
    .hword 0x4698    @ 081133ea 9846
    .hword 0x46a1    @ 081133ec a146
    .hword 0x46aa    @ 081133ee aa46
    pop {r4,r5,r6,r7,pc}                     @ 081133f0 f0bd
    .zero  0x2
DAT_081133f4:
    .word  0x00000000                     @ 081133f4 00000000
DAT_081133f8:
    .word  0x00000001                     @ 081133f8 01000000
DAT_081133fc:
    .word  0x1fffffff                     @ 081133fc ffffff1f
DAT_08113400:
    .word  0x0fffffff                     @ 08113400 ffffff0f
__divdf3:
    push {r4,r5,r6,r7,lr}                    @ 08113404 f0b5
    sub sp,#0x48                             @ 08113406 92b0
    str r0,[sp,#0x28]                        @ 08113408 0a90
    str r1,[sp,#0x2c]                        @ 0811340a 0b91
    str r2,[sp,#0x30]                        @ 0811340c 0c92
    str r3,[sp,#0x34]                        @ 0811340e 0d93
    add r0,sp,#0x28                          @ 08113410 0aa8
    .hword 0x4669    @ 08113412 6946
    bl __unpack_d                            @ 08113414 fff7ccfc
    add r0,sp,#0x30                          @ 08113418 0ca8
    add r4,sp,#0x14                          @ 0811341a 05ac
    adds r1,r4,#0x0    @ 0811341c 211c
    bl __unpack_d                            @ 0811341e fff7c7fc
    .hword 0x46ec    @ 08113422 ec46
    movs r0,#0x0    @ 08113424 0020
    ldr r3,[sp,#0x0]                         @ 08113426 009b
    cmp r3,#0x1                              @ 08113428 012b
    bhi LAB_0811342e                         @ 0811342a 00d8
    movs r0,#0x1    @ 0811342c 0120
LAB_0811342e:
    cmp r0,#0x0                              @ 0811342e 0028
    beq LAB_08113436                         @ 08113430 01d0
    .hword 0x4669    @ 08113432 6946
    b LAB_08113578                           @ 08113434 a0e0
LAB_08113436:
    movs r0,#0x0    @ 08113436 0020
    ldr r2,[sp,#0x14]                        @ 08113438 059a
    adds r5,r2,#0x0    @ 0811343a 151c
    cmp r2,#0x1                              @ 0811343c 012a
    bhi LAB_08113442                         @ 0811343e 00d8
    movs r0,#0x1    @ 08113440 0120
LAB_08113442:
    cmp r0,#0x0                              @ 08113442 0028
    beq LAB_0811344a                         @ 08113444 01d0
    adds r1,r4,#0x0    @ 08113446 211c
    b LAB_08113578                           @ 08113448 96e0
LAB_0811344a:
    ldr r0,[sp,#0x4]                         @ 0811344a 0198
    ldr r1,[sp,#0x18]                        @ 0811344c 0699
    eors r0,r1    @ 0811344e 4840
    str r0,[sp,#0x4]                         @ 08113450 0190
    movs r0,#0x0    @ 08113452 0020
    cmp r3,#0x4                              @ 08113454 042b
    bne LAB_0811345a                         @ 08113456 00d1
    movs r0,#0x1    @ 08113458 0120
LAB_0811345a:
    cmp r0,#0x0                              @ 0811345a 0028
    bne LAB_0811346a                         @ 0811345c 05d1
    movs r4,#0x0    @ 0811345e 0024
    cmp r3,#0x2                              @ 08113460 022b
    bne LAB_08113466                         @ 08113462 00d1
    movs r4,#0x1    @ 08113464 0124
LAB_08113466:
    cmp r4,#0x0                              @ 08113466 002c
    beq LAB_0811347c                         @ 08113468 08d0
LAB_0811346a:
    .hword 0x4661    @ 0811346a 6146
    ldr r0,[r1,#0x0]                         @ 0811346c 0868
    cmp r0,r5                                @ 0811346e a842
    beq LAB_08113474                         @ 08113470 00d0
    b LAB_08113578                           @ 08113472 81e0
LAB_08113474:
    ldr r1, DAT_08113478                     @ 08113474 0049
    b LAB_08113578                           @ 08113476 7fe0
DAT_08113478:
    .word  0x03005828                     @ 08113478 28580003
LAB_0811347c:
    movs r0,#0x0    @ 0811347c 0020
    cmp r2,#0x4                              @ 0811347e 042a
    bne LAB_08113484                         @ 08113480 00d1
    movs r0,#0x1    @ 08113482 0120
LAB_08113484:
    cmp r0,#0x0                              @ 08113484 0028
    beq LAB_08113496                         @ 08113486 06d0
    movs r0,#0x0    @ 08113488 0020
    movs r1,#0x0    @ 0811348a 0021
    str r0,[sp,#0xc]                         @ 0811348c 0390
    str r1,[sp,#0x10]                        @ 0811348e 0491
    str r4,[sp,#0x8]                         @ 08113490 0294
    .hword 0x4669    @ 08113492 6946
    b LAB_08113578                           @ 08113494 70e0
LAB_08113496:
    movs r0,#0x0    @ 08113496 0020
    cmp r2,#0x2                              @ 08113498 022a
    bne LAB_0811349e                         @ 0811349a 00d1
    movs r0,#0x1    @ 0811349c 0120
LAB_0811349e:
    cmp r0,#0x0                              @ 0811349e 0028
    beq LAB_081134aa                         @ 081134a0 03d0
    movs r0,#0x4    @ 081134a2 0420
    .hword 0x4662    @ 081134a4 6246
    str r0,[r2,#0x0]                         @ 081134a6 1060
    b LAB_08113576                           @ 081134a8 65e0
LAB_081134aa:
    .hword 0x4663    @ 081134aa 6346
    ldr r1,[r3,#0x8]                         @ 081134ac 9968
    ldr r0,[sp,#0x1c]                        @ 081134ae 0798
    subs r6,r1,r0    @ 081134b0 0e1a
    str r6,[r3,#0x8]                         @ 081134b2 9e60
    ldr r4,[r3,#0xc]                         @ 081134b4 dc68
    ldr r5,[r3,#0x10]                        @ 081134b6 1d69
    ldr r0,[sp,#0x20]                        @ 081134b8 0898
    ldr r1,[sp,#0x24]                        @ 081134ba 0999
    str r0,[sp,#0x38]                        @ 081134bc 0e90
    str r1,[sp,#0x3c]                        @ 081134be 0f91
    cmp r1,r5                                @ 081134c0 a942
    bhi LAB_081134ce                         @ 081134c2 04d8
    ldr r1,[sp,#0x3c]                        @ 081134c4 0f99
    cmp r1,r5                                @ 081134c6 a942
    bne LAB_081134e2                         @ 081134c8 0bd1
    cmp r0,r4                                @ 081134ca a042
    bls LAB_081134e2                         @ 081134cc 09d9
LAB_081134ce:
    lsrs r3,r4,#0x1f    @ 081134ce e30f
    lsls r2,r5,#0x1    @ 081134d0 6a00
    adds r1,r3,#0x0    @ 081134d2 191c
    orrs r1,r2    @ 081134d4 1143
    lsls r0,r4,#0x1    @ 081134d6 6000
    adds r5,r1,#0x0    @ 081134d8 0d1c
    adds r4,r0,#0x0    @ 081134da 041c
    subs r0,r6,#0x1    @ 081134dc 701e
    .hword 0x4662    @ 081134de 6246
    str r0,[r2,#0x8]                         @ 081134e0 9060
LAB_081134e2:
    ldr r7, DAT_08113588                     @ 081134e2 294f
    ldr r6, DAT_08113584                     @ 081134e4 274e
    movs r0,#0x0    @ 081134e6 0020
    movs r1,#0x0    @ 081134e8 0021
    str r0,[sp,#0x40]                        @ 081134ea 1090
    str r1,[sp,#0x44]                        @ 081134ec 1191
LAB_081134ee:
    ldr r1,[sp,#0x3c]                        @ 081134ee 0f99
    cmp r1,r5                                @ 081134f0 a942
    bhi LAB_08113512                         @ 081134f2 0ed8
    cmp r1,r5                                @ 081134f4 a942
    bne LAB_081134fe                         @ 081134f6 02d1
    ldr r2,[sp,#0x38]                        @ 081134f8 0e9a
    cmp r2,r4                                @ 081134fa a242
    bhi LAB_08113512                         @ 081134fc 09d8
LAB_081134fe:
    ldr r0,[sp,#0x40]                        @ 081134fe 1098
    orrs r0,r6    @ 08113500 3043
    ldr r1,[sp,#0x44]                        @ 08113502 1199
    orrs r1,r7    @ 08113504 3943
    str r0,[sp,#0x40]                        @ 08113506 1090
    str r1,[sp,#0x44]                        @ 08113508 1191
    ldr r0,[sp,#0x38]                        @ 0811350a 0e98
    ldr r1,[sp,#0x3c]                        @ 0811350c 0f99
    subs r4,r4,r0    @ 0811350e 241a
    sbcs r5,r1    @ 08113510 8d41
LAB_08113512:
    lsls r3,r7,#0x1f    @ 08113512 fb07
    lsrs r2,r6,#0x1    @ 08113514 7208
    adds r0,r3,#0x0    @ 08113516 181c
    orrs r0,r2    @ 08113518 1043
    lsrs r1,r7,#0x1    @ 0811351a 7908
    adds r7,r1,#0x0    @ 0811351c 0f1c
    adds r6,r0,#0x0    @ 0811351e 061c
    lsrs r3,r4,#0x1f    @ 08113520 e30f
    lsls r2,r5,#0x1    @ 08113522 6a00
    adds r1,r3,#0x0    @ 08113524 191c
    orrs r1,r2    @ 08113526 1143
    lsls r0,r4,#0x1    @ 08113528 6000
    adds r5,r1,#0x0    @ 0811352a 0d1c
    adds r4,r0,#0x0    @ 0811352c 041c
    adds r0,r7,#0x0    @ 0811352e 381c
    orrs r0,r6    @ 08113530 3043
    cmp r0,#0x0                              @ 08113532 0028
    bne LAB_081134ee                         @ 08113534 dbd1
    movs r0,#0xff    @ 08113536 ff20
    ldr r1,[sp,#0x40]                        @ 08113538 1099
    ands r1,r0    @ 0811353a 0140
    movs r2,#0x0    @ 0811353c 0022
    cmp r1,#0x80                             @ 0811353e 8029
    bne LAB_0811356c                         @ 08113540 14d1
    cmp r2,#0x0                              @ 08113542 002a
    bne LAB_0811356c                         @ 08113544 12d1
    adds r0,#0x1    @ 08113546 0130
    ldr r1,[sp,#0x40]                        @ 08113548 1099
    ands r1,r0    @ 0811354a 0140
    adds r0,r2,#0x0    @ 0811354c 101c
    orrs r0,r1    @ 0811354e 0843
    cmp r0,#0x0                              @ 08113550 0028
    bne LAB_0811355c                         @ 08113552 03d1
    adds r0,r5,#0x0    @ 08113554 281c
    orrs r0,r4    @ 08113556 2043
    cmp r0,#0x0                              @ 08113558 0028
    beq LAB_0811356c                         @ 0811355a 07d0
LAB_0811355c:
    movs r0,#0x80    @ 0811355c 8020
    movs r1,#0x0    @ 0811355e 0021
    ldr r2,[sp,#0x40]                        @ 08113560 109a
    ldr r3,[sp,#0x44]                        @ 08113562 119b
    adds r2,r2,r0    @ 08113564 1218
    adcs r3,r1    @ 08113566 4b41
    str r2,[sp,#0x40]                        @ 08113568 1092
    str r3,[sp,#0x44]                        @ 0811356a 1193
LAB_0811356c:
    ldr r0,[sp,#0x40]                        @ 0811356c 1098
    ldr r1,[sp,#0x44]                        @ 0811356e 1199
    .hword 0x4662    @ 08113570 6246
    str r0,[r2,#0xc]                         @ 08113572 d060
    str r1,[r2,#0x10]                        @ 08113574 1161
LAB_08113576:
    .hword 0x4661    @ 08113576 6146
LAB_08113578:
    adds r0,r1,#0x0    @ 08113578 081c
    bl __pack_d                              @ 0811357a fff775fb
    add sp,#0x48                             @ 0811357e 12b0
    pop {r4,r5,r6,r7,pc}                     @ 08113580 f0bd
    .zero  0x2
DAT_08113584:
    .word  0x00000000                     @ 08113584 00000000
DAT_08113588:
    .word  0x10000000                     @ 08113588 00000010
__fpcmp_parts_d:
    push {r4,r5,r6,lr}                       @ 0811358c 70b5
    adds r5,r0,#0x0    @ 0811358e 051c
    adds r6,r1,#0x0    @ 08113590 0e1c
    movs r0,#0x0    @ 08113592 0020
    ldr r1,[r5,#0x0]                         @ 08113594 2968
    cmp r1,#0x1                              @ 08113596 0129
    bhi LAB_0811359c                         @ 08113598 00d8
    movs r0,#0x1    @ 0811359a 0120
LAB_0811359c:
    cmp r0,#0x0                              @ 0811359c 0028
    bne LAB_081135ae                         @ 0811359e 06d1
    movs r0,#0x0    @ 081135a0 0020
    ldr r2,[r6,#0x0]                         @ 081135a2 3268
    cmp r2,#0x1                              @ 081135a4 012a
    bhi LAB_081135aa                         @ 081135a6 00d8
    movs r0,#0x1    @ 081135a8 0120
LAB_081135aa:
    cmp r0,#0x0                              @ 081135aa 0028
    beq LAB_081135b2                         @ 081135ac 01d0
LAB_081135ae:
    movs r0,#0x1    @ 081135ae 0120
    b LAB_08113688                           @ 081135b0 6ae0
LAB_081135b2:
    movs r0,#0x0    @ 081135b2 0020
    cmp r1,#0x4                              @ 081135b4 0429
    bne LAB_081135ba                         @ 081135b6 00d1
    movs r0,#0x1    @ 081135b8 0120
LAB_081135ba:
    cmp r0,#0x0                              @ 081135ba 0028
    beq LAB_081135d2                         @ 081135bc 09d0
    movs r0,#0x0    @ 081135be 0020
    cmp r2,#0x4                              @ 081135c0 042a
    bne LAB_081135c6                         @ 081135c2 00d1
    movs r0,#0x1    @ 081135c4 0120
LAB_081135c6:
    cmp r0,#0x0                              @ 081135c6 0028
    beq LAB_081135d2                         @ 081135c8 03d0
    ldr r0,[r6,#0x4]                         @ 081135ca 7068
    ldr r1,[r5,#0x4]                         @ 081135cc 6968
    subs r0,r0,r1    @ 081135ce 401a
    b LAB_08113688                           @ 081135d0 5ae0
LAB_081135d2:
    movs r1,#0x0    @ 081135d2 0021
    ldr r0,[r5,#0x0]                         @ 081135d4 2868
    cmp r0,#0x4                              @ 081135d6 0428
    bne LAB_081135dc                         @ 081135d8 00d1
    movs r1,#0x1    @ 081135da 0121
LAB_081135dc:
    cmp r1,#0x0                              @ 081135dc 0029
    bne LAB_0811362a                         @ 081135de 24d1
    movs r1,#0x0    @ 081135e0 0021
    cmp r2,#0x4                              @ 081135e2 042a
    bne LAB_081135e8                         @ 081135e4 00d1
    movs r1,#0x1    @ 081135e6 0121
LAB_081135e8:
    cmp r1,#0x0                              @ 081135e8 0029
    beq LAB_081135fa                         @ 081135ea 06d0
LAB_081135ec:
    ldr r0,[r6,#0x4]                         @ 081135ec 7068
    movs r1,#0x1    @ 081135ee 0121
    rsbs r1,r1,#0    @ 081135f0 4942
    cmp r0,#0x0                              @ 081135f2 0028
    beq LAB_08113634                         @ 081135f4 1ed0
    movs r1,#0x1    @ 081135f6 0121
    b LAB_08113634                           @ 081135f8 1ce0
LAB_081135fa:
    movs r1,#0x0    @ 081135fa 0021
    cmp r0,#0x2                              @ 081135fc 0228
    bne LAB_08113602                         @ 081135fe 00d1
    movs r1,#0x1    @ 08113600 0121
LAB_08113602:
    cmp r1,#0x0                              @ 08113602 0029
    beq LAB_08113612                         @ 08113604 05d0
    movs r1,#0x0    @ 08113606 0021
    cmp r2,#0x2                              @ 08113608 022a
    bne LAB_0811360e                         @ 0811360a 00d1
    movs r1,#0x1    @ 0811360c 0121
LAB_0811360e:
    cmp r1,#0x0                              @ 0811360e 0029
    bne LAB_08113686                         @ 08113610 39d1
LAB_08113612:
    movs r1,#0x0    @ 08113612 0021
    cmp r0,#0x2                              @ 08113614 0228
    bne LAB_0811361a                         @ 08113616 00d1
    movs r1,#0x1    @ 08113618 0121
LAB_0811361a:
    cmp r1,#0x0                              @ 0811361a 0029
    bne LAB_081135ec                         @ 0811361c e6d1
    movs r0,#0x0    @ 0811361e 0020
    cmp r2,#0x2                              @ 08113620 022a
    bne LAB_08113626                         @ 08113622 00d1
    movs r0,#0x1    @ 08113624 0120
LAB_08113626:
    cmp r0,#0x0                              @ 08113626 0028
    beq LAB_08113638                         @ 08113628 06d0
LAB_0811362a:
    ldr r0,[r5,#0x4]                         @ 0811362a 6868
    movs r1,#0x1    @ 0811362c 0121
    cmp r0,#0x0                              @ 0811362e 0028
    beq LAB_08113634                         @ 08113630 00d0
    subs r1,#0x2    @ 08113632 0239
LAB_08113634:
    adds r0,r1,#0x0    @ 08113634 081c
    b LAB_08113688                           @ 08113636 27e0
LAB_08113638:
    ldr r0,[r6,#0x4]                         @ 08113638 7068
    ldr r4,[r5,#0x4]                         @ 0811363a 6c68
    cmp r4,r0                                @ 0811363c 8442
    beq LAB_0811364a                         @ 0811363e 04d0
LAB_08113640:
    movs r0,#0x1    @ 08113640 0120
    cmp r4,#0x0                              @ 08113642 002c
    beq LAB_08113688                         @ 08113644 20d0
    subs r0,#0x2    @ 08113646 0238
    b LAB_08113688                           @ 08113648 1ee0
LAB_0811364a:
    ldr r1,[r5,#0x8]                         @ 0811364a a968
    ldr r0,[r6,#0x8]                         @ 0811364c b068
    cmp r1,r0                                @ 0811364e 8142
    bgt LAB_08113640                         @ 08113650 f6dc
    cmp r1,r0                                @ 08113652 8142
    bge LAB_08113662                         @ 08113654 05da
LAB_08113656:
    movs r0,#0x1    @ 08113656 0120
    rsbs r0,r0,#0    @ 08113658 4042
    cmp r4,#0x0                              @ 0811365a 002c
    beq LAB_08113688                         @ 0811365c 14d0
    movs r0,#0x1    @ 0811365e 0120
    b LAB_08113688                           @ 08113660 12e0
LAB_08113662:
    ldr r3,[r5,#0x10]                        @ 08113662 2b69
    ldr r2,[r6,#0x10]                        @ 08113664 3269
    cmp r3,r2                                @ 08113666 9342
    bhi LAB_08113640                         @ 08113668 ead8
    cmp r3,r2                                @ 0811366a 9342
    bne LAB_08113676                         @ 0811366c 03d1
    ldr r1,[r5,#0xc]                         @ 0811366e e968
    ldr r0,[r6,#0xc]                         @ 08113670 f068
    cmp r1,r0                                @ 08113672 8142
    bhi LAB_08113640                         @ 08113674 e4d8
LAB_08113676:
    cmp r2,r3                                @ 08113676 9a42
    bhi LAB_08113656                         @ 08113678 edd8
    cmp r2,r3                                @ 0811367a 9a42
    bne LAB_08113686                         @ 0811367c 03d1
    ldr r1,[r6,#0xc]                         @ 0811367e f168
    ldr r0,[r5,#0xc]                         @ 08113680 e868
    cmp r1,r0                                @ 08113682 8142
    bhi LAB_08113656                         @ 08113684 e7d8
LAB_08113686:
    movs r0,#0x0    @ 08113686 0020
LAB_08113688:
    pop {r4,r5,r6,pc}                        @ 08113688 70bd
    .zero  0x2
__cmpdf2:
    push {r4,lr}                             @ 0811368c 10b5
    sub sp,#0x38                             @ 0811368e 8eb0
    str r0,[sp,#0x28]                        @ 08113690 0a90
    str r1,[sp,#0x2c]                        @ 08113692 0b91
    str r2,[sp,#0x30]                        @ 08113694 0c92
    str r3,[sp,#0x34]                        @ 08113696 0d93
    add r0,sp,#0x28                          @ 08113698 0aa8
    .hword 0x4669    @ 0811369a 6946
    bl __unpack_d                            @ 0811369c fff788fb
    add r0,sp,#0x30                          @ 081136a0 0ca8
    add r4,sp,#0x14                          @ 081136a2 05ac
    adds r1,r4,#0x0    @ 081136a4 211c
    bl __unpack_d                            @ 081136a6 fff783fb
    .hword 0x4668    @ 081136aa 6846
    adds r1,r4,#0x0    @ 081136ac 211c
    bl __fpcmp_parts_d                       @ 081136ae fff76dff
    add sp,#0x38                             @ 081136b2 0eb0
    pop {r4,pc}                              @ 081136b4 10bd
    .zero  0x2

@ GCC libgcc double-precision floating-point equality comparison (__eqdf2): unpacks two doubles (r0:r1=A, r2:r3=B), checks for NaN/Inf; if either operand is NaN returns 1 (nonzero = not equal); otherwise calls __fpcmp_parts_d to compare mantissas, returns 0 for equal, nonzero for unequal.
@ Called by _strtod_r three times; usage pattern: "bl compare_double_eq; cmp r0,#0; bne not_equal".
@ GCC convention: 0 = equal, nonzero = not equal.
compare_double_eq:
    push {r4,lr}                             @ 081136b8 10b5
    sub sp,#0x38                             @ 081136ba 8eb0
    str r0,[sp,#0x28]                        @ 081136bc 0a90
    str r1,[sp,#0x2c]                        @ 081136be 0b91
    str r2,[sp,#0x30]                        @ 081136c0 0c92
    str r3,[sp,#0x34]                        @ 081136c2 0d93
    add r0,sp,#0x28                          @ 081136c4 0aa8
    .hword 0x4669    @ 081136c6 6946
    bl __unpack_d                            @ 081136c8 fff772fb
    add r0,sp,#0x30                          @ 081136cc 0ca8
    add r4,sp,#0x14                          @ 081136ce 05ac
    adds r1,r4,#0x0    @ 081136d0 211c
    bl __unpack_d                            @ 081136d2 fff76dfb
    movs r1,#0x0    @ 081136d6 0021
    ldr r0,[sp,#0x0]                         @ 081136d8 0098
    cmp r0,#0x1                              @ 081136da 0128
    bhi LAB_081136e0                         @ 081136dc 00d8
    movs r1,#0x1    @ 081136de 0121
LAB_081136e0:
    cmp r1,#0x0                              @ 081136e0 0029
    bne LAB_081136f2                         @ 081136e2 06d1
    movs r1,#0x0    @ 081136e4 0021
    ldr r0,[sp,#0x14]                        @ 081136e6 0598
    cmp r0,#0x1                              @ 081136e8 0128
    bhi LAB_081136ee                         @ 081136ea 00d8
    movs r1,#0x1    @ 081136ec 0121
LAB_081136ee:
    cmp r1,#0x0                              @ 081136ee 0029
    beq LAB_081136f6                         @ 081136f0 01d0
LAB_081136f2:
    movs r0,#0x1    @ 081136f2 0120
    b LAB_081136fe                           @ 081136f4 03e0
LAB_081136f6:
    .hword 0x4668    @ 081136f6 6846
    adds r1,r4,#0x0    @ 081136f8 211c
    bl __fpcmp_parts_d                       @ 081136fa fff747ff
LAB_081136fe:
    add sp,#0x38                             @ 081136fe 0eb0
    pop {r4,pc}                              @ 08113700 10bd
    .zero  0x2

@ GCC libgcc double-precision floating-point inequality comparison (__nedf2): structure identical to compare_double_eq (0x081136b8); unpacks two doubles, checks NaN (returns 1) or calls __fpcmp_parts_d.
@ GCC __nedf2 convention: nonzero = not equal (same return value semantics as __eqdf2; caller uses beq/bne to distinguish purpose).
@ This function has callgraph indeg=0 (not directly called by any function), no function pointer references; unused symbol (dead code) from compiler output.
compare_double_ne:
    push {r4,lr}                             @ 08113704 10b5
    sub sp,#0x38                             @ 08113706 8eb0
    str r0,[sp,#0x28]                        @ 08113708 0a90
    str r1,[sp,#0x2c]                        @ 0811370a 0b91
    str r2,[sp,#0x30]                        @ 0811370c 0c92
    str r3,[sp,#0x34]                        @ 0811370e 0d93
    add r0,sp,#0x28                          @ 08113710 0aa8
    .hword 0x4669    @ 08113712 6946
    bl __unpack_d                            @ 08113714 fff74cfb
    add r0,sp,#0x30                          @ 08113718 0ca8
    add r4,sp,#0x14                          @ 0811371a 05ac
    adds r1,r4,#0x0    @ 0811371c 211c
    bl __unpack_d                            @ 0811371e fff747fb
    movs r1,#0x0    @ 08113722 0021
    ldr r0,[sp,#0x0]                         @ 08113724 0098
    cmp r0,#0x1                              @ 08113726 0128
    bhi LAB_0811372c                         @ 08113728 00d8
    movs r1,#0x1    @ 0811372a 0121
LAB_0811372c:
    cmp r1,#0x0                              @ 0811372c 0029
    bne LAB_0811373e                         @ 0811372e 06d1
    movs r1,#0x0    @ 08113730 0021
    ldr r0,[sp,#0x14]                        @ 08113732 0598
    cmp r0,#0x1                              @ 08113734 0128
    bhi LAB_0811373a                         @ 08113736 00d8
    movs r1,#0x1    @ 08113738 0121
LAB_0811373a:
    cmp r1,#0x0                              @ 0811373a 0029
    beq LAB_08113742                         @ 0811373c 01d0
LAB_0811373e:
    movs r0,#0x1    @ 0811373e 0120
    b LAB_0811374a                           @ 08113740 03e0
LAB_08113742:
    .hword 0x4668    @ 08113742 6846
    adds r1,r4,#0x0    @ 08113744 211c
    bl __fpcmp_parts_d                       @ 08113746 fff721ff
LAB_0811374a:
    add sp,#0x38                             @ 0811374a 0eb0
    pop {r4,pc}                              @ 0811374c 10bd
    .zero  0x2

@ GCC libgcc double-precision floating-point greater-than comparison (__gtdf2): unpacks two doubles, checks NaN (executes rsbs -> returns -1 = unordered, not greater); normal path calls __fpcmp_parts_d.
@ GCC convention: positive = A>B, zero or negative = A<=B or contains NaN.
@ Called by _strtod_r using "cmp r0,#0; ble label" pattern (result <=0 = not greater, branch taken).
compare_double_gt:
    push {r4,lr}                             @ 08113750 10b5
    sub sp,#0x38                             @ 08113752 8eb0
    str r0,[sp,#0x28]                        @ 08113754 0a90
    str r1,[sp,#0x2c]                        @ 08113756 0b91
    str r2,[sp,#0x30]                        @ 08113758 0c92
    str r3,[sp,#0x34]                        @ 0811375a 0d93
    add r0,sp,#0x28                          @ 0811375c 0aa8
    .hword 0x4669    @ 0811375e 6946
    bl __unpack_d                            @ 08113760 fff726fb
    add r0,sp,#0x30                          @ 08113764 0ca8
    add r4,sp,#0x14                          @ 08113766 05ac
    adds r1,r4,#0x0    @ 08113768 211c
    bl __unpack_d                            @ 0811376a fff721fb
    movs r1,#0x0    @ 0811376e 0021
    ldr r0,[sp,#0x0]                         @ 08113770 0098
    cmp r0,#0x1                              @ 08113772 0128
    bhi LAB_08113778                         @ 08113774 00d8
    movs r1,#0x1    @ 08113776 0121
LAB_08113778:
    cmp r1,#0x0                              @ 08113778 0029
    bne LAB_0811378a                         @ 0811377a 06d1
    movs r1,#0x0    @ 0811377c 0021
    ldr r0,[sp,#0x14]                        @ 0811377e 0598
    cmp r0,#0x1                              @ 08113780 0128
    bhi LAB_08113786                         @ 08113782 00d8
    movs r1,#0x1    @ 08113784 0121
LAB_08113786:
    cmp r1,#0x0                              @ 08113786 0029
    beq LAB_08113790                         @ 08113788 02d0
LAB_0811378a:
    movs r0,#0x1    @ 0811378a 0120
    rsbs r0,r0,#0    @ 0811378c 4042
    b LAB_08113798                           @ 0811378e 03e0
LAB_08113790:
    .hword 0x4668    @ 08113790 6846
    adds r1,r4,#0x0    @ 08113792 211c
    bl __fpcmp_parts_d                       @ 08113794 fff7fafe
LAB_08113798:
    add sp,#0x38                             @ 08113798 0eb0
    pop {r4,pc}                              @ 0811379a 10bd

@ GCC libgcc double-precision floating-point greater-or-equal comparison (__gedf2): unpacks two doubles, checks NaN (rsbs -> returns -1 = unordered, does not satisfy >=); normal path calls __fpcmp_parts_d.
@ GCC convention: >=0 = A>=B, negative = A<B or contains NaN.
@ Called by _strtod_r using "cmp r0,#0; blt label" pattern (result <0 = less than or unordered, branch taken).
compare_double_ge:
    push {r4,lr}                             @ 0811379c 10b5
    sub sp,#0x38                             @ 0811379e 8eb0
    str r0,[sp,#0x28]                        @ 081137a0 0a90
    str r1,[sp,#0x2c]                        @ 081137a2 0b91
    str r2,[sp,#0x30]                        @ 081137a4 0c92
    str r3,[sp,#0x34]                        @ 081137a6 0d93
    add r0,sp,#0x28                          @ 081137a8 0aa8
    .hword 0x4669    @ 081137aa 6946
    bl __unpack_d                            @ 081137ac fff700fb
    add r0,sp,#0x30                          @ 081137b0 0ca8
    add r4,sp,#0x14                          @ 081137b2 05ac
    adds r1,r4,#0x0    @ 081137b4 211c
    bl __unpack_d                            @ 081137b6 fff7fbfa
    movs r1,#0x0    @ 081137ba 0021
    ldr r0,[sp,#0x0]                         @ 081137bc 0098
    cmp r0,#0x1                              @ 081137be 0128
    bhi LAB_081137c4                         @ 081137c0 00d8
    movs r1,#0x1    @ 081137c2 0121
LAB_081137c4:
    cmp r1,#0x0                              @ 081137c4 0029
    bne LAB_081137d6                         @ 081137c6 06d1
    movs r1,#0x0    @ 081137c8 0021
    ldr r0,[sp,#0x14]                        @ 081137ca 0598
    cmp r0,#0x1                              @ 081137cc 0128
    bhi LAB_081137d2                         @ 081137ce 00d8
    movs r1,#0x1    @ 081137d0 0121
LAB_081137d2:
    cmp r1,#0x0                              @ 081137d2 0029
    beq LAB_081137dc                         @ 081137d4 02d0
LAB_081137d6:
    movs r0,#0x1    @ 081137d6 0120
    rsbs r0,r0,#0    @ 081137d8 4042
    b LAB_081137e4                           @ 081137da 03e0
LAB_081137dc:
    .hword 0x4668    @ 081137dc 6846
    adds r1,r4,#0x0    @ 081137de 211c
    bl __fpcmp_parts_d                       @ 081137e0 fff7d4fe
LAB_081137e4:
    add sp,#0x38                             @ 081137e4 0eb0
    pop {r4,pc}                              @ 081137e6 10bd

@ GCC libgcc double-precision floating-point less-than comparison (__ltdf2): unpacks two doubles, checks NaN (returns +1 = unordered, does not satisfy <); normal path calls __fpcmp_parts_d.
@ GCC convention: negative = A<B, >=0 = A>=B or contains NaN.
@ Called by _strtod_r three times using "cmp r0,#0; bge label" pattern (result >=0 = not less, branch taken).
compare_double_lt:
    push {r4,lr}                             @ 081137e8 10b5
    sub sp,#0x38                             @ 081137ea 8eb0
    str r0,[sp,#0x28]                        @ 081137ec 0a90
    str r1,[sp,#0x2c]                        @ 081137ee 0b91
    str r2,[sp,#0x30]                        @ 081137f0 0c92
    str r3,[sp,#0x34]                        @ 081137f2 0d93
    add r0,sp,#0x28                          @ 081137f4 0aa8
    .hword 0x4669    @ 081137f6 6946
    bl __unpack_d                            @ 081137f8 fff7dafa
    add r0,sp,#0x30                          @ 081137fc 0ca8
    add r4,sp,#0x14                          @ 081137fe 05ac
    adds r1,r4,#0x0    @ 08113800 211c
    bl __unpack_d                            @ 08113802 fff7d5fa
    movs r1,#0x0    @ 08113806 0021
    ldr r0,[sp,#0x0]                         @ 08113808 0098
    cmp r0,#0x1                              @ 0811380a 0128
    bhi LAB_08113810                         @ 0811380c 00d8
    movs r1,#0x1    @ 0811380e 0121
LAB_08113810:
    cmp r1,#0x0                              @ 08113810 0029
    bne LAB_08113822                         @ 08113812 06d1
    movs r1,#0x0    @ 08113814 0021
    ldr r0,[sp,#0x14]                        @ 08113816 0598
    cmp r0,#0x1                              @ 08113818 0128
    bhi LAB_0811381e                         @ 0811381a 00d8
    movs r1,#0x1    @ 0811381c 0121
LAB_0811381e:
    cmp r1,#0x0                              @ 0811381e 0029
    beq LAB_08113826                         @ 08113820 01d0
LAB_08113822:
    movs r0,#0x1    @ 08113822 0120
    b LAB_0811382e                           @ 08113824 03e0
LAB_08113826:
    .hword 0x4668    @ 08113826 6846
    adds r1,r4,#0x0    @ 08113828 211c
    bl __fpcmp_parts_d                       @ 0811382a fff7affe
LAB_0811382e:
    add sp,#0x38                             @ 0811382e 0eb0
    pop {r4,pc}                              @ 08113830 10bd
    .zero  0x2

@ GCC libgcc double-precision floating-point less-or-equal comparison (__ledf2): unpacks two doubles, checks NaN (returns +1 = unordered, does not satisfy <=); normal path calls __fpcmp_parts_d.
@ GCC convention: <=0 = A<=B, positive = A>B or contains NaN.
@ Called by _strtod_r using "cmp r0,#0; bgt label" pattern (result >0 = greater or unordered, branch taken).
compare_double_le:
    push {r4,lr}                             @ 08113834 10b5
    sub sp,#0x38                             @ 08113836 8eb0
    str r0,[sp,#0x28]                        @ 08113838 0a90
    str r1,[sp,#0x2c]                        @ 0811383a 0b91
    str r2,[sp,#0x30]                        @ 0811383c 0c92
    str r3,[sp,#0x34]                        @ 0811383e 0d93
    add r0,sp,#0x28                          @ 08113840 0aa8
    .hword 0x4669    @ 08113842 6946
    bl __unpack_d                            @ 08113844 fff7b4fa
    add r0,sp,#0x30                          @ 08113848 0ca8
    add r4,sp,#0x14                          @ 0811384a 05ac
    adds r1,r4,#0x0    @ 0811384c 211c
    bl __unpack_d                            @ 0811384e fff7affa
    movs r1,#0x0    @ 08113852 0021
    ldr r0,[sp,#0x0]                         @ 08113854 0098
    cmp r0,#0x1                              @ 08113856 0128
    bhi LAB_0811385c                         @ 08113858 00d8
    movs r1,#0x1    @ 0811385a 0121
LAB_0811385c:
    cmp r1,#0x0                              @ 0811385c 0029
    bne LAB_0811386e                         @ 0811385e 06d1
    movs r1,#0x0    @ 08113860 0021
    ldr r0,[sp,#0x14]                        @ 08113862 0598
    cmp r0,#0x1                              @ 08113864 0128
    bhi LAB_0811386a                         @ 08113866 00d8
    movs r1,#0x1    @ 08113868 0121
LAB_0811386a:
    cmp r1,#0x0                              @ 0811386a 0029
    beq LAB_08113872                         @ 0811386c 01d0
LAB_0811386e:
    movs r0,#0x1    @ 0811386e 0120
    b LAB_0811387a                           @ 08113870 03e0
LAB_08113872:
    .hword 0x4668    @ 08113872 6846
    adds r1,r4,#0x0    @ 08113874 211c
    bl __fpcmp_parts_d                       @ 08113876 fff789fe
LAB_0811387a:
    add sp,#0x38                             @ 0811387a 0eb0
    pop {r4,pc}                              @ 0811387c 10bd
    .zero  0x2
__floatsidf:
    push {r4,r5,lr}                          @ 08113880 30b5
    sub sp,#0x14                             @ 08113882 85b0
    adds r2,r0,#0x0    @ 08113884 021c
    movs r0,#0x3    @ 08113886 0320
    str r0,[sp,#0x0]                         @ 08113888 0090
    lsrs r1,r2,#0x1f    @ 0811388a d10f
    str r1,[sp,#0x4]                         @ 0811388c 0191
    cmp r2,#0x0                              @ 0811388e 002a
    bne LAB_08113898                         @ 08113890 02d1
    movs r0,#0x2    @ 08113892 0220
    str r0,[sp,#0x0]                         @ 08113894 0090
    b LAB_081138ee                           @ 08113896 2ae0
LAB_08113898:
    movs r0,#0x3c    @ 08113898 3c20
    str r0,[sp,#0x8]                         @ 0811389a 0290
    cmp r1,#0x0                              @ 0811389c 0029
    beq LAB_081138be                         @ 0811389e 0ed0
    movs r0,#0x80    @ 081138a0 8020
    lsls r0,r0,#0x18    @ 081138a2 0006
    cmp r2,r0                                @ 081138a4 8242
    bne LAB_081138b8                         @ 081138a6 07d1
    ldr r1, DAT_081138b4                     @ 081138a8 0249
    ldr r0, DAT_081138b0                     @ 081138aa 0148
    b LAB_081138f4                           @ 081138ac 22e0
    .zero  0x2
DAT_081138b0:
    .word  0xc1e00000                     @ 081138b0 0000e0c1
DAT_081138b4:
    .word  0x00000000                     @ 081138b4 00000000
LAB_081138b8:
    rsbs r0,r2,#0    @ 081138b8 5042
    asrs r1,r0,#0x1f    @ 081138ba c117
    b LAB_081138c2                           @ 081138bc 01e0
LAB_081138be:
    adds r0,r2,#0x0    @ 081138be 101c
    asrs r1,r2,#0x1f    @ 081138c0 d117
LAB_081138c2:
    str r0,[sp,#0xc]                         @ 081138c2 0390
    str r1,[sp,#0x10]                        @ 081138c4 0491
    ldr r0,[sp,#0x10]                        @ 081138c6 0498
    ldr r1, DAT_081138f8                     @ 081138c8 0b49
    cmp r0,r1                                @ 081138ca 8842
    bhi LAB_081138ee                         @ 081138cc 0fd8
    adds r5,r1,#0x0    @ 081138ce 0d1c
    ldr r4,[sp,#0x8]                         @ 081138d0 029c
LAB_081138d2:
    ldr r0,[sp,#0xc]                         @ 081138d2 0398
    ldr r1,[sp,#0x10]                        @ 081138d4 0499
    lsrs r3,r0,#0x1f    @ 081138d6 c30f
    lsls r2,r1,#0x1    @ 081138d8 4a00
    adds r1,r3,#0x0    @ 081138da 191c
    orrs r1,r2    @ 081138dc 1143
    lsls r0,r0,#0x1    @ 081138de 4000
    str r0,[sp,#0xc]                         @ 081138e0 0390
    str r1,[sp,#0x10]                        @ 081138e2 0491
    subs r4,#0x1    @ 081138e4 013c
    ldr r0,[sp,#0x10]                        @ 081138e6 0498
    cmp r0,r5                                @ 081138e8 a842
    bls LAB_081138d2                         @ 081138ea f2d9
    str r4,[sp,#0x8]                         @ 081138ec 0294
LAB_081138ee:
    .hword 0x4668    @ 081138ee 6846
    bl __pack_d                              @ 081138f0 fff7baf9
LAB_081138f4:
    add sp,#0x14                             @ 081138f4 05b0
    pop {r4,r5,pc}                           @ 081138f6 30bd
DAT_081138f8:
    .word  0x0fffffff                     @ 081138f8 ffffff0f
__fixdfsi:
    push {lr}                                @ 081138fc 00b5
    sub sp,#0x1c                             @ 081138fe 87b0
    str r0,[sp,#0x14]                        @ 08113900 0590
    str r1,[sp,#0x18]                        @ 08113902 0691
    add r0,sp,#0x14                          @ 08113904 05a8
    .hword 0x4669    @ 08113906 6946
    bl __unpack_d                            @ 08113908 fff752fa
    movs r1,#0x0    @ 0811390c 0021
    ldr r0,[sp,#0x0]                         @ 0811390e 0098
    cmp r0,#0x2                              @ 08113910 0228
    bne LAB_08113916                         @ 08113912 00d1
    movs r1,#0x1    @ 08113914 0121
LAB_08113916:
    cmp r1,#0x0                              @ 08113916 0029
    bne LAB_0811394a                         @ 08113918 17d1
    movs r1,#0x0    @ 0811391a 0021
    cmp r0,#0x1                              @ 0811391c 0128
    bhi LAB_08113922                         @ 0811391e 00d8
    movs r1,#0x1    @ 08113920 0121
LAB_08113922:
    cmp r1,#0x0                              @ 08113922 0029
    bne LAB_0811394a                         @ 08113924 11d1
    movs r1,#0x0    @ 08113926 0021
    cmp r0,#0x4                              @ 08113928 0428
    bne LAB_0811392e                         @ 0811392a 00d1
    movs r1,#0x1    @ 0811392c 0121
LAB_0811392e:
    cmp r1,#0x0                              @ 0811392e 0029
    beq LAB_08113944                         @ 08113930 08d0
LAB_08113932:
    ldr r0,[sp,#0x4]                         @ 08113932 0198
    ldr r1, DAT_08113940                     @ 08113934 0249
    cmp r0,#0x0                              @ 08113936 0028
    beq LAB_08113968                         @ 08113938 16d0
    adds r1,#0x1    @ 0811393a 0131
    b LAB_08113968                           @ 0811393c 14e0
    .zero  0x2
DAT_08113940:
    .word  0x7fffffff                     @ 08113940 ffffff7f
LAB_08113944:
    ldr r0,[sp,#0x8]                         @ 08113944 0298
    cmp r0,#0x0                              @ 08113946 0028
    bge LAB_0811394e                         @ 08113948 01da
LAB_0811394a:
    movs r0,#0x0    @ 0811394a 0020
    b LAB_0811396a                           @ 0811394c 0de0
LAB_0811394e:
    cmp r0,#0x1e                             @ 0811394e 1e28
    bgt LAB_08113932                         @ 08113950 efdc
    movs r2,#0x3c    @ 08113952 3c22
    subs r2,r2,r0    @ 08113954 121a
    ldr r0,[sp,#0xc]                         @ 08113956 0398
    ldr r1,[sp,#0x10]                        @ 08113958 0499
    bl __lshrdi3                             @ 0811395a 00f0f9fc
    adds r1,r0,#0x0    @ 0811395e 011c
    ldr r0,[sp,#0x4]                         @ 08113960 0198
    cmp r0,#0x0                              @ 08113962 0028
    beq LAB_08113968                         @ 08113964 00d0
    rsbs r1,r1,#0    @ 08113966 4942
LAB_08113968:
    adds r0,r1,#0x0    @ 08113968 081c
LAB_0811396a:
    add sp,#0x1c                             @ 0811396a 07b0
    pop {pc}                                 @ 0811396c 00bd
    .zero  0x2
__negdf2:
    push {lr}                                @ 08113970 00b5
    sub sp,#0x1c                             @ 08113972 87b0
    str r0,[sp,#0x14]                        @ 08113974 0590
    str r1,[sp,#0x18]                        @ 08113976 0691
    add r0,sp,#0x14                          @ 08113978 05a8
    .hword 0x4669    @ 0811397a 6946
    bl __unpack_d                            @ 0811397c fff718fa
    movs r1,#0x0    @ 08113980 0021
    ldr r0,[sp,#0x4]                         @ 08113982 0198
    cmp r0,#0x0                              @ 08113984 0028
    bne LAB_0811398a                         @ 08113986 00d1
    movs r1,#0x1    @ 08113988 0121
LAB_0811398a:
    str r1,[sp,#0x4]                         @ 0811398a 0191
    .hword 0x4668    @ 0811398c 6846
    bl __pack_d                              @ 0811398e fff76bf9
    add sp,#0x1c                             @ 08113992 07b0
    pop {pc}                                 @ 08113994 00bd
    .zero  0x2
__make_dp:
    sub sp,#0x4                              @ 08113998 81b0
    push {r4,lr}                             @ 0811399a 10b5
    sub sp,#0x14                             @ 0811399c 85b0
    str r3,[sp,#0x1c]                        @ 0811399e 0793
    ldr r3,[sp,#0x1c]                        @ 081139a0 079b
    ldr r4,[sp,#0x20]                        @ 081139a2 089c
    str r0,[sp,#0x0]                         @ 081139a4 0090
    str r1,[sp,#0x4]                         @ 081139a6 0191
    str r2,[sp,#0x8]                         @ 081139a8 0292
    str r3,[sp,#0xc]                         @ 081139aa 0393
    str r4,[sp,#0x10]                        @ 081139ac 0494
    .hword 0x4668    @ 081139ae 6846
    bl __pack_d                              @ 081139b0 fff75af9
    add sp,#0x14                             @ 081139b4 05b0
    pop {r4}                                 @ 081139b6 10bc
    pop {r3}                                 @ 081139b8 08bc
    add sp,#0x4                              @ 081139ba 01b0
    bx r3                                    @ 081139bc 1847
    .zero  0x2
__truncdfsf2:
    push {r4,r5,lr}                          @ 081139c0 30b5
    sub sp,#0x1c                             @ 081139c2 87b0
    str r0,[sp,#0x14]                        @ 081139c4 0590
    str r1,[sp,#0x18]                        @ 081139c6 0691
    add r0,sp,#0x14                          @ 081139c8 05a8
    .hword 0x4669    @ 081139ca 6946
    bl __unpack_d                            @ 081139cc fff7f0f9
    ldr r2,[sp,#0xc]                         @ 081139d0 039a
    ldr r3,[sp,#0x10]                        @ 081139d2 049b
    lsls r5,r3,#0x2    @ 081139d4 9d00
    lsrs r4,r2,#0x1e    @ 081139d6 940f
    adds r0,r5,#0x0    @ 081139d8 281c
    orrs r0,r4    @ 081139da 2043
    adds r5,r0,#0x0    @ 081139dc 051c
    ldr r4, DAT_08113a00                     @ 081139de 084c
    adds r0,r2,#0x0    @ 081139e0 101c
    ands r0,r4    @ 081139e2 2040
    movs r1,#0x0    @ 081139e4 0021
    orrs r0,r1    @ 081139e6 0843
    cmp r0,#0x0                              @ 081139e8 0028
    beq LAB_081139f0                         @ 081139ea 01d0
    movs r0,#0x1    @ 081139ec 0120
    orrs r5,r0    @ 081139ee 0543
LAB_081139f0:
    ldr r0,[sp,#0x0]                         @ 081139f0 0098
    ldr r1,[sp,#0x4]                         @ 081139f2 0199
    ldr r2,[sp,#0x8]                         @ 081139f4 029a
    adds r3,r5,#0x0    @ 081139f6 2b1c
    bl __make_fp                             @ 081139f8 00f088fc
    add sp,#0x1c                             @ 081139fc 07b0
    pop {r4,r5,pc}                           @ 081139fe 30bd
DAT_08113a00:
    .word  0x3fffffff                     @ 08113a00 ffffff3f
__pack_f:
    push {r4,r5,r6,lr}                       @ 08113a04 70b5
    ldr r2,[r0,#0xc]                         @ 08113a06 c268
    ldr r6,[r0,#0x4]                         @ 08113a08 4668
    movs r5,#0x0    @ 08113a0a 0025
    movs r1,#0x0    @ 08113a0c 0021
    ldr r3,[r0,#0x0]                         @ 08113a0e 0368
    cmp r3,#0x1                              @ 08113a10 012b
    bhi LAB_08113a16                         @ 08113a12 00d8
    movs r1,#0x1    @ 08113a14 0121
LAB_08113a16:
    cmp r1,#0x0                              @ 08113a16 0029
    beq LAB_08113a24                         @ 08113a18 04d0
    movs r5,#0xff    @ 08113a1a ff25
    movs r0,#0x80    @ 08113a1c 8020
    lsls r0,r0,#0xd    @ 08113a1e 4003
    orrs r2,r0    @ 08113a20 0243
    b LAB_08113a8a                           @ 08113a22 32e0
LAB_08113a24:
    movs r1,#0x0    @ 08113a24 0021
    cmp r3,#0x4                              @ 08113a26 042b
    bne LAB_08113a2c                         @ 08113a28 00d1
    movs r1,#0x1    @ 08113a2a 0121
LAB_08113a2c:
    cmp r1,#0x0                              @ 08113a2c 0029
    bne LAB_08113a60                         @ 08113a2e 17d1
    movs r1,#0x0    @ 08113a30 0021
    cmp r3,#0x2                              @ 08113a32 022b
    bne LAB_08113a38                         @ 08113a34 00d1
    movs r1,#0x1    @ 08113a36 0121
LAB_08113a38:
    cmp r1,#0x0                              @ 08113a38 0029
    beq LAB_08113a40                         @ 08113a3a 01d0
    movs r2,#0x0    @ 08113a3c 0022
    b LAB_08113a8a                           @ 08113a3e 24e0
LAB_08113a40:
    cmp r2,#0x0                              @ 08113a40 002a
    beq LAB_08113a8a                         @ 08113a42 22d0
    ldr r0,[r0,#0x8]                         @ 08113a44 8068
    movs r3,#0x7e    @ 08113a46 7e23
    rsbs r3,r3,#0    @ 08113a48 5b42
    cmp r0,r3                                @ 08113a4a 9842
    bge LAB_08113a5c                         @ 08113a4c 06da
    subs r0,r3,r0    @ 08113a4e 181a
    cmp r0,#0x19                             @ 08113a50 1928
    ble LAB_08113a58                         @ 08113a52 01dd
    movs r2,#0x0    @ 08113a54 0022
    b LAB_08113a88                           @ 08113a56 17e0
LAB_08113a58:
    lsrs r2,r0    @ 08113a58 c240
    b LAB_08113a88                           @ 08113a5a 15e0
LAB_08113a5c:
    cmp r0,#0x7f                             @ 08113a5c 7f28
    ble LAB_08113a66                         @ 08113a5e 02dd
LAB_08113a60:
    movs r5,#0xff    @ 08113a60 ff25
    movs r2,#0x0    @ 08113a62 0022
    b LAB_08113a8a                           @ 08113a64 11e0
LAB_08113a66:
    adds r5,r0,#0x0    @ 08113a66 051c
    adds r5,#0x7f    @ 08113a68 7f35
    movs r0,#0x7f    @ 08113a6a 7f20
    ands r0,r2    @ 08113a6c 1040
    cmp r0,#0x40                             @ 08113a6e 4028
    bne LAB_08113a7e                         @ 08113a70 05d1
    movs r0,#0x80    @ 08113a72 8020
    ands r0,r2    @ 08113a74 1040
    cmp r0,#0x0                              @ 08113a76 0028
    beq LAB_08113a80                         @ 08113a78 02d0
    adds r2,#0x40    @ 08113a7a 4032
    b LAB_08113a80                           @ 08113a7c 00e0
LAB_08113a7e:
    adds r2,#0x3f    @ 08113a7e 3f32
LAB_08113a80:
    cmp r2,#0x0                              @ 08113a80 002a
    bge LAB_08113a88                         @ 08113a82 01da
    lsrs r2,r2,#0x1    @ 08113a84 5208
    adds r5,#0x1    @ 08113a86 0135
LAB_08113a88:
    lsrs r2,r2,#0x7    @ 08113a88 d209
LAB_08113a8a:
    ldr r0, DAT_08113aac                     @ 08113a8a 0848
    ands r2,r0    @ 08113a8c 0240
    ldr r0, DAT_08113ab0                     @ 08113a8e 0848
    ands r4,r0    @ 08113a90 0440
    orrs r4,r2    @ 08113a92 1443
    movs r0,#0xff    @ 08113a94 ff20
    ands r5,r0    @ 08113a96 0540
    lsls r1,r5,#0x17    @ 08113a98 e905
    ldr r0, DAT_08113ab4                     @ 08113a9a 0648
    ands r4,r0    @ 08113a9c 0440
    orrs r4,r1    @ 08113a9e 0c43
    lsls r1,r6,#0x1f    @ 08113aa0 f107
    ldr r0, DAT_08113ab8                     @ 08113aa2 0548
    ands r4,r0    @ 08113aa4 0440
    orrs r4,r1    @ 08113aa6 0c43
    adds r0,r4,#0x0    @ 08113aa8 201c
    pop {r4,r5,r6,pc}                        @ 08113aaa 70bd
DAT_08113aac:
    .word  0x007fffff                     @ 08113aac ffff7f00
DAT_08113ab0:
    .word  0xff800000                     @ 08113ab0 000080ff
DAT_08113ab4:
    .word  0x807fffff                     @ 08113ab4 ffff7f80
DAT_08113ab8:
    .word  0x7fffffff                     @ 08113ab8 ffffff7f
__unpack_f:
    push {r4,lr}                             @ 08113abc 10b5
    adds r3,r1,#0x0    @ 08113abe 0b1c
    ldr r0,[r0,#0x0]                         @ 08113ac0 0068
    lsls r1,r0,#0x9    @ 08113ac2 4102
    lsrs r2,r1,#0x9    @ 08113ac4 4a0a
    lsls r1,r0,#0x1    @ 08113ac6 4100
    lsrs r1,r1,#0x18    @ 08113ac8 090e
    lsrs r0,r0,#0x1f    @ 08113aca c00f
    str r0,[r3,#0x4]                         @ 08113acc 5860
    cmp r1,#0x0                              @ 08113ace 0029
    bne LAB_08113b00                         @ 08113ad0 16d1
    cmp r2,#0x0                              @ 08113ad2 002a
    bne LAB_08113adc                         @ 08113ad4 02d1
    movs r0,#0x2    @ 08113ad6 0220
    str r0,[r3,#0x0]                         @ 08113ad8 1860
    b LAB_08113b34                           @ 08113ada 2be0
LAB_08113adc:
    adds r4,r1,#0x0    @ 08113adc 0c1c
    subs r4,#0x7e    @ 08113ade 7e3c
    str r4,[r3,#0x8]                         @ 08113ae0 9c60
    lsls r2,r2,#0x7    @ 08113ae2 d201
    movs r0,#0x3    @ 08113ae4 0320
    str r0,[r3,#0x0]                         @ 08113ae6 1860
    ldr r1, DAT_08113afc                     @ 08113ae8 0449
    cmp r2,r1                                @ 08113aea 8a42
    bhi LAB_08113b1c                         @ 08113aec 16d8
    adds r0,r4,#0x0    @ 08113aee 201c
LAB_08113af0:
    lsls r2,r2,#0x1    @ 08113af0 5200
    subs r0,#0x1    @ 08113af2 0138
    cmp r2,r1                                @ 08113af4 8a42
    bls LAB_08113af0                         @ 08113af6 fbd9
    str r0,[r3,#0x8]                         @ 08113af8 9860
    b LAB_08113b1c                           @ 08113afa 0fe0
DAT_08113afc:
    .word  0x3fffffff                     @ 08113afc ffffff3f
LAB_08113b00:
    cmp r1,#0xff                             @ 08113b00 ff29
    bne LAB_08113b20                         @ 08113b02 0dd1
    cmp r2,#0x0                              @ 08113b04 002a
    bne LAB_08113b0e                         @ 08113b06 02d1
    movs r0,#0x4    @ 08113b08 0420
    str r0,[r3,#0x0]                         @ 08113b0a 1860
    b LAB_08113b34                           @ 08113b0c 12e0
LAB_08113b0e:
    movs r0,#0x80    @ 08113b0e 8020
    lsls r0,r0,#0xd    @ 08113b10 4003
    ands r0,r2    @ 08113b12 1040
    cmp r0,#0x0                              @ 08113b14 0028
    beq LAB_08113b1a                         @ 08113b16 00d0
    movs r0,#0x1    @ 08113b18 0120
LAB_08113b1a:
    str r0,[r3,#0x0]                         @ 08113b1a 1860
LAB_08113b1c:
    str r2,[r3,#0xc]                         @ 08113b1c da60
    b LAB_08113b34                           @ 08113b1e 09e0
LAB_08113b20:
    adds r0,r1,#0x0    @ 08113b20 081c
    subs r0,#0x7f    @ 08113b22 7f38
    str r0,[r3,#0x8]                         @ 08113b24 9860
    movs r0,#0x3    @ 08113b26 0320
    str r0,[r3,#0x0]                         @ 08113b28 1860
    lsls r0,r2,#0x7    @ 08113b2a d001
    movs r1,#0x80    @ 08113b2c 8021
    lsls r1,r1,#0x17    @ 08113b2e c905
    orrs r0,r1    @ 08113b30 0843
    str r0,[r3,#0xc]                         @ 08113b32 d860
LAB_08113b34:
    pop {r4,pc}                              @ 08113b34 10bd
    .zero  0x2

@ newlib/libgcc single-precision floating-point add/subtract core: receives two unpacked float component structs (r0=A, r1=B, r2=result), performs NaN/Inf/zero propagation checks, aligns mantissas (max 0x1f shift), executes 32-bit sub/add and normalizes, writes result components.
@ Called by __addsf3 (0x08113cb4) and __subsf3 (0x08113ce0); both share this core after unpacking float.
@ Single-precision version symmetric with exec_addsubdf3_core (0x08112e88) but operates on 32-bit mantissa (not 64-bit).
@ 
@ Constants:
@ - MAX_EXP_DIFF_SF=0x1f (exponent difference threshold; operand with smaller exponent is zeroed if exceeded)
@ - MANTISSA_BOUND=0x3ffffffe (normalized mantissa upper bound)
exec_addsubsf3_core:
    push {r4,r5,r6,r7,lr}                    @ 08113b38 f0b5
    .hword 0x4647    @ 08113b3a 4746
    push {r7}                                @ 08113b3c 80b4
    adds r6,r0,#0x0    @ 08113b3e 061c
    adds r7,r1,#0x0    @ 08113b40 0f1c
    adds r5,r2,#0x0    @ 08113b42 151c
    movs r0,#0x0    @ 08113b44 0020
    ldr r2,[r6,#0x0]                         @ 08113b46 3268
    cmp r2,#0x1                              @ 08113b48 012a
    bhi LAB_08113b4e                         @ 08113b4a 00d8
    movs r0,#0x1    @ 08113b4c 0120
LAB_08113b4e:
    cmp r0,#0x0                              @ 08113b4e 0028
    beq LAB_08113b56                         @ 08113b50 01d0
LAB_08113b52:
    adds r0,r6,#0x0    @ 08113b52 301c
    b LAB_08113cac                           @ 08113b54 aae0
LAB_08113b56:
    movs r1,#0x0    @ 08113b56 0021
    ldr r0,[r7,#0x0]                         @ 08113b58 3868
    cmp r0,#0x1                              @ 08113b5a 0128
    bhi LAB_08113b60                         @ 08113b5c 00d8
    movs r1,#0x1    @ 08113b5e 0121
LAB_08113b60:
    cmp r1,#0x0                              @ 08113b60 0029
    bne LAB_08113bd4                         @ 08113b62 37d1
    movs r1,#0x0    @ 08113b64 0021
    cmp r2,#0x4                              @ 08113b66 042a
    bne LAB_08113b6c                         @ 08113b68 00d1
    movs r1,#0x1    @ 08113b6a 0121
LAB_08113b6c:
    cmp r1,#0x0                              @ 08113b6c 0029
    beq LAB_08113b8c                         @ 08113b6e 0dd0
    movs r1,#0x0    @ 08113b70 0021
    cmp r0,#0x4                              @ 08113b72 0428
    bne LAB_08113b78                         @ 08113b74 00d1
    movs r1,#0x1    @ 08113b76 0121
LAB_08113b78:
    cmp r1,#0x0                              @ 08113b78 0029
    beq LAB_08113b52                         @ 08113b7a ead0
    ldr r1,[r6,#0x4]                         @ 08113b7c 7168
    ldr r0,[r7,#0x4]                         @ 08113b7e 7868
    cmp r1,r0                                @ 08113b80 8142
    beq LAB_08113b52                         @ 08113b82 e6d0
    ldr r0, DAT_08113b88                     @ 08113b84 0048
    b LAB_08113cac                           @ 08113b86 91e0
DAT_08113b88:
    .word  0x03005840                     @ 08113b88 40580003
LAB_08113b8c:
    movs r1,#0x0    @ 08113b8c 0021
    cmp r0,#0x4                              @ 08113b8e 0428
    bne LAB_08113b94                         @ 08113b90 00d1
    movs r1,#0x1    @ 08113b92 0121
LAB_08113b94:
    cmp r1,#0x0                              @ 08113b94 0029
    bne LAB_08113bd4                         @ 08113b96 1dd1
    movs r1,#0x0    @ 08113b98 0021
    cmp r0,#0x2                              @ 08113b9a 0228
    bne LAB_08113ba0                         @ 08113b9c 00d1
    movs r1,#0x1    @ 08113b9e 0121
LAB_08113ba0:
    cmp r1,#0x0                              @ 08113ba0 0029
    beq LAB_08113bc6                         @ 08113ba2 10d0
    movs r0,#0x0    @ 08113ba4 0020
    cmp r2,#0x2                              @ 08113ba6 022a
    bne LAB_08113bac                         @ 08113ba8 00d1
    movs r0,#0x1    @ 08113baa 0120
LAB_08113bac:
    cmp r0,#0x0                              @ 08113bac 0028
    beq LAB_08113b52                         @ 08113bae d0d0
    adds r1,r5,#0x0    @ 08113bb0 291c
    adds r0,r6,#0x0    @ 08113bb2 301c
    ldmia r0!,{r2,r3,r4}                     @ 08113bb4 1cc8
    stmia r1!,{r2,r3,r4}                     @ 08113bb6 1cc1
    ldr r0,[r0,#0x0]                         @ 08113bb8 0068
    str r0,[r1,#0x0]                         @ 08113bba 0860
    ldr r0,[r6,#0x4]                         @ 08113bbc 7068
    ldr r1,[r7,#0x4]                         @ 08113bbe 7968
    ands r0,r1    @ 08113bc0 0840
    str r0,[r5,#0x4]                         @ 08113bc2 6860
    b LAB_08113caa                           @ 08113bc4 71e0
LAB_08113bc6:
    movs r1,#0x0    @ 08113bc6 0021
    ldr r0,[r6,#0x0]                         @ 08113bc8 3068
    cmp r0,#0x2                              @ 08113bca 0228
    bne LAB_08113bd0                         @ 08113bcc 00d1
    movs r1,#0x1    @ 08113bce 0121
LAB_08113bd0:
    cmp r1,#0x0                              @ 08113bd0 0029
    beq LAB_08113bd8                         @ 08113bd2 01d0
LAB_08113bd4:
    adds r0,r7,#0x0    @ 08113bd4 381c
    b LAB_08113cac                           @ 08113bd6 69e0
LAB_08113bd8:
    ldr r1,[r6,#0x8]                         @ 08113bd8 b168
    ldr r3,[r7,#0x8]                         @ 08113bda bb68
    ldr r2,[r6,#0xc]                         @ 08113bdc f268
    ldr r4,[r7,#0xc]                         @ 08113bde fc68
    subs r0,r1,r3    @ 08113be0 c81a
    cmp r0,#0x0                              @ 08113be2 0028
    bge LAB_08113be8                         @ 08113be4 00da
    rsbs r0,r0,#0    @ 08113be6 4042
LAB_08113be8:
    cmp r0,#0x1f                             @ 08113be8 1f28
    bgt LAB_08113c2c                         @ 08113bea 1fdc
    ldr r6,[r6,#0x4]                         @ 08113bec 7668
    ldr r7,[r7,#0x4]                         @ 08113bee 7f68
    .hword 0x46b8    @ 08113bf0 b846
    cmp r1,r3                                @ 08113bf2 9942
    ble LAB_08113c0e                         @ 08113bf4 0bdd
    movs r7,#0x1    @ 08113bf6 0127
    .hword 0x46bc    @ 08113bf8 bc46
    subs r3,r1,r3    @ 08113bfa cb1a
LAB_08113bfc:
    subs r3,#0x1    @ 08113bfc 013b
    adds r0,r4,#0x0    @ 08113bfe 201c
    .hword 0x4667    @ 08113c00 6746
    ands r0,r7    @ 08113c02 3840
    lsrs r4,r4,#0x1    @ 08113c04 6408
    orrs r4,r0    @ 08113c06 0443
    cmp r3,#0x0                              @ 08113c08 002b
    bne LAB_08113bfc                         @ 08113c0a f7d1
    adds r3,r1,#0x0    @ 08113c0c 0b1c
LAB_08113c0e:
    cmp r3,r1                                @ 08113c0e 8b42
    ble LAB_08113c3e                         @ 08113c10 15dd
    movs r0,#0x1    @ 08113c12 0120
    .hword 0x4684    @ 08113c14 8446
    subs r1,r3,r1    @ 08113c16 591a
LAB_08113c18:
    subs r1,#0x1    @ 08113c18 0139
    adds r0,r2,#0x0    @ 08113c1a 101c
    .hword 0x4667    @ 08113c1c 6746
    ands r0,r7    @ 08113c1e 3840
    lsrs r2,r2,#0x1    @ 08113c20 5208
    orrs r2,r0    @ 08113c22 0243
    cmp r1,#0x0                              @ 08113c24 0029
    bne LAB_08113c18                         @ 08113c26 f7d1
    adds r1,r3,#0x0    @ 08113c28 191c
    b LAB_08113c3e                           @ 08113c2a 08e0
LAB_08113c2c:
    cmp r1,r3                                @ 08113c2c 9942
    ble LAB_08113c34                         @ 08113c2e 01dd
    movs r4,#0x0    @ 08113c30 0024
    b LAB_08113c38                           @ 08113c32 01e0
LAB_08113c34:
    adds r1,r3,#0x0    @ 08113c34 191c
    movs r2,#0x0    @ 08113c36 0022
LAB_08113c38:
    ldr r6,[r6,#0x4]                         @ 08113c38 7668
    ldr r7,[r7,#0x4]                         @ 08113c3a 7f68
    .hword 0x46b8    @ 08113c3c b846
LAB_08113c3e:
    cmp r6,r8                                @ 08113c3e 4645
    beq LAB_08113c88                         @ 08113c40 22d0
    cmp r6,#0x0                              @ 08113c42 002e
    beq LAB_08113c4a                         @ 08113c44 01d0
    subs r3,r4,r2    @ 08113c46 a31a
    b LAB_08113c4c                           @ 08113c48 00e0
LAB_08113c4a:
    subs r3,r2,r4    @ 08113c4a 131b
LAB_08113c4c:
    cmp r3,#0x0                              @ 08113c4c 002b
    blt LAB_08113c5a                         @ 08113c4e 04db
    movs r0,#0x0    @ 08113c50 0020
    str r0,[r5,#0x4]                         @ 08113c52 6860
    str r1,[r5,#0x8]                         @ 08113c54 a960
    str r3,[r5,#0xc]                         @ 08113c56 eb60
    b LAB_08113c64                           @ 08113c58 04e0
LAB_08113c5a:
    movs r0,#0x1    @ 08113c5a 0120
    str r0,[r5,#0x4]                         @ 08113c5c 6860
    str r1,[r5,#0x8]                         @ 08113c5e a960
    rsbs r0,r3,#0    @ 08113c60 5842
    str r0,[r5,#0xc]                         @ 08113c62 e860
LAB_08113c64:
    ldr r1,[r5,#0xc]                         @ 08113c64 e968
    subs r0,r1,#0x1    @ 08113c66 481e
    ldr r2, DAT_08113c84                     @ 08113c68 064a
    cmp r0,r2                                @ 08113c6a 9042
    bhi LAB_08113c90                         @ 08113c6c 10d8
LAB_08113c6e:
    lsls r0,r1,#0x1    @ 08113c6e 4800
    str r0,[r5,#0xc]                         @ 08113c70 e860
    ldr r1,[r5,#0x8]                         @ 08113c72 a968
    subs r1,#0x1    @ 08113c74 0139
    str r1,[r5,#0x8]                         @ 08113c76 a960
    adds r1,r0,#0x0    @ 08113c78 011c
    subs r0,r1,#0x1    @ 08113c7a 481e
    cmp r0,r2                                @ 08113c7c 9042
    bls LAB_08113c6e                         @ 08113c7e f6d9
    b LAB_08113c90                           @ 08113c80 06e0
    .zero  0x2
DAT_08113c84:
    .word  0x3ffffffe                     @ 08113c84 feffff3f
LAB_08113c88:
    str r6,[r5,#0x4]                         @ 08113c88 6e60
    str r1,[r5,#0x8]                         @ 08113c8a a960
    adds r0,r2,r4    @ 08113c8c 1019
    str r0,[r5,#0xc]                         @ 08113c8e e860
LAB_08113c90:
    movs r0,#0x3    @ 08113c90 0320
    str r0,[r5,#0x0]                         @ 08113c92 2860
    ldr r1,[r5,#0xc]                         @ 08113c94 e968
    cmp r1,#0x0                              @ 08113c96 0029
    bge LAB_08113caa                         @ 08113c98 07da
    movs r0,#0x1    @ 08113c9a 0120
    ands r0,r1    @ 08113c9c 0840
    lsrs r1,r1,#0x1    @ 08113c9e 4908
    orrs r0,r1    @ 08113ca0 0843
    str r0,[r5,#0xc]                         @ 08113ca2 e860
    ldr r0,[r5,#0x8]                         @ 08113ca4 a868
    adds r0,#0x1    @ 08113ca6 0130
    str r0,[r5,#0x8]                         @ 08113ca8 a860
LAB_08113caa:
    adds r0,r5,#0x0    @ 08113caa 281c
LAB_08113cac:
    pop {r3}                                 @ 08113cac 08bc
    .hword 0x4698    @ 08113cae 9846
    pop {r4,r5,r6,r7,pc}                     @ 08113cb0 f0bd
    .zero  0x2
__addsf3:
    push {r4,lr}                             @ 08113cb4 10b5
    sub sp,#0x38                             @ 08113cb6 8eb0
    str r0,[sp,#0x30]                        @ 08113cb8 0c90
    str r1,[sp,#0x34]                        @ 08113cba 0d91
    add r0,sp,#0x30                          @ 08113cbc 0ca8
    .hword 0x4669    @ 08113cbe 6946
    bl __unpack_f                            @ 08113cc0 fff7fcfe
    add r0,sp,#0x34                          @ 08113cc4 0da8
    add r4,sp,#0x10                          @ 08113cc6 04ac
    adds r1,r4,#0x0    @ 08113cc8 211c
    bl __unpack_f                            @ 08113cca fff7f7fe
    add r2,sp,#0x20                          @ 08113cce 08aa
    .hword 0x4668    @ 08113cd0 6846
    adds r1,r4,#0x0    @ 08113cd2 211c
    bl exec_addsubsf3_core                   @ 08113cd4 fff730ff
    bl __pack_f                              @ 08113cd8 fff794fe
    add sp,#0x38                             @ 08113cdc 0eb0
    pop {r4,pc}                              @ 08113cde 10bd
__subsf3:
    push {r4,lr}                             @ 08113ce0 10b5
    sub sp,#0x38                             @ 08113ce2 8eb0
    str r0,[sp,#0x30]                        @ 08113ce4 0c90
    str r1,[sp,#0x34]                        @ 08113ce6 0d91
    add r0,sp,#0x30                          @ 08113ce8 0ca8
    .hword 0x4669    @ 08113cea 6946
    bl __unpack_f                            @ 08113cec fff7e6fe
    add r0,sp,#0x34                          @ 08113cf0 0da8
    add r4,sp,#0x10                          @ 08113cf2 04ac
    adds r1,r4,#0x0    @ 08113cf4 211c
    bl __unpack_f                            @ 08113cf6 fff7e1fe
    ldr r0,[r4,#0x4]                         @ 08113cfa 6068
    movs r1,#0x1    @ 08113cfc 0121
    eors r0,r1    @ 08113cfe 4840
    str r0,[r4,#0x4]                         @ 08113d00 6060
    add r2,sp,#0x20                          @ 08113d02 08aa
    .hword 0x4668    @ 08113d04 6846
    adds r1,r4,#0x0    @ 08113d06 211c
    bl exec_addsubsf3_core                   @ 08113d08 fff716ff
    bl __pack_f                              @ 08113d0c fff77afe
    add sp,#0x38                             @ 08113d10 0eb0
    pop {r4,pc}                              @ 08113d12 10bd
__mulsf3:
    push {r4,r5,r6,r7,lr}                    @ 08113d14 f0b5
    .hword 0x464f    @ 08113d16 4f46
    .hword 0x4646    @ 08113d18 4646
    push {r6,r7}                             @ 08113d1a c0b4
    sub sp,#0x38                             @ 08113d1c 8eb0
    str r0,[sp,#0x30]                        @ 08113d1e 0c90
    str r1,[sp,#0x34]                        @ 08113d20 0d91
    add r0,sp,#0x30                          @ 08113d22 0ca8
    .hword 0x4669    @ 08113d24 6946
    bl __unpack_f                            @ 08113d26 fff7c9fe
    add r0,sp,#0x34                          @ 08113d2a 0da8
    add r4,sp,#0x10                          @ 08113d2c 04ac
    adds r1,r4,#0x0    @ 08113d2e 211c
    bl __unpack_f                            @ 08113d30 fff7c4fe
    .hword 0x466f    @ 08113d34 6f46
    add r0,sp,#0x20                          @ 08113d36 08a8
    .hword 0x4680    @ 08113d38 8046
    movs r0,#0x0    @ 08113d3a 0020
    ldr r1,[sp,#0x0]                         @ 08113d3c 0099
    .hword 0x46c1    @ 08113d3e c146
    cmp r1,#0x1                              @ 08113d40 0129
    bhi LAB_08113d46                         @ 08113d42 00d8
    movs r0,#0x1    @ 08113d44 0120
LAB_08113d46:
    cmp r0,#0x0                              @ 08113d46 0028
    bne LAB_08113da4                         @ 08113d48 2cd1
    movs r2,#0x0    @ 08113d4a 0022
    ldr r0,[sp,#0x10]                        @ 08113d4c 0498
    cmp r0,#0x1                              @ 08113d4e 0128
    bhi LAB_08113d54                         @ 08113d50 00d8
    movs r2,#0x1    @ 08113d52 0122
LAB_08113d54:
    cmp r2,#0x0                              @ 08113d54 002a
    beq LAB_08113d5c                         @ 08113d56 01d0
    ldr r0,[sp,#0x4]                         @ 08113d58 0198
    b LAB_08113dc4                           @ 08113d5a 33e0
LAB_08113d5c:
    movs r2,#0x0    @ 08113d5c 0022
    cmp r1,#0x4                              @ 08113d5e 0429
    bne LAB_08113d64                         @ 08113d60 00d1
    movs r2,#0x1    @ 08113d62 0122
LAB_08113d64:
    cmp r2,#0x0                              @ 08113d64 002a
    beq LAB_08113d76                         @ 08113d66 06d0
    movs r1,#0x0    @ 08113d68 0021
    cmp r0,#0x2                              @ 08113d6a 0228
    bne LAB_08113d70                         @ 08113d6c 00d1
    movs r1,#0x1    @ 08113d6e 0121
LAB_08113d70:
    cmp r1,#0x0                              @ 08113d70 0029
    bne LAB_08113d8e                         @ 08113d72 0cd1
    b LAB_08113da4                           @ 08113d74 16e0
LAB_08113d76:
    movs r2,#0x0    @ 08113d76 0022
    cmp r0,#0x4                              @ 08113d78 0428
    bne LAB_08113d7e                         @ 08113d7a 00d1
    movs r2,#0x1    @ 08113d7c 0122
LAB_08113d7e:
    cmp r2,#0x0                              @ 08113d7e 002a
    beq LAB_08113d98                         @ 08113d80 0ad0
    movs r0,#0x0    @ 08113d82 0020
    cmp r1,#0x2                              @ 08113d84 0229
    bne LAB_08113d8a                         @ 08113d86 00d1
    movs r0,#0x1    @ 08113d88 0120
LAB_08113d8a:
    cmp r0,#0x0                              @ 08113d8a 0028
    beq LAB_08113dc2                         @ 08113d8c 19d0
LAB_08113d8e:
    ldr r0, DAT_08113d94                     @ 08113d8e 0148
    b LAB_08113e66                           @ 08113d90 69e0
    .zero  0x2
DAT_08113d94:
    .word  0x03005840                     @ 08113d94 40580003
LAB_08113d98:
    movs r2,#0x0    @ 08113d98 0022
    cmp r1,#0x2                              @ 08113d9a 0229
    bne LAB_08113da0                         @ 08113d9c 00d1
    movs r2,#0x1    @ 08113d9e 0122
LAB_08113da0:
    cmp r2,#0x0                              @ 08113da0 002a
    beq LAB_08113db6                         @ 08113da2 08d0
LAB_08113da4:
    ldr r0,[sp,#0x4]                         @ 08113da4 0198
    ldr r1,[sp,#0x14]                        @ 08113da6 0599
    eors r0,r1    @ 08113da8 4840
    rsbs r1,r0,#0    @ 08113daa 4142
    orrs r1,r0    @ 08113dac 0143
    lsrs r1,r1,#0x1f    @ 08113dae c90f
    str r1,[sp,#0x4]                         @ 08113db0 0191
    .hword 0x4668    @ 08113db2 6846
    b LAB_08113e66                           @ 08113db4 57e0
LAB_08113db6:
    movs r1,#0x0    @ 08113db6 0021
    cmp r0,#0x2                              @ 08113db8 0228
    bne LAB_08113dbe                         @ 08113dba 00d1
    movs r1,#0x1    @ 08113dbc 0121
LAB_08113dbe:
    cmp r1,#0x0                              @ 08113dbe 0029
    beq LAB_08113dd4                         @ 08113dc0 08d0
LAB_08113dc2:
    ldr r0,[r7,#0x4]                         @ 08113dc2 7868
LAB_08113dc4:
    ldr r1,[sp,#0x14]                        @ 08113dc4 0599
    eors r0,r1    @ 08113dc6 4840
    rsbs r1,r0,#0    @ 08113dc8 4142
    orrs r1,r0    @ 08113dca 0143
    lsrs r1,r1,#0x1f    @ 08113dcc c90f
    str r1,[sp,#0x14]                        @ 08113dce 0591
    adds r0,r4,#0x0    @ 08113dd0 201c
    b LAB_08113e66                           @ 08113dd2 48e0
LAB_08113dd4:
    ldr r0,[r7,#0xc]                         @ 08113dd4 f868
    movs r1,#0x0    @ 08113dd6 0021
    ldr r2,[sp,#0x1c]                        @ 08113dd8 079a
    movs r3,#0x0    @ 08113dda 0023
    bl __muldi3                              @ 08113ddc faf7c6fc
    adds r2,r1,#0x0    @ 08113de0 0a1c
    adds r5,r2,#0x0    @ 08113de2 151c
    adds r6,r0,#0x0    @ 08113de4 061c
    ldr r4,[r7,#0x8]                         @ 08113de6 bc68
    ldr r0,[sp,#0x18]                        @ 08113de8 0698
    adds r4,r4,r0    @ 08113dea 2418
    str r4,[sp,#0x28]                        @ 08113dec 0a94
    ldr r1,[r7,#0x4]                         @ 08113dee 7968
    ldr r0,[sp,#0x14]                        @ 08113df0 0598
    eors r1,r0    @ 08113df2 4140
    rsbs r0,r1,#0    @ 08113df4 4842
    orrs r0,r1    @ 08113df6 0843
    lsrs r0,r0,#0x1f    @ 08113df8 c00f
    str r0,[sp,#0x24]                        @ 08113dfa 0990
    adds r4,#0x2    @ 08113dfc 0234
    str r4,[sp,#0x28]                        @ 08113dfe 0a94
    cmp r2,#0x0                              @ 08113e00 002a
    bge LAB_08113e20                         @ 08113e02 0dda
    movs r2,#0x1    @ 08113e04 0122
    movs r1,#0x80    @ 08113e06 8021
    lsls r1,r1,#0x18    @ 08113e08 0906
LAB_08113e0a:
    adds r4,#0x1    @ 08113e0a 0134
    adds r0,r5,#0x0    @ 08113e0c 281c
    ands r0,r2    @ 08113e0e 1040
    cmp r0,#0x0                              @ 08113e10 0028
    beq LAB_08113e18                         @ 08113e12 01d0
    lsrs r6,r6,#0x1    @ 08113e14 7608
    orrs r6,r1    @ 08113e16 0e43
LAB_08113e18:
    lsrs r5,r5,#0x1    @ 08113e18 6d08
    cmp r5,#0x0                              @ 08113e1a 002d
    blt LAB_08113e0a                         @ 08113e1c f5db
    str r4,[sp,#0x28]                        @ 08113e1e 0a94
LAB_08113e20:
    ldr r0, DAT_08113e74                     @ 08113e20 1448
    cmp r5,r0                                @ 08113e22 8542
    bhi LAB_08113e46                         @ 08113e24 0fd8
    movs r4,#0x80    @ 08113e26 8024
    lsls r4,r4,#0x18    @ 08113e28 2406
    movs r3,#0x1    @ 08113e2a 0123
    adds r2,r0,#0x0    @ 08113e2c 021c
    ldr r1,[sp,#0x28]                        @ 08113e2e 0a99
LAB_08113e30:
    subs r1,#0x1    @ 08113e30 0139
    lsls r5,r5,#0x1    @ 08113e32 6d00
    adds r0,r6,#0x0    @ 08113e34 301c
    ands r0,r4    @ 08113e36 2040
    cmp r0,#0x0                              @ 08113e38 0028
    beq LAB_08113e3e                         @ 08113e3a 00d0
    orrs r5,r3    @ 08113e3c 1d43
LAB_08113e3e:
    lsls r6,r6,#0x1    @ 08113e3e 7600
    cmp r5,r2                                @ 08113e40 9542
    bls LAB_08113e30                         @ 08113e42 f5d9
    str r1,[sp,#0x28]                        @ 08113e44 0a91
LAB_08113e46:
    movs r0,#0x7f    @ 08113e46 7f20
    ands r0,r5    @ 08113e48 2840
    cmp r0,#0x40                             @ 08113e4a 4028
    bne LAB_08113e5c                         @ 08113e4c 06d1
    movs r0,#0x80    @ 08113e4e 8020
    ands r0,r5    @ 08113e50 2840
    cmp r0,#0x0                              @ 08113e52 0028
    bne LAB_08113e5a                         @ 08113e54 01d1
    cmp r6,#0x0                              @ 08113e56 002e
    beq LAB_08113e5c                         @ 08113e58 00d0
LAB_08113e5a:
    adds r5,#0x40    @ 08113e5a 4035
LAB_08113e5c:
    str r5,[sp,#0x2c]                        @ 08113e5c 0b95
    movs r0,#0x3    @ 08113e5e 0320
    .hword 0x4641    @ 08113e60 4146
    str r0,[r1,#0x0]                         @ 08113e62 0860
    .hword 0x4648    @ 08113e64 4846
LAB_08113e66:
    bl __pack_f                              @ 08113e66 fff7cdfd
    add sp,#0x38                             @ 08113e6a 0eb0
    pop {r3,r4}                              @ 08113e6c 18bc
    .hword 0x4698    @ 08113e6e 9846
    .hword 0x46a1    @ 08113e70 a146
    pop {r4,r5,r6,r7,pc}                     @ 08113e72 f0bd
DAT_08113e74:
    .word  0x3fffffff                     @ 08113e74 ffffff3f
__divsf3:
    push {r4,r5,r6,lr}                       @ 08113e78 70b5
    sub sp,#0x28                             @ 08113e7a 8ab0
    str r0,[sp,#0x20]                        @ 08113e7c 0890
    str r1,[sp,#0x24]                        @ 08113e7e 0991
    add r0,sp,#0x20                          @ 08113e80 08a8
    .hword 0x4669    @ 08113e82 6946
    bl __unpack_f                            @ 08113e84 fff71afe
    add r0,sp,#0x24                          @ 08113e88 09a8
    add r5,sp,#0x10                          @ 08113e8a 04ad
    adds r1,r5,#0x0    @ 08113e8c 291c
    bl __unpack_f                            @ 08113e8e fff715fe
    .hword 0x466c    @ 08113e92 6c46
    movs r0,#0x0    @ 08113e94 0020
    ldr r3,[sp,#0x0]                         @ 08113e96 009b
    cmp r3,#0x1                              @ 08113e98 012b
    bhi LAB_08113e9e                         @ 08113e9a 00d8
    movs r0,#0x1    @ 08113e9c 0120
LAB_08113e9e:
    cmp r0,#0x0                              @ 08113e9e 0028
    beq LAB_08113ea6                         @ 08113ea0 01d0
    .hword 0x4669    @ 08113ea2 6946
    b LAB_08113f58                           @ 08113ea4 58e0
LAB_08113ea6:
    movs r0,#0x0    @ 08113ea6 0020
    ldr r2,[sp,#0x10]                        @ 08113ea8 049a
    adds r6,r2,#0x0    @ 08113eaa 161c
    cmp r2,#0x1                              @ 08113eac 012a
    bhi LAB_08113eb2                         @ 08113eae 00d8
    movs r0,#0x1    @ 08113eb0 0120
LAB_08113eb2:
    cmp r0,#0x0                              @ 08113eb2 0028
    beq LAB_08113eba                         @ 08113eb4 01d0
    adds r1,r5,#0x0    @ 08113eb6 291c
    b LAB_08113f58                           @ 08113eb8 4ee0
LAB_08113eba:
    ldr r0,[sp,#0x4]                         @ 08113eba 0198
    ldr r1,[sp,#0x14]                        @ 08113ebc 0599
    eors r0,r1    @ 08113ebe 4840
    str r0,[sp,#0x4]                         @ 08113ec0 0190
    movs r0,#0x0    @ 08113ec2 0020
    cmp r3,#0x4                              @ 08113ec4 042b
    bne LAB_08113eca                         @ 08113ec6 00d1
    movs r0,#0x1    @ 08113ec8 0120
LAB_08113eca:
    cmp r0,#0x0                              @ 08113eca 0028
    bne LAB_08113eda                         @ 08113ecc 05d1
    movs r0,#0x0    @ 08113ece 0020
    cmp r3,#0x2                              @ 08113ed0 022b
    bne LAB_08113ed6                         @ 08113ed2 00d1
    movs r0,#0x1    @ 08113ed4 0120
LAB_08113ed6:
    cmp r0,#0x0                              @ 08113ed6 0028
    beq LAB_08113eec                         @ 08113ed8 08d0
LAB_08113eda:
    ldr r0,[r4,#0x0]                         @ 08113eda 2068
    adds r1,r4,#0x0    @ 08113edc 211c
    cmp r0,r6                                @ 08113ede b042
    bne LAB_08113f58                         @ 08113ee0 3ad1
    ldr r1, DAT_08113ee8                     @ 08113ee2 0149
    b LAB_08113f58                           @ 08113ee4 38e0
    .zero  0x2
DAT_08113ee8:
    .word  0x03005840                     @ 08113ee8 40580003
LAB_08113eec:
    movs r1,#0x0    @ 08113eec 0021
    cmp r2,#0x4                              @ 08113eee 042a
    bne LAB_08113ef4                         @ 08113ef0 00d1
    movs r1,#0x1    @ 08113ef2 0121
LAB_08113ef4:
    cmp r1,#0x0                              @ 08113ef4 0029
    beq LAB_08113f00                         @ 08113ef6 03d0
    str r0,[sp,#0xc]                         @ 08113ef8 0390
    str r0,[sp,#0x8]                         @ 08113efa 0290
    .hword 0x4669    @ 08113efc 6946
    b LAB_08113f58                           @ 08113efe 2be0
LAB_08113f00:
    movs r0,#0x0    @ 08113f00 0020
    cmp r2,#0x2                              @ 08113f02 022a
    bne LAB_08113f08                         @ 08113f04 00d1
    movs r0,#0x1    @ 08113f06 0120
LAB_08113f08:
    cmp r0,#0x0                              @ 08113f08 0028
    beq LAB_08113f12                         @ 08113f0a 02d0
    movs r0,#0x4    @ 08113f0c 0420
    str r0,[r4,#0x0]                         @ 08113f0e 2060
    b LAB_08113f56                           @ 08113f10 21e0
LAB_08113f12:
    ldr r1,[r4,#0x8]                         @ 08113f12 a168
    ldr r0,[sp,#0x18]                        @ 08113f14 0698
    subs r0,r1,r0    @ 08113f16 081a
    str r0,[r4,#0x8]                         @ 08113f18 a060
    ldr r2,[r4,#0xc]                         @ 08113f1a e268
    ldr r3,[sp,#0x1c]                        @ 08113f1c 079b
    cmp r2,r3                                @ 08113f1e 9a42
    bcs LAB_08113f28                         @ 08113f20 02d2
    lsls r2,r2,#0x1    @ 08113f22 5200
    subs r0,#0x1    @ 08113f24 0138
    str r0,[r4,#0x8]                         @ 08113f26 a060
LAB_08113f28:
    movs r0,#0x80    @ 08113f28 8020
    lsls r0,r0,#0x17    @ 08113f2a c005
    movs r1,#0x0    @ 08113f2c 0021
LAB_08113f2e:
    cmp r2,r3                                @ 08113f2e 9a42
    bcc LAB_08113f36                         @ 08113f30 01d3
    orrs r1,r0    @ 08113f32 0143
    subs r2,r2,r3    @ 08113f34 d21a
LAB_08113f36:
    lsrs r0,r0,#0x1    @ 08113f36 4008
    lsls r2,r2,#0x1    @ 08113f38 5200
    cmp r0,#0x0                              @ 08113f3a 0028
    bne LAB_08113f2e                         @ 08113f3c f7d1
    movs r0,#0x7f    @ 08113f3e 7f20
    ands r0,r1    @ 08113f40 0840
    cmp r0,#0x40                             @ 08113f42 4028
    bne LAB_08113f54                         @ 08113f44 06d1
    movs r0,#0x80    @ 08113f46 8020
    ands r0,r1    @ 08113f48 0840
    cmp r0,#0x0                              @ 08113f4a 0028
    bne LAB_08113f52                         @ 08113f4c 01d1
    cmp r2,#0x0                              @ 08113f4e 002a
    beq LAB_08113f54                         @ 08113f50 00d0
LAB_08113f52:
    adds r1,#0x40    @ 08113f52 4031
LAB_08113f54:
    str r1,[r4,#0xc]                         @ 08113f54 e160
LAB_08113f56:
    adds r1,r4,#0x0    @ 08113f56 211c
LAB_08113f58:
    adds r0,r1,#0x0    @ 08113f58 081c
    bl __pack_f                              @ 08113f5a fff753fd
    add sp,#0x28                             @ 08113f5e 0ab0
    pop {r4,r5,r6,pc}                        @ 08113f60 70bd
    .zero  0x2
__fpcmp_parts_f:
    push {r4,lr}                             @ 08113f64 10b5
    adds r4,r0,#0x0    @ 08113f66 041c
    movs r0,#0x0    @ 08113f68 0020
    ldr r2,[r4,#0x0]                         @ 08113f6a 2268
    cmp r2,#0x1                              @ 08113f6c 012a
    bhi LAB_08113f72                         @ 08113f6e 00d8
    movs r0,#0x1    @ 08113f70 0120
LAB_08113f72:
    cmp r0,#0x0                              @ 08113f72 0028
    bne LAB_08113f84                         @ 08113f74 06d1
    movs r0,#0x0    @ 08113f76 0020
    ldr r3,[r1,#0x0]                         @ 08113f78 0b68
    cmp r3,#0x1                              @ 08113f7a 012b
    bhi LAB_08113f80                         @ 08113f7c 00d8
    movs r0,#0x1    @ 08113f7e 0120
LAB_08113f80:
    cmp r0,#0x0                              @ 08113f80 0028
    beq LAB_08113f88                         @ 08113f82 01d0
LAB_08113f84:
    movs r0,#0x1    @ 08113f84 0120
    b LAB_08114046                           @ 08113f86 5ee0
LAB_08113f88:
    movs r0,#0x0    @ 08113f88 0020
    cmp r2,#0x4                              @ 08113f8a 042a
    bne LAB_08113f90                         @ 08113f8c 00d1
    movs r0,#0x1    @ 08113f8e 0120
LAB_08113f90:
    cmp r0,#0x0                              @ 08113f90 0028
    beq LAB_08113fa8                         @ 08113f92 09d0
    movs r0,#0x0    @ 08113f94 0020
    cmp r3,#0x4                              @ 08113f96 042b
    bne LAB_08113f9c                         @ 08113f98 00d1
    movs r0,#0x1    @ 08113f9a 0120
LAB_08113f9c:
    cmp r0,#0x0                              @ 08113f9c 0028
    beq LAB_08113fa8                         @ 08113f9e 03d0
    ldr r0,[r1,#0x4]                         @ 08113fa0 4868
    ldr r1,[r4,#0x4]                         @ 08113fa2 6168
    subs r0,r0,r1    @ 08113fa4 401a
    b LAB_08114046                           @ 08113fa6 4ee0
LAB_08113fa8:
    movs r2,#0x0    @ 08113fa8 0022
    ldr r0,[r4,#0x0]                         @ 08113faa 2068
    cmp r0,#0x4                              @ 08113fac 0428
    bne LAB_08113fb2                         @ 08113fae 00d1
    movs r2,#0x1    @ 08113fb0 0122
LAB_08113fb2:
    cmp r2,#0x0                              @ 08113fb2 002a
    bne LAB_08114000                         @ 08113fb4 24d1
    movs r2,#0x0    @ 08113fb6 0022
    cmp r3,#0x4                              @ 08113fb8 042b
    bne LAB_08113fbe                         @ 08113fba 00d1
    movs r2,#0x1    @ 08113fbc 0122
LAB_08113fbe:
    cmp r2,#0x0                              @ 08113fbe 002a
    beq LAB_08113fd0                         @ 08113fc0 06d0
LAB_08113fc2:
    ldr r0,[r1,#0x4]                         @ 08113fc2 4868
    movs r1,#0x1    @ 08113fc4 0121
    rsbs r1,r1,#0    @ 08113fc6 4942
    cmp r0,#0x0                              @ 08113fc8 0028
    beq LAB_0811400a                         @ 08113fca 1ed0
    movs r1,#0x1    @ 08113fcc 0121
    b LAB_0811400a                           @ 08113fce 1ce0
LAB_08113fd0:
    movs r2,#0x0    @ 08113fd0 0022
    cmp r0,#0x2                              @ 08113fd2 0228
    bne LAB_08113fd8                         @ 08113fd4 00d1
    movs r2,#0x1    @ 08113fd6 0122
LAB_08113fd8:
    cmp r2,#0x0                              @ 08113fd8 002a
    beq LAB_08113fe8                         @ 08113fda 05d0
    movs r2,#0x0    @ 08113fdc 0022
    cmp r3,#0x2                              @ 08113fde 022b
    bne LAB_08113fe4                         @ 08113fe0 00d1
    movs r2,#0x1    @ 08113fe2 0122
LAB_08113fe4:
    cmp r2,#0x0                              @ 08113fe4 002a
    bne LAB_08114044                         @ 08113fe6 2dd1
LAB_08113fe8:
    movs r2,#0x0    @ 08113fe8 0022
    cmp r0,#0x2                              @ 08113fea 0228
    bne LAB_08113ff0                         @ 08113fec 00d1
    movs r2,#0x1    @ 08113fee 0122
LAB_08113ff0:
    cmp r2,#0x0                              @ 08113ff0 002a
    bne LAB_08113fc2                         @ 08113ff2 e6d1
    movs r0,#0x0    @ 08113ff4 0020
    cmp r3,#0x2                              @ 08113ff6 022b
    bne LAB_08113ffc                         @ 08113ff8 00d1
    movs r0,#0x1    @ 08113ffa 0120
LAB_08113ffc:
    cmp r0,#0x0                              @ 08113ffc 0028
    beq LAB_0811400e                         @ 08113ffe 06d0
LAB_08114000:
    ldr r0,[r4,#0x4]                         @ 08114000 6068
    movs r1,#0x1    @ 08114002 0121
    cmp r0,#0x0                              @ 08114004 0028
    beq LAB_0811400a                         @ 08114006 00d0
    subs r1,#0x2    @ 08114008 0239
LAB_0811400a:
    adds r0,r1,#0x0    @ 0811400a 081c
    b LAB_08114046                           @ 0811400c 1be0
LAB_0811400e:
    ldr r3,[r4,#0x4]                         @ 0811400e 6368
    ldr r0,[r1,#0x4]                         @ 08114010 4868
    cmp r3,r0                                @ 08114012 8342
    beq LAB_08114020                         @ 08114014 04d0
LAB_08114016:
    movs r0,#0x1    @ 08114016 0120
    cmp r3,#0x0                              @ 08114018 002b
    beq LAB_08114046                         @ 0811401a 14d0
    subs r0,#0x2    @ 0811401c 0238
    b LAB_08114046                           @ 0811401e 12e0
LAB_08114020:
    ldr r2,[r4,#0x8]                         @ 08114020 a268
    ldr r0,[r1,#0x8]                         @ 08114022 8868
    cmp r2,r0                                @ 08114024 8242
    bgt LAB_08114016                         @ 08114026 f6dc
    cmp r2,r0                                @ 08114028 8242
    bge LAB_08114038                         @ 0811402a 05da
LAB_0811402c:
    movs r0,#0x1    @ 0811402c 0120
    rsbs r0,r0,#0    @ 0811402e 4042
    cmp r3,#0x0                              @ 08114030 002b
    beq LAB_08114046                         @ 08114032 08d0
    movs r0,#0x1    @ 08114034 0120
    b LAB_08114046                           @ 08114036 06e0
LAB_08114038:
    ldr r0,[r4,#0xc]                         @ 08114038 e068
    ldr r1,[r1,#0xc]                         @ 0811403a c968
    cmp r0,r1                                @ 0811403c 8842
    bhi LAB_08114016                         @ 0811403e ead8
    cmp r0,r1                                @ 08114040 8842
    bcc LAB_0811402c                         @ 08114042 f3d3
LAB_08114044:
    movs r0,#0x0    @ 08114044 0020
LAB_08114046:
    pop {r4,pc}                              @ 08114046 10bd
__cmpsf2:
    push {r4,lr}                             @ 08114048 10b5
    sub sp,#0x28                             @ 0811404a 8ab0
    str r0,[sp,#0x20]                        @ 0811404c 0890
    str r1,[sp,#0x24]                        @ 0811404e 0991
    add r0,sp,#0x20                          @ 08114050 08a8
    .hword 0x4669    @ 08114052 6946
    bl __unpack_f                            @ 08114054 fff732fd
    add r0,sp,#0x24                          @ 08114058 09a8
    add r4,sp,#0x10                          @ 0811405a 04ac
    adds r1,r4,#0x0    @ 0811405c 211c
    bl __unpack_f                            @ 0811405e fff72dfd
    .hword 0x4668    @ 08114062 6846
    adds r1,r4,#0x0    @ 08114064 211c
    bl __fpcmp_parts_f                       @ 08114066 fff77dff
    add sp,#0x28                             @ 0811406a 0ab0
    pop {r4,pc}                              @ 0811406c 10bd
    .zero  0x2

@ GCC libgcc single-precision float equal comparison (__eqsf2): unpacks two floats (r0, r1) then checks NaN (kind > 1 -> returns 1 = not-equal), normal path calls __fpcmp_parts_f and returns comparison result.
@ GCC __eqsf2 contract: 0 = A==B, nonzero = A!=B or NaN. Caller pattern: bl compare_float_eq; cmp r0,#0; bne not_equal.
@ indeg=0 in static callgraph: grep ".word 0x08114071" asm/all.s -> no hits; dead code (compiler-generated __eqsf2 not directly called in this ROM).
@ Symmetric with compare_double_eq (0x081136b8); differs only in precision (__unpack_f vs __unpack_d, __fpcmp_parts_f vs __fpcmp_parts_d, r0/r1 only).
compare_float_eq:
    push {r4,lr}                             @ 08114070 10b5
    sub sp,#0x28                             @ 08114072 8ab0
    str r0,[sp,#0x20]                        @ 08114074 0890
    str r1,[sp,#0x24]                        @ 08114076 0991
    add r0,sp,#0x20                          @ 08114078 08a8
    .hword 0x4669    @ 0811407a 6946
    bl __unpack_f                            @ 0811407c fff71efd
    add r0,sp,#0x24                          @ 08114080 09a8
    add r4,sp,#0x10                          @ 08114082 04ac
    adds r1,r4,#0x0    @ 08114084 211c
    bl __unpack_f                            @ 08114086 fff719fd
    movs r1,#0x0    @ 0811408a 0021
    ldr r0,[sp,#0x0]                         @ 0811408c 0098
    cmp r0,#0x1                              @ 0811408e 0128
    bhi LAB_08114094                         @ 08114090 00d8
    movs r1,#0x1    @ 08114092 0121
LAB_08114094:
    cmp r1,#0x0                              @ 08114094 0029
    bne LAB_081140a6                         @ 08114096 06d1
    movs r1,#0x0    @ 08114098 0021
    ldr r0,[sp,#0x10]                        @ 0811409a 0498
    cmp r0,#0x1                              @ 0811409c 0128
    bhi LAB_081140a2                         @ 0811409e 00d8
    movs r1,#0x1    @ 081140a0 0121
LAB_081140a2:
    cmp r1,#0x0                              @ 081140a2 0029
    beq LAB_081140aa                         @ 081140a4 01d0
LAB_081140a6:
    movs r0,#0x1    @ 081140a6 0120
    b LAB_081140b2                           @ 081140a8 03e0
LAB_081140aa:
    .hword 0x4668    @ 081140aa 6846
    adds r1,r4,#0x0    @ 081140ac 211c
    bl __fpcmp_parts_f                       @ 081140ae fff759ff
LAB_081140b2:
    add sp,#0x28                             @ 081140b2 0ab0
    pop {r4,pc}                              @ 081140b4 10bd
    .zero  0x2

@ GCC libgcc single-precision float not-equal comparison (__nesf2): same structure as compare_float_eq (0x08114070); unpacks two floats, checks NaN (kind > 1 -> returns 1), normal path calls __fpcmp_parts_f.
@ GCC __nesf2 contract: nonzero = not-equal (semantically same return value as __eqsf2; caller uses beq/bne to select behavior).
@ indeg=0 in static callgraph: grep ".word 0x081140b9" asm/all.s -> no hits; dead code (compiler-generated __nesf2 not directly called in this ROM).
compare_float_ne:
    push {r4,lr}                             @ 081140b8 10b5
    sub sp,#0x28                             @ 081140ba 8ab0
    str r0,[sp,#0x20]                        @ 081140bc 0890
    str r1,[sp,#0x24]                        @ 081140be 0991
    add r0,sp,#0x20                          @ 081140c0 08a8
    .hword 0x4669    @ 081140c2 6946
    bl __unpack_f                            @ 081140c4 fff7fafc
    add r0,sp,#0x24                          @ 081140c8 09a8
    add r4,sp,#0x10                          @ 081140ca 04ac
    adds r1,r4,#0x0    @ 081140cc 211c
    bl __unpack_f                            @ 081140ce fff7f5fc
    movs r1,#0x0    @ 081140d2 0021
    ldr r0,[sp,#0x0]                         @ 081140d4 0098
    cmp r0,#0x1                              @ 081140d6 0128
    bhi LAB_081140dc                         @ 081140d8 00d8
    movs r1,#0x1    @ 081140da 0121
LAB_081140dc:
    cmp r1,#0x0                              @ 081140dc 0029
    bne LAB_081140ee                         @ 081140de 06d1
    movs r1,#0x0    @ 081140e0 0021
    ldr r0,[sp,#0x10]                        @ 081140e2 0498
    cmp r0,#0x1                              @ 081140e4 0128
    bhi LAB_081140ea                         @ 081140e6 00d8
    movs r1,#0x1    @ 081140e8 0121
LAB_081140ea:
    cmp r1,#0x0                              @ 081140ea 0029
    beq LAB_081140f2                         @ 081140ec 01d0
LAB_081140ee:
    movs r0,#0x1    @ 081140ee 0120
    b LAB_081140fa                           @ 081140f0 03e0
LAB_081140f2:
    .hword 0x4668    @ 081140f2 6846
    adds r1,r4,#0x0    @ 081140f4 211c
    bl __fpcmp_parts_f                       @ 081140f6 fff735ff
LAB_081140fa:
    add sp,#0x28                             @ 081140fa 0ab0
    pop {r4,pc}                              @ 081140fc 10bd
    .zero  0x2

@ GCC libgcc single-precision float greater-than comparison (__gtsf2): unpacks two floats (r0, r1), checks NaN; NaN path executes rsbs r0,r0,#0 -> returns -1 (unordered, does not satisfy >), normal path calls __fpcmp_parts_f.
@ GCC __gtsf2 contract: positive = A>B, zero or negative = A<=B or NaN. Caller pattern: bl compare_float_gt; cmp r0,#0; ble not_greater.
@ indeg=0 in static callgraph: grep ".word 0x08114101" asm/all.s -> no hits; dead code (compiler-generated __gtsf2 not directly called in this ROM).
@ Symmetric with compare_double_gt (0x08113750); rsbs (NaN -> -1) is the key distinction from eq/ne/lt/le (which return +1 for NaN).
compare_float_gt:
    push {r4,lr}                             @ 08114100 10b5
    sub sp,#0x28                             @ 08114102 8ab0
    str r0,[sp,#0x20]                        @ 08114104 0890
    str r1,[sp,#0x24]                        @ 08114106 0991
    add r0,sp,#0x20                          @ 08114108 08a8
    .hword 0x4669    @ 0811410a 6946
    bl __unpack_f                            @ 0811410c fff7d6fc
    add r0,sp,#0x24                          @ 08114110 09a8
    add r4,sp,#0x10                          @ 08114112 04ac
    adds r1,r4,#0x0    @ 08114114 211c
    bl __unpack_f                            @ 08114116 fff7d1fc
    movs r1,#0x0    @ 0811411a 0021
    ldr r0,[sp,#0x0]                         @ 0811411c 0098
    cmp r0,#0x1                              @ 0811411e 0128
    bhi LAB_08114124                         @ 08114120 00d8
    movs r1,#0x1    @ 08114122 0121
LAB_08114124:
    cmp r1,#0x0                              @ 08114124 0029
    bne LAB_08114136                         @ 08114126 06d1
    movs r1,#0x0    @ 08114128 0021
    ldr r0,[sp,#0x10]                        @ 0811412a 0498
    cmp r0,#0x1                              @ 0811412c 0128
    bhi LAB_08114132                         @ 0811412e 00d8
    movs r1,#0x1    @ 08114130 0121
LAB_08114132:
    cmp r1,#0x0                              @ 08114132 0029
    beq LAB_0811413c                         @ 08114134 02d0
LAB_08114136:
    movs r0,#0x1    @ 08114136 0120
    rsbs r0,r0,#0    @ 08114138 4042
    b LAB_08114144                           @ 0811413a 03e0
LAB_0811413c:
    .hword 0x4668    @ 0811413c 6846
    adds r1,r4,#0x0    @ 0811413e 211c
    bl __fpcmp_parts_f                       @ 08114140 fff710ff
LAB_08114144:
    add sp,#0x28                             @ 08114144 0ab0
    pop {r4,pc}                              @ 08114146 10bd

@ GCC libgcc single-precision float greater-or-equal comparison (__gesf2): unpacks two floats (r0, r1), checks NaN; NaN path executes rsbs r0,r0,#0 -> returns -1 (unordered, does not satisfy >=), normal path calls __fpcmp_parts_f.
@ GCC __gesf2 contract: >=0 = A>=B, negative = A<B or NaN. Caller pattern: bl compare_float_ge; cmp r0,#0; blt not_ge.
@ indeg=0 in static callgraph: grep ".word 0x08114149" asm/all.s -> no hits; dead code (compiler-generated __gesf2 not directly called in this ROM).
@ Symmetric with compare_double_ge (0x0811379c); same rsbs NaN->-1 as compare_float_gt (0x08114100); 4th of 6 float comparison functions (eq/ne/gt/ge/lt/le order).
compare_float_ge:
    push {r4,lr}                             @ 08114148 10b5
    sub sp,#0x28                             @ 0811414a 8ab0
    str r0,[sp,#0x20]                        @ 0811414c 0890
    str r1,[sp,#0x24]                        @ 0811414e 0991
    add r0,sp,#0x20                          @ 08114150 08a8
    .hword 0x4669    @ 08114152 6946
    bl __unpack_f                            @ 08114154 fff7b2fc
    add r0,sp,#0x24                          @ 08114158 09a8
    add r4,sp,#0x10                          @ 0811415a 04ac
    adds r1,r4,#0x0    @ 0811415c 211c
    bl __unpack_f                            @ 0811415e fff7adfc
    movs r1,#0x0    @ 08114162 0021
    ldr r0,[sp,#0x0]                         @ 08114164 0098
    cmp r0,#0x1                              @ 08114166 0128
    bhi LAB_0811416c                         @ 08114168 00d8
    movs r1,#0x1    @ 0811416a 0121
LAB_0811416c:
    cmp r1,#0x0                              @ 0811416c 0029
    bne LAB_0811417e                         @ 0811416e 06d1
    movs r1,#0x0    @ 08114170 0021
    ldr r0,[sp,#0x10]                        @ 08114172 0498
    cmp r0,#0x1                              @ 08114174 0128
    bhi LAB_0811417a                         @ 08114176 00d8
    movs r1,#0x1    @ 08114178 0121
LAB_0811417a:
    cmp r1,#0x0                              @ 0811417a 0029
    beq LAB_08114184                         @ 0811417c 02d0
LAB_0811417e:
    movs r0,#0x1    @ 0811417e 0120
    rsbs r0,r0,#0    @ 08114180 4042
    b LAB_0811418c                           @ 08114182 03e0
LAB_08114184:
    .hword 0x4668    @ 08114184 6846
    adds r1,r4,#0x0    @ 08114186 211c
    bl __fpcmp_parts_f                       @ 08114188 fff7ecfe
LAB_0811418c:
    add sp,#0x28                             @ 0811418c 0ab0
    pop {r4,pc}                              @ 0811418e 10bd

@ GCC libgcc single-precision float less-than comparison (__ltsf2): unpacks two floats (r0, r1), checks NaN (kind > 1 -> returns +1 = unordered, does not satisfy <), normal path calls __fpcmp_parts_f.
@ GCC __ltsf2 contract: negative = A<B, >=0 = A>=B or NaN. Caller pattern: bl compare_float_lt; cmp r0,#0; bge not_less.
@ indeg=0 in static callgraph: grep ".word 0x08114191" asm/all.s -> no hits; dead code (compiler-generated __ltsf2 not directly called in this ROM).
@ Symmetric with compare_double_lt (0x081137e8); NaN returns +1 (no rsbs); 5th of 6 float comparison functions.
compare_float_lt:
    push {r4,lr}                             @ 08114190 10b5
    sub sp,#0x28                             @ 08114192 8ab0
    str r0,[sp,#0x20]                        @ 08114194 0890
    str r1,[sp,#0x24]                        @ 08114196 0991
    add r0,sp,#0x20                          @ 08114198 08a8
    .hword 0x4669    @ 0811419a 6946
    bl __unpack_f                            @ 0811419c fff78efc
    add r0,sp,#0x24                          @ 081141a0 09a8
    add r4,sp,#0x10                          @ 081141a2 04ac
    adds r1,r4,#0x0    @ 081141a4 211c
    bl __unpack_f                            @ 081141a6 fff789fc
    movs r1,#0x0    @ 081141aa 0021
    ldr r0,[sp,#0x0]                         @ 081141ac 0098
    cmp r0,#0x1                              @ 081141ae 0128
    bhi LAB_081141b4                         @ 081141b0 00d8
    movs r1,#0x1    @ 081141b2 0121
LAB_081141b4:
    cmp r1,#0x0                              @ 081141b4 0029
    bne LAB_081141c6                         @ 081141b6 06d1
    movs r1,#0x0    @ 081141b8 0021
    ldr r0,[sp,#0x10]                        @ 081141ba 0498
    cmp r0,#0x1                              @ 081141bc 0128
    bhi LAB_081141c2                         @ 081141be 00d8
    movs r1,#0x1    @ 081141c0 0121
LAB_081141c2:
    cmp r1,#0x0                              @ 081141c2 0029
    beq LAB_081141ca                         @ 081141c4 01d0
LAB_081141c6:
    movs r0,#0x1    @ 081141c6 0120
    b LAB_081141d2                           @ 081141c8 03e0
LAB_081141ca:
    .hword 0x4668    @ 081141ca 6846
    adds r1,r4,#0x0    @ 081141cc 211c
    bl __fpcmp_parts_f                       @ 081141ce fff7c9fe
LAB_081141d2:
    add sp,#0x28                             @ 081141d2 0ab0
    pop {r4,pc}                              @ 081141d4 10bd
    .zero  0x2

@ GCC libgcc single-precision float less-or-equal comparison (__lesf2): unpacks two floats (r0, r1), checks NaN (kind > 1 -> returns +1 = unordered, does not satisfy <=), normal path calls __fpcmp_parts_f.
@ GCC __lesf2 contract: <=0 = A<=B, positive = A>B or NaN. Caller pattern: bl compare_float_le; cmp r0,#0; bgt not_le.
@ indeg=0 in static callgraph: grep ".word 0x081141d9" asm/all.s -> no hits; dead code (compiler-generated __lesf2 not directly called in this ROM).
@ Symmetric with compare_double_le (0x08113834); NaN returns +1 (no rsbs); 6th (last) of 6 float comparison functions.
compare_float_le:
    push {r4,lr}                             @ 081141d8 10b5
    sub sp,#0x28                             @ 081141da 8ab0
    str r0,[sp,#0x20]                        @ 081141dc 0890
    str r1,[sp,#0x24]                        @ 081141de 0991
    add r0,sp,#0x20                          @ 081141e0 08a8
    .hword 0x4669    @ 081141e2 6946
    bl __unpack_f                            @ 081141e4 fff76afc
    add r0,sp,#0x24                          @ 081141e8 09a8
    add r4,sp,#0x10                          @ 081141ea 04ac
    adds r1,r4,#0x0    @ 081141ec 211c
    bl __unpack_f                            @ 081141ee fff765fc
    movs r1,#0x0    @ 081141f2 0021
    ldr r0,[sp,#0x0]                         @ 081141f4 0098
    cmp r0,#0x1                              @ 081141f6 0128
    bhi LAB_081141fc                         @ 081141f8 00d8
    movs r1,#0x1    @ 081141fa 0121
LAB_081141fc:
    cmp r1,#0x0                              @ 081141fc 0029
    bne LAB_0811420e                         @ 081141fe 06d1
    movs r1,#0x0    @ 08114200 0021
    ldr r0,[sp,#0x10]                        @ 08114202 0498
    cmp r0,#0x1                              @ 08114204 0128
    bhi LAB_0811420a                         @ 08114206 00d8
    movs r1,#0x1    @ 08114208 0121
LAB_0811420a:
    cmp r1,#0x0                              @ 0811420a 0029
    beq LAB_08114212                         @ 0811420c 01d0
LAB_0811420e:
    movs r0,#0x1    @ 0811420e 0120
    b LAB_0811421a                           @ 08114210 03e0
LAB_08114212:
    .hword 0x4668    @ 08114212 6846
    adds r1,r4,#0x0    @ 08114214 211c
    bl __fpcmp_parts_f                       @ 08114216 fff7a5fe
LAB_0811421a:
    add sp,#0x28                             @ 0811421a 0ab0
    pop {r4,pc}                              @ 0811421c 10bd
    .zero  0x2
__floatsisf:
    push {lr}                                @ 08114220 00b5
    sub sp,#0x10                             @ 08114222 84b0
    adds r1,r0,#0x0    @ 08114224 011c
    movs r0,#0x3    @ 08114226 0320
    str r0,[sp,#0x0]                         @ 08114228 0090
    lsrs r2,r1,#0x1f    @ 0811422a ca0f
    str r2,[sp,#0x4]                         @ 0811422c 0192
    cmp r1,#0x0                              @ 0811422e 0029
    bne LAB_08114238                         @ 08114230 02d1
    movs r0,#0x2    @ 08114232 0220
    str r0,[sp,#0x0]                         @ 08114234 0090
    b LAB_08114270                           @ 08114236 1be0
LAB_08114238:
    movs r0,#0x1e    @ 08114238 1e20
    str r0,[sp,#0x8]                         @ 0811423a 0290
    cmp r2,#0x0                              @ 0811423c 002a
    beq LAB_08114256                         @ 0811423e 0ad0
    movs r0,#0x80    @ 08114240 8020
    lsls r0,r0,#0x18    @ 08114242 0006
    cmp r1,r0                                @ 08114244 8142
    bne LAB_08114250                         @ 08114246 03d1
    ldr r0, DAT_0811424c                     @ 08114248 0048
    b LAB_08114276                           @ 0811424a 14e0
DAT_0811424c:
    .word  0xcf000000                     @ 0811424c 000000cf
LAB_08114250:
    rsbs r0,r1,#0    @ 08114250 4842
    str r0,[sp,#0xc]                         @ 08114252 0390
    b LAB_08114258                           @ 08114254 00e0
LAB_08114256:
    str r1,[sp,#0xc]                         @ 08114256 0391
LAB_08114258:
    ldr r2,[sp,#0xc]                         @ 08114258 039a
    ldr r3, DAT_0811427c                     @ 0811425a 084b
    cmp r2,r3                                @ 0811425c 9a42
    bhi LAB_08114270                         @ 0811425e 07d8
    ldr r1,[sp,#0x8]                         @ 08114260 0299
LAB_08114262:
    lsls r0,r2,#0x1    @ 08114262 5000
    subs r1,#0x1    @ 08114264 0139
    adds r2,r0,#0x0    @ 08114266 021c
    cmp r0,r3                                @ 08114268 9842
    bls LAB_08114262                         @ 0811426a fad9
    str r1,[sp,#0x8]                         @ 0811426c 0291
    str r0,[sp,#0xc]                         @ 0811426e 0390
LAB_08114270:
    .hword 0x4668    @ 08114270 6846
    bl __pack_f                              @ 08114272 fff7c7fb
LAB_08114276:
    add sp,#0x10                             @ 08114276 04b0
    pop {pc}                                 @ 08114278 00bd
    .zero  0x2
DAT_0811427c:
    .word  0x3fffffff                     @ 0811427c ffffff3f
__fixsfsi:
    push {lr}                                @ 08114280 00b5
    sub sp,#0x14                             @ 08114282 85b0
    str r0,[sp,#0x10]                        @ 08114284 0490
    add r0,sp,#0x10                          @ 08114286 04a8
    .hword 0x4669    @ 08114288 6946
    bl __unpack_f                            @ 0811428a fff717fc
    movs r1,#0x0    @ 0811428e 0021
    ldr r0,[sp,#0x0]                         @ 08114290 0098
    cmp r0,#0x2                              @ 08114292 0228
    bne LAB_08114298                         @ 08114294 00d1
    movs r1,#0x1    @ 08114296 0121
LAB_08114298:
    cmp r1,#0x0                              @ 08114298 0029
    bne LAB_081142ca                         @ 0811429a 16d1
    movs r1,#0x0    @ 0811429c 0021
    cmp r0,#0x1                              @ 0811429e 0128
    bhi LAB_081142a4                         @ 081142a0 00d8
    movs r1,#0x1    @ 081142a2 0121
LAB_081142a4:
    cmp r1,#0x0                              @ 081142a4 0029
    bne LAB_081142ca                         @ 081142a6 10d1
    movs r1,#0x0    @ 081142a8 0021
    cmp r0,#0x4                              @ 081142aa 0428
    bne LAB_081142b0                         @ 081142ac 00d1
    movs r1,#0x1    @ 081142ae 0121
LAB_081142b0:
    cmp r1,#0x0                              @ 081142b0 0029
    beq LAB_081142c4                         @ 081142b2 07d0
LAB_081142b4:
    ldr r0,[sp,#0x4]                         @ 081142b4 0198
    ldr r1, DAT_081142c0                     @ 081142b6 0249
    cmp r0,#0x0                              @ 081142b8 0028
    beq LAB_081142e2                         @ 081142ba 12d0
    adds r1,#0x1    @ 081142bc 0131
    b LAB_081142e2                           @ 081142be 10e0
DAT_081142c0:
    .word  0x7fffffff                     @ 081142c0 ffffff7f
LAB_081142c4:
    ldr r1,[sp,#0x8]                         @ 081142c4 0299
    cmp r1,#0x0                              @ 081142c6 0029
    bge LAB_081142ce                         @ 081142c8 01da
LAB_081142ca:
    movs r0,#0x0    @ 081142ca 0020
    b LAB_081142e4                           @ 081142cc 0ae0
LAB_081142ce:
    cmp r1,#0x1e                             @ 081142ce 1e29
    bgt LAB_081142b4                         @ 081142d0 f0dc
    movs r0,#0x1e    @ 081142d2 1e20
    subs r0,r0,r1    @ 081142d4 401a
    ldr r1,[sp,#0xc]                         @ 081142d6 0399
    lsrs r1,r0    @ 081142d8 c140
    ldr r0,[sp,#0x4]                         @ 081142da 0198
    cmp r0,#0x0                              @ 081142dc 0028
    beq LAB_081142e2                         @ 081142de 00d0
    rsbs r1,r1,#0    @ 081142e0 4942
LAB_081142e2:
    adds r0,r1,#0x0    @ 081142e2 081c
LAB_081142e4:
    add sp,#0x14                             @ 081142e4 05b0
    pop {pc}                                 @ 081142e6 00bd
__negsf2:
    push {lr}                                @ 081142e8 00b5
    sub sp,#0x14                             @ 081142ea 85b0
    str r0,[sp,#0x10]                        @ 081142ec 0490
    add r0,sp,#0x10                          @ 081142ee 04a8
    .hword 0x4669    @ 081142f0 6946
    bl __unpack_f                            @ 081142f2 fff7e3fb
    movs r1,#0x0    @ 081142f6 0021
    ldr r0,[sp,#0x4]                         @ 081142f8 0198
    cmp r0,#0x0                              @ 081142fa 0028
    bne LAB_08114300                         @ 081142fc 00d1
    movs r1,#0x1    @ 081142fe 0121
LAB_08114300:
    str r1,[sp,#0x4]                         @ 08114300 0191
    .hword 0x4668    @ 08114302 6846
    bl __pack_f                              @ 08114304 fff77efb
    add sp,#0x14                             @ 08114308 05b0
    pop {pc}                                 @ 0811430a 00bd
__make_fp:
    push {lr}                                @ 0811430c 00b5
    sub sp,#0x10                             @ 0811430e 84b0
    str r0,[sp,#0x0]                         @ 08114310 0090
    str r1,[sp,#0x4]                         @ 08114312 0191
    str r2,[sp,#0x8]                         @ 08114314 0292
    str r3,[sp,#0xc]                         @ 08114316 0393
    .hword 0x4668    @ 08114318 6846
    bl __pack_f                              @ 0811431a fff773fb
    add sp,#0x10                             @ 0811431e 04b0
    pop {pc}                                 @ 08114320 00bd
    .zero  0x2
__extendsfdf2:
    push {r4,r5,r6,lr}                       @ 08114324 70b5
    sub sp,#0x18                             @ 08114326 86b0
    str r0,[sp,#0x14]                        @ 08114328 0590
    add r0,sp,#0x14                          @ 0811432a 05a8
    add r1,sp,#0x4                           @ 0811432c 01a9
    bl __unpack_f                            @ 0811432e fff7c5fb
    ldr r0,[sp,#0x4]                         @ 08114332 0198
    ldr r1,[sp,#0x8]                         @ 08114334 0299
    ldr r2,[sp,#0xc]                         @ 08114336 039a
    ldr r3,[sp,#0x10]                        @ 08114338 049b
    movs r4,#0x0    @ 0811433a 0024
    lsrs r6,r3,#0x2    @ 0811433c 9e08
    lsls r5,r4,#0x1e    @ 0811433e a507
    adds r4,r6,#0x0    @ 08114340 341c
    orrs r4,r5    @ 08114342 2c43
    lsls r3,r3,#0x1e    @ 08114344 9b07
    str r4,[sp,#0x0]                         @ 08114346 0094
    bl __make_dp                             @ 08114348 fff726fb
    add sp,#0x18                             @ 0811434c 06b0
    pop {r4,r5,r6,pc}                        @ 0811434e 70bd
__lshrdi3:
    push {r4,r5,r6,lr}                       @ 08114350 70b5
    adds r6,r1,#0x0    @ 08114352 0e1c
    adds r5,r0,#0x0    @ 08114354 051c
    cmp r2,#0x0                              @ 08114356 002a
    beq LAB_08114380                         @ 08114358 12d0
    movs r0,#0x20    @ 0811435a 2020
    subs r0,r0,r2    @ 0811435c 801a
    cmp r0,#0x0                              @ 0811435e 0028
    bgt LAB_0811436c                         @ 08114360 04dc
    movs r4,#0x0    @ 08114362 0024
    rsbs r0,r0,#0    @ 08114364 4042
    adds r3,r6,#0x0    @ 08114366 331c
    lsrs r3,r0    @ 08114368 c340
    b LAB_0811437c                           @ 0811436a 07e0
LAB_0811436c:
    adds r1,r6,#0x0    @ 0811436c 311c
    lsls r1,r0    @ 0811436e 8140
    adds r4,r6,#0x0    @ 08114370 341c
    lsrs r4,r2    @ 08114372 d440
    adds r0,r5,#0x0    @ 08114374 281c
    lsrs r0,r2    @ 08114376 d040
    adds r3,r0,#0x0    @ 08114378 031c
    orrs r3,r1    @ 0811437a 0b43
LAB_0811437c:
    adds r1,r4,#0x0    @ 0811437c 211c
    adds r0,r3,#0x0    @ 0811437e 181c
LAB_08114380:
    pop {r4,r5,r6,pc}                        @ 08114380 70bd
    .zero  0x2
__negdi2:
    push {r4,lr}                             @ 08114384 10b5
    rsbs r2,r0,#0    @ 08114386 4242
    adds r3,r2,#0x0    @ 08114388 131c
    rsbs r1,r1,#0    @ 0811438a 4942
    cmp r2,#0x0                              @ 0811438c 002a
    beq LAB_08114392                         @ 0811438e 00d0
    subs r1,#0x1    @ 08114390 0139
LAB_08114392:
    adds r4,r1,#0x0    @ 08114392 0c1c
    adds r1,r4,#0x0    @ 08114394 211c
    adds r0,r3,#0x0    @ 08114396 181c
    pop {r4,pc}                              @ 08114398 10bd
    .zero  0x6
DWORD_081143a0:
    .word  0x00000000                     @ 081143a0 00000000
DWORD_081143a4:
    .word  0x00000000                     @ 081143a4 00000000
DWORD_081143a8:
    .word  0x00000000                     @ 081143a8 00000000
DWORD_081143ac:
    .word  0x00000000                     @ 081143ac 00000000
    .byte  0xa0, 0x49, 0x11, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
DWORD_081143c0:
    .word  0x0b010808                     @ 081143c0 0808010b
    ROM_INCBIN 0x1143c4, 0x6cc
PTR_DAT_08114a90:
    .word  0x08114b20                     @ 08114a90 204b1108
    .word  0x081176bc                     @ 08114a94 bc761108
    .word  0x0811c8b8                     @ 08114a98 b8c81108
    .word  0x08120774                     @ 08114a9c 74071208
    .word  0x08122dc4                     @ 08114aa0 c42d1208
    .word  0x081266d8                     @ 08114aa4 d8661208
    .word  0x08129360                     @ 08114aa8 60931208
    .word  0x0812b14c                     @ 08114aac 4cb11208
    .word  0x0812bdec                     @ 08114ab0 ecbd1208
    .word  0x0812ebd0                     @ 08114ab4 d0eb1208
    .word  0x08130d84                     @ 08114ab8 840d1308
    .word  0x081341a8                     @ 08114abc a8411308
    .word  0x08137924                     @ 08114ac0 24791308
    .word  0x0813abf0                     @ 08114ac4 f0ab1308
    .word  0x0813e98c                     @ 08114ac8 8ce91308
    .word  0x081407c8                     @ 08114acc c8071408
    .word  0x08146a90                     @ 08114ad0 906a1408
    .word  0x0814bbb0                     @ 08114ad4 b0bb1408
    .word  0x0814d340                     @ 08114ad8 40d31408
    .word  0x08150524                     @ 08114adc 24051508
    .word  0x081547d4                     @ 08114ae0 d4471508
    .word  0x08155ad0                     @ 08114ae4 d05a1508
    .word  0x08157c0c                     @ 08114ae8 0c7c1508
    .word  0x08161a8c                     @ 08114aec 8c1a1608
    .word  0x0816a21c                     @ 08114af0 1ca21608
    .word  0x0816a720                     @ 08114af4 20a71608
    .word  0x0816be64                     @ 08114af8 64be1608
    .word  0x0816ef20                     @ 08114afc 20ef1608
    .word  0x081771a0                     @ 08114b00 a0711708
    .word  0x0817ea50                     @ 08114b04 50ea1708
    .word  0x08180604                     @ 08114b08 04061808
    .word  0x081849c4                     @ 08114b0c c4491808
    .word  0x0818bb70                     @ 08114b10 70bb1808
    .word  0x0818e9a8                     @ 08114b14 a8e91808
    .word  0x0818ecec                     @ 08114b18 ecec1808
    .word  0x08190f24                     @ 08114b1c 240f1908
DAT_08114b20:
    ROM_INCBIN 0x114b20, 0x14870
    .word  0x02020202                     @ 08129390 02020202
    .word  0x02020202                     @ 08129394 02020202
    .word  0x02020202                     @ 08129398 02020202
    .word  0x02020202                     @ 0812939c 02020202
    .word  0x02020202                     @ 081293a0 02020202
    .word  0x02020202                     @ 081293a4 02020202
    .word  0x02020202                     @ 081293a8 02020202
    .word  0x02020202                     @ 081293ac 02020202
    .word  0x02020202                     @ 081293b0 02020202
    .word  0x02020202                     @ 081293b4 02020202
    .word  0x02020202                     @ 081293b8 02020202
    .word  0x02020202                     @ 081293bc 02020202
    .word  0x02020201                     @ 081293c0 01020202
    .word  0x02020202                     @ 081293c4 02020202
    .word  0x02020202                     @ 081293c8 02020202
    .word  0x02020202                     @ 081293cc 02020202
    .word  0x02020202                     @ 081293d0 02020202
    .word  0x02010202                     @ 081293d4 02020102
    ROM_INCBIN 0x1293d8, 0x530
    .word  0x02020202                     @ 08129908 02020202
    .word  0x02020202                     @ 0812990c 02020202
    .word  0x02020202                     @ 08129910 02020202
    .word  0x02020202                     @ 08129914 02020202
    .word  0x02020202                     @ 08129918 02020202
    .word  0x02020202                     @ 0812991c 02020202
    .word  0x02020202                     @ 08129920 02020202
    .word  0x02020202                     @ 08129924 02020202
    .word  0x02020202                     @ 08129928 02020202
    .word  0x02020202                     @ 0812992c 02020202
    .word  0x02020202                     @ 08129930 02020202
    .word  0x02020202                     @ 08129934 02020202
    .word  0x02020202                     @ 08129938 02020202
    .word  0x02020202                     @ 0812993c 02020202
    .word  0x02020202                     @ 08129940 02020202
    .word  0x02020202                     @ 08129944 02020202
    .word  0x02020202                     @ 08129948 02020202
    .word  0x02020202                     @ 0812994c 02020202
    .word  0x02020202                     @ 08129950 02020202
    .word  0x02020202                     @ 08129954 02020202
    .word  0x02020202                     @ 08129958 02020202
    .word  0x02020202                     @ 0812995c 02020202
    .word  0x02020202                     @ 08129960 02020202
    .word  0x02020201                     @ 08129964 01020202
    .word  0x02020102                     @ 08129968 02010202
    .word  0x02020201                     @ 0812996c 01020202
    .word  0x02020202                     @ 08129970 02020202
    ROM_INCBIN 0x129974, 0x418
    .word  0x02020202                     @ 08129d8c 02020202
    .word  0x02020102                     @ 08129d90 02010202
    .word  0x02020202                     @ 08129d94 02020202
    .word  0x02020202                     @ 08129d98 02020202
    .word  0x02020202                     @ 08129d9c 02020202
    .word  0x02020202                     @ 08129da0 02020202
    .word  0x02020202                     @ 08129da4 02020202
    .word  0x02020202                     @ 08129da8 02020202
    .word  0x02020202                     @ 08129dac 02020202
    .word  0x02020202                     @ 08129db0 02020202
    .word  0x02020202                     @ 08129db4 02020202
    .word  0x02020202                     @ 08129db8 02020202
    .word  0x02020202                     @ 08129dbc 02020202
    .word  0x02020202                     @ 08129dc0 02020202
    .word  0x02020202                     @ 08129dc4 02020202
    .word  0x02030203                     @ 08129dc8 03020302
    .word  0x02030203                     @ 08129dcc 03020302
    .word  0x02030203                     @ 08129dd0 03020302
    ROM_INCBIN 0x129dd4, 0x2c
    .word  0x02020302                     @ 08129e00 02030202
    .word  0x02020203                     @ 08129e04 03020202
    .word  0x02020203                     @ 08129e08 03020202
    .word  0x02020202                     @ 08129e0c 02020202
    .word  0x02020202                     @ 08129e10 02020202
    .word  0x02020202                     @ 08129e14 02020202
    .word  0x02020202                     @ 08129e18 02020202
    ROM_INCBIN 0x129e1c, 0xb6c
    .word  0x02020202                     @ 0812a988 02020202
    .word  0x02020202                     @ 0812a98c 02020202
    .word  0x02020202                     @ 0812a990 02020202
    .word  0x02020202                     @ 0812a994 02020202
    .word  0x02020202                     @ 0812a998 02020202
    .word  0x02020202                     @ 0812a99c 02020202
    .word  0x02020202                     @ 0812a9a0 02020202
    .word  0x02020202                     @ 0812a9a4 02020202
    .word  0x02020202                     @ 0812a9a8 02020202
    .word  0x02020202                     @ 0812a9ac 02020202
    .word  0x02020202                     @ 0812a9b0 02020202
    .word  0x02020202                     @ 0812a9b4 02020202
    .word  0x02020202                     @ 0812a9b8 02020202
    .word  0x02020202                     @ 0812a9bc 02020202
    .word  0x02020202                     @ 0812a9c0 02020202
    .word  0x02020202                     @ 0812a9c4 02020202
    .word  0x02020202                     @ 0812a9c8 02020202
    ROM_INCBIN 0x12a9cc, 0x20c
    .word  0x02020102                     @ 0812abd8 02010202
    .word  0x02020202                     @ 0812abdc 02020202
    .word  0x02020202                     @ 0812abe0 02020202
    .word  0x02020202                     @ 0812abe4 02020202
    .word  0x02020202                     @ 0812abe8 02020202
    .word  0x02020202                     @ 0812abec 02020202
    .word  0x02020202                     @ 0812abf0 02020202
    .word  0x02020202                     @ 0812abf4 02020202
    .word  0x02020202                     @ 0812abf8 02020202
    ROM_INCBIN 0x12abfc, 0x218
    .word  0x02010101                     @ 0812ae14 01010102
    .word  0x02010201                     @ 0812ae18 01020102
    .word  0x02010201                     @ 0812ae1c 01020102
    .word  0x02020201                     @ 0812ae20 01020202
    .word  0x02020202                     @ 0812ae24 02020202
    .word  0x02020202                     @ 0812ae28 02020202
    .byte  0x02, 0x02, 0x02, 0x01
    .word  0x02020202                     @ 0812ae30 02020202
    .word  0x02020202                     @ 0812ae34 02020202
    .word  0x02020202                     @ 0812ae38 02020202
    .word  0x02020202                     @ 0812ae3c 02020202
    .word  0x02020202                     @ 0812ae40 02020202
    .word  0x02020202                     @ 0812ae44 02020202
    .word  0x02020202                     @ 0812ae48 02020202
    ROM_INCBIN 0x12ae4c, 0x1c
    .word  0x02020202                     @ 0812ae68 02020202
    .word  0x02020202                     @ 0812ae6c 02020202
    .word  0x02020202                     @ 0812ae70 02020202
    .word  0x02020201                     @ 0812ae74 01020202
    .word  0x02020201                     @ 0812ae78 01020202
    .word  0x02020202                     @ 0812ae7c 02020202
    .word  0x02020202                     @ 0812ae80 02020202
    .word  0x02020202                     @ 0812ae84 02020202
    .word  0x02020202                     @ 0812ae88 02020202
    .word  0x02020202                     @ 0812ae8c 02020202
    .word  0x02020202                     @ 0812ae90 02020202
    .word  0x02020202                     @ 0812ae94 02020202
    .word  0x02020202                     @ 0812ae98 02020202
    .word  0x02020202                     @ 0812ae9c 02020202
    .word  0x02030202                     @ 0812aea0 02020302
    ROM_INCBIN 0x12aea4, 0x18
    .word  0x02020202                     @ 0812aebc 02020202
    .word  0x02020203                     @ 0812aec0 03020202
    .word  0x02020202                     @ 0812aec4 02020202
    .word  0x02020202                     @ 0812aec8 02020202
    .word  0x02020202                     @ 0812aecc 02020202
    .word  0x02020202                     @ 0812aed0 02020202
    .word  0x02020201                     @ 0812aed4 01020202
    ROM_INCBIN 0x12aed8, 0x1e8
    .word  0x02010202                     @ 0812b0c0 02020102
    .word  0x02010201                     @ 0812b0c4 01020102
    .word  0x02010201                     @ 0812b0c8 01020102
    .word  0x02020201                     @ 0812b0cc 01020202
    .word  0x02020102                     @ 0812b0d0 02010202
    .word  0x02020202                     @ 0812b0d4 02020202
    .byte  0x02, 0x01, 0x02, 0x01
    .word  0x02020202                     @ 0812b0dc 02020202
    .word  0x02020202                     @ 0812b0e0 02020202
    .word  0x02020202                     @ 0812b0e4 02020202
    .word  0x02020202                     @ 0812b0e8 02020202
    .word  0x02030202                     @ 0812b0ec 02020302
    .word  0x02030203                     @ 0812b0f0 03020302
    .word  0x02030203                     @ 0812b0f4 03020302
    ROM_INCBIN 0x12b0f8, 0x1c
    .word  0x02030202                     @ 0812b114 02020302
    .word  0x02020203                     @ 0812b118 03020202
    .word  0x02020202                     @ 0812b11c 02020202
    .word  0x02020202                     @ 0812b120 02020202
    .word  0x02020202                     @ 0812b124 02020202
    .word  0x02020202                     @ 0812b128 02020202
    ROM_INCBIN 0x12b12c, 0x3e50c
    .word  0x02020200                     @ 08169638 00020202
    .word  0x02020202                     @ 0816963c 02020202
    .word  0x02020202                     @ 08169640 02020202
    .word  0x02020202                     @ 08169644 02020202
    .word  0x02020202                     @ 08169648 02020202
    ROM_INCBIN 0x16964c, 0x38
    .word  0x02020202                     @ 08169684 02020202
    .word  0x02020202                     @ 08169688 02020202
    .word  0x02020202                     @ 0816968c 02020202
    .word  0x02020202                     @ 08169690 02020202
    .word  0x02020202                     @ 08169694 02020202
    ROM_INCBIN 0x169698, 0x20c
    .word  0x02020203                     @ 081698a4 03020202
    .word  0x02020202                     @ 081698a8 02020202
    .word  0x02020202                     @ 081698ac 02020202
    .word  0x02020202                     @ 081698b0 02020202
    .word  0x02020202                     @ 081698b4 02020202
    .word  0x02020202                     @ 081698b8 02020202
    ROM_INCBIN 0x1698bc, 0x118
    .word  0x02020203                     @ 081699d4 03020202
    .word  0x02020202                     @ 081699d8 02020202
    .word  0x02020202                     @ 081699dc 02020202
    .word  0x02020202                     @ 081699e0 02020202
    .word  0x02020202                     @ 081699e4 02020202
    .word  0x02020202                     @ 081699e8 02020202
    ROM_INCBIN 0x1699ec, 0x260
    .word  0x02020200                     @ 08169c4c 00020202
    .word  0x02020202                     @ 08169c50 02020202
    .word  0x02020202                     @ 08169c54 02020202
    .word  0x02020202                     @ 08169c58 02020202
    .word  0x02020202                     @ 08169c5c 02020202
    .word  0x02020202                     @ 08169c60 02020202
    .word  0x02020202                     @ 08169c64 02020202
    ROM_INCBIN 0x169c68, 0x17c
    .word  0x02000000                     @ 08169de4 00000002
    .word  0x02020202                     @ 08169de8 02020202
    .word  0x02020202                     @ 08169dec 02020202
    .word  0x02020202                     @ 08169df0 02020202
    .word  0x02020202                     @ 08169df4 02020202
    .word  0x02020202                     @ 08169df8 02020202
    ROM_INCBIN 0x169dfc, 0x14aa0
    .word  0x02020200                     @ 0817e89c 00020202
    .word  0x02020202                     @ 0817e8a0 02020202
    .word  0x02020202                     @ 0817e8a4 02020202
    .word  0x02020202                     @ 0817e8a8 02020202
    .word  0x02020202                     @ 0817e8ac 02020202
    .word  0x02020202                     @ 0817e8b0 02020202
    ROM_INCBIN 0x17e8b4, 0x37e4
    .word  0x090e0909                     @ 08182098 09090e09
    .word  0x09090b05                     @ 0818209c 050b0909
    .word  0x0909090b                     @ 081820a0 0b090909
    .word  0x09070909                     @ 081820a4 09090709
    .word  0x090b0709                     @ 081820a8 09070b09
    .word  0x09090b07                     @ 081820ac 070b0909
    .word  0x090b0709                     @ 081820b0 09070b09
    .word  0x09070b09                     @ 081820b4 090b0709
    .byte  0x0b, 0x09, 0x09, 0x07
    .word  0x09070b09                     @ 081820bc 090b0709
    .word  0x090b0709                     @ 081820c0 09070b09
    .word  0x09070909                     @ 081820c4 09090709
    .word  0x090b0709                     @ 081820c8 09070b09
    .word  0x09090b09                     @ 081820cc 090b0909
    ROM_INCBIN 0x1820d0, 0x1644
    .word  0x02020202                     @ 08183714 02020202
    .word  0x02020205                     @ 08183718 05020202
    .word  0x02020502                     @ 0818371c 02050202
    .word  0x02020202                     @ 08183720 02020202
    .word  0x02020202                     @ 08183724 02020202
    .word  0x02020202                     @ 08183728 02020202
    .word  0x02020502                     @ 0818372c 02050202
    .word  0x02020202                     @ 08183730 02020202
    .word  0x02020202                     @ 08183734 02020202
    .word  0x02020202                     @ 08183738 02020202
    .word  0x02020202                     @ 0818373c 02020202
    ROM_INCBIN 0x183740, 0x28
    .word  0x02020202                     @ 08183768 02020202
    .word  0x02020205                     @ 0818376c 05020202
    .word  0x02020202                     @ 08183770 02020202
    .word  0x02020202                     @ 08183774 02020202
    .word  0x02020202                     @ 08183778 02020202
    .word  0x02020205                     @ 0818377c 05020202
    .word  0x02020502                     @ 08183780 02050202
    .word  0x02020202                     @ 08183784 02020202
    .word  0x02020202                     @ 08183788 02020202
    .word  0x02020202                     @ 0818378c 02020202
    .word  0x02020502                     @ 08183790 02050202
    ROM_INCBIN 0x183794, 0x28
    .word  0x02020202                     @ 081837bc 02020202
    .word  0x02020202                     @ 081837c0 02020202
    .word  0x02020202                     @ 081837c4 02020202
    .word  0x02020202                     @ 081837c8 02020202
    .word  0x02020202                     @ 081837cc 02020202
    .word  0x02020202                     @ 081837d0 02020202
    .word  0x02020202                     @ 081837d4 02020202
    .word  0x02020202                     @ 081837d8 02020202
    .word  0x02020202                     @ 081837dc 02020202
    .word  0x02020202                     @ 081837e0 02020202
    .word  0x02020202                     @ 081837e4 02020202
    .word  0x02020202                     @ 081837e8 02020202
    .word  0x02020202                     @ 081837ec 02020202
    .word  0x02020202                     @ 081837f0 02020202
    .word  0x02020202                     @ 081837f4 02020202
    .word  0x02020202                     @ 081837f8 02020202
    .word  0x02020202                     @ 081837fc 02020202
    .word  0x02020202                     @ 08183800 02020202
    .word  0x02020202                     @ 08183804 02020202
    .word  0x02020202                     @ 08183808 02020202
    .word  0x02020202                     @ 0818380c 02020202
    .word  0x02020202                     @ 08183810 02020202
    .word  0x02020202                     @ 08183814 02020202
    .word  0x02020202                     @ 08183818 02020202
    .word  0x02020202                     @ 0818381c 02020202
    .word  0x02020202                     @ 08183820 02020202
    .word  0x02020202                     @ 08183824 02020202
    .word  0x02020202                     @ 08183828 02020202
    .word  0x02020202                     @ 0818382c 02020202
    .word  0x02020202                     @ 08183830 02020202
    .word  0x02020202                     @ 08183834 02020202
    .word  0x02020202                     @ 08183838 02020202
    .word  0x02020202                     @ 0818383c 02020202
    .word  0x02020202                     @ 08183840 02020202
    .word  0x02020202                     @ 08183844 02020202
    .word  0x02020202                     @ 08183848 02020202
    .word  0x02020202                     @ 0818384c 02020202
    .word  0x02020202                     @ 08183850 02020202
    .word  0x02020202                     @ 08183854 02020202
    .word  0x02020202                     @ 08183858 02020202
    .word  0x02020202                     @ 0818385c 02020202
    .word  0x02020202                     @ 08183860 02020202
    .word  0x02020202                     @ 08183864 02020202
    .word  0x02020202                     @ 08183868 02020202
    .word  0x02020202                     @ 0818386c 02020202
    .word  0x02020202                     @ 08183870 02020202
    .word  0x02020202                     @ 08183874 02020202
    .word  0x02020202                     @ 08183878 02020202
    .word  0x02020202                     @ 0818387c 02020202
    .word  0x02020202                     @ 08183880 02020202
    .word  0x02020202                     @ 08183884 02020202
    .word  0x02020202                     @ 08183888 02020202
    .word  0x02020202                     @ 0818388c 02020202
    .word  0x02020202                     @ 08183890 02020202
    .word  0x02020202                     @ 08183894 02020202
    .word  0x02020202                     @ 08183898 02020202
    .word  0x02020202                     @ 0818389c 02020202
    .word  0x02020202                     @ 081838a0 02020202
    .word  0x02020202                     @ 081838a4 02020202
    .word  0x02020202                     @ 081838a8 02020202
    .word  0x02020202                     @ 081838ac 02020202
    .word  0x02020202                     @ 081838b0 02020202
    .word  0x02020202                     @ 081838b4 02020202
    .word  0x02020202                     @ 081838b8 02020202
    .word  0x02020202                     @ 081838bc 02020202
    .word  0x02020202                     @ 081838c0 02020202
    .word  0x02020202                     @ 081838c4 02020202
    .word  0x02020202                     @ 081838c8 02020202
    .word  0x02020202                     @ 081838cc 02020202
    .word  0x02020202                     @ 081838d0 02020202
    .word  0x02020202                     @ 081838d4 02020202
    .word  0x02020202                     @ 081838d8 02020202
    .word  0x02020202                     @ 081838dc 02020202
    .word  0x02020202                     @ 081838e0 02020202
    .word  0x02020202                     @ 081838e4 02020202
    .word  0x02020202                     @ 081838e8 02020202
    .word  0x02020202                     @ 081838ec 02020202
    .word  0x02020202                     @ 081838f0 02020202
    .word  0x02020202                     @ 081838f4 02020202
    .word  0x02020202                     @ 081838f8 02020202
    .word  0x02020202                     @ 081838fc 02020202
    .word  0x02020202                     @ 08183900 02020202
    .word  0x02020202                     @ 08183904 02020202
    .word  0x02020202                     @ 08183908 02020202
    .word  0x02020202                     @ 0818390c 02020202
    .word  0x02020202                     @ 08183910 02020202
    .word  0x02020202                     @ 08183914 02020202
    .word  0x02020202                     @ 08183918 02020202
    .word  0x02020202                     @ 0818391c 02020202
    .word  0x02020202                     @ 08183920 02020202
    .word  0x02020202                     @ 08183924 02020202
    .word  0x02020202                     @ 08183928 02020202
    .word  0x02020202                     @ 0818392c 02020202
    .word  0x02020202                     @ 08183930 02020202
    .word  0x02020202                     @ 08183934 02020202
    .word  0x02020202                     @ 08183938 02020202
    .word  0x02020202                     @ 0818393c 02020202
    .word  0x02020202                     @ 08183940 02020202
    .word  0x02020202                     @ 08183944 02020202
    .word  0x02020202                     @ 08183948 02020202
    .word  0x02020202                     @ 0818394c 02020202
    .word  0x02020202                     @ 08183950 02020202
    .word  0x02020202                     @ 08183954 02020202
    .word  0x02020202                     @ 08183958 02020202
    .word  0x02020202                     @ 0818395c 02020202
    .word  0x02020202                     @ 08183960 02020202
    .word  0x02020202                     @ 08183964 02020202
    .word  0x02020202                     @ 08183968 02020202
    .word  0x02020202                     @ 0818396c 02020202
    .word  0x02020202                     @ 08183970 02020202
    .word  0x02020202                     @ 08183974 02020202
    .word  0x02020202                     @ 08183978 02020202
    .word  0x02020202                     @ 0818397c 02020202
    .word  0x02020202                     @ 08183980 02020202
    .word  0x02020202                     @ 08183984 02020202
    .word  0x02020202                     @ 08183988 02020202
    .word  0x02020202                     @ 0818398c 02020202
    .word  0x02020202                     @ 08183990 02020202
    .word  0x02020202                     @ 08183994 02020202
    .word  0x02020202                     @ 08183998 02020202
    .word  0x02020202                     @ 0818399c 02020202
    .word  0x02020202                     @ 081839a0 02020202
    .word  0x02020202                     @ 081839a4 02020202
    .word  0x02020202                     @ 081839a8 02020202
    .word  0x02020202                     @ 081839ac 02020202
    .word  0x02020202                     @ 081839b0 02020202
    .word  0x02020202                     @ 081839b4 02020202
    .word  0x02020202                     @ 081839b8 02020202
    .word  0x02020202                     @ 081839bc 02020202
    .word  0x02020202                     @ 081839c0 02020202
    .word  0x02020202                     @ 081839c4 02020202
    .word  0x02020202                     @ 081839c8 02020202
    .word  0x02020202                     @ 081839cc 02020202
    .word  0x02020202                     @ 081839d0 02020202
    .word  0x02020202                     @ 081839d4 02020202
    .word  0x02020202                     @ 081839d8 02020202
    .word  0x02020202                     @ 081839dc 02020202
    .word  0x02020202                     @ 081839e0 02020202
    .word  0x02020202                     @ 081839e4 02020202
    .word  0x02020202                     @ 081839e8 02020202
    .word  0x02020202                     @ 081839ec 02020202
    .word  0x02020202                     @ 081839f0 02020202
    .word  0x02020202                     @ 081839f4 02020202
    .word  0x02020202                     @ 081839f8 02020202
    .word  0x02020202                     @ 081839fc 02020202
    .word  0x02020202                     @ 08183a00 02020202
    .word  0x02020202                     @ 08183a04 02020202
    .word  0x02020202                     @ 08183a08 02020202
    .word  0x02020202                     @ 08183a0c 02020202
    .word  0x02020202                     @ 08183a10 02020202
    .word  0x02020202                     @ 08183a14 02020202
    .word  0x02020202                     @ 08183a18 02020202
    .word  0x02020202                     @ 08183a1c 02020202
    .word  0x02020202                     @ 08183a20 02020202
    .word  0x02020202                     @ 08183a24 02020202
    .word  0x02020202                     @ 08183a28 02020202
    .word  0x02020202                     @ 08183a2c 02020202
    .word  0x02020202                     @ 08183a30 02020202
    .word  0x02020202                     @ 08183a34 02020202
    .word  0x02020202                     @ 08183a38 02020202
    .word  0x02020202                     @ 08183a3c 02020202
    .word  0x02020202                     @ 08183a40 02020202
    .word  0x02020202                     @ 08183a44 02020202
    .word  0x02020202                     @ 08183a48 02020202
    .word  0x02020202                     @ 08183a4c 02020202
    .word  0x02020202                     @ 08183a50 02020202
    .word  0x02020202                     @ 08183a54 02020202
    .word  0x02020202                     @ 08183a58 02020202
    .word  0x02020202                     @ 08183a5c 02020202
    .word  0x02020202                     @ 08183a60 02020202
    .word  0x02020202                     @ 08183a64 02020202
    .word  0x02020202                     @ 08183a68 02020202
    .word  0x02020202                     @ 08183a6c 02020202
    .word  0x02020202                     @ 08183a70 02020202
    .word  0x02020202                     @ 08183a74 02020202
    .word  0x02020202                     @ 08183a78 02020202
    .word  0x02020202                     @ 08183a7c 02020202
    .word  0x02020202                     @ 08183a80 02020202
    .word  0x02020202                     @ 08183a84 02020202
    .word  0x02020202                     @ 08183a88 02020202
    .word  0x02020202                     @ 08183a8c 02020202
    .word  0x02020202                     @ 08183a90 02020202
    .word  0x02020202                     @ 08183a94 02020202
    .word  0x02020202                     @ 08183a98 02020202
    .word  0x02020202                     @ 08183a9c 02020202
    .word  0x02020202                     @ 08183aa0 02020202
    .word  0x02020202                     @ 08183aa4 02020202
    .word  0x02020202                     @ 08183aa8 02020202
    .word  0x02020202                     @ 08183aac 02020202
    .word  0x02020202                     @ 08183ab0 02020202
    .word  0x02020202                     @ 08183ab4 02020202
    .word  0x02020202                     @ 08183ab8 02020202
    .word  0x02020202                     @ 08183abc 02020202
    .word  0x02020202                     @ 08183ac0 02020202
    .word  0x02020202                     @ 08183ac4 02020202
    .word  0x02020202                     @ 08183ac8 02020202
    .word  0x02020202                     @ 08183acc 02020202
    .word  0x02020202                     @ 08183ad0 02020202
    .word  0x02020202                     @ 08183ad4 02020202
    .word  0x02020202                     @ 08183ad8 02020202
    .word  0x02020202                     @ 08183adc 02020202
    .word  0x02020202                     @ 08183ae0 02020202
    .word  0x02020202                     @ 08183ae4 02020202
    .word  0x02020202                     @ 08183ae8 02020202
    .word  0x02020202                     @ 08183aec 02020202
    .word  0x02020202                     @ 08183af0 02020202
    .word  0x02020202                     @ 08183af4 02020202
    .word  0x02020202                     @ 08183af8 02020202
    .word  0x02020202                     @ 08183afc 02020202
    .word  0x02020202                     @ 08183b00 02020202
    .word  0x02020202                     @ 08183b04 02020202
    .word  0x02020202                     @ 08183b08 02020202
    .word  0x02020202                     @ 08183b0c 02020202
    .word  0x02020202                     @ 08183b10 02020202
    .word  0x02020202                     @ 08183b14 02020202
    .word  0x02020202                     @ 08183b18 02020202
    .word  0x02020202                     @ 08183b1c 02020202
    .word  0x02020202                     @ 08183b20 02020202
    .word  0x02020202                     @ 08183b24 02020202
    .word  0x02020202                     @ 08183b28 02020202
    .word  0x02020202                     @ 08183b2c 02020202
    .word  0x02020202                     @ 08183b30 02020202
    .word  0x02020202                     @ 08183b34 02020202
    .word  0x02020202                     @ 08183b38 02020202
    .word  0x02020202                     @ 08183b3c 02020202
    .word  0x02020202                     @ 08183b40 02020202
    .word  0x02020202                     @ 08183b44 02020202
    .word  0x02020202                     @ 08183b48 02020202
    .word  0x02020202                     @ 08183b4c 02020202
    .word  0x02020202                     @ 08183b50 02020202
    .word  0x02020202                     @ 08183b54 02020202
    .word  0x02020202                     @ 08183b58 02020202
    .word  0x02020202                     @ 08183b5c 02020202
    .word  0x02020202                     @ 08183b60 02020202
    .word  0x02020202                     @ 08183b64 02020202
    .word  0x02020202                     @ 08183b68 02020202
    .word  0x02020202                     @ 08183b6c 02020202
    .word  0x02020202                     @ 08183b70 02020202
    .word  0x02020202                     @ 08183b74 02020202
    .word  0x02020202                     @ 08183b78 02020202
    .word  0x02020202                     @ 08183b7c 02020202
    .word  0x02020202                     @ 08183b80 02020202
    .word  0x02020202                     @ 08183b84 02020202
    .word  0x02020202                     @ 08183b88 02020202
    .word  0x02020202                     @ 08183b8c 02020202
    .word  0x02020202                     @ 08183b90 02020202
    .word  0x02020202                     @ 08183b94 02020202
    .word  0x02020202                     @ 08183b98 02020202
    .word  0x02020202                     @ 08183b9c 02020202
    .word  0x02020202                     @ 08183ba0 02020202
    .word  0x02020202                     @ 08183ba4 02020202
    .word  0x02020202                     @ 08183ba8 02020202
    .word  0x02020202                     @ 08183bac 02020202
    .word  0x02020202                     @ 08183bb0 02020202
    .word  0x02020202                     @ 08183bb4 02020202
    .word  0x02020202                     @ 08183bb8 02020202
    .word  0x02020202                     @ 08183bbc 02020202
    .word  0x02020202                     @ 08183bc0 02020202
    .word  0x02020202                     @ 08183bc4 02020202
    .word  0x02020202                     @ 08183bc8 02020202
    .word  0x02020202                     @ 08183bcc 02020202
    .word  0x02020202                     @ 08183bd0 02020202
    .word  0x02020202                     @ 08183bd4 02020202
    .word  0x02020202                     @ 08183bd8 02020202
    .word  0x02020202                     @ 08183bdc 02020202
    .word  0x02020202                     @ 08183be0 02020202
    .word  0x02020202                     @ 08183be4 02020202
    .word  0x02020202                     @ 08183be8 02020202
    .word  0x02020202                     @ 08183bec 02020202
    .word  0x02020202                     @ 08183bf0 02020202
    .word  0x02020202                     @ 08183bf4 02020202
    .word  0x02020202                     @ 08183bf8 02020202
    .word  0x02020202                     @ 08183bfc 02020202
    .word  0x02020202                     @ 08183c00 02020202
    .word  0x02020202                     @ 08183c04 02020202
    .word  0x02020202                     @ 08183c08 02020202
    .word  0x02020202                     @ 08183c0c 02020202
    .word  0x02020202                     @ 08183c10 02020202
    .word  0x02020202                     @ 08183c14 02020202
    .word  0x02020202                     @ 08183c18 02020202
    .word  0x02020202                     @ 08183c1c 02020202
    .word  0x02020202                     @ 08183c20 02020202
    .word  0x02020202                     @ 08183c24 02020202
    .word  0x02020202                     @ 08183c28 02020202
    .word  0x02020202                     @ 08183c2c 02020202
    .word  0x02020202                     @ 08183c30 02020202
    .word  0x02020202                     @ 08183c34 02020202
    .word  0x02020202                     @ 08183c38 02020202
    .word  0x02020202                     @ 08183c3c 02020202
    .word  0x02020202                     @ 08183c40 02020202
    .word  0x02020202                     @ 08183c44 02020202
    .word  0x02020202                     @ 08183c48 02020202
    .word  0x02020202                     @ 08183c4c 02020202
    .word  0x02020202                     @ 08183c50 02020202
    .word  0x02020202                     @ 08183c54 02020202
    .word  0x02020202                     @ 08183c58 02020202
    .word  0x02020202                     @ 08183c5c 02020202
    .word  0x02020202                     @ 08183c60 02020202
    .word  0x02020202                     @ 08183c64 02020202
    .word  0x02020202                     @ 08183c68 02020202
    .word  0x02020202                     @ 08183c6c 02020202
    .word  0x02020202                     @ 08183c70 02020202
    .word  0x02020202                     @ 08183c74 02020202
    .word  0x02020202                     @ 08183c78 02020202
    .word  0x02020202                     @ 08183c7c 02020202
    .word  0x02020202                     @ 08183c80 02020202
    .word  0x02020202                     @ 08183c84 02020202
    .word  0x02020202                     @ 08183c88 02020202
    .word  0x02020202                     @ 08183c8c 02020202
    .word  0x02020202                     @ 08183c90 02020202
    .word  0x02020202                     @ 08183c94 02020202
    .word  0x02020202                     @ 08183c98 02020202
    .word  0x02020202                     @ 08183c9c 02020202
    .word  0x02020202                     @ 08183ca0 02020202
    .word  0x02020202                     @ 08183ca4 02020202
    .word  0x02020202                     @ 08183ca8 02020202
    .word  0x02020202                     @ 08183cac 02020202
    .word  0x02020202                     @ 08183cb0 02020202
    .word  0x02020202                     @ 08183cb4 02020202
    .word  0x02020202                     @ 08183cb8 02020202
    .word  0x02020202                     @ 08183cbc 02020202
    .word  0x02020202                     @ 08183cc0 02020202
    .word  0x02020202                     @ 08183cc4 02020202
    .word  0x02020202                     @ 08183cc8 02020202
    .word  0x02020202                     @ 08183ccc 02020202
    .word  0x02020202                     @ 08183cd0 02020202
    .word  0x02020202                     @ 08183cd4 02020202
    .word  0x02020202                     @ 08183cd8 02020202
    .word  0x02020202                     @ 08183cdc 02020202
    .word  0x02020202                     @ 08183ce0 02020202
    .word  0x02020202                     @ 08183ce4 02020202
    .word  0x02020202                     @ 08183ce8 02020202
    .word  0x02020202                     @ 08183cec 02020202
    .word  0x02020202                     @ 08183cf0 02020202
    .word  0x02020202                     @ 08183cf4 02020202
    .word  0x02020202                     @ 08183cf8 02020202
    .word  0x02020202                     @ 08183cfc 02020202
    .word  0x02020202                     @ 08183d00 02020202
    .word  0x02020202                     @ 08183d04 02020202
    .word  0x02020205                     @ 08183d08 05020202
    .word  0x02020202                     @ 08183d0c 02020202
    ROM_INCBIN 0x183d10, 0x510
    .word  0x02020502                     @ 08184220 02050202
    .word  0x02020202                     @ 08184224 02020202
    .word  0x02020502                     @ 08184228 02050202
    .word  0x02020202                     @ 0818422c 02020202
    .word  0x02020202                     @ 08184230 02020202
    .word  0x02020205                     @ 08184234 05020202
    .word  0x02020202                     @ 08184238 02020202
    .word  0x02020202                     @ 0818423c 02020202
    .word  0x02020202                     @ 08184240 02020202
    .word  0x02020202                     @ 08184244 02020202
    .word  0x02020202                     @ 08184248 02020202
    .word  0x02020202                     @ 0818424c 02020202
    .word  0x02020202                     @ 08184250 02020202
    .word  0x02020202                     @ 08184254 02020202
    .word  0x02020202                     @ 08184258 02020202
    .word  0x02020202                     @ 0818425c 02020202
    .word  0x02020202                     @ 08184260 02020202
    .word  0x02020202                     @ 08184264 02020202
    .word  0x02020202                     @ 08184268 02020202
    .word  0x02020202                     @ 0818426c 02020202
    .word  0x02020202                     @ 08184270 02020202
    .word  0x02020202                     @ 08184274 02020202
    .word  0x02020202                     @ 08184278 02020202
    .word  0x02020202                     @ 0818427c 02020202
    .word  0x02020202                     @ 08184280 02020202
    .word  0x02020202                     @ 08184284 02020202
    .word  0x02020202                     @ 08184288 02020202
    .word  0x02020202                     @ 0818428c 02020202
    .word  0x02020202                     @ 08184290 02020202
    .word  0x02020202                     @ 08184294 02020202
    .word  0x02020202                     @ 08184298 02020202
    .word  0x02020202                     @ 0818429c 02020202
    .word  0x02020202                     @ 081842a0 02020202
    .word  0x02020202                     @ 081842a4 02020202
    .word  0x02020202                     @ 081842a8 02020202
    .word  0x02020202                     @ 081842ac 02020202
    .word  0x02020202                     @ 081842b0 02020202
    .word  0x02020202                     @ 081842b4 02020202
    .word  0x02020202                     @ 081842b8 02020202
    .word  0x02020202                     @ 081842bc 02020202
    .word  0x02020202                     @ 081842c0 02020202
    .word  0x02020202                     @ 081842c4 02020202
    .word  0x02020202                     @ 081842c8 02020202
    .word  0x02020202                     @ 081842cc 02020202
    .word  0x02020202                     @ 081842d0 02020202
    .word  0x02020202                     @ 081842d4 02020202
    .word  0x02020202                     @ 081842d8 02020202
    .word  0x02020202                     @ 081842dc 02020202
    .word  0x02020202                     @ 081842e0 02020202
    .word  0x02020202                     @ 081842e4 02020202
    .word  0x02020202                     @ 081842e8 02020202
    .word  0x02020202                     @ 081842ec 02020202
    .word  0x02020202                     @ 081842f0 02020202
    .word  0x02020202                     @ 081842f4 02020202
    .word  0x02020202                     @ 081842f8 02020202
    .word  0x02020202                     @ 081842fc 02020202
    .word  0x02020202                     @ 08184300 02020202
    .word  0x02020202                     @ 08184304 02020202
    .word  0x02020202                     @ 08184308 02020202
    .word  0x02020202                     @ 0818430c 02020202
    .word  0x02020202                     @ 08184310 02020202
    .word  0x02020202                     @ 08184314 02020202
    .word  0x02020202                     @ 08184318 02020202
    .word  0x02020202                     @ 0818431c 02020202
    .word  0x02020202                     @ 08184320 02020202
    .word  0x02020202                     @ 08184324 02020202
    .word  0x02020202                     @ 08184328 02020202
    .word  0x02020202                     @ 0818432c 02020202
    .word  0x02020202                     @ 08184330 02020202
    .word  0x02020202                     @ 08184334 02020202
    .word  0x02020202                     @ 08184338 02020202
    .word  0x02020202                     @ 0818433c 02020202
    .word  0x02020202                     @ 08184340 02020202
    .word  0x02020202                     @ 08184344 02020202
    .word  0x02020502                     @ 08184348 02050202
    .word  0x02020202                     @ 0818434c 02020202
    .word  0x02020202                     @ 08184350 02020202
    .word  0x02020202                     @ 08184354 02020202
    .word  0x02020202                     @ 08184358 02020202
    .word  0x02020202                     @ 0818435c 02020202
    .word  0x02020202                     @ 08184360 02020202
    .word  0x02020202                     @ 08184364 02020202
    .word  0x02020202                     @ 08184368 02020202
    .word  0x02020202                     @ 0818436c 02020202
    .word  0x02020202                     @ 08184370 02020202
    .word  0x02020202                     @ 08184374 02020202
    .word  0x02020202                     @ 08184378 02020202
    .word  0x02020202                     @ 0818437c 02020202
    .word  0x02020202                     @ 08184380 02020202
    .word  0x02020202                     @ 08184384 02020202
    .word  0x02020202                     @ 08184388 02020202
    .word  0x02020202                     @ 0818438c 02020202
    .word  0x02020202                     @ 08184390 02020202
    .word  0x02020202                     @ 08184394 02020202
    .word  0x02020202                     @ 08184398 02020202
    .word  0x02020202                     @ 0818439c 02020202
    .word  0x02020202                     @ 081843a0 02020202
    .word  0x02020202                     @ 081843a4 02020202
    .word  0x02020202                     @ 081843a8 02020202
    .word  0x02020202                     @ 081843ac 02020202
    .word  0x02020202                     @ 081843b0 02020202
    .word  0x02020202                     @ 081843b4 02020202
    .word  0x02020202                     @ 081843b8 02020202
    .word  0x02020202                     @ 081843bc 02020202
    .word  0x02020202                     @ 081843c0 02020202
    .word  0x02020202                     @ 081843c4 02020202
    .word  0x02020202                     @ 081843c8 02020202
    .word  0x02020202                     @ 081843cc 02020202
    .word  0x02020202                     @ 081843d0 02020202
    .word  0x02020202                     @ 081843d4 02020202
    .word  0x02020202                     @ 081843d8 02020202
    .word  0x02020202                     @ 081843dc 02020202
    .word  0x02020202                     @ 081843e0 02020202
    .word  0x02020202                     @ 081843e4 02020202
    .word  0x02020202                     @ 081843e8 02020202
    .word  0x02020202                     @ 081843ec 02020202
    .word  0x02020202                     @ 081843f0 02020202
    .word  0x02020202                     @ 081843f4 02020202
    .word  0x02020202                     @ 081843f8 02020202
    .word  0x02020202                     @ 081843fc 02020202
    .word  0x02020202                     @ 08184400 02020202
    .word  0x02020202                     @ 08184404 02020202
    .word  0x02020202                     @ 08184408 02020202
    .word  0x02020202                     @ 0818440c 02020202
    .word  0x02020202                     @ 08184410 02020202
    .word  0x02020202                     @ 08184414 02020202
    .word  0x02020202                     @ 08184418 02020202
    .word  0x02020202                     @ 0818441c 02020202
    .word  0x02020202                     @ 08184420 02020202
    .word  0x02020202                     @ 08184424 02020202
    .word  0x02020202                     @ 08184428 02020202
    .word  0x02020202                     @ 0818442c 02020202
    .word  0x02020202                     @ 08184430 02020202
    .word  0x02020202                     @ 08184434 02020202
    .word  0x02020202                     @ 08184438 02020202
    .word  0x02020202                     @ 0818443c 02020202
    .word  0x02020202                     @ 08184440 02020202
    .word  0x02020202                     @ 08184444 02020202
    .word  0x02020202                     @ 08184448 02020202
    .word  0x02020202                     @ 0818444c 02020202
    .word  0x02020202                     @ 08184450 02020202
    .word  0x02020202                     @ 08184454 02020202
    .word  0x02020202                     @ 08184458 02020202
    .word  0x02020202                     @ 0818445c 02020202
    .word  0x02020202                     @ 08184460 02020202
    .word  0x02020202                     @ 08184464 02020202
    .word  0x02020202                     @ 08184468 02020202
    .word  0x02020202                     @ 0818446c 02020202
    .word  0x02020202                     @ 08184470 02020202
    .word  0x02020202                     @ 08184474 02020202
    .word  0x02020202                     @ 08184478 02020202
    .word  0x02020202                     @ 0818447c 02020202
    .word  0x02020202                     @ 08184480 02020202
    .word  0x02020202                     @ 08184484 02020202
    .word  0x02020202                     @ 08184488 02020202
    .word  0x02020202                     @ 0818448c 02020202
    .word  0x02020202                     @ 08184490 02020202
    .word  0x02020202                     @ 08184494 02020202
    .word  0x02020202                     @ 08184498 02020202
    .word  0x02020202                     @ 0818449c 02020202
    .word  0x02020202                     @ 081844a0 02020202
    .word  0x02020202                     @ 081844a4 02020202
    .word  0x02020202                     @ 081844a8 02020202
    .word  0x02020202                     @ 081844ac 02020202
    .word  0x02020202                     @ 081844b0 02020202
    .word  0x02020202                     @ 081844b4 02020202
    .word  0x02020202                     @ 081844b8 02020202
    .word  0x02020202                     @ 081844bc 02020202
    .word  0x02020202                     @ 081844c0 02020202
    .word  0x02020202                     @ 081844c4 02020202
    .word  0x02020202                     @ 081844c8 02020202
    .word  0x02020202                     @ 081844cc 02020202
    .word  0x02020202                     @ 081844d0 02020202
    .word  0x02020202                     @ 081844d4 02020202
    .word  0x02020202                     @ 081844d8 02020202
    .word  0x02020202                     @ 081844dc 02020202
    .word  0x02020202                     @ 081844e0 02020202
    .word  0x02020202                     @ 081844e4 02020202
    .word  0x02020202                     @ 081844e8 02020202
    .word  0x02020202                     @ 081844ec 02020202
    .word  0x02020202                     @ 081844f0 02020202
    .word  0x02020202                     @ 081844f4 02020202
    .word  0x02020202                     @ 081844f8 02020202
    .word  0x02020202                     @ 081844fc 02020202
    .word  0x02020202                     @ 08184500 02020202
    .word  0x02020202                     @ 08184504 02020202
    .word  0x02020202                     @ 08184508 02020202
    .word  0x02020202                     @ 0818450c 02020202
    .word  0x02020202                     @ 08184510 02020202
    .word  0x02020202                     @ 08184514 02020202
    .word  0x02020202                     @ 08184518 02020202
    .word  0x02020202                     @ 0818451c 02020202
    .word  0x02020202                     @ 08184520 02020202
    .word  0x02020202                     @ 08184524 02020202
    .word  0x02020202                     @ 08184528 02020202
    .word  0x02020202                     @ 0818452c 02020202
    .word  0x02020202                     @ 08184530 02020202
    .word  0x02020202                     @ 08184534 02020202
    .word  0x02020202                     @ 08184538 02020202
    .word  0x02020202                     @ 0818453c 02020202
    .word  0x02020202                     @ 08184540 02020202
    .word  0x02020202                     @ 08184544 02020202
    .word  0x02020202                     @ 08184548 02020202
    .word  0x02020202                     @ 0818454c 02020202
    .word  0x02020202                     @ 08184550 02020202
    .word  0x02020202                     @ 08184554 02020202
    .word  0x02020202                     @ 08184558 02020202
    .word  0x02020202                     @ 0818455c 02020202
    .word  0x02020202                     @ 08184560 02020202
    .word  0x02020202                     @ 08184564 02020202
    .word  0x02020202                     @ 08184568 02020202
    .word  0x02020202                     @ 0818456c 02020202
    .word  0x02020202                     @ 08184570 02020202
    .word  0x02020202                     @ 08184574 02020202
    .word  0x02020202                     @ 08184578 02020202
    .word  0x02020202                     @ 0818457c 02020202
    .word  0x02020202                     @ 08184580 02020202
    .word  0x02020202                     @ 08184584 02020202
    .word  0x02020202                     @ 08184588 02020202
    .word  0x02020202                     @ 0818458c 02020202
    .word  0x02020202                     @ 08184590 02020202
    .word  0x02020202                     @ 08184594 02020202
    .word  0x02020202                     @ 08184598 02020202
    .word  0x02020202                     @ 0818459c 02020202
    .word  0x02020202                     @ 081845a0 02020202
    .word  0x02020202                     @ 081845a4 02020202
    .word  0x02020202                     @ 081845a8 02020202
    .word  0x02020202                     @ 081845ac 02020202
    .word  0x02020202                     @ 081845b0 02020202
    .word  0x02020202                     @ 081845b4 02020202
    .word  0x02020202                     @ 081845b8 02020202
    .word  0x02020202                     @ 081845bc 02020202
    .word  0x02020202                     @ 081845c0 02020202
    .word  0x02020202                     @ 081845c4 02020202
    .word  0x02020202                     @ 081845c8 02020202
    .word  0x02020202                     @ 081845cc 02020202
    .word  0x02020202                     @ 081845d0 02020202
    .word  0x02020202                     @ 081845d4 02020202
    .word  0x02020202                     @ 081845d8 02020202
    .word  0x02020202                     @ 081845dc 02020202
    .word  0x02020202                     @ 081845e0 02020202
    .word  0x02020202                     @ 081845e4 02020202
    .word  0x02020202                     @ 081845e8 02020202
    .word  0x02020202                     @ 081845ec 02020202
    .word  0x02020202                     @ 081845f0 02020202
    .word  0x02020202                     @ 081845f4 02020202
    .word  0x02020202                     @ 081845f8 02020202
    .word  0x02020202                     @ 081845fc 02020202
    .word  0x02020202                     @ 08184600 02020202
    .word  0x02020202                     @ 08184604 02020202
    .word  0x02020202                     @ 08184608 02020202
    .word  0x02020202                     @ 0818460c 02020202
    .word  0x02020202                     @ 08184610 02020202
    .word  0x02020202                     @ 08184614 02020202
    .word  0x02020202                     @ 08184618 02020202
    .word  0x02020202                     @ 0818461c 02020202
    .word  0x02020202                     @ 08184620 02020202
    .word  0x02020202                     @ 08184624 02020202
    .word  0x02020202                     @ 08184628 02020202
    .word  0x02020202                     @ 0818462c 02020202
    .word  0x02020202                     @ 08184630 02020202
    .word  0x02020202                     @ 08184634 02020202
    .word  0x02020202                     @ 08184638 02020202
    .word  0x02020202                     @ 0818463c 02020202
    .word  0x02020202                     @ 08184640 02020202
    .word  0x02020202                     @ 08184644 02020202
    .word  0x02020202                     @ 08184648 02020202
    .word  0x02020202                     @ 0818464c 02020202
    .word  0x02020202                     @ 08184650 02020202
    .word  0x02020202                     @ 08184654 02020202
    .word  0x02020202                     @ 08184658 02020202
    .word  0x02020202                     @ 0818465c 02020202
    .word  0x02020202                     @ 08184660 02020202
    .word  0x02020202                     @ 08184664 02020202
    .word  0x02020202                     @ 08184668 02020202
    .word  0x02020202                     @ 0818466c 02020202
    .word  0x02020202                     @ 08184670 02020202
    .word  0x02020202                     @ 08184674 02020202
    .word  0x02020202                     @ 08184678 02020202
    .word  0x02020202                     @ 0818467c 02020202
    .word  0x02020202                     @ 08184680 02020202
    .word  0x02020202                     @ 08184684 02020202
    .word  0x02020202                     @ 08184688 02020202
    .word  0x02020202                     @ 0818468c 02020202
    .word  0x02020202                     @ 08184690 02020202
    .word  0x02020202                     @ 08184694 02020202
    .word  0x02020202                     @ 08184698 02020202
    .word  0x02020202                     @ 0818469c 02020202
    .word  0x02020202                     @ 081846a0 02020202
    .word  0x02020202                     @ 081846a4 02020202
    .word  0x02020202                     @ 081846a8 02020202
    .word  0x02020202                     @ 081846ac 02020202
    .word  0x02020202                     @ 081846b0 02020202
    .word  0x02020202                     @ 081846b4 02020202
    .word  0x02020202                     @ 081846b8 02020202
    .word  0x02020202                     @ 081846bc 02020202
    .word  0x02020202                     @ 081846c0 02020202
    .word  0x02020202                     @ 081846c4 02020202
    .word  0x02020202                     @ 081846c8 02020202
    .word  0x02020202                     @ 081846cc 02020202
    .word  0x02020202                     @ 081846d0 02020202
    .word  0x02020202                     @ 081846d4 02020202
    .word  0x02020202                     @ 081846d8 02020202
    .word  0x02020202                     @ 081846dc 02020202
    .word  0x02020202                     @ 081846e0 02020202
    .word  0x02020202                     @ 081846e4 02020202
    .word  0x02020202                     @ 081846e8 02020202
    .word  0x02020202                     @ 081846ec 02020202
    .word  0x02020202                     @ 081846f0 02020202
    .word  0x02020202                     @ 081846f4 02020202
    .word  0x02020202                     @ 081846f8 02020202
    .word  0x02020202                     @ 081846fc 02020202
    .word  0x02020202                     @ 08184700 02020202
    .word  0x02020202                     @ 08184704 02020202
    .word  0x02020202                     @ 08184708 02020202
    .word  0x02020202                     @ 0818470c 02020202
    .word  0x02020202                     @ 08184710 02020202
    .word  0x02020202                     @ 08184714 02020202
    .word  0x02020202                     @ 08184718 02020202
    .word  0x02020202                     @ 0818471c 02020202
    .word  0x02020202                     @ 08184720 02020202
    .word  0x02020202                     @ 08184724 02020202
    .word  0x02020202                     @ 08184728 02020202
    .word  0x02020202                     @ 0818472c 02020202
    .word  0x02020202                     @ 08184730 02020202
    .word  0x02020202                     @ 08184734 02020202
    .word  0x02020202                     @ 08184738 02020202
    .word  0x02020202                     @ 0818473c 02020202
    .word  0x02020202                     @ 08184740 02020202
    .word  0x02020202                     @ 08184744 02020202
    .word  0x02020202                     @ 08184748 02020202
    .word  0x02020202                     @ 0818474c 02020202
    .word  0x02020202                     @ 08184750 02020202
    .word  0x02020202                     @ 08184754 02020202
    .word  0x02020202                     @ 08184758 02020202
    .word  0x02020202                     @ 0818475c 02020202
    .word  0x02020202                     @ 08184760 02020202
    .word  0x02020202                     @ 08184764 02020202
    .word  0x02020202                     @ 08184768 02020202
    .word  0x02020202                     @ 0818476c 02020202
    .word  0x02020202                     @ 08184770 02020202
    .word  0x02020202                     @ 08184774 02020202
    .word  0x02020202                     @ 08184778 02020202
    .word  0x02020202                     @ 0818477c 02020202
    .word  0x02020202                     @ 08184780 02020202
    .word  0x02020202                     @ 08184784 02020202
    .word  0x02020202                     @ 08184788 02020202
    .word  0x02020202                     @ 0818478c 02020202
    .word  0x02020202                     @ 08184790 02020202
    .word  0x02020202                     @ 08184794 02020202
    .word  0x02020202                     @ 08184798 02020202
    .word  0x02020202                     @ 0818479c 02020202
    .word  0x02020202                     @ 081847a0 02020202
    .word  0x02020202                     @ 081847a4 02020202
    .word  0x02020202                     @ 081847a8 02020202
    .word  0x02020202                     @ 081847ac 02020202
    .word  0x02020202                     @ 081847b0 02020202
    .word  0x02020202                     @ 081847b4 02020202
    .word  0x02020202                     @ 081847b8 02020202
    .word  0x02020202                     @ 081847bc 02020202
    .word  0x02020202                     @ 081847c0 02020202
    .word  0x02020202                     @ 081847c4 02020202
    .word  0x02020202                     @ 081847c8 02020202
    .word  0x02020202                     @ 081847cc 02020202
    .word  0x02020202                     @ 081847d0 02020202
    .word  0x02020202                     @ 081847d4 02020202
    .word  0x02020202                     @ 081847d8 02020202
    .word  0x02020202                     @ 081847dc 02020202
    .word  0x02020202                     @ 081847e0 02020202
    .word  0x02020202                     @ 081847e4 02020202
    .word  0x02020202                     @ 081847e8 02020202
    .word  0x02020202                     @ 081847ec 02020202
    .word  0x02020202                     @ 081847f0 02020202
    .word  0x02020202                     @ 081847f4 02020202
    .word  0x02020202                     @ 081847f8 02020202
    .word  0x02020202                     @ 081847fc 02020202
    .word  0x02020202                     @ 08184800 02020202
    .word  0x02020202                     @ 08184804 02020202
    .word  0x02020202                     @ 08184808 02020202
    .word  0x02020202                     @ 0818480c 02020202
    .word  0x02020202                     @ 08184810 02020202
    .word  0x02020202                     @ 08184814 02020202
    .word  0x02020202                     @ 08184818 02020202
    .word  0x02020202                     @ 0818481c 02020202
    .word  0x02020202                     @ 08184820 02020202
    .word  0x02020202                     @ 08184824 02020202
    .word  0x02020202                     @ 08184828 02020202
    .word  0x02020202                     @ 0818482c 02020202
    .word  0x02020202                     @ 08184830 02020202
    .word  0x02020202                     @ 08184834 02020202
    .word  0x02020202                     @ 08184838 02020202
    .word  0x02020202                     @ 0818483c 02020202
    .word  0x02020202                     @ 08184840 02020202
    .word  0x02020202                     @ 08184844 02020202
    .word  0x02020202                     @ 08184848 02020202
    .word  0x02020202                     @ 0818484c 02020202
    .word  0x02020202                     @ 08184850 02020202
    .word  0x02020202                     @ 08184854 02020202
    .word  0x02020202                     @ 08184858 02020202
    .word  0x02020202                     @ 0818485c 02020202
    .word  0x02020202                     @ 08184860 02020202
    .word  0x02020202                     @ 08184864 02020202
    .word  0x02020202                     @ 08184868 02020202
    .word  0x02020202                     @ 0818486c 02020202
    .word  0x02020202                     @ 08184870 02020202
    .word  0x02020202                     @ 08184874 02020202
    .word  0x02020202                     @ 08184878 02020202
    .word  0x02020202                     @ 0818487c 02020202
    .word  0x02020202                     @ 08184880 02020202
    .word  0x02020202                     @ 08184884 02020202
    .word  0x02020202                     @ 08184888 02020202
    .word  0x02020202                     @ 0818488c 02020202
    .word  0x02020202                     @ 08184890 02020202
    .word  0x02020202                     @ 08184894 02020202
    .word  0x02020202                     @ 08184898 02020202
    .word  0x02020202                     @ 0818489c 02020202
    .word  0x02020202                     @ 081848a0 02020202
    .word  0x02020202                     @ 081848a4 02020202
    .word  0x02020202                     @ 081848a8 02020202
    .word  0x02020202                     @ 081848ac 02020202
    .word  0x02020202                     @ 081848b0 02020202
    .word  0x02020202                     @ 081848b4 02020202
    .word  0x02020202                     @ 081848b8 02020202
    .word  0x02020202                     @ 081848bc 02020202
    .word  0x02020202                     @ 081848c0 02020202
    .word  0x02020202                     @ 081848c4 02020202
    .word  0x02020202                     @ 081848c8 02020202
    .word  0x02020202                     @ 081848cc 02020202
    .word  0x02020202                     @ 081848d0 02020202
    .word  0x02020202                     @ 081848d4 02020202
    .word  0x02020202                     @ 081848d8 02020202
    .word  0x02020202                     @ 081848dc 02020202
    .word  0x02020202                     @ 081848e0 02020202
    .word  0x02020202                     @ 081848e4 02020202
    .word  0x02020202                     @ 081848e8 02020202
    .word  0x02020202                     @ 081848ec 02020202
    .word  0x02020202                     @ 081848f0 02020202
    .word  0x02020202                     @ 081848f4 02020202
    .word  0x02020202                     @ 081848f8 02020202
    .word  0x02020202                     @ 081848fc 02020202
    .word  0x02020202                     @ 08184900 02020202
    .word  0x02020202                     @ 08184904 02020202
    .word  0x02020202                     @ 08184908 02020202
    .word  0x02020202                     @ 0818490c 02020202
    .word  0x02020202                     @ 08184910 02020202
    .word  0x02020202                     @ 08184914 02020202
    .word  0x02020202                     @ 08184918 02020202
    .word  0x02020202                     @ 0818491c 02020202
    .word  0x02020202                     @ 08184920 02020202
    .word  0x02020202                     @ 08184924 02020202
    .word  0x02020202                     @ 08184928 02020202
    .word  0x02020202                     @ 0818492c 02020202
    .word  0x02020202                     @ 08184930 02020202
    .word  0x02020202                     @ 08184934 02020202
    .word  0x02020202                     @ 08184938 02020202
    .word  0x02020202                     @ 0818493c 02020202
    .word  0x02020202                     @ 08184940 02020202
    .word  0x02020202                     @ 08184944 02020202
    .word  0x02020202                     @ 08184948 02020202
    .word  0x02020202                     @ 0818494c 02020202
    .word  0x02020202                     @ 08184950 02020202
    .word  0x02020202                     @ 08184954 02020202
    .word  0x02020202                     @ 08184958 02020202
    .word  0x02020202                     @ 0818495c 02020202
    .word  0x02020202                     @ 08184960 02020202
    .word  0x02020202                     @ 08184964 02020202
    .word  0x02020202                     @ 08184968 02020202
    .word  0x02020202                     @ 0818496c 02020202
    .word  0x02020202                     @ 08184970 02020202
    .word  0x02020202                     @ 08184974 02020202
    .word  0x02020202                     @ 08184978 02020202
    .word  0x02020202                     @ 0818497c 02020202
    .word  0x02020202                     @ 08184980 02020202
    .word  0x02020202                     @ 08184984 02020202
    .word  0x02020202                     @ 08184988 02020202
    .word  0x02020202                     @ 0818498c 02020202
    .word  0x02020202                     @ 08184990 02020202
    .word  0x02020202                     @ 08184994 02020202
    .word  0x02020202                     @ 08184998 02020202
    .word  0x02020202                     @ 0818499c 02020202
    .word  0x02020202                     @ 081849a0 02020202
    .word  0x02020202                     @ 081849a4 02020202
    .word  0x02020202                     @ 081849a8 02020202
    .word  0x02020202                     @ 081849ac 02020202
    .word  0x02020202                     @ 081849b0 02020202
    .word  0x02020202                     @ 081849b4 02020202
    .word  0x02020202                     @ 081849b8 02020202
    .word  0x02020202                     @ 081849bc 02020202
    ROM_INCBIN 0x1849c0, 0x94c8
    .word  0x02020203                     @ 0818de88 03020202
    .word  0x02020202                     @ 0818de8c 02020202
    .word  0x02030302                     @ 0818de90 02030302
    .word  0x02030202                     @ 0818de94 02020302
    .word  0x02020202                     @ 0818de98 02020202
    .word  0x02020202                     @ 0818de9c 02020202
    ROM_INCBIN 0x18dea0, 0xc8
    .word  0x02020000                     @ 0818df68 00000202
    .word  0x02020202                     @ 0818df6c 02020202
    .word  0x02020202                     @ 0818df70 02020202
    .word  0x02020202                     @ 0818df74 02020202
    .word  0x02020202                     @ 0818df78 02020202
    .word  0x02030202                     @ 0818df7c 02020302
    .word  0x02020002                     @ 0818df80 02000202
    .word  0x02020202                     @ 0818df84 02020202
    .word  0x02000002                     @ 0818df88 02000002
    ROM_INCBIN 0x18df8c, 0x254
    .word  0x02020203                     @ 0818e1e0 03020202
    .word  0x02030303                     @ 0818e1e4 03030302
    .word  0x02030202                     @ 0818e1e8 02020302
    .word  0x02020202                     @ 0818e1ec 02020202
    .word  0x02020202                     @ 0818e1f0 02020202
    .word  0x02020202                     @ 0818e1f4 02020202
    .word  0x02020202                     @ 0818e1f8 02020202
    .word  0x02020202                     @ 0818e1fc 02020202
    ROM_INCBIN 0x18e200, 0x100
    .word  0x02020200                     @ 0818e300 00020202
    .word  0x02020202                     @ 0818e304 02020202
    .word  0x02020202                     @ 0818e308 02020202
    .word  0x02020202                     @ 0818e30c 02020202
    .word  0x02020202                     @ 0818e310 02020202
    .word  0x02020202                     @ 0818e314 02020202
    .word  0x02020202                     @ 0818e318 02020202
    .word  0x02020202                     @ 0818e31c 02020202
    .word  0x02020202                     @ 0818e320 02020202
    .word  0x02020202                     @ 0818e324 02020202
    ROM_INCBIN 0x18e328, 0x6c
    .word  0x02020202                     @ 0818e394 02020202
    .word  0x02020202                     @ 0818e398 02020202
    .word  0x02020202                     @ 0818e39c 02020202
    .word  0x02020202                     @ 0818e3a0 02020202
    .word  0x02020202                     @ 0818e3a4 02020202
    .word  0x02020202                     @ 0818e3a8 02020202
    ROM_INCBIN 0x18e3ac, 0x2c
    .word  0x02020000                     @ 0818e3d8 00000202
    .word  0x02020002                     @ 0818e3dc 02000202
    .word  0x02020202                     @ 0818e3e0 02020202
    .word  0x02020202                     @ 0818e3e4 02020202
    .word  0x02020202                     @ 0818e3e8 02020202
    ROM_INCBIN 0x18e3ec, 0x50
    .word  0x02020200                     @ 0818e43c 00020202
    .word  0x02020000                     @ 0818e440 00000202
    .word  0x02020202                     @ 0818e444 02020202
    .word  0x02020202                     @ 0818e448 02020202
    .word  0x02020202                     @ 0818e44c 02020202
    .word  0x02020202                     @ 0818e450 02020202
    .word  0x02020202                     @ 0818e454 02020202
    .word  0x02020202                     @ 0818e458 02020202
    .word  0x02020202                     @ 0818e45c 02020202
    .word  0x02020202                     @ 0818e460 02020202
    .word  0x02020202                     @ 0818e464 02020202
    .word  0x02020202                     @ 0818e468 02020202
    .word  0x02020202                     @ 0818e46c 02020202
    ROM_INCBIN 0x18e470, 0x44
    .word  0x02020202                     @ 0818e4b4 02020202
    .word  0x02020202                     @ 0818e4b8 02020202
    .word  0x02020202                     @ 0818e4bc 02020202
    .word  0x02020202                     @ 0818e4c0 02020202
    .word  0x02020202                     @ 0818e4c4 02020202
    .word  0x02020202                     @ 0818e4c8 02020202
    .word  0x02000202                     @ 0818e4cc 02020002
    ROM_INCBIN 0x18e4d0, 0x38
    .word  0x02020200                     @ 0818e508 00020202
    .word  0x02000002                     @ 0818e50c 02000002
    .word  0x02020202                     @ 0818e510 02020202
    .word  0x02020202                     @ 0818e514 02020202
    .word  0x02020202                     @ 0818e518 02020202
    .word  0x02020202                     @ 0818e51c 02020202
    .word  0x02020202                     @ 0818e520 02020202
    .word  0x02020202                     @ 0818e524 02020202
    .word  0x02020202                     @ 0818e528 02020202
    .word  0x02020202                     @ 0818e52c 02020202
    .word  0x02020202                     @ 0818e530 02020202
    .word  0x02020202                     @ 0818e534 02020202
    .word  0x02020202                     @ 0818e538 02020202
    .word  0x02020202                     @ 0818e53c 02020202
    .word  0x02020202                     @ 0818e540 02020202
    .word  0x02020202                     @ 0818e544 02020202
    .word  0x02020202                     @ 0818e548 02020202
    .word  0x02020202                     @ 0818e54c 02020202
    .word  0x02020202                     @ 0818e550 02020202
    .word  0x02020202                     @ 0818e554 02020202
    .word  0x02020202                     @ 0818e558 02020202
    .word  0x02020202                     @ 0818e55c 02020202
    ROM_INCBIN 0x18e560, 0xb0
    .word  0x02000000                     @ 0818e610 00000002
    .word  0x02020202                     @ 0818e614 02020202
    .word  0x02020202                     @ 0818e618 02020202
    .word  0x02020202                     @ 0818e61c 02020202
    .word  0x02020202                     @ 0818e620 02020202
    .word  0x02020202                     @ 0818e624 02020202
    .word  0x02020202                     @ 0818e628 02020202
    .word  0x02020202                     @ 0818e62c 02020202
    .word  0x02020202                     @ 0818e630 02020202
    ROM_INCBIN 0x18e634, 0x68
    .word  0x02020200                     @ 0818e69c 00020202
    .word  0x02020202                     @ 0818e6a0 02020202
    .word  0x02020202                     @ 0818e6a4 02020202
    .word  0x02020202                     @ 0818e6a8 02020202
    .word  0x02020202                     @ 0818e6ac 02020202
    .word  0x02020202                     @ 0818e6b0 02020202
    .word  0x02020202                     @ 0818e6b4 02020202
    .word  0x02020202                     @ 0818e6b8 02020202
    .word  0x02020202                     @ 0818e6bc 02020202
    ROM_INCBIN 0x18e6c0, 0xac
    .word  0x02020200                     @ 0818e76c 00020202
    .word  0x02020202                     @ 0818e770 02020202
    .word  0x02020202                     @ 0818e774 02020202
    .word  0x02020202                     @ 0818e778 02020202
    .word  0x02020202                     @ 0818e77c 02020202
    ROM_INCBIN 0x18e780, 0x154
    .word  0x02020000                     @ 0818e8d4 00000202
    .word  0x02020202                     @ 0818e8d8 02020202
    .word  0x02020202                     @ 0818e8dc 02020202
    .word  0x02020202                     @ 0818e8e0 02020202
    .word  0x02020202                     @ 0818e8e4 02020202
    .word  0x02020002                     @ 0818e8e8 02000202
    ROM_INCBIN 0x18e8ec, 0x98
    .word  0x02000000                     @ 0818e984 00000002
    .word  0x02020202                     @ 0818e988 02020202
    .word  0x02020202                     @ 0818e98c 02020202
    .word  0x02020202                     @ 0818e990 02020202
    .word  0x02020202                     @ 0818e994 02020202
    .word  0x02020202                     @ 0818e998 02020202
    .word  0x02020202                     @ 0818e99c 02020202
    .word  0x02020202                     @ 0818e9a0 02020202
    ROM_INCBIN 0x18e9a4, 0x57dc
DWORD_08194180:
    .word  0x081944e0                     @ 08194180 e0441908
DWORD_08194184:
    .word  0x000e0000                     @ 08194184 00000e00
    ROM_INCBIN 0x194188, 0x3604
    .word  0x09a916a8                     @ 0819778c a816a909
    .word  0x08a920a8                     @ 08197790 a820a908
    .word  0x09a622a8                     @ 08197794 a822a609
    .word  0x08a718a8                     @ 08197798 a818a708
    .word  0x08a822a8                     @ 0819779c a822a808
    ROM_INCBIN 0x1977a0, 0xbc
    .word  0x0901a422                     @ 0819785c 22a40109
    .word  0x08af0aa8                     @ 08197860 a80aaf08
    .word  0x08af0aa8                     @ 08197864 a80aaf08
    .word  0x09a622a8                     @ 08197868 a822a609
    .word  0x08a718a8                     @ 0819786c a818a708
    ROM_INCBIN 0x197870, 0x1e4
    .word  0x08a518a8                     @ 08197a54 a818a508
    .word  0x08a922a8                     @ 08197a58 a822a908
    .word  0x09a518a8                     @ 08197a5c a818a509
    .word  0x08a922a8                     @ 08197a60 a822a908
    .word  0x09a818a8                     @ 08197a64 a818a809
    .word  0x08a922a8                     @ 08197a68 a822a908
    ROM_INCBIN 0x197a6c, 0x2f0
    .word  0x0901af18                     @ 08197d5c 18af0109
    .word  0x08b122a8                     @ 08197d60 a822b108
    .word  0x08b018a8                     @ 08197d64 a818b008
    .word  0x09ac22a8                     @ 08197d68 a822ac09
    .word  0x08af0aa8                     @ 08197d6c a80aaf08
    .word  0x09a522a8                     @ 08197d70 a822a509
    .word  0x08af0aa8                     @ 08197d74 a80aaf08
    .word  0x08a922a8                     @ 08197d78 a822a908
    ROM_INCBIN 0x197d7c, 0x25a68
    .word  0x09a119a8                     @ 081bd7e4 a819a109
    .word  0x08a219a8                     @ 081bd7e8 a819a208
    .word  0x09942aa8                     @ 081bd7ec a82a9409
    .word  0x089c19a8                     @ 081bd7f0 a8199c08
    .word  0x099519a8                     @ 081bd7f4 a8199509
    .word  0x089619a8                     @ 081bd7f8 a8199608
    ROM_INCBIN 0x1bd7fc, 0x1d4
    .word  0x08a219a8                     @ 081bd9d0 a819a208
    .word  0x09942aa8                     @ 081bd9d4 a82a9409
    .word  0x089c19a8                     @ 081bd9d8 a8199c08
    .word  0x099519a8                     @ 081bd9dc a8199509
    .word  0x099619a8                     @ 081bd9e0 a8199609
    .word  0x089721a8                     @ 081bd9e4 a8219708
    ROM_INCBIN 0x1bd9e8, 0x15c
    .word  0x09a119a8                     @ 081bdb44 a819a109
    .word  0x08a219a8                     @ 081bdb48 a819a208
    .word  0x09942aa8                     @ 081bdb4c a82a9409
    .word  0x089c19a8                     @ 081bdb50 a8199c08
    .word  0x099519a8                     @ 081bdb54 a8199509
    .word  0x089619a8                     @ 081bdb58 a8199608
    ROM_INCBIN 0x1bdb5c, 0x114
    .word  0x099d21a8                     @ 081bdc70 a8219d09
    .word  0x099e19a8                     @ 081bdc74 a8199e09
    .word  0x089f21a8                     @ 081bdc78 a8219f08
    .word  0x099710a8                     @ 081bdc7c a8109709
    .word  0x08a119a8                     @ 081bdc80 a819a108
    ROM_INCBIN 0x1bdc84, 0x214
    .word  0x09942aa8                     @ 081bde98 a82a9409
    .word  0x089c19a8                     @ 081bde9c a8199c08
    .word  0x099519a8                     @ 081bdea0 a8199509
    .word  0x099619a8                     @ 081bdea4 a8199609
    .word  0x089721a8                     @ 081bdea8 a8219708
    ROM_INCBIN 0x1bdeac, 0x20
    .word  0x099519a8                     @ 081bdecc a8199509
    .word  0x089b2aa8                     @ 081bded0 a82a9b08
    .word  0x099619a8                     @ 081bded4 a8199609
    .word  0x099721a8                     @ 081bded8 a8219709
    .word  0x089919a8                     @ 081bdedc a8199908
    ROM_INCBIN 0x1bdee0, 0x2e7c
    .word  0x09bc1fa8                     @ 081c0d5c a81fbc09
    .word  0x08be1fa8                     @ 081c0d60 a81fbe08
    .word  0x08bf1fa8                     @ 081c0d64 a81fbf08
    .word  0x08c01fa8                     @ 081c0d68 a81fc008
    .word  0x08c11fa8                     @ 081c0d6c a81fc108
    ROM_INCBIN 0x1c0d70, 0x8c
    .word  0x08bc1fa8                     @ 081c0dfc a81fbc08
    .word  0x08bd1fa8                     @ 081c0e00 a81fbd08
    .word  0x08be1fa8                     @ 081c0e04 a81fbe08
    .word  0x08b323a8                     @ 081c0e08 a823b308
    .word  0x08b41fa8                     @ 081c0e0c a81fb408
    ROM_INCBIN 0x1c0e10, 0x2b8
    .word  0x08bd1fa8                     @ 081c10c8 a81fbd08
    .word  0x08bc1fa8                     @ 081c10cc a81fbc08
    .word  0x08c01fa8                     @ 081c10d0 a81fc008
    .word  0x08bf1fa8                     @ 081c10d4 a81fbf08
    .word  0x08be1fa8                     @ 081c10d8 a81fbe08
    ROM_INCBIN 0x1c10dc, 0x1e8
    .word  0x08bd1fa8                     @ 081c12c4 a81fbd08
    .word  0x08bc1fa8                     @ 081c12c8 a81fbc08
    .word  0x08be1fa8                     @ 081c12cc a81fbe08
    .word  0x08bf1fa8                     @ 081c12d0 a81fbf08
    .word  0x08b91fa8                     @ 081c12d4 a81fb908
    ROM_INCBIN 0x1c12d8, 0x18
    .word  0x08b91fa8                     @ 081c12f0 a81fb908
    .word  0x09b51fa8                     @ 081c12f4 a81fb509
    .word  0x08c11fa8                     @ 081c12f8 a81fc108
    .word  0x08b91fa8                     @ 081c12fc a81fb908
    .word  0x08b323a8                     @ 081c1300 a823b308
    .word  0x08b91fa8                     @ 081c1304 a81fb908
    .word  0x09b323a8                     @ 081c1308 a823b309
    .word  0x08b41fa8                     @ 081c130c a81fb408
    .word  0x08b91fa8                     @ 081c1310 a81fb908
    .word  0x08b71fa8                     @ 081c1314 a81fb708
    ROM_INCBIN 0x1c1318, 0x28
    .word  0x08b51fa8                     @ 081c1340 a81fb508
    .word  0x08b61fa8                     @ 081c1344 a81fb608
    .word  0x08b71fa8                     @ 081c1348 a81fb708
    .word  0x08b81fa8                     @ 081c134c a81fb808
    .word  0x08b91fa8                     @ 081c1350 a81fb908
    .byte  0xa8, 0x1f, 0xba, 0x09
    .word  0x08bf1fa8                     @ 081c1358 a81fbf08
    .word  0x08c01fa8                     @ 081c135c a81fc008
    .word  0x08c11fa8                     @ 081c1360 a81fc108
    .word  0x08c21fa8                     @ 081c1364 a81fc208
    .word  0x09b323a8                     @ 081c1368 a823b309
    .word  0x08b41fa8                     @ 081c136c a81fb408
    .word  0x08b51fa8                     @ 081c1370 a81fb508
    .word  0x08b61fa8                     @ 081c1374 a81fb608
    .word  0x08b71fa8                     @ 081c1378 a81fb708
    ROM_INCBIN 0x1c137c, 0x37b0
    .word  0x08b520a8                     @ 081c4b2c a820b508
    .word  0x08b620a8                     @ 081c4b30 a820b608
    .word  0x08b728a8                     @ 081c4b34 a828b708
    .word  0x08b820a8                     @ 081c4b38 a820b808
    .word  0x08ba30a8                     @ 081c4b3c a830ba08
    .word  0x08b920a8                     @ 081c4b40 a820b908
    .word  0x08bb20a8                     @ 081c4b44 a820bb08
    .word  0x08bc20a8                     @ 081c4b48 a820bc08
    .word  0x08bd20a8                     @ 081c4b4c a820bd08
    .word  0x08be20a8                     @ 081c4b50 a820be08
    .word  0x08bf28a8                     @ 081c4b54 a828bf08
    .word  0x08c020a8                     @ 081c4b58 a820c008
    .word  0x08c120a8                     @ 081c4b5c a820c108
    .word  0x08c220a8                     @ 081c4b60 a820c208
    .word  0x08b330a8                     @ 081c4b64 a830b308
    .word  0x08b820a8                     @ 081c4b68 a820b808
    .word  0x08b520a8                     @ 081c4b6c a820b508
    .word  0x08b620a8                     @ 081c4b70 a820b608
    .word  0x08b728a8                     @ 081c4b74 a828b708
    .word  0x08b820a8                     @ 081c4b78 a820b808
    .word  0x08b920a8                     @ 081c4b7c a820b908
    .word  0x08ba20a8                     @ 081c4b80 a820ba08
    .word  0x08bb20a8                     @ 081c4b84 a820bb08
    .word  0x08bc20a8                     @ 081c4b88 a820bc08
    .word  0x08bd30a8                     @ 081c4b8c a830bd08
    .word  0x08be20a8                     @ 081c4b90 a820be08
    ROM_INCBIN 0x1c4b94, 0x14
    .word  0x08b520a8                     @ 081c4ba8 a820b508
    .word  0x08b620a8                     @ 081c4bac a820b608
    .word  0x08b728a8                     @ 081c4bb0 a828b708
    .word  0x08b820a8                     @ 081c4bb4 a820b808
    .word  0x08ba30a8                     @ 081c4bb8 a830ba08
    .word  0x08b920a8                     @ 081c4bbc a820b908
    .word  0x08bb20a8                     @ 081c4bc0 a820bb08
    .word  0x08bc20a8                     @ 081c4bc4 a820bc08
    .word  0x08bd20a8                     @ 081c4bc8 a820bd08
    .word  0x08be20a8                     @ 081c4bcc a820be08
    .word  0x08bf28a8                     @ 081c4bd0 a828bf08
    .word  0x08c020a8                     @ 081c4bd4 a820c008
    .word  0x08c120a8                     @ 081c4bd8 a820c108
    .word  0x08c220a8                     @ 081c4bdc a820c208
    .word  0x08b330a8                     @ 081c4be0 a830b308
    .word  0x08b820a8                     @ 081c4be4 a820b808
    .word  0x08b520a8                     @ 081c4be8 a820b508
    .word  0x08b620a8                     @ 081c4bec a820b608
    .word  0x08b728a8                     @ 081c4bf0 a828b708
    .word  0x08b820a8                     @ 081c4bf4 a820b808
    .word  0x08b920a8                     @ 081c4bf8 a820b908
    .word  0x08ba20a8                     @ 081c4bfc a820ba08
    .byte  0xa8, 0x20, 0xbb, 0x09
    .word  0x08bc20a8                     @ 081c4c04 a820bc08
    .word  0x08bd30a8                     @ 081c4c08 a830bd08
    .word  0x08be20a8                     @ 081c4c0c a820be08
    .word  0x08bf28a8                     @ 081c4c10 a828bf08
    .word  0x08c020a8                     @ 081c4c14 a820c008
    .word  0x08c120a8                     @ 081c4c18 a820c108
    .word  0x08c220a8                     @ 081c4c1c a820c208
    .byte  0xa8, 0x30, 0xb3, 0x10
    .word  0x08b520a8                     @ 081c4c24 a820b508
    .word  0x08b620a8                     @ 081c4c28 a820b608
    .word  0x08b728a8                     @ 081c4c2c a828b708
    .word  0x08b820a8                     @ 081c4c30 a820b808
    .word  0x08ba30a8                     @ 081c4c34 a830ba08
    .word  0x08b920a8                     @ 081c4c38 a820b908
    .word  0x08bb20a8                     @ 081c4c3c a820bb08
    .word  0x08bc20a8                     @ 081c4c40 a820bc08
    .word  0x08bd20a8                     @ 081c4c44 a820bd08
    .word  0x08be20a8                     @ 081c4c48 a820be08
    .word  0x08bf28a8                     @ 081c4c4c a828bf08
    .word  0x08c020a8                     @ 081c4c50 a820c008
    .word  0x08c120a8                     @ 081c4c54 a820c108
    .word  0x08c220a8                     @ 081c4c58 a820c208
    .word  0x08b330a8                     @ 081c4c5c a830b308
    .word  0x08b820a8                     @ 081c4c60 a820b808
    .word  0x08b520a8                     @ 081c4c64 a820b508
    .word  0x08b620a8                     @ 081c4c68 a820b608
    .byte  0xa8, 0x28, 0xb7, 0x09
    .word  0x08b820a8                     @ 081c4c70 a820b808
    .word  0x08b920a8                     @ 081c4c74 a820b908
    .word  0x08ba20a8                     @ 081c4c78 a820ba08
    .word  0x08bb20a8                     @ 081c4c7c a820bb08
    .word  0x08bc20a8                     @ 081c4c80 a820bc08
    .word  0x08bd30a8                     @ 081c4c84 a830bd08
    .word  0x08be20a8                     @ 081c4c88 a820be08
    .word  0x08bf28a8                     @ 081c4c8c a828bf08
    .word  0x08c020a8                     @ 081c4c90 a820c008
    .word  0x08c120a8                     @ 081c4c94 a820c108
    .word  0x08c220a8                     @ 081c4c98 a820c208
    .byte  0xa8, 0x30, 0xb3, 0x10
    .word  0x08b520a8                     @ 081c4ca0 a820b508
    .word  0x08b620a8                     @ 081c4ca4 a820b608
    .word  0x08b728a8                     @ 081c4ca8 a828b708
    .word  0x08b820a8                     @ 081c4cac a820b808
    .word  0x08ba30a8                     @ 081c4cb0 a830ba08
    .word  0x08b920a8                     @ 081c4cb4 a820b908
    .word  0x08bb20a8                     @ 081c4cb8 a820bb08
    .word  0x08bc20a8                     @ 081c4cbc a820bc08
    .word  0x08bd20a8                     @ 081c4cc0 a820bd08
    .word  0x08be20a8                     @ 081c4cc4 a820be08
    .word  0x08bf28a8                     @ 081c4cc8 a828bf08
    .word  0x08c020a8                     @ 081c4ccc a820c008
    .word  0x08c120a8                     @ 081c4cd0 a820c108
    .word  0x08c220a8                     @ 081c4cd4 a820c208
    .word  0x09b330a8                     @ 081c4cd8 a830b309
    .word  0x08b820a8                     @ 081c4cdc a820b808
    .word  0x08b520a8                     @ 081c4ce0 a820b508
    .word  0x08b620a8                     @ 081c4ce4 a820b608
    .word  0x08b728a8                     @ 081c4ce8 a828b708
    .word  0x08b820a8                     @ 081c4cec a820b808
    .word  0x08b920a8                     @ 081c4cf0 a820b908
    .word  0x08ba20a8                     @ 081c4cf4 a820ba08
    .word  0x08bb20a8                     @ 081c4cf8 a820bb08
    .word  0x08bc20a8                     @ 081c4cfc a820bc08
    .word  0x08bd30a8                     @ 081c4d00 a830bd08
    .word  0x08be20a8                     @ 081c4d04 a820be08
    .word  0x08bf28a8                     @ 081c4d08 a828bf08
    .word  0x08c020a8                     @ 081c4d0c a820c008
    .word  0x08c120a8                     @ 081c4d10 a820c108
    .word  0x08c220a8                     @ 081c4d14 a820c208
    .byte  0xa8, 0x30, 0xb3, 0x10
    .word  0x08b520a8                     @ 081c4d1c a820b508
    .word  0x08b620a8                     @ 081c4d20 a820b608
    .word  0x08b728a8                     @ 081c4d24 a828b708
    .word  0x08b820a8                     @ 081c4d28 a820b808
    .word  0x08ba30a8                     @ 081c4d2c a830ba08
    .word  0x08b920a8                     @ 081c4d30 a820b908
    .word  0x08bb20a8                     @ 081c4d34 a820bb08
    .word  0x08bc20a8                     @ 081c4d38 a820bc08
    .word  0x08bd20a8                     @ 081c4d3c a820bd08
    .word  0x08be20a8                     @ 081c4d40 a820be08
    .byte  0xa8, 0x28, 0xbf, 0x09
    .word  0x08c020a8                     @ 081c4d48 a820c008
    .word  0x08c120a8                     @ 081c4d4c a820c108
    .word  0x08c220a8                     @ 081c4d50 a820c208
    .word  0x08b330a8                     @ 081c4d54 a830b308
    .word  0x08b820a8                     @ 081c4d58 a820b808
    .word  0x08b520a8                     @ 081c4d5c a820b508
    .word  0x08b620a8                     @ 081c4d60 a820b608
    .word  0x08b728a8                     @ 081c4d64 a828b708
    .word  0x08b820a8                     @ 081c4d68 a820b808
    .word  0x08b920a8                     @ 081c4d6c a820b908
    .word  0x08ba20a8                     @ 081c4d70 a820ba08
    .word  0x08bb20a8                     @ 081c4d74 a820bb08
    .word  0x08bc20a8                     @ 081c4d78 a820bc08
    .word  0x08bd30a8                     @ 081c4d7c a830bd08
    .word  0x08be20a8                     @ 081c4d80 a820be08
    .word  0x08bf28a8                     @ 081c4d84 a828bf08
    .word  0x08c020a8                     @ 081c4d88 a820c008
    .word  0x08c120a8                     @ 081c4d8c a820c108
    .word  0x08c220a8                     @ 081c4d90 a820c208
    .byte  0xa8, 0x30, 0xb3, 0x10
    .word  0x08b520a8                     @ 081c4d98 a820b508
    .word  0x08b620a8                     @ 081c4d9c a820b608
    .word  0x08b728a8                     @ 081c4da0 a828b708
    .word  0x08b820a8                     @ 081c4da4 a820b808
    .word  0x08ba30a8                     @ 081c4da8 a830ba08
    .word  0x08b920a8                     @ 081c4dac a820b908
    .byte  0xa8, 0x20, 0xbb, 0x09
    .word  0x08bc20a8                     @ 081c4db4 a820bc08
    .word  0x08bd20a8                     @ 081c4db8 a820bd08
    .word  0x08be20a8                     @ 081c4dbc a820be08
    .word  0x08bf28a8                     @ 081c4dc0 a828bf08
    .word  0x08c020a8                     @ 081c4dc4 a820c008
    .word  0x08c120a8                     @ 081c4dc8 a820c108
    .word  0x08c220a8                     @ 081c4dcc a820c208
    .word  0x08b330a8                     @ 081c4dd0 a830b308
    .word  0x08b820a8                     @ 081c4dd4 a820b808
    .word  0x08b520a8                     @ 081c4dd8 a820b508
    .word  0x08b620a8                     @ 081c4ddc a820b608
    .word  0x08b728a8                     @ 081c4de0 a828b708
    .word  0x08b820a8                     @ 081c4de4 a820b808
    .word  0x08b920a8                     @ 081c4de8 a820b908
    .word  0x08ba20a8                     @ 081c4dec a820ba08
    .word  0x08bb20a8                     @ 081c4df0 a820bb08
    .word  0x08bc20a8                     @ 081c4df4 a820bc08
    .word  0x08bd30a8                     @ 081c4df8 a830bd08
    .word  0x08be20a8                     @ 081c4dfc a820be08
    .word  0x08bf28a8                     @ 081c4e00 a828bf08
    .word  0x08c020a8                     @ 081c4e04 a820c008
    .word  0x08c120a8                     @ 081c4e08 a820c108
    .word  0x08c220a8                     @ 081c4e0c a820c208
    .byte  0xa8, 0x30, 0xb3, 0x10, 0xa8, 0x20, 0xb5, 0x08, 0xa8, 0x20, 0xb6, 0x08, 0xa8, 0x28, 0xb7, 0x09
    .word  0x08b820a8                     @ 081c4e20 a820b808
    .word  0x08ba30a8                     @ 081c4e24 a830ba08
    .word  0x08b920a8                     @ 081c4e28 a820b908
    .word  0x08bb20a8                     @ 081c4e2c a820bb08
    .word  0x08bc20a8                     @ 081c4e30 a820bc08
    .word  0x08bd20a8                     @ 081c4e34 a820bd08
    .word  0x08be20a8                     @ 081c4e38 a820be08
    .word  0x08bf28a8                     @ 081c4e3c a828bf08
    .word  0x08c020a8                     @ 081c4e40 a820c008
    .word  0x08c120a8                     @ 081c4e44 a820c108
    .word  0x08c220a8                     @ 081c4e48 a820c208
    .word  0x08b330a8                     @ 081c4e4c a830b308
    .word  0x08b820a8                     @ 081c4e50 a820b808
    .word  0x08b520a8                     @ 081c4e54 a820b508
    .word  0x08b620a8                     @ 081c4e58 a820b608
    .word  0x08b728a8                     @ 081c4e5c a828b708
    .word  0x08b820a8                     @ 081c4e60 a820b808
    .word  0x08b920a8                     @ 081c4e64 a820b908
    .word  0x08ba20a8                     @ 081c4e68 a820ba08
    .word  0x08bb20a8                     @ 081c4e6c a820bb08
    .word  0x08bc20a8                     @ 081c4e70 a820bc08
    .word  0x08bd30a8                     @ 081c4e74 a830bd08
    .word  0x08be20a8                     @ 081c4e78 a820be08
    .word  0x08bf28a8                     @ 081c4e7c a828bf08
    .word  0x08c020a8                     @ 081c4e80 a820c008
    .word  0x08c120a8                     @ 081c4e84 a820c108
    .word  0x08c220a8                     @ 081c4e88 a820c208
    .byte  0xa8, 0x30, 0xb3, 0x11
    .word  0x08b520a8                     @ 081c4e90 a820b508
    .word  0x08b620a8                     @ 081c4e94 a820b608
    .word  0x08b728a8                     @ 081c4e98 a828b708
    .word  0x08b820a8                     @ 081c4e9c a820b808
    .word  0x08ba30a8                     @ 081c4ea0 a830ba08
    .word  0x08b920a8                     @ 081c4ea4 a820b908
    .word  0x08bb20a8                     @ 081c4ea8 a820bb08
    .word  0x08bc20a8                     @ 081c4eac a820bc08
    .word  0x08bd20a8                     @ 081c4eb0 a820bd08
    .word  0x08be20a8                     @ 081c4eb4 a820be08
    .word  0x08bf28a8                     @ 081c4eb8 a828bf08
    .word  0x08c020a8                     @ 081c4ebc a820c008
    .word  0x08c120a8                     @ 081c4ec0 a820c108
    .word  0x08c220a8                     @ 081c4ec4 a820c208
    .word  0x08b330a8                     @ 081c4ec8 a830b308
    .word  0x08b820a8                     @ 081c4ecc a820b808
    .word  0x08b520a8                     @ 081c4ed0 a820b508
    .word  0x08b620a8                     @ 081c4ed4 a820b608
    .word  0x08b728a8                     @ 081c4ed8 a828b708
    .word  0x08b820a8                     @ 081c4edc a820b808
    .word  0x08b920a8                     @ 081c4ee0 a820b908
    .word  0x08ba20a8                     @ 081c4ee4 a820ba08
    .word  0x08bb20a8                     @ 081c4ee8 a820bb08
    .word  0x08bc20a8                     @ 081c4eec a820bc08
    .word  0x08bd30a8                     @ 081c4ef0 a830bd08
    .word  0x08be20a8                     @ 081c4ef4 a820be08
    ROM_INCBIN 0x1c4ef8, 0x14
    .word  0x08b520a8                     @ 081c4f0c a820b508
    .word  0x08b620a8                     @ 081c4f10 a820b608
    .word  0x08b728a8                     @ 081c4f14 a828b708
    .word  0x08b820a8                     @ 081c4f18 a820b808
    .word  0x08ba30a8                     @ 081c4f1c a830ba08
    .word  0x08b920a8                     @ 081c4f20 a820b908
    .word  0x08bb20a8                     @ 081c4f24 a820bb08
    .word  0x08bc20a8                     @ 081c4f28 a820bc08
    .word  0x08bd20a8                     @ 081c4f2c a820bd08
    .word  0x08be20a8                     @ 081c4f30 a820be08
    .word  0x08bf28a8                     @ 081c4f34 a828bf08
    .word  0x08c020a8                     @ 081c4f38 a820c008
    .word  0x08c120a8                     @ 081c4f3c a820c108
    .word  0x08c220a8                     @ 081c4f40 a820c208
    .word  0x08b330a8                     @ 081c4f44 a830b308
    .word  0x08b820a8                     @ 081c4f48 a820b808
    .word  0x08b520a8                     @ 081c4f4c a820b508
    .word  0x08b620a8                     @ 081c4f50 a820b608
    .word  0x08b728a8                     @ 081c4f54 a828b708
    .word  0x08b820a8                     @ 081c4f58 a820b808
    .word  0x08b920a8                     @ 081c4f5c a820b908
    .word  0x08ba20a8                     @ 081c4f60 a820ba08
    .byte  0xa8, 0x20, 0xbb, 0x09
    .word  0x08bc20a8                     @ 081c4f68 a820bc08
    .word  0x08bd30a8                     @ 081c4f6c a830bd08
    .word  0x08be20a8                     @ 081c4f70 a820be08
    .word  0x08bf28a8                     @ 081c4f74 a828bf08
    .word  0x08c020a8                     @ 081c4f78 a820c008
    .word  0x08c120a8                     @ 081c4f7c a820c108
    .word  0x08c220a8                     @ 081c4f80 a820c208
    .byte  0xa8, 0x30, 0xb3, 0x10
    .word  0x08b520a8                     @ 081c4f88 a820b508
    .word  0x08b620a8                     @ 081c4f8c a820b608
    .word  0x08b728a8                     @ 081c4f90 a828b708
    .word  0x08b820a8                     @ 081c4f94 a820b808
    .word  0x08ba30a8                     @ 081c4f98 a830ba08
    .word  0x08b920a8                     @ 081c4f9c a820b908
    .word  0x08bb20a8                     @ 081c4fa0 a820bb08
    .word  0x08bc20a8                     @ 081c4fa4 a820bc08
    .word  0x08bd20a8                     @ 081c4fa8 a820bd08
    .word  0x08be20a8                     @ 081c4fac a820be08
    .word  0x08bf28a8                     @ 081c4fb0 a828bf08
    .word  0x08c020a8                     @ 081c4fb4 a820c008
    .word  0x08c120a8                     @ 081c4fb8 a820c108
    .word  0x08c220a8                     @ 081c4fbc a820c208
    .word  0x08b330a8                     @ 081c4fc0 a830b308
    .word  0x08b820a8                     @ 081c4fc4 a820b808
    .word  0x08b520a8                     @ 081c4fc8 a820b508
    .word  0x08b620a8                     @ 081c4fcc a820b608
    .byte  0xa8, 0x28, 0xb7, 0x09
    .word  0x08b820a8                     @ 081c4fd4 a820b808
    .word  0x08b920a8                     @ 081c4fd8 a820b908
    .word  0x08ba20a8                     @ 081c4fdc a820ba08
    .word  0x08bb20a8                     @ 081c4fe0 a820bb08
    .word  0x08bc20a8                     @ 081c4fe4 a820bc08
    .word  0x08bd30a8                     @ 081c4fe8 a830bd08
    .word  0x08be20a8                     @ 081c4fec a820be08
    .word  0x08bf28a8                     @ 081c4ff0 a828bf08
    .word  0x08c020a8                     @ 081c4ff4 a820c008
    .word  0x08c120a8                     @ 081c4ff8 a820c108
    .word  0x08c220a8                     @ 081c4ffc a820c208
    .byte  0xa8, 0x30, 0xb3, 0x10
    .word  0x08b520a8                     @ 081c5004 a820b508
    .word  0x08b620a8                     @ 081c5008 a820b608
    .word  0x08b728a8                     @ 081c500c a828b708
    .word  0x08b820a8                     @ 081c5010 a820b808
    .word  0x08ba30a8                     @ 081c5014 a830ba08
    .word  0x08b920a8                     @ 081c5018 a820b908
    .word  0x08bb20a8                     @ 081c501c a820bb08
    .word  0x08bc20a8                     @ 081c5020 a820bc08
    .word  0x08bd20a8                     @ 081c5024 a820bd08
    .word  0x08be20a8                     @ 081c5028 a820be08
    .word  0x08bf28a8                     @ 081c502c a828bf08
    .word  0x08c020a8                     @ 081c5030 a820c008
    .word  0x08c120a8                     @ 081c5034 a820c108
    .word  0x08c220a8                     @ 081c5038 a820c208
    .word  0x09b330a8                     @ 081c503c a830b309
    .word  0x08b820a8                     @ 081c5040 a820b808
    .word  0x08b520a8                     @ 081c5044 a820b508
    .word  0x08b620a8                     @ 081c5048 a820b608
    .word  0x08b728a8                     @ 081c504c a828b708
    .word  0x08b820a8                     @ 081c5050 a820b808
    .word  0x08b920a8                     @ 081c5054 a820b908
    .word  0x08ba20a8                     @ 081c5058 a820ba08
    .word  0x08bb20a8                     @ 081c505c a820bb08
    .word  0x08bc20a8                     @ 081c5060 a820bc08
    .word  0x08bd30a8                     @ 081c5064 a830bd08
    .word  0x08be20a8                     @ 081c5068 a820be08
    .word  0x08bf28a8                     @ 081c506c a828bf08
    .word  0x08c020a8                     @ 081c5070 a820c008
    .word  0x08c120a8                     @ 081c5074 a820c108
    .word  0x08c220a8                     @ 081c5078 a820c208
    .byte  0xa8, 0x30, 0xb3, 0x10
    .word  0x08b520a8                     @ 081c5080 a820b508
    .word  0x08b620a8                     @ 081c5084 a820b608
    .word  0x08b728a8                     @ 081c5088 a828b708
    .word  0x08b820a8                     @ 081c508c a820b808
    .word  0x08ba30a8                     @ 081c5090 a830ba08
    .word  0x08b920a8                     @ 081c5094 a820b908
    .word  0x08bb20a8                     @ 081c5098 a820bb08
    .word  0x08bc20a8                     @ 081c509c a820bc08
    .word  0x08bd20a8                     @ 081c50a0 a820bd08
    .word  0x08be20a8                     @ 081c50a4 a820be08
    .byte  0xa8, 0x28, 0xbf, 0x09
    .word  0x08c020a8                     @ 081c50ac a820c008
    .word  0x08c120a8                     @ 081c50b0 a820c108
    .word  0x08c220a8                     @ 081c50b4 a820c208
    .word  0x08b330a8                     @ 081c50b8 a830b308
    .word  0x08b820a8                     @ 081c50bc a820b808
    .word  0x08b520a8                     @ 081c50c0 a820b508
    .word  0x08b620a8                     @ 081c50c4 a820b608
    .word  0x08b728a8                     @ 081c50c8 a828b708
    .word  0x08b820a8                     @ 081c50cc a820b808
    .word  0x08b920a8                     @ 081c50d0 a820b908
    .word  0x08ba20a8                     @ 081c50d4 a820ba08
    .word  0x08bb20a8                     @ 081c50d8 a820bb08
    .word  0x08bc20a8                     @ 081c50dc a820bc08
    .word  0x08bd30a8                     @ 081c50e0 a830bd08
    .word  0x08be20a8                     @ 081c50e4 a820be08
    .word  0x08bf28a8                     @ 081c50e8 a828bf08
    .word  0x08c020a8                     @ 081c50ec a820c008
    .word  0x08c120a8                     @ 081c50f0 a820c108
    .word  0x08c220a8                     @ 081c50f4 a820c208
    .byte  0xa8, 0x30, 0xb3, 0x10
    .word  0x08b520a8                     @ 081c50fc a820b508
    .word  0x08b620a8                     @ 081c5100 a820b608
    .word  0x08b728a8                     @ 081c5104 a828b708
    .word  0x08b820a8                     @ 081c5108 a820b808
    .word  0x08ba30a8                     @ 081c510c a830ba08
    .word  0x08b920a8                     @ 081c5110 a820b908
    .byte  0xa8, 0x20, 0xbb, 0x09
    .word  0x08bc20a8                     @ 081c5118 a820bc08
    .word  0x08bd20a8                     @ 081c511c a820bd08
    .word  0x08be20a8                     @ 081c5120 a820be08
    .word  0x08bf28a8                     @ 081c5124 a828bf08
    .word  0x08c020a8                     @ 081c5128 a820c008
    .word  0x08c120a8                     @ 081c512c a820c108
    .word  0x08c220a8                     @ 081c5130 a820c208
    .word  0x08b330a8                     @ 081c5134 a830b308
    .word  0x08b820a8                     @ 081c5138 a820b808
    .word  0x08b520a8                     @ 081c513c a820b508
    .word  0x08b620a8                     @ 081c5140 a820b608
    .word  0x08b728a8                     @ 081c5144 a828b708
    .word  0x08b820a8                     @ 081c5148 a820b808
    .word  0x08b920a8                     @ 081c514c a820b908
    .word  0x08ba20a8                     @ 081c5150 a820ba08
    .word  0x08bb20a8                     @ 081c5154 a820bb08
    .word  0x08bc20a8                     @ 081c5158 a820bc08
    .word  0x08bd30a8                     @ 081c515c a830bd08
    .word  0x08be20a8                     @ 081c5160 a820be08
    .word  0x08bf28a8                     @ 081c5164 a828bf08
    .word  0x08c020a8                     @ 081c5168 a820c008
    .word  0x08c120a8                     @ 081c516c a820c108
    .word  0x08c220a8                     @ 081c5170 a820c208
    .byte  0xa8, 0x30, 0xb3, 0x10, 0xa8, 0x20, 0xb5, 0x08, 0xa8, 0x20, 0xb6, 0x08, 0xa8, 0x28, 0xb7, 0x09
    .word  0x08b820a8                     @ 081c5184 a820b808
    .word  0x08ba30a8                     @ 081c5188 a830ba08
    .word  0x08b920a8                     @ 081c518c a820b908
    .word  0x08bb20a8                     @ 081c5190 a820bb08
    .word  0x08bc20a8                     @ 081c5194 a820bc08
    .word  0x08bd20a8                     @ 081c5198 a820bd08
    .word  0x08be20a8                     @ 081c519c a820be08
    .word  0x08bf28a8                     @ 081c51a0 a828bf08
    .word  0x08c020a8                     @ 081c51a4 a820c008
    .word  0x08c120a8                     @ 081c51a8 a820c108
    .word  0x08c220a8                     @ 081c51ac a820c208
    .word  0x08b330a8                     @ 081c51b0 a830b308
    .word  0x08b820a8                     @ 081c51b4 a820b808
    .word  0x08b520a8                     @ 081c51b8 a820b508
    .word  0x08b620a8                     @ 081c51bc a820b608
    .word  0x08b728a8                     @ 081c51c0 a828b708
    .word  0x08b820a8                     @ 081c51c4 a820b808
    .word  0x08b920a8                     @ 081c51c8 a820b908
    .word  0x08ba20a8                     @ 081c51cc a820ba08
    .word  0x08bb20a8                     @ 081c51d0 a820bb08
    .word  0x08bc20a8                     @ 081c51d4 a820bc08
    .word  0x08bd30a8                     @ 081c51d8 a830bd08
    .word  0x08be20a8                     @ 081c51dc a820be08
    .word  0x08bf28a8                     @ 081c51e0 a828bf08
    .word  0x08c020a8                     @ 081c51e4 a820c008
    .word  0x08c120a8                     @ 081c51e8 a820c108
    .word  0x08c220a8                     @ 081c51ec a820c208
    .byte  0xa8, 0x30, 0xb3, 0x11
    .word  0x08b520a8                     @ 081c51f4 a820b508
    .word  0x08b620a8                     @ 081c51f8 a820b608
    .word  0x08b728a8                     @ 081c51fc a828b708
    .word  0x08b820a8                     @ 081c5200 a820b808
    .word  0x08ba30a8                     @ 081c5204 a830ba08
    .word  0x08b920a8                     @ 081c5208 a820b908
    .word  0x08bb20a8                     @ 081c520c a820bb08
    .word  0x08bc20a8                     @ 081c5210 a820bc08
    .word  0x08bd20a8                     @ 081c5214 a820bd08
    .word  0x08be20a8                     @ 081c5218 a820be08
    .word  0x08bf28a8                     @ 081c521c a828bf08
    .word  0x08c020a8                     @ 081c5220 a820c008
    .word  0x08c120a8                     @ 081c5224 a820c108
    .word  0x08c220a8                     @ 081c5228 a820c208
    .word  0x08b330a8                     @ 081c522c a830b308
    .word  0x08b820a8                     @ 081c5230 a820b808
    .word  0x08b520a8                     @ 081c5234 a820b508
    .word  0x08b620a8                     @ 081c5238 a820b608
    .word  0x08b728a8                     @ 081c523c a828b708
    .word  0x08b820a8                     @ 081c5240 a820b808
    .word  0x08b920a8                     @ 081c5244 a820b908
    .word  0x08ba20a8                     @ 081c5248 a820ba08
    .word  0x08bb20a8                     @ 081c524c a820bb08
    .word  0x08bc20a8                     @ 081c5250 a820bc08
    .word  0x08bd30a8                     @ 081c5254 a830bd08
    .word  0x08be20a8                     @ 081c5258 a820be08
    ROM_INCBIN 0x1c525c, 0x9dcc
    .word  0x09a91ca8                     @ 081cf028 a81ca909
    .word  0x09b00fa8                     @ 081cf02c a80fb009
    .word  0x09a91ca8                     @ 081cf030 a81ca909
    .word  0x09b11ca8                     @ 081cf034 a81cb109
    .word  0x09a31ca8                     @ 081cf038 a81ca309
    .word  0x09a41ca8                     @ 081cf03c a81ca409
    .word  0x09a51ca8                     @ 081cf040 a81ca509
    .word  0x09a61ca8                     @ 081cf044 a81ca609
    .word  0x09a71ca8                     @ 081cf048 a81ca709
    .word  0x09a81ca8                     @ 081cf04c a81ca809
    .word  0x09a91ca8                     @ 081cf050 a81ca909
    .word  0x09aa1ca8                     @ 081cf054 a81caa09
    .word  0x09ab1ca8                     @ 081cf058 a81cab09
    .word  0x09ac1ca8                     @ 081cf05c a81cac09
    .word  0x09ad1ca8                     @ 081cf060 a81cad09
    .word  0x09ae1ca8                     @ 081cf064 a81cae09
    .word  0x09af11a8                     @ 081cf068 a811af09
    .word  0x09b00fa8                     @ 081cf06c a80fb009
    .word  0x09b11ca8                     @ 081cf070 a81cb109
    .word  0x09b21ca8                     @ 081cf074 a81cb209
    .word  0x09a31ca8                     @ 081cf078 a81ca309
    .word  0x09a51ca8                     @ 081cf07c a81ca509
    .word  0x09a61ca8                     @ 081cf080 a81ca609
    .word  0x09a51ca8                     @ 081cf084 a81ca509
    .word  0x09a71ca8                     @ 081cf088 a81ca709
    .word  0x09a81ca8                     @ 081cf08c a81ca809
    .word  0x09a91ca8                     @ 081cf090 a81ca909
    .word  0x09a41ca8                     @ 081cf094 a81ca409
    .word  0x09ab1ca8                     @ 081cf098 a81cab09
    ROM_INCBIN 0x1cf09c, 0x244
    .word  0x0901b11c                     @ 081cf2e0 1cb10109
    .word  0x09a91ca8                     @ 081cf2e4 a81ca909
    .word  0x09ab1ca8                     @ 081cf2e8 a81cab09
    .word  0x09ac1ca8                     @ 081cf2ec a81cac09
    .word  0x09ad1ca8                     @ 081cf2f0 a81cad09
    .word  0x09ae1ca8                     @ 081cf2f4 a81cae09
    .word  0x09b11ca8                     @ 081cf2f8 a81cb109
    .word  0x09b00fa8                     @ 081cf2fc a80fb009
    .word  0x09a31ca8                     @ 081cf300 a81ca309
    .word  0x09a91ca8                     @ 081cf304 a81ca909
    .word  0x09a31ca8                     @ 081cf308 a81ca309
    .word  0x09a41ca8                     @ 081cf30c a81ca409
    .word  0x09a91ca8                     @ 081cf310 a81ca909
    .word  0x09a71ca8                     @ 081cf314 a81ca709
    ROM_INCBIN 0x1cf318, 0x2c
    .word  0x09a31ca8                     @ 081cf344 a81ca309
    .word  0x09a41ca8                     @ 081cf348 a81ca409
    .word  0x09a51ca8                     @ 081cf34c a81ca509
    .word  0x09a61ca8                     @ 081cf350 a81ca609
    .word  0x09a71ca8                     @ 081cf354 a81ca709
    .word  0x09a81ca8                     @ 081cf358 a81ca809
    .word  0x09a91ca8                     @ 081cf35c a81ca909
    .word  0x09aa1ca8                     @ 081cf360 a81caa09
    .word  0x09ab1ca8                     @ 081cf364 a81cab09
    .word  0x09ac1ca8                     @ 081cf368 a81cac09
    .word  0x09ad1ca8                     @ 081cf36c a81cad09
    .word  0x09ae1ca8                     @ 081cf370 a81cae09
    .word  0x09af11a8                     @ 081cf374 a811af09
    .word  0x09b00fa8                     @ 081cf378 a80fb009
    .word  0x09b11ca8                     @ 081cf37c a81cb109
    .word  0x09b21ca8                     @ 081cf380 a81cb209
    .word  0x09a31ca8                     @ 081cf384 a81ca309
    .word  0x09a41ca8                     @ 081cf388 a81ca409
    .word  0x09a51ca8                     @ 081cf38c a81ca509
    .word  0x09a61ca8                     @ 081cf390 a81ca609
    .word  0x09a71ca8                     @ 081cf394 a81ca709
    .word  0x09a81ca8                     @ 081cf398 a81ca809
    .word  0x09a91ca8                     @ 081cf39c a81ca909
    .word  0x09aa1ca8                     @ 081cf3a0 a81caa09
    .word  0x09ab1ca8                     @ 081cf3a4 a81cab09
    ROM_INCBIN 0x1cf3a8, 0x38
    .word  0x0901b11c                     @ 081cf3e0 1cb10109
    .word  0x09aa1ca8                     @ 081cf3e4 a81caa09
    .word  0x09ab1ca8                     @ 081cf3e8 a81cab09
    .word  0x09ac1ca8                     @ 081cf3ec a81cac09
    .word  0x09ad1ca8                     @ 081cf3f0 a81cad09
    .word  0x09ae1ca8                     @ 081cf3f4 a81cae09
    .word  0x09af11a8                     @ 081cf3f8 a811af09
    .word  0x09b00fa8                     @ 081cf3fc a80fb009
    .word  0x09b21ca8                     @ 081cf400 a81cb209
    .word  0x09b21ca8                     @ 081cf404 a81cb209
    .word  0x09a31ca8                     @ 081cf408 a81ca309
    .word  0x09a41ca8                     @ 081cf40c a81ca409
    .word  0x09a51ca8                     @ 081cf410 a81ca509
    .word  0x09a61ca8                     @ 081cf414 a81ca609
    .word  0x09a71ca8                     @ 081cf418 a81ca709
    .word  0x09a81ca8                     @ 081cf41c a81ca809
    .word  0x09a91ca8                     @ 081cf420 a81ca909
    .word  0x09aa1ca8                     @ 081cf424 a81caa09
    ROM_INCBIN 0x1cf428, 0xbc
    .word  0x0901b11c                     @ 081cf4e4 1cb10109
    .word  0x09aa1ca8                     @ 081cf4e8 a81caa09
    .word  0x09ab1ca8                     @ 081cf4ec a81cab09
    .word  0x09ac1ca8                     @ 081cf4f0 a81cac09
    .word  0x09ad1ca8                     @ 081cf4f4 a81cad09
    .word  0x09ae1ca8                     @ 081cf4f8 a81cae09
    .word  0x09af11a8                     @ 081cf4fc a811af09
    .word  0x09b00fa8                     @ 081cf500 a80fb009
    .word  0x09b21ca8                     @ 081cf504 a81cb209
    .word  0x09b21ca8                     @ 081cf508 a81cb209
    .word  0x09a31ca8                     @ 081cf50c a81ca309
    .word  0x09a41ca8                     @ 081cf510 a81ca409
    .word  0x09a51ca8                     @ 081cf514 a81ca509
    .word  0x09a61ca8                     @ 081cf518 a81ca609
    .word  0x09a71ca8                     @ 081cf51c a81ca709
    .word  0x09a81ca8                     @ 081cf520 a81ca809
    .word  0x09a91ca8                     @ 081cf524 a81ca909
    .word  0x09ad1ca8                     @ 081cf528 a81cad09
    .word  0x09ab1ca8                     @ 081cf52c a81cab09
    .word  0x09ad1ca8                     @ 081cf530 a81cad09
    .word  0x09ac1ca8                     @ 081cf534 a81cac09
    .word  0x09ae1ca8                     @ 081cf538 a81cae09
    .word  0x09af11a8                     @ 081cf53c a811af09
    .word  0x09a91ca8                     @ 081cf540 a81ca909
    ROM_INCBIN 0x1cf544, 0x114
    .word  0x09a31ca8                     @ 081cf658 a81ca309
    .word  0x09a41ca8                     @ 081cf65c a81ca409
    .word  0x09a51ca8                     @ 081cf660 a81ca509
    .word  0x09a61ca8                     @ 081cf664 a81ca609
    .word  0x09a91ca8                     @ 081cf668 a81ca909
    .word  0x09a81ca8                     @ 081cf66c a81ca809
    .word  0x09a91ca8                     @ 081cf670 a81ca909
    .word  0x09aa1ca8                     @ 081cf674 a81caa09
    ROM_INCBIN 0x1cf678, 0x60
    .word  0x0901aa1c                     @ 081cf6d8 1caa0109
    .word  0x09b11ca8                     @ 081cf6dc a81cb109
    .word  0x09a31ca8                     @ 081cf6e0 a81ca309
    .word  0x09a41ca8                     @ 081cf6e4 a81ca409
    .word  0x09a51ca8                     @ 081cf6e8 a81ca509
    .word  0x09a61ca8                     @ 081cf6ec a81ca609
    .word  0x09aa1ca8                     @ 081cf6f0 a81caa09
    .word  0x09a81ca8                     @ 081cf6f4 a81ca809
    .word  0x09a91ca8                     @ 081cf6f8 a81ca909
    .word  0x09aa1ca8                     @ 081cf6fc a81caa09
    ROM_INCBIN 0x1cf700, 0x87a0
PTR_DAT_081d7ea0:
    .word  0x081d8244                     @ 081d7ea0 44821d08
    .word  0x081d8350                     @ 081d7ea4 50831d08
    .word  0x081d93d0                     @ 081d7ea8 d0931d08
    .word  0x081d9f80                     @ 081d7eac 809f1d08
    .word  0x081dacd4                     @ 081d7eb0 d4ac1d08
    .word  0x081dbb20                     @ 081d7eb4 20bb1d08
    .word  0x081dcb9c                     @ 081d7eb8 9ccb1d08
    .word  0x081dd844                     @ 081d7ebc 44d81d08
    .word  0x081de5cc                     @ 081d7ec0 cce51d08
    .word  0x081df238                     @ 081d7ec4 38f21d08
    .word  0x081e02b4                     @ 081d7ec8 b4021e08
    .word  0x081e0f84                     @ 081d7ecc 840f1e08
    .word  0x081e1cdc                     @ 081d7ed0 dc1c1e08
    .word  0x081e2b28                     @ 081d7ed4 282b1e08
    .word  0x081e3ba4                     @ 081d7ed8 a43b1e08
    .word  0x081e484c                     @ 081d7edc 4c481e08
    .word  0x081e55d8                     @ 081d7ee0 d8551e08
    .word  0x081e6424                     @ 081d7ee4 24641e08
    .word  0x081e8754                     @ 081d7ee8 54871e08
    .word  0x081e8c9c                     @ 081d7eec 9c8c1e08
    .word  0x081ea604                     @ 081d7ef0 04a61e08
    .word  0x081eb4b0                     @ 081d7ef4 b0b41e08
    .word  0x081ef38c                     @ 081d7ef8 8cf31e08
    .word  0x081f0560                     @ 081d7efc 60051f08
    .word  0x081f17ac                     @ 081d7f00 ac171f08
    .word  0x081f1e28                     @ 081d7f04 281e1f08
    .word  0x081f3138                     @ 081d7f08 38311f08
    .word  0x081f3e78                     @ 081d7f0c 783e1f08
    .word  0x081f648c                     @ 081d7f10 8c641f08
    .word  0x081f66c8                     @ 081d7f14 c8661f08
    .word  0x081f8664                     @ 081d7f18 64861f08
    .word  0x081f96b4                     @ 081d7f1c b4961f08
    .word  0x081f9c58                     @ 081d7f20 589c1f08
    .word  0x081faf8c                     @ 081d7f24 8caf1f08
    .word  0x081fb4f8                     @ 081d7f28 f8b41f08
    .word  0x081fb730                     @ 081d7f2c 30b71f08
    .word  0x081fb7d8                     @ 081d7f30 d8b71f08
    .word  0x081fb9d0                     @ 081d7f34 d0b91f08
    .word  0x081ff400                     @ 081d7f38 00f41f08
    .word  0x082022fc                     @ 081d7f3c fc222008
    .word  0x08203f20                     @ 081d7f40 203f2008
    .word  0x08205a8c                     @ 081d7f44 8c5a2008
    .word  0x08206e14                     @ 081d7f48 146e2008
    .word  0x08207760                     @ 081d7f4c 60772008
    .word  0x082084d4                     @ 081d7f50 d4842008
    .word  0x0820dd4c                     @ 081d7f54 4cdd2008
    .word  0x082131a4                     @ 081d7f58 a4312108
    .word  0x08215f0c                     @ 081d7f5c 0c5f2108
    .word  0x08218cac                     @ 081d7f60 ac8c2108
    .word  0x0821afe8                     @ 081d7f64 e8af2108
    .word  0x0821f52c                     @ 081d7f68 2cf52108
    .word  0x08220e6c                     @ 081d7f6c 6c0e2208
    .word  0x082230f0                     @ 081d7f70 f0302208
    .word  0x08223ad8                     @ 081d7f74 d83a2208
    .word  0x08224bf0                     @ 081d7f78 f04b2208
    .word  0x08227dc8                     @ 081d7f7c c87d2208
    .word  0x0822b57c                     @ 081d7f80 7cb52208
    .word  0x0822e464                     @ 081d7f84 64e42208
    .word  0x0823135c                     @ 081d7f88 5c132308
    .word  0x08234210                     @ 081d7f8c 10422308
    .word  0x08237210                     @ 081d7f90 10722308
    .word  0x082391e0                     @ 081d7f94 e0912308
    .word  0x0823ade8                     @ 081d7f98 e8ad2308
    .word  0x08241858                     @ 081d7f9c 58182408
    .word  0x08248b44                     @ 081d7fa0 448b2408
    .word  0x0824b52c                     @ 081d7fa4 2cb52408
    .word  0x0824d1e4                     @ 081d7fa8 e4d12408
    .word  0x0824ef38                     @ 081d7fac 38ef2408
    .word  0x08251e18                     @ 081d7fb0 181e2508
    .word  0x08253de0                     @ 081d7fb4 e03d2508
    .word  0x08254364                     @ 081d7fb8 64432508
    .word  0x082560e8                     @ 081d7fbc e8602508
    .word  0x08256f74                     @ 081d7fc0 746f2508
    .word  0x0825822c                     @ 081d7fc4 2c822508
    .word  0x08259cec                     @ 081d7fc8 ec9c2508
    .word  0x0825a9bc                     @ 081d7fcc bca92508
    .word  0x0825c46c                     @ 081d7fd0 6cc42508
    .word  0x0825ccb4                     @ 081d7fd4 b4cc2508
    .word  0x0825d7fc                     @ 081d7fd8 fcd72508
    .word  0x0825ebe0                     @ 081d7fdc e0eb2508
    .word  0x0825f468                     @ 081d7fe0 68f42508
    .word  0x0825fed0                     @ 081d7fe4 d0fe2508
    .word  0x082605ec                     @ 081d7fe8 ec052608
    .word  0x08260ce8                     @ 081d7fec e80c2608
    .word  0x08262938                     @ 081d7ff0 38292608
    .word  0x08264adc                     @ 081d7ff4 dc4a2608
    .word  0x082678d4                     @ 081d7ff8 d4782608
    .word  0x08269548                     @ 081d7ffc 48952608
    .word  0x0826f334                     @ 081d8000 34f32608
    .word  0x08274d24                     @ 081d8004 244d2708
    .word  0x0827a954                     @ 081d8008 54a92708
    .word  0x08280890                     @ 081d800c 90082808
    .word  0x082865e8                     @ 081d8010 e8652808
    .word  0x0828c544                     @ 081d8014 44c52808
    .word  0x082922d8                     @ 081d8018 d8222908
    .word  0x08297e34                     @ 081d801c 347e2908
    .word  0x0829dd6c                     @ 081d8020 6cdd2908
    .word  0x082a0870                     @ 081d8024 70082a08
    .word  0x082a3460                     @ 081d8028 60342a08
    .word  0x082a61a4                     @ 081d802c a4612a08
    .word  0x082a8b78                     @ 081d8030 788b2a08
    .word  0x082ab638                     @ 081d8034 38b62a08
    .word  0x082ae258                     @ 081d8038 58e22a08
    .word  0x082b0980                     @ 081d803c 80092b08
    .word  0x082b31c8                     @ 081d8040 c8312b08
    .word  0x082b55f8                     @ 081d8044 f8552b08
    .word  0x082b8094                     @ 081d8048 94802b08
    .word  0x082ba90c                     @ 081d804c 0ca92b08
    .word  0x082bcdf0                     @ 081d8050 f0cd2b08
    .word  0x082bf098                     @ 081d8054 98f02b08
    .word  0x082c1898                     @ 081d8058 98182c08
    .word  0x082c39b8                     @ 081d805c b8392c08
    .word  0x082c5a6c                     @ 081d8060 6c5a2c08
    .word  0x082c6424                     @ 081d8064 24642c08
    .word  0x082c6bf4                     @ 081d8068 f46b2c08
    .word  0x082c7f98                     @ 081d806c 987f2c08
    .word  0x082c8350                     @ 081d8070 50832c08
    .word  0x082c9c44                     @ 081d8074 449c2c08
    .word  0x082cc26c                     @ 081d8078 6cc22c08
    .word  0x082cd2f4                     @ 081d807c f4d22c08
    .word  0x082cd9f8                     @ 081d8080 f8d92c08
    .word  0x082cf4c8                     @ 081d8084 c8f42c08
    .word  0x082cf95c                     @ 081d8088 5cf92c08
    .word  0x082cffb0                     @ 081d808c b0ff2c08
    .word  0x082d1004                     @ 081d8090 04102d08
    .word  0x082d1214                     @ 081d8094 14122d08
    .word  0x082d1ba0                     @ 081d8098 a01b2d08
    .word  0x082d2bd8                     @ 081d809c d82b2d08
    .word  0x082d311c                     @ 081d80a0 1c312d08
    .word  0x082d3b30                     @ 081d80a4 303b2d08
    .word  0x082d4ef8                     @ 081d80a8 f84e2d08
    .word  0x082d55e8                     @ 081d80ac e8552d08
    .word  0x082d6cac                     @ 081d80b0 ac6c2d08
    .word  0x082d8c5c                     @ 081d80b4 5c8c2d08
    .word  0x082da4a4                     @ 081d80b8 a4a42d08
    .word  0x082dc48c                     @ 081d80bc 8cc42d08
    .word  0x082df98c                     @ 081d80c0 8cf92d08
    .word  0x082e3b8c                     @ 081d80c4 8c3b2e08
    .word  0x082e5ed8                     @ 081d80c8 d85e2e08
    .word  0x082e84a4                     @ 081d80cc a4842e08
    .word  0x082eaa34                     @ 081d80d0 34aa2e08
    .word  0x082edd30                     @ 081d80d4 30dd2e08
    .word  0x082f345c                     @ 081d80d8 5c342f08
    .word  0x082fbb94                     @ 081d80dc 94bb2f08
    .word  0x082fdec4                     @ 081d80e0 c4de2f08
    .word  0x08301cb4                     @ 081d80e4 b41c3008
    .word  0x08305ae8                     @ 081d80e8 e85a3008
    .word  0x0830990c                     @ 081d80ec 0c993008
    .word  0x0830d6d0                     @ 081d80f0 d0d63008
    .word  0x0830f19c                     @ 081d80f4 9cf13008
    .word  0x08310408                     @ 081d80f8 08043108
    .word  0x083107c0                     @ 081d80fc c0073108
    .word  0x08311c04                     @ 081d8100 041c3108
    .word  0x083125a0                     @ 081d8104 a0253108
    .word  0x08313a34                     @ 081d8108 343a3108
    .word  0x08313f28                     @ 081d810c 283f3108
    .word  0x083150f8                     @ 081d8110 f8503108
    .word  0x08315574                     @ 081d8114 74553108
    .word  0x08316db4                     @ 081d8118 b46d3108
    .word  0x08317cbc                     @ 081d811c bc7c3108
    .word  0x0831916c                     @ 081d8120 6c913108
    .word  0x08319f78                     @ 081d8124 789f3108
    .word  0x0831af50                     @ 081d8128 50af3108
    .word  0x0831be54                     @ 081d812c 54be3108
    .word  0x0831cdec                     @ 081d8130 eccd3108
    .word  0x0831d934                     @ 081d8134 34d93108
    .word  0x0831eaf4                     @ 081d8138 f4ea3108
    .word  0x0831f6e8                     @ 081d813c e8f63108
    .word  0x083205a0                     @ 081d8140 a0053208
    .word  0x0832165c                     @ 081d8144 5c163208
    .word  0x08322660                     @ 081d8148 60263208
    .word  0x0832351c                     @ 081d814c 1c353208
    .word  0x08324574                     @ 081d8150 74453208
    .word  0x083253c0                     @ 081d8154 c0533208
    .word  0x08326190                     @ 081d8158 90613208
    .word  0x08327020                     @ 081d815c 20703208
    .word  0x08328148                     @ 081d8160 48813208
    .word  0x08328e00                     @ 081d8164 008e3208
    .word  0x0832a0b0                     @ 081d8168 b0a03208
    .word  0x0832b090                     @ 081d816c 90b03208
    .word  0x0832df70                     @ 081d8170 70df3208
    .word  0x0832e208                     @ 081d8174 08e23208
    .word  0x0832e63c                     @ 081d8178 3ce63208
    .word  0x0832e974                     @ 081d817c 74e93208
    .word  0x0832f828                     @ 081d8180 28f83208
    .word  0x083302a8                     @ 081d8184 a8023308
    .word  0x083306d8                     @ 081d8188 d8063308
    .word  0x08333328                     @ 081d818c 28333308
    .word  0x083335b8                     @ 081d8190 b8353308
    .word  0x08334350                     @ 081d8194 50433308
    .word  0x08336f98                     @ 081d8198 986f3308
    .word  0x08337d58                     @ 081d819c 587d3308
    .word  0x08338c00                     @ 081d81a0 008c3308
    .word  0x0833b838                     @ 081d81a4 38b83308
    .word  0x0833c648                     @ 081d81a8 48c63308
    .word  0x0833ca18                     @ 081d81ac 18ca3308
    .word  0x0833df48                     @ 081d81b0 48df3308
    .word  0x0833e924                     @ 081d81b4 24e93308
    .word  0x0833f2a4                     @ 081d81b8 a4f23308
    .word  0x0833fd14                     @ 081d81bc 14fd3308
    .word  0x08341240                     @ 081d81c0 40123408
    .word  0x083419dc                     @ 081d81c4 dc193408
    .word  0x08342474                     @ 081d81c8 74243408
    .word  0x08342f80                     @ 081d81cc 802f3408
    .word  0x083444b0                     @ 081d81d0 b0443408
    .word  0x08344f1c                     @ 081d81d4 1c4f3408
    .word  0x08345998                     @ 081d81d8 98593408
    .word  0x08346180                     @ 081d81dc 80613408
    .word  0x083476ac                     @ 081d81e0 ac763408
    .word  0x08347fc0                     @ 081d81e4 c07f3408
    .word  0x08348684                     @ 081d81e8 84863408
    .word  0x08348e6c                     @ 081d81ec 6c8e3408
    .word  0x0834b0ac                     @ 081d81f0 acb03408
    .word  0x0834b480                     @ 081d81f4 80b43408
    .word  0x08351704                     @ 081d81f8 04173508
    .word  0x0835800c                     @ 081d81fc 0c803508
    .word  0x0835fed8                     @ 081d8200 d8fe3508
    .word  0x08365cbc                     @ 081d8204 bc5c3608
    .word  0x0836bb40                     @ 081d8208 40bb3608
    .word  0x08370b44                     @ 081d820c 440b3708
    .word  0x08375c48                     @ 081d8210 485c3708
    .word  0x0837a2cc                     @ 081d8214 cca23708
    .word  0x0837c1e0                     @ 081d8218 e0c13708
    .word  0x0837e9c4                     @ 081d821c c4e93708
    .word  0x08381b98                     @ 081d8220 981b3808
    .word  0x08387758                     @ 081d8224 58773808
    .word  0x0838b658                     @ 081d8228 58b63808
    .word  0x0838e4b8                     @ 081d822c b8e43808
    .word  0x083c5180                     @ 081d8230 80513c08
    .word  0x083fc334                     @ 081d8234 34c33f08
    .word  0x0842fb54                     @ 081d8238 54fb4208
    .word  0x08462c20                     @ 081d823c 202c4608
    .word  0x08490a10                     @ 081d8240 100a4908
DAT_081d8244:
    ROM_INCBIN 0x1d8244, 0x1b0c
    .word  0x02010102                     @ 081d9d50 02010102
    .word  0x02020202                     @ 081d9d54 02020202
    .word  0x02020202                     @ 081d9d58 02020202
    .word  0x02020202                     @ 081d9d5c 02020202
    .word  0x02020202                     @ 081d9d60 02020202
    .word  0x02020202                     @ 081d9d64 02020202
    .word  0x02020202                     @ 081d9d68 02020202
    .word  0x02020202                     @ 081d9d6c 02020202
    .word  0x02020202                     @ 081d9d70 02020202
    .word  0x02020202                     @ 081d9d74 02020202
    .word  0x02020202                     @ 081d9d78 02020202
    .word  0x02020202                     @ 081d9d7c 02020202
    .word  0x02020202                     @ 081d9d80 02020202
    ROM_INCBIN 0x1d9d84, 0x1d6c
    .word  0x02020201                     @ 081dbaf0 01020202
    .word  0x02020202                     @ 081dbaf4 02020202
    .word  0x02020202                     @ 081dbaf8 02020202
    .word  0x02020202                     @ 081dbafc 02020202
    .word  0x02020202                     @ 081dbb00 02020202
    .word  0x02020202                     @ 081dbb04 02020202
    .word  0x02020202                     @ 081dbb08 02020202
    .word  0x02020202                     @ 081dbb0c 02020202
    .word  0x02020202                     @ 081dbb10 02020202
    .word  0x02020202                     @ 081dbb14 02020202
    ROM_INCBIN 0x1dbb18, 0x4ae8
DWORD_081e0600:
    .word  0xfef9f6f4                     @ 081e0600 f4f6f9fe
    ROM_INCBIN 0x1e0604, 0x24f4
    .word  0x02020201                     @ 081e2af8 01020202
    .word  0x02020202                     @ 081e2afc 02020202
    .word  0x02020202                     @ 081e2b00 02020202
    .word  0x02020202                     @ 081e2b04 02020202
    .word  0x02020202                     @ 081e2b08 02020202
    .word  0x02020202                     @ 081e2b0c 02020202
    .word  0x02020202                     @ 081e2b10 02020202
    .word  0x02020202                     @ 081e2b14 02020202
    .word  0x02020202                     @ 081e2b18 02020202
    .word  0x02020202                     @ 081e2b1c 02020202
    ROM_INCBIN 0x1e2b20, 0x38d4
    .word  0x02020201                     @ 081e63f4 01020202
    .word  0x02020202                     @ 081e63f8 02020202
    .word  0x02020202                     @ 081e63fc 02020202
    .word  0x02020202                     @ 081e6400 02020202
    .word  0x02020202                     @ 081e6404 02020202
    .word  0x02020202                     @ 081e6408 02020202
    .word  0x02020202                     @ 081e640c 02020202
    .word  0x02020202                     @ 081e6410 02020202
    .word  0x02020202                     @ 081e6414 02020202
    .word  0x02020202                     @ 081e6418 02020202
    ROM_INCBIN 0x1e641c, 0x3060
    .word  0x09090909                     @ 081e947c 09090909
    .word  0x09090909                     @ 081e9480 09090909
    .word  0x09090909                     @ 081e9484 09090909
    .word  0x09090909                     @ 081e9488 09090909
    .word  0x090a0a09                     @ 081e948c 090a0a09
    .word  0x09090909                     @ 081e9490 09090909
    ROM_INCBIN 0x1e9494, 0xd0
    .word  0x09090808                     @ 081e9564 08080909
    .word  0x09090909                     @ 081e9568 09090909
    .word  0x09090909                     @ 081e956c 09090909
    .word  0x09090909                     @ 081e9570 09090909
    .word  0x09080809                     @ 081e9574 09080809
    .word  0x09090909                     @ 081e9578 09090909
    ROM_INCBIN 0x1e957c, 0xc2c
    .word  0x02020201                     @ 081ea1a8 01020202
    .word  0x02020202                     @ 081ea1ac 02020202
    .word  0x02020202                     @ 081ea1b0 02020202
    .word  0x02020202                     @ 081ea1b4 02020202
    .word  0x02020202                     @ 081ea1b8 02020202
    .word  0x02020202                     @ 081ea1bc 02020202
    ROM_INCBIN 0x1ea1c0, 0x14
    .word  0x02020203                     @ 081ea1d4 03020202
    .word  0x02020202                     @ 081ea1d8 02020202
    .word  0x02020202                     @ 081ea1dc 02020202
    .word  0x02020202                     @ 081ea1e0 02020202
    .word  0x02020202                     @ 081ea1e4 02020202
    .word  0x02020202                     @ 081ea1e8 02020202
    ROM_INCBIN 0x1ea1ec, 0xcc
    .word  0x02020201                     @ 081ea2b8 01020202
    .word  0x02020202                     @ 081ea2bc 02020202
    .word  0x02020202                     @ 081ea2c0 02020202
    .word  0x02020202                     @ 081ea2c4 02020202
    .word  0x02020202                     @ 081ea2c8 02020202
    .word  0x02020202                     @ 081ea2cc 02020202
    .word  0x02020202                     @ 081ea2d0 02020202
    .word  0x02020202                     @ 081ea2d4 02020202
    .word  0x02020202                     @ 081ea2d8 02020202
    .word  0x02020202                     @ 081ea2dc 02020202
    .word  0x02020202                     @ 081ea2e0 02020202
    .word  0x02020202                     @ 081ea2e4 02020202
    .word  0x02020202                     @ 081ea2e8 02020202
    .word  0x02020202                     @ 081ea2ec 02020202
    .word  0x02020202                     @ 081ea2f0 02020202
    ROM_INCBIN 0x1ea2f4, 0xd4
    .word  0x02020101                     @ 081ea3c8 01010202
    .word  0x02020202                     @ 081ea3cc 02020202
    .word  0x02020202                     @ 081ea3d0 02020202
    .word  0x02020202                     @ 081ea3d4 02020202
    .word  0x02020202                     @ 081ea3d8 02020202
    .word  0x02020202                     @ 081ea3dc 02020202
    .word  0x02020202                     @ 081ea3e0 02020202
    .word  0x02020202                     @ 081ea3e4 02020202
    .word  0x02020202                     @ 081ea3e8 02020202
    .word  0x02020202                     @ 081ea3ec 02020202
    .word  0x02020202                     @ 081ea3f0 02020202
    .word  0x02020202                     @ 081ea3f4 02020202
    .word  0x02020202                     @ 081ea3f8 02020202
    ROM_INCBIN 0x1ea3fc, 0xe0
    .word  0x02020201                     @ 081ea4dc 01020202
    .word  0x02020202                     @ 081ea4e0 02020202
    .word  0x02020202                     @ 081ea4e4 02020202
    .word  0x02020202                     @ 081ea4e8 02020202
    .word  0x02020202                     @ 081ea4ec 02020202
    .word  0x02020202                     @ 081ea4f0 02020202
    .word  0x02020202                     @ 081ea4f4 02020202
    .word  0x02020202                     @ 081ea4f8 02020202
    .word  0x02020202                     @ 081ea4fc 02020202
    ROM_INCBIN 0x1ea500, 0x3a64
    .word  0x08070707                     @ 081edf64 07070708
    .word  0x080a0908                     @ 081edf68 08090a08
    .word  0x080a090a                     @ 081edf6c 0a090a08
    .word  0x080a090a                     @ 081edf70 0a090a08
    .word  0x0807090a                     @ 081edf74 0a090708
    .word  0x08060809                     @ 081edf78 09080608
    ROM_INCBIN 0x1edf7c, 0xb44
    .word  0x02020203                     @ 081eeac0 03020202
    .word  0x02020203                     @ 081eeac4 03020202
    .word  0x02020302                     @ 081eeac8 02030202
    .word  0x02020202                     @ 081eeacc 02020202
    .word  0x02030304                     @ 081eead0 04030302
    ROM_INCBIN 0x1eead4, 0x2c4
    .word  0x02000201                     @ 081eed98 01020002
    .word  0x02000101                     @ 081eed9c 01010002
    .word  0x02010101                     @ 081eeda0 01010102
    .word  0x02010101                     @ 081eeda4 01010102
    .word  0x02010101                     @ 081eeda8 01010102
    .word  0x02020201                     @ 081eedac 01020202
    .word  0x02010301                     @ 081eedb0 01030102
    ROM_INCBIN 0x1eedb4, 0x18a0
    .byte  0x2a, 0x4a, 0x5b, 0x62, 0x64, 0x62, 0x5f, 0x5d, 0x5b, 0x5a, 0x5a, 0x5a, 0x5a, 0x5a, 0x5a, 0x5a @ 081f0654 2a4a5b6264625f5d5b5a5a5a5a5a5a5a
    .byte  0x5a, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x56, 0x56, 0x56, 0x56, 0x56, 0x56, 0x56, 0x56 @ 081f0664 5a585858585858585656565656565656
    .byte  0x54, 0x54, 0x54, 0x54, 0x54, 0x54, 0x54, 0x53, 0x53, 0x53, 0x53, 0x53, 0x53, 0x53, 0x53, 0x53 @ 081f0674 54545454545454535353535353535353
    .byte  0x53, 0x53, 0x51, 0x51, 0x51, 0x51, 0x51, 0x4f, 0x4f, 0x4f, 0x4f, 0x4f, 0x4f, 0x4f, 0x4f, 0x4d @ 081f0684 535351515151514f4f4f4f4f4f4f4f4d
    .byte  0x4d, 0x4d, 0x4d, 0x4d, 0x4d, 0x4d, 0x4d, 0x4d, 0x4b, 0x44, 0x2c, 0x00 @ 081f0694 4d4d4d4d4d4d4d4d4b442c00
    ROM_INCBIN 0x1f06a0, 0x1740
    .word  0x03000300                     @ 081f1de0 00030003
    .word  gIntrTable                     @ 081f1de4 00000003
    .word  gIntrTable                     @ 081f1de8 00000003
    .word  gIntrTable                     @ 081f1dec 00000003
    .word  gIntrTable                     @ 081f1df0 00000003
    .word  gIntrTable                     @ 081f1df4 00000003
    .word  gIntrTable                     @ 081f1df8 00000003
    .word  gIntrTable                     @ 081f1dfc 00000003
    .word  gIntrTable                     @ 081f1e00 00000003
    .word  gIntrTable                     @ 081f1e04 00000003
    .word  gIntrTable                     @ 081f1e08 00000003
    .word  gIntrTable                     @ 081f1e0c 00000003
    .word  gIntrTable                     @ 081f1e10 00000003
    .word  gIntrTable                     @ 081f1e14 00000003
    .word  gIntrTable                     @ 081f1e18 00000003
    .word  gIntrTable                     @ 081f1e1c 00000003
    ROM_INCBIN 0x1f1e20, 0x102c4
    .word  0x02020201                     @ 082020e4 01020202
    .word  0x02020202                     @ 082020e8 02020202
    .word  0x02020202                     @ 082020ec 02020202
    .word  0x02020202                     @ 082020f0 02020202
    .word  0x02020202                     @ 082020f4 02020202
    .word  0x02020202                     @ 082020f8 02020202
    .word  0x02020202                     @ 082020fc 02020202
    .word  0x02020202                     @ 08202100 02020202
    .word  0x02020302                     @ 08202104 02030202
    .word  0x02020202                     @ 08202108 02020202
    .word  0x02020202                     @ 0820210c 02020202
    .word  0x02020202                     @ 08202110 02020202
    .word  0x02020202                     @ 08202114 02020202
    ROM_INCBIN 0x202118, 0xc4
    .word  0x02020201                     @ 082021dc 01020202
    .word  0x02020202                     @ 082021e0 02020202
    .word  0x02020202                     @ 082021e4 02020202
    .word  0x02020202                     @ 082021e8 02020202
    .word  0x02020202                     @ 082021ec 02020202
    .word  0x02020202                     @ 082021f0 02020202
    .word  0x02020202                     @ 082021f4 02020202
    .word  0x02020202                     @ 082021f8 02020202
    .word  0x02020202                     @ 082021fc 02020202
    .word  0x02020202                     @ 08202200 02020202
    .word  0x02020202                     @ 08202204 02020202
    ROM_INCBIN 0x202208, 0xcc
    .word  0x02010101                     @ 082022d4 01010102
    .word  0x02020202                     @ 082022d8 02020202
    .word  0x02020202                     @ 082022dc 02020202
    .word  0x02020202                     @ 082022e0 02020202
    .word  0x02020202                     @ 082022e4 02020202
    .word  0x02020202                     @ 082022e8 02020202
    .word  0x02020202                     @ 082022ec 02020202
    .word  0x02020202                     @ 082022f0 02020202
    .word  0x02020202                     @ 082022f4 02020202
    ROM_INCBIN 0x2022f8, 0x174c
    .word  0x09080908                     @ 08203a44 08090809
    .word  0x09090909                     @ 08203a48 09090909
    .word  0x09090909                     @ 08203a4c 09090909
    .word  0x09090909                     @ 08203a50 09090909
    .word  0x09090909                     @ 08203a54 09090909
    ROM_INCBIN 0x203a58, 0x430
    .word  0x02010101                     @ 08203e88 01010102
    .word  0x02010101                     @ 08203e8c 01010102
    .word  0x02020202                     @ 08203e90 02020202
    .word  0x02020202                     @ 08203e94 02020202
    .word  0x02020202                     @ 08203e98 02020202
    .word  0x02020202                     @ 08203e9c 02020202
    .word  0x02020202                     @ 08203ea0 02020202
    .word  0x02020202                     @ 08203ea4 02020202
    ROM_INCBIN 0x203ea8, 0x2f4c
    .word  0x02010201                     @ 08206df4 01020102
    .word  0x02020102                     @ 08206df8 02010202
    .word  0x02020202                     @ 08206dfc 02020202
    .word  0x02020202                     @ 08206e00 02020202
    .word  0x02020202                     @ 08206e04 02020202
    .word  0x02010202                     @ 08206e08 02020102
    ROM_INCBIN 0x206e0c, 0x15a4
    .word  0x02010001                     @ 082083b0 01000102
    .word  0x02020201                     @ 082083b4 01020202
    .word  0x02020202                     @ 082083b8 02020202
    .word  0x02020202                     @ 082083bc 02020202
    .word  0x02020202                     @ 082083c0 02020202
    .word  0x02020202                     @ 082083c4 02020202
    .word  0x02030201                     @ 082083c8 01020302
    .word  0x02030303                     @ 082083cc 03030302
    .word  0x02010203                     @ 082083d0 03020102
    .word  0x02020201                     @ 082083d4 01020202
    .word  0x02020202                     @ 082083d8 02020202
    .word  0x02020202                     @ 082083dc 02020202
    ROM_INCBIN 0x2083e0, 0x74
    .word  0x02020102                     @ 08208454 02010202
    .word  0x02020202                     @ 08208458 02020202
    .word  0x02020202                     @ 0820845c 02020202
    .word  0x02020202                     @ 08208460 02020202
    .word  0x02020202                     @ 08208464 02020202
    .word  0x02020202                     @ 08208468 02020202
    .word  0x02020202                     @ 0820846c 02020202
    .word  0x02020202                     @ 08208470 02020202
    .word  0x02010202                     @ 08208474 02020102
    ROM_INCBIN 0x208478, 0x53f04
    .word  0x02020201                     @ 0825c37c 01020202
    .word  0x02020202                     @ 0825c380 02020202
    .word  0x02020202                     @ 0825c384 02020202
    .word  0x02020202                     @ 0825c388 02020202
    .word  0x02020202                     @ 0825c38c 02020202
    ROM_INCBIN 0x25c390, 0x4c3bc
    .word  0x02020101                     @ 082a874c 01010202
    .word  0x02020202                     @ 082a8750 02020202
    .word  0x02020202                     @ 082a8754 02020202
    .word  0x02020202                     @ 082a8758 02020202
    .word  0x02020202                     @ 082a875c 02020202
    ROM_INCBIN 0x2a8760, 0x48
    .word  0x02020101                     @ 082a87a8 01010202
    .word  0x02020202                     @ 082a87ac 02020202
    .word  0x02020202                     @ 082a87b0 02020202
    .word  0x02020202                     @ 082a87b4 02020202
    .word  0x02030303                     @ 082a87b8 03030302
    .word  0x02020202                     @ 082a87bc 02020202
    ROM_INCBIN 0x2a87c0, 0x2cb8
    .word  0x02010000                     @ 082ab478 00000102
    .word  0x02020202                     @ 082ab47c 02020202
    .word  0x02020202                     @ 082ab480 02020202
    .word  0x02020202                     @ 082ab484 02020202
    .word  0x02020202                     @ 082ab488 02020202
    ROM_INCBIN 0x2ab48c, 0x5d88
LAB_082b1214:
    bx r8                                    @ 082b1214 4047
DAT_082b1216:
    ROM_INCBIN 0x2b1216, 0x151ae
    .word  0x02020000                     @ 082c63c4 00000202
    .word  0x02020202                     @ 082c63c8 02020202
    .word  0x02020202                     @ 082c63cc 02020202
    .word  0x02020202                     @ 082c63d0 02020202
    .word  0x02020202                     @ 082c63d4 02020202
    .word  0x02020202                     @ 082c63d8 02020202
    .word  0x02020202                     @ 082c63dc 02020202
    ROM_INCBIN 0x2c63e0, 0x17ec
    .word  0x02020202                     @ 082c7bcc 02020202
    .word  0x02020202                     @ 082c7bd0 02020202
    .word  0x02020202                     @ 082c7bd4 02020202
    .word  0x02020202                     @ 082c7bd8 02020202
    .word  0x02020202                     @ 082c7bdc 02020202
    .word  0x02020202                     @ 082c7be0 02020202
    .word  0x02020202                     @ 082c7be4 02020202
    .word  0x02020202                     @ 082c7be8 02020202
    ROM_INCBIN 0x2c7bec, 0x4d08
    .word  0x090b0b0b                     @ 082cc8f4 0b0b0b09
    .word  0x090b090b                     @ 082cc8f8 0b090b09
    .word  0x0909090b                     @ 082cc8fc 0b090909
    .word  0x09090909                     @ 082cc900 09090909
    .word  0x09060909                     @ 082cc904 09090609
    ROM_INCBIN 0x2cc908, 0x118
    .word  0x09090b09                     @ 082cca20 090b0909
    .word  0x09090909                     @ 082cca24 09090909
    .word  0x09090909                     @ 082cca28 09090909
    .word  0x09060906                     @ 082cca2c 06090609
    .word  0x09060906                     @ 082cca30 06090609
    ROM_INCBIN 0x2cca34, 0xfc
    .word  0x09090909                     @ 082ccb30 09090909
    .word  0x09090909                     @ 082ccb34 09090909
    .word  0x09090909                     @ 082ccb38 09090909
    .word  0x09090909                     @ 082ccb3c 09090909
    .word  0x09090909                     @ 082ccb40 09090909
    .word  0x09090909                     @ 082ccb44 09090909
    ROM_INCBIN 0x2ccb48, 0x280
    .word  0x02020402                     @ 082ccdc8 02040202
    .word  0x02020204                     @ 082ccdcc 04020202
    .word  0x02020202                     @ 082ccdd0 02020202
    .word  0x02000202                     @ 082ccdd4 02020002
    .word  0x02020002                     @ 082ccdd8 02000202
    ROM_INCBIN 0x2ccddc, 0x1ec
    .word  0x02020200                     @ 082ccfc8 00020202
    .word  0x02020202                     @ 082ccfcc 02020202
    .word  0x02020002                     @ 082ccfd0 02000202
    .word  0x02020202                     @ 082ccfd4 02020202
    .word  0x02020202                     @ 082ccfd8 02020202
    .word  0x02020202                     @ 082ccfdc 02020202
    .word  0x02020202                     @ 082ccfe0 02020202
    ROM_INCBIN 0x2ccfe4, 0x11c
    .word  0x02020202                     @ 082cd100 02020202
    .word  0x02020202                     @ 082cd104 02020202
    .word  0x02020202                     @ 082cd108 02020202
    .word  0x02020202                     @ 082cd10c 02020202
    .word  0x02020202                     @ 082cd110 02020202
    .word  0x02020202                     @ 082cd114 02020202
    .word  0x02020202                     @ 082cd118 02020202
    ROM_INCBIN 0x2cd11c, 0x24
    .word  0x02020202                     @ 082cd140 02020202
    .word  0x02020402                     @ 082cd144 02040202
    .word  0x02020202                     @ 082cd148 02020202
    .word  0x02020202                     @ 082cd14c 02020202
    .word  0x02020200                     @ 082cd150 00020202
    .word  0x02020002                     @ 082cd154 02000202
    ROM_INCBIN 0x2cd158, 0x100
    .word  0x02020202                     @ 082cd258 02020202
    .word  0x02020202                     @ 082cd25c 02020202
    .word  0x02020204                     @ 082cd260 04020202
    .word  0x02020202                     @ 082cd264 02020202
    .word  0x02020202                     @ 082cd268 02020202
    .word  0x02020202                     @ 082cd26c 02020202
    .word  0x02020202                     @ 082cd270 02020202
    ROM_INCBIN 0x2cd274, 0x1f90
    .word  0x02020201                     @ 082cf204 01020202
    .word  0x02020202                     @ 082cf208 02020202
    .word  0x02020202                     @ 082cf20c 02020202
    .word  0x02020202                     @ 082cf210 02020202
    .word  0x02020202                     @ 082cf214 02020202
    .word  0x02020202                     @ 082cf218 02020202
    .word  0x02020202                     @ 082cf21c 02020202
    ROM_INCBIN 0x2cf220, 0x88
    .word  0x02010101                     @ 082cf2a8 01010102
    .word  0x02020202                     @ 082cf2ac 02020202
    .word  0x02020202                     @ 082cf2b0 02020202
    .word  0x02020202                     @ 082cf2b4 02020202
    .word  0x02020202                     @ 082cf2b8 02020202
    .word  0x02020202                     @ 082cf2bc 02020202
    .word  0x02020202                     @ 082cf2c0 02020202
    .word  0x02020202                     @ 082cf2c4 02020202
    .word  0x02020202                     @ 082cf2c8 02020202
    .word  0x02020202                     @ 082cf2cc 02020202
    .word  0x02020202                     @ 082cf2d0 02020202
    .word  0x02020202                     @ 082cf2d4 02020202
    .word  0x02020202                     @ 082cf2d8 02020202
    .word  0x02020202                     @ 082cf2dc 02020202
    .word  0x02020202                     @ 082cf2e0 02020202
    ROM_INCBIN 0x2cf2e4, 0x70
    .word  0x02020201                     @ 082cf354 01020202
    .word  0x02020202                     @ 082cf358 02020202
    .word  0x02020202                     @ 082cf35c 02020202
    .word  0x02020202                     @ 082cf360 02020202
    .word  0x02020202                     @ 082cf364 02020202
    .word  0x02020202                     @ 082cf368 02020202
    .word  0x02020202                     @ 082cf36c 02020202
    .word  0x02020202                     @ 082cf370 02020202
    .word  0x02020202                     @ 082cf374 02020202
    .word  0x02020202                     @ 082cf378 02020202
    .word  0x02020202                     @ 082cf37c 02020202
    ROM_INCBIN 0x2cf380, 0x7c
    .word  0x02020202                     @ 082cf3fc 02020202
    .word  0x02020202                     @ 082cf400 02020202
    .word  0x02020202                     @ 082cf404 02020202
    .word  0x02020202                     @ 082cf408 02020202
    .word  0x02020202                     @ 082cf40c 02020202
    .word  0x02020202                     @ 082cf410 02020202
    .word  0x02020202                     @ 082cf414 02020202
    .word  0x02020202                     @ 082cf418 02020202
    .word  0x02020202                     @ 082cf41c 02020202
    .word  0x02020202                     @ 082cf420 02020202
    .word  0x02020201                     @ 082cf424 01020202
    ROM_INCBIN 0x2cf428, 0x7c
    .word  0x02010101                     @ 082cf4a4 01010102
    .word  0x02020202                     @ 082cf4a8 02020202
    .word  0x02020202                     @ 082cf4ac 02020202
    .word  0x02020202                     @ 082cf4b0 02020202
    .word  0x02020202                     @ 082cf4b4 02020202
    .word  0x02020202                     @ 082cf4b8 02020202
    .word  0x02020202                     @ 082cf4bc 02020202
    .word  0x02020202                     @ 082cf4c0 02020202
    ROM_INCBIN 0x2cf4c4, 0x36e8
    .word  0x02020102                     @ 082d2bac 02010202
    .word  0x02020104                     @ 082d2bb0 04010202
    .word  0x02030202                     @ 082d2bb4 02020302
    .word  0x02030303                     @ 082d2bb8 03030302
    .word  0x02020302                     @ 082d2bbc 02030202
    ROM_INCBIN 0x2d2bc0, 0xe88
    .word  0x02010202                     @ 082d3a48 02020102
    .word  0x02020302                     @ 082d3a4c 02030202
    .word  0x02020201                     @ 082d3a50 01020202
    .word  0x02010202                     @ 082d3a54 02020102
    .word  0x02010302                     @ 082d3a58 02030102
    ROM_INCBIN 0x2d3a5c, 0x48
    .word  0x02020201                     @ 082d3aa4 01020202
    .word  0x02020201                     @ 082d3aa8 01020202
    .word  0x02010102                     @ 082d3aac 02010102
    .word  0x02020101                     @ 082d3ab0 01010202
    .word  0x02010202                     @ 082d3ab4 02020102
    .word  0x02010202                     @ 082d3ab8 02020102
    .word  0x02020201                     @ 082d3abc 01020202
    .word  0x02010202                     @ 082d3ac0 02020102
    .word  0x02020202                     @ 082d3ac4 02020202
    ROM_INCBIN 0x2d3ac8, 0x12c8
    .word  0x02010301                     @ 082d4d90 01030102
    .word  0x02010301                     @ 082d4d94 01030102
    .word  0x02020301                     @ 082d4d98 01030202
    .word  0x02020301                     @ 082d4d9c 01030202
    .word  0x02020301                     @ 082d4da0 01030202
    .word  0x02020301                     @ 082d4da4 01030202
    ROM_INCBIN 0x2d4da8, 0xb4
    .word  0x02000200                     @ 082d4e5c 00020002
    .word  0x02000201                     @ 082d4e60 01020002
    .word  0x02000200                     @ 082d4e64 00020002
    .word  0x02000100                     @ 082d4e68 00010002
    .word  0x02000100                     @ 082d4e6c 00010002
    .word  0x02010100                     @ 082d4e70 00010102
    ROM_INCBIN 0x2d4e74, 0x57cb8
    .word  0x08060605                     @ 0832cb2c 05060608
    .word  0x08070806                     @ 0832cb30 06080708
    .word  0x08070806                     @ 0832cb34 06080708
    .word  0x08070806                     @ 0832cb38 06080708
    .word  0x08070806                     @ 0832cb3c 06080708
    .word  0x08070806                     @ 0832cb40 06080708
    .word  0x08070806                     @ 0832cb44 06080708
    .word  0x08070806                     @ 0832cb48 06080708
    .word  0x08070806                     @ 0832cb4c 06080708
    .word  0x08070806                     @ 0832cb50 06080708
    ROM_INCBIN 0x32cb54, 0xdc4
    .word  0x02020202                     @ 0832d918 02020202
    .word  0x02020202                     @ 0832d91c 02020202
    .word  0x02020203                     @ 0832d920 03020202
    .word  0x02030103                     @ 0832d924 03010302
    .word  0x02000103                     @ 0832d928 03010002
    .word  0x02000200                     @ 0832d92c 00020002
    .word  0x02000201                     @ 0832d930 01020002
    .word  0x02000101                     @ 0832d934 01010002
    ROM_INCBIN 0x32d938, 0x11c
    .word  0x02030103                     @ 0832da54 03010302
    .word  0x02030103                     @ 0832da58 03010302
    .word  0x02030103                     @ 0832da5c 03010302
    .word  0x02030103                     @ 0832da60 03010302
    .word  0x02000103                     @ 0832da64 03010002
    .word  0x02000200                     @ 0832da68 00020002
    .word  0x02000201                     @ 0832da6c 01020002
    .word  0x02000101                     @ 0832da70 01010002
    ROM_INCBIN 0x32da74, 0x238
    .word  0x02010301                     @ 0832dcac 01030102
    .word  0x02010301                     @ 0832dcb0 01030102
    .word  0x02010301                     @ 0832dcb4 01030102
    .word  0x02010302                     @ 0832dcb8 02030102
    .word  0x02010202                     @ 0832dcbc 02020102
    .word  0x02020202                     @ 0832dcc0 02020202
    .word  0x02020202                     @ 0832dcc4 02020202
    .word  0x02020202                     @ 0832dcc8 02020202
    .word  0x02020202                     @ 0832dccc 02020202
    .word  0x02020202                     @ 0832dcd0 02020202
    ROM_INCBIN 0x32dcd4, 0x104
    .word  0x02010101                     @ 0832ddd8 01010102
    .word  0x02030201                     @ 0832dddc 01020302
    .word  0x02010202                     @ 0832dde0 02020102
    .word  0x02010202                     @ 0832dde4 02020102
    .word  0x02010202                     @ 0832dde8 02020102
    .word  0x02020202                     @ 0832ddec 02020202
    .word  0x02020202                     @ 0832ddf0 02020202
    ROM_INCBIN 0x32ddf4, 0x13c
    .word  0x02010202                     @ 0832df30 02020102
    .word  0x02010202                     @ 0832df34 02020102
    .word  0x02020202                     @ 0832df38 02020202
    .word  0x02020202                     @ 0832df3c 02020202
    .word  0x02020202                     @ 0832df40 02020202
    .word  0x02010202                     @ 0832df44 02020102
    .word  0x02030201                     @ 0832df48 01020302
    .word  0x02010100                     @ 0832df4c 00010102
    .word  0x02000200                     @ 0832df50 00020002
    .word  0x02000200                     @ 0832df54 00020002
    .word  0x02000201                     @ 0832df58 01020002
    .word  0x02000101                     @ 0832df5c 01010002
    .word  0x02000101                     @ 0832df60 01010002
    .word  0x02010101                     @ 0832df64 01010102
    .word  0x02000101                     @ 0832df68 01010002
    ROM_INCBIN 0x32df6c, 0x3e6c
    .word  0x090a0909                     @ 08331dd8 09090a09
    .word  0x09090909                     @ 08331ddc 09090909
    .word  0x090a0909                     @ 08331de0 09090a09
    .word  0x090a0909                     @ 08331de4 09090a09
    .word  0x090a0909                     @ 08331de8 09090a09
    .word  0x09090909                     @ 08331dec 09090909
    .word  0x09090909                     @ 08331df0 09090909
    .word  0x09090a09                     @ 08331df4 090a0909
    ROM_INCBIN 0x331df8, 0x120
    .word  0x09090909                     @ 08331f18 09090909
    .word  0x09080909                     @ 08331f1c 09090809
    .word  0x09080909                     @ 08331f20 09090809
    .word  0x09080909                     @ 08331f24 09090809
    .word  0x09080909                     @ 08331f28 09090809
    .word  0x09080909                     @ 08331f2c 09090809
    .word  0x09090909                     @ 08331f30 09090909
    ROM_INCBIN 0x331f34, 0x1164
    .word  0x02010201                     @ 08333098 01020102
    .word  0x02020102                     @ 0833309c 02010202
    .word  0x02020103                     @ 083330a0 03010202
    .word  0x02020103                     @ 083330a4 03010202
    .word  0x02020103                     @ 083330a8 03010202
    .word  0x02020103                     @ 083330ac 03010202
    ROM_INCBIN 0x3330b0, 0x128
    .word  0x02000200                     @ 083331d8 00020002
    .word  0x02000100                     @ 083331dc 00010002
    .word  0x02000200                     @ 083331e0 00020002
    .word  0x02000200                     @ 083331e4 00020002
    .word  0x02000200                     @ 083331e8 00020002
    .word  0x02000200                     @ 083331ec 00020002
    .word  0x02000200                     @ 083331f0 00020002
    .word  0x02000200                     @ 083331f4 00020002
    .word  0x02000200                     @ 083331f8 00020002
    .word  0x02010200                     @ 083331fc 00020102
    .word  0x02010200                     @ 08333200 00020102
    ROM_INCBIN 0x333204, 0x2bf4
    .word  0x090b090b                     @ 08335df8 0b090b09
    .word  0x090b0a0b                     @ 08335dfc 0b0a0b09
    .word  0x090b0a0b                     @ 08335e00 0b0a0b09
    .word  0x090b0a0b                     @ 08335e04 0b0a0b09
    .word  0x090b0a0a                     @ 08335e08 0a0a0b09
    .word  0x090b0a0a                     @ 08335e0c 0a0a0b09
    ROM_INCBIN 0x335e10, 0x264
    .word  0x09090909                     @ 08336074 09090909
    .word  0x09090909                     @ 08336078 09090909
    .word  0x09090909                     @ 0833607c 09090909
    .word  0x090a0909                     @ 08336080 09090a09
    .word  0x090a0909                     @ 08336084 09090a09
    .word  0x090a0909                     @ 08336088 09090a09
    .byte  0x09, 0x09, 0x09, 0x08
    .word  0x09090808                     @ 08336090 08080909
    .word  0x09090909                     @ 08336094 09090909
    .word  0x09080809                     @ 08336098 09080809
    .word  0x09080807                     @ 0833609c 07080809
    .word  0x09080907                     @ 083360a0 07090809
    ROM_INCBIN 0x3360a4, 0x108
    .word  0x08080708                     @ 083361ac 08070808
    .word  0x09070907                     @ 083361b0 07090709
    .word  0x09070807                     @ 083361b4 07080709
    .word  0x08070808                     @ 083361b8 08080708
    .word  0x08070808                     @ 083361bc 08080708
    ROM_INCBIN 0x3361c0, 0xc58
    .word  0x02010100                     @ 08336e18 00010102
    .word  0x02020202                     @ 08336e1c 02020202
    .word  0x02020203                     @ 08336e20 03020202
    .word  0x02020202                     @ 08336e24 02020202
    .word  0x02020203                     @ 08336e28 03020202
    .byte  0x03, 0x02, 0x02, 0x01, 0x03, 0x01, 0x03, 0x01
    .word  0x02030202                     @ 08336e34 02020302
    .word  0x02030202                     @ 08336e38 02020302
    .word  0x02030202                     @ 08336e3c 02020302
    .word  0x02030202                     @ 08336e40 02020302
    .word  0x02020202                     @ 08336e44 02020202
    ROM_INCBIN 0x336e48, 0x12c
    .word  0x02000100                     @ 08336f74 00010002
    .word  0x02000101                     @ 08336f78 01010002
    .word  0x02000100                     @ 08336f7c 00010002
    .word  0x02000100                     @ 08336f80 00010002
    .word  0x02000100                     @ 08336f84 00010002
    .word  0x02000200                     @ 08336f88 00020002
    .word  0x02000200                     @ 08336f8c 00020002
    .word  0x02010200                     @ 08336f90 00020102
    ROM_INCBIN 0x336f94, 0x3974
    .word  0x09070709                     @ 0833a908 09070709
    .word  0x08070907                     @ 0833a90c 07090708
    .word  0x080a0909                     @ 0833a910 09090a08
    .word  0x080a0909                     @ 0833a914 09090a08
    .word  0x080a0909                     @ 0833a918 09090a08
    .word  0x080a0909                     @ 0833a91c 09090a08
    .word  0x080a0909                     @ 0833a920 09090a08
    .byte  0x09, 0x09, 0x09, 0x08
    .word  0x09090909                     @ 0833a928 09090909
    .word  0x09090909                     @ 0833a92c 09090909
    .word  0x09090909                     @ 0833a930 09090909
    .word  0x0909090a                     @ 0833a934 0a090909
    .word  0x0909090a                     @ 0833a938 0a090909
    ROM_INCBIN 0x33a93c, 0x11c
    .word  0x080a0809                     @ 0833aa58 09080a08
    .word  0x080a0809                     @ 0833aa5c 09080a08
    .word  0x080a0909                     @ 0833aa60 09090a08
    .word  0x09090909                     @ 0833aa64 09090909
    .word  0x09090a08                     @ 0833aa68 080a0909
    ROM_INCBIN 0x33aa6c, 0x25c
    .word  0x08070507                     @ 0833acc8 07050708
    .word  0x08060807                     @ 0833accc 07080608
    .word  0x08060807                     @ 0833acd0 07080608
    .word  0x08060707                     @ 0833acd4 07070608
    .word  0x08070707                     @ 0833acd8 07070708
    .word  0x08070707                     @ 0833acdc 07070708
    ROM_INCBIN 0x33ace0, 0x9c0
    .word  0x02010100                     @ 0833b6a0 00010102
    .word  0x02010100                     @ 0833b6a4 00010102
    .word  0x02010101                     @ 0833b6a8 01010102
    .word  0x02010101                     @ 0833b6ac 01010102
    .word  0x02010101                     @ 0833b6b0 01010102
    .word  0x02010101                     @ 0833b6b4 01010102
    ROM_INCBIN 0x33b6b8, 0x26e0
    .word  0x09090909                     @ 0833dd98 09090909
    .word  0x09090909                     @ 0833dd9c 09090909
    .word  0x09090909                     @ 0833dda0 09090909
    .word  0x09090909                     @ 0833dda4 09090909
    .word  0x09090909                     @ 0833dda8 09090909
    .word  0x09090909                     @ 0833ddac 09090909
    .word  0x09090909                     @ 0833ddb0 09090909
    .word  0x09090909                     @ 0833ddb4 09090909
    .word  0x09090909                     @ 0833ddb8 09090909
    .word  0x09090909                     @ 0833ddbc 09090909
    .word  0x09090909                     @ 0833ddc0 09090909
    .word  0x09090909                     @ 0833ddc4 09090909
    .word  0x09090909                     @ 0833ddc8 09090909
    .word  0x09090909                     @ 0833ddcc 09090909
    .word  0x09090909                     @ 0833ddd0 09090909
    .word  0x09090909                     @ 0833ddd4 09090909
    .word  0x09090909                     @ 0833ddd8 09090909
    .word  0x09090909                     @ 0833dddc 09090909
    .word  0x09090909                     @ 0833dde0 09090909
    ROM_INCBIN 0x33dde4, 0x13dc
    .word  0x02020201                     @ 0833f1c0 01020202
    .word  0x02020202                     @ 0833f1c4 02020202
    .word  0x02020202                     @ 0833f1c8 02020202
    .word  0x02020202                     @ 0833f1cc 02020202
    .word  0x02020202                     @ 0833f1d0 02020202
    ROM_INCBIN 0x33f1d4, 0x1ebc
    .word  0x09090908                     @ 08341090 08090909
    .word  0x09090909                     @ 08341094 09090909
    .word  0x09090909                     @ 08341098 09090909
    .word  0x09090909                     @ 0834109c 09090909
    .word  0x09090909                     @ 083410a0 09090909
    .word  0x09090909                     @ 083410a4 09090909
    .word  0x09090909                     @ 083410a8 09090909
    .word  0x09090909                     @ 083410ac 09090909
    .word  0x09090909                     @ 083410b0 09090909
    .word  0x09090909                     @ 083410b4 09090909
    .word  0x09090909                     @ 083410b8 09090909
    .word  0x09090909                     @ 083410bc 09090909
    .word  0x09090909                     @ 083410c0 09090909
    .word  0x09090909                     @ 083410c4 09090909
    .word  0x09090909                     @ 083410c8 09090909
    .word  0x09090909                     @ 083410cc 09090909
    .word  0x09090909                     @ 083410d0 09090909
    .word  0x09090909                     @ 083410d4 09090909
    .word  0x09090909                     @ 083410d8 09090909
    ROM_INCBIN 0x3410dc, 0x1e84
    .word  0x02020201                     @ 08342f60 01020202
    .word  0x02020202                     @ 08342f64 02020202
    .word  0x02020202                     @ 08342f68 02020202
    .word  0x02020202                     @ 08342f6c 02020202
    .word  0x02020202                     @ 08342f70 02020202
    .word  0x02020202                     @ 08342f74 02020202
    .word  0x02020202                     @ 08342f78 02020202
    ROM_INCBIN 0x342f7c, 0x1380
    .word  0x09080808                     @ 083442fc 08080809
    .word  0x09090909                     @ 08344300 09090909
    .word  0x09090909                     @ 08344304 09090909
    .word  0x09090909                     @ 08344308 09090909
    .word  0x09090909                     @ 0834430c 09090909
    .word  0x09090909                     @ 08344310 09090909
    .word  0x09090909                     @ 08344314 09090909
    .word  0x09090909                     @ 08344318 09090909
    .word  0x09090909                     @ 0834431c 09090909
    .word  0x09090909                     @ 08344320 09090909
    .word  0x09090909                     @ 08344324 09090909
    .word  0x09090909                     @ 08344328 09090909
    .word  0x09090909                     @ 0834432c 09090909
    .word  0x09090909                     @ 08344330 09090909
    .word  0x09090909                     @ 08344334 09090909
    .word  0x09090909                     @ 08344338 09090909
    .word  0x09090909                     @ 0834433c 09090909
    .word  0x09090909                     @ 08344340 09090909
    .word  0x09090909                     @ 08344344 09090909
    .word  0x09090909                     @ 08344348 09090909
    ROM_INCBIN 0x34434c, 0x161c
    .word  0x02010101                     @ 08345968 01010102
    .word  0x02020202                     @ 0834596c 02020202
    .word  0x02020202                     @ 08345970 02020202
    .word  0x02020202                     @ 08345974 02020202
    .word  0x02020202                     @ 08345978 02020202
    ROM_INCBIN 0x34597c, 0x608
    .word  0x02010101                     @ 08345f84 01010102
    .word  0x02020202                     @ 08345f88 02020202
    .word  0x02020202                     @ 08345f8c 02020202
    .word  0x02020202                     @ 08345f90 02020202
    .word  0x02020202                     @ 08345f94 02020202
    ROM_INCBIN 0x345f98, 0x1564
    .word  0x09090909                     @ 083474fc 09090909
    .word  0x09090909                     @ 08347500 09090909
    .word  0x09090909                     @ 08347504 09090909
    .word  0x09090909                     @ 08347508 09090909
    .word  0x09090909                     @ 0834750c 09090909
    .word  0x09090909                     @ 08347510 09090909
    .word  0x09090909                     @ 08347514 09090909
    .word  0x09090909                     @ 08347518 09090909
    .word  0x09090909                     @ 0834751c 09090909
    .word  0x09090909                     @ 08347520 09090909
    .word  0x09090909                     @ 08347524 09090909
    .word  0x09090909                     @ 08347528 09090909
    .word  0x09090909                     @ 0834752c 09090909
    .word  0x09090909                     @ 08347530 09090909
    .word  0x09090909                     @ 08347534 09090909
    .word  0x09090909                     @ 08347538 09090909
    .word  0x09090909                     @ 0834753c 09090909
    .word  0x09090909                     @ 08347540 09090909
    .word  0x09090909                     @ 08347544 09090909
    ROM_INCBIN 0x347548, 0x1728
    .word  0x02010101                     @ 08348c70 01010102
    .word  0x02020202                     @ 08348c74 02020202
    .word  0x02020202                     @ 08348c78 02020202
    .word  0x02020202                     @ 08348c7c 02020202
    .word  0x02020202                     @ 08348c80 02020202
    ROM_INCBIN 0x348c84, 0x2398
    .word  0x02020202                     @ 0834b01c 02020202
    .word  0x02020202                     @ 0834b020 02020202
    .word  0x02020202                     @ 0834b024 02020202
    .word  0x02020202                     @ 0834b028 02020202
    .word  0x02020202                     @ 0834b02c 02020202
    .word  0x02020202                     @ 0834b030 02020202
    ROM_INCBIN 0x34b034, 0x15de6
    b LAB_083615d2                           @ 08360e1a dae3
    ROM_INCBIN 0x360e1c, 0x7b6
LAB_083615d2:
    .hword 0xf7f2    @ 083615d2 f2f7
    lsls r7,r7,#0x1f    @ 083615d4 ff07
    asrs r7,r1,#0x10    @ 083615d6 0f14
    adds r7,r2,#0x0    @ 083615d8 171c
    subs r6,r3,r0    @ 083615da 1e1a
    asrs r5,r2,#0x10    @ 083615dc 1514
    adds r7,r2,#0x4    @ 083615de 171d
    movs r0,#0x20    @ 083615e0 2020
    adds r5,r3,r4    @ 083615e2 1d19
    asrs r5,r2,#0xc    @ 083615e4 1513
    asrs r7,r1,#0x20    @ 083615e6 0f10
    lsrs r1,r2,#0x18    @ 083615e8 110e
    lsls r1,r1,#0x1c    @ 083615ea 0907
    lsls r6,r0,#0x14    @ 083615ec 0605
    lsrs r5,r0,#0x8    @ 083615ee 050a
    subs r3,r2,#0x0    @ 083615f0 131e
    adds r2,#0x2b    @ 083615f2 2b32
    movs r7,#0x2f    @ 083615f4 2f27
    adds r7,r3,#0x0    @ 083615f6 1f1c
    cmp r4,#0x1f                             @ 083615f8 1f2c
    .hword 0x463c    @ 083615fa 3c46
    bx r9                                    @ 083615fc 4847
    ROM_INCBIN 0x3615fe, 0x20032
    .word  0x02030304                     @ 08381630 04030302
    .word  0x02030303                     @ 08381634 03030302
    .word  0x02010303                     @ 08381638 03030102
    .word  0x02010301                     @ 0838163c 01030102
    .word  0x02020102                     @ 08381640 02010202
    ROM_INCBIN 0x381644, 0x280
    .word  0x02020202                     @ 083818c4 02020202
    .word  0x02020202                     @ 083818c8 02020202
    .word  0x02020202                     @ 083818cc 02020202
    .word  0x02020203                     @ 083818d0 03020202
    .word  0x02020202                     @ 083818d4 02020202
    ROM_INCBIN 0x3818d8, 0x10c05c
    .word  0x02010000                     @ 0848d934 00000102
    .word  0x02030202                     @ 0848d938 02020302
    .word  0x02020202                     @ 0848d93c 02020202
    .word  0x02020202                     @ 0848d940 02020202
    .word  0x02020202                     @ 0848d944 02020202
    .word  0x02020202                     @ 0848d948 02020202
    .word  0x02020202                     @ 0848d94c 02020202
    ROM_INCBIN 0x48d950, 0xcc8
    .word  0x02010100                     @ 0848e618 00010102
    .word  0x02020202                     @ 0848e61c 02020202
    .word  0x02020202                     @ 0848e620 02020202
    .word  0x02020202                     @ 0848e624 02020202
    .word  0x02020202                     @ 0848e628 02020202
    ROM_INCBIN 0x48e62c, 0x170
    .word  0x02020101                     @ 0848e79c 01010202
    .word  0x02020202                     @ 0848e7a0 02020202
    .word  0x02020202                     @ 0848e7a4 02020202
    .word  0x02020202                     @ 0848e7a8 02020202
    .word  0x02020202                     @ 0848e7ac 02020202
    ROM_INCBIN 0x48e7b0, 0x2cf8c
    .word  0x02020101                     @ 084bb73c 01010202
    .word  0x02020202                     @ 084bb740 02020202
    .word  0x02020202                     @ 084bb744 02020202
    .word  0x02020202                     @ 084bb748 02020202
    .word  0x02020202                     @ 084bb74c 02020202
    ROM_INCBIN 0x4bb750, 0x2fc0
DWORD_084be710:
    .word  0x00000000                     @ 084be710 00000000
DWORD_084be714:
    .word  0x00000000                     @ 084be714 00000000
DWORD_084be718:
    .word  0x00000000                     @ 084be718 00000000
DWORD_084be71c:
    .word  0x00000000                     @ 084be71c 00000000
    ROM_INCBIN 0x4be720, 0x9f0
DWORD_084bf110:
    .word  0x80208010                     @ 084bf110 10802080
    ROM_INCBIN 0x4bf114, 0xfc
    .word  0x02020201                     @ 084bf210 01020202
    .word  0x02020202                     @ 084bf214 02020202
    .word  0x02020202                     @ 084bf218 02020202
    .word  0x02020202                     @ 084bf21c 02020202
    .word  0x02020202                     @ 084bf220 02020202
    ROM_INCBIN 0x4bf224, 0x13dd
    .byte  0x20, 0x22, 0x23, 0x24, 0x26, 0x27, 0x29, 0x2a, 0x2c, 0x2d, 0x2e, 0x30, 0x31, 0x33, 0x34, 0x36 @ 084c0601 202223242627292a2c2d2e3031333436
    .byte  0x37, 0x38, 0x3a, 0x3b, 0x3d, 0x3e, 0x40, 0x41, 0x42, 0x44, 0x45, 0x47, 0x48, 0x49, 0x4b, 0x4c @ 084c0611 37383a3b3d3e40414244454748494b4c
    .byte  0x4e, 0x4f, 0x50, 0x52, 0x53, 0x53, 0x53, 0x00 @ 084c0621 4e4f505253535300
    ROM_INCBIN 0x4c0629, 0x223
    .byte  0x35, 0x37, 0x38, 0x3a, 0x3b, 0x3d, 0x3f, 0x40, 0x42, 0x43, 0x45, 0x46, 0x48, 0x4a, 0x4b, 0x4d @ 084c084c 3537383a3b3d3f4042434546484a4b4d
    .byte  0x4e, 0x50, 0x51, 0x53, 0x54, 0x56, 0x58, 0x59, 0x5b, 0x5c, 0x5c, 0x5c, 0x00 @ 084c085c 4e505153545658595b5c5c5c00
    ROM_INCBIN 0x4c0869, 0x254
    .byte  0x21, 0x23, 0x24, 0x26, 0x28, 0x29, 0x2b, 0x2d, 0x2f, 0x30, 0x32, 0x34, 0x36, 0x37, 0x39, 0x3b @ 084c0abd 2123242628292b2d2f3032343637393b
    .byte  0x3d, 0x3e, 0x40, 0x42, 0x44, 0x45, 0x47, 0x49, 0x4b, 0x4c, 0x4e, 0x50, 0x52, 0x53, 0x55, 0x57 @ 084c0acd 3d3e4042444547494b4c4e5052535557
    .byte  0x59, 0x5a, 0x5c, 0x5e, 0x5f, 0x61, 0x63, 0x65, 0x66, 0x66, 0x66, 0x00 @ 084c0add 595a5c5e5f61636566666600
    ROM_INCBIN 0x4c0ae9, 0x351
    .byte  0x20, 0x22, 0x24, 0x26, 0x27, 0x29, 0x2b, 0x2d, 0x2f, 0x31, 0x33, 0x35, 0x37, 0x39, 0x3b, 0x3d @ 084c0e3a 2022242627292b2d2f31333537393b3d
    .byte  0x3f, 0x41, 0x43, 0x45, 0x47, 0x49, 0x4b, 0x4d, 0x4f, 0x51, 0x53, 0x55, 0x57, 0x59, 0x5b, 0x5d @ 084c0e4a 3f41434547494b4d4f51535557595b5d
    .byte  0x5f, 0x61, 0x63, 0x65, 0x67, 0x69, 0x6b, 0x6d, 0x6f, 0x70, 0x72, 0x74, 0x74, 0x74, 0x00 @ 084c0e5a 5f61636567696b6d6f707274747400
    ROM_INCBIN 0x4c0e69, 0x273f
    .byte  0x20, 0x20, 0x20, 0x20, 0x21, 0x21, 0x21, 0x21, 0x22, 0x22, 0x22, 0x22, 0x23, 0x23, 0x23, 0x24 @ 084c35a8 20202020212121212222222223232324
    .byte  0x20, 0x20, 0x20, 0x20, 0x21, 0x21, 0x21, 0x21, 0x22, 0x22, 0x22, 0x22, 0x23, 0x23, 0x23, 0x24 @ 084c35b8 20202020212121212222222223232324
    .byte  0x20, 0x20, 0x20, 0x20, 0x21, 0x21, 0x21, 0x21, 0x22, 0x22, 0x22, 0x22, 0x23, 0x23, 0x23, 0x24 @ 084c35c8 20202020212121212222222223232324
    .byte  0x20, 0x20, 0x20, 0x20, 0x21, 0x21, 0x21, 0x21, 0x22, 0x22, 0x22, 0x22, 0x23, 0x23, 0x23, 0x24 @ 084c35d8 20202020212121212222222223232324
    .byte  0x30, 0x30, 0x30, 0x30, 0x31, 0x31, 0x31, 0x31, 0x32, 0x32, 0x32, 0x32, 0x33, 0x33, 0x33, 0x34 @ 084c35e8 30303030313131313232323233333334
    .byte  0x30, 0x30, 0x30, 0x30, 0x31, 0x31, 0x31, 0x31, 0x32, 0x32, 0x32, 0x32, 0x33, 0x33, 0x33, 0x34 @ 084c35f8 30303030313131313232323233333334
    .byte  0x30, 0x30, 0x30, 0x30, 0x31, 0x31, 0x31, 0x31, 0x32, 0x32, 0x32, 0x32, 0x33, 0x33, 0x33, 0x34 @ 084c3608 30303030313131313232323233333334
    .byte  0x40, 0x40, 0x40, 0x40, 0x41, 0x41, 0x41, 0x41, 0x42, 0x42, 0x42, 0x42, 0x43, 0x43, 0x43, 0x44 @ 084c3618 40404040414141414242424243434344
    .byte  0x00                           @ 084c3628 00
    ROM_INCBIN 0x4c3629, 0x5f
    .byte  0x20, 0x20, 0x20, 0x21, 0x21, 0x21, 0x22, 0x22, 0x22, 0x23, 0x23, 0x23, 0x24, 0x24, 0x24, 0x25 @ 084c3688 20202021212122222223232324242425
    .byte  0x20, 0x20, 0x20, 0x21, 0x21, 0x21, 0x22, 0x22, 0x22, 0x23, 0x23, 0x23, 0x24, 0x24, 0x24, 0x25 @ 084c3698 20202021212122222223232324242425
    .byte  0x20, 0x20, 0x20, 0x21, 0x21, 0x21, 0x22, 0x22, 0x22, 0x23, 0x23, 0x23, 0x24, 0x24, 0x24, 0x25 @ 084c36a8 20202021212122222223232324242425
    .byte  0x30, 0x30, 0x30, 0x31, 0x31, 0x31, 0x32, 0x32, 0x32, 0x33, 0x33, 0x33, 0x34, 0x34, 0x34, 0x35 @ 084c36b8 30303031313132323233333334343435
    .byte  0x30, 0x30, 0x30, 0x31, 0x31, 0x31, 0x32, 0x32, 0x32, 0x33, 0x33, 0x33, 0x34, 0x34, 0x34, 0x35 @ 084c36c8 30303031313132323233333334343435
    .byte  0x30, 0x30, 0x30, 0x31, 0x31, 0x31, 0x32, 0x32, 0x32, 0x33, 0x33, 0x33, 0x34, 0x34, 0x34, 0x35 @ 084c36d8 30303031313132323233333334343435
    .byte  0x40, 0x40, 0x40, 0x41, 0x41, 0x41, 0x42, 0x42, 0x42, 0x43, 0x43, 0x43, 0x44, 0x44, 0x44, 0x45 @ 084c36e8 40404041414142424243434344444445
    .byte  0x40, 0x40, 0x40, 0x41, 0x41, 0x41, 0x42, 0x42, 0x42, 0x43, 0x43, 0x43, 0x44, 0x44, 0x44, 0x45 @ 084c36f8 40404041414142424243434344444445
    .byte  0x40, 0x40, 0x40, 0x41, 0x41, 0x41, 0x42, 0x42, 0x42, 0x43, 0x43, 0x43, 0x44, 0x44, 0x44, 0x45 @ 084c3708 40404041414142424243434344444445
    .byte  0x50, 0x50, 0x50, 0x51, 0x51, 0x51, 0x52, 0x52, 0x52, 0x53, 0x53, 0x53, 0x54, 0x54, 0x54, 0x55 @ 084c3718 50505051515152525253535354545455
    .byte  0x00                           @ 084c3728 00
    ROM_INCBIN 0x4c3729, 0x4f
    .byte  0x20, 0x20, 0x20, 0x21, 0x21, 0x22, 0x22, 0x22, 0x23, 0x23, 0x24, 0x24, 0x24, 0x25, 0x25, 0x26 @ 084c3778 20202021212222222323242424252526
    .byte  0x20, 0x20, 0x20, 0x21, 0x21, 0x22, 0x22, 0x22, 0x23, 0x23, 0x24, 0x24, 0x24, 0x25, 0x25, 0x26 @ 084c3788 20202021212222222323242424252526
    .byte  0x20, 0x20, 0x20, 0x21, 0x21, 0x22, 0x22, 0x22, 0x23, 0x23, 0x24, 0x24, 0x24, 0x25, 0x25, 0x26 @ 084c3798 20202021212222222323242424252526
    .byte  0x30, 0x30, 0x30, 0x31, 0x31, 0x32, 0x32, 0x32, 0x33, 0x33, 0x34, 0x34, 0x34, 0x35, 0x35, 0x36 @ 084c37a8 30303031313232323333343434353536
    .byte  0x30, 0x30, 0x30, 0x31, 0x31, 0x32, 0x32, 0x32, 0x33, 0x33, 0x34, 0x34, 0x34, 0x35, 0x35, 0x36 @ 084c37b8 30303031313232323333343434353536
    .byte  0x40, 0x40, 0x40, 0x41, 0x41, 0x42, 0x42, 0x42, 0x43, 0x43, 0x44, 0x44, 0x44, 0x45, 0x45, 0x46 @ 084c37c8 40404041414242424343444444454546
    .byte  0x40, 0x40, 0x40, 0x41, 0x41, 0x42, 0x42, 0x42, 0x43, 0x43, 0x44, 0x44, 0x44, 0x45, 0x45, 0x46 @ 084c37d8 40404041414242424343444444454546
    .byte  0x40, 0x40, 0x40, 0x41, 0x41, 0x42, 0x42, 0x42, 0x43, 0x43, 0x44, 0x44, 0x44, 0x45, 0x45, 0x46 @ 084c37e8 40404041414242424343444444454546
    .byte  0x50, 0x50, 0x50, 0x51, 0x51, 0x52, 0x52, 0x52, 0x53, 0x53, 0x54, 0x54, 0x54, 0x55, 0x55, 0x56 @ 084c37f8 50505051515252525353545454555556
    .byte  0x50, 0x50, 0x50, 0x51, 0x51, 0x52, 0x52, 0x52, 0x53, 0x53, 0x54, 0x54, 0x54, 0x55, 0x55, 0x56 @ 084c3808 50505051515252525353545454555556
    .byte  0x60, 0x60, 0x60, 0x61, 0x61, 0x62, 0x62, 0x62, 0x63, 0x63, 0x64, 0x64, 0x64, 0x65, 0x65, 0x66 @ 084c3818 60606061616262626363646464656566
    .byte  0x00                           @ 084c3828 00
    ROM_INCBIN 0x4c3829, 0x4f
    .byte  0x20, 0x20, 0x20, 0x21, 0x21, 0x22, 0x22, 0x23, 0x23, 0x24, 0x24, 0x25, 0x25, 0x26, 0x26, 0x27 @ 084c3878 20202021212222232324242525262627
    .byte  0x20, 0x20, 0x20, 0x21, 0x21, 0x22, 0x22, 0x23, 0x23, 0x24, 0x24, 0x25, 0x25, 0x26, 0x26, 0x27 @ 084c3888 20202021212222232324242525262627
    .byte  0x30, 0x30, 0x30, 0x31, 0x31, 0x32, 0x32, 0x33, 0x33, 0x34, 0x34, 0x35, 0x35, 0x36, 0x36, 0x37 @ 084c3898 30303031313232333334343535363637
    .byte  0x30, 0x30, 0x30, 0x31, 0x31, 0x32, 0x32, 0x33, 0x33, 0x34, 0x34, 0x35, 0x35, 0x36, 0x36, 0x37 @ 084c38a8 30303031313232333334343535363637
    .byte  0x40, 0x40, 0x40, 0x41, 0x41, 0x42, 0x42, 0x43, 0x43, 0x44, 0x44, 0x45, 0x45, 0x46, 0x46, 0x47 @ 084c38b8 40404041414242434344444545464647
    .byte  0x40, 0x40, 0x40, 0x41, 0x41, 0x42, 0x42, 0x43, 0x43, 0x44, 0x44, 0x45, 0x45, 0x46, 0x46, 0x47 @ 084c38c8 40404041414242434344444545464647
    .byte  0x50, 0x50, 0x50, 0x51, 0x51, 0x52, 0x52, 0x53, 0x53, 0x54, 0x54, 0x55, 0x55, 0x56, 0x56, 0x57 @ 084c38d8 50505051515252535354545555565657
    .byte  0x50, 0x50, 0x50, 0x51, 0x51, 0x52, 0x52, 0x53, 0x53, 0x54, 0x54, 0x55, 0x55, 0x56, 0x56, 0x57 @ 084c38e8 50505051515252535354545555565657
    .byte  0x60, 0x60, 0x60, 0x61, 0x61, 0x62, 0x62, 0x63, 0x63, 0x64, 0x64, 0x65, 0x65, 0x66, 0x66, 0x67 @ 084c38f8 60606061616262636364646565666667
    .byte  0x60, 0x60, 0x60, 0x61, 0x61, 0x62, 0x62, 0x63, 0x63, 0x64, 0x64, 0x65, 0x65, 0x66, 0x66, 0x67 @ 084c3908 60606061616262636364646565666667
    .byte  0x70, 0x70, 0x70, 0x71, 0x71, 0x72, 0x72, 0x73, 0x73, 0x74, 0x74, 0x75, 0x75, 0x76, 0x76, 0x77 @ 084c3918 70707071717272737374747575767677
    .byte  0x00                           @ 084c3928 00
    ROM_INCBIN 0x4c3929, 0x1107
    .word  0x0813080f                     @ 084c4a30 0f081308
    .word  0x081a0816                     @ 084c4a34 16081a08
    .word  0x0822081e                     @ 084c4a38 1e082208
    .word  0x08290825                     @ 084c4a3c 25082908
    .word  0x0831082d                     @ 084c4a40 2d083108
    .word  0x08380834                     @ 084c4a44 34083808
    .word  0x0840083c                     @ 084c4a48 3c084008
    .word  0x08470844                     @ 084c4a4c 44084708
    .word  0x084f084b                     @ 084c4a50 4b084f08
    .word  0x08570853                     @ 084c4a54 53085708
    .word  0x085f085b                     @ 084c4a58 5b085f08
    .word  0x08660862                     @ 084c4a5c 62086608
    .word  0x086e086a                     @ 084c4a60 6a086e08
    .word  0x08760872                     @ 084c4a64 72087608
    .word  0x087e087a                     @ 084c4a68 7a087e08
    .word  0x08860882                     @ 084c4a6c 82088608
    .word  0x088d088a                     @ 084c4a70 8a088d08
    .word  0x08950891                     @ 084c4a74 91089508
    .word  0x089d0899                     @ 084c4a78 99089d08
    .word  0x08a508a1                     @ 084c4a7c a108a508
    .word  0x08ad08a9                     @ 084c4a80 a908ad08
    .word  0x08b508b1                     @ 084c4a84 b108b508
    .word  0x08bd08b9                     @ 084c4a88 b908bd08
    .word  0x08c508c1                     @ 084c4a8c c108c508
    .word  0x08ce08ca                     @ 084c4a90 ca08ce08
    .word  0x08d608d2                     @ 084c4a94 d208d608
    .word  0x08de08da                     @ 084c4a98 da08de08
    .word  0x08e608e2                     @ 084c4a9c e208e608
    .word  0x08ee08ea                     @ 084c4aa0 ea08ee08
    .word  0x08f708f3                     @ 084c4aa4 f308f708
    .word  0x08ff08fb                     @ 084c4aa8 fb08ff08
    .word  0x09070903                     @ 084c4aac 03090709
    .word  0x0910090b                     @ 084c4ab0 0b091009
    .word  0x09180914                     @ 084c4ab4 14091809
    .word  0x0920091c                     @ 084c4ab8 1c092009
    .word  0x09290925                     @ 084c4abc 25092909
    .word  0x0931092d                     @ 084c4ac0 2d093109
    .word  0x093a0936                     @ 084c4ac4 36093a09
    .word  0x0942093e                     @ 084c4ac8 3e094209
    .word  0x094b0947                     @ 084c4acc 47094b09
    .word  0x0954094f                     @ 084c4ad0 4f095409
    .word  0x095c0958                     @ 084c4ad4 58095c09
    .word  0x09650961                     @ 084c4ad8 61096509
    .word  0x096e0969                     @ 084c4adc 69096e09
    .word  0x09760972                     @ 084c4ae0 72097609
    .word  0x097f097b                     @ 084c4ae4 7b097f09
    .word  0x09880983                     @ 084c4ae8 83098809
    .word  0x0991098c                     @ 084c4aec 8c099109
    .word  0x099a0995                     @ 084c4af0 95099a09
    .word  0x09a2099e                     @ 084c4af4 9e09a209
    .word  0x09ab09a7                     @ 084c4af8 a709ab09
    .word  0x09b409b0                     @ 084c4afc b009b409
    .word  0x09bd09b9                     @ 084c4b00 b909bd09
    .word  0x09c609c2                     @ 084c4b04 c209c609
    .word  0x09cf09cb                     @ 084c4b08 cb09cf09
    .word  0x09d809d4                     @ 084c4b0c d409d809
    .word  0x09e209dd                     @ 084c4b10 dd09e209
    .word  0x09eb09e6                     @ 084c4b14 e609eb09
    .word  0x09f409ef                     @ 084c4b18 ef09f409
    .word  0x09fd09f9                     @ 084c4b1c f909fd09
    ROM_INCBIN 0x4c4b20, 0x208
DWORD_084c4d28:
    .word  0x10071000                     @ 084c4d28 00100710
    ROM_INCBIN 0x4c4d2c, 0xbfc
DWORD_084c5928:
    .word  0x802f802c                     @ 084c5928 2c802f80
    ROM_INCBIN 0x4c592c, 0x1a3c
DWORD_084c7368:
    .word  0x00640000                     @ 084c7368 00006400
    ROM_INCBIN 0x4c736c, 0x1fc
DAT_084c7568:
    .hword 0x1000                         @ 084c7568 0010
    .byte  0xd1, 0x0d, 0x00, 0x0c, 0x2e, 0x0a, 0x00, 0x08
DAT_084c7572:
    .hword 0x0007                         @ 084c7572 0700
    ROM_INCBIN 0x4c7574, 0xb0
DWORD_084c7624:
    .word  0xffffffff                     @ 084c7624 ffffffff
    .byte  0x02, 0x04, 0x06, 0x08, 0xff, 0xff, 0xff, 0xff, 0x02, 0x04, 0x06, 0x08
DAT_084c7634:
    .word  0x0000fce2                     @ 084c7634 e2fc0000

/* End */
