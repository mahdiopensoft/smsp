/**
 * Auth Service - Authentication API calls
 */

import api from '../../plugins/axios-plugin'

export const authService = {
  /**
   * تسجيل الدخول
   */
  async login (credentials) {
    const response = await api.post('/auth/login/', credentials)
    return response.data
  },

  /**
   * تسجيل مستخدم جديد
   */
  async register (userData) {
    const response = await api.post('/auth/register/', userData)
    return response.data
  },

  /**
   * تسجيل الخروج
   */
  async logout () {
    const response = await api.post('/auth/logout/')
    return response.data
  },

  /**
   * الحصول على الملف الشخصي
   */
  async getProfile () {
    const response = await api.get('/auth/profile/')
    return response.data
  },

  /**
   * تحديث الملف الشخصي
   */
  async updateProfile (data) {
    const response = await api.patch('/auth/profile/', data)
    return response.data
  },

  /**
   * تغيير كلمة المرور
   */
  async changePassword (data) {
    const response = await api.post('/auth/password/change/', data)
    return response.data
  },

  /**
   * تحديث صورة الملف الشخصي
   */
  async updateProfilePicture (file, userData) {
    const formData = new FormData()
    formData.append('profile_picture', file)
    // إضافة الحقول المطلوبة
    if (userData?.email) {
      formData.append('email', userData.email)
    }
    if (userData?.username) {
      formData.append('username', userData.username)
    }
    const response = await api.patch('/auth/profile/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  /**
   * البحث عن مستخدمين
   */
  async searchUsers (query) {
    const response = await api.get('/auth/users/', {
      params: { search: query },
    })
    return response.data
  },

  /**
   * حظر مستخدم
   */
  async blockUser (userId) {
    const response = await api.post(`/auth/users/${userId}/block/`)
    return response.data
  },

  /**
   * إلغاء حظر مستخدم
   */
  async unblockUser (userId) {
    const response = await api.delete(`/auth/users/${userId}/unblock/`)
    return response.data
  },

  /**
   * الحصول على قائمة المحظورين
   */
  async getBlockedUsers () {
    const response = await api.get('/auth/users/blocked/')
    return response.data
  },

  // ==================== Admin Methods ====================

  /**
   * الحصول على جميع المستخدمين (للمشرفين)
   */
  async getUsers (params) {
    const response = await api.get('/auth/admin/users/', { params })
    return response.data
  },

  /**
   * إنشاء مستخدم جديد (للمشرفين)
   */
  async createUser (userData) {
    const response = await api.post('/auth/admin/users/', userData)
    return response.data
  },

  /**
   * تحديث مستخدم (للمشرفين)
   */
  async updateUser (userId, userData) {
    const response = await api.put(`/auth/admin/users/${userId}/`, userData)
    return response.data
  },

  /**
   * حذف مستخدم (للمشرفين)
   */
  async deleteUser (userId) {
    const response = await api.delete(`/auth/admin/users/${userId}/`)
    return response.data
  },

  /**
   * إحصائيات النظام
   */
  async getSystemStats () {
    const response = await api.get('/auth/admin/stats/')
    return response.data
  },

  /**
   * التحقق من الصلاحيات
   */
  async getCurrentUserRole () {
    const response = await api.get('/auth/me/role/')
    return response.data
  },

  /**
   * إعادة تعيين كلمة مرور المستخدم (للمشرفين)
   */
  async resetUserPassword (userId) {
    const response = await api.post(`/auth/admin/users/${userId}/reset-password/`)
    return response.data
  },
}

export default authService
