<script lang="ts">
    import LoadingProgress from "./LoadingProgress.svelte";
    import Mod from "./Mod.svelte";
    import type {IMod} from "./Interfaces";
    import {singleModId} from "./stores";

    const loadHistory = async () => {
        let json;
        let response;
        const filename = '/api/v1/mod/' + $singleModId + '/history';
        response = await fetch(filename);
        json = await response.json();
        if (response.ok) {
            let modEntries = json.modEntries;
            return modEntries.map(e => JSON.parse(e.json_str));
        } else {
            throw new Error("Fetching mod history failed");
        }
    };

    let promise: Promise<{ modList }>;


    export let modList: IMod[];
    $: filteredModList = modList ? modList.filter(mod => mod.modId === $singleModId) : [];
    $: historyPromise = loadHistory();
</script>

{#if modList}
    {#await historyPromise}
        <LoadingProgress/>
    {:then resolved}
        {#each filteredModList as mod (mod.modId)}
            <Mod short={false} extraInfo={true} {mod} history="{resolved}"/>
        {/each}
    {/await}
{:else}
    <LoadingProgress/>
{/if}
