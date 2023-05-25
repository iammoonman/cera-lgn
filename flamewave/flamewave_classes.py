from typing import List, Literal, Union

LayoutType = Union[
    Literal["creature"],
    Literal["sorcery"],
    Literal["planeswalker"],
    Literal["vanguard"],
    Literal["plane"],
    Literal["battle"],
    Literal["permanent"],
    Literal["attraction"],
    Literal["token"],
    Literal["scheme"],
]
RarityType = Union[Literal["common"], Literal["uncommon"], Literal["rare"], Literal["mythic"], Literal["bonus"], Literal["special"]]
ColorType = Union[Literal["W"], Literal["U"], Literal["B"], Literal["R"], Literal["G"]]
RelationType = Union[
    Literal["token"],
    Literal["variation"],
    Literal["base_variant"],
    Literal["meld_part"],
    Literal["meld_result"],
    Literal["combo_piece"],
]


class FWCard:
    def __init__(self):
        self.object: str
        self.id: str
        self.multiverse_ids: List[str]
        self.tcgplayer_id: str
        self.cardmarket_id: str
        self.lang: str
        self.released_at: str
        self.uri: str
        self.scryfall_uri: str
        self.name: str
        self.card_faces: List[FWCardFace]
        self.relations: List[FWRelated]
        self.digital: bool
        self.booster: bool
        self.content_warning: bool
        self.reprint: bool
        self.reserved: bool
        self.border
        self.frame
        self.set: str
        self.collector_number: str
        return self

    def create_from_scryfall(self, sc_data):
        self.name = sc_data["name"]
        self.set = sc_data["set"]
        self.collector_number = sc_data["collector_number"]
        self.oracle_id = sc_data["oracle_id"] if "oracle_id" in sc_data else ""
        self.card_faces = []
        if sc_data["layout"] in ["transform", "modal_dfc", "double_faced_token", "reversible_card"]:
            for face in sc_data["card_faces"]:
                if "Battle" in face["type_line"]:
                    self.card_faces.append(FWBattleFace().from_scryfall(sc_data, face))
                elif "Planeswalker" in face["type_line"]:
                    self.card_faces.append(FWPlaneswalkerFace().from_scryfall(sc_data, face))
                elif "Creature" in face["type_line"]:
                    self.card_faces.append(FWCreatureFace().from_scryfall(sc_data, face))
                elif "Sorcery" in face["type_line"] or "Instant" in face["type_line"]:
                    self.card_faces.append(FWSorceryFace().from_scryfall(sc_data, face))
                elif "Artifact" in face["type_line"] or "Enchantment" in face["type_line"] or "Land" in face["type_line"] or "Card" in face["type_line"]:
                    self.card_faces.append(FWPermanentFace().from_scryfall(sc_data, face))
        elif sc_data["layout"] == "split":
            for face in sc_data["card_faces"]:
                if "Sorcery" in face["type_line"] or "Instant" in face["type_line"]:
                    self.card_faces.append(FWSorceryFace().from_scryfall(sc_data, face))
        elif sc_data["layout"] == "flip":
            for face in sc_data["card_faces"]:
                if "Creature" in face["type_line"]:
                    self.card_faces.append(FWCreatureFace().from_scryfall(sc_data, face))
                elif "Artifact" in face["type_line"] or "Enchantment" in face["type_line"] or "Land" in face["type_line"]:
                    self.card_faces.append(FWPermanentFace().from_scryfall(sc_data, face))
        elif sc_data["layout"] == "adventure":
            for face in sc_data["card_faces"]:
                if "Creature" in face["type_line"]:
                    self.card_faces.append(FWCreatureFace().from_scryfall(sc_data, face))
                elif "Sorcery" in face["type_line"] or "Instant" in face["type_line"]:
                    self.card_faces.append(FWSorceryFace().from_scryfall(sc_data, face))
                elif "Artifact" in face["type_line"] or "Enchantment" in face["type_line"] or "Land" in face["type_line"]:
                    self.card_faces.append(FWPermanentFace().from_scryfall(sc_data, face))
        elif sc_data["layout"] in ["vanguard", "Vanguard"]:
            self.card_faces.append(FWVanguardFace().from_scryfall(sc_data, face))
        elif sc_data["layout"] == "planar":
            self.card_faces.append(FWPlaneFace().from_scryfall(sc_data, face))
        elif sc_data["layout"] in ["normal", "token", "leveler", "meld", "saga", "class"]:
            if "Battle" in sc_data["type_line"]:
                self.card_faces.append(FWBattleFace().from_scryfall(sc_data))
            elif "Planeswalker" in sc_data["type_line"]:
                self.card_faces.append(FWPlaneswalkerFace().from_scryfall(sc_data))
            elif "Creature" in sc_data["type_line"]:
                self.card_faces.append(FWCreatureFace().from_scryfall(sc_data))
            elif "Sorcery" in sc_data["type_line"] or "Instant" in sc_data["type_line"]:
                self.card_faces.append(FWSorceryFace().from_scryfall(sc_data))
            elif "Artifact" in sc_data["type_line"] or "Enchantment" in sc_data["type_line"] or "Land" in sc_data["type_line"] or "Card" in sc_data["type_line"]:
                self.card_faces.append(FWPermanentFace().from_scryfall(sc_data))
        elif sc_data["layout"] == "scheme":
            self.card_faces.append(FWSchemeFace().from_scryfall(sc_data))
        elif sc_data["layout"] == "emblem":
            self.card_faces.append(FWPermanentFace().from_scryfall(sc_data))
        elif sc_data["layout"] == "augment":
            self.card_faces.append(FWCreatureFace().from_scryfall(sc_data))
        elif sc_data["layout"] == "host":
            self.card_faces.append(FWCreatureFace().from_scryfall(sc_data))
        elif sc_data["layout"] == "art_series":
            for face in sc_data["card_faces"]:
                self.card_faces.append(FWPermanentFace().from_scryfall(sc_data, face))
        else:
            pass
        return self


