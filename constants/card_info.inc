@ =============================================================================
@ Card Info Page constants (card_info_page_init_bg0 / draw_card_*_label_to_vram)
@ Source: asm/01_vija_scene_text.s, Seg-2 (0x0801d448..0x0801d998)
@ Seg-3 additions: card_image_decode_wrapper / render_card_name_to_desc_page_vram /
@   card_info_page_finalize / blit_glyph_2x2_to_bg_vram / tick_blend_fadein_and_poll_done
@ =============================================================================

@ BG Layer Control Register initial values (written to BG1CNT/BG2CNT/BG3CNT)
.equ CARD_INFO_BG1CNT_INIT, 0x00004104  @ BG1CNT: pri=0 charbase=1 16col scrbase=0x10 32x32
.equ CARD_INFO_BG2CNT_INIT, 0x00000407  @ BG2CNT: pri=3 charbase=1 16col scrbase=0 32x32
.equ CARD_INFO_BG3CNT_INIT, 0x00000305  @ BG3CNT: pri=1 charbase=0 16col scrbase=0 32x32

@ OBJ Palette slot for card info frame (OBJ_PALRAM_BASE + 0x1e0 = pal 15 color 0)
.equ CARD_INFO_OBJ_PAL_SLOT, 0x050003e0  @ OBJ palette slot for card name/stat frame tiles

@ BG VRAM write bases for card info text (all < 0x06010000 = BG VRAM, not OBJ tile VRAM)
.equ CARD_INFO_NAME_BG_TILE_VRAM, 0x06001840  @ BG screen-map tile-attr write base for card name line (CB0, SB3+0x040)
.equ CARD_INFO_NAME_SPRITE_VRAM,  0x06008200  @ commit_line_buffer_to_sprite_vram target for card name
.equ CARD_INFO_STAT_BG_TILE_VRAM, 0x06001c00  @ BG screen-map tile-attr write base for ATK/DEF/Level lines (CB0, SB3+0x400)
.equ CARD_INFO_STAT_SPRITE_VRAM,  0x06008580  @ commit_line_buffer_to_sprite_vram target for ATK/DEF/Level

@ --- Seg-3 additions (card_image_decode_wrapper + render_card_name_to_desc_page_vram + card_info_page_finalize) ---

@ Card image tile pack parameters (card_image_decode_wrapper)
.equ CARD_TILE_PACK_GLYPH_OFF_A,   0x0985004c  @ card_glyph_table_3+0xa80 (tile src A, normal card map)
.equ CARD_TILE_PACK_GLYPH_OFF_B,   0x09850934  @ card_glyph_table_3+0x1368 (tile src B)
.equ CARD_TILE_PACK_MAP_PARAM,     0x0000020e  @ load_pack_tile_and_map_to_vram map param (31 ROM refs)
.equ CARD_FRAME_TILE_SRC_MONSTER,  0x0984a3fc  @ seg-C blob: monster card frame tile pack source
.equ CARD_FRAME_TILE_SRC_SPELL,    0x0984b994  @ seg-C blob: spell card frame tile pack source (type23)
.equ CARD_FRAME_PAL_SRC_MONSTER_A, 0x0984dd6c  @ seg-C blob: monster frame OBJ palette A (32B)
.equ CARD_FRAME_TILE_SRC_MONSTER_A,0x0984d8ec  @ seg-C blob: monster frame OBJ tile data A (256B)
.equ CARD_FRAME_PAL_SRC_SPELL_A,   0x0984de6c  @ seg-C blob: spell frame OBJ palette A
.equ CARD_FRAME_TILE_SRC_SPELL_A,  0x0984dcec  @ seg-C blob: spell frame OBJ tile data A
.equ CARD_FRAME_PAL_SRC_STAR_A,    0x0984f52c  @ seg-C blob: star/level frame OBJ palette A
.equ CARD_FRAME_TILE_SRC_STAR,     0x0984dc6c  @ seg-C blob: star/level OBJ tile data
.equ CARD_FRAME_TILE_SRC_STAR_B,   0x0984f46c  @ seg-C blob: star/level OBJ tile data B
.equ CARD_FRAME_PAL_SRC_MONSTER_B, 0x0984de4c  @ seg-C blob: monster frame OBJ palette B
.equ CARD_FRAME_PAL_SRC_ICON_A,    0x0984ee2c  @ seg-C blob: icon frame OBJ palette A (type 0x17)
.equ CARD_FRAME_PAL_SRC_ICON_B,    0x0984f3ac  @ seg-C blob: icon frame OBJ palette B (type 0x16)
.equ CARD_FRAME_TILE_SRC_ICON,     0x0984f0ac  @ seg-C blob: icon frame OBJ tile data (type 0x16)
.equ CARD_FRAME_TILE_SRC_SPELL_B,  0x0984e42c  @ seg-C blob: spell frame OBJ tile data B (type 0x17)
.equ CARD_OVERLAY_TILE_SRC,        0x09ccd2d0  @ name_o region+0x40: card overlay nibble-sequence tile (5 refs)

@ Card frame PALRAM/VRAM destinations (card_image_decode_wrapper + card_info_page_finalize)
.equ CARD_FRAME_BG_PAL_BASE,    0x050000a0  @ BG PALRAM row 5 (card frame BG palette base)
.equ CARD_FRAME_OBJ_PAL_MONSTER,0x050003a0  @ OBJ PALRAM slot 13 (monster frame palette, PAL+0x1a0)
.equ CARD_FRAME_OBJ_PAL_SPELL,  0x050003c0  @ OBJ PALRAM slot 14 (spell/star frame palette, PAL+0x1c0)
.equ CARD_FRAME_OBJ_PAL_LEVEL,  0x05000380  @ OBJ PALRAM slot 12 (level/icon frame palette, PAL+0x180)
.equ CARD_FRAME_OBJ_TILE_BASE,  0x06017440  @ OBJ VRAM card frame tile base (OBJ+0x7440)
.equ CARD_LEVEL_OBJ_TILE_BASE,  0x060174c0  @ OBJ VRAM card level star tile base (OBJ+0x74c0)
.equ CARD_SPELL_OBJ_TILE_BASE,  0x06017500  @ OBJ VRAM spell card icon tile base (OBJ+0x7500)
.equ CARD_ICON_OBJ_TILE_BASE,   0x06017580  @ OBJ VRAM card icon/status tile base (OBJ+0x7580)
.equ CARD_FRAME_OBJ_TILE_SLOT1, 0x06010020  @ OBJ_TILE_VRAM_BASE+0x20 (tile slot 1 for card art overlay)
.equ CARD_DESC_OBJ_TILE_BASE,   0x06010040  @ OBJ_TILE_VRAM_BASE+0x40 (tile slot 2 for card desc text)

@ Card description page text VRAM (render_card_name_to_desc_page_vram + render_card_description_text)
.equ CARD_DESC_LINE_BUF_VRAM,   0x06007100  @ BG VRAM card description text line buffer
.equ CARD_DESC_BG_VRAM_A,       0x06000800  @ BG VRAM desc page tile region A (tile-seq write target A)
.equ CARD_DESC_BG_VRAM_B,       0x06000c80  @ BG VRAM desc page tile region B (tile-seq write target B)
.equ CARD_DESC_RENDER_PARAM,    0x00008008  @ render_glyph_jp layer param for card description

@ --- Seg-4 additions (draw_card_stat_digits_to_oam / draw_stat_row_sprites_to_oam) ---

@ OAM packed constants for card stat digit sprites (write_oam_entry_from_packed_args: r0=packed_xy, r1=tile_idx, r2=attr2)
@ packed_xy format: low16=x_coord (9-bit), high16=oam_y
.equ CARD_STAT_ATK_DEF_OAM_XY,    0x00060056  @ ATK/DEF frame OBJ position (x=86, y=6); 4 ROM refs
.equ CARD_STAT_ATK_DEF_OAM_ATTR2, 0x0000d3a2  @ ATK/DEF frame attr2: pal13, tile0x3a2; 2 ROM refs
.equ CARD_STAT_QPLAY_OAM_XY,      0x00150058  @ Quick-Play Spell secondary marker pos (x=88, y=21); 2 ROM refs
.equ CARD_STAT_QPLAY_OAM_ATTR2,   0x0000e3a6  @ Quick-Play marker attr2: pal14, tile0x3a6; 2 ROM refs
.equ CARD_STAT_DIGIT_OAM_ATTR2,   0x0000f001  @ ATK/DEF digit sprite attr2: pal15, tile1; 2 ROM refs
.equ CARD_STAT_FUSION_OAM_ATTR2,  0x0000c3a8  @ Fusion/extra-type marker attr2: pal12, tile0x3a8; 1 ROM ref

@ OAM attr2 base offsets for stat row sprites (draw_stat_row_sprites_to_oam)
@ Added to r5 (col_idx*0x10 + 2) then u16-truncated to produce attr2 per row
.equ CARD_STAT_ROW_ATTR2_BASE_A,  0xfffff800  @ stat row sprite group A attr2 base (row 0, Y=0x70)
.equ CARD_STAT_ROW_ATTR2_BASE_B,  0xfffff804  @ stat row sprite group B attr2 base (row 1, Y=0x90)
.equ CARD_STAT_ROW_ATTR2_BASE_C,  0xfffff808  @ stat row sprite group C attr2 base (row 2, Y=0xb0)
.equ CARD_STAT_ROW_ATTR2_BASE_D,  0xfffff80c  @ stat row sprite group D attr2 base (row 3, Y=0xd0)

@ --- Seg-8 additions: LP threshold constants for render_card_stats_to_line_buf ---

