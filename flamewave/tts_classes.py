import random
import re
from xml.etree import ElementTree

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


def blank_image(face, cardData):
    if is_split_card(cardData):
        if "W" in face["colors"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/K.png"
        if "U" in face["colors"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/L.png"
        if "B" in face["colors"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/M.png"
        if "R" in face["colors"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/N.png"
        if "G" in face["colors"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/O.png"
        return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/P.png"
    if len(face["colors"]) > 1:
        return "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/mcard.jpg"
    if "W" in face["colors"]:
        return "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/wcard.jpg"
    elif "U" in face["colors"]:
        return "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/ucard.jpg"
    elif "B" in face["colors"]:
        return "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/bcard.jpg"
    elif "R" in face["colors"]:
        return "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/rcard.jpg"
    elif "G" in face["colors"]:
        return "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/gcard.jpg"
    if "Basic" in face["type_line"]:
        return {"Plains": "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/wlcard.jpg", "Island": "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/ulcard.jpg", "Swamp": "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/blcard.jpg", "Mountain": "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/rlcard.jpg", "Forest": "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/glcard.jpg"}[face["name"]]
    if len(face["colors"]) == 0 and "Artifact" in face["type_line"]:
        return "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/acard.jpg"
    if len(face["colors"]) == 0 and "Land" in face["type_line"]:
        if len(cardData["color_identity"]) > 2:
            return "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/mlcard.jpg"
        if "W" in cardData["color_identity"] and "U" in cardData["color_identity"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/A.png"
        elif "W" in cardData["color_identity"] and "B" in cardData["color_identity"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/B.png"
        elif "W" in cardData["color_identity"] and "R" in cardData["color_identity"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/C.png"
        elif "W" in cardData["color_identity"] and "G" in cardData["color_identity"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/D.png"
        elif "U" in cardData["color_identity"] and "B" in cardData["color_identity"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/E.png"
        elif "U" in cardData["color_identity"] and "R" in cardData["color_identity"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/F.png"
        elif "U" in cardData["color_identity"] and "G" in cardData["color_identity"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/G.png"
        elif "B" in cardData["color_identity"] and "R" in cardData["color_identity"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/H.png"
        elif "B" in cardData["color_identity"] and "G" in cardData["color_identity"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/I.png"
        elif "R" in cardData["color_identity"] and "G" in cardData["color_identity"]:
            return "https://limitedperspectiverzp.s3.us-east-1.amazonaws.com/J.png"
        return "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/clcard.jpg"
    return "https://raw.githubusercontent.com/MagicSetEditorPacks/Full-Magic-Pack/refs/heads/main/data/magic-modules.mse-include/cards/375%20m15%20simple/xcard.png"


def write_xmlui(face, cardData, is_back_face=False) -> str:
    def add_child_text(node, alignment, text):
        textNode = ElementTree.SubElement(node, "Text")
        textNode.set("resizeTextMaxSize", "150")
        textNode.set("resizeTextForBestFit", "true")
        textNode.set("alignment", alignment)
        if text is not None:
            textNode.set("text", text)
        return textNode

    def add_child_panel(node, typ, height, width, position):
        panel = ElementTree.SubElement(node, typ)
        panel.set("height", height)
        panel.set("width", width)
        panel.set("position", position)
        return panel

    root = ElementTree.Element("Panel")
    root.set("height", "3050")
    root.set("width", "2150")
    root.set("position", "0 0 -30")
    root.set("rotation", "0 0 180")
    root.set("scale", "0.1 0.1 1")
    namebox = add_child_panel(root, "HorizontalLayout", "170", "1800", "0 1300 0")
    add_child_text(namebox, "MiddleLeft", face["name"])
    add_child_text(namebox, "MiddleRight", face["mana_cost"])
    typebox = add_child_panel(root, "Panel", "170", "1800", "0 -270 0")
    add_child_text(typebox, "MiddleLeft", face["type_line"])
    if is_split_card(cardData):
        textbox = add_child_panel(root, "Panel", "845", "900", "-450 -815 0")
        text_text = add_child_text(textbox, "UpperLeft", None)
        italicize_reminder_xml(text_text, face["oracle_text"] if "oracle_text" in face else "")
        othernamebox = add_child_panel(root, "HorizontalLayout", "130", "900", "460 -475 0")
        add_child_text(othernamebox, "MiddleLeft", cardData["card_faces"][1]["name"])
        add_child_text(othernamebox, "MiddleRight", cardData["card_faces"][1]["mana_cost"])
        othertypebox = add_child_panel(root, "Panel", "130", "900", "460 -605 0")
        add_child_text(othertypebox, "MiddleLeft", cardData["card_faces"][1]["type_line"])
        otheroraclebox = add_child_panel(root, "Panel", "590", "900", "460 -1000 0")
        otheroracletext = add_child_text(otheroraclebox, "UpperLeft", None)
        italicize_reminder_xml(otheroracletext, cardData["card_faces"][1]["oracle_text"])
    else:
        textbox = add_child_panel(root, "Panel", "845", "1800", "0 -815 0")
        text_text = add_child_text(textbox, "UpperLeft", None)
        italicize_reminder_xml(text_text, face["oracle_text"] if "oracle_text" in face else "")
    if is_creature_face(face):
        ptbox = ElementTree.SubElement(root, "Panel")
        ptbox.set("position", "800 -1350 0")
        ptbox.set("color", "#FFFFFF88")
        ptbox.set("height", "200")
        ptbox.set("width", "300")
        pt_text = ElementTree.SubElement(ptbox, "Text")
        pt_text.set("resizeTextMaxSize", "300")
        pt_text.set("resizeTextForBestFit", "true")
        pt_text.text = face["power"] + "/" + face["toughness"]
    if is_pw_face(face):
        ptbox = ElementTree.SubElement(root, "Panel")
        ptbox.set("position", "800 -1350 0")
        ptbox.set("color", "#FFFFFF88")
        ptbox.set("height", "200")
        ptbox.set("width", "300")
        pt_text = ElementTree.SubElement(ptbox, "Text")
        pt_text.set("resizeTextMaxSize", "300")
        pt_text.set("resizeTextForBestFit", "true")
        pt_text.text = face["loyalty"]
    if is_dfc(cardData) and not is_back_face:
        transformpanel = add_child_panel(root, "Panel", "170", "1600", "-300 -1400 0")
        transformtext = add_child_text(transformpanel, "MiddleLeft", f'Transforms into {cardData["card_faces"][1]["name"]}')
        transformtext.set("color", "White")
    return ElementTree.tostring(root, encoding="unicode")


def is_creature_face(face):
    return "power" in face and "toughness" in face and face["power"] is not None and face["toughness"] is not None


def italicize_reminder(text: str):
    out = re.sub(r"\(", "[i](", text)
    out = re.sub(r"\)", ")[/i]", out)
    return out


def italicize_reminder_xml(node, text: str):
    for string in re.split(r"((?=\()|(?<=\)))", text):
        if string.startswith("("):
            newI = ElementTree.SubElement(node, "i")
            newI.text = string
        else:
            newT = ElementTree.SubElement(node, None)
            newT.text = string


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


def is_pw_face(face):
    return "loyalty" in face and face["loyalty"] is not None


def is_battle_face(face):
    return "defense" in face.keys() and "Battle" in face["type_line"]


def is_split_card(card):
    return card["layout"] in ["adventure", "split", "flip", "prepare"]


def is_dfc(card):
    return "card_faces" in card and card["layout"] not in ["adventure", "split", "flip", "prepare"]


def write_description_normal(face, cardData):
    return f'[b]{face["name"]} {face["mana_cost"]}[/b]' + "\n" + f'{face["type_line"]} {rarity_icon(cardData["rarity"])}' + "\n" + italicize_reminder(face["oracle_text"]) + (f"\n[b]{face['power']}/{face['toughness']}[/b]" if is_creature_face(face) else "") + (f"\n[b]{face['loyalty']}[/b] Starting Loyalty" if is_pw_face(face) else "") + (f"\n[b]{face['defense']}[/b] Starting Defense" if is_battle_face(face) else "")


def write_description_dfc(card, is_reverse=False):
    return ("[6E6E6E]" if is_reverse else "") + write_description_normal(card["card_faces"][0], card) + ("\n\n[-]" if is_reverse else "[6E6E6E]\n\n") + write_description_normal(card["card_faces"][1], card) + ("[-]" if is_reverse else "")


def write_description_split(card):
    return "[b]" + f'[b]{card["card_faces"][0]["name"]} {card["card_faces"][0]["mana_cost"]}[/b]' + "\n" + f'{card["card_faces"][0]["type_line"]} {rarity_icon(card["rarity"])}' + "\n" + italicize_reminder(card["card_faces"][0]["oracle_text"]) + ("\n[b]" + card["card_faces"][0]["power"] + "/" + card["card_faces"][0]["toughness"] + "[/b]\n" if is_creature_face(card["card_faces"][0]) else "") + "\n" + f'[b]{card["card_faces"][1]["name"]} {card["card_faces"][1]["mana_cost"]}[/b]' + "\n" + f'{card["card_faces"][1]["type_line"]} {rarity_icon(card["rarity"])}' + "\n" + italicize_reminder(card["card_faces"][1]["oracle_text"]) + "\n" + ("\n[b]" + card["card_faces"][1]["power"] + "/" + card["card_faces"][1]["toughness"] + "[/b]\n" if is_creature_face(card["card_faces"][1]) else "")


class Save:
    """Represents a TTS save file."""

    def __init__(self, name: str = "Bag of Stuff"):
        self.ContainedObjects = []
        self.Nickname = name
        pass

    def addObject(self, obj):
        self.ContainedObjects.append(obj)
        return

    def getOut(self):
        return {
            "ObjectStates": [
                {
                    "Name": "Bag",
                    "Transform": transformAttrs,
                    "Nickname": self.Nickname,
                    "ColorDiffuse": colorAttrs,
                    "Bag": {"Order": 0},
                    "ContainedObjects": [f.toDict() for f in self.ContainedObjects],
                }
            ]
        }


class Deck:
    """Represents one stack of cards output to the bag."""

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

    def __init__(self, nick=""):
        """Create a pack."""
        self.DeckIDs = []
        self.CustomDeck = {}
        self.ContainedObjects = []
        self.Nickname = nick
        self.deckObject = {
            "Name": "Deck",
            "Nickname": nick,
            "Transform": transformAttrs,
            "ColorDiffuse": colorAttrs,
            "DeckIDs": [],
            "CustomDeck": {},
            "ContainedObjects": [],
        }
        self.Decals = [random.choice([Deck.StarFoil, Deck.SetSpiralFoil, Deck.VoronoiFoil])]
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
            self.Transform = transformAttrs
            self.ColorDiffuse = colorAttrs
            self.CardID = counter * 100
            self.frontImage = {
                "FaceURL": re.sub(
                    "\?\d+$",
                    "",
                    cardData["card_faces"][0]["image_uris"]["normal"] if "card_faces" in cardData and "adventure" != cardData["layout"] and "split" != cardData["layout"] else cardData["image_uris"]["normal"],
                ),
                "BackURL": "https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/f/f8/Magic_card_back.jpg",
                "NumWidth": (2 if cardData["stitched"] else 1) if "stitched" in cardData else 1,
                "NumHeight": 1,
                "BackIsHidden": True,
                "UniqueBack": False,
            }
            self.isPlanar = (cardData["planar"] if "planar" in cardData else False) or cardData["layout"] == "split"
            self.CustomDeck = self.frontImage
            self.AttachedDecals = decals if isFoil else []
            self.States = None
            self.Script = None
            self.XML = None
            if "card_faces" in cardData and "adventure" != cardData["layout"] and "split" != cardData["layout"]:
                backImage = {
                    "FaceURL": re.sub("\?\d+$", "", cardData["card_faces"][1]["image_uris"]["normal"]),
                    "BackURL": "https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/f/f8/Magic_card_back.jpg",
                    "NumWidth": (2 if cardData["stitched"] else 1) if "stitched" in cardData else 1,
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
                        "Transform": transformAttrs,
                        "AltLookAngle": ({"x": 180.0, "y": 0.0, "z": 90.0} if cardData["card_faces"][1]["planar"] else {"x": 0.0, "y": 0.0, "z": 0.0}) if "planar" in cardData["card_faces"][1] else ({"x": 180.0, "y": 0.0, "z": 180.0} if cardData["layout"] == "flip" else {"x": 0.0, "y": 0.0, "z": 0.0}),
                        "ColorDiffuse": colorAttrs,
                        "CardID": int((counter * 1000) - 100) * 100 + ((1 if cardData["stitched"] else 0) if "stitched" in cardData else 0),
                        "CustomDeck": {str((counter * 1000) - 100): backImage},
                        "AttachedDecals": (decals if isFoil else []),
                        # "SidewaysCard": "Battle" in cardData["card_faces"][1]["type_line"] or "Plane" in cardData["card_faces"][1]["type_line"]
                    }
                }
            if "all_parts" in cardData:
                tokens = [part for part in cardData["all_parts"] if part["component"] in ["meld_result", "token"]]
                if len(tokens) > 0:
                    self.Script = 'function onLoad() tbl=Global.getVar("Table") if tbl ~= nil then tbl.call("addToTable", {"' + cardData["name"] + '", {' + ','.join(['{"' + part["name"] + '","' + part["id"] + '",' + ("true" if "//" in part["name"] else "false") + "}" for part in tokens]) + '}}) end self.setLuaScript("") end'

        def toDict(self):
            """Returns a dictionary for the final JSON."""
            return {
                "Nickname": self.Nickname,
                "Name": self.Name,
                "Memo": self.Memo,
                "Description": self.Description,
                "ColorDiffuse": self.ColorDiffuse,
                "Transform": self.Transform,
                "AltLookAngle": {"x": 180.0 if self.isPlanar else 0.0, "y": 0.0, "z": 90.0 if self.isPlanar else 0.0},
                "CardID": int(self.CardID),
                "CustomDeck": {str(self.CardID // 100): self.CustomDeck},
                "States": self.States,
                "AttachedDecals": self.AttachedDecals,
                "XmlUI": self.XML,
                "LuaScript": self.Script,
                # "SidewaysCard": self.SidewaysCard,
            }

    class CardBlobBlankImage:
        def __init__(self, cardData, counter, isFoil=False, decals=[]):
            """Represents one card."""
            self.Nickname = f'{cardData["name"]}\n{cardData["type_line"]} {round(cardData["cmc"])}MV'
            """Shows up in TTS as the name of the object.
            
            Contains the name, mana value, and type line for easy searching."""
            self.Memo = cardData["oracle_id"]
            """Contains oracle id for tracking using the importer."""
            self.Description = write_description_dfc(cardData, False) if is_dfc(cardData) else write_description_split(cardData) if is_split_card(cardData) else write_description_normal(cardData, cardData)
            """Contains oracle text, power/toughness, and loyalty if any."""
            self.CardID = counter * 100

            self.XML = write_xmlui(cardData["card_faces"][0] if is_dfc(cardData) or is_split_card(cardData) else cardData, cardData)
            self.isPlanar = (cardData["planar"] if "planar" in cardData else False) or cardData["layout"] == "split"
            self.CustomDeck = {
                "FaceURL": blank_image(cardData["card_faces"][0] if is_dfc(cardData) else cardData, cardData),
                "BackURL": "https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/f/f8/Magic_card_back.jpg",
                "NumWidth": (2 if cardData["stitched"] else 1) if "stitched" in cardData else 1,
                "NumHeight": 1,
                "BackIsHidden": True,
                "UniqueBack": False,
            }
            self.AttachedDecals = decals if isFoil else []
            self.States = None
            if "card_faces" in cardData.keys() and "adventure" != cardData["layout"] and "split" != cardData["layout"]:
                backImage = {
                    "FaceURL": blank_image(cardData["card_faces"][1], cardData),
                    "BackURL": "https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/f/f8/Magic_card_back.jpg",
                    "NumWidth": (2 if cardData["stitched"] else 1) if "stitched" in cardData else 1,
                    "NumHeight": 1,
                    "BackIsHidden": True,
                    "UniqueBack": False,
                }
                backName = f'{cardData["name"]}\n{cardData["type_line"]} {round(cardData["cmc"])}MV'
                backDescription = write_description_dfc(cardData, True)
                self.States = {
                    "2": {
                        "Name": "Card",
                        "Nickname": backName,
                        "Description": backDescription,
                        "Transform": transformAttrs,
                        "AltLookAngle": ({"x": 180.0, "y": 0.0, "z": 90.0} if cardData["card_faces"][1]["planar"] else {"x": 0.0, "y": 0.0, "z": 0.0}) if "planar" in cardData["card_faces"][1] else ({"x": 180.0, "y": 0.0, "z": 180.0} if cardData["layout"] == "flip" else {"x": 0.0, "y": 0.0, "z": 0.0}),
                        "ColorDiffuse": colorAttrs,
                        "CardID": int((counter * 1000) - 100) * 100 + ((1 if cardData["stitched"] else 0) if "stitched" in cardData else 0),
                        "CustomDeck": {str((counter * 1000) - 100): backImage},
                        "AttachedDecals": (decals if isFoil else []),
                        "XmlUI": write_xmlui(cardData["card_faces"][1], cardData, True),
                        # "SidewaysCard": "Battle" in cardData["card_faces"][1]["type_line"] or "Plane" in cardData["card_faces"][1]["type_line"]
                    }
                }

        def toDict(self):
            """Returns a dictionary for the final JSON."""
            return {
                "Nickname": self.Nickname,
                "Name": "Card",
                "Memo": self.Memo,
                "Description": self.Description,
                "ColorDiffuse": colorAttrs,
                "Transform": transformAttrs,
                "AltLookAngle": {"x": 180.0 if self.isPlanar else 0.0, "y": 0.0, "z": 90.0 if self.isPlanar else 0.0},
                "CardID": int(self.CardID),
                "CustomDeck": {str(self.CardID // 100): self.CustomDeck},
                "States": self.States,
                "AttachedDecals": self.AttachedDecals,
                "XmlUI": self.XML,
                # "SidewaysCard": self.SidewaysCard,
            }

    def import_cards(self, cardDataList, foilIndexes=[]):
        """Takes a list of card objects from a Scryfall search."""
        for index, item in enumerate(cardDataList):
            self.ContainedObjects.append(tempCard := self.CardBlob(item, self.Counter + 1, index in foilIndexes, self.Decals).toDict())
            self.DeckIDs.append(int((self.Counter + 1) * 100))
            self.CustomDeck[str((self.Counter + 1) * 100)] = tempCard["CustomDeck"]
            self.Counter += 1
        return

    def toDict(self):
        """Returns a dictionary for the final JSON."""
        if len(self.ContainedObjects) == 1:
            return self.ContainedObjects[0]
        else:
            return {
                "Name": "Deck",
                "Transform": transformAttrs,
                "ColorDiffuse": colorAttrs,
                "Nickname": self.Nickname,
                "DeckIDs": [int(card["CardID"]) for card in self.ContainedObjects],
                "CustomDeck": {str(card["CardID"] // 100): card["CustomDeck"][str(card["CardID"] // 100)] for card in self.ContainedObjects},
                "ContainedObjects": self.ContainedObjects,
            }
