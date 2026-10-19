<template>
  <div class="qb-omr-verification pa-4 pa-md-6">
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center">
        <v-avatar size="48" color="error" variant="tonal" class="me-3 rounded-xl elevation-1">
          <v-icon size="26">mdi-shield-check</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">المطابقة والتحقق من الأوراق المفقودة</h1>
          <p class="text-caption text-medium-emphasis mb-0">
            مقارنة سجل الطباعة مع الأوراق الممسوحة ضوئياً لاكتشاف حالات الفقد قبل الترحيل النهائي
          </p>
        </div>
      </div>
      <div class="d-flex align-center gap-2 flex-wrap">
        <v-btn
          color="primary"
          variant="flat"
          rounded="lg"
          class="font-weight-bold shadow-sm"
          prepend-icon="mdi-refresh"
          :loading="loading"
          @click="fetchVerificationStats"
        >
          تحديث المطابقة
        </v-btn>
      </div>
    </div>

    <!-- Unified Filter Fields (Standard Tripartite Institution Filters: Schools, Universities, Institutes) -->
    <filter-fields label="خيارات تصفية المطابقة والتحقق" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Institution Type Selector (مدارس / جامعات / معاهد / الكل) موحد كـ auto-list -->
        <auto-list
          v-model="filterInstitutionType"
          name="InstitutionType"
          placeholder="نوع المؤسسة التعليمية"
          cols="3"
          :add="false"
          @update:model-value="onInstitutionTypeChange"
        />

        <!-- 🏫 School Filters -->
        <template v-if="filterInstitutionType === 'school'">
          <auto-list
            v-model="filterStage"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="3"
            :add="false"
            @update:model-value="onStageChange"
          />
          <auto-list
            v-model="filterClassTrack"
            name="ClassTrackByStage"
            :param="filterStage"
            placeholder="الصف والمسار"
            cols="3"
            :add="false"
            :disabled="!filterStage"
            @update:model-value="fetchVerificationStats"
          />
          <auto-list
            v-model="filterSubject"
            name="Subject"
            :param="subjectFilterParam"
            placeholder="المادة الدراسية"
            cols="3"
            :add="false"
            @update:model-value="fetchVerificationStats"
          />
        </template>

        <!-- 🎓 University Filters -->
        <template v-if="filterInstitutionType === 'university'">
          <auto-list
            v-model="filterCollege"
            name="College"
            placeholder="الكلية الجامعية"
            cols="3"
            :add="false"
            @update:model-value="onCollegeChange"
          />
          <auto-list
            v-model="filterDepartment"
            name="DepartmentByCollege"
            :param="filterCollege"
            placeholder="القسم الأكاديمي"
            cols="3"
            :add="false"
            :disabled="!filterCollege"
            @update:model-value="onDepartmentChange"
          />
          <auto-list
            v-model="filterSpecialization"
            name="Specialization"
            :param="filterDepartment"
            placeholder="التخصص والبرنامج"
            cols="3"
            :add="false"
            :disabled="!filterDepartment"
            @update:model-value="fetchVerificationStats"
          />
          <auto-list
            v-model="filterSemesterSubject"
            name="SemesterSubject"
            :param="filterSpecialization"
            placeholder="مقرر الفصل الجامعي"
            cols="3"
            :add="false"
            @update:model-value="fetchVerificationStats"
          />
        </template>

        <!-- 🏢 Institute Filters -->
        <template v-if="filterInstitutionType === 'institute'">
          <auto-list
            v-model="filterInstituteField"
            name="InstituteField"
            placeholder="المجال المهني / التقني"
            cols="3"
            :add="false"
            @update:model-value="onInstituteFieldChange"
          />
          <auto-list
            v-model="filterInstituteEducationSystem"
            name="InstituteEducationSystem"
            :param="filterInstituteField"
            placeholder="نظام التعليم والتدريب"
            cols="3"
            :add="false"
            :disabled="!filterInstituteField"
            @update:model-value="onInstituteEducationSystemChange"
          />
          <auto-list
            v-model="filterInstituteSpecialization"
            name="InstituteSpecialization"
            :param="instituteSpecParam"
            placeholder="التخصص المهني"
            cols="3"
            :add="false"
            :disabled="!filterInstituteEducationSystem"
            @update:model-value="fetchVerificationStats"
          />
          <auto-list
            v-model="filterInstituteSubject"
            name="InstituteSubject"
            :param="instituteSubjectParam"
            placeholder="المادة الدراسية للمعهد"
            cols="3"
            :add="false"
            @update:model-value="fetchVerificationStats"
          />
        </template>

        <!-- Common Subject Filter (All / Fallback) -->
        <auto-list
          v-if="!filterInstitutionType || filterInstitutionType === 'all'"
          v-model="filterSubject"
          name="Subject"
          placeholder="المادة الدراسية (عام)"
          cols="3"
          :add="false"
          @update:model-value="fetchVerificationStats"
        />

        <!-- Search Query Input -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="searchQuery"
            label="اسم الاختبار أو رمزه"
            placeholder="ابحث باسم الاختبار..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @keyup.enter="fetchVerificationStats"
          />
        </v-col>

        <!-- Actions -->
        <v-col cols="12" sm="6" md="3" class="d-flex align-center gap-2">
          <custom-btn
            type="show"
            label="تحديث"
            color="primary"
            class="font-weight-bold flex-grow-1 mb-6"
            :click="fetchVerificationStats"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ"
            class="font-weight-bold mb-6"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Custom Data Table -->
    <div class="main-card rounded-2xl overflow-hidden mb-6">
      <custom-data-table
        v-bind="{ items: tableItems, headers, loading }"
        :actions="false"
        :hasFilter="false"
        :log="false"
        :restore="false"
      >
        <template v-slot:item-slot="{ item, key }">
          <template v-if="key === 'exam_info'">
            <div class="font-weight-bold text-body-2">{{ item.title }}</div>
            <div class="text-caption text-medium-emphasis font-mono">{{ item.uniqueCode }}</div>
          </template>

          <template v-else-if="key === 'total_printed'">
            <v-chip color="secondary" variant="tonal" size="small" class="font-weight-bold unified-table-chip">
              {{ item.total_printed }} ورقة مطبوعة
            </v-chip>
          </template>

          <template v-else-if="key === 'total_scanned'">
            <v-chip color="primary" variant="tonal" size="small" class="font-weight-bold unified-table-chip">
              {{ item.total_scanned }} ورقة ممسوحة
            </v-chip>
          </template>

          <template v-else-if="key === 'missing_count'">
            <v-chip :color="item.missing_count > 0 ? 'error' : 'success'" variant="flat" size="small" class="font-weight-bold unified-table-chip">
              {{ item.missing_count }} مفقودة
            </v-chip>
          </template>

          <template v-else-if="key === 'status'">
            <div :class="item.missing_count > 0 ? 'text-error' : 'text-success'" class="font-weight-bold text-caption">
              <v-icon size="16" class="me-1">{{ item.missing_count > 0 ? 'mdi-alert-circle' : 'mdi-check-circle' }}</v-icon>
              {{ item.status }}
            </div>
          </template>

          <template v-else-if="key === 'actions'">
            <custom-btn
              is-icon
              icon="eye"
              color="primary"
              variant="tonal"
              label="تفاصيل المطابقة للطلاب"
              :click="() => viewExamDetails(item)"
            />
          </template>
        </template>
      </custom-data-table>
    </div>

    <!-- DIALOG: Exam Verification Details -->
    <v-dialog v-model="detailsDialog" max-width="1000px" scrollable>
      <v-card class="rounded-2xl" elevation="4">
        <v-card-title class="pa-4 pa-md-5 border-b d-flex align-center justify-space-between bg-surface">
          <div class="d-flex align-center">
            <v-avatar color="error" variant="tonal" size="44" class="me-3 rounded-xl">
              <v-icon size="24">mdi-file-find</v-icon>
            </v-avatar>
            <div>
              <div class="text-h6 font-weight-black mb-0">تفاصيل وحالات الطلاب</div>
              <div class="text-caption text-medium-emphasis">
                {{ activeExam?.title }}
              </div>
            </div>
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" color="medium-emphasis" @click="detailsDialog = false" />
        </v-card-title>
        
        <v-card-text class="pa-0 bg-grey-lighten-5">
          <div v-if="loadingDetails" class="text-center py-12">
            <v-progress-circular indeterminate color="primary" size="44" class="mb-3" />
            <p class="text-body-2 font-weight-bold">جاري مقارنة السجلات...</p>
          </div>
          <div v-else>
            <div class="pa-4 bg-white border-b">
              <!-- Filter by status inside the dialog -->
              <v-btn-toggle v-model="statusFilter" mandatory color="primary" variant="outlined" density="compact" rounded="lg">
                <v-btn value="all" class="font-weight-bold">الكل ({{ examStudents.length }})</v-btn>
                <v-btn value="missing" color="error" class="font-weight-bold">مفقودة ({{ examStudents.filter(s => s.status === 'مفقودة').length }})</v-btn>
                <v-btn value="scanned" color="success" class="font-weight-bold">ممسوحة ({{ examStudents.filter(s => s.has_scanned).length }})</v-btn>
              </v-btn-toggle>
            </div>
            <custom-data-table
              v-bind="{ items: filteredStudentsTableItems, headers: studentsHeaders }"
              :hasFilter="false" :log="false" :restore="false" :actions="false"
            >
              <template v-slot:item-slot="{ item, key }">
                <template v-if="key === 'seat_number'">
                  <span class="font-weight-bold font-mono">{{ item.seat_number }}</span>
                </template>
                <template v-else-if="key === 'status'">
                  <v-chip
                    :color="item.status === 'مفقودة' ? 'error' : (item.has_scanned ? 'success' : 'grey')"
                    variant="tonal"
                    size="small"
                    class="font-weight-bold unified-table-chip"
                  >
                    {{ item.status }}
                  </v-chip>
                </template>
              </template>
            </custom-data-table>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/omr/client.js'

