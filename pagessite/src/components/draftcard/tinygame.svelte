<script lang="ts">
	import type { Match } from 'src/types/events';
	import { PlayerList } from '../../types/playerstore';
	export let m: Match;
</script>

<div class="pill">
	<div class="innerpill">
		{#if m.p_ids.length == 1}
			<span class="overflow-x-hidden text-ellipsis whitespace-nowrap text-center">BYE</span>
		{/if}
		{#each m.p_ids as p}
			<div class="topguy">
				<span class="overflow-x-hidden text-ellipsis whitespace-nowrap"
					>{PlayerList.get(p) ?? 'Unknown'}</span
				>
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
		/* background-color: white */
		background: linear-gradient(150deg, #ffed9e99 0%, #c69800 100%);
		padding: 5px 6px 7px 5px;
		margin-bottom: 1px;
		width: 203px;
		transition: transform 0.1s ease-in-out;
		cursor: default;
		color: black;
	}
	.pill:hover {
		position: relative;
		transform: scale(1.2);
		filter: drop-shadow(0 0 0.1rem black);
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
