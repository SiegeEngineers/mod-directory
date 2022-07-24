<script lang="ts">
    import LoadingProgress from "./LoadingProgress.svelte";
    import Mod from "./Mod.svelte";
    import type {IMod} from "./Interfaces";
    import {singleModId} from "./stores";

    export let modList: IMod[];
    $: filteredModList = modList ? modList.filter(mod => mod.modId === $singleModId) : [];
</script>

{#if modList}
    {#each filteredModList as mod (mod.modId)}
        <Mod short={false} extraInfo={true} {mod}/>
    {/each}
{:else}
    <LoadingProgress/>
{/if}
