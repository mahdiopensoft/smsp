<template>
  <div class="qb-fast-page-v4 pb-16">
    <!-- Top Bar: Header & Primary Actions -->
    <div class="d-flex align-center justify-space-between mb-5 flex-wrap gap-3">
      <div class="d-flex align-center gap-3">
        <v-avatar size="42" color="primary" variant="tonal" class="rounded-xl flex-shrink-0">
          <v-icon size="22">mdi-lightning-bolt</v-icon>
        </v-avatar>
        <div>
          <h2 class="text-h6 font-weight-black text-high-emphasis mb-0">الإدخال السريع للأسئلة</h2>
          <span class="text-caption text-medium-emphasis">إدخال وبناء نماذج الأسئلة المتعددة بسرعة فائقة</span>
        </div>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <v-chip color="primary" variant="tonal" class="font-weight-bold px-3" v-if="questions.length">
          <v-icon start size="15">mdi-format-list-checks</v-icon>
          {{ questions.length }} {{ questions.length === 1 ? 'سؤال' : 'أسئلة' }}
        </v-chip>
        <custom-btn
          type="save"
          label="حفظ جميع الأسئلة"
          color="primary"
          class="font-weight-bold px-5"
          :disabled="questions.length === 0 || !isContextComplete"
          :loading="saving"
          :click="saveAllQuestions"
        />
      </div>
    </div>

    <!-- Context Classification & Defaults Card -->
    <div class="main-card mb-6 pa-4 pa-md-5 rounded-2xl sticky-context-bar">
      <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
        <div class="d-flex align-center gap-2">
          <v-avatar size="30" color="primary" variant="tonal" class="rounded-lg">
            <v-icon size="16">mdi-map-marker-path</v-icon>
          </v-avatar>
          <div>
            <h3 class="text-subtitle-2 font-weight-black mb-0">التصنيف الأكاديمي المشترك</h3>
            <span class="text-caption text-medium-emphasis">يطبق هذا التصنيف على كافة الأسئلة المدخلة</span>
          </div>
        </div>

        <custom-btn
          color="primary"
          variant="tonal"
          size="small"
          :icon="showDefaults ? 'mdi-chevron-up' : 'mdi-cog-outline'"
          :label="showDefaults ? 'إخفاء القيم الافتراضية' : 'القيم الافتراضية للأسئلة'"
          class="font-weight-bold text-caption"
          :click="() => showDefaults = !showDefaults"
        />
      </div>

      <!-- Classification Dropdowns Row -->
      <v-row dense class="align-center">
        <!-- Institution Type Select (مدرسي / جامعي) -->
        <v-col cols="12" md="3" lg="3" class="mb-5">
          <v-select
            v-model="context.institution_type"
            :items="institutionTypes"
            item-title="text"
            item-value="value"
            label="نوع النظام التعليمي"
            prepend-inner-icon="mdi-school-outline"
            variant="outlined"
            density="compact"
            color="primary"
            hide-details="auto"
            @update:model-value="onInstitutionTypeToggle"
          >
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :prepend-icon="item.raw.icon" />
            </template>
          </v-select>
        </v-col>

        <!-- 🏫 School Selects (cols="3" internally sets desktop: md=3, mobile: cols=12) -->
        <template v-if="context.institution_type === 'school'">
          <auto-list
            v-model="context.stageId"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="3"
            :add="false"
            @update:model-value="onStageChange"
          />
          <auto-list
            v-model="context.classTrackId"
            name="ClassTrackByStage"
            :param="context.stageId"
            placeholder="الصف والمسار"
            cols="3"
            :add="false"
            :disabled="!context.stageId"
            @update:model-value="onClassTrackChange"
          />
          <auto-list
            v-model="context.subjectId"
            name="Subject"
            :param="context.classTrackId || context.stageId"
            placeholder="اختر المادة"
            cols="3"
            :add="false"
            :disabled="!context.classTrackId && !context.stageId"
            @update:model-value="onSubjectChange"
          />
          <auto-list
            v-model="context.semesterId"
            name="Semester"
            placeholder="الفصل الدراسي"
            cols="3"
            :add="false"
          />
        </template>

        <!-- 🎓 University Selects -->
        <template v-if="context.institution_type === 'university'">
          <auto-list
            v-model="context.collegeId"
            name="College"
            placeholder="الكلية الجامعية"
            cols="3"
            :add="false"
            @update:model-value="onCollegeChange"
          />
          <auto-list
            v-model="context.departmentId"
            name="DepartmentByCollege"
            :param="context.collegeId"
            placeholder="القسم الأكاديمي"
            cols="3"
            :add="false"
            :disabled="!context.collegeId"
            @update:model-value="onDepartmentChange"
          />
          <auto-list
            v-model="context.specializationId"
            name="Specialization"
            :param="context.departmentId"
            placeholder="التخصص والبرنامج"
            cols="3"
            :add="false"
            :disabled="!context.departmentId"
            @update:model-value="onSpecializationChange"
          />
          <auto-list
            v-model="context.semesterSubjectId"
            name="SemesterSubject"
            :param="context.specializationId"
            placeholder="مقرر الفصل الجامعي"
            cols="3"
            :add="false"
            @update:model-value="onSemesterSubjectChange"
          />
        </template>

        <!-- 🏢 Institute Selects -->
        <template v-if="context.institution_type === 'institute'">
          <auto-list
            v-model="context.instituteFieldId"
            name="InstituteField"
            placeholder="المجال المهني / التقني"
            cols="3"
            :add="false"
            @update:model-value="onInstituteFieldChange"
          />
          <auto-list
            v-model="context.instituteEducationSystemId"
            name="InstituteEducationSystem"
            :param="context.instituteFieldId"
            placeholder="نظام التعليم والتدريب"
            cols="3"
            :add="false"
            :disabled="!context.instituteFieldId"
            @update:model-value="onInstituteEducationSystemChange"
          />
          <auto-list
            v-model="context.instituteSpecializationId"
            name="InstituteSpecialization"
            :param="{ field: context.instituteFieldId, education_system: context.instituteEducationSystemId }"
            placeholder="التخصص المهني"
            cols="3"
            :add="false"
            :disabled="!context.instituteEducationSystemId"
            @update:model-value="onInstituteSpecializationChange"
          />
          <auto-list
            v-model="context.instituteCurriculumId"
            name="InstituteCurriculum"
            :param="context.instituteSpecializationId"
            placeholder="الخطة الدراسية"
            cols="3"
            :add="false"
            :disabled="!context.instituteSpecializationId"
          />
          <auto-list
            v-model="context.instituteSubjectId"
            name="InstituteSubject"
            :param="{ field: context.instituteFieldId }"
            placeholder="المادة الدراسية للمعهد"
            cols="3"
            :add="false"
            @update:model-value="onInstituteSubjectChange"
          />
        </template>

        <!-- Common: Unit, Lesson, Learning Outcome -->
        <auto-list
          v-model="context.unitId"
          name="UnitBySubject"
          :param="context.institution_type === 'university' ? { semester_subject: context.semesterSubjectId } : (context.institution_type === 'institute' ? { subject: context.instituteSubjectId } : { subject: context.subjectId })"
          :placeholder="context.institution_type === 'university' ? 'مفردة / موضوع المقرر' : (context.institution_type === 'institute' ? 'الوحدة / التدريب العملي' : 'الوحدة الدراسية')"
          cols="3"
          :add="false"
          :disabled="context.institution_type === 'university' ? !context.semesterSubjectId : (context.institution_type === 'institute' ? !context.instituteSubjectId : !context.subjectId)"
          @update:model-value="onUnitChange"
        />
        <auto-list
          v-model="context.lessonId"
          name="LessonByUnit"
          :param="context.unitId"
          :placeholder="context.institution_type === 'university' ? 'المحاضرة / الدرس الأكاديمي' : (context.institution_type === 'institute' ? 'التدريب / الدرس المهني' : 'الدرس المدرسي')"
          cols="3"
          :add="false"
          :disabled="!context.unitId"
        />
        <auto-list
          v-model="context.learningOutcomeId"
          name="LearningOutcome"
          :param="context.unitId"
          :placeholder="context.institution_type === 'university' ? 'مخرج تعلم المقرر (CLO)' : 'مخرج التعلم (اختياري)'"
          cols="3"
          :add="false"
          :disabled="!context.unitId"
        />
      </v-row>

      <!-- Expandable Defaults Panel -->
      <v-expand-transition>
        <div v-if="showDefaults" class="mt-3 pt-3 border-t border-slate-100">
          <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
            <span class="text-caption font-weight-bold text-primary d-flex align-center gap-1">
              <v-icon size="14">mdi-tune</v-icon>
              القيم الافتراضية المطبقة عند إنشاء سؤال جديد:
            </span>
            <custom-btn
              type="add"
              color="primary"
              variant="tonal"
              icon="mdi-check-all"
              label="تطبيق على كافة الأسئلة"
              class="font-weight-bold text-caption"
              size="small"
              :click="applyDefaultsToAll"
            />
          </div>

          <v-row dense class="align-center">
            <v-col cols="6" sm="3">
              <v-text-field
                v-model.number="defaults.defaultScore"
                type="number"
                min="1"
                label="الدرجة الافتراضية"
                prepend-inner-icon="mdi-star-circle-outline"
                variant="outlined"
                density="compact"
                rounded="lg"
                hide-details="auto"
              />
            </v-col>
            <v-col cols="6" sm="3">
              <v-text-field
                v-model.number="defaults.expectedTimeMinutes"
                type="number"
                min="1"
                label="الزمن (دقائق)"
                prepend-inner-icon="mdi-clock-outline"
                variant="outlined"
                density="compact"
                rounded="lg"
                hide-details="auto"
              />
            </v-col>
            <v-col cols="6" sm="3">
              <v-select
                v-model="defaults.difficulty"
                :items="difficultiesOptions"
                item-title="text"
                item-value="value"
                label="الصعوبة"
                prepend-inner-icon="mdi-speedometer"
                variant="outlined"
                density="compact"
                rounded="lg"
                hide-details="auto"
              />
            </v-col>
            <v-col cols="6" sm="3">
              <v-select
                v-model="defaults.bloomLevel"
                :items="bloomLevels"
                label="مستوى بلوم"
                prepend-inner-icon="mdi-brain"
                variant="outlined"
                density="compact"
                rounded="lg"
                hide-details="auto"
              />
            </v-col>
          </v-row>
        </div>
      </v-expand-transition>

      <v-alert v-if="!isContextComplete" type="info" variant="tonal" density="compact" class="mt-3 rounded-xl">
        <v-icon start size="16">mdi-information</v-icon>
        يرجى اختيار المادة، الوحدة، والدرس لحفظ الأسئلة بنجاح.
      </v-alert>
    </div>

    <!-- Questions Toolbar Header -->
    <div class="d-flex align-center justify-space-between mb-4 flex-wrap gap-2">
      <div class="text-subtitle-1 font-weight-black d-flex align-center gap-2">
        <v-icon color="primary">mdi-format-list-numbered</v-icon>
        قائمة الأسئلة ({{ questions.length }})
      </div>
      <div class="d-flex align-center gap-2 flex-wrap">
        <custom-btn
          label="طي الكل"
          icon="unfold-less-horizontal"
          variant="outlined"
          color="medium-emphasis"
          class="font-weight-bold text-caption"
          :click="collapseAll"
        />
        <custom-btn
          label="توسيع الكل"
          icon="unfold-more-horizontal"
          variant="outlined"
          color="medium-emphasis"
          class="font-weight-bold text-caption"
          :click="expandAll"
        />
        <custom-btn
          type="add"
          label="إضافة سؤال جديد"
          class="font-weight-bold text-caption"
          :disabled="!canAddNewQuestion"
          :title="!canAddNewQuestion ? 'يرجى إكمال تجهيز السؤال الحالي أولاً لإضافة سؤال جديد' : 'إضافة سؤال جديد'"
          :click="addQuestion"
        />
      </div>
    </div>

    <!-- Questions List Form -->
    <v-form ref="formRef">
      <!-- Hidden file input for question helper image -->
      <input
        type="file"
        ref="singleImageInput"
        accept="image/*"
        class="d-none"
        @change="onQuestionImageSelected"
      />

      <div
        v-for="(q, index) in questions"
        :key="q.id"
        class="main-card rounded-2xl mb-4 overflow-hidden question-card-item"
      >
        <!-- Question Header Accordion -->
        <div
          class="question-card-header px-4 py-3 d-flex align-center justify-space-between cursor-pointer"
          @click="q.isCollapsed = !q.isCollapsed"
        >
          <div class="d-flex align-center gap-2 gap-sm-3 overflow-hidden flex-grow-1 me-2">
            <v-avatar
              :color="getTypeColor(q.type)"
              size="28"
              class="text-white font-weight-black flex-shrink-0 text-caption"
            >
              {{ index + 1 }}
            </v-avatar>

            <v-chip
              size="small"
              :color="getTypeColor(q.type)"
              variant="tonal"
              class="font-weight-bold flex-shrink-0"
            >
              <v-icon start size="14">{{ getTypeIcon(q.type) }}</v-icon>
              {{ getTypeLabel(q.type) }}
            </v-chip>

            <!-- Completion Status Indicator Chip -->
            <v-chip
              size="x-small"
              :color="isQuestionComplete(q) ? 'success' : 'warning'"
              variant="tonal"
              class="font-weight-bold flex-shrink-0"
            >
              <v-icon start size="12">{{ isQuestionComplete(q) ? 'mdi-check-circle' : 'mdi-clock-outline' }}</v-icon>
              {{ isQuestionComplete(q) ? 'مكتمل' : 'قيد الإعداد' }}
            </v-chip>

            <!-- Helper Image Badge (Header) -->
            <v-chip
              v-if="q.image"
              size="x-small"
              color="info"
              variant="tonal"
              class="font-weight-bold flex-shrink-0"
            >
              <v-icon start size="12">mdi-image</v-icon>
              صورة
            </v-chip>

            <span
              v-if="q.isCollapsed"
              class="text-body-2 font-weight-medium text-truncate flex-grow-1"
              style="max-width: 450px"
              v-html="renderSnippet(q.text) || 'سؤال بدون عنوان...'"
            >
            </span>

            <div v-if="q.isCollapsed" class="d-none d-sm-flex align-center gap-2 flex-shrink-0">
              <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                ⭐ {{ q.defaultScore }} د
              </v-chip>
              <v-chip
                size="x-small"
                :color="getDifficultyColor(q.difficulty)"
                variant="tonal"
                class="font-weight-bold"
              >
                <v-icon start size="12">{{ getDifficultyIcon(q.difficulty) }}</v-icon>
                {{ getDifficultyLabel(q.difficulty) }}
              </v-chip>
            </div>
          </div>

          <div class="d-flex align-center gap-1 flex-shrink-0">
            <custom-btn
              icon="mdi-content-copy"
              isIcon
              variant="text"
              color="medium-emphasis"
              title="نسخ السؤال"
              :click="(e) => { if (e) e.stopPropagation(); duplicateQuestion(index); }"
            />
            <custom-btn
              type="del"
              isIcon
              variant="text"
              title="حذف السؤال"
              :click="(e) => { if (e) e.stopPropagation(); removeQuestion(index); }"
            />
            <v-icon class="ms-1 text-medium-emphasis collapse-icon" :class="{ 'collapse-icon--open': !q.isCollapsed }">
              mdi-chevron-down
            </v-icon>
          </div>
        </div>

        <!-- Question Card Expandable Body -->
        <v-expand-transition>
          <div v-show="!q.isCollapsed" class="pa-4 pa-md-5 border-t border-slate-100">
            <v-row dense>
              <!-- Left / Main Column: Question Content & Answers (8 cols on desktop) -->
              <v-col cols="12" md="8" class="pe-md-3">
                <!-- Question Type Buttons -->
                <div class="mb-4">
                  <label class="text-caption font-weight-bold text-medium-emphasis mb-2 d-block">نوع السؤال</label>
                  <div class="type-selector-compact">
                    <v-btn
                      v-for="t in questionTypes"
                      :key="t.value"
                      size="small"
                      class="font-weight-bold type-btn"
                      :variant="q.type === t.value ? 'flat' : 'outlined'"
                      :color="q.type === t.value ? t.color : 'medium-emphasis'"
                      :class="q.type === t.value ? 'text-white' : ''"
                      rounded="lg"
                      @click="() => { q.type = t.value; onTypeChange(q); }"
                    >
                      <v-icon start size="15">{{ t.icon }}</v-icon>
                      {{ t.label }}
                    </v-btn>
                  </div>
                </div>

                <!-- Compact Helper Image Strip -->
                <div v-if="!q.image"
                  class="compact-image-strip pa-2 px-3 rounded-lg d-flex align-center justify-space-between mb-3 cursor-pointer"
                  @click="triggerImageUpload(index)">
                  <div class="d-flex align-center gap-2">
                    <v-icon size="17" color="primary">mdi-image-plus-outline</v-icon>
                    <span class="text-caption font-weight-bold image-strip-text">
                      الصورة المساعدة: اضغط لإرفاق رسم توضيحي أو مخطط لهذا السؤال (اختياري)
                    </span>
                  </div>
                  <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                    <v-icon start size="12">mdi-paperclip</v-icon>
                    استعراض صورة
                  </v-chip>
                </div>

                <!-- Attached Helper Image Card -->
                <div v-else
                  class="compact-helper-image-card pa-2 px-3 rounded-lg mb-3 d-flex align-center justify-space-between flex-wrap gap-2">
                  <div class="d-flex align-center gap-3">
                    <div class="image-thumb cursor-pointer" title="اضغط للمعاينة المكبرة" @click="openImagePreview(q.image)">
                      <img :src="q.image" alt="الصورة المساعدة" class="rounded-lg object-cover" />
                    </div>
                    <div>
                      <div class="text-caption font-weight-bold text-success d-flex align-center gap-1">
                        <v-icon size="14" color="success">mdi-check-circle</v-icon>
                        تم إرفاق الصورة المساعدة بنجاح
                      </div>
                      <span class="text-caption text-medium-emphasis">تظهر مع نص السؤال في ورقة الاختبار</span>
                    </div>
                  </div>
                  <div class="d-flex align-center gap-2">
                    <custom-btn
                      label="معاينة"
                      icon="mdi-eye-outline"
                      variant="tonal"
                      color="info"
                      density="compact"
                      size="small"
                      class="font-weight-bold"
                      :click="() => openImagePreview(q.image)"
                    />
                    <custom-btn
                      label="تغيير"
                      icon="mdi-swap-horizontal"
                      variant="tonal"
                      color="primary"
                      density="compact"
                      size="small"
                      class="font-weight-bold"
                      :click="() => triggerImageUpload(index)"
                    />
                    <custom-btn
                      type="del"
                      label="حذف"
                      variant="tonal"
                      density="compact"
                      size="small"
                      class="font-weight-bold"
                      :click="(e) => removeQuestionImage(index, e)"
                    />
                  </div>
                </div>

                <!-- Scientific Formula & Question Text Editor -->
                <scientific-formula-editor
                  v-model="q.text"
                  label="نص السؤال"
                  placeholder="اكتب صياغة السؤال هنا... انقر على زر (شريط الأدوات والرموز العلمية) بالأعلى لإدراج أي معادلات أو كسور أو رموز علمية."
                  :rows="3"
                  class="mb-4"
                />

                <!-- Answers Options Builder -->
                <div>
                  <!-- Single Choice / Multiple Choice Options -->
                  <template v-if="q.type === 'single_choice' || q.type === 'multiple_choice'">
                    <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
                      <div class="d-flex align-center gap-2">
                        <v-icon size="18" color="success">mdi-format-list-checks</v-icon>
                        <span class="text-subtitle-2 font-weight-bold">خيارات الإجابة:</span>
                      </div>
                      <v-chip size="x-small" variant="tonal" color="success" class="font-weight-bold">
                        {{ q.type === 'single_choice' ? 'حدد خيار الإجابة الصحيحة' : 'حدد الإجابات الصحيحة' }}
                      </v-chip>
                    </div>

                    <!-- Unboxed, standard clean option rows without enclosing cards -->
                    <div
                      v-for="(opt, oIndex) in q.options"
                      :key="oIndex"
                      class="d-flex align-center gap-2 mb-3"
                    >
                      <!-- Selection Radio / Checkbox -->
                      <div class="cursor-pointer" @click="toggleCorrectOption(q, oIndex)">
                        <v-radio-group
                          v-if="q.type === 'single_choice'"
                          v-model="q.correctAnswerIndex"
                          hide-details
                          class="ma-0"
                        >
                          <v-radio :value="oIndex" color="success" density="compact" />
                        </v-radio-group>
                        <v-checkbox
                          v-if="q.type === 'multiple_choice'"
                          v-model="q.correctAnswerIndices"
                          :value="oIndex"
                          color="success"
                          hide-details
                          density="compact"
                          class="ma-0"
                        />
                      </div>

                      <!-- Option Letter Badge (Square with slight radius, NOT circular) -->
                      <div
                        class="option-letter-badge font-weight-bold rounded-lg cursor-pointer"
                        :class="isCorrectOption(q, oIndex) ? 'option-letter--correct' : 'option-letter--default'"
                        title="انقر لتعيين هذا الخيار كإجابة صحيحة"
                        @click="toggleCorrectOption(q, oIndex)"
                      >
                        {{ String.fromCharCode(65 + oIndex) }}
                      </div>

                      <!-- Input Text Field (Standard clean input with live formula preview) -->
                      <div class="flex-grow-1">
                        <v-text-field
                          v-model="q.options[oIndex]"
                          :placeholder="'اكتب خيار الإجابة (' + String.fromCharCode(65 + oIndex) + ')'"
                          variant="outlined"
                          density="compact"
                          rounded="lg"
                          hide-details="auto"
                          :color="isCorrectOption(q, oIndex) ? 'success' : 'primary'"
                          :rules="[rules.required]"
                        />
                        <!-- Scientific Formula Auto-Preview for Option -->
                        <div
                          v-if="hasScientificMarkup(q.options[oIndex])"
                          class="option-formula-preview mt-1 px-3 py-1 rounded text-caption d-inline-flex align-center gap-2"
                        >
                          <v-icon size="13" color="primary">mdi-variable</v-icon>
                          <span class="text-medium-emphasis">المعاينة:</span>
                          <span class="font-weight-bold" v-html="renderOptionMarkup(q.options[oIndex])"></span>
                        </div>
                      </div>

                      <!-- Correct Answer Badge Chip -->
                      <v-chip
                        v-if="isCorrectOption(q, oIndex)"
                        size="x-small"
                        color="success"
                        variant="tonal"
                        class="font-weight-bold d-none d-sm-inline-flex"
                      >
                        <v-icon start size="12">mdi-check</v-icon>
                        إجابة صحيحة
                      </v-chip>

                      <!-- Delete Option Button -->
                      <custom-btn
                        v-if="q.options.length > 2"
                        type="del"
                        isIcon
                        variant="text"
                        density="compact"
                        title="حذف الخيار"
                        :click="() => q.options.splice(oIndex, 1)"
                      />
                    </div>

                    <custom-btn
                      type="add"
                      label="إضافة خيار إجابة"
                      size="small"
                      class="font-weight-bold mt-2"
                      :click="() => q.options.push('')"
                    />
                  </template>

                  <!-- True / False Options -->
                  <template v-else-if="q.type === 'true_false'">
                    <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
                      <div class="d-flex align-center gap-2">
                        <v-icon size="18" color="success">mdi-scale-balance</v-icon>
                        <span class="text-subtitle-2 font-weight-bold">الإجابة الصحيحة:</span>
                      </div>
                      <v-chip size="x-small" variant="tonal" color="success" class="font-weight-bold">
                        حدد الإجابة النموذجية للسؤال
                      </v-chip>
                    </div>
                    <div class="d-flex gap-3">
                      <v-btn
                        class="flex-grow-1 font-weight-bold"
                        :variant="q.tfCorrect === true ? 'flat' : 'outlined'"
                        :color="q.tfCorrect === true ? 'success' : undefined"
                        :class="q.tfCorrect === true ? 'text-white' : ''"
                        rounded="lg"
                        prepend-icon="mdi-check-circle"
                        @click="q.tfCorrect = true"
                      >
                        صواب (True)
                      </v-btn>
                      <v-btn
                        class="flex-grow-1 font-weight-bold"
                        :variant="q.tfCorrect === false ? 'flat' : 'outlined'"
                        :color="q.tfCorrect === false ? 'error' : undefined"
                        :class="q.tfCorrect === false ? 'text-white' : ''"
                        rounded="lg"
                        prepend-icon="mdi-close-circle"
                        @click="q.tfCorrect = false"
                      >
                        خطأ (False)
                      </v-btn>
                    </div>
                  </template>

                  <!-- Essay Options -->
                  <template v-else-if="q.type === 'essay'">
                    <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
                      <div class="d-flex align-center gap-2">
                        <v-icon size="18" color="primary">mdi-text-box-check-outline</v-icon>
                        <span class="text-subtitle-2 font-weight-bold">الإجابة النموذجية المعتمدة (للمصحح):</span>
                      </div>
                    </div>
                    <scientific-formula-editor
                      v-model="q.options[0]"
                      label="نص الإجابة النموذجية"
                      placeholder="اكتب الإجابة النموذجية وعناصر التصحيح هنا..."
                      :rows="2"
                    />
                  </template>
                </div>
              </v-col>

              <!-- Right Column: Question Properties (4 cols on desktop, compact on mobile) -->
              <v-col cols="12" md="4" class="mt-4 mt-md-0">
                <div class="pa-4 rounded-xl properties-box">
                  <div class="text-subtitle-2 font-weight-black mb-3 d-flex align-center gap-1 text-high-emphasis">
                    <v-icon size="16" color="warning">mdi-tune</v-icon>
                    خصائص وعلامات السؤال
                  </div>

                  <v-row dense>
                    <v-col cols="6" md="12" class="mb-md-2">
                      <label class="text-caption font-weight-bold text-medium-emphasis mb-1 d-block">الدرجة</label>
                      <v-text-field
                        v-model.number="q.defaultScore"
                        type="number"
                        min="1"
                        variant="outlined"
                        density="compact"
                        rounded="lg"
                        hide-details="auto"
                      />
                    </v-col>

                    <v-col cols="6" md="12" class="mb-md-2">
                      <label class="text-caption font-weight-bold text-medium-emphasis mb-1 d-block">الزمن (دقائق)</label>
                      <v-text-field
                        v-model.number="q.expectedTimeMinutes"
                        type="number"
                        min="1"
                        variant="outlined"
                        density="compact"
                        rounded="lg"
                        hide-details="auto"
                      />
                    </v-col>

                    <v-col cols="6" md="12" class="mb-md-2">
                      <label class="text-caption font-weight-bold text-medium-emphasis mb-1 d-block">مستوى الصعوبة</label>
                      <v-select
                        v-model="q.difficulty"
                        :items="difficultiesOptions"
                        item-title="text"
                        item-value="value"
                        variant="outlined"
                        density="compact"
                        rounded="lg"
                        hide-details="auto"
                      />
                    </v-col>

                    <v-col cols="6" md="12">
                      <label class="text-caption font-weight-bold text-medium-emphasis mb-1 d-block">مستوى بلوم</label>
                      <v-select
                        v-model="q.bloomLevel"
                        :items="bloomLevels"
                        variant="outlined"
                        density="compact"
                        rounded="lg"
                        hide-details="auto"
                      />
                    </v-col>
                  </v-row>
                </div>
              </v-col>
            </v-row>

            <!-- Card Bottom Bar: Readiness & Add Next Question -->
            <div class="mt-4 pt-3 border-t d-flex align-center justify-space-between flex-wrap gap-2">
              <div class="d-flex align-center gap-2">
                <v-chip
                  v-if="isQuestionComplete(q)"
                  size="small"
                  color="success"
                  variant="tonal"
                  class="font-weight-bold"
                >
                  <v-icon start size="14">mdi-check-circle</v-icon>
                  تم تجهيز السؤال بالكامل وهو جاهز للحفظ
                </v-chip>
                <v-chip
                  v-else
                  size="small"
                  color="warning"
                  variant="tonal"
                  class="font-weight-bold"
                >
                  <v-icon start size="14">mdi-alert-circle-outline</v-icon>
                  {{ getQuestionIncompleteSummary(q) }}
                </v-chip>
              </div>

              <div class="d-flex align-center gap-2">
                <custom-btn
                  v-if="index === questions.length - 1"
                  type="add"
                  label="تجهيز وإضافة السؤال التالي"
                  icon="mdi-plus-circle"
                  :disabled="!isQuestionComplete(q)"
                  :title="!isQuestionComplete(q) ? 'أكمل تجهيز هذا السؤال أولاً لإضافة السؤال التالي' : 'إضافة السؤال التالي'"
                  class="font-weight-bold"
                  :click="addQuestion"
                />
                <custom-btn
                  v-else
                  label="السؤال التالي"
                  icon="mdi-chevron-left"
                  variant="tonal"
                  color="primary"
                  class="font-weight-bold"
                  :click="() => { collapseAll(); questions[index + 1].isCollapsed = false; }"
                />
              </div>
            </div>
          </div>
        </v-expand-transition>
      </div>
    </v-form>

    <!-- Empty State -->
    <div v-if="questions.length === 0" class="main-card pa-8 text-center rounded-2xl">
      <v-avatar size="64" color="primary" variant="tonal" class="mb-3 mx-auto">
        <v-icon size="32">mdi-lightning-bolt-outline</v-icon>
      </v-avatar>
      <h3 class="text-h6 font-weight-black mb-1">لا توجد أسئلة في القائمة</h3>
      <p class="text-body-2 text-medium-emphasis mb-4">ابدأ بإضافة السؤال الأول لإدخال البيانات بسرعة.</p>
      <custom-btn type="add" label="إضافة السؤال الأول" class="font-weight-bold" :click="addQuestion" />
    </div>

    <!-- Floating Action Button -->
    <custom-btn
      v-if="questions.length > 0"
      type="add"
      isIcon
      color="primary"
      class="fab-btn"
      :disabled="!canAddNewQuestion"
      :title="!canAddNewQuestion ? 'يرجى إكمال تجهيز السؤال الحالي أولاً لإضافة سؤال آخر' : 'إضافة سؤال آخر'"
      :click="addQuestion"
    />

    <!-- Full Image Preview Modal Dialog -->
    <v-dialog v-model="previewImageDialog" max-width="750" scrollable>
      <v-card class="rounded-xl overflow-hidden main-card">
        <v-card-title class="d-flex align-center justify-space-between py-3 px-4 border-b">
          <div class="d-flex align-center gap-2">
            <v-icon color="primary" size="20">mdi-image-outline</v-icon>
            <span class="text-subtitle-1 font-weight-bold">معاينة الصورة المساعدة للسؤال</span>
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" @click="previewImageDialog = false" />
        </v-card-title>
        <v-card-text class="pa-4 text-center" style="background: rgba(var(--v-theme-surface-variant), 0.15);">
          <img
            :src="previewImageSrc"
            alt="معاينة الصورة"
            style="max-width: 100%; max-height: 70vh; object-fit: contain; border-radius: 8px;"
          />
        </v-card-text>
        <v-card-actions class="px-4 py-3 justify-end">
          <custom-btn
            label="إغلاق"
            variant="tonal"
            color="secondary"
            :click="() => previewImageDialog = false"
          />
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { academicService } from "@/services/academicService";
import { bankService } from "@/services/bankService";
import ScientificFormulaEditor from "@/components/common/ScientificFormulaEditor.vue";
import { parseScientificMarkup, ensureKaTeXLoaded } from "@/utils/scientificRenderer";

