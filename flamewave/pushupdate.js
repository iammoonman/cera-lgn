import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, PutCommand } from '@aws-sdk/lib-dynamodb';
const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);
export const handler = async (event) => {
    const set = event.set ?? event.queryStringParameters.set ?? JSON.parse(event).set;
    const scryfallresponse = await fetch(`https://api.scryfall.com/cards/search?q=set%3A${set}`);
    const { data } = await scryfallresponse.json();
    if (!data) return;
    let counter = 0;
    for (let card of data) {
        const command = new PutCommand({
            TableName: "flamewave",
            Item: {
                flamewave_id: card.id,
                scryfall_id: card.id,
                set: card.set,
                cn: card.collector_number,
                oracle_id: card.oracle_id ?? card.card_faces?.at(0)?.oracle_id ?? "",
                img: {
                    FaceURL: card.image_uris?.normal ?? card.card_faces?.at(0)?.image_uris?.normal ?? "",
                    BackURL: "",
                    NumWidth: 1,
                    NumHeight: 1,
                    BackIsHidden: true
                },
                obj: {
                    Transform: {
                        scaleX: 1.0,
                        scaleY: 1.0,
                        scaleZ: 1.0
                    },
                    Name: "Card",
                    Nickname: `${card.name}\n${card.type_line}`,
                    Description: card.card_faces && `${makeDescription(card.card_faces.at(0), card)}\n[6E6E6E]${makeDescription(card.card_faces.at(1), card)}[-]` || makeDescription(card),
                    States: card.card_faces && {
                        "2": {
                            Name: "Card",
                            Transform: {
                                scaleX: 1.0,
                                scaleY: 1.0,
                                scaleZ: 1.0
                            },
                            Nickname: `${card.name}\n${card.type_line}`,
                            Description: `[6E6E6E]${makeDescription(card.card_faces.at(0), card)}\n[-]${makeDescription(card.card_faces.at(1), card)}`,
                            LuaScript: "",
                            Memo: card.oracle_id ?? card.card_faces?.at(1)?.oracle_id ?? "",
                            CardID: 100,
                            CustomDeck: {
                                "1": {
                                    FaceURL: card.card_faces?.at(1)?.image_uris?.normal ?? card.image_uris?.normal ?? "",
                                    BackURL: "",
                                    NumWidth: 1,
                                    NumHeight: 1,
                                    BackIsHidden: true
                                }
                            }
                        }
                    } || {},
                    LuaScript: ((card.type_line.includes("Siege") && card.type_line.includes("Battle")) || card.layout.includes("planar")) && "function onLoad()self.alt_view_angle=Vector(180,0,180)end" || "",
                    Memo: card.oracle_id ?? card.card_faces?.at(0)?.oracle_id
                },
                type: card.type_line ?? "",
                name: card.name ?? "",
                mv: card.cmc ?? 0,
                colors: card.colors?.reduce((a, clr) => a + clr, "") ?? card.card_faces?.reduce((a, fc) => a + fc.colors?.reduce((t, sc) => t + sc, ""), ""),
                rarity: card.rarity.charAt(0) ?? "c",
            },
            ReturnConsumedCapacity: "TOTAL"
        });
        await docClient.send(command);
        if (counter > 5) {
            await new Promise(r => setTimeout(r, 500));
            counter = 0;
        } else {
            counter++;
        }
    }
    return;
}

function makeDescription(cardface, card) {
    return `[b]${cardface.name} ${cardface.mana_cost}[/b]\n${cardface.type_line} |${cardface.rarity?.charAt(0) ?? card.rarity}|\n${cardface.oracle_text ?? ""}\n${(cardface.power && '[b]' + cardface.power + '/' + cardface.toughness + '[/b]\n') || (cardface.loyalty && 'Starting Loyalty: [b]' + cardface.loyalty + '[/b]\n') || (cardface.defense && 'Defense: ' + cardface.defense) || ''}`
}