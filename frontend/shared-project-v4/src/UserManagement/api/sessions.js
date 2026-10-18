/**
 * User Sessions API
 * Endpoints: /user-manager/sessions/ (user's own sessions)
 */
import api from '../../../plugins/axios-plugin'

const SESSIONS_BASE = '/user-manager/sessions'

export const sessionsApi = {
    /**
     * Get current user's active sessions
     * @returns {Promise} [{ id, browser, os, device, ip_address, created_at, last_activity, is_current }]
     */
    async getMySessions() {
        const response = await api.get(`${SESSIONS_BASE}/`)
        return response.data
    },

    /**
     * Revoke a specific session
     * @param {number|string} sessionId
     * @returns {Promise}
     */
    async revokeSession(sessionId) {
        const response = await api.delete(`${SESSIONS_BASE}/${sessionId}/`)
        return response.data
    },

    /**
     * Revoke all sessions except current
     * @returns {Promise}
     */
    async revokeAllSessions() {
        const response = await api.delete(`${SESSIONS_BASE}/all/`)
        return response.data
    },
}

export default sessionsApi
