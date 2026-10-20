<template>
  <div class="qb-omr-exams-linking-v4 pa-4 pa-md-6">
    <!-- ── Page Header (Institutional OpenSoftCore Style) ─────────────── -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center">
        <v-avatar size="48" color="primary" variant="tonal" class="me-3 rounded-xl elevation-1">
          <v-icon size="26">mdi-link-box-variant-outline</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">ربط الاختبارات والتصحيح الضوئي (OMR)</h1>
          <p class="text-caption text-medium-emphasis mb-0">
            استعراض كشوفات الطلاب، معاينة النماذج ومفاتيح الحل، وتوليد وطباعة أوراق التظليل الوزارية المعتمدة
          </p>
        </div>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <v-btn
          color="secondary"
          variant="tonal"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-scanner"
          to="/omr-scanner-lab"
        >
          مختبر المسح والتصحيح
        </v-btn>
        <v-btn
          color="secondary"
          variant="tonal"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-card-text-outline"
          to="/omr-templates"
        >
          مكتبة القوالب
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          rounded="lg"
          class="font-weight-bold shadow-sm"
          prepend-icon="mdi-refresh"
          :loading="loading"
          @click="fetchExams"
        >
          تحديث القائمة
        </v-btn>
      </div>
    </div>

    <!-- ── OMR Workflow Stepper (المرحلة 1: استلام وتجهيز الاختبار) ── -->
    <omr-workflow-bar :active-step="1" :exam-id="selectedExam?.id" />

    <!-- Unified Filter Fields (Standard Tripartite Institution Filters: Schools, Universities, Institutes) -->
    <filter-fields label="خيارات التصفية والبحث المتقدم في الاختبارات" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Search Query Input -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="searchQuery"
            label="اسم الاختبار أو الرمز"
            placeholder="بحث باسم الاختبار أو رمزه (Code)..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @keyup.enter="fetchExams"
          />
        </v-col>

        <!-- Institution Type Selector (مدارس / جامعات / معاهد / الكل) موحد كـ auto-list -->
        <auto-list
          v-model="filterInstitutionType"
          name="InstitutionType"
          placeholder="نوع المؤسسة التعليمية"
          cols="3"
          :add="false"
          @update:model-value="onInstitutionTypeChange"
        />

        <!-- 🏫 School Filters (المرحلة، الصف والمسار، المادة) -->
        <template v-if="filterInstitutionType === 'school'">
          <auto-list
            v-model="filterStage"
            name="Stage"
            label="المرحلة الدراسية"
            cols="3"
            sm="6"
            md="3"
            :add="false"
            @update:model-value="onStageChange"
          />
          <auto-list
            v-model="filterClassTrack"
            name="ClassTrackByStage"
            :param="filterStage"
            label="الصف والمسار المدرسي"
            cols="3"
            sm="6"
            md="3"
            :add="false"
            :disabled="!filterStage"
            @update:model-value="onClassTrackChange"
          />
          <auto-list
            v-model="filterSubject"
            name="Subject"
            :param="subjectFilterParam"
            label="المادة الدراسية"
            cols="3"
            sm="6"
            md="3"
            :add="false"
            @update:model-value="fetchExams"
          />
        </template>

        <!-- 🎓 University Filters (الكلية، القسم، التخصص، المقرر) -->
        <template v-if="filterInstitutionType === 'university'">
          <auto-list
            v-model="filterCollege"
            name="College"
            label="الكلية الجامعية"
            cols="3"
            sm="6"
            md="3"
            :add="false"
            @update:model-value="onCollegeChange"
          />
          <auto-list
            v-model="filterDepartment"
            name="DepartmentByCollege"
            :param="filterCollege"
            label="القسم الأكاديمي"
            cols="3"
            sm="6"
            md="3"
            :add="false"
            :disabled="!filterCollege"
            @update:model-value="onDepartmentChange"
          />
          <auto-list
            v-model="filterSpecialization"
            name="Specialization"
            :param="filterDepartment"
            label="التخصص والبرنامج"
            cols="3"
            sm="6"
            md="3"
            :add="false"
            :disabled="!filterDepartment"
            @update:model-value="onSpecializationChange"
          />
          <auto-list
            v-model="filterSemesterSubject"
            name="SemesterSubject"
            :param="filterSpecialization"
            label="مقرر الفصل الجامعي"
            cols="3"
            sm="6"
            md="3"
            :add="false"
            @update:model-value="fetchExams"
          />
        </template>

        <!-- 🏢 Institute Filters (المجال المهني، نظام التعليم، التخصص، المادة) -->
        <template v-if="filterInstitutionType === 'institute'">
          <auto-list
            v-model="filterInstituteField"
            name="InstituteField"
            label="المجال المهني / التقني"
            cols="3"
            sm="6"
            md="3"
            :add="false"
            @update:model-value="onInstituteFieldChange"
          />
          <auto-list
            v-model="filterInstituteEducationSystem"
            name="InstituteEducationSystem"
            :param="filterInstituteField"
            label="نظام التعليم والتدريب"
            cols="3"
            sm="6"
            md="3"
            :add="false"
            :disabled="!filterInstituteField"
            @update:model-value="onInstituteEducationSystemChange"
          />
          <auto-list
            v-model="filterInstituteSpecialization"
            name="InstituteSpecialization"
            :param="instituteSpecParam"
            label="التخصص المهني"
            cols="3"
            sm="6"
            md="3"
            :add="false"
            :disabled="!filterInstituteEducationSystem"
            @update:model-value="fetchExams"
          />
          <auto-list
            v-model="filterInstituteSubject"
            name="InstituteSubject"
            :param="instituteSubjectParam"
            label="المادة الدراسية للمعهد"
            cols="3"
            sm="6"
            md="3"
            :add="false"
            @update:model-value="fetchExams"
          />
        </template>

        <!-- Fallback Subject if All / None selected -->
        <auto-list
          v-if="!filterInstitutionType || filterInstitutionType === 'all'"
          v-model="filterSubject"
          name="Subject"
          placeholder="المادة الدراسية (عام)"
          cols="3"
          :add="false"
          @update:model-value="fetchExams"
        />

        <!-- Actions -->
        <v-col cols="12" sm="6" md="3" class="d-flex align-center gap-2">
          <custom-btn
            type="show"
            label="تحديث"
            color="primary"
            class="font-weight-bold flex-grow-1 mb-6"
            :click="fetchExams"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ"
            class="font-weight-bold mb-6"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Unified Custom Data Table -->
    <div class="main-card rounded-2xl overflow-hidden mb-6">
      <custom-data-table
        v-bind="{
          items: tableItems,
          headers,
          loading,
        }"
        :actions="false"
        :hasFilter="false"
        :log="false"
        :restore="false"
      >
        <template v-slot:item-slot="{ item, key }">
          <!-- Code & Title (Clickable) -->
          <template v-if="key === 'exam_info'">
            <div
              class="d-flex align-center py-2 cursor-pointer exam-row-title-trigger"
              @click.stop="openExamHub(item)"
              title="انقر لفتح كشوفات الطلاب والأسئلة ومفاتيح الحل وتوليد الأوراق"
            >
              <v-avatar color="primary" variant="tonal" size="38" class="me-3 rounded-lg flex-shrink-0">
                <v-icon size="20">mdi-file-document-edit-outline</v-icon>
              </v-avatar>
              <div>
                <div class="font-weight-black text-body-2 text-on-surface exam-clickable-title">{{ item.title }}</div>
                <div class="text-caption text-medium-emphasis d-flex align-center gap-2 mt-1">
                  <span class="font-mono bg-grey-lighten-4 px-2 py-0.5 rounded border text-caption">{{ item.uniqueCode }}</span>
                  <span>{{ item.created_at }}</span>
                </div>
              </div>
            </div>
          </template>

          <!-- Subject & Year -->
          <template v-else-if="key === 'subject_info'">
            <div class="font-weight-bold text-body-2">{{ item.subject_name }}</div>
            <div class="text-caption text-medium-emphasis">{{ item.year_name }} ({{ item.institution_type_display }})</div>
          </template>

          <!-- Versions & Questions (Clickable to open Keys Tab) -->
          <template v-else-if="key === 'versions_info'">
            <div
              class="cursor-pointer py-1"
              @click.stop="openExamHub(item, 'keys')"
              title="انقر لمعاينة نماذج الأسئلة ومفاتيح الحل المعتمدة"
            >
              <div class="d-flex justify-center gap-1 mb-1">
                <v-chip
                  v-for="v in item.versions"
                  :key="v.id"
                  size="x-small"
                  color="primary"
                  variant="tonal"
                  class="font-weight-bold unified-table-chip"
                >
                  {{ v.versionCode }}
                </v-chip>
              </div>
              <div class="text-caption font-weight-bold text-primary">
                {{ item.total_questions }} سؤال (مفاتيح الحل)
              </div>
            </div>
          </template>

          <!-- Registered Students (Clickable to open Roster Tab) -->
          <template v-else-if="key === 'students_count'">
            <div
              class="cursor-pointer py-1"
              @click.stop="openExamHub(item, 'roster')"
              title="انقر لفتح كشف الطلاب وأرقام الجلوس"
            >
              <v-chip
                :color="item.registered_students_count > 0 ? 'primary' : 'grey'"
                variant="tonal"
                size="small"
                class="font-weight-bold unified-table-chip"
                prepend-icon="mdi-account-school-outline"
              >
                {{ item.registered_students_count || 0 }} طالب
              </v-chip>
              <div v-if="item.registered_students_count > 0" class="text-caption text-success mt-1">
                <v-icon size="12">mdi-check-circle</v-icon> كشف معتمد
              </div>
              <div v-else class="text-caption text-medium-emphasis mt-1">
                يحتاج تسجيل
              </div>
            </div>
          </template>

          <!-- Grading Progress (Clickable to open Submissions Tab) -->
          <template v-else-if="key === 'progress'">
            <div
              class="cursor-pointer py-1"
              @click.stop="openExamHub(item, 'submissions')"
              title="انقر لاستعراض أوراق الإجابة المصححة"
            >
              <div class="d-flex align-center justify-center gap-2">
                <v-progress-linear
                  :model-value="item.submissions_total > 0 ? Math.min(100, Math.round((item.submissions_completed / item.submissions_total) * 100)) : 0"
                  color="success"
                  rounded
                  height="6"
                  style="width: 70px;"
                />
                <span class="text-caption font-weight-black font-mono">
                  {{ item.submissions_completed }}/{{ item.submissions_total }}
                </span>
              </div>
              <div v-if="item.average_score > 0" class="text-caption text-medium-emphasis mt-1">
                متوسط: <strong class="text-primary">{{ item.average_score }}%</strong>
              </div>
            </div>
          </template>

          <!-- Actions -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-2 flex-wrap">
              <!-- 1. طباعة وتوليد أوراق التظليل للطلاب مباشرة -->
              <v-btn
                color="primary"
                variant="flat"
                rounded="lg"
                size="small"
                class="font-weight-bold px-3"
                prepend-icon="mdi-printer"
                @click.stop.prevent="openExamHub(item, 'template')"
                title="توليد ومعاينة وطباعة أوراق التظليل (البابل شيت) لجميع طلاب الاختبار"
              >
                طباعة أوراق التظليل
              </v-btn>

              <!-- 2. كشف الطلاب ونماذج الأسئلة ومفاتيح الحل -->
              <v-btn
                color="info"
                variant="tonal"
                rounded="lg"
                size="small"
                class="font-weight-bold px-3"
                prepend-icon="mdi-account-school-outline"
                @click.stop.prevent="openExamHub(item, 'roster')"
                title="استعراض كشف الطلاب ونماذج الأسئلة ومفاتيح الحل"
              >
                كشف الطلاب والحلول
              </v-btn>

              <!-- 3. تصميم مواصفات الورقة (أداة مساعدة) -->
              <v-btn
                color="secondary"
                variant="tonal"
                rounded="lg"
                size="small"
                class="font-weight-bold px-2"
                icon="mdi-draw-pen"
                @click.stop.prevent="openInTemplateDesigner(item)"
                title="فتح مواصفات الاختبار في مصمم قوالب التظليل OMR"
              />

              <!-- 4. سجل الطباعة للدفعات -->
              <v-btn
                color="medium-emphasis"
                variant="text"
                rounded="lg"
                size="small"
                icon="mdi-history"
                @click.stop.prevent="goToPrintRegistry(item)"
                title="سجل دفعات الطباعة السابقة لهذا الاختبار"
              />
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>

    <!-- ════════════════════════════════════════════════════════════════ -->
    <!-- DIALOG: النافذة الشاملة لإدارة الاختبار، الطلاب، وتوليد القوالب  -->
    <!-- ════════════════════════════════════════════════════════════════ -->
    <v-dialog v-model="detailsDialog" max-width="1360px" scrollable>
      <v-card class="rounded-2xl" elevation="4" style="height: 94vh; max-height: 94vh; display: flex; flex-direction: column;">
        <!-- Dialog Header -->
        <v-card-title class="pa-4 pa-md-5 border-b d-flex align-center justify-space-between bg-surface flex-wrap gap-2">
          <div class="d-flex align-center">
            <v-avatar color="primary" variant="tonal" size="44" class="me-3 rounded-xl">
              <v-icon size="24">mdi-school-outline</v-icon>
            </v-avatar>
            <div>
              <div class="text-h6 font-weight-black mb-0">{{ activeExam?.title }}</div>
              <div class="text-caption text-medium-emphasis d-flex align-center gap-2 flex-wrap">
                <span>رمز: <strong class="font-mono">{{ activeExam?.uniqueCode }}</strong></span>
                <span>• المادة: <strong>{{ activeExam?.subject_name }}</strong></span>
                <span>• العام: <strong>{{ activeExam?.year_name }}</strong></span>
                <span v-if="activeExam?.governorate">
                  • المحافظة: <strong>{{ activeExam.governorate }}{{ activeExam.directorate ? ` (${activeExam.directorate})` : '' }}</strong>
                </span>
              </div>
            </div>
          </div>

          <div class="d-flex align-center gap-2">
            <v-btn
              size="small"
              variant="flat"
              color="success"
              class="font-weight-black rounded-lg px-3"
              prepend-icon="mdi-scanner"
              @click="startGradingExam(activeExam, currentVersionObj?.versionCode || 'A')"
            >
              بدء التصحيح الضوئي
            </v-btn>
            <v-btn
              icon="mdi-close"
              variant="text"
              size="small"
              density="comfortable"
              color="medium-emphasis"
              @click="detailsDialog = false"
            />
          </div>
        </v-card-title>

        <!-- ── Main Navigation Tabs in Dialog (خفيف وسهل ومرن) ── -->
        <div class="px-4 pt-3 pb-2 bg-surface">
          <div class="exam-hub-nav-bar">
            <div class="exam-hub-nav-container">
              <div
                class="exam-hub-nav-item"
                :class="{ 'is-active': hubActiveTab === 'questions' }"
                @click="hubActiveTab = 'questions'"
                role="button"
                tabindex="0"
              >
                <v-icon size="17" class="nav-icon">mdi-file-document-outline</v-icon>
                <span>ورقة الأسئلة الرسمية (الكراسة)</span>
                <span
                  v-if="examDetails?.versions?.length"
                  class="hub-count-badge badge-purple"
                >
                  {{ examDetails.versions.length }} نماذج
                </span>
              </div>

              <div
                class="exam-hub-nav-item"
                :class="{ 'is-active': hubActiveTab === 'template' }"
                @click="hubActiveTab = 'template'"
                role="button"
                tabindex="0"
              >
                <v-icon size="17" class="nav-icon">mdi-card-text-outline</v-icon>
                <span>توليد ومعاينة ورقة التظليل</span>
              </div>

              <div
                class="exam-hub-nav-item"
                :class="{ 'is-active': hubActiveTab === 'roster' }"
                @click="hubActiveTab = 'roster'"
                role="button"
                tabindex="0"
              >
                <v-icon size="17" class="nav-icon">mdi-account-school-outline</v-icon>
                <span>كشف الطلاب والبيانات الامتحانية</span>
                <span
                  v-if="totalStudentsCount || examDetails?.registered_students_count || examDetails?.registered_students?.length"
                  class="hub-count-badge badge-blue"
                >
                  {{ totalStudentsCount || examDetails?.registered_students_count || examDetails?.registered_students?.length }}
                </span>
              </div>

              <div
                class="exam-hub-nav-item"
                :class="{ 'is-active': hubActiveTab === 'keys' }"
                @click="hubActiveTab = 'keys'"
                role="button"
                tabindex="0"
              >
                <v-icon size="17" class="nav-icon">mdi-key-variant</v-icon>
                <span>النماذج ومفاتيح الحل</span>
                <span
                  v-if="examDetails?.versions?.length"
                  class="hub-count-badge badge-amber"
                >
                  {{ examDetails.versions.length }}
                </span>
              </div>

              <div
                class="exam-hub-nav-item"
                :class="{ 'is-active': hubActiveTab === 'submissions' }"
                @click="hubActiveTab = 'submissions'"
                role="button"
                tabindex="0"
              >
                <v-icon size="17" class="nav-icon">mdi-check-decagram-outline</v-icon>
                <span>أوراق الإجابة المصححة</span>
                <span
                  v-if="examDetails?.submissions?.length || examDetails?.recent_submissions?.length"
                  class="hub-count-badge badge-green"
                >
                  {{ (examDetails?.submissions?.length || examDetails?.recent_submissions?.length) }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <v-card-text class="pa-3 pa-md-4 bg-grey-lighten-5 flex-grow-1 overflow-y-auto">
          <div v-if="loadingDetails" class="text-center py-12">
            <v-progress-circular indeterminate color="primary" size="44" class="mb-3" />
            <p class="text-body-2 font-weight-bold">جاري جلب تفاصيل الاختبار والطلاب ونماذج الأسئلة...</p>
          </div>

          <div v-else-if="examDetails">
            <!-- TAB 1: ورقة الأسئلة الرسمية (الكراسة) -->
            <ExamBookletTab
              v-show="hubActiveTab === 'questions'"
              ref="bookletTabRef"
              :active-exam="activeExam"
              :exam-details="examDetails"
              v-model:active-version-tab="activeVersionTab"
              :selected-sheet-layout="bubbleSheetTabRef?.selectedSheetLayout || 'compact_a5'"
              :get-omr-element="() => bubbleSheetTabRef?.getPrintableElement()"
              @switch-tab="(tab) => hubActiveTab = tab"
              @seed-students="seedSampleStudents"
            />

            <!-- TAB 2: توليد ومعاينة ورقة التظليل -->
            <ExamBubbleSheetTab
              v-show="hubActiveTab === 'template'"
              ref="bubbleSheetTabRef"
              :active-exam="activeExam"
              :exam-details="examDetails"
              @open-designer="openInTemplateDesigner"
              @print-package="() => bookletTabRef?.printQuestionsAndSheets('package')"
              @print-roster="() => rosterTabRef?.printRosterList()"
              @seed-students="seedSampleStudents"
              @refresh-details="() => fetchExamHubDetails(activeExam)"
            />

            <!-- TAB 3: كشف الطلاب والبيانات الامتحانية -->
            <ExamStudentsRosterTab
              v-show="hubActiveTab === 'roster'"
              ref="rosterTabRef"
              :active-exam="activeExam"
              :exam-details="examDetails"
              :seeding-students="seedingStudents"
              @switch-to-template="(mode) => { hubActiveTab = 'template'; nextTick(() => bubbleSheetTabRef?.setMode(mode)); }"
              @select-student-for-sheet="(st) => { hubActiveTab = 'template'; nextTick(() => bubbleSheetTabRef?.setStudent(st.id)); }"
              @print-student-sheet="(st) => { hubActiveTab = 'template'; nextTick(() => { bubbleSheetTabRef?.setStudent(st.id); bubbleSheetTabRef?.printSingleSheet(); }); }"
              @seed-students="seedSampleStudents"
            />

            <!-- TAB 4: النماذج ومفاتيح الحل -->
            <ExamAnswerKeysTab
              v-show="hubActiveTab === 'keys'"
              ref="answerKeysTabRef"
              :active-exam="activeExam"
              :exam-details="examDetails"
              v-model:active-version-tab="activeVersionTab"
              @open-question-paper-modal="() => bookletTabRef?.openQuestionPaperModal()"
              @print-questions-only="() => bookletTabRef?.printQuestionsAndSheets('questions_only')"
              @print-package="() => bookletTabRef?.printQuestionsAndSheets('package')"
              @start-grading="(code) => startGradingExam(activeExam, code)"
            />

            <!-- TAB 5: أوراق الإجابة المصححة -->
            <ExamSubmissionsTab
              v-show="hubActiveTab === 'submissions'"
              ref="submissionsTabRef"
              :active-exam="activeExam"
              :exam-details="examDetails"
              @view-submissions="viewSubmissions"
            />
          </div>
        </v-card-text>

        <!-- Dialog Footer Actions -->
        <v-card-actions class="pa-4 bg-surface border-t d-flex justify-space-between align-center flex-wrap gap-2">
          <div class="text-caption text-medium-emphasis">
            نظام التصحيح الضوئي المعتمد — بنك الأسئلة والتقويم التربوي
          </div>
          <div class="d-flex align-center gap-2">
            <custom-btn
              type="cancel"
              variant="outlined"
              label="إغلاق"
              :click="() => detailsDialog = false"
            />
            <custom-btn
              icon="tune"
              label="مختبر المعايرة والتجربة"
              color="primary"
              variant="tonal"
              class="font-weight-bold"
              :click="() => openScannerLab(activeExam)"
            />
          </div>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/services/omr/client.js'
import ExamBookletTab from './exam_hub/ExamBookletTab.vue'
import ExamStudentsRosterTab from './exam_hub/ExamStudentsRosterTab.vue'
import ExamBubbleSheetTab from './exam_hub/ExamBubbleSheetTab.vue'
import ExamAnswerKeysTab from './exam_hub/ExamAnswerKeysTab.vue'
import ExamSubmissionsTab from './exam_hub/ExamSubmissionsTab.vue'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const exams = ref([])
const searchQuery = ref('')
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
  fetchExams()
}