.equ CARD_STAT_LP_THRESHOLD,      0x00000bb8  @ 3000 LP threshold for card stat display branch; 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_999,  0x000003e7  @ 999 LP threshold branch; 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_1500, 0x000005dc  @ 1500 LP threshold (render_card_stats dispatch); 35 ROM refs
.equ CARD_STAT_LP_THRESHOLD_5730, 0x00001662  @ 5730 LP threshold branch; 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_57300,0x0000dfd4  @ 57300 LP threshold branch; 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_572488,0x0008be48 @ 572488 LP threshold (upper range); 1 ROM ref
.equ CARD_STAT_LP_THRESHOLD_20000,0x00004e20  @ 20000 LP threshold extended render path; 1 ROM ref

@ gCardInfoPageState.word0 bit-field masks (card_list_on_select_to_info_page)
@ word0 layout: bits[2:0]=flags, bits[16:3]=card_id (14-bit), bit17=active_flag
.equ CARD_INFO_STATE_CARD_ID_MASK,  0x00003fff  @ mask for card_id bits[13:0] before shift-3 into word0
.equ CARD_INFO_STATE_CARD_ID_CLEAR, 0xfffe0007  @ AND mask to clear card_id field bits[16:3], preserve [17]+[2:0]

@ =============================================================================
@ file 02 Seg-1 additions: text render / pack selection / opp card name offsets
@ =============================================================================

.equ GAME_STR_TEXT_BASE,            0x00000C1C  @ str_base_offset=0x0c1c; adds to game_str_id_offset; 15 ROM refs
.equ CARD_ID_BASE_NEG_ADJ,          0xFFFFD8EF  @ neg adj -0x2711 so card_id 0x2711 maps to 0; 5 ROM refs
.equ PACK_DECK_A_KEY,               0x00002711  @ deck A key for find_deck_record_index_by_key; 5 ROM refs
.equ OPP_CARD_NAME_STR_OFF_ES,      0x0003A90C  @ ES offset from game_str_ja_0326 base; 1 ROM ref
.equ OPP_CARD_NAME_STR_OFF_ES_NULL, 0x0003A90E  @ ES offset from game_str_ja_0327 base; 1 ROM ref

@ =============================================================================
@ file 02 Seg-5 additions: field spell type-B effect chain guard
@ =============================================================================
.equ FIELD_SPELL_B_EFFECT_ID, 0x00001407  @ effect chain guard value for field spell type-B placement check; 12 ROM refs

@ =============================================================================
@ file 02 Seg-6 additions: zone slot set_code / card_id mask
@ =============================================================================
.equ SLOT_CARD_SET_CODE_MASK, 0x00001fff  @ 13-bit mask for YGO set_code/card_id fields in zone slot arrays; 101 raw refs; 2 Seg-6 slots

@ =============================================================================
@ file 02 Seg-8 additions: field spell / monster zone card IDs
@ =============================================================================
.equ TOON_WORLD_CARD_ID,             0x000012be  @ Toon World field-magic card id; presence check via equip-zone scan; 9 raw refs
.equ GROUND_COLLAPSE_FIELD_CARD_ID,  0x00001432  @ Ground Collapse field spell card id (data.md line 900, passcode 90502999); placement-block check in check_slot_placement_blocked_by_field_effect; 18 raw refs
.equ OJAMA_KING_CARD_ID,             0x000017ee  @ Ojama King card id (data.md line 1639, passcode 90140980); monster-zone limit effect; placement-block check; 13 raw refs
.equ SPATIAL_COLLAPSE_CARD_ID,       0x000016df  @ Spatial Collapse field spell id; monster zone clamp in count_available_monster_slots; 16 raw refs

@ =============================================================================
@ file 02 Seg-9 additions: equip placement eligibility / lock IDs
@ =============================================================================
@ Zone slot card_id values > 5169 (max card stat entry index) are effect/token IDs
@ used by the equip chain and field effect systems, not regular card stats entries.
.equ EQUIP_LOCKDOWN_CID,        0x000013f2  @ equip lockdown: count_field_copies>0 blocks all equip placement; 4 slots
.equ EQUIP_ZONE_BLOCKER_CID,    0x000013eb  @ cross-player equip blocker effect node; find_effect_node absent -> no equip; 1 slot
.equ EQUIP_LOCK_A_CID,          0x000016a4  @ equip lock chain effect A; check_value_in_slot_chain; 1 slot
.equ EQUIP_LOCK_B_CID,          0x000012d1  @ equip lock chain effect B; check_value_in_slot_chain; 1 slot
.equ EQUIP_ELIG_EXCL_A,         0x000014f9  @ equip eligibility exclusion id A; BST in check_slot_equip_eligibility; 1 slot
.equ EQUIP_ELIG_EXCL_B,         0x00001836  @ equip eligibility exclusion id B; bit-flag check path; 1 slot
.equ EQUIP_ELIG_EXCL_C,         0x00001670  @ equip eligibility exclusion id C; 1 slot
.equ EQUIP_ELIG_EXCL_D,         0x000019ee  @ equip eligibility exclusion id D; bit18 path; 1 slot
.equ EQUIP_PAIR_EXCL_A,         0x000017e9  @ field7 equip-pair whitelist A; check_equip_cards_share_field7; 1 slot
.equ EQUIP_PAIR_EXCL_B,         0x00001521  @ field7 equip-pair whitelist B; 1 slot
.equ EQUIP_PAIR_EXCL_C,         0x00001798  @ field7 equip-pair whitelist C; 1 slot
.equ EQUIP_PAIR_RANGE_MAX,      0x00001874  @ field7 BST range boundary: IDs in [0x1873..0x1874] pass; 1 slot
.equ EQUIP_CHAIN_PAIR_CARD_MAX, 0x0000164f  @ max card_id for chain pairing path in count_equip_placements_with_chain_check; 1 slot

@ =============================================================================
@ file 02 Seg-10a additions: card slot IDs for activation eligibility checks
@ =============================================================================
.equ UMI_CARD_ID,                    0x000010f4  @ Umi field spell (pw=22702055); special-case in check_card_matches_active_effect_slot; 31 raw refs; 2 slots
.equ A_LEGENDARY_OCEAN_CARD_ID,      0x0000150b  @ A Legendary Ocean (pw=295517); proxy reference for Umi activation category; 18 raw refs; 1 slot
.equ SPELL_ZONE_TARGET_CARD_ID,      0x00001368  @ cross-player spell-zone effect node type ID; used in find_paired_zone_entry_for_card + check_card_targeted_by_spell_zone_effect; 11 raw refs; 2 slots
.equ TOTAL_DEFENSE_SHOGUN_CARD_ID,   0x000012b4  @ Total Defense Shogun (pw=75372290); special activation via slot[+0x10] bit5; 5 raw refs; 1 slot
.equ EHERO_RAMPART_BLASTER_CARD_ID,  0x00001956  @ Elemental Hero Rampart Blaster (pw=47737087); activation: inverted bit5 + zone count; 8 raw refs; 1 slot
.equ TWINHEADED_BEAST_CARD_ID,       0x00001723  @ Twinheaded Beast (pw=82035781); monster activation check; 4 raw refs; 1 slot
.equ TYRANT_DRAGON_CARD_ID,          0x000014d5  @ Tyrant Dragon (pw=94568601); monster activation check; 8 raw refs; 1 slot
.equ ARMED_SAMURAI_BEN_KEI_CARD_ID,  0x0000186c  @ Armed Samurai - Ben Kei (pw=84430950); monster activation check; 8 raw refs (1 Seg-10a slot)

