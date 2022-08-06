<script lang="ts">
	let headers = {};
	import { V3Store } from './stores';
	V3Store.subscribe((v) => {
		headers = { full_name: v.full_name, default_set: v.default_set };
	});
	import Distrobuilder from './distrobuilder.svelte';
	import Slotsbuilder from './slotsbuilder.svelte';
</script>

<section id="headers" class="rounded-xl grid grid-cols-1 p-1 gap-1 hidden">
	HEADERS
	<div class="rounded-xl flex flex-row justify-between">
		<label for="full_name" class="p-2">Set Full Name</label>
		<input id="full_name" value={''} class="rounded-sm m-1" />
	</div>
	<div class="rounded-xl flex flex-row justify-between">
		<label for="custom_set" class="p-2">Custom Set Code</label>
		<input id="custom_set" value={''} class="rounded-sm m-1" />
	</div>
	<div class="rounded-xl flex flex-row justify-between">
		<label for="default_set" class="p-2">Default Set Code</label>
		<input id="default_set" value={''} class="rounded-sm m-1" />
	</div>
</section>
<Distrobuilder />

<Slotsbuilder />
<style>
</style>
