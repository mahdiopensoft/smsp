<template>
  <div class="qb-omr-print-registry pa-4 pa-md-6">

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 1. MASTER VIEW: الهيكل الإداري وسجل الطباعة المركزي             -->
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
              @click="loadMasterData"
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
                :items="officesList"
                item-title="office_name"
                item-value="id"
                label="مكتب التربية (المحافظة)"
                placeholder="اختر مكتب التربية بالمحافظة..."
                clearable
                density="compact"
                variant="outlined"
                rounded="lg"
                hide-details
                prepend-inner-icon="mdi-office-building-outline"
                @update:model-value="onOfficeFilterChange"
              />
            </v-col>

            <v-col cols="12" sm="6" md="2">
              <v-autocomplete
                v-model="selectedDirectorateId"
                :items="directoratesOptions"
                item-title="name"
                item-value="id"
                label="إدارة التربية (المديرية)"
                placeholder="اختر إدارة التربية بالمديرية..."
                clearable
                density="compact"
                variant="outlined"
                rounded="lg"
                hide-details
                prepend-inner-icon="mdi-map-marker-radius-outline"
                @update:model-value="onDirectorateFilterChange"
              />
            </v-col>

            <v-col cols="12" sm="6" md="3">
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
                rounded="lg"
                hide-details
                prepend-inner-icon="mdi-school-outline"
                @update:model-value="onSchoolFilterChange"
              />
            </v-col>

            <v-col cols="12" sm="6" md="3">
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
                placeholder="اختر الجامعة أو الكلية..."
                clearable
                density="compact"
                variant="outlined"
                rounded="lg"
                hide-details
                prepend-inner-icon="mdi-domain"
                @update:model-value="onSchoolFilterChange"
              />
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
                placeholder="اختر المعهد..."
                clearable
                density="compact"
                variant="outlined"
                rounded="lg"
                hide-details
                prepend-inner-icon="mdi-tools"
                @update:model-value="onSchoolFilterChange"
              />
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
              class="rounded-lg"
            />
          </div>
        </div>

        <v-window v-model="masterTab">
          <!-- 1. تبويب مكاتب التربية بالمحافظات -->
          <v-window-item value="offices" v-if="institutionType === 'school'">
            <custom-data-table
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

                <template v-else-if="key === 'printed_count'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-primary">{{ item.printed_count || 0 }} ورقة</span>
                  </div>
                </template>

                <template v-else-if="key === 'printed_rate'">
                  <div class="d-flex align-center justify-center gap-2 px-1">
                    <v-progress-linear
                      :model-value="item.printed_rate || 0"
                      :color="(item.printed_rate >= 100) ? 'success' : (item.printed_rate > 0 ? 'warning' : 'primary')"
                      height="8"
                      rounded
                      style="min-width: 60px; max-width: 80px;"
                    />
                    <span class="text-caption font-weight-bold">{{ item.printed_rate || 0 }}%</span>
                  </div>
                </template>

                <template v-else-if="key === 'print_status'">
                  <div class="d-flex justify-center align-center">
                    <v-chip size="x-small" :color="(item.printed_rate >= 100 || item.print_status === 'full') ? 'success' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'warning' : 'grey')" variant="tonal" class="font-weight-bold">
                      {{ (item.printed_rate >= 100 || item.print_status === 'full') ? 'مكتمل الطباعة' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'طباعة جزئية' : 'لم يطبع بعد') }}
                    </v-chip>
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
                      prepend-icon="mdi-printer-outline"
                      @click="openOfficeStudio(item)"
                    >
                      استوديو الطباعة
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </v-window-item>

          <!-- 2. تبويب إدارات التربية بالمديريات -->
          <v-window-item value="directorates" v-if="institutionType === 'school'">
            <custom-data-table
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

                <template v-else-if="key === 'printed_count'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-teal">{{ item.printed_count || 0 }} ورقة</span>
                  </div>
                </template>

                <template v-else-if="key === 'printed_rate'">
                  <div class="d-flex align-center justify-center gap-2 px-1">
                    <v-progress-linear
                      :model-value="item.printed_rate || 0"
                      :color="(item.printed_rate >= 100) ? 'success' : (item.printed_rate > 0 ? 'warning' : 'teal')"
                      height="8"
                      rounded
                      style="min-width: 60px; max-width: 80px;"
                    />
                    <span class="text-caption font-weight-bold">{{ item.printed_rate || 0 }}%</span>
                  </div>
                </template>

                <template v-else-if="key === 'print_status'">
                  <div class="d-flex justify-center align-center">
                    <v-chip size="x-small" :color="(item.printed_rate >= 100 || item.print_status === 'full') ? 'success' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'warning' : 'grey')" variant="tonal" class="font-weight-bold">
                      {{ (item.printed_rate >= 100 || item.print_status === 'full') ? 'مكتمل الطباعة' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'طباعة جزئية' : 'لم يطبع بعد') }}
                    </v-chip>
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
                      prepend-icon="mdi-printer-outline"
                      @click="openDirectorateStudio(item)"
                    >
                      استوديو الطباعة
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </v-window-item>

          <!-- 3. تبويب المراكز الامتحانية والمدارس / الجامعات / المعاهد -->
          <v-window-item value="schools">
            <custom-data-table
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

                <template v-else-if="key === 'name'">
                  <div class="d-flex align-center py-2" style="min-width: 280px;">
                    <v-avatar color="indigo" variant="tonal" size="36" class="me-3 rounded-lg flex-shrink-0">
                      <v-icon color="indigo" size="20">mdi-school-outline</v-icon>
                    </v-avatar>
                    <div>
                      <div class="font-weight-bold text-subtitle-2 text-on-surface text-wrap">{{ item.name }}</div>
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
                    <span class="font-weight-bold text-subtitle-2">{{ item.total_students }} طالب</span>
                  </div>
                </template>

                <template v-else-if="key === 'printed_count'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-indigo">{{ item.printed_count || 0 }} ورقة</span>
                  </div>
                </template>

                <template v-else-if="key === 'printed_rate'">
                  <div class="d-flex align-center justify-center gap-2 px-1">
                    <v-progress-linear
                      :model-value="item.printed_rate || 0"
                      :color="(item.printed_rate >= 100) ? 'success' : (item.printed_rate > 0 ? 'warning' : 'indigo')"
                      height="8"
                      rounded
                      style="min-width: 60px; max-width: 80px;"
                    />
                    <span class="text-caption font-weight-bold">{{ item.printed_rate || 0 }}%</span>
                  </div>
                </template>

                <template v-else-if="key === 'print_status'">
                  <div class="d-flex justify-center align-center">
                    <v-chip size="x-small" :color="(item.printed_rate >= 100 || item.print_status === 'full') ? 'success' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'warning' : 'grey')" variant="tonal" class="font-weight-bold">
                      {{ (item.printed_rate >= 100 || item.print_status === 'full') ? 'مكتمل الطباعة' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'طباعة جزئية' : 'لم يطبع بعد') }}
                    </v-chip>
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
                      color="primary"
                      variant="flat"
                      rounded="lg"
                      class="font-weight-bold"
                      prepend-icon="mdi-printer-check"
                      @click="openSchoolStudio(item)"
                    >
                      سحب وطباعة
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </v-window-item>

          <!-- 4. تبويب الاختبارات الأكاديمية -->
          <v-window-item value="exams">
            <custom-data-table
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

                <template v-else-if="key === 'title'">
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

                <template v-else-if="key === 'total_registered'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-subtitle-2">{{ item.total_registered || item.total_students || 0 }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'printed_count'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-weight-bold text-primary">{{ item.printed_count || 0 }} ورقة</span>
                  </div>
                </template>

                <template v-else-if="key === 'printed_rate'">
                  <div class="d-flex align-center justify-center gap-2 px-1">
                    <v-progress-linear
                      :model-value="item.printed_rate || 0"
                      :color="(item.printed_rate >= 100) ? 'success' : (item.printed_rate > 0 ? 'warning' : 'primary')"
                      height="8"
                      rounded
                      style="min-width: 60px; max-width: 80px;"
                    />
                    <span class="text-caption font-weight-bold">{{ item.printed_rate || 0 }}%</span>
                  </div>
                </template>

                <template v-else-if="key === 'print_status'">
                  <div class="d-flex justify-center align-center">
                    <v-chip size="x-small" :color="(item.printed_rate >= 100 || item.print_status === 'full') ? 'success' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'warning' : 'grey')" variant="tonal" class="font-weight-bold">
                      {{ (item.printed_rate >= 100 || item.print_status === 'full') ? 'مكتمل الطباعة' : ((item.printed_count > 0 || item.print_status === 'partial') ? 'طباعة جزئية' : 'لم يطبع بعد') }}
                    </v-chip>
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
                      prepend-icon="mdi-printer-eye"
                      @click="openExamStudio(item)"
                    >
                      استوديو الطباعة
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </v-window-item>

          <!-- 5. تبويب سجل الدفعات المطبوعة العام -->
          <v-window-item value="registry">
            <custom-data-table
              v-model="selectedBatchMasterRows"
              item-value="batch_id"
              :items="batchMasterTableItems"
              :getData="getBatchMasterData"
              :headers="registryMasterHeaders"
              :customLoading="loadingBatches"
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

                <template v-else-if="key === 'batch_id'">
                  <div class="d-flex justify-center align-center">
                    <span class="font-mono font-weight-bold text-caption text-primary">
                      {{ item.batch_id }}
                    </span>
                  </div>
                </template>

                <template v-else-if="key === 'exam_title'">
                  <span class="text-body-2 font-weight-medium text-wrap">{{ item.exam_title }}</span>
                </template>

                <template v-else-if="key === 'total_sheets'">
                  <div class="d-flex justify-center align-center">
                    <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                      {{ item.total_sheets }} ورقة
                    </v-chip>
                  </div>
                </template>

                <template v-else-if="key === 'printed_at'">
                  <div class="d-flex justify-center align-center">
                    <span class="text-caption text-medium-emphasis">{{ item.printed_at || '-' }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'printed_by_name'">
                  <div class="d-flex justify-center align-center">
                    <span class="text-body-2">{{ item.printed_by_name || '-' }}</span>
                  </div>
                </template>

                <template v-else-if="key === 'actions'">
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
              </template>
            </custom-data-table>
          </v-window-item>
        </v-window>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 2. DETAIL VIEW: استوديو المعاينة وطباعة الوثائق وحزم الاختبار  -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <div v-else class="detail-studio-container">
      <!-- شريط الفلاتر الهيكلية واختيار الاختبار المعتمد (مرتب وهرمي) -->
      <div class="main-card pa-4 rounded-2xl mb-4 bg-surface border elevation-1">
        <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3 pb-2 border-b">
          <div class="d-flex align-center gap-3 flex-wrap">
            <v-icon color="primary" size="20">mdi-filter-variant</v-icon>
            <span class="text-subtitle-2 font-weight-black text-on-surface">فلاتر الهيكل واختيار الاختبار:</span>

            <v-chip
              v-if="selectedSchoolName"
              size="small"
              color="info"
              variant="tonal"
              closable
              class="font-weight-bold ms-1"
              prepend-icon="mdi-filter-check"
              @click:close="clearSchoolFilter"
            >
              {{ selectedSchoolName }} ({{ examDetails?.registered_students?.length || 0 }} طالب)
            </v-chip>
          </div>

          <div class="d-flex align-center gap-2">
            <v-btn
              color="primary"
              variant="tonal"
              size="small"
              rounded="lg"
              class="font-weight-bold"
              prepend-icon="mdi-arrow-right"
              @click="returnToMaster"
            >
              العودة للهيكل الإداري
            </v-btn>
            <v-btn
              v-if="selectedExam"
              variant="text"
              color="primary"
              size="small"
              class="font-weight-bold"
              :prepend-icon="showHierarchyFilters ? 'mdi-chevron-up' : 'mdi-tune'"
              @click="showHierarchyFilters = !showHierarchyFilters"
            >
              {{ showHierarchyFilters ? 'إخفاء محدد الاختبار' : 'تغيير الاختبار أو المدرسة' }}
            </v-btn>
            <v-btn
              variant="tonal"
              color="error"
              size="small"
              rounded="lg"
              class="font-weight-bold"
              prepend-icon="mdi-filter-remove-outline"
              @click="resetHierarchyStudioFilters"
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
              :loading="loadingExams"
              @click="fetchExamsList"
            >
              تحديث
            </v-btn>
          </div>
        </div>

        <v-expand-transition>
          <div v-show="!selectedExam || showHierarchyFilters">
            <v-row dense class="align-center">
              <!-- نوع المؤسسة التعليمية كفلتر منسدل أساسي -->
              <v-col cols="12" sm="6" :md="institutionType === 'school' ? 4 : 3" :lg="institutionType === 'school' ? 2 : 3">
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

              <!-- التعليم العام (المدرسي): محافظة -> مديرية -> مدرسة/مركز -->
              <template v-if="institutionType === 'school'">
                <v-col cols="12" sm="6" md="4" lg="2">
                  <v-autocomplete
                    v-model="selectedOfficeId"
                    :items="officesList"
                    item-title="office_name"
                    item-value="id"
                    label="مكتب التربية (المحافظة)"
                    placeholder="كل المحافظات..."
                    clearable
                    density="compact"
                    variant="outlined"
                    rounded="lg"
                    hide-details
                    prepend-inner-icon="mdi-office-building-outline"
                    @update:model-value="onStudioOfficeChange"
                  />
                </v-col>

                <v-col cols="12" sm="6" md="4" lg="2">
                  <v-autocomplete
                    v-model="selectedDirectorateId"
                    :items="directoratesOptions"
                    item-title="name"
                    item-value="id"
                    label="إدارة التربية (المديرية)"
                    placeholder="كل المديريات..."
                    clearable
                    density="compact"
                    variant="outlined"
                    rounded="lg"
                    hide-details
                    prepend-inner-icon="mdi-map-marker-radius-outline"
                    @update:model-value="onStudioDirectorateChange"
                  />
                </v-col>

                <v-col cols="12" sm="6" md="6" lg="3">
                  <v-autocomplete
                    v-model="selectedSchoolId"
                    :items="schoolsOptions"
                    item-title="name"
                    item-value="id"
                    label="المدرسة / المركز الامتحاني"
                    placeholder="كل المراكز والمدارس..."
                    clearable
                    density="compact"
                    variant="outlined"
                    rounded="lg"
                    hide-details
                    prepend-inner-icon="mdi-school-outline"
                    @update:model-value="onStudioSchoolChange"
                  />
                </v-col>
              </template>

              <!-- التعليم الجامعي: جامعة/كلية -->
              <template v-else-if="institutionType === 'university'">
                <v-col cols="12" sm="6" md="4" lg="4">
                  <v-autocomplete
                    v-model="selectedSchoolId"
                    :items="schoolsOptions"
                    item-title="name"
                    item-value="id"
                    label="الجامعة / الكلية"
                    placeholder="اختر الكلية أو الجامعة..."
                    clearable
                    density="compact"
                    variant="outlined"
                    rounded="lg"
                    hide-details
                    prepend-inner-icon="mdi-domain"
                    @update:model-value="onStudioSchoolChange"
                  />
                </v-col>
              </template>

              <!-- التعليم الفني (معاهد): معهد/مركز -->
              <template v-else-if="institutionType === 'institute'">
                <v-col cols="12" sm="6" md="4" lg="4">
                  <v-autocomplete
                    v-model="selectedSchoolId"
                    :items="schoolsOptions"
                    item-title="name"
                    item-value="id"
                    label="المعهد / المركز الفني"
                    placeholder="اختر المعهد أو المركز..."
                    clearable
                    density="compact"
                    variant="outlined"
                    rounded="lg"
                    hide-details
                    prepend-inner-icon="mdi-tools"
                    @update:model-value="onStudioSchoolChange"
                  />
                </v-col>
              </template>

              <!-- منسدلة اختيار الاختبار المعتمد المطلوب طباعة وثائقه -->
              <v-col cols="12" :sm="institutionType === 'school' ? 6 : 12" :md="institutionType === 'school' ? 6 : 5" :lg="institutionType === 'school' ? 3 : 5">
                <v-autocomplete
                  v-model="selectedExamId"
                  :items="examsList"
                  item-title="title"
                  item-value="id"
                  label="الاختبار المعتمد المطلوب طباعته"
                  placeholder="ابحث بالاختبار أو المادة أو الرمز..."
                  prepend-inner-icon="mdi-file-document-check-outline"
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
                      :subtitle="`المادة: ${item.raw.subject_name || 'عام'} | النماذج: ${item.raw.versions_count || 1} | الطلاب: ${item.raw.registered_students_count || 0}`"
                    />
                  </template>
                </v-autocomplete>
              </v-col>
            </v-row>
          </div>
        </v-expand-transition>
      </div>

    <!-- ── بطاقة معلومات الاختبار المحدد (تصميم مؤسسي متوازن وأنيق) ── -->
    <div v-if="selectedExam" class="main-card mb-4 pa-4 bg-surface border rounded-2xl elevation-2">
      <!-- السطر الأول: العنوان والهوية والاعتماد -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-3 border-b">
        <div class="d-flex align-center gap-3">
          <v-avatar color="primary" variant="tonal" size="44" class="rounded-xl flex-shrink-0">
            <v-icon size="24" color="primary">mdi-file-document-check-outline</v-icon>
          </v-avatar>
          <div>
            <div class="d-flex align-center gap-2 flex-wrap">
              <h2 class="text-subtitle-1 font-weight-black text-on-surface mb-0">
                {{ selectedExam.title }}
              </h2>
              <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold">
                معتمد للطباعة
              </v-chip>
            </div>
            <div class="d-flex align-center gap-2 text-caption text-medium-emphasis flex-wrap mt-1">
              <span class="font-mono font-weight-bold text-primary">{{ selectedExam.uniqueCode }}</span>
              <span>•</span>
              <span v-if="selectedExam.subject_name">المادة: <strong class="text-on-surface font-weight-bold">{{ selectedExam.subject_name }}</strong></span>
              <span>•</span>
              <span>العام الدراسي: <strong class="text-on-surface font-weight-bold">{{ selectedExam.year_name || '2025-2026' }}</strong></span>
              <template v-if="selectedSchoolName">
                <span>•</span>
                <span>المركز: <strong class="text-teal font-weight-bold">{{ selectedSchoolName }}</strong></span>
              </template>
            </div>
          </div>
        </div>

        <div class="d-flex align-center gap-2 flex-wrap">
          <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold" prepend-icon="mdi-layers-outline">
            {{ selectedExam.versions_count || examDetails?.versions?.length || 4 }} نماذج (A, B, C, D)
          </v-chip>
          <v-chip size="small" color="success" variant="tonal" class="font-weight-black" prepend-icon="mdi-account-group-outline">
            {{ examDetails?.registered_students?.length || selectedExam.registered_students_count || 0 }} طالب
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
    </div>

    <!-- ── Navigation Tabs (خفيف وسهل) ───────────────────────────── -->
    <div class="registry-nav-bar mb-6">
      <div class="registry-nav-container">
        <div
          class="registry-nav-item"
          :class="{ 'is-active': activeTab === 'sheets' }"
          @click="switchDetailTab('sheets')"
          role="button"
          tabindex="0"
        >
          <v-icon size="17" class="nav-icon">mdi-table-account</v-icon>
          <span>الجدول الموحد لأوراق التظليل</span>
        </div>

        <div
          class="registry-nav-item"
          :class="{ 'is-active': activeTab === 'questions' }"
          @click="switchDetailTab('questions')"
          role="button"
          tabindex="0"
        >
          <v-icon size="17" class="nav-icon">mdi-file-document-outline</v-icon>
          <span>ورقة الأسئلة الرسمية (الكراسة)</span>
        </div>

        <div
          class="registry-nav-item"
          :class="{ 'is-active': activeTab === 'package' }"
          @click="switchDetailTab('package')"
          role="button"
          tabindex="0"
        >
          <v-icon size="17" class="nav-icon">mdi-package-variant-closed</v-icon>
          <span>حزمة الاختبار (أسئلة + تظليل)</span>
        </div>

        <div
          class="registry-nav-item"
          :class="{ 'is-active': activeTab === 'history' }"
          @click="switchDetailTab('history')"
          role="button"
          tabindex="0"
        >
          <v-icon size="17" class="nav-icon">mdi-history</v-icon>
          <span>سجل الدفعات المطبوعة ({{ (batches && batches.length) || 0 }})</span>
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
        <!-- TAB 1: UNIFIED ROSTER TABLE (الجدول الموحد custom-data-table) -->
        <!-- ════════════════════════════════════════════════════════════ -->
        <div v-if="isTabVisited('sheets')" v-show="activeTab === 'sheets'">
          <!-- Controls Toolbar (شريط الفلاتر والبحث السريع وأوامر الطباعة) -->
          <!-- ── شريط العمليات والطباعة والتصفية الموحد (Control Center) ── -->
          <div class="main-card rounded-2xl pa-4 mb-4 border bg-surface elevation-1">
            <!-- السطر الأول: أوامر الطباعة السريعة وخيارات الإنتاج -->
            <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-3 border-b">
              <!-- أزرار الطباعة والإنتاج -->
              <div class="d-flex align-center gap-2 flex-wrap">
                <!-- زر الطباعة الرئيسي الفوري -->
                <v-btn
                  color="success"
                  variant="flat"
                  rounded="xl"
                  size="default"
                  class="font-weight-black shadow-sm px-5"
                  prepend-icon="mdi-printer-check"
                  :loading="printingBatch"
                  :disabled="!targetBatchStudents.length"
                  @click="printSelectedOrAllRoster"
                >
                  طباعة أوراق التظليل {{ selectedStudentIds.length > 0 ? `المحددة (${selectedStudentIds.length})` : `للكل (${filteredRosterStudents.length})` }}
                </v-btn>

                <!-- كشف تسليم الكنترول -->
                <v-btn
                  variant="tonal"
                  color="primary"
                  rounded="xl"
                  class="font-weight-bold px-4"
                  prepend-icon="mdi-clipboard-text-outline"
                  title="طباعة كشف تسليم الكنترول الرسمي"
                  @click="printAuditRoster"
                >
                  كشف تسليم الكنترول
                </v-btn>

                <!-- قائمة خيارات الطباعة المتقدمة (تجمع: ورقة فارغة، مقاس A5/A4، تعديل الترويسة) -->
                <v-menu location="bottom end" :close-on-content-click="false">
                  <template #activator="{ props: mProps }">
                    <v-btn
                      v-bind="mProps"
                      variant="tonal"
                      color="secondary"
                      rounded="xl"
                      class="font-weight-bold px-3"
                      prepend-icon="mdi-cog-outline"
                      append-icon="mdi-chevron-down"
                    >
                      خيارات الطباعة وإعدادات الورق
                    </v-btn>
                  </template>

                  <v-card min-width="280" class="rounded-xl border elevation-4 pa-2 bg-surface">
                    <div class="text-caption font-weight-black text-primary px-3 py-2 border-b mb-1 d-flex align-center gap-1">
                      <v-icon size="16">mdi-tune</v-icon>
                      إعدادات الورقة ونماذج الطباعة
                    </div>

                    <!-- تبديل المقاس A5 / A4 -->
                    <div class="px-3 py-2">
                      <div class="text-caption text-medium-emphasis mb-1 font-weight-bold">مقاس الورقة:</div>
                      <v-btn-toggle
                        v-model="selectedSheetLayout"
                        mandatory
                        density="compact"
                        color="primary"
                        variant="outlined"
                        rounded="lg"
                        class="w-100"
                      >
                        <v-btn value="compact_a5" class="font-weight-bold flex-1" size="small" prepend-icon="mdi-card-outline">
                          A5 الوزارية
                        </v-btn>
                        <v-btn value="full_a4" class="font-weight-bold flex-1" size="small" prepend-icon="mdi-file-document-outline">
                          A4 الشاملة
                        </v-btn>
                      </v-btn-toggle>
                    </div>

                    <v-divider class="my-1" />

                    <!-- تعديل الترويسة -->
                    <v-list-item
                      rounded="lg"
                      prepend-icon="mdi-pencil-outline"
                      title="تعديل بيانات الترويسة فورياً"
                      subtitle="اسم المركز، المديرية، والمحافظة"
                      @click="showAdjustmentsPanel = !showAdjustmentsPanel"
                    />

                    <v-divider class="my-1" />

                    <!-- ورقة عامة فارغة -->
                    <div class="px-3 py-1">
                      <div class="text-caption text-medium-emphasis font-weight-bold mb-1">طباعة ورقة عامة فارغة:</div>
                      <div class="d-flex gap-1">
                        <v-btn
                          v-for="ver in ['A', 'B', 'C', 'D']"
                          :key="`blank-opt-${ver}`"
                          size="x-small"
                          variant="tonal"
                          color="primary"
                          class="font-weight-bold flex-1"
                          @click="printBlankSheetVersion(ver)"
                        >
                          نموذج {{ ver }}
                        </v-btn>
                      </div>
                    </div>
                  </v-card>
                </v-menu>
              </div>

              <!-- أدوات التحديد السريع -->
              <div class="d-flex align-center gap-2">
                <v-chip
                  v-if="selectedStudentIds.length > 0"
                  size="small"
                  color="primary"
                  variant="flat"
                  class="font-weight-bold"
                >
                  محدد: {{ selectedStudentIds.length }} طالب
                </v-chip>

                <v-btn
                  v-if="filteredRosterStudents.length > 0"
                  size="small"
                  variant="tonal"
                  color="primary"
                  rounded="lg"
                  class="font-weight-bold"
                  :prepend-icon="selectedStudentIds.length === filteredRosterStudents.length ? 'mdi-checkbox-blank-outline' : 'mdi-checkbox-multiple-marked-outline'"
                  @click="selectAllRosterStudents"
                >
                  {{ selectedStudentIds.length === filteredRosterStudents.length ? 'إلغاء التحديد' : 'تحديد كل المعروضين' }}
                </v-btn>

                <v-btn
                  v-if="selectedStudentIds.length > 0"
                  size="small"
                  variant="tonal"
                  color="success"
                  rounded="lg"
                  class="font-weight-bold"
                  prepend-icon="mdi-check-all"
                  @click="markSelectedAsPrinted"
                >
                  تحديد كمطبوع
                </v-btn>
              </div>
            </div>

            <!-- Live Adjustments Panel -->
            <v-expand-transition>
              <div v-if="showAdjustmentsPanel" class="pa-4 my-3 bg-surface border rounded-xl">
                <div class="text-caption font-weight-black text-primary mb-3 d-flex align-center justify-space-between">
                  <div class="d-flex align-center gap-1">
                    <v-icon size="16">mdi-auto-fix</v-icon>
                    تعديل بيانات الترويسة فورياً (تنعكس التعديلات لحظياً على كافة أوراق الطلاب المطبوعة)
                  </div>
                  <v-btn icon="mdi-close" variant="text" size="x-small" @click="showAdjustmentsPanel = false" />
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
                  <v-col cols="12" sm="3" class="d-flex align-center justify-end">
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

            <!-- السطر الثاني: شريط الفلاتر والبحث الموحد (فلاتر منسدلة أنيقة) -->
            <div class="d-flex align-center justify-space-between flex-wrap gap-2 pt-3">
              <!-- الفلاتر المنسدلة -->
              <div class="d-flex align-center gap-2 flex-wrap">
                <!-- فلتر النموذج كمنسدلة -->
                <div style="min-width: 190px; max-width: 230px;">
                  <v-select
                    v-model="rosterModelFilter"
                    :items="modelFilterSelectOptions"
                    item-title="title"
                    item-value="value"
                    label="النموذج"
                    density="compact"
                    variant="outlined"
                    rounded="lg"
                    hide-details
                    prepend-inner-icon="mdi-layers-outline"
                  />
                </div>

                <!-- فلتر حالة الطباعة كمنسدلة -->
                <div style="min-width: 190px; max-width: 230px;">
                  <v-select
                    v-model="rosterPrintFilter"
                    :items="printStatusFilterOptions"
                    item-title="title"
                    item-value="value"
                    label="حالة الطباعة"
                    density="compact"
                    variant="outlined"
                    rounded="lg"
                    hide-details
                    prepend-inner-icon="mdi-printer-outline"
                  />
                </div>

                <!-- زر تفريغ الفلاتر -->
                <v-btn
                  v-if="rosterModelFilter !== 'all' || rosterPrintFilter !== 'all' || rosterSearch"
                  variant="text"
                  color="error"
                  size="small"
                  class="font-weight-bold"
                  prepend-icon="mdi-filter-off-outline"
                  @click="resetRosterFilters"
                >
                  إلغاء التصفية
                </v-btn>
              </div>

              <!-- حقل البحث السريع بالاسم أو رقم الجلوس أو السري -->
              <div style="min-width: 260px; max-width: 340px;">
                <v-text-field
                  v-model="rosterSearch"
                  density="compact"
                  variant="outlined"
                  rounded="lg"
                  placeholder="بحث بالاسم أو رقم الجلوس أو السري..."
                  prepend-inner-icon="mdi-magnify"
                  hide-details
                  clearable
                />
              </div>
            </div>
          </div>

          <!-- ── الجدول الموحد للطلاب وأوراق التظليل (custom-data-table) ── -->
          <div class="main-card rounded-2xl overflow-hidden mb-6">
            <custom-data-table
              :items="rosterTableItems"
              :getData="getRosterData"
              :headers="rosterHeaders"
              :customLoading="loadingExamDetails"
              :hasFilter="false"
              :log="false"
              :restore="false"
              :numbering="true"
              :showSelect="false"
              :actions="false"
              :search="false"
              class="bg-transparent"
            >
              <template v-slot:item-slot="{ item, key, index }">
                <!-- Numbering -->
                <template v-if="key === 'numbering'">
                  <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
                </template>

                <!-- Select Box -->
                <template v-else-if="key === 'select_box'">
                  <div class="d-flex justify-center">
                    <v-checkbox-btn
                      :model-value="selectedStudentIds.includes(item.id)"
                      color="primary"
                      density="compact"
                      hide-details
                      @update:model-value="toggleStudentSelection(item.id)"
                    />
                  </div>
                </template>

                <!-- Seat Number -->
                <template v-else-if="key === 'seat_number'">
                  <span class="font-mono font-weight-black text-primary px-2 py-1 bg-blue-lighten-5 rounded-lg border">
                    {{ item.seat_number }}
                  </span>
                </template>

                <!-- Secret Number -->
                <template v-else-if="key === 'secret_number'">
                  <span class="font-mono text-medium-emphasis">
                    {{ item.secret_number || '-' }}
                  </span>
                </template>

                <!-- Student Info -->
                <template v-else-if="key === 'student_name'">
                  <div class="d-flex align-center gap-2 py-1">
                    <v-avatar size="32" color="primary" variant="tonal" class="text-caption font-weight-black">
                      {{ (item.student_name || 'ط').slice(0, 1) }}
                    </v-avatar>
                    <div>
                      <div class="font-weight-bold text-body-2 text-on-surface">
                        {{ item.student_name || 'طالب بدون اسم' }}
                      </div>
                    </div>
                  </div>
                </template>

                <!-- School / Center -->
                <template v-else-if="key === 'school_name'">
                  <div class="py-1">
                    <div class="font-weight-medium text-body-2">{{ item.school_name || selectedExam?.directorate || 'المركز الرئيسي' }}</div>
                    <div class="text-caption text-medium-emphasis">{{ item.directorate || selectedExam?.directorate || '-' }}</div>
                  </div>
                </template>

                <!-- Model Code -->
                <template v-else-if="key === 'model_code'">
                  <v-chip
                    size="small"
                    :color="getModelChipColor(item.model_code)"
                    variant="tonal"
                    class="font-weight-black rounded-lg border px-2.5 font-mono"
                  >
                    نموذج {{ item.model_code || 'A' }}
                  </v-chip>
                </template>

                <!-- Print Status -->
                <template v-else-if="key === 'is_printed'">
                  <v-chip
                    size="small"
                    :color="item.is_printed ? 'success' : 'grey'"
                    :variant="item.is_printed ? 'flat' : 'tonal'"
                    class="font-weight-bold unified-table-chip cursor-pointer"
                    title="انقر لتبديل حالة الطباعة"
                    @click="toggleStudentPrintedStatus(item)"
                  >
                    <v-icon start size="14">{{ item.is_printed ? 'mdi-check-circle' : 'mdi-clock-outline' }}</v-icon>
                    {{ item.is_printed ? 'تمت الطباعة' : 'جاهز للطباعة' }}
                  </v-chip>
                </template>

                <!-- Actions -->
                <template v-else-if="key === 'actions'">
                  <div class="d-flex align-center justify-center gap-1">
                    <!-- Preview Dialog Button -->
                    <v-btn
                      icon
                      size="small"
                      variant="tonal"
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
                      variant="tonal"
                      color="success"
                      title="طباعة ورقة هذا الطالب فورياً"
                      @click="printSingleStudentDirect(item)"
                    >
                      <v-icon size="18">mdi-printer</v-icon>
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </div>
        </div>

        <!-- ════════════════════════════════════════════════════════════ -->
        <!-- TAB 2: QUESTIONS PAPER (كراسات نماذج الأسئلة الرسمية)          -->
        <!-- ════════════════════════════════════════════════════════════ -->
        <div v-if="isTabVisited('questions')" v-show="activeTab === 'questions'" class="questions-paper-viewport mb-6">
          <!-- شريط الإجراءات والمقاس الوزاري المعتمد -->
          <div class="main-card pa-3 px-4 rounded-2xl mb-4 bg-surface border elevation-1">
            <div class="d-flex align-center justify-space-between flex-wrap gap-2">
              <div class="d-flex align-center gap-2 flex-wrap">
                <v-btn
                  color="primary"
                  variant="flat"
                  rounded="lg"
                  class="font-weight-bold"
                  prepend-icon="mdi-printer"
                  @click="printAllFourQuestionPapers"
                >
                  طباعة كافة النماذج الأربعة (A, B, C, D)
                </v-btn>

                <v-btn-toggle
                  v-model="selectedQuestionPaperLayout"
                  mandatory
                  density="compact"
                  color="secondary"
                  variant="outlined"
                  rounded="lg"
                >
                  <v-btn value="a4" class="font-weight-bold px-3" prepend-icon="mdi-file-outline">
                    A4 الوزاري القياسي
                  </v-btn>
                  <v-btn value="a3" class="font-weight-bold px-3" prepend-icon="mdi-file-document-outline">
                    A3 عريض (عمودين)
                  </v-btn>
                </v-btn-toggle>
              </div>

              <div class="d-flex align-center gap-2">
                <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                  <v-icon start size="16">mdi-book-open-page-variant-outline</v-icon>
                  كراسات الأسئلة المعتمدة (4 نماذج)
                </v-chip>
              </div>
            </div>
          </div>

          <!-- الجدول الموحد لكراسات النماذج الأربعة (custom-data-table) -->
          <div class="main-card rounded-2xl overflow-hidden mb-6">
            <custom-data-table
              :items="questionModelsTableItems"
              :getData="getQuestionModelsData"
              :headers="questionModelsHeaders"
              :customLoading="loadingExamDetails"
              :hasFilter="false"
              :log="false"
              :restore="false"
              :numbering="true"
              :showSelect="false"
              :actions="false"
              :search="false"
              class="bg-transparent"
            >
              <template v-slot:item-slot="{ item, key, index }">
                <template v-if="key === 'numbering'">
                  <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
                </template>

                <!-- Model Code -->
                <template v-else-if="key === 'model_code'">
                  <v-chip
                    size="small"
                    :color="getModelChipColor(item.versionCode)"
                    variant="tonal"
                    class="font-weight-black rounded-lg border px-3 font-mono"
                  >
                    نموذج {{ item.versionCode }}
                  </v-chip>
                </template>

                <!-- Paper Title -->
                <template v-else-if="key === 'paper_title'">
                  <div class="py-1">
                    <div class="font-weight-bold text-body-2 text-on-surface">
                      كراسة أسئلة مادة {{ selectedExam?.subject_name || 'الاختبار' }} - النموذج ({{ item.versionCode }})
                    </div>
                    <div class="text-caption text-medium-emphasis mt-0.5">
                      {{ selectedExam?.title || 'اختبار معتمد' }} • {{ customExamYear || selectedExam?.year_name || 'العام الحالي' }}
                    </div>
                  </div>
                </template>

                <!-- Questions Count -->
                <template v-else-if="key === 'questions_count'">
                  <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                    {{ item.questionsCount }} سؤال
                  </v-chip>
                </template>

                <!-- Approved Layout -->
                <template v-else-if="key === 'layout_type'">
                  <span class="text-caption font-weight-bold text-medium-emphasis">
                    {{ selectedQuestionPaperLayout === 'a3' ? 'A3 عريض (عمودين)' : 'A4 الوزاري القياسي' }}
                  </span>
                </template>

                <!-- Paper Status -->
                <template v-else-if="key === 'status'">
                  <v-chip size="small" color="success" variant="tonal" class="font-weight-bold" prepend-icon="mdi-check-decagram-outline">
                    معتمد وجاهز
                  </v-chip>
                </template>

                <!-- Actions -->
                <template v-else-if="key === 'actions'">
                  <div class="d-flex align-center justify-center gap-2">
                    <v-btn
                      size="small"
                      color="secondary"
                      variant="tonal"
                      rounded="lg"
                      class="font-weight-bold"
                      prepend-icon="mdi-eye-outline"
                      @click="openPreviewQuestionPaper(item.versionCode)"
                    >
                      معاينة
                    </v-btn>
                    <v-btn
                      size="small"
                      color="primary"
                      variant="flat"
                      rounded="lg"
                      class="font-weight-bold"
                      prepend-icon="mdi-printer"
                      @click="printQuestionPaperForModel(item.versionCode)"
                    >
                      طباعة
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </div>

          <!-- نافذة حوار معاينة كراسة الأسئلة الرسمية المنبثقة -->
          <v-dialog v-model="previewQuestionPaperDialog" max-width="960" scrollable>
            <v-card rounded="2xl" class="overflow-hidden">
              <v-toolbar color="surface" density="comfortable" class="border-b px-4">
                <div class="d-flex align-center gap-2">
                  <v-avatar color="primary" variant="tonal" size="32" rounded="lg">
                    <v-icon size="18">mdi-file-document-outline</v-icon>
                  </v-avatar>
                  <span class="text-subtitle-1 font-weight-black">
                    معاينة كراسة الأسئلة الرسمية - نموذج {{ selectedQuestionsModelCode }}
                  </span>
                  <v-chip size="small" :color="getModelChipColor(selectedQuestionsModelCode)" variant="tonal" class="font-weight-bold ms-2">
                    نموذج {{ selectedQuestionsModelCode }}
                  </v-chip>
                </div>
                <v-spacer />
                <v-btn
                  color="primary"
                  variant="flat"
                  size="small"
                  rounded="lg"
                  class="font-weight-bold me-2"
                  prepend-icon="mdi-printer"
                  @click="printCurrentQuestionPaper"
                >
                  طباعة الكراسة الآن
                </v-btn>
                <v-btn icon size="small" variant="text" @click="previewQuestionPaperDialog = false">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </v-toolbar>
              <v-card-text class="pa-4 bg-grey-lighten-4 d-flex justify-center" style="max-height: 80vh;">
                <div ref="questionPaperRef" class="w-100 d-flex justify-center">
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
              </v-card-text>
            </v-card>
          </v-dialog>
        </div>

        <!-- ════════════════════════════════════════════════════════════ -->
        <!-- TAB 3: COMBINED PACKAGE (حزم الاختبار المتكاملة للطلاب)     -->
        <!-- ════════════════════════════════════════════════════════════ -->
        <div v-if="isTabVisited('package')" v-show="activeTab === 'package'" class="exam-package-viewport mb-6">
          <!-- شريط الإجراءات والبحث وفلاتر حزم الطلاب (منظم وموحد) -->
          <div class="main-card pa-3 px-4 rounded-2xl mb-4 bg-surface border elevation-1">
            <div class="d-flex align-center justify-space-between flex-wrap gap-2">
              <div class="d-flex align-center gap-2 flex-wrap">
                <v-btn
                  color="success"
                  variant="flat"
                  rounded="lg"
                  class="font-weight-bold"
                  prepend-icon="mdi-printer"
                  :loading="printingPackages"
                  :disabled="!filteredPackageStudents.length"
                  @click="batchPrintSelectedPackages"
                >
                  طباعة حزم الاختبار {{ selectedPackageStudentIds.length > 0 ? `المحددة (${selectedPackageStudentIds.length})` : `للكل (${filteredPackageStudents.length})` }}
                </v-btn>

                <v-btn
                  v-if="filteredPackageStudents.length > 0"
                  size="small"
                  variant="tonal"
                  color="primary"
                  class="font-weight-bold"
                  prepend-icon="mdi-checkbox-multiple-marked-outline"
                  @click="selectAllPackageStudents"
                >
                  {{ selectedPackageStudentIds.length === filteredPackageStudents.length ? 'إلغاء تحديد الكل' : 'تحديد كل المعروضين' }}
                </v-btn>
              </div>

              <!-- حقول التصفية والبحث -->
              <div class="d-flex align-center gap-2 flex-wrap">
                <div style="min-width: 190px; max-width: 230px;">
                  <v-select
                    v-model="packageModelFilter"
                    :items="modelFilterSelectOptions"
                    item-title="title"
                    item-value="value"
                    label="النموذج"
                    density="compact"
                    variant="outlined"
                    rounded="lg"
                    hide-details
                    prepend-inner-icon="mdi-layers-outline"
                  />
                </div>

                <div style="min-width: 220px; max-width: 280px;">
                  <v-text-field
                    v-model="packageSearch"
                    density="compact"
                    variant="outlined"
                    rounded="lg"
                    placeholder="بحث برقم الجلوس أو اسم الطالب..."
                    prepend-inner-icon="mdi-magnify"
                    hide-details
                    clearable
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- الجدول الموحد لحزم الاختبار المتكاملة للطلاب (custom-data-table) -->
          <div class="main-card rounded-2xl overflow-hidden mb-6">
            <custom-data-table
              :items="packageTableItems"
              :getData="getPackageData"
              :headers="packageHeaders"
              :customLoading="loadingExamDetails"
              :hasFilter="false"
              :log="false"
              :restore="false"
              :numbering="true"
              :showSelect="false"
              :actions="false"
              :search="false"
              class="bg-transparent"
            >
              <template v-slot:item-slot="{ item, key, index }">
                <template v-if="key === 'numbering'">
                  <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
                </template>

                <!-- Select Box -->
                <template v-else-if="key === 'select_box'">
                  <div class="d-flex justify-center">
                    <v-checkbox-btn
                      :model-value="selectedPackageStudentIds.includes(item.id)"
                      color="primary"
                      density="compact"
                      hide-details
                      @update:model-value="togglePackageStudentSelection(item.id)"
                    />
                  </div>
                </template>

                <!-- Seat Number -->
                <template v-else-if="key === 'seat_number'">
                  <span class="font-mono font-weight-black text-primary px-2 py-1 bg-blue-lighten-5 rounded-lg border">
                    {{ item.seat_number }}
                  </span>
                </template>

                <!-- Student Info -->
                <template v-else-if="key === 'student_name'">
                  <div class="d-flex align-center gap-2 py-1">
                    <v-avatar size="32" color="primary" variant="tonal" class="text-caption font-weight-black">
                      {{ (item.student_name || 'ط').slice(0, 1) }}
                    </v-avatar>
                    <div>
                      <div class="font-weight-bold text-body-2 text-on-surface">
                        {{ item.student_name || 'طالب بدون اسم' }}
                      </div>
                      <div class="text-caption text-medium-emphasis mt-0.5">
                        {{ item.school_name || selectedExam?.directorate || 'المركز الرئيسي' }}
                      </div>
                    </div>
                  </div>
                </template>

                <!-- School / Center -->
                <template v-else-if="key === 'school_name'">
                  <div class="py-1">
                    <div class="font-weight-medium text-body-2">{{ item.school_name || selectedExam?.directorate || 'المركز الرئيسي' }}</div>
                    <div class="text-caption text-medium-emphasis">{{ item.directorate || selectedExam?.directorate || '-' }}</div>
                  </div>
                </template>

                <!-- Model Code -->
                <template v-else-if="key === 'model_code'">
                  <v-chip
                    size="small"
                    :color="getModelChipColor(item.model_code)"
                    variant="tonal"
                    class="font-weight-black rounded-lg border px-2.5 font-mono"
                  >
                    نموذج {{ item.model_code || 'A' }}
                  </v-chip>
                </template>

                <!-- Package Contents -->
                <template v-else-if="key === 'package_contents'">
                  <div class="d-flex align-center justify-center gap-1 flex-wrap">
                    <v-chip size="x-small" color="secondary" variant="tonal" class="font-weight-bold">
                      <v-icon start size="12">mdi-file-document-outline</v-icon>
                      كراسة أسئلة ({{ item.model_code || 'A' }})
                    </v-chip>
                    <span class="text-caption text-disabled">+</span>
                    <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                      <v-icon start size="12">mdi-checkbox-marked-circle-outline</v-icon>
                      ورقة تظليل OMR
                    </v-chip>
                  </div>
                </template>

                <!-- Print Status -->
                <template v-else-if="key === 'is_printed'">
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

                <!-- Actions -->
                <template v-else-if="key === 'actions'">
                  <div class="d-flex align-center justify-center gap-1">
                    <v-btn
                      icon
                      size="small"
                      variant="tonal"
                      color="primary"
                      title="معاينة الحزمة المتكاملة"
                      @click="openPreviewPackage(item)"
                    >
                      <v-icon size="18">mdi-eye-outline</v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      size="small"
                      variant="tonal"
                      color="success"
                      title="طباعة حزمة هذا الطالب"
                      @click="printSingleStudentPackage(item)"
                    >
                      <v-icon size="18">mdi-printer</v-icon>
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </div>

          <!-- نافذة حوار معاينة حزمة الاختبار المتكاملة للطلاب المنبثقة -->
          <v-dialog v-model="previewPackageDialog" max-width="960" scrollable>
            <v-card rounded="2xl" class="overflow-hidden" v-if="previewPackageStudent">
              <v-toolbar color="surface" density="comfortable" class="border-b px-4">
                <div class="d-flex align-center gap-2">
                  <v-avatar color="primary" variant="tonal" size="32" rounded="lg">
                    <v-icon size="18">mdi-package-variant-closed</v-icon>
                  </v-avatar>
                  <span class="text-subtitle-1 font-weight-black">
                    معاينة حزمة الاختبار للطالب: {{ previewPackageStudent.student_name }}
                  </span>
                  <v-chip size="small" :color="getModelChipColor(previewPackageStudent.model_code)" variant="tonal" class="font-weight-bold ms-2">
                    نموذج {{ previewPackageStudent.model_code || 'A' }}
                  </v-chip>
                </div>
                <v-spacer />
                <v-btn
                  color="success"
                  variant="flat"
                  size="small"
                  rounded="lg"
                  class="font-weight-bold me-2"
                  prepend-icon="mdi-printer"
                  @click="printSingleStudentPackage(previewPackageStudent)"
                >
                  طباعة حزمة الطالب
                </v-btn>
                <v-btn icon size="small" variant="text" @click="previewPackageDialog = false">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </v-toolbar>
              <v-card-text class="pa-4 bg-grey-lighten-4" style="max-height: 80vh;">
                <div class="d-flex flex-column align-center gap-6">
                  <div class="text-caption font-weight-black text-primary border-b pb-1 w-100 text-center d-flex align-center justify-center gap-1">
                    <v-icon size="16" color="primary">mdi-file-document-outline</v-icon>
                    <span>الجزء 1: كراسة ورقة الأسئلة الرسمية المعتمدة (نموذج {{ previewPackageStudent.model_code || 'A' }})</span>
                  </div>
                  <YemeniOfficialQuestionPaper
                    :exam-title="customStageTitle || selectedExam?.title || ''"
                    :exam-subject="selectedExam?.subject_name || ''"
                    :stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || ''))"
                    :exam-year="customExamYear || selectedExam?.year_name || ''"
                    :governorate="customGovernorate || selectedExam?.governorate || ''"
                    :directorate="customDirectorate || selectedExam?.directorate || ''"
                    :center-name="customCenterName || previewPackageStudent.school_name || selectedExam?.school_name || selectedExam?.center_name || 'المركز الامتحاني الرئيسي'"
                    :center-code="previewPackageStudent.school_id || selectedExam?.center_code || selectedExam?.id || '11'"
                    :exam-time="selectedExam?.time_allowed || selectedExam?.exam_time || ''"
                    :day-name="selectedExam?.day_name || ''"
                    :exam-date="selectedExam?.exam_date || ''"
                    :envelope-no="selectedExam?.envelope_no || '1'"
                    :student-name="previewPackageStudent.student_name"
                    :seat-number="previewPackageStudent.seat_number"
                    :secret-number="previewPackageStudent.secret_number || '60'"
                    :model-code="previewPackageStudent.model_code || 'A'"
                    :questions="examDetails?.versions?.find(v => v.versionCode === (previewPackageStudent.model_code || 'A'))?.questions || []"
                    :default-layout="'a4'"
                  />

                  <div class="text-caption font-weight-black text-teal border-b pb-1 w-100 text-center mt-4 d-flex align-center justify-center gap-1">
                    <v-icon size="16" color="teal">mdi-checkbox-marked-circle-outline</v-icon>
                    <span>الجزء 2: ورقة التظليل الإلكترونية OMR المخصصة للطالب</span>
                  </div>
                  <div class="sheet-page-card elevation-4 bg-white rounded-lg position-relative d-inline-block text-start" :style="sheetArtboardStyle">
                    <YemeniMinistrySheet
                      layout-mode="compact_a5"
                      :student-name="previewPackageStudent.student_name"
                      :seat-number="previewPackageStudent.seat_number"
                      :serial-number="previewPackageStudent.secret_number || previewPackageStudent.model_code"
                      :model-code="previewPackageStudent.model_code || 'A'"
                      :exam-subject="selectedExam?.subject_name || 'الرياضيات'"
                      :exam-stage-title="customStageTitle || (selectedExam?.stage_name ? `اختبار ${selectedExam.stage_name}` : (selectedExam?.title || 'اختبار الشهادة الثانوية العامة'))"
                      :exam-year="customExamYear || selectedExam?.year_name || '2026'"
                      :center-name="customCenterName || previewPackageStudent.school_name || selectedExam?.directorate || 'المركز الامتحاني الرئيسي'"
                      :governorate="customGovernorate || selectedExam?.governorate || 'أمانة العاصمة'"
                      :directorate="customDirectorate || previewPackageStudent.directorate || selectedExam?.directorate || 'السبعين'"
                      :barcode-value="`EXAM_${selectedExam?.id}_VER_${previewPackageStudent.model_code || 'A'}_SEAT_${previewPackageStudent.seat_number}`"
                      :qr-value="`${selectedExam?.uniqueCode}|${previewPackageStudent.model_code || 'A'}|${previewPackageStudent.seat_number}`"
                      :field-layout="examFieldLayout"
                      :institution-type="previewPackageStudent.institution_type || selectedExam?.institution_type || institutionType || 'school'"
                      :college-name="previewPackageStudent.college_name || selectedExam?.college_name || ''"
                      :major-name="previewPackageStudent.major_name || selectedExam?.major_name || ''"
                      :academic-year="previewPackageStudent.academic_year || selectedExam?.academic_year || ''"
                      :semester-name="previewPackageStudent.semester_name || selectedExam?.semester_name || ''"
                      :course-name="previewPackageStudent.course_name || selectedExam?.subject_name || ''"
                      :course-code="previewPackageStudent.course_code || selectedExam?.subject_code || ''"
                      :student-level="previewPackageStudent.student_level || selectedExam?.stage_name || ''"
                      :group-section="previewPackageStudent.group_section || ''"
                      :term-name="previewPackageStudent.term_name || ''"
                      :student-id="previewPackageStudent.seat_number"
                      :is-preview="true"
                    />
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </v-dialog>
        </div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════════════ -->
    <!-- TAB 4: سجل الدفعات السابقة المطبوعة                                 -->
    <!-- ══════════════════════════════════════════════════════════════════ -->
    <div v-if="isTabVisited('history')" v-show="activeTab === 'history'">
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
            items: batchesTableItems,
            getData: getBatchesData,
            headers,
            loading: loadingBatches,
          }"
          :actions="false"
          :hasFilter="false"
          :log="false"
          :restore="false"
        >
          <template v-slot:item-slot="{ item, key, index }">
            <template v-if="key === 'numbering'">
              <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
            </template>
            <template v-else-if="key === 'batch_info'">
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
                items: batchStudentsTableItems,
                getData: getBatchStudentsData,
                headers: studentsHeaders,
              }"
              :hasFilter="false"
              :log="false"
              :restore="false"
              :actions="false"
            >
              <template v-slot:item-slot="{ item, key, index }">
                <template v-if="key === 'numbering'">
                  <span class="font-weight-bold text-caption text-medium-emphasis">{{ (index ?? 0) + 1 }}</span>
                </template>
                <template v-else-if="key === 'seat_number'">
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

        <!-- Single Sheet Preview Dialog (معاينة ورقة التظليل الفردية - مطابق لتصميم omr-human-review) -->
    <v-dialog v-model="singleSheetDialog" max-width="850px" scrollable>
      <v-card v-if="previewStudent" class="rounded-2xl overflow-hidden main-card">
        <!-- Dialog Header (مطابق تماماً لـ omr-human-review) -->
        <v-card-title class="d-flex align-center justify-space-between bg-surface px-6 py-4 border-b">
          <div class="d-flex align-center gap-3">
            <v-avatar color="primary" variant="tonal" rounded="lg" size="44">
              <v-icon size="24" color="primary">mdi-card-account-details-outline</v-icon>
            </v-avatar>
            <div>
              <div class="d-flex align-center gap-2 flex-wrap">
                <h3 class="text-h6 font-weight-black text-on-surface mb-0">
                  {{ previewStudent.student_name || 'طالب بدون اسم' }}
                </h3>
                <v-chip size="small" color="primary" variant="flat" class="font-weight-bold px-2 unified-table-chip">
                  رقم الجلوس: {{ previewStudent.seat_number }}
                </v-chip>
                <v-chip size="small" :color="getModelChipColor(previewStudent.model_code)" variant="tonal" class="font-weight-bold px-2.5 rounded-lg border">
                  نموذج {{ previewStudent.model_code || 'A' }}
                </v-chip>
              </div>
              <p class="text-caption text-medium-emphasis mb-0 mt-1">
                {{ selectedExam?.title || 'اختبار عام' }} • {{ previewStudent.school_name || selectedExam?.directorate || 'المركز الاختباري' }}
              </p>
            </div>
          </div>

          <div class="d-flex align-center gap-2">
            <v-btn
              color="success"
              variant="flat"
              rounded="lg"
              size="default"
              class="font-weight-black px-4 shadow-sm"
              prepend-icon="mdi-printer"
              @click="printPreviewStudentSheet"
            >
              طباعة هذه الورقة
            </v-btn>
            <v-btn icon="mdi-close" variant="text" size="small" color="medium-emphasis" @click="singleSheetDialog = false" />
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
              <div class="text-subtitle-1 font-weight-black text-on-surface">{{ selectedSchoolDialogItem?.name }}</div>
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
              كل صف أدناه يمثل <strong>اختباراً مستقلاً معتمداً</strong> مقيد به طلاب المدرسة، وموضح أمامه <strong>النماذج الامتحانية (A, B, C...)</strong> وتوزيع الطلاب عليها، مع إمكانية طباعة وثائق أي اختبار مباشرة.
            </v-alert>

            <!-- ── الجدول الموحد للاختبارات والمواد المعتمدة للمدرسة (custom-data-table) ── -->
            <div class="main-card rounded-2xl overflow-hidden border">
              <custom-data-table
                :items="schoolExamsTableItems"
                :getData="getSchoolExamsData"
                :headers="schoolExamsHeaders"
                :hasFilter="false"
                :log="false"
                :restore="false"
                :showSelect="false"
                :actions="false"
                :search="false"
              >
                <template v-slot:item-slot="{ item, key }">
                  <template v-if="key === 'code'">
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
                            اختبار مستقل
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
                        {{ item.students_count || 0 }} طالب
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
                        نموذج {{ v.code }} ({{ v.students_count }} طالب)
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
                        prepend-icon="mdi-printer"
                        class="font-weight-bold px-3"
                        @click="selectExamFromSchoolDialog(item, selectedSchoolDialogItem)"
                      >
                        طباعة
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
            يمكنك اختيار اختبار معين للطباعة أو فتح استوديو الطباعة الشامل للمركز
          </div>
          <div class="d-flex gap-2">
            <v-btn variant="tonal" color="grey" rounded="lg" class="font-weight-bold px-4" @click="schoolExamsDialog = false">
              إغلاق
            </v-btn>
            <v-btn
              color="primary"
              variant="flat"
              rounded="lg"
              prepend-icon="mdi-printer-check"
              class="font-weight-bold px-4"
              @click="openSchoolStudio(selectedSchoolDialogItem); schoolExamsDialog = false;"
            >
              فتح استوديو الطباعة الشامل للمركز
            </v-btn>
          </div>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
