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

    export let modList: IMod[];
    export let paginationInfo: IPaginationInfo;
</script>

<section class="section">
    <div class="container">
        <Messages {modList}/>
        {#if $singleModId}
            <SingleMod {modList}/>
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
            <ModList modList={modList}/>
            <Pagination page={paginationInfo.page} pageSize={paginationInfo.pageSize} total={paginationInfo.filtered}/>
        {/if}
    </div>
</section>