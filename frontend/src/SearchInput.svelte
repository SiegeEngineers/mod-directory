<script lang="ts">
    import {searchTerm, searchTermTmp} from "./stores";

    export let filteredCount = 0;

    const callback = () => {
        $searchTerm = $searchTermTmp;
    }
</script>

<form on:submit|preventDefault={callback}>
    <div class="field has-addons">
        <p class="control">
                <span class="button is-static is-rounded">
                    {filteredCount}
                </span>
        </p>
        <p class="control is-flex-grow-1">
            <input class="input is-rounded" type="text" id="searchInput" placeholder="Search..."
                   bind:value={$searchTermTmp}>
        </p>
        <p class="control">
            <button class="button is-rounded" type="submit">
                Search
            </button>
        </p>
    </div>
</form>