const sectorOptions = [
  { title: 'التعليم العام (المدرسي)', value: 'school', icon: 'mdi-school' },
  { title: 'التعليم الجامعي (كليات وجامعات)', value: 'university', icon: 'mdi-domain' },
  { title: 'التعليم الفني والمهني (معاهد)', value: 'institute', icon: 'mdi-tools' },
]
const loadingMaster = ref(false)
const masterSearchQuery = ref('')

const selectedOfficeId = ref(null)
const selectedOfficeName = ref('')
const selectedDirectorateId = ref(null)
const selectedDirectorateName = ref('')
const selectedSchoolId = ref(null)
const selectedSchoolName = ref('')
const selectedSubjectId = ref(null)
const selectedSubjectName = ref('')
const subjectsList = ref([])

// Dialog for School Exams List
const schoolExamsDialog = ref(false)
const selectedSchoolDialogItem = ref(null)

const officesList = ref([])
const directoratesList = ref([])
const schoolsList = ref([])
const masterExamsList = ref([])
const batches = ref([])
const loadingBatches = ref(false)

// Master Table Headers
const officeMasterHeaders = [
  { title: "مكتب التربية والتعليم (المحافظة)", key: "office_name", sortable: true, align: "start", width: "340px", minWidth: "320px" },
  { title: "المديريات", key: "directorates_count", sortable: true, align: "center", width: "95px" },
  { title: "المراكز والمدارس", key: "schools_count", sortable: true, align: "center", width: "125px" },
  { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "95px" },
  { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
  { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "120px" },
  { title: "نسبة الإنجاز", key: "printed_rate", sortable: true, align: "center", width: "130px" },
  { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "120px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "220px" },
]

const directorateMasterHeaders = [
  { title: "إدارة التربية والتعليم (المديرية)", key: "name", sortable: true, align: "start", width: "340px", minWidth: "320px" },
  { title: "المكتب التابع له", key: "office_name", sortable: true, align: "center", width: "180px" },
  { title: "المراكز والمدارس", key: "schools_count", sortable: true, align: "center", width: "125px" },
  { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "95px" },
  { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
  { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "120px" },
  { title: "نسبة الإنجاز", key: "printed_rate", sortable: true, align: "center", width: "130px" },
  { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "120px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "220px" },
]

const schoolMasterHeaders = [
  { title: "المدرسة / المركز الامتحاني", key: "name", sortable: true, align: "start", width: "320px", minWidth: "280px" },
  { title: "نوع المؤسسة", key: "institution_type", sortable: true, align: "center", width: "105px" },
  { title: "المحافظة والمديرية", key: "directorate_name", sortable: true, align: "center", width: "170px" },
  { title: "المادة الدراسية", key: "subject_name", sortable: true, align: "center", width: "160px" },
  { title: "الاختبارات", key: "exams_count", sortable: true, align: "center", width: "105px" },
  { title: "إجمالي الطلاب", key: "total_students", sortable: true, align: "center", width: "110px" },
  { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "115px" },
  { title: "نسبة الطباعة", key: "printed_rate", sortable: true, align: "center", width: "120px" },
  { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "115px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "190px" },
]

const schoolExamsHeaders = [
  { title: "رمز الاختبار", key: "code", sortable: true, align: "center", width: "135px" },
  { title: "عنوان الاختبار والمواصفات", key: "title", sortable: true, align: "start" },
  { title: "المادة الدراسية", key: "subject", sortable: true, align: "center", width: "120px" },
  { title: "طلاب المركز", key: "students_count", sortable: true, align: "center", width: "105px" },
  { title: "النماذج المخصصة للطلاب وتوزيعها", key: "versions", sortable: false, align: "center", width: "230px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "110px" },
]

const examMasterHeaders = [
  { title: "رمز الاختبار", key: "uniqueCode", sortable: true, align: "center", width: "140px" },
  { title: "عنوان الاختبار والمادة", key: "title", sortable: true, align: "start", width: "340px", minWidth: "300px" },
  { title: "المدارس المشاركة", key: "schools_count", sortable: true, align: "center", width: "125px" },
  { title: "المقيدون", key: "total_registered", sortable: true, align: "center", width: "110px" },
  { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "120px" },
  { title: "نسبة الطباعة", key: "printed_rate", sortable: true, align: "center", width: "130px" },
  { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "120px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "160px" },
]

const registryMasterHeaders = [
  { title: "رقم الدفعة", key: "batch_id", sortable: true, align: "center", width: "170px" },
  { title: "عنوان الاختبار", key: "exam_title", sortable: true, align: "start", width: "300px", minWidth: "260px" },
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
  if (selectedSubjectId.value) {
    list = list.filter(o => (o.exams_count || 0) > 0)
  }
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
  if (selectedSubjectId.value) {
    list = list.filter(d => (d.exams_count || 0) > 0)
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
  if (selectedSubjectId.value) {
    const sObj = subjectsList.value.find(s => s.id === selectedSubjectId.value)
    const sName = sObj?.name?.trim()
    list = list.filter(s => {
      if (s.subjects && Array.isArray(s.subjects)) {
        return s.subjects.some(sub => sub === sName || (sName && sub.includes(sName)))
      }
      return s.subject_name === sName || (sName && s.subject_name && s.subject_name.includes(sName))
    })
  }
  if (masterSearchQuery.value) {
    const q = masterSearchQuery.value.toLowerCase().trim()
    list = list.filter(s => 
      (s.name && s.name.toLowerCase().includes(q)) ||
      (s.directorate_name && s.directorate_name.toLowerCase().includes(q)) ||
      (s.governorate_name && s.governorate_name.toLowerCase().includes(q)) ||
      (s.subject_name && s.subject_name.toLowerCase().includes(q))
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
  if (selectedSubjectId.value) {
    list = list.filter(e => e.subject_id === selectedSubjectId.value || e.subject === selectedSubjectId.value)
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

// ── Master Tables Selection State ──
const selectedOfficeMasterRows = ref([])
const selectedDirectorateMasterRows = ref([])
const selectedSchoolMasterRows = ref([])
const selectedExamMasterRows = ref([])
const selectedBatchMasterRows = ref([])

// ── Master Tables Reactive State for custom-data-table ──
const officeMasterTableItems = ref({
  results: [],
  count: 0,
  pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
})

const getOfficeMasterData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = p.page || 1
  const pageSize = p.page_size || 20
  const all = filteredOfficesTable.value || []
  const start = (page - 1) * pageSize
  officeMasterTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
    },
  }
  return officeMasterTableItems.value
}

const directorateMasterTableItems = ref({
  results: [],
  count: 0,
  pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
})

const getDirectorateMasterData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = p.page || 1
  const pageSize = p.page_size || 20
  const all = filteredDirectoratesTable.value || []
  const start = (page - 1) * pageSize
  directorateMasterTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
    },
  }
  return directorateMasterTableItems.value
}

const schoolMasterTableItems = ref({
  results: [],
  count: 0,
  pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
})

const getSchoolMasterData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = p.page || 1
  const pageSize = p.page_size || 20
  const all = filteredSchoolsTable.value || []
  const start = (page - 1) * pageSize
  schoolMasterTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
    },
  }
  return schoolMasterTableItems.value
}

const schoolExamsPage = ref(1)
const schoolExamsPageSize = ref(10)
const schoolExamsTableItems = ref({
  results: [],
  count: 0,
  pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
})

const getSchoolExamsData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = Number(p.page) || schoolExamsPage.value || 1
  const pageSize = Number(p.page_size) || schoolExamsPageSize.value || 10
  schoolExamsPage.value = page
  schoolExamsPageSize.value = pageSize

  const all = selectedSchoolDialogItem.value?.exams || []
  const total = all.length
  const numPages = Math.ceil(total / pageSize) || 1
  const validPage = Math.min(Math.max(1, page), numPages)
  const start = (validPage - 1) * pageSize

  schoolExamsTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: total,
    pagination: {
      count: total,
      total: total,
      num_pages: numPages,
      current_page: validPage,
    },
  }
  return schoolExamsTableItems.value
}

const examMasterTableItems = ref({
  results: [],
  count: 0,
  pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
})

const getExamMasterData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = p.page || 1
  const pageSize = p.page_size || 20
  const all = filteredMasterExamsTable.value || []
  const start = (page - 1) * pageSize
  examMasterTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
    },
  }
  return examMasterTableItems.value
}

