<template>
  <div class="qb-curriculum-exclusions-v4">
    <!-- ══════════════════════════════════════════════════════════════════════════ -->
    <!-- 1. FILTER FIELDS BAR (OPTIONS & SEARCH) -->
    <!-- ══════════════════════════════════════════════════════════════════════════ -->
    <filter-fields label="خيارات التصفية والبحث في سجل المحذوفات" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
      <v-row dense class="align-center">
        <!-- 1. نوع المؤسسة التعليمية -->
        <v-col cols="12" md="12" class="mb-3">
          <v-btn-toggle
            v-model="filterListInstType"
            mandatory
            color="primary"
            variant="outlined"
            density="compact"
            rounded="lg"
            class="w-100 d-flex flex-wrap"
            @update:model-value="applyFilters"
          >
            <v-btn value="school" class="flex-grow-1 font-weight-bold">
              <v-icon start size="16" color="teal">mdi-school</v-icon>
              مدارس التعليم العام
            </v-btn>
            <v-btn value="university" class="flex-grow-1 font-weight-bold">
              <v-icon start size="16" color="indigo">mdi-domain</v-icon>
              الجامعات والكليات
            </v-btn>
            <v-btn value="institute" class="flex-grow-1 font-weight-bold">
              <v-icon start size="16" color="amber-darken-3">mdi-tools</v-icon>
              المعاهد ومراكز التدريب
            </v-btn>
          </v-btn-toggle>
        </v-col>

        <!-- 2. العام الدراسي -->
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filterListYear"
            name="AcademicYear"
            placeholder="العام الدراسي"
            label="العام الدراسي"
            cols="12"
            :add="false"
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- 3. نطاق الحذف (وحدة / درس) -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterExclusionType"
            :items="[
              { value: null, title: 'كافة النطاقات (وحدات ودروس)' },
              { value: 'unit', title: 'وحدات دراسية كاملة' },
              { value: 'lesson', title: 'دروس وموضوعات محددة' }
            ]"
            item-value="value"
            item-title="title"
            placeholder="نطاق الحذف"
            label="نطاق الحذف"
            prepend-inner-icon="mdi-shape-outline"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- 4. بحث نصي مباشر -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="searchExclusionsQuery"
            placeholder="بحث بالمادة، الدرس، الوحدة، القرار..."
            label="بحث نصي"
            variant="outlined"
            density="compact"
            prepend-inner-icon="mdi-magnify"
            hide-details
            clearable
            class="mb-6"
            @keydown.enter="applyFilters"
          />
        </v-col>

        <!-- 5. أزرار الإجراءات -->
        <v-col cols="12" sm="6" md="3" class="d-flex align-center justify-end gap-2 mb-6">
          <custom-btn
            type="show"
            label="تصفية النتائج"
            color="primary"
            icon="mdi-filter"
            class="font-weight-bold px-6"
            :click="applyFilters"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ"
            icon="mdi-filter-off"
            class="font-weight-bold"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- ══════════════════════════════════════════════════════════════════════════ -->
    <!-- 3. ACTIVE APPROVED EXCLUSIONS DATA TABLE -->
    <!-- ══════════════════════════════════════════════════════════════════════════ -->
    <custom-data-table
      ref="tableRef"
      v-bind="{
        items,
        getData,
        headers: exclusionsTableHeaders,
        delItem: url,
        create: openExclusionDialog,
      }"
      :hasFilter="false"
      :log="false"
      :restore="false"
      :customLoading="loadingList"
    >
      <template v-slot:item-slot="{ item, key }">
        <!-- 1. العام الدراسي -->
        <template v-if="key === 'academic_year_name'">
          <div class="d-flex align-center gap-1">
            <v-icon size="16" color="primary">mdi-calendar-range</v-icon>
            <span class="font-weight-bold text-body-2">{{ item.academic_year_name || '-' }}</span>
          </div>
        </template>

        <!-- 2. نوع المؤسسة التعليمية -->
        <template v-else-if="key === 'institution_type'">
          <v-chip
            v-if="item.institution_type === 'university'"
            size="small"
            color="indigo"
            variant="tonal"
            class="font-weight-bold"
          >
            <v-icon start size="14">mdi-domain</v-icon>
            جامعي
          </v-chip>
          <v-chip
            v-else-if="item.institution_type === 'institute'"
            size="small"
            color="amber-darken-3"
            variant="tonal"
            class="font-weight-bold"
          >
            <v-icon start size="14">mdi-tools</v-icon>
            معهد مهني
          </v-chip>
          <v-chip
            v-else
            size="small"
            color="teal"
            variant="tonal"
            class="font-weight-bold"
          >
            <v-icon start size="14">mdi-school</v-icon>
            مدرسي
          </v-chip>
        </template>

        <!-- 3. المادة أو المقرر الدراسي -->
        <template v-else-if="key === 'subject_display'">
          <div class="d-flex align-center gap-1 font-weight-bold">
            <v-icon size="16" color="slate-600">mdi-book-open-page-variant-outline</v-icon>
            <span>{{ getSubjectDisplay(item) }}</span>
          </div>
        </template>

        <!-- 4. التصنيف الأكاديمي والهرمي (الصف / المسار / التخصص) -->
        <template v-else-if="key === 'hierarchy_display'">
          <span class="text-caption font-weight-medium text-medium-emphasis">
            {{ getHierarchyDisplay(item) }}
          </span>
        </template>

        <!-- 5. نطاق الحذف -->
        <template v-else-if="key === 'exclusion_type'">
          <v-chip
            size="x-small"
            :color="item.exclusion_type === 'unit' ? 'error' : 'deep-orange'"
            variant="tonal"
            class="font-weight-bold"
          >
            <v-icon start size="12">
              {{ item.exclusion_type === 'unit' ? 'mdi-folder-remove' : 'mdi-book-cancel' }}
            </v-icon>
            {{ item.exclusion_type_display || (item.exclusion_type === 'unit' ? 'وحدة كاملة' : 'درس محدد') }}
          </v-chip>
        </template>

        <!-- 6. المحتوى المستبعد بدقة -->
        <template v-else-if="key === 'target_name'">
          <div>
            <div class="font-weight-bold text-body-2 text-error d-flex align-center gap-1">
              <v-icon size="16" color="error">
                {{ item.exclusion_type === 'unit' ? 'mdi-folder-alert' : 'mdi-file-cancel' }}
              </v-icon>
              <span>{{ item.exclusion_type === 'unit' ? item.unit_name : item.lesson_name }}</span>
            </div>
            <div v-if="item.exclusion_type === 'lesson' && item.unit_name" class="text-caption text-medium-emphasis ps-5">
              الوحدة الأصل: {{ item.unit_name }}
            </div>
          </div>
        </template>

        <!-- 7. رقم أو قرار ومبرر الاستبعاد -->
        <template v-else-if="key === 'reason'">
          <div v-if="item.reason" class="text-caption text-truncate" style="max-width: 260px;" :title="item.reason">
            <v-icon size="14" color="slate-500" class="me-1">mdi-file-certificate-outline</v-icon>
            {{ item.reason }}
          </div>
          <span v-else class="text-caption text-medium-emphasis">-</span>
        </template>

        <!-- 8. إجراءات السجل (حذف وإعادة تضمين) -->
        <template v-else-if="key === 'actions'">
          <custom-btn
            type="delete"
            label="إلغاء الحذف وتضمين"
            color="error"
            variant="tonal"
            size="x-small"
            class="font-weight-bold"
            :click="() => deleteExclusionItem(item.id)"
          />
        </template>
      </template>
    </custom-data-table>

    <!-- ══════════════════════════════════════════════════════════════════════════ -->
    <!-- 4. CUSTOM DIALOG: DEFINE & MANAGE CURRICULUM EXCLUSIONS -->
    <!-- ══════════════════════════════════════════════════════════════════════════ -->
    <custom-dialog
      v-model="exclusionDialog"
      title="تحديد واستبعاد موضوعات من المنهج والمقررات"
      width="1150px"
      height="auto"
      persistent
    >
      <div class="pa-4 pa-md-5">
        <!-- ── Section 1: Hierarchy Context Selection Bar ── -->
        <v-card class="main-card pa-4 rounded-xl border-subtle mb-4" elevation="0">
          <!-- Institution Type & Academic Year Row -->
          <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-3 mb-3 border-b-subtle">
            <div class="d-flex align-center gap-2 flex-wrap">
              <v-btn-toggle
                v-model="institutionType"
                mandatory
                density="compact"
                color="primary"
                rounded="lg"
                variant="outlined"
                divided
                @update:model-value="onInstitutionTypeChange"
              >
                <v-btn value="school" class="px-4">
                  <v-icon start size="18" color="primary">mdi-school-outline</v-icon>
                  <span class="font-weight-medium">مدارس التعليم العام</span>
                </v-btn>
                <v-btn value="university" class="px-4">
                  <v-icon start size="18" color="indigo">mdi-domain</v-icon>
                  <span class="font-weight-medium">الجامعات والكليات</span>
                </v-btn>
                <v-btn value="institute" class="px-4">
                  <v-icon start size="18" color="amber-darken-3">mdi-tools</v-icon>
                  <span class="font-weight-medium">المعاهد ومراكز التدريب</span>
                </v-btn>
              </v-btn-toggle>
            </div>

            <div style="min-width: 250px; max-width: 320px;">
              <auto-list
                v-model="selectedYearId"
                name="AcademicYear"
                placeholder="العام الدراسي المستهدف *"
                label="العام الدراسي"
                cols="12"
                :add="false"
                @update:model-value="onYearOrSubjectChange"
              />
            </div>
          </div>

          <!-- Cascading Filters for Chosen Institution -->
          <v-row dense class="align-center">
            <!-- 🏫 SCHOOL SELECTORS -->
            <template v-if="institutionType === 'school'">
              <v-col cols="12" sm="4">
                <auto-list
                  v-model="selectedStageId"
                  name="EducationalStage"
                  placeholder="المرحلة الدراسية"
                  label="المرحلة الدراسية"
                  cols="12"
                  :add="false"
                  @update:model-value="onStageChange"
                />
              </v-col>
              <v-col cols="12" sm="4">
                <auto-list
                  v-model="selectedClassTrackId"
                  name="SchoolClassTrack"
                  :param="selectedStageId"
                  placeholder="الصف والمسار الدراسي *"
                  label="الصف والمسار"
                  cols="12"
                  :add="false"
                  :disabled="!selectedStageId"
                  @update:model-value="onClassTrackChange"
                />
              </v-col>
              <v-col cols="12" sm="4">
                <auto-list
                  v-model="selectedSubjectId"
                  name="Subject"
                  :param="selectedClassTrackId"
                  placeholder="المادة الدراسية *"
                  label="المادة الدراسية"
                  cols="12"
                  :add="false"
                  :disabled="!selectedClassTrackId"
                  @update:model-value="onYearOrSubjectChange"
                />
              </v-col>
            </template>

            <!-- 🎓 UNIVERSITY SELECTORS -->
            <template v-if="institutionType === 'university'">
              <v-col cols="12" sm="3">
                <auto-list
                  v-model="selectedCollegeId"
                  name="College"
                  placeholder="الكلية الجامعية"
                  label="الكلية"
                  cols="12"
                  :add="false"
                  @update:model-value="onCollegeChange"
                />
              </v-col>
              <v-col cols="12" sm="3">
                <auto-list
                  v-model="selectedDepartmentId"
                  name="DepartmentByCollege"
                  :param="selectedCollegeId"
                  placeholder="القسم الأكاديمي"
                  label="القسم"
                  cols="12"
                  :add="false"
                  :disabled="!selectedCollegeId"
                  @update:model-value="onDepartmentChange"
                />
              </v-col>
              <v-col cols="12" sm="3">
                <auto-list
                  v-model="selectedSpecializationId"
                  name="Specialization"
                  :param="selectedDepartmentId || selectedCollegeId"
                  placeholder="التخصص الأكاديمي"
                  label="التخصص"
                  cols="12"
                  :add="false"
                  :disabled="!selectedCollegeId && !selectedDepartmentId"
                  @update:model-value="onSpecializationChange"
                />
              </v-col>
              <v-col cols="12" sm="3">
                <auto-list
                  v-model="selectedSemesterSubjectId"
                  name="SemesterSubject"
                  :param="selectedSpecializationId"
                  placeholder="مقرر الفصل الجامعي *"
                  label="المقرر الجامعي"
                  cols="12"
                  :add="false"
                  :disabled="!selectedSpecializationId"
                  @update:model-value="onYearOrSubjectChange"
                />
              </v-col>
            </template>

            <!-- 🏢 INSTITUTE SELECTORS -->
            <template v-if="institutionType === 'institute'">
              <v-col cols="12" sm="2">
                <auto-list
                  v-model="selectedInstituteFieldId"
                  name="InstituteField"
                  placeholder="المجال المهني"
                  label="المجال"
                  cols="12"
                  :add="false"
                  @update:model-value="onInstituteFieldChange"
                />
              </v-col>
              <v-col cols="12" sm="2">
                <auto-list
                  v-model="selectedInstituteEducationSystemId"
                  name="InstituteEducationSystem"
                  :param="selectedInstituteFieldId"
                  placeholder="نظام التعليم"
                  label="نظام التدريب"
                  cols="12"
                  :add="false"
                  :disabled="!selectedInstituteFieldId"
                  @update:model-value="onInstituteEduSystemChange"
                />
              </v-col>
              <v-col cols="12" sm="3">
                <auto-list
                  v-model="selectedInstituteSpecializationId"
                  name="InstituteSpecialization"
                  :param="selectedInstituteSpecParam"
                  placeholder="التخصص المهني"
                  label="التخصص"
                  cols="12"
                  :add="false"
                  :disabled="!selectedInstituteEducationSystemId"
                  @update:model-value="onInstituteSpecChange"
                />
              </v-col>
              <v-col cols="12" sm="2">
                <auto-list
                  v-model="selectedInstituteCurriculumId"
                  name="InstituteCurriculum"
                  :param="selectedInstituteSpecializationId"
                  placeholder="الخطة التدريبية"
                  label="الخطة"
                  cols="12"
                  :add="false"
                  :disabled="!selectedInstituteSpecializationId"
                  @update:model-value="onInstituteCurriculumChange"
                />
              </v-col>
              <v-col cols="12" sm="3">
                <auto-list
                  v-model="selectedInstituteSubjectId"
                  name="InstituteSubject"
                  :param="selectedInstituteCurriculumId"
                  placeholder="المادة التدريبية *"
                  label="المادة التدريبية"
                  cols="12"
                  :add="false"
                  :disabled="!selectedInstituteCurriculumId"
                  @update:model-value="onYearOrSubjectChange"
                />
              </v-col>
            </template>
          </v-row>

          <!-- Decree / Ministerial Reason Field -->
          <div class="mt-3 pt-3 border-t-subtle">
            <v-text-field
              v-model="decreeReason"
              label="رقم القرار / التعميم أو مبرر الحذف (قرار وزاري / تعميم قطاع التعليم)"
              variant="outlined"
              density="compact"
              color="primary"
              prepend-inner-icon="mdi-file-document-edit-outline"
              placeholder="مثال: تعميم وزاري رقم (14) للعام الدراسي 2025/2026 باستبعاد الموضوعات الإثرائية"
              hide-details
            />
          </div>
        </v-card>

        <!-- ── Section 2: Interactive Curriculum Units & Lessons Tree ── -->
        <!-- A. Loading State -->
        <div v-if="loadingTree" class="text-center py-10 rounded-xl border-subtle bg-card">
          <v-progress-circular indeterminate color="primary" size="44" class="mb-3" />
          <p class="text-subtitle-2 font-weight-bold text-slate-700 mb-0">جاري تحميل شجرة موضوعات ووحدات المنهج...</p>
        </div>

        <!-- B. No Subject Selected State -->
        <div v-else-if="!isSubjectSelected" class="text-center py-10 rounded-xl border-subtle bg-slate-50">
          <v-avatar size="52" color="primary" variant="tonal" class="mb-3">
            <v-icon size="28" color="primary">mdi-cursor-default-click-outline</v-icon>
          </v-avatar>
          <h4 class="text-subtitle-1 font-weight-bold text-slate-800 mb-1">يرجى تحديد المادة أو المقرر الدراسي</h4>
          <p class="text-caption text-medium-emphasis mb-0">
            حدد العام الدراسي والمادة أعلاه لعرض قائمة الوحدات والدروس وتحديد المستبعد منها.
          </p>
        </div>

        <!-- C. Empty Units in Syllabus State -->
        <div v-else-if="treeData.length === 0" class="text-center py-10 rounded-xl border-subtle bg-slate-50">
          <v-avatar size="52" color="warning" variant="tonal" class="mb-3">
            <v-icon size="28" color="warning">mdi-folder-alert-outline</v-icon>
          </v-avatar>
          <h4 class="text-subtitle-1 font-weight-bold text-slate-800 mb-1">لا توجد وحدات أو دروس مسجلة لهذه المادة</h4>
          <p class="text-caption text-medium-emphasis mb-0">
            يرجى التأكد من تهيئة وإدخال وحدات ودروس المادة في شاشات النظام الأكاديمي أولاً.
          </p>
        </div>

        <!-- D. Active Curriculum Tree Panel -->
        <div v-else>
          <!-- Summary Counts & Bulk Toggle Actions -->
          <div class="tree-summary-bar d-flex align-center justify-space-between flex-wrap gap-3 mb-4 pa-3 rounded-xl border-subtle">
            <div class="d-flex align-center gap-2 flex-wrap">
              <v-chip color="primary" variant="tonal" size="small" class="font-weight-bold px-3">
                <v-icon start size="15">mdi-book-multiple-outline</v-icon>
                {{ treeData.length }} وحدات دراسية
              </v-chip>
              <v-chip
                :color="excludedUnitsCount > 0 ? 'error' : 'grey-darken-1'"
                :variant="excludedUnitsCount > 0 ? 'flat' : 'tonal'"
                size="small"
                class="font-weight-bold px-3"
              >
                <v-icon start size="15">mdi-folder-remove-outline</v-icon>
                {{ excludedUnitsCount }} وحدات مستبعدة
              </v-chip>
              <v-chip color="indigo" variant="tonal" size="small" class="font-weight-bold px-3">
                <v-icon start size="15">mdi-format-list-bulleted</v-icon>
                {{ totalLessonsCount }} دروس وموضوعات
              </v-chip>
              <v-chip
                :color="excludedLessonsCount > 0 ? 'error' : 'grey-darken-1'"
                :variant="excludedLessonsCount > 0 ? 'flat' : 'tonal'"
                size="small"
                class="font-weight-bold px-3"
              >
                <v-icon start size="15">mdi-book-cancel-outline</v-icon>
                {{ excludedLessonsCount }} دروس مستبعدة
              </v-chip>
            </div>

            <div class="d-flex align-center gap-2">
              <v-btn
                size="small"
                variant="tonal"
                color="error"
                prepend-icon="mdi-folder-remove-outline"
                class="font-weight-bold"
                rounded="lg"
                @click="excludeAll"
              >
                استبعاد كافة الوحدات
              </v-btn>
              <v-btn
                size="small"
                variant="tonal"
                color="success"
                prepend-icon="mdi-check-all"
                class="font-weight-bold"
                rounded="lg"
                @click="includeAll"
              >
                تضمين الكل (إلغاء الاستبعاد)
              </v-btn>
            </div>
          </div>

          <!-- Units Cards List -->
          <div class="d-flex flex-column gap-3 max-h-500 overflow-y-auto pe-1">
            <div
              v-for="unit in treeData"
              :key="unit.id"
              class="unit-card rounded-xl border-subtle transition-all"
              :class="{ 'unit-card--excluded': unit.is_excluded }"
            >
              <!-- Unit Header -->
              <div
                class="unit-card__header pa-3 px-4 d-flex align-center justify-space-between flex-wrap gap-2 border-b-subtle"
                :class="{ 'bg-red-50': unit.is_excluded, 'bg-slate-50': !unit.is_excluded }"
              >
                <div class="d-flex align-center gap-3">
                  <v-avatar
                    size="34"
                    rounded="lg"
                    :color="unit.is_excluded ? 'error' : 'primary'"
                    :variant="unit.is_excluded ? 'flat' : 'tonal'"
                    class="font-weight-bold text-body-2"
                  >
                    {{ unit.order || '#' }}
                  </v-avatar>
                  <div>
                    <div class="d-flex align-center gap-2">
                      <h4
                        class="text-subtitle-2 font-weight-bold mb-0"
                        :class="{ 'text-error': unit.is_excluded, 'text-slate-900': !unit.is_excluded }"
                      >
                        {{ unit.name }}
                      </h4>
                      <v-chip
                        v-if="unit.is_excluded"
                        size="x-small"
                        color="error"
                        variant="flat"
                        class="font-weight-bold"
                      >
                        مستبعدة بالكامل
                      </v-chip>
                    </div>
                    <span class="text-caption text-medium-emphasis">
                      تتضمن {{ unit.lessons ? unit.lessons.length : 0 }} دروس وموضوعات
                    </span>
                  </div>
                </div>

                <!-- Unit Exclusion Switch -->
                <div class="d-flex align-center gap-2">
                  <span
                    class="text-caption font-weight-bold"
                    :class="unit.is_excluded ? 'text-error' : 'text-medium-emphasis'"
                  >
                    {{ unit.is_excluded ? 'الوحدة مستبعدة بالكامل من الاختبارات' : 'استبعاد كامل موضوعات الوحدة' }}
                  </span>
                  <v-switch
                    v-model="unit.is_excluded"
                    color="error"
                    density="compact"
                    hide-details
                    inset
                    @update:model-value="(val) => onUnitToggle(unit, val)"
                  />
                </div>
              </div>

              <!-- Unit Lessons Grid -->
              <div class="pa-3">
                <div
                  v-if="!unit.lessons || unit.lessons.length === 0"
                  class="text-center py-2 text-medium-emphasis text-caption"
                >
                  لا توجد دروس مدخلة تحت هذه الوحدة.
                </div>
                <v-row dense v-else>
                  <v-col
                    v-for="lesson in unit.lessons"
                    :key="lesson.id"
                    cols="12"
                    sm="6"
                  >
                    <div
                      class="lesson-item pa-2 px-3 rounded-lg border-subtle d-flex align-center justify-space-between gap-2 transition-all cursor-pointer"
                      :class="{
                        'lesson-item--excluded': lesson.is_excluded || unit.is_excluded,
                        'lesson-item--included': !lesson.is_excluded && !unit.is_excluded
                      }"
                      @click="!unit.is_excluded && (lesson.is_excluded = !lesson.is_excluded)"
                    >
                      <div class="d-flex align-center gap-2 overflow-hidden">
                        <v-icon
                          size="18"
                          :color="lesson.is_excluded || unit.is_excluded ? 'error' : 'slate-500'"
                        >
                          {{ lesson.is_excluded || unit.is_excluded ? 'mdi-close-circle-outline' : 'mdi-book-outline' }}
                        </v-icon>
                        <span
                          class="text-body-2 font-weight-medium text-truncate"
                          :class="{
                            'text-error text-decoration-line-through': lesson.is_excluded || unit.is_excluded,
                            'text-slate-800': !lesson.is_excluded && !unit.is_excluded
                          }"
                        >
                          {{ lesson.name }}
                        </span>
                      </div>

                      <div class="d-flex align-center gap-2 flex-shrink-0" @click.stop>
                        <v-chip
                          size="x-small"
                          :color="lesson.is_excluded || unit.is_excluded ? 'error' : 'teal'"
                          :variant="lesson.is_excluded || unit.is_excluded ? 'flat' : 'tonal'"
                          class="font-weight-bold"
                        >
                          {{ lesson.is_excluded || unit.is_excluded ? 'مستبعد' : 'مشمول' }}
                        </v-chip>

                        <v-checkbox-btn
                          v-model="lesson.is_excluded"
                          :disabled="unit.is_excluded"
                          color="error"
                          density="compact"
                          hide-details
                        />
                      </div>
                    </div>
                  </v-col>
                </v-row>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Dialog Action Buttons -->
      <template #actions>
        <div class="w-100 pa-4 pt-2 border-t-subtle d-flex align-center justify-space-between flex-wrap gap-3">
          <div class="d-flex align-center gap-2">
            <v-icon color="primary" size="20">mdi-shield-check-outline</v-icon>
            <span class="text-caption font-weight-bold text-medium-emphasis">
              عند الحفظ، سيتم اعتماد المحذوفات رسمياً واستبعادها من نماذج الاختبارات لذلك العام.
            </span>
          </div>

          <div class="d-flex align-center gap-2">
            <custom-btn
              label="إغلاق وإلغاء"
              variant="tonal"
              color="secondary"
              :click="() => { exclusionDialog = false; }"
            />
            <custom-btn
              type="add"
              label="حفظ واعتماد المحذوفات لهذا العام"
              icon="mdi-content-save-check"
              color="primary"
              class="px-6 font-weight-bold shadow-sm"
              :loading="saving"
              :disabled="!isSubjectSelected || treeData.length === 0"
              :click="saveExclusions"
            />
          </div>
        </div>
      </template>
    </custom-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, getCurrentInstance } from 'vue'
