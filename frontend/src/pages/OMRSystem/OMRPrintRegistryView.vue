<template>
  <div class="qb-omr-print-registry pa-4 pa-md-6">
    <!-- ── Page Header (Institutional OpenSoftCore Style) ─────────────── -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center">
        <v-avatar size="48" color="secondary" variant="tonal" class="me-3 rounded-xl elevation-1">
          <v-icon size="26">mdi-printer-check</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">المرحلة 2: طباعة وتصدير أوراق الإجابة (OMR)</h1>
          <p class="text-caption text-medium-emphasis mb-0">
            توليد ومعاينة أوراق التظليل لكافة الطلاب مثل فواتير متتالية في المصمم وتصديرها للطباعة وتتبع السجلات
          </p>
        </div>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <v-btn
          color="primary"
          variant="flat"
          rounded="lg"
          class="font-weight-bold shadow-sm"
          prepend-icon="mdi-format-list-checks"
          to="/omr-exams"
        >
          استعراض وإدارة الاختبارات
        </v-btn>
        <v-btn
          color="secondary"
          variant="tonal"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-refresh"
          :loading="loadingBatches || loadingExams"
          @click="refreshData"
        >
          تحديث البيانات
        </v-btn>
      </div>
    </div>

    <!-- ── OMR Workflow Stepper (المرحلة 2: طباعة أوراق الإجابة) ── -->
    <omr-workflow-bar :active-step="2" />

    <!-- Unified Filter Fields (Standard Tripartite Institution Filters: Schools, Universities, Institutes) -->
    <filter-fields label="خيارات تصفية وتحديد الاختبارات للطباعة" class="main-card border-0 pa-5 rounded-2xl mb-4">
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
        <template v-if="filterInstitutionType === 'school'">
          <auto-list
            v-model="filterStage"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="3"
            :add="false"
            @update:model-value="onStageChange"
          />
          <auto-list
            v-model="filterClassTrack"
            name="ClassTrackByStage"
            :param="filterStage"
            placeholder="الصف والمسار"
            cols="3"
            :add="false"
            :disabled="!filterStage"
            @update:model-value="fetchExamsList"
          />
          <auto-list
            v-model="filterSubject"
            name="Subject"
            :param="subjectFilterParam"
            placeholder="المادة الدراسية"
            cols="3"
            :add="false"
            @update:model-value="fetchExamsList"
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
            @update:model-value="onDepartmentChange"
          />
          <auto-list
            v-model="filterSpecialization"
            name="Specialization"
            :param="filterDepartment"
            placeholder="التخصص والبرنامج"
            cols="3"
            :add="false"
            :disabled="!filterDepartment"
            @update:model-value="fetchExamsList"
          />
          <auto-list
            v-model="filterSemesterSubject"
            name="SemesterSubject"
            :param="filterSpecialization"
            placeholder="مقرر الفصل الجامعي"
            cols="3"
            :add="false"
            @update:model-value="fetchExamsList"
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
            @update:model-value="fetchExamsList"
          />
          <auto-list
            v-model="filterInstituteSubject"
            name="InstituteSubject"
            :param="instituteSubjectParam"
            placeholder="المادة الدراسية للمعهد"
            cols="3"
            :add="false"
            @update:model-value="fetchExamsList"
          />
        </template>

        <!-- Common Subject Filter (All / Fallback) -->
        <auto-list
          v-if="!filterInstitutionType || filterInstitutionType === 'all'"
          v-model="filterSubject"
          name="Subject"
          placeholder="المادة الدراسية (عام)"
          cols="3"
          :add="false"
          @update:model-value="fetchExamsList"
        />

        <!-- Actions -->
        <v-col cols="12" sm="6" md="3" class="d-flex align-center gap-2">
          <custom-btn
            type="show"
            label="تحديث الاختبارات"
            color="primary"
            class="font-weight-bold flex-grow-1 mb-6"
            :click="fetchExamsList"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetInstitutionFilters"
            variant="tonal"
            color="error"
            label="تفريغ"
            class="font-weight-bold mb-6"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Exam Selection & Quick Meta Card (دائماً في أعلى الصفحة لسهولة التنقل) -->
    <div class="main-card rounded-2xl pa-5 mb-4 border bg-white">
      <v-row dense class="align-center">
        <v-col cols="12" md="6">
          <v-autocomplete
            v-model="selectedExamId"
            :items="examsList"
            item-title="title"
            item-value="id"
            label="اختر الاختبار لمعاينة وطباعة أوراق الأسئلة والتظليل"
            placeholder="ابحث باسم الاختبار أو رمزه أو المادة..."
            prepend-inner-icon="mdi-school-outline"
            variant="outlined"
            density="compact"
            rounded="lg"
            hide-details
            :loading="loadingExams"
            @update:model-value="onExamSelected"
          >
            <template #item="{ props: iProps, item }">
              <v-list-item
                v-bind="iProps"
                :title="item.raw.title"
                :subtitle="`المادة: ${item.raw.subject_name || 'عام'} | الطلاب: ${item.raw.registered_students_count || 0} | النماذج: ${item.raw.versions_count || 1}`"
              />
            </template>
          </v-autocomplete>
        </v-col>

        <v-col cols="12" md="6" class="d-flex align-center justify-md-end gap-2 flex-wrap">
          <v-chip v-if="selectedExam" color="primary" variant="tonal" class="font-weight-bold" prepend-icon="mdi-book-open-page-variant">
            المادة: {{ selectedExam.subject_name || 'عام' }}
          </v-chip>
          <v-chip v-if="selectedExam" color="info" variant="tonal" class="font-weight-bold" prepend-icon="mdi-calendar">
            العام: {{ selectedExam.year_name || '2026' }}
          </v-chip>
          <v-chip v-if="selectedExam" color="secondary" variant="tonal" class="font-weight-bold font-mono" prepend-icon="mdi-barcode">
            رمز: {{ selectedExam.uniqueCode }}
          </v-chip>
        </v-col>
      </v-row>
    </div>

    <!-- ── Navigation Tabs (خفيف وسهل) ───────────────────────────── -->
    <div class="registry-nav-bar mb-6">
      <div class="registry-nav-container">
        <div
          class="registry-nav-item"
          :class="{ 'is-active': activeTab === 'sheets' }"
          @click="activeTab = 'sheets'"
          role="button"
          tabindex="0"
        >
          <v-icon size="17" class="nav-icon">mdi-checkbox-multiple-marked-circle-outline</v-icon>
          <span>أوراق التظليل (OMR Sheets)</span>
        </div>

        <div
          class="registry-nav-item"
          :class="{ 'is-active': activeTab === 'questions' }"
          @click="activeTab = 'questions'"
          role="button"
          tabindex="0"
        >
          <v-icon size="17" class="nav-icon">mdi-file-document-outline</v-icon>
          <span>ورقة الأسئلة الرسمية (الكراسة)</span>
        </div>

        <div
          class="registry-nav-item"
          :class="{ 'is-active': activeTab === 'package' }"
          @click="activeTab = 'package'"
          role="button"
          tabindex="0"
        >
          <v-icon size="17" class="nav-icon">mdi-package-variant-closed</v-icon>
          <span>حزمة الاختبار (أسئلة + تظليل)</span>
        </div>

        <div
          class="registry-nav-item"
          :class="{ 'is-active': activeTab === 'history' }"
          @click="activeTab = 'history'"
          role="button"
          tabindex="0"
        >
          <v-icon size="17" class="nav-icon">mdi-history</v-icon>
          <span>سجل الدفعات المطبوعة ({{ batches.length }})</span>
        </div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════════════ -->
    <!-- STUDIO WORKSPACE: للأوراق والأسئلة والحزم                              -->
    <!-- ══════════════════════════════════════════════════════════════════ -->
    <div v-if="activeTab !== 'history'">
      <!-- Loading State for Exam Details -->
      <div v-if="loadingExamDetails" class="text-center py-12">
        <v-progress-circular indeterminate color="primary" size="48" class="mb-3" />
        <p class="text-body-2 font-weight-bold">جاري تحميل بيانات الاختبار والطلاب ونماذج الأسئلة...</p>
      </div>

      <!-- No Exam Selected State -->
      <div v-else-if="!selectedExamId" class="text-center py-16 main-card rounded-2xl border">
        <v-avatar size="64" color="primary" variant="tonal" class="mb-4">
          <v-icon size="36">mdi-file-document-multiple-outline</v-icon>
        </v-avatar>
        <h3 class="text-h6 font-weight-black mb-1">يرجى اختيار الاختبار لعرض وتوليد أوراق الأسئلة والتظليل</h3>
        <p class="text-caption text-medium-emphasis mb-4">
          حدد الاختبار من القائمة المنسدلة أعلاه لعرض ورقة الأسئلة المعتمدة أو أوراق التظليل للطلاب المسجلين
        </p>
      </div>

      <!-- Exam Active Studio -->
      <div v-else-if="examDetails">
        <!-- Notification Alert -->
        <v-alert
          v-if="batchPrintNotification.show"
          :type="batchPrintNotification.color"
          variant="tonal"
          closable
          class="mb-4 rounded-xl font-weight-bold"
          @click:close="batchPrintNotification.show = false"
        >
          {{ batchPrintNotification.message }}
        </v-alert>

        <!-- Controls Toolbar (مثل مصمم الفواتير والتقارير) -->
        <div class="main-card rounded-2xl pa-4 mb-4 border">
          <!-- Row 0: Document Mode Switcher (أوراق التظليل vs ورقة الأسئلة الرسمية vs حزمة الاختبار) -->
          <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-3 mb-3 border-b">
            <div class="d-flex align-center gap-2 flex-wrap">
              <span class="text-caption font-weight-black text-primary me-1">
                <v-icon size="18" start>mdi-file-tree</v-icon>
                نوع الوثيقة المطلوبة:
              </span>
              <v-btn-toggle
                v-model="selectedDocType"
                mandatory
                density="compact"
                color="primary"
                variant="outlined"
                rounded="lg"
              >
                <v-btn value="sheets" class="font-weight-black px-4" prepend-icon="mdi-checkbox-multiple-marked-circle-outline">
                  أوراق التظليل (OMR Sheets)
                </v-btn>
                <v-btn value="questions" class="font-weight-black px-4" prepend-icon="mdi-file-document-outline">
                  ورقة الأسئلة الرسمية (كراسة الأسئلة)
                </v-btn>
                <v-btn value="package" class="font-weight-black px-4" prepend-icon="mdi-package-variant-closed">
                  حزمة الاختبار الكاملة (أسئلة + تظليل)
                </v-btn>
              </v-btn-toggle>
            </div>

            <!-- Fast Context Action -->
            <div class="d-flex align-center gap-2">
              <v-btn
                v-if="selectedDocType === 'questions'"
                color="primary"
                variant="flat"
                rounded="lg"
                class="font-weight-black px-4"
                prepend-icon="mdi-printer"
                @click="printCurrentQuestionPaper"
              >
                طباعة ورقة الأسئلة (النموذج {{ selectedQuestionsModelCode }})
              </v-btn>
              <v-btn
                v-else-if="selectedDocType === 'package'"
                color="primary"
                variant="flat"
                rounded="lg"
                class="font-weight-black px-4"
                prepend-icon="mdi-printer"
                @click="printCurrentExamPackage"
              >
                طباعة حزمة الاختبار الكاملة
              </v-btn>
              <v-btn
                v-else
                color="info"
                variant="tonal"
                rounded="lg"
                class="font-weight-bold px-3"
                prepend-icon="mdi-newspaper-variant-outline"
                @click="selectedDocType = 'questions'"
              >
                معاينة ورقة الأسئلة
              </v-btn>
            </div>
          </div>

          <!-- Row 1: Target, Model Filter, Layout, Adjustments Toggle -->
          <div v-if="selectedDocType === 'sheets'" class="d-flex align-center justify-space-between flex-wrap gap-3 pb-3 border-b">
            <div class="d-flex align-center gap-3 flex-grow-1 flex-wrap">
              <!-- Target Mode Toggle -->
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
                  ورقة نموذج عامة فارغة
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
                  :key="`reg-filter-v-${v.versionCode}`"
                  :value="v.versionCode"
                  class="font-weight-bold px-3"
                >
                  النموذج {{ v.versionCode }}
                </v-btn>
              </v-btn-toggle>

              <!-- Student Picker if single student mode -->
              <div v-if="sheetGenerationMode === 'student'" style="min-width: 260px; max-width: 360px;" class="flex-grow-1">
                <v-autocomplete
                  v-model="selectedStudentId"
                  :items="examDetails.registered_students || []"
                  item-title="student_name"
                  item-value="id"
                  placeholder="ابحث عن الطالب..."
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

              <!-- Blank version picker -->
              <div v-else-if="sheetGenerationMode === 'blank'" style="min-width: 200px; max-width: 280px;" class="flex-grow-1">
                <v-select
                  v-model="selectedBlankVersionCode"
                  :items="versionCodeOptions"
                  label="اختيار النموذج"
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

              <!-- Live Adjustments Button -->
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

          <!-- Collapsible Live Adjustments Panel -->
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
                    :placeholder="selectedExam?.directorate || 'المركز الامتحاني الرئيسي'"
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
                    :placeholder="selectedExam?.directorate || 'السبعين'"
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
                    :placeholder="selectedExam?.governorate || 'أمانة العاصمة'"
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
                    :placeholder="selectedExam?.title || 'اختبار الشهادة العامة'"
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
                    :placeholder="selectedExam?.year_name || '2026'"
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

          <!-- Row 2: Status, Zoom & Print Actions (when in sheets mode) -->
          <div v-if="selectedDocType === 'sheets'" class="d-flex align-center justify-space-between flex-wrap gap-2 pt-3">
            <!-- Status & Zoom Controls -->
            <div class="d-flex align-center gap-2 flex-wrap">
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
                class="font-weight-black shadow-sm px-5"
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
                v-if="!examDetails.registered_students?.length"
                type="create"
                icon="account-multiple-plus"
                label="تسجيل طلاب تجريبيين للاختبار"
                color="secondary"
                variant="tonal"
                class="font-weight-bold"
                :loading="seedingStudents"
                :click="seedSampleStudents"
              />
            </div>
          </div>
        </div>

        <!-- ════════════════════════════════════════════════════════════ -->
        <!-- VIEW 1: QUESTIONS PAPER (كراسة ورقة الأسئلة الرسمية المعتمدة) -->
        <!-- ════════════════════════════════════════════════════════════ -->
        <div v-if="selectedDocType === 'questions'" class="questions-paper-viewport mb-6">
          <div class="main-card rounded-2xl pa-4 mb-4 border d-flex align-center justify-space-between flex-wrap gap-3 bg-white">
            <div class="d-flex align-center gap-3 flex-wrap">
              <div class="text-caption font-weight-black text-primary d-flex align-center gap-1">
                <v-icon size="18">mdi-format-list-bulleted-type</v-icon>
                اختيار النموذج:
              </div>
              <v-btn-toggle
                v-model="selectedQuestionsModelCode"
                mandatory
                density="compact"
                color="primary"
                variant="outlined"
                rounded="lg"
              >
                <v-btn
                  v-for="v in (examDetails.versions || [])"
                  :key="`qp-ver-${v.versionCode}`"
                  :value="v.versionCode"
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
                @click="printCurrentQuestionPaper"
              >
                طباعة ورقة الأسئلة الرسمية
              </v-btn>
            </div>
          </div>

          <!-- Official Question Paper Component Frame -->
          <div ref="questionPaperRef" class="overflow-auto bg-grey-lighten-4 pa-4 rounded-2xl border d-flex justify-center">
            <YemeniOfficialQuestionPaper
              :exam-title="customStageTitle || selectedExam?.title || ''"
              :exam-subject="selectedExam?.subject_name || ''"
              :stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || ''))"
              :exam-year="customExamYear || selectedExam?.year_name || ''"
              :governorate="customGovernorate || selectedExam?.governorate || ''"
              :directorate="customDirectorate || selectedExam?.directorate || ''"
              :center-name="customCenterName || activeSheetStudent?.school_name || ''"
              :center-code="activeSheetStudent?.school_id || selectedExam?.id || ''"
              :exam-time="selectedExam?.time_allowed || selectedExam?.exam_time || ''"
              :day-name="selectedExam?.day_name || ''"
              :exam-date="selectedExam?.exam_date || ''"
              :envelope-no="selectedExam?.envelope_no || ''"
              :student-name="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_name || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.student_name || ''))"
              :seat-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.seat_number || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.seat_number || ''))"
              :secret-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.secret_number || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.secret_number || ''))"
              :student-photo="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_photo || activeSheetStudent?.photo || '') : ''"
              :is-blank-mode="sheetGenerationMode === 'blank'"
              :model-code="selectedQuestionsModelCode"
              :questions="selectedQuestionsVersionObj?.questions || []"
              :default-layout="selectedQuestionPaperLayout"
            />
          </div>
        </div>

        <!-- ════════════════════════════════════════════════════════════ -->
        <!-- VIEW 2: COMBINED PACKAGE (كراسة الأسئلة + ورقة التظليل)     -->
        <!-- ════════════════════════════════════════════════════════════ -->
        <div v-else-if="selectedDocType === 'package'" class="exam-package-viewport mb-6">
          <div class="main-card rounded-2xl pa-4 mb-4 border d-flex align-center justify-space-between flex-wrap gap-3 bg-white">
            <div class="d-flex align-center gap-2">
              <v-avatar color="primary" variant="tonal" size="36" rounded="lg">
                <v-icon size="20">mdi-package-variant-closed</v-icon>
              </v-avatar>
              <div>
                <div class="text-subtitle-2 font-weight-black">حزمة الاختبار المتكاملة الرسمية</div>
                <div class="text-caption text-medium-emphasis">تدمج كراسة الأسئلة المعتمدة مع ورقة التظليل الخاصة بكل طالب في مستند واحد جاهز للطباعة</div>
              </div>
            </div>

            <v-btn
              color="primary"
              variant="flat"
              rounded="lg"
              class="font-weight-black px-5"
              prepend-icon="mdi-printer"
              @click="printCurrentExamPackage"
            >
              طباعة حزمة الاختبار الكاملة
            </v-btn>
          </div>

          <div class="d-flex flex-column align-center gap-6 overflow-auto bg-grey-lighten-4 pa-4 rounded-2xl border">
            <div class="text-caption font-weight-black text-primary">1. كراسة الأسئلة الرسمية:</div>
            <YemeniOfficialQuestionPaper
              :exam-title="customStageTitle || selectedExam?.title || ''"
              :exam-subject="selectedExam?.subject_name || ''"
              :stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || ''))"
              :exam-year="customExamYear || selectedExam?.year_name || ''"
              :governorate="customGovernorate || selectedExam?.governorate || ''"
              :directorate="customDirectorate || selectedExam?.directorate || ''"
              :center-name="customCenterName || activeSheetStudent?.school_name || ''"
              :center-code="activeSheetStudent?.school_id || selectedExam?.id || ''"
              :exam-time="selectedExam?.time_allowed || selectedExam?.exam_time || ''"
              :day-name="selectedExam?.day_name || ''"
              :exam-date="selectedExam?.exam_date || ''"
              :envelope-no="selectedExam?.envelope_no || ''"
              :student-name="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_name || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.student_name || ''))"
              :seat-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.seat_number || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.seat_number || ''))"
              :secret-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.secret_number || '') : (sheetGenerationMode === 'blank' ? '__BLANK__' : (activeSheetStudent?.secret_number || ''))"
              :student-photo="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_photo || activeSheetStudent?.photo || '') : ''"
              :is-blank-mode="sheetGenerationMode === 'blank'"
              :model-code="activeSheetModelCode"
              :questions="selectedQuestionsVersionObj?.questions || []"
              :default-layout="'a4'"
            />

            <div class="text-caption font-weight-black text-primary mt-4">2. ورقة التظليل (OMR Answer Sheet):</div>
            <div class="sheet-page-card elevation-4 bg-white rounded-lg position-relative d-inline-block text-start" :style="sheetArtboardStyle">
              <YemeniMinistrySheet
                layout-mode="compact_a5"
                :student-name="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_name || '................................') : '................................'"
                :seat-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.seat_number || '.....') : '.....'"
                :serial-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.secret_number || activeSheetModelCode) : activeSheetModelCode"
                :model-code="activeSheetModelCode"
                :exam-subject="selectedExam?.subject_name || 'الرياضيات'"
                :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار الشهادة الثانوية العامة'))"
                :exam-year="customExamYear || selectedExam?.year_name || '2026'"
                :center-name="customCenterName || activeSheetStudent?.school_name || selectedExam?.directorate || 'المركز الامتحاني الرئيسي'"
                :governorate="customGovernorate || selectedExam?.governorate || 'أمانة العاصمة'"
                :directorate="customDirectorate || activeSheetStudent?.directorate || selectedExam?.directorate || 'السبعين'"
                :barcode-value="sheetGenerationMode === 'student' ? (activeSheetStudent?.barcode_value || `EXAM_${selectedExam?.id}_VER_${activeSheetModelCode}_SEAT_${activeSheetStudent?.seat_number}`) : `EXAM_${selectedExam?.id}_VER_${selectedBlankVersionCode}_BLANK`"
                :qr-value="sheetGenerationMode === 'student' ? (activeSheetStudent?.qr_value || `${selectedExam?.uniqueCode}|${activeSheetModelCode}|${activeSheetStudent?.seat_number}`) : `${selectedExam?.uniqueCode}|${selectedBlankVersionCode}|BLANK`"
                :total-questions="getQuestionsCountForVersion(activeSheetModelCode)"
                :sections="getSectionsForVersion(activeSheetModelCode)"
                :interactive="false"
              />
            </div>
          </div>
        </div>

        <!-- ════════════════════════════════════════════════════════════ -->
        <!-- VIEW 3: OMR ANSWER SHEETS CANVAS (عارض أوراق التظليل)        -->
        <!-- ════════════════════════════════════════════════════════════ -->
        <div v-else class="omr-preview-viewport pa-4 pa-md-6 rounded-2xl border text-center overflow-auto bg-grey-lighten-4 mb-6">
          <!-- ALL STUDENTS BATCH STREAM (عرض كافة الأوراق بالكامل كالفواتير في المصمم) -->
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
              <v-btn color="primary" rounded="lg" prepend-icon="mdi-account-plus" :loading="seedingStudents" @click="seedSampleStudents">
                توليد كشف طلاب تجريبي للاختبار
              </v-btn>
            </div>

            <template v-else>
              <div
                v-for="(st, sIndex) in filteredStreamStudents"
                :key="`reg-stream-sheet-${st.id}-${selectedSheetLayout}`"
                class="sheet-page-card elevation-4 bg-white rounded-lg position-relative d-inline-block text-start mb-6"
                :style="sheetArtboardStyle"
              >
                <!-- Page Indicator Banner (Hidden on Print) -->
                <div class="d-print-none sheet-page-header px-4 py-2 bg-grey-lighten-4 border-b d-flex align-center justify-space-between text-caption font-weight-bold">
                  <div class="d-flex align-center gap-2">
                    <span class="text-primary font-mono font-weight-black">
                      ورقة رقم {{ sIndex + 1 }} من {{ filteredStreamStudents.length }}
                    </span>
                    <v-chip v-if="st.is_printed" size="x-small" color="success" variant="tonal" class="font-weight-bold">
                      تمت الطباعة
                    </v-chip>
                  </div>
                  <div class="d-flex align-center gap-3">
                    <span class="text-medium-emphasis font-weight-bold">
                      الطالب: <strong>{{ st.student_name }}</strong> | رقم الجلوس: <strong>{{ st.seat_number }}</strong> | النموذج: <strong>{{ st.model_code || 'A' }}</strong>
                    </span>
                    <v-btn
                      size="x-small"
                      color="primary"
                      variant="tonal"
                      rounded="lg"
                      class="font-weight-bold px-2"
                      prepend-icon="mdi-printer"
                      @click="printSingleStudentCard(sIndex)"
                    >
                      طباعة هذه الورقة فقط
                    </v-btn>
                  </div>
                </div>

                <!-- Sheet Content -->
                <YemeniAuditReportSheet
                  v-if="selectedSheetLayout === 'full_a4'"
                  :student-name="st.student_name"
                  :seat-number="st.seat_number"
                  :serial-number="st.secret_number || st.model_code"
                  :model-code="st.model_code || 'A'"
                  :form-number="st.model_code || 'A'"
                  :exam-subject="selectedExam?.subject_name || 'الرياضيات'"
                  :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار الشهادة الثانوية العامة'))"
                  :exam-year="customExamYear || selectedExam?.year_name || '2026'"
                  :center-name="customCenterName || st.school_name || selectedExam?.directorate || 'المركز الاختباري الرئيسي'"
                  :center-code="st.school_id || selectedExam?.id || '101'"
                  :governorate="customGovernorate || st.governorate || selectedExam?.governorate || 'أمانة العاصمة'"
                  :directorate="customDirectorate || st.directorate || selectedExam?.directorate || 'السبعين'"
                  :barcode-value="st.barcode_value || `EXAM_${selectedExam?.id}_VER_${st.model_code || 'A'}_SEAT_${st.seat_number}`"
                  :qr-value="st.qr_value || `${selectedExam?.uniqueCode}|${st.model_code || 'A'}|${st.seat_number}`"
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
                  :exam-subject="selectedExam?.subject_name || 'الرياضيات'"
                  :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار الشهادة الثانوية العامة'))"
                  :exam-year="customExamYear || selectedExam?.year_name || '2026'"
                  :center-name="customCenterName || st.school_name || selectedExam?.directorate || 'المركز الامتحاني الرئيسي'"
                  :governorate="customGovernorate || selectedExam?.governorate || 'أمانة العاصمة'"
                  :directorate="customDirectorate || st.directorate || selectedExam?.directorate || 'السبعين'"
                  :barcode-value="st.barcode_value || `EXAM_${selectedExam?.id}_VER_${st.model_code || 'A'}_SEAT_${st.seat_number}`"
                  :qr-value="st.qr_value || `${selectedExam?.uniqueCode}|${st.model_code || 'A'}|${st.seat_number}`"
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
              :key="`reg-audit-sheet-${activeSheetStudent?.id || selectedBlankVersionCode}`"
              :student-name="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_name || '................................') : '................................'"
              :seat-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.seat_number || '.....') : '.....'"
              :serial-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.secret_number || activeSheetModelCode) : activeSheetModelCode"
              :model-code="activeSheetModelCode"
              :form-number="activeSheetModelCode"
              :exam-subject="selectedExam?.subject_name || 'الرياضيات'"
              :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار الشهادة الثانوية العامة'))"
              :exam-year="customExamYear || selectedExam?.year_name || '2026'"
              :center-name="customCenterName || activeSheetStudent?.school_name || selectedExam?.directorate || 'المركز الاختباري الرئيسي'"
              :center-code="activeSheetStudent?.school_id || selectedExam?.id || '101'"
              :governorate="customGovernorate || activeSheetStudent?.governorate || selectedExam?.governorate || 'أمانة العاصمة'"
              :directorate="customDirectorate || activeSheetStudent?.directorate || selectedExam?.directorate || 'السبعين'"
              :barcode-value="sheetGenerationMode === 'student' ? (activeSheetStudent?.barcode_value || `EXAM_${selectedExam?.id}_VER_${activeSheetModelCode}_SEAT_${activeSheetStudent?.seat_number}`) : `EXAM_${selectedExam?.id}_VER_${selectedBlankVersionCode}_BLANK`"
              :qr-value="sheetGenerationMode === 'student' ? (activeSheetStudent?.qr_value || `${selectedExam?.uniqueCode}|${activeSheetModelCode}|${activeSheetStudent?.seat_number}`) : `${selectedExam?.uniqueCode}|${selectedBlankVersionCode}|BLANK`"
              :total-questions="getQuestionsCountForVersion(activeSheetModelCode)"
              :sections="getSectionsForVersion(activeSheetModelCode)"
            />

            <!-- Mode 2: Compact Ministry A5 Sheet (ورقة الطالب الوزارية A5) -->
            <YemeniMinistrySheet
              v-else
              :key="`reg-ministry-sheet-${activeSheetStudent?.id || selectedBlankVersionCode}`"
              layout-mode="compact_a5"
              :student-name="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_name || '................................') : '................................'"
              :seat-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.seat_number || '.....') : '.....'"
              :serial-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.secret_number || activeSheetModelCode) : activeSheetModelCode"
              :model-code="activeSheetModelCode"
              :exam-subject="selectedExam?.subject_name || 'الرياضيات'"
              :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار الشهادة الثانوية العامة'))"
              :exam-year="customExamYear || selectedExam?.year_name || '2026'"
              :center-name="customCenterName || activeSheetStudent?.school_name || selectedExam?.directorate || 'المركز الامتحاني الرئيسي'"
              :governorate="customGovernorate || selectedExam?.governorate || 'أمانة العاصمة'"
              :directorate="customDirectorate || activeSheetStudent?.directorate || selectedExam?.directorate || 'السبعين'"
              :barcode-value="sheetGenerationMode === 'student' ? (activeSheetStudent?.barcode_value || `EXAM_${selectedExam?.id}_VER_${activeSheetModelCode}_SEAT_${activeSheetStudent?.seat_number}`) : `EXAM_${selectedExam?.id}_VER_${selectedBlankVersionCode}_BLANK`"
              :qr-value="sheetGenerationMode === 'student' ? (activeSheetStudent?.qr_value || `${selectedExam?.uniqueCode}|${activeSheetModelCode}|${activeSheetStudent?.seat_number}`) : `${selectedExam?.uniqueCode}|${selectedBlankVersionCode}|BLANK`"
              :total-questions="getQuestionsCountForVersion(activeSheetModelCode)"
              :sections="getSectionsForVersion(activeSheetModelCode)"
              :interactive="false"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════════════ -->
    <!-- TAB 2: سجل الدفعات السابقة المطبوعة                                 -->
    <!-- ══════════════════════════════════════════════════════════════════ -->
    <div v-else-if="activeTab === 'history'">
      <!-- Unified Filter Fields -->
      <filter-fields label="خيارات التصفية للبحث في سجلات الطباعة" class="main-card border-0 pa-5 rounded-2xl mb-6">
        <v-row dense class="align-center">
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
            loading: loadingBatches,
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
                  label="استعراض تفاصيل الدفعة والطلاب"
                  :click="() => viewBatchDetails(item)"
                />
              </div>
            </template>
          </template>
        </custom-data-table>
      </div>
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

    <!-- Hidden Staging Container for Print Batches -->
    <div id="omr-registry-batch-staging" class="d-none">
      <div
        v-for="st in filteredStreamStudents"
        :key="`staging-reg-${st.id}-${selectedSheetLayout}`"
        class="batch-sheet-slot"
      >
        <YemeniAuditReportSheet
          v-if="selectedSheetLayout === 'full_a4'"
          :student-name="st.student_name"
          :seat-number="st.seat_number"
          :serial-number="st.secret_number || st.model_code"
          :model-code="st.model_code || 'A'"
          :form-number="st.model_code || 'A'"
          :exam-subject="selectedExam?.subject_name || 'الرياضيات'"
          :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار الشهادة العامة'))"
          :exam-year="customExamYear || selectedExam?.year_name || '2026'"
          :center-name="customCenterName || st.school_name || selectedExam?.directorate || 'المركز الاختباري الرئيسي'"
          :center-code="st.school_id || selectedExam?.id || '101'"
          :governorate="customGovernorate || st.governorate || selectedExam?.governorate || 'أمانة العاصمة'"
          :directorate="customDirectorate || st.directorate || selectedExam?.directorate || 'السبعين'"
          :barcode-value="st.barcode_value || `EXAM_${selectedExam?.id}_VER_${st.model_code || 'A'}_SEAT_${st.seat_number}`"
          :qr-value="st.qr_value || `${selectedExam?.uniqueCode}|${st.model_code || 'A'}|${st.seat_number}`"
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
          :exam-subject="selectedExam?.subject_name || 'الرياضيات'"
          :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار الشهادة العامة'))"
          :exam-year="customExamYear || selectedExam?.year_name || '2026'"
          :center-name="customCenterName || st.school_name || selectedExam?.directorate || 'المركز الامتحاني الرئيسي'"
          :governorate="customGovernorate || selectedExam?.governorate || 'أمانة العاصمة'"
          :directorate="customDirectorate || st.directorate || selectedExam?.directorate || 'السبعين'"
          :barcode-value="st.barcode_value || `EXAM_${selectedExam?.id}_VER_${st.model_code || 'A'}_SEAT_${st.seat_number}`"
          :qr-value="st.qr_value || `${selectedExam?.uniqueCode}|${st.model_code || 'A'}|${st.seat_number}`"
          :total-questions="getQuestionsCountForVersion(st.model_code)"
          :sections="getSectionsForVersion(st.model_code)"
          :interactive="false"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/omr/client.js'
