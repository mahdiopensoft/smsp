<template>
  <!-- Snackbar Mode (Toast) -->
  <v-snackbar
    v-if="notificationStore.mode === 'snackbar'"
    v-model="notificationStore.show"
    :color="statusColor"
    :timeout="notificationStore.timeout"
    location="bottom center"
    variant="elevated"
    elevation="24"
    class="custom-snackbar"
    rounded="xl"
  >
    <div class="d-flex align-center w-100 pa-1">
      <v-avatar :color="avatarColor" size="36" class="me-3 elevation-1">
        <v-icon :icon="statusIcon" color="white" size="20"></v-icon>
      </v-avatar>
      
      <div class="d-flex flex-column flex-grow-1">
        <span class="text-subtitle-2 font-weight-bold text-white mb-n1" v-if="notificationStore.title">
          {{ notificationStore.title }}
        </span>
        <span class="text-body-2 text-white opacity-90">
          {{ notificationStore.message }}
        </span>
      </div>

      <v-btn
        icon="mdi-close"
        size="small"
        variant="text"
        color="white"
        @click="notificationStore.close"
        class="ms-2 opacity-80 hover-opacity-100"
      ></v-btn>
    </div>
  </v-snackbar>

  <!-- Dialog Mode (Modal) -->
  <v-dialog 
    v-else 
    v-model="notificationStore.show" 
    max-width="400" 
    persistent
  >
    <v-card class="rounded-xl overflow-hidden glass-card">
      <div 
        class="dialog-header d-flex flex-column align-center justify-center py-6"
        :style="{ background: dialogHeaderBg }"
      >
        <v-avatar color="white" size="64" class="elevation-4 mb-3">
          <v-icon :color="statusColor" size="40" :icon="statusIcon"></v-icon>
        </v-avatar>
        <h3 class="text-h6 font-weight-bold text-white mb-0">
          {{ notificationStore.title }}
        </h3>
      </div>
      
      <v-card-text class="text-center pt-6 pb-4 text-body-1">
        {{ notificationStore.message }}
      </v-card-text>
      
      <v-card-actions class="px-6 pb-6 d-flex justify-center flex-wrap gap-3">
        <v-btn
          v-if="notificationStore.showCancel"
          color="grey-darken-1"
          variant="outlined"
          rounded="lg"
          class="flex-1-1-100"
          @click="notificationStore.close"
        >
          {{ notificationStore.cancelText }}
        </v-btn>
        
        <v-btn
          :color="statusColor"
          variant="tonal"
          rounded="lg"
          class="flex-1-1-100 text-white font-weight-bold"
          @click="notificationStore.confirm"
        >
          {{ notificationStore.confirmText }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed } from 'vue'
import { useNotificationStore } from '@/stores/notificationStore'

const notificationStore = useNotificationStore()

const statusColor = computed(() => {
  switch (notificationStore.type) {
    case 'success': return '#10b981' // emerald-500
    case 'error': return '#ef4444' // red-500
    case 'warning': return '#f59e0b' // amber-500
    case 'info': return '#3b82f6' // blue-500
    default: return '#3b82f6'
  }
})

const dialogHeaderBg = computed(() => {
  return `linear-gradient(135deg, ${statusColor.value} 0%, ${statusColor.value}dd 100%)`
})

const avatarColor = computed(() => {
  switch (notificationStore.type) {
    case 'success': return 'rgba(255, 255, 255, 0.25)'
    case 'error': return 'rgba(255, 255, 255, 0.25)'
    case 'warning': return 'rgba(255, 255, 255, 0.25)'
    case 'info': return 'rgba(255, 255, 255, 0.25)'
    default: return 'rgba(255, 255, 255, 0.25)'
  }
})

const statusIcon = computed(() => {
  switch (notificationStore.type) {
    case 'success': return 'mdi-check-circle'
    case 'error': return 'mdi-alert-circle'
    case 'warning': return 'mdi-alert'
    case 'info': return 'mdi-information'
    default: return 'mdi-information-outline'
  }
})
</script>

<style scoped>
.custom-snackbar :deep(.v-snackbar__wrapper) {
  min-width: 320px;
  max-width: 480px;
  padding: 8px 12px;
  border: 1px solid rgba(255,255,255,0.1);
}

.custom-snackbar :deep(.v-snackbar__content) {
  padding: 0;
  width: 100%;
}

.opacity-90 { opacity: 0.9; }
.opacity-80 { opacity: 0.8; }
.hover-opacity-100:hover { opacity: 1 !important; }

/* Dialog Styles */
.glass-card {
  background: rgba(var(--v-theme-surface), 0.95);
  border: 1px solid rgba(128, 128, 128, 0.1);
}

.dialog-header {
  box-shadow: inset 0 -10px 20px -10px rgba(0,0,0,0.1);
}

.gap-3 {
  gap: 12px;
}

.flex-1-1-100 {
  flex: 1 1 auto;
  min-width: 120px;
}
</style>
