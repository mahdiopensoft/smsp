<template>
  <div class="qb-omr-print-registry pa-4 pa-md-6">
    <!-- ── Page Header (Institutional OpenSoftCore Style) ─────────────── -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center">
        <back-to class="me-3" />
        <v-avatar size="48" color="secondary" variant="tonal" class="me-3 rounded-xl elevation-1">
          <v-icon size="26">mdi-printer-check</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">سجل الطباعة وتصدير الأوراق (OMR)</h1>
          <p class="text-caption text-medium-emphasis mb-0">
            تتبع ومعاينة حزم أوراق التظليل التي تم إخراجها للطباعة لكل مركز امتحاني واختبار
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
          @click="fetchBatches"
        >
          تحديث السجل
        </v-btn>
      </div>
    </div>

    <!-- Unified Filter Fields -->
    <filter-fields label="خيارات التصفية للبحث في سجلات الطباعة" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Search Query Input -->
        <v-col cols="12" sm="8" md="9">
          <v-text-field
            v-model="searchQuery"
            label="اسم الاختبار أو دفعة الطباعة"
            placeholder="بحث بمعرف الدفعة (Batch) أو اسم الاختبار..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @keyup.enter="fetchBatches"
          />
        </v-col>

        <!-- Actions -->
        <v-col cols="12" sm="4" md="3" class="d-flex align-center gap-2">
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ"
            class="font-weight-bold mb-6"
          />
          <custom-btn
            type="show"
            label="تحديث"
            color="primary"
            class="font-weight-bold flex-grow-1 mb-6"
            :click="fetchBatches"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Unified Custom Data Table for Batches -->
    <div class="main-card rounded-2xl overflow-hidden mb-6">
      <custom-data-table
        v-bind="{
          items: tableItems,
          headers,
          loading,
        }"
        :actions="false"
        :hasFilter="false"
        :log="false"
        :restore="false"
      >
        <template v-slot:item-slot="{ item, key }">
          
          <template v-if="key === 'batch_info'">
            <div class="d-flex align-center py-2">
              <v-avatar color="secondary" variant="tonal" size="38" class="me-3 rounded-lg">
                <v-icon size="20">mdi-folder-printer</v-icon>
              </v-avatar>
              <div>
                <div class="font-weight-black text-body-2 font-mono text-on-surface">{{ item.batch_id }}</div>
                <div class="text-caption text-medium-emphasis mt-1">
                  {{ item.print_date }}
                </div>
              </div>
            </div>
          </template>

          <template v-else-if="key === 'exam_info'">
            <div class="font-weight-bold text-body-2">{{ item.exam_title }}</div>
          </template>

          <template v-else-if="key === 'papers_count'">
            <v-chip
              color="primary"
              variant="tonal"
              size="small"
              class="font-weight-bold unified-table-chip"
              prepend-icon="mdi-file-document-multiple"
            >
              {{ item.total_papers }} ورقة
            </v-chip>
          </template>

          <template v-else-if="key === 'status'">
            <v-chip
              color="success"
              variant="flat"
              size="small"
              class="font-weight-bold unified-table-chip"
              prepend-icon="mdi-check-all"
            >
              {{ item.status }}
            </v-chip>
          </template>

          <!-- Actions -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-1">
              <custom-btn
                is-icon
                icon="eye"
                color="primary"
                variant="tonal"
                label="استعراض الأوراق المطبوعة للدفعة"
                :click="() => viewBatchDetails(item)"
              />
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>

    <!-- DIALOG: Batch Details -->
    <v-dialog v-model="detailsDialog" max-width="900px" scrollable>
      <v-card class="rounded-2xl" elevation="4">
        <v-card-title class="pa-4 pa-md-5 border-b d-flex align-center justify-space-between bg-surface">
          <div class="d-flex align-center">
            <v-avatar color="secondary" variant="tonal" size="44" class="me-3 rounded-xl">
              <v-icon size="24">mdi-file-document-check</v-icon>
            </v-avatar>
            <div>
              <div class="text-h6 font-weight-black mb-0">تفاصيل الدفعة المطبوعة</div>
              <div class="text-caption text-medium-emphasis font-mono">
                {{ activeBatch?.batch_id }} - {{ activeBatch?.exam_title }}
              </div>
            </div>
          </div>
          <v-btn
            icon="mdi-close"
            variant="text"
            size="small"
            density="comfortable"
            color="medium-emphasis"
            @click="detailsDialog = false"
          />
        </v-card-title>
        
        <v-card-text class="pa-0 bg-grey-lighten-5">
          <div v-if="loadingDetails" class="text-center py-12">
            <v-progress-circular indeterminate color="primary" size="44" class="mb-3" />
            <p class="text-body-2 font-weight-bold">جاري تحميل قائمة الطلاب...</p>
          </div>
          <div v-else>
            <custom-data-table
              v-bind="{
                items: studentsTableItems,
                headers: studentsHeaders,
              }"
              :hasFilter="false"
              :log="false"
              :restore="false"
              :actions="false"
            >
              <template v-slot:item-slot="{ item, key }">
                <template v-if="key === 'seat_number'">
                  <span class="font-weight-bold font-mono">{{ item.seat_number }}</span>
                </template>
                <template v-else-if="key === 'model_code'">
                  <v-chip size="x-small" variant="tonal" color="primary" class="font-weight-bold">
                    {{ item.model_code }}
                  </v-chip>
                </template>
                <template v-else-if="key === 'printed_at'">
                  <span class="text-caption text-medium-emphasis">{{ item.printed_at }}</span>
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
import { useRoute } from 'vue-router'
import api from '@/services/omr/client.js'