const onStageChange = () => {
  filterClassTrack.value = null
  filterSubject.value = null
  fetchExams()
}

const onClassTrackChange = () => {
  filterSubject.value = null
  fetchExams()
}

const onCollegeChange = () => {
  filterDepartment.value = null
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  fetchExams()
}

const onDepartmentChange = () => {
  filterSpecialization.value = null
  filterSemesterSubject.value = null
  fetchExams()
}

const onSpecializationChange = () => {
  filterSemesterSubject.value = null
  fetchExams()
}

const onInstituteFieldChange = () => {
  filterInstituteEducationSystem.value = null
  filterInstituteSpecialization.value = null
  filterInstituteSubject.value = null
  fetchExams()
}

const onInstituteEducationSystemChange = () => {
  filterInstituteSpecialization.value = null
  fetchExams()
}

const stats = ref({
  totalExams: 0,
  totalVersions: 0,
  totalStudents: 0,
  totalSubmissions: 0,
  avgScore: 0,
})

// Dialog State
const detailsDialog = ref(false)
const loadingDetails = ref(false)
const activeExam = ref(null)
const examDetails = ref(null)
const hubActiveTab = ref('roster') // 'questions', 'template', 'roster', 'keys', 'submissions'
const activeVersionTab = ref(0)
const seedingStudents = ref(false)

