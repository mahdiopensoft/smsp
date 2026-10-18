/**
 * Auth Service - Authentication API calls
 */

import api from '../../plugins/axios-plugin'

export const authService = {
  /**
   * تحديث الملف الشخصي
   */
  async updateProfile(data) {
    const response = await api.patch('/auth/profile/', data)
    return response.data
  },

  /**
   * تحديث صورة الملف الشخصي
   */
  async updateProfilePicture(file, userData) {
    const formData = new FormData()
    formData.append('profile_picture', file)
    // إضافة الحقول المطلوبة
    if (userData?.email) {
      formData.append('email', userData.email)
    }
    if (userData?.username) {
      formData.append('username', userData.username)
    }
    const response = await api.post('/auth/users/change-image/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },
}

export default authService
