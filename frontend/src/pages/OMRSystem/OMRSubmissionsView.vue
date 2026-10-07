<template>
  <div class="qb-submissions-view-v4">
    <!-- Header Controls & Actions -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div>
        <h2 class="text-h5 font-weight-black mb-1">أوراق الطلاب المصححة (OMR Submissions)</h2>
        <span class="text-caption text-medium-emphasis">
          إدارة ومتابعة نتائج الأوراق المعالجة ضوئياً ومراجعة درجات الطلاب
        </span>
      </div>

      <div class="d-flex align-center gap-3">
        <custom-btn
          label="شاشة المسح الضوئي (Lab)"
          icon="mdi-scanner"
          color="indigo"
          variant="tonal"
          class="font-weight-bold px-5"
          :click="() => $router.push('/omr-scanner')"
        />
        <custom-btn
          type="add"
          icon="mdi-cloud-upload-outline"
          label="استخراج وتصحيح مباشر"
          color="primary"
          class="font-weight-bold px-5"
          :click="() => $router.push('/omr-extraction')"
        />
      </div>
    </div>

    <!-- Stats Bar Dashboard (Calculated directly on Backend) -->
    <v-row class="mb-6">
      <!-- Total Submissions -->
      <v-col cols="12" sm="6" md="3">
        <div class="stat-glass-card pa-5 rounded-xl shadow-indigo">
          <div class="d-flex align-center justify-space-between mb-3">
            <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">إجمالي الأوراق</span>
            <div class="stat-icon-wrapper bg-indigo-gradient">
              <v-icon color="white" size="22">mdi-file-multiple-outline</v-icon>
            </div>
          </div>
          <div class="stat-value text-h3 font-weight-black mb-2 text-indigo">{{ statsData.total || 0 }}</div>
          <div class="stat-footer border-t pt-2 mt-2 text-caption text-medium-emphasis">
            <span>جميع السجلات المرفوعة</span>
          </div>
        </div>
      </v-col>

      <!-- Completed Submissions -->
      <v-col cols="12" sm="6" md="3">
        <div class="stat-glass-card pa-5 rounded-xl shadow-emerald">
          <div class="d-flex align-center justify-space-between mb-3">
            <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">أوراق مصححة بالكامل</span>
            <div class="stat-icon-wrapper bg-emerald-gradient">
              <v-icon color="white" size="22">mdi-check-decagram-outline</v-icon>
            </div>
          </div>
          <div class="stat-value text-h3 font-weight-black mb-2 text-emerald">{{ statsData.completed || 0 }}</div>
          <div class="stat-footer border-t pt-2 mt-2 text-caption text-medium-emphasis">
            <span>متوسط الدرجات: {{ statsData.average_score || 0 }}</span>
          </div>
        </div>
      </v-col>

      <!-- Needs Review Submissions -->
      <v-col cols="12" sm="6" md="3">
        <div class="stat-glass-card pa-5 rounded-xl shadow-amber">
          <div class="d-flex align-center justify-space-between mb-3">
            <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">تحت المراجعة البشرية</span>
            <div class="stat-icon-wrapper bg-amber-gradient">
              <v-icon color="white" size="22">mdi-account-eye-outline</v-icon>
            </div>
          </div>
          <div class="stat-value text-h3 font-weight-black mb-2 text-amber">{{ statsData.needs_review || 0 }}</div>
          <div class="stat-footer border-t pt-2 mt-2 text-caption text-medium-emphasis">
            <span class="text-amber-darken-2 font-weight-bold">تتطلب تدقيق يدوي</span>
          </div>
        </div>
      </v-col>

      <!-- Failed Submissions -->
      <v-col cols="12" sm="6" md="3">
        <div class="stat-glass-card pa-5 rounded-xl shadow-rose">
          <div class="d-flex align-center justify-space-between mb-3">
            <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">أوراق فشلت المعالجة</span>
            <div class="stat-icon-wrapper bg-rose-gradient">
              <v-icon color="white" size="22">mdi-alert-circle-outline</v-icon>
            </div>
          </div>
          <div class="stat-value text-h3 font-weight-black mb-2 text-rose">{{ statsData.failed || 0 }}</div>
          <div class="stat-footer border-t pt-2 mt-2 text-caption text-medium-emphasis">
            <span>تحتاج إعادة معالجة أو مسح</span>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Filters Control Bar (Theme Compatible) -->
    <filter-fields label="خيارات تصفية أوراق الإجابة ونتائج التصحيح" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Institution Type Selector (مدارس / جامعات / الكل) -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterInstitutionType"
            :items="institutionTypeOptions"
            item-title="text"
            item-value="value"
            class="mb-6"
            placeholder="نوع المؤسسة"
            prepend-inner-icon="mdi-domain"
            hide-details
            density="compact"
            variant="outlined"
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

        <!-- 🏫 School Filters -->
        <template v-if="filterInstitutionType === 'school' || filterInstitutionType === 'all'">
          <auto-list
            v-if="filterInstitutionType === 'school'"
            v-model="filterStage"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="3"
            :add="false"
            @update:model-value="onStageChange"
          />
          <auto-list
            v-if="filterInstitutionType === 'school'"
            v-model="filterClassTrack"
            name="ClassTrackByStage"
            :param="filterStage"
            placeholder="الصف والمسار"
            cols="3"
            :add="false"
            :disabled="!filterStage"
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
            @update:model-value="filterSpecialization = null"
          />
          <auto-list
            v-model="filterSpecialization"
            name="Specialization"
            :param="filterDepartment"
            placeholder="التخصص والبرنامج"
            cols="3"
            :add="false"
            :disabled="!filterDepartment"
          />
          <auto-list
            v-model="filterSemesterSubject"
            name="SemesterSubject"
            :param="filterSpecialization"
            placeholder="مقرر الفصل الجامعي"
            cols="3"
            :add="false"
          />
        </template>

        <!-- Common Subject Filter (School only) -->
        <auto-list
          v-if="filterInstitutionType !== 'university'"
          v-model="filterSubject"
          name="Subject"
          placeholder="المادة الدراسية"
          cols="3"
          :add="false"
          @update:model-value="onSubjectChange"
        />

        <!-- Exam Filter -->
        <auto-list
          v-model="filterExam"
          name="Exam"
          :param="examFilterParam"
          :key="JSON.stringify(examFilterParam)"
          placeholder="الاختبار"
          cols="3"
          :add="false"
        />

        <!-- Status Filter -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterStatus"
            :items="statusOptions"
            item-title="title"
            item-value="value"
            placeholder="حالة التصحيح"
            prepend-inner-icon="mdi-list-status"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Search Query -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="searchQuery"
            :placeholder="filterInstitutionType === 'university' ? 'بحث بالرقم الأكاديمي أو اسم الطالب...' : 'بحث برقم الجلوس أو اسم الطالب...'"
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Filter Action Buttons -->
        <v-col cols="12" sm="6" md="3" class="d-flex align-center gap-2">
          <custom-btn
            type="show"
            label="تصفية"
            color="primary"
            class="font-weight-bold flex-grow-1 mb-6"
            :click="loadData"
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
          <!-- Seat Number -->
          <template v-if="key === 'seat_number'">
            <span class="font-weight-bold text-body-2 text-on-surface">{{ item.seat_number || '-' }}</span>
          </template>

          <!-- Student Name -->
          <template v-else-if="key === 'student_name'">
            <div>
              <div class="font-weight-bold text-body-2 text-on-surface">{{ item.student_name || 'طالب غير محدد' }}</div>
              <div class="text-caption text-medium-emphasis">{{ item.subject_name || '-' }}</div>
            </div>
          </template>

          <!-- Exam & Version -->
          <template v-else-if="key === 'exam_title'">
            <div>
              <div class="text-body-2 font-weight-bold">{{ item.exam_title || 'اختبار عام' }}</div>
              <div class="text-caption text-medium-emphasis mt-1">
                <span>{{ item.institution_type === 'university' ? 'جامعي' : 'مدرسي' }}</span>
                <span v-if="item.exam_version_code" class="ms-1 font-weight-medium">• {{ item.exam_version_code }}</span>
              </div>
            </div>
          </template>

          <!-- Total Score -->
          <template v-else-if="key === 'total_score'">
            <div>
              <span class="text-body-2 font-weight-black text-on-surface">
                {{ item.total_score != null ? item.total_score : '-' }}
              </span>
              <div v-if="item.mcq_score != null" class="text-caption text-medium-emphasis">
                خيارات: {{ item.mcq_score }} | مقالي: {{ item.essay_score || 0 }}
              </div>
            </div>
          </template>

          <!-- Status -->
          <template v-else-if="key === 'status'">
            <v-chip
              size="small"
              :color="getStatusColor(item.status)"
              variant="tonal"
              class="font-weight-bold unified-table-chip"
            >
              {{ item.status_display || item.status }}
            </v-chip>
          </template>

          <!-- Actions -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-1">
              <custom-btn
                type="show"
                is-icon
                label="معاينة وتدقيق الورقة"
                :click="() => openReviewDialog(item)"
              />
              <custom-btn
                type="refresh"
                is-icon
                label="إعادة المعالجة الضوئية"
                :loading="reprocessingId === item.id"
                :click="() => reprocessSubmission(item)"
              />
              <custom-btn
                type="del"
                is-icon
                label="حذف ورقة الإجابة"
                :click="() => confirmDelete(item)"
              />
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>

    <!-- Review & Score Adjustment Dialog (CustomDialog Component) -->
    <CustomDialog
      v-model="reviewDialog"
      width="680"
      title="مراجعة وتعديل نتيجة ورقة الإجابة"
      :subTitle="selectedSubmission ? `طالب: ${selectedSubmission.student_name} • رقم الجلوس: ${selectedSubmission.seat_number}` : ''"
    >
      <div v-if="selectedSubmission">
        <!-- Status & Metrics Summary -->
        <div class="d-flex flex-wrap gap-2 mb-4">
          <v-chip :color="getStatusColor(selectedSubmission.status)" variant="flat" class="font-weight-bold text-white">
            الحالة: {{ selectedSubmission.status_display || selectedSubmission.status }}
          </v-chip>
          <v-chip v-if="selectedSubmission.overall_confidence" color="indigo" variant="tonal" class="font-weight-bold">
            نسبة الثقة: {{ Math.round(selectedSubmission.overall_confidence * 100) }}%
          </v-chip>
        </div>

        <v-row class="mb-3">
          <v-col cols="12" md="6">
            <v-text-field
              v-model.number="reviewForm.mcq_score"
              label="درجة أسئلة الخيارات (MCQ) *"
              type="number"
              variant="outlined"
              density="compact"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model.number="reviewForm.essay_score"
              label="درجة الأسئلة المقالية (Essay) *"
              type="number"
              variant="outlined"
              density="compact"
            />
          </v-col>
          <v-col cols="12">
            <v-select
              v-model="reviewForm.status"
              :items="[
                { title: 'مكتمل ومعتمد (Completed)', value: 'completed' },
                { title: 'تمت المراجعة (Reviewed)', value: 'reviewed' },
                { title: 'يحتاج مراجعة إضافية (Needs Review)', value: 'needs_review' }
              ]"
              label="الحالة بعد الاعتماد *"
              variant="outlined"
              density="compact"
            />
          </v-col>
        </v-row>

        <div v-if="selectedSubmission.original_image" class="text-center pa-3 bg-slate-50 rounded-xl border mb-3">
          <div class="text-caption text-medium-emphasis mb-2 font-weight-bold">صورة ورقة الإجابة الممسوحة:</div>
          <v-img :src="selectedSubmission.original_image" max-height="240" contain class="rounded-lg mx-auto" />
        </div>
      </div>

      <template #actions>
        <custom-btn
          type="cancel"
          :click="() => reviewDialog = false"
          variant="text"
          label="إلغاء"
          class="font-weight-bold"
        />
        <custom-btn
          type="add"
          :click="submitReview"
          :loading="savingReview"
          color="primary"
          label="اعتماد وحفظ الدرجات"
          class="font-weight-bold ms-auto"
        />
      </template>
    </CustomDialog>

    <!-- Delete Confirmation Modal (DeleteDialog Component) -->
    <DeleteDialog
      v-model="deleteDialog"
      title="حذف ورقة الإجابة"
      :message="`هل أنت متأكد من حذف ورقة إجابة الطالب '${submissionToDelete ? submissionToDelete.student_name : ''}'؟`"
      @confirm-delete="executeDelete"
    />
  </div>
