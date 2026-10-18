<template>
  <v-expansion-panels density class="notes-container w-auto">
    <v-expansion-panel elevation="0" density>
      <v-expansion-panel-title class="px-5 py-0">
        <div class="notes-header">
          <v-icon size="18" color="primary" class="me-2">mdi-information-outline</v-icon>
          <span class="notes-title">ملاحظات</span>
        </div>
      </v-expansion-panel-title>

      <v-expansion-panel-text>
        <div class="notes-content">
          <div v-for="(item, index) in items" :key="index" class="note-item">
            <span class="note-index">{{ index + 1 }}</span>
            <div class="note-text" v-html="item"></div>
          </div>
        </div>

        <div v-if="!items || items.length === 0" class="notes-empty">
          لا توجد ملاحظات مضافة
        </div>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup>
const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
});
</script>

<style scoped>
.notes-container {
  background: rgba(var(--v-theme-primary), 0.03);
  border-radius: var(--radius-lg);
  border-inline-start: 4px solid rgb(var(--v-theme-primary));
  transition: all 0.2s ease;
  margin: 5px 0;
}

.notes-header {
  display: flex;
  align-items: center;
  margin-bottom: var(--space-sm);
}

.notes-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: rgb(var(--v-theme-primary));
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.notes-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.note-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-sm);
  padding: var(--space-xs) 0;
}

.note-index {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  background: rgba(var(--v-theme-primary), 0.1);
  color: rgb(var(--v-theme-primary));
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 700;
  margin-top: 2px;
}

.note-text {
  font-size: 0.875rem;
  color: rgba(var(--v-theme-on-surface), 0.8);
  line-height: 1.5;
}

.notes-empty {
  font-size: 0.875rem;
  color: rgba(var(--v-theme-on-surface), 0.4);
  font-style: italic;
  padding: var(--space-xs) 0;
}
</style>
