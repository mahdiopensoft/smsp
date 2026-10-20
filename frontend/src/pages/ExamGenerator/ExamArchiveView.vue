<template>
  <div class="exam-archive-page">

    <!-- VIEW 1: LIST -->
    <div v-if="!selectedExam">


      <!-- Filters -->
      <filter-fields label="خيارات تصفية والبحث في أرشيف الاختبارات" class="main-card border-0 pa-5 rounded-2xl mb-8">
        <v-row dense class="align-center">
          <!-- Institution Type Selector (مدارس / جامعات / معاهد) -->
          <v-col cols="12" sm="6" :md="filterInstitutionType ? 3 : 4">
            <v-select
              v-model="filterInstitutionType"
              :items="institutionTypeOptions"
              item-title="text"
              item-value="value"
              class="mb-6"
              label="نوع المؤسسة التعليمية"
              placeholder="اختر نوع المؤسسة"
              prepend-inner-icon="mdi-domain"
              hide-details
              clearable
              density="compact"
              variant="outlined"
              @update:model-value="onInstitutionTypeChange"
            >
              <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" :prepend-icon="item.raw.icon" />
              </template>
            </v-select>
          </v-col>

          <!-- الظهور مشروط باختيار نوع المؤسسة: مدارس أو جامعات أو معاهد -->
          <template v-if="filterInstitutionType">
            <!-- 🏫 School Filters -->
            <template v-if="filterInstitutionType === 'school'">
              <auto-list
                v-model="filterStage"
                name="Stage"
                placeholder="المرحلة الدراسية"
                cols="3"
                :add="false"
                @update:model-value="onStageChange"
              />
              <auto-list
                v-model="filterClassTrack"
                name="ClassTrackByStage"
                :param="filterStage"
                placeholder="الصف والمسار"
                cols="3"
                :add="false"
                :disabled="!filterStage"
              />
              <auto-list
                v-model="filterSubject"
                name="Subject"
                :param="subjectFilterParam"
                placeholder="المادة الدراسية"
                cols="3"
                :add="false"
              />
            </template>

            <!-- 🎓 University Filters -->
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
                @update:model-value="filterSpecialization = null"
              />
              <auto-list
                v-model="filterSpecialization"
                name="Specialization"
                :param="filterDepartment"
                placeholder="التخصص والبرنامج"
                cols="3"
                :add="false"
                :disabled="!filterDepartment"
              />
              <auto-list
                v-model="filterSemesterSubject"
                name="SemesterSubject"
                :param="filterSpecialization"
                placeholder="مقرر الفصل الجامعي"
                cols="3"
                :add="false"
              />
            </template>

            <!-- 🏢 Institute Filters -->
            <template v-if="filterInstitutionType === 'institute'">
              <auto-list
                v-model="filterInstituteField"
                name="InstituteField"
                placeholder="المجال المهني"
                cols="3"
                :add="false"
                @update:model-value="() => { filterInstituteEducationSystem = null; filterInstituteSpecialization = null; filterInstituteCurriculum = null; filterInstituteSubject = null; }"
              />
              <auto-list
                v-model="filterInstituteEducationSystem"
                name="InstituteEducationSystem"
                :param="filterInstituteField"
                placeholder="نظام التعليم"
                cols="3"
                :add="false"
                :disabled="!filterInstituteField"
                @update:model-value="() => { filterInstituteSpecialization = null; filterInstituteCurriculum = null; filterInstituteSubject = null; }"
              />
              <auto-list
                v-model="filterInstituteSpecialization"
                name="InstituteSpecialization"
                :param="filterInstituteSpecParam"
                placeholder="التخصص المهني"
                cols="3"
                :add="false"
                :disabled="!filterInstituteEducationSystem"
                @update:model-value="() => { filterInstituteCurriculum = null; filterInstituteSubject = null; }"
              />
              <auto-list
                v-model="filterInstituteCurriculum"
                name="InstituteCurriculum"
                :param="filterInstituteSpecialization"
                placeholder="الخطة الدراسية"
                cols="3"
                :add="false"
                :disabled="!filterInstituteSpecialization"
                @update:model-value="filterInstituteSubject = null"
              />
              <auto-list
                v-model="filterInstituteSubject"
                name="InstituteSubject"
                :param="filterInstituteCurriculum"
                placeholder="المادة التدريبية"
                cols="3"
                :add="false"
                :disabled="!filterInstituteCurriculum"
              />
            </template>
          </template>

          <!-- Exam Period Filter -->
          <auto-list
            v-model="filterPeriod"
            name="Period"
            placeholder="الفترة الامتحانية"
            cols="3"
            :add="false"
          />

          <!-- Filter Actions -->
          <v-col cols="12" sm="12" md="auto" class="d-flex align-center justify-end gap-2 ms-auto">
            <custom-btn
              type="show"
              label="تصفية الأرشيف"
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

      <!-- Table -->
      <div class="main-card rounded-2xl overflow-hidden mb-8">
        <custom-data-table :headers="headers" :items="items" :getData="getData" :customLoading="loading"
          class="bg-transparent" :hasFilter="false" :log="false" :restore="false">
          <template v-slot:item-slot="{ item, key }">

            <template v-if="key === 'title'">
              <div class="d-flex align-center gap-3 py-1 cursor-pointer" @click="openDashboard(item)">
                <v-avatar :color="item.institutionTypeColor" variant="tonal" size="36" class="rounded-lg">
                  <v-icon size="18">{{ item.institutionTypeIcon }}</v-icon>
                </v-avatar>
                <div>
                  <div class="d-flex align-center gap-2">
                    <span class="font-weight-black text-subtitle-2 text-primary">{{ item.title }}</span>
                    <v-chip
                      size="x-small"
                      :color="item.institutionTypeColor"
                      variant="tonal"
                      class="font-weight-bold"
                    >
                      <v-icon start size="12">{{ item.institutionTypeIcon }}</v-icon>
                      {{ item.institutionTypeShortLabel }}
                    </v-chip>
                  </div>
                  <div class="text-caption text-medium-emphasis">{{ item.subjectName }}</div>
                </div>
              </div>
            </template>

            <template v-else-if="key === 'institutionType'">
              <v-chip
                size="small"
                :color="item.institutionTypeColor"
                variant="tonal"
                class="font-weight-bold"
              >
                <v-icon start size="15">{{ item.institutionTypeIcon }}</v-icon>
                {{ item.institutionTypeFullLabel }}
              </v-chip>
            </template>

            <template v-else-if="key === 'versionCode'">
              <div class="d-flex flex-wrap gap-1">
                <v-chip v-for="v in item.versionsList" :key="v.id" size="x-small" color="primary" variant="tonal"
                  class="font-weight-bold">
                  نموذج {{ v.versionCode }}
                </v-chip>
                <span v-if="!item.versionsList || item.versionsList.length === 0" class="text-medium-emphasis">-</span>
              </div>
            </template>

            <template v-else-if="key === 'questionsCount'">
              <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold">
                {{ item.questionsCount }} سؤال
              </v-chip>
            </template>

            <template v-else-if="key === 'studentsCount'">
              <v-chip size="small" :color="(item.studentsCount || 0) > 0 ? 'success' : 'default'" variant="tonal" class="font-weight-bold">
                <v-icon start size="x-small">mdi-account-group</v-icon>
                {{ item.studentsCount || 0 }} طالب
              </v-chip>
            </template>

            <template v-else-if="key === 'actions'">
              <div class="d-flex align-center justify-center">
                <v-menu location="bottom end" transition="slide-y-transition">
                  <template v-slot:activator="{ props }">
                    <v-btn
                      v-bind="props"
                      icon="mdi-dots-vertical"
                      variant="tonal"
                      color="primary"
                      size="small"
                      rounded="lg"
                      title="قائمة الإجراءات"
                    />
                  </template>

                  <v-list density="compact" class="rounded-xl border elevation-4 py-2" min-width="230">
                    <!-- عرض تفاصيل الاختبار والمناطق (زر العين) -->
                    <v-list-item
                      prepend-icon="mdi-eye-outline"
                      class="font-weight-bold text-info"
                      @click="openExamDetailsModal(item)"
                    >
                      <v-list-item-title class="font-weight-bold">تفاصيل الاختبار والمناطق</v-list-item-title>
                      <v-list-item-subtitle class="text-caption">المحافظة، المديرية والمعلومات</v-list-item-subtitle>
                    </v-list-item>

                    <v-divider class="my-1" />

                    <!-- لوحة التحكم -->
                    <v-list-item
                      prepend-icon="mdi-monitor-dashboard"
                      class="font-weight-bold text-primary"
                      @click="openDashboard(item)"
                    >
                      <v-list-item-title class="font-weight-bold">لوحة التحكم</v-list-item-title>
                      <v-list-item-subtitle class="text-caption">النماذج، الطلاب والطباعة</v-list-item-subtitle>
                    </v-list-item>

                    <!-- التصحيح الضوئي OMR -->
                    <v-list-item
                      prepend-icon="mdi-scanner"
                      class="font-weight-bold text-purple-darken-1"
                      :to="`/omr-exams?open_exam_id=${item.id}`"
                    >
                      <v-list-item-title class="font-weight-bold">التصحيح الضوئي (OMR)</v-list-item-title>
                      <v-list-item-subtitle class="text-caption">ربط وتصحيح الأوراق آلياً</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </div>
            </template>

          </template>
        </custom-data-table>
      </div>
    </div>

    <!-- VIEW 2: DASHBOARD -->
    <div v-else>
      <div class="main-card mb-6 pa-5 rounded-2xl">
        <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4">
          <div class="d-flex align-center gap-3">
            <back-to class="rounded-xl" @click="closeDashboard" />
            <div>
              <div class="d-flex align-center gap-2 mb-1">
                <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">{{
                  selectedExam.subjectName
                }}</v-chip>
              </div>
              <h1 class="text-h4 font-weight-black mb-0">{{ selectedExam.title }}</h1>
            </div>
          </div>
          <div class="d-flex align-center gap-2 flex-wrap">
            <custom-btn type="add" label="طباعة الأسئلة" icon="mdi-file-document-outline" variant="tonal" color="primary"
              class="font-weight-bold" :click="() => openPrintDialog('questions')" />
            <custom-btn type="add" label="مفتاح الإجابة" icon="mdi-key-variant" variant="tonal" color="success"
              class="font-weight-bold" :click="() => openPrintDialog('key')" />
            <custom-btn type="add" label="أوراق التظليل" icon="mdi-printer" color="emerald"
              class="font-weight-bold text-white" :click="() => openPrintDialog('sheets')" />
            <v-btn
              variant="flat"
              color="purple-darken-1"
              rounded="lg"
              class="font-weight-bold text-white shadow-sm"
              prepend-icon="mdi-scanner"
              :to="`/omr-exams?open_exam_id=${selectedExam.id}`"
            >
              الانتقال للتصحيح الآلي (OMR)
            </v-btn>
          </div>
        </div>
      </div>

      <div class="main-card rounded-2xl overflow-hidden">
        <v-tabs v-model="dashboardTab" color="primary" align-tabs="center" class="border-b border-slate-100">
          <v-tab :value="0" class="font-weight-bold"><v-icon start>mdi-information-outline</v-icon>معلومات
            الاختبار</v-tab>
          <v-tab :value="1" class="font-weight-bold"><v-icon start>mdi-file-document-multiple-outline</v-icon>النماذج
            والأسئلة</v-tab>
          <v-tab :value="2" class="font-weight-bold">
            <v-icon start>mdi-account-group</v-icon>
            الطلاب المسجلون
            <v-chip v-if="(totalStudentsCount || studentsTableItems.pagination?.count || 0) > 0" size="x-small" color="success" variant="tonal" class="font-weight-bold ms-2">
              {{ totalStudentsCount || studentsTableItems.pagination?.count || 0 }}
            </v-chip>
          </v-tab>
        </v-tabs>

        <v-window v-model="dashboardTab">

          <!-- TAB 1: INFO -->
          <v-window-item :value="0">
            <div class="pa-6">
              <v-row>
                <v-col cols="12" md="6">
                  <div class="pa-5 rounded-2xl border-subtle">
                    <h3 class="text-subtitle-1 font-weight-black mb-4 d-flex align-center gap-2">
                      <v-icon color="primary">mdi-calendar-clock</v-icon>
                      معلومات الاختبار
                    </h3>
                    <v-list density="compact" class="bg-transparent">
                      <v-list-item class="px-0">
                        <template v-slot:prepend><v-icon size="small"
                            class="me-2 text-medium-emphasis">mdi-book-open-variant</v-icon></template>
                        <v-list-item-title>المادة الدراسية</v-list-item-title>
                        <template v-slot:append><span class="font-weight-bold text-primary">{{ selectedExam.subjectName
                        }}</span></template>
                      </v-list-item>
                      <v-list-item class="px-0" v-if="examDashboardData && examDashboardData.classTrack">
                        <template v-slot:prepend><v-icon size="small"
                            class="me-2 text-medium-emphasis">mdi-school</v-icon></template>
                        <v-list-item-title>الصف والمسار</v-list-item-title>
                        <template v-slot:append><span class="font-weight-bold text-secondary">{{ examDashboardData.classTrack.name
                        }}</span></template>
                      </v-list-item>
                      <v-list-item class="px-0">
                        <template v-slot:prepend><v-icon size="small"
                            class="me-2 text-medium-emphasis">mdi-layers-triple</v-icon></template>
                        <v-list-item-title>عدد النماذج</v-list-item-title>
                        <template v-slot:append><span class="font-weight-bold text-emerald">{{
                          (selectedExam.versionsList || []).length }} نماذج</span></template>
                      </v-list-item>
                      <v-list-item class="px-0">
                        <template v-slot:prepend><v-icon size="small"
                            class="me-2 text-medium-emphasis">mdi-help-circle-outline</v-icon></template>
                        <v-list-item-title>إجمالي الأسئلة</v-list-item-title>
                        <template v-slot:append><span class="font-weight-bold text-indigo">{{
                          selectedExam.questionsCount }} سؤال</span></template>
                      </v-list-item>
                      <v-list-item class="px-0">
                        <template v-slot:prepend><v-icon size="small"
                            class="me-2 text-medium-emphasis">mdi-account-group</v-icon></template>
                        <v-list-item-title>الطلاب المسجلون</v-list-item-title>
                        <template v-slot:append>
                          <v-chip size="small" :color="totalStudentsCount > 0 ? 'success' : 'warning'" variant="tonal" class="font-weight-bold">
                            {{ totalStudentsCount }} طالب
                          </v-chip>
                        </template>
                      </v-list-item>
                    </v-list>
                  </div>
                </v-col>
                <v-col cols="12" md="6">
                  <div class="pa-5 rounded-2xl border-subtle">
                    <h3 class="text-subtitle-1 font-weight-black mb-4 d-flex align-center gap-2">
                      <v-icon color="secondary">mdi-chart-bar</v-icon>
                      توزيع مستويات الصعوبة
                    </h3>
                    <div v-if="selectedSetting">
                      <div class="mb-4" v-for="diff in difficultyBars" :key="diff.label">
                        <div class="d-flex justify-space-between mb-1">
                          <span class="text-body-2 font-weight-bold">{{ diff.label }}</span>
                          <span class="text-body-2 font-weight-black">{{ diff.pct }}%</span>
                        </div>
                        <v-progress-linear :model-value="diff.pct" :color="diff.color" height="12" rounded />
                      </div>
                    </div>
                    <div v-else class="text-center text-medium-emphasis pa-4">لا توجد بيانات إعدادات التوليد</div>
                  </div>
                </v-col>
              </v-row>
            </div>
          </v-window-item>

          <!-- TAB 2: VERSIONS -->
          <v-window-item :value="1">
            <div class="pa-6">
              <div class="d-flex align-center justify-center mb-6"
                v-if="selectedExam.versionsList && selectedExam.versionsList.length">
                <v-btn-toggle v-model="activeVersionIndex" mandatory color="primary" variant="outlined" divided
                  rounded="xl">
                  <v-btn v-for="(v, idx) in selectedExam.versionsList" :key="v.id" :value="idx" min-width="130"
                    class="font-weight-bold">
                    <v-icon start size="small">mdi-file-document-outline</v-icon>
                    نموذج {{ v.versionCode }}
                  </v-btn>
                </v-btn-toggle>
              </div>

              <v-tabs v-model="versionSubTab" color="secondary" density="compact"
                class="mb-4 border-b border-slate-100">
                <v-tab :value="0" class="font-weight-bold"><v-icon start size="small">mdi-file-eye</v-icon>ورقة
                  الأسئلة</v-tab>
                <v-tab :value="1" class="font-weight-bold"><v-icon start size="small">mdi-key-variant</v-icon>مفتاح
                  الإجابة</v-tab>
              </v-tabs>

              <v-window v-model="versionSubTab">

                <!-- Question Paper -->
                <v-window-item :value="0">
                  <div class="pa-5 rounded-2xl border-subtle">
                    <div class="d-flex align-center justify-space-between mb-4 flex-wrap gap-2">
                      <h4 class="text-subtitle-1 font-weight-black mb-0">ورقة الأسئلة - نموذج {{ activeVersion &&
                        activeVersion.versionCode }}</h4>
                      <custom-btn type="add" label="معاينة وطباعة" icon="mdi-printer" variant="tonal" color="primary"
                        :click="() => openPrintDialog('questions')" />
                    </div>
                    <div v-for="(q, idx) in activeVersionQuestions" :key="q.id"
                      class="question-preview-box mb-4 pa-4 rounded-xl">
                      <div class="d-flex align-start gap-3">
                        <v-avatar size="30" color="primary" class="text-white font-weight-black flex-shrink-0">{{ idx +
                          1
                        }}</v-avatar>
                        <div class="flex-grow-1">
                          <div class="d-flex justify-space-between align-center mb-2">
                            <div class="text-body-1 font-weight-bold" v-html="q.content" />
                            <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold ms-2">{{
                              q.assignedMark }} درجة</v-chip>
                          </div>
                          <div v-if="q.options && q.options.length">
                            <v-row dense class="mt-2">
                              <v-col v-for="(opt, oIdx) in q.options" :key="oIdx" cols="12" sm="6">
                                <div class="d-flex align-center py-1">
                                  <span class="option-badge me-2">{{ ['أ', 'ب', 'ج', 'د'][oIdx] }}</span>
                                  <span class="text-body-2">{{ opt.text }}</span>
                                </div>
                              </v-col>
                            </v-row>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div v-if="activeVersionQuestions.length === 0" class="text-center text-medium-emphasis pa-8">لا
                      توجد
                      أسئلة لهذا النموذج</div>
                  </div>
                </v-window-item>

                <!-- Answer Key -->
                <v-window-item :value="1">
                  <div class="pa-5 rounded-2xl border-subtle">
                    <div class="d-flex align-center justify-space-between mb-4 flex-wrap gap-2">
                      <h4 class="text-subtitle-1 font-weight-black mb-0">مفتاح الإجابة - نموذج {{ activeVersion &&
                        activeVersion.versionCode }}</h4>
                      <custom-btn type="add" label="معاينة وطباعة" icon="mdi-printer" variant="tonal" color="secondary"
                        :click="() => openPrintDialog('key')" />
                    </div>
                    <v-table density="compact" class="bg-transparent">
                      <thead>
                        <tr>
                          <th class="text-center font-weight-bold" style="width:80px">#</th>
                          <th class="text-center font-weight-bold" style="width:120px">الإجابة الصحيحة</th>
                          <th class="font-weight-bold">نص الإجابة</th>
                          <th class="text-center font-weight-bold" style="width:80px">الدرجة</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(q, idx) in activeVersionQuestions" :key="q.id">
                          <td class="text-center font-weight-bold">{{ idx + 1 }}</td>
                          <td class="text-center">
                            <v-chip size="small" color="success" variant="tonal" class="font-weight-bold text-white">{{
                              getCorrectOptionLabel(q) }}</v-chip>
                          </td>
                          <td class="font-weight-medium">{{ getCorrectOptionText(q) }}</td>
                          <td class="text-center">
                            <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">{{
                              q.assignedMark }}</v-chip>
                          </td>
                        </tr>
                      </tbody>
                      <tfoot v-if="activeVersionQuestions.length">
                        <tr>
                          <td colspan="3" class="text-end font-weight-bold">إجمالي درجات النموذج</td>
                          <td class="text-center">
                            <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">{{
                              versionTotalScore }}</v-chip>
                          </td>
                        </tr>
                      </tfoot>
                    </v-table>
                    <div v-if="activeVersionQuestions.length === 0" class="text-center text-medium-emphasis pa-8">لا
                      توجد
                      أسئلة لهذا النموذج</div>
                  </div>
                </v-window-item>

              </v-window>
            </div>
          </v-window-item>

          <!-- TAB 3: REGISTERED STUDENTS -->
          <v-window-item :value="2">
            <div class="pa-6">
              <!-- Summary Stats -->
              <v-row class="mb-6" v-if="totalStudentsCount > 0 || (studentsTableItems.results && studentsTableItems.results.length > 0)">
                <v-col cols="12" sm="4">
                  <div class="pa-4 rounded-2xl border-subtle text-center">
                    <v-icon size="28" color="primary" class="mb-2">mdi-account-group</v-icon>
                    <div class="text-h5 font-weight-black text-primary">{{ totalStudentsCount || studentsTableItems.pagination?.count || 0 }}</div>
                    <div class="text-caption font-weight-bold text-medium-emphasis">إجمالي الطلاب المسجلين</div>
                  </div>
                </v-col>
                <v-col cols="12" sm="4">
                  <div class="pa-4 rounded-2xl border-subtle text-center">
                    <v-icon size="28" color="success" class="mb-2">mdi-domain</v-icon>
                    <div class="text-h5 font-weight-black text-success">{{ backendUniqueSchoolsCount || 0 }}</div>
                    <div class="text-caption font-weight-bold text-medium-emphasis">مدارس مشمولة</div>
                  </div>
                </v-col>
                <v-col cols="12" sm="4">
                  <div class="pa-4 rounded-2xl border-subtle text-center">
                    <v-icon size="28" color="indigo" class="mb-2">mdi-file-document-multiple</v-icon>
                    <div class="text-h5 font-weight-black text-indigo">{{ (selectedExam.versionsList || []).length }}</div>
                    <div class="text-caption font-weight-bold text-medium-emphasis">نماذج موزعة</div>
                  </div>
                </v-col>
              </v-row>

              <!-- Controls Toolbar: Title + Filter by Version + Refresh -->
              <div class="d-flex align-center justify-space-between mb-4 flex-wrap gap-2">
                <h4 class="text-subtitle-1 font-weight-black d-flex align-center gap-2">
                  <v-icon size="20" color="primary">mdi-format-list-bulleted</v-icon>
                  قائمة الطلاب المسجلين
                </h4>
                <div class="d-flex align-center gap-2">
                  <v-select
                    v-if="totalStudentsCount > 0 || (studentsTableItems.results && studentsTableItems.results.length > 0)"
                    v-model="studentsFilterVersion"
                    :items="studentsVersionOptions"
                    item-title="text"
                    item-value="value"
                    density="compact"
                    variant="outlined"
                    style="min-width: 170px;"
                    hide-details
                    placeholder="تصفية بالنموذج"
                    prepend-inner-icon="mdi-filter-variant"
                  />
                  <custom-btn
                    label="تحديث"
                    icon="mdi-refresh"
                    variant="tonal"
                    color="primary"
                    :loading="loadingStudents"
                    :click="() => fetchRegisteredStudents()"
                  />
                </div>
              </div>

              <!-- Empty state alert if loaded and count is 0 -->
              <v-alert
                v-if="!loadingStudents && totalStudentsCount === 0 && (!studentsTableItems.results || studentsTableItems.results.length === 0)"
                type="info"
                variant="tonal"
                class="rounded-xl mb-4"
                icon="mdi-account-off-outline"
              >
                <div class="font-weight-bold mb-1">لا يوجد طلاب مسجلون</div>
                <div class="text-body-2">
                  لم يتم تسجيل أي طلاب في هذا الاختبار بعد. تأكد من أن الاختبار مرتبط بصف دراسي ونطاق جغرافي يحتوي على طلاب تم توليدهم.
                </div>
              </v-alert>

              <!-- Custom Data Table -->
              <div class="main-card rounded-2xl overflow-hidden mb-4">
                <custom-data-table
                  :headers="studentsHeaders"
                  :items="studentsTableItems"
                  :getData="fetchRegisteredStudents"
                  :customLoading="loadingStudents"
                  :hasFilter="false"
                  :log="false"
                  :restore="false"
                  :showSelect="false"
                  :actions="false"
                  class="bg-transparent"
                >
                  <template v-slot:item-slot="{ item, key }">
                    <!-- Student Name -->
                    <template v-if="key === 'studentName'">
                      <div class="d-flex align-center gap-2">
                        <v-avatar size="30" :color="item.gender === 'ذكر' ? 'blue' : 'pink'" variant="tonal" class="flex-shrink-0">
                          <v-icon size="16" :color="item.gender === 'ذكر' ? 'blue' : 'pink'">
                            {{ item.gender === 'ذكر' ? 'mdi-gender-male' : 'mdi-gender-female' }}
                          </v-icon>
                        </v-avatar>
                        <span class="font-weight-bold text-subtitle-2">{{ item.studentName }}</span>
                      </div>
                    </template>

                    <!-- Academic Number -->
                    <template v-else-if="key === 'academicNumber'">
                      <v-chip size="x-small" color="indigo" variant="tonal" class="font-weight-bold">
                        {{ item.academicNumber || '-' }}
                      </v-chip>
                    </template>

                    <!-- Seat Number -->
                    <template v-else-if="key === 'seatNumber'">
                      <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                        {{ item.seatNumber || '-' }}
                      </v-chip>
                    </template>

                    <!-- Secret Number -->
                    <template v-else-if="key === 'secretNumber'">
                      <span class="font-mono text-caption text-medium-emphasis">{{ item.secretNumber || '-' }}</span>
                    </template>

                    <!-- Version Code -->
                    <template v-else-if="key === 'versionCode'">
                      <v-chip size="x-small" color="success" variant="tonal" class="font-weight-bold">
                        نموذج {{ item.versionCode }}
                      </v-chip>
                    </template>

                    <!-- School Name -->
                    <template v-else-if="key === 'schoolName'">
                      <span class="text-body-2 font-weight-medium">{{ item.schoolName || '-' }}</span>
                    </template>

                    <!-- Directorate Name -->
                    <template v-else-if="key === 'directorateName'">
                      <span class="text-body-2 text-medium-emphasis">{{ item.directorateName || '-' }}</span>
                    </template>

                    <template v-else>
                      {{ item[key] }}
                    </template>
                  </template>
                </custom-data-table>
              </div>
            </div>
          </v-window-item>

        </v-window>
      </div>
    </div>

    <!-- WIDE PRINT & PREVIEW DIALOG -->
    <v-dialog v-model="printPreviewDialog" max-width="1150" width="1150" scrollable>
      <v-card class="d-flex flex-column rounded-2xl overflow-hidden" style="max-height: 90vh;">
        <!-- Sticky Dialog Header -->
        <div class="pa-4 border-b d-flex align-center justify-space-between flex-wrap gap-3 bg-surface d-print-none">
          <div class="d-flex align-center gap-3">
            <v-avatar size="40" :color="printModalType === 'questions' ? 'primary' : printModalType === 'key' ? 'success' : 'teal'" variant="tonal" class="rounded-xl">
              <v-icon size="22">
                {{ printModalType === 'questions' ? 'mdi-file-document-outline' : printModalType === 'key' ? 'mdi-key-variant' : 'mdi-checkbox-marked-circle-outline' }}
              </v-icon>
            </v-avatar>
            <div>
              <div class="text-subtitle-1 font-weight-black">
                {{ printModalType === 'questions' ? 'معاينة وطباعة ورقة الأسئلة' : printModalType === 'key' ? 'معاينة وطباعة مفتاح الإجابة الرسمي' : 'معاينة وطباعة أوراق التظليل الآلية' }}
              </div>
              <div class="text-caption text-medium-emphasis">
                {{ selectedExam?.title }} • كود الاختبار: {{ selectedExam?.uniqueCode }}
              </div>
            </div>
          </div>

          <!-- Controls: Mode Switcher + Version Selector + Print Button + Close -->
          <div class="d-flex align-center gap-2 flex-wrap">
            <!-- Mode Switcher -->
            <v-btn-toggle v-model="printModalType" mandatory density="compact" rounded="lg" color="primary" variant="outlined">
              <v-btn value="questions" class="font-weight-bold" size="small">
                <v-icon start size="16">mdi-file-document-outline</v-icon>
                الأسئلة
              </v-btn>
              <v-btn value="key" class="font-weight-bold" size="small">
                <v-icon start size="16">mdi-key-variant</v-icon>
                مفتاح الحل
              </v-btn>
              <v-btn value="sheets" class="font-weight-bold" size="small">
                <v-icon start size="16">mdi-checkbox-marked-circle-outline</v-icon>
                أوراق التظليل
              </v-btn>
            </v-btn-toggle>

            <!-- Version Selector (if exam has versions) -->
            <v-select
              v-if="examDetails?.versions?.length > 1"
              v-model="printVersionIndex"
              :items="examDetails.versions.map((v, i) => ({ title: `نموذج ${v.versionCode}`, value: i }))"
              item-title="title"
              item-value="value"
              density="compact"
              variant="outlined"
              hide-details
              style="min-width: 120px;"
            />

            <!-- Toggle Blank vs Key (Only for Sheets) -->
            <div v-if="printModalType === 'sheets'" class="d-flex align-center border rounded-lg pa-1 bg-slate-50 gap-1">
              <v-btn
                size="small"
                :variant="printSheetMode === 'blank' ? 'flat' : 'text'"
                :color="printSheetMode === 'blank' ? 'primary' : undefined"
                class="font-weight-bold text-caption"
                @click="printSheetMode = 'blank'"
              >
                ورقة الطالب
              </v-btn>
              <v-btn
                size="small"
                :variant="printSheetMode === 'key' ? 'flat' : 'text'"
                :color="printSheetMode === 'key' ? 'secondary' : undefined"
                class="font-weight-bold text-caption"
                @click="printSheetMode = 'key'"
              >
                المفتاح المظلل
              </v-btn>
            </div>

            <!-- Print Action Button -->
            <custom-btn
              label="طباعة الآن"
              icon="mdi-printer"
              color="primary"
              class="font-weight-bold px-4"
              :click="triggerPrint"
            />

            <!-- Close Dialog -->
            <v-btn icon="mdi-close" variant="text" size="small" @click="printPreviewDialog = false" />
          </div>
        </div>

        <!-- Scrollable Paper Body -->
        <v-card-text class="pa-4 pa-md-8 print-modal-body overflow-y-auto" style="background-color: #f1f5f9;">
          <div class="printable-exam-sheet pa-8 pa-md-10 rounded-2xl mx-auto" v-if="selectedExam">
            <!-- Exam Paper Header -->
            <div class="exam-paper-header mb-6 pb-4 border-b text-center">
              <div class="text-caption text-medium-emphasis mb-1 font-weight-bold">{{ ministryHeading }}</div>
              <h2 class="text-h4 font-weight-black mb-2">{{ selectedExam?.title }}</h2>
              <div class="text-subtitle-1 font-weight-bold text-primary mb-3" v-if="printModalType === 'key'">
                نموذج مفتاح الإجابة الرسمي المعتمد
              </div>
              <div class="text-subtitle-1 font-weight-bold text-teal mb-3" v-else-if="printModalType === 'sheets'">
                {{ printSheetMode === 'key' ? 'مفتاح الإجابة المظلل الآلي (Bubble Sheet Key)' : 'ورقة إجابة الطالب الآلية (Bubble Sheet Answer Sheet)' }}
              </div>

              <div class="d-flex justify-center flex-wrap gap-3 text-body-2 font-weight-bold mb-3">
                <span class="paper-badge"><strong>المادة:</strong> {{ selectedExam?.subjectName || '-' }}</span>
                <span class="paper-badge" v-if="selectedExam?.yearName && selectedExam.yearName !== '-'"><strong>العام الدراسي:</strong> {{ selectedExam.yearName }}</span>
                <span class="paper-badge"><strong>النموذج:</strong> {{ printVersion?.versionCode || 'A' }}</span>
                <span class="paper-badge" v-if="printModalType !== 'sheets'"><strong>الدرجة الكلية:</strong> {{ printTotalScore }}</span>
                <span class="paper-badge" v-if="printModalType === 'questions'"><strong>الزمن:</strong> ساعتان</span>
              </div>

              <!-- Student Header Box for Questions -->
              <div v-if="printModalType === 'questions'" class="student-info-box pa-3 rounded-xl border d-flex justify-space-between align-center flex-wrap gap-4 text-body-2 mt-4">
                <div class="flex-grow-1 text-start">
                  اسم الطالب: <span class="dotted-underline flex-grow-1 d-inline-block" style="min-width: 250px;"></span>
                </div>
                <div>
                  رقم الجلوس: <span class="dotted-underline d-inline-block" style="min-width: 120px;"></span>
                </div>
                <div>
                  المدرسة: <span class="dotted-underline d-inline-block" style="min-width: 150px;"></span>
                </div>
              </div>

              <!-- Bubble Sheet Header Box -->
              <div v-else-if="printModalType === 'sheets'" class="mt-4 pt-2 border-t text-start">
                <v-row align="center">
                  <v-col cols="8">
                    <div class="d-flex align-center mb-2">
                      <span class="font-weight-bold me-2">اسم الطالب:</span>
                      <div class="dotted-underline flex-grow-1"></div>
                    </div>
                    <div class="d-flex align-center">
                      <span class="font-weight-bold me-2">المدرسة / المركز:</span>
                      <div class="dotted-underline flex-grow-1 me-4"></div>
                      <span class="font-weight-bold me-2">رقم الجلوس:</span>
                      <div class="dotted-underline flex-grow-1"></div>
                    </div>
                  </v-col>
                  <v-col cols="4" class="text-left">
                    <div class="box-border pa-2 text-center rounded-lg border">
                      <span class="text-caption font-weight-bold d-block mb-1">الرقم الأكاديمي / السري</span>
                      <div class="id-grid justify-center d-flex gap-1">
                        <div v-for="n in 6" :key="n" class="id-box"></div>
                      </div>
                    </div>
                  </v-col>
                </v-row>
              </div>
            </div>

            <!-- Content Type 1: Questions Paper -->
            <div v-if="printModalType === 'questions'" class="questions-list d-flex flex-column gap-6">
              <div
                v-for="(q, index) in printQuestions"
                :key="q.id || index"
                class="print-q-card pa-4 rounded-xl border mb-4"
              >
                <div class="d-flex align-start gap-3">
                  <div class="q-number-badge font-weight-black flex-shrink-0">
                    {{ index + 1 }}
                  </div>
                  <div class="flex-grow-1">
                    <div class="d-flex justify-space-between align-center mb-2">
                      <div class="text-body-1 font-weight-bold" v-html="q.content"></div>
                      <span class="paper-badge ms-2 text-caption">{{ q.assignedMark }} درجة</span>
                    </div>
                    <div v-if="q.options && q.options.length" class="mt-3">
                      <v-row dense>
                        <v-col
                          v-for="(opt, optIdx) in q.options"
                          :key="opt.id || optIdx"
                          cols="12"
                          sm="6"
                        >
                          <div class="option-pill pa-2 rounded-lg d-flex align-center gap-2 mb-1">
                            <span class="option-circle">{{ ['أ', 'ب', 'ج', 'د'][optIdx] || (optIdx + 1) }}</span>
                            <span class="text-body-2">{{ opt.text }}</span>
                          </div>
                        </v-col>
                      </v-row>
                    </div>
                  </div>
                </div>
              </div>
              <div v-if="printQuestions.length === 0" class="text-center text-medium-emphasis pa-8">
                لا توجد أسئلة مسجلة في هذا النموذج.
              </div>
            </div>

            <!-- Content Type 2: Answer Key -->
            <div v-else-if="printModalType === 'key'" class="answer-key-content">
              <v-table density="comfortable" class="answer-key-table mb-8 border rounded-xl overflow-hidden">
                <thead>
                  <tr class="bg-slate-100">
                    <th class="text-center font-weight-black" style="width: 80px;">#</th>
                    <th class="text-center font-weight-black" style="width: 140px;">الخيار الصحيح</th>
                    <th class="font-weight-black">نص الإجابة الصحيحة</th>
                    <th class="text-center font-weight-black" style="width: 100px;">الدرجة</th>
                    <th class="text-center font-weight-black" style="width: 140px;">المستوى المعرفي</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(q, index) in printQuestions" :key="q.id || index">
                    <td class="text-center font-weight-black">{{ index + 1 }}</td>
                    <td class="text-center">
                      <v-chip size="small" color="success" variant="tonal" class="font-weight-black">
                        {{ getCorrectOptionLabel(q) }}
                      </v-chip>
                    </td>
                    <td class="font-weight-medium">{{ getCorrectOptionText(q) }}</td>
                    <td class="text-center font-weight-bold">{{ q.assignedMark }}</td>
                    <td class="text-center text-caption text-medium-emphasis">{{ q.bloomLevel || '-' }}</td>
                  </tr>
                </tbody>
                <tfoot v-if="printQuestions.length">
                  <tr class="bg-slate-50 font-weight-black">
                    <td colspan="3" class="text-end">إجمالي درجات النموذج</td>
                    <td class="text-center text-primary">{{ printTotalScore }}</td>
                    <td></td>
                  </tr>
                </tfoot>
              </v-table>

              <!-- Signatures -->
              <div class="mt-12 pt-6 border-t border-slate-300">
                <v-row>
                  <v-col cols="4" class="text-center">
                    <p class="font-weight-bold mb-3">توقيع واضع الاختبار</p>
                    <div class="signature-line mx-auto" style="width: 180px; border-bottom: 1px dashed #64748b; height: 30px;"></div>
                  </v-col>
                  <v-col cols="4" class="text-center">
                    <p class="font-weight-bold mb-3">توقيع المراجع والمدقق</p>
                    <div class="signature-line mx-auto" style="width: 180px; border-bottom: 1px dashed #64748b; height: 30px;"></div>
                  </v-col>
                  <v-col cols="4" class="text-center">
                    <p class="font-weight-bold mb-3">اعتماد مدير الاختبارات</p>
                    <div class="signature-line mx-auto" style="width: 180px; border-bottom: 1px dashed #64748b; height: 30px;"></div>
                  </v-col>
                </v-row>
              </div>
            </div>

            <!-- Content Type 3: Bubble Sheets (OMR) -->
            <div v-else-if="printModalType === 'sheets'" class="bubble-sheets-content">
              <!-- Instruction Banner -->
              <div class="d-flex align-center justify-space-between mb-4 pa-3 rounded-xl border bg-slate-50 flex-wrap gap-2">
                <div class="d-flex align-center gap-2 text-caption font-weight-bold">
                  <v-icon size="18" color="primary">mdi-information-outline</v-icon>
                  <span>طريقة التظليل الصحيحة: ظلل الدائرة بالكامل بلون داكن. لا تثني الورقة ولا تضع أي علامات عشوائية.</span>
                </div>
                <div class="d-flex align-center gap-3 text-caption font-weight-bold">
                  <span class="d-flex align-center gap-1">صحيح: <span class="bubble-circle bubble-filled d-inline-flex" style="width: 18px; height: 18px; font-size: 10px;">●</span></span>
                  <span class="d-flex align-center gap-1 text-medium-emphasis">خاطئ: <span class="bubble-circle d-inline-flex" style="width: 18px; height: 18px; font-size: 10px;">✕</span></span>
                </div>
              </div>

              <!-- Bubble Grid Columns -->
              <div class="bubble-grid-container py-4">
                <div
                  v-for="(colQuestions, colIndex) in printBubbleColumns"
                  :key="colIndex"
                  class="bubble-column pa-3 rounded-xl border mb-3"
                >
                  <div
                    v-for="q in colQuestions"
                    :key="q.num"
                    class="bubble-row d-flex align-center justify-space-between mb-2 gap-3"
                  >
                    <span class="q-num font-weight-black text-caption">{{ q.num }}</span>
                    <div class="bubbles d-flex gap-2">
                      <div
                        v-for="(opt, optIdx) in (q.questionType === 'صح وخطأ' ? ['أ', 'ب'] : ['أ', 'ب', 'ج', 'د'])"
                        :key="opt"
                        class="bubble-item text-center"
                      >
                        <div
                          class="bubble-circle font-weight-bold"
                          :class="{ 'bubble-filled': printSheetMode === 'key' && q.correctIndex === optIdx }"
                        >
                          {{ opt }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="printQuestions.length === 0" class="text-center text-medium-emphasis pa-8">
                لا توجد أسئلة مسجلة لتوليد ورقة التظليل.
              </div>

              <!-- Footer -->
              <div class="mt-8 pt-4 border-t border-slate-300 d-flex justify-space-between text-caption text-medium-emphasis">
                <span>نظام بنك الأسئلة والتصحيح الآلي المعتمد (OMR)</span>
                <span>كود التحقق: {{ selectedExam?.uniqueCode }} • نموذج {{ printVersion?.versionCode || 'A' }}</span>
              </div>
            </div>

          </div>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- MODAL: EXAM DETAILS & GEOGRAPHIC SCOPE (زر العين) -->
    <v-dialog v-model="detailsDialog" max-width="750" scrollable>
      <v-card class="rounded-2xl overflow-hidden shadow-2xl">
        <!-- Header -->
        <div class="pa-5 bg-surface border-b d-flex align-center justify-space-between">
          <div class="d-flex align-center gap-3">
            <v-avatar :color="inspectingExam?.institutionTypeColor || 'info'" variant="tonal" size="44" class="rounded-xl">
              <v-icon size="24">{{ inspectingExam?.institutionTypeIcon || 'mdi-text-box-search-outline' }}</v-icon>
            </v-avatar>
            <div>
              <div class="d-flex align-center gap-2 flex-wrap">
                <h3 class="text-h6 font-weight-black mb-0 text-slate-800">{{ inspectingExam?.title }}</h3>
                <v-chip
                  size="small"
                  :color="inspectingExam?.institutionTypeColor"
                  variant="flat"
                  class="font-weight-bold"
                >
                  <v-icon start size="15">{{ inspectingExam?.institutionTypeIcon }}</v-icon>
                  {{ inspectingExam?.institutionTypeFullLabel }}
                </v-chip>
              </div>
              <div class="text-caption text-medium-emphasis mt-1">
                رمز الاختبار: <span class="font-weight-bold font-mono">{{ inspectingExam?.uniqueCode || '—' }}</span>
                <span class="mx-2">•</span>
                المادة: <span class="font-weight-bold text-slate-700">{{ inspectingExam?.subjectName }}</span>
                <span class="mx-2">•</span>
                الجهة: <span class="font-weight-bold" :class="`text-${inspectingExam?.institutionTypeColor}`">{{ inspectingExam?.institutionTypeMinistry }}</span>
              </div>
            </div>
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" @click="detailsDialog = false" />
        </div>

        <!-- Content -->
        <v-card-text class="pa-5 overflow-y-auto" style="max-height: 70vh;">
          <v-row dense>
            <!-- 1. النطاق الجغرافي والمناطق المستهدفة -->
            <v-col cols="12">
              <v-card variant="outlined" class="rounded-xl pa-4 mb-4 border-slate-200 bg-slate-50">
                <div class="d-flex align-center gap-2 mb-3">
                  <v-icon color="primary" size="20">mdi-map-marker-radius</v-icon>
                  <h4 class="text-subtitle-1 font-weight-black text-slate-800">النطاق الجغرافي والمناطق المستهدفة</h4>
                </div>

                <v-row dense>
                  <v-col cols="12" sm="6" md="4">
                    <div class="detail-box pa-2 bg-white rounded-lg border">
                      <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">المحافظة</div>
                      <div class="font-weight-bold text-body-2 text-primary d-flex align-center gap-1">
                        <v-icon size="16">mdi-city-variant-outline</v-icon>
                        {{ inspectingExam?.governorateName || '—' }}
                      </div>
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6" md="4">
                    <div class="detail-box pa-2 bg-white rounded-lg border">
                      <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">المديرية</div>
                      <div class="font-weight-bold text-body-2 text-teal d-flex align-center gap-1">
                        <v-icon size="16">mdi-map-marker-outline</v-icon>
                        {{ inspectingExam?.directorateName || '—' }}
                      </div>
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6" md="4">
                    <div class="detail-box pa-2 bg-white rounded-lg border">
                      <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">المنطقة / العزلة</div>
                      <div class="font-weight-bold text-body-2 text-slate-700 d-flex align-center gap-1">
                        <v-icon size="16">mdi-compass-outline</v-icon>
                        {{ inspectingExam?.regionName || '—' }}
                      </div>
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6" md="6" class="mt-2">
                    <div class="detail-box pa-2 bg-white rounded-lg border">
                      <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">مستوى الاستهداف</div>
                      <div class="font-weight-bold text-body-2 text-indigo">
                        {{ inspectingExam?.targetScopeDisplay || 'شامل لكافة المدارس' }}
                      </div>
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6" md="6" class="mt-2">
                    <div class="detail-box pa-2 bg-white rounded-lg border">
                      <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">الدولة</div>
                      <div class="font-weight-bold text-body-2 text-slate-700">
                        {{ inspectingExam?.countryName || 'الجمهورية اليمنية' }}
                      </div>
                    </div>
                  </v-col>
                </v-row>

                <!-- تفاصيل النطاقات المستهدفة (إذا كانت مدارس أو جهات محددة) -->
                <div v-if="inspectingExam?.targetedScopesSummary?.targets?.length" class="mt-4 pt-3 border-t">
                  <div class="text-caption font-weight-bold text-slate-700 mb-2">
                    الجهات والمدارس المحددة المستهدفة:
                  </div>
                  <div class="d-flex flex-wrap gap-2">
                    <v-chip
                      v-for="(target, idx) in inspectingExam.targetedScopesSummary.targets"
                      :key="idx"
                      size="small"
                      color="indigo"
                      variant="tonal"
                      class="font-weight-bold"
                    >
                      <v-icon start size="14">
                        {{ target.scope_level === 'school' ? 'mdi-school' : 'mdi-domain' }}
                      </v-icon>
                      {{ target.name }}
                      <span class="text-caption ms-1 opacity-75">({{ target.scope_level_display }})</span>
                    </v-chip>
                  </div>
                </div>
              </v-card>
            </v-col>

            <!-- 2. البيانات الأكاديمية والتعليمية -->
            <v-col cols="12">
              <v-card variant="outlined" class="rounded-xl pa-4 mb-4 border-slate-200">
                <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3">
                  <div class="d-flex align-center gap-2">
                    <v-icon :color="inspectingExam?.institutionTypeColor || 'success'" size="20">
                      {{ inspectingExam?.institutionTypeIcon || 'mdi-school-outline' }}
                    </v-icon>
                    <h4 class="text-subtitle-1 font-weight-black text-slate-800">البيانات الأكاديمية والتعليمية</h4>
                  </div>
                  <v-chip
                    size="small"
                    :color="inspectingExam?.institutionTypeColor"
                    variant="tonal"
                    class="font-weight-bold"
                  >
                    <v-icon start size="14">{{ inspectingExam?.institutionTypeIcon }}</v-icon>
                    {{ inspectingExam?.institutionTypeFullLabel }}
                  </v-chip>
                </div>

                <!-- بطاقة مميزة لتحديد تصنيف المؤسسة والوزارة -->
                <div
                  class="pa-3 rounded-lg border mb-3 d-flex align-center justify-space-between flex-wrap gap-2"
                  :style="`background-color: ${inspectingExam?.institutionTypeBg || '#f8fafc'}; border-color: ${inspectingExam?.institutionTypeBorder || '#e2e8f0'} !important;`"
                >
                  <div class="d-flex align-center gap-3">
                    <v-avatar size="36" :color="inspectingExam?.institutionTypeColor" variant="tonal" class="rounded-lg">
                      <v-icon size="20">{{ inspectingExam?.institutionTypeIcon }}</v-icon>
                    </v-avatar>
                    <div>
                      <div class="text-caption text-medium-emphasis">تصنيف المؤسسة التعليمية</div>
                      <div class="font-weight-black text-body-2" :class="`text-${inspectingExam?.institutionTypeColor}`">
                        {{ inspectingExam?.institutionTypeFullLabel }}
                      </div>
                    </div>
                  </div>
                  <div class="text-caption font-weight-bold text-medium-emphasis">
                    {{ inspectingExam?.institutionTypeMinistry }}
                  </div>
                </div>

                <v-row dense>
                  <v-col cols="12" sm="6" md="4">
                    <div class="detail-box pa-2 bg-slate-50 rounded-lg">
                      <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">المادة الدراسية</div>
                      <div class="font-weight-bold text-body-2">{{ inspectingExam?.subjectName || '—' }}</div>
                    </div>
                  </v-col>

                  <!-- الحقول المدرسية إذا كان مدرسي -->
                  <template v-if="inspectingExam?.institutionType === 'school' || !inspectingExam?.institutionType">
                    <v-col cols="12" sm="6" md="4">
                      <div class="detail-box pa-2 bg-slate-50 rounded-lg">
                        <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">المرحلة الدراسية</div>
                        <div class="font-weight-bold text-body-2">{{ inspectingExam?.stageName || '—' }}</div>
                      </div>
                    </v-col>

                    <v-col cols="12" sm="6" md="4">
                      <div class="detail-box pa-2 bg-slate-50 rounded-lg">
                        <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">الصف / الشعبة</div>
                        <div class="font-weight-bold text-body-2">{{ inspectingExam?.classTrackName || '—' }}</div>
                      </div>
                    </v-col>
                  </template>

                  <!-- الحقول الجامعية إذا كان جامعي -->
                  <template v-else-if="inspectingExam?.institutionType === 'university'">
                    <v-col cols="12" sm="6" md="4">
                      <div class="detail-box pa-2 bg-slate-50 rounded-lg">
                        <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">تصنيف التعليم</div>
                        <div class="font-weight-bold text-body-2 text-purple-darken-1">تعليم جامعي (أكاديمي)</div>
                      </div>
                    </v-col>

                    <v-col cols="12" sm="6" md="4">
                      <div class="detail-box pa-2 bg-slate-50 rounded-lg">
                        <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">المقرر الجامعي</div>
                        <div class="font-weight-bold text-body-2">{{ inspectingExam?.subjectName || '—' }}</div>
                      </div>
                    </v-col>
                  </template>

                  <!-- الحقول المهنية إذا كان معهد -->
                  <template v-else-if="inspectingExam?.institutionType === 'institute'">
                    <v-col cols="12" sm="6" md="4">
                      <div class="detail-box pa-2 bg-slate-50 rounded-lg">
                        <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">تصنيف التعليم</div>
                        <div class="font-weight-bold text-body-2 text-teal-darken-1">معاهد وتدريب مهني وتقني</div>
                      </div>
                    </v-col>

                    <v-col cols="12" sm="6" md="4">
                      <div class="detail-box pa-2 bg-slate-50 rounded-lg">
                        <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">المادة / المسار التدريبي</div>
                        <div class="font-weight-bold text-body-2">{{ inspectingExam?.subjectName || '—' }}</div>
                      </div>
                    </v-col>
                  </template>

                  <v-col cols="12" sm="6" md="6" class="mt-2">
                    <div class="detail-box pa-2 bg-slate-50 rounded-lg">
                      <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">العام الدراسي</div>
                      <div class="font-weight-bold text-body-2">{{ inspectingExam?.yearName || inspectingExam?.year_name || '—' }}</div>
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6" md="6" class="mt-2">
                    <div class="detail-box pa-2 bg-slate-50 rounded-lg">
                      <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">الفترة / الفصل الدراسي</div>
                      <div class="font-weight-bold text-body-2">{{ inspectingExam?.period || inspectingExam?.period_name || '—' }}</div>
                    </div>
                  </v-col>
                </v-row>
              </v-card>
            </v-col>

            <!-- 3. الجدولة وإعدادات النماذج -->
            <v-col cols="12">
              <v-card variant="outlined" class="rounded-xl pa-4 border-slate-200">
                <div class="d-flex align-center gap-2 mb-3">
                  <v-icon color="warning" size="20">mdi-clock-outline</v-icon>
                  <h4 class="text-subtitle-1 font-weight-black text-slate-800">بيانات الجدولة وتكوين الاختبار</h4>
                </div>

                <v-row dense>
                  <v-col cols="12" sm="6" md="4">
                    <div class="detail-box pa-2 bg-slate-50 rounded-lg">
                      <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">تاريخ الاختبار</div>
                      <div class="font-weight-bold text-body-2">{{ inspectingExam?.scheduleDate || 'غير محدد' }}</div>
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6" md="4">
                    <div class="detail-box pa-2 bg-slate-50 rounded-lg">
                      <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">مدة الاختبار</div>
                      <div class="font-weight-bold text-body-2">{{ inspectingExam?.scheduleDuration || 'غير محدد' }}</div>
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6" md="4">
                    <div class="detail-box pa-2 bg-slate-50 rounded-lg">
                      <div class="text-caption text-medium-emphasis mb-1 font-weight-medium">نمط توزيع النماذج</div>
                      <div class="font-weight-bold text-body-2">{{ inspectingExam?.models_mode_display || 'افتراضي' }}</div>
                    </div>
                  </v-col>

                  <v-col cols="12" class="mt-2">
                    <div class="detail-box pa-3 bg-slate-50 rounded-lg d-flex align-center justify-space-between flex-wrap gap-2">
                      <div class="d-flex align-center gap-2">
                        <span class="text-caption text-medium-emphasis font-weight-medium">النماذج المتوفرة:</span>
                        <div class="d-flex gap-1">
                          <v-chip
                            v-for="ver in (inspectingExam?.versionsList || [])"
                            :key="ver.id || ver.versionCode"
                            size="x-small"
                            color="primary"
                            variant="flat"
                            class="font-weight-bold"
                          >
                            نموذج {{ ver.versionCode }}
                          </v-chip>
                        </div>
                      </div>
                      <div class="d-flex align-center gap-3">
                        <span class="text-caption font-weight-bold text-slate-700">
                          <v-icon size="14" color="indigo" class="me-1">mdi-help-circle-outline</v-icon>
                          {{ inspectingExam?.questionsCount || 0 }} سؤال
                        </span>
                        <span class="text-caption font-weight-bold text-slate-700">
                          <v-icon size="14" color="success" class="me-1">mdi-account-group</v-icon>
                          {{ inspectingExam?.studentsCount || 0 }} طالب
                        </span>
                      </div>
                    </div>
                  </v-col>
                </v-row>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>

        <!-- Dialog Footer Actions -->
        <div class="pa-4 bg-slate-50 border-t d-flex align-center justify-space-between">
          <v-btn variant="text" color="grey-darken-1" class="font-weight-bold" @click="detailsDialog = false">
            إغلاق
          </v-btn>
          <div class="d-flex align-center gap-2">
            <v-btn
              variant="tonal"
              color="purple-darken-1"
              rounded="lg"
              class="font-weight-bold"
              prepend-icon="mdi-scanner"
              :to="`/omr-exams?open_exam_id=${inspectingExam?.id}`"
            >
              شاشة التصحيح (OMR)
            </v-btn>
            <custom-btn
              label="فتح لوحة التحكم"
              icon="monitor-dashboard"
              color="primary"
              class="font-weight-bold"
              :click="() => viewExamFromModal(inspectingExam)"
            />
          </div>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { examsService } from '@/services/examsService'
import { academicService } from '@/services/academicService'
import { bankService } from '@/services/bankService'

export default {
  name: 'ExamArchiveView',

  computed: {
    filterInstituteSpecParam() {
      const p = {}
      if (this.filterInstituteField) p.field = this.filterInstituteField
      if (this.filterInstituteEducationSystem) p.education_system = this.filterInstituteEducationSystem
      return Object.keys(p).length ? p : null
    },

    subjectFilterParam() {
      const p = {}
      if (this.filterInstitutionType && this.filterInstitutionType !== 'all') {
        p.institution_type = this.filterInstitutionType
      }
      if (this.filterInstitutionType === 'school') {
        if (this.filterClassTrack) {
          p.class_track = this.filterClassTrack
        } else if (this.filterStage) {
          p.stage = this.filterStage
        }
      } else if (this.filterInstitutionType === 'university') {
        if (this.filterSemesterSubject) {
          p.semester_subject = this.filterSemesterSubject
        } else if (this.filterSpecialization) {
          p.specialization = this.filterSpecialization
        } else if (this.filterDepartment) {
          p.department = this.filterDepartment
        } else if (this.filterCollege) {
          p.college = this.filterCollege
        }
      }
      return Object.keys(p).length > 0 ? p : null
    },

    activeVersion() {
      if (!this.examDetails || !this.examDetails.versions || !this.examDetails.versions.length) return null
      return this.examDetails.versions[this.activeVersionIndex] || this.examDetails.versions[0]
    },

    activeVersionQuestions() {
      if (!this.activeVersion) return []
      return this.activeVersion.questions || []
    },

    versionTotalScore() {
      return this.activeVersionQuestions.reduce((sum, q) => sum + (Number(q.assignedMark) || 0), 0)
    },

    selectedSetting() {
      return this.examDashboardData?.setting || null
    },

    difficultyBars() {
      if (!this.selectedSetting) return []
      return [
        { label: 'سهل', pct: this.selectedSetting.easyPercentage || 0, color: 'success' },
        { label: 'متوسط', pct: this.selectedSetting.mediumPercentage || 0, color: 'warning' },
        { label: 'صعب', pct: this.selectedSetting.hardPercentage || 0, color: 'error' },
      ]
    },

    studentsVersionOptions() {
      const options = [{ text: 'جميع النماذج', value: 'all' }]
      if (this.selectedExam && this.selectedExam.versionsList) {
        this.selectedExam.versionsList.forEach(v => {
          options.push({ text: `نموذج ${v.versionCode}`, value: v.versionCode })
        })
      }
      return options
    },

    printVersion() {
      if (!this.examDetails || !this.examDetails.versions || !this.examDetails.versions.length) return null
      return this.examDetails.versions[this.printVersionIndex] || this.examDetails.versions[0]
    },

    printQuestions() {
      if (!this.printVersion) return []
      return this.printVersion.questions || []
    },

    printTotalScore() {
      return this.printQuestions.reduce((sum, q) => sum + (Number(q.assignedMark) || 0), 0)
    },

    printBubbleColumns() {
      const qs = this.printQuestions || []
      if (qs.length === 0) return []

      const items = qs.map((q, idx) => {
        let correctIndex = -1
        if (q.options && q.options.length) {
          correctIndex = q.options.findIndex(o => o.isTrue)
        } else if (q.questionType === 'صح وخطأ') {
          correctIndex = q.isTrue ? 0 : 1
        }
        return {
          num: idx + 1,
          correctIndex,
          assignedMark: q.assignedMark || 1,
          questionType: q.questionType
        }
      })

      const perCol = 20
      const cols = []
      for (let i = 0; i < items.length; i += perCol) {
        cols.push(items.slice(i, i + perCol))
      }
      return cols
    },

    ministryHeading() {
      if (this.selectedExam?.institution_type === 'institute') {
        return 'الجمهورية اليمنية - وزارة التعليم الفني والتدريب المهني'
      }
      if (this.selectedExam?.institution_type === 'university') {
        return 'الجمهورية اليمنية - وزارة التعليم العالي والبحث العلمي'
      }
      return 'الجمهورية اليمنية - وزارة التربية والتعليم والبحث العلمي'
    },

    registeredStudents() {
      return this.studentsTableItems?.results || []
    },
  },

  watch: {
    studentsFilterVersion() {
      this.fetchRegisteredStudents({ params: { page: 1 } })
    },
  },

  data() {
    return {
      loading: false,
      items: { results: [], pagination: {} },
      examDetails: null,
      detailsDialog: false,
      inspectingExam: null,
      // Filters
      filterInstitutionType: null,
      institutionTypeOptions: [
        { text: "تعليم مدرسي", value: "school", icon: "mdi-school" },
        { text: "تعليم جامعي", value: "university", icon: "mdi-domain" },
        { text: "معاهد وتدريب مهني", value: "institute", icon: "mdi-tools" },
      ],
      filterCollege: null,
      filterDepartment: null,
      filterSpecialization: null,
      filterSemesterSubject: null,
      filterInstituteField: null,
      filterInstituteEducationSystem: null,
      filterInstituteSpecialization: null,
      filterInstituteCurriculum: null,
      filterInstituteSubject: null,
      filterSubject: null,
      filterStage: null,
      filterClassTrack: null,
      filterPeriod: null,
      searchQuery: '',
      headers: [
        { title: 'عنوان الاختبار', key: 'title', sortable: true },
        { title: 'نوع المؤسسة', key: 'institutionType', sortable: false, align: 'center' },
        { title: 'النماذج', key: 'versionCode', sortable: false },
        { title: 'عدد الأسئلة', key: 'questionsCount', sortable: false, align: 'center' },
        { title: 'الطلاب المسجلون', key: 'studentsCount', sortable: false, align: 'center' },
      ],
      selectedExam: null,
      dashboardTab: 0,
      activeVersionIndex: 0,
      versionSubTab: 0,
      // Students
      studentsTableItems: { results: [], pagination: { count: 0, num_pages: 1, current_page: 1, page_size: 10 } },
      loadingStudents: false,
      studentsFilterVersion: 'all',
      totalStudentsCount: 0,
      backendUniqueSchoolsCount: 0,
      examDashboardData: null,
      studentsHeaders: [
        { title: 'اسم الطالب', key: 'studentName', sortable: true },
        { title: 'الرقم الأكاديمي', key: 'academicNumber', align: 'center', sortable: true },
        { title: 'رقم الجلوس', key: 'seatNumber', align: 'center', sortable: true },
        { title: 'الرقم السري', key: 'secretNumber', align: 'center', sortable: true },
        { title: 'النموذج', key: 'versionCode', align: 'center', sortable: true },
        { title: 'المدرسة', key: 'schoolName', sortable: true },
        { title: 'المديرية', key: 'directorateName', sortable: true },
      ],
      // Print Dialog
      printPreviewDialog: false,
      printModalType: 'questions', // 'questions' | 'key' | 'sheets'
      printVersionIndex: 0,
      printSheetMode: 'blank', // 'blank' | 'key'
    }
  },

  async created() {
    await this.getData()
  },

  methods: {

    async getData(tableParams = null) {
      this.loading = true
      try {
        let queryParams = {}
        if (tableParams && tableParams.params) {
          queryParams = { ...tableParams.params, hasPagination: true }
        } else {
          queryParams = { page: 1, perPage: 12, hasPagination: true }
        }

        if (this.filterInstitutionType && this.filterInstitutionType !== 'all') queryParams.institution_type = this.filterInstitutionType
        if (this.filterCollege) queryParams.college = this.filterCollege
        if (this.filterDepartment) queryParams.department = this.filterDepartment
        if (this.filterSpecialization) queryParams.specialization = this.filterSpecialization
        if (this.filterSemesterSubject) queryParams.semester_subject = this.filterSemesterSubject
        if (this.filterInstituteSubject) queryParams.institute_subject = this.filterInstituteSubject
        if (this.filterInstituteField) queryParams.institute_field = this.filterInstituteField
        if (this.filterSubject) queryParams.subject = this.filterSubject
        if (this.filterStage) queryParams.stage = this.filterStage
        if (this.filterClassTrack) queryParams.class_track = this.filterClassTrack
        if (this.filterPeriod) queryParams.period = this.filterPeriod
        if (this.searchQuery) queryParams.search = this.searchQuery

        const response = await this.$axios.get('api/exams/exam-archive/', { params: queryParams })

        const raw = response.data || {}
        const results = raw.results || (raw.data && raw.data.results) || []

        const getInstitutionTypeMeta = (type) => {
          if (type === 'university') {
            return {
              shortLabel: 'جامعة',
              fullLabel: 'تعليم جامعي (جامعة)',
              icon: 'mdi-domain',
              color: 'purple-darken-1',
              ministry: 'وزارة التعليم العالي والبحث العلمي',
              bg: '#faf5ff',
              border: '#e9d5ff',
            }
          }
          if (type === 'institute') {
            return {
              shortLabel: 'معهد مهني',
              fullLabel: 'معاهد وتدريب مهني (معهد)',
              icon: 'mdi-tools',
              color: 'teal-darken-1',
              ministry: 'وزارة التعليم الفني والتدريب المهني',
              bg: '#f0fdfa',
              border: '#ccfbf1',
            }
          }
          return {
            shortLabel: 'مدرسة',
            fullLabel: 'تعليم مدرسي (مدرسة)',
            icon: 'mdi-school',
            color: 'primary',
            ministry: 'وزارة التربية والتعليم والبحث العلمي',
            bg: '#eff6ff',
            border: '#dbeafe',
          }
        }

        const enriched = results.map(exam => {
          const instMeta = getInstitutionTypeMeta(exam.institution_type)
          return {
            ...exam,
            subjectName: exam.subject_name || 'عام',
            yearName: exam.year_name || (exam.year && exam.year.name_ar) || '-',
            versionsList: exam.versions_list || [],
            questionsCount: exam.questions_count || 0,
            studentsCount: exam.students_count ?? exam.studentsCount ?? 0,
            institutionType: exam.institution_type || 'school',
            institutionTypeShortLabel: instMeta.shortLabel,
            institutionTypeFullLabel: instMeta.fullLabel,
            institutionTypeIcon: instMeta.icon,
            institutionTypeColor: instMeta.color,
            institutionTypeMinistry: instMeta.ministry,
            institutionTypeBg: instMeta.bg,
            institutionTypeBorder: instMeta.border,
            governorateName: exam.governorate_name || '—',
            directorateName: exam.directorate_name || '—',
            regionName: exam.region_name || '—',
            countryName: exam.country_name || 'الجمهورية اليمنية',
            stageName: exam.stage_name || '—',
            classTrackName: exam.class_track_name || '—',
            scheduleDate: exam.schedule_date || '—',
            scheduleDuration: exam.schedule_duration ? `${exam.schedule_duration} دقيقة` : '—',
            targetScopeDisplay: exam.target_scope_level_display || '—',
            targetedScopesSummary: exam.targeted_scopes_summary || null,
          }
        })

        this.items = Object.assign({}, raw, { results: enriched })
      } catch (err) {
        console.error('فشل تحميل الاختبارات:', err)
      } finally {
        this.loading = false
      }
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
      this.getData()
    },

    onCollegeChange() {
      this.filterDepartment = null
      this.filterSpecialization = null
      this.filterSemesterSubject = null
    },

    onStageChange() {
      this.filterClassTrack = null
    },

    applyFilters() { this.getData() },

    resetFilters() {
      this.filterInstitutionType = null
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
      this.filterStage = null
      this.filterClassTrack = null
      this.filterPeriod = null
      this.searchQuery = ''
      this.getData()
    },

    openExamDetailsModal(exam) {
      this.inspectingExam = exam
      this.detailsDialog = true
    },

    viewExamFromModal(exam) {
      this.detailsDialog = false
      if (exam) {
        this.openDashboard(exam)
      }
    },

    async openDashboard(exam) {
      this.selectedExam = exam
      this.dashboardTab = 0
      this.activeVersionIndex = 0
      this.versionSubTab = 0
      this.examDashboardData = null
      this.studentsFilterVersion = 'all'
      this.totalStudentsCount = exam.students_count ?? exam.studentsCount ?? 0
      this.backendUniqueSchoolsCount = 0
      this.studentsTableItems = { results: [], pagination: { count: 0, num_pages: 1, current_page: 1, page_size: 10 } }
      
      try {
        const details = await examsService.getExamModelsDetails(exam.id)
        this.examDetails = details
      } catch (err) {
        console.error("Failed to load exam details for dashboard", err)
      }

      // Load registered students via backend pagination
      await this.fetchRegisteredStudents()

      // Load dashboard data (for classTrack info etc.)
      try {
        const dashData = await examsService.getArchivedExamDashboard(exam.id)
        this.examDashboardData = dashData
      } catch (err) {
        console.error("Failed to load dashboard data", err)
      }
    },

    async fetchRegisteredStudents(tableParams = null) {
      if (!this.selectedExam?.id) return
      this.loadingStudents = true
      try {
        let queryParams = {}
        if (tableParams && tableParams.params) {
          queryParams = { ...tableParams.params, hasPagination: true }
        } else if (tableParams && typeof tableParams === 'object' && ('page' in tableParams || 'page_size' in tableParams)) {
          queryParams = { ...tableParams, hasPagination: true }
        } else {
          queryParams = { page: 1, page_size: 10, hasPagination: true }
        }

        if (this.studentsFilterVersion && this.studentsFilterVersion !== 'all') {
          queryParams.version = this.studentsFilterVersion
        }

        const res = await examsService.getExamRegisteredStudents(this.selectedExam.id, queryParams)
        const raw = res || {}
        const results = raw.results || raw.students || (raw.data && raw.data.results) || []
        const pagination = raw.pagination || {
          count: raw.totalStudents ?? raw.count ?? results.length,
          num_pages: raw.num_pages ?? 1,
          current_page: raw.current_page ?? (queryParams.page || 1),
          page_size: raw.page_size ?? (queryParams.page_size || 10),
        }

        this.studentsTableItems = {
          ...raw,
          results,
          pagination,
        }

        if (raw.totalStudents !== undefined) {
          this.totalStudentsCount = raw.totalStudents
        } else if (pagination.count !== undefined) {
          this.totalStudentsCount = pagination.count
        }

        if (raw.uniqueSchoolsCount !== undefined) {
          this.backendUniqueSchoolsCount = raw.uniqueSchoolsCount
        }
      } catch (err) {
        console.error("Failed to load registered students", err)
        this.studentsTableItems = { results: [], pagination: { count: 0, num_pages: 1, current_page: 1 } }
      } finally {
        this.loadingStudents = false
      }
    },

    closeDashboard() { 
      this.selectedExam = null 
      this.examDetails = null
      this.examDashboardData = null
      this.studentsFilterVersion = 'all'
      this.totalStudentsCount = 0
      this.backendUniqueSchoolsCount = 0
      this.studentsTableItems = { results: [], pagination: { count: 0, num_pages: 1, current_page: 1, page_size: 10 } }
      this.printPreviewDialog = false
    },

    openPrintDialog(type = 'questions') {
      this.printModalType = type
      this.printVersionIndex = this.activeVersionIndex || 0
      this.printSheetMode = type === 'key' ? 'key' : 'blank'
      this.printPreviewDialog = true
      if (!this.examDetails && this.selectedExam?.id) {
        examsService.getExamModelsDetails(this.selectedExam.id).then(details => {
          this.examDetails = details
        }).catch(err => console.error("Error loading exam details:", err))
      }
    },

    triggerPrint() {
      window.print()
    },

    goToExamPrint(exam, type) {
      this.openPrintDialog(type)
    },

    getCorrectOptionLabel(question) {
      const labels = ['أ', 'ب', 'ج', 'د']
      if (question.options && question.options.length) {
        const idx = question.options.findIndex(o => o.isTrue)
        if (idx >= 0) return labels[idx]
      }
      if (question.questionType === 'صح وخطأ') return question.isTrue ? 'أ (صواب)' : 'ب (خطأ)'
      return '?'
    },

    getCorrectOptionText(question) {
      if (question.options && question.options.length) {
        const correct = question.options.find(o => o.isTrue)
        if (correct) return correct.text
      }
      if (question.questionType === 'صح وخطأ') return question.isTrue ? 'صواب' : 'خطأ'
      return 'غير محدد'
    },
  },
}
</script>

<style scoped>
.exam-archive-page {
  color: rgb(var(--v-theme-on-surface));
}


.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.border-subtle {
  border: 1px solid rgba(var(--v-border-color), 0.12);
  background: rgb(var(--v-theme-background));
}

.question-preview-box {
  background: rgb(var(--v-theme-background));
  border: 1px solid rgba(var(--v-border-color), 0.12);
}

.option-badge {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1.5px solid currentColor;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.premium-list-item {
  border-radius: 8px !important;
  margin-bottom: 2px;
}

.premium-list-item:hover {
  background: rgba(var(--v-theme-primary), 0.06) !important;
}

.gap-1 {
  gap: 4px;
}

.gap-2 {
  gap: 8px;
}

.gap-3 {
  gap: 12px;
}

.gap-4 {
  gap: 16px;
}

/* Printable Sheet & Preview Dialog Styles */
.print-modal-body {
  background-color: #f1f5f9;
}

.printable-exam-sheet {
  background: #ffffff;
  color: #0f172a;
  max-width: 900px;
  width: 100%;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
}

.paper-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  font-size: 0.85rem;
  color: #334155;
}

.student-info-box {
  background: #f8fafc;
  border-color: #e2e8f0;
}

.q-number-badge {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #0284c7;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
}

.option-pill {
  border: 1px solid #e2e8f0;
  background: #f8fafc;
}

.option-circle {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 1.5px solid #0284c7;
  color: #0284c7;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: bold;
}

.dotted-underline {
  border-bottom: 1.5px dotted #94a3b8;
  height: 16px;
}

/* Bubble Sheets */
.bubble-grid-container {
  display: flex;
  gap: 16px;
  justify-content: space-around;
  flex-wrap: wrap;
}

.bubble-column {
  min-width: 180px;
  background: #f8fafc;
  border-color: #e2e8f0;
}

.bubble-circle {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1.5px solid #64748b;
  background: #ffffff;
  color: #1e293b;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: bold;
}

.bubble-filled {
  background-color: #0f172a !important;
  color: #ffffff !important;
  border-color: #0f172a !important;
}

.id-box {
  width: 22px;
  height: 26px;
  border: 1.5px solid #64748b;
  border-radius: 4px;
}

@media print {
  body * {
    visibility: hidden;
  }
  .printable-exam-sheet, .printable-exam-sheet * {
    visibility: visible;
  }
  .printable-exam-sheet {
    position: absolute !important;
    left: 0 !important;
    top: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding: 15mm !important;
    background: white !important;
    color: black !important;
    box-shadow: none !important;
    border: none !important;
  }
  .d-print-none {
    display: none !important;
  }
  .q-number-badge {
    background: #000 !important;
    color: #fff !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  .bubble-filled {
    background-color: #000 !important;
    color: #fff !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
}
</style>