export default {
  name: "QuestionFastEntryView",

  components: {
    ScientificFormulaEditor,
  },

  data() {
    return {
      saving: false,
      showDefaults: false,
      activeImageQuestionIndex: null,
      previewImageSrc: "",
      previewImageDialog: false,

      // Context
      context: {
        institution_type: "school",
        // School
        stageId: null,
        classTrackId: null,
        subjectId: null,
        semesterId: null,
        // University
        collegeId: null,
        departmentId: null,
        specializationId: null,
        semesterSubjectId: null,
        // Institute
        instituteFieldId: null,
        instituteEducationSystemId: null,
        instituteSpecializationId: null,
        instituteCurriculumId: null,
        instituteSubjectId: null,
        // Common
        unitId: null,
        lessonId: null,
        learningOutcomeId: null,
      },

      // Defaults
      defaults: {
        defaultScore: 1,
        expectedTimeMinutes: 1,
        difficulty: 2,
        bloomLevel: "تطبيق",
      },

      // Questions Array
      questions: [],

      // Options
      institutionTypes: [
        { text: "تعليم مدرسي (م)", value: "school", icon: "mdi-school" },
        { text: "تعليم جامعي (ج)", value: "university", icon: "mdi-domain" },
        { text: "معاهد وتدريب مهني (ع)", value: "institute", icon: "mdi-tools" },
      ],
      difficultiesOptions: [
        { text: "سهل", value: 1 },
        { text: "متوسط", value: 2 },
        { text: "صعب", value: 3 },
      ],
      bloomLevels: ["تذكر", "فهم", "تطبيق", "تحليل", "تقييم", "ابتكار"],
      questionTypes: [
        { value: "single_choice", label: "مفرد", color: "indigo", icon: "mdi-record-circle" },
        { value: "multiple_choice", label: "متعدد", color: "warning", icon: "mdi-checkbox-multiple-marked" },
        { value: "true_false", label: "صواب/خطأ", color: "success", icon: "mdi-toggle-switch" },
        { value: "essay", label: "مقالي", color: "primary", icon: "mdi-text-box-edit" },
      ],
      rules: {
        required: (v) => !!v || v === 0 || "مطلوب",
      },
    };
  },

  computed: {
    isContextComplete() {
      if (this.context.institution_type === 'university') {
        return !!(this.context.semesterSubjectId && this.context.unitId && this.context.lessonId);
      } else if (this.context.institution_type === 'institute') {
        return !!(this.context.instituteSubjectId && this.context.unitId && this.context.lessonId);
      }
      return !!(this.context.subjectId && this.context.unitId && this.context.lessonId);
    },

    canAddNewQuestion() {
      if (this.questions.length === 0) return true;
      return this.questions.every((q) => this.isQuestionComplete(q));
    },
  },

  created() {
    this.addQuestion();
  },

  mounted() {
    ensureKaTeXLoaded();
  },

  methods: {
    // === CASCADE HANDLERS ===
    onInstitutionTypeToggle() {
      this.context.stageId = null;
      this.context.classTrackId = null;
      this.context.subjectId = null;
      this.context.semesterId = null;
      this.context.collegeId = null;
      this.context.departmentId = null;
      this.context.specializationId = null;
      this.context.semesterSubjectId = null;
      this.context.instituteFieldId = null;
      this.context.instituteEducationSystemId = null;
      this.context.instituteSpecializationId = null;
      this.context.instituteCurriculumId = null;
      this.context.instituteSubjectId = null;
      this.context.unitId = null;
      this.context.lessonId = null;
      this.context.learningOutcomeId = null;
    },

    onInstituteFieldChange() {
      this.context.instituteEducationSystemId = null;
      this.context.instituteSpecializationId = null;
      this.context.instituteCurriculumId = null;
      this.context.instituteSubjectId = null;
      this.context.unitId = null;
      this.context.lessonId = null;
      this.context.learningOutcomeId = null;
    },

    onInstituteEducationSystemChange() {
      this.context.instituteSpecializationId = null;
      this.context.instituteCurriculumId = null;
    },

    onInstituteSpecializationChange() {
      this.context.instituteCurriculumId = null;
    },

    onInstituteSubjectChange() {
      this.context.unitId = null;
      this.context.lessonId = null;
      this.context.learningOutcomeId = null;
    },

    onStageChange() {
      this.context.classTrackId = null;
      this.context.subjectId = null;
      this.context.unitId = null;
      this.context.lessonId = null;
      this.context.learningOutcomeId = null;
    },

    onClassTrackChange() {
      this.context.subjectId = null;
      this.context.unitId = null;
      this.context.lessonId = null;
      this.context.learningOutcomeId = null;
    },

    onSubjectChange() {
      this.context.unitId = null;
      this.context.lessonId = null;
      this.context.learningOutcomeId = null;
    },

    onCollegeChange() {
      this.context.departmentId = null;
      this.context.specializationId = null;
      this.context.semesterSubjectId = null;
      this.context.unitId = null;
      this.context.lessonId = null;
      this.context.learningOutcomeId = null;
    },

    onDepartmentChange() {
      this.context.specializationId = null;
      this.context.semesterSubjectId = null;
      this.context.unitId = null;
      this.context.lessonId = null;
      this.context.learningOutcomeId = null;
    },

    onSpecializationChange() {
      this.context.semesterSubjectId = null;
      this.context.unitId = null;
      this.context.lessonId = null;
      this.context.learningOutcomeId = null;
    },

    onSemesterSubjectChange() {
      this.context.unitId = null;
      this.context.lessonId = null;
      this.context.learningOutcomeId = null;
    },

    onUnitChange() {
      this.context.lessonId = null;
      this.context.learningOutcomeId = null;
    },

    // === QUESTIONS MANAGEMENT ===
    createQuestionObject() {
      return {
        id: Date.now() + Math.random(),
        isCollapsed: false,
        image: "",
        text: "",
        type: "single_choice",
        options: ["", "", "", ""],
        correctAnswerIndex: 0,
        correctAnswerIndices: [],
        tfCorrect: true,
        defaultScore: this.defaults.defaultScore,
        expectedTimeMinutes: this.defaults.expectedTimeMinutes,
        difficulty: this.defaults.difficulty,
        bloomLevel: this.defaults.bloomLevel,
      };
    },

    // === HELPER IMAGE MANAGEMENT ===
    triggerImageUpload(index) {
      this.activeImageQuestionIndex = index;
      if (this.$refs.singleImageInput) {
        this.$refs.singleImageInput.value = "";
        this.$refs.singleImageInput.click();
      }
    },
    onQuestionImageSelected(event) {
      const file = event.target.files && event.target.files[0];
      if (!file) return;
      if (this.activeImageQuestionIndex === null || !this.questions[this.activeImageQuestionIndex]) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        this.questions[this.activeImageQuestionIndex].image = e.target.result;
        this.$alert("success", { message: "تم إرفاق الصورة المساعدة بنجاح" });
      };
      reader.readAsDataURL(file);
    },
    removeQuestionImage(index, event) {
      if (event) event.stopPropagation();
      if (this.questions[index]) {
        this.questions[index].image = "";
      }
    },
    openImagePreview(imageSrc) {
      if (!imageSrc) return;
      this.previewImageSrc = imageSrc;
      this.previewImageDialog = true;
    },

    // === OPTION & SCIENTIFIC HELPERS ===
    isCorrectOption(q, oIndex) {
      if (q.type === 'single_choice') {
        return q.correctAnswerIndex === oIndex;
      }
      if (q.type === 'multiple_choice') {
        return Array.isArray(q.correctAnswerIndices) && q.correctAnswerIndices.includes(oIndex);
      }
      return false;
    },
    toggleCorrectOption(q, oIndex) {
      if (q.type === 'single_choice') {
        q.correctAnswerIndex = oIndex;
      } else if (q.type === 'multiple_choice') {
        if (!Array.isArray(q.correctAnswerIndices)) {
          q.correctAnswerIndices = [];
        }
        const idx = q.correctAnswerIndices.indexOf(oIndex);
        if (idx > -1) {
          q.correctAnswerIndices.splice(idx, 1);
        } else {
          q.correctAnswerIndices.push(oIndex);
        }
      }
    },
    hasScientificMarkup(text) {
      if (!text || typeof text !== 'string') return false;
      return (
        text.includes('$') ||
        text.includes('\\') ||
        text.includes('_{') ||
        text.includes('^{') ||
        text.includes('->') ||
        text.includes('<-')
      );
    },
    renderOptionMarkup(text) {
      if (!text) return '';
      try {
        return parseScientificMarkup(text);
      } catch (e) {
        return text;
      }
    },
    renderSnippet(text) {
      if (!text) return '';
      const plain = text.replace(/<[^>]*>/g, '').replace(/\$+/g, '').trim();
      return plain.length > 60 ? plain.substring(0, 60) + '...' : plain;
    },
    // === COMPLETION & READINESS VALIDATION ===
    isQuestionComplete(q) {
      if (!q) return false;
      if (!q.text || !q.text.trim()) return false;
      if (q.type === 'single_choice') {
        if (!q.options || q.options.length < 2) return false;
        if (q.options.some((opt) => !opt || !opt.trim())) return false;
        if (
          q.correctAnswerIndex === null ||
          q.correctAnswerIndex === undefined ||
          q.correctAnswerIndex < 0 ||
          q.correctAnswerIndex >= q.options.length
        ) {
          return false;
        }
      } else if (q.type === 'multiple_choice') {
        if (!q.options || q.options.length < 2) return false;
        if (q.options.some((opt) => !opt || !opt.trim())) return false;
        if (!q.correctAnswerIndices || q.correctAnswerIndices.length === 0) return false;
      } else if (q.type === 'true_false') {
        if (typeof q.tfCorrect !== 'boolean') return false;
      } else if (q.type === 'essay') {
        if (!q.options || !q.options[0] || !q.options[0].trim()) return false;
      }
      return true;
    },

    getQuestionIncompleteSummary(q) {
      if (!q) return 'قيد الإعداد';
      if (!q.text || !q.text.trim()) return 'يرجى كتابة نص السؤال';
      if (q.type === 'single_choice' || q.type === 'multiple_choice') {
        if (!q.options || q.options.length < 2) return 'أضف خيارين على الأقل';
        const emptyIdx = q.options.findIndex((opt) => !opt || !opt.trim());
        if (emptyIdx !== -1) {
          const letter = String.fromCharCode(65 + emptyIdx);
          return `يرجى كتابة خيار (${letter}) أو حذفه`;
        }
        if (q.type === 'single_choice') {
          if (
            q.correctAnswerIndex === null ||
            q.correctAnswerIndex === undefined ||
            q.correctAnswerIndex < 0 ||
            q.correctAnswerIndex >= q.options.length
          ) {
            return 'يرجى تحديد خيار الإجابة الصحيحة';
          }
        } else {
          if (!q.correctAnswerIndices || q.correctAnswerIndices.length === 0) {
            return 'حدد إجابة صحيحة واحدة على الأقل';
          }
        }
      } else if (q.type === 'essay') {
        if (!q.options || !q.options[0] || !q.options[0].trim()) {
          return 'يرجى كتابة الإجابة النموذجية';
        }
      }
      return 'قيد الإعداد';
    },

    getQuestionCompletionValidation(q, index) {
      const num = index !== undefined && index !== null ? index + 1 : 1;
      if (!q) return { valid: false, message: `السؤال رقم ${num} غير موجود` };

      if (!q.text || !q.text.trim()) {
        return {
          valid: false,
          message: `يرجى كتابة نص السؤال (السؤال رقم ${num}) أولاً قبل إضافة سؤال جديد.`,
        };
      }

      if (q.type === 'single_choice' || q.type === 'multiple_choice') {
        if (!q.options || q.options.length < 2) {
          return {
            valid: false,
            message: `يجب توفير خيارين على الأقل في السؤال رقم ${num}.`,
          };
        }
        const emptyIdx = q.options.findIndex((opt) => !opt || !opt.trim());
        if (emptyIdx !== -1) {
          const letter = String.fromCharCode(65 + emptyIdx);
          return {
            valid: false,
            message: `يرجى كتابة نص الخيار (${letter}) أو حذفه في السؤال رقم ${num} قبل إضافة سؤال جديد.`,
          };
        }
        if (q.type === 'single_choice') {
          if (
            q.correctAnswerIndex === null ||
            q.correctAnswerIndex === undefined ||
            q.correctAnswerIndex < 0 ||
            q.correctAnswerIndex >= q.options.length
          ) {
            return {
              valid: false,
              message: `يرجى تحديد خيار الإجابة الصحيحة في السؤال رقم ${num}.`,
            };
          }
        } else {
          if (!q.correctAnswerIndices || q.correctAnswerIndices.length === 0) {
            return {
              valid: false,
              message: `يرجى تحديد إجابة صحيحة واحدة على الأقل في السؤال رقم ${num}.`,
            };
          }
        }
      } else if (q.type === 'essay') {
        if (!q.options || !q.options[0] || !q.options[0].trim()) {
          return {
            valid: false,
            message: `يرجى كتابة الإجابة النموذجية للسؤال المقالي رقم ${num}.`,
          };
        }
      }

      return { valid: true };
    },

    addQuestion() {
      if (this.questions.length > 0) {
        const incompleteIndex = this.questions.findIndex((q) => !this.isQuestionComplete(q));
        if (incompleteIndex !== -1) {
          const incompleteQ = this.questions[incompleteIndex];
          const validation = this.getQuestionCompletionValidation(incompleteQ, incompleteIndex);
          this.$alert("warning", {
            title: "تنبيه: يجب إكمال السؤال الحالي",
            message: validation.message,
          });
          this.collapseAll();
          incompleteQ.isCollapsed = false;
          return;
        }
      }

      this.questions.push(this.createQuestionObject());
      this.collapseAll();
      this.questions[this.questions.length - 1].isCollapsed = false;
    },
    duplicateQuestion(index) {
      const q = this.questions[index];
      const validation = this.getQuestionCompletionValidation(q, index);
      if (!validation.valid) {
        this.$alert("warning", {
          title: "تنبيه: تعذر نسخ السؤال",
          message: `يرجى إكمال بيانات هذا السؤال أولاً قبل نسخه: ${validation.message}`,
        });
        this.collapseAll();
        q.isCollapsed = false;
        return;
      }
      const newQ = JSON.parse(JSON.stringify(q));
      newQ.id = Date.now() + Math.random();
      this.questions.splice(index + 1, 0, newQ);
      this.collapseAll();
      newQ.isCollapsed = false;
      this.$alert("info", { message: `تم نسخ السؤال بنجاح` });
    },
    removeQuestion(index) {
      this.questions.splice(index, 1);
    },
    onTypeChange(q) {
      if (q.type === 'single_choice' || q.type === 'multiple_choice') {
        if (q.options.length === 0 || (q.options.length === 1 && !q.options[0])) {
          q.options = ["", "", "", ""];
        }
      } else if (q.type === 'essay') {
        q.options = [""];
      }
    },
    collapseAll() {
      this.questions.forEach((q) => (q.isCollapsed = true));
    },
    expandAll() {
      this.questions.forEach((q) => (q.isCollapsed = false));
    },
    applyDefaultsToAll() {
      this.questions.forEach((q) => {
        q.defaultScore = this.defaults.defaultScore;
        q.expectedTimeMinutes = this.defaults.expectedTimeMinutes;
        q.difficulty = this.defaults.difficulty;
        q.bloomLevel = this.defaults.bloomLevel;
      });
      this.$alert("success", { message: "تم تطبيق القيم الافتراضية على جميع الأسئلة" });
    },

    // === HELPERS ===
    getTypeLabel(type) {
      const t = this.questionTypes.find((x) => x.value === type);
      return t ? t.label : type;
    },
    getTypeColor(type) {
      const t = this.questionTypes.find((x) => x.value === type);
      return t ? t.color : "grey";
    },
    getTypeIcon(type) {
      const t = this.questionTypes.find((x) => x.value === type);
      return t ? t.icon : "mdi-help";
    },
    getDifficultyLabel(diff) {
      const d = String(diff ?? '').toLowerCase().trim();
      if (d === '1' || d === 'easy' || d === 'سهل') return 'سهل';
      if (d === '2' || d === 'medium' || d === 'متوسط') return 'متوسط';
      if (d === '3' || d === 'hard' || d === 'صعب') return 'صعب';
      return diff || '-';
    },
    getDifficultyColor(diff) {
      const d = String(diff ?? '').toLowerCase().trim();
      if (d === '1' || d === 'easy' || d === 'سهل') return 'success';
      if (d === '2' || d === 'medium' || d === 'متوسط') return 'warning';
      if (d === '3' || d === 'hard' || d === 'صعب') return 'error';
      return 'blue-grey';
    },
    getDifficultyIcon(diff) {
      const d = String(diff ?? '').toLowerCase().trim();
      if (d === '1' || d === 'easy' || d === 'سهل') return 'mdi-signal-cellular-1';
      if (d === '2' || d === 'medium' || d === 'متوسط') return 'mdi-signal-cellular-2';
      if (d === '3' || d === 'hard' || d === 'صعب') return 'mdi-signal-cellular-3';
      return 'mdi-help-circle-outline';
    },

    // === TYPE MAPPING ===
    mapQuestionType(frontendType) {
      const map = {
        single_choice: 'Single Choice',
        multiple_choice: 'Multiple Choice',
        true_false: 'True/False',
        essay: 'Essay',
        fill_blanks: 'Fill in the Blanks',
      };
      return map[frontendType] || frontendType;
    },

    // === SUBMIT ===
    async saveAllQuestions() {
      if (this.questions.length === 0) return;
      if (!this.isContextComplete) {
        this.$alert("errorData", { message: "يرجى إكمال تحديد المادة والوحدة والدرس المشترك" });
        return;
      }

      const { valid } = await this.$refs.formRef.validate();
      if (!valid) {
        this.$alert("errorData", { message: "يرجى ملء جميع الحقول الإلزامية في الأسئلة" });
        this.expandAll();
        return;
      }

      const hasEmptyText = this.questions.some((q) => !q.text || !q.text.trim());
      if (hasEmptyText) {
        this.$alert("errorData", { message: "يرجى كتابة نص السؤال لجميع الأسئلة قبل الحفظ" });
        this.expandAll();
        return;
      }

      const hasInvalidMC = this.questions.some((q) => q.type === "multiple_choice" && q.correctAnswerIndices.length === 0);
      if (hasInvalidMC) {
        this.$alert("errorData", { message: "تأكد من اختيار إجابة صحيحة واحدة على الأقل لأسئلة الاختيار المتعدد" });
        return;
      }

      this.saving = true;
      try {
        const payload = {
          lesson: this.context.lessonId,
          institution_type: this.context.institution_type || "school",
          questions: this.questions.map((q) => {
            const questionData = {
              content: q.text,
              image: q.image || "",
              questionType: this.mapQuestionType(q.type),
              institution_type: this.context.institution_type || "school",
              difficulty: q.difficulty,
              bloomLevel: q.bloomLevel,
              learningOutcome: q.learningOutcomeId || this.context.learningOutcomeId || null,
              defaultMark: q.defaultScore,
              expected_time_minutes: q.expectedTimeMinutes,
              status: "قيد المراجعة",
              options: [],
            };

            if (q.type === "single_choice" || q.type === "multiple_choice") {
              questionData.options = q.options.map((optText, i) => ({
                text: optText,
                isTrue: q.type === "single_choice" ? i === q.correctAnswerIndex : q.correctAnswerIndices.includes(i),
                order: i + 1,
              }));
            } else if (q.type === "true_false") {
              questionData.options = [
                { text: "صواب", isTrue: q.tfCorrect === true, order: 1 },
                { text: "خطأ", isTrue: q.tfCorrect === false, order: 2 },
              ];
            } else if (q.type === "essay") {
              questionData.options = [
                { text: q.options[0] || "", isTrue: true, order: 1 },
              ];
            }

            return questionData;
          }),
        };

        await bankService.fastBulkCreateQuestions(payload);

        this.$alert("success", { message: `تم حفظ ${this.questions.length} أسئلة بنجاح!` });
        this.$navigateTo({ name: "question-bank", blank: false });
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء حفظ الأسئلة" });
        console.error(err);
      } finally {
        this.saving = false;
      }
    },
  },
};
</script>

