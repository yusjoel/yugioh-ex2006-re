# -*- coding: utf-8 -*-
#@runtime Jython
#@category Ygo-ex2006
# RefineF04Seg10PlateFix.py -- fix residual FUN_0808e5c4 tokens in Seg-10 plates
# (not in original proposal list; found in post-land grep)

from ghidra.program.model.listing import CodeUnit

DRY = False
try:
    _a = list(getScriptArgs())
    if _a and _a[0].lower() in ("dry", "--dry", "1", "true"):
        DRY = True
except Exception:
    pass

def _addr(x):
    return toAddr(x)

def _plate(fn_addr, fn_name, replacements):
    listing = currentProgram.getListing()
    addr = _addr(fn_addr)
    cu = listing.getCodeUnitAt(addr)
    if cu is None:
        print("  WARN PLATE no code unit @ 0x%08x (%s)" % (fn_addr, fn_name))
        return
    old = cu.getComment(CodeUnit.PLATE_COMMENT)
    if old is None:
        old = ""
    new = old
    warns = 0
    for old_tok, new_tok in replacements:
        if old_tok not in new:
            print("  WARN PLATE 0x%08x (%s): token '%s' not found" % (fn_addr, fn_name, old_tok))
            warns += 1
        else:
            new = new.replace(old_tok, new_tok)
    if new == old and warns == 0:
        print("  WARN PLATE no-change @ 0x%08x (%s)" % (fn_addr, fn_name))
        return
    if not DRY:
        try:
            listing.setComment(addr, CodeUnit.PLATE_COMMENT, new)
            print("  PLATE OK 0x%08x (%s) -- %d tokens, %d warns" % (
                fn_addr, fn_name, len(replacements) - warns, warns))
        except Exception as e:
            print("  WARN PLATE set @ 0x%08x: %s" % (fn_addr, e))
    else:
        print("  DRY PLATE 0x%08x (%s) -- %d tokens, %d warns" % (
            fn_addr, fn_name, len(replacements), warns))

FIXES = [
    (0x080486b0, 'enqueue_sprite_attr_by_sign', [
        ('FUN_0808e5c4', '0x0808e5c4'),
    ]),
    (0x08048750, 'enqueue_sprite_attr_clamped', [
        ('FUN_0808e5c4', '0x0808e5c4'),
    ]),
]

print("=== RefineF04Seg10PlateFix (DRY=%s) ===" % DRY)
total_warns = 0
for fn_addr, fn_name, replacements in FIXES:
    _plate(fn_addr, fn_name, replacements)
print("=== Done ===")
