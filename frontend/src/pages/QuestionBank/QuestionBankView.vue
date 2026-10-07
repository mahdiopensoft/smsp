<template>
  <div class="qb-page-v4">




    <!-- Filters Control Bar (Theme Compatible) -->
    <filter-fields label="خيارات التصفية المتقدمة" class="main-card border-0 pa-5 rounded-2xl mb-8">
      <v-row dense class="align-center">
        <!-- Institution Type Selector (مدارس / جامعات / الكل) -->
        <v-col cols="12" sm="6" md="3">
          <v-select v-model="filterInstitutionType" :items="institutionTypeOptions" item-title="text" item-value="value"
            class="mb-6" placeholder="نوع المؤسسة التعليمية" prepend-inner-icon="mdi-domain" hide-details
            density="compact" variant="outlined" @update:model-value="onInstitutionTypeChange" />
        </v-col>

        <!-- 🏫 School Filters (المرحلة والصف والمسار) -->
        <template v-if="filterInstitutionType === 'school' || filterInstitutionType === 'all'">
          <auto-list v-if="filterInstitutionType === 'school'" v-model="filterStage" name="Stage"
            placeholder="المرحلة الدراسية" cols="3" sm="6" md="3" :add="false" @update:model-value="onStageChange" />
          <auto-list v-if="filterInstitutionType === 'school'" v-model="filterClassTrack" name="ClassTrackByStage"
            :param="filterStage" placeholder="الصف والمسار المدرسي" cols="3" sm="6" md="3" :add="false"
            :disabled="!filterStage" @update:model-value="onClassTrackChange" />
        </template>

        <!-- 🎓 University Filters (الكلية، القسم، التخصص، المقرر) -->
        <template v-if="filterInstitutionType === 'university'">
          <auto-list v-model="filterCollege" name="College" placeholder="الكلية الجامعية" cols="3" sm="6" md="3"
            :add="false" @update:model-value="onCollegeChange" />
          <auto-list v-model="filterDepartment" name="DepartmentByCollege" :param="filterCollege"
            placeholder="القسم الأكاديمي" cols="3" sm="6" md="3" :add="false" :disabled="!filterCollege"
            @update:model-value="onDepartmentChange" />
          <auto-list v-model="filterSpecialization" name="Specialization" :param="filterDepartment"
            placeholder="التخصص والبرنامج" cols="3" sm="6" md="3" :add="false" :disabled="!filterDepartment"
            @update:model-value="onSpecializationChange" />
          <auto-list v-model="filterSemesterSubject" name="SemesterSubject" :param="filterSpecialization"
            placeholder="مقرر الفصل الجامعي" cols="3" sm="6" md="3" :add="false"
            @update:model-value="onSemesterSubjectChange" />
        </template>

        <!-- 🏢 Institute Filters (المجال المهني، نظام التعليم، التخصص، المادة) -->
        <template v-if="filterInstitutionType === 'institute'">
          <auto-list v-model="filterInstituteField" name="InstituteField" placeholder="المجال المهني / التقني"
            cols="3" sm="6" md="3" :add="false" @update:model-value="onInstituteFieldChange" />
          <auto-list v-model="filterInstituteEducationSystem" name="InstituteEducationSystem"
            :param="filterInstituteField" placeholder="نظام التعليم والتدريب" cols="3" sm="6" md="3" :add="false"
            :disabled="!filterInstituteField" @update:model-value="onInstituteEducationSystemChange" />
          <auto-list v-model="filterInstituteSpecialization" name="InstituteSpecialization"
            :param="{ field: filterInstituteField, education_system: filterInstituteEducationSystem }"
            placeholder="التخصص المهني" cols="3" sm="6" md="3" :add="false"
            :disabled="!filterInstituteEducationSystem" @update:model-value="onInstituteSpecializationChange" />
          <auto-list v-model="filterInstituteSubject" name="InstituteSubject"
            :param="{ field: filterInstituteField }" placeholder="المادة الدراسية للمعهد" cols="3" sm="6" md="3"
            :add="false" @update:model-value="onInstituteSubjectChange" />
        </template>

        <!-- General Subject (المادة للمدارس أو النمط العام) -->
        <auto-list v-if="filterInstitutionType !== 'university' && filterInstitutionType !== 'institute'" v-model="filterSubject" name="Subject" :param="subjectFilterParam" placeholder="المادة الدراسية"
          cols="3" sm="6" md="3" :add="false" @update:model-value="onSubjectChange" />

        <!-- Unit / Topic (الوحدة الدراسية للمدارس / مفردة المقرر للجامعات / الوحدة للمعاهد) -->
        <auto-list v-model="filterUnit" name="UnitBySubject"
          :param="filterInstitutionType === 'university' ? { semester_subject: filterSemesterSubject } : (filterInstitutionType === 'institute' ? { subject: filterInstituteSubject } : filterSubject)"
          :placeholder="filterInstitutionType === 'university' ? 'مفردة / موضوع المقرر' : (filterInstitutionType === 'institute' ? 'الوحدة / التدريب العملي' : 'الوحدة الدراسية')"
          cols="3" sm="6" md="3" :add="false"
          :disabled="filterInstitutionType === 'university' ? !filterSemesterSubject : (filterInstitutionType === 'institute' ? !filterInstituteSubject : !filterSubject)" />

        <!-- Status -->
        <v-col cols="3" sm="6" md="3">
          <v-select v-model="filterStatus" :items="statusOptions" item-title="text" item-value="value" class="mb-6"
            placeholder="حالة السؤال" prepend-inner-icon="mdi-flag-outline" hide-details clearable density="compact"
            variant="outlined" />
        </v-col>

        <!-- Difficulty & Question Type -->
        <auto-list v-model="filterDifficulty" name="Difficulty" placeholder="مستوى الصعوبة" cols="3" sm="6" md="3"
          :add="false" />
        <auto-list v-model="filterType" name="QuestionType" placeholder="نوع السؤال" cols="3" sm="6" md="3"
          :add="false" />

        <!-- Bloom Level -->
        <v-col cols="3" sm="6" md="3">
          <v-select v-model="filterBloom" :items="bloomOptions" item-title="title" item-value="value" class="mb-6"
            placeholder="مستوى بلوم المعرفي" prepend-inner-icon="mdi-brain" hide-details clearable density="compact"
            variant="outlined" />
        </v-col>

        <!-- Filter Actions -->
        <v-col cols="3" sm="12" md="3" class="d-flex align-center gap-2">
          <custom-btn type="show" label="تصفية" color="primary" class="font-weight-bold flex-grow-1 mb-6"
            :click="applyFilters" />
          <custom-btn type="cancel_filter" :click="resetFilters" variant="tonal" color="error" label="تفريغ"
            class="font-weight-bold mb-6" />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Table View -->
    <div class="main-card rounded-2xl overflow-hidden mb-8">
      <custom-data-table :headers="headers" :items="items" :getData="getData" :customLoading="loading"
        class="bg-transparent" :hasFilter="false" :log="false" :restore="false">
        <template v-slot:item-slot="{ item, key }">
          <!-- Content Snippet -->
          <template v-if="key === 'content'">
            <span class="text-truncate font-weight-medium d-inline-block" style="max-width: 360px">
              {{ stripHtml(item.content) }}
            </span>
          </template>

          <template v-else-if="key === 'subject'">
            <div>
              <div class="text-body-2 font-weight-bold text-primary">{{ item.subject_name || getSubjectName(item) }}
              </div>
              <div class="text-caption text-medium-emphasis" v-if="item.lesson_name">{{ item.lesson_name }}</div>
            </div>
          </template>

          <template v-else-if="key === 'status'">
            <v-chip :color="getStatusColor(item.status)" variant="tonal" size="small"
              class="font-weight-bold text-white">
              <v-icon start size="14">{{ getStatusIcon(item.status) }}</v-icon>
              {{ item.status }}
            </v-chip>
          </template>

          <template v-else-if="key === 'difficulty'">
            <v-chip :color="getDifficultyColor(item.difficulty)" variant="tonal" size="small"
              class="font-weight-bold text-white">
              <v-icon start size="14">{{ getDifficultyIcon(item.difficulty) }}</v-icon>
              {{ getDifficultyText(item.difficulty) }}
            </v-chip>
          </template>

          <template v-else-if="key === 'questionType'">
            <v-chip size="small" color="secondary" variant="tonal" class="font-weight-bold">
              {{ getTypeText(item.questionType) }}
            </v-chip>
          </template>

          <template v-else-if="key === 'defaultMark'">
            <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
              <v-icon start size="14">mdi-star</v-icon> {{ item.defaultMark || 1 }}
            </v-chip>
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

                  <v-card-text class="pa-2">
                    <v-list density="compact" class="bg-transparent pa-0">
                      <v-list-item @click="viewQuestion(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="primary" class="me-2">mdi-eye-outline</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium"
                          style="color: rgba(var(--v-theme-on-surface), 0.7)">
                          معاينة التفاصيل
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item v-if="item.status !== 'معتمد'" @click="editQuestion(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="warning" class="me-2">mdi-pencil-outline</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-warning">
                          تعديل السؤال
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item @click="duplicateQuestion(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="indigo" class="me-2">mdi-content-copy</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-indigo">
                          استنساخ السؤال
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item v-if="item.status === 'معتمد'" @click="createQuestionVersion(item)"
                        class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="teal" class="me-2">mdi-source-branch</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-teal">
                          إنشاء إصدار جديد (v{{ (item.version_number || 1) + 1 }})
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item v-if="item.status === 'مسودة'" @click="updateQuestionStatus(item, 'قيد المراجعة')"
                        class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="info" class="me-2">mdi-send-clock</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-info">
                          تقديم للمراجعة
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item v-if="item.status !== 'مؤرشف'" @click="archiveQuestion(item)"
                        class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="purple" class="me-2">mdi-archive-arrow-down-outline</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-purple">
                          أرشفة السؤال
                        </v-list-item-title>
                      </v-list-item>

                      <v-list-item v-else @click="restoreQuestion(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="success" class="me-2">mdi-archive-arrow-up-outline</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-success">
                          استعادة من الأرشيف
                        </v-list-item-title>
                      </v-list-item>

                      <v-divider class="my-1 opacity-20"></v-divider>

                      <v-list-item @click="openDeleteDialog(item)" class="premium-list-item">
                        <template v-slot:prepend>
                          <v-icon size="18" color="error" class="me-2">mdi-trash-can-outline</v-icon>
                        </template>
                        <v-list-item-title class="text-caption font-weight-medium text-error">
                          نقل للمهملات
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

    <!-- View Question Dialog -->
    <CustomDialog v-model="viewDialog" width="720" title="معاينة السؤال"
      :subTitle="selectedQuestion ? getTypeText(selectedQuestion.questionType) : ''">
      <template v-if="selectedQuestion">
        <!-- Loading indicator while full details are loaded on demand -->
        <v-progress-linear v-if="selectedQuestion._loading" indeterminate color="primary" class="mb-4 rounded" />

        <!-- Status Badges -->
        <div class="d-flex flex-wrap gap-2 mb-6">
          <v-chip :color="getStatusColor(selectedQuestion.status)" variant="tonal" class="font-weight-bold text-white">
            {{ selectedQuestion.status }}
          </v-chip>
          <v-chip :color="getDifficultyColor(selectedQuestion.difficulty)" variant="tonal"
            class="font-weight-bold text-white">
            <v-icon start size="14">{{ getDifficultyIcon(selectedQuestion.difficulty) }}</v-icon>
            {{ getDifficultyText(selectedQuestion.difficulty) }}
          </v-chip>
          <v-chip color="secondary" variant="tonal" class="font-weight-bold" v-if="selectedQuestion.bloomLevel">
            <v-icon start size="14">mdi-brain</v-icon> {{ selectedQuestion.bloomLevel }}
          </v-chip>
          <v-chip color="warning" variant="tonal" class="font-weight-bold">
            <v-icon start size="14">mdi-star</v-icon> {{ selectedQuestion.defaultMark || 1 }} درجة
          </v-chip>
          <v-chip color="info" variant="tonal" class="font-weight-bold" v-if="selectedQuestion.expected_time_minutes">
            <v-icon start size="14">mdi-timer-outline</v-icon> {{ selectedQuestion.expected_time_minutes }} دقيقة
          </v-chip>
        </div>

        <div class="question-content-box pa-5 rounded-2xl mb-6">
          <div v-if="selectedQuestion.description"
            class="text-subtitle-2 text-primary font-weight-bold mb-3 bg-primary-lighten-5 pa-3 rounded-lg border-s-4 border-primary d-flex align-center gap-2">
            <v-icon size="20">mdi-lightbulb-on-outline</v-icon> <span>فكرة السؤال: {{ selectedQuestion.description
              }}</span>
          </div>
          <div v-if="selectedQuestion.image" class="mb-4 text-center">
            <v-img :src="selectedQuestion.image" max-height="250" class="rounded-lg bg-surface-variant mx-auto"
              contain></v-img>
          </div>
          <div class="text-body-1 font-weight-medium" style="line-height: 2" v-html="selectedQuestion.content" />
        </div>

        <!-- Answers / Options -->
        <div v-if="selectedQuestion.options && selectedQuestion.options.length">
          <h4 class="text-subtitle-1 font-weight-bold mb-3">الإجابات والخيارات</h4>
          <div v-for="(answer, i) in selectedQuestion.options" :key="i"
            class="pa-4 rounded-xl mb-2 d-flex align-center gap-3 border"
            :style="answer.isTrue ? 'background: rgba(22, 163, 74, 0.08); border-color: rgba(22, 163, 74, 0.4);' : 'background: rgba(0, 0, 0, 0.02); border-color: rgba(0, 0, 0, 0.08);'">
            <v-avatar size="32" :color="answer.isTrue ? 'success' : 'surface-variant'">
              <v-icon size="18" color="white">{{ answer.isTrue ? 'mdi-check' : 'mdi-circle-outline' }}</v-icon>
            </v-avatar>
            <div class="d-flex flex-column">
              <span class="text-body-1" :class="{ 'font-weight-bold': answer.isTrue }" v-html="answer.text"></span>
              <v-img v-if="answer.image" :src="answer.image" max-height="100" contain class="mt-2 rounded" />
              <span v-if="answer.latex" class="text-caption font-weight-medium mt-1 dir-ltr text-left">{{ answer.latex
                }}</span>
            </div>
          </div>
        </div>

        <!-- Essay or Fill in the blank -->
        <div v-else-if="selectedQuestion.answerText">
          <h4 class="text-subtitle-1 font-weight-bold mb-3">الإجابة المرجعية</h4>
          <div class="pa-4 rounded-xl mb-2 border"
            style="background: rgba(22, 163, 74, 0.08); border-color: rgba(22, 163, 74, 0.4);">
            <div class="text-body-1 font-weight-bold text-success" v-html="selectedQuestion.answerText"></div>
          </div>
        </div>

        <!-- True/False if no options provided -->
        <div v-else-if="selectedQuestion.isTrue !== null && selectedQuestion.isTrue !== undefined">
          <h4 class="text-subtitle-1 font-weight-bold mb-3">الإجابة الصحيحة</h4>
          <div class="pa-4 rounded-xl mb-2 d-flex align-center gap-3 border"
            style="background: rgba(22, 163, 74, 0.08); border-color: rgba(22, 163, 74, 0.4);">
            <v-avatar size="32" color="success">
              <v-icon size="18" color="white">mdi-check</v-icon>
            </v-avatar>
            <span class="text-body-1 font-weight-bold text-success">
              {{ selectedQuestion.isTrue ? 'صح (True)' : 'خطأ (False)' }}
            </span>
          </div>
        </div>

        <!-- Psychometrics & Item Tracking Section -->
        <div v-if="selectedQuestion.metrics" class="mt-4 pa-4 rounded-2xl bg-slate-50 border">
          <h4 class="text-subtitle-2 font-weight-bold mb-3 d-flex align-center gap-2 text-indigo">
            <v-icon size="18">mdi-chart-bell-curve-cumulative</v-icon>
            مؤشرات القياس النفسي والأداء التراكمي
          </h4>
          <v-row dense>
            <v-col cols="6" sm="3">
              <div class="text-caption text-medium-emphasis">مرات الاستخدام</div>
              <div class="text-body-2 font-weight-black">{{ selectedQuestion.metrics.usage_count || 0 }}</div>
            </v-col>
            <v-col cols="6" sm="3">
              <div class="text-caption text-medium-emphasis">معامل الصعوبة (p-value)</div>
              <div class="text-body-2 font-weight-black text-primary">{{ selectedQuestion.metrics.actual_difficulty !=
                null ? selectedQuestion.metrics.actual_difficulty : 'غير محسوب' }}</div>
            </v-col>
            <v-col cols="6" sm="3">
              <div class="text-caption text-medium-emphasis">معامل التمييز (D)</div>
              <div class="text-body-2 font-weight-black text-teal">{{ selectedQuestion.metrics.discrimination_index !=
                null ? selectedQuestion.metrics.discrimination_index : 'غير محسوب' }}</div>
            </v-col>
            <v-col cols="6" sm="3">
              <div class="text-caption text-medium-emphasis">الارتباط النقطي (rpb)</div>
              <div class="text-body-2 font-weight-black text-purple">{{ selectedQuestion.metrics.point_biserial != null
                ? selectedQuestion.metrics.point_biserial : 'غير محسوب' }}</div>
            </v-col>
          </v-row>
        </div>

        <!-- Metadata Summary Row -->
        <v-divider class="my-6 opacity-20" />
        <v-row class="ma-0 pa-3 rounded-xl question-content-box">
          <v-col cols="6" sm="6">
            <div class="text-caption text-medium-emphasis mb-1">المادة</div>
            <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">{{
              getSubjectName(selectedQuestion) }}</v-chip>
          </v-col>
          <v-col cols="6" sm="6">
            <div class="text-caption text-medium-emphasis mb-1">تاريخ الإنشاء</div>
            <div class="text-body-2 font-weight-bold">{{ selectedQuestion.createdAt || '-' }}</div>
          </v-col>
        </v-row>
      </template>

      <template #actions>
        <custom-btn type="cancel" :click="() => viewDialog = false" variant="text" label="إغلاق"
          class="font-weight-bold" />
        <div class="d-flex align-center gap-2 ms-auto">
          <custom-btn v-if="selectedQuestion && selectedQuestion.status !== 'معتمد'" type="update"
            :click="() => { editQuestion(selectedQuestion); viewDialog = false; }" variant="tonal" color="warning"
            label="تعديل السؤال" class="font-weight-bold" />
          <custom-btn v-if="selectedQuestion && selectedQuestion.status === 'مسودة'" type="add"
            :click="() => { updateQuestionStatus(selectedQuestion, 'قيد المراجعة'); viewDialog = false; }" color="info"
            label="تقديم للمراجعة" class="font-weight-bold" />
        </div>
      </template>
    </CustomDialog>

    <!-- Delete Confirmation Modal -->
    <DeleteDialog v-model="deleteDialog" title="تأكيد الحذف"
      message="هل أنت متأكد من حذف هذا السؤال؟ سيتم نقله إلى سلة المحذوفات." @confirm-delete="executeDelete" />


  </div>
