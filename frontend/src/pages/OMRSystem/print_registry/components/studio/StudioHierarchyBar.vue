<template>
  <div class="main-card pa-4 rounded-2xl mb-4 bg-surface border elevation-1">
    <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3 pb-2 border-b">
      <div class="d-flex align-center gap-3 flex-wrap">
        <v-icon color="primary" size="20">mdi-filter-variant</v-icon>
        <span class="text-subtitle-2 font-weight-black text-on-surface">فلاتر الهيكل واختيار الاختبار:</span>

        <v-chip
          v-if="selectedSchoolName"
          size="small"
          color="info"
          variant="tonal"
          closable
          class="font-weight-bold ms-1"
          prepend-icon="mdi-filter-check"
          @click:close="$emit('clear-school-filter')"
        >
          {{ selectedSchoolName }} ({{ examDetails?.registered_students?.length || 0 }} طالب)
        </v-chip>
      </div>

      <div class="d-flex align-center gap-2">
        <v-btn
          color="primary"
          variant="tonal"
          size="small"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-arrow-right"
          @click="$emit('return-to-master')"
        >
          العودة للهيكل الإداري
        </v-btn>
        <v-btn
          v-if="selectedExam"
          variant="text"
          color="primary"
          size="small"
          class="font-weight-bold"
          :prepend-icon="showHierarchyFilters ? 'mdi-chevron-up' : 'mdi-tune'"
          @click="$emit('update:showHierarchyFilters', !showHierarchyFilters)"
        >
          {{ showHierarchyFilters ? 'إخفاء محدد الاختبار' : 'تغيير الاختبار أو المدرسة' }}
        </v-btn>
        <v-btn
          variant="tonal"
          color="error"
          size="small"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-filter-remove-outline"
          @click="$emit('reset-filters')"
        >
          تفريغ الفلاتر
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          size="small"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-refresh"
          :loading="loadingExams"
          @click="$emit('refresh')"
        >
          تحديث
        </v-btn>
      </div>
    </div>

    <v-expand-transition>
      <div v-show="!selectedExam || showHierarchyFilters">
        <v-row dense class="align-center">
          <!-- نوع المؤسسة التعليمية كفلتر منسدل أساسي عبر auto-list الموحد -->
          <v-col cols="12" sm="6" :md="institutionType === 'school' ? 4 : 3" :lg="institutionType === 'school' ? 2 : 3">
            <auto-list
              :model-value="institutionType"
              @update:model-value="(val) => { $emit('update:institutionType', val); $emit('sector-change', val); }"
              :objects="sectorOptionsObjects"
              name="ScreenTypeChoices"
              label="نوع المؤسسة التعليمية"
              placeholder="نوع المؤسسة التعليمية"
              cols="12"
              :add="false"
              :hideDetails="true"
            />
          </v-col>

          <!-- التعليم العام (المدرسي): محافظة -> مديرية -> مدرسة/مركز عبر auto-list الموحد -->
          <template v-if="institutionType === 'school'">
            <v-col cols="12" sm="6" md="4" lg="2">
              <auto-list
                :model-value="selectedOfficeId"
                @update:model-value="(val) => { $emit('update:selectedOfficeId', val); $emit('office-change', val); }"
                :objects="officesObjects"
                name="ScreenTypeChoices"
                label="مكتب التربية (المحافظة)"
                placeholder="كل المحافظات..."
                cols="12"
                :add="false"
                :hideDetails="true"
              />
            </v-col>

            <v-col cols="12" sm="6" md="4" lg="2">
              <auto-list
                :model-value="selectedDirectorateId"
                @update:model-value="(val) => { $emit('update:selectedDirectorateId', val); $emit('directorate-change', val); }"
                :objects="directoratesObjectsFormatted"
                name="ScreenTypeChoices"
                label="إدارة التربية (المديرية)"
                placeholder="كل المديريات..."
                cols="12"
                :add="false"
                :hideDetails="true"
              />
            </v-col>

            <v-col cols="12" sm="6" md="6" lg="3">
              <auto-list
                :model-value="selectedSchoolId"
                @update:model-value="(val) => { $emit('update:selectedSchoolId', val); $emit('school-change', val); }"
                :objects="schoolsObjectsFormatted"
                name="ScreenTypeChoices"
                label="المدرسة / المركز الامتحاني"
                placeholder="كل المراكز والمدارس..."
                cols="12"
                :add="false"
                :hideDetails="true"
              />
            </v-col>
          </template>

          <!-- التعليم الجامعي: جامعة/كلية عبر auto-list الموحد -->
          <template v-else-if="institutionType === 'university'">
            <v-col cols="12" sm="6" md="4" lg="4">
              <auto-list
                :model-value="selectedSchoolId"
                @update:model-value="(val) => { $emit('update:selectedSchoolId', val); $emit('school-change', val); }"
                :objects="schoolsObjectsFormatted"
                name="ScreenTypeChoices"
                label="الجامعة / الكلية"
                placeholder="اختر الكلية أو الجامعة..."
                cols="12"
                :add="false"
                :hideDetails="true"
              />
            </v-col>
          </template>

          <!-- التعليم الفني (معاهد): معهد/مركز عبر auto-list الموحد -->
          <template v-else-if="institutionType === 'institute'">
            <v-col cols="12" sm="6" md="4" lg="4">
              <auto-list
                :model-value="selectedSchoolId"
                @update:model-value="(val) => { $emit('update:selectedSchoolId', val); $emit('school-change', val); }"
                :objects="schoolsObjectsFormatted"
                name="ScreenTypeChoices"
                label="المعهد / المركز الفني"
                placeholder="اختر المعهد أو المركز..."
                cols="12"
                :add="false"
                :hideDetails="true"
              />
            </v-col>
          </template>

          <!-- منسدلة اختيار الاختبار المعتمد المطلوب طباعة وثائقه عبر auto-list الموحد -->
          <v-col cols="12" :sm="institutionType === 'school' ? 6 : 12" :md="institutionType === 'school' ? 6 : 5" :lg="institutionType === 'school' ? 3 : 5">
            <auto-list
              :model-value="selectedExamId"
              @update:model-value="(val) => { $emit('update:selectedExamId', val); $emit('exam-selected', val); }"
              :objects="examsObjectsFormatted"
              name="ScreenTypeChoices"
              label="الاختبار المعتمد المطلوب طباعته"
              placeholder="ابحث بالاختبار أو المادة أو الرمز..."
              cols="12"
              :add="false"
              :hideDetails="true"
            />
          </v-col>
        </v-row>
      </div>
    </v-expand-transition>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  selectedSchoolName?: string
  examDetails?: any
  selectedExam?: any
  showHierarchyFilters: boolean
  loadingExams?: boolean
  institutionType: string
  sectorOptionsObjects?: any[]
  selectedOfficeId?: any
  officesObjects?: any[]
  selectedDirectorateId?: any
  directoratesObjectsFormatted?: any[]
  selectedSchoolId?: any
  schoolsObjectsFormatted?: any[]
  selectedExamId?: any
  examsObjectsFormatted?: any[]
}>()

defineEmits<{
  (e: 'update:showHierarchyFilters', val: boolean): void
  (e: 'update:institutionType', val: string): void
  (e: 'update:selectedOfficeId', val: any): void
  (e: 'update:selectedDirectorateId', val: any): void
  (e: 'update:selectedSchoolId', val: any): void
  (e: 'update:selectedExamId', val: any): void
  (e: 'clear-school-filter'): void
  (e: 'return-to-master'): void
  (e: 'reset-filters'): void
  (e: 'refresh'): void
  (e: 'sector-change', val: string): void
  (e: 'office-change', val: any): void
  (e: 'directorate-change', val: any): void
  (e: 'school-change', val: any): void
  (e: 'exam-selected', val: any): void
}>()
</script>