@ =============================================================================
@ file 02 Seg-10b additions: fieldspell / activation eligibility card IDs
@ =============================================================================
.equ JINZO_7_CID,                0x0000114c  @ Jinzo #7; fieldspell eligibility BST; 12 raw refs
.equ MANGA_RYU_RAN_CID,          0x0000127d  @ Manga Ryu-Ran; fieldspell chain; 10 raw refs
.equ GEAR_GOLEM_CID,             0x00001295  @ Gear Golem the Moving Fortress; 9 raw refs
.equ BLUE_EYES_TOON_DRAGON_CID,  0x000012a5  @ Blue-Eyes Toon Dragon; activation elig; 10 raw refs
.equ RING_OF_MAGNETISM_CID,      0x00001318  @ Ring of Magnetism; activation elig; 22 raw refs
.equ JOWLS_OF_DARK_DEMISE_CID,   0x000013ab  @ Jowls of Dark Demise; fieldspell chain; 12 raw refs
.equ SERVANT_OF_CATABOLISM_CID,  0x000013b3  @ Servant of Catabolism; fieldspell BST; 5 raw refs
.equ LEGENDARY_FISHERMAN_CID,    0x000013cd  @ The Legendary Fisherman; chain check; 8 raw refs
.equ ZOMBYRA_THE_DARK_CID,       0x0000147d  @ Zombyra the Dark; fieldspell chain; 7 raw refs
.equ MARAUDING_CAPTAIN_CID,      0x000014c6  @ Marauding Captain; activation elig; 9 raw refs
.equ A_FEINT_PLAN_CID,           0x000014d4  @ A Feint Plan; activation elig; 7 raw refs
.equ ASURA_PRIEST_CID,           0x00001505  @ Asura Priest; activation elig BST; 32 raw refs
.equ TOON_DARK_MAGICIAN_GIRL_CID,0x0000154a  @ Toon Dark Magician Girl; 6 raw refs
.equ TOON_DEFENSE_CID,           0x00001561  @ Toon Defense; zone chain filter; 12 raw refs
.equ TOON_GOBLIN_AF_CID,         0x00001566  @ Toon Goblin Attack Force; fieldspell BST; 13 raw refs
.equ REAPER_ON_NIGHTMARE_CID,    0x00001598  @ Reaper on the Nightmare; fieldspell BST; 10 raw refs
.equ DRILLAGO_CID,               0x000015ba  @ Drillago; fieldspell BST; 9 raw refs
.equ KIRYU_CID,                  0x000015cf  @ Kiryu; fieldspell chain filter; 16 raw refs
.equ RAREGOLD_ARMOR_CID,         0x000015ea  @ Raregold Armor; activation elig; 6 raw refs
.equ DIFFUSION_WAVE_MOTION_CID,  0x000015ff  @ Diffusion Wave-Motion; activation/fieldspell elig BST; 23 raw refs
.equ AMAZONESS_TIGER_CID,        0x0000160f  @ Amazoness Tiger; activation elig BST; 10 raw refs
.equ MAGICAL_SCIENTIST_CID,      0x00001619  @ Magical Scientist; fieldspell chain; 83 raw refs
.equ BERSERK_DRAGON_CID,         0x00001644  @ Berserk Dragon; activation elig BST; 14 raw refs
.equ GUARDIAN_KAYEST_CID,        0x0000164e  @ Guardian Kay'est; activation/trap chain; 8 raw refs
.equ SHOOTING_STAR_BOW_CID,      0x0000165d  @ Shooting Star Bow - Ceal; fieldspell chain; 14 raw refs
.equ STAUNCH_DEFENDER_CID,       0x00001669  @ Staunch Defender; activation/fieldspell elig; 14 raw refs
.equ VILEPAWN_ARCHFIEND_CID,     0x0000168c  @ Vilepawn Archfiend; activation elig BST; 8 raw refs
.equ CHECKMATE_CID,              0x0000169b  @ Checkmate; fieldspell chain filter; 13 raw refs
.equ DARK_SCORPION_COMBO_CID,    0x000016a3  @ Dark Scorpion Combination; fieldspell chain; 14 raw refs
.equ MAGICIANS_VALKYRIE_CID,     0x000016ed  @ Magician's Valkyrie; activation elig BST; 8 raw refs
.equ BLACK_TYRANNO_CID,          0x00001701  @ Black Tyranno; fieldspell BST; 8 raw refs
.equ PRICKLE_FAIRY_CID,          0x00001703  @ Prickle Fairy; activation elig BST; 16 raw refs
.equ AMPHIBIOUS_BUGROTH_MK3_CID, 0x00001705  @ Amphibious Bugroth MK-3; fieldspell BST; 11 raw refs
.equ SOLAR_FLARE_DRAGON_CID,     0x00001756  @ Solar Flare Dragon; activation elig BST; 7 raw refs
.equ OPTI_CAMO_ARMOR_CID,        0x00001759  @ Opti-Camouflage Armor; fieldspell chain; 10 raw refs
.equ MARSHMALLON_CID,            0x00001770  @ Marshmallon; activation elig BST; 11 raw refs
.equ MARSHMALLON_GLASSES_CID,    0x00001777  @ Marshmallon glasses; activation elig; 25 raw refs
.equ EMISSARY_OF_OASIS_CID,      0x0000179d  @ Emissary of the Oasis; activation elig BST; 7 raw refs
.equ DELTA_ATTACKER_CID,         0x000017aa  @ Delta Attacker; fieldspell chain; 12 raw refs
.equ TAUNT_CID,                  0x000017fc  @ Taunt; activation/fieldspell elig BST; 8 raw refs
.equ ABSOLUTE_END_CID,           0x000017fd  @ Absolute End; activation/fieldspell zone chain; 7 raw refs
.equ RAGING_FLAME_SPRITE_CID,    0x0000182d  @ Raging Flame Sprite; fieldspell BST; 9 raw refs
.equ ASTRAL_BARRIER_CID,         0x00001852  @ Astral Barrier; activation/fieldspell elig; 14 raw refs
.equ SHADOWSLAYER_CID,           0x0000186d  @ Shadowslayer; fieldspell BST; 6 raw refs
.equ UNION_ATTACK_CID,           0x00001890  @ Union Attack; fieldspell chain; 14 raw refs
.equ OVERPOWERING_EYE_CID,       0x00001893  @ Overpowering Eye; fieldspell chain filter; 13 raw refs
.equ HIERACOSPHINX_CID,          0x000018b1  @ Hieracosphinx; activation elig BST; 12 raw refs
.equ GRAVE_OHJA_CID,             0x000018b6  @ Grave Ohja; activation elig; 7 raw refs
.equ EHERO_WILDEDGE_CID,         0x00001958  @ Elemental Hero Wildedge; activation elig BST (distinct from 0x1956=Rampart Blaster); 11 raw refs
.equ FEATHER_SHOT_CID,           0x0000195b  @ Feather Shot; fieldspell chain; 10 raw refs
.equ HAMON_LORD_CID,             0x000019a4  @ Hamon, Lord of Striking Thunder; 13 raw refs
.equ HAMON_LORD_CID_SHIFTED,     0xcd200000  @ HAMON_LORD_CID<<19; slot_word<<19 sentinel check; 6 raw refs

@ =============================================================================
@ file 03 Seg-1 additions: equip node link + slot eligibility card IDs
@ =============================================================================
.equ EHERO_AVIAN_CID,               0x000018a6  @ Elemental Hero Avian (pw=21844576); link_equip_node_by_card_type_check card_type_A; 12 raw refs; data.md Starter/Opp=0x18A6
.equ CHAIN_THRASHER_CID,            0x000019c1  @ Chain Thrasher (pw=88190453); link_equip_node_by_card_type_check card_type_B; 9 raw refs; data.md=0x19C1
.equ ROYAL_COMMAND_CID,             0x0000148e  @ Royal Command (pw=33950246); check_slot_equip_eligibility_by_type BST; 10 raw refs; data.md=0x148E
.equ FIEND_SKULL_DRAGON_CID,        0x000014da  @ Fiend Skull Dragon (pw=66235877); BST; 12 raw refs; data.md=0x14DA
.equ POSSESSED_DARK_SOUL_CID,       0x000014b8  @ Possessed Dark Soul (pw=52860176); BST; 8 raw refs; data.md=0x14B8
.equ SNATCH_STEAL_CID,              0x00001322  @ Snatch Steal (pw=45986603); BST; 20 raw refs; data.md=0x1322
.equ MAGIC_ARM_SHIELD_CID,          0x000012e2  @ Magic-Arm Shield (pw=96008713); BST; 9 raw refs; data.md=0x12E2
.equ CHANGE_OF_HEART_CID,           0x000012fc  @ Change of Heart (pw=04031928); BST; 8 raw refs; data.md=0x12FC
.equ MYSTIC_BOX_CID,                0x00001430  @ Mystic Box (pw=25774450); BST; 100 raw refs; data.md=0x1430
.equ DARK_NECROFEAR_CID,            0x00001466  @ Dark Necrofear (pw=31829185); BST (3 slots); 19 raw refs; data.md=0x1466
.equ BRAIN_JACKER_CID,              0x00001877  @ Brain Jacker (pw=40267580); BST; 10 raw refs; data.md=0x1877
.equ ENEMY_CONTROLLER_CID,          0x00001581  @ Enemy Controller (pw=98045062); BST; 10 raw refs; data.md=0x1581
.equ FALLING_DOWN_CID,              0x0000169a  @ Falling Down (pw=32919136); BST (2 slots); 15 raw refs; data.md=0x169A
.equ OWNER_SEAL_CID,                0x00001857  @ Owner's Seal (pw=09720537); BST; 5 raw refs; data.md=0x1857
.equ RESHEF_THE_DARK_BEING_CID,     0x000018c6  @ Reshef the Dark Being (pw=62420419); BST; 7 raw refs; data.md=0x18C6
.equ CHTHONIAN_POLYMER_CID,         0x0000195d  @ Chthonian Polymer (pw=72287557); BST; 7 raw refs; card-stats.s card_1963 slot=0x195D
.equ CHARMER_RANGE_MAX_CID,         0x000018c2  @ Wynn the Wind Charmer (pw=37744402); range_max of charmer block [0x18BF..0x18C2] (Aussa/Eria/Hiita/Wynn); 7 raw refs; card-stats.s card_1842
.equ ELEMENT_MAGICIAN_CID,          0x00001826  @ Element Magician (pw=65260293); check_slot_field_zone_card_eligible; 12 raw refs; data.md=0x1826
.equ CANNONBALL_SPEAR_SHELLFISH_CID,0x00001709  @ Cannonball Spear Shellfish (pw=95614612); check_slot_card_effect_eligibility whitelist; 7 raw refs; data.md=0x1709
.equ DEEPSEA_WARRIOR_CID,           0x000012a8  @ Deepsea Warrior (pw=24128274); check_slot_card_effect_eligibility whitelist; 9 raw refs; card-stats.s card_0632 slot=0x12A8
.equ HORUS_LV6_CID,                 0x000017d3  @ Horus the Black Flame Dragon LV6 (pw=11224103); check_slot_card_effect_eligibility; 9 raw refs; data.md=0x17D3
.equ HORUS_LV8_CID,                 0x000017d4  @ Horus the Black Flame Dragon LV8 (pw=48229808); check_zone_slot_equip_prerequisites range; 12 raw refs; data.md=0x17D4
.equ HORUS_SERVANT_CID,             0x000017dc  @ Horus' Servant (pw=09264485); check_zone_slot_equip_prerequisites; 6 raw refs; data.md=0x17DC
.equ SILENT_SWORDSMAN_LV5_CID,      0x00001814  @ Silent Swordsman LV5 (pw=74388798); check_slot_card_effect_eligibility whitelist; 22 raw refs; data.md=0x1814
.equ METALLIZING_PARASITE_CID,      0x00001693  @ Metallizing Parasite - Lunatite (pw=07369217); count_slot_equip_list_matches ref; 9 raw refs; data.md=0x1693
.equ NON_SPELLCASTING_AREA_CID,     0x00001667  @ Non-Spellcasting Area (pw=20065549); count_field_copies_of_card param; 4 raw refs; data.md=0x1667
.equ DUST_BARRIER_CID,              0x000017a1  @ Dust Barrier (pw=31476755); count_available_effect_zones param; 8 raw refs; data.md=0x17A1
.equ EHERO_WILDHEART_CID,           0x0000194e  @ Elemental Hero Wildheart (pw=86188410); check_slot_card_fieldspell_eligibility; 9 raw refs; data.md=0x194E
.equ LORD_OF_D_CID,                 0x0000128b  @ Lord of D. (pw=17985575); check_zone_slot_equip_prerequisites; 6 raw refs; data.md=0x128B
.equ KING_DRAGUN_CID,               0x00001879  @ King Dragun (pw=13756293); check_zone_slot_equip_prerequisites; 11 raw refs; data.md=0x1879
.equ HEART_OF_CLEAR_WATER_CID,      0x0000150a  @ Heart of Clear Water (pw=64801562); query_zone_chain_count_with_eligibility param; 22 raw refs; data.md=0x150A
.equ TIMIDITY_CID,                  0x0000153c  @ Timidity (pw=40350910); check_slot_card_eligible_for_special_action; 8 raw refs; data.md=0x153C
.equ EXODIA_NECROSS_CID,            0x00001645  @ Exodia Necross (pw=12600382); check_card_equip_eligible_for_slot TYPE_B; 21 raw refs; data.md=0x1645
.equ EQUIP_TYPE_A_CID,              0x0000150c  @ Fusion Sword Murasame Blade (pw=37684215); check_card_equip_eligible_for_slot TYPE_A; 14 raw refs; data.md=0x150C
.equ DARK_MAGICIAN_OF_CHAOS_CID,    0x000016f8  @ Dark Magician of Chaos (pw=40737112); check_slot_card_special_activation_eligible; 17 raw refs; data.md=0x16F8

