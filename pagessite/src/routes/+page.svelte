<script lang="ts">
	export let data: {
		cds: (Draft | CardDisplayType)[];
		users: Record<
			string,
			{
				id: string;
				bot: boolean;
				system: boolean;
				flags: number;
				username: string;
				discriminator: string;
				avatar: string;
				banner: null;
				accentColor: null;
				createdTimestamp: number;
				defaultAvatarURL: string;
				hexAccentColor: null;
				tag: string;
				avatarURL: string;
				displayAvatarURL: string;
				bannerURL: null;
			}
		>;
	};
	let { cds, users } = data;
	// console.log('on page', users, cds)
	import type { CardDisplayType } from '../types/displaycard';
	import type { Draft } from '../types/events';
	import Carddisplay from '../components/cardcard/carddisplay.svelte';
	import Draftcard from '../components/draftcard/draftcard.svelte';
	// apply filters to array of objects
	$: PlayerName = '';
	$: TagSelect = '';
	$: Date1 = '2018-01-01';
	$: Date2 = '';
	$: DraftName = '';
	$: CardName = '';
	$: DescriptionSearch = '';

	$: filteredDC = [] as (Draft | CardDisplayType)[];
	$: {
		// @ts-ignore
		filteredDC = cds.filter((x) => {
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
						if (users[y.id] !== undefined) {
							if (users[y.id]!.username.toLowerCase().search(PlayerName.toLowerCase()) > -1) {
								n = true;
							}
						}
					});
					return n;
				}
				return true;
			}
			if ('p_id' in x) {
				if (PlayerName !== '') {
					let n = false;
					Object.entries(users).forEach(([k, v]) => {
						if (v.username.toLowerCase().search(PlayerName.toLowerCase()) > -1) {
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
	class="topnav w-full h-min p-2 z-10 flex flex-row justify-between shadow-lg shadow-green-700/40 sticky top-0 text-xl"
>
	<span>The Rat Zone</span>
	<span>&nbsp;</span>
</div>
<div class="grid grid-catch gap-4">
	<div class="sticky top-12 h-min rounded-lg filterblock">
		<div class="flex flex-col sidefilters p-3 gap-2">
			<div class="text-xl text-center">Filter Controls</div>
			<div class="flex flex-row w-full justify-between">
				<label for="ps">Player Search</label>
				<input type="text" name="ps" bind:value={PlayerName} />
			</div>
			<div class="flex flex-row w-full justify-between">
				<label for="tag">Tag</label>
				<select name="tag" bind:value={TagSelect} style="width: 201px;">
					<option value="" />
					<option value="ptm">Prime Time with Moon</option>
					<option value="dps">Draft Progression Series</option>
					<option value="anti">No Tag</option>
				</select>
			</div>
			<div class="flex flex-row w-full justify-between">
				<label for="dt1">Earliest Date</label>
				<input type="date" name="dt1" bind:value={Date1} style="width: 201px;" />
			</div>
			<div class="flex flex-row w-full justify-between">
				<label for="dt2">Latest Date</label>
				<input type="date" name="dt2" bind:value={Date2} style="width: 201px;" />
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
	<div class="h-full mt-2 grid gap-4 booty place-items-center">
		{#each filteredDC as c}
			{#if 'uri' in c}
				<Carddisplay C={c} pn={users} />
			{/if}
			{#if 'date' in c}
				<Draftcard D={c} pn={users} tapped={true}/>
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
	.topnav {
		background-color: #21633f;
		color: white;
	}
	.filterblock {
		background-color: #3f3663;
		color: white;
		box-shadow: 0 1px 3px 0 black, 0 1px 2px -1px black;
	}
	input {
		background-color: black;
		border-radius: 4px;
	}
	select,
	option {
		background-color: black;
		border-radius: 4px;
	}
</style>
