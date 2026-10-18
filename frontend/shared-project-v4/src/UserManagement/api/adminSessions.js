/**
 * Admin Session Management API
 * Endpoints: /user-manager/admin-sessions/
 * Requires: superuser permission
 */
import api from '../../../plugins/axios-plugin'

const ADMIN_SESSIONS_BASE = '/user-manager/admin-sessions'

export const adminSessionsApi = {
    /**
     * Get all active sessions (admin view)
     * @param {Object} params - { page, page_size, search, user_id }
     * @returns {Promise} Paginated list of all active sessions
     */
    async getAllSessions(params = {}) {
        const response = await api.get(`${ADMIN_SESSIONS_BASE}/`, { params })
        return response.data
    },

    /**
     * Revoke a specific session (admin)
     * @param {number|string} sessionId
     * @returns {Promise}
     */
    async revokeSession(sessionId) {
        const response = await api.delete(`${ADMIN_SESSIONS_BASE}/${sessionId}/`)
        return response.data
    },

    /**
     * Revoke ALL sessions for a specific user (admin)
     * @param {number} userId
     * @returns {Promise}
     */
    async revokeUserSessions(userId) {
        const response = await api.delete(`${ADMIN_SESSIONS_BASE}/user/${userId}/`)
        return response.data
    },
}

export default adminSessionsApi
