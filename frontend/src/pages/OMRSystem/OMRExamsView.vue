<template>
  <div class="qb-omr-exams-linking-v4 pa-4 pa-md-6">
    <!-- ── Page Header (Institutional OpenSoftCore Style) ─────────────── -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center">
        <v-avatar size="48" color="primary" variant="tonal" class="me-3 rounded-xl elevation-1">
          <v-icon size="26">mdi-link-box-variant-outline</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">ربط الاختبارات والتصحيح الضوئي (OMR)</h1>
          <p class="text-caption text-medium-emphasis mb-0">
            استعراض كشوفات الطلاب، معاينة النماذج ومفاتيح الحل، وتوليد وطباعة أوراق التظليل الوزارية المعتمدة
          </p>
        </div>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <v-btn
          color="secondary"
          variant="tonal"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-scanner"
          to="/omr/scanner-lab"
        >
          مختبر المسح والتصحيح
        </v-btn>
        <v-btn
          color="secondary"
          variant="tonal"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-card-text-outline"
          to="/omr/bubble-sheets"
        >
          مكتبة القوالب
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          rounded="lg"
          class="font-weight-bold shadow-sm"
          prepend-icon="mdi-refresh"
          :loading="loading"
          @click="fetchExams"
        >
          تحديث القائمة
        </v-btn>
      </div>
    </div>

    <!-- ── OMR Workflow Stepper (المرحلة 1: استلام وتجهيز الاختبار) ── -->
    <omr-workflow-bar :active-step="1" :exam-id="selectedExam?.id" />

    <!-- Unified Filter Fields -->
    <filter-fields label="خيارات التصفية والبحث المتقدم في الاختبارات" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Search Query Input -->
        <v-col cols="12" sm="6" md="5">
          <v-text-field
            v-model="searchQuery"
            label="اسم الاختبار أو الرمز أو المادة"
            placeholder="بحث باسم الاختبار أو رمزه (Code) أو المادة..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Institution Type -->
        <v-col cols="12" sm="6" md="4">
          <v-select
            v-model="selectedInstitutionType"
            :items="institutionOptions"
            item-title="label"
            item-value="value"
            label="نوع التعليم"
            prepend-inner-icon="mdi-school-outline"
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @update:model-value="fetchExams"
          />
        </v-col>

        <!-- Actions -->
        <v-col cols="12" sm="12" md="3" class="d-flex align-center gap-2">
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
            :click="fetchExams"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Unified Custom Data Table -->
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
          <!-- Code & Title (Clickable) -->
          <template v-if="key === 'exam_info'">
            <div
              class="d-flex align-center py-2 cursor-pointer exam-row-title-trigger"
              @click.stop="openExamHub(item)"
              title="انقر لفتح كشوفات الطلاب والأسئلة ومفاتيح الحل وتوليد الأوراق"
            >
              <v-avatar color="primary" variant="tonal" size="38" class="me-3 rounded-lg flex-shrink-0">
                <v-icon size="20">mdi-file-document-edit-outline</v-icon>
              </v-avatar>
              <div>
                <div class="font-weight-black text-body-2 text-on-surface exam-clickable-title">{{ item.title }}</div>
                <div class="text-caption text-medium-emphasis d-flex align-center gap-2 mt-1">
                  <span class="font-mono bg-grey-lighten-4 px-2 py-0.5 rounded border text-caption">{{ item.uniqueCode }}</span>
                  <span>{{ item.created_at }}</span>
                </div>
              </div>
            </div>
          </template>

          <!-- Subject & Year -->
          <template v-else-if="key === 'subject_info'">
            <div class="font-weight-bold text-body-2">{{ item.subject_name }}</div>
            <div class="text-caption text-medium-emphasis">{{ item.year_name }} ({{ item.institution_type_display }})</div>
          </template>

          <!-- Versions & Questions (Clickable to open Keys Tab) -->
          <template v-else-if="key === 'versions_info'">
            <div
              class="cursor-pointer py-1"
              @click.stop="openExamHub(item, 'keys')"
              title="انقر لمعاينة نماذج الأسئلة ومفاتيح الحل المعتمدة"
            >
              <div class="d-flex justify-center gap-1 mb-1">
                <v-chip
                  v-for="v in item.versions"
                  :key="v.id"
                  size="x-small"
                  color="primary"
                  variant="tonal"
                  class="font-weight-bold unified-table-chip"
                >
                  {{ v.versionCode }}
                </v-chip>
              </div>
              <div class="text-caption font-weight-bold text-primary">
                {{ item.total_questions }} سؤال (مفاتيح الحل)
              </div>
            </div>
          </template>

          <!-- Registered Students (Clickable to open Roster Tab) -->
          <template v-else-if="key === 'students_count'">
            <div
              class="cursor-pointer py-1"
              @click.stop="openExamHub(item, 'roster')"
              title="انقر لفتح كشف الطلاب وأرقام الجلوس"
            >
              <v-chip
                :color="item.registered_students_count > 0 ? 'primary' : 'grey'"
                variant="tonal"
                size="small"
                class="font-weight-bold unified-table-chip"
                prepend-icon="mdi-account-school-outline"
              >
                {{ item.registered_students_count || 0 }} طالب
              </v-chip>
              <div v-if="item.registered_students_count > 0" class="text-caption text-success mt-1">
                <v-icon size="12">mdi-check-circle</v-icon> كشف معتمد
              </div>
              <div v-else class="text-caption text-medium-emphasis mt-1">
                يحتاج تسجيل
              </div>
            </div>
          </template>

          <!-- Grading Progress (Clickable to open Submissions Tab) -->
          <template v-else-if="key === 'progress'">
            <div
              class="cursor-pointer py-1"
              @click.stop="openExamHub(item, 'submissions')"
              title="انقر لاستعراض أوراق الإجابة المصححة"
            >
              <div class="d-flex align-center justify-center gap-2">
                <v-progress-linear
                  :model-value="item.submissions_total > 0 ? Math.min(100, Math.round((item.submissions_completed / item.submissions_total) * 100)) : 0"
                  color="success"
                  rounded
                  height="6"
                  style="width: 70px;"
                />
                <span class="text-caption font-weight-black font-mono">
                  {{ item.submissions_completed }}/{{ item.submissions_total }}
                </span>
              </div>
              <div v-if="item.average_score > 0" class="text-caption text-medium-emphasis mt-1">
                متوسط: <strong class="text-primary">{{ item.average_score }}%</strong>
              </div>
            </div>
          </template>

          <!-- Actions -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-2 flex-wrap">
              <!-- 1. طباعة وتوليد أوراق التظليل للطلاب مباشرة -->
              <v-btn
                color="primary"
                variant="flat"
                rounded="lg"
                size="small"
                class="font-weight-bold px-3"
                prepend-icon="mdi-printer"
                @click.stop.prevent="openExamHub(item, 'template')"
                title="توليد ومعاينة وطباعة أوراق التظليل (البابل شيت) لجميع طلاب الاختبار"
              >
                طباعة أوراق التظليل
              </v-btn>

              <!-- 2. كشف الطلاب ونماذج الأسئلة ومفاتيح الحل -->
              <v-btn
                color="info"
                variant="tonal"
                rounded="lg"
                size="small"
                class="font-weight-bold px-3"
                prepend-icon="mdi-account-school-outline"
                @click.stop.prevent="openExamHub(item, 'roster')"
                title="استعراض كشف الطلاب ونماذج الأسئلة ومفاتيح الحل"
              >
                كشف الطلاب والحلول
              </v-btn>

              <!-- 3. تصميم مواصفات الورقة (أداة مساعدة) -->
              <v-btn
                color="secondary"
                variant="tonal"
                rounded="lg"
                size="small"
                class="font-weight-bold px-2"
                icon="mdi-draw-pen"
                @click.stop.prevent="openInTemplateDesigner(item)"
                title="فتح مواصفات الاختبار في مصمم قوالب التظليل OMR"
              />

              <!-- 4. سجل الطباعة للدفعات -->
              <v-btn
                color="medium-emphasis"
                variant="text"
                rounded="lg"
                size="small"
                icon="mdi-history"
                @click.stop.prevent="goToPrintRegistry(item)"
                title="سجل دفعات الطباعة السابقة لهذا الاختبار"
              />
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>

    <!-- ════════════════════════════════════════════════════════════════ -->
    <!-- DIALOG: النافذة الشاملة لإدارة الاختبار، الطلاب، وتوليد القوالب  -->
    <!-- ════════════════════════════════════════════════════════════════ -->
    <v-dialog v-model="detailsDialog" max-width="1280px" scrollable>
      <v-card class="rounded-2xl" elevation="4">
        <!-- Dialog Header -->
        <v-card-title class="pa-4 pa-md-5 border-b d-flex align-center justify-space-between bg-surface flex-wrap gap-2">
          <div class="d-flex align-center">
            <v-avatar color="primary" variant="tonal" size="44" class="me-3 rounded-xl">
              <v-icon size="24">mdi-school-outline</v-icon>
            </v-avatar>
            <div>
              <div class="text-h6 font-weight-black mb-0">{{ activeExam?.title }}</div>
              <div class="text-caption text-medium-emphasis d-flex align-center gap-2 flex-wrap">
                <span>رمز: <strong class="font-mono">{{ activeExam?.uniqueCode }}</strong></span>
                <span>• المادة: <strong>{{ activeExam?.subject_name }}</strong></span>
                <span>• العام: <strong>{{ activeExam?.year_name }}</strong></span>
                <span v-if="activeExam?.governorate">
                  • المحافظة: <strong>{{ activeExam.governorate }}{{ activeExam.directorate ? ` (${activeExam.directorate})` : '' }}</strong>
                </span>
              </div>
            </div>
          </div>

          <div class="d-flex align-center gap-2">
            <v-btn
              size="small"
              variant="flat"
              color="success"
              class="font-weight-black rounded-lg px-3"
              prepend-icon="mdi-scanner"
              @click="startGradingExam(activeExam, currentVersionObj?.versionCode || 'A')"
            >
              بدء التصحيح الضوئي
            </v-btn>
            <v-btn
              icon="mdi-close"
              variant="text"
              size="small"
              density="comfortable"
              color="medium-emphasis"
              @click="detailsDialog = false"
            />
          </div>
        </v-card-title>

        <!-- ── Main Navigation Tabs in Dialog (خفيف وسهل ومرن) ── -->
        <div class="px-4 pt-3 pb-2 bg-surface">
          <div class="exam-hub-nav-bar">
            <div class="exam-hub-nav-container">
              <div
                class="exam-hub-nav-item"
                :class="{ 'is-active': hubActiveTab === 'questions' }"
                @click="hubActiveTab = 'questions'"
                role="button"
                tabindex="0"
              >
                <v-icon size="17" class="nav-icon">mdi-file-document-outline</v-icon>
                <span>ورقة الأسئلة الرسمية (الكراسة)</span>
                <span
                  v-if="examDetails?.versions?.length"
                  class="hub-count-badge badge-purple"
                >
                  {{ examDetails.versions.length }} نماذج
                </span>
              </div>

              <div
                class="exam-hub-nav-item"
                :class="{ 'is-active': hubActiveTab === 'template' }"
                @click="hubActiveTab = 'template'"
                role="button"
                tabindex="0"
              >
                <v-icon size="17" class="nav-icon">mdi-card-text-outline</v-icon>
                <span>توليد ومعاينة ورقة التظليل</span>
              </div>

              <div
                class="exam-hub-nav-item"
                :class="{ 'is-active': hubActiveTab === 'roster' }"
                @click="hubActiveTab = 'roster'"
                role="button"
                tabindex="0"
              >
                <v-icon size="17" class="nav-icon">mdi-account-school-outline</v-icon>
                <span>كشف الطلاب والبيانات الامتحانية</span>
                <span
                  v-if="totalStudentsCount || examDetails?.registered_students_count || examDetails?.registered_students?.length"
                  class="hub-count-badge badge-blue"
                >
                  {{ totalStudentsCount || examDetails?.registered_students_count || examDetails?.registered_students?.length }}
                </span>
              </div>

              <div
                class="exam-hub-nav-item"
                :class="{ 'is-active': hubActiveTab === 'keys' }"
                @click="hubActiveTab = 'keys'"
                role="button"
                tabindex="0"
              >
                <v-icon size="17" class="nav-icon">mdi-key-variant</v-icon>
                <span>النماذج ومفاتيح الحل</span>
                <span
                  v-if="examDetails?.versions?.length"
                  class="hub-count-badge badge-amber"
                >
                  {{ examDetails.versions.length }}
                </span>
              </div>

              <div
                class="exam-hub-nav-item"
                :class="{ 'is-active': hubActiveTab === 'submissions' }"
                @click="hubActiveTab = 'submissions'"
                role="button"
                tabindex="0"
              >
                <v-icon size="17" class="nav-icon">mdi-check-decagram-outline</v-icon>
                <span>أوراق الإجابة المصححة</span>
                <span
                  v-if="examDetails?.submissions?.length || examDetails?.recent_submissions?.length"
                  class="hub-count-badge badge-green"
                >
                  {{ (examDetails?.submissions?.length || examDetails?.recent_submissions?.length) }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <v-card-text class="pa-4 pa-md-6 bg-grey-lighten-5">
          <div v-if="loadingDetails" class="text-center py-12">
            <v-progress-circular indeterminate color="primary" size="44" class="mb-3" />
            <p class="text-body-2 font-weight-bold">جاري جلب تفاصيل الاختبار والطلاب ونماذج الأسئلة...</p>
          </div>

          <div v-else-if="examDetails">
            <!-- ══════════════════════════════════════════════════════════ -->
            <!-- TAB 0: ورقة الأسئلة الرسمية (كراسة الأسئلة المعتمدة)         -->
            <!-- ══════════════════════════════════════════════════════════ -->
            <div v-if="hubActiveTab === 'questions'">
              <div class="main-card rounded-2xl pa-4 mb-4 border d-flex align-center justify-space-between flex-wrap gap-3 bg-white">
                <div class="d-flex align-center gap-3 flex-wrap">
                  <div class="text-caption font-weight-black text-primary d-flex align-center gap-1">
                    <v-icon size="18">mdi-format-list-bulleted-type</v-icon>
                    اختيار النموذج:
                  </div>
                  <v-btn-toggle
                    v-model="activeVersionTab"
                    mandatory
                    density="compact"
                    color="primary"
                    variant="outlined"
                    rounded="lg"
                  >
                    <v-btn
                      v-for="(v, idx) in (examDetails.versions || [])"
                      :key="`tab-qp-${v.id || idx}`"
                      :value="idx"
                      class="font-weight-bold px-3"
                    >
                      النموذج {{ v.versionCode }} ({{ v.questions?.length || v.questionsCount || 0 }} سؤال)
                    </v-btn>
                  </v-btn-toggle>

                  <v-btn-toggle
                    v-model="selectedQuestionPaperLayout"
                    mandatory
                    density="compact"
                    color="secondary"
                    variant="outlined"
                    rounded="lg"
                  >
                    <v-btn value="a4" class="font-weight-bold px-3" prepend-icon="mdi-file-outline">
                      مقاس A4 (النمط الوزاري المعتمد)
                    </v-btn>
                    <v-btn value="a3" class="font-weight-bold px-3" prepend-icon="mdi-file-document-outline">
                      مقاس كبير A3 (ورقة واحدة عمودين)
                    </v-btn>
                  </v-btn-toggle>
                </div>

                <div class="d-flex align-center gap-2">
                  <v-btn
                    color="primary"
                    variant="flat"
                    rounded="lg"
                    class="font-weight-black px-5"
                    prepend-icon="mdi-printer"
                    @click="() => printQuestionsAndSheets('questions_only')"
                  >
                    طباعة ورقة الأسئلة الرسمية
                  </v-btn>
                  <v-btn
                    color="secondary"
                    variant="tonal"
                    rounded="lg"
                    class="font-weight-bold px-4"
                    prepend-icon="mdi-package-variant-closed"
                    @click="() => printQuestionsAndSheets('package')"
                  >
                    طباعة الحزمة المتكاملة (أسئلة + تظليل)
                  </v-btn>
                </div>
              </div>

              <!-- Official Question Paper Component Frame -->
              <div class="overflow-auto bg-grey-lighten-4 pa-4 rounded-2xl border d-flex justify-center mb-6">
                <YemeniOfficialQuestionPaper
                  :exam-title="customStageTitle || activeExam?.title || 'اختبار الشهادة الثانوية العامة'"
                  :exam-subject="activeExam?.subject_name || 'الرياضيات'"
                  :stage-title="customStageTitle || (activeExam?.stage_name ? `اختبار ${activeExam.stage_name}` : 'اختبار الشهادة الثانوية العامة (المراكز الفرعية - علمي)')"
                  :exam-year="(customExamYear || activeExam?.year_name || '1445هـ - 2024-2023م')"
                  :governorate="customGovernorate || activeExam?.governorate || 'أمانة العاصمة'"
                  :directorate="customDirectorate || activeExam?.directorate || 'الثورة / الأمانة'"
                  :center-name="customCenterName || activeSheetStudent?.school_name || activeExam?.directorate || 'المركز الاختباري الرئيسي'"
                  :center-code="activeSheetStudent?.school_id || activeExam?.id || '3026'"
                  :student-name="sheetGenerationMode === 'student' ? activeSheetStudent?.student_name : ''"
                  :seat-number="sheetGenerationMode === 'student' ? activeSheetStudent?.seat_number : ''"
                  :secret-number="sheetGenerationMode === 'student' ? activeSheetStudent?.secret_number : '60'"
                  :model-code="currentVersionObj?.versionCode || 'A'"
                  :questions="currentVersionObj?.questions || []"
                  :default-layout="selectedQuestionPaperLayout"
                />
              </div>
            </div>

            <!-- ══════════════════════════════════════════════════════════ -->
            <!-- TAB 1: كشف الطلاب والبيانات الامتحانية (Roster)            -->
            <!-- ══════════════════════════════════════════════════════════ -->
            <div v-else-if="hubActiveTab === 'roster'">
              <!-- Quick Actions & Info Bar -->
              <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-4">
                <div class="d-flex align-center gap-2">
                  <v-avatar size="36" color="primary" variant="tonal" class="rounded-lg">
                    <v-icon size="20">mdi-account-group-outline</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-subtitle-2 font-weight-black text-on-surface">كشف الطلاب المقيدين للاختبار</div>
                    <div class="text-caption text-medium-emphasis">إدارة أرقام الجلوس والنماذج المسندة ومعاينة أوراق التظليل</div>
                  </div>
                </div>

                <div class="d-flex align-center gap-2 flex-wrap">
                  <custom-btn
                    type="show"
                    icon="file-document-multiple-outline"
                    label="معاينة وتوليد أوراق التظليل للجميع"
                    color="primary"
                    variant="tonal"
                    class="font-weight-bold"
                    :disabled="!totalStudentsCount"
                    :click="() => { hubActiveTab = 'template'; sheetGenerationMode = 'all_students'; }"
                  />
                  <custom-btn
                    type="show"
                    icon="format-list-numbered"
                    label="طباعة كشف المناداة والجلوس"
                    color="secondary"
                    variant="tonal"
                    class="font-weight-bold"
                    :disabled="!totalStudentsCount"
                    :click="printRosterList"
                  />
                  <custom-btn
                    v-if="!totalStudentsCount"
                    type="create"
                    icon="account-multiple-plus"
                    label="تسجيل الطلاب المقيدين في الاختبار"
                    color="primary"
                    variant="tonal"
                    class="font-weight-bold"
                    :loading="seedingStudents"
                    :click="seedSampleStudents"
                  />
                </div>
              </div>

              <!-- Unified Filter Fields for Students (Backend Filtering) -->
              <filter-fields label="خيارات تصفية كشف الطلاب والبيانات الامتحانية" class="main-card border-0 pa-5 rounded-2xl mb-4">
                <v-row dense class="align-center">
                  <!-- Search Query -->
                  <v-col cols="12" md="5">
                    <v-text-field
                      v-model="studentSearchQuery"
                      label="اسم الطالب أو رقم الجلوس أو الرقم السري"
                      placeholder="بحث بالاسم، رقم الجلوس، أو الرقم السري..."
                      prepend-inner-icon="mdi-magnify"
                      clearable
                      density="compact"
                      variant="outlined"
                      class="mb-6"
                      hide-details
                      @update:model-value="onStudentSearchInput"
                      @keydown.enter="applyStudentFilters"
                    />
                  </v-col>

                  <!-- Model Code -->
                  <v-col cols="12" sm="6" md="3">
                    <v-select
                      v-model="filterModelCode"
                      :items="modelFilterOptions"
                      item-title="title"
                      item-value="value"
                      label="النموذج الامتحاني"
                      prepend-inner-icon="mdi-format-list-bulleted-type"
                      density="compact"
                      variant="outlined"
                      class="mb-6"
                      hide-details
                      @update:model-value="applyStudentFilters"
                    />
                  </v-col>

                  <!-- School Name -->
                  <v-col cols="12" sm="6" md="3">
                    <v-select
                      v-model="filterSchoolName"
                      :items="schoolFilterOptions"
                      item-title="title"
                      item-value="value"
                      :label="institutionLabel"
                      prepend-inner-icon="mdi-school-outline"
                      density="compact"
                      variant="outlined"
                      class="mb-6"
                      hide-details
                      @update:model-value="applyStudentFilters"
                    />
                  </v-col>

                  <!-- Action: Reset -->
                  <v-col cols="12" md="1" class="d-flex align-center">
                    <custom-btn
                      type="cancel_filter"
                      :click="resetStudentFilters"
                      variant="tonal"
                      color="error"
                      label="تفريغ"
                      class="font-weight-bold mb-6 w-100"
                    />
                  </v-col>
                </v-row>
              </filter-fields>

              <!-- Students Unified Custom Data Table (Server-side Paginated) -->
              <div class="main-card rounded-2xl overflow-hidden mb-4">
                <custom-data-table
                  v-bind="{
                    items: studentTableItems,
                    headers: studentHeaders,
                    loading: loadingStudents,
                  }"
                  :getData="fetchExamStudents"
                  :customLoading="loadingStudents"
                  :hasFilter="false"
                  :log="false"
                  :restore="false"
                  :showSelect="false"
                  :actions="false"
                >
                  <template v-slot:item-slot="{ item, key }">
                    <!-- Seat Number -->
                    <template v-if="key === 'seat_number'">
                      <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold font-mono unified-table-chip">
                        {{ item.seat_number }}
                      </v-chip>
                    </template>

                    <!-- Secret Number -->
                    <template v-else-if="key === 'secret_number'">
                      <span class="font-mono font-weight-bold text-caption text-medium-emphasis">
                        {{ item.secret_number || '—' }}
                      </span>
                    </template>

                    <!-- Student Name -->
                    <template v-else-if="key === 'student_name'">
                      <div class="d-flex align-center gap-2 py-1">
                        <v-avatar size="30" color="primary" variant="tonal" class="rounded-lg">
                          <v-icon size="16">mdi-account-outline</v-icon>
                        </v-avatar>
                        <span class="font-weight-bold text-body-2">{{ item.student_name }}</span>
                      </div>
                    </template>

                    <!-- School Info -->
                    <template v-else-if="key === 'school_info'">
                      <div class="text-caption">
                        <div class="font-weight-bold text-on-surface">{{ item.school_name || '—' }}</div>
                        <div class="text-medium-emphasis" v-if="item.governorate || item.directorate">{{ item.governorate }} - {{ item.directorate }}</div>
                      </div>
                    </template>

                    <!-- Model Code -->
                    <template v-else-if="key === 'model_code'">
                      <v-chip
                        size="small"
                        variant="tonal"
                        :color="item.model_code === 'A' ? 'primary' : item.model_code === 'B' ? 'info' : 'secondary'"
                        class="font-weight-bold unified-table-chip"
                      >
                        النموذج {{ item.model_code }}
                      </v-chip>
                    </template>

                    <!-- Barcode Value -->
                    <template v-else-if="key === 'barcode_val'">
                      <span class="font-mono text-caption text-medium-emphasis border px-2 py-0.5 rounded bg-grey-lighten-4">
                        {{ item.seat_number }}
                      </span>
                    </template>

                    <!-- Attendance -->
                    <template v-else-if="key === 'is_present'">
                      <v-icon v-if="item.is_present" size="18" color="success">mdi-check-circle</v-icon>
                      <v-icon v-else size="18" color="medium-emphasis">mdi-minus-circle-outline</v-icon>
                    </template>

                    <!-- Actions: Exactly like /departments with custom-btn is-icon -->
                    <template v-else-if="key === 'actions'">
                      <div class="d-flex align-center justify-center gap-1">
                        <custom-btn
                          is-icon
                          icon="card-text-outline"
                          color="primary"
                          label="معاينة وتوليد ورقة التظليل"
                          :click="() => selectStudentForSheet(item)"
                        />
                        <custom-btn
                          is-icon
                          icon="printer"
                          color="secondary"
                          label="طباعة ورقة هذا الطالب"
                          :click="() => { selectStudentForSheet(item); printSingleSheet(); }"
                        />
                      </div>
                    </template>
                  </template>
                </custom-data-table>
              </div>
            </div>

            <!-- ══════════════════════════════════════════════════════════ -->
            <!-- TAB 2: توليد ومعاينة ورقة التظليل (OMR Sheet Generator)   -->
            <!-- ══════════════════════════════════════════════════════════ -->
            <div v-if="hubActiveTab === 'template'">
              <!-- Alert Banner for Batch Printing Status -->
              <v-alert
                v-if="batchPrintNotification.show"
                :type="batchPrintNotification.color"
                variant="tonal"
                closable
                class="mb-3 rounded-xl font-weight-bold"
                @click:close="batchPrintNotification.show = false"
              >
                {{ batchPrintNotification.message }}
              </v-alert>

              <!-- Sheet Controls Bar -->
              <div class="main-card rounded-2xl pa-4 mb-4">
                <!-- Row 1: Setup Configuration -->
                <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-3 border-b">
                  <div class="d-flex align-center gap-3 flex-grow-1 flex-wrap">
                    <!-- Target Selection Mode -->
                    <v-btn-toggle
                      v-model="sheetGenerationMode"
                      mandatory
                      density="compact"
                      color="primary"
                      variant="outlined"
                      rounded="lg"
                    >
                      <v-btn value="all_students" class="font-weight-bold px-3" prepend-icon="mdi-account-group">
                        أوراق كافة الطلاب (الدفعة كاملة)
                      </v-btn>
                      <v-btn value="student" class="font-weight-bold px-3" prepend-icon="mdi-account">
                        ورقة مخصصة لطالب
                      </v-btn>
                      <v-btn value="blank" class="font-weight-bold px-3" prepend-icon="mdi-file-outline">
                        ورقة نموذج عامة
                      </v-btn>
                    </v-btn-toggle>

                    <!-- Model Filter when all_students is active -->
                    <v-btn-toggle
                      v-if="sheetGenerationMode === 'all_students'"
                      v-model="filterStreamModelCode"
                      density="compact"
                      color="primary"
                      variant="outlined"
                      rounded="lg"
                    >
                      <v-btn value="all" class="font-weight-bold px-3">
                        كل النماذج ({{ examDetails.registered_students?.length || 0 }})
                      </v-btn>
                      <v-btn
                        v-for="v in (examDetails.versions || [])"
                        :key="`stream-filter-v-${v.versionCode}`"
                        :value="v.versionCode"
                        class="font-weight-bold px-3"
                      >
                        النموذج {{ v.versionCode }}
                      </v-btn>
                    </v-btn-toggle>

                    <!-- Student or Version Picker -->
                    <div v-if="sheetGenerationMode === 'student'" style="min-width: 260px; max-width: 380px;" class="flex-grow-1">
                      <v-autocomplete
                        v-model="selectedStudentId"
                        :items="examDetails.registered_students || []"
                        item-title="student_name"
                        item-value="id"
                        placeholder="ابحث عن الطالب بالاسم أو رقم الجلوس..."
                        density="compact"
                        variant="outlined"
                        rounded="lg"
                        hide-details
                        prepend-inner-icon="mdi-account-search"
                      >
                        <template #item="{ props: iProps, item }">
                          <v-list-item v-bind="iProps" :subtitle="`رقم الجلوس: ${item.raw.seat_number} | النموذج: ${item.raw.model_code}`" />
                        </template>
                      </v-autocomplete>
                    </div>

                    <div v-else-if="sheetGenerationMode === 'blank'" style="min-width: 200px; max-width: 280px;" class="flex-grow-1">
                      <v-select
                        v-model="selectedBlankVersionCode"
                        :items="versionCodeOptions"
                        label="اختيار النموذج لورقة التظليل"
                        density="compact"
                        variant="outlined"
                        rounded="lg"
                        hide-details
                        prepend-inner-icon="mdi-format-list-bulleted-type"
                      />
                    </div>

                    <!-- Layout Mode Toggle (A5 vs A4) -->
                    <v-btn-toggle
                      v-model="selectedSheetLayout"
                      mandatory
                      density="compact"
                      color="primary"
                      variant="outlined"
                      rounded="lg"
                    >
                      <v-btn value="compact_a5" class="font-weight-bold px-3" prepend-icon="mdi-card-outline">
                        ورقة الطالب A5 (الوزارية)
                      </v-btn>
                      <v-btn value="full_a4" class="font-weight-bold px-3" prepend-icon="mdi-file-document-outline">
                        الورقة الشاملة A4
                      </v-btn>
                    </v-btn-toggle>

                    <!-- Live Adjustments Button (Like Designer) -->
                    <v-btn
                      variant="tonal"
                      :color="showAdjustmentsPanel ? 'primary' : 'secondary'"
                      size="small"
                      rounded="lg"
                      prepend-icon="mdi-pencil-ruler"
                      class="font-weight-bold"
                      @click="showAdjustmentsPanel = !showAdjustmentsPanel"
                    >
                      {{ showAdjustmentsPanel ? 'إخفاء التعديلات الحية' : 'تعديلات الترويسة والبيانات' }}
                    </v-btn>
                  </div>
                </div>

                <!-- Collapsible Live Adjustments Panel (مثل مصمم الفواتير) -->
                <v-expand-transition>
                  <div v-if="showAdjustmentsPanel" class="pa-4 mt-3 bg-grey-lighten-4 rounded-xl border">
                    <div class="text-caption font-weight-black text-primary mb-3 d-flex align-center gap-1">
                      <v-icon size="16">mdi-auto-fix</v-icon>
                      تعديل بيانات الترويسة فورياً (تنعكس التعديلات لحظياً على كافة أوراق الطلاب قبل نقلها للطباعة)
                    </div>
                    <v-row dense>
                      <v-col cols="12" sm="4">
                        <v-text-field
                          v-model="customCenterName"
                          label="اسم المركز الامتحاني / المدرسة"
                          density="compact"
                          variant="outlined"
                          rounded="lg"
                          hide-details
                          :placeholder="activeExam?.directorate || 'المركز الامتحاني الرئيسي'"
                        />
                      </v-col>
                      <v-col cols="12" sm="4">
                        <v-text-field
                          v-model="customDirectorate"
                          label="المديرية"
                          density="compact"
                          variant="outlined"
                          rounded="lg"
                          hide-details
                          :placeholder="activeExam?.directorate || 'السبعين'"
                        />
                      </v-col>
                      <v-col cols="12" sm="4">
                        <v-text-field
                          v-model="customGovernorate"
                          label="المحافظة"
                          density="compact"
                          variant="outlined"
                          rounded="lg"
                          hide-details
                          :placeholder="activeExam?.governorate || 'أمانة العاصمة'"
                        />
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-text-field
                          v-model="customStageTitle"
                          label="عنوان الاختبار والمرحلة"
                          density="compact"
                          variant="outlined"
                          rounded="lg"
                          hide-details
                          :placeholder="activeExam?.title || 'اختبار الشهادة العامة'"
                        />
                      </v-col>
                      <v-col cols="12" sm="3">
                        <v-text-field
                          v-model="customExamYear"
                          label="العام الدراسي"
                          density="compact"
                          variant="outlined"
                          rounded="lg"
                          hide-details
                          :placeholder="activeExam?.year_name || '2026'"
                        />
                      </v-col>
                      <v-col cols="12" sm="3" class="d-flex align-center">
                        <v-btn
                          size="small"
                          variant="text"
                          color="error"
                          class="font-weight-bold"
                          prepend-icon="mdi-restore"
                          @click="resetHeaderOverrides"
                        >
                          استعادة البيانات الأصلية
                        </v-btn>
                      </v-col>
                    </v-row>
                  </div>
                </v-expand-transition>

                <!-- Row 2: Status, Zoom & Print Actions -->
                <div class="d-flex align-center justify-space-between flex-wrap gap-2 pt-3">
                  <!-- Status Chip & Zoom Controls -->
                  <div class="d-flex align-center gap-2 flex-wrap">
                    <!-- Target summary badge -->
                    <v-chip v-if="sheetGenerationMode === 'all_students'" size="small" color="success" variant="tonal" class="font-weight-bold">
                      <v-icon start size="16">mdi-file-multiple</v-icon>
                      جاهز للمعاينة والطباعة: {{ filteredStreamStudents.length }} ورقة (من إجمالي {{ examDetails.registered_students?.length || 0 }} طالب)
                    </v-chip>
                    <v-chip v-else-if="activeSheetStudent && sheetGenerationMode === 'student'" size="small" color="primary" variant="tonal" class="font-weight-bold">
                      <v-icon start size="16">mdi-account-check</v-icon>
                      {{ activeSheetStudent.student_name }} (جلوس: {{ activeSheetStudent.seat_number }} | نموذج: {{ activeSheetStudent.model_code }})
                    </v-chip>
                    <v-chip v-else size="small" color="primary" variant="tonal" class="font-weight-bold">
                      <v-icon start size="16">mdi-file-check</v-icon>
                      ورقة عامة فارغة — النموذج {{ selectedBlankVersionCode }}
                    </v-chip>

                    <!-- Zoom Controls -->
                    <div class="d-flex align-center bg-grey-lighten-4 rounded-lg px-1 border ms-2">
                      <v-btn icon size="x-small" variant="text" :disabled="sheetZoomLevel <= 0.5" @click="sheetZoomLevel = Math.max(0.5, sheetZoomLevel - 0.15)">
                        <v-icon size="16">mdi-minus</v-icon>
                      </v-btn>
                      <span class="text-caption font-weight-bold px-2 font-mono">
                        {{ Math.round(sheetZoomLevel * 100) }}%
                      </span>
                      <v-btn icon size="x-small" variant="text" :disabled="sheetZoomLevel >= 2.0" @click="sheetZoomLevel = Math.min(2.0, sheetZoomLevel + 0.15)">
                        <v-icon size="16">mdi-plus</v-icon>
                      </v-btn>
                      <v-btn icon size="x-small" variant="text" title="إعادة ضبط" @click="sheetZoomLevel = 1.0">
                        <v-icon size="14">mdi-refresh</v-icon>
                      </v-btn>
                    </div>
                  </div>

                  <!-- Actions Bar -->
                  <div class="d-flex align-center gap-2 flex-wrap">
                    <!-- الزر الرئيسي المباشر: نقل للطباعة -->
                    <v-btn
                      color="success"
                      variant="flat"
                      rounded="lg"
                      size="default"
                      class="font-weight-black shadow-sm px-4"
                      prepend-icon="mdi-printer-check"
                      :loading="printingBatch"
                      :disabled="!filteredStreamStudents?.length && sheetGenerationMode === 'all_students'"
                      @click="batchPrintAllStudents"
                    >
                      نقل للطباعة ({{ filteredStreamStudents.length || 1 }} ورقة)
                    </v-btn>

                    <custom-btn
                      type="print"
                      label="طباعة الورقة الفردية"
                      color="primary"
                      variant="tonal"
                      class="font-weight-bold"
                      :click="printSingleSheet"
                    />
                    <custom-btn
                      icon="clipboard-list-outline"
                      label="طباعة كشف المناداة"
                      color="secondary"
                      variant="tonal"
                      class="font-weight-bold"
                      :click="printRosterList"
                    />
                    <custom-btn
                      icon="book-open-page-variant-outline"
                      label="حزمة الاختبار"
                      color="secondary"
                      variant="tonal"
                      class="font-weight-bold"
                      :click="() => printQuestionsAndSheets('package')"
                    />
                    <custom-btn
                      is-icon
                      icon="tune-vertical"
                      color="secondary"
                      label="تعديل القالب في المصمم"
                      :click="() => openInTemplateDesigner(activeExam)"
                    />
                  </div>
                </div>
              </div>

              <!-- Live OMR Sheet Artboard Canvas -->
              <div class="omr-preview-viewport pa-4 pa-md-6 rounded-2xl border text-center overflow-auto bg-grey-lighten-4">
                
                <!-- ALL STUDENTS BATCH STREAM (عرض كافة الأوراق بالكامل مثل الفواتير في المصمم) -->
                <div
                  v-if="sheetGenerationMode === 'all_students'"
                  ref="batchStreamRef"
                  class="all-sheets-stream d-flex flex-column align-center gap-6"
                >
                  <div v-if="!examDetails.registered_students?.length" class="text-center py-12">
                    <v-avatar size="56" color="grey-lighten-2" class="mb-3">
                      <v-icon size="32" color="medium-emphasis">mdi-account-off-outline</v-icon>
                    </v-avatar>
                    <div class="text-subtitle-1 font-weight-bold mb-1">لا يوجد طلاب مسجلون في هذا الاختبار حتى الآن</div>
                    <div class="text-caption text-medium-emphasis mb-4">يمكنك توليد وتعبئة طلاب تجريبيين للاختبار لمعاينة وطباعة أوراقهم</div>
                    <v-btn color="primary" rounded="lg" prepend-icon="mdi-account-plus" @click="seedSampleStudents">
                      توليد كشف طلاب تجريبي للاختبار
                    </v-btn>
                  </div>

                  <template v-else>
                    <div
                      v-for="(st, sIndex) in filteredStreamStudents"
                      :key="`stream-sheet-${st.id}-${selectedSheetLayout}`"
                      class="sheet-page-card elevation-4 bg-white rounded-lg position-relative d-inline-block text-start mb-6"
                      :style="sheetArtboardStyle"
                    >
                      <!-- Page Indicator Banner (Hidden on Print) -->
                      <div class="d-print-none sheet-page-header px-4 py-2 bg-grey-lighten-4 border-b d-flex align-center justify-space-between text-caption font-weight-bold">
                        <span class="text-primary font-mono font-weight-black">
                          ورقة رقم {{ sIndex + 1 }} من {{ filteredStreamStudents.length }}
                        </span>
                        <span class="text-medium-emphasis font-weight-bold">
                          الطالب: <strong>{{ st.student_name }}</strong> | رقم الجلوس: <strong>{{ st.seat_number }}</strong> | النموذج: <strong>{{ st.model_code || 'A' }}</strong>
                        </span>
                      </div>

                      <!-- Sheet Content -->
                      <YemeniAuditReportSheet
                        v-if="selectedSheetLayout === 'full_a4'"
                        :student-name="st.student_name"
                        :seat-number="st.seat_number"
                        :serial-number="st.secret_number || st.model_code"
                        :model-code="st.model_code || 'A'"
                        :form-number="st.model_code || 'A'"
                        :exam-subject="activeExam?.subject_name || 'الرياضيات'"
                        :exam-stage-title="customStageTitle || (activeExam?.stage_name ? `اختبار ${activeExam.stage_name}` : (activeExam?.title || 'اختبار الشهادة الثانوية العامة (القسم العلمي)'))"
                        :exam-year="customExamYear || activeExam?.year_name || '2026'"
                        :center-name="customCenterName || st.school_name || activeExam?.directorate || 'المركز الاختباري الرئيسي'"
                        :center-code="st.school_id || activeExam?.id || '101'"
                        :governorate="customGovernorate || st.governorate || activeExam?.governorate || 'أمانة العاصمة'"
                        :directorate="customDirectorate || st.directorate || activeExam?.directorate || 'السبعين'"
                        :barcode-value="st.barcode_value || `EXAM_${activeExam?.id}_VER_${st.model_code || 'A'}_SEAT_${st.seat_number}`"
                        :qr-value="st.qr_value || `${activeExam?.uniqueCode}|${st.model_code || 'A'}|${st.seat_number}`"
                        :total-questions="getQuestionsCountForVersion(st.model_code)"
                        :sections="getSectionsForVersion(st.model_code)"
                      />

                      <YemeniMinistrySheet
                        v-else
                        layout-mode="compact_a5"
                        :student-name="st.student_name"
                        :seat-number="st.seat_number"
                        :serial-number="st.secret_number || st.model_code"
                        :model-code="st.model_code || 'A'"
                        :exam-subject="activeExam?.subject_name || 'الرياضيات'"
                        :exam-stage-title="customStageTitle || (activeExam?.stage_name ? `اختبار ${activeExam.stage_name}` : (activeExam?.title || 'اختبار الشهادة الثانوية العامة (القسم العلمي)'))"
                        :exam-year="customExamYear || activeExam?.year_name || '2026'"
                        :center-name="customCenterName || st.school_name || activeExam?.directorate || 'المركز الامتحاني الرئيسي'"
                        :governorate="customGovernorate || activeExam?.governorate || 'أمانة العاصمة'"
                        :directorate="customDirectorate || st.directorate || activeExam?.directorate || 'السبعين'"
                        :barcode-value="st.barcode_value || `EXAM_${activeExam?.id}_VER_${st.model_code || 'A'}_SEAT_${st.seat_number}`"
                        :qr-value="st.qr_value || `${activeExam?.uniqueCode}|${st.model_code || 'A'}|${st.seat_number}`"
                        :total-questions="getQuestionsCountForVersion(st.model_code)"
                        :sections="getSectionsForVersion(st.model_code)"
                        :interactive="false"
                      />
                    </div>
                  </template>
                </div>

                <!-- SINGLE SHEET CANVAS (عند اختيار ورقة فردية أو فارغة) -->
                <div
                  v-else
                  ref="sheetArtboardRef"
                  class="sheet-artboard-container d-inline-block rounded-lg elevation-4 bg-white position-relative"
                  :style="sheetArtboardStyle"
                >
                  <!-- Mode 1: Full A4 Official Audit Sheet (الورقة الشاملة A4) -->
                  <YemeniAuditReportSheet
                    v-if="selectedSheetLayout === 'full_a4'"
                    :key="`audit-sheet-${activeSheetStudent?.id || selectedBlankVersionCode}`"
                    :student-name="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_name || '................................') : '................................'"
                    :seat-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.seat_number || '418485') : '................'"
                    :serial-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.secret_number || '101') : activeSheetModelCode"
                    :model-code="activeSheetModelCode"
                    :form-number="activeSheetModelCode"
                    :exam-subject="activeExam?.subject_name || 'الرياضيات'"
                    :exam-stage-title="activeExam?.stage_name ? `اختبار ${activeExam.stage_name}` : (activeExam?.title || 'اختبار الشهادة الثانوية العامة (القسم العلمي)')"
                    :exam-year="activeExam?.year_name || '2026'"
                    :center-name="activeSheetStudent?.school_name || activeExam?.directorate || 'المركز الاختباري الرئيسي'"
                    :center-code="activeSheetStudent?.school_id || activeExam?.id || '101'"
                    :governorate="activeSheetStudent?.governorate || activeExam?.governorate || 'أمانة العاصمة'"
                    :directorate="activeSheetStudent?.directorate || activeExam?.directorate || 'السبعين'"
                    :barcode-value="activeSheetBarcode"
                    :qr-value="activeSheetQr"
                    :total-questions="activeModelQuestionsCount"
                    :sections="activeExamSections"
                    :answer-key="activeSheetAnswerKey"
                  />

                  <!-- Mode 2: Compact A5 Ministry Student Sheet (ورقة الطالب A5) -->
                  <YemeniMinistrySheet
                    v-else
                    :key="`compact-sheet-${activeSheetStudent?.id || selectedBlankVersionCode}`"
                    layout-mode="compact_a5"
                    :student-name="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_name || '................................') : '................................'"
                    :seat-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.seat_number || '418485') : '................'"
                    :serial-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.secret_number || '101') : activeSheetModelCode"
                    :model-code="activeSheetModelCode"
                    :exam-subject="activeExam?.subject_name || 'الرياضيات'"
                    :exam-year="activeExam?.year_name || '2026'"
                    :center-name="activeSheetStudent?.school_name || activeExam?.directorate || 'المركز الامتحاني الرئيسي'"
                    :governorate="activeExam?.governorate || 'أمانة العاصمة'"
                    :directorate="activeSheetStudent?.directorate || activeExam?.directorate || 'السبعين'"
                    :barcode-value="activeSheetBarcode"
                    :qr-value="activeSheetQr"
                    :total-questions="activeModelQuestionsCount"
                    :sections="activeExamSections"
                    :interactive="true"
                  />
                </div>
              </div>
            </div>

            <!-- ══════════════════════════════════════════════════════════ -->
            <!-- TAB 3: نماذج الأسئلة ومفاتيح الحل (Models & Answer Keys)    -->
            <!-- ══════════════════════════════════════════════════════════ -->
            <div v-if="hubActiveTab === 'keys'">
              <!-- Single Consolidated Model & Answer Key Card -->
              <div class="main-card rounded-2xl pa-4 mb-4">
                <!-- Row 1: Model Selection & Core Model Actions -->
                <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-3 border-b">
                  <!-- Model Selector -->
                  <div class="d-flex align-center gap-2 flex-wrap">
                    <span class="text-caption font-weight-black text-medium-emphasis">النموذج:</span>
                    <v-btn-toggle
                      v-model="activeVersionTab"
                      mandatory
                      density="compact"
                      color="primary"
                      variant="outlined"
                      rounded="lg"
                    >
                      <v-btn
                        v-for="(v, idx) in examDetails.versions"
                        :key="v.id"
                        :value="idx"
                        class="font-weight-bold px-3"
                      >
                        <v-icon start size="16">mdi-file-document-outline</v-icon>
                        النموذج {{ v.versionCode }}
                        <span class="ms-1 text-caption text-medium-emphasis">({{ v.questionsCount }} سؤال)</span>
                      </v-btn>
                    </v-btn-toggle>
                  </div>

                  <!-- Actions for this Model -->
                  <div class="d-flex align-center gap-2 flex-wrap" v-if="currentVersionObj">
                    <custom-btn
                      icon="newspaper-variant-outline"
                      label="معاينة كراسة الأسئلة"
                      color="primary"
                      variant="tonal"
                      class="font-weight-bold"
                      :click="openQuestionPaperModal"
                    />
                    <custom-btn
                      type="print"
                      icon="file-document-outline"
                      :label="`طباعة أسئلة (${currentVersionObj.versionCode})`"
                      color="secondary"
                      variant="tonal"
                      class="font-weight-bold"
                      :click="() => printQuestionsAndSheets('questions_only')"
                    />
                    <custom-btn
                      icon="book-open-page-variant-outline"
                      label="طباعة الحزمة"
                      color="secondary"
                      variant="tonal"
                      class="font-weight-bold"
                      :click="() => printQuestionsAndSheets('package')"
                    />
                    <custom-btn
                      icon="scanner"
                      label="بدء التصحيح"
                      color="success"
                      variant="tonal"
                      class="font-weight-bold"
                      :click="() => startGradingExam(activeExam, currentVersionObj.versionCode)"
                    />
                  </div>
                </div>

                <!-- Row 2: Answer Key Strip (Inline & Sleek) -->
                <div class="d-flex align-center justify-space-between flex-wrap gap-2 pt-3" v-if="currentVersionObj">
                  <div class="d-flex align-center gap-2">
                    <v-icon color="success" size="18">mdi-key-variant</v-icon>
                    <span class="text-caption font-weight-black text-on-surface">
                      مفتاح الإجابة المعتمد (النموذج {{ currentVersionObj.versionCode }}):
                    </span>
                    <span class="text-caption text-medium-emphasis">({{ Object.keys(currentVersionObj.answerKey || {}).length }} إجابة)</span>
                  </div>

                  <!-- Answer Key Pills -->
                  <div class="d-flex align-center gap-1 flex-wrap">
                    <div
                      v-for="(ans, qNum) in currentVersionObj.answerKey"
                      :key="qNum"
                      class="answer-key-pill d-inline-flex align-center px-2 py-0.5 rounded border"
                    >
                      <span class="font-mono text-caption text-medium-emphasis me-1">س{{ qNum }}:</span>
                      <span class="font-weight-black font-mono text-caption text-primary">{{ ans }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="currentVersionObj">

                <!-- Unified Filter Fields for Questions -->
                <filter-fields label="خيارات تصفية والبحث في أسئلة النموذج" class="main-card border-0 pa-5 rounded-2xl mb-4">
                  <v-row dense class="align-center">
                    <!-- Search Query -->
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="questionSearchQuery"
                        label="البحث في نص السؤال أو الخيارات"
                        placeholder="بحث بنص السؤال أو البدائل..."
                        density="compact"
                        variant="outlined"
                        rounded="lg"
                        hide-details
                        clearable
                        prepend-inner-icon="mdi-magnify"
                      />
                    </v-col>

                    <!-- Bloom Level -->
                    <v-col cols="12" sm="6" md="3">
                      <v-select
                        v-model="filterBloomLevel"
                        :items="bloomLevelOptions"
                        item-title="title"
                        item-value="value"
                        label="المستوى المعرفي"
                        density="compact"
                        variant="outlined"
                        rounded="lg"
                        hide-details
                        prepend-inner-icon="mdi-brain"
                      />
                    </v-col>

                    <!-- Question Type -->
                    <v-col cols="12" sm="6" md="2">
                      <v-select
                        v-model="filterQuestionType"
                        :items="questionTypeFilterOptions"
                        item-title="title"
                        item-value="value"
                        label="نوع السؤال"
                        density="compact"
                        variant="outlined"
                        rounded="lg"
                        hide-details
                        prepend-inner-icon="mdi-format-list-checks"
                      />
                    </v-col>

                    <!-- Cancel Filter -->
                    <v-col cols="12" sm="12" md="1" class="d-flex justify-center">
                      <custom-btn
                        type="cancel_filter"
                        :click="resetQuestionFilters"
                        variant="tonal"
                        color="error"
                        label="تفريغ"
                        class="font-weight-bold mb-6 w-100"
                      />
                    </v-col>
                  </v-row>
                </filter-fields>

                <!-- Unified Custom Data Table for Questions -->
                <div class="main-card rounded-2xl overflow-hidden mb-4">
                  <custom-data-table
                    v-bind="{
                      items: questionsTableItems,
                      headers: questionsHeaders,
                    }"
                    :hasFilter="false"
                    :log="false"
                    :restore="false"
                  >
                    <template v-slot:item-slot="{ item, key }">
                      <!-- Question Number -->
                      <template v-if="key === 'orderIndex'">
                        <v-chip size="small" variant="tonal" color="primary" class="font-weight-bold font-mono unified-table-chip">
                          {{ item.orderIndex }}
                        </v-chip>
                      </template>

                      <!-- Question Content & Options -->
                      <template v-else-if="key === 'question_content'">
                        <div class="py-2 text-start">
                          <div class="text-body-2 font-weight-bold mb-2 text-on-surface" v-html="item.content"></div>
                          <!-- Options Badges -->
                          <div class="d-flex flex-wrap gap-2">
                            <div
                              v-for="opt in item.options"
                              :key="opt.id"
                              class="option-badge px-2 py-1 rounded-lg text-caption d-inline-flex align-center border"
                              :class="{ 'option-correct': opt.isTrue }"
                            >
                              <span class="font-weight-black font-mono me-1" :class="opt.isTrue ? 'text-success' : 'text-medium-emphasis'">
                                {{ opt.letter }} ({{ opt.arabic_letter }}):
                              </span>
                              <span :class="opt.isTrue ? 'font-weight-bold text-on-surface' : 'text-medium-emphasis'">
                                {{ opt.text }}
                              </span>
                              <v-icon v-if="opt.isTrue" size="14" color="success" class="ms-1">mdi-check-circle</v-icon>
                            </div>
                          </div>
                        </div>
                      </template>

                      <!-- Bloom Level -->
                      <template v-else-if="key === 'bloom_level'">
                        <v-chip size="small" color="secondary" variant="tonal" class="font-weight-bold unified-table-chip">
                          {{ item.bloomLevel || 'عام' }}
                        </v-chip>
                      </template>

                      <!-- Correct Answer -->
                      <template v-else-if="key === 'correct_answer'">
                        <v-chip size="small" color="success" variant="tonal" class="font-weight-black font-mono unified-table-chip px-3">
                          <v-icon size="14" start>mdi-check-circle-outline</v-icon>
                          {{ item.correctLetter }} ({{ item.correctArabic }})
                        </v-chip>
                      </template>

                      <!-- Assigned Mark -->
                      <template v-else-if="key === 'assigned_mark'">
                        <span class="font-weight-black font-mono text-body-2 text-primary">
                          {{ item.assignedMark }}
                        </span>
                      </template>
                    </template>
                  </custom-data-table>
                </div>
              </div>
            </div>

            <!-- ══════════════════════════════════════════════════════════ -->
            <!-- TAB 4: سجل أوراق الإجابة المصححة (Submissions)             -->
            <!-- ══════════════════════════════════════════════════════════ -->
            <div v-if="hubActiveTab === 'submissions'">
              <div class="main-card rounded-2xl overflow-hidden mb-4">
                <custom-data-table
                  v-bind="{
                    items: submissionsTableItems,
                    headers: submissionsHeaders,
                  }"
                  :hasFilter="false"
                  :log="false"
                  :restore="false"
                >
                  <template v-slot:item-slot="{ item, key }">
                    <template v-if="key === 'submission_id'">
                      <span class="font-mono text-caption text-medium-emphasis">#{{ item.id }}</span>
                    </template>

                    <template v-else-if="key === 'seat_number'">
                      <v-chip size="small" variant="tonal" color="primary" class="font-weight-bold font-mono unified-table-chip">
                        {{ item.seat_number || '—' }}
                      </v-chip>
                    </template>

                    <template v-else-if="key === 'student_name'">
                      <span class="font-weight-bold text-body-2">{{ item.student_name || 'طالب' }}</span>
                    </template>

                    <template v-else-if="key === 'score'">
                      <span class="font-weight-black text-body-1 text-primary">{{ item.score ?? '—' }}</span>
                    </template>

                    <template v-else-if="key === 'confidence'">
                      <span v-if="item.confidence != null" class="font-mono font-weight-bold text-caption text-success">
                        {{ Math.round(item.confidence * 100) }}%
                      </span>
                      <span v-else class="text-caption text-medium-emphasis">—</span>
                    </template>

                    <template v-else-if="key === 'status'">
                      <v-chip size="small" color="success" variant="tonal" class="font-weight-bold unified-table-chip">
                        {{ item.status }}
                      </v-chip>
                    </template>

                    <template v-else-if="key === 'created_at'">
                      <span class="text-caption text-medium-emphasis">{{ item.created_at }}</span>
                    </template>

                    <template v-else-if="key === 'actions'">
                      <div class="d-flex align-center justify-center gap-1">
                        <custom-btn
                          type="show"
                          is-icon
                          label="عرض وتدقيق الورقة"
                          :click="() => viewSubmissions(activeExam)"
                        />
                      </div>
                    </template>
                  </template>
                </custom-data-table>
              </div>
            </div>
          </div>
        </v-card-text>

        <!-- Dialog Footer Actions -->
        <v-card-actions class="pa-4 bg-surface border-t d-flex justify-space-between align-center flex-wrap gap-2">
          <div class="text-caption text-medium-emphasis">
            نظام التصحيح الضوئي المعتمد — بنك الأسئلة والتقويم التربوي
          </div>
          <div class="d-flex align-center gap-2">
            <custom-btn
              type="cancel"
              variant="outlined"
              label="إغلاق"
              :click="() => detailsDialog = false"
            />
            <custom-btn
              icon="scanner"
              label="الانتقال لمختبر التصحيح"
              color="primary"
              variant="tonal"
              class="font-weight-bold"
              :click="() => startGradingExam(activeExam)"
            />
          </div>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ── Official Question Paper (A3 Large Sheet) Preview Modal ── -->
    <v-dialog v-model="showQuestionPaperDialog" max-width="1340" scrollable>
      <v-card class="pa-4 rounded-2xl">
        <div class="d-flex align-center justify-space-between pb-3 border-b mb-3">
          <div class="d-flex align-center gap-2">
            <v-avatar color="primary" variant="tonal" size="36" rounded="lg">
              <v-icon size="20">mdi-newspaper-variant-outline</v-icon>
            </v-avatar>
            <div>
              <h3 class="text-subtitle-1 font-weight-black mb-0">معاينة ورقة الأسئلة الرسمية المعتمدة (النمط الوزاري الموحد A4)</h3>
              <span class="text-caption text-medium-emphasis">مطابقة تماماً للنسخة الرسمية الوزارية الصادرة عن لجنة المطبعة السرية المركزية</span>
            </div>
          </div>
          <v-btn icon size="small" variant="text" @click="showQuestionPaperDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <div class="overflow-auto bg-grey-lighten-4 pa-4 rounded-xl d-flex justify-center" style="max-height: 80vh;">
          <YemeniOfficialQuestionPaper
            :exam-title="activeExam?.title || 'اختبار الشهادة الثانوية العامة'"
            :exam-subject="activeExam?.subject_name || 'الأحياء'"
            :stage-title="activeExam?.stage_name ? `اختبار ${activeExam.stage_name}` : 'اختبار الشهادة الثانوية العامة (المراكز الفرعية - علمي)'"
            :exam-year="(activeExam?.year_name && String(activeExam.year_name).length > 2 && activeExam.year_name !== '1') ? activeExam.year_name : '1445هـ - 2024-2023م'"
            :governorate="activeExam?.governorate || 'أمانة العاصمة'"
            :directorate="activeExam?.directorate || 'الثورة / الأمانة'"
            :center-name="activeSheetStudent?.school_name || activeExam?.directorate || 'المركز الاختباري الرئيسي'"
            :center-code="activeSheetStudent?.school_id || activeExam?.id || '3026'"
            :student-name="sheetGenerationMode === 'student' ? activeSheetStudent?.student_name : ''"
            :seat-number="sheetGenerationMode === 'student' ? activeSheetStudent?.seat_number : ''"
            :secret-number="sheetGenerationMode === 'student' ? activeSheetStudent?.secret_number : '60'"
            :model-code="currentVersionObj?.versionCode || '1'"
            :questions="currentVersionObj?.questions || []"
            :default-layout="'a4'"
          />
        </div>
      </v-card>
    </v-dialog>

    <!-- Hidden Container for Batch Printing All Students' Sheets -->
    <div id="omr-batch-print-staging" class="d-none">
      <div
        v-for="st in (filteredStreamStudents.length ? filteredStreamStudents : (examDetails?.registered_students || []))"
        :key="`batch-${st.id}-${selectedSheetLayout}`"
        class="batch-sheet-slot"
      >
        <!-- A4 Audit Sheet -->
        <YemeniAuditReportSheet
          v-if="selectedSheetLayout === 'full_a4'"
          :student-name="st.student_name"
          :seat-number="st.seat_number"
          :serial-number="st.secret_number || st.model_code"
          :model-code="st.model_code || 'A'"
          :form-number="st.model_code || 'A'"
          :exam-subject="activeExam?.subject_name || 'الرياضيات'"
          :exam-stage-title="customStageTitle || (activeExam?.stage_name ? `اختبار ${activeExam.stage_name}` : (activeExam?.title || 'اختبار الشهادة الثانوية العامة (القسم العلمي)'))"
          :exam-year="customExamYear || activeExam?.year_name || '2026'"
          :center-name="customCenterName || st.school_name || activeExam?.directorate || 'المركز الاختباري الرئيسي'"
          :center-code="st.school_id || activeExam?.id || '101'"
          :governorate="customGovernorate || st.governorate || activeExam?.governorate || 'أمانة العاصمة'"
          :directorate="customDirectorate || st.directorate || activeExam?.directorate || 'السبعين'"
          :barcode-value="st.barcode_value || `EXAM_${activeExam?.id}_VER_${st.model_code || 'A'}_SEAT_${st.seat_number}`"
          :qr-value="st.qr_value || `${activeExam?.uniqueCode}|${st.model_code || 'A'}|${st.seat_number}`"
          :total-questions="getQuestionsCountForVersion(st.model_code)"
          :sections="getSectionsForVersion(st.model_code)"
        />

        <!-- A5 Compact Sheet -->
        <YemeniMinistrySheet
          v-else
          layout-mode="compact_a5"
          :student-name="st.student_name"
          :seat-number="st.seat_number"
          :serial-number="st.secret_number || st.model_code"
          :model-code="st.model_code || 'A'"
          :exam-subject="activeExam?.subject_name || 'الرياضيات'"
          :exam-stage-title="customStageTitle || (activeExam?.stage_name ? `اختبار ${activeExam.stage_name}` : (activeExam?.title || 'اختبار الشهادة الثانوية العامة (القسم العلمي)'))"
          :exam-year="customExamYear || activeExam?.year_name || '2026'"
          :center-name="customCenterName || st.school_name || activeExam?.directorate || 'المركز الامتحاني الرئيسي'"
          :governorate="customGovernorate || activeExam?.governorate || 'أمانة العاصمة'"
          :directorate="customDirectorate || st.directorate || activeExam?.directorate || 'السبعين'"
          :barcode-value="st.barcode_value || `EXAM_${activeExam?.id}_VER_${st.model_code || 'A'}_SEAT_${st.seat_number}`"
          :qr-value="st.qr_value || `${activeExam?.uniqueCode}|${st.model_code || 'A'}|${st.seat_number}`"
          :total-questions="getQuestionsCountForVersion(st.model_code)"
          :sections="getSectionsForVersion(st.model_code)"
          :interactive="false"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/services/omr/client.js'
