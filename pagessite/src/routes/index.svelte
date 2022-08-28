<script lang="ts">
	import Draftcard from '../components/draftcard/draftcard.svelte';
	import type { Draft } from 'src/types/events';
	import Carddisplay from '../components/cardcard/carddisplay.svelte';
	import Fancycardhover from '../components/cardcard/fancycardhover.svelte';
	const applyFilter = <T, X>(list: Array<T>, filter: (x: T) => boolean) => {
		return list.filter((x) => filter(x));
	};
	const filterList = [{ active: false, filter: (x: unknown) => false }];
	// filter filterList to get actives
	// apply filters to array of objects
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
	<div class="h-full mt-2 grid gap-4 booty">
		<Carddisplay />
		<Draftcard />
	</div>
</div>

<style>
	.grid-catch {
		grid-template-columns: 200px auto;
	}
	.booty {
		grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
		grid-auto-rows: auto;
	}
</style>