import YemeniMinistrySheet from '@/components/omr_templates/YemeniMinistrySheet.vue'
import YemeniAuditReportSheet from '@/components/omr_templates/YemeniAuditReportSheet.vue'
import YemeniOfficialQuestionPaper from '@/components/omr_templates/YemeniOfficialQuestionPaper.vue'
import { printOmrElement, printOmrBatch, printOfficialQuestionPaper, printExamPackage } from './utils/omrPrint'

const route = useRoute()

// Active Tab: 'sheets' | 'questions' | 'package' | 'history'
const activeTab = ref(
  route.query.tab === 'history' ? 'history' :
  route.query.tab === 'questions' ? 'questions' :
  route.query.tab === 'package' ? 'package' : 'sheets'
)

// Document Category: أوراق التظليل vs ورقة الأسئلة الرسمية vs حزمة الاختبار الكاملة
const selectedDocType = ref(
  ['sheets', 'questions', 'package'].includes(activeTab.value) ? activeTab.value : 'sheets'
)
const selectedQuestionsModelCode = ref('A')
const selectedQuestionPaperLayout = ref('a4') // 'a4' | 'a3'
const questionPaperRef = ref(null)

watch(activeTab, (newTab) => {
  if (['sheets', 'questions', 'package'].includes(newTab)) {
    selectedDocType.value = newTab
  }
})

