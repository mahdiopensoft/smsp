<template>
  <div class="exam-dispatch-page">
    <!-- TAB 1: LIST & MONITOR VIEW -->
    <div v-if="currentTab === 'list'">
      <!-- System Filters Component -->
      <filter-fields label="خيارات البحث وتصفية مهام التوزيع" class="main-card border-0 pa-5 rounded-2xl mb-8">
        <v-row dense class="align-center">
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="searchQuery"
              placeholder="بحث بالعنوان أو المادة أو الرمز..."
              prepend-inner-icon="mdi-magnify"
              clearable
              density="compact"
              variant="outlined"
              hide-details
              class="mb-6"
            />
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
            />
          </v-col>

          <v-col cols="12" sm="6" md="2">
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
                    <v-list-item prepend-icon="mdi-code-json" title="معاينة حزمة JSON" @click="previewPackageJson(item)" />
                    <v-list-item prepend-icon="mdi-download" title="تنزيل الحزمة الرسمية (JSON)" @click="downloadPackageFile(item)" />
                    <v-divider class="my-1" />
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
        <!-- Wizard Header Bar with Return Button -->
        <div class="d-flex align-center justify-space-between mb-6 pb-4 border-b">
          <div class="d-flex align-center gap-3">
            <custom-btn
              type="prev"
              label="العودة لقائمة التوزيعات"
              variant="outlined"
              class="font-weight-bold px-4"
              :click="() => (currentTab = 'list')"
            />
            <div>
              <h2 class="text-h6 font-weight-black text-slate-800 mb-0">معالج جدولة وتصدير الاختبارات</h2>
              <span class="text-caption text-medium-emphasis">توزيع حزم الاختبارات المعتمدة وقوالب OMR للمدارس والجامعات</span>
            </div>
          </div>
        </div>

        <!-- Stepper Indicator -->
        <div class="wizard-stepper mb-8 d-flex justify-center">
          <div class="d-flex align-center gap-4">
            <div
              v-for="step in [1, 2, 3]"
              :key="step"
              class="step-item d-flex align-center gap-2"
              :class="{ 'step-active': currentStep === step, 'step-done': currentStep > step }"
            >
              <v-avatar size="34" :color="currentStep >= step ? 'primary' : 'slate-200'" class="font-weight-bold text-white">
                {{ step }}
              </v-avatar>
              <span class="text-subtitle-2 font-weight-bold" :class="currentStep >= step ? 'text-primary' : 'text-medium-emphasis'">
                {{ stepTitles[step - 1] }}
              </span>
              <v-icon v-if="step < 3" color="slate-300" class="ms-2">mdi-chevron-left</v-icon>
            </div>
          </div>
        </div>

        <!-- STEP 1: EXAM SELECTION -->
        <div v-if="currentStep === 1">
          <h2 class="text-h6 font-weight-bold text-slate-800 mb-2">1. اختيار الاختبار المعتمد المراد تصديره</h2>
          <p class="text-body-2 text-medium-emphasis mb-4">
            اختر أحد الاختبارات المعتمدة من الأرشيف لتوزيعها على المدارس أو الجامعات أو المعاهد التابعة.
          </p>

          <!-- Institution Type Filter Toggle -->
          <div class="d-flex align-center gap-2 mb-5 flex-wrap">
            <span class="text-caption font-weight-bold text-slate-700">نوع المؤسسة التعليمية:</span>
            <v-btn-toggle
              v-model="filterExamInstitutionType"
              mandatory
              density="compact"
              color="primary"
              rounded="lg"
              variant="outlined"
            >
              <v-btn value="school" size="small">
                <v-icon start size="16">mdi-school-outline</v-icon>
                مدارس
              </v-btn>
              <v-btn value="university" size="small">
                <v-icon start size="16">mdi-town-hall</v-icon>
                جامعات
              </v-btn>
              <v-btn value="institute" size="small">
                <v-icon start size="16">mdi-tools</v-icon>
                معاهد وتدريب مهني
              </v-btn>
            </v-btn-toggle>
            <v-chip size="small" variant="tonal" color="slate-600" class="font-weight-bold ms-auto">
              عدد الاختبارات المتاحة: {{ filteredAvailableExams.length }}
            </v-chip>
          </div>

          <!-- Empty State if no exams found for selected institution type -->
          <div v-if="filteredAvailableExams.length === 0" class="pa-8 text-center border rounded-2xl bg-slate-50 mb-4">
            <v-icon size="48" color="slate-400" class="mb-2">mdi-file-document-alert-outline</v-icon>
            <div class="text-subtitle-1 font-weight-bold text-slate-700">
              لا توجد اختبارات معتمدة خاصة بـ ({{ filterExamInstitutionType === 'school' ? 'المدارس' : filterExamInstitutionType === 'university' ? 'الجامعات' : 'المعاهد والتدريب المهني' }}) حالياً
            </div>
            <div class="text-caption text-medium-emphasis mt-1">
              يمكنك اعتماد اختبارات جديدة من شاشة «أرشيف الاختبارات» أو توليد اختبار مخصص لهذا المسار.
            </div>
          </div>

          <v-row v-else class="mb-4">
            <v-col
              v-for="exam in filteredAvailableExams"
              :key="exam.id"
              cols="12"
              md="6"
              lg="4"
            >
              <v-card
                class="main-card pa-5 rounded-2xl border-subtle transition-all cursor-pointer h-100 hover-lift"
                :class="{ 
                  'selected-card': selectedExam?.id === exam.id,
                  'border-amber-lighten-1 bg-amber-lighten-5': getExamActiveDistribution(exam)
                }"
                elevation="0"
                @click="selectExam(exam)"
              >
                <div class="d-flex justify-space-between align-start mb-2">
                  <div class="d-flex align-center gap-1 flex-wrap">
                    <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                      {{ exam.uniqueCode || exam.unique_code }}
                    </v-chip>
                    <v-chip
                      v-if="exam.institution_type"
                      size="x-small"
                      :color="exam.institution_type === 'institute' ? 'warning' : exam.institution_type === 'university' ? 'info' : 'emerald'"
                      variant="tonal"
                      class="font-weight-bold"
                    >
                      {{ exam.institution_type === 'institute' ? 'معاهد' : exam.institution_type === 'university' ? 'جامعة' : 'مدرسة' }}
                    </v-chip>
                    <v-chip
                      size="x-small"
                      :color="exam.target_scope_level === 'governorate' ? 'deep-purple' : exam.target_scope_level === 'directorate' ? 'indigo' : exam.target_scope_level === 'school' ? 'amber-darken-3' : 'teal'"
                      variant="tonal"
                      class="font-weight-bold"
                    >
                      <v-icon start size="12">{{ exam.target_scope_level === 'governorate' ? 'mdi-map-marker-radius' : exam.target_scope_level === 'directorate' ? 'mdi-town-hall' : exam.target_scope_level === 'school' ? 'mdi-school' : 'mdi-earth' }}</v-icon>
                      {{ exam.target_scope_level === 'governorate' ? 'محافظات محددة' : exam.target_scope_level === 'directorate' ? 'مديريات محددة' : exam.target_scope_level === 'school' ? 'مدارس محددة' : 'نطاق شامل' }}
                    </v-chip>

                    <!-- Active Distribution Status Badge -->
                    <v-chip
                      v-if="getExamActiveDistribution(exam)"
                      size="x-small"
                      color="amber-darken-4"
                      variant="flat"
                      class="font-weight-bold text-white shadow-xs"
                    >
                      <v-icon start size="12">mdi-clock-alert-outline</v-icon>
                      قيد التوزيع حالياً ({{ getExamActiveDistribution(exam).status_display }})
                    </v-chip>
                  </div>
                  <v-icon :color="selectedExam?.id === exam.id ? 'primary' : 'slate-300'">
                    {{ selectedExam?.id === exam.id ? 'mdi-checkbox-marked-circle' : 'mdi-checkbox-blank-circle-outline' }}
                  </v-icon>
                </div>
                <h3 class="text-subtitle-1 font-weight-bold text-slate-800 mb-2">{{ exam.title }}</h3>
                <div class="d-flex flex-column gap-1 text-caption text-medium-emphasis mb-3">
                  <div class="d-flex align-center gap-1">
                    <v-icon size="14">mdi-book-open-outline</v-icon>
                    <span>المادة: <strong>{{ exam.subject_name || 'عام' }}</strong></span>
                  </div>
                  <div class="d-flex align-center gap-1">
                    <v-icon size="14">mdi-calendar-range</v-icon>
                    <span>العام الدراسي: <strong>{{ exam.year_name || '2025/2026' }}</strong></span>
                  </div>
                </div>
                <div class="d-flex align-center justify-space-between pt-3 border-t text-caption font-weight-bold text-indigo">
                  <span>{{ exam.versions_count || 4 }} نماذج (A, B, C, D)</span>
                  <span>{{ exam.questions_count || 40 }} سؤالاً</span>
                </div>
              </v-card>
            </v-col>
          </v-row>

          <!-- Active Distribution Warning Alert -->
          <v-alert
            v-if="selectedExam && getExamActiveDistribution(selectedExam)"
            type="warning"
            variant="tonal"
            class="rounded-2xl font-weight-bold mt-4 mb-2 border-amber"
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

          <div class="d-flex justify-end mt-8">
            <custom-btn
              type="next"
              label="التالي: تحديد نطاق المؤسسات المستهدفة"
              color="primary"
              class="px-8 font-weight-bold"
              :disabled="!selectedExam || !!getExamActiveDistribution(selectedExam)"
              :click="() => (currentStep = 2)"
            />
          </div>
        </div>

        <!-- STEP 2: TARGETING HIERARCHY (DIRECTLY PRE-DETERMINED FROM EXAM) -->
        <div v-else-if="currentStep === 2">
          <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3">
            <div>
              <h2 class="text-h6 font-weight-bold text-slate-800 mb-1">
                2. نطاق المؤسسات المستهدفة بالتوزيع (معتمد ومحدد مسبقاً)
              </h2>
              <p class="text-body-2 text-medium-emphasis mb-0">
                تم اعتماد وتطبيق النطاق الجغرافي والمؤسسي المحدد مسبقاً للاختبار مباشرة دون الحاجة لإعادة التحديد.
              </p>
            </div>
            <v-chip color="success" variant="tonal" class="font-weight-bold">
              <v-icon start size="16">mdi-check-decagram</v-icon>
              نطاق معتمد تلقائياً من الاختبار
            </v-chip>
          </div>

          <!-- Pre-determined Target Scope Highlight Card -->
          <v-card class="main-card pa-5 rounded-2xl border-subtle bg-slate-50 mb-6" elevation="0">
            <v-row dense class="align-center">
              <v-col cols="12" md="7">
                <div class="d-flex align-center gap-3">
                  <v-avatar size="52" color="primary" class="text-white shadow-sm">
                    <v-icon size="26">{{ getLevelIcon(selectedTargetLevel) }}</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-caption text-medium-emphasis font-weight-bold">مستوى الاستهداف المعتمد للاختبار:</div>
                    <div class="text-h6 font-weight-black text-slate-800">
                      {{ getPreDeterminedScopeTitle(selectedExam) }}
                    </div>
                    <div class="text-caption text-slate-600 mt-1 d-flex align-center gap-1 flex-wrap">
                      <span class="font-weight-bold">الجهات المشمولة:</span>
                      <template v-if="getPreDeterminedScopeTargets(selectedExam).length > 0">
                        <v-chip
                          v-for="(tgt, idx) in getPreDeterminedScopeTargets(selectedExam)"
                          :key="idx"
                          size="x-small"
                          color="primary"
                          variant="flat"
                          class="font-weight-bold"
                        >
                          {{ tgt }}
                        </v-chip>
                      </template>
                      <v-chip v-else size="x-small" color="teal" variant="flat" class="font-weight-bold text-white">
                        كافة مدارس ومؤسسات الجمهورية
                      </v-chip>
                    </div>
                  </div>
                </div>
              </v-col>

              <v-col cols="12" md="5" class="d-flex justify-md-end align-center gap-3 mt-3 mt-md-0">
                <div class="pa-3 rounded-xl bg-white border text-center flex-grow-1 flex-md-grow-0" style="min-width: 170px;">
                  <div class="text-caption text-medium-emphasis font-weight-bold">المؤسسات المحصورة فعلياً</div>
                  <div class="text-h5 font-weight-black text-primary">{{ resolvedSchools.length }}</div>
                  <div class="text-caption text-emerald font-weight-bold">جاهزة لاستلام الحزمة</div>
                </div>

                <v-btn
                  size="small"
                  variant="text"
                  color="slate-600"
                  class="font-weight-bold"
                  prepend-icon="mdi-tune"
                  @click="showManualScopeOverride = !showManualScopeOverride"
                >
                  {{ showManualScopeOverride ? 'إخفاء التعديل' : 'تخصيص يدوي (اختياري)' }}
                </v-btn>
              </v-col>
            </v-row>

            <!-- Collapsible Manual Override (Only for edge cases) -->
            <v-expand-transition>
              <div v-if="showManualScopeOverride" class="mt-4 pt-4 border-t">
                <div class="d-flex align-center justify-space-between mb-3">
                  <span class="text-caption font-weight-bold text-slate-700">
                    تعديل استثنائي للمستوى والنطاق المعتمد:
                  </span>
                  <v-btn size="x-small" variant="text" color="error" @click="resetScopeToExamDefault">
                    إعادة ضبط للنطاق الافتراضي للاختبار
                  </v-btn>
                </div>

                <v-row class="mb-3" dense>
                  <v-col v-for="lvl in targetLevelOptions" :key="lvl.value" cols="6" sm="3">
                    <v-card
                      class="pa-3 rounded-xl border text-center cursor-pointer transition-all"
                      :class="{ 'selected-card': selectedTargetLevel === lvl.value }"
                      elevation="0"
                      @click="changeTargetLevel(lvl.value)"
                    >
                      <v-icon :color="selectedTargetLevel === lvl.value ? 'primary' : 'slate-500'" size="20" class="mb-1">{{ lvl.icon }}</v-icon>
                      <div class="text-caption font-weight-bold">{{ lvl.label }}</div>
                    </v-card>
                  </v-col>
                </v-row>

                <div v-if="selectedTargetLevel === 'governorate'">
                  <v-autocomplete
                    v-model="selectedOrgIds"
                    :items="governoratesList"
                    item-title="name_ar"
                    item-value="id"
                    multiple
                    chips
                    closable-chips
                    variant="outlined"
                    placeholder="اختر المحافظات المستهدفة..."
                    density="compact"
                    hide-details
                    @update:model-value="fetchResolvedSchools"
                  />
                </div>
                <div v-else-if="selectedTargetLevel === 'directorate'">
                  <v-autocomplete
                    v-model="selectedOrgIds"
                    :items="directoratesList"
                    item-title="name_ar"
                    item-value="id"
                    multiple
                    chips
                    closable-chips
                    variant="outlined"
                    placeholder="اختر المديريات المستهدفة..."
                    density="compact"
                    hide-details
                    @update:model-value="fetchResolvedSchools"
                  />
                </div>
                <div v-else-if="selectedTargetLevel === 'school'">
                  <v-autocomplete
                    v-model="selectedOrgIds"
                    :items="allSchoolsList"
                    item-title="name_ar"
                    item-value="id"
                    multiple
                    chips
                    closable-chips
                    variant="outlined"
                    placeholder="ابحث بالاسم أو رقم الفرع للمدرسة..."
                    density="compact"
                    hide-details
                    @update:model-value="fetchResolvedSchools"
                  />
                </div>
              </div>
            </v-expand-transition>
          </v-card>

          <!-- Resolved Schools Header & Real-time Search -->
          <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
            <div class="d-flex align-center gap-2">
              <span class="text-subtitle-2 font-weight-bold text-slate-800">
                قائمة المؤسسات والمدارس المستهدفة فعلياً:
              </span>
              <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                {{ resolvedSchools.length }} مؤسسة / مدرسة
              </v-chip>
              <v-chip size="small" color="teal" variant="tonal" class="font-weight-bold">
                <v-icon size="14" start>mdi-check-all</v-icon>
                عرض شامل لكافة المدارس الـ 30 دفعة واحدة (بدون بجنشن)
              </v-chip>
            </div>

            <!-- Inline Search Filter for Resolved Schools -->
            <div style="min-width: 260px;">
              <v-text-field
                v-model="schoolSearchQuery"
                density="compact"
                variant="outlined"
                placeholder="تصفية سريعة (الاسم، الفرع، المحافظة)..."
                prepend-inner-icon="mdi-magnify"
                hide-details
                clearable
              />
            </div>
          </div>

          <!-- Unpaginated Full Schools Table (Guaranteed 30 Schools Visible in Scrollable Card) -->
          <v-card class="main-card rounded-2xl overflow-hidden border-subtle mb-6" elevation="0">
            <div style="max-height: 460px; overflow-y: auto;">
              <v-table hover density="comfortable" class="bg-transparent">
                <thead>
                  <tr class="bg-slate-50 text-slate-700">
                    <th class="font-weight-bold text-center" style="width: 60px;">#</th>
                    <th class="font-weight-bold">اسم المدرسة</th>
                    <th class="font-weight-bold" style="width: 160px;">رقم الفرع (Branch No)</th>
                    <th class="font-weight-bold" style="width: 180px;">المحافظة</th>
                    <th class="font-weight-bold" style="width: 180px;">المديرية</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="filteredResolvedSchools.length === 0">
                    <td colspan="5" class="text-center py-8 text-medium-emphasis">
                      <v-icon size="36" color="slate-300" class="mb-2 d-block mx-auto">mdi-school-outline</v-icon>
                      <span>لا توجد مدارس مطابقة للاستهداف المحدد</span>
                    </td>
                  </tr>
                  <tr
                    v-for="(school, index) in filteredResolvedSchools"
                    :key="school.id || index"
                    class="transition-all"
                  >
                    <td class="text-center text-caption font-weight-bold text-medium-emphasis">
                      {{ index + 1 }}
                    </td>
                    <td>
                      <div class="font-weight-bold text-slate-800 d-flex align-center gap-2 py-1">
                        <v-avatar size="28" color="primary" variant="tonal" class="rounded-lg">
                          <v-icon size="16">mdi-school</v-icon>
                        </v-avatar>
                        <span>{{ school.name_ar }}</span>
                      </div>
                    </td>
                    <td>
                      <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold font-mono">
                        {{ school.branch_no }}
                      </v-chip>
                    </td>
                    <td>
                      <span class="text-body-2 text-slate-700">{{ school.governorate }}</span>
                    </td>
                    <td>
                      <span class="text-body-2 text-slate-600">{{ school.directorate }}</span>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </div>
            
            <!-- Table Footer Summary Confirming Full Unpaginated Delivery -->
            <div class="pa-3 bg-slate-50 border-t d-flex align-center justify-space-between text-caption text-medium-emphasis">
              <span>
                إجمالي المدارس المعروضة: <strong>{{ filteredResolvedSchools.length }}</strong> من أصل <strong>{{ resolvedSchools.length }}</strong> مدرسة
              </span>
              <span class="text-teal font-weight-bold">
                <v-icon size="14" color="teal" class="me-1">mdi-check-circle</v-icon>
                كافة المدارس الـ 30 مدرجة وجاهزة للاستلام دون تقسيم
              </span>
            </div>
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
              class="px-8 font-weight-bold"
              :disabled="resolvedSchools.length === 0"
              :click="() => (currentStep = 3)"
            />
          </div>
        </div>

        <!-- STEP 3: TIMING & SECURITY -->
        <div v-else-if="currentStep === 3">
          <h2 class="text-h6 font-weight-bold text-slate-800 mb-2">3. جدول المواعيد الزمنية والسرية</h2>
          <p class="text-body-2 text-medium-emphasis mb-6">
            اضبط مواعيد تسليم الحزمة، وقت إتاحة الأسئلة للطباعة بالمدرسة، ووقت بدء الامتحان.
          </p>

          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="dispatchForm.title"
                label="عنوان مهمة التوزيع"
                variant="outlined"
                density="compact"
                class="rounded-lg"
                placeholder="مثال: الاختبار النصفي الموحد - الرياضيات - ثالث ثانوي"
              />
            </v-col>

            <!-- Timing Fields Card -->
            <v-col cols="12" md="6">
              <v-card class="main-card pa-5 rounded-2xl border-subtle mb-4 h-100" elevation="0">
                <div class="text-subtitle-2 font-weight-bold text-indigo mb-3 d-flex align-center gap-1">
                  <v-icon size="18">mdi-clock-outline</v-icon>
                  <span>نوافذ التوقيت والجدولة</span>
                </div>

                <!-- Quick Timing Presets -->
                <div class="d-flex align-center gap-2 mb-4 flex-wrap">
                  <span class="text-caption font-weight-bold text-medium-emphasis">اختصارات ذكية:</span>
                  <v-chip size="x-small" variant="tonal" color="indigo" class="cursor-pointer font-weight-bold" @click="applyTimingPreset('now')">
                    <v-icon start size="12">mdi-lightning-bolt</v-icon> تجربة فورية (الآن)
                  </v-chip>
                  <v-chip size="x-small" variant="tonal" color="teal" class="cursor-pointer font-weight-bold" @click="applyTimingPreset('2hours')">
                    <v-icon start size="12">mdi-timer-outline</v-icon> بعد ساعتين
                  </v-chip>
                  <v-chip size="x-small" variant="tonal" color="primary" class="cursor-pointer font-weight-bold" @click="applyTimingPreset('tomorrow_morning')">
                    <v-icon start size="12">mdi-weather-sunset-up</v-icon> صباح الغد (08:00 ص)
                  </v-chip>
                </div>

                <div class="mb-4">
                  <label class="text-caption font-weight-bold text-slate-700 d-block mb-1">
                    1. وقت توفر الحزمة لنظام المدرسة (Dispatch Time):
                  </label>
                  <v-text-field
                    v-model="dispatchForm.dispatch_at"
                    type="datetime-local"
                    density="compact"
                    variant="outlined"
                    hide-details
                  />
                  <span class="text-caption text-medium-emphasis">تصل الحزمة لمخدم المدرسة بانتظار موعد الإتاحة.</span>
                </div>

                <div class="mb-4">
                  <label class="text-caption font-weight-bold text-amber-darken-3 d-block mb-1">
                    2. وقت فك الحجب وإتاحة الأسئلة للطباعة (Accessible Time):
                  </label>
                  <v-text-field
                    v-model="dispatchForm.accessible_from"
                    type="datetime-local"
                    density="compact"
                    variant="outlined"
                    hide-details
                  />
                  <span class="text-caption text-medium-emphasis">تفتح الأسئلة تلقائياً لكادر الكنترول بالمدرسة لبدء الطباعة.</span>
                </div>

                <div>
                  <label class="text-caption font-weight-bold text-teal d-block mb-1">
                    3. موعد بدء ونهاية الاختبار الرسمي:
                  </label>
                  <v-row dense>
                    <v-col cols="6">
                      <v-text-field
                        v-model="dispatchForm.exam_start_at"
                        type="datetime-local"
                        density="compact"
                        variant="outlined"
                        placeholder="البدء"
                        hide-details
                      />
                    </v-col>
                    <v-col cols="6">
                      <v-text-field
                        v-model="dispatchForm.exam_end_at"
                        type="datetime-local"
                        density="compact"
                        variant="outlined"
                        placeholder="الانتهاء"
                        hide-details
                      />
                    </v-col>
                  </v-row>
                </div>
              </v-card>
            </v-col>

            <!-- Security & Delivery Options Card -->
            <v-col cols="12" md="6">
              <v-card class="main-card pa-5 rounded-2xl border-subtle mb-4 h-100" elevation="0">
                <div class="text-subtitle-2 font-weight-bold text-teal mb-4 d-flex align-center gap-1">
                  <v-icon size="18">mdi-shield-lock-outline</v-icon>
                  <span>خيارات الأمان والسرية (منع التسريب)</span>
                </div>

                <v-switch
                  v-model="dispatchForm.is_encrypted"
                  color="indigo"
                  label="تشفير محتوى الأسئلة حتى موعد الإتاحة"
                  hide-details
                  class="mb-2"
                />

                <v-switch
                  v-model="dispatchForm.auto_unlock"
                  color="teal"
                  label="فتح الأسئلة تلقائياً بمجرد حلول وقت الإتاحة"
                  hide-details
                  class="mb-3"
                />

                <div class="pa-3 rounded-xl bg-slate-50 border mb-3">
                  <div class="text-caption font-weight-bold text-slate-800 mb-1">نمط تسليم وتنفيذ الاختبار المعتمد:</div>
                  <v-chip color="teal" variant="tonal" size="small" class="font-weight-bold">
                    <v-icon size="14" start>mdi-printer</v-icon>
                    طباعة كراسات + أوراق إجابة OMR
                  </v-chip>
                </div>

                <v-textarea
                  v-model="dispatchForm.notes"
                  label="تعليمات وملاحظات للكنترول المدرسي"
                  variant="outlined"
                  density="compact"
                  rows="2"
                  class="rounded-lg"
                  placeholder="تعليمات خاصة بأوراق الإجابة أو نماذج A/B/C/D..."
                />
              </v-card>
            </v-col>
          </v-row>

          <div class="d-flex justify-space-between mt-6">
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
              class="px-8 font-weight-bold text-white"
              :loading="saving"
              :click="submitDispatch"
            />
          </div>
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
const searchQuery = ref('')
const filterTargetLevel = ref(null)
const filterStatus = ref(null)

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

