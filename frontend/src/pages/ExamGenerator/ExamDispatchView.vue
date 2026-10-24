<template>
  <div class="exam-dispatch-page">
    <!-- TAB 1: LIST & MONITOR VIEW -->
    <div v-if="currentTab === 'list'">
      <!-- System Filters Component -->
      <filter-fields label="خيارات البحث وتصفية مهام التوزيع" class="main-card border-0 pa-5 rounded-2xl mb-8">
        <v-row dense class="align-center">
          <!-- فلتر نوع المؤسسة والنظام التعليمي (مدارس / جامعات / معاهد) -->
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="filterInstitutionType"
              :items="institutionTypeFilterOptions"
              item-title="label"
              item-value="value"
              placeholder="نوع المؤسسة (مدارس / جامعات / معاهد)"
              prepend-inner-icon="mdi-domain"
              clearable
              density="compact"
              variant="outlined"
              hide-details
              class="mb-6"
              @update:model-value="onInstitutionTypeFilterChange"
            >
              <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" :prepend-icon="item.raw.icon" />
              </template>
            </v-select>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="filterTargetLevel"
              :items="targetLevelFilterOptions"
              item-title="label"
              item-value="value"
              placeholder="مستوى الاستهداف الهرمي"
              prepend-inner-icon="mdi-sitemap"
              clearable
              density="compact"
              variant="outlined"
              hide-details
              class="mb-6"
              @update:model-value="applyFilters"
            />
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="filterStatus"
              :items="statusFilterOptions"
              item-title="label"
              item-value="value"
              placeholder="حالة المهمة"
              prepend-inner-icon="mdi-check-circle-outline"
              clearable
              density="compact"
              variant="outlined"
              hide-details
              class="mb-6"
              @update:model-value="applyFilters"
            />
          </v-col>

          <v-col cols="12" sm="12" md="3" class="d-flex align-center justify-end gap-2">
            <custom-btn
              type="show"
              label="تصفية"
              color="primary"
              class="font-weight-bold px-6 mb-6"
              :click="applyFilters"
            />
            <custom-btn
              type="cancel_filter"
              label="تفريغ الفلاتر"
              variant="tonal"
              color="error"
              class="font-weight-bold mb-6"
              :click="resetFilters"
            />
          </v-col>
        </v-row>
      </filter-fields>

      <!-- System Custom Data Table -->
      <v-card class="main-card rounded-2xl overflow-hidden mb-8 border-subtle" elevation="0">
        <custom-data-table
          :headers="tableHeaders"
          :items="tableItems"
          :getData="getData"
          :customLoading="loading"
          class="bg-transparent"
          :hasFilter="false"
          :log="false"
          :restore="false"
          :showSelect="false"
          :editItem="false"
        >
          <!-- Table Header Actions (Move 'جدولة توزيع جديد' button here) -->
          <template #header-actions>
            <custom-btn
              type="create"
              label="جدولة توزيع جديد"
              color="primary"
              class="font-weight-bold px-4"
              :click="openNewDispatchWizard"
            />
          </template>

          <template v-slot:item-slot="{ item, key }">
            <!-- Title & Exam Details -->
            <template v-if="key === 'title'">
              <div class="d-flex align-center gap-3 py-2">
                <v-avatar color="primary" variant="tonal" size="38" class="rounded-lg">
                  <v-icon size="20">mdi-file-document-outline</v-icon>
                </v-avatar>
                <div>
                  <div class="font-weight-bold text-subtitle-2 text-slate-800">{{ item.title }}</div>
                  <div class="text-caption text-medium-emphasis d-flex align-center gap-1">
                    <span>{{ item.exam_title }}</span>
                    <v-chip size="x-small" color="primary" variant="tonal" class="ms-1 font-weight-bold">
                      {{ item.exam_unique_code }}
                    </v-chip>
                  </div>
                </div>
              </div>
            </template>

            <!-- Institution Type -->
            <template v-else-if="key === 'institution_type'">
              <v-chip size="small" :color="getInstTypeColor(item)" variant="tonal" class="font-weight-bold">
                <v-icon size="14" start>{{ getInstTypeIcon(item) }}</v-icon>
                {{ getInstTypeLabel(item) }}
              </v-chip>
            </template>

            <!-- Target Level -->
            <template v-else-if="key === 'target_level'">
              <v-chip size="small" :color="getLevelColor(item.target_level)" variant="tonal" class="font-weight-bold">
                <v-icon size="14" start>{{ getLevelIcon(item.target_level) }}</v-icon>
                {{ getLevelLabel(item.target_level) }}
              </v-chip>
            </template>

            <!-- Schools Receipt Progress -->
            <template v-else-if="key === 'targeted_schools_count'">
              <div class="d-flex align-center gap-2">
                <v-progress-linear
                  :model-value="item.targeted_schools_count ? (item.received_schools_count / item.targeted_schools_count) * 100 : 0"
                  color="indigo"
                  height="8"
                  rounded
                  style="width: 80px"
                />
                <span class="text-caption font-weight-bold">
                  {{ item.received_schools_count || 0 }} / {{ item.targeted_schools_count || 0 }}
                </span>
              </div>
            </template>

            <!-- Timing Windows -->
            <template v-else-if="key === 'accessible_from'">
              <div class="text-caption font-weight-bold text-slate-800">
                <v-icon size="14" color="amber-darken-2" class="me-1">mdi-printer</v-icon>
                {{ formatDateTime(item.accessible_from) }}
              </div>
              <div class="text-caption text-medium-emphasis">
                <v-icon size="14" color="indigo" class="me-1">mdi-play-circle-outline</v-icon>
                {{ formatDateTime(item.exam_start_at) }}
              </div>
            </template>

            <!-- Delivery Mode -->
            <template v-else-if="key === 'delivery_mode'">
              <v-chip size="small" variant="tonal" color="teal" class="font-weight-bold">
                <v-icon size="14" start>mdi-card-text-outline</v-icon>
                طباعة كراسات + OMR
              </v-chip>
            </template>

            <!-- Status -->
            <template v-else-if="key === 'status'">
              <v-chip size="small" :color="getStatusColor(item.status)" variant="tonal" class="font-weight-bold">
                <v-icon size="12" start>mdi-circle</v-icon>
                {{ getStatusLabel(item.status) }}
              </v-chip>
            </template>

            <!-- Action Buttons using custom-btn & action menu -->
            <template v-else-if="key === 'actions'">
              <div class="d-flex align-center justify-center gap-1">
                <custom-btn
                  label="متابعة حية"
                  icon="radar"
                  color="indigo"
                  variant="tonal"
                  class="font-weight-bold px-3"
                  :click="() => openLiveMonitor(item)"
                />
                <v-menu location="bottom end">
                  <template v-slot:activator="{ props }">
                    <v-btn icon="mdi-dots-vertical" variant="text" size="small" color="slate-600" v-bind="props" />
                  </template>
                  <v-list density="compact" class="rounded-xl border elevation-4">
                    <v-list-item
                      v-if="item.status !== 'accessible' && item.status !== 'completed' && item.status !== 'cancelled'"
                      prepend-icon="mdi-lock-open-alert"
                      title="فك حجب فوري (طوارئ)"
                      class="text-amber-darken-3 font-weight-bold"
                      @click="promptForceUnlock(item)"
                    />
                    <v-list-item
                      v-if="item.status !== 'completed' && item.status !== 'cancelled'"
                      prepend-icon="mdi-close-circle-outline"
                      title="إلغاء مهمة التوزيع"
                      class="text-error font-weight-bold"
                      @click="promptCancelDispatch(item)"
                    />
                  </v-list>
                </v-menu>
              </div>
            </template>
          </template>
        </custom-data-table>
      </v-card>
    </div>

    <!-- TAB 2: WIZARD CREATION VIEW -->
    <div v-else-if="currentTab === 'wizard'">
      <v-card class="main-card rounded-2xl border-subtle pa-6 mb-8" elevation="0">
        <!-- Wizard Top Bar: Return Icon Button opposite Stepper Indicator -->
        <div class="d-flex align-center justify-space-between mb-6 pb-4 border-b">
          <!-- Return Icon Button -->
          <v-tooltip text="العودة لقائمة التوزيعات" location="bottom">
            <template v-slot:activator="{ props }">
              <v-btn
                v-bind="props"
                icon="mdi-arrow-right"
                variant="outlined"
                color="slate-700"
                density="comfortable"
                class="rounded-xl border shadow-xs"
                @click="currentTab = 'list'"
              />
            </template>
          </v-tooltip>

          <!-- Stepper Indicator (Aligned opposite return button) -->
          <div class="wizard-stepper d-flex justify-center flex-grow-1 mx-4">
            <div class="d-flex align-center gap-3 bg-slate-50 pa-2 px-5 rounded-2xl border">
              <div
                v-for="step in [1, 2, 3]"
                :key="step"
                class="step-item d-flex align-center gap-2"
                :class="{ 
                  'cursor-pointer': canNavigateToStep(step),
                  'step-active': currentStep === step,
                  'step-done': currentStep > step 
                }"
                @click="canNavigateToStep(step) && (currentStep = step)"
              >
                <v-avatar size="32" :color="currentStep === step ? 'primary' : currentStep > step ? 'teal' : 'slate-200'" class="font-weight-bold text-white shadow-xs">
                  <v-icon v-if="currentStep > step" size="18">mdi-check</v-icon>
                  <span v-else>{{ step }}</span>
                </v-avatar>
                <span class="text-subtitle-2 font-weight-bold" :class="currentStep === step ? 'text-primary' : currentStep > step ? 'text-teal-darken-2' : 'text-medium-emphasis'">
                  {{ stepTitles[step - 1] }}
                </span>
                <v-icon v-if="step < 3" color="slate-300" class="ms-2">mdi-chevron-left</v-icon>
              </div>
            </div>
          </div>

          <!-- Symmetrical Spacer -->
          <div style="width: 40px;" class="d-none d-sm-block"></div>
        </div>

        <!-- STEP 1: EXAM SELECTION -->
        <div v-if="currentStep === 1">
          <!-- Enhanced Institution Type Filter Bar -->
          <div class="pa-3 px-4 rounded-2xl bg-white border mb-5 shadow-xs">
            <div class="d-flex align-center gap-3 flex-wrap">
              <span class="text-caption font-weight-bold text-slate-700 d-flex align-center gap-1">
                <v-icon size="16" color="primary">mdi-filter-variant</v-icon>
                <span>نوع المؤسسة:</span>
              </span>
              <div class="d-flex align-center gap-2 flex-wrap">
                <v-btn
                  v-for="opt in institutionTypeFilterTabs"
                  :key="opt.value"
                  size="small"
                  :variant="filterExamInstitutionType === opt.value ? 'flat' : 'outlined'"
                  :color="filterExamInstitutionType === opt.value ? 'primary' : 'slate-600'"
                  class="font-weight-bold rounded-lg px-4 transition-all"
                  @click="filterExamInstitutionType = opt.value"
                >
                  <v-icon start size="16">{{ opt.icon }}</v-icon>
                  <span>{{ opt.label }}</span>
                  <v-chip
                    size="x-small"
                    class="ms-2 font-weight-black"
                    :color="filterExamInstitutionType === opt.value ? 'white' : 'primary'"
                    :variant="filterExamInstitutionType === opt.value ? 'flat' : 'tonal'"
                    :class="filterExamInstitutionType === opt.value ? 'text-primary' : ''"
                  >
                    {{ opt.count }}
                  </v-chip>
                </v-btn>
              </div>
            </div>
          </div>

          <!-- Empty State if no exams found -->
          <div v-if="filteredAvailableExams.length === 0" class="pa-8 text-center border rounded-2xl bg-slate-50 mb-6">
            <v-icon size="48" color="slate-400" class="mb-2">mdi-file-document-alert-outline</v-icon>
            <div class="text-subtitle-1 font-weight-bold text-slate-700">
              لا توجد اختبارات معتمدة مطابقة للبحث أو للمسار المحدد حالياً
            </div>
            <div class="text-caption text-medium-emphasis mt-1">
              يمكنك اعتماد اختبارات جديدة من شاشة «أرشيف الاختبارات» أو التحقق من معايير البحث.
            </div>
          </div>

          <!-- Exams Table using custom-data-table Component -->
          <v-card v-else class="main-card rounded-2xl overflow-hidden mb-6 border-subtle" elevation="0">
            <custom-data-table
              :headers="wizardExamHeaders"
              :items="wizardExamsTableItems"
              :getData="getWizardExamsData"
              :customLoading="loading"
              class="bg-transparent"
              :hasFilter="false"
              :log="false"
              :restore="false"
              :showSelect="false"
              :editItem="false"
            >
              <template v-slot:item-slot="{ item, key }">
                <!-- Select Button / Radio -->
                <template v-if="key === 'select'">
                  <div class="text-center py-1">
                    <v-btn
                      size="small"
                      :variant="selectedExam?.id === item.id ? 'flat' : 'outlined'"
                      :color="selectedExam?.id === item.id ? 'primary' : 'slate-500'"
                      class="font-weight-bold rounded-lg"
                      :disabled="!!getExamActiveDistribution(item)"
                      @click.stop="selectExam(item)"
                    >
                      <v-icon start size="16">
                        {{ selectedExam?.id === item.id ? 'mdi-radiobox-marked' : 'mdi-radiobox-blank' }}
                      </v-icon>
                      {{ selectedExam?.id === item.id ? 'محدد' : 'تحديد' }}
                    </v-btn>
                  </div>
                </template>

                <!-- Unique Code -->
                <template v-else-if="key === 'unique_code'">
                  <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold font-mono">
                    {{ item.uniqueCode || item.unique_code }}
                  </v-chip>
                </template>

                <!-- Title -->
                <template v-else-if="key === 'title'">
                  <div 
                    class="font-weight-bold text-slate-800 cursor-pointer hover:text-primary transition-colors py-1"
                    @click="!getExamActiveDistribution(item) && selectExam(item)"
                  >
                    {{ item.title }}
                  </div>
                </template>

                <!-- Institution Type -->
                <template v-else-if="key === 'institution_type'">
                  <v-chip
                    size="x-small"
                    :color="item.institution_type === 'institute' ? 'warning' : item.institution_type === 'university' ? 'info' : 'emerald'"
                    variant="tonal"
                    class="font-weight-bold"
                  >
                    {{ item.institution_type === 'institute' ? 'معاهد' : item.institution_type === 'university' ? 'جامعة' : 'مدرسة' }}
                  </v-chip>
                </template>

                <!-- Subject -->
                <template v-else-if="key === 'subject_name'">
                  <div class="d-flex align-center gap-1">
                    <v-icon size="14" color="primary">mdi-book-open-outline</v-icon>
                    <span class="text-body-2 font-weight-medium">{{ item.subject_name || 'عام' }}</span>
                  </div>
                </template>

                <!-- Academic Year -->
                <template v-else-if="key === 'year_name'">
                  <span class="text-caption font-weight-bold">{{ item.year_name || '2025/2026' }}</span>
                </template>

                <!-- Target Scope Level -->
                <template v-else-if="key === 'target_scope_level'">
                  <v-chip
                    size="x-small"
                    :color="item.target_scope_level === 'governorate' ? 'deep-purple' : item.target_scope_level === 'directorate' ? 'indigo' : item.target_scope_level === 'school' ? 'amber-darken-3' : 'teal'"
                    variant="tonal"
                    class="font-weight-bold"
                  >
                    <v-icon start size="12">{{ item.target_scope_level === 'governorate' ? 'mdi-map-marker-radius' : item.target_scope_level === 'directorate' ? 'mdi-town-hall' : item.target_scope_level === 'school' ? 'mdi-school' : 'mdi-earth' }}</v-icon>
                    {{ item.target_scope_level === 'governorate' ? 'محافظات محددة' : item.target_scope_level === 'directorate' ? 'مديريات محددة' : item.target_scope_level === 'school' ? 'مدارس محددة' : 'نطاق شامل' }}
                  </v-chip>
                </template>

                <!-- Exam Details -->
                <template v-else-if="key === 'exam_details'">
                  <div class="text-caption font-weight-bold text-slate-700">
                    <span>{{ item.versions_count || 4 }} نماذج</span>
                    <span class="mx-1 text-slate-300">•</span>
                    <span>{{ item.questions_count || 40 }} سؤالاً</span>
                  </div>
                </template>

                <!-- Distribution Status -->
                <template v-else-if="key === 'distribution_status'">
                  <template v-if="getExamActiveDistribution(item)">
                    <v-chip size="x-small" color="amber-darken-4" variant="flat" class="text-white font-weight-bold">
                      <v-icon start size="12">mdi-clock-alert-outline</v-icon>
                      قيد التوزيع ({{ getExamActiveDistribution(item).status_display }})
                    </v-chip>
                  </template>
                  <template v-else>
                    <v-chip size="x-small" color="success" variant="tonal" class="font-weight-bold">
                      <v-icon start size="12">mdi-check-circle-outline</v-icon>
                      جاهز للجدولة
                    </v-chip>
                  </template>
                </template>
              </template>
            </custom-data-table>
          </v-card>

          <!-- Selected Exam Confirmation Bar & Action ("وعند تختار اختبار يظهر لك التالي") -->
          <v-card
            v-if="selectedExam && !getExamActiveDistribution(selectedExam)"
            class="pa-4 rounded-2xl border border-primary bg-blue-lighten-5 mb-4 shadow-xs"
            elevation="0"
          >
            <div class="d-flex align-center justify-space-between flex-wrap gap-4">
              <div class="d-flex align-center gap-3">
                <v-avatar color="primary" size="46" class="text-white shadow-xs">
                  <v-icon size="24">mdi-check-decagram</v-icon>
                </v-avatar>
                <div>
                  <div class="text-caption text-primary font-weight-bold">تم تحديد الاختبار المعتمد بنجاح:</div>
                  <div class="text-subtitle-1 font-weight-black text-slate-900">{{ selectedExam.title }}</div>
                  <div class="text-caption text-slate-600 d-flex align-center gap-2 mt-1 flex-wrap">
                    <span>الرمز: <strong>{{ selectedExam.uniqueCode || selectedExam.unique_code }}</strong></span>
                    <span>•</span>
                    <span>المادة: <strong>{{ selectedExam.subject_name || 'عام' }}</strong></span>
                    <span>•</span>
                    <span>العام الدراسي: <strong>{{ selectedExam.year_name || '2025/2026' }}</strong></span>
                    <span>•</span>
                    <span>النطاق: <strong>{{ getPreDeterminedScopeTitle(selectedExam) }}</strong></span>
                  </div>
                </div>
              </div>

              <div>
                <custom-btn
                  type="next"
                  label="التالي: نطاق المؤسسات المستهدفة"
                  color="primary"
                  class="px-8 font-weight-bold text-white shadow-xs"
                  :click="() => (currentStep = 2)"
                />
              </div>
            </div>
          </v-card>

          <!-- Active Distribution Warning Alert -->
          <v-alert
            v-if="selectedExam && getExamActiveDistribution(selectedExam)"
            type="warning"
            variant="tonal"
            class="rounded-2xl font-weight-bold mt-4 mb-4 border-amber"
          >
            <div class="d-flex align-center justify-space-between flex-wrap gap-2">
              <div class="d-flex align-center gap-3">
                <v-avatar color="amber-darken-3" size="40" class="text-white">
                  <v-icon size="22">mdi-alert-octagon-outline</v-icon>
                </v-avatar>
                <div>
                  <div class="text-subtitle-2 font-weight-black text-amber-darken-4">
                    لا يمكن إعادة تصدير هذا الاختبار؛ توجد مهمة توزيع نشطة قائمة بالفعل (#{{ getExamActiveDistribution(selectedExam).id }}: {{ getExamActiveDistribution(selectedExam).title }})
                  </div>
                  <div class="text-caption text-slate-700 mt-1">
                    حالة المهمة الحالية: <strong>{{ getExamActiveDistribution(selectedExam).status_display }}</strong>. لمنع ازدواجية سحب الحزم وتضارب طباعة أوراق OMR في المدارس، لا يمكن إنشاء مهمة ثانية حتى تكتمل المهمة السابقة أو يتم إلغاؤها أولاً.
                  </div>
                </div>
              </div>
              <div class="d-flex align-center gap-2">
                <v-btn
                  size="small"
                  color="amber-darken-4"
                  variant="flat"
                  class="font-weight-bold text-white rounded-lg px-4"
                  prepend-icon="mdi-monitor-dashboard"
                  @click="openLiveMonitorFromActiveDist(getExamActiveDistribution(selectedExam))"
                >
                  فتح شاشة المتابعة الحية
                </v-btn>
              </div>
            </div>
          </v-alert>

          <div v-if="!selectedExam" class="d-flex justify-end mt-4">
            <v-chip color="slate-400" variant="tonal" class="font-weight-bold">
              <v-icon start size="16">mdi-information-outline</v-icon>
              يرجى تحديد أحد الاختبارات أعلاه للمتابعة إلى الخطوة التالية
            </v-chip>
          </div>
        </div>

        <!-- STEP 2: TARGETING HIERARCHY (DIRECTLY PRE-DETERMINED FROM EXAM) -->
        <div v-else-if="currentStep === 2">
          <!-- Resolved Schools Header & Filters -->
          <div class="mb-4">
            <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
              <div class="d-flex align-center gap-2">
                <span class="text-subtitle-2 font-weight-bold text-slate-800">
                  {{ isSchoolTarget ? 'قائمة المدارس المستهدفة فعلياً:' : 'قائمة المعاهد / الجامعات المستهدفة فعلياً:' }}
                </span>
                <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                  {{ totalResolvedSchoolsCount }} {{ isSchoolTarget ? 'مدرسة' : 'مؤسسة / فرع' }}
                </v-chip>
              </div>

              <div v-if="step2FilterGovernorate || step2FilterDirectorate" class="d-flex align-center">
                <v-btn
                  size="small"
                  variant="text"
                  color="error"
                  density="compact"
                  class="font-weight-bold"
                  @click="resetStep2Filters"
                >
                  <v-icon start size="16">mdi-filter-remove-outline</v-icon>
                  إعادة ضبط الفلاتر
                </v-btn>
              </div>
            </div>

            <!-- Inline Filters Bar -->
            <v-card class="pa-3 rounded-xl border bg-slate-50 mb-3" elevation="0">
              <v-row dense class="align-center">
                <!-- Filter by Governorate -->
                <v-col cols="12" :md="isSchoolTarget ? 6 : 12">
                  <v-autocomplete
                    v-model="step2FilterGovernorate"
                    :items="governoratesList"
                    item-title="name"
                    item-value="id"
                    label="المحافظة"
                    placeholder="كل المحافظات"
                    variant="outlined"
                    density="compact"
                    prepend-inner-icon="mdi-map-marker-outline"
                    clearable
                    hide-details
                    bg-color="white"
                    :loading="loadingGeoData"
                    @update:model-value="onStep2GovernorateChanged"
                  />
                </v-col>

                <!-- Filter by Directorate (Only shown if isSchoolTarget is true) -->
                <v-col v-if="isSchoolTarget" cols="12" md="6">
                  <v-autocomplete
                    v-model="step2FilterDirectorate"
                    :items="directoratesList"
                    item-title="name"
                    item-value="id"
                    label="المديرية"
                    placeholder="كل المديريات"
                    variant="outlined"
                    density="compact"
                    prepend-inner-icon="mdi-domain"
                    clearable
                    hide-details
                    bg-color="white"
                    :loading="loadingGeoData"
                    @update:model-value="onStep2DirectorateChanged"
                  />
                </v-col>
              </v-row>
            </v-card>
          </div>

          <!-- Targeted Schools Table using custom-data-table Component -->
          <v-card class="main-card rounded-2xl overflow-hidden mb-6 border-subtle" elevation="0">
            <custom-data-table
              :headers="schoolTableHeaders"
              :items="resolvedSchoolsTableItems"
              :getData="getResolvedSchoolsData"
              :customLoading="loadingSchools"
              class="bg-transparent"
              :hasFilter="false"
              :log="false"
              :restore="false"
              :showSelect="false"
              :editItem="false"
            >
              <template v-slot:item-slot="{ item, key, index }">
                <!-- Index -->
                <template v-if="key === 'index'">
                  <div class="text-center text-caption font-weight-bold text-medium-emphasis">
                    {{ (resolvedSchoolsPagination.current_page - 1) * resolvedSchoolsPagination.page_size + index + 1 }}
                  </div>
                </template>

                <!-- School / Institution Name -->
                <template v-else-if="key === 'name_ar'">
                  <div class="font-weight-bold text-slate-800 d-flex align-center gap-2 py-1">
                    <v-avatar size="28" color="primary" variant="tonal" class="rounded-lg">
                      <v-icon size="16">mdi-school</v-icon>
                    </v-avatar>
                    <span>{{ item.name_ar }}</span>
                  </div>
                </template>

                <!-- Branch No -->
                <template v-else-if="key === 'branch_no'">
                  <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold font-mono">
                    {{ item.branch_no }}
                  </v-chip>
                </template>

                <!-- Governorate -->
                <template v-else-if="key === 'governorate'">
                  <span class="text-body-2 text-slate-700">{{ item.governorate }}</span>
                </template>

                <!-- Directorate -->
                <template v-else-if="key === 'directorate'">
                  <span class="text-body-2 text-slate-600">{{ item.directorate }}</span>
                </template>

                <!-- Status -->
                <template v-else-if="key === 'status'">
                  <v-chip size="x-small" color="success" variant="tonal" class="font-weight-bold">
                    <v-icon start size="12">mdi-check-decagram</v-icon>
                    جاهزة للاستلام
                  </v-chip>
                </template>
              </template>
            </custom-data-table>
          </v-card>

          <div class="d-flex justify-space-between mt-6">
            <custom-btn
              type="prev"
              label="السابق"
              variant="outlined"
              class="px-6 font-weight-bold"
              :click="() => (currentStep = 1)"
            />
            <custom-btn
              type="next"
              label="التالي: جدول المواعيد والأمان"
              color="primary"
              class="px-8 font-weight-bold text-white shadow-xs"
              :disabled="totalResolvedSchoolsCount === 0"
              :click="() => (currentStep = 3)"
            />
          </div>
        </div>

        <!-- STEP 3: TIMING & SECURITY -->
        <div v-else-if="currentStep === 3">
          <!-- Executive Context Recap Card -->
          <v-card class="pa-4 rounded-2xl border bg-slate-50 mb-6 shadow-xs" elevation="0">
            <v-row dense class="align-center">
              <v-col cols="12" md="7">
                <div class="d-flex align-center gap-3">
                  <v-avatar color="primary" variant="tonal" size="46" class="rounded-xl">
                    <v-icon size="24">mdi-file-document-check</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-caption text-medium-emphasis font-weight-bold">الاختبار المعتمد المجدول للتصدير:</div>
                    <div class="text-subtitle-1 font-weight-black text-slate-900">{{ selectedExam?.title || '-' }}</div>
                    <div class="text-caption text-slate-600 mt-1 d-flex align-center gap-2 flex-wrap">
                      <span>الرمز: <strong>{{ selectedExam?.uniqueCode || selectedExam?.unique_code }}</strong></span>
                      <span>•</span>
                      <span>المادة: <strong>{{ selectedExam?.subject_name || 'عام' }}</strong></span>
                      <span>•</span>
                      <span>العام الدراسي: <strong>{{ selectedExam?.year_name || '2025/2026' }}</strong></span>
                    </div>
                  </div>
                </div>
              </v-col>
              <v-col cols="12" md="5" class="d-flex justify-md-end align-center gap-3 mt-3 mt-md-0 flex-wrap">
                <div class="pa-2 px-4 rounded-xl bg-white border text-center flex-grow-1 flex-md-grow-0">
                  <div class="text-caption text-medium-emphasis font-weight-bold">نطاق الاستهداف</div>
                  <div class="text-subtitle-2 font-weight-black text-slate-800">{{ getPreDeterminedScopeTitle(selectedExam) }}</div>
                </div>
                <div class="pa-2 px-4 rounded-xl bg-white border text-center flex-grow-1 flex-md-grow-0">
                  <div class="text-caption text-medium-emphasis font-weight-bold">المؤسسات المحصورة</div>
                  <div class="text-subtitle-2 font-weight-black text-primary">{{ totalResolvedSchoolsCount }} مؤسسة جاهزة</div>
                </div>
              </v-col>
            </v-row>
          </v-card>

          <!-- Mission Title Input -->
          <div class="mb-5">
            <label class="text-caption font-weight-bold text-slate-700 d-block mb-1">
              مسمى مهمة التصدير والجدولة:
            </label>
            <v-text-field
              v-model="dispatchForm.title"
              variant="outlined"
              density="compact"
              placeholder="مثال: تصدير الاختبار النصفي الموحد - الرياضيات"
              prepend-inner-icon="mdi-format-title"
              hide-details
            />
          </div>

          <v-row>
            <!-- Timing Milestones Card -->
            <v-col cols="12" md="6">
              <v-card class="main-card pa-5 rounded-2xl border-subtle mb-4 h-100" elevation="0">
                <div class="d-flex align-center justify-space-between mb-4 flex-wrap gap-2">
                  <div class="text-subtitle-2 font-weight-bold text-indigo d-flex align-center gap-2">
                    <v-icon size="20">mdi-clock-outline</v-icon>
                    <span>المحطات والمواعيد الزمنية الرسمية</span>
                  </div>
                </div>

                <!-- Quick Timing Presets -->
                <div class="pa-3 rounded-xl bg-slate-50 border mb-4">
                  <div class="text-caption font-weight-bold text-slate-700 mb-2 d-flex align-center gap-1">
                    <v-icon size="14" color="primary">mdi-lightning-bolt</v-icon>
                    <span>اختصارات التوقيت القياسية:</span>
                  </div>
                  <div class="d-flex align-center gap-2 flex-wrap">
                    <v-btn size="x-small" variant="flat" color="primary" class="font-weight-bold rounded-lg" @click="applyTimingPreset('tomorrow_morning')">
                      <v-icon start size="14">mdi-weather-sunset-up</v-icon> صباح الغد (08:00 ص)
                    </v-btn>
                    <v-btn size="x-small" variant="tonal" color="teal" class="font-weight-bold rounded-lg" @click="applyTimingPreset('2hours')">
                      <v-icon start size="14">mdi-timer-outline</v-icon> بعد ساعتين
                    </v-btn>
                    <v-btn size="x-small" variant="tonal" color="indigo" class="font-weight-bold rounded-lg" @click="applyTimingPreset('now')">
                      <v-icon start size="14">mdi-play-circle-outline</v-icon> الآن (تجربة فورية)
                    </v-btn>
                  </div>
                </div>

                <!-- Milestone 1: Dispatch Time -->
                <div class="mb-4 pa-3 rounded-xl border bg-white">
                  <div class="d-flex align-center gap-2 mb-1">
                    <v-avatar size="22" color="indigo" class="text-white text-caption font-weight-bold">1</v-avatar>
                    <label class="text-caption font-weight-bold text-slate-800">
                      موعد إرسال الحزمة المشفرة للمؤسسات (Dispatch Time):
                    </label>
                  </div>
                  <v-text-field
                    v-model="dispatchForm.dispatch_at"
                    type="datetime-local"
                    density="compact"
                    variant="outlined"
                    prepend-inner-icon="mdi-cloud-upload-outline"
                    hide-details
                    class="mb-1"
                  />
                  <div class="text-caption text-medium-emphasis">تصل الحزمة مؤمنة ومشفرة لمخدم المدرسة وتُحفظ دون فتح.</div>
                </div>

                <!-- Milestone 2: Accessible Time -->
                <div class="mb-4 pa-3 rounded-xl border bg-white">
                  <div class="d-flex align-center gap-2 mb-1">
                    <v-avatar size="22" color="amber-darken-3" class="text-white text-caption font-weight-bold">2</v-avatar>
                    <label class="text-caption font-weight-bold text-amber-darken-4">
                      موعد فك الحجب والإتاحة للطباعة (Accessible Time):
                    </label>
                  </div>
                  <v-text-field
                    v-model="dispatchForm.accessible_from"
                    type="datetime-local"
                    density="compact"
                    variant="outlined"
                    prepend-inner-icon="mdi-printer-eye"
                    hide-details
                    class="mb-1"
                  />
                  <div class="text-caption text-medium-emphasis">يُفتح التشفير تلقائياً لكادر الكنترول بالمدرسة لبدء طباعة الكراسات وأوراق OMR.</div>
                </div>

                <!-- Milestone 3: Exam Duration -->
                <div class="pa-3 rounded-xl border bg-white">
                  <div class="d-flex align-center gap-2 mb-1">
                    <v-avatar size="22" color="teal" class="text-white text-caption font-weight-bold">3</v-avatar>
                    <label class="text-caption font-weight-bold text-teal-darken-3">
                      فترة انعقاد الامتحان الفعلي (Exam Session):
                    </label>
                  </div>
                  <v-row dense>
                    <v-col cols="6">
                      <v-text-field
                        v-model="dispatchForm.exam_start_at"
                        type="datetime-local"
                        density="compact"
                        variant="outlined"
                        prepend-inner-icon="mdi-play-outline"
                        label="بدء الامتحان"
                        hide-details
                      />
                    </v-col>
                    <v-col cols="6">
                      <v-text-field
                        v-model="dispatchForm.exam_end_at"
                        type="datetime-local"
                        density="compact"
                        variant="outlined"
                        prepend-inner-icon="mdi-stop-outline"
                        label="انتهاء الامتحان"
                        hide-details
                      />
                    </v-col>
                  </v-row>
                  <div class="text-caption text-medium-emphasis mt-1">وقت دخول الطلاب القاعات ووقت جمع الأوراق وسحب الإجابات.</div>
                </div>
              </v-card>
            </v-col>

            <!-- Security & Execution Policies Card -->
            <v-col cols="12" md="6">
              <v-card class="main-card pa-5 rounded-2xl border-subtle mb-4 h-100" elevation="0">
                <div class="text-subtitle-2 font-weight-bold text-teal d-flex align-center gap-2 mb-4">
                  <v-icon size="20">mdi-shield-lock-outline</v-icon>
                  <span>سياسات الأمان والسرية وطريقة التسليم</span>
                </div>

                <div class="pa-3 rounded-xl border bg-white mb-3">
                  <v-switch
                    v-model="dispatchForm.is_encrypted"
                    color="primary"
                    label="تشفير محتوى الحزمة والأسئلة (AES-256 GCM)"
                    hide-details
                    density="compact"
                  />
                  <div class="text-caption text-medium-emphasis ms-8">
                    يضمن عدم إمكانية استعراض أو تسريب نماذج الأسئلة قبل حلول موعد الإتاحة المحدد رسمياً.
                  </div>
                </div>

                <div class="pa-3 rounded-xl border bg-white mb-3">
                  <v-switch
                    v-model="dispatchForm.auto_unlock"
                    color="teal"
                    label="فك التشفير التلقائي فور حلول موعد الإتاحة"
                    hide-details
                    density="compact"
                  />
                  <div class="text-caption text-medium-emphasis ms-8">
                    توليد وتوفير مفتاح فك التشفير ذاتياً لنظام المدرسة عند الوقت المحدد دون تدخل يدوي.
                  </div>
                </div>

                <div class="pa-3 rounded-xl bg-slate-50 border mb-4">
                  <div class="text-caption font-weight-bold text-slate-800 mb-1 d-flex align-center gap-1">
                    <v-icon size="16" color="teal">mdi-check-circle</v-icon>
                    <span>نمط تنفيذ الاختبار المعتمد:</span>
                  </div>
                  <div class="text-body-2 text-slate-700 font-weight-bold">
                    طباعة كراسات الأسئلة بنماذجها المتعددة (A, B, C, D) + أوراق إجابة OMR مخصصة للطلاب.
                  </div>
                </div>

                <div>
                  <label class="text-caption font-weight-bold text-slate-700 d-block mb-1">
                    توجيهات وملاحظات للكنترول المدرسي (اختياري):
                  </label>
                  <v-textarea
                    v-model="dispatchForm.notes"
                    variant="outlined"
                    density="compact"
                    rows="3"
                    class="rounded-lg"
                    placeholder="اكتب أي تعليمات خاصة بتسليم النماذج أو لجان الامتحان..."
                    hide-details
                  />
                </div>
              </v-card>
            </v-col>
          </v-row>

          <!-- Final Confirmation Strip -->
          <v-card class="pa-4 rounded-2xl border bg-slate-50 mt-4 shadow-xs" elevation="0">
            <div class="d-flex align-center justify-space-between flex-wrap gap-4">
              <div class="d-flex align-center gap-3">
                <v-avatar color="success" size="44" class="text-white shadow-xs">
                  <v-icon size="24">mdi-shield-check</v-icon>
                </v-avatar>
                <div>
                  <div class="text-subtitle-2 font-weight-black text-slate-900">جاهز لاعتماد وجدولة مهمة التوزيع</div>
                  <div class="text-caption text-slate-600 mt-1 d-flex align-center gap-2 flex-wrap">
                    <span>المؤسسات المستهدفة: <strong>{{ totalResolvedSchoolsCount }} مؤسسة</strong></span>
                    <span>•</span>
                    <span>موعد الطباعة: <strong>{{ formatDateTime(dispatchForm.accessible_from) }}</strong></span>
                    <span>•</span>
                    <span>بدء الامتحان: <strong>{{ formatDateTime(dispatchForm.exam_start_at) }}</strong></span>
                    <span>•</span>
                    <span>التشفير: <strong>{{ dispatchForm.is_encrypted ? 'مشفر بالكامل' : 'غير مشفر' }}</strong></span>
                  </div>
                </div>
              </div>

              <div class="d-flex align-center gap-3">
                <custom-btn
                  type="prev"
                  label="السابق"
                  variant="outlined"
                  class="px-6 font-weight-bold"
                  :click="() => (currentStep = 2)"
                />
                <custom-btn
                  type="save"
                  label="تأكيد وجدولة التصدير الآن"
                  color="success"
                  class="px-8 font-weight-bold text-white shadow-xs"
                  :loading="saving"
                  :click="submitDispatch"
                />
              </div>
            </div>
          </v-card>
        </div>
      </v-card>
    </div>

    <!-- LIVE MONITOR DIALOG using system CustomDialog -->
    <custom-dialog
      v-model="showLiveMonitorDialog"
      width="1050"
      height="auto"
      title="المتابعة الميدانية الحية للاستلام والطباعة"
      :subTitle="selectedMonitorDistribution ? `${selectedMonitorDistribution.title} | رمز الاختبار: ${selectedMonitorDistribution.exam_unique_code}` : ''"
    >
      <div v-if="selectedMonitorDistribution" class="pa-2">
        <!-- Live KPI Counters Cards (5 Cards) -->
        <v-row class="mb-4" v-if="liveMonitorData" dense>
          <v-col cols="6" sm="4" md="2">
            <v-card class="main-card pa-3 rounded-xl border-subtle text-center h-100" elevation="0">
              <div class="text-h5 font-weight-black text-indigo">{{ liveMonitorData.kpis.total_schools }}</div>
              <div class="text-caption text-medium-emphasis font-weight-bold">إجمالي المدارس</div>
            </v-card>
          </v-col>
          <v-col cols="6" sm="4" md="3">
            <v-card class="main-card pa-3 rounded-xl border-subtle text-center bg-emerald-lighten-5 h-100" elevation="0">
              <div class="text-h5 font-weight-black text-emerald">{{ liveMonitorData.kpis.received_schools }}</div>
              <div class="text-caption text-emerald-darken-2 font-weight-bold">استلمت الحزمة ({{ liveMonitorData.kpis.received_percentage }}%)</div>
            </v-card>
          </v-col>
          <v-col cols="6" sm="4" md="2">
            <v-card class="main-card pa-3 rounded-xl border-subtle text-center bg-amber-lighten-5 h-100" elevation="0">
              <div class="text-h5 font-weight-black text-amber-darken-3">{{ liveMonitorData.kpis.accessible_schools }}</div>
              <div class="text-caption text-amber-darken-3 font-weight-bold">أتيحت للطباعة</div>
            </v-card>
          </v-col>
          <v-col cols="6" sm="6" md="3">
            <v-card class="main-card pa-3 rounded-xl border-subtle text-center bg-teal-lighten-5 h-100" elevation="0">
              <div class="text-h5 font-weight-black text-teal-darken-3">{{ liveMonitorData.kpis.total_printed_sheets }}</div>
              <div class="text-caption text-teal-darken-3 font-weight-bold">أوراق OMR مطبوعة</div>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6" md="2">
            <v-card class="main-card pa-3 rounded-xl border-subtle text-center bg-purple-lighten-5 h-100" elevation="0">
              <div class="text-h5 font-weight-black text-purple">{{ liveMonitorData.kpis.total_attended_students || 0 }}</div>
              <div class="text-caption text-purple-darken-2 font-weight-bold">الطلاب الحاضرين</div>
            </v-card>
          </v-col>
        </v-row>

        <!-- Live Monitor Toolbar Strip: Search, Filter, Simulator Toggle & Export CSV -->
        <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3 pa-2 rounded-xl bg-slate-50 border">
          <div class="d-flex align-center gap-2 flex-grow-1" style="max-width: 320px;">
            <v-text-field
              v-model="liveMonitorSearchQuery"
              density="compact"
              variant="outlined"
              placeholder="بحث بالمدرسة أو كود الفرع..."
              prepend-inner-icon="mdi-magnify"
              hide-details
              clearable
            />
          </div>

          <div class="d-flex align-center gap-2 flex-wrap">
            <v-btn-toggle
              v-model="liveMonitorFilterStatus"
              mandatory
              density="compact"
              color="primary"
              variant="outlined"
              rounded="lg"
            >
              <v-btn value="all" size="small">الكل</v-btn>
              <v-btn value="received" size="small">المستلمة فقط</v-btn>
              <v-btn value="pending" size="small">بانتظار السحب</v-btn>
            </v-btn-toggle>

            <v-btn
              size="small"
              :variant="showSimulatorPanel ? 'flat' : 'tonal'"
              color="indigo"
              class="font-weight-bold rounded-lg"
              prepend-icon="mdi-flask-outline"
              @click="showSimulatorPanel = !showSimulatorPanel"
            >
              {{ showSimulatorPanel ? 'إخفاء المحاكي' : 'محاكي تفاعل المدارس' }}
            </v-btn>

            <v-btn
              size="small"
              variant="tonal"
              color="teal"
              class="font-weight-bold rounded-lg"
              prepend-icon="mdi-file-delimited-outline"
              @click="exportLiveMonitorCsv"
            >
              تصدير CSV
            </v-btn>
          </div>
        </div>

        <!-- School Interaction Simulator Card (Collapsible) -->
        <v-expand-transition>
          <div v-if="showSimulatorPanel" class="pa-4 rounded-xl border border-indigo bg-indigo-lighten-5 mb-4">
            <div class="d-flex align-center justify-space-between mb-3">
              <div class="d-flex align-center gap-2 text-indigo font-weight-bold">
                <v-icon>mdi-laptop-account</v-icon>
                <span>محاكي استجابة نظام المدرسة (SMS Client Simulator)</span>
              </div>
              <v-chip size="x-small" color="indigo" variant="flat" class="font-weight-bold text-white">
                أداة فحص واختبار التفاعل الميداني
              </v-chip>
            </div>

            <v-row dense class="align-center">
              <v-col cols="12" md="4">
                <v-select
                  v-model="simulatorForm.school_id"
                  :items="liveMonitorData?.schools || []"
                  item-title="school_name_ar"
                  item-value="school"
                  placeholder="اختر المدرسة لمحاكاتها"
                  variant="outlined"
                  density="compact"
                  hide-details
                  class="bg-white rounded-lg"
                />
              </v-col>
              <v-col cols="12" sm="4" md="2">
                <v-text-field
                  v-model.number="simulatorForm.printed_booklets"
                  label="كراسات الأسئلة"
                  type="number"
                  variant="outlined"
                  density="compact"
                  hide-details
                  class="bg-white rounded-lg"
                />
              </v-col>
              <v-col cols="12" sm="4" md="2">
                <v-text-field
                  v-model.number="simulatorForm.printed_sheets"
                  label="أوراق OMR"
                  type="number"
                  variant="outlined"
                  density="compact"
                  hide-details
                  class="bg-white rounded-lg"
                />
              </v-col>
              <v-col cols="12" sm="4" md="2">
                <v-text-field
                  v-model.number="simulatorForm.attended_students"
                  label="الطلاب الحاضرين"
                  type="number"
                  variant="outlined"
                  density="compact"
                  hide-details
                  class="bg-white rounded-lg"
                />
              </v-col>
              <v-col cols="12" md="2" class="d-flex justify-end">
                <custom-btn
                  type="save"
                  label="تنفيذ المحاكاة"
                  color="indigo"
                  class="font-weight-bold w-100"
                  :loading="simulating"
                  :disabled="!simulatorForm.school_id"
                  :click="runSimulator"
                />
              </v-col>
            </v-row>

            <!-- Simulator Execution Feedback Alert -->
            <v-alert
              v-if="simulatorResult"
              type="success"
              variant="tonal"
              class="mt-4 rounded-xl font-weight-bold"
              closable
              @click:close="simulatorResult = null"
            >
              <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-2">
                <div class="d-flex align-center gap-2">
                  <v-icon color="success" size="24">mdi-check-decagram</v-icon>
                  <span class="text-subtitle-1 font-weight-black text-success">{{ simulatorResult.message }}</span>
                </div>
                <v-chip color="teal" size="small" variant="flat" class="font-weight-bold text-white">
                  فرع: {{ simulatorResult.school_status?.school_branch_no }}
                </v-chip>
              </div>

              <div class="text-body-2 text-slate-700 mb-3">
                قام المحاكي بتمثيل استجابة نظام المدرسة (SMS) بنجاح وإرسال إشعار استلام وتأكيد الطباعة إلى بنك الأسئلة المركزي، وتم تنفيذ وتحديث ما يلي:
              </div>

              <!-- Quick Stats Grid -->
              <v-row dense class="mb-2">
                <v-col cols="6" sm="3">
                  <div class="pa-2 rounded-lg bg-white border text-center">
                    <div class="text-caption text-medium-emphasis">حالة السحب والاستلام</div>
                    <div class="text-subtitle-2 font-weight-bold text-emerald">
                      <v-icon size="14" color="emerald" class="me-1">mdi-cloud-download</v-icon>
                      تم الاستلام
                    </div>
                  </div>
                </v-col>
                <v-col cols="6" sm="3">
                  <div class="pa-2 rounded-lg bg-white border text-center">
                    <div class="text-caption text-medium-emphasis">كراسات الأسئلة</div>
                    <div class="text-subtitle-2 font-weight-bold text-teal">
                      <v-icon size="14" color="teal" class="me-1">mdi-book-open-page-variant</v-icon>
                      {{ simulatorResult.school_status?.printed_booklets_count || 0 }} كراسة
                    </div>
                  </div>
                </v-col>
                <v-col cols="6" sm="3">
                  <div class="pa-2 rounded-lg bg-white border text-center">
                    <div class="text-caption text-medium-emphasis">أوراق OMR المطبوعة</div>
                    <div class="text-subtitle-2 font-weight-bold text-indigo">
                      <v-icon size="14" color="indigo" class="me-1">mdi-card-text-outline</v-icon>
                      {{ simulatorResult.school_status?.printed_sheets_count || 0 }} ورقة
                    </div>
                  </div>
                </v-col>
                <v-col cols="6" sm="3">
                  <div class="pa-2 rounded-lg bg-white border text-center">
                    <div class="text-caption text-medium-emphasis">حضور الطلاب بالقاعات</div>
                    <div class="text-subtitle-2 font-weight-bold text-purple">
                      <v-icon size="14" color="purple" class="me-1">mdi-account-check</v-icon>
                      {{ simulatorResult.school_status?.students_attended_count || 0 }} طالب
                    </div>
                  </div>
                </v-col>
              </v-row>

              <div class="text-caption text-medium-emphasis">
                <v-icon size="14" class="me-1">mdi-information-outline</v-icon>
                تم تحديث عدادات المؤشرات الحية (KPIs) في الأعلى وسجل المدرسة في جدول المتابعة الميدانية بالأسفل تلقائياً.
              </div>
            </v-alert>
          </div>
        </v-expand-transition>

        <!-- Schools Live CustomDataTable -->
        <div class="main-card rounded-xl overflow-hidden border-subtle mt-2">
          <custom-data-table
            :headers="liveMonitorHeaders"
            :items="liveMonitorSchoolsTableItems"
            :hasFilter="false"
            :log="false"
            :restore="false"
            :showSelect="false"
            class="bg-transparent"
          >
            <template v-slot:item-slot="{ item, key }">
              <template v-if="key === 'school_name_ar'">
                <div class="font-weight-bold py-1">{{ item.school_name_ar }}</div>
              </template>
              <template v-else-if="key === 'school_branch_no'">
                <v-chip size="x-small" variant="tonal" color="primary" class="font-weight-bold font-mono">
                  {{ item.school_branch_no }}
                </v-chip>
              </template>
              <template v-else-if="key === 'governorate_name'">
                <span>{{ item.governorate_name }}</span>
              </template>
              <template v-else-if="key === 'is_received'">
                <v-chip size="x-small" :color="item.is_received ? 'emerald' : 'amber'" variant="tonal" class="font-weight-bold">
                  <v-icon size="10" start>{{ item.is_received ? 'mdi-check-circle' : 'mdi-clock-outline' }}</v-icon>
                  {{ item.is_received ? 'تم الاستلام' : 'بانتظار السحب' }}
                </v-chip>
              </template>
              <template v-else-if="key === 'received_at'">
                <span class="text-caption">{{ item.received_at ? formatDateTime(item.received_at) : '-' }}</span>
              </template>
              <template v-else-if="key === 'printed_booklets_count'">
                <v-chip size="x-small" color="teal" variant="tonal" class="font-weight-bold">
                  {{ item.printed_booklets_count || 0 }} كراسة
                </v-chip>
              </template>
              <template v-else-if="key === 'printed_sheets_count'">
                <v-chip size="x-small" color="indigo" variant="tonal" class="font-weight-bold">
                  {{ item.printed_sheets_count || 0 }} ورقة
                </v-chip>
              </template>
              <template v-else-if="key === 'students_attended_count'">
                <v-chip size="x-small" color="purple" variant="tonal" class="font-weight-bold">
                  {{ item.students_attended_count || 0 }} طالب
                </v-chip>
              </template>
              <template v-else-if="key === 'results_synced_back'">
                <v-icon :color="item.results_synced_back ? 'emerald' : 'slate-300'" size="18">
                  {{ item.results_synced_back ? 'mdi-check-decagram' : 'mdi-minus' }}
                </v-icon>
              </template>
            </template>
          </custom-data-table>
        </div>
      </div>

      <template #actions>
        <custom-btn
          type="refresh"
          label="تحديث الحالة"
          color="primary"
          variant="tonal"
          class="font-weight-bold"
          :click="refreshLiveMonitor"
        />
        <custom-btn
          type="cancel"
          label="إغلاق"
          variant="outlined"
          :click="() => (showLiveMonitorDialog = false)"
        />
      </template>
    </custom-dialog>

    <!-- PREVIEW API PACKAGE DIALOG using system CustomDialog -->
    <custom-dialog
      v-model="showPackagePreviewDialog"
      width="750"
      height="auto"
      title="معاينة حزمة التصدير (Export Payload Contract)"
      subTitle="بنية البيانات المصدرة للأنظمة الطرفية المدرسية والجامعية"
    >
      <div class="pa-2">
        <pre class="pa-4 rounded-xl bg-slate-900 text-emerald-accent-3 text-caption font-mono" style="max-height: 420px; overflow-y: auto;">
{{ packageJsonSnippet }}
        </pre>
      </div>
      <template #actions>
        <custom-btn
          v-if="selectedMonitorDistribution"
          type="add"
          label="تنزيل الملف (JSON)"
          icon="download"
          color="primary"
          variant="tonal"
          class="font-weight-bold"
          :click="() => downloadPackageFile(selectedMonitorDistribution)"
        />
        <custom-btn
          type="cancel"
          label="إغلاق"
          variant="outlined"
          :click="() => (showPackagePreviewDialog = false)"
        />
      </template>
    </custom-dialog>

    <!-- CONFIRM FORCE UNLOCK DIALOG -->
    <custom-dialog
      v-model="showForceUnlockDialog"
      width="550"
      height="auto"
      title="تأكيد فك الحجب الفوري (حالة طوارئ)"
      subTitle="إتاحة نص الأسئلة للطباعة في المدارس قبل الموعد المجدول"
    >
      <div class="pa-4">
        <v-alert type="warning" variant="tonal" class="rounded-xl font-weight-bold mb-4">
          <v-icon start>mdi-alert-circle-outline</v-icon>
          هل أنت متأكد من رغبتك في فك حجب أسئلة هذا الاختبار فوراً؟ سيتم تمكين لجان الكنترول بجميع المدارس المستهدفة من سحب الأسئلة والبدء في طباعتها في هذه اللحظة.
        </v-alert>
        <div v-if="distributionToUnlock" class="pa-3 bg-slate-50 rounded-xl border text-caption">
          <div><strong>المهمة:</strong> {{ distributionToUnlock.title }}</div>
          <div><strong>رمز الاختبار:</strong> {{ distributionToUnlock.exam_unique_code }}</div>
        </div>
      </div>
      <template #actions>
        <custom-btn
          type="save"
          label="تأكيد فك الحجب الآن"
          color="amber-darken-3"
          class="font-weight-bold text-white px-4"
          :loading="unlocking"
          :click="confirmForceUnlock"
        />
        <custom-btn
          type="cancel"
          label="إلغاء"
          variant="outlined"
          :click="() => (showForceUnlockDialog = false)"
        />
      </template>
    </custom-dialog>

    <!-- CONFIRM CANCEL DISTRIBUTION DIALOG -->
    <custom-dialog
      v-model="showCancelDialog"
      width="550"
      height="auto"
      title="تأكيد إلغاء مهمة التوزيع"
      subTitle="حجب الاختبار ومنع المدارس من استلام الحزمة"
    >
      <div class="pa-4">
        <v-alert type="error" variant="tonal" class="rounded-xl font-weight-bold mb-4">
          <v-icon start>mdi-alert-octagon-outline</v-icon>
          سيؤدي إلغاء مهمة التوزيع إلى حجب الأسئلة ومنع كافة الأنظمة المدرسية من سحبها أو استكمال الاختبار.
        </v-alert>
        <v-textarea
          v-model="cancelReason"
          label="سبب الإلغاء (اختياري)"
          placeholder="اكتب سبب إلغاء مهمة التوزيع..."
          variant="outlined"
          density="compact"
          rows="2"
          class="rounded-lg mb-2"
        />
      </div>
      <template #actions>
        <custom-btn
          type="del"
          label="تأكيد الإلغاء"
          color="error"
          class="font-weight-bold px-4"
          :loading="cancelling"
          :click="confirmCancelDispatch"
        />
        <custom-btn
          type="cancel"
          label="تراجع"
          variant="outlined"
          :click="() => (showCancelDialog = false)"
        />
      </template>
    </custom-dialog>

    <!-- Global Action Feedback Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="5000"
      location="top center"
      rounded="pill"
      class="font-weight-bold"
    >
      <div class="d-flex align-center gap-2">
        <v-icon :icon="snackbar.icon" />
        <span>{{ snackbar.text }}</span>
      </div>
      <template #actions>
        <v-btn icon="mdi-close" variant="text" size="small" @click="snackbar.show = false" />
      </template>
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { examsService } from '@/services/examsService'
import api from '@/services/api'

// State variables
const loading = ref(false)
const saving = ref(false)
const currentTab = ref('list') // 'list' | 'wizard'
const currentStep = ref(1)

// Filters State
const filterInstitutionType = ref(null)
const filterTargetLevel = ref(null)
const filterStatus = ref(null)

const institutionTypeFilterOptions = [
  { value: 'school', label: 'مدارس (التعليم العام)', icon: 'mdi-school-outline' },
  { value: 'university', label: 'جامعات (التعليم الجامعي)', icon: 'mdi-town-hall' },
  { value: 'institute', label: 'معاهد (التعليم المهني)', icon: 'mdi-tools' },
]

const targetLevelFilterOptions = [
  { value: 'ministry', label: 'الوزارة (شامل)' },
  { value: 'governorate', label: 'المحافظات' },
  { value: 'directorate', label: 'المديريات' },
  { value: 'school', label: 'مدارس محددة' },
]

const statusFilterOptions = [
  { value: 'scheduled', label: 'مجدول' },
  { value: 'dispatched', label: 'تم الإرسال' },
  { value: 'accessible', label: 'متاح للطباعة' },
  { value: 'in_progress', label: 'جاري الاختبار' },
  { value: 'completed', label: 'مكتمل' },
]

// Data
const distributionsList = ref([])
const availableExams = ref([])
const selectedExam = ref(null)
const filterExamInstitutionType = ref('school')
const examSearchQuery = ref('')

const filteredAvailableExams = computed(() => {
  let list = availableExams.value.filter(e => {
    const instType = e.institution_type || 'school'
    return instType === filterExamInstitutionType.value
  })
  if (examSearchQuery.value?.trim()) {
    const q = examSearchQuery.value.trim().toLowerCase()
    list = list.filter(e =>
      (e.title && e.title.toLowerCase().includes(q)) ||
      (e.unique_code && e.unique_code.toLowerCase().includes(q)) ||
      (e.uniqueCode && e.uniqueCode.toLowerCase().includes(q)) ||
      (e.subject_name && e.subject_name.toLowerCase().includes(q)) ||
      (e.year_name && e.year_name.toLowerCase().includes(q))
    )
  }
  return list
})

const institutionTypeFilterTabs = computed(() => [
  {
    value: 'school',
    label: 'المدارس',
    icon: 'mdi-school',
    count: availableExams.value.filter(e => (e.institution_type || 'school') === 'school').length
  },
  {
    value: 'university',
    label: 'الجامعات والكليات',
    icon: 'mdi-town-hall',
    count: availableExams.value.filter(e => e.institution_type === 'university').length
  },
  {
    value: 'institute',
    label: 'المعاهد والتدريب المهني',
    icon: 'mdi-tools',
    count: availableExams.value.filter(e => e.institution_type === 'institute').length
  }
])

const wizardExamsTableItems = computed(() => ({
  results: filteredAvailableExams.value,
  count: filteredAvailableExams.value.length,
  pagination: {
    count: filteredAvailableExams.value.length,
    current_page: 1,
    num_pages: 1,
  }
}))

async function getWizardExamsData() {
  return wizardExamsTableItems.value
}

const noop = async () => ({
  results: [],
  count: 0,
  pagination: { count: 0, current_page: 1, num_pages: 1 }
})

function canNavigateToStep(step) {
  if (step === 1) return true
  if (step === 2) return !!selectedExam.value && !getExamActiveDistribution(selectedExam.value)
  if (step === 3) return !!selectedExam.value && !getExamActiveDistribution(selectedExam.value) && totalResolvedSchoolsCount.value > 0
  return false
}

watch(filterExamInstitutionType, (newType) => {
  const matching = availableExams.value.filter(e => (e.institution_type || 'school') === newType)
  if (matching.length > 0) {
    const firstNonActive = matching.find(e => !getExamActiveDistribution(e)) || matching[0]
    if (!selectedExam.value || (selectedExam.value.institution_type || 'school') !== newType) {
      selectExam(firstNonActive)
    }
  } else {
    selectedExam.value = null
    dispatchForm.value.title = ''
  }
})

const selectedTargetLevel = ref('ministry')
const selectedOrgIds = ref([])
const resolvedSchools = ref([])
const totalResolvedSchoolsCount = ref(0)
const allResolvedSchoolIds = ref([])
const schoolSearchQuery = ref('')
const step2FilterGovernorate = ref(null)
const step2FilterDirectorate = ref(null)

const isSchoolTarget = computed(() => {
  const type = selectedExam.value?.institution_type || filterExamInstitutionType.value || 'school'
  return type === 'school'
})

const resolvedSchoolsPagination = ref({
  count: 0,
  current_page: 1,
  num_pages: 1,
  page_size: 10
})

const resolvedSchoolsTableItems = ref({
  results: [],
  count: 0,
  pagination: {
    count: 0,
    current_page: 1,
    num_pages: 1,
    page_size: 10
  }
})

let schoolSearchTimeout = null
function onSchoolSearchChanged() {
  if (schoolSearchTimeout) clearTimeout(schoolSearchTimeout)
  schoolSearchTimeout = setTimeout(() => {
    getResolvedSchoolsData({ page: 1 })
  }, 350)
}

function onClearSchoolSearch() {
  schoolSearchQuery.value = ''
  getResolvedSchoolsData({ page: 1 })
}

function onStep2GovernorateChanged(val) {
  step2FilterGovernorate.value = val
  step2FilterDirectorate.value = null
  getResolvedSchoolsData({ page: 1 })
}

function onStep2DirectorateChanged(val) {
  step2FilterDirectorate.value = val
  getResolvedSchoolsData({ page: 1 })
}

function resetStep2Filters() {
  step2FilterGovernorate.value = null
  step2FilterDirectorate.value = null
  schoolSearchQuery.value = ''
  getResolvedSchoolsData({ page: 1 })
}

async function getResolvedSchoolsData(tableParams = null) {
  loadingSchools.value = true
  try {
    let page = 1
    let pageSize = resolvedSchoolsPagination.value.page_size || 10

    if (tableParams) {
      const p = tableParams.params || tableParams
      if (p.page) page = Number(p.page)
      if (p.page_size) pageSize = Number(p.page_size)
      else if (p.limit) pageSize = Number(p.limit)
      else if (p.itemsPerPage) pageSize = Number(p.itemsPerPage)
    }

    const currentInstType = selectedExam.value?.institution_type || filterExamInstitutionType.value || 'school'
    const payload = {
      target_level: selectedTargetLevel.value || 'ministry',
      selected_org_ids: selectedOrgIds.value || [],
      institution_type: currentInstType,
      page,
      page_size: pageSize,
      limit: pageSize
    }

    if (selectedExam.value?.id) {
      payload.exam_id = selectedExam.value.id
    }

    if (schoolSearchQuery.value && schoolSearchQuery.value.trim()) {
      payload.search = schoolSearchQuery.value.trim()
    }

    if (step2FilterGovernorate.value) {
      payload.filter_governorate = step2FilterGovernorate.value
    }

    if (isSchoolTarget.value && step2FilterDirectorate.value) {
      payload.filter_directorate = step2FilterDirectorate.value
    }

    const res = await examsService.resolveDistributionHierarchy(payload)
    const results = res?.results || res?.schools || (Array.isArray(res) ? res : [])
    const count = res?.count ?? res?.total_schools ?? results.length
    const numPages = res?.num_pages ?? Math.max(1, Math.ceil(count / pageSize))
    const currentPage = res?.current_page ?? page

    resolvedSchools.value = results
    totalResolvedSchoolsCount.value = count

    if (res?.all_school_ids && Array.isArray(res.all_school_ids)) {
      allResolvedSchoolIds.value = res.all_school_ids
    } else if (results.length > 0) {
      allResolvedSchoolIds.value = results.map(s => s.id)
    }

    resolvedSchoolsPagination.value = {
      count,
      current_page: currentPage,
      num_pages: numPages,
      page_size: pageSize
    }

    resolvedSchoolsTableItems.value = {
      results,
      count,
      pagination: {
        count,
        current_page: currentPage,
        num_pages: numPages,
        page_size: pageSize
      }
    }

    return resolvedSchoolsTableItems.value
  } catch (e) {
    console.error('Error resolving hierarchy schools with backend pagination:', e)
    resolvedSchoolsTableItems.value = {
      results: [],
      count: 0,
      pagination: {
        count: 0,
        current_page: 1,
        num_pages: 1,
        page_size: 10
      }
    }
    return resolvedSchoolsTableItems.value
  } finally {
    loadingSchools.value = false
  }
}

const educationalOrgsList = ref([])

const governoratesList = computed(() => {
  return educationalOrgsList.value
    .filter(org => Number(org.company_level) === 30)
    .map(org => ({
      id: org.id,
      name: org.name_ar || org.name || org.name_en || '',
      name_ar: org.name_ar || org.name || '',
      name_en: org.name_en || '',
      branch_no: org.branch_no,
      company_level: org.company_level,
      fk_parent_organization: org.fk_parent_organization
    }))
})

const directoratesList = computed(() => {
  if (!step2FilterGovernorate.value) {
    return educationalOrgsList.value
      .filter(org => Number(org.company_level) === 40)
      .map(org => ({
        id: org.id,
        name: org.name_ar || org.name || org.name_en || '',
        name_ar: org.name_ar || org.name || '',
        name_en: org.name_en || '',
        branch_no: org.branch_no,
        company_level: org.company_level,
        fk_parent_organization: org.fk_parent_organization
      }))
  }
  return educationalOrgsList.value
    .filter(org => {
      if (Number(org.company_level) !== 40) return false
      const parentId = typeof org.fk_parent_organization === 'object' && org.fk_parent_organization !== null
        ? org.fk_parent_organization.id
        : org.fk_parent_organization
      return Number(parentId) === Number(step2FilterGovernorate.value)
    })
    .map(org => ({
      id: org.id,
      name: org.name_ar || org.name || org.name_en || '',
      name_ar: org.name_ar || org.name || '',
      name_en: org.name_en || '',
      branch_no: org.branch_no,
      company_level: org.company_level,
      fk_parent_organization: org.fk_parent_organization
    }))
})

const allSchoolsList = ref([])
const loadingGeoData = ref(false)
const loadingDirectorates = ref(false)
const loadingSchools = ref(false)
// Wizard Form
const dispatchForm = ref({
  title: '',
  dispatch_at: '',
  accessible_from: '',
  exam_start_at: '',
  exam_end_at: '',
  is_encrypted: true,
  auto_unlock: true,
  delivery_mode: 'printed_omr',
  notes: '',
})

// Dialogs
const showLiveMonitorDialog = ref(false)
const selectedMonitorDistribution = ref(null)
const liveMonitorData = ref(null)

const showPackagePreviewDialog = ref(false)
const packageJsonSnippet = ref('')

const stepTitles = [
  'اختيار الاختبار المعتمد',
  'نطاق المؤسسات المستهدفة',
  'جدول المواعيد والأمان',
]

function getPreDeterminedScopeTitle(exam) {
  if (!exam) return '-'
  if (exam.target_scope_level === 'governorate') return 'محافظات محددة'
  if (exam.target_scope_level === 'directorate') return 'إدارات مديريات محددة'
  if (exam.target_scope_level === 'school') return 'مؤسسات / مدارس محددة'
  if (exam.governorate_name) return `محافظة ${exam.governorate_name}`
  return 'نطاق شامل (كافة مدارس ومؤسسات الجمهورية)'
}

function getPreDeterminedScopeTargets(exam) {
  if (!exam) return []
  if (exam.target_scopes_data && exam.target_scopes_data.length > 0) {
    return exam.target_scopes_data.map(s => s.target_name || s.name_ar || s.scope_level_display).filter(Boolean)
  }
  if (exam.governorate_name) return [exam.governorate_name]
  if (exam.directorate_name) return [exam.directorate_name]
  return []
}

function getExamActiveDistribution(exam) {
  if (!exam) return null
  const activeStatuses = ['scheduled', 'dispatched', 'accessible', 'in_progress']
  if (exam.active_distribution && activeStatuses.includes(exam.active_distribution.status)) {
    return exam.active_distribution
  }
  const found = distributionsList.value.find(d => 
    (d.exam === exam.id || d.exam_id === exam.id) && activeStatuses.includes(d.status)
  )
  if (found) {
    return {
      id: found.id,
      title: found.title,
      status: found.status,
      status_display: getStatusLabel(found.status)
    }
  }
  return null
}

function openLiveMonitorFromActiveDist(activeDist) {
  if (!activeDist) return
  const targetDist = distributionsList.value.find(d => d.id === activeDist.id) || {
    id: activeDist.id,
    title: activeDist.title,
    status: activeDist.status,
    exam_unique_code: selectedExam.value?.uniqueCode || selectedExam.value?.unique_code
  }
  openLiveMonitor(targetDist)
}

// Main Table Headers for custom-data-table
const tableHeaders = [
  { title: 'مهمة التوزيع والاختبار', key: 'title', sortable: true },
  { title: 'نوع المؤسسة', key: 'institution_type', sortable: true },
  { title: 'المستوى المستهدف', key: 'target_level', sortable: true },
  { title: 'تقدم استلام المؤسسات', key: 'targeted_schools_count', sortable: true },
  { title: 'نافذة الإتاحة والامتحان', key: 'accessible_from', sortable: true },
  { title: 'نمط التسليم', key: 'delivery_mode', sortable: false },
  { title: 'الحالة', key: 'status', sortable: true },
]

// Wizard Step 1: Exams Table Headers
const wizardExamHeaders = [
  { title: 'تحديد', key: 'select', sortable: false, width: '90px', align: 'center' },
  { title: 'رمز الاختبار', key: 'unique_code', sortable: true, width: '130px' },
  { title: 'عنوان الاختبار المعتمد', key: 'title', sortable: true },
  { title: 'نوع المؤسسة', key: 'institution_type', sortable: true, width: '110px' },
  { title: 'المادة', key: 'subject_name', sortable: true, width: '140px' },
  { title: 'العام الدراسي', key: 'year_name', sortable: true, width: '120px' },
  { title: 'نطاق الاستهداف', key: 'target_scope_level', sortable: true, width: '140px' },
  { title: 'النماذج والأسئلة', key: 'exam_details', sortable: false, width: '150px' },
  { title: 'حالة التوزيع', key: 'distribution_status', sortable: false, width: '160px' },
]

// Wizard Step 2: Secondary Table Headers for resolved schools in Step 2
const schoolTableHeaders = computed(() => {
  const headers = [
    { title: '#', key: 'index', sortable: false, width: '60px', align: 'center' },
    {
      title: isSchoolTarget.value ? 'اسم المدرسة' : 'اسم المعهد / الجامعة',
      key: 'name_ar',
      sortable: true
    },
    { title: 'رقم الفرع (Branch No)', key: 'branch_no', sortable: true, width: '160px' },
    { title: 'المحافظة', key: 'governorate', sortable: true, width: '180px' },
  ]

  if (isSchoolTarget.value) {
    headers.push({ title: 'المديرية', key: 'directorate', sortable: true, width: '180px' })
  }

  headers.push({ title: 'حالة الجاهزية', key: 'status', sortable: false, width: '150px' })

  return headers
})

// Secondary Table Headers for Live Monitor Dialog
const liveMonitorHeaders = [
  { title: 'المدرسة المستهدفة', key: 'school_name_ar', sortable: true },
  { title: 'كود الفرع', key: 'school_branch_no', sortable: true },
  { title: 'المحافظة', key: 'governorate_name', sortable: true },
  { title: 'حالة الاستلام', key: 'is_received', sortable: true },
  { title: 'وقت الاستلام', key: 'received_at', sortable: true },
  { title: 'كراسات الأسئلة', key: 'printed_booklets_count', sortable: true },
  { title: 'أوراق OMR', key: 'printed_sheets_count', sortable: true },
  { title: 'الطلاب الحاضرين', key: 'students_attended_count', sortable: true },
  { title: 'رفع النتائج', key: 'results_synced_back', sortable: true },
]

const filteredDistributions = computed(() => {
  let list = distributionsList.value
  if (filterInstitutionType.value) {
    list = list.filter(d => {
      const type = d.institution_type || d.target_system || d.exam?.institution_type || 'school'
      return type === filterInstitutionType.value
    })
  }
  if (filterTargetLevel.value) {
    list = list.filter(d => d.target_level === filterTargetLevel.value)
  }
  if (filterStatus.value) {
    list = list.filter(d => d.status === filterStatus.value)
  }
  return list
})

function getInstType(item) {
  return item.institution_type || item.target_system || item.exam?.institution_type || 'school'
}

function getInstTypeLabel(item) {
  const type = getInstType(item)
  if (type === 'university') return 'جامعات'
  if (type === 'institute') return 'معاهد'
  return 'مدارس'
}

function getInstTypeColor(item) {
  const type = getInstType(item)
  if (type === 'university') return 'indigo'
  if (type === 'institute') return 'amber-darken-3'
  return 'teal'
}

function getInstTypeIcon(item) {
  const type = getInstType(item)
  if (type === 'university') return 'mdi-town-hall'
  if (type === 'institute') return 'mdi-tools'
  return 'mdi-school-outline'
}

// Items object format compatible with custom-data-table
const tableItems = computed(() => ({
  results: filteredDistributions.value,
  count: filteredDistributions.value.length,
  pagination: {
    count: filteredDistributions.value.length,
    current_page: 1,
    num_pages: 1,
  }
}))

const liveMonitorSearchQuery = ref('')
const liveMonitorFilterStatus = ref('all')

const filteredLiveMonitorSchools = computed(() => {
  let list = liveMonitorData.value?.schools || []
  if (liveMonitorFilterStatus.value === 'received') {
    list = list.filter(s => s.is_received)
  } else if (liveMonitorFilterStatus.value === 'pending') {
    list = list.filter(s => !s.is_received)
  }
  if (liveMonitorSearchQuery.value) {
    const q = liveMonitorSearchQuery.value.toLowerCase().trim()
    list = list.filter(s =>
      (s.school_name_ar && s.school_name_ar.toLowerCase().includes(q)) ||
      (s.school_branch_no && String(s.school_branch_no).includes(q)) ||
      (s.governorate_name && s.governorate_name.toLowerCase().includes(q))
    )
  }
  return list
})

const liveMonitorSchoolsTableItems = computed(() => ({
  results: filteredLiveMonitorSchools.value,
  count: filteredLiveMonitorSchools.value.length,
  pagination: {
    count: filteredLiveMonitorSchools.value.length,
    current_page: 1,
    num_pages: 1,
  }
}))

const totalTargetedSchoolsCount = computed(() => {
  return distributionsList.value.reduce((acc, cur) => acc + (cur.targeted_schools_count || 0), 0)
})

onMounted(() => {
  initDefaultTimings()
  getData()
  loadAuxiliaryData()
  loadEducationalHierarchy()
})

function initDefaultTimings() {
  const now = new Date()
  const pad = (n) => String(n).padStart(2, '0')
  const toLocalISO = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`

  const dispatchTime = new Date(now.getTime() + 10 * 60000) // بعد 10 دقائق
  const accessibleTime = new Date(now.getTime() + 60 * 60000) // بعد ساعة للطباعة
  const examStartTime = new Date(now.getTime() + 90 * 60000) // بعد ساعة ونصف
  const examEndTime = new Date(now.getTime() + 210 * 60000) // بعد 3 ساعات ونصف

  dispatchForm.value.dispatch_at = toLocalISO(dispatchTime)
  dispatchForm.value.accessible_from = toLocalISO(accessibleTime)
  dispatchForm.value.exam_start_at = toLocalISO(examStartTime)
  dispatchForm.value.exam_end_at = toLocalISO(examEndTime)
}

// Standard getData function used by custom-data-table
async function getData(tableParams = null) {
  loading.value = true
  try {
    let queryParams = {}
    if (tableParams && tableParams.params) {
      queryParams = { ...tableParams.params }
    }
    if (filterInstitutionType.value) queryParams.institution_type = filterInstitutionType.value
    if (filterTargetLevel.value) queryParams.target_level = filterTargetLevel.value
    if (filterStatus.value) queryParams.status = filterStatus.value

    const distData = await examsService.getDistributions(queryParams)
    distributionsList.value = distData.results || distData || []
    return tableItems.value
  } catch (err) {
    console.error('Error fetching distributions:', err)
    return { results: [], count: 0, pagination: { count: 0, current_page: 1, num_pages: 1 } }
  } finally {
    loading.value = false
  }
}

async function loadAuxiliaryData() {
  try {
    const examsRes = await examsService.getArchivedExams({ limit: 50, page_size: 50 })
    availableExams.value = examsRes.results || examsRes || []
  } catch (err) {
    console.error('Error loading auxiliary data:', err)
  }
}

async function loadEducationalHierarchy() {
  loadingGeoData.value = true
  try {
    const res = await examsService.getEducationalHierarchy()
    const data = res?.data || res?.results || (Array.isArray(res) ? res : [])
    educationalOrgsList.value = Array.isArray(data) ? data : []
  } catch (err) {
    console.error('Error loading educational hierarchy:', err)
  } finally {
    loadingGeoData.value = false
  }
}

async function loadOrganizations(params = {}) {
  const instType = selectedExam.value?.institution_type || filterExamInstitutionType.value || 'school'
  if (instType === 'school' && (!params.governorate || !params.directorate)) {
    allSchoolsList.value = []
    return
  }
  if ((instType === 'university' || instType === 'institute') && !params.governorate) {
    allSchoolsList.value = []
    return
  }

  loadingSchools.value = true
  try {
    const queryParts = [`institution_type=${instType}`]
    if (params.governorate) queryParts.push(`governorate=${params.governorate}`)
    if (params.directorate) queryParts.push(`directorate=${params.directorate}`)
    const res = await api.get(`api/academic/organizations/all/?${queryParts.join('&')}`)
    const data = res.data?.data || res.data?.results || res.data || []
    allSchoolsList.value = Array.isArray(data) ? data : []
  } catch (err) {
    console.error('Error loading organizations:', err)
    allSchoolsList.value = []
  } finally {
    loadingSchools.value = false
  }
}

function applyFilters() {
  return getData()
}

function resetFilters() {
  filterInstitutionType.value = null
  filterTargetLevel.value = null
  filterStatus.value = null
  return getData()
}

function onInstitutionTypeFilterChange() {
  return getData()
}

async function openNewDispatchWizard() {
  currentTab.value = 'wizard'
  currentStep.value = 1
  if (availableExams.value.length === 0) {
    loading.value = true
    await loadAuxiliaryData()
    loading.value = false
  }
  filterExamInstitutionType.value = filterInstitutionType.value || 'school'
  const targetType = filterExamInstitutionType.value
  const typedExams = availableExams.value.filter(e => (e.institution_type || 'school') === targetType)
  const firstNonActive = typedExams.find(e => !getExamActiveDistribution(e)) || typedExams[0] || null
  selectedExam.value = firstNonActive
  if (selectedExam.value) {
    selectExam(selectedExam.value)
  } else {
    dispatchForm.value.title = ''
    selectedTargetLevel.value = 'ministry'
    selectedOrgIds.value = []
    schoolSearchQuery.value = ''
    fetchResolvedSchools()
  }
}

function selectExam(exam) {
  selectedExam.value = exam
  dispatchForm.value.title = `تصدير اختبار: ${exam.title}`
  step2FilterGovernorate.value = null
  step2FilterDirectorate.value = null
  schoolSearchQuery.value = ''

  // استخراج وتطبيق نطاق الاستهداف المعتمد مسبقاً للاختبار مباشرة
  if (exam.target_scope_level && exam.target_scope_level !== 'all') {
    selectedTargetLevel.value = exam.target_scope_level
    const scopes = exam.target_scopes_data || []
    if (scopes.length > 0) {
      if (exam.target_scope_level === 'governorate') {
        selectedOrgIds.value = scopes.filter(s => s.governorate).map(s => s.governorate)
      } else if (exam.target_scope_level === 'directorate') {
        selectedOrgIds.value = scopes.filter(s => s.directorate).map(s => s.directorate)
      } else if (exam.target_scope_level === 'school') {
        selectedOrgIds.value = scopes.filter(s => s.organization).map(s => s.organization)
      }
    } else if (exam.governorate) {
      selectedTargetLevel.value = 'governorate'
      selectedOrgIds.value = [exam.governorate]
    } else if (exam.directorate) {
      selectedTargetLevel.value = 'directorate'
      selectedOrgIds.value = [exam.directorate]
    } else {
      selectedOrgIds.value = []
    }
  } else if (exam.governorate) {
    selectedTargetLevel.value = 'governorate'
    selectedOrgIds.value = [exam.governorate]
  } else {
    selectedTargetLevel.value = 'ministry'
    selectedOrgIds.value = []
  }
  fetchResolvedSchools()
}

async function fetchResolvedSchools() {
  return getResolvedSchoolsData({ page: 1 })
}

async function submitDispatch() {
  if (!selectedExam.value) return
  saving.value = true

  try {
    const payload = {
      exam_id: selectedExam.value.id,
      title: dispatchForm.value.title,
      target_level: selectedTargetLevel.value,
      target_system: selectedExam.value.institution_type || filterExamInstitutionType.value || 'school',
      delivery_mode: dispatchForm.value.delivery_mode,
      dispatch_at: dispatchForm.value.dispatch_at,
      accessible_from: dispatchForm.value.accessible_from,
      exam_start_at: dispatchForm.value.exam_start_at,
      exam_end_at: dispatchForm.value.exam_end_at,
      is_encrypted: dispatchForm.value.is_encrypted,
      auto_unlock: dispatchForm.value.auto_unlock,
      notes: dispatchForm.value.notes,
      selected_school_ids: allResolvedSchoolIds.value.length > 0 ? allResolvedSchoolIds.value : resolvedSchools.value.map(s => s.id)
    }

    await examsService.createDispatch(payload)
    await getData()
    currentTab.value = 'list'
  } catch (err) {
    console.error('Error creating dispatch:', err)
    const msg = err.response?.data?.message || err.message || 'فشل جدولة مهمة التوزيع'
    showNotification(msg, 'error', 'mdi-alert-circle')
  } finally {
    saving.value = false
  }
}

async function openLiveMonitor(item) {
  selectedMonitorDistribution.value = item
  showLiveMonitorDialog.value = true
  await refreshLiveMonitor()
}

async function refreshLiveMonitor() {
  if (!selectedMonitorDistribution.value) return liveMonitorSchoolsTableItems.value
  try {
    const res = await examsService.getDistributionLiveStatus(selectedMonitorDistribution.value.id)
    liveMonitorData.value = res
    return liveMonitorSchoolsTableItems.value
  } catch (err) {
    console.error('Error loading live status:', err)
    return liveMonitorSchoolsTableItems.value
  }
}

function previewPackageJson(item) {
  const snippet = {
    dispatch_id: item.id,
    exam_title: item.exam_title,
    exam_unique_code: item.exam_unique_code,
    timing: {
      dispatch_at: item.dispatch_at,
      accessible_from: item.accessible_from,
      exam_start_at: item.exam_start_at,
      exam_end_at: item.exam_end_at,
      is_locked: item.status === 'scheduled'
    },
    sample_api_call: `GET /api/exams/distributions/export-package/?branch_no=50001`,
    models_sample: [
      {
        version_code: "A",
        total_questions: 40,
        omr_spec: "A4_40Q_STANDARD"
      }
    ]
  }
  packageJsonSnippet.value = JSON.stringify(snippet, null, 2)
  showPackagePreviewDialog.value = true
}

// Quick Timing Presets
function applyTimingPreset(type) {
  const now = new Date()
  const pad = (n) => String(n).padStart(2, '0')
  const toLocalISO = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`

  if (type === 'now') {
    dispatchForm.value.dispatch_at = toLocalISO(now)
    dispatchForm.value.accessible_from = toLocalISO(now)
    dispatchForm.value.exam_start_at = toLocalISO(new Date(now.getTime() + 5 * 60000))
    dispatchForm.value.exam_end_at = toLocalISO(new Date(now.getTime() + 125 * 60000))
  } else if (type === '2hours') {
    dispatchForm.value.dispatch_at = toLocalISO(now)
    dispatchForm.value.accessible_from = toLocalISO(new Date(now.getTime() + 60 * 60000))
    dispatchForm.value.exam_start_at = toLocalISO(new Date(now.getTime() + 120 * 60000))
    dispatchForm.value.exam_end_at = toLocalISO(new Date(now.getTime() + 240 * 60000))
  } else if (type === 'tomorrow_morning') {
    const tomorrow = new Date(now)
    tomorrow.setDate(tomorrow.getDate() + 1)

    const dispatchTime = new Date(now)
    dispatchTime.setHours(22, 0, 0, 0)

    const accessibleTime = new Date(tomorrow)
    accessibleTime.setHours(7, 0, 0, 0)

    const examStart = new Date(tomorrow)
    examStart.setHours(8, 0, 0, 0)

    const examEnd = new Date(tomorrow)
    examEnd.setHours(10, 0, 0, 0)

    dispatchForm.value.dispatch_at = toLocalISO(dispatchTime)
    dispatchForm.value.accessible_from = toLocalISO(accessibleTime)
    dispatchForm.value.exam_start_at = toLocalISO(examStart)
    dispatchForm.value.exam_end_at = toLocalISO(examEnd)
  }
}

// Download Package File (Offline JSON Export)
async function downloadPackageFile(item) {
  try {
    const res = await examsService.downloadDistributionPackage(item.id)
    const pkg = res.package || res
    const blob = new Blob([JSON.stringify(pkg, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `ExamPackage_${item.exam_unique_code || item.id}_${item.id}.json`
    a.click()
    URL.revokeObjectURL(url)
  } catch (err) {
    console.error('Error downloading package file:', err)
  }
}

// Emergency Force Unlock State & Methods
const showForceUnlockDialog = ref(false)
const distributionToUnlock = ref(null)
const unlocking = ref(false)

function promptForceUnlock(item) {
  distributionToUnlock.value = item
  showForceUnlockDialog.value = true
}

// Floating Feedback Snackbar State
const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
  icon: 'mdi-check-circle'
})

function showNotification(text, color = 'success', icon = 'mdi-check-circle') {
  snackbar.value = {
    show: true,
    text,
    color,
    icon
  }
}

async function confirmForceUnlock() {
  if (!distributionToUnlock.value) return
  unlocking.value = true
  try {
    await examsService.forceUnlockDistribution(distributionToUnlock.value.id)
    showForceUnlockDialog.value = false
    showNotification('تم فك حجب الأسئلة بنجاح وإتاحتها للطباعة في المدارس فوراً', 'amber-darken-3', 'mdi-lock-open-check')
    await getData()
    if (selectedMonitorDistribution.value && selectedMonitorDistribution.value.id === distributionToUnlock.value.id) {
      await refreshLiveMonitor()
    }
  } catch (err) {
    console.error('Error in force unlock:', err)
    showNotification('فشل فك الحجب: ' + (err.response?.data?.message || err.message), 'error', 'mdi-alert-circle')
  } finally {
    unlocking.value = false
  }
}

// Cancel Dispatch State & Methods
const showCancelDialog = ref(false)
const distributionToCancel = ref(null)
const cancelReason = ref('')
const cancelling = ref(false)

function promptCancelDispatch(item) {
  distributionToCancel.value = item
  cancelReason.value = ''
  showCancelDialog.value = true
}

async function confirmCancelDispatch() {
  if (!distributionToCancel.value) return
  cancelling.value = true
  try {
    await examsService.cancelDistribution(distributionToCancel.value.id, cancelReason.value)
    showCancelDialog.value = false
    showNotification('تم إلغاء مهمة التوزيع وحجب الأسئلة بنجاح', 'error', 'mdi-close-circle')
    await getData()
    if (selectedMonitorDistribution.value && selectedMonitorDistribution.value.id === distributionToCancel.value.id) {
      await refreshLiveMonitor()
    }
  } catch (err) {
    console.error('Error in cancel dispatch:', err)
    showNotification('فشل إلغاء المهمة: ' + (err.response?.data?.message || err.message), 'error', 'mdi-alert-circle')
  } finally {
    cancelling.value = false
  }
}

// School Interaction Simulator State & Methods
const showSimulatorPanel = ref(false)
const simulatorResult = ref(null)
const simulatorForm = ref({
  school_id: null,
  action_type: 'full_sync',
  printed_booklets: 120,
  printed_sheets: 120,
  attended_students: 118,
  sync_results: false
})
const simulating = ref(false)

async function runSimulator() {
  if (!selectedMonitorDistribution.value || !simulatorForm.value.school_id) return
  simulating.value = true
  simulatorResult.value = null
  try {
    const res = await examsService.simulateSchoolSync(selectedMonitorDistribution.value.id, simulatorForm.value)
    simulatorResult.value = res
    showNotification(res.message || 'تمت محاكاة تفاعل المدرسة وتحديث لوحة المتابعة بنجاح', 'success', 'mdi-check-decagram')
    await refreshLiveMonitor()
  } catch (err) {
    console.error('Error in running simulator:', err)
    showNotification('فشل تنفيذ المحاكاة: ' + (err.response?.data?.message || err.message), 'error', 'mdi-alert-circle')
  } finally {
    simulating.value = false
  }
}

// Export Live Monitor Data to CSV
function exportLiveMonitorCsv() {
  if (!liveMonitorData.value?.schools?.length) return
  const headers = ['اسم المدرسة', 'رقم الفرع', 'المحافظة', 'حالة الاستلام', 'وقت الاستلام', 'كراسات الأسئلة المطبوعة', 'أوراق OMR المطبوعة', 'الطلاب الحاضرين', 'إعادة رفع النتائج']
  const rows = liveMonitorData.value.schools.map(s => [
    `"${s.school_name_ar}"`,
    `"${s.school_branch_no}"`,
    `"${s.governorate_name}"`,
    s.is_received ? 'مستلم' : 'بانتظار السحب',
    s.received_at ? formatDateTime(s.received_at) : '-',
    s.printed_booklets_count || 0,
    s.printed_sheets_count || 0,
    s.students_attended_count || 0,
    s.results_synced_back ? 'نعم' : 'لا'
  ])
  const csvContent = '\uFEFF' + [headers.join(','), ...rows.map(r => r.join(','))].join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `live_dispatch_monitor_${selectedMonitorDistribution.value?.id || 'report'}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

function formatDateTime(val) {
  if (!val) return '-'
  const d = new Date(val)
  return d.toLocaleString('ar-YE', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function getLevelLabel(level) {
  const map = {
    ministry: 'الوزارة (شامل)',
    governorate: 'المحافظات',
    directorate: 'المديريات',
    school: 'مدارس محددة',
  }
  return map[level] || level
}

function getLevelColor(level) {
  const map = {
    ministry: 'purple',
    governorate: 'indigo',
    directorate: 'teal',
    school: 'blue',
  }
  return map[level] || 'grey'
}

function getLevelIcon(level) {
  const map = {
    ministry: 'mdi-city-variant',
    governorate: 'mdi-map-marker-radius',
    directorate: 'mdi-town-hall',
    school: 'mdi-school',
  }
  return map[level] || 'mdi-circle'
}

function getStatusLabel(status) {
  const map = {
    draft: 'مسودة',
    scheduled: 'مجدول',
    dispatched: 'تم الإرسال',
    accessible: 'متاح للطباعة',
    in_progress: 'جاري الاختبار',
    completed: 'مكتمل',
    cancelled: 'ملغي',
  }
  return map[status] || status
}

function getStatusColor(status) {
  const map = {
    draft: 'grey',
    scheduled: 'amber',
    dispatched: 'blue',
    accessible: 'teal',
    in_progress: 'indigo',
    completed: 'emerald',
    cancelled: 'red',
  }
  return map[status] || 'grey'
}
</script>

<style scoped>
.selected-card {
  border-color: rgb(var(--v-theme-primary)) !important;
  border-width: 2px !important;
  background-color: rgba(var(--v-theme-primary), 0.04) !important;
}

.step-item {
  opacity: 0.5;
  transition: all 0.3s;
}

.step-item.step-active {
  opacity: 1;
}

.step-item.step-done {
  opacity: 0.9;
}

.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-lift:hover {
  transform: translateY(-3px);
}
</style>
