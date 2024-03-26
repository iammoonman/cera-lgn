import json
from xml.etree import ElementTree
import uuid

def fromMSE(file) -> str:
    tree = ElementTree.parse(file)
    root = tree.getroot()
    cards = root.find("cards")
    longcards = []
    for i, card in enumerate(cards):
        cr = {
            "Name": "Card",
            "Transform": {
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0,
            },
            "Nickname": card.find("name").text + ('\n' + card.find('prop').find('type').text if card.find('prop').find('type') else ""),
            "Description": card.find("name").text + ' ' + card.find('prop').find('manacost').text + '\n' + (card.find('prop').find('type').text if card.find('prop').find('type') else "") + ' ' + card.find('set').get('rarity')[0] + ' ' + '\n' + card.find("text").text + ('\n' + card.find('prop').find('pt').text if card.find('prop').find('pt') else ""),
            "Memo": "",
            "LuaScript": "",
            "States": {},
        }
        cd = {
            "FaceURL": "",
            "BackURL": "https://i.imgur.com/TyC0LWj.jpg",
            "NumWidth": 1,
            "NumHeight": 1,
            "BackIsHidden": True,
        }
        longcards.append({
            "cn": f'{i}',
            "set": card.find('set').text,
            "oracle_id": "",
            "scryfall_id": "",
            "flamewave_id": str(uuid.uuid4()),
            "custom_deck": cd,
            "cotd_objs": cr,
        })
    return json.dumps(longcards)
