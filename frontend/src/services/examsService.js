import api from './api'

const BASE = 'api/exams/'

export const examsService = {
    // ========================================================
    // 1. شاشة توليد اختبار (Exam Create Wizard Screen)
    // Endpoint: api/exams/exam-create/
    // ========================================================
    async checkShortage(payload) {
        const { data } = await api.post(`${BASE}exam-create/check-shortage/`, payload)
        return data
    },

    async generateExam(payload) {
        const { data } = await api.post(`${BASE}exam-create/generate/`, payload)
        return data
    },

    async getExamTemplates(params = {}) {
        const { data } = await api.get(`${BASE}exam-create/templates/`, { params })
        return data
    },

    async saveExamTemplate(payload) {
        const { data } = await api.post(`${BASE}exam-create/save-template/`, payload)
        return data
    },

    async deleteExamTemplate(templateId) {
        const { data } = await api.delete(`${BASE}exam-create/delete-template/${templateId}/`)
        return data
    },

    // ========================================================
    // 2. شاشة إدارة النماذج (Exam Models Management Screen)
    // Endpoint: api/exams/exam-models/
    // ========================================================
    async getExamModelsDetails(examId) {
        const { data } = await api.get(`${BASE}exam-models/${examId}/details/`)
        return data
    },

    async shuffleModelQuestions(payload) {
        const { data } = await api.post(`${BASE}exam-models/shuffle/`, payload)
        return data
    },

    async reorderModelQuestions(payload) {
        const { data } = await api.post(`${BASE}exam-models/reorder/`, payload)
        return data
    },

    async removeModelQuestion(payload) {
        const { data } = await api.post(`${BASE}exam-models/remove-question/`, payload)
        return data
    },

    // ========================================================
    // 3. شاشة أرشيف الاختبارات (Exam Archive Screen)
    // Endpoint: api/exams/exam-archive/
    // ========================================================
    async getArchivedExams(params = {}) {
        const { data } = await api.get(`${BASE}exam-archive/`, { params })
        return data
    },

    async getArchiveStats() {
        const { data } = await api.get(`${BASE}exam-archive/stats/`)
        return data
    },

    async getArchivedExamDashboard(id) {
        const { data } = await api.get(`${BASE}exam-archive/${id}/dashboard/`)
        return data
    },

    // ========================================================
    // 4. جدول المواصفات (Table of Specifications Screen)
    // Endpoint: api/exams/table-of-specifications/
    // ========================================================
    async getTablesOfSpecifications(params = {}) {
        const { data } = await api.get(`${BASE}table-of-specifications/`, { params })
        return data.results || data
    },

    async getTableOfSpecificationsById(id) {
        const { data } = await api.get(`${BASE}table-of-specifications/${id}/`)
        return data
    },

    async createTableOfSpecifications(payload) {
        const { data } = await api.post(`${BASE}table-of-specifications/`, payload)
        return data
    },

    async updateTableOfSpecifications(id, payload) {
        const { data } = await api.patch(`${BASE}table-of-specifications/${id}/`, payload)
        return data
    },

    async deleteTableOfSpecifications(id) {
        await api.delete(`${BASE}table-of-specifications/${id}/`)
    },

    async getTOSBlueprint(id) {
        const { data } = await api.get(`${BASE}table-of-specifications/${id}/blueprint/`)
        return data
    },

    // ========================================================
    // 5. المحذوفات من المنهج والمقررات (Curriculum Exclusions)
    // Endpoint: api/exams/curriculum-exclusions/
    // ========================================================
    async getCurriculumExclusions(params = {}) {
        const { data } = await api.get(`${BASE}curriculum-exclusions/`, { params })
        return data
    },

    async getCurriculumTreeForSubject(params = {}) {
        const { data } = await api.get(`${BASE}curriculum-exclusions/tree-for-subject/`, { params })
        return data
    },

    async syncCurriculumExclusions(payload) {
        const { data } = await api.post(`${BASE}curriculum-exclusions/batch-sync/`, payload)
        return data
    },

    async getActiveExclusionIds(params = {}) {
        const { data } = await api.get(`${BASE}curriculum-exclusions/active-ids/`, { params })
        return data
    },

    async deleteCurriculumExclusion(id) {
        await api.delete(`${BASE}curriculum-exclusions/${id}/`)
    },

    // ========================================================
    // Auxiliaries & Sub-entities
    // ========================================================
    async getExamSettings() {
        const { data } = await api.get(`${BASE}exam-generation-settings/`)
        return data.results || data
    },
    async createExamSetting(payload) {
        const { data } = await api.post(`${BASE}exam-generation-settings/`, payload)
        return data
    },

    async getExamSchedules() {
        const { data } = await api.get(`${BASE}exam-schedules/`)
        return data.results || data
    },
    async createExamSchedule(payload) {
        const { data } = await api.post(`${BASE}exam-schedules/`, payload)
        return data
    },
    async updateExamSchedule(id, payload) {
        const { data } = await api.patch(`${BASE}exam-schedules/${id}/`, payload)
        return data
    },
    async deleteExamSchedule(id) {
        await api.delete(`${BASE}exam-schedules/${id}/`)
    },

    async getExams() {
        const { data } = await api.get(`${BASE}exams/`)
        return data.results || data
    },
    async getExamById(id) {
        const { data } = await api.get(`${BASE}exams/${id}/`)
        return data
    },
    async createExam(payload) {
        const { data } = await api.post(`${BASE}exams/`, payload)
        return data
    },
    async updateExam(id, payload) {
        const { data } = await api.patch(`${BASE}exams/${id}/`, payload)
        return data
    },
    async deleteExam(id) {
        await api.delete(`${BASE}exams/${id}/`)
    },

    async getExamVersions(params = {}) {
        const { data } = await api.get(`${BASE}exam-versions/`, { params })
        return data.results || data
    },
    async createExamVersion(payload) {
        const { data } = await api.post(`${BASE}exam-versions/`, payload)
        return data
    },
    async deleteExamVersion(id) {
        await api.delete(`${BASE}exam-versions/${id}/`)
    },

    async getExamQuestionOrders(params = {}) {
        const { data } = await api.get(`${BASE}exam-question-orders/`, { params })
        return data.results || data
    },
    async createExamQuestionOrder(payload) {
        const { data } = await api.post(`${BASE}exam-question-orders/`, payload)
        return data
    },
    async updateExamQuestionOrder(id, payload) {
        const { data } = await api.patch(`${BASE}exam-question-orders/${id}/`, payload)
        return data
    },
    async deleteExamQuestionOrder(id) {
        await api.delete(`${BASE}exam-question-orders/${id}/`)
    },

    async getStudentExamRegistrations(params = {}) {
        const { data } = await api.get(`${BASE}student-exam-registrations/`, { params })
        return data
    },
    async getStudentRegistrationStats(params = {}) {
        const { data } = await api.get(`${BASE}student-exam-registrations/stats/`, { params })
        return data
    },
    async createStudentExamRegistration(payload) {
        const { data } = await api.post(`${BASE}student-exam-registrations/`, payload)
        return data
    },
    async updateStudentExamRegistration(id, payload) {
        const { data } = await api.patch(`${BASE}student-exam-registrations/${id}/`, payload)
        return data
    },
    async deleteStudentExamRegistration(id) {
        await api.delete(`${BASE}student-exam-registrations/${id}/`)
    },
    async toggleStudentAttendance(id, isPresent) {
        const { data } = await api.post(`${BASE}student-exam-registrations/${id}/toggle_attendance/`, { is_present: isPresent })
        return data
    },
    async bulkRegisterStudents(payload) {
        const { data } = await api.post(`${BASE}student-exam-registrations/bulk_register/`, payload)
        return data
    },

    // ========================================================
    // 7. شاشة توزيع وتصدير الاختبارات المجدول (Exam Distribution)
    // Endpoint: api/exams/distributions/
    // ========================================================
    async getDistributions(params = {}) {
        const { data } = await api.get(`${BASE}distributions/`, { params })
        return data
    },
    async resolveDistributionHierarchy(payload) {
        const { data } = await api.post(`${BASE}distributions/resolve-hierarchy/`, payload)
        return data
    },
    async createDispatch(payload) {
        const { data } = await api.post(`${BASE}distributions/create-dispatch/`, payload)
        return data
    },
    async getDistributionLiveStatus(id) {
        const { data } = await api.get(`${BASE}distributions/${id}/live-status/`)
        return data
    },
    async getExportPackage(params = {}) {
        const { data } = await api.get(`${BASE}export/package/`, { params })
        return data
    },
    async ackExportPackage(payload) {
        const { data } = await api.post(`${BASE}distributions/export-ack/`, payload)
        return data
    },
    async cancelDistribution(id, reason = '') {
        const { data } = await api.post(`${BASE}distributions/${id}/cancel-dispatch/`, { reason })
        return data
    },
    async forceUnlockDistribution(id) {
        const { data } = await api.post(`${BASE}distributions/${id}/force-unlock/`)
        return data
    },
    async downloadDistributionPackage(id) {
        const { data } = await api.get(`${BASE}distributions/${id}/download-package/`)
        return data
    },
    async simulateSchoolSync(id, payload) {
        const { data } = await api.post(`${BASE}distributions/${id}/simulate-school-sync/`, payload)
        return data
    },
}

