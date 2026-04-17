# Yu-Gi-Oh! Ultimate Masters: World Championship Tournament 2006 — ROM map

> 来源: https://datacrystal.tcrf.net/wiki/Yu-Gi-Oh!_Ultimate_Masters:_World_Championship_Tournament_2006/ROM_map
> 抓取日期: 2026-04-17

The following article is a ROM map for Yu-Gi-Oh! Ultimate Masters: World Championship Tournament 2006.

## 目录

1. Banlist Password
   - 1.1 Enter character
2. 0x2387C
3. Retrieve CPU opponent's data
4. Check if internal_card_id is valid, and convert it to card_id
5. Checks which charset to use (Japanese or International), then branch depending on lookup table using card_id
6. Load pointer_to_card_name
7. Retrieve card_id from internal_card_id, retrieve EWRAM 02006C2C and call 080EE7AC
8. Cards IDs array
9. Card name pointers
10. Cards names

---

## Banlist Password

### Enter character

```
080143F0 B570     push    r4-r6,r14
080143F2 1C04     mov     r4,r0
080143F4 1C0B     mov     r3,r1
080143F6 1C16     mov     r6,r2
080143F8 490D     ldr     r1,=2000000h
080143FA 480E     ldr     r0,=6C2Ch
080143FC 1809     add     r1,r1,r0
080143FE 2007     mov     r0,7h
08014400 7809     ldrb    r1,[r1]
08014402 4008     and     r0,r1
08014404 2800     cmp     r0,0h
08014406 D003     beq     8014410h
08014408 480B     ldr     r0,=202348Ch
0801440A 7800     ldrb    r0,[r0]
0801440C 2800     cmp     r0,0h
0801440E D023     beq     8014458h
08014410 7821     ldrb    r1,[r4]
08014412 2900     cmp     r1,0h
08014414 D025     beq     8014462h
08014416 2A00     cmp     r2,0h
08014418 D023     beq     8014462h
0801441A 2580     mov     r5,80h
0801441C 1C28     mov     r0,r5
0801441E 4008     and     r0,r1
08014420 2800     cmp     r0,0h
08014422 D00B     beq     801443Ch
08014424 7019     strb    r1,[r3]                  ;Store charset
08014426 3401     add     r4,1h
08014428 3301     add     r3,1h
0801442A 7820     ldrb    r0,[r4]                  ;Load character_id in r0
0801442C 7018     strb    r0,[r3]                  ;Store character_id
0801442E E006     b       801443Eh
```

---

## 0x2387C

```
0802387C B5F0     push    r4-r7,r14
0802387E 4657     mov     r7,r10
08023880 464E     mov     r6,r9
08023882 4645     mov     r5,r8
08023884 B4E0     push    r5-r7
08023886 1C1F     mov     r7,r3
08023888 9C08     ldr     r4,[sp,20h]
0802388A 0400     lsl     r0,r0,10h
0802388C 0C00     lsr     r0,r0,10h
0802388E 4681     mov     r9,r0
08023890 0409     lsl     r1,r1,10h
08023892 0412     lsl     r2,r2,10h
08023894 0C12     lsr     r2,r2,10h
08023896 4692     mov     r10,r2
08023898 0208     lsl     r0,r1,8h
0802389A 0E06     lsr     r6,r0,18h
0802389C 0E09     lsr     r1,r1,18h
0802389E 4688     mov     r8,r1
080238A0 1C38     mov     r0,r7
080238A2 F0D1FE1D bl      80F54E0h
080238A6 00B2     lsl     r2,r6,2h
080238A8 0041     lsl     r1,r0,1h
080238AA 1809     add     r1,r1,r0
080238AC 1A55     sub     r5,r2,r1
080238AE 1C30     mov     r0,r6
080238B0 4641     mov     r1,r8
080238B2 F0CDF97F bl      80F0BB4h
080238B6 2C00     cmp     r4,0h
080238B8 D108     bne     80238CCh
080238BA 4903     ldr     r1,=2006ED0h
080238BC 2002     mov     r0,2h
080238BE 4240     neg     r0,r0
080238C0 7A0A     ldrb    r2,[r1,8h]
080238C2 4010     and     r0,r2
080238C4 E006     b       80238D4h
```

