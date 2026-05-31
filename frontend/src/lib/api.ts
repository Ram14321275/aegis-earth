import axios from "axios";

// Creating an axios instance pointing to the backend
// In Vite dev mode, this will be proxied to http://localhost:8000 via vite.config.ts
export const apiClient = axios.create({
  baseURL: "/api/v1",
  timeout: 30000, // 30 seconds timeout to handle analysis latency
  headers: {
    "Content-Type": "application/json",
  },
});

// Response interceptor for error handling globally
apiClient.interceptors.response.use(
  (response) => {
    // Unpack the standard APIResponse{data, meta} if available
    return response.data;
  },
  (error) => {
    console.error("[API Error]", error.response?.data || error.message);
    return Promise.reject(error.response?.data || { detail: error.message });
  }
);
