<div style="position: absolute; left: 600px; top: 200px; transform-style: preserve-3d;" class="q">
	<div class="a square specialcolor" />
	<div class="b square specialcolor" />
	<div class="c square specialcolor" />
	<div class="d square specialcolor" />
	<div class="e square specialcolor" />
	<div class="f square specialcolor" />
</div>

<style>
	.square {
		min-width: 100%;
		min-height: 100%;
		position: absolute;
		backface-visibility: visible;
	}
	.specialcolor {
		background: linear-gradient(217deg, rgba(255, 0, 0, 0.8), rgba(255, 0, 0, 0) 70.71%),
			linear-gradient(127deg, rgba(0, 255, 0, 0.8), rgba(0, 255, 0, 0) 70.71%),
			linear-gradient(336deg, rgba(0, 0, 255, 0.8), rgba(0, 0, 255, 0) 70.71%);
	}
	.q {
		transform: rotate3d(1, 1, 1, 25deg);
		height: 100px;
		width: 100px;
	}
	.a {
		transform: translateZ(50px);
		width: 120px;
	}
	.b {
		transform: rotateY(180deg) translateZ(50px);
		width: 120px;
	}
	.c {
		transform: rotateY(90deg) translateZ(50px) translateZ(20px);
	}
	.d {
		transform: rotateX(90deg) translateZ(50px);
		width: 120px;
	}
	.e {
		transform: rotateY(-90deg) translateZ(50px);
	}
	.f {
		transform: rotateX(-90deg) translateZ(50px);
		width: 120px;
	}
</style>