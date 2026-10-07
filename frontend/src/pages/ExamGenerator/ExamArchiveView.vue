<template>
  <div class="exam-archive-page">

    <!-- VIEW 1: LIST -->
    <div v-if="!selectedExam">


      <!-- Filters -->
      <filter-fields label="خيارات تصفية والبحث في أرشيف الاختبارات" class="main-card border-0 pa-5 rounded-2xl mb-8">
        <v-row dense class="align-center">
          <!-- Institution Type Selector (مدارس / جامعات / الكل) -->
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="filterInstitutionType"
              :items="institutionTypeOptions"
              item-title="text"
              item-value="value"
              class="mb-6"
              placeholder="نوع المؤسسة"
              prepend-inner-icon="mdi-domain"
              hide-details
              density="compact"
              variant="outlined"
              @update:model-value="onInstitutionTypeChange"
            />
          </v-col>

          <!-- 🏫 School Filters -->
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
              :param="{ field: filterInstituteField, education_system: filterInstituteEducationSystem }"
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

          <!-- Common Subject Filter (Hidden when university or institute mode) -->
          <auto-list
            v-if="filterInstitutionType !== 'university' && filterInstitutionType !== 'institute'"
            v-model="filterSubject"
            name="Subject"
            :param="subjectFilterParam"
            placeholder="المادة الدراسية"
            cols="3"
            :add="false"
          />

          <!-- Exam Period Filter -->
          <auto-list
            v-model="filterPeriod"
            name="Period"
            placeholder="الفترة الامتحانية"
            cols="3"
            :add="false"
          />

          <!-- Search Query -->
          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model="searchQuery"
              placeholder="بحث بالرمز أو عنوان الاختبار..."
              prepend-inner-icon="mdi-magnify"
              clearable
              density="compact"
              variant="outlined"
              class="mb-6"
              hide-details
            />
          </v-col>

          <!-- Filter Actions -->
          <v-col cols="12" sm="12" md="6" class="d-flex align-center justify-end gap-2">
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
                <v-avatar color="primary" variant="tonal" size="36" class="rounded-lg">
                  <v-icon size="18">mdi-file-document-outline</v-icon>
                </v-avatar>
                <div>
                  <div class="d-flex align-center gap-2">
                    <span class="font-weight-black text-subtitle-2 text-primary">{{ item.title }}</span>
                    <v-chip
                      v-if="filterInstitutionType === 'all' && item.institution_type"
                      size="x-small"
                      :color="item.institution_type === 'university' ? 'purple' : 'primary'"
                      variant="tonal"
                      class="font-weight-bold"
                    >
                      {{ item.institution_type === 'university' ? '🎓 جامعي' : '🏫 مدرسي' }}
                    </v-chip>
                  </div>
                  <div class="text-caption text-medium-emphasis">{{ item.subjectName }}</div>
                </div>
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
              <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold">
                {{ item.questionsCount }} سؤال
              </v-chip>
            </template>

            <template v-else-if="key === 'actions'">
              <div class="d-flex align-center justify-center">
                <custom-btn label="لوحة التحكم" icon="monitor-dashboard" variant="tonal" color="primary"
                  class="font-weight-bold px-3" :click="() => openDashboard(item)" />
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
            <custom-btn type="add" label="طباعة الأسئلة" icon="mdi-file-pdf-box" variant="tonal" color="primary"
              class="font-weight-bold" :click="() => goToExamPrint(selectedExam, 'questions')" />
            <custom-btn type="add" label="مفتاح الإجابة" icon="mdi-key-variant" variant="tonal" color="success"
              class="font-weight-bold" :click="() => goToExamPrint(selectedExam, 'key')" />
            <custom-btn type="add" label="أوراق التظليل" icon="mdi-printer" color="emerald"
              class="font-weight-bold text-white" :click="() => goToExamPrint(selectedExam, 'sheets')" />
          </div>
        </div>
      </div>

      <div class="main-card rounded-2xl overflow-hidden">
        <v-tabs v-model="dashboardTab" color="primary" align-tabs="center" class="border-b border-slate-100">
          <v-tab :value="0" class="font-weight-bold"><v-icon start>mdi-information-outline</v-icon>معلومات
            الاختبار</v-tab>
          <v-tab :value="1" class="font-weight-bold"><v-icon start>mdi-file-document-multiple-outline</v-icon>النماذج
            والأسئلة</v-tab>
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
                      <custom-btn type="add" label="تصدير PDF" icon="mdi-file-pdf-box" variant="tonal" color="primary"
                        :click="() => goToExamPrint(selectedExam, 'questions')" />
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
                      <custom-btn type="add" label="تصدير PDF" icon="mdi-file-pdf-box" variant="tonal" color="primary"
                        :click="() => goToExamPrint(selectedExam, 'key')" />
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

        </v-window>
      </div>
    </div>

  </div>
</template>

<script>
import { examsService } from '@/services/examsService'
import { academicService } from '@/services/academicService'
import { bankService } from '@/services/bankService'

export default {
  name: 'ExamArchiveView',

  computed: {
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
  },

  data() {
    return {
      loading: false,
      items: { results: [], pagination: {} },
      examDetails: null,
      // Filters
      filterInstitutionType: 'all',
      institutionTypeOptions: [
        { text: "الكل (مدارس وجامعات ومعاهد)", value: "all" },
        { text: "🏫 مدارس فقط", value: "school" },
        { text: "🎓 جامعات فقط", value: "university" },
        { text: "🏢 معاهد وتدريب مهني", value: "institute" },
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
        { title: 'النماذج', key: 'versionCode', sortable: false },
        { title: 'عدد الأسئلة', key: 'questionsCount', sortable: false, align: 'center' },
      ],
      selectedExam: null,
      dashboardTab: 0,
      activeVersionIndex: 0,
      versionSubTab: 0,
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

        const enriched = results.map(exam => ({
          ...exam,
          subjectName: exam.subject_name || 'عام',
          versionsList: exam.versions_list || [],
          questionsCount: exam.questions_count || 0,
        }))

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
      this.filterInstitutionType = 'all'
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

    async openDashboard(exam) {
      this.selectedExam = exam
      this.dashboardTab = 0
      this.activeVersionIndex = 0
      this.versionSubTab = 0
      
      try {
        const details = await examsService.getExamModelsDetails(exam.id)
        this.examDetails = details
      } catch (err) {
        console.error("Failed to load exam details for dashboard", err)
      }
    },

    closeDashboard() { 
      this.selectedExam = null 
      this.examDetails = null
    },

    goToExamPrint(exam, type) {
      const routeNames = {
        questions: 'exams-print-questions',
        key: 'exams-print-key',
        sheets: 'exams-print-sheets',
      }
      const routeData = this.$router.resolve({ name: routeNames[type], query: { examId: exam.id } })
      window.open(routeData.href, '_blank')
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
</style>
