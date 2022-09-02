from exporttemplates import tts_output
import requests
import random
import csv
import copy


def get_cube(cc_id, p_len):
    """Returns a JSON save file for Tabletop Simulator."""

    save = tts_output.Save(name=f"packs of of the cube with id {cc_id}")
    response = requests.get(
        f"https://cubecobra.com/cube/download/csv/{cc_id}?primary=Color%20Category&secondary=Types-Multicolor&tertiary=Mana%20Value&quaternary=Alphabetical&showother=false",
        headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"},
    )
    reader = csv.DictReader(response.content.decode("utf-8").splitlines())
    if "Name" not in reader.fieldnames:  # Catching 404 errors in CubeCobra is much harder than it should be.
        return None
    templist = []
    # foil_indexes = []
    for row in reader:
        templist.append([row["Collector Number"], row["Set"]])
        # if row["Finish"] == "Foil":
        #     foil_indexes += [len(templist)]
    cardinfo = tts_output.ijson_collection(templist)
    cubelist = []
    reader = csv.DictReader(response.content.decode("utf-8").splitlines())
    for row in reader:
        for c in cardinfo:
            if row["Collector Number"] == c["collector_number"] and row["Set"] == c["set"]:
                x = {}
                if "card_faces" in c.keys():
                    x = {
                        "card_faces": [
                            {
                                **c["card_faces"][0],
                                "image_uris": {
                                    "png": row["Image URL"]
                                    if row["Image URL"] != ""
                                    else c["card_faces"][0]["image_uris"]["png"]
                                },
                            },
                            {
                                **c["card_faces"][1],
                                "image_uris": {
                                    "png": row["Image Back URL"]
                                    if row["Image Back URL"] != ""
                                    else c["card_faces"][1]["image_uris"]["png"]
                                },
                            },
                        ],
                        "finish": row["Finish"] == "Foil",
                    }
                else:
                    x = {
                        "image_uris": {"png": row["Image URL"] if row["Image URL"] != "" else c["image_uris"]["png"]},
                        "finish": row["Finish"] == "Foil",
                    }
                cubelist.append({**c, **x})
                break
    random.shuffle(cubelist)
    for i in [cubelist[u : u + p_len] for u in range(0, len(cubelist), p_len)]:
        the_cube = tts_output.Pack()
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