---

## Retrieve CPU opponent's data

```
080242C8 485B     ldr     r0,=9E58D0Ch        ;r0 = deck_id_and_data_array
080242CA 0DA1     lsr     r1,r4,16h
080242CC 1809     add     r1,r1,r0            ;r1 = deck_id_and_data_array + (opponent_id << 16)
080242CE 8848     ldrh    r0,[r1,2h]          ;r0 = internal_card_id
080242D0 F0CAFC94 bl      80EEBFCh            ;call general routine to retrieve pointer_to_card_name
080242D4 1C03     mov     r3,r0
080242D6 2187     mov     r1,87h
080242D8 0089     lsl     r1,r1,2h
080242DA 9600     str     r6,[sp]
080242DC 20C0     mov     r0,0C0h
080242DE 2201     mov     r2,1h
080242E0 F7FFFACC bl      802387Ch            ;call 0802387C
080242E4 4A55     ldr     r2,=2023360h
080242E6 2002     mov     r0,2h
080242E8 7A13     ldrb    r3,[r2,8h]
080242EA 4318     orr     r0,r3
080242EC 2178     mov     r1,78h
080242EE 4308     orr     r0,r1
080242F0 7210     strb    r0,[r2,8h]          ;called by 080241EC, if r0 ≠ 0. Store r0 in [r2+8]
080242F2 4D52     ldr     r5,=2023360h        ;called by 080241EE. r5 = 0x2023360
080242F4 792C     ldrb    r4,[r5,4h]
080242F6 0961     lsr     r1,r4,5h
080242F8 78EF     ldrb    r7,[r5,3h]
080242FA 06F8     lsl     r0,r7,1Bh
080242FC 0F40     lsr     r0,r0,1Dh
080242FE 3802     sub     r0,2h
08024300 4281     cmp     r1,r0
08024302 DA15     bge     8024330h
08024304 484E     ldr     r0,=830070h
08024306 2180     mov     r1,80h
08024308 01C9     lsl     r1,r1,7h
0802430A 4C4E     ldr     r4,=9E59CE8h
0802430C 4A4E     ldr     r2,=3000040h
0802430E 2383     mov     r3,83h
08024310 009B     lsl     r3,r3,2h
08024312 18D2     add     r2,r2,r3
08024314 8812     ldrh    r2,[r2]
08024316 0892     lsr     r2,r2,2h
08024318 2307     mov     r3,7h
0802431A 401A     and     r2,r3
0802431C 0052     lsl     r2,r2,1h
0802431E 1912     add     r2,r2,r4
08024320 8812     ldrh    r2,[r2]
08024322 2487     mov     r4,87h
08024324 00E4     lsl     r4,r4,3h
08024326 1912     add     r2,r2,r4
08024328 0412     lsl     r2,r2,10h
0802432A 0C12     lsr     r2,r2,10h
0802432C F0D1FF1E bl      80F616Ch
08024330 20E0     mov     r0,0E0h
08024332 792F     ldrb    r7,[r5,4h]
08024334 4038     and     r0,r7
08024336 2800     cmp     r0,0h
08024338 D01B     beq     8024372h
0802433A 68A8     ldr     r0,[r5,8h]
0802433C 21FF     mov     r1,0FFh
0802433E 03C9     lsl     r1,r1,0Fh
08024340 4008     and     r0,r1
08024342 2800     cmp     r0,0h
08024344 D11B     bne     802437Eh
08024346 4841     ldr     r0,=210070h
08024348 2180     mov     r1,80h
0802434A 01C9     lsl     r1,r1,7h
0802434C 4C3D     ldr     r4,=9E59CE8h
0802434E 4A3E     ldr     r2,=3000040h
08024350 2383     mov     r3,83h
08024352 009B     lsl     r3,r3,2h
08024354 18D2     add     r2,r2,r3
08024356 8812     ldrh    r2,[r2]
08024358 0892     lsr     r2,r2,2h
0802435A 2307     mov     r3,7h
0802435C 401A     and     r2,r3
0802435E 0052     lsl     r2,r2,1h
08024360 1912     add     r2,r2,r4
08024362 8812     ldrh    r2,[r2]
08024364 2483     mov     r4,83h
08024366 00E4     lsl     r4,r4,3h
08024368 1912     add     r2,r2,r4
0802436A 0412     lsl     r2,r2,10h
0802436C 0C12     lsr     r2,r2,10h
0802436E F0D1FEFD bl      80F616Ch
08024372 68A8     ldr     r0,[r5,8h]
08024374 21FF     mov     r1,0FFh
08024376 03C9     lsl     r1,r1,0Fh
08024378 4008     and     r0,r1
0802437A 2800     cmp     r0,0h
0802437C D02C     beq     80243D8h
0802437E 492F     ldr     r1,=2023360h
08024380 898D     ldrh    r5,[r1,0Ch]
08024382 046C     lsl     r4,r5,11h
08024384 0E24     lsr     r4,r4,18h
08024386 7ACF     ldrb    r7,[r1,0Bh]
08024388 09FA     lsr     r2,r7,7h
0802438A 207F     mov     r0,7Fh
0802438C 7B09     ldrb    r1,[r1,0Ch]
0802438E 4008     and     r0,r1
08024390 0040     lsl     r0,r0,1h
08024392 4310     orr     r0,r2
08024394 1A24     sub     r4,r4,r0
08024396 0124     lsl     r4,r4,4h
08024398 1C25     mov     r5,r4
0802439A 3520     add     r5,20h
0802439C 042D     lsl     r5,r5,10h
0802439E 2020     mov     r0,20h
080243A0 4328     orr     r0,r5
080243A2 4A2B     ldr     r2,=814h
080243A4 2140     mov     r1,40h
080243A6 F0D1FEE1 bl      80F616Ch
080243AA 1C2E     mov     r6,r5
080243AC 1C27     mov     r7,r4
080243AE 2430     mov     r4,30h
080243B0 2508     mov     r5,8h
080243B2 1C20     mov     r0,r4
080243B4 4330     orr     r0,r6
080243B6 2140     mov     r1,40h
080243B8 4A26     ldr     r2,=815h
080243BA F0D1FED7 bl      80F616Ch
080243BE 3410     add     r4,10h
080243C0 3D01     sub     r5,1h
080243C2 2D00     cmp     r5,0h
080243C4 DAF5     bge     80243B2h
080243C6 1C38     mov     r0,r7
080243C8 3020     add     r0,20h
080243CA 0400     lsl     r0,r0,10h
080243CC 21C0     mov     r1,0C0h
080243CE 4308     orr     r0,r1
080243D0 4A21     ldr     r2,=816h
080243D2 2140     mov     r1,40h
080243D4 F0D1FECA bl      80F616Ch
080243D8 4E18     ldr     r6,=2023360h
080243DA 6870     ldr     r0,[r6,4h]
080243DC 491F     ldr     r1,=0FFFF0F00h
080243DE 4008     and     r0,r1
080243E0 2800     cmp     r0,0h
080243E2 D000     beq     80243E6h
080243E4 E0E1     b       80245AAh
```

