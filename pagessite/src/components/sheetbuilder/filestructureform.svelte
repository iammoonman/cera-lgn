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
	import Button from '../utilities/button.svelte';
	import { V3Store } from './stores';
	V3Store.subscribe((v) => {
		distros = v.distros;
		headers = { full_name: v.full_name, default_set: v.default_set };
		slots = v.slots;
	});
</script>

<section id="headers" class="rounded-xl bg-yellow-200 grid grid-cols-1 p-1 gap-1">
	HEADERS
	<div class="rounded-xl bg-yellow-400 flex flex-row justify-between">
		<label for="full_name" class="p-2">Set Full Name</label>
		<input id="full_name" value={''} class="rounded-sm m-1" />
	</div>
	<div class="rounded-xl bg-yellow-400 flex flex-row justify-between">
		<label for="custom_set" class="p-2">Custom Set Code</label>
		<input id="custom_set" value={''} class="rounded-sm m-1" />
	</div>
	<div class="rounded-xl bg-yellow-400 flex flex-row justify-between">
		<label for="default_set" class="p-2">Default Set Code</label>
		<input id="default_set" value={''} class="rounded-sm m-1" />
	</div>
</section>
<section id="distros" class="rounded-xl bg-yellow-200 p-1 grid gap-1">
	DISTROS
	{#each distros as d}
		<div class="rounded-xl bg-yellow-400 p-1 flex flex-col gap-1">
			<div class="rounded-xl bg-yellow-500 p-1 flex flex-row justify-between">
				<span>DISTRO</span>
				<Button text={'Delete'} bgColorClass={'bg-red-400'} />
			</div>
			<div class="rounded-xl bg-yellow-600 p-1">
				<span>SLOTS</span>
				<div class="grid grid-cols-1 gap-1">
					{#each Array.from(Object.entries(d.slots)) as s}
						<div class="rounded-xl bg-yellow-800 p-1 flex justify-around">
							<span>KEY: {s[0]}</span>
							<span>NUM: {s[1]}</span>
							<Button text={'Add'} bgColorClass={'bg-green-200'} />
							<Button text={'Subtract'} bgColorClass={'bg-blue-200'} />
							<Button text={'Delete'} bgColorClass={'bg-red-400'} />
						</div>
					{/each}
					<div class="rounded-xl bg-yellow-900 p-1 flex justify-around w-40">
						<span>KEY: A</span>
						<Button text={'Add'} bgColorClass={'bg-green-200'} />
					</div>
				</div>
			</div>
			<div class="rounded-xl bg-yellow-600 p-1">
				<span>DROPS</span>
				<div class="grid grid-cols-1 gap-1">
					{#each Array.from(Object.entries(d.drops)) as s}
						<div class="rounded-xl bg-yellow-800 p-1 flex justify-around">
							<span>KEY: {s[0]}</span>
							<div class="rounded-xl bg-yellow-900 p-1 flex justify-between w-4/6">
								{#each s[1] as q}
									<span>SHEET: {q.key}</span>
									<span>NUM: {q.count}</span>
									<span>FREQ: {q.freq}</span>
									<Button text={'Add'} bgColorClass={'bg-green-200'} />
									<Button text={'Subtract'} bgColorClass={'bg-blue-200'} />
									<Button text={'Delete'} bgColorClass={'bg-red-400'} />
								{/each}
							</div>
						</div>
					{/each}
					<div class="rounded-xl bg-yellow-900 p-1 flex justify-around w-40">
						<span>KEY: A</span>
						<Button text={'Add'} bgColorClass={'bg-green-200'} />
					</div>
				</div>
			</div>
			<div class="rounded-xl bg-yellow-600 p-1 flex flex-row justify-between">
				<span>FREQ</span>
				<input type="number" value={0} step={0.1} max={1} min={0} class="rounded-sm" />
			</div>
		</div>
	{/each}
	<span class="rounded-lg bg-yellow-400 p-1">ADD NEW DISTRO</span>
</section>
<section id="slots" class="rounded-xl bg-yellow-200 p-1">
	SLOTS
	<div class="rounded-xl bg-yellow-400 p-1">
		{#each Object.entries(slots) as s}
			<div class="rounded-xl bg-yellow-500 p-1 grid grid-cols-1 gap-1">
				<div class="rounded-xl bg-yellow-500 p-1 flex flex-row justify-between">
					<span>SLOT {s[0]}</span>
					<Button text={'Delete'} bgColorClass={'bg-red-400'} />
				</div>
				<div class="rounded-xl bg-yellow-600 p-1">
					<div>
						<input type="checkbox" value="foil" name="foil" />
						<label for="foil">foil</label>
					</div>
					<div>
						<input type="checkbox" value="duplicate_control" name="duplicate_control" />
						<label for="duplicate_control">duplicate_control</label>
					</div>
				</div>
				<div class="rounded-xl bg-yellow-600 p-1">
					<span>OPTIONS</span>
					<div>
						{#each s[1].options as o}
							<div class="rounded-xl bg-yellow-700">
								OPTION
								<div class="grid grid-cols-1 gap-1">
									{#each Array.from(Object.entries(o.struct)) as st}
										<div class="rounded-xl bg-yellow-800 p-1 flex justify-around">
											<span>KEY: {st[0]}</span>
											<span>NUM: {st[1]}</span>
											<Button text={'Add'} bgColorClass={'bg-green-200'} />
											<Button text={'Subtract'} bgColorClass={'bg-blue-200'} />
											<Button text={'Delete'} bgColorClass={'bg-red-400'} />
										</div>
									{/each}
									<div class="rounded-xl bg-yellow-900 p-1 flex justify-around w-40">
										<span>KEY: b</span>
										<Button text={'Add'} bgColorClass={'bg-green-200'} />
									</div>
								</div>
								<div class="rounded-xl bg-yellow-800 p-1 flex flex-row justify-between">
									<span>FREQ</span>
									<input type="number" value={0} step={0.1} max={1} min={0} class="rounded-sm" />
								</div>
							</div>
						{/each}
					</div>
				</div>
				<div class="rounded-xl bg-yellow-600 p-1 grid gap-1">
					SHEETS
					{#each Object.entries(s[1].sheets) as sh}
						<div class="rounded-xl bg-yellow-700 flex flex-row justify-between p-1">
							<span>KEY: {sh[0]}</span>
							<Button text={'View'} bgColorClass={'bg-blue-200'} />
						</div>
					{/each}
					<div class="rounded-xl bg-yellow-800 p-1 flex justify-around w-40">
						<span>KEY: b</span>
						<Button text={'Add'} bgColorClass={'bg-green-200'} />
					</div>
				</div>
			</div>
		{/each}
	</div>
</section>

<style>
	#distros {
		background-color: beige;
	}
	#headers {
		width: max-content;
	}
</style>
