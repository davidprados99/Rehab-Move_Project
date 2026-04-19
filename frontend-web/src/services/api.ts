import axios from 'axios';

// Determine the API URL based on the environment
const API_URL = import.meta.env.MODE === 'production' ? import.meta.env.VITE_API_URL_PRODUCTION : import.meta.env.VITE_API_URL_DEVELOPMENT;

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to include the token in the Authorization header
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;