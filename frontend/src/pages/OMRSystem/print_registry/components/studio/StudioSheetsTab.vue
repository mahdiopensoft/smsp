<template>
  <div class="studio-sheets-tab">
    <!-- تنبيه أمني واضح عند عدم توفر طلاب مقيدين في قاعدة البيانات -->
    <v-alert
      v-if="examDetails && (!examDetails.registered_students || examDetails.registered_students.length === 0)"
      type="warning"
      variant="tonal"
      border="start"
      rounded="xl"
      class="mb-4"
    >
      <template #title>
        <div class="d-flex align-center gap-2 font-weight-black text-body-1">
          <v-icon color="warning">mdi-shield-alert-outline</v-icon>
          <span>لا تتوفر سجلات طلاب مقيدين في قاعدة البيانات لهذا الاختبار</span>
        </div>
      </template>
      <div class="text-body-2 mt-1">
        حفاظاً على سلامة الوثائق والكنترول، يمنع النظام توليد كشوف مناداة رسمية أو إصدار أوراق تظليل ببيانات أو أرقام جلوس افتراضية.
        يرجى تسكين وقيد الطلاب وتوليد أرقام جلوسهم من إدارة الاختبارات قبل الشروع في الطباعة الرسمية.
        يمكنك في هذه الأثناء طباعة نماذج كراسات الأسئلة أو إجراء معاينة تجريبية لقالب التظليل فقط.
      </div>
    </v-alert>

    <!-- Controls Toolbar (شريط الفلاتر والبحث السريع وأوامر الطباعة) -->
    <div class="main-card rounded-2xl pa-4 mb-4 border bg-surface elevation-1">
      <!-- السطر الأول: أوامر الطباعة السريعة وخيارات الإنتاج -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-3 border-b">
        <!-- أزرار الطباعة والإنتاج -->
        <div class="d-flex align-center gap-2 flex-wrap">
          <!-- زر الطباعة الرئيسي الفوري -->
          <v-btn
            color="success"
            variant="flat"
            rounded="xl"
            size="default"
            class="font-weight-black shadow-sm px-5"
            prepend-icon="mdi-printer-check"
            :loading="printingBatch"
            :disabled="!targetBatchStudents.length"
            @click="$emit('print-batch')"
          >
            طباعة أوراق التظليل {{ selectedStudentIds.length > 0 ? `المحددة (${selectedStudentIds.length})` : `للكل (${filteredRosterStudents.length})` }}
          </v-btn>

          <!-- كشف تسليم الكنترول -->
          <v-btn
            variant="tonal"
            color="primary"
            rounded="xl"
            class="font-weight-bold px-4"
            prepend-icon="mdi-clipboard-text-outline"
            title="طباعة كشف تسليم الكنترول الرسمي"
            :disabled="!examDetails?.registered_students?.length"
            @click="$emit('print-audit')"
          >
            كشف تسليم الكنترول
          </v-btn>

          <!-- قائمة خيارات الطباعة المتقدمة (تجمع: ورقة فارغة، مقاس A5/A4، تعديل الترويسة) -->
          <v-menu location="bottom end" :close-on-content-click="false">
            <template #activator="{ props: mProps }">
              <v-btn
                v-bind="mProps"
                variant="tonal"
                color="secondary"
                rounded="xl"
                class="font-weight-bold px-3"
                prepend-icon="mdi-cog-outline"
                append-icon="mdi-chevron-down"
              >
                خيارات الطباعة وإعدادات الورق
              </v-btn>
            </template>

            <v-card min-width="280" class="rounded-xl border elevation-4 pa-2 bg-surface">
              <div class="text-caption font-weight-black text-primary px-3 py-2 border-b mb-1 d-flex align-center gap-1">
                <v-icon size="16">mdi-tune</v-icon>
                إعدادات الورقة ونماذج الطباعة
              </div>

              <!-- تبديل المقاس A5 / A4 -->
              <div class="px-3 py-2">
                <div class="text-caption text-medium-emphasis mb-1 font-weight-bold">مقاس الورقة:</div>
                <v-btn-toggle
                  :model-value="selectedSheetLayout"
                  @update:model-value="$emit('update:selectedSheetLayout', $event)"
                  mandatory
                  density="compact"
                  color="primary"
                  variant="outlined"
                  rounded="lg"
                  class="w-100"
                >
                  <v-btn value="compact_a5" class="font-weight-bold flex-1" size="small" prepend-icon="mdi-card-outline">
                    A5 الوزارية
                  </v-btn>
                  <v-btn value="full_a4" class="font-weight-bold flex-1" size="small" prepend-icon="mdi-file-document-outline">
                    A4 الشاملة
                  </v-btn>
                </v-btn-toggle>
              </div>

              <v-divider class="my-1" />

              <!-- تعديل الترويسة -->
              <v-list-item
                rounded="lg"
                prepend-icon="mdi-pencil-outline"
                title="تعديل بيانات الترويسة فورياً"
                subtitle="اسم المركز، المديرية، والمحافظة"
                @click="$emit('update:showAdjustmentsPanel', !showAdjustmentsPanel)"
              />

              <v-divider class="my-1" />

              <!-- ورقة عامة فارغة -->
              <div class="px-3 py-1">
                <div class="text-caption text-medium-emphasis font-weight-bold mb-1">طباعة ورقة عامة فارغة:</div>
                <div class="d-flex gap-1">
                  <v-btn
                    v-for="ver in ['A', 'B', 'C', 'D']"
                    :key="`blank-opt-${ver}`"
                    size="x-small"
                    variant="tonal"
                    color="primary"
                    class="font-weight-bold flex-1"
                    @click="$emit('print-blank', ver)"
                  >
                    نموذج {{ ver }}
                  </v-btn>
                </div>
              </div>
            </v-card>
          </v-menu>
        </div>

        <!-- أدوات التحديد السريع -->
        <div class="d-flex align-center gap-2">
          <v-chip
            v-if="selectedStudentIds.length > 0"
            size="small"
            color="primary"
            variant="flat"
            class="font-weight-bold"
          >
            محدد: {{ selectedStudentIds.length }} طالب
          </v-chip>

          <v-btn
            v-if="filteredRosterStudents.length > 0"
            size="small"
            variant="tonal"
            color="primary"
            rounded="lg"
            class="font-weight-bold"
            :prepend-icon="selectedStudentIds.length === filteredRosterStudents.length ? 'mdi-checkbox-blank-outline' : 'mdi-checkbox-multiple-marked-outline'"
            @click="$emit('select-all')"
          >
            {{ selectedStudentIds.length === filteredRosterStudents.length ? 'إلغاء التحديد' : 'تحديد كل المعروضين' }}
          </v-btn>

          <v-btn
            v-if="selectedStudentIds.length > 0"
            size="small"
            variant="tonal"
            color="success"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-check-all"
            :loading="markingPrintedLoading"
            :disabled="markingPrintedLoading"
            @click="$emit('mark-printed')"
          >
            تحديد كمطبوع
          </v-btn>
        </div>
      </div>

      <!-- Live Adjustments Panel -->
      <v-expand-transition>
        <div v-if="showAdjustmentsPanel" class="pa-4 my-3 bg-surface border rounded-xl">
          <div class="text-caption font-weight-black text-primary mb-3 d-flex align-center justify-space-between">
            <div class="d-flex align-center gap-1">
              <v-icon size="16">mdi-auto-fix</v-icon>
              تعديل بيانات الترويسة فورياً (تنعكس التعديلات لحظياً على كافة أوراق الطلاب المطبوعة)
            </div>
            <v-btn icon="mdi-close" variant="text" size="x-small" @click="$emit('update:showAdjustmentsPanel', false)" />
          </div>
          <v-row dense>
            <v-col cols="12" sm="4">
              <custom-text-field
                :model-value="customCenterName"
                @update:model-value="$emit('update:customCenterName', $event)"
                label="اسم المركز الامتحاني / المدرسة"
                cols="12"
                :placeholder="selectedExam?.directorate || 'المركز الامتحاني الرئيسي'"
              />
            </v-col>
            <v-col cols="12" sm="4">
              <custom-text-field
                :model-value="customDirectorate"
                @update:model-value="$emit('update:customDirectorate', $event)"
                label="المديرية"
                cols="12"
                :placeholder="selectedExam?.directorate || 'السبعين'"
              />
            </v-col>
            <v-col cols="12" sm="4">
              <custom-text-field
                :model-value="customGovernorate"
                @update:model-value="$emit('update:customGovernorate', $event)"
                label="المحافظة"
                cols="12"
                :placeholder="selectedExam?.governorate || 'أمانة العاصمة'"
              />
            </v-col>
            <v-col cols="12" sm="6">
              <custom-text-field
                :model-value="customStageTitle"
                @update:model-value="$emit('update:customStageTitle', $event)"
                label="عنوان الاختبار والمرحلة"
                cols="12"
                :placeholder="selectedExam?.title || 'اختبار الشهادة العامة'"
              />
            </v-col>
            <v-col cols="12" sm="3">
              <custom-text-field
                :model-value="customExamYear"
                @update:model-value="$emit('update:customExamYear', $event)"
                label="العام الدراسي"
                cols="12"
                :placeholder="selectedExam?.year_name || '2026'"
              />
            </v-col>
            <v-col cols="12" sm="3" class="d-flex align-center justify-end">
              <v-btn
                size="small"
                variant="text"
                color="error"
                class="font-weight-bold"
                prepend-icon="mdi-restore"
                @click="$emit('reset-overrides')"
              >
                استعادة البيانات الأصلية
              </v-btn>
            </v-col>
          </v-row>
        </div>
      </v-expand-transition>

      <!-- السطر الثاني: شريط الفلاتر المنسدلة للنموذج وحالة الطباعة -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-2 pt-3">
        <!-- الفلاتر المنسدلة عبر auto-list الموحد -->
        <div class="d-flex align-center gap-2 flex-wrap">
          <!-- فلتر النموذج كمنسدلة عبر auto-list الموحد -->
          <div style="min-width: 190px; max-width: 230px;">
            <auto-list
              :model-value="rosterModelFilter"
              @update:model-value="$emit('update:rosterModelFilter', $event)"
              :objects="modelFilterObjects"
              name="ScreenTypeChoices"
              label="النموذج"
              placeholder="النموذج"
              cols="12"
              :add="false"
            />
          </div>

          <!-- فلتر حالة الطباعة كمنسدلة عبر auto-list الموحد -->
          <div style="min-width: 190px; max-width: 230px;">
            <auto-list
              :model-value="rosterPrintFilter"
              @update:model-value="$emit('update:rosterPrintFilter', $event)"
              :objects="printStatusFilterObjects"
              name="ScreenTypeChoices"
              label="حالة الطباعة"
              placeholder="حالة الطباعة"
              cols="12"
              :add="false"
            />
          </div>

          <!-- زر تفريغ الفلاتر -->
          <v-btn
            v-if="rosterModelFilter !== 'all' || rosterPrintFilter !== 'all' || rosterSearch"
            variant="text"
            color="error"
            size="small"
            class="font-weight-bold"
            prepend-icon="mdi-filter-off-outline"
            @click="$emit('reset-filters')"
          >
            إلغاء التصفية
          </v-btn>
        </div>
      </div>
    </div>

    <!-- ── الجدول الموحد للطلاب وأوراق التظليل (custom-data-table) ── -->
    <div class="main-card rounded-2xl overflow-hidden mb-6">
      <custom-data-table
        :items="rosterTableItems"
        :getData="getRosterData"
        :headers="rosterHeaders"
        :customLoading="loadingExamDetails"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :numbering="true"
        :showSelect="false"
        :search="true"
        class="bg-transparent"
      
        :actionList="(item) => ([ { label: 'معاينة ورقة التظليل', icon: 'eye-outline', color: 'primary', onClick: () => $emit('preview-sheet', item) }, { label: 'طباعة ورقة هذا الطالب فورياً', icon: 'printer', color: 'success', onClick: () => $emit('print-single', item) }, ]).filter((a) => a && a.show !== false).map((a) => ({ title_ar: a.label, title_en: a.label, click: a.onClick }))">
        <template v-slot:item-slot="{ item, key, index }">
          <!-- Numbering -->
          <template v-if="key === 'numbering'">
            <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
          </template>

          <!-- Select Box -->
          <template v-else-if="key === 'select_box'">
            <div class="d-flex justify-center">
              <v-checkbox-btn
                :model-value="selectedStudentIds.includes(item.id)"
                color="primary"
                density="compact"
                hide-details
                @update:model-value="$emit('toggle-select', item.id)"
              />
            </div>
          </template>

          <!-- Seat Number -->
          <template v-else-if="key === 'seat_number'">
            <span class="font-mono font-weight-black text-primary px-2 py-1 bg-blue-lighten-5 rounded-lg border">
              {{ item.seat_number }}
            </span>
          </template>

          <!-- Secret Number -->
          <template v-else-if="key === 'secret_number'">
            <span class="font-mono text-medium-emphasis">
              {{ item.secret_number || '-' }}
            </span>
          </template>

          <!-- Student Info -->
          <template v-else-if="key === 'student_name'">
            <div class="font-weight-bold text-body-2 text-on-surface py-1">
              {{ item.student_name || 'طالب بدون اسم' }}
            </div>
          </template>

          <!-- School / Center -->
          <template v-else-if="key === 'school_name'">
            <div class="py-1">
              <div class="font-weight-medium text-body-2">{{ item.school_name || selectedExam?.directorate || 'المركز الرئيسي' }}</div>
              <div class="text-caption text-medium-emphasis">{{ item.directorate || selectedExam?.directorate || '-' }}</div>
            </div>
          </template>

          <!-- Model Code -->
          <template v-else-if="key === 'model_code'">
            <span class="font-weight-bold font-mono text-body-2 text-primary">
              نموذج {{ item.model_code || 'A' }}
            </span>
          </template>

          <!-- Print Status -->
          <template v-else-if="key === 'is_printed'">
            <v-chip
              size="small"
              :color="item.is_printed ? 'success' : 'grey'"
              :variant="item.is_printed ? 'flat' : 'tonal'"
              class="font-weight-bold unified-table-chip cursor-pointer"
              :title="item._updating ? 'جاري توثيق التحديث في السجل...' : 'انقر لتبديل حالة الطباعة'"
              :disabled="item._updating"
              @click="$emit('toggle-printed', item)"
            >
              <v-progress-circular v-if="item._updating" indeterminate size="12" width="2" class="me-1" />
              {{ item._updating ? 'جاري التحديث...' : (item.is_printed ? 'تمت الطباعة' : 'جاهز للطباعة') }}
            </v-chip>
          </template>

          <!-- Actions -->
          
        </template>
      </custom-data-table>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  examDetails: any
  targetBatchStudents: any[]
  selectedStudentIds: any[]
  filteredRosterStudents: any[]
  printingBatch: boolean
  selectedSheetLayout: string
  showAdjustmentsPanel: boolean
  customCenterName?: string
  customDirectorate?: string
  customGovernorate?: string
  customStageTitle?: string
  customExamYear?: string
  selectedExam: any
  rosterModelFilter: string
  modelFilterObjects: any[]
  rosterPrintFilter: string
  printStatusFilterObjects: any[]
  rosterSearch?: string
  rosterTableItems: any
  getRosterData: any
  rosterHeaders: any[]
  loadingExamDetails: boolean
  markingPrintedLoading?: boolean
  getModelChipColor: (code?: string) => string
}>()

defineEmits<{
  (e: 'update:selectedSheetLayout', val: string): void
  (e: 'update:showAdjustmentsPanel', val: boolean): void
  (e: 'update:customCenterName', val: string): void
  (e: 'update:customDirectorate', val: string): void
  (e: 'update:customGovernorate', val: string): void
  (e: 'update:customStageTitle', val: string): void
  (e: 'update:customExamYear', val: string): void
  (e: 'update:rosterModelFilter', val: string): void
  (e: 'update:rosterPrintFilter', val: string): void
  (e: 'print-batch'): void
  (e: 'print-audit'): void
  (e: 'print-blank', ver: string): void
  (e: 'select-all'): void
  (e: 'mark-printed'): void
  (e: 'reset-overrides'): void
  (e: 'reset-filters'): void
  (e: 'toggle-select', id: any): void
  (e: 'toggle-printed', item: any): void
  (e: 'preview-sheet', item: any): void
  (e: 'print-single', item: any): void
}>()
</script>
