export interface ChasterExtensionSessionSchema {
    id: string;
    role: string;
    is_linked: boolean;
    link_token: string | null;
}
