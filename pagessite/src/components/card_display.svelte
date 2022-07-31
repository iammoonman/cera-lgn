<style>
	.card {
		background-color: grey;
		width: 468px;
		height: 336px;
		border-radius: 17px;
		display: grid;
		grid-template-columns: "a b";
	}
    .textbox {
        grid-area: a;
			outline: 1px solid red;
			display: flex;
			flex-direction: column;
			justify-items: space-between;
			gap: 6px;
			padding: 12px;
			max-width: 50%;
    }
	.textbox>* {
		margin-top: 0;
		margin-bottom: 0;
	}
	.textbox>footer{
		margin-top: auto;
	}
    .cardbox {
        grid-area: b;
			outline: 1px solid red;
    }
</style>

<div class="card">
	<section class="textbox">
		<h3>
			Title
		</h3>
		<p>
			Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.
		</p>
		<footer>
			SET/CN
		</footer>
	</section>
	<div class="cardbox">
		CARD AREA
	</div>
</div>