<template>
  <div class="master-exams-tab-component">
    <!-- ── شريط التبويبات الفرعية الأربعة: الطلبات / المجدولة / المستحقة / المكتملة ── -->
    <div class="d-flex align-center justify-space-between flex-wrap gap-2 px-4 py-2 border-b bg-surface-variant-subtle">
      <v-tabs
        :model-value="subTab"
        @update:model-value="$emit('update:subTab', $event)"
        color="primary"
        density="compact"
        class="sub-stage-tabs"
      >
        <!-- 1. الطلبات (الطلبات الجارية وغير المكتملة) -->
        <v-tab value="orders" class="font-weight-bold">
          <v-icon start size="18" color="primary">mdi-format-list-bulleted</v-icon>
          الطلبات ({{ pendingAndActiveOrdersCount }})
        </v-tab>

        <!-- 2. المجدولة (المستقبلية) -->
        <v-tab value="scheduled" class="font-weight-bold">
          <v-icon start size="18" color="info">mdi-calendar-clock</v-icon>
          المجدولة ({{ scheduledExamsCount }})
        </v-tab>

        <!-- 3. المستحقة (قائمة انتظار الطباعة الجاهزة للتنفيذ) -->
        <v-tab value="due" class="font-weight-bold">
          <v-icon start size="18" color="warning">mdi-clock-alert-outline</v-icon>
          المستحقة ({{ dueExamsCount }})
        </v-tab>

        <!-- 4. المكتملة (الاختبارات التي تم سحب وثائقها بالكامل) -->
        <v-tab value="completed" class="font-weight-bold">
          <v-icon start size="18" color="primary">mdi-check-decagram</v-icon>
          المكتملة ({{ completedExamsCount }})
        </v-tab>

        <!-- 5. الملغية (أوامر ملغاة رسمياً من الكنترول) -->
        <v-tab value="cancelled" class="font-weight-bold">
          <v-icon start size="18" color="secondary">mdi-cancel</v-icon>
          الملغية ({{ cancelledExamsCount }})
        </v-tab>

        <!-- 6. السجل الشامل (كافة الاختبارات لكافة الحالات) -->
        <v-tab value="all" class="font-weight-bold">
          <v-icon start size="18" color="medium-emphasis">mdi-archive-outline</v-icon>
          السجل الشامل ({{ allExamsCount }})
        </v-tab>
      </v-tabs>

      <div class="d-flex align-center gap-2">
        <v-chip
          size="small"
          variant="tonal"
          :color="subTab === 'due' ? 'warning' : (subTab === 'scheduled' ? 'info' : (subTab === 'cancelled' ? 'secondary' : (subTab === 'all' ? 'default' : 'primary')))"
          class="font-weight-medium"
        >
          <v-icon start size="14">
            {{ subTab === 'due' ? 'mdi-clock-fast' : (subTab === 'scheduled' ? 'mdi-calendar-range' : (subTab === 'completed' ? 'mdi-check-all' : (subTab === 'cancelled' ? 'mdi-cancel' : (subTab === 'all' ? 'mdi-archive-outline' : 'mdi-file-document-multiple-outline')))) }}
          </v-icon>
          {{ subTab === 'due' ? 'المستحقة للتنفيذ' : (subTab === 'scheduled' ? 'أوامر مجدولة' : (subTab === 'completed' ? 'مكتملة 100%' : (subTab === 'cancelled' ? 'طلبات ملغاة' : (subTab === 'all' ? 'السجل الشامل (الكل)' : 'الطلبات النشطة')))) }}
        </v-chip>
      </div>
    </div>

    <!-- عرض الجدول المركزي للاختبارات حسب التبويب النشط -->
    <custom-data-table
      :key="'exams-tbl-' + subTab"
      :model-value="selectedRows"
      @update:model-value="$emit('update:selectedRows', $event)"
      :items="items"
      :getData="getData"
      :headers="headers"
      :customLoading="loading"
      :hasFilter="false"
      :log="false"
      :restore="false"
      :numbering="true"
      :showSelect="true"
      :actionList="getRowActions"
      :search="true"
      class="bg-transparent"
    >
      <template v-slot:item-slot="{ item, key, index }">
        <template v-if="key === 'numbering'">
          <div class="d-flex justify-center align-center">
            <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
          </div>
        </template>

        <template v-else-if="key === 'uniqueCode'">
          <div class="d-flex justify-center align-center">
            <span class="font-mono font-weight-bold text-caption px-2 py-1 rounded bg-grey-lighten-4 border">
              {{ item.uniqueCode }}
            </span>
          </div>
        </template>

        <template v-else-if="key === 'title'">
          <div class="py-2" style="min-width: 280px;">
            <div class="font-weight-bold text-subtitle-2 text-on-surface text-wrap">{{ item.title }}</div>
            <div class="d-flex align-center flex-wrap gap-2 text-caption text-medium-emphasis mt-0.5">
              <span class="font-weight-medium">المادة: {{ item.subject_name || 'عام' }}</span>
              <span v-if="item.order_number" class="text-primary font-mono font-weight-bold">
                • {{ item.order_number }}
              </span>
              <span v-if="item.exam_date" class="text-medium-emphasis">
                • الامتحان: {{ item.exam_date }}
              </span>
              <span v-if="item.scheduled_print_date" class="text-medium-emphasis">
                • الطباعة: {{ item.scheduled_print_date }}
              </span>
            </div>

            <!-- شريط توضيح سبب الإرجاع إذا كان الطلب مرتجعاً -->
            <div
              v-if="item.order_status === 'returned' || item.is_returned"
              class="mt-1 text-error text-caption font-weight-bold"
            >
              <span>سبب الإرجاع: {{ item.return_reason || 'يحتاج مراجعة وتعديل فني' }}</span>
              <span v-if="item.return_notes" class="text-medium-emphasis ms-1 font-weight-regular">({{ item.return_notes }})</span>
            </div>
          </div>
        </template>

        <template v-else-if="key === 'schools_count'">
          <div class="d-flex justify-center align-center">
            <span class="font-weight-bold text-subtitle-2">{{ item.schools_count ?? 0 }}</span>
          </div>
        </template>

        <template v-else-if="key === 'total_registered'">
          <div class="d-flex justify-center align-center">
            <span class="font-weight-bold text-subtitle-2">{{ item.total_registered || item.total_students || 0 }}</span>
          </div>
        </template>

        <template v-else-if="key === 'printed_count'">
          <div class="d-flex justify-center align-center">
            <span class="font-weight-bold text-primary">{{ item.printed_count || 0 }} ورقة</span>
          </div>
        </template>

        <template v-else-if="key === 'printed_rate'">
          <div class="d-flex align-center justify-center gap-2 px-1">
            <v-progress-linear
              :model-value="item.printed_rate || 0"
              :color="(item.printed_rate >= 100) ? 'success' : (item.printed_rate > 0 ? 'warning' : 'primary')"
              height="8"
              rounded
              style="min-width: 60px; max-width: 80px;"
            />
            <span class="text-caption font-weight-bold">{{ item.printed_rate || 0 }}%</span>
          </div>
        </template>

        <template v-else-if="key === 'print_status'">
          <div class="d-flex justify-center align-center">
            <v-chip
              v-if="item.is_completed || item.order_status === 'completed'"
              size="small"
              color="primary"
              variant="tonal"
              class="font-weight-bold"
            >
              مكتمل
            </v-chip>
            <v-chip
              v-else-if="item.order_status === 'printing'"
              size="small"
              color="warning"
              variant="tonal"
              class="font-weight-bold"
            >
              قيد الطباعة
            </v-chip>
            <v-chip
              v-else-if="item.is_scheduled || item.order_status === 'scheduled'"
              size="small"
              color="info"
              variant="tonal"
              class="font-weight-bold"
            >
              بانتظار الموعد
            </v-chip>
            <v-chip
              v-else-if="item.is_returned || item.order_status === 'failed' || item.order_status === 'returned'"
              size="small"
              color="error"
              variant="tonal"
              class="font-weight-bold"
              :title="item.return_reason || 'مرتجع للتعديل'"
            >
              فشل أو يحتاج معالجة
            </v-chip>
            <v-chip
              v-else-if="item.order_status === 'cancelled'"
              size="small"
              color="grey"
              variant="tonal"
              class="font-weight-bold"
            >
              ملغى
            </v-chip>
            <v-chip
              v-else-if="item.is_pending || item.order_status === 'pending'"
              size="small"
              color="warning"
              variant="tonal"
              class="font-weight-bold"
            >
              بانتظار الاعتماد
            </v-chip>
            <v-chip
              v-else
              size="small"
              color="primary"
              variant="tonal"
              class="font-weight-bold"
            >
              جاهز للتنفيذ
            </v-chip>
          </div>
        </template>

      </template>
    </custom-data-table>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  items: any
  getData: (params?: any) => Promise<any>
  headers: any[]
  loading?: boolean
  selectedRows: any[]
  subTab: string
  pendingAndActiveOrdersCount: number
  scheduledExamsCount: number
  dueExamsCount: number
  completedExamsCount: number
  cancelledExamsCount: number
  allExamsCount: number
}>()

