import flamewave
import requests
import random


def get_cube(cc_id, p_len):
    """Returns a JSON save file for Tabletop Simulator."""

    save = flamewave.tts_classes.Save(name=f"packs of the cube with id {cc_id}")
    response = requests.get(
        f"https://cubecobra.com/cube/api/cubeJSON/{cc_id}",
        headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"},
    )
    js = response.json()
    cube_cards = js["cards"]["mainboard"]
    cardinfo = flamewave.collection_import.mm_collection(
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
                        "image_uris": {"normal": row["imgUrl"] if "imgUrl" in row else card["card_faces"][0]["image_uris"]["normal"]},
                    },
                    {
                        **card["card_faces"][1],
                        "image_uris": {"normal": row["imgBackUrl"] if "imgBackUrl" in row else card["card_faces"][1]["image_uris"]["normal"]},
                    },
                ],
                "finish": row["finish"] == "Foil" if "finish" in row else False,
            }
        else:
            x = {
                "image_uris": {"normal": row["imgUrl"] if "imgUrl" in row else card["image_uris"]["normal"]},
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
