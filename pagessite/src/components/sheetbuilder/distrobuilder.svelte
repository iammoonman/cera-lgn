<script lang="ts">
	import Badge from '../utilities/badge.svelte';
	import Button from '../utilities/button.svelte';
	import { V3Store } from './stores';
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
	V3Store.subscribe((v) => {
		distros = v.distros;
		keyColors = new Map(Object.keys(v.slots).map((k) => [k, colors.pop()]));
	});
	let keyColors = new Map();
	let colors: string[] = ['green', 'blue', 'red', 'orange', 'purple'];
</script>

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
