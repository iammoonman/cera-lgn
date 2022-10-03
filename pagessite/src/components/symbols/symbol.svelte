<script lang="ts">
	import Blackmana from './blackmana.svelte';
	import Bluemana from './bluemana.svelte';
	import Diamondmana from './diamondmana.svelte';
	import Dps from './dps.svelte';
	import Ptm from './ptm_symbol.svelte'
	import Fourmana from './fourmana.svelte';
	import Greenmana from './greenmana.svelte';
	import Onemana from './onemana.svelte';
	import Redmana from './redmana.svelte';
	import Threemana from './threemana.svelte';
	import Twomana from './twomana.svelte';
	import Whitemana from './whitemana.svelte';
	import Zeromana from './zeromana.svelte';

	export let symbol_name: string;
	export let symbol_size: number;
</script>

<div style={`--size: ${symbol_size}px`}>
	{#if symbol_name === 'dps'}
		<Dps />
	{/if}
	{#if symbol_name === 'ptm'}
		<Ptm />
	{/if}
	{#if symbol_name === 'W'}
		<Whitemana />
	{/if}
	{#if symbol_name === 'U'}
		<Bluemana />
	{/if}
	{#if symbol_name === 'B'}
		<Blackmana />
	{/if}
	{#if symbol_name === 'R'}
		<Redmana />
	{/if}
	{#if symbol_name === 'G'}
		<Greenmana />
	{/if}
	{#if symbol_name === 'C'}
		<Diamondmana />
	{/if}
	{#if symbol_name === '0'}
		<Zeromana />
	{/if}
	{#if symbol_name === '1'}
		<Onemana />
	{/if}
	{#if symbol_name === '2'}
		<Twomana />
	{/if}
	{#if symbol_name === '3'}
		<Threemana />
	{/if}
	{#if symbol_name === '4'}
		<Fourmana />
	{/if}
</div>

<style>
	div {
		display: block;
		height: var(--size);
		width: var(--size);
	}
</style>
