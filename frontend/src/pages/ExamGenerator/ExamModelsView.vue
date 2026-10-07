<template>
  <div class="exam-models-page">

    <!-- Page Header (Always mounted) -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-4 mb-6">
        <div>
          <div class="d-flex align-center gap-2 mb-1">
            <v-btn
              icon="mdi-arrow-right"
              variant="text"
              size="small"
              class="me-1"
              title="العودة لأرشيف الاختبارات"
              @click="goToArchive"
            />
            <h2 class="text-h5 font-weight-black mb-0 d-flex align-center gap-2">
              <v-icon color="primary" size="28">mdi-file-document-multiple-outline</v-icon>
              إدارة نماذج ورقة الاختبار
            </h2>
          </div>
          <p class="text-caption text-medium-emphasis mb-0 ms-10">
            استعراض، فحص، وإعادة ترتيب أسئلة نماذج ورقة الاختبار المعتمدة وطباعتها
          </p>
        </div>

        <div class="d-flex align-center gap-2 flex-wrap" v-if="hasSelectedExam">
          <v-btn
            variant="tonal"
            color="secondary"
            size="small"
            class="font-weight-bold"
            prepend-icon="mdi-key-variant"
            @click="goToPrintKey()"
          >
            مفاتيح الإجابة
          </v-btn>
          <v-btn
            variant="tonal"
            color="info"
            size="small"
            class="font-weight-bold"
            prepend-icon="mdi-checkbox-marked-circle-outline"
            @click="goToPrintSheets()"
          >
            أوراق OMR
          </v-btn>
          <v-btn
            variant="tonal"
            color="primary"
            size="small"
            class="font-weight-bold px-4"
            prepend-icon="mdi-printer"
            @click="goToPrintQuestions()"
          >
            طباعة جميع النماذج
          </v-btn>
        </div>
      </div>

      <!-- Exam Selector & Filters Card -->
      <filter-fields label="اختيار وتصفية الاختبار لعرض وإدارة نماذجه" class="main-card border-0 pa-5 rounded-2xl mb-6">
        <v-row dense class="align-center">
          <!-- Institution Type Selector (مدارس / جامعات / معاهد / الكل) -->
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="filterInstitutionType"
              :items="institutionTypeOptions"
              item-title="text"
              item-value="value"
              placeholder="نوع المؤسسة"
              prepend-inner-icon="mdi-domain"
              hide-details="auto"
              density="compact"
              variant="outlined"
              rounded="lg"
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
              @update:model-value="() => { filterInstituteEducationSystem = null; filterInstituteSpecialization = null; filterInstituteCurriculum = null; filterInstituteSubject = null; selectedExamId = null; }"
            />
            <auto-list
              v-model="filterInstituteEducationSystem"
              name="InstituteEducationSystem"
              :param="filterInstituteField"
              placeholder="نظام التعليم"
              cols="3"
              :add="false"
              :disabled="!filterInstituteField"
              @update:model-value="() => { filterInstituteSpecialization = null; filterInstituteCurriculum = null; filterInstituteSubject = null; selectedExamId = null; }"
            />
            <auto-list
              v-model="filterInstituteSpecialization"
              name="InstituteSpecialization"
              :param="{ field: filterInstituteField, education_system: filterInstituteEducationSystem }"
              placeholder="التخصص المهني"
              cols="3"
              :add="false"
              :disabled="!filterInstituteEducationSystem"
              @update:model-value="() => { filterInstituteCurriculum = null; filterInstituteSubject = null; selectedExamId = null; }"
            />
            <auto-list
              v-model="filterInstituteCurriculum"
              name="InstituteCurriculum"
              :param="filterInstituteSpecialization"
              placeholder="الخطة الدراسية"
              cols="3"
              :add="false"
              :disabled="!filterInstituteSpecialization"
              @update:model-value="() => { filterInstituteSubject = null; selectedExamId = null; }"
            />
            <auto-list
              v-model="filterInstituteSubject"
              name="InstituteSubject"
              :param="filterInstituteCurriculum"
              placeholder="المادة التدريبية"
              cols="3"
              :add="false"
              :disabled="!filterInstituteCurriculum"
              @update:model-value="selectedExamId = null"
            />
          </template>

          <!-- School Subject Filter -->
          <auto-list
            v-if="filterInstitutionType !== 'university' && filterInstitutionType !== 'institute'"
            v-model="filterSubject"
            name="Subject"
            placeholder="المادة الدراسية"
            cols="3"
            :add="false"
            @update:model-value="selectedExamId = null"
          />

          <!-- Exam Selector -->
          <auto-list
            v-model="selectedExamId"
            name="Exam"
            :param="examFilterParam"
            placeholder="اختر الاختبار لعرض وإدارة نماذجه"
            cols="3"
            :add="false"
            @update:model-value="onExamSelected"
          />

          <!-- Reset Filter Button -->
          <v-col cols="auto" v-if="hasAnyFilterActive">
            <v-btn
              size="small"
              variant="text"
              color="error"
              class="font-weight-bold"
              prepend-icon="mdi-refresh"
              @click="resetFilters"
            >
              تصفير التصفية
            </v-btn>
          </v-col>
        </v-row>
      </filter-fields>

      <!-- Linear Progress Indicator during fetch (Clean & Non-disruptive) -->
      <v-progress-linear
        v-if="loading"
        indeterminate
        color="primary"
        height="3"
        rounded
        class="mb-4"
      />

      <!-- Error Alert (If any, closable banner without destroying page) -->
      <v-alert
        v-if="error"
        type="error"
        variant="tonal"
        class="mb-6 rounded-2xl"
        closable
        @click:close="error = null"
      >
        {{ error }}
      </v-alert>

      <!-- Content Workspace -->
      <!-- State 0: Loading exam data for the first time or when switching -->
      <div v-if="loading && !exam" class="main-card pa-12 rounded-2xl text-center border-subtle">
        <v-progress-circular indeterminate color="primary" size="44" class="mb-3" />
        <div class="text-subtitle-2 font-weight-bold">جاري تحميل بيانات ونماذج الاختبار...</div>
        <div class="text-caption text-medium-emphasis">يرجى الانتظار لحظات لجلب النماذج والأسئلة</div>
      </div>

      <!-- State 1: No Exam Selected Yet -->
      <div v-else-if="!hasSelectedExam" class="main-card pa-12 rounded-2xl text-center border-subtle">
        <v-avatar size="68" color="primary" variant="tonal" class="mb-4 rounded-2xl">
          <v-icon size="36">mdi-card-search-outline</v-icon>
        </v-avatar>
        <h3 class="text-h6 font-weight-black mb-1">حدد الاختبار لعرض وإدارة نماذجه</h3>
        <p class="text-caption text-medium-emphasis mb-5 mx-auto" style="max-width: 520px;">
          يرجى اختيار الاختبار المطلوب من القائمة أعلاه لبدء استعراض نماذجه المعتمدة، ترتيب الأسئلة، فحص الإجابات، والطباعة.
        </p>
        <div class="d-flex justify-center gap-2 flex-wrap">
          <v-chip size="small" variant="tonal" color="primary" class="font-weight-bold">
            <v-icon start size="14">mdi-filter-variant</v-icon>
            تصفية دقيقة حسب المرحلة والتخصص
          </v-chip>
          <v-chip size="small" variant="tonal" color="secondary" class="font-weight-bold">
            <v-icon start size="14">mdi-shuffle</v-icon>
            خلط وإعادة ترتيب أسئلة النماذج
          </v-chip>
          <v-chip size="small" variant="tonal" color="info" class="font-weight-bold">
            <v-icon start size="14">mdi-printer</v-icon>
            طباعة النماذج والمفاتيح المعتمدة
          </v-chip>
        </div>
      </div>

      <!-- State 2: Exam Selected but Has No Versions -->
      <div v-else-if="!exam.versions || exam.versions.length === 0" class="main-card pa-10 rounded-2xl text-center border-subtle">
        <v-avatar size="64" color="warning" variant="tonal" class="mb-4 rounded-2xl">
          <v-icon size="32">mdi-alert-circle-outline</v-icon>
        </v-avatar>
        <h3 class="text-h6 font-weight-black mb-1">لا توجد نماذج مولدة لهذا الاختبار بعد</h3>
        <p class="text-caption text-medium-emphasis mb-5">
          تم تسجيل بيانات الاختبار الأساسية ولكن لم يتم توليد أي نماذج أسئلة له بعد.
        </p>
        <v-btn
          color="primary"
          variant="tonal"
          size="small"
          prepend-icon="mdi-plus-circle"
          class="font-weight-bold px-4"
          @click="$router.push('/ExamGenerator/ExamCreateView')"
        >
          الانتقال لتوليد نماذج جديدة
        </v-btn>
      </div>

      <!-- State 3: Active Exam Models Workspace -->
      <div v-else>
        <!-- Exam Summary Banner -->
        <div class="main-card pa-5 rounded-2xl border-subtle mb-6">
          <div class="d-flex align-center justify-space-between flex-wrap gap-3">
            <div class="d-flex align-center gap-3">
              <v-avatar size="44" :color="exam.institution_type === 'university' ? 'secondary' : 'primary'" variant="tonal" class="rounded-xl">
                <v-icon size="24">{{ exam.institution_type === 'university' ? 'mdi-domain' : exam.institution_type === 'institute' ? 'mdi-tools' : 'mdi-school' }}</v-icon>
              </v-avatar>
              <div>
                <div class="d-flex align-center gap-2 mb-1 flex-wrap">
                  <h3 class="text-subtitle-1 font-weight-black mb-0">{{ exam.title }}</h3>
                  <v-chip
                    size="x-small"
                    :color="exam.institution_type === 'university' ? 'secondary' : 'primary'"
                    variant="tonal"
                    class="font-weight-bold text-white"
                  >
                    {{ exam.institution_type === 'university' ? 'تعليم جامعي' : exam.institution_type === 'institute' ? 'تعليم مهني' : 'تعليم مدرسي' }}
                  </v-chip>
                </div>
                <div class="d-flex align-center gap-2 text-caption text-medium-emphasis flex-wrap">
                  <span class="d-flex align-center gap-1 font-weight-bold" v-if="exam.subjectName">
                    <v-icon size="14">mdi-book-open-page-variant</v-icon>
                    {{ exam.subjectName }}
                  </span>
                  <span v-if="exam.uniqueCode">•</span>
                  <span class="d-flex align-center gap-1" v-if="exam.uniqueCode">
                    <v-icon size="14">mdi-identifier</v-icon>
                    رمز الاختبار: {{ exam.uniqueCode }}
                  </span>
                </div>
              </div>
            </div>

            <div class="d-flex align-center gap-2 flex-wrap">
              <v-chip size="small" variant="tonal" color="primary" class="font-weight-bold">
                {{ exam.versions.length }} نماذج معتمدة
              </v-chip>
              <v-chip size="small" variant="tonal" color="success" class="font-weight-bold">
                {{ totalQuestionsInFirstVersion }} سؤالاً / نموذج
              </v-chip>
            </div>
          </div>
        </div>

        <!-- 4 Enterprise KPI Cards (Clean, Official, No AI Glow) -->
        <v-row dense class="mb-6">
          <v-col cols="12" sm="6" md="3">
            <div class="kpi-official-card pa-4 rounded-xl border-subtle">
              <div class="d-flex align-center justify-space-between mb-2">
                <span class="text-caption font-weight-bold text-medium-emphasis">عدد النماذج</span>
                <v-avatar size="36" color="primary" variant="tonal" class="rounded-lg">
                  <v-icon size="20">mdi-file-multiple-outline</v-icon>
                </v-avatar>
              </div>
              <div class="text-h5 font-weight-black mb-1">{{ exam.versions.length }}</div>
              <div class="text-caption text-medium-emphasis">نسخ امتحانية معتمدة</div>
            </div>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <div class="kpi-official-card pa-4 rounded-xl border-subtle">
              <div class="d-flex align-center justify-space-between mb-2">
                <span class="text-caption font-weight-bold text-medium-emphasis">أسئلة النموذج</span>
                <v-avatar size="36" color="info" variant="tonal" class="rounded-lg">
                  <v-icon size="20">mdi-format-list-numbered</v-icon>
                </v-avatar>
              </div>
              <div class="text-h5 font-weight-black mb-1">{{ totalQuestionsInFirstVersion }}</div>
              <div class="text-caption text-medium-emphasis">سؤالاً في كل نموذج</div>
            </div>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <div class="kpi-official-card pa-4 rounded-xl border-subtle">
              <div class="d-flex align-center justify-space-between mb-2">
                <span class="text-caption font-weight-bold text-medium-emphasis">إجمالي الدرجات</span>
                <v-avatar size="36" color="success" variant="tonal" class="rounded-lg">
                  <v-icon size="20">mdi-calculator-variant-outline</v-icon>
                </v-avatar>
              </div>
              <div class="text-h5 font-weight-black mb-1">{{ activeVersionScore }}</div>
              <div class="text-caption text-medium-emphasis">للنموذج الحالي المحدد</div>
            </div>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <div class="kpi-official-card pa-4 rounded-xl border-subtle">
              <div class="d-flex align-center justify-space-between mb-2">
                <span class="text-caption font-weight-bold text-medium-emphasis">ملف الصعوبة</span>
                <v-avatar size="36" color="warning" variant="tonal" class="rounded-lg">
                  <v-icon size="20">mdi-speedometer</v-icon>
                </v-avatar>
              </div>
              <div class="text-h5 font-weight-black mb-1 text-truncate">{{ activeVersionDifficultyText }}</div>
              <div class="text-caption text-medium-emphasis">مستوى تمايز النموذج</div>
            </div>
          </v-col>
        </v-row>

        <!-- Models Container -->
        <div class="main-card pa-6 rounded-2xl mb-8">
          <!-- Segmented Tab Bar -->
          <div class="segmented-tab-bar mb-6 pa-1 rounded-xl">
            <button
              v-for="(version, idx) in exam.versions"
              :key="version.id"
              class="segmented-tab-btn font-weight-bold"
              :class="{ 'is-active': activeTab === idx }"
              @click="activeTab = idx"
            >
              <v-icon start size="18">mdi-file-document-outline</v-icon>
              <span>نموذج {{ version.versionCode }}</span>
              <v-chip
                size="x-small"
                :color="activeTab === idx ? 'primary' : undefined"
                :variant="activeTab === idx ? 'flat' : 'tonal'"
                class="ms-1 font-weight-bold"
              >
                {{ version.questions ? version.questions.length : 0 }}
              </v-chip>
            </button>
          </div>

          <v-window v-model="activeTab">
            <v-window-item v-for="(version, vIdx) in exam.versions" :key="version.id" :value="vIdx">
              <!-- Version Header Toolbar -->
              <div class="d-flex flex-wrap align-center justify-space-between mb-5 pa-4 rounded-xl border-subtle gap-3">
                <div class="d-flex align-center gap-2 flex-wrap">
                  <v-chip color="primary" variant="tonal" class="font-weight-black">
                    نموذج {{ version.versionCode }}
                  </v-chip>
                  <v-chip color="success" variant="tonal" class="font-weight-bold" size="small">
                    <v-icon start size="14">mdi-check-circle-outline</v-icon>
                    {{ version.questions.length }} أسئلة
                  </v-chip>
                  <v-chip color="info" variant="tonal" class="font-weight-bold" size="small">
                    <v-icon start size="14">mdi-star-circle-outline</v-icon>
                    {{ calculateTotalScore(version) }} درجة
                  </v-chip>
                  <v-chip
                    v-if="version.difficulty_profile"
                    :color="difficultyColor(version.difficulty_profile)"
                    variant="tonal"
                    class="font-weight-bold"
                    size="small"
                  >
                    <v-icon start size="14">mdi-speedometer</v-icon>
                    {{ version.difficulty_profile_display || difficultyLabel(version.difficulty_profile) }}
                  </v-chip>
                  <v-chip v-if="version.difficulty_distribution" size="x-small" variant="outlined" class="font-weight-bold">
                    سهل {{ version.difficulty_distribution.easy }}% • متوسط {{ version.difficulty_distribution.medium }}% • صعب {{ version.difficulty_distribution.hard }}%
                  </v-chip>
                </div>

                <!-- Action Controls -->
                <div class="d-flex flex-wrap align-center gap-2">
                  <!-- Answer Key Toggle -->
                  <v-btn
                    size="small"
                    :variant="showAnswers ? 'flat' : 'tonal'"
                    :color="showAnswers ? 'success' : undefined"
                    class="font-weight-bold"
                    prepend-icon="mdi-eye-check-outline"
                    @click="showAnswers = !showAnswers"
                  >
                    {{ showAnswers ? 'إخفاء الإجابات' : 'معاينة الإجابات' }}
                  </v-btn>

                  <!-- Shuffle Questions -->
                  <v-btn
                    size="small"
                    variant="tonal"
                    color="primary"
                    class="font-weight-bold"
                    prepend-icon="mdi-shuffle-variant"
                    :loading="shufflingIdx === vIdx"
                    @click="shuffleAndSave(vIdx)"
                  >
                    خلط الأسئلة
                  </v-btn>

                  <!-- Print Specific Model -->
                  <v-btn
                    size="small"
                    variant="tonal"
                    color="secondary"
                    class="font-weight-bold"
                    prepend-icon="mdi-printer"
                    @click="goToPrintQuestions(version.id)"
                  >
                    طباعة هذا النموذج
                  </v-btn>

                  <!-- Delete Version -->
                  <v-btn
                    size="small"
                    variant="text"
                    color="error"
                    class="font-weight-bold"
                    icon="mdi-trash-can-outline"
                    title="حذف هذا النموذج"
                    @click="openDeleteVersionDialog(vIdx)"
                  />
                </div>
              </div>

              <!-- Questions List with Options & Visual Answers -->
              <div class="d-flex flex-column gap-3" v-if="version.questions && version.questions.length">
                <div
                  v-for="(question, qIdx) in version.questions"
                  :key="question.orderId"
                  class="pa-4 rounded-xl border-subtle model-question-card"
                >
                  <!-- Question Top Header -->
                  <div class="d-flex align-start justify-space-between gap-3 mb-3">
                    <div class="d-flex align-center gap-2 flex-wrap">
                      <v-avatar color="primary" size="32" class="text-white font-weight-black flex-shrink-0">
                        {{ qIdx + 1 }}
                      </v-avatar>
                      <v-chip size="x-small" color="secondary" variant="tonal" class="font-weight-bold">
                        {{ getTypeText(question.questionType) }}
                      </v-chip>
                      <v-chip size="x-small" :color="getDifficultyColor(question.difficulty)" variant="tonal" class="font-weight-bold text-white">
                        {{ getDifficultyText(question.difficulty) }}
                      </v-chip>
                      <v-chip v-if="question.bloomLevel" size="x-small" color="info" variant="tonal" class="font-weight-bold">
                        {{ question.bloomLevel }}
                      </v-chip>
                      <span v-if="question.unitName || question.lessonName" class="text-caption text-medium-emphasis">
                        {{ question.unitName }} {{ question.lessonName ? `• ${question.lessonName}` : '' }}
                      </span>
                    </div>

                    <div class="d-flex align-center gap-1 flex-shrink-0">
                      <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                        {{ question.assignedMark }} درجة
                      </v-chip>
                      
                      <!-- Move Controls -->
                      <v-btn
                        icon="mdi-arrow-up"
                        size="x-small"
                        variant="text"
                        :disabled="qIdx === 0"
                        title="تحريك لأعلى"
                        @click="moveQuestion(vIdx, qIdx, -1)"
                      />
                      <v-btn
                        icon="mdi-arrow-down"
                        size="x-small"
                        variant="text"
                        :disabled="qIdx === version.questions.length - 1"
                        title="تحريك لأسفل"
                        @click="moveQuestion(vIdx, qIdx, 1)"
                      />
                      <v-btn
                        icon="mdi-delete-outline"
                        size="x-small"
                        variant="text"
                        color="error"
                        title="حذف من النموذج"
                        @click="openDeleteQuestionDialog(vIdx, qIdx)"
                      />
                    </div>
                  </div>

                  <!-- Question Text -->
                  <div class="text-body-1 font-weight-bold mb-3 px-1 leading-relaxed" v-html="parseScientificMarkup(question.content)" />

                  <!-- Options / Answers Display (for Multiple Choice) -->
                  <div v-if="question.options && question.options.length" class="options-container pt-2">
                    <v-row dense>
                      <v-col
                        v-for="(opt, optIdx) in question.options"
                        :key="opt.id || optIdx"
                        cols="12"
                        sm="6"
                      >
                        <div
                          class="pa-2 rounded-lg border-subtle d-flex align-center gap-2 option-display-item"
                          :class="{ 'is-correct-option': showAnswers && opt.isTrue }"
                        >
                          <v-avatar
                            size="24"
                            :color="showAnswers && opt.isTrue ? 'success' : 'surface-variant'"
                            :variant="showAnswers && opt.isTrue ? 'flat' : 'tonal'"
                            class="font-weight-black text-caption flex-shrink-0"
                            :class="{ 'text-white': showAnswers && opt.isTrue }"
                          >
                            {{ getOptionLetter(optIdx) }}
                          </v-avatar>
                          <span class="text-body-2 flex-grow-1" :class="{ 'font-weight-bold text-success': showAnswers && opt.isTrue }" v-html="parseScientificMarkup(opt.text)">
                          </span>
                          <v-icon v-if="showAnswers && opt.isTrue" size="18" color="success">
                            mdi-check-circle
                          </v-icon>
                        </div>
                      </v-col>
                    </v-row>
                  </div>

                  <!-- True / False Display -->
                  <div v-else-if="question.questionType === 'True/False' || question.questionType === 'صح وخطأ'" class="pt-2">
                    <div class="d-flex align-center gap-2">
                      <div
                        class="pa-2 px-4 rounded-lg border-subtle font-weight-bold text-body-2 option-display-item"
                        :class="{ 'is-correct-option text-success': showAnswers && question.isTrue }"
                      >
                        <v-icon start size="16" :color="showAnswers && question.isTrue ? 'success' : undefined">mdi-check</v-icon>
                        صواب (True)
                      </div>
                      <div
                        class="pa-2 px-4 rounded-lg border-subtle font-weight-bold text-body-2 option-display-item"
                        :class="{ 'is-correct-option text-success': showAnswers && !question.isTrue }"
                      >
                        <v-icon start size="16" :color="showAnswers && !question.isTrue ? 'success' : undefined">mdi-close</v-icon>
                        خطأ (False)
                      </div>
                    </div>
                  </div>

                  <!-- Essay / Model Answer Display -->
                  <div v-else-if="showAnswers && question.answerText" class="mt-2 pa-3 rounded-lg border-subtle bg-surface-variant">
                    <span class="text-caption font-weight-bold text-success d-block mb-1">
                      <v-icon start size="14">mdi-text-box-check-outline</v-icon>
                      الإجابة النموذجية المعتمدة:
                    </span>
                    <div class="text-caption text-medium-emphasis" v-html="question.answerText" />
                  </div>
                </div>
              </div>

              <!-- Empty State -->
              <div v-else class="text-center text-medium-emphasis pa-8">
                <v-icon size="48" class="mb-2 text-medium-emphasis">mdi-file-document-outline</v-icon>
                <div>لا توجد أسئلة مضافة في هذا النموذج بعد</div>
              </div>

            </v-window-item>
          </v-window>
        </div>
      </div>

    <!-- Delete Version Dialog -->
    <CustomDialog
      v-model="deleteVersionDialog"
      width="450"
      title="تأكيد حذف النموذج"
      subTitle="هل أنت متأكد من حذف هذا النموذج نهائياً؟"
    >
      <p class="text-body-2 text-medium-emphasis mb-4">
        سيتم حذف النموذج وجميع ترتيبات أسئلته من قاعدة البيانات. لا يمكن التراجع عن هذا الإجراء.
      </p>
      <template #actions>
        <custom-btn label="إلغاء" variant="text" class="font-weight-bold" :click="() => deleteVersionDialog = false" />
        <custom-btn type="del" label="تأكيد الحذف" color="error" :loading="deleteLoading" class="font-weight-bold" :click="performDeleteVersion" />
      </template>
    </CustomDialog>

    <!-- Delete Question Dialog -->
    <CustomDialog
      v-model="deleteQuestionDialog"
      width="450"
      title="تأكيد حذف السؤال"
      subTitle="هل تريد إزالة هذا السؤال من النموذج؟"
    >
      <p class="text-body-2 text-medium-emphasis mb-4">
        سيتم إزالة هذا السؤال من ترتيب النموذج في قاعدة البيانات دون حذفه من بنك الأسئلة الرئيسي.
      </p>
      <template #actions>
        <custom-btn label="إلغاء" variant="text" class="font-weight-bold" :click="() => deleteQuestionDialog = false" />
        <custom-btn type="del" label="تأكيد الحذف" color="error" :loading="deleteLoading" class="font-weight-bold" :click="performDeleteQuestion" />
      </template>
    </CustomDialog>

  </div>
