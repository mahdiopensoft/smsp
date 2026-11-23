<template>
  <filter-fields label="خيارات التصفية الأكاديمية والبحث المتقدم في سجلات الطباعة والتوليد" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
    <v-row dense class="align-center">
      <!-- 1. نوع المؤسسة التعليمية -->
      <v-col cols="12" sm="6" md="3">
        <auto-list
          v-model="filters.filterInstitutionType.value"
          name="InstitutionType"
          placeholder="نوع المؤسسة التعليمية"
          label="نوع المؤسسة التعليمية"
          cols="12"
          :add="false"
          @update:model-value="filters.onInstitutionTypeChange"
        />
      </v-col>

      <!-- 2. حقل البحث الفوري الموحد -->
      <v-col cols="12" sm="6" md="3">
        <custom-text-field
          v-model="filters.masterSearchQuery.value"
          label="اسم الاختبار أو الرمز"
          placeholder="بحث باسم الاختبار، الرمز (Code)..."
          icon="magnify"
          cols="12"
          class="mb-3"
        />
      </v-col>

      <!-- 3. المحافظة -->
      <v-col cols="12" sm="6" md="3">
        <auto-list
          v-model="filters.filterGovernorate.value"
          name="Governorate"
          placeholder="المحافظة"
          label="المحافظة"
          cols="12"
          :add="false"
          @update:model-value="filters.onGovernorateChange"
        />
      </v-col>

      <!-- 4. المديرية (تظهر للمدارس) -->
      <v-col v-if="filters.isSchoolFilter.value" cols="12" sm="6" md="3">
        <auto-list
          v-model="filters.filterDirectorate.value"
          name="Directorate"
          :param="filters.filterGovernorate.value"
          :placeholder="filters.filterGovernorate.value ? 'المديرية' : 'اختر المحافظة أولاً'"
          label="المديرية"
          cols="12"
          :add="false"
          :disabled="!filters.filterGovernorate.value"
          @update:model-value="filters.onDirectorateChange"
        />
      </v-col>

      <!-- 5. المركز الامتحاني / المدرسة -->
      <v-col cols="12" sm="6" :md="filters.isSchoolFilter.value ? 3 : 3">
        <auto-list
          v-model="filters.filterOrganization.value"
          name="Organization"
          :param="filters.orgParam.value"
          :placeholder="filters.orgPlaceholder.value"
          :label="filters.orgFieldLabel.value"
          cols="12"
          :add="false"
          :disabled="filters.isOrgDisabled.value"
          @update:model-value="filters.onOrganizationChange"
        />
      </v-col>

      <!-- 🏫 School Filters (المرحلة، الصف والمسار، المادة) -->
      <template v-if="filters.filterInstitutionType.value === 'school'">
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filters.filterStage.value"
            name="Stage"
            label="المرحلة الدراسية"
            placeholder="المرحلة الدراسية"
            cols="12"
            :add="false"
            @update:model-value="filters.onStageChange"
          />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filters.filterClassTrack.value"
            name="ClassTrackByStage"
            :param="filters.filterStage.value"
            label="الصف والمسار المدرسي"
            placeholder="الصف والمسار المدرسي"
            cols="12"
            :add="false"
            :disabled="!filters.filterStage.value"
            @update:model-value="filters.onClassTrackChange"
          />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filters.filterSubject.value"
            name="Subject"
            :param="filters.subjectFilterParam.value"
            label="المادة الدراسية"
            placeholder="المادة الدراسية"
            cols="12"
            :add="false"
            @update:model-value="$emit('apply')"
          />
        </v-col>
      </template>

      <!-- 🎓 University Filters (الكلية، القسم، التخصص، المقرر) -->
      <template v-if="filters.filterInstitutionType.value === 'university'">
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filters.filterCollege.value"
            name="College"
            label="الكلية الجامعية"
            placeholder="الكلية الجامعية"
            cols="12"
            :add="false"
            @update:model-value="filters.onCollegeChange"
          />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filters.filterDepartment.value"
            name="DepartmentByCollege"
            :param="filters.filterCollege.value"
            label="القسم الأكاديمي"
            placeholder="القسم الأكاديمي"
            cols="12"
            :add="false"
            :disabled="!filters.filterCollege.value"
            @update:model-value="filters.onDepartmentChange"
          />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filters.filterSpecialization.value"
            name="Specialization"
            :param="filters.filterDepartment.value"
            label="التخصص والبرنامج"
            placeholder="التخصص والبرنامج"
            cols="12"
            :add="false"
            :disabled="!filters.filterDepartment.value"
            @update:model-value="filters.onSpecializationChange"
          />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filters.filterSemesterSubject.value"
            name="SemesterSubject"
            :param="filters.filterSpecialization.value"
            label="مقرر الفصل الجامعي"
            placeholder="مقرر الفصل الجامعي"
            cols="12"
            :add="false"
            @update:model-value="$emit('apply')"
          />
        </v-col>
      </template>

      <!-- 🏢 Institute Filters (المجال المهني، نظام التعليم، التخصص، المادة) -->
      <template v-if="filters.filterInstitutionType.value === 'institute'">
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filters.filterInstituteField.value"
            name="InstituteField"
            label="المجال المهني / التقني"
            placeholder="المجال المهني / التقني"
            cols="12"
            :add="false"
            @update:model-value="filters.onInstituteFieldChange"
          />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filters.filterInstituteEducationSystem.value"
            name="InstituteEducationSystem"
            :param="filters.filterInstituteField.value"
            label="نظام التعليم والتدريب"
            placeholder="نظام التعليم والتدريب"
            cols="12"
            :add="false"
            :disabled="!filters.filterInstituteField.value"
            @update:model-value="filters.onInstituteEducationSystemChange"
          />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filters.filterInstituteSpecialization.value"
            name="InstituteSpecialization"
            :param="filters.instituteSpecParam.value"
            label="التخصص المهني"
            placeholder="التخصص المهني"
            cols="12"
            :add="false"
            :disabled="!filters.filterInstituteEducationSystem.value"
            @update:model-value="$emit('apply')"
          />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filters.filterInstituteSubject.value"
            name="InstituteSubject"
            :param="filters.instituteSubjectParam.value"
            label="المادة الدراسية للمعهد"
            placeholder="المادة الدراسية للمعهد"
            cols="12"
            :add="false"
            @update:model-value="$emit('apply')"
          />
        </v-col>
      </template>

      <!-- Fallback Subject if All / None selected -->
      <v-col v-if="!filters.filterInstitutionType.value || filters.filterInstitutionType.value === 'all'" cols="12" sm="6" md="3">
        <auto-list
          v-model="filters.filterSubject.value"
          name="Subject"
          placeholder="المادة الدراسية (عام)"
          label="المادة الدراسية (عام)"
          cols="12"
          :add="false"
          @update:model-value="$emit('apply')"
        />
      </v-col>

      <!-- أزرار الإجراءات -->
      <v-col cols="12" class="d-flex align-center justify-end gap-2 mb-3">
        <custom-btn
          type="show"
          label="تصفية النتائج"
          color="primary"
          icon="mdi-filter"
          class="font-weight-bold px-5"
          :loading="loading"
          :click="() => $emit('apply')"
        />
        <custom-btn
          type="cancel_filter"
          :click="() => filters.resetUnifiedFilters()"
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
defineProps<{
  filters: any
  loading?: boolean
}>()

defineEmits<{
  (e: 'apply'): void
}>()
</script>
