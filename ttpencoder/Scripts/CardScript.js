const { refObject, Card, GlobalScriptingEvents, world, globalEvents } = require('@tabletop-playground/api')

refObject.onCreated = (object) => {
    if (object instanceof Card) {
        if (object.getStackSize() > 1) return;
        process.nextTick(() => fetchCardData())
    }
}
globalEvents.onChatMessage = (sender, message) => {
    if (message.match(/^Frostwind\sfuzzy\s/g)) {
        // Fuzzy search Scryfall for cards.
        const [query] = message.match(/(?<=^Frostwind\sfuzzy\s).+/) ?? [null]
        if (query !== null) {
            fetch(`https://api.scryfall.com/cards/named?fuzzy=${encodeURI(query)}`).then(r => {
                return r.json()
            }).then(v => {
                world.createObjectFromTemplate(refObject.getTemplateId(), [1, 1, 1]).setSavedData(v.id, 'sf_id')
            })
        }
    }
}

function fetchCardData() {
    if (refObject.getSavedData('sf_id') !== '') {
        console.log(refObject.getSavedData('sf_id'))
        fetch(`https://api.scryfall.com/cards/${refObject.getSavedData('sf_id')}`).then((r) => {
            return r.json()
        }).then(v => {
            const {
                id,
                name,
                layout,
                image_uris,
                mana_cost,
                cmc,
                type_line,
                oracle_text,
                power,
                toughness,
                rarity,
                all_parts,
                card_faces,
                keywords,
            } = v
            // Remove unused properties. Max length of savedData is 1023 chars
            refObject.setName(name ?? 'New Card')
            refObject.setDescription(makeDescription(layout, { name, mana_cost, cmc, type_line, oracle_text, power, toughness, rarity }, card_faces))
            refObject.setTextureOverrideURL(image_uris['large'] ?? image_uris['normal'])
        })
    } else {
        console.log(`Card with id ${refObject.getId()} does not have an sf_id.`)
    }
}

// This should look a lot like the description from TTS, if possible.
// Not sure if there's a text coloring module for setDescription. If not, redo this.
function makeDescription(layout, easy_face, card_faces) {
    return ''
}