</template>

<script>
import { examsService } from '@/services/examsService'
import { parseScientificMarkup, ensureKaTeXLoaded } from '@/utils/scientificRenderer'

export default {
  name: 'ExamModelsView',

  data() {
    return {
      loading: false,
      error: null,
      exam: null,
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
      filterStage: null,
      filterClassTrack: null,
      filterSubject: null,
      selectedExamId: null,
      activeTab: 0,
      showAnswers: false,
      shufflingIdx: null,

      deleteVersionDialog: false,
      deleteQuestionDialog: false,
      deleteLoading: false,
      targetVersionIdx: null,
      targetQuestionIdx: null,
    }
  },

  computed: {
    hasSelectedExam() {
      return !!this.selectedExamId && !!this.exam && !!this.exam.id
    },

    hasAnyFilterActive() {
      return (
        this.filterInstitutionType !== 'all' ||
        !!this.filterCollege ||
        !!this.filterDepartment ||
        !!this.filterSpecialization ||
        !!this.filterSemesterSubject ||
        !!this.filterInstituteField ||
        !!this.filterInstituteEducationSystem ||
        !!this.filterInstituteSpecialization ||
        !!this.filterInstituteCurriculum ||
        !!this.filterInstituteSubject ||
        !!this.filterStage ||
        !!this.filterClassTrack ||
        !!this.filterSubject ||
        !!this.selectedExamId
      )
    },

    totalQuestionsInFirstVersion() {
      if (!this.exam || !this.exam.versions || !this.exam.versions.length) return 0
      return this.exam.versions[0].questions ? this.exam.versions[0].questions.length : 0
    },

    activeVersionScore() {
      if (!this.exam || !this.exam.versions || !this.exam.versions.length) return 0
      const v = this.exam.versions[this.activeTab]
      return v ? this.calculateTotalScore(v) : 0
    },

    activeVersionDifficultyText() {
      if (!this.exam || !this.exam.versions || !this.exam.versions.length) return '—'
      const v = this.exam.versions[this.activeTab]
      if (!v) return '—'
      if (v.difficulty_profile_display) return v.difficulty_profile_display
      return this.difficultyLabel(v.difficulty_profile) || 'متوازن'
    },

    examFilterParam() {
      const p = {}
      if (this.filterInstitutionType && this.filterInstitutionType !== 'all') {
        p.institution_type = this.filterInstitutionType
      }
      if (this.filterInstitutionType === 'school') {
        if (this.filterClassTrack) p.class_track = this.filterClassTrack
        if (this.filterStage) p.stage = this.filterStage
        if (this.filterSubject) p.subject = this.filterSubject
      } else if (this.filterInstitutionType === 'university') {
        if (this.filterSemesterSubject) p.semester_subject = this.filterSemesterSubject
        if (this.filterSpecialization) p.specialization = this.filterSpecialization
        if (this.filterDepartment) p.department = this.filterDepartment
        if (this.filterCollege) p.college = this.filterCollege
      } else if (this.filterInstitutionType === 'institute') {
        if (this.filterInstituteSubject) p.subject = this.filterInstituteSubject
        else if (this.filterInstituteField) p.field = this.filterInstituteField
      } else {
        if (this.filterSubject) p.subject = this.filterSubject
      }
      return Object.keys(p).length > 0 ? p : null
    },
  },

  async created() {
    await this.loadData()
  },

  mounted() {
    ensureKaTeXLoaded()
  },

  methods: {
    parseScientificMarkup(content) {
      return parseScientificMarkup(content)
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
      this.selectedExamId = null
      this.exam = null
    },

    onCollegeChange() {
      this.filterDepartment = null
      this.filterSpecialization = null
      this.filterSemesterSubject = null
      this.selectedExamId = null
      this.exam = null
    },

    onStageChange() {
      this.filterClassTrack = null
      this.selectedExamId = null
      this.exam = null
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
      this.filterClassTrack = null
      this.filterSubject = null
      this.selectedExamId = null
      this.exam = null
      this.error = null
      if (this.$route.query.examId || this.$route.query.id) {
        const q = { ...this.$route.query }
        delete q.examId
        delete q.id
        this.$router.replace({ query: q }).catch(() => {})
      }
    },

    // ── LOAD ─────────────────────────────────────────
    async loadData(overrideExamId = null) {
      let examId = overrideExamId

      if (!examId) {
        const routeId = this.$route.params.id || this.$route.query.id || this.$route.query.examId
        if (routeId) examId = Number(routeId)
      }

      if (!examId || isNaN(examId)) {
        this.exam = null
        this.selectedExamId = null
        this.loading = false
        return
      }

      // If already loaded and matching, skip duplicate fetch
      if (this.exam && this.exam.id === examId && !this.loading) {
        return
      }

      this.loading = true
      this.error = null
      this.selectedExamId = examId

      // Update URL query silently so refresh preserves selection without re-rendering layout
      if (this.$route.query.examId != examId && this.$route.query.id != examId) {
        this.$router.replace({ query: { ...this.$route.query, examId } }).catch(() => {})
      }

      try {
        // Fetch full exam models structure directly from dedicated MVS
        const examDetails = await examsService.getExamModelsDetails(examId)
        this.exam = examDetails
        this.activeTab = 0
      } catch (err) {
        console.error('فشل تحميل بيانات النماذج:', err)
        this.error = 'فشل تحميل بيانات الاختبار. تأكد من صحة الرابط وأن الاختبار موجود.'
      } finally {
        this.loading = false
      }
    },

    // ── SHUFFLE & SAVE ───────────────────────────────
    async shuffleAndSave(vIdx) {
      this.shufflingIdx = vIdx
      try {
        const version = this.exam.versions[vIdx]
        await examsService.shuffleModelQuestions({ versionId: version.id })
        
        // Refresh details
        const updated = await examsService.getExamModelsDetails(this.exam.id)
        this.exam = updated
        if (this.$alert) {
          this.$alert('success', { message: 'تم خلط وترتيب أسئلة النموذج بنجاح' })
        }
      } catch (err) {
        if (this.$alert) {
          this.$alert('errorData', { message: 'فشل حفظ الترتيب الجديد' })
        }
        console.error(err)
      } finally {
        this.shufflingIdx = null
      }
    },

    // ── MOVE QUESTION ────────────────────────────────
    async moveQuestion(vIdx, qIdx, direction) {
      const newIdx = qIdx + direction
      const questions = [...this.exam.versions[vIdx].questions]
      if (newIdx < 0 || newIdx >= questions.length) return;
      [questions[qIdx], questions[newIdx]] = [questions[newIdx], questions[qIdx]]
      try {
        await examsService.reorderModelQuestions({
          orders: [
            { orderId: questions[qIdx].orderId, orderIndex: qIdx + 1 },
            { orderId: questions[newIdx].orderId, orderIndex: newIdx + 1 }
          ]
        })
        this.exam.versions[vIdx].questions = questions.map((q, i) => ({ ...q, orderIndex: i + 1 }))
      } catch (err) {
        if (this.$alert) {
          this.$alert('errorData', { message: 'فشل تحديث ترتيب السؤال' })
        }
        console.error(err)
      }
    },

    // ── DELETE VERSION ───────────────────────────────
    openDeleteVersionDialog(vIdx) {
      this.targetVersionIdx = vIdx
      this.deleteVersionDialog = true
    },

    async performDeleteVersion() {
      if (this.targetVersionIdx === null) return
      this.deleteLoading = true
      try {
        const version = this.exam.versions[this.targetVersionIdx]
        await examsService.deleteExamVersion(version.id)
        this.exam.versions.splice(this.targetVersionIdx, 1)
        this.activeTab = Math.max(0, this.exam.versions.length - 1)
        if (this.$alert) {
          this.$alert('success', { message: 'تم حذف النموذج بنجاح' })
        }
      } catch (err) {
        if (this.$alert) {
          this.$alert('errorData', { message: 'فشل حذف النموذج' })
        }
        console.error(err)
      } finally {
        this.deleteLoading = false
        this.deleteVersionDialog = false
        this.targetVersionIdx = null
      }
    },

    // ── DELETE QUESTION ──────────────────────────────
    openDeleteQuestionDialog(vIdx, qIdx) {
      this.targetVersionIdx = vIdx
      this.targetQuestionIdx = qIdx
      this.deleteQuestionDialog = true
    },

    async performDeleteQuestion() {
      if (this.targetVersionIdx === null || this.targetQuestionIdx === null) return
      this.deleteLoading = true
      try {
        const q = this.exam.versions[this.targetVersionIdx].questions[this.targetQuestionIdx]
        await examsService.removeModelQuestion({ orderId: q.orderId })
        this.exam.versions[this.targetVersionIdx].questions.splice(this.targetQuestionIdx, 1)
        if (this.$alert) {
          this.$alert('success', { message: 'تم حذف السؤال من النموذج بنجاح' })
        }
      } catch (err) {
        if (this.$alert) {
          this.$alert('errorData', { message: 'فشل حذف السؤال من النموذج' })
        }
        console.error(err)
      } finally {
        this.deleteLoading = false
        this.deleteQuestionDialog = false
        this.targetVersionIdx = null
        this.targetQuestionIdx = null
      }
    },

    // ── PRINT & NAVIGATION ───────────────────────────
    goToPrintQuestions(versionId = null) {
      if (!this.exam || !this.exam.id) return
      const query = { examId: this.exam.id }
      if (versionId) query.versionId = versionId
      try {
        const routeData = this.$router.resolve({ name: 'exams-print-questions', query })
        window.open(routeData.href, '_blank')
      } catch (e) {
        this.$router.push({ path: '/ExamGenerator/ExamPrintQuestionsView', query })
      }
    },

    goToPrintKey(versionId = null) {
      if (!this.exam || !this.exam.id) return
      const query = { examId: this.exam.id }
      if (versionId) query.versionId = versionId
      try {
        const routeData = this.$router.resolve({ name: 'exams-print-key', query })
        window.open(routeData.href, '_blank')
      } catch (e) {
        this.$router.push({ path: '/ExamGenerator/ExamPrintKeyView', query })
      }
    },

    goToPrintSheets() {
      if (!this.exam || !this.exam.id) return
      try {
        const routeData = this.$router.resolve({ name: 'exams-print-sheets', query: { examId: this.exam.id } })
        window.open(routeData.href, '_blank')
      } catch (e) {
        this.$router.push({ path: '/ExamGenerator/ExamPrintSheetsView', query: { examId: this.exam.id } })
      }
    },

    goToArchive() {
      this.$router.push('/ExamGenerator/ExamArchiveView').catch(() => {
        this.$router.push({ name: 'exams-archive' })
      })
    },

    // ── HELPERS ──────────────────────────────────────
    onExamSelected(val) {
      if (val) {
        const id = typeof val === 'object' ? (val.id || val.value) : val
        const numId = Number(id)
        if (numId && (!this.exam || this.exam.id !== numId)) {
          this.loadData(numId)
        }
      } else {
        this.exam = null
        this.selectedExamId = null
        if (this.$route.query.examId || this.$route.query.id) {
          const q = { ...this.$route.query }
          delete q.examId
          delete q.id
          this.$router.replace({ query: q }).catch(() => {})
        }
      }
    },

    calculateTotalScore(version) {
      if (!version || !version.questions) return 0
      return version.questions.reduce((sum, q) => sum + (Number(q.assignedMark) || 0), 0)
    },

    getOptionLetter(idx) {
      const letters = ['أ', 'ب', 'ج', 'د', 'هـ', 'و']
      return letters[idx] || String.fromCharCode(65 + idx)
    },

    getDifficultyColor(d) {
      if (d === 1 || d === 'easy' || d === 'سهل') return 'success'
      if (d === 2 || d === 'medium' || d === 'متوسط') return 'warning'
      if (d === 3 || d === 'hard' || d === 'صعب') return 'error'
      return 'info'
    },

    difficultyColor(profile) {
      const map = { easy: 'success', medium: 'warning', hard: 'error', mixed: 'info' }
      return map[profile] || 'info'
    },

    difficultyLabel(profile) {
      const map = { easy: 'سهل', medium: 'متوسط', hard: 'صعب', mixed: 'متوازن' }
      return map[profile] || profile
    },

    getDifficultyText(d) {
      if (d === 1 || d === 'easy') return 'سهل'
      if (d === 2 || d === 'medium') return 'متوسط'
      if (d === 3 || d === 'hard') return 'صعب'
      return d || '-'
    },

    getTypeText(type) {
      const map = {
        'Single Choice': 'اختيار واحد',
        'Multiple Choice': 'متعدد الخيارات',
        'True/False': 'صح وخطأ',
        'Essay': 'سؤال مقالي'
      }
      return map[type] || type || '-'
    },
  },
}
</script>

