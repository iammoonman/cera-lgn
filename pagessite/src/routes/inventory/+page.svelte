<script lang="ts">
	import type { CardWrapper, Save, TTSCard } from 'src/types/tts';
	import VerticalList from './VerticalList.svelte';
	import { v4 } from 'uuid';

	function handleFileInput() {
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
											return { ...c };
										})
									];
								}
								if (g.Name === 'Card') {
									output = [...output, { ...g }];
								}
							}
						}
						if (f.Name === 'Deck') {
							output = [
								...output,
								...f.ContainedObjects.map((c) => {
									return { ...c };
								})
							];
						}
						if (f.Name === 'Card') {
							output = [...output, { ...f }];
						}
					}
					return output;
				});
			})
		).then((result) => {
			let newList: CardWrapper[] = [];
			result.forEach((r) => {
				if (r.status === 'fulfilled')
					newList = [
						...newList,
						...r.value.map((c) => {
							return { id: v4(), card: c, highlighted: false };
						})
					];
			});
			biglist = [...biglist, ...newList];
		});
	}
	let files_input: FileList;
	let outlist = [] as CardWrapper[];
	let biglist = [] as CardWrapper[];
	function outputSave() {
		console.log(
			Object.fromEntries(
				outlist.map((v, i) => {
					return [i + 1, Object.entries(v.card.CustomDeck)[0][1]];
				})
			)
		);
		if (outlist.length < 2) return alert("Don't export with one or fewer cards, it breaks things.");
		const data: Save = {
			ObjectStates: [
				{
					Name: 'Deck',
					ColorDiffuse: { b: 0, g: 0, r: 0 },
					ContainedObjects: outlist.map((c, i) => {
						return {
							...c.card,
							CardID: (i + 1) * 100,
							CustomDeck: Object.fromEntries(
								Object.entries(c.card.CustomDeck).map(([a, b]) => {
									return [i + 1, b];
								})
							)
						};
					}),
					CustomDeck: Object.fromEntries(
						outlist.map((v, i) => {
							return [i + 1, Object.entries(v.card.CustomDeck)[0][1]];
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
		const filename = `${prompt('File name:')}.json` ?? 'myCards.json';
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
	$: {
		biglist.sort((a, b) => {
			return a.highlighted ? 1 : -1;
		});
	}
</script>

<div class="parent">
	<div class="sidebar">
		<input
			type="file"
			bind:files={files_input}
			accept="text/json"
			on:change={() => {
				handleFileInput();
			}}
		/>
		<button on:click={() => outputSave()}>Export</button>
		<button
			on:click={() => {
				outlist = [biglist, (biglist = outlist)][0];
			}}>Swap</button
		>
		<input
			type="text"
			on:change={(e) => {
				// Doesn't work.
				biglist.map((c) => {
					return { ...c, highlighted: c.card.Description.includes(e.currentTarget.value) };
				});
			}}
		/>
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