---

## Check if internal_card_id is valid, and convert it to card_id

```
080EE76C 0400     lsl     r0,r0,10h              ;start of the function
080EE76E 0C02     lsr     r2,r0,10h
080EE770 1C11     mov     r1,r2
080EE772 4808     ldr     r0,=0FA6h
080EE774 4282     cmp     r2,r0
080EE776 D917     bls     80EE7A8h               ;if (r2 ≤ 4006), branch to 080EE7A8
080EE778 4807     ldr     r0,=1BA6h
080EE77A 4282     cmp     r2,r0
080EE77C D814     bhi     80EE7A8h               ;if (r2 ≤ 7078), branch to 080EE7A8
080EE77E 4807     ldr     r0,=95B7CCCh           ;r0 = pointer_to_cards_ids_array
080EE780 4A07     ldr     r2,=0FFFFF059h
080EE782 1889     add     r1,r1,r2               ;r1 -= 0xFA7 [4007; Blue-Eyes White Dragon]
080EE784 0049     lsl     r1,r1,1h               ;r1 << 1
080EE786 1809     add     r1,r1,r0               ;r1 = pointer_to_cards_ids_array + ((internal_card_id - 4007) << 1)
080EE788 8809     ldrh    r1,[r1]                ;r1 = card_id
080EE78A 4806     ldr     r0,=0FFFFh
080EE78C 4281     cmp     r1,r0
080EE78E D00B     beq     80EE7A8h               ;if (invalid_card_id), branch to 080EE7A8
080EE790 1C08     mov     r0,r1                 ;r0 = card_id
080EE792 E00A     b       80EE7AAh               ;branch to 080EE7AA
080EE794 0FA6     lsr     r6,r4,1Eh
080EE796 0000     lsl     r0,r0,0h
080EE798 1BA6     sub     r6,r4,r6
080EE79A 0000     lsl     r0,r0,0h
080EE79C 7CCC     ldrb    r4,[r1,13h]
080EE79E 095B     lsr     r3,r3,5h
080EE7A0 F059FFFF bl      81487A2h
080EE7A4 FFFF     bl      lr+0FFEh
080EE7A6 0000     lsl     r0,r0,0h
080EE7A8 2000     mov     r0,0h                 ;if (not an internal_card_id), r0 = 0
080EE7AA 4770     bx      r14                   ;go back right after the function call (0xEEC07 in the case of displaying CPU opponents' names)
```

