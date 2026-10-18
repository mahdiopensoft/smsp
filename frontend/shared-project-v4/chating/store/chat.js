/**
 * Chat Store - Chat and messages state management
 */

import { defineStore } from "pinia";
// import router from "@/router";
import { chatService } from "../services/chatService";
import { useAuthStore } from "../../src/UserManagement/stores/auth";

// import { state } from "../store/state";

let messageAudio = null;

export const useChatStore = defineStore("chat", {
  state: () => ({
    chats: [],
    activeChat: null,
    activeChatId: null,
    messages: [],
    isLoadingChats: false,
    isLoadingMessages: false,
    isLoadingMore: false,
    hasMoreMessages: false,
    nextPage: 1,
    isSending: false,
    searchQuery: "",
    typingUsers: [], // قائمة المستخدمين الذين يكتبون
    unreadCounts: {}, // عدد الرسائل غير المقروءة لكل محادثة
    pendingChatFetches: new Set(), // لمنع جلب نفس المحادثة مرتين
    recentMessageIds: new Set(), // لمنع تكرار معالجة الرسائل
    starredMessages: [], // قائمة الرسائل المميزة بنجمة

    // حالة الوسائط المشاركة
    // { chatId: { media: [...], files: [...], audio: [...] } }
    sharedMedia: {},
    isFetchingSharedMedia: false, 
    
    isQuickChatOpen: false,
  }),

  getters: {
    /**
     * المحادثات المفلترة حسب البحث
     */

    filteredChats: (state) => {
      if (!state.searchQuery) {
        return state.chats;
      }
      const query = state.searchQuery.toLowerCase().trim();
      return state.chats.filter((chat) => {
        const name = chat.name || "";
        const other = chat.other_participant || {};
        
        const searchableText = [
          name,
          other.username,
          other.full_name,
          other.first_name,
          other.last_name
        ].filter(Boolean).join(" ").toLowerCase();

        return searchableText.includes(query);
      });
    },

    /**
     * المحادثات المثبتة
     */
    pinnedChats: (state) => state.chats.filter((chat) => chat.is_pinned),

    /**
     * المحادثات غير المثبتة
     */
    unpinnedChats: (state) => state.chats.filter((chat) => !chat.is_pinned),

    /**
     * إجمالي الرسائل غير المقروءة
     */
    totalUnread: (state) =>
      Object.values(state.unreadCounts).reduce((a, b) => a + b, 0),

    /**
     * هل هناك من يكتب في المحادثة النشطة؟
     */
    isTyping: (state) => state.typingUsers.length > 0,

    /**
     * نص مؤشر الكتابة
     */
    typingText: (state) => {
      if (state.typingUsers.length === 0) {
        return "";
      }
      if (state.typingUsers.length === 1) {
        return `${state.typingUsers[0]} يكتب...`;
      }
      return `${state.typingUsers.length} يكتبون...`;
    },
  },

  actions: {
    userId() {
      const authStore = useAuthStore();
      if (authStore?.user?.id) return authStore.user.id;
      
      if (authStore?.accessToken) {
        try {
          const payload = JSON.parse(atob(authStore.accessToken.split(".")[1]));
          if (payload && payload.user_id) return payload.user_id;
        } catch(e) {}
      }

      try {
        let pStr = localStorage.getItem('profile');
        if (pStr) {
          let p = JSON.parse(pStr);
          let id = p.id || p.user_id || p.data?.id || p.data?.user_id;
          if (id) return id;
        }
        let uStr = localStorage.getItem('user');
        if (uStr) {
          let u = JSON.parse(uStr);
          let id = u.id || u.user_id || u.data?.id || u.data?.user_id;
          if (id) return id;
        }
        
        let tStr = localStorage.getItem('token');
        if (tStr) {
          const payload = JSON.parse(atob(tStr.split(".")[1]));
          if (payload && payload.user_id) return payload.user_id;
        }
      } catch(e) {}

      return null;
    },

    /**
     * تبديل نافذة المحادثة السريعة
     */
    toggleQuickChat() {
      this.isQuickChatOpen = !this.isQuickChatOpen;
    },

    /**
     * تحميل المحادثات
     */
    async fetchChats() {
      this.isLoadingChats = true;
      try {
        const chats = await chatService.getChats();
        const chatsArray = Array.isArray(chats)
          ? chats
          : chats.results
          ? chats.results
          : chats.data
          ? chats.data
          : [];
        this.chats = chatsArray;

        // تحديث عدد الرسائل غير المقروءة
        for (const chat of chatsArray) {
          if (chat.unread_count) {
            this.unreadCounts[chat.id] = chat.unread_count;
          }
        }

        return chatsArray;
      } catch (error) {
        throw error;
      } finally {
        this.isLoadingChats = false;
      }
    },

    /**
     * تحديد المحادثة النشطة
     */
    async setActiveChat(chatId) {
      const normalizedNewId = chatId ? String(chatId) : null;
      const normalizedCurrentId = this.activeChatId
        ? String(this.activeChatId)
        : null;

      if (normalizedNewId === normalizedCurrentId && this.activeChat) {
        return;
      }

      this.activeChatId = chatId;
      this.messages = [];
      this.typingUsers = [];

      if (chatId) {
        const chat = this.chats.find((c) => String(c.id) === String(chatId));
        if (chat) {
          this.activeChat = chat;
        } else {
          try {
            this.activeChat = await chatService.getChat(chatId);
          } catch (error) {
            this.activeChat = null;
          }
        }

        if (this.activeChat) {
          await this.fetchMessages(chatId);
          const incomingMessages = this.messages.filter(
            (m) => m.sender?.id !== this.userId
          );

          if (incomingMessages.length > 0) {
            const unreadIds = incomingMessages
              .filter((m) => !m.is_read)
              .map((m) => m.id);

            const latestMessage = incomingMessages.at(-1);
            const latestId = latestMessage.id;

            // نرسل معرفات غير المقروءة بالإضافة لآخر رسالة (حتى لو كانت مقروءة لضمان تحديث المؤشر)
            const idsToSend = [...new Set([...unreadIds, latestId])];

            if (idsToSend.length > 0) {
              chatService
                .markAsRead(chatId, idsToSend)
                .catch((error) => console.error("Failed to mark read", error));

              // تحديث الحالة محلياً
              for (const m of this.messages) {
                if (idsToSend.includes(m.id)) {
                  m.is_read = true;
                }
              }
            }
          }
        }

        // مسح عدد غير المقروءة
        this.unreadCounts[chatId] = 0;
      } else {
        this.activeChat = null;
      }
    },

    async refreshActiveChat() {
      if (!this.activeChatId) return;
      try {
        const chatData = await chatService.getChat(this.activeChatId);
        this.activeChat = chatData;

        const index = this.chats.findIndex(
          (c) => String(c.id) === String(this.activeChatId)
        );
        if (index !== -1) {
          this.chats[index] = { ...this.chats[index], ...chatData };
        }
        return chatData;
      } catch (error) {
        // console.error("Failed to refresh active chat:", error);
      }
    },
    /**
     * تحميل الرسائل
     */
    async fetchMessages(chatId, page = 1) {
      if (page === 1) {
        this.isLoadingMessages = true;
      } else {
        this.isLoadingMore = true;
      }
      try {
        const data = await chatService.getMessages(chatId, page);
        const results = Array.isArray(data.results) ? data.results : [];
        const reversed = [...results].reverse();

        if (page === 1) {
          this.messages = reversed;
        } else {
          this.messages = [...reversed, ...this.messages];
        }

        const pagination = data.pagination || {};
        const hasNext = pagination.links ? !!pagination.links.next : !!data.next;
        
        this.hasMoreMessages = hasNext;
        this.nextPage = hasNext ? page + 1 : null;

        return data;
      } catch (error) {
        console.error("Error fetching messages:", error);
        throw error;
      } finally {
        if (page === 1) {
          this.isLoadingMessages = false;
        } else {
          this.isLoadingMore = false;
        }
      }
    },

    /**
     * جلب الوسائط المشاركة
     */
    async fetchSharedMedia(chatId, filterType = 'media', page = 1) {
      if (!this.sharedMedia[chatId]) {
        this.sharedMedia[chatId] = { media: [], files: [], audio: [] };
      }
      
      this.isFetchingSharedMedia = true;
      try {
        const data = await chatService.getSharedMedia(chatId, filterType, page);
        
        // إذا كان يحتوي على نتائج pagination
        const items = Array.isArray(data) ? data : (data.results || []);
        
        if (page === 1) {
          this.sharedMedia[chatId][filterType] = items;
        } else {
          // إضافة العناصر الجديدة بدون تكرار
          const existingIds = new Set(this.sharedMedia[chatId][filterType].map(m => m.id));
          const newItems = items.filter(m => !existingIds.has(m.id));
          this.sharedMedia[chatId][filterType].push(...newItems);
        }
        
        return data; // للتعامل مع pagination (next, previous)
      } catch (error) {
        console.error("Failed to fetch shared media", error);
        throw error;
      } finally {
        this.isFetchingSharedMedia = false;
      }
    },

    /**
     * إعادة توجيه الرسائل
     */
    async forwardMessages(messageIds, chatIds) {
      try {
        // نرسل كل رسالة لكل المحادثات المختارة
        // يمكن تحسين الباك اند لاستقبال مصفوفة رسائل، لكن هنا سنقوم بالتكرار
        const promises = messageIds.map((msgId) =>
          chatService.forwardMessage(msgId, chatIds)
        );
        await Promise.all(promises);
        return { success: true };
      } catch (error) {
        console.error("Error forwarding messages:", error);
        throw error;
      }
    },

    /**
     * إرسال رسالة
     */
    async sendMessage(content, replyTo = null, messageType = "text") {
      if (!this.activeChatId) {
        return;
      }

      this.isSending = true;
      try {
        const data = await chatService.sendMessage(
          this.activeChatId,
          content,
          replyTo,
          messageType
        );

        if (data.message && data.message.id) {
          this.recentMessageIds.add(String(data.message.id));
        }

        const messageExists =
          this.messages &&
          Array.isArray(this.messages) &&
          this.messages.some((m) => String(m.id) === String(data.message.id));
        if (!messageExists) {
          if (!Array.isArray(this.messages)) this.messages = [];
          this.messages = [...this.messages, data.message];
          this.updateChatLastMessage(this.activeChatId, data.message);
        }
        return data.message;
      } catch (error) {
        console.error("Error sending message:", error);
        throw error;
      } finally {
        this.isSending = false;
      }
    },

    /**
     * إرسال ملف
     */
    async sendFile(file, messageType = "file", caption = "") {
      if (!this.activeChatId) {
        return;
      }

      this.isSending = true;
      try {
        const data = await chatService.sendFile(
          this.activeChatId,
          file,
          messageType,
          caption
        );
        const messageExists =
          this.messages &&
          Array.isArray(this.messages) &&
          this.messages.some((m) => String(m.id) === String(data.message.id));
        if (!messageExists) {
          if (!Array.isArray(this.messages)) this.messages = [];
          this.messages = [...this.messages, data.message];
        }
        return data.message;
      } catch (error) {
        console.error("Error sending file:", error);
        throw error;
      } finally {
        this.isSending = false;
      }
    },

    /**
     * تعديل رسالة
     */
    async editMessage(messageId, content) {
      try {
        const data = await chatService.editMessage(messageId, content);

        // تحديث الرسالة في القائمة
        if (Array.isArray(this.messages)) {
          const index = this.messages.findIndex((m) => m.id === messageId);
          if (index !== -1) {
            this.messages[index] = {
              ...this.messages[index],
              content: data.message.content,
              is_edited: true,
            };
          }
        }

        // تحديث آخر رسالة في المحادثة إذا كانت هي المعدلة
        if (this.activeChatId) {
          const chatIndex = this.chats.findIndex(
            (c) => c.id === this.activeChatId
          );
          if (
            chatIndex !== -1 &&
            this.chats[chatIndex].last_message?.id === messageId
          ) {
            this.chats[chatIndex].last_message = {
              ...this.chats[chatIndex].last_message,
              content: data.message.content,
            };
          }
        }

        return data.message;
      } catch (error) {
        console.error("Error editing message:", error);
        throw error;
      }
    },

    /**
     * إنشاء محادثة جديدة
     */
    async createChat(data) {
      try {
        const result = await chatService.createChat(data);
        // إضافة المحادثة للقائمة إذا لم تكن موجودة
        const existingIndex = this.chats.findIndex(
          (c) => c.id === result.chat.id
        );
        if (existingIndex === -1) {
          this.chats.unshift(result.chat);
        }
        return result.chat;
      } catch (error) {
        console.error("Error creating chat:", error);
        throw error;
      }
    },

    /**
     * تبديل تثبيت المحادثة
     */
    async togglePin(chatId) {
      try {
        const result = await chatService.togglePinChat(chatId);
        const chatIndex = this.chats.findIndex((c) => c.id === chatId);
        if (chatIndex !== -1) {
          this.chats[chatIndex].is_pinned = result.is_pinned;
        }
        return result;
      } catch (error) {
        console.error("Error toggling pin:", error);
        throw error;
      }
    },

    /**
     * تبديل كتم الإشعارات
     */
    async toggleMute(chatId) {
      try {
        const result = await chatService.toggleMuteChat(chatId);
        const chatIndex = this.chats.findIndex((c) => c.id === chatId);
        if (chatIndex !== -1) {
          this.chats[chatIndex].is_muted = result.is_muted;
        }
        return result;
      } catch (error) {
        console.error("Error toggling mute:", error);
        throw error;
      }
    },

    /**
     * تبديل أرشفة المحادثة
     */
    async toggleArchive(chatId) {
      try {
        const result = await chatService.toggleArchiveChat(chatId);
        const chatIndex = this.chats.findIndex((c) => c.id === chatId);
        if (chatIndex !== -1) {
          this.chats[chatIndex].is_archived = result.is_archived;
        }
        return result;
      } catch (error) {
        console.error("Error toggling archive:", error);
        throw error;
      }
    },

    /**
     * تفعيل/تعطيل المراسلة للمشرفين فقط
     */
    async toggleReadOnly(chatId) {
      try {
        const data = await chatService.toggleReadOnly(chatId);
        // تحديث المحادثة محلياً
        const chat = this.chats.find((c) => c.id === chatId);
        if (chat) {
          chat.is_read_only = data.is_read_only;
        }
        if (this.activeChat && this.activeChat.id === chatId) {
          this.activeChat.is_read_only = data.is_read_only;
        }
        return data;
      } catch (error) {
        console.error("Failed to toggle read-only mode", error);
        throw error;
      }
    },

    /**
     * كتم/إلغاء كتم عضو محدد
     */
    async toggleMemberMessaging(chatId, userId) {
      try {
        const data = await chatService.toggleMemberMessaging(chatId, userId);
        // تحديث حالة العضو في المحادثة النشطة
        if (this.activeChat && this.activeChat.id === chatId) {
          const participant = this.activeChat.participants_data.find(
            (p) => p.user.id === userId
          );
          if (participant) {
            participant.can_send_messages = data.can_send_messages;
          }
        }
        return data;
      } catch (error) {
        console.error("Failed to toggle member messaging", error);
        throw error;
      }
    },

    /**
     * تثبيت رسالة
     */
    async pinMessage(chatId, messageId) {
      try {
        const data = await chatService.pinMessage(chatId, messageId);
        // تحديث المحادثة محلياً بالرسالة المثبتة
        const message = this.messages.find((m) => m.id === messageId);
        if (message) {
          const chat = this.chats.find((c) => c.id === chatId);
          if (chat) {
            chat.pinned_message = messageId;
            chat.pinned_message_data = message;
          }
          if (this.activeChat && this.activeChat.id === chatId) {
            this.activeChat.pinned_message = messageId;
            this.activeChat.pinned_message_data = message;
          }
        }
        return data;
      } catch (error) {
        console.error("Failed to pin message", error);
        throw error;
      }
    },

    /**
     * إلغاء تثبيت الرسالة
     */
    async unpinMessage(chatId) {
      try {
        await chatService.unpinMessage(chatId);
        const chat = this.chats.find((c) => c.id === chatId);
        if (chat) {
          chat.pinned_message = null;
          chat.pinned_message_data = null;
        }
        if (this.activeChat && this.activeChat.id === chatId) {
          this.activeChat.pinned_message = null;
          this.activeChat.pinned_message_data = null;
        }
      } catch (error) {
        console.error("Failed to unpin message", error);
        throw error;
      }
    },

    /**
     * حذف المحادثة
     */
    async deleteChat(chatId, deleteForAll = false) {
      try {
        try {
          await chatService.updateWallpaper(chatId, "");
        } catch (e) {
          console.warn("Could not clear wallpaper before deleting chat:", e);
        }
        await chatService.deleteChat(chatId, deleteForAll);

        // إزالة المحادثة من القائمة المحلية
        this.chats = this.chats.filter((c) => c.id !== chatId);

        // إذا كانت المحادثة المحذوفة هي النشطة، نزيل التفعيل
        if (this.activeChatId === chatId) {
          this.activeChatId = null;
          this.activeChat = null;
          this.messages = [];
        }

        // إزالة عدد غير المقروءة
        delete this.unreadCounts[chatId];

        return { success: true };
      } catch (error) {
        console.error("Error deleting chat:", error);
        throw error;
      }
    },

    /**
     * حذف رسالة
     */
    async deleteMessage(messageId) {
      try {
        await chatService.deleteMessage(messageId);

        // إزالة الرسالة من القائمة المحلية
        this.messages = this.messages.filter((m) => m.id !== messageId);

        return { success: true };
      } catch (error) {
        console.error("Error deleting message:", error);
        throw error;
      }
    },

    /**
     * مسح جميع رسائل المحادثة
     */
    async clearChat(chatId) {
      try {
        await chatService.clearChat(chatId);

        // مسح الرسائل محلياً إذا كانت المحادثة نشطة
        if (this.activeChatId === chatId) {
          this.messages = [];
        }

        // تحديث آخر رسالة في قائمة المحادثات
        const chatIndex = this.chats.findIndex((c) => c.id === chatId);
        if (chatIndex !== -1) {
          this.chats[chatIndex].last_message = null;
        }

        return { success: true };
      } catch (error) {
        console.error("Error clearing chat:", error);
        throw error;
      }
    },

    /**
     * تبديل كتم الإشعارات
     */
    async toggleMute(chatId) {
      try {
        const result = await chatService.toggleMuteChat(chatId);
        const chatIndex = this.chats.findIndex((c) => c.id === chatId);
        if (chatIndex !== -1) {
          this.chats[chatIndex].is_muted = result.is_muted;
        }
        return result;
      } catch (error) {
        console.error("Error toggling mute:", error);
        throw error;
      }
    },

    /**
     * تبديل أرشفة المحادثة
     */
    async toggleArchive(chatId) {
      try {
        const result = await chatService.toggleArchiveChat(chatId);
        const chatIndex = this.chats.findIndex((c) => c.id === chatId);
        if (chatIndex !== -1) {
          this.chats[chatIndex].is_archived = result.is_archived;
        }
        return result;
      } catch (error) {
        console.error("Error toggling archive:", error);
        throw error;
      }
    },

    /**
     * تفعيل/تعطيل المراسلة للمشرفين فقط
     */
    async toggleReadOnly(chatId) {
      try {
        const data = await chatService.toggleReadOnly(chatId);
        // تحديث المحادثة محلياً
        const chat = this.chats.find((c) => c.id === chatId);
        if (chat) {
          chat.is_read_only = data.is_read_only;
        }
        if (this.activeChat && this.activeChat.id === chatId) {
          this.activeChat.is_read_only = data.is_read_only;
        }
        return data;
      } catch (error) {
        console.error("Failed to toggle read-only mode", error);
        throw error;
      }
    },

    /**
     * تحديث آخر رسالة في المحادثة
     */
    async updateChatLastMessage(chatId, message) {
      const chatIndex = this.chats.findIndex((c) => c.id === chatId);
      if (chatIndex === -1) {
        // تحقق إذا كان هناك طلب جاري لهذه المحادثة
        if (this.pendingChatFetches.has(chatId)) {
          return;
        }

        // المحادثة غير موجودة - نجلبها من الـ API ونضيفها
        this.pendingChatFetches.add(chatId);
        try {
          const newChat = await chatService.getChat(chatId);
          if (newChat) {
            // تحقق مرة أخرى بعد الـ await لتجنب التكرار (race condition)
            const existingIndex = this.chats.findIndex((c) => c.id === chatId);
            if (existingIndex === -1) {
              newChat.last_message = message;
              const pinnedCount = this.chats.filter((c) => c.is_pinned).length;
              this.chats.splice(pinnedCount, 0, newChat);
            } else {
              // المحادثة أُضيفت بالفعل بواسطة طلب آخر، فقط نحدث الرسالة الأخيرة
              this.chats[existingIndex].last_message = message;
            }
          }
        } catch (error) {
          console.error("Error fetching new chat:", error);
        } finally {
          this.pendingChatFetches.delete(chatId);
        }
      } else {
        this.chats[chatIndex].last_message = message;
        // نقل المحادثة للأعلى
        const chat = this.chats.splice(chatIndex, 1)[0];
        const pinnedCount = this.chats.filter((c) => c.is_pinned).length;
        if (chat.is_pinned) {
          this.chats.unshift(chat);
        } else {
          this.chats.splice(pinnedCount, 0, chat);
        }
      }
    },

    /**
     * إضافة رسالة واردة (من WebSocket)
     */
    async addIncomingMessage(message) {
      // 1. Check strict deduplication using recentMessageIds
      if (this.recentMessageIds.has(String(message.id))) {
        console.warn(`[ChatStore] Duplicate suppressed: ${message.id}`);
        return;
      }
      this.recentMessageIds.add(String(message.id));

      // Cleanup old IDs to prevent memory leak (keep last 100)
      if (this.recentMessageIds.size > 100) {
        const first = this.recentMessageIds.values().next().value;
        this.recentMessageIds.delete(first);
      }

      const isHidden =
        document.hidden || document.visibilityState !== "visible";
      const isVisible = !isHidden && document.hasFocus();
      const isForActiveChat =
        this.activeChatId && String(message.chat) === String(this.activeChatId);

      // 2. Add to messages list if active chat
      if (isForActiveChat) {
        // Double check against current list just in case

        const messageExists =
          this.messages &&
          Array.isArray(this.messages) &&
          this.messages.some((m) => m && String(m.id) === String(message.id));
        if (!messageExists) {
          if (!Array.isArray(this.messages)) this.messages = [];
          this.messages = [...this.messages, message];

          // Mark read if visible
          if (isVisible && String(message.sender?.id) !== String(this.userId)) {
            chatService
              .markAsRead(message.chat, [message.id])
              .catch(console.error);
          }
        }
      }

      // انتظر جلب تفاصيل المحادثة من الخادم بالكامل لتجنب undefined في الإشعارات
      if (message.chat) {
        await this.updateChatLastMessage(message.chat, message);
      }

      // 3. تحديد ما إذا كان يجب تشغيل تنبيه (صوت/إشعار)
      const isChattingViewOpen = window.location.pathname.includes('/chatting');
      const isCurrentChatOpen = (this.isQuickChatOpen || isChattingViewOpen) && String(message.chat) === String(this.activeChatId);
      const isFromMe = String(message.sender?.id) === String(this.userId);

      if (!isFromMe) {
        if (isCurrentChatOpen && !isHidden) {
          // المحادثة مفتوحة والنافذة ظاهرة للمستخدم، لا داعي لتشغيل أي إشعار أو صوت
        } else {
          // المحادثة مغلقة أو المستخدم في تبويب آخر أو يتصفح محادثة أخرى
          this.triggerNotification(message);
        }
      }
    },

    /**
     * تشغيل الإشعار (صوت + سطح مكتب)
     */
    async triggerNotification(message) {
      if (message.chat !== this.activeChatId) {
        this.unreadCounts[message.chat] =
          (this.unreadCounts[message.chat] || 0) + 1;
      }

      const chat = this.chats.find((c) => String(c.id) === String(message.chat));
      const isMuted = chat?.is_muted || false;

      const currentUserId = this.userId;
      const isDirectReply =
        message.reply_to &&
        String(message.reply_to.sender?.id) === String(currentUserId);

      if (isMuted && !isDirectReply) {
        return;
      }

      const soundEnabled =
        localStorage.getItem("notification_sound") !== "false";
      const desktopEnabled =
        localStorage.getItem("notification_desktop") !== "false";

      if (soundEnabled) {
        try {
          const selectedTone =
            localStorage.getItem("notification_sound_tone") || "iphone";

          if (!messageAudio) {
            messageAudio = new Audio();
          }

          if (selectedTone === "custom") {
            try {
              const { audioStorage } = await import("../utils/audioStorage");
              const blob = await audioStorage.getSound("custom_message_sound");
              if (blob) {
                const url = URL.createObjectURL(blob);
                try {
                  messageAudio.pause();
                } catch (e) {}
                messageAudio.src = url;
                messageAudio.volume = 1.0;
                messageAudio.play().catch(async (e) => {
                  console.error(
                    "Custom message sound play failed, using fallback:",
                    e
                  );
                  try {
                    const { audioSynthesizer } = await import(
                      "../utils/audioSynthesizer"
                    );
                    audioSynthesizer.playMarimba();
                  } catch (err) {
                    console.error("Synthesizer fallback failed:", err);
                  }
                });
              }
            } catch (err) {
              console.error("Failed to load custom message tone:", err);
            }
          } else {
            let audioUrl = "/iphone.mp3?v=3";
            if (selectedTone === "note") audioUrl = "/note.mp3?v=3";
            else if (selectedTone === "ping") audioUrl = "/ping.mp3?v=3";
            else if (selectedTone === "notification")
              audioUrl = "/notification.mp3?v=3";
            try {
              messageAudio.pause();
            } catch (e) {}
            messageAudio.src = audioUrl;
            const audio = messageAudio;
            audio.volume = 1.0;
            audio.play().catch(async (error) => {
              console.warn(
                "Audio play failed, executing synthesizer fallback:",
                error
              );
              try {
                const { audioSynthesizer } = await import(
                  "../utils/audioSynthesizer"
                );
                if (selectedTone === "ping") audioSynthesizer.playPing();
                else if (selectedTone === "note") audioSynthesizer.playNote();
                else audioSynthesizer.playMarimba();
              } catch (e) {
                console.error("Synthesizer fallback failed:", e);
              }
            });
          }
        } catch (error) {
          console.error("Error playing audio:", error);
        }
      }

      // عرض التنبيه التفاعلي الجذاب داخل التطبيق (Premium Clickable Toast)
      try {
        const { useToastStore } = await import("../store/toastStore");
        const toastStore = useToastStore();

        const senderName =
          message.sender?.first_name || message.sender?.username || "مستخدم";
        const chatName = chat?.name || senderName;
        const title =
          chat?.chat_type === "group"
            ? `${senderName} في ${chatName}`
            : senderName;
        const bodyText =
          message.content ||
          (message.message_type === "image"
            ? "📷 صورة"
            : message.message_type === "sticker"
            ? "🎴 ملصق"
            : message.message_type === "audio"
            ? "🎵 رسالة صوتية"
            : "📎 ملف");

        let avatarUrl = "";
        if (chat?.chat_type === "group") {
          if (chat.group_picture) {
            avatarUrl = chat.group_picture.startsWith("http")
              ? chat.group_picture
              : window.location.origin + chat.group_picture;
          }
        } else {
          if (message.sender && message.sender.profile_picture) {
            const pic = message.sender.profile_picture;
            avatarUrl = pic.startsWith("http")
              ? pic
              : window.location.origin + pic;
          }
        }

        toastStore.showInteractiveToast({
          title: title,
          message: bodyText,
          avatar: avatarUrl,
          color: "info",
          chatId: message.chat,
          onClick: () => {
            this.setActiveChat(message.chat);
            this.isQuickChatOpen = true;
          },
        });
      } catch (err) {
        console.error("Failed to trigger in-app notification toast:", err);
      }

      if (desktopEnabled && Notification.permission === "granted") {
        const senderName = message.sender?.first_name || "مستخدم";
        const chatName = chat?.name || senderName;
        const title =
          chat?.chat_type === "group"
            ? `${senderName} في ${chatName}`
            : senderName;

        // مولد صور محلي للأوف لاين (PNG عبر Canvas لضمان التوافق مع إشعارات ويندوز)
        const getLocalAvatar = (name, bgColor = "#00a884") => {
          const initial = (name || "?").charAt(0).toUpperCase();
          const colors = [
            "#00a884",
            "#128c7e",
            "#075e54",
            "#34b7f1",
            "#25d366",
            "#34b7f1",
          ];
          const color = name ? colors[name.length % colors.length] : bgColor;

          const canvas = document.createElement("canvas");
          canvas.width = 128;
          canvas.height = 128;
          const ctx = canvas.getContext("2d");

          // رسم الخلفية
          ctx.fillStyle = color;
          ctx.fillRect(0, 0, 128, 128);

          // رسم الحرف
          ctx.fillStyle = "white";
          ctx.font = "bold 64px Arial";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(initial, 64, 64);

          return canvas.toDataURL("image/png");
        };

        let notificationIcon = window.location.origin + "/favicon.ico";

        if (chat?.chat_type === "group") {
          if (chat.group_picture) {
            notificationIcon = chat.group_picture.startsWith("http")
              ? chat.group_picture
              : window.location.origin + chat.group_picture;
          } else {
            notificationIcon = getLocalAvatar(chat.name, "#00a884");
          }
        } else {
          if (message.sender && message.sender.profile_picture) {
            const pic = message.sender.profile_picture;
            notificationIcon = pic.startsWith("http")
              ? pic
              : window.location.origin + pic;
          } else {
            const name =
              message.sender?.full_name || message.sender?.username || "User";
            notificationIcon = getLocalAvatar(name);
          }
        }

        const notification = new Notification(`رسالة جديدة من ${title}`, {
          body:
            message.content ||
            (message.message_type === "image"
              ? "📷 صورة"
              : message.message_type === "sticker"
              ? "🎴 ملصق"
              : "📎 ملف"),
          icon: notificationIcon,
          badge: notificationIcon,
          image: notificationIcon,
          tag: "chat-" + message.chat,
          renotify: true,
        });

        // Keep reference to prevent Garbage Collection
        window.activeNotifications = window.activeNotifications || [];
        window.activeNotifications.push(notification);

        const cleanup = () => {
          const idx = window.activeNotifications.indexOf(notification);
          if (idx !== -1) {
            window.activeNotifications.splice(idx, 1);
          }
        };

        notification.addEventListener("click", (event) => {
          event.preventDefault(); // Prevent default browser action if any
          window.focus();
          notification.close();

          this.setActiveChat(message.chat);
          this.isQuickChatOpen = true;
          cleanup();
        });

        notification.addEventListener("close", cleanup);
      }
    },

    /**
     * تشغيل صوت خفيف عند استقبال رسالة داخل المحادثة المفتوحة
     */
    async playInChatSound() {
      const soundEnabled =
        localStorage.getItem("notification_sound") !== "false";
      if (!soundEnabled) return;

      try {
        const audio = new Audio("/ping.mp3?v=3");
        audio.volume = 0.4;
        audio
          .play()
          .catch((e) => {});
      } catch (err) {
        console.error("Failed to play in-chat sound:", err);
      }
    },

    /**
     * التحقق من الرسائل غير المقروءة في المحادثة النشطة (عند العودة للصفحة)
     */
    checkActiveChatUnread() {
      if (!this.activeChatId || this.messages.length === 0) {
        return;
      }

      const unreadMessages = this.messages.filter(
        (m) => !m.is_read && m.sender?.id !== this.userId
      );

      if (unreadMessages.length > 0) {
        const ids = unreadMessages.map((m) => m.id);

        chatService.markAsRead(this.activeChatId, ids).catch(console.error);

        // تحديث محلي
        for (const m of unreadMessages) {
          m.is_read = true;
        }

        // تصفير العداد
        this.unreadCounts[this.activeChatId] = 0;
      }
    },

    /**
     * تعيين مستخدم يكتب
     */
    setUserTyping(username, isTyping) {
      if (isTyping) {
        if (!this.typingUsers.includes(username)) {
          this.typingUsers.push(username);
        }
      } else {
        this.typingUsers = this.typingUsers.filter((u) => u !== username);
      }
    },

    /**
     * تحديث حالة اتصال مستخدم (متصل/غير متصل)
     */
    updateUserStatus(userId, isOnline) {
      this.updateUser({
        user_id: userId,
        data: { is_online: isOnline },
      });
    },

    /**
     * تحديث حالة قراءة الرسائل
     */
    markMessagesAsRead(messageIds) {
      for (const id of messageIds) {
        // تحديث في الرسائل النشطة
        const msg = this.messages.find((m) => String(m.id) === String(id));
        if (msg) {
          msg.is_read = true;
        }
        // تحديث في قائمة المحادثات (آخر رسالة)
        for (const chat of this.chats) {
          if (chat.last_message && String(chat.last_message.id) === String(id)) {
            chat.last_message.is_read = true;
          }
        }
      }
    },

    /**
     * تحديث حالة تسليم الرسائل
     */
    markMessagesAsDelivered(messageIds) {
      for (const id of messageIds) {
        // تحديث في الرسائل النشطة
        const msg = this.messages.find((m) => String(m.id) === String(id));
        if (msg) {
          msg.is_delivered = true;
        }
        // تحديث في قائمة المحادثات (آخر رسالة)
        for (const chat of this.chats) {
          if (chat.last_message && String(chat.last_message.id) === String(id)) {
            chat.last_message.is_delivered = true;
          }
        }
      }
    },

    /**
     * البحث
     */
    setSearchQuery(query) {
      this.searchQuery = query;
    },

    /**
     * إزالة محادثة من القائمة
     */
    removeChat(chatId) {
      const index = this.chats.findIndex((c) => c.id === chatId);
      if (index !== -1) {
        this.chats.splice(index, 1);
      }

      if (this.activeChatId === chatId) {
        this.activeChatId = null;
        this.activeChat = null;
        this.messages = [];
      }
      delete this.unreadCounts[chatId];
    },
    /**
     * مغادرة المجموعة
     */
    async leaveChat(chatId) {
      try {
        await chatService.leaveChat(chatId);

        // إزالة من القائمة
        this.removeChat(chatId);

        return { success: true };
      } catch (error) {
        console.error("Error leaving chat:", error);
        throw error;
      }
    },

    /**
     * معالجة إشعارات المجموعة (من WebSocket)
     */
    handleGroupNotification(data) {
      const { notification_type, chat_id, data: eventData } = data;
      const chat = this.chats.find((c) => c.id === chat_id);

      switch (notification_type) {
        case "group_settings_updated": {
          if (chat) {
            Object.assign(chat, eventData);
          }
          if (this.activeChat && this.activeChat.id === chat_id) {
            // تحديث كائن المحادثة بالكامل لضمان التفاعلية
            this.activeChat = {
              ...this.activeChat,
              ...eventData,
            };
          }
          break;
        }

        case "chat_added": {
          if (eventData && eventData.chat) {
            this.addChat(eventData.chat);
            import("../store/toastStore").then(({ useToastStore }) => {
              useToastStore().showInteractiveToast({
                title: "مجموعة جديدة",
                message: `تمت إضافتك إلى مجموعة جديدة: ${eventData.chat.name || "بدون اسم"}`,
                color: "info",
              });
            });
            import("../store/notificationStore").then(({ useNotificationStore }) => {
              useNotificationStore().playNotificationSound();
            });
          }
          break;
        }

        case "group_deleted": {
          this.chats = this.chats.filter((c) => c.id !== chat_id);
          if (this.activeChatId === chat_id) {
            this.activeChatId = null;
            this.activeChat = null;
            this.messages = [];
          }
          break;
        }

        case "messaging_status_changed": {
          // تحديث حالة عضو محدد
          if (this.activeChat && this.activeChat.id == chat_id) {
            const index = this.activeChat.participants_data.findIndex(
              (p) => p.user && p.user.id == eventData.user_id
            );
            if (index !== -1) {
              const updatedParticipants = [
                ...this.activeChat.participants_data,
              ];
              updatedParticipants[index] = {
                ...updatedParticipants[index],
                can_send_messages: eventData.can_send_messages,
              };
              this.activeChat.participants_data = updatedParticipants;
            }
          }
          // تحديث في القائمة العامة أيضاً
          if (chat && chat.participants_data) {
            const index = chat.participants_data.findIndex(
              (p) => p.user && p.user.id == eventData.user_id
            );
            if (index !== -1) {
              const updatedParticipants = [...chat.participants_data];
              updatedParticipants[index] = {
                ...updatedParticipants[index],
                can_send_messages: eventData.can_send_messages,
              };
              chat.participants_data = updatedParticipants;
            }
          }
          break;
        }

        case "message_pinned": {
          if (chat) {
            chat.pinned_message = eventData.message_id;
            chat.pinned_message_data = eventData.message_data;
          }
          if (this.activeChat && this.activeChat.id === chat_id) {
            this.activeChat.pinned_message = eventData.message_id;
            this.activeChat.pinned_message_data = eventData.message_data;
          }
          break;
        }

        case "message_unpinned": {
          if (chat) {
            chat.pinned_message = null;
            chat.pinned_message_data = null;
          }
          if (this.activeChat && this.activeChat.id === chat_id) {
            this.activeChat.pinned_message = null;
            this.activeChat.pinned_message_data = null;
          }
          break;
        }

        case "member_added": {
          if (this.activeChat && this.activeChat.id === chat_id) {
            this.activeChat.participants_data.push(eventData.member);
          }
          break;
        }

        case "member_removed":
        case "member_left": {
          if (this.activeChat && this.activeChat.id === chat_id) {
            this.activeChat.participants_data =
              this.activeChat.participants_data.filter(
                (p) => p.user.id !== eventData.user_id
              );
          }
          break;
        }

        case "admin_changed": {
          if (this.activeChat && this.activeChat.id === chat_id) {
            const participant = this.activeChat.participants_data.find(
              (p) => p.user.id === eventData.user_id
            );
            if (participant) {
              participant.is_admin = eventData.is_admin;
            }
            // تحديث حالتي أنا إذا كنت أنا المعني

            if (eventData.user_id === this.userId) {
              this.activeChat.current_user_is_admin = eventData.is_admin;
              if (chat) {
                chat.current_user_is_admin = eventData.is_admin;
              }
            }
          }
          break;
        }
      }
    },

    /**
     * إضافة محادثة جديدة للقائمة (من WebSocket)
     */
    addChat(chat) {
      // التحقق من عدم وجود المحادثة مسبقاً
      const existingIndex = this.chats.findIndex((c) => c.id === chat.id);
      if (existingIndex === -1) {
        // إضافة في المكان المناسب (بعد المثبتة)
        const pinnedCount = this.chats.filter((c) => c.is_pinned).length;
        this.chats.splice(pinnedCount, 0, chat);
      }
    },

    /**
     * تحديث بيانات محادثة (من WebSocket)
     */
    updateChatData(chatId, data) {
      const chatIndex = this.chats.findIndex((c) => c.id === chatId);
      if (chatIndex !== -1) {
        // تحديث الحقول المحددة فقط
        if (data.name !== undefined) {
          this.chats[chatIndex].name = data.name;
        }
        if (data.description !== undefined) {
          this.chats[chatIndex].description = data.description;
        }
        if (data.group_picture !== undefined) {
          this.chats[chatIndex].group_picture = data.group_picture;
        }
      }

      // تحديث المحادثة النشطة إذا كانت هي نفسها
      if (this.activeChat && this.activeChat.id === chatId) {
        if (data.name !== undefined) {
          this.activeChat.name = data.name;
        }
        if (data.description !== undefined) {
          this.activeChat.description = data.description;
        }
        if (data.group_picture !== undefined) {
          this.activeChat.group_picture = data.group_picture;
        }
      }
    },

    /**
     * إضافة عضو للمحادثة (من WebSocket)
     */
    addChatMember(chatId, member) {
      // تنسيق العضو ليتوافق مع ChatParticipantSerializer
      // البيانات الواردة من الـ Socket (بعد التحديث):
      // { id: participant_id, user_id: user.id, username, full_name, ... }

      const participantData = {
        id: member.id, // هذا الآن هو participant_id الصحيح
        is_admin: member.is_admin || false,
        user: {
          id: member.user_id || member.id, // استخدام user_id إذا توفر (من التحديث الجديد) أو id كاحتياط
          username: member.username,
          full_name: member.full_name,
          profile_picture: member.profile_picture,
          is_online: member.is_online || false,
        },
      };

      // معرف المستخدم للمقارنة
      const targetUserId = participantData.user.id;

      const chatIndex = this.chats.findIndex((c) => c.id === chatId);
      if (chatIndex !== -1 && this.chats[chatIndex].participants_data) {
        // التحقق من عدم وجود العضو مسبقاً
        const exists = this.chats[chatIndex].participants_data.some(
          (p) => p.user.id === targetUserId
        );
        if (!exists) {
          this.chats[chatIndex].participants_data.push(participantData);
        }
      } else if (chatIndex !== -1 && !this.chats[chatIndex].participants_data) {
        this.chats[chatIndex].participants_data = [participantData];
      }

      // تحديث المحادثة النشطة - هذه الجزئية مهمة جداً لـ GroupInfoDialog
      if (this.activeChat && this.activeChat.id === chatId) {
        if (!this.activeChat.participants_data) {
          this.activeChat.participants_data = [];
        }

        const exists = this.activeChat.participants_data.some(
          (p) => p.user.id === targetUserId
        );
        if (!exists) {
          this.activeChat.participants_data.push(participantData);
        }
      }
    },

    /**
     * إزالة عضو من المحادثة (من WebSocket)
     */
    removeChatMember(chatId, userId) {
      const chatIndex = this.chats.findIndex((c) => c.id === chatId);
      if (chatIndex !== -1 && this.chats[chatIndex].participants_data) {
        this.chats[chatIndex].participants_data = this.chats[
          chatIndex
        ].participants_data.filter((p) => p.user.id !== userId);
      }

      // تحديث المحادثة النشطة (بشكل تفاعلي)
      if (
        this.activeChat &&
        this.activeChat.id === chatId &&
        this.activeChat.participants_data
      ) {
        this.activeChat.participants_data =
          this.activeChat.participants_data.filter((p) => p.user.id !== userId);
      }
    },

    /**
     * تحديث بيانات مستخدم (من WebSocket)
     */
    updateUser(data) {
      if (!data || !data.user_id) {
        return;
      }

      const userId = data.user_id;
      const userData = data.data; // البيانات الجديدة

      for (const chat of this.chats) {
        // تحديث في المحادثات الخاصة
        if (
          chat.chat_type === "private" &&
          String(chat.other_participant?.id) === String(userId)
        ) {
          if (userData.full_name !== undefined) {
            chat.other_participant.full_name = userData.full_name;
          }
          if (userData.profile_picture !== undefined) {
            chat.other_participant.profile_picture = userData.profile_picture;
          }
          if (userData.username !== undefined) {
            chat.other_participant.username = userData.username;
          }
          if (userData.is_online !== undefined) {
            chat.other_participant.is_online = userData.is_online;
          }
        }

        // تحديث في قائمة المشاركين (للمجموعات والخاصة)
        if (chat.participants_data) {
          const participant = chat.participants_data.find(
            (p) => String(p.user?.id) === String(userId)
          );
          if (participant && participant.user) {
            Object.assign(participant.user, userData);
          }
        }
      }

      // 2. تحديث في المحادثة النشطة
      if (this.activeChat) {
        // إذا كانت محادثة خاصة مع هذا المستخدم
        if (
          this.activeChat.chat_type === "private" &&
          String(this.activeChat.other_participant?.id) === String(userId)
        ) {
          Object.assign(this.activeChat.other_participant, userData);
          // تحديث اسم المحادثة إذا كان يعتمد على اسم المستخدم
          // (في المحادثات الخاصة الاسم يأتي عادة فارغ من السيرفر ويتم حسابه في الواجهة، لكن هنا نحدث الكائن مباشرة)
        }

        // تحديث في قائمة المشاركين
        if (this.activeChat.participants_data) {
          const participant = this.activeChat.participants_data.find(
            (p) => String(p.user?.id) === String(userId)
          );
          if (participant && participant.user) {
            Object.assign(participant.user, userData);
          }
        }
      }

      // 3. تحديث الرسائل (اختياري - قد يكون مكلفاً إذا كانت القائمة طويلة)
      // نكتفي بتحديث الرسائل الظاهرة أو التي يتم تحميلها
      for (const msg of this.messages) {
        if (msg.sender && String(msg.sender.id) === String(userId)) {
          Object.assign(msg.sender, userData);
        }
      }
    },

    /**
     * تحديث صلاحيات عضو (من WebSocket)
     */
    updateMemberRole(chatId, userId, isAdmin) {
      const chatIndex = this.chats.findIndex((c) => c.id === chatId);
      if (chatIndex !== -1 && this.chats[chatIndex].participants_data) {
        const member = this.chats[chatIndex].participants_data.find(
          (p) => p.user.id === userId
        );
        if (member) {
          member.is_admin = isAdmin;
        }
      }

      // تحديث المحادثة النشطة
      if (
        this.activeChat &&
        this.activeChat.id === chatId &&
        this.activeChat.participants_data
      ) {
        const member = this.activeChat.participants_data.find(
          (p) => p.user.id === userId
        );
        if (member) {
          member.is_admin = isAdmin;
        }
      }
    },

    /**
     * تمييز رسالة بنجمة
     */
    async toggleStar(messageId) {
      try {
        const response = await chatService.toggleStar(messageId);

        // تحديث الرسالة في القائمة المحلية
        const message = this.messages.find((m) => m.id === messageId);
        if (message) {
          message.is_starred = response.is_starred;
        }

        return response;
      } catch (error) {
        console.error("Error toggling star:", error);
        throw error;
      }
    },

    /**
     * تحميل الرسائل المميزة بنجمة
     */
    async fetchStarredMessages() {
      try {
        const messages = await chatService.getStarredMessages();
        this.starredMessages = messages.results || messages;
        return this.starredMessages;
      } catch (error) {
        console.error("Error fetching starred messages:", error);
        throw error;
      }
    },

    /**
     * تحديث خلفية المحادثة
     */
    async updateChatWallpaper(chatId, wallpaper) {
      try {
        const response = await chatService.updateWallpaper(chatId, wallpaper);

        // تحديث المحادثة محلياً
        const chatIndex = this.chats.findIndex((c) => c.id === chatId);
        if (chatIndex !== -1) {
          this.chats[chatIndex].wallpaper = wallpaper;
        }

        if (this.activeChat && this.activeChat.id === chatId) {
          this.activeChat.wallpaper = wallpaper;
        }

        return response;
      } catch (error) {
        console.error("Error updating wallpaper:", error);
        throw error;
      }
    },

    /**
     * إضافة/إزالة تفاعل
     */
    async toggleReaction(messageId, emoji) {
      try {
        const response = await chatService.toggleReaction(messageId, emoji);
        return response;
      } catch (error) {
        console.error("Error toggling reaction:", error);
        throw error;
      }
    },

    /**
     * تحديث تفاعل (من WebSocket)
     */
    updateReaction(data) {
      const { message_id, action, reaction, emoji, user_id } = data;

      // تأمين مقارنة المعرفات (تحويل الاثنين لنصوص لضمان التطابق)
      const message = this.messages.find(
        (m) => String(m.id) === String(message_id)
      );
      if (!message) {
        return;
      }

      const currentReactions = Array.isArray(message.reactions)
        ? message.reactions
        : [];

      const getUserId = (r) =>
        String(r?.user?.id || r?.user || r?.user_id || "");
      const targetUserId = String(user_id);
      switch (action) {
        case "added": {
          if (!reaction) return;

          // تاكد من عدم تكرار تفاعل لنفس المستخدم
          const filtered = currentReactions.filter(
            (r) => getUserId(r) !== targetUserId
          );
          message.reactions = [...filtered, reaction];
          break;
        }
        case "removed": {
          message.reactions = currentReactions.filter(
            (r) => getUserId(r) !== targetUserId
          );
          break;
        }
        case "updated": {
          if (!reaction) return;
          const filtered = currentReactions.filter(
            (r) => getUserId(r) !== targetUserId
          );
          message.reactions = [...filtered, reaction];
          break;
        }
      }
    },
  },
});

// إضافة مراقبة لعودة التركيز على النافذة لتحديث حالة الرسائل إلى "مقروءة"
if (typeof window !== 'undefined') {
  const handleFocusAndVisibility = () => {
    if (document.visibilityState === 'visible' && document.hasFocus()) {
      const chatStore = useChatStore();
      chatStore.checkActiveChatUnread();
    }
  };

  window.addEventListener('focus', handleFocusAndVisibility);
  document.addEventListener('visibilitychange', handleFocusAndVisibility);
}
