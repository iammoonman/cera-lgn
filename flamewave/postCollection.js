import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, BatchGetCommand } from "@aws-sdk/lib-dynamodb";
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
	if (postData.length < 2) return "{}"
	let requests = [];
	for (let { flamewave_id, scryfall_id, set, cn, oracle_id, quantity } of postData) {
		if (flamewave_id) {
			// Verify that the flamewave_id is valid.
			requests.push({ flamewave_id })
		} else if (scryfall_id) {
			requests.push({ scryfall_id })
		} else if (set && cn) {
			requests.push({ set, cn })
		} else if (oracle_id) {
			requests.push({ oracle_id })
		}
	}
	const quants = [];
	const ids = [];
	for (let ind = 0; ind < requests.length; ind += 25) {
		let command = new BatchGetCommand({ RequestItems: { flamewave: { Keys: requests.slice(ind, ind + 25) } } })
		let resp = await doc.send(command);
		if (resp.Responses !== undefined) {
			resp.Responses.flamewave.forEach((e) => {
				let i = ids.findIndex(v => v["flamewave_id"] === e["flamewave_id"])
				if (i > -1) {
					quants[i] += 1
				} else {
					ids.push(e);
					quants.push(requests[ind].quantity ?? 1);
				}
			})
		} else {
			return "{}"
		}
	}
	const deckids = [];
	const objentries = [];
	const imgrecord = new Map();
	for (let entry of ids) {
		count += 1;
		imgrecord.set(count, entry.img);
		for (let e = 0; e < qpool[count - 1]; e++) {
			deckids.push(count);
			objentries.push(entry.obj);
		}
	}
	if (deckids.length < 2) {
		console.log(objentries)
		return "{}"
	}
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