const batchMasterTableItems = ref({
  results: [],
  count: 0,
  pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
})

const getBatchMasterData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = p.page || 1
  const pageSize = p.page_size || 20
  const all = filteredBatchesTable.value || []
  const start = (page - 1) * pageSize
  batchMasterTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
    },
  }
  return batchMasterTableItems.value
}

watch(filteredOfficesTable, () => {
  getOfficeMasterData()
}, { immediate: true })

watch(filteredDirectoratesTable, () => {
  getDirectorateMasterData()
}, { immediate: true })

watch(filteredSchoolsTable, () => {
  getSchoolMasterData()
}, { immediate: true })

watch(filteredMasterExamsTable, () => {
  getExamMasterData()
}, { immediate: true })

watch(filteredBatchesTable, () => {
  getBatchMasterData()
}, { immediate: true })

watch(masterTab, (tab) => {
  if (tab === 'offices') getOfficeMasterData()
  else if (tab === 'directorates') getDirectorateMasterData()
  else if (tab === 'schools') getSchoolMasterData()
  else if (tab === 'exams') getExamMasterData()
  else if (tab === 'registry') getBatchMasterData()
})

// Master Methods
const loadSubjects = async () => {
  try {
    const res = await gradebookAPI.getSubjects()
    subjectsList.value = res.data?.results || []
  } catch (err) {
    console.error('Failed to load subjects:', err)
  }
}

