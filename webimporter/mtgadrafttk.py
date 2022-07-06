import ijson
import io

from exporttemplates import tts_output


def create_mtgadrafttk(draft_file: io.FileIO):
    # Push the file into ijson generator
    # carddata is k,v for data. Not the same as oracle_id.
    #  Contains the oracle_id for querying and set,cn
    #  Also contains the image links
    # sessionID as a name
    # users > userName
    # users > picks as keys for carddata
    iterations = 0
    users = {}
    users_generator = ijson.kvitems(draft_file, "users")
    for k, v in users_generator:
        iterations += 1
        users[k] = {
            "name": v["userName"],
            "picks": v["cards"],
            "pack": tts_output.Pack(f'cards for {v["userName"]}')
        }
    draft_file.seek(0)
    cards_generator = ijson.kvitems(draft_file, "carddata")
    while True:
        iterations += 1
        fifty_card_objects = []
        mid_cards = []
        for (k, v), i in zip(cards_generator, range(50)):
            iterations += 1
            mid_cards.append([v["collector_number"], v["set"], k])  # add extra properties for customs
            pass
        fifty_card_objects = tts_output.ijson_collection([[c[0], c[1]] for c in mid_cards], True)
        for obj in mid_cards:
            for u, b in users.items():
                iterations += 1
                if obj[2] in b["picks"]:
                    print(obj[2])
                    # catch this for customs
                    # b["pack"].import_cards(fifty_card_objects[obj[0]+obj[1]])
        if len(mid_cards) < 50:
            break
    s = tts_output.Save(f"Big Draft Bag")
    for k, v in users.items():
        s.addObject(v["pack"])
    # Push carddata into ijson collection blocks at a time
    # Distribute it out to user cards
    print(iterations)
    return s