export default {
  name: 'OMRVerificationView',
  setup() {
    const loading = ref(false)
    const searchQuery = ref('')
    const examsStats = ref([])

    // Filters
    const filterInstitutionType = ref('all')
    const filterStage = ref(null)
    const filterClassTrack = ref(null)
    const filterSubject = ref(null)

    const filterCollege = ref(null)
    const filterDepartment = ref(null)
    const filterSpecialization = ref(null)
    const filterSemesterSubject = ref(null)

    const filterInstituteField = ref(null)
    const filterInstituteEducationSystem = ref(null)
    const filterInstituteSpecialization = ref(null)
    const filterInstituteSubject = ref(null)

    const institutionTypeOptions = [
      { text: 'الكل (مدارس وجامعات ومعاهد)', value: 'all', icon: 'mdi-domain' },
      { text: 'تعليم مدرسي', value: 'school', icon: 'mdi-school' },
      { text: 'تعليم جامعي', value: 'university', icon: 'mdi-domain' },
      { text: 'معاهد وتدريب مهني', value: 'institute', icon: 'mdi-tools' },
    ]

    const subjectFilterParam = computed(() => {
      const p = {}
      if (filterClassTrack.value) p.class_track = filterClassTrack.value
      if (filterStage.value) p.stage = filterStage.value
      return Object.keys(p).length > 0 ? p : null
    })

    const instituteSpecParam = computed(() => {
      const p = {}
      if (filterInstituteField.value) p.field = filterInstituteField.value
      if (filterInstituteEducationSystem.value) p.education_system = filterInstituteEducationSystem.value
      return Object.keys(p).length ? p : null
    })

    const instituteSubjectParam = computed(() => {
      if (filterInstituteField.value) return { field: filterInstituteField.value }
      return null
    })

    const onInstitutionTypeChange = () => {
      filterStage.value = null
      filterClassTrack.value = null
      filterSubject.value = null
      filterCollege.value = null
      filterDepartment.value = null
      filterSpecialization.value = null
      filterSemesterSubject.value = null
      filterInstituteField.value = null
      filterInstituteEducationSystem.value = null
      filterInstituteSpecialization.value = null
      filterInstituteSubject.value = null
      fetchVerificationStats()
    }

    const onStageChange = () => {
      filterClassTrack.value = null
      filterSubject.value = null
      fetchVerificationStats()
    }

    const onCollegeChange = () => {
      filterDepartment.value = null
      filterSpecialization.value = null
      filterSemesterSubject.value = null
      fetchVerificationStats()
    }

    const onDepartmentChange = () => {
      filterSpecialization.value = null
      filterSemesterSubject.value = null
      fetchVerificationStats()
    }

    const onInstituteFieldChange = () => {
      filterInstituteEducationSystem.value = null
      filterInstituteSpecialization.value = null
      filterInstituteSubject.value = null
      fetchVerificationStats()
    }

    const onInstituteEducationSystemChange = () => {
      filterInstituteSpecialization.value = null
      fetchVerificationStats()
    }

    const detailsDialog = ref(false)
    const activeExam = ref(null)
    const loadingDetails = ref(false)
    const examStudents = ref([])
    const statusFilter = ref('all')

    const headers = computed(() => [
      { title: "الاختبار", key: "exam_info", sortable: true },
      { title: "الأوراق المطبوعة", key: "total_printed", sortable: true, align: "center", width: "160px" },
      { title: "الأوراق الممسوحة", key: "total_scanned", sortable: true, align: "center", width: "160px" },
      { title: "الناقص والمفقود", key: "missing_count", sortable: true, align: "center", width: "140px" },
      { title: "حالة المطابقة", key: "status", sortable: true, align: "center", width: "140px" },
      { title: "التفاصيل", key: "actions", sortable: false, align: "center", width: "100px" },
    ])

    const tableItems = computed(() => ({
      results: examsStats.value,
      count: examsStats.value.length,
      pagination: { count: examsStats.value.length, total: examsStats.value.length }
    }))

    const studentsHeaders = computed(() => [
      { title: "رقم الجلوس", key: "seat_number", sortable: true, align: "center", width: "120px" },
      { title: "اسم الطالب", key: "student_name", sortable: true },
      { title: "النموذج", key: "model_code", sortable: true, align: "center", width: "100px" },
      { title: "حالة الورقة (التتبع)", key: "status", sortable: true, align: "center", width: "160px" },
    ])

    const filteredStudents = computed(() => {
      if (statusFilter.value === 'missing') return examStudents.value.filter(s => s.status === 'مفقودة')
      if (statusFilter.value === 'scanned') return examStudents.value.filter(s => s.has_scanned)
      return examStudents.value
    })

    const filteredStudentsTableItems = computed(() => ({
      results: filteredStudents.value,
      count: filteredStudents.value.length,
      pagination: { count: filteredStudents.value.length, total: filteredStudents.value.length }
    }))

    const fetchVerificationStats = async () => {
      loading.value = true
      try {
        const params = {}
        if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
          params.institution_type = filterInstitutionType.value
        }
        if (searchQuery.value && searchQuery.value.trim()) {
          params.search = searchQuery.value.trim()
        }
        if (filterInstitutionType.value === 'school') {
          if (filterStage.value) params.stage = filterStage.value
          if (filterClassTrack.value) params.class_track = filterClassTrack.value
          if (filterSubject.value) params.subject = filterSubject.value
        } else if (filterInstitutionType.value === 'university') {
          if (filterCollege.value) params.college = filterCollege.value
          if (filterDepartment.value) params.department = filterDepartment.value
          if (filterSpecialization.value) params.specialization = filterSpecialization.value
          if (filterSemesterSubject.value) params.semester_subject = filterSemesterSubject.value
        } else if (filterInstitutionType.value === 'institute') {
          if (filterInstituteField.value) params.institute_field = filterInstituteField.value
          if (filterInstituteEducationSystem.value) params.institute_education_system = filterInstituteEducationSystem.value
          if (filterInstituteSpecialization.value) params.institute_specialization = filterInstituteSpecialization.value
          if (filterInstituteSubject.value) params.institute_subject = filterInstituteSubject.value
        } else {
          if (filterSubject.value) params.subject = filterSubject.value
        }

        const resp = await api.get('/api/omr/verification/', { params })
        if (resp.data && resp.data.success) {
          examsStats.value = resp.data.results
        }
      } catch (e) {
        console.error("Failed to load verification stats", e)
      } finally {
        loading.value = false
      }
    }

    const resetFilters = () => {
      searchQuery.value = ''
      filterInstitutionType.value = 'all'
      filterStage.value = null
      filterClassTrack.value = null
      filterSubject.value = null
      filterCollege.value = null
      filterDepartment.value = null
      filterSpecialization.value = null
      filterSemesterSubject.value = null
      filterInstituteField.value = null
      filterInstituteEducationSystem.value = null
      filterInstituteSpecialization.value = null
      filterInstituteSubject.value = null
      fetchVerificationStats()
    }

    const viewExamDetails = async (exam) => {
      activeExam.value = exam
      detailsDialog.value = true
      loadingDetails.value = true
      examStudents.value = []
      statusFilter.value = 'all'
      
      try {
        const resp = await api.get(`/api/omr/verification/${exam.id}/`)
        if (resp.data && resp.data.success) {
          examStudents.value = resp.data.students
        }
      } catch (e) {
        console.error("Failed to load verification details", e)
      } finally {
        loadingDetails.value = false
      }
    }

    onMounted(() => {
      fetchVerificationStats()
    })

    return {
      loading, searchQuery, headers, tableItems, fetchVerificationStats, resetFilters,
      filterInstitutionType, institutionTypeOptions,
      filterStage, filterClassTrack, filterSubject, subjectFilterParam,
      filterCollege, filterDepartment, filterSpecialization, filterSemesterSubject,
      filterInstituteField, filterInstituteEducationSystem, filterInstituteSpecialization, filterInstituteSubject,
      instituteSpecParam, instituteSubjectParam,
      onInstitutionTypeChange, onStageChange, onCollegeChange, onDepartmentChange,
      onInstituteFieldChange, onInstituteEducationSystemChange,
      detailsDialog, activeExam, loadingDetails, studentsHeaders, filteredStudentsTableItems,
      viewExamDetails, examStudents, statusFilter
    }
  }
}
</script>

<style scoped>
.font-mono { font-family: monospace, monospace; }
.unified-table-chip { border-radius: 6px !important; font-weight: 700 !important; }
</style>
