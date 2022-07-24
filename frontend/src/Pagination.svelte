<script type="ts">
    import PaginationButton from "./PaginationButton.svelte";

    export let total: number;
    export let page: number;
    export let pageSize: number;
    $: lastPage = Math.ceil(total / pageSize);

</script>

<nav class="pagination is-centered" aria-label="pagination">
    {#if page > 1}
        <PaginationButton cssClass="pagination-previous" label="Previous" page={page-1}/>
    {:else}
        <span class="button is-static pagination-previous">Previous</span>
    {/if}
    {#if page < lastPage}
        <PaginationButton cssClass="pagination-next" label="Next page" page={page+1}/>
    {:else}
        <span class="button is-static pagination-next">Next page</span>
    {/if}
    <ul class="pagination-list">
        <li>
            {#if page === 1}
                <PaginationButton cssClass="pagination-link is-current" label="1" page={1}/>
            {:else}
                <PaginationButton cssClass="pagination-link" label="1" page={1}/>
            {/if}
        </li>
        {#if page > 2}
            <li><span class="pagination-ellipsis">&hellip;</span></li>
            <li>
                <PaginationButton cssClass="pagination-link" label="{page-1}" page={page-1}/>
            </li>
        {/if}
        {#if page > 1 && page < lastPage}
            <li>
                <PaginationButton cssClass="pagination-link is-current" label="{page}" page={page}/>
            </li>
        {/if}
        {#if page < lastPage - 1}
            <li>
                <PaginationButton cssClass="pagination-link" label="{page+1}" page={page+1}/>
            </li>
            <li><span class="pagination-ellipsis">&hellip;</span></li>
        {/if}
        <li>
            {#if lastPage > 1}
                {#if page === lastPage}
                    <PaginationButton cssClass="pagination-link is-current" label="{lastPage}" page={lastPage}/>
                {:else}
                    <PaginationButton cssClass="pagination-link" label="{lastPage}" page={lastPage}/>
                {/if}
            {/if}
        </li>
    </ul>
</nav>