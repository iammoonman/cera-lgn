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
OperativePacksToPass = 0
DebounceSkipping = nil
TrackerTag = ''
ThisColor = self.getGMNotes()

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
        self.takeObject({ position = { x = (4 * i) + pos["x"], y = pos["y"] + 1, z = pos["z"] } })
    end
end

function onSave()
    return JSON.encode({ taken_count = TakenCount, pick_timer = PickTimerCount, next_bag = NextBagGUID, agent_active = AgentActive, packs_to_pass = OperativePacksToPass })
end

function onLoad(state)
    TrackerTag = self.getTags()[1] .. self.getGMNotes()
    self.createButton({ click_function = "doNothing", function_owner = self, label = "0:00", position = { x = 0, y = 1, z = 3 }, scale = { 2, 2, 2 }, width = 600 })
    self.createButton({ click_function = "doNothing", function_owner = self, label = "0 cards picked", position = { x = 0, y = 1, z = 3.5 }, scale = { 2, 2, 2 }, width = 800 })
    local script_state = JSON.decode(state)
    if script_state ~= nil then
        TakenCount = script_state.taken_count
        PickTimerCount = script_state.pick_timer
        NextBagGUID = script_state.next_bag
        AgentActive = script_state.agent_active
        if AgentActive then self.createButton({ click_function = "doAgent", function_owner = self, label = "Disable Agent", position = { x = 0, y = 1, z = 4 }, scale = { 2, 2, 2 }, width = 800 }) end
        OperativePacksToPass = script_state.packs_to_pass
        if OperativePacksToPass > 0 then
            if DebounceSkipping ~= nil then Wait.stop(DebounceSkipping) end
            DebounceSkipping = Wait.time(SkipPack, 1, OperativePacksToPass)
        end
    end
end

function onObjectEnterContainer(container, object)
    if container.getGUID() == self.getGUID() then
        if #self.getObjects() == 1 then
            if AgentActive or OperativePacksToPass > 0 then
                if DebounceSkipping ~= nil then Wait.stop(DebounceSkipping) end
                DebounceSkipping = Wait.time(SkipPack, 1, OperativePacksToPass)
            else
                DealCardsToHand()
            end
        end
    end
end

