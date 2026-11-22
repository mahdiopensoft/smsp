<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" width="1180px" max-width="95vw" scrollable>
    <v-card rounded="2xl" class="border elevation-6 overflow-hidden main-card">
      <v-card-title class="d-flex align-center justify-space-between bg-surface pa-4 px-6 border-b">
        <div class="d-flex align-center gap-3">
          <v-avatar color="primary" variant="tonal" size="44" class="rounded-xl flex-shrink-0">
            <v-icon color="primary" size="24">mdi-school</v-icon>
          </v-avatar>
          <div>
            <div class="text-subtitle-1 font-weight-black text-on-surface">{{ school?.name }}</div>
            <div class="text-caption text-medium-emphasis d-flex align-center gap-2 flex-wrap mt-0.5">
              <span>{{ school?.directorate_name }} • {{ school?.governorate_name }}</span>
              <span>|</span>
              <span>إجمالي الطلاب: <strong class="text-primary">{{ school?.total_students || 0 }} طالب</strong></span>
              <span>|</span>
              <span>عدد الاختبارات: <strong class="text-teal">{{ school?.exams?.length || school?.exams_count || 0 }} اختبار</strong></span>
            </div>
          </div>
        </div>
        <v-btn icon="mdi-close" variant="text" size="small" @click="$emit('update:modelValue', false)" />
      </v-card-title>

      <v-card-text class="pa-4 pa-md-5 bg-surface">
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
              :actions="false"
              :search="false"
            >
              <template v-slot:item-slot="{ item, key }">
                <template v-if="key === 'code'">
                  <div class="d-flex justify-center align-center">
                    <v-chip size="small" color="primary" variant="tonal" class="font-mono font-weight-bold px-2">
                      {{ item.code }}
                    </v-chip>
                  </div>
                </template>

                <template v-else-if="key === 'title'">
                  <div class="d-flex align-center gap-2.5 py-1.5">
                    <v-avatar color="teal" variant="tonal" size="32" class="rounded-lg flex-shrink-0">
                      <v-icon color="teal" size="18">mdi-book-education-outline</v-icon>
                    </v-avatar>
                    <div class="text-truncate">
                      <div class="font-weight-bold text-body-2 text-on-surface text-truncate" :title="item.title">
                        {{ item.title }}
                      </div>
                      <div class="d-flex align-center gap-1.5 mt-0.5">
                        <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold px-1.5">
                          اختبار مستقل
                        </v-chip>
                      </div>
                    </div>
                  </div>
                </template>

                <template v-else-if="key === 'subject'">
                  <div class="d-flex justify-center align-center">
                    <v-chip size="small" color="teal" variant="flat" class="font-weight-bold px-2.5">
                      <v-icon size="13" start>mdi-book-outline</v-icon>
                      {{ item.subject || 'عام' }}
                    </v-chip>
                  </div>
                </template>

                <template v-else-if="key === 'students_count'">
                  <div class="d-flex justify-center align-center">
                    <v-chip size="small" color="primary" variant="tonal" class="font-weight-black px-2.5">
                      <v-icon size="13" start>mdi-account-group-outline</v-icon>
                      {{ item.students_count || 0 }} طالب
                    </v-chip>
                  </div>
                </template>

                <template v-else-if="key === 'versions'">
                  <div v-if="item.versions && item.versions.length > 0" class="d-flex align-center justify-center gap-1.5 flex-wrap py-1">
                    <v-chip
                      v-for="v in item.versions"
                      :key="v.code"
                      size="x-small"
                      variant="outlined"
                      color="primary"
                      class="font-weight-bold px-2"
                    >
                      <v-icon size="11" start>mdi-file-document-check-outline</v-icon>
                      نموذج {{ v.code }} ({{ v.students_count }} طالب)
                    </v-chip>
                  </div>
                  <div v-else class="text-center text-caption text-medium-emphasis">—</div>
                </template>

                <template v-else-if="key === 'actions'">
                  <div class="d-flex justify-center align-center">
                    <v-btn
                      size="small"
                      color="primary"
                      variant="flat"
                      rounded="lg"
                      prepend-icon="mdi-printer"
                      class="font-weight-bold px-3"
                      @click="$emit('select-exam', item, school)"
                    >
                      طباعة
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </div>
        </div>
      </v-card-text>

      <v-divider />
      <v-card-actions class="pa-4 bg-surface d-flex justify-space-between align-center flex-wrap gap-2">
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
      </v-card-actions>
    </v-card>
  </v-dialog>
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
