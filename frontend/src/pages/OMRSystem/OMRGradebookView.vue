<template>
  <div class="qb-gradebook-view-v4">
    <!-- ── Page Header (Institutional OpenSoftCore Style) ─────────────── -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center">
        <back-to class="me-3" />
        <v-avatar size="44" color="primary" variant="tonal" class="me-3 rounded-xl">
          <v-icon size="24">mdi-clipboard-check-multiple-outline</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">سجل درجات الاختبارات وترحيل الكنترول</h1>
          <p class="text-caption text-medium-emphasis mb-0">
            تدقيق ومراجعة كشوفات الرصد الأكاديمية وترحيل الدرجات المعتمدة رسمياً لنظام الكنترول المركزي
          </p>
        </div>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <custom-btn
          type="restore"
          :click="() => $router.push('/omr/dashboard')"
          label="لوحة التحكم"
          color="secondary"
          variant="tonal"
          class="font-weight-bold"
        />
        <custom-btn
          type="show"
          :click="() => $router.push('/omr/submissions')"
          label="سجل الأوراق"
          color="secondary"
          variant="tonal"
          class="font-weight-bold"
        />
        <custom-btn
          type="add"
          :click="() => $router.push('/omr/scanner-lab')"
          label="المسح الضوئي"
          color="primary"
          variant="tonal"
          class="font-weight-bold"
        />
      </div>
    </div>

    <!-- ── Overview KPI Cards ───────────────────────────────────────── -->
    <v-row class="mb-6">
      <!-- Total Students -->
      <v-col cols="12" sm="6" md="2">
        <div class="stat-glass-card pa-4 rounded-xl shadow-indigo">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="text-caption font-weight-bold text-medium-emphasis">إجمالي المسجلين</span>
            <div class="stat-icon-wrapper bg-indigo-gradient">
              <v-icon color="white" size="18">mdi-account-group-outline</v-icon>
            </div>
          </div>
          <div class="stat-value text-h4 font-weight-black text-indigo">{{ activeExamStats.total_students }}</div>
          <div class="text-caption text-medium-emphasis mt-1">طالب مسجل بالكشف</div>
        </div>
      </v-col>

      <!-- Completed & Graded -->
      <v-col cols="12" sm="6" md="2">
        <div class="stat-glass-card pa-4 rounded-xl shadow-emerald">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="text-caption font-weight-bold text-medium-emphasis">أوراق مصححة</span>
            <div class="stat-icon-wrapper bg-emerald-gradient">
              <v-icon color="white" size="18">mdi-check-decagram-outline</v-icon>
            </div>
          </div>
          <div class="stat-value text-h4 font-weight-black text-emerald">{{ activeExamStats.completed_count }}</div>
          <div class="text-caption text-medium-emphasis mt-1">جاهزة للترحيل</div>
        </div>
      </v-col>

      <!-- Needs Review -->
      <v-col cols="12" sm="6" md="2">
        <div class="stat-glass-card pa-4 rounded-xl shadow-amber">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="text-caption font-weight-bold text-medium-emphasis">تحت التدقيق</span>
            <div class="stat-icon-wrapper bg-amber-gradient">
              <v-icon color="white" size="18">mdi-account-eye-outline</v-icon>
            </div>
          </div>
          <div class="stat-value text-h4 font-weight-black text-amber">{{ activeExamStats.needs_review_count }}</div>
          <div class="text-caption text-amber-darken-2 font-weight-bold mt-1">تتطلب تدقيق يدوي</div>
        </div>
      </v-col>

      <!-- Absent Students -->
      <v-col cols="12" sm="6" md="2">
        <div class="stat-glass-card pa-4 rounded-xl shadow-rose">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="text-caption font-weight-bold text-medium-emphasis">الطلاب الغائبون</span>
            <div class="stat-icon-wrapper bg-rose-gradient">
              <v-icon color="white" size="18">mdi-account-cancel-outline</v-icon>
            </div>
          </div>
          <div class="stat-value text-h4 font-weight-black text-rose">{{ activeExamStats.absent_count }}</div>
          <div class="text-caption text-medium-emphasis mt-1">لم ترصد أوراقهم</div>
        </div>
      </v-col>

      <!-- Average Score & Pass Rate -->
      <v-col cols="12" sm="6" md="2">
        <div class="stat-glass-card pa-4 rounded-xl shadow-teal">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="text-caption font-weight-bold text-medium-emphasis">متوسط الدرجات</span>
            <div class="stat-icon-wrapper bg-teal-gradient">
              <v-icon color="white" size="18">mdi-chart-line</v-icon>
            </div>
          </div>
          <div class="stat-value text-h4 font-weight-black text-teal">{{ activeExamStats.average_score }}%</div>
          <div class="text-caption text-teal-darken-1 font-weight-bold mt-1">نسبة النجاح: {{ activeExamStats.pass_rate }}%</div>
        </div>
      </v-col>

      <!-- Dispatched to Control Status -->
      <v-col cols="12" sm="6" md="2">
        <div class="stat-glass-card pa-4 rounded-xl shadow-purple">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="text-caption font-weight-bold text-medium-emphasis">حالة الكنترول</span>
            <div class="stat-icon-wrapper bg-purple-gradient">
              <v-icon color="white" size="18">mdi-bank-transfer</v-icon>
            </div>
          </div>
          <div class="stat-value text-h4 font-weight-black text-purple">
            {{ activeExamStats.dispatched_count }} / {{ activeExamStats.completed_count }}
          </div>
          <div class="text-caption mt-1 font-weight-bold" :class="activeExamStats.is_fully_dispatched ? 'text-success' : 'text-purple-darken-1'">
            {{ activeExamStats.is_fully_dispatched ? 'مرحل بالكامل ✓' : 'قيد الترحيل' }}
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- ── Filter & Exam Selector Card ──────────────────────────────── -->
    <filter-fields label="اختيار الاختبار وتصفية كشوفات الرصد والكنترول" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Exam Autocomplete -->
        <v-col cols="12" md="5">
          <v-autocomplete
            v-model="selectedExamId"
            :items="examsList"
            item-title="title"
            item-value="id"
            label="اختر الاختبار الأكاديمي المطلوب استعراض درجاته"
            placeholder="ابحث باسم الاختبار أو كود المادة..."
            prepend-inner-icon="mdi-file-document-edit-outline"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            :loading="loadingExams"
            @update:model-value="onExamChange"
          >
            <template #item="{ props, item }">
              <v-list-item
                v-bind="props"
                :title="item.raw.title"
                :subtitle="`${item.raw.uniqueCode || ''} • ${item.raw.subject_name || ''} • مسجلين: ${item.raw.total_students || 0}`"
              >
                <template #append>
                  <v-chip
                    size="x-small"
                    :color="item.raw.is_fully_dispatched ? 'success' : (item.raw.dispatched_count > 0 ? 'warning' : 'grey')"
                    variant="tonal"
                    class="font-weight-bold"
                  >
                    {{ item.raw.is_fully_dispatched ? 'مرحل للكنترول' : (item.raw.dispatched_count > 0 ? 'مرحل جزئياً' : 'غير مرحل') }}
                  </v-chip>
                </template>
              </v-list-item>
            </template>
          </v-autocomplete>
        </v-col>

        <!-- Search Student -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="searchQuery"
            label="بحث سريع في كشف الرصد"
            placeholder="اسم الطالب، رقم الجلوس، الرقم السري..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Filter by Status -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterStatus"
            :items="statusFilterOptions"
            item-title="text"
            item-value="value"
            label="حالة الورقة"
            prepend-inner-icon="mdi-filter-outline"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Filter by Dispatch -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterDispatch"
            :items="dispatchFilterOptions"
            item-title="text"
            item-value="value"
            label="حالة الترحيل"
            prepend-inner-icon="mdi-bank-check"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- ── Selected Exam Banner & Actions Bar ──────────────────────── -->
    <v-card v-if="selectedExamObj" class="main-card pa-4 rounded-2xl mb-6 elevation-1 border">
      <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4">
        <div class="d-flex align-center gap-3">
          <v-avatar color="primary" variant="tonal" rounded="lg" size="48">
            <v-icon size="28">mdi-school-outline</v-icon>
          </v-avatar>
          <div>
            <div class="d-flex align-center gap-2 flex-wrap">
              <h2 class="text-h6 font-weight-black mb-0">{{ selectedExamObj.title }}</h2>
              <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                {{ selectedExamObj.uniqueCode || 'EXAM' }}
              </v-chip>
              <v-chip size="x-small" color="grey" variant="outlined" class="font-weight-bold">
                الدرجة الكلية: {{ selectedExamObj.max_score }} درجة
              </v-chip>
            </div>
            <p class="text-caption text-medium-emphasis mb-0 mt-1">
              المادة: <span class="font-weight-bold text-on-surface">{{ selectedExamObj.subject_name || '—' }}</span>
              • العام: <span class="font-weight-bold text-on-surface">{{ selectedExamObj.year_name || '—' }}</span>
              • الطلاب: <span class="font-weight-bold text-primary">{{ filteredRecords.length }}</span> طالب في الكشف الحالي
            </p>
          </div>
        </div>

        <!-- Action Buttons Bar -->
        <div class="d-flex align-center gap-2 flex-wrap">
          <!-- Dispatch to Control Button (Main CTA) -->
          <v-btn
            color="success"
            rounded="lg"
            class="font-weight-bold px-4"
            prepend-icon="mdi-send-check"
            :loading="dispatchingLoading"
            :disabled="activeExamStats.completed_count === 0 || activeExamStats.is_fully_dispatched"
            @click="openDispatchDialog"
          >
            ترحيل الدرجات للكنترول
          </v-btn>

          <!-- Rollback Dispatch Button -->
          <v-btn
            v-if="activeExamStats.dispatched_count > 0"
            color="warning"
            variant="tonal"
            rounded="lg"
            class="font-weight-bold px-4"
            prepend-icon="mdi-undo-variant"
            :loading="rollbackLoading"
            @click="confirmRollbackDispatch"
          >
            إلغاء الترحيل للتدقيق
          </v-btn>

          <!-- Export Excel / CSV -->
          <v-btn
            color="primary"
            variant="tonal"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-file-excel-outline"
            @click="exportToExcel"
          >
            تصدير الكشف (Excel)
          </v-btn>

          <!-- Print Official Roster -->
          <v-btn
            color="secondary"
            variant="tonal"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-printer-outline"
            @click="printRosterSheet"
          >
            طباعة كشف الكنترول
          </v-btn>

          <!-- Reload / Refresh -->
          <v-btn
            icon="mdi-refresh"
            variant="text"
            color="primary"
            :loading="loadingRecords"
            @click="loadRoster(selectedExamId)"
          />
        </div>
      </div>
    </v-card>

    <!-- ── Student Gradebook Table ──────────────────────────────────── -->
    <v-card class="main-card rounded-2xl overflow-hidden mb-6 elevation-1">
      <v-table hover density="comfortable" class="gradebook-table">
        <thead>
          <tr class="bg-grey-lighten-4">
            <th class="text-right font-weight-black py-4">رقم الجلوس</th>
            <th class="text-right font-weight-black py-4">الرقم السري</th>
            <th class="text-right font-weight-black py-4">اسم الطالب</th>
            <th class="text-center font-weight-black py-4">النموذج</th>
            <th class="text-center font-weight-black py-4">الدرجة المحرزة</th>
            <th class="text-center font-weight-black py-4">النسبة %</th>
            <th class="text-center font-weight-black py-4">التقدير</th>
            <th class="text-center font-weight-black py-4">دقة OMR</th>
            <th class="text-center font-weight-black py-4">حالة التصحيح</th>
            <th class="text-center font-weight-black py-4">الترحيل للكنترول</th>
            <th class="text-center font-weight-black py-4">الإجراءات</th>
          </tr>
        </thead>
        <tbody>
          <!-- Loading state -->
          <tr v-if="loadingRecords">
            <td colspan="11" class="text-center py-8">
              <v-progress-circular indeterminate color="primary" size="36" class="mb-2" />
              <div class="text-caption text-medium-emphasis">جاري تحميل وتدقيق كشف الدرجات...</div>
            </td>
          </tr>

          <!-- Empty state -->
          <tr v-else-if="filteredRecords.length === 0">
            <td colspan="11" class="text-center py-10">
              <v-icon size="48" color="grey-lighten-1" class="mb-2">mdi-clipboard-text-search-outline</v-icon>
              <div class="text-subtitle-1 font-weight-bold text-medium-emphasis">لا توجد سجلات مطابقة للبحث أو التصفية</div>
              <div class="text-caption text-medium-emphasis">تأكد من اختيار الاختبار المناسب ووجود طلاب مسجلين.</div>
            </td>
          </tr>

          <!-- Data rows -->
          <tr
            v-else
            v-for="record in filteredRecords"
            :key="record.registration_id"
            :class="{ 'row-dispatched': record.is_dispatched, 'row-absent': !record.is_present }"
          >
            <!-- Seat Number -->
            <td class="font-weight-black font-mono text-primary">
              {{ record.seat_number }}
            </td>

            <!-- Secret Number -->
            <td class="font-mono text-medium-emphasis">
              {{ record.secret_number }}
            </td>

            <!-- Student Name -->
            <td>
              <div class="font-weight-bold text-on-surface">{{ record.student_name }}</div>
              <div class="text-caption text-medium-emphasis">{{ record.school_name }}</div>
            </td>

            <!-- Version Code -->
            <td class="text-center">
              <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold">
                {{ record.version_code || 'A' }}
              </v-chip>
            </td>

            <!-- Score -->
            <td class="text-center">
              <span v-if="record.status === 'absent'" class="text-caption text-medium-emphasis font-weight-bold">غائب</span>
              <span v-else class="text-subtitle-2 font-weight-black">
                <span :class="record.percentage >= 50 ? 'text-success' : 'text-error'">{{ record.score }}</span>
                <span class="text-caption text-medium-emphasis"> / {{ record.max_score }}</span>
              </span>
            </td>

            <!-- Percentage -->
            <td class="text-center" style="min-width: 110px;">
              <template v-if="record.status !== 'absent'">
                <div class="d-flex align-center justify-center gap-1 mb-1">
                  <span class="text-caption font-weight-bold">{{ record.percentage }}%</span>
                </div>
                <v-progress-linear
                  :model-value="record.percentage"
                  :color="record.percentage >= 50 ? 'success' : 'error'"
                  height="5"
                  rounded
                />
              </template>
              <span v-else class="text-caption text-medium-emphasis">—</span>
            </td>

            <!-- Grade Letter -->
            <td class="text-center">
              <v-chip
                size="small"
                :color="record.grade_color"
                variant="tonal"
                class="font-weight-bold"
              >
                {{ record.grade_code }} • {{ record.grade_name_ar }}
              </v-chip>
            </td>

            <!-- OMR Confidence -->
            <td class="text-center">
              <v-chip
                v-if="record.confidence"
                size="x-small"
                :color="record.confidence >= 0.9 ? 'success' : (record.confidence >= 0.75 ? 'warning' : 'error')"
                variant="tonal"
                class="font-weight-bold"
              >
                {{ Math.round(record.confidence * 100) }}%
              </v-chip>
              <span v-else class="text-caption text-medium-emphasis">—</span>
            </td>

            <!-- Grading Status -->
            <td class="text-center">
              <v-chip
                size="x-small"
                :color="getStatusColor(record.status)"
                variant="flat"
                class="font-weight-bold text-white"
              >
                {{ getStatusDisplay(record.status) }}
              </v-chip>
            </td>

            <!-- Dispatched to Control -->
            <td class="text-center">
              <v-chip
                size="small"
                :color="record.is_dispatched ? 'success' : 'grey-lighten-1'"
                :variant="record.is_dispatched ? 'flat' : 'outlined'"
                class="font-weight-bold"
                :class="{ 'text-white': record.is_dispatched }"
              >
                <v-icon start size="14">{{ record.is_dispatched ? 'mdi-lock-check' : 'mdi-clock-outline' }}</v-icon>
                {{ record.is_dispatched ? 'مرحل ومقفل' : 'غير مرحل' }}
              </v-chip>
            </td>

            <!-- Actions -->
            <td class="text-center">
              <div class="d-flex align-center justify-center gap-1">
                <v-btn
                  v-if="record.submission_id"
                  icon="mdi-file-eye-outline"
                  size="small"
                  variant="text"
                  color="primary"
                  title="معاينة وتدقيق ورقة الإجابة"
                  @click="$router.push(`/omr/submissions/${record.submission_id}`)"
                />
                <v-btn
                  v-else
                  icon="mdi-pencil-off-outline"
                  size="small"
                  variant="text"
                  color="grey"
                  disabled
                />
              </div>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>

    <!-- ── Dispatch Confirmation Modal ──────────────────────────────── -->
    <v-dialog v-model="dispatchDialog" max-width="580" persistent>
      <v-card class="rounded-2xl pa-5">
        <div class="d-flex align-center gap-3 mb-4">
          <v-avatar color="success" variant="tonal" size="48" rounded="lg">
            <v-icon size="28" color="success">mdi-shield-check-outline</v-icon>
          </v-avatar>
          <div>
            <h3 class="text-h6 font-weight-black mb-0">تأكيد ترحيل الدرجات إلى نظام الكنترول</h3>
            <p class="text-caption text-medium-emphasis mb-0">قفل نتائج التصحيح وتثبيت حالة الحضور رسمياً</p>
          </div>
        </div>

        <v-alert
          type="info"
          variant="tonal"
          color="primary"
          rounded="xl"
          class="mb-4 text-body-2"
          icon="mdi-information-outline"
        >
          أنت على وشك ترحيل نتائج <strong class="text-primary">{{ activeExamStats.completed_count }}</strong> ورقة إجابة مصححة ومكتملة إلى نظام الكنترول المركزي.
          سيتم قفل هذه السجلات وتوثيق توقيت الترحيل واسم المسؤول في سجل التدقيق الأكاديمي.
        </v-alert>

        <div class="bg-grey-lighten-5 pa-4 rounded-xl border mb-4">
          <div class="d-flex justify-space-between py-1 border-b">
            <span class="text-caption text-medium-emphasis">اسم الاختبار:</span>
            <span class="text-caption font-weight-bold">{{ selectedExamObj?.title }}</span>
          </div>
          <div class="d-flex justify-space-between py-1 border-b">
            <span class="text-caption text-medium-emphasis">المادة:</span>
            <span class="text-caption font-weight-bold">{{ selectedExamObj?.subject_name }}</span>
          </div>
          <div class="d-flex justify-space-between py-1 border-b">
            <span class="text-caption text-medium-emphasis">عدد السجلات الجاهزة للترحيل:</span>
            <span class="text-caption font-weight-bold text-success">{{ activeExamStats.completed_count }} طالب</span>
          </div>
          <div class="d-flex justify-space-between py-1">
            <span class="text-caption text-medium-emphasis">أوراق تحت المراجعة (لن ترحل):</span>
            <span class="text-caption font-weight-bold text-amber">{{ activeExamStats.needs_review_count }} طالب</span>
          </div>
        </div>

        <v-card-actions class="px-0 pt-2">
          <v-btn
            variant="text"
            color="grey-darken-1"
            class="font-weight-bold"
            @click="dispatchDialog = false"
          >
            إلغاء
          </v-btn>
          <v-spacer />
          <v-btn
            color="success"
            rounded="lg"
            class="font-weight-bold px-6"
            prepend-icon="mdi-check-decagram"
            :loading="dispatchingLoading"
            @click="executeDispatchToControl"
          >
            تأكيد الترحيل الرسمي
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ── Rollback Confirmation Modal ──────────────────────────────── -->
    <v-dialog v-model="rollbackDialog" max-width="520">
      <v-card class="rounded-2xl pa-5">
        <div class="d-flex align-center gap-3 mb-4">
          <v-avatar color="warning" variant="tonal" size="48" rounded="lg">
            <v-icon size="28" color="warning">mdi-undo-variant</v-icon>
          </v-avatar>
          <div>
            <h3 class="text-h6 font-weight-black mb-0">إلغاء ترحيل الدرجات</h3>
            <p class="text-caption text-medium-emphasis mb-0">فك قفل النتائج لإعادة التدقيق بطلب من الكنترول</p>
          </div>
        </div>

        <p class="text-body-2 text-medium-emphasis mb-4">
          هل أنت متأكد من إلغاء ترحيل درجات هذا الاختبار؟ ستتم إعادة السجلات لوضع المراجعة والتدقيق وتوثيق العملية.
        </p>

        <v-card-actions class="px-0 pt-2">
          <v-btn
            variant="text"
            color="grey-darken-1"
            class="font-weight-bold"
            @click="rollbackDialog = false"
          >
            تراجع
          </v-btn>
          <v-spacer />
          <v-btn
            color="warning"
            rounded="lg"
            class="font-weight-bold px-6"
            :loading="rollbackLoading"
            @click="executeRollbackDispatch"
          >
            تأكيد إلغاء الترحيل
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ── Print Layout View (Shown only on print) ───────────────────── -->
    <div class="d-none d-print-block print-roster-container">
      <div class="print-header text-center mb-6">
        <h2 class="font-weight-black mb-1">كشف رصد درجات الاختبار الرسمي</h2>
        <h4 class="text-subtitle-1 mb-2">نظام التصحيح الآلي (OMR) ولجنة الكنترول المركزية</h4>
        <div class="d-flex justify-space-between align-center border-t border-b py-2 px-4 mt-3">
          <span><strong>الاختبار:</strong> {{ selectedExamObj?.title }}</span>
          <span><strong>المادة:</strong> {{ selectedExamObj?.subject_name }}</span>
          <span><strong>العام:</strong> {{ selectedExamObj?.year_name }}</span>
          <span><strong>الدرجة الكلية:</strong> {{ selectedExamObj?.max_score }}</span>
        </div>
      </div>

      <table class="print-table w-100">
        <thead>
          <tr>
            <th>#</th>
            <th>رقم الجلوس</th>
            <th>الرقم السري</th>
            <th>اسم الطالب</th>
            <th>النموذج</th>
            <th>الدرجة</th>
            <th>النسبة %</th>
            <th>التقدير</th>
            <th>حالة الحضور</th>
            <th>ملاحظات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(rec, idx) in filteredRecords" :key="rec.registration_id">
            <td class="text-center">{{ idx + 1 }}</td>
            <td class="text-center">{{ rec.seat_number }}</td>
            <td class="text-center">{{ rec.secret_number }}</td>
            <td>{{ rec.student_name }}</td>
            <td class="text-center">{{ rec.version_code }}</td>
            <td class="text-center font-weight-bold">{{ rec.status === 'absent' ? 'غائب' : rec.score }}</td>
            <td class="text-center">{{ rec.status === 'absent' ? '—' : rec.percentage + '%' }}</td>
            <td class="text-center">{{ rec.grade_code }}</td>
            <td class="text-center">{{ rec.is_present ? 'حاضر' : 'غائب' }}</td>
            <td class="text-center">{{ rec.is_dispatched ? 'مرحل للكنترول' : '' }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Signatures Footer -->
      <div class="d-flex justify-space-between align-center mt-10 pt-6 px-4 text-center">
        <div>
          <p class="font-weight-bold mb-8">مصحح ومسؤول الـ OMR</p>
          <p>.......................................</p>
        </div>
        <div>
          <p class="font-weight-bold mb-8">أستاذ مقرر المادة</p>
          <p>.......................................</p>
        </div>
        <div>
          <p class="font-weight-bold mb-8">رئيس لجنة الكنترول</p>
          <p>.......................................</p>
        </div>
        <div>
          <p class="font-weight-bold mb-8">عميد الكلية / المدير</p>
          <p>.......................................</p>
        </div>
      </div>
    </div>

    <!-- Snackbar Notifications -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="4000" location="top left">
      {{ snackbar.text }}
      <template #actions>
        <v-btn variant="text" @click="snackbar.show = false">إغلاق</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { gradebookAPI, examsAPI } from '@/services/omr/endpoints'

export default {
  name: 'OMRGradebookView',

  data() {
    return {
      loadingExams: false,
      loadingRecords: false,
      dispatchingLoading: false,
      rollbackLoading: false,

      examsList: [],
      selectedExamId: null,
      selectedExamObj: null,

      allRecords: [],
      activeExamStats: {
        total_students: 0,
        completed_count: 0,
        needs_review_count: 0,
        absent_count: 0,
        average_score: 0,
        pass_rate: 0,
        dispatched_count: 0,
        is_fully_dispatched: false,
      },

      // Filters
      searchQuery: '',
      filterStatus: null,
      filterDispatch: null,

      statusFilterOptions: [
        { text: 'الكل', value: null },
        { text: 'مصححة ومكتملة', value: 'completed' },
        { text: 'تحت التدقيق', value: 'needs_review' },
        { text: 'غائب', value: 'absent' },
      ],

      dispatchFilterOptions: [
        { text: 'الكل', value: null },
        { text: 'مرحل للكنترول', value: 'dispatched' },
        { text: 'غير مرحل', value: 'not_dispatched' },
      ],

      // Dialogs
      dispatchDialog: false,
      rollbackDialog: false,

      snackbar: {
        show: false,
        text: '',
        color: 'success',
      },
    }
  },

  computed: {
    filteredRecords() {
      let list = this.allRecords || []

      if (this.searchQuery && this.searchQuery.trim()) {
        const q = this.searchQuery.trim().toLowerCase()
        list = list.filter(r =>
          (r.student_name && r.student_name.toLowerCase().includes(q)) ||
          (String(r.seat_number).toLowerCase().includes(q)) ||
          (String(r.secret_number).toLowerCase().includes(q))
        )
      }

      if (this.filterStatus) {
        list = list.filter(r => r.status === this.filterStatus)
      }

      if (this.filterDispatch === 'dispatched') {
        list = list.filter(r => r.is_dispatched)
      } else if (this.filterDispatch === 'not_dispatched') {
        list = list.filter(r => !r.is_dispatched)
      }

      return list
    },
  },

  async created() {
    await this.fetchExamsList()

    // If query param exam is passed
    if (this.$route.query.exam) {
      this.selectedExamId = parseInt(this.$route.query.exam) || this.$route.query.exam
      this.loadRoster(this.selectedExamId)
    }
  },

  methods: {
    notify(text, color = 'success') {
      this.snackbar.text = text
      this.snackbar.color = color
      this.snackbar.show = true
    },

    async fetchExamsList() {
      this.loadingExams = true
      try {
        const res = await gradebookAPI.list()
        const data = res.data
        if (data && data.results) {
          this.examsList = data.results
        } else if (Array.isArray(data)) {
          this.examsList = data
        }

        // Auto select first exam if not selected
        if (!this.selectedExamId && this.examsList.length > 0) {
          this.selectedExamId = this.examsList[0].id
          await this.loadRoster(this.selectedExamId)
        }
      } catch (err) {
        console.error('Error fetching exams for gradebook:', err)
        // Fallback to general exams list if gradebook list has issue
        try {
          const exRes = await examsAPI.list()
          const exData = exRes.data?.results || exRes.data || []
          this.examsList = exData.map(e => ({
            id: e.id,
            title: e.title,
            uniqueCode: e.uniqueCode,
            subject_name: e.subject?.name_ar || e.subject || '',
            total_students: 0,
            completed_count: 0,
            dispatched_count: 0,
            is_fully_dispatched: false,
          }))
          if (this.examsList.length > 0 && !this.selectedExamId) {
            this.selectedExamId = this.examsList[0].id
            await this.loadRoster(this.selectedExamId)
          }
        } catch (exErr) {
          this.notify('تعذر جلب قائمة الاختبارات', 'error')
        }
      } finally {
        this.loadingExams = false
      }
    },

    async onExamChange(examId) {
      if (!examId) {
        this.selectedExamObj = null
        this.allRecords = []
        this.resetStats()
        return
      }
      await this.loadRoster(examId)
    },

    resetStats() {
      this.activeExamStats = {
        total_students: 0,
        completed_count: 0,
        needs_review_count: 0,
        absent_count: 0,
        average_score: 0,
        pass_rate: 0,
        dispatched_count: 0,
        is_fully_dispatched: false,
      }
    },

    async loadRoster(examId) {
      if (!examId) return
      this.loadingRecords = true
      try {
        const res = await gradebookAPI.getRoster(examId)
        const data = res.data
        if (data.success) {
          this.selectedExamObj = data.exam
          this.allRecords = data.records || []

          // Calculate summary stats
          const total = this.allRecords.length
          const completed = this.allRecords.filter(r => r.status === 'completed')
          const needsReview = this.allRecords.filter(r => r.status === 'needs_review')
          const absent = this.allRecords.filter(r => r.status === 'absent')
          const dispatched = this.allRecords.filter(r => r.is_dispatched)

          const sumScore = completed.reduce((acc, r) => acc + (r.score || 0), 0)
          const maxScore = data.exam?.max_score || 100
          const avgPercent = completed.length > 0 ? (sumScore / (completed.length * maxScore)) * 100 : 0
          const passedCount = completed.filter(r => r.percentage >= 50).length
          const passRate = completed.length > 0 ? (passedCount / completed.length) * 100 : 0

          this.activeExamStats = {
            total_students: total,
            completed_count: completed.length,
            needs_review_count: needsReview.length,
            absent_count: absent.length,
            average_score: Math.round(avgPercent * 10) / 10,
            pass_rate: Math.round(passRate * 10) / 10,
            dispatched_count: dispatched.length,
            is_fully_dispatched: dispatched.length >= completed.length && completed.length > 0,
          }
        }
      } catch (err) {
        console.error('Error loading gradebook roster:', err)
        this.notify('تعذر تحميل كشف درجات الاختبار', 'error')
      } finally {
        this.loadingRecords = false
      }
    },

    openDispatchDialog() {
      this.dispatchDialog = true
    },

    async executeDispatchToControl() {
      if (!this.selectedExamId) return
      this.dispatchingLoading = true
      try {
        const res = await gradebookAPI.dispatchToControl(this.selectedExamId, {})
        if (res.data?.success) {
          this.notify(res.data.message || 'تم ترحيل الدرجات بنجاح لنظام الكنترول', 'success')
          this.dispatchDialog = false
          await this.loadRoster(this.selectedExamId)
          await this.fetchExamsList()
        } else {
          this.notify(res.data?.message || 'حدث خطأ أثناء الترحيل', 'error')
        }
      } catch (err) {
        console.error('Error dispatching to control:', err)
        const msg = err.response?.data?.message || 'تعذر الترحيل لنظام الكنترول'
        this.notify(msg, 'error')
      } finally {
        this.dispatchingLoading = false
      }
    },

    confirmRollbackDispatch() {
      this.rollbackDialog = true
    },

    async executeRollbackDispatch() {
      if (!this.selectedExamId) return
      this.rollbackLoading = true
      try {
        const res = await gradebookAPI.rollbackDispatch(this.selectedExamId, {})
        if (res.data?.success) {
          this.notify(res.data.message || 'تم إلغاء الترحيل وإعادة السجلات للمراجعة', 'warning')
          this.rollbackDialog = false
          await this.loadRoster(this.selectedExamId)
          await this.fetchExamsList()
        }
      } catch (err) {
        console.error('Error rolling back dispatch:', err)
        this.notify('تعذر إلغاء ترحيل الدرجات', 'error')
      } finally {
        this.rollbackLoading = false
      }
    },

    exportToExcel() {
      if (!this.filteredRecords.length) {
        this.notify('لا توجد بيانات لتصديرها', 'warning')
        return
      }

      const rows = [
        ['م', 'رقم الجلوس', 'الرقم السري', 'اسم الطالب', 'النموذج', 'الدرجة', 'الدرجة الكلية', 'النسبة %', 'التقدير', 'حالة التصحيح', 'حالة الترحيل للكنترول']
      ]

      this.filteredRecords.forEach((r, idx) => {
        rows.push([
          idx + 1,
          r.seat_number,
          r.secret_number || '—',
          `"${r.student_name || ''}"`,
          r.version_code || 'A',
          r.status === 'absent' ? 'غائب' : r.score,
          r.max_score,
          r.status === 'absent' ? 0 : r.percentage,
          `"${r.grade_code} - ${r.grade_name_ar}"`,
          r.status,
          r.is_dispatched ? 'مرحل للكنترول' : 'غير مرحل'
        ])
      })

      const csvContent = 'data:text/csv;charset=utf-8,\uFEFF' + rows.map(e => e.join(',')).join('\n')
      const encodedUri = encodeURI(csvContent)
      const link = document.createElement('a')
      link.setAttribute('href', encodedUri)
      link.setAttribute('download', `كشف_درجات_الكنترول_${this.selectedExamObj?.title || 'exam'}.csv`)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      this.notify('تم تصدير كشف الدرجات بنجاح', 'success')
    },

    printRosterSheet() {
      window.print()
    },

    getStatusColor(st) {
      const map = {
        completed: 'success',
        needs_review: 'amber-darken-2',
        failed: 'error',
        processing: 'info',
        pending: 'grey',
        absent: 'grey-darken-1',
      }
      return map[st] || 'grey'
    },

    getStatusDisplay(st) {
      const map = {
        completed: 'مكتمل ومعتمد',
        needs_review: 'تدقيق يدوي',
        failed: 'فشل المعالجة',
        processing: 'قيد المعالجة',
        pending: 'في الانتظار',
        absent: 'غائب',
      }
      return map[st] || st
    },
  },
}
</script>

<style scoped>
.qb-gradebook-view-v4 {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

.stat-glass-card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.04);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-glass-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.08);
}