// Subcomponent template refs
const bookletTabRef = ref(null)
const bubbleSheetTabRef = ref(null)
const rosterTabRef = ref(null)
const answerKeysTabRef = ref(null)
const submissionsTabRef = ref(null)

const currentVersionObj = computed(() => {
  if (!examDetails.value || !examDetails.value.versions) return null
  return examDetails.value.versions[activeVersionTab.value] || examDetails.value.versions[0]
})

const totalStudentsCount = computed(() => {
  return rosterTabRef.value?.totalStudentsCount || examDetails.value?.registered_students_count || (examDetails.value?.registered_students?.length || 0)
})

const headers = computed(() => [
  { title: "رمز وعنوان الاختبار", key: "exam_info", sortable: true },
  { title: "المادة والعام", key: "subject_info", sortable: true, align: "center", width: "180px" },
  { title: "النماذج والأسئلة", key: "versions_info", sortable: false, align: "center", width: "160px" },
  { title: "كشف الطلاب", key: "students_count", sortable: true, align: "center", width: "140px" },
  { title: "حالة التصحيح", key: "progress", sortable: false, align: "center", width: "160px" },
  { title: "الاجراءات", key: "actions", sortable: false, align: "center", width: "320px" },
])

const filteredExams = computed(() => {
  let list = exams.value
  if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
    list = list.filter(e => e.institution_type === filterInstitutionType.value)
  }
  if (searchQuery.value && searchQuery.value.trim()) {
    const q = searchQuery.value.trim().toLowerCase()
    list = list.filter(e =>
      (e.title && e.title.toLowerCase().includes(q)) ||
      (e.uniqueCode && e.uniqueCode.toLowerCase().includes(q)) ||
      (e.subject_name && e.subject_name.toLowerCase().includes(q))
    )
  }
  return list
})