watch(selectedDocType, (newDoc) => {
  if (['sheets', 'questions', 'package'].includes(newDoc) && activeTab.value !== newDoc && activeTab.value !== 'history') {
    activeTab.value = newDoc
  }
})

// Exams List & Selection
const loadingExams = ref(false)
const examsList = ref([])
const selectedExamId = ref(null)

// Institutional Hierarchy Filters
const filterInstitutionType = ref('all')
const filterStage = ref(null)
const filterClassTrack = ref(null)
const filterSubject = ref(null)

const filterCollege = ref(null)
const filterDepartment = ref(null)
const filterSpecialization = ref(null)
const filterSemesterSubject = ref(null)

const filterInstituteField = ref(null)
const filterInstituteEducationSystem = ref(null)
const filterInstituteSpecialization = ref(null)
const filterInstituteSubject = ref(null)

const institutionTypeOptions = [
  { text: 'الكل (مدارس وجامعات ومعاهد)', value: 'all', icon: 'mdi-domain' },
  { text: 'تعليم مدرسي', value: 'school', icon: 'mdi-school' },
  { text: 'تعليم جامعي', value: 'university', icon: 'mdi-domain' },
  { text: 'معاهد وتدريب مهني', value: 'institute', icon: 'mdi-tools' },
]

const subjectFilterParam = computed(() => {
  const p = {}
  if (filterClassTrack.value) p.class_track = filterClassTrack.value
  if (filterStage.value) p.stage = filterStage.value
  return Object.keys(p).length > 0 ? p : null
})

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