import { examsService } from '@/services/examsService'

const { proxy } = getCurrentInstance()

// Endpoint URL for custom-data-table
const url = "api/exams/curriculum-exclusions/"

// Table State
const tableRef = ref(null)
const items = ref({ count: 0, results: [] })
const loadingList = ref(false)

// Table Filter State
const filterListInstType = ref('school')
const filterListYear = ref(null)
const filterExclusionType = ref(null)
const searchExclusionsQuery = ref('')

// Dialog & Creation State
const exclusionDialog = ref(false)
const institutionType = ref('school')
const selectedYearId = ref(null)

// School Hierarchy Selectors
const selectedStageId = ref(null)
const selectedClassTrackId = ref(null)
const selectedSubjectId = ref(null)

// University Hierarchy Selectors
const selectedCollegeId = ref(null)
const selectedDepartmentId = ref(null)
const selectedSpecializationId = ref(null)
const selectedSemesterSubjectId = ref(null)

// Institute Hierarchy Selectors
const selectedInstituteFieldId = ref(null)
const selectedInstituteEducationSystemId = ref(null)
const selectedInstituteSpecializationId = ref(null)
const selectedInstituteCurriculumId = ref(null)
const selectedInstituteSubjectId = ref(null)

// Decree / Reason
const decreeReason = ref('')

