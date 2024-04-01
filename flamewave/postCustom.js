import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, PutCommand } from '@aws-sdk/lib-dynamodb';
const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);
export const handler = async (event) => {
    const postData = JSON.parse(event.body);
    if (!Array.isArray(postData)) return `"Failed to load cards."`;
    const commands = [];
    for (const { flamewave_id, scryfall_id, set, cn, oracle_id, img: { FaceURL, BackURL, NumWidth, NumHeight, BackIsHidden }, obj: { Transform, Name, Nickname, Description, States, LuaScript, Memo }, type, name, mv, colors, rarity } of postData) {
        if (!(flamewave_id && (typeof flamewave_id === 'string'))) return `"Failed to load a card."`;
        if (!(set && (typeof set === 'string'))) return `"Failed to load a card."`;
        if (!(cn && (typeof cn === 'string'))) return `"Failed to load a card."`;
        if (!(name && (typeof name === 'string'))) return `"Failed to load a card."`;
        if (!(typeof colors === 'string')) return `"Failed to load a card."`;
        if (!(rarity && (typeof rarity === 'string'))) return `"Failed to load a card."`;
        if (!(typeof mv === 'number')) return `"Failed to load a card."`;
        if (!(FaceURL && (typeof FaceURL === 'string'))) return `"Failed to load a card."`;
        if (!(BackURL && (typeof BackURL === 'string'))) return `"Failed to load a card."`;
        if (!(NumWidth && (typeof NumWidth === 'number'))) return `"Failed to load a card."`;
        if (!(NumHeight && (typeof NumHeight === 'number'))) return `"Failed to load a card."`;
        if (!(BackIsHidden && (typeof BackIsHidden === 'boolean'))) return `"Failed to load a card."`;
        if (!(typeof Nickname === 'string')) return `"Failed to load a card."`;
        if (!(typeof Description === 'string')) return `"Failed to load a card."`;
        if (!(typeof LuaScript === 'string')) return `"Failed to load a card."`;
        if (!(typeof Memo === 'string')) return `"Failed to load a card."`;
        if (JSON.stringify(States).length > 1500) return `"Failed to load a card."`;
        commands.push(new PutCommand({
            TableName: "flamewave",
            Item: {
                flamewave_id, scryfall_id, set, cn, oracle_id,
                img: {
                    FaceURL, BackURL, NumWidth, NumHeight, BackIsHidden
                },
                obj: {
                    Name: "Card", Nickname, Description, LuaScript, Memo, Transform: {
                        scaleX: 1.0,
                        scaleY: 1.0,
                        scaleZ: 1.0
                    }, States
                },
                type, name, mv, colors, rarity,
            },
            ReturnConsumedCapacity: "TOTAL"
        }))
    }
    let counter = 0;
    for (let command of commands) {
        await docClient.send(command);
        if (counter > 5) {
            await new Promise(r => setTimeout(r, 500));
            counter = 0;
        } else {
            counter++;
        }
    }
    return `${counter} cards added to the database.`;
}