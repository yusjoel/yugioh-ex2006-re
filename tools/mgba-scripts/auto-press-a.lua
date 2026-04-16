-- auto-press-a.lua
-- 启动后等 120 帧 (~2 秒)，然后按 A 键 5 帧，模拟进入卡牌详情页
local TARGET_FRAME = 120
local pressed = false

callbacks:add("frame", function()
    local f = emu:currentFrame()
    if not pressed and f >= TARGET_FRAME then
        emu:addKey(0)  -- A = bit 0
        pressed = true
    end
    if pressed and f >= TARGET_FRAME + 5 then
        emu:clearKey(0)
        -- 不需要做更多，断点会接管
    end
end)