// Curriculum Tree State inside Dialog
const loadingTree = ref(false)
const saving = ref(false)
const treeData = ref([])

// Table Headers Definition
const exclusionsTableHeaders = [
  { title: 'العام الدراسي', key: 'academic_year_name', sortable: true },
  { title: 'نوع المؤسسة', key: 'institution_type', sortable: true },
  { title: 'المادة / المقرر', key: 'subject_display', sortable: true },
  { title: 'المرحلة / الصف / التخصص', key: 'hierarchy_display', sortable: false },
  { title: 'نطاق الحذف', key: 'exclusion_type', sortable: true },
  { title: 'المحتوى المستبعد', key: 'target_name', sortable: true },
  { title: 'قرار / مبرر الحذف', key: 'reason', sortable: false },
]



// Dialog Computed Props
const selectedInstituteSpecParam = computed(() => {
  const p = {}
  if (selectedInstituteFieldId.value) p.field = selectedInstituteFieldId.value
  if (selectedInstituteEducationSystemId.value) p.education_system = selectedInstituteEducationSystemId.value
  return Object.keys(p).length ? p : null
})

const isSubjectSelected = computed(() => {
  if (institutionType.value === 'school') return Boolean(selectedSubjectId.value)
  if (institutionType.value === 'university') return Boolean(selectedSemesterSubjectId.value)
  if (institutionType.value === 'institute') return Boolean(selectedInstituteSubjectId.value)
  return false
})

