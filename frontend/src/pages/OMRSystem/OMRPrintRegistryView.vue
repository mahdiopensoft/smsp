<template>
  <div class="qb-omr-print-registry pa-4 pa-md-6">

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 1. MASTER VIEW: الهيكل الإداري وسجل الطباعة المركزي             -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <div v-if="currentView === 'master'" class="master-view-container">
      <!-- شريط التصفية الهيكلي الموحد بنمط students-master القياسي -->
      <filter-fields label="خيارات التصفية الأكاديمية والبحث المتقدم في سجلات الطباعة والتوليد" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
        <v-row dense class="align-center">
          <!-- 1. نوع المؤسسة التعليمية (حقل واحد قياسي موحد بنمط students-master) -->
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterInstitutionType"
              name="InstitutionType"
              placeholder="نوع المؤسسة التعليمية"
              label="نوع المؤسسة التعليمية"
              cols="12"
              :add="false"
              @update:model-value="onInstitutionTypeChange"
            />
          </v-col>

          <!-- 2. حقل البحث الفوري الموحد -->
          <v-col cols="12" sm="6" md="3">
            <custom-text-field
              v-model="masterSearchQuery"
              label="اسم الاختبار أو الرمز"
              placeholder="بحث باسم الاختبار، الرمز (Code)..."
              icon="magnify"
              cols="12"
              class="mb-3"
              :hideDetails="true"
            />
          </v-col>

          <!-- 3. المحافظة -->
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterGovernorate"
              name="Governorate"
              placeholder="المحافظة"
              label="المحافظة"
              cols="12"
              :add="false"
              @update:model-value="onGovernorateChange"
            />
          </v-col>

          <!-- 4. المديرية (تظهر للمدارس) -->
          <v-col v-if="isSchoolFilter" cols="12" sm="6" md="3">
            <auto-list
              v-model="filterDirectorate"
              name="Directorate"
              :param="filterGovernorate"
              :placeholder="filterGovernorate ? 'المديرية' : 'اختر المحافظة أولاً'"
              label="المديرية"
              cols="12"
              :add="false"
              :disabled="!filterGovernorate"
              @update:model-value="onDirectorateChange"
            />
          </v-col>

          <!-- 5. المركز الامتحاني / المدرسة -->
          <v-col cols="12" sm="6" :md="isSchoolFilter ? 3 : 3">
            <auto-list
              v-model="filterOrganization"
              name="Organization"
              :param="orgParam"
              :placeholder="orgPlaceholder"
              :label="orgFieldLabel"
              cols="12"
              :add="false"
              :disabled="isOrgDisabled"
              @update:model-value="onOrganizationChange"
            />
          </v-col>

          <!-- 🏫 School Filters (المرحلة، الصف والمسار، المادة) -->
          <template v-if="filterInstitutionType === 'school'">
            <v-col cols="12" sm="6" md="3">
              <auto-list
                v-model="filterStage"
                name="Stage"
                label="المرحلة الدراسية"
                placeholder="المرحلة الدراسية"
                cols="12"
                :add="false"
                @update:model-value="onStageChange"
              />
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <auto-list
                v-model="filterClassTrack"
                name="ClassTrackByStage"
                :param="filterStage"
                label="الصف والمسار المدرسي"
                placeholder="الصف والمسار المدرسي"
                cols="12"
                :add="false"
                :disabled="!filterStage"
                @update:model-value="onClassTrackChange"
              />
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <auto-list
                v-model="filterSubject"
                name="Subject"
                :param="subjectFilterParam"
                label="المادة الدراسية"
                placeholder="المادة الدراسية"
                cols="12"
                :add="false"
                @update:model-value="loadMasterData"
              />
            </v-col>
          </template>

          <!-- 🎓 University Filters (الكلية، القسم، التخصص، المقرر) -->
          <template v-if="filterInstitutionType === 'university'">
            <v-col cols="12" sm="6" md="3">
              <auto-list
                v-model="filterCollege"
                name="College"
                label="الكلية الجامعية"
                placeholder="الكلية الجامعية"
                cols="12"
                :add="false"
                @update:model-value="onCollegeChange"
              />
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <auto-list
                v-model="filterDepartment"
                name="DepartmentByCollege"
                :param="filterCollege"
                label="القسم الأكاديمي"
                placeholder="القسم الأكاديمي"
                cols="12"
                :add="false"
                :disabled="!filterCollege"
                @update:model-value="onDepartmentChange"
              />
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <auto-list
                v-model="filterSpecialization"
                name="Specialization"
                :param="filterDepartment"
                label="التخصص والبرنامج"
                placeholder="التخصص والبرنامج"
                cols="12"
                :add="false"
                :disabled="!filterDepartment"
                @update:model-value="onSpecializationChange"
              />
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <auto-list
                v-model="filterSemesterSubject"
                name="SemesterSubject"
                :param="filterSpecialization"
                label="مقرر الفصل الجامعي"
                placeholder="مقرر الفصل الجامعي"
                cols="12"
                :add="false"
                @update:model-value="loadMasterData"
              />
            </v-col>
          </template>

          <!-- 🏢 Institute Filters (المجال المهني، نظام التعليم، التخصص، المادة) -->
          <template v-if="filterInstitutionType === 'institute'">
            <v-col cols="12" sm="6" md="3">
              <auto-list
                v-model="filterInstituteField"
                name="InstituteField"
                label="المجال المهني / التقني"
                placeholder="المجال المهني / التقني"
                cols="12"
                :add="false"
                @update:model-value="onInstituteFieldChange"
              />
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <auto-list
                v-model="filterInstituteEducationSystem"
                name="InstituteEducationSystem"
                :param="filterInstituteField"
                label="نظام التعليم والتدريب"
                placeholder="نظام التعليم والتدريب"
                cols="12"
                :add="false"
                :disabled="!filterInstituteField"
                @update:model-value="onInstituteEducationSystemChange"
              />
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <auto-list
                v-model="filterInstituteSpecialization"
                name="InstituteSpecialization"
                :param="instituteSpecParam"
                label="التخصص المهني"
                placeholder="التخصص المهني"
                cols="12"
                :add="false"
                :disabled="!filterInstituteEducationSystem"
                @update:model-value="loadMasterData"
              />
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <auto-list
                v-model="filterInstituteSubject"
                name="InstituteSubject"
                :param="instituteSubjectParam"
                label="المادة الدراسية للمعهد"
                placeholder="المادة الدراسية للمعهد"
                cols="12"
                :add="false"
                @update:model-value="loadMasterData"
              />
            </v-col>
          </template>

          <!-- Fallback Subject if All / None selected -->
          <v-col v-if="!filterInstitutionType || filterInstitutionType === 'all'" cols="12" sm="6" md="3">
            <auto-list
              v-model="filterSubject"
              name="Subject"
              placeholder="المادة الدراسية (عام)"
              label="المادة الدراسية (عام)"
              cols="12"
              :add="false"
              @update:model-value="loadMasterData"
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
              :click="resetUnifiedFilters"
              variant="tonal"
              color="error"
              label="تفريغ الفلاتر"
              icon="mdi-filter-off"
              class="font-weight-bold"
            />
          </v-col>
        </v-row>
      </filter-fields>

      <!-- 4. تبويبات الاستعراض الهيكلي وسجل الطباعة المركزي (Master Tabs) -->
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
              الاختبارات المعتمدة للطباعة ({{ filteredMasterExamsTable.length }})
            </v-tab>
            <v-tab value="registry" class="font-weight-bold">
              <v-icon start size="18">mdi-history</v-icon>
              سجل الدفعات المطبوعة ({{ filteredBatchesTable.length }})
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

          <!-- 4. تبويب الاختبارات المعتمدة للطباعة (مع التبويبات الفرعية الثلاثة) -->
          <v-window-item value="exams">
            <!-- ── شريط التبويبات الفرعية الأربعة: الطلبات / المجدولة / المستحقة / المكتملة ── -->
            <div class="d-flex align-center justify-space-between flex-wrap gap-2 px-4 py-2 border-b bg-surface-variant-subtle">
              <v-tabs
                v-model="examSubTab"
                color="primary"
                density="compact"
                class="sub-stage-tabs"
              >
                <!-- 1. الطلبات (الطلبات الجارية وغير المكتملة) -->
                <v-tab value="orders" class="font-weight-bold">
                  <v-icon start size="18" color="primary">mdi-format-list-bulleted</v-icon>
                  الطلبات ({{ pendingAndActiveOrdersCount }})
                </v-tab>

                <!-- 2. المجدولة (المستقبلية) -->
                <v-tab value="scheduled" class="font-weight-bold">
                  <v-icon start size="18" color="info">mdi-calendar-clock</v-icon>
                  المجدولة ({{ scheduledExamsCount }})
                </v-tab>

                <!-- 3. المستحقة (قائمة انتظار الطباعة الجاهزة للتنفيذ) -->
                <v-tab value="due" class="font-weight-bold">
                  <v-icon start size="18" color="warning">mdi-clock-alert-outline</v-icon>
                  المستحقة ({{ dueExamsCount }})
                </v-tab>

                <!-- 4. المكتملة (الاختبارات التي تم سحب وثائقها بالكامل) -->
                <v-tab value="completed" class="font-weight-bold">
                  <v-icon start size="18" color="primary">mdi-check-decagram</v-icon>
                  المكتملة ({{ completedExamsCount }})
                </v-tab>

                <!-- 5. الملغية (أوامر ملغاة رسمياً من الكنترول) -->
                <v-tab value="cancelled" class="font-weight-bold">
                  <v-icon start size="18" color="secondary">mdi-cancel</v-icon>
                  الملغية ({{ cancelledExamsCount }})
                </v-tab>

                <!-- 6. السجل الشامل (كافة الاختبارات لكافة الحالات) -->
                <v-tab value="all" class="font-weight-bold">
                  <v-icon start size="18" color="medium-emphasis">mdi-archive-outline</v-icon>
                  السجل الشامل ({{ allExamsCount }})
                </v-tab>
              </v-tabs>

              <div class="d-flex align-center gap-2">
                <div style="min-width: 240px; max-width: 300px;">
                  <custom-text-field
                    v-model="masterSearchQuery"
                    placeholder="بحث برمز أو اسم الاختبار أو رقم الطلب..."
                    icon="magnify"
                    cols="12"
                    :hideDetails="true"
                  />
                </div>
                <v-chip
                  size="small"
                  variant="tonal"
                  :color="examSubTab === 'due' ? 'warning' : (examSubTab === 'scheduled' ? 'info' : (examSubTab === 'cancelled' ? 'secondary' : (examSubTab === 'all' ? 'default' : 'primary')))"
                  class="font-weight-medium"
                >
                  <v-icon start size="14">
                    {{ examSubTab === 'due' ? 'mdi-clock-fast' : (examSubTab === 'scheduled' ? 'mdi-calendar-range' : (examSubTab === 'completed' ? 'mdi-check-all' : (examSubTab === 'cancelled' ? 'mdi-cancel' : (examSubTab === 'all' ? 'mdi-archive-outline' : 'mdi-file-document-multiple-outline')))) }}
                  </v-icon>
                  {{ examSubTab === 'due' ? 'المستحقة للتنفيذ' : (examSubTab === 'scheduled' ? 'أوامر مجدولة' : (examSubTab === 'completed' ? 'مكتملة 100%' : (examSubTab === 'cancelled' ? 'طلبات ملغاة' : (examSubTab === 'all' ? 'السجل الشامل (الكل)' : 'الطلبات النشطة')))) }}
                </v-chip>
              </div>
            </div>

            <!-- عرض الجدول المركزي للاختبارات حسب التبويب النشط -->
            <custom-data-table
              :key="'exams-tbl-' + examSubTab + '-' + currentExamSubTabList.length"
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
                    <div class="d-flex align-center flex-wrap gap-2 text-caption text-medium-emphasis mt-0.5">
                      <span class="font-weight-medium">المادة: {{ item.subject_name || 'عام' }}</span>
                      <span v-if="item.order_number" class="text-primary font-mono font-weight-bold">
                        <v-icon size="12" class="me-0.5">mdi-barcode</v-icon>
                        {{ item.order_number }}
                      </span>
                      <span v-if="item.exam_date" class="text-medium-emphasis">
                        <v-icon size="12" class="me-0.5" color="teal">mdi-calendar-check</v-icon>
                        الامتحان: {{ item.exam_date }}
                      </span>
                      <span v-if="item.scheduled_print_date" class="text-medium-emphasis">
                        <v-icon size="12" class="me-0.5" color="indigo">mdi-calendar-clock</v-icon>
                        الطباعة: {{ item.scheduled_print_date }}
                      </span>
                    </div>

                    <!-- شريط توضيح سبب الإرجاع إذا كان الطلب مرتجعاً -->
                    <div
                      v-if="item.order_status === 'returned' || item.is_returned"
                      class="mt-1 d-inline-flex align-center gap-1 px-2 py-0.5 rounded-lg bg-error-lighten-5 text-error border border-error-subtle text-caption font-weight-bold"
                    >
                      <v-icon size="14" color="error">mdi-alert-circle-outline</v-icon>
                      <span>سبب الإرجاع: {{ item.return_reason || 'يحتاج مراجعة وتعديل فني' }}</span>
                      <span v-if="item.return_notes" class="text-medium-emphasis ms-1 font-weight-regular">({{ item.return_notes }})</span>
                    </div>
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
                    <!-- 1. مكتمل (Completed) -->
                    <div
                      v-if="item.is_completed || item.order_status === 'completed'"
                      class="center-count-badge unified-badge-primary px-2.5 py-1 text-caption font-weight-bold"
                    >
                      <v-icon size="14" color="primary" class="me-1">mdi-check-decagram</v-icon>
                      <span>مكتمل</span>
                    </div>

                    <!-- 2. قيد الطباعة (Printing - سحب جزئي جارٍ) -->
                    <div
                      v-else-if="item.order_status === 'printing'"
                      class="center-count-badge unified-badge-warning px-2.5 py-1 text-caption font-weight-bold"
                    >
                      <v-icon size="14" color="warning" class="me-1">mdi-printer-play</v-icon>
                      <span>قيد الطباعة</span>
                    </div>

                    <!-- 3. بانتظار الموعد (Scheduled - مجدول لموعد قادم) -->
                    <div
                      v-else-if="item.is_scheduled || item.order_status === 'scheduled'"
                      class="center-count-badge unified-badge-info px-2.5 py-1 text-caption font-weight-bold"
                    >
                      <v-icon size="14" color="info" class="me-1">mdi-calendar-clock</v-icon>
                      <span>بانتظار الموعد</span>
                    </div>

                    <!-- 4. فشل أو يحتاج معالجة (Failed - تعثر أو مرتجع) -->
                    <div
                      v-else-if="item.is_returned || item.order_status === 'failed' || item.order_status === 'returned'"
                      class="center-count-badge unified-badge-error px-2.5 py-1 text-caption font-weight-bold"
                      :title="item.return_reason || 'مرتجع للتعديل'"
                    >
                      <v-icon size="14" color="error" class="me-1">mdi-alert-circle-outline</v-icon>
                      <span>فشل أو يحتاج معالجة</span>
                    </div>

                    <!-- 5. ملغى (Cancelled) -->
                    <div
                      v-else-if="item.order_status === 'cancelled'"
                      class="center-count-badge unified-badge-grey px-2.5 py-1 text-caption font-weight-bold"
                    >
                      <v-icon size="14" class="me-1">mdi-cancel</v-icon>
                      <span>ملغى</span>
                    </div>

                    <!-- 6. بانتظار الاعتماد والمراجعة (Pending) -->
                    <div
                      v-else-if="item.is_pending || item.order_status === 'pending'"
                      class="center-count-badge unified-badge-warning px-2.5 py-1 text-caption font-weight-bold"
                    >
                      <v-icon size="14" color="warning" class="me-1">mdi-clock-alert-outline</v-icon>
                      <span>بانتظار الاعتماد</span>
                    </div>

                    <!-- 7. جاهز للتنفيذ (Ready - مستحق التنفيذ اليوم) -->
                    <div
                      v-else
                      class="center-count-badge unified-badge-primary px-2.5 py-1 text-caption font-weight-bold"
                    >
                      <v-icon size="14" color="primary" class="me-1">mdi-clock-fast</v-icon>
                      <span>جاهز للتنفيذ</span>
                    </div>
                  </div>
                </template>

                <template v-else-if="key === 'actions'">
                  <div class="d-flex align-center justify-center gap-1 flex-nowrap table-actions-cell">
                    <!-- 1. في تبويب "المستحقة" (Due Queue): تنفيذ فوري عبر الطباعة المباشرة واستوديو الطباعة -->
                    <template v-if="examSubTab === 'due'">
                      <!-- زر الطباعة المباشرة الفورية -->
                      <v-btn
                        size="small"
                        density="compact"
                        color="primary"
                        variant="flat"
                        rounded="lg"
                        class="font-weight-bold table-action-btn px-2"
                        prepend-icon="mdi-printer"
                        @click="openDirectPrintDialog(item)"
                        title="أمر الطباعة المباشر الفوري لكافة وثائق الاختبار"
                      >
                        طباعة مباشرة
                      </v-btn>

                      <!-- زر استوديو الطباعة التفصيلي -->
                      <v-btn
                        size="small"
                        density="compact"
                        icon="mdi-printer-eye"
                        color="primary"
                        variant="tonal"
                        rounded="lg"
                        class="table-action-icon-btn ms-1"
                        @click="openExamStudio(item)"
                        title="فتح استوديو الطباعة التفصيلي لتأكيد وتنفيذ السحب"
                      />

                      <!-- زر إذن الصرف الرسمي A4 -->
                      <v-btn
                        v-if="item.has_order"
                        size="small"
                        density="compact"
                        icon="mdi-file-document-check-outline"
                        color="secondary"
                        variant="tonal"
                        rounded="lg"
                        class="table-action-icon-btn ms-1"
                        @click="previewOrderManifest(item)"
                        title="معاينة إذن الصرف وأمر الطباعة الرسمي A4"
                      />

                      <!-- زر إلغاء أمر الطباعة رسمياً -->
                      <v-btn
                        size="small"
                        density="compact"
                        icon="mdi-cancel"
                        color="error"
                        variant="tonal"
                        rounded="lg"
                        class="table-action-icon-btn ms-1"
                        @click="openCancelOrderDialog(item)"
                        title="إلغاء أمر الطباعة رسمياً"
                      />
                    </template>

                    <!-- 2. في تبويب "المجدولة" (Scheduled): تقديم الموعد استثنائياً -->
                    <template v-else-if="examSubTab === 'scheduled'">
                      <v-btn
                        size="small"
                        density="compact"
                        color="warning"
                        variant="tonal"
                        rounded="lg"
                        class="font-weight-bold table-action-btn px-2"
                        prepend-icon="mdi-fast-forward"
                        @click="openAdvanceScheduleDialog(item)"
                        title="تقديم موعد الطباعة استثنائياً لليوم ونقله للمستحقة"
                      >
                        تقديم الموعد
                      </v-btn>
                      <v-btn
                        v-if="item.has_order"
                        size="small"
                        density="compact"
                        icon="mdi-file-document-outline"
                        color="secondary"
                        variant="tonal"
                        rounded="lg"
                        class="table-action-icon-btn ms-1"
                        @click="previewOrderManifest(item)"
                        title="معاينة إذن الصرف وأمر الطباعة الرسمي A4"
                      />
                      <!-- زر إلغاء أمر الطباعة رسمياً -->
                      <v-btn
                        size="small"
                        density="compact"
                        icon="mdi-cancel"
                        color="error"
                        variant="tonal"
                        rounded="lg"
                        class="table-action-icon-btn ms-1"
                        @click="openCancelOrderDialog(item)"
                        title="إلغاء أمر الطباعة رسمياً"
                      />
                    </template>

                    <!-- 3. في تبويب "المكتملة" (Completed): أرشفة وتوثيق فقط (حالة الطباعة مكتمل تظهر في عمود الحالة) -->
                    <template v-else-if="examSubTab === 'completed'">
                      <v-btn
                        v-if="item.has_order"
                        size="small"
                        density="compact"
                        color="secondary"
                        variant="tonal"
                        rounded="lg"
                        class="font-weight-bold table-action-btn px-2"
                        prepend-icon="mdi-file-document-check-outline"
                        @click="previewOrderManifest(item)"
                        title="معاينة إذن الصرف ومحضر التسليم الرسمي A4"
                      >
                        إذن الصرف والتسليم
                      </v-btn>
                      <v-btn
                        size="small"
                        density="compact"
                        icon="mdi-history"
                        color="info"
                        variant="tonal"
                        rounded="lg"
                        class="table-action-icon-btn ms-1"
                        @click="openExamBatchesHistory(item)"
                        title="عرض سجل وتاريخ دفعات السحب المطبوعة لهذا الاختبار"
                      />
                    </template>

                    <!-- 4. في تبويب "الملغية" (Cancelled): استعراض إذن الصرف أو إعادة التفعيل -->
                    <template v-else-if="examSubTab === 'cancelled'">
                      <v-btn
                        size="small"
                        density="compact"
                        color="primary"
                        variant="flat"
                        rounded="lg"
                        class="font-weight-bold table-action-btn px-2 text-white"
                        prepend-icon="mdi-restore"
                        @click="openApproveDialog(item)"
                        title="إعادة تفعيل واعتماد وجدولة طلب الطباعة الملغى"
                      >
                        إعادة التفعيل
                      </v-btn>
                      <v-btn
                        v-if="item.has_order"
                        size="small"
                        density="compact"
                        icon="mdi-file-document-outline"
                        color="secondary"
                        variant="tonal"
                        rounded="lg"
                        class="table-action-icon-btn ms-1"
                        @click="previewOrderManifest(item)"
                        title="معاينة إذن الصرف المحفوظ في الأرشيف"
                      />
                    </template>

                    <!-- 5. في تبويب "الطلبات" (All Orders): إجراءات مركزة دون تكرار شارات الحالة -->
                    <template v-else>
                      <!-- أ. مكتمل 100% -->
                      <template v-if="item.is_completed">
                        <v-btn
                          v-if="item.has_order"
                          size="small"
                          density="compact"
                          color="secondary"
                          variant="tonal"
                          rounded="lg"
                          class="font-weight-bold table-action-btn px-2"
                          prepend-icon="mdi-file-document-check-outline"
                          @click="previewOrderManifest(item)"
                          title="معاينة إذن الصرف ومحضر التسليم الرسمي A4"
                        >
                          إذن الصرف والتسليم
                        </v-btn>
                        <v-btn
                          size="small"
                          density="compact"
                          icon="mdi-history"
                          color="info"
                          variant="tonal"
                          rounded="lg"
                          class="table-action-icon-btn ms-1"
                          @click="openExamBatchesHistory(item)"
                          title="عرض سجل وتاريخ دفعات السحب المطبوعة لهذا الاختبار"
                        />
                      </template>

                      <!-- ب. طلب بانتظار الاعتماد والمراجعة -->
                      <template v-else-if="item.is_pending">
                        <v-btn
                          size="small"
                          density="compact"
                          color="primary"
                          variant="flat"
                          rounded="lg"
                          class="font-weight-bold table-action-btn px-2 text-white"
                          prepend-icon="mdi-check-decagram-outline"
                          @click="openApproveDialog(item)"
                          title="مراجعة واعتماد وجدولة طلب الطباعة رسمياً"
                        >
                          تأكيد واعتماد
                        </v-btn>
                        <v-btn
                          size="small"
                          density="compact"
                          icon="mdi-keyboard-return"
                          color="warning"
                          variant="tonal"
                          rounded="lg"
                          class="table-action-icon-btn ms-1"
                          @click="openReturnDialog(item)"
                          title="إرجاع طلب الطباعة للتعديل مع توثيق السبب"
                        />
                        <v-btn
                          v-if="item.has_order"
                          size="small"
                          density="compact"
                          icon="mdi-file-document-outline"
                          color="secondary"
                          variant="tonal"
                          rounded="lg"
                          class="table-action-icon-btn ms-1"
                          @click="previewOrderManifest(item)"
                          title="معاينة إذن الصرف واستمارة الطلب الرسمية"
                        />
                        <v-btn
                          size="small"
                          density="compact"
                          icon="mdi-cancel"
                          color="error"
                          variant="tonal"
                          rounded="lg"
                          class="table-action-icon-btn ms-1"
                          @click="openCancelOrderDialog(item)"
                          title="إلغاء أمر الطباعة رسمياً"
                        />
                      </template>

                      <!-- ج. طلب مرتجع للتعديل -->
                      <template v-else-if="item.is_returned">
                        <v-btn
                          size="small"
                          density="compact"
                          color="primary"
                          variant="flat"
                          rounded="lg"
                          class="font-weight-bold table-action-btn px-2 text-white"
                          prepend-icon="mdi-check-decagram-outline"
                          @click="openApproveDialog(item)"
                          title="إعادة فحص واعتماد الطلب بعد التعديل"
                        >
                          إعادة الاعتماد
                        </v-btn>
                        <v-btn
                          size="small"
                          density="compact"
                          icon="mdi-alert-circle-outline"
                          color="error"
                          variant="tonal"
                          rounded="lg"
                          class="table-action-icon-btn ms-1"
                          @click="openReturnDialog(item)"
                          :title="item.return_reason ? ('سبب الإرجاع: ' + item.return_reason) : 'عرض سبب الإرجاع'"
                        />
                        <v-btn
                          v-if="item.has_order"
                          size="small"
                          density="compact"
                          icon="mdi-file-document-outline"
                          color="secondary"
                          variant="tonal"
                          rounded="lg"
                          class="table-action-icon-btn ms-1"
                          @click="previewOrderManifest(item)"
                          title="معاينة إذن الصرف الرسمي A4"
                        />
                        <v-btn
                          size="small"
                          density="compact"
                          icon="mdi-cancel"
                          color="error"
                          variant="tonal"
                          rounded="lg"
                          class="table-action-icon-btn ms-1"
                          @click="openCancelOrderDialog(item)"
                          title="إلغاء أمر الطباعة رسمياً"
                        />
                      </template>

                      <!-- د. طلب مجدول لموعد قادم -->
                      <template v-else-if="item.is_scheduled">
                        <v-btn
                          size="small"
                          density="compact"
                          color="warning"
                          variant="tonal"
                          rounded="lg"
                          class="font-weight-bold table-action-btn px-2"
                          prepend-icon="mdi-fast-forward"
                          @click="openAdvanceScheduleDialog(item)"
                          title="تقديم موعد الطباعة استثنائياً ونقله للمستحقة"
                        >
                          تقديم الموعد
                        </v-btn>
                        <v-btn
                          v-if="item.has_order"
                          size="small"
                          density="compact"
                          icon="mdi-file-document-outline"
                          color="secondary"
                          variant="tonal"
                          rounded="lg"
                          class="table-action-icon-btn ms-1"
                          @click="previewOrderManifest(item)"
                          title="معاينة إذن الصرف الرسمي A4"
                        />
                        <v-btn
                          size="small"
                          density="compact"
                          icon="mdi-cancel"
                          color="error"
                          variant="tonal"
                          rounded="lg"
                          class="table-action-icon-btn ms-1"
                          @click="openCancelOrderDialog(item)"
                          title="إلغاء أمر الطباعة رسمياً"
                        />
                      </template>

                      <!-- هـ. طلب معتمد ومستحق جاهز للتنفيذ -->
                      <template v-else-if="item.is_due">
                        <v-btn
                          size="small"
                          density="compact"
                          color="primary"
                          variant="tonal"
                          rounded="lg"
                          class="font-weight-bold table-action-btn px-2"
                          prepend-icon="mdi-printer"
                          @click="examSubTab = 'due'"
                          title="الانتقال إلى تبويب المستحقة لتنفيذ الطباعة"
                        >
                          تنفيذ الطباعة
                        </v-btn>
                        <v-btn
                          v-if="item.has_order"
                          size="small"
                          density="compact"
                          icon="mdi-file-document-outline"
                          color="secondary"
                          variant="tonal"
                          rounded="lg"
                          class="table-action-icon-btn ms-1"
                          @click="previewOrderManifest(item)"
                          title="معاينة إذن الصرف الرسمي A4"
                        />
                        <v-btn
                          size="small"
                          density="compact"
                          icon="mdi-cancel"
                          color="error"
                          variant="tonal"
                          rounded="lg"
                          class="table-action-icon-btn ms-1"
                          @click="openCancelOrderDialog(item)"
                          title="إلغاء أمر الطباعة رسمياً"
                        />
                      </template>

                      <!-- و. في أي حالة أخرى -->
                      <template v-else>
                        <v-btn
                          size="small"
                          density="compact"
                          color="success"
                          variant="flat"
                          rounded="lg"
                          class="font-weight-bold table-action-btn px-2"
                          prepend-icon="mdi-check-circle-outline"
                          @click="openApproveDialog(item)"
                          title="اعتماد وجدولة طلب الطباعة"
                        >
                          تأكيد واعتماد
                        </v-btn>
                        <v-btn
                          size="small"
                          density="compact"
                          icon="mdi-keyboard-return"
                          color="warning"
                          variant="tonal"
                          rounded="lg"
                          class="table-action-icon-btn ms-1"
                          @click="openReturnDialog(item)"
                          title="إرجاع الطلب للتعديل"
                        />
                      </template>
                    </template>
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
              <!-- نوع المؤسسة التعليمية كفلتر منسدل أساسي عبر auto-list الموحد -->
              <v-col cols="12" sm="6" :md="institutionType === 'school' ? 4 : 3" :lg="institutionType === 'school' ? 2 : 3">
                <auto-list
                  v-model="institutionType"
                  :objects="sectorOptionsObjects"
                  name="ScreenTypeChoices"
                  label="نوع المؤسسة التعليمية"
                  placeholder="نوع المؤسسة التعليمية"
                  cols="12"
                  :add="false"
                  :hideDetails="true"
                  @update:model-value="onSectorChange"
                />
              </v-col>

              <!-- التعليم العام (المدرسي): محافظة -> مديرية -> مدرسة/مركز عبر auto-list الموحد -->
              <template v-if="institutionType === 'school'">
                <v-col cols="12" sm="6" md="4" lg="2">
                  <auto-list
                    v-model="selectedOfficeId"
                    :objects="officesObjects"
                    name="ScreenTypeChoices"
                    label="مكتب التربية (المحافظة)"
                    placeholder="كل المحافظات..."
                    cols="12"
                    :add="false"
                    :hideDetails="true"
                    @update:model-value="onStudioOfficeChange"
                  />
                </v-col>

                <v-col cols="12" sm="6" md="4" lg="2">
                  <auto-list
                    v-model="selectedDirectorateId"
                    :objects="directoratesObjectsFormatted"
                    name="ScreenTypeChoices"
                    label="إدارة التربية (المديرية)"
                    placeholder="كل المديريات..."
                    cols="12"
                    :add="false"
                    :hideDetails="true"
                    @update:model-value="onStudioDirectorateChange"
                  />
                </v-col>

                <v-col cols="12" sm="6" md="6" lg="3">
                  <auto-list
                    v-model="selectedSchoolId"
                    :objects="schoolsObjectsFormatted"
                    name="ScreenTypeChoices"
                    label="المدرسة / المركز الامتحاني"
                    placeholder="كل المراكز والمدارس..."
                    cols="12"
                    :add="false"
                    :hideDetails="true"
                    @update:model-value="onStudioSchoolChange"
                  />
                </v-col>
              </template>

              <!-- التعليم الجامعي: جامعة/كلية عبر auto-list الموحد -->
              <template v-else-if="institutionType === 'university'">
                <v-col cols="12" sm="6" md="4" lg="4">
                  <auto-list
                    v-model="selectedSchoolId"
                    :objects="schoolsObjectsFormatted"
                    name="ScreenTypeChoices"
                    label="الجامعة / الكلية"
                    placeholder="اختر الكلية أو الجامعة..."
                    cols="12"
                    :add="false"
                    :hideDetails="true"
                    @update:model-value="onStudioSchoolChange"
                  />
                </v-col>
              </template>

              <!-- التعليم الفني (معاهد): معهد/مركز عبر auto-list الموحد -->
              <template v-else-if="institutionType === 'institute'">
                <v-col cols="12" sm="6" md="4" lg="4">
                  <auto-list
                    v-model="selectedSchoolId"
                    :objects="schoolsObjectsFormatted"
                    name="ScreenTypeChoices"
                    label="المعهد / المركز الفني"
                    placeholder="اختر المعهد أو المركز..."
                    cols="12"
                    :add="false"
                    :hideDetails="true"
                    @update:model-value="onStudioSchoolChange"
                  />
                </v-col>
              </template>

              <!-- منسدلة اختيار الاختبار المعتمد المطلوب طباعة وثائقه عبر auto-list الموحد -->
              <v-col cols="12" :sm="institutionType === 'school' ? 6 : 12" :md="institutionType === 'school' ? 6 : 5" :lg="institutionType === 'school' ? 3 : 5">
                <auto-list
                  v-model="selectedExamId"
                  :objects="examsObjectsFormatted"
                  name="ScreenTypeChoices"
                  label="الاختبار المعتمد المطلوب طباعته"
                  placeholder="ابحث بالاختبار أو المادة أو الرمز..."
                  cols="12"
                  :add="false"
                  :hideDetails="true"
                  @update:model-value="onExamSelected"
                />
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
                    <custom-text-field
                      v-model="customCenterName"
                      label="اسم المركز الامتحاني / المدرسة"
                      cols="12"
                      :hideDetails="true"
                      :placeholder="selectedExam?.directorate || 'المركز الامتحاني الرئيسي'"
                    />
                  </v-col>
                  <v-col cols="12" sm="4">
                    <custom-text-field
                      v-model="customDirectorate"
                      label="المديرية"
                      cols="12"
                      :hideDetails="true"
                      :placeholder="selectedExam?.directorate || 'السبعين'"
                    />
                  </v-col>
                  <v-col cols="12" sm="4">
                    <custom-text-field
                      v-model="customGovernorate"
                      label="المحافظة"
                      cols="12"
                      :hideDetails="true"
                      :placeholder="selectedExam?.governorate || 'أمانة العاصمة'"
                    />
                  </v-col>
                  <v-col cols="12" sm="6">
                    <custom-text-field
                      v-model="customStageTitle"
                      label="عنوان الاختبار والمرحلة"
                      cols="12"
                      :hideDetails="true"
                      :placeholder="selectedExam?.title || 'اختبار الشهادة العامة'"
                    />
                  </v-col>
                  <v-col cols="12" sm="3">
                    <custom-text-field
                      v-model="customExamYear"
                      label="العام الدراسي"
                      cols="12"
                      :hideDetails="true"
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
              <!-- الفلاتر المنسدلة عبر auto-list الموحد -->
              <div class="d-flex align-center gap-2 flex-wrap">
                <!-- فلتر النموذج كمنسدلة عبر auto-list الموحد -->
                <div style="min-width: 190px; max-width: 230px;">
                  <auto-list
                    v-model="rosterModelFilter"
                    :objects="modelFilterObjects"
                    name="ScreenTypeChoices"
                    label="النموذج"
                    placeholder="النموذج"
                    cols="12"
                    :add="false"
                    :hideDetails="true"
                  />
                </div>

                <!-- فلتر حالة الطباعة كمنسدلة عبر auto-list الموحد -->
                <div style="min-width: 190px; max-width: 230px;">
                  <auto-list
                    v-model="rosterPrintFilter"
                    :objects="printStatusFilterObjects"
                    name="ScreenTypeChoices"
                    label="حالة الطباعة"
                    placeholder="حالة الطباعة"
                    cols="12"
                    :add="false"
                    :hideDetails="true"
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

              <!-- حقل البحث السريع بالاسم أو رقم الجلوس أو السري عبر custom-text-field الموحد -->
              <div style="min-width: 260px; max-width: 340px;">
                <custom-text-field
                  v-model="rosterSearch"
                  placeholder="بحث بالاسم أو رقم الجلوس أو السري..."
                  icon="magnify"
                  cols="12"
                  :hideDetails="true"
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
                  @click="printAllQuestionPapers"
                  :disabled="!questionModelsList.some(m => m.hasQuestions)"
                >
                  طباعة كافة نماذج الأسئلة ({{ questionModelsList.map(m => m.versionCode).join(', ') }})
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
                  <v-chip
                    size="small"
                    :color="item.hasQuestions ? 'success' : 'warning'"
                    variant="tonal"
                    class="font-weight-bold"
                    :prepend-icon="item.hasQuestions ? 'mdi-check-decagram-outline' : 'mdi-alert-circle-outline'"
                  >
                    {{ item.hasQuestions ? 'معتمد وجاهز' : 'فارغ (لا توجد أسئلة)' }}
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

              <!-- حقول التصفية والبحث عبر المكونات الموحدة -->
              <div class="d-flex align-center gap-2 flex-wrap">
                <div style="min-width: 190px; max-width: 230px;">
                  <auto-list
                    v-model="packageModelFilter"
                    :objects="modelFilterObjects"
                    name="ScreenTypeChoices"
                    label="النموذج"
                    placeholder="النموذج"
                    cols="12"
                    :add="false"
                    :hideDetails="true"
                  />
                </div>

                <div style="min-width: 220px; max-width: 280px;">
                  <custom-text-field
                    v-model="packageSearch"
                    placeholder="بحث برقم الجلوس أو اسم الطالب..."
                    icon="magnify"
                    cols="12"
                    :hideDetails="true"
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
            <custom-text-field
              v-model="searchQuery"
              label="اسم الاختبار أو دفعة الطباعة"
              placeholder="بحث بمعرف الدفعة (Batch) أو اسم الاختبار..."
              icon="magnify"
              cols="12"
              class="mb-3"
              :hideDetails="true"
              @keyup.enter="fetchBatches"
            />
          </v-col>

          <v-col cols="12" sm="4" md="3" class="d-flex align-center justify-end gap-2 mb-3">
            <custom-btn
              type="show"
              label="تصفية النتائج"
              color="primary"
              icon="mdi-filter"
              class="font-weight-bold px-5"
              :click="fetchBatches"
            />
            <custom-btn
              type="cancel_filter"
              :click="resetFilters"
              variant="tonal"
              color="error"
              label="تفريغ الفلاتر"
              icon="mdi-filter-off"
              class="font-weight-bold"
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

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 4. نافذة معاينة إذن الصرف وأمر الطباعة الرسمي A4                -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <PrintOrderManifestDialog
      v-model="manifestDialog"
      :order-data="selectedManifestOrder"
    />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 5. نافذة تأكيد اعتماد وجدولة طلب الطباعة (مكون منفصل ومستقل)     -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <PrintOrderApproveDialog
      v-model="approveOrderDialog"
      :exam="targetExamForApproval"
      @approved="onOrderApproved"
    />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 6. نافذة إرجاع طلب الطباعة للتعديل مع الملاحظات                  -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <v-dialog v-model="returnOrderDialog" max-width="560px" persistent>
      <v-card rounded="2xl" class="border elevation-6 overflow-hidden main-card">
        <v-card-title class="d-flex align-center justify-space-between bg-surface pa-4 px-6 border-b">
          <div class="d-flex align-center gap-3">
            <v-avatar color="warning" variant="tonal" size="40" class="rounded-xl">
              <v-icon color="warning" size="22">mdi-keyboard-return</v-icon>
            </v-avatar>
            <div>
              <div class="text-subtitle-1 font-weight-black text-on-surface">إرجاع طلب الطباعة للتعديل</div>
              <div class="text-caption text-medium-emphasis">تسجيل ملاحظات وأسباب الإرجاع لمسؤول الإدخال</div>
            </div>
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" @click="returnOrderDialog = false" />
        </v-card-title>

        <v-card-text class="pa-5 bg-surface text-right">
          <div class="pa-3 rounded-xl bg-surface-variant-subtle border mb-4">
            <div class="text-subtitle-2 font-weight-bold text-on-surface mb-1">
              {{ targetExamForReturn?.title }}
            </div>
            <div class="text-caption text-medium-emphasis">
              الكود: <span class="font-mono text-primary font-weight-bold">{{ targetExamForReturn?.uniqueCode }}</span>
            </div>
          </div>

          <!-- أسباب الإرجاع الشائعة عبر auto-list الموحد -->
          <div class="mb-4">
            <auto-list
              v-model="returnReasonSelected"
              :objects="returnReasonsObjects"
              name="ScreenTypeChoices"
              label="سبب الإرجاع الرئيسي"
              placeholder="اختر سبب الإرجاع الرئيسي"
              cols="12"
              :add="false"
              :hideDetails="true"
            />
          </div>

          <!-- تفاصيل وملاحظات إضافية عبر custom-text-note الموحد -->
          <div class="mb-2">
            <custom-text-note
              v-model="returnNotesText"
              rows="3"
              label="ملاحظات وتوجيهات التعديل المطلوبة"
              placeholder="يرجى كتابة التعديلات المطلوبة بدقة ليتمكن المُنشئ من معالجتها..."
              cols="12"
              :hideDetails="true"
            />
          </div>
        </v-card-text>

        <v-card-actions class="pa-4 bg-surface border-t d-flex justify-space-between align-center">
          <v-btn variant="tonal" color="grey" rounded="lg" class="font-weight-bold px-4" @click="returnOrderDialog = false">
            إلغاء
          </v-btn>
          <v-btn
            color="warning"
            variant="flat"
            rounded="lg"
            class="font-weight-bold px-6"
            prepend-icon="mdi-keyboard-return"
            :loading="actionLoading"
            @click="confirmOrderReturn"
          >
            تأكيد إرجاع الطلب
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 7. نافذة تقديم موعد الطباعة استثنائياً (مكون موحد)               -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <AdvanceScheduleDialog
      v-model="advanceScheduleDialog"
      :exam="targetExamForAdvance"
      :loading="actionLoading"
      @confirm="onConfirmAdvanceSchedule"
    />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 8. نافذة إلغاء أمر الطباعة رسمياً وتوثيق القرار (مكون موحد)      -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <CancelPrintOrderDialog
      v-model="cancelOrderDialog"
      :exam="targetExamForCancel"
      :loading="actionLoading"
      @confirm="onConfirmCancelOrder"
    />

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- 8. نافذة تنفيذ أمر الطباعة المباشر الفوري (مكون منفصل ومستقل)     -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <DirectPrintOrderDialog
      v-model="directPrintDialog"
      :exam="targetExamForDirectPrint"
      :loading="directPrintLoading"
      @start-print="onDirectPrintStart"
      @confirm-execution="executeDirectPrint"
      @open-studio="openExamStudioFromDirect"
      @preview-omr="previewFirstOmrSheet"
      @preview-question-paper="previewFirstQuestionPaper"
      @preview-manifest="previewOrderManifest"
    />

    <!-- Hidden Staging Container for Print Batches (Available at Root Template Level for Zero DOM Overhead in Both Master & Studio Views) -->
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
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/omr/client.js'
import { gradebookAPI } from '@/services/omr/endpoints'
import YemeniMinistrySheet from '@/components/omr_templates/YemeniMinistrySheet.vue'
import YemeniAuditReportSheet from '@/components/omr_templates/YemeniAuditReportSheet.vue'
import YemeniOfficialQuestionPaper from '@/components/omr_templates/YemeniOfficialQuestionPaper.vue'
import { printOmrElement, printOmrBatch, printOfficialQuestionPaper, printExamPackage } from './utils/omrPrint'
import PrintOrderManifestDialog from './components/PrintOrderManifestDialog.vue'
import PrintOrderApproveDialog from './components/PrintOrderApproveDialog.vue'
import DirectPrintOrderDialog from './components/DirectPrintOrderDialog.vue'
import AdvanceScheduleDialog from './components/AdvanceScheduleDialog.vue'
import CancelPrintOrderDialog from './components/CancelPrintOrderDialog.vue'

