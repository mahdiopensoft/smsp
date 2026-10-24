<template>
  <div class="qb-omr-print-registry pa-4 pa-md-6">
    <!-- ── Page Header ─────────────────────────────────────────── -->
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
          v-if="currentView === 'detail'"
          color="secondary"
          variant="tonal"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-view-dashboard-outline"
          @click="returnToMaster"
        >
          عرض الهيكل وسجل الطباعة
        </v-btn>
        <v-btn
          v-else
          color="primary"
          variant="flat"
          rounded="lg"
          class="font-weight-bold shadow-sm"
          prepend-icon="mdi-printer-outline"
          @click="currentView = 'detail'"
        >
          استوديو المعاينة والطباعة المباشر
        </v-btn>
        <v-btn
          color="secondary"
          variant="tonal"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-refresh"
          :loading="loadingMaster || loadingBatches || loadingExams"
          @click="refreshData"
        >
          تحديث البيانات
        </v-btn>
      </div>
    </div>

    <!-- ── OMR Workflow Stepper (المرحلة 2: طباعة أوراق الإجابة) ── -->
    <omr-workflow-bar :active-step="2" />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 1. MASTER VIEW: الهيكل الإداري وسجل الطباعة المركزي             -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <div v-if="currentView === 'master'" class="master-view-container">
      <!-- 1. Sector Switcher (فصل نوع المؤسسة التعليمية بشكل قاطع) -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-4">
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

        <div class="d-flex align-center gap-2">
          <v-btn
            color="primary"
            variant="flat"
            size="small"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-printer-eye"
            @click="currentView = 'detail'"
          >
            استوديو الطباعة المباشر
          </v-btn>
          <v-btn
            variant="tonal"
            color="secondary"
            size="small"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-refresh"
            :loading="loadingMaster"
            @click="loadMasterData"
          >
            تحديث السجل
          </v-btn>
        </div>
      </div>



      <!-- 3. شريط التصفية الهيكلي الموحد (مرتب وبدون تكرار) -->
      <div class="main-card pa-4 rounded-2xl mb-4 bg-surface border elevation-1">
        <v-row dense class="align-center">
          <!-- التعليم العام (مدرسي) -->
          <template v-if="institutionType === 'school'">
            <v-col cols="12" md="4">
              <v-autocomplete
                v-model="selectedOfficeId"
                :items="officesList"
                item-title="office_name"
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

            <v-col cols="12" md="4">
              <v-autocomplete
                v-model="selectedDirectorateId"
                :items="directoratesOptions"
                item-title="name"
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

            <v-col cols="12" md="4">
              <v-autocomplete
                v-model="selectedSchoolId"
                :items="schoolsOptions"
                item-title="name"
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
                :items="schoolsOptions"
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
                :items="schoolsOptions"
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

      <!-- 4. تبويبات الاستعراض الهيكلي وسجل الطباعة المركزي (Master Tabs) -->
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
              الاختبارات المعتمدة للطباعة ({{ filteredMasterExamsTable.length }})
            </v-tab>
            <v-tab value="registry" class="font-weight-bold">
              <v-icon start size="18">mdi-history</v-icon>
              سجل الدفعات المطبوعة ({{ filteredBatchesTable.length }})
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

              <template #item.printed_count="{ item }">
                <span class="font-weight-bold text-primary">{{ item.printed_count || 0 }} ورقة</span>
              </template>

              <template #item.printed_rate="{ item }">
                <div class="d-flex align-center gap-2">
                  <v-progress-linear
                    :model-value="item.printed_rate || 0"
                    :color="(item.printed_rate >= 100) ? 'success' : (item.printed_rate > 0 ? 'warning' : 'primary')"
                    height="8"
                    rounded
                    class="flex-grow-1"
                  />
                  <span class="text-caption font-weight-bold">{{ item.printed_rate || 0 }}%</span>
                </div>
              </template>

              <template #item.print_status="{ item }">
                <v-chip size="x-small" :color="(item.printed_rate >= 100 || item.print_status === 'full') ? 'success' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'warning' : 'grey')" variant="tonal" class="font-weight-bold">
                  {{ (item.printed_rate >= 100 || item.print_status === 'full') ? 'مكتمل الطباعة' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'طباعة جزئية' : 'لم يطبع بعد') }}
                </v-chip>
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
                    prepend-icon="mdi-printer-outline"
                    @click="openOfficeStudio(item)"
                  >
                    استوديو الطباعة
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

              <template #item.printed_count="{ item }">
                <span class="font-weight-bold text-teal">{{ item.printed_count || 0 }} ورقة</span>
              </template>

              <template #item.printed_rate="{ item }">
                <div class="d-flex align-center gap-2">
                  <v-progress-linear
                    :model-value="item.printed_rate || 0"
                    :color="(item.printed_rate >= 100) ? 'success' : (item.printed_rate > 0 ? 'warning' : 'teal')"
                    height="8"
                    rounded
                    class="flex-grow-1"
                  />
                  <span class="text-caption font-weight-bold">{{ item.printed_rate || 0 }}%</span>
                </div>
              </template>

              <template #item.print_status="{ item }">
                <v-chip size="x-small" :color="(item.printed_rate >= 100 || item.print_status === 'full') ? 'success' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'warning' : 'grey')" variant="tonal" class="font-weight-bold">
                  {{ (item.printed_rate >= 100 || item.print_status === 'full') ? 'مكتمل الطباعة' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'طباعة جزئية' : 'لم يطبع بعد') }}
                </v-chip>
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
                    المراكز والمدارس
                  </v-btn>
                  <v-btn
                    size="small"
                    color="teal"
                    variant="flat"
                    rounded="lg"
                    class="font-weight-bold"
                    prepend-icon="mdi-printer-outline"
                    @click="openDirectorateStudio(item)"
                  >
                    استوديو الطباعة
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
              <template #item.name="{ item }">
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

              <template #item.printed_count="{ item }">
                <span class="font-weight-bold text-indigo">{{ item.printed_count || 0 }} ورقة</span>
              </template>

              <template #item.printed_rate="{ item }">
                <div class="d-flex align-center gap-2">
                  <v-progress-linear
                    :model-value="item.printed_rate || 0"
                    :color="(item.printed_rate >= 100) ? 'success' : (item.printed_rate > 0 ? 'warning' : 'indigo')"
                    height="8"
                    rounded
                    class="flex-grow-1"
                  />
                  <span class="text-caption font-weight-bold">{{ item.printed_rate || 0 }}%</span>
                </div>
              </template>

              <template #item.print_status="{ item }">
                <v-chip size="x-small" :color="(item.printed_rate >= 100 || item.print_status === 'full') ? 'success' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'warning' : 'grey')" variant="tonal" class="font-weight-bold">
                  {{ (item.printed_rate >= 100 || item.print_status === 'full') ? 'مكتمل الطباعة' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'طباعة جزئية' : 'لم يطبع بعد') }}
                </v-chip>
              </template>

              <template #item.actions="{ item }">
                <div class="d-flex align-center justify-center gap-2">
                  <v-btn
                    size="small"
                    color="primary"
                    variant="flat"
                    rounded="lg"
                    class="font-weight-bold"
                    prepend-icon="mdi-printer-check"
                    @click="openSchoolStudio(item)"
                  >
                    سحب وطباعة أوراق الطلاب
                  </v-btn>
                </div>
              </template>
            </v-data-table>
          </v-window-item>

          <!-- 4. تبويب الاختبارات الأكاديمية -->
          <v-window-item value="exams">
            <v-data-table
              :headers="examMasterHeaders"
              :items="filteredMasterExamsTable"
              :loading="loadingMaster"
              density="comfortable"
              hover
              class="elevation-0"
              no-data-text="لا توجد اختبارات مسجلة في هذا النطاق"
            >
              <template #item.uniqueCode="{ item }">
                <span class="font-mono font-weight-bold text-caption px-2 py-1 rounded bg-grey-lighten-4 border">
                  {{ item.uniqueCode }}
                </span>
              </template>

              <template #item.title="{ item }">
                <div class="py-2">
                  <div class="font-weight-bold text-subtitle-2 text-on-surface">{{ item.title }}</div>
                  <div class="text-caption text-medium-emphasis">المادة: {{ item.subject_name || 'عام' }} • {{ item.directorate_name }}</div>
                </div>
              </template>

              <template #item.printed_count="{ item }">
                <span class="font-weight-bold text-primary">{{ item.printed_count || 0 }} ورقة</span>
              </template>

              <template #item.printed_rate="{ item }">
                <div class="d-flex align-center gap-2">
                  <v-progress-linear
                    :model-value="item.printed_rate || 0"
                    :color="(item.printed_rate >= 100) ? 'success' : (item.printed_rate > 0 ? 'warning' : 'primary')"
                    height="8"
                    rounded
                    class="flex-grow-1"
                  />
                  <span class="text-caption font-weight-bold">{{ item.printed_rate || 0 }}%</span>
                </div>
              </template>

              <template #item.print_status="{ item }">
                <v-chip size="x-small" :color="(item.printed_rate >= 100 || item.print_status === 'full') ? 'success' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'warning' : 'grey')" variant="tonal" class="font-weight-bold">
                  {{ (item.printed_rate >= 100 || item.print_status === 'full') ? 'مكتمل الطباعة' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'طباعة جزئية' : 'لم يطبع بعد') }}
                </v-chip>
              </template>

              <template #item.actions="{ item }">
                <div class="d-flex align-center justify-center gap-2">
                  <v-btn
                    size="small"
                    color="primary"
                    variant="tonal"
                    rounded="lg"
                    class="font-weight-bold"
                    prepend-icon="mdi-printer-eye"
                    @click="openExamStudio(item)"
                  >
                    استوديو الطباعة
                  </v-btn>
                </div>
              </template>
            </v-data-table>
          </v-window-item>

          <!-- 5. تبويب سجل الدفعات المطبوعة العام -->
          <v-window-item value="registry">
            <v-data-table
              :headers="registryMasterHeaders"
              :items="filteredBatchesTable"
              :loading="loadingBatches"
              density="comfortable"
              hover
              class="elevation-0"
              no-data-text="لا توجد دفعات طباعة مسجلة"
            >
              <template #item.batch_id="{ item }">
                <span class="font-mono font-weight-bold text-caption text-primary">
                  {{ item.batch_id }}
                </span>
              </template>

              <template #item.total_sheets="{ item }">
                <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                  {{ item.total_sheets }} ورقة
                </v-chip>
              </template>

              <template #item.actions="{ item }">
                <v-btn
                  size="small"
                  color="secondary"
                  variant="tonal"
                  rounded="lg"
                  class="font-weight-bold"
                  prepend-icon="mdi-eye-outline"
                  @click="viewBatchDetails(item)"
                >
                  تفاصيل الدفعة
                </v-btn>
              </template>
            </v-data-table>
          </v-window-item>
        </v-window>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 2. DETAIL VIEW: استوديو المعاينة وطباعة الوثائق وحزم الاختبار  -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <div v-else class="detail-studio-container">
      <!-- شريط التنقل الهرمي والعودة للهيكل وسياق التصفية -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-4 pa-3 rounded-2xl bg-surface border elevation-1">
        <div class="d-flex align-center gap-2 flex-wrap">
          <v-btn
            color="primary"
            variant="tonal"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-arrow-right"
            @click="returnToMaster"
          >
            العودة للهيكل الإداري وسجل الطباعة
          </v-btn>
          <v-divider vertical class="mx-1" />
          <!-- Breadcrumb trail -->
          <div class="d-flex align-center text-caption font-weight-bold text-medium-emphasis flex-wrap gap-1">
            <span class="text-primary">{{ institutionType === 'university' ? 'التعليم الجامعي' : (institutionType === 'institute' ? 'التعليم الفني' : 'التعليم العام') }}</span>
            <v-icon size="14">mdi-chevron-left</v-icon>
            <span>{{ selectedOfficeName || 'كل المحافظات' }}</span>
            <v-icon size="14">mdi-chevron-left</v-icon>
            <span>{{ selectedDirectorateName || 'كل المديريات' }}</span>
            <template v-if="selectedSchoolName">
              <v-icon size="14">mdi-chevron-left</v-icon>
              <span class="text-primary font-weight-black">{{ selectedSchoolName }}</span>
            </template>
          </div>
        </div>

        <div class="d-flex align-center gap-2">
          <v-chip
            v-if="selectedSchoolName"
            color="info"
            variant="tonal"
            closable
            class="font-weight-bold"
            prepend-icon="mdi-filter-check"
            @click:close="clearSchoolFilter"
          >
            تصفية خاصة بالمدرسة: {{ selectedSchoolName }} ({{ examDetails?.registered_students?.length || 0 }} طالب)
          </v-chip>
        </div>
      </div>

      <!-- ── شريط اختيار وتصفية الاختبار الموحد (Unified Exam Selector & Filters) ── -->
      <filter-fields label="تصفية واختيار الاختبار المطلوب طباعة وثائقه" class="main-card border-0 pa-5 rounded-2xl mb-4">
        <v-row dense class="align-center">
          <!-- 1. نوع المؤسسة التعليمية -->
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
            @update:model-value="fetchExamsList"
          />
          <auto-list
            v-model="filterSubject"
            name="Subject"
            :param="subjectFilterParam"
            placeholder="المادة الدراسية"
            :cols="filterInstitutionType === 'school' ? '3' : '3'"
            :add="false"
            @update:model-value="fetchExamsList"
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

        <!-- فلاتر المعاهد -->
        <template v-if="filterInstitutionType === 'institute'">
          <auto-list
            v-model="filterInstituteField"
            name="InstituteField"
            placeholder="المجال المهني"
            cols="3"
            :add="false"
            @update:model-value="onInstituteFieldChange"
          />
          <auto-list
            v-model="filterInstituteEducationSystem"
            name="InstituteEducationSystem"
            :param="filterInstituteField"
            placeholder="نظام التعليم"
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
            :param="filterInstituteSpecialization"
            placeholder="المادة التدريبية"
            cols="3"
            :add="false"
            @update:model-value="fetchExamsList"
          />
        </template>

        <!-- منسدلة اختيار الاختبار المعتمد (في الأخير بعد الفلترة!) -->
        <v-col cols="12" :md="filterInstitutionType === 'all' ? 4 : 6" class="py-2">
          <v-autocomplete
            v-model="selectedExamId"
            :items="examsList"
            item-title="title"
            item-value="id"
            label="اختر الاختبار لمعاينة وطباعة وثائقه (الأسئلة والتظليل)"
            placeholder="ابحث باسم الاختبار أو رمزه أو المادة..."
            prepend-inner-icon="mdi-school-outline"
            variant="outlined"
            density="compact"
            rounded="lg"
            hide-details
            clearable
            :loading="loadingExams"
            @update:model-value="onExamSelected"
          >
            <template #item="{ props: iProps, item }">
              <v-list-item
                v-bind="iProps"
                :title="item.raw.title"
                :subtitle="`المادة: ${item.raw.subject_name || 'عام'} | الطلاب: ${item.raw.registered_students_count || 0} طالب | النماذج: ${item.raw.versions_count || 1}`"
              />
            </template>
          </v-autocomplete>
        </v-col>

        <!-- أزرار الإجراءات السريعة (تحديث وتفريغ) -->
        <v-col cols="12" sm="6" :md="filterInstitutionType === 'all' ? 2 : 3" class="d-flex align-center gap-2 py-2">
          <custom-btn
            type="show"
            label="تحديث"
            color="primary"
            class="font-weight-bold flex-grow-1"
            :click="fetchExamsList"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetInstitutionFilters"
            variant="tonal"
            color="error"
            label="تفريغ"
            class="font-weight-bold"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- ── بطاقة معلومات الاختبار المحدد (تصميم مؤسسي متوازن وأنيق) ── -->
    <div v-if="selectedExam" class="active-exam-banner mb-4 pa-4 bg-white border rounded-xl elevation-1">
      <!-- السطر الأول: العنوان والهوية والاعتماد -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-3 border-b">
        <div class="d-flex align-center gap-3">
          <div class="exam-icon-badge rounded-lg d-flex align-center justify-center border" style="width: 40px; height: 40px; flex-shrink: 0;">
            <v-icon size="22" color="primary">mdi-file-document-check-outline</v-icon>
          </div>
          <div>
            <h2 class="text-subtitle-1 font-weight-black text-on-surface mb-0" style="font-size: 0.98rem !important;">
              {{ selectedExam.title }}
            </h2>
          </div>
        </div>

        <div class="d-flex align-center gap-2">
          <span class="exam-code-tag font-mono font-weight-bold text-caption px-2.5 py-1 rounded-lg border">
            {{ selectedExam.uniqueCode }}
          </span>
          <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold" prepend-icon="mdi-check-decagram-outline">
            معتمد للطباعة
          </v-chip>
          <v-btn
            size="small"
            variant="tonal"
            color="primary"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-tune-vertical"
            :to="`/omr-template-builder?examId=${selectedExam.id}&mode=designer`"
            title="تخصيص وضبط القالب الهندسي في المصمم"
          >
            تخصيص القالب
          </v-btn>
        </div>
      </div>

      <!-- السطر الثاني: التفاصيل والمقاييس التشغيلية -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-3 pt-3">
        <div class="d-flex align-center gap-3 text-caption text-medium-emphasis flex-wrap">
          <span v-if="selectedExam.subject_name" class="d-flex align-center gap-1">
            <v-icon size="15" color="primary">mdi-book-open-page-variant-outline</v-icon>
            المادة: <strong class="text-on-surface font-weight-bold">{{ selectedExam.subject_name }}</strong>
          </span>
          <span class="text-disabled">•</span>
          <span class="d-flex align-center gap-1">
            <v-icon size="15" color="primary">mdi-calendar-range-outline</v-icon>
            العام الدراسي: <strong class="text-on-surface font-weight-bold">{{ selectedExam.year_name || '2025-2026' }}</strong>
          </span>
        </div>

        <div class="d-flex align-center gap-2 flex-wrap">
          <div class="exam-stat-chip px-3 py-1.5 rounded-lg border d-flex align-center gap-2">
            <v-icon size="16" color="primary">mdi-layers-outline</v-icon>
            <span class="text-caption text-medium-emphasis">النماذج:</span>
            <span class="text-caption font-weight-black text-primary">
              {{ selectedExam.versions_count || examDetails?.versions?.length || 1 }} نماذج (A, B, C, D)
            </span>
          </div>

          <div class="exam-stat-chip px-3 py-1.5 rounded-lg border d-flex align-center gap-2">
            <v-icon size="16" color="success">mdi-account-group-outline</v-icon>
            <span class="text-caption text-medium-emphasis">الطلاب المشمولين:</span>
            <span class="text-caption font-weight-black text-success">
              {{ examDetails?.registered_students?.length || selectedExam.registered_students_count || 0 }} طالب
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Navigation Tabs (خفيف وسهل) ───────────────────────────── -->
    <div class="registry-nav-bar mb-6">
      <div class="registry-nav-container">
        <div
          class="registry-nav-item"
          :class="{ 'is-active': activeTab === 'sheets' }"
          @click="activeTab = 'sheets'; visitedTabs.add('sheets')"
          role="button"
          tabindex="0"
        >
          <v-icon size="17" class="nav-icon">mdi-table-account</v-icon>
          <span>الجدول الموحد لأوراق التظليل</span>
        </div>

        <div
          class="registry-nav-item"
          :class="{ 'is-active': activeTab === 'questions' }"
          @click="activeTab = 'questions'; visitedTabs.add('questions')"
          role="button"
          tabindex="0"
        >
          <v-icon size="17" class="nav-icon">mdi-file-document-outline</v-icon>
          <span>ورقة الأسئلة الرسمية (الكراسة)</span>
        </div>

        <div
          class="registry-nav-item"
          :class="{ 'is-active': activeTab === 'package' }"
          @click="activeTab = 'package'; visitedTabs.add('package')"
          role="button"
          tabindex="0"
        >
          <v-icon size="17" class="nav-icon">mdi-package-variant-closed</v-icon>
          <span>حزمة الاختبار (أسئلة + تظليل)</span>
        </div>

        <div
          class="registry-nav-item"
          :class="{ 'is-active': activeTab === 'history' }"
          @click="activeTab = 'history'; visitedTabs.add('history')"
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
    <div v-show="activeTab !== 'history'">
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

        <!-- ════════════════════════════════════════════════════════════ -->
        <!-- TAB 1: UNIFIED ROSTER TABLE (الجدول الموحد لأوراق التظليل)  -->
        <!-- ════════════════════════════════════════════════════════════ -->
        <div v-if="visitedTabs.has('sheets')" v-show="activeTab === 'sheets'">
          <!-- Top Control Toolbar (شريط التحكم والفلترة الموحد) -->
          <div class="main-card rounded-2xl pa-4 mb-4 border bg-white shadow-sm">
            <!-- Row 1: Search, Filters & Main Actions -->
            <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-3 border-b">
              <!-- Search and Filters -->
              <div class="d-flex align-center gap-2 flex-wrap flex-grow-1">
                <!-- Search Field -->
                <div style="min-width: 240px; max-width: 340px;" class="flex-grow-1">
                  <v-text-field
                    v-model="rosterSearch"
                    placeholder="ابحث بالاسم، رقم الجلوس، الرقم السري، المدرسة..."
                    density="compact"
                    variant="outlined"
                    rounded="lg"
                    hide-details
                    clearable
                    prepend-inner-icon="mdi-magnify"
                  />
                </div>

                <!-- Model Filter -->
                <div style="min-width: 140px; max-width: 180px;">
                  <v-select
                    v-model="rosterModelFilter"
                    :items="[
                      { title: 'كافة النماذج', value: 'all' },
                      { title: 'النموذج A', value: 'A' },
                      { title: 'النموذج B', value: 'B' },
                      { title: 'النموذج C', value: 'C' },
                      { title: 'النموذج D', value: 'D' },
                    ]"
                    item-title="title"
                    item-value="value"
                    density="compact"
                    variant="outlined"
                    rounded="lg"
                    hide-details
                    label="النموذج"
                    prepend-inner-icon="mdi-layers-outline"
                  />
                </div>

                <!-- Print Status Filter -->
                <div style="min-width: 150px; max-width: 190px;">
                  <v-select
                    v-model="rosterPrintFilter"
                    :items="[
                      { title: 'كافة الحالات', value: 'all' },
                      { title: 'بانتظار الطباعة', value: 'unprinted' },
                      { title: 'تمت الطباعة', value: 'printed' },
                    ]"
                    item-title="title"
                    item-value="value"
                    density="compact"
                    variant="outlined"
                    rounded="lg"
                    hide-details
                    label="حالة الطباعة"
                    prepend-inner-icon="mdi-filter-check-outline"
                  />
                </div>

                <!-- Layout Toggle (A5 vs A4) -->
                <v-btn-toggle
                  v-model="selectedSheetLayout"
                  mandatory
                  density="compact"
                  color="primary"
                  variant="outlined"
                  rounded="lg"
                >
                  <v-btn value="compact_a5" class="font-weight-bold px-2.5" prepend-icon="mdi-card-outline">
                    A5 الوزارية
                  </v-btn>
                  <v-btn value="full_a4" class="font-weight-bold px-2.5" prepend-icon="mdi-file-document-outline">
                    A4 الشاملة
                  </v-btn>
                </v-btn-toggle>
              </div>

              <!-- Action Buttons -->
              <div class="d-flex align-center gap-2 flex-wrap">
                <!-- Main Print Action -->
                <v-btn
                  color="success"
                  variant="flat"
                  rounded="lg"
                  size="default"
                  class="font-weight-black shadow-sm px-4"
                  prepend-icon="mdi-printer-check"
                  :loading="printingBatch"
                  :disabled="!targetBatchStudents.length"
                  @click="printSelectedOrAllRoster"
                >
                  طباعة أوراق التظليل {{ selectedStudentIds.length > 0 ? `المحددة (${selectedStudentIds.length})` : `للكل (${filteredRosterStudents.length})` }}
                </v-btn>

                <!-- Audit Roster Button -->
                <v-btn
                  variant="tonal"
                  color="primary"
                  rounded="lg"
                  class="font-weight-bold px-3"
                  prepend-icon="mdi-clipboard-text-outline"
                  title="طباعة كشف تسليم الكنترول الرسمي"
                  @click="printAuditRoster"
                >
                  كشف تسليم الكنترول
                </v-btn>

                <!-- Blank Version Sheet Quick Print -->
                <v-menu location="bottom end">
                  <template #activator="{ props: bProps }">
                    <v-btn
                      v-bind="bProps"
                      variant="outlined"
                      color="secondary"
                      rounded="lg"
                      class="font-weight-bold px-3"
                      prepend-icon="mdi-file-outline"
                    >
                      ورقة فارغة
                    </v-btn>
                  </template>
                  <v-list density="compact" rounded="lg">
                    <v-list-item
                      v-for="ver in ['A', 'B', 'C', 'D']"
                      :key="`blank-opt-${ver}`"
                      :title="`طباعة ورقة عامة فارغة - نموذج ${ver}`"
                      prepend-icon="mdi-printer-outline"
                      @click="printBlankSheetVersion(ver)"
                    />
                  </v-list>
                </v-menu>

                <!-- Header Override / Settings Button -->
                <v-btn
                  variant="tonal"
                  color="secondary"
                  rounded="lg"
                  icon
                  size="small"
                  title="تعديل بيانات الترويسة فورياً"
                  @click="showAdjustmentsPanel = !showAdjustmentsPanel"
                >
                  <v-icon size="18">mdi-pencil-ruler</v-icon>
                </v-btn>

                <!-- Seed sample students if empty -->
                <v-btn
                  v-if="!examDetails.registered_students?.length"
                  color="primary"
                  variant="tonal"
                  rounded="lg"
                  size="small"
                  prepend-icon="mdi-account-plus"
                  :loading="seedingStudents"
                  @click="seedSampleStudents"
                >
                  توليد طلاب تجريبيين
                </v-btn>
              </div>
            </div>

            <!-- Collapsible Live Adjustments Panel -->
            <v-expand-transition>
              <div v-if="showAdjustmentsPanel" class="pa-4 mt-3 bg-grey-lighten-4 rounded-xl border">
                <div class="text-caption font-weight-black text-primary mb-3 d-flex align-center gap-1">
                  <v-icon size="16">mdi-auto-fix</v-icon>
                  تعديل بيانات الترويسة فورياً (تنعكس التعديلات لحظياً على كافة أوراق الطلاب المطبوعة)
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

            <!-- Table Meta & Selection Bar -->
            <div class="d-flex align-center justify-space-between flex-wrap gap-2 pt-3 text-caption">
              <div class="d-flex align-center gap-2">
                <span class="font-weight-bold text-medium-emphasis">
                  إجمالي الطلاب في الكشف: <strong class="text-primary font-mono">{{ filteredRosterStudents.length }}</strong>
                </span>
                <span v-if="selectedStudentIds.length > 0" class="font-weight-black text-success">
                  • تم تحديد {{ selectedStudentIds.length }} طالب للطباعة
                </span>
              </div>
              <div class="d-flex align-center gap-2">
                <v-btn
                  v-if="filteredRosterStudents.length > 0"
                  size="x-small"
                  variant="text"
                  color="primary"
                  class="font-weight-bold"
                  @click="selectAllRosterStudents"
                >
                  {{ selectedStudentIds.length === filteredRosterStudents.length ? 'إلغاء التحديد' : 'تحديد الكل' }}
                </v-btn>
                <v-btn
                  v-if="selectedStudentIds.length > 0"
                  size="x-small"
                  variant="tonal"
                  color="success"
                  class="font-weight-bold"
                  prepend-icon="mdi-check-all"
                  @click="markSelectedAsPrinted"
                >
                  تحديد كمطبوع
                </v-btn>
              </div>
            </div>
          </div>

          <!-- UNIFIED ROSTER DATA TABLE (الجدول الموحد للطلاب وأوراق التظليل) -->
          <v-card class="rounded-2xl border overflow-hidden shadow-sm mb-6 bg-white">
            <v-data-table
              v-model="selectedStudentIds"
              :headers="rosterHeaders"
              :items="filteredRosterStudents"
              item-value="id"
              show-select
              density="comfortable"
              hover
              :items-per-page="25"
              :items-per-page-options="[10, 25, 50, 100, -1]"
              class="unified-roster-table text-body-2"
              no-data-text="لا يوجد طلاب مطابقين لمعايير البحث أو التصفية"
            >
              <!-- Seat Number Column -->
              <template #[`item.seat_number`]="{ item }">
                <span class="font-mono font-weight-black text-primary px-2 py-1 bg-blue-lighten-5 rounded-lg border">
                  {{ item.seat_number }}
                </span>
              </template>

              <!-- Secret Number Column -->
              <template #[`item.secret_number`]="{ item }">
                <span class="font-mono text-medium-emphasis">
                  {{ item.secret_number || '-' }}
                </span>
              </template>

              <!-- Student Name Column -->
              <template #[`item.student_name`]="{ item }">
                <div class="d-flex align-center gap-2">
                  <v-avatar size="28" color="grey-lighten-3" class="text-caption font-weight-bold text-primary">
                    {{ (item.student_name || 'ط').slice(0, 1) }}
                  </v-avatar>
                  <span class="font-weight-bold text-on-surface">{{ item.student_name }}</span>
                </div>
              </template>

              <!-- School / Center Column -->
              <template #[`item.school_name`]="{ item }">
                <span class="text-caption text-medium-emphasis">
                  {{ item.school_name || selectedExam?.directorate || 'المركز الرئيسي' }}
                </span>
              </template>

              <!-- Directorate Column -->
              <template #[`item.directorate`]="{ item }">
                <span class="text-caption">
                  {{ item.directorate || selectedExam?.directorate || '-' }}
                </span>
              </template>

              <!-- Model Code Column -->
              <template #[`item.model_code`]="{ item }">
                <v-chip
                  size="small"
                  :color="getModelChipColor(item.model_code)"
                  variant="flat"
                  class="font-weight-black"
                >
                  النموذج {{ item.model_code || 'A' }}
                </v-chip>
              </template>

              <!-- Print Status Column -->
              <template #[`item.is_printed`]="{ item }">
                <v-chip
                  size="small"
                  :color="item.is_printed ? 'success' : 'grey'"
                  :variant="item.is_printed ? 'flat' : 'tonal'"
                  class="font-weight-bold cursor-pointer"
                  title="انقر لتبديل حالة الطباعة"
                  @click="toggleStudentPrintedStatus(item)"
                >
                  <v-icon start size="14">{{ item.is_printed ? 'mdi-check-circle' : 'mdi-clock-outline' }}</v-icon>
                  {{ item.is_printed ? 'تمت الطباعة' : 'جاهز للطباعة' }}
                </v-chip>
              </template>

              <!-- Actions Column -->
              <template #[`item.actions`]="{ item }">
                <div class="d-flex align-center gap-1 justify-center">
                  <!-- Preview Dialog Button -->
                  <v-btn
                    icon
                    size="small"
                    variant="text"
                    color="primary"
                    title="معاينة ورقة التظليل"
                    @click="openSingleSheetPreview(item)"
                  >
                    <v-icon size="18">mdi-eye-outline</v-icon>
                  </v-btn>

                  <!-- Direct Print Button -->
                  <v-btn
                    icon
                    size="small"
                    variant="text"
                    color="success"
                    title="طباعة ورقة هذا الطالب فورياً"
                    @click="printSingleStudentDirect(item)"
                  >
                    <v-icon size="18">mdi-printer</v-icon>
                  </v-btn>
                </div>
              </template>
            </v-data-table>
          </v-card>
        </div>

        <!-- ════════════════════════════════════════════════════════════ -->
        <!-- TAB 2: QUESTIONS PAPER (كراسة ورقة الأسئلة الرسمية المعتمدة) -->
        <!-- ════════════════════════════════════════════════════════════ -->
        <div v-if="visitedTabs.has('questions')" v-show="activeTab === 'questions'" class="questions-paper-viewport mb-6">
          <div class="main-card rounded-2xl pa-4 mb-4 border d-flex align-center justify-space-between flex-wrap gap-3 bg-white">
            <div class="d-flex align-center gap-3 flex-wrap">
              <div class="text-caption font-weight-black text-primary d-flex align-center gap-1">
                <v-icon size="18">mdi-format-list-bulleted-type</v-icon>
                اختيار النموذج:
              </div>
              <div style="min-width: 200px; max-width: 260px;">
                <v-select
                  v-model="selectedQuestionsModelCode"
                  :items="questionsModelSelectOptions"
                  item-title="title"
                  item-value="value"
                  density="compact"
                  variant="outlined"
                  rounded="lg"
                  hide-details
                  prepend-inner-icon="mdi-format-list-bulleted-type"
                  label="النموذج المعروض"
                />
              </div>

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
              :center-name="customCenterName || activeSheetStudent?.school_name || selectedExam?.school_name || selectedExam?.center_name || 'المركز الامتحاني الرئيسي'"
              :center-code="activeSheetStudent?.school_id || selectedExam?.center_code || selectedExam?.id || '11'"
              :exam-time="selectedExam?.time_allowed || selectedExam?.exam_time || ''"
              :day-name="selectedExam?.day_name || ''"
              :exam-date="selectedExam?.exam_date || ''"
              :envelope-no="selectedExam?.envelope_no || '1'"
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
        <!-- TAB 3: COMBINED PACKAGE (كراسة الأسئلة + ورقة التظليل)     -->
        <!-- ════════════════════════════════════════════════════════════ -->
        <div v-if="visitedTabs.has('package')" v-show="activeTab === 'package'" class="exam-package-viewport mb-6">
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
              :center-name="customCenterName || activeSheetStudent?.school_name || selectedExam?.school_name || selectedExam?.center_name || 'المركز الامتحاني الرئيسي'"
              :center-code="activeSheetStudent?.school_id || selectedExam?.center_code || selectedExam?.id || '11'"
              :exam-time="selectedExam?.time_allowed || selectedExam?.exam_time || ''"
              :day-name="selectedExam?.day_name || ''"
              :exam-date="selectedExam?.exam_date || ''"
              :envelope-no="selectedExam?.envelope_no || '1'"
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
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════════════ -->
    <!-- TAB 4: سجل الدفعات السابقة المطبوعة                                 -->
    <!-- ══════════════════════════════════════════════════════════════════ -->
    <div v-if="visitedTabs.has('history')" v-show="activeTab === 'history'">
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

    <!-- Single Sheet Preview Dialog (معاينة ورقة التظليل الفردية في نافذة منبثقة دون تشويش الشاشة) -->
    <v-dialog v-model="singleSheetDialog" max-width="850px" scrollable>
      <v-card v-if="previewStudent" class="rounded-2xl overflow-hidden">
        <v-card-title class="d-flex align-center justify-space-between bg-grey-lighten-4 py-3 px-4 border-b">
          <div class="d-flex align-center gap-2">
            <v-icon color="primary" size="22">mdi-card-account-details-outline</v-icon>
            <span class="font-weight-black text-subtitle-1">
              معاينة ورقة التظليل: {{ previewStudent.student_name }}
            </span>
            <v-chip size="x-small" :color="getModelChipColor(previewStudent.model_code)" variant="flat" class="font-weight-black ms-2">
              النموذج {{ previewStudent.model_code || 'A' }}
            </v-chip>
          </div>
          <div class="d-flex align-center gap-2">
            <v-btn
              color="success"
              variant="flat"
              rounded="lg"
              size="small"
              class="font-weight-bold px-3"
              prepend-icon="mdi-printer"
              @click="printPreviewStudentSheet"
            >
              طباعة هذه الورقة
            </v-btn>
            <v-btn icon size="small" variant="text" @click="singleSheetDialog = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </div>
        </v-card-title>

        <v-card-text class="pa-4 d-flex justify-center bg-grey-lighten-5">
          <div ref="singlePreviewRef" class="single-sheet-preview-wrap bg-white rounded-xl border elevation-1 pa-3">
            <YemeniAuditReportSheet
              v-if="selectedSheetLayout === 'full_a4'"
              :student-name="previewStudent.student_name"
              :seat-number="previewStudent.seat_number"
              :serial-number="previewStudent.secret_number || previewStudent.model_code"
              :model-code="previewStudent.model_code || 'A'"
              :form-number="previewStudent.model_code || 'A'"
              :exam-subject="selectedExam?.subject_name || 'الرياضيات'"
              :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار الشهادة العامة'))"
              :exam-year="customExamYear || selectedExam?.year_name || '2026'"
              :center-name="customCenterName || previewStudent.school_name || selectedExam?.directorate || 'المركز الاختباري الرئيسي'"
              :center-code="previewStudent.school_id || selectedExam?.id || '101'"
              :governorate="customGovernorate || previewStudent.governorate || selectedExam?.governorate || 'أمانة العاصمة'"
              :directorate="customDirectorate || previewStudent.directorate || selectedExam?.directorate || 'السبعين'"
              :barcode-value="previewStudent.barcode_value || `EXAM_${selectedExam?.id}_VER_${previewStudent.model_code || 'A'}_SEAT_${previewStudent.seat_number}`"
              :qr-value="previewStudent.qr_value || `${selectedExam?.uniqueCode}|${previewStudent.model_code || 'A'}|${previewStudent.seat_number}`"
              :total-questions="getQuestionsCountForVersion(previewStudent.model_code)"
              :sections="getSectionsForVersion(previewStudent.model_code)"
            />

            <YemeniMinistrySheet
              v-else
              layout-mode="compact_a5"
              :student-name="previewStudent.student_name"
              :seat-number="previewStudent.seat_number"
              :serial-number="previewStudent.secret_number || previewStudent.model_code"
              :model-code="previewStudent.model_code || 'A'"
              :exam-subject="selectedExam?.subject_name || 'الرياضيات'"
              :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار الشهادة العامة'))"
              :exam-year="customExamYear || selectedExam?.year_name || '2026'"
              :center-name="customCenterName || previewStudent.school_name || selectedExam?.directorate || 'المركز الامتحاني الرئيسي'"
              :governorate="customGovernorate || selectedExam?.governorate || 'أمانة العاصمة'"
              :directorate="customDirectorate || previewStudent.directorate || selectedExam?.directorate || 'السبعين'"
              :barcode-value="previewStudent.barcode_value || `EXAM_${selectedExam?.id}_VER_${previewStudent.model_code || 'A'}_SEAT_${previewStudent.seat_number}`"
              :qr-value="previewStudent.qr_value || `${selectedExam?.uniqueCode}|${previewStudent.model_code || 'A'}|${previewStudent.seat_number}`"
              :total-questions="getQuestionsCountForVersion(previewStudent.model_code)"
              :sections="getSectionsForVersion(previewStudent.model_code)"
              :interactive="false"
            />
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Hidden Staging Container for Print Batches (Only rendered during print execution for zero DOM overhead) -->
    <div v-if="printingBatch" id="omr-registry-batch-staging" class="d-none">
      <div
        v-for="st in targetBatchStudents"
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
import { gradebookAPI } from '@/services/omr/endpoints'
import YemeniMinistrySheet from '@/components/omr_templates/YemeniMinistrySheet.vue'
import YemeniAuditReportSheet from '@/components/omr_templates/YemeniAuditReportSheet.vue'
import YemeniOfficialQuestionPaper from '@/components/omr_templates/YemeniOfficialQuestionPaper.vue'
import { printOmrElement, printOmrBatch, printOfficialQuestionPaper, printExamPackage } from './utils/omrPrint'

