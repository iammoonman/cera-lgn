<script lang="ts">
	export let val: number;
    export let step: number;
    export let max: number = 999999;
    export let min: number = -999999;
</script>

<input type="number" value={val} step={step} max={max} min={min} class="rounded-sm p-1" on:change />
