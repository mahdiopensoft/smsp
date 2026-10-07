import api from './api'

export const authService = {
    async login(username, password) {
        const { data } = await api.post('accounts/login/', { username, password })

        localStorage.setItem('access_token', data.access)
        localStorage.setItem('refresh_token', data.refresh)
        localStorage.setItem('auth_user', JSON.stringify(data.user))

        return data
    },

    async logout() {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('auth_user')
        return { success: true }
    },

    async getCurrentUser() {
        const { data } = await api.get('accounts/me/')
        return data
    },

    getStoredUser() {
        const user = localStorage.getItem('auth_user')
        return user ? JSON.parse(user) : null
    },

    isAuthenticated() {
        return !!localStorage.getItem('access_token')
    },
}
