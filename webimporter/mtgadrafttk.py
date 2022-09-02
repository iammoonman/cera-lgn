import ijson
import io

from exporttemplates import tts_output, tts_import


def create_mtgadrafttk(draft_file: io.FileIO):
    # Push the file into ijson generator
    # carddata is k,v for data. Not the same as oracle_id.
    #  Contains the oracle_id for querying and set,cn
    #  Also contains the image links
    # sessionID as a name
    # users > userName
    # users > picks as keys for carddata
    name = ""
    name_gen = ijson.items(draft_file, "sessionID")
    for u in name_gen:
        name = u
    draft_file.seek(0)
    cards = {}
    cards_generator = ijson.kvitems(draft_file, "carddata")
    for k, v in cards_generator:
        cards[k] = [v["collector_number"], v["set"]]  # add extra properties for customs
    ij_cards = tts_import.ijson_collection([[v[0], v[1]] for k, v in cards.items()], True)
    draft_file.seek(0)
    users = {}
    users_generator = ijson.kvitems(draft_file, "users")
    for k, v in users_generator:
        users[k] = {"name": v["userName"], "picks": v["cards"], "pack": tts_output.Pack(f'cards for {v["userName"]}')}
        users[k]["pack"].import_cards([ij_cards[cards[s][0] + cards[s][1]] for s in users[k]["picks"]])
    s = tts_output.Save(f"Big Draft Bag")
    for k, v in users.items():
        s.addObject(v["pack"])
    # Push carddata into ijson collection blocks at a time
    # Distribute it out to user cards
    return s.getOut(), name