.stat-icon-wrapper {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-indigo-gradient { background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%); }
.bg-emerald-gradient { background: linear-gradient(135deg, #10b981 0%, #047857 100%); }
.bg-amber-gradient { background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%); }
.bg-rose-gradient { background: linear-gradient(135deg, #f43f5e 0%, #be123c 100%); }
.bg-teal-gradient { background: linear-gradient(135deg, #14b8a6 0%, #0f766e 100%); }
.bg-purple-gradient { background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%); }

.shadow-indigo { box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.12); }
.shadow-emerald { box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.12); }
.shadow-amber { box-shadow: 0 4px 14px 0 rgba(245, 158, 11, 0.12); }
.shadow-rose { box-shadow: 0 4px 14px 0 rgba(244, 63, 94, 0.12); }
.shadow-teal { box-shadow: 0 4px 14px 0 rgba(20, 184, 166, 0.12); }
.shadow-purple { box-shadow: 0 4px 14px 0 rgba(139, 92, 246, 0.12); }

.gradebook-table th {
  font-size: 0.85rem !important;
  color: #374151 !important;
}

.gradebook-table td {
  font-size: 0.875rem !important;
  border-bottom: 1px solid #f1f5f9 !important;
}

.row-dispatched {
  background-color: rgba(16, 185, 129, 0.03);
}

.row-absent {
  background-color: rgba(244, 63, 94, 0.02);
}

.font-mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

/* ── Print Specific Styles ────────────────────────────────────────── */
@media print {
  body * {
    visibility: hidden;
  }
  .print-roster-container,
  .print-roster-container * {
    visibility: visible;
  }
  .print-roster-container {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    padding: 20px;
    background: white;
  }
  .print-table {
    border-collapse: collapse;
    width: 100%;
    margin-top: 15px;
  }
  .print-table th,
  .print-table td {
    border: 1px solid #333;
    padding: 6px 8px;
    font-size: 11pt;
  }
  .print-table th {
    background-color: #eee !important;
  }
}
</style>
