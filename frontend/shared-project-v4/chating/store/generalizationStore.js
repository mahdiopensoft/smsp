import { defineStore } from "pinia";
import api from "../../plugins/axios-plugin";

export const useGeneralizationStore = defineStore("generalization", {
  state: () => ({
    generalizations: [],
    unreadGeneralizations: [],
    unreadCount: 0,
    inboxCount: 0,
    sentCount: 0,
    loading: false,
    loadingMore: false,
    error: null,
    nextPageUrl: null,
    hasMore: true,
    currentFilter: 'inbox',
  }),

  getters: {
    hasUnread: (state) => state.unreadCount > 0,
  },

  actions: {
    async fetchCounts() {
      try {
        const response = await api.get('/chat/generalizations/counts/');
        const data = response.data;
        this.unreadCount = data.unread || 0;
        this.inboxCount = data.inbox || 0;
        this.sentCount = data.sent || 0;
      } catch (err) {
        console.error("Error fetching generalization counts:", err);
      }
    },

    async fetchUnreadGeneralizations() {
      try {
        const response = await api.get('/chat/generalizations/?filter=unread');
        const data = response.data;
        if (data && typeof data === 'object' && 'results' in data) {
          this.unreadGeneralizations = data.results || [];
        } else {
          this.unreadGeneralizations = Array.isArray(data) ? data : [];
        }
      } catch (err) {
        console.error("Error fetching unread generalizations:", err);
      }
    },

    async fetchGeneralizations(filter) {
      if (filter) {
        this.currentFilter = filter;
      } else {
        filter = this.currentFilter;
      }
      this.loading = true;
      this.error = null;
      this.hasMore = true;
      this.nextPageUrl = null;
      this.generalizations = [];

      try {
        // Fetch fresh tab counts
        await this.fetchCounts();

        const response = await api.get(`/chat/generalizations/?filter=${filter}`);
        const data = response.data;

        if (data && typeof data === 'object' && 'results' in data) {
          // Response is paginated
          this.generalizations = data.results || [];
          this.nextPageUrl = data.next || null;
          this.hasMore = !!data.next;
        } else {
          // Response is standard array
          this.generalizations = Array.isArray(data) ? data : [];
          this.nextPageUrl = null;
          this.hasMore = false;
        }
      } catch (err) {
        console.error("Error fetching generalizations:", err);
        this.error = err;
      } finally {
        this.loading = false;
      }
    },

    async loadMoreGeneralizations() {
      if (this.loadingMore || !this.hasMore || !this.nextPageUrl) return;

      this.loadingMore = true;
      try {
        const response = await api.get(this.nextPageUrl);
        const data = response.data;

        if (data && typeof data === 'object' && 'results' in data) {
          this.generalizations.push(...(data.results || []));
          this.nextPageUrl = data.next || null;
          this.hasMore = !!data.next;
        } else {
          this.hasMore = false;
        }
      } catch (err) {
        console.error("Error loading more generalizations:", err);
      } finally {
        this.loadingMore = false;
      }
    },
    
    async fetchUnreadCount() {
      // Keep it for backward compatibility, but routes to fetchCounts
      await this.fetchCounts();
    },

    async markAsRead(id) {
      try {
        await api.post(`/chat/generalizations/${id}/mark-read/`);
        
        const isInUnreadList = this.unreadGeneralizations.some(g => g.id === id);
        const itemInMainList = this.generalizations.find(g => g.id === id);
        const isUnreadInMainList = itemInMainList && !itemInMainList.is_read;
        const isSenderWithUnreadReplies = itemInMainList && itemInMainList.unread_replies_count > 0;
        
        if (isInUnreadList || isUnreadInMainList || isSenderWithUnreadReplies) {
          this.unreadCount = Math.max(0, this.unreadCount - 1);
        }
        
        if (isInUnreadList || isUnreadInMainList) {
          this.inboxCount = Math.max(0, this.inboxCount - 1);
        }
        
        if (itemInMainList) {
          itemInMainList.is_read = true;
          if (itemInMainList.unread_replies_count > 0) {
            itemInMainList.unread_replies_count = 0;
          }
        }
        
        this.unreadGeneralizations = this.unreadGeneralizations.filter(g => g.id !== id);
      } catch (err) {
        console.error("Error marking generalization as read:", err);
      }
    },
    
    async submitReply(generalizationId, formData) {
      try {
        const response = await api.post(`/chat/generalizations/${generalizationId}/reply/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
      } catch (err) {
        console.error("Error submitting reply:", err);
        throw err;
      }
    },

    async fetchReplies(generalizationId, params = {}) {
      try {
        const response = await api.get(`/chat/generalizations/${generalizationId}/replies/`, { params });
        return response.data;
      } catch (err) {
        console.error("Error fetching replies:", err);
        throw err;
      }
    },

    async markReplyAsRead(generalizationId, replyId) {
      try {
        await api.post(`/chat/generalizations/${generalizationId}/mark-reply-read/`, { reply_id: replyId });
      } catch (err) {
        console.error("Error marking reply as read:", err);
        throw err;
      }
    },

    async fetchMyReply(generalizationId) {
      try {
        const response = await api.get(`/chat/generalizations/${generalizationId}/my-reply/`);
        return response.data;
      } catch (err) {
        console.error("Error fetching my reply:", err);
        throw err;
      }
    },

    async toggleStar(generalizationId) {
      try {
        const response = await api.post(`/chat/generalizations/${generalizationId}/toggle-star/`);
        const item = this.generalizations.find(g => g.id === generalizationId);
        if (item) {
          item.is_starred = response.data.status === 'starred';
        }
        return response.data;
      } catch (err) {
        console.error("Error toggling star:", err);
        throw err;
      }
    },

    async bulkMarkAsRead(ids) {
      try {
        await api.post(`/chat/generalizations/bulk-mark-read/`, { ids });
        ids.forEach(id => {
          const item = this.generalizations.find(g => g.id === id);
          if (item && !item.is_read) {
            item.is_read = true;
            this.unreadCount = Math.max(0, this.unreadCount - 1);
            this.inboxCount = Math.max(0, this.inboxCount - 1);
          }
        });
        this.unreadGeneralizations = this.unreadGeneralizations.filter(g => !ids.includes(g.id));
      } catch (err) {
        console.error("Error bulk marking as read:", err);
        throw err;
      }
    },

    async bulkDelete(ids) {
      if (!ids || !ids.length) return;
      try {
        const response = await api.post(`/chat/generalizations/bulk-delete/`, { ids });
        this.generalizations = this.generalizations.filter(g => !ids.includes(g.id));
        this.sentCount = Math.max(0, this.sentCount - response.data.deleted_count);
        return response.data;
      } catch (err) {
        console.error("Error bulk deleting:", err);
        throw err;
      }
    },

    async handleWebSocketEvent(payload) {
      // Re-fetch counts and unread list
      await this.fetchCounts();
      await this.fetchUnreadGeneralizations();
      // If we are on generalizations view, refresh the main view
      if (this.generalizations.length > 0) {
        await this.fetchGeneralizations();
      }
    }
  },
});