const filteredAvailableExams = computed(() => {
  return availableExams.value.filter(e => {
    const instType = e.institution_type || 'school'
    return instType === filterExamInstitutionType.value
  })
})

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
const schoolSearchQuery = ref('')

const filteredResolvedSchools = computed(() => {
  if (!schoolSearchQuery.value) return resolvedSchools.value
  const q = schoolSearchQuery.value.toLowerCase().trim()
  return resolvedSchools.value.filter(s =>
    (s.name_ar && s.name_ar.toLowerCase().includes(q)) ||
    (s.branch_no && String(s.branch_no).includes(q)) ||
    (s.governorate && s.governorate.toLowerCase().includes(q)) ||
    (s.directorate && s.directorate.toLowerCase().includes(q))
  )
})

const governoratesList = ref([])
const directoratesList = ref([])
const allSchoolsList = ref([])

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

const showManualScopeOverride = ref(false)

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

function resetScopeToExamDefault() {
  if (selectedExam.value) {
    selectExam(selectedExam.value)
  }
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

const targetLevelOptions = [
  { value: 'ministry', label: 'الوزارة (شامل)', icon: 'mdi-city-variant', desc: 'كافة المدارس والمعاهد في الجمهورية' },
  { value: 'governorate', label: 'مكاتب المحافظات', icon: 'mdi-map-marker-radius', desc: 'كل مؤسسات المحافظات المختارة' },
  { value: 'directorate', label: 'إدارات المديريات', icon: 'mdi-town-hall', desc: 'كل مؤسسات المديريات المختارة' },
  { value: 'school', label: 'مؤسسات / معاهد محددة', icon: 'mdi-school', desc: 'اختيار مدارس أو معاهد محددة بالاسم' },
]

// Main Table Headers for custom-data-table
const tableHeaders = [
  { title: 'مهمة التوزيع والاختبار', key: 'title', sortable: true },
  { title: 'المستوى المستهدف', key: 'target_level', sortable: true },
  { title: 'تقدم استلام المدارس', key: 'targeted_schools_count', sortable: true },
  { title: 'نافذة الإتاحة والامتحان', key: 'accessible_from', sortable: true },
  { title: 'نمط التسليم', key: 'delivery_mode', sortable: false },
  { title: 'الحالة', key: 'status', sortable: true },
]

// Secondary Table Headers for resolved schools in Step 2
const schoolTableHeaders = [
  { title: 'اسم المدرسة', key: 'name_ar', sortable: true },
  { title: 'رقم الفرع (Branch No)', key: 'branch_no', sortable: true },
  { title: 'المحافظة', key: 'governorate', sortable: true },
  { title: 'المديرية', key: 'directorate', sortable: true },
]

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
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(d =>
      (d.title && d.title.toLowerCase().includes(q)) ||
      (d.exam_title && d.exam_title.toLowerCase().includes(q)) ||
      (d.subject_name && d.subject_name.toLowerCase().includes(q)) ||
      (d.exam_unique_code && d.exam_unique_code.toLowerCase().includes(q))
    )
  }
  if (filterTargetLevel.value) {
    list = list.filter(d => d.target_level === filterTargetLevel.value)
  }
  if (filterStatus.value) {
    list = list.filter(d => d.status === filterStatus.value)
  }
  return list
})

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

