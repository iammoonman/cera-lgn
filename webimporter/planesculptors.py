import requests
import re

legal_sets = {"dms": "dreamscape", "ldo": "lorado", "ank": "ankheret"}


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
    shapeconvert = {"normal": "normal", "double": "transform"}
    out = []
    for k, v in cards.items():
        face_1 = {
            "name": v["name"],
            "cmc": v["cmc"],
            "type_line": v["types"],
            "power": v["power"] if v["power"] is not None else 0,
            "toughness": v["toughness"] if v["toughness"] is not None else 0,
            "oracle_text": decode_rtext(v["rulesText"])
            if v["rulesText"] is not None
            else "",
            "mana_cost": v["manaCost"].replace("[", "{").replace("]", "}") if v["manaCost"] is not None else "",
        }
        face_2 = {
            "name": v["name2"],
            "cmc": v["cmc"],
            "type_line": v["types2"],
            "power": v["power2"] if v["power2"] is not None else 0,
            "toughness": v["toughness2"] if v["toughness2"] is not None else 0,
            "oracle_text": decode_rtext(v["rulesText2"])
            if v["rulesText2"] is not None
            else "",
            "mana_cost": v["manaCost2"].replace("[", "{").replace("]", "}") if v["manaCost2"] is not None else "",
        }
        sc_obj = {
            "oracle_id": "",
            "layout": shapeconvert[v["shape"]],
            "set": setcode,
            "collector_number": v["cardNumber"],
            "card_faces": [face_1, face_2] if v["shape"] == "double" else [],
            "rarity": v["rarity"].lower(),
            "image_uris": {"png": f"https://www.planesculptors.net{v['artUrl']}", "small": ""},
        }
        if v["shape"] == "normal":
            sc_obj = {**sc_obj, **face_1}
        out.append(sc_obj)
    return out


print(get_ps_set("ldo")[0:5])


def decode_rtext(text: str):
    newtext = re.sub('\[(?=.\])', '{', text)
    newtext = re.sub('(?<=\[.)\]', '}', newtext)
    return (
        newtext.replace("&#8217;", "'")
        .replace("<br>", "")
        .replace("<i>", "")
        .replace("</i>", "")
        .replace("&#8212;", "—")
        .replace('&#8226;', '•')
    )
