import json

import starlight
import flamewave


def get_packs(setcode, num_packs, land_pack=False):
    """Returns a JSON save file for Tabletop Simulator."""
    with open(f"starlight/v2/{setcode}.json", "rb") as f:
        setJSON = json.load(f)
    save = flamewave.tts_classes.Save(name=f"packs of {setcode}")
    all_packs = []
    for _ in range(num_packs):
        raw_cn_cards, foil_indexes = starlight.p_generation.generatepack_c1c2_special(sheet_index_func=lambda a: starlight.number_generator.get_number(a), setJSON=setJSON)
        all_packs.append([raw_cn_cards, foil_indexes])
    all_cn_sets = []
    for p in all_packs:
        all_cn_sets += p[0]
    set_info = flamewave.collection_import.mm_collection(all_cn_sets)
    for p in all_packs:
        new_colle = []
        for crd in p[0]:
            new_colle += [x for x in set_info if x["collector_number"] == crd[0] and x["set"] == crd[1]]
        pack_to_add = flamewave.tts_classes.Deck()
        pack_to_add.import_cards(new_colle, p[1])
        save.addObject(pack_to_add)
    if land_pack:
        basicslist = ["Plains", "Island", "Swamp", "Mountain", "Forest"]
        setcode = "m21" if setcode in ["fun"] else setcode
        pack_to_add = flamewave.tts_classes.Deck()
        basic_cards = flamewave.collection_import.scryfall_collection([[setcode, i] for i in basicslist])
        pack_to_add.import_cards(basic_cards)
        save.addObject(pack_to_add)
    return save.getOut()


def get_packs_v3(setcode, num_packs, land_pack=False):
    """Returns a JSON save file for Tabletop Simulator. Also returns logging information."""
    with open(f"starlight/v3/{setcode}.json", "rb") as f:
        setJSON = json.load(f)
    save = flamewave.tts_classes.Save(name=f"packs of {setJSON['full_name']}")
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
            duplicate_control_list = {k: starlight.number_generator.get_sampled_numbers(num_packs * i["per_pack_count"], i["max_sheet_length"]) for k, i in setJSON["flag_data"]["duplicate_control"]["slots_counts"].items()}
            # Log duplicate_control_list
            # log["d_c"] = duplicate_control_list[:]
    all_packs = []
    for _ in range(num_packs):
        raw_cn_cards, foil_indexes, seed = starlight.p_generation.pack_gen_v3(set=setJSON, d_c=duplicate_control_list)
        # Log the seed
        # log["seeds"].append(seed)
        all_packs.append([raw_cn_cards, foil_indexes])
    all_cn_sets = []
    for p in all_packs:
        all_cn_sets += p[0]
    set_info = {**flamewave.collection_import.mm_collection(all_cn_sets, True), **flamewave.planesculptors.ps_collection(all_cn_sets, True)}
    for p in all_packs:
        new_colle = []
        for crd in p[0]:
            if f"{crd[0]}{crd[1]}" in set_info:
                new_colle += [set_info[f"{crd[0]}{crd[1]}"]]
            else:
                raise Exception(f"Card does not exist: {crd[0]} {crd[1]}")
        pack_to_add = flamewave.tts_classes.Deck()
        pack_to_add.import_cards(new_colle, p[1])
        save.addObject(pack_to_add)
    if land_pack:
        basicslist = ["Plains", "Island", "Swamp", "Mountain", "Forest"]
        setcode = setJSON["default_set"]
        pack_to_add = flamewave.tts_classes.Deck()
        basic_cards = flamewave.collection_import.scryfall_collection([[setcode, i] for i in basicslist])
        pack_to_add.import_cards(basic_cards)
        save.addObject(pack_to_add)
    return save.getOut()  # , log


def get_p1p1_v3(setcode):
    """Returns a list of card objects for use in the p1p1 function."""
    with open(f"starlight/v3/{setcode}.json", "rb") as f:
        setJSON = json.load(f)
    duplicate_control_list = {}
    if "flag_data" in setJSON.keys():
        if "duplicate_control" in setJSON["flag_data"].keys():
            duplicate_control_list = {k: starlight.number_generator.get_sampled_numbers(i["per_pack_count"], i["max_sheet_length"]) for k, i in setJSON["flag_data"]["duplicate_control"]["slots_counts"].items()}
            # Log duplicate_control_list
            # log["d_c"] = duplicate_control_list[:]
    raw_cn_cards, foil_indexes, seed = starlight.p_generation.pack_gen_v3(set=setJSON, d_c=duplicate_control_list)
    # Log the seed
    # log["seeds"].append(seed)
    set_info = {**flamewave.collection_import.mm_collection(raw_cn_cards, True), **flamewave.planesculptors.ps_collection(raw_cn_cards, True)}
    new_colle = []
    for crd in raw_cn_cards:
        if f"{crd[0]}{crd[1]}" in set_info:
            new_colle += [set_info[f"{crd[0]}{crd[1]}"]]
        else:
            raise Exception(f"Card does not exist: {crd[0]} {crd[1]}")
    return new_colle, foil_indexes


def get_packs_setfile(setfile, num_packs, land_pack=False):
    """Returns a JSON save file for Tabletop Simulator."""
    setJSON = json.load(setfile)
    setcode = setJSON["default_set"]
    save = flamewave.tts_classes.Save(name=f"packs of {setJSON['full_name']}")
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
            duplicate_control_list = {k: starlight.number_generator.get_sampled_numbers(num_packs * i["per_pack_count"], i["max_sheet_length"]) for k, i in setJSON["flag_data"]["duplicate_control"]["slots_counts"].items()}
            # Log duplicate_control_list
            # log["d_c"] = duplicate_control_list[:]
    all_packs = []
    for _ in range(num_packs):
        raw_cn_cards, foil_indexes, seed = starlight.p_generation.pack_gen_v3(set=setJSON, d_c=duplicate_control_list)
        # Log the seed
        # log["seeds"].append(seed)
        all_packs.append([raw_cn_cards, foil_indexes])
    all_cn_sets = []
    for p in all_packs:
        all_cn_sets += p[0]
    set_info = {**flamewave.collection_import.mm_collection(all_cn_sets, True), **flamewave.planesculptors.ps_collection(all_cn_sets, True)}
    for p in all_packs:
        new_colle = []
        for crd in p[0]:
            if f"{crd[0]}{crd[1]}" in set_info:
                new_colle += [set_info[f"{crd[0]}{crd[1]}"]]
            else:
                raise Exception(f"Card does not exist: {crd[0]} {crd[1]}")
        pack_to_add = flamewave.tts_classes.Deck()
        pack_to_add.import_cards(new_colle, p[1])
        save.addObject(pack_to_add)
    if land_pack:
        basicslist = ["Plains", "Island", "Swamp", "Mountain", "Forest"]
        setcode = "m21"
        pack_to_add = flamewave.tts_classes.Deck()
        basic_cards = flamewave.collection_import.scryfall_collection([[setcode, i] for i in basicslist])
        pack_to_add.import_cards(basic_cards)
        save.addObject(pack_to_add)
    return save.getOut()  # , log
