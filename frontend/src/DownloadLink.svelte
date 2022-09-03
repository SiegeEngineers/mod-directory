<script lang="ts">
    export let fileUrl = '';
    export let modFileSize = 0;
    export let className = 'card-footer-item';
</script>

{#if fileUrl.startsWith('#')}
    <span title="Sorry, could not get download URL"
          class="{className}">Download ({(modFileSize / 1024 / 1024).toFixed(2)} MiB)</span>
{:else}
    <a href="{fileUrl}" class="{className}">Download ({(modFileSize / 1024 / 1024).toFixed(2)} MiB)</a>
{/if}
