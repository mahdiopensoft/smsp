<template>
  <custom-dialog
    v-model="isOpen"
    :title="currentView === 'menu' ? ($t('chat.settings.title') || 'الإعدادات') : currentView === 'notifications' ? 'الإشعارات' : ($t('chat.settings.blockedUsers') || 'المستخدمين المحظورين')"
    width="500"
  >
    <div class="settings-container pa-1" style="min-height: 380px;">
      <!-- زر الرجوع -->
      <v-slide-y-transition>
        <div v-if="currentView !== 'menu'" class="mb-4">
          <v-btn 
            variant="tonal" 
            color="primary" 
            rounded="pill" 
            @click="currentView = 'menu'" 
            size="small"
            class="back-btn font-weight-bold"
            elevation="0"
          >
            <v-icon start size="18">{{ isRtl ? 'mdi-arrow-right' : 'mdi-arrow-left' }}</v-icon>
            {{ $t("common.back") || "رجوع" }}
          </v-btn>
        </div>
      </v-slide-y-transition>
      
      <v-window v-model="currentView" class="settings-window">
        <!-- القائمة الرئيسية -->
        <v-window-item value="menu">
          <div class="d-flex flex-column gap-3">
            <v-card 
              link 
              @click="currentView = 'blocked_users'" 
              class="setting-card" 
              elevation="0"
              rounded="xl"
            >
              <div class="d-flex align-center pa-4">
                <div class="icon-wrapper error-gradient me-4 shadow-error">
                  <v-icon color="white">mdi-account-cancel-outline</v-icon>
                </div>
                <div class="flex-grow-1">
                  <h3 class="text-subtitle-1 font-weight-bold mb-1">{{ $t("chat.settings.blockedUsers") || "قائمة المحظورين" }}</h3>
                  <p class="text-caption text-medium-emphasis mb-0">إدارة جهات الاتصال المحظورة</p>
                </div>
                <v-icon color="grey-lighten-1">{{ isRtl ? 'mdi-chevron-left' : 'mdi-chevron-right' }}</v-icon>
              </div>
            </v-card>

            <v-card 
              link 
              @click="currentView = 'notifications'" 
              class="setting-card" 
              elevation="0"
              rounded="xl"
            >
              <div class="d-flex align-center pa-4">
                <div class="icon-wrapper primary-gradient me-4 shadow-primary">
                  <v-icon color="white">mdi-bell-outline</v-icon>
                </div>
                <div class="flex-grow-1">
                  <h3 class="text-subtitle-1 font-weight-bold mb-1">الإشعارات</h3>
                  <p class="text-caption text-medium-emphasis mb-0">التحكم في أصوات النظام والمحادثات</p>
                </div>
                <v-icon color="grey-lighten-1">{{ isRtl ? 'mdi-chevron-left' : 'mdi-chevron-right' }}</v-icon>
              </div>
            </v-card>
          </div>
        </v-window-item>

        <!-- قسم المحظورين -->
        <v-window-item value="blocked_users">
          <div class="d-flex flex-column h-100">
            <div v-if="loading" class="d-flex flex-column align-center justify-center pa-8 flex-grow-1" style="min-height: 250px;">
              <v-progress-circular indeterminate color="primary" size="48" width="4"></v-progress-circular>
              <span class="mt-4 text-medium-emphasis text-body-2">جاري تحميل القائمة...</span>
            </div>

            <div v-else-if="blockedUsers.length === 0" class="empty-state text-center pa-8 flex-grow-1 d-flex flex-column justify-center align-center" style="min-height: 250px;">
              <div class="empty-icon-wrapper mb-4">
                <v-icon size="56" color="success">mdi-shield-check-outline</v-icon>
              </div>
              <h3 class="text-h6 font-weight-bold mb-2">قائمتك نظيفة</h3>
              <p class="text-body-2 text-medium-emphasis">{{ $t("chat.settings.noBlockedUsers") || "لا يوجد أي مستخدمين محظورين في قائمتك حالياً." }}</p>
            </div>

            <div v-else class="blocked-list custom-scrollbar">
              <v-slide-y-transition group>
                <v-card 
                  v-for="user in blockedUsers" 
                  :key="user.id" 
                  class="blocked-user-card mb-3" 
                  elevation="0"
                  variant="outlined"
                  rounded="lg"
                >
                  <div class="d-flex align-center pa-3">
                    <v-avatar color="grey-lighten-3" class="me-3 border-avatar" size="48">
                      <span class="text-h6 font-weight-bold text-grey-darken-2">
                        {{ user.first_name?.[0] || user.username?.[0] || "?" }}
                      </span>
                    </v-avatar>
                    
                    <div class="flex-grow-1 overflow-hidden">
                      <h4 class="text-subtitle-1 font-weight-bold text-truncate mb-1">
                        {{ user.first_name ? user.first_name + ' ' + (user.last_name || '') : user.username }}
                      </h4>
                      <p class="text-caption text-medium-emphasis mb-0 text-truncate" dir="ltr" style="text-align: right;">
                        @{{ user.username }}
                      </p>
                    </div>

                    <v-btn
                      color="error"
                      variant="tonal"
                      size="small"
                      rounded="pill"
                      class="px-4 ms-2 font-weight-bold unblock-btn"
                      :loading="unblockingId === user.id"
                      @click="unblock(user.id)"
                    >
                      {{ $t('chat.settings.unblock') || 'إلغاء الحظر' }}
                    </v-btn>
                  </div>
                </v-card>
              </v-slide-y-transition>
            </div>
          </div>
        </v-window-item>

        <!-- قسم الإشعارات -->
        <v-window-item value="notifications">
          <div class="d-flex flex-column gap-4 py-2">
            <div class="notification-group">
              <div class="d-flex align-center mb-3 px-1">
                <v-icon color="primary" size="20" class="me-2">mdi-volume-high</v-icon>
                <span class="text-subtitle-2 font-weight-bold text-primary">أصوات التنبيهات</span>
              </div>
              
              <v-card class="notification-card mb-3" elevation="0" rounded="xl" variant="flat">
                <div class="d-flex align-center pa-4">
                  <div class="icon-box me-4 bg-grey-lighten-4">
                    <v-icon color="grey-darken-3">mdi-laptop</v-icon>
                  </div>
                  <div class="flex-grow-1">
                    <h4 class="text-subtitle-1 font-weight-bold mb-1">إشعارات النظام</h4>
                    <p class="text-caption text-medium-emphasis mb-0">تشغيل نغمة عند وصول تنبيهات عامة وإشعارات من المنصة.</p>
                  </div>
                  <div class="ms-3 custom-switch">
                    <v-switch v-model="enableSystemSounds" color="success" hide-details density="compact" inset @change="saveNotificationSettings"></v-switch>
                  </div>
                </div>
              </v-card>

              <v-card class="notification-card" elevation="0" rounded="xl" variant="flat">
                <div class="d-flex align-center pa-4">
                  <div class="icon-box me-4 bg-grey-lighten-4">
                    <v-icon color="grey-darken-3">mdi-message-badge-outline</v-icon>
                  </div>
                  <div class="flex-grow-1">
                    <h4 class="text-subtitle-1 font-weight-bold mb-1">إشعارات المحادثات</h4>
                    <p class="text-caption text-medium-emphasis mb-0">تشغيل نغمة عند استلام رسائل جديدة في الدردشة.</p>
                  </div>
                  <div class="ms-3 custom-switch">
                    <v-switch v-model="enableChatSounds" color="success" hide-details density="compact" inset @change="saveNotificationSettings"></v-switch>
                  </div>
                </div>
              </v-card>
            </div>
          </div>
        </v-window-item>
      </v-window>
    </div>
  </custom-dialog>
