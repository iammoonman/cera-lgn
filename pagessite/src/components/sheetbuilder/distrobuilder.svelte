<script lang="ts">
	import Button from '../utilities/button.svelte';
	import { V3Store } from './stores';
	import List, { Item } from '@smui/list';
	import Numberinput from '../utilities/numberinput.svelte';
	import Fakeselectmenu from '../utilities/fakeselectmenu.svelte';
	function swapSlotKey(
		distro: {
			slots: Map<string, number>;
			drops: Map<string, { key: string; count: number; freq: number }[]>;
			freq: number;
		},
		oldkey: string,
		newkey: string
	) {
		const newDistro = distro;
		const oldValue = newDistro.slots.get(oldkey) ?? 1;
		newDistro.slots.delete(oldkey);
		newDistro.slots.set(newkey, oldValue);
		V3Store.update((p) => {
			return {
				...p,
				distros: [...p.distros.filter((d) => d != distro), newDistro]
			};
		});
		return;
	}
	function swapDropSlotKey(
		distro: {
			slots: Map<string, number>;
			drops: Map<string, { key: string; count: number; freq: number }[]>;
			freq: number;
		},
		oldkey: string,
		newkey: string
	) {
		const newDistro = distro;
		const prevDropslot = newDistro.drops.get(oldkey);
		if (prevDropslot === undefined) return;
		newDistro.drops.delete(oldkey);
		newDistro.drops.set(newkey, prevDropslot);
		V3Store.update((pv) => {
			return {
				...pv,
				distros: [...pv.distros.filter((d) => d !== distro), newDistro]
			};
		});
		return;
	}
	function swapdropsheetkey(
		distro: {
			slots: Map<string, number>;
			drops: Map<string, { key: string; count: number; freq: number }[]>;
			freq: number;
		},
		dropkey: string,
		oldobj: { key: string; count: number; freq: number },
		newkey: string
	) {
		const newDistro = distro;
		const newDropSheets = newDistro.drops.get(dropkey);
		if (newDropSheets === undefined) return;
		newDistro.drops.set(dropkey, [
			...newDropSheets.filter((ds) => ds.key !== oldobj.key),
			{ key: newkey, count: oldobj.count, freq: oldobj.freq }
		]);
		V3Store.update((pv) => {
			return {
				...pv,
				distros: [...pv.distros.filter((d) => d !== distro), newDistro]
			};
		});
	}
</script>