const tableItems = computed(() => ({
  results: filteredExams.value,
  count: filteredExams.value.length,
  pagination: {
    count: filteredExams.value.length,
    total: filteredExams.value.length,
  }
}))

const resetFilters = () => {
  searchQuery.value = ''
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
  fetchExams()
}

const fetchExams = async () => {
  loading.value = true
  try {
    const params = {}
    if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
      params.institution_type = filterInstitutionType.value
    }
    if (searchQuery.value && searchQuery.value.trim()) {
      params.search = searchQuery.value.trim()
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
      exams.value = resp.data.results
      updateStats(resp.data.results)
    }
  } catch (err) {
    console.error('Error fetching linking exams:', err)
  } finally {
    loading.value = false
  }
}

const updateStats = (data) => {
  let vCount = 0
  let sCount = 0
  let stCount = 0
  let totalScoreSum = 0
  let scoredExams = 0

  data.forEach(e => {
    vCount += (e.versions_count || 0)
    sCount += (e.submissions_completed || 0)
    stCount += (e.registered_students_count || 0)
    if (e.average_score > 0) {
      totalScoreSum += e.average_score
      scoredExams++
    }
  })

  stats.value = {
    totalExams: data.length,
    totalVersions: vCount,
    totalStudents: stCount,
    totalSubmissions: sCount,
    avgScore: scoredExams > 0 ? (totalScoreSum / scoredExams).toFixed(1) : '0',
  }
}

