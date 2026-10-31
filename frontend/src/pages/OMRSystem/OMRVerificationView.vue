<template>
  <div class="qb-omr-verification pa-4 pa-md-6">

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 1. MASTER VIEW: الهيكل الإداري وسجل المطابقة والتحقق المركزي    -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <div v-if="currentView === 'master'" class="master-view-container">

      <!-- شريط التصفية الهيكلي الموحد بنمط students-master -->
      <filter-fields label="خيارات التصفية الأكاديمية والهرمية للتحقق والرقابة" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
        <v-row dense class="align-center">
          <!-- نوع المؤسسة التعليمية كفلتر منسدل أساسي -->
          <v-col cols="12" sm="6" :md="institutionType === 'school' ? 2 : 3">
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
              class="mb-3"
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
                class="mb-3"
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
                class="mb-3"
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

            <v-col cols="12" sm="6" md="3">
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
                class="mb-3"
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
                class="mb-3"
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
                multiple
                chips
                closable-chips
                density="compact"
                variant="outlined"
                rounded="lg"
                hide-details
                class="mb-3"
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
                class="mb-3"
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
                multiple
                chips
                closable-chips
                density="compact"
                variant="outlined"
                rounded="lg"
                hide-details
                class="mb-3"
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
                class="mb-3"
                prepend-inner-icon="mdi-book-education-outline"
                @update:model-value="onSubjectFilterChange"
              />
            </v-col>
          </template>

          <!-- فلتر حالة المطابقة والرقابة للاختبارات -->
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="masterFilterStatus"
              :items="masterStatusOptions"
              item-title="title"
              item-value="value"
              label="حالة المطابقة والرقابة"
              density="compact"
              variant="outlined"
              rounded="lg"
              hide-details
              class="mb-3"
              prepend-inner-icon="mdi-shield-search"
            />
          </v-col>

          <!-- أزرار الإجراءات -->
          <v-col cols="12" class="d-flex align-center justify-end gap-2 mb-3">
            <custom-btn
              type="show"
              label="تصفية النتائج"
              color="primary"
              icon="mdi-filter"
              class="font-weight-bold px-5"
              :loading="loadingMaster"
              :click="loadMasterData"
            />
            <custom-btn
              type="cancel_filter"
              :click="resetHierarchyFilters"
              variant="tonal"
              color="error"
              label="تفريغ الفلاتر"
              icon="mdi-filter-off"
              class="font-weight-bold"
            />
          </v-col>
        </v-row>
      </filter-fields>

      <!-- 2. المؤشرات الرقابية الإجمالية (فلاتر مربعات شفافة أنيقة - لون Teal موحد) -->
      <div class="d-flex align-center gap-2 flex-wrap pa-3 bg-surface border rounded-0 mb-6 elevation-1">
        <span class="text-caption font-weight-black text-medium-emphasis me-1">تصفية المؤشرات:</span>
        <v-chip
          v-for="chip in masterFilterChips"
          :key="chip.key"
          color="teal"
          :variant="masterActiveFilter === chip.key ? 'flat' : 'tonal'"
          size="small"
          rounded="lg"
          class="font-weight-bold cursor-pointer transition-all"
          :class="{ 'elevation-2 text-white font-weight-black': masterActiveFilter === chip.key }"
          @click="toggleMasterFilter(chip.key)"
        >
          <v-icon v-if="masterActiveFilter === chip.key" start size="14">mdi-check</v-icon>
          <span>{{ chip.label }}: {{ chip.countText }}</span>
        </v-chip>
        <v-btn
          v-if="masterActiveFilter !== 'all'"
          size="x-small"
          variant="text"
          color="teal"
          class="font-weight-bold ms-1"
          prepend-icon="mdi-close-circle"
          @click="toggleMasterFilter('all')"
        >
          إلغاء التصفية
        </v-btn>
      </div>

      <!-- 3. تبويبات الاستعراض الهيكلي (Master Tabs) -->
      <div class="main-card rounded-2xl overflow-hidden mb-6 elevation-1 bg-surface border">
        <div class="d-flex align-center flex-wrap gap-2 px-4 pt-3 border-b">
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
              الاختبارات المعتمدة للتحقق ({{ filteredMasterExamsTable.length }})
            </v-tab>
          </v-tabs>
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
            >
              <template v-slot:item-slot="{ item, key }">
                <template v-if="key === 'office_name'">
                  <div class="d-flex align-center py-2" style="min-width: 220px;">
                    <v-avatar color="primary" variant="tonal" size="36" class="me-3 rounded-lg flex-shrink-0">
                      <v-icon color="primary" size="20">mdi-office-building-outline</v-icon>
                    </v-avatar>
                    <div>
                      <div class="font-weight-bold text-subtitle-2 text-on-surface">{{ item.office_name }}</div>
                      <div class="text-caption text-medium-emphasis">{{ item.governorate_name }}</div>
                    </div>
                  </div>
                </template>

                <template v-else-if="key === 'total_students'">
                  <span class="font-weight-bold text-subtitle-2">{{ item.total_students ?? 0 }}</span>
                </template>

                <template v-else-if="key === 'printed_count'">
                  <v-chip size="small" color="secondary" variant="tonal" class="font-weight-bold">
                    {{ item.printed_count || 0 }} ورقة
                  </v-chip>
                </template>

                <template v-else-if="key === 'scanned_count'">
                  <v-chip size="small" color="teal" variant="tonal" class="font-weight-bold">
                    {{ item.scanned_count || 0 }} ورقة
                  </v-chip>
                </template>

                <template v-else-if="key === 'missing_count'">
                  <v-chip size="small" :color="(item.missing_count || 0) > 0 ? 'error' : 'success'" variant="flat" class="font-weight-bold">
                    {{ item.missing_count || 0 }} مفقود
                  </v-chip>
                </template>

                <template v-else-if="key === 'absent_count'">
                  <span class="font-weight-bold text-orange-darken-2">{{ item.absent_count || 0 }}</span>
                </template>

                <template v-else-if="key === 'completion_rate'">
                  <div class="d-flex align-center justify-center gap-2 px-1">
                    <v-progress-linear
                      :model-value="item.completion_rate || 0"
                      color="teal"
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
                      prepend-icon="mdi-map-marker-radius-outline"
                      @click="drillDownToDirectorates(item)"
                    >
                      المديريات
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </v-window-item>

          <!-- 2. تبويب إدارات التربية بالمديريات -->
          <v-window-item value="directorates" v-if="institutionType === 'school'">
            <custom-data-table
              :key="'dirs-tbl-' + filteredDirectoratesTable.length + '-' + normalizeIds(selectedDirectorateId).join('-')"
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
            >
              <template v-slot:item-slot="{ item, key }">
                <template v-if="key === 'name'">
                  <div class="d-flex align-center py-2" style="min-width: 220px;">
                    <v-avatar color="teal" variant="tonal" size="36" class="me-3 rounded-lg flex-shrink-0">
                      <v-icon color="teal" size="20">mdi-map-marker-radius-outline</v-icon>
                    </v-avatar>
                    <div>
                      <div class="font-weight-bold text-subtitle-2 text-on-surface">{{ item.name }}</div>
                      <div class="text-caption text-medium-emphasis">{{ item.office_name }}</div>
                    </div>
                  </div>
                </template>

                <template v-else-if="key === 'total_students'">
                  <span class="font-weight-bold text-subtitle-2">{{ item.total_students ?? 0 }}</span>
                </template>

                <template v-else-if="key === 'printed_count'">
                  <v-chip size="small" color="secondary" variant="tonal" class="font-weight-bold">
                    {{ item.printed_count || 0 }} ورقة
                  </v-chip>
                </template>

                <template v-else-if="key === 'scanned_count'">
                  <v-chip size="small" color="teal" variant="tonal" class="font-weight-bold">
                    {{ item.scanned_count || 0 }} ورقة
                  </v-chip>
                </template>

                <template v-else-if="key === 'missing_count'">
                  <v-chip size="small" :color="(item.missing_count || 0) > 0 ? 'error' : 'success'" variant="flat" class="font-weight-bold">
                    {{ item.missing_count || 0 }} مفقود
                  </v-chip>
                </template>

                <template v-else-if="key === 'absent_count'">
                  <span class="font-weight-bold text-orange-darken-2">{{ item.absent_count || 0 }}</span>
                </template>

                <template v-else-if="key === 'completion_rate'">
                  <div class="d-flex align-center justify-center gap-2 px-1">
                    <v-progress-linear
                      :model-value="item.completion_rate || 0"
                      color="teal"
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
                      @click="drillDownToSchools(item)"
                    >
                      المدارس
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </v-window-item>

          <!-- 3. تبويب المراكز الامتحانية والمدارس / الجامعات / المعاهد -->
          <v-window-item value="schools">
            <custom-data-table
              :key="'schools-tbl-' + filteredSchoolsTable.length + '-' + normalizeIds(selectedSchoolId).join('-')"
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
            >
              <template v-slot:item-slot="{ item, key }">
                <template v-if="key === 'name' || key === 'school_name'">
                  <div class="d-flex align-center py-2" style="min-width: 220px;">
                    <v-avatar color="indigo" variant="tonal" size="36" class="me-3 rounded-lg flex-shrink-0">
                      <v-icon color="indigo" size="20">mdi-school-outline</v-icon>
                    </v-avatar>
                    <div>
                      <div class="font-weight-bold text-subtitle-2 text-on-surface">{{ item.name || item.school_name }}</div>
                      <div class="text-caption text-medium-emphasis">{{ item.directorate_name }} - {{ item.governorate_name }}</div>
                    </div>
                  </div>
                </template>

                <template v-else-if="key === 'total_students'">
                  <span class="font-weight-bold text-subtitle-2">{{ item.total_students ?? 0 }}</span>
                </template>

                <template v-else-if="key === 'printed_count'">
                  <v-chip size="small" color="secondary" variant="tonal" class="font-weight-bold">
                    {{ item.printed_count || 0 }} ورقة
                  </v-chip>
                </template>

                <template v-else-if="key === 'scanned_count'">
                  <v-chip size="small" color="teal" variant="tonal" class="font-weight-bold">
                    {{ item.scanned_count || 0 }} ورقة
                  </v-chip>
                </template>

                <template v-else-if="key === 'missing_count'">
                  <v-chip size="small" :color="(item.missing_count || 0) > 0 ? 'error' : 'success'" variant="flat" class="font-weight-bold">
                    {{ item.missing_count || 0 }} مفقود
                  </v-chip>
                </template>

                <template v-else-if="key === 'absent_count'">
                  <span class="font-weight-bold text-orange-darken-2">{{ item.absent_count || 0 }}</span>
                </template>

                <template v-else-if="key === 'completion_rate'">
                  <div class="d-flex align-center justify-center gap-2 px-1">
                    <v-progress-linear
                      :model-value="item.completion_rate || 0"
                      color="teal"
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
                      color="indigo"
                      variant="flat"
                      rounded="lg"
                      class="font-weight-bold text-white"
                      prepend-icon="mdi-file-find-outline"
                      @click="drillDownToExams(item)"
                    >
                      الاختبارات
                    </v-btn>
                  </div>
                </template>
              </template>
            </custom-data-table>
          </v-window-item>

          <!-- 4. تبويب الاختبارات المعتمدة للتحقق -->
          <v-window-item value="exams">
            <custom-data-table
              :key="'exams-tbl-' + filteredMasterExamsTable.length"
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
            >
              <template v-slot:item-slot="{ item, key }">
                <template v-if="key === 'title' || key === 'exam_title'">
                  <div class="py-2" style="min-width: 220px;">
                    <div class="font-weight-bold text-subtitle-2 text-on-surface">{{ item.title }}</div>
                    <div class="d-flex align-center gap-2 mt-1">
                      <v-chip size="x-small" color="primary" variant="tonal" class="font-mono font-weight-bold">
                        {{ item.uniqueCode || item.code }}
                      </v-chip>
                      <span class="text-caption text-medium-emphasis">{{ item.subject_name }}</span>
                    </div>
                  </div>
                </template>

                <template v-else-if="key === 'total_students'">
                  <span class="font-weight-bold text-subtitle-2">{{ item.total_students || item.total_registered || 0 }}</span>
                </template>

                <template v-else-if="key === 'total_printed'">
                  <v-chip size="small" color="secondary" variant="tonal" class="font-weight-bold">
                    {{ item.total_printed || 0 }} ورقة
                  </v-chip>
                </template>

                <template v-else-if="key === 'total_scanned'">
                  <v-chip size="small" color="teal" variant="tonal" class="font-weight-bold">
                    {{ item.total_scanned || 0 }} ورقة
                  </v-chip>
                </template>

                <template v-else-if="key === 'missing_count'">
                  <v-chip size="small" :color="(item.missing_count || 0) > 0 ? 'error' : 'success'" variant="flat" class="font-weight-bold">
                    {{ item.missing_count || 0 }} مفقود
                  </v-chip>
                </template>

                <template v-else-if="key === 'status'">
                  <v-chip size="small" :color="item.status_color || 'primary'" variant="tonal" class="font-weight-bold">
                    {{ item.status }}
                  </v-chip>
                </template>

                <template v-else-if="key === 'pass_rate'">
                  <div class="d-flex align-center justify-center gap-1 font-weight-bold text-caption text-success">
                    <span>{{ item.pass_rate || 0 }}%</span>
                  </div>
                </template>

                <template v-else-if="key === 'actions'">
                  <div class="d-flex align-center justify-center gap-2">
                    <v-btn
                      size="small"
                      color="primary"
                      variant="flat"
                      rounded="lg"
                      class="font-weight-bold shadow-sm"
                      prepend-icon="mdi-shield-search"
                      @click="openExamVerificationDetail(item)"
                    >
                      كشف تدقيق الطلاب
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
    <!-- 2. DETAIL VIEW: كشف تدقيق ومطابقة أوراق الطلاب التفصيلي        -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <div v-else class="detail-view-container">

      <!-- شريط المسار والرجوع والعمليات -->
      <div class="main-card pa-4 rounded-2xl mb-4 bg-surface border elevation-1">
        <div class="d-flex align-center justify-space-between flex-wrap gap-3">
          <!-- زر العودة والمسار الأكاديمي -->
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
                {{ activeBreadcrumb.institution_type_name || (institutionType === 'university' ? 'التعليم الجامعي' : (institutionType === 'institute' ? 'التعليم الفني' : 'التعليم العام')) }}
              </span>
              <template v-if="activeBreadcrumb.office_name || selectedOfficeObj">
                <v-icon size="14">mdi-chevron-left</v-icon>
                <span class="text-primary font-weight-bold">{{ activeBreadcrumb.office_name || selectedOfficeObj?.office_name || selectedOfficeObj?.name_ar }}</span>
              </template>
              <template v-if="activeBreadcrumb.directorate_name || selectedDirectorateObj || (detailFilterDirectorate && detailFilterDirectorate !== 'all')">
                <v-icon size="14">mdi-chevron-left</v-icon>
                <span class="text-teal font-weight-bold">{{ (detailFilterDirectorate && detailFilterDirectorate !== 'all') ? detailFilterDirectorate : (selectedDirectorateObj?.name || selectedDirectorateObj?.name_ar || activeBreadcrumb.directorate_name) }}</span>
              </template>
              <template v-if="activeBreadcrumb.school_name || selectedSchoolObj || (detailFilterSchool && detailFilterSchool !== 'all')">
                <v-icon size="14">mdi-chevron-left</v-icon>
                <span class="text-indigo font-weight-bold">{{ (detailFilterSchool && detailFilterSchool !== 'all') ? detailFilterSchool : (selectedSchoolObj?.name || activeBreadcrumb.school_name || 'كافة المدارس والمراكز') }}</span>
              </template>
              <v-icon size="14">mdi-chevron-left</v-icon>
              <span class="text-primary font-weight-black">{{ activeBreadcrumb.exam_title || activeExam?.title }}</span>
            </div>
          </div>

          <!-- أزرار التصدير والطباعة والتحديث -->
          <div class="d-flex align-center gap-2 flex-wrap">
            <v-btn
              color="secondary"
              variant="tonal"
              size="small"
              rounded="lg"
              class="font-weight-bold"
              prepend-icon="mdi-refresh"
              :loading="loadingRecords"
              @click="refreshExamRoster"
            >
              تحديث الكشف
            </v-btn>

            <v-btn
              color="success"
              variant="flat"
              size="small"
              rounded="lg"
              class="font-weight-bold"
              prepend-icon="mdi-file-excel-outline"
              @click="exportAuditToExcel"
            >
              تصدير Excel
            </v-btn>

            <v-btn
              color="primary"
              variant="flat"
              size="small"
              rounded="lg"
              class="font-weight-bold"
              prepend-icon="mdi-printer-outline"
              @click="printAuditSheet"
            >
              طباعة كشف الرقابة
            </v-btn>
          </div>
        </div>
      </div>

      <!-- مؤشرات تدقيق ومطابقة أوراق الاختبار النشط كفلاتر مربعات شفافة موحدة بلون Teal -->
      <div class="d-flex align-center gap-2 flex-wrap pa-3 bg-surface border rounded-xl mb-4 elevation-1">
        <span class="text-caption font-weight-black text-medium-emphasis me-1">تصفية كشف الطلاب:</span>
        <v-chip
          v-for="chip in detailFilterChips"
          :key="chip.key"
          color="teal"
          :variant="detailActiveFilter === chip.key ? 'flat' : 'tonal'"
          size="small"
          rounded="lg"
          class="font-weight-bold cursor-pointer transition-all"
          :class="{ 'elevation-2 text-white font-weight-black': detailActiveFilter === chip.key }"
          @click="toggleDetailFilter(chip.key)"
        >
          <v-icon v-if="detailActiveFilter === chip.key" start size="14">mdi-check</v-icon>
          <span>{{ chip.label }}: {{ chip.countText }}</span>
        </v-chip>
        <v-btn
          v-if="detailActiveFilter !== 'all'"
          size="x-small"
          variant="text"
          color="teal"
          class="font-weight-bold ms-1"
          prepend-icon="mdi-close-circle"
          @click="toggleDetailFilter('all')"
        >
          إلغاء التصفية
        </v-btn>
      </div>

      <!-- شريط فلاتر التدقيق التفصيلي للطلاب -->
      <filter-fields label="خيارات تدقيق وتصفية كشف الطلاب" class="main-card border-0 pa-4 rounded-2xl mb-4 elevation-1">
        <v-row dense class="align-center">
          <!-- فلتر حالة المطابقة -->
          <v-col cols="12" sm="6" md="2">
            <v-select
              v-model="detailFilterStatus"
              :items="statusFilterOptions"
              item-title="title"
              item-value="value"
              label="حالة المطابقة"
              density="compact"
              variant="outlined"
              rounded="lg"
              hide-details
              class="mb-3"
              prepend-inner-icon="mdi-shield-search"
              @update:model-value="applyDetailFilters"
            />
          </v-col>

          <!-- فلتر الحضور والسلوك -->
          <v-col cols="12" sm="6" md="2">
            <v-select
              v-model="detailFilterAttendance"
              :items="attendanceFilterOptions"
              item-title="title"
              item-value="value"
              label="الحضور والسلوك"
              density="compact"
              variant="outlined"
              rounded="lg"
              hide-details
              class="mb-3"
              prepend-inner-icon="mdi-account-check-outline"
              @update:model-value="applyDetailFilters"
            />
          </v-col>

          <!-- فلتر النتيجة الأكاديمية -->
          <v-col cols="12" sm="6" md="2">
            <v-select
              v-model="detailFilterResult"
              :items="resultFilterOptions"
              item-title="title"
              item-value="value"
              label="النتيجة"
              density="compact"
              variant="outlined"
              rounded="lg"
              hide-details
              class="mb-3"
              prepend-inner-icon="mdi-medal-outline"
              @update:model-value="applyDetailFilters"
            />
          </v-col>

          <!-- فلتر النموذج -->
          <v-col cols="12" sm="6" md="2">
            <v-select
              v-model="detailFilterVersion"
              :items="['all', ...(activeExamFilterOptions.versions || [])]"
              label="النموذج"
              density="compact"
              variant="outlined"
              rounded="lg"
              hide-details
              class="mb-3"
              prepend-inner-icon="mdi-layers-outline"
              @update:model-value="applyDetailFilters"
            />
          </v-col>

          <!-- فلتر المديرية (إدارة التربية) -->
          <v-col cols="12" sm="6" md="2" v-if="institutionType === 'school'">
            <v-autocomplete
              v-model="detailFilterDirectorate"
              :items="detailDirectorateItems"
              item-title="title"
              item-value="value"
              label="المديرية"
              density="compact"
              variant="outlined"
              rounded="lg"
              hide-details
              clearable
              class="mb-3"
              prepend-inner-icon="mdi-map-marker-radius-outline"
              @update:model-value="onDetailDirectorateChange"
              @click:clear="clearDetailDirectorate"
            />
          </v-col>

          <!-- فلتر المدرسة / المركز -->
          <v-col cols="12" sm="6" md="2">
            <v-autocomplete
              v-model="detailFilterSchool"
              :items="detailSchoolItems"
              item-title="title"
              item-value="value"
              label="المدرسة / المركز"
              density="compact"
              variant="outlined"
              rounded="lg"
              hide-details
              clearable
              class="mb-3"
              prepend-inner-icon="mdi-school-outline"
              @update:model-value="applyDetailFilters"
              @click:clear="clearDetailSchool"
            />
          </v-col>

          <!-- بحث سريع برقم الجلوس أو اسم الطالب -->
          <v-col cols="12" sm="6" md="2">
            <v-text-field
              v-model="detailSearchQuery"
              label="رقم الجلوس أو الاسم"
              placeholder="ابحث..."
              prepend-inner-icon="mdi-magnify"
              density="compact"
              variant="outlined"
              rounded="lg"
              hide-details
              clearable
              class="mb-3"
              @keyup.enter="applyDetailFilters"
              @click:clear="clearDetailSearch"
            />
          </v-col>
        </v-row>
      </filter-fields>

      <!-- جدول تدقيق ومطابقة الطلاب التفصيلي -->
      <div class="main-card rounded-2xl overflow-hidden mb-6 elevation-1 bg-surface border">
        <custom-data-table
          :key="'student-roster-' + activeExam?.id + '-' + detailFilterStatus"
          v-model="selectedStudentRows"
          :items="studentTableItems"
          :getData="getStudentRosterData"
          :headers="studentAuditHeaders"
          :customLoading="loadingRecords"
          :hasFilter="false"
          :log="false"
          :restore="false"
          :numbering="true"
          :showSelect="true"
          :actions="false"
        >
          <template v-slot:item-slot="{ item, key }">
            <template v-if="key === 'seat_number'">
              <span class="font-weight-black font-mono text-subtitle-2">{{ item.seat_number }}</span>
            </template>

            <template v-else-if="key === 'secret_number'">
              <span class="font-mono text-caption font-weight-bold text-medium-emphasis">{{ item.secret_number || '—' }}</span>
            </template>

            <template v-else-if="key === 'student_name'">
              <div class="py-2" style="min-width: 180px;">
                <div class="font-weight-bold text-subtitle-2 text-on-surface">{{ item.student_name }}</div>
                <div class="text-caption text-medium-emphasis">{{ item.school_name }}</div>
              </div>
            </template>

            <template v-else-if="key === 'version_code'">
              <v-chip size="x-small" color="primary" variant="flat" class="font-weight-black font-mono">
                {{ item.version_code || 'A' }}
              </v-chip>
            </template>

            <template v-else-if="key === 'print_status'">
              <v-chip size="small" :color="item.is_printed ? 'secondary' : 'grey'" variant="tonal" class="font-weight-bold">
                {{ item.print_status_display || (item.is_printed ? (item.has_scanned ? 'طُبعت ومُسحت' : 'طُبعت') : 'لم تُطبع') }}
              </v-chip>
            </template>

            <template v-else-if="key === 'scan_status'">
              <div v-if="item.has_scanned">
                <v-chip v-if="item.scan_status === 'completed'" size="small" color="teal" variant="tonal" class="font-weight-bold">
                  ممسوحة ({{ Math.round((item.scan_confidence || 0.95) * 100) }}%)
                </v-chip>
                <v-chip v-else-if="item.scan_status === 'failed'" size="small" color="error" variant="flat" class="font-weight-bold">
                  فشل المسح
                </v-chip>
                <v-chip v-else size="small" color="warning" variant="flat" class="font-weight-bold">
                  يحتاج مراجعة
                </v-chip>
              </div>
              <v-chip v-else size="small" color="grey" variant="tonal" class="font-weight-bold">
                لم تُمسح
              </v-chip>
            </template>

            <template v-else-if="key === 'attendance_status'">
              <v-chip v-if="item.is_cheating" size="small" color="purple" variant="flat" class="font-weight-bold">
                غش / مخالفة
              </v-chip>
              <v-chip v-else-if="item.is_present" size="small" color="success" variant="tonal" class="font-weight-bold">
                حاضر
              </v-chip>
              <v-chip v-else size="small" color="orange-darken-2" variant="tonal" class="font-weight-bold">
                غائب
              </v-chip>
            </template>

            <template v-else-if="key === 'score'">
              <div v-if="item.has_scanned" class="font-weight-black text-subtitle-2 d-inline-flex align-center" dir="ltr">
                <span :class="item.result_status === 'passed' ? 'text-success' : 'text-error'">
                  {{ item.score }} / {{ item.max_score }}
                </span>
                <span class="text-caption text-medium-emphasis ms-1" dir="ltr">({{ item.percentage }}%)</span>
              </div>
              <span v-else class="text-caption text-medium-emphasis">غائب</span>
            </template>

            <template v-else-if="key === 'verdict'">
              <v-chip size="small" :color="item.verdict_color || 'primary'" variant="flat" class="font-weight-bold">
                {{ item.verdict_name_ar }}
              </v-chip>
            </template>

            <template v-else-if="key === 'actions'">
              <div class="d-flex align-center justify-center gap-1">
                <!-- زر معاينة الورقة الممسوحة -->
                <v-btn
                  v-if="item.has_scanned && (item.original_image || item.aligned_image)"
                  size="small"
                  color="teal"
                  variant="tonal"
                  rounded="lg"
                  icon="mdi-file-eye-outline"
                  title="معاينة ورقة الطالب الممسوحة"
                  @click="previewScannedSheet(item)"
                />
                <v-btn
                  size="small"
                  color="primary"
                  variant="tonal"
                  rounded="lg"
                  icon="mdi-information-outline"
                  title="تفاصيل الطالب"
                  @click="openStudentRecordDetails(item)"
                />
              </div>
            </template>
          </template>
        </custom-data-table>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 3. DIALOG: معاينة صورة ورقة الطالب الممسوحة والمحاذاة           -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <v-dialog v-model="imagePreviewDialog" max-width="900px" scrollable>
      <v-card class="rounded-2xl elevation-4 overflow-hidden">
        <v-card-title class="pa-4 border-b d-flex align-center justify-space-between bg-surface">
          <div class="d-flex align-center">
            <v-avatar color="teal" variant="tonal" size="40" class="me-3 rounded-xl">
              <v-icon size="22">mdi-file-eye-outline</v-icon>
            </v-avatar>
            <div>
              <div class="text-subtitle-1 font-weight-black">{{ previewStudent?.student_name }}</div>
              <div class="text-caption text-medium-emphasis">
                رقم الجلوس: <span class="font-mono font-weight-bold text-primary">{{ previewStudent?.seat_number }}</span> |
                النموذج: <span class="font-mono font-weight-bold">{{ previewStudent?.version_code }}</span> |
                الدرجة: <span class="font-weight-bold text-success" dir="ltr">{{ previewStudent?.score }} / {{ previewStudent?.max_score }}</span>
              </div>
            </div>
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" @click="imagePreviewDialog = false" />
        </v-card-title>

        <v-card-text class="pa-4 bg-grey-lighten-4 text-center">
          <div v-if="previewStudent?.original_image || previewStudent?.aligned_image" class="d-flex justify-center">
            <v-img
              :src="previewStudent?.aligned_image || previewStudent?.original_image"
              max-height="650"
              contain
              class="rounded-xl elevation-2 bg-white"
            >
              <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height">
                  <v-progress-circular indeterminate color="primary" />
                </div>
              </template>
            </v-img>
          </div>
          <div v-else class="py-12 text-medium-emphasis font-weight-bold">
            لا توجد صورة ممسوحة متاحة لهذه الورقة.
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 4. DIALOG: تفاصيل سجل الطالب الكامل                            -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <v-dialog v-model="studentDetailsDialog" max-width="600px">
      <v-card class="rounded-2xl elevation-4">
        <v-card-title class="pa-4 border-b d-flex align-center justify-space-between bg-surface">
          <span class="text-h6 font-weight-black">بطاقة تدقيق ورقة الطالب</span>
          <v-btn icon="mdi-close" variant="text" size="small" @click="studentDetailsDialog = false" />
        </v-card-title>
        <v-card-text class="pa-4">
          <v-list density="compact" class="bg-transparent">
            <v-list-item title="اسم الطالب" :subtitle="selectedStudentDetails?.student_name" />
            <v-list-item title="رقم الجلوس" :subtitle="selectedStudentDetails?.seat_number" />
            <v-list-item title="الرقم السري" :subtitle="selectedStudentDetails?.secret_number" />
            <v-list-item title="المدرسة / المركز" :subtitle="selectedStudentDetails?.school_name" />
            <v-list-item title="المديرية والمحافظة" :subtitle="`${selectedStudentDetails?.directorate_name || ''} - ${selectedStudentDetails?.governorate_name || ''}`" />
            <v-list-item title="كود النموذج" :subtitle="selectedStudentDetails?.version_code" />
            <v-list-item title="حالة الطباعة" :subtitle="selectedStudentDetails?.is_printed ? `طُبعت بتاريخ ${selectedStudentDetails?.printed_at} (دفعة: ${selectedStudentDetails?.print_batch})` : 'لم تُطبع'" />
            <v-list-item title="حالة المسح" :subtitle="selectedStudentDetails?.has_scanned ? `ممسوحة بنسبة ثقة ${Math.round((selectedStudentDetails?.scan_confidence || 0.95) * 100)}%` : 'لم تُمسح'" />
            <v-list-item title="حكم المطابقة" :subtitle="selectedStudentDetails?.verdict_name_ar" />
            <v-list-item v-if="selectedStudentDetails?.cheating_reason" title="ملاحظة الرقابة" :subtitle="selectedStudentDetails?.cheating_reason" class="text-error" />
          </v-list>
        </v-card-text>
      </v-card>
    </v-dialog>

  </div>
