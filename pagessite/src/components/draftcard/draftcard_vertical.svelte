<script lang="ts">
	import type { Draft } from 'src/types/events';
	import Tooltip, { Wrapper } from '@smui/tooltip';
	import Symbol from '../symbols/symbol.svelte';
	import type { PD } from 'src/types/discord';
	import { createEventDispatcher } from 'svelte';
	export let D: Draft;
	export let pn: Record<string, PD>;
	const dispatch = createEventDispatcher();
	const sortedscores = D.scores.sort((a, b) =>
		a.points > b.points ? -1 : b.points > a.points ? 1 : 0
	);
</script>

<div class="outercard grid grid-cols-1 p-2 relative justify-between">
    <div class="black-border"><div></div><div></div></div>
	<Wrapper>
		<div class="titlecard relative">
			<span class="text-title text-ellipsis overflow-x-hidden whitespace-nowrap">
				{D.title ?? ''}
			</span>
			<span class="text-date">{D.date.toLocaleDateString()}</span>
		</div>
		<Tooltip xPos="center" yPos="detected" class="bg-slate-400">
			{D.title}
			<hr />
			{D.description ?? 'No description provided.'}
		</Tooltip>
	</Wrapper>
	<div class="tagsymbolcontainer"><Symbol symbol_name={D.tag} symbol_size={230} /></div>
	<div class="top-three">
		<div class="player-avatar">
			<img src={pn[sortedscores[0].id].avatarURL} alt="player_pfp" />
			<span>{pn[sortedscores[0].id].username}</span>
		</div>
		<div class="player-avatar">
			<img src={pn[sortedscores[1].id].avatarURL} alt="player_pfp" />
			<span>{pn[sortedscores[1].id].username}</span>
		</div>
		<div class="player-avatar">
			<img src={pn[sortedscores[2].id].avatarURL} alt="player_pfp" />
			<span>{pn[sortedscores[2].id].username}</span>
		</div>
	</div>
    <table>
        <thead>
            <tr style="background-color: inherit;">
                <th>Player</th>
                <th class="text-right">PTS</th>
                <th class="text-right">OMP</th>
                <th class="text-right">GWP</th>
                <th class="text-right">OGP</th>
            </tr>
        </thead>
        <tbody>
            {#each sortedscores as s}
                <tr>
                    <td>{pn[s.id]?.username ?? 'BYE'}</td>
                    <td class="text-right">{s.points}</td>
                    <td class="text-right">{typeof s.ogp === 'string' ? s.ogp : s.ogp.toFixed(2)}</td>
                    <td class="text-right">{typeof s.gwp === 'string' ? s.gwp : s.gwp.toFixed(2)}</td>
                    <td class="text-right">{typeof s.omp === 'string' ? s.omp : s.omp.toFixed(2)}</td>
                </tr>
            {/each}
        </tbody>
    </table>
	<button class="absolute tap-icon" on:click={() => dispatch('untap', {})}>
		<span>Show Games</span>
		<Symbol symbol_name={'T'} symbol_size={20} />
	</button>
</div>

<style>
    .black-border {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 4.75% / 3.5%;
		box-shadow: inset 0 0 0 8px black, inset 0 -8px 0 8px black;
        z-index: 0;
		pointer-events: none;
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
		z-index: 4;
		appearance: none;
		display: flex;
		flex-direction: row;
		flex-wrap: nowrap;
		place-items: center;
		gap: 4px;
		font-size: 0.7rem;
	}
	.outercard {
		aspect-ratio: 336 / 468;
		width: 336px;
		height: 468px;
		border-radius: 4.75% / 3.5%;
		box-shadow: 0 1px 3px 0 black, 0 1px 2px -1px black;
		background-color: #176337;
		color: white;
		overflow-x: visible;
		overflow-y: clip;
        position: relative;
		grid-template-rows: 55px 190px 200px;
	}
	table {
		display: block;
		text-align: left;
		border-collapse: collapse;
		font-size: small;
		overflow: hidden;
		z-index: 3;
        position: relative;
        left: 0.5rem;
		scrollbar-gutter: stable;
        height: 200px;
        overflow: auto;
	}
	th,
	td {
		padding-inline: 0.6rem;
		max-width: 115px;
	}
	tr:nth-child(2n + 1) {
		background-color: #ffffff06;
	}
	thead {
		position: sticky;
		top: 0; /* Don't forget this, required for the stickiness */
		background-color: #176337;
		box-shadow: 0 2px 2px -2px white;
		z-index: 0;
	}
	tbody {
		white-space: nowrap;
	}
	.titlecard {
		display: grid;
		grid-template-areas: 'title' 'date';
		grid-template-columns: auto;
		grid-template-rows: auto auto;
		align-items: center;
		z-index: 1;
		box-shadow: 0 1px 3px -3px white;
        padding: 0.2rem;
		padding-top: 0;
	}
	.text-title {
		grid-area: title;
		font-size: 1.5rem;
	}
	.text-date {
		grid-area: date;
		text-align: left;
		font-size: 0.8rem;
		height: min-content;
	}
	.tagsymbolcontainer {
		filter: opacity(15%) invert();
		left: 50%;
		top: 28%;
		transform: translateX(-50%) translateY(-50%);
		position: absolute;
		z-index: 0;
	}
	.top-three {
		display: grid;
		align-items: center;
		grid-template-columns: 60% 40%;
		gap: 4px;
		z-index: 9;
	}
	.player-avatar {
		display: grid;
		grid-template-rows: auto min-content;
		place-items: center;
		transition-property: scale;
		transition-duration: 70ms;
		transition-timing-function: ease;
		z-index: 9;
	}
	.player-avatar > span {
		background-color: #17633799;
		border-radius: 15%;
	}
	.player-avatar > img {
		filter: drop-shadow(0px 2px 5px black);
		border-radius: 50%;
	}
	.top-three > .player-avatar:first-child {
		grid-area: 1 / 1 / 3;
	}
	.top-three > .player-avatar:first-child > span {
		white-space: nowrap;
		font-size: 1rem;
	}
	.top-three > .player-avatar:first-child > img {
		height: 120px;
		width: 120px;
		border-image: url();
	}
	.top-three > .player-avatar:nth-child(n + 2) > span {
		max-width: 100px;
		overflow-x: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
		font-size: 0.9rem;
	}
	.top-three > .player-avatar:nth-child(n + 3) > span {
		max-width: 100px;
		overflow-x: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
		font-size: 0.8rem;
	}
	.top-three > .player-avatar:nth-child(n + 2) > img {
		height: 80px;
		width: 80px;
	}
	.top-three > .player-avatar:nth-child(n + 2) {
		grid-area: 1 / 2;
	}
	.top-three > .player-avatar:nth-child(n + 3) > img {
		height: 50px;
		width: 50px;
	}
	.top-three > .player-avatar:nth-child(n + 3) {
		grid-area: 2 / 2;
	}
	.top-three > .player-avatar:hover {
		scale: 1.1;
	}
</style>