const loadMasterData = async () => {
  loadingMaster.value = true
  try {
    const params = {
      institution_type: institutionType.value !== 'all' ? institutionType.value : undefined,
      subject: selectedSubjectId.value || undefined,
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
    getOfficeMasterData()
    getDirectorateMasterData()
    getSchoolMasterData()
    getExamMasterData()
    getBatchMasterData()
  } catch (err) {
    console.error('Failed to load master data:', err)
  } finally {
    loadingMaster.value = false
  }
}

const resetHierarchyFilters = async () => {
  institutionType.value = 'school'
  selectedOfficeId.value = null
  selectedOfficeName.value = ''
  selectedDirectorateId.value = null
  selectedDirectorateName.value = ''
  selectedSchoolId.value = null
  selectedSchoolName.value = ''
  selectedSubjectId.value = null
  selectedSubjectName.value = ''
  masterSearchQuery.value = ''
  await loadMasterData()
}

const onSectorChange = (val) => {
  institutionType.value = val
  selectedOfficeId.value = null
  selectedOfficeName.value = ''
  selectedDirectorateId.value = null
  selectedDirectorateName.value = ''
  selectedSchoolId.value = null
  selectedSchoolName.value = ''
  selectedSubjectId.value = null
  selectedSubjectName.value = ''
  if (currentView.value === 'master') {
    loadMasterData()
  } else {
    fetchExamsList()
  }
}

const onSubjectFilterChange = async (subjId) => {
  selectedSubjectId.value = subjId
  if (subjId) {
    const s = subjectsList.value.find(item => item.id === subjId)
    selectedSubjectName.value = s?.name || ''
  } else {
    selectedSubjectName.value = ''
  }
  await loadMasterData()
}

const openSchoolExamsDialog = (schoolItem) => {
  selectedSchoolDialogItem.value = schoolItem
  schoolExamsPage.value = 1
  getSchoolExamsData({ page: 1, page_size: schoolExamsPageSize.value })
  schoolExamsDialog.value = true
}

watch(selectedSchoolDialogItem, () => {
  if (schoolExamsDialog.value) {
    getSchoolExamsData({ page: 1, page_size: schoolExamsPageSize.value })
  }
})

const selectExamFromSchoolDialog = async (exam, school) => {
  schoolExamsDialog.value = false
  selectedExamId.value = exam.id
  if (school) {
    selectedSchoolId.value = school.id
    selectedSchoolName.value = school.name
    if (school.directorate_name) selectedDirectorateName.value = school.directorate_name
    if (school.governorate_name) selectedOfficeName.value = school.governorate_name
  }
  currentView.value = 'detail'
  await loadExamDetails(exam.id, {
    school_id: school?.id || undefined,
  })
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
  showHierarchyFilters.value = false
  await loadMasterData()
}

const clearSchoolFilter = async () => {
  selectedSchoolId.value = null
  selectedSchoolName.value = ''
  if (selectedExamId.value) {
    await loadExamDetails(selectedExamId.value)
  }
}

// Studio Hierarchical Filter Handlers
const onStudioOfficeChange = async (officeId) => {
  onOfficeFilterChange(officeId)
  await fetchExamsList()
  if (examsList.value && examsList.value.length > 0) {
    if (!examsList.value.some(e => e.id === selectedExamId.value)) {
      selectedExamId.value = examsList.value[0].id
      await loadExamDetails(selectedExamId.value)
    }
  } else {
    selectedExamId.value = null
    examDetails.value = null
  }
}

const onStudioDirectorateChange = async (dirId) => {
  onDirectorateFilterChange(dirId)
  await fetchExamsList()
  if (examsList.value && examsList.value.length > 0) {
    if (!examsList.value.some(e => e.id === selectedExamId.value)) {
      selectedExamId.value = examsList.value[0].id
      await loadExamDetails(selectedExamId.value)
    }
  } else {
    selectedExamId.value = null
    examDetails.value = null
  }
}

const onStudioSchoolChange = async (schoolId) => {
  onSchoolFilterChange(schoolId)
  await fetchExamsList()
  if (examsList.value && examsList.value.length > 0) {
    if (!examsList.value.some(e => e.id === selectedExamId.value)) {
      selectedExamId.value = examsList.value[0].id
      await loadExamDetails(selectedExamId.value)
    }
  } else {
    selectedExamId.value = null
    examDetails.value = null
  }
}

const resetHierarchyStudioFilters = async () => {
  selectedOfficeId.value = null
  selectedOfficeName.value = ''
  selectedDirectorateId.value = null
  selectedDirectorateName.value = ''
  selectedSchoolId.value = null
  selectedSchoolName.value = ''
  await fetchExamsList()
  if (examsList.value && examsList.value.length > 0) {
    selectedExamId.value = examsList.value[0].id
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
const isTabVisited = (tab) => {
  return visitedTabs.value ? visitedTabs.value.has(tab) : true
}
const switchDetailTab = (tab) => {
  activeTab.value = tab
  if (visitedTabs.value) {
    visitedTabs.value.add(tab)
  }
}

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
  if (newTab === 'unified') {
    getRosterData()
  } else if (newTab === 'questions') {
    getQuestionModelsData()
  } else if (newTab === 'package') {
    getPackageData()
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
const showHierarchyFilters = ref(false)
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
const searchQuery = ref('')
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
  const students = examDetails.value?.registered_students || []
  const total = students.length
  const list = [
    { title: `كافة النماذج (${total})`, value: 'all' }
  ]
  const versions = examDetails.value?.versions || []
  if (versions.length > 0) {
    versions.forEach(v => {
      const count = students.filter(s => (s.model_code || 'A') === v.versionCode).length
      list.push({ title: `نموذج ${v.versionCode} (${count})`, value: v.versionCode })
    })
  } else {
    ['A', 'B', 'C', 'D'].forEach(code => {
      const count = students.filter(s => (s.model_code || 'A') === code).length
      list.push({ title: `نموذج ${code} (${count})`, value: code })
    })
  }
  return list
})

const printStatusFilterOptions = computed(() => {
  const students = examDetails.value?.registered_students || []
  return [
    { title: `كافة الحالات (${students.length})`, value: 'all' },
    { title: `جاهز للطباعة (${unprintedCount.value})`, value: 'unprinted' },
    { title: `المطبوعة (${printedCount.value})`, value: 'printed' },
  ]
})

const resetRosterFilters = () => {
  rosterModelFilter.value = 'all'
  rosterPrintFilter.value = 'all'
  rosterSearch.value = ''
}

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

const rosterHeaders = computed(() => [
  { title: "تحديد", key: "select_box", sortable: false, align: "center", width: "65px" },
  { title: "رقم الجلوس", key: "seat_number", sortable: true, align: "center", width: "110px" },
  { title: "الرقم السري", key: "secret_number", sortable: true, align: "center", width: "100px" },
  { title: "اسم الطالب الرباعي", key: "student_name", sortable: true, align: "start" },
  { title: "المدرسة والمركز", key: "school_name", sortable: true, align: "start" },
  { title: "النموذج", key: "model_code", sortable: true, align: "center", width: "115px" },
  { title: "حالة الطباعة", key: "is_printed", sortable: true, align: "center", width: "135px" },
  { title: "إجراءات الطباعة والمعاينة", key: "actions", sortable: false, align: "center", width: "130px" },
])

const toggleStudentSelection = (studentId) => {
  const idx = selectedStudentIds.value.indexOf(studentId)
  if (idx > -1) {
    selectedStudentIds.value.splice(idx, 1)
  } else {
    selectedStudentIds.value.push(studentId)
  }
}

const unprintedCount = computed(() => {
  return (examDetails.value?.registered_students || []).filter(s => !s.is_printed).length
})

const printedCount = computed(() => {
  return (examDetails.value?.registered_students || []).filter(s => s.is_printed).length
})

const modelCounts = computed(() => {
  const students = examDetails.value?.registered_students || []
  return {
    all: students.length,
    A: students.filter(s => (s.model_code || 'A') === 'A').length,
    B: students.filter(s => s.model_code === 'B').length,
    C: students.filter(s => s.model_code === 'C').length,
    D: students.filter(s => s.model_code === 'D').length,
  }
})

const getModelChipColor = (code) => {
  switch (code) {
    case 'A': return 'primary'
    case 'B': return 'deep-purple'
    case 'C': return 'amber-darken-3'
    case 'D': return 'teal'
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

const rosterTableItems = ref({
  results: [],
  count: 0,
  pagination: {
    count: 0,
    total: 0,
    num_pages: 1,
    current_page: 1,
  },
})

const getRosterData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = p.page || 1
  const pageSize = p.page_size || 50
  const all = filteredRosterStudents.value || []
  const start = (page - 1) * pageSize
  rosterTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
    },
  }
  return rosterTableItems.value
}

watch(filteredRosterStudents, () => {
  getRosterData()
}, { immediate: true })

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

const batchesPage = ref(1)
const batchesPageSize = ref(10)
const batchesTableItems = ref({
  results: [],
  count: 0,
  pagination: {
    count: 0,
    total: 0,
    num_pages: 1,
    current_page: 1,
  },
})

const getBatchesData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = Number(p.page) || batchesPage.value || 1
  const pageSize = Number(p.page_size) || batchesPageSize.value || 10
  batchesPage.value = page
  batchesPageSize.value = pageSize

  const all = batches.value || []
  const total = all.length
  const numPages = Math.ceil(total / pageSize) || 1
  const validPage = Math.min(Math.max(1, page), numPages)
  const start = (validPage - 1) * pageSize

  batchesTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: total,
    pagination: {
      count: total,
      total: total,
      num_pages: numPages,
      current_page: validPage,
    },
  }
  return batchesTableItems.value
}

