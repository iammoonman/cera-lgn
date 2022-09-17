import time
import requests
import ijson
import json
import re


def scryfall_collection(cardlist, out_dict=False):
    """Returns a list of JSON data from Scryfall, parsed into the tts format.

    Input uses [ set , name ].

    Don't input more than 75 card objects."""
    if len(cardlist) > 74:
        return None
    time.sleep(0.25)
    response = requests.post(
        f"https://api.scryfall.com/cards/collection",
        json={"identifiers": [{"set": i[0], "name": i[1]} for i in cardlist]},
        headers={
            "User-Agent": "Python 3.9.13 CERA",
            "Content-Type": "application/json",
        },
    )
    f_n = response.json()["data"]
    out = []
    out_2 = {}
    for item in f_n:
        c_obj = tts_parse(item)
        out.append(c_obj)
        out_2[c_obj["name"] + c_obj["set"]] = c_obj
    if out_dict:
        return out_2
    return out


def scryfall_set(setcode):
    """Returns list of JSON data containing all cards from the set. Deprecated."""
    full_set_json = []
    time.sleep(0.25)
    response = requests.get(
        f"https://api.scryfall.com/cards/search?q=set%3A{setcode}&unique=prints",
        headers={"User-Agent": "Python 3.9.13 CERA"},
    )
    full_set_json += (resjson := response.json())["data"]
    while resjson["has_more"]:
        time.sleep(0.25)
        response = requests.get(
            resjson["next_page"],
            headers={"User-Agent": "Python 3.9.13 CERA"},
        )
        full_set_json += (resjson := response.json())["data"]
    return full_set_json


def ijson_collection(cardlist, out_dict=False):
    """Returns list of JSON data containing all cards from the list by collector_number and set."""
    blob_json = []
    out = {}
    f = open("default-cards.json", "rb")
    objects = ijson.items(f, "item")
    for o in objects:
        if [o["collector_number"], o["set"]] in cardlist:
            card_obj = tts_parse(o)
            blob_json.append(card_obj)
            out[o["collector_number"] + o["set"]] = card_obj
        if len(blob_json) == len(cardlist):
            break
    f.close()
    if out_dict:
        return out
    return blob_json


def italicize_reminder(text: str):
    out = re.sub(r"\(", "[i](", text)
    out = re.sub(r"\)", ")[/i]", out)
    return out


def make_oracle_dfc(card_dota, is_reverse=False):
    face_1 = card_dota["card_faces"][0]
    face_2 = card_dota["card_faces"][1]
    descriptionHold = (
        ("" if is_reverse else "[6E6E6E]")
        + "[b]"
        + face_1["name"]
        + " "
        + face_1["mana_cost"]
        + "[/b]\n"
        + face_1["type_line"]
        + plus_rarity(card_dota["rarity"])
        + "\n"
        + italicize_reminder(face_1["oracle_text"])
        + (
            f"\n[b]{face_1['power']}/{face_1['toughness']}[/b]"
            if ("Creature" in face_1["type_line"] or "Vehicle" in face_1["type_line"])
            else ""
        )
        + (
            f"\n[b]{face_1['loyalty']}[/b] Starting Loyalty"
            if "loyalty" in face_1.keys()
            else "" + "\n" + "[6E6E6E]"
            if is_reverse
            else "[-]"
        )
        + "\n"
        + "[b]"
        + face_2["name"]
        + " "
        + face_2["mana_cost"]
        + "[/b]\n"
        + face_2["type_line"]
        + plus_rarity(card_dota["rarity"])
        + "\n"
        + italicize_reminder(face_2["oracle_text"])
        + (
            f"\n[b]{face_2['power']}/{face_2['toughness']}[/b]"
            if ("Creature" in face_2["type_line"] or "Vehicle" in face_2["type_line"])
            else ""
        )
        + (f"\n[b]{face_2['loyalty']}[/b] Starting Loyalty" if "loyalty" in face_2.keys() else "")
        + ("[-]" if is_reverse else "")
    )
    return descriptionHold


