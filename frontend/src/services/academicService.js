import api from './api'

const BASE = 'api/academic/'

const fetchAllPages = async (endpoint) => {
    let results = []
    let url = endpoint
    while (url) {
        // Strip absolute domain and /api/ prefix if url is absolute to maintain Axios baseURL & Bearer Token
        const cleanUrl = url.replace(/^https?:\/\/[^\/]+\/api\//, '')
        const { data } = await api.get(cleanUrl)
        if (data && data.results) {
            results = results.concat(data.results)
            url = data.next ? data.next : null
        } else {
            return data // Fallback if not paginated
        }
    }
    return results
}

export const academicService = {
    // Organizations
    async getOrganizations() {
        return await fetchAllPages(`${BASE}organizations/`)
    },
    async createOrganization(payload) {
        const { data } = await api.post(`${BASE}organizations/`, payload)
        return data
    },
    async updateOrganization(id, payload) {
        const { data } = await api.patch(`${BASE}organizations/${id}/`, payload)
        return data
    },
    async deleteOrganization(id) {
        await api.delete(`${BASE}organizations/${id}/`)
    },

    // Academic Years
    async getAcademicYears() {
        return await fetchAllPages(`${BASE}academic-years/`)
    },
    async createAcademicYear(payload) {
        const { data } = await api.post(`${BASE}academic-years/`, payload)
        return data
    },
    async updateAcademicYear(id, payload) {
        const { data } = await api.patch(`${BASE}academic-years/${id}/`, payload)
        return data
    },
    async deleteAcademicYear(id) {
        await api.delete(`${BASE}academic-years/${id}/`)
    },

    // Tracks (المسارات الدراسية)
    async getTracks() {
        return await fetchAllPages(`${BASE}tracks/`)
    },
    async createTrack(payload) {
        const { data } = await api.post(`${BASE}tracks/`, payload)
        return data
    },
    async updateTrack(id, payload) {
        const { data } = await api.patch(`${BASE}tracks/${id}/`, payload)
        return data
    },
    async deleteTrack(id) {
        await api.delete(`${BASE}tracks/${id}/`)
    },

    // Stages (المراحل الدراسية)
    async getStages() {
        return await fetchAllPages(`${BASE}educational-stages/`)
    },
    async createStage(payload) {
        const { data } = await api.post(`${BASE}educational-stages/`, payload)
        return data
    },
    async updateStage(id, payload) {
        const { data } = await api.patch(`${BASE}educational-stages/${id}/`, payload)
        return data
    },
    async deleteStage(id) {
        await api.delete(`${BASE}educational-stages/${id}/`)
    },

    // Levels (الصفوف الدراسية)
    async getLevels() {
        return await fetchAllPages(`${BASE}levels/`)
    },
    async createLevel(payload) {
        const { data } = await api.post(`${BASE}levels/`, payload)
        return data
    },
    async updateLevel(id, payload) {
        const { data } = await api.patch(`${BASE}levels/${id}/`, payload)
        return data
    },
    async deleteLevel(id) {
        await api.delete(`${BASE}levels/${id}/`)
    },

    // Class Tracks (ربط الصفوف بالمسارات)
    async getClassTracks() {
        return await fetchAllPages(`${BASE}class-tracks/`)
    },
    async createClassTrack(payload) {
        const { data } = await api.post(`${BASE}class-tracks/`, payload)
        return data
    },
    async updateClassTrack(id, payload) {
        const { data } = await api.patch(`${BASE}class-tracks/${id}/`, payload)
        return data
    },
    async deleteClassTrack(id) {
        await api.delete(`${BASE}class-tracks/${id}/`)
    },

    // Subjects (المواد الدراسية)
    async getSubjects() {
        return await fetchAllPages(`${BASE}subjects/`)
    },
    async createSubject(payload) {
        const { data } = await api.post(`${BASE}subjects/`, payload)
        return data
    },
    async updateSubject(id, payload) {
        const { data } = await api.patch(`${BASE}subjects/${id}/`, payload)
        return data
    },
    async deleteSubject(id) {
        await api.delete(`${BASE}subjects/${id}/`)
    },

    // Class Subjects (مواد مسارات الصفوف)
    async getClassSubjects() {
        return await fetchAllPages(`${BASE}class-subjects/`)
    },
    async createClassSubject(payload) {
        const { data } = await api.post(`${BASE}class-subjects/`, payload)
        return data
    },
    async updateClassSubject(id, payload) {
        const { data } = await api.patch(`${BASE}class-subjects/${id}/`, payload)
        return data
    },
    async deleteClassSubject(id) {
        await api.delete(`${BASE}class-subjects/${id}/`)
    },

    // Semesters (الفصول الدراسية)
    async getSemesters() {
        return await fetchAllPages(`${BASE}semesters/`)
    },
    async createSemester(payload) {
        const { data } = await api.post(`${BASE}semesters/`, payload)
        return data
    },
    async updateSemester(id, payload) {
        const { data } = await api.patch(`${BASE}semesters/${id}/`, payload)
        return data
    },
    async deleteSemester(id) {
        await api.delete(`${BASE}semesters/${id}/`)
    },

    // Units (الوحدات)
    async getUnits(params = {}) {
        const query = params && Object.keys(params).length ? '?' + new URLSearchParams(params).toString() : ''
        return await fetchAllPages(`${BASE}units/${query}`)
    },
    async createUnit(payload) {
        const { data } = await api.post(`${BASE}units/`, payload)
        return data
    },
    async updateUnit(id, payload) {
        const { data } = await api.patch(`${BASE}units/${id}/`, payload)
        return data
    },
    async deleteUnit(id) {
        await api.delete(`${BASE}units/${id}/`)
    },

    // Lessons (الدروس)
    async getLessons() {
        return await fetchAllPages(`${BASE}lessons/`)
    },
    async createLesson(payload) {
        const { data } = await api.post(`${BASE}lessons/`, payload)
        return data
    },
    async updateLesson(id, payload) {
        const { data } = await api.patch(`${BASE}lessons/${id}/`, payload)
        return data
    },
    async deleteLesson(id) {
        await api.delete(`${BASE}lessons/${id}/`)
    },

    // Learning Outcomes (مخرجات التعلم)
    async getLearningOutcomes() {
        return await fetchAllPages(`${BASE}learning-outcomes/`)
    },
    async createLearningOutcome(payload) {
        const { data } = await api.post(`${BASE}learning-outcomes/`, payload)
        return data
    },
    async updateLearningOutcome(id, payload) {
        const { data } = await api.patch(`${BASE}learning-outcomes/${id}/`, payload)
        return data
    },
    async deleteLearningOutcome(id) {
        await api.delete(`${BASE}learning-outcomes/${id}/`)
    },



    // Students (الطلاب)
    async getStudents() {
        return await fetchAllPages(`${BASE}students/`)
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

    // Exam Periods
    async getExamPeriods() {
        return await fetchAllPages(`${BASE}exam-periods/`)
    },
}