const route = useRoute()
const router = useRouter()

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

// ── Unified Tripartite Filters State (matching students-master & OMRExamsView) ──
const filterInstitutionType = ref('school')
const filterGovernorate = ref(null)
const filterDirectorate = ref(null)
const filterOrganization = ref(null)

const isSchoolFilter = computed(() => {
  return !filterInstitutionType.value || filterInstitutionType.value === 'all' || filterInstitutionType.value === 'school'
})

const isOrgDisabled = computed(() => {
  if (isSchoolFilter.value) {
    return !filterGovernorate.value || !filterDirectorate.value
  }
  return !filterGovernorate.value
})

const orgFieldLabel = computed(() => {
  if (filterInstitutionType.value === 'university') return 'الجامعة / الكلية'
  if (filterInstitutionType.value === 'institute') return 'المعهد / مركز التدريب'
  return 'المدرسة / المركز الامتحاني'
})

const orgPlaceholder = computed(() => {
  if (isSchoolFilter.value) {
    if (!filterGovernorate.value) return 'اختر المحافظة أولاً'
    if (!filterDirectorate.value) return 'اختر المديرية أولاً'
    return 'المدرسة / المركز الامتحاني'
  }
  return filterGovernorate.value ? 'الجامعة / الكلية / المعهد' : 'اختر المحافظة أولاً'
})

