const { globalEvents } = require('@tabletop-playground/api')
globalEvents.onChatMessage = (sender, message) => {
    if (message.match(/^Frostwind\sfuzzy\s/g)) {
        // Fuzzy search Scryfall for cards.
        const [query] = message.match(/(?<=^Frostwind\sfuzzy\s).+/) ?? [null]
        if (query !== null) {
            fetch(`https://api.scryfall.com/cards/named?fuzzy=${encodeURI(query)}`).then(r => {
                return r.json()
            }).then(v => {
                world.createObjectFromTemplate('31E5DB224CB620FF0B35E79BB7BB8D02', sender.getCursorPosition()).setSavedData(v.id, 'sf_id')
            })
        }
    }
    if (message.match(/^Frostwind\shttps:\/\/www\.moxfield\.com\/decks\/.+/g)) {
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

        const m = world.createObjectFromTemplate('31E5DB224CB620FF0B35E79BB7BB8D02', player.getCursorPosition().add([0, 0, 0]))
        
        main_deck.reduce((acc, curr) => {
            if (JSON.stringify([...acc.at(-1), curr]).length < 900) {
                acc.at(-1).push(curr)
            } else {
                acc.push([curr])
            }
            return acc
        }, [[]]).map((v, i) => m.setSavedData(JSON.stringify(v), `sf_id_${i}`))
        // const s = world.createObjectFromTemplate('31E5DB224CB620FF0B35E79BB7BB8D02', player.getCursorPosition().add([1, 0, 0]))
        // side_deck.reduce((acc, curr) => {
        //     if (JSON.stringify([...acc.at(-1), curr]).length < 900) {
        //         acc.at(-1).push(curr)
        //     } else {
        //         acc.push([curr])
        //     }
        //     return acc
        // }, [[]]).map((v, i) => s.setSavedData(JSON.stringify(v), `sf_id_${i}`))
        // const c = world.createObjectFromTemplate('31E5DB224CB620FF0B35E79BB7BB8D02', player.getCursorPosition().add([2, 0, 0]))
        // comm_deck.reduce((acc, curr) => {
        //     if (JSON.stringify([...acc.at(-1), curr]).length < 900) {
        //         acc.at(-1).push(curr)
        //     } else {
        //         acc.push([curr])
        //     }
        //     return acc
        // }, [[]]).map((v, i) => c.setSavedData(JSON.stringify(v), `sf_id_${i}`))
        // const p = world.createObjectFromTemplate('31E5DB224CB620FF0B35E79BB7BB8D02', player.getCursorPosition().add([3, 0, 0]))
        // comp_deck.reduce((acc, curr) => {
        //     if (JSON.stringify([...acc.at(-1), curr]).length < 900) {
        //         acc.at(-1).push(curr)
        //     } else {
        //         acc.push([curr])
        //     }
        //     return acc
        // }, [[]]).map((v, i) => p.setSavedData(JSON.stringify(v), `sf_id_${i}`))
        // const a = world.createObjectFromTemplate('31E5DB224CB620FF0B35E79BB7BB8D02', player.getCursorPosition().add([4, 0, 0]))
        // attr_deck.reduce((acc, curr) => {
        //     if (JSON.stringify([...acc.at(-1), curr]).length < 900) {
        //         acc.at(-1).push(curr)
        //     } else {
        //         acc.push([curr])
        //     }
        //     return acc
        // }, [[]]).map((v, i) => a.setSavedData(JSON.stringify(v), `sf_id_${i}`))
        // const g = world.createObjectFromTemplate('31E5DB224CB620FF0B35E79BB7BB8D02', player.getCursorPosition().add([5, 0, 0]))
        // sign_deck.reduce((acc, curr) => {
        //     if (JSON.stringify([...acc.at(-1), curr]).length < 900) {
        //         acc.at(-1).push(curr)
        //     } else {
        //         acc.push([curr])
        //     }
        //     return acc
        // }, [[]]).map((v, i) => g.setSavedData(JSON.stringify(v), `sf_id_${i}`))
        // const t = world.createObjectFromTemplate('31E5DB224CB620FF0B35E79BB7BB8D02', player.getCursorPosition().add([6, 0, 0]))
        // stic_deck.reduce((acc, curr) => {
        //     if (JSON.stringify([...acc.at(-1), curr]).length < 900) {
        //         acc.at(-1).push(curr)
        //     } else {
        //         acc.push([curr])
        //     }
        //     return acc
        // }, [[]]).map((v, i) => t.setSavedData(JSON.stringify(v), `sf_id_${i}`))
    })
}