const excludedUnitsCount = computed(() => {
  return treeData.value.filter(u => u.is_excluded).length
})

const totalLessonsCount = computed(() => {
  return treeData.value.reduce((acc, u) => acc + (u.lessons?.length || 0), 0)
})

const excludedLessonsCount = computed(() => {
  let count = 0
  for (const u of treeData.value) {
    if (u.is_excluded) {
      count += u.lessons?.length || 0
    } else {
      count += u.lessons?.filter(l => l.is_excluded).length || 0
    }
  }
  return count
})

// ══════════════════════════════════════════════════════════════════════════════
// Lifecycle & Table Methods
// ══════════════════════════════════════════════════════════════════════════════
onMounted(async () => {
  await getData()
})

async function getData(params = {}) {
  loadingList.value = true
  const queryParams = {
    ...(params?.params || params || {}),
  }

  if (filterListInstType.value && filterListInstType.value !== 'all') {
    queryParams.institution_type = filterListInstType.value
  }
  if (filterListYear.value) {
    queryParams.academic_year = filterListYear.value
  }
  if (filterExclusionType.value) {
    queryParams.exclusion_type = filterExclusionType.value
  }
  if (searchExclusionsQuery.value && searchExclusionsQuery.value.trim()) {
    queryParams.search = searchExclusionsQuery.value.trim()
  }

  try {
    const res = await examsService.getCurriculumExclusions(queryParams)
    if (res && res.results) {
      items.value = res
    } else if (Array.isArray(res)) {
      items.value = { count: res.length, results: res }
    } else {
      items.value = { count: 0, results: [] }
    }
    return items.value
  } catch (err) {
    console.error('فشل جلب سجل المحذوفات:', err)
    items.value = { count: 0, results: [] }
  } finally {
    loadingList.value = false
  }
}

