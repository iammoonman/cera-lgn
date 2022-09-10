<script lang="ts">
	import Blackmana from './blackmana.svelte';
	import Bluemana from './bluemana.svelte';
	import Diamondmana from './diamondmana.svelte';
	import Dps from './dps.svelte';
	import Fourmana from './fourmana.svelte';
	import Greenmana from './greenmana.svelte';
	import Onemana from './onemana.svelte';
	import Redmana from './redmana.svelte';
	import Threemana from './threemana.svelte';
	import Twomana from './twomana.svelte';
	import Whitemana from './whitemana.svelte';
	import Zeromana from './zeromana.svelte';

	export let symbol_name: string;
</script>

<div>
	{#if symbol_name === 'DPS'}
		<Dps />
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
		height: 14px;
		width: 14px;
	}
</style>
