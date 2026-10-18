/**
 * WebSocket Composable
 * Real-time communication with Django Channels
 */

import { getCurrentInstance, onUnmounted, ref } from "vue";
import settings from "@/../settings";
import { useAuthStore } from "../../src/UserManagement/stores/auth";

export function useWebSocket(url) {
  const socket = ref(null);
  const isConnected = ref(false);
  const reconnectAttempts = ref(0);
  const maxReconnectAttempts = Infinity;

  const messageHandlers = new Map();
  const messageQueue = ref([]);

  /**
   * الاتصال بـ WebSocket
   */
  const connect = () => {
    if (!url) {
      return;
    }

    // Prevent duplicate connection attempts if already open or connecting
    if (
      socket.value &&
      (socket.value.readyState === WebSocket.OPEN ||
        socket.value.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    const wsUrl = url;

    try {
      socket.value = new WebSocket(wsUrl);

      socket.value.onopen = () => {
        isConnected.value = true;
        reconnectAttempts.value = 0;

        if (messageQueue.value.length > 0) {
          while (messageQueue.value.length > 0) {
            const { type, data } = messageQueue.value.shift();
            send(type, data);
          }
        }
      };

      socket.value.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          const handlers = messageHandlers.get(data.type);
          if (handlers) {
            handlers.forEach((handler) => {
              try {
                handler(data);
              } catch (e) {
                console.error(` Error in handler for ${data.type}:`, e);
              }
            });
          }
        } catch (error) {
          console.error(" Error parsing WebSocket message:", error);
        }
      };

      socket.value.onclose = (event) => {
        console.warn(
          `🔌 WebSocket closed. Code: ${event.code}, Reason: ${event.reason}`
        );
        isConnected.value = false;

        // إعادة الاتصال تلقائياً
        if (reconnectAttempts.value < maxReconnectAttempts) {
          reconnectAttempts.value++;
          const delay = Math.min(
            1000 * Math.pow(2, reconnectAttempts.value),
            30_000
          );
          setTimeout(connect, delay);
        }
      };

      socket.value.onerror = (error) => {
        console.error(
          " WebSocket error occurred. This usually means the connection was rejected or the server id down.:",
          error
        );
      };
    } catch (e) {
      console.log(" Error creating WebSocoket instance:", e);
    }
  };

  /**
   * إرسال رسالة
   */
  const send = (type, data = {}) => {
    if (socket.value?.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify({ type, ...data }));
    } else {
      messageQueue.value.push({ type, data });

      if (
        !socket.value ||
        socket.value.readyState === WebSocket.CLOSED ||
        socket.value.readyState === WebSocket.CLOSING
      ) {
        connect();
      }
    }
  };

  /**
   * تسجيل معالج لنوع رسالة
   */
  const on = (type, handler) => {
    if (!messageHandlers.has(type)) {
      messageHandlers.set(type, new Set());
    }
    messageHandlers.get(type).add(handler);
  };

  /**
   * إلغاء تسجيل معالج
   */
  const off = (type, handler) => {
    if (messageHandlers.has(type)) {
      if (handler) {
        messageHandlers.get(type).delete(handler);
      } else {
        messageHandlers.delete(type);
      }
    }
  };

  /**
   * قطع الاتصال
   */
  const disconnect = () => {
    if (socket.value) {
      reconnectAttempts.value = maxReconnectAttempts; // منع إعادة الاتصال
      socket.value.close();
      socket.value = null;
    }
  };

  // تنظيف عند إلغاء المكون فقط إذا تم استدعاء الكومبوزبل في مرحلة الـ setup
  if (getCurrentInstance()) {
    onUnmounted(() => {
      disconnect();
    });
  }

  return {
    socket,
    isConnected,
    connect,
    send,
    on,
    off,
    disconnect,
  };
}

/**
 * Chat WebSocket Composable
 * For specific chat connections
 */
export function useChatWebSocket(chatId) {
  const wsBaseUrl =
    import.meta.env.VITE_WS_URL ||
    (settings.url || import.meta.env.VITE_WS_URL || window.location.origin)
      .replace(/^http/, "ws")
      .replace(/\/?$/, "")
      .replace(/\/$/, "");
  
  const authStore = useAuthStore();
  const token = authStore.accessToken || authStore.token || "";
  const url = `${wsBaseUrl}/ws/chat/${chatId}/?token=${token}`;

  const { socket, isConnected, connect, send, on, off, disconnect } =
    useWebSocket(url);

  // إرسال رسالة نصية
  const sendMessage = (content, replyTo = null) => {
    send("chat_message", { content, reply_to: replyTo });
  };

  // بدء الكتابة
  const startTyping = () => {
    send("typing_start");
  };

  // إيقاف الكتابة
  const stopTyping = () => {
    send("typing_stop");
  };

  // تحديد كمقروء
  const markAsRead = (messageIds) => {
    send("mark_as_read", { message_ids: messageIds });
  };

  return {
    socket,
    isConnected,
    connect,
    send,
    on,
    off,
    disconnect,
    sendMessage,
    startTyping,
    stopTyping,
    markAsRead,
  };
}

/**
 * Notification WebSocket Composable
 * For global notifications (Singleton)
 */
let notificationSocketInstance = null;

export function useNotificationWebSocket() {
  if (!notificationSocketInstance) {
    // const wsBaseUrl = (import.meta.env.VITE_API_URL || window.location.origin).replace(/^http/, 'ws').replace(/\/api\/?$/, '')
    const wsBaseUrl = (
      settings.url ||
      import.meta.env.VITE_WS_URL ||
      window.location.origin
    )
      .replace(/^http/, "ws")
      .replace(/\/?$/, "")
      .replace(/\/$/, "");
    
    const authStore = useAuthStore();
    const token = authStore.accessToken || authStore.token || "";
    const url = `${wsBaseUrl}/ws/notifications/?token=${token}`;
    notificationSocketInstance = useWebSocket(url);

    // حماية الاتصال العالمي من الإغلاق العرضي من قبل الصفحات
    const originalDisconnect = notificationSocketInstance.disconnect;
    notificationSocketInstance.disconnect = () => {
      // لا نفعل شيئاً هنا لمنع الصفحات من إغلاق الاتصال العالمي
      // الإغلاق الحقيقي يجب أن يتم فقط عند تسجيل الخروج (عبر دالة خاصة)
    };

    // دالة خاصة للإغلاق الحقيقي عند تسجيل الخروج
    notificationSocketInstance.forceDisconnect = originalDisconnect;
  }
  return notificationSocketInstance;
}

export default useWebSocket;
