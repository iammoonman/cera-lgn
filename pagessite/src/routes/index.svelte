<script lang="ts">
	import type { Draft } from 'src/types/events';

	import Carddisplay from '../components/carddisplay.svelte';
	const applyFilter = <T, X>(list: Array<T>, filter: (x: T) => boolean) => {
		return list.filter((x) => filter(x));
	};
	const filterList = [{ active: false, filter: (x: unknown) => false }];
	// filter filterList to get actives
	// apply filters to array of objects
	const test: Draft = {
		date: new Date(),
		id: 0,
		rounds: [
			{ matches: [{ bye: true, drops: [], games: new Map(), p_ids: [0] }], r_id: 0, title: 'test' }
		],
		scores: [{ gwp: 0, id: 0, ogp: 0, omp: 0, points: 0 }],
		tag: '',
		title: 'test',
		description: 'test'
	};
</script>

<div
	class="w-full h-min p-2 z-10 relative flex flex-row justify-between shadow-lg shadow-green-700/40 bg-green-200"
>
	<span>The Rat Zone</span>
	<span>Hamburgler</span>
</div>
<div class="grid grid-catch gap-4">
	<div class="h-full shadow-lg shadow-blue-400 bg-blue-200">
		<div>SIDEBAR HEADER</div>
		<div class="h-full flex flex-col">SIDEBAR ROWS</div>
	</div>
	<div class="h-full mt-2">
		<Carddisplay />
	</div>
</div>

<style>
	.grid-catch {
		grid-template-columns: 1fr 5fr;
	}
</style>
