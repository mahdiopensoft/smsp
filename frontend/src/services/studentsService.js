import api from './api'

const BASE = 'students/'

export const studentsService = {
    async getStudents(params = {}) {
        const { data } = await api.get(`${BASE}students/`, { params })
        return data.results || data
    },

    async getStudentById(id) {
        const { data } = await api.get(`${BASE}students/${id}/`)
        return data
    },

    async createStudent(payload) {
        const { data } = await api.post(`${BASE}students/`, payload)
        return data
    },

    async updateStudent(id, payload) {
        const { data } = await api.patch(`${BASE}students/${id}/`, payload)
        return data
    },

    async deleteStudent(id) {
        await api.delete(`${BASE}students/${id}/`)
    },

    // Level-Student-Years
    async getLevelStudentYears(params = {}) {
        const { data } = await api.get(`${BASE}level-student-years/`, { params })
        return data.results || data
    },

    async createLevelStudentYear(payload) {
        const { data } = await api.post(`${BASE}level-student-years/`, payload)
        return data
    },
}
