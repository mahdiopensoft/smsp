<template>
  <div class="qb-regional-report-v4">
    <!-- Header Controls -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div>
        <h2 class="text-h5 font-weight-black mb-1">التقرير الإقليمي والجغرافي (Regional Report)</h2>
        <span class="text-caption text-medium-emphasis">
          مقارنة الأداء الأكاديمي بين المحافظات والمدن الرئيسية والمناطق النائية ومعامل العدالة الجغرافية
        </span>
      </div>

      <div class="d-flex align-center gap-3">
        <custom-btn
          label="طباعة التقرير (PDF)"
          icon="mdi-printer"
          color="primary"
          variant="tonal"
          class="font-weight-bold px-5"
          :click="printReport"
        />
      </div>
    </div>

    <!-- Filters Control Bar (Theme Compatible) -->
    <filter-fields label="خيارات تصفية التقرير الإقليمي (مدرسي / جامعي)" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Institution Type Filter -->
        <v-col cols="12" md="2">
          <v-select
            v-model="filter_fields.institution_type"
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
        <template v-if="filter_fields.institution_type !== 'university'">
          <!-- Stage Filter -->
          <auto-list
            v-model="filter_fields.stageId"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="2"
            :add="false"
            @update:model-value="onStageChange"
          />

          <!-- ClassTrack Filter (الصف والمسار) -->
          <auto-list
            v-model="filter_fields.classTrackId"
            name="ClassTrackByStage"
            :param="filter_fields.stageId"
            placeholder="الصف والمسار"
            cols="2"
            :add="false"
            :disabled="!filter_fields.stageId"
            @update:model-value="loadReport"
          />

          <!-- Subject Filter -->
          <auto-list
            v-model="filter_fields.subjectId"
            name="Subject"
            placeholder="المادة الدراسية"
            cols="2"
            :add="false"
            @update:model-value="loadReport"
          />
        </template>

        <!-- University Filters -->
        <template v-if="filter_fields.institution_type !== 'school'">
          <auto-list
            v-model="filter_fields.collegeId"
            name="College"
            placeholder="الكلية"
            :add="false"
            cols="2"
            @update:model-value="onCollegeChange"
          />

          <auto-list
            v-model="filter_fields.departmentId"
            name="DepartmentByCollege"
            :param="filter_fields.collegeId"
            placeholder="القسم الأكاديمي"
            :add="false"
            cols="2"
            :disabled="!filter_fields.collegeId"
            @update:model-value="loadReport"
          />

          <auto-list
            v-model="filter_fields.specializationId"
            name="Specialization"
            placeholder="التخصص الجامعي"
            :add="false"
            cols="2"
            @update:model-value="loadReport"
          />

          <auto-list
            v-model="filter_fields.semesterSubjectId"
            name="SemesterSubject"
            placeholder="المقرر الجامعي"
            :add="false"
            cols="2"
            @update:model-value="loadReport"
          />
        </template>

        <!-- Exam Filter -->
        <auto-list
          v-model="filter_fields.examId"
          name="Exam"
          :param="examFilterParam"
          placeholder="اختر الاختبار"
          cols="3"
          :add="false"
          @update:model-value="loadReport"
        />

        <!-- Comparison Type -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filter_fields.comparisonType"
            :items="comparisonOptions"
            item-title="text"
            item-value="value"
            placeholder="نوع المقارنة"
            variant="outlined"
            density="compact"
            class="mb-6"
            hide-details
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- Filter Actions -->
        <v-col cols="12" sm="6" md="3" class="d-flex align-center gap-2">
          <custom-btn
            type="show"
            label="تحديث"
            color="primary"
            class="font-weight-bold flex-grow-1 mb-6"
            :loading="loading"
            :click="loadReport"
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

    <!-- Justice Impact Alert (Calculated from Backend) -->
    <v-alert
      v-if="summary.justiceImpact"
      type="info"
      variant="tonal"
      class="mb-6 rounded-2xl font-weight-medium border"
      border="start"
    >
      <template #title>
        <span class="font-weight-bold">مؤشر العدالة وتكافؤ الفرص الجغرافي:</span>
      </template>
      تم تطبيق معامل تخفيف صعوبة الأسئلة على المدارس والمناطق النائية. الفارق في متوسط الدرجات بين المدن والمناطق النائية
      قبل المعايرة: <strong>{{ summary.justiceImpact.beforeAdjustmentDiff }}%</strong>، وبعد المعايرة:
      <strong class="text-primary">{{ summary.justiceImpact.afterAdjustmentDiff }}%</strong>
      (تحسن في مؤشر العدالة بنسبة <strong>{{ summary.justiceImpact.improvementRate }}%</strong>).
    </v-alert>

    <!-- Overview Stat Cards -->
    <v-row class="mb-6">
      <!-- City Average -->
      <v-col cols="12" sm="6" md="3">
        <div class="stat-glass-card shadow-indigo pa-5 rounded-xl">
          <div class="d-flex align-center justify-space-between mb-3">
            <div class="stat-value text-h3 font-weight-black text-indigo">
              {{ summary.cityAverage }}%
            </div>
            <div class="stat-icon-wrapper bg-indigo-gradient">
              <v-icon size="24" color="white">mdi-city</v-icon>
            </div>
          </div>
          <div class="stat-label text-subtitle-2 font-weight-bold text-medium-emphasis">متوسط المدن الرئيسية</div>
          <div class="stat-footer mt-2 pt-2 border-t border-slate-100 text-caption text-medium-emphasis">
            إجمالي الطلاب: {{ (summary.cityStudents || 0).toLocaleString() }}
          </div>
        </div>
      </v-col>

      <!-- Remote Average -->
      <v-col cols="12" sm="6" md="3">
        <div class="stat-glass-card shadow-amber pa-5 rounded-xl">
          <div class="d-flex align-center justify-space-between mb-3">
            <div class="stat-value text-h3 font-weight-black text-amber">
              {{ summary.remoteAverage }}%
            </div>
            <div class="stat-icon-wrapper bg-amber-gradient">
              <v-icon size="24" color="white">mdi-map-marker-radius</v-icon>
            </div>
          </div>
          <div class="stat-label text-subtitle-2 font-weight-bold text-medium-emphasis">متوسط المناطق النائية</div>
          <div class="stat-footer mt-2 pt-2 border-t border-slate-100 text-caption text-medium-emphasis">
            إجمالي الطلاب: {{ (summary.remoteStudents || 0).toLocaleString() }}
          </div>
        </div>
      </v-col>

      <!-- Score Gap -->
      <v-col cols="12" sm="6" md="3">
        <div class="stat-glass-card shadow-emerald pa-5 rounded-xl">
          <div class="d-flex align-center justify-space-between mb-3">
            <div class="stat-value text-h3 font-weight-black text-emerald">
              {{ summary.difference }}%
            </div>
            <div class="stat-icon-wrapper bg-emerald-gradient">
              <v-icon size="24" color="white">mdi-scale-balance</v-icon>
            </div>
          </div>
          <div class="stat-label text-subtitle-2 font-weight-bold text-medium-emphasis">فارق الأداء (الفجوة)</div>
          <div class="stat-footer mt-2 pt-2 border-t border-slate-100 text-caption text-medium-emphasis">
            ضمن المعدل الآمن المقبول
          </div>
        </div>
      </v-col>

      <!-- Pass Rate Difference -->
      <v-col cols="12" sm="6" md="3">
        <div class="stat-glass-card shadow-teal pa-5 rounded-xl">
          <div class="d-flex align-center justify-space-between mb-3">
            <div class="stat-value text-h3 font-weight-black text-teal">
              {{ summary.passRateDiff }}%
            </div>
            <div class="stat-icon-wrapper bg-teal-gradient">
              <v-icon size="24" color="white">mdi-chart-bell-curve</v-icon>
            </div>
          </div>
          <div class="stat-label text-subtitle-2 font-weight-bold text-medium-emphasis">فارق نسب النجاح</div>
          <div class="stat-footer mt-2 pt-2 border-t border-slate-100 text-caption text-medium-emphasis">
            بين المركز والأطراف
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Regional Comparison Chart & Performance Bars -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card elevation="0" class="main-card pa-6 rounded-2xl border">
          <div class="d-flex align-center justify-space-between mb-4">
            <div class="d-flex align-center gap-2">
              <v-icon color="primary">mdi-chart-bar</v-icon>
              <h3 class="text-subtitle-1 font-weight-black mb-0">مقارنة متوسطات المحافظات ونسب النجاح</h3>
            </div>
            <v-chip color="secondary" size="small" variant="tonal" class="font-weight-bold">
              {{ filteredGovernorates.length }} محافظة مسجلة
            </v-chip>
          </div>

          <v-row>
            <v-col
              v-for="region in filteredGovernorates"
              :key="region.id"
              cols="12"
              md="6"
              class="mb-3"
            >
              <div class="pa-4 rounded-xl border bg-slate-50">
                <div class="d-flex justify-space-between align-center mb-2">
                  <div class="d-flex align-center gap-2">
                    <v-avatar size="28" :color="region.isRemote ? 'warning' : 'primary'" variant="tonal">
                      <v-icon size="16">{{ region.isRemote ? 'mdi-map-marker-radius' : 'mdi-city' }}</v-icon>
                    </v-avatar>
                    <span class="font-weight-bold text-body-2">{{ region.name }}</span>
                    <v-chip size="x-small" :color="region.isRemote ? 'warning' : 'primary'" variant="tonal" class="text-white font-weight-bold">
                      {{ region.type }}
                    </v-chip>
                  </div>
                  <div class="d-flex align-center gap-2">
                    <span class="text-body-2 font-weight-black text-primary">{{ region.average }}%</span>
                    <v-chip size="x-small" :color="region.trend >= 0 ? 'success' : 'error'" variant="tonal" class="font-weight-bold">
                      {{ region.trend >= 0 ? '+' : '' }}{{ region.trend }}%
                    </v-chip>
                  </div>
                </div>

                <v-progress-linear
                  :model-value="region.average"
                  :color="region.isRemote ? 'warning' : 'primary'"
                  height="16"
                  rounded
                  class="rounded-pill"
                >
                  <template #default>
                    <span class="text-white text-caption font-weight-bold">{{ region.passRate }}% نسبة النجاح</span>
                  </template>
                </v-progress-linear>
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <!-- Detailed Custom Data Table -->
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
          <!-- Governorate Name -->
          <template v-if="key === 'name'">
            <div class="d-flex align-center gap-2">
              <v-icon :color="item.isRemote ? 'warning' : 'primary'" size="18">
                {{ item.isRemote ? 'mdi-map-marker-radius' : 'mdi-city' }}
              </v-icon>
              <span class="font-weight-bold">{{ item.name }}</span>
            </div>
          </template>

          <!-- Type -->
          <template v-else-if="key === 'type'">
            <v-chip
              :color="item.isRemote ? 'warning' : 'primary'"
              variant="tonal"
              size="small"
              class="font-weight-bold"
            >
              {{ item.type }}
            </v-chip>
          </template>

          <!-- Modifier -->
          <template v-else-if="key === 'modifier'">
            <v-chip
              :color="item.modifier < 1 ? 'info' : 'default'"
              variant="outlined"
              size="small"
              class="font-weight-bold"
            >
              ×{{ item.modifier.toFixed(2) }}
            </v-chip>
          </template>

          <!-- Students -->
          <template v-else-if="key === 'students'">
            <span class="font-weight-medium">{{ (item.students || 0).toLocaleString() }}</span>
          </template>

          <!-- Average -->
          <template v-else-if="key === 'average'">
            <span class="font-weight-black text-body-2" :class="getScoreColor(item.average)">
              {{ item.average }}%
            </span>
          </template>

          <!-- Pass Rate -->
          <template v-else-if="key === 'passRate'">
            <div class="d-flex align-center justify-center gap-2">
              <v-progress-linear
                :model-value="item.passRate"
                :color="item.passRate >= 75 ? 'success' : (item.passRate >= 60 ? 'primary' : 'error')"
                height="10"
                rounded
                style="width: 80px;"
              />
              <span class="text-caption font-weight-bold">{{ item.passRate }}%</span>
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
  name: 'RegionalReportView',

  data() {
    return {
      loading: false,

      filter_fields: {
        institution_type: 'all',
        stageId: null,
        classTrackId: null,
        subjectId: null,
        collegeId: null,
        departmentId: null,
        specializationId: null,
        semesterSubjectId: null,
        examId: null,
        comparisonType: 'all',
      },

      comparisonOptions: [
        { text: 'الكل (جميع المحافظات)', value: 'all' },
        { text: 'المدن الرئيسية فقط', value: 'cities_only' },
        { text: 'المناطق النائية فقط', value: 'remote_only' },
      ],

      summary: {
        cityAverage: 75.0,
        remoteAverage: 65.3,
        difference: 9.7,
        passRateDiff: 8.5,
        cityStudents: 0,
        remoteStudents: 0,
        justiceImpact: null,
      },

      allGovernorates: [],
      filteredGovernorates: [],
      tableItems: { results: [], pagination: {} },

      headers: [
        { title: 'المحافظة / الإقليم', key: 'name', sortable: true },
        { title: 'التصنيف الجغرافي', key: 'type', sortable: true, align: 'center' },
        { title: 'معامل الصعوبة', key: 'modifier', sortable: true, align: 'center' },
        { title: 'عدد الطلاب الممتحنين', key: 'students', sortable: true, align: 'center' },
        { title: 'المتوسط العام', key: 'average', sortable: true, align: 'center' },
        { title: 'نسبة النجاح', key: 'passRate', sortable: true, align: 'center' },
      ],
    }
  },

  computed: {
    examFilterParam() {
      if (this.filter_fields.institution_type && this.filter_fields.institution_type !== 'all') {
        return { institution_type: this.filter_fields.institution_type }
      }
      return null
    },
  },

  methods: {
    onInstitutionTypeChange() {
      this.filter_fields.stageId = null
      this.filter_fields.classTrackId = null
      this.filter_fields.subjectId = null
      this.filter_fields.collegeId = null
      this.filter_fields.departmentId = null
      this.filter_fields.specializationId = null
      this.filter_fields.semesterSubjectId = null
      this.filter_fields.examId = null
      this.loadReport()
    },

    onStageChange() {
      this.filter_fields.classTrackId = null
      this.loadReport()
    },

    onCollegeChange() {
      this.filter_fields.departmentId = null
      this.loadReport()
    },

    async getData(params = {}) {
      this.loading = true
      try {
        const queryParams = {
          ...params,
          institution_type: this.filter_fields.institution_type !== 'all' ? this.filter_fields.institution_type : undefined,
          college: this.filter_fields.collegeId || undefined,
          department: this.filter_fields.departmentId || undefined,
          specialization: this.filter_fields.specializationId || undefined,
          semester_subject: this.filter_fields.semesterSubjectId || undefined,
          stage_id: this.filter_fields.stageId || undefined,
          class_track_id: this.filter_fields.classTrackId || undefined,
          exam_id: this.filter_fields.examId || undefined,
          subject_id: this.filter_fields.subjectId || undefined,
        }
        const data = await reportsService.getRegionalReport(queryParams)
        if (data) {
          this.summary = data.summary || this.summary
          this.allGovernorates = data.governorates || []
          this.applyFilters()
        }
      } catch (err) {
        console.error('Error fetching regional report:', err)
      } finally {
        this.loading = false
      }
    },

    async loadReport() {
      await this.getData()
    },

    applyFilters() {
      let list = [...this.allGovernorates]
      if (this.filter_fields.comparisonType === 'cities_only') {
        list = list.filter(g => !g.isRemote)
      } else if (this.filter_fields.comparisonType === 'remote_only') {
        list = list.filter(g => g.isRemote)
      }
      this.filteredGovernorates = list
      this.tableItems = {
        results: list,
        pagination: { count: list.length, total: list.length },
      }
    },

    resetFilters() {
      this.filter_fields = {
        institution_type: 'all',
        stageId: null,
        classTrackId: null,
        subjectId: null,
        collegeId: null,
        departmentId: null,
        specializationId: null,
        semesterSubjectId: null,
        examId: null,
        comparisonType: 'all',
      }
      this.loadReport()
    },

    getScoreColor(val) {
      if (val >= 75) return 'text-success'
      if (val >= 60) return 'text-primary'
      return 'text-error'
    },

    printReport() {
      window.print()
    },
  },

  mounted() {
    this.loadReport()
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

.bg-amber-gradient {
  background: linear-gradient(135deg, #f59e0b, #d97706);
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

.shadow-amber {
  box-shadow: 0 8px 20px -6px rgba(245, 158, 11, 0.18);
}

.shadow-teal {
  box-shadow: 0 8px 20px -6px rgba(20, 184, 166, 0.18);
}
</style>
