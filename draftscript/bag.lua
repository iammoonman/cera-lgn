TakenCount = 0
PickTimerCount = 0
NextBagGUID = nil -- This var is passed from the base red block.
CountToTake = 1
DebouncePickTimer = nil
DebouncePassing = nil
CogworkLibrarian = "ec0d964e-ca2c-4252-8551-cf1916576653"
AgentOfAcquisitions = "19047c4b-0106-455d-ab71-68cabfae7404"
AgentActive = false
LeovoldsOperative = "8fedb2c2-fb13-4af1-b85e-714832562da7"
function onNumberTyped(player_color, number)
    return true
end

function tryRandomize(color)
    return false
end

function onSearchStart(player_color)
    if player_color == "Black" or Player[player_color].host then return end
    local player = Player[player_color]
    player.changeColor("Grey")
    log(player_color .. " tried to search a bag that shouldn't be searched.")
end

function tryObjectEnter(object)
    return object.type == 'Card' or object.type == 'Deck'
end

function onDestroy()
    local pos = self.getPosition()
    for i, _ in ipairs(self.getObjects()) do
        self.takeObject({
            position = { x = (4 * i) + pos["x"], y = pos["y"] + 1, z = pos["z"] }
        })
    end
end

function onSave()
    return JSON.encode({ taken_count = TakenCount, pick_timer = PickTimerCount, next_bag = NextBagGUID, agent_active = AgentActive })
end

function onLoad(state)
    self.createButton({
        click_function = "doNothing",
        function_owner = self,
        label = "0:00",
        position = { x = 0, y = 1, z = 3 },
        scale = { 2, 2, 2 },
        width = 600
    })
    self.createButton({
        click_function = "doNothing",
        function_owner = self,
        label = "0 cards picked",
        position = { x = 0, y = 1, z = 3.5 },
        scale = { 2, 2, 2 },
        width = 800
    })
    local script_state = JSON.decode(state)
    if script_state ~= nil then
        TakenCount = script_state.taken_count
        PickTimerCount = script_state.pick_timer
        NextBagGUID = script_state.next_bag
        AgentActive = script_state.agent_active
        if AgentActive then
            self.createButton({
                click_function = "doAgent",
                function_owner = self,
                label = "Disable Agent",
                position = { x = 0, y = 1, z = 4 },
                scale = { 2, 2, 2 },
                width = 800
            })
        end
    end
end

function onObjectEnterContainer(container, object)
    if container.getGUID() == self.getGUID() then
        if AgentActive then
            local nextBag = getObjectFromGUID(NextBagGUID)
            self.takeObject({ callback_function = function(object) nextBag.putObject(object) end })
        else
            DealCardsToHand()
        end
    end
end

-- These two update the taken counter.
StopCounting = false
function onObjectLeaveZone(zone, obj)
    if zone.type == 'Hand' and obj.type == 'Card' then
        if self.getGMNotes() == zone.getValue() and not AgentActive then
            local HandCards = {}
            for _, ob in ipairs(getObjectsWithTag(self.getTags()[2])) do
                if ob.type == 'Card' then
                    table.insert(HandCards, ob.getGUID())
                end
            end
            if (indexOf(HandCards, obj.getGUID()) == nil or StopCounting) and #HandCards > 0 then
                StopCounting = false
                obj.highlightOff('Red')
                -- Double check that the pack cards are the only thing in the player's hand.
                if #zone.getObjects() ~= #HandCards - 1 then
                    StopCounting = true
                end
                for _, objectInHand in ipairs(zone.getObjects()) do
                    if indexOf(HandCards, objectInHand.getGUID()) == nil then
                        print(self.getGMNotes() ..
                            ", return all cards from your pack to your current hand and remove all other objects.")
                        StopCounting = objectInHand.getGUID() ~= obj.getGUID()
                    end
                end
            end
            if not StopCounting then
                TakenCount = TakenCount + 1
                self.editButton({ index = 1, label = TakenCount .. " cards picked" })
                -- If the player has taken all the cards they needed, pass
                if TakenCount == CountToTake and NextBagGUID ~= nil then
                    if not AgentActive and obj.memo ~= AgentOfAcquisitions then
                        PassCardsFromHand(zone)
                    else
                        AgentActive = true
                        local nextBag = getObjectFromGUID(NextBagGUID)
                        local handObjects = zone.getObjects()
                        group(handObjects)
                        for _i, _v in ipairs(self.getObjects()) do
                            self.takeObject({ callback_function = function(object) nextBag.putObject(object) end })
                        end
                        self.createButton({
                            click_function = "doAgent",
                            function_owner = self,
                            label = "Disable Agent",
                            position = { x = 0, y = 1, z = 4 },
                            scale = { 2, 2, 2 },
                            width = 800
                        })
                    end
                end
            end
        end
    end
    if not AgentActive then
        DealCardsToHand()
    end
