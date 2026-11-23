<template>
  <div class="template-table">
    <custom-data-table
      v-bind="{
        items: tableItems,
        getData,
        headers,
        editItem: (item: any) => $emit('edit', item),
      }"
      :actionList="(item) => [
        { title_ar: 'بدء التصحيح الضوئي بهذا القالب', title_en: 'Start Scan', click: () => $emit('scan', item.id) },
        { title_ar: 'معاينة الورقة', title_en: 'Preview Sheet', click: () => $emit('preview', item) },
        { title_ar: 'تعديل القالب', title_en: 'Edit Template', click: () => $emit('edit', item) },
        { title_ar: 'طباعة القالب', title_en: 'Print Template', click: () => $emit('print', item) },
        { title_ar: 'نسخ كقالب جديد', title_en: 'Duplicate Template', click: () => $emit('duplicate', item) },
        { title_ar: 'حذف القالب', title_en: 'Delete Template', click: () => $emit('confirm-delete', item) },
      ]"
      :numbering="false"
      :create="false"
      :search="true"
      :hasFilter="false"
      :log="false"
      :restore="false"
    >
      <template v-slot:header-actions>
        <v-btn
          color="primary"
          size="small"
          class="rounded-lg font-weight-bold px-4"
          style="height: 38px"
          prepend-icon="mdi-plus"
          @click="$emit('create-new')"
        >
          تصميم قالب جديد
        </v-btn>
      </template>

      <template v-slot:item-slot="{ item, key }">
        <!-- Template ID -->
        <template v-if="key === 'id'">
          <span class="font-mono font-weight-bold text-body-2">#{{ item.id }}</span>
        </template>

        <!-- Template Name and Subtitle -->
        <template v-else-if="key === 'name'">
          <div class="py-1">
            <div class="font-weight-bold text-body-2 text-primary">{{ item.name }}</div>
            <div class="text-caption text-medium-emphasis">{{ item.description || 'قالب تصحيح آلي عالي الدقة 300 DPI' }}</div>
          </div>
        </template>

        <!-- Category / Organization -->
        <template v-else-if="key === 'category'">
          <span class="text-body-2 font-weight-medium">{{ getCategoryLabel(item) }}</span>
        </template>

        <!-- Questions Count -->
        <template v-else-if="key === 'total_mcq'">
          <span class="font-mono font-weight-bold text-body-2">{{ getQuestionsCount(item) }} سؤال</span>
        </template>

        <!-- Columns & Layout -->
        <template v-else-if="key === 'layout'">
          <span class="text-body-2">{{ getColumnsCount(item) }} أعمدة ({{ getChoicesCount(item) }} خيارات)</span>
        </template>

        <!-- Paper Size -->
        <template v-else-if="key === 'paper_size'">
          <span class="font-mono text-body-2">{{ getPaperSize(item) }}</span>
        </template>

        <!-- Version -->
        <template v-else-if="key === 'version'">
          <span class="font-mono text-caption text-medium-emphasis">v{{ item.version || '1.0' }}</span>
        </template>

        <!-- Is Active Status -->
        <template v-else-if="key === 'is_active'">
          <v-chip
            size="small"
            :color="item.is_active !== false ? 'success' : 'error'"
            variant="tonal"
            class="font-weight-bold"
          >
            {{ item.is_active !== false ? 'مفعل' : 'معطل' }}
          </v-chip>
        </template>
      </template>
    </custom-data-table>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  tableItems: any
  headers: any[]
  getData: (params?: any) => Promise<any>
  getCategoryColor: (item: any) => string
  getCategoryIcon: (item: any) => string
  getCategoryLabel: (item: any) => string
  getQuestionsCount: (item: any) => number
  getColumnsCount: (item: any) => number
  getChoicesCount: (item: any) => number
  getPaperSize: (item: any) => string
}>()

defineEmits<{
  (e: 'create-new'): void
  (e: 'edit', item: any): void
  (e: 'scan', id: number | string): void
  (e: 'preview', item: any): void
  (e: 'print', item: any): void
  (e: 'duplicate', item: any): void
  (e: 'confirm-delete', item: any): void
}>()
</script>
