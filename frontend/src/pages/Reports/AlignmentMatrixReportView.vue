<template>
  <div class="qb-alignment-matrix-page-v4">
    <!-- Header Controls -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div>
        <h2 class="text-h5 font-weight-black mb-1">مصفوفة المواءمة الأكاديمية (CLO Alignment Matrix)</h2>
        <span class="text-caption text-medium-emphasis">
          ربط مخرجات التعلم بالأسئلة المعتمدة والمستويات المعرفية (متطلبات الاعتماد الأكاديمي ABET / NCAAA)
        </span>
      </div>

      <div class="d-flex align-center gap-3">
        <custom-btn
          label="طباعة تقرير المواءمة"
          icon="mdi-printer"
          color="primary"
          variant="tonal"
          class="font-weight-bold px-5"
          :click="printReport"
        />
      </div>
    </div>

    <!-- Filters Control Bar (Theme Compatible) -->
    <filter-fields label="تحديد المقرر الدراسي والوحدة للتقرير (مدرسي / جامعي)" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Institution Type Filter -->
        <v-col cols="12" md="2">
          <v-select
            v-model="filterInstitutionType"
            :items="[
              { title: '🏫 الكل (مدارس وجامعات)', value: 'all' },
              { title: '🏫 التعليم المدرسي فقط', value: 'school' },
              { title: '🎓 التعليم الجامعي فقط', value: 'university' }
            ]"
            label="نوع المنشأة"
            variant="outlined"
            density="comfortable"
            hide-details
            rounded="lg"
            class="mb-6"
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

        <!-- School Filters -->
        <template v-if="filterInstitutionType !== 'university'">
          <!-- Stage Filter -->
          <auto-list
            v-model="filterStage"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="2"
            :add="false"
            @update:model-value="onStageChange"
          />

          <!-- ClassTrack Filter (الصف والمسار) -->
          <auto-list
            v-model="filterClassTrack"
            name="ClassTrackByStage"
            :param="filterStage"
            placeholder="الصف والمسار"
            cols="2"
            :add="false"
            :disabled="!filterStage"
          />

          <!-- Subject Filter -->
          <auto-list
            v-model="selectedSubjectId"
            name="Subject"
            placeholder="المادة الدراسية"
            cols="2"
            :add="false"
          />
        </template>

        <!-- University Filters -->
        <template v-if="filterInstitutionType !== 'school'">
          <auto-list
            v-model="filterCollege"
            name="College"
            placeholder="الكلية"
            :add="false"
            cols="2"
            @update:model-value="onCollegeChange"
          />

          <auto-list
            v-model="filterDepartment"
            name="DepartmentByCollege"
            :param="filterCollege"
            placeholder="القسم الأكاديمي"
            :add="false"
            cols="2"
            :disabled="!filterCollege"
          />

          <auto-list
            v-model="filterSpecialization"
            name="Specialization"
            placeholder="التخصص الجامعي"
            :add="false"
            cols="2"
          />

          <auto-list
            v-model="filterSemesterSubject"
            name="SemesterSubject"
            placeholder="المقرر الجامعي"
            :add="false"
            cols="2"
          />
        </template>

        <!-- Search Query -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="searchQuery"
            placeholder="بحث برمز أو وصف المخرج (CLO)..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Filter Actions -->
        <v-col cols="12" sm="6" md="3" class="d-flex align-center gap-2">
          <custom-btn
            type="show"
            label="تحديث التقرير"
            color="primary"
            class="font-weight-bold flex-grow-1 mb-6"
            :click="loadMatrixReport"
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

    <!-- Summary Metric Cards (Calculated directly on Backend) -->
    <v-row v-if="reportData" class="mb-6">
      <!-- Total CLOs -->
      <v-col cols="12" sm="6" md="3">
        <div class="stat-glass-card shadow-indigo pa-5 rounded-xl">
          <div class="d-flex align-center justify-space-between mb-3">
            <div class="stat-value text-h3 font-weight-black text-indigo">
              {{ reportData.total_clos || 0 }}
            </div>
            <div class="stat-icon-wrapper bg-indigo-gradient">
              <v-icon size="24" color="white">mdi-target</v-icon>
            </div>
          </div>
          <div class="stat-label text-subtitle-2 font-weight-bold text-medium-emphasis">
            إجمالي مخرجات التعلم (CLOs)
          </div>
          <div class="stat-footer mt-2 pt-2 border-t border-slate-100 text-caption text-medium-emphasis">
            المسجلة في هذا المقرر
          </div>
        </div>
      </v-col>

      <!-- Coverage Rate -->
      <v-col cols="12" sm="6" md="3">
        <div class="stat-glass-card shadow-emerald pa-5 rounded-xl">
          <div class="d-flex align-center justify-space-between mb-3">
            <div class="stat-value text-h3 font-weight-black text-emerald">
              {{ reportData.coverage_rate_percentage || 0 }}%
            </div>
            <div class="stat-icon-wrapper bg-emerald-gradient">
              <v-icon size="24" color="white">mdi-chart-arc</v-icon>
            </div>
          </div>
          <div class="stat-label text-subtitle-2 font-weight-bold text-medium-emphasis">
            نسبة تغطية المخرجات
          </div>
          <div class="stat-footer mt-2 pt-2 border-t border-slate-100 text-caption text-medium-emphasis">
            بأسئلة معتمدة جاهزة للاختبار
          </div>
        </div>
      </v-col>

      <!-- Uncovered CLOs (Gaps) -->
      <v-col cols="12" sm="6" md="3">
        <div class="stat-glass-card shadow-rose pa-5 rounded-xl">
          <div class="d-flex align-center justify-space-between mb-3">
            <div class="stat-value text-h3 font-weight-black text-rose">
              {{ reportData.uncovered_clos || 0 }}
            </div>
            <div class="stat-icon-wrapper bg-rose-gradient">
              <v-icon size="24" color="white">mdi-alert-octagon-outline</v-icon>
            </div>
          </div>
          <div class="stat-label text-subtitle-2 font-weight-bold text-medium-emphasis">
            مخرجات غير مغطاة (فجوات)
          </div>
          <div class="stat-footer mt-2 pt-2 border-t border-slate-100 text-caption text-medium-emphasis">
            <span class="text-rose font-weight-bold">تتطلب تأليف أسئلة فوراً</span>
          </div>
        </div>
      </v-col>

      <!-- Total Approved Questions -->
      <v-col cols="12" sm="6" md="3">
        <div class="stat-glass-card shadow-teal pa-5 rounded-xl">
          <div class="d-flex align-center justify-space-between mb-3">
            <div class="stat-value text-h3 font-weight-black text-teal">
              {{ reportData.total_approved_questions || 0 }}
            </div>
            <div class="stat-icon-wrapper bg-teal-gradient">
              <v-icon size="24" color="white">mdi-database-check-outline</v-icon>
            </div>
          </div>
          <div class="stat-label text-subtitle-2 font-weight-bold text-medium-emphasis">
            إجمالي الأسئلة المعتمدة
          </div>
          <div class="stat-footer mt-2 pt-2 border-t border-slate-100 text-caption text-medium-emphasis">
            المرتبطة بالمخرجات
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Matrix Custom Data Table -->
    <div class="main-card rounded-2xl overflow-hidden mb-8">
      <custom-data-table
        :headers="headers"
        :items="tableItems"
        :getData="getData"
        :customLoading="loading"
        class="bg-transparent"
        :hasFilter="false"
        :log="false"
        :restore="false"
      >
        <template v-slot:item-slot="{ item, key }">
          <!-- Institution Type -->
          <template v-if="key === 'institutionType'">
            <v-chip
              size="x-small"
              :color="item.institutionType === 'university' ? 'primary' : 'secondary'"
              variant="tonal"
              class="font-weight-bold"
            >
              <v-icon size="12" start>{{ item.institutionType === 'university' ? 'mdi-school' : 'mdi-domain' }}</v-icon>
              {{ item.institutionType === 'university' ? 'جامعي' : 'مدرسي' }}
            </v-chip>
          </template>

          <!-- CLO Code -->
          <template v-else-if="key === 'code'">
            <v-chip color="primary" size="small" variant="tonal" class="font-weight-bold text-white">
              {{ item.code }}
            </v-chip>
          </template>

          <!-- CLO Description -->
          <template v-else-if="key === 'name_ar'">
            <div class="font-weight-medium text-body-2">{{ item.name_ar }}</div>
          </template>

          <!-- Unit Name -->
          <template v-else-if="key === 'unit_name'">
            <v-chip v-if="item.unit_name" size="small" variant="tonal" color="indigo" class="font-weight-medium">
              {{ item.unit_name }}
            </v-chip>
            <span v-else class="text-caption text-medium-emphasis">-</span>
          </template>

          <!-- Questions Count -->
          <template v-else-if="key === 'questions_count'">
            <span class="text-body-1 font-weight-black" :class="item.questions_count === 0 ? 'text-error' : 'text-primary'">
              {{ item.questions_count }}
            </span>
          </template>

          <!-- Coverage Status -->
          <template v-else-if="key === 'coverage_status'">
            <v-chip
              :color="item.coverage_color"
              size="small"
              variant="tonal"
              class="font-weight-bold text-white"
            >
              <v-icon start size="14">
                {{ item.questions_count === 0 ? 'mdi-close-circle' : (item.questions_count < 3 ? 'mdi-alert' : 'mdi-check-circle') }}
              </v-icon>
              {{ item.coverage_status }}
            </v-chip>
          </template>

          <!-- Bloom Taxonomy Breakdown -->
          <template v-else-if="key === 'bloom_breakdown'">
            <div class="d-flex align-center justify-center flex-wrap gap-1">
              <v-tooltip text="تذكر" location="top">
                <template #activator="{ props }">
                  <v-chip v-bind="props" size="x-small" color="blue" variant="tonal">
                    تذكر: {{ item.bloom_breakdown?.remember || 0 }}
                  </v-chip>
                </template>
              </v-tooltip>
              <v-tooltip text="فهم" location="top">
                <template #activator="{ props }">
                  <v-chip v-bind="props" size="x-small" color="teal" variant="tonal">
                    فهم: {{ item.bloom_breakdown?.understand || 0 }}
                  </v-chip>
                </template>
              </v-tooltip>
              <v-tooltip text="تطبيق" location="top">
                <template #activator="{ props }">
                  <v-chip v-bind="props" size="x-small" color="purple" variant="tonal">
                    تطبيق: {{ item.bloom_breakdown?.apply || 0 }}
                  </v-chip>
                </template>
              </v-tooltip>
              <v-tooltip text="تحليل" location="top">
                <template #activator="{ props }">
                  <v-chip v-bind="props" size="x-small" color="amber" variant="tonal">
                    تحليل: {{ item.bloom_breakdown?.analyze || 0 }}
                  </v-chip>
                </template>
              </v-tooltip>
            </div>
          </template>

          <!-- Difficulty Breakdown -->
          <template v-else-if="key === 'difficulty_breakdown'">
            <div class="d-flex align-center justify-center gap-1">
              <v-chip size="x-small" color="success" variant="tonal" class="font-weight-bold">
                سهل: {{ item.difficulty_breakdown?.easy || 0 }}
              </v-chip>
              <v-chip size="x-small" color="warning" variant="tonal" class="font-weight-bold">
                متوسط: {{ item.difficulty_breakdown?.medium || 0 }}
              </v-chip>
              <v-chip size="x-small" color="error" variant="tonal" class="font-weight-bold">
                صعب: {{ item.difficulty_breakdown?.hard || 0 }}
              </v-chip>
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>
  </div>