const orgParam = computed(() => {
  const p = {}
  if (filterGovernorate.value) p.governorate = filterGovernorate.value
  if (filterDirectorate.value) p.directorate = filterDirectorate.value
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
    p.institution_type = filterInstitutionType.value
  }
  return Object.keys(p).length > 0 ? p : null
})

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
  institutionType.value = filterInstitutionType.value
  filterGovernorate.value = null
  filterDirectorate.value = null
  filterOrganization.value = null
  filterStage.value = null
  filterClassTrack.value = null
  filterSubject.value = null
  loadMasterData()
}

const onGovernorateChange = () => {
  filterDirectorate.value = null
  filterOrganization.value = null
  loadMasterData()
}

const onDirectorateChange = () => {
  filterOrganization.value = null
  loadMasterData()
}

const onOrganizationChange = () => {
  loadMasterData()
}

const onStageChange = () => {
  filterClassTrack.value = null
  filterSubject.value = null
  loadMasterData()
}

const onClassTrackChange = () => {
  filterSubject.value = null
  loadMasterData()
}

const onCollegeChange = () => {
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  loadMasterData()
}

const onDepartmentChange = () => {
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  loadMasterData()
}

const onSpecializationChange = () => {
  filterSemesterSubject.value = null
  loadMasterData()
}

