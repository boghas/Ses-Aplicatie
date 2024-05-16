import axios, { InternalAxiosRequestConfig, AxiosError } from "axios";
import { ACCESS_TOKEN } from "./constants";



const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL as string
});

// Request interceptor
api.interceptors.request.use(
    (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error: AxiosError) => {
        return Promise.reject(error);
    }
);

// Response interceptor
api.interceptors.response.use(
    (response) => {
        // Return the response directly
        return response;
    },
    (error: AxiosError) => {
        // Log the error
        console.error('Request failed:', error);
        // Reject the promise with the error
        return Promise.reject(error);
    }
);

export default api;
