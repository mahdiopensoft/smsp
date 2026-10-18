/**
 * User Management API
 * Endpoints: /user-manager/
 */
import api from '../../../plugins/axios-plugin'

const USER_MANAGER_BASE = '/user-manager'

export const usersApi = {
    // ========================================
    // Users CRUD
    // ========================================

    /**
     * Get users list with pagination and filters
     * @param {Object} params - { page, page_size, search, ordering, is_active, is_approved }
     * @returns {Promise} Paginated results
     */
    async getUsers(params = {}) {
        const response = await api.get(`${USER_MANAGER_BASE}/users/`, { params })
        return response.data
    },

    /**
     * Get single user by ID
     * @param {number} id 
     * @returns {Promise} User object
     */
    async getUser(id) {
        const response = await api.get(`${USER_MANAGER_BASE}/users/${id}/`)
        return response.data
    },

    /**
     * Create new user
     * @param {Object} data - { username, email, password, first_name, last_name, ... }
     * @returns {Promise} Created user
     */
    async createUser(data) {
        const response = await api.post(`${USER_MANAGER_BASE}/users/`, data)
        return response.data
    },

    /**
     * Update user (full update)
     * @param {number} id 
     * @param {Object} data 
     * @returns {Promise} Updated user
     */
    async updateUser(id, data) {
        const response = await api.put(`${USER_MANAGER_BASE}/users/${id}/`, data)
        return response.data
    },

    /**
     * Partial update user
     * @param {number} id 
     * @param {Object} data 
     * @returns {Promise} Updated user
     */
    async patchUser(id, data) {
        const response = await api.patch(`${USER_MANAGER_BASE}/users/${id}/`, data)
        return response.data
    },

    /**
     * Delete user
     * @param {number} id 
     */
    async deleteUser(id) {
        const response = await api.delete(`${USER_MANAGER_BASE}/users/${id}/`)
        return response.data
    },

    // ========================================
    // User Actions
    // ========================================

    /**
     * Approve user
     * @param {number} id 
     * @param {string} approvedTo - Date until approval is valid
     * @returns {Promise}
     */
    async approveUser(id, approvedTo) {
        const response = await api.post(`${USER_MANAGER_BASE}/users/${id}/approve/`, {
            approved_to: approvedTo,
        })
        return response.data
    },

    /**
     * Unapprove user
     * @param {number} id 
     * @returns {Promise}
     */
    async unapproveUser(id) {
        const response = await api.post(`${USER_MANAGER_BASE}/users/${id}/unapprove/`)
        return response.data
    },

    /**
     * Toggle user active status
     * @param {number} id 
     * @returns {Promise}
     */
    async toggleActive(id) {
        const response = await api.post(`${USER_MANAGER_BASE}/users/${id}/change-user-active-status/`)
        return response.data
    },

    /**
     * Admin change user password
     * @param {number} id 
     * @param {string} newPassword 
     * @returns {Promise}
     */
    async adminChangePassword(id, newPassword) {
        const response = await api.post(`${USER_MANAGER_BASE}/users/${id}/admin-change-password/`, {
            new_password: newPassword,
        })
        return response.data
    },

    /**
     * Update user image
     * @param {number} id 
     * @param {File} imageFile 
     * @returns {Promise}
     */
    async updateImage(id, imageFile) {
        const formData = new FormData()
        formData.append('image', imageFile)

        const response = await api.post(`${USER_MANAGER_BASE}/users/${id}/change-image/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        })
        return response.data
    },

    // ========================================
    // Groups
    // ========================================

    /**
     * Get groups list
     * @param {Object} params 
     * @returns {Promise}
     */
    async getGroups(params = {}) {
        const response = await api.get(`${USER_MANAGER_BASE}/groups/`, { params })
        return response.data
    },

    /**
     * Get single group
     * @param {number} id 
     * @returns {Promise}
     */
    async getGroup(id) {
        const response = await api.get(`${USER_MANAGER_BASE}/groups/${id}/`)
        return response.data
    },

    /**
     * Create group
     * @param {Object} data 
     * @returns {Promise}
     */
    async createGroup(data) {
        const response = await api.post(`${USER_MANAGER_BASE}/groups/`, data)
        return response.data
    },

    /**
     * Update group
     * @param {number} id 
     * @param {Object} data 
     * @returns {Promise}
     */
    async updateGroup(id, data) {
        const response = await api.put(`${USER_MANAGER_BASE}/groups/${id}/`, data)
        return response.data
    },

    /**
     * Delete group
     * @param {number} id 
     */
    async deleteGroup(id) {
        const response = await api.delete(`${USER_MANAGER_BASE}/groups/${id}/`)
        return response.data
    },

    // ========================================
    // User Types
    // ========================================

    /**
     * Get user types list
     * @param {Object} params 
     * @returns {Promise}
     */
    async getUserTypes(params = {}) {
        const response = await api.get(`${USER_MANAGER_BASE}/user-type/`, { params })
        return response.data
    },

    /**
     * Get single user type
     * @param {number} id 
     * @returns {Promise}
     */
    async getUserType(id) {
        const response = await api.get(`${USER_MANAGER_BASE}/user-type/${id}/`)
        return response.data
    },

    /**
     * Create user type
     * @param {Object} data 
     * @returns {Promise}
     */
    async createUserType(data) {
        const response = await api.post(`${USER_MANAGER_BASE}/user-type/`, data)
        return response.data
    },

    /**
     * Update user type
     * @param {number} id 
     * @param {Object} data 
     * @returns {Promise}
     */
    async updateUserType(id, data) {
        const response = await api.put(`${USER_MANAGER_BASE}/user-type/${id}/`, data)
        return response.data
    },

    /**
     * Delete user type
     * @param {number} id 
     */
    async deleteUserType(id) {
        const response = await api.delete(`${USER_MANAGER_BASE}/user-type/${id}/`)
        return response.data
    },

    // ========================================
    // Keycloak Roles
    // ========================================

    /**
     * Get all Keycloak realm roles with assignment status for a user
     * @param {number} userId 
     * @returns {Promise} [{name, description, assigned: true/false}, ...]
     */
    async getKeycloakRoles(userId) {
        const response = await api.get(`${USER_MANAGER_BASE}/users/${userId}/keycloak-roles/`)
        return response.data
    },

    /**
     * Assign Keycloak realm roles to a user
     * @param {number} userId 
     * @param {string[]} roleNames 
     * @returns {Promise}
     */
    async assignKeycloakRoles(userId, roleNames) {
        const response = await api.post(`${USER_MANAGER_BASE}/users/${userId}/keycloak-roles/assign/`, {
            roles: roleNames,
        })
        return response.data
    },

    /**
     * Remove Keycloak realm roles from a user
     * @param {number} userId 
     * @param {string[]} roleNames 
     * @returns {Promise}
     */
    async removeKeycloakRoles(userId, roleNames) {
        const response = await api.post(`${USER_MANAGER_BASE}/users/${userId}/keycloak-roles/remove/`, {
            roles: roleNames,
        })
        return response.data
    },
}

export default usersApi