<style scoped>
.qb-fast-page-v4 {
  color: rgb(var(--v-theme-on-surface));
}

/* ===== Main Cards (Theme Compatible) ===== */
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

/* ===== Sticky Context Bar ===== */
.sticky-context-bar {
  position: sticky;
  top: 12px;
  z-index: 10;
}

/* ===== Question Card Items ===== */
.question-card-item {
  background: rgb(var(--v-theme-surface)) !important;
  border-radius: 16px;
  border: 1px solid rgba(var(--v-border-color), 0.16);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
  transition: all 0.25s ease;
}

.question-card-item:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

.question-card-header {
  background: rgb(var(--v-theme-background));
  border-radius: 16px 16px 0 0;
  transition: background 0.2s ease;
}

.question-card-header:hover {
  background: rgba(var(--v-theme-primary), 0.04);
}

.collapse-icon {
  transition: transform 0.25s ease;
}

.collapse-icon--open {
  transform: rotate(180deg);
}

/* ===== Type Selector Pills ===== */
.type-selector-compact {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.type-btn {
  min-width: 90px;
}

/* ===== Properties Sidebar Box ===== */
.properties-box {
  background: rgb(var(--v-theme-background));
  border: 1px solid rgba(var(--v-border-color), 0.12);
}

/* ===== Option Row ===== */
.option-row {
  min-height: 40px;
}

/* ===== Floating Action Button ===== */
.fab-btn {
  position: fixed;
  bottom: 24px;
  left: 24px;
  z-index: 99;
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.45) !important;
  transition: transform 0.25s ease, box-shadow 0.25s ease !important;
}

