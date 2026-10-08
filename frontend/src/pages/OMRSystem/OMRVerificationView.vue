<template>
  <div class="qb-omr-verification pa-4 pa-md-6">
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center">
        <back-to class="me-3" />
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

    <!-- Unified Filter Fields -->
    <filter-fields label="خيارات تصفية المطابقة" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <v-col cols="12" sm="8" md="9">
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
        <v-col cols="12" sm="4" md="3" class="d-flex align-center gap-2">
          <custom-btn type="cancel_filter" :click="resetFilters" variant="tonal" color="error" label="تفريغ" class="font-weight-bold mb-6" />
          <custom-btn type="show" label="تحديث" color="primary" class="font-weight-bold flex-grow-1 mb-6" :click="fetchVerificationStats" />
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
        const resp = await api.get('/api/omr/verification/', { params: { search: searchQuery.value } })
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
