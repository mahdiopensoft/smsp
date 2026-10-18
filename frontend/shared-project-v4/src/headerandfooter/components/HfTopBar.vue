<template>
  <div class="hf-topbar">
    <div class="hf-topbar-inner">
      <!-- Logo & Title -->
      <div class="d-flex align-center ga-3">
        <div class="hf-logo">
          <v-icon icon="mdi-page-layout-header-footer" size="20" color="white" />
        </div>
        <div>
          <div class="text-subtitle-2 font-weight-black text-white d-flex align-center ga-2">
            <span>محرر وقوالب الهيدر والفوتر</span>
            <span class="hf-topbar-badge">v2.0</span>
          </div>
          <div class="text-caption hf-topbar-subtitle">
            إدارة وتصميم وتنسيق قوالب الهيدر والفوتر للشاشات والتقارير
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="d-flex align-center ga-2 ms-auto">
        <v-btn
          prepend-icon="mdi-monitor-dashboard"
          variant="tonal"
          color="white"
          class="font-weight-bold hf-topbar-btn"
          size="small"
          rounded="lg"
          title="اختيار وتخصيص الهيدر للشاشات والتقارير"
          @click="$emit('open-assign')"
        >
          تخصيص للشاشات
        </v-btn>

        <v-btn
          prepend-icon="mdi-plus"
          variant="flat"
          color="white"
          class="text-primary font-weight-bold hf-topbar-btn-primary"
          size="small"
          rounded="lg"
          @click="$emit('open-create')"
        >
          قالب جديد
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  templates: {
    type: Array,
    default: () => []
  }
})

defineEmits(['open-create', 'open-assign'])
</script>

<style scoped>
/* Scoped styles if needed */
</style>

