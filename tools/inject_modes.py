#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inject_modes.py
向 all.s 中注入 .thumb / .arm 指令集切换指令，
并为 Thumb-1 数据处理指令补全 s 后缀（符合 GAS .syntax unified 要求）。

检测规则（基于每行注释中的 hex bytes）：
  - 4 个 hex 字符 (2 字节)                 → THUMB 指令
  - 8 个 hex 字符 (4 字节)，且
    first_hw & 0xF800 == 0xF000 AND
    second_hw & 0xF800 in {0xF800, 0xE800} → THUMB BL/BLX (ARMv4T)
  - 其余 8 个 hex 字符 (4 字节)            → ARM 指令
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 正则
# ---------------------------------------------------------------------------

# 匹配带注释的指令/数据行：  <空白><助记符><操作数>  @ <地址8位> <hex字节>
INSTR_RE = re.compile(
    r'^(\s+)(\S+)(.*?)\s+@\s+[0-9a-f]{8}\s+([0-9a-f]+)\s*$'
)

# 数据伪指令，不参与模式或 s-suffix 处理
DATA_DIRECTIVES = {
    '.word', '.hword', '.byte', '.short', '.space',
    '.string', '.ascii', '.asciz',
}

# ---------------------------------------------------------------------------
# Thumb s-suffix 规则
# ---------------------------------------------------------------------------

# 这些指令在 Thumb-1 中只有设标志（S）的编码，必须加 s
ALWAYS_S = frozenset({
    'adc', 'and', 'asr', 'bic', 'eor',
    'lsl', 'lsr', 'mul', 'mvn', 'orr',
    'ror', 'sbc',
})

# 高寄存器（r8-r15 及别名）
HIGH_REGS = frozenset({
    'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15',
    'sp', 'lr', 'pc',
})

# sp/pc 相关的 add/sub 不设标志
SP_PC = frozenset({'sp', 'r13', 'pc', 'r15'})


def operand_regs(operands_str: str):
    """从操作数字符串中提取寄存器名列表（小写）。"""
    parts = [p.strip().lower() for p in operands_str.split(',')]
    regs = []
    for p in parts:
        p = p.strip('[]!{}')
        if re.match(r'^r\d+$|^sp$|^lr$|^pc$|^ip$|^fp$|^sl$|^sb$', p):
            regs.append(p)
    return regs


def needs_s_suffix(mnemonic: str, operands_str: str) -> bool:
    """判断 Thumb 模式下该指令是否需要补加 s 后缀。"""
    m = mnemonic.lower()

    if m in ALWAYS_S:
        return True

    if m == 'rsb':
        return True  # rsb → rsbs ...,#0 (另行处理操作数)

    if m == 'mov':
        regs = operand_regs(operands_str)
        # mov 含高寄存器（MOV Rd,Rs 形式）→ 不设标志
        for r in regs:
            if r in HIGH_REGS:
                return False
        return True  # mov Rd,#imm 或 low→low → movs

    if m == 'add':
        regs = operand_regs(operands_str)
        # add sp,... / add ...,sp / add ...,pc → 不设标志
        if regs and regs[0] in SP_PC:
            return False
        if len(regs) >= 2 and regs[1] in SP_PC:
            return False
        # 含高寄存器 → 不设标志
        for r in regs:
            if r in HIGH_REGS:
                return False
        return True

    if m == 'sub':
        regs = operand_regs(operands_str)
        if regs and regs[0] in SP_PC:
            return False
        return True

    return False


def fix_rsb_operands(operands_str: str) -> str:
    """rsb r1,r1 → 操作数加 ,#0（如果还没有 #0）"""
    if '#' not in operands_str:
        return operands_str.rstrip() + ',#0'
    return operands_str


# ---------------------------------------------------------------------------
# 模式检测
# ---------------------------------------------------------------------------

def detect_mode(hex_str: str):
    """从注释 hex bytes 判断 ARM/THUMB。无法判断返回 None。"""
    h = hex_str.strip()
    if len(h) == 4:
        return 'thumb'
    elif len(h) == 8:
        b0 = int(h[0:2], 16)
        b1 = int(h[2:4], 16)
        b2 = int(h[4:6], 16)
        b3 = int(h[6:8], 16)
        first_hw  = (b1 << 8) | b0
        second_hw = (b3 << 8) | b2
        # ARMv4T Thumb BL：first_hw[15:11]==11110, second_hw[15:11]==11111
        # ARMv5T Thumb BLX：second_hw[15:11]==11101
        if (first_hw  & 0xF800) == 0xF000 and \
           (second_hw & 0xF800) in (0xF800, 0xE800):
            return 'thumb'
        return 'arm'
    return None


# ---------------------------------------------------------------------------
# 主处理
# ---------------------------------------------------------------------------

