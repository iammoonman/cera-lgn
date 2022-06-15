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
    abbr = setJSON["set_code"]
    set_info = tts_output.scryfall_set(abbr)
    codes = [abbr]
    for _ in range(num_packs):
        (raw_cn_cards, foil_indexes,) = p_creator.generatepack_c1c2_special(
            sheet_index_func=lambda a: point_slicer.get_number(a),
            setJSON=setJSON,
        )
        # Find the scryfall set data for the cards in the pack. Could be varied.
        # Grabs the entire set to reduce queries. Watch for memory usage.
        for new_setcode in list(filter(lambda x: x[1] not in codes, raw_cn_cards)):
            set_info += tts_output.scryfall_set(new_setcode[1])
            codes.append(new_setcode[1])
        pack_to_add = tts_output.Pack()
        pack_to_add.import_cards(
            [
                next(c for c in set_info if c["collector_number"] == cn_pair[0] and c["set"] == cn_pair[1])
                for cn_pair in raw_cn_cards
            ],
            foil_indexes,
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
    for row in reader:
        if len(templist) == 10:  # Buffering to serve query length has an impact on sorting.
            # CubeCobra data is always fundamentally based on data from Scryfall. The query will not fail.
            response = requests.get(
                "https://api.scryfall.com/cards/search?q="
                + "".join(
                    [
                        f'(cn%3D"{i["Collector Number"]}"+set%3D{i["Set"]}){"+or+" if templist.index(i)<len(templist)-1 else ""}'
                        for i in templist
                    ]
                )
                + "&unique=prints",
                headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"},
            )
            holdhold = response.json()
            cards_to_import = []
            foil_indexes = []
            for i, n in enumerate(templist):
                # Convert the CubeCobra csv information to the Scryfall data used by the Pack class.
                # This will also catch duplicate cards.
                card_data = copy.deepcopy(
                    [
                        j
                        for j in holdhold["data"]
                        if j["collector_number"] == n["Collector Number"] and j["set"] == n["Set"]
                    ][0]
                )
                if n["Image URL"]:  # Catch whether the CubeCobra card has custom images.
                    if (
                        "card_faces" in card_data.keys()
                        and "Adventure" not in card_data["type_line"]
                        and "split" != card_data["layout"]
                        and "flip" != card_data["layout"]
                    ):
                        card_data["card_faces"][0]["image_uris"]["png"] = n["Image URL"]
                        if n["Image Back URL"]:
                            card_data["card_faces"][1]["image_uris"]["png"] = n["Image Back URL"]
                    else:
                        card_data["image_uris"]["png"] = n["Image URL"]
                cards_to_import.append(card_data)
                if n["Finish"] == "Foil":  # Catch the CubeCobra card being foiled.
                    foil_indexes.append(i)
            the_cube.import_cards(cards_to_import, foil_indexes)
            templist = []
            foil_indexes = []
            time.sleep(0.25)
        if row["Maybeboard"] == "false":  # Maybeboarded cards are included in the csv.
            templist.append(row)
    if len(templist) > 0:
        # Catch an uneven number of cards.
        response = requests.get(
            "https://api.scryfall.com/cards/search?q="
            + "".join(
                [
                    f'(cn%3D"{i["Collector Number"]}"+set%3D{i["Set"]}){"+or+" if templist.index(i)<len(templist)-1 else ""}'
                    for i in templist
                ]
            )
            + "&unique=prints",
            headers={"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"},
        )
        holdhold = response.json()
        cards_to_import = []
        foil_indexes = []
        for i, n in enumerate(templist):
            card_data = copy.deepcopy(
                [
                    j
                    for j in holdhold["data"]
                    if j["collector_number"] == n["Collector Number"] and j["set"] == n["Set"]
                ][0]
            )
            if n["Image URL"]:
                if (
                    "card_faces" in card_data.keys()
                    and "Adventure" not in card_data["type_line"]
                    and "split" != card_data["layout"]
                    and "flip" != card_data["layout"]
                ):
                    # print(card_data["name"])
                    card_data["card_faces"][0]["image_uris"]["png"] = n["Image URL"]
                    if n["Image Back URL"]:
                        card_data["card_faces"][1]["image_uris"]["png"] = n["Image Back URL"]
                else:
                    card_data["image_uris"]["png"] = n["Image URL"]
            cards_to_import.append(card_data)
            if n["Finish"] == "Foil":
                foil_indexes.append(i)
        the_cube.import_cards(cards_to_import, foil_indexes)
        templist = []
        foil_indexes = []
    save["ObjectStates"][0]["ContainedObjects"] = [the_cube.toDict()]
    return save
