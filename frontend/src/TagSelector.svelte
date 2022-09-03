<script type="ts">

    import {MOD_CATEGORIES} from "./helpers";
    import {compactMode, modCategories} from "./stores";

    const toggle = (id: number) => {
        if ($modCategories.includes(id)) {
            $modCategories = $modCategories.filter(value => value !== id);
        } else {
            $modCategories = [...$modCategories, id];
        }
    }

    const selectAll = () => {
        $modCategories = MOD_CATEGORIES.map(value => value.id);
    }

    const clear = () => {
        $modCategories = [];
    }
    const toggleCompactMode = () => {
        $compactMode = !$compactMode;
    }

</script>

<div class="columns is-desktop is-flex-wrap-wrap">
    {#each MOD_CATEGORIES as {id, name} (id)}
        <div class="column is-one-fifth-desktop">
            <label class="checkbox">
                <input type="checkbox" checked="{$modCategories.includes(id) ? 'checked' : ''}"
                       on:click={()=>toggle(id)}>
                {name}
            </label>
        </div>
    {/each}
    <div class="column is-one-fifth-desktop">
        <button class="button is-small" on:click={selectAll}>select all</button>
    </div>
    <div class="column is-one-fifth-desktop">
        <button class="button is-small" on:click={clear}>clear all</button>
    </div>
    <div class="column is-one-fifth-desktop">
        <label class="checkbox">
            <input type="checkbox" checked="{$compactMode}"
                   on:click={()=>toggleCompactMode()}>
            Compact View
        </label>
    </div>
</div>

<style>
    .column {
        padding: 0;
    }

    .columns {
        padding-bottom: .5em;
    }
</style>