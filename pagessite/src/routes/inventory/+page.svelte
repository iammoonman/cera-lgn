<script lang="ts">
	import type { Save, TTSCard } from 'src/types/tts';
	import VerticalList from './VerticalList.svelte';
	import { v4 as uuidv4 } from 'uuid';
	import { overrideItemIdKeyNameBeforeInitialisingDndZones } from 'svelte-dnd-action';
	overrideItemIdKeyNameBeforeInitialisingDndZones('GMNotes');

	let files_input: FileList;
	$: if (files_input)
		Promise.allSettled(
			Array.from(files_input).map((f) => {
				return f.text().then((tt) => {
					let save = JSON.parse(tt) as Save;
					let output: TTSCard[] = [];
					for (const f of save.ObjectStates) {
						if (f.Name === 'Bag') {
							for (const g of f.ContainedObjects) {
								if (g.Name === 'Deck') {
									output = [
										...output,
										...g.ContainedObjects.map((c) => {
											return { ...c, GMNotes: c.GMNotes ?? uuidv4() };
										})
									];
								}
								if (g.Name === 'Card') {
									output = [...output, { ...g, GMNotes: g.GMNotes ?? uuidv4() }];
								}
							}
						}
						if (f.Name === 'Deck') {
							output = [
								...output,
								...f.ContainedObjects.map((c) => {
									return { ...c, GMNotes: c.GMNotes ?? uuidv4() };
								})
							];
						}
						if (f.Name === 'Card') {
							output = [...output, { ...f, GMNotes: f.GMNotes ?? uuidv4() }];
						}
					}
					return output;
				});
			})
		).then((result) => {
			let newList: TTSCard[] = [];
			result.forEach((r) => {
				if (r.status === 'fulfilled') newList = [...newList, ...r.value];
			});
			biglist = newList;
		});
	$: outlist = [] as TTSCard[];
	$: biglist = [] as TTSCard[];
</script>

<div class="parent">
	<div class="sidebar">
		<input type="file" bind:files={files_input} accept="text/json" />
		<VerticalList items={outlist} />
	</div>
	<div class="p-2">
		<VerticalList items={biglist} />
	</div>
</div>

<style>
	.parent {
		display: grid;
		grid-template-columns: 20% 80%;
		height: 100vh;
		width: 100vw;
	}
	.parent > * {
		outline: 1px solid red;
	}
</style>
