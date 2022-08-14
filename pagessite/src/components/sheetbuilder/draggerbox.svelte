<script lang="ts">
	import { dndzone } from 'svelte-dnd-action';
	import Button from '../utilities/button.svelte';
	import { V3Selection, V3Store, type V3 } from './stores';
	let cardlist: {
		cardname: string;
		uri: string;
		id: number;
		set: string;
		cn: string;
	}[] = [];
	let slotkey = '';
	let sheetkey = '';
	V3Selection.subscribe((s) => {
		slotkey = s.slotkey;
		sheetkey = s.sheetkey;
	});
	let timer: string | number | NodeJS.Timeout | undefined;
	function debounceUpdate() {
		clearTimeout(timer);
		timer = setTimeout(() => {
			V3Store.update((v) => {
				return {
					...v,
					slots: new Map([
						...v.slots,
						[
							slotkey,
							{
								...v.slots.get(slotkey),
								sheets: new Map([
									...v.slots.get(slotkey)!.sheets,
									[
										sheetkey,
										cardlist.map(
											(e: {
												cardname: string;
												uri: string;
												id: number;
												set: string;
												cn: string;
											}) => {
												return [e.cn, e.set];
											}
										)
									]
								])
							}
						]
					])
				} as V3;
			});
		}, 3000);
	}
	V3Store.subscribe((v) => {
		const tempslot = v.slots.get(slotkey);
		if (tempslot === undefined) return;
		const templist = tempslot.sheets.get(sheetkey);
		if (templist === undefined) return;
		cardlist = templist.map((c, i) => {
			if (Array.isArray(c)) {
				return {
					cardname: '',
					cn: c[0],
					id: i,
					set: c[1],
					uri: ''
				};
			}
			return {
				cardname: '',
				cn: c,
				id: i,
				set: v.default_set,
				uri: ''
			};
		});
		getStuff();
	});

	function handleDndConsider(e: any) {
		cardlist = e.detail.items;
	}
	function handleDndFinalize(e: any) {
		cardlist = e.detail.items;
		debounceUpdate();
	}
	function handleDeleteFinalize(e: any) {
		deletezoneobjects = e.detail.items;
		deletezoneobjects = [];
		cardlist = cardlist.filter(
			(q) =>
				e.detail.items.find((h: any) => {
					return h.id == q.id && h.cn == q.cn && h.set == q.set;
				}) === undefined
		);
		debounceUpdate();
	}
	function handleDeleteConsider(e: any) {
		deletezoneobjects = e.detail.items;
	}
	async function getStuff() {
		let identifiers: { collector_number: string; set: string }[] = [];
		cardlist.map(async (d) => {
			identifiers.push({
				collector_number: d.cn,
				set: d.set
			});
		});
		const resp = await fetch(`https://api.scryfall.com/cards/collection`, {
			method: 'POST',
			mode: 'cors',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ identifiers: identifiers })
		})
			.then((r) => r.json())
			.then((j) => {
				const newlist: typeof cardlist = [];
				cardlist.forEach((e, i) => {
					const cardstuff = j.data.find((q: any) => q.collector_number == e.cn && q.set == e.set);
					if (cardstuff !== undefined) {
						newlist.push({
							cardname: cardstuff.name,
							cn: cardstuff.collector_number,
							set: cardstuff.set,
							id: i,
							uri: cardstuff.image_uris.small
						});
					}
				});
				cardlist = newlist;
			});
	}
	let deletezoneobjects: typeof cardlist = [];
	let searchText = '';
	let searchResults: any[] = [];
</script>

<div class="grid p-2 gap-2" id="draggercomponent">
	<section
		class="rounded-lg cardarea"
		use:dndzone={{ items: cardlist, flipDurationMs: 50, type: 'healthy' }}
		on:consider={handleDndConsider}
		on:finalize={handleDndFinalize}
	>
		{#each cardlist as card (card.id)}
			<div class="singlecard">
				<img src={card.uri} alt={card.cardname} />
			</div>
		{/each}
	</section>
	<section class="">
		<div id="textarea" class="border-black border">
			{`[${cardlist.map((e) => `["${e.cn}", "${e.set}"]`)}]`}
		</div>
	</section>
	<section
		class="rounded-lg cardarea bg-red-100"
		use:dndzone={{ items: deletezoneobjects, flipDurationMs: 50, type: 'healthy' }}
		style="height: 100px; width: 100px; overflow: hidden;"
		on:consider={handleDeleteConsider}
		on:finalize={handleDeleteFinalize}
	>
		{#each deletezoneobjects as card (card.id)}
			<div class="singlecard">
				<img src={card.uri} alt={card.cardname} />
			</div>
		{/each}
	</section>
	<section class="grid h-min self-center gap-2 grid-cols-2">
		<input type="text" bind:value={searchText} />
		<Button
			bgColorClass={'bg-green-200'}
			text={'Search'}
			on:click={async () => {
				const text = encodeURIComponent(searchText);
				const resp = await fetch('https://api.scryfall.com/cards/search?q=' + text, {
					method: 'GET',
					headers: { 'Content-Type': 'application/json' }
				})
					.then((r) => r.json())
					.then((j) => {
						searchResults = j.data ?? [];
					});
			}}
		/>
		<span>{searchResults.length} cards returned in search.</span>
		<Button
			bgColorClass={'bg-green-200'}
			text={'Add'}
			on:click={() => {
				const newList = searchResults.map((r) => {
					return { cardname: r.name, uri: '', id: 999, set: r.set, cn: r.collector_number };
				});
				newList.forEach((ne) => cardlist.push(ne));
				debounceUpdate();
			}}
		/>
	</section>
</div>

<style>
	.cardarea {
		display: grid;
		grid-template-columns: repeat(11, 1fr);
		grid-template-rows: repeat(11, 1fr);
		max-width: 600px;
		padding: 5px;
		overflow-y: scroll;
	}
	.singlecard {
		width: 50px;
		height: 69.85px;
	}
	#textarea {
		height: 100%;
		font-size: 0.8em;
	}
	#draggercomponent {
		width: fit-content;
		grid-template-columns: 600px auto;
		grid-template-rows: 480px auto;
	}
</style>