def make_oracle_normal(card_data):
    descriptionHold = (
        "[b]"
        + card_data["name"]
        + card_data["mana_cost"]
        + "[/b]"
        + "\n"
        + card_data["type_line"]
        + plus_rarity(card_data["rarity"])
        + "\n"
        + italicize_reminder(card_data["oracle_text"])
        + (
            f"\n[b]{card_data['power']}/{card_data['toughness']}[/b]"
            if ("Creature" in card_data["type_line"] or "Vehicle" in card_data["type_line"])
            and "adventure" != card_data["layout"]
            else ""
        )
        + (f"\n[b]{card_data['loyalty']}[/b] Starting Loyalty" if "Planeswalker" in card_data["type_line"] else "")
    )
    return descriptionHold


def make_oracle_splitadventure(card_data):
    descriptionHold = (
        "[b]"
        + f'[b]{card_data["card_faces"][0]["name"]} {card_data["card_faces"][0]["mana_cost"]}[/b]'
        + "\n"
        + card_data["card_faces"][0]["type_line"]
        + plus_rarity(card_data["rarity"])
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
        + card_data["card_faces"][1]["type_line"]
        + plus_rarity(card_data["rarity"])
        + "\n"
        + italicize_reminder(card_data["card_faces"][1]["oracle_text"])
        + "\n"
        + (
            "\n[b]" + card_data["card_faces"][1]["power"] + "/" + card_data["card_faces"][1]["toughness"] + "[/b]\n"
            if "power" in card_data["card_faces"][1].keys() and "toughness" in card_data["card_faces"][1].keys()
            else ""
        )
    )
    return descriptionHold


def make_oracle_reversible(card_data):
    return


def make_oracle_vanguard(card_data):
    descriptionHold = (
        "[b]"
        + card_data["name"]
        + card_data["mana_cost"]
        + "[/b]"
        + "\n"
        + card_data["type_line"]
        + plus_rarity(card_data["rarity"])
        + "\n"
        + italicize_reminder(card_data["oracle_text"])
        + "\n"
        + "Life: "
        + card_data["life_modifier"]
        + " + 20 = [b]"
        + (20 + int(card_data["life_modifier"]))
        + "[/b]"
        + "\n"
        + "Hand: "
        + card_data["hand_modifier"]
        + " + 7 = [b]"
        + (7 + int(card_data["hand_modifier"]))
        + "[/b]"
    )
    return descriptionHold


def plus_rarity(rarity):
    # Colors scraped from Scryfall
    if rarity == "mythic":
        # f64800
        return "[f64800]「M」[-]"
    elif rarity == "rare":
        # c5b37c
        return "[c5b37c]「R」[-]"
    elif rarity == "uncommon":
        # 6c848c
        return "[6c848c]「U」[-]"
    elif rarity == "common":
        # 16161d
        return "「C」"
    elif rarity == "special":
        # 905d98
        return "[905d98]「S」[-]"
    elif rarity == "bonus":
        # 9c202b
        return "[9c202b]「B」[-]"
    return ""


