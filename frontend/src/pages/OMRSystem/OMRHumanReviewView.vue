<template>
  <div class="qb-human-review-v4 pa-4 pa-md-6">
    <!-- Header -->
    <div class="d-flex align-center justify-space-between mb-6">
      <div class="d-flex align-center">
        <v-avatar size="44" color="primary" variant="tonal" class="me-3 rounded-xl">
          <v-icon size="24">mdi-account-eye-outline</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">المراجعة والتدقيق البشري</h1>
          <p class="text-caption text-medium-emphasis mb-0">أوراق الإجابة ذات درجات الثقة المنخفضة أو التظليل الملتبس التي تتطلب تدقيقاً وتحققاً.</p>
        </div>
      </div>

      <div>
        <custom-btn
          label="تحديث البيانات"
          icon="refresh"
          variant="tonal"
          color="primary"
          :loading="loading"
          :click="fetchData"
        />
      </div>
    </div>

    <!-- ── OMR Workflow Stepper (المرحلة 5: المراجعة والتدقيق البشري) ── -->
    <omr-workflow-bar :active-step="5" :exam-id="selectedExam" />

    <!-- Filters Control Bar (Standard filter-fields) -->
    <filter-fields label="خيارات تصفية أوراق المراجعة والتدقيق" class="main-card border-0 pa-5 rounded-2xl mb-6">
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
          />
          <auto-list
            v-model="filterInstituteSubject"
            name="InstituteSubject"
            :param="instituteSubjectParam"
            placeholder="المادة الدراسية للمعهد"
            cols="3"
            :add="false"
          />
        </template>

        <!-- Common Subject Filter (School or All) -->
        <auto-list
          v-if="filterInstitutionType === 'school' || filterInstitutionType === 'all'"
          v-model="filterSubject"
          name="Subject"
          placeholder="المادة الدراسية"
          cols="3"
          :add="false"
        />

        <!-- Exam Filter -->
        <auto-list
          v-model="filterExam"
          name="Exam"
          :param="examFilterParam"
          placeholder="الاختبار"
          cols="3"
          :add="false"
          @update:model-value="fetchData"
        />

        <!-- Status Filter -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterStatus"
            :items="statusOptions"
            item-title="title"
            item-value="value"
            label="حالة المراجعة"
            placeholder="حالة المراجعة"
            prepend-inner-icon="mdi-list-status"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @update:model-value="fetchData"
          />
        </v-col>

        <!-- Search Query -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="searchQuery"
            label="اسم الطالب أو رقم القيد"
            placeholder="بحث برقم السجل أو الطالب..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @keyup.enter="fetchData"
          />
        </v-col>

        <!-- Filter Action Buttons (Standard style matching /levels) -->
        <v-col cols="12" sm="6" md="3" class="d-flex align-center gap-2">
          <custom-btn
            type="show"
            label="تصفية"
            color="primary"
            class="font-weight-bold flex-grow-1 mb-6"
            :click="fetchData"
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

    <!-- Unified Data Table (matching standard /levels) -->
    <div class="main-card rounded-2xl overflow-hidden mb-8">
      <custom-data-table
        v-bind="{
          items: tableItems,
          getData,
          headers,
        }"
        :customLoading="loading"
        :hasFilter="false"
        :log="false"
        :restore="false"
      >
        <template v-slot:item-slot="{ item, key }">
          <!-- Student Info -->
          <template v-if="key === 'student_info'">
            <div class="py-1">
              <div class="font-weight-bold text-body-2 text-on-surface">
                {{ item.student_name || ('ورقة #' + item.id) }}
              </div>
              <div v-if="item.seat_number" class="text-caption text-medium-emphasis mt-1">
                {{ item.institution_type === 'university' ? 'رقم القيد:' : 'رقم الجلوس:' }}
                <span class="font-weight-bold text-on-surface ms-1">{{ item.seat_number }}</span>
              </div>
            </div>
          </template>

          <!-- Exam -->
          <template v-else-if="key === 'exam_title'">
            <div class="py-1">
              <div class="text-body-2 font-weight-medium text-truncate" style="max-width: 250px;">
                {{ item.exam_title || 'اختبار عام' }}
              </div>
              <div class="text-caption text-medium-emphasis mt-1">
                {{ item.institution_type === 'university' ? 'جامعي' : 'مدرسي' }}
              </div>
            </div>
          </template>

          <!-- Confidence -->
          <template v-else-if="key === 'confidence'">
            <v-chip
              size="small"
              :color="item.confidence >= 0.85 ? 'success' : 'warning'"
              variant="tonal"
              class="font-weight-bold unified-table-chip"
            >
              {{ Math.round((item.confidence || 0) * 100) }}%
            </v-chip>
          </template>

          <!-- Ambiguous questions -->
          <template v-else-if="key === 'ambiguous_count'">
            <v-chip
              v-if="item.ambiguous_count > 0"
              size="small"
              color="error"
              variant="tonal"
              class="font-weight-bold unified-table-chip"
            >
              <v-icon start size="13">mdi-alert-circle-outline</v-icon>
              {{ item.ambiguous_count }} أسئلة
            </v-chip>
            <span v-else class="text-medium-emphasis text-caption">-</span>
          </template>

          <!-- Score -->
          <template v-else-if="key === 'score'">
            <span class="font-weight-bold text-body-2">
              {{ item.mcq_score != null ? item.mcq_score : 0 }} / {{ item.mcq_max_score != null ? item.mcq_max_score : 0 }}
            </span>
          </template>

          <!-- Status -->
          <template v-else-if="key === 'status'">
            <v-chip
              size="small"
              :color="item.status === 'verified' ? 'success' : 'warning'"
              variant="tonal"
              class="font-weight-bold unified-table-chip"
            >
              <v-icon start size="14">{{ item.status === 'verified' ? 'mdi-check-circle' : 'mdi-clock-outline' }}</v-icon>
              {{ item.status === 'verified' ? 'معتمد' : 'قيد التدقيق' }}
            </v-chip>
          </template>

          <!-- Actions -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-1">
              <v-btn
                size="small"
                color="primary"
                variant="tonal"
                class="font-weight-bold px-2"
                prepend-icon="mdi-file-find-outline"
                @click="openReviewModal(item)"
              >
                تدقيق وتعديل
              </v-btn>
              <custom-btn
                v-if="item.status !== 'verified'"
                type="ok"
                is-icon
                label="اعتماد ومصادقة النتيجة"
                :click="() => approveSheet(item)"
              />
              <custom-btn
                v-else
                type="done"
                is-icon
                label="تم الاعتماد مسبقاً"
                disabled
              />
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>

    <!-- ── نافذة المراجعة والتدقيق وتعديل الإجابات الملتبسة ── -->
    <v-dialog v-model="reviewDialog" max-width="1000" scrollable>
      <v-card class="rounded-2xl overflow-hidden review-dialog-card" v-if="activeReviewSheet">
        <!-- Dialog Header - Bright, Clean & Modern (No black/dark background) -->
        <v-card-title class="d-flex align-center justify-space-between bg-white px-6 py-4 border-b dialog-header">
          <div class="d-flex align-center gap-3">
            <div class="dialog-icon-avatar">
              <v-icon size="24" color="primary">mdi-file-eye-outline</v-icon>
            </div>
            <div>
              <div class="d-flex align-center gap-2 flex-wrap">
                <h3 class="text-h6 font-weight-black text-slate-900 mb-0">
                  {{ activeReviewSheet.student_name || 'ورقة بدون اسم' }}
                </h3>
                <v-chip size="small" color="primary" variant="flat" class="font-weight-bold px-2">
                  {{ activeReviewSheet.seat_number ? (activeReviewSheet.institution_type === 'university' ? 'رقم القيد: ' : 'رقم الجلوس: ') + activeReviewSheet.seat_number : 'ورقة #' + activeReviewSheet.id }}
                </v-chip>
                <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold px-2">
                  النموذج: {{ activeReviewSheet.version_code || 'A' }}
                </v-chip>
              </div>
              <p class="text-caption text-slate-500 mb-0 mt-1">
                {{ activeReviewSheet.exam_title || 'اختبار عام' }} • نسبة الثقة: 
                <strong :class="(activeReviewSheet.confidence || 0) >= 0.85 ? 'text-success' : 'text-warning'">
                  {{ Math.round((activeReviewSheet.confidence || 0) * 100) }}%
                </strong>
              </p>
            </div>
          </div>

          <div class="d-flex align-center gap-3">
            <div class="header-score-pill d-flex align-center gap-2 px-3 py-1.5 rounded-xl">
              <v-icon size="18" color="success">mdi-check-decagram</v-icon>
              <div class="d-flex flex-column text-end">
                <span class="text-caption text-slate-500 font-weight-medium" style="font-size: 10px; line-height: 1;">الدرجة الحالية</span>
                <span class="font-weight-black text-body-1 text-success" style="line-height: 1.2;">
                  {{ activeReviewSheet.mcq_score != null ? activeReviewSheet.mcq_score : 0 }} <span class="text-caption text-slate-400">/ {{ activeReviewSheet.mcq_max_score || 0 }}</span>
                </span>
              </div>
            </div>
            <v-btn icon="mdi-close" variant="text" size="small" color="grey-darken-1" @click="reviewDialog = false" />
          </div>
        </v-card-title>

        <v-card-text class="pa-6 dialog-body-content" style="max-height: 72vh; background-color: #f8fafc;">
          <!-- تنبيه الأسئلة الملتبسة -->
          <v-alert
            v-if="dialogCounts.ambiguous > 0"
            type="warning"
            variant="tonal"
            density="compact"
            class="mb-4 rounded-xl font-weight-bold border-warning"
          >
            <div class="d-flex align-center justify-space-between flex-wrap gap-2">
              <div class="d-flex align-center gap-2">
                <v-icon size="20">mdi-alert-circle</v-icon>
                <span>يوجد <strong>{{ dialogCounts.ambiguous }}</strong> أسئلة بها تظليل ملتبس أو غير مؤكد يتطلب فحص وتأكيد المدقق.</span>
              </div>
              <v-btn
                size="x-small"
                variant="flat"
                color="warning"
                class="font-weight-bold"
                @click="dialogQuestionFilter = 'ambiguous'"
              >
                تصفية الأسئلة الملتبسة فقط
              </v-btn>
            </div>
          </v-alert>

          <!-- Sheet image preview if present -->
          <div v-if="activeReviewSheet.sheet_image" class="mb-4 text-center">
            <v-expansion-panels variant="accordion">
              <v-expansion-panel class="rounded-xl border border-slate-200">
                <v-expansion-panel-title class="font-weight-bold text-slate-700">
                  <v-icon start size="18" color="primary">mdi-image-search-outline</v-icon>
                  معاينة الصورة الأصلية للورقة المصححة ضوئياً
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <div class="image-preview-wrapper pa-2 bg-white rounded-lg border text-center">
                    <img :src="activeReviewSheet.sheet_image" alt="Scanned OMR Sheet" style="max-width: 100%; max-height: 500px; object-fit: contain; border-radius: 8px;" />
                  </div>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </div>

          <!-- شريط التصفية والتحكم السريع في الأسئلة -->
          <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-4 bg-white pa-3 rounded-xl border border-slate-200">
            <div class="d-flex align-center gap-2">
              <v-icon size="20" color="primary">mdi-format-list-checks</v-icon>
              <span class="text-subtitle-2 font-weight-black text-slate-800">
                سجل إجابات وتظليلات الطالب ({{ dialogCounts.all }} سؤال):
              </span>
            </div>

            <v-btn-toggle
              v-model="dialogQuestionFilter"
              mandatory
              density="compact"
              rounded="lg"
              color="primary"
              class="dialog-filter-toggle"
            >
              <v-btn value="all" size="x-small" class="font-weight-bold">
                الكل ({{ dialogCounts.all }})
              </v-btn>
              <v-btn
                v-if="dialogCounts.ambiguous > 0"
                value="ambiguous"
                size="x-small"
                color="warning"
                class="font-weight-bold"
              >
                <v-icon start size="12">mdi-alert</v-icon>
                الملتبسة ({{ dialogCounts.ambiguous }})
              </v-btn>
              <v-btn
                value="wrong"
                size="x-small"
                color="error"
                class="font-weight-bold"
              >
                <v-icon start size="12">mdi-close-circle</v-icon>
                الخاطئة ({{ dialogCounts.wrong }})
              </v-btn>
              <v-btn
                value="correct"
                size="x-small"
                color="success"
                class="font-weight-bold"
              >
                <v-icon start size="12">mdi-check-circle</v-icon>
                الصحيحة ({{ dialogCounts.correct }})
              </v-btn>
              <v-btn
                value="empty"
                size="x-small"
                class="font-weight-bold text-slate-600"
              >
                <v-icon start size="12">mdi-circle-outline</v-icon>
                الفارغة ({{ dialogCounts.empty }})
              </v-btn>
            </v-btn-toggle>
          </div>

          <!-- بطاقات الأسئلة OMR Cards Grid -->
          <v-row dense>
            <v-col
              v-for="q in filteredDialogQuestions"
              :key="q.id || q.question_number"
              cols="12"
              md="6"
            >
              <div
                class="review-question-card pa-3 mb-2"
                :class="getCardStatusClass(q)"
              >
                <!-- Card Header -->
                <div class="d-flex align-center justify-space-between mb-2">
                  <div class="d-flex align-center gap-2">
                    <div class="q-number-circle">
                      {{ q.question_number }}
                    </div>
                    <span class="font-weight-black text-body-2 text-slate-800">
                      السؤال {{ q.question_number }}
                    </span>
                    <v-chip
                      size="x-small"
                      :color="getStatusChipColor(q)"
                      variant="flat"
                      class="font-weight-bold px-2 rounded-md"
                    >
                      <v-icon start size="12">{{ getStatusChipIcon(q) }}</v-icon>
                      {{ getStatusChipText(q) }}
                    </v-chip>
                    <v-chip
                      v-if="q.bubble_state === 'ambiguous' || (q.final_confidence && q.final_confidence < 0.7)"
                      size="x-small"
                      color="warning"
                      variant="flat"
                      class="font-weight-black px-2 rounded-md"
                    >
                      ملتبس
                    </v-chip>
                  </div>

                  <!-- Model Answer Tag -->
                  <div class="model-key-pill d-flex align-center gap-1">
                    <span class="text-caption text-slate-500 font-weight-medium">النموذجية:</span>
                    <span class="model-key-char">
                      {{ q.correct_choice || '—' }}
                    </span>
                  </div>
                </div>

                <!-- Divider -->
                <div class="card-inner-divider my-2"></div>

                <!-- Interactive OMR Bubbles Row -->
                <div class="d-flex align-center justify-space-between gap-1 flex-wrap pt-1">
                  <div class="d-flex align-center gap-2">
                    <span class="text-caption font-weight-bold text-slate-600">تظليل الطالب:</span>
                    <div class="bubbles-row d-flex align-center gap-1.5">
                      <button
                        v-for="opt in getQuestionOptions(q)"
                        :key="opt"
                        type="button"
                        class="omr-bubble-interactive"
                        :class="getBubbleClass(q, opt)"
                        :disabled="overridingLoading === `${q.question_number}_${opt}`"
                        :title="getBubbleTooltip(q, opt)"
                        @click="overrideQuestionChoice(q, opt)"
                      >
                        <v-progress-circular
                          v-if="overridingLoading === `${q.question_number}_${opt}`"
                          size="14"
                          width="2"
                          indeterminate
                          color="primary"
                        />
                        <span v-else>{{ opt }}</span>
                      </button>

                      <!-- خيار مسح التظليل -->
                      <button
                        type="button"
                        class="omr-eraser-btn ms-1"
                        :class="{ 'opacity-50 pointer-events-none': overridingLoading === `${q.question_number}_clear` }"
                        title="مسح إجابة هذا السؤال (جعله بدون إجابة)"
                        @click="overrideQuestionChoice(q, '')"
                      >
                        <v-progress-circular
                          v-if="overridingLoading === `${q.question_number}_clear`"
                          size="12"
                          width="2"
                          indeterminate
                          color="error"
                        />
                        <v-icon v-else size="14" color="error">mdi-eraser</v-icon>
                      </button>
                    </div>
                  </div>

                  <!-- Question Score & Confidence -->
                  <div class="d-flex align-center gap-2">
                    <span class="text-caption font-weight-bold" :class="q.is_correct ? 'text-success' : 'text-slate-400'">
                      الدرجة: {{ q.is_correct ? (q.marks_awarded != null && Number(q.marks_awarded) > 0 ? Number(q.marks_awarded).toFixed(1).replace('.0', '') : '1') : '0' }}
                    </span>
                    <span v-if="q.final_confidence" class="text-caption text-slate-400" style="font-size: 10px;">
                      ({{ Math.round(q.final_confidence * 100) }}%)
                    </span>
                  </div>
                </div>
              </div>
            </v-col>

            <!-- حالة عدم وجود نتائج للفلتر -->
            <v-col cols="12" v-if="filteredDialogQuestions.length === 0">
              <div class="text-center pa-8 bg-white rounded-xl border border-slate-200">
                <v-icon size="42" color="grey-lighten-1" class="mb-2">mdi-filter-off-outline</v-icon>
                <div class="text-body-2 font-weight-bold text-slate-700">لا توجد أسئلة تطابق الفلتر المحدد</div>
                <div class="text-caption text-slate-400 mt-1">اختر "الكل" لعرض كافة أسئلة الورقة</div>
              </div>
            </v-col>
          </v-row>
        </v-card-text>

        <!-- Dialog Footer - Bright, Clean Slate -->
        <v-card-actions class="px-6 py-4 bg-white border-t dialog-footer" style="background-color: #ffffff !important; border-top: 1px solid #e2e8f0 !important;">
          <v-btn
            variant="text"
            color="grey-darken-2"
            class="font-weight-bold px-4"
            @click="reviewDialog = false"
          >
            إغلاق النافذة
          </v-btn>
          <v-spacer />
          <v-btn
            color="success"
            rounded="lg"
            elevation="1"
            class="font-weight-black px-6"
            prepend-icon="mdi-check-decagram"
            :loading="approvingLoading"
            @click="approveCurrentSheet"
          >
            اعتماد ومصادقة الورقة نهائياً
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, getCurrentInstance } from 'vue'
import { humanReviewAPI } from '@/services/omr/endpoints.js'

