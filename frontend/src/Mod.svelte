<script lang="ts">
    import DownloadLink from "./DownloadLink.svelte";
    import type {IMod} from "./Interfaces";
    import {singleModId} from "./stores";
    import {afterUpdate} from "svelte";

    export let mod: IMod;
    let div;
    export let short: boolean = true;
    let displayShortToggle: boolean = false;
    $: classlist = short ? 'mod-description short' : 'mod-description';
    afterUpdate(() => {
        if (short && (div.scrollHeight != div.offsetHeight)) {
            displayShortToggle = true;
        }
    });
    const clickHandler = () => {
        singleModId.set(mod.modId);
    }
</script>

<div class="card">
    <div class="card-content">
        <div class="columns">
            <div class="column is-one-fifth">
                <figure class="image is-16by9">
                    <img loading="lazy" src="{mod.imageUrls[0].imageThumbnail}" alt="Thumbnail">
                </figure>
            </div>
            <div class="column">
                <h3 class="title is-4">
                    <a href="/{mod.modId}" on:click|preventDefault={clickHandler}>{mod.modName}</a>
                    {#each mod.modTagNames as tag}
                        <span class="tag">{tag}</span>
                    {/each}
                </h3>
                <h4 class="title is-6">
                    by {mod.creatorName}
                    <img loading="lazy" alt="creator avatar" class="image is-24x24 avatar" src="{mod.creatorAvatarUrl}"/>
                </h4>
                <div class={classlist} bind:this={div}>{@html mod.modDescription}</div>
                {#if displayShortToggle}
                <div class="short-toggle" on:click={()=>short = !short}>
                    {#if short}
                        <img class="arrow" alt="expand" src="/img/arrowdown.svg">
                    {:else}
                        <img class="arrow" alt="condense" src="/img/arrowup.svg">
                    {/if}
                </div>
                {/if}
            </div>
        </div>
    </div>
    <footer class="card-footer">
        <a href="https://www.ageofempires.com/mods/details/{mod.modId}/" class="card-footer-item">View on
            ageofempires.com</a>
        <DownloadLink fileUrl={mod.fileUrl} modFileSize={mod.modFileSize}/>
        <p class="card-footer-item">
            <span class="tag is-secondary" title="created">C: {mod.createDate.substring(0, 10)}</span>
            <span class="tag is-secondary" title="updated">U: {mod.lastUpdate.substring(0, 10)}</span>
            <span class="tag is-info">{mod.downloads.toLocaleString('en-US')} Downloads</span>
        </p>
    </footer>
</div>

<style>
    .card {
        margin-bottom: 1rem;
    }

    .avatar {
        display: inline-block;
        vertical-align: middle;
    }

    .mod-description.short {
        max-height: 200px;
        overflow: hidden;
    }

    .short-toggle {
        text-align: center;
        border-top: 1px solid #999;
        background: linear-gradient(#ccc, #fff);
    }

    .arrow {
        height: .8em;
    }

    .tag {
        margin-right: .5em;
    }
</style>
