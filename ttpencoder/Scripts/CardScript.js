const { refObject, Card, GlobalScriptingEvents, world, globalEvents } = require('@tabletop-playground/api')

refObject.onCreated = (object) => {
    if (object instanceof Card) {
        process.nextTick(() => {
            // If this card will be one card, 'sf_id' will be set and a string.
            const sf_id = refObject.getSavedData('sf_id')
            if (sf_id !== '') {
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
                    refObject.setDescription(makeDetailedDescription(layout, { name, mana_cost, cmc, type_line, oracle_text, power, toughness, rarity }, card_faces))
                    refObject.setTextureOverrideURL(image_uris['large'] ?? image_uris['normal'])
                })
            } else {
                console.log(`Card with id ${refObject.getId()} does not have an sf_id.`)
            }
            // If this card will be a deck, loop over 'sf_id_N`` until it isn't empty.
        })
    }
}

// This should look a lot like the description from TTS, if possible.
// Not sure if there's a text coloring module for setDescription. If not, redo this.
function makeDetailedDescription(layout, easy_face, card_faces) {
    return ''
}