import YemeniMinistrySheet from '@/components/omr_templates/YemeniMinistrySheet.vue'
import YemeniAuditReportSheet from '@/components/omr_templates/YemeniAuditReportSheet.vue'
import YemeniOfficialQuestionPaper from '@/components/omr_templates/YemeniOfficialQuestionPaper.vue'
import { printOmrElement, printOmrBatch, printExamPackage } from './utils/omrPrint'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const exams = ref([])
const searchQuery = ref('')
const selectedInstitutionType = ref('all')

const stats = ref({
  totalExams: 0,
  totalVersions: 0,
  totalStudents: 0,
  totalSubmissions: 0,
  avgScore: 0,
})

const institutionOptions = [
  { label: 'جميع المؤسسات (مدرسي / جامعي / معاهد)', value: 'all' },
  { label: 'تعليم مدرسي', value: 'school' },
  { label: 'تعليم جامعي', value: 'university' },
  { label: 'معاهد وتدريب مهني', value: 'institute' },
]

// Dialog State
const detailsDialog = ref(false)
const loadingDetails = ref(false)
const activeExam = ref(null)
const examDetails = ref(null)
const hubActiveTab = ref('roster') // 'roster', 'template', 'keys', 'submissions'
const activeVersionTab = ref(0)
const seedingStudents = ref(false)
const showQuestionPaperDialog = ref(false)
const selectedQuestionPaperLayout = ref('a4')

