import api from './api'

export const reportsService = {
  // ── 1. تقرير جودة الاختبار (أوراق الطلاب) ──
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

  // ── 7. تقرير الأسئلة التفصيلي (جديد) ──
  getQuestionsDetailReport: async (params = {}) => {
    const response = await api.get('/api/bank/questions-detail-report/', { params })
    return response.data
  },

  // ── 8. تقرير الأسئلة المرفوضة (جديد) ──
  getRejectedQuestionsReport: async (params = {}) => {
    const response = await api.get('/api/bank/rejected-questions-report/', { params })
    return response.data
  },

  // ── 9. تقرير الاختبارات المولدة (جديد) ──
  getExamsGeneratedReport: async (params = {}) => {
    const response = await api.get('/api/exams/exams-generated-report/', { params })
    return response.data
  },

  // ── 10. تقرير توزيع وإرسال الاختبارات (جديد) ──
  getExamDistributionReport: async (params = {}) => {
    const response = await api.get('/api/exams/exam-distribution-report/', { params })
    return response.data
  },

  // ── 11. تقرير المحذوفات من المنهج (جديد) ──
  getCurriculumExclusionsReport: async (params = {}) => {
    const response = await api.get('/api/exams/curriculum-exclusions-report/', { params })
    return response.data
  },

  // ── 12. تقرير تسجيلات الطلاب في الاختبارات (جديد) ──
  getStudentRegistrationsReport: async (params = {}) => {
    const response = await api.get('/api/exams/student-registrations-report/', { params })
    return response.data
  },

  // ── 13. تقرير الطلاب (جديد) ──
  getStudentsReport: async (params = {}) => {
    const response = await api.get('/api/academic/students-report/', { params })
    return response.data
  },

  // ── 14. تقرير نتائج التصحيح الآلي (جديد) ──
  getOMRResultsReport: async (params = {}) => {
    const response = await api.get('/api/omr/omr-results-report/', { params })
    return response.data
  },

  // ── 15. تقرير الأسئلة التي تحتاج مراجعة OMR (جديد) ──
  getOMRReviewQuestionsReport: async (params = {}) => {
    const response = await api.get('/api/omr/omr-review-questions-report/', { params })
    return response.data
  },
}
