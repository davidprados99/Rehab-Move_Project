import api from './api';
import type { AuthResponse } from '../models/User';

export const authService = {
    login: async (email: string, password: string): Promise<AuthResponse> => {
        const response = await api.post<AuthResponse>(`/login`, { email, password });
        return response.data;
    },
};