</template>

<script setup>
import { ref, watch, computed, onMounted } from "vue";
import chatService from "../../services/chatService";
import { useChatStore } from "../../store/chat"

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["update:modelValue"]);

const isOpen = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});

const loading = ref(false);
const unblockingId = ref(null);
const blockedUsers = ref([]);
const currentView = ref("menu");
const isRtl = computed(() => document.documentElement.dir === "rtl" || true); 

const enableSystemSounds = ref(true);
const enableChatSounds = ref(true);

onMounted(() => {
  enableSystemSounds.value = localStorage.getItem("enable_system_sounds") !== "false";
  enableChatSounds.value = localStorage.getItem("notification_sound") !== "false";
});

const saveNotificationSettings = () => {
  localStorage.setItem("enable_system_sounds", enableSystemSounds.value ? "true" : "false");
  localStorage.setItem("notification_sound", enableChatSounds.value ? "true" : "false");
};

watch(isOpen, async (newVal) => {
  if (newVal) {
    if (currentView.value === "blocked_users") {
      await fetchBlockedUsers();
    }
  }
});

watch(currentView, async (newView) => {
  if (newView === "blocked_users" && blockedUsers.value.length === 0) {
    await fetchBlockedUsers();
  }
});

async function fetchBlockedUsers() {
  loading.value = true;
  try {
    const data = await chatService.getBlockedUsers();
    blockedUsers.value = data || [];
  } catch (error) {
    console.error("Failed to fetch blocked users:", error);
  } finally {
    loading.value = false;
  }
}

