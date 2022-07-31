<script lang="ts">
	import Singlecard from './singlecard.svelte';

	let cardlist: { cardname: string; uri: string; id: number; set: string; cn: string }[] = [
		{
			set: '',
			cn: '',
			id: 1,
			cardname: 'Metallic Mimic',
			uri: 'https://c1.scryfall.com/file/scryfall-cards/small/front/1/a/1aa4eba9-9e91-4beb-9296-a18baa73a318.jpg?1576382339'
		},
		{
			set: '',
			cn: '',
			id: 2,
			cardname: 'Metallic Mimic',
			uri: 'https://c1.scryfall.com/file/scryfall-cards/small/front/1/a/1aa4eba9-9e91-4beb-9296-a18baa73a318.jpg?1576382339'
		}
	];
	import { dndzone } from 'svelte-dnd-action';
	function handleDndConsider(e: any) {
		cardlist = e.detail.items;
	}
	function handleDndFinalize(e: any) {
		cardlist = e.detail.items;
	}
</script>

<div>
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
		<input type="text" value={`${cardlist}`}/>
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
		width: max-content;
	}
</style>
