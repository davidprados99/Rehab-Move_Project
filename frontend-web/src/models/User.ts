export interface BaseUser {
    name: string;
    surnames: string;
    email: string;
    phone: string;
}

export interface Physio extends BaseUser {
    id_physio: number;
    role: 'physio';
}

export interface Patient extends BaseUser {
    id_patient: number;
    start_date: string;
    role: 'patient';
    id_physio: number;
}

// For login
export interface AuthResponse {
    access_token: string;
    token_type: string;
    role: string;
    user_id: number;
    name: string;
}
