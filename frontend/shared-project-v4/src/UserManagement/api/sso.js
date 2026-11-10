/**
 * SSO Keycloak Authentication API
 * Endpoints: /sso/
 * Uses HMAC-SHA256 signatures for client authentication
 */
import api from '../../../plugins/axios-plugin'
import settings from "@/../settings"
const SSO_BASE = 'sso'

// Client credentials - secret is NEVER sent directly, only used for HMAC signing
const CLIENT_ID = 'web'
const CLIENT_SECRET = '0b174bccbb1205107c86b85ce96f933698835335e3dd2c3565daeaf48e0406c9'

/**
 * Generate HMAC-SHA256 signature for client authentication.
 * Signs: client_id + ":" + timestamp using the secret key.
 * @returns {Promise<{client_id: string, timestamp: string, signature: string}>}
 */
async function generateClientSignature() {
    const timestamp = Math.floor(Date.now() / 1000).toString()
    const message = `${CLIENT_ID}:${timestamp}`

    // Import the secret key for HMAC-SHA256
    const encoder = new TextEncoder()
    const keyData = encoder.encode(CLIENT_SECRET)
    const cryptoKey = await crypto.subtle.importKey(
        'raw',
        keyData,
        { name: 'HMAC', hash: 'SHA-256' },
        false,
        ['sign']
    )

    // Sign the message
    const messageData = encoder.encode(message)
    const signatureBuffer = await crypto.subtle.sign('HMAC', cryptoKey, messageData)

    // Convert to hex string
    const signatureArray = new Uint8Array(signatureBuffer)
    const signature = Array.from(signatureArray)
        .map(b => b.toString(16).padStart(2, '0'))
        .join('')

    return { client_id: CLIENT_ID, timestamp, signature }
}

/**
 * Build query string with signature parameters
 * @returns {Promise<string>}
 */
async function buildSignedParams() {
    const { client_id, timestamp, signature } = await generateClientSignature()
    const params = new URLSearchParams()
    params.append('client_id', client_id)
    params.append('timestamp', timestamp)
    params.append('signature', signature)
    return params.toString()
}

export const ssoApi = {
    /**
     * Initiate SSO login - generates signed URL for redirect
     * @param {string} redirectUri - Where to redirect after login
     * @returns {Promise<string>} Signed SSO login URL
     */
    async getSignedLoginUrl(redirectUri = null) {
        const signedParams = await buildSignedParams()
        let url = `${SSO_BASE}/login/?${signedParams}`
        if (redirectUri) url += `&redirect_uri=${encodeURIComponent(redirectUri)}`
        return url
    },

    /**
     * Handle SSO callback - exchange code for tokens
     * @param {string} code - Authorization code from Keycloak
     * @param {string} state - State parameter for validation
     * @param {string} codeVerifier - PKCE code verifier
     * @returns {Promise} { access_token, refresh_token, id_token }
     */
    async handleCallback(code, state, codeVerifier = null) {
        const params = new URLSearchParams()
        params.append('code', code)
        params.append('state', state)
        if (codeVerifier) params.append('code_verifier', codeVerifier)

        const response = await api.get(`${SSO_BASE}/callback?${params.toString()}`)
        return response.data
    },

    /**
     * Build signed SSO logout URL for browser redirect.
     * The browser navigates to this URL → backend handles everything:
     *   1. Revokes refresh_token in Keycloak
     *   2. Clears Django session
     *   3. Redirects to Keycloak logout page (clears SSO cookie)
     *   4. Keycloak redirects to /sso/logout-callback → /login
     *
     * @param {string} idToken - ID token for Keycloak logout hint
     * @param {string} refreshToken - Refresh token for server-side revocation
     * @returns {Promise<string>} Full signed logout URL
     */
    async getSignedLogoutUrl(idToken = null, refreshToken = null) {
        const baseUrl = settings.url
        const signedParams = await buildSignedParams()
        let url = `${baseUrl}${SSO_BASE}/logout/?${signedParams}`

        if (idToken) {
            url += `&id_token_hint=${encodeURIComponent(idToken)}`
        }
        if (refreshToken) {
            url += `&refresh_token=${encodeURIComponent(refreshToken)}`
        }
        return url
    },

    /**
     * Refresh SSO token
     * @param {string} refreshToken 
     * @returns {Promise} { access_token, refresh_token }
     */
    async refreshToken(refreshToken) {
        const response = await api.post(`${SSO_BASE}/refresh/`, { refresh_token: refreshToken })
        // ResponseHandler.success wraps data in {success, message, data: {access_token, ...}}
        return response.data?.data || response.data
    },

    /**
     * Get user info from Keycloak
     * @returns {Promise} User info object
     */
    async getUserInfo() {
        const response = await api.get(`${SSO_BASE}/userinfo/`)
        return response.data
    },

    /**
     * Validate a token
     * @param {string} token 
     * @returns {Promise} { valid, claims }
     */
    async validateToken(token) {
        const response = await api.post(`${SSO_BASE}/validate/`, { token })
        return response.data
    },

    /**
     * Get active sessions
     * @returns {Promise} List of sessions
     */
    async getSessions() {
        const response = await api.get(`${SSO_BASE}/sessions/`)
        return response.data
    },

    /**
     * Revoke a session
     * @param {string} sessionId 
     */
    async revokeSession(sessionId) {
        const response = await api.delete(`${SSO_BASE}/sessions/${sessionId}/`)
        return response.data
    },

    /**
     * Check Keycloak health
     * @returns {Promise} { status, message }
     */
    async checkHealth() {
        const response = await api.get(`${SSO_BASE}/health/`)
        return response.data
    },

    /**
     * Get allowed systems for the current user
     * Based on their Keycloak realm roles and org level
     * @returns {Promise} { data: [{role, system_name, url}, ...] }
     */
    async getAllowedSystems() {
        const response = await api.get(`${SSO_BASE}/allowed-systems/`)
        return response.data
    },

    // Expose for external use
    generateClientSignature,
    buildSignedParams,
}

export default ssoApi
