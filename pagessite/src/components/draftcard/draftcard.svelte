<script lang="ts">
	import type { Draft } from 'src/types/events';
	import type { PD } from 'src/types/discord';
	import DraftcardHorizontal from './draftcard_horizontal.svelte';
	import DraftcardVertical from './draftcard_vertical.svelte';
	import { cubicInOut } from 'svelte/easing';
	export let D: Draft;
	export let pn: Record<string, PD>;
	$: tapped = false;
	let setTap = () => (tapped = !tapped);
	function turnLeft(node: HTMLDivElement, { duration }: { duration: number }) {
		return {
			duration,
			css: (t: number) => {
				const eased = cubicInOut(t);
				return `
				transform: rotate(${eased * 90 - 90}deg);
				opacity: ${eased * 100}%;
				`;
			}
		};
	}
	function turnRight(node: HTMLDivElement, { duration }: { duration: number }) {
		return {
			duration,
			css: (t: number) => {
				const eased = cubicInOut(t);
				return `
				transform: rotate(${eased * -90 + 90}deg);
				opacity: ${eased * 100}%;
				`;
			}
		};
	}
</script>

<div class="fakecontainer">
	{#if tapped}
		<div in:turnRight={{ duration: 450 }} out:turnRight={{ duration: 450 }}>
			<DraftcardHorizontal {D} {pn} {setTap} />
		</div>
	{:else}
		<div in:turnLeft={{ duration: 450 }} out:turnLeft={{ duration: 450 }}>
			<DraftcardVertical {D} {pn} {setTap} />
		</div>
	{/if}
</div>

<style>
	.fakecontainer {
		display: grid;
		grid-template-areas: 'a';
		place-items: center;
	}
	.fakecontainer > div {
		grid-area: a;
	}
</style>
