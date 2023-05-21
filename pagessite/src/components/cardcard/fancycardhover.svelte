<script lang="ts">
	// Track cursor position
	// If above center, negative x
	// If below center, positive x
	// If right, negative y
	// If left, positive y
	// Angle proportional to the distance from center
	export let width = 264;
	export let height = 367;
	let v: HTMLDivElement;
	let w: number = 264;
	let h: number = 367;
	let pos = { x: (w ?? width) / 2, y: (h ?? height) / 2 };
	function handleMM(e: { clientX: any; clientY: any }) {
		pos = {
			x: e.clientX - v.getBoundingClientRect().left,
			y: e.clientY - v.getBoundingClientRect().top
		};
	}
	function handleML() {
		pos = { x: (w ?? width) / 2, y: (h ?? height) / 2 };
	}
	function distanceToPoint(x1: number, y1: number, x2: number, y2: number) {
		return Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
	}
	function normalize(x: number, x_max: number, x_min: number) {
		return (x - x_min) / (x_max - x_min);
	}
</script>

<div
	class="superparent"
	on:mousemove={handleMM}
	on:mouseleave={handleML}
	bind:offsetWidth={w}
	bind:offsetHeight={h}
	bind:this={v}
>
	<div
		class="card_s"
		style={`--posX: ${-normalize(pos.x - w / 2, w, 0) * 60}deg;
		--posY: ${normalize(pos.y - h / 2, h, 0) * 45}deg;
		--rX: ${normalize(pos.x, w, 0) * 100}%;
		--rY: ${normalize(pos.y, h, 0) * 100}%;`}
	>
		<div class="card__glare" />
		<slot />
	</div>
</div>

<style>
	* {
		transform-style: preserve-3d;
	}
	.superparent {
		perspective: 600px;
	}
	.card_s {
		will-change: transform;
		transform-origin: center;
		transition: transform 0ms;
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
			rgba(0, 0, 0, 0.2) 90%
		);
		mix-blend-mode: overlay;
		opacity: 0%;
		filter: brightness(0.8) contrast(1.5);
		transition: opacity 100ms;
	}
	.card_s:hover > .card__glare {
		opacity: 30%;
	}
</style>
