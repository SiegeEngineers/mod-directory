<script lang="ts">
    import FilterInput from "./SearchInput.svelte";
    import Messages from "./Messages.svelte";
    import ModList from "./ModList.svelte";
    import SingleMod from "./SingleMod.svelte";
    import type {IMod, IPaginationInfo} from "./Interfaces";
    import Sorter from "./Sorter.svelte";
    import {singleModId} from "./stores";
    import Pagination from "./Pagination.svelte";
    import TagSelector from "./TagSelector.svelte";
    import LoadingProgress from "./LoadingProgress.svelte";
    import LoadingError from "./LoadingError.svelte";

    export let promise: Promise<{ modList, paginationInfo }>;
    let result: { modList, paginationInfo };
    let modList: IMod[] = [];
    let paginationInfo: IPaginationInfo = {total: 0, filtered: 0, page: 0, pageSize: 0};

    $: updateResult(promise);

    async function updateResult(promise) {
		result = await promise;
        modList = result.modList;
        paginationInfo = result.paginationInfo;
	}
</script>

<section class="section">
    <div class="container">
        <Messages {modList}/>
        {#if $singleModId}
            {#await promise}
                <LoadingProgress/>
            {:then resolved}
                <SingleMod modList="{resolved.modList}"/>
            {:catch error}
                <LoadingError/>
            {/await}
        {:else}
            <Pagination page={paginationInfo.page} pageSize={paginationInfo.pageSize} total={paginationInfo.filtered}/>
            <TagSelector/>
            <div class="columns is-desktop">
                <div class="column is-three-fifths-widescreen">
                    <FilterInput filteredCount={paginationInfo.filtered}/>
                </div>
                <div class="column">
                    <Sorter/>
                </div>
            </div>
            {#await promise}
                <LoadingProgress/>
            {:then resolved}
                <ModList modList="{resolved.modList}"/>
            {:catch error}
                <LoadingError/>
            {/await}
            <Pagination page={paginationInfo.page} pageSize={paginationInfo.pageSize} total={paginationInfo.filtered}/>
        {/if}
    </div>
</section>