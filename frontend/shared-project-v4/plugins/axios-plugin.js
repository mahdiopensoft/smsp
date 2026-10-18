import Axios from "axios";
import { useAuthStore } from "../src/UserManagement/stores/auth";
import setting from "@/../settings";
import { HandelError } from "../src/utils/HandelError";
import { state } from "@/../src/store/state";

const api = Axios.create({
  baseURL: setting.url,
  timeout: 200000,
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
  
    const exId = state?.organization_ex_id || JSON.parse(localStorage.getItem("current_org") || "{}")?.ex_id;
    if (exId) {
      config.headers["X-Organization-ExId"] = exId;
    }

    // Optional: filter transformation logic (kept as-is)
    if (config.params && config?.params?.filters) {
      
      const hasPagination = config.params.hasPagination;
      config.method = "post";
      
      if (
        !config.url.endsWith("/filter/") &&
        !config.url.endsWith("/filter-paginate/")
        ) {
          config.url += hasPagination ? "filter-paginate/" : "filter/";
        
        }

      var filtersPatam = []
      if(config.data && config.data.filters){
        filtersPatam.push(...config?.data?.filters)
      }
      if(config.params&& config.params.filters){
        filtersPatam.push(...config.params.filters )
      }
        
    

      config.data = {
        ...(config.data || {}),
        filters:filtersPatam
      };
      // filters:[...config?.data?.filters, ...config?.params?.filters],

      const { filters, ...rest } = config.params;
      config.params = rest;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// ================================
// RESPONSE INTERCEPTOR (BFF STYLE)
// ================================

let isLoggingOut = false;
api.interceptors.response.use(
  (response) => response,

  async (error) => {
 
    
    if (error?.config?.skipInterceptor) return Promise.reject(error);

    
    const originalRequest = error.config;
    const requestUrl = originalRequest?.url || ""

    const isLoginEndpoint = originalRequest?.url?.includes("/auth/") ||
    originalRequest?.url?.includes("/sso/") ||
    originalRequest?.url?.includes("/mfa/") ||
    originalRequest?.url?.includes("/token/");          
      
    if(error?.status === 401){
      if(isLoginEndpoint){
        return Promise.reject(error)
      }
      if(!isLoggingOut){
        isLoggingOut = true;
        try{
          const authStore = useAuthStore();
          await authStore.logout()
        }catch(e){
          console.warn("401 Auto-logout error :" ,e)
          
        }finally{
          const authStore = useAuthStore()
          authStore.clearAuth()
          window.location.reload()
        }
      }
      return Promise.reject(error)
    }

  
    HandelError(error);

    return Promise.reject(error);
  }
);

export default api;
