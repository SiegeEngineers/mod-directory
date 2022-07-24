export const resetTitleAndUrl = () => {
    const title = 'Mod Directory | Siege Engineers';
    window.history.pushState({}, title, window.location.protocol + '//' + window.location.host);
    document.title = title;
}

export const updateTitleAndUrl = (modId: number) => {
    const title = 'Mod ' + modId + ' | Siege Engineers';
    window.history.pushState({}, title, window.location.protocol + '//' + window.location.host + '/' + modId);
    document.title = title;
}

export const getSingleModId = () => {
    if (window.location.pathname === '/') {
        return null;
    }
    const items = window.location.pathname.split('/');
    return parseInt(items[1]);
}

export const MOD_CATEGORIES = [
    {"id": 9, "name": 'Artificial Intelligence'},
    {"id": 10, "name": 'Campaign'},
    {"id": 11, "name": 'Data Mod'},
    {"id": 12, "name": 'Graphics'},
    {"id": 13, "name": 'Movie'},
    {"id": 14, "name": 'Music'},
    {"id": 15, "name": 'Random Maps'},
    {"id": 16, "name": 'Scenarios'},
    {"id": 17, "name": 'Sounds'},
    {"id": 18, "name": 'Speech'},
    {"id": 19, "name": 'Taunt'},
    {"id": 20, "name": 'Terrain'},
    {"id": 21, "name": 'Menu Background'},
    {"id": 22, "name": 'User Interface'},
    {"id": 23, "name": 'Text'},
    {"id": 26, "name": 'Other'},
]
