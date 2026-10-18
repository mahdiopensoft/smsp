/**
 * Auth Configuration Store
 * Fetches and stores authentication configuration from backend
 * Determines which login methods are available
 */
import { defineStore } from 'pinia'
import api from '../../../plugins/axios-plugin'

export const useAuthConfigStore = defineStore('authConfig', {
    state: () => ({
        // Configuration loaded from backend
        authMode: null,           // 'standard', 'keycloak', etc.
        allowDualAuth: false,     // Allow both local and SSO
        allowLocal: true,         // Allow local JWT login
        allowSSO: false,          // Allow SSO login
        ssoProvider: null,        // 'keycloak' or null
        keycloakConfigured: false,

        // Loading state
        isLoaded: false,
        isLoading: false,
        error: null,
    }),

    getters: {
        /**
         * Show local login button?
         */
        showLocalLogin: (state) => state.allowLocal,

        /**
         * Show SSO login button?
         */
        showSSOLogin: (state) => state.allowSSO && state.keycloakConfigured,

        /**
         * Is dual auth mode active?
         */
        isDualAuth: (state) => state.allowDualAuth,

        /**
         * Is SSO only mode?
         */
        isSSOOnly: (state) => state.allowSSO && !state.allowLocal,

        /**
         * Is local only mode?
         */
        isLocalOnly: (state) => state.allowLocal && !state.allowSSO,
    },

    actions: {
        /**
         * Fetch auth configuration from backend
         */
        async fetchConfig() {
            if (this.isLoading) return

            this.isLoading = true
            this.error = null

            try {
                const response = await api.get('/user-manager/config/')
                const data = response.data?.data || response.data

                this.authMode = data.auth_mode
                this.allowDualAuth = data.allow_dual_auth
                this.allowLocal = data.allow_local
                this.allowSSO = data.allow_sso
                this.ssoProvider = data.sso_provider
                this.keycloakConfigured = data.keycloak_configured

                this.isLoaded = true
                return data
            } catch (error) {
                console.error('Failed to fetch auth config:', error)
                this.error = 'فشل في جلب إعدادات المصادقة'
                // Default to local login only if API fails
                this.allowLocal = true
                this.allowSSO = false
                this.isLoaded = true
                throw error
            } finally {
                this.isLoading = false
            }
        },

        /**
         * Force refresh config
         */
        async refreshConfig() {
            this.isLoaded = false
            return this.fetchConfig()
        },
    },
})
