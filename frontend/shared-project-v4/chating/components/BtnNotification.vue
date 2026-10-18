<template>
  <v-menu v-model="isMenuOpen" :close-on-content-click="false" class="me-2" transition="slide-y-transition">
    <template v-slot:activator="{ props, isActive }">
      <v-badge
        color="success"
        :content="unreadCount"
        :model-value="unreadCount > 0"
        bordered
        location="left top"
        class="me-3 custom-badge"
        :class="{ 'pulse-badge': unreadCount > 0 }"
      >
        <v-btn
          v-bind="props"
          v-tooltip:top="'الإشعارات'"
          :icon="isActive ? 'mdi-bell' : 'mdi-bell-outline'"
          density="compact"
          :color="isActive ? 'primary' : 'grey-darken-1'"
          variant="text"
          class="nav-icon-btn"
        ></v-btn>
      </v-badge>
    </template>
    
    <v-card class="custom-menu-card elevation-12" min-width="360">
      <!-- Gradient Header -->
      <div class="bg-surface border-b py-3 px-4 d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-icon icon="mdi-bell" class="me-2 text-primary pulse-icon"></v-icon>
          <span class="text-subtitle-1 font-weight-bold">إشعارات النظام</span>
        </div>
        <v-btn
          v-if="unreadCount > 0"
          icon="mdi-email-open-outline"
          variant="tonal"
          density="compact"
          color="primary"
          @click.stop="notificationStore.markAllSystemAsRead"
          v-tooltip:top="'تحديد الكل كمقروء'"
          class="mark-all-btn"
        ></v-btn>
      </div>

      <v-list lines="two" max-height="350" class="overflow-y-auto py-1">
        <template v-if="notificationStore.systemNotifications?.filter((n) => !n.is_read).length">
          <v-list-item
            v-for="(notification, index) in notificationStore.systemNotifications.filter((n) => !n.is_read).slice(0, 5)"
            :key="index"
            @click="handleNotificationClick(notification)"
            class="notification-item px-4 py-2 border-b-1"
          >
            <template v-slot:prepend>
              <v-avatar
                :color="
                  notification.priority === 'high'
                    ? 'error'
                    : notification.event_type === 'success'
                    ? 'success'
                    : 'primary'
                "
                variant="tonal"
                size="40"
                class="me-2"
              >
                <v-icon size="20">{{
                  notification.event_type === 'alert'
                    ? 'mdi-alert'
                    : notification.event_type === 'success'
                    ? 'mdi-check-circle'
                    : 'mdi-bell-outline'
                }}</v-icon>
              </v-avatar>
            </template>

            <v-list-item-title class="font-weight-bold text-body-2 mb-1">
              {{ notification.title }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-caption text-medium-emphasis text-truncate" style="max-width: 220px">
              {{ notification.message }}
            </v-list-item-subtitle>

            <template v-slot:append>
              <v-btn
                icon="mdi-check-circle-outline"
                variant="text"
                size="small"
                color="grey-darken-1"
                @click.stop="notificationStore.markSystemAsRead(notification.id)"
                v-tooltip:top="'تحديد كمقروء'"
              ></v-btn>
            </template>
          </v-list-item>
        </template>

        <v-list-item v-else class="py-6">
          <div class="d-flex align-center flex-column text-center w-100 my-4">
            <div class="empty-state-avatar mb-3">
              <v-icon size="32" color="grey-darken-1">mdi-bell-sleep-outline</v-icon>
            </div>
            <div class="text-subtitle-2 font-weight-bold text-medium-emphasis">
              لا توجد إشعارات جديدة غير مقروءة
            </div>
            <div class="text-caption text-medium-emphasis mt-1">
              تصفح الأرشيف لرؤية الإشعارات السابقة
            </div>
          </div>
        </v-list-item>
      </v-list>
      
      <v-divider></v-divider>
      
      <v-card-actions class="bg-background pa-3 justify-center">
        <v-btn
          block
          color="primary"
          variant="flat"
          @click="$router.push('/notifications-view'); isMenuOpen = false"
          prepend-icon="mdi-archive-outline"
          class="rounded-lg text-body-2 font-weight-bold shadow-sm py-2"
        >
          عرض كل الإشعارات
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-menu>
</template>

<script setup>
import { useNotificationStore } from "../store/notificationStore";
import { ref, computed, onMounted } from "vue";

const notificationStore = useNotificationStore();
const isMenuOpen = ref(false);

const handleNotificationClick = (notification) => {
  if (notification.action_url) {
    notificationStore.markSystemAsRead(notification.id);
    if (notification.action_url.startsWith("http")) {
      window.open(notification.action_url, "_self");
    } else {
      const basePath = window.location.origin;
      window.location.href = notification.action_url.startsWith("/")
        ? basePath + notification.action_url
        : basePath + "/" + notification.action_url;
    }
  }
};

const unreadCount = computed(() => {
  return notificationStore.unreadSystemCount || 0;
});

onMounted(() => {
  notificationStore.initWebSocket();
  notificationStore.fetchSystemNotifications();
});
</script>

<style scoped>
.custom-menu-card {
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important;
  background-color: rgb(var(--v-theme-surface)) !important;
}

.header-gradient {
  background: rgb(var(--v-theme-primary));
  background-image: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(0, 0, 0, 0.15) 100%);
  position: relative;
}

.mark-all-btn {
  
  transition: all 0.3s ease;
}
.mark-all-btn:hover {
  background: rgba(255, 255, 255, 0.3) !important;
}

.notification-item {
  transition: background-color 0.2s ease, transform 0.2s ease;
  border-bottom: 1px solid rgba(var(--v-border-color), 0.08);
}
.notification-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.08) !important;
  cursor: pointer;
}

.border-b-1 {
  border-bottom: 1px solid rgba(var(--v-border-color), 0.12);
}

.empty-state-avatar {
  background: rgba(var(--v-theme-on-surface), 0.04);
  border-radius: 50%;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed rgba(var(--v-theme-on-surface), 0.2);
}

.shadow-sm {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* Pulsing Badge & Icon animation */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(var(--v-theme-success), 0.7);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(var(--v-theme-success), 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(var(--v-theme-success), 0);
  }
}

.pulse-badge :deep(.v-badge__badge) {
  animation: pulse 1.8s infinite;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-3px); }
  100% { transform: translateY(0px); }
}
.pulse-icon {
  animation: float 2.5s ease-in-out infinite;
}

.nav-icon-btn {
  transition: all 0.2s ease;
}
.nav-icon-btn:hover {
  transform: scale(1.08);
}
</style>
