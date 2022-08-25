<script lang="ts">
	import type { Match } from 'src/types/events';
    import { PlayerList } from '../../types/playerstore';
	export let m: Match;
</script>

<div class="pill">
	<div class="innerpill">
		{#each m.p_ids as p}
			<div class="topguy">
                <span class="overflow-x-hidden text-ellipsis whitespace-nowrap">{PlayerList.get(p) ?? 'Unknown'}</span>
                <span>{[...m.games].filter(([k, x]) => x === p).length}</span>
            </div>
		{/each}
	</div>
</div>

<style>
	.pill {
		border: none;
		border-radius: 15px;
		box-shadow: inset 0 0 0 2px black, inset 0 -2px 0 3px black;
		padding: 5px 6px 7px 5px;
		background-image: linear-gradient(70deg, #d6a53b5d, #d4aa576c, #c59c4263, #d4bc8c62),
			linear-gradient(45deg, #c99a3560, #d4bc8c6c, #c0973e75, #d4bc8c75, #d4bc8c60),
			linear-gradient(120deg, #c99e4360, #d4bc8c6c, #be9c5260, #d4bc8c75, #d4bc8c60),
			radial-gradient(ellipse at 0 0, #c99e433b, #d4bc8c3d, #be9c5244, #d4bc8c38, #d4bc8c46),
			linear-gradient(180deg, #dab36b, #c2a64d, #977d4f);
		margin-bottom: 1px;
		width: 203px;
		transition: transform 0.1s ease-in-out;
		cursor: default;
	}
	.pill:hover {
		position: relative;
		z-index: 2;
		transform: scale(1.2);
		filter: drop-shadow(0 0 0.75rem black);;
	}
	.innerpill {
		margin-bottom: 0;
		margin-top: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 2px;
	}
	.topguy {
		display: flex;
		flex-direction: row;
		flex-wrap: nowrap;
		align-items: center;
		justify-content: space-between;
		border-radius: 20px/50px;
		border-style: solid;
		border-color: #634f29;
		padding-left: 7px;
		padding-right: 7px;
		background-color: hsla(0, 0%, 100%, 0.4);
		box-shadow: inset 2px -2px rgba(65, 65, 65, 0.425), inset -2px 2px #ffffff8f;
		max-height: 33px;
	}
	span {
		line-height: 100%;
		padding-top: 2px;
		padding-bottom: 5px;
	}
</style>
