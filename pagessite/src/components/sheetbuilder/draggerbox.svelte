<script lang="ts">
	import Singlecard from './singlecard.svelte';

	export let cardlist: { cardname: string; uri: string; id: number; set: string; cn: string }[];
	import { dndzone } from 'svelte-dnd-action';
	function handleDndConsider(e: any) {
		cardlist = e.detail.items;
	}
	function handleDndFinalize(e: any) {
		cardlist = e.detail.items;
	}
</script>

<div class="m-10">
	<section
		id="cardarea"
		use:dndzone={{ items: cardlist, flipDurationMs: 50 }}
		on:consider={handleDndConsider}
		on:finalize={handleDndFinalize}
	>
		{#each cardlist as card (card.id)}
			<Singlecard cardName={card.cardname} uri={card.uri} />
		{/each}
	</section>
	<section id="textarea">
		<input type="text" value={`[${cardlist.map((e) => `["${e.cn}", "${e.set}"]`)}]`} />
	</section>
</div>

<style>
	#cardarea {
		display: grid;
		grid-template-columns: repeat(11, 1fr);
		grid-template-rows: repeat(11, 1fr);
		width: 874px;
		gap: 2px;
		border: 1px solid blue;
		padding: 5px;
		height: 300px;
		overflow-y: scroll;
	}
	input {
		width: 874px;
	}
</style>
