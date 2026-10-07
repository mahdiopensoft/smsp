<template>
  <div class="qb-submission-detail-v4">
    <!-- Header Controls -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center gap-3">
        <custom-btn
          is-icon
          icon="arrow-right"
          variant="tonal"
          color="primary"
          :click="() => $router.push('/omr-submissions')"
        />
        <v-avatar size="44" color="primary" variant="tonal" class="rounded-xl">
          <v-icon size="24">mdi-file-document-check-outline</v-icon>
        </v-avatar>
        <div>
          <h2 class="text-h5 font-weight-black mb-1">تفاصيل تصحيح ورقة الإجابة</h2>
          <span class="text-caption text-medium-emphasis">
            عرض وتحليل نتائج خط المعالجة الهجين والتحقق بالذكاء الاصطناعي
          </span>
        </div>
      </div>

      <div class="d-flex align-center gap-2">
        <custom-btn
          label="إعادة المعالجة ضوئياً"
          icon="mdi-refresh"
          color="warning"
          variant="tonal"
          class="font-weight-bold"
          :loading="reprocessing"
          :click="reprocessSheet"
        />
        <custom-btn
          label="تعديل واعتماد الدرجات"
          icon="mdi-pencil-outline"
          color="primary"
          class="font-weight-bold"
          :click="openEditDialog"
        />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center pa-12">
      <v-progress-circular indeterminate color="primary" size="48" />
      <div class="text-caption mt-3 text-medium-emphasis">جاري تحميل تفاصيل الورقة...</div>
    </div>

    <div v-else-if="submission">
      <!-- Top Stats Overview Bar -->
      <v-row class="mb-6">
        <!-- Total Score -->
        <v-col cols="12" sm="6" md="3">
          <div class="stat-glass-card pa-5 rounded-xl shadow-emerald">
            <div class="d-flex align-center justify-space-between mb-3">
              <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">الدرجة الكلية</span>
              <div class="stat-icon-wrapper bg-emerald-gradient">
                <v-icon color="white" size="22">mdi-check-decagram</v-icon>
              </div>
            </div>
            <div class="stat-value text-h3 font-weight-black text-emerald mb-1">
              {{ submission.total_score != null ? submission.total_score : '—' }}
            </div>
            <div class="stat-footer border-t pt-2 mt-2 text-caption text-medium-emphasis">
              <span>خيارات: {{ submission.mcq_score || 0 }} | مقالي: {{ submission.essay_score || 0 }}</span>
            </div>
          </div>
        </v-col>

        <!-- Confidence Index -->
        <v-col cols="12" sm="6" md="3">
          <div class="stat-glass-card pa-5 rounded-xl shadow-indigo">
            <div class="d-flex align-center justify-space-between mb-3">
              <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">مؤشر الثقة الإجمالي</span>
              <div class="stat-icon-wrapper bg-indigo-gradient">
                <v-icon color="white" size="22">mdi-brain</v-icon>
              </div>
            </div>
            <div class="stat-value text-h3 font-weight-black text-indigo mb-1">
              {{ submission.overall_confidence ? (submission.overall_confidence * 100).toFixed(0) + '%' : '—' }}
            </div>
            <div class="stat-footer border-t pt-2 mt-2 text-caption text-medium-emphasis">
              <span>تحقق شبكة CNN والـ OMR</span>
            </div>
          </div>
        </v-col>

        <!-- Processing Time -->
        <v-col cols="12" sm="6" md="3">
          <div class="stat-glass-card pa-5 rounded-xl shadow-amber">
            <div class="d-flex align-center justify-space-between mb-3">
              <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">زمن المعالجة الضوئية</span>
              <div class="stat-icon-wrapper bg-amber-gradient">
                <v-icon color="white" size="22">mdi-timer-outline</v-icon>
              </div>
            </div>
            <div class="stat-value text-h3 font-weight-black text-amber mb-1">
              {{ submission.processing_time_ms ? (submission.processing_time_ms / 1000).toFixed(2) + ' ث' : '—' }}
            </div>
            <div class="stat-footer border-t pt-2 mt-2 text-caption text-medium-emphasis">
              <span>محاذاة وقراءة وتصحيح</span>
            </div>
          </div>
        </v-col>

        <!-- Status -->
        <v-col cols="12" sm="6" md="3">
          <div class="stat-glass-card pa-5 rounded-xl shadow-rose">
            <div class="d-flex align-center justify-space-between mb-3">
              <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">حالة الورقة</span>
              <div class="stat-icon-wrapper bg-rose-gradient">
                <v-icon color="white" size="22">mdi-list-status</v-icon>
              </div>
            </div>
            <div class="stat-value text-h4 font-weight-black mb-1">
              <v-chip :color="getStatusColor(submission.status)" variant="flat" class="font-weight-bold text-white">
                {{ submission.status_display || submission.status }}
              </v-chip>
            </div>
            <div class="stat-footer border-t pt-2 mt-2 text-caption text-medium-emphasis">
              <span>معرف السجل: #{{ submission.id }}</span>
            </div>
          </div>
        </v-col>
      </v-row>

      <v-row class="align-stretch">
        <!-- Right Column: Sheet Visualizer & Overlay -->
        <v-col cols="12" md="6">
          <v-card elevation="0" class="main-card pa-5 rounded-2xl border h-100 d-flex flex-column justify-space-between">
            <div>
              <div class="d-flex align-center justify-space-between mb-4">
                <div class="d-flex align-center gap-2">
                  <v-icon color="primary">mdi-image-filter-center-focus</v-icon>
                  <h3 class="text-subtitle-1 font-weight-black mb-0">ورقة الإجابة المصححة</h3>
                </div>

                <div class="d-flex align-center gap-2">
                  <v-chip v-if="submission.aligned_image" color="success" size="small" variant="tonal" class="font-weight-bold">
                    <v-icon start size="14">mdi-check-all</v-icon>
                    محاذاة صحيحة
                  </v-chip>
                  <v-chip v-else color="warning" size="small" variant="tonal" class="font-weight-bold">
                    صورة أصلية
                  </v-chip>

                  <custom-btn
                    :label="showOverlays ? 'إخفاء التظليل' : 'إظهار التظليل'"
                    :icon="showOverlays ? 'mdi-eye-off' : 'mdi-eye'"
                    size="small"
                    variant="tonal"
                    color="indigo"
                    class="font-weight-bold"
                    :click="() => showOverlays = !showOverlays"
                  />
                </div>
              </div>

              <!-- Visualizer Wrapper -->
              <div class="visualizer-wrapper bg-slate-900 rounded-xl pa-2 text-center position-relative overflow-hidden">
                <div class="image-relative-container position-relative d-inline-block">
                  <img
                    :src="getMediaUrl(submission.aligned_image || submission.original_image)"
                    alt="Student Answer Sheet"
                    class="sheet-img rounded-lg d-block w-100"
                    style="max-height: 650px; object-fit: contain;"
                  />

                  <!-- Bubble overlays mapped onto the image -->
                  <template v-if="showOverlays">
                    <div v-for="q in mcqQuestions" :key="'overlay-' + q.question_id">
                      <div
                        v-for="choice in getChoicesForQuestion(q.question_id)"
                        :key="'choice-' + choice.bubble_id"
                        class="image-bubble-overlay"
                        :class="getOverlayClass(q, choice.choice)"
                        :style="getOverlayStyle(choice.bubble_region)"
                        :title="'سؤال ' + q.question_id + ' - خيار ' + choice.choice"
                        @mouseenter="hoveredQ = q.question_id"
                        @mouseleave="hoveredQ = null"
                      >
                        <span class="overlay-letter">{{ choice.choice }}</span>
                      </div>
                    </div>
                  </template>
                </div>
              </div>
            </div>
          </v-card>
        </v-col>

        <!-- Left Column: Student Data, Pipeline, & Detailed Question Scores -->
        <v-col cols="12" md="6">
          <!-- Student & Exam Meta Card -->
          <v-card elevation="0" class="main-card pa-5 rounded-2xl border mb-4">
            <div class="d-flex align-center justify-space-between mb-3 border-b pb-2">
              <h3 class="text-subtitle-1 font-weight-black mb-0">بيانات الطالب والاختبار</h3>
              <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                رقم الجلوس: {{ submission.seat_number }}
              </v-chip>
            </div>

            <v-row dense>
              <v-col cols="12" sm="6">
                <div class="text-caption text-medium-emphasis">اسم الطالب:</div>
                <div class="text-body-2 font-weight-bold text-primary">{{ submission.student_name }}</div>
              </v-col>
              <v-col cols="12" sm="6">
                <div class="text-caption text-medium-emphasis">عنوان الاختبار:</div>
                <div class="text-body-2 font-weight-bold">{{ submission.exam_title }}</div>
              </v-col>
              <v-col cols="12" sm="6" class="mt-2">
                <div class="text-caption text-medium-emphasis">المادة الدراسية:</div>
                <div class="text-body-2 font-weight-medium">{{ submission.subject_name || '-' }}</div>
              </v-col>
              <v-col cols="12" sm="6" class="mt-2">
                <div class="text-caption text-medium-emphasis">النموذج:</div>
                <div class="text-body-2 font-weight-medium">{{ submission.exam_version_code || 'نموذج رئيسي' }}</div>
              </v-col>
            </v-row>
          </v-card>

          <!-- Pipeline Stepper Status -->
          <v-card elevation="0" class="main-card pa-5 rounded-2xl border mb-4">
            <h3 class="text-subtitle-1 font-weight-black mb-3">خطوات المعالجة الهجينة (Pipeline)</h3>
            <v-timeline density="compact" side="end">
              <!-- Step 1 -->
              <v-timeline-item dot-color="success" size="small">
                <div class="font-weight-bold text-body-2">1. المحاذاة الهندسية (Perspective Alignment)</div>
                <div class="text-caption text-medium-emphasis">تمت المحاذاة وإسقاط المنظور باستخدام علامات الارتكاز الأربعة</div>
              </v-timeline-item>

              <!-- Step 2 -->
              <v-timeline-item dot-color="success" size="small">
                <div class="font-weight-bold text-body-2">2. مطابقة القالب وتحديد الدوائر (Layout Mapping)</div>
                <div class="text-caption text-medium-emphasis">مطابقة إحداثيات القالب الهندسي واستخراج مناطق التظليل</div>
              </v-timeline-item>

              <!-- Step 3 -->
              <v-timeline-item dot-color="primary" size="small">
                <div class="font-weight-bold text-body-2">3. قراءة التظليل والتحقق الذكي (OMR + AI Verification)</div>
                <div class="text-caption text-medium-emphasis">تحليل كثافة التظليل بالـ OpenCV وتدقيق الالتباس بشبكة CNN</div>
              </v-timeline-item>

              <!-- Step 4 -->
              <v-timeline-item dot-color="indigo" size="small">
                <div class="font-weight-bold text-body-2">4. احتساب الدرجات والاعتماد الأكاديمي</div>
                <div class="text-caption text-medium-emphasis">المقارنة مع مفتاح الإجابة واعتماد النتيجة النهائية</div>
              </v-timeline-item>
            </v-timeline>
          </v-card>

          <!-- Detailed Questions Breakdown -->
          <v-card elevation="0" class="main-card pa-5 rounded-2xl border">
            <div class="d-flex align-center justify-space-between mb-3 border-b pb-2">
              <h3 class="text-subtitle-1 font-weight-black mb-0">نتائج الأسئلة التفصيلية</h3>
              <v-chip size="small" color="secondary" variant="tonal">
                {{ mcqQuestions.length }} سؤال خيارات
              </v-chip>
            </div>

            <v-table class="border rounded-xl">
              <thead>
                <tr class="bg-slate-50">
                  <th class="pa-2 font-weight-bold text-center">السؤال</th>
                  <th class="pa-2 font-weight-bold text-center">إجابة الطالب</th>
                  <th class="pa-2 font-weight-bold text-center">الإجابة النموذجية</th>
                  <th class="pa-2 font-weight-bold text-center">النتيجة</th>
                  <th class="pa-2 font-weight-bold text-center">الثقة</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="q in mcqQuestions"
                  :key="'detail-q-' + q.question_id"
                  :class="{ 'bg-primary-lighten-5': hoveredQ === q.question_id }"
                  @mouseenter="hoveredQ = q.question_id"
                  @mouseleave="hoveredQ = null"
                >
                  <td class="pa-2 text-center font-weight-bold">سـ {{ q.question_id }}</td>
                  <td class="pa-2 text-center">
                    <v-chip
                      size="small"
                      rounded="md"
                      :color="isTrueVariant(q.marked_choice) ? 'success' : isFalseVariant(q.marked_choice) ? 'error' : q.marked_choice ? 'primary' : 'grey'"
                      variant="tonal"
                      class="font-weight-bold"
                    >
                      <v-icon v-if="isTrueVariant(q.marked_choice)" start size="13">mdi-check</v-icon>
                      <v-icon v-else-if="isFalseVariant(q.marked_choice)" start size="13">mdi-close</v-icon>
                      {{ q.marked_choice || 'بدون إجابة' }}
                    </v-chip>
                  </td>
                  <td class="pa-2 text-center">
                    <v-chip
                      size="small"
                      rounded="md"
                      :color="isTrueVariant(q.correct_choice) ? 'success' : isFalseVariant(q.correct_choice) ? 'error' : 'teal'"
                      variant="tonal"
                      class="font-weight-bold"
                    >
                      <v-icon v-if="isTrueVariant(q.correct_choice)" start size="13">mdi-check</v-icon>
                      <v-icon v-else-if="isFalseVariant(q.correct_choice)" start size="13">mdi-close</v-icon>
                      {{ q.correct_choice }}
                    </v-chip>
                  </td>
                  <td class="pa-2 text-center">
                    <v-chip
                      size="small"
                      rounded="md"
                      :color="q.is_correct ? 'success' : 'error'"
                      variant="tonal"
                      class="font-weight-bold"
                    >
                      <v-icon start size="14">{{ q.is_correct ? 'mdi-check-circle' : 'mdi-close-circle' }}</v-icon>
                      {{ q.is_correct ? 'صحيحة' : 'خاطئة' }}
                    </v-chip>
                  </td>
                  <td class="pa-2 text-center text-caption font-weight-bold">
                    {{ (q.final_confidence * 100).toFixed(0) }}%
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Edit / Manual Review Dialog (CustomDialog Component) -->
    <CustomDialog
      v-model="editDialog"
      width="560"
      title="تعديل درجات الورقة واعتمادها"
      :subTitle="submission ? `طالب: ${submission.student_name} • رقم الجلوس: ${submission.seat_number}` : ''"
    >
      <v-row class="mb-3">
        <v-col cols="12" md="6">
          <v-text-field
            v-model.number="editForm.mcq_score"
            label="درجة أسئلة الخيارات (MCQ) *"
            type="number"
            variant="outlined"
            density="compact"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model.number="editForm.essay_score"
            label="درجة الأسئلة المقالية (Essay) *"
            type="number"
            variant="outlined"
            density="compact"
          />
        </v-col>
        <v-col cols="12">
          <v-select
            v-model="editForm.status"
            :items="[
              { title: 'مكتمل ومعتمد (Completed)', value: 'completed' },
              { title: 'تمت المراجعة (Reviewed)', value: 'reviewed' },
              { title: 'يحتاج مراجعة (Needs Review)', value: 'needs_review' }
            ]"
            label="الحالة بعد الحفظ *"
            variant="outlined"
            density="compact"
          />
        </v-col>
      </v-row>

      <template #actions>
        <custom-btn
          type="cancel"
          :click="() => editDialog = false"
          variant="text"
          label="إلغاء"
          class="font-weight-bold"
        />
        <custom-btn
          type="add"
          :click="saveReview"
          :loading="saving"
          color="primary"
          label="حفظ واعتماد الدرجات"
          class="font-weight-bold ms-auto"
        />
      </template>
    </CustomDialog>
  </div>
