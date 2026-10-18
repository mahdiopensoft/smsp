<template>
  <v-snackbar
    v-model="toastStore.show"
    :class="['global-toast', { 'rich-interactive-toast': !!toastStore.title }]"
    :color="toastStore.title ? 'transparent' : toastStore.color"
    elevation="0"
    location="top"
    :rounded="toastStore.title ? 'xl' : 'pill'"
    :timeout="toastStore.timeout"
  >
    <!-- Rich Interactive Toast (Modern Push Notification Style) -->
    <div
      v-if="toastStore.title"
      class="interactive-card elevation-12"
      @click="handleToastClick"
    >
      <div class="d-flex align-center w-100 py-1">
        <!-- Avatar / Icon -->
        <v-avatar v-if="toastStore.avatar" size="48" class="me-3 premium-avatar">
          <v-img :src="toastStore.avatar" />
        </v-avatar>
        <v-avatar v-else :color="toastStore.color || 'primary'" size="48" class="me-3 premium-avatar">
          <v-icon color="white">{{iconName}}</v-icon>
        </v-avatar>

        <!-- Message Body -->
        <div class="flex-grow-1 min-width-0 pe-2">
          <h4 class="text-subtitle-1 font-weight-black text-high-emphasis text-truncate mb-0">
            {{ toastStore.title }}
          </h4>
          <p class="text-body-2 text-medium-emphasis text-truncate mb-0">
            {{ toastStore.message }}
          </p>
        </div>

        <!-- Actions -->
        <div class="d-flex align-center gap-1">
          <v-btn
            v-if="toastStore.onClick || toastStore.chatId"
            color="primary"
            variant="flat"
            size="small"
            class="rounded-pill font-weight-black px-4"
          >
            {{ $t('chat.open') || 'فتح' }}
          </v-btn>
          <v-btn
            icon="mdi-close"
            size="small"
            variant="text"
            class="close-btn opacity-60"
            @click.stop="toastStore.closeToast"
          />
        </div>
      </div>
    </div>

    <!-- Standard Simple Toast -->
    <div v-else class="d-flex align-center gap-3 w-100 px-2">
      <v-icon :icon="iconName" size="large" />
      <span class="text-body-1 font-weight-medium flex-grow-1">{{ toastStore.message }}</span>
      <v-btn
        icon="mdi-close"
        size="small"
        variant="text"
        @click="toastStore.closeToast"
      />
    </div>
  </v-snackbar>
</template>

<script setup>
  import { computed } from 'vue'
  import { useToastStore } from '../../store/toastStore'

  const toastStore = useToastStore()

  const handleToastClick = () => {
    if (toastStore.onClick && typeof toastStore.onClick === 'function') {
      toastStore.onClick()
    }
    toastStore.closeToast()
  }

  const iconName = computed(() => {
    switch (toastStore.color) {
      case 'success': {
        return 'mdi-check-circle'
      }
      case 'error': {
        return 'mdi-alert-circle'
      }
      case 'warning': {
        return 'mdi-alert'
      }
      case 'info':
      default: {
        return 'mdi-information'
      }
    }
  })
</script>

<style scoped>
.global-toast {
  margin-top: 16px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.global-toast.rich-interactive-toast {
  padding: 0 !important;
}

.global-toast.rich-interactive-toast :deep(.v-snackbar__wrapper) {
  background: transparent !important;
  box-shadow: none !important;
  padding: 0 !important;
  min-width: 320px;
  max-width: 500px;
  width: 100%;
}

.interactive-card {
  background: rgba(var(--v-theme-surface), 0.8) !important;
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  border-radius: 20px;
  padding: 12px 16px;
  width: 100%;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12), 0 4px 8px rgba(0, 0, 0, 0.06) !important;
}

.interactive-card:hover {
  transform: translateY(-2px);
  background: rgba(var(--v-theme-surface), 0.9) !important;
  border-color: rgba(var(--v-theme-primary), 0.3);
}

.premium-avatar {
  border: 2px solid rgba(var(--v-theme-primary), 0.2);
}

.global-toast :deep(.v-snackbar__content) {
  padding: 8px 16px;
}

.rich-interactive-toast :deep(.v-snackbar__content) {
  padding: 0 !important;
}
</style>