const { proxy } = getCurrentInstance()
const loading = ref(false)
const sheets = ref([])
const stats = ref({ pendingReview: 0, ambiguousSheets: 0, verifiedSheets: 0, totalSheets: 0 })

// Dialog & Override state
const reviewDialog = ref(false)
const activeReviewSheet = ref(null)
const overridingLoading = ref('')
const approvingLoading = ref(false)

// Table headers (Clean & Professional, with actions column)
const headers = computed(() => [
  { title: "الطالب ورقم الجلوس / القيد", key: "student_info", sortable: true },
  { title: "الاختبار", key: "exam_title", sortable: true },
  { title: "نسبة الثقة", key: "confidence", sortable: true, align: "center", width: "120px" },
  { title: "الأسئلة الملتبسة", key: "ambiguous_count", sortable: true, align: "center", width: "130px" },
  { title: "الدرجة المقدرة", key: "score", sortable: false, align: "center", width: "130px" },
  { title: "حالة المراجعة", key: "status", sortable: true, align: "center", width: "120px" },
  { title: "الإجراءات والتدقيق", key: "actions", sortable: false, align: "center", width: "180px" },
])

// Bound items for custom-data-table
const tableItems = computed(() => ({
  results: sheets.value,
  count: sheets.value.length,
  pagination: {
    count: sheets.value.length,
    total: sheets.value.length,
  },
}))

