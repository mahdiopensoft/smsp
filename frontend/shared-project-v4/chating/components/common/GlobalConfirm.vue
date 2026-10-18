<template>
  <v-dialog
    v-model="confirmStore.isOpen"
    max-width="400"
    persistent
  >
    <v-card class="rounded-xl pa-4 confirm-card">
      <v-card-title class="text-h6 font-weight-black d-flex align-center gap-2">
        <v-icon color="warning" size="28">mdi-alert-circle-outline</v-icon>
        {{ confirmStore.title }}
      </v-card-title>

      <v-card-text class="text-body-1 py-4 opacity-90">
        {{ confirmStore.message }}
      </v-card-text>

      <v-card-actions class="pt-2">
        <v-spacer />
        <v-btn
          class="rounded-lg px-6"
          color="grey-darken-1"
          variant="text"
          @click="confirmStore.cancel"
        >
          {{ confirmStore.cancelText }}
        </v-btn>
        <v-btn
          class="rounded-lg px-8 confirm-btn-glow"
          color="error"
          elevation="4"
          variant="flat"
          @click="confirmStore.confirm"
        >
          {{ confirmStore.confirmText }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
  import { useConfirmStore } from '../../store/confirmStore'

  const confirmStore = useConfirmStore()
</script>

<style scoped>
.confirm-card {
  background: rgba(var(--v-theme-surface), 0.95) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(var(--v-theme-primary), 0.1) !important;
  box-shadow: 0 20px 50px rgba(0,0,0,0.2) !important;
}

.confirm-btn-glow {
  box-shadow: 0 4px 15px rgba(var(--v-theme-error), 0.4) !important;
  transition: all 0.2s ease;
}

.confirm-btn-glow:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(var(--v-theme-error), 0.6) !important;
}

.gap-2 {
  gap: 8px;
}
</style>
