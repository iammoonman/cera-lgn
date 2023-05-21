<script lang="ts">
	import type { TTSCard } from 'src/types/tts';

	export let card: TTSCard;
	export let highlighted = false;
</script>

<div class="grid" style={`--visible: ${highlighted ? '100%' : '30%'}`}>
	{#each [...Object.entries(card.CustomDeck)] as c}
		<img src={c[1].FaceURL} alt={card.Nickname.split('\n')[0]} />
	{/each}
	{#each card.AttachedDecals ?? [] as d}
		<img src={d.CustomDecal.ImageURL} alt={'Decal'} />
	{/each}
</div>

<style>
	.grid {
		grid-template-areas: 'a';
		filter: brightness(var(--visible));
	}
	.grid > * {
		grid-area: a;
	}
	img {
		max-height: 170px;
	}
</style>
