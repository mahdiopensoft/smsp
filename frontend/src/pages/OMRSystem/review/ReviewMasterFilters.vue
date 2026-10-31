<template>
  <filter-fields label="خيارات التصفية الأكاديمية والهرمية لمراجعة وتدقيق أوراق الإجابة" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
    <v-row dense class="align-center">
      <!-- 1. نوع المؤسسة التعليمية -->
      <v-col cols="12" sm="6" :md="institutionType === 'school' ? 2 : 3">
        <v-select
          :model-value="institutionType"
          :items="sectorOptions"
          item-title="title"
          item-value="value"
          label="نوع المؤسسة التعليمية"
          density="compact"
          variant="outlined"
          rounded="lg"
          hide-details
          class="mb-3"
          :prepend-inner-icon="institutionType === 'university' ? 'mdi-domain' : (institutionType === 'institute' ? 'mdi-tools' : 'mdi-school')"
          @update:model-value="$emit('update:institutionType', $event)"
        >
          <template #item="{ props: itemProps, item }">
            <v-list-item v-bind="itemProps" :prepend-icon="item.raw?.icon" />
          </template>
        </v-select>
      </v-col>

      <!-- التعليم العام (مدرسي) -->
      <template v-if="institutionType === 'school'">
        <v-col cols="12" sm="6" md="2">
          <v-autocomplete
            :model-value="selectedOfficeId"
            :items="allOfficesList && allOfficesList.length ? allOfficesList : officesList"
            item-title="office_name"
            item-value="id"
            label="مكتب التربية (المحافظة)"
            placeholder="اختر مكتب أو أكثر..."
            clearable
            multiple
            chips
            closable-chips
            density="compact"
            variant="outlined"
            rounded="lg"
            hide-details
            class="mb-3"
            prepend-inner-icon="mdi-office-building-outline"
            @update:model-value="$emit('update:selectedOfficeId', $event)"
          />
        </v-col>

        <v-col cols="12" sm="6" md="2">
          <v-autocomplete
            :model-value="selectedDirectorateId"
            :items="directoratesOptions"
            item-title="name"
            item-value="id"
            label="إدارة التربية (المديرية)"
            placeholder="اختر مديرية أو أكثر..."
            clearable
            multiple
            chips
            closable-chips
            density="compact"
            variant="outlined"
            rounded="lg"
            hide-details
            class="mb-3"
            prepend-inner-icon="mdi-map-marker-radius-outline"
            @update:model-value="$emit('update:selectedDirectorateId', $event)"
          />
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <v-autocomplete
            :model-value="selectedSchoolId"
            :items="schoolsOptions"
            item-title="name"
            item-value="id"
            label="المدرسة / المركز الامتحاني"
            placeholder="اختر مركز أو أكثر..."
            clearable
            multiple
            chips
            closable-chips
            density="compact"
            variant="outlined"
            rounded="lg"
            hide-details
            class="mb-3"
            prepend-inner-icon="mdi-school-outline"
            @update:model-value="$emit('update:selectedSchoolId', $event)"
          />
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <v-autocomplete
            :model-value="selectedSubjectId"
            :items="subjectsList"
            item-title="name"
            item-value="id"
            label="المادة الدراسية"
            placeholder="تصفية حسب المادة..."
            clearable
            density="compact"
            variant="outlined"
            rounded="lg"
            hide-details
            class="mb-3"
            prepend-inner-icon="mdi-book-education-outline"
            @update:model-value="$emit('update:selectedSubjectId', $event)"
          />
        </v-col>
      </template>

      <!-- التعليم الجامعي -->
      <template v-else-if="institutionType === 'university'">
        <v-col cols="12" sm="6" md="4">
          <v-autocomplete
            :model-value="selectedSchoolId"
            :items="schoolsOptions"
            item-title="name"
            item-value="id"
            label="الجامعة / الكلية"
            placeholder="اختر الجامعة أو الكلية..."
            clearable
            multiple
            chips
            closable-chips
            density="compact"
            variant="outlined"
            rounded="lg"
            hide-details
            class="mb-3"
            prepend-inner-icon="mdi-domain"
            @update:model-value="$emit('update:selectedSchoolId', $event)"
          />
        </v-col>

        <v-col cols="12" sm="6" md="5">
          <v-autocomplete
            :model-value="selectedSubjectId"
            :items="subjectsList"
            item-title="name"
            item-value="id"
            label="المادة الدراسية"
            placeholder="تصفية حسب المادة..."
            clearable
            density="compact"
            variant="outlined"
            rounded="lg"
            hide-details
            class="mb-3"
            prepend-inner-icon="mdi-book-education-outline"
            @update:model-value="$emit('update:selectedSubjectId', $event)"
          />
        </v-col>
      </template>

      <!-- التعليم الفني والمهني (معاهد) -->
      <template v-else-if="institutionType === 'institute'">
        <v-col cols="12" sm="6" md="4">
          <v-autocomplete
            :model-value="selectedSchoolId"
            :items="schoolsOptions"
            item-title="name"
            item-value="id"
            label="المعهد التقني / المهني"
            placeholder="اختر المعهد..."
            clearable
            multiple
            chips
            closable-chips
            density="compact"
            variant="outlined"
            rounded="lg"
            hide-details
            class="mb-3"
            prepend-inner-icon="mdi-tools"
            @update:model-value="$emit('update:selectedSchoolId', $event)"
          />
        </v-col>

        <v-col cols="12" sm="6" md="5">
          <v-autocomplete
            :model-value="selectedSubjectId"
            :items="subjectsList"
            item-title="name"
            item-value="id"
            label="المادة الدراسية"
            placeholder="تصفية حسب المادة..."
            clearable
            density="compact"
            variant="outlined"
            rounded="lg"
            hide-details
            class="mb-3"
            prepend-inner-icon="mdi-book-education-outline"
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
defineProps<{
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
</script>