</template>

<script>
import { verificationAPI } from '@/services/omr/endpoints'
import api from '@/services/omr/client.js'

export default {
  name: 'OMRVerificationView',
  data() {
    return {
      currentView: 'master', // 'master' | 'detail'
      institutionType: 'school',
      masterTab: 'exams',

      // فلاتر الهيكل الإداري
      selectedOfficeId: null,
      selectedDirectorateId: null,
      selectedSchoolId: null,
      selectedSubjectId: null,

      allOfficesList: [],
      officesList: [],
      directoratesOptions: [],
      schoolsOptions: [],
      subjectsList: [],

      sectorOptions: [
        { title: 'التعليم العام (مدرسي)', value: 'school', icon: 'mdi-school' },
        { title: 'التعليم الجامعي (أكاديمي)', value: 'university', icon: 'mdi-domain' },
        { title: 'التعليم الفني والمهني (معاهد)', value: 'institute', icon: 'mdi-tools' },
      ],

      // جداول الـ Master
      loadingMaster: false,
      masterSearchQuery: '',
      masterActiveFilter: 'all',
      masterFilterStatus: 'all',
      masterStatusOptions: [
        { title: 'الكل (جميع الاختبارات)', value: 'all' },
        { title: 'مطابقة مكتملة وسليمة', value: 'verified' },
        { title: 'يوجد أوراق مفقودة', value: 'missing' },
        { title: 'يتطلب مراجعة أو فشل مسح', value: 'review' },
        { title: 'بانتظار المسح الضوئي', value: 'waiting_scan' },
        { title: 'بانتظار الطباعة', value: 'waiting_print' },
      ],
      activeBreadcrumb: {
        institution_type_name: 'التعليم العام',
        office_name: '',
        directorate_name: '',
        school_name: '',
        exam_title: '',
      },

      selectedOfficeMasterRows: [],
      selectedDirectorateMasterRows: [],
      selectedSchoolMasterRows: [],
      selectedExamMasterRows: [],

      masterOfficesData: [],
      masterDirectoratesData: [],
      masterSchoolsData: [],
      masterExamsData: [],

      globalStats: {
        total_students: 0,
        total_printed: 0,
        total_scanned: 0,
        total_missing: 0,
        total_needs_review: 0,
        total_failed_scan: 0,
        total_absent: 0,
        total_cheating: 0,
        total_passed: 0,
        overall_pass_rate: 0,
      },

      // أعمدة الـ Master
      officeMasterHeaders: [
        { title: 'مكتب التربية (المحافظة)', key: 'office_name', sortable: true },
        { title: 'إجمالي الطلاب', key: 'total_students', sortable: true, align: 'center', width: '130px' },
        { title: 'المطبوع', key: 'printed_count', sortable: true, align: 'center', width: '130px' },
        { title: 'الممسوح', key: 'scanned_count', sortable: true, align: 'center', width: '130px' },
        { title: 'المفقود', key: 'missing_count', sortable: true, align: 'center', width: '130px' },
        { title: 'الغياب', key: 'absent_count', sortable: true, align: 'center', width: '110px' },
        { title: 'نسبة الإنجاز', key: 'completion_rate', sortable: true, align: 'center', width: '140px' },
        { title: 'إجراءات', key: 'actions', sortable: false, align: 'center', width: '120px' },
      ],

      directorateMasterHeaders: [
        { title: 'إدارة التربية (المديرية)', key: 'name', sortable: true },
        { title: 'إجمالي الطلاب', key: 'total_students', sortable: true, align: 'center', width: '130px' },
        { title: 'المطبوع', key: 'printed_count', sortable: true, align: 'center', width: '130px' },
        { title: 'الممسوح', key: 'scanned_count', sortable: true, align: 'center', width: '130px' },
        { title: 'المفقود', key: 'missing_count', sortable: true, align: 'center', width: '130px' },
        { title: 'الغياب', key: 'absent_count', sortable: true, align: 'center', width: '110px' },
        { title: 'نسبة الإنجاز', key: 'completion_rate', sortable: true, align: 'center', width: '140px' },
        { title: 'إجراءات', key: 'actions', sortable: false, align: 'center', width: '120px' },
      ],

      schoolMasterHeaders: [
        { title: 'المدرسة / المركز الامتحاني', key: 'name', sortable: true },
        { title: 'إجمالي الطلاب', key: 'total_students', sortable: true, align: 'center', width: '130px' },
        { title: 'المطبوع', key: 'printed_count', sortable: true, align: 'center', width: '130px' },
        { title: 'الممسوح', key: 'scanned_count', sortable: true, align: 'center', width: '130px' },
        { title: 'المفقود', key: 'missing_count', sortable: true, align: 'center', width: '130px' },
        { title: 'الغياب', key: 'absent_count', sortable: true, align: 'center', width: '110px' },
        { title: 'نسبة الإنجاز', key: 'completion_rate', sortable: true, align: 'center', width: '140px' },
        { title: 'إجراءات', key: 'actions', sortable: false, align: 'center', width: '130px' },
      ],

      examMasterHeaders: [
        { title: 'الاختبار والمادة', key: 'title', sortable: true },
        { title: 'إجمالي الطلاب', key: 'total_students', sortable: true, align: 'center', width: '120px' },
        { title: 'المطبوع', key: 'total_printed', sortable: true, align: 'center', width: '130px' },
        { title: 'الممسوح', key: 'total_scanned', sortable: true, align: 'center', width: '130px' },
        { title: 'المفقود', key: 'missing_count', sortable: true, align: 'center', width: '130px' },
        { title: 'حالة المطابقة', key: 'status', sortable: true, align: 'center', width: '160px' },
        { title: 'نسبة النجاح', key: 'pass_rate', sortable: true, align: 'center', width: '110px' },
        { title: 'إجراءات', key: 'actions', sortable: false, align: 'center', width: '150px' },
      ],

      // ── بيانات كشف تدقيق الطلاب (Detail View) ──
      activeExam: null,
      loadingRecords: false,
      selectedStudentRows: [],

      detailActiveFilter: 'all',
      detailFilterStatus: 'all',
      detailFilterAttendance: 'all',
      detailFilterResult: 'all',
      detailFilterVersion: 'all',
      detailFilterDirectorate: 'all',
      detailFilterSchool: 'all',
      detailSearchQuery: '',

      statusFilterOptions: [
        { title: 'الكل (جميع الأوراق)', value: 'all' },
        { title: 'مطابقة سليمة وممسوحة', value: 'verified' },
        { title: 'أوراق مفقودة', value: 'missing' },
        { title: 'فشل المسح الضوئي', value: 'failed' },
        { title: 'يحتاج مراجعة وتدقيق', value: 'needs_review' },
        { title: 'لم تطبع بعد', value: 'not_printed' },
      ],

      attendanceFilterOptions: [
        { title: 'الكل (جميع الحالات)', value: 'all' },
        { title: 'حاضرون', value: 'present' },
        { title: 'غائبون', value: 'absent' },
        { title: 'حالات غش ومخالفات', value: 'cheating' },
      ],

      resultFilterOptions: [
        { title: 'الكل', value: 'all' },
        { title: 'ناجح', value: 'passed' },
        { title: 'راسب', value: 'failed' },
      ],

      activeExamStats: {
        total_students: 0,
        total_printed: 0,
        total_scanned: 0,
        missing_count: 0,
        failed_scan_count: 0,
        needs_review_count: 0,
        absent_count: 0,
        cheating_count: 0,
        passed_count: 0,
        failed_score_count: 0,
        pass_rate: 0,
      },

      activeExamFilterOptions: {
        schools: [],
        directorates: [],
        versions: [],
        grades: [],
      },

      studentAuditHeaders: [
        { title: 'رقم الجلوس', key: 'seat_number', sortable: true, align: 'center', width: '110px' },
        { title: 'الرقم السري', key: 'secret_number', sortable: true, align: 'center', width: '100px' },
        { title: 'اسم الطالب والمدرسة', key: 'student_name', sortable: true },
        { title: 'النموذج', key: 'version_code', sortable: true, align: 'center', width: '80px' },
        { title: 'حالة الطباعة', key: 'print_status', sortable: true, align: 'center', width: '140px' },
        { title: 'حالة المسح', key: 'scan_status', sortable: true, align: 'center', width: '150px' },
        { title: 'الحضور والسلوك', key: 'attendance_status', sortable: true, align: 'center', width: '130px' },
        { title: 'الدرجة والنسبة', key: 'score', sortable: true, align: 'center', width: '130px' },
        { title: 'حكم المطابقة', key: 'verdict', sortable: true, align: 'center', width: '150px' },
        { title: 'إجراءات', key: 'actions', sortable: false, align: 'center', width: '100px' },
      ],

      studentRecordsData: [],
      totalStudentsCount: 0,

      // Dialogs
      imagePreviewDialog: false,
      previewStudent: null,
      studentDetailsDialog: false,
      selectedStudentDetails: null,
    }
  },

  computed: {
    selectedOfficeObj() {
      const ids = this.normalizeIds(this.selectedOfficeId)
      if (!ids.length) return null
      return this.allOfficesList.find(o => ids.includes(o.id)) || null
    },

    selectedDirectorateObj() {
      const ids = this.normalizeIds(this.selectedDirectorateId)
      if (!ids.length) return null
      return this.directoratesOptions.find(d => ids.includes(d.id)) || null
    },

    selectedSchoolObj() {
      const ids = this.normalizeIds(this.selectedSchoolId)
      if (!ids.length) return null
      return this.schoolsOptions.find(s => ids.includes(s.id)) || null
    },

    masterFilterChips() {
      const g = this.globalStats || {}
      const reviewCnt = (g.total_failed_scan || 0) + (g.total_needs_review || 0)
      return [
        { key: 'all', label: 'المسجلين', countText: `${g.total_students || 0} طالب` },
        { key: 'printed', label: 'المطبوعة', countText: `${g.total_printed || 0} ورقة` },
        { key: 'scanned', label: 'الممسوحة', countText: `${g.total_scanned || 0} ورقة` },
        { key: 'missing', label: 'المفقودة', countText: `${g.total_missing || 0} ورقة` },
        { key: 'review', label: 'فشل/مراجعة', countText: `${reviewCnt} ورقة` },
        { key: 'absent', label: 'الغياب', countText: `${g.total_absent || 0} طالب` },
        { key: 'cheating', label: 'الغش', countText: `${g.total_cheating || 0} مخالفة` },
        { key: 'passed', label: 'النجاح', countText: `${g.overall_pass_rate || 0}% (${g.total_passed || 0} طالب)` },
      ]
    },

    detailFilterChips() {
      const s = this.activeExamStats || {}
      const reviewCnt = (s.failed_scan_count || 0) + (s.needs_review_count || 0)
      return [
        { key: 'all', label: 'المسجلين', countText: `${s.total_students || 0} طالب` },
        { key: 'printed', label: 'المطبوعة', countText: `${s.total_printed || 0} ورقة` },
        { key: 'scanned', label: 'الممسوحة', countText: `${s.total_scanned || 0} ورقة` },
        { key: 'missing', label: 'المفقودة', countText: `${s.missing_count || 0} ورقة` },
        { key: 'review', label: 'فشل/مراجعة', countText: `${reviewCnt} ورقة` },
        { key: 'absent', label: 'الغياب', countText: `${s.absent_count || 0} طالب` },
        { key: 'cheating', label: 'الغش', countText: `${s.cheating_count || 0} مخالفة` },
        { key: 'passed', label: 'النجاح', countText: `${s.pass_rate || 0}% (${s.passed_count || 0} طالب)` },
      ]
    },

    detailDirectorateItems() {
      const dirs = (this.activeExamFilterOptions?.directorates || [])
        .map(d => typeof d === 'string' ? d : (d.value !== 'all' ? (d.value || d.title) : null))
        .filter(d => d && d !== 'all')
      return [
        { title: 'كافة المديريات (الكل)', value: 'all' },
        ...dirs.map(d => ({ title: d, value: d }))
      ]
    },

    detailSchoolItems() {
      const schools = (this.activeExamFilterOptions?.schools || [])
        .map(s => typeof s === 'string' ? s : (s.value !== 'all' ? (s.value || s.title) : null))
        .filter(s => s && s !== 'all')
      return [
        { title: 'كافة المدارس والمراكز (الكل)', value: 'all' },
        ...schools.map(s => ({ title: s, value: s }))
      ]
    },

    filteredOfficesTable() {
      const q = (this.masterSearchQuery || '').trim().toLowerCase()
      let list = this.masterOfficesData || []

      if (this.masterActiveFilter && this.masterActiveFilter !== 'all') {
        if (this.masterActiveFilter === 'printed') list = list.filter(item => (item.printed_count || 0) > 0)
        else if (this.masterActiveFilter === 'scanned') list = list.filter(item => (item.scanned_count || 0) > 0)
        else if (this.masterActiveFilter === 'missing') list = list.filter(item => (item.missing_count || 0) > 0)
        else if (this.masterActiveFilter === 'review') list = list.filter(item => (item.needs_review_count || 0) > 0 || (item.failed_scan_count || 0) > 0)
        else if (this.masterActiveFilter === 'absent') list = list.filter(item => (item.absent_count || 0) > 0)
      }

      if (!q) return list
      return list.filter(item => 
        (item.office_name && item.office_name.toLowerCase().includes(q)) ||
        (item.governorate_name && item.governorate_name.toLowerCase().includes(q))
      )
    },

    filteredDirectoratesTable() {
      const q = (this.masterSearchQuery || '').trim().toLowerCase()
      let list = this.masterDirectoratesData || []

      if (this.masterActiveFilter && this.masterActiveFilter !== 'all') {
        if (this.masterActiveFilter === 'printed') list = list.filter(item => (item.printed_count || 0) > 0)
        else if (this.masterActiveFilter === 'scanned') list = list.filter(item => (item.scanned_count || 0) > 0)
        else if (this.masterActiveFilter === 'missing') list = list.filter(item => (item.missing_count || 0) > 0)
        else if (this.masterActiveFilter === 'review') list = list.filter(item => (item.needs_review_count || 0) > 0 || (item.failed_scan_count || 0) > 0)
        else if (this.masterActiveFilter === 'absent') list = list.filter(item => (item.absent_count || 0) > 0)
      }

      if (!q) return list
      return list.filter(item => 
        (item.name && item.name.toLowerCase().includes(q)) ||
        (item.office_name && item.office_name.toLowerCase().includes(q))
      )
    },

    filteredSchoolsTable() {
      const q = (this.masterSearchQuery || '').trim().toLowerCase()
      let list = this.masterSchoolsData || []

      if (this.masterActiveFilter && this.masterActiveFilter !== 'all') {
        if (this.masterActiveFilter === 'printed') list = list.filter(item => (item.printed_count || 0) > 0)
        else if (this.masterActiveFilter === 'scanned') list = list.filter(item => (item.scanned_count || 0) > 0)
        else if (this.masterActiveFilter === 'missing') list = list.filter(item => (item.missing_count || 0) > 0)
        else if (this.masterActiveFilter === 'review') list = list.filter(item => (item.needs_review_count || 0) > 0 || (item.failed_scan_count || 0) > 0)
        else if (this.masterActiveFilter === 'absent') list = list.filter(item => (item.absent_count || 0) > 0)
      }

      if (!q) return list
      return list.filter(item => 
        (item.name && item.name.toLowerCase().includes(q)) ||
        (item.directorate_name && item.directorate_name.toLowerCase().includes(q))
      )
    },

    filteredMasterExamsTable() {
      const q = (this.masterSearchQuery || '').trim().toLowerCase()
      let list = this.masterExamsData || []

      if (this.masterActiveFilter && this.masterActiveFilter !== 'all') {
        if (this.masterActiveFilter === 'printed') {
          list = list.filter(e => (e.total_printed || 0) > 0)
        } else if (this.masterActiveFilter === 'scanned') {
          list = list.filter(e => (e.total_scanned || 0) > 0)
        } else if (this.masterActiveFilter === 'missing') {
          list = list.filter(e => (e.missing_count || 0) > 0)
        } else if (this.masterActiveFilter === 'review') {
          list = list.filter(e => (e.failed_scan_count || 0) > 0 || (e.needs_review_count || 0) > 0)
        } else if (this.masterActiveFilter === 'absent') {
          list = list.filter(e => (e.absent_count || 0) > 0)
        } else if (this.masterActiveFilter === 'cheating') {
          list = list.filter(e => (e.cheating_count || 0) > 0)
        } else if (this.masterActiveFilter === 'passed') {
          list = list.filter(e => (e.pass_rate || 0) >= 50 || (e.passed_count || 0) > 0)
        }
      }

      if (this.masterFilterStatus && this.masterFilterStatus !== 'all') {
        if (this.masterFilterStatus === 'verified') {
          list = list.filter(e => (e.missing_count || 0) === 0 && (e.total_scanned || 0) > 0 && (e.failed_scan_count || 0) === 0 && (e.needs_review_count || 0) === 0)
        } else if (this.masterFilterStatus === 'missing') {
          list = list.filter(e => (e.missing_count || 0) > 0)
        } else if (this.masterFilterStatus === 'review') {
          list = list.filter(e => (e.failed_scan_count || 0) > 0 || (e.needs_review_count || 0) > 0)
        } else if (this.masterFilterStatus === 'waiting_scan') {
          list = list.filter(e => (e.total_printed || 0) > 0 && (e.total_scanned || 0) === 0)
        } else if (this.masterFilterStatus === 'waiting_print') {
          list = list.filter(e => (e.total_printed || 0) === 0)
        }
      }

      if (!q) return list
      return list.filter(item => 
        (item.title && item.title.toLowerCase().includes(q)) ||
        (item.uniqueCode && item.uniqueCode.toLowerCase().includes(q)) ||
        (item.subject_name && item.subject_name.toLowerCase().includes(q))
      )
    },

    officeMasterTableItems() {
      const all = this.filteredOfficesTable || []
      return {
        results: all,
        count: all.length,
        pagination: { count: all.length, total: all.length, num_pages: 1, current_page: 1 }
      }
    },

    directorateMasterTableItems() {
      const all = this.filteredDirectoratesTable || []
      return {
        results: all,
        count: all.length,
        pagination: { count: all.length, total: all.length, num_pages: 1, current_page: 1 }
      }
    },

    schoolMasterTableItems() {
      const all = this.filteredSchoolsTable || []
      return {
        results: all,
        count: all.length,
        pagination: { count: all.length, total: all.length, num_pages: 1, current_page: 1 }
      }
    },

    examMasterTableItems() {
      const all = this.filteredMasterExamsTable || []
      return {
        results: all,
        count: all.length,
        pagination: { count: all.length, total: all.length, num_pages: 1, current_page: 1 }
      }
    },

    studentTableItems() {
      const all = this.studentRecordsData || []
      return {
        results: all,
        count: this.totalStudentsCount || all.length,
        pagination: { count: this.totalStudentsCount || all.length, total: this.totalStudentsCount || all.length, num_pages: 1, current_page: 1 }
      }
    },
  },

  mounted() {
    this.loadMasterData()
  },

  methods: {
    normalizeIds(val) {
      if (!val) return []
      if (Array.isArray(val)) return val.filter(Boolean)
      if (typeof val === 'string') return val.split(',').map(s => s.trim()).filter(Boolean)
      return [val]
    },

    onSectorChange() {
      this.selectedOfficeId = null
      this.selectedDirectorateId = null
      this.selectedSchoolId = null
      this.selectedSubjectId = null
      this.loadMasterData()
    },

    onOfficeFilterChange() {
      this.selectedDirectorateId = null
      this.selectedSchoolId = null
      this.loadMasterData()
    },

    onDirectorateFilterChange() {
      this.selectedSchoolId = null
      this.loadMasterData()
    },

    onSchoolFilterChange() {
      this.loadMasterData()
    },

    onSubjectFilterChange() {
      this.loadMasterData()
    },

    toggleMasterFilter(key) {
      if (this.masterActiveFilter === key) {
        this.masterActiveFilter = 'all'
      } else {
        this.masterActiveFilter = key
      }
    },

    toggleDetailFilter(key) {
      if (this.detailActiveFilter === key) {
        this.detailActiveFilter = 'all'
      } else {
        this.detailActiveFilter = key
      }

      this.detailFilterStatus = 'all'
      this.detailFilterAttendance = 'all'
      this.detailFilterResult = 'all'

      if (this.detailActiveFilter === 'printed') {
        this.detailFilterStatus = 'printed'
      } else if (this.detailActiveFilter === 'scanned') {
        this.detailFilterStatus = 'scanned'
      } else if (this.detailActiveFilter === 'missing') {
        this.detailFilterStatus = 'missing'
      } else if (this.detailActiveFilter === 'review') {
        this.detailFilterStatus = 'review'
      } else if (this.detailActiveFilter === 'absent') {
        this.detailFilterAttendance = 'absent'
      } else if (this.detailActiveFilter === 'cheating') {
        this.detailFilterAttendance = 'cheating'
      } else if (this.detailActiveFilter === 'passed') {
        this.detailFilterResult = 'passed'
      }

      this.applyDetailFilters()
    },

    resetHierarchyFilters() {
      this.selectedOfficeId = null
      this.selectedDirectorateId = null
      this.selectedSchoolId = null
      this.selectedSubjectId = null
      this.masterActiveFilter = 'all'
      this.masterFilterStatus = 'all'
      this.masterSearchQuery = ''
      this.loadMasterData()
    },

    async loadMasterData() {
      this.loadingMaster = true
      try {
        const officeIds = this.normalizeIds(this.selectedOfficeId)
        const dirIds = this.normalizeIds(this.selectedDirectorateId)
        const schoolIds = this.normalizeIds(this.selectedSchoolId)

        const baseParams = {
          institution_type: this.institutionType
        }
        if (officeIds.length) baseParams.office_id = officeIds.join(',')
        if (dirIds.length) baseParams.directorate_id = dirIds.join(',')
        if (schoolIds.length) baseParams.school_id = schoolIds.join(',')
        if (this.selectedSubjectId) baseParams.subject_id = this.selectedSubjectId

        // جلب البيانات الهرمية بالتوازي
        const [officesRes, dirsRes, schoolsRes, examsRes, subjectsRes] = await Promise.all([
          verificationAPI.getByOffice(baseParams).catch(() => ({ data: { results: [] } })),
          verificationAPI.getByDirectorate(baseParams).catch(() => ({ data: { results: [] } })),
          verificationAPI.getBySchool(baseParams).catch(() => ({ data: { results: [] } })),
          verificationAPI.list(baseParams).catch(() => ({ data: { results: [], global_stats: {} } })),
          verificationAPI.getSubjects({ institution_type: this.institutionType }).catch(() => ({ data: { results: [] } })),
        ])

        this.masterOfficesData = officesRes.data?.results || []
        if (!this.allOfficesList.length && this.masterOfficesData.length) {
          this.allOfficesList = this.masterOfficesData
        }
        this.officesList = this.masterOfficesData

        this.masterDirectoratesData = dirsRes.data?.results || []
        this.directoratesOptions = this.masterDirectoratesData

        this.masterSchoolsData = schoolsRes.data?.results || []
        this.schoolsOptions = this.masterSchoolsData

        this.masterExamsData = examsRes.data?.results || []
        if (examsRes.data?.global_stats) {
          this.globalStats = examsRes.data.global_stats
        }

        this.subjectsList = subjectsRes.data?.results || []
      } catch (err) {
        console.error('Error loading verification master data:', err)
      } finally {
        this.loadingMaster = false
      }
    },

    getOfficeMasterData() { return this.officeMasterTableItems },
    getDirectorateMasterData() { return this.directorateMasterTableItems },
    getSchoolMasterData() { return this.schoolMasterTableItems },
    getExamMasterData() { return this.examMasterTableItems },

    drillDownToDirectorates(office) {
      if (office && office.id) {
        this.selectedOfficeId = [office.id]
        this.masterTab = 'directorates'
        this.loadMasterData()
      }
    },

    drillDownToSchools(dir) {
      if (dir && dir.id) {
        this.selectedDirectorateId = [dir.id]
        this.masterTab = 'schools'
        this.loadMasterData()
      }
    },

    drillDownToExams(school) {
      if (school && school.id) {
        this.selectedSchoolId = [school.id]
        this.masterTab = 'exams'
        this.loadMasterData()
      }
    },

    openExamVerificationDetail(exam) {
      this.activeExam = exam
      this.currentView = 'detail'
      this.detailActiveFilter = 'all'
      this.detailFilterStatus = 'all'
      this.detailFilterAttendance = 'all'
      this.detailFilterResult = 'all'
      this.detailFilterVersion = 'all'

      // فتح الشاشة التفصيلية بكافة المديريات والمدارس لتصفية حرة وشاملة
      this.detailFilterDirectorate = 'all'
      this.detailFilterSchool = 'all'
      this.detailSearchQuery = ''

      this.activeBreadcrumb = {
        institution_type_name: this.institutionType === 'university' ? 'التعليم الجامعي' : (this.institutionType === 'institute' ? 'التعليم الفني' : 'التعليم العام'),
        office_name: this.selectedOfficeObj?.office_name || (exam.governorate_name ? `مكتب التربية والتعليم - ${exam.governorate_name}` : 'كافة مكاتب التربية'),
        directorate_name: 'كافة المديريات',
        school_name: exam.school_name || 'كافة المدارس والمراكز',
        exam_title: exam.title || '',
      }
      this.fetchExamStudentRoster({ page: 1 })
    },

    returnToMaster() {
      this.currentView = 'master'
      this.loadMasterData()
    },

    onDetailDirectorateChange() {
      this.applyDetailFilters()
    },

    clearDetailDirectorate() {
      this.detailFilterDirectorate = 'all'
      this.applyDetailFilters()
    },

    clearDetailSchool() {
      this.detailFilterSchool = 'all'
      this.applyDetailFilters()
    },

    applyDetailFilters() {
      this.fetchExamStudentRoster({ page: 1 })
    },

    clearDetailSearch() {
      this.detailSearchQuery = ''
      this.fetchExamStudentRoster({ page: 1 })
    },

    refreshExamRoster() {
      this.fetchExamStudentRoster({ page: 1 })
    },

    async fetchExamStudentRoster(params = {}) {
      if (!this.activeExam || !this.activeExam.id) return
      this.loadingRecords = true
      try {
        const queryParams = {
          page: params.page || 1,
          page_size: params.page_size || 50,
        }
        if (this.detailFilterStatus && this.detailFilterStatus !== 'all') {
          queryParams.status = this.detailFilterStatus
        }
        if (this.detailFilterAttendance && this.detailFilterAttendance !== 'all') {
          queryParams.attendance = this.detailFilterAttendance
        }
        if (this.detailFilterResult && this.detailFilterResult !== 'all') {
          queryParams.result = this.detailFilterResult
        }
        if (this.detailFilterVersion && this.detailFilterVersion !== 'all') {
          queryParams.version = this.detailFilterVersion
        }
        if (this.detailFilterDirectorate && this.detailFilterDirectorate !== 'all') {
          queryParams.directorate = this.detailFilterDirectorate
        }
        if (this.detailFilterSchool && this.detailFilterSchool !== 'all') {
          queryParams.school = this.detailFilterSchool
        }

        if (this.detailSearchQuery && this.detailSearchQuery.trim()) {
          queryParams.search = this.detailSearchQuery.trim()
        }

        const res = await verificationAPI.getRoster(this.activeExam.id, queryParams)
        const data = res.data || {}

        this.studentRecordsData = data.results || data.students || []
        this.totalStudentsCount = data.count || this.studentRecordsData.length

        if (data.breadcrumb) {
          const currentSchool = (this.detailFilterSchool && this.detailFilterSchool !== 'all') 
            ? this.detailFilterSchool 
            : (this.selectedSchoolObj?.name || data.breadcrumb.school_name || 'كافة المدارس والمراكز')

          this.activeBreadcrumb = {
            ...data.breadcrumb,
            school_name: currentSchool,
            directorate_name: this.selectedDirectorateObj?.name || data.breadcrumb.directorate_name || 'كافة المديريات',
            office_name: this.selectedOfficeObj?.office_name || data.breadcrumb.office_name || 'كافة مكاتب التربية'
          }
        }
        if (data.stats) {
          this.activeExamStats = data.stats
        }
        if (data.filter_options) {
          this.activeExamFilterOptions = data.filter_options
        }
      } catch (err) {
        console.error('Error fetching exam student roster:', err)
      } finally {
        this.loadingRecords = false
      }
    },

    getStudentRosterData(params) {
      return this.fetchExamStudentRoster(params?.params || params)
    },

    previewScannedSheet(item) {
      this.previewStudent = item
      this.imagePreviewDialog = true
    },

    openStudentRecordDetails(item) {
      this.selectedStudentDetails = item
      this.studentDetailsDialog = true
    },

    exportAuditToExcel() {
      if (!this.studentRecordsData.length) return
      let csvContent = 'data:text/csv;charset=utf-8,\uFEFF'
      csvContent += 'رقم الجلوس,الرقم السري,اسم الطالب,المدرسة,المديرية,النموذج,حالة الطباعة,حالة المسح,الحضور,الدرجة,النسبة %,حكم المطابقة\n'

      this.studentRecordsData.forEach(s => {
        const row = [
          `"${s.seat_number || ''}"`,
          `"${s.secret_number || ''}"`,
          `"${s.student_name || ''}"`,
          `"${s.school_name || ''}"`,
          `"${s.directorate_name || ''}"`,
          `"${s.version_code || 'A'}"`,
          `"${s.is_printed ? 'طُبعت' : 'لم تُطبع'}"`,
          `"${s.has_scanned ? 'ممسوحة' : 'لم تُمسح'}"`,
          `"${s.is_cheating ? 'غش/مخالفة' : (s.is_present ? 'حاضر' : 'غائب')}"`,
          `"${s.score || 0}"`,
          `"${s.percentage || 0}%"`,
          `"${s.verdict_name_ar || ''}"`
        ]
        csvContent += row.join(',') + '\n'
      })

      const encodedUri = encodeURI(csvContent)
      const link = document.createElement('a')
      link.setAttribute('href', encodedUri)
      link.setAttribute('download', `كشف_مطابقة_${this.activeExam?.title || 'الاختبار'}.csv`)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },

    printAuditSheet() {
      window.print()
    },
  }
}
</script>

<style scoped>
.qb-omr-verification {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

.main-card {
  transition: all 0.2s ease;
}

.border-error {
  border-color: rgba(var(--v-theme-error), 0.4) !important;
}

@media print {
  .v-btn, .v-tabs, .filter-fields, .v-dialog {
    display: none !important;
  }
}
</style>
