/**
 * Pinia Auth Store
 * Hybrid BFF Security Architecture
 */

import { defineStore } from "pinia";
import { authApi } from "../api/auth";
import { mfaApi } from "../api/mfa";

export const AUTH_MODES = {
  STANDARD: "standard",
  SSO_KEYCLOAK: "keycloak",
};

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,

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
    // Login
    // ==========================

    async login(username, password) {
      this.isLoading = true;
      this.error = null;

      try {
        const data = await authApi.login(username, password);

        const payload = data.data || data;

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
        if (payload?.access) {
          try { localStorage.setItem("token", payload.access); } catch (_) {}
        }
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
        /*
        Backend reads refresh token
        from HttpOnly cookie
        */

        const data = await authApi.refreshToken();

        this.accessToken = data.access;

        this.startProactiveRefresh();

        return true;
      } catch (error) {
        console.error("Refresh failed", error);

        this.clearAuth();

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

        await authApi.logout();
      } catch (e) {
        console.warn(e);
      }

      this.clearAuth();

     },

    // ==========================
    // User profile
    // ==========================

    async fetchProfile() {
      try {
        const profile = await authApi.getProfile();

        this.user = profile.data || profile;
      } catch (error) {
        console.error(error);
      }
    },

    // ==========================
    // Clear auth
    // ==========================

    clearAuth() {
      try { localStorage.removeItem("token"); } catch (_) {}
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
      const savedToken = typeof localStorage !== "undefined" ? localStorage.getItem("token") : null;
      if (savedToken) {
        this.accessToken = savedToken;
      }
      try {
        const data = await authApi.refreshToken();
        this.accessToken = data.access;
        if (data.access) {
          try { localStorage.setItem("token", data.access); } catch (_) {}
        }
        this.startProactiveRefresh();
      } catch {
        if (!this.accessToken) {
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
  },
});