function applyFilters() {
  getData()
}

function resetFilters() {
  filterListInstType.value = 'school'
  filterListYear.value = null
  filterExclusionType.value = null
  searchExclusionsQuery.value = ''
  getData()
}

function getSubjectDisplay(item) {
  return item.subject_name || item.semester_subject_name || item.institute_subject_name || '-'
}

function getHierarchyDisplay(item) {
  if (item.institution_type === 'school') {
    return [item.stage_name, item.class_track_name].filter(Boolean).join(' - ') || '-'
  }
  if (item.institution_type === 'university') {
    return [item.college_name, item.department_name, item.specialization_name].filter(Boolean).join(' - ') || '-'
  }
  if (item.institution_type === 'institute') {
    return [item.institute_field_name, item.institute_specialization_name].filter(Boolean).join(' - ') || '-'
  }
  return '-'
}

async function deleteExclusionItem(id) {
  try {
    await examsService.deleteCurriculumExclusion(id)
    if (proxy?.$alert) {
      proxy.$alert('success', { message: 'تم إلغاء الحذف وإعادة تضمين المحتوى في المنهج بنجاح' })
    }
    await getData()
    if (exclusionDialog.value && isSubjectSelected.value) {
      await onYearOrSubjectChange()
    }
  } catch (err) {
    console.error('فشل إلغاء الحذف:', err)
  }
}

