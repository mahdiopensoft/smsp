<template>
  <div class="qb-submissions-view-v4 pa-4 pa-md-6">

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 1. MASTER VIEW: الهيكل الإداري وسجل الأوراق الممسوحة المركزي    -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <div v-if="currentView === 'master'" class="master-view-container">

      <!-- شريط التصفية الهيكلي الموحد (مرتب وبدون تكرار) -->
      <div class="main-card pa-4 rounded-2xl mb-4 bg-surface border elevation-1">
        <!-- شريط الفلاتر الهيكلية العلوي: عنوان وأزرار الإجراءات -->
        <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3 pb-2 border-b">
          <div class="d-flex align-center gap-2">
            <v-icon color="primary" size="20">mdi-filter-variant</v-icon>
            <span class="text-subtitle-2 font-weight-black text-on-surface">فلاتر الهيكل الإداري والمؤسسي:</span>
          </div>

          <div class="d-flex align-center gap-2">
            <v-chip color="indigo" variant="tonal" size="small" class="font-weight-black px-3">
              متوسط الدرجات: {{ statsData.average_score || 0 }}% لعموم الأوراق المصححة
            </v-chip>

            <v-btn
              variant="tonal"
              color="error"
              size="small"
              rounded="lg"
              class="font-weight-bold"
              prepend-icon="mdi-filter-remove-outline"
              @click="resetHierarchyFilters"
            >
              تفريغ الفلاتر
            </v-btn>
            <v-btn
              color="primary"
              variant="flat"
              size="small"
              rounded="lg"
              class="font-weight-bold"
              prepend-icon="mdi-refresh"
              :loading="loadingMaster"
              @click="refreshMasterData"
            >
              تحديث
            </v-btn>
          </div>
        </div>

        <v-row dense class="align-center">
          <!-- نوع المؤسسة التعليمية كفلتر منسدل أساسي -->
          <v-col cols="12" sm="6" :md="institutionType === 'school' ? 2 : 4">
            <v-select
              v-model="institutionType"
              :items="sectorOptions"
              item-title="title"
              item-value="value"
              label="نوع المؤسسة التعليمية"
              density="compact"
              variant="outlined"
              rounded="lg"
              hide-details
              :prepend-inner-icon="institutionType === 'university' ? 'mdi-domain' : (institutionType === 'institute' ? 'mdi-tools' : 'mdi-school')"
              @update:model-value="onSectorChange"
            >
              <template #item="{ props, item }">
                <v-list-item v-bind="props" :prepend-icon="item.raw?.icon" />
              </template>
            </v-select>
          </v-col>

          <!-- التعليم العام (مدرسي) -->
          <template v-if="institutionType === 'school'">
            <v-col cols="12" sm="6" md="2">
              <v-autocomplete
                v-model="selectedOfficeId"
                :items="allOfficesList && allOfficesList.length ? allOfficesList : officesList"
                item-title="office_name"
                item-value="id"
                label="مكتب التربية (المحافظة)"
                placeholder="اختر مكتب أو أكثر..."
                clearable
                multiple
                chips
                closable-chips
                density="compact"
                variant="outlined"
                rounded="lg"
                hide-details
                prepend-inner-icon="mdi-office-building-outline"
                @update:model-value="onOfficeFilterChange"
              >
                <template #selection="{ item, index }">
                  <v-chip v-if="index < 1" size="x-small" class="font-weight-bold" color="primary" variant="flat">
                    {{ item.title }}
                  </v-chip>
                  <span v-if="index === 1" class="text-caption text-primary font-weight-bold ms-1">
                    (+{{ (selectedOfficeId || []).length - 1 }})
                  </span>
                </template>
              </v-autocomplete>
            </v-col>

            <v-col cols="12" sm="6" md="2">
              <v-autocomplete
                v-model="selectedDirectorateId"
                :items="directoratesOptions"
                item-title="name"
                item-value="id"
                label="إدارة التربية (المديرية)"
                placeholder="اختر مديرية أو أكثر..."
                clearable
                multiple
                chips
                closable-chips
                density="compact"
                variant="outlined"
                rounded="lg"
                hide-details
                prepend-inner-icon="mdi-map-marker-radius-outline"
                @update:model-value="onDirectorateFilterChange"
              >
                <template #selection="{ item, index }">
                  <v-chip v-if="index < 1" size="x-small" class="font-weight-bold" color="teal" variant="flat">
                    {{ item.title }}
                  </v-chip>
                  <span v-if="index === 1" class="text-caption text-teal font-weight-bold ms-1">
                    (+{{ (selectedDirectorateId || []).length - 1 }})
                  </span>
                </template>
              </v-autocomplete>
            </v-col>

            <v-col cols="12" sm="6" md="2">
              <v-autocomplete
                v-model="selectedSchoolId"
                :items="schoolsOptions"
                item-title="name"
                item-value="id"
                label="المدرسة / المركز الامتحاني"
                placeholder="اختر مركز أو أكثر..."
                clearable
                multiple
                chips
                closable-chips
                density="compact"
                variant="outlined"
                rounded="lg"
                hide-details
                prepend-inner-icon="mdi-school-outline"
                @update:model-value="onSchoolFilterChange"
              >
                <template #selection="{ item, index }">
                  <v-chip v-if="index < 1" size="x-small" class="font-weight-bold" color="indigo" variant="flat">
                    {{ item.title }}
                  </v-chip>
                  <span v-if="index === 1" class="text-caption text-indigo font-weight-bold ms-1">
                    (+{{ (selectedSchoolId || []).length - 1 }})
                  </span>
                </template>
              </v-autocomplete>
            </v-col>

            <v-col cols="12" sm="6" md="2">
              <v-autocomplete
                v-model="selectedSubjectId"
                :items="subjectsList"
                item-title="name"
                item-value="id"
                label="المادة الدراسية"
                placeholder="تصفية حسب المادة..."
                clearable
                density="compact"
                variant="outlined"
                rounded="lg"
                hide-details
                prepend-inner-icon="mdi-book-education-outline"
                @update:model-value="onSubjectFilterChange"
              />
            </v-col>
          </template>

          <!-- التعليم الجامعي -->
          <template v-else-if="institutionType === 'university'">
            <v-col cols="12" sm="6" md="4">
              <v-autocomplete
                v-model="selectedSchoolId"
                :items="schoolsOptions"
                item-title="name"
                item-value="id"
                label="الجامعة / الكلية"
                placeholder="اختر كلية أو أكثر..."
                clearable
                multiple
                chips
                closable-chips
                density="compact"
                variant="outlined"
                rounded="lg"
                hide-details
                prepend-inner-icon="mdi-domain"
                @update:model-value="onSchoolFilterChange"
              >
                <template #selection="{ item, index }">
                  <v-chip v-if="index < 1" size="x-small" class="font-weight-bold" color="indigo" variant="flat">
                    {{ item.title }}
                  </v-chip>
                  <span v-if="index === 1" class="text-caption text-indigo font-weight-bold ms-1">
                    (+{{ (selectedSchoolId || []).length - 1 }})
                  </span>
                </template>
              </v-autocomplete>
            </v-col>

            <v-col cols="12" sm="6" md="4">
              <v-autocomplete
                v-model="selectedSubjectId"
                :items="subjectsList"
                item-title="name"
                item-value="id"
                label="المادة الدراسية"
                placeholder="تصفية حسب المادة..."
                clearable
                density="compact"
                variant="outlined"
                rounded="lg"
                hide-details
                prepend-inner-icon="mdi-book-education-outline"
                @update:model-value="onSubjectFilterChange"
              />
            </v-col>
          </template>

          <!-- التعليم الفني والمهني (معاهد) -->
          <template v-else-if="institutionType === 'institute'">
            <v-col cols="12" sm="6" md="4">
              <v-autocomplete
                v-model="selectedSchoolId"
                :items="schoolsOptions"
                item-title="name"
                item-value="id"
                label="المعهد التقني / المهني"
                placeholder="اختر معهد أو أكثر..."
                clearable
                multiple
                chips
                closable-chips
                density="compact"
                variant="outlined"
                rounded="lg"
                hide-details
                prepend-inner-icon="mdi-tools"
                @update:model-value="onSchoolFilterChange"
              >
                <template #selection="{ item, index }">
                  <v-chip v-if="index < 1" size="x-small" class="font-weight-bold" color="indigo" variant="flat">
                    {{ item.title }}
                  </v-chip>
                  <span v-if="index === 1" class="text-caption text-indigo font-weight-bold ms-1">
                    (+{{ (selectedSchoolId || []).length - 1 }})
                  </span>
                </template>
              </v-autocomplete>
            </v-col>

            <v-col cols="12" sm="6" md="4">
              <v-autocomplete
                v-model="selectedSubjectId"
                :items="subjectsList"
                item-title="name"
                item-value="id"
                label="المادة الدراسية"
                placeholder="تصفية حسب المادة..."
                clearable
                density="compact"
                variant="outlined"
                rounded="lg"
                hide-details
                prepend-inner-icon="mdi-book-education-outline"
                @update:model-value="onSubjectFilterChange"
              />
            </v-col>
          </template>

          <!-- حقل فلتر حالة وتدقيق ورقة الإجابة -->
          <v-col cols="12" sm="6" md="2">
            <v-select
              v-model="filterStatus"
              :items="statusFilterFieldOptions"
              item-title="title"
              item-value="value"
              label="حالة ورقة الإجابة والتصحيح"
              placeholder="تصفية بحالة الورقة..."
              clearable
              density="compact"
              variant="outlined"
              rounded="lg"
              hide-details
              prepend-inner-icon="mdi-list-status"
              @update:model-value="onStatusFilterChange"
            />
          </v-col>
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
              الاختبارات ومسحوبات الدفعات ({{ filteredExamsTable.length }})
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
              class="rounded-lg"
            />
          </div>
        </div>

        <v-window v-model="masterTab">
          <!-- 1. تبويب مكاتب التربية بالمحافظات -->
          <v-window-item value="offices" v-if="institutionType === 'school'">
            <custom-data-table
              :key="'offices-tbl-' + filteredOfficesTable.length + '-' + normalizeIds(selectedOfficeId).join('-')"
              v-model="selectedOfficeMasterRows"
              :items="officeMasterTableItems"
              :getData="getOfficeMasterData"
              :headers="officeMasterHeaders"
              :customLoading="loadingMaster"
              :hasFilter="false"
              :log="false"
              :restore="false"
              :numbering="true"
              :showSelect="true"
              :actions="false"
              :search="false"
              class="bg-transparent"
            >
              <template v-slot:item-slot="{ item, key, index }">
                <template v-if="key === 'numbering'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'office_name'">
                  <div class="d-flex align-center py-2" style="min-width: 280px;">
                    <v-avatar color="primary" variant="tonal" size="36" class="me-3 rounded-lg flex-shrink-0">
                      <v-icon color="primary" size="20">mdi-office-building-outline</v-icon>
                    </v-avatar>
                    <div>
                      <div class="font-weight-bold text-subtitle-2 text-on-surface text-wrap">{{ item.office_name }}</div>
                      <div class="text-caption text-medium-emphasis">المحافظة: {{ item.governorate_name }}</div>
                    </div>
                  </div>
                </template>

                <template v-else-if="key === 'directorates_count'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-subtitle-2">{{ item.directorates_count ?? 0 }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'schools_count'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-subtitle-2">{{ item.schools_count ?? 0 }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'exams_count'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-subtitle-2">{{ item.exams_count ?? 0 }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'total_students'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-subtitle-2">{{ item.total_students ?? 0 }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'completed_count'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-primary">{{ item.completed_count || 0 }} ورقة</span>
                  </div>
                </template>

                <template v-else-if="key === 'completion_rate'">
                  <div class="d-flex align-center justify-center gap-2 px-1">
                    <v-progress-linear
                      :model-value="item.completion_rate || 0"
                      :color="(item.completion_rate >= 100) ? 'success' : (item.completion_rate > 0 ? 'warning' : 'primary')"
                      height="8"
                      rounded
                      style="min-width: 60px; max-width: 80px;"
                    />
                    <span class="text-caption font-weight-bold">{{ item.completion_rate || 0 }}%</span>
                  </div>
                </template>

                <template v-else-if="key === 'actions'">
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
                      prepend-icon="mdi-file-document-multiple-outline"
                      @click="openOfficeSubmissions(item)"
                    >
                      سجل أوراق المكتب
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </v-window-item>

          <!-- 2. تبويب إدارات التربية بالمديريات -->
          <v-window-item value="directorates" v-if="institutionType === 'school'">
            <custom-data-table
              :key="'dirs-tbl-' + filteredDirectoratesTable.length + '-' + normalizeIds(selectedDirectorateId).join('-') + '-' + normalizeIds(selectedOfficeId).join('-')"
              v-model="selectedDirectorateMasterRows"
              :items="directorateMasterTableItems"
              :getData="getDirectorateMasterData"
              :headers="directorateMasterHeaders"
              :customLoading="loadingMaster"
              :hasFilter="false"
              :log="false"
              :restore="false"
              :numbering="true"
              :showSelect="true"
              :actions="false"
              :search="false"
              class="bg-transparent"
            >
              <template v-slot:item-slot="{ item, key, index }">
                <template v-if="key === 'numbering'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'name'">
                  <div class="d-flex align-center py-2" style="min-width: 280px;">
                    <v-avatar color="teal" variant="tonal" size="36" class="me-3 rounded-lg flex-shrink-0">
                      <v-icon color="teal" size="20">mdi-map-marker-radius-outline</v-icon>
                    </v-avatar>
                    <div>
                      <div class="font-weight-bold text-subtitle-2 text-on-surface text-wrap">{{ item.name }}</div>
                    </div>
                  </div>
                </template>

                <template v-else-if="key === 'office_name'">
                  <div class="d-flex justify-center align-center">
                    <span class="text-body-2 font-weight-medium">{{ item.office_name || '-' }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'schools_count'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-subtitle-2">{{ item.schools_count ?? 0 }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'exams_count'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-subtitle-2">{{ item.exams_count ?? 0 }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'total_students'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-subtitle-2">{{ item.total_students ?? 0 }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'completed_count'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-teal">{{ item.completed_count || 0 }} ورقة</span>
                  </div>
                </template>

                <template v-else-if="key === 'completion_rate'">
                  <div class="d-flex align-center justify-center gap-2 px-1">
                    <v-progress-linear
                      :model-value="item.completion_rate || 0"
                      :color="(item.completion_rate >= 100) ? 'success' : (item.completion_rate > 0 ? 'warning' : 'teal')"
                      height="8"
                      rounded
                      style="min-width: 60px; max-width: 80px;"
                    />
                    <span class="text-caption font-weight-bold">{{ item.completion_rate || 0 }}%</span>
                  </div>
                </template>

                <template v-else-if="key === 'actions'">
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
                      prepend-icon="mdi-file-document-multiple-outline"
                      @click="openDirectorateSubmissions(item)"
                    >
                      سجل أوراق المديرية
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </v-window-item>

          <!-- 3. تبويب المراكز الامتحانية والمدارس / الجامعات / المعاهد -->
          <v-window-item value="schools">
            <custom-data-table
              :key="'schools-tbl-' + filteredSchoolsTable.length + '-' + normalizeIds(selectedSchoolId).join('-') + '-' + normalizeIds(selectedDirectorateId).join('-')"
              v-model="selectedSchoolMasterRows"
              :items="schoolMasterTableItems"
              :getData="getSchoolMasterData"
              :headers="schoolMasterHeaders"
              :customLoading="loadingMaster"
              :hasFilter="false"
              :log="false"
              :restore="false"
              :numbering="true"
              :showSelect="true"
              :actions="false"
              :search="false"
              class="bg-transparent"
            >
              <template v-slot:item-slot="{ item, key, index }">
                <template v-if="key === 'numbering'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'name' || key === 'school_name'">
                  <div class="d-flex align-center py-2" style="min-width: 280px;">
                    <v-avatar color="indigo" variant="tonal" size="36" class="me-3 rounded-lg flex-shrink-0">
                      <v-icon color="indigo" size="20">mdi-school-outline</v-icon>
                    </v-avatar>
                    <div>
                      <div class="font-weight-bold text-subtitle-2 text-on-surface text-wrap">{{ item.name || item.school_name }}</div>
                    </div>
                  </div>
                </template>

                <template v-else-if="key === 'institution_type'">
                  <div class="d-flex justify-center align-center">
                    <v-chip size="x-small" :color="item.institution_type === 'university' ? 'purple' : (item.institution_type === 'institute' ? 'amber' : 'primary')" variant="tonal" class="font-weight-bold">
                      {{ item.institution_type === 'university' ? 'جامعي' : (item.institution_type === 'institute' ? 'مهني/معهد' : 'مدرسي') }}
                    </v-chip>
                  </div>
                </template>

                <template v-else-if="key === 'directorate_name'">
                  <div class="d-flex justify-center align-center">
                    <span class="text-body-2">{{ item.directorate_name }} • {{ item.governorate_name }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'subject_name'">
                  <div class="d-flex align-center justify-center flex-wrap gap-1 py-1" style="min-width: 150px;">
                    <template v-if="item.subjects && item.subjects.length > 0">
                      <v-chip
                        v-for="(subj, sIdx) in item.subjects.slice(0, 2)"
                        :key="sIdx"
                        size="x-small"
                        color="teal"
                        variant="tonal"
                        class="font-weight-bold"
                      >
                        {{ subj }}
                      </v-chip>
                      <v-tooltip v-if="item.subjects.length > 2" location="top">
                        <template #activator="{ props: tProps }">
                          <v-chip
                            v-bind="tProps"
                            size="x-small"
                            color="primary"
                            variant="flat"
                            class="font-weight-bold cursor-pointer"
                            @click.stop="openSchoolExamsDialog(item)"
                          >
                            +{{ item.subjects.length - 2 }}
                          </v-chip>
                        </template>
                        <span>{{ item.subjects.slice(2).join('، ') }}</span>
                      </v-tooltip>
                    </template>
                    <span v-else class="text-caption text-medium-emphasis">{{ item.subject_name || '—' }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'exams_count'">
                  <div class="d-flex justify-center align-center">
                    <v-tooltip location="top" text="انقر لمعاينة قائمة الاختبارات والمواد لهذا المركز">
                      <template #activator="{ props }">
                        <v-chip
                          v-bind="props"
                          size="small"
                          color="primary"
                          variant="tonal"
                          class="font-weight-bold cursor-pointer elevation-0"
                          prepend-icon="mdi-format-list-bulleted"
                          @click.stop="openSchoolExamsDialog(item)"
                        >
                          {{ item.exams_count }} اختبار
                        </v-chip>
                      </template>
                    </v-tooltip>
                  </div>
                </template>

                <template v-else-if="key === 'total_students'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-subtitle-2">{{ item.total_students }} ورقة</span>
                  </div>
                </template>

                <template v-else-if="key === 'completed_count'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-indigo">{{ item.completed_count || 0 }} ورقة</span>
                  </div>
                </template>

                <template v-else-if="key === 'completion_rate'">
                  <div class="d-flex align-center justify-center gap-2 px-1">
                    <v-progress-linear
                      :model-value="item.completion_rate || 0"
                      :color="(item.completion_rate >= 100) ? 'success' : (item.completion_rate > 0 ? 'warning' : 'indigo')"
                      height="8"
                      rounded
                      style="min-width: 60px; max-width: 80px;"
                    />
                    <span class="text-caption font-weight-bold">{{ item.completion_rate || 0 }}%</span>
                  </div>
                </template>

                <template v-else-if="key === 'average_score'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold">{{ item.average_score || 0 }}%</span>
                  </div>
                </template>

                <template v-else-if="key === 'actions'">
                  <div class="d-flex align-center justify-center gap-1">
                    <v-tooltip location="top" text="استعراض تفاصيل الاختبارات والمواد">
                      <template #activator="{ props }">
                        <v-btn
                          v-bind="props"
                          size="small"
                          color="secondary"
                          variant="tonal"
                          icon="mdi-format-list-text"
                          rounded="lg"
                          @click.stop="openSchoolExamsDialog(item)"
                        />
                      </template>
                    </v-tooltip>
                    <v-btn
                      size="small"
                      color="indigo"
                      variant="tonal"
                      rounded="lg"
                      class="font-weight-bold"
                      prepend-icon="mdi-file-document-check-outline"
                      @click="openSchoolSubmissions(item)"
                    >
                      سجل أوراق المركز
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </v-window-item>

          <!-- 4. تبويب الاختبارات الأكاديمية ومسحوبات الدفعات -->
          <v-window-item value="exams">
            <custom-data-table
              :key="'exams-tbl-' + filteredExamsTable.length + '-' + normalizeIds(selectedOfficeId).join('-')"
              v-model="selectedExamMasterRows"
              :items="examMasterTableItems"
              :getData="getExamMasterData"
              :headers="examMasterHeaders"
              :customLoading="loadingMaster"
              :hasFilter="false"
              :log="false"
              :restore="false"
              :numbering="true"
              :showSelect="true"
              :actions="false"
              :search="false"
              class="bg-transparent"
            >
              <template v-slot:item-slot="{ item, key, index }">
                <template v-if="key === 'numbering'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'uniqueCode'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-mono font-weight-bold text-caption px-2 py-1 rounded bg-grey-lighten-4 border">
                      {{ item.uniqueCode }}
                    </span>
                  </div>
                </template>

                <template v-else-if="key === 'title' || key === 'exam_title'">
                  <div class="py-2" style="min-width: 280px;">
                    <div class="font-weight-bold text-subtitle-2 text-on-surface text-wrap">{{ item.title }}</div>
                    <div class="text-caption text-medium-emphasis">المادة: {{ item.subject_name || 'عام' }}</div>
                  </div>
                </template>

                <template v-else-if="key === 'schools_count'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-subtitle-2">{{ item.schools_count ?? 0 }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'total_students'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-subtitle-2">{{ item.total_students || item.total_registered || 0 }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'completed_count'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-primary">{{ item.completed_count || 0 }} ورقة</span>
                  </div>
                </template>

                <template v-else-if="key === 'completion_rate'">
                  <div class="d-flex align-center justify-center gap-2 px-1">
                    <v-progress-linear
                      :model-value="item.completion_rate || 0"
                      :color="(item.completion_rate >= 100) ? 'success' : (item.completion_rate > 0 ? 'warning' : 'primary')"
                      height="8"
                      rounded
                      style="min-width: 60px; max-width: 80px;"
                    />
                    <span class="text-caption font-weight-bold">{{ item.completion_rate || 0 }}%</span>
                  </div>
                </template>

                <template v-else-if="key === 'dispatch_status'">
                  <div class="d-flex justify-center align-center">
                    <v-chip
                      size="small"
                      :color="item.dispatch_status === 'dispatched' ? 'success' : (item.dispatch_status === 'partial' ? 'warning' : 'grey')"
                      variant="tonal"
                      class="font-weight-bold"
                    >
                      {{ item.dispatch_status === 'dispatched' ? 'مرحل بالكامل' : (item.dispatch_status === 'partial' ? 'ترحيل جزئي' : 'غير مرحل') }}
                    </v-chip>
                  </div>
                </template>

                <template v-else-if="key === 'actions'">
                  <div class="d-flex align-center justify-center gap-2">
                    <v-btn
                      size="small"
                      color="primary"
                      variant="flat"
                      rounded="lg"
                      class="font-weight-bold px-3"
                      prepend-icon="mdi-file-document-check-outline"
                      @click="openExamSubmissions(item)"
                    >
                      فتح سجل أوراق الاختبار
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </v-window-item>
        </v-window>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 2. DETAIL VIEW: سجل أوراق إجابة المركز / الاختبار التفصيلي      -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <div v-else class="detail-view-container">
      <!-- شريط التنقل الهيكلي واختيار الاختبار والعمليات المجمعة -->
      <div class="main-card pa-4 rounded-2xl mb-4 bg-surface border elevation-1">
        <div class="d-flex align-center justify-space-between flex-wrap gap-3">
          <!-- مسار التنقل وزر العودة -->
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
              <span class="text-primary font-weight-black">{{ selectedExamObj?.title || 'سجل الأوراق الممسوحة' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- شريط تصفية نتائج أوراق الإجابة (الاختبار والنموذج والحالة والمتوسط) -->
      <div class="main-card pa-4 rounded-2xl mb-4 bg-surface border">
        <v-row dense class="align-center">
          <v-col cols="12" sm="6" md="4">
            <v-autocomplete
              v-model="selectedExamId"
              :items="examsList"
              item-title="title"
              item-value="id"
              label="الاختبار المعروض"
              placeholder="اختر الاختبار..."
              density="compact"
              variant="outlined"
              hide-details
              prepend-inner-icon="mdi-file-document-edit-outline"
              @update:model-value="onExamChange"
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
              v-model="filterStatus"
              :items="statusFilterFieldOptions"
              item-title="title"
              item-value="value"
              placeholder="حالة المسح والتصحيح"
              prepend-inner-icon="mdi-list-status"
              density="compact"
              variant="outlined"
              hide-details
              clearable
              @update:model-value="applyFilters"
            />
          </v-col>

          <v-col cols="12" sm="12" md="4" class="d-flex justify-end align-center gap-2 flex-wrap">
            <v-chip color="indigo" variant="tonal" size="small" class="font-weight-black">
              متوسط الدرجات: {{ statsData.average_score || 0 }}%
            </v-chip>

            <v-btn
              v-if="selectedExamId"
              color="indigo"
              variant="tonal"
              size="small"
              rounded="lg"
              class="font-weight-bold"
              prepend-icon="mdi-clipboard-list-outline"
              @click="$router.push(`/omr-gradebook?exam=${selectedExamId}`)"
            >
              كشف الرصد الأكاديمي
            </v-btn>

            <v-btn
              variant="tonal"
              color="error"
              size="small"
              rounded="lg"
              class="font-weight-bold"
              prepend-icon="mdi-filter-remove-outline"
              @click="resetDetailFilters"
            >
              تفريغ الفلاتر
            </v-btn>
          </v-col>
        </v-row>
      </div>

      <!-- جدول أوراق الإجابة المصححة والممسوحة -->
      <div class="main-card rounded-2xl overflow-hidden mb-6 elevation-1">
        <custom-data-table
          v-model="selectedSubmissionIds"
          :headers="detailHeaders"
          :items="tableItems"
          :getData="fetchSubmissionsRoster"
          :customLoading="loadingRecords"
          class="bg-transparent"
          :hasFilter="false"
          :log="false"
          :restore="false"
          :numbering="true"
          :showSelect="true"
          :itemValue="'id'"
          :actions="false"
        >
          <template v-slot:item-slot="{ item, key, index }">
            <!-- الترقيم الموحد -->
            <template v-if="key === 'numbering'">
              <div class="d-flex justify-center align-center">
                <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
              </div>
            </template>

            <!-- صورة الورقة الممسوحة المصغرة مع إمكانية التكبير -->
            <template v-else-if="key === 'sheet_thumbnail'">
              <div class="d-flex justify-center align-center py-1">
                <v-tooltip location="top" text="انقر لمعاينة صورة ورقة الإجابة الممسوحة بدقة عالية">
                  <template #activator="{ props }">
                    <div
                      v-bind="props"
                      class="sheet-thumb-wrapper rounded-lg border overflow-hidden cursor-pointer"
                      style="width: 44px; height: 56px; background: #f8fafc;"
                      @click="previewSheetImage(item)"
                    >
                      <v-img
                        v-if="item.original_image"
                        :src="fixImageUrl(item.original_image)"
                        cover
                        class="w-100 h-100"
                      />
                      <div v-else class="d-flex align-center justify-center w-100 h-100 text-grey">
                        <v-icon size="20">mdi-file-document-outline</v-icon>
                      </div>
                    </div>
                  </template>
                </v-tooltip>
              </div>
            </template>

            <!-- رقم الجلوس أو الرقم الأكاديمي -->
            <template v-else-if="key === 'seat_number'">
              <div class="d-flex justify-center align-center">
                <span class="font-weight-black font-mono text-primary text-subtitle-2">
                  {{ item.seat_number || '-' }}
                </span>
              </div>
            </template>

            <!-- اسم الطالب والمادة -->
            <template v-else-if="key === 'student_name'">
              <div class="py-1">
                <div class="font-weight-bold text-body-2 text-on-surface">{{ item.student_name || 'طالب غير محدد' }}</div>
                <div class="text-caption text-medium-emphasis">{{ item.subject_name || selectedExamObj?.subject_name || '-' }}</div>
              </div>
            </template>

            <!-- كود النموذج الامتحاني -->
            <template v-else-if="key === 'exam_version_code'">
              <div class="d-flex justify-center align-center">
                <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                  {{ item.exam_version_code || 'نموذج عام' }}
                </v-chip>
              </div>
            </template>

            <!-- الدرجة الكلية -->
            <template v-else-if="key === 'total_score'">
              <div class="text-center py-1">
                <span class="text-subtitle-2 font-weight-black text-on-surface">
                  {{ item.total_score != null ? item.total_score : '-' }}
                </span>
                <div v-if="item.mcq_score != null" class="text-caption text-medium-emphasis">
                  خيارات: {{ item.mcq_score }} | مقالي: {{ item.essay_score || 0 }}
                </div>
              </div>
            </template>

            <!-- نسبة الثقة الضوئية OMR Confidence -->
            <template v-else-if="key === 'confidence'">
              <div class="d-flex align-center justify-center gap-1">
                <v-progress-circular
                  :model-value="Math.round((item.overall_confidence || 0.95) * 100)"
                  :color="(item.overall_confidence || 0.95) >= 0.85 ? 'success' : 'warning'"
                  size="26"
                  width="3"
                />
                <span class="text-caption font-weight-bold">
                  {{ Math.round((item.overall_confidence || 0.95) * 100) }}%
                </span>
              </div>
            </template>

            <!-- حالة المعالجة الضوئية والتصحيح -->
            <template v-else-if="key === 'status'">
              <div class="d-flex justify-center align-center">
                <v-chip
                  size="small"
                  :color="getStatusColor(item.status)"
                  variant="tonal"
                  class="font-weight-bold"
                >
                  {{ item.status_display || getStatusText(item.status) }}
                </v-chip>
              </div>
            </template>

            <!-- الإجراءات المباشرة -->
            <template v-else-if="key === 'actions'">
              <div class="d-flex align-center justify-center gap-1">
                <v-tooltip location="top" text="فحص تفاصيل الورقة الكاملة والفقاعات">
                  <template #activator="{ props }">
                    <v-btn
                      v-bind="props"
                      size="small"
                      color="primary"
                      variant="flat"
                      icon="mdi-file-eye-outline"
                      rounded="lg"
                      @click="navigateToDetail(item)"
                    />
                  </template>
                </v-tooltip>

                <v-tooltip location="top" text="معاينة صورة الورقة الممسوحة">
                  <template #activator="{ props }">
                    <v-btn
                      v-bind="props"
                      size="small"
                      color="secondary"
                      variant="tonal"
                      icon="mdi-image-search-outline"
                      rounded="lg"
                      @click="previewSheetImage(item)"
                    />
                  </template>
                </v-tooltip>

                <v-tooltip location="top" text="إعادة المعالجة الضوئية للورقة">
                  <template #activator="{ props }">
                    <v-btn
                      v-bind="props"
                      size="small"
                      color="warning"
                      variant="tonal"
                      icon="mdi-refresh"
                      rounded="lg"
                      :loading="reprocessingId === item.id"
                      @click="reprocessSingleSheet(item)"
                    />
                  </template>
                </v-tooltip>

                <v-tooltip location="top" text="حذف ورقة الإجابة">
                  <template #activator="{ props }">
                    <v-btn
                      v-bind="props"
                      size="small"
                      color="error"
                      variant="tonal"
                      icon="mdi-delete-outline"
                      rounded="lg"
                      @click="confirmDeleteSubmission(item)"
                    />
                  </template>
                </v-tooltip>
              </div>
            </template>
          </template>
        </custom-data-table>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 3. نافذة تفاصيل اختبارات ومواد المدرسة / المركز الامتحاني      -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <v-dialog v-model="schoolExamsDialog" width="1180px" max-width="95vw" scrollable>
      <v-card rounded="2xl" class="border elevation-6 overflow-hidden main-card">
        <v-card-title class="d-flex align-center justify-space-between bg-surface pa-4 px-6 border-b">
          <div class="d-flex align-center gap-3">
            <v-avatar color="primary" variant="tonal" size="44" class="rounded-xl flex-shrink-0">
              <v-icon color="primary" size="24">mdi-school</v-icon>
            </v-avatar>
            <div>
              <div class="text-subtitle-1 font-weight-black text-on-surface">{{ selectedSchoolDialogItem?.name || selectedSchoolDialogItem?.school_name }}</div>
              <div class="text-caption text-medium-emphasis d-flex align-center gap-2 flex-wrap mt-0.5">
                <span>{{ selectedSchoolDialogItem?.directorate_name }} • {{ selectedSchoolDialogItem?.governorate_name }}</span>
                <span>|</span>
                <span>إجمالي الطلاب: <strong class="text-primary">{{ selectedSchoolDialogItem?.total_students || 0 }} طالب</strong></span>
                <span>|</span>
                <span>عدد الاختبارات: <strong class="text-teal">{{ selectedSchoolDialogItem?.exams?.length || selectedSchoolDialogItem?.exams_count || 0 }} اختبار</strong></span>
              </div>
            </div>
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" @click="schoolExamsDialog = false" />
        </v-card-title>

        <v-card-text class="pa-4 pa-md-5 bg-surface">
          <div v-if="!selectedSchoolDialogItem?.exams || selectedSchoolDialogItem.exams.length === 0" class="text-center py-8">
            <v-icon size="48" color="grey">mdi-file-document-outline</v-icon>
            <div class="text-body-1 text-medium-emphasis mt-2">لا توجد اختبارات مسجلة لهذه المدرسة حالياً</div>
          </div>

          <div v-else class="d-flex flex-column gap-3">
            <v-alert
              type="info"
              variant="tonal"
              density="compact"
              rounded="xl"
              class="mb-2 text-caption font-weight-medium"
            >
              <template v-slot:prepend>
                <v-icon size="20" color="info">mdi-information-outline</v-icon>
              </template>
              كل صف أدناه يمثل <strong>اختباراً معتمداً</strong> مقيد به طلاب المدرسة، وموضح أمامه <strong>النماذج الامتحانية</strong>، مع إمكانية فتح سجل أوراق أي اختبار مباشرة.
            </v-alert>

            <div class="main-card rounded-2xl overflow-hidden border">
              <custom-data-table
                :items="schoolExamsTableItems"
                :getData="getSchoolExamsData"
                :headers="schoolExamsHeaders"
                :hasFilter="false"
                :log="false"
                :restore="false"
                :numbering="true"
                :showSelect="false"
                :actions="false"
                :search="false"
              >
                <template v-slot:item-slot="{ item, key, index }">
                  <template v-if="key === 'numbering'">
                    <div class="d-flex justify-center align-center">
                      <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
                    </div>
                  </template>

                  <template v-else-if="key === 'code'">
                    <div class="d-flex justify-center align-center">
                      <v-chip size="small" color="primary" variant="tonal" class="font-mono font-weight-bold px-2">
                        {{ item.code }}
                      </v-chip>
                    </div>
                  </template>

                  <template v-else-if="key === 'title'">
                    <div class="d-flex align-center gap-2.5 py-1.5">
                      <v-avatar color="teal" variant="tonal" size="32" class="rounded-lg flex-shrink-0">
                        <v-icon color="teal" size="18">mdi-book-education-outline</v-icon>
                      </v-avatar>
                      <div class="text-truncate">
                        <div class="font-weight-bold text-body-2 text-on-surface text-truncate" :title="item.title">
                          {{ item.title }}
                        </div>
                        <div class="d-flex align-center gap-1.5 mt-0.5">
                          <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold px-1.5">
                            اختبار معتمد
                          </v-chip>
                        </div>
                      </div>
                    </div>
                  </template>

                  <template v-else-if="key === 'subject'">
                    <div class="d-flex justify-center align-center">
                      <v-chip size="small" color="teal" variant="flat" class="font-weight-bold px-2.5">
                        <v-icon size="13" start>mdi-book-outline</v-icon>
                        {{ item.subject || 'عام' }}
                      </v-chip>
                    </div>
                  </template>

                  <template v-else-if="key === 'students_count'">
                    <div class="d-flex justify-center align-center">
                      <v-chip size="small" color="primary" variant="tonal" class="font-weight-black px-2.5">
                        <v-icon size="13" start>mdi-account-group-outline</v-icon>
                        {{ item.students_count || 0 }} ورقة
                      </v-chip>
                    </div>
                  </template>

                  <template v-else-if="key === 'versions'">
                    <div v-if="item.versions && item.versions.length > 0" class="d-flex align-center justify-center gap-1.5 flex-wrap py-1">
                      <v-chip
                        v-for="v in item.versions"
                        :key="v.code"
                        size="x-small"
                        color="indigo"
                        variant="tonal"
                        class="font-weight-bold"
                      >
                        <v-icon size="11" start>mdi-file-document-check-outline</v-icon>
                        نموذج {{ v.code }} ({{ v.students_count }} ورقة)
                      </v-chip>
                    </div>
                    <div v-else class="text-center text-caption text-medium-emphasis">—</div>
                  </template>

                  <template v-else-if="key === 'actions'">
                    <div class="d-flex justify-center align-center">
                      <v-btn
                        size="small"
                        color="primary"
                        variant="flat"
                        rounded="lg"
                        prepend-icon="mdi-file-document-check-outline"
                        class="font-weight-bold px-3"
                        @click="schoolExamsDialog = false; openExamSubmissions(item);"
                      >
                        فتح سجل الأوراق
                      </v-btn>
                    </div>
                  </template>
                </template>
              </custom-data-table>
            </div>
          </div>
        </v-card-text>

        <v-divider />
        <v-card-actions class="pa-4 bg-surface d-flex justify-space-between align-center flex-wrap gap-2">
          <div class="text-caption text-medium-emphasis d-flex align-center gap-1">
            <v-icon size="16" color="primary">mdi-cursor-default-click-outline</v-icon>
            يمكنك فتح سجل أوراق أي اختبار مستقل أو استعراض السجل الشامل للمركز
          </div>
          <div class="d-flex gap-2">
            <v-btn variant="tonal" color="grey" rounded="lg" class="font-weight-bold px-4" @click="schoolExamsDialog = false">
              إغلاق
            </v-btn>
            <v-btn
              color="indigo"
              variant="flat"
              rounded="lg"
              prepend-icon="mdi-file-document-multiple-outline"
              class="font-weight-bold px-4"
              @click="openSchoolSubmissions(selectedSchoolDialogItem); schoolExamsDialog = false;"
            >
              فتح سجل أوراق المركز بالكامل
            </v-btn>
          </div>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 4. نافذة المعاينة السريعة لصورة ورقة الإجابة الممسوحة (Lightbox) -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <v-dialog v-model="imagePreviewDialog" width="860px" max-width="95vw">
      <v-card rounded="2xl" class="border elevation-6 overflow-hidden main-card">
        <v-card-title class="d-flex align-center justify-space-between bg-surface pa-4 px-6 border-b">
          <div class="d-flex align-center gap-2">
            <v-icon color="primary" size="22">mdi-image-search-outline</v-icon>
            <div>
              <div class="text-subtitle-1 font-weight-black text-on-surface">معاينة ورقة إجابة الطالب: {{ previewSubmission?.student_name }}</div>
              <div class="text-caption text-medium-emphasis">رقم الجلوس: {{ previewSubmission?.seat_number }} • {{ previewSubmission?.exam_title }}</div>
            </div>
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" @click="imagePreviewDialog = false" />
        </v-card-title>

        <v-card-text class="pa-4 bg-surface text-center">
          <div v-if="previewSubmission?.original_image" class="border rounded-xl pa-2 bg-grey-lighten-4 overflow-auto" style="max-height: 72vh;">
            <v-img
              :src="fixImageUrl(previewSubmission.original_image)"
              contain
              class="rounded-lg mx-auto"
              style="max-height: 68vh;"
            />
          </div>
          <div v-else class="py-12 text-medium-emphasis">
            <v-icon size="48" color="grey">mdi-image-off-outline</v-icon>
            <div class="mt-2 text-body-2 font-weight-bold">لا توجد صورة ممسوحة مرفقة لهذه الورقة في النظام</div>
          </div>
        </v-card-text>

        <v-divider />
        <v-card-actions class="pa-4 bg-surface d-flex justify-space-between align-center">
          <v-chip color="primary" variant="tonal" class="font-weight-bold">
            درجة الورقة: {{ previewSubmission?.total_score ?? '-' }}
          </v-chip>
          <div class="d-flex gap-2">
            <v-btn variant="tonal" color="grey" rounded="lg" class="font-weight-bold px-4" @click="imagePreviewDialog = false">
              إغلاق
            </v-btn>
            <v-btn
              color="primary"
              variant="flat"
              rounded="lg"
              class="font-weight-bold px-4"
              prepend-icon="mdi-file-eye-outline"
              @click="imagePreviewDialog = false; navigateToDetail(previewSubmission);"
            >
              فحص تفاصيل الورقة الكاملة
            </v-btn>
          </div>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- نافذة تأكيد الحذف -->
    <DeleteDialog
      v-model="deleteDialog"
      title="حذف ورقة الإجابة"
      :message="`هل أنت متأكد من حذف ورقة إجابة الطالب '${submissionToDelete ? submissionToDelete.student_name : ''}' نهائياً؟`"
      @confirm-delete="executeDelete"
    />

    <!-- الإشعارات المنبثقة -->
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
import { submissionsAPI, gradebookAPI } from '@/services/omr/endpoints'
import OMRWorkflowBar from '@/components/OMRWorkflowBar.vue'

export default {
  name: 'OMRSubmissionsView',

  components: {
    OMRWorkflowBar,
  },

  data() {
    return {
      institutionType: 'school', // 'school' | 'university' | 'institute'
      showKpiCards: true,
      activeKpiFilter: null,
      sectorOptions: [
        { title: 'التعليم العام (المدرسي)', value: 'school', icon: 'mdi-school' },
        { title: 'التعليم الجامعي (كليات وجامعات)', value: 'university', icon: 'mdi-domain' },
        { title: 'التعليم الفني والمهني (معاهد)', value: 'institute', icon: 'mdi-tools' }
      ],
      currentView: 'master', // 'master' | 'detail'
      masterTab: 'offices',  // 'offices' | 'directorates' | 'schools' | 'exams'
      loadingMaster: false,
      masterSearchQuery: '',

      educationalOrgs: [],
      allOfficesList: [],
      officesList: [],
      directoratesList: [],
      schoolsList: [],
      examsList: [],
      subjectsList: [],

      selectedOfficeId: [],
      selectedDirectorateId: [],
      selectedSchoolId: [],
      selectedSubjectId: null,
      selectedSubjectName: '',

      selectedOfficeMasterRows: [],
      selectedDirectorateMasterRows: [],
      selectedSchoolMasterRows: [],
      selectedExamMasterRows: [],

      // Stats
      statsData: {
        total: 0,
        completed: 0,
        needs_review: 0,
        failed: 0,
        pending: 0,
        average_score: 0,
      },

      // Master Tables Reactive Items
      officeMasterTableItems: {
        results: [],
        count: 0,
        pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 }
      },
      directorateMasterTableItems: {
        results: [],
        count: 0,
        pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 }
      },
      schoolMasterTableItems: {
        results: [],
        count: 0,
        pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 }
      },
      examMasterTableItems: {
        results: [],
        count: 0,
        pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 }
      },

      officeMasterHeaders: [
        { title: "مكتب التربية والتعليم (المحافظة)", key: "office_name", sortable: true, align: "start", width: "340px", minWidth: "320px" },
        { title: "المديريات", key: "directorates_count", sortable: true, align: "center", width: "95px" },
        { title: "المراكز والمدارس", key: "schools_count", sortable: true, align: "center", width: "125px" },
        { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "95px" },
        { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
        { title: "أوراق مقروءة", key: "completed_count", sortable: true, align: "center", width: "120px" },
        { title: "نسبة الإنجاز", key: "completion_rate", sortable: true, align: "center", width: "130px" },
        { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "220px" },
      ],

      directorateMasterHeaders: [
        { title: "إدارة التربية والتعليم (المديرية)", key: "name", sortable: true, align: "start", width: "340px", minWidth: "320px" },
        { title: "المكتب التابع له", key: "office_name", sortable: true, align: "center", width: "180px" },
        { title: "المراكز والمدارس", key: "schools_count", sortable: true, align: "center", width: "125px" },
        { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "95px" },
        { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
        { title: "أوراق مقروءة", key: "completed_count", sortable: true, align: "center", width: "120px" },
        { title: "نسبة الإنجاز", key: "completion_rate", sortable: true, align: "center", width: "130px" },
        { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "220px" },
      ],

      schoolMasterHeaders: [
        { title: "المدرسة / المركز الامتحاني", key: "name", sortable: true, align: "start", width: "320px", minWidth: "280px" },
        { title: "نوع المؤسسة", key: "institution_type", sortable: true, align: "center", width: "105px" },
        { title: "المحافظة والمديرية", key: "directorate_name", sortable: true, align: "center", width: "170px" },
        { title: "المادة الدراسية", key: "subject_name", sortable: true, align: "center", width: "160px" },
        { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "105px" },
        { title: "إجمالي الأوراق", key: "total_students", sortable: true, align: "center", width: "110px" },
        { title: "أوراق مقروءة", key: "completed_count", sortable: true, align: "center", width: "115px" },
        { title: "نسبة الإنجاز", key: "completion_rate", sortable: true, align: "center", width: "120px" },
        { title: "متوسط الدرجات", key: "average_score", sortable: true, align: "center", width: "110px" },
        { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "190px" },
      ],

      examMasterHeaders: [
        { title: "رمز الاختبار", key: "uniqueCode", sortable: true, align: "center", width: "140px" },
        { title: "عنوان الاختبار والمادة", key: "title", sortable: true, align: "start", width: "340px", minWidth: "300px" },
        { title: "المدارس المشاركة", key: "schools_count", sortable: true, align: "center", width: "125px" },
        { title: "المقيدون", key: "total_students", sortable: true, align: "center", width: "110px" },
        { title: "أوراق مقروءة", key: "completed_count", sortable: true, align: "center", width: "120px" },
        { title: "نسبة المعالجة", key: "completion_rate", sortable: true, align: "center", width: "130px" },
        { title: "حالة الكنترول", key: "dispatch_status", sortable: true, align: "center", width: "130px" },
        { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "160px" },
      ],

      // School Exams Dialog
      schoolExamsDialog: false,
      selectedSchoolDialogItem: null,
      schoolExamsHeaders: [
        { title: "رمز الاختبار", key: "code", sortable: true, align: "center", width: "135px" },
        { title: "عنوان الاختبار والمواصفات", key: "title", sortable: true, align: "start" },
        { title: "المادة الدراسية", key: "subject", sortable: true, align: "center", width: "120px" },
        { title: "أوراق المركز", key: "students_count", sortable: true, align: "center", width: "105px" },
        { title: "النماذج المخصصة للطلاب وتوزيعها", key: "versions", sortable: false, align: "center", width: "230px" },
        { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "140px" },
      ],
      schoolExamsTableItems: {
        results: [],
        count: 0,
        pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 }
      },

      // Detail View State
      selectedExamId: null,
      selectedExamObj: null,
      filterOrganization: null,
      searchQuery: '',
      filterVersion: 'all',
      filterStatus: null,
      availableVersions: ['A', 'B', 'C', 'D'],
      selectedSubmissionIds: [],
      loadingRecords: false,
      reprocessingId: null,

      tableItems: {
        results: [],
        count: 0,
        pagination: { count: 0, total: 0, num_pages: 1, current_page: 1, page_size: 15 }
      },

      detailHeaders: [
        { title: "الورقة الممسوحة", key: "sheet_thumbnail", sortable: false, align: "center", width: "90px" },
        { title: "رقم الجلوس", key: "seat_number", sortable: true, align: "center", width: "120px" },
        { title: "اسم الطالب والمادة", key: "student_name", sortable: true, align: "start" },
        { title: "النموذج", key: "exam_version_code", sortable: true, align: "center", width: "100px" },
        { title: "الدرجة الكلية", key: "total_score", sortable: true, align: "center", width: "130px" },
        { title: "دقة OMR", key: "confidence", sortable: true, align: "center", width: "110px" },
        { title: "حالة التصحيح", key: "status", sortable: true, align: "center", width: "135px" },
        { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "170px" },
      ],

      statusOptions: [
        { title: 'جميع الحالات', value: null },
        { title: 'مكتمل ومعتمد (Completed)', value: 'completed' },
        { title: 'يحتاج مراجعة (Needs Review)', value: 'needs_review' },
        { title: 'تمت المراجعة (Reviewed)', value: 'reviewed' },
        { title: 'فشل التصحيح (Failed)', value: 'failed' },
        { title: 'قيد الانتظار (Pending)', value: 'pending' },
      ],

      // Dialogs
      imagePreviewDialog: false,
      previewSubmission: null,
      deleteDialog: false,
      submissionToDelete: null,

      snackbar: {
        show: false,
        text: '',
        color: 'success',
      },

      searchDebounceTimer: null,
    }
  },

  computed: {
    statusFilterFieldOptions() {
      return [
        { title: `إجمالي الأوراق المقروءة (${this.statsData.total || 0} ورقة مسجلة - عرض الكل)`, value: null },
        { title: `أوراق مصححة بنجاح (${this.statsData.completed || 0} مكتملة القراءة بالكامل)`, value: 'completed' },
        { title: `تحتاج مراجعة وتدقيق (${this.statsData.needs_review || 0} شطب أو تظليل مزدوج)`, value: 'needs_review' },
        { title: `فشل قراءة الباركود (${this.statsData.failed || 0} أوراق تالفة أو غير مقروءة)`, value: 'failed' },
      ]
    },

    directoratesOptions() {
      const officeIds = this.normalizeIds(this.selectedOfficeId)
      if (officeIds.length > 0) {
        return (this.directoratesList || []).filter(d => officeIds.includes(d.office_id))
      }
      return this.directoratesList || []
    },

    schoolsOptions() {
      let list = this.schoolsList || []
      if (this.institutionType !== 'all') {
        list = list.filter(s => !s.institution_type || s.institution_type === this.institutionType)
      }
      const dirIds = this.normalizeIds(this.selectedDirectorateId)
      const officeIds = this.normalizeIds(this.selectedOfficeId)

      if (dirIds.length > 0) {
        const dObjs = (this.directoratesList || []).filter(d => dirIds.includes(d.id))
        const dNames = dObjs.map(d => d.name?.replace(/^(إدارة التربية والتعليم - مديرية |مديرية )/, '').trim()).filter(Boolean)
        list = list.filter(s => 
          dirIds.includes(s.directorate_id) ||
          dNames.some(dn => s.directorate_name && s.directorate_name.includes(dn))
        )
      } else if (officeIds.length > 0) {
        const oObjs = (this.officesList || []).filter(o => officeIds.includes(o.id))
        const oGovs = oObjs.map(o => o.governorate_name?.trim()).filter(Boolean)
        list = list.filter(s => 
          officeIds.includes(s.office_id) ||
          oGovs.some(og => s.governorate_name && s.governorate_name.includes(og))
        )
      }
      return list
    },

    realOfficesList() {
      return (this.educationalOrgs || []).filter(o => o.company_level === 30)
    },

    realDirectoratesList() {
      const officeIds = this.normalizeIds(this.selectedOfficeId)
      if (officeIds.length > 0) {
        return (this.educationalOrgs || []).filter(o => o.company_level === 40 && officeIds.includes(o.fk_parent_organization))
      }
      return (this.educationalOrgs || []).filter(o => o.company_level === 40)
    },

    selectedOfficeObj() {
      const officeIds = this.normalizeIds(this.selectedOfficeId)
      if (officeIds.length === 0) return null
      return (this.realOfficesList || []).find(o => officeIds.includes(o.id)) || (this.officesList || []).find(o => officeIds.includes(o.id)) || null
    },

    selectedDirectorateObj() {
      const dirIds = this.normalizeIds(this.selectedDirectorateId)
      if (dirIds.length === 0) return null
      return (this.realDirectoratesList || []).find(d => dirIds.includes(d.id)) || (this.directoratesList || []).find(d => dirIds.includes(d.id)) || null
    },

    filteredOfficesTable() {
      let list = this.officesList || []
      const selIds = this.normalizeIds(this.selectedOfficeId)
      if (selIds.length > 0) {
        list = list.filter(o => selIds.includes(Number(o.id)))
      }
      if (this.selectedSubjectId) {
        list = list.filter(o => (o.exams_count || 0) > 0)
      }
      if (this.masterSearchQuery && this.masterSearchQuery.trim()) {
        const q = this.masterSearchQuery.trim().toLowerCase()
        list = list.filter(o => (o.office_name || '').toLowerCase().includes(q) || (o.governorate_name || '').toLowerCase().includes(q))
      }
      return list
    },

    filteredDirectoratesTable() {
      let list = this.directoratesList || []
      const officeIds = this.normalizeIds(this.selectedOfficeId)
      if (officeIds.length > 0) {
        list = list.filter(d => officeIds.includes(Number(d.office_id)))
      }
      const dirIds = this.normalizeIds(this.selectedDirectorateId)
      if (dirIds.length > 0) {
        list = list.filter(d => dirIds.includes(Number(d.id)))
      }
      if (this.selectedSubjectId) {
        list = list.filter(d => (d.exams_count || 0) > 0)
      }
      if (this.masterSearchQuery && this.masterSearchQuery.trim()) {
        const q = this.masterSearchQuery.trim().toLowerCase()
        list = list.filter(d => (d.name || '').toLowerCase().includes(q) || (d.office_name || '').toLowerCase().includes(q))
      }
      return list
    },

    filteredSchoolsTable() {
      let list = this.schoolsList || []
      if (this.institutionType !== 'all') {
        list = list.filter(s => !s.institution_type || s.institution_type === this.institutionType)
      }
      const dirIds = this.normalizeIds(this.selectedDirectorateId)
      const officeIds = this.normalizeIds(this.selectedOfficeId)

      if (dirIds.length > 0) {
        const dObjs = (this.directoratesList || []).filter(d => dirIds.includes(Number(d.id)))
        const dNames = dObjs.map(d => d.name?.replace(/^(إدارة التربية والتعليم - مديرية |مديرية )/, '').trim()).filter(Boolean)
        list = list.filter(s => 
          dirIds.includes(Number(s.directorate_id)) ||
          dNames.some(dn => s.directorate_name && s.directorate_name.includes(dn))
        )
      } else if (officeIds.length > 0) {
        const oObjs = (this.officesList || []).filter(o => officeIds.includes(Number(o.id)))
        const oGovs = oObjs.map(o => o.governorate_name?.trim()).filter(Boolean)
        list = list.filter(s => 
          officeIds.includes(Number(s.office_id)) ||
          oGovs.some(og => s.governorate_name && s.governorate_name.includes(og))
        )
      }
      const schoolIds = this.normalizeIds(this.selectedSchoolId)
      if (schoolIds.length > 0) {
        list = list.filter(s => schoolIds.includes(Number(s.id)))
      }
      if (this.selectedSubjectId) {
        const sObj = (this.subjectsList || []).find(s => s.id === this.selectedSubjectId)
        const sName = sObj?.name?.trim()
        list = list.filter(s => {
          if (s.subjects && Array.isArray(s.subjects)) {
            return s.subjects.some(sub => sub === sName || (sName && sub.includes(sName)))
          }
          return s.subject_name === sName || (sName && s.subject_name && s.subject_name.includes(sName))
        })
      }
      if (this.masterSearchQuery && this.masterSearchQuery.trim()) {
        const q = this.masterSearchQuery.trim().toLowerCase()
        list = list.filter(s => 
          (s.name && s.name.toLowerCase().includes(q)) ||
          (s.directorate_name && s.directorate_name.toLowerCase().includes(q)) ||
          (s.governorate_name && s.governorate_name.toLowerCase().includes(q)) ||
          (s.subject_name && s.subject_name.toLowerCase().includes(q))
        )
      }
      return list
    },

    filteredExamsTable() {
      let list = this.examsList || []
      if (this.institutionType && this.institutionType !== 'all') {
        list = list.filter(e => e.institution_type === this.institutionType)
      }
      const dirIds = this.normalizeIds(this.selectedDirectorateId)
      const officeIds = this.normalizeIds(this.selectedOfficeId)

      if (dirIds.length > 0) {
        list = list.filter(e => dirIds.includes(Number(e.directorate_id)))
      } else if (officeIds.length > 0) {
        list = list.filter(e => officeIds.includes(Number(e.office_id)) || officeIds.includes(Number(e.governorate_id)))
      }
      if (this.selectedSubjectId) {
        list = list.filter(e => e.subject_id === this.selectedSubjectId || e.subject === this.selectedSubjectId)
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

    versionFilterOptions() {
      const opts = [{ text: 'جميع النماذج', value: 'all' }]
      if (this.availableVersions && this.availableVersions.length) {
        this.availableVersions.forEach(v => {
          if (v) opts.push({ text: `النموذج ${v}`, value: v })
        })
      }
      return opts
    },

    isAllCurrentSelected() {
      const currentIds = (this.tableItems.results || []).map(s => s.id).filter(Boolean)
      if (!currentIds.length) return false
      return currentIds.every(id => this.selectedSubmissionIds.includes(id))
    },

    isSomeCurrentSelected() {
      const currentIds = (this.tableItems.results || []).map(s => s.id).filter(Boolean)
      if (!currentIds.length || this.isAllCurrentSelected) return false
      return currentIds.some(id => this.selectedSubmissionIds.includes(id))
    },
  },

  watch: {
    filteredOfficesTable: {
      handler() {
        this.getOfficeMasterData()
      },
      immediate: true,
    },
    filteredDirectoratesTable: {
      handler() {
        this.getDirectorateMasterData()
      },
      immediate: true,
    },
    filteredSchoolsTable: {
      handler() {
        this.getSchoolMasterData()
      },
      immediate: true,
    },
    filteredExamsTable: {
      handler() {
        this.getExamMasterData()
      },
      immediate: true,
    },
  },

  async created() {
    await this.loadEducationalHierarchy()
    await this.loadSubjects()
    await this.fetchStats()
    await this.refreshMasterData()

    const queryExam = this.$route.query.exam || this.$route.query.open_exam_id
    if (queryExam) {
      this.selectedExamId = parseInt(queryExam) || queryExam
      this.selectedExamObj = this.examsList.find(e => e.id === this.selectedExamId) || null
      this.currentView = 'detail'
      await this.fetchSubmissionsRoster({ params: { page: 1, page_size: 15 } })
    } else {
      this.currentView = 'master'
    }
  },

  methods: {
    normalizeIds(val) {
      if (!val) return []
      const arr = Array.isArray(val) ? val : [val]
      const result = []
      for (const item of arr) {
        if (item === null || item === undefined || item === 'all' || item === '') continue
        if (typeof item === 'object') {
          const id = item.id ?? item.value ?? item.raw?.id ?? item.raw?.value
          if (id !== undefined && !isNaN(Number(id)) && Number(id) > 0) {
            result.push(Number(id))
          }
        } else if (!isNaN(Number(item)) && Number(item) > 0) {
          result.push(Number(item))
        } else if (typeof item === 'string' && item.includes(',')) {
          for (const s of item.split(',')) {
            const n = Number(s.trim())
            if (!isNaN(n) && n > 0) result.push(n)
          }
        } else if (typeof item === 'string') {
          const matchOff = (this.allOfficesList || this.officesList || []).find(o => o.office_name === item || o.governorate_name === item)
          if (matchOff && matchOff.id) result.push(Number(matchOff.id))
        }
      }
      return Array.from(new Set(result))
    },

    notify(text, color = 'success') {
      this.snackbar.text = text
      this.snackbar.color = color
      this.snackbar.show = true
    },

    fixImageUrl(url) {
      if (!url) return ''
      if (typeof url !== 'string') return ''
      const token = localStorage.getItem('token') || localStorage.getItem('access_token') || ''
      let cleanUrl = url
      if (url.startsWith('http://') || url.startsWith('https://')) {
        cleanUrl = url
      } else if (this.$fix_image_url) {
        cleanUrl = this.$fix_image_url(url)
      } else if (url.startsWith('/media/')) {
        cleanUrl = url
      } else if (url.startsWith('media/')) {
        cleanUrl = `/${url}`
      } else {
        cleanUrl = `/media/${url}`
      }
      if (token && cleanUrl.includes('/media/')) {
        cleanUrl = `${cleanUrl}${cleanUrl.includes('?') ? '&' : '?'}token=${token}`
      }
      return cleanUrl
    },

    getStatusColor(status) {
      switch (status) {
        case 'completed': return 'success'
        case 'reviewed': return 'teal'
        case 'needs_review': return 'warning'
        case 'failed': return 'error'
        case 'pending':
        case 'aligning':
        case 'omr_processing': return 'info'
        default: return 'grey'
      }
    },

    getStatusText(status) {
      switch (status) {
        case 'completed': return 'مكتمل ومعتمد'
        case 'reviewed': return 'تمت المراجعة'
        case 'needs_review': return 'يحتاج مراجعة'
        case 'failed': return 'فشل التصحيح'
        case 'pending': return 'قيد الانتظار'
        case 'aligning': return 'جاري المحاذاة'
        case 'omr_processing': return 'جاري قراءة الدوائر'
        default: return status || '-'
      }
    },

    async fetchStats() {
      try {
        const res = await submissionsAPI.getStats()
        if (res && res.data) {
          this.statsData = res.data
        }
      } catch (err) {
        console.error('Failed to load submissions stats:', err)
      }
    },

    async loadSubjects() {
      try {
        const officeIds = this.normalizeIds(this.selectedOfficeId)
        const dirIds = this.normalizeIds(this.selectedDirectorateId)
        const schoolIds = this.normalizeIds(this.selectedSchoolId)

        const params = {}
        if (this.institutionType && this.institutionType !== 'all') {
          params.institution_type = this.institutionType
        }
        if (officeIds.length > 0) params.office_id = officeIds.join(',')
        if (dirIds.length > 0) params.directorate_id = dirIds.join(',')
        if (schoolIds.length > 0) params.school_id = schoolIds.join(',')

        const res = await gradebookAPI.getSubjects(params)
        this.subjectsList = res.data?.results || []
      } catch (err) {
        console.error('Failed to load subjects:', err)
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
        const officeIds = this.normalizeIds(this.selectedOfficeId)
        const dirIds = this.normalizeIds(this.selectedDirectorateId)
        const schoolIds = this.normalizeIds(this.selectedSchoolId)

        const baseParams = {
          institution_type: this.institutionType !== 'all' ? this.institutionType : undefined,
          subject: this.selectedSubjectId || undefined,
        }
        const officeParams = { ...baseParams }
        if (officeIds.length > 0) officeParams.office_id = officeIds.join(',')

        const dirParams = { ...officeParams }

        const schoolParams = { ...dirParams }
        if (dirIds.length > 0) schoolParams.directorate_id = dirIds.join(',')
        if (schoolIds.length > 0) schoolParams.school_id = schoolIds.join(',')

        const [allOfficesRes, officesRes, directoratesRes, schoolsRes, examsRes] = await Promise.all([
          (!this.allOfficesList || !this.allOfficesList.length)
            ? gradebookAPI.getByOffice(baseParams).catch(() => ({ data: { results: [] } }))
            : Promise.resolve({ data: { results: this.allOfficesList } }),
          gradebookAPI.getByOffice(officeParams).catch(() => ({ data: { results: [] } })),
          gradebookAPI.getByDirectorate(dirParams).catch(() => ({ data: { results: [] } })),
          gradebookAPI.getBySchool(schoolParams).catch(() => ({ data: { results: [] } })),
          gradebookAPI.list(schoolParams).catch(() => ({ data: { results: [] } }))
        ])
        if (!this.allOfficesList || !this.allOfficesList.length) {
          this.allOfficesList = allOfficesRes.data?.results || []
        }
        this.officesList = officesRes.data?.results || []
        this.directoratesList = directoratesRes.data?.results || []
        this.schoolsList = schoolsRes.data?.results || []
        this.examsList = examsRes.data?.results || []

        await Promise.all([
          this.getOfficeMasterData(),
          this.getDirectorateMasterData(),
          this.getSchoolMasterData(),
          this.getExamMasterData(),
        ])
      } catch (err) {
        console.error('Error refreshing master data:', err)
      } finally {
        this.loadingMaster = false
      }
    },

    async resetHierarchyFilters() {
      this.institutionType = 'school'
      this.selectedOfficeId = []
      this.selectedDirectorateId = []
      this.selectedSchoolId = []
      this.selectedSubjectId = null
      this.selectedSubjectName = ''
      this.masterSearchQuery = ''
      await this.loadSubjects()
      await this.refreshMasterData()
      await this.fetchStats()
    },

    async onSectorChange(val) {
      this.institutionType = val
      this.selectedOfficeId = []
      this.selectedDirectorateId = []
      this.selectedSchoolId = []
      this.selectedSubjectId = null
      this.selectedSubjectName = ''
      if (val === 'school') {
        this.masterTab = 'offices'
      } else {
        this.masterTab = 'schools'
      }
      await this.loadSubjects()
      this.refreshMasterData()
    },

    onOfficeFilterChange(val) {
      this.selectedOfficeId = val || []
      const officeIds = this.normalizeIds(this.selectedOfficeId)
      if (officeIds.length > 0) {
        const validDirIds = (this.directoratesList || []).filter(d => officeIds.includes(Number(d.office_id))).map(d => d.id)
        this.selectedDirectorateId = (this.selectedDirectorateId || []).filter(id => validDirIds.includes(id))
      } else {
        this.selectedDirectorateId = []
      }
      this.selectedSchoolId = []
      this.loadSubjects()
      this.refreshMasterData()
    },

    onDirectorateFilterChange(val) {
      this.selectedDirectorateId = val || []
      this.selectedSchoolId = []
      // ربط عكسي ذكي: لو تم اختيار مديريات ولم يكن محدد مكاتب مسبقاً، تضاف مكاتبها تلقائياً
      const dirIds = this.normalizeIds(this.selectedDirectorateId)
      const currentOfficeIds = this.normalizeIds(this.selectedOfficeId)
      if (dirIds.length > 0 && currentOfficeIds.length === 0) {
        const relatedOffices = (this.directoratesList || [])
          .filter(d => dirIds.includes(Number(d.id)) && d.office_id)
          .map(d => Number(d.office_id))
        if (relatedOffices.length > 0) {
          this.selectedOfficeId = Array.from(new Set(relatedOffices))
        }
      }
      this.loadSubjects()
      this.refreshMasterData()
    },

    onSchoolFilterChange(val) {
      this.selectedSchoolId = val || []
      this.loadSubjects()
      this.refreshMasterData()
    },

    onSubjectFilterChange(subjId) {
      this.selectedSubjectId = subjId
      const s = (this.subjectsList || []).find(item => item.id === subjId)
      this.selectedSubjectName = s ? s.name : ''
      this.refreshMasterData()
    },

    drillDownToOffice(item) {
      if (!item || !item.id) return
      this.selectedOfficeId = [item.id]
      this.masterTab = 'directorates'
      this.refreshMasterData()
    },

    drillDownToDirectorate(item) {
      if (!item || !item.id) return
      this.selectedDirectorateId = [item.id]
      if (item.office_id) {
        this.selectedOfficeId = [item.office_id]
      }
      this.masterTab = 'schools'
      this.refreshMasterData()
    },

    // Master Tables Data Providers
    async getOfficeMasterData(params = {}) {
      const p = params?.params || params || {}
      const page = p.page || 1
      const pageSize = p.page_size || 20
      const all = this.filteredOfficesTable || []
      const start = (page - 1) * pageSize
      this.officeMasterTableItems = {
        results: all.slice(start, start + pageSize),
        count: all.length,
        pagination: {
          count: all.length,
          total: all.length,
          num_pages: Math.ceil(all.length / pageSize) || 1,
          current_page: page,
        },
      }
      return this.officeMasterTableItems
    },

    async getDirectorateMasterData(params = {}) {
      const p = params?.params || params || {}
      const page = p.page || 1
      const pageSize = p.page_size || 20
      const all = this.filteredDirectoratesTable || []
      const start = (page - 1) * pageSize
      this.directorateMasterTableItems = {
        results: all.slice(start, start + pageSize),
        count: all.length,
        pagination: {
          count: all.length,
          total: all.length,
          num_pages: Math.ceil(all.length / pageSize) || 1,
          current_page: page,
        },
      }
      return this.directorateMasterTableItems
    },

    async getSchoolMasterData(params = {}) {
      const p = params?.params || params || {}
      const page = p.page || 1
      const pageSize = p.page_size || 20
      const all = this.filteredSchoolsTable || []
      const start = (page - 1) * pageSize
      this.schoolMasterTableItems = {
        results: all.slice(start, start + pageSize),
        count: all.length,
        pagination: {
          count: all.length,
          total: all.length,
          num_pages: Math.ceil(all.length / pageSize) || 1,
          current_page: page,
        },
      }
      return this.schoolMasterTableItems
    },

    async getExamMasterData(params = {}) {
      const p = params?.params || params || {}
      const page = p.page || 1
      const pageSize = p.page_size || 20
      const all = this.filteredExamsTable || []
      const start = (page - 1) * pageSize
      this.examMasterTableItems = {
        results: all.slice(start, start + pageSize),
        count: all.length,
        pagination: {
          count: all.length,
          total: all.length,
          num_pages: Math.ceil(all.length / pageSize) || 1,
          current_page: page,
        },
      }
      return this.examMasterTableItems
    },

    openSchoolExamsDialog(schoolItem) {
      this.selectedSchoolDialogItem = schoolItem
      this.schoolExamsDialog = true
      this.getSchoolExamsData()
    },

    getSchoolExamsData(params = {}) {
      const p = params?.params || params || {}
      const page = p.page || 1
      const pageSize = p.page_size || 10
      const all = this.selectedSchoolDialogItem?.exams || []
      const start = (page - 1) * pageSize
      this.schoolExamsTableItems = {
        results: all.slice(start, start + pageSize),
        count: all.length,
        pagination: {
          count: all.length,
          total: all.length,
          num_pages: Math.ceil(all.length / pageSize) || 1,
          current_page: page,
        },
      }
      return this.schoolExamsTableItems
    },

    // Navigation between Master and Detail
    async openOfficeSubmissions(item) {
      if (!item || !item.id) return
      this.selectedOfficeId = item.id
      this.selectedDirectorateId = null
      this.selectedSchoolId = null
      this.selectedSubmissionIds = []

      const offExams = (this.examsList || []).filter(e => e.governorate_id === item.id || e.office_id === item.id)
      if (offExams.length > 0) {
        this.selectedExamId = offExams[0].id
        this.selectedExamObj = offExams[0]
      } else {
        this.selectedExamId = null
        this.selectedExamObj = null
      }
      this.currentView = 'detail'
      await this.fetchSubmissionsRoster({ params: { page: 1, page_size: 15, office_id: item.id } })
    },

    async openDirectorateSubmissions(item) {
      if (!item || !item.id) return
      this.selectedDirectorateId = item.id
      this.selectedSchoolId = null
      if (item.office_id) this.selectedOfficeId = item.office_id
      this.selectedSubmissionIds = []

      const dirExams = (this.examsList || []).filter(e => e.directorate_id === item.id)
      if (dirExams.length > 0) {
        this.selectedExamId = dirExams[0].id
        this.selectedExamObj = dirExams[0]
      } else {
        this.selectedExamId = null
        this.selectedExamObj = null
      }
      this.currentView = 'detail'
      await this.fetchSubmissionsRoster({ params: { page: 1, page_size: 15, directorate_id: item.id } })
    },

    async openSchoolSubmissions(item) {
      if (!item) return
      this.selectedSchoolId = item.id
      this.selectedDirectorateId = null
      this.selectedOfficeId = null
      this.filterOrganization = item.name
      this.selectedSubmissionIds = []

      if (item.exams && item.exams.length > 0) {
        this.selectedExamId = item.exams[0].id || item.exams[0].code
        this.selectedExamObj = item.exams[0]
      } else {
        this.selectedExamId = null
        this.selectedExamObj = null
      }
      this.currentView = 'detail'
      await this.fetchSubmissionsRoster({ params: { page: 1, page_size: 15, school_id: item.id, school: item.name } })
    },

    async openExamSubmissions(item) {
      if (!item || !item.id) return
      this.selectedExamId = item.id
      this.selectedExamObj = item
      this.selectedSubmissionIds = []
      this.currentView = 'detail'
      await this.fetchSubmissionsRoster({ params: { page: 1, page_size: 15 } })
    },

    returnToMaster() {
      this.currentView = 'master'
      this.selectedOfficeId = []
      this.selectedDirectorateId = []
      this.selectedSchoolId = []
      this.filterOrganization = null
      this.searchQuery = ''
      this.filterStatus = null
      this.filterVersion = 'all'
      this.selectedSubmissionIds = []
      this.refreshMasterData()
      this.fetchStats()
    },

    async onExamChange(examId) {
      if (!examId) {
        this.selectedExamObj = null
        this.tableItems = { results: [], pagination: { count: 0, num_pages: 1, current_page: 1, page_size: 15, total: 0 } }
        return
      }
      this.selectedExamId = examId
      this.selectedExamObj = (this.examsList || []).find(e => e.id === examId) || null
      this.selectedSubmissionIds = []
      await this.fetchSubmissionsRoster({ params: { page: 1, page_size: 15 } })
    },

    // Detail View Filters and Roster Fetch
    buildFilterParams(extra = {}) {
      const q = { ...extra }
      if (this.selectedExamId) q.exam = this.selectedExamId
      if (this.searchQuery && this.searchQuery.trim()) {
        q.search = this.searchQuery.trim()
      } else if (extra && extra.search) {
        q.search = extra.search
      }
      if (this.filterStatus) q.status = this.filterStatus
      if (this.filterVersion && this.filterVersion !== 'all') {
        q.version_code = this.filterVersion
        q.exam_version = this.filterVersion
      }
      const officeIds = this.normalizeIds(this.selectedOfficeId)
      const dirIds = this.normalizeIds(this.selectedDirectorateId)
      const schoolIds = this.normalizeIds(this.selectedSchoolId)
      if (officeIds.length > 0) q.office_id = officeIds.join(',')
      if (dirIds.length > 0) q.directorate_id = dirIds.join(',')
      if (schoolIds.length > 0) q.school_id = schoolIds.join(',')
      return q
    },

    async fetchSubmissionsRoster(tableParams = null) {
      this.loadingRecords = true
      try {
        let baseParams = { page: 1, page_size: 15 }
        if (tableParams && tableParams.params) {
          baseParams = { ...tableParams.params }
        } else if (tableParams && typeof tableParams === 'object') {
          baseParams = { ...tableParams }
        }
        const queryParams = this.buildFilterParams(baseParams)

        const res = await submissionsAPI.list(queryParams)
        const data = res.data || res || {}
        if (Array.isArray(data)) {
          this.tableItems = {
            results: data,
            count: data.length,
            pagination: {
              count: data.length,
              total: data.length,
              num_pages: Math.ceil(data.length / (queryParams.page_size || 15)) || 1,
              current_page: queryParams.page || 1,
              page_size: queryParams.page_size || 15,
            }
          }
        } else if (data && data.results) {
          const results = data.results || []
          const total = data.pagination?.total || data.count || results.length
          const pageSize = queryParams.page_size || data.pagination?.page_size || 15
          this.tableItems = {
            ...data,
            results,
            count: total,
            pagination: {
              count: total,
              total,
              num_pages: Math.ceil(total / pageSize) || 1,
              current_page: queryParams.page || 1,
              page_size: pageSize,
            }
          }
        }
        return this.tableItems
      } catch (err) {
        console.error('Failed to fetch submissions roster:', err)
        return { results: [], pagination: {} }
      } finally {
        this.loadingRecords = false
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

    onQuickStatusFilterChange(val) {
      this.filterStatus = val
      if (this.currentView === 'master') {
        this.currentView = 'detail'
      }
      this.fetchSubmissionsRoster({ params: { page: 1 } })
    },

    onStatusFilterChange(val) {
      this.filterStatus = val
      if (this.currentView === 'master' && val) {
        this.currentView = 'detail'
      }
      this.fetchSubmissionsRoster({ params: { page: 1 } })
    },

    onKpiCardClick(statusKey) {
      if (this.activeKpiFilter === statusKey && this.currentView === 'detail') {
        this.activeKpiFilter = null
        this.filterStatus = null
      } else {
        this.activeKpiFilter = statusKey
        this.filterStatus = statusKey
      }
      if (this.currentView === 'master') {
        this.currentView = 'detail'
      }
      this.fetchSubmissionsRoster({ params: { page: 1 } })
    },

    applyFilters() {
      this.activeKpiFilter = this.filterStatus
      this.fetchSubmissionsRoster({ params: { page: 1 } })
    },

    resetDetailFilters() {
      this.searchQuery = ''
      this.filterVersion = 'all'
      this.filterStatus = null
      this.activeKpiFilter = null
      this.applyFilters()
    },

    toggleSubmissionSelection(id) {
      if (!id) return
      const idx = this.selectedSubmissionIds.indexOf(id)
      if (idx > -1) {
        this.selectedSubmissionIds.splice(idx, 1)
      } else {
        this.selectedSubmissionIds.push(id)
      }
    },

    toggleSelectAllCurrent(val) {
      const currentIds = (this.tableItems.results || []).map(s => s.id).filter(Boolean)
      if (val) {
        const set = new Set([...this.selectedSubmissionIds, ...currentIds])
        this.selectedSubmissionIds = Array.from(set)
      } else {
        this.selectedSubmissionIds = this.selectedSubmissionIds.filter(id => !currentIds.includes(id))
      }
    },

    // Sheet Actions
    navigateToDetail(item) {
      if (!item || !item.id) return
      this.$router.push(`/omr-submissions/${item.id}`)
    },

    previewSheetImage(item) {
      this.previewSubmission = item
      this.imagePreviewDialog = true
    },

    async reprocessSingleSheet(item) {
      if (!item || !item.id) return
      this.reprocessingId = item.id
      try {
        const res = await submissionsAPI.reprocess(item.id)
        if (res && res.data && res.data.success) {
          this.notify('تمت إعادة المعالجة والتصحيح الضوئي بنجاح', 'success')
          await this.fetchSubmissionsRoster()
        } else {
          this.notify(res?.data?.message || 'تم تحديث نتائج المعالجة الضوئية', 'info')
          await this.fetchSubmissionsRoster()
        }
      } catch (err) {
        console.error('Error reprocessing sheet:', err)
        this.notify('حدث خطأ أثناء إعادة المعالجة الضوئية', 'error')
      } finally {
        this.reprocessingId = null
      }
    },

    confirmDeleteSubmission(item) {
      this.submissionToDelete = item
      this.deleteDialog = true
    },

    async executeDelete() {
      if (!this.submissionToDelete || !this.submissionToDelete.id) return
      try {
        await submissionsAPI.delete(this.submissionToDelete.id)
        this.notify('تم حذف ورقة الإجابة بنجاح', 'success')
        this.deleteDialog = false
        this.submissionToDelete = null
        await this.fetchSubmissionsRoster()
        await this.fetchStats()
      } catch (err) {
        console.error('Error deleting submission:', err)
        this.notify('تعذر حذف ورقة الإجابة', 'error')
      }
    },
  },
}
</script>

<style scoped>
.qb-submissions-view-v4 {
  direction: rtl;
}

.main-card {
  transition: all 0.2s ease-in-out;
}

.sheet-thumb-wrapper {
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.sheet-thumb-wrapper:hover {
  transform: scale(1.08);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.kpi-filter-card {
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.kpi-filter-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08) !important;
}

.kpi-card-active {
  border-width: 2px !important;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12) !important;
}
</style>