def process(input_path: Path, output_path: Path):
    current_mode = 'arm'  # rom.s 进入时已是 .arm
    injected_modes = 0
    fixed_s = 0

    with input_path.open('r', encoding='utf-8') as fin, \
         output_path.open('w', encoding='utf-8') as fout:

        for lineno, line in enumerate(fin, 1):
            m = INSTR_RE.match(line)
            if m:
                indent    = m.group(1)
                mnemonic  = m.group(2)
                operands  = m.group(3)
                hex_bytes = m.group(4)
                mn_lower  = mnemonic.lower()

                if mn_lower not in DATA_DIRECTIVES:
                    # 1. 检测并注入模式切换
                    mode = detect_mode(hex_bytes)
                    if mode and mode != current_mode:
                        fout.write('.thumb\n' if mode == 'thumb' else '.arm\n')
                        current_mode = mode
                        injected_modes += 1

                    # 2. Thumb 模式下：检测 Ghidra 拆分的孤立 BL/BLX 半字
                    #    Ghidra 有时把 ARMv4T Thumb BL（4字节）的两个半字分别反汇编，
                    #    第一个半字显示为 "bl #addr" 带 2-byte 注释。
                    #    GAS 会把 bl 汇编成完整 4 字节，造成 +2 字节偏移。
                    #    解决：将孤立 BL/BLX 半字替换为 .hword 原始数据。
                    if current_mode == 'thumb' and mn_lower in ('bl', 'blx') \
                            and len(hex_bytes) == 4:
                        b0 = int(hex_bytes[0:2], 16)
                        b1 = int(hex_bytes[2:4], 16)
                        hword_val = (b1 << 8) | b0  # 小端半字
                        full_comment = line[line.index('@'):]
                        line = indent + f'.hword 0x{hword_val:04x}' + \
                               '    @ ' + full_comment.split('@ ', 1)[1]
                        fixed_s += 1  # 复用计数器

                    # 3a. Thumb MOV 高寄存器操作格式（字节高位 = 0x46）
                    #     GAS 拒绝 mov Rd,Rs（两个低寄存器）使用高寄存器操作格式，
                    #     但原始 ROM 可能使用此格式。直接输出 .hword 保持字节一致。
                    elif current_mode == 'thumb' and mn_lower == 'mov' \
                            and len(hex_bytes) == 4 \
                            and int(hex_bytes[2:4], 16) == 0x46:
                        b0 = int(hex_bytes[0:2], 16)
                        b1 = int(hex_bytes[2:4], 16)
                        hword_val = (b1 << 8) | b0
                        full_comment = line[line.index('@'):]
                        line = indent + f'.hword 0x{hword_val:04x}' + \
                               '    @ ' + full_comment.split('@ ', 1)[1]
                        fixed_s += 1

                    # 3b. Thumb 模式下补全 s 后缀
                    elif current_mode == 'thumb' and not mnemonic.lower().endswith('s'):
                        if needs_s_suffix(mn_lower, operands):
                            if mn_lower == 'rsb':
                                operands = fix_rsb_operands(operands)
                            mnemonic = mnemonic + 's'
                            fixed_s += 1
                            full_comment = line[line.index('@'):]
                            line = indent + mnemonic + operands + \
                                   '    @ ' + full_comment.split('@ ', 1)[1]

            fout.write(line)

            if lineno % 500_000 == 0:
                print(f'  {lineno:,} 行，注入模式 {injected_modes}，修复s后缀 {fixed_s}...')

    return injected_modes, fixed_s


if __name__ == '__main__':
    src = Path('asm/all.s')
    tmp = Path('asm/all.s.tmp')

    if not src.exists():
        print(f'错误：找不到 {src}')
        sys.exit(1)

    print(f'开始处理 {src} ...')
    modes, fixed = process(src, tmp)
    print(f'完成！注入 {modes} 处模式切换，修复 {fixed} 处 s 后缀')

    tmp.replace(src)
    print(f'已写回 {src}')

    # ---------------------------------------------------------------------------
    # 手动补丁：无法用通用规则处理的特殊指令
    # ---------------------------------------------------------------------------
    content = src.read_text(encoding='utf-8').splitlines(keepends=True)
    patches = 0

    for i, line in enumerate(content):
        # adr r10,0x810e204 → sub r10,pc,#4（GAS 无法对绝对地址做 PC-relative 引用）
        if 'adr r10,0x810e204' in line:
            content[i] = line.replace('adr r10,0x810e204', 'sub r10,pc,#4   @', 1)
            patches += 1
        # adds r4,r4,#0x4 @ 0809fb20 241d → .hword 0x1d24（3-operand 编码，GAS 生成2-operand）
        elif 'adds r4,r4,#0x4' in line and '0809fb20' in line and '241d' in line:
            content[i] = line.replace('adds r4,r4,#0x4', '.hword 0x1d24 @', 1)
            patches += 1
        # bx r11 @ 087e0bc4 5e47 → .hword 0x475e（原始编译器未清零 SBZ 位）
        elif 'bx r11' in line and '087e0bc4' in line and '5e47' in line:
            import re as _re
            content[i] = _re.sub(r'(\s+)bx r11(\s+)', r'\1.hword 0x475e\2', line, count=1)
            patches += 1

    if patches:
        src.write_text(''.join(content), encoding='utf-8')
        print(f'已应用 {patches} 处手动补丁')
