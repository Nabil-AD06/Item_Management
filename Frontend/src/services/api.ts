import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
    config.headers.Authorization = `Bearer ${keycloak.token}`;
    return config;
});

export default api;