const openQuestionPaperModal = () => {
  showQuestionPaperDialog.value = true
}

// Roster Filters & Server-Side Pagination
const loadingStudents = ref(false)
const totalStudentsCount = ref(0)
const availableSchools = ref([])
const studentTableData = ref({
  results: [],
  pagination: { count: 0, num_pages: 1, current_page: 1, page_size: 10, total: 0 }
})
const studentSearchQuery = ref('')
const filterModelCode = ref('all')
const filterSchoolName = ref('all')

// Template Generation State
const sheetGenerationMode = ref('student') // 'student' | 'blank'
const selectedStudentId = ref(null)
const selectedBlankVersionCode = ref('A')
const selectedSheetLayout = ref('compact_a5') // 'compact_a5' | 'full_a4'
const sheetArtboardRef = ref(null)
const batchStreamRef = ref(null)
const printingBatch = ref(false)

// Designer Stream & Batch Adjustments
const filterStreamModelCode = ref('all')
const customCenterName = ref('')
const customDirectorate = ref('')
const customGovernorate = ref('')
const customExamYear = ref('')
const customStageTitle = ref('')
const showAdjustmentsPanel = ref(false)
const batchPrintNotification = ref({ show: false, message: '', color: 'success' })

const filteredStreamStudents = computed(() => {
  if (!examDetails.value?.registered_students) return []
  let list = examDetails.value.registered_students
  if (filterStreamModelCode.value && filterStreamModelCode.value !== 'all') {
    list = list.filter(s => s.model_code === filterStreamModelCode.value)
  }
  return list
})

