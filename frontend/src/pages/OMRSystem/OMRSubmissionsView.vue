<template>
  <div class="qb-submissions-view-v4 pa-4 pa-md-6">

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 1. شريط مسار وسير عمل التصحيح الضوئي (OMR Workflow)             -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <OMRWorkflowBar :currentStep="4" class="mb-5" />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 2. بطاقات المؤشرات الإحصائية المباشرة (Server-Side KPI Cards)  -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <v-row dense class="mb-4">
      <!-- 1. إجمالي الأوراق الممسوحة -->
      <v-col cols="12" sm="6" md="2">
        <v-card
          elevation="1"
          rounded="xl"
          class="kpi-filter-card pa-3 border cursor-pointer"
          :class="{ 'kpi-card-active border-primary bg-primary-lighten-5': activeKpiFilter === null }"
          @click="onKpiCardClick(null)"
        >
          <div class="d-flex align-center justify-space-between mb-1">
            <span class="text-caption font-weight-bold text-medium-emphasis">إجمالي الأوراق</span>
            <v-avatar color="primary" variant="tonal" size="28" rounded="lg">
              <v-icon size="16">mdi-file-document-multiple-outline</v-icon>
            </v-avatar>
          </div>
          <div class="text-h6 font-weight-black text-primary font-mono">
            {{ statsData.total || 0 }}
          </div>
          <div class="text-caption text-medium-emphasis mt-0.5">عموم الأوراق في النظام</div>
        </v-card>
      </v-col>

      <!-- 2. أوراق مقروءة ومعتمدة -->
      <v-col cols="12" sm="6" md="2">
        <v-card
          elevation="1"
          rounded="xl"
          class="kpi-filter-card pa-3 border cursor-pointer"
          :class="{ 'kpi-card-active border-success bg-green-lighten-5': activeKpiFilter === 'completed' }"
          @click="onKpiCardClick('completed')"
        >
          <div class="d-flex align-center justify-space-between mb-1">
            <span class="text-caption font-weight-bold text-success">مقروءة ومعتمدة</span>
            <v-avatar color="success" variant="tonal" size="28" rounded="lg">
              <v-icon size="16">mdi-check-decagram</v-icon>
            </v-avatar>
          </div>
          <div class="text-h6 font-weight-black text-success font-mono">
            {{ statsData.completed || 0 }}
          </div>
          <div class="text-caption text-medium-emphasis mt-0.5">تم تصحيحها واعتمادها</div>
        </v-card>
      </v-col>

      <!-- 3. أوراق تحتاج مراجعة وتدقيق -->
      <v-col cols="12" sm="6" md="2">
        <v-card
          elevation="1"
          rounded="xl"
          class="kpi-filter-card pa-3 border cursor-pointer"
          :class="{ 'kpi-card-active border-warning bg-amber-lighten-5': activeKpiFilter === 'needs_review' }"
          @click="onKpiCardClick('needs_review')"
        >
          <div class="d-flex align-center justify-space-between mb-1">
            <span class="text-caption font-weight-bold text-warning">تحتاج مراجعة</span>
            <v-avatar color="warning" variant="tonal" size="28" rounded="lg">
              <v-icon size="16">mdi-alert-circle-outline</v-icon>
            </v-avatar>
          </div>
          <div class="text-h6 font-weight-black text-warning font-mono">
            {{ statsData.needs_review || 0 }}
          </div>
          <div class="text-caption text-medium-emphasis mt-0.5">فقاعات ملتبسة أو مزدوجة</div>
        </v-card>
      </v-col>

      <!-- 4. أوراق فاشلة القراءة -->
      <v-col cols="12" sm="6" md="2">
        <v-card
          elevation="1"
          rounded="xl"
          class="kpi-filter-card pa-3 border cursor-pointer"
          :class="{ 'kpi-card-active border-error bg-red-lighten-5': activeKpiFilter === 'failed' }"
          @click="onKpiCardClick('failed')"
        >
          <div class="d-flex align-center justify-space-between mb-1">
            <span class="text-caption font-weight-bold text-error">فشل قراءة</span>
            <v-avatar color="error" variant="tonal" size="28" rounded="lg">
              <v-icon size="16">mdi-close-circle-outline</v-icon>
            </v-avatar>
          </div>
          <div class="text-h6 font-weight-black text-error font-mono">
            {{ statsData.failed || 0 }}
          </div>
          <div class="text-caption text-medium-emphasis mt-0.5">تعذر التعرف الضوئي</div>
        </v-card>
      </v-col>

      <!-- 5. أوراق قيد المعالجة -->
      <v-col cols="12" sm="6" md="2">
        <v-card
          elevation="1"
          rounded="xl"
          class="kpi-filter-card pa-3 border cursor-pointer"
          :class="{ 'kpi-card-active border-info bg-cyan-lighten-5': activeKpiFilter === 'pending' }"
          @click="onKpiCardClick('pending')"
        >
          <div class="d-flex align-center justify-space-between mb-1">
            <span class="text-caption font-weight-bold text-info">قيد المعالجة</span>
            <v-avatar color="info" variant="tonal" size="28" rounded="lg">
              <v-icon size="16">mdi-clock-outline</v-icon>
            </v-avatar>
          </div>
          <div class="text-h6 font-weight-black text-info font-mono">
            {{ statsData.pending || 0 }}
          </div>
          <div class="text-caption text-medium-emphasis mt-0.5">في رتل محرك OMR</div>
        </v-card>
      </v-col>

      <!-- 6. متوسط درجات التصحيح -->
      <v-col cols="12" sm="6" md="2">
        <v-card elevation="1" rounded="xl" class="pa-3 border bg-deep-purple-lighten-5">
          <div class="d-flex align-center justify-space-between mb-1">
            <span class="text-caption font-weight-bold text-deep-purple">متوسط الدرجات</span>
            <v-avatar color="deep-purple" variant="tonal" size="28" rounded="lg">
              <v-icon size="16">mdi-chart-bell-curve-cumulative</v-icon>
            </v-avatar>
          </div>
          <div class="text-h6 font-weight-black text-deep-purple font-mono">
            {{ statsData.average_score || 0 }}%
          </div>
          <div class="text-caption text-medium-emphasis mt-0.5">للأوراق المعتمدة</div>
        </v-card>
      </v-col>
    </v-row>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 3. شريط التصفية والبحث الموحد (Server-Side Filter Fields)       -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <filter-fields label="خيارات تصفية وتدقيق نتائج أوراق الإجابة المصححة" class="main-card border-0 pa-5 rounded-2xl mb-5 elevation-1">
      <v-row dense class="align-center">
        <!-- 1. البحث الفوري باسم الطالب أو رقم الجلوس أو الباركود -->
        <v-col cols="12" sm="6" md="3">
          <custom-text-field
            v-model="searchQuery"
            label="اسم الطالب أو رقم الجلوس أو الباركود"
            placeholder="بحث بالاسم، رقم الجلوس، الباركود..."
            icon="magnify"
            cols="12"
            :hideDetails="true"
            clearable
            @update:model-value="onSearchInput"
          />
        </v-col>

        <!-- 2. الاختبار المعروض -->
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="selectedExamId"
            name="Exam"
            :objects="examsObjects"
            label="الاختبار المعروض"
            placeholder="اختر الاختبار..."
            cols="12"
            :add="false"
            :hideDetails="true"
            @update:model-value="onExamChange"
          />
        </v-col>

        <!-- 3. النموذج الامتحاني -->
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filterVersion"
            name="ScreenTypeChoices"
            :objects="versionFilterObjects"
            label="النموذج الامتحاني"
            placeholder="النموذج (A, B, C, D)"
            cols="12"
            :add="false"
            :hideDetails="true"
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- 4. حالة ورقة الإجابة والتصحيح -->
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filterStatus"
            name="ScreenTypeChoices"
            :objects="statusFilterObjects"
            label="حالة الورقة"
            placeholder="حالة المسح والتصحيح"
            cols="12"
            :add="false"
            :hideDetails="true"
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- شريط إجراءات الفلترة السريعة وروابط الكنترول -->
        <v-col cols="12" class="d-flex align-center justify-space-between flex-wrap gap-2 pt-2">
          <div class="d-flex align-center gap-2 flex-wrap">
            <v-chip
              v-if="selectedExamObj"
              color="primary"
              variant="tonal"
              size="small"
              class="font-weight-bold px-3"
            >
              <v-icon start size="14">mdi-book-education-outline</v-icon>
              المادة: {{ selectedExamObj.subject_name || selectedExamObj.subject || 'عام' }}
            </v-chip>

            <v-chip
              v-if="filterStatus"
              color="warning"
              variant="tonal"
              size="small"
              class="font-weight-bold px-3 cursor-pointer"
              closable
              @click:close="onKpiCardClick(null)"
            >
              الحالة: {{ getStatusText(filterStatus) }}
            </v-chip>
          </div>

          <div class="d-flex align-center gap-2">
            <v-btn
              v-if="selectedExamId"
              color="indigo"
              variant="tonal"
              size="small"
              rounded="lg"
              class="font-weight-bold"
              prepend-icon="mdi-clipboard-list-outline"
              @click="$router.push(`/omr-gradebook?exam=${selectedExamId}`)"
            >
              كشف الرصد والكنترول
            </v-btn>

            <custom-btn
              type="cancel_filter"
              :click="resetDetailFilters"
              variant="tonal"
              color="error"
              label="تفريغ الفلاتر"
              icon="mdi-filter-off"
              class="font-weight-bold"
            />
          </div>
        </v-col>
      </v-row>
    </filter-fields>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 4. جدول سجل أوراق الإجابة الممسوحة والمصححة (Server Paginated)   -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <div class="main-card rounded-2xl overflow-hidden mb-6 elevation-1 bg-surface border">
      <custom-data-table
        v-model="selectedSubmissionIds"
        :headers="detailHeaders"
        :items="tableItems"
        :getData="fetchSubmissionsRoster"
        :customLoading="loadingRecords"
        class="bg-transparent"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :numbering="true"
        :showSelect="true"
        :itemValue="'id'"
        :actions="false"
      >
        <template v-slot:item-slot="{ item, key, index }">
          <!-- الترقيم الموحد -->
          <template v-if="key === 'numbering'">
            <div class="d-flex justify-center align-center">
              <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
            </div>
          </template>

          <!-- صورة الورقة الممسوحة المصغرة مع زر المعاينة -->
          <template v-else-if="key === 'sheet_thumbnail'">
            <div class="d-flex justify-center align-center py-1">
              <v-tooltip location="top" text="انقر لمعاينة صورة ورقة الإجابة الممسوحة بدقة عالية">
                <template #activator="{ props }">
                  <div
                    v-bind="props"
                    class="sheet-thumb-wrapper rounded-lg border overflow-hidden cursor-pointer"
                    style="width: 44px; height: 56px; background: #f8fafc;"
                    @click="previewSheetImage(item)"
                  >
                    <v-img
                      v-if="item.original_image"
                      :src="fixImageUrl(item.original_image)"
                      cover
                      class="w-100 h-100"
                    />
                    <div v-else class="d-flex align-center justify-center w-100 h-100 text-grey">
                      <v-icon size="20">mdi-file-document-outline</v-icon>
                    </div>
                  </div>
                </template>
              </v-tooltip>
            </div>
          </template>

          <!-- رقم الجلوس أو الرقم الأكاديمي -->
          <template v-else-if="key === 'seat_number'">
            <div class="d-flex justify-center align-center">
              <span class="font-weight-black font-mono text-primary text-subtitle-2">
                {{ item.seat_number || '-' }}
              </span>
            </div>
          </template>

          <!-- اسم الطالب والمادة -->
          <template v-else-if="key === 'student_name'">
            <div class="py-1">
              <div class="font-weight-bold text-body-2 text-on-surface">{{ item.student_name || 'طالب غير محدد' }}</div>
              <div class="text-caption text-medium-emphasis">{{ item.subject_name || selectedExamObj?.subject_name || '-' }}</div>
            </div>
          </template>

          <!-- كود النموذج الامتحاني -->
          <template v-else-if="key === 'exam_version_code'">
            <div class="d-flex justify-center align-center">
              <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                {{ item.exam_version_code || 'نموذج عام' }}
              </v-chip>
            </div>
          </template>

          <!-- الدرجة الكلية -->
          <template v-else-if="key === 'total_score'">
            <div class="text-center py-1">
              <span class="text-subtitle-2 font-weight-black text-on-surface">
                {{ item.total_score != null ? item.total_score : '-' }}
              </span>
              <div v-if="item.mcq_score != null" class="text-caption text-medium-emphasis">
                خيارات: {{ item.mcq_score }} | مقالي: {{ item.essay_score || 0 }}
              </div>
            </div>
          </template>

          <!-- نسبة الثقة الضوئية OMR Confidence -->
          <template v-else-if="key === 'confidence'">
            <div class="d-flex align-center justify-center gap-1">
              <v-progress-circular
                :model-value="Math.round((item.overall_confidence || 0.95) * 100)"
                :color="(item.overall_confidence || 0.95) >= 0.85 ? 'success' : 'warning'"
                size="26"
                width="3"
              />
              <span class="text-caption font-weight-bold">
                {{ Math.round((item.overall_confidence || 0.95) * 100) }}%
              </span>
            </div>
          </template>

          <!-- حالة المعالجة الضوئية والتصحيح -->
          <template v-else-if="key === 'status'">
            <div class="d-flex justify-center align-center">
              <v-chip
                size="small"
                :color="getStatusColor(item.status)"
                variant="tonal"
                class="font-weight-bold"
              >
                {{ item.status_display || getStatusText(item.status) }}
              </v-chip>
            </div>
          </template>

          <!-- الإجراءات المباشرة -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-1">
              <v-tooltip location="top" text="فحص تفاصيل الورقة الكاملة والفقاعات">
                <template #activator="{ props }">
                  <v-btn
                    v-bind="props"
                    size="small"
                    color="primary"
                    variant="flat"
                    icon="mdi-file-eye-outline"
                    rounded="lg"
                    @click="navigateToDetail(item)"
                  />
                </template>
              </v-tooltip>

              <v-tooltip location="top" text="معاينة صورة الورقة الممسوحة">
                <template #activator="{ props }">
                  <v-btn
                    v-bind="props"
                    size="small"
                    color="secondary"
                    variant="tonal"
                    icon="mdi-image-search-outline"
                    rounded="lg"
                    @click="previewSheetImage(item)"
                  />
                </template>
              </v-tooltip>

              <v-tooltip location="top" text="إعادة المعالجة الضوئية للورقة">
                <template #activator="{ props }">
                  <v-btn
                    v-bind="props"
                    size="small"
                    color="warning"
                    variant="tonal"
                    icon="mdi-refresh"
                    rounded="lg"
                    :loading="reprocessingId === item.id"
                    @click="reprocessSingleSheet(item)"
                  />
                </template>
              </v-tooltip>

              <v-tooltip location="top" text="حذف ورقة الإجابة">
                <template #activator="{ props }">
                  <v-btn
                    v-bind="props"
                    size="small"
                    color="error"
                    variant="tonal"
                    icon="mdi-delete-outline"
                    rounded="lg"
                    @click="confirmDeleteSubmission(item)"
                  />
                </template>
              </v-tooltip>
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 5. نافذة المعاينة السريعة لصورة ورقة الإجابة (Lightbox)         -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <v-dialog v-model="imagePreviewDialog" width="860px" max-width="95vw">
      <v-card rounded="2xl" class="border elevation-6 overflow-hidden main-card">
        <v-card-title class="d-flex align-center justify-space-between bg-surface pa-4 px-6 border-b">
          <div class="d-flex align-center gap-2">
            <v-icon color="primary" size="22">mdi-image-search-outline</v-icon>
            <div>
              <div class="text-subtitle-1 font-weight-black text-on-surface">معاينة ورقة إجابة الطالب: {{ previewSubmission?.student_name }}</div>
              <div class="text-caption text-medium-emphasis">رقم الجلوس: {{ previewSubmission?.seat_number }} • {{ previewSubmission?.exam_title }}</div>
            </div>
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" @click="imagePreviewDialog = false" />
        </v-card-title>

        <v-card-text class="pa-4 bg-surface text-center">
          <div v-if="previewSubmission?.original_image" class="border rounded-xl pa-2 bg-grey-lighten-4 overflow-auto" style="max-height: 72vh;">
            <v-img
              :src="fixImageUrl(previewSubmission.original_image)"
              contain
              class="rounded-lg mx-auto"
              style="max-height: 68vh;"
            />
          </div>
          <div v-else class="py-12 text-medium-emphasis">
            <v-icon size="48" color="grey">mdi-image-off-outline</v-icon>
            <div class="mt-2 text-body-2 font-weight-bold">لا توجد صورة ممسوحة مرفقة لهذه الورقة في النظام</div>
          </div>
        </v-card-text>

        <v-divider />
        <v-card-actions class="pa-4 bg-surface d-flex justify-space-between align-center">
          <v-chip color="primary" variant="tonal" class="font-weight-bold">
            درجة الورقة: {{ previewSubmission?.total_score ?? '-' }}
          </v-chip>
          <div class="d-flex gap-2">
            <v-btn variant="tonal" color="grey" rounded="lg" class="font-weight-bold px-4" @click="imagePreviewDialog = false">
              إغلاق
            </v-btn>
            <v-btn
              color="primary"
              variant="flat"
              rounded="lg"
              class="font-weight-bold px-4"
              prepend-icon="mdi-file-eye-outline"
              @click="imagePreviewDialog = false; navigateToDetail(previewSubmission);"
            >
              فحص تفاصيل الورقة الكاملة
            </v-btn>
          </div>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- نافذة تأكيد الحذف -->
    <DeleteDialog
      v-model="deleteDialog"
      title="حذف ورقة الإجابة"
      :message="`هل أنت متأكد من حذف ورقة إجابة الطالب '${submissionToDelete ? submissionToDelete.student_name : ''}' نهائياً؟`"
      @confirm-delete="executeDelete"
    />

    <!-- الإشعارات المنبثقة -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="4000" location="top left">
      {{ snackbar.text }}
      <template #actions>
        <v-btn variant="text" @click="snackbar.show = false">إغلاق</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import api from '@/services/api'