</template>

<script>
import { submissionsAPI } from '@/services/omr/endpoints'

export default {
  name: 'OMRSubmissionsView',

  data() {
    return {
      loading: false,
      savingReview: false,
      reprocessingId: null,

      // Data items
      tableItems: { results: [], pagination: {} },
      statsData: {
        total: 0,
        completed: 0,
        needs_review: 0,
        failed: 0,
        average_score: 0,
      },

      // Filters
      filterInstitutionType: 'all',
      institutionTypeOptions: [
        { text: "الكل (مدارس وجامعات)", value: "all" },
        { text: "🏫 مدارس فقط", value: "school" },
        { text: "🎓 جامعات فقط", value: "university" },
      ],
      filterCollege: null,
      filterDepartment: null,
      filterSpecialization: null,
      filterSemesterSubject: null,
      filterStage: null,
      filterClassTrack: null,
      filterSubject: null,
      filterExam: null,
      filterStatus: null,
      searchQuery: '',

      statusOptions: [
        { title: 'مكتمل (Completed)', value: 'completed' },
        { title: 'يحتاج مراجعة (Needs Review)', value: 'needs_review' },
        { title: 'تمت المراجعة (Reviewed)', value: 'reviewed' },
        { title: 'فشل التصحيح (Failed)', value: 'failed' },
        { title: 'قيد الانتظار (Pending)', value: 'pending' },
      ],

      // Dialogs
      reviewDialog: false,
      deleteDialog: false,
      selectedSubmission: null,
      submissionToDelete: null,

      reviewForm: {
        mcq_score: 0,
        essay_score: 0,
        status: 'completed',
      },
    }
  },

  computed: {
    examFilterParam() {
      if (this.filterInstitutionType === 'university') {
        const p = { institution_type: 'university' }
        if (this.filterCollege) p.college = this.filterCollege
        if (this.filterDepartment) p.department = this.filterDepartment
        if (this.filterSpecialization) p.specialization = this.filterSpecialization
        if (this.filterSemesterSubject) p.semester_subject = this.filterSemesterSubject
        return p
      } else if (this.filterInstitutionType === 'school') {
        const p = { institution_type: 'school' }
        if (this.filterStage) p.stage = this.filterStage
        if (this.filterClassTrack) p.class_track = this.filterClassTrack
        if (this.filterSubject) p.subject = this.filterSubject
        return p
      }
      return this.filterSubject ? this.filterSubject : null
    },

    headers() {
      const isUniv = this.filterInstitutionType === 'university'
      return [
        { title: isUniv ? "الرقم الأكاديمي" : "رقم الجلوس", key: "seat_number", sortable: true, width: "130px" },
        { title: "اسم الطالب والمادة", key: "student_name", sortable: true },
        { title: "الاختبار والنموذج", key: "exam_title", sortable: false },
        { title: "الدرجة الكلية", key: "total_score", sortable: true, align: "center" },
        { title: "حالة التصحيح", key: "status", sortable: true, align: "center", width: "140px" },
      ]
    },
  },

  methods: {
    async getData(params = {}) {
      this.loading = true
      try {
        const queryParams = {
          ...params,
          institution_type: (this.filterInstitutionType && this.filterInstitutionType !== 'all') ? this.filterInstitutionType : undefined,
          college: this.filterCollege || undefined,
          department: this.filterDepartment || undefined,
          specialization: this.filterSpecialization || undefined,
          semester_subject: this.filterSemesterSubject || undefined,
          stage: this.filterStage || undefined,
          class_track: this.filterClassTrack || undefined,
          subject: this.filterSubject || undefined,
          exam: this.filterExam || undefined,
          status: this.filterStatus || undefined,
          search: this.searchQuery || undefined,
        }
        const res = await submissionsAPI.list(queryParams)
        const data = res.data || res
        if (Array.isArray(data)) {
          this.tableItems = {
            results: data,
            pagination: { count: data.length, total: data.length },
          }
        } else {
          this.tableItems = data
        }
      } catch (err) {
        console.error('Error fetching submissions:', err)
      } finally {
        this.loading = false
      }
    },

    async loadStats() {
      try {
        const res = await submissionsAPI.getStats({
          institution_type: (this.filterInstitutionType && this.filterInstitutionType !== 'all') ? this.filterInstitutionType : undefined,
          college: this.filterCollege || undefined,
          department: this.filterDepartment || undefined,
          specialization: this.filterSpecialization || undefined,
          semester_subject: this.filterSemesterSubject || undefined,
          stage: this.filterStage || undefined,
          class_track: this.filterClassTrack || undefined,
          subject: this.filterSubject || undefined,
          exam: this.filterExam || undefined,
          status: this.filterStatus || undefined,
          search: this.searchQuery || undefined,
        })
        this.statsData = res.data || res || { total: 0, completed: 0, needs_review: 0, failed: 0, average_score: 0 }
      } catch (err) {
        console.error('Error loading stats:', err)
      }
    },

    onInstitutionTypeChange() {
      this.filterStage = null
      this.filterClassTrack = null
      this.filterCollege = null
      this.filterDepartment = null
      this.filterSpecialization = null
      this.filterSemesterSubject = null
      this.filterSubject = null
      this.filterExam = null
      this.loadData()
    },

    onCollegeChange() {
      this.filterDepartment = null
      this.filterSpecialization = null
      this.filterSemesterSubject = null
      this.filterExam = null
    },

    onStageChange() {
      this.filterClassTrack = null
      this.filterExam = null
    },

    onSubjectChange() {
      this.filterExam = null
    },

    resetFilters() {
      this.filterInstitutionType = 'all'
      this.filterCollege = null
      this.filterDepartment = null
      this.filterSpecialization = null
      this.filterSemesterSubject = null
      this.filterStage = null
      this.filterClassTrack = null
      this.filterSubject = null
      this.filterExam = null
      this.filterStatus = null
      this.searchQuery = ''
      this.loadData()
    },

    async loadData() {
      await Promise.all([
        this.getData(),
        this.loadStats(),
      ])
    },

    getStatusColor(status) {
      const map = {
        completed: 'success',
        reviewed: 'teal',
        needs_review: 'warning',
        failed: 'error',
        pending: 'grey',
        omr_processing: 'indigo',
        htr_processing: 'purple',
        aligning: 'info',
        judging: 'blue',
      }
      return map[status] || 'grey'
    },

    openReviewDialog(item) {
      this.selectedSubmission = item
      this.reviewForm = {
        mcq_score: Number(item.mcq_score) || 0,
        essay_score: Number(item.essay_score) || 0,
        status: item.status === 'needs_review' ? 'completed' : item.status,
      }
      this.reviewDialog = true
    },

    async submitReview() {
      if (!this.selectedSubmission) return
      this.savingReview = true
      try {
        await submissionsAPI.updateReview(this.selectedSubmission.id, this.reviewForm)
        this.reviewDialog = false
        await this.loadData()
      } catch (err) {
        console.error('Error updating review:', err)
      } finally {
        this.savingReview = false
      }
    },

    async reprocessSubmission(item) {
      this.reprocessingId = item.id
      try {
        await submissionsAPI.reprocess(item.id)
        await this.loadData()
      } catch (err) {
        console.error('Error reprocessing submission:', err)
      } finally {
        this.reprocessingId = null
      }
    },

    confirmDelete(item) {
      this.submissionToDelete = item
      this.deleteDialog = true
    },

    async executeDelete() {
      if (!this.submissionToDelete) return
      try {
        await submissionsAPI.delete(this.submissionToDelete.id)
        this.deleteDialog = false
        this.submissionToDelete = null
        await this.loadData()
      } catch (err) {
        console.error('Error deleting submission:', err)
      }
    },

    resetFilters() {
      this.filterSubject = null
      this.filterStatus = null
      this.searchQuery = ''
      this.loadData()
    },
  },

  mounted() {
    this.loadData()
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

.bg-rose-gradient {
  background: linear-gradient(135deg, #f43f5e, #e11d48);
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

.shadow-rose {
  box-shadow: 0 8px 20px -6px rgba(244, 63, 94, 0.18);
}

.unified-table-chip {
  border-radius: 6px !important;
  font-weight: 700 !important;
}
</style>
