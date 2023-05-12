const { refObject, Vector, Rotator, Border, RichText, Button, UIElement, VerticalBox } = require("@tabletop-playground/api");

const globalState = {
	loyalty: undefined,
	stat_counters: undefined,
};

const debounce = (func, wait) => {
	let d = null;
	return (args) => {
		if (d !== null) clearTimeout(d);
		d = setTimeout(() => {
			if (refObject.isValid && refObject.getStackSize() === 1) func.apply(args);
		}, wait);
	};
};
const debounceCardDetails = debounce(generateCardDetails, 1000);

debounceCardDetails();

refObject.onCreated = (t) => {
	refObject.setName("");
	debounceCardDetails();
};

refObject.onInserted = (t) => {
	refObject.setName("");
	refObject.removeUI(0);
};

refObject.onRemoved = (t) => {
	refObject.setName("");
	debounceCardDetails();
};

function createTokens() {
	const selfURL = refObject.getCardDetails().textureOverrideURL;
	const [front_face] = selfURL.match(/(?<=&front_face=)(false|true)/g) ?? ["true"];
	const [sf_id] = selfURL.match(/[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}/g) ?? [];
	if (sf_id !== undefined) {
		fetch(`https://api.scryfall.com/cards/${sf_id}`)
			.then((r) => r.json())
			.then(async (v) => {
				const position = refObject.getPosition();
				const { all_parts } = v;
				let main_stack = undefined;
				for (let index = 0; index < all_parts.length; index++) {
					const element = all_parts[index];
					if (element.id === sf_id) continue;
					if (main_stack === undefined) {
						const c = await fetch(`https://api.scryfall.com/cards/${element.id}`);
						const j = await c.json();
						const q = world.createObjectFromTemplate("31E5DB224CB620FF0B35E79BB7BB8D02", position.add([0, 8, 1]));
						if (["normal", "adventure", "flip", "split", "meld", "leveler", "class", "saga", "planar", "vanguard", "token", "augment", "host", "emblem"].includes(j.layout)) {
							q.setTextureOverrideURL(j.image_uris.normal.concat(`&scryfall_id=${element.id}&front_face=true`));
						} else {
							q.setTextureOverrideURL(j.card_faces[0].image_uris.normal.concat(`&scryfall_id=${element.id}&front_face=true`));
						}
						main_stack = q;
					} else {
						const c = await fetch(`https://api.scryfall.com/cards/${element.id}`);
						const j = await c.json();
						const q = world.createObjectFromTemplate("31E5DB224CB620FF0B35E79BB7BB8D02", position.add([0, 8, 1]));
						if (["normal", "adventure", "flip", "split", "meld", "leveler", "class", "saga", "planar", "vanguard", "token", "augment", "host", "emblem"].includes(j.layout)) {
							q.setTextureOverrideURL(j.image_uris.normal.concat(`&scryfall_id=${element.id}&front_face=true`));
						} else {
							q.setTextureOverrideURL(j.card_faces[0].image_uris.normal.concat(`&scryfall_id=${element.id}&front_face=true`));
						}
						main_stack.addCards(q);
					}
				}
			});
	}
}

function transformCard() {
	const selfURL = refObject.getCardDetails().textureOverrideURL;
	const [front_face] = selfURL.match(/(?<=&front_face=)(false|true)/g) ?? ["true"];
	const [sf_id] = selfURL.match(/[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}/g) ?? [];
	if (sf_id !== undefined) {
		fetch(`https://api.scryfall.com/cards/${sf_id}`)
			.then((r) => r.json())
			.then((v) => {
				const { name, layout, mana_cost, cmc, type_line, oracle_text, power, toughness, rarity, card_faces, all_parts } = v;
				refObject.setName(name ?? "New Card");
				makeDetailedDescription(layout, { name, mana_cost, cmc, type_line, oracle_text, power, toughness, rarity, all_parts }, card_faces, front_face !== "true");
			});
	}
}