@ =============================================================================
@ file 03 Seg-2 additions: special action eligibility card IDs
@ =============================================================================
.equ GAP_CID_13EA,              0x000013ea  @ gap slot (not in card-stats.s; range [0x13E8..0x13EB]: Nuvia the Wicked/Soul Exchange); check_slot_card_eligible_for_special_action
.equ KUNAI_WITH_CHAIN_CID,      0x00001231  @ Kunai with Chain (pw=37390589; card_0533 slot=0x1231); check_slot_card_eligible_for_special_action; note: Metalmorph(0x1238=+7) computed inline
.equ BLAST_WITH_CHAIN_CID,      0x00001514  @ Blast with Chain (pw=98239899; card_1086 slot=0x1514); check_slot_card_eligible_for_special_action; note: Hero_Heyro(0x1980=0xcc<<5) computed inline

@ =============================================================================
@ file 03 Seg-3 additions: equip eligibility / field array card IDs
@ =============================================================================
.equ GRADIUS_OPTION_CID,         0x000014fc  @ Gradius' Option (pw=14291024; card-stats.s card_1063 slot=0x14FC); check_zone_slot_equip_eligible special: count_paired_slots_with_field5_default(player,GRADIUS_CID); 8 raw refs; 2 Seg-3 slots
.equ GRADIUS_CID,                0x00001414  @ Gradius (pw=10992251; card-stats.s card_0895 slot=0x1414); paired with GRADIUS_OPTION_CID in check_zone_slot_equip_eligible count_paired path; 6 raw refs; 2 Seg-3 slots
.equ ULTIMATE_OFFERING_CID,      0x000012f3  @ Ultimate Offering (pw=80604091; card-stats.s card_0678 slot=0x12F3); check_value_in_slot_chain guard in check_zone_slot_equip_eligible; 6 raw refs; 2 Seg-3 slots
.equ XYZ_DRAGON_CANNON_CID,      0x000015b4  @ XYZ-Dragon Cannon (pw=91998119; card-stats.s card_1203 slot=0x15B4); range_base in equip-eligible blacklist; 4 raw refs; 1 Seg-3 slot
.equ HELPOEMER_CID,              0x00001571  @ Helpoemer (pw=76052811; card-stats.s card_1148 slot=0x1571); blacklist single-ID in check_zone_slot_equip_eligible; 4 raw refs; 1 Seg-3 slot
.equ SPHINX_TELEIA_CID,          0x000017c8  @ Sphinx Teleia (pw=51402177; card-stats.s card_1623 slot=0x17C8); range_max in [ANDRO_SPHINX 0x17c7, SPHINX_TELEIA 0x17c8] blacklist; 4 raw refs; 1 Seg-3 slot
.equ YZ_TANK_DRAGON_CID,         0x000015fa  @ YZ-Tank Dragon (pw=25119460; card-stats.s card_1254 slot=0x15FA); range_max in [XZ_TANK_CANNON 0x15f9, YZ_TANK_DRAGON 0x15fa] blacklist; 4 raw refs; 1 Seg-3 slot
.equ LEVEL_CONVERSION_LAB_CID,   0x000018d9  @ Level Conversion Lab (pw=84397023; card-stats.s card_1865 slot=0x18D9); check_level_conv_lab_node_match predicate target; 4 raw refs; 1 Seg-3 slot
.equ COST_DOWN_CID,              0x000015c7  @ Cost Down (pw=23265313; card-stats.s card_1213 slot=0x15C7); eval_equip_bonus_for_slot count_slot_chain_nodes_by_card_id arg; 4 raw refs; 1 Seg-3 slot

@ =============================================================================
@ file 03 Seg-4a additions (compute_zone_effect_atk_delta + check_field_effect_zone_activation_eligible)
@ =============================================================================

@ Field-effect zone activation eligibility guard cards
.equ EYE_OF_TRUTH_CID,            0x0000137b  @ The Eye of Truth (pw=34694160; card-stats.s card_0791 slot=0x137b);
                                               @ check_field_effect_zone_activation_eligible guard;
                                               @ 2 ROM refs; data.md=0x137B
.equ MIND_ON_AIR_CID,             0x000017e7  @ Mind on Air (pw=66690411; card-stats.s card_1652 slot=0x17e7 L21491);
                                               @ check_field_effect_zone_activation_eligible guard;
                                               @ 2 ROM refs; data.md=0x17E7
.equ RESPECT_PLAY_CID,            0x0000135e  @ Respect Play (pw=08073514; card-stats.s card_0766 slot=0x135e);
                                               @ check_field_effect_zone_activation_eligible gP1LP+0x1ce8 guard;
                                               @ 2 ROM refs; data.md=0x135E

@ ATK delta table card ID range bounds (compute_zone_effect_atk_delta)
.equ YAMI_CID,                    0x000010f5  @ Yami (pw=59197169; card-stats.s card_0297 slot=0x10f5 L3876);
                                               @ lower bound: card_id <= YAMI -> field-spell ATK bonus table path;
                                               @ 2 ROM refs; data.md=0x10F5
.equ MOLTEN_DESTRUCTION_CID,      0x00001346  @ Molten Destruction (pw=19384334; card-stats.s card_0747 slot=0x1346);
                                               @ upper bound of card-dispatch binary-search; card_id > this -> separate branch;
                                               @ 2 ROM refs; data.md=0x1346
.equ GAIA_POWER_CID,              0x00001344  @ Gaia Power (pw=56594520; card-stats.s card_0745 slot=0x1344);
                                               @ compute_zone_effect_atk_delta binary-search node;
                                               @ 2 ROM refs; data.md=0x1344
.equ MYSTIC_PLASMA_ZONE_CID,      0x00001349  @ Mystic Plasma Zone (pw=18161786; card-stats.s card_0750 slot=0x1349);
                                               @ compute_zone_effect_atk_delta exact cmp;
                                               @ 2 ROM refs; data.md=0x1349
.equ NECROVALLEY_CID,             0x0000159d  @ Necrovalley (pw=47355498; card-stats.s card_1185 slot=0x159d);
                                               @ compute_zone_effect_atk_delta gravekeeper-check branch;
                                               @ 2 ROM refs; data.md=0x159D
.equ HARPIES_HUNTING_GROUND_CID,  0x0000183f  @ Harpies' Hunting Ground (pw=75782277; card-stats.s card_1731 slot=0x183f);
                                               @ compute_zone_effect_atk_delta exact cmp;
                                               @ 2 ROM refs; data.md=0x183F

@ =============================================================================
@ file 03 Seg-4b additions: eval_slot_score_entry_full + dispatch_equip_node_by_type cluster
@ =============================================================================

