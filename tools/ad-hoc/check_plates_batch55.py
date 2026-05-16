# -*- coding: utf-8 -*-
import unicodedata

plates = [
    ('080431f4', u'由 scan_equip_zone_for_super_rejuvenation_activation (0x0809d374) 在确认装备激活通过后调用. 入口保存 r0=player_id->r4, r1=slot_idx->r5, r2=idx->r7, r3=type_flag->r6. 调用 check_node_in_slot_chain(r4, r5, r7, r6); 若链中存在节点: 根据 r4(player) 选择 OAM attr 高位 (0x37/0x8037), 将 r5/r6 的 bit 域打包进 r1/r2/r3, 调用 enqueue_sprite_attr_record 将精灵属性提交到 OAM 缓冲. 若不存在直接跳过. 副作用: OAM 精灵属性缓冲 (via enqueue_sprite_attr_record). Constants: OAM_P0=0x37, OAM_P1=0x8037.'),
]

# just check for non-ASCII non-CJK chars
for addr, plate in plates:
    bad = []
    for ch in plate:
        cp = ord(ch)
        if cp > 127:
            cat = unicodedata.category(ch)
            name = unicodedata.name(ch, 'UNKNOWN')
            if 'CJK' not in name and cat not in ('Lo', 'Ll', 'Lu', 'Lt', 'Lm'):
                bad.append((hex(cp), ch, cat, name))
    if bad:
        print('%s: BAD: %s' % (addr, bad))
    else:
        print('%s: OK' % addr)