watch(batches, () => {
  batchesPage.value = 1
  getBatchesData({ page: 1, page_size: batchesPageSize.value })
}, { immediate: true })

const tableItems = computed(() => batchesTableItems.value)

const studentsHeaders = computed(() => [
  { title: "رقم الجلوس", key: "seat_number", sortable: true, align: "center" },
  { title: "اسم الطالب", key: "student_name", sortable: true },
  { title: "النموذج", key: "model_code", sortable: true, align: "center" },
  { title: "وقت الطباعة الفعلي", key: "printed_at", sortable: true, align: "center" },
])

const batchStudentsPage = ref(1)
const batchStudentsPageSize = ref(10)
const batchStudentsTableItems = ref({
  results: [],
  count: 0,
  pagination: {
    count: 0,
    total: 0,
    num_pages: 1,
    current_page: 1,
  },
})

const getBatchStudentsData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = Number(p.page) || batchStudentsPage.value || 1
  const pageSize = Number(p.page_size) || batchStudentsPageSize.value || 10
  batchStudentsPage.value = page
  batchStudentsPageSize.value = pageSize

  const all = batchStudents.value || []
  const total = all.length
  const numPages = Math.ceil(total / pageSize) || 1
  const validPage = Math.min(Math.max(1, page), numPages)
  const start = (validPage - 1) * pageSize

  batchStudentsTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: total,
    pagination: {
      count: total,
      total: total,
      num_pages: numPages,
      current_page: validPage,
    },
  }
  return batchStudentsTableItems.value
}