---

## Checks which charset to use (Japanese or International), then branch depending on a look-up table using card_id

```
080EE7AC 1C02     mov     r2,r0                 ;r2 = card_id
080EE7AE 1C0B     mov     r3,r1                 ;r3 = [0x2006C2C] & 7; language_id
080EE7B0 480B     ldr     r0,=80000AEh
080EE7B2 8800     ldrh    r0,[r0]               ;r0 = second_part_of_game_code
080EE7B4 0A00     lsr     r0,r0,8h
080EE7B6 284A     cmp     r0,4Ah
080EE7B8 D100     bne     80EE7BCh              ;if the game is not Japanese, branch to 080EE7BC
080EE7BA E0D5     b       80EE968h              ;else branch to 080EE968
080EE7BC 2B00     cmp     r3,0h                 ;if the game is not Japanese
080EE7BE D000     beq     80EE7C2h              ;if (language_id == JAPANESE), branch to 080EE7C2
080EE7C0 E0D2     b       80EE968h              ;else branch to 080EE968
080EE7C2 4908     ldr     r1,=98169B8h          ;r1 = 0x98169B8
080EE7C4 2016     mov     r0,16h
080EE7C6 4350     mul     r0,r2
080EE7C8 1840     add     r0,r0,r1              ;r0 = 0x98169B8 + (card_id × 22)
080EE7CA 8801     ldrh    r1,[r0]               ;r1 = [0x98169B8 + (card_id × 22)]
080EE7CC 4806     ldr     r0,=1498h
080EE7CE 4281     cmp     r1,r0
080EE7D0 D044     beq     80EE85Ch              ;if ((0x98169B8 + (card_id × 22)) == 0x1498), branch to 080EE85C
080EE7D2 4281     cmp     r1,r0
080EE7D4 DC0A     bgt     80EE7ECh              ;else if ((0x98169B8 + (card_id × 22)) > 0x1498), branch to 080EE7EC
080EE7D6 3801     sub     r0,1h
080EE7D8 4281     cmp     r1,r0
080EE7DA D011     beq     80EE800h              ;if ((0x98169B8 + (card_id × 22))) == 0x1497), branch to 080EE800
080EE7DC E0C4     b       80EE968h              ;else branch to 080EE968
080EE7DE 0000     lsl     r0,r0,0h
080EE7E0 00AE     lsl     r6,r5,2h
080EE7E2 0800     lsr     r0,r0,20h
080EE7E4 69B8     ldr     r0,[r7,18h]
080EE7E6 0981     lsr     r1,r0,6h
080EE7E8 1498     asr     r0,r3,12h
080EE7EA 0000     lsl     r0,r0,0h
080EE7EC 4803     ldr     r0,=1499h
080EE7EE 4281     cmp     r1,r0
080EE7F0 D062     beq     80EE8B8h              ;if ((0x98169B8 + (card_id × 22)) == 0x1499), branch to 080EE8B8
080EE7F2 3001     add     r0,1h
080EE7F4 4281     cmp     r1,r0
080EE7F6 D100     bne     80EE7FAh              ;else if ((0x98169B8 + (card_id × 22)) ≠ 0x149A), branch to 080EE7FA (branch to 080EE968)
080EE7F8 E08A     b       80EE910h              ;else branch to 080EE910
080EE7FA E0B5     b       80EE968h              ;branch to 080EE968
```