// Filters
const filterInstitutionType = ref('all')
const institutionTypeOptions = [
  { text: "الكل (مدارس وجامعات ومعاهد)", value: "all" },
  { text: "مدارس فقط", value: "school" },
  { text: "جامعات فقط", value: "university" },
  { text: "معاهد وتدريب مهني", value: "institute" },
]
const filterCollege = ref(null)
const filterDepartment = ref(null)
const filterSpecialization = ref(null)
const filterSemesterSubject = ref(null)
const filterInstituteField = ref(null)
const filterInstituteEducationSystem = ref(null)
const filterInstituteSpecialization = ref(null)
const filterInstituteSubject = ref(null)
const filterStage = ref(null)
const filterClassTrack = ref(null)
const filterSubject = ref(null)
const filterExam = ref(null)
const filterStatus = ref(null)
const searchQuery = ref('')

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

const examFilterParam = computed(() => {
  const p = {}
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
    p.institution_type = filterInstitutionType.value
  }
  if (filterInstitutionType.value === 'school') {
    if (filterClassTrack.value) p.class_track = filterClassTrack.value
    if (filterStage.value) p.stage = filterStage.value
    if (filterSubject.value) p.subject = filterSubject.value
  } else if (filterInstitutionType.value === 'university') {
    if (filterSemesterSubject.value) p.semester_subject = filterSemesterSubject.value
    if (filterSpecialization.value) p.specialization = filterSpecialization.value
    if (filterDepartment.value) p.department = filterDepartment.value
    if (filterCollege.value) p.college = filterCollege.value
  } else if (filterInstitutionType.value === 'institute') {
    if (filterInstituteField.value) p.institute_field = filterInstituteField.value
    if (filterInstituteEducationSystem.value) p.institute_education_system = filterInstituteEducationSystem.value
    if (filterInstituteSpecialization.value) p.institute_specialization = filterInstituteSpecialization.value
    if (filterInstituteSubject.value) p.institute_subject = filterInstituteSubject.value
  } else {
    if (filterSubject.value) p.subject = filterSubject.value
  }
  return Object.keys(p).length > 0 ? p : null
})

