<script lang="ts">
	import Ripple from '@smui/ripple';
    export let text: string;
    export let bgColorClass: string;
</script>

<button
	class="px-4 py-2 rounded-md drop-shadow-md font-semibold text-sm text-black tracking-wide {bgColorClass}"
	use:Ripple={{ surface: true }}
	on:click
>
	{text}
</button>

<style>
</style>
