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
              <div class="d-flex align-center justify-center text-body-2" style="color: #000000 !important;">
                <span>{{ item.institutionTypeFullLabel }}</span>
              </div>
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
              <span class="text-body-2" style="color: #000000 !important;">
                {{ item.questionsCount }} سؤال
              </span>
            </template>

            <template v-else-if="key === 'is_approved'">
              <v-chip
                size="small"
                :color="item.is_approved ? 'success' : 'amber-darken-2'"
                variant="tonal"
                class="font-weight-bold"
              >
                <v-icon start size="14">{{ item.is_approved ? 'mdi-check-decagram' : 'mdi-clock-outline' }}</v-icon>
                {{ item.is_approved ? 'معتمد' : 'بانتظار الاعتماد' }}
              </v-chip>
            </template>

            <template v-else-if="key === 'studentsCount'">
              <div class="d-flex align-center justify-center text-body-2" style="color: #000000 !important;">
                <span>{{ item.studentsCount || 0 }} طالب</span>
              </div>
            </template>

            <template v-else-if="key === 'actions'">
              <div class="d-flex align-center justify-center">
                <v-menu transition="slide-y-transition" location="bottom end" offset="8">
                  <template v-slot:activator="{ props }">
                    <custom-btn v-bind="props" is-icon icon="dots-vertical" color="secondary" variant="text" />
                  </template>

                  <v-card elevation="24" rounded="lg" class="premium-menu-card border-thin overflow-hidden"
                    style="min-width: 220px">
                    <div class="pa-3 border-b d-flex align-center"
                      style="background-color: rgba(var(--v-theme-primary), 0.08)">
                      <v-icon color="primary" class="me-2" size="20">mdi-dots-horizontal-circle-outline</v-icon>
                      <div class="text-caption font-weight-bold" style="color: rgb(var(--v-theme-on-surface))">
                        إجراءات السجل
                      </div>
                    </div>

                    <v-card-text class="pa-1">
                      <v-list density="compact" class="bg-transparent pa-0">
                        <v-list-subheader class="modern-subheader px-2 mt-1 mb-1">
                          خيارات الاختبار
                        </v-list-subheader>

                        <!-- اعتماد وتسكين الطلاب -->
                        <v-list-item
                          v-if="!item.is_approved"
                          @click="confirmApproveExam(item)"
                          class="premium-list-item"
                        >
                          <template v-slot:prepend>
                            <v-icon size="18" color="success" class="me-2">mdi-check-decagram</v-icon>
                          </template>
                          <v-list-item-title class="text-caption font-weight-bold text-success">
                            اعتماد وتسكين الطلاب
                          </v-list-item-title>
                        </v-list-item>

                          <!-- تعديل الاختبار ومسودته (فقط إذا لم يكن معتمداً) -->
                          <v-list-item
                            v-if="!item.is_approved"
                            :disabled="loadingEditId === item.id"
                            @click="editExam(item)"
                            class="premium-list-item"
                          >
                            <template v-slot:prepend>
                              <v-progress-circular
                                v-if="loadingEditId === item.id"
                                indeterminate
                                size="18"
                                width="2"
                                color="warning"
                                class="me-2"
                              />
                              <v-icon v-else size="18" color="warning" class="me-2">mdi-pencil-outline</v-icon>
                            </template>
                            <v-list-item-title class="text-caption font-weight-bold text-warning">
                              {{ loadingEditId === item.id ? 'جاري الانتقال للتعديل...' : 'تعديل الاختبار ومسودته' }}
                            </v-list-item-title>
                          </v-list-item>

                        <!-- إلغاء الاعتماد (إعادة لمسودة) -->
                        <v-list-item
                          v-else
                          @click="confirmUnapproveExam(item)"
                          class="premium-list-item"
                        >
                          <template v-slot:prepend>
                            <v-icon size="18" color="amber-darken-3" class="me-2">mdi-undo-variant</v-icon>
                          </template>
                          <v-list-item-title class="text-caption font-weight-medium text-amber-darken-3">
                            إلغاء الاعتماد (إعادة لمسودة)
                          </v-list-item-title>
                        </v-list-item>

                        <!-- تفاصيل الاختبار والمناطق -->
                        <v-list-item @click="openExamDetailsModal(item)" class="premium-list-item">
                          <template v-slot:prepend>
                            <v-icon size="18" color="info" class="me-2">mdi-eye-outline</v-icon>
                          </template>
                          <v-list-item-title class="text-caption font-weight-medium text-info">
                            تفاصيل الاختبار والمناطق
                          </v-list-item-title>
                        </v-list-item>

                        <!-- لوحة التحكم والطباعة -->
                        <v-list-item @click="openDashboard(item)" class="premium-list-item">
                          <template v-slot:prepend>
                            <v-icon size="18" color="primary" class="me-2">mdi-monitor-dashboard</v-icon>
                          </template>
                          <v-list-item-title class="text-caption font-weight-medium text-primary">
                            لوحة التحكم والطباعة
                          </v-list-item-title>
                        </v-list-item>

                        <!-- التصحيح الضوئي OMR -->
                        <v-list-item :to="`/omr-exams?open_exam_id=${item.id}`" class="premium-list-item">
                          <template v-slot:prepend>
                            <v-icon size="18" color="purple-darken-1" class="me-2">mdi-scanner</v-icon>
                          </template>
                          <v-list-item-title class="text-caption font-weight-medium text-purple-darken-1">
                            التصحيح الضوئي (OMR)
                          </v-list-item-title>
                        </v-list-item>

                      </v-list>
                    </v-card-text>
                  </v-card>
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
                <v-chip
                  size="x-small"
                  :color="selectedExam.is_approved ? 'success' : 'amber-darken-2'"
                  variant="flat"
                  class="font-weight-bold"
                >
                  <v-icon start size="12">{{ selectedExam.is_approved ? 'mdi-check-decagram' : 'mdi-clock-outline' }}</v-icon>
                  {{ selectedExam.is_approved ? 'معتمد رسمياً' : 'مسودة بانتظار الاعتماد' }}
                </v-chip>
              </div>
              <h1 class="text-h4 font-weight-black mb-0">{{ selectedExam.title }}</h1>
            </div>
          </div>
          <div class="d-flex align-center gap-2 flex-wrap">
            <v-btn
              v-if="!selectedExam.is_approved"
              variant="flat"
              color="success"
              rounded="lg"
              class="font-weight-bold text-white shadow-sm"
              prepend-icon="mdi-check-decagram"
              :loading="approvingExamId === selectedExam.id"
              @click="confirmApproveExam(selectedExam)"
            >
              اعتماد الاختبار وتسكين الطلاب
            </v-btn>
              <v-btn
                v-if="!selectedExam.is_approved"
                variant="tonal"
                color="warning"
                rounded="lg"
                class="font-weight-bold shadow-sm"
                :loading="loadingEditId === selectedExam.id"
                prepend-icon="mdi-pencil-outline"
                @click="editExam(selectedExam)"
              >
                تعديل الاختبار ومسودته
              </v-btn>

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
                :type="selectedExam.is_approved ? 'info' : 'warning'"
                variant="tonal"
                class="rounded-xl mb-4"
                :icon="selectedExam.is_approved ? 'mdi-account-off-outline' : 'mdi-alert-circle-outline'"
              >
                <div class="font-weight-bold mb-1">
                  {{ selectedExam.is_approved ? 'لا يوجد طلاب مسجلون' : 'الاختبار غير معتمد بعد (قيد المسودة)' }}
                </div>
                <div class="text-body-2 mb-2">
                  <template v-if="!selectedExam.is_approved">
                    لم يتم تسكين وتوزيع الطلاب على نماذج هذا الاختبار لأن الاختبار لا يزال مسودة بانتظار الاعتماد الرسمي. عند اعتماد الاختبار، سيقوم النظام تلقائياً بحصر الطلاب وتسكينهم وتوزيعهم على النماذج وتجميد مفاتيح الإجابة.
                  </template>
                  <template v-else>
                    لم يتم تسجيل أي طلاب في هذا الاختبار. تأكد من أن الاختبار مرتبط بصف دراسي ونطاق جغرافي يحتوي على طلاب مسجلين.
                  </template>
                </div>
                <v-btn
                  v-if="!selectedExam.is_approved"
                  variant="flat"
                  color="success"
                  size="small"
                  rounded="lg"
                  class="font-weight-bold text-white mt-1"
                  prepend-icon="mdi-check-decagram"
                  :loading="approvingExamId === selectedExam.id"
                  @click="confirmApproveExam(selectedExam)"
                >
                  اعتماد الاختبار وتسكين الطلاب الآن
                </v-btn>
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

    <!-- WIDE PRINT & PREVIEW DIALOG (CustomDialog) -->
    <CustomDialog v-model="printPreviewDialog" width="1150" :showClose="true">
      <template #title>
        <div class="d-flex align-center justify-space-between flex-wrap gap-3 w-100 pe-2 d-print-none">
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

          <!-- Controls: Mode Switcher + Version Selector + Print Button -->
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
          </div>
        </div>
      </template>

      <!-- Scrollable Paper Body -->
      <div class="pa-4 pa-md-6 print-modal-body" style="background-color: #f1f5f9; max-height: 75vh; overflow-y: auto;">
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
      </div>
    </CustomDialog>

    <!-- DIALOG: CONFIRM APPROVAL MODAL (CustomDialog) -->
    <CustomDialog
      v-model="approvalConfirmDialog"
      width="540"
      title="تأكيد اعتماد الاختبار"
      subTitle="تسكين الطلاب على نماذج الاختبار وتجميد مفاتيح الإجابة"
      :showClose="true"
    >
      <div class="text-center py-2">
        <v-avatar color="success" variant="tonal" size="64" class="mb-4 mx-auto">
          <v-icon size="36" color="success">mdi-check-decagram</v-icon>
        </v-avatar>

        <p class="text-body-1 font-weight-bold mb-3 text-slate-800">
          هل أنت متأكد من رغبتك في اعتماد اختبار 
          <span class="text-primary font-weight-black">"{{ examToApprove?.title }}"</span> 
          رسمياً؟
        </p>

        <v-alert type="info" variant="tonal" density="compact" class="rounded-xl text-start mb-2 text-caption">
          <div class="font-weight-bold mb-1">النتائج المترتبة على الاعتماد:</div>
          <ul class="ps-4 mb-0">
            <li>حصر الطلاب المستهدفين وفق الصف/المسار والنطاق الجغرافي المحدد.</li>
            <li>توزيع وتسكين الطلاب على نماذج الاختبار وتوليد أرقام الجلوس والأرقام السرية.</li>
            <li>تجميد مفاتيح الإجابة (Answer Keys) وتوليد التوقيع الرقمي المشفر.</li>
          </ul>
        </v-alert>
      </div>

      <template #actions>
        <custom-btn
          label="إلغاء"
          variant="tonal"
          color="secondary"
          class="font-weight-bold px-4"
          :disabled="approvingExamId !== null"
          :click="() => approvalConfirmDialog = false"
        />
        <custom-btn
          type="add"
          label="تأكيد الاعتماد وتسكين الطلاب"
          icon="mdi-check-decagram"
          color="success"
          class="font-weight-bold px-6"
          :loading="approvingExamId !== null"
          :click="executeApproveExam"
        />
      </template>
    </CustomDialog>

    <!-- DIALOG: CONFIRM UNAPPROVE MODAL (CustomDialog) -->
    <CustomDialog
      v-model="unapproveConfirmDialog"
      width="500"
      title="إلغاء اعتماد الاختبار"
      subTitle="إعادة الاختبار لحالة المسودة وإلغاء تسكين الطلاب"
      :showClose="true"
    >
      <div class="text-center py-2">
        <v-avatar color="warning" variant="tonal" size="64" class="mb-4 mx-auto">
          <v-icon size="36" color="warning">mdi-undo-variant</v-icon>
        </v-avatar>

        <p class="text-body-1 font-weight-bold mb-3 text-slate-800">
          هل ترغب بإلغاء اعتماد اختبار 
          <span class="text-warning-darken-2 font-weight-black">"{{ examToUnapprove?.title }}"</span> 
          وإعادته لمسودة؟
        </p>

        <v-alert type="warning" variant="tonal" density="compact" class="rounded-xl text-start mb-2 text-caption">
          <span class="font-weight-bold text-error">
            تنبيه: سيتم حذف جميع تسجيلات وتسكين الطلاب على هذا الاختبار وإلغاء تجميد مفاتيح الإجابة.
          </span>
        </v-alert>
      </div>

      <template #actions>
        <custom-btn
          label="تراجع"
          variant="tonal"
          color="secondary"
          class="font-weight-bold px-4"
          :disabled="unapprovingExamId !== null"
          :click="() => unapproveConfirmDialog = false"
        />
        <custom-btn
          type="del"
          label="نعم، إلغاء الاعتماد"
          icon="mdi-undo-variant"
          color="warning"
          class="font-weight-bold px-5"
          :loading="unapprovingExamId !== null"
          :click="executeUnapproveExam"
        />
      </template>
    </CustomDialog>

    <!-- MODAL: EXAM DETAILS & GEOGRAPHIC SCOPE (CustomDialog) -->
    <CustomDialog
      v-model="detailsDialog"
      width="820"
      :showClose="true"
    >
      <template #title>
        <div class="d-flex align-center gap-3 pe-2">
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
      </template>

      <!-- Content -->
      <div class="pa-2">
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
      </div>

      <!-- Dialog Footer Actions -->
      <template #actions>
        <custom-btn
          label="إغلاق"
          variant="outlined"
          color="secondary"
          class="font-weight-bold px-4"
          :click="() => detailsDialog = false"
        />
        <div class="d-flex align-center gap-2 ms-auto">
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
      </template>
    </CustomDialog>
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
      loadingEditId: null,
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
        { title: 'حالة الاعتماد', key: 'is_approved', sortable: true, align: 'center' },
        { title: 'الطلاب المسجلون', key: 'studentsCount', sortable: false, align: 'center' },
      ],
      approvalConfirmDialog: false,
      examToApprove: null,
      approvingExamId: null,
      unapproveConfirmDialog: false,
      examToUnapprove: null,
      unapprovingExamId: null,
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
            is_approved: !!exam.is_approved,
            approved_at: exam.approved_at,
            approved_by_name: exam.approved_by_name,
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

    editExam(item) {
      if (!item || item.is_approved) return
      this.loadingEditId = item.id
      this.$router.push({
        path: '/exams-create',
        query: { edit_exam_id: item.id }
      }).catch(() => {
        this.$router.push({
          path: '/ExamGenerator/ExamCreateView',
          query: { edit_exam_id: item.id }
        })
      }).finally(() => {
        setTimeout(() => {
          this.loadingEditId = null
        }, 1200)
      })
    },

    confirmApproveExam(item) {
      this.examToApprove = item
      this.approvalConfirmDialog = true
    },

    async executeApproveExam() {
      if (!this.examToApprove) return
      const exam = this.examToApprove
      this.approvingExamId = exam.id
      try {
        const res = await examsService.approveExam(exam.id)
        if (res && res.success) {
          exam.is_approved = true
          exam.studentsCount = res.studentsCount ?? exam.studentsCount
          exam.approved_at = res.approved_at
          exam.approved_by_name = res.approved_by_name

          if (this.selectedExam && this.selectedExam.id === exam.id) {
            this.selectedExam.is_approved = true
            this.selectedExam.studentsCount = exam.studentsCount
            this.totalStudentsCount = exam.studentsCount
            await this.fetchRegisteredStudents({ params: { page: 1 } })
          }

          if (this.$alert) {
            this.$alert("successData", {
              title: "تم اعتماد الاختبار بنجاح",
              message: res.message || `تم اعتماد الاختبار وتسكين ${res.studentsCount || 0} طالب وتجميد المفاتيح.`
            })
          }
          this.approvalConfirmDialog = false
          this.examToApprove = null
        } else {
          throw new Error(res?.message || 'فشل اعتماد الاختبار')
        }
      } catch (err) {
        console.error('فشل اعتماد الاختبار:', err)
        const errMsg = err.response?.data?.message || err.message || 'حدث خطأ أثناء اعتماد الاختبار'
        if (this.$alert) {
          this.$alert("errorData", {
            title: "خطأ في الاعتماد",
            message: errMsg
          })
        }
      } finally {
        this.approvingExamId = null
      }
    },

    confirmUnapproveExam(item) {
      this.examToUnapprove = item
      this.unapproveConfirmDialog = true
    },

    async executeUnapproveExam() {
      if (!this.examToUnapprove) return
      const exam = this.examToUnapprove
      this.unapprovingExamId = exam.id
      try {
        const res = await examsService.unapproveExam(exam.id)
        if (res && res.success) {
          exam.is_approved = false
          exam.studentsCount = 0
          exam.approved_at = null
          exam.approved_by_name = null

          if (this.selectedExam && this.selectedExam.id === exam.id) {
            this.selectedExam.is_approved = false
            this.selectedExam.studentsCount = 0
            this.totalStudentsCount = 0
            await this.fetchRegisteredStudents({ params: { page: 1 } })
          }

          if (this.$alert) {
            this.$alert("successData", {
              title: "تم إلغاء الاعتماد",
              message: res.message || "تمت إعادة الاختبار لحالة المسودة وإلغاء تسكين الطلاب."
            })
          }
          this.unapproveConfirmDialog = false
          this.examToUnapprove = null
        } else {
          throw new Error(res?.message || 'فشل إلغاء اعتماد الاختبار')
        }
      } catch (err) {
        console.error('فشل إلغاء اعتماد الاختبار:', err)
        const errMsg = err.response?.data?.message || err.message || 'حدث خطأ أثناء إلغاء الاعتماد'
        if (this.$alert) {
          this.$alert("errorData", {
            title: "خطأ",
            message: errMsg
          })
        }
      } finally {
        this.unapprovingExamId = null
      }
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
        if (dashData && dashData.isApproved !== undefined) {
          this.selectedExam.is_approved = dashData.isApproved
          if (dashData.studentsCount !== undefined) {
            this.selectedExam.studentsCount = dashData.studentsCount
            this.totalStudentsCount = dashData.studentsCount
          }
        }
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
