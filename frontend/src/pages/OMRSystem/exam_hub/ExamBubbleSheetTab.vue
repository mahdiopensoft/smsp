<template>
  <div class="exam-bubble-sheet-tab">
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
              كل النماذج ({{ examDetails?.registered_students?.length || 0 }})
            </v-btn>
            <v-btn
              v-for="v in (examDetails?.versions || [])"
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
              :items="examDetails?.registered_students || []"
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
          <v-chip v-if="sheetGenerationMode === 'all_students'" size="small" color="success" variant="tonal" class="font-weight-bold">
            <v-icon start size="16">mdi-file-multiple</v-icon>
            جاهز للمعاينة والطباعة: {{ filteredStreamStudents.length }} ورقة (من إجمالي {{ examDetails?.registered_students?.length || 0 }} طالب)
          </v-chip>
          <v-chip v-else-if="activeSheetStudent && sheetGenerationMode === 'student'" size="small" color="primary" variant="tonal" class="font-weight-bold">
            <v-icon start size="16">mdi-account-check</v-icon>
            {{ activeSheetStudent.student_name }} (جلوس: {{ activeSheetStudent.seat_number }} | نموذج: {{ activeSheetStudent.model_code }})
          </v-chip>
          <v-chip v-else size="small" color="primary" variant="tonal" class="font-weight-bold">
            <v-icon start size="16">mdi-file-check</v-icon>
            ورقة عامة فارغة — النموذج {{ selectedBlankVersionCode }}
          </v-chip>

          <!-- Zoom Controls with Quick Presets -->
          <div class="d-flex align-center bg-grey-lighten-4 rounded-lg px-2 py-1 border ms-2 gap-1">
            <v-btn
              size="x-small"
              variant="text"
              class="font-weight-bold px-2"
              :color="sheetZoomLevel <= 0.86 ? 'primary' : 'medium-emphasis'"
              title="ملاءمة كاملة للشاشة (عرض كامل الورقة بدون تمرير)"
              @click="sheetZoomLevel = 0.85"
            >
              ملاءمة
            </v-btn>
            <v-btn
              size="x-small"
              variant="text"
              class="font-weight-bold px-2"
              :color="sheetZoomLevel >= 0.95 && sheetZoomLevel <= 1.05 ? 'primary' : 'medium-emphasis'"
              title="الحجم القياسي 100%"
              @click="sheetZoomLevel = 1.0"
            >
              100%
            </v-btn>
            <v-btn
              size="x-small"
              variant="text"
              class="font-weight-bold px-2"
              :color="sheetZoomLevel >= 1.15 ? 'primary' : 'medium-emphasis'"
              title="عرض متسع للقراءة والتدقيق"
              @click="sheetZoomLevel = 1.2"
            >
              متسع
            </v-btn>
            <v-divider vertical class="mx-1 my-1" />
            <v-btn icon size="x-small" variant="text" :disabled="sheetZoomLevel <= 0.5" @click="sheetZoomLevel = Math.max(0.5, Number((sheetZoomLevel - 0.1).toFixed(2)))">
              <v-icon size="15">mdi-minus</v-icon>
            </v-btn>
            <span class="text-caption font-weight-bold px-1 font-mono" style="min-width: 38px; text-align: center;">
              {{ Math.round(sheetZoomLevel * 100) }}%
            </span>
            <v-btn icon size="x-small" variant="text" :disabled="sheetZoomLevel >= 2.0" @click="sheetZoomLevel = Math.min(2.0, Number((sheetZoomLevel + 0.1).toFixed(2)))">
              <v-icon size="15">mdi-plus</v-icon>
            </v-btn>
          </div>
        </div>

        <!-- Actions Bar -->
        <div class="d-flex align-center gap-2 flex-wrap">
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
            :click="() => $emit('print-roster')"
          />
          <custom-btn
            icon="book-open-page-variant-outline"
            label="حزمة الاختبار"
            color="secondary"
            variant="tonal"
            class="font-weight-bold"
            :click="() => $emit('print-package')"
          />
          <custom-btn
            is-icon
            icon="tune-vertical"
            color="secondary"
            label="تعديل القالب في المصمم"
            :click="() => $emit('open-designer', activeExam)"
          />
        </div>
      </div>

      <!-- Row 3: Pagination & Quick Student Navigator (Active in all_students mode) -->
      <div
        v-if="sheetGenerationMode === 'all_students' && filteredStreamStudents.length > 0"
        class="d-flex align-center justify-space-between flex-wrap gap-2 pt-3 mt-3 border-t bg-grey-lighten-5 pa-2 rounded-xl"
      >
        <!-- Nav Controls -->
        <div class="d-flex align-center gap-1">
          <v-btn
            icon
            size="small"
            variant="tonal"
            color="primary"
            :disabled="currentPage <= 1 || perPage === -1"
            title="الورقة الأولى"
            @click="currentPage = 1"
          >
            <v-icon size="18">mdi-page-first</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            variant="tonal"
            color="primary"
            :disabled="currentPage <= 1 || perPage === -1"
            title="الورقة السابقة"
            @click="currentPage--"
          >
            <v-icon size="20">mdi-chevron-right</v-icon>
          </v-btn>

          <!-- Current Page Badge -->
          <div class="px-3 py-1 bg-white border rounded-lg text-caption font-weight-bold d-flex align-center gap-1 shadow-sm">
            <span class="text-medium-emphasis">ورقة</span>
            <span class="text-primary font-weight-black font-mono text-body-2">{{ perPage === -1 ? '1 - ' + filteredStreamStudents.length : currentPage }}</span>
            <span class="text-medium-emphasis">من</span>
            <span class="font-weight-black font-mono text-body-2">{{ totalPages }}</span>
          </div>

          <v-btn
            icon
            size="small"
            variant="tonal"
            color="primary"
            :disabled="currentPage >= totalPages || perPage === -1"
            title="الورقة التالية"
            @click="currentPage++"
          >
            <v-icon size="20">mdi-chevron-left</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            variant="tonal"
            color="primary"
            :disabled="currentPage >= totalPages || perPage === -1"
            title="الورقة الأخيرة"
            @click="currentPage = totalPages"
          >
            <v-icon size="18">mdi-page-last</v-icon>
          </v-btn>

          <!-- Compact Vuetify Pagination for Direct Page Clicking -->
          <v-pagination
            v-if="totalPages > 1 && totalPages <= 7 && perPage !== -1"
            v-model="currentPage"
            :length="totalPages"
            density="compact"
            size="small"
            rounded="circle"
            class="d-none d-md-inline-flex ms-1"
          />
        </div>

        <!-- Jump to Student Direct Dropdown -->
        <div class="d-flex align-center gap-2 flex-grow-1" style="max-width: 400px;">
          <v-autocomplete
            v-model="jumpToStudentIndex"
            :items="studentJumpOptions"
            item-title="title"
            item-value="value"
            placeholder="انتقال مباشر لطالب بالاسم أو رقم الجلوس..."
            density="compact"
            variant="outlined"
            rounded="lg"
            hide-details
            prepend-inner-icon="mdi-account-search"
            class="bg-white flex-grow-1"
            :disabled="perPage === -1"
            @update:model-value="onJumpToStudent"
          />
        </div>

        <!-- Per-Page Display Selector -->
        <div class="d-flex align-center gap-2">
          <span class="text-caption font-weight-bold text-medium-emphasis">عرض بالمعاينة:</span>
          <v-btn-toggle
            v-model="perPage"
            mandatory
            density="compact"
            color="primary"
            variant="outlined"
            rounded="lg"
          >
            <v-btn :value="1" class="font-weight-bold px-2" title="ورقة واحدة (فائقة السرعة والخفة)">
              1 ورقة
            </v-btn>
            <v-btn :value="2" class="font-weight-bold px-2">
              2
            </v-btn>
            <v-btn :value="5" class="font-weight-bold px-2">
              5
            </v-btn>
            <v-btn :value="-1" class="font-weight-bold px-2" title="عرض كافة الأوراق متتالية">
              الكل
            </v-btn>
          </v-btn-toggle>
        </div>
      </div>
    </div>

    <!-- Live OMR Sheet Artboard Canvas -->
    <div class="omr-preview-viewport pa-4 pa-md-6 rounded-2xl border text-center overflow-auto">
      <!-- ALL STUDENTS BATCH STREAM -->
      <div
        v-if="sheetGenerationMode === 'all_students'"
        ref="batchStreamRef"
        class="all-sheets-stream w-100 d-flex flex-column align-center gap-6"
      >
        <div v-if="!examDetails?.registered_students?.length" class="text-center py-12">
          <v-avatar size="56" color="grey-lighten-2" class="mb-3">
            <v-icon size="32" color="medium-emphasis">mdi-account-off-outline</v-icon>
          </v-avatar>
          <div class="text-subtitle-1 font-weight-bold mb-1">لا يوجد طلاب مسجلون في هذا الاختبار حتى الآن</div>
          <div class="text-caption text-medium-emphasis mb-4">يمكنك توليد وتعبئة طلاب تجريبيين للاختبار لمعاينة وطباعة أوراقهم</div>
          <v-btn color="primary" rounded="lg" prepend-icon="mdi-account-plus" @click="() => $emit('seed-students')">
            توليد كشف طلاب تجريبي للاختبار
          </v-btn>
        </div>

        <template v-else>
          <div
            v-for="(st, sIndex) in paginatedStudents"
            :key="`stream-sheet-${st.id}-${selectedSheetLayout}`"
            class="sheet-page-card bg-white position-relative text-start mb-6"
            :style="sheetArtboardStyle"
          >
            <!-- Page Indicator Banner (Hidden on Print) -->
            <div class="d-print-none sheet-page-header px-4 py-2 border-b d-flex align-center justify-space-between text-body-2 font-weight-bold">
              <div class="d-flex align-center gap-2 flex-wrap">
                <v-avatar color="primary" variant="flat" size="26" class="text-caption font-weight-black text-white">
                  {{ st.model_code || 'A' }}
                </v-avatar>
                <span class="text-high-emphasis">
                  الطالب: <strong class="text-primary font-weight-black">{{ st.student_name }}</strong>
                </span>
                <span class="text-medium-emphasis text-caption">
                  | رقم الجلوس: <strong class="text-dark font-mono font-weight-bold">{{ st.seat_number }}</strong>
                </span>
                <span v-if="st.secret_number" class="text-medium-emphasis text-caption">
                  | سري: <strong class="font-mono">{{ st.secret_number }}</strong>
                </span>
              </div>
              <div class="d-flex align-center gap-2">
                <v-chip size="small" color="primary" variant="tonal" class="font-weight-black font-mono">
                  ورقة {{ getRealStudentIndex(sIndex) }} من {{ filteredStreamStudents.length }}
                </v-chip>
                <v-btn
                  icon="mdi-printer"
                  size="x-small"
                  variant="text"
                  color="primary"
                  title="طباعة هذه الورقة مباشرة"
                  @click.stop="printSingleSheet"
                />
              </div>
            </div>

            <!-- Sheet Content Wrapper with Even Paper Margins -->
            <div class="sheet-content-wrapper">
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
          </div>
        </template>
      </div>

      <!-- SINGLE SHEET CANVAS -->
      <div
        v-else
        ref="sheetArtboardRef"
        class="sheet-artboard-container bg-white position-relative"
        :style="sheetArtboardStyle"
      >
        <div class="sheet-content-wrapper">
          <YemeniAuditReportSheet
            v-if="selectedSheetLayout === 'full_a4'"
            :key="`audit-sheet-${activeSheetStudent?.id || selectedBlankVersionCode}`"
            :student-name="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_name || '................................') : '................................'"
            :seat-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.seat_number || '................') : '................'"
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
            :question-marks="activeSheetQuestionMarks"
          />

          <YemeniMinistrySheet
            v-else
            :key="`compact-sheet-${activeSheetStudent?.id || selectedBlankVersionCode}`"
            layout-mode="compact_a5"
            :student-name="sheetGenerationMode === 'student' ? (activeSheetStudent?.student_name || '................................') : '................................'"
            :seat-number="sheetGenerationMode === 'student' ? (activeSheetStudent?.seat_number || '................') : '................'"
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

    <!-- Bottom Pagination (when in all_students mode) -->
    <div
      v-if="sheetGenerationMode === 'all_students' && totalPages > 1 && perPage !== -1"
      class="d-flex align-center justify-center gap-2 mt-4"
    >
      <v-pagination
        v-model="currentPage"
        :length="totalPages"
        total-visible="7"
        density="comfortable"
        rounded="lg"
        active-color="primary"
      />
    </div>

    <!-- Hidden Container for Batch Printing All Students' Sheets (Only mounted during printing) -->
    <div
      v-if="printingBatch"
      id="omr-batch-print-staging"
      style="position: fixed; left: -9999px; top: -9999px; width: 800px; opacity: 0; pointer-events: none; z-index: -9999;"
    >
      <div
        v-for="st in (filteredStreamStudents.length ? filteredStreamStudents : (examDetails?.registered_students || []))"
        :key="`batch-${st.id}-${selectedSheetLayout}`"
        class="batch-sheet-slot"
      >
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
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import api from '@/services/omr/client.js'
import YemeniMinistrySheet from '@/components/omr_templates/YemeniMinistrySheet.vue'
import YemeniAuditReportSheet from '@/components/omr_templates/YemeniAuditReportSheet.vue'
import { printOmrElement, printOmrBatch } from '../utils/omrPrint'