const openExamHub = async (exam, tab = 'questions') => {
  activeExam.value = exam
  detailsDialog.value = true
  loadingDetails.value = true
  hubActiveTab.value = tab
  activeVersionTab.value = 0

  try {
    const resp = await api.get(`/api/omr/exam-linking/${exam.id}/`)
    examDetails.value = { ...resp.data, ...(resp.data?.exam || {}) }
    if (resp.data && resp.data.exam) {
      activeExam.value = { ...activeExam.value, ...resp.data.exam }
    }
    await nextTick()
    if (rosterTabRef.value?.fetchExamStudents) {
      rosterTabRef.value.fetchExamStudents({ page: 1, page_size: 10 })
    }
  } catch (err) {
    console.error('Failed to load exam details:', err)
  } finally {
    loadingDetails.value = false
  }
}

const fetchExamHubDetails = async (exam) => {
  if (!exam?.id) return
  try {
    const resp = await api.get(`/api/omr/exam-linking/${exam.id}/`)
    examDetails.value = { ...resp.data, ...(resp.data?.exam || {}) }
    if (resp.data && resp.data.exam) {
      activeExam.value = { ...activeExam.value, ...resp.data.exam }
    }
  } catch (err) {
    console.error('Failed to reload exam hub details:', err)
  }
}