const emit = defineEmits<{
  (e: 'update:selectedRows', val: any[]): void
  (e: 'update:subTab', val: string): void
  (e: 'direct-print', item: any): void
  (e: 'open-studio', item: any): void
  (e: 'preview-manifest', item: any): void
  (e: 'approve-order', item: any): void
  (e: 'return-order', item: any): void
  (e: 'advance-schedule', item: any): void
  (e: 'cancel-order', item: any): void
  (e: 'view-history', item: any): void
}>()

const getRowActions = (item: any) => {
  const build = (arr: any[]) =>
    arr
      .filter((a) => a && a.show !== false)
      .map((a) => ({ title_ar: a.label, title_en: a.label, click: a.onClick }))

  if (props.subTab === 'due') {
    return build([
      { label: 'طباعة مباشرة فورية', onClick: () => emit('direct-print', item) },
      { label: 'فتح استوديو الطباعة التفصيلي', onClick: () => emit('open-studio', item) },
      { label: 'معاينة إذن الصرف الرسمي A4', show: Boolean(item.has_order), onClick: () => emit('preview-manifest', item) },
      { label: 'إلغاء أمر الطباعة رسمياً', onClick: () => emit('cancel-order', item) },
    ])
  }
  if (props.subTab === 'scheduled') {
    return build([
      { label: 'تقديم موعد الطباعة استثنائياً', onClick: () => emit('advance-schedule', item) },
      { label: 'معاينة إذن الصرف الرسمي A4', show: Boolean(item.has_order), onClick: () => emit('preview-manifest', item) },
      { label: 'إلغاء أمر الطباعة رسمياً', onClick: () => emit('cancel-order', item) },
    ])
  }
  if (props.subTab === 'completed') {
    return build([
      { label: 'معاينة إذن الصرف والتسليم A4', show: Boolean(item.has_order), onClick: () => emit('preview-manifest', item) },
      { label: 'سجل وتاريخ دفعات السحب', onClick: () => emit('view-history', item) },
    ])
  }
  if (props.subTab === 'cancelled') {
    return build([
      { label: 'إعادة تفعيل واعتماد الطلب', onClick: () => emit('approve-order', item) },
      { label: 'معاينة إذن الصرف المحفوظ', show: Boolean(item.has_order), onClick: () => emit('preview-manifest', item) },
    ])
  }
  if (item.is_completed) {
    return build([
      { label: 'معاينة إذن الصرف والتسليم A4', show: Boolean(item.has_order), onClick: () => emit('preview-manifest', item) },
      { label: 'سجل وتاريخ دفعات السحب', onClick: () => emit('view-history', item) },
    ])
  }
  if (item.is_pending) {
    return build([
      { label: 'تأكيد واعتماد وجدولة الطلب', onClick: () => emit('approve-order', item) },
      { label: 'إرجاع الطلب للتعديل', onClick: () => emit('return-order', item) },
      { label: 'معاينة إذن الصرف واستمارة الطلب', show: Boolean(item.has_order), onClick: () => emit('preview-manifest', item) },
      { label: 'إلغاء أمر الطباعة رسمياً', onClick: () => emit('cancel-order', item) },
    ])
  }
  if (item.is_returned) {
    return build([
      { label: 'إعادة الاعتماد بعد التعديل', onClick: () => emit('approve-order', item) },
      { label: 'عرض سبب الإرجاع', onClick: () => emit('return-order', item) },
      { label: 'معاينة إذن الصرف الرسمي A4', show: Boolean(item.has_order), onClick: () => emit('preview-manifest', item) },
      { label: 'إلغاء أمر الطباعة رسمياً', onClick: () => emit('cancel-order', item) },
    ])
  }
  if (item.is_scheduled) {
    return build([
      { label: 'تقديم موعد الطباعة استثنائياً', onClick: () => emit('advance-schedule', item) },
      { label: 'معاينة إذن الصرف الرسمي A4', show: Boolean(item.has_order), onClick: () => emit('preview-manifest', item) },
      { label: 'إلغاء أمر الطباعة رسمياً', onClick: () => emit('cancel-order', item) },
    ])
  }
  if (item.is_due) {
    return build([
      { label: 'الانتقال لتنفيذ الطباعة', onClick: () => emit('update:subTab', 'due') },
      { label: 'معاينة إذن الصرف الرسمي A4', show: Boolean(item.has_order), onClick: () => emit('preview-manifest', item) },
      { label: 'إلغاء أمر الطباعة رسمياً', onClick: () => emit('cancel-order', item) },
    ])
  }
  return build([
    { label: 'تأكيد واعتماد طلب الطباعة', onClick: () => emit('approve-order', item) },
    { label: 'إرجاع الطلب للتعديل', onClick: () => emit('return-order', item) },
  ])
}
</script>
