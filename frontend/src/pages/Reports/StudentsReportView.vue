<template>
  <div class="students-report-page">
    <filter-fields label="معايير التصفية والبحث في سجل الطلاب" class="mb-4">
      <template #fields>
        <!-- اختيار نوع المؤسسة التعليمية (مدارس / جامعات / معاهد) بدون خيار الكل -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterInstitutionType"
            :items="institutionTypeOptions"
            item-title="text"
            item-value="value"
            label="نوع المؤسسة التعليمية"
            placeholder="اختر نوع المؤسسة"
            prepend-inner-icon="mdi-domain"
            hide-details
            clearable
            density="compact"
            variant="outlined"
            @update:model-value="onInstitutionTypeChange"
          >
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :prepend-icon="item.raw.icon" />
            </template>
          </v-select>
        </v-col>

        <!-- فلاتر هرمية حسب النوع -->
        <template v-if="filterInstitutionType === 'school'">
          <auto-list
            v-model="filterStage"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="2"
            :add="false"
          />
        </template>

        <template v-if="filterInstitutionType === 'university'">
          <auto-list
            v-model="filterCollege"
            name="College"
            placeholder="الكلية الجامعية"
            cols="2"
            :add="false"
          />
        </template>

        <template v-if="filterInstitutionType === 'institute'">
          <auto-list
            v-model="filterInstituteField"
            name="InstituteField"
            placeholder="المجال المهني"
            cols="2"
            :add="false"
          />
        </template>

        <!-- فلاتر جغرافية عامة -->
        <auto-list
          v-model="filterGovernorate"
          name="Governorate"
          placeholder="المحافظة"
          cols="2"
          :add="false"
          @update:model-value="filterDirectorate = null"
        />

        <auto-list
          v-model="filterDirectorate"
          name="DirectorateByGovernorate"
          :param="filterGovernorate"
          placeholder="المديرية"
          cols="2"
          :add="false"
          :disabled="!filterGovernorate"
        />

        <v-col cols="12" md="3">
          <v-text-field
            v-model="filterSearch"
            placeholder="بحث باسم الطالب أو الرقم الأكاديمي..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            hide-details
          />
        </v-col>

        <v-col cols="auto" class="d-flex align-center gap-2 py-2">
          <custom-btn type="filter" :loading="loading" :click="applyFilters" />
          <custom-btn
            color="primary"
            variant="tonal"
            :click="resetFilters"
            label="إعادة ضبط"
            icon="mdi-refresh"
          />
        </v-col>
      </template>
    </filter-fields>

    <CustomCard elevation="0" class="rounded-xl overflow-hidden">
      <custom-data-table
        :items="items"
        :headers="headers"
        :loading="loading"
        :hasFilter="false"
        hover
      >
        <template #item.index="{ index }">{{ index + 1 }}</template>
        <template #item.gender="{ item }">
          <v-chip
            :color="item.gender === 'ذكر' ? 'info' : 'pink'"
            size="small"
            variant="tonal"
          >
            {{ item.gender }}
          </v-chip>
        </template>
      </custom-data-table>
    </CustomCard>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { reportsService } from '@/services/reportsService'

const loading = ref(false)
const items = ref([])

// خيارات نوع المؤسسة بدون "الكل"
const filterInstitutionType = ref(null)
const institutionTypeOptions = [
  { text: 'تعليم مدرسي', value: 'school', icon: 'mdi-school' },
  { text: 'تعليم جامعي', value: 'university', icon: 'mdi-domain' },
  { text: 'معاهد وتدريب مهني', value: 'institute', icon: 'mdi-tools' },
]

const filterStage = ref(null)
const filterCollege = ref(null)
const filterInstituteField = ref(null)
const filterGovernorate = ref(null)
const filterDirectorate = ref(null)
const filterSearch = ref('')

const onInstitutionTypeChange = () => {
  filterStage.value = null
  filterCollege.value = null
  filterInstituteField.value = null
  applyFilters()
}

const headers = [
  { title: '#', key: 'index', sortable: false, width: '60px' },
  { title: 'اسم الطالب', key: 'name', sortable: true },
  { title: 'الرقم الأكاديمي', key: 'academicNumber', sortable: true },
  { title: 'الجنس', key: 'gender', sortable: true, align: 'center' },
  { title: 'المؤسسة التعليمية', key: 'institution', sortable: true },
  { title: 'المرحلة / المستوى', key: 'levelStage', sortable: true },
  { title: 'المحافظة', key: 'governorate', sortable: true },
  { title: 'المديرية', key: 'directorate', sortable: true },
  { title: 'تاريخ التسجيل', key: 'createdAt', sortable: true },
]

const buildParams = () => {
  const p = {}
  if (filterInstitutionType.value) {
    p.institution_type = filterInstitutionType.value
  }
  if (filterStage.value) p.stage = filterStage.value
  if (filterCollege.value) p.college = filterCollege.value
  if (filterInstituteField.value) p.field = filterInstituteField.value
  if (filterGovernorate.value) p.governorate = filterGovernorate.value
  if (filterDirectorate.value) p.directorate = filterDirectorate.value
  if (filterSearch.value) p.search = filterSearch.value
  return p
}

const applyFilters = async () => {
  loading.value = true
  try {
    const res = await reportsService.getStudentsReport(buildParams())
    items.value = res.results || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filterInstitutionType.value = null
  filterStage.value = null
  filterCollege.value = null
  filterInstituteField.value = null
  filterGovernorate.value = null
  filterDirectorate.value = null
  filterSearch.value = ''
  applyFilters()
}

onMounted(applyFilters)
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