const props = defineProps({
  activeExam: { type: Object, default: () => ({}) },
  examDetails: { type: Object, default: () => ({}) },
})

const emit = defineEmits([
  'open-designer',
  'print-package',
  'print-roster',
  'seed-students',
  'refresh-details',
])

const sheetGenerationMode = ref('all_students')
const selectedStudentId = ref(null)
const selectedBlankVersionCode = ref('A')
const selectedSheetLayout = ref('compact_a5')
const sheetArtboardRef = ref(null)
const batchStreamRef = ref(null)
const printingBatch = ref(false)
const filterStreamModelCode = ref('all')

// ─── Pagination Controls for High Performance ───
const currentPage = ref(1)
const perPage = ref(1) // Default to 1 sheet for ultra-fast rendering & zero lag!
const jumpToStudentIndex = ref(null)

const customCenterName = ref('')
const customDirectorate = ref('')
const customGovernorate = ref('')
const customExamYear = ref('')
const customStageTitle = ref('')
const showAdjustmentsPanel = ref(false)
const batchPrintNotification = ref({ show: false, message: '', color: 'info' })

const sheetZoomLevel = ref(0.85)

const isA4 = computed(() => selectedSheetLayout.value === 'full_a4')
const sheetArtboardStyle = computed(() => {
  // A4 Portrait: 210 x 297 mm -> base width ~780px
  // A5 Landscape: 210 x 148.5 mm -> base width ~860px
  const baseWidth = isA4.value ? 780 : 860
  const scaledWidth = Math.round(baseWidth * sheetZoomLevel.value)

  return {
    width: '100%',
    maxWidth: `${scaledWidth}px`,
    margin: '0 auto',
    transformOrigin: 'top center',
    transition: 'max-width 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
  }
})

