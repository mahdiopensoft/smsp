<template>
  <div class="qb-bulk-complete-page-v4">


    <!-- Filters Control Bar (Theme Compatible) -->
    <filter-fields label="خيارات التصفية والبحث المتقدم" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Institution Type Selector (مدارس / جامعات / الكل) -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterInstitutionType"
            :items="institutionTypeOptions"
            item-title="text"
            item-value="value"
            class="mb-6"
            placeholder="نوع المؤسسة التعليمية"
            prepend-inner-icon="mdi-domain"
            hide-details
            density="compact"
            variant="outlined"
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

        <!-- 🏫 School Filters (المرحلة والصف والمسار) -->
        <template v-if="filterInstitutionType === 'school' || filterInstitutionType === 'all'">
          <auto-list v-if="filterInstitutionType === 'school'" v-model="filterStage" name="Stage" placeholder="المرحلة الدراسية" cols="3" :add="false" />
          <auto-list v-if="filterInstitutionType === 'school'" v-model="filterLevel" name="Level" placeholder="الصف الدراسي" cols="3" :add="false" />
          <auto-list v-if="filterInstitutionType === 'school'" v-model="filterTrack" name="Track" placeholder="المسار التعليمي" cols="3" :add="false" />
        </template>

        <!-- 🎓 University Filters (الكلية، القسم، التخصص، المقرر) -->
        <template v-if="filterInstitutionType === 'university'">
          <auto-list v-model="filterCollege" name="College" placeholder="الكلية الجامعية" cols="3" :add="false" @update:model-value="filterDepartment = null" />
          <auto-list v-model="filterDepartment" name="DepartmentByCollege" :param="filterCollege" placeholder="القسم الأكاديمي" cols="3" :add="false" :disabled="!filterCollege" @update:model-value="filterSpecialization = null" />
          <auto-list v-model="filterSpecialization" name="Specialization" :param="filterDepartment" placeholder="التخصص والبرنامج" cols="3" :add="false" :disabled="!filterDepartment" />
          <auto-list v-model="filterSemesterSubject" name="SemesterSubject" :param="filterSpecialization" placeholder="مقرر الفصل الجامعي" cols="3" :add="false" />
        </template>

        <!-- 🏢 Institute Filters (المجال، نظام التعليم، التخصص، الخطة، المادة) -->
        <template v-if="filterInstitutionType === 'institute'">
          <auto-list v-model="filterInstituteField" name="InstituteField" placeholder="المجال المهني" cols="3" :add="false" @update:model-value="filterInstituteSpecialization = null" />
          <auto-list v-model="filterInstituteEducationSystem" name="InstituteEducationSystem" placeholder="نظام التعليم" cols="3" :add="false" @update:model-value="filterInstituteSpecialization = null" />
          <auto-list v-model="filterInstituteSpecialization" name="InstituteSpecialization" :param="filterInstituteSpecParam" placeholder="التخصص المهني" cols="3" :add="false" :disabled="!filterInstituteField && !filterInstituteEducationSystem" @update:model-value="filterInstituteCurriculum = null" />
          <auto-list v-model="filterInstituteCurriculum" name="InstituteCurriculum" :param="filterInstituteSpecialization" placeholder="الخطة الدراسية" cols="3" :add="false" :disabled="!filterInstituteSpecialization" @update:model-value="filterInstituteSubject = null" />
          <auto-list v-model="filterInstituteSubject" name="InstituteSubject" :param="filterInstituteCurriculum" placeholder="المادة التدريبية" cols="3" :add="false" :disabled="!filterInstituteCurriculum" />
        </template>

        <!-- General Subject & Unit -->
        <auto-list v-if="filterInstitutionType !== 'university' && filterInstitutionType !== 'institute'" v-model="filterSubject" name="Subject" placeholder="المادة الدراسية" cols="3" :add="false" />
        <auto-list v-model="filterUnit" name="UnitBySubject"
          :param="filterInstitutionType === 'university' ? { semester_subject: filterSemesterSubject } : (filterInstitutionType === 'institute' ? { institute_subject: filterInstituteSubject } : filterSubject)"
          :placeholder="filterInstitutionType === 'university' ? 'مفردة / موضوع المقرر' : (filterInstitutionType === 'institute' ? 'الوحدة التدريبية' : 'الوحدة الدراسية')"
          cols="3" :add="false"
          :disabled="filterInstitutionType === 'university' ? !filterSemesterSubject : (filterInstitutionType === 'institute' ? !filterInstituteSubject : !filterSubject)" />

        <!-- Difficulty & Bloom & Readiness -->
        <auto-list v-model="filterDifficulty" name="Difficulty" placeholder="مستوى الصعوبة" cols="3" :add="false" />

        <!-- Bloom Level -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterBloom"
            :items="['تذكر', 'فهم', 'تطبيق', 'تحليل', 'تقييم', 'ابتكار']"
            placeholder="مستوى بلوم"
            prepend-inner-icon="mdi-brain"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Readiness Filter -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterReadiness"
            :items="readinessOptions"
            item-title="title"
            item-value="value"
            placeholder="حالة الاكتمال"
            prepend-inner-icon="mdi-filter-check-outline"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Filter Actions -->
        <v-col cols="12" sm="6" md="3" class="d-flex align-center gap-2">
          <custom-btn
            type="show"
            label="تصفية"
            color="primary"
            class="font-weight-bold flex-grow-1 mb-6"
            :click="loadData"
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

    <!-- Bulk Action Tool Bar -->
    <v-card elevation="0" class="main-card pa-4 rounded-2xl mb-6 border">
      <div class="d-flex flex-column flex-md-row align-center justify-space-between gap-4">
        <!-- Selection Status & Selection Buttons -->
        <div class="d-flex align-center gap-3">
          <v-chip color="primary" variant="tonal" class="font-weight-bold">
            تم تحديد {{ selectedQuestions.length }} من {{ currentQuestionsList.length }}
          </v-chip>
          <custom-btn
            :label="selectedQuestions.length === currentQuestionsList.length && currentQuestionsList.length > 0 ? 'إلغاء تحديد الكل' : 'تحديد الكل'"
            variant="text"
            color="primary"
            class="font-weight-bold"
            :click="selectAllQuestions"
          />
        </div>

        <!-- Action Buttons Group -->
        <div class="d-flex align-center flex-wrap gap-2">
          <!-- Assign Unit & Lesson -->
          <custom-btn
            label="تعيين الدرس والوحدة"
            icon="mdi-book-arrow-right-outline"
            color="indigo"
            variant="tonal"
            class="font-weight-bold"
            :disabled="selectedQuestions.length === 0"
            :click="() => openAssignDialog('curriculum')"
          />

          <!-- Assign Bloom -->
          <custom-btn
            label="تعيين مستوى بلوم"
            icon="mdi-brain"
            color="purple"
            variant="tonal"
            class="font-weight-bold"
            :disabled="selectedQuestions.length === 0"
            :click="() => openAssignDialog('bloom')"
          />

          <!-- Assign Difficulty -->
          <custom-btn
            label="تعيين الصعوبة"
            icon="mdi-gauge"
            color="teal"
            variant="tonal"
            class="font-weight-bold"
            :disabled="selectedQuestions.length === 0"
            :click="() => openAssignDialog('difficulty')"
          />

          <v-divider vertical class="mx-2 d-none d-md-block" />

          <!-- Bulk Activate Button -->
          <custom-btn
            label="نقل المحدد إلى مسودة"
            icon="mdi-check-all"
            color="success"
            class="font-weight-bold px-5"
            :disabled="selectedQuestions.length === 0"
            :loading="activating"
            :click="bulkActivate"
          />
        </div>
      </div>
    </v-card>

    <!-- Custom Data Table -->
    <div class="main-card rounded-2xl overflow-hidden mb-8">
      <custom-data-table
        :headers="headers"
        :items="tableItems"
        :getData="getData"
        :customLoading="loading"
        class="bg-transparent"
        :hasFilter="false"
        :log="false"
        :restore="false"
      >
        <template v-slot:item-slot="{ item, key }">
          <!-- Selection Checkbox -->
          <template v-if="key === 'select'">
            <div class="d-flex justify-center">
              <v-checkbox-btn
                :model-value="isSelected(item.id)"
                @update:model-value="toggleSelect(item.id)"
                density="compact"
                color="primary"
              />
            </div>
          </template>

          <!-- Question Content Snippet -->
          <template v-else-if="key === 'content'">
            <div class="py-1">
              <div
                class="font-weight-bold text-body-2 text-truncate"
                style="max-width: 340px; cursor: pointer"
                @click="openPreviewDialog(item)"
              >
                {{ stripHtml(item.content) }}
              </div>
              <div class="d-flex align-center gap-2 mt-1">
                <span class="text-caption text-medium-emphasis">#{{ item.id }}</span>
                <v-chip size="x-small" color="secondary" variant="tonal" class="font-weight-medium">
                  {{ getTypeText(item.questionType) }}
                </v-chip>
                <v-chip v-if="item.defaultMark" size="x-small" color="primary" variant="tonal">
                  {{ item.defaultMark }} درجات
                </v-chip>
              </div>
            </div>
          </template>

          <!-- Subject & Lesson -->
          <template v-else-if="key === 'curriculum'">
            <div>
              <div class="text-body-2 font-weight-bold text-primary">
                {{ item.subject_name || getSubjectName(item) || 'غير محدد' }}
              </div>
              <div class="mt-1">
                <v-chip
                  v-if="item.lesson"
                  size="small"
                  color="indigo"
                  variant="tonal"
                  class="font-weight-bold"
                >
                  <v-icon start size="14">mdi-book-open-page-variant</v-icon>
                  {{ item.lesson_name || `درس #${item.lesson}` }}
                </v-chip>
                <v-chip
                  v-else
                  size="small"
                  color="error"
                  variant="tonal"
                  class="font-weight-bold text-white"
                >
                  <v-icon start size="14">mdi-alert-circle</v-icon>
                  الدرس غير محدد
                </v-chip>
              </div>
            </div>
          </template>

          <!-- Bloom Level -->
          <template v-else-if="key === 'bloomLevel'">
            <v-chip size="small" color="purple" variant="tonal" class="font-weight-bold">
              <v-icon start size="14">mdi-brain</v-icon>
              {{ item.bloomLevel || 'تذكر' }}
            </v-chip>
          </template>

          <!-- Difficulty -->
          <template v-else-if="key === 'difficulty'">
            <v-chip
              size="small"
              :color="getDifficultyColor(item.difficulty)"
              variant="tonal"
              class="font-weight-bold text-white"
            >
              {{ getDifficultyText(item.difficulty) }}
            </v-chip>
          </template>

          <!-- Learning Outcome -->
          <template v-else-if="key === 'learningOutcome'">
            <span class="text-caption text-medium-emphasis">
              {{ item.learningOutcome ? `مخرج #${item.learningOutcome}` : 'غير مرتبط' }}
            </span>
          </template>

          <!-- Readiness Status -->
          <template v-else-if="key === 'readiness'">
            <v-chip
              size="small"
              :color="item.lesson ? 'success' : 'warning'"
              variant="tonal"
              class="font-weight-bold text-white"
            >
              <v-icon start size="14">{{ item.lesson ? 'mdi-check-circle' : 'mdi-clock-outline' }}</v-icon>
              {{ item.lesson ? 'جاهز للنقل' : 'ناقص الدرس' }}
            </v-chip>
          </template>

          <!-- Actions -->
          <template v-else-if="key === 'actions'">
            <div class="d-flex align-center justify-center gap-1">
              <custom-btn
                is-icon
                icon="eye-outline"
                color="primary"
                variant="text"
                :click="() => openPreviewDialog(item)"
              />
              <custom-btn
                is-icon
                icon="pencil-outline"
                color="indigo"
                variant="text"
                :click="() => openSingleAssign(item)"
              />
            </div>
          </template>
        </template>
      </custom-data-table>
    </div>

    <!-- Bulk Assignment Dialog (CustomDialog Component) -->
    <CustomDialog
      v-model="assignDialog"
      width="560"
      :title="getAssignDialogTitle"
      :subTitle="`تطبيق التغييرات على (${selectedQuestions.length}) سؤال محدد`"
    >
      <!-- Curriculum Assign -->
      <div v-if="assignType === 'curriculum'">
        <div class="mb-4">
          <v-btn-toggle
            v-model="batchForm.institution_type"
            mandatory
            color="primary"
            variant="outlined"
            density="compact"
            rounded="lg"
            class="w-100 d-flex"
            @update:model-value="onBatchInstitutionTypeToggle"
          >
            <v-btn value="school" class="flex-grow-1 font-weight-bold">
              <v-icon start size="16">mdi-school</v-icon>
              مدرسي
            </v-btn>
            <v-btn value="university" class="flex-grow-1 font-weight-bold">
              <v-icon start size="16">mdi-domain</v-icon>
              جامعي
            </v-btn>
            <v-btn value="institute" class="flex-grow-1 font-weight-bold">
              <v-icon start size="16">mdi-domain</v-icon>
              معاهد
            </v-btn>
          </v-btn-toggle>
        </div>

        <!-- School -->
        <template v-if="batchForm.institution_type === 'school'">
          <auto-list
            v-model="batchForm.stageId"
            name="Stage"
            placeholder="اختر المرحلة الدراسية"
            cols="12"
            :add="false"
            @update:model-value="() => { batchForm.classTrackId = null; batchForm.subjectId = null; }"
          />
          <auto-list
            v-model="batchForm.classTrackId"
            name="ClassTrackByStage"
            :param="batchForm.stageId"
            placeholder="اختر الصف والمسار"
            cols="12"
            :add="false"
            :disabled="!batchForm.stageId"
            @update:model-value="batchForm.subjectId = null"
          />
          <auto-list
            v-model="batchForm.subjectId"
            name="Subject"
            :param="batchForm.classTrackId || batchForm.stageId"
            placeholder="اختر المادة الدراسية"
            cols="12"
            :add="false"
            :disabled="!batchForm.classTrackId && !batchForm.stageId"
            @update:model-value="onSubjectChange"
          />
        </template>

        <!-- University -->
        <template v-if="batchForm.institution_type === 'university'">
          <auto-list
            v-model="batchForm.collegeId"
            name="College"
            placeholder="الكلية الجامعية"
            cols="12"
            :add="false"
            @update:model-value="batchForm.departmentId = null"
          />
          <auto-list
            v-model="batchForm.departmentId"
            name="DepartmentByCollege"
            :param="batchForm.collegeId"
            placeholder="القسم الأكاديمي"
            cols="12"
            :add="false"
            :disabled="!batchForm.collegeId"
            @update:model-value="batchForm.specializationId = null"
          />
          <auto-list
            v-model="batchForm.specializationId"
            name="Specialization"
            :param="batchForm.departmentId"
            placeholder="التخصص والبرنامج"
            cols="12"
            :add="false"
            :disabled="!batchForm.departmentId"
            @update:model-value="batchForm.semesterSubjectId = null"
          />
          <auto-list
            v-model="batchForm.semesterSubjectId"
            name="SemesterSubject"
            :param="batchForm.specializationId"
            placeholder="مقرر الفصل الجامعي"
            cols="12"
            :add="false"
            @update:model-value="onSemesterSubjectChange"
          />
        </template>

        <!-- Institute -->
        <template v-if="batchForm.institution_type === 'institute'">
          <auto-list
            v-model="batchForm.instituteFieldId"
            name="InstituteField"
            placeholder="اختر المجال المهني"
            cols="12"
            :add="false"
            @update:model-value="batchForm.instituteSpecializationId = null"
          />
          <auto-list
            v-model="batchForm.instituteEducationSystemId"
            name="InstituteEducationSystem"
            placeholder="اختر نظام التعليم"
            cols="12"
            :add="false"
            @update:model-value="batchForm.instituteSpecializationId = null"
          />
          <auto-list
            v-model="batchForm.instituteSpecializationId"
            name="InstituteSpecialization"
            :param="batchInstituteSpecParam"
            placeholder="اختر التخصص المهني"
            cols="12"
            :add="false"
            :disabled="!batchForm.instituteFieldId && !batchForm.instituteEducationSystemId"
            @update:model-value="batchForm.instituteCurriculumId = null"
          />
          <auto-list
            v-model="batchForm.instituteCurriculumId"
            name="InstituteCurriculum"
            :param="batchForm.instituteSpecializationId"
            placeholder="اختر الخطة الدراسية"
            cols="12"
            :add="false"
            :disabled="!batchForm.instituteSpecializationId"
            @update:model-value="batchForm.instituteSubjectId = null"
          />
          <auto-list
            v-model="batchForm.instituteSubjectId"
            name="InstituteSubject"
            :param="batchForm.instituteCurriculumId"
            placeholder="اختر المادة التدريبية"
            cols="12"
            :add="false"
            :disabled="!batchForm.instituteCurriculumId"
            @update:model-value="onInstituteSubjectChange"
          />
        </template>

        <!-- Common: Unit, Lesson, Learning Outcome -->
        <auto-list
          v-model="batchForm.unitId"
          name="UnitBySubject"
          :param="batchForm.institution_type === 'university' ? { semester_subject: batchForm.semesterSubjectId } : (batchForm.institution_type === 'institute' ? { institute_subject: batchForm.instituteSubjectId } : { subject: batchForm.subjectId })"
          :placeholder="batchForm.institution_type === 'university' ? 'مفردة / موضوع المقرر' : (batchForm.institution_type === 'institute' ? 'الوحدة التدريبية' : 'الوحدة الدراسية')"
          cols="12"
          :add="false"
          :disabled="batchForm.institution_type === 'university' ? !batchForm.semesterSubjectId : (batchForm.institution_type === 'institute' ? !batchForm.instituteSubjectId : !batchForm.subjectId)"
          @update:model-value="onUnitChange"
        />
        <auto-list
          v-model="batchForm.lessonId"
          name="LessonByUnit"
          :param="batchForm.unitId"
          :placeholder="batchForm.institution_type === 'university' ? 'المحاضرة / الدرس الأكاديمي *' : (batchForm.institution_type === 'institute' ? 'الدرس / التمرين العملي *' : 'الدرس المدرسي *')"
          cols="12"
          :add="false"
          :disabled="!batchForm.unitId"
        />
        <auto-list
          v-model="batchForm.learningOutcomeId"
          name="LearningOutcome"
          :param="batchForm.unitId"
          :placeholder="batchForm.institution_type === 'university' ? 'مخرج تعلم المقرر (CLO)' : (batchForm.institution_type === 'institute' ? 'مخرج التدريب المستهدف (اختياري)' : 'مخرج التعلم المستهدف (اختياري)')"
          cols="12"
          :add="false"
          :disabled="!batchForm.unitId"
        />
      </div>

      <!-- Bloom Level Assign -->
      <div v-else-if="assignType === 'bloom'">
        <v-select
          v-model="batchForm.bloomLevel"
          :items="['تذكر', 'فهم', 'تطبيق', 'تحليل', 'تقييم', 'ابتكار']"
          label="مستوى بلوم المعرفي *"
          variant="outlined"
          density="compact"
        />
      </div>

      <!-- Difficulty Assign -->
      <div v-else-if="assignType === 'difficulty'">
        <v-select
          v-model="batchForm.difficulty"
          :items="[
            { title: 'سهل', value: 1 },
            { title: 'متوسط', value: 2 },
            { title: 'صعب', value: 3 }
          ]"
          label="مستوى الصعوبة التقديرية *"
          variant="outlined"
          density="compact"
        />
      </div>

      <template #actions>
        <custom-btn
          type="cancel"
          :click="() => assignDialog = false"
          variant="text"
          label="إلغاء"
          class="font-weight-bold"
        />
        <custom-btn
          type="add"
          :click="submitBatchAssign"
          :loading="savingBatch"
          color="primary"
          label="تطبيق التغييرات"
          class="font-weight-bold ms-auto"
        />
      </template>
    </CustomDialog>

    <!-- Question Preview Modal (CustomDialog Component) -->
    <CustomDialog
      v-model="previewDialog"
      width="700"
      title="معاينة تفاصيل السؤال"
      :subTitle="previewQuestion ? `#${previewQuestion.id} • ${getTypeText(previewQuestion.questionType)}` : ''"
    >
      <template v-if="previewQuestion">
        <!-- Badges -->
        <div class="d-flex flex-wrap gap-2 mb-4">
          <v-chip :color="previewQuestion.lesson ? 'success' : 'warning'" variant="tonal" class="font-weight-bold text-white">
            {{ previewQuestion.lesson ? 'جاهز للنقل' : 'ناقص الدرس' }}
          </v-chip>
          <v-chip :color="getDifficultyColor(previewQuestion.difficulty)" variant="tonal" class="font-weight-bold text-white">
            {{ getDifficultyText(previewQuestion.difficulty) }}
          </v-chip>
          <v-chip color="purple" variant="tonal" class="font-weight-bold">
            <v-icon start size="14">mdi-brain</v-icon> {{ previewQuestion.bloomLevel || 'تذكر' }}
          </v-chip>
          <v-chip v-if="previewQuestion.defaultMark" color="primary" variant="tonal" class="font-weight-bold">
            {{ previewQuestion.defaultMark }} درجات
          </v-chip>
        </div>

        <!-- Question Body Box -->
        <div class="question-preview-box pa-4 rounded-xl mb-4 bg-slate-50 border">
          <div class="text-body-1 font-weight-medium" style="line-height: 1.8" v-html="previewQuestion.content"></div>
        </div>

        <!-- Answers / Options -->
        <div v-if="previewQuestion.options && previewQuestion.options.length" class="mb-4">
          <h4 class="text-subtitle-2 font-weight-bold mb-2">الخيارات والإجابات:</h4>
          <div
            v-for="(ans, idx) in previewQuestion.options"
            :key="idx"
            class="pa-3 rounded-lg mb-2 d-flex align-center gap-2 border"
            :style="ans.isTrue ? 'background: rgba(22, 163, 74, 0.08); border-color: rgba(22, 163, 74, 0.4);' : 'background: rgba(0, 0, 0, 0.02);'"
          >
            <v-avatar size="24" :color="ans.isTrue ? 'success' : 'surface-variant'">
              <v-icon size="14" color="white">{{ ans.isTrue ? 'mdi-check' : 'mdi-circle-outline' }}</v-icon>
            </v-avatar>
            <span class="text-body-2" :class="{ 'font-weight-bold text-success': ans.isTrue }" v-html="ans.text"></span>
          </div>
        </div>
      </template>

      <template #actions>
        <custom-btn
          type="cancel"
          :click="() => previewDialog = false"
          variant="text"
          label="إغلاق"
          class="font-weight-bold"
        />
        <custom-btn
          v-if="previewQuestion"
          label="تعديل وتعيين الدرس"
          color="indigo"
          class="font-weight-bold ms-auto"
          :click="() => { previewDialog = false; openSingleAssign(previewQuestion); }"
        />
      </template>
    </CustomDialog>
  </div>
