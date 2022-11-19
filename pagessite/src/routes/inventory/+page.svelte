<script lang="ts">
	import Inventorycard from '../../components/inventorycard/inventorycard.svelte';
	import type { Save, TTSCard } from 'src/types/tts';

	let files_input: FileList;
	$: cardlist = files_input
		? Array.from(files_input).map((f) => {
				return f.text().then((tt) => {
					let save = JSON.parse(tt) as Save;
					let output: TTSCard[] = [];
					for (const f of save.ObjectStates) {
						if (f.Name === 'Bag') {
							for (const g of f.ContainedObjects) {
								if (g.Name === 'Deck') {
									output = [...output, ...g.ContainedObjects];
								}
								if (g.Name === 'Card') {
									output = [...output, g];
								}
							}
						}
						if (f.Name === 'Deck') {
							output = [...output, ...f.ContainedObjects];
						}
						if (f.Name === 'Card') {
							output = [...output, f];
						}
					}
					return output;
				});
		  })
		: [];
	$: outlist = [] as TTSCard[];
	$: biglist = [] as TTSCard[];
</script>

<div class="parent">
	<div class="sidebar">
		<input type="file" bind:files={files_input} accept="text/json" />
		<div class="sidebox">
			{#each outlist as c}
				<Inventorycard card={c} />
			{/each}
		</div>
	</div>
	<div class="flex flex-wrap gap-2">
		{#each cardlist as c}
			{#await c}
				<p>Waiting...</p>
			{:then result}
				{#if result !== undefined}
					{#each result as r}
						<Inventorycard card={r} />
					{/each}
				{:else}
					<p>Null</p>
				{/if}
			{/await}
		{/each}
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
