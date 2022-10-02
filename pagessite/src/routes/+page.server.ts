import fs from 'fs';
import type { CardDisplayType } from 'src/types/displaycard';
import { json_to_new, type Draft } from '../types/events';
import { NODE_ENV, DIS_TOKEN } from '$env/static/private';
import { Client, REST, Routes } from 'discord.js'
export const prerender = true;
export function load() {
    const CDs: (Draft | CardDisplayType)[] = [];
    const users = new Map([])
    // const rest = new REST({ version: '10' }).setToken(DIS_TOKEN);
    const client = new Client({ intents: ['GuildMembers'] });
    client.login(DIS_TOKEN)
    // let thanos = client.users.fetch('237059875073556481').then(y => { console.log(y); return y })
    // console.log(thanos)
    fs.readdir('./src/data', (e, fn) => {
        // console.log(e);
        if (e) {
            return;
        }
        fn.forEach((fname) => {
            fs.readFile('./src/data/' + fname, 'utf-8', (error, content) => {
                if (error) {
                    return;
                }
                const cn: (Draft | CardDisplayType) = json_to_new(JSON.parse(content));
                if ('date' in cn) {
                    cn.scores.forEach(async (v, i) => {
                        if (!users.get(v.id)) {
                            users.set(v.id, client.users.fetch(`${v.id}`).then(y => y).catch(console.error) ?? {id: `${v.id}`, ursername: 'Unknown', discriminator: '0000'})
                        }
                    })
                }
                CDs.push(cn);
            });
        });
    })
    // cn.forEach(x => {
    //     if ('date' in x) {
    //         x.scores.forEach((v) => users.get(v.id) === undefined ? users.set(v.id, fetchUser(v.id).then((y) => y)) : null)
    //     }
    // })
    return { cds: CDs, users: users }
    // CDs = [
    // 	{
    // 		cn: '1',
    // 		id: 0,
    // 		p_id: '237059875073556481',
    // 		set: 'ala',
    // 		title: 'test',
    // 		description: '',
    // 		uri: 'https://c1.scryfall.com/file/scryfall-cards/large/front/7/7/774ec405-5127-4475-8c74-b8858bd84379.jpg?1562877904'
    // 	},
    // 	{
    // 		cn: '1',
    // 		id: 0,
    // 		p_id: '237059875073556481',
    // 		set: 'ala',
    // 		title: 'test',
    // 		description: '',
    // 		uri: 'https://c1.scryfall.com/file/scryfall-cards/large/front/7/7/774ec405-5127-4475-8c74-b8858bd84379.jpg?1562877904'
    // 	},
    // 	{
    // 		date: new Date(),
    // 		id: 0,
    // 		rounds: new Map([
    // 			[
    // 				0,
    // 				{
    // 					matches: [
    // 						{
    // 							p_ids: ['411627939478765568', '237059875073556481'],
    // 							bye: false,
    // 							drops: [],
    // 							games: new Map([
    // 								[0, '411627939478765568'],
    // 								[1, '411627939478765568']
    // 							])
    // 						},
    // 						{
    // 							p_ids: ['320756550992134145', '317470784870285323'],
    // 							bye: false,
    // 							drops: [],
    // 							games: new Map([
    // 								[0, '320756550992134145'],
    // 								[1, '320756550992134145']
    // 							])
    // 						},
    // 						{
    // 							p_ids: ['298561362034950154', '247076572295593984'],
    // 							bye: false,
    // 							drops: ['247076572295593984'],
    // 							games: new Map([
    // 								[0, '298561362034950154'],
    // 								[1, '298561362034950154']
    // 							])
    // 						},
    // 						{
    // 							p_ids: ['250385022106730496', '265851480462852096'],
    // 							bye: false,
    // 							drops: ['250385022106730496'],
    // 							games: new Map([
    // 								[0, '265851480462852096'],
    // 								[1, '265851480462852096']
    // 							])
    // 						}
    // 					]
    // 				}
    // 			],
    // 			[
    // 				1,
    // 				{
    // 					matches: [
    // 						{
    // 							p_ids: ['320756550992134145', '265851480462852096'],
    // 							bye: false,
    // 							drops: ['320756550992134145', '265851480462852096'],
    // 							games: new Map([
    // 								[0, '320756550992134145'],
    // 								[1, '320756550992134145']
    // 							])
    // 						},
    // 						{
    // 							p_ids: ['411627939478765568', '298561362034950154'],
    // 							bye: false,
    // 							drops: ['298561362034950154'],
    // 							games: new Map([[0, '411627939478765568']])
    // 						},
    // 						{
    // 							p_ids: ['237059875073556481', '317470784870285323'],
    // 							bye: false,
    // 							drops: [],
    // 							games: new Map([
    // 								[0, '237059875073556481'],
    // 								[1, '317470784870285323'],
    // 								[2, '237059875073556481']
    // 							])
    // 						}
    // 					]
    // 				}
    // 			],
    // 			[
    // 				2,
    // 				{
    // 					matches: [
    // 						{
    // 							p_ids: ['411627939478765568', '317470784870285323'],
    // 							bye: false,
    // 							drops: [],
    // 							games: new Map([[0, '411627939478765568']])
    // 						},
    // 						{
    // 							p_ids: ['237059875073556481'],
    // 							bye: true,
    // 							drops: [],
    // 							games: new Map()
    // 						}
    // 					]
    // 				}
    // 			]
    // 		]),
    // 		scores: [
    // 			{ id: '411627939478765568', points: 9, gwp: 1.0, ogp: 0.4667, omp: 0.5 },
    // 			{ id: '237059875073556481', points: 6, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
    // 			{ id: '320756550992134145', points: 6, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
    // 			{ id: '298561362034950154', points: 3, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
    // 			{ id: '265851480462852096', points: 3, gwp: 0.5, ogp: 0.6667, omp: 0.6667 },
    // 			{ id: '317470784870285323', points: 0, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
    // 			{ id: '247076572295593984', points: 0, gwp: 0, ogp: 0.6667, omp: 0.5 },
    // 			{ id: '250385022106730496', points: 0, gwp: 0, ogp: 0.5, omp: 0.5 }
    // 		],
    // 		tag: 'dps',
    // 		title: 'TEST TITLE',
    // 		description:
    // 			'TEST DESCRIPTION lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum'
    // 	}
    // ];
}

const fetchUser = async (id: string) => {
    const response = await fetch(`https://discord.com/api/v9/users/${id}`, {
        headers: {
            Authorization: `Bot ${DIS_TOKEN}`
        }
    })
    if (!response.ok) return `Error status code: ${response.status}`;
    // console.log(await response.json())
    let x = await response.json()
    // console.log(x)
    return x // JSON.parse(x)
}