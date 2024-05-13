import axios, { AxiosRequestConfig, AxiosError } from "axios";
import { ACCESS_TOKEN } from "./constants";

// Define the type of response data
interface ResponseData {
    // Define the structure of your response data
    // For example:
    accessToken: string;
    // Add other properties as needed
}

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL as string
});

// Request interceptor
api.interceptors.request.use(
    (config: AxiosRequestConfig): AxiosRequestConfig => {
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