onMounted(async () => {
  initDefaultTimings()
  await getData()
  await loadAuxiliaryData()
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
    if (searchQuery.value) queryParams.search = searchQuery.value
    if (filterTargetLevel.value) queryParams.target_level = filterTargetLevel.value
    if (filterStatus.value) queryParams.status = filterStatus.value

    const distData = await examsService.getDistributions(queryParams)
    distributionsList.value = distData.results || distData || []
  } catch (err) {
    console.error('Error fetching distributions:', err)
  } finally {
    loading.value = false
  }
}

async function loadAuxiliaryData() {
  try {
    // 1. Fetch approved exams
    const examsRes = await examsService.getArchivedExams({ limit: 50, page_size: 50 })
    availableExams.value = examsRes.results || examsRes || []

    // 2. Load schools hierarchy directly from resolve-hierarchy endpoint
    await fetchResolvedSchools()

    // 3. Fetch organizations hierarchy with high page_size to avoid pagination truncating
    const orgsRes = await api.get('common/branch/?page_size=500&limit=500')
    const allOrgs = orgsRes.data?.data || orgsRes.data?.results || orgsRes.data || []
    governoratesList.value = allOrgs.filter(o => o.company_level === 30)
    directoratesList.value = allOrgs.filter(o => o.company_level === 40)
    allSchoolsList.value = allOrgs.filter(o => o.company_level === 50)
  } catch (err) {
    console.error('Error loading auxiliary data:', err)
  }
}

