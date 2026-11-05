<template>
  <filter-fields label="خيارات التصفية والبحث المتقدم" class="main-card border-0 pa-5 rounded-2xl mb-6">
    <v-row dense class="align-center">
      <!-- 1. حقل البحث بالاسم والمادة الموحد -->
      <v-col cols="12" sm="6" md="3">
        <custom-text-field
          :model-value="searchQuery"
          label="اسم القالب أو المادة"
          placeholder="بحث باسم القالب أو المادة..."
          icon="magnify"
          cols="12"
          :hideDetails="true"
          clearable
          @update:model-value="$emit('update:searchQuery', $event); $emit('apply')"
        />
      </v-col>

      <!-- 2. فلتر نوع القالب / المؤسسة الموحد -->
      <v-col cols="12" sm="6" md="3">
        <auto-list
          :model-value="filterCategory"
          name="ScreenTypeChoices"
          :objects="formattedCategoryOptions"
          label="نوع القالب / المؤسسة"
          placeholder="كافة الأنواع..."
          cols="12"
          :add="false"
          :hideDetails="true"
          @update:model-value="$emit('update:filterCategory', $event); $emit('apply')"
        />
      </v-col>

      <!-- 3. فلتر سعة الأسئلة الموحد -->
      <v-col cols="12" sm="6" md="2">
        <auto-list
          :model-value="filterQuestions"
          name="ScreenTypeChoices"
          :objects="formattedQuestionOptions"
          label="سعة الأسئلة"
          placeholder="كافة السعات..."
          cols="12"
          :add="false"
          :hideDetails="true"
          @update:model-value="$emit('update:filterQuestions', $event); $emit('apply')"
        />
      </v-col>

      <!-- 4. فلتر حالة التفعيل الموحد -->
      <v-col cols="12" sm="6" md="2">
        <auto-list
          :model-value="filterActive"
          name="ScreenTypeChoices"
          :objects="formattedActiveOptions"
          label="حالة التفعيل"
          placeholder="كافة الحالات..."
          cols="12"
          :add="false"
          :hideDetails="true"
          @update:model-value="$emit('update:filterActive', $event); $emit('apply')"
        />
      </v-col>

      <!-- 5. أزرار إجراءات الفلترة الموحدة -->
      <v-col cols="12" sm="6" md="2" class="d-flex align-center justify-end gap-2">
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
import { computed } from 'vue'

const props = defineProps<{
  searchQuery: string
  filterCategory: string
  filterQuestions: any
  filterActive: any
  categoryOptions?: any[]
  questionCountOptions?: any[]
  activeOptions?: any[]
}>()

const emit = defineEmits<{
  (e: 'update:searchQuery', val: string): void
  (e: 'update:filterCategory', val: string): void
  (e: 'update:filterQuestions', val: any): void
  (e: 'update:filterActive', val: any): void
  (e: 'apply'): void
  (e: 'reset'): void
}>()

const formattedCategoryOptions = computed(() => {
  return (props.categoryOptions || []).map((o: any) => ({
    id: o.id !== undefined ? o.id : (o.value !== undefined ? o.value : o),
    value: o.value !== undefined ? o.value : (o.id !== undefined ? o.id : o),
    name: o.name || o.text || o.title || String(o),
    title: o.title || o.name || o.text || String(o),
  }))
})

const formattedQuestionOptions = computed(() => {
  return (props.questionCountOptions || []).map((o: any) => ({
    id: o.id !== undefined ? o.id : (o.value !== undefined ? o.value : o),
    value: o.value !== undefined ? o.value : (o.id !== undefined ? o.id : o),
    name: o.name || o.text || o.title || String(o),
    title: o.title || o.name || o.text || String(o),
  }))
})

const formattedActiveOptions = computed(() => {
  return (props.activeOptions || []).map((o: any) => ({
    id: o.id !== undefined ? o.id : (o.value !== undefined ? o.value : o),
    value: o.value !== undefined ? o.value : (o.id !== undefined ? o.id : o),
    name: o.name || o.text || o.title || String(o),
    title: o.title || o.name || o.text || String(o),
  }))
})
</script>

<style scoped>
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 4px 12px rgba(0, 0, 0, 0.02);
}
</style>
