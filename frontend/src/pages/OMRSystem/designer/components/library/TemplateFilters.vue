<template>
  <filter-fields label="خيارات التصفية والبحث المتقدم" class="main-card border-0 pa-5 rounded-2xl mb-6">
    <v-row dense class="align-center">
      <!-- 1. Search Query Input -->
      <v-col cols="12" sm="6" md="3">
        <v-text-field
          :model-value="searchQuery"
          label="اسم القالب أو المادة"
          placeholder="بحث باسم القالب أو المادة..."
          prepend-inner-icon="mdi-magnify"
          clearable
          density="compact"
          variant="outlined"
          rounded="lg"
          class="mb-3"
          hide-details
          @update:model-value="$emit('update:searchQuery', $event); $emit('apply')"
        />
      </v-col>

      <!-- 2. Category / Organization Filter -->
      <v-col cols="12" sm="6" md="3">
        <v-select
          :model-value="filterCategory"
          :items="categoryOptions"
          item-title="text"
          item-value="value"
          label="نوع القالب / المؤسسة"
          prepend-inner-icon="mdi-domain"
          clearable
          density="compact"
          variant="outlined"
          rounded="lg"
          class="mb-3"
          hide-details
          @update:model-value="$emit('update:filterCategory', $event); $emit('apply')"
        />
      </v-col>

      <!-- 3. Question Count Capacity Filter -->
      <v-col cols="12" sm="6" md="2">
        <v-select
          :model-value="filterQuestions"
          :items="questionCountOptions"
          item-title="text"
          item-value="value"
          label="سعة الأسئلة"
          prepend-inner-icon="mdi-help-circle-outline"
          clearable
          density="compact"
          variant="outlined"
          rounded="lg"
          class="mb-3"
          hide-details
          @update:model-value="$emit('update:filterQuestions', $event); $emit('apply')"
        />
      </v-col>

      <!-- 4. Active Status Filter -->
      <v-col cols="12" sm="6" md="2">
        <v-select
          :model-value="filterActive"
          :items="activeOptions"
          item-title="text"
          item-value="value"
          label="حالة التفعيل"
          prepend-inner-icon="mdi-check-circle-outline"
          clearable
          density="compact"
          variant="outlined"
          rounded="lg"
          class="mb-3"
          hide-details
          @update:model-value="$emit('update:filterActive', $event); $emit('apply')"
        />
      </v-col>

      <!-- 5. Filter Action Buttons -->
      <v-col cols="12" sm="6" md="2" class="d-flex align-center justify-end gap-2 mb-3">
        <custom-btn
          type="show"
          label="تصفية"
          color="primary"
          icon="mdi-filter"
          class="font-weight-bold flex-grow-1"
          :click="() => $emit('apply')"
        />
        <custom-btn
          type="cancel_filter"
          variant="tonal"
          color="error"
          label="تفريغ"
          icon="mdi-filter-off"
          class="font-weight-bold"
          :click="() => $emit('reset')"
        />
      </v-col>
    </v-row>
  </filter-fields>
</template>

<script setup lang="ts">
defineProps<{
  searchQuery: string
  filterCategory: string
  filterQuestions: any
  filterActive: boolean | null
  categoryOptions: any[]
  questionCountOptions: any[]
  activeOptions: any[]
}>()

defineEmits<{
  (e: 'update:searchQuery', val: string): void
  (e: 'update:filterCategory', val: string): void
  (e: 'update:filterQuestions', val: any): void
  (e: 'update:filterActive', val: boolean | null): void
  (e: 'apply'): void
  (e: 'reset'): void
}>()
</script>

<style scoped>
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 4px 12px rgba(0, 0, 0, 0.02);
}
</style>
