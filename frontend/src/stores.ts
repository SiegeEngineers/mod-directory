import {derived, Readable, Writable, writable} from "svelte/store";
import {getSingleModId, MOD_CATEGORIES} from "./helpers";

export const searchTermTmp: Writable<string> = writable('');
export const searchTerm: Writable<string> = writable('');
export const sortMethod: Writable<string> = writable('createDate');
export const sortDirection: Writable<string> = writable('DESC');
export const queryPage: Writable<number> = writable(1);
export const modCategories: Writable<number[]> = writable(MOD_CATEGORIES.map(value => value.id));
export const singleModId: Writable<number | null> = writable(getSingleModId());
export const excludeCivbuilder: Writable<boolean> = writable(true);
export const compactMode: Writable<boolean> = writable(false);

export const reloadTriggers: Readable<string> = derived([searchTerm, sortMethod, sortDirection, queryPage, singleModId, modCategories, excludeCivbuilder],
    ([$searchTerm, $sortMethod, $sortDirection, $queryPage, $singleModId, $modCategories, $excludeCivbuilder]) =>
        `${$searchTerm}|${$sortMethod}|${$sortDirection}|${$queryPage}|${$singleModId}|${$modCategories.join(',')}|${$excludeCivbuilder}`);
