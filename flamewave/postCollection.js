import { GetObjectCommand, S3Client } from "@aws-sdk/client-s3";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, GetCommand } from "@aws-sdk/lib-dynamodb";
const s3 = new S3Client({ region: "us-east-1" });
const dbc = new DynamoDBClient({ region: "us-east-1" });
const doc = DynamoDBDocumentClient.from(dbc);
/**
 *
 * @param {import("aws-lambda").LambdaFunctionURLEvent} event
 * @returns
 */
export const handler = async (event) => {
	const postData = JSON.parse(event.body);
	if (!Array.isArray(postData)) {
		return "{}"
	}
	const deckids = [];
	const objentries = [];
	const imgrecord = new Map();
	const ids = [];
	const quants = [];
	for (let { flamewave_id, scryfall_id, set, cn, oracle_id, quantity } of postData) {
		let command = null;
		if (flamewave_id) {
			// Verify that the flamewave_id is valid.
			command = new GetCommand({ TableName: "flamewave", Key: { flamewave_id }, AttributesToGet: ["flamewave_id"] });
		} else if (scryfall_id) {
			command = new GetCommand({ TableName: "flamewave", Key: { scryfall_id }, AttributesToGet: ["flamewave_id"] });
		} else if (set && cn) {
			command = new GetCommand({ TableName: "flamewave", Key: { set, cn }, AttributesToGet: ["flamewave_id"] });
		} else if (oracle_id) {
			command = new GetCommand({ TableName: "flamewave", Key: { oracle_id }, AttributesToGet: ["flamewave_id"] });
		}
		try {
			const resp = await doc.send(command);
			if (resp.Item !== undefined) {
				const i = ids.findIndex(v => v === resp.Item["flamewave_id"])
				if (i > -1) {
					quants[i] += quantity
				} else {
					ids.push(resp.Item["flamewave_id"]);
					quants.push(quantity ?? 1);
				}
			} else {
				return "{}"
			}
		} catch (e) {
			return "{}"
		}
	}
	const transformPool = []
	const qpool = []
	for (let i = 0; i < ids.length; i++) {
		try {
			const getObjectCommand = new GetObjectCommand({ Bucket: "flamewave", Key: `${ids[i]}.json` });
			const resp = await s3.send(getObjectCommand);
			if (resp.Body) {
				transformPool.push(resp.Body?.transformToString('utf-8'))
				qpool.push(quants[i])
			}
		} catch (e) {
			return "{}"
		}
	}
	await Promise.allSettled(transformPool).then(vs => {
		let count = 0
		for (let { value: st, status } of vs) {
			if (!st || status === "rejected") {
				return
			}
			const out = JSON.parse(st);
			count += 1;
			imgrecord.set(count, out.img);
			for (let e = 0; e < qpool[count]; e++) {
				deckids.push(count);
				objentries.push(out.obj);
			}
		}
	})
	return JSON.stringify({
		Name: "Deck",
		Transform: {
			scaleX: 1.0,
			scaleY: 1.0,
			scaleZ: 1.0,
		},
		DeckIDs: deckids.map(v => v * 100),
		CustomDeck: Object.fromEntries(imgrecord),
		ContainedObjects: objentries,
	});
};
