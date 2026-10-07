import api from './api'

export const reportsService = {
  // ── 1. تقرير جودة وأوراق الاختبار ──
  getExamQualityReport: async (params = {}) => {
    const response = await api.get('/api/exams/exam-quality-report/', { params })
    return response.data
  },
  getExamQualityStats: async () => {
    const response = await api.get('/api/exams/exam-quality-report/stats/')
    return response.data
  },

  // ── 2. تقرير أداء المؤلفين ──
  getAuthorsReport: async (params = {}) => {
    const response = await api.get('/api/bank/authors-report/', { params })
    return response.data
  },
  getAuthorsReportStats: async () => {
    const response = await api.get('/api/bank/authors-report/stats/')
    return response.data
  },

  // ── 3. تقرير التغطية الأكاديمية للمناهج ──
  getCurriculumReport: async (params = {}) => {
    const response = await api.get('/api/academic/curriculum-report/', { params })
    return response.data
  },
  getCurriculumReportStats: async () => {
    const response = await api.get('/api/academic/curriculum-report/stats/')
    return response.data
  },

  // ── 4. تقرير حالة بنك الأسئلة والمستويات المعرفية ──
  getBankStatusOverview: async (params = {}) => {
    const response = await api.get('/api/bank/bank-status-report/overview/', { params })
    return response.data
  },

  // ── 5. مصفوفة المواءمة الأكاديمية لمخرجات التعلم (CLOs) ──
  getAlignmentMatrixReport: async (params = {}) => {
    const response = await api.get('/api/academic/alignment-matrix-report/matrix/', { params })
    return response.data
  },

  // ── 6. التقرير الإقليمي والجغرافي ──
  getRegionalReport: async (params = {}) => {
    const response = await api.get('/api/exams/regional-report/overview/', { params })
    return response.data
  },
}