const onInstituteFieldChange = () => {
  filterInstituteEducationSystem.value = null
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
  loadMasterData()
}

const onInstituteEducationSystemChange = () => {
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
  loadMasterData()
}

const resetUnifiedFilters = async () => {
  filterInstitutionType.value = 'all'
  institutionType.value = 'school'
  filterGovernorate.value = null
  filterDirectorate.value = null
  filterOrganization.value = null
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
  masterSearchQuery.value = ''
  await loadMasterData()
}

const allOfficesList = ref([])
const selectedOfficeId = ref([])
const selectedOfficeName = ref('')
const selectedDirectorateId = ref([])
const selectedDirectorateName = ref('')
const selectedSchoolId = ref([])
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
  { title: "رمز الاختبار", key: "uniqueCode", sortable: true, align: "center", width: "125px" },
  { title: "عنوان الاختبار والمادة", key: "title", sortable: true, align: "start", width: "290px", minWidth: "240px" },
  { title: "المدارس المشاركة", key: "schools_count", sortable: true, align: "center", width: "115px" },
  { title: "المقيدون", key: "total_registered", sortable: true, align: "center", width: "95px" },
  { title: "أوراق مطبوعة", key: "printed_count", sortable: true, align: "center", width: "105px" },
  { title: "نسبة الطباعة", key: "printed_rate", sortable: true, align: "center", width: "115px" },
  { title: "حالة الطباعة", key: "print_status", sortable: true, align: "center", width: "120px" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "140px" },
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

const normalizeIds = (val) => {
  if (!val) return []
  if (Array.isArray(val)) {
    return val.map(x => {
      if (typeof x === 'object' && x !== null) {
        return Number(x.id ?? x.value ?? x.raw?.id)
      }
      return Number(x)
    }).filter(n => !isNaN(n) && n > 0)
  }
  if (typeof val === 'object' && val !== null) {
    const id = Number(val.id ?? val.value ?? val.raw?.id)
    return (!isNaN(id) && id > 0) ? [id] : []
  }
  if (typeof val === 'string' && val.includes(',')) {
    return val.split(',').map(s => Number(s.trim())).filter(n => !isNaN(n) && n > 0)
  }
  const num = Number(val)
  return (!isNaN(num) && num > 0) ? [num] : []
}

// Autocomplete Options
const directoratesOptions = computed(() => {
  const officeIds = normalizeIds(selectedOfficeId.value)
  if (officeIds.length > 0) {
    return (directoratesList.value || []).filter(d => officeIds.includes(Number(d.office_id)))
  }
  return directoratesList.value || []
})

const schoolsOptions = computed(() => {
  let list = schoolsList.value || []
  if (institutionType.value !== 'all') {
    list = list.filter(s => !s.institution_type || s.institution_type === institutionType.value)
  }
  const dirIds = normalizeIds(selectedDirectorateId.value)
  const officeIds = normalizeIds(selectedOfficeId.value)

  if (dirIds.length > 0) {
    const dObjs = (directoratesList.value || []).filter(d => dirIds.includes(Number(d.id)))
    const dNames = dObjs.map(d => d.name?.replace(/^(إدارة التربية والتعليم - مديرية |مديرية )/, '').trim()).filter(Boolean)
    list = list.filter(s => 
      dirIds.includes(Number(s.directorate_id)) ||
      dNames.some(dn => s.directorate_name && s.directorate_name.includes(dn))
    )
  } else if (officeIds.length > 0) {
    const oObjs = (officesList.value || []).filter(o => officeIds.includes(Number(o.id)))
    const oGovs = oObjs.map(o => o.governorate_name?.trim()).filter(Boolean)
    list = list.filter(s => 
      officeIds.includes(Number(s.office_id)) ||
      oGovs.some(og => s.governorate_name && s.governorate_name.includes(og))
    )
  }
  const schoolIds = normalizeIds(selectedSchoolId.value)
  if (schoolIds.length > 0) {
    list = list.filter(s => schoolIds.includes(Number(s.id)))
  }
  return list
})

// Unified Objects for <auto-list> integration
const sectorOptionsObjects = computed(() => {
  return (sectorOptions || []).map(opt => ({
    id: opt.value,
    value: opt.value,
    name: opt.title,
    title: opt.title,
  }))
})

const officesObjects = computed(() => {
  return (officesList.value || []).map(o => ({
    id: o.id,
    value: o.id,
    name: o.office_name || o.name_ar || o.name,
    title: o.office_name || o.name_ar || o.name,
  }))
})

const directoratesObjectsFormatted = computed(() => {
  return (directoratesOptions.value || []).map(d => ({
    id: d.id,
    value: d.id,
    name: d.name || d.name_ar,
    title: d.name || d.name_ar,
  }))
})

const schoolsObjectsFormatted = computed(() => {
  return (schoolsOptions.value || []).map(s => ({
    id: s.id,
    value: s.id,
    name: s.name || s.school_name || s.name_ar,
    title: s.name || s.school_name || s.name_ar,
  }))
})

const examsObjectsFormatted = computed(() => {
  return (examsList.value || []).map(e => ({
    id: e.id,
    value: e.id,
    name: `${e.title || e.name || 'اختبار'} (${e.subject_name || 'عام'} - ${e.uniqueCode || ''})`,
    title: `${e.title || e.name || 'اختبار'} (${e.subject_name || 'عام'} - ${e.uniqueCode || ''})`,
  }))
})

