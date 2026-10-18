/**
 * Pinia Auth Store
 * Hybrid BFF Security Architecture
 */

import { defineStore } from "pinia";
import { authApi } from "../api/auth";
import { mfaApi } from "../api/mfa";
import { ssoApi } from "../api/sso";
import { useAuthConfigStore } from "./authConfig";
import { getRouter } from "../../router/routerInstance";
import { state as primaryState } from "@/../src/store/state";

export const AUTH_MODES = {
  STANDARD: "standard",
  SSO_KEYCLOAK: "keycloak",
};

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    permissions: {},
    isSuperUser: false,
    permissionType: {
      view: 1,
      add: 2,
      edit: 3,
      delete: 4,
      force_delete: 5,
      export: 6,
      import: 7,
      view_delete: 8,
      restore: 9,
      select: 10,
      log: 11,
      print: 12,
    },

    // Access token in memory only
    accessToken: null,

    // Remove refreshToken completely
    idToken: null,

    authMode: AUTH_MODES.STANDARD,
    isLoading: false,
    error: null,

    // SSO
    ssoState: null,
    ssoNonce: null,
    codeVerifier: null,

    // MFA
    mfaPending: false,
    mfaUsername: null,
    mfaRegester: false,
    // Timers
    _refreshTimerId: null,
    _heartbeatTimerId: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,

    isSSO: (state) => state.authMode === AUTH_MODES.SSO_KEYCLOAK,

    userDisplayName: (state) => {
      if (!state.user) return "";

      return state.user.first_name
        ? `${state.user.first_name} ${state.user.last_name || ""}`.trim()
        : state.user.username;
    },

    userInitials: (state) => {
      if (!state.user) return "?";

      const name = state.user.first_name || state.user.username || "";

      return name.charAt(0).toUpperCase();
    },
  },

  actions: {
    // ==========================
    // Set Tokens (used by SSO callback)
    // ==========================
    setTokens(
      accessToken,
      refreshToken = null,
      authMode = AUTH_MODES.STANDARD,
      idToken = null
    ) {
      this.accessToken = accessToken;
      this.idToken = idToken;
      this.authMode = authMode;
      // refresh_token is in HttpOnly cookie (BFF pattern), not stored in JS
      this.startProactiveRefresh();
    },

    // ==========================
    // Login
    // ==========================

    async login(username, password) {
      this.isLoading = true;
      this.error = null;

      try {
        const data = await authApi.login(username, password);

        const payload = data.data || data;
        const authConfigStore = useAuthConfigStore();
        const isKeyLock = authConfigStore?.authMode;
        localStorage.setItem("authMode", isKeyLock);

        if (payload.mfa_required) {
          this.mfaPending = true;
          this.mfaUsername = payload.username || username;

          return {
            mfaRequired: true,
          };
        } else if (payload?.setup_required) {
          this.accessToken = payload?.access;
          this.mfaUsername = payload?.username || username;
          this.mfaRegester = true;
          return {
            mfaRequired: true,
          };
        }

        this.accessToken = payload?.access;
        this.authMode = AUTH_MODES.STANDARD;

        this.startProactiveRefresh();

        // await this.fetchProfile();

        return {
          mfaRequired: false,
        };
      } catch (error) {
        this.error = error.response?.data?.message || "فشل تسجيل الدخول";

        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    async fullLogout() {
      const wasSSO = this.isSSO;
      const idToken = this.idToken;

      try {
        if (wasSSO) {
          this.clearAuth();
          const logoutUrl = await ssoApi.getSignedLogoutUrl(
            idToken,
            this.refreshToken
          );

          window.location.href = logoutUrl;
          return;
        } else if (this.refreshToken) {
          await authApi.logout(this.refreshToken);
          this.clearAuth();
        }
      } catch (error) {
        console.warn("Logout API error:", error);
      }
    },

    // ==========================
    // MFA Verify
    // ==========================

    async verifyMFA(otpCode) {
      const data = await mfaApi.loginVerify(this.mfaUsername, otpCode);

      const payload = data.data || data;

      this.accessToken = payload.access;

      this.mfaUsername = null;

      this.startProactiveRefresh();

      // await this.fetchProfile();

      return true;
    },

    // ==========================
    // Refresh Access Token
    // ==========================

    async refreshAccessToken() {
      try {
        console.log("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx");
        /*
        Backend reads refresh token
        from HttpOnly cookie
        */

        const data = await authApi.refreshToken();

        // Support both SimpleJWT (access) and Keycloak (access_token) response formats
        this.accessToken =
          data.access ||
          data.data?.access ||
          data.access_token ||
          data.data?.access_token;

        // Detect auth mode from cookie (set by backend)
        const authModeCookie = document.cookie
          .split("; ")
          .find((c) => c.startsWith("oss_am="))
          ?.split("=")[1];

        if (authModeCookie === "keycloak") {
          this.authMode = AUTH_MODES.SSO_KEYCLOAK;
        }

        this.startProactiveRefresh();

        return true;
      } catch (error) {
        console.error("Refresh failed", error);

        // this.clearAuth();
        const currentPath = window.location.pathname + window.location.search;
        const redirectParam =
          currentPath &&
          currentPath !== "/login" &&
          !currentPath.includes("/login")
            ? `&redirect=${encodeURIComponent(currentPath)}`
            : ``;
        ("");
        window.location.href = `/login?reason=session_expired${redirectParam}`;

        return false;

        window.location.href = "/login?reason=session_expired";

        return false;
      }
    },

    // ==========================
    // Logout
    // ==========================

    async logout() {
      try {
        /*
        Backend clears cookie
        and revokes refresh token
        */
        await authApi.logout(this.accessToken);

        this.clearAuth();
      } catch (e) {
        console.warn(e);
      }
    },

    // ==========================
    // User profile
    // ==========================
    getProfile() {
      this.permissions = primaryState.permissions;
      this.isSuperUser = primaryState.is_super_user;
    },
    async fetchProfile() {
      try {
        const response = await authApi.getProfile();

        const result = response?.data?.data || response.data;

        primaryState.organization_id = result.ip;
        primaryState.is_super_user = result.ib;
        primaryState.is_manager = result.iv;

        let profile = {};
        profile.first_name = result.first_name;
        profile.last_name = result.last_name;
        profile.username = result.username;
        profile.image_user = result.image_user;
        profile.email = result.email;
        profile.org_logo = result.org_logo;

        profile.fk_user_type = result.fk_user_type;
        profile.zi = result.zi;
        primaryState.profile = profile;
        this.user = profile;

        let data = {};
        if (Array.isArray(result?.permissions))
          result?.permissions?.forEach((element) => {
            if (!data[element.route]) data[element.route] = [];

            data[element.route].push(element.operation_type);
          });

        primaryState.permissions = data;
        this.permissions = data;
      } catch (error) {
        console.error(error);
      }
    },

    // ==========================
    // Clear auth
    // ==========================

    clearAuth() {
      console.log("clear auth success");
      localStorage.removeItem("logo");
      this.stopProactiveRefresh();
      this.stopSessionHeartbeat();

      this.user = null;

      this.accessToken = null;

      this.idToken = null;

      this.ssoState = null;
      this.ssoNonce = null;
      this.codeVerifier = null;

      this.mfaPending = false;
      this.mfaRegester = false;
      this.mfaUsername = null;

      this.error = null;
    },

    // ==========================
    // Restore Session
    // ==========================

    async initAuth() {
      try {
        /*
        Called at App startup

        Browser automatically sends
        HttpOnly cookie
        */

        const data = await authApi.refreshToken();
        

        // Support both SimpleJWT (access) and Keycloak (access_token) response formats
        this.accessToken =
          data.access ||
          data.data?.access ||
          data.access_token ||
          data.data?.access_token;

        // Detect auth mode from cookie (set by backend)
        const authModeCookie = document.cookie
          .split("; ")
          .find((c) => c.startsWith("oss_am="))
          ?.split("=")[1];
        if (authModeCookie === "keycloak") {
          this.authMode = AUTH_MODES.SSO_KEYCLOAK;
        }

        // await this.fetchProfile();

        this.startProactiveRefresh();
      } catch (error) {
        if (error?.response?.data?.success === false) {
          console.log("refresh is filed ");
          this.clearAuth();
        }
      }
    },

    // ==========================
    // Proactive refresh
    // ==========================

    startProactiveRefresh() {
      this.stopProactiveRefresh();

      if (!this.accessToken) return;

      try {
        const payload = JSON.parse(atob(this.accessToken.split(".")[1]));

        const exp = payload.exp;

        const now = Math.floor(Date.now() / 1000);

        const refreshAfter = Math.max(exp - now - 60, 10);
        

        this._refreshTimerId = setTimeout(() => {

          this.refreshAccessToken();
        }, refreshAfter * 1000);
      } catch (e) {
        console.warn(e);
      }
    },

    stopProactiveRefresh() {
      if (this._refreshTimerId) {
        clearTimeout(this._refreshTimerId);

        this._refreshTimerId = null;
      }
    },

    stopSessionHeartbeat() {
      if (this._heartbeatTimerId) {
        clearInterval(this._heartbeatTimerId);

        this._heartbeatTimerId = null;
      }
    },

    setPermissions(permissions) {
      this.permissions = permissions;
    },
    checkPermission(type, path) {
      if (this.isSuperUser) return true;

      const router = getRouter();

      const routeName = path || router.currentRoute.value.name;

      const pathPermissions = this.permissions?.[routeName];
      const permissionCode = this.permissionType[type];

      if (!pathPermissions || !permissionCode) return false;

      return pathPermissions.includes(permissionCode);
    },
  },
});
