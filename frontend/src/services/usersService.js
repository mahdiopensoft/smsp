import api from './api'

export const usersService = {
    async getAll() {
        const { data } = await api.get('user-manager/users/')
        return data.results || data
    },

    async getById(id) {
        const { data } = await api.get(`user-manager/users/${id}/`)
        return data
    },

    async create(payload) {
        const { data } = await api.post('user-manager/users/', payload)
        return data
    },

    async update(id, payload) {
        const { data } = await api.patch(`user-manager/users/${id}/`, payload)
        return data
    },

    async delete(id) {
        await api.delete(`user-manager/users/${id}/`)
        return { success: true }
    },
}
