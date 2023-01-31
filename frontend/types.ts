export interface PlatformUserSerializer {
    uuid?: string;
    platform?: number | string;
    username: string;
    password: string;
    token?: string;
}

