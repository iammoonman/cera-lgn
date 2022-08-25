<script lang="ts">
	import type { Draft } from 'src/types/events';
	import Tinygame from './tinygame.svelte';
	import { PlayerList } from '../../types/playerstore';
	const D: Draft = {
		date: new Date(),
		id: 0,
		rounds: new Map([
			[
				0,
				{
					title: 'TEST',
					matches: [
						{
							p_ids: ['411627939478765568', '237059875073556481'],
							bye: false,
							drops: [],
							games: new Map([
								[0, '411627939478765568'],
								[1, '411627939478765568']
							])
						},
						{
							p_ids: ['320756550992134145', '317470784870285323'],
							bye: false,
							drops: [],
							games: new Map([
								[0, '320756550992134145'],
								[1, '320756550992134145']
							])
						},
						{
							p_ids: ['298561362034950154', '247076572295593984'],
							bye: false,
							drops: ['247076572295593984'],
							games: new Map([
								[0, '298561362034950154'],
								[1, '298561362034950154']
							])
						},
						{
							p_ids: ['250385022106730496', '265851480462852096'],
							bye: false,
							drops: ['250385022106730496'],
							games: new Map([
								[0, '265851480462852096'],
								[1, '265851480462852096']
							])
						}
					]
				}
			],
			[
				1,
				{
					title: 'TEST',
					matches: [
						{
							p_ids: ['320756550992134145', '265851480462852096'],
							bye: false,
							drops: ['320756550992134145', '265851480462852096'],
							games: new Map([
								[0, '320756550992134145'],
								[1, '320756550992134145']
							])
						},
						{
							p_ids: ['411627939478765568', '298561362034950154'],
							bye: false,
							drops: ['298561362034950154'],
							games: new Map([[0, '411627939478765568']])
						},
						{
							p_ids: ['237059875073556481', '317470784870285323'],
							bye: false,
							drops: [],
							games: new Map([
								[0, '237059875073556481'],
								[1, '317470784870285323'],
								[2, '237059875073556481']
							])
						}
					]
				}
			],
			[
				2,
				{
					title: 'TEST',
					matches: [
						{
							p_ids: ['411627939478765568', '317470784870285323'],
							bye: false,
							drops: [],
							games: new Map([[0, '411627939478765568']])
						},
						{
							p_ids: ['237059875073556481'],
							bye: true,
							drops: [],
							games: new Map([])
						}
					]
				}
			]
		]),
		scores: [
			{ id: '411627939478765568', points: 9, gwp: 1.0, ogp: 0.4667, omp: 0.5 },
			{ id: '237059875073556481', points: 6, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
			{ id: '320756550992134145', points: 6, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
			{ id: '298561362034950154', points: 3, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
			{ id: '265851480462852096', points: 3, gwp: 0.5, ogp: 0.6667, omp: 0.6667 },
			{ id: '317470784870285323', points: 0, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
			{ id: '247076572295593984', points: 0, gwp: 0, ogp: 0.6667, omp: 0.5 },
			{ id: '250385022106730496', points: 0, gwp: 0, ogp: 0.5, omp: 0.5 }
		],
		tag: 'dps',
		title: 'TEST TITLE',
		description: 'TEST DESCRIPTION'
	};
	$: selectedRound = 0;
	let roundHold = D.rounds.get(0)?.matches ?? [];
	let round = D.rounds.get(selectedRound)?.title ?? "0";
</script>

<div class="outercard grid grid-cols-2">
	<div class="leftside grid p-2">
		<div class="titlecard">
			<span class="text-lg text-title">{D.title}</span>
			<span class="text-xs text-date">{D.date.toLocaleDateString()}</span>
			<span class="text-xs text-hack">{D.description}</span>
		</div>
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
					{#each D.scores as s}
						<tr>
							<td>{PlayerList.get(s.id) ?? 'Unknown'}</td>
							<td class="text-right">{s.points}</td>
							<td class="text-right">{s.ogp.toFixed(2)}</td>
							<td class="text-right">{s.gwp.toFixed(2)}</td>
							<td class="text-right">{s.omp.toFixed(2)}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
	<div class="rightside grid grid-cols-1">
		<div class="grid place-items-center">
			<span class="w-fit text-lg">ROUND {round}</span>
		</div>
		<div class="">
			{#each roundHold as m}
				<Tinygame {m} />
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
		box-shadow: 0 0 15px black;
	}
	.leftside {
		grid-template-rows: 65px auto;
		box-shadow: 2px 0px 4px -4px black;
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
		background: white;
		position: sticky;
		top: 0; /* Don't forget this, required for the stickiness */
		box-shadow: 0 2px 2px -1px rgba(0, 0, 0, 0.4);
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
		grid-template-areas: 'title date' 'description description';
		grid-template-columns: auto 55px;
	}
	.text-hack {
		grid-area: description;
		text-overflow: ellipsis;
		overflow: hidden;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
	}
	.text-title {
		grid-area: title;
	}
	.text-date {
		grid-area: date;
		text-align: center;
	}
	.rightside {
		grid-template-rows: 50px auto;
		padding: 7px;
	}
</style>