class FWCardFace:
    def __init__(self, layout: LayoutType):
        self.layout: LayoutType = layout
        self.id: str
        self.name: str
        self.rarity: RarityType
        self.flavor_name: str
        self.type_line: str
        self.keywords: List[str]
        self.watermark: str
        self.oracle_text: str
        self.colors: List[ColorType]
        self.mv: str
        self.oracle_id: str
        self.image_uris
        self.artist: str
        self.finishes
        self.frame_effects
        return self

    def from_scryfall(self, sc_data):
        self.id: str = sc_data["id"]
        self.name: str = sc_data["name"]
        self.rarity: RarityType = sc_data["rarity"]
        self.flavor_name: str = sc_data["flavor_name"] if "flavor_name" in sc_data else sc_data["name"]
        self.type_line: str = sc_data["type_line"]
        self.keywords: List[str] = []
        self.watermark: str = sc_data["watermark"] if "watermark" in sc_data else ""
        self.oracle_text: str = sc_data["oracle_text"] if "oracle_text" in sc_data else ""
        self.colors: List[ColorType] = sc_data["colors"] if "colors" in sc_data else []
        self.mv: str = f'{sc_data["cmc"]}'
        self.oracle_id: str = sc_data["oracle_id"] if "oracle_id" in sc_data else ""
        self.image_uris
        self.artist: str = sc_data["artist"] if "artist" in sc_data else ""
        self.finishes = sc_data["finishes"]
        self.frame_effects = sc_data["frame_effects"] if "frame_effects" in sc_data else []
        return self


class FWCreatureFace(FWCardFace):
    def __init__(self):
        super().__init__("creature")
        self.power: str
        self.tougness: str
        self.mana_cost: str
        self.flavor_text: str
        return self

    def from_scryfall(self, sc_data, face=None):
        super().from_scryfall(sc_data)
        if face is not None:
            self.name = face["name"]
            self.oracle_text = face["oracle_text"] if "oracle_text" in face else ""
            self.type_line = face["type_line"]
            self.power = face["power"]
            self.tougness = face["toughness"]
            self.mana_cost = face["mana_cost"] if "mana_cost" in sc_data else ""
            self.flavor_text = face["flavor_text"] if "flavor_text" in face else ""
        else:
            self.power = sc_data['power']
            self.tougness = sc_data['toughness']
            self.mana_cost = sc_data['mana_cost'] if "mana_cost" in sc_data else ""
            self.flavor_text = sc_data["flavor_text"] if "flavor_text" in sc_data else ""
        return self


