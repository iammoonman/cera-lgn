
import { writable } from 'svelte/store';

export const sheetlist = writable(
	[] as {
		cardname: string;
		uri: string;
		id: number;
		set: string;
		cn: string;
	}[]
);
