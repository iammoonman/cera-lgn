<div class="card grid grid-cols-2">
	<section class="textbox">
		<h3>Title</h3>
		<p>
			Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has
			been the industry's standard dummy text ever since the 1500s, when an unknown printer took a
			galley of type and scrambled it to make a type specimen book.
		</p>
		<footer>SET/CN</footer>
	</section>
	<div class="cardbox">
		<div class="v_card"></div>
	</div>
</div>

<style>
	.card {
		background-color: grey;
		aspect-ratio: 468 / 336;
		width: 468px;
		height: 336px;
		border-radius: 15px;
		margin: 15px;
		box-shadow: 0 1px 3px 0 black, 0 1px 2px -1px black;
	}
	.v_card {
		background-color: lightslategray;
		aspect-ratio: 336 / 468;
		height: auto;
		border-radius: 15px;
		margin: 15px;
		box-shadow: 0 1px 3px 0 black, 0 1px 2px -1px black;
	}
	.textbox {
		display: flex;
		flex-direction: column;
		justify-items: space-between;
		gap: 6px;
		padding: 12px;
	}
	.textbox > * {
		margin-top: 0;
		margin-bottom: 0;
	}
	.textbox > footer {
		margin-top: auto;
	}
</style>
