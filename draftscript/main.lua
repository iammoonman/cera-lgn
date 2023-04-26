mod_name, version = 'Dawnglare', 1.002
function onload(state)
    WebRequest.get('https://raw.githubusercontent.com/iammoonman/cera/master/draftscript/main.lua', self,
        'GetFreshVersion')
    LocalBounds = self.getBounds()
    self.createButton({
        label = "Create Bags",
        click_function = "onClickGetBags",
        function_owner = self,
        width = 680,
        rotation = { -90, 0, 0 },
        position = { x = 0, y = -LocalBounds.size.y / 4, z = LocalBounds.size.z / 2 }
    })
    self.createButton({
        label = "Reverse Order",
        click_function = "onClickReverse",
        function_owner = self,
        width = 680,
        rotation = { 0, 0, 0 },
        position = { x = 0, y = LocalBounds.size.y / 2, z = 0.3 }
    })
    self.createButton({
        label = "Highlight Bags",
        click_function = "onClickHighlightBags",
        function_owner = self,
        width = 680,
        rotation = { -90, 0, 0 },
        position = { x = 0, y = LocalBounds.size.y / 4, z = LocalBounds.size.z / 2 }
    })
    self.createButton({
        label = "Destroy Bags",
        click_function = "onClickDestroyBags",
        function_owner = self,
        width = 680,
        rotation = { 0, 0, 180 },
        position = { x = 0, y = -LocalBounds.size.y / 2, z = 0 }
    })
    self.createButton({
        label = "1",
        click_function = "onClickChangeTaken",
        function_owner = self,
        width = 400,
        rotation = { 0, 0, 0 },
        position = { x = 0, y = LocalBounds.size.y / 2, z = -0.3 }
    })
    if not self.hasAnyTag() then self.addTag(self.getGUID()) end
    UpdateVariables()
end

CardsTaken = 1
TurnsReverseOrder = true
UnbelievablyRedundantManualTurnOrder = {
    'Orange',
    'Red',
    'Brown',
    'White',
    'Pink',
    'Purple',
    'Blue',
    'Teal',
    'Green',
    'Yellow',
}

function onClickReverse()
    TurnsReverseOrder = not TurnsReverseOrder
    local direction = "Right"
    if TurnsReverseOrder then
        direction = "Left"
    end
    UnbelievablyRedundantManualTurnOrder = array_reverse(UnbelievablyRedundantManualTurnOrder)
    self.editButton({ index = 1, label = "Now Passing " .. direction, width = 850 })
    UpdateVariables()
end

function onClickChangeTaken(obj, color, alt)
    -- Race Condition
    local tab = {
        [1] = function() if alt then CardsTaken = 1 else CardsTaken = 2 end end,
        [2] = function() if alt then CardsTaken = 1 else CardsTaken = 3 end end,
        [3] = function() if alt then CardsTaken = 2 else CardsTaken = 3 end end
    }
    tab[CardsTaken]()
    obj.editButton({ index = 4, label = CardsTaken, width = 400 })
    UpdateVariables()
end

function onClickHighlightBags()
    local length = 0
    -- local ActiveBags = {}
    for _, ob in ipairs(getObjects()) do
        if ob.hasTag(self.getTags()[1]) then
            length = length + 1
            ob.highlightOn('White', 3)
        end
    end
    log(length .. " bag(s).")
end

