<template>
  <div class="template-table">
    <custom-data-table
      v-bind="{
        items: tableItems,
        getData,
        headers,
        editItem: (item: any) => $emit('edit', item),
        create: () => $emit('create-new'),
      }"
      :hasFilter="false"
      :log="false"
      :restore="false"
    >
      <template v-slot:item-slot="{ item, key }">
        <!-- Template Name and Subtitle -->
        <template v-if="key === 'name'">
          <div class="d-flex align-center gap-3 py-1">
            <v-avatar size="36" color="primary" variant="tonal" class="rounded-lg">
              <v-icon size="20">mdi-file-document-edit-outline</v-icon>
            </v-avatar>
            <div>
              <div class="font-weight-black text-body-2 text-primary">{{ item.name }}</div>
              <div class="text-caption text-medium-emphasis">{{ item.description || 'قالب تصحيح آلي عالي الدقة 300 DPI' }}</div>
            </div>
          </div>
        </template>

        <!-- Category / Organization -->
        <template v-else-if="key === 'category'">
          <v-chip
            size="small"
            :color="getCategoryColor(item)"
            variant="tonal"
            class="font-weight-bold"
          >
            <v-icon start size="14">{{ getCategoryIcon(item) }}</v-icon>
            {{ getCategoryLabel(item) }}
          </v-chip>
        </template>

        <!-- Questions Count -->
        <template v-else-if="key === 'total_mcq'">
          <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
            <v-icon start size="14">mdi-help-circle-outline</v-icon>
            {{ getQuestionsCount(item) }} سؤال
          </v-chip>
        </template>

        <!-- Columns & Layout -->
        <template v-else-if="key === 'layout'">
          <v-chip size="small" color="info" variant="tonal" class="font-weight-bold">
            <v-icon start size="14">mdi-view-column-outline</v-icon>
            {{ getColumnsCount(item) }} أعمدة ({{ getChoicesCount(item) }} خيارات)
          </v-chip>
        </template>

        <!-- Paper Size -->
        <template v-else-if="key === 'paper_size'">
          <v-chip size="small" color="secondary" variant="tonal" class="font-weight-bold">
            <v-icon start size="14">mdi-file-outline</v-icon>
            {{ getPaperSize(item) }}
          </v-chip>
        </template>

        <!-- Version -->
        <template v-else-if="key === 'version'">
          <v-chip size="small" color="grey-darken-2" variant="tonal" class="font-weight-bold">
            v{{ item.version || '1.0' }}
          </v-chip>
        </template>

        <!-- Is Active Status -->
        <template v-else-if="key === 'is_active'">
          <v-chip
            size="small"
            :color="item.is_active !== false ? 'success' : 'error'"
            variant="tonal"
            class="font-weight-bold text-white"
          >
            <v-icon start size="14">{{ item.is_active !== false ? 'mdi-check-circle' : 'mdi-close-circle' }}</v-icon>
            {{ item.is_active !== false ? 'مفعل' : 'معطل' }}
          </v-chip>
        </template>

        <!-- Custom Actions Bar -->
        <template v-else-if="key === 'actions'">
          <div class="d-flex align-center justify-center gap-1">
            <custom-btn
              is-icon
              icon="scanner"
              color="success"
              label="بدء التصحيح الضوئي بهذا القالب"
              :click="() => $emit('scan', item.id)"
            />
            <custom-btn
              type="show"
              is-icon
              label="معاينة الورقة"
              :click="() => $emit('preview', item)"
            />
            <custom-btn
              type="update"
              is-icon
              label="تعديل القالب"
              :click="() => $emit('edit', item)"
            />
            <custom-btn
              is-icon
              icon="printer"
              color="secondary"
              label="طباعة القالب"
              :click="() => $emit('print', item)"
            />
            <custom-btn
              is-icon
              icon="content-copy"
              color="info"
              label="نسخ كقالب جديد"
              :click="() => $emit('duplicate', item)"
            />
            <custom-btn
              type="del"
              is-icon
              label="حذف القالب"
              :click="() => $emit('confirm-delete', item)"
            />
          </div>
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
