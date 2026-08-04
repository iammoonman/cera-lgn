import flamewave
import requests
import random
import csv
import copy
import json

def cera_cache(scryfall_id: str, front_or_back: str) -> str:
    return f"https://cera-lgn.stream/{front_or_back}/{scryfall_id[0]}/{scryfall_id[1]}/{scryfall_id}.webp"

def get_cube(cc_id, p_len):
    """Returns a JSON save file for Tabletop Simulator."""

    save = flamewave.tts_classes.Save(name=f"packs of the cube with id {cc_id}")
    response = requests.get(
        f"https://cubecobra.com/cube/api/cubeJSON/{cc_id}",
        headers={"User-Agent": "CERA-LGN/0.0"},
    )
    js = response.json()
    cube_cards = js["cards"]["mainboard"]
    cardinfo = flamewave.collection_import.jsonl_collection(
        [[n["details"]["collector_number"], n["details"]["set"]] for n in cube_cards],
        out_dict=True,
    )
    cubelist = []
    for row in cube_cards:
        card = cardinfo[f'{row["details"]["collector_number"]}{row["details"]["set"]}']
        x = {}
        if "card_faces" in card.keys():
            x = {
                "card_faces": [
                    {
                        **card["card_faces"][0],
                        "image_uris": {"normal": row["imgUrl"] if "imgUrl" in row else cera_cache(card["card_faces"][0]["image_uris"]["normal"], 'front')},
                    },
                    {
                        **card["card_faces"][1],
                        "image_uris": {"normal": row["imgBackUrl"] if "imgBackUrl" in row else cera_cache(card["card_faces"][1]["image_uris"]["normal"], 'back')},
                    },
                ],
                "finish": row["finish"] == "Foil" if "finish" in row else False,
            }
        else:
            x = {
                "image_uris": {"normal": row["imgUrl"] if "imgUrl" in row else cera_cache(card["image_uris"]["normal"], 'front')},
                "finish": row["finish"] == "Foil" if "finish" in row else False,
            }
        cubelist.append({**card, **x})
    random.shuffle(cubelist)
    for i in [cubelist[u : u + p_len] for u in range(0, len(cubelist), p_len)]:
        the_cube = flamewave.tts_classes.Deck()
        the_cube.import_cards(i, [i.index(q) for q in [r for r in i if r["finish"]]])
        save.addObject(the_cube)
    return save.getOut()


def get_cube_p1p1(cc_id, seed="0"):
    # Generate a random string of numbers
    if seed == "0":
        seed = "".join([f"{random.randint(0,9)}" for _ in range(6)])
    return f"https://cubecobra.com/cube/samplepackimage/{cc_id}/{seed}", seed


def get_cube_deck():
    # The full export template isn't ready yet.
    return
