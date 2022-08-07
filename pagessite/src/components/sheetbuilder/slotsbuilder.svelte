<script lang="ts">
	import Switch from '@smui/switch';
	import Badge from '../utilities/badge.svelte';
	import Button from '../utilities/button.svelte';
	import Numberinput from '../utilities/numberinput.svelte';
	let slots: Map<
		string,
		{
			flags: ('foil' | 'duplicate_control')[];
			options: {
				struct: Map<string, number>;
				freq: number;
			}[];
			sheets: Map<string, (string | string[])[]>;
		}
	> = new Map();
	import { V3Store } from './stores';
	V3Store.subscribe((v) => {
		slots = v.slots;
	});
</script>

<section id="slots" class="rounded-xl p-1 grid gap-1">
	SLOTS
	{#each [...slots] as [s_key, s_value]}
		<div class="rounded-xl p-1 grid grid-cols-1 gap-1">
			<div class="rounded-xl p-1 flex flex-row justify-between">
				<span>SLOT: {s_key}</span>
				<Button
					text={'Delete'}
					bgColorClass={'bg-red-400'}
					on:click={() => {
						const newSlots = slots;
						newSlots.delete(s_key);
						V3Store.update((oldstore) => {
							return {
								...oldstore,
								slots: newSlots
							};
						});
					}}
				/>
			</div>
			<div class="rounded-xl p-1 flex flex-row justify-around">
				<div class="flex justify-between items-center w-max">
					<span class="h-min">foil</span>
					<Switch
						color="primary"
						on:SMUISwitch:change={(e) => {
							const newFlags = e.detail.selected
								? [...s_value.flags, 'foil']
								: s_value.flags.filter((f) => f !== 'foil');
							const newSlots = slots;
							// @ts-ignore
							newSlots.set(s_key, { ...s_value, flags: newFlags });
							V3Store.update((oldstore) => {
								return {
									...oldstore,
									slots: newSlots
								};
							});
						}}
					/>
				</div>
				<div class="flex justify-between items-center w-max">
					<span class="h-min">duplicate_control</span>
					<Switch
						color="primary"
						on:SMUISwitch:change={(e) => {
							const newFlags = e.detail.selected
								? [...s_value.flags, 'duplicate_control']
								: s_value.flags.filter((f) => f !== 'duplicate_control');
							const newSlots = slots;
							// @ts-ignore
							newSlots.set(s_key, { ...s_value, flags: newFlags });
							V3Store.update((oldstore) => {
								return {
									...oldstore,
									slots: newSlots
								};
							});
						}}
					/>
				</div>
			</div>
			<div class="grid grid-cols-[120px_minmax(100px,_1fr)] gap-1">
				<div class="grid grid-rows-2 rounded-xl h-min mt-auto mb-auto p-1">
					<span class="h-min text-center">OPTIONS</span>
					<Button
						text={'New Option'}
						bgColorClass={'bg-green-200 whitespace-nowrap'}
						on:click={() => {
							const newOptions = { struct: new Map(), freq: 1 };
							const newSlot = s_value;
							newSlot.options.push(newOptions);
							const newSlots = slots;
							newSlots.set(s_key, newSlot);
							V3Store.update((oldstore) => {
								return {
									...oldstore,
									slots: newSlots
								};
							});
						}}
					/>
				</div>
				<div class="rounded-xl p-1 grid gap-1">
					{#each s_value.options as o}
						<div class="rounded-xl p-1 grid grid-cols-[120px_minmax(100px,_1fr)] gap-1">
							<div class="rounded-xl p-1 grid grid-cols-1 gap-1 w-max">
								<div class="flex flex-row justify-between w-min px-3 items-center gap-1">
									<span class="h-min text-center">FREQ</span>
									<Numberinput val={o.freq} step={0.1} max={1} min={0} />
								</div>
								<div class="flex flex-row flex-nowrap w-full gap-1">
									<Button
										text={'New Slot'}
										bgColorClass={'bg-green-200'}
										on:click={() => {
											const newSlots = slots;
											const newSlot = newSlots.get(s_key);
											if (newSlot === undefined) return;
											const myOptions = newSlot.options.filter((o2) => o2 !== o);
											o.struct.set('x', 1);
											newSlot.options = [...myOptions, o];
											newSlots.set(s_key, newSlot);
											V3Store.update((oldstore) => {
												return {
													...oldstore,
													slots: newSlots
												};
											});
										}}
									/>
									<Button
										text={'Delete'}
										bgColorClass={'bg-red-400'}
										on:click={() => {
											const newSlot = s_value;
											newSlot.options = newSlot.options.filter(o2 => o2 != o);
											const newSlots = slots;
											newSlots.set(s_key, newSlot);
											V3Store.update((oldstore) => {
												return {
													...oldstore,
													slots: newSlots
												};
											});
										}}
									/>
								</div>
							</div>
							<div class="grid grid-cols-1 gap-1 h-min">
								{#each [...o.struct] as [st, st_v]}
									<div class="rounded-xl p-1 flex justify-around items-center">
										<span class="h-min text-center">KEY: {st}</span>
										<span class="h-min text-center">
											NUM:
											<Numberinput val={st_v} step={1} min={1} />
										</span>
										<Button
											text={'Delete'}
											bgColorClass={'bg-red-400'}
											on:click={() => {
												const newSlots = slots;
												const newSlot = newSlots.get(s_key);
												if (newSlot === undefined) return;
												const myOptions = newSlot.options.filter((o2) => o2 !== o);
												o.struct.delete(st);
												newSlot.options = [...myOptions, o];
												newSlots.set(s_key, newSlot);
												V3Store.update((oldstore) => {
													return {
														...oldstore,
														slots: newSlots
													};
												});
											}}
										/>
									</div>
								{/each}
							</div>
						</div>
					{/each}
				</div>
			</div>
			<div class="grid grid-cols-[120px_minmax(100px,_1fr)] gap-1">
				<div class="grid grid-rows-2 rounded-xl h-min mt-auto mb-auto p-1">
					<span class="h-min text-center">SHEETS</span>
					<Button text={'New Sheet'} bgColorClass={'bg-green-200'} />
				</div>
				<div class="rounded-xl p-1 grid gap-1">
					{#each [...s_value.sheets] as [sh, sh_v]}
						<div class="rounded-xl flex flex-row justify-between p-1 items-center gap-1">
							<span class="h-min text-center mr-auto">KEY: {sh}</span>
							<Button text={'Edit'} bgColorClass={'bg-blue-400'} />
							<Button text={'Delete'} bgColorClass={'bg-red-400'} />
						</div>
					{/each}
				</div>
			</div>
		</div>
	{/each}
	<Button
		bgColorClass={'bg-green-200'}
		text={'ADD NEW SLOT'}
		on:click={() => {
			V3Store.update((oldstore) => {
				return {
					...oldstore,
					slots: new Map([...oldstore.slots, ['m', { flags: [], options: [], sheets: new Map() }]])
				};
			});
		}}
	/>
</section>
