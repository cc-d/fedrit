export interface Platform {
    id?: string;
    name?: string;
    domain?: string;
    createdAt?: string;
    updatedAt?: string;
    host?: boolean;
}

export interface PlatformUser {
    id?: string;
    platform?: Platform;
    originUsername: string;
    createdAt?: string;
    updatedAt?: string;
    username: string;
    password?: string;
    token?: string;
}

export interface Community {
    id?: string;
    platform: Platform;
    communityType?: "SUB" | "IMGBOARD" | "FORUM";
    name?: string;
    createdAt?: string;
    updatedAt?: string;
}

export interface Post {
    id?: string;
    author: PlatformUser;
    community: Community;
    platform: Platform;
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
    post: Post;
    postId?: any;
    platform?: any;
    createdAt?: string;
    updatedAt?: string;
}

export interface UserToken {
    id?: string;
    user: PlatformUser;
    platform: Platform;
    token?: string;
}