watch(batchStudents, () => {
  batchStudentsPage.value = 1
  getBatchStudentsData({ page: 1, page_size: batchStudentsPageSize.value })
}, { immediate: true })

const studentsTableItems = computed(() => batchStudentsTableItems.value)

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
    showHierarchyFilters.value = false
    if (resp.data.registered_students && resp.data.registered_students.length > 0) {
      selectedStudentId.value = resp.data.registered_students[0].id
      sheetGenerationMode.value = 'all_students'
    } else {
      sheetGenerationMode.value = 'blank'
    }
    await getRosterData()
    await getQuestionModelsData()
    await getPackageData()
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

// State & Methods for Tab 2: Question Booklets
const previewQuestionPaperDialog = ref(false)
const questionModelsList = computed(() => {
  const models = ['A', 'B', 'C', 'D']
  return models.map(code => {
    const ver = examDetails.value?.versions?.find(v => v.versionCode === code)
    const qCount = ver?.questions?.length || 56
    return {
      versionCode: code,
      title: `كراسة ورقة الأسئلة - نموذج ${code}`,
      questionsCount: qCount,
      hasQuestions: !!(ver?.questions && ver.questions.length > 0)
    }
  })
})

const questionModelsHeaders = computed(() => [
  { title: "النموذج", key: "model_code", sortable: false, align: "center", width: "120px" },
  { title: "عنوان كراسة الأسئلة", key: "paper_title", sortable: false, align: "start" },
  { title: "عدد الأسئلة", key: "questions_count", sortable: false, align: "center", width: "130px" },
  { title: "المقاس المعتمد", key: "layout_type", sortable: false, align: "center", width: "170px" },
  { title: "حالة الكراسة", key: "status", sortable: false, align: "center", width: "150px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "230px" },
])

const questionModelsTableItems = ref({
  results: [],
  count: 0,
  pagination: {
    count: 0,
    total: 0,
    num_pages: 1,
    current_page: 1,
  },
})

const getQuestionModelsData = async (params = {}) => {
  const all = questionModelsList.value || []
  questionModelsTableItems.value = {
    results: all,
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: 1,
      current_page: 1,
    },
  }
  return questionModelsTableItems.value
}