const filteredStreamStudents = computed(() => {
  let list = props.examDetails?.registered_students || []
  if (filterStreamModelCode.value && filterStreamModelCode.value !== 'all') {
    list = list.filter(st => (st.model_code || 'A') === filterStreamModelCode.value)
  }
  return list
})

// Total pages computation
const totalPages = computed(() => {
  if (perPage.value === -1) return 1
  return Math.ceil(filteredStreamStudents.value.length / perPage.value) || 1
})

// Current slice of students for preview
const paginatedStudents = computed(() => {
  if (perPage.value === -1) return filteredStreamStudents.value
  const start = (currentPage.value - 1) * perPage.value
  return filteredStreamStudents.value.slice(start, start + perPage.value)
})

const getRealStudentIndex = (sIndex) => {
  if (perPage.value === -1) return sIndex + 1
  return (currentPage.value - 1) * perPage.value + sIndex + 1
}

const studentJumpOptions = computed(() => {
  return filteredStreamStudents.value.map((st, idx) => {
    const pageNum = perPage.value === -1 ? 1 : Math.floor(idx / perPage.value) + 1
    return {
      title: `${idx + 1}. ${st.student_name} (جلوس: ${st.seat_number} | نموذج: ${st.model_code || 'A'})`,
      value: pageNum,
    }
  })
})