const statusOptions = [
  { title: 'كافة الحالات', value: null },
  { title: 'تتطلب تدقيق يدوي', value: 'pending' },
  { title: 'معتمدة ومحققة', value: 'verified' },
]

const onInstitutionTypeChange = () => {
  filterStage.value = null
  filterClassTrack.value = null
  filterCollege.value = null
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterInstituteField.value = null
  filterInstituteEducationSystem.value = null
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
  filterSubject.value = null
  filterExam.value = null
  fetchData()
}

const onCollegeChange = () => {
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
}

const onInstituteFieldChange = () => {
  filterInstituteEducationSystem.value = null
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
}

const onInstituteEducationSystemChange = () => {
  filterInstituteSpecialization.value = null
}

const onStageChange = () => {
  filterClassTrack.value = null
}

const resetFilters = () => {
  filterInstitutionType.value = 'all'
  filterCollege.value = null
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterInstituteField.value = null
  filterInstituteEducationSystem.value = null
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
  filterStage.value = null
  filterClassTrack.value = null
  filterSubject.value = null
  filterExam.value = null
  filterStatus.value = null
  searchQuery.value = ''
  fetchData()
}

const getData = async (params = {}) => {
  return await fetchData(params)
}

const fetchData = async () => {
  loading.value = true
  try {
    const queryParams = {
      institution_type: (filterInstitutionType.value && filterInstitutionType.value !== 'all') ? filterInstitutionType.value : undefined,
      college: filterCollege.value || undefined,
      department: filterDepartment.value || undefined,
      specialization: filterSpecialization.value || undefined,
      semester_subject: filterSemesterSubject.value || undefined,
      institute_field: filterInstituteField.value || undefined,
      institute_education_system: filterInstituteEducationSystem.value || undefined,
      institute_specialization: filterInstituteSpecialization.value || undefined,
      institute_subject: filterInstituteSubject.value || undefined,
      stage: filterStage.value || undefined,
      class_track: filterClassTrack.value || undefined,
      subject: filterSubject.value || undefined,
      exam: filterExam.value || undefined,
      status: filterStatus.value || undefined,
      search: searchQuery.value || undefined,
    }
    const [statsRes, listRes] = await Promise.all([
      humanReviewAPI.getStats(),
      humanReviewAPI.list(queryParams)
    ])
    stats.value = statsRes?.data || stats.value
    const results = listRes?.data?.results || listRes?.data || []
    sheets.value = Array.isArray(results) ? results : []
    return tableItems.value
  } catch (err) {
    console.error('Failed to load human review data', err)
    return { results: [], count: 0 }
  } finally {
    loading.value = false
  }
}

