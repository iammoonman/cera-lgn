<script lang="ts">
	import Badge from '../utilities/badge.svelte';
	import Button from '../utilities/button.svelte';
	import Select, { Option } from '@smui/select';
	import { V3Store } from './stores';
	import Numberinput from '../utilities/numberinput.svelte';
	let distros: {
		slots: Map<string, number>;
		drops: Map<string, { key: string; count: number; freq: number }[]>;
		freq: number;
	}[];
	let outerslots: Map<
		string,
		{
			flags: ('foil' | 'duplicate_control')[];
			options: {
				struct: Map<string, number>;
				freq: number;
			}[];
			sheets: Map<string, (string | string[])[]>;
		}
	>;
	V3Store.subscribe((v) => {
		distros = v.distros;
		outerslots = v.slots;
	});
	let val = '';
</script>

<section id="distros" class="rounded-xl p-1 grid gap-1">
	DISTROS
	{#each distros as distro}
		<div class="rounded-xl p-1 flex flex-col gap-1 outline-dotted outline-slate-800">
			<div class="rounded-xl p-1 flex flex-row justify-between">
				<span>DISTRO</span>
				<Button text={'Delete'} bgColorClass={'bg-red-400'} />
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
								const filtered = [...outerslots].filter(([o, r]) => !distro.slots.has(o));
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
						{#each [...distro.slots] as [slotkey, numberinslot]}
							<div class="rounded-xl p-1 flex justify-around place-items-center">
								<Select
									label="Slot key: {slotkey}"
									on:MDCSelect:change={(e) => {
										const newDistro = distro;
										const oldValue = newDistro.slots.get(slotkey) ?? 1;
										newDistro.slots.delete(slotkey);
										newDistro.slots.set(e.detail.value, oldValue);
										V3Store.update((p) => {
											return {
												...p,
												distros: [...p.distros.filter((d) => d != distro), newDistro]
											};
										});
									}}
								>
									{#each [...outerslots].filter(([o, r]) => !distro.slots.has(o)) as [otherslotkey, v]}
										<Option value={otherslotkey}>{otherslotkey}</Option>
									{/each}
								</Select>
								<span>
									NUM:
									<Numberinput
										val={numberinslot}
										step={1}
										min={1}
										on:change={(e) => {
											const newDistro = distro;
											// @ts-ignore
											newDistro.slots.set(slotkey, parseInt(e.currentTarget.value));
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
										newDistro.slots.delete(slotkey);
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
						<Button text={'Add Key'} bgColorClass={'bg-green-200'} />
					</div>
					<div class="flex flex-col gap-1 p-0">
						{#each [...distro.drops] as [s, v]}
							<div class="rounded-xl p-1 flex justify-around items-center">
								<div class="flex flex-col gap-1">
									<Select label="Slot key: {s}">
										{#each [...outerslots] as [slotkey, v]}
											<Option value={slotkey}>{slotkey}</Option>
										{/each}
									</Select>
									<Button text={'Add Sheet'} bgColorClass={'bg-green-200'} />
								</div>
								<div class="rounded-xl p-1 flex flex-col justify-between w-4/6 items-center gap-1">
									{#each v as q}
										<div
											class="flex flex-row items-center justify-between w-full rounded-xl gap-1 p-1"
										>
											<div class="flex flex-row justify-between px-3 gap-1">
												<Select label="Sheet key: {q.key}">
													{#each [...(outerslots.get(s)?.sheets ?? [])] as [sheetkey, v]}
														<Option value={sheetkey}>{sheetkey}</Option>
													{/each}
												</Select>
											</div>
											<div class="flex flex-row justify-between px-3 gap-1">
												<span class="h-min text-center">NUM</span>
												<Numberinput val={0} step={0.1} max={1} min={0} />
											</div>
											<div class="flex flex-row justify-between px-3 gap-1">
												<span class="h-min text-center">FREQ</span>
												<Numberinput val={0} step={0.1} max={1} min={0} />
											</div>
											<Button text={'Delete'} bgColorClass={'bg-red-400'} />
										</div>
									{/each}
								</div>
								<Button text={'Delete'} bgColorClass={'bg-red-400'} />
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
	<Button bgColorClass={'bg-green-200'} text={'ADD NEW DISTRO'} />
</section>