---

## Load pointer_to_card_name

```
080EE968 4905     ldr     r1,=95F3A5Ch          ;r1 = 0x95F3A5C
080EE96A 0050     lsl     r0,r2,1h
080EE96C 1880     add     r0,r0,r2
080EE96E 0040     lsl     r0,r0,1h
080EE970 18C0     add     r0,r0,r3              ;r0 += [0x2006C2C] & 7; language_id
080EE972 0080     lsl     r0,r0,2h
080EE974 1840     add     r0,r0,r1
080EE976 6800     ldr     r0,[r0]               ;r0 = [0x95F3A5C + ((card_id × 6 + (language_id)) << 2)]
080EE978 4902     ldr     r1,=95BB594h          ;r1 = 0x95BB594
080EE97A 1840     add     r0,r0,r1              ;r0 = 0x95BB594 + pointer_to_card_name_pointer
080EE97C 4770     bx      r14                   ;return
```

---

## Retrieve card_id from an internal_card_id, retrieve EWRAM 02006C2C and call 080EE7AC

```
080EEBF2 0000     lsl     r0,r0,0h
080EEBF4 A508     add     r5,=80EEC18h
080EEBF6 0980     lsr     r0,r0,6h
080EEBF8 FF0C     bl      lr+0E18h
080EEBFA 095F     lsr     r7,r3,5h
080EEBFC B500     push    r14
080EEBFE 0400     lsl     r0,r0,10h
080EEC00 0C00     lsr     r0,r0,10h
080EEC02 F7FFFDB3 bl      80EE76Ch              ;call Check if internal_card_id is valid, and convert it to card_id
080EEC06 0400     lsl     r0,r0,10h
080EEC08 0C00     lsr     r0,r0,10h             ;r0 = card_id
080EEC0A 4905     ldr     r1,=2000000h
080EEC0C 4A05     ldr     r2,=6C2Ch
080EEC0E 1889     add     r1,r1,r2              ;r1 = 0x2006C2C
080EEC10 7809     ldrb    r1,[r1]               ;r1 = [0x2006C2C]
080EEC12 0749     lsl     r1,r1,1Dh
080EEC14 0F49     lsr     r1,r1,1Dh             ;r1 &= 7
080EEC16 F7FFFDC9 bl      80EE7ACh              ;call 080EE7AC
080EEC1A BC02     pop     r1
080EEC1C 4708     bx      r1                    ;branch to r1
```

---

## Cards IDs array

- `0x157BCCC` to `0x15B917B` — Conversion table from `internal_card_id` to `card_id`

## Card name pointers

- `0x15F3A5C`

## Cards names

- `0x15BB594`