class FWSorceryFace(FWCardFace):
    def __init__(self):
        super().__init__("sorcery")
        self.mana_cost: str
        self.flavor_text: str
        return self
    def from_scryfall(self, sc_data, face=None):
        super().from_scryfall(sc_data)
        if face is not None:
            self.name = face["name"]
            self.oracle_text = face["oracle_text"]
            self.type_line = face["type_line"]
            self.mana_cost = face["mana_cost"] if "mana_cost" in face else ""
            self.flavor_text = face["flavor_text"] if "flavor_text" in face else ""
        else:
            self.mana_cost = sc_data['mana_cost'] if "mana_cost" in sc_data else ""
            self.flavor_text = sc_data["flavor_text"] if "flavor_text" in sc_data else ""
        return self


class FWPlaneswalkerFace(FWCardFace):
    def __init__(self):
        super().__init__("planeswalker")
        self.mana_cost: str
        self.loyalty: str
        return self
    def from_scryfall(self, sc_data, face=None):
        super().from_scryfall(sc_data)
        if face is not None:
            self.name = face["name"]
            self.oracle_text = face["oracle_text"]
            self.type_line = face["type_line"]
            self.mana_cost = face["mana_cost"] if "mana_cost" in face else ""
            self.loyalty = face['loyalty']
        else:
            self.mana_cost = sc_data['mana_cost'] if "mana_cost" in sc_data else ""
            self.loyalty = sc_data['loyalty']
        return self


class FWVanguardFace(FWCardFace):
    def __init__(self):
        super().__init__("vanguard")
        self.hand_mod: str
        self.life_mod: str
        self.restriction: str
        return self
    def from_scryfall(self, sc_data, face=None):
        super().from_scryfall(sc_data)
        self.hand_mod = sc_data['hand_mod']
        self.life_mod = sc_data["life_mod"]
        self.restriction = sc_data['restriction'] if 'restriction' in sc_data else ''
        return self


class FWPlaneFace(FWCardFace):
    def __init__(self):
        super().__init__("plane")
        return self
    def from_scryfall(self, sc_data, face=None):
        super().from_scryfall(sc_data)
        return self


class FWSchemeFace(FWCardFace):
    def __init__(self):
        super().__init__("scheme")
        return self
    def from_scryfall(self, sc_data, face=None):
        super().from_scryfall(sc_data)
        return self


class FWBattleFace(FWCardFace):
    def __init__(self):
        super().__init__("battle")
        self.defense: str
        self.mana_cost: str
        self.flavor_text: str
        return self
    def from_scryfall(self, sc_data, face=None):
        super().from_scryfall(sc_data)
        if face is not None:
            self.name = face["name"]
            self.oracle_text = face["oracle_text"]
            self.type_line = face["type_line"]
            self.mana_cost = face["mana_cost"] if "mana_cost" in face else ""
            self.flavor_text = face["flavor_text"] if "flavor_text" in face else ""
            self.defense = face['defense']
        else:
            self.mana_cost = sc_data['mana_cost'] if "mana_cost" in sc_data else ""
            self.flavor_text = sc_data["flavor_text"] if "flavor_text" in sc_data else ""
            self.defense = sc_data['defense']
        return self


class FWPermanentFace(FWCardFace):
    def __init__(self):
        super().__init__("permanent")
        self.mana_cost: str
        self.flavor_text: str
        return self
    def from_scryfall(self, sc_data, face=None):
        super().from_scryfall(sc_data)
        if face is not None:
            self.name = face["name"]
            self.oracle_text = face["oracle_text"]
            self.type_line = face["type_line"]
            self.mana_cost = face["mana_cost"] if "mana_cost" in face else ""
            self.flavor_text = face["flavor_text"] if "flavor_text" in face else ""
        else:
            self.mana_cost = sc_data['mana_cost'] if "mana_cost" in sc_data else ""
            self.flavor_text = sc_data["flavor_text"] if "flavor_text" in sc_data else ""
        return self


class FWAttractionFace(FWCardFace):
    def __init__(self):
        super().__init__("attraction")
        self.lights: List[int]
        return self
    def from_scryfall(self, sc_data, face=None):
        super().from_scryfall(sc_data)
        self.mana_cost = sc_data['mana_cost'] if "mana_cost" in sc_data else ""
        self.flavor_text = sc_data["flavor_text"] if "flavor_text" in sc_data else ""
        self.lights = sc_data['lights']
        return self


class FWRelated:
    def __init__(self):
        self.id: str
        self.object: RelationType
        self.name: str
        self.type_line: str
        self.uri: str
        return self
