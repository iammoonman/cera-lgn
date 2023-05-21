<script lang="ts">
	import type { Draft } from 'src/types/events';
	import { fly } from 'svelte/transition';
	import { Splide, SplideSlide } from '@splidejs/svelte-splide';
	import '@splidejs/svelte-splide/css';
	import Symbol from '../symbols/symbol.svelte';
	import type { PD } from 'src/types/discord';
	import Swoochgame from './swoochgame.svelte';
	export let D: Draft;
	export let pn: Record<string, PD>;
	export let setTap: () => void;
</script>

<div class="outercard grid grid-cols-1 relative">
	<div class="black-border" />
	<Splide options={{ width: '100%', perPage: 2 }}>
		{#each [...D.rounds] as [i, rnd]}
			<SplideSlide>
				<div class="leftside grid grid-cols-1 relative">
					{#if i % 2 == 1}
						<div class="tagsymbolcontainer">
							<Symbol symbol_name={D.tag} symbol_size={220} />
						</div>
					{/if}
					<div class="flex flex-row place-items-center justify-around controls-right h-10">
						<span class="w-fit text-xl">ROUND {rnd.title}</span>
					</div>
					<div
						class={`grid place-items-center games ${
							rnd['matches'].length > 2 ? 'grid-cols-2' : 'grid-cols-1'
						}`}
						style={`${rnd['matches'].length == 5 ? 'scale: 0.85; top: -20px; gap: 22px;' : ''}`}
					>
						{#each rnd['matches'] as m, i (m)}
							<div in:fly={{ duration: 200, y: 50, delay: 25 * i }} style={`width: min-content; ${rnd.matches.length == 2 ? 'scale: 1.25;' : ''}`}>
								<Swoochgame {m} {pn} />
							</div>
						{/each}
					</div>
				</div>
			</SplideSlide>
		{/each}
	</Splide>
	<button class="absolute tap-icon" on:click={setTap}>
		<span>Hide Games</span>
		<Symbol symbol_name={'T'} symbol_size={20} />
	</button>
</div>

<style>
	.black-border {
		position: absolute;
		width: 100%;
		height: 100%;
		border-radius: 3.5% / 4.75%;
		box-shadow: inset 0 0 0 8px black, inset 0 -8px 0 8px black;
		pointer-events: none;
		z-index: 1;
	}
	.black-border:before {
		background: radial-gradient(ellipse at 100% 0px, transparent 43%, black 44%);
		position: absolute;
		height: 45px;
		width: 20px;
		bottom: 12px;
		content: '';
	}
	.black-border:after {
		background: radial-gradient(ellipse at 0px 0px, transparent 43%, black 44%);
		position: absolute;
		height: 45px;
		width: 20px;
		bottom: 12px;
		right: 0px;
		content: '';
	}
	.tap-icon {
		bottom: 0px;
		right: 0px;
		z-index: 9;
		appearance: none;
		display: flex;
		flex-direction: row;
		flex-wrap: nowrap;
		place-items: center;
		gap: 4px;
		font-size: 0.7rem;
	}
	.outercard {
		aspect-ratio: 468 / 336;
		width: 468px;
		height: 336px;
		border-radius: 3.5% / 4.75%;
		box-shadow: 0 1px 3px 0 black, 0 1px 2px -1px black;
		background-color: #176337;
		color: white;
		overflow-x: visible;
		overflow-y: clip;
	}
	.leftside {
		grid-template-rows: 50px auto;
		padding: 7px;
		border-radius: 0 22px 32px 0;
		box-shadow: -2px 0px 4px -4px rgba(255, 255, 255, 0.5),
			2px 0px 4px -4px rgba(255, 255, 255, 0.5);
		height: 336px;
	}
	.games {
		padding-bottom: 12px;
		position: relative;
		z-index: 8;
	}
	.controls-right {
		box-shadow: 0px 2px 4px -4px white;
		z-index: 3;
	}
	.tagsymbolcontainer {
		filter: opacity(15%) invert();
		top: 50%;
		left: 50%;
		transform-origin: center;
		transform: translateX(-50%) translateY(-50%);
		position: absolute;
		z-index: 0;
	}
	.player-avatar {
		display: grid;
		grid-template-rows: auto min-content;
		place-items: center;
		transition-property: scale;
		transition-duration: 70ms;
		transition-timing-function: ease;
	}
</style>
