<script lang="ts">
	let js = '';
	let distros: {
		slots: Record<string, number>;
		drops: Record<
			string,
			{
				key: string;
				count: number;
				freq: number;
			}[]
		>;
		freq: number;
	}[] = [];
	let headers = {};
	let slots: Record<
		string,
		{
			flags: ('foil' | 'duplicate_control')[];
			options: {
				struct: Record<string, number>;
				freq: number;
			}[];
			sheets: Record<string, (string | string[])[]>;
		}
	> = {};
	let keyColors = new Map();
	let colors: string[] = ['green', 'blue', 'red', 'orange', 'purple'];
	import Button from '../utilities/button.svelte';
	import { V3Store } from './stores';
	V3Store.subscribe((v) => {
		distros = v.distros;
		headers = { full_name: v.full_name, default_set: v.default_set };
		slots = v.slots;
		keyColors = new Map(Object.keys(v.slots).map((k) => [k, colors.pop()]));
	});
	import Switch from '@smui/switch';
	import Badge from '../utilities/badge.svelte';
</script>

<section id="headers" class="rounded-xl grid grid-cols-1 p-1 gap-1">
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
<section id="distros" class="rounded-xl p-1 grid gap-1">
	DISTROS
	{#each distros as d}
		<div class="rounded-xl p-1 flex flex-col gap-1">
			<div class="rounded-xl p-1 flex flex-row justify-between">
				<span>DISTRO</span>
				<Button text={'Delete'} bgColorClass={'bg-red-400'} />
			</div>
			<div class="rounded-xl p-1">
				<span>SLOTS</span>
				<div class="grid grid-cols-[100px_minmax(100px,_1fr)] gap-1">
					<div class="grid place-content-center">
						<Button text={'Add Key'} bgColorClass={'bg-green-200'} />
					</div>
					<div class="grid grid-cols-1 gap-1">
						{#each Array.from(Object.entries(d.slots)) as s}
							<div class="rounded-xl p-1 flex justify-around place-items-center">
								<span class="h-min text-center"
									>KEY: <Badge text={s[0]} bgcolor={keyColors.get(s[0])} /></span
								>
								<span
									>NUM: <input
										type="number"
										value={0}
										step={0.1}
										max={1}
										min={0}
										class="rounded-sm w-10"
									/></span
								>
								<Button text={'Delete'} bgColorClass={'bg-red-400'} />
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
						{#each Array.from(Object.entries(d.drops)) as s}
							<div class="rounded-xl p-1 flex justify-around items-center">
								<div class="flex flex-col gap-1">
									<span class="mr-auto ml-auto"
										>KEY: <Badge text={s[0]} bgcolor={keyColors.get(s[0])} /></span
									>
									<Button text={'Add Sheet'} bgColorClass={'bg-green-200'} />
								</div>
								<div class="rounded-xl p-1 flex flex-col justify-between w-4/6 items-center gap-1">
									{#each s[1] as q}
										<div
											class="flex flex-row items-center justify-between w-full rounded-xl gap-1 p-1"
										>
											<div class="flex flex-row justify-between px-3 gap-1">
												<span class="h-min text-center">SHEET: a</span>
											</div>
											<div class="flex flex-row justify-between px-3 gap-1">
												<span class="h-min text-center">NUM</span>
												<input
													type="number"
													value={0}
													step={0.1}
													max={1}
													min={0}
													class="rounded-sm w-10"
												/>
											</div>
											<div class="flex flex-row justify-between px-3 gap-1">
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
			<div class="rounded-xl p-1 flex flex-row justify-between">
				<span>FREQ</span>
				<input type="number" value={0} step={0.1} max={1} min={0} class="rounded-sm" />
			</div>
		</div>
	{/each}
	<Button bgColorClass={'bg-green-200'} text={'ADD NEW DISTRO'} />
</section>
<section id="slots" class="rounded-xl p-1 grid gap-1">
	SLOTS
	{#each Object.entries(slots) as s}
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
								{#each Array.from(Object.entries(o.struct)) as st}
									<div class="rounded-xl p-1 flex justify-around items-center">
										<span class="h-min text-center">KEY: {st[0]}</span>
										<span class="h-min text-center"
											>NUM: <input
												type="number"
												value={1}
												step={1}
												min={1}
												class="rounded-sm w-10"
											/></span
										>
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
					{#each Object.entries(s[1].sheets) as sh}
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
	<Button bgColorClass={'bg-green-200'} text={'ADD NEW SLOT'} />
</section>

<style>
</style>
