const { refObject, UIElement, Vector, Text, Rotator, Canvas, RichText, refPackageId } = require("@tabletop-playground/api");

generateCardDetails();

refObject.onCreated = (t) => {
	if (refObject.getStackSize() > 1) return refObject.setName("");
	generateCardDetails();
};

refObject.onInserted = (t) => {
	refObject.setName("");
	refObject.removeUI(0);
};

refObject.onRemoved = (t) => {
	if (refObject.getStackSize() > 1) return refObject.setName("");
	generateCardDetails();
};

// This should look a lot like the description from TTS, if possible.
function makeDetailedDescription(layout, easy_face, card_faces, front_face = true) {
	// add ui elements
	const RightSide = new UIElement();
	RightSide.height = 760;
	RightSide.width = 760;
	RightSide.useWidgetSize = false;
	RightSide.zoomVisibility = 1;
	RightSide.position = new Vector(4.5, -3.5, -0.1);
	RightSide.rotation = new Rotator(180, 180, 0);
	RightSide.scale = 0.08;
	RightSide.anchorX = 0;
	RightSide.anchorY = 0;
	const RightCanvas = new Canvas();
	if (layout === "normal") {
		const Name = easy_face.name ?? "";
		const Type_Line = easy_face.type_line ?? "";
		const Mana_Cost = easy_face.mana_cost ?? "NONE";
		const Oracle_Text = easy_face.oracle_text ?? "";
		const Canvas_Text = `${Name} :: ${Mana_Cost}
${Type_Line} :: ${easy_face.rarity.toUpperCase()}
${Oracle_Text.replace(/\(/, "[size=24][i](").replace(/\)/, ")[/i][/size]")}`;
		RightCanvas.addChild(new RichText().setText(Canvas_Text).setFontSize(24).setAutoWrap(true).setTextColor([0, 0, 0, 1]), 0, 0, 760, 1500);
	} else if (layout === "saga") {
		// Show a nice chapter split ui
	} else if (layout === "transform") {
		// UI is different based on which side is face up.
		const Name = card_faces[0].name ?? "";
		const Type_Line = card_faces[0].type_line ?? "";
		const Mana_Cost = card_faces[0].mana_cost ?? "NONE";
		const Oracle_Text = card_faces[0].oracle_text ?? "";
		const Name_2 = card_faces[1].name ?? "";
		const Type_Line_2 = card_faces[1].type_line ?? "";
		const Mana_Cost_2 = card_faces[1].mana_cost ?? "NONE";
		const Oracle_Text_2 = card_faces[1].oracle_text ?? "";
		const Canvas_Text = `[color=${front_face ? '#000000' : '#444444'}]${Name} :: ${Mana_Cost}
${Type_Line} :: ${easy_face.rarity.toUpperCase()}
${Oracle_Text.replace(/\(/, "[size=24][i](").replace(/\)/, ")[/i][/size]")}[/color]
-------------------------
[color=${front_face ? '#444444' : '#000000'}]${Name_2} :: ${Mana_Cost_2}
${Type_Line_2} :: ${easy_face.rarity.toUpperCase()}
${Oracle_Text_2.replace(/\(/, "[size=24][i](").replace(/\)/, ")[/i][/size]")}[/color]`;
		RightCanvas.addChild(new RichText().setText(Canvas_Text).setFontSize(24).setAutoWrap(true).setTextColor([0, 0, 0, 1]), 0, 0, 760, 1500);
		if (front_face) {
			const altFace = "31E5DB224CB620FF0B35E79BB7BB8D02";
			altFace.setTextureOverrideURL(card_faces[1].image_uris.normal.concat('&front_face=false'))
			refObject.createSwitcher([altFace]);
		}
	}
	RightSide.widget = RightCanvas;
	refObject.addUI(RightSide);
}

function generateCardDetails() {
	process.nextTick(() => {
		if (refObject.getStackSize() > 1) return;
		// If this card will be one card, 'sf_id' will be set and a string.
		const [sf_id] = refObject.getCardDetails()?.textureOverrideURL?.match(/[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}/g) ?? [];
		const [front_face] = refObject.getCardDetails()?.textureOverrideURL?.match(/(?<=&front_face=)(false|true)/g) ?? [];
		if (sf_id !== undefined) {
			fetch(`https://api.scryfall.com/cards/${sf_id}`)
				.then((r) => r.json())
				.then((v) => {
					const { name, layout, mana_cost, cmc, type_line, oracle_text, power, toughness, rarity, card_faces } = v;
					// Remove unused properties. Max length of savedData is 1023 chars
					refObject.setName(name ?? "New Card");
					makeDetailedDescription(layout, { name, mana_cost, cmc, type_line, oracle_text, power, toughness, rarity }, card_faces, front_face === "true" || front_face === undefined);
				});
		}
	});
}