const resetHeaderOverrides = () => {
  customCenterName.value = ''
  customDirectorate.value = ''
  customGovernorate.value = ''
  customExamYear.value = ''
  customStageTitle.value = ''
}

const sheetZoomLevel = ref(1.0)

const sheetArtboardStyle = computed(() => {
  const isA4 = selectedSheetLayout.value === 'full_a4'
  return {
    width: '210mm',
    minWidth: '210mm',
    minHeight: isA4 ? '297mm' : '148.5mm',
    zoom: sheetZoomLevel.value,
    transition: 'zoom 0.15s ease'
  }
})

const currentVersionObj = computed(() => {
  if (!examDetails.value || !examDetails.value.versions) return null
  return examDetails.value.versions[activeVersionTab.value] || examDetails.value.versions[0]
})

const getQuestionsCountForVersion = (versionCode) => {
  const v = examDetails.value?.versions?.find(ver => ver.versionCode === versionCode) ||
            examDetails.value?.versions?.[0]
  if (v?.questions?.length) return v.questions.length
  if (v?.questionsCount) return v.questionsCount
  return activeExam.value?.total_questions || 20
}

const getSectionsForVersion = (versionCode) => {
  const v = examDetails.value?.versions?.find(ver => ver.versionCode === versionCode) ||
            examDetails.value?.versions?.[0]
  const qList = v?.questions || []
  const total = qList.length || v?.questionsCount || activeExam.value?.total_questions || 20
  let tfCount = 0
  let mcqCount = 0

  qList.forEach(q => {
    const typeStr = String(q.questionType || '').toLowerCase()
    if (typeStr.includes('true') || typeStr.includes('false') || typeStr.includes('صح') || typeStr.includes('خطأ')) {
      tfCount++
    } else {
      mcqCount++
    }
  })

  // If no detailed question records found, use standard ministerial distribution
  if (tfCount === 0 && mcqCount === 0) {
    if (total <= 20) {
      tfCount = Math.min(10, Math.floor(total / 2))
      mcqCount = total - tfCount
    } else {
      tfCount = 20
      mcqCount = total - 20
    }
  }

  if (tfCount > 0 && mcqCount > 0) {
    return [
      { id: 'sec1', title: 'القسم الأول: أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: tfCount, choices: ['صح', 'خطأ'], mark: 1 },
      { id: 'sec2', title: 'القسم الثاني: أسئلة الاختيار من متعدد', type: 'mcq', from_q: tfCount + 1, to_q: total, choices: ['1', '2', '3', '4'], mark: 2 }
    ]
  } else if (tfCount > 0) {
    return [
      { id: 'sec1', title: 'أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: total, choices: ['صح', 'خطأ'], mark: 1 }
    ]
  } else {
    return [
      { id: 'sec1', title: 'أسئلة الاختيار من متعدد', type: 'mcq', from_q: 1, to_q: total, choices: ['1', '2', '3', '4'], mark: 2 }
    ]
  }
}

const activeModelQuestionsCount = computed(() => {
  return getQuestionsCountForVersion(activeSheetModelCode.value)
})

const activeExamSections = computed(() => {
  return getSectionsForVersion(activeSheetModelCode.value)
})

const versionCodeOptions = computed(() => {
  if (!examDetails.value?.versions) return ['A', 'B']
  return examDetails.value.versions.map(v => v.versionCode)
})

const modelFilterOptions = computed(() => {
  const opts = [{ title: 'جميع النماذج', value: 'all' }]
  if (examDetails.value?.versions) {
    examDetails.value.versions.forEach(v => {
      opts.push({ title: `النموذج ${v.versionCode}`, value: v.versionCode })
    })
  }
  return opts
})

const institutionLabel = computed(() => {
  const t = examDetails.value?.exam?.institution_type || activeExam.value?.institution_type
  if (t === 'university') return 'الكلية / القسم'
  if (t === 'institute') return 'المعهد / المركز التدريبي'
  return 'المدرسة / المركز الامتحاني'
})

const schoolFilterOptions = computed(() => {
  const opts = [{ title: `جميع المؤسسات (${institutionLabel.value})`, value: 'all' }]
  if (availableSchools.value && availableSchools.value.length) {
    availableSchools.value.forEach(sch => {
      if (sch) opts.push({ title: sch, value: sch })
    })
  } else if (examDetails.value?.schools && examDetails.value.schools.length) {
    examDetails.value.schools.forEach(sch => {
      if (sch) opts.push({ title: sch, value: sch })
    })
  } else if (examDetails.value?.registered_students) {
    const set = new Set()
    examDetails.value.registered_students.forEach(s => {
      if (s.school_name) set.add(s.school_name)
    })
    set.forEach(sch => opts.push({ title: sch, value: sch }))
  }
  return opts
})

const studentHeaders = computed(() => [
  { title: "رقم الجلوس", key: "seat_number", sortable: true, align: "center", width: "120px" },
  { title: "الرقم السري", key: "secret_number", sortable: true, align: "center", width: "110px" },
  { title: "اسم الطالب", key: "student_name", sortable: true },
  { title: institutionLabel.value, key: "school_info", sortable: true },
  { title: "النموذج", key: "model_code", sortable: true, align: "center", width: "110px" },
  { title: "كود الباركود", key: "barcode_val", sortable: false, align: "center", width: "130px" },
  { title: "الحضور", key: "is_present", sortable: true, align: "center", width: "90px" },
])

const studentTableItems = computed(() => studentTableData.value)
const filteredStudents = computed(() => studentTableData.value.results || [])

let searchDebounceTimer = null
const onStudentSearchInput = () => {
  if (searchDebounceTimer) clearTimeout(searchDebounceTimer)
  searchDebounceTimer = setTimeout(() => {
    applyStudentFilters()
  }, 400)
}

const applyStudentFilters = () => {
  fetchExamStudents({ params: { page: 1 } })
}

const resetStudentFilters = () => {
  studentSearchQuery.value = ''
  filterModelCode.value = 'all'
  filterSchoolName.value = 'all'
  fetchExamStudents({ params: { page: 1 } })
}

const fetchExamStudents = async (tableParams = null) => {
  if (!activeExam.value?.id) return
  loadingStudents.value = true
  try {
    let queryParams = {}
    if (tableParams && tableParams.params) {
      queryParams = { ...tableParams.params }
    } else if (tableParams && typeof tableParams === 'object' && ('page' in tableParams || 'page_size' in tableParams || 'perPage' in tableParams)) {
      queryParams = { ...tableParams }
    } else {
      queryParams = { page: 1, page_size: 10 }
    }

    if (studentSearchQuery.value && studentSearchQuery.value.trim()) {
      queryParams.search = studentSearchQuery.value.trim()
    }
    if (filterModelCode.value && filterModelCode.value !== 'all') {
      queryParams.version = filterModelCode.value
    }
    if (filterSchoolName.value && filterSchoolName.value !== 'all') {
      queryParams.school = filterSchoolName.value
    }

    const resp = await api.get(`/api/omr/exam-linking/${activeExam.value.id}/students/`, { params: queryParams })
    const data = resp.data || {}
    const results = data.results || data.students || []
    const pagination = data.pagination || {
      count: data.count || results.length,
      current_page: queryParams.page || 1,
      num_pages: Math.ceil((data.count || results.length) / (queryParams.page_size || queryParams.perPage || 10)) || 1,
      page_size: queryParams.page_size || queryParams.perPage || 10,
      total: data.count || results.length,
    }

    studentTableData.value = {
      ...data,
      results,
      pagination,
    }
    totalStudentsCount.value = pagination.count || data.count || 0

    if (data.schools && Array.isArray(data.schools) && data.schools.length) {
      availableSchools.value = data.schools
    }
  } catch (err) {
    console.error('Failed to load exam students from backend:', err)
  } finally {
    loadingStudents.value = false
  }
}

const submissionsHeaders = computed(() => [
  { title: "معاملة التصحيح", key: "submission_id", sortable: true, align: "center", width: "120px" },
  { title: "رقم الجلوس", key: "seat_number", sortable: true, align: "center", width: "120px" },
  { title: "اسم الطالب", key: "student_name", sortable: true },
  { title: "الدرجة", key: "score", sortable: true, align: "center", width: "100px" },
  { title: "نسبة الثقة", key: "confidence", sortable: true, align: "center", width: "130px" },
  { title: "الحالة", key: "status", sortable: true, align: "center", width: "120px" },
  { title: "وقت التصحيح", key: "created_at", sortable: true, align: "center", width: "140px" },
])

const submissionsTableItems = computed(() => {
  const subs = examDetails.value?.recent_submissions || []
  return {
    results: subs,
    count: subs.length,
    pagination: {
      count: subs.length,
      total: subs.length,
    }
  }
})

// Questions and Answer Key State (Tab 3)
const questionSearchQuery = ref('')
const filterBloomLevel = ref('all')
const filterQuestionType = ref('all')

const bloomLevelOptions = computed(() => {
  const opts = [{ title: 'جميع المستويات المعرفية', value: 'all' }]
  const qs = currentVersionObj.value?.questions || []
  const levels = new Set()
  qs.forEach(q => {
    if (q.bloomLevel) levels.add(q.bloomLevel)
  })
  levels.forEach(lvl => opts.push({ title: lvl, value: lvl }))
  return opts
})

const questionTypeFilterOptions = [
  { title: 'جميع أنواع الأسئلة', value: 'all' },
  { title: 'اختيار من متعدد (MCQ)', value: 'mcq' },
  { title: 'صح وخطأ (T/F)', value: 'tf' },
]

const filteredQuestions = computed(() => {
  const list = currentVersionObj.value?.questions || []
  return list.filter(q => {
    if (filterBloomLevel.value !== 'all' && q.bloomLevel !== filterBloomLevel.value) {
      return false
    }
    if (filterQuestionType.value !== 'all') {
      const typeStr = String(q.questionType || '').toLowerCase()
      if (filterQuestionType.value === 'tf') {
        if (!typeStr.includes('true') && !typeStr.includes('false') && !typeStr.includes('صح') && !typeStr.includes('خطأ')) return false
      } else if (filterQuestionType.value === 'mcq') {
        if (typeStr.includes('true') || typeStr.includes('false') || typeStr.includes('صح') || typeStr.includes('خطأ')) return false
      }
    }
    if (questionSearchQuery.value && questionSearchQuery.value.trim()) {
      const s = questionSearchQuery.value.trim().toLowerCase()
      const contentMatch = (q.content || '').toLowerCase().includes(s)
      const optionsMatch = (q.options || []).some(opt => (opt.text || '').toLowerCase().includes(s))
      if (!contentMatch && !optionsMatch) return false
    }
    return true
  })
})

const questionsHeaders = computed(() => [
  { title: "رقم الفقرة", key: "orderIndex", sortable: true, align: "center", width: "95px" },
  { title: "نص السؤال والبدائل المتاحة", key: "question_content", sortable: false },
  { title: "المستوى المعرفي", key: "bloom_level", sortable: true, align: "center", width: "130px" },
  { title: "الإجابة المعتمدة", key: "correct_answer", sortable: true, align: "center", width: "140px" },
  { title: "الدرجة", key: "assigned_mark", sortable: true, align: "center", width: "90px" },
])

const questionsTableItems = computed(() => {
  const qs = filteredQuestions.value
  return {
    results: qs,
    count: qs.length,
    pagination: {
      count: qs.length,
      total: qs.length,
    }
  }
})

const resetQuestionFilters = () => {
  questionSearchQuery.value = ''
  filterBloomLevel.value = 'all'
  filterQuestionType.value = 'all'
}

const activeSheetStudent = computed(() => {
  if (!examDetails.value?.registered_students) return null
  if (selectedStudentId.value) {
    return examDetails.value.registered_students.find(s => s.id === selectedStudentId.value) || examDetails.value.registered_students[0]
  }
  return examDetails.value.registered_students[0] || null
})

const activeSheetModelCode = computed(() => {
  if (sheetGenerationMode.value === 'student' && activeSheetStudent.value) {
    return activeSheetStudent.value.model_code || 'A'
  }
  return selectedBlankVersionCode.value || 'A'
})

const activeSheetBarcode = computed(() => {
  if (sheetGenerationMode.value === 'student' && activeSheetStudent.value) {
    return activeSheetStudent.value.barcode_value || `EXAM_${activeExam.value?.id}_VER_${activeSheetModelCode.value}_SEAT_${activeSheetStudent.value.seat_number}`
  }
  return `EXAM_${activeExam.value?.id}_VER_${activeSheetModelCode.value}_BLANK`
})

const activeSheetQr = computed(() => {
  if (sheetGenerationMode.value === 'student' && activeSheetStudent.value) {
    return activeSheetStudent.value.qr_value || `${activeExam.value?.uniqueCode}|${activeSheetModelCode.value}|${activeSheetStudent.value.seat_number}`
  }
  return `${activeExam.value?.uniqueCode}|${activeSheetModelCode.value}|BLANK`
})

const activeSheetAnswerKey = computed(() => {
  if (!examDetails.value?.versions) return {}
  const v = examDetails.value.versions.find(ver => ver.versionCode === activeSheetModelCode.value)
  return v?.answerKey || {}
})

const headers = computed(() => [
  { title: "رمز وعنوان الاختبار", key: "exam_info", sortable: true },
  { title: "المادة والعام", key: "subject_info", sortable: true, align: "center", width: "180px" },
  { title: "النماذج والأسئلة", key: "versions_info", sortable: false, align: "center", width: "160px" },
  { title: "كشف الطلاب", key: "students_count", sortable: true, align: "center", width: "140px" },
  { title: "حالة التصحيح", key: "progress", sortable: false, align: "center", width: "160px" },
  { title: "الاجراءات", key: "actions", sortable: false, align: "center", width: "320px" },
])

const filteredExams = computed(() => {
  let list = exams.value
  if (selectedInstitutionType.value && selectedInstitutionType.value !== 'all') {
    list = list.filter(e => e.institution_type === selectedInstitutionType.value)
  }
  if (searchQuery.value && searchQuery.value.trim()) {
    const q = searchQuery.value.trim().toLowerCase()
    list = list.filter(e =>
      (e.title && e.title.toLowerCase().includes(q)) ||
      (e.uniqueCode && e.uniqueCode.toLowerCase().includes(q)) ||
      (e.subject_name && e.subject_name.toLowerCase().includes(q))
    )
  }
  return list
})

const tableItems = computed(() => ({
  results: filteredExams.value,
  count: filteredExams.value.length,
  pagination: {
    count: filteredExams.value.length,
    total: filteredExams.value.length,
  }
}))

const resetFilters = () => {
  searchQuery.value = ''
  selectedInstitutionType.value = 'all'
  fetchExams()
}

const fetchExams = async () => {
  loading.value = true
  try {
    const resp = await api.get('/api/omr/exam-linking/', {
      params: {
        institution_type: selectedInstitutionType.value !== 'all' ? selectedInstitutionType.value : undefined,
      }
    })
    if (resp.data && resp.data.results) {
      exams.value = resp.data.results
      updateStats(resp.data.results)
    }
  } catch (err) {
    console.error('Error fetching linking exams:', err)
  } finally {
    loading.value = false
  }
}

const updateStats = (data) => {
  let vCount = 0
  let sCount = 0
  let stCount = 0
  let totalScoreSum = 0
  let scoredExams = 0

  data.forEach(e => {
    vCount += (e.versions_count || 0)
    sCount += (e.submissions_completed || 0)
    stCount += (e.registered_students_count || 0)
    if (e.average_score > 0) {
      totalScoreSum += e.average_score
      scoredExams++
    }
  })

  stats.value = {
    totalExams: data.length,
    totalVersions: vCount,
    totalStudents: stCount,
    totalSubmissions: sCount,
    avgScore: scoredExams > 0 ? (totalScoreSum / scoredExams).toFixed(1) : '0',
  }
}

const openExamHub = async (exam, tab = 'template') => {
  activeExam.value = exam
  detailsDialog.value = true
  loadingDetails.value = true
  hubActiveTab.value = tab
  activeVersionTab.value = 0
  studentSearchQuery.value = ''
  filterModelCode.value = 'all'
  filterSchoolName.value = 'all'

  try {
    const resp = await api.get(`/api/omr/exam-linking/${exam.id}/`)
    examDetails.value = resp.data
    totalStudentsCount.value = resp.data.registered_students_count || (resp.data.registered_students?.length || 0)
    if (resp.data.registered_students && resp.data.registered_students.length > 0) {
      selectedStudentId.value = resp.data.registered_students[0].id
      sheetGenerationMode.value = 'all_students'
    } else {
      sheetGenerationMode.value = 'blank'
    }

    // Load server-side paginated students from backend
    await fetchExamStudents({ params: { page: 1, page_size: 10 } })
  } catch (err) {
    console.error('Failed to load exam details:', err)
  } finally {
    loadingDetails.value = false
  }
}

const quickBatchPrint = async (exam) => {
  await openExamHub(exam, 'template')
  await nextTick()
  if (examDetails.value?.registered_students?.length) {
    await batchPrintAllStudents()
  } else {
    await printSingleSheet()
  }
}

const quickPrintRoster = async (exam) => {
  await openExamHub(exam, 'roster')
  await nextTick()
  printRosterList()
}

const selectStudentForSheet = (student) => {
  selectedStudentId.value = student.id
  sheetGenerationMode.value = 'student'
  hubActiveTab.value = 'template'
}

const previewSheetForVersion = (versionCode) => {
  selectedBlankVersionCode.value = versionCode
  sheetGenerationMode.value = 'blank'
  hubActiveTab.value = 'template'
}

const seedSampleStudents = async () => {
  if (!activeExam.value) return
  seedingStudents.value = true
  try {
    await api.post(`/api/omr/exam-linking/${activeExam.value.id}/seed-students/`)
    // Reload exam details
    const resp = await api.get(`/api/omr/exam-linking/${activeExam.value.id}/`)
    examDetails.value = resp.data
    if (resp.data.registered_students && resp.data.registered_students.length > 0) {
      selectedStudentId.value = resp.data.registered_students[0].id
    }
    fetchExams() // update stats
  } catch (err) {
    console.error('Failed to seed students:', err)
  } finally {
    seedingStudents.value = false
  }
}

const printSingleSheet = async () => {
  await nextTick()
  const printableEl = sheetArtboardRef.value?.querySelector('.yemeni-audit-report-sheet') ||
                      sheetArtboardRef.value?.querySelector('svg.yemeni-ministry-sheet-svg') ||
                      sheetArtboardRef.value?.querySelector('svg')

  if (printableEl) {
    await printOmrElement(printableEl, {
      title: `${activeExam.value?.uniqueCode || 'OMR'}_${activeSheetStudent.value?.seat_number || activeSheetModelCode.value}`,
      isA5: selectedSheetLayout.value === 'compact_a5'
    })
  } else {
    window.print()
  }
}

const batchPrintAllStudents = async () => {
  printingBatch.value = true
  try {
    const isAudit = selectedSheetLayout.value === 'full_a4'
    let elements = []

    // 1. First, pick elements directly from visible stream if mounted
    if (batchStreamRef.value) {
      if (isAudit) {
        elements = Array.from(batchStreamRef.value.querySelectorAll('.yemeni-audit-report-sheet'))
      } else {
        elements = Array.from(batchStreamRef.value.querySelectorAll('svg.yemeni-ministry-sheet-svg'))
        if (!elements.length) {
          elements = Array.from(batchStreamRef.value.querySelectorAll('svg'))
        }
      }
    }

    // 2. Fallback to hidden staging container if stream not available
    if (!elements.length) {
      const stagingEl = document.getElementById('omr-batch-print-staging')
      if (stagingEl) {
        stagingEl.classList.remove('d-none')
        await nextTick()
        if (isAudit) {
          elements = Array.from(stagingEl.querySelectorAll('.yemeni-audit-report-sheet'))
        } else {
          elements = Array.from(stagingEl.querySelectorAll('svg.yemeni-ministry-sheet-svg'))
          if (!elements.length) {
            elements = Array.from(stagingEl.querySelectorAll('svg'))
          }
        }
        stagingEl.classList.add('d-none')
      }
    }

    if (elements.length > 0) {
      const batchId = `BATCH_${Date.now()}`
      await printOmrBatch(elements, {
        title: `كشف_أوراق_تظليل_${activeExam.value?.uniqueCode || 'الاختبار'}_${selectedSheetLayout.value}`,
        isA5: selectedSheetLayout.value === 'compact_a5'
      })
      
      // تسجيل الطباعة في قاعدة البيانات (Print Registry)
      const targetStudentIds = (filteredStreamStudents.value && filteredStreamStudents.value.length > 0)
        ? filteredStreamStudents.value.map(s => s.id)
        : (examDetails.value?.registered_students?.map(s => s.id) || [])

      if (activeExam.value && targetStudentIds.length > 0) {
        try {
          await api.post(`/api/omr/exam-linking/${activeExam.value.id}/mark-printed/`, {
            student_ids: targetStudentIds,
            batch_id: batchId
          })
          console.log("✅ تم توثيق الطباعة بنجاح في قاعدة البيانات")
          batchPrintNotification.value = {
            show: true,
            message: `تم نقل ${elements.length} ورقة بنجاح إلى أمر الطباعة وتوثيق الدفعة (${batchId}) في سجل الطباعة!`,
            color: 'success'
          }
          await fetchExamHubDetails(activeExam.value) 
        } catch (e) {
          console.error("❌ فشل في توثيق حالة الطباعة", e)
        }
      }
    } else {
      await printSingleSheet()
    }
  } catch (err) {
    console.error('Error during batch printing:', err)
  } finally {
    printingBatch.value = false
  }
}

const printQuestionsAndSheets = async (mode = 'package') => {
  await nextTick()
  const printableEl = sheetArtboardRef.value?.querySelector('.yemeni-audit-report-sheet') ||
                      sheetArtboardRef.value?.querySelector('svg.yemeni-ministry-sheet-svg') ||
                      sheetArtboardRef.value?.querySelector('svg')

  const targetVersion = (hubActiveTab.value === 'questions' && examDetails.value?.versions?.[activeVersionTab.value])
    ? examDetails.value.versions[activeVersionTab.value]
    : (examDetails.value?.versions?.find(v => v.versionCode === activeSheetModelCode.value) ||
       currentVersionObj.value ||
       examDetails.value?.versions?.[0])

  if (!targetVersion || !targetVersion.questions || !targetVersion.questions.length) {
    console.warn('No questions found to print.')
    return
  }

  const activeVCode = targetVersion.versionCode || activeSheetModelCode.value || 'A'

  await printExamPackage({
    title: mode === 'package' ? `حزمة_اختبار_${activeExam.value?.subject_name || 'الاختبار'}_النموذج_${activeVCode}` : `كراسة_أسئلة_${activeExam.value?.subject_name || 'الاختبار'}_النموذج_${activeVCode}`,
    examTitle: activeExam.value?.title || '',
    subjectName: activeExam.value?.subject_name || '',
    stageName: activeExam.value?.stage_name ? `اختبار ${activeExam.value.stage_name}` : '',
    yearName: (activeExam.value?.year_name && String(activeExam.value.year_name).length > 2 && activeExam.value.year_name !== '1') ? activeExam.value.year_name : '',
    governorate: activeExam.value?.governorate || '',
    directorate: activeExam.value?.directorate || '',
    centerName: activeSheetStudent.value?.school_name || activeExam.value?.directorate || '',
    centerCode: activeSheetStudent.value?.school_id || activeExam.value?.id || '',
    dayName: activeExam.value?.day_name || '',
    examDate: activeExam.value?.exam_date || '',
    envelopeNo: activeExam.value?.envelope_no || '1',
    timeAllowed: activeExam.value?.time_allowed || '',
    versionCode: activeVCode,
    studentName: sheetGenerationMode.value === 'student' ? activeSheetStudent.value?.student_name : '',
    seatNumber: sheetGenerationMode.value === 'student' ? activeSheetStudent.value?.seat_number : '',
    secretNumber: sheetGenerationMode.value === 'student' ? (activeSheetStudent.value?.secret_number || '') : '',
    studentPhoto: sheetGenerationMode.value === 'student' ? (activeSheetStudent.value?.student_photo || '') : '',
    schoolName: activeSheetStudent.value?.school_name || activeExam.value?.directorate || '',
    institutionType: activeExam.value?.institution_type || 'school',
    questions: targetVersion.questions,
    omrElement: printableEl,
    mode: mode,
    isA3: selectedQuestionPaperLayout.value === 'a3',
    isA5: selectedSheetLayout.value === 'compact_a5'
  })
}

const printRosterList = () => {
  if (!examDetails.value?.registered_students?.length) return

  const students = filteredStudents.value
  const exam = activeExam.value

  const iframe = document.createElement('iframe')
  iframe.style.position = 'fixed'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = '0'
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow?.document
  if (!doc) return

  const rows = students.map((s, idx) => `
    <tr>
      <td style="text-align:center; padding: 6px; border: 1px solid #000;">${idx + 1}</td>
      <td style="text-align:center; padding: 6px; border: 1px solid #000; font-weight:bold; font-family:monospace;">${s.seat_number}</td>
      <td style="text-align:center; padding: 6px; border: 1px solid #000; font-family:monospace;">${s.secret_number || '-'}</td>
      <td style="padding: 6px 10px; border: 1px solid #000; font-weight:bold;">${s.student_name}</td>
      <td style="padding: 6px; border: 1px solid #000;">${s.school_name}</td>
      <td style="text-align:center; padding: 6px; border: 1px solid #000; font-weight:bold;">${s.model_code}</td>
      <td style="border: 1px solid #000; width: 120px;"></td>
    </tr>
  `).join('')

  doc.open()
  doc.write(`
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
      <meta charset="utf-8">
      <title>كشف مناداة وجلوس الطلاب</title>
      <style>
        @page { size: A4 portrait; margin: 12mm; }
        body { font-family: 'Cairo', Arial, sans-serif; direction: rtl; margin: 0; padding: 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px; }
        th { background: #f0f0f0; border: 1px solid #000; padding: 8px; font-weight: bold; }
        .header { text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 15px; }
      </style>
    </head>
    <body>
      <div class="header">
        <h2 style="margin: 0 0 5px 0;">${
          exam?.institution_type === 'institute'
            ? 'الجمهورية اليمنية — وزارة التعليم الفني والتدريب المهني'
            : (exam?.institution_type === 'university'
              ? 'الجمهورية اليمنية — وزارة التعليم العالي والبحث العلمي'
              : 'الجمهورية اليمنية — وزارة التربية والتعليم')
        }</h2>
        <h3 style="margin: 0 0 5px 0;">كشف مناداة وتوقيع حضور الطلاب للاختبارات</h3>
        <p style="margin: 0; font-size: 14px;"><strong>الاختبار:</strong> ${exam?.title || ''} (${exam?.uniqueCode || ''}) | <strong>المادة:</strong> ${exam?.subject_name || ''} | <strong>العام:</strong> ${exam?.year_name || ''}</p>
      </div>
      <table>
        <thead>
          <tr>
            <th style="width: 40px;">#</th>
            <th style="width: 90px;">رقم الجلوس</th>
            <th style="width: 80px;">الرقم السري</th>
            <th>اسم الطالب الرباعي</th>
            <th>${institutionLabel.value}</th>
            <th style="width: 70px;">النموذج</th>
            <th style="width: 120px;">توقيع الطالب</th>
          </tr>
        </thead>
        <tbody>
          ${rows}
        </tbody>
      </table>
    </body>
    </html>
  `)
  doc.close()

  setTimeout(() => {
    iframe.contentWindow?.focus()
    iframe.contentWindow?.print()
    setTimeout(() => {
      if (document.body.contains(iframe)) document.body.removeChild(iframe)
    }, 3000)
  }, 400)
}

const startGradingExam = (exam, versionCode = 'A') => {
  router.push({
    path: '/omr/scanner-lab',
    query: {
      exam_id: exam.id,
      exam_code: exam.uniqueCode,
      exam_title: exam.title,
      version: versionCode,
    }
  })
}

const viewSubmissions = (exam) => {
  router.push({
    path: '/omr/submissions',
    query: {
      exam_id: exam.id,
    }
  })
}

const openInTemplateDesigner = (exam) => {
  if (!exam?.id) return
  const target = `/omr-template-builder?examId=${exam.id}&mode=designer`
  router.push(target).catch(() => {
    window.location.href = target
  })
}

const goToPrintRegistry = (exam) => {
  if (!exam?.id) return
  const target = `/omr-print-registry?exam_id=${exam.id}`
  router.push(target).catch(() => {
    window.location.href = target
  })
}

onMounted(async () => {
  if (route.query.search) {
    searchQuery.value = String(route.query.search)
  }
  await fetchExams()
  const targetId = route.query.open_exam_id || route.query.exam_id || route.query.examId
  if (targetId) {
    const targetExam = exams.value.find(e => String(e.id) === String(targetId))
    if (targetExam) {
      openExamHub(targetExam)
    }
  }
})
</script>

<style scoped>
.qb-omr-exams-linking-v4 {
  color: rgb(var(--v-theme-on-surface));
}

.stat-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
}

.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.hover-row:hover {
  background: rgba(var(--v-theme-primary), 0.03) !important;
}

.table-header-row th {
  background: rgba(var(--v-theme-surface-variant), 0.3) !important;
  padding: 12px 16px !important;
}

.omr-preview-viewport {
  min-height: 480px;
  max-height: 680px;
  background: #f1f3f5;
}

.sheet-artboard-container {
  display: inline-block;
  background: #ffffff;
  padding: 8px;
}

.option-badge {
  background: rgba(var(--v-theme-on-surface), 0.05);
  border: 1px solid rgba(var(--v-border-color), 0.1);
}

.option-correct {
  background: rgba(var(--v-theme-success), 0.12) !important;
  border-color: rgba(var(--v-theme-success), 0.3) !important;
  color: rgb(var(--v-theme-success)) !important;
  font-weight: bold;
}

.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }

