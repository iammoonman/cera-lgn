import { GetObjectCommand, S3Client } from "@aws-sdk/client-s3";
const s3 = new S3Client({ region: "us-east-1" });
export const handler = async (event) => {
	const id = event.queryStringParameters?.q ?? "0000579f-7b35-4ed3-b44c-db2a538066fe";
	try {
		const Bucket = "flamewave";
		const Key = `${id}.json`;
		const getObjectCommand = new GetObjectCommand({ Bucket, Key });
		const response = await s3.send(getObjectCommand);
		const data = await response.Body.transformToString("utf-8");
		const out = JSON.parse(data);
		return JSON.stringify({
			CardID: 100,
			CustomDeck: { "1": out.img },
			...out.obj,
		});
	} catch {
		return JSON.stringify({});
	}
};
