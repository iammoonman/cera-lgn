
import { writable } from 'svelte/store';

type V3 = {
	default_set: string,
	full_name: string,
	distros: { slots: Record<string, number>, drops: Record<string, { key: string, count: number, freq: number }[]>, freq: number }[],
	slots: Record<string, { flags: ('foil' | 'duplicate_control')[], options: { struct: Record<string, number>, freq: number }[], sheets: Record<string, (string | string[])[]> }>,
	flag_data: { duplicate_control?: { slots_counts: Record<string, { per_pack_count: number, max_sheet_length: number }> } }
}

export const V3Store = writable({
	default_set: "lea",
	full_name: "",
	distros: [
		{
			slots: { c: 1, d: 2, e: 3 },
			drops: {
				"c": [{ key: "a", count: 1, freq: 1 }],
				"d": [{ key: "a", count: 1, freq: 1 }, { key: "a", count: 1, freq: 1 }]
			},
			freq: 1
		}
	],
	slots: {
		c: {
			flags: [],
			options: [
				{ struct: { a: 2 }, freq: 1 },
				{ struct: { a: 2, b: 3 }, freq: 1 },
				{ struct: { a: 2, b: 3, c: 4 }, freq: 1 }
			],
			sheets: {
				a: ["1", "2", "3", "4", "5", "6", "7", "1", "9", "10", "11", "1", "1", "2", "3", "4", "5", "6", "7", "1", "9", "10", "11", "1", "1", "2", "3", "4", "5", "6", "7", "1", "9", "10", "11", "1", "2", "3", "4", "5", "6", "7", "1", "9", "10", "11"],
				b: ["1", "2", "3", "4", "5", "6", "7", "1", "9", "10", "11", "1", "1", "2", "3", "4", "5", "6", "7", "1", "9", "10", "11", "1", "1", "2", "3", "4", "5", "6", "7", "1", "9", "10", "11", "1", "2", "3", "4", "5", "6", "7", "1", "9", "10", "11"],
				c: ["1", "2", "3", "4", "5", "6", "7", "1", "9", "10", "11", "1", "1", "2", "3", "4", "5", "6", "7", "1", "9", "10", "11", "1", "1", "2", "3", "4", "5", "6", "7", "1", "9", "10", "11", "1", "2", "3", "4", "5", "6", "7", "1", "9", "10", "11"]
			}
		},
	},
	flag_data: {
	}
} as V3);