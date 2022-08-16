<script>
	import Carddisplay from '../components/carddisplay.svelte';
	import Masonry from '../components/utilities/masonry.svelte';
</script>

<div
	class="w-full h-min p-2 mb-2 z-10 relative flex flex-row justify-between shadow-lg shadow-green-700/40 bg-green-200"
>
	<span>The Rat Zone</span>
	<span>Hamburgler</span>
</div>
<div class="mx-auto relative gap-1 p-4 shadow-lg masonrygrid rounded-xl border-blue-100">
	<Carddisplay horizontal={false} />
	<Carddisplay />
	<Carddisplay />
    <Carddisplay />
    <Carddisplay horizontal={true} />
    <Carddisplay />
    <Carddisplay horizontal={false} />
    <Carddisplay />
    <Carddisplay />
</div>

<style>
	.masonrygrid {
        display: flex;
        flex-wrap: wrap;
        gap: 2rem;
        place-items: center;
        max-width: 90%;
	}
</style>