export default {
  name: 'OMRPrintRegistryView',
  setup() {
    const route = useRoute()
    const loading = ref(false)
    const searchQuery = ref('')
    const batches = ref([])

    const detailsDialog = ref(false)
    const activeBatch = ref(null)
    const loadingDetails = ref(false)
    const batchStudents = ref([])

    const headers = computed(() => [
      { title: "معرف الدفعة (Batch)", key: "batch_info", sortable: true },
      { title: "الاختبار", key: "exam_info", sortable: true },
      { title: "الأوراق المطبوعة", key: "papers_count", sortable: true, align: "center", width: "160px" },
      { title: "الحالة", key: "status", sortable: true, align: "center", width: "120px" },
      { title: "استعراض الأوراق", key: "actions", sortable: false, align: "center", width: "140px" },
    ])

    const tableItems = computed(() => {
      return {
        results: batches.value,
        count: batches.value.length,
        pagination: { count: batches.value.length, total: batches.value.length }
      }
    })

    const studentsHeaders = computed(() => [
      { title: "رقم الجلوس", key: "seat_number", sortable: true, align: "center" },
      { title: "اسم الطالب", key: "student_name", sortable: true },
      { title: "النموذج", key: "model_code", sortable: true, align: "center" },
      { title: "وقت الطباعة الفعلي", key: "printed_at", sortable: true, align: "center" },
    ])

    const studentsTableItems = computed(() => ({
      results: batchStudents.value,
      count: batchStudents.value.length,
      pagination: { count: batchStudents.value.length, total: batchStudents.value.length }
    }))

    const fetchBatches = async () => {
      loading.value = true
      try {
        const resp = await api.get('/api/omr/print-registry/', {
          params: { search: searchQuery.value }
        })
        if (resp.data && resp.data.success) {
          batches.value = resp.data.results
        }
      } catch (e) {
        console.error("Failed to load print batches", e)
      } finally {
        loading.value = false
      }
    }

    const resetFilters = () => {
      searchQuery.value = ''
      fetchBatches()
    }

    const viewBatchDetails = async (batch) => {
      activeBatch.value = batch
      detailsDialog.value = true
      loadingDetails.value = true
      batchStudents.value = []
      
      try {
        const resp = await api.get(`/api/omr/print-registry/${batch.batch_id}/`)
        if (resp.data && resp.data.success) {
          batchStudents.value = resp.data.students
        }
      } catch (e) {
        console.error("Failed to load batch students", e)
      } finally {
        loadingDetails.value = false
      }
    }

    onMounted(() => {
      if (route.query.exam_id) {
        searchQuery.value = String(route.query.exam_id)
      }
      fetchBatches()
    })

    return {
      loading,
      searchQuery,
      headers,
      tableItems,
      fetchBatches,
      resetFilters,
      detailsDialog,
      activeBatch,
      loadingDetails,
      studentsHeaders,
      studentsTableItems,
      viewBatchDetails
    }
  }
}
</script>

<style scoped>
.font-mono {
  font-family: monospace, monospace;
}
.unified-table-chip {
  border-radius: 6px !important;
  font-weight: 700 !important;
}
</style>
