<template>
  <div class="empty-state">
    <v-icon class="mb-4" color="secondary" :size="iconSize">
      {{ icon }}
    </v-icon>
    <h3 class="text-secondary mb-2">{{ title }}</h3>
    <p v-if="description" class="text-secondary text-center mb-4">
      {{ description }}
    </p>
    <slot name="action" />
  </div>
</template>

<script setup>
  defineProps({
    icon: {
      type: String,
      default: 'mdi-chat-outline',
    },
    title: {
      type: String,
      default: 'لا توجد بيانات',
    },
    description: {
      type: String,
      default: '',
    },
    iconSize: {
      type: [Number, String],
      default: 80,
    },
  })
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  text-align: center;
  height: 100%;
  min-height: 300px;
}
</style>
