<script lang="ts">
	import Header from "./Header.svelte";
	import PageContent from "./PageContent.svelte";
	import Footer from "./Footer.svelte";
	import {resetTitleAndUrl, updateTitleAndUrl} from "./helpers";
	import {onDestroy} from "svelte";
	import {
		modCategories,
		queryPage,
		reloadTriggers,
		searchTerm,
		singleModId,
		sortDirection,
		sortMethod
	} from "./stores";

	const init = async () => {
		let json;
		let response;
		if ($singleModId) {
			const filename = "/api/v1/mod/" + $singleModId
			response = await fetch(filename);
			json = await response.json();
		} else {
			const filename = "/api/v1/mods"
			response = await fetch(filename, {
				method: 'POST',
				headers: {'Content-Type': 'application/json'},
				body: JSON.stringify({
					page: $queryPage,
					sortColumn: $sortMethod,
					sortDirection: $sortDirection,
					modCategories: $modCategories,
					searchTerm: $searchTerm
				})
			});
			json = await response.json();
		}

		if (response.ok) {
			let modEntries = json.modEntries;
			let modList = modEntries.map(e => ({json: JSON.parse(e.json_str), fileList: JSON.parse(e.fileList)}))
			let total = json.total
			let filtered = json.filtered
			let page = json.page;
			let pageSize = json.pageSize;
			let paginationInfo = {page, total, filtered, pageSize}
			return {modList, paginationInfo};
		} else {
			throw new Error("Fetching mods failed");
		}
	};

	let promise: Promise<{ modList, paginationInfo }>;


	const unsubscribeSingleModId = singleModId.subscribe(value => {
		if (value) {
			updateTitleAndUrl(value);
		} else {
			resetTitleAndUrl();
		}
	});

	onDestroy(unsubscribeSingleModId);


	const unsubscribeReloadTriggers = reloadTriggers.subscribe(value => {
		promise = init();
	});

	onDestroy(unsubscribeReloadTriggers);

</script>

<main>
	<Header {promise}/>
	<PageContent {promise}/>
	<Footer/>
</main>
