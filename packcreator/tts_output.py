import random
from . import p_creator
from . import point_slicer
import json
import requests
import time
import re
import datetime
import ijson


class Pack:
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
    StarFoil = {
        "CustomDecal": {
            "Name": "StarFoil",
            "ImageURL": "https://i.imgur.com/QnxyMMK.png",
            "Size": 1.0,
        },
        "Transform": {
            "posX": 0.0,
            "posY": 0.25,
            "posZ": 0.0,
            "rotX": 90.0,
            "rotY": 180.0,
            "rotZ": 0.0,
            "scaleX": 0.7006438 * 3.1,
            "scaleY": 0.9999966 * 3.1,
            "scaleZ": 15.3846169 * 3.1,
        },
    }
    """Standard diagonal rainbow gradient with small star glyph in the bottom left corner of the art."""
    SetSpiralFoil = {
        "CustomDecal": {
            "Name": "SetSpiralFoil",
            "ImageURL": "https://i.imgur.com/Roq6TDw.png",
            "Size": 1.0,
        },
        "Transform": {
            "posX": 0.0,
            "posY": 0.25,
            "posZ": 0.0,
            "rotX": 90.0,
            "rotY": 180.0,
            "rotZ": 0.0,
            "scaleX": 0.7006438 * 3.1,
            "scaleY": 0.9999966 * 3.1,
            "scaleZ": 15.3846169 * 3.1,
        },
    }
    """Scattered set symbols with a spiraling rainbow coloring over the stroke."""
    VoronoiFoil = {
        "CustomDecal": {
            "Name": "VoronoiFoil",
            "ImageURL": "https://i.imgur.com/oIgRF2r.png",
            "Size": 1.0,
        },
        "Transform": {
            "posX": 0.0,
            "posY": 0.25,
            "posZ": 0.0,
            "rotX": 90.0,
            "rotY": 180.0,
            "rotZ": 0.0,
            "scaleX": 0.7006438 * 3.1,
            "scaleY": 0.9999966 * 3.1,
            "scaleZ": 15.3846169 * 3.1,
        },
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
            self.Nickname = (
                f'{cardData["card_faces"][0]["name"]}\n{cardData["card_faces"][0]["type_line"]} {round(cardData["card_faces"][0]["cmc"]) if "cmc" in cardData["card_faces"][0].keys() else round(cardData["cmc"])}MV'
                if "card_faces" in cardData.keys()
                else f'{cardData["name"]}\n{cardData["type_line"]} {round(cardData["cmc"])}MV'
            )
            self.Name = "Card"
            """Default property which identifies the type of this object. \"Card\" only."""
            self.Memo = cardData["oracle_id"]
            """Contains oracle id for tracking using the importer."""
            descriptionHold = ""
            if "oracle_text" not in cardData.keys():
                descriptionHold += (
                    "" if "card_faces" not in cardData.keys() else cardData["card_faces"][0]["oracle_text"]
                )
            else:
                descriptionHold += cardData["oracle_text"]
            descriptionHold += (
                (
                    f"\n[b]{cardData['power']}/{cardData['toughness']}[/b]"
                    if "Creature" in cardData["type_line"] or "Vehicle" in cardData["type_line"]
                    else ""
                )
                if "card_faces" not in cardData.keys()
                else (
                    f"\n[b]{cardData['card_faces'][0]['power']}/{cardData['card_faces'][0]['toughness']}[/b]"
                    if "Creature" in cardData["type_line"] or "Vehicle" in cardData["type_line"]
                    else ""
                )
            )
            descriptionHold += (
                f"\n[b]{cardData['loyalty']}[/b] Starting Loyalty" if "Planeswalker" in cardData["type_line"] else ""
            )
            self.Description = f"{descriptionHold}"
            """Contains oracle text, if any."""
            self.Transform = Pack.transformAttrs
            self.ColorDiffuse = Pack.colorAttrs
            self.CardID = counter * 100
            self.frontImage = {
                "FaceURL": re.sub(
                    "\?\d+$",
                    "",
                    cardData["card_faces"][0]["image_uris"]["png"]
                    if "card_faces" in cardData.keys()
                    and "Adventure" not in cardData["layout"]
                    and "split" != cardData["layout"]
                    and "flip" != cardData["layout"]
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
            if (
                "card_faces" in cardData.keys()
                and "Adventure" not in cardData["layout"]
                and "split" != cardData["layout"]
                and "flip" != cardData["layout"]
            ):
                backImage = {
                    "FaceURL": re.sub("\?\d+$", "", cardData["card_faces"][1]["image_uris"]["png"]),
                    "BackURL": "https://i.imgur.com/TyC0LWj.jpg",
                    "NumWidth": 1,
                    "NumHeight": 1,
                    "BackIsHidden": True,
                    "UniqueBack": False,
                }
                backName = f'{cardData["card_faces"][1]["name"]}\n{cardData["card_faces"][1]["type_line"]} {round(cardData["card_faces"][1]["cmc"]) if "cmc" in cardData["card_faces"][1].keys() else round(cardData["cmc"])}MV'
                backDescription = ""
                backDescription += (
                    ""
                    if "oracle_text" not in cardData["card_faces"][1].keys()
                    else cardData["card_faces"][1]["oracle_text"]
                )
                backDescription += (
                    f"\n[b]{cardData['card_faces'][1]['power']}/{cardData['card_faces'][1]['toughness']}[/b]"
                    if "Creature" in cardData["card_faces"][1]["type_line"]
                    or "Vehicle" in cardData["card_faces"][1]["type_line"]
                    else ""
                )
                backDescription += (
                    f"\n[b]{cardData['card_faces'][1]['loyalty']}[/b] Starting Loyalty"
                    if "Planeswalker" in cardData["card_faces"][1]["type_line"]
                    else ""
                )
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


def get_packs(setcode, num_packs, land_pack=False):
    """Returns a JSON save file for Tabletop Simulator."""
    with open(
        f"setjson/{setcode}.json" if __name__ == "__main__" else f"packcreator/setjson/{setcode}.json", "rb"
    ) as f:
        setJSON = json.load(f)
    save = {
        "ObjectStates": [
            {
                "Name": "Bag",
                "Transform": {
                    "posX": 0.0,
                    "posY": 0.0,
                    "posZ": 0.0,
                    "rotX": 0.0,
                    "rotY": 0.0,
                    "rotZ": 0.0,
                    "scaleX": 1.0,
                    "scaleY": 1.0,
                    "scaleZ": 1.0,
                },
                "Nickname": f"{num_packs} Packs of {setcode}",
                "ColorDiffuse": {"r": 0.0, "g": 0.0, "b": 0.0},
                "Bag": {"Order": 0},
                "ContainedObjects": [],
            }
        ]
    }
    abbr = setJSON["set_code"]
    set_info = scryfall_set(abbr)
    codes = [abbr]
    for _ in range(num_packs):
        (raw_cn_cards, foil_indexes,) = p_creator.generatepack_c1c2_special(
            sheet_index_func=lambda a: point_slicer.get_number(a),
            setJSON=setJSON,
        )
        # Find the scryfall set data for the cards in the pack. Could be varied.
        # Grabs the entire set to reduce queries. Watch for memory usage.
        for new_setcode in list(filter(lambda x: x[1] not in codes, raw_cn_cards)):
            set_info += scryfall_set(new_setcode[1])
            codes.append(new_setcode[1])
        pack_to_add = Pack()
        pack_to_add.import_cards(
            [
                next(c for c in set_info if c["collector_number"] == cn_pair[0] and c["set"] == cn_pair[1])
                for cn_pair in raw_cn_cards
            ],
            foil_indexes,
        )
        save["ObjectStates"][0]["ContainedObjects"].append(pack_to_add.toDict())
    if land_pack:
        basicslist = list(
            filter(
                lambda x: x["name"] in ["Plains", "Island", "Swamp", "Mountain", "Forest"],
                set_info,
            )
        )
        if len(basicslist) >= 5:
            pack_to_add = Pack()
            pack_to_add.import_cards(basicslist)
            save["ObjectStates"][0]["ContainedObjects"].append(pack_to_add.toDict())
    return save


def get_packs_v3(setcode, num_packs, land_pack=False):
    """Returns a JSON save file for Tabletop Simulator. Also returns logging information."""
    with open(f"sj3/{setcode}.json" if __name__ == "__main__" else f"packcreator/sj3/{setcode}.json", "rb") as f:
        setJSON = json.load(f)
    save = {
        "ObjectStates": [
            {
                "Name": "Bag",
                "Transform": {
                    "posX": 0.0,
                    "posY": 0.0,
                    "posZ": 0.0,
                    "rotX": 0.0,
                    "rotY": 0.0,
                    "rotZ": 0.0,
                    "scaleX": 1.0,
                    "scaleY": 1.0,
                    "scaleZ": 1.0,
                },
                "Nickname": f"packs of {setcode}",
                "ColorDiffuse": {"r": 0.0, "g": 0.0, "b": 0.0},
                "Bag": {"Order": 0},
                "ContainedObjects": [],
            }
        ]
    }
    # log = {
    #     "seeds": [],
    #     "setcode": setcode,
    #     "num_p": num_packs,
    #     "timestamp": datetime.datetime.now().isoformat(),
    # }
    # Calculate duplicate control specs
    duplicate_control_list = {}
    if "flag_data" in setJSON.keys():
        if "duplicate_control" in setJSON["flag_data"].keys():
            duplicate_control_list = {
                k: point_slicer.get_sampled_numbers(num_packs * i["max_length"], i["count"])
                for k, i in setJSON["flag_data"]["duplicate_control"]["slots_counts"].items()
            }
            # Log duplicate_control_list
            # log["d_c"] = duplicate_control_list[:]
    all_packs = []
    for _ in range(num_packs):
        raw_cn_cards, foil_indexes, seed = p_creator.pack_gen_v3(set=setJSON, d_c=duplicate_control_list)
        # Log the seed
        # log["seeds"].append(seed)
        all_packs.append([raw_cn_cards, foil_indexes])
    all_cn_sets = []
    for p in all_packs:
        all_cn_sets += p[0]
    set_info = ijson_collection(all_cn_sets)
    for p in all_packs:
        # print([a['name'] for a in set_info])
        # print(len(raw_cn_cards))
        # print(len(set_info))
        new_colle = []
        for crd in p[0]:
            new_colle += [x for x in set_info if x["collector_number"] == crd[0] and x["set"] == crd[1]]
        # print([a['name'] for a in new_colle])
        pack_to_add = Pack()
        pack_to_add.import_cards(
            new_colle,
            p[1],
        )
        save["ObjectStates"][0]["ContainedObjects"].append(pack_to_add.toDict())
    if land_pack:
        pack_to_add = Pack()
        pack_to_add.import_cards(
            [
                list(
                    filter(
                        lambda x: x["name"] in ["Plains", "Island", "Swamp", "Mountain", "Forest"],
                        set_info,
                    )
                )
            ]
        )
        save["ContainedObjects"].append(pack_to_add.toDict())
    return save  # , log


def get_cube(cc_id):
    """Returns a JSON save file for Tabletop Simulator."""
    import csv

    save = {
        "ObjectStates": [
            {
                "Name": "Bag",
                "Transform": {
                    "posX": 0.0,
                    "posY": 0.0,
                    "posZ": 0.0,
                    "rotX": 0.0,
                    "rotY": 0.0,
                    "rotZ": 0.0,
                    "scaleX": 1.0,
                    "scaleY": 1.0,
                    "scaleZ": 1.0,
                },
                "Nickname": f"{cc_id}",
                "ColorDiffuse": {"r": 0.0, "g": 0.0, "b": 0.0},
                "Bag": {"Order": 0},
                "ContainedObjects": [],
            }
        ]
    }
    response = requests.get(
        f"https://cubecobra.com/cube/download/csv/{cc_id}?primary=Color%20Category&secondary=Types-Multicolor&tertiary=Mana%20Value&quaternary=Alphabetical&showother=false",
        headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"},
    )
    reader = csv.DictReader(response.content.decode("utf-8").splitlines())
    if "Name" not in reader.fieldnames:  # Catching 404 errors in CubeCobra is much harder than it should be.
        return None
    templist = []
    the_cube = Pack()
    for row in reader:
        if row["Maybeboard"] == "true":
            continue
        templist.append([row["Collector Number"], row["Set"]])
    cardinfo = ijson_collection(templist, True)
    cubelist = []
    reader = csv.DictReader(response.content.decode("utf-8").splitlines())
    for row in reader:
        if row["Maybeboard"] == "true":
            continue
        c = cardinfo[row["Collector Number"]+row["Set"]]
        extras = {}
        if row["Image URL"] != "" and c["layout"] not in ["transform", "modal_dfc"]:
            extras = {"image_uris": {"png": row["Image URL"]}}
        if (row["Image URL"] != "" or row["Image Back URL"] != "") and c["layout"] in [
            "transform",
            "modal_dfc",
        ]:
            extras = {
                "card_faces": [
                    {**c["card_faces"][0], "image_uris": {"png": row["Image URL"]}}
                    if row["Image URL"] != ""
                    else {**c["card_faces"][0]},
                    {**c["card_faces"][1], "image_uris": {"png": row["Image Back URL"]}}
                    if row["Image Back URL"] != ""
                    else {**c["card_faces"][1]},
                ]
            }
        cubelist.append({**c, **extras})
    the_cube.import_cards(cubelist)
    save["ObjectStates"][0]["ContainedObjects"] = [the_cube.toDict()]
    return save


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


def ijson_collection(cardlist, out_dict = False):
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
                "collector_number": o["collector_number"],
            }
            if "card_faces" in o.keys() and o["layout"] in ["transform", "modal_dfc"]:
                extra_obj = {
                    "card_faces": [
                        {
                            "name": i["name"],
                            "type_line": i["type_line"],
                            "oracle_text": i["oracle_text"],
                            "image_uris": {"png": i["image_uris"]["png"]},
                            "power": i["power"] if "Creature" in i["type_line"] or "Vehicle" in i["type_line"] else 0,
                            "toughness": i["toughness"]
                            if "Creature" in i["type_line"] or "Vehicle" in i["type_line"]
                            else 0,
                            "mana_cost": i["mana_cost"],
                            "loyalty": i["loyalty"] if "Planeswalker" in i["type_line"] else 0,
                        }
                        for i in o["card_faces"]
                    ],
                }
            elif "card_faces" in o.keys() and o["layout"] in ["split"]:
                extra_obj = {
                    "name": o["name"],
                    "type_line": o["type_line"],
                    "oracle_text": o["card_faces"][0]["oracle_text"] + "\n" + o["card_faces"][1]["oracle_text"],
                    "image_uris": {"png": o["image_uris"]["png"]},
                    "power": o["power"] if "Creature" in o["type_line"] or "Vehicle" in o["type_line"] else 0,
                    "toughness": o["power"] if "Creature" in o["type_line"] or "Vehicle" in o["type_line"] else 0,
                    "mana_cost": o["mana_cost"],
                    "loyalty": o["loyalty"] if "Planeswalker" in o["type_line"] else 0,
                }
            elif "card_faces" in o.keys() and o["layout"] in ["flip"]:
                extra_obj = {
                    "card_faces": [
                        {
                            "name": i["name"],
                            "type_line": i["type_line"],
                            "oracle_text": i["oracle_text"],
                            "image_uris": {"png": o["image_uris"]["png"]},
                            "power": i["power"] if "Creature" in i["type_line"] or "Vehicle" in i["type_line"] else 0,
                            "toughness": i["toughness"]
                            if "Creature" in i["type_line"] or "Vehicle" in i["type_line"]
                            else 0,
                            "mana_cost": i["mana_cost"],
                            "loyalty": i["loyalty"] if "Planeswalker" in i["type_line"] else 0,
                        }
                        for i in o["card_faces"]
                    ],
                }
            else:
                extra_obj = {
                    "name": o["name"],
                    "type_line": o["type_line"],
                    "oracle_text": o["oracle_text"],
                    "image_uris": {"png": o["image_uris"]["png"]},
                    "power": o["power"] if "Creature" in o["type_line"] or "Vehicle" in o["type_line"] else 0,
                    "toughness": o["power"] if "Creature" in o["type_line"] or "Vehicle" in o["type_line"] else 0,
                    "mana_cost": o["mana_cost"],
                    "loyalty": o["loyalty"] if "Planeswalker" in o["type_line"] else 0,
                }
            card_obj = {**card_obj, **extra_obj}
            blob_json.append(card_obj)
            out[o["collector_number"]+o["set"]] = card_obj
        if len(blob_json) == len(cardlist):
            break
    f.close()
    if out_dict:
        return out
    return blob_json
