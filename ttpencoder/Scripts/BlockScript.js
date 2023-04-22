const { globalEvents } = require("@tabletop-playground/api");
globalEvents.onChatMessage = (sender, message) => {
	if (message.match(/^Frostwind\sfuzzy\s/g)) {
		// Fuzzy search Scryfall for cards.
		const [query] = message.match(/(?<=^Frostwind\sfuzzy\s).+/) ?? [null];
		if (query !== null) {
			fetch(`https://api.scryfall.com/cards/named?fuzzy=${encodeURI(query)}`)
				.then((r) => {
					return r.json();
				})
				.then((v) => {
					world.createObjectFromTemplate("31E5DB224CB620FF0B35E79BB7BB8D02", sender.getCursorPosition()).setSavedData(v.id, "sf_id");
				});
		}
	}
	if (message.match(/^Frostwind\shttps:\/\/www\.moxfield\.com\/decks\/.+/g)) {
		const [mox_id] = message.match(/(?<=^Frostwind\shttps:\/\/www\.moxfield\.com\/decks\/).+/) ?? [null];
		if (mox_id !== null) {
			makeMoxfieldDeck(mox_id, sender);
		}
	}
};

function makeMoxfieldDeck(deck_id, player) {
	fetch(`https://api2.moxfield.com/v2/decks/all/${deck_id}`)
		.then((r) => {
			return r.json();
		})
		.then((v) => {
			const main_deck = [];
			// const side_deck = []
			// const comm_deck = []
			// const comp_deck = []
			// const attr_deck = []
			// const sign_deck = []
			// const stic_deck = []

			const { mainboard, sideboard, commanders, companions, attractions, signatureSpells, stickers } = v;

			Object.entries(mainboard).forEach(([k, v]) => (v.printingData === undefined ? main_deck.push(...Array(v.quantity).fill({ scryfall_id: v.card.scryfall_id })) : main_deck.push(...Array(v.printingData[0].quantity).fill({ scryfall_id: v.printingData[0].card.scryfall_id }), ...Array(v.printingData[1].quantity).fill({ scryfall_id: v.printingData[1].card.scryfall_id }))));
			// Object.entries(sideboard).forEach(([k, v]) => side_deck.push(...Array(v.quantity).fill(v.card.scryfall_id)))
			// Object.entries(commanders).forEach(([k, v]) => comm_deck.push(...Array(v.quantity).fill(v.card.scryfall_id)))
			// Object.entries(companions).forEach(([k, v]) => comp_deck.push(...Array(v.quantity).fill(v.card.scryfall_id)))
			// Object.entries(attractions).forEach(([k, v]) => attr_deck.push(...Array(v.quantity).fill(v.card.scryfall_id)))
			// Object.entries(signatureSpells).forEach(([k, v]) => sign_deck.push(...Array(v.quantity).fill(v.card.scryfall_id)))
			// Object.entries(stickers).forEach(([k, v]) => stic_deck.push(...Array(v.quantity).fill(v.card.scryfall_id)))

			main_deck.map(({ scryfall_id }, i) => {
				fetch(`https://api.scryfall.com/cards/${scryfall_id}`)
					.then((r) => r.json())
					.then((r) => {
						const q = world.createObjectFromTemplate("31E5DB224CB620FF0B35E79BB7BB8D02", player.getCursorPosition().add([0, 0, 0]));
						if (["normal", "adventure", "flip", "split", "meld", "leveler", "class", "saga", "planar", "vanguard", "token", "augment", "host"].includes(r.layout)) {
							q.setTextureOverrideURL(r.image_uris.normal.concat(`&scryfall_id=${scryfall_id}`));
						} else {
							q.setTextureOverrideURL(r.card_faces[0].image_uris.normal.concat(`&scryfall_id=${scryfall_id}`));
						}
					});
			});
		});
}
