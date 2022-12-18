<script lang="ts">
    import type {IMod, IModListEntry} from "./Interfaces";
    import {singleModId} from "./stores";

    const calculateNotFound = (list: IModListEntry[] | undefined, id: number | null) => {
        if (!list) {
            return false;
        }
        if (id === null) {
            return false;
        }
        return list.filter(mod => mod.json.modId === $singleModId).length === 0;
    }
    export let modList: IModListEntry[];
    $: modNotFound = calculateNotFound(modList, $singleModId);

    const clickHandler = () => {
        singleModId.set(null);
    }
</script>

{#if modNotFound}
    <article class="message is-danger" id="not-found-alert">
        <div class="message-header">
            <p>Not found</p>
        </div>
        <div class="message-body">
            There currently is no known mod with id {$singleModId}.
        </div>
    </article>
{:else if $singleModId}
    <article class="message is-info" id="single-mod-alert">
        <div class="message-body">
            You are viewing a single mod. <a href="/" on:click|preventDefault={clickHandler}>Show all mods</a>
        </div>
    </article>
{/if}
