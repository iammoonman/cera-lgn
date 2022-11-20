<script lang="ts">
	import { flip } from 'svelte/animate';
	import { dndzone } from 'svelte-dnd-action';
	import type { TTSCard } from 'src/types/tts';
	import Inventorycard from '../../components/inventorycard/inventorycard.svelte';
	export let items: TTSCard[];
	import { createEventDispatcher } from 'svelte';
	export const postChanges = createEventDispatcher();
	const flipDurationMs = 300;
	function handleDndConsider(e: any) {
		items = e.detail.items;
		// postChanges('postChanges', e);
	}
	function handleDndFinalize(e: any) {
		items = e.detail.items;
		postChanges('postChanges', { items: e.detail.items });
	}
</script>

<section
	use:dndzone={{ items, flipDurationMs }}
	on:consider={handleDndConsider}
	on:finalize={handleDndFinalize}
	class="flex flex-wrap gap-2"
>
	{#each items as item (item.GMNotes)}
		<div animate:flip={{ duration: flipDurationMs }}>
			<Inventorycard card={item} />
		</div>
	{/each}
</section>

<style>
	section {
		flex-grow: 1;
		min-height: 350px;
	}
	div {
		height: min-content;
	}
</style>
