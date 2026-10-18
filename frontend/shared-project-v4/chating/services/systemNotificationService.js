import api from "../../plugins/axios-plugin";

export const systemNotificationService = {
  // Fetch central notifications for user
  async getNotifications(page = 1) {
    const response = await api.get(`/chat/system-notifications/?page=${page}`, {
      skipInterceptor: true,
    });
    return response.data;
  },

  /**
   * تعليم الإشعار كمقروء
   */
  async markAsRead(id) {
    const response = await api.post(
      `/chat/system-notifications/${id}/mark-read/`
    );
    return response.data;
  },

  /**
   * تعليم كافة الإشعارات كمقروءة
   */
  async markAllAsRead() {
    const response = await api.post(
      `/chat/system-notifications/mark-all-read/`
    );
    return response.data;
  },
};
