<script lang="ts">
	export const data = {};
	let CDs: (Draft | CardDisplayType)[] = [];
	export function load() {
		CDs = [
			{
				cn: '1',
				id: 0,
				p_id: '237059875073556481',
				set: 'ala',
				title: 'test',
				description: '',
				uri: 'https://c1.scryfall.com/file/scryfall-cards/large/front/7/7/774ec405-5127-4475-8c74-b8858bd84379.jpg?1562877904'
			},
			{
				cn: '1',
				id: 0,
				p_id: '237059875073556481',
				set: 'ala',
				title: 'test',
				description: '',
				uri: 'https://c1.scryfall.com/file/scryfall-cards/large/front/7/7/774ec405-5127-4475-8c74-b8858bd84379.jpg?1562877904'
			},
			{
				date: new Date(),
				id: 0,
				rounds: new Map([
					[
						0,
						{
							matches: [
								{
									p_ids: ['411627939478765568', '237059875073556481'],
									bye: false,
									drops: [],
									games: new Map([
										[0, '411627939478765568'],
										[1, '411627939478765568']
									])
								},
								{
									p_ids: ['320756550992134145', '317470784870285323'],
									bye: false,
									drops: [],
									games: new Map([
										[0, '320756550992134145'],
										[1, '320756550992134145']
									])
								},
								{
									p_ids: ['298561362034950154', '247076572295593984'],
									bye: false,
									drops: ['247076572295593984'],
									games: new Map([
										[0, '298561362034950154'],
										[1, '298561362034950154']
									])
								},
								{
									p_ids: ['250385022106730496', '265851480462852096'],
									bye: false,
									drops: ['250385022106730496'],
									games: new Map([
										[0, '265851480462852096'],
										[1, '265851480462852096']
									])
								}
							]
						}
					],
					[
						1,
						{
							matches: [
								{
									p_ids: ['320756550992134145', '265851480462852096'],
									bye: false,
									drops: ['320756550992134145', '265851480462852096'],
									games: new Map([
										[0, '320756550992134145'],
										[1, '320756550992134145']
									])
								},
								{
									p_ids: ['411627939478765568', '298561362034950154'],
									bye: false,
									drops: ['298561362034950154'],
									games: new Map([[0, '411627939478765568']])
								},
								{
									p_ids: ['237059875073556481', '317470784870285323'],
									bye: false,
									drops: [],
									games: new Map([
										[0, '237059875073556481'],
										[1, '317470784870285323'],
										[2, '237059875073556481']
									])
								}
							]
						}
					],
					[
						2,
						{
							matches: [
								{
									p_ids: ['411627939478765568', '317470784870285323'],
									bye: false,
									drops: [],
									games: new Map([[0, '411627939478765568']])
								},
								{
									p_ids: ['237059875073556481'],
									bye: true,
									drops: [],
									games: new Map()
								}
							]
						}
					]
				]),
				scores: [
					{ id: '411627939478765568', points: 9, gwp: 1.0, ogp: 0.4667, omp: 0.5 },
					{ id: '237059875073556481', points: 6, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
					{ id: '320756550992134145', points: 6, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
					{ id: '298561362034950154', points: 3, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
					{ id: '265851480462852096', points: 3, gwp: 0.5, ogp: 0.6667, omp: 0.6667 },
					{ id: '317470784870285323', points: 0, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
					{ id: '247076572295593984', points: 0, gwp: 0, ogp: 0.6667, omp: 0.5 },
					{ id: '250385022106730496', points: 0, gwp: 0, ogp: 0.5, omp: 0.5 }
				],
				tag: 'dps',
				title: 'TEST TITLE',
				description:
					'TEST DESCRIPTION lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum'
			}
		];
	}
	import type { CardDisplayType } from '../types/displaycard';
	import type { Draft } from '../types/events';
	import { PlayerList } from '../types/playerstore';

	import Layouts from '../components/sheetbuilder/layouts.svelte';

	import Sheetbuildercomponent from '../components/sheetbuilder/sheetbuildercomponent.svelte';
	import Carddisplay from '../components/cardcard/carddisplay.svelte';
	import Draftcard from '../components/draftcard/draftcard.svelte';
	// apply filters to array of objects
	$: PlayerName = '';
	$: TagSelect = '';
	$: Date1 = '2018-01-01';
	$: Date2 = '';
	$: DraftName = '';
	$: CardName = '';

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
