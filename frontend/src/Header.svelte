<script lang="ts">
    import {singleModId} from "./stores";

    export let promise: Promise<{modList, lastUpdate, modCount}>;

    const clickHandler = () => {
        singleModId.set(null);
    }
</script>

<section class="hero is-warning is-bold">
    <div class="hero-body">
        <div class="container">
            <h1 class="title is-2">
                <img src="/img/SiegeEngineers.png" alt="Siege Engineers"/>
                <a href="/" on:click|preventDefault={clickHandler}>Mod Directory</a>
            </h1>
            <p class="subtitle">
                {#await promise}
                    Age of Empires II DE mod directory – … Mods Total
                {:then resolved}
                    Age of Empires II DE mod directory – {resolved.paginationInfo.total} Mods Total
                {/await}
            </p>
        </div>
    </div>
</section>