const approveSheet = async (sheet) => {
  try {
    await humanReviewAPI.approveReview(sheet.id)
    proxy.$alert('success', { message: 'تم اعتماد نتيجة ورقة الإجابة بنجاح' })
    await fetchData()
  } catch (err) {
    proxy.$alert('errorData', { message: 'فشل اعتماد الورقة' })
    console.error(err)
  }
}

// Dialog Question Filtering & Counts
const dialogQuestionFilter = ref('all')

const filteredDialogQuestions = computed(() => {
  const qs = activeReviewSheet.value?.questions || []
  if (dialogQuestionFilter.value === 'ambiguous') {
    return qs.filter(q => q.bubble_state === 'ambiguous' || (q.final_confidence && q.final_confidence < 0.7))
  }
  if (dialogQuestionFilter.value === 'wrong') {
    return qs.filter(q => q.is_correct === false && q.marked_choice)
  }
  if (dialogQuestionFilter.value === 'correct') {
    return qs.filter(q => q.is_correct === true)
  }
  if (dialogQuestionFilter.value === 'empty') {
    return qs.filter(q => !q.marked_choice)
  }
  return qs
})

const dialogCounts = computed(() => {
  const qs = activeReviewSheet.value?.questions || []
  return {
    all: qs.length,
    ambiguous: qs.filter(q => q.bubble_state === 'ambiguous' || (q.final_confidence && q.final_confidence < 0.7)).length,
    wrong: qs.filter(q => q.is_correct === false && q.marked_choice).length,
    correct: qs.filter(q => q.is_correct === true).length,
    empty: qs.filter(q => !q.marked_choice).length,
  }
})