const quickBatchPrint = async (exam) => {
  await openExamHub(exam, 'template')
  await nextTick()
  bubbleSheetTabRef.value?.batchPrintAllStudents()
}

const quickPrintRoster = async (exam) => {
  await openExamHub(exam, 'roster')
  await nextTick()
  rosterTabRef.value?.printRosterList()
}

const seedSampleStudents = async () => {
  if (!activeExam.value) return
  seedingStudents.value = true
  try {
    await api.post(`/api/omr/exam-linking/${activeExam.value.id}/seed-students/`)
    await fetchExamHubDetails(activeExam.value)
    if (rosterTabRef.value?.fetchExamStudents) {
      rosterTabRef.value.fetchExamStudents({ page: 1, page_size: 10 })
    }
    fetchExams() // update stats
  } catch (err) {
    console.error('Failed to seed students:', err)
  } finally {
    seedingStudents.value = false
  }
}

const startGradingExam = (exam, versionCode = 'A') => {
  router.push({
    path: '/omr-scanner',
    query: {
      exam_id: exam.id,
      exam_code: exam.uniqueCode,
      exam_title: exam.title,
      version: versionCode,
    }
  })
}

const openScannerLab = (exam, versionCode = 'A') => {
  router.push({
    path: '/omr-scanner-lab',
    query: {
      exam_id: exam.id,
      exam_code: exam.uniqueCode,
      exam_title: exam.title,
      version: versionCode,
    }
  })
}

