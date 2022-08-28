<script lang="ts">
	// Track cursor position
	// If above center, negative x
	// If below center, positive x
	// If right, negative y
	// If left, positive y
	// Angle proportional to the distance from center
	let v: HTMLDivElement;
	$: pos = { x: 0, y: 0 };
	function handleMM(e: { clientX: any; clientY: any }) {
		pos = {
			x: e.clientX - v.getBoundingClientRect().left,
			y: e.clientY - v.getBoundingClientRect().top
		};
	}
	function handleML() {
		pos = { x: 168, y: 234 };
	}
	function distanceToPoint(x1: number, y1: number, x2: number, y2: number) {
		return Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
	}
	function normalize(x: number, x_max: number, x_min: number) {
		return (x - x_min) / (x_max - x_min);
	}
    $: {
        console.log(normalize(pos.x - 168, 168, 0) * 100);
    }
    // --posY = distance from center at 0 normalized to 30
</script>

<div
	class="card_s"
	on:mousemove={handleMM}
	on:mouseleave={handleML}
	style={`--posX: ${normalize(pos.y - 234, 234, 0) * 30}deg; --posY: ${normalize(pos.x - 168, 168, 0) * 30}deg;`}
	bind:this={v}
>
	<div class="card__glare" style={`--rX: ${normalize(pos.y - 234, 234, 0) * 100}%; --rY: ${normalize(pos.x - 168, 168, 0) * 100}%;`} />
	&nbsp;
</div>

<style>
	.card_s {
		margin-left: 20px;
		transition: transform ease 100ms;
		background: linear-gradient(217deg, rgba(255, 0, 0, 0.8), rgba(255, 0, 0, 0) 70.71%),
			linear-gradient(127deg, rgba(0, 255, 0, 0.8), rgba(0, 255, 0, 0) 70.71%),
			linear-gradient(336deg, rgba(0, 0, 255, 0.8), rgba(0, 0, 255, 0) 70.71%);
		height: 468px;
		width: 336px;
		transform: rotateX(clamp(-30deg, var(--posX), 30deg)) rotateY(clamp(-20deg, var(--posY), 20deg));
	}
	.card__glare {
		transform: translateZ(10px);
        height: 100%;
        width: 100%;
		z-index: 4;
		background: radial-gradient(
			farthest-corner circle at var(--rY) var(--rX),
			rgba(255, 255, 255, 0.8) 10%,
			rgba(255, 255, 255, 0.65) 20%,
			rgba(0, 0, 0, 0.5) 90%
		);
		mix-blend-mode: overlay;
        opacity: 30%;
        filter: brightness(0.8) contrast(1.5);
	}
</style>
