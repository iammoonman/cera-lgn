const { refObject, UIElement, Vector, Text, Rotator } = require("@tabletop-playground/api");

generateCardDetails();

refObject.onCreated = () => {
	generateCardDetails();
};

refObject.onRemoved = (t) => {
	if (t.getStackSize() > 1) return;
	generateCardDetails();
};

// This should look a lot like the description from TTS, if possible.
function makeDetailedDescription(layout, easy_face, card_faces) {
	const fancyDescription = new UIElement();
    fancyDescription.scale = 0.1
    fancyDescription.zoomVisibility = 1
    fancyDescription.twoSided = true;
    fancyDescription.anchorX = 0
	fancyDescription.position = new Vector(0, -3.5, -0.1);
    fancyDescription.rotation = new Rotator(180, 180, 0);
	fancyDescription.widget = new Text().setText(`BOTTOM TEXT`).setFontSize(48);
	refObject.addUI(fancyDescription);
}

function generateCardDetails() {
	process.nextTick(() => {
		// If this card will be one card, 'sf_id' will be set and a string.
		const sf_id = refObject.getCardDetails()?.textureOverrideURL?.match(/[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}/g);
		if (sf_id !== undefined) {
			fetch(`https://api.scryfall.com/cards/${sf_id}`)
				.then((r) => {
					return r.json();
				})
				.then((v) => {
					const { name, layout, mana_cost, cmc, type_line, oracle_text, power, toughness, rarity, card_faces } = v;
					// Remove unused properties. Max length of savedData is 1023 chars
					refObject.setName(name ?? "New Card");
					makeDetailedDescription(layout, { name, mana_cost, cmc, type_line, oracle_text, power, toughness, rarity }, card_faces);
				});
		}
	});
}
