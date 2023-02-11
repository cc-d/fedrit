export interface Platform {
    id?: string;
    name: string;
    domain: string;
    createdAt?: string;
    updatedAt?: string;
}

export interface PlatformUser {
    id?: string;
    platform?: Platform;
    originUsername?: string;
    createdAt?: string;
    updatedAt?: string;
    username: string;
    password?: string;
    token?: string;
}

export interface Community {
    id?: string;
    communityType?: "SUB" | "IMGBOARD" | "FORUM";
    platform?: number | string;
    name?: string;
    createdAt?: string;
    updatedAt?: string;
}