function onClickGetBags()
    -- Find existing bags
    local ActiveBags = {}
    for _, ob in ipairs(getObjectsWithTag(self.getTags()[1])) do
        local tint = ob.getColorTint()
        if tint.r == 0.956 and tint.g == 0.392 and tint.b == 0.113 and tint.a == 1 then
            table.insert(ActiveBags, 'Orange')
        end
        if tint.r == 0.856 and tint.g == 0.1 and tint.b == 0.094 and tint.a == 1 then
            table.insert(ActiveBags, 'Red')
        end
        if tint.r == 0.443 and tint.g == 0.231 and tint.b == 0.09 and tint.a == 1 then
            table.insert(ActiveBags, 'Brown')
        end
        if tint.r == 1 and tint.g == 1 and tint.b == 1 and tint.a == 1 then
            table.insert(ActiveBags, 'White')
        end
        if tint.r == 0.96 and tint.g == 0.439 and tint.b == 0.807 and tint.a == 1 then
            table.insert(ActiveBags, 'Pink')
        end
        if tint.r == 0.627 and tint.g == 0.125 and tint.b == 0.941 and tint.a == 1 then
            table.insert(ActiveBags, 'Purple')
        end
        if tint.r == 0.118 and tint.g == 0.53 and tint.b == 1 and tint.a == 1 then
            table.insert(ActiveBags, 'Blue')
        end
        if tint.r == 0.129 and tint.g == 0.694 and tint.b == 0.607 and tint.a == 1 then
            table.insert(ActiveBags, 'Teal')
        end
        if tint.r == 0.192 and tint.g == 0.701 and tint.b == 0.168 and tint.a == 1 then
            table.insert(ActiveBags, 'Green')
        end
        if tint.r == 0.905 and tint.g == 0.898 and tint.b == 0.172 and tint.a == 1 then
            table.insert(ActiveBags, 'Yellow')
        end
    end
    -- Create new bags
    for player_index, player in ipairs(Player.getPlayers()) do
        if player.color ~= 'Grey' and player.color ~= 'Black' and indexOf(ActiveBags, player.color) == nil then
            -- Give player a bag and put it into the table
            local pos = self.getPosition()
            local rot = self.getRotation()
            Wait.time(function()
                local NewBag = spawnObjectData({
                    data = {
                        Name = "Bag",
                        Transform = { posX = 0, posY = 0, pozZ = 0, rotX = 0, rotY = 0, rotZ = 0, scaleX = 1, scaleY = 1, scaleZ = 1 },
                        Nickname = player.color .. "'s bag.",
                        Description = "Don't take cards out of me!",
                        GMNotes = player.color,
                        AltLookAngle = { x = 0, y = 0, z = 0 },
                        ColorDiffuse = { r = 0, g = 0, b = 0, a = 1 },
                        LayoutGroupSortIndex = 0,
                        Value = 0,
                        Locked = false,
                        Grid = true,
                        Snap = true,
                        IgnoreFoW = false,
                        MeasureMovement = false,
                        DragSelectable = true,
                        Autoraise = true,
                        Sticky = true,
                        Tooltip = true,
                        GridProjection = false,
                        HideWhenFaceDown = false,
                        Hands = false,
                        MaterialIndex = -1,
                        MeshIndex = -1,
                        Number = 0,
                        XmlUI = "",
                        Bag = { Order = 1 },
                        LuaScript = [[
                                function onLoad()
                                    WebRequest.get('https://raw.githubusercontent.com/iammoonman/cera/master/draftscript/bag.lua',self,'GetFreshScript')
                                end
                                function GetFreshScript (wr)
                                    self.setLuaScript(wr.text)
                                    self.reload()
                                end
                                ]],
                        LuaScriptState = "",
                        ContainedObjects = {},
                    },
                    position = { x = pos['x'] + player_index * 4, y = pos['y'], z = pos['z'] },
                    rotation = rot,
                    scale = { 1, 1, 1 },
                })
                NewBag.setColorTint(player.color)
                NewBag.addTag(self.getTags()[1] .. player.color)
                NewBag.addTag(self.getTags()[1])
            end, player_index / 3)
        end
    end
    UpdateVariables()
end

function doNothing(obj, playerColor, alt_click)
end

function onClickDestroyBags()
    for _, ob in ipairs(getObjects()) do
        if ob.hasTag(self.getTags()[1]) then
            destroyObject(ob)
        end
    end
end

function indexOf(array, value)
    for i, v in ipairs(array) do
        if v == value then
            return i
        end
    end
    return nil
end

function array_reverse(x)
    local n, m = #x, #x / 2
    for i = 1, m do
        x[i], x[n - i + 1] = x[n - i + 1], x[i]
    end
    return x
end

function onObjectDestroy(object)
    UpdateVariables()
    return false
end

function UpdateVariables()
    Wait.time(function()
        local ActiveBags = {}
        for _, ob in ipairs(getObjects()) do
            if ob.hasTag(self.getTags()[1]) and ob.type == 'Bag' then
                table.insert(ActiveBags, ob)
            end
        end
        for _, o in ipairs(ActiveBags) do
            -- local obj = getObjectFromGUID(o)
            -- Get next color's bag GUID
            local thisColor = o.getGMNotes()
            -- Consider validating this against playerColor. May reduce griefing if its only this color or black.
            local myIndex = indexOf(UnbelievablyRedundantManualTurnOrder, thisColor)
            local minDiff = 999
            local leastNegative = 0
            local wrapColorBagGUID = ActiveBags[1]
            local nextColorBagGUID = nil
            -- Find both the lowest negative AKA the first bag in the list
            -- and the lowest positive AKA the next bag in the list
            for _, bg in ipairs(ActiveBags) do
                local diffVal = myIndex - indexOf(UnbelievablyRedundantManualTurnOrder, bg.getGMNotes())
                if (diffVal > 0) then
                    if diffVal < minDiff then
                        minDiff = diffVal
                        nextColorBagGUID = bg
                    end
                end
                if (diffVal < 0) then
                    if diffVal < leastNegative then
                        leastNegative = diffVal
                        wrapColorBagGUID = bg
                    end
                end
            end
            -- If the next postitive bag doesn't exist, wrap the list.
            if nextColorBagGUID == nil then
                nextColorBagGUID = wrapColorBagGUID
            end
            o.setVar('NextBagGUID', nextColorBagGUID.getGUID())
            o.setVar('CountToTake', CardsTaken)
        end
        return false
    end, 1, 4)
end

function GetFreshVersion(wr)
    local v = wr.text:match('mod_name, version = \'Dawnglare\', (%d+%p%d+)')
    log('GITHUB Version ' .. v)
    if v then v = tonumber(v) else v = version end
    if version < v then
        self.setLuaScript(wr.text)
        self.reload()
    end
end
