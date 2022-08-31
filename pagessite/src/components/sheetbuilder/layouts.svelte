<script lang="ts">
	import { V3Store } from './stores';
	// $V3Store;
	// Small card
	// For each slot, show how many cards are taken
    $: option = 0;
</script>

<div class="flex flex-row gap-1">
	{#each [...$V3Store.slots] as [k, v]}
		{#if v.options.length > 0}
			{#each [...v.options[option].struct] as [sk, sv]}
				{#each { length: sv } as _}
					<div class="card">&nbsp;</div>
				{/each}
			{/each}
		{/if}
	{/each}
</div>

<style>
	.card {
		aspect-ratio: 336 / 468;
		width: 33px;
		border-radius: 3.5% / 4.75%;
		box-shadow: 0 0 3px black;
		background-color: beige;
	}
</style>
