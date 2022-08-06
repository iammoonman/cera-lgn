
import { writable } from 'svelte/store';

type V3 = {
	default_set: string,
	full_name: string,
	distros: {
		slots: Map<string, number>,
		drops: Map<string,
			{ key: string, count: number, freq: number }[]>,
		freq: number
	}[],
	slots: Map<string, {
		flags: ('foil' | 'duplicate_control')[],
		options: { struct: Map<string, number>, freq: number }[],
		sheets: Map<string, (string | string[])[]>
	}>,
	flag_data: {
		duplicate_control?: { slots_counts: Record<string, { per_pack_count: number, max_sheet_length: number }> }
	}
}

// export const V3Store = writable({
// 	default_set: "lea",
// 	full_name: "",
// 	distros: [
// 		{
// 			slots: new Map([['c', 1], ['d', 2]]),
// 			drops: new Map([
// 				['c', [{ key: "a", count: 1, freq: 1 }]],
// 				['d', [{ key: "q", count: 1, freq: 1 }, { key: "r", count: 1, freq: 1 }]
// 				]]),
// 			freq: 1
// 		}
// 	],
// 	slots: new Map([
// 		['c', {
// 			flags: [],
// 			options: [
// 				{ struct: new Map(Object.entries({ a: 2 })), freq: 1 },
// 				{ struct: new Map(Object.entries({ a: 2, b: 3 })), freq: 1 },
// 				{ struct: new Map(Object.entries({ a: 2, b: 3, c: 4 })), freq: 1 }
// 			],
// 			sheets: new Map(Object.entries({
// 				a: ["10", "11"],
// 				b: ["10", "11"],
// 				c: ["10", "11"]
// 			}))
// 		}],
// 		['d', {
// 			flags: [],
// 			options: [
// 				{ struct: new Map(Object.entries({ q: 2 })), freq: 1 },
// 				{ struct: new Map(Object.entries({ q: 2, b: 3 })), freq: 1 },
// 				{ struct: new Map(Object.entries({ q: 2, v: 3, r: 4 })), freq: 1 }
// 			],
// 			sheets: new Map(Object.entries({
// 				q: ["10", "11"],
// 				v: ["10", "11"],
// 				r: ["10", "11"]
// 			}))
// 		}],
// 		['q', {
// 			flags: [],
// 			options: [
// 				{ struct: new Map(Object.entries({ q: 2 })), freq: 1 },
// 				{ struct: new Map(Object.entries({ q: 2, b: 3 })), freq: 1 },
// 				{ struct: new Map(Object.entries({ q: 2, v: 3, r: 4 })), freq: 1 }
// 			],
// 			sheets: new Map(Object.entries({
// 				q: ["10", "11"],
// 				v: ["10", "11"],
// 				r: ["10", "11"]
// 			}))
// 		}]
// 	]),
// 	flag_data: {
// 	},
// } as V3);

export const V3Store = writable({
	default_set: "",
	full_name: "",
	distros: [],
	slots: new Map([['q', {
		flags: [],
		options: [
			{ struct: new Map(Object.entries({ q: 2 })), freq: 1 },
			{ struct: new Map(Object.entries({ q: 2, v: 3 })), freq: 1 },
			{ struct: new Map(Object.entries({ q: 2, v: 3, r: 4 })), freq: 1 }
		],
		sheets: new Map(Object.entries({
			q: ["10", "11"],
			v: ["10", "11"],
			r: ["10", "11"]
		}))
	}]]),
	flag_data: {
	},
} as V3);