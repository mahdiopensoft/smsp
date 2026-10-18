<template>
  <v-menu v-model="isMenuOpen" :close-on-content-click="false" class="me-2" transition="slide-y-transition">
    <template v-slot:activator="{ props, isActive }">
      <v-badge
        color="error"
        :content="unreadCount"
        :model-value="unreadCount > 0"
        bordered
        location="left top"
        class="me-3 custom-badge"
        :class="{ 'pulse-badge': unreadCount > 0 }"
      >
        <v-btn
          v-bind="props"
          v-tooltip:top="'التعميمات'"
          :icon="isActive ? 'mdi-bullhorn' : 'mdi-bullhorn-outline'"
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
          <v-icon icon="mdi-bullhorn" class="me-2 text-primary pulse-icon"></v-icon>
          <span class="text-subtitle-1 font-weight-bold">التعميمات الإدارية</span>
        </div>
        <v-btn 
          icon="mdi-plus" 
          variant="tonal" 
          density="compact" 
          color="primary" 
          @click="showCreateDialog = true" 
          v-tooltip:top="'إنشاء تعميم جديد'"
          class="create-btn"
        ></v-btn>
      </div>
      
      <v-list lines="two" max-height="350" class="overflow-y-auto py-1">
        <template v-if="unreadGeneralizations.length">
          <v-list-item
            v-for="(gen, index) in unreadGeneralizations"
            :key="gen.id"
            @click="openGeneralization(gen)"
            class="generalization-item px-4 py-2 border-b-1"
          >
            <template v-slot:prepend>
              <v-avatar color="primary" variant="tonal" size="40" class="me-2">
                <v-icon size="20">mdi-bullhorn-variant-outline</v-icon>
              </v-avatar>
            </template>
            
            <v-list-item-title class="font-weight-bold text-body-2 mb-1">
              {{ gen.title }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-caption text-grey-darken-1 text-truncate">
              {{ gen.content }}
            </v-list-item-subtitle>
            
            <template v-slot:append>
              <div class="d-flex flex-column align-end justify-center h-100">
                <span class="text-caption text-grey-darken-1 mb-1">{{ formatDate(gen.created_at) }}</span>
                <v-btn
                  icon="mdi-eye-outline"
                  size="x-small"
                  variant="text"
                  color="grey"
                  @click.stop="openGeneralization(gen)"
                  v-tooltip:top="'عرض التعميم'"
                ></v-btn>
              </div>
            </template>
          </v-list-item>
        </template>
        
        <v-list-item v-else class="py-6">
          <div class="d-flex align-center flex-column text-center w-100 my-4">
            <div class="empty-state-avatar mb-3">
              <v-icon size="32" color="grey-darken-1">mdi-bell-sleep-outline</v-icon>
            </div>
            <div class="text-subtitle-2 font-weight-bold text-grey-darken-2">
              لا توجد تعميمات جديدة غير مقروءة
            </div>
            <div class="text-caption text-grey mt-1">
              تصفح الأرشيف لرؤية التعميمات السابقة
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
          to="/generalizations-view"
          prepend-icon="mdi-archive-outline"
          class="rounded-lg text-body-2 font-weight-bold shadow-sm py-2"
          @click="isMenuOpen = false"
        >
          أرشيف التعميمات
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-menu>

  <!-- Dialog لعرض التعميم -->
  <GeneralizationViewDialog
    v-model="showViewDialog"
    :generalization="selectedGeneralization"
  />

  <!-- Dialog لإنشاء تعميم -->
  <GeneralizationCreateDialog
    v-model="showCreateDialog"
  />
</template>

<script setup>
import { useGeneralizationStore } from "../store/generalizationStore";
import { useAuthStore } from "../../src/UserManagement/stores/auth";
import { ref, computed, onMounted } from "vue";
import GeneralizationViewDialog from "../pages/Generalizations/GeneralizationViewDialog.vue";
import GeneralizationCreateDialog from "../pages/Generalizations/GeneralizationCreateDialog.vue";

const genStore = useGeneralizationStore();
const authStore = useAuthStore();

const isMenuOpen = ref(false);
const showViewDialog = ref(false);
const showCreateDialog = ref(false);
const selectedGeneralization = ref(null);

const unreadGeneralizations = computed(() => {
  return genStore.unreadGeneralizations;
});

const unreadCount = computed(() => genStore.unreadCount || 0);

const openGeneralization = (gen) => {
  selectedGeneralization.value = gen;
  showViewDialog.value = true;
  
  const isSender = gen.sender_data?.id === authStore.user?.id || gen.sender_data?.username === authStore.user?.username;
  
  if (!isSender && !gen.is_read) {
    genStore.markAsRead(gen.id);
  } else if (isSender && gen.unread_replies_count > 0) {
    genStore.markAsRead(gen.id);
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  return date.toLocaleDateString('ar-EG');
};

onMounted(() => {
  genStore.fetchUnreadGeneralizations();
  genStore.fetchCounts();
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

.create-btn {
  
  transition: all 0.3s ease;
}
.create-btn:hover {
  background: rgba(255, 255, 255, 0.3) !important;
  transform: rotate(90deg);
}

.generalization-item {
  transition: background-color 0.2s ease, transform 0.2s ease;
  border-bottom: 1px solid rgba(var(--v-border-color), 0.08);
}
.generalization-item:hover {
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
    box-shadow: 0 0 0 0 rgba(var(--v-theme-error), 0.7);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(var(--v-theme-error), 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(var(--v-theme-error), 0);
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