const viewSubmissions = (exam) => {
  router.push({
    path: '/omr-submissions',
    query: {
      exam_id: exam.id,
    }
  })
}

const openInTemplateDesigner = (exam) => {
  if (!exam?.id) return
  const target = `/omr-template-builder?examId=${exam.id}&mode=designer`
  router.push(target).catch(() => {
    window.location.href = target
  })
}

const goToPrintRegistry = (exam) => {
  if (!exam?.id) return
  const target = `/omr-print-registry?exam_id=${exam.id}`
  router.push(target).catch(() => {
    window.location.href = target
  })
}

onMounted(async () => {
  if (route.query.search) {
    searchQuery.value = String(route.query.search)
  }
  await fetchExams()
  const targetId = route.query.open_exam_id || route.query.exam_id || route.query.examId
  if (targetId) {
    const targetExam = exams.value.find(e => String(e.id) === String(targetId))
    if (targetExam) {
      const targetTab = route.query.tab || 'questions'
      openExamHub(targetExam, targetTab)
    }
  }
})
</script>

<style scoped>
.qb-omr-exams-linking-v4 {
  color: rgb(var(--v-theme-on-surface));
}

.stat-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
}

.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.hover-row:hover {
  background: rgba(var(--v-theme-primary), 0.03) !important;
}