</template>

<script>
import { bankService } from '@/services/bankService'
import { academicService } from '@/services/academicService'

export default {
  name: 'QuestionBulkCompleteView',

  data() {
    return {
      loading: false,
      activating: false,
      savingBatch: false,

      // Questions Data (Server-driven)
      tableItems: { results: [], pagination: {} },
      selectedQuestions: [],

      // Filters
      filterInstitutionType: 'all',
      institutionTypeOptions: [
        { text: "الكل (مدارس، جامعات، معاهد)", value: "all" },
        { text: "🏫 مدارس فقط", value: "school" },
        { text: "🎓 جامعات فقط", value: "university" },
        { text: "🏢 معاهد وتدريب مهني فقط", value: "institute" },
      ],
      // Institute Filters
      filterInstituteField: null,
      filterInstituteEducationSystem: null,
      filterInstituteSpecialization: null,
      filterInstituteCurriculum: null,
      filterInstituteSubject: null,
      // University Filters
      filterCollege: null,
      filterDepartment: null,
      filterSpecialization: null,
      filterSemesterSubject: null,
      // School Filters
      filterStage: null,
      filterLevel: null,
      filterTrack: null,
      // General Filters
      filterSubject: null,
      filterUnit: null,
      filterDifficulty: null,
      filterBloom: null,
      filterReadiness: null,

      readinessOptions: [
        { title: 'جاهز للنقل (محدد الدرس)', value: 'ready' },
        { title: 'ناقص (غير محدد الدرس)', value: 'missing' },
      ],

      // Dialogs
      assignDialog: false,
      assignType: 'curriculum', // 'curriculum' | 'bloom' | 'difficulty'
      previewDialog: false,
      previewQuestion: null,

      // Academic Lists
      subjects: [],
      units: [],
      lessons: [],

      // Form State
      batchForm: {
        institution_type: 'school',
        subjectId: null,
        collegeId: null,
        departmentId: null,
        specializationId: null,
        semesterSubjectId: null,
        instituteFieldId: null,
        instituteEducationSystemId: null,
        instituteSpecializationId: null,
        instituteCurriculumId: null,
        instituteSubjectId: null,
        unitId: null,
        lessonId: null,
        learningOutcomeId: null,
        bloomLevel: 'تذكر',
        difficulty: 1,
      },

      // Table Headers Configuration
      headers: [
        { title: "تحديد", key: "select", sortable: false, width: "60px", align: "center" },
        { title: "نص السؤال", key: "content", sortable: false },
        { title: "المادة والدرس", key: "curriculum", sortable: true },
        { title: "مستوى بلوم", key: "bloomLevel", sortable: true, align: "center" },
        { title: "الصعوبة", key: "difficulty", sortable: true, align: "center" },
        { title: "مخرج التعلم", key: "learningOutcome", sortable: false, align: "center" },
        { title: "حالة الاكتمال", key: "readiness", sortable: true, align: "center" },
        { title: "الإجراءات", key: "actions", sortable: false, align: "center", width: "100px" },
      ],
    }
  },

  computed: {
    currentQuestionsList() {
      return this.tableItems.results || []
    },

    filterInstituteSpecParam() {
      const p = {}
      if (this.filterInstituteField) p.field = this.filterInstituteField
      if (this.filterInstituteEducationSystem) p.education_system = this.filterInstituteEducationSystem
      return Object.keys(p).length ? p : null
    },

    batchInstituteSpecParam() {
      const p = {}
      if (this.batchForm.instituteFieldId) p.field = this.batchForm.instituteFieldId
      if (this.batchForm.instituteEducationSystemId) p.education_system = this.batchForm.instituteEducationSystemId
      return Object.keys(p).length ? p : null
    },

    getAssignDialogTitle() {
      if (this.assignType === 'curriculum') return 'تعيين المادة والوحدة والدرس ومخرج التعلم'
      if (this.assignType === 'bloom') return 'تعيين مستوى بلوم المعرفي'
      if (this.assignType === 'difficulty') return 'تعيين مستوى الصعوبة التقديرية'
      return 'تعيين جماعي'
    },
  },

  methods: {
    async getData(params = {}) {
      this.loading = true
      try {
        const queryParams = {
          ...params,
          institution_type: (this.filterInstitutionType && this.filterInstitutionType !== 'all') ? this.filterInstitutionType : undefined,
          college: this.filterCollege || undefined,
          department: this.filterDepartment || undefined,
          specialization: (this.filterInstitutionType === 'institute' ? this.filterInstituteSpecialization : this.filterSpecialization) || undefined,
          semester_subject: this.filterSemesterSubject || undefined,
          stage: this.filterStage || undefined,
          level: this.filterLevel || undefined,
          track: this.filterTrack || undefined,
          field: this.filterInstituteField || undefined,
          education_system: this.filterInstituteEducationSystem || undefined,
          curriculum: this.filterInstituteCurriculum || undefined,
          subject: (this.filterInstitutionType === 'institute' ? this.filterInstituteSubject : this.filterSubject) || undefined,
          unit: this.filterUnit || undefined,
          difficulty: this.filterDifficulty || undefined,
          bloom_level: this.filterBloom || undefined,
          readiness: this.filterReadiness || undefined,
        }
        const data = await bankService.getImportedList(queryParams)
        if (Array.isArray(data)) {
          this.tableItems = {
            results: data,
            pagination: { count: data.length, total: data.length }
          }
        } else {
          this.tableItems = data
        }
        this.selectedQuestions = []
      } catch (err) {
        console.error('Failed to load imported questions', err)
      } finally {
        this.loading = false
      }
    },

    onInstitutionTypeChange() {
      this.filterStage = null
      this.filterLevel = null
      this.filterTrack = null
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
      this.filterUnit = null
      this.loadData()
    },

    onBatchInstitutionTypeToggle() {
      this.batchForm.subjectId = null
      this.batchForm.collegeId = null
      this.batchForm.departmentId = null
      this.batchForm.specializationId = null
      this.batchForm.semesterSubjectId = null
      this.batchForm.instituteFieldId = null
      this.batchForm.instituteEducationSystemId = null
      this.batchForm.instituteSpecializationId = null
      this.batchForm.instituteCurriculumId = null
      this.batchForm.instituteSubjectId = null
      this.batchForm.unitId = null
      this.batchForm.lessonId = null
      this.batchForm.learningOutcomeId = null
    },

    onInstituteSubjectChange() {
      this.batchForm.unitId = null
      this.batchForm.lessonId = null
      this.batchForm.learningOutcomeId = null
    },

    onSemesterSubjectChange() {
      this.batchForm.unitId = null
      this.batchForm.lessonId = null
      this.batchForm.learningOutcomeId = null
    },

    async loadData() {
      await this.getData()
    },

    async loadSubjects() {
      try {
        const res = await academicService.getSubjects()
        this.subjects = (res.results || res || []).map(s => ({
          id: s.id,
          name: s.name_ar || s.name_en || s.name || `مادة #${s.id}`,
        }))
      } catch (err) {
        console.error(err)
      }
    },

    async onSubjectChange() {
      this.batchForm.unitId = null
      this.batchForm.lessonId = null
      this.units = []
      this.lessons = []
      if (!this.batchForm.subjectId) return
      try {
        const res = await academicService.getUnits({ subject_id: this.batchForm.subjectId })
        this.units = (res.results || res || []).map(u => ({
          id: u.id,
          name: u.name_ar || u.name_en || u.name || `وحدة #${u.id}`,
        }))
      } catch (err) {
        console.error(err)
      }
    },

    async onUnitChange() {
      this.batchForm.lessonId = null
      this.lessons = []
      if (!this.batchForm.unitId) return
      try {
        const res = await academicService.getLessons({ unit_id: this.batchForm.unitId })
        this.lessons = (res.results || res || []).map(l => ({
          id: l.id,
          name: l.name_ar || l.name_en || l.name || `درس #${l.id}`,
        }))
      } catch (err) {
        console.error(err)
      }
    },

    isSelected(id) {
      return this.selectedQuestions.includes(id)
    },

    toggleSelect(id) {
      const idx = this.selectedQuestions.indexOf(id)
      if (idx > -1) {
        this.selectedQuestions.splice(idx, 1)
      } else {
        this.selectedQuestions.push(id)
      }
    },

    selectAllQuestions() {
      if (this.selectedQuestions.length === this.currentQuestionsList.length) {
        this.selectedQuestions = []
      } else {
        this.selectedQuestions = this.currentQuestionsList.map(q => q.id)
      }
    },

    openAssignDialog(type) {
      this.assignType = type
      this.assignDialog = true
    },

    openSingleAssign(item) {
      this.selectedQuestions = [item.id]
      if (item.institution_type) {
        this.batchForm.institution_type = item.institution_type
      }
      this.assignType = 'curriculum'
      this.assignDialog = true
    },

    openPreviewDialog(item) {
      this.previewQuestion = item
      this.previewDialog = true
    },

    async submitBatchAssign() {
      this.savingBatch = true
      try {
        const payload = {
          question_ids: this.selectedQuestions,
        }
        if (this.assignType === 'curriculum') {
          payload.institution_type = this.batchForm.institution_type
          if (this.batchForm.lessonId) payload.lesson_id = this.batchForm.lessonId
          if (this.batchForm.learningOutcomeId) payload.learning_outcome_id = this.batchForm.learningOutcomeId
        }
        if (this.assignType === 'bloom') {
          payload.bloom_level = this.batchForm.bloomLevel
        }
        if (this.assignType === 'difficulty') {
          payload.difficulty = this.batchForm.difficulty
        }

        await bankService.bulkAssignImported(payload)
        this.assignDialog = false
        await this.loadData()
      } catch (err) {
        console.error('Batch assign error', err)
      } finally {
        this.savingBatch = false
      }
    },

    async bulkActivate() {
      this.activating = true
      try {
        await bankService.bulkActivateImported({
          question_ids: this.selectedQuestions,
          target_status: 'مسودة',
        })
        await this.loadData()
      } catch (err) {
        console.error('Activation error', err)
      } finally {
        this.activating = false
      }
    },

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
      this.filterStage = null
      this.filterLevel = null
      this.filterTrack = null
      this.filterSubject = null
      this.filterUnit = null
      this.filterDifficulty = null
      this.filterBloom = null
      this.filterReadiness = null
      this.loadData()
    },

    stripHtml(html) {
      if (!html) return ''
      const tmp = document.createElement('DIV')
      tmp.innerHTML = html
      return tmp.textContent || tmp.innerText || ''
    },

    getTypeText(type) {
      const map = {
        single_choice: 'اختيار واحد',
        multiple_choice: 'اختيارات متعددة',
        true_false: 'صواب / خطأ',
        essay: 'مقالي',
        fill_blank: 'إكمال الفراغ',
        matching: 'مطابقة',
        ordering: 'ترتيب',
        case_study: 'دراسة حالة',
      }
      return map[type] || type || 'سؤال'
    },

    getDifficultyText(val) {
      if (val === 1) return 'سهل'
      if (val === 2) return 'متوسط'
      if (val === 3) return 'صعب'
      return 'غير محدد'
    },

    getDifficultyColor(val) {
      if (val === 1) return 'success'
      if (val === 2) return 'warning'
      if (val === 3) return 'error'
      return 'grey'
    },

    getSubjectName(item) {
      if (!item) return ''
      if (typeof item.subject === 'object' && item.subject) {
        return item.subject.name_ar || item.subject.name_en || item.subject.name || ''
      }
      return item.subject || ''
    },
  },

  mounted() {
    this.loadData()
    this.loadSubjects()
  },
}
</script>

<style scoped>
.main-card {
  background: white;
  border-color: rgba(0, 0, 0, 0.08) !important;
}


</style>
