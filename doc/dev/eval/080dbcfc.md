# Eval: 0x080dbcfc
proposal_name: render_pack_card_name_to_sprite
score: 45/45
status: PASSED

R1 (form): 5/5 -- regex ^[a-z][a-z0-9_]+$ OK; verb_object "render <pack_card_name> to <sprite>"; no ARM mnemonic collision; not a duplicate (grep naming-proposals.csv: 0 hits).
R2 (plate): 5/5 -- ASCII OK, 89 words (<500), factual; Constants block consistent (IWRAM_LANG_FLAG / FONT_CTX / OBJ_ATTR_BASE / TILE_WIDTH_SHIFT) and matches asm DAT pool (DAT_080dbd7c=0x02000000, DAT_080dbd80=0x6c2c, DAT_080dbd84=0x02006ed0, DAT_080dbd8c=0x8108).
R3 (params): 5/5 -- FIXED. r0=void* vram_dest (captured via .hword 0x4680=mov r8,r0 + adds r0,r1,#0 immediate swap at 080dbd06); r1=u8* card_name_ptr (passes through r0 to select_charset_then_load_name); r2=u8 render_mode [0..4+] correctly captured via `adds r4,r2,#0` at 080dbd08 and branches at cmp r4,#0/#2/#3 confirm enum semantics. The spurious "r4 (via .hword 0x4646)" APCS row is removed -- .hword 0x4646 = mov r6,r8 is callee-save spill (entry note correctly explains this is "callee-save 高寄存器保存"). Charset flag IWRAM read at [0x02000000+0x6c2c] noted as internal, not APCS.
R4 (return): 5/5 -- r0 = u8 tile_width with [1..N] range; `adds r0,r7,#0` before pop preserves r7 (asrs r7,r0,#3 at 080dbd62 = (pixel_width+8)>>3).
R5 (side effects): 5/5 -- vram_dest write via commit_line_buffer_to_sprite_vram + font ctx [0x02006ed0+0x4/+0x8/+0x14/+0x15] all listed; matches strb sequences 080dbd30/080dbd38/080dbd42 + str r0,[r2,#0x4] at 080dbd58.
R6 (constants): 5/5 -- All non-trivial literals captured: IWRAM_LANG_FLAG, FONT_CTX, OBJ_ATTR_BASE=0x8108, TILE_WIDTH_SHIFT=3. Arithmetic (pixel+8)>>3 matches asrs r7,r0,#3.
R7 (callers): 5/5 -- FIXED. form(b): caller `0x080d4de4` (font_jp_080d4de4, CSV tags [vram; font_jp]) matches actual containing function start (BL site 080d4e1c sits inside FUN_080d4de4). Tag string now matches CSV exactly.
R8 (confidence): 5/5 -- high with three independent positive layers: L1 (function body 0x080dbcfc..0x080dbe0c fully static-readable, ~130 instr), L2 (select_charset_then_load_name + text_render_wrapper + commit_line_buffer_to_sprite_vram triple = text-render family fingerprint), L3 (caller font_jp_080d4de4 [vram;font_jp] + font ctx 0x02006ed0 + OBJ_ATTR_BASE 0x8108). Prologue decode correctly identified .hword 0x464f=mov r7,r9 / .hword 0x4646=mov r6,r8 / .hword 0x4680=mov r8,r0 as callee-save spills (post_rewrite_register_side_effect now satisfied).
R9 (zero-tolerance): 5/5 -- ASCII plate, no banned words, no fabricated calls, register classifications correct.
