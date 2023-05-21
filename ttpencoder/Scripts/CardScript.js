const { refObject, Vector, Rotator, Border, RichText, Button, UIElement, VerticalBox, UIZoomVisibility, ImageButton, refPackageId } = require("@tabletop-playground/api");

const globalState = {
	loyalty: undefined,
	stats: undefined,
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

function createTokens(button, player) {
	let setting = button.getText() === "Tokens";
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
					if (setting && element.component !== "token") continue;
					if (!setting && !element.type_line.includes("Emblem")) continue;
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
function makeDetailedDescription(layout, easy_face, [front, back] = [], front_face = true) {
	// Add ui elements
	const RightSide = new UIElement();
	RightSide.height = 1060;
	RightSide.width = 760;
	RightSide.useWidgetSize = false;
	RightSide.zoomVisibility = UIZoomVisibility.ZoomedOnly;
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
	LeftSide.zoomVisibility = UIZoomVisibility.Regular;
	LeftSide.position = new Vector(4.5, 3.5, -0.1);
	LeftSide.rotation = new Rotator(180, 180, 0);
	LeftSide.scale = 0.08;
	LeftSide.anchorX = 1;
	LeftSide.anchorY = 0;
	LeftSide.useTransparency = true;

	const LeftBorder = new VerticalBox();

	const RightBorder = new Border();
	RightBorder.setColor([1, 1, 1, 0.9]);

	// UI is different depending on layout.
	if (layout === "normal") {
		const Name = easy_face.name ?? "";
		const Type_Line = easy_face.type_line ?? "";
		const Mana_Cost = easy_face.mana_cost ?? "NO MANA COST";
		const Oracle_Text = easy_face.oracle_text ?? "";
		const Canvas_Text = `${Name} :: ${Mana_Cost}\n${Type_Line} :: ${easy_face.rarity.toUpperCase()}\n${Oracle_Text.replace(/\(/g, "[size=24][i](").replace(/\)/g, ")[/i][/size]")}${easy_face["type_line"].includes("Planeswalker") ? "\nStarting Loyalty: " + easy_face["loyalty"] : ""}${easy_face["type_line"].includes("Creature") || easy_face["type_line"].includes("Vehicle") ? "\n" + easy_face["power"] + "/" + easy_face["toughness"] : ""}`;
		RightBorder.setChild(new RichText().setText(Canvas_Text).setFontSize(24).setAutoWrap(true).setTextColor([0, 0, 0, 1]), 0, 0, 760, 1500);
		if (easy_face["type_line"].includes("Planeswalker")) {
			const LoyaltyText = new Button();
			LoyaltyText.setFontSize(48);
			LoyaltyText.setText(easy_face["loyalty"]);
			LoyaltyText.onClicked = () => null;
			globalState.loyalty = parseInt(easy_face["loyalty"]);
			const LoyaltyContainer = new UIElement();
			LoyaltyContainer.width = 100;
			LoyaltyContainer.height = 100;
			LoyaltyContainer.useWidgetSize = false;
			LoyaltyContainer.zoomVisibility = UIZoomVisibility.Both;
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
	} else if (layout === "saga") {
		// Show a nice chapter split ui
		const Name = easy_face.name ?? "";
		const Type_Line = easy_face.type_line ?? "";
		const Mana_Cost = easy_face.mana_cost ?? "NO MANA COST";
		const Oracle_Text = easy_face.oracle_text ?? "";
		const Canvas_Text = `${Name} :: ${Mana_Cost}\n${Type_Line} :: ${easy_face.rarity.toUpperCase()}\n${Oracle_Text.replace(/\(/g, "[size=24][i](").replace(/\)/g, ")[/i][/size]")}`;
		RightBorder.setChild(new RichText().setText(Canvas_Text).setFontSize(24).setAutoWrap(true).setTextColor([0, 0, 0, 1]), 0, 0, 760, 1500);
	} else if (layout === "transform") {
		// UI is different based on which side is face up.
		const Name = front.name ?? "";
		const Type_Line = front.type_line ?? "";
		const Mana_Cost = front.mana_cost ?? "NO MANA COST";
		const Oracle_Text = front.oracle_text ?? "";
		const Name_2 = back.name ?? "";
		const Type_Line_2 = back.type_line ?? "";
		const Mana_Cost_2 = back.mana_cost ?? "NO MANA COST";
		const Oracle_Text_2 = back.oracle_text ?? "";
		let use_l_d = front_face ? (front["type_line"].includes("Planeswalker") ? "pw" : front["type_line"].includes("Battle") ? "bt" : false) : back["type_line"].includes("Planeswalker") ? "pw" : back["type_line"].includes("Battle") ? "bt" : false;
		let use_l_d_f = front["type_line"].includes("Planeswalker") ? "pw" : front["type_line"].includes("Battle") ? "bt" : false;
		let use_l_d_b = back["type_line"].includes("Planeswalker") ? "pw" : back["type_line"].includes("Battle") ? "bt" : false;
		const Canvas_Text = `[color=${front_face ? "#000000" : "#777777"}]${Name} :: ${Mana_Cost}\n${Type_Line} :: ${easy_face.rarity.toUpperCase()}\n${Oracle_Text.replace(/\(/g, "[size=24][i](").replace(/\)/g, ")[/i][/size]")}${use_l_d_f === "pw" ? "\nStarting Loyalty: " + front["loyalty"] : use_l_d_f === "bt" ? "\nStarting Defense: " + front["defense"] : ""}${front["type_line"].includes("Creature") || front["type_line"].includes("Vehicle") ? "\n" + front["power"] + "/" + front["toughness"] : ""}[/color]\n-------------------------\n[color=${front_face ? "#444444" : "#000000"}]${Name_2} :: ${Mana_Cost_2}\n${Type_Line_2} :: ${easy_face.rarity.toUpperCase()}\n${Oracle_Text_2.replace(/\(/g, "[size=24][i](").replace(/\)/g, ")[/i][/size]")}${use_l_d_b === "pw" ? "\nStarting Loyalty: " + back["loyalty"] : use_l_d_b === "bt" ? "\nStarting Defense: " + back["defense"] : ""}${
			back["type_line"].includes("Creature") || back["type_line"].includes("Vehicle") ? "\n" + back["power"] + "/" + back["toughness"] : ""
		}[/color]`;
		RightBorder.setChild(new RichText().setText(Canvas_Text).setFontSize(24).setAutoWrap(true).setTextColor([0, 0, 0, 1]), 0, 0, 760, 1500);
		refObject.setTextureOverrideURL(front_face ? front.image_uris.normal.concat("&front_face=true") : back.image_uris.normal.concat("&front_face=false"));
		if (use_l_d) {
			const LoyaltyText = new Button();
			LoyaltyText.setFontSize(48);
			LoyaltyText.setText(use_l_d === "pw" ? (front_face ? front["loyalty"] : back["loyalty"]) : front_face ? front["defense"] : back["defense"]);
			LoyaltyText.onClicked = () => null;
			globalState.loyalty = parseInt(use_l_d === "pw" ? (front_face ? front["loyalty"] : back["loyalty"]) : front_face ? front["defense"] : back["defense"]);
			const LoyaltyContainer = new UIElement();
			LoyaltyContainer.width = 100;
			LoyaltyContainer.height = 100;
			LoyaltyContainer.useWidgetSize = false;
			LoyaltyContainer.zoomVisibility = UIZoomVisibility.Both;
			LoyaltyContainer.position = use_l_d === "bt" ? new Vector(4.5, -2.4, -0.1) : new Vector(-3.5, -2.13, -0.1);
			LoyaltyContainer.rotation = new Rotator(180, 180, 0);
			LoyaltyContainer.scale = 0.08;
			LoyaltyContainer.anchorX = 0;
			LoyaltyContainer.anchorY = 0;
			LoyaltyContainer.useTransparency = true;
			LoyaltyContainer.widget = LoyaltyText;
			refObject.addUI(LoyaltyContainer);
			refObject.addCustomAction("Add 1 " + (use_l_d === "pw" ? "Loyalty" : "Defense"), undefined, "add_one_loyalty");
			refObject.addCustomAction("Lose 1 " + (use_l_d === "pw" ? "Loyalty" : "Defense"), undefined, "lose_one_loyalty");
			refObject.addCustomAction("Add 5 " + (use_l_d === "pw" ? "Loyalty" : "Defense"), undefined, "add_five_loyalty");
			refObject.addCustomAction("Lose 5 " + (use_l_d === "pw" ? "Loyalty" : "Defense"), undefined, "lose_five_loyalty");
		} else {
			const loyaltyElement = refObject.getUIs().find((ui) => ui.position.equals(new Vector(-3.5, -2.13, -0.1), 1));
			const defenseElement = refObject.getUIs().find((ui) => ui.position.equals(new Vector(4.5, -2.4, -0.1), 1));
			if (!!loyaltyElement) refObject.removeUIElement(loyaltyElement);
			if (!!defenseElement) refObject.removeUIElement(defenseElement);
			refObject.removeCustomAction("add_one_loyalty");
			refObject.removeCustomAction("lose_one_loyalty");
			refObject.removeCustomAction("add_five_loyalty");
			refObject.removeCustomAction("lose_five_loyalty");
		}
		const LeftButton = new ImageButton();
		LeftButton.setImage("back-forth.png", refPackageId); // Icon created by Lorc, sourced from game-icons.net
		LeftButton.setImageSize(64, 0);
		LeftButton.onClicked = transformCard;
		LeftBorder.addChild(LeftButton);
	}
	if (!!easy_face["all_parts"] && easy_face["all_parts"].some((part) => part.component === "token")) {
		const TokenButton = new Button();
		TokenButton.setFontSize(24);
		TokenButton.setText("Tokens");
		TokenButton.onClicked = createTokens;
		LeftBorder.addChild(TokenButton);
	}
	if (!!easy_face["all_parts"] && !easy_face.type_line.includes("Emblem") && easy_face["all_parts"].some((part) => part.type_line.includes("Emblem"))) {
		const EmblemButton = new Button();
		EmblemButton.setFontSize(24);
		EmblemButton.setText("Emblems");
		EmblemButton.onClicked = createTokens;
		LeftBorder.addChild(EmblemButton);
	}
	refObject.addCustomAction("Add 1 Stat Counter", undefined, "add_one_stat");
	refObject.addCustomAction("Lose 1 Stat Counter", undefined, "lose_one_stat");
	refObject.addCustomAction("Add 5 Stat Counters", undefined, "add_five_stat");
	refObject.addCustomAction("Lose 5 Stat Counters", undefined, "lose_five_stat");

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

function createStatCounterUI() {
	const StatCounterText = new Button();
	StatCounterText.setFontSize(24);
	StatCounterText.setText("+0/+0");
	StatCounterText.onClicked = () => null;
	const StatCounterContainer = new UIElement();
	StatCounterContainer.width = 140;
	StatCounterContainer.height = 75;
	StatCounterContainer.useWidgetSize = false;
	StatCounterContainer.zoomVisibility = UIZoomVisibility.Both;
	StatCounterContainer.position = new Vector(-3, -1.65, -0.1);
	StatCounterContainer.rotation = new Rotator(180, 180, 0);
	StatCounterContainer.scale = 0.08;
	StatCounterContainer.anchorX = 0;
	StatCounterContainer.anchorY = 0;
	StatCounterContainer.useTransparency = true;
	StatCounterContainer.widget = StatCounterText;
	refObject.addUI(StatCounterContainer);
	return StatCounterContainer;
}

function onCustomAction(self, player, action_id) {
	let UIToUpdate = undefined;
	switch (action_id) {
		case "add_one_loyalty":
			UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(-3.5, -2.13, -0.1), 0.2));
			if (UIToUpdate === undefined) UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(4.5, -2.4, -0.1), 1));
			if (UIToUpdate === undefined) break;
			globalState.loyalty = (globalState.loyalty ?? 0) + 1;
			UIToUpdate.widget.setText(`${globalState.loyalty}`);
			break;
		case "lose_one_loyalty":
			UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(-3.5, -2.13, -0.1), 0.2));
			if (UIToUpdate === undefined) UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(4.5, -2.4, -0.1), 1));
			if (UIToUpdate === undefined) break;
			globalState.loyalty = (globalState.loyalty ?? 0) - 1;
			UIToUpdate.widget.setText(`${globalState.loyalty}`);
			break;
		case "add_five_loyalty":
			UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(-3.5, -2.13, -0.1), 0.2));
			if (UIToUpdate === undefined) UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(4.5, -2.4, -0.1), 1));
			if (UIToUpdate === undefined) break;
			globalState.loyalty = (globalState.loyalty ?? 0) + 5;
			UIToUpdate.widget.setText(`${globalState.loyalty}`);
			break;
		case "lose_five_loyalty":
			UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(-3.5, -2.13, -0.1), 0.2));
			if (UIToUpdate === undefined) UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(4.5, -2.4, -0.1), 1));
			if (UIToUpdate === undefined) break;
			globalState.loyalty = (globalState.loyalty ?? 0) - 5;
			UIToUpdate.widget.setText(`${globalState.loyalty}`);
			break;
		case "add_one_stat":
			UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(-3, -1.65, -0.1), 0.2));
			if (UIToUpdate === undefined) UIToUpdate = createStatCounterUI();
			globalState.stats = (globalState.stats ?? 0) + 1;
			if (globalState.stats === 0) refObject.removeUIElement(UIToUpdate);
			else UIToUpdate.widget.setText(globalState.stats >= 0 ? `+${globalState.stats}/+${globalState.stats}` : `${globalState.stats}/${globalState.stats}`);
			break;
		case "lose_one_stat":
			UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(-3, -1.65, -0.1), 0.2));
			if (UIToUpdate === undefined) UIToUpdate = createStatCounterUI();
			globalState.stats = (globalState.stats ?? 0) - 1;
			if (globalState.stats === 0) refObject.removeUIElement(UIToUpdate);
			else UIToUpdate.widget.setText(globalState.stats >= 0 ? `+${globalState.stats}/+${globalState.stats}` : `${globalState.stats}/${globalState.stats}`);
			break;
		case "add_five_stat":
			UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(-3, -1.65, -0.1), 0.2));
			if (UIToUpdate === undefined) UIToUpdate = createStatCounterUI();
			globalState.stats = (globalState.stats ?? 0) + 5;
			if (globalState.stats === 0) refObject.removeUIElement(UIToUpdate);
			else UIToUpdate.widget.setText(globalState.stats >= 0 ? `+${globalState.stats}/+${globalState.stats}` : `${globalState.stats}/${globalState.stats}`);
			break;
		case "lose_five_stat":
			UIToUpdate = refObject.getUIs().find((v) => v.position.equals(new Vector(-3, -1.65, -0.1), 0.2));
			if (UIToUpdate === undefined) UIToUpdate = createStatCounterUI();
			globalState.stats = (globalState.stats ?? 0) - 5;
			if (globalState.stats === 0) refObject.removeUIElement(UIToUpdate);
			else UIToUpdate.widget.setText(globalState.stats >= 0 ? `+${globalState.stats}/+${globalState.stats}` : `${globalState.stats}/${globalState.stats}`);
			break;

		default:
			break;
	}
}
