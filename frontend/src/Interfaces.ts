export interface Image {
    "imageId": string
    "displayIndex": number
    "imageName": string
    "imageThumbnail": string
    "imageFileSize": string
}

export interface IMod {
    "modId": number
    "modName": string
    "modDescription": string
    "changeList": string
    "modType": string
    "modTagIds": number[]
    "modStatus": string
    "modVisibility": string
    "creatorName": string,
    "creatorAvatarUrl": string
    "createDate": string
    "lastUpdate": string
    "modFileSize": number
    "downloads": number
    "userFlagged": boolean
    "thumbnail": string
    "imageUrls": Image[]
    "modTagNames": string[]
    "fileUrl": string
}

export interface IPaginationInfo {
    total: number
    filtered: number
    page: number
    pageSize: number
}
