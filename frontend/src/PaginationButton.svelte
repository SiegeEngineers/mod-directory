<script type="ts">
    import {queryPage} from "./stores";

    export let label: string;
    export let page: number;
    export let cssClass: string;

    const callback = () => {
        queryPage.set(page);
    }
</script>

<span class="{cssClass}" aria-label="Goto page {page}" on:click={callback}>{label}</span>

<style>
    span {
        cursor: pointer;
    }
</style>