const onJumpToStudent = (targetPage) => {
  if (targetPage) {
    currentPage.value = targetPage
  }
}

watch([filterStreamModelCode, perPage], () => {
  currentPage.value = 1
  jumpToStudentIndex.value = null
})

const resetHeaderOverrides = () => {
  customCenterName.value = ''
  customDirectorate.value = ''
  customGovernorate.value = ''
  customExamYear.value = ''
  customStageTitle.value = ''
}

const versionCodeOptions = computed(() => {
  if (props.examDetails?.versions && Array.isArray(props.examDetails.versions)) {
    return props.examDetails.versions.map(v => v.versionCode || 'A')
  }
  return ['A', 'B', 'C', 'D']
})

const getQuestionsCountForVersion = (versionCode) => {
  const v = props.examDetails?.versions?.find(ver => ver.versionCode === versionCode) ||
            props.examDetails?.versions?.[0]
  if (v?.questions?.length) return v.questions.length
  if (v?.questionsCount) return v.questionsCount
  return props.activeExam?.total_questions || 20
}

const getSectionsForVersion = (versionCode) => {
  const v = props.examDetails?.versions?.find(ver => ver.versionCode === versionCode) ||
            props.examDetails?.versions?.[0]
  const qList = v?.questions || []
  const total = qList.length || v?.questionsCount || props.activeExam?.total_questions || 20
  let tfCount = 0
  let mcqCount = 0

  qList.forEach(q => {
    const typeStr = String(q.questionType || q.question_type || q.type || '').toLowerCase()
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
    const tfAvg = qList.filter(q => String(q.questionType || q.question_type || '').toLowerCase().includes('true') || String(q.questionType || q.question_type || '').toLowerCase().includes('صح')).reduce((acc, q) => acc + (parseFloat(q.assignedMark || q.mark) || 1), 0) / Math.max(1, tfCount)
    const mcqAvg = qList.filter(q => !String(q.questionType || q.question_type || '').toLowerCase().includes('true') && !String(q.questionType || q.question_type || '').toLowerCase().includes('صح')).reduce((acc, q) => acc + (parseFloat(q.assignedMark || q.mark) || 1), 0) / Math.max(1, mcqCount)
    return [
      { id: 'sec1', title: 'القسم الأول: أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: tfCount, choices: ['صح', 'خطأ'], mark: Math.round(tfAvg * 10) / 10 },
      { id: 'sec2', title: 'القسم الثاني: أسئلة الاختيار من متعدد', type: 'mcq', from_q: tfCount + 1, to_q: total, choices: ['1', '2', '3', '4'], mark: Math.round(mcqAvg * 10) / 10 }
    ]
  } else if (tfCount > 0) {
    const avg = qList.reduce((acc, q) => acc + (parseFloat(q.assignedMark || q.mark) || 1), 0) / Math.max(1, total)
    return [
      { id: 'sec1', title: 'أسئلة الصواب والخطأ', type: 'true_false', from_q: 1, to_q: total, choices: ['صح', 'خطأ'], mark: Math.round(avg * 10) / 10 }
    ]
  } else {
    const avg = qList.reduce((acc, q) => acc + (parseFloat(q.assignedMark || q.mark) || 1), 0) / Math.max(1, total)
    return [
      { id: 'sec1', title: 'أسئلة الاختيار من متعدد', type: 'mcq', from_q: 1, to_q: total, choices: ['1', '2', '3', '4'], mark: Math.round(avg * 10) / 10 }
    ]
  }
}

const activeSheetStudent = computed(() => {
  if (sheetGenerationMode.value !== 'student') return null
  if (!selectedStudentId.value && props.examDetails?.registered_students?.length) {
    return props.examDetails.registered_students[0]
  }
  return props.examDetails?.registered_students?.find(s => s.id === selectedStudentId.value) || null
})

const activeSheetModelCode = computed(() => {
  if (sheetGenerationMode.value === 'blank') {
    return selectedBlankVersionCode.value || 'A'
  }
  return activeSheetStudent.value?.model_code || 'A'
})

const activeSheetBarcode = computed(() => {
  const examId = props.activeExam?.id || 'EXAM'
  const model = activeSheetModelCode.value
  const seat = activeSheetStudent.value?.seat_number || 'BLANK'
  return activeSheetStudent.value?.barcode_value || `EXAM_${examId}_VER_${model}_SEAT_${seat}`
})

const activeSheetQr = computed(() => {
  const code = props.activeExam?.uniqueCode || 'EXAM'
  const model = activeSheetModelCode.value
  const seat = activeSheetStudent.value?.seat_number || 'BLANK'
  return activeSheetStudent.value?.qr_value || `${code}|${model}|${seat}`
})

const activeModelQuestionsCount = computed(() => {
  return getQuestionsCountForVersion(activeSheetModelCode.value)
})

const activeExamSections = computed(() => {
  return getSectionsForVersion(activeSheetModelCode.value)
})

const activeSheetAnswerKey = computed(() => {
  if (!props.examDetails?.versions) return {}
  const v = props.examDetails.versions.find(x => x.versionCode === activeSheetModelCode.value) || props.examDetails.versions[0]
  return v?.answerKey || v?.answer_key || {}
})

const activeSheetQuestionMarks = computed(() => {
  if (!props.examDetails?.versions) return {}
  const v = props.examDetails.versions.find(x => x.versionCode === activeSheetModelCode.value) || props.examDetails.versions[0]
  if (!v || !v.questions) return {}
  const marks = {}
  v.questions.forEach((q, idx) => {
    marks[q.orderIndex || q.id || idx + 1] = parseFloat(q.assignedMark || q.mark) || 1
  })
  return marks
})

const printSingleSheet = async () => {
  await nextTick()
  let printableEl = null
  let curStudent = null

  if (sheetGenerationMode.value === 'all_students') {
    printableEl = batchStreamRef.value?.querySelector('.sheet-page-card:first-child .yemeni-audit-report-sheet') ||
                  batchStreamRef.value?.querySelector('.sheet-page-card:first-child svg.yemeni-ministry-sheet-svg') ||
                  batchStreamRef.value?.querySelector('.sheet-page-card:first-child svg')
    curStudent = paginatedStudents.value?.[0]
  } else {
    printableEl = sheetArtboardRef.value?.querySelector('.yemeni-audit-report-sheet') ||
                  sheetArtboardRef.value?.querySelector('svg.yemeni-ministry-sheet-svg') ||
                  sheetArtboardRef.value?.querySelector('svg')
    curStudent = activeSheetStudent.value
  }

  if (printableEl) {
    await printOmrElement(printableEl, {
      title: `${props.activeExam?.uniqueCode || 'OMR'}_${curStudent?.seat_number || activeSheetModelCode.value}`,
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

    if (perPage.value === -1 && batchStreamRef.value) {
      if (isAudit) {
        elements = Array.from(batchStreamRef.value.querySelectorAll('.yemeni-audit-report-sheet'))
      } else {
        elements = Array.from(batchStreamRef.value.querySelectorAll('svg.yemeni-ministry-sheet-svg'))
        if (!elements.length) {
          elements = Array.from(batchStreamRef.value.querySelectorAll('svg'))
        }
      }
    }

    if (!elements.length) {
      await nextTick()
      const stagingEl = document.getElementById('omr-batch-print-staging')
      if (stagingEl) {
        if (isAudit) {
          elements = Array.from(stagingEl.querySelectorAll('.yemeni-audit-report-sheet'))
        } else {
          elements = Array.from(stagingEl.querySelectorAll('svg.yemeni-ministry-sheet-svg'))
          if (!elements.length) {
            elements = Array.from(stagingEl.querySelectorAll('svg'))
          }
        }
      }
    }

    if (elements.length > 0) {
      const batchId = `BATCH_${Date.now()}`
      await printOmrBatch(elements, {
        title: `كشف_أوراق_تظليل_${props.activeExam?.uniqueCode || 'الاختبار'}_${selectedSheetLayout.value}`,
        isA5: selectedSheetLayout.value === 'compact_a5'
      })

      const targetStudentIds = (filteredStreamStudents.value && filteredStreamStudents.value.length > 0)
        ? filteredStreamStudents.value.map(s => s.id)
        : (props.examDetails?.registered_students?.map(s => s.id) || [])

      if (props.activeExam && targetStudentIds.length > 0) {
        try {
          await api.post(`/api/omr/exam-linking/${props.activeExam.id}/mark-printed/`, {
            student_ids: targetStudentIds,
            batch_id: batchId
          })
          batchPrintNotification.value = {
            show: true,
            message: `تم نقل ${elements.length} ورقة بنجاح إلى أمر الطباعة وتوثيق الدفعة (${batchId}) في سجل الطباعة!`,
            color: 'success'
          }
          emit('refresh-details')
        } catch (e) {
          console.error('Failed to register print status:', e)
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

defineExpose({
  setStudent: (studentId) => {
    selectedStudentId.value = studentId
    sheetGenerationMode.value = 'student'
  },
  setMode: (mode) => {
    sheetGenerationMode.value = mode
  },
  printSingleSheet,
  batchPrintAllStudents,
  getPrintableElement: () => {
    return sheetArtboardRef.value?.querySelector('.yemeni-audit-report-sheet') ||
           sheetArtboardRef.value?.querySelector('svg.yemeni-ministry-sheet-svg') ||
           sheetArtboardRef.value?.querySelector('svg')
  },
  selectedSheetLayout,
  customCenterName,
  customDirectorate,
  customGovernorate,
  customExamYear,
  customStageTitle,
})
</script>

<style scoped>
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}
.omr-preview-viewport {
  min-height: 480px;
  max-height: calc(100vh - 280px);
  background: #f1f5f9;
  border-color: #e2e8f0 !important;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.sheet-page-card,
.sheet-artboard-container {
  display: block;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04), 0 0 0 1px rgba(0, 0, 0, 0.06);
  margin: 0 auto;
}

.sheet-page-header {
  background-color: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}

.sheet-content-wrapper {
  padding: 12px 14px 22px 14px;
  background: #ffffff;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
}

/* Ensure SVG sheets fill 100% of the wrapper with natural aspect ratio and clean margins */
.sheet-content-wrapper :deep(svg.yemeni-ministry-sheet-svg) {
  width: 100% !important;
  height: auto !important;
  max-width: 100% !important;
  display: block;
  margin: 0 auto;
  filter: none !important; /* Remove fuzzy filter drop-shadow to keep border lines razor-sharp */
}

.sheet-content-wrapper :deep(.yemeni-audit-report-sheet) {
  width: 100% !important;
  box-sizing: border-box;
}

.omr-preview-viewport::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
.omr-preview-viewport::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}
.omr-preview-viewport::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.font-mono {
  font-family: monospace, monospace;
}
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-6 { gap: 24px; }
</style>
