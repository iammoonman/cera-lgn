
import { get, writable } from 'svelte/store';

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

export const V3Store = writable({
	default_set: "",
	full_name: "",
	distros: [],
	slots: new Map([]),
	flag_data: {
	},
} as V3);

export function validateStore() {
	const slots: Record<string, Array<string>> = {};
	const stor = get(V3Store);
	[...stor.slots].forEach(([sk, sv]) => {
		slots[sk] = [...sv.sheets.keys()]
	});
	// Iterate over slots.options
	const newslots = new Map();
	[...stor.slots].forEach(([sk, sv]) => {
		const newOptions: typeof sv.options = []
		sv.options.forEach(x => {
			const newX = {
				struct: new Map([...x.struct].filter(([k, v]) => {
					return slots[sk].find(sheetkey => sheetkey === k)
				})),
				freq: x.freq
			};
			newOptions.push(newX)
		})
		newslots.set(sk, { ...sv, options: newOptions })
	})
	// Iterate over distros.slots
	// Iterate over distros.drops
	const newDistros: typeof stor.distros = []
	stor.distros.forEach(d => {
		const newDS = new Map();
		[...d.slots].forEach(([dsk, dsv]) => {
			if (slots[dsk]) {
				newDS.set(dsk, dsv)
			}
		})
		const newDD = new Map();
		[...d.drops].forEach(([dsk, dsv]) => {
			const newDSV: { key: string; count: number; freq: number; }[] = []
			dsv.forEach(dsvI => {
				if (slots[dsk]) {
					if (slots[dsk].find(n => n == dsvI.key)) {
						newDSV.push(dsvI)
					}
				}
			})
			if (newDSV.length > 0) {
				newDD.set(dsk, newDSV)
			}
		})
		newDistros.push({ slots: newDS, drops: newDD, freq: d.freq })
	})
	V3Store.update(oldstore => {
		return { ...oldstore, distros: newDistros, slots: newslots }
	})
}