</template>

<script>

import { bankService } from "@/services/bankService";
import { academicService } from "@/services/academicService";

export default {
  name: "QuestionBankView",
  components: {
  },

  data() {
    return {
      // State
      loading: false,
      items: { results: [], pagination: {} },
      subjects: [],

      // Filters
      search: "",
      filterInstitutionType: "all",
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
      filterInstituteSubject: null,
      // University Filters
      filterCollege: null,
      filterDepartment: null,
      filterSpecialization: null,
      filterSemesterSubject: null,
      // School Filters
      filterStage: null,
      filterClassTrack: null,
      // General Filters
      filterSubject: null,
      filterUnit: null,
      filterDifficulty: null,
      filterStatus: null,
      filterType: null,
      filterBloom: null,

      statusOptions: [
        { text: "الكل", value: null },
        { text: "معتمد", value: "معتمد" },
        { text: "مسودة", value: "مسودة" },
        { text: "قيد المراجعة", value: "قيد المراجعة" },
        { text: "مرفوض", value: "مرفوض" },
      ],
      bloomOptions: [
        { title: "تذكر", value: "تذكر" },
        { title: "فهم", value: "فهم" },
        { title: "تطبيق", value: "تطبيق" },
        { title: "تحليل", value: "تحليل" },
        { title: "تقييم", value: "تقييم" },
        { title: "ابتكار", value: "ابتكار" },
      ],

      // Pagination
      currentPage: 1,
      itemsPerPage: 12,

      // Dialogs
      viewDialog: false,
      deleteDialog: false,
      selectedQuestion: null,
      questionToDelete: null,
      deleteLoading: false,

      // Options
      difficulties: [
        { name: "سهل", id: 1 },
        { name: "متوسط", id: 2 },
        { name: "صعب", id: 3 },
      ],
      questionTypes: [
        { name: "اختيار واحد", id: "single_choice" },
        { name: "اختيارات متعددة", id: "multiple_choice" },
        { name: "صواب/خطأ", id: "true_false" },
      ],

      // Table Headers
      headers: [
        { title: "السؤال", key: "content", sortable: false },
        { title: "المادة", key: "subject", sortable: true },
        { title: "نوع السؤال", key: "questionType", sortable: true },
        { title: "الصعوبة", key: "difficulty", sortable: true },
        { title: "الدرجة", key: "defaultMark", sortable: true, align: "center" },
        { title: "الحالة", key: "status", sortable: true },
      ],
    };
  },

  computed: {
    subjectFilterParam() {
      const p = {};
      if (this.filterInstitutionType && this.filterInstitutionType !== "all") {
        p.institution_type = this.filterInstitutionType;
      }
      if (this.filterClassTrack) {
        p.class_track = this.filterClassTrack;
      } else if (this.filterStage) {
        p.stage = this.filterStage;
      }
      if (this.filterSemesterSubject) {
        p.semester_subject = this.filterSemesterSubject;
      } else if (this.filterSpecialization) {
        p.specialization = this.filterSpecialization;
      } else if (this.filterDepartment) {
        p.department = this.filterDepartment;
      } else if (this.filterCollege) {
        p.college = this.filterCollege;
      }
      return Object.keys(p).length > 0 ? p : null;
    },
  },

  watch: {
    // Only watch page changes if table triggers it, but mostly custom-data-table handles its own.
  },

  async created() {
    await this.fetchData();
  },

  methods: {
    // === DATA FETCHING ===
    async fetchData() {
      this.loading = true;
      try {
        const subjectsRes = await academicService.getSubjects();
        this.subjects = (Array.isArray(subjectsRes) ? subjectsRes : subjectsRes?.data) || [];

        await this.getData();
      } catch (err) {
        console.error("فشل في تحميل البيانات:", err);
      } finally {
        this.loading = false;
      }
    },

    async getData(tableParams = null) {
      this.loading = true;
      try {
        let queryParams = {};
        if (tableParams && tableParams.params) {
          queryParams = { ...tableParams.params, hasPagination: true };
        } else {
          queryParams = { page: this.currentPage, perPage: this.itemsPerPage, hasPagination: true };
        }

        if (this.search) queryParams.search = this.search;
        if (queryParams.page) this.currentPage = queryParams.page;

        // Map local filters to backend API fields
        let filters = [];
        if (this.filterInstitutionType && this.filterInstitutionType !== "all") {
          filters.push({ field: "institution_type", value: this.filterInstitutionType });
        }
        if (this.filterStatus) filters.push({ field: "status", value: this.filterStatus });
        if (this.filterDifficulty) filters.push({ field: "difficulty", value: this.filterDifficulty });
        if (this.filterType) filters.push({ field: "questionType", value: this.filterType });
        if (this.filterBloom) filters.push({ field: "bloomLevel", value: this.filterBloom });
        if (this.filterSubject) {
          if (this.filterInstitutionType === "university") {
            filters.push({ field: "lesson__unit__semester_subject__fk_subject", value: this.filterSubject });
          } else if (this.filterInstitutionType === "school") {
            filters.push({ field: "lesson__unit__class_subject__subject", value: this.filterSubject });
          } else {
            queryParams.subject = this.filterSubject;
          }
        }
        if (this.filterUnit) filters.push({ field: "lesson__unit", value: this.filterUnit });

        // School filters
        if (this.filterStage) filters.push({ field: "lesson__unit__class_subject__class_track__level__stage", value: this.filterStage });
        if (this.filterClassTrack) filters.push({ field: "lesson__unit__class_subject__class_track", value: this.filterClassTrack });

        // University filters
        if (this.filterSemesterSubject) {
          filters.push({ field: "lesson__unit__semester_subject", value: this.filterSemesterSubject });
        } else if (this.filterSpecialization) {
          filters.push({ field: "lesson__unit__semester_subject__fk_specialization", value: this.filterSpecialization });
        } else if (this.filterDepartment) {
          filters.push({ field: "lesson__unit__semester_subject__fk_specialization__fk_section", value: this.filterDepartment });
        } else if (this.filterCollege) {
          filters.push({ field: "lesson__unit__semester_subject__fk_specialization__fk_college", value: this.filterCollege });
        }

        // Institute filters
        if (this.filterInstituteSubject) {
          filters.push({ field: "lesson__subject", value: this.filterInstituteSubject });
        }

        if (filters.length > 0) {
          const response = await this.$axios.post(
            "api/bank/questions/filter-paginate/",
            { filters },
            { params: queryParams }
          );
          this.items = response.data || response?.data?.data || { results: [], pagination: {} };
        } else {
          const response = await this.$axios.get("api/bank/questions/", { params: queryParams });
          this.items = response.data || response?.data?.data || { results: [], pagination: {} };
        }
      } catch (err) {
        console.error("فشل في تحميل بيانات الأسئلة:", err);
      } finally {
        this.loading = false;
      }
    },

    onInstitutionTypeChange() {
      this.filterStage = null;
      this.filterClassTrack = null;
      this.filterCollege = null;
      this.filterDepartment = null;
      this.filterSpecialization = null;
      this.filterSemesterSubject = null;
      this.filterInstituteField = null;
      this.filterInstituteEducationSystem = null;
      this.filterInstituteSpecialization = null;
      this.filterInstituteSubject = null;
      this.filterSubject = null;
      this.filterUnit = null;
      this.applyFilters();
    },

    onInstituteFieldChange() {
      this.filterInstituteEducationSystem = null;
      this.filterInstituteSpecialization = null;
      this.filterInstituteSubject = null;
      this.filterUnit = null;
    },

    onInstituteEducationSystemChange() {
      this.filterInstituteSpecialization = null;
      this.filterInstituteSubject = null;
      this.filterUnit = null;
    },

    onInstituteSpecializationChange() {
      this.filterInstituteSubject = null;
      this.filterUnit = null;
    },

    onInstituteSubjectChange() {
      this.filterUnit = null;
    },

    onStageChange() {
      this.filterClassTrack = null;
      this.filterSubject = null;
      this.filterUnit = null;
    },

    onClassTrackChange() {
      this.filterSubject = null;
      this.filterUnit = null;
    },

    onCollegeChange() {
      this.filterDepartment = null;
      this.filterSpecialization = null;
      this.filterSemesterSubject = null;
      this.filterSubject = null;
      this.filterUnit = null;
    },

    onDepartmentChange() {
      this.filterSpecialization = null;
      this.filterSemesterSubject = null;
      this.filterSubject = null;
      this.filterUnit = null;
    },

    onSpecializationChange() {
      this.filterSemesterSubject = null;
      this.filterSubject = null;
      this.filterUnit = null;
    },

    onSemesterSubjectChange() {
      this.filterSubject = null;
      this.filterUnit = null;
    },

    onSubjectChange() {
      this.filterUnit = null;
    },

    // === FILTERING ===
    applyFilters() {
      this.currentPage = 1;
      this.getData();
    },

    resetFilters() {
      this.search = "";
      this.filterInstitutionType = "all";
      this.filterSubject = null;
      this.filterUnit = null;
      this.filterStage = null;
      this.filterClassTrack = null;
      this.filterCollege = null;
      this.filterDepartment = null;
      this.filterSpecialization = null;
      this.filterSemesterSubject = null;
      this.filterInstituteField = null;
      this.filterInstituteEducationSystem = null;
      this.filterInstituteSpecialization = null;
      this.filterInstituteSubject = null;
      this.filterSemesterSubject = null;
      this.filterDifficulty = null;
      this.filterStatus = null;
      this.filterType = null;
      this.filterBloom = null;
      this.currentPage = 1;
      this.getData();
    },

    // === NAVIGATION ===
    editQuestion(question) {
      this.$navigateTo({
        name: "question-bank-new",
        blank: false,
        query: { id: question.id },
      });
    },


    // === QUESTION ACTIONS ===
    async viewQuestion(question) {
      this.selectedQuestion = { ...question, _loading: true };
      this.viewDialog = true;
      try {
        const res = await this.$axios.get(`api/bank/questions/${question.id}/`);
        const details = res?.data?.data || res?.data || res;
        this.selectedQuestion = { ...this.selectedQuestion, ...details, _loading: false };
      } catch (err) {
        console.error("فشل في جلب تفاصيل السؤال:", err);
        if (this.selectedQuestion) {
          this.selectedQuestion._loading = false;
        }
      }
    },

    openDeleteDialog(question) {
      this.questionToDelete = question;
      this.deleteDialog = true;
    },

    async executeDelete() {
      if (!this.questionToDelete) return;
      this.deleteLoading = true;
      try {
        await bankService.deleteQuestion(this.questionToDelete.id);
        this.$alert("success", { message: "تم نقل السؤال إلى المهملات بنجاح" });
        await this.fetchData();
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء محاولة حذف السؤال" });
        console.error(err);
      } finally {
        this.deleteDialog = false;
        this.questionToDelete = null;
        this.deleteLoading = false;
      }
    },

    async duplicateQuestion(question) {
      try {
        const res = await bankService.duplicateQuestion(question.id);
        this.$alert("success", { message: "تم استنساخ السؤال بنجاح كمسودة جديدة" });
        await this.fetchData();
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء محاولة استنساخ السؤال" });
        console.error(err);
      }
    },

    async archiveQuestion(question) {
      try {
        await bankService.archiveQuestion(question.id);
        this.$alert("success", { message: "تمت أرشفة السؤال بنجاح" });
        await this.fetchData();
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء أرشفة السؤال" });
        console.error(err);
      }
    },

    async restoreQuestion(question) {
      try {
        await bankService.restoreQuestion(question.id);
        this.$alert("success", { message: "تمت استعادة السؤال إلى مسودة بنجاح" });
        await this.fetchData();
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء استعادة السؤال" });
        console.error(err);
      }
    },

    async createQuestionVersion(question) {
      const reason = prompt("يرجى كتابة سبب إنشاء إصدار جديد:");
      if (reason === null) return;
      try {
        const res = await bankService.createQuestionVersion(question.id, { reason });
        this.$alert("success", { message: "تم إنشاء الإصدار الجديد بنجاح" });
        await this.fetchData();
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء إنشاء الإصدار الجديد" });
        console.error(err);
      }
    },

    async updateQuestionStatus(question, newStatus) {
      try {
        await bankService.updateQuestion(question.id, {
          status: newStatus,
        });
        question.status = newStatus;
        this.$alert("success", { message: "تم تحديث حالة السؤال بنجاح" });
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء محاولة تحديث حالة السؤال" });
        console.error(err);
      }
    },


    // === FILTERS ===
    resetFilters() {
      this.search = "";
      this.filterSubject = null;
      this.filterDifficulty = null;
      this.filterStatus = null;
      this.filterType = null;
      this.currentPage = 1;
    },

    // === HELPERS ===
    stripHtml(html) {
      if (!html) return "";
      const tmp = document.createElement("div");
      tmp.innerHTML = html;
      return tmp.textContent || tmp.innerText || "";
    },

    getSubjectName(question) {
      if (question.subject_name) return question.subject_name;
      const subId = question.subject_id || question.fk_subject;
      if (!subId) return "عام";
      const subject = this.subjects.find((s) => s.id === subId);
      return subject ? subject.name : "عام";
    },

    getStatusColor(status) {
      switch (status) {
        case 'معتمد': return 'success';
        case 'مرفوض': return 'error';
        case 'قيد المراجعة': return 'warning';
        case 'مسودة': return 'grey';
        default: return 'grey';
      }
    },

    getStatusIcon(status) {
      const icons = {
        معتمد: "mdi-check-decagram",
        مرفوض: "mdi-close-octagon",
        "قيد المراجعة": "mdi-clock-outline",
        مسودة: "mdi-pencil-outline",
      };
      return icons[status] || "mdi-file-document-outline";
    },

    getDifficultyColor(difficulty) {
      const d = String(difficulty ?? '').toLowerCase().trim();
      if (d === '1' || d === 'easy' || d === 'سهل') return 'success';
      if (d === '2' || d === 'medium' || d === 'متوسط') return 'warning';
      if (d === '3' || d === 'hard' || d === 'صعب') return 'error';
      return 'blue-grey';
    },

    getDifficultyText(difficulty) {
      const d = String(difficulty ?? '').toLowerCase().trim();
      if (d === '1' || d === 'easy' || d === 'سهل') return 'سهل';
      if (d === '2' || d === 'medium' || d === 'متوسط') return 'متوسط';
      if (d === '3' || d === 'hard' || d === 'صعب') return 'صعب';
      return difficulty || '-';
    },

    getDifficultyIcon(difficulty) {
      const d = String(difficulty ?? '').toLowerCase().trim();
      if (d === '1' || d === 'easy' || d === 'سهل') return 'mdi-signal-cellular-1';
      if (d === '2' || d === 'medium' || d === 'متوسط') return 'mdi-signal-cellular-2';
      if (d === '3' || d === 'hard' || d === 'صعب') return 'mdi-signal-cellular-3';
      return 'mdi-help-circle-outline';
    },

    getTypeText(type) {
      const types = {
        'Single Choice': "اختيار واحد",
        'Multiple Choice': "عدة إجابات",
        'True/False': "صواب / خطأ",
        'Essay': "مقالي",
        'Fill in the Blanks': "فراغات",
        'Matching': "مطابقة",
        'Ordering': "ترتيب",
      };
      return types[type] || type || "-";
    },
  },
};
</script>

<style scoped>
.qb-page-v4 {
  color: rgb(var(--v-theme-on-surface));
}

/* ===== Primary Action Button ===== */
.btn-glow-primary {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, color-mix(in srgb, rgb(var(--v-theme-primary)) 85%, #000) 100%) !important;
  box-shadow: 0 8px 24px -4px rgba(var(--v-theme-primary), 0.45) !important;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
  letter-spacing: 0.02em;
}

.btn-glow-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 32px -4px rgba(var(--v-theme-primary), 0.55) !important;
}

.btn-glow-primary:active {
  transform: translateY(-1px);
}
</style>
