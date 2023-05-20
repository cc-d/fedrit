export interface Platform {
    id?: string;
    url?: string;
    createdAt?: string;
    updatedAt?: string;
    isHost?: boolean;
}

export interface PlatformUser {
    id?: string;
    platform?: Platform;
    platUsername?: string;
    createdAt?: string;
    updatedAt?: string;
    username?: string;
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

export interface PlatUserToken {
    id?: string;
    user: PlatformUser;
    platform: Platform;
    token?: string;
}

