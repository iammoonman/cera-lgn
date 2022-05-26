import random
from . import p_creator
from . import point_slicer
import json
import requests
import time
import re
import datetime


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
                (f"\n[b]{cardData['power']}/{cardData['toughness']}[/b]" if "power" in cardData.keys() else "")
                if "card_faces" not in cardData.keys()
                else (
                    f"\n[b]{cardData['card_faces'][0]['power']}/{cardData['card_faces'][0]['toughness']}[/b]"
                    if "power" in cardData["card_faces"][0].keys()
                    else ""
                )
            )
            descriptionHold += f"\n[b]{cardData['loyalty']}[/b] Starting Loyalty" if "loyalty" in cardData.keys() else ""
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
                    and "Adventure" not in cardData["type_line"]
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
                and "Adventure" not in cardData["type_line"]
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
                    if "power" in cardData["card_faces"][1].keys()
                    else ""
                )
                backDescription += (
                    f"\n[b]{cardData['card_faces'][1]['loyalty']}[/b] Starting Loyalty"
                    if "loyalty" in cardData["card_faces"][1].keys()
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
    with open(f"setjson/{setcode}.json" if __name__ == "__main__" else f"packcreator/setjson/{setcode}.json", "rb") as f:
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
                "Nickname": f"{num_packs} Packs of {setcode}",
                "ColorDiffuse": {"r": 0.0, "g": 0.0, "b": 0.0},
                "Bag": {"Order": 0},
                "ContainedObjects": [],
            }
        ]
    }
    abbr = setJSON["default_set"]
    set_info = scryfall_set(abbr)
    codes = [abbr]
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
                k: point_slicer.get_sampled_numbers(num_packs * i["count"], i["max_length"])
                for k, i in setJSON["flag_data"]["duplicate_control"]["slots_counts"].items()
            }
            # Log duplicate_control_list
            # log["d_c"] = duplicate_control_list[:]
    for _ in range(num_packs):
        raw_cn_cards, foil_indexes, seed = p_creator.pack_gen_v3(set=setJSON, d_c=duplicate_control_list)
        # Log the seed
        # log["seeds"].append(seed)
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
    import copy

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
        if len(templist) == 10:  # Buffering to serve query length has an impact on sorting.
            # CubeCobra data is always fundamentally based on data from Scryfall. The query will not fail.
            response = requests.get(
                "https://api.scryfall.com/cards/search?q="
                + "".join(
                    [
                        f'(cn%3D"{i["Collector Number"]}"+set%3D{i["Set"]}){"+or+" if templist.index(i)<len(templist)-1 else ""}'
                        for i in templist
                    ]
                )
                + "&unique=prints",
                headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"},
            )
            holdhold = response.json()
            cards_to_import = []
            foil_indexes = []
            for i, n in enumerate(templist):
                # Convert the CubeCobra csv information to the Scryfall data used by the Pack class.
                # This will also catch duplicate cards.
                card_data = copy.deepcopy(
                    [
                        j
                        for j in holdhold["data"]
                        if j["collector_number"] == n["Collector Number"] and j["set"] == n["Set"]
                    ][0]
                )
                if n["Image URL"]:  # Catch whether the CubeCobra card has custom images.
                    if (
                        "card_faces" in card_data.keys()
                        and "Adventure" not in card_data["type_line"]
                        and "split" != card_data["layout"]
                        and "flip" != card_data["layout"]
                    ):
                        card_data["card_faces"][0]["image_uris"]["png"] = n["Image URL"]
                        if n["Image Back URL"]:
                            card_data["card_faces"][1]["image_uris"]["png"] = n["Image Back URL"]
                    else:
                        card_data["image_uris"]["png"] = n["Image URL"]
                cards_to_import.append(card_data)
                if n["Finish"] == "Foil":  # Catch the CubeCobra card being foiled.
                    foil_indexes.append(i)
            the_cube.import_cards(cards_to_import, foil_indexes)
            templist = []
            foil_indexes = []
            time.sleep(0.25)
        if row["Maybeboard"] == "false":  # Maybeboarded cards are included in the csv.
            templist.append(row)
    if len(templist) > 0:
        # Catch an uneven number of cards.
        response = requests.get(
            "https://api.scryfall.com/cards/search?q="
            + "".join(
                [
                    f'(cn%3D"{i["Collector Number"]}"+set%3D{i["Set"]}){"+or+" if templist.index(i)<len(templist)-1 else ""}'
                    for i in templist
                ]
            )
            + "&unique=prints",
            headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"},
        )
        holdhold = response.json()
        cards_to_import = []
        foil_indexes = []
        for i, n in enumerate(templist):
            card_data = copy.deepcopy(
                [
                    j
                    for j in holdhold["data"]
                    if j["collector_number"] == n["Collector Number"] and j["set"] == n["Set"]
                ][0]
            )
            if n["Image URL"]:
                if (
                    "card_faces" in card_data.keys()
                    and "Adventure" not in card_data["type_line"]
                    and "split" != card_data["layout"]
                    and "flip" != card_data["layout"]
                ):
                    print(card_data["name"])
                    card_data["card_faces"][0]["image_uris"]["png"] = n["Image URL"]
                    if n["Image Back URL"]:
                        card_data["card_faces"][1]["image_uris"]["png"] = n["Image Back URL"]
                else:
                    card_data["image_uris"]["png"] = n["Image URL"]
            cards_to_import.append(card_data)
            if n["Finish"] == "Foil":
                foil_indexes.append(i)
        the_cube.import_cards(cards_to_import, foil_indexes)
        templist = []
        foil_indexes = []
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
