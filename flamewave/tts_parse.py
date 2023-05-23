import re


def italicize_reminder(text: str):
    out = re.sub(r"\(", "[i](", text)
    out = re.sub(r"\)", ")[/i]", out)
    return out


def make_oracle_dfc(card_dota, is_reverse=False):
    face_1 = card_dota["card_faces"][0]
    face_2 = card_dota["card_faces"][1]
    return (
        ("" if is_reverse else "[6E6E6E]")
        + f'[b]{face_1["name"]} {face_1["mana_cost"]}[/b]'
        + "\n"
        + f'{face_1["type_line"]} {rarity_icon(card_dota["rarity"])}'
        + "\n"
        + italicize_reminder(face_1["oracle_text"])
        + (
            f"\n[b]{face_1['power']}/{face_1['toughness']}[/b]"
            if ("Creature" in face_1["type_line"] or "Vehicle" in face_1["type_line"])
            else ""
        )
        + (
            f"\n[b]{face_1['loyalty']}[/b] Starting Loyalty"
            if "loyalty" in face_1.keys() and "Planeswalker" in face_1["type_line"]
            else ""
        )
        + (
            f"\n[b]{face_1['defense']}[/b] Starting Defense"
            if "defense" in face_1.keys() and "Battle" in face_1["type_line"]
            else ""
        )
        + "\n"
        + ("[6E6E6E]" if is_reverse else "[-]")
        + "\n"
        + f'[b]{face_2["name"]} {face_2["mana_cost"]}[/b]'
        + "\n"
        + f'{face_2["type_line"]} {rarity_icon(card_dota["rarity"])}'
        + "\n"
        + italicize_reminder(face_2["oracle_text"])
        + (
            f"\n[b]{face_2['power']}/{face_2['toughness']}[/b]"
            if ("Creature" in face_2["type_line"] or "Vehicle" in face_2["type_line"])
            else ""
        )
        + (
            (f"\n[b]{face_2['loyalty']}[/b] Starting Loyalty" if "Planeswalker" in face_2["type_line"] else "")
            if "loyalty" in face_2.keys()
            else ""
        )
        + (
            f"\n[b]{face_2['defense']}[/b] Starting Defense"
            if "defense" in face_2.keys() and "Battle" in face_2["type_line"]
            else ""
        )
        + ("[-]" if is_reverse else "")
    )


def make_oracle_normal(card_data):
    return (
        f'[b]{card_data["name"]} {card_data["mana_cost"]}[/b]'
        + "\n"
        + f'{card_data["type_line"]} {rarity_icon(card_data["rarity"])}'
        + "\n"
        + italicize_reminder(card_data["oracle_text"])
        + (
            f"\n[b]{card_data['power']}/{card_data['toughness']}[/b]"
            if ("Creature" in card_data["type_line"] or "Vehicle" in card_data["type_line"])
            and "adventure" != card_data["layout"]
            else ""
        )
        + (f"\n[b]{card_data['loyalty']}[/b] Starting Loyalty" if "Planeswalker" in card_data["type_line"] else "")
        + (
            f"\n[b]{card_data['defense']}[/b] Starting Defense"
            if "defense" in card_data.keys() and "Battle" in card_data["type_line"]
            else ""
        )
    )


def make_oracle_splitadventure(card_data):
    return (
        "[b]"
        + f'[b]{card_data["card_faces"][0]["name"]} {card_data["card_faces"][0]["mana_cost"]}[/b]'
        + "\n"
        + f'{card_data["card_faces"][0]["type_line"]} {rarity_icon(card_data["rarity"])}'
        + "\n"
        + italicize_reminder(card_data["card_faces"][0]["oracle_text"])
        + (
            "\n[b]" + card_data["card_faces"][0]["power"] + "/" + card_data["card_faces"][0]["toughness"] + "[/b]\n"
            if "power" in card_data["card_faces"][0].keys() and "toughness" in card_data["card_faces"][0].keys()
            else ""
        )
        + "\n"
        + f'[b]{card_data["card_faces"][1]["name"]} {card_data["card_faces"][1]["mana_cost"]}[/b]'
        + "\n"
        + f'{card_data["card_faces"][1]["type_line"]} {rarity_icon(card_data["rarity"])}'
        + "\n"
        + italicize_reminder(card_data["card_faces"][1]["oracle_text"])
        + "\n"
        + (
            "\n[b]" + card_data["card_faces"][1]["power"] + "/" + card_data["card_faces"][1]["toughness"] + "[/b]\n"
            if "power" in card_data["card_faces"][1].keys() and "toughness" in card_data["card_faces"][1].keys()
            else ""
        )
    )


def make_oracle_reversible(card_data):
    return


def make_oracle_vanguard(card_data):
    return (
        "[b]"
        + card_data["name"]
        + card_data["mana_cost"]
        + "[/b]"
        + "\n"
        + card_data["type_line"]
        + rarity_icon(card_data["rarity"])
        + "\n"
        + italicize_reminder(card_data["oracle_text"])
        + "\n"
        + f'Life: {card_data["life_modifier"]} + 20 = [b]{(20 + int(card_data["life_modifier"]))}[/b]'
        + "\n"
        + f'Hand: {card_data["hand_modifier"]} + 7 = [b]{(7 + int(card_data["hand_modifier"]))}[/b]'
    )


def rarity_icon(rarity):
    # Colors scraped from Scryfall
    if rarity == "mythic":
        return "[f64800]「M」[-]"
    elif rarity == "rare":
        return "[c5b37c]「R」[-]"
    elif rarity == "uncommon":
        return "[6c848c]「U」[-]"
    elif rarity == "common":
        return "[ffffff]「C」[-]"
    elif rarity == "special":
        return "[905d98]「S」[-]"
    elif rarity == "bonus":
        return "[9c202b]「B」[-]"
    return ""