const onInstitutionTypeChange = () => {
  filterStage.value = null
  filterClassTrack.value = null
  filterSubject.value = null
  filterCollege.value = null
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterInstituteField.value = null
  filterInstituteEducationSystem.value = null
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
  fetchExamsList()
}

const onStageChange = () => {
  filterClassTrack.value = null
  filterSubject.value = null
  fetchExamsList()
}

const onCollegeChange = () => {
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  fetchExamsList()
}

const onDepartmentChange = () => {
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  fetchExamsList()
}

const onInstituteFieldChange = () => {
  filterInstituteEducationSystem.value = null
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
  fetchExamsList()
}

const onInstituteEducationSystemChange = () => {
  filterInstituteSpecialization.value = null
  fetchExamsList()
}

const resetInstitutionFilters = () => {
  filterInstitutionType.value = 'all'
  filterStage.value = null
  filterClassTrack.value = null
  filterSubject.value = null
  filterCollege.value = null
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  filterInstituteField.value = null
  filterInstituteEducationSystem.value = null
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
  fetchExamsList()
}

const selectedExam = computed(() => {
  const base = examsList.value.find(e => e.id === selectedExamId.value) || {}
  const detailed = examDetails.value?.exam || {}
  return (base.id || detailed.id) ? { ...base, ...detailed } : null
})

