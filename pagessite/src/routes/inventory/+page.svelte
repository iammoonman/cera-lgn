<script lang="ts">
	import type { CardWrapper, Save, TTSCard } from 'src/types/tts';
	import { dndzone } from 'svelte-dnd-action';
	import { v4 } from 'uuid';
	import { flip } from 'svelte/animate';
	import Inventorycard from '../../components/inventorycard/inventorycard.svelte';
	import Tooltip, { Wrapper } from '@smui/tooltip';
	$: nth = 0;

	function handleFileInput() {
		Promise.allSettled(
			Array.from(files_input).map((f) => {
				return f.text().then((tt) => {
					let save = JSON.parse(tt) as Save;
					let output: TTSCard[][] = [];
					for (const f of save.ObjectStates) {
						if (f.Name === 'Bag') {
							for (const g of f.ContainedObjects) {
								if (g.Name === 'Deck') {
									output.push(g.ContainedObjects);
								}
								if (g.Name === 'Card') {
									output.push([g]);
								}
							}
						}
						if (f.Name === 'Deck') {
							output.push(f.ContainedObjects);
						}
						if (f.Name === 'Card') {
							output.push([f]);
						}
					}
					return output;
				});
			})
		).then((result) => {
			result.forEach((r) => {
				if (r.status === 'fulfilled') {
					r.value.map((c) => {
						superList[nth] = c.map((cf) => {
							return { id: v4(), card: cf, highlighted: true };
						});
						nth = nth + 1;
					});
				}
			});
		});
	}
	let files_input: FileList;
	let outlist = [] as CardWrapper[];
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
	function handleDndEvent(e: any, bigKey?: keyof typeof superList) {
		if (bigKey === undefined) outlist = e.detail.items;
		if (bigKey !== undefined) {
			superList[bigKey] = e.detail.items;
		}
	}
	let superList: Record<string, CardWrapper[]> = {};
</script>

<div class="parent">
	<div class="sidebar flex flex-col">
		<input
			type="file"
			bind:files={files_input}
			accept="text/json"
			on:change={() => {
				handleFileInput();
			}}
		/>
		<button on:click={() => outputSave()}>Export</button>
		<input
			type="text"
			on:change={(e) => {
				superList = Object.fromEntries(
					Object.entries(superList).map(([k, cc]) => {
						return [
							k,
							cc.map((c) => {
								return {
									...c,
									highlighted:
										e.currentTarget.value === '' ||
										c.card.Description.includes(e.currentTarget.value)
								};
							})
						];
					})
				);
			}}
		/>
		<section
			use:dndzone={{ items: outlist, flipDurationMs: 300 }}
			on:consider={(e) => handleDndEvent(e)}
			on:finalize={(e) => handleDndEvent(e)}
			class="flex flex-wrap gap-2"
			style="min-height: 120px; max-height: 900px; overflow-y: scroll"
		>
			{#each outlist as item (item.id)}
				<div animate:flip={{ duration: 300 }}>
					<Inventorycard card={item.card} highlighted={item.highlighted} />
				</div>
			{/each}
		</section>
	</div>
	<div class="grid overflow-scroll">
		{#each Object.entries(superList) as [k, v]}
			<div class="">
				<div class="text-xl">Group {k}</div>
				<section
					use:dndzone={{ items: v, flipDurationMs: 300 }}
					on:consider={(e) => handleDndEvent(e, k)}
					on:finalize={(e) => handleDndEvent(e, k)}
					class="grouping"
				>
					{#each v as bigItem (bigItem.id)}
						<div animate:flip={{ duration: 300 }} style="height: min-content;">
							<Wrapper>
								<Tooltip>{bigItem.card.Nickname}</Tooltip>
								<Inventorycard card={bigItem.card} highlighted={bigItem.highlighted} />
							</Wrapper>
						</div>
					{/each}
				</section>
			</div>
		{/each}
	</div>
</div>

<style>
	.parent {
		display: grid;
		grid-template-columns: 20% 80%;
		background-color: #aaaaaa;
		overflow: hidden;
	}
	.parent > * {
		outline: 1px solid red;
	}
	.grouping {
		display: grid;
		grid-template-rows: 37px 37px 37px 37px;
		grid-template-columns: repeat(auto-fill, 120px);
		grid-auto-flow: column;
		height: 280px;
		gap: 2px;
	}
	.grid {
		max-height: 100vh;
	}
</style>