end

function onObjectEnterZone(zone, obj)
    if zone.type == 'Hand' and obj.type == 'Card' then
        if self.getGMNotes() == zone.getValue() then
            local HandCards = {}
            local isCogwork = false
            for _, ob in ipairs(getObjectsWithTag(self.getTags()[2])) do
                if ob.type == 'Card' then
                    table.insert(HandCards, ob.getGUID())
                end
            end
            if obj.memo == CogworkLibrarian and not obj.hasTag(self.getTags()[2]) then
                table.insert(HandCards, obj.getGUID())
                obj.addTag(self.getTags()[2])
                isCogwork = true
            end
            if indexOf(HandCards, obj.getGUID()) == nil and #HandCards > 0 then
                obj.highlightOn('Red')
                StopCounting = true
                return
            end
            if not StopCounting then
                TakenCount = TakenCount - 1
                if TakenCount < 0 and not isCogwork then
                    TakenCount = 0
                end
                self.editButton({ index = 1, label = TakenCount .. " cards picked" })
            end
        end
    end
    if zone.type == 'Hand' and obj.type == 'Deck' then
        if self.getGMNotes() == zone.getValue() then
            if #zone.getObjects() > 1 then
                local hand_objects = Player[self.getGMNotes()].getHandObjects(1)
                for _, object in ipairs(hand_objects) do
                    if object.getGUID() == obj.getGUID() then
                        object.setPosition(Vector(0, 10, 0))
                        return
                    end
                end
            end
            obj.setLuaScript("function onObjectLeaveContainer(container, leave_object) if container.type == 'Deck' then leave_object.setTags(container.getTags()) end end")
            obj.addTag(self.getTags()[1] .. self.getGMNotes())
            Wait.frames(function() obj.spread() end, 1)
            -- Start the pick timer.
            if (DebouncePickTimer ~= nil) then Wait.stop(DebouncePickTimer) end
            -- Count seconds
            PickTimerCount = 0
            DebouncePickTimer = Wait.time(function()
                PickTimerCount = PickTimerCount + 1
                local seconds = PickTimerCount % 60
                local minutes = math.floor(PickTimerCount / 60)
                local outString = string.format("%s:", minutes)
                if seconds < 10 then
                    outString = outString .. "0"
                end
                outString = outString .. seconds
                self.editButton({ index = 0, label = outString })
            end, 1, 5999)
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

function doNothing(obj, playerColor, alt_click)
    -- Do Nothing
end

function doAgent(obj, playerColor, alt_click)
    if Player[playerColor].host then
        AgentActive = false
        self.removeButton(2)
    end
end

function SpecialAbilities()
    -- Leovold's Operative
    --  Make an extra pick, then pass the next pack with no picks
    --  Move the "pass" and "pick up pack" processes to their own functions
    --  Add button to the card itself when picked, "Pick two cards from this pack."
    --  State boolean for pass the incoming pack immediately
end

function PassCardsFromHand(zone)
    for _, ob in ipairs(getObjectsWithTag(self.getTags()[2])) do
        if ob.type == 'Card' then
            ob.removeTag(self.getTags()[2])
        end
    end
    local handObjects = zone.getObjects()
    local nextBag = getObjectFromGUID(NextBagGUID)
    if nextBag ~= nil then
        -- Should prevent the counter from counting all the cards being passed.
        StopCounting = true
        Wait.time(function() StopCounting = false end, 0.3)
        for _, o in ipairs(handObjects) do
            o.flip()
        end
        local groupdObj = group(handObjects)
        if #groupdObj == 0 then
            for _, occObj in ipairs(handObjects) do
                if occObj.name == "Card" then
                    nextBag.putObject(occObj)
                end
            end
        else
            nextBag.putObject(groupdObj[1])
        end
        -- Reset the timer and count, since we passed the cards.
        TakenCount = 0
        if (DebouncePickTimer ~= nil) then Wait.stop(DebouncePickTimer) end
    end
end

function DealCardsToHand()
    if DebouncePassing ~= nil then Wait.stop(DebouncePassing) end
    DebouncePassing = Wait.time(function()
        if #Player[self.getGMNotes()].getHandObjects(1) == 0 and #self.getObjects() > 0 then
            TakenCount = 0
            -- Look to onObjectEnterZone for dealing logic
            self.deal(1, self.getGMNotes())
        end
        DebouncePassing = nil
    end, 2)
end