watch(questionModelsList, () => {
  getQuestionModelsData()
}, { immediate: true })

const openPreviewQuestionPaper = (modelCode) => {
  selectedQuestionsModelCode.value = modelCode
  previewQuestionPaperDialog.value = true
}

const printQuestionPaperForModel = async (modelCode) => {
  selectedQuestionsModelCode.value = modelCode
  await nextTick()
  const verObj = examDetails.value?.versions?.find(ver => ver.versionCode === modelCode) || examDetails.value?.versions?.[0]
  await printExamPackage({
    examTitle: customStageTitle.value || selectedExam.value?.title || 'اختبار الشهادة العامة',
    subjectName: selectedExam.value?.subject_name || 'الرياضيات',
    stageName: selectedExam.value?.stage_name || '',
    yearName: customExamYear.value || selectedExam.value?.year_name || '1446هـ - 2024-2025م',
    governorate: customGovernorate.value || selectedExam.value?.governorate || 'أمانة العاصمة',
    directorate: customDirectorate.value || selectedExam.value?.directorate || 'السبعين',
    centerName: customCenterName.value || selectedExam.value?.school_name || selectedExam.value?.directorate || 'المركز الاختباري الرئيسي',
    centerCode: selectedExam.value?.id || '3026',
    versionCode: modelCode,
    studentName: '',
    seatNumber: '',
    secretNumber: '',
    isA3: selectedQuestionPaperLayout.value === 'a3',
    questions: verObj?.questions || [],
    mode: 'questions_only'
  })
}