const openReviewModal = (sheet) => {
  activeReviewSheet.value = { ...sheet }
  dialogQuestionFilter.value = 'all'
  reviewDialog.value = true
}

const normalizeChoiceValue = (val) => {
  if (!val) return ''
  const c = String(val).trim().toUpperCase()
  const map = {
    '1': 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E',
    'أ': 'A', 'ا': 'A', 'ب': 'B', 'ج': 'C', 'د': 'D', 'هـ': 'E', 'ه': 'E',
    'صح': 'A', 'ص': 'A', 'T': 'A', 'TRUE': 'A', '✓': 'A',
    'خطأ': 'B', 'خ': 'B', 'F': 'B', 'FALSE': 'B', '✗': 'B'
  }
  return map[c] || c
}

const getQuestionOptions = (q) => {
  if (!q) return ['1', '2', '3', '4']

  // 1. Check choice_confidences keys if present
  if (q.choice_confidences && typeof q.choice_confidences === 'object' && Object.keys(q.choice_confidences).length > 0) {
    const keys = Object.keys(q.choice_confidences)
    if (keys.every(k => !isNaN(Number(k)))) {
      return keys.sort((a, b) => Number(a) - Number(b))
    }
    return keys
  }

  // 2. Check darkness_values keys if present
  if (q.darkness_values && typeof q.darkness_values === 'object' && Object.keys(q.darkness_values).length > 0) {
    const keys = Object.keys(q.darkness_values)
    if (keys.every(k => !isNaN(Number(k)))) {
      return keys.sort((a, b) => Number(a) - Number(b))
    }
    return keys
  }

  // 3. Check choices array if provided
  if (Array.isArray(q.choices) && q.choices.length > 0) {
    return q.choices
  }

  // 4. Infer from correct_choice or marked_choice
  const ref = String(q.correct_choice || q.marked_choice || '').trim()
  if (['صح', 'خطأ', 'T', 'F', 'True', 'False', 'true', 'false'].includes(ref)) {
    return ['صح', 'خطأ']
  }
  if (['1', '2', '3', '4', '5'].includes(ref)) {
    return ['1', '2', '3', '4']
  }
  if (['أ', 'ب', 'ج', 'د', 'هـ'].includes(ref)) {
    return ['أ', 'ب', 'ج', 'د']
  }
  if (['A', 'B', 'C', 'D', 'E'].includes(ref)) {
    return ['A', 'B', 'C', 'D']
  }

  // Check if exam mostly uses numeric choices
  const allQs = activeReviewSheet.value?.questions || []
  const hasNumbers = allQs.some(item => ['1', '2', '3', '4'].includes(String(item.correct_choice || '').trim()))
  if (hasNumbers) {
    return ['1', '2', '3', '4']
  }

  return ['A', 'B', 'C', 'D']
}

