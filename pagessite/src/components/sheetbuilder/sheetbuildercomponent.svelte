<script lang="ts">
	import Draggerbox from './draggerbox.svelte';
import Filestructureform from './filestructureform.svelte';
</script>

<div class="m-10 rounded-md bg-blue-200 p-5">
	<Draggerbox sheetname={'a'} slotname={'c'} />
	<Filestructureform />
</div>

<style>
	div {
		width: min-content;
	}
</style>
