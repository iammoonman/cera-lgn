<script lang="ts">
	import type { Draft } from 'src/types/events';
	import Tinygame from './tinygame.svelte';
	// import { PlayerList } from '../../types/playerstore';
	import { fly } from 'svelte/transition';
	import Tooltip, { Wrapper } from '@smui/tooltip';
	import AnglesRight from '../utilities/angles-right.svelte';
	import Symbol from '../symbols/symbol.svelte';
	import type { User } from 'discord.js';
	import type { PD } from 'src/types/discord';
	export let D: Draft;
	export let pn: Record<string, PD>;
	$: selectedRound = 0;
	$: roundHold = [...(D.rounds.get(selectedRound)?.matches ?? [])];
	$: round = D.rounds.get(selectedRound)?.title ?? `${selectedRound + 1}`;
	const sortedscores = D.scores.sort((a, b) =>
		a.points > b.points ? -1 : b.points > a.points ? 1 : 0
	);
</script>

<div class="outercard grid grid-cols-2">
	<div class="leftside grid p-2 relative">
		<Wrapper>
			<div class="titlecard relative">
				<span class="text-lg text-title text-ellipsis overflow-x-hidden whitespace-nowrap">
					{D.title ?? ''}
				</span>
				<span class="text-xs text-date">{D.date.toLocaleDateString()}</span>
			</div>
			<Tooltip xPos="center" yPos="detected" class="bg-slate-400">
				{D.description ?? 'No description provided.'}
			</Tooltip>
		</Wrapper>
		<div class="tagsymbolcontainer"><Symbol symbol_name={D.tag} symbol_size={170} /></div>
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
				<tr>
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
	</div>
	<div class="rightside grid grid-cols-1">
		<div class="flex flex-row place-items-center justify-between">
			<button
				on:click={() => {
					D.rounds.get(selectedRound - 1) ? (selectedRound = selectedRound - 1) : null;
				}}
				class={D.rounds.get(selectedRound - 1) ? 'visible' : 'invisible'}
			>
				<AnglesRight direction="left" fill="white" />
			</button>
			<span class="w-fit text-lg">ROUND {round}</span>
			<button
				on:click={() => {
					D.rounds.get(selectedRound + 1) ? (selectedRound = selectedRound + 1) : null;
				}}
				class={D.rounds.get(selectedRound + 1) ? 'visible' : 'invisible'}
			>
				<AnglesRight direction="right" fill="white" />
			</button>
		</div>
		<div
			class="flex flex-col items-center games"
			style={`${roundHold.length == 5 ? 'scale: 0.90; top: -15px' : ''}`}
		>
			{#each roundHold as m (m)}
				<div in:fly={{ duration: 200, y: 50 }}>
					<Tinygame {m} {pn} />
				</div>
			{/each}
		</div>
	</div>
</div>

<style>
	.outercard {
		aspect-ratio: 468 / 336;
		width: 468px;
		height: 336px;
		border-radius: 3.5% / 4.75%;
		box-shadow: 0 1px 3px 0 black, 0 1px 2px -1px black;
		background-color: #7e1515;
		color: white;
		overflow-x: visible;
		overflow-y: clip;
	}
	.leftside {
		grid-template-rows: 65px;
		box-shadow: 2px 0px 4px -4px black;
		max-height: 336px;
	}
	table {
		display: block;
		text-align: left;
		border-collapse: collapse;
		width: 107%;
		font-size: small;
		height: 130px;
		overflow: auto;
		background-color: #7e151588;
		z-index: 3;
	}
	th,
	td {
		padding: -0.25rem;
	}
	thead {
		position: sticky;
		top: 0; /* Don't forget this, required for the stickiness */
		background-color: #7e1515;
		box-shadow: 0 2px 2px -1px white;
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
	}
	.text-title {
		grid-area: title;
	}
	.text-date {
		grid-area: date;
		text-align: left;
	}
	.rightside {
		grid-template-rows: 50px auto;
		padding: 7px;
	}
	.games {
		padding-bottom: 12px;
		position: relative;
	}
	.tagsymbolcontainer {
		filter: opacity(15%) invert();
		left: 50%;
		top: 28%;
		transform: translateX(-50%) translateY(-50%);
		position: absolute;
		z-index: 2;
	}
	.top-three {
		display: grid;
		align-items: center;
		grid-template-columns: 60% 40%;
		gap: 4px;
		z-index: 3;
	}
	.player-avatar {
		display: grid;
		grid-template-rows: auto min-content;
		place-items: center;
	}
	.player-avatar > span {
		background-color: #7e151599;
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
		height: 80px;
		width: 80px;
		border-image: url()
	}
	.top-three > .player-avatar:nth-child(n + 2) > span {
		max-width: 70px;
		overflow-x: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
		font-size: 0rem;
	}
	.top-three > .player-avatar:nth-child(n + 3) > span {
		max-width: 70px;
		overflow-x: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
		font-size: 0rem;
	}
	.top-three > .player-avatar:nth-child(n + 2) > img {
		height: 50px;
		width: 50px;
	}
	.top-three > .player-avatar:nth-child(n + 2) {
		grid-area: 1 / 2;
	}
	.top-three > .player-avatar:nth-child(n + 3) > img {
		height: 40px;
		width: 40px;
	}
	.top-three > .player-avatar:nth-child(n + 3) {
		grid-area: 2 / 2;
	}
</style>
