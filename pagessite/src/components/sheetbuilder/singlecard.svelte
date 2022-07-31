<script>
	export let cardName = '';
	export let uri = '';
</script>

<div>
	<img src={uri} alt={cardName} />
</div>

<style>
	img {
		height: 102px;
		width: 73px;
	}
</style>
