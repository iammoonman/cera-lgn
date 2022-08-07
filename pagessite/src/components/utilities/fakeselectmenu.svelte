<script lang="ts">
	import type { MenuComponentDev } from '@smui/menu';
	import Menu from '@smui/menu';
    import Button from './button.svelte'
    export let buttonText:string;
    export let bgColor:string;
	let menu: MenuComponentDev;
</script>

<div style="min-width: 100px;">
	<Button on:click={() => menu.setOpen(true)} text={buttonText} bgColorClass={bgColor} />
	<Menu bind:this={menu}>
		<!-- <List>
			<Item on:SMUI:action={() => null}>
				<Text>Cut</Text>
			</Item>
			<Item on:SMUI:action={() => null}>
				<Text>Copy</Text>
			</Item>
			<Item on:SMUI:action={() => null}>
				<Text>Paste</Text>
			</Item>
			<Separator />
			<Item on:SMUI:action={() => null}>
				<Text>Delete</Text>
			</Item>
		</List> -->
        <slot></slot>
	</Menu>
</div>
