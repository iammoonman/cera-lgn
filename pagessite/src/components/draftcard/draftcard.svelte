<script lang="ts">
	import type { Draft } from 'src/types/events';
	import type { PD } from 'src/types/discord';
	import DraftcardHorizontal from './draftcard_horizontal.svelte';
	import DraftcardVertical from './draftcard_vertical.svelte';
	export let D: Draft;
	export let pn: Record<string, PD>;
	export let tapped = false;
</script>

{#if tapped}
    <DraftcardHorizontal {D} {pn} />
{:else}
    <DraftcardVertical {D} {pn} />
{/if}