// Exam Details State
const loadingExamDetails = ref(false)
const examDetails = ref(null)
const seedingStudents = ref(false)

// Sheet Generation Settings
const sheetGenerationMode = ref('all_students') // 'all_students' | 'student' | 'blank'
const selectedSheetLayout = ref('compact_a5') // 'compact_a5' | 'full_a4'
const selectedStudentId = ref(null)
const selectedBlankVersionCode = ref('A')
const sheetZoomLevel = ref(1.0)
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

// DOM Refs
const sheetArtboardRef = ref(null)
const batchStreamRef = ref(null)

// Batches Registry State
const loadingBatches = ref(false)
const searchQuery = ref('')
const batches = ref([])
const detailsDialog = ref(false)
const activeBatch = ref(null)
const loadingDetails = ref(false)
const batchStudents = ref([])

// Version Code Options
const versionCodeOptions = computed(() => {
  if (examDetails.value?.versions && examDetails.value.versions.length > 0) {
    return examDetails.value.versions.map(v => v.versionCode)
  }
  return ['A', 'B', 'C', 'D']
})

const activeSheetStudent = computed(() => {
  if (!examDetails.value?.registered_students) return null
  if (selectedStudentId.value) {
    return examDetails.value.registered_students.find(s => s.id === selectedStudentId.value) || examDetails.value.registered_students[0]
  }
  return examDetails.value.registered_students[0] || null
})