@ Card IDs verified against data/card-stats.s slot= fields (all confidence high)
.equ SKULL_SERVANT_CID,            0x00000fbe  @ Skull Servant (pw=32274490; card_0281 slot=0x0FBE); eval_skull_servant path
.equ DARK_MAGICIAN_CID_0FC9,       0x00000fc9  @ Dark Magician alt print (card_0730 slot=0x0FC9; pw=46986414); distinct from 0x142d
.equ HARPIE_LADY_CID,              0x00000fe4  @ Harpie Lady (pw=76812113; card_0301 slot=0x0FE4); count_paired_slots path
.equ CASTLE_OF_DARK_ILLUSIONS_CID, 0x00000ff9  @ Castle of Dark Illusions (pw=00062986; card_0310 slot=0x0FF9); classify_equip_target_eligibility
.equ PUMPKING_CID,                 0x00001009  @ Pumpking the King of Ghosts (pw=29155212; card_0315 slot=0x1009); eval path
.equ MACHINE_KING_CID,             0x0000113d  @ Machine King (pw=46700124; card_0365 slot=0x113D); eval path
.equ MUKA_MUKA_CID,                0x000011aa  @ Muka Muka (pw=46657337; card_0430 slot=0x11AA); eval path
.equ MAHA_VAILO_CID,               0x00001193  @ Maha Vailo (pw=05798832; card_0420 slot=0x1193); eval path
.equ REVERSE_TRAP_CID,             0x00001257  @ Reverse Trap (pw=77622396; card_0537 slot=0x1257); eval path
.equ MAGICIAN_OF_BLACK_CHAOS_CID,  0x00001278  @ Magician of Black Chaos (pw=30208479; card_0560 slot=0x1278); Dark Magician path
.equ DARK_MAGICIAN_GIRL_CID,       0x0000129e  @ Dark Magician Girl (pw=38033121; card_0584 slot=0x129E); eval path
.equ SHIELD_AND_SWORD_CID,         0x000012cb  @ Shield & Sword (pw=73051941; card_0619 slot=0x12CB); eval path
.equ MIRROR_WALL_CID,              0x00001381  @ Mirror Wall (pw=22359980; card_0704 slot=0x1381); check_slot_equip_chain_rule
.equ AQUA_CHORUS_CID,              0x0000138e  @ Aqua Chorus (pw=95132338; card_0710 slot=0x138E); eval_aqua_chorus path
.equ COMMAND_KNIGHT_CID,           0x00001399  @ Command Knight (pw=10375182; card_0724 slot=0x1399); eval + chain_rule
.equ FLASH_ASSAILANT_CID,          0x00001336  @ Flash Assailant (pw=96890582; card_0648 slot=0x1336); eval path
.equ SLATE_WARRIOR_CID,            0x000013ad  @ Slate Warrior (pw=78636495; card_0726 slot=0x13AD); eval path
.equ NUVIA_THE_WICKED_CID,         0x000013e8  @ Nuvia the Wicked (pw=12953226; card_0745_nuvia slot=0x13E8); eval path
.equ LIGHTNING_BLADE_CID,          0x000013f6  @ Lightning Blade (pw=55226821; card_0752 slot=0x13F6); eval_bonus_state
.equ YELLOW_LUSTER_SHIELD_CID,     0x00001429  @ Yellow Luster Shield (pw=04811901; card_0778 slot=0x1429); eval_bonus_state
.equ DARK_MAGICIAN_CID_142D,       0x0000142d  @ Dark Magician (card_3256 slot=0x142D; pw=46986414 dup); distinct from 0x0fc9
.equ EMBODIMENT_OF_APOPHIS_CID,    0x00001472  @ Embodiment of Apophis (pw=28649820; card_0823 slot=0x1472); eval path
.equ SOUL_OF_PURITY_CID,           0x00001483  @ Soul of Purity and Light (pw=77527210; card_0833 slot=0x1483); eval_bonus_state
.equ ROCK_SPIRIT_CID,              0x00001486  @ The Rock Spirit (pw=04081094; card_0836 slot=0x1486); eval path
.equ THE_A_FORCES_CID,             0x000014cf  @ The A. Forces (pw=00000000; card_0883 slot=0x14CF); eval_command_knight path
.equ MUDORA_CID,                   0x000014ec  @ Mudora (pw=00000000; card_0897 slot=0x14EC); eval path
.equ MASTER_OF_DRAGON_SOLDIER_CID, 0x0000157d  @ Master of Dragon Soldier (pw=00000000; card_1159 slot=0x157D); eval path
.equ BANNER_OF_COURAGE_CID,        0x000015a2  @ Banner of Courage (pw=10012614; card_1185b slot=0x15A2); eval_bonus_state
.equ DARK_PALADIN_CID,             0x000015fc  @ Dark Paladin (pw=98502113; card_1257 slot=0x15FC); eval_dark_paladin path
.equ MAGICAL_MARIONETTE_CID,       0x00001615  @ Magical Marionette (pw=08034697; card_1280 slot=0x1615); eval path
.equ METAL_REFLECT_SLIME_CID,      0x00001636  @ Metal Reflect Slime (pw=26905245; card_1304 slot=0x1636); eval path
.equ GYAKU_GIRE_PANDA_CID,         0x00001651  @ Gyaku-Gire Panda (pw=00000000; card_1328 slot=0x1651); eval path
.equ NIGHTMARE_PENGUIN_CID,        0x000016ab  @ Nightmare Penguin (pw=81306586; card_1400 slot=0x16AB); eval_bonus_state
.equ PERFECT_MACHINE_KING_CID,     0x000016ac  @ Perfect Machine King (pw=00000000; card_1401 slot=0x16AC); eval path
.equ SKULL_ZOMA_CID,               0x0000172f  @ Skull Zoma (pw=00000000; card_1472 slot=0x172F); eval path
.equ AGENT_OF_FORCE_MARS_CID,      0x00001742  @ The Agent of Force - Mars (pw=91123920; card_1488 slot=0x1742); eval path
.equ UNHAPPY_GIRL_CID,             0x00001743  @ The Unhappy Girl (pw=27618832; card_1489 slot=0x1743); classify_equip_target_eligibility
.equ MOKEY_MOKEY_CID,              0x00001782  @ Mokey Mokey (pw=27973334; card_1540 slot=0x1782); eval_mokey_mokey path
.equ THEBAN_NIGHTMARE_CID,         0x00001789  @ Theban Nightmare (pw=00000000; card_1548 slot=0x1789); eval path
.equ ELEMENT_DRAGON_CID,           0x000017e3  @ Element Dragon (pw=00000000; card_1651 slot=0x17E3); eval path
.equ ENRAGED_MUKA_MUKA_CID,        0x000017eb  @ Enraged Muka Muka (pw=01945754; card_1658 slot=0x17EB); eval path
.equ GREEN_GADGET_CID,             0x00001807  @ Green Gadget (pw=67376548; card_1680 slot=0x1807); eval_gadget path
.equ STRONGHOLD_CID,               0x00001809  @ Stronghold (pw=00000000; card_1682 slot=0x1809); eval path
.equ RED_GADGET_CID,               0x0000180b  @ Red Gadget (pw=86445415; card_1684 slot=0x180B); eval_gadget path
.equ YELLOW_GADGET_CID,            0x0000180c  @ Yellow Gadget (pw=13839120; card_1685 slot=0x180C); eval_gadget path
.equ SILENT_MAGICIAN_LV4_CID,      0x00001817  @ Silent Magician LV4 (pw=73752131; card_1697 slot=0x1817); eval path
.equ ULTIMATE_INSECT_LV3_CID,      0x00001822  @ Ultimate Insect LV3 (pw=00000000; card_1710 slot=0x1822); eval_bonus_state
.equ ELEMENT_SAURUS_CID,           0x00001827  @ Element Saurus (pw=00000000; card_1716 slot=0x1827); eval path
.equ MOKEY_MOKEY_SMACKDOWN_CID,    0x00001843  @ Mokey Mokey Smackdown (pw=01784618; card_1741 slot=0x1843); eval_mokey_mokey path
.equ BEHEMOTH_KING_CID,            0x00001864  @ Behemoth the King of All Animals (pw=00000000; card_1764 slot=0x1864); eval path
.equ ULTIMATE_INSECT_LV5_CID,      0x0000185e  @ Ultimate Insect LV5 (pw=00000000; card_1757 slot=0x185E); eval_bonus_state
.equ RED_EYES_DARKNESS_DRAGON_CID, 0x00001894  @ Red-Eyes Darkness Dragon (pw=00000000; card_1801 slot=0x1894); eval path
.equ KING_OF_SKULL_SERVANTS_CID,   0x000018c5  @ King of the Skull Servants (pw=00000000; card_1842 slot=0x18C5); eval path
.equ DORIADO_CID,                  0x000018c7  @ Elemental Mistress Doriado (pw=00000000; card_1843 slot=0x18C7); eval path
.equ BATTERYMAN_AA_CID,            0x000018c3  @ Batteryman AA (pw=63142001; card-stats.s card_1842b slot=0x18C3); shifted sentinel in eval_hand_field6
.equ BATTERYMAN_AA_CID_SHIFTED,    0xc6180000  @ BATTERYMAN_AA_CID<<19 = 0x18c3<<19; slot_word<<19 sentinel; DAT_08038c84
.equ BATTERYMAN_C_CID,             0x0000191c  @ Batteryman C (pw=00000000; card-stats.s card_1913 slot=0x191C); shifted sentinel
.equ BATTERYMAN_C_CID_SHIFTED,     0xc8e00000  @ BATTERYMAN_C_CID<<19 = 0x191c<<19; slot_word<<19 sentinel; DAT_08039128
.equ SANCTUARY_CID_SHIFTED,        0xbaf00000  @ SANCTUARY_IN_THE_SKY_CID(0x175e)<<19; slot_word<<19 sentinel; DAT_08038ae4
.equ DARK_DREADROUTE_CID,          0x00001905  @ Dark Dreadroute (pw=00000000; card_1904 slot=0x1905); check_slot_equip_chain_rule
.equ TADPOLE_CID,                  0x00001919  @ T.A.D.P.O.L.E. (pw=10012614; card_1912 slot=0x1919); eval_extra_deck path
.equ TYRANNO_INFINITY_CID,         0x0000191b  @ Tyranno Infinity (pw=00000000; card_1914 slot=0x191B); eval path
.equ EHERO_SHINING_FLARE_WINGMAN_CID, 0x00001943 @ Elemental Hero Shining Flare Wingman (pw=25366484; card_1939 slot=0x1943); eval path
.equ WATER_DRAGON_CID,             0x00001951  @ Water Dragon (pw=85066822; card_1958 slot=0x1951); check_slot_equip_chain_rule
.equ CYBER_BLADER_CID,             0x00001955  @ Cyber Blader (pw=00000000; card_1962 slot=0x1955); check_slot_equip_chain_rule
.equ MACHINE_KING_PROTOTYPE_CID,   0x000019be  @ Machine King - 3000/8 (pw=00000000; card_1949 slot=0x19BE); eval path
.equ ANCIENT_GEAR_CASTLE_CID,      0x000019b2  @ Ancient Gear Castle (pw=92001300; card_1933 slot=0x19B2); eval_bonus_state
.equ PARASITIC_TICKY_CID,          0x000019c4  @ Parasitic Ticky (pw=00000000; card_1952 slot=0x19C4); eval path
.equ TREEBORN_FROG_CID,            0x000019cb  @ Treeborn Frog (pw=00000000; card_1960 slot=0x19CB); eval_extra_deck path
.equ BEELZE_FROG_CID,              0x000019cc  @ Beelze Frog (pw=00000000; card_1961 slot=0x19CC); eval path
.equ SAND_MOTH_CID,                0x000019d2  @ Sand Moth (pw=00000000; card_1968 slot=0x19D2); eval path
.equ D3S_FROG_CID,                 0x000019d6  @ D.3.S. Frog (pw=00000000; card_1972 slot=0x19D6); eval path
.equ EHERO_ERIKSHIELER_CID,        0x000019ef  @ Elemental Hero Erikshieler (pw=00000000; card_1992 slot=0x19EF); eval path
.equ GREAT_SPIRIT_CID,             0x000019f1  @ Great Spirit (pw=00000000; card_1994 slot=0x19F1); eval path
.equ HELIOS_CID,                   0x000019f6  @ The Ancient Sun Helios (pw=00000000; card_1999 slot=0x19F6); eval_helios path
.equ HELIOS_DUO_MEGISTE_CID,       0x000019f7  @ Helios Duo Megiste (pw=00000000; card_2000 slot=0x19F7); eval_helios path
.equ GOBLIN_KING_CID,              0x00001755  @ Goblin King (pw=18590133; card_1536 slot=0x1755); eval path
.equ SLOT_CARD_EMPTY,              0x0000ffff  @ empty slot sentinel: u16 card_id = 0xffff means no card; eval_slot_empty_sentinel