-- These two update the taken counter.
function onObjectLeaveZone(zone, obj)
    if ThisColor ~= zone.getValue() then return end
    if zone.type == 'Hand' and obj.type == 'Card' then
        if not AgentActive then
            local StopCounting = false
            local isOperative = obj.memo == LeovoldsOperative and not obj.hasTag(TrackerTag) and obj.getGMNotes() == 'operative_used'
            local operativeInHand = false
            for _, objectInHand in ipairs(zone.getObjects()) do
                if objectInHand.getGMNotes() == 'operative_used' then
                    operativeInHand = true
                    print(ThisColor .. ", remove the used Leovold's Operative from your hand. Return all other cards from this pack to it and pick once.")
                end
                if not objectInHand.hasTag(TrackerTag) then StopCounting = true end
            end
            if not isOperative and obj.hasTag(TrackerTag) then TakenCount = TakenCount + 1 end
            self.editButton({ index = 1, label = TakenCount .. " cards picked" })
            if StopCounting then return end
            -- If the player has taken all the cards they needed, pass
            if TakenCount == (CountToTake + OperativePacksToPass) and NextBagGUID ~= nil then
                if not AgentActive and obj.memo ~= AgentOfAcquisitions and not operativeInHand then
                    PassCardsFromHand(zone)
                else
                    AgentActive = true
                    group(zone.getObjects())
                    if DebounceSkipping ~= nil then Wait.stop(DebounceSkipping) end
                    DebounceSkipping = Wait.time(SkipPack, 1, #self.getObjects())
                    self.createButton({ click_function = "doAgent", function_owner = self, label = "Disable Agent", position = { x = 0, y = 1, z = 4 }, scale = { 2, 2, 2 }, width = 800 })
                end
                -- Stop the pick timer.
                if (DebouncePickTimer ~= nil) then Wait.stop(DebouncePickTimer) end
                PickTimerCount = 0
            end
            DealCardsToHand()
        end
        obj.highlightOff('Red')
    end
end

function onObjectEnterZone(zone, obj)
    if ThisColor ~= zone.getValue() then return end
    if zone.type == 'Hand' and obj.type == 'Card' then
        if (obj.hasTag(TrackerTag)) then
            TakenCount = TakenCount - 1
            if TakenCount < 0 then TakenCount = 0 end
            self.editButton({ index = 1, label = TakenCount .. " cards picked" })
        else
            local isOperative = false
            local isCogwork = false
            if obj.memo == LeovoldsOperative and obj.getGMNotes() ~= 'operative_used' then
                isOperative = true
                OperativePacksToPass = OperativePacksToPass + 1
                obj.setGMNotes('operative_used')
                print(ThisColor .. ", you have used a Leovold's Operative. Please remove it from your hand. You will pass the next " .. OperativePacksToPass .. " packs.")
            end
            if obj.memo == CogworkLibrarian then
                obj.addTag(TrackerTag)
                isCogwork = true
                print(ThisColor .. ", you have used a Cogwork Librarian. You may make an additional pick from this pack.")
            end
            if not isOperative and not isCogwork then
                -- Kind of a reminder to the player that the draft is still going.
                obj.highlightOn('Red', 15)
                print(ThisColor .. ", return all cards from your pack to your current hand and remove all other objects. If this is the last card in the pack, ignore this message.")
            end
            if isCogwork then
                if not isOperative then TakenCount = TakenCount - 1 end
                if TakenCount < 0 and not isCogwork then TakenCount = 0 end
                self.editButton({ index = 1, label = TakenCount .. " cards picked" })
            end
        end
    end
    if zone.type == 'Hand' and obj.type == 'Deck' then
        if #zone.getObjects() > 1 then
            obj.highlightOn('Red')
            print(self.getGMNotes() .. ", take the deck of cards out of your hand before proceeding.")
            return
        end
        obj.setLuaScript("function onObjectLeaveContainer(container, leave_object) if container.type == 'Deck' then leave_object.setTags(container.getTags()) end end")
        obj.addTag(TrackerTag)
        Wait.frames(function() obj.spread() end, 5)
        -- Start the pick timer.
        if (DebouncePickTimer ~= nil) then Wait.stop(DebouncePickTimer) end
        -- Count seconds
        PickTimerCount = 0
        DebouncePickTimer = Wait.time(function()
            PickTimerCount = PickTimerCount + 1
            local seconds = PickTimerCount % 60
            local minutes = math.floor(PickTimerCount / 60)
            local outString = string.format("%s:", minutes)
            if seconds < 10 then outString = outString .. "0" end
            outString = outString .. seconds
            self.editButton({ index = 0, label = outString })
            if PickTimerCount % 60 == 0 and PickTimerCount ~= 0 then printToColor("Pick time: " .. outString, ThisColor) end
        end, 1, 5999)
    end
end

function indexOf(array, value)
    for i, v in ipairs(array) do if v == value then return i end end
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

function PassCardsFromHand(zone)
    for _, ob in ipairs(getObjectsWithTag(TrackerTag)) do if ob.type == 'Card' then ob.removeTag(TrackerTag) end end
    local handObjects = zone.getObjects()
    local nextBag = getObjectFromGUID(NextBagGUID)
    if nextBag ~= nil then
        -- Should prevent the counter from counting all the cards being passed.
        if #handObjects == 1 then
            nextBag.putObject(handObjects[1])
        elseif #handObjects > 1 then
            local groupdObj = group(handObjects)
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
        if #Player[ThisColor].getHandObjects(1) == 0 and #self.getObjects() > 0 then
            TakenCount = 0
            -- Look to onObjectEnterZone for dealing logic
            self.deal(1, ThisColor)
        end
    end, 1)
end

function SkipPack()
    if #self.getObjects() == 0 then return end
    if OperativePacksToPass > 0 then
        OperativePacksToPass = OperativePacksToPass - 1
        local nextBag = getObjectFromGUID(NextBagGUID)
        self.takeObject({ callback_function = function(object) nextBag.putObject(object) end })
        print(ThisColor .. " has skipped a pack for Leovold's Operative. " .. OperativePacksToPass .. " skipped packs remaining.")
        return
    end
    if AgentActive then
        local nextBag = getObjectFromGUID(NextBagGUID)
        self.takeObject({ callback_function = function(object) nextBag.putObject(object) end })
    end
end
