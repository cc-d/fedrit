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
    platform?: any;
}

export interface Post {
    id?: string;
    author?: any;
    community?: any;
    platform?: any;
    url?: string;
    title: string;
    text?: string;
    createdAt?: string;
    updatedAt?: string;
}

export interface Comment {
    id?: string;
    author?: any;
    community?: any;
    text?: string;
    post?: any;
    postId?: any;
    platform?: any;
    createdAt?: string;
    updatedAt?: string;
}