// ══════════════════════════════════════════════════════════════════════════════
// Dialog Management & Hierarchy Handlers
// ══════════════════════════════════════════════════════════════════════════
function openExclusionDialog() {
  exclusionDialog.value = true
  if (isSubjectSelected.value && treeData.value.length === 0) {
    onYearOrSubjectChange()
  }
}

function onInstitutionTypeChange() {
  selectedStageId.value = null
  selectedClassTrackId.value = null
  selectedSubjectId.value = null
  selectedCollegeId.value = null
  selectedDepartmentId.value = null
  selectedSpecializationId.value = null
  selectedSemesterSubjectId.value = null
  selectedInstituteFieldId.value = null
  selectedInstituteEducationSystemId.value = null
  selectedInstituteSpecializationId.value = null
  selectedInstituteCurriculumId.value = null
  selectedInstituteSubjectId.value = null
  treeData.value = []
}

function onStageChange() {
  selectedClassTrackId.value = null
  selectedSubjectId.value = null
  treeData.value = []
}

function onClassTrackChange() {
  selectedSubjectId.value = null
  treeData.value = []
}

function onCollegeChange() {
  selectedDepartmentId.value = null
  selectedSpecializationId.value = null
  selectedSemesterSubjectId.value = null
  treeData.value = []
}