def tts_parse(card):
    card_obj = {
        "oracle_id": card["oracle_id"] if "oracle_id" in card.keys() else "",
        "cmc": card["cmc"] if "cmc" in card.keys() else 0,
        "type_line": card["type_line"] if "type_line" in card.keys() else "",
        "layout": card["layout"],
        "set": card["set"],
        "name": card["name"],
        "collector_number": card["collector_number"],
        "planar": "Battle " in card["type_line"] or "Plane " in card["type_line"] if "type_line" in card else False,
    }
    if "card_faces" in card.keys() and card["layout"] in ["transform", "modal_dfc", "battle"]:
        extra_obj = {
            "stitched": card["stitched"] if "stitched" in card else False,
            "card_faces": [
                {
                    "name": face["name"],
                    "type_line": face["type_line"],
                    "planar": "Battle " in face["type_line"] or "Plane " in face["type_line"]
                    if "type_line" in face
                    else False,
                    "oracle_text": make_oracle_dfc(card, side == 0),
                    "image_uris": {"normal": face["image_uris"]["normal"], "small": face["image_uris"]["small"]},
                    "power": face["power"] if "power" in face.keys() and "toughness" in face.keys() else 0,
                    "toughness": face["toughness"] if "power" in face.keys() and "toughness" in face.keys() else 0,
                    "mana_cost": face["mana_cost"],
                    "loyalty": face["loyalty"] if "loyalty" in face.keys() else 0,
                }
                for side, face in enumerate(card["card_faces"])
            ],
        }
    elif card["layout"] in ["battle"]:
        extra_obj = {
            "name": card["name"],
            "type_line": card["type_line"],
            "oracle_text": make_oracle_normal(card),
            "image_uris": {"normal": card["image_uris"]["normal"], "small": card["image_uris"]["small"]},
            "power": card["power"] if "power" in card.keys() and "toughness" in card.keys() else 0,
            "toughness": card["toughness"] if "power" in card.keys() and "toughness" in card.keys() else 0,
            "mana_cost": card["mana_cost"],
            "loyalty": card["loyalty"] if "loyalty" in card.keys() else 0,
        }
    elif card["layout"] in ["split"]:
        extra_obj = {
            "type_line": card["type_line"],
            "oracle_text": make_oracle_splitadventure(card),
            "image_uris": {"normal": card["image_uris"]["normal"], "small": card["image_uris"]["small"]},
            "power": card["power"] if "power" in card.keys() and "toughness" in card.keys() else 0,
            "toughness": card["toughness"] if "power" in card.keys() and "toughness" in card.keys() else 0,
            "mana_cost": card["mana_cost"],
            "loyalty": card["loyalty"] if "loyalty" in card.keys() else 0,
        }
    elif card["layout"] in ["flip"]:
        extra_obj = {
            "card_faces": [
                {
                    "name": face["name"],
                    "type_line": face["type_line"],
                    "oracle_text": make_oracle_dfc(card, side == 0),
                    "image_uris": {"normal": card["image_uris"]["normal"], "small": card["image_uris"]["small"]},
                    "power": face["power"] if "power" in face.keys() and "toughness" in face.keys() else 0,
                    "toughness": face["toughness"] if "power" in face.keys() and "toughness" in face.keys() else 0,
                    "mana_cost": face["mana_cost"],
                    "loyalty": face["loyalty"] if "loyalty" in face.keys() else 0,
                }
                for side, face in enumerate(card["card_faces"])
            ],
        }
    elif card["layout"] in ["adventure"]:
        extra_obj = {
            "oracle_text": make_oracle_splitadventure(card),
            "image_uris": {"normal": card["image_uris"]["normal"], "small": card["image_uris"]["small"]},
            "power": 0,
            "toughness": 0,
            "mana_cost": card["mana_cost"],
            "loyalty": card["loyalty"] if "loyalty" in card.keys() else 0,
        }
    elif card["layout"] == "Vanguard" or card["layout"] == "vanguard":
        extra_obj = {
            "oracle_text": make_oracle_vanguard(card),
            "image_uris": {"normal": card["image_uris"]["normal"]},
            "power": 0,
            "toughness": 0,
            "mana_cost": card["mana_cost"],
            "loyalty": 0,
        }
    elif card["layout"] in ["reversible_card"]:
        extra_obj = {
            "card_faces": [
                {
                    "name": face["name"],
                    "type_line": face["type_line"],
                    "oracle_text": make_oracle_dfc(card, side == 0),
                    "image_uris": {"normal": face["image_uris"]["normal"]},
                    "power": 0,
                    "toughness": 0,
                    "mana_cost": face["mana_cost"],
                    "loyalty": 0,
                }
                for side, face in enumerate(card["card_faces"])
            ],
            "type_line": card["card_faces"][0]["type_line"] + " // " + card["card_faces"][1]["type_line"],
            "cmc": card["card_faces"][0]["cmc"],
            "oracle_id": card["card_faces"][0]["oracle_id"],
        }
    else:
        extra_obj = {
            "oracle_text": make_oracle_normal(card),
            "image_uris": {"normal": card["image_uris"]["normal"], "small": card["image_uris"]["small"]},
            "power": card["power"] if "power" in card.keys() and "toughness" in card.keys() else 0,
            "toughness": card["toughness"] if "power" in card.keys() and "toughness" in card.keys() else 0,
            "mana_cost": card["mana_cost"],
            "loyalty": card["loyalty"] if "loyalty" in card.keys() else 0,
        }
    card_obj = {**card_obj, **extra_obj}
    return card_obj
