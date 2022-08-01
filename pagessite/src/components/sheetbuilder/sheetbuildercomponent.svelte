<script lang="ts">
	import { onMount } from 'svelte';
	import { afterUpdate } from 'svelte';

	import Draggerbox from './draggerbox.svelte';
	let cardlist = [] as {
		cardname: string;
		uri: string;
		id: number;
		set: string;
		cn: string;
	}[];
	let defaultcardlist = [
		['11', 'eld'],
		['5', 'isd'],
		['24', 'afr'],
		['5', 'isd'],
		['24', 'afr'],
		['5', 'isd'],
		['24', 'afr'],
		['5', 'isd'],
		['24', 'afr'],
		['5', 'isd'],
		['24', 'afr'],
		['5', 'isd'],
		['24', 'afr']
	];
	onMount(async () => {
		let identifiers: any[] = [];
		defaultcardlist.map(async (d) => {
			identifiers.push({
				collector_number: d[0],
				set: d[1] == '' ? 'lea' : d[1]
			});
		});
		console.log({ identifiers: identifiers });
		const resp = await fetch(`https://api.scryfall.com/cards/collection`, {
			method: 'POST',
			mode: 'cors',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ identifiers: identifiers })
		})
			.then((r) => r.json())
			.then((j) => {
                const newlist: any[] = [];
				defaultcardlist.map((e, i) => {
					const cardstuff = j.data.find((q: any) => q.collector_number == e[0] && q.set == e[1]);
					newlist.push({
						cardname: cardstuff.name,
						cn: cardstuff.collector_number,
						set: cardstuff.set,
						id: i,
						uri: cardstuff.image_uris.small
					});
				});
                // this assignment MUST be here
                // this aint react, props dont just update by themselves
                cardlist = newlist;
			});
		console.log(cardlist);
	});
</script>

<div>
	<Draggerbox propcardlist={cardlist} />
</div>