const printAllFourQuestionPapers = async () => {
  for (const ver of ['A', 'B', 'C', 'D']) {
    await printQuestionPaperForModel(ver)
  }
}

// State & Methods for Tab 3: Combined Student Packages
const packageSearch = ref('')
const packageModelFilter = ref('all')
const selectedPackageStudentIds = ref([])
const previewPackageStudent = ref(null)
const previewPackageDialog = ref(false)
const printingPackages = ref(false)

const packageHeaders = computed(() => [
  { title: "تحديد", key: "select_box", sortable: false, align: "center", width: "65px" },
  { title: "رقم الجلوس", key: "seat_number", sortable: true, align: "center", width: "115px" },
  { title: "اسم الطالب الرباعي", key: "student_name", sortable: true, align: "start" },
  { title: "المدرسة / المركز الامتحاني", key: "school_name", sortable: true, align: "start" },
  { title: "النموذج", key: "model_code", sortable: true, align: "center", width: "110px" },
  { title: "محتوى الحزمة", key: "package_contents", sortable: false, align: "center", width: "220px" },
  { title: "حالة الطباعة", key: "is_printed", sortable: true, align: "center", width: "130px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "180px" },
])

const packageTableItems = ref({
  results: [],
  count: 0,
  pagination: {
    count: 0,
    total: 0,
    num_pages: 1,
    current_page: 1,
  },
})

const filteredPackageStudents = computed(() => {
  if (!examDetails.value?.registered_students) return []
  let list = examDetails.value.registered_students
  if (packageModelFilter.value && packageModelFilter.value !== 'all') {
    list = list.filter(s => (s.model_code || 'A') === packageModelFilter.value)
  }
  if (packageSearch.value && packageSearch.value.trim()) {
    const q = packageSearch.value.trim().toLowerCase()
    list = list.filter(s =>
      String(s.seat_number || '').toLowerCase().includes(q) ||
      String(s.student_name || '').toLowerCase().includes(q) ||
      String(s.school_name || '').toLowerCase().includes(q)
    )
  }
  return list
})

const getPackageData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = p.page || 1
  const pageSize = p.page_size || 50
  const all = filteredPackageStudents.value || []
  const start = (page - 1) * pageSize
  packageTableItems.value = {
    results: all.slice(start, start + pageSize),
    count: all.length,
    pagination: {
      count: all.length,
      total: all.length,
      num_pages: Math.ceil(all.length / pageSize) || 1,
      current_page: page,
    },
  }
  return packageTableItems.value
}

watch(filteredPackageStudents, () => {
  getPackageData()
}, { immediate: true })

const togglePackageStudentSelection = (studentId) => {
  const idx = selectedPackageStudentIds.value.indexOf(studentId)
  if (idx > -1) {
    selectedPackageStudentIds.value.splice(idx, 1)
  } else {
    selectedPackageStudentIds.value.push(studentId)
  }
}

const openPreviewPackage = (student) => {
  previewPackageStudent.value = student
  previewPackageDialog.value = true
}

const printSingleStudentPackage = async (student) => {
  const vCode = student?.model_code || 'A'
  const verObj = examDetails.value?.versions?.find(ver => ver.versionCode === vCode) || examDetails.value?.versions?.[0]
  await printExamPackage({
    examTitle: customStageTitle.value || selectedExam.value?.title || 'اختبار الشهادة العامة',
    subjectName: selectedExam.value?.subject_name || 'الرياضيات',
    stageName: selectedExam.value?.stage_name || '',
    yearName: customExamYear.value || selectedExam.value?.year_name || '1446هـ - 2024-2025م',
    governorate: customGovernorate.value || selectedExam.value?.governorate || 'أمانة العاصمة',
    directorate: customDirectorate.value || selectedExam.value?.directorate || 'السبعين',
    centerName: customCenterName.value || student?.school_name || selectedExam.value?.directorate || 'المركز الاختباري الرئيسي',
    centerCode: student?.school_id || selectedExam.value?.id || '3026',
    versionCode: vCode,
    studentName: student?.student_name || '',
    seatNumber: student?.seat_number || '',
    secretNumber: student?.secret_number || '60',
    isA3: false,
    questions: verObj?.questions || [],
    omrElement: null,
    mode: 'package',
    isA5: selectedSheetLayout.value === 'compact_a5'
  })
}

const batchPrintSelectedPackages = async () => {
  printingPackages.value = true
  try {
    const targets = selectedPackageStudentIds.value.length > 0
      ? filteredPackageStudents.value.filter(s => selectedPackageStudentIds.value.includes(s.id))
      : filteredPackageStudents.value
    for (const st of targets) {
      await printSingleStudentPackage(st)
    }
  } finally {
    printingPackages.value = false
  }
}

const selectAllPackageStudents = () => {
  if (selectedPackageStudentIds.value.length === filteredPackageStudents.value.length) {
    selectedPackageStudentIds.value = []
  } else {
    selectedPackageStudentIds.value = filteredPackageStudents.value.map(s => s.id)
  }
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
  await Promise.all([
    loadSubjects(),
    loadMasterData(),
    fetchBatches(),
  ])

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
/* ── Custom Data Table Cell Width & Centering Fixes ── */
:deep(.custom-data-table td),
:deep(.custom-data-table .v-data-table__td) {
  max-width: none !important;
  white-space: normal !important;
  word-break: normal !important;
  overflow: visible !important;
  text-overflow: clip !important;
}

:deep(.custom-data-table th),
:deep(.custom-data-table .v-data-table__th) {
  white-space: nowrap !important;
}

:deep(.custom-data-table .class-numbering-child-2 th:nth-child(2)),
:deep(.custom-data-table .class-numbering-child-2 td:nth-child(2)),
:deep(.class-numbering-child-2 th:nth-child(2)),
:deep(.class-numbering-child-2 td:nth-child(2)) {
  width: 44px !important;
  min-width: 44px !important;
  max-width: 50px !important;
  text-align: center !important;
}

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
  border-color: rgba(var(--v-border-color), var(--v-border-opacity, 0.12)) !important;
  background-color: rgb(var(--v-theme-surface)) !important;
  transition: all 0.2s ease;
}

.exam-icon-badge {
  background-color: rgba(var(--v-theme-primary), 0.1) !important;
  border-color: rgba(var(--v-theme-primary), 0.2) !important;
}

.exam-code-tag {
  letter-spacing: 0.5px;
  font-size: 0.72rem !important;
  border-color: rgba(var(--v-border-color), var(--v-border-opacity, 0.12)) !important;
  background-color: rgba(var(--v-theme-surface), 0.8) !important;
  color: rgb(var(--v-theme-primary)) !important;
}

.exam-stat-chip {
  border-color: rgba(var(--v-border-color), var(--v-border-opacity, 0.12)) !important;
  background-color: rgba(var(--v-theme-surface), 0.8) !important;
  min-width: 110px;
}

.registry-nav-bar {
  direction: rtl;
}

.registry-nav-container {
  display: flex;
  align-items: center;
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity, 0.12));
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
  color: rgba(var(--v-theme-on-surface), 0.7);
  background: transparent;
  transition: all 0.2s ease;
  user-select: none;
  white-space: nowrap;
}

.registry-nav-item:hover {
  background: rgba(var(--v-theme-on-surface), 0.06);
  color: rgb(var(--v-theme-on-surface));
}

.registry-nav-item.is-active {
  background: rgba(var(--v-theme-primary), 0.12);
  color: rgb(var(--v-theme-primary));
  font-weight: 800;
  border: 1px solid rgba(var(--v-theme-primary), 0.25);
}

.registry-nav-item.is-active .nav-icon {
  color: rgb(var(--v-theme-primary));
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
