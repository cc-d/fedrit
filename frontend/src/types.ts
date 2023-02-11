export interface PlatformUser {
    id?: string;
    platform?: number | string;
    originUsername?: string;
    username: string;
    password?: string;
    token?: string;
}

export interface Platform {
    id?: string;
    name: string;
    domain: string;
    createdAt?: string;
    updatedAt?: string;
}

