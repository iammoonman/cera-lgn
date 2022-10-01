<script lang="ts">
	import type { CardDisplayType } from 'src/types/displaycard';
	export let C: CardDisplayType;
	$: horizontal = C.description == '';
	let scry_link = `https://scryfall.com/card/${C.set === '' ? 'lea' : C.set}/${
		C.cn === '' ? '1' : C.cn
	}`;
	let image_link = C.uri === '' ? 'https://picsum.photos/336/468' : C.uri;
	import Fancycardhover from './fancycardhover.svelte';
</script>

<div
	class={horizontal ? 'card-h tiny-shadow grid grid-cols-2' : 'card-v tiny-shadow grid grid-cols-1'}
>
	<section class={`textbox-h ${horizontal ? 'flex-col' : 'flex-row'}`}>
		<div class="text-lg truncate force-height-title">
			{C.title === '' ? 'Animate Wall' : C.title}
		</div>
		<hr />
		<p class={`text-hack text-sm force-height-desc ${horizontal ? '' : 'invisible'}`}>
			{C.description === ''
				? `I'll be honest I don't play EDH with strangers very often, I have a wide range of friends that I play with and most of the myriad of problems I see brought up on this subreddit never really seem to be a problem for me so maybe it's a perspective issue.

			Anyway politics has always been a large part of the fun of multiplayer at least with me and my friends, would others really get salty if I say "Listen, you can kill me, but since I have a gun you'll die after, so what if you don't kill me?" which in my eyes is just like any other deal, 2 players agreeing on a line of actions because they both believe it will let them win the whole thing in the long run.
			
			Are yall mostly concerned about brandishing firearms for no reason?`
				: C.description}
		</p>
		<footer class="text-xs flex space-x-4">
			<span>{C.set === '' ? 'LEA' : C.set} / {C.cn === '' ? '1' : C.cn}</span>
			<a href={scry_link}>Scryfall</a>
		</footer>
	</section>
	<div class={`cardbox ${horizontal ? 'ml-1 mr-2' : 'ml-9 mr-9 mb-3'}`}>
		<Fancycardhover height={234} width={168}>
			<img class="card tiny-shadow" alt="card" src={image_link} />
		</Fancycardhover>
	</div>
</div>

<style>
	.tiny-shadow {
		box-shadow: 0 1px 3px 0 black, 0 1px 2px -1px black;
	}
	.card-h {
		background-color: var(--gamma);
		aspect-ratio: 468 / 336;
		width: 468px;
		height: 336px;
		border-radius: 3.5% / 4.75%;
		background-color: #144A76;
		color: white;
	}
	.card-v {
		background-color: var(--gamma);
		aspect-ratio: 336 / 468;
		height: 468px;
		width: 336px;
		border-radius: 4.75% / 3.5%;
		background-color: #18578C;
	}
	.card {
		background-color: var(--yotta);
		aspect-ratio: 336 / 468;
		height: auto;
		border-radius: 4.75% / 3.5%;
	}
	.textbox-h {
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
		color: var(--alpha);
	}
	.textbox-h > footer {
		margin-top: auto;
		color: var(--beta);
	}
	.cardbox {
		display: flex;
		flex-direction: column;
		justify-content: center;
		border-radius: 0 15px 15px 0;
	}
	.text-hack {
		text-overflow: ellipsis;
		overflow: hidden;
		display: -webkit-box;
		-webkit-line-clamp: 12;
		-webkit-box-orient: vertical;
	}
	hr {
		border-color: var(--yotta);
		margin-left: 5px;
		margin-right: 16px;
	}
	.force-height-title {
		height: 1.75rem;
	}
	.force-height-desc {
		min-height: 1.25rem;
	}
	.invisible {
		display: none;
	}
</style>