const getBubbleClass = (q, opt) => {
  const isMarked = String(q.marked_choice || '').trim() === String(opt).trim()
  const isCorrectKey = String(q.correct_choice || '').trim() === String(opt).trim()

  if (isMarked) {
    return q.is_correct ? 'bubble-marked-correct' : 'bubble-marked-wrong'
  }
  if (isCorrectKey) {
    return 'bubble-model-key'
  }
  return 'bubble-default'
}

const getBubbleTooltip = (q, opt) => {
  const isMarked = String(q.marked_choice || '').trim() === String(opt).trim()
  const isCorrectKey = String(q.correct_choice || '').trim() === String(opt).trim()

  if (isMarked && q.is_correct) {
    return `الخيار ${opt}: تظليل الطالب الصحيح`
  }
  if (isMarked && !q.is_correct) {
    return `الخيار ${opt}: تظليل الطالب (إجابة خاطئة)`
  }
  if (isCorrectKey) {
    return `الخيار ${opt}: الإجابة النموذجية الصحيحة (انقر للتعيين)`
  }
  return `الخيار ${opt}: انقر لتعيينه كتظليل للطالب`
}

const getCardStatusClass = (q) => {
  if (q.bubble_state === 'ambiguous' || (q.final_confidence && q.final_confidence < 0.7)) {
    return 'card-ambiguous'
  }
  if (q.is_correct === true) {
    return 'card-correct'
  }
  if (q.is_correct === false && q.marked_choice) {
    return 'card-wrong'
  }
  return 'card-empty'
}

const getStatusChipColor = (q) => {
  if (q.bubble_state === 'ambiguous') return 'warning'
  if (q.is_correct === true) return 'success'
  if (q.is_correct === false && q.marked_choice) return 'error'
  return 'grey-darken-1'
}

const getStatusChipIcon = (q) => {
  if (q.bubble_state === 'ambiguous') return 'mdi-alert'
  if (q.is_correct === true) return 'mdi-check-circle'
  if (q.is_correct === false && q.marked_choice) return 'mdi-close-circle'
  return 'mdi-circle-outline'
}

const getStatusChipText = (q) => {
  if (q.bubble_state === 'ambiguous') return 'ملتبس'
  if (q.is_correct === true) return 'صحيحة'
  if (q.is_correct === false && q.marked_choice) return 'خاطئة'
  return 'لم يُجب (فارغ)'
}

const overrideQuestionChoice = async (q, choice) => {
  if (!activeReviewSheet.value) return
  const key = `${q.question_number}_${choice || 'clear'}`
  overridingLoading.value = key
  try {
    const res = await humanReviewAPI.overrideQuestion(activeReviewSheet.value.id, {
      question_number: q.question_number,
      marked_choice: choice
    })
    q.marked_choice = choice
    q.is_correct = choice ? (normalizeChoiceValue(choice) === normalizeChoiceValue(q.correct_choice)) : false
    q.bubble_state = choice ? 'filled' : 'empty'

    if (res.data?.mcq_score != null) {
      activeReviewSheet.value.mcq_score = res.data.mcq_score
    }
    if (res.data?.correct_answers != null) {
      activeReviewSheet.value.correct_answers = res.data.correct_answers
    }
    if (res.data?.ambiguous_count != null) {
      activeReviewSheet.value.ambiguous_count = res.data.ambiguous_count
    }

    proxy.$alert('success', { message: `تم تحديث إجابة السؤال ${q.question_number} بنجاح` })
  } catch (err) {
    console.error('Error overriding question choice:', err)
    proxy.$alert('errorData', { message: 'تعذر تعديل إجابة السؤال' })
  } finally {
    overridingLoading.value = ''
  }
}

