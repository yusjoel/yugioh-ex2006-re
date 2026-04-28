@echo off
@rem 把 5 个导出目录移到 temp\ 作为 baseline (覆盖旧 baseline), 再清理构建产物.
@rem 同盘符 move 是原子 rename, 不复制字节, 速度无关目录大小.

if not exist temp mkdir temp

for %%D in (data fs fs-decompressed graphics text) do (
    if exist %%D (
        if exist temp\%%D rmdir /s /q temp\%%D
        if errorlevel 1 goto :err
        move %%D temp\ >nul
        if errorlevel 1 goto :err
        echo moved %%D -^> temp\%%D
    )
)

call "%~dp0clean.bat"
goto :ok

:err
echo CLEAN-ALL FAILED
exit /b 1
:ok
echo CLEAN-ALL OK: 5 个导出目录已移到 temp\, 构建产物已清理
