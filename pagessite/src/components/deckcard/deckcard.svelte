<script lang="ts">
	import Tooltip, { Wrapper } from '@smui/tooltip';
	import Symbol from '../symbols/symbol.svelte';
	import { createEventDispatcher } from 'svelte';
	import type { PD } from 'src/types/discord';
    export let p: PD;
	const dispatch = createEventDispatcher();
</script>

<div class="outercard grid grid-cols-1 p-2 relative justify-between">
    <div class="black-border"><div></div><div></div></div>
    <Wrapper>
		<div class="titlecard relative">
            <div class="player-avatar">
                <img src={p.avatarURL} alt="player_pfp" />
            </div>
			<span class="text-title text-ellipsis overflow-x-hidden whitespace-nowrap" style="grid-area: playername;">
                <span>{p.username}</span>
			</span>
			<span class="text-date" style="grid-area: deckname;">{'D.date.toLocaleDateString()'}</span>
		</div>
		<Tooltip xPos="center" yPos="detected" class="bg-slate-400">
			{'D.title'}
			<hr />
			{'No description provided.'}
		</Tooltip>
	</Wrapper>
    <div class="grid grid-cols-2 px-2">
        <div>Large card display</div>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>CARDNAME</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>Colossal Dreadmaw</td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="px-4 bottomrow">
        Bottom row
    </div>
	<button class="absolute tap-icon" on:click={() => dispatch('untap', {})}>
		<span>Show Picks</span>
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
		background-color: #5e3710;
		color: white;
		overflow-x: visible;
		overflow-y: clip;
        position: relative;
		grid-template-rows: 75px 324px 45px;
	}
	table {
		display: block;
		text-align: left;
		border-collapse: collapse;
		font-size: small;
		overflow: auto;
        position: relative;
		scrollbar-gutter: stable;
	}
	tbody tr:nth-child(2n + 1) {
		background-color: #ffffff06;
	}
    tbody tr td {
        width: 1px;
    }
    tbody tr td:last-child {
        width: 100%;
    }
	thead {
		position: sticky;
		top: 0; /* Don't forget this, required for the stickiness */
		box-shadow: 0 2px 2px -2px white;
	}
	tbody {
		white-space: nowrap;
	}
	.titlecard {
		display: grid;
        grid-template-areas: 'avatar playername' 'avatar deckname';
		grid-template-columns: 65px auto;
		grid-template-rows: auto auto;
		align-items: center;
		box-shadow: 0 1px 3px -3px white;
        padding: 0.5rem;
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
	.player-avatar {
        width: 55px;
        height: 55px;
        grid-area: avatar;
	}
	.player-avatar > img {
		filter: drop-shadow(0px 2px 5px black);
		border-radius: 50%;
	}
    .bottomrow {
		box-shadow: 0 -1px 3px -3px white;
    }
</style>
