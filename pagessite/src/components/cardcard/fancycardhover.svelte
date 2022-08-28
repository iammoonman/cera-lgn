<script lang="ts">
	// Track cursor position
	// If above center, negative x
	// If below center, positive x
	// If right, negative y
	// If left, positive y
	// Angle proportional to the distance from center
	export let width = 336;
	export let height = 468;
	let v: HTMLDivElement;
	$: pos = { x: 0, y: 0 };
	function handleMM(e: { clientX: any; clientY: any }) {
		pos = {
			x: e.clientX - v.getBoundingClientRect().left,
			y: e.clientY - v.getBoundingClientRect().top
		};
	}
	function handleML() {
		pos = { x: width / 2, y: height / 2 };
	}
	function distanceToPoint(x1: number, y1: number, x2: number, y2: number) {
		return Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
	}
	function normalize(x: number, x_max: number, x_min: number) {
		return (x - x_min) / (x_max - x_min);
	}
	// --posY = distance from center at 0 normalized to 30
	$: {
		console.log(normalize(pos.y - height / 2, height / 2, 0) * 21);
	}
</script>

<div class="superparent">
	<div
		class="card_s"
		on:mousemove={handleMM}
		on:mouseleave={handleML}
		style={`--posX: ${-normalize(pos.x - width / 2, width / 2, 0) * 17}deg; --posY: ${
			normalize(pos.y - height / 2, height / 2, 0) * 13
		}deg; --rX: ${normalize(pos.x, width, 0) * 100}%; --rY: ${normalize(pos.y, height, 0) * 100}%;`}
		bind:this={v}
	>
		<div class="card__glare" />
		<slot />
	</div>
</div>

<style>
	* {
		transform-style: preserve-3d;
		transform: translate3d(0, 0, 0.1px);
	}
	.superparent {
		perspective: 600px;
	}
	.card_s {
		will-change: transform;
		transform-origin: center;
		transition: transform  100ms;
		/* background: linear-gradient(217deg, rgba(255, 0, 0, 0.8), rgba(255, 0, 0, 0) 70.71%),
			linear-gradient(127deg, rgba(0, 255, 0, 0.8), rgba(0, 255, 0, 0) 70.71%),
			linear-gradient(336deg, rgba(0, 0, 255, 0.8), rgba(0, 0, 255, 0) 70.71%); */
		transform: rotateX(var(--posY)) rotateY(var(--posX));
		box-shadow: 0px 10px 20px -5px black;
		border-radius: 4.75% / 3.5%;
	}
	.card__glare {
		border-radius: 4.75% / 3.5%;
		transform: translateZ(1px);
		height: 100%;
		width: 100%;
		z-index: 4;
		position: absolute;
		background: radial-gradient(
			farthest-corner circle at var(--rX) var(--rY),
			rgba(255, 255, 255, 1) 10%,
			rgba(255, 255, 255, 0.65) 20%,
			rgba(0, 0, 0, 0.5) 90%
		);
		mix-blend-mode: overlay;
		opacity: 80%;
		filter: brightness(0.8) contrast(1.5);
		transition: opacity 100ms;
	}
</style>
