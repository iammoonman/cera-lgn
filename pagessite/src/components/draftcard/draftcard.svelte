<script lang="ts">
	import type { Draft } from 'src/types/events';
	import type { PD } from 'src/types/discord';
	import DraftcardHorizontal from './draftcard_horizontal.svelte';
	import DraftcardVertical from './draftcard_vertical.svelte';
	import { cubicInOut } from 'svelte/easing';
	import { tweened } from 'svelte/motion';
	export let D: Draft;
	export let pn: Record<string, PD>;
	const flip = tweened(0, { duration: 700, easing: cubicInOut });
</script>

<div class="fakecontainer">
	<div class="hori" style={`--ZHspin: ${$flip * 90}deg; --YHspin: ${180 + $flip * 180}deg;`}>
		<div style="transform: rotateZ(270deg);">
			<DraftcardHorizontal
				{D}
				{pn}
				on:untap={() =>
					flip.update((t) => {
						return t === 0 ? 1 : 0;
					})}
			/>
		</div>
	</div>
	<div class="vert" style={`--ZVspin: ${$flip * 90}deg; --YVspin: ${$flip * 180}deg;`}>
		<DraftcardVertical
			{D}
			{pn}
			on:untap={() =>
				flip.update((t) => {
					return t === 0 ? 1 : 0;
				})}
		/>
	</div>
</div>

<style>
	.fakecontainer {
		display: grid;
		grid-template-areas: 'a';
		place-items: center;
		perspective: 600px;
	}
	.fakecontainer > div {
		grid-area: a;
	}
	.hori {
		transform: rotateZ(var(--ZHspin)) rotateY(var(--YHspin));
		backface-visibility: hidden;
	}
	.vert {
		transform: rotateZ(var(--ZVspin)) rotateY(var(--YVspin));
		backface-visibility: hidden;
	}
</style>
