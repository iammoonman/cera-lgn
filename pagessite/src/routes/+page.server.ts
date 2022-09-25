import fs from 'fs';
import type { CardDisplayType } from 'src/types/displaycard';
import type { Draft } from 'src/types/events';
import { NODE_ENV } from '$env/static/private';
export const prerender = true;
export function load() {
    const CDs: (Draft | CardDisplayType)[] = [];
    fs.readdir('../data', (e, fn) => {
        if (e) {
            return;
        }
        fn.forEach((fname) => {
            fs.readFile('../data/' + fname, 'utf-8', (error, content) => {
                if (error) {
                    return;
                }
                const cn = JSON.parse(content);
                CDs.push(cn);
            });
        });
    });
    return { cds: CDs }
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