<template>
  <div class="registry-nav-bar mb-6">
    <div class="registry-nav-container">
      <div
        class="registry-nav-item"
        :class="{ 'is-active': activeTab === 'sheets' }"
        @click="$emit('switch-tab', 'sheets')"
        role="button"
        tabindex="0"
      >
        <v-icon size="17" class="nav-icon">mdi-table-account</v-icon>
        <span>الجدول الموحد لأوراق التظليل</span>
      </div>

      <div
        class="registry-nav-item"
        :class="{ 'is-active': activeTab === 'questions' }"
        @click="$emit('switch-tab', 'questions')"
        role="button"
        tabindex="0"
      >
        <v-icon size="17" class="nav-icon">mdi-file-document-outline</v-icon>
        <span>ورقة الأسئلة الرسمية (الكراسة)</span>
      </div>

      <div
        class="registry-nav-item"
        :class="{ 'is-active': activeTab === 'package' }"
        @click="$emit('switch-tab', 'package')"
        role="button"
        tabindex="0"
      >
        <v-icon size="17" class="nav-icon">mdi-package-variant-closed</v-icon>
        <span>حزمة الاختبار (أسئلة + تظليل)</span>
      </div>

      <div
        class="registry-nav-item"
        :class="{ 'is-active': activeTab === 'history' }"
        @click="$emit('switch-tab', 'history')"
        role="button"
        tabindex="0"
      >
        <v-icon size="17" class="nav-icon">mdi-history</v-icon>
        <span>سجل الدفعات المطبوعة ({{ batchesCount || 0 }})</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  activeTab: string
  batchesCount: number
}>()

defineEmits<{
  (e: 'switch-tab', tab: string): void
}>()
</script>

<style scoped>
.registry-nav-bar {
  display: flex;
  justify-content: center;
  align-items: center;
}

.registry-nav-container {
  display: flex;
  align-items: center;
  background: rgba(var(--v-theme-surface-variant), 0.2);
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-radius: 14px;
  padding: 4px;
  gap: 4px;
  overflow-x: auto;
  max-width: 100%;
}

.registry-nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 700;
  color: rgb(var(--v-theme-on-surface));
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  user-select: none;
}

.registry-nav-item:hover {
  background: rgba(var(--v-theme-surface-variant), 0.4);
}

.registry-nav-item.is-active {
  background: rgb(var(--v-theme-surface));
  color: rgb(var(--v-theme-primary));
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(var(--v-border-color), 0.5);
}
</style>