async function unblock(userId) {
  unblockingId.value = userId;
  try {
    await chatService.unblockUser(userId);
    blockedUsers.value = blockedUsers.value.filter((u) => u.id !== userId);

    const chatStore = useChatStore();
    await chatStore.fetchChats()
  } catch (error) {
    console.error("Failed to unblock user:", error);
  } finally {
    unblockingId.value = null;
  }
}

function close() {
  isOpen.value = false;
  setTimeout(() => {
    currentView.value = "menu";
  }, 300);
}
</script>

<style scoped>
.settings-container {
  position: relative;
}

.setting-card {
  background: rgba(var(--v-theme-surface), 1);
  border: 1px solid rgba(var(--v-border-color), 0.08) !important;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow: hidden;
  position: relative;
  cursor: pointer;
}

.setting-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: currentColor;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

.setting-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.06) !important;
  border-color: rgba(var(--v-theme-primary), 0.3) !important;
}

.setting-card:hover::before {
  opacity: 0.02;
}

.icon-wrapper {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.primary-gradient {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.error-gradient {
  background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%);
}

.shadow-primary {
  box-shadow: 0 8px 16px rgba(79, 172, 254, 0.3);
}

.shadow-error {
  box-shadow: 0 8px 16px rgba(255, 8, 68, 0.3);
}

.back-btn {
  transition: all 0.2s ease;
}

.back-btn:hover {
  transform: translateX(4px);
}
[dir="rtl"] .back-btn:hover {
  transform: translateX(-4px);
}

/* Blocked Users */
.blocked-list {
  max-height: 350px;
  overflow-y: auto;
  padding-right: 4px;
}

.blocked-user-card {
  border-color: rgba(var(--v-border-color), 0.1) !important;
  transition: all 0.2s ease;
  background: rgba(var(--v-theme-surface), 0.3);
}

.blocked-user-card:hover {
  border-color: rgba(var(--v-theme-error), 0.3) !important;
  background: rgba(var(--v-theme-error), 0.02);
}

.border-avatar {
  border: 2px solid rgba(var(--v-theme-surface), 1);
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.unblock-btn {
  text-transform: none !important;
  letter-spacing: 0;
}

/* Empty State */
.empty-icon-wrapper {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  background: rgba(var(--v-theme-success), 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Notifications */
.notification-card {
  background: rgba(var(--v-theme-on-surface), 0.02) !important;
  border: 1px solid rgba(var(--v-border-color), 0.05) !important;
  transition: background 0.2s ease;
}

.notification-card:hover {
  background: rgba(var(--v-theme-on-surface), 0.04) !important;
}

.icon-box {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.gap-3 {
  gap: 12px;
}

.gap-4 {
  gap: 16px;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.15);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-on-surface), 0.3);
}

.settings-window {
  transition: height 0.3s ease;
}
</style>
