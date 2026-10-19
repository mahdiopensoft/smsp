<template>
  <div class="qb-gradebook-view-v4">
    <!-- ── Page Header (Institutional OpenSoftCore Style) ─────────────── -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-4">
      <div class="d-flex align-center">
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
        <!-- الزر المباشر لشاشة سجل الأوراق المصححة -->
        <v-btn
          color="indigo-darken-1"
          variant="flat"
          class="font-weight-bold text-white px-4 rounded-xl shadow-indigo"
          prepend-icon="mdi-file-document-check-outline"
          @click="$router.push(`/omr/submissions${selectedExamId ? '?exam=' + selectedExamId : ''}`)"
        >
          سجل الأوراق المصححة (Submissions)
          <v-chip size="x-small" color="white" variant="outlined" class="ms-2 font-weight-black" v-if="activeExamStats.completed_count">
            {{ activeExamStats.completed_count }}
          </v-chip>
        </v-btn>

        <custom-btn
          type="add"
          :click="() => $router.push('/omr/scanner-lab')"
          label="معمل المسح الضوئي"
          color="primary"
          variant="tonal"
          class="font-weight-bold"
        />

        <custom-btn
          type="restore"
          :click="() => $router.push('/omr/dashboard')"
          label="لوحة التحكم"
          color="secondary"
          variant="tonal"
          class="font-weight-bold"
        />
      </div>
    </div>

    <!-- ── OMR Workflow Stepper (مسار مراحل التصحيح الآلي والكنترول خطوة بخطوة) ── -->
    <omr-workflow-bar :active-step="6" :exam-id="selectedExamId" />

    <!-- ── Filter & Exam Selector Card (الفلاتر الموحدة المتطابقة مع بنك الأسئلة والشاشات الموحدة) ── -->
    <filter-fields label="اختيار وتصفية الاختبار وكشوفات الرصد والكنترول" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- نوع المؤسسة التعليمية (مدارس / جامعات / معاهد) موحد كـ auto-list -->
        <auto-list
          v-model="filterInstitutionType"
          name="InstitutionType"
          placeholder="نوع المؤسسة التعليمية"
          cols="3"
          :add="false"
          @update:model-value="onInstitutionTypeChange"
        />

        <!-- فلاتر المدارس -->
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
            @update:model-value="applyFilters"
          />
          <auto-list
            v-model="filterSubject"
            name="Subject"
            :param="subjectFilterParam"
            placeholder="المادة الدراسية"
            :cols="filterInstitutionType === 'school' ? '3' : '9'"
            :add="false"
            @update:model-value="onSubjectChange"
          />
        </template>

        <!-- فلاتر الجامعات -->
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
            @update:model-value="selectedExamId = null"
          />
        </template>

        <!-- فلاتر المعاهد -->
        <template v-if="filterInstitutionType === 'institute'">
          <auto-list
            v-model="filterInstituteField"
            name="InstituteField"
            placeholder="المجال المهني"
            cols="3"
            :add="false"
            @update:model-value="() => { filterInstituteEducationSystem = null; filterInstituteSpecialization = null; filterInstituteCurriculum = null; filterInstituteSubject = null; selectedExamId = null; }"
          />
          <auto-list
            v-model="filterInstituteEducationSystem"
            name="InstituteEducationSystem"
            :param="filterInstituteField"
            placeholder="نظام التعليم"
            cols="3"
            :add="false"
            :disabled="!filterInstituteField"
            @update:model-value="() => { filterInstituteSpecialization = null; filterInstituteCurriculum = null; filterInstituteSubject = null; selectedExamId = null; }"
          />
          <auto-list
            v-model="filterInstituteSpecialization"
            name="InstituteSpecialization"
            :param="{ field: filterInstituteField, education_system: filterInstituteEducationSystem }"
            placeholder="التخصص المهني"
            cols="3"
            :add="false"
            :disabled="!filterInstituteEducationSystem"
            @update:model-value="() => { filterInstituteCurriculum = null; filterInstituteSubject = null; selectedExamId = null; }"
          />
          <auto-list
            v-model="filterInstituteSubject"
            name="InstituteSubject"
            :param="filterInstituteSpecialization"
            placeholder="المادة التدريبية"
            cols="3"
            :add="false"
            @update:model-value="selectedExamId = null"
          />
        </template>

        <!-- الهيكلية الجغرافية والمؤسسية + اختيار الاختبار (4 أعمدة متساوية cols="3") -->
        <!-- المحافظة -->
        <auto-list
          v-model="filterGovernorate"
          name="Governorate"
          placeholder="المحافظة"
          cols="3"
          :add="false"
          @update:model-value="onGovernorateChange"
        />

        <!-- المديرية -->
        <auto-list
          v-model="filterDirectorate"
          name="Directorate"
          :param="filterGovernorate"
          :placeholder="filterGovernorate ? 'اختر المديرية التابعة للمحافظة' : 'اختر المحافظة أولاً'"
          cols="3"
          :add="false"
          :disabled="!filterGovernorate"
          @update:model-value="onDirectorateChange"
        />

        <!-- المدرسة / المؤسسة -->
        <auto-list
          v-model="filterOrganization"
          name="Organization"
          :param="orgParam"
          :placeholder="orgPlaceholder"
          cols="3"
          :add="false"
          @update:model-value="applyFilters"
        />

        <!-- اختيار الاختبار الأكاديمي المعتمد -->
        <auto-list
          v-model="selectedExamId"
          name="Exam"
          :param="examFilterParam"
          placeholder="اختر الاختبار الأكاديمي لعرض كشف درجاته..."
          cols="3"
          :add="false"
          @update:model-value="onExamChange"
        />

        <!-- البحث الفوري -->
        <v-col cols="12" sm="6" md="3" class="py-2">
          <v-text-field
            v-model="searchQuery"
            label="بحث بالاسم أو رقم الجلوس أو السري..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            hide-details
            @update:model-value="onSearchInput"
            @keydown.enter="applyFilters"
            @click:clear="onClearSearch"
          />
        </v-col>

        <!-- النموذج -->
        <v-col cols="6" sm="3" md="2" class="py-2">
          <v-select
            v-model="filterVersion"
            :items="versionFilterOptions"
            item-title="text"
            item-value="value"
            label="النموذج"
            prepend-inner-icon="mdi-file-document-multiple-outline"
            clearable
            density="compact"
            variant="outlined"
            hide-details
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- التقدير الأكاديمي -->
        <v-col cols="6" sm="3" md="2" class="py-2">
          <v-select
            v-model="filterGrade"
            :items="gradeFilterOptions"
            item-title="text"
            item-value="value"
            label="التقدير الأكاديمي"
            prepend-inner-icon="mdi-medal-outline"
            clearable
            density="compact"
            variant="outlined"
            hide-details
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- حالة التصحيح -->
        <v-col cols="6" sm="3" md="2" class="py-2">
          <v-select
            v-model="filterStatus"
            :items="statusFilterOptions"
            item-title="text"
            item-value="value"
            label="حالة التصحيح"
            prepend-inner-icon="mdi-clipboard-check-outline"
            clearable
            density="compact"
            variant="outlined"
            hide-details
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- أزرار الإجراءات الموحدة (تحديث وتفريغ) -->
        <v-col cols="12" sm="12" md="3" class="d-flex align-center gap-2 py-2">
          <custom-btn
            type="show"
            label="تحديث الكشف"
            color="primary"
            class="font-weight-bold flex-grow-1"
            :loading="loadingRecords"
            :click="applyFilters"
          />
          <custom-btn
            type="cancel_filter"
            label="تفريغ الفلاتر"
            variant="tonal"
            color="error"
            class="font-weight-bold"
            :click="resetFilters"
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
              • الطلاب: <span class="font-weight-bold text-primary">{{ activeExamStats.total_students || totalRecordsCount }}</span> طالب مسجل في الكشف
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

          <!-- Psychometrics Button -->
          <v-btn
            color="purple-darken-1"
            variant="tonal"
            rounded="lg"
            class="font-weight-bold px-3"
            prepend-icon="mdi-chart-bell-curve-cumulative"
            :loading="psychometricsLoading"
            :disabled="!selectedExamId"
            @click="openPsychometricsDialog"
          >
            التحليل السيكومتري (Item Analysis)
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
            تصدير كشف الكنترول (Excel/CSV)
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

    <!-- ── Selected Students Batch Bar (شريط عمليات الطلاب المحددين) ── -->
    <v-card v-if="selectedStudentIds.length > 0" class="main-card pa-3 mb-4 rounded-xl border elevation-2" color="primary" variant="tonal">
      <div class="d-flex align-center justify-space-between flex-wrap gap-3">
        <div class="d-flex align-center gap-2">
          <v-chip color="primary" variant="flat" class="font-weight-black">
            {{ selectedStudentIds.length }}
          </v-chip>
          <span class="font-weight-bold text-subtitle-2">
            طالب محدد في الكشف حالياً
          </span>
        </div>
        <div class="d-flex align-center gap-2 flex-wrap">
          <v-btn
            size="small"
            color="primary"
            class="font-weight-bold px-4"
            prepend-icon="mdi-bank-transfer-in"
            :loading="dispatchingLoading"
            @click="dispatchSelectedToControl"
          >
            ترحيل المحدد للكنترول ({{ selectedStudentIds.length }})
          </v-btn>
          <v-btn
            size="small"
            variant="text"
            color="error"
            prepend-icon="mdi-close"
            @click="selectedStudentIds = []"
          >
            إلغاء التحديد
          </v-btn>
        </div>
      </div>
    </v-card>

    <!-- ── Student Gradebook Table (Component with Server-Side Pagination) ── -->
    <div class="main-card rounded-2xl overflow-hidden mb-6 elevation-1">
      <!-- ── شريط إدارة التحديد والتحكم السريع في الكشف ── -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-2 px-4 py-3 bg-surface border-b">
        <div class="d-flex align-center gap-3">
          <v-checkbox-btn
            :model-value="isAllCurrentSelected"
            :indeterminate="isSomeCurrentSelected"
            color="primary"
            density="compact"
            hide-details
            @update:model-value="toggleSelectAllCurrent"
          />
          <span class="text-caption font-weight-bold text-on-surface">
            تحديد الكل في هذه الصفحة
          </span>
          <v-chip
            v-if="selectedStudentIds.length > 0"
            size="small"
            color="primary"
            variant="flat"
            class="font-weight-black"
          >
            {{ selectedStudentIds.length }} طالب محدد
          </v-chip>
          <v-btn
            v-if="selectedStudentIds.length > 0"
            size="x-small"
            variant="text"
            color="error"
            class="font-weight-bold"
            @click="selectedStudentIds = []"
          >
            إلغاء التحديد
          </v-btn>
        </div>

        <div class="d-flex align-center gap-2">
          <v-btn
            v-if="selectedStudentIds.length > 0"
            color="purple-darken-1"
            variant="flat"
            size="small"
            class="font-weight-bold text-white rounded-lg px-4"
            prepend-icon="mdi-bank-transfer"
            :loading="dispatchingLoading"
            @click="dispatchSelectedToControl"
          >
            ترحيل درجات المحدد ({{ selectedStudentIds.length }}) للكنترول
          </v-btn>
          <span class="text-caption text-medium-emphasis">
            إجمالي السجلات: {{ tableItems.pagination?.total || tableItems.pagination?.count || totalRecordsCount }} طالب
          </span>
        </div>
      </div>

      <custom-data-table
        v-model="selectedStudentIds"
        :headers="headers"
        :items="tableItems"
        :getData="fetchGradebookRoster"
        :customLoading="loadingRecords"
        class="bg-transparent"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :showSelect="false"
        :itemValue="'registration_id'"
        :actions="false"
      >
        <template v-slot:item-slot="{ item, key }">
          <!-- Selection Checkbox Column -->
          <template v-if="key === 'select'">
            <v-checkbox-btn
              :model-value="selectedStudentIds.includes(item.registration_id)"
              color="primary"
              density="compact"
              hide-details
              @update:model-value="toggleStudentSelection(item.registration_id)"
            />
          </template>

          <!-- Seat Number -->
          <template v-else-if="key === 'seat_number'">
            <span class="font-weight-black font-mono text-primary">
              {{ item.seat_number }}
            </span>
          </template>

          <!-- Secret Number -->
          <template v-else-if="key === 'secret_number'">
            <span class="font-mono text-medium-emphasis">
              {{ item.secret_number }}
            </span>
          </template>

          <!-- Student Name -->
          <template v-else-if="key === 'student_name'">
            <div class="py-1">
              <div class="font-weight-bold text-on-surface">{{ item.student_name }}</div>
              <div class="text-caption text-medium-emphasis">{{ item.school_name }}</div>
            </div>
          </template>

          <!-- School / Organization -->
          <template v-else-if="key === 'school_name'">
            <v-chip size="small" color="primary" variant="tonal" class="font-weight-medium" v-if="item.school_name">
              <v-icon start size="14">mdi-domain</v-icon>
              {{ item.school_name }}
            </v-chip>
            <span v-else class="text-medium-emphasis">—</span>
          </template>

          <!-- Governorate / Directorate -->
          <template v-else-if="key === 'governorate_name'">
            <div class="py-1">
              <div class="text-caption font-weight-bold">
                <v-icon size="13" class="me-1 text-primary">mdi-map-marker-outline</v-icon>
                {{ item.governorate_name || '—' }}
              </div>
              <div class="text-caption text-medium-emphasis" v-if="item.directorate_name">
                {{ item.directorate_name }}
              </div>
            </div>
          </template>

          <!-- Version Code -->
          <template v-else-if="key === 'version_code'">
            <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold">
              {{ item.version_code || 'A' }}
            </v-chip>
          </template>

          <!-- Score -->
          <template v-else-if="key === 'score'">
            <span v-if="item.status === 'absent'" class="text-caption text-medium-emphasis font-weight-bold">غائب</span>
            <span v-else class="text-subtitle-2 font-weight-black">
              <span :class="item.percentage >= 50 ? 'text-success' : 'text-error'">{{ item.score }}</span>
              <span class="text-caption text-medium-emphasis"> / {{ item.max_score }}</span>
            </span>
          </template>

          <!-- Percentage -->
          <template v-else-if="key === 'percentage'">
            <div style="min-width: 100px;">
              <template v-if="item.status !== 'absent'">
                <div class="d-flex align-center justify-center gap-1 mb-1">
                  <span class="text-caption font-weight-bold">{{ item.percentage }}%</span>
                </div>
                <v-progress-linear
                  :model-value="item.percentage"
                  :color="item.percentage >= 50 ? 'success' : 'error'"
                  height="5"
                  rounded
                />
              </template>
              <span v-else class="text-caption text-medium-emphasis">—</span>
            </div>
          </template>

          <!-- Grade Letter -->
          <template v-else-if="key === 'grade_code'">
            <v-chip
              size="small"
              :color="item.grade_color"
              variant="tonal"
              class="font-weight-bold"
            >
              {{ item.grade_code }} • {{ item.grade_name_ar }}
            </v-chip>
          </template>

          <!-- OMR Confidence -->
          <template v-else-if="key === 'confidence'">
            <v-chip
              v-if="item.confidence"
              size="x-small"
              :color="item.confidence >= 0.9 ? 'success' : (item.confidence >= 0.75 ? 'warning' : 'error')"
              variant="tonal"
              class="font-weight-bold"
            >
              {{ Math.round(item.confidence * 100) }}%
            </v-chip>
            <span v-else class="text-caption text-medium-emphasis">—</span>
          </template>

          <!-- Grading Status -->
          <template v-else-if="key === 'status'">
            <v-chip
              size="x-small"
              :color="getStatusColor(item.status)"
              variant="flat"
              class="font-weight-bold text-white"
            >
              {{ getStatusDisplay(item.status) }}
            </v-chip>
          </template>

          <!-- Dispatched to Control -->
          <template v-else-if="key === 'is_dispatched'">
            <v-chip
              size="small"
              :color="item.is_dispatched ? 'success' : 'grey-lighten-1'"
              :variant="item.is_dispatched ? 'flat' : 'outlined'"
              class="font-weight-bold"
              :class="{ 'text-white': item.is_dispatched }"
            >
              <v-icon start size="14">{{ item.is_dispatched ? 'mdi-lock-check' : 'mdi-clock-outline' }}</v-icon>
              {{ item.is_dispatched ? 'مرحل ومقفل' : 'غير مرحل' }}
            </v-chip>
          </template>

          <!-- Actions -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-1">
              <v-btn
                v-if="item.submission_id"
                icon="mdi-file-eye-outline"
                size="small"
                variant="text"
                color="primary"
                title="معاينة وتدقيق ورقة الإجابة"
                @click="$router.push(`/omr/submissions/${item.submission_id}`)"
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
          </template>
        </template>
      </custom-data-table>
    </div>

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

    <!-- ── Psychometrics & Item Analysis Modal ───────────────────────── -->
    <v-dialog v-model="psychometricsDialog" max-width="1100" scrollable>
      <v-card class="rounded-2xl overflow-hidden" v-if="psychometricsData">
        <v-card-title class="d-flex align-center justify-space-between bg-surface-variant px-6 py-4 border-b">
          <div class="d-flex align-center gap-3">
            <v-avatar color="purple" variant="tonal" size="44" rounded="lg">
              <v-icon size="26" color="purple-darken-2">mdi-chart-bell-curve-cumulative</v-icon>
            </v-avatar>
            <div>
              <h3 class="text-h6 font-weight-black mb-0">التحليل السيكومتري وتحليل الفقرات (Item Analysis)</h3>
              <p class="text-caption text-medium-emphasis mb-0">
                قياس ثبات الاختبار (Cronbach's Alpha) ومؤشرات الصعوبة والتمييز وكفاءة المشتتات
              </p>
            </div>
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" @click="psychometricsDialog = false" />
        </v-card-title>

        <v-card-text class="pa-6" style="max-height: 75vh;">
          <!-- ملخص ثبات الاختبار والعينة -->
          <v-row class="mb-4">
            <v-col cols="12" sm="4">
              <v-card variant="tonal" color="purple" class="pa-4 rounded-xl text-center border">
                <div class="text-caption font-weight-bold text-medium-emphasis mb-1">معامل ثبات ألفا كرونباخ (α)</div>
                <div class="text-h4 font-weight-black text-purple-darken-2 font-mono">
                  {{ psychometricsData.cronbach_alpha != null ? psychometricsData.cronbach_alpha : '—' }}
                </div>
                <v-chip size="x-small" color="purple" variant="flat" class="font-weight-black mt-2">
                  {{ psychometricsData.cronbach_quality || 'يتطلب مزيداً من البيانات' }}
                </v-chip>
              </v-card>
            </v-col>

            <v-col cols="12" sm="4">
              <v-card variant="tonal" color="primary" class="pa-4 rounded-xl text-center border">
                <div class="text-caption font-weight-bold text-medium-emphasis mb-1">حجم العينة المصححة ضوئياً</div>
                <div class="text-h4 font-weight-black text-primary font-mono">
                  {{ psychometricsData.sample_size || 0 }}
                </div>
                <div class="text-caption text-medium-emphasis mt-2">ورقة إجابة مكتملة</div>
              </v-card>
            </v-col>

            <v-col cols="12" sm="4">
              <v-card variant="tonal" color="info" class="pa-4 rounded-xl text-center border">
                <div class="text-caption font-weight-bold text-medium-emphasis mb-1">إجمالي الفقرات المحللة</div>
                <div class="text-h4 font-weight-black text-info font-mono">
                  {{ psychometricsData.items_count || 0 }}
                </div>
                <div class="text-caption text-medium-emphasis mt-2">فقرة امتحانية</div>
              </v-card>
            </v-col>
          </v-row>

          <v-alert
            v-if="psychometricsData.sample_size < 2"
            type="info"
            variant="tonal"
            class="rounded-xl font-weight-bold mb-4"
          >
            {{ psychometricsData.message || 'يتطلب التحليل السيكومتري تصحيح ورقتي إجابة على الأقل لاحتساب التباين ومعاملات الصعوبة.' }}
          </v-alert>

          <!-- جدول تحليل الفقرات التفصيلي -->
          <div v-if="psychometricsData.items && psychometricsData.items.length > 0">
            <h4 class="text-subtitle-1 font-weight-black mb-3">مؤشرات صعوبة وتمييز الفقرات الامتحانية:</h4>
            <v-table class="border rounded-xl" density="comfortable">
              <thead>
                <tr class="bg-surface-variant font-weight-bold">
                  <th class="text-center font-weight-bold">رقم الفقرة</th>
                  <th class="text-center font-weight-bold">المفتاح</th>
                  <th class="text-center font-weight-bold">معامل الصعوبة (P)</th>
                  <th class="text-center font-weight-bold">معامل التمييز (D)</th>
                  <th class="text-center font-weight-bold">التقييم المعياري</th>
                  <th class="text-center font-weight-bold">توزيع الإجابات (المشتتات)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in psychometricsData.items" :key="item.question_number">
                  <td class="text-center font-mono font-weight-black">{{ item.question_number }}</td>
                  <td class="text-center">
                    <v-chip size="x-small" color="primary" variant="flat" class="font-weight-black">
                      {{ item.correct_choice }}
                    </v-chip>
                  </td>
                  <td class="text-center font-mono font-weight-bold">
                    {{ (item.difficulty_index * 100).toFixed(1) }}%
                  </td>
                  <td class="text-center font-mono font-weight-bold">
                    {{ item.discrimination_index }}
                  </td>
                  <td class="text-center">
                    <v-chip size="x-small" :color="item.quality_color" variant="tonal" class="font-weight-black">
                      {{ item.quality_badge }}
                    </v-chip>
                  </td>
                  <td class="text-center">
                    <div class="d-flex align-center justify-center gap-1 flex-wrap">
                      <span
                        v-for="(count, opt) in item.choices_distribution"
                        :key="opt"
                        class="text-caption font-mono px-1 rounded"
                        :class="opt === item.correct_choice ? 'bg-success text-white font-weight-bold' : (count > 0 ? 'bg-grey-lighten-3' : 'text-disabled')"
                      >
                        {{ opt }}: {{ count }}
                      </span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </div>
        </v-card-text>

        <v-card-actions class="px-6 py-4 bg-surface-variant border-t">
          <v-spacer />
          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            class="font-weight-bold px-6"
            @click="psychometricsDialog = false"
          >
            إغلاق
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
          <tr v-for="(rec, idx) in printRecordsList" :key="rec.registration_id">
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
import OMRWorkflowBar from '@/components/OMRWorkflowBar.vue'

export default {
  name: 'OMRGradebookView',

  components: {
    OMRWorkflowBar,
  },

  data() {
    return {
      showAdvancedFilters: true,
      loadingExams: false,
      loadingRecords: false,
      dispatchingLoading: false,
      rollbackLoading: false,

      examsList: [],
      selectedExamId: null,
      selectedExamObj: null,

      totalRecordsCount: 0,
      tableItems: {
        results: [],
        pagination: { count: 0, num_pages: 1, current_page: 1, page_size: 10, total: 0 }
      },
      printRecords: [],

      headers: [
        { title: "تحديد", key: "select", sortable: false, align: "center", width: "60px" },
        { title: "رقم الجلوس", key: "seat_number", sortable: true, align: "center", width: "115px" },
        { title: "الرقم السري", key: "secret_number", sortable: true, align: "center", width: "105px" },
        { title: "اسم الطالب", key: "student_name", sortable: true, align: "start" },
        { title: "المدرسة / المؤسسة", key: "school_name", sortable: true, align: "start" },
        { title: "المحافظة", key: "governorate_name", sortable: true, align: "center", width: "120px" },
        { title: "النموذج", key: "version_code", sortable: true, align: "center", width: "85px" },
        { title: "الدرجة المحرزة", key: "score", sortable: true, align: "center", width: "130px" },
        { title: "النسبة %", key: "percentage", sortable: true, align: "center", width: "120px" },
        { title: "التقدير", key: "grade_code", sortable: true, align: "center", width: "135px" },
        { title: "دقة OMR", key: "confidence", sortable: true, align: "center", width: "95px" },
        { title: "حالة التصحيح", key: "status", sortable: true, align: "center", width: "115px" },
        { title: "الترحيل للكنترول", key: "is_dispatched", sortable: true, align: "center", width: "135px" },
        { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "90px" },
      ],

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

      // Selection (تحديد الطلاب لعمليات الكنترول والترحيل المجمعة)
      selectedStudentIds: [],

      // Filters (مطابقة لشاشة نماذج الاختبار exams-models والهيكلية الموحدة)
      filterInstitutionType: 'all',
      institutionTypeOptions: [
        { text: 'الكل', value: 'all' },
        { text: '🏫 مدارس', value: 'school' },
        { text: '🎓 جامعات', value: 'university' },
        { text: '🏢 معاهد وتدريب مهني', value: 'institute' },
      ],
      filterStage: null,
      filterClassTrack: null,
      filterSubject: null,
      filterCollege: null,
      filterDepartment: null,
      filterSpecialization: null,
      filterSemesterSubject: null,
      filterInstituteField: null,
      filterInstituteEducationSystem: null,
      filterInstituteSpecialization: null,
      filterInstituteCurriculum: null,
      filterInstituteSubject: null,

      // الهيكلية الجغرافية والمؤسسية الموحدة
      filterGovernorate: null,
      filterDirectorate: null,
      filterOrganization: null,
      filterSchool: null,

      // Filters
      searchQuery: '',
      filterVersion: 'all',
      filterGrade: 'all',
      filterStatus: null,
      filterDispatch: null,

      // Filter options populated from backend
      availableSchools: [],
      availableDirectorates: [],
      availableGovernorates: [],
      availableVersions: [],

      statusFilterOptions: [
        { text: 'جميع الحالات', value: null },
        { text: 'مصححة ومكتملة', value: 'completed' },
        { text: 'تحت التدقيق', value: 'needs_review' },
        { text: 'غائب', value: 'absent' },
      ],

      dispatchFilterOptions: [
        { text: 'جميع حالات الترحيل', value: null },
        { text: 'مرحل للكنترول', value: 'dispatched' },
        { text: 'غير مرحل', value: 'not_dispatched' },
      ],

      // Dialogs
      dispatchDialog: false,
      rollbackDialog: false,
      psychometricsDialog: false,
      psychometricsLoading: false,
      psychometricsData: null,

      snackbar: {
        show: false,
        text: '',
        color: 'success',
      },

      searchDebounceTimer: null,
    }
  },

  computed: {
    printRecordsList() {
      if (this.printRecords && this.printRecords.length > 0) {
        return this.printRecords
      }
      return this.tableItems.results || []
    },
    filteredRecords() {
      return this.tableItems.results || []
    },

    isAllCurrentSelected() {
      const currentIds = (this.tableItems.results || [])
        .map(s => s.registration_id)
        .filter(Boolean)
      if (!currentIds.length) return false
      return currentIds.every(id => this.selectedStudentIds.includes(id))
    },

    isSomeCurrentSelected() {
      const currentIds = (this.tableItems.results || [])
        .map(s => s.registration_id)
        .filter(Boolean)
      if (!currentIds.length || this.isAllCurrentSelected) return false
      return currentIds.some(id => this.selectedStudentIds.includes(id))
    },

    subjectFilterParam() {
      if (this.filterClassTrack) return { class_track: this.filterClassTrack }
      if (this.filterStage) return { stage: this.filterStage }
      return null
    },

    orgPlaceholder() {
      if (!this.filterInstitutionType || this.filterInstitutionType === 'all') {
        return this.filterDirectorate ? 'المدرسة / المؤسسة (التابعة للمديرية)' : 'المدرسة / المؤسسة التعليمية'
      }
      const typeLabel = this.filterInstitutionType === 'university'
        ? 'الكلية / الجامعة'
        : (this.filterInstitutionType === 'institute' ? 'المعهد / المركز' : 'المدرسة')
      if (this.filterDirectorate) {
        return `${typeLabel} (التابعة للمديرية)`
      }
      if (this.filterGovernorate) {
        return `${typeLabel} (التابعة للمحافظة)`
      }
      return `${typeLabel} (حدد المحافظة للتصفية الهرمية)`
    },

    orgParam() {
      const p = {}
      if (this.filterInstitutionType && this.filterInstitutionType !== 'all') {
        p.institution_type = this.filterInstitutionType
      }
      if (this.filterGovernorate) p.governorate = this.filterGovernorate
      if (this.filterDirectorate) p.directorate = this.filterDirectorate
      return Object.keys(p).length > 0 ? p : undefined
    },

    examFilterParam() {
      const p = {}
      if (this.filterInstitutionType && this.filterInstitutionType !== 'all') {
        p.institution_type = this.filterInstitutionType
      }
      if (this.filterInstitutionType === 'school') {
        if (this.filterClassTrack) p.class_track = this.filterClassTrack
        if (this.filterStage) p.stage = this.filterStage
        if (this.filterSubject) p.subject = this.filterSubject
      } else if (this.filterInstitutionType === 'university') {
        if (this.filterSemesterSubject) p.semester_subject = this.filterSemesterSubject
        if (this.filterSpecialization) p.specialization = this.filterSpecialization
        if (this.filterDepartment) p.department = this.filterDepartment
        if (this.filterCollege) p.college = this.filterCollege
      } else if (this.filterInstitutionType === 'institute') {
        if (this.filterInstituteSubject) p.subject = this.filterInstituteSubject
        else if (this.filterInstituteField) p.field = this.filterInstituteField
      } else {
        if (this.filterSubject) p.subject = this.filterSubject
      }
      return Object.keys(p).length > 0 ? p : null
    },

    versionFilterOptions() {
      const opts = [{ text: 'جميع النماذج', value: 'all' }]
      if (this.availableVersions && this.availableVersions.length) {
        this.availableVersions.forEach(v => {
          if (v) opts.push({ text: `النموذج ${v}`, value: v })
        })
      }
      return opts
    },

    gradeFilterOptions() {
      return [
        { text: 'جميع التقديرات', value: 'all' },
        { text: 'ممتاز مرتفع (A+)', value: 'A+' },
        { text: 'ممتاز (A)', value: 'A' },
        { text: 'جيد جداً مرتفع (B+)', value: 'B+' },
        { text: 'جيد جداً (B)', value: 'B' },
        { text: 'جيد مرتفع (C+)', value: 'C+' },
        { text: 'جيد (C)', value: 'C' },
        { text: 'مقبول مرتفع (D+)', value: 'D+' },
        { text: 'مقبول (D)', value: 'D' },
        { text: 'راسب (F)', value: 'F' },
      ]
    },

    hasActiveFilters() {
      return Boolean(
        (this.filterInstitutionType && this.filterInstitutionType !== 'all') ||
        this.filterStage ||
        this.filterClassTrack ||
        this.filterSubject ||
        this.filterCollege ||
        this.filterDepartment ||
        this.filterSpecialization ||
        this.filterSemesterSubject ||
        this.filterInstituteField ||
        this.filterGovernorate ||
        this.filterDirectorate ||
        this.filterOrganization ||
        (this.searchQuery && this.searchQuery.trim()) ||
        (this.filterVersion && this.filterVersion !== 'all') ||
        (this.filterGrade && this.filterGrade !== 'all') ||
        this.filterStatus ||
        this.filterDispatch
      )
    },

    hasActiveAdvancedFilters() {
      return Boolean(
        (this.filterInstitutionType && this.filterInstitutionType !== 'all') ||
        this.filterStage ||
        this.filterClassTrack ||
        this.filterSubject ||
        this.filterCollege ||
        this.filterDepartment ||
        this.filterSpecialization ||
        this.filterSemesterSubject ||
        this.filterInstituteField ||
        this.filterGovernorate ||
        this.filterDirectorate ||
        this.filterOrganization ||
        (this.filterVersion && this.filterVersion !== 'all') ||
        (this.filterGrade && this.filterGrade !== 'all') ||
        this.filterStatus ||
        this.filterDispatch
      )
    },

    activeFilterCount() {
      let count = 0
      if (this.filterInstitutionType && this.filterInstitutionType !== 'all') count++
      if (this.filterStage) count++
      if (this.filterClassTrack) count++
      if (this.filterSubject) count++
      if (this.filterCollege) count++
      if (this.filterDepartment) count++
      if (this.filterSpecialization) count++
      if (this.filterSemesterSubject) count++
      if (this.filterInstituteField) count++
      if (this.filterGovernorate) count++
      if (this.filterDirectorate) count++
      if (this.filterOrganization) count++
      if (this.filterVersion && this.filterVersion !== 'all') count++
      if (this.filterGrade && this.filterGrade !== 'all') count++
      if (this.filterStatus) count++
      if (this.filterDispatch) count++
      return count
    },
  },

  async created() {
    await this.fetchExamsList()

    // If query param exam is passed
    if (this.$route.query.exam) {
      this.selectedExamId = parseInt(this.$route.query.exam) || this.$route.query.exam
      await this.fetchGradebookRoster({ params: { page: 1, page_size: 10 } })
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
          await this.fetchGradebookRoster({ params: { page: 1, page_size: 10 } })
        }
      } catch (err) {
        console.error('Error fetching exams for gradebook:', err)
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
            await this.fetchGradebookRoster({ params: { page: 1, page_size: 10 } })
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
        this.tableItems = { results: [], pagination: { count: 0, num_pages: 1, current_page: 1, page_size: 10, total: 0 } }
        this.resetStats()
        return
      }
      this.selectedExamId = examId
      this.selectedStudentIds = []
      await this.fetchGradebookRoster({ params: { page: 1, page_size: 10 } })
    },

    onInstitutionTypeChange() {
      this.filterStage = null
      this.filterClassTrack = null
      this.filterCollege = null
      this.filterDepartment = null
      this.filterSpecialization = null
      this.filterSemesterSubject = null
      this.filterInstituteField = null
      this.filterInstituteEducationSystem = null
      this.filterInstituteSpecialization = null
      this.filterInstituteCurriculum = null
      this.filterInstituteSubject = null
      this.filterSubject = null
      this.filterOrganization = null
      this.selectedExamId = null
      this.selectedExamObj = null
      this.selectedStudentIds = []
      this.applyFilters()
    },

    onStageChange() {
      this.filterClassTrack = null
      this.selectedExamId = null
      this.applyFilters()
    },

    onCollegeChange() {
      this.filterDepartment = null
      this.filterSpecialization = null
      this.filterSemesterSubject = null
      this.selectedExamId = null
      this.applyFilters()
    },

    onGovernorateChange(val) {
      if (val !== undefined) this.filterGovernorate = val
      this.filterDirectorate = null
      this.filterOrganization = null
      this.applyFilters()
    },

    onDirectorateChange(val) {
      if (val !== undefined) this.filterDirectorate = val
      this.filterOrganization = null
      this.applyFilters()
    },

    onSubjectChange(val) {
      this.filterSubject = val
      this.selectedExamId = null
      this.applyFilters()
    },

    toggleStudentSelection(regId) {
      if (!regId) return
      const idx = this.selectedStudentIds.indexOf(regId)
      if (idx > -1) {
        this.selectedStudentIds.splice(idx, 1)
      } else {
        this.selectedStudentIds.push(regId)
      }
    },

    toggleSelectAllCurrent(val) {
      const currentIds = (this.tableItems.results || [])
        .map(s => s.registration_id)
        .filter(Boolean)
      if (val) {
        const set = new Set([...this.selectedStudentIds, ...currentIds])
        this.selectedStudentIds = Array.from(set)
      } else {
        this.selectedStudentIds = this.selectedStudentIds.filter(id => !currentIds.includes(id))
      }
    },

    async dispatchSelectedToControl() {
      if (!this.selectedExamId || !this.selectedStudentIds.length) return
      this.dispatchingLoading = true
      try {
        const res = await gradebookAPI.dispatchToControl(this.selectedExamId, {
          registration_ids: this.selectedStudentIds
        })
        const data = res.data || {}
        if (data.success) {
          this.notify(data.message || `تم ترحيل درجات ${data.dispatched_count || this.selectedStudentIds.length} طالب للكنترول بنجاح`, 'success')
          this.selectedStudentIds = []
          await this.loadRoster(this.selectedExamId)
        } else {
          this.notify(data.message || 'تعذر ترحيل درجات الطلاب المحددين', 'error')
        }
      } catch (err) {
        console.error('Error dispatching selected students to control:', err)
        this.notify('حدث خطأ أثناء ترحيل درجات الطلاب المحددين للكنترول', 'error')
      } finally {
        this.dispatchingLoading = false
      }
    },

    resetFilterSelections() {
      this.searchQuery = ''
      this.filterGovernorate = null
      this.filterDirectorate = null
      this.filterOrganization = null
      this.filterSchool = null
      this.filterVersion = 'all'
      this.filterGrade = 'all'
      this.filterStatus = null
      this.filterDispatch = null
      this.selectedStudentIds = []
    },

    resetFilters() {
      this.filterInstitutionType = 'all'
      this.filterStage = null
      this.filterClassTrack = null
      this.filterCollege = null
      this.filterDepartment = null
      this.filterSpecialization = null
      this.filterSemesterSubject = null
      this.filterInstituteField = null
      this.filterInstituteEducationSystem = null
      this.filterInstituteSpecialization = null
      this.filterInstituteCurriculum = null
      this.filterInstituteSubject = null
      this.filterSubject = null
      this.resetFilterSelections()
      this.applyFilters()
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

    onSearchInput() {
      if (this.searchDebounceTimer) clearTimeout(this.searchDebounceTimer)
      this.searchDebounceTimer = setTimeout(() => {
        this.applyFilters()
      }, 400)
    },

    onClearSearch() {
      this.searchQuery = ''
      this.applyFilters()
    },

    applyFilters() {
      this.fetchGradebookRoster({ params: { page: 1 } })
    },

    loadRoster(examId) {
      if (examId) this.selectedExamId = examId
      return this.fetchGradebookRoster({ params: { page: 1 } })
    },

    buildFilterParams(extra = {}) {
      const queryParams = { ...extra }
      if (this.searchQuery && this.searchQuery.trim()) {
        queryParams.search = this.searchQuery.trim()
      }
      if (this.filterGovernorate && this.filterGovernorate !== 'all') {
        queryParams.governorate = this.filterGovernorate
      }
      if (this.filterDirectorate && this.filterDirectorate !== 'all') {
        queryParams.directorate = this.filterDirectorate
      }
      if (this.filterOrganization && this.filterOrganization !== 'all') {
        queryParams.organization = this.filterOrganization
        queryParams.school = this.filterOrganization
      } else if (this.filterSchool && this.filterSchool !== 'all') {
        queryParams.school = this.filterSchool
      }
      if (this.filterVersion && this.filterVersion !== 'all') {
        queryParams.version = this.filterVersion
      }
      if (this.filterGrade && this.filterGrade !== 'all') {
        queryParams.grade = this.filterGrade
      }
      if (this.filterStatus && this.filterStatus !== 'all') {
        queryParams.status = this.filterStatus
      }
      if (this.filterDispatch && this.filterDispatch !== 'all') {
        queryParams.dispatch = this.filterDispatch
      }
      return queryParams
    },

    async fetchGradebookRoster(tableParams = null) {
      if (!this.selectedExamId) {
        this.tableItems = { results: [], pagination: { count: 0, num_pages: 1, current_page: 1, page_size: 10, total: 0 } }
        return
      }
      this.loadingRecords = true
      try {
        let baseParams = {}
        if (tableParams && tableParams.params) {
          baseParams = { ...tableParams.params }
        } else if (tableParams && typeof tableParams === 'object' && ('page' in tableParams || 'page_size' in tableParams || 'perPage' in tableParams)) {
          baseParams = { ...tableParams }
        } else {
          baseParams = { page: 1, page_size: 10 }
        }

        const queryParams = this.buildFilterParams(baseParams)

        const res = await gradebookAPI.getRoster(this.selectedExamId, queryParams)
        const data = res.data || {}
        if (data.success) {
          this.selectedExamObj = data.exam || this.selectedExamObj

          const results = data.results || data.records || []
          const pagination = data.pagination || {
            count: data.count || results.length,
            current_page: queryParams.page || 1,
            num_pages: Math.ceil((data.count || results.length) / (queryParams.page_size || queryParams.perPage || 10)) || 1,
            page_size: queryParams.page_size || queryParams.perPage || 10,
            total: data.count || results.length,
          }

          this.tableItems = {
            ...data,
            results,
            records: results,
            pagination,
          }
          this.totalRecordsCount = pagination.count || data.count || 0

          // Update available dropdown filter options
          if (data.schools && Array.isArray(data.schools)) {
            this.availableSchools = data.schools
          }
          if (data.directorates && Array.isArray(data.directorates)) {
            this.availableDirectorates = data.directorates
          }
          if (data.governorates && Array.isArray(data.governorates)) {
            this.availableGovernorates = data.governorates
          }
          if (data.versions && Array.isArray(data.versions)) {
            this.availableVersions = data.versions
          }

          if (data.stats) {
            this.activeExamStats = data.stats
          } else if (data.exam) {
            this.activeExamStats = {
              total_students: data.exam.total_students || 0,
              completed_count: data.exam.completed_count || 0,
              needs_review_count: data.exam.needs_review_count || 0,
              absent_count: data.exam.absent_count || 0,
              average_score: data.exam.average_score || 0,
              pass_rate: data.exam.pass_rate || 0,
              dispatched_count: data.exam.dispatched_count || 0,
              is_fully_dispatched: data.exam.is_fully_dispatched || false,
            }
          }
        }
      } catch (err) {
        console.error('Error loading gradebook roster from backend:', err)
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
          await this.fetchGradebookRoster({ params: { page: 1 } })
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
          await this.fetchGradebookRoster({ params: { page: 1 } })
          await this.fetchExamsList()
        }
      } catch (err) {
        console.error('Error rolling back dispatch:', err)
        this.notify('تعذر إلغاء ترحيل الدرجات', 'error')
      } finally {
        this.rollbackLoading = false
      }
    },

    async exportToExcel() {
      if (!this.selectedExamId) {
        this.notify('يرجى اختيار اختبار أولاً', 'warning')
        return
      }

      try {
        this.notify('جاري إعداد وتصدير كشف الدرجات الكامل...', 'info')
        const queryParams = this.buildFilterParams({ all: 'true' })

        const res = await gradebookAPI.getRoster(this.selectedExamId, queryParams)
        const records = res.data?.records || res.data?.results || this.tableItems.results || []

        if (!records.length) {
          this.notify('لا توجد بيانات لتصديرها', 'warning')
          return
        }

        const rows = [
          ['م', 'رقم الجلوس', 'الرقم السري', 'اسم الطالب', 'المدرسة', 'المديرية', 'المحافظة', 'النموذج', 'الدرجة', 'الدرجة الكلية', 'النسبة %', 'التقدير', 'حالة التصحيح', 'حالة الترحيل للكنترول']
        ]

        records.forEach((r, idx) => {
          rows.push([
            idx + 1,
            r.seat_number,
            r.secret_number || '—',
            `"${r.student_name || ''}"`,
            `"${r.school_name || ''}"`,
            `"${r.directorate_name || ''}"`,
            `"${r.governorate_name || ''}"`,
            r.version_code || 'A',
            r.status === 'absent' ? 'غائب' : r.score,
            r.max_score,
            r.status === 'absent' ? 0 : r.percentage,
            `"${r.grade_code} - ${r.grade_name_ar}"`,
            r.status,
            r.is_dispatched ? 'مرحل للكنترول' : 'غير مرحل'
          ])
        })

        const downloadUrl = gradebookAPI.exportControlSheetUrl(this.selectedExamId)
        window.open(downloadUrl, '_blank')
        this.notify('تم تصدير كشف الكنترول الرسمي المعتمد بنجاح', 'success')
      } catch (e) {
        console.error('Error exporting gradebook:', e)
        this.notify('حدث خطأ أثناء تصدير الكشف', 'error')
      }
    },

    async openPsychometricsDialog() {
      if (!this.selectedExamId) {
        this.notify('يرجى اختيار اختبار أولاً', 'warning')
        return
      }
      this.psychometricsLoading = true
      try {
        const res = await gradebookAPI.getPsychometrics(this.selectedExamId)
        this.psychometricsData = res.data
        this.psychometricsDialog = true
      } catch (err) {
        console.error('Failed to load psychometrics:', err)
        this.notify('تعذر استخراج التحليل السيكومتري للاختبار', 'error')
      } finally {
        this.psychometricsLoading = false
      }
    },

    async printRosterSheet() {
      if (!this.selectedExamId) return
      try {
        const queryParams = this.buildFilterParams({ all: 'true' })
        const res = await gradebookAPI.getRoster(this.selectedExamId, queryParams)
        this.printRecords = res.data?.records || res.data?.results || this.tableItems.results || []
        this.$nextTick(() => {
          window.print()
        })
      } catch (err) {
        console.error('Error preparing print roster:', err)
        window.print()
      }
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
