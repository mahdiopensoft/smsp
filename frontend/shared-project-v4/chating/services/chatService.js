/**
 * Chat Service - Chat and Message API calls
 */
 import api from "../../plugins/axios-plugin"

export const chatService = {
  // ==================== المحادثات ====================

  /**
   * الحصول على قائمة المحادثات
   */
  async getChats() {
    const response = await api.get("/chat/");
    const data = response.data;
    const chats = Array.isArray(data) ? data : (data.results || []);

    // معالجة البيانات لضمان توافقها مع ChatListItem.vue
    return chats.map(chat => this._normalizeChat(chat));
  },

  /**
   * معالجة بيانات المحادثة لضمان اكتمال الحقول
   */
  _normalizeChat(chat) {
    if (!chat) return null;

    return {
      ...chat,
      // التأكد من وجود كائن المشارك الآخر
      other_participant: chat.other_participant || null,
      // التأكد من وجود مصفوفة المشاركين
      participants_data: chat.participants_data || [],
      // التأكد من وجود آخر رسالة
      last_message: chat.last_message || null,
      // الحقول الافتراضية للفرونت
      is_pinned: !!chat.is_pinned,
      is_archived: !!chat.is_archived,
      is_muted: !!chat.is_muted,
      unread_count: chat.unread_count || 0
    };
  },

  /**
   * الحصول على جهات الاتصال المسموح بها
   */
  async getAllowedContacts() {
    const response = await api.get("/chat/contacts/allowed-contacts/");
    const data = response.data;

    if (Array.isArray(data)) {
      return data;
    }

    if (Array.isArray(data?.results)) {
      return data.results;
    }

    if (Array.isArray(data?.data)) {
      return data.data;
    }

    if (Array.isArray(data?.users)) {
      return data.users;
    }

    return [];
  },

  /**
   * الحصول على جهات الاتصال مجمّعة حسب البنية التنظيمية
   */
  async getGroupedContacts() {
    const response = await api.get("/chat/contacts/grouped-contacts/");
    return response.data;
  },

  /**
   * الحصول على تفاصيل محادثة
   */
  async getChat(chatId) {
    const response = await api.get(`/chat/${chatId}/`);
    return this._normalizeChat(response.data);
  },

  /**
   * إنشاء محادثة جديدة
   */
  async createChat(data) {
    if (data.group_picture) {
      const formData = new FormData();
      Object.keys(data).forEach(key => {
        if (key === 'participant_ids') {
          data[key].forEach(id => formData.append('participant_ids', id));
        } else {
          formData.append(key, data[key]);
        }
      });
      const response = await api.post("/chat/create/", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      return response.data;
    } else {
      const response = await api.post("/chat/create/", data);
      return response.data;
    }
  },

  /**
   * تثبيت/إلغاء تثبيت محادثة
   */
  async togglePinChat(chatId) {
    const response = await api.post(`/chat/preferences/${chatId}/pin/`);
    return response.data;
  },

  /**
   * كتم/إلغاء كتم إشعارات محادثة
   */
  async toggleMuteChat(chatId) {
    const response = await api.post(`/chat/preferences/${chatId}/mute/`);
    return response.data;
  },

  /**
   * أرشفة/إلغاء أرشفة محادثة
   */
  async toggleArchiveChat(chatId) {
    const response = await api.post(`/chat/preferences/${chatId}/archive/`);
    return response.data;
  },

  /**
   * مغادرة المجموعة
   */
  async leaveChat(chatId) {
    const response = await api.delete(`/chat/participants/${chatId}/leave/`);
    return response.data;
  },

  /**
   * مسح الرسائل
   */
  async clearChat(chatId) {
    const response = await api.delete(`/chat/${chatId}/clear/`);
    return response.data;
  },

  /**
   * حذف المحادثة
   */
  async deleteChat(chatId, deleteForAll = false) {
    const response = await api.delete(`/chat/${chatId}/delete/`, { params: { delete_for_all: deleteForAll } });
    return response.data;
  },

  async updateWallpaper(chatId, wallpaper) {
    if (typeof wallpaper === 'string' && wallpaper.startsWith('data:image')) {
      // Send as multipart/form-data to bypass WAF, but keep as string so backend doesn't crash on .startswith()
      const formData = new FormData();
      formData.append("wallpaper", wallpaper);
      
      const response = await api.post(`/chat/preferences/${chatId}/wallpaper/`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      return response.data;
    }

    const response = await api.post(`/chat/preferences/${chatId}/wallpaper/`, {
      wallpaper,
    });
    return response.data;
  },

  /**
   * تحديث الخلفية لمجموعة من المحادثات أو الكل
   */
  async bulkUpdateWallpaper(data) {
    const response = await api.post("/chat/preferences/bulk-wallpaper/", data);
    return response.data;
  },

  /**
   * إضافة مشارك للمجموعة
   */
  async addParticipant(chatId, userId) {
    const response = await api.post(`/chat/participants/${chatId}/add-participant/`, {
      user_id: userId,
    });
    return response.data;
  },

  /**
   * إزالة مشارك من المجموعة
   */
  async removeParticipant(chatId, userId) {
    const response = await api.delete(
      `/chat/participants/${chatId}/participants/${userId}/remove/`,
    );
    return response.data;
  },

  /**
   * تحديث دور المشارك (مشرف أو عادي)
   */
  async updateParticipantRole(chatId, userId, isAdmin) {
    const response = await api.patch(
      `/chat/participants/${chatId}/participants/${userId}/role/`,
      { is_admin: isAdmin }
    );
    return response.data;
  },

  /**
   * تحديث معلومات المجموعة (الاسم، الصورة، الوصف)
   */
  async updateGroup(chatId, data) {
    const formData = new FormData();
    if (data.name) {
      formData.append("name", data.name);
    }
    if (data.description !== undefined) {
      formData.append("description", data.description);
    }
    if (data.group_picture) {
      formData.append("group_picture", data.group_picture);
    }

    const response = await api.put(`/chat/${chatId}/update/`, formData);
    return response.data;
  },

  /**
   * تفعيل/تعطيل المراسلة للمشرفين فقط
   */
  async toggleReadOnly(chatId) {
    const response = await api.post(`/chat/${chatId}/toggle-read-only/`);
    return response.data;
  },

  /**
   * كتم/إلغاء كتم عضو محدد
   */
  async toggleMemberMessaging(chatId, userId) {
    const response = await api.post(
      `/chat/participants/${chatId}/participants/${userId}/toggle-messaging/`,
    );
    return response.data;
  },

  /**
   * تثبيت رسالة
   */
  async pinMessage(chatId, messageId) {
    const response = await api.post(
      `/chat/${chatId}/messages/${messageId}/pin/`,
    );
    return response.data;
  },

  /**
   * إلغاء تثبيت الرسالة
   */
  async unpinMessage(chatId) {
    const response = await api.post(`/chat/${chatId}/unpin/`);
    return response.data;
  },

  // ==================== الرسائل ====================

  /**
   * الحصول على رسائل محادثة
   */
  async getMessages(chatId, page = 1) {
 
    const response = await api.get(`/chat/messages/chat/${chatId}/`, {
      params: { page },
    });
    return response.data;
  },

  /**
   * الحصول على الوسائط المشاركة
   */
  async getSharedMedia(chatId, filterType = 'media', page = 1) {
    const response = await api.get(`/chat/messages/chat/${chatId}/shared-media/`, {
      params: { type: filterType, page },
    });
    return response.data;
  },

  /**
   * إرسال رسالة نصية
   */
  async sendMessage(chatId, content, replyTo = null, messageType = "text") {
    const response = await api.post(`/chat/messages/chat/${chatId}/send/`, {
      content,
      message_type: messageType,
      reply_to: replyTo,
    });
    return response.data;
  },

  /**
   * إرسال ملف/صورة/صوت
   */
  async sendFile(chatId, file, messageType = "file", caption = "") {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("message_type", messageType);
    if (caption) {
      formData.append("content", caption);
    }

    const response = await api.post(`/chat/messages/chat/${chatId}/send/`, formData);
    return response.data;
  },

  /**
   * تحديد رسائل كمقروءة
   */
  async markAsRead(chatId, messageIds) {
    const response = await api.post(`/chat/messages/chat/${chatId}/mark-read/`, {
      message_ids: messageIds,
    });
    return response.data;
  },

  /**
   * حذف رسالة
   */
  async deleteMessage(messageId, forEveryone = false) {
    const response = await api.delete(`/chat/messages/${messageId}/delete/`, {
      data: { everyone: forEveryone },
    });
    return response.data;
  },

  /**
   * تعديل رسالة
   */
  async editMessage(messageId, content) {
    const response = await api.put(`/chat/messages/${messageId}/edit/`, { content });
    return response.data;
  },

  /**
   * إضافة/إزالة تفاعل
   */
  async toggleReaction(messageId, emoji) {
    const response = await api.post(`/chat/messages/${messageId}/react/`, {
      emoji,
    });
    return response.data;
  },

  /**
   * البحث في الرسائل
   */
  async searchMessages(chatId, query) {
    const response = await api.get(`/chat/messages/chat/${chatId}/search/`, {
      params: { q: query },
    });
    return response.data;
  },

  /**
   * إعادة توجيه رسالة
   */
  async forwardMessage(messageId, chatIds) {
    const response = await api.post(`/chat/messages/${messageId}/forward/`, {
      chat_ids: chatIds,
    });
    return response.data;
  },

  /**
   * تمييز رسالة بنجمة
   */
  async toggleStar(messageId) {
    const response = await api.post(`/chat/messages/${messageId}/star/`);
    return response.data;
  },

  /**
   * الحصول على الرسائل المميزة بنجمة
   */
  async getStarredMessages() {
    const response = await api.get("/chat/messages/starred/");
    return response.data;
  },

  // ==================== الخصوصية والمحظورين ====================

  /**
   * حظر مستخدم
   */
  async blockUser(userId) {
    const response = await api.post(`/chat/preferences/users/${userId}/block/`);
    return response.data;
  },

  /**
   * إلغاء حظر مستخدم
   */
  async unblockUser(userId) {
    const response = await api.delete(`/chat/preferences/users/${userId}/unblock/`);
    return response.data;
  },

  /**
   * الحصول على قائمة المستخدمين المحظورين
   */
  async getBlockedUsers() {
    const response = await api.get('/chat/preferences/users/blocked/');
    return response.data;
  },
};

export default chatService;
