@echo off
@rem 全量重建 + 一致性验证.
@rem 流程: ROM → export_all → build → ROM byte-identical 校验 → temp/ 对比.
@rem 用 NOPAUSE=1 抑制 build.bat 末尾的 pause.

setlocal
set NOPAUSE=1

@rem 1. ROM → data/*.s + fs/* + fs-decompressed/* + graphics/* + text/*
@rem    (export_all 内含 decode→encode 闭环, 见 Step 4/5)
python tools\rom-export\export_all.py
if errorlevel 1 goto :err

@rem 2. data/*.s → output/2343.gba
call "%~dp0build.bat"
if errorlevel 1 goto :err

@rem 3. ROM byte-identical 校验 (output\2343.gba == roms\2343.gba)
echo.
echo ============================================================
echo   ROM byte-identical 校验
echo ============================================================
fc /b roms\2343.gba output\2343.gba >nul
if errorlevel 1 (
    echo [FAIL] output\2343.gba 与 roms\2343.gba 不一致
    goto :err
)
echo [OK] output\2343.gba == roms\2343.gba

@rem 4. round-trip 校验: temp\^<dir^> vs ./^<dir^> (clean-all 后 build-all 双跑)
python tools\rom-export\verify_against_temp.py
if errorlevel 1 goto :err

echo.
echo BUILD-ALL OK
endlocal
exit /b 0

:err
echo.
echo BUILD-ALL FAILED
endlocal
exit /b 1
