<script lang="ts">
	import type { Draft } from 'src/types/events';
	import Tinygame from './tinygame.svelte';
	import { PlayerList } from '../../types/playerstore';
	import { fly } from 'svelte/transition';
	import Tooltip, { Wrapper } from '@smui/tooltip';
	import AnglesRight from '../utilities/angles-right.svelte';
	import Symbol from '../symbols/symbol.svelte';
	export let D: Draft;
	// {
	// 	date: new Date(),
	// 	id: 0,
	// 	rounds: new Map([
	// 		[
	// 			0,
	// 			{
	// 				matches: [
	// 					{
	// 						p_ids: ['411627939478765568', '237059875073556481'],
	// 						bye: false,
	// 						drops: [],
	// 						games: new Map([
	// 							[0, '411627939478765568'],
	// 							[1, '411627939478765568']
	// 						])
	// 					},
	// 					{
	// 						p_ids: ['320756550992134145', '317470784870285323'],
	// 						bye: false,
	// 						drops: [],
	// 						games: new Map([
	// 							[0, '320756550992134145'],
	// 							[1, '320756550992134145']
	// 						])
	// 					},
	// 					{
	// 						p_ids: ['298561362034950154', '247076572295593984'],
	// 						bye: false,
	// 						drops: ['247076572295593984'],
	// 						games: new Map([
	// 							[0, '298561362034950154'],
	// 							[1, '298561362034950154']
	// 						])
	// 					},
	// 					{
	// 						p_ids: ['250385022106730496', '265851480462852096'],
	// 						bye: false,
	// 						drops: ['250385022106730496'],
	// 						games: new Map([
	// 							[0, '265851480462852096'],
	// 							[1, '265851480462852096']
	// 						])
	// 					}
	// 				]
	// 			}
	// 		],
	// 		[
	// 			1,
	// 			{
	// 				matches: [
	// 					{
	// 						p_ids: ['320756550992134145', '265851480462852096'],
	// 						bye: false,
	// 						drops: ['320756550992134145', '265851480462852096'],
	// 						games: new Map([
	// 							[0, '320756550992134145'],
	// 							[1, '320756550992134145']
	// 						])
	// 					},
	// 					{
	// 						p_ids: ['411627939478765568', '298561362034950154'],
	// 						bye: false,
	// 						drops: ['298561362034950154'],
	// 						games: new Map([[0, '411627939478765568']])
	// 					},
	// 					{
	// 						p_ids: ['237059875073556481', '317470784870285323'],
	// 						bye: false,
	// 						drops: [],
	// 						games: new Map([
	// 							[0, '237059875073556481'],
	// 							[1, '317470784870285323'],
	// 							[2, '237059875073556481']
	// 						])
	// 					}
	// 				]
	// 			}
	// 		],
	// 		[
	// 			2,
	// 			{
	// 				matches: [
	// 					{
	// 						p_ids: ['411627939478765568', '317470784870285323'],
	// 						bye: false,
	// 						drops: [],
	// 						games: new Map([[0, '411627939478765568']])
	// 					},
	// 					{
	// 						p_ids: ['237059875073556481'],
	// 						bye: true,
	// 						drops: [],
	// 						games: new Map([])
	// 					}
	// 				]
	// 			}
	// 		]
	// 	]),
	// 	scores: [
	// 		{ id: '411627939478765568', points: 9, gwp: 1.0, ogp: 0.4667, omp: 0.5 },
	// 		{ id: '237059875073556481', points: 6, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
	// 		{ id: '320756550992134145', points: 6, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
	// 		{ id: '298561362034950154', points: 3, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
	// 		{ id: '265851480462852096', points: 3, gwp: 0.5, ogp: 0.6667, omp: 0.6667 },
	// 		{ id: '317470784870285323', points: 0, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
	// 		{ id: '247076572295593984', points: 0, gwp: 0, ogp: 0.6667, omp: 0.5 },
	// 		{ id: '250385022106730496', points: 0, gwp: 0, ogp: 0.5, omp: 0.5 }
	// 	],
	// 	tag: 'dps',
	// 	title: 'TEST TITLE',
	// 	description:
	// 		'TEST DESCRIPTION lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum'
	// };
	$: selectedRound = 0;
	$: roundHold = [...(D.rounds.get(selectedRound)?.matches ?? [])];
	$: round = D.rounds.get(selectedRound)?.title ?? `${selectedRound + 1}`;