@ --- file 03 Seg-5 additions (build_equip_target_eligibility_table .. get_zone_slot_ptr) ---
.equ DEMOTION_CID,                 0x000015e3  @ Demotion (pw=72575145; card_1236 slot=0x15E3); eval_equip_chain_score_for_slot
.equ PARASITE_PARACIDE_CID,        0x000012a1  @ Parasite Paracide (pw=27911549; card_0625 slot=0x12A1); query_slot_card_state_code
.equ DNA_SURGERY_CID,              0x00001357  @ DNA Surgery (pw=74701381; card_0760 slot=0x1357); query_slot_card_state_code
.equ D_TRIBE_CID,                  0x000015ae  @ D. Tribe (pw=02833249; card_1199 slot=0x15AE); query_slot_card_state_code
.equ HOMUNCULUS_CID,               0x0000183b  @ Homunculus the Alchemic Being (pw=40410110; card_1727 slot=0x183B); resolve_slot_chain_best_target
.equ SCROLL_OF_BEWITCHMENT_CID,    0x0000145b  @ Scroll of Bewitchment (pw=10352095; card_0927 slot=0x145B); resolve_slot_chain_best_target
.equ DNA_TRANSPLANT_CID,           0x0000171f  @ DNA Transplant (pw=56769674; card_1495 slot=0x171F); base value for shifted sentinel
.equ DNA_TRANSPLANT_CID_SHIFTED,   0xb8f80000  @ DNA_TRANSPLANT_CID(0x171f)<<19; lsls r0,#0x13 then cmp sentinel; resolve_slot_chain_best_target

@ --- file 03 Seg-6 additions (get_zone_slot_entity_ref_by_type .. check_field_spell_neo_daedalus_group_placeable) ---
.equ CHAIN_ENERGY_CID,               0x0000132c  @ Chain Energy (pw=79323590; card_0723 slot=0x132C); LP-threshold gate in check_lp_exceeds_spell_copy_threshold; 1 slot
.equ JUDGEMENT_OF_PHARAOH_CID,       0x00001679  @ Judgement of Pharaoh (pw=55948544; card_1350 slot=0x1679); zone effect node guard (x5 refs); field-spell placement gates
.equ LIGHT_OF_INTERVENTION_CID,      0x0000135d  @ Light of Intervention (pw=62867251; card_0765 slot=0x135D); field-spell group gate in check_field_spell_group_placeable; 1 slot
.equ NON_AGGRESSION_AREA_CID,        0x000015ad  @ Non Aggression Area (pw=76848240; card_1198 slot=0x15AD); zone node block check (x3 refs); placement gates
.equ LAVA_GOLEM_CID,                 0x00001578  @ Lava Golem (pw=00102380; card_1152 slot=0x1578); field-spell placement block (x2 refs)
.equ BOSS_RUSH_CID,                  0x00001972  @ Boss Rush (pw=66947414; card_1983 slot=0x1972); effect zone count gate (x2 refs)
.equ JAM_BREEDING_MACHINE_CID,       0x000013ff  @ Jam Breeding Machine (pw=21770260; card_0874 slot=0x13FF); effect zone count gate (x3 refs)
.equ LAST_WARRIOR_FROM_ANOTHER_PLANET_CID, 0x000012b1  @ The Last Warrior from Another Planet (pw=86099788; card_0634 slot=0x12B1); field-spell Last Warrior gate (x3 refs)
.equ JOWGEN_THE_SPIRITUALIST_CID,    0x0000147f  @ Jowgen the Spiritualist (pw=41855169; card_0957 slot=0x147F); Neo Daedalus placement gate; 1 slot

@ --- file 03 Seg-7 additions (eval_equip_placement_full_check .. tick_equip_candidate_scan_with_display) ---
.equ BALLISTA_OF_RAMPART_SMASHING_CID, 0x00001846  @ Ballista of Rampart Smashing (pw=00242146; card_4305 slot=0x1846); tick_equip_chain_link_display_seq chain pool index; 1 slot

@ =============================================================================
@ file 03 Seg-8 additions: equip chain display seq card IDs
@ =============================================================================
.equ BLUE_EYES_WHITE_DRAGON_CID,    0x00000fa7  @ Blue-Eyes White Dragon (pw=89631139; card_0001 slot=0x0FA7); setup_equip_chain_for_slot card_type upper bound
.equ eval_gap_cid_0fa6,             0x00000fa6  @ gap slot (NOT in card-stats.s; between slot 0x0fa5 and card_0001=BEWD); setup_equip_chain_for_slot card_type lower bound; low confidence
.equ A_DEAL_WITH_DARK_RULER_CID,    0x0000165a  @ A Deal with Dark Ruler (pw=06850209; card_1330 slot=0x165A); tick_normal_summon_zone_state link_equip_node_to_chain chain_type arg
.equ eval_gap_cid_11ed,             0x000011ed  @ gap slot (NOT in card-stats.s; between 0x11eb=Takuhee and 0x11ee=Binding Chain); finalize_equip_chain_removal_state sentinel; low confidence

@ =============================================================================
@ file 03 Seg-9 additions: flip-summon / zone-slot display seq card IDs
@ =============================================================================
.equ UNHAPPY_GIRL_CID_SHIFTED,  0xba180000  @ UNHAPPY_GIRL_CID(0x1743)<<19; lsls r0,r0,#0x13; cmp sentinel in tick_flip_summon_state; 1 slot
.equ BACKFIRE_CID,              0x00001762  @ Backfire (pw=82705573; card_1547 slot=0x1762); tick_zone_card_place_with_slot_resolve_seq + tick_equip_node_chain_link_display_seq; 2 slots
.equ SOUL_ABSORPTION_CID,       0x000016da  @ Soul Absorption (pw=68073522; card_1435 slot=0x16DA); same 2 funcs; 2 slots
.equ HUMAN_WAVE_TACTICS_CID,    0x000017b2  @ Human-Wave Tactics (pw=30353551; card_1606 slot=0x17B2); tick_equip_node_chain_link_display_seq; 1 slot

@ =============================================================================
@ file 03 Seg-10 additions: equip detach / zone display seq shifted CID sentinel
@ =============================================================================
.equ HELPOEMER_CID_SHIFTED,     0xab880000  @ HELPOEMER_CID(0x1571)<<19; lsls r1,r0,#0x13; cmp sentinel in tick_zone_slot_equip_detach_display_seq state=0; 1 slot

@ =============================================================================
@ file 04 Seg-4 additions: equip-chain / draw-card display seq card IDs
@ =============================================================================
.equ POLYMERIZATION_CID,            0x000012e5  @ Polymerization (pw=24094653; card_0669 slot=0x12E5); tick_equip_attach_display_sequence equip chain depth table base offset; 1 Seg-4 slot; 27 ROM refs
.equ RYU_SENSHI_CID,                0x000014c7  @ Ryu Senshi (pw=49868263; card_1016 slot=0x14C7); dispatch_equip_chain_slot_scan_by_player BST card_id gate (lower); 1 Seg-4 slot; 13 ROM refs
.equ FRONTIER_WISEMAN_CID,          0x000014ca  @ Frontier Wiseman (pw=38742075; card_1018 slot=0x14CA); dispatch_equip_chain_slot_scan_by_player BST card_id gate + count_available_effect_zones; 2 Seg-4 slots; 8 ROM refs
.equ VICTORY_D_CID,                 0x000016ec  @ Victory D. (pw=44910027; card_1446 slot=0x16EC); tick_draw_card_display_seq zone_ref == VICTORY_D_CID branch; 1 Seg-4 slot; 12 ROM refs
.equ BLUE_EYES_SHINING_DRAGON_CID,  0x000017c2  @ Blue-Eyes Shining Dragon (pw=53347303; card_1617 slot=0x17C2); dispatch_equip_chain_slot_scan_by_player enqueue_field_slot path; 1 Seg-4 slot; 11 ROM refs
.equ RARE_METALMORPH_CID,           0x0000184b  @ Rare Metalmorph (pw=12503902; card_1743 slot=0x184B); dispatch_equip_chain_slot_scan_by_player find_equip_slot + final BST; 2 Seg-4 slots; 17 ROM refs

