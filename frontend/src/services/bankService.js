import api from './api'

const BASE = 'api/bank/'

export const bankService = {
    // ==========================================
    // 1. شاشة بنك الأسئلة (Question Bank Screen)
    // Endpoint: api/bank/questions/
    // ==========================================
    async getQuestions(params = {}) {
        const { data } = await api.get(`${BASE}questions/`, { params })
        return data.results || data
    },

    async getQuestionStats() {
        const { data } = await api.get(`${BASE}questions/stats/`)
        return data
    },

    async duplicateQuestion(id) {
        const { data } = await api.post(`${BASE}questions/${id}/duplicate/`)
        return data
    },

    async archiveQuestion(id) {
        const { data } = await api.post(`${BASE}questions/${id}/archive/`)
        return data
    },

    async restoreQuestion(id) {
        const { data } = await api.post(`${BASE}questions/${id}/restore/`)
        return data
    },

    async createQuestionVersion(id, payload = {}) {
        const { data } = await api.post(`${BASE}questions/${id}/create_version/`, payload)
        return data
    },

    async deleteQuestion(id) {
        await api.delete(`${BASE}questions/${id}/`)
    },

    async getDeletedQuestions() {
        const { data } = await api.get(`${BASE}questions/deleted/`)
        return data.results || data
    },

    // ====================================================
    // 0. شاشة لوحة التحكم الرئيسية (Main Dashboard Screen)
    // Endpoint: api/bank/dashboard/
    // ====================================================
    async getDashboardSummary(params = {}) {
        const { data } = await api.get(`${BASE}dashboard/summary/`, { params })
        return data
    },

    // ==============================================================
    // 2. شاشة إضافة وتعديل سؤال جديد (Question Create & Edit Screen)
    // Endpoint: api/bank/question-new/
    // ==============================================================
    async createQuestion(payload) {
        const { data } = await api.post(`${BASE}question-new/`, payload)
        return data
    },

    async updateQuestion(id, payload) {
        const { data } = await api.patch(`${BASE}question-new/${id}/`, payload)
        return data
    },

    async getQuestionDetails(id) {
        const { data } = await api.get(`${BASE}question-new/${id}/details/`)
        return data
    },

    async getQuestionById(id) {
        const { data } = await api.get(`${BASE}question-new/${id}/`)
        return data
    },

    async checkQuestionSimilarity(payload) {
        const { data } = await api.post(`${BASE}question-new/check_similarity/`, payload)
        return data
    },

    // =========================================================
    // 3. شاشة الإدخال السريع للأسئلة (Question Fast Entry Screen)
    // Endpoint: api/bank/question-fast-entry/
    // =========================================================
    async fastBulkCreateQuestions(payload) {
        const { data } = await api.post(`${BASE}question-fast-entry/bulk_create_full/`, payload)
        return data
    },

    // ===================================================
    // 4. شاشة استيراد من إكسل (Question Excel Import Screen)
    // Endpoint: api/bank/question-import/
    // ===================================================
    async importExcelQuestions(formData) {
        const { data } = await api.post(`${BASE}question-import/import-excel/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
        return data
    },

    // ===================================================
    // 4.1 شاشة استكمال البيانات (Bulk Complete Screen)
    // Endpoint: api/bank/bulk-complete/
    // ===================================================
    async getImportedList(params = {}) {
        const { data } = await api.get(`${BASE}bulk-complete/imported_list/`, { params })
        return data
    },

    async getImportedStats(params = {}) {
        const { data } = await api.get(`${BASE}bulk-complete/stats/`, { params })
        return data
    },

    async bulkAssignImported(payload) {
        const { data } = await api.post(`${BASE}bulk-complete/bulk_assign/`, payload)
        return data
    },

    async bulkActivateImported(payload) {
        const { data } = await api.post(`${BASE}bulk-complete/bulk_activate/`, payload)
        return data
    },

    // ===================================================
    // 4.2 مقارنة النسخ (Question Diff View)
    // Endpoint: api/bank/question-diff/
    // ===================================================
    async compareQuestionVersions(v1, v2) {
        const { data } = await api.get(`${BASE}question-diff/compare/`, { params: { v1, v2 } })
        return data
    },

    async getQuestionVersionHistory(questionId) {
        const { data } = await api.get(`${BASE}question-diff/history/`, { params: { question_id: questionId } })
        return data
    },

    // ===================================================
    // 5. شاشة طابور المراجعة (Question Review Queue Screen)
    // Endpoint: api/bank/question-review/
    // ===================================================
    async getReviewQuestions(params = {}) {
        const { data } = await api.get(`${BASE}question-review/`, { params })
        return data
    },

    async getReviewStats() {
        const { data } = await api.get(`${BASE}question-review/stats/`)
        return data
    },

    async approveReviewQuestion(id, payload = {}) {
        const { data } = await api.post(`${BASE}question-review/${id}/approve/`, payload)
        return data
    },

    async rejectReviewQuestion(id, payload = {}) {
        const { data } = await api.post(`${BASE}question-review/${id}/reject/`, payload)
        return data
    },

    async escalateDeptHead(id) {
        const { data } = await api.post(`${BASE}question-review/${id}/escalate_dept_head/`)
        return data
    },

    async bulkApproveReviewQuestions(payload) {
        const { data } = await api.post(`${BASE}question-review/bulk-approve/`, payload)
        return data
    },

    async bulkRejectReviewQuestions(payload) {
        const { data } = await api.post(`${BASE}question-review/bulk-reject/`, payload)
        return data
    },

    // ===================================================
    // 6. سجل الرقابة والتدقيق (Audit Logs)
    // Endpoint: api/bank/audit-logs/
    // ===================================================
    async getAuditLogs(params = {}) {
        const { data } = await api.get(`${BASE}audit-logs/`, { params })
        return data
    },

    async getAuditLogStats(params = {}) {
        const { data } = await api.get(`${BASE}audit-logs/stats/`, { params })
        return data
    },


    // ===================================================
    // Auxiliaries / Answers
    // ===================================================
    async getAnswers(params = {}) {
        const { data } = await api.get(`${BASE}answers/`, { params })
        return data.results || data
    },

    async createAnswer(payload) {
        const { data } = await api.post(`${BASE}answers/`, payload)
        return data
    },

    async updateAnswer(id, payload) {
        const { data } = await api.patch(`${BASE}answers/${id}/`, payload)
        return data
    },

    async deleteAnswer(id) {
        await api.delete(`${BASE}answers/${id}/`)
    },
}
