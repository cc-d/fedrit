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
    username: string;
    password?: string;
    token?: string;
}

