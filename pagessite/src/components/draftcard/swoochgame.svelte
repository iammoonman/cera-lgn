<script lang="ts">
	import { Wrapper } from '@smui/tooltip';
	import Tooltip from '@smui/tooltip/src/Tooltip.svelte';
	import type { PD } from 'src/types/discord';
	import { fly } from 'svelte/transition';
	import type { Match } from 'src/types/events';
	import Swooch from '../utilities/swooch.svelte';
	export let m: Match;
	export let pn: Record<string, PD>;
</script>

<div class="container">
	<Wrapper>
		<div class="tiltedcontainer" in:fly={{ duration: 200, x: -50 }}>
			<div class="swoochcontainer">
				<Swooch fill={'black'} h={20} w={90} />
			</div>
			<img src={pn[m.p_ids[0]].avatarURL ?? ''} alt="pfp" />
			<span>{[...m.games].filter(([k, x]) => x === m.p_ids[0]).length}</span>
		</div>
        <Tooltip xPos="center" yPos="above" style="margin-top: 12px">{pn[m.p_ids[0]].username}</Tooltip>
	</Wrapper>
	{#if m.p_ids[1] !== '-1'}
		<Wrapper>
			<div class="tiltedcontainer_2" in:fly={{ duration: 200, x: 50, delay: 50 }}>
				<div class="swoochcontainer_2">
					<Swooch fill={'black'} h={20} w={90} />
				</div>
				<span>{[...m.games].filter(([k, x]) => x === m.p_ids[1]).length}</span>
				<img src={pn[m.p_ids[1]]?.avatarURL ?? ''} alt="pfp" />
                <Tooltip xPos="center" yPos="below">{pn[m.p_ids[1]].username}</Tooltip>
			</div>
		</Wrapper>
	{:else}
		<div class="tiltedcontainer_2" in:fly={{ duration: 200, x: 50, delay: 50 }}>
			<div class="swoochcontainer_2">
				<Swooch fill={'black'} h={20} w={90} />
			</div>
			<span>{'BYE'}</span>
		</div>
	{/if}
</div>

<style>
	.container {
		display: block;
		position: relative;
		height: 85px;
        width: 85px;
	}
	.tiltedcontainer {
		transform: rotateZ(-15deg);
		display: flex;
		justify-content: end;
		flex-direction: row;
		gap: 7px;
		position: relative;
		height: 50px;
		right: 20px;
        width: 85px;
	}
	.tiltedcontainer > img {
		height: 35px;
		width: 35px;
		filter: drop-shadow(0px 2px 5px black);
		border-radius: 50%;
	}
	.tiltedcontainer > span {
		height: 35px;
		font-size: 35px;
		top: -8px;
		position: relative;
	}
	.swoochcontainer {
		position: absolute;
		bottom: 0;
		right: -7px;
		transform: rotateZ(-5deg) rotateY(180deg);
	}
	.tiltedcontainer_2 {
		transform: rotateZ(-17deg);
		display: flex;
		justify-content: start;
		flex-direction: row;
		gap: 7px;
		position: relative;
		height: 50px;
		right: -23px;
		top: -10px;
		padding-top: 5px;
	}
	.tiltedcontainer_2 > img {
		height: 35px;
		width: 35px;
		filter: drop-shadow(0px 2px 5px black);
		border-radius: 50%;
	}
	.tiltedcontainer_2 > span {
		height: 35px;
		font-size: 35px;
		top: -10px;
		position: relative;
	}
	.swoochcontainer_2 {
		position: absolute;
		top: -6px;
		left: -7px;
		transform: rotateZ(-4deg) rotateX(180deg);
	}
</style>
