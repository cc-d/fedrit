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
    name?: string;
    createdAt?: string;
    updatedAt?: string;
    platform?: number | string;
}

export interface Post {
    id?: string;
    author?: number | string | null;
    community?: number | string;
    platform?: number | string;
    url?: string;
    title: string;
    text?: string;
    createdAt?: string;
    updatedAt?: string;
}