.fab-btn:hover {
  transform: scale(1.08);
  box-shadow: 0 12px 32px rgba(var(--v-theme-primary), 0.6) !important;
}

/* ===== Gap Utilities ===== */
.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }

/* ===== Compact Helper Image Styles (Theme-Adaptive) ===== */
.compact-image-strip {
  background: rgba(var(--v-theme-primary), 0.04);
  border: 1px dashed rgba(var(--v-theme-primary), 0.28);
  border-radius: 8px;
  color: rgb(var(--v-theme-on-surface));
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.compact-image-strip:hover {
  background: rgba(var(--v-theme-primary), 0.08);
  border-color: rgba(var(--v-theme-primary), 0.55);
}

.image-strip-text {
  color: rgba(var(--v-theme-on-surface), 0.75);
}

.compact-helper-image-card {
  background: rgba(var(--v-theme-success), 0.05);
  border: 1px solid rgba(var(--v-theme-success), 0.28);
  border-radius: 8px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.image-thumb img {
  width: 44px;
  height: 44px;
  object-fit: cover;
  border: 1.5px solid rgba(var(--v-theme-success), 0.4);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: block;
}

.image-thumb:hover img {
  transform: scale(1.06);
  box-shadow: 0 4px 12px rgba(var(--v-theme-success), 0.2);
}

/* ===== Option Letter Badges (Unboxed & Standard Non-Circular) ===== */
.option-letter-badge {
  width: 36px;
  height: 36px;
  min-width: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  border-radius: 8px; /* Standard rounded-lg, NOT circular */
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
}

.option-letter--default {
  background: rgba(var(--v-theme-surface-variant), 0.5);
  color: rgba(var(--v-theme-on-surface), 0.7);
  border: 1px solid rgba(var(--v-border-color), 0.15);
}

.option-letter--default:hover {
  background: rgba(var(--v-theme-primary), 0.08);
  border-color: rgba(var(--v-theme-primary), 0.4);
}

.option-letter--correct {
  background: rgb(var(--v-theme-success)) !important;
  color: #ffffff !important;
  border: 1px solid rgb(var(--v-theme-success));
  box-shadow: 0 2px 8px rgba(var(--v-theme-success), 0.3);
}

/* Option Formula Live Preview */
.option-formula-preview {
  background: rgba(var(--v-theme-surface-variant), 0.45);
  border: 1px dashed rgba(var(--v-theme-primary), 0.25);
  border-radius: 8px;
  color: rgb(var(--v-theme-on-surface));
}
</style>
