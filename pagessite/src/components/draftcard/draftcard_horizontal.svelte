<script lang="ts">
	import type { Draft } from 'src/types/events';
	import { fly } from 'svelte/transition';
	import Tooltip, { Wrapper } from '@smui/tooltip';
	import AnglesRight from '../utilities/angles-right.svelte';
	import Symbol from '../symbols/symbol.svelte';
	import type { PD } from 'src/types/discord';
	import Swoochgame from './swoochgame.svelte';
	export let D: Draft;
	export let pn: Record<string, PD>;
	$: selectedRound = 0;
	$: roundHold = [...(D.rounds.get(selectedRound)?.matches ?? [])];
	$: round = D.rounds.get(selectedRound)?.title ?? `${selectedRound + 1}`;
	const sortedscores = D.scores.sort((a, b) =>
		a.points > b.points ? -1 : b.points > a.points ? 1 : 0
	);
</script>

<div class="outercard grid grid-cols-2 relative">
	<div class="black-border">
		<div />
		<div />
	</div>
	<div class="leftside grid py-2 pl-2 relative">
		<Wrapper>
			<div class="titlecard relative">
				<span class="text-title text-ellipsis overflow-x-hidden whitespace-nowrap pl-1">
					{D.title ?? ''}
				</span>
				<span class="text-date pl-1">{D.date.toLocaleDateString()}</span>
			</div>
			<Tooltip xPos="center" yPos="detected" class="bg-slate-400">
				{D.title}
				<hr />
				{D.description ?? 'No description provided.'}
			</Tooltip>
		</Wrapper>
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
	</div>
	<div class="rightside grid grid-cols-1 relative">
		<div class="tagsymbolcontainer"><Symbol symbol_name={D.tag} symbol_size={220} /></div>
		<div class="flex flex-row place-items-center justify-around controls-right h-10">
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
			class={`grid place-items-center games ${
				roundHold.length > 2 ? 'grid-cols-2' : 'grid-cols-1'
			}`}
			style={`${roundHold.length == 5 ? 'scale: 0.85; top: -20px; gap: 22px;' : ''}`}
		>
			{#each roundHold as m, i (m)}
				<div in:fly={{ duration: 200, y: 50, delay: 25 * i }} style="width: min-content;">
					<!-- <Tinygame {m} {pn} /> -->
					<Swoochgame {m} {pn} />
				</div>
			{/each}
		</div>
	</div>
</div>

<style>
	.black-border {
		position: absolute;
		width: 100%;
		height: 100%;
		border-radius: 3.5% / 4.75%;
		box-shadow: inset 0 0 0 8px black;
		z-index: 1;
	}
	.black-border:after {
		position: absolute;
		height: 15px;
		width: 460px;
		border-radius: 0 0 50% 50%;
		bottom: 0;
		left: 50%;
		transform: translateX(-50%);
		content: '';
		background-color: black;
	}
	.black-border > div:first-child {
		background: radial-gradient(ellipse at 100% 0px, transparent 43%, black 44%);
		position: absolute;
		height: 45px;
		width: 20px;
		bottom: 12px;
	}
	.black-border > div:last-child {
		background: radial-gradient(ellipse at 0px 0px, transparent 43%, black 44%);
		position: absolute;
		height: 45px;
		width: 20px;
		bottom: 12px;
		right: 0px;
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
		grid-template-rows: 40px 142px 130px;
		box-shadow: 2px 0px 4px -4px white;
		max-height: 336px;
	}
	table {
		display: block;
		text-align: left;
		border-collapse: collapse;
		width: 102%;
		font-size: small;
		height: 130px;
		overflow: auto;
		background-color: #17633788;
		z-index: 3;
		scrollbar-gutter: stable;
		left: 4px;
		position: relative;
	}
	th,
	td {
		padding: -0.25rem;
	}
	td {
		text-align: center;
	}
	td:first-child {
		text-align: left;
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
		height: 40px;
		box-shadow: 0 1px 3px -3px white;
	}
	.text-title {
		grid-area: title;
		font-size: 1.125rem;
	}
	.text-date {
		grid-area: date;
		text-align: left;
		font-size: 0.7rem;
	}
	.rightside {
		grid-template-rows: 50px auto;
		padding: 7px;
		background-color: #145a32;
		border-radius: 0 22px 32px 0;
		box-shadow: inset 0 0 12px -4px black;
		height: 336px;
	}
	.rightside > div > button {
		padding-inline: 0.2rem;
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
	.top-three {
		display: grid;
		align-items: center;
		grid-template-columns: 60% 40%;
		gap: 4px;
		z-index: 7;
	}
	.player-avatar {
		display: grid;
		grid-template-rows: auto min-content;
		place-items: center;
		transition-property: scale;
		transition-duration: 70ms;
		transition-timing-function: ease;
	}
	.player-avatar > span {
		background-color: #17633799;
		border-radius: 15%;
	}
	.player-avatar > img {
		/* filter: drop-shadow(0px 2px 3px goldenrod); */
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
		filter: drop-shadow(0px 2px 4px black);
		height: 95px;
		width: 95px;
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
		filter: drop-shadow(0px 2px 3px black);
		height: 70px;
		width: 70px;
	}
	.top-three > .player-avatar:nth-child(n + 2) {
		grid-area: 1 / 2;
	}
	.top-three > .player-avatar:nth-child(n + 3) > img {
		filter: drop-shadow(0px 2px 3px black);
		height: 50px;
		width: 50px;
	}
	.top-three > .player-avatar:nth-child(n + 3) {
		grid-area: 2 / 2;
	}
	.top-three > .player-avatar:hover {
		scale: 1.05;
	}
</style>
