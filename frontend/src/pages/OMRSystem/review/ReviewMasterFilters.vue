<template>
  <filter-fields label="خيارات التصفية الأكاديمية والهرمية لمراجعة وتدقيق أوراق الإجابة" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
    <v-row dense class="align-center">
      <!-- 1. نوع المؤسسة التعليمية -->
      <v-col cols="12" sm="6" :md="institutionType === 'school' ? 2 : 3">
        <auto-list
          :model-value="institutionType"
          name="InstitutionType"
          :objects="sectorOptionsObjects"
          label="نوع المؤسسة التعليمية"
          placeholder="نوع المؤسسة التعليمية"
          cols="12"
          :add="false"
          :hideDetails="true"
          @update:model-value="$emit('update:institutionType', $event)"
        />
      </v-col>

      <!-- التعليم العام (مدرسي) -->
      <template v-if="institutionType === 'school'">
        <v-col cols="12" sm="6" md="2">
          <auto-list
            :model-value="selectedOfficeId"
            name="Governorate"
            :objects="officesObjects"
            label="مكتب التربية (المحافظة)"
            placeholder="اختر مكتب أو أكثر..."
            cols="12"
            multiple
            :add="false"
            :hideDetails="true"
            @update:model-value="$emit('update:selectedOfficeId', $event)"
          />
        </v-col>

        <v-col cols="12" sm="6" md="2">
          <auto-list
            :model-value="selectedDirectorateId"
            name="Directorate"
            :objects="directoratesObjects"
            label="إدارة التربية (المديرية)"
            placeholder="اختر مديرية أو أكثر..."
            cols="12"
            multiple
            :add="false"
            :hideDetails="true"
            @update:model-value="$emit('update:selectedDirectorateId', $event)"
          />
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <auto-list
            :model-value="selectedSchoolId"
            name="Organization"
            :objects="schoolsObjects"
            label="المدرسة / المركز الامتحاني"
            placeholder="اختر مركز أو أكثر..."
            cols="12"
            multiple
            :add="false"
            :hideDetails="true"
            @update:model-value="$emit('update:selectedSchoolId', $event)"
          />
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <auto-list
            :model-value="selectedSubjectId"
            name="Subject"
            :objects="subjectsObjects"
            label="المادة الدراسية"
            placeholder="تصفية حسب المادة..."
            cols="12"
            :add="false"
            :hideDetails="true"
            @update:model-value="$emit('update:selectedSubjectId', $event)"
          />
        </v-col>
      </template>

      <!-- التعليم الجامعي -->
      <template v-else-if="institutionType === 'university'">
        <v-col cols="12" sm="6" md="4">
          <auto-list
            :model-value="selectedSchoolId"
            name="College"
            :objects="schoolsObjects"
            label="الجامعة / الكلية"
            placeholder="اختر الجامعة أو الكلية..."
            cols="12"
            multiple
            :add="false"
            :hideDetails="true"
            @update:model-value="$emit('update:selectedSchoolId', $event)"
          />
        </v-col>

        <v-col cols="12" sm="6" md="5">
          <auto-list
            :model-value="selectedSubjectId"
            name="Subject"
            :objects="subjectsObjects"
            label="المادة الدراسية"
            placeholder="تصفية حسب المادة..."
            cols="12"
            :add="false"
            :hideDetails="true"
            @update:model-value="$emit('update:selectedSubjectId', $event)"
          />
        </v-col>
      </template>

      <!-- التعليم الفني والمهني (معاهد) -->
      <template v-else-if="institutionType === 'institute'">
        <v-col cols="12" sm="6" md="4">
          <auto-list
            :model-value="selectedSchoolId"
            name="Institute"
            :objects="schoolsObjects"
            label="المعهد التقني / المهني"
            placeholder="اختر المعهد..."
            cols="12"
            multiple
            :add="false"
            :hideDetails="true"
            @update:model-value="$emit('update:selectedSchoolId', $event)"
          />
        </v-col>

        <v-col cols="12" sm="6" md="5">
          <auto-list
            :model-value="selectedSubjectId"
            name="Subject"
            :objects="subjectsObjects"
            label="المادة الدراسية"
            placeholder="تصفية حسب المادة..."
            cols="12"
            :add="false"
            :hideDetails="true"
            @update:model-value="$emit('update:selectedSubjectId', $event)"
          />
        </v-col>
      </template>

      <!-- أزرار الإجراءات -->
      <v-col cols="12" class="d-flex align-center justify-end gap-2 mb-3">
        <custom-btn
          type="show"
          label="تصفية النتائج"
          color="primary"
          icon="mdi-filter"
          class="font-weight-bold px-5"
          :loading="loadingMaster"
          :click="() => $emit('refresh')"
        />
        <custom-btn
          type="cancel_filter"
          :click="() => $emit('reset')"
          variant="tonal"
          color="error"
          label="تفريغ الفلاتر"
          icon="mdi-filter-off"
          class="font-weight-bold"
        />
      </v-col>
    </v-row>
  </filter-fields>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  institutionType: string
  sectorOptions: any[]
  selectedOfficeId: any
  selectedDirectorateId: any
  selectedSchoolId: any
  selectedSubjectId: any
  allOfficesList: any[]
  officesList: any[]
  directoratesOptions: any[]
  schoolsOptions: any[]
  subjectsList: any[]
  loadingMaster: boolean
}>()

defineEmits<{
  (e: 'update:institutionType', val: string): void
  (e: 'update:selectedOfficeId', val: any): void
  (e: 'update:selectedDirectorateId', val: any): void
  (e: 'update:selectedSchoolId', val: any): void
  (e: 'update:selectedSubjectId', val: any): void
  (e: 'refresh'): void
  (e: 'reset'): void
}>()

const sectorOptionsObjects = computed(() => {
  return (props.sectorOptions || []).map(opt => ({
    id: opt.value,
    value: opt.value,
    name: opt.title,
    name_ar: opt.title,
    title: opt.title,
  }))
})

const officesObjects = computed(() => {
  const list = props.allOfficesList && props.allOfficesList.length ? props.allOfficesList : (props.officesList || [])
  return list.map(o => ({
    id: o.id,
    value: o.id,
    name: o.office_name || o.name_ar || o.name,
    name_ar: o.office_name || o.name_ar || o.name,
    title: o.office_name || o.name_ar || o.name,
  }))
})

const directoratesObjects = computed(() => {
  return (props.directoratesOptions || []).map(d => ({
    id: d.id,
    value: d.id,
    name: d.name || d.name_ar,
    name_ar: d.name || d.name_ar,
    title: d.name || d.name_ar,
  }))
})

const schoolsObjects = computed(() => {
  return (props.schoolsOptions || []).map(s => ({
    id: s.id,
    value: s.id,
    name: s.name || s.school_name || s.name_ar,
    name_ar: s.name || s.school_name || s.name_ar,
    title: s.name || s.school_name || s.name_ar,
  }))
})

const subjectsObjects = computed(() => {
  return (props.subjectsList || []).map(s => ({
    id: s.id,
    value: s.id,
    name: s.name || s.name_ar,
    name_ar: s.name || s.name_ar,
    title: s.name || s.name_ar,
  }))
})
</script>
