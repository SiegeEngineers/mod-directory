<script lang="ts">
    import SorterButton from "./SorterButton.svelte";
</script>

<div class="buttons has-addons is-right">
    <button class="button" disabled>Order by</button>
    <SorterButton label="Created"/>
    <SorterButton label="Updated"/>
</div>