@ =============================================================================
@ file 04 Seg-5 additions: Gearfried card IDs (enqueue_zone_slot_sprite_attr_by_card_type BST)
@ =============================================================================
.equ GEARFRIED_IRON_KNIGHT_CID,    0x000013c3  @ Gearfried the Iron Knight (pw=00423705; card_0839 slot=0x13C3); BST dispatch in enqueue_zone_slot_sprite_attr_by_card_type; 10 ROM refs
.equ GEARFRIED_SWORDMASTER_CID,    0x0000186b  @ Gearfried the Swordmaster (pw=57046845; card_1772 slot=0x186B); BST dispatch; set_field_slot_bit_with_sprite_update path; 8 ROM refs

@ =============================================================================
@ file 04 Seg-6 additions: equip zone sprite / banisher cluster card IDs
@ =============================================================================
.equ BANISHER_OF_THE_LIGHT_CID,      0x00001332  @ Banisher of the Light (pw=61528025; card_0729 slot=0x1332); dispatch_equip_zone_sprite_banisher_* cluster; 6 Seg-6 slots
.equ GRAVEROBBER_CID,                0x00001379  @ Graverobber (pw=61705417; card_0789 slot=0x1379); dispatch_equip_zone_sprite_and_activation + render_equip_zone_sprite_with_chain_lp; 2 Seg-6 slots
.equ SUPER_REJUVENATION_CID,         0x000014e2  @ Super Rejuvenation (pw=27770341; card_1042 slot=0x14E2); dispatch_equip_zone_sprite_and_activation + dispatch_equip_zone_sprite_banisher_with_spell_check; 2 Seg-6 slots
.equ SAMSARA_CID,                    0x000019da  @ Samsara (pw=44182827; card_2061 slot=0x19DA); dispatch_equip_zone_sprite_banisher_with_spell_check second-card check; 1 slot
.equ CRASS_CLOWN_CID,                0x00001005  @ Crass Clown (pw=93889755; card_0101 slot=0x1005); apply_slot_equip_activation_with_sprite branch A; 1 slot
.equ BLADE_RABBIT_CID,               0x00001868  @ Blade Rabbit (pw=58268433; card_1769 slot=0x1868); apply_slot_equip_activation_with_sprite branch D; 1 slot
.equ AMEBA_CID,                      0x0000118a  @ Ameba (pw=95174353; card_0407 slot=0x118A); scan_equip_chain_list_for_activation_sprite equip activation range base (0x118a..0x11c9); 1 slot; 28 raw ROM refs
.equ MANTICORE_OF_DARKNESS_CID,      0x000016f9  @ Manticore of Darkness (pw=77121851; card_1458 slot=0x16F9); dispatch_equip_zone_sprite_and_activation BST root; 1 slot
.equ ARCHFIEND_OF_GILFER_CID,        0x000013e3  @ Archfiend of Gilfer (pw=50287060; card_0853 slot=0x13E3); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ MINAR_CID,                      0x000011bc  @ Minar (pw=32539892; card_0444 slot=0x11BC); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ SKULL_MARK_LADYBUG_CID,         0x000012a2  @ Skull-Mark Ladybug (pw=64306248; card_0626 slot=0x12A2); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ MAKYURA_THE_DESTRUCTOR_CID,     0x000014a5  @ Makyura the Destructor (pw=21593977; card_0991 slot=0x14A5); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ DESPAIR_FROM_THE_DARK_CID,      0x00001653  @ Despair from the Dark (pw=71200730; card_1323 slot=0x1653); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ FEAR_FROM_THE_DARK_CID,         0x00001655  @ Fear from the Dark (pw=34193084; card_1325 slot=0x1655); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ OUTSTANDING_DOG_MARRON_CID,     0x00001687  @ Outstanding Dog Marron (pw=11548522; card_1364 slot=0x1687); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ ROC_FROM_THE_VALLEY_OF_HAZE_CID, 0x00001828 @ Roc from the Valley of Haze (pw=28143906; card_1708 slot=0x1828); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ NIGHT_ASSAILANT_CID,            0x0000179a  @ Night Assailant (pw=16226786; card_1585 slot=0x179A); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ BROWW_HUNTSMAN_OF_DARK_WORLD_CID, 0x00001966 @ Broww, Huntsman of Dark World (pw=79126789; card_1972 slot=0x1966); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ SILLVA_WARLORD_OF_DARK_WORLD_CID, 0x00001968 @ Sillva, Warlord of Dark World (pw=32619583; card_1974 slot=0x1968); dispatch_equip_zone_sprite_and_activation BST; 1 slot
.equ EKIBYO_DRAKMORD_CID_SHIFTED,    0xa4e80000  @ EKIBYO_DRAKMORD_CID(0x149d)<<19; scan_equip_chain_list_for_activation_sprite type-match sentinel; 1 raw ROM ref
@ (card_0987: Ekibyo Drakmord pw=69954399; 0xa4e80000>>19=0x149d; card-stats.s verified)
.equ act_cid_1048_08043b48,          0x00001048  @ card_id branch B in apply_slot_equip_activation_with_sprite; NOT in card-stats.s -> neutral name; 1 slot
.equ act_cid_1197_08043be8,          0x00001197  @ card_id branch C in apply_slot_equip_activation_with_sprite; NOT in card-stats.s -> neutral name; 1 slot

@ =============================================================================
@ file 04 Seg-7 additions: Watapon / Dark Mimic LV1 card IDs
@ =============================================================================
.equ WATAPON_CID,                    0x000017cc  @ Watapon (pw=87774234; card-stats.s card_1626 slot=0x17CC); enqueue_hand_sprite_by_zone_set_code Watapon-path; 10 raw ROM refs
.equ WATAPON_EQUIP_ACTIVATION_MASK,  0x34500000  @ activation flag mask ORed into attr2 arg of apply_equip_activation_with_id_lookup for Watapon path in enqueue_hand_sprite_by_zone_set_code; 24 raw ROM refs
.equ DARK_MIMIC_LV1_CID,             0x000017d5  @ Dark Mimic LV1 (pw=74713516; card-stats.s card_1635 slot=0x17D5); enqueue_equip_chain_sprite_attrs_for_slot card_type filter A; 16 raw ROM refs

