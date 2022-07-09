import random
import re

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


class Pack:
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
            self.Transform = transformAttrs
            self.ColorDiffuse = colorAttrs
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
                        "Transform": transformAttrs,
                        "ColorDiffuse": colorAttrs,
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
            "Transform": transformAttrs,
            "ColorDiffuse": colorAttrs,
            "Nickname": self.Nickname,
            "DeckIDs": [int(card["CardID"]) for card in self.ContainedObjects],
            "CustomDeck": {
                str(card["CardID"] // 100): card["CustomDeck"][str(card["CardID"] // 100)]
                for card in self.ContainedObjects
            },
            "ContainedObjects": self.ContainedObjects,
        }