function applyFilters() {
  getData()
}

function resetFilters() {
  searchQuery.value = ''
  filterTargetLevel.value = null
  filterStatus.value = null
  getData()
}

function openNewDispatchWizard() {
  currentTab.value = 'wizard'
  currentStep.value = 1
  filterExamInstitutionType.value = 'school'
  const schoolExams = availableExams.value.filter(e => (e.institution_type || 'school') === 'school')
  const firstNonActive = schoolExams.find(e => !getExamActiveDistribution(e)) || schoolExams[0] || null
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
  showManualScopeOverride.value = false

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

function changeTargetLevel(level) {
  selectedTargetLevel.value = level
  selectedOrgIds.value = []
  schoolSearchQuery.value = ''
  fetchResolvedSchools()
}

async function fetchResolvedSchools() {
  try {
    const payload = {
      target_level: selectedTargetLevel.value || 'ministry',
      selected_org_ids: selectedOrgIds.value || []
    }
    if (selectedExam.value?.id) {
      payload.exam_id = selectedExam.value.id
    }
    const res = await examsService.resolveDistributionHierarchy(payload)
    const list = res?.schools || res?.results || res?.data?.schools || (Array.isArray(res) ? res : [])
    if (list && list.length > 0) {
      resolvedSchools.value = list
    } else if (selectedTargetLevel.value === 'ministry' && allSchoolsList.value.length > 0) {
      resolvedSchools.value = allSchoolsList.value.map(s => ({
        id: s.id,
        name_ar: s.name_ar,
        branch_no: s.branch_no,
        governorate: s.fk_governorate_name || s.governorate || '-',
        directorate: s.fk_directorate_name || s.directorate || '-'
      }))
    } else {
      resolvedSchools.value = []
    }
  } catch (e) {
    console.error('Error resolving hierarchy:', e)
    if (selectedTargetLevel.value === 'ministry' && allSchoolsList.value.length > 0) {
      resolvedSchools.value = allSchoolsList.value.map(s => ({
        id: s.id,
        name_ar: s.name_ar,
        branch_no: s.branch_no,
        governorate: s.fk_governorate_name || s.governorate || '-',
        directorate: s.fk_directorate_name || s.directorate || '-'
      }))
    }
  }
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
      selected_school_ids: resolvedSchools.value.map(s => s.id)
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
  if (!selectedMonitorDistribution.value) return
  try {
    const res = await examsService.getDistributionLiveStatus(selectedMonitorDistribution.value.id)
    liveMonitorData.value = res
  } catch (err) {
    console.error('Error loading live status:', err)
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