.table-header-row th {
  background: rgba(var(--v-theme-surface-variant), 0.3) !important;
  padding: 12px 16px !important;
}

.omr-preview-viewport {
  min-height: 480px;
  max-height: 680px;
  background: #f1f3f5;
}

.sheet-artboard-container {
  display: inline-block;
  background: #ffffff;
  padding: 8px;
}

.option-badge {
  background: rgba(var(--v-theme-on-surface), 0.05);
  border: 1px solid rgba(var(--v-border-color), 0.1);
}

.option-correct {
  background: rgba(var(--v-theme-success), 0.12) !important;
  border-color: rgba(var(--v-theme-success), 0.3) !important;
  color: rgb(var(--v-theme-success)) !important;
  font-weight: bold;
}

.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }

.font-mono {
  font-family: monospace, monospace;
}

.unified-table-chip {
  border-radius: 6px !important;
  font-weight: 700 !important;
}

.answer-key-pill {
  white-space: nowrap;
  min-width: 54px;
  justify-content: center;
  border-color: rgba(var(--v-border-color), 0.12) !important;
  background: rgba(var(--v-theme-surface-variant), 0.12) !important;
  transition: all 0.15s ease;
}

.answer-key-pill:hover {
  background: rgba(var(--v-theme-primary), 0.08) !important;
  border-color: rgba(var(--v-theme-primary), 0.3) !important;
}

.action-icon-btn {
  transition: transform 0.18s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.18s ease !important;
}

.action-icon-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12) !important;
}

.cursor-pointer {
  cursor: pointer;
}

.exam-row-title-trigger {
  transition: opacity 0.15s ease;
}

.exam-row-title-trigger:hover .exam-clickable-title {
  color: rgb(var(--v-theme-primary)) !important;
  text-decoration: underline;
}

/* ── Lightweight Navigation Bar in Exam Hub Dialog ── */
.exam-hub-nav-bar {
  direction: rtl;
}

.exam-hub-nav-container {
  display: flex;
  align-items: center;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 5px;
  gap: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.exam-hub-nav-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  padding: 9px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.84rem;
  font-weight: 600;
  color: #64748b;
  background: transparent;
  border: 1px solid transparent;
  transition: all 0.2s ease;
  user-select: none;
  white-space: nowrap;
}

.exam-hub-nav-item:hover {
  background: #f8fafc;
  color: #334155;
}

.exam-hub-nav-item.is-active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 800;
  border-color: #bfdbfe;
}

.exam-hub-nav-item.is-active .nav-icon {
  color: #2563eb !important;
}

.hub-count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 1px 7px;
  border-radius: 9999px;
  font-size: 0.72rem;
  font-weight: 800;
  line-height: 1.4;
}

.hub-count-badge.badge-purple {
  background: #f3e8ff;
  color: #7e22ce;
  border: 1px solid #e9d5ff;
}

.hub-count-badge.badge-blue {
  background: #e0f2fe;
  color: #0369a1;
  border: 1px solid #bae6fd;
}

.hub-count-badge.badge-amber {
  background: #fef3c7;
  color: #b45309;
  border: 1px solid #fde68a;
}

.hub-count-badge.badge-green {
  background: #dcfce7;
  color: #15803d;
  border: 1px solid #bbf7d0;
}

@media (max-width: 1100px) {
  .exam-hub-nav-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .exam-hub-nav-container {
    grid-template-columns: 1fr;
  }
}
</style>