// This should look a lot like the description from TTS, if possible.
function makeDetailedDescription(layout, easy_face, card_faces, front_face = true) {
	// Add ui elements
	const RightSide = new UIElement();
	RightSide.height = 1060;
	RightSide.width = 760;
	RightSide.useWidgetSize = false;
	RightSide.zoomVisibility = 1;
	RightSide.position = new Vector(4.5, -3.5, -0.1);
	RightSide.rotation = new Rotator(180, 180, 0);
	RightSide.scale = 0.08;
	RightSide.anchorX = 0;
	RightSide.anchorY = 0;
	RightSide.useTransparency = true;

	const LeftSide = new UIElement();
	// LeftSide.height = 70;
	// LeftSide.width = 170;
	LeftSide.useWidgetSize = true;
	LeftSide.zoomVisibility = 0;
	LeftSide.position = new Vector(4.5, 5.0, -0.1);
	LeftSide.rotation = new Rotator(180, 180, 0);
	LeftSide.scale = 0.08;
	LeftSide.anchorX = 0;
	LeftSide.anchorY = 0;
	LeftSide.useTransparency = true;

	const LeftBorder = new VerticalBox();

	const RightBorder = new Border();
	RightBorder.setColor([1, 1, 1, 0.75]);

	// UI is different depending on layout.
	if (layout === "normal") {
		const Name = easy_face.name ?? "";
		const Type_Line = easy_face.type_line ?? "";
		const Mana_Cost = easy_face.mana_cost ?? "NO MANA COST";
		const Oracle_Text = easy_face.oracle_text ?? "";
		const Canvas_Text = `${Name} :: ${Mana_Cost}\n${Type_Line} :: ${easy_face.rarity.toUpperCase()}\n${Oracle_Text.replace(/\(/, "[size=24][i](").replace(/\)/, ")[/i][/size]")}`;
		RightBorder.setChild(new RichText().setText(Canvas_Text).setFontSize(24).setAutoWrap(true).setTextColor([0, 0, 0, 1]), 0, 0, 760, 1500);
	} else if (layout === "saga") {
		// Show a nice chapter split ui
		const Name = easy_face.name ?? "";
		const Type_Line = easy_face.type_line ?? "";
		const Mana_Cost = easy_face.mana_cost ?? "NO MANA COST";
		const Oracle_Text = easy_face.oracle_text ?? "";
		const Canvas_Text = `${Name} :: ${Mana_Cost}\n${Type_Line} :: ${easy_face.rarity.toUpperCase()}\n${Oracle_Text.replace(/\(/, "[size=24][i](").replace(/\)/, ")[/i][/size]")}`;
		RightBorder.setChild(new RichText().setText(Canvas_Text).setFontSize(24).setAutoWrap(true).setTextColor([0, 0, 0, 1]), 0, 0, 760, 1500);
	} else if (layout === "transform") {
		// UI is different based on which side is face up.
		const Name = card_faces[0].name ?? "";
		const Type_Line = card_faces[0].type_line ?? "";
		const Mana_Cost = card_faces[0].mana_cost ?? "NO MANA COST";
		const Oracle_Text = card_faces[0].oracle_text ?? "";
		const Name_2 = card_faces[1].name ?? "";
		const Type_Line_2 = card_faces[1].type_line ?? "";
		const Mana_Cost_2 = card_faces[1].mana_cost ?? "NO MANA COST";
		const Oracle_Text_2 = card_faces[1].oracle_text ?? "";
		const Canvas_Text = `[color=${front_face ? "#000000" : "#777777"}]${Name} :: ${Mana_Cost}\n${Type_Line} :: ${easy_face.rarity.toUpperCase()}\n${Oracle_Text.replace(/\(/, "[size=24][i](").replace(/\)/, ")[/i][/size]")}[/color]\n-------------------------\n[color=${front_face ? "#444444" : "#000000"}]${Name_2} :: ${Mana_Cost_2}\n${Type_Line_2} :: ${easy_face.rarity.toUpperCase()}\n${Oracle_Text_2.replace(/\(/, "[size=24][i](").replace(/\)/, ")[/i][/size]")}[/color]`;
		RightBorder.setChild(new RichText().setText(Canvas_Text).setFontSize(24).setAutoWrap(true).setTextColor([0, 0, 0, 1]), 0, 0, 760, 1500);
		if (!front_face) {
			refObject.setTextureOverrideURL(card_faces[1].image_uris.normal.concat("&front_face=false"));
			if (card_faces[1]["type_line"].includes("Planeswalker")) {
				const LoyaltyText = new Button();
				LoyaltyText.setFontSize(32);
				LoyaltyText.setText(card_faces[1]["loyalty"]);
				LoyaltyText.onClicked = () => null; // Actually, this should just be text.
				LoyaltyText.my_id = "loyalty";
				globalState.loyalty = parseInt(card_faces[1]["loyalty"]);
				// Use the global state to track loyalty

				const LoyaltyContainer = new UIElement();
				LoyaltyContainer.width = 100;
				LoyaltyContainer.height = 100;
				LoyaltyContainer.useWidgetSize = false;
				LoyaltyContainer.zoomVisibility = 0;
				LoyaltyContainer.position = new Vector(-3.5, -2.13, -0.1);
				LoyaltyContainer.rotation = new Rotator(180, 180, 0);
				LoyaltyContainer.scale = 0.08;
				LoyaltyContainer.anchorX = 0;
				LoyaltyContainer.anchorY = 0;
				LoyaltyContainer.useTransparency = true;
				LoyaltyContainer.widget = LoyaltyText;
				refObject.addUI(LoyaltyContainer);
				refObject.addCustomAction("Add 1 Loyalty", undefined, "add_one_loyalty");
				refObject.addCustomAction("Lose 1 Loyalty", undefined, "lose_one_loyalty");
				refObject.addCustomAction("Add 5 Loyalty", undefined, "add_five_loyalty");
				refObject.addCustomAction("Lose 5 Loyalty", undefined, "lose_five_loyalty");
			} else {
				const loyaltyElement = refObject.getUIs().find((ui) => ui.position.equals(new Vector(-3.5, -2.13, -0.1), 2));
				if (!!loyaltyElement) {
					refObject.removeUIElement(loyaltyElement);
					refObject.removeCustomAction("add_one_loyalty");
					refObject.removeCustomAction("lose_one_loyalty");
					refObject.removeCustomAction("add_five_loyalty");
					refObject.removeCustomAction("lose_five_loyalty");
				}
			}
		} else {
			refObject.setTextureOverrideURL(card_faces[0].image_uris.normal.concat("&front_face=true"));
			if (card_faces[0]["type_line"].includes("Planeswalker")) {
				const LoyaltyText = new Button();
				LoyaltyText.setFontSize(32);
				LoyaltyText.setText(card_faces[0]["loyalty"]);
				LoyaltyText.onClicked = () => null; // Actually, this should just be text.
				LoyaltyText.my_id = "loyalty";
				globalState.loyalty = parseInt(card_faces[0]["loyalty"]);
				// Use the global state to track loyalty

				const LoyaltyContainer = new UIElement();
				LoyaltyContainer.width = 100;
				LoyaltyContainer.height = 100;
				LoyaltyContainer.useWidgetSize = false;
				LoyaltyContainer.zoomVisibility = 0;
				LoyaltyContainer.position = new Vector(-3.5, -2.13, -0.1);
				LoyaltyContainer.rotation = new Rotator(180, 180, 0);
				LoyaltyContainer.scale = 0.08;
				LoyaltyContainer.anchorX = 0;
				LoyaltyContainer.anchorY = 0;
				LoyaltyContainer.useTransparency = true;
				LoyaltyContainer.widget = LoyaltyText;
				refObject.addUI(LoyaltyContainer);
				refObject.addCustomAction("Add 1 Loyalty", undefined, "add_one_loyalty");
				refObject.addCustomAction("Lose 1 Loyalty", undefined, "lose_one_loyalty");
				refObject.addCustomAction("Add 5 Loyalty", undefined, "add_five_loyalty");
				refObject.addCustomAction("Lose 5 Loyalty", undefined, "lose_five_loyalty");
			} else {
				const loyaltyElement = refObject.getUIs().find((ui) => ui.position.equals(new Vector(-3.5, -2.13, -0.1), 2));
				if (!!loyaltyElement) {
					refObject.removeUIElement(loyaltyElement);
					refObject.removeCustomAction("add_one_loyalty");
					refObject.removeCustomAction("lose_one_loyalty");
					refObject.removeCustomAction("add_five_loyalty");
					refObject.removeCustomAction("lose_five_loyalty");
				}
			}
		}
		const LeftButton = new Button();
		LeftButton.setFontSize(24);
		LeftButton.setText("Transform");
		LeftButton.onClicked = transformCard;
		LeftBorder.addChild(LeftButton);
	}
	if (!!easy_face["all_parts"] && layout !== "token") {
		const TokenButton = new Button();
		TokenButton.setFontSize(24);
		TokenButton.setText("Tokens");
		TokenButton.onClicked = createTokens;
		LeftBorder.addChild(TokenButton);
	}
	if (layout === "normal" && easy_face["type_line"].includes("Planeswalker")) {
		const LoyaltyText = new Button();
		LoyaltyText.setFontSize(32);
		LoyaltyText.setText(easy_face["loyalty"]);
		LoyaltyText.onClicked = () => null; // Actually, this should just be text.
		LoyaltyText.my_id = "loyalty";
		globalState.loyalty = parseInt(easy_face["loyalty"]);
		// Use the global state to track loyalty

		const LoyaltyContainer = new UIElement();
		LoyaltyContainer.width = 100;
		LoyaltyContainer.height = 100;
		LoyaltyContainer.useWidgetSize = false;
		LoyaltyContainer.zoomVisibility = 0;
		LoyaltyContainer.position = new Vector(-3.5, -2.13, -0.1);
		LoyaltyContainer.rotation = new Rotator(180, 180, 0);
		LoyaltyContainer.scale = 0.08;
		LoyaltyContainer.anchorX = 0;
		LoyaltyContainer.anchorY = 0;
		LoyaltyContainer.useTransparency = true;
		LoyaltyContainer.widget = LoyaltyText;
		refObject.addUI(LoyaltyContainer);
		refObject.addCustomAction("Add 1 Loyalty", undefined, "add_one_loyalty");
		refObject.addCustomAction("Lose 1 Loyalty", undefined, "lose_one_loyalty");
		refObject.addCustomAction("Add 5 Loyalty", undefined, "add_five_loyalty");
		refObject.addCustomAction("Lose 5 Loyalty", undefined, "lose_five_loyalty");
	}

	RightSide.widget = RightBorder;
	LeftSide.widget = LeftBorder;
	refObject.addUI(RightSide);
	refObject.addUI(LeftSide);
}

