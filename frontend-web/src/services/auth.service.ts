import api from './api';
import type { AuthResponse } from '../models/User';

let API_URL: string;

if (import.meta.env.MODE === 'development') {
    API_URL = import.meta.env.VITE_API_URL_DEVELOPMENT;
} else {
    API_URL = import.meta.env.VITE_API_URL_PRODUCTION;
}

export const authService = {
    login: async (email: string, password: string): Promise<AuthResponse> => {
        const response = await api.post<AuthResponse>(`${API_URL}/login`, { email, password });
        return response.data;
    },
};