const route = useRoute()

// ── Master View & Administrative Hierarchy State ──
const currentView = ref(route.query.exam ? 'detail' : 'master')
const masterTab = ref('schools')
const institutionType = ref('school')
const loadingMaster = ref(false)
const masterSearchQuery = ref('')

const selectedOfficeId = ref(null)
const selectedOfficeName = ref('')
const selectedDirectorateId = ref(null)
const selectedDirectorateName = ref('')
const selectedSchoolId = ref(null)
const selectedSchoolName = ref('')

const officesList = ref([])
const directoratesList = ref([])
const schoolsList = ref([])
const masterExamsList = ref([])

// Master Table Headers
const officeMasterHeaders = [
  { title: "مكتب التربية والتعليم (المحافظة)", key: "office_name", sortable: true, align: "start" },
  { title: "المديريات", key: "directorates_count", sortable: true, align: "center", width: "100px" },
  { title: "المراكز والمدارس", key: "schools_count", sortable: true, align: "center", width: "130px" },
  { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "100px" },
  { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
  { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "120px" },
  { title: "نسبة الإنجاز", key: "printed_rate", sortable: true, align: "center", width: "130px" },
  { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "120px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "220px" },
]

const directorateMasterHeaders = [
  { title: "إدارة التربية والتعليم (المديرية)", key: "name", sortable: true, align: "start" },
  { title: "المكتب التابع له", key: "office_name", sortable: true, align: "center", width: "180px" },
  { title: "المراكز والمدارس", key: "schools_count", sortable: true, align: "center", width: "130px" },
  { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "100px" },
  { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
  { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "120px" },
  { title: "نسبة الإنجاز", key: "printed_rate", sortable: true, align: "center", width: "130px" },
  { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "120px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "220px" },
]

const schoolMasterHeaders = [
  { title: "المدرسة / المركز الامتحاني", key: "name", sortable: true, align: "start" },
  { title: "نوع المؤسسة", key: "institution_type", sortable: true, align: "center", width: "110px" },
  { title: "المحافظة والمديرية", key: "directorate_name", sortable: true, align: "center", width: "160px" },
  { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "100px" },
  { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
  { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "120px" },
  { title: "نسبة الطباعة", key: "printed_rate", sortable: true, align: "center", width: "130px" },
  { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "120px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "190px" },
]

const examMasterHeaders = [
  { title: "رمز الاختبار", key: "uniqueCode", sortable: true, align: "center", width: "160px" },
  { title: "عنوان الاختبار والمادة", key: "title", sortable: true, align: "start" },
  { title: "المدارس المشاركة", key: "schools_count", sortable: true, align: "center", width: "120px" },
  { title: "المقيدون", key: "total_registered", sortable: true, align: "center", width: "110px" },
  { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "120px" },
  { title: "نسبة الطباعة", key: "printed_rate", sortable: true, align: "center", width: "130px" },
  { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "120px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "160px" },
]

const registryMasterHeaders = [
  { title: "رقم الدفعة", key: "batch_id", sortable: true, align: "start", width: "170px" },
  { title: "عنوان الاختبار", key: "exam_title", sortable: true, align: "start" },
  { title: "عدد الأوراق", key: "total_sheets", sortable: true, align: "center", width: "110px" },
  { title: "تاريخ الطباعة", key: "printed_at", sortable: true, align: "center", width: "160px" },
  { title: "المسؤول", key: "printed_by_name", sortable: true, align: "center", width: "140px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "120px" },
]

// Master KPI Computeds
const kpiTotalPrinted = computed(() => {
  return masterExamsList.value.reduce((acc, e) => acc + (Number(e.printed_count) || 0), 0)
})

const kpiTotalRegistered = computed(() => {
  return masterExamsList.value.reduce((acc, e) => acc + (Number(e.total_registered || e.total_students) || 0), 0)
})

const kpiPrintRate = computed(() => {
  if (!kpiTotalRegistered.value) return 0
  return Math.round((kpiTotalPrinted.value / kpiTotalRegistered.value) * 1000) / 10
})

const kpiSchoolsCount = computed(() => {
  return schoolsList.value.length
})

const kpiExamsCount = computed(() => {
  return masterExamsList.value.length
})

// Autocomplete Options
const directoratesOptions = computed(() => {
  if (selectedOfficeId.value) {
    return directoratesList.value.filter(d => d.office_id === selectedOfficeId.value)
  }
  return directoratesList.value
})

const schoolsOptions = computed(() => {
  let list = schoolsList.value
  if (institutionType.value !== 'all') {
    list = list.filter(s => !s.institution_type || s.institution_type === institutionType.value)
  }
  if (selectedDirectorateId.value) {
    const dObj = directoratesList.value.find(d => d.id === selectedDirectorateId.value)
    const dName = dObj?.name?.replace(/^(إدارة التربية والتعليم - مديرية |مديرية )/, '').trim()
    list = list.filter(s => 
      s.directorate_id === selectedDirectorateId.value ||
      (dName && s.directorate_name && s.directorate_name.includes(dName))
    )
  } else if (selectedOfficeId.value) {
    const oObj = officesList.value.find(o => o.id === selectedOfficeId.value)
    const oGov = oObj?.governorate_name?.trim()
    list = list.filter(s => 
      s.office_id === selectedOfficeId.value ||
      (oGov && s.governorate_name && s.governorate_name.includes(oGov))
    )
  }
  return list
})

// Filtered Master Tables Computeds
const filteredOfficesTable = computed(() => {
  let list = officesList.value || []
  if (masterSearchQuery.value) {
    const q = masterSearchQuery.value.toLowerCase().trim()
    list = list.filter(o => 
      (o.office_name && o.office_name.toLowerCase().includes(q)) ||
      (o.governorate_name && o.governorate_name.toLowerCase().includes(q))
    )
  }
  return list
})

const filteredDirectoratesTable = computed(() => {
  let list = directoratesList.value || []
  if (selectedOfficeId.value) {
    list = list.filter(d => d.office_id === selectedOfficeId.value)
  }
  if (masterSearchQuery.value) {
    const q = masterSearchQuery.value.toLowerCase().trim()
    list = list.filter(d => 
      (d.name && d.name.toLowerCase().includes(q)) ||
      (d.office_name && d.office_name.toLowerCase().includes(q))
    )
  }
  return list
})

const filteredSchoolsTable = computed(() => {
  let list = schoolsList.value || []
  if (institutionType.value !== 'all') {
    list = list.filter(s => !s.institution_type || s.institution_type === institutionType.value)
  }
  if (selectedDirectorateId.value) {
    const dObj = directoratesList.value.find(d => d.id === selectedDirectorateId.value)
    const dName = dObj?.name?.replace(/^(إدارة التربية والتعليم - مديرية |مديرية )/, '').trim()
    list = list.filter(s => 
      s.directorate_id === selectedDirectorateId.value ||
      (dName && s.directorate_name && s.directorate_name.includes(dName))
    )
  } else if (selectedOfficeId.value) {
    const oObj = officesList.value.find(o => o.id === selectedOfficeId.value)
    const oGov = oObj?.governorate_name?.trim()
    list = list.filter(s => 
      s.office_id === selectedOfficeId.value ||
      (oGov && s.governorate_name && s.governorate_name.includes(oGov))
    )
  }
  if (masterSearchQuery.value) {
    const q = masterSearchQuery.value.toLowerCase().trim()
    list = list.filter(s => 
      (s.name && s.name.toLowerCase().includes(q)) ||
      (s.directorate_name && s.directorate_name.toLowerCase().includes(q)) ||
      (s.governorate_name && s.governorate_name.toLowerCase().includes(q))
    )
  }
  return list
})

const filteredMasterExamsTable = computed(() => {
  let list = masterExamsList.value || []
  if (selectedDirectorateId.value) {
    list = list.filter(e => e.directorate_id === selectedDirectorateId.value)
  } else if (selectedOfficeId.value) {
    list = list.filter(e => e.governorate_id === selectedOfficeId.value || e.office_id === selectedOfficeId.value)
  }
  if (masterSearchQuery.value) {
    const q = masterSearchQuery.value.toLowerCase().trim()
    list = list.filter(e => 
      (e.title && e.title.toLowerCase().includes(q)) ||
      (e.uniqueCode && e.uniqueCode.toLowerCase().includes(q)) ||
      (e.subject_name && e.subject_name.toLowerCase().includes(q))
    )
  }
  return list
})

const filteredBatchesTable = computed(() => {
  let list = batches.value || []
  if (masterSearchQuery.value) {
    const q = masterSearchQuery.value.toLowerCase().trim()
    list = list.filter(b => 
      (b.batch_id && b.batch_id.toLowerCase().includes(q)) ||
      (b.exam_title && b.exam_title.toLowerCase().includes(q)) ||
      (b.exam_code && b.exam_code.toLowerCase().includes(q))
    )
  }
  return list
})

// Master Methods
const loadMasterData = async () => {
  loadingMaster.value = true
  try {
    const params = {
      institution_type: institutionType.value !== 'all' ? institutionType.value : undefined,
    }
    const [officesRes, directoratesRes, schoolsRes, examsRes] = await Promise.all([
      gradebookAPI.getByOffice(params).catch(() => ({ data: { results: [] } })),
      gradebookAPI.getByDirectorate(params).catch(() => ({ data: { results: [] } })),
      gradebookAPI.getBySchool(params).catch(() => ({ data: { results: [] } })),
      gradebookAPI.list(params).catch(() => ({ data: { results: [] } }))
    ])
    officesList.value = officesRes.data?.results || []
    directoratesList.value = directoratesRes.data?.results || []
    schoolsList.value = schoolsRes.data?.results || []
    masterExamsList.value = examsRes.data?.results || []
  } catch (err) {
    console.error('Failed to load master data:', err)
  } finally {
    loadingMaster.value = false
  }
}

const onSectorChange = (val) => {
  institutionType.value = val
  selectedOfficeId.value = null
  selectedOfficeName.value = ''
  selectedDirectorateId.value = null
  selectedDirectorateName.value = ''
  selectedSchoolId.value = null
  selectedSchoolName.value = ''
  loadMasterData()
}

const onOfficeFilterChange = (officeId) => {
  selectedOfficeId.value = officeId
  selectedDirectorateId.value = null
  selectedDirectorateName.value = ''
  selectedSchoolId.value = null
  selectedSchoolName.value = ''
  if (officeId) {
    const o = officesList.value.find(item => item.id === officeId)
    if (o) selectedOfficeName.value = o.office_name
  } else {
    selectedOfficeName.value = ''
  }
}

const onDirectorateFilterChange = (dirId) => {
  selectedDirectorateId.value = dirId
  selectedSchoolId.value = null
  selectedSchoolName.value = ''
  if (dirId) {
    const d = directoratesList.value.find(item => item.id === dirId)
    if (d) {
      selectedDirectorateName.value = d.name
      if (d.office_id && !selectedOfficeId.value) {
        selectedOfficeId.value = d.office_id
        selectedOfficeName.value = d.office_name
      }
    }
  } else {
    selectedDirectorateName.value = ''
  }
}

const onSchoolFilterChange = (schoolId) => {
  selectedSchoolId.value = schoolId
  if (schoolId) {
    const s = schoolsList.value.find(item => item.id === schoolId)
    if (s) {
      selectedSchoolName.value = s.name
      if (s.directorate_name && !selectedDirectorateName.value) selectedDirectorateName.value = s.directorate_name
      if (s.governorate_name && !selectedOfficeName.value) selectedOfficeName.value = s.governorate_name
    }
  } else {
    selectedSchoolName.value = ''
  }
}

const drillDownToOffice = (office) => {
  selectedOfficeId.value = office.id
  selectedOfficeName.value = office.office_name
  masterTab.value = 'directorates'
}

const drillDownToDirectorate = (dir) => {
  selectedDirectorateId.value = dir.id
  selectedDirectorateName.value = dir.name
  if (dir.office_id && !selectedOfficeId.value) {
    selectedOfficeId.value = dir.office_id
    selectedOfficeName.value = dir.office_name
  }
  masterTab.value = 'schools'
}

const openSchoolStudio = async (school) => {
  selectedSchoolId.value = school.id
  selectedSchoolName.value = school.name
  if (school.directorate_name) selectedDirectorateName.value = school.directorate_name
  if (school.governorate_name) selectedOfficeName.value = school.governorate_name
  currentView.value = 'detail'
  await fetchExamsList({ school_id: school.id })
  if (examsList.value && examsList.value.length > 0) {
    selectedExamId.value = examsList.value[0].id
    await loadExamDetails(selectedExamId.value, { school_id: school.id })
  }
}

const openDirectorateStudio = async (dir) => {
  selectedDirectorateId.value = dir.id
  selectedDirectorateName.value = dir.name
  if (dir.office_name) selectedOfficeName.value = dir.office_name
  currentView.value = 'detail'
  await fetchExamsList({ directorate_id: dir.id })
  if (examsList.value && examsList.value.length > 0) {
    selectedExamId.value = examsList.value[0].id
    await loadExamDetails(selectedExamId.value, { directorate_id: dir.id })
  }
}

const openOfficeStudio = async (office) => {
  selectedOfficeId.value = office.id
  selectedOfficeName.value = office.office_name
  currentView.value = 'detail'
  await fetchExamsList({ office_id: office.id })
  if (examsList.value && examsList.value.length > 0) {
    selectedExamId.value = examsList.value[0].id
    await loadExamDetails(selectedExamId.value, { office_id: office.id })
  }
}

const openExamStudio = async (exam) => {
  selectedExamId.value = exam.id
  currentView.value = 'detail'
  await loadExamDetails(exam.id, {
    school_id: selectedSchoolId.value || undefined,
    directorate_id: selectedDirectorateId.value || undefined,
    office_id: selectedOfficeId.value || undefined,
  })
}

const returnToMaster = async () => {
  currentView.value = 'master'
  await loadMasterData()
}

const clearSchoolFilter = async () => {
  selectedSchoolId.value = null
  selectedSchoolName.value = ''
  if (selectedExamId.value) {
    await loadExamDetails(selectedExamId.value)
  }
}

// Active Tab: 'sheets' | 'questions' | 'package' | 'history'
const activeTab = ref(
  route.query.tab === 'history' ? 'history' :
  route.query.tab === 'questions' ? 'questions' :
  route.query.tab === 'package' ? 'package' : 'sheets'
)

// Track visited tabs for instant lazy-mounting & zero-lag tab switching
const visitedTabs = ref(new Set([activeTab.value]))

// Document Category: أوراق التظليل vs ورقة الأسئلة الرسمية vs حزمة الاختبار الكاملة
const selectedDocType = ref(
  ['sheets', 'questions', 'package'].includes(activeTab.value) ? activeTab.value : 'sheets'
)
const selectedQuestionsModelCode = ref('A')
const selectedQuestionPaperLayout = ref('a4') // 'a4' | 'a3'
const questionPaperRef = ref(null)

// ── Smart Print Job Manifest Computeds ──
const activeTabTitle = computed(() => {
  if (activeTab.value === 'sheets') return 'أوراق التظليل المخصصة للطلاب (OMR Sheets)'
  if (activeTab.value === 'questions') return 'كراسة الأسئلة الرسمية المعتمدة (Exam Booklet)'
  if (activeTab.value === 'package') return 'حزمة الاختبار المتكاملة للمظروف (أسئلة + تظليل)'
  return 'سجل الدفعات المطبوعة'
})

watch(activeTab, (newTab) => {
  visitedTabs.value.add(newTab)
  if (['sheets', 'questions', 'package'].includes(newTab)) {
    selectedDocType.value = newTab
  }
})

watch(selectedDocType, (newDoc) => {
  if (['sheets', 'questions', 'package'].includes(newDoc) && activeTab.value !== newDoc && activeTab.value !== 'history') {
    activeTab.value = newDoc
    visitedTabs.value.add(newDoc)
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
  selectedExamId.value = null
  examDetails.value = null
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

const modelFilterSelectOptions = computed(() => {
  const total = examDetails.value?.registered_students?.length || 0
  const list = [
    { title: `كل النماذج (${total})`, value: 'all' }
  ]
  ;(examDetails.value?.versions || []).forEach(v => {
    list.push({ title: `النموذج ${v.versionCode}`, value: v.versionCode })
  })
  return list
})

const questionsModelSelectOptions = computed(() => {
  if (!examDetails.value?.versions?.length) return []
  return examDetails.value.versions.map(v => ({
    title: `النموذج ${v.versionCode} (${v.questions?.length || v.questionsCount || 0} سؤال)`,
    value: v.versionCode
  }))
})

// ── Unified Roster Table & Batch Print State (الجدول الموحد لأوراق التظليل والطلاب) ──
const rosterSearch = ref('')
const rosterModelFilter = ref('all')
const rosterPrintFilter = ref('all')
const selectedStudentIds = ref([])
const singleSheetDialog = ref(false)
const previewStudent = ref(null)
const singlePreviewRef = ref(null)

const rosterHeaders = [
  { title: 'رقم الجلوس', key: 'seat_number', align: 'start', sortable: true },
  { title: 'الرقم السري', key: 'secret_number', align: 'start', sortable: true },
  { title: 'اسم الطالب الرباعي', key: 'student_name', align: 'start', sortable: true },
  { title: 'المدرسة / المركز', key: 'school_name', align: 'start', sortable: true },
  { title: 'المديرية', key: 'directorate', align: 'start', sortable: true },
  { title: 'النموذج', key: 'model_code', align: 'center', sortable: true },
  { title: 'حالة الطباعة', key: 'is_printed', align: 'center', sortable: true },
  { title: 'الإجراءات', key: 'actions', align: 'center', sortable: false },
]

const getModelChipColor = (code) => {
  switch (code) {
    case 'A': return 'primary'
    case 'B': return 'deep-purple-darken-1'
    case 'C': return 'warning'
    case 'D': return 'teal-darken-1'
    default: return 'primary'
  }
}

const filteredRosterStudents = computed(() => {
  if (!examDetails.value?.registered_students) return []
  let list = examDetails.value.registered_students

  if (rosterModelFilter.value && rosterModelFilter.value !== 'all') {
    list = list.filter(s => (s.model_code || 'A') === rosterModelFilter.value)
  }

  if (rosterPrintFilter.value === 'printed') {
    list = list.filter(s => s.is_printed)
  } else if (rosterPrintFilter.value === 'unprinted') {
    list = list.filter(s => !s.is_printed)
  }

  if (rosterSearch.value && rosterSearch.value.trim()) {
    const q = rosterSearch.value.trim().toLowerCase()
    list = list.filter(s =>
      String(s.seat_number || '').toLowerCase().includes(q) ||
      String(s.secret_number || '').toLowerCase().includes(q) ||
      String(s.student_name || '').toLowerCase().includes(q) ||
      String(s.school_name || '').toLowerCase().includes(q) ||
      String(s.directorate || '').toLowerCase().includes(q)
    )
  }

  return list
})

const targetBatchStudents = computed(() => {
  if (selectedStudentIds.value && selectedStudentIds.value.length > 0) {
    const idSet = new Set(selectedStudentIds.value)
    return (examDetails.value?.registered_students || []).filter(s => idSet.has(s.id))
  }
  return filteredRosterStudents.value
})

const filteredStreamStudents = computed(() => filteredRosterStudents.value)

const selectAllRosterStudents = () => {
  if (selectedStudentIds.value.length === filteredRosterStudents.value.length) {
    selectedStudentIds.value = []
  } else {
    selectedStudentIds.value = filteredRosterStudents.value.map(s => s.id)
  }
}

const toggleStudentPrintedStatus = (st) => {
  st.is_printed = !st.is_printed
  if (st.is_printed) {
    st.printed_at = new Date().toLocaleTimeString('ar-YE')
  }
  if (selectedExamId.value) {
    api.post(`/api/omr/exam-linking/${selectedExamId.value}/mark-printed/`, {
      student_ids: [st.id],
      is_printed: st.is_printed
    }).catch(e => console.error("Toggle print status error:", e))
  }
}

const markSelectedAsPrinted = () => {
  if (!selectedStudentIds.value.length) return
  const idSet = new Set(selectedStudentIds.value)
  const targetIds = []
  ;(examDetails.value?.registered_students || []).forEach(st => {
    if (idSet.has(st.id)) {
      st.is_printed = true
      st.printed_at = new Date().toLocaleTimeString('ar-YE')
      targetIds.push(st.id)
    }
  })
  if (selectedExamId.value && targetIds.length) {
    api.post(`/api/omr/exam-linking/${selectedExamId.value}/mark-printed/`, {
      student_ids: targetIds,
      is_printed: true
    }).catch(e => console.error("Mark printed error:", e))
  }
  batchPrintNotification.value = {
    show: true,
    color: 'success',
    message: `تم تحديد ${targetIds.length} طالب كمطبوع وتحديث السجل بنجاح.`
  }
}

const openSingleSheetPreview = (st) => {
  previewStudent.value = st
  singleSheetDialog.value = true
}

const printPreviewStudentSheet = async () => {
  await nextTick()
  let printableEl = null
  if (singlePreviewRef.value) {
    printableEl = singlePreviewRef.value.querySelector('.yemeni-audit-report-sheet') ||
                  singlePreviewRef.value.querySelector('svg.yemeni-ministry-sheet-svg') ||
                  singlePreviewRef.value.querySelector('svg')
  }
  if (printableEl && previewStudent.value) {
    const st = previewStudent.value
    await printOmrElement(printableEl, {
      title: `${selectedExam.value?.uniqueCode || 'OMR'}_${st?.seat_number || st?.model_code || 'SHEET'}`,
      isA5: selectedSheetLayout.value === 'compact_a5'
    })
    st.is_printed = true
    st.printed_at = new Date().toLocaleTimeString('ar-YE')
    if (selectedExamId.value && st.id && !String(st.id).startsWith('blank_')) {
      api.post(`/api/omr/exam-linking/${selectedExamId.value}/mark-printed/`, {
        student_ids: [st.id],
        is_printed: true
      }).catch(e => console.error(e))
    }
  } else {
    window.print()
  }
}

const printSingleStudentDirect = async (st) => {
  previewStudent.value = st
  singleSheetDialog.value = true
  await nextTick()
  await printPreviewStudentSheet()
}

const printBlankSheetVersion = async (verCode) => {
  previewStudent.value = {
    id: `blank_${verCode}`,
    student_name: '............................................',
    seat_number: '.....',
    secret_number: verCode,
    model_code: verCode,
    school_name: customCenterName.value || selectedExam.value?.directorate || 'المركز الاختباري الرئيسي',
    directorate: customDirectorate.value || selectedExam.value?.directorate || 'السبعين',
    governorate: customGovernorate.value || selectedExam.value?.governorate || 'أمانة العاصمة',
    barcode_value: `EXAM_${selectedExam.value?.id}_VER_${verCode}_BLANK`,
    qr_value: `${selectedExam.value?.uniqueCode}|${verCode}|BLANK`
  }
  singleSheetDialog.value = true
  await nextTick()
  await printPreviewStudentSheet()
}

const printAuditRoster = () => {
  const students = filteredRosterStudents.value
  if (!students.length) return

  const printWindow = window.open('', '_blank')
  if (!printWindow) return

  const exam = selectedExam.value || {}
  const center = customCenterName.value || exam.directorate || 'المركز الاختباري الرئيسي'
  const directorate = customDirectorate.value || exam.directorate || 'السبعين'
  const governorate = customGovernorate.value || exam.governorate || 'أمانة العاصمة'
  const examTitle = customStageTitle.value || exam.title || 'اختبار الشهادة الثانوية العامة'
  const yearName = customExamYear.value || exam.year_name || '1445هـ - 2024م'
  const subjectName = exam.subject_name || 'الرياضيات'

  let rowsHtml = ''
  students.forEach((st, idx) => {
    rowsHtml += `
      <tr>
        <td style="text-align: center; font-weight: bold;">${idx + 1}</td>
        <td style="text-align: center; font-family: monospace; font-weight: bold; font-size: 14px;">${st.seat_number || ''}</td>
        <td style="text-align: center; font-family: monospace;">${st.secret_number || ''}</td>
        <td style="font-weight: bold; padding-right: 8px;">${st.student_name || ''}</td>
        <td>${st.school_name || ''}</td>
        <td style="text-align: center; font-weight: bold;">النموذج ${st.model_code || 'A'}</td>
        <td style="text-align: center;">${st.is_printed ? 'نعم' : 'لا'}</td>
        <td style="min-width: 120px;"></td>
      </tr>
    `
  })

  const html = `
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
      <meta charset="utf-8">
      <title>كشف تسليم واستلام الكنترول - ${exam.uniqueCode || ''}</title>
      <style>
        body { font-family: 'Amiri', 'Traditional Arabic', Tahoma, sans-serif; margin: 15mm; color: #000; }
        .header { text-align: center; border-bottom: 2px solid #000; padding-bottom: 12px; margin-bottom: 16px; }
        .header h2 { margin: 0 0 6px 0; font-size: 20px; }
        .header h3 { margin: 0 0 6px 0; font-size: 16px; font-weight: normal; }
        .meta-grid { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 13px; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; }
        th, td { border: 1px solid #000; padding: 6px 4px; }
        th { background-color: #f0f0f0; }
        .footer { margin-top: 25px; display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; }
        @media print {
          body { margin: 10mm; }
        }
      </style>
    </head>
    <body>
      <div class="header">
        <h2>الجمهورية اليمنية - وزارة التربية والتعليم</h2>
        <h3>قطاع المناهج والتوجيه - الإدارة العامة للاختبارات</h3>
        <h2>كشف تسليم واستلام أوراق إجابة التظليل (OMR)</h2>
      </div>
      <div class="meta-grid">
        <div>المحافظة: ${governorate} | المديرية: ${directorate}</div>
        <div>المركز / المدرسة: ${center}</div>
      </div>
      <div class="meta-grid">
        <div>المادة: ${subjectName} | المرحلة: ${examTitle}</div>
        <div>العام الدراسي: ${yearName} | إجمالي الطلاب: ${students.length}</div>
      </div>
      <table>
        <thead>
          <tr>
            <th style="width: 35px;">م</th>
            <th style="width: 85px;">رقم الجلوس</th>
            <th style="width: 75px;">الرقم السري</th>
            <th>اسم الطالب الرباعي</th>
            <th>المدرسة</th>
            <th style="width: 75px;">النموذج</th>
            <th style="width: 65px;">مطبوع</th>
            <th style="width: 140px;">توقيع المستلم / الملاحظات</th>
          </tr>
        </thead>
        <tbody>
          ${rowsHtml}
        </tbody>
      </table>
      <div class="footer">
        <div>مسؤول الكنترول: .......................................</div>
        <div>رئيس المركز الامتحاني: .......................................</div>
        <div>تاريخ التسليم: ${new Date().toLocaleDateString('ar-YE')}</div>
      </div>
      <script>
        window.onload = function() { window.print(); }
      <\/script>
    </body>
    </html>
  `
  printWindow.document.write(html)
  printWindow.document.close()
}

const printSelectedOrAllRoster = async () => {
  if (!targetBatchStudents.value.length) return
  printingBatch.value = true
  try {
    const isAudit = selectedSheetLayout.value === 'full_a4'
    let elements = []

    await nextTick()
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

    if (elements.length > 0) {
      const batchId = `BATCH_${Date.now()}`
      await printOmrBatch(elements, {
        title: `كشف_أوراق_تظليل_${selectedExam.value?.uniqueCode || 'الاختبار'}_${selectedSheetLayout.value}`,
        isA5: selectedSheetLayout.value === 'compact_a5'
      })

      const targetStudentIds = targetBatchStudents.value.map(s => s.id)
      if (selectedExamId.value && targetStudentIds.length > 0) {
        targetStudentIds.forEach(id => {
          const st = examDetails.value?.registered_students?.find(s => s.id === id)
          if (st) {
            st.is_printed = true
            st.printed_at = new Date().toLocaleTimeString('ar-YE')
            st.print_batch = batchId
          }
        })

        api.post(`/api/omr/exam-linking/${selectedExamId.value}/mark-printed/`, {
          student_ids: targetStudentIds,
          batch_id: batchId
        }).catch(e => console.error("Mark printed error:", e))

        fetchBatches()
      }

      batchPrintNotification.value = {
        show: true,
        color: 'success',
        message: `تم إرسال ${elements.length} ورقة تظليل إلى أمر الطباعة وتحديث سجل الدفعات بنجاح.`
      }
    }
  } catch (err) {
    console.error("Batch print error:", err)
    batchPrintNotification.value = {
      show: true,
      color: 'error',
      message: `تعذر إتمام عملية الطباعة: ${err?.message || err}`
    }
  } finally {
    printingBatch.value = false
  }
}

const batchPrintAllStudents = printSelectedOrAllRoster

const activeSheetStudent = computed(() => {
  if (previewStudent.value) return previewStudent.value
  if (!examDetails.value?.registered_students) return null
  return examDetails.value.registered_students[0] || null
})

const activeSheetModelCode = computed(() => {
  return activeSheetStudent.value?.model_code || 'A'
})

const resetHeaderOverrides = () => {
  customCenterName.value = ''
  customDirectorate.value = ''
  customGovernorate.value = ''
  customExamYear.value = ''
  customStageTitle.value = ''
}

const sheetArtboardStyle = computed(() => {
  return {
    width: '218mm',
    maxWidth: '100%',
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
const fetchExamsList = async (customParams = {}) => {
  loadingExams.value = true
  try {
    const params = {
      school_id: selectedSchoolId.value || undefined,
      directorate_id: selectedDirectorateId.value || undefined,
      office_id: selectedOfficeId.value || undefined,
      ...customParams,
    }
    if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
      params.institution_type = filterInstitutionType.value
    } else if (institutionType.value && institutionType.value !== 'all') {
      params.institution_type = institutionType.value
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
      if (selectedExamId.value && !examsList.value.some(e => e.id === selectedExamId.value)) {
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

const loadExamDetails = async (examId, customParams = {}) => {
  if (!examId) return
  loadingExamDetails.value = true
  try {
    const params = {
      school_id: selectedSchoolId.value || undefined,
      directorate_id: selectedDirectorateId.value || undefined,
      office_id: selectedOfficeId.value || undefined,
      ...customParams,
    }
    const resp = await api.get(`/api/omr/exam-linking/${examId}/`, { params })
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

const printSingleStudentCard = async (globalIndex) => {
  const isAudit = selectedSheetLayout.value === 'full_a4'
  let printableEl = null

  // 1. Check if the element is currently visible in the paginated stream
  if (batchStreamRef.value) {
    const localIndex = globalIndex % streamPageSize.value
    const pageOfIndex = Math.floor(globalIndex / streamPageSize.value) + 1
    if (pageOfIndex === streamCurrentPage.value) {
      const cards = batchStreamRef.value.querySelectorAll('.sheet-page-card')
      if (cards && cards[localIndex]) {
        printableEl = isAudit
          ? cards[localIndex].querySelector('.yemeni-audit-report-sheet')
          : (cards[localIndex].querySelector('svg.yemeni-ministry-sheet-svg') || cards[localIndex].querySelector('svg'))
      }
    }
  }

  // 2. Fallback to hidden staging container
  if (!printableEl) {
    const stagingEl = document.getElementById('omr-registry-batch-staging')
    if (stagingEl) {
      const slots = stagingEl.querySelectorAll('.batch-sheet-slot')
      if (slots && slots[globalIndex]) {
        printableEl = isAudit
          ? slots[globalIndex].querySelector('.yemeni-audit-report-sheet')
          : (slots[globalIndex].querySelector('svg.yemeni-ministry-sheet-svg') || slots[globalIndex].querySelector('svg'))
      }
    }
  }

  if (printableEl) {
    const st = filteredStreamStudents.value[globalIndex]
    await printOmrElement(printableEl, {
      title: `${selectedExam.value?.uniqueCode || 'OMR'}_${st?.seat_number || st?.model_code || globalIndex + 1}`,
      isA5: selectedSheetLayout.value === 'compact_a5'
    })
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

const refreshData = async () => {
  if (currentView.value === 'master') {
    await loadMasterData()
    await fetchBatches()
  } else {
    await fetchExamsList()
    if (selectedExamId.value) {
      await loadExamDetails(selectedExamId.value)
    }
    await fetchBatches()
  }
}

onMounted(async () => {
  await loadMasterData()
  await fetchBatches()

  const qExam = route.query.exam || route.query.exam_id
  if (qExam) {
    currentView.value = 'detail'
    selectedExamId.value = Number(qExam)
    await loadExamDetails(selectedExamId.value)
    if (route.query.tab && ['sheets', 'questions', 'package', 'history'].includes(route.query.tab)) {
      activeTab.value = route.query.tab
    } else {
      activeTab.value = 'sheets'
    }
    const title = selectedExam.value?.title || examDetails.value?.exam?.title || 'الاختبار'
    batchPrintNotification.value = {
      show: true,
      color: 'success',
      message: `تم نقل واستلام "${title}" بنجاح! كافة وثائق الاختبار وأوراق التظليل جاهزة للمعاينة والطباعة الفورية.`
    }
  } else {
    await fetchExamsList()
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
  box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.08), 0 2px 6px -1px rgba(0, 0, 0, 0.04);
  border: 1px solid #e2e8f0;
  background-color: #ffffff;
  border-radius: 16px !important;
}

.sheet-paper-wrapper {
  background-color: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: visible;
}

/* ── Lightweight Navigation Bar ── */
/* Active Exam Banner Styling */
.active-exam-banner {
  border-color: #e2e8f0 !important;
  background-color: #ffffff;
  transition: all 0.2s ease;
}

.exam-icon-badge {
  background-color: #f0f7ff !important;
  border-color: #dbeafe !important;
}

.exam-code-tag {
  letter-spacing: 0.5px;
  font-size: 0.72rem !important;
  border-color: #e2e8f0 !important;
  background-color: #f8fafc !important;
  color: #334155 !important;
}

.exam-stat-chip {
  border-color: #e2e8f0 !important;
  background-color: #f8fafc !important;
  min-width: 110px;
}

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
