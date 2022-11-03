<script lang="ts">
	import Tooltip, { Wrapper } from '@smui/tooltip';
	import type { PD } from 'src/types/discord';
	import type { CardDisplayType } from 'src/types/displaycard';
	export let C: CardDisplayType;
	export let pn: Record<string, PD>;
	let scry_link = `https://scryfall.com/card/${C.set === '' ? 'lea' : C.set}/${
		C.cn === '' ? '1' : C.cn
	}`;
	let image_link = C.uri === '' ? 'https://picsum.photos/336/468' : C.uri;
	import Fancycardhover from './fancycardhover.svelte';
</script>

<div class={'card-v tiny-shadow grid grid-cols-1 relative'}>
	<div class="black-border">
		<div />
		<div />
	</div>
	<Wrapper>
		<section class="textbox-h flex-row relative">
			<div class="text-lg truncate force-height-title relative">
				{C.title === '' ? 'Animate Wall' : C.title}
			</div>
			<Tooltip xPos="center" yPos="detected" class="bg-slate-400">
				{pn[C.p_id].username}
				<hr />
				{C.description ?? ""}
			</Tooltip>
			<div class="text-xs flex space-x-4">
				<span>{C.set === '' ? 'LEA' : C.set} / {C.cn === '' ? '1' : C.cn}</span>
				<a href={scry_link}>Scryfall</a>
			</div>
		</section>
	</Wrapper>
	<div class="cardbox ml-9 mr-9 mb-3">
		<Fancycardhover height={234} width={168}>
			<img class="card tiny-shadow" alt="card" src={image_link} />
		</Fancycardhover>
	</div>
</div>

<style>
	.tiny-shadow {
		box-shadow: 0 1px 3px 0 black, 0 1px 2px -1px black;
	}
	.card-v {
		aspect-ratio: 336 / 468;
		height: 468px;
		width: 336px;
		border-radius: 4.75% / 3.5%;
		background-color: #18578c;
		color: white;
	}
	.card {
		aspect-ratio: 336 / 468;
		height: auto;
		border-radius: 4.75% / 3.5%;
	}
	.textbox-h {
		z-index: 1;
		display: flex;
		flex-direction: column;
		justify-items: space-between;
		gap: 6px;
		padding: 12px;
		border-radius: 15px 0 0 15px;
	}
	.textbox-h > * {
		margin-top: 0;
		margin-bottom: 0;
	}
	.cardbox {
		z-index: 1;
		display: flex;
		flex-direction: column;
		justify-content: center;
		border-radius: 0 15px 15px 0;
		transition-duration: 400ms;
	}
	.cardbox:hover {
		transition-property: scale;
		scale: 1.05;
	}
	.force-height-title {
		box-shadow: 0 1px 3px -3px white;
	}
	.black-border {
		position: absolute;
		width: 100%;
		height: 100%;
		border-radius: 4.75% / 3.5%;
		box-shadow: inset 0 0 0 8px black;
		z-index: 0;
	}
	.black-border:after {
		position: absolute;
		height: 15px;
		width: 320px;
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
</style>
