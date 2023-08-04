<script lang="ts">
    import Mod from "./Mod.svelte";

    export let modList;
</script>

{#each modList as mod (mod.json.modId)}
    <Mod mod={mod.json} civbuilder={mod.civbuilder}/>
{:else}
    <article class="message is-info">
        <div class="message-body">
            No results.
        </div>
    </article>
{/each}
