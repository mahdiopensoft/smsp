// import { useAuthStore } from "../UserManagement/stores/auth";
import { state } from "@/../src/store/state";
import { controlRoutes } from "../utils/Globals";
import { useAuthStore } from "../UserManagement/stores/auth";
import { setRouter } from "./routerInstance";

export default function (router) {
  setRouter(router);

  // Navigation guards
  return router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();

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
        const redirect =
          to.fullPath && to.name !== "Login" && to.path !== "/login"
            ? to.fullPath
            : undefined;

        next({ name: "Login", qurery: redirect ? { redirect } : undefined });

        return;
      } else if (to?.name === "Login" && isAuthenticated) {
        const redirect = to.query?.redirect;
        if (redirect && redirect !== "/login" && !redirect.includes("/login")) {
          next({ path: redirect });
        } else {
          next({ name: "home" });
        }
        return;
      } else if (!isAuthenticated) {
        const redirect = to.fullPath && to.name !== "Login" && to.path !== "/login" ? to.fullPath:undefined
 
        next({ name: "Login" ,query:redirect?{redirect} : undefined});
        return;
      } else if (
        to?.meta?.quest === true &&
        !to?.meta?.requiresAuth &&
        isAuthenticated
      ) {
        // Guest-only pages (login, callback) — redirect authenticated users to home
        next({ name: "home" });
        return;
      }
      controlRoutes(to, next);
    } catch (e) {
      console.log("error is :", e);
    }
  });
}
