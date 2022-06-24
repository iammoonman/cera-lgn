import random
import requests
import time
import re
import ijson


class Pack:
    """Represents one stack of cards output to the bag."""

    transformAttrs = {
        "posX": 0.0,
        "posY": 0.0,
        "posZ": 0.0,
        "rotX": 0.0,
        "rotY": 0.0,
        "rotZ": 0.0,
        "scaleX": 1.0,
        "scaleY": 1.0,
        "scaleZ": 1.0,
    }
    """Required for TTS."""
    colorAttrs = {"r": 0.0, "g": 0.0, "b": 0.0}
    """Required for TTS."""
    foilTransformAttrs = {
        "posX": 0.0,
        "posY": 0.25,
        "posZ": 0.0,
        "rotX": 90.0,
        "rotY": 180.0,
        "rotZ": 0.0,
        "scaleX": 0.7006438 * 3.1,
        "scaleY": 0.9999966 * 3.1,
        "scaleZ": 15.3846169 * 3.1,
    }
    """Required for TTS."""
    StarFoil = {
        "CustomDecal": {
            "Name": "StarFoil",
            "ImageURL": "https://i.imgur.com/QnxyMMK.png",
            "Size": 1.0,
        },
        "Transform": foilTransformAttrs,
    }
    """Standard diagonal rainbow gradient with small star glyph in the bottom left corner of the art."""
    SetSpiralFoil = {
        "CustomDecal": {
            "Name": "SetSpiralFoil",
            "ImageURL": "https://i.imgur.com/Roq6TDw.png",
            "Size": 1.0,
        },
        "Transform": foilTransformAttrs,
    }
    """Scattered set symbols with a spiraling rainbow coloring over the stroke."""
    VoronoiFoil = {
        "CustomDecal": {
            "Name": "VoronoiFoil",
            "ImageURL": "https://i.imgur.com/oIgRF2r.png",
            "Size": 1.0,
        },
        "Transform": foilTransformAttrs,
    }
    """Voronoi diagram, filled with separate rainbow patters to resemble shattered glass."""

    def __init__(self):
        """Create a pack."""
        self.DeckIDs = []
        self.CustomDeck = {}
        self.ContainedObjects = []
        self.deckObject = {
            "Name": "Deck",
            "Transform": self.transformAttrs,
            "ColorDiffuse": self.colorAttrs,
            "DeckIDs": [],
            "CustomDeck": {},
            "ContainedObjects": [],
        }
        self.Decals = [random.choice([Pack.StarFoil, Pack.SetSpiralFoil, Pack.VoronoiFoil])]
        self.Counter = 0
        """Uniquely identifies each card in the pack."""

    class CardBlob:
        def __init__(self, cardData, counter, isFoil=False, decals=[]):
            """Represents one card."""
            self.Nickname = f'{cardData["name"]}\n{cardData["type_line"]} {round(cardData["cmc"])}MV'
            """Shows up in TTS as the name of the object.
            
            Contains the name, mana value, and type line for easy searching."""
            self.Name = "Card"
            """Default property which identifies the type of this object. \"Card\" only."""
            self.Memo = cardData["oracle_id"]
            """Contains oracle id for tracking using the importer."""
            self.Description = ""
            """Contains oracle text, power/toughness, and loyalty if any.
            
            Formatted on import."""
            if "card_faces" in cardData.keys() and "adventure" != cardData["layout"] and "split" != cardData["layout"]:
                self.Description = cardData["card_faces"][0]["oracle_text"]
            else:
                # Oracle text formatting is applied on import
                self.Description = cardData["oracle_text"]
            self.Transform = Pack.transformAttrs
            self.ColorDiffuse = Pack.colorAttrs
            self.CardID = counter * 100
            self.frontImage = {
                "FaceURL": re.sub(
                    "\?\d+$",
                    "",
                    cardData["card_faces"][0]["image_uris"]["png"]
                    if "card_faces" in cardData.keys()
                    and "adventure" != cardData["layout"]
                    and "split" != cardData["layout"]
                    else cardData["image_uris"]["png"],
                ),
                "BackURL": "https://i.imgur.com/TyC0LWj.jpg",
                "NumWidth": 1,
                "NumHeight": 1,
                "BackIsHidden": True,
                "UniqueBack": False,
            }
            self.CustomDeck = self.frontImage
            self.AttachedDecals = decals if isFoil else []
            self.States = {}
            if "card_faces" in cardData.keys() and "adventure" != cardData["layout"] and "split" != cardData["layout"]:
                backImage = {
                    "FaceURL": re.sub("\?\d+$", "", cardData["card_faces"][1]["image_uris"]["png"]),
                    "BackURL": "https://i.imgur.com/TyC0LWj.jpg",
                    "NumWidth": 1,
                    "NumHeight": 1,
                    "BackIsHidden": True,
                    "UniqueBack": False,
                }
                backName = f'{cardData["name"]}\n{cardData["type_line"]} {round(cardData["cmc"])}MV'
                backDescription = cardData["card_faces"][1]["oracle_text"]
                self.States = {
                    "2": {
                        "Name": "Card",
                        "Nickname": backName,
                        "Description": backDescription,
                        "Transform": Pack.transformAttrs,
                        "ColorDiffuse": Pack.colorAttrs,
                        "CardID": int((counter * 1000) - 100) * 100,
                        "CustomDeck": {str((counter * 1000) - 100): backImage},
                        "AttachedDecals": (decals if isFoil else []),
                    }
                }

        def toDict(self):
            """Returns a dictionary for the final JSON."""
            return {
                "Nickname": self.Nickname,
                "Name": self.Name,
                "Memo": self.Memo,
                "Description": self.Description,
                "ColorDiffuse": self.ColorDiffuse,
                "Transform": self.Transform,
                "CardID": int(self.CardID),
                "CustomDeck": {str(self.CardID // 100): self.CustomDeck},
                "States": self.States,
                "AttachedDecals": self.AttachedDecals,
            }

    def import_cards(self, cardDataList, foilIndexes=[]):
        """Takes a list of card objects from a Scryfall search."""
        for index, item in enumerate(cardDataList):
            self.ContainedObjects.append(
                tempCard := self.CardBlob(item, self.Counter + 1, index in foilIndexes, self.Decals).toDict()
            )
            self.DeckIDs.append(int((self.Counter + 1) * 100))
            self.CustomDeck[str((self.Counter + 1) * 100)] = tempCard["CustomDeck"]
            self.Counter += 1
        return

    def toDict(self):
        """Returns a dictionary for the final JSON."""
        return {
            "Name": "Deck",
            "Transform": self.transformAttrs,
            "ColorDiffuse": self.colorAttrs,
            "DeckIDs": [int(card["CardID"]) for card in self.ContainedObjects],
            "CustomDeck": {
                str(card["CardID"] // 100): card["CustomDeck"][str(card["CardID"] // 100)]
                for card in self.ContainedObjects
            },
            "ContainedObjects": self.ContainedObjects,
        }


def scryfall_set(setcode):
    """Returns list of JSON data containing all cards from the set."""
    full_set_json = []
    time.sleep(0.25)
    response = requests.get(
        f"https://api.scryfall.com/cards/search?q=set%3A{setcode}&unique=prints",
        headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"},
    )
    full_set_json += (resjson := response.json())["data"]
    while resjson["has_more"]:
        time.sleep(0.25)
        response = requests.get(
            resjson["next_page"],
            headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"},
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
            card_obj = {
                "oracle_id": o["oracle_id"],
                "cmc": o["cmc"],
                "type_line": o["type_line"],
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
                            "image_uris": {"png": i["image_uris"]["png"]},
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
                    "name": o["name"],
                    "type_line": o["type_line"],
                    "oracle_text": make_oracle_splitadventure(o),
                    "image_uris": {"png": o["image_uris"]["png"]},
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
                            "image_uris": {"png": o["image_uris"]["png"]},
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
                    "name": o["name"],
                    "type_line": o["type_line"],
                    "oracle_text": make_oracle_splitadventure(o),
                    "image_uris": {"png": o["image_uris"]["png"]},
                    "power": 0,  # o["power"] if "power" in o.keys() and "toughness" in o.keys() else 0,
                    "toughness": 0,  # o["toughness"] if "power" in o.keys() and "toughness" in o.keys() else 0,
                    "mana_cost": o["mana_cost"],
                    "loyalty": o["loyalty"] if "loyalty" in o.keys() else 0,
                }
            else:
                extra_obj = {
                    "name": o["name"],
                    "type_line": o["type_line"],
                    "oracle_text": make_oracle_normal(o),
                    "image_uris": {"png": o["image_uris"]["png"]},
                    "power": o["power"] if "power" in o.keys() and "toughness" in o.keys() else 0,
                    "toughness": o["toughness"] if "power" in o.keys() and "toughness" in o.keys() else 0,
                    "mana_cost": o["mana_cost"],
                    "loyalty": o["loyalty"] if "loyalty" in o.keys() else 0,
                }
            card_obj = {**card_obj, **extra_obj}
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
    descriptionHold = "" if is_reverse else "[6E6E6E]"
    descriptionHold += "[b]" + face_1["name"] + " " + face_1["mana_cost"] + "[/b]\n"
    descriptionHold += face_1["type_line"] + "\n"
    descriptionHold += italicize_reminder(face_1["oracle_text"])
    descriptionHold += (
        f"\n[b]{face_1['power']}/{face_1['toughness']}[/b]"
        if ("Creature" in face_1["type_line"] or "Vehicle" in face_1["type_line"])
        else ""
    )
    descriptionHold += f"\n[b]{face_1['loyalty']}[/b] Starting Loyalty" if "loyalty" in face_1.keys() else ""
    descriptionHold += "\n"
    descriptionHold += "[6E6E6E]" if is_reverse else "[-]"
    descriptionHold += "\n"
    descriptionHold += "[b]" + face_2["name"] + " " + face_2["mana_cost"] + "[/b]\n"
    descriptionHold += face_2["type_line"] + "\n"
    descriptionHold += italicize_reminder(face_2["oracle_text"])
    descriptionHold += (
        f"\n[b]{face_2['power']}/{face_2['toughness']}[/b]"
        if ("Creature" in face_2["type_line"] or "Vehicle" in face_2["type_line"])
        else ""
    )
    descriptionHold += f"\n[b]{face_2['loyalty']}[/b] Starting Loyalty" if "loyalty" in face_2.keys() else ""
    descriptionHold += "[-]" if is_reverse else ""
    return descriptionHold


def make_oracle_normal(card_data):
    descriptionHold = italicize_reminder(card_data["oracle_text"])
    descriptionHold += (
        f"\n[b]{card_data['power']}/{card_data['toughness']}[/b]"
        if ("Creature" in card_data["type_line"] or "Vehicle" in card_data["type_line"])
        and "adventure" != card_data["layout"]
        else ""
    )
    descriptionHold += (
        f"\n[b]{card_data['loyalty']}[/b] Starting Loyalty" if "Planeswalker" in card_data["type_line"] else ""
    )
    return descriptionHold


def make_oracle_splitadventure(card_data):
    descriptionHold = (
        "[b]"
        + f'[b]{card_data["card_faces"][0]["name"]} {card_data["card_faces"][0]["mana_cost"]}[/b]'
        + "\n"
        + card_data["card_faces"][0]["type_line"]
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
