<script lang="ts">
	export let text: string;
	export let bgcolor: string;
</script>

<span
	class="rounded-sm font-semibold px-3 text-center shadow border-slate-200 border"
	style="background-color: {bgcolor};"
>
	{text}
</span>