const activeSheetModelCode = computed(() => {
  if (sheetGenerationMode.value === 'blank') {
    return selectedBlankVersionCode.value || 'A'
  }
  return activeSheetStudent.value?.model_code || 'A'
})

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

const getQuestionsCountForVersion = (versionCode) => {
  const v = examDetails.value?.versions?.find(ver => ver.versionCode === versionCode) ||
            examDetails.value?.versions?.[0]
  if (v?.questions?.length) return v.questions.length
  if (v?.questionsCount) return v.questionsCount
  return selectedExam.value?.total_questions || 20
}

const getSectionsForVersion = (versionCode) => {
  const v = examDetails.value?.versions?.find(ver => ver.versionCode === versionCode) ||
            examDetails.value?.versions?.[0]
  const qList = v?.questions || []
  const total = qList.length || v?.questionsCount || selectedExam.value?.total_questions || 20
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

const selectedQuestionsVersionObj = computed(() => {
  return examDetails.value?.versions?.find(ver => ver.versionCode === selectedQuestionsModelCode.value) ||
         examDetails.value?.versions?.[0] || null
})

// Tables Headers
const headers = computed(() => [
  { title: "معرف الدفعة (Batch)", key: "batch_info", sortable: true },
  { title: "الاختبار", key: "exam_info", sortable: true },
  { title: "الأوراق المطبوعة", key: "papers_count", sortable: true, align: "center", width: "160px" },
  { title: "الحالة", key: "status", sortable: true, align: "center", width: "120px" },
  { title: "استعراض الأوراق", key: "actions", sortable: false, align: "center", width: "140px" },
])

const tableItems = computed(() => ({
  results: batches.value,
  count: batches.value.length,
  pagination: { count: batches.value.length, total: batches.value.length }
}))

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

// Methods
const fetchExamsList = async () => {
  loadingExams.value = true
  try {
    const params = {}
    if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
      params.institution_type = filterInstitutionType.value
    }
    if (filterInstitutionType.value === 'school') {
      if (filterStage.value) params.stage = filterStage.value
      if (filterClassTrack.value) params.class_track = filterClassTrack.value
      if (filterSubject.value) params.subject = filterSubject.value
    } else if (filterInstitutionType.value === 'university') {
      if (filterCollege.value) params.college = filterCollege.value
      if (filterDepartment.value) params.department = filterDepartment.value
      if (filterSpecialization.value) params.specialization = filterSpecialization.value
      if (filterSemesterSubject.value) params.semester_subject = filterSemesterSubject.value
    } else if (filterInstitutionType.value === 'institute') {
      if (filterInstituteField.value) params.institute_field = filterInstituteField.value
      if (filterInstituteEducationSystem.value) params.institute_education_system = filterInstituteEducationSystem.value
      if (filterInstituteSpecialization.value) params.institute_specialization = filterInstituteSpecialization.value
      if (filterInstituteSubject.value) params.institute_subject = filterInstituteSubject.value
    } else {
      if (filterSubject.value) params.subject = filterSubject.value
    }

    const resp = await api.get('/api/omr/exam-linking/', { params })
    if (resp.data && resp.data.results) {
      examsList.value = resp.data.results
      if (examsList.value.length > 0 && (!selectedExamId.value || !examsList.value.some(e => e.id === selectedExamId.value))) {
        selectedExamId.value = examsList.value[0].id
        await loadExamDetails(selectedExamId.value)
      } else if (examsList.value.length === 0) {
        selectedExamId.value = null
        examDetails.value = null
      }
    }
  } catch (err) {
    console.error('Failed to load exams list:', err)
  } finally {
    loadingExams.value = false
  }
}