<style scoped>
.exam-models-page {
  color: rgb(var(--v-theme-on-surface));
}

.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03);
}

.border-subtle {
  border: 1px solid rgba(var(--v-border-color), 0.12);
}

.kpi-official-card {
  background: rgb(var(--v-theme-surface));
  transition: all 0.2s ease;
}

.kpi-official-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.35);
}

.segmented-tab-bar {
  display: flex;
  gap: 6px;
  background: rgba(var(--v-theme-background), 0.8);
  border: 1px solid rgba(var(--v-border-color), 0.12);
  overflow-x: auto;
}

.segmented-tab-btn {
  padding: 8px 18px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
  color: rgba(var(--v-theme-on-surface), 0.7);
  background: transparent;
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  transition: all 0.18s ease;
}

.segmented-tab-btn:hover {
  background: rgba(var(--v-theme-primary), 0.06);
  color: rgb(var(--v-theme-primary));
}

.segmented-tab-btn.is-active {
  background: rgb(var(--v-theme-surface)) !important;
  color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

.model-question-card {
  background: rgb(var(--v-theme-surface));
  transition: border-color 0.15s ease;
}

.model-question-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.3);
}

.option-display-item {
  background: rgba(var(--v-theme-background), 0.6);
  transition: all 0.15s ease;
}

.option-display-item.is-correct-option {
  background: rgba(var(--v-theme-success), 0.08) !important;
  border-color: rgb(var(--v-theme-success)) !important;
}

.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
</style>
