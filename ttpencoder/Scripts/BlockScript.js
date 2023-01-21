const { globalEvents } = require('@tabletop-playground/api')
globalEvents.onChatMessage = (sender, message) => {
    if (message.match(/^Frostwind\sfuzzy\s/g)) {
        // Fuzzy search Scryfall for cards.
        const [query] = message.match(/(?<=^Frostwind\sfuzzy\s).+/) ?? [null]
        if (query !== null) {
            fetch(`https://api.scryfall.com/cards/named?fuzzy=${encodeURI(query)}`).then(r => {
                return r.json()
            }).then(v => {
                world.createObjectFromTemplate(refObject.getTemplateId(), sender.getCursorPosition()).setSavedData(v.id, 'sf_id')
            })
        }
    }
    if (message.match(/^Frostwind\shttps:\/\/www\.moxfield\.com\/decks\/).+/g)) {
        const [mox_id] = message.match(/(?<=^Frostwind\shttps:\/\/www\.moxfield\.com\/decks\/).+/) ?? [null]
        if (mox_id !== null) {
            makeMoxfieldDeck(mox_id, sender)
        }
    }
}

function makeMoxfieldDeck(deck_id, player) {
    fetch(`https://api2.moxfield.com/v2/decks/all/${deck_id}`).then(r => {
        return r.json()
    }).then(v => {
        const main_deck = []
        const side_deck = []
        const comm_deck = []
        const comp_deck = []
        const attr_deck = []
        const sign_deck = []
        const stic_deck = []

        const { mainboard, sideboard, commanders, companions, attractions, signatureSpells, stickers } = v

        Object.entries(mainboard).forEach(([k, v]) => main_deck.push(...Array(v.quantity).fill(v.card.scryfall_id)))
        Object.entries(sideboard).forEach(([k, v]) => side_deck.push(...Array(v.quantity).fill(v.card.scryfall_id)))
        Object.entries(commanders).forEach(([k, v]) => comm_deck.push(...Array(v.quantity).fill(v.card.scryfall_id)))
        Object.entries(companions).forEach(([k, v]) => comp_deck.push(...Array(v.quantity).fill(v.card.scryfall_id)))
        Object.entries(attractions).forEach(([k, v]) => attr_deck.push(...Array(v.quantity).fill(v.card.scryfall_id)))
        Object.entries(signatureSpells).forEach(([k, v]) => sign_deck.push(...Array(v.quantity).fill(v.card.scryfall_id)))
        Object.entries(stickers).forEach(([k, v]) => stic_deck.push(...Array(v.quantity).fill(v.card.scryfall_id)))

        const m = world.createObjectFromTemplate('', player.getCursorPosition().add([0, 0, 0]))
        break_array_1023(main_deck).map((v, i) => s.setSavedData(JSON.stringify(v, `sf_id_${i}`)))
        const s = world.createObjectFromTemplate('', player.getCursorPosition().add([1, 0, 0]))
        break_array_1023(side_deck).map((v, i) => s.setSavedData(JSON.stringify(v, `sf_id_${i}`)))
        const c = world.createObjectFromTemplate('', player.getCursorPosition().add([2, 0, 0]))
        break_array_1023(comm_deck).map((v, i) => c.setSavedData(JSON.stringify(v, `sf_id_${i}`)))
        const p = world.createObjectFromTemplate('', player.getCursorPosition().add([3, 0, 0]))
        break_array_1023(comp_deck).map((v, i) => p.setSavedData(JSON.stringify(v, `sf_id_${i}`)))
        const a = world.createObjectFromTemplate('', player.getCursorPosition().add([4, 0, 0]))
        break_array_1023(attr_deck).map((v, i) => a.setSavedData(JSON.stringify(v, `sf_id_${i}`)))
        const g = world.createObjectFromTemplate('', player.getCursorPosition().add([5, 0, 0]))
        break_array_1023(sign_deck).map((v, i) => g.setSavedData(JSON.stringify(v, `sf_id_${i}`)))
        const t = world.createObjectFromTemplate('', player.getCursorPosition().add([6, 0, 0]))
        break_array_1023(stic_deck).map((v, i) => t.setSavedData(JSON.stringify(v, `sf_id_${i}`)))
    })
}

function break_array_1023(arr) {
    const collection = []
    arr.map(e => {
        if (JSON.stringify([...collection.at(-1), e]).length > 1010) {
            collection.at(-1).push(e)
        } else {
            collection.push([e])
        }
    })
    return collection
}