</template>

<script>
import { reportsService } from '@/services/reportsService'

export default {
  name: 'AlignmentMatrixReportView',

  data() {
    return {
      loading: false,
      filterInstitutionType: 'all',
      filterStage: null,
      filterClassTrack: null,
      selectedSubjectId: null,
      filterCollege: null,
      filterDepartment: null,
      filterSpecialization: null,
      filterSemesterSubject: null,
      searchQuery: '',
      reportData: null,
      tableItems: { results: [], pagination: {} },
    }
  },

  computed: {
    headers() {
      return [
        { title: "النوع", key: "institutionType", sortable: true, width: "100px" },
        { title: "رمز المخرج", key: "code", sortable: true, width: "130px" },
        { title: "وصف مخرج التعلم (CLO)", key: "name_ar", sortable: true },
        { title: this.filterInstitutionType === 'university' ? "المقرر / الوحدة" : "الوحدة الدراسية", key: "unit_name", sortable: true },
        { title: "الأسئلة المتاحة", key: "questions_count", sortable: true, align: "center", width: "130px" },
        { title: "حالة التغطية", key: "coverage_status", sortable: true, align: "center", width: "160px" },
        { title: "توزيع مستويات بلوم", key: "bloom_breakdown", sortable: false, align: "center" },
        { title: "توزيع الصعوبة", key: "difficulty_breakdown", sortable: false, align: "center" },
      ]
    }
  },

  methods: {
    onInstitutionTypeChange() {
      this.filterStage = null
      this.filterClassTrack = null
      this.selectedSubjectId = null
      this.filterCollege = null
      this.filterDepartment = null
      this.filterSpecialization = null
      this.filterSemesterSubject = null
      this.loadMatrixReport()
    },

    onStageChange() {
      this.filterClassTrack = null
    },

    onCollegeChange() {
      this.filterDepartment = null
    },

    async getData(params = {}) {
      this.loading = true
      try {
        const queryParams = {
          ...params,
          institution_type: this.filterInstitutionType !== 'all' ? this.filterInstitutionType : undefined,
          college: this.filterCollege || undefined,
          department: this.filterDepartment || undefined,
          specialization: this.filterSpecialization || undefined,
          semester_subject: this.filterSemesterSubject || undefined,
          stage: this.filterStage || undefined,
          class_track: this.filterClassTrack || undefined,
          subject_id: this.selectedSubjectId || undefined,
          search: this.searchQuery || undefined,
        }
        const data = await reportsService.getAlignmentMatrixReport(queryParams)
        this.reportData = data
        if (!this.selectedSubjectId && !this.filterSemesterSubject && data.subject_id) {
          if (this.filterInstitutionType === 'university') {
            this.filterSemesterSubject = data.subject_id
          } else {
            this.selectedSubjectId = data.subject_id
          }
        }
        const clos = data.clos || []
        this.tableItems = {
          results: clos,
          pagination: { count: clos.length, total: clos.length },
        }
      } catch (err) {
        console.error('Error loading alignment matrix:', err)
      } finally {
        this.loading = false
      }
    },

    async loadMatrixReport() {
      await this.getData()
    },

    onSubjectChange() {
      this.loadMatrixReport()
    },

    resetFilters() {
      this.filterInstitutionType = 'all'
      this.filterStage = null
      this.filterClassTrack = null
      this.selectedSubjectId = null
      this.filterCollege = null
      this.filterDepartment = null
      this.filterSpecialization = null
      this.filterSemesterSubject = null
      this.searchQuery = ''
      this.loadMatrixReport()
    },

    printReport() {
      window.print()
    },
  },

  mounted() {
    this.loadMatrixReport()
  },
}
</script>

<style scoped>
.main-card {
  background: white;
  border-color: rgba(0, 0, 0, 0.08) !important;
}

.stat-glass-card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.06);
  transition: all 0.25s ease;
}

.stat-glass-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.08);
}

.stat-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-indigo-gradient {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
}

.bg-emerald-gradient {
  background: linear-gradient(135deg, #10b981, #059669);
}

.bg-rose-gradient {
  background: linear-gradient(135deg, #f43f5e, #e11d48);
}

.bg-teal-gradient {
  background: linear-gradient(135deg, #14b8a6, #0d9488);
}

.shadow-indigo {
  box-shadow: 0 8px 20px -6px rgba(99, 102, 241, 0.18);
}

.shadow-emerald {
  box-shadow: 0 8px 20px -6px rgba(16, 185, 129, 0.18);
}

.shadow-rose {
  box-shadow: 0 8px 20px -6px rgba(244, 63, 94, 0.18);
}

.shadow-teal {
  box-shadow: 0 8px 20px -6px rgba(20, 184, 166, 0.18);
}
</style>