const loadExamDetails = async (examId) => {
  if (!examId) return
  loadingExamDetails.value = true
  try {
    const resp = await api.get(`/api/omr/exam-linking/${examId}/`)
    examDetails.value = resp.data
    if (resp.data.registered_students && resp.data.registered_students.length > 0) {
      selectedStudentId.value = resp.data.registered_students[0].id
      sheetGenerationMode.value = 'all_students'
    } else {
      sheetGenerationMode.value = 'blank'
    }
  } catch (err) {
    console.error('Failed to load exam details:', err)
  } finally {
    loadingExamDetails.value = false
  }
}

const onExamSelected = (newId) => {
  if (newId) {
    loadExamDetails(newId)
  } else {
    examDetails.value = null
  }
}

const fetchBatches = async () => {
  loadingBatches.value = true
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
    loadingBatches.value = false
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

const seedSampleStudents = async () => {
  if (!selectedExamId.value) return
  seedingStudents.value = true
  try {
    await api.post(`/api/omr/exam-linking/${selectedExamId.value}/seed-students/`)
    await loadExamDetails(selectedExamId.value)
    fetchExamsList()
  } catch (err) {
    console.error('Failed to seed students:', err)
  } finally {
    seedingStudents.value = false
  }
}

const printSingleStudentCard = async (index) => {
  if (!batchStreamRef.value) return
  const isAudit = selectedSheetLayout.value === 'full_a4'
  const cards = batchStreamRef.value.querySelectorAll('.sheet-page-card')
  if (cards && cards[index]) {
    const printableEl = isAudit
      ? cards[index].querySelector('.yemeni-audit-report-sheet')
      : (cards[index].querySelector('svg.yemeni-ministry-sheet-svg') || cards[index].querySelector('svg'))
    if (printableEl) {
      const st = filteredStreamStudents.value[index]
      await printOmrElement(printableEl, {
        title: `${selectedExam.value?.uniqueCode || 'OMR'}_${st?.seat_number || st?.model_code || index + 1}`,
        isA5: selectedSheetLayout.value === 'compact_a5'
      })
    }
  }
}

const printCurrentQuestionPaper = async () => {
  if (questionPaperRef.value) {
    const paperEl = questionPaperRef.value.querySelector('.yemeni-official-question-paper') || questionPaperRef.value
    await printOfficialQuestionPaper(paperEl, {
      title: `ورقة_أسئلة_${selectedExam.value?.subject_name || 'الاختبار'}_النموذج_${selectedQuestionsModelCode.value}`,
      isA3: selectedQuestionPaperLayout.value === 'a3'
    })
  } else {
    const verObj = selectedQuestionsVersionObj.value
    await printExamPackage({
      examTitle: customStageTitle.value || selectedExam.value?.title || 'اختبار الشهادة الثانوية العامة',
      subjectName: selectedExam.value?.subject_name || 'الرياضيات',
      stageName: selectedExam.value?.stage_name || '',
      yearName: customExamYear.value || selectedExam.value?.year_name || '1445هـ - 2024-2023م',
      governorate: customGovernorate.value || selectedExam.value?.governorate || 'أمانة العاصمة',
      directorate: customDirectorate.value || selectedExam.value?.directorate || 'السبعين',
      centerName: customCenterName.value || activeSheetStudent.value?.school_name || selectedExam.value?.directorate || 'المركز الاختباري الرئيسي',
      centerCode: activeSheetStudent.value?.school_id || selectedExam.value?.id || '3026',
      versionCode: selectedQuestionsModelCode.value,
      studentName: sheetGenerationMode.value === 'student' ? activeSheetStudent.value?.student_name : '',
      seatNumber: sheetGenerationMode.value === 'student' ? activeSheetStudent.value?.seat_number : '',
      secretNumber: sheetGenerationMode.value === 'student' ? activeSheetStudent.value?.secret_number : '60',
      isA3: selectedQuestionPaperLayout.value === 'a3',
      questions: verObj?.questions || [],
      mode: 'questions_only'
    })
  }
}

const printCurrentExamPackage = async () => {
  const st = activeSheetStudent.value
  const vCode = st?.model_code || selectedBlankVersionCode.value || selectedQuestionsModelCode.value || 'A'
  const verObj = examDetails.value?.versions?.find(ver => ver.versionCode === vCode) || examDetails.value?.versions?.[0]

  let omrEl = null
  if (sheetArtboardRef.value) {
    omrEl = sheetArtboardRef.value.querySelector('.yemeni-audit-report-sheet') ||
            sheetArtboardRef.value.querySelector('svg.yemeni-ministry-sheet-svg') ||
            sheetArtboardRef.value.querySelector('svg')
  } else if (batchStreamRef.value) {
    omrEl = batchStreamRef.value.querySelector('.sheet-page-card:first-child .yemeni-audit-report-sheet') ||
            batchStreamRef.value.querySelector('.sheet-page-card:first-child svg.yemeni-ministry-sheet-svg') ||
            batchStreamRef.value.querySelector('svg')
  }

  await printExamPackage({
    examTitle: customStageTitle.value || selectedExam.value?.title || 'اختبار الشهادة الثانوية العامة',
    subjectName: selectedExam.value?.subject_name || 'الرياضيات',
    stageName: selectedExam.value?.stage_name || '',
    yearName: customExamYear.value || selectedExam.value?.year_name || '1445هـ - 2024-2023م',
    governorate: customGovernorate.value || selectedExam.value?.governorate || 'أمانة العاصمة',
    directorate: customDirectorate.value || selectedExam.value?.directorate || 'السبعين',
    centerName: customCenterName.value || st?.school_name || selectedExam.value?.directorate || 'المركز الاختباري الرئيسي',
    centerCode: st?.school_id || selectedExam.value?.id || '3026',
    versionCode: vCode,
    studentName: st?.student_name || '',
    seatNumber: st?.seat_number || '',
    secretNumber: st?.secret_number || '60',
    isA3: false,
    questions: verObj?.questions || [],
    omrElement: omrEl,
    mode: 'package',
    isA5: selectedSheetLayout.value === 'compact_a5'
  })
}

const printSingleSheet = async () => {
  await nextTick()
  let printableEl = null
  if (sheetArtboardRef.value) {
    printableEl = sheetArtboardRef.value.querySelector('.yemeni-audit-report-sheet') ||
                  sheetArtboardRef.value.querySelector('svg.yemeni-ministry-sheet-svg') ||
                  sheetArtboardRef.value.querySelector('svg')
  } else if (batchStreamRef.value) {
    printableEl = batchStreamRef.value.querySelector('.sheet-page-card:first-child .yemeni-audit-report-sheet') ||
                  batchStreamRef.value.querySelector('.sheet-page-card:first-child svg.yemeni-ministry-sheet-svg') ||
                  batchStreamRef.value.querySelector('svg')
  }

  if (printableEl) {
    await printOmrElement(printableEl, {
      title: `${selectedExam.value?.uniqueCode || 'OMR'}_${activeSheetStudent.value?.seat_number || activeSheetModelCode.value}`,
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

    // 1. Pick elements from visible stream if mounted
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

    // 2. Fallback to hidden staging container
    if (!elements.length) {
      const stagingEl = document.getElementById('omr-registry-batch-staging')
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
        title: `كشف_أوراق_تظليل_${selectedExam.value?.uniqueCode || 'الاختبار'}_${selectedSheetLayout.value}`,
        isA5: selectedSheetLayout.value === 'compact_a5'
      })

      // Update local state smoothly without tearing down the DOM
      const targetStudentIds = (filteredStreamStudents.value && filteredStreamStudents.value.length > 0)
        ? filteredStreamStudents.value.map(s => s.id)
        : (examDetails.value?.registered_students?.map(s => s.id) || [])

      if (selectedExamId.value && targetStudentIds.length > 0) {
        targetStudentIds.forEach(id => {
          const st = examDetails.value?.registered_students?.find(s => s.id === id)
          if (st) {
            st.is_printed = true
            st.printed_at = new Date().toLocaleTimeString('ar-YE')
            st.print_batch = batchId
          }
        })

        // Call backend in background
        api.post(`/api/omr/exam-linking/${selectedExamId.value}/mark-printed/`, {
          student_ids: targetStudentIds,
          batch_id: batchId
        }).catch(e => console.error("Mark printed error:", e))

        fetchBatches()

        batchPrintNotification.value = {
          show: true,
          message: `تم نقل وتجهيز ${elements.length} ورقة بنجاح للطباعة وتوثيق الدفعة (${batchId}) في سجل الطباعة!`,
          color: 'success'
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

const refreshData = async () => {
  await fetchExamsList()
  if (selectedExamId.value) {
    await loadExamDetails(selectedExamId.value)
  }
  await fetchBatches()
}

onMounted(async () => {
  await fetchExamsList()
  await fetchBatches()

  const qExam = route.query.exam || route.query.exam_id
  if (qExam) {
    selectedExamId.value = Number(qExam)
    await loadExamDetails(selectedExamId.value)
    activeTab.value = 'sheets'
  } else if (examsList.value.length > 0) {
    selectedExamId.value = examsList.value[0].id
    await loadExamDetails(selectedExamId.value)
  }
})
</script>

<style scoped>
.font-mono {
  font-family: monospace, monospace;
}
.unified-table-chip {
  border-radius: 6px !important;
  font-weight: 700 !important;
}
.omr-preview-viewport {
  background-color: #f1f5f9;
  min-height: 500px;
}
.all-sheets-stream {
  width: 100%;
}
.sheet-page-card {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  border: 1px solid #cbd5e1;
  background-color: #ffffff;
}

/* ── Lightweight Navigation Bar ── */
.registry-nav-bar {
  direction: rtl;
}

.registry-nav-container {
  display: flex;
  align-items: center;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 6px;
  gap: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.registry-nav-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 9px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.84rem;
  font-weight: 600;
  color: #64748b;
  background: transparent;
  transition: all 0.2s ease;
  user-select: none;
  white-space: nowrap;
}

.registry-nav-item:hover {
  background: #f8fafc;
  color: #334155;
}

.registry-nav-item.is-active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 800;
  border: 1px solid #bfdbfe;
}

.registry-nav-item.is-active .nav-icon {
  color: #2563eb;
}

@media (max-width: 1024px) {
  .registry-nav-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .registry-nav-container {
    grid-template-columns: 1fr;
  }
}
</style>