<section id="distros" class="rounded-xl p-1 grid gap-1">
	DISTROS
	{#each $V3Store.distros as distro}
		<div class="rounded-xl p-1 flex flex-col gap-1">
			<div class="rounded-xl p-1 flex flex-row justify-between">
				<span>DISTRO</span>
				<Button
					text={'Delete'}
					bgColorClass={'bg-red-400'}
					on:click={() => {
						V3Store.update((p) => {
							return {
								...p,
								distros: [...p.distros.filter((d) => d != distro)]
							};
						});
					}}
				/>
			</div>
			<div class="rounded-xl p-1">
				<span>SLOTS</span>
				<div class="grid grid-cols-[100px_minmax(100px,_1fr)] gap-1">
					<div class="grid place-content-center">
						<Button
							text={'Add Key'}
							bgColorClass={'bg-green-200'}
							on:click={() => {
								const newDistro = distro;
								const filtered = [...$V3Store.slots].filter(([o, r]) => !distro.slots.has(o));
								if (filtered.length === 0) return;
								const [newKey, newV] = filtered[0];
								newDistro.slots.set(newKey, 1);
								V3Store.update((p) => {
									return {
										...p,
										distros: [...p.distros.filter((d) => d != distro), newDistro]
									};
								});
							}}
						/>
					</div>
					<div class="grid grid-cols-1 gap-1">
						{#each [...distro.slots] as [slots_slotkey, numberinslot]}
							<div class="rounded-xl p-1 flex justify-around place-items-center">
								<Fakeselectmenu bgColor={''} buttonText={`Slot key: ${slots_slotkey}`}>
									<List>
										{#each [...$V3Store.slots].filter(([ok, ov]) => !distro.slots.has(ok)) as [slotkey, v]}
											<Item on:SMUI:action={() => swapSlotKey(distro, slots_slotkey, slotkey)}>
												<span>{slotkey}</span>
											</Item>
										{/each}
									</List>
								</Fakeselectmenu>
								<span>
									NUM:
									<Numberinput
										val={numberinslot}
										step={1}
										min={1}
										on:change={(e) => {
											const newDistro = distro;
											// @ts-ignore
											newDistro.slots.set(slots_slotkey, parseInt(e.currentTarget.value));
											V3Store.update((p) => {
												return {
													...p,
													distros: [...p.distros.filter((d) => d != distro), newDistro]
												};
											});
										}}
									/>
								</span>
								<Button
									text={'Delete'}
									bgColorClass={'bg-red-400'}
									on:click={() => {
										const newDistro = distro;
										newDistro.slots.delete(slots_slotkey);
										V3Store.update((p) => {
											return {
												...p,
												distros: [...p.distros.filter((d) => d != distro), newDistro]
											};
										});
									}}
								/>
							</div>
						{/each}
					</div>
				</div>
			</div>
			<div class="rounded-xl p-1">
				<span>DROPS</span>
				<div class="grid grid-cols-[100px_minmax(100px,_1fr)] gap-1">
					<div class="grid place-content-center">
						<Button
							text={'Add Key'}
							bgColorClass={'bg-green-200'}
							on:click={() => {
								const newDistro = distro;
								const newKey = [...$V3Store.slots].filter(([d, v]) => !newDistro.drops.has(d));
								if (newKey.length === 0) return;
								const [foundKey, foundVal] = newKey[0];
								newDistro.drops.set(foundKey, []);
								V3Store.update((p) => {
									return {
										...p,
										distros: [...p.distros.filter((d) => d != distro), newDistro]
									};
								});
							}}
						/>
					</div>
					<div class="flex flex-col gap-1 p-0">
						{#each [...distro.drops] as [dropslotkey, dropslotvalue]}
							<div class="rounded-xl p-1 flex justify-around items-center">
								<div class="flex flex-col gap-1">
									<Fakeselectmenu bgColor={''} buttonText={`Slot key: ${dropslotkey}`}>
										<List>
											{#each [...$V3Store.slots].filter(([ok, ov]) => !distro.drops.has(ok)) as [slotkey, v]}
												<Item
													on:SMUI:action={() => {
														swapDropSlotKey(distro, dropslotkey, slotkey);
													}}
												>
													<span>{slotkey}</span>
												</Item>
											{/each}
										</List>
									</Fakeselectmenu>
									<Button
										text={'Add Sheet'}
										bgColorClass={'bg-green-200'}
										on:click={() => {
											const newDistro = distro;
											const mySlot = $V3Store.slots.get(dropslotkey);
											if (mySlot === undefined) return;
											const newSheet = [...mySlot.sheets].filter(
												([ms, mv]) => !dropslotvalue.find((ev) => ev.key === ms)
											);
											if (newSheet.length === 0) return;
											const [newKey, newVal] = newSheet[0];
											newDistro.drops.set(dropslotkey, [
												...dropslotvalue,
												{ key: newKey, count: 1, freq: 1 }
											]);
											V3Store.update((p) => {
												return {
													...p,
													distros: [...p.distros.filter((d) => d != distro), newDistro]
												};
											});
										}}
									/>
								</div>
								<div class="rounded-xl p-1 flex flex-col justify-between w-4/6 items-center gap-1">
									{#each dropslotvalue as q}
										<div
											class="flex flex-row items-center justify-between w-full rounded-xl gap-1 p-1"
										>
											<div class="flex flex-row justify-between px-3 gap-1">
												<Fakeselectmenu bgColor={''} buttonText={`Sheet key: ${q.key}`}>
													<List>
														{#each [...($V3Store.slots.get(dropslotkey)?.sheets ?? [])].filter(([sk, sv]) => !dropslotvalue.find((x) => x.key === sk)) as [sheetkey, v]}
															<Item
																on:SMUI:action={() =>
																	swapdropsheetkey(distro, dropslotkey, q, sheetkey)}
															>
																<span>{sheetkey}</span>
															</Item>
														{/each}
													</List>
												</Fakeselectmenu>
											</div>
											<div class="flex flex-row justify-between items-center px-3 gap-1">
												<span class="h-min text-center">NUM</span>
												<Numberinput
													val={q.count}
													step={1}
													max={99}
													min={1}
													on:change={(e) => {
														const newDistro = distro;
														const newDropSheets = newDistro.drops.get(dropslotkey);
														if (newDropSheets === undefined) return;
														newDistro.drops.set(dropslotkey, [
															...newDropSheets.filter((ds) => ds.key !== q.key),
															// @ts-ignore
															{ key: q.key, count: parseInt(e.currentTarget.value), freq: q.freq }
														]);
														V3Store.update((p) => {
															return {
																...p,
																distros: [...p.distros.filter((d) => d != distro), newDistro]
															};
														});
														return null;
													}}
												/>
											</div>
											<div class="flex flex-row justify-between items-center px-3 gap-1">
												<span class="h-min text-center">FREQ</span>
												<Numberinput
													val={q.freq}
													step={0.1}
													max={1}
													min={0}
													on:change={(e) => {
														const newDistro = distro;
														const newDropSheets = newDistro.drops.get(dropslotkey);
														if (newDropSheets === undefined) return;
														newDistro.drops.set(dropslotkey, [
															...newDropSheets.filter((ds) => ds.key !== q.key),
															// @ts-ignore
															{ key: q.key, count: q.count, freq: parseFloat(e.currentTarget.value) }
														]);
														V3Store.update((p) => {
															return {
																...p,
																distros: [...p.distros.filter((d) => d != distro), newDistro]
															};
														});
														return null;
													}}
												/>
											</div>
											<Button
												text={'Delete'}
												bgColorClass={'bg-red-400'}
												on:click={() => {
													const newDistro = distro;
													const thisDrop = newDistro.drops.get(dropslotkey);
													if (thisDrop === undefined) return;
													const newDrop = thisDrop.filter(({ key }) => key !== q.key);
													newDistro.drops.set(dropslotkey, newDrop);
													V3Store.update((p) => {
														return {
															...p,
															distros: [...p.distros.filter((d) => d != distro), newDistro]
														};
													});
												}}
											/>
										</div>
									{/each}
								</div>
								<Button
									text={'Delete'}
									bgColorClass={'bg-red-400'}
									on:click={() => {
										const newDistro = distro;
										newDistro.drops.delete(dropslotkey);
										V3Store.update((p) => {
											return {
												...p,
												distros: [...p.distros.filter((d) => d != distro), newDistro]
											};
										});
									}}
								/>
							</div>
						{/each}
					</div>
				</div>
			</div>
			<div class="rounded-xl flex p-1 flex-row justify-between">
				<span>FREQ</span>
				<Numberinput
					val={distro.freq}
					step={0.1}
					max={1}
					min={0}
					on:change={(e) => {
						V3Store.update((p) => {
							return {
								...p,
								distros: [
									...p.distros.filter((d) => d != distro),
									// @ts-ignore
									{ ...distro, freq: parseFloat(e.currentTarget.value) }
								]
							};
						});
					}}
				/>
			</div>
		</div>
	{/each}
	<Button
		bgColorClass={'bg-green-200'}
		text={'ADD NEW DISTRO'}
		on:click={() => {
			V3Store.update((p) => {
				return {
					...p,
					distros: [
						...p.distros,
						{
							slots: new Map([]),
							drops: new Map([]),
							freq: 1
						}
					]
				};
			});
		}}
	/>
</section>
