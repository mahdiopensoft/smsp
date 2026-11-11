import Axios from "axios";
import { useAuthStore } from "../src/UserManagement/stores/auth";
import setting from "@/../settings";
import { HandelError } from "../src/utils/HandelError";


const api = Axios.create({
  baseURL: setting.url,
  timeout: 1000000,
  withCredentials: true, // مهم جداً للـ HttpOnly cookies
});

// CSRF Protection (إذا backend يدعمه)
api.defaults.xsrfCookieName = "XSRF-TOKEN";
api.defaults.xsrfHeaderName = "X-XSRF-TOKEN";

// Default headers
api.defaults.headers.common["Accept-Language"] = "ar";

// ================================
// REQUEST INTERCEPTORa
// ================================
api.interceptors.request.use(
  (config) => {       
    const authStore = useAuthStore();

    const token = authStore.accessToken;

    // Access Token from MEMORY only
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
 
    // Optional: filter transformation logic (kept as-is)
    if (config.params && config.params.filters) {
      config.method = "post";

      const hasPagination = config.params.hasPagination;

      if (
        !config.url.endsWith("/filter/") &&
        !config.url.endsWith("/filter-paginate/")
      ) {
        config.url += hasPagination ? "filter-paginate/" : "filter/";
      }

      config.data = {
        ...(config.data || {}),
        filters: config.params.filters,
      };

      const { filters, ...rest } = config.params;
      config.params = rest;
    }

    return config;
  },
  (error) => Promise.reject(error),
);

let isHandling401 = false;

// ================================
// RESPONSE INTERCEPTOR (BFF STYLE)
// ================================
api.interceptors.response.use(
  (response) => response,

  async (error) => {
    if (error?.config?.skipInterceptor) return Promise.reject(error);

    const authStore = useAuthStore();
    const originalRequest = error.config;
    const requestUrl = (originalRequest?.url || "").toLowerCase();

    const isAuthEndpoint =
      requestUrl.includes("auth/") ||
      requestUrl.includes("sso/") ||
      requestUrl.includes("mfa/") ||
      requestUrl.includes("token/");

    // ================================
    // HYBRID BFF RULE:
    // Redirection on 401 with loop protection
    // ================================
    if (error.response?.status === 401 && !isAuthEndpoint) {        
      if (!isHandling401) {
        isHandling401 = true;
        authStore.clearAuth();
        try {
          await authStore.logout();
        } catch (_) {}

        const isLoginPage = typeof window !== 'undefined' && window.location.pathname.includes('/login');
        if (!isLoginPage && typeof window !== 'undefined') {
          const currentPage = window.location.pathname + window.location.search;
          window.location.href = `/login?redirect=${encodeURIComponent(currentPage)}`;
        }
        setTimeout(() => { isHandling401 = false; }, 3000);
      }
      return Promise.reject(error);
    }

    // General error handler
    HandelError(error);

    return Promise.reject(error);
  },
);

export default api;