</template>

<script>
import { submissionsAPI } from '@/services/omr/endpoints'

export default {
  name: 'OMRSubmissionDetailView',

  data() {
    return {
      loading: false,
      reprocessing: false,
      saving: false,

      submission: null,
      hoveredQ: null,
      showOverlays: true,

      paperWidth: 210.0,
      paperHeight: 297.0,

      editDialog: false,
      editForm: {
        mcq_score: 0,
        essay_score: 0,
        status: 'completed',
      },
    }
  },

  computed: {
    mcqQuestions() {
      return this.submission?.omr_result?.data?.questions || []
    },
  },

  methods: {
    async loadSubmission() {
      const id = this.$route.params.id
      if (!id) return
      this.loading = true
      try {
        const res = await submissionsAPI.get(id)
        this.submission = res.data || res
      } catch (err) {
        console.error('Error fetching submission details:', err)
      } finally {
        this.loading = false
      }
    },

    getMediaUrl(path) {
      if (!path) return ''
      if (path.startsWith('http')) return path
      return `http://localhost:8000${path}`
    },

    getStatusColor(status) {
      const map = {
        completed: 'success',
        reviewed: 'teal',
        needs_review: 'warning',
        failed: 'error',
        pending: 'grey',
      }
      return map[status] || 'grey'
    },

    getChoicesForQuestion(qId) {
      const layoutQuestions = this.submission?.layout_result?.data?.detected_regions?.mcq_questions || []
      const found = layoutQuestions.find(q => String(q.question_id) === String(qId))
      if (found && found.choices) return found.choices
      return []
    },

    getOverlayStyle(reg) {
      if (!reg) return {}
      const w = reg.width_mm || 4.5
      const h = reg.height_mm || 4.5
      const cx = reg.dx_mm + w / 2.0
      const cy = reg.dy_mm + h / 2.0
      return {
        left: `${(cx / this.paperWidth) * 100}%`,
        top: `${(cy / this.paperHeight) * 100}%`,
        width: `${(w / this.paperWidth) * 100}%`,
        height: `${(h / this.paperHeight) * 100}%`,
      }
    },

    getOverlayClass(q, letter) {
      if (q.marked_choice === letter) {
        return q.is_correct ? 'overlay-selected-correct' : 'overlay-selected-incorrect'
      }
      if (q.correct_choice === letter) {
        return 'overlay-correct-key'
      }
      return 'overlay-normal'
    },

    openEditDialog() {
      if (!this.submission) return
      this.editForm = {
        mcq_score: Number(this.submission.mcq_score) || 0,
        essay_score: Number(this.submission.essay_score) || 0,
        status: this.submission.status === 'needs_review' ? 'completed' : this.submission.status,
      }
      this.editDialog = true
    },

    async saveReview() {
      if (!this.submission) return
      this.saving = true
      try {
        await submissionsAPI.updateReview(this.submission.id, this.editForm)
        this.editDialog = false
        await this.loadSubmission()
      } catch (err) {
        console.error('Error saving review:', err)
      } finally {
        this.saving = false
      }
    },

    isTrueVariant(val) {
      if (val === null || val === undefined) return false
      const s = String(val).trim().toLowerCase()
      return s === 'صح' || s === 'ص' || s === 'true' || s === 't' || s === '1' || s === 'yes'
    },

    isFalseVariant(val) {
      if (val === null || val === undefined) return false
      const s = String(val).trim().toLowerCase()
      return s === 'خطأ' || s === 'خطا' || s === 'خ' || s === 'false' || s === 'f' || s === '2' || s === 'no'
    },

    async reprocessSheet() {
      if (!this.submission) return
      this.reprocessing = true
      try {
        await submissionsAPI.reprocess(this.submission.id)
        await this.loadSubmission()
      } catch (err) {
        console.error('Error reprocessing sheet:', err)
      } finally {
        this.reprocessing = false
      }
    },
  },

  mounted() {
    this.loadSubmission()
  },
}
</script>

<style scoped>
:deep(.v-chip) {
  border-radius: 6px !important;
  font-family: inherit;
  letter-spacing: 0;
}

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

/* Image overlays */
.image-bubble-overlay {
  position: absolute;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;
}

.overlay-selected-correct {
  background: rgba(16, 185, 129, 0.4);
  border: 2px solid #10b981;
  color: white;
}

.overlay-selected-incorrect {
  background: rgba(239, 68, 68, 0.45);
  border: 2px solid #ef4444;
  color: white;
}

.overlay-correct-key {
  border: 2px dashed #10b981;
  color: #10b981;
  background: rgba(16, 185, 129, 0.15);
}

.overlay-normal {
  border: 1px solid rgba(255, 255, 255, 0.4);
  background: rgba(0, 0, 0, 0.15);
  color: white;
}
</style>
