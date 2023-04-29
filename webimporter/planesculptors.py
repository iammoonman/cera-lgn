import requests
import re
import html

from exporttemplates.tts_import import tts_parse

legal_sets = {
    "c_dms": "dreamscape",
    "c_ldo": "lorado",
    "c_ank": "ankheret",
    "c_gsc": "ghariv-the-sacred-city",
    "c_blr": "blood-like-rivers",
    "c_vtm": "villains-the-musical",
    "c_fmq": "the-fabled-masquerade",
    "c_son": "splinters-of-novanda",
    "c_ksv": "karslav",
    "c_alr": "alara",
    "c_hnn": "high-noon1",
    "c_rzp": "rat-zone-promos",
}


def decode_rtext(text: str):
    newtext = re.sub("\[(?=.\])", "{", text)
    newtext = re.sub("(?<=\{.)\]", "}", newtext)
    return html.unescape(newtext.replace("<br>", "").replace("<i>", "").replace("</i>", ""))


def get_ps_set(setcode):
    if setcode not in legal_sets:
        return False
    code = legal_sets[setcode]
    response = requests.get(
        f"https://www.planesculptors.net/set/{code}?json",
        headers={
            "User-Agent": "Python 3.9.13 CERA",
        },
    )
    data: dict = response.json()
    cards: dict[str, dict] = data["cards"]
    # shapes = ["normal", "split", "flip", "double", "plane", "vsplit"]
    shapeconvert = {"normal": "normal", "double": "transform", "split": "split"}
    out = []
    for k, v in cards.items():
        if v["rarity"] == "T":
            continue
        face_1 = {
            "name": v["name"],
            "cmc": int(v["cmc"]),
            "type_line": v["types"],
            "power": v["power"] if v["power"] is not None else "0",
            "toughness": v["toughness"] if v["toughness"] is not None else "0",
            "oracle_text": decode_rtext(v["rulesText"]) if v["rulesText"] is not None else "",
            "mana_cost": v["manaCost"].replace("[", "{").replace("]", "}") if v["manaCost"] is not None else "",
            "loyalty": "",
            "image_uris": {"normal": f"https://www.planesculptors.net{v['artUrl']}", "small": ""},
        }
        face_2 = {
            "name": v["name2"],
            "cmc": int(v["cmc"]),
            "type_line": v["types2"],
            "power": v["power2"] if v["power2"] is not None else "0",
            "toughness": v["toughness2"] if v["toughness2"] is not None else "0",
            "oracle_text": decode_rtext(v["rulesText2"]) if v["rulesText2"] is not None else "",
            "mana_cost": v["manaCost2"].replace("[", "{").replace("]", "}") if v["manaCost2"] is not None else "",
            "loyalty": "",
            "image_uris": {"normal": f"https://www.planesculptors.net{v['artUrl']}", "small": ""},
        }
        sc_obj = {
            "oracle_id": "",
            "layout": shapeconvert[v["shape"]],
            "set": setcode,
            "collector_number": v["cardNumber"],
            "rarity": v["rarity"].lower(),
            "image_uris": {"normal": f"https://www.planesculptors.net{v['artUrl']}", "small": ""},
        }
        if v["shape"] == "normal":
            sc_obj = {**sc_obj, **face_1}
        if v["shape"] == "split":
            sc_obj["name"] = face_1["name"] + "//" + face_2["name"]
            sc_obj["type_line"] = face_1["type_line"] + "//" + face_2["type_line"]
            sc_obj["mana_cost"] = face_1["mana_cost"] + "//" + face_2["mana_cost"]
            sc_obj["card_faces"] = [face_1, face_2]
        if v["shape"] == "double":
            sc_obj["name"] = face_1["name"] + "//" + face_2["name"]
            sc_obj["cmc"] = int(v["cmc"])
            sc_obj["type_line"] = face_1["type_line"] + "//" + face_2["type_line"]
            sc_obj["mana_cost"] = face_1["mana_cost"] + "//" + face_2["mana_cost"]
            sc_obj["card_faces"] = [face_1, face_2]
            sc_obj["stitched"] = True
        out.append(tts_parse(sc_obj))
    return out


def ps_collection(cardlist, out_dict=False):
    """Returns list of JSON data containing all cards from the list by collector_number and set."""
    blob_json = []
    out = {}
    for cd in legal_sets:
        if cd in [x[1] for x in cardlist]:
            s = get_ps_set(cd)
            if s:
                blob_json += [x for x in s if [x["collector_number"], x["set"]] in cardlist]
                n = {
                    f"{x['collector_number']}{x['set']}": x for x in s if [x["collector_number"], x["set"]] in cardlist
                }
                out = {**out, **n}
    if out_dict:
        return out
    return blob_json
