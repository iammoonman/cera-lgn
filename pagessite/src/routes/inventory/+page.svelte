<script lang="ts">
	import type { Save, TTSCard } from 'src/types/tts';
	import VerticalList from './VerticalList.svelte';
	import { v4 as uuidv4 } from 'uuid';
	import { overrideItemIdKeyNameBeforeInitialisingDndZones } from 'svelte-dnd-action';
	overrideItemIdKeyNameBeforeInitialisingDndZones('GMNotes');

	let files_input: FileList;
	$: if (files_input)
		Promise.allSettled(
			Array.from(files_input).map((f) => {
				return f.text().then((tt) => {
					let save = JSON.parse(tt) as Save;
					let output: TTSCard[] = [];
					for (const f of save.ObjectStates) {
						if (f.Name === 'Bag') {
							for (const g of f.ContainedObjects) {
								if (g.Name === 'Deck') {
									output = [
										...output,
										...g.ContainedObjects.map((c) => {
											return { ...c, GMNotes: c.GMNotes ?? uuidv4() };
										})
									];
								}
								if (g.Name === 'Card') {
									output = [...output, { ...g, GMNotes: g.GMNotes ?? uuidv4() }];
								}
							}
						}
						if (f.Name === 'Deck') {
							output = [
								...output,
								...f.ContainedObjects.map((c) => {
									return { ...c, GMNotes: c.GMNotes ?? uuidv4() };
								})
							];
						}
						if (f.Name === 'Card') {
							output = [...output, { ...f, GMNotes: f.GMNotes ?? uuidv4() }];
						}
					}
					return output;
				});
			})
		).then((result) => {
			let newList: TTSCard[] = [];
			result.forEach((r) => {
				if (r.status === 'fulfilled') newList = [...newList, ...r.value];
			});
			biglist = newList;
		});
	let outlist = [] as TTSCard[];
	let biglist = [] as TTSCard[];
	function outputSave() {
		if (outlist.length < 2) return alert("Don't export with only one card, that's such a waste of time.");
		const data: Save = {
			ObjectStates: [
				{
					Name: 'Deck',
					ColorDiffuse: { b: 0, g: 0, r: 0 },
					ContainedObjects: outlist.map((c, i) => {
						return { ...c, CardID: (i + 1) * 100 };
					}),
					CustomDeck: Object.fromEntries(
						outlist.map((v, i) => {
							return [i + 1, Object.entries(v.CustomDeck)[0][1]];
						})
					),
					DeckIDs: outlist.map((c, i) => (i + 1) * 100),
					Nickname: '',
					Transform: {
						posX: 0,
						posY: 0,
						posZ: 0,
						rotX: 0,
						rotY: 0,
						rotZ: 0,
						scaleX: 1,
						scaleY: 1,
						scaleZ: 1
					}
				}
			]
		};
		const filename = 'myFile.json';
		var file = new Blob([JSON.stringify(data)], { type: 'text/json' });
		// Others
		var a = document.createElement('a'),
			url = URL.createObjectURL(file);
		a.href = url;
		a.download = filename;
		document.body.appendChild(a);
		a.click();
		setTimeout(function () {
			document.body.removeChild(a);
			window.URL.revokeObjectURL(url);
		}, 0);
	}
</script>

<div class="parent">
	<div class="sidebar">
		<input type="file" bind:files={files_input} accept="text/json" />
		<button on:click={() => outputSave()}>Export</button>
		<VerticalList items={outlist} on:postChanges={(x) => (outlist = x.detail.items)} />
	</div>
	<div class="p-2">
		<VerticalList items={biglist} on:postChanges={(x) => (biglist = x.detail.items)} />
	</div>
</div>

<style>
	.parent {
		display: grid;
		grid-template-columns: 20% 80%;
		height: 100vh;
		width: 100vw;
	}
	.parent > * {
		outline: 1px solid red;
	}
</style>
