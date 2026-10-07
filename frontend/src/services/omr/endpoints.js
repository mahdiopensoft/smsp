/**
 * API endpoints — organized by module for OMR and Exam Management.
 */

import api from './client.js'

// ── Auth ──
export const authAPI = {
  login: (email, password) => api.post('/accounts/auth/login/', { email, password }),
  refresh: (refresh) => api.post('/accounts/auth/refresh/', { refresh }),
  register: (data) => api.post('/accounts/auth/register/', data),
  getProfile: () => api.get('/accounts/profile/'),
  updateProfile: (data) => api.patch('/accounts/profile/', data),
}

// ── Academics ──
export const departmentsAPI = {
  list: (params) => api.get('/academics/departments/', { params }),
  get: (id) => api.get(`/academics/departments/${id}/`),
  create: (data) => api.post('/academics/departments/', data),
  update: (id, data) => api.patch(`/academics/departments/${id}/`, data),
  delete: (id) => api.delete(`/academics/departments/${id}/`),
}

export const coursesAPI = {
  list: (params) => api.get('/academics/courses/', { params }),
  get: (id) => api.get(`/academics/courses/${id}/`),
  create: (data) => api.post('/academics/courses/', data),
  update: (id, data) => api.patch(`/academics/courses/${id}/`, data),
  delete: (id) => api.delete(`/academics/courses/${id}/`),
}

export const studentsAPI = {
  list: (params) => api.get('/academics/students/', { params }),
  get: (id) => api.get(`/academics/students/${id}/`),
  create: (data) => api.post('/academics/students/', data),
  update: (id, data) => api.patch(`/academics/students/${id}/`, data),
  delete: (id) => api.delete(`/academics/students/${id}/`),
}

// ── Exams (Linked to OMR) ──
export const examsAPI = {
  list: (params) => api.get('/api/exams/exams/', { params }),
  get: (id) => api.get(`/api/exams/exams/${id}/`),
  create: (data) => api.post('/api/exams/exams/', data),
  update: (id, data) => api.patch(`/api/exams/exams/${id}/`, data),
  delete: (id) => api.delete(`/api/exams/exams/${id}/`),
  setAnswerKey: (id, data) => api.post(`/api/exams/exams/${id}/answer-key/`, data),
}

// ── Templates ──
export const templatesAPI = {
  list: (params) => api.get('/api/templates-engine/exam-templates/', { params }),
  get: (id) => api.get(`/api/templates-engine/exam-templates/${id}/`),
  create: (data) => api.post('/api/templates-engine/exam-templates/', data),
  update: (id, data) => api.patch(`/api/templates-engine/exam-templates/${id}/`, data),
  delete: (id) => api.delete(`/api/templates-engine/exam-templates/${id}/`),
  validate: (id) => api.post(`/api/templates-engine/exam-templates/${id}/validate/`),
  generate: (data) => api.post('/api/templates-engine/generate/', data),
  createVersion: (id, notes) => api.post(`/api/templates-engine/exam-templates/${id}/create-version/`, { notes }),
}

// ── Submissions & Results ──
export const submissionsAPI = {
  list: (params) => api.get('/api/submissions/submissions/', { params }),
  getStats: (params) => api.get('/api/submissions/submissions/stats/', { params }),
  get: (id) => api.get(`/api/submissions/submissions/${id}/`),
  reprocess: (id) => api.post(`/api/submissions/submissions/${id}/reprocess/`),
  updateReview: (id, data) => api.post(`/api/submissions/submissions/${id}/update_review/`, data),
  delete: (id) => api.delete(`/api/submissions/submissions/${id}/`),
  process: (id) => api.post(`/api/submissions/submissions/${id}/process/`),
  bulkUpload: (formData) => api.post('/api/submissions/submissions/bulk-upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
}

export const batchesAPI = {
  list: (params) => api.get('/api/submissions/submission-batches/', { params }),
  get: (id) => api.get(`/api/submissions/submission-batches/${id}/`),
  create: (data) => api.post('/api/submissions/submission-batches/', data),
  process: (id) => api.post(`/api/submissions/submission-batches/${id}/process/`),
}

// ── 1. شاشة المراجعة البشرية والتدقيق ──
export const humanReviewAPI = {
  list: (params) => api.get('/api/omr/human-review/', { params }),
  getStats: () => api.get('/api/omr/human-review/stats/'),
  approveReview: (id) => api.post(`/api/omr/human-review/${id}/approve-review/`),
  overrideQuestion: (id, data) => api.post(`/api/omr/human-review/${id}/override-question/`, data),
}

// ── 2. شاشة الاستخراج الكامل المباشر ──
export const omrExtractionAPI = {
  uploadAndExtract: (formData) => api.post('/api/omr/omr-extraction/upload-and-extract/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
}

// ── 3. شاشة المختبر والمسح الضوئي ──
export const omrScannerLabAPI = {
  getAnswerKey: (params) => api.get('/api/omr/omr-scanner/answer-key/', { params }),
  scanSheet: (data) => api.post('/api/omr/omr-scanner/scan-sheet/', data),
}

// ── 4. شاشة أوراق الإجابة ومكتبة القوالب ──
export const omrBubbleSheetsAPI = {
  list: (params) => api.get('/api/omr/omr-bubble-sheets/', { params }),
  getQualityAudit: (id) => api.get(`/api/omr/omr-bubble-sheets/${id}/quality-audit/`),
}

// ── 5. شاشة تصميم القوالب الهندسية (CAD) ──
export const omrTemplatesAPI = {
  list: (params) => api.get('/api/omr/omr-templates/', { params }),
  get: (id) => api.get(`/api/omr/omr-templates/${id}/`),
  create: (data) => api.post('/api/omr/omr-templates/', data),
  update: (id, data) => api.patch(`/api/omr/omr-templates/${id}/`, data),
  delete: (id) => api.delete(`/api/omr/omr-templates/${id}/`),
  validateLayout: (data) => api.post('/api/omr/omr-templates/validate-layout/', data),
  exportJson: (id) => api.get(`/api/omr/omr-templates/${id}/export-json/`),
}