function onDepartmentChange() {
  selectedSpecializationId.value = null
  selectedSemesterSubjectId.value = null
  treeData.value = []
}

function onSpecializationChange() {
  selectedSemesterSubjectId.value = null
  treeData.value = []
}

function onInstituteFieldChange() {
  selectedInstituteEducationSystemId.value = null
  selectedInstituteSpecializationId.value = null
  selectedInstituteCurriculumId.value = null
  selectedInstituteSubjectId.value = null
  treeData.value = []
}

function onInstituteEduSystemChange() {
  selectedInstituteSpecializationId.value = null
  selectedInstituteCurriculumId.value = null
  selectedInstituteSubjectId.value = null
  treeData.value = []
}

function onInstituteSpecChange() {
  selectedInstituteCurriculumId.value = null
  selectedInstituteSubjectId.value = null
  treeData.value = []
}

function onInstituteCurriculumChange() {
  selectedInstituteSubjectId.value = null
  treeData.value = []
}

async function onYearOrSubjectChange() {
  if (!isSubjectSelected.value) {
    treeData.value = []
    return
  }

  loadingTree.value = true
  try {
    const params = {
      year_id: selectedYearId.value,
      institution_type: institutionType.value,
      subject_id: selectedSubjectId.value,
      stage_id: selectedStageId.value,
      class_track_id: selectedClassTrackId.value,
      semester_subject_id: selectedSemesterSubjectId.value,
      institute_subject_id: selectedInstituteSubjectId.value,
    }

    const res = await examsService.getCurriculumTreeForSubject(params)
    if (res && res.success) {
      treeData.value = res.tree || []
      const firstReason = res.tree.find(u => u.reason)?.reason || res.tree.flatMap(u => u.lessons || []).find(l => l.reason)?.reason
      if (firstReason && !decreeReason.value) {
        decreeReason.value = firstReason
      }
    } else {
      treeData.value = []
    }
  } catch (err) {
    console.error('فشل جلب وحدات المنهج:', err)
    treeData.value = []
  } finally {
    loadingTree.value = false
  }
}

