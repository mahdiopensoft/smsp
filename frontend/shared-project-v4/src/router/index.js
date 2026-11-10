// import { useAuthStore } from "../UserManagement/stores/auth";
import { state } from "@/../src/store/state";
import { controlRoutes, logOut } from "../utils/Globals";
import { useAuthStore } from "../UserManagement/stores/auth";

export default function (router) {  
  
  // Navigation guards
  return router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()
    
    
    // const isSSO =  authStore.isSSO
    const isAuthenticated = authStore.isAuthenticated;
    

    if (!state.current_system) state.current_system = to.meta.system || null;

    try {
      if (to?.meta?.quest === true && !isAuthenticated) {
        next();
        return;
      } else if (
        (to?.meta?.requiresAuth || to?.meta?.requiresAuth == undefined) &&
        !isAuthenticated
      ) {
        logOut(false);
        next({ name: "Login" });
        return;
      } else if (to?.name === "Login" && isAuthenticated) {
        next({ name: "home" });
        return;
      } else if (!isAuthenticated) {
        next({ name: "Login"});
        return;
      } else if ((to?.meta?.quest === true || to?.meta?.requiresSSO ) && isAuthenticated) {
        next({ name: "home" });
        return;
      }
        
      controlRoutes(to, next);
    } catch (e) {
      console.log("error is :", e);
    }
  });
}
