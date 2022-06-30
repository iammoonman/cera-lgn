import json

from exports import tts_output
from packcreator import p_creator, point_slicer


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
                k: point_slicer.get_sampled_numbers(num_packs * i["per_pack_count"], i["max_sheet_length"])
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


def get_p1p1_v3(setcode):
    """Returns a list of card objects for use in the p1p1 function."""
    with open(f"sj3/{setcode}.json" if __name__ == "__main__" else f"packcreator/sj3/{setcode}.json", "rb") as f:
        setJSON = json.load(f)
    duplicate_control_list = {}
    if "flag_data" in setJSON.keys():
        if "duplicate_control" in setJSON["flag_data"].keys():
            duplicate_control_list = {
                k: point_slicer.get_sampled_numbers(i["per_pack_count"], i["max_sheet_length"])
                for k, i in setJSON["flag_data"]["duplicate_control"]["slots_counts"].items()
            }
            # Log duplicate_control_list
            # log["d_c"] = duplicate_control_list[:]
    raw_cn_cards, foil_indexes, seed = p_creator.pack_gen_v3(set=setJSON, d_c=duplicate_control_list)
    # Log the seed
    # log["seeds"].append(seed)
    set_info = tts_output.ijson_collection(raw_cn_cards)
    new_colle = []
    for crd in raw_cn_cards:
        new_colle += [x for x in set_info if x["collector_number"] == crd[0] and x["set"] == crd[1]]
    return new_colle, foil_indexes