def tts_parse(o):
    card_obj = {
        "oracle_id": o["oracle_id"] if "oracle_id" in o.keys() else "",
        "cmc": o["cmc"] if "cmc" in o.keys() else 0,
        "type_line": o["type_line"] if "type_line" in o.keys() else "",
        "layout": o["layout"],
        "set": o["set"],
        "name": o["name"],
        "collector_number": o["collector_number"],
    }
    if "card_faces" in o.keys() and o["layout"] in ["transform", "modal_dfc"]:
        extra_obj = {
            "card_faces": [
                {
                    "name": i["name"],
                    "type_line": i["type_line"],
                    "oracle_text": make_oracle_dfc(o, c == 0),
                    "image_uris": {"normal": i["image_uris"]["normal"], "small": i["image_uris"]["small"]},
                    "power": i["power"] if "power" in i.keys() and "toughness" in i.keys() else 0,
                    "toughness": i["toughness"] if "power" in i.keys() and "toughness" in i.keys() else 0,
                    "mana_cost": i["mana_cost"],
                    "loyalty": i["loyalty"] if "loyalty" in i.keys() else 0,
                }
                for c, i in enumerate(o["card_faces"])
            ],
        }
    elif "card_faces" in o.keys() and o["layout"] in ["split"]:
        extra_obj = {
            "type_line": o["type_line"],
            "oracle_text": make_oracle_splitadventure(o),
            "image_uris": {"normal": o["image_uris"]["normal"], "small": o["image_uris"]["small"]},
            "power": o["power"] if "power" in o.keys() and "toughness" in o.keys() else 0,
            "toughness": o["toughness"] if "power" in o.keys() and "toughness" in o.keys() else 0,
            "mana_cost": o["mana_cost"],
            "loyalty": o["loyalty"] if "loyalty" in o.keys() else 0,
        }
    elif "card_faces" in o.keys() and o["layout"] in ["flip"]:
        extra_obj = {
            "card_faces": [
                {
                    "name": i["name"],
                    "type_line": i["type_line"],
                    "oracle_text": make_oracle_dfc(o, c == 0),
                    "image_uris": {"normal": o["image_uris"]["normal"], "small": o["image_uris"]["small"]},
                    "power": i["power"] if "power" in i.keys() and "toughness" in i.keys() else 0,
                    "toughness": i["toughness"] if "power" in i.keys() and "toughness" in i.keys() else 0,
                    "mana_cost": i["mana_cost"],
                    "loyalty": i["loyalty"] if "loyalty" in i.keys() else 0,
                }
                for c, i in enumerate(o["card_faces"])
            ],
        }
    elif "card_faces" in o.keys() and o["layout"] in ["adventure"]:
        extra_obj = {
            "oracle_text": make_oracle_splitadventure(o),
            "image_uris": {"normal": o["image_uris"]["normal"], "small": o["image_uris"]["small"]},
            "power": 0,
            "toughness": 0,
            "mana_cost": o["mana_cost"],
            "loyalty": o["loyalty"] if "loyalty" in o.keys() else 0,
        }
    elif "layout" == "vanguard":
        extra_obj = {
            "oracle_text": make_oracle_vanguard(o),
            "image_uris": {"normal": o["image_uris"]["normal"]},
            "power": 0,
            "toughness": 0,
            "mana_cost": o["mana_cost"],
            "loyalty": 0,
        }
    elif "reversible_card" in o["layout"]:
        extra_obj = {
            "card_faces": [
                {
                    "name": i["name"],
                    "type_line": i["type_line"],
                    "oracle_text": make_oracle_dfc(o, c == 0),
                    "image_uris": {"normal": i["image_uris"]["normal"]},
                    "power": 0,
                    "toughness": 0,
                    "mana_cost": i["mana_cost"],
                    "loyalty": 0,
                }
                for c, i in enumerate(o["card_faces"])
            ],
            "type_line": o["card_faces"][0]["type_line"] + " // " + o["card_faces"][1]["type_line"],
            "cmc": o["card_faces"][0]["cmc"],
            "oracle_id": o["card_faces"][0]["oracle_id"],
        }
    else:
        extra_obj = {
            "oracle_text": make_oracle_normal(o),
            "image_uris": {"normal": o["image_uris"]["normal"], "small": o["image_uris"]["small"]},
            "power": o["power"] if "power" in o.keys() and "toughness" in o.keys() else 0,
            "toughness": o["toughness"] if "power" in o.keys() and "toughness" in o.keys() else 0,
            "mana_cost": o["mana_cost"],
            "loyalty": o["loyalty"] if "loyalty" in o.keys() else 0,
        }
    card_obj = {**card_obj, **extra_obj}
    return card_obj
