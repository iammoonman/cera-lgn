import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, GetCommand } from "@aws-sdk/lib-dynamodb";
const dbc = new DynamoDBClient({ region: "us-east-1" });
const doc = DynamoDBDocumentClient.from(dbc);
export const handler = async (event) => {
	const id = event.queryStringParameters?.q ?? "0000579f-7b35-4ed3-b44c-db2a538066fe";
	const getObjectCommand = new GetCommand({
		TableName: "flamewave",
		Key: {
			flamewave_id: id
		}
	});
	const response = await doc.send(getObjectCommand);
	const data = response.Item;
	return JSON.stringify({
		CardID: 100,
		CustomDeck: { "1": data.img },
		...data.obj,
	});
};
