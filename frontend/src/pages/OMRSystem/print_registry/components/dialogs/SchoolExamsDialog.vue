<template>
  <custom-dialog
    :model-value="modelValue"
    :title="school?.name || 'اختبارات المدرسة'"
    width="1180"
    height="88vh"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <div class="text-caption text-medium-emphasis d-flex align-center gap-2 flex-wrap mb-4 pb-3 border-b">
      <span>{{ school?.directorate_name }} • {{ school?.governorate_name }}</span>
      <span>|</span>
      <span>إجمالي الطلاب: <strong class="text-primary">{{ school?.total_students || 0 }} طالب</strong></span>
      <span>|</span>
      <span>عدد الاختبارات: <strong class="text-teal">{{ school?.exams?.length || school?.exams_count || 0 }} اختبار</strong></span>
    </div>

    <div v-if="!school?.exams || school.exams.length === 0" class="text-center py-8">
      <v-icon size="48" color="grey">mdi-file-document-outline</v-icon>
      <div class="text-body-1 text-medium-emphasis mt-2">لا توجد اختبارات مسجلة لهذه المدرسة حالياً</div>
    </div>

    <div v-else class="d-flex flex-column gap-3">
      <v-alert
        type="info"
        variant="tonal"
        density="compact"
        rounded="xl"
        class="mb-2 text-caption font-weight-medium"
      >
        <template v-slot:prepend>
          <v-icon size="20" color="info">mdi-information-outline</v-icon>
        </template>
        كل صف أدناه يمثل <strong>اختباراً مستقلاً معتمداً</strong> مقيد به طلاب المدرسة، وموضح أمامه <strong>النماذج الامتحانية (A, B, C...)</strong> وتوزيع الطلاب عليها، مع إمكانية طباعة وثائق أي اختبار مباشرة.
      </v-alert>

      <!-- ── الجدول الموحد للاختبارات والمواد المعتمدة للمدرسة (custom-data-table) ── -->
      <div class="main-card rounded-2xl overflow-hidden border">
        <custom-data-table
          :items="tableItems"
          :getData="getData"
          :headers="headers"
          :hasFilter="false"
          :log="false"
          :restore="false"
          :showSelect="false"
          :search="true"
          :actionList="(item) => ([ { label: 'طباعة الاختبار', icon: 'printer', color: 'primary', onClick: () => $emit('select-exam', item, school) }, ]).filter((a) => a && a.show !== false).map((a) => ({ title_ar: a.label, title_en: a.label, click: a.onClick }))"
        >
          <template v-slot:item-slot="{ item, key }">
            <template v-if="key === 'code'">
              <span class="font-mono font-weight-bold text-body-2">{{ item.code }}</span>
            </template>

            <template v-else-if="key === 'title'">
              <div class="py-1 font-weight-bold text-body-2 text-on-surface text-truncate" :title="item.title">
                {{ item.title }}
              </div>
            </template>

            <template v-else-if="key === 'subject'">
              <span class="text-body-2 font-weight-medium">{{ item.subject || 'عام' }}</span>
            </template>

            <template v-else-if="key === 'students_count'">
              <span class="font-mono font-weight-bold text-body-2">{{ item.students_count || 0 }} طالب</span>
            </template>

            <template v-else-if="key === 'versions'">
              <span v-if="item.versions && item.versions.length > 0" class="text-caption font-mono">
                {{ item.versions.map(v => `${v.code} (${v.students_count})`).join('، ') }}
              </span>
              <span v-else class="text-caption text-medium-emphasis">—</span>
            </template>
          </template>
        </custom-data-table>
      </div>
    </div>

    <template #actions>
      <div class="d-flex justify-space-between align-center flex-wrap gap-2 w-100">
        <div class="text-caption text-medium-emphasis d-flex align-center gap-1">
          <v-icon size="16" color="primary">mdi-cursor-default-click-outline</v-icon>
          يمكنك اختيار اختبار معين للطباعة أو فتح استوديو الطباعة الشامل للمركز
        </div>
        <div class="d-flex gap-2">
          <v-btn variant="tonal" color="grey" rounded="lg" class="font-weight-bold px-4" @click="$emit('update:modelValue', false)">
            إغلاق
          </v-btn>
          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            prepend-icon="mdi-printer-check"
            class="font-weight-bold px-4"
            @click="$emit('open-studio', school); $emit('update:modelValue', false);"
          >
            فتح استوديو الطباعة الشامل للمركز
          </v-btn>
        </div>
      </div>
    </template>
  </custom-dialog>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: boolean
  school: any
  tableItems: any
  getData: (params?: any) => Promise<any>
  headers: any[]
}>()

defineEmits<{
  (e: 'update:modelValue', val: boolean): void
  (e: 'select-exam', item: any, school: any): void
  (e: 'open-studio', school: any): void
}>()
</script>
