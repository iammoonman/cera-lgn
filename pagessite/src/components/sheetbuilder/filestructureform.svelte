<script lang="ts">
	let headers = {};
	import { V3Store } from './stores';
	V3Store.subscribe((v) => {
		headers = { full_name: v.full_name, default_set: v.default_set };
	});
	import Distrobuilder from './distrobuilder.svelte';
	import Slotsbuilder from './slotsbuilder.svelte';
	import { get } from 'svelte/store';
	import Button from '../utilities/button.svelte';
	$: textcontent = '';
</script>

<section id="headers" class="rounded-xl grid grid-cols-1 p-1 gap-1">
	HEADERS
	<Button
		text={'Print object'}
		bgColorClass={'bg-green-200'}
		on:click={() => {
			const output2 = get(V3Store);
			const newOutput = {
				full_name: output2.full_name,
				default_set: output2.default_set,
				slots: Object.fromEntries(
					[...output2.slots].map(([key, value]) => {
						return [
							key,
							{
								flags: value.flags,
								options: value.options.map((o) => {
									return { struct: Object.fromEntries([...o.struct]), freq: o.freq };
								}),
								sheets: Object.fromEntries([...value.sheets])
							}
						];
					})
				),
				distros: output2.distros.map((d) => {
					return {
						slots: Object.fromEntries([...d.slots]),
						drops: Object.fromEntries([...d.drops]),
						freq: d.freq
					};
				})
			};
			console.log(JSON.stringify(newOutput));
			textcontent = JSON.stringify(newOutput)
		}}
	/>
	<textarea disabled value={textcontent} style="resize: none; overflow-y: scroll;" />
	<div class="rounded-xl flex flex-row justify-between">
		<label for="full_name" class="p-2">Set Full Name</label>
		<input
			id="full_name"
			value={''}
			class="rounded-sm m-1"
			on:change={(e) => {
				V3Store.update((oldstore) => {
					// @ts-ignore
					return { ...oldstore, full_name: e.target.value };
				});
			}}
		/>
	</div>
	<div class="rounded-xl flex flex-row justify-between">
		<label for="custom_set" class="p-2">Custom Set Code</label>
		<input
			id="custom_set"
			value={''}
			class="rounded-sm m-1"
			on:change={(e) => {
				V3Store.update((oldstore) => {
					// @ts-ignore
					return { ...oldstore, full_name: e.target.value };
				});
			}}
		/>
	</div>
	<div class="rounded-xl flex flex-row justify-between">
		<label for="default_set" class="p-2">Default Set Code</label>
		<input
			id="default_set"
			value={''}
			class="rounded-sm m-1"
			on:change={(e) => {
				V3Store.update((oldstore) => {
					// @ts-ignore
					return { ...oldstore, default_set: e.target.value };
				});
			}}
		/>
	</div>
</section>
<Distrobuilder />

<Slotsbuilder />

<style>
</style>