.font-mono {
  font-family: monospace, monospace;
}

.unified-table-chip {
  border-radius: 6px !important;
  font-weight: 700 !important;
}

.answer-key-pill {
  white-space: nowrap;
  min-width: 54px;
  justify-content: center;
  border-color: rgba(var(--v-border-color), 0.12) !important;
  background: rgba(var(--v-theme-surface-variant), 0.12) !important;
  transition: all 0.15s ease;
}

.answer-key-pill:hover {
  background: rgba(var(--v-theme-primary), 0.08) !important;
  border-color: rgba(var(--v-theme-primary), 0.3) !important;
}

.action-icon-btn {
  transition: transform 0.18s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.18s ease !important;
}

.action-icon-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12) !important;
}

.cursor-pointer {
  cursor: pointer;
}

.exam-row-title-trigger {
  transition: opacity 0.15s ease;
}

.exam-row-title-trigger:hover .exam-clickable-title {
  color: rgb(var(--v-theme-primary)) !important;
  text-decoration: underline;
}

/* ── Lightweight Navigation Bar in Exam Hub Dialog ── */
.exam-hub-nav-bar {
  direction: rtl;
}

.exam-hub-nav-container {
  display: flex;
  align-items: center;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 5px;
  gap: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.exam-hub-nav-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  padding: 9px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.84rem;
  font-weight: 600;
  color: #64748b;
  background: transparent;
  border: 1px solid transparent;
  transition: all 0.2s ease;
  user-select: none;
  white-space: nowrap;
}

.exam-hub-nav-item:hover {
  background: #f8fafc;
  color: #334155;
}

.exam-hub-nav-item.is-active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 800;
  border-color: #bfdbfe;
}

.exam-hub-nav-item.is-active .nav-icon {
  color: #2563eb !important;
}

.hub-count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 1px 7px;
  border-radius: 9999px;
  font-size: 0.72rem;
  font-weight: 800;
  line-height: 1.4;
}

.hub-count-badge.badge-purple {
  background: #f3e8ff;
  color: #7e22ce;
  border: 1px solid #e9d5ff;
}

.hub-count-badge.badge-blue {
  background: #e0f2fe;
  color: #0369a1;
  border: 1px solid #bae6fd;
}

.hub-count-badge.badge-amber {
  background: #fef3c7;
  color: #b45309;
  border: 1px solid #fde68a;
}

.hub-count-badge.badge-green {
  background: #dcfce7;
  color: #15803d;
  border: 1px solid #bbf7d0;
}

@media (max-width: 1100px) {
  .exam-hub-nav-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .exam-hub-nav-container {
    grid-template-columns: 1fr;
  }
}
</style>