import { submissionsAPI, examsAPI } from '@/services/omr/endpoints'
import OMRWorkflowBar from '@/components/OMRWorkflowBar.vue'

export default {
  name: 'OMRSubmissionsView',

  components: {
    OMRWorkflowBar,
  },

  data() {
    return {
      institutionType: 'school',
      activeKpiFilter: null,
      loadingRecords: false,
      searchQuery: '',
      filterStatus: null,
      filterVersion: 'all',

      selectedExamId: null,
      selectedExamObj: null,
      examsList: [],

      selectedSubmissionIds: [],
      reprocessingId: null,

      // Stats from Backend SQL aggregation
      statsData: {
        total: 0,
        completed: 0,
        needs_review: 0,
        failed: 0,
        pending: 0,
        average_score: 0,
      },

      // Server-Side Paginated Table Items
      tableItems: {
        results: [],
        count: 0,
        pagination: {
          count: 0,
          total: 0,
          num_pages: 1,
          current_page: 1,
          page_size: 15,
        }
      },

      detailHeaders: [
        { title: "الورقة الممسوحة", key: "sheet_thumbnail", sortable: false, align: "center", width: "90px" },
        { title: "رقم الجلوس", key: "seat_number", sortable: true, align: "center", width: "120px" },
        { title: "اسم الطالب والمادة", key: "student_name", sortable: true, align: "start" },
        { title: "النموذج", key: "exam_version_code", sortable: true, align: "center", width: "100px" },
        { title: "الدرجة الكلية", key: "total_score", sortable: true, align: "center", width: "130px" },
        { title: "دقة OMR", key: "confidence", sortable: true, align: "center", width: "110px" },
        { title: "حالة التصحيح", key: "status", sortable: true, align: "center", width: "135px" },
        { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "170px" },
      ],

      statusOptions: [
        { title: 'جميع الحالات', value: null },
        { title: 'مكتمل ومعتمد (Completed)', value: 'completed' },
        { title: 'يحتاج مراجعة (Needs Review)', value: 'needs_review' },
        { title: 'تمت المراجعة (Reviewed)', value: 'reviewed' },
        { title: 'فشل التصحيح (Failed)', value: 'failed' },
        { title: 'قيد الانتظار (Pending)', value: 'pending' },
      ],

      // Dialogs
      imagePreviewDialog: false,
      previewSubmission: null,
      deleteDialog: false,
      submissionToDelete: null,

      snackbar: {
        show: false,
        text: '',
        color: 'success',
      },

      searchDebounceTimer: null,
    }
  },

  computed: {
    examsObjects() {
      return (this.examsList || []).map(e => ({
        id: e.id,
        value: e.id,
        name: e.title || e.name || `اختبار #${e.id}`,
        name_ar: e.title || e.name || `اختبار #${e.id}`,
        title: e.title || e.name || `اختبار #${e.id}`,
        uniqueCode: e.uniqueCode || '',
        subject_name: e.subject_name || '',
      }))
    },

    availableVersions() {
      if (!this.selectedExamObj) return ['A', 'B', 'C', 'D']
      if (this.selectedExamObj.versions_list && this.selectedExamObj.versions_list.length) {
        return this.selectedExamObj.versions_list.map(v => v.versionCode || v.code || v)
      }
      return ['A', 'B', 'C', 'D']
    },

    versionFilterObjects() {
      const opts = [
        { id: 'all', value: 'all', name: 'جميع النماذج', name_ar: 'جميع النماذج', title: 'جميع النماذج' }
      ]
      if (this.availableVersions && this.availableVersions.length) {
        this.availableVersions.forEach(v => {
          if (v) {
            opts.push({
              id: v,
              value: v,
              name: `النموذج ${v}`,
              name_ar: `النموذج ${v}`,
              title: `النموذج ${v}`,
            })
          }
        })
      }
      return opts
    },

    statusFilterObjects() {
      return [
        { id: 'all', value: 'all', name: 'جميع الحالات', name_ar: 'جميع الحالات', title: 'جميع الحالات' },
        { id: 'completed', value: 'completed', name: 'مكتمل ومعتمد', name_ar: 'مكتمل ومعتمد', title: 'مكتمل ومعتمد' },
        { id: 'needs_review', value: 'needs_review', name: 'يحتاج مراجعة وتدقيق', name_ar: 'يحتاج مراجعة وتدقيق', title: 'يحتاج مراجعة وتدقيق' },
        { id: 'reviewed', value: 'reviewed', name: 'تمت المراجعة يدوياً', name_ar: 'تمت المراجعة يدوياً', title: 'تمت المراجعة يدوياً' },
        { id: 'failed', value: 'failed', name: 'فشل التصحيح', name_ar: 'فشل التصحيح', title: 'فشل التصحيح' },
        { id: 'pending', value: 'pending', name: 'قيد الانتظار والمعالجة', name_ar: 'قيد الانتظار والمعالجة', title: 'قيد الانتظار والمعالجة' },
      ]
    },
  },

  async created() {
    await this.loadExamsList()

    const queryExam = this.$route.query.exam || this.$route.query.open_exam_id
    if (queryExam) {
      this.selectedExamId = parseInt(queryExam) || queryExam
      this.selectedExamObj = (this.examsList || []).find(e => e.id === this.selectedExamId) || null
    }

    await Promise.all([
      this.fetchStats(),
      this.fetchSubmissionsRoster({ page: 1, page_size: 15 })
    ])
  },

  methods: {
    async loadExamsList() {
      try {
        const res = await examsAPI.list({ page_size: 100 })
        const data = res.data?.results || res.data || []
        this.examsList = Array.isArray(data) ? data : []
      } catch (err) {
        console.error('Failed to load exams list:', err)
      }
    },

    async fetchStats() {
      try {
        const params = this.buildFilterParams()
        const res = await submissionsAPI.getStats(params)
        if (res && res.data) {
          this.statsData = res.data
        }
      } catch (err) {
        console.error('Failed to load submissions stats:', err)
      }
    },

    buildFilterParams(extra = {}) {
      const q = { ...extra }
      if (this.selectedExamId) q.exam = this.selectedExamId
      if (this.searchQuery && this.searchQuery.trim()) {
        q.search = this.searchQuery.trim()
      } else if (extra && extra.search) {
        q.search = extra.search
      }
      if (this.filterStatus && this.filterStatus !== 'all') {
        q.status = this.filterStatus
      }
      if (this.filterVersion && this.filterVersion !== 'all') {
        q.version_code = this.filterVersion
        q.exam_version = this.filterVersion
      }
      if (this.institutionType && this.institutionType !== 'all') {
        q.institution_type = this.institutionType
      }
      return q
    },

    async fetchSubmissionsRoster(tableParams = null) {
      this.loadingRecords = true
      try {
        let baseParams = { page: 1, page_size: 15 }
        if (tableParams && tableParams.params) {
          baseParams = { ...tableParams.params }
        } else if (tableParams && typeof tableParams === 'object') {
          baseParams = { ...tableParams }
        }
        const queryParams = this.buildFilterParams(baseParams)

        const res = await submissionsAPI.list(queryParams)
        const data = res.data || res || {}
        if (Array.isArray(data)) {
          this.tableItems = {
            results: data,
            count: data.length,
            pagination: {
              count: data.length,
              total: data.length,
              num_pages: Math.ceil(data.length / (queryParams.page_size || 15)) || 1,
              current_page: queryParams.page || 1,
              page_size: queryParams.page_size || 15,
            }
          }
        } else if (data && data.results) {
          const results = data.results || []
          const total = data.pagination?.total || data.count || results.length
          const pageSize = queryParams.page_size || data.pagination?.page_size || 15
          this.tableItems = {
            ...data,
            results,
            count: total,
            pagination: {
              count: total,
              total,
              num_pages: Math.ceil(total / pageSize) || 1,
              current_page: queryParams.page || 1,
              page_size: pageSize,
            }
          }
        }
        return this.tableItems
      } catch (err) {
        console.error('Failed to fetch submissions roster:', err)
        return { results: [], pagination: {} }
      } finally {
        this.loadingRecords = false
      }
    },

    onSearchInput() {
      if (this.searchDebounceTimer) clearTimeout(this.searchDebounceTimer)
      this.searchDebounceTimer = setTimeout(() => {
        this.applyFilters()
      }, 400)
    },

    onExamChange(examId) {
      this.selectedExamId = examId
      this.selectedExamObj = (this.examsList || []).find(e => e.id === examId) || null
      this.applyFilters()
    },

    onKpiCardClick(statusKey) {
      if (this.activeKpiFilter === statusKey) {
        this.activeKpiFilter = null
        this.filterStatus = null
      } else {
        this.activeKpiFilter = statusKey
        this.filterStatus = statusKey
      }
      this.fetchSubmissionsRoster({ page: 1 })
    },

    applyFilters() {
      if (this.filterStatus === 'all') this.filterStatus = null
      this.activeKpiFilter = this.filterStatus
      this.fetchSubmissionsRoster({ page: 1 })
      this.fetchStats()
    },

    resetDetailFilters() {
      this.searchQuery = ''
      this.filterVersion = 'all'
      this.filterStatus = null
      this.activeKpiFilter = null
      this.selectedExamId = null
      this.selectedExamObj = null
      this.applyFilters()
    },

    // Sheet Actions
    navigateToDetail(item) {
      if (!item || !item.id) return
      this.$router.push(`/omr-submissions/${item.id}`)
    },

    previewSheetImage(item) {
      this.previewSubmission = item
      this.imagePreviewDialog = true
    },

    async reprocessSingleSheet(item) {
      if (!item || !item.id) return
      this.reprocessingId = item.id
      try {
        const res = await submissionsAPI.reprocess(item.id)
        if (res && res.data && res.data.success) {
          this.notify('تمت إعادة المعالجة والتصحيح الضوئي بنجاح', 'success')
          await this.fetchSubmissionsRoster()
          await this.fetchStats()
        } else {
          this.notify(res?.data?.message || 'تم تحديث نتائج المعالجة الضوئية', 'info')
          await this.fetchSubmissionsRoster()
          await this.fetchStats()
        }
      } catch (err) {
        console.error('Error reprocessing sheet:', err)
        this.notify('حدث خطأ أثناء إعادة المعالجة الضوئية', 'error')
      } finally {
        this.reprocessingId = null
      }
    },

    confirmDeleteSubmission(item) {
      this.submissionToDelete = item
      this.deleteDialog = true
    },

    async executeDelete() {
      if (!this.submissionToDelete || !this.submissionToDelete.id) return
      try {
        await submissionsAPI.delete(this.submissionToDelete.id)
        this.notify('تم حذف ورقة الإجابة بنجاح', 'success')
        this.deleteDialog = false
        this.submissionToDelete = null
        await this.fetchSubmissionsRoster()
        await this.fetchStats()
      } catch (err) {
        console.error('Error deleting submission:', err)
        this.notify('تعذر حذف ورقة الإجابة', 'error')
      }
    },

    fixImageUrl(url) {
      if (!url) return ''
      if (url.startsWith('http')) return url
      return url.startsWith('/') ? url : `/${url}`
    },

    getStatusColor(status) {
      const map = {
        'completed': 'success',
        'reviewed': 'info',
        'needs_review': 'warning',
        'failed': 'error',
        'pending': 'grey',
        'processing': 'primary',
      }
      return map[status] || 'grey'
    },

    getStatusText(status) {
      const map = {
        'completed': 'مكتمل ومعتمد',
        'reviewed': 'تمت المراجعة',
        'needs_review': 'يحتاج مراجعة',
        'failed': 'فشل التصحيح',
        'pending': 'قيد الانتظار',
        'processing': 'جاري المعالجة',
      }
      return map[status] || status || 'غير محدد'
    },

    notify(text, color = 'success') {
      this.snackbar.text = text
      this.snackbar.color = color
      this.snackbar.show = true
    },
  },
}
</script>

<style scoped>
.qb-submissions-view-v4 {
  direction: rtl;
}

.main-card {
  transition: all 0.2s ease-in-out;
}

.sheet-thumb-wrapper {
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.sheet-thumb-wrapper:hover {
  transform: scale(1.08);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.kpi-filter-card {
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.kpi-filter-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08) !important;
}

.kpi-card-active {
  border-width: 2px !important;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12) !important;
}
</style>