@ =============================================================================
@ file 04 Seg-8a additions: card IDs for dispatch_card_effect_sprite_render_by_card_id BST
@   + equip chain activation eligibility cluster (update_duel_field_slot_sprite_state etc.)
@ Values confirmed via data/card-stats.s slot=0xXXXX pattern; 4 gap stubs (*_cid_* names).
@ =============================================================================
.equ SANGAN_CID,                       0x00000fd6  @ Sangan (pw=26202165; card-stats.s slot=0x0fd6)
.equ upd_cid_10c6,                     0x000010c6  @ card gap; no card-stats entry; neutral name
.equ BLACK_PENDANT_CID,                0x000010dd  @ Black Pendant (pw=65169794; card-stats.s slot=0x10dd)
@ UMI_CARD_ID = 0x000010f4 already in card_info.inc -- REUSE
.equ GODDESS_OF_WHIM_CID,              0x00001153  @ Goddess of Whim (pw=67959180; card-stats.s slot=0x1153)
.equ COCKROACH_KNIGHT_CID,             0x00001185  @ Cockroach Knight (pw=33413638; card-stats.s slot=0x1185)
.equ WITCH_OF_THE_BLACK_FOREST_CID,    0x000011e4  @ Witch of the Black Forest (pw=78010363; card-stats.s slot=0x11e4)
.equ upd_cid_120e,                     0x0000120e  @ card gap; no card-stats entry; neutral name
.equ JINZO_CID,                        0x00001296  @ Jinzo (pw=77585513; card-stats.s slot=0x1296)
.equ SATELLITE_CANNON_CID,             0x000012ac  @ Satellite Cannon (pw=50400231; card-stats.s slot=0x12ac)
.equ COPYCAT_CID,                      0x000012bb  @ Copycat (pw=26376390; card-stats.s slot=0x12bb)
.equ GIANT_RAT_CID,                    0x00001333  @ Giant Rat (pw=97017120; card-stats.s slot=0x1333)
.equ KARATE_MAN_CID,                   0x00001337  @ Karate Man (pw=23289281; card-stats.s slot=0x1337)
.equ NIMBLE_MOMONGA_CID,               0x0000133a  @ Nimble Momonga (pw=22567609; card-stats.s slot=0x133a)
.equ SHINING_ANGEL_CID,                0x0000133c  @ Shining Angel (pw=95956346; card-stats.s slot=0x133c)
.equ MYSTIC_TOMATO_CID,                0x00001342  @ Mystic Tomato (pw=83011277; card-stats.s slot=0x1342)
@ SPELL_ZONE_TARGET_CARD_ID = 0x00001368 already in card_info.inc -- REUSE
.equ MUCUS_YOLK_CID,                   0x000013b2  @ Mucus Yolk (pw=70307656; card-stats.s slot=0x13b2)
.equ upd_cid_13e9,                     0x000013e9  @ card gap; no card-stats entry; neutral name
.equ TORNADO_WALL_CID,                 0x000013f7  @ Tornado Wall (pw=18605135; card-stats.s slot=0x13f7)
@ ZOMBYRA_THE_DARK_CID = 0x0000147d already in card_info.inc -- REUSE
.equ THE_EMPERORS_HOLIDAY_CID,         0x00001495  @ The Emperor's Holiday (pw=68400115; card-stats.s slot=0x1495)
.equ AMAZONESS_CHAIN_MASTER_CID,       0x000014ab  @ Amazoness Chain Master (pw=29654737; card-stats.s slot=0x14ab)
.equ AGIDO_CID,                        0x000014f6  @ Agido (pw=16135253; card-stats.s slot=0x14f6)
.equ DARK_COFFIN_CID,                  0x00001544  @ Dark Coffin (pw=01804528; card-stats.s slot=0x1544)
.equ LORD_POISON_CID,                  0x0000156d  @ Lord Poison (pw=40320754; card-stats.s slot=0x156d)
.equ YOMI_SHIP_CID,                    0x00001591  @ Yomi Ship (pw=51534754; card-stats.s slot=0x1591)
.equ COBRA_JAR_CID,                    0x00001595  @ Cobra Jar (pw=86801871; card-stats.s slot=0x1595)
.equ GRANADORA_CID,                    0x0000163f  @ Granadora (pw=13944422; card-stats.s slot=0x163f)
.equ OJAMA_TRIO_CID,                   0x0000166a  @ Ojama Trio (pw=29843091; card-stats.s slot=0x166a)
.equ upd_cid_1672,                     0x00001672  @ card gap; no card-stats entry; neutral name
.equ GREAT_MAJU_GARZETT_CID,           0x00001688  @ Great Maju Garzett (pw=47942531; card-stats.s slot=0x1688)
.equ PANDEMONIUM_CID,                  0x0000169f  @ Pandemonium (pw=94585852; card-stats.s slot=0x169f)
.equ SILPHEED_CID,                     0x000016c8  @ Silpheed (pw=73001017; card-stats.s slot=0x16c8)
.equ FUHMA_SHURIKEN_CID,               0x000016cc  @ Fuhma Shuriken (pw=09373534; card-stats.s slot=0x16cc)
.equ TOWER_OF_BABEL_CID,               0x000016de  @ Tower of Babel (pw=94256039; card-stats.s slot=0x16de)
.equ BURNING_ALGAE_CID,                0x000016f5  @ Burning Algae (pw=41859700; card-stats.s slot=0x16f5)
.equ EMES_THE_INFINITY_CID,            0x0000172b  @ Emes the Infinity (pw=43580269; card-stats.s slot=0x172b)
.equ EMISSARY_OF_THE_AFTERLIFE_CID,    0x00001796  @ Emissary of the Afterlife (pw=75043725; card-stats.s slot=0x1796)
.equ FAMILIAR_KNIGHT_CID,              0x000017c3  @ Familiar Knight (pw=89731911; card-stats.s slot=0x17c3)
.equ MASKED_DRAGON_CID,                0x000017e6  @ Masked Dragon (pw=39191307; card-stats.s slot=0x17e6)
.equ NINJITSU_ART_OF_DECOY_CID,        0x000017ff  @ Ninjitsu Art of Decoy (pw=89628781; card-stats.s slot=0x17ff)
.equ SILENT_MAGICIAN_LV8_CID,          0x0000181a  @ Silent Magician LV8 (pw=72443568; card-stats.s slot=0x181a)
@ RAGING_FLAME_SPRITE_CID = 0x0000182d already in card_info.inc -- REUSE
.equ GAIA_SOUL_CID,                    0x00001835  @ Gaia Soul the Combustible Collective (pw=51355346; card-stats.s slot=0x1835)
.equ MOKEY_MOKEY_KING_CID,             0x0000183d  @ Mokey Mokey King (pw=13803864; card-stats.s slot=0x183d)
.equ NECKLACE_OF_COMMAND_CID,          0x00001841  @ Necklace of Command (pw=48576971; card-stats.s slot=0x1841)
.equ XING_ZHEN_HU_CID,                 0x0000184a  @ Xing Zhen Hu (pw=76515293; card-stats.s slot=0x184a)
.equ SACRED_PHOENIX_CID,               0x0000185c  @ Sacred Phoenix of Nephthys (pw=61441708; card-stats.s slot=0x185c)
.equ MECHA_DOG_MARRON_CID,             0x00001869  @ Mecha-Dog Marron (pw=94667532; card-stats.s slot=0x1869)
.equ FIREBIRD_CID,                     0x00001875  @ Firebird (pw=87473172; card-stats.s slot=0x1875)
.equ CENTRIFUGAL_FIELD_CID,            0x0000187f  @ Centrifugal Field (pw=01801154; card-stats.s slot=0x187f)
.equ MILLENNIUM_SCORPION_CID,          0x000018ae  @ Millennium Scorpion (pw=82482194; card-stats.s slot=0x18ae)
.equ CRIOSPHINX_CID,                   0x000018b2  @ Criosphinx (pw=18654201; card-stats.s slot=0x18b2)
.equ MEGAROCK_DRAGON_CID,              0x000018b4  @ Megarock Dragon (pw=71544954; card-stats.s slot=0x18b4)
.equ DD_SURVIVOR_CID,                  0x000018bc  @ D.D. Survivor (pw=48092532; card-stats.s slot=0x18bc)
.equ NITRO_UNIT_CID,                   0x000018d1  @ Nitro Unit (pw=23842445; card-stats.s slot=0x18d1)
.equ KOZAKYS_SELF_DESTRUCT_CID,        0x000018d7  @ Kozaky's Self-Destruct Button (pw=21908319; card-stats.s slot=0x18d7)
.equ UFOROID_CID,                      0x000018f4  @ UFOroid (pw=07602840; card-stats.s slot=0x18f4)
.equ UFOROID_FIGHTER_CID,              0x000018fb  @ UFOroid Fighter (pw=32752319; card-stats.s slot=0x18fb)
.equ GIANT_KOZAKY_CID,                 0x00001914  @ Giant Kozaky (pw=58185394; card-stats.s slot=0x1914)
.equ OJAMAGIC_CID,                     0x00001946  @ Ojamagic (pw=24643836; card-stats.s slot=0x1946)
.equ WHITE_HORNS_DRAGON_CID,           0x00001996  @ White Horns Dragon (pw=73891874; card-stats.s slot=0x1996)
.equ RAVIEL_LORD_CID,                  0x000019a5  @ Raviel, Lord of Phantasms (pw=69890967; card-stats.s slot=0x19a5)
.equ GOKIPON_CID,                      0x000019c5  @ Gokipon (pw=14472500; card-stats.s slot=0x19c5)
.equ HELIOS_TRIS_MEGISTE_CID,          0x000019f8  @ Helios Tris Megiste (pw=17286057; card-stats.s slot=0x19f8)
.equ VAMPIRE_LORD_CID,                 0x00001522  @ Vampire Lord (pw=53839837; card-stats.s slot=0x1522)
.equ ROYAL_KEEPER_CID,                 0x00001527  @ Royal Keeper (pw=16509093; card-stats.s slot=0x1527)
.equ EXARION_UNIVERSE_CID,             0x0000154c  @ Exarion Universe (pw=63749102; card-stats.s slot=0x154c)
.equ MAJI_GIRE_PANDA_CID,              0x00001862  @ Maji-Gire Panda (pw=60102563; card-stats.s slot=0x1862)

@ =============================================================================
@ file 04 Seg-8b additions: equip target eligibility / zone action CIDs
@ =============================================================================
.equ PANDEMONIUM_WATCHBEAR_CID,        0x00001683  @ Pandemonium Watchbear (pw=75375465; card-stats.s slot=0x1683)
.equ HEAVY_MECH_SUPPORT_PLATFORM_CID, 0x00001825  @ Heavy Mech Support Platform (pw=23265594; card-stats.s slot=0x1825)
.equ AUTONOMOUS_ACTION_UNIT_CID,      0x000015e6  @ Autonomous Action Unit (pw=71453557; card-stats.s slot=0x15e6)
.equ CALL_OF_THE_HAUNTED_CID,         0x0000137d  @ Call of the Haunted (pw=97077563; card-stats.s slot=0x137d)
.equ PREMATURE_BURIAL_CID,            0x00001366  @ Premature Burial (pw=70828912; card-stats.s slot=0x1366)
.equ SPIRIT_MESSAGE_L_CID,            0x0000149a  @ Spirit Message L (pw=30170981; card-stats.s slot=0x149a)
.equ SPIRITUAL_ENERGY_SETTLE_CID,     0x0000150e  @ Spiritual Energy Settle Machine (pw=99173029; card-stats.s slot=0x150e)
.equ THE_FIRST_SARCOPHAGUS_CID,       0x000017af  @ The First Sarcophagus (pw=31076103; card-stats.s slot=0x17af)
.equ THE_THIRD_SARCOPHAGUS_CID,       0x000017ad  @ The Third Sarcophagus (pw=78697395; card-stats.s slot=0x17ad)
.equ BATTLE_SCARRED_CID,              0x000016a2  @ Battle-Scarred (pw=94463200; card-stats.s slot=0x16a2)
.equ NINJITSU_ART_OF_TRANSFORMATION_CID, 0x00001768  @ Ninjitsu Art of Transformation (pw=70861343; card-stats.s slot=0x1768)
.equ RE_FUSION_CID,                   0x00001881  @ Re-Fusion (pw=74694807; card-stats.s slot=0x1881)
.equ SYMBOL_OF_HERITAGE_CID,          0x000019d7  @ Symbol of Heritage (pw=45305419; card-stats.s slot=0x19d7)
.equ BIG_BANG_SHOT_CID,               0x00001625  @ Big Bang Shot (pw=61127349; card-stats.s slot=0x1625)
.equ DESTINY_BOARD_CID,               0x00001468  @ Destiny Board (pw=94212438; card-stats.s slot=0x1468)
.equ AMPLIFIER_CID,                   0x000012d3  @ Amplifier (pw=00303660; card-stats.s slot=0x12d3)
.equ SOUL_RESURRECTION_CID,           0x000017b7  @ Soul Resurrection (pw=92924317; card-stats.s slot=0x17b7)
.equ FIBER_JAR_CID,                   0x000014fb  @ Fiber Jar (pw=78706415; card-stats.s slot=0x14fb)
.equ GOBLIN_OUT_OF_FRYING_PAN_CID,    0x000019e1  @ Goblin Out of the Frying Pan (pw=69632396; card-stats.s slot=0x19e1)