</script>

<div class="outercard grid grid-cols-2">
	<div class="leftside grid p-2">
		<Wrapper>
			<div class="titlecard relative">
				<div class="tagsymbolcontainer"><Symbol symbol_name={D.tag} symbol_size={75} /></div>
				<span class="text-lg text-title text-ellipsis overflow-x-hidden whitespace-nowrap">
					{D.title ?? ''}
				</span>
				<span class="text-xs text-date">{D.date.toLocaleDateString()}</span>
			</div>
			<Tooltip xPos="center" yPos="detected" class="bg-slate-400">
				{D.description ?? 'No description provided.'}
			</Tooltip>
		</Wrapper>
		<div class="mytable overflow-y-hidden">
			<table class="table-auto">
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
					{#each D.scores.sort( (a, b) => (a.points > b.points ? -1 : b.points > a.points ? 1 : 0) ) as s}
						<tr>
							<td>{PlayerList.get(s.id) ?? 'Unknown'}</td>
							<td class="text-right">{s.points}</td>
							<td class="text-right">{typeof s.ogp === 'string' ? s.ogp : s.ogp.toFixed(2)}</td>
							<td class="text-right">{typeof s.gwp === 'string' ? s.gwp : s.gwp.toFixed(2)}</td>
							<td class="text-right">{typeof s.omp === 'string' ? s.omp : s.omp.toFixed(2)}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
	<div class="rightside grid grid-cols-1">
		<div class="flex flex-row place-items-center justify-between">
			<button
				on:click={() => {
					D.rounds.get(selectedRound - 1) ? (selectedRound = selectedRound - 1) : null;
				}}
				class={D.rounds.get(selectedRound - 1) ? 'visible' : 'invisible'}
			>
				<AnglesRight direction="left" />
			</button>
			<span class="w-fit text-lg">ROUND {round}</span>
			<button
				on:click={() => {
					D.rounds.get(selectedRound + 1) ? (selectedRound = selectedRound + 1) : null;
				}}
				class={D.rounds.get(selectedRound + 1) ? 'visible' : 'invisible'}
			>
				<AnglesRight direction="right" />
			</button>
		</div>
		<div
			class="flex flex-col items-center games"
			style={`${roundHold.length == 5 ? 'scale: 0.90; top: -15px' : ''}`}
		>
			{#each roundHold as m (m)}
				<div in:fly={{ duration: 200, y: 50 }}>
					<Tinygame {m} />
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
		text-align: left;
		position: relative;
		border-collapse: collapse;
		width: 100%;
	}
	th,
	td {
		padding: -0.25rem;
	}
	th {
		background: inherit;
		position: sticky;
		top: 0; /* Don't forget this, required for the stickiness */
		box-shadow: 0 2px 2px -1px white;
	}
	.mytable {
		font-size: small;
		overflow-y: hidden;
		display: grid;
		justify-items: center;
		align-items: start;
	}
	.titlecard {
		display: grid;
		grid-template-areas: 'title' 'date';
		grid-template-columns: auto;
		align-items: center;
	}
	/* .text-hack {
		grid-area: description;
		text-overflow: ellipsis;
		overflow: hidden;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
	} */
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
		filter: opacity(30%) invert();
		left: 50%;
		top: 75%;
		transform: translateX(-50%) translateY(-50%);
		position: absolute;
	}
</style>
