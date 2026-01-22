import ijson
import io
from flamewave import tts_classes, collection_import


def full_draftmancer_log(draft_file: io.BytesIO):
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
        cards[k] = v["id"]  # add extra properties for customs
    ij_cards = collection_import.ijson_collection_scryfallIDs(cards.values(), True)
    draft_file.seek(0)
    users = {}
    users_generator = ijson.kvitems(draft_file, "users")
    for k, v in users_generator:
        if v['isBot']:
            users[k] = {"name": v["userName"], "picks": v["cards"], "pack": tts_classes.Deck(f'cards for {v["userName"]}')}
            users[k]["pack"].import_cards([ij_cards[cards[s]] for s in users[k]["picks"]])
        else:
            users[k] = {"name": v["userName"], "picks": v["decklist"]["main"], "pack": tts_classes.Deck(f'maindeck cards for {v["userName"]}')}
            users[k]["pack"].import_cards([ij_cards[cards[s]] for s in users[k]["picks"]])
            if len(v["decklist"]["side"]) > 0:
                users[f'{k}_side'] = {"name": v["userName"], "picks": v["decklist"]["side"], "pack": tts_classes.Deck(f'sideboard cards for {v["userName"]}')}
                users[f'{k}_side']["pack"].import_cards([ij_cards[cards[s]] for s in users[f'{k}_side']["picks"]])
    s = tts_classes.Save(f"Big Draft Bag")
    for k, v in users.items():
        s.addObject(v["pack"])
    # Push carddata into ijson collection blocks at a time
    # Distribute it out to user cards
    return s.getOut(), name
