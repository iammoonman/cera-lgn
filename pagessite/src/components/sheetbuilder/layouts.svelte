<script lang="ts">
	import { V3Store } from './stores';
	// $V3Store;
	// Small card
	// For each slot, show how many cards are taken
	const f = (d: {
		slots: Map<string, number>;
		drops: Map<
			string,
			{
				key: string;
				count: number;
				freq: number;
			}[]
		>;
		freq: number;
	}) => {
		let out: string[][] = [];
		// recursive func that calls next option, then next slot
		const recur = (sk: string[], long: string[]) => {
			// pop from sk
			const key = sk.at(-1);
			if (key === undefined) {
				// if sk === [], push to out
				out.push(long);
				return;
			}
			const slot = $V3Store.slots.get(key);
			// for options in slot
			slot?.options.forEach((x) => {
				const temp = long;
                const hold: string[] = [];
				// append recur to long
				[...x.struct].forEach(([yk, yv]) => {
					[...Array(yv)].forEach(() => hold.push(yk));
				});
				recur(sk.slice(0, -1), temp.concat(hold));
			});
		};
		recur([...d.slots.keys()], []);
		return out;
	};
</script>

<div class="flex flex-col gap-1 h-max">
	{#each [...$V3Store.distros] as d}
		{#each f(d) as r}
			<div class="flex flex-row gap-1">
				{#each r as c}
					<div class="card" style={`background-color: #${c};`} />
				{/each}
			</div>
		{/each}
	{/each}
</div>

<style>
	.card {
		aspect-ratio: 336 / 468;
		width: 33px;
		border-radius: 3.5% / 4.75%;
		box-shadow: 0 0 3px black;
		background-color: beige;
	}
</style>
