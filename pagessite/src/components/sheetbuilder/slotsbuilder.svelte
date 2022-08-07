<script lang="ts">
	import Switch from '@smui/switch';
	import Badge from '../utilities/badge.svelte';
	import Button from '../utilities/button.svelte';
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
	let keyColors = new Map();
	let colors: string[] = ['green', 'blue', 'red', 'orange', 'purple'];
	V3Store.subscribe((v) => {
		slots = v.slots;
		keyColors = new Map(Object.keys(v.slots).map((k) => [k, colors.pop()]));
	});
</script>

<section id="slots" class="rounded-xl p-1 grid gap-1">
	SLOTS
	{#each [...slots] as s}
		<div class="rounded-xl p-1 grid grid-cols-1 gap-1">
			<div class="rounded-xl p-1 flex flex-row justify-between">
				<span>SLOT: <Badge text={s[0]} bgcolor={keyColors.get(s[0])} /></span>
				<Button text={'Delete'} bgColorClass={'bg-red-400'} />
			</div>
			<div class="rounded-xl p-1 flex flex-row justify-around">
				<div class="flex justify-between items-center w-max">
					<span class="h-min">foil</span>
					<Switch
						color="primary"
						on:SMUISwitch:change={(e) =>
							e.detail.selected
								? s[1].flags.push('foil')
								: (s[1].flags = s[1].flags.filter((f) => f !== 'foil'))}
					/>
				</div>
				<div class="flex justify-between items-center w-max">
					<span class="h-min">duplicate_control</span>
					<Switch
						color="primary"
						on:SMUISwitch:change={(e) =>
							e.detail.selected
								? s[1].flags.push('duplicate_control')
								: (s[1].flags = s[1].flags.filter((f) => f !== 'duplicate_control'))}
					/>
				</div>
			</div>
			<div class="grid grid-cols-[120px_minmax(100px,_1fr)] gap-1">
				<div class="grid grid-rows-2 rounded-xl h-min mt-auto mb-auto p-1">
					<span class="h-min text-center">OPTIONS</span>
					<Button text={'New Option'} bgColorClass={'bg-green-200 whitespace-nowrap'} />
				</div>
				<div class="rounded-xl p-1 grid gap-1">
					{#each s[1].options as o}
						<div class="rounded-xl p-1 grid grid-cols-[120px_minmax(100px,_1fr)] gap-1">
							<div
								class="rounded-xl p-1 flex flex-col justify-between h-min items-center gap-1 my-auto"
							>
								<div class="flex flex-row justify-between w-full px-3">
									<span class="h-min text-center">FREQ</span>
									<input
										type="number"
										value={0}
										step={0.1}
										max={1}
										min={0}
										class="rounded-sm w-10"
									/>
								</div>
								<Button text={'New Slot'} bgColorClass={'bg-green-200'} />
							</div>
							<div class="grid grid-cols-1 gap-1 h-min">
								{#each [...o.struct] as st}
									<div class="rounded-xl p-1 flex justify-around items-center">
										<span class="h-min text-center">KEY: {st[0]}</span>
										<span class="h-min text-center">
											NUM:
											<input type="number" value={1} step={1} min={1} class="rounded-sm w-10" />
										</span>
										<Button text={'Delete'} bgColorClass={'bg-red-400'} />
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
					{#each [...s[1].sheets] as sh}
						<div class="rounded-xl flex flex-row justify-between p-1 items-center gap-1">
							<span class="h-min text-center mr-auto">KEY: {sh[0]}</span>
							<Button text={'View'} bgColorClass={'bg-blue-400'} />
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
