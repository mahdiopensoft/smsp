import { watch } from "vue";
import { defineStore } from "pinia";
import { useNotificationWebSocket } from "../composables/useWebSocket"

 import { useChatStore } from "./chat.js"

export const useNotificationStore = defineStore("notification", {
  state: () => ({
    systemNotifications: [],
    systemNotificationsHasNext: true,
    activeAnnouncement: null,
    loading: false,
    error: null,
    _isConnected: false,
  }),

  getters: {
    unreadSystemCount: (state) => state.systemNotifications.filter((n) => !n.is_read).length,
    isConnected: (state) => state._isConnected,
  },

  actions: {
    async requestPermission() {
      if (!("Notification" in window)) {
        return false;
      }

      if (Notification.permission === "granted") {
        return true;
      }

      if (Notification.permission !== "denied") {
        const permission = await Notification.requestPermission();
        return permission === "granted";
      }

      return false;
    },

    // ==========================================
    // 🌍 WEBSOCKET & INITIALIZATION REGION
    // ==========================================
    initWebSocket() {
      if (this._wsInitialized) return;
      this.requestPermission();
      const { connect, on, isConnected } = useNotificationWebSocket();
      const chatStore = useChatStore();
      watch(
        isConnected,
        (val) => {
          this._isConnected = val;
        },
        { immediate: true }
      );
      if (!isConnected.value) connect();


      // الرسائل الجديدة والتنبيهات
      on("chat_message_notification", (data) => {
        if (data.message) chatStore.addIncomingMessage(data.message);
      });

      on("messages_read", (data) => {
        if (data.message_ids) chatStore.markMessagesAsRead(data.message_ids);
      });

      on("messages_delivered", (data) => {
        if (data.message_ids) chatStore.markMessagesAsDelivered(data.message_ids);
      });
      
      on("system_notification", (data) => {
        this.addSystemNotification(data.payload);
      });
      
      on("generalization_event", (data) => {
        import('./generalizationStore').then(({ useGeneralizationStore }) => {
          const genStore = useGeneralizationStore();
          const oldUnreadCount = genStore.unreadCount;
          
          genStore.handleWebSocketEvent(data.payload).then(() => {
             if (genStore.unreadCount > oldUnreadCount) {
                import("../store/toastStore").then(({ useToastStore }) => {
                  let msg = data.payload.title || "لديك تعميم إداري جديد";
                  if (data.payload.requires_reply) {
                      msg += " (يتطلب الرد)";
                  }
                  useToastStore().showInteractiveToast({
                    title: "تعميم إداري جديد",
                    message: msg,
                    color: "info",
                  });
                });
                this.playNotificationSound();
             }
          });
        });
      });

      on("generalization_reply_event", (data) => {
        import('./generalizationStore').then(({ useGeneralizationStore }) => {
          const genStore = useGeneralizationStore();
          genStore.handleWebSocketEvent(data.payload).then(() => {
            try {
              import("../store/toastStore").then(({ useToastStore }) => {
                useToastStore().showInteractiveToast({
                  title: "رد جديد على تعميم",
                  message: `قام ${data.payload.replier_name} بالرد على التعميم: ${data.payload.generalization_title}`,
                  color: "success",
                });
              });
            } catch (err) {
              console.error(err);
            }
            this.playNotificationSound();
          });
        });
      });

      on("note_reminder", (data) => {
        try {
          import("../store/toastStore").then(({ useToastStore }) => {
            useToastStore
            ().showInteractiveToast({
              title: "تذكير بملاحظة 📝",
              message: `${data.title} - ${new Date(
                data.due_date
              ).toLocaleString()}`,
              color: data.is_urgent ? "error" : "info",
            });
          });
        } catch (err) {
          console.error(err);
        }
        this.playNotificationSound();
      });

      on("user_status_update", (data) =>
        chatStore.updateUserStatus(data.user_id, data.is_online)
      );
      on("user_profile_updated", (data) => chatStore.updateUser(data));
      on("group_notification", (data) =>
        chatStore.handleGroupNotification(data)
      );
      on("reaction_update", (data) => chatStore.updateReaction(data));
      on("messaging_status_changed", (data) =>
        chatStore.handleGroupNotification({
          notification_type: "messaging_status_changed",
          chat_id: data.chat_id,
          data: data,
        })
      );

      on("message_edited", (data) => {
        const message = chatStore.messages.find(
          (m) => m.id === data.message_id
        );
        if (message) {
          message.content = data.new_content;
          message.updated_at = data.updated_at;
        }
      });

      on("reaction_notification", (data) => {
        const msg = `${data.reactor_name} ${
          data.action === "updated" ? "غيّر تفاعله إلى" : "تفاعل بـ"
        } ${data.emoji} على رسالتك`;
        try {
          import("../store/toastStore").then(({ useToastStore }) => {
            useToastStore().showInteractiveToast({
              title: "تفاعل جديد",
              message: msg,
              avatar: data.reactor_avatar,
            });
          });
        } catch (err) {
          console.error(err);
        }
        this.playNotificationSound();
      });

      // استلام إشعارات الوسيط المركزي (Core Notification Broker)
      on("dynamic_notification", (data) => {
        const payload = data.payload || data;
        let currentList = this.systemNotifications;
        if (!Array.isArray(currentList)) currentList = [];
        this.systemNotifications = [payload, ...currentList];

        if (
          payload.event_type === "news" ||
          payload.event_type === "announcement"
        ) {
          this.activeAnnouncement = payload;
          this.playNotificationSound();
        } else {
          try {
            import("../store/toastStore").then(({ useToastStore }) => {
              const getColor = () => {
                if (
                  payload.priority === "high" ||
                  payload.event_type === "alert"
                )
                  return "error";
                if (payload.event_type === "success") return "success";
                if (payload.event_type === "warning") return "warning";
                return "info";
              };
              useToastStore().showInteractiveToast({
                title: payload.title,
                message: payload.message,
                color: getColor(),
              });
            });
          } catch (err) {
            console.error(err);
          }
          if (payload.priority !== "low") this.playNotificationSound();
        }
      });

      this._wsInitialized = true;
    },

    clearActiveAnnouncement() {
      this.activeAnnouncement = null;
    },

    // ==========================================
    // 📢 SYSTEM NOTIFICATIONS REGION (التعميمات والشات)
    // ==========================================
    async fetchSystemNotifications(page = 1, append = false, force = false) {
      if (!append && !force && this.systemNotifications.length > 0) {
        return;
      }
      try {
        const { systemNotificationService } = await import(
          "../services/systemNotificationService"
        );
        const data = await systemNotificationService.getNotifications(page);
        const results = data.results || (Array.isArray(data) ? data : []);
        this.systemNotificationsHasNext = !!(
          data.pagination?.links?.next || !!data.next
        );

        if (append) {
          const existingIds = new Set(
            this.systemNotifications.map((n) => n.id)
          );
          const newItems = results.filter((n) => !existingIds.has(n.id));
          this.systemNotifications = [...this.systemNotifications, ...newItems];
        } else {
          this.systemNotifications = results;
        }
      } catch (error) {
        console.error("Failed to fetch system notifications:", error);
        if (!append) this.systemNotifications = [];
      }
    },

    async markSystemAsRead(id) {
      try {
        const { systemNotificationService } = await import(
          "../services/systemNotificationService"
        );
        await systemNotificationService.markAsRead(id);
        const notif = this.systemNotifications.find((n) => n.id === id);
        if (notif) notif.is_read = true;
      } catch (error) {
        console.error("Failed to mark system notification as read:", error);
      }
    },

    async markAllSystemAsRead() {
      try {
        const { systemNotificationService } = await import(
          "../services/systemNotificationService"
        );
        await systemNotificationService.markAllAsRead();
        if (this.systemNotifications) {
          this.systemNotifications.forEach((n) => (n.is_read = true));
        }
      } catch (error) {
        console.error(
          "Failed to mark all system notifications as read:",
          error
        );
      }
    },


    // ==========================================
    // 🎵 AUDIO & UTILS REGION
    // ==========================================
    async playNotificationSound() {
      if (localStorage.getItem("enable_system_sounds") === "false") return;
      try {
        const selectedTone =
          localStorage.getItem("notification_sound_tone") || "iphone";
        if (selectedTone === "custom") {
          try {
            const { audioStorage } = await import("../utils/audioStorage");
            const blob = await audioStorage.getSound("custom_message_sound");
            if (blob) {
              const audio = new Audio(URL.createObjectURL(blob));
              audio.volume = 1.0;
              audio.play().catch(async () => {
                const { audioSynthesizer } = await import(
                  "../utils/audioSynthesizer"
                );
                audioSynthesizer.playMarimba();
              });
              return;
            }
          } catch (err) {
            console.error(err);
          }
        }
        let audioUrl = "/iphone.mp3?v=3";
        if (selectedTone === "note") audioUrl = "/note.mp3?v=3";
        else if (selectedTone === "ping") audioUrl = "/ping.mp3?v=3";
        const audio = new Audio(audioUrl);
        audio.volume = 1.0;
        audio.play().catch(async () => {
          const { audioSynthesizer } = await import("../utils/audioSynthesizer");
          if (selectedTone === "ping") audioSynthesizer.playPing();
          else if (selectedTone === "note") audioSynthesizer.playNote();
          else audioSynthesizer.playMarimba();
        });
      } catch {}
    },

    reset() {
      this._wsInitialized = false;
      this.systemNotifications = [];
      this._isConnected = false;
    },
  },
});
