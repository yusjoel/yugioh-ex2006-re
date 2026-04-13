# 项目规范

## 项目概述

这是一个 GBA ROM 反汇编项目，目标游戏为《游戏王 EX2006》(2343.gba)。

## 工具链

- **反汇编工具**: devkitARM
- **安装路径**: 见 `LOCAL.md`（各机器路径不同）

## PowerShell 配置

- **推荐版本**: PowerShell 7.5.4
- **可执行文件路径**: 见 `LOCAL.md`（各机器路径不同）
- **说明**: 系统自带的 PowerShell 版本较低，建议使用 PowerShell 7 版本执行脚本

## 目标文件

- **ROM 文件**: `2343.gba` (32MB)
- **ROM 基址**: `0x08000000` (GBA 标准)

## 项目目录结构

```
.
├── asm/                    # 汇编代码目录
│   ├── rom.s               # 主汇编文件
│   ├── rom_header.s        # ROM 头部定义
│   └── crt0.s              # 启动代码
├── constants/              # 常量定义目录
│   └── gba_constants.inc   # GBA 硬件寄存器常量
├── data/                   # 数据目录
│   └── (存放数据表等)
├── include/                # 头文件目录
│   └── macros.inc          # 汇编宏定义
├── build.bat               # 构建脚本
├── disassemble.bat         # 反汇编脚本
├── ld_script.txt           # 链接器脚本
└── .gitignore              # Git 忽略配置
```

### 汇编文件说明

| 文件 | 地址范围 | 说明 |
|------|----------|------|
| `rom_header.s` | 0x000 - 0x0BF | ROM 头部，包含跳转指令、Logo、游戏标题等 |
| `crt0.s` | 0x0C0 - 0x0FF | 启动代码，负责初始化系统、设置堆栈 |
| `rom.s` | 0x000 - 0x1FFFF00 | 主文件，使用 `.include` 包含 header 和 crt0，其余使用 incbin 载入 |

**注意**: ROM 实际大小为 `0x1FFFF00` (33554176 字节)，构建时需使用正确的长度。

## 构建脚本

### build.bat

构建 ROM 的脚本，使用 devkitARM 工具链。

```batch
build.bat
```

构建流程：
1. 汇编 `asm/rom.s` -> `rom.o`
2. 链接 `rom.o` -> `2343.elf`
3. 转换 `2343.elf` -> `2343.gba`
4. 校验生成的 ROM 与 `baserom.gba` 的差异

### disassemble.bat

反汇编脚本，使用 objdump 生成汇编代码。

```batch
disassemble.bat
```

输出: `2343.asm`

## 使用提示

- GBA ROM 使用混合指令集：大部分是 THUMB (16位)，部分启动代码和特定函数使用 ARM (32位)
- ROM 入口点通常在 `0x080000C0`
- 构建前确保已安装 devkitARM 并正确配置路径

## 语言偏好

- **交流语言**: 简体中文
- **文档语言**: 简体中文
- **代码注释**: 简体中文

所有生成的文档、代码注释都应使用简体中文编写。
