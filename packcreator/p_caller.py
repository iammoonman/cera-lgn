import json
import time
import requests
from . import tts_output, p_creator, point_slicer


def get_packs(setcode, num_packs, land_pack=False):
    """Returns a JSON save file for Tabletop Simulator."""
    with open(
        f"setjson/{setcode}.json" if __name__ == "__main__" else f"packcreator/setjson/{setcode}.json", "rb"
    ) as f:
        setJSON = json.load(f)
    save = {
        "ObjectStates": [
            {
                "Name": "Bag",
                "Transform": tts_output.Pack.transformAttrs,
                "Nickname": f"{num_packs} Packs of {setcode}",
                "ColorDiffuse": tts_output.Pack.colorAttrs,
                "Bag": {"Order": 0},
                "ContainedObjects": [],
            }
        ]
    }
    all_packs = []
    for _ in range(num_packs):
        (raw_cn_cards, foil_indexes,) = p_creator.generatepack_c1c2_special(
            sheet_index_func=lambda a: point_slicer.get_number(a),
            setJSON=setJSON,
        )
        all_packs.append([raw_cn_cards, foil_indexes])
    all_cn_sets = []
    for p in all_packs:
        all_cn_sets += p[0]
    set_info = tts_output.ijson_collection(all_cn_sets)
    for p in all_packs:
        new_colle = []
        for crd in p[0]:
            new_colle += [x for x in set_info if x["collector_number"] == crd[0] and x["set"] == crd[1]]
        # print([a['name'] for a in new_colle])
        pack_to_add = tts_output.Pack()
        pack_to_add.import_cards(
            new_colle,
            p[1],
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
            pack_to_add = tts_output.Pack()
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
                "Transform": tts_output.Pack.transformAttrs,
                "Nickname": f"packs of {setcode}",
                "ColorDiffuse": tts_output.Pack.colorAttrs,
                "Bag": {"Order": 0},
                "ContainedObjects": [],
            }
        ]
    }
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
                k: point_slicer.get_sampled_numbers(num_packs * i["max_sheet_length"], i["per_pack_count"])
                for k, i in setJSON["flag_data"]["duplicate_control"]["slots_counts"].items()
            }
            # Log duplicate_control_list
            # log["d_c"] = duplicate_control_list[:]
    all_packs = []
    for _ in range(num_packs):
        raw_cn_cards, foil_indexes, seed = p_creator.pack_gen_v3(set=setJSON, d_c=duplicate_control_list)
        # Log the seed
        # log["seeds"].append(seed)
        all_packs.append([raw_cn_cards, foil_indexes])
    all_cn_sets = []
    for p in all_packs:
        all_cn_sets += p[0]
    set_info = tts_output.ijson_collection(all_cn_sets)
    for p in all_packs:
        # print([a['name'] for a in set_info])
        # print(len(raw_cn_cards))
        # print(len(set_info))
        new_colle = []
        for crd in p[0]:
            new_colle += [x for x in set_info if x["collector_number"] == crd[0] and x["set"] == crd[1]]
        # print([a['name'] for a in new_colle])
        pack_to_add = tts_output.Pack()
        pack_to_add.import_cards(
            new_colle,
            p[1],
        )
        save["ObjectStates"][0]["ContainedObjects"].append(pack_to_add.toDict())
    if land_pack:
        pack_to_add = tts_output.Pack()
        pack_to_add.import_cards(
            [
                x
                for x in filter(
                    lambda x: x["name"] in ["Plains", "Island", "Swamp", "Mountain", "Forest"],
                    set_info,
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
                "Transform": tts_output.Pack.transformAttrs,
                "Nickname": f"{cc_id}",
                "ColorDiffuse": tts_output.Pack.colorAttrs,
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
    the_cube = tts_output.Pack()
    foil_indexes = []
    for row in reader:
        templist.append([row["Collector Number"], row["Set"]])
        if row["Finish"] == "Foil":
            foil_indexes += [len(templist)]
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
                        ]
                    }
                else:
                    x = {
                        "image_uris": {"png": row["Image URL"] if row["Image URL"] != "" else c["image_uris"]["png"]},
                    }
                cubelist.append({**c, **x})
                break
    the_cube.import_cards(cubelist, foil_indexes)
    save["ObjectStates"][0]["ContainedObjects"] = [the_cube.toDict()]
    return save
