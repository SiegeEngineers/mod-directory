<script lang="ts">
    import DownloadLink from "./DownloadLink.svelte";
    import type {IMod} from "./Interfaces";
    import {compactMode, singleModId} from "./stores";
    import {afterUpdate} from "svelte";

    export let mod: IMod;
    export let fileList: string[] | null = null;
    export let history: IMod[] = undefined;
    let div;
    export let extraInfo: boolean = false;
    export let short: boolean = true;
    let displayShortToggle: boolean = false;
    $: classlist = short ? 'mod-description short' : 'mod-description';
    afterUpdate(() => {
        if (short && div && (div.scrollHeight != div.offsetHeight)) {
            displayShortToggle = true;
        }
    });
    const clickHandler = () => {
        singleModId.set(mod.modId);
    }
</script>

<div class="card">
    {#if $compactMode && !extraInfo}
        <div class="card-content slim">
            <div class="columns">
                <div class="column is-1">
                    {#if mod.imageUrls.length > 0}
                        <figure class="image is-16by9">
                            <img loading="lazy" src="{mod.imageUrls[0].imageThumbnail}" alt="Thumbnail">
                        </figure>
                    {/if}
                </div>
                <div class="column">
                    <a href="/{mod.modId}" on:click|preventDefault={clickHandler}><b>{mod.modName}</b></a>
                    <small>by {mod.creatorName}</small>
                    <br>
                    {#each mod.modTagNames as tag}
                        <span class="tag">{tag}</span>
                    {/each}
                </div>
                <div class="column is-narrow-tablet">
                    <a href="https://www.ageofempires.com/mods/details/{mod.modId}/" class="">View on
                        ageofempires.com</a>
                </div>
                <div class="column is-2-tablet">
                    <DownloadLink fileUrl={mod.fileUrl} modFileSize={mod.modFileSize} className=""/>
                </div>
                <div class="column is-narrow-tablet">
                    <span class="tag is-secondary" title="created: {mod.createDate}">C: {mod.createDate.substring(0, 10)}</span>
                <span class="tag is-secondary" title="updated: {mod.lastUpdate}">U: {mod.lastUpdate.substring(0, 10)}</span>
                </div>
                </div>
        </div>
    {:else}
        <div class="card-content">
            <div class="columns">
                <div class="column is-one-fifth">
                    {#if extraInfo}
                        {#each mod.imageUrls as imageUrl}
                            <figure class="image is-16by9">
                                <img loading="lazy" src="{imageUrl.imageThumbnail}" alt="Thumbnail">
                            </figure>
                        {/each}
                    {:else if mod.imageUrls.length > 0}
                        <figure class="image is-16by9">
                            <img loading="lazy" src="{mod.imageUrls[0].imageThumbnail}" alt="Thumbnail">
                        </figure>
                    {/if}
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
                        <img loading="lazy" alt="creator avatar" class="image is-24x24 avatar"
                             src="{mod.creatorAvatarUrl}"/>
                    </h4>
                    <div class={classlist} bind:this={div}>
                        {@html mod.modDescription}
                        {#if extraInfo}
                            <hr>
                            <h4 class="title is-5">File List</h4>
                            {#if fileList}
                                <pre>{#each fileList as line}{#if !line.endsWith('/')}{line + '\n'}{/if}{/each}</pre>
                            {:else}
                                <pre>currently not available.</pre>
                            {/if}
                            {#if mod.changeList}
                                <hr>
                                <h4 class="title is-5">Changelog</h4>
                                {@html mod.changeList}
                            {/if}
                        {/if}
                    </div>
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
                <span class="tag is-secondary" title="created: {mod.createDate}">C: {mod.createDate.substring(0, 10)}</span>
                <span class="tag is-secondary" title="updated: {mod.lastUpdate}">U: {mod.lastUpdate.substring(0, 10)}</span>
                <span class="tag is-info">{mod.downloads.toLocaleString('en-US')} Downloads</span>
            </p>
        </footer>
    {/if}
</div>
{#if history}
    <div class="card">
        <header class="card-header">
            <p class="card-header-title">
                Version History
            </p>
        </header>
        <div class="card-content">
            <div class="content">
                <table class="table is-hoverable">
                    <tr>
                        <th>Updated</th>
                        <th>Title</th>
                        <th>Download</th>
                    </tr>
                    {#each history as entry}
                        <tr>
                            <td>{entry.lastUpdate}</td>
                            <td>{entry.modName}</td>
                            <td>
                                <DownloadLink fileUrl={entry.fileUrl} modFileSize={entry.modFileSize} className=""/>
                            </td>
                        </tr>
                    {/each}
                </table>
            </div>
        </div>
    </div>
{/if}

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

    figure {
        margin-bottom: .5rem;
    }

    .card-footer-item {
        flex-wrap: wrap;
    }

    .card-content.slim {
        padding: 0 1em;
    }
</style>
