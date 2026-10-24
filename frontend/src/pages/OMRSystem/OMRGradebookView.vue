<template>
  <div class="qb-gradebook-view-v4">

    <!-- ── 1. Sector Switcher (فصل نوع المؤسسة التعليمية بشكل قاطع) ── -->
    <div class="d-flex align-center justify-start flex-wrap gap-3 mb-4">
      <v-btn-toggle
        v-model="institutionType"
        mandatory
        color="primary"
        variant="outlined"
        density="comfortable"
        rounded="xl"
        class="bg-surface border"
        @update:model-value="onSectorChange"
      >
        <v-btn value="school" class="px-4 font-weight-bold" prepend-icon="mdi-school">
          التعليم العام (المدرسي)
        </v-btn>
        <v-btn value="university" class="px-4 font-weight-bold" prepend-icon="mdi-domain">
          التعليم الجامعي (كليات وجامعات)
        </v-btn>
        <v-btn value="institute" class="px-4 font-weight-bold" prepend-icon="mdi-tools">
          التعليم الفني والمهني (معاهد)
        </v-btn>
      </v-btn-toggle>


    </div>

    <!-- ── 2. MASTER VIEW: عرض الهيكل الإداري والمكاتب والمديريات والمراكز والاختبارات ── -->
    <div v-if="currentView === 'master'" class="master-view-container">
      <!-- شريط التصفية الهيكلي الموحد (مرتب وبدون تكرار) -->
      <div class="main-card pa-4 rounded-2xl mb-4 bg-surface border elevation-1">
        <v-row dense class="align-center">
          <!-- التعليم العام (مدرسي) -->
          <template v-if="institutionType === 'school'">
            <!-- مكتب التربية والتعليم بالمحافظة (المستوى 30 الحقيقي) -->
            <v-col cols="12" md="4">
              <v-autocomplete
                v-model="selectedOfficeId"
                :items="realOfficesList"
                item-title="name_ar"
                item-value="id"
                label="مكتب التربية والتعليم (المحافظة)"
                placeholder="اختر مكتب التربية بالمحافظة..."
                clearable
                density="compact"
                variant="outlined"
                hide-details
                prepend-inner-icon="mdi-office-building-outline"
                @update:model-value="onOfficeFilterChange"
              />
            </v-col>

            <!-- إدارة التربية والتعليم بالمديرية (المستوى 40 الحقيقي) -->
            <v-col cols="12" md="4">
              <v-autocomplete
                v-model="selectedDirectorateId"
                :items="realDirectoratesList"
                item-title="name_ar"
                item-value="id"
                label="إدارة التربية والتعليم (المديرية)"
                placeholder="اختر إدارة التربية بالمديرية..."
                clearable
                density="compact"
                variant="outlined"
                hide-details
                prepend-inner-icon="mdi-map-marker-radius-outline"
                @update:model-value="onDirectorateFilterChange"
              />
            </v-col>

            <!-- المدرسة / المركز الامتحاني -->
            <v-col cols="12" md="4">
              <v-autocomplete
                v-model="selectedSchoolId"
                :items="realSchoolsList"
                item-title="name_ar"
                item-value="id"
                label="المدرسة / المركز الامتحاني"
                placeholder="اختر المركز أو المدرسة..."
                clearable
                density="compact"
                variant="outlined"
                hide-details
                prepend-inner-icon="mdi-school-outline"
                @update:model-value="onSchoolFilterChange"
              />
            </v-col>
          </template>

          <!-- التعليم الجامعي -->
          <template v-else-if="institutionType === 'university'">
            <v-col cols="12" md="6">
              <v-autocomplete
                v-model="selectedSchoolId"
                :items="filteredSchoolsTable"
                item-title="name"
                item-value="id"
                label="الجامعة / الكلية"
                placeholder="اختر الجامعة أو الكلية..."
                clearable
                density="compact"
                variant="outlined"
                hide-details
                prepend-inner-icon="mdi-domain"
                @update:model-value="onSchoolFilterChange"
              />
            </v-col>
          </template>

          <!-- التعليم الفني والمهني (معاهد) -->
          <template v-else-if="institutionType === 'institute'">
            <v-col cols="12" md="6">
              <v-autocomplete
                v-model="selectedSchoolId"
                :items="filteredSchoolsTable"
                item-title="name"
                item-value="id"
                label="المعهد التقني / المهني"
                placeholder="اختر المعهد..."
                clearable
                density="compact"
                variant="outlined"
                hide-details
                prepend-inner-icon="mdi-tools"
                @update:model-value="onSchoolFilterChange"
              />
            </v-col>
          </template>
        </v-row>
      </div>

      <!-- تبويبات الاستعراض الهيكلي (Master Tabs) -->
      <div class="main-card rounded-2xl overflow-hidden mb-6 elevation-1 bg-surface border">
        <div class="d-flex align-center justify-space-between flex-wrap gap-2 px-4 pt-3 border-b">
          <v-tabs v-model="masterTab" color="primary" density="compact">
            <v-tab v-if="institutionType === 'school'" value="offices" class="font-weight-bold">
              <v-icon start size="18">mdi-office-building-outline</v-icon>
              مكاتب التربية والتعليم ({{ filteredOfficesTable.length }})
            </v-tab>
            <v-tab v-if="institutionType === 'school'" value="directorates" class="font-weight-bold">
              <v-icon start size="18">mdi-map-marker-radius-outline</v-icon>
              إدارات التربية بالمديريات ({{ filteredDirectoratesTable.length }})
            </v-tab>
            <v-tab value="schools" class="font-weight-bold">
              <v-icon start size="18">{{ institutionType === 'university' ? 'mdi-domain' : (institutionType === 'institute' ? 'mdi-tools' : 'mdi-school-outline') }}</v-icon>
              {{ institutionType === 'university' ? 'الجامعات والكليات' : (institutionType === 'institute' ? 'المعاهد والمراكز' : 'المراكز الامتحانية والمدارس') }} ({{ filteredSchoolsTable.length }})
            </v-tab>
            <v-tab value="exams" class="font-weight-bold">
              <v-icon start size="18">mdi-file-document-check-outline</v-icon>
              الاختبارات الأكاديمية ({{ filteredExamsTable.length }})
            </v-tab>
          </v-tabs>

          <!-- شريط بحث الجدول السريع -->
          <div style="max-width: 280px;" class="pb-2">
            <v-text-field
              v-model="masterSearchQuery"
              placeholder="بحث سريع في الجدول..."
              prepend-inner-icon="mdi-magnify"
              density="compact"
              variant="outlined"
              hide-details
              clearable
              class="bg-white rounded-lg"
            />
          </div>
        </div>

        <v-window v-model="masterTab">
          <!-- 1. تبويب مكاتب التربية بالمحافظات -->
          <v-window-item value="offices" v-if="institutionType === 'school'">
            <v-data-table
              :headers="officeMasterHeaders"
              :items="filteredOfficesTable"
              :loading="loadingMaster"
              density="comfortable"
              hover
              class="elevation-0"
              no-data-text="لا توجد مكاتب تربية مسجلة"
            >
              <template #item.office_name="{ item }">
                <div class="d-flex align-center py-2">
                  <v-avatar color="primary" variant="tonal" size="36" class="me-3 rounded-lg">
                    <v-icon color="primary" size="20">mdi-office-building-outline</v-icon>
                  </v-avatar>
                  <div>
                    <div class="font-weight-bold text-subtitle-2 text-on-surface">{{ item.office_name }}</div>
                    <div class="text-caption text-medium-emphasis">المحافظة: {{ item.governorate_name }}</div>
                  </div>
                </div>
              </template>

              <template #item.completion_rate="{ item }">
                <div class="d-flex align-center gap-2">
                  <v-progress-linear
                    :model-value="item.completion_rate"
                    color="primary"
                    height="8"
                    rounded
                    class="flex-grow-1"
                  />
                  <span class="text-caption font-weight-bold">{{ item.completion_rate }}%</span>
                </div>
              </template>

              <template #item.actions="{ item }">
                <div class="d-flex align-center justify-center gap-2">
                  <v-btn
                    size="small"
                    color="primary"
                    variant="tonal"
                    rounded="lg"
                    class="font-weight-bold"
                    prepend-icon="mdi-arrow-down-right"
                    @click="drillDownToOffice(item)"
                  >
                    المديريات
                  </v-btn>
                  <v-btn
                    size="small"
                    color="primary"
                    variant="flat"
                    rounded="lg"
                    class="font-weight-bold"
                    prepend-icon="mdi-account-group-outline"
                    @click="openOfficeRoster(item)"
                  >
                    كشف الطلاب
                  </v-btn>
                </div>
              </template>
            </v-data-table>
          </v-window-item>

          <!-- 2. تبويب إدارات التربية بالمديريات -->
          <v-window-item value="directorates" v-if="institutionType === 'school'">
            <v-data-table
              :headers="directorateMasterHeaders"
              :items="filteredDirectoratesTable"
              :loading="loadingMaster"
              density="comfortable"
              hover
              class="elevation-0"
              no-data-text="لا توجد إدارات تربية مسجلة"
            >
              <template #item.name="{ item }">
                <div class="d-flex align-center py-2">
                  <v-avatar color="teal" variant="tonal" size="36" class="me-3 rounded-lg">
                    <v-icon color="teal" size="20">mdi-map-marker-radius-outline</v-icon>
                  </v-avatar>
                  <div>
                    <div class="font-weight-bold text-subtitle-2 text-on-surface">{{ item.name }}</div>
                    <div class="text-caption text-medium-emphasis">{{ item.office_name }}</div>
                  </div>
                </div>
              </template>

              <template #item.completion_rate="{ item }">
                <div class="d-flex align-center gap-2">
                  <v-progress-linear
                    :model-value="item.completion_rate"
                    color="teal"
                    height="8"
                    rounded
                    class="flex-grow-1"
                  />
                  <span class="text-caption font-weight-bold">{{ item.completion_rate }}%</span>
                </div>
              </template>

              <template #item.actions="{ item }">
                <div class="d-flex align-center justify-center gap-2">
                  <v-btn
                    size="small"
                    color="teal"
                    variant="tonal"
                    rounded="lg"
                    class="font-weight-bold"
                    prepend-icon="mdi-school"
                    @click="drillDownToDirectorate(item)"
                  >
                    المدارس
                  </v-btn>
                  <v-btn
                    size="small"
                    color="teal"
                    variant="flat"
                    rounded="lg"
                    class="font-weight-bold"
                    prepend-icon="mdi-account-group-outline"
                    @click="openDirectorateRoster(item)"
                  >
                    كشف الطلاب
                  </v-btn>
                </div>
              </template>
            </v-data-table>
          </v-window-item>

          <!-- 3. تبويب المراكز الامتحانية والمدارس / الجامعات / المعاهد -->
          <v-window-item value="schools">
            <v-data-table
              :headers="schoolMasterHeaders"
              :items="filteredSchoolsTable"
              :loading="loadingMaster"
              density="comfortable"
              hover
              class="elevation-0"
              no-data-text="لا توجد مدارس أو مراكز امتحانية مسجلة"
            >
              <template #item.school_name="{ item }">
                <div class="d-flex align-center py-2">
                  <v-avatar color="indigo" variant="tonal" size="36" class="me-3 rounded-lg">
                    <v-icon color="indigo" size="20">mdi-school-outline</v-icon>
                  </v-avatar>
                  <div>
                    <div class="font-weight-bold text-subtitle-2 text-on-surface">{{ item.name }}</div>
                    <div class="text-caption text-medium-emphasis">{{ item.directorate_name }} • {{ item.governorate_name }}</div>
                  </div>
                </div>
              </template>

              <template #item.institution_type="{ item }">
                <v-chip size="x-small" :color="item.institution_type === 'university' ? 'purple' : (item.institution_type === 'institute' ? 'amber' : 'primary')" variant="tonal" class="font-weight-bold">
                  {{ item.institution_type === 'university' ? 'جامعي' : (item.institution_type === 'institute' ? 'مهني/معهد' : 'مدرسي') }}
                </v-chip>
              </template>

              <template #item.exams_count="{ item }">
                <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                  {{ item.exams_count }} اختبار
                </v-chip>
              </template>

              <template #item.total_students="{ item }">
                <span class="font-weight-bold text-subtitle-2">{{ item.total_students }} طالب</span>
              </template>

              <template #item.completed_count="{ item }">
                <span class="font-weight-bold text-success">{{ item.completed_count }} ورقة</span>
              </template>

              <template #item.average_score="{ item }">
                <span class="font-weight-bold">{{ item.average_score }}%</span>
              </template>

              <template #item.completion_rate="{ item }">
                <div class="d-flex align-center gap-2">
                  <v-progress-linear
                    :model-value="item.completion_rate"
                    color="indigo"
                    height="8"
                    rounded
                    class="flex-grow-1"
                  />
                  <span class="text-caption font-weight-bold">{{ item.completion_rate }}%</span>
                </div>
              </template>

              <template #item.actions="{ item }">
                <div class="d-flex align-center justify-center gap-2">
                  <v-btn
                    size="small"
                    color="indigo"
                    variant="tonal"
                    rounded="lg"
                    class="font-weight-bold"
                    prepend-icon="mdi-clipboard-list-outline"
                    @click="openSchoolRoster(item)"
                  >
                    كشف درجات الطلاب
                  </v-btn>
                </div>
              </template>
            </v-data-table>
          </v-window-item>

          <!-- 4. تبويب الاختبارات الأكاديمية -->
          <v-window-item value="exams">
            <v-data-table
              :headers="examMasterHeaders"
              :items="filteredExamsTable"
              :loading="loadingMaster"
              density="comfortable"
              hover
              class="elevation-0"
              no-data-text="لا توجد اختبارات مسجلة في هذا النطاق"
            >
              <template #item.exam_title="{ item }">
                <div class="d-flex align-center py-2">
                  <v-avatar color="primary" variant="tonal" size="36" class="me-3 rounded-lg">
                    <v-icon color="primary" size="20">mdi-file-document-check-outline</v-icon>
                  </v-avatar>
                  <div>
                    <div class="font-weight-bold text-subtitle-2 text-on-surface">{{ item.title }}</div>
                    <div class="text-caption text-medium-emphasis">
                      <v-chip size="x-small" color="primary" variant="tonal" class="me-1 font-mono font-weight-black">
                        {{ item.uniqueCode }}
                      </v-chip>
                      <span>{{ item.subject_name }}</span>
                    </div>
                  </div>
                </div>
              </template>

              <template #item.geo_info="{ item }">
                <div class="text-caption font-weight-bold">
                  {{ item.governorate_name || 'كافة المناطق' }}
                  <span v-if="item.directorate_name" class="text-medium-emphasis"> • {{ item.directorate_name }}</span>
                </div>
              </template>

              <template #item.schools_count="{ item }">
                <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold">
                  <v-icon start size="14">mdi-school-outline</v-icon>
                  {{ item.schools_count }} {{ item.schools_count === 1 ? 'مدرسة/مركز' : 'مدارس/مراكز' }}
                </v-chip>
              </template>

              <template #item.total_students="{ item }">
                <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                  <v-icon start size="14">mdi-account-group</v-icon>
                  {{ item.total_students }} طالب
                </v-chip>
              </template>

              <template #item.completed_count="{ item }">
                <v-chip size="small" color="teal" variant="tonal" class="font-weight-bold">
                  <v-icon start size="14">mdi-check-decagram-outline</v-icon>
                  {{ item.completed_count }} ورقة
                </v-chip>
              </template>

              <template #item.completion_rate="{ item }">
                <div class="d-flex align-center gap-2">
                  <v-progress-linear
                    :model-value="item.completion_rate"
                    color="success"
                    height="8"
                    rounded
                    class="flex-grow-1"
                  />
                  <span class="text-caption font-weight-bold">{{ item.completion_rate }}%</span>
                </div>
              </template>

              <template #item.dispatch_status="{ item }">
                <v-chip
                  size="small"
                  :color="item.dispatch_status === 'dispatched' ? 'success' : (item.dispatch_status === 'partial' ? 'warning' : 'grey')"
                  variant="tonal"
                  class="font-weight-bold"
                >
                  {{ item.dispatch_status === 'dispatched' ? 'مرحل بالكامل ✓' : (item.dispatch_status === 'partial' ? 'ترحيل جزئي' : 'غير مرحل') }}
                </v-chip>
              </template>

              <template #item.actions="{ item }">
                <div class="d-flex align-center justify-center gap-2">
                  <v-btn
                    size="small"
                    color="primary"
                    variant="flat"
                    rounded="lg"
                    class="font-weight-bold px-3"
                    prepend-icon="mdi-clipboard-list-outline"
                    @click="openExamRoster(item)"
                  >
                    فتح كشف الدرجات
                  </v-btn>
                </div>
              </template>
            </v-data-table>
          </v-window-item>
        </v-window>
      </div>
    </div>

    <!-- ── 3. DETAIL VIEW: كشف رصد درجات الطلاب والترحيل للكنترول ── -->
    <div v-else class="detail-view-container">
      <!-- شريط التنقل الهيكلي ومحدد الاختبار والعمليات (Breadcrumb & Detail Header) -->
      <div class="main-card pa-4 rounded-2xl mb-4 bg-surface border elevation-1">
        <div class="d-flex align-center justify-space-between flex-wrap gap-3">
          <!-- زر العودة والمسار -->
          <div class="d-flex align-center gap-3 flex-wrap">
            <v-btn
              color="primary"
              variant="tonal"
              rounded="lg"
              class="font-weight-bold"
              prepend-icon="mdi-arrow-right"
              @click="returnToMaster"
            >
              العودة للهيكل الإداري
            </v-btn>

            <v-divider vertical class="mx-1" />

            <div class="d-flex align-center gap-2 flex-wrap text-caption font-weight-bold text-medium-emphasis">
              <span class="text-on-surface font-weight-black">
                {{ institutionType === 'university' ? 'التعليم الجامعي' : (institutionType === 'institute' ? 'التعليم الفني' : 'التعليم العام') }}
              </span>
              <template v-if="selectedOfficeObj">
                <v-icon size="14">mdi-chevron-left</v-icon>
                <span class="text-primary">{{ selectedOfficeObj.office_name || selectedOfficeObj.name_ar }}</span>
              </template>
              <template v-if="selectedDirectorateObj">
                <v-icon size="14">mdi-chevron-left</v-icon>
                <span class="text-teal font-weight-bold">{{ selectedDirectorateObj.name || selectedDirectorateObj.name_ar }}</span>
              </template>
              <template v-if="filterOrganization">
                <v-icon size="14">mdi-chevron-left</v-icon>
                <span class="text-indigo font-weight-bold">{{ filterOrganization }}</span>
              </template>
              <v-icon size="14">mdi-chevron-left</v-icon>
              <span class="text-primary font-weight-black">{{ selectedExamObj?.title }}</span>
            </div>
          </div>

          <!-- اختيار الاختبار والأزرار -->
          <div class="d-flex align-center gap-2 flex-wrap">
            <v-autocomplete
              v-model="selectedExamId"
              :items="examsList"
              item-title="title"
              item-value="id"
              label="الاختبار المعروض"
              density="compact"
              variant="outlined"
              hide-details
              style="min-width: 280px;"
              @update:model-value="onExamChange"
            />

            <!-- زر ترحيل الدرجات للكنترول -->
            <v-btn
              color="success"
              size="small"
              rounded="lg"
              class="font-weight-bold px-4"
              prepend-icon="mdi-send-check"
              :loading="dispatchingLoading"
              :disabled="activeExamStats.completed_count === 0 || activeExamStats.is_fully_dispatched"
              @click="openDispatchDialog"
            >
              ترحيل الدرجات للكنترول
            </v-btn>

            <!-- زر إلغاء الترحيل (إذا تم ترحيله مسبقاً) -->
            <v-btn
              v-if="activeExamStats.dispatched_count > 0"
              color="warning"
              variant="tonal"
              size="small"
              rounded="lg"
              class="font-weight-bold px-3"
              prepend-icon="mdi-undo-variant"
              :loading="rollbackLoading"
              @click="confirmRollbackDispatch"
            >
              إلغاء الترحيل
            </v-btn>

            <!-- قائمة التصدير والتقارير -->
            <v-menu transition="slide-y-transition" location="bottom end">
              <template v-slot:activator="{ props }">
                <v-btn
                  v-bind="props"
                  color="primary"
                  variant="tonal"
                  size="small"
                  rounded="lg"
                  class="font-weight-bold px-3"
                  append-icon="mdi-chevron-down"
                  prepend-icon="mdi-printer-outline"
                >
                  خيارات الكشف والتصدير
                </v-btn>
              </template>
              <v-list density="compact" rounded="lg" elevation="6" class="py-1">
                <v-list-item prepend-icon="mdi-file-excel-outline" title="تصدير كشف الكنترول (Excel/CSV)" @click="exportToExcel" />
                <v-list-item prepend-icon="mdi-printer-outline" title="طباعة كشف الكنترول الرسمي" @click="printRosterSheet" />
                <v-divider class="my-1" />
                <v-list-item prepend-icon="mdi-chart-bell-curve-cumulative" title="التحليل السيكومتري (Item Analysis)" :disabled="!selectedExamId" @click="openPsychometricsDialog" />
              </v-list>
            </v-menu>
          </div>
        </div>
      </div>

      <!-- شريط تصفية نتائج الطلاب (البحث والنموذج والحالة والتقدير) -->
      <div class="main-card pa-3 px-4 rounded-2xl mb-4 bg-surface border">
        <v-row dense class="align-center">
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="searchQuery"
              placeholder="بحث بالاسم أو رقم الجلوس أو السري..."
              prepend-inner-icon="mdi-magnify"
              density="compact"
              variant="outlined"
              hide-details
              clearable
              @update:model-value="onSearchInput"
              @keydown.enter="applyFilters"
              @click:clear="onClearSearch"
            />
          </v-col>

          <v-col cols="6" sm="3" md="2">
            <v-select
              v-model="filterVersion"
              :items="versionFilterOptions"
              item-title="text"
              item-value="value"
              placeholder="النموذج"
              prepend-inner-icon="mdi-file-document-multiple-outline"
              density="compact"
              variant="outlined"
              hide-details
              @update:model-value="applyFilters"
            />
          </v-col>

          <v-col cols="6" sm="3" md="2">
            <v-select
              v-model="filterGrade"
              :items="gradeFilterOptions"
              item-title="text"
              item-value="value"
              placeholder="التقدير الأكاديمي"
              prepend-inner-icon="mdi-medal-outline"
              density="compact"
              variant="outlined"
              hide-details
              @update:model-value="applyFilters"
            />
          </v-col>

          <v-col cols="6" sm="3" md="2">
            <v-select
              v-model="filterStatus"
              :items="statusFilterOptions"
              item-title="text"
              item-value="value"
              placeholder="حالة التصحيح"
              prepend-inner-icon="mdi-filter-check-outline"
              density="compact"
              variant="outlined"
              hide-details
              @update:model-value="applyFilters"
            />
          </v-col>

          <v-col cols="6" sm="3" md="2">
            <v-select
              v-model="filterDispatch"
              :items="dispatchFilterOptions"
              item-title="text"
              item-value="value"
              placeholder="حالة الكنترول"
              prepend-inner-icon="mdi-shield-check-outline"
              density="compact"
              variant="outlined"
              hide-details
              @update:model-value="applyFilters"
            />
          </v-col>
        </v-row>
      </div>


    <!-- ── Student Gradebook Table (Component with Server-Side Pagination) ── -->
    <div class="main-card rounded-2xl overflow-hidden mb-6 elevation-1">
      <!-- ── شريط إدارة التحديد والتحكم والعمليات الموحد في الكشف ── -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-3 px-4 py-3 bg-surface border-b">
        <!-- قسم التحديد والطلاب -->
        <div class="d-flex align-center gap-3 flex-wrap">
          <v-checkbox-btn
            :model-value="isAllCurrentSelected"
            :indeterminate="isSomeCurrentSelected"
            color="primary"
            density="compact"
            hide-details
            @update:model-value="toggleSelectAllCurrent"
          />
          <span class="text-caption font-weight-bold text-on-surface">
            تحديد الكل
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

          <!-- زر ترحيل درجات الطلاب المحددين فقط عند اختيارهم -->
          <v-btn
            v-if="selectedStudentIds.length > 0"
            color="purple-darken-1"
            variant="flat"
            size="small"
            class="font-weight-bold text-white rounded-lg px-3"
            prepend-icon="mdi-bank-transfer"
            :loading="dispatchingLoading"
            @click="dispatchSelectedToControl"
          >
            ترحيل المحدد ({{ selectedStudentIds.length }})
          </v-btn>

          <span class="text-caption text-medium-emphasis">
            ({{ tableItems.pagination?.total || tableItems.pagination?.count || totalRecordsCount }} طالب مسجل)
          </span>
        </div>

        <!-- إجراءات تحديث الكشف -->
        <div class="d-flex align-center gap-2" v-if="selectedExamObj">
          <v-btn
            icon="mdi-refresh"
            variant="text"
            size="small"
            color="medium-emphasis"
            title="إعادة تحميل الكشف"
            :loading="loadingRecords"
            @click="fetchGradebookRoster({ params: { page: 1 } })"
          />
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
                size="small"
                color="primary"
                variant="tonal"
                class="font-weight-bold px-2 rounded-lg"
                prepend-icon="mdi-file-eye-outline"
                title="معاينة وتدقيق ورقة الإجابة والتفاصيل"
                @click.stop="navigateToSubmission(item)"
              >
                معاينة الورقة
              </v-btn>
              <v-btn
                v-else
                size="small"
                color="secondary"
                variant="tonal"
                class="font-weight-bold px-2 rounded-lg"
                prepend-icon="mdi-card-account-details-outline"
                title="عرض تفاصيل سجل قيد الطالب بالاختبار"
                @click.stop="openStudentRecordModal(item)"
              >
                تفاصيل السجل
              </v-btn>
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>
    </div> <!-- end detail-view-container -->

    <!-- ── نافذة تفاصيل سجل الطالب في الاختبار (عند عدم وجود ورقة مصححة) ── -->
    <v-dialog v-model="studentRecordDialog" max-width="560">
      <v-card class="rounded-2xl pa-5 main-card" v-if="selectedStudentRecord">
        <div class="d-flex align-center justify-space-between mb-4">
          <div class="d-flex align-center gap-3">
            <v-avatar color="primary" variant="tonal" size="44" rounded="lg">
              <v-icon size="24" color="primary">mdi-account-school-outline</v-icon>
            </v-avatar>
            <div>
              <h3 class="text-h6 font-weight-black mb-0">{{ selectedStudentRecord.student_name }}</h3>
              <p class="text-caption text-medium-emphasis mb-0">بيانات القيد والتسجيل في الاختبار</p>
            </div>
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" @click="studentRecordDialog = false" />
        </div>

        <v-list density="compact" class="bg-surface rounded-xl border pa-2 mb-4">
          <v-list-item title="رقم الجلوس" :subtitle="selectedStudentRecord.seat_number || '—'">
            <template #prepend><v-icon color="primary" class="me-2">mdi-numeric</v-icon></template>
          </v-list-item>
          <v-list-item title="الرقم السري" :subtitle="selectedStudentRecord.secret_number || '—'">
            <template #prepend><v-icon color="secondary" class="me-2">mdi-shield-key-outline</v-icon></template>
          </v-list-item>
          <v-list-item title="النموذج المخصص" :subtitle="`النموذج (${selectedStudentRecord.version_code || 'A'})`">
            <template #prepend><v-icon color="indigo" class="me-2">mdi-file-document-multiple-outline</v-icon></template>
          </v-list-item>
          <v-list-item title="المدرسة / المؤسسة" :subtitle="selectedStudentRecord.school_name || '—'">
            <template #prepend><v-icon color="teal" class="me-2">mdi-domain</v-icon></template>
          </v-list-item>
          <v-list-item title="المديرية / المحافظة" :subtitle="`${selectedStudentRecord.directorate_name || ''} - ${selectedStudentRecord.governorate_name || ''}`">
            <template #prepend><v-icon color="orange" class="me-2">mdi-map-marker-outline</v-icon></template>
          </v-list-item>
          <v-list-item title="حالة التصحيح" subtitle="لم يتم مسح وتصحيح ورقة إجابة لهذا الطالب بعد (حالة الطالب: غائب)">
            <template #prepend><v-icon color="error" class="me-2">mdi-alert-circle-outline</v-icon></template>
          </v-list-item>
        </v-list>

        <v-card-actions class="px-0 pt-2 d-flex justify-end gap-2">
          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            class="font-weight-bold px-4"
            prepend-icon="mdi-scanner"
            @click="goToScannerLabForStudent"
          >
            الانتقال لمعمل المسح الضوئي
          </v-btn>
          <v-btn
            variant="tonal"
            rounded="lg"
            class="font-weight-bold"
            @click="studentRecordDialog = false"
          >
            إغلاق
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
import api from '@/services/api'
import { gradebookAPI, examsAPI } from '@/services/omr/endpoints'
import OMRWorkflowBar from '@/components/OMRWorkflowBar.vue'

