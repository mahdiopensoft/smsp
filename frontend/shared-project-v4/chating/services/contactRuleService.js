import api from "../../plugins/axios-plugin"


export const contactRuleService = {
  /**
   * جلب جميع القواعد
   */
  async getRules() {
    const response = await api.get("/chat/contacts/rules/");
    return response.data;
  },

  /**
   * جلب قاعدة محددة
   */
  async getRule(id) {
    const response = await api.get(`/chat/contacts/rules/${id}/`);
    return response.data;
  },

  /**
   * إنشاء قاعدة جديدة
   */
  async createRule(data) {
    const response = await api.post("/chat/contacts/rules/", data);
    return response.data;
  },

  /**
   * تعديل قاعدة
   */
  async updateRule(id, data) {
    const response = await api.patch(`/chat/contacts/rules/${id}/`, data);
    return response.data;
  },

  /**
   * حذف قاعدة
   */
  async deleteRule(id) {
    const response = await api.delete(`/chat/contacts/rules/${id}/`);
    return response.data;
  },

  /**
   * تسجيل مجموعة قواعد دفعة واحدة
   */
  async bulkRegister(rulesData) {
    const response = await api.post("/chat/contacts/rules/bulk-register/", rulesData);
    return response.data;
  },
};

export default contactRuleService;