// Filtered Master Tables Computeds
const filteredOfficesTable = computed(() => {
  let list = officesList.value || []
  const effGov = filterGovernorate.value ? [Number(filterGovernorate.value)] : normalizeIds(selectedOfficeId.value)
  if (effGov.length > 0) {
    list = list.filter(o => effGov.includes(Number(o.id)) || effGov.includes(Number(o.governorate_id)))
  }
  const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
  if (effSubj) {
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
  const effGov = filterGovernorate.value ? [Number(filterGovernorate.value)] : normalizeIds(selectedOfficeId.value)
  if (effGov.length > 0) {
    list = list.filter(d => effGov.includes(Number(d.office_id)) || effGov.includes(Number(d.governorate_id)))
  }
  const effDir = filterDirectorate.value ? [Number(filterDirectorate.value)] : normalizeIds(selectedDirectorateId.value)
  if (effDir.length > 0) {
    list = list.filter(d => effDir.includes(Number(d.id)))
  }
  const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
  if (effSubj) {
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
  const effType = (filterInstitutionType.value && filterInstitutionType.value !== 'all') 
    ? filterInstitutionType.value 
    : (institutionType.value !== 'all' ? institutionType.value : undefined)
  if (effType) {
    list = list.filter(s => !s.institution_type || s.institution_type === effType)
  }
  const effDir = filterDirectorate.value ? [Number(filterDirectorate.value)] : normalizeIds(selectedDirectorateId.value)
  const effGov = filterGovernorate.value ? [Number(filterGovernorate.value)] : normalizeIds(selectedOfficeId.value)

  if (effDir.length > 0) {
    const dObjs = (directoratesList.value || []).filter(d => effDir.includes(Number(d.id)))
    const dNames = dObjs.map(d => d.name?.replace(/^(إدارة التربية والتعليم - مديرية |مديرية )/, '').trim()).filter(Boolean)
    list = list.filter(s => 
      effDir.includes(Number(s.directorate_id)) ||
      dNames.some(dn => s.directorate_name && s.directorate_name.includes(dn))
    )
  } else if (effGov.length > 0) {
    const oObjs = (officesList.value || []).filter(o => effGov.includes(Number(o.id)))
    const oGovs = oObjs.map(o => o.governorate_name?.trim()).filter(Boolean)
    list = list.filter(s => 
      effGov.includes(Number(s.office_id)) ||
      effGov.includes(Number(s.governorate_id)) ||
      oGovs.some(og => s.governorate_name && s.governorate_name.includes(og))
    )
  }
  const effOrg = filterOrganization.value ? [Number(filterOrganization.value)] : normalizeIds(selectedSchoolId.value)
  if (effOrg.length > 0) {
    list = list.filter(s => effOrg.includes(Number(s.id)))
  }
  const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
  if (effSubj) {
    const sObj = subjectsList.value.find(s => s.id === effSubj)
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
  const effType = (filterInstitutionType.value && filterInstitutionType.value !== 'all') 
    ? filterInstitutionType.value 
    : (institutionType.value !== 'all' ? institutionType.value : undefined)
  if (effType) {
    list = list.filter(e => !e.institution_type || e.institution_type === effType)
  }
  const effOrg = filterOrganization.value ? [Number(filterOrganization.value)] : normalizeIds(selectedSchoolId.value)
  const effDir = filterDirectorate.value ? [Number(filterDirectorate.value)] : normalizeIds(selectedDirectorateId.value)
  const effGov = filterGovernorate.value ? [Number(filterGovernorate.value)] : normalizeIds(selectedOfficeId.value)

  if (effOrg.length > 0) {
    list = list.filter(e => effOrg.includes(Number(e.school_id)) || effOrg.includes(Number(e.school)) || effOrg.includes(Number(e.organization_id)))
  } else if (effDir.length > 0) {
    list = list.filter(e => effDir.includes(Number(e.directorate_id)) || effDir.includes(Number(e.directorate)))
  } else if (effGov.length > 0) {
    list = list.filter(e => effGov.includes(Number(e.governorate_id)) || effGov.includes(Number(e.office_id)) || effGov.includes(Number(e.governorate)))
  }

  if (filterStage.value) {
    list = list.filter(e => Number(e.stage_id) === Number(filterStage.value) || Number(e.stage) === Number(filterStage.value))
  }
  if (filterClassTrack.value) {
    list = list.filter(e => Number(e.class_track_id) === Number(filterClassTrack.value) || Number(e.class_track) === Number(filterClassTrack.value))
  }

  const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value
  if (effSubj) {
    list = list.filter(e => Number(e.subject_id) === Number(effSubj) || Number(e.subject) === Number(effSubj))
  }
  if (masterSearchQuery.value) {
    const q = masterSearchQuery.value.toLowerCase().trim()
    list = list.filter(e => 
      (e.title && e.title.toLowerCase().includes(q)) ||
      (e.uniqueCode && e.uniqueCode.toLowerCase().includes(q)) ||
      (e.subject_name && e.subject_name.toLowerCase().includes(q)) ||
      (e.order_number && e.order_number.toLowerCase().includes(q))
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

// ── Sub-tabs for "الاختبارات المعتمدة للطباعة" (الطلبات / المجدولة / المستحقة / المكتملة / الملغية / السجل الشامل) ──
const examSubTab = ref('orders')
const savedPrintOrders = ref([])
const manifestDialog = ref(false)
const selectedManifestOrder = ref(null)

const loadSavedPrintOrders = async () => {
  try {
    const res = await api.get('/api/omr/print-orders/')
    if (res.data && res.data.success) {
      savedPrintOrders.value = res.data.results || []
    }
  } catch (err) {
    console.error('Failed to load real print orders from backend:', err)
  }
}

const previewOrderManifest = (exam) => {
  const order = (savedPrintOrders.value || []).find(o => 
    String(o.exam_id) === String(exam.id) || 
    (o.exam_code && o.exam_code === exam.uniqueCode) ||
    (o.order_number && exam.uniqueCode && o.order_number.includes(exam.uniqueCode))
  )
  if (order) {
    selectedManifestOrder.value = {
      ...order,
      exam_title: exam.title || order.exam_title,
      subject_name: exam.subject_name || order.subject_name || 'عام',
      grand_total: exam.total_registered || exam.total_students || order.grand_total || 0,
      actual_exam_date: exam.exam_date || order.actual_exam_date,
    }
    manifestDialog.value = true
  } else {
    selectedManifestOrder.value = {
      order_number: exam.order_number || `PRN-REQ-${exam.uniqueCode || exam.id}`,
      exam_id: exam.id,
      exam_title: exam.title,
      exam_code: exam.uniqueCode,
      subject_name: exam.subject_name || 'عام',
      press_name: exam.press_name || 'المطبعة السرية المركزية (ديوان الوزارة)',
      scheduled_print_date: exam.scheduled_print_date || getTodayIso(),
      actual_exam_date: exam.exam_date || exam.actual_exam_date || getTodayIso(),
      status: exam.order_status || 'approved',
      grand_total: exam.total_registered || exam.total_students || 0,
    }
    manifestDialog.value = true
  }
}

const getTodayIso = () => {
  const d = new Date()
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const enrichedMasterExamsList = computed(() => {
  try {
    const baseList = filteredMasterExamsTable.value || []
    const today = getTodayIso()

    return baseList.filter(Boolean).map(exam => {
      try {
        const order = (savedPrintOrders.value || []).find(o => 
          o && (
            String(o.exam_id) === String(exam.id) || 
            (o.exam_code && exam.uniqueCode && String(o.exam_code) === String(exam.uniqueCode)) ||
            (o.order_number && exam.uniqueCode && String(o.order_number).includes(String(exam.uniqueCode)))
          )
        )

        const rawStatus = order?.status || (exam.order_status || 'pending')
        const scheduledDate = order?.scheduled_print_date || exam.scheduled_print_date || null
        const examDate = order?.actual_exam_date || exam.exam_date || null
        const orderNumber = order?.order_number || exam.order_number || null
        const pressName = order?.press_name || exam.press_name || null
        const grandTotal = order?.grand_total || (exam.total_registered || exam.total_students || 0)
        const returnReason = order?.return_reason || exam.return_reason || ''
        const returnNotes = order?.return_notes || exam.return_notes || ''

        const isFullyPrinted = (Number(exam.printed_rate) >= 100) || (exam.print_status === 'full') || (exam.print_status === 'printed') || rawStatus === 'completed'
        const isFailed = rawStatus === 'failed' || rawStatus === 'returned'
        const isCancelled = rawStatus === 'cancelled'

        // 1. Completed: 100% printed or status completed
        const isCompleted = isFullyPrinted

        // 2. Returned / Failed
        const isReturned = !isCompleted && isFailed

        // 3. Pending: incoming request not yet approved by committee
        const isPending = !isCompleted && !isReturned && !isCancelled && (rawStatus === 'pending')

        // 4. Scheduled: approved with future print date (> today)
        const isScheduled = !isCompleted && !isReturned && !isCancelled && !isPending && (rawStatus === 'scheduled' || (scheduledDate && scheduledDate > today))

        // 5. Due: approved with print date today or earlier (<= today), or in active printing
        const isDue = !isCompleted && !isReturned && !isCancelled && !isPending && !isScheduled && (rawStatus === 'ready' || rawStatus === 'printing' || (scheduledDate && scheduledDate <= today) || rawStatus === 'approved')

        const effectiveStatus = isCompleted ? 'completed' :
                               (isReturned ? 'failed' :
                               (isScheduled ? 'scheduled' :
                               (isDue ? (rawStatus === 'printing' ? 'printing' : 'ready') :
                               (isCancelled ? 'cancelled' : 'pending'))))

        return {
          ...exam,
          has_order: !!order || !!exam.order_number,
          order_status: effectiveStatus,
          raw_order_status: rawStatus,
          return_reason: returnReason,
          return_notes: returnNotes,
          order_number: orderNumber,
          scheduled_print_date: scheduledDate,
          actual_exam_date: examDate,
          press_name: pressName,
          total_to_print: grandTotal,
          is_pending: isPending,
          is_returned: isReturned,
          is_approved: !isPending && !isReturned && !isCancelled,
          is_scheduled: isScheduled,
          is_due: isDue,
          is_completed: isCompleted,
        }
      } catch (itemErr) {
        console.error('Error enriching exam item:', exam, itemErr)
        return exam
      }
    })
  } catch (err) {
    console.error('Error in enrichedMasterExamsList:', err)
    return filteredMasterExamsTable.value || []
  }
})

// ── Dialog States & Handlers for Print Orders Workflow ──
const approveOrderDialog = ref(false)
const targetExamForApproval = ref(null)
const actionLoading = ref(false)

const getCurrentUserOfficerName = () => {
  try {
    const raw = localStorage.getItem('auth_user') || localStorage.getItem('profile')
    if (raw) {
      const u = JSON.parse(raw)
      return u.full_name || u.name || u.username || 'مدير إدارة الامتحانات والكنترول'
    }
  } catch (e) {}
  return 'مدير إدارة الامتحانات والكنترول'
}

const openApproveDialog = (exam) => {
  targetExamForApproval.value = exam
  approveOrderDialog.value = true
}

const onOrderApproved = async (payload) => {
  await loadSavedPrintOrders()
  await loadMasterData()

  const today = getTodayIso()
  const isFuture = payload.scheduledDate > today
  if (isFuture) {
    examSubTab.value = 'scheduled'
    batchPrintNotification.value = {
      show: true,
      color: 'info',
      message: `تم اعتماد وتوثيق أمر الطباعة بنجاح للاختبار "${payload.exam.title}"! تم نقله إلى تبويب [المجدولة] بموعد طباعة (${payload.scheduledDate}).`,
    }
  } else {
    examSubTab.value = 'due'
    batchPrintNotification.value = {
      show: true,
      color: 'success',
      message: `تم اعتماد وتوثيق أمر الطباعة بنجاح للاختبار "${payload.exam.title}"! تم نقله إلى تبويب [المستحقة] وهو جاهز للتنفيذ الفوري الآن.`,
    }
  }

  if (payload.openManifest) {
    previewOrderManifest(payload.exam)
  }
}

const returnOrderDialog = ref(false)
const targetExamForReturn = ref(null)
const returnReasonSelected = ref('كمية الاحتياط تتجاوز النسبة المعتمدة دون وثيقة تفويض')
const returnNotesText = ref('')
const predefinedReturnReasons = [
  'كمية الاحتياط تتجاوز النسبة المعتمدة دون وثيقة تفويض',
  'نقص أو عدم تطابق في كشوفات الطلاب لبعض المراكز الامتحانية',
  'نماذج الأسئلة بحاجة لإعادة تدقيق ومراجعة فنية',
  'تعارض موعد الطباعة مع جدول تشغيل المطبعة المركزية',
  'أخرى (توضيح في الملاحظات أدناه)',
]

const returnReasonsObjects = computed(() => {
  return predefinedReturnReasons.map(r => ({
    id: r,
    value: r,
    name: r,
    title: r,
  }))
})

const advanceScheduleDialog = ref(false)
const targetExamForAdvance = ref(null)
const advanceReasonSelected = ref('شحن وترحيل مبكر لمحافظات بعيدة أو نائية (سقطرى، المهرة، إلخ)')
const advanceAuthDoc = ref('')
const advanceReasonsList = [
  'شحن وترحيل مبكر لمحافظات بعيدة أو نائية (سقطرى، المهرة، إلخ)',
  'توزيع أحمال ماكينات المطبعة المركزية وتفادي ضغط الأيام الأخيرة',
  'توجيه وزاري استثنائي لتقديم موعد الاختبار',
  'إجازة رسمية أو طارئ مناخي/أمني يستوجب الترحيل المبكر',
  'أخرى (مبرر إداري استثنائي)',
]

const openReturnDialog = (exam) => {
  targetExamForReturn.value = exam
  returnReasonSelected.value = predefinedReturnReasons[0]
  returnNotesText.value = ''
  returnOrderDialog.value = true
}

const confirmOrderReturn = async () => {
  if (!targetExamForReturn.value) return
  actionLoading.value = true
  try {
    const exam = targetExamForReturn.value

    await api.post('/api/omr/print-orders/return-order/', {
      exam_id: exam.id,
      return_reason: returnReasonSelected.value,
      return_notes: returnNotesText.value,
    })

    await loadSavedPrintOrders()
    await loadMasterData()
    returnOrderDialog.value = false

    batchPrintNotification.value = {
      show: true,
      color: 'warning',
      message: `تم إرجاع طلب طباعة الاختبار "${exam.title}" للتعديل بنجاح: (${returnReasonSelected.value}). سيظهر كمرتجع في السجل وشاشة إدارة الاختبارات.`,
    }
  } catch (e) {
    console.error('Failed to return order:', e)
  } finally {
    actionLoading.value = false
  }
}

const openAdvanceScheduleDialog = (exam) => {
  targetExamForAdvance.value = exam
  advanceReasonSelected.value = advanceReasonsList[0]
  advanceAuthDoc.value = ''
  advanceScheduleDialog.value = true
}

const onConfirmAdvanceSchedule = async ({ exam, reason, authDoc }) => {
  const target = exam || targetExamForAdvance.value
  if (!target) return
  actionLoading.value = true
  try {
    await api.post('/api/omr/print-orders/advance/', {
      exam_id: target.id,
      advance_reason: reason || advanceReasonSelected.value,
      advance_auth_doc: authDoc || advanceAuthDoc.value,
    })

    await loadSavedPrintOrders()
    await loadMasterData()
    advanceScheduleDialog.value = false
    examSubTab.value = 'due'

    batchPrintNotification.value = {
      show: true,
      color: 'success',
      message: `تم تقديم موعد طباعة "${target.title}" لليوم وتوثيق التفويض رسمياً! تم نقله إلى تبويب [المستحقة] وهو جاهز للتنفيذ الفوري الآن.`,
    }
  } catch (e) {
    console.error('Failed to advance schedule:', e)
  } finally {
    actionLoading.value = false
  }
}

// ── Cancel Print Order Handlers ──
const cancelOrderDialog = ref(false)
const targetExamForCancel = ref(null)

const openCancelOrderDialog = (exam) => {
  targetExamForCancel.value = exam
  cancelOrderDialog.value = true
}

const onConfirmCancelOrder = async ({ exam, reason, notes }) => {
  const target = exam || targetExamForCancel.value
  if (!target) return
  actionLoading.value = true
  try {
    const fullReason = (reason || 'تم إلغاء الاختبار بقرار من إدارة الامتحانات والكنترول') + (notes ? ` (${notes})` : '')

    await api.post('/api/omr/print-orders/cancel-order/', {
      exam_id: target.id,
      cancel_reason: fullReason,
    })

    target.order_status = 'cancelled'
    target.raw_order_status = 'cancelled'
    target.is_cancelled = true
    target.is_due = false
    target.is_scheduled = false
    target.return_reason = fullReason

    await Promise.all([
      loadSavedPrintOrders(),
      loadMasterData(),
    ])

    cancelOrderDialog.value = false
    examSubTab.value = 'cancelled'

    batchPrintNotification.value = {
      show: true,
      color: 'info',
      message: `تم إلغاء أمر طباعة "${target.title}" بنجاح وتوثيق القرار رسمياً! تم نقله إلى تبويب [الملغية].`,
    }
  } catch (err) {
    console.error('Failed to cancel order:', err)
    batchPrintNotification.value = {
      show: true,
      color: 'error',
      message: 'تعذر إلغاء أمر الطباعة، يرجى المحاولة لاحقاً.',
    }
  } finally {
    actionLoading.value = false
  }
}

// ── Direct Print Workflow Handlers ──
const directPrintDialog = ref(false)
const targetExamForDirectPrint = ref(null)
const directPrintLoading = ref(false)
const directPrintOptions = ref({
  sheets: true,
  booklets: true,
  roster: true,
  manifest: true,
})

const openDirectPrintDialog = async (exam) => {
  targetExamForDirectPrint.value = exam
  directPrintOptions.value = {
    sheets: true,
    booklets: true,
    roster: true,
    manifest: true,
  }
  rosterModelFilter.value = 'all'
  selectedStudentIds.value = []
  directPrintDialog.value = true
  if (selectedExamId.value !== exam.id || !examDetails.value) {
    selectedExamId.value = exam.id
    loadExamDetails(exam.id)
  }
}

const previewFirstOmrSheet = async () => {
  if (!examDetails.value || !examDetails.value.registered_students?.length) {
    if (targetExamForDirectPrint.value?.id) {
      await loadExamDetails(targetExamForDirectPrint.value.id)
    }
  }
  const st = examDetails.value?.registered_students?.[0]
  if (st) {
    openSingleSheetPreview(st)
  } else {
    printBlankSheetVersion('A')
  }
}

const previewFirstQuestionPaper = async () => {
  if (!examDetails.value?.question_models?.length) {
    if (targetExamForDirectPrint.value?.id) {
      await loadExamDetails(targetExamForDirectPrint.value.id)
    }
  }
  const model = examDetails.value?.question_models?.[0] || {
    id: 1,
    model_code: 'A',
    paper_title: targetExamForDirectPrint.value?.title || 'كراسة الأسئلة الامتحانية',
    questions_count: 50,
  }
  selectedQuestionPaperForPreview.value = model
  previewQuestionPaperDialog.value = true
}

const openExamStudioFromDirect = (exam) => {
  directPrintDialog.value = false
  openExamStudio(exam)
}

const dispatchRealDirectPrint = (exam, options, realOmrElements = []) => {
  if (!exam) return

  const orderNum = exam.order_number || `PRN-REQ-${exam.uniqueCode || exam.id}`
  const examTitle = exam.title || 'الاختبار العام'
  const examCode = exam.uniqueCode || 'EXAM-CODE'
  const subjectName = exam.subject_name || 'الرياضيات'
  const pressName = exam.press_name || 'المطبعة السرية المركزية (ديوان الوزارة)'
  const officerName = exam.responsible_officer || 'مدير إدارة الامتحانات والكنترول'
  const schedDate = exam.scheduled_print_date || getTodayIso()
  const totalCount = exam.total_registered || exam.total_students || 8
  const schoolsCount = exam.schools_count || 1

  const students = examDetails.value?.registered_students || []

  let sectionsHtml = ''

  // 1. إذا تم تحديد إذن الصرف وأمر الطباعة A4
  if (options?.manifest) {
    sectionsHtml += `
      <div class="print-page manifest-page">
        <div class="header">
          <div class="header-badge">وثيقة رسمية معتمدة</div>
          <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
          <h3>اللجنة العليا للاختبارات — الإدارة العامة للاختبارات والكنترول</h3>
          <h1 class="manifest-title">إذن صرف وأمر طباعة رسمي للاختبارات</h1>
          <div class="order-code">رقم أمر الطباعة: ${orderNum}</div>
        </div>

        <table class="info-table">
          <tr>
            <td class="lbl">اسم الاختبار:</td>
            <td class="val"><strong>${examTitle}</strong></td>
            <td class="lbl">المادة:</td>
            <td class="val">${subjectName}</td>
          </tr>
          <tr>
            <td class="lbl">كود الاختبار:</td>
            <td class="val font-mono">${examCode}</td>
            <td class="lbl">تاريخ التنفيذ المعتمد:</td>
            <td class="val font-mono">${schedDate}</td>
          </tr>
          <tr>
            <td class="lbl">المطبعة المنفذة:</td>
            <td class="val">${pressName}</td>
            <td class="lbl">المسؤول المعتمد:</td>
            <td class="val">${officerName}</td>
          </tr>
          <tr>
            <td class="lbl">إجمالي الطلاب المشمولين:</td>
            <td class="val"><strong>${totalCount} طالب</strong></td>
            <td class="lbl">عدد المراكز الامتحانية:</td>
            <td class="val">${schoolsCount} مركز</td>
          </tr>
        </table>

        <div class="section-title">بيان وتفويض صرف وثائق الاختبار للمطبعة</div>
        <table class="items-table">
          <thead>
            <tr>
              <th>م</th>
              <th>البيان والمستند</th>
              <th>المواصفة والمقاس</th>
              <th>الكمية المصرح بها</th>
              <th>حالة التجهيز</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>أوراق إجابة التصحيح الآلي (OMR) مشفرة ومؤمنة بالباركود</td>
              <td>A5 / A4 ورق أبيض 80 جرام مقاوم للحرارة</td>
              <td><strong>${totalCount} ورقة</strong></td>
              <td>معتمد وجاهز للسحب</td>
            </tr>
            <tr>
              <td>2</td>
              <td>كراسات الأسئلة الامتحانية (النماذج المعتمدة)</td>
              <td>A4 / A3 مغلفة طباعة سرية عالية الدقة</td>
              <td><strong>${totalCount} كراسة</strong></td>
              <td>معتمد وجاهز للسحب</td>
            </tr>
            <tr>
              <td>3</td>
              <td>كشوف المناداة ومحاضر فتح المظاريف للمراكز</td>
              <td>A4 كشوف جرد وتسليم رسمية</td>
              <td><strong>${schoolsCount} كشوف</strong></td>
              <td>معتمد وجاهز للسحب</td>
            </tr>
          </tbody>
        </table>

        <div class="signatures-grid">
          <div class="sig-box">
            <div>عضو لجنة التحقق والاعتماد</div>
            <div class="sig-line">التوقيع: ...........................</div>
            <div>التاريخ: ${schedDate}</div>
          </div>
          <div class="sig-box">
            <div>المشرف المسؤول بالمطبعة</div>
            <div class="sig-line">التوقيع: ...........................</div>
            <div>الختم الرسمي: ....................</div>
          </div>
          <div class="sig-box">
            <div>مدير عام الامتحانات والكنترول</div>
            <div class="sig-line">المصادقة: ...........................</div>
            <div>التاريخ: ${schedDate}</div>
          </div>
        </div>
      </div>
    `
  }

  // 2. إذا تم تحديد كشوف المناداة ومحاضر المراكز
  if (options?.roster) {
    const listForRoster = students.length > 0 ? students : Array.from({ length: totalCount }, (_, i) => ({
      seat_number: 1001 + i,
      secret_number: 5001 + i,
      student_name: `طالب مقيد ${i + 1}`,
      school_name: 'المركز الامتحاني المعتمد',
      model_code: ['A', 'B', 'C', 'D'][i % 4],
    }))

    let studentRows = ''
    listForRoster.forEach((st, idx) => {
      studentRows += `
        <tr>
          <td style="text-align: center;">${idx + 1}</td>
          <td style="text-align: center; font-family: monospace; font-weight: bold;">${st.seat_number || ''}</td>
          <td style="text-align: center; font-family: monospace;">${st.secret_number || ''}</td>
          <td style="font-weight: bold;">${st.student_name || ''}</td>
          <td>${st.school_name || 'المركز الرئيسي'}</td>
          <td style="text-align: center; font-weight: bold;">نموذج ${st.model_code || 'A'}</td>
          <td style="min-width: 100px;"></td>
        </tr>
      `
    })

    sectionsHtml += `
      <div class="print-page">
        <div class="header">
          <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
          <h3>كشف تسليم واستلام وثائق الاختبار للمركز الامتحاني</h3>
          <div class="order-code">الاختبار: ${examTitle} (${examCode}) — المادة: ${subjectName}</div>
        </div>
        <table class="items-table" style="font-size: 12px;">
          <thead>
            <tr>
              <th style="width: 30px;">م</th>
              <th style="width: 90px;">رقم الجلوس</th>
              <th style="width: 80px;">الرقم السري</th>
              <th>اسم الطالب</th>
              <th>المدرسة</th>
              <th style="width: 80px;">النموذج</th>
              <th style="width: 120px;">توقيع الاستلام</th>
            </tr>
          </thead>
          <tbody>
            ${studentRows}
          </tbody>
        </table>
      </div>
    `
  }

  // 3. كراسات الأسئلة الامتحانية (إذا تم تحديدها)
  if (options?.booklets) {
    const models = examDetails.value?.question_models || [
      { model_code: 'A', questions_count: 50 },
      { model_code: 'B', questions_count: 50 },
      { model_code: 'C', questions_count: 50 },
      { model_code: 'D', questions_count: 50 },
    ]
    models.forEach((m) => {
      sectionsHtml += `
        <div class="print-page question-booklet-page">
          <div class="header">
            <div class="header-badge">سري للغاية — وثيقة امتحانية رسمية</div>
            <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
            <h3>كراسة الأسئلة الامتحانية المقننة — نموذج (${m.model_code || 'A'})</h3>
            <div class="order-code">المادة: ${subjectName} | كود الاختبار: ${examCode}</div>
          </div>
          <div style="border: 2px dashed #000; padding: 25px; text-align: center; margin: 40px 0; border-radius: 8px;">
            <h2 style="margin: 0 0 10px 0;">كراسة الأسئلة — نموذج (${m.model_code || 'A'})</h2>
            <p style="font-size: 14px; color: #444;">
              عدد الفقرات: <strong>${m.questions_count || 50} فقرة اختيار من متعدد</strong> | الزمن المحدد: <strong>ساعتان ونصف</strong>
            </p>
            <p style="font-size: 12px; color: #777; margin-top: 20px;">
              تعليمات: تأكد من تطابق نموذج كراسة الأسئلة (${m.model_code || 'A'}) مع النموذج المطبوع على ورقة إجابتك المخصصة.
            </p>
          </div>
        </div>
      `
    })
  }

  // 4. أوراق إجابة OMR الرسمية الحقيقية للنظام (SVGs الأصلية المعتمدة)
  if (options?.sheets && realOmrElements && realOmrElements.length > 0) {
    realOmrElements.forEach(el => {
      const cloned = el.cloneNode(true)
      if (cloned instanceof HTMLElement) {
        cloned.querySelectorAll('.d-print-none, button, .v-btn').forEach(b => b.remove())
      }
      sectionsHtml += `
        <div class="print-page omr-real-sheet-page">
          <div class="real-sheet-container">
            ${cloned.outerHTML}
          </div>
        </div>
      `
    })
  }

  // إذا لم يختر أي خيار محدد، نطبع حزمة الاختبار الأساسية
  if (!sectionsHtml) {
    sectionsHtml = `
      <div class="print-page">
        <div class="header">
          <h2>الجمهورية اليمنية — وزارة التربية والتعليم</h2>
          <h3>أمر سحب وثائق الاختبار</h3>
          <h1>${examTitle} (${examCode})</h1>
        </div>
        <p style="text-align: center; font-size: 16px; margin-top: 30px;">
          المادة: ${subjectName} | إجمالي المقيدين: ${totalCount} طالب | المطبعة: ${pressName}
        </p>
      </div>
    `
  }

  const onlySheetsSelected = !!(options?.sheets && !options?.manifest && !options?.booklets && !options?.roster)
  const omrPageSize = selectedSheetLayout.value === 'full_a4' ? 'A4 portrait' : 'A5 landscape'

  const fullHtml = `
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
      <meta charset="utf-8">
      <title>أمر سحب وثائق الاختبار - ${examTitle} (${examCode})</title>
      <style>
        @page {
          size: ${onlySheetsSelected ? omrPageSize : 'A4 portrait'};
          margin: ${onlySheetsSelected ? '0' : '6mm 8mm'};
        }
        @page omr-page {
          size: ${omrPageSize};
          margin: 0;
        }
        *, *::before, *::after {
          box-sizing: border-box;
          -webkit-print-color-adjust: exact !important;
          print-color-adjust: exact !important;
        }
        body {
          font-family: 'Amiri', 'Traditional Arabic', 'Cairo', Tahoma, Arial, sans-serif;
          margin: 0;
          padding: 0;
          color: #000;
          background: #fff;
        }
        .print-page {
          page-break-after: always;
          break-after: page;
          padding: 6px;
          min-height: 270mm;
          box-sizing: border-box;
        }
        .print-page:last-child {
          page-break-after: auto;
          break-after: auto;
        }
        .header {
          text-align: center;
          border-bottom: 2px solid #000;
          padding-bottom: 8px;
          margin-bottom: 12px;
        }
        .header h2 { margin: 0 0 3px 0; font-size: 17px; font-weight: bold; }
        .header h3 { margin: 0 0 3px 0; font-size: 14px; font-weight: normal; color: #333; }
        .header-badge {
          display: inline-block;
          font-size: 11px;
          font-weight: bold;
          border: 1px solid #000;
          padding: 2px 8px;
          border-radius: 4px;
          margin-bottom: 4px;
        }
        .manifest-title {
          font-size: 19px;
          font-weight: 900;
          margin: 4px 0;
          text-decoration: underline;
        }
        .order-code {
          font-family: monospace;
          font-weight: bold;
          font-size: 13px;
          margin-top: 3px;
        }
        .info-table, .items-table {
          width: 100%;
          border-collapse: collapse;
          margin-bottom: 12px;
          font-size: 12px;
        }
        .info-table td {
          border: 1px solid #666;
          padding: 5px 8px;
        }
        .info-table .lbl {
          background: #f4f4f4;
          width: 18%;
          font-weight: bold;
        }
        .info-table .val {
          width: 32%;
        }
        .items-table th, .items-table td {
          border: 1px solid #000;
          padding: 5px 6px;
          text-align: center;
        }
        .items-table th {
          background: #f0f0f0;
          font-weight: bold;
        }
        .section-title {
          font-weight: bold;
          font-size: 13px;
          margin: 10px 0 5px 0;
        }
        .signatures-grid {
          display: flex;
          justify-content: space-between;
          margin-top: 30px;
          font-size: 11px;
          font-weight: bold;
          text-align: center;
        }
        .sig-box {
          width: 30%;
          border: 1px solid #aaa;
          padding: 8px;
          border-radius: 6px;
        }
        .sig-line {
          margin: 20px 0 6px 0;
        }
        .font-mono {
          font-family: monospace, monospace;
        }

        /* ── تنسيق ورقة OMR الحقيقية الأصلية ── */
        .omr-real-sheet-page {
          page: omr-page;
          display: flex;
          justify-content: center;
          align-items: center;
          padding: 0;
          min-height: ${onlySheetsSelected ? '100vh' : 'auto'};
        }
        .real-sheet-container {
          width: 100%;
          max-width: 210mm;
          margin: auto;
        }
        .real-sheet-container svg {
          width: 100% !important;
          max-width: 210mm !important;
          height: auto !important;
          max-height: ${selectedSheetLayout.value === 'full_a4' ? '297mm' : '148.5mm'} !important;
          display: block !important;
          margin: auto !important;
        }
        .yemeni-audit-report-sheet {
          width: 100% !important;
          max-width: 100% !important;
          margin: 0 auto !important;
        }
      </style>
    </head>
    <body>
      ${sectionsHtml}
    </body>
    </html>
  `

  // إزالة أي إطار طباعة سابق لضمان عدم التراكم
  const existingFrame = document.getElementById('omr-hardware-print-frame')
  if (existingFrame) {
    existingFrame.remove()
  }

  // إنشاء إطار طباعة مخفي في الصفحة (لا يحظره أي متصفح كالنوافذ المنبثقة)
  const iframe = document.createElement('iframe')
  iframe.id = 'omr-hardware-print-frame'
  iframe.style.position = 'fixed'
  iframe.style.right = '0'
  iframe.style.bottom = '0'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = '0'
  iframe.style.visibility = 'hidden'
  iframe.setAttribute('aria-hidden', 'true')
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow?.document || iframe.contentDocument
  if (doc) {
    doc.open()
    doc.write(fullHtml)
    doc.close()

    // استدعاء نافذة الطباعة الحقيقية للنظام والمتصفح فوراً بعد إعداد المستند
    setTimeout(() => {
      try {
        iframe.contentWindow?.focus()
        iframe.contentWindow?.print()
      } catch (err) {
        console.warn('Iframe print error, falling back to window.print():', err)
        window.print()
      }
    }, 250)
  } else {
    window.print()
  }
}

const onDirectPrintStart = async ({ exam, options }) => {
  if (!exam) return

  directPrintLoading.value = true
  try {
    // 1. التأكد من تحديد الاختبار وتحميل بياناته
    selectedExam.value = exam
    selectedExamId.value = exam.id
    if (!examDetails.value || examDetails.value.id !== exam.id) {
      await loadExamDetails(exam.id)
    }

    rosterModelFilter.value = 'all'
    selectedStudentIds.value = []

    // 2. إذا تم اختيار أوراق إجابة OMR، نقوم باستخراج الأوراق الحقيقية الأصلية من المكون المعتمد
    let realOmrElements = []
    if (options?.sheets) {
      printingBatch.value = true
      await nextTick()
      const stagingEl = document.getElementById('omr-registry-batch-staging')
      if (stagingEl) {
        stagingEl.classList.remove('d-none')
        await nextTick()
        // منح وقت كافٍ للمكون لرسم SVG وشفرات الباركود وQR الرسمية
        await new Promise(resolve => setTimeout(resolve, 450))

        const isAudit = selectedSheetLayout.value === 'full_a4'
        if (isAudit) {
          realOmrElements = Array.from(stagingEl.querySelectorAll('.yemeni-audit-report-sheet'))
        } else {
          realOmrElements = Array.from(stagingEl.querySelectorAll('svg.yemeni-ministry-sheet-svg'))
          if (!realOmrElements.length) {
            realOmrElements = Array.from(stagingEl.querySelectorAll('svg'))
          }
        }
        stagingEl.classList.add('d-none')
      }
    }

    // 3. التحقق من الحالات المحددة بدقة كاملة وفق ما يحدده المستخدم فقط:
    // أ) إذا اختار المستخدم أوراق إجابة OMR فقط:
    if (options?.sheets && !options?.manifest && !options?.roster && !options?.booklets) {
      if (realOmrElements.length > 0) {
        await printOmrBatch(realOmrElements, {
          title: `أوراق_تظليل_${exam.uniqueCode || 'OMR'}_${selectedSheetLayout.value}`,
          isA5: selectedSheetLayout.value === 'compact_a5',
        })
        return
      }
    }

    // ب) إذا اختار المستخدم كشوف المناداة ومحاضر المراكز فقط:
    if (options?.roster && !options?.sheets && !options?.manifest && !options?.booklets) {
      printAuditRoster()
      return
    }

    // ج) إذا اختار كراسات الأسئلة الرسمية فقط:
    if (options?.booklets && !options?.sheets && !options?.manifest && !options?.roster) {
      await printCurrentQuestionPaper()
      return
    }

    // د) في حال اختيار أكثر من مستند أو توليفة كاملة:
    dispatchRealDirectPrint(exam, options, realOmrElements)
  } catch (err) {
    console.error('Error during direct print execution:', err)
  } finally {
    directPrintLoading.value = false
    printingBatch.value = false
  }
}

const executeDirectPrint = async (payload) => {
  const exam = payload?.exam || targetExamForDirectPrint.value
  const actualCount = Number(payload?.actualPrintedCount ?? (exam?.total_registered || exam?.total_students || 0))
  const totalCount = exam?.total_registered || exam?.total_students || 0
  const chosenOptions = payload?.options || directPrintOptions.value
  const notes = payload?.notes || ''

  if (!exam) return
  if (actualCount <= 0) {
    directPrintDialog.value = false
    batchPrintNotification.value = {
      show: true,
      color: 'warning',
      message: `تم إلغاء عملية السحب لعدم اكتمال الطباعة على الماكينة (0 ورقة). الطلب لا زال محفوظاً في قائمة المستحقة للتنفيذ.`,
    }
    return
  }

  directPrintLoading.value = true
  try {
    const batchId = `BATCH_DIRECT_${Date.now()}`

    // 1. Call mark-printed on real backend database with the verified count
    await api.post(`/api/omr/exam-linking/${exam.id}/mark-printed/`, {
      batch_id: batchId,
      student_ids: actualCount >= totalCount ? 'all' : undefined,
      notes: notes,
    })

    // 2. Update state reflecting whether it's fully or partially printed
    exam.printed_count = actualCount
    exam.printed_rate = Math.round((actualCount / (totalCount || 1)) * 100)
    if (actualCount >= totalCount) {
      exam.print_status = 'full'
      exam.is_completed = true
      exam.is_due = false
      examSubTab.value = 'completed'
    } else {
      exam.print_status = 'partial'
      exam.is_completed = false
      exam.is_due = true
    }

    // 3. Reload persistent state from backend
    await Promise.all([
      loadSavedPrintOrders(),
      loadMasterData(),
      fetchExamsList(),
      fetchBatches(),
    ])

    directPrintDialog.value = false

    batchPrintNotification.value = {
      show: true,
      color: 'info',
      message: actualCount >= totalCount 
        ? `تمت مصادقة إتمام الطباعة بنجاح للاختبار "${exam.title}"! تم توثيق الدفعة برقم (${batchId}) لعدد ${actualCount} ورقة بنسبة 100%.`
        : `تم توثيق السحب الجزئي بنجاح للاختبار "${exam.title}"! تم قيد ${actualCount} ورقة وتبقى ${totalCount - actualCount} ورقة في قائمة المستحقة.`,
    }
  } catch (err) {
    console.error('Direct print error:', err)
  } finally {
    directPrintLoading.value = false
  }
}

const openExamBatchesHistory = (exam) => {
  const b = (batches.value || []).find(x => 
    String(x.exam_id) === String(exam.id) || 
    (x.exam_code && x.exam_code === exam.uniqueCode) || 
    (x.exam_title && exam.title && (x.exam_title.includes(exam.title) || exam.title.includes(x.exam_title)))
  )
  if (b) {
    viewBatchDetails(b)
  } else {
    masterTab.value = 'registry'
    masterSearchQuery.value = exam.title || exam.uniqueCode || ''
    getBatchMasterData()
  }
}

const allExamsList = computed(() => enrichedMasterExamsList.value || [])
const pendingAndActiveOrdersList = computed(() => (enrichedMasterExamsList.value || []).filter(e => !e.is_completed && !e.is_cancelled && e.order_status !== 'cancelled'))
const scheduledExamsList = computed(() => (enrichedMasterExamsList.value || []).filter(e => e.is_scheduled))
const dueExamsList = computed(() => (enrichedMasterExamsList.value || []).filter(e => e.is_due))
const completedExamsList = computed(() => (enrichedMasterExamsList.value || []).filter(e => e.is_completed))
const cancelledExamsList = computed(() => (enrichedMasterExamsList.value || []).filter(e => e.order_status === 'cancelled' || e.raw_order_status === 'cancelled' || e.is_cancelled))

const allExamsCount = computed(() => allExamsList.value.length)
const pendingAndActiveOrdersCount = computed(() => pendingAndActiveOrdersList.value.length)
const scheduledExamsCount = computed(() => scheduledExamsList.value.length)
const dueExamsCount = computed(() => dueExamsList.value.length)
const completedExamsCount = computed(() => completedExamsList.value.length)
const cancelledExamsCount = computed(() => cancelledExamsList.value.length)

const currentExamSubTabList = computed(() => {
  if (examSubTab.value === 'orders') return pendingAndActiveOrdersList.value
  if (examSubTab.value === 'scheduled') return scheduledExamsList.value
  if (examSubTab.value === 'due') return dueExamsList.value
  if (examSubTab.value === 'completed') return completedExamsList.value
  if (examSubTab.value === 'cancelled') return cancelledExamsList.value
  return allExamsList.value
})

const examMasterTableItems = ref({
  results: [],
  count: 0,
  pagination: { count: 0, total: 0, num_pages: 1, current_page: 1 },
})

const getExamMasterData = async (params = {}) => {
  const p = params?.params || params || {}
  const page = p.page || 1
  const pageSize = p.page_size || 20
  const all = currentExamSubTabList.value || []
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

watch([currentExamSubTabList, examSubTab], () => {
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
    const effGov = filterGovernorate.value || (normalizeIds(selectedOfficeId.value)[0] || undefined)
    const effDir = filterDirectorate.value || (normalizeIds(selectedDirectorateId.value)[0] || undefined)
    const effOrg = filterOrganization.value || (normalizeIds(selectedSchoolId.value)[0] || undefined)
    const effSubj = filterSubject.value || filterSemesterSubject.value || filterInstituteSubject.value || selectedSubjectId.value || undefined
    const effType = (filterInstitutionType.value && filterInstitutionType.value !== 'all') 
      ? filterInstitutionType.value 
      : (institutionType.value !== 'all' ? institutionType.value : undefined)

    const baseParams = {
      institution_type: effType,
      subject: effSubj,
      governorate: effGov,
    }
    const officeParams = { ...baseParams }
    if (effGov) {
      officeParams.office_id = effGov
      officeParams.governorate_id = effGov
    }

    const dirParams = { ...officeParams }
    if (effDir) {
      dirParams.directorate_id = effDir
    }

    const schoolParams = { ...dirParams }
    if (effOrg) {
      schoolParams.school_id = effOrg
      schoolParams.organization_id = effOrg
    }
    if (filterStage.value) schoolParams.stage = filterStage.value
    if (filterClassTrack.value) schoolParams.class_track = filterClassTrack.value
    if (filterCollege.value) schoolParams.college = filterCollege.value
    if (filterDepartment.value) schoolParams.department = filterDepartment.value
    if (filterSpecialization.value) schoolParams.specialization = filterSpecialization.value

    const [allOfficesRes, officesRes, directoratesRes, schoolsRes, examsRes] = await Promise.all([
      (!allOfficesList.value || !allOfficesList.value.length)
        ? gradebookAPI.getByOffice(baseParams).catch(() => ({ data: { results: [] } }))
        : Promise.resolve({ data: { results: allOfficesList.value } }),
      gradebookAPI.getByOffice(officeParams).catch(() => ({ data: { results: [] } })),
      gradebookAPI.getByDirectorate(dirParams).catch(() => ({ data: { results: [] } })),
      gradebookAPI.getBySchool(schoolParams).catch(() => ({ data: { results: [] } })),
      gradebookAPI.list(schoolParams).catch(() => ({ data: { results: [] } }))
    ])
    if (!allOfficesList.value || !allOfficesList.value.length) {
      allOfficesList.value = allOfficesRes.data?.results || []
    }
    officesList.value = officesRes.data?.results || []
    directoratesList.value = directoratesRes.data?.results || []
    schoolsList.value = schoolsRes.data?.results || []
    masterExamsList.value = examsRes.data?.results || []
    await loadSavedPrintOrders()
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
  selectedOfficeId.value = []
  selectedOfficeName.value = ''
  selectedDirectorateId.value = []
  selectedDirectorateName.value = ''
  selectedSchoolId.value = []
  selectedSchoolName.value = ''
  selectedSubjectId.value = null
  selectedSubjectName.value = ''
  masterSearchQuery.value = ''
  await loadMasterData()
}

const onSectorChange = (val) => {
  institutionType.value = val
  selectedOfficeId.value = []
  selectedOfficeName.value = ''
  selectedDirectorateId.value = []
  selectedDirectorateName.value = ''
  selectedSchoolId.value = []
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
  selectedOfficeId.value = officeId || []
  const officeIds = normalizeIds(selectedOfficeId.value)
  if (officeIds.length > 0) {
    const validDirIds = (directoratesList.value || []).filter(d => officeIds.includes(Number(d.office_id))).map(d => d.id)
    selectedDirectorateId.value = (selectedDirectorateId.value || []).filter(id => validDirIds.includes(id))
  } else {
    selectedDirectorateId.value = []
  }
  selectedSchoolId.value = []
  loadMasterData()
}

const onDirectorateFilterChange = (dirId) => {
  selectedDirectorateId.value = dirId || []
  selectedSchoolId.value = []
  const dirIds = normalizeIds(selectedDirectorateId.value)
  const currentOfficeIds = normalizeIds(selectedOfficeId.value)
  if (dirIds.length > 0 && currentOfficeIds.length === 0) {
    const relatedOffices = (directoratesList.value || [])
      .filter(d => dirIds.includes(Number(d.id)) && d.office_id)
      .map(d => Number(d.office_id))
    if (relatedOffices.length > 0) {
      selectedOfficeId.value = Array.from(new Set(relatedOffices))
    }
  }
  loadMasterData()
}

const onSchoolFilterChange = (schoolId) => {
  selectedSchoolId.value = schoolId || []
  loadMasterData()
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

const institutionTypeOptions = [
  { text: 'الكل (مدارس وجامعات ومعاهد)', value: 'all', icon: 'mdi-domain' },
  { text: 'تعليم مدرسي', value: 'school', icon: 'mdi-school' },
  { text: 'تعليم جامعي', value: 'university', icon: 'mdi-domain' },
  { text: 'معاهد وتدريب مهني', value: 'institute', icon: 'mdi-tools' },
]

const resetInstitutionFilters = () => {
  resetUnifiedFilters()
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

const modelFilterObjects = computed(() => {
  return (modelFilterSelectOptions.value || []).map(o => ({
    id: o.value,
    value: o.value,
    name: o.title,
    title: o.title,
  }))
})

const printStatusFilterObjects = computed(() => {
  return (printStatusFilterOptions.value || []).map(o => ({
    id: o.value,
    value: o.value,
    name: o.title,
    title: o.title,
  }))
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
  if (filteredRosterStudents.value && filteredRosterStudents.value.length > 0) {
    return filteredRosterStudents.value
  }
  if (examDetails.value?.registered_students && examDetails.value.registered_students.length > 0) {
    return examDetails.value.registered_students
  }
  const count = selectedExam.value?.total_registered || selectedExam.value?.total_students || 8
  const models = ['A', 'B', 'C', 'D']
  return Array.from({ length: Math.max(count, 4) }, (_, i) => ({
    id: `reg_st_${i + 1}`,
    student_name: `طالب مقيد ${i + 1}`,
    seat_number: 418485 + i,
    secret_number: 5001 + i,
    model_code: models[i % models.length],
    school_name: selectedExam.value?.directorate || 'المركز الاختباري المعتمد',
    governorate: selectedExam.value?.governorate || 'أمانة العاصمة',
    directorate: selectedExam.value?.directorate || 'معين',
  }))
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
  const students = (filteredRosterStudents.value && filteredRosterStudents.value.length > 0)
    ? filteredRosterStudents.value
    : (examDetails.value?.registered_students || [])
  if (!students.length) return

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
        @page { size: A4 landscape; margin: 10mm; }
        *, *::before, *::after { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
        body { font-family: 'Amiri', 'Traditional Arabic', Tahoma, sans-serif; margin: 0; padding: 10px; color: #000; background: #fff; }
        .header { text-align: center; border-bottom: 2px solid #000; padding-bottom: 12px; margin-bottom: 16px; }
        .header h2 { margin: 0 0 6px 0; font-size: 20px; }
        .header h3 { margin: 0 0 6px 0; font-size: 16px; font-weight: normal; }
        .meta-grid { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 13px; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; }
        th, td { border: 1px solid #000; padding: 6px 4px; }
        th { background-color: #f0f0f0; }
        .footer { margin-top: 25px; display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; }
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
    </body>
    </html>
  `

  const existingFrame = document.getElementById('roster-print-frame')
  if (existingFrame) existingFrame.remove()

  const iframe = document.createElement('iframe')
  iframe.id = 'roster-print-frame'
  iframe.style.position = 'fixed'
  iframe.style.right = '0'
  iframe.style.bottom = '0'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = '0'
  iframe.style.visibility = 'hidden'
  iframe.setAttribute('aria-hidden', 'true')
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow?.document || iframe.contentDocument
  if (doc) {
    doc.open()
    doc.write(html)
    doc.close()

    setTimeout(() => {
      try {
        iframe.contentWindow?.focus()
        iframe.contentWindow?.print()
      } catch (err) {
        window.print()
      }
    }, 250)
  } else {
    window.print()
  }
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
  if (v?.questions?.length !== undefined) return v.questions.length
  if (v?.questionsCount !== undefined) return v.questionsCount
  return 0
}

const getSectionsForVersion = (versionCode) => {
  const v = examDetails.value?.versions?.find(ver => ver.versionCode === versionCode) ||
            examDetails.value?.versions?.[0]
  const qList = v?.questions || []
  const total = qList.length || (v?.questionsCount || 0)
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
  const vers = examDetails.value?.versions || []
  if (vers.length > 0) {
    return vers.map(v => {
      const qCount = v.questions?.length || 0
      return {
        versionCode: v.versionCode,
        title: `كراسة ورقة الأسئلة - نموذج ${v.versionCode}`,
        questionsCount: qCount,
        hasQuestions: qCount > 0,
      }
    })
  }
  return []
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

const printAllQuestionPapers = async () => {
  const versions = questionModelsList.value.filter(m => m.hasQuestions).map(m => m.versionCode)
  for (const ver of versions) {
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
    loadSavedPrintOrders(),
    loadSubjects(),
    loadMasterData(),
    fetchBatches(),
  ])

  const qExam = route.query.exam || route.query.exam_id
  const qView = route.query.view
  const qTab = route.query.tab

  if (qView === 'orders' || qTab === 'exams') {
    currentView.value = 'master'
    masterTab.value = 'exams'
    if (route.query.subtab) {
      examSubTab.value = route.query.subtab
    }
  } else if (qExam) {
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

// Watch route.query to maintain URL and tab/subtab synchronization reactively
watch(() => route.query, (q) => {
  if (!q) return
  const qExam = q.exam || q.exam_id
  const qView = q.view
  const qTab = q.tab

  if (qView === 'orders' || qTab === 'exams') {
    currentView.value = 'master'
    masterTab.value = 'exams'
    if (q.subtab && ['orders', 'all', 'scheduled', 'due', 'completed', 'cancelled'].includes(q.subtab)) {
      examSubTab.value = q.subtab
    }
  } else if (qExam) {
    const eid = Number(qExam)
    if (eid && selectedExamId.value !== eid) {
      currentView.value = 'detail'
      selectedExamId.value = eid
      loadExamDetails(eid)
    }
  }
}, { deep: true })

// Keep route.query updated when user switches subtabs
watch(examSubTab, (sub) => {
  getExamMasterData()
  if (masterTab.value === 'exams' && currentView.value === 'master') {
    if (route.query.subtab !== sub) {
      router.replace({ query: { ...route.query, subtab: sub } }).catch(() => {})
    }
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

/* ── Compact & Refined Table Action Buttons and Chips ── */
:deep(.table-actions-cell) {
  min-height: 30px;
}

:deep(.table-action-btn),
.table-action-btn {
  height: 28px !important;
  min-height: 28px !important;
  font-size: 0.74rem !important;
  letter-spacing: 0 !important;
  padding: 0 8px !important;
  border-radius: 6px !important;
  box-shadow: none !important;
  text-transform: none !important;
  transition: all 0.15s ease-in-out !important;
}

:deep(.table-action-btn:hover),
.table-action-btn:hover {
  transform: translateY(-1px);
}

:deep(.table-action-btn .v-icon),
.table-action-btn .v-icon {
  font-size: 14px !important;
  width: 14px !important;
  height: 14px !important;
  margin-inline-end: 4px !important;
}

:deep(.table-action-chip),
.table-action-chip {
  height: 24px !important;
  min-height: 24px !important;
  font-size: 0.72rem !important;
  padding: 0 8px !important;
  border-radius: 6px !important;
}

:deep(.table-action-icon-btn),
.table-action-icon-btn {
  height: 28px !important;
  width: 28px !important;
  min-width: 28px !important;
  max-width: 28px !important;
  padding: 0 !important;
  border-radius: 6px !important;
}

:deep(.table-action-icon-btn .v-icon),
.table-action-icon-btn .v-icon {
  font-size: 15px !important;
  width: 15px !important;
  height: 15px !important;
  margin: 0 !important;
}

:deep(.table-action-chip .v-icon),
.table-action-chip .v-icon {
  font-size: 13px !important;
  width: 13px !important;
  height: 13px !important;
  margin-inline-end: 4px !important;
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

/* ── Unified Rectangular Status Badges ── */
.center-count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--v-theme-surface-variant), 0.35);
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-radius: 6px !important;
  font-size: 0.74rem;
  line-height: 1.2;
}

.unified-badge-primary {
  background: rgba(var(--v-theme-primary), 0.1) !important;
  color: rgb(var(--v-theme-primary)) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.25) !important;
}

.unified-badge-warning {
  background: rgba(245, 158, 11, 0.12) !important;
  color: #b45309 !important;
  border: 1px solid rgba(245, 158, 11, 0.25) !important;
}

.unified-badge-info {
  background: rgba(2, 132, 199, 0.12) !important;
  color: #0284c7 !important;
  border: 1px solid rgba(2, 132, 199, 0.25) !important;
}

.unified-badge-error {
  background: rgba(239, 68, 68, 0.12) !important;
  color: #dc2626 !important;
  border: 1px solid rgba(239, 68, 68, 0.25) !important;
}

.unified-badge-grey {
  background: rgba(148, 163, 184, 0.14) !important;
  color: #64748b !important;
  border: 1px solid rgba(148, 163, 184, 0.28) !important;
}
</style>
