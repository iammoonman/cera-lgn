TakenCount = 0 -- Will break if the user saves the game in between the take card and pass card function calls
TimerCount = 0
NextBagGUID = nil -- This var is passed from the base red block.
CountToTake = 1
TimerIsCounting = false
DraftCardsTaken = {}
function onNumberTyped(player_color, number)
    return true
end

function tryRandomize(color)
    return false
end

function onSearchStart(player_color)
    if player_color == "Black" then return end
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
        -- Zone.getObjects() returns {Object, ...}
        self.takeObject({
            position = { x = (4 * i) + pos["x"], y = pos["y"] + 1, z = pos["z"] }
        })
    end
end

function onLoad()
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
    -- Count seconds
    Wait.time(function()
        if not TimerIsCounting then return end
        TimerCount = TimerCount + 1
        local seconds = TimerCount % 60
        local minutes = math.floor(TimerCount / 60)
        local outString = string.format("%s:", minutes)
        if seconds < 10 then
            outString = outString .. "0"
        end
        outString = outString .. seconds
        self.editButton({ index = 0, label = outString })
    end, 1, 5999)
end

DebounceTimer = nil
function onObjectEnterContainer(container, object)
    if container.getGUID() == self.getGUID() then
        if DebounceTimer ~= nil then Wait.stop(DebounceTimer) end
        DebounceTimer = Wait.time(function()
            if #Player[self.getGMNotes()].getHandObjects(1) == 0 and #self.getObjects() > 0 then
                TakenCount = 0
                -- Deal the cards from the stack dealt and add the right tags
                for _, j in ipairs(self.dealToColorWithOffset(Vector(0, 0, 0), true, self.getGMNotes()).spread()) do
                    Wait.time(j.addTag(self.getTags()[1] .. self.getGMNotes()), 1)
                end
                TimerCount = 0
                -- Start the pick timer.
                TimerIsCounting = true
            end
            DebounceTimer = nil
        end, 2)
    end
end

-- These two update the taken counter.
StopCounting = false
function onObjectLeaveZone(zone, obj)
    if zone.type == 'Hand' and obj.type == 'Card' then
        if self.getGMNotes() == zone.getValue() then
            local HandCards = {}
            for _, ob in ipairs(getObjects()) do
                if ob.hasTag(self.getTags()[2]) and ob.type == 'Card' then
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
                for i, objectInHand in ipairs(zone.getObjects()) do
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
                    for _, ob in ipairs(getObjects()) do
                        if ob.hasTag(self.getTags()[2]) and ob.type == 'Card' then
                            ob.removeTag(self.getTags()[2])
                        end
                    end
                    local handObjects = zone.getObjects()
                    -- Pass pick info to DraftCardsTaken here
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
                        TimerIsCounting = false
                    end
                end
            end
        end
    end
    if DebounceTimer ~= nil then Wait.stop(DebounceTimer) end
    DebounceTimer = Wait.time(function()
        if #Player[self.getGMNotes()].getHandObjects(1) == 0 and #self.getObjects() > 0 then
            TakenCount = 0
            -- Deal the cards from the stack dealt and add the right tags
            for _, j in ipairs(self.dealToColorWithOffset(Vector(0, 0, 0), true, self.getGMNotes()).spread()) do
                Wait.time(j.addTag(self.getTags()[1] .. self.getGMNotes()), 1)
            end
            TimerCount = 0
            -- Start the pick timer.
            TimerIsCounting = true
        end
        DebounceTimer = nil
    end, 1)
end

function onObjectEnterZone(zone, obj)
    if zone.type == 'Hand' and obj.type == 'Card' then
        if self.getGMNotes() == zone.getValue() then
            local HandCards = {}
            for _, ob in ipairs(getObjects()) do
                if ob.hasTag(self.getTags()[2]) and ob.type == 'Card' then
                    table.insert(HandCards, ob.getGUID())
                end
            end
            if indexOf(HandCards, obj.getGUID()) == nil and #HandCards > 0 then
                obj.highlightOn('Red')
                StopCounting = true
                return
            end
            if not StopCounting then
                TakenCount = TakenCount - 1
                if TakenCount < 0 then
                    TakenCount = 0
                end
                self.editButton({ index = 1, label = TakenCount .. " cards picked" })
            end
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
    log(StopCounting)
end
