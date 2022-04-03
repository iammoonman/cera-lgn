"""GENERALIZED"""
import random
import pickle


def generatepack_c1c2_special(
    sheet_index=0, sheet_index_func=lambda a: random.randint(0, 121), setJSON=None
):
    """
    Takes a set_template JSON object, parsed.

    Returns a pack in the btts.py format, [ ('collector_number','set_code'), ... ].

    Returns indexes of the list which indicate foiled cards.
    """
    distribution = random.choices(
        [d[0] for d in setJSON["distributions_odds"]],
        [d[1] for d in setJSON["distributions_odds"]],
    )[0]
    ABCD_c = random.choices(
        [c[0] for c in setJSON["ABCD_commons_odds"]],
        [c[1] for c in setJSON["ABCD_commons_odds"]],
    )[0]
    ABCD_u = random.choices(
        [u[0] for u in setJSON["ABCD_uncommon_odds"]],
        [u[1] for u in setJSON["ABCD_uncommon_odds"]],
    )[0]
    ABCD_r = random.choices(
        [u[0] for u in setJSON["rare_slot_odds"]],
        [u[1] for u in setJSON["rare_slot_odds"]],
    )[0]
    pack = []  # The pack object. Put [cn,set_code] objects into this list.
    keydrops_c = []
    # Contains the keys from the common ABCD to skip adding to make room for foils.
    keydrops_u = []
    # Contains the keys from the uncommon ABCD to skip adding to make room for foils.
    keydrops_r = 0  # Might be redundant. Tallies the number of rares to drop if using extra sheets. Number rather than list due to rarity independence.
    if "drops" in distribution.keys():
        # Calculate drops, which remove one number from a given key for the ABCD.
        if "c" in distribution["drops"]:
            for d in range(distribution["drops"]["c"]):
                keydrops_c.append(random.choice(list(ABCD_c.keys())))
        if "u" in distribution["drops"]:
            for d in range(distribution["drops"]["u"]):
                keydrops_u.append(random.choice(list(ABCD_u.keys())))
        if "r" in distribution["drops"]:
            keydrops_r += distribution["drops"]["r"]
    for key, value in ABCD_c.items():
        # For each sheet key in the ABCD, take the value and grab that many cards from the sheet.
        sheet_index = sheet_index_func(value)
        for p in range(value - len([j for j in keydrops_c if j == key])):
            pack = pack + [
                (
                    setJSON["ABCD_common_sheets"][key][
                        (sheet_index + p) % len(setJSON["ABCD_common_sheets"][key])
                    ],
                    setJSON["set_code"],
                )
            ]
    for key, value in ABCD_u.items():
        # For each sheet key in the ABCD, take the value and grab that many cards from the sheet.
        sheet_index = sheet_index_func(value)
        for p in range(value - len([j for j in keydrops_u if j == key])):
            pack = pack + [
                (
                    setJSON["ABCD_uncommon_sheets"][key][
                        (sheet_index + p) % len(setJSON["ABCD_uncommon_sheets"][key])
                    ],
                    setJSON["set_code"],
                )
            ]
    for key, value in ABCD_r.items():
        # Grab that many rares from the selected rare sheet.
        sheet_index = sheet_index_func(value)
        # Manually check if the rare has been hit recently.
        # If it tries to hit a duplicate more than 10 times, reset the tracker. Can't calculate how far out this would be, but it should prevent a ton of duplicate rares.
        # This might introduce some real lag.
        # Also, whiffs on double rares; if taking more than one rare, it could choose X-1 as the pointer and take the duplicate. Not too likely, but possible.

        try:
            with open("prevrares.pickle", "rb") as f:
                prev_rares = pickle.load(f)
        except:
            with open("prevrares.pickle", "wb") as f:
                prev_rares = [[], 0]
                pickle.dump(prev_rares, f)
        while sheet_index in prev_rares[0]:
            # Loop while the rare chosen had been chosen recently. Pick a new one unless the "recent" rares aren't recent anymore.
            prev_rares[1] += 1
            if prev_rares[1] > 50:
                prev_rares = [[], 0]
                break
            else:
                sheet_index = sheet_index_func(value)
        prev_rares[0] += [sheet_index]
        with open("prevrares.pickle", "wb") as f:
            pickle.dump(prev_rares, f)

        # Now that the number has been checked, actually put in the rare.
        for p in range(value - keydrops_r):
            pack = pack + [
                (
                    setJSON["rare_slot_sheets"][key][
                        (sheet_index + value) % len(setJSON["rare_slot_sheets"][key])
                    ],
                    setJSON["set_code"],
                )
            ]
    f_indexes = []
    # Tracks the indexes of foils within the pack.
    if "f" in distribution.keys():
        # Grab that many foils from the foil sheets. In the case of multiple foils, rarity is independently selected.
        sheet_index = sheet_index_func(distribution["f"])
        for _ in range(distribution["f"]):
            pack = pack + [
                (
                    (
                        sheet := (
                            random.choices(
                                [g[0] for g in setJSON["foil_sheets_odds"]],
                                [g[1] for g in setJSON["foil_sheets_odds"]],
                            )[0]
                        )
                    )[sheet_index % len(sheet)],
                    setJSON["set_code"],
                )
            ]
            f_indexes.append(len(pack))
    for key in [
        key for key in distribution.keys() if key not in ["c", "u", "r", "f", "drops"]
    ]:
        # Catch special sheets.
        sheet_index = sheet_index_func(distribution[key])
        for n in range(distribution[key]):
            pack = pack + [
                (
                    (
                        sheet := (
                            random.choices(
                                setJSON["extras_sheets_odds"][key][0],
                                setJSON["extras_sheets_odds"][key][1],
                            )[0]
                        )
                    )[sheet_index % len(sheet)],
                    setJSON["extras_sheets_odds"][key][2],
                )
            ]
    # Reverse the pack and pivot the foil indexes. This hides the rare at the bottom of the card stack in TTS.
    return pack[::-1], [(r + (len(pack) - r) * 2) % len(pack) for r in f_indexes]


if __name__ == "__main__":
    import json
    import point_slicer

    with open("packcreator/setjson/mid.json", "rb") as f:
        ooo = json.load(f)
        for n in range(24):
            w, n = generatepack_c1c2_special(
                sheet_index=0,
                setJSON=ooo,
                sheet_index_func=lambda a: point_slicer.get_number(a),
            )
            print(w, n)
