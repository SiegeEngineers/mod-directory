<script type="ts">

    import {MOD_CATEGORIES} from "./helpers";
    import {modCategories} from "./stores";

    const toggle = (id: number) => {
        if ($modCategories.includes(id)) {
            $modCategories = $modCategories.filter(value => value !== id);
        } else {
            $modCategories = [...$modCategories, id];
        }
    }

</script>

<div class="columns is-desktop is-flex-wrap-wrap">
    {#each MOD_CATEGORIES as {id, name} (id)}
        <div class="column is-one-fifth-desktop">
            <label class="checkbox">
                <input type="checkbox" checked="{$modCategories.includes(id) ? 'checked' : ''}" on:click={()=>toggle(id)}>
                {name}
            </label>
        </div>
    {/each}
</div>

<style>
    .column {
        padding: 0;
    }

    .columns {
        padding-bottom: .5em;
    }
</style>