const approveCurrentSheet = async () => {
  if (!activeReviewSheet.value) return
  approvingLoading.value = true
  try {
    await humanReviewAPI.approveReview(activeReviewSheet.value.id)
    proxy.$alert('success', { message: 'تم اعتماد ومصادقة الورقة بنجاح' })
    reviewDialog.value = false
    await fetchData()
  } catch (err) {
    proxy.$alert('errorData', { message: 'فشل اعتماد الورقة' })
    console.error(err)
  } finally {
    approvingLoading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.qb-human-review-v4 {
  color: rgb(var(--v-theme-on-surface));
}

.main-card, .stat-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.unified-table-chip {
  border-radius: 6px !important;
  font-weight: 700 !important;
}

/* ── Modern Dialog Header & Footer Styling (No Dark Background) ── */
.dialog-header {
  border-bottom: 1px solid #e2e8f0 !important;
  background-color: #ffffff !important;
}

.dialog-footer {
  border-top: 1px solid #e2e8f0 !important;
  background-color: #ffffff !important;
}

.dialog-icon-avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background-color: #eff6ff;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #dbeafe;
}

.header-score-pill {
  background-color: #ecfdf5;
  border: 1px solid #a7f3d0;
}

/* ── Question Box Cards (مربعات الأسئلة المتطورة) ── */
.review-question-card {
  background: #ffffff;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
  transition: all 0.2s ease-in-out;
  position: relative;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

.review-question-card:hover {
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
  transform: translateY(-1px);
}

.card-correct {
  border-color: #86efac !important;
  background-color: #fafffc !important;
}

.card-wrong {
  border-color: #fca5a5 !important;
  background-color: #fffafa !important;
}

.card-ambiguous {
  border-color: #fcd34d !important;
  background-color: #fffbeb !important;
  box-shadow: 0 0 0 1px #f59e0b, 0 4px 12px rgba(245, 158, 11, 0.1);
}

.card-empty {
  border-color: #e2e8f0;
  background-color: #ffffff;
}

/* Card Inner Elements */
.card-inner-divider {
  height: 1px;
  background-color: #f1f5f9;
}

.q-number-circle {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: #f1f5f9;
  color: #334155;
  font-size: 13px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-correct .q-number-circle {
  background: #dcfce7;
  color: #15803d;
}

.card-wrong .q-number-circle {
  background: #fee2e2;
  color: #b91c1c;
}

.card-ambiguous .q-number-circle {
  background: #fef3c7;
  color: #b45309;
}

/* Model Answer Tag */
.model-key-pill {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 2px 8px;
  font-size: 11px;
}

.model-key-char {
  background: #059669;
  color: white;
  border-radius: 4px;
  padding: 1px 7px;
  font-weight: 800;
  font-size: 12px;
}

/* ── Authentic OMR Bubble Circles ── */
.omr-bubble-interactive {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  font-size: 13px;
  font-weight: 800;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  outline: none;
  transition: all 0.15s ease-in-out;
  border: 1.5px solid #cbd5e1;
  background: #ffffff;
  color: #475569;
  user-select: none;
}

.omr-bubble-interactive:hover:not(:disabled) {
  border-color: #2563eb;
  background: #eff6ff;
  color: #1d4ed8;
  transform: scale(1.08);
}

.bubble-marked-correct {
  border: 2px solid #059669 !important;
  background: #10b981 !important;
  color: #ffffff !important;
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.4);
  transform: scale(1.06);
}

.bubble-marked-wrong {
  border: 2px solid #dc2626 !important;
  background: #ef4444 !important;
  color: #ffffff !important;
  box-shadow: 0 2px 6px rgba(239, 68, 68, 0.4);
  transform: scale(1.06);
}

.bubble-model-key {
  border: 2px dashed #059669 !important;
  background: #ecfdf5 !important;
  color: #047857 !important;
}

.bubble-model-key:hover:not(:disabled) {
  background: #d1fae5 !important;
  border-color: #047857 !important;
  transform: scale(1.08);
}

/* Eraser Button */
.omr-eraser-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #fecaca;
  background: #fef2f2;
  cursor: pointer;
  transition: all 0.15s ease-in-out;
}

.omr-eraser-btn:hover {
  background: #fee2e2;
  border-color: #ef4444;
  transform: scale(1.08);
}
</style>