export default {
  name: 'OMRGradebookView',

  components: {
    OMRWorkflowBar,
  },

  data() {
    return {
      institutionType: 'school', // 'school' | 'university' | 'institute'
      currentView: 'master', // 'master' | 'detail'
      masterTab: 'offices',  // 'offices' | 'directorates' | 'schools' | 'exams'
      loadingMaster: false,
      masterSearchQuery: '',
      masterInstitutionType: 'all',

      educationalOrgs: [],
      officesList: [],
      directoratesList: [],
      schoolsList: [],

      selectedOfficeId: null,
      selectedDirectorateId: null,
      selectedSchoolId: null,

      officeMasterHeaders: [
        { title: "مكتب التربية والتعليم (المحافظة)", key: "office_name", sortable: true, align: "start" },
        { title: "المديريات", key: "directorates_count", sortable: true, align: "center", width: "110px" },
        { title: "المدارس / المراكز", key: "schools_count", sortable: true, align: "center", width: "130px" },
        { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "110px" },
        { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "120px" },
        { title: "أوراق مصححة", key: "completed_count", sortable: true, align: "center", width: "120px" },
        { title: "نسبة الإنجاز", key: "completion_rate", sortable: true, align: "center", width: "140px" },
        { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "230px" },
      ],

      directorateMasterHeaders: [
        { title: "إدارة التربية والتعليم (المديرية)", key: "name", sortable: true, align: "start" },
        { title: "المكتب التابع له (المحافظة)", key: "office_name", sortable: true, align: "center", width: "180px" },
        { title: "المدارس / المراكز", key: "schools_count", sortable: true, align: "center", width: "130px" },
        { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "110px" },
        { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "120px" },
        { title: "أوراق مصححة", key: "completed_count", sortable: true, align: "center", width: "120px" },
        { title: "نسبة الإنجاز", key: "completion_rate", sortable: true, align: "center", width: "140px" },
        { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "230px" },
      ],

      schoolMasterHeaders: [
        { title: "المدرسة / المركز الامتحاني / المؤسسة", key: "school_name", sortable: true, align: "start" },
        { title: "نوع المؤسسة", key: "institution_type", sortable: true, align: "center", width: "110px" },
        { title: "المحافظة والمديرية", key: "directorate_name", sortable: true, align: "center", width: "160px" },
        { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "100px" },
        { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
        { title: "أوراق مصححة", key: "completed_count", sortable: true, align: "center", width: "110px" },
        { title: "نسبة الإنجاز", key: "completion_rate", sortable: true, align: "center", width: "125px" },
        { title: "متوسط الدرجات", key: "average_score", sortable: true, align: "center", width: "110px" },
        { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "140px" },
      ],

      examMasterHeaders: [
        { title: "اسم الاختبار والمادة", key: "exam_title", sortable: true, align: "start" },
        { title: "النطاق الإداري / المكاتب", key: "geo_info", sortable: true, align: "center", width: "180px" },
        { title: "المراكز / المدارس", key: "schools_count", sortable: true, align: "center", width: "130px" },
        { title: "المقيدون", key: "total_students", sortable: true, align: "center", width: "100px" },
        { title: "أوراق مصححة", key: "completed_count", sortable: true, align: "center", width: "110px" },
        { title: "نسبة التصحيح", key: "completion_rate", sortable: true, align: "center", width: "125px" },
        { title: "حالة الكنترول", key: "dispatch_status", sortable: true, align: "center", width: "130px" },
        { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "140px" },
      ],


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

      studentRecordDialog: false,
      selectedStudentRecord: null,

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
        { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "135px" },
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
    realOfficesList() {
      return (this.educationalOrgs || []).filter(o => o.company_level === 30)
    },

    realDirectoratesList() {
      if (this.selectedOfficeId) {
        return (this.educationalOrgs || []).filter(o => o.company_level === 40 && o.fk_parent_organization === this.selectedOfficeId)
      }
      return (this.educationalOrgs || []).filter(o => o.company_level === 40)
    },

    realSchoolsList() {
      if (this.selectedDirectorateId) {
        return (this.educationalOrgs || []).filter(o => o.company_level === 50 && o.fk_parent_organization === this.selectedDirectorateId)
      }
      if (this.selectedOfficeId) {
        const dirIds = this.realDirectoratesList.map(d => d.id)
        return (this.educationalOrgs || []).filter(o => o.company_level === 50 && dirIds.includes(o.fk_parent_organization))
      }
      return (this.educationalOrgs || []).filter(o => o.company_level === 50)
    },

    selectedOfficeObj() {
      if (!this.selectedOfficeId) return null
      return (this.realOfficesList || []).find(o => o.id === this.selectedOfficeId) || (this.officesList || []).find(o => o.id === this.selectedOfficeId) || null
    },

    selectedDirectorateObj() {
      if (!this.selectedDirectorateId) return null
      return (this.realDirectoratesList || []).find(d => d.id === this.selectedDirectorateId) || (this.directoratesList || []).find(d => d.id === this.selectedDirectorateId) || null
    },

    filteredOfficesTable() {
      let list = this.officesList || []
      if (this.selectedOfficeId) {
        list = list.filter(o => o.id === this.selectedOfficeId)
      }
      if (this.masterSearchQuery && this.masterSearchQuery.trim()) {
        const q = this.masterSearchQuery.trim().toLowerCase()
        list = list.filter(o => (o.office_name || '').toLowerCase().includes(q) || (o.governorate_name || '').toLowerCase().includes(q))
      }
      return list
    },

    filteredDirectoratesTable() {
      let list = this.directoratesList || []
      if (this.selectedOfficeId) {
        list = list.filter(d => d.office_id === this.selectedOfficeId)
      }
      if (this.selectedDirectorateId) {
        list = list.filter(d => d.id === this.selectedDirectorateId)
      }
      if (this.masterSearchQuery && this.masterSearchQuery.trim()) {
        const q = this.masterSearchQuery.trim().toLowerCase()
        list = list.filter(d => (d.name || '').toLowerCase().includes(q) || (d.office_name || '').toLowerCase().includes(q))
      }
      return list
    },

    filteredSchoolsTable() {
      let list = this.schoolsList || []
      if (this.selectedSchoolId) {
        list = list.filter(s => s.id === this.selectedSchoolId)
      }
      if (this.masterSearchQuery && this.masterSearchQuery.trim()) {
        const q = this.masterSearchQuery.trim().toLowerCase()
        list = list.filter(s => (s.name || '').toLowerCase().includes(q) || (s.directorate_name || '').toLowerCase().includes(q))
      }
      return list
    },

    filteredExamsTable() {
      let list = this.examsList || []
      if (this.institutionType && this.institutionType !== 'all') {
        list = list.filter(e => e.institution_type === this.institutionType)
      }
      if (this.masterSearchQuery && this.masterSearchQuery.trim()) {
        const q = this.masterSearchQuery.trim().toLowerCase()
        list = list.filter(e => {
          const title = (e.title || '').toLowerCase()
          const code = (e.uniqueCode || '').toLowerCase()
          const subj = (e.subject_name || '').toLowerCase()
          return title.includes(q) || code.includes(q) || subj.includes(q)
        })
      }
      return list
    },


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
    await this.loadEducationalHierarchy()
    await this.refreshMasterData()

    const queryExam = this.$route.query.exam || this.$route.query.open_exam_id
    if (queryExam) {
      this.selectedExamId = parseInt(queryExam) || queryExam
      this.selectedExamObj = this.examsList.find(e => e.id === this.selectedExamId) || null
      this.currentView = 'detail'
      await this.fetchGradebookRoster({ params: { page: 1, page_size: 10 } })
    } else {
      this.currentView = 'master'
    }
  },

  methods: {
    notify(text, color = 'success') {
      this.snackbar.text = text
      this.snackbar.color = color
      this.snackbar.show = true
    },

    refreshCurrentView() {
      if (this.currentView === 'master') {
        this.refreshMasterData()
      } else {
        this.fetchGradebookRoster({ params: { page: 1, page_size: 10 } })
      }
    },

    async loadEducationalHierarchy() {
      try {
        const res = await api.get('/api/exams/distributions/educational-hierarchy/')
        this.educationalOrgs = res.data?.data || []
      } catch (err) {
        console.error('Error fetching educational hierarchy:', err)
      }
    },

    async refreshMasterData() {
      this.loadingMaster = true
      try {
        const params = { institution_type: this.institutionType }
        if (this.selectedOfficeId) params.office_id = this.selectedOfficeId
        if (this.selectedDirectorateId) params.directorate_id = this.selectedDirectorateId
        if (this.selectedSchoolId) params.school_id = this.selectedSchoolId

        const promises = [
          this.fetchExamsList(params),
          gradebookAPI.getBySchool(params).then(res => { this.schoolsList = res.data?.results || [] }),
        ]
        if (this.institutionType === 'school') {
          promises.push(
            gradebookAPI.getByOffice().then(res => { this.officesList = res.data?.results || [] }),
            gradebookAPI.getByDirectorate({ office_id: this.selectedOfficeId || undefined }).then(res => { this.directoratesList = res.data?.results || [] })
          )
        }
        await Promise.all(promises)
      } catch (err) {
        console.error('Error refreshing master data:', err)
      } finally {
        this.loadingMaster = false
      }
    },

    onSectorChange(val) {
      this.institutionType = val
      this.selectedOfficeId = null
      this.selectedDirectorateId = null
      this.selectedSchoolId = null
      if (val === 'school') {
        this.masterTab = 'offices'
      } else {
        this.masterTab = 'schools'
      }
      this.refreshMasterData()
    },

    onOfficeFilterChange(val) {
      this.selectedOfficeId = val
      this.selectedDirectorateId = null
      this.selectedSchoolId = null
      this.refreshMasterData()
    },

    onDirectorateFilterChange(val) {
      this.selectedDirectorateId = val
      this.selectedSchoolId = null
      this.refreshMasterData()
    },

    onSchoolFilterChange(val) {
      this.selectedSchoolId = val
      this.refreshMasterData()
    },

    drillDownToOffice(item) {
      if (!item || !item.id) return
      this.selectedOfficeId = item.id
      this.masterTab = 'directorates'
      this.refreshMasterData()
    },

    drillDownToDirectorate(item) {
      if (!item || !item.id) return
      this.selectedDirectorateId = item.id
      this.masterTab = 'schools'
      this.refreshMasterData()
    },

    async openOfficeRoster(item) {
      if (!item || !item.id) return
      this.selectedOfficeId = item.id
      this.selectedDirectorateId = null
      this.selectedSchoolId = null
      this.resetFilterSelections()
      this.selectedStudentIds = []

      // جلب الاختبارات الخاصة بهذا المكتب فقط
      const offExams = await this.fetchExamsList({ office_id: item.id })
      if (offExams && offExams.length > 0) {
        this.selectedExamId = offExams[0].id
        this.selectedExamObj = offExams[0]
      } else {
        this.selectedExamId = null
        this.selectedExamObj = null
      }
      this.currentView = 'detail'
      await this.fetchGradebookRoster({ params: { page: 1, page_size: 10, office_id: item.id } })
    },

    async openDirectorateRoster(item) {
      if (!item || !item.id) return
      this.selectedDirectorateId = item.id
      this.selectedSchoolId = null
      if (item.office_id) {
        this.selectedOfficeId = item.office_id
      }
      this.resetFilterSelections()
      this.selectedStudentIds = []

      // جلب الاختبارات الخاصة بهذه المديرية فقط
      const dirExams = await this.fetchExamsList({ directorate_id: item.id })
      if (dirExams && dirExams.length > 0) {
        this.selectedExamId = dirExams[0].id
        this.selectedExamObj = dirExams[0]
      } else {
        this.selectedExamId = null
        this.selectedExamObj = null
      }
      this.currentView = 'detail'
      await this.fetchGradebookRoster({ params: { page: 1, page_size: 10, directorate_id: item.id } })
    },

    async openExamRoster(item) {
      if (!item || !item.id) return
      this.selectedExamId = item.id
      this.selectedExamObj = item
      this.currentView = 'detail'
      this.resetFilterSelections()
      this.selectedStudentIds = []
      await this.fetchGradebookRoster({ params: { page: 1, page_size: 10 } })
    },

    async openSchoolRoster(item) {
      if (!item) return
      this.selectedSchoolId = item.id
      this.selectedDirectorateId = null
      this.selectedOfficeId = null
      this.resetFilterSelections()
      this.filterOrganization = item.name
      this.selectedStudentIds = []

      // جلب الاختبارات الخاصة بهذه المدرسة فقط
      const schoolExams = await this.fetchExamsList({ school_id: item.id })
      if (schoolExams && schoolExams.length > 0) {
        this.selectedExamId = schoolExams[0].id
        this.selectedExamObj = schoolExams[0]
      } else {
        this.selectedExamId = null
        this.selectedExamObj = null
      }
      this.currentView = 'detail'
      await this.fetchGradebookRoster({ params: { page: 1, page_size: 10, school: item.name, school_id: item.id } })
    },

    returnToMaster() {
      this.currentView = 'master'
      this.selectedOfficeId = null
      this.selectedDirectorateId = null
      this.selectedSchoolId = null
      this.filterOrganization = null
      this.resetFilterSelections()
      this.fetchExamsList()
      this.refreshMasterData()
    },


    async fetchExamsList(customParams = null) {
      this.loadingExams = true
      try {
        const params = customParams || { institution_type: this.institutionType }
        if (this.selectedOfficeId && !params.office_id) params.office_id = this.selectedOfficeId
        if (this.selectedDirectorateId && !params.directorate_id) params.directorate_id = this.selectedDirectorateId
        if (this.selectedSchoolId && !params.school_id) params.school_id = this.selectedSchoolId

        const res = await gradebookAPI.list(params)
        const data = res.data
        if (data && data.results) {
          this.examsList = data.results
        } else if (Array.isArray(data)) {
          this.examsList = data
        }

        // Auto select first exam only if currently in detail view and no exam is selected
        if (this.currentView === 'detail' && !this.selectedExamId && this.examsList.length > 0) {
          this.selectedExamId = this.examsList[0].id
          await this.fetchGradebookRoster({ params: { page: 1, page_size: 10 } })
        }
        return this.examsList
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
          if (this.currentView === 'detail' && this.examsList.length > 0 && !this.selectedExamId) {
            this.selectedExamId = this.examsList[0].id
            await this.fetchGradebookRoster({ params: { page: 1, page_size: 10 } })
          }
          return this.examsList
        } catch (exErr) {
          this.notify('تعذر جلب قائمة الاختبارات', 'error')
          return []
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

    async loadGovernorates() {
      this.loadingGeo = true
      try {
        const res = await api.get('api/common/governorate/all/')
        const data = res.data?.data || res.data?.results || res.data || []
        this.governoratesList = (Array.isArray(data) ? data : []).map(item => ({
          ...item,
          id: item.id,
          name: item.name || item.name_ar || item.name_en || '',
          name_ar: item.name_ar || item.name || '',
        }))
      } catch (err) {
        console.error('Error loading governorates:', err)
      } finally {
        this.loadingGeo = false
      }
    },

    async loadAllDirectorates() {
      try {
        const res = await api.get('api/common/directorate/all/')
        const data = res.data?.data || res.data?.results || res.data || []
        this.allDirectoratesList = (Array.isArray(data) ? data : []).map(item => ({
          ...item,
          id: item.id,
          name: item.name || item.name_ar || item.name_en || '',
          name_ar: item.name_ar || item.name || '',
          fk_governorate: item.fk_governorate,
        }))
      } catch (err) {
        console.error('Error loading directorates:', err)
      }
    },

    async loadAllOrganizations() {
      await this.loadOrganizationsForScope()
    },

    async loadOrganizationsForScope() {
      try {
        const params = []
        if (this.selectedGovernorates && this.selectedGovernorates.length > 0) {
          params.push(`governorate=${this.selectedGovernorates.join(',')}`)
        }
        if (this.selectedDirectorates && this.selectedDirectorates.length > 0) {
          params.push(`directorate=${this.selectedDirectorates.join(',')}`)
        }
        const qs = params.length > 0 ? `?${params.join('&')}` : ''
        const res = await api.get(`api/academic/organizations/all/${qs}`)
        const data = res.data?.data || res.data?.results || res.data || []
        this.allOrganizationsList = (Array.isArray(data) ? data : []).map(item => ({
          ...item,
          id: item.id,
          name_ar: item.name_ar || item.name || '',
          name_en: item.name_en || '',
        }))
      } catch (err) {
        console.error('Error loading organizations for scope:', err)
      }
    },

    async onGovernoratesChange() {
      // Clear directorates and schools that do not belong to the selected governorates
      if (this.selectedGovernorates && this.selectedGovernorates.length > 0) {
        this.selectedDirectorates = (this.selectedDirectorates || []).filter(dirId => {
          const dir = this.allDirectoratesList.find(d => d.id === dirId)
          return dir && this.selectedGovernorates.includes(dir.fk_governorate)
        })
      } else {
        this.selectedDirectorates = []
      }
      this.selectedSchools = []
      await this.loadOrganizationsForScope()
      this.applyFilters()
    },

    async onDirectoratesChange() {
      this.selectedSchools = []
      await this.loadOrganizationsForScope()
      this.applyFilters()
    },

    onSchoolsChange() {
      this.applyFilters()
    },

    async clearGeoFilters() {
      this.selectedGovernorates = []
      this.selectedDirectorates = []
      this.selectedSchools = []
      await this.loadOrganizationsForScope()
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
      this.selectedGovernorates = []
      this.selectedDirectorates = []
      this.selectedSchools = []
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
      if (this.selectedGovernorates && this.selectedGovernorates.length > 0) {
        queryParams.governorate = this.selectedGovernorates.join(',')
      } else if (this.filterGovernorate && this.filterGovernorate !== 'all') {
        queryParams.governorate = this.filterGovernorate
      }

      if (this.selectedDirectorates && this.selectedDirectorates.length > 0) {
        queryParams.directorate = this.selectedDirectorates.join(',')
      } else if (this.filterDirectorate && this.filterDirectorate !== 'all') {
        queryParams.directorate = this.filterDirectorate
      }

      if (this.selectedSchools && this.selectedSchools.length > 0) {
        queryParams.school = this.selectedSchools.join(',')
      } else if (this.filterOrganization && this.filterOrganization !== 'all') {
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
      if (this.selectedOfficeId) {
        queryParams.office_id = this.selectedOfficeId
      }
      if (this.selectedDirectorateId) {
        queryParams.directorate_id = this.selectedDirectorateId
      }
      if (this.selectedSchoolId) {
        queryParams.school_id = this.selectedSchoolId
      }
      if (this.filterDispatch && this.filterDispatch !== 'all') {
        queryParams.dispatch = this.filterDispatch
      }
      return queryParams
    },

    async fetchGradebookRoster(tableParams = null) {
      if (!this.selectedExamId) {
        this.tableItems = { results: [], pagination: { count: 0, num_pages: 1, current_page: 1, page_size: 10, total: 0 } }
        return Promise.resolve(this.tableItems)
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
        return Promise.resolve(this.tableItems)
      } catch (err) {
        console.error('Error loading gradebook roster from backend:', err)
        this.notify('تعذر تحميل كشف درجات الاختبار', 'error')
        return Promise.resolve(this.tableItems)
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

    navigateToSubmission(item) {
      if (item && item.submission_id) {
        this.$router.push(`/omr-submissions/${item.submission_id}`)
      } else {
        this.openStudentRecordModal(item)
      }
    },

    openStudentRecordModal(item) {
      this.selectedStudentRecord = item
      this.studentRecordDialog = true
    },

    goToScannerLabForStudent() {
      this.studentRecordDialog = false
      if (this.selectedExamId) {
        this.$router.push(`/omr-scanner-lab?examId=${this.selectedExamId}`)
      } else {
        this.$router.push('/omr-scanner-lab')
      }
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