function onUnitToggle(unit, val) {
  if (unit.lessons) {
    unit.lessons.forEach(l => {
      l.is_excluded = val
    })
  }
}

function excludeAll() {
  treeData.value.forEach(u => {
    u.is_excluded = true
    if (u.lessons) {
      u.lessons.forEach(l => { l.is_excluded = true })
    }
  })
}

function includeAll() {
  treeData.value.forEach(u => {
    u.is_excluded = false
    if (u.lessons) {
      u.lessons.forEach(l => { l.is_excluded = false })
    }
  })
}

async function saveExclusions() {
  if (!selectedYearId.value) {
    if (proxy?.$alert) proxy.$alert('errorData', { message: 'يرجى تحديد العام الدراسي أولاً' })
    return
  }

  saving.value = true
  try {
    const excluded_unit_ids = []
    const excluded_lesson_ids = []
    const scope_unit_ids = treeData.value.map(u => u.id)

    for (const u of treeData.value) {
      if (u.is_excluded) {
        excluded_unit_ids.push(u.id)
      } else if (u.lessons) {
        for (const l of u.lessons) {
          if (l.is_excluded) {
            excluded_lesson_ids.push(l.id)
          }
        }
      }
    }

    const payload = {
      academic_year_id: selectedYearId.value,
      institution_type: institutionType.value,
      scope_unit_ids,
      excluded_unit_ids,
      excluded_lesson_ids,
      reason: decreeReason.value,
      stage_id: selectedStageId.value,
      class_track_id: selectedClassTrackId.value,
      subject_id: selectedSubjectId.value,
      college_id: selectedCollegeId.value,
      department_id: selectedDepartmentId.value,
      specialization_id: selectedSpecializationId.value,
      semester_subject_id: selectedSemesterSubjectId.value,
      institute_field_id: selectedInstituteFieldId.value,
      institute_education_system_id: selectedInstituteEducationSystemId.value,
      institute_specialization_id: selectedInstituteSpecializationId.value,
      institute_curriculum_id: selectedInstituteCurriculumId.value,
      institute_subject_id: selectedInstituteSubjectId.value,
    }

    const res = await examsService.syncCurriculumExclusions(payload)
    if (res && res.success) {
      if (proxy?.$alert) {
        proxy.$alert('success', {
          title: 'تم الاعتماد بنجاح',
          message: `تم حفظ المحذوفات بنجاح (${excluded_unit_ids.length} وحدات و ${excluded_lesson_ids.length} دروس). تم استبعادها من الاختبارات لهذا العام.`
        })
      }
      exclusionDialog.value = false
      await getData()
    }
  } catch (err) {
    console.error('فشل حفظ المحذوفات:', err)
    if (proxy?.$alert) {
      proxy.$alert('errorData', { message: err?.response?.data?.message || err.message || 'فشل حفظ المحذوفات' })
    }
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.qb-curriculum-exclusions-v4 {
  animation: fadeIn 0.3s ease-in-out;
}

.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.border-subtle {
  border: 1px solid rgba(var(--v-border-color), 0.12);
}

.border-b-subtle {
  border-bottom: 1px solid rgba(var(--v-border-color), 0.12);
}

.border-t-subtle {
  border-top: 1px solid rgba(var(--v-border-color), 0.12);
}

.tree-summary-bar {
  background: #f8fafc !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
}

.unit-card {
  background: rgb(var(--v-theme-surface)) !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
  overflow: hidden;
}

.unit-card--excluded {
  border-color: rgba(var(--v-theme-error), 0.45) !important;
}

.bg-slate-50 {
  background: #f8fafc !important;
}

.bg-red-50 {
  background: #fef2f2 !important;
}

.text-slate-800 {
  color: #1e293b !important;
}

.text-slate-900 {
  color: #0f172a !important;
}

.lesson-item {
  background: rgb(var(--v-theme-surface));
  user-select: none;
}

.lesson-item--included:hover {
  background: #f1f5f9;
}

.lesson-item--excluded {
  background: #fef2f2 !important;
  border-color: rgba(var(--v-theme-error), 0.35) !important;
}

.cursor-pointer {
  cursor: pointer;
}

.max-h-500 {
  max-height: 480px;
}

.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
