import mmap
import ijson
import orjson
import flamewave
import requests
import time


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
        c_obj = flamewave.tts_parse(item)
        out.append(c_obj)
        out_2[c_obj["name"] + c_obj["set"]] = c_obj
    if out_dict:
        return out_2
    return out


def scryfall_set(setcode):
    """Returns list of JSON data containing all cards from the set. Deprecated."""
    full_set_json = []
    time.sleep(0.25)
    response = requests.get(f"https://api.scryfall.com/cards/search?q=set%3A{setcode}&unique=prints", headers={"User-Agent": "Python 3.9.13 CERA"})
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
    str_l = {f"{a[0]}{a[1]}": True for a in cardlist}
    out = {}
    f = open("default-cards.json", "rb")
    objects = ijson.items(f, "item")
    for o in objects:
        if f'{o["collector_number"]}{o["set"]}' in str_l:
            card_obj = flamewave.tts_parse(o)
            blob_json.append(card_obj)
            out[f'{o["collector_number"]}{o["set"]}'] = card_obj
        if o['set'] == 'plst' and f'{o["collector_number"]}mb1' in str_l:
            card_obj = flamewave.tts_parse(o)
            blob_json.append(card_obj)
            out[f'{o["collector_number"]}mb1'] = card_obj
        if len(blob_json) == len(cardlist):
            break
    f.close()
    if out_dict:
        return out
    return blob_json


def mm_collection(cardlist, out_dict=False):
    def file_parse_generator():
        with open("default-cards.json", mode="r") as f:
            with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as m:
                for line in iter(m.readline, b""):
                    L = line.strip()
                    if len(L) > 5:  # We assume that the lines are nicely formed.
                        if L.endswith(b","):
                            yield orjson.loads(L[:-1])
                        else:
                            yield orjson.loads(L)
                    else:
                        continue

    generator = file_parse_generator()
    string_list = {f"{a[0]}{a[1]}": True for a in cardlist}
    blob_json = []
    out = {}
    while True:
        try:
            card = next(generator)
        except:
            break
        if f'{card["collector_number"]}{card["set"]}' in string_list:
            card_obj = flamewave.tts_parse(card)
            blob_json.append(card_obj)
            out[f'{card["collector_number"]}{card["set"]}'] = card_obj
        if card['set'] == 'plst' and f'{card["collector_number"]}mb1' in string_list:
            card_obj = flamewave.tts_parse(card)
            blob_json.append(card_obj)
            out[f'{card["collector_number"]}{card["set"]}'] = card_obj
    if out_dict:
        return out
    return blob_json
