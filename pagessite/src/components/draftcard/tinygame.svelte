<script lang="ts">
	import type { Match } from 'src/types/events';
    import { PlayerList } from '../../types/playerstore';
	export let m: Match;
</script>

<div class="pill">
	<div class="innerpill">
		{#each m.p_ids as p}
			<div class="topguy">
                <span>{PlayerList.get(p) ?? 'Unknown'}</span>
                <span>{[...m.games].filter(([k, x]) => x === p).length}</span>
            </div>
		{/each}
	</div>
</div>

<style>
	.pill {
		border: none;
		border-radius: 15px;
		box-shadow: inset 0 0 0 3px black, inset 0 -3px 0 4px black;
		padding: 0.35rem 0.4rem 0.55rem 0.3rem;
		background-image: linear-gradient(70deg, #d6a53b5d, #d4aa576c, #c59c4263, #d4bc8c62),
			linear-gradient(45deg, #c99a3560, #d4bc8c6c, #c0973e75, #d4bc8c75, #d4bc8c60),
			linear-gradient(120deg, #c99e4360, #d4bc8c6c, #be9c5260, #d4bc8c75, #d4bc8c60),
			radial-gradient(ellipse at 0 0, #c99e433b, #d4bc8c3d, #be9c5244, #d4bc8c38, #d4bc8c46),
			linear-gradient(180deg, #dab36b, #c2a64d, #977d4f);
		margin-bottom: 1px;
	}
	.innerpill {
		margin-bottom: 0;
		margin-top: 0;
		padding: 0;
	}
	.topguy {
		display: flex;
		border-radius: 20px/50px;
		border-style: solid;
		border-color: #634f29;
		padding-left: 0.2rem;
		padding-right: 0.2rem;
		background-color: hsla(0, 0%, 100%, 0.4);
		box-shadow: inset 2px -2px rgba(65, 65, 65, 0.425), inset -2px 2px #ffffff8f;
		justify-content: space-between;
		max-height: 33px;
	}
</style>
