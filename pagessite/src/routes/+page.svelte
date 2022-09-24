<script lang="ts">
	import fs from 'fs';
	export let data: { cds: (Draft | CardDisplayType)[] };
	let CDs = data.cds;
	import type { CardDisplayType } from '../types/displaycard';
	import type { Draft } from '../types/events';
	import { PlayerList } from '../types/playerstore';

	import Layouts from '../components/sheetbuilder/layouts.svelte';

	import Sheetbuildercomponent from '../components/sheetbuilder/sheetbuildercomponent.svelte';
	import Carddisplay from '../components/cardcard/carddisplay.svelte';
	import Draftcard from '../components/draftcard/draftcard.svelte';
	import { error, json } from '@sveltejs/kit';
	// apply filters to array of objects
	$: PlayerName = '';
	$: TagSelect = '';
	$: Date1 = '2018-01-01';
	$: Date2 = '';
	$: DraftName = '';
	$: CardName = '';
	$: DescriptionSearch = '';

	$: filteredDC = [] as typeof CDs;
	$: {
		// @ts-ignore
		filteredDC = CDs.filter((x) => {
			if ('date' in x) {
				if (x.date > new Date(Date2)) {
					return false;
				}
				if (x.date < new Date(Date1)) {
					return false;
				}
				if (x.title.toLowerCase().search(DraftName.toLowerCase()) < 0) {
					return false;
				}
				if (x.tag !== '' && TagSelect === 'anti') {
					return false;
				}
				if (TagSelect.length > 0 && TagSelect !== 'anti' && x.tag !== TagSelect) {
					return false;
				}
				if (x.description?.toLowerCase().search(DescriptionSearch.toLowerCase()) ?? 1 < 0) {
					return false;
				}
				if (PlayerName !== '') {
					let n = false;
					x.scores.forEach((y) => {
						if (PlayerList.get(y.id)?.toLowerCase().search(PlayerName.toLowerCase())) {
							n = true;
						}
					});
					return n;
				}
				return true;
			}
			if ('p_id' in x) {
				if (PlayerName !== '') {
					let n = false;
					[...PlayerList].forEach(([k, v]) => {
						if (v.toLowerCase().search(PlayerName.toLowerCase()) > -1) {
							n = true;
						}
					});
					return n;
				}
				if (x.title.toLowerCase().search(CardName.toLowerCase()) < 0) {
					return false;
				}
				return true;
			}
		});
	}
</script>

<div
	class="w-full h-min p-2 z-10 flex flex-row justify-between shadow-lg shadow-green-700/40 bg-green-200 sticky top-0"
>
	<span>The Rat Zone</span>
	<span>&nbsp;</span>
</div>
<div class="grid grid-catch gap-4">
	<div class="shadow-lg shadow-blue-400 bg-blue-200 sticky top-10 h-min">
		<div class="flex flex-col sidefilters p-3 gap-2">
			<div class="flex flex-row w-full justify-between">
				<label for="ps">Player Search</label>
				<input type="text" name="ps" bind:value={PlayerName} />
			</div>
			<div class="flex flex-row w-full justify-between">
				<label for="tag">Tag</label>
				<select name="tag" bind:value={TagSelect}>
					<option value="" />
					<option value="ptm">Prime Time with Moon</option>
					<option value="dps">Draft Progression Series</option>
					<option value="anti">No Tag</option>
				</select>
			</div>
			<div class="flex flex-row w-full justify-between">
				<label for="dt1">Earliest Date</label>
				<input type="date" name="dt1" bind:value={Date1} />
			</div>
			<div class="flex flex-row w-full justify-between">
				<label for="dt2">Latest Date</label>
				<input type="date" name="dt2" bind:value={Date2} />
			</div>
			<div class="flex flex-row w-full justify-between">
				<label for="dts">Draft Title</label>
				<input type="text" name="dts" bind:value={DraftName} />
			</div>
			<div class="flex flex-row w-full justify-between">
				<label for="dds">Draft Description</label>
				<input type="text" name="dds" bind:value={DescriptionSearch} />
			</div>
			<div class="flex flex-row w-full justify-between">
				<label for="dts">Card Title</label>
				<input type="text" name="dts" bind:value={CardName} />
			</div>
		</div>
	</div>
	<!-- <Sheetbuildercomponent /> -->
	<div class="h-full mt-2 grid gap-4 booty">
		{#each filteredDC as c}
			{#if 'uri' in c}
				<Carddisplay C={c} />
			{/if}
			{#if 'date' in c}
				<Draftcard D={c} />
			{/if}
		{/each}
	</div>
</div>

<style>
	.grid-catch {
		grid-template-columns: 400px auto;
	}
	.booty {
		grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
		grid-auto-rows: auto;
	}
</style>