function generateCardDetails() {
	process.nextTick(() => {
		if (refObject.getStackSize() > 1) return;
		const [sf_id] = refObject.getCardDetails()?.textureOverrideURL?.match(/[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}/g) ?? [];
		const [front_face] = refObject.getCardDetails()?.textureOverrideURL?.match(/(?<=&front_face=)(false|true)/g) ?? ["true"];
		if (sf_id !== undefined) {
			fetch(`https://api.scryfall.com/cards/${sf_id}`)
				.then((r) => r.json())
				.then((v) => {
					const { name, layout, mana_cost, cmc, type_line, oracle_text, power, toughness, rarity, card_faces, all_parts, loyalty } = v;
					// Remove unused properties. Max length of savedData is 1023 chars
					refObject.setName(name ?? "New Card");
					makeDetailedDescription(layout, { name, mana_cost, cmc, type_line, oracle_text, power, toughness, rarity, all_parts, loyalty }, card_faces, front_face === "true");
					refObject.onCustomAction = onCustomAction;
				});
		}
	});
}

function onCustomAction(self, player, action_id) {
	let UIToUpdate = undefined;
	switch (action_id) {
		case "add_one_loyalty":
			UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(-3.5, -2.13, -0.1), 1));
			if (UIToUpdate === undefined) {
				console.log("Did not find.");
				break;
			}
			globalState.loyalty = (globalState.loyalty ?? 0) + 1;
			UIToUpdate.widget.setText(`${globalState.loyalty}`);
			break;
		case "lose_one_loyalty":
			UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(-3.5, -2.13, -0.1), 1));
			if (UIToUpdate === undefined) {
				console.log("Did not find.");
				break;
			}
			globalState.loyalty = (globalState.loyalty ?? 0) - 1;
			UIToUpdate.widget.setText(`${globalState.loyalty}`);
			break;
		case "add_five_loyalty":
			UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(-3.5, -2.13, -0.1), 1));
			if (UIToUpdate === undefined) {
				console.log("Did not find.");
				break;
			}
			globalState.loyalty = (globalState.loyalty ?? 0) + 5;
			UIToUpdate.widget.setText(`${globalState.loyalty}`);
			break;
		case "lose_five_loyalty":
			UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(-3.5, -2.13, -0.1), 1));
			if (UIToUpdate === undefined) {
				console.log("Did not find.");
				break;
			}
			globalState.loyalty = (globalState.loyalty ?? 0) - 5;
			UIToUpdate.widget.setText(`${globalState.loyalty}`);
			break;

		default:
			break;
	}
}
