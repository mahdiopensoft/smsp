import api from '../../plugins/axios-plugin'

export const dashboardService = {
  /**
   * جلب إحصائيات لوحة التحكم
   */
  async getStats(filters = {}) {
    const response = await api.get('/chat/dashboard/stats/', { params: filters })
    return response.data
  },
}

export default dashboardService
