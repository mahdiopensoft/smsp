<!-- Responsive & Theme Compatible QuestionNewView -->
<template>
  <div class="qb-new-page-v4">

    <!-- Main Form -->
    <v-form ref="formRef" @submit.prevent>
      <v-row>
        <!-- Left Column: Question Content & Options Builder -->
        <v-col cols="12" lg="8">
          <div class="main-card pa-6 mb-6 rounded-2xl">
            <!-- Question Type Selector -->
            <div class="mb-6">
              <h3 class="text-h6  mb-4 d-flex align-center gap-2">
                <v-icon color="indigo">mdi-shape-outline</v-icon>
                اختر نوع السؤال
              </h3>

              <v-item-group mandatory v-model="form.type" class="type-selector-grid">
                <v-item v-for="qt in questionTypeOptions" :key="qt.value" :value="qt.value"
                  v-slot="{ isSelected, toggle }">
                  <div class="type-option-card pa-4 rounded-xl d-flex align-center gap-3"
                    :class="[
                      `type-card-${qt.color}`,
                      { 'type-option-card--active': isSelected }
                    ]"
                    @click="toggle">
                    <v-avatar size="42" :color="qt.color" :variant="isSelected ? 'flat' : 'tonal'"
                      :class="isSelected ? 'text-white' : ''" rounded="lg">
                      <v-icon size="22" :color="isSelected ? 'white' : qt.color">{{ isSelected ? qt.iconActive : qt.icon }}</v-icon>
                    </v-avatar>
                    <div>
                      <div class="text-body-2 font-weight-black" :class="isSelected ? 'text-white' : `text-${qt.color}`">
                        {{ qt.label }}
                      </div>
                    </div>
                  </div>
                </v-item>
              </v-item-group>
            </div>

            <v-divider class="my-6 opacity-20" />

            <!-- Question Text Editor & Compact Helper Image Area -->
            <div class="mb-6">
              <div class="d-flex align-center justify-space-between mb-3">
                <h3 class="text-h6 mb-0 d-flex align-center gap-2">
                  <v-icon color="primary">mdi-text-box-edit-outline</v-icon>
                  صياغة السؤال والوسائط
                </h3>
              </div>

              <!-- Hidden File Input -->
              <input type="file" ref="imageInput" accept="image/*" class="d-none" @change="onImageSelected" />

              <!-- Compact Helper Image Area: State 1 (No Image Attached) -->
              <div v-if="!form.image"
                class="compact-image-strip pa-2 px-3 rounded-lg d-flex align-center justify-space-between mb-3 cursor-pointer"
                @click="$refs.imageInput.click()">
                <div class="d-flex align-center gap-2">
                  <v-icon size="18" color="primary">mdi-image-plus-outline</v-icon>
                  <span class="text-caption font-weight-bold image-strip-text">
                    الصورة المساعدة: اضغط لإرفاق رسم توضيحي أو مخطط للسؤال (اختياري)
                  </span>
                </div>
                <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                  <v-icon start size="12">mdi-paperclip</v-icon>
                  استعراض صورة
                </v-chip>
              </div>

              <!-- Compact Helper Image Area: State 2 (Image Attached) -->
              <div v-else
                class="compact-helper-image-card pa-2 px-3 rounded-xl mb-3 d-flex align-center justify-space-between flex-wrap gap-2">
                <div class="d-flex align-center gap-3">
                  <div class="image-thumb cursor-pointer" title="اضغط للمعاينة المكبرة" @click="previewImageDialog = true">
                    <img :src="form.image" alt="الصورة المساعدة" class="rounded-lg object-cover" />
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
                    class="font-weight-bold"
                    :click="() => previewImageDialog = true"
                  />
                  <custom-btn
                    label="تغيير"
                    icon="mdi-swap-horizontal"
                    variant="tonal"
                    color="primary"
                    density="compact"
                    class="font-weight-bold"
                    :click="() => $refs.imageInput.click()"
                  />
                  <custom-btn
                    type="del"
                    label="حذف"
                    variant="tonal"
                    density="compact"
                    class="font-weight-bold"
                    :click="removeImage"
                  />
                </div>
              </div>

              <!-- Scientific Formula & Question Text Editor -->
              <scientific-formula-editor
                v-model="form.text"
                label="نص السؤال"
                placeholder="اكتب صياغة السؤال هنا... يمكنك النقر على زر (شريط الأدوات والرموز العلمية) بالأعلى لإدراج أي معادلات رياضية أو كيميائية أو كتل برمجية بنقرة واحدة."
                :rows="5"
                class="mb-2"
              />
            </div>

            <v-divider class="my-6 opacity-20" />

            <!-- Dynamic Options: Single / Multiple Choice -->
            <div v-if="form.type === 'single_choice' || form.type === 'multiple_choice'">
              <div class="d-flex align-center justify-space-between mb-4">
                <h3 class="text-h6 mb-0 d-flex align-center gap-2">
                  <v-icon color="success">mdi-format-list-checks</v-icon>
                  خيارات الإجابة
                </h3>
                <v-chip size="small" variant="tonal" color="success" class="font-weight-bold">
                  {{ form.type === 'single_choice' ? 'حدد خيار الإجابة الصحيحة' : 'حدد الإجابات الصحيحة' }}
                </v-chip>
              </div>

              <!-- Unboxed, standard clean option rows without enclosing cards -->
              <div v-for="(option, index) in form.options" :key="index"
                class="d-flex align-center gap-2 mb-3">
                <!-- Selection Radio / Checkbox -->
                <div class="cursor-pointer" @click="toggleCorrectOption(index)">
                  <v-radio-group v-if="form.type === 'single_choice'" v-model="form.correctAnswerIndex" hide-details class="ma-0">
                    <v-radio :value="index" color="success" density="compact" />
                  </v-radio-group>
                  <v-checkbox v-if="form.type === 'multiple_choice'" v-model="form.correctAnswerIndices" :value="index"
                    color="success" hide-details density="compact" class="ma-0" />
                </div>

                <!-- Option Letter Badge (Square with slight radius, NOT circular) -->
                <div class="option-letter-badge font-weight-bold rounded-lg cursor-pointer"
                  :class="isCorrectOption(index) ? 'option-letter--correct' : 'option-letter--default'"
                  title="انقر لتعيين هذا الخيار كإجابة صحيحة"
                  @click="toggleCorrectOption(index)">
                  {{ String.fromCharCode(65 + index) }}
                </div>

                <!-- Input Text Field (Standard clean input) -->
                <div class="flex-grow-1">
                  <custom-text-field
                    v-model="form.options[index]"
                    :placeholder="'اكتب خيار الإجابة (' + String.fromCharCode(65 + index) + ')'"
                    variant="outlined"
                    density="compact"
                    hide-details="auto"
                    :color="isCorrectOption(index) ? 'success' : 'primary'"
                    :rules="[rules.required]"
                  />
                  <!-- Scientific Formula Auto-Preview for Option -->
                  <div
                    v-if="hasScientificMarkup(form.options[index])"
                    class="option-formula-preview mt-1 px-3 py-1 rounded text-caption d-inline-flex align-center gap-2"
                  >
                    <v-icon size="13" color="primary">mdi-variable</v-icon>
                    <span class="text-medium-emphasis">معاينة الرمز:</span>
                    <span class="font-weight-bold" v-html="renderOptionMarkup(form.options[index])"></span>
                  </div>
                </div>

                <!-- Correct Answer Badge -->
                <v-chip v-if="isCorrectOption(index)" size="x-small" color="success" variant="tonal" class="font-weight-bold d-none d-sm-inline-flex">
                  <v-icon start size="12">mdi-check</v-icon>
                  إجابة صحيحة
                </v-chip>

                <!-- Remove Btn -->
                <custom-btn v-if="form.options.length > 2" type="del" isIcon variant="text" density="compact"
                  :click="() => removeOption(index)" title="حذف الخيار" />
              </div>

              <custom-btn type="add" label="إضافة خيار إضافي" class="font-weight-bold mt-2"
                :disabled="form.options.length >= 6" :click="addOption" />

              <v-alert v-if="form.type === 'multiple_choice' && form.correctAnswerIndices.length === 0" type="warning"
                variant="tonal" density="compact" class="mt-4 rounded-xl">
                يرجى تحديد إجابة صحيحة واحدة على الأقل للاختيار المتعدد.
              </v-alert>
            </div>

            <!-- Dynamic Options: True / False -->
            <div v-else-if="form.type === 'true_false'">
              <h3 class="text-h6 mb-4 d-flex align-center gap-2">
                <v-icon color="success">mdi-scale-balance</v-icon>
                حدد الإجابة الصحيحة
              </h3>

              <v-row class="ma-0 gap-4">
                <div class="tf-option-card flex-grow-1 pa-4 rounded-lg text-center cursor-pointer"
                  :class="{ 'tf-option-card--active-true': form.tfCorrect === true }" @click="form.tfCorrect = true">
                  <v-icon size="36" :color="form.tfCorrect === true ? 'success' : 'grey'"
                    class="mb-2">mdi-check-circle</v-icon>
                  <div class="text-h6 font-weight-bold">صواب</div>
                </div>

                <div class="tf-option-card flex-grow-1 pa-4 rounded-lg text-center cursor-pointer"
                  :class="{ 'tf-option-card--active-false': form.tfCorrect === false }" @click="form.tfCorrect = false">
                  <v-icon size="36" :color="form.tfCorrect === false ? 'error' : 'grey'"
                    class="mb-2">mdi-close-circle</v-icon>
                  <div class="text-h6 font-weight-bold">خطأ</div>
                </div>
              </v-row>
            </div>

            <!-- Dynamic Options: Essay -->
            <div v-else-if="form.type === 'essay'">
              <h3 class="text-h6 mb-3 d-flex align-center gap-2">
                <v-icon color="primary">mdi-text-box-check-outline</v-icon>
                الإجابة النموذجية (للمصحح)
              </h3>
              <custom-text-note v-model="form.options[0]" placeholder="اكتب الإجابة النموذجية المعتمدة لتقييم المصحح..."
                rows="4" variant="outlined" density="comfortable" rounded="lg" color="primary" :rules="[rules.required]"
                hide-details="auto" />
            </div>

            <!-- Dynamic Options: Fill Blanks -->
            <div v-else-if="form.type === 'fill_blanks'">
              <h3 class="text-h6 mb-4 d-flex align-center gap-2">
                <v-icon color="deep-purple">mdi-form-textbox</v-icon>
                الكلمات المفقودة (الإجابات)
              </h3>
              <div v-for="(option, index) in form.options" :key="index" class="d-flex align-center gap-3 mb-3">
                <div class="option-letter-badge font-weight-bold rounded-lg option-letter--default" style="width: 36px; height: 36px; min-width: 36px;">
                  {{ index + 1 }}
                </div>
                <div class="flex-grow-1">
                  <custom-text-field v-model="form.options[index]"
                    :placeholder="'الكلمة المفقودة للفراغ (' + (index + 1) + ')'" variant="outlined" density="compact"
                    hide-details="auto" :rules="[rules.required]" />
                </div>
                <custom-btn v-if="form.options.length > 1" type="del" isIcon variant="text" :click="() => removeOption(index)" />
              </div>
              <custom-btn type="add" color="deep-purple" label="إضافة فراغ آخر" class="font-weight-bold mt-2"
                :click="addOption" />
            </div>
          </div>
        </v-col>

        <!-- Right Column: Classification & Attributes Sidebar -->
        <v-col cols="12" lg="4">
          <!-- Academic Classification Card -->
          <div class="main-card pa-6 mb-6 rounded-2xl">
            <div class="d-flex align-center justify-space-between mb-4 flex-wrap gap-2">
              <div class="d-flex align-center gap-2">
                <v-icon color="indigo">mdi-shape</v-icon>
                <h3 class="text-h6 mb-0">التصنيف والربط الأكاديمي</h3>
              </div>
            </div>

            <!-- Academic fields container -->
            <div v-if="isLoadingQuestion" class="d-flex flex-column align-center justify-center py-10">
              <v-progress-circular indeterminate color="primary" size="36" class="mb-3" />
              <span class="text-caption font-weight-bold text-medium-emphasis">جاري تحميل التصنيف الأكاديمي...</span>
            </div>
            <div v-else>
              <!-- Institution Type Selector (مدارس / جامعات) -->
              <div class="mb-4">
                <v-btn-toggle
                  v-model="form.institution_type"
                  mandatory
                  color="primary"
                  variant="outlined"
                  density="compact"
                  rounded="lg"
                  class="w-100 d-flex"
                  @update:model-value="onInstitutionTypeToggle"
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
                    <v-icon start size="16">mdi-tools</v-icon>
                    مهني / معاهد
                  </v-btn>
                </v-btn-toggle>
              </div>

              <!-- 🏫 School Academic Classification Fields -->
              <template v-if="form.institution_type === 'school'">
                <!-- Stage -->
                <auto-list
                  v-model="form.stageId"
                  name="Stage"
                  placeholder="المرحلة الدراسية"
                  cols="12"
                  :add="false"
                  @update:model-value="onStageChange"
                />

                <!-- ClassTrack (الصف والمسار) -->
                <auto-list
                  v-model="form.classTrackId"
                  name="ClassTrackByStage"
                  :param="form.stageId"
                  placeholder="الصف والمسار"
                  cols="12"
                  :add="false"
                  :disabled="!form.stageId"
                  @update:model-value="onClassTrackChange"
                />

                <!-- Subject -->
                <auto-list
                  v-model="form.subjectId"
                  name="Subject"
                  :param="form.classTrackId || form.stageId"
                  placeholder="المادة الدراسية"
                  cols="12"
                  :add="false"
                  :disabled="!form.classTrackId && !form.stageId"
                  @update:model-value="onSubjectChange"
                />

                <!-- Semester -->
                <auto-list
                  v-model="form.semesterId"
                  name="Semester"
                  placeholder="الفصل الدراسي"
                  cols="12"
                  :add="false"
                />
              </template>

              <!-- 🎓 University Academic Classification Fields -->
              <template v-if="form.institution_type === 'university'">
                <!-- College -->
                <auto-list
                  v-model="form.collegeId"
                  name="College"
                  placeholder="الكلية الجامعية"
                  cols="12"
                  :add="false"
                  @update:model-value="onCollegeChange"
                />

                <!-- Department -->
                <auto-list
                  v-model="form.departmentId"
                  name="DepartmentByCollege"
                  :param="form.collegeId"
                  placeholder="القسم الأكاديمي"
                  cols="12"
                  :add="false"
                  :disabled="!form.collegeId"
                  @update:model-value="onDepartmentChange"
                />

                <!-- Specialization -->
                <auto-list
                  v-model="form.specializationId"
                  name="Specialization"
                  :param="form.departmentId"
                  placeholder="التخصص والبرنامج"
                  cols="12"
                  :add="false"
                  :disabled="!form.departmentId"
                  @update:model-value="onSpecializationChange"
                />

                <!-- SemesterSubject (مقرر الفصل الجامعي) -->
                <auto-list
                  v-model="form.semesterSubjectId"
                  name="SemesterSubject"
                  :param="form.specializationId"
                  placeholder="مقرر الفصل الجامعي"
                  cols="12"
                  :add="false"
                  @update:model-value="onSemesterSubjectChange"
                />
              </template>

              <!-- 🏢 Institute Academic Classification Fields -->
              <template v-if="form.institution_type === 'institute'">
                <!-- Field (المجال المهني) -->
                <auto-list
                  v-model="form.instituteFieldId"
                  name="InstituteField"
                  placeholder="المجال المهني / التقني"
                  cols="12"
                  :add="false"
                  @update:model-value="onInstituteFieldChange"
                />

                <!-- Education System (نظام التعليم) -->
                <auto-list
                  v-model="form.instituteEducationSystemId"
                  name="InstituteEducationSystem"
                  :param="form.instituteFieldId"
                  placeholder="نظام التعليم والتدريب"
                  cols="12"
                  :add="false"
                  :disabled="!form.instituteFieldId"
                  @update:model-value="onInstituteEducationSystemChange"
                />

                <!-- Specialization (التخصص) -->
                <auto-list
                  v-model="form.instituteSpecializationId"
                  name="InstituteSpecialization"
                  :param="{ field: form.instituteFieldId, education_system: form.instituteEducationSystemId }"
                  placeholder="التخصص المهني"
                  cols="12"
                  :add="false"
                  :disabled="!form.instituteEducationSystemId"
                  @update:model-value="onInstituteSpecializationChange"
                />

                <!-- Curriculum (الخطة الدراسية) -->
                <auto-list
                  v-model="form.instituteCurriculumId"
                  name="InstituteCurriculum"
                  :param="form.instituteSpecializationId"
                  placeholder="الخطة الدراسية للمعهد"
                  cols="12"
                  :add="false"
                  :disabled="!form.instituteSpecializationId"
                />

                <!-- Subject (المادة الدراسية للمعهد) -->
                <auto-list
                  v-model="form.instituteSubjectId"
                  name="InstituteSubject"
                  :param="{ field: form.instituteFieldId }"
                  placeholder="المادة الدراسية للمعهد"
                  cols="12"
                  :add="false"
                  @update:model-value="onInstituteSubjectChange"
                />
              </template>

              <!-- 🎯 Common: Unit, Lesson, Learning Outcome -->
              <!-- Unit -->
              <auto-list
                v-model="form.unitId"
                name="UnitBySubject"
                :param="form.institution_type === 'university' ? { semester_subject: form.semesterSubjectId } : (form.institution_type === 'institute' ? { subject: form.instituteSubjectId } : { subject: form.subjectId })"
                :placeholder="form.institution_type === 'university' ? 'مفردة / موضوع المقرر' : (form.institution_type === 'institute' ? 'الوحدة / التدريب العملي' : 'الوحدة الدراسية')"
                cols="12"
                :add="false"
                :disabled="form.institution_type === 'university' ? !form.semesterSubjectId : (form.institution_type === 'institute' ? !form.instituteSubjectId : !form.subjectId)"
                @update:model-value="onUnitChange"
              />

              <!-- Lesson -->
              <auto-list
                v-model="form.lessonId"
                name="LessonByUnit"
                :param="form.unitId"
                :placeholder="form.institution_type === 'university' ? 'المحاضرة / الدرس الأكاديمي' : (form.institution_type === 'institute' ? 'التدريب / الدرس المهني' : 'الدرس المدرسي')"
                cols="12"
                :add="false"
                :disabled="!form.unitId"
              />

              <!-- Learning Outcome -->
              <auto-list
                v-model="form.learningOutcomeId"
                name="LearningOutcome"
                :param="form.unitId"
                :placeholder="form.institution_type === 'university' ? 'مخرج تعلم المقرر (CLO)' : 'مخرج التعلم المستهدف (اختياري)'"
                cols="12"
                :add="false"
                :disabled="!form.unitId"
              />
            </div>
          </div>

          <!-- Question Attributes Card -->
          <div class="main-card pa-6 mb-6 rounded-2xl">
            <div class="d-flex align-center gap-2 mb-4">
              <v-icon color="warning">mdi-speedometer</v-icon>
              <h3 class="text-h6 ">خصائص ومواصفات السؤال</h3>
            </div>

            <!-- Default Score -->
            <div class="mb-4">
              <label class="text-caption font-weight-bold text-medium-emphasis mb-1 d-block">درجة السؤال
                المستحقة</label>
              <custom-text-field v-model.number="form.defaultScore" type="number" min="1" icon="star-circle-outline"
                variant="outlined" density="compact" hide-details="auto"
                :rules="[rules.required, rules.positive]" />
            </div>

            <!-- Expected Time -->
            <div class="mb-5">
              <label class="text-caption font-weight-bold text-medium-emphasis mb-1 d-block">الزمن المتوقع للحل
                (بالدقائق)</label>
              <custom-text-field v-model.number="form.expectedTimeMinutes" type="number" min="1" icon="clock-outline"
                variant="outlined" density="compact" hide-details="auto"
                :rules="[rules.required, rules.positive]" />
            </div>

            <!-- Difficulty Toggle -->
            <div class="mb-5">
              <label class="text-caption font-weight-bold text-medium-emphasis mb-2 d-block">مستوى الصعوبة</label>
              <div class="segmented-control w-100 pa-1 d-flex gap-1">
                <button type="button" class="flex-grow-1 d-flex align-center justify-center gap-1 font-weight-bold" :class="{ active: form.difficulty === 1 }"
                  @click="form.difficulty = 1">
                  <v-icon size="18" color="success">mdi-gauge-low</v-icon>
                  <span>سهل</span>
                </button>
                <button type="button" class="flex-grow-1 d-flex align-center justify-center gap-1 font-weight-bold" :class="{ active: form.difficulty === 2 }"
                  @click="form.difficulty = 2">
                  <v-icon size="18" color="warning">mdi-gauge</v-icon>
                  <span>متوسط</span>
                </button>
                <button type="button" class="flex-grow-1 d-flex align-center justify-center gap-1 font-weight-bold" :class="{ active: form.difficulty === 3 }"
                  @click="form.difficulty = 3">
                  <v-icon size="18" color="error">mdi-gauge-full</v-icon>
                  <span>صعب</span>
                </button>
              </div>
            </div>

            <!-- Bloom Level -->
            <div>
              <label class="text-caption font-weight-bold text-medium-emphasis mb-2 d-block">مستوى بلوم المعرفي</label>
              <v-chip-group v-model="form.bloomLevel" mandatory class="flex-wrap">
                <v-chip v-for="level in bloomLevels" :key="level.value" :value="level.value" filter variant="outlined"
                  class="font-weight-bold" active-class="bg-primary text-white border-0">
                  {{ level.text }}
                </v-chip>
              </v-chip-group>
            </div>
          </div>

          <!-- Actions Card -->
          <div class="main-card pa-6 rounded-2xl sticky-action-card">
            <custom-btn type="add" :label="isEditMode ? 'حفظ التعديلات' : 'إرسال السؤال للمراجعة'"
              :icon="isEditMode ? 'mdi-check-circle' : 'mdi-send'" color="primary"
              class="font-weight-bold mb-3 w-100" :loading="saving" :click="() => submitQuestion(isEditMode ? form.status || 'قيد المراجعة' : 'قيد المراجعة')" />

            <custom-btn v-if="!isEditMode" type="save" label="حفظ كمسودة" icon="mdi-content-save-outline" color="secondary" variant="tonal"
              class="font-weight-bold w-100" :disabled="saving" :click="() => submitQuestion('مسودة')" />
          </div>
        </v-col>
      </v-row>
    </v-form>

    <!-- Dialog for Image Preview -->
    <v-dialog v-model="previewImageDialog" max-width="650">
      <v-card class="pa-4 rounded-2xl">
        <div class="d-flex justify-space-between align-center mb-3">
          <div class="font-weight-bold text-subtitle-1 d-flex align-center gap-2">
            <v-icon color="primary" size="20">mdi-image-outline</v-icon>
            معاينة الصورة المساعدة
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" @click="previewImageDialog = false" />
        </div>
        <div class="d-flex justify-center align-center pa-2 rounded-xl overflow-hidden" style="background: rgba(var(--v-theme-surface-variant), 0.3);">
          <img :src="form.image" alt="الصورة المساعدة" style="max-height: 480px; max-width: 100%; object-fit: contain; border-radius: 8px;" />
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import api from "@/services/api";
import { bankService } from "@/services/bankService";
import ScientificFormulaEditor from "@/components/common/ScientificFormulaEditor.vue";
import { parseScientificMarkup, ensureKaTeXLoaded } from "@/utils/scientificRenderer";

export default {
  name: "QuestionNewView",

  components: {
    ScientificFormulaEditor,
  },

  data() {
    return {
      saving: false,
      isLoadingQuestion: false,
      isEditMode: false,
      editId: null,
      previewImageDialog: false,

      // Tracking variables to prevent cascading resets during mount/edit
      _lastCollegeId: null,
      _lastDepartmentId: null,
      _lastSpecializationId: null,
      _lastSemesterSubjectId: null,
      _lastStageId: null,
      _lastClassTrackId: null,
      _lastSubjectId: null,
      _lastUnitId: null,

      // State snapshots to preserve selections across toggling between school and university
      schoolState: {
        stageId: null,
        classTrackId: null,
        subjectId: null,
        semesterId: null,
        unitId: null,
        lessonId: null,
        learningOutcomeId: null,
      },
      universityState: {
        collegeId: null,
        departmentId: null,
        specializationId: null,
        semesterSubjectId: null,
        unitId: null,
        lessonId: null,
        learningOutcomeId: null,
      },
      instituteState: {
        instituteFieldId: null,
        instituteEducationSystemId: null,
        instituteSpecializationId: null,
        instituteCurriculumId: null,
        instituteSubjectId: null,
        unitId: null,
        lessonId: null,
        learningOutcomeId: null,
      },

      // Form
      form: {
        text: "",
        type: "single_choice",
        institution_type: "school",
        // School Relations
        stageId: null,
        classTrackId: null,
        subjectId: null,
        semesterId: null,
        // University Relations
        collegeId: null,
        departmentId: null,
        specializationId: null,
        semesterSubjectId: null,
        // Institute Relations
        instituteFieldId: null,
        instituteEducationSystemId: null,
        instituteSpecializationId: null,
        instituteCurriculumId: null,
        instituteSubjectId: null,
        // Common Relations
        unitId: null,
        lessonId: null,
        learningOutcomeId: null,
        difficulty: 2,
        bloomLevel: "تطبيق",
        options: ["", "", "", ""],
        correctAnswerIndex: 0,
        correctAnswerIndices: [],
        tfCorrect: true,
        image: "",
        defaultScore: 1,
        expectedTimeMinutes: 1,
      },

      // Definitions
      questionTypeOptions: [
        { value: "single_choice", label: "اختيار مفرد", color: "indigo", icon: "mdi-record-circle-outline", iconActive: "mdi-record-circle" },
        { value: "multiple_choice", label: "اختيار متعدد", color: "warning", icon: "mdi-checkbox-multiple-blank-outline", iconActive: "mdi-checkbox-multiple-marked" },
        { value: "true_false", label: "صواب / خطأ", color: "success", icon: "mdi-toggle-switch-off-outline", iconActive: "mdi-toggle-switch" },
        { value: "essay", label: "مقالي", color: "primary", icon: "mdi-text-box-edit-outline", iconActive: "mdi-text-box-edit" },
        { value: "fill_blanks", label: "فراغات", color: "deep-purple", icon: "mdi-form-textbox", iconActive: "mdi-form-textbox" },
      ],
      bloomLevels: [
        { text: "تذكر", value: "تذكر" },
        { text: "فهم", value: "فهم" },
        { text: "تطبيق", value: "تطبيق" },
        { text: "تحليل", value: "تحليل" },
        { text: "تقييم", value: "تقييم" },
        { text: "ابتكار", value: "ابتكار" },
      ],
      rules: {
        required: (v) => !!v || v === 0 || "هذا الحقل مطلوب",
        positive: (v) => (v && v > 0) || "يجب أن تكون القيمة أكبر من صفر",
      },
    };
  },

  async created() {
    if (this.$route.query.id) {
      this.isLoadingQuestion = true;
      this.isEditMode = true;
      this.editId = this.$route.query.id;
      await this.loadQuestionForEdit(this.editId);
    }
  },

  mounted() {
    ensureKaTeXLoaded();
  },

  methods: {
    hasScientificMarkup(text) {
      if (!text || typeof text !== 'string') return false;
      return text.includes('$') || text.includes('\\') || /([A-Za-z]\^[0-9]|[A-Za-z]_[0-9]|->|⇌)/.test(text);
    },

    renderOptionMarkup(text) {
      return parseScientificMarkup(text);
    },

    // === EDIT MODE LOADER ===
    async loadQuestionForEdit(id) {
      this.saving = true;
      try {
        const data = await bankService.getQuestionDetails(id);
        const q = data?.data || data;

        // Debug: log raw API response for university fields
        console.log('Raw API response:', {
          institution_type: q.institution_type,
          college_id: q.college_id,
          department_id: q.department_id,
          specialization_id: q.specialization_id,
          semester_subject_id: q.semester_subject_id,
          unit_id: q.unit_id, fk_unit: q.fk_unit,
          lesson: q.lesson, subject_id: q.subject_id, fk_subject: q.fk_subject,
        });

        this.form.text = q.content || "";
        this.form.difficulty = q.difficulty || 2;
        this.form.bloomLevel = q.bloomLevel || "تطبيق";
        this.form.defaultScore = q.defaultMark || 1;
        this.form.expectedTimeMinutes = q.expected_time_minutes || 1;
        this.form.image = q.image || "";

        // Reverse map question type
        const typeMap = {
          'Single Choice': 'single_choice',
          'Multiple Choice': 'multiple_choice',
          'True/False': 'true_false',
          'Essay': 'essay',
          'Fill in the Blanks': 'fill_blanks',
        };
        this.form.type = typeMap[q.questionType] || 'single_choice';

        // Academic Relations & Hierarchy
        if (q.institution_type === 'institute') {
          this.form.institution_type = 'institute';
        } else if (q.semester_subject_id || q.college_id) {
          this.form.institution_type = 'university';
        } else if (q.stage_id || q.class_track_id) {
          this.form.institution_type = 'school';
        } else {
          this.form.institution_type = q.institution_type || 'school';
        }

        if (this.form.institution_type === 'school') {
          this.form.stageId = q.stage_id ? Number(q.stage_id) : null;
          this.form.classTrackId = q.class_track_id ? Number(q.class_track_id) : null;
          this.form.subjectId = (q.subject_id || q.fk_subject) ? Number(q.subject_id || q.fk_subject) : null;
        } else if (this.form.institution_type === 'institute') {
          this.form.instituteFieldId = q.institute_field_id ? Number(q.institute_field_id) : null;
          this.form.instituteEducationSystemId = q.institute_education_system_id ? Number(q.institute_education_system_id) : null;
          this.form.instituteSpecializationId = q.institute_specialization_id ? Number(q.institute_specialization_id) : null;
          this.form.instituteSubjectId = (q.institute_subject_id || q.subject_id || q.fk_subject) ? Number(q.institute_subject_id || q.subject_id || q.fk_subject) : null;
          this.form.subjectId = this.form.instituteSubjectId;
        } else {
          this.form.collegeId = q.college_id ? Number(q.college_id) : null;
          this.form.departmentId = q.department_id ? Number(q.department_id) : null;
          this.form.specializationId = q.specialization_id ? Number(q.specialization_id) : null;
          this.form.semesterSubjectId = q.semester_subject_id ? Number(q.semester_subject_id) : null;
          this.form.subjectId = (q.subject_id || q.fk_subject) ? Number(q.subject_id || q.fk_subject) : null;
        }
        this.form.unitId = (q.unit_id || q.fk_unit) ? Number(q.unit_id || q.fk_unit) : null;
        this.form.lessonId = q.lesson ? Number(q.lesson) : null;
        this.form.learningOutcomeId = (q.learningOutcome || q.learning_outcome_id) ? Number(q.learningOutcome || q.learning_outcome_id) : null;

        if (this.form.institution_type === 'school') {
          this.schoolState = {
            stageId: this.form.stageId,
            classTrackId: this.form.classTrackId,
            subjectId: this.form.subjectId,
            semesterId: this.form.semesterId,
            unitId: this.form.unitId,
            lessonId: this.form.lessonId,
            learningOutcomeId: this.form.learningOutcomeId,
          };
        } else if (this.form.institution_type === 'institute') {
          this.instituteState = {
            instituteFieldId: this.form.instituteFieldId,
            instituteEducationSystemId: this.form.instituteEducationSystemId,
            instituteSpecializationId: this.form.instituteSpecializationId,
            instituteCurriculumId: this.form.instituteCurriculumId,
            instituteSubjectId: this.form.instituteSubjectId,
            unitId: this.form.unitId,
            lessonId: this.form.lessonId,
            learningOutcomeId: this.form.learningOutcomeId,
          };
        } else {
          this.universityState = {
            collegeId: this.form.collegeId,
            departmentId: this.form.departmentId,
            specializationId: this.form.specializationId,
            semesterSubjectId: this.form.semesterSubjectId,
            unitId: this.form.unitId,
            lessonId: this.form.lessonId,
            learningOutcomeId: this.form.learningOutcomeId,
          };
        }

        this._currentActiveType = this.form.institution_type;

        // Initialize change-tracking guards to prevent AutoList from wiping values during initial render
        this._lastCollegeId = this.form.collegeId;
        this._lastDepartmentId = this.form.departmentId;
        this._lastSpecializationId = this.form.specializationId;
        this._lastSemesterSubjectId = this.form.semesterSubjectId;
        this._lastStageId = this.form.stageId;
        this._lastClassTrackId = this.form.classTrackId;
        this._lastSubjectId = this.form.subjectId;
        this._lastUnitId = this.form.unitId;

        // Options / Answers
        const answers = q.answers || q.options || [];
        if (answers.length > 0) {
          if (this.form.type === "single_choice") {
            this.form.options = answers.map((a) => a.text || "");
            const correctIdx = answers.findIndex((a) => a.isTrue);
            this.form.correctAnswerIndex = correctIdx >= 0 ? correctIdx : 0;
          } else if (this.form.type === "multiple_choice") {
            this.form.options = answers.map((a) => a.text || "");
            this.form.correctAnswerIndices = answers
              .map((a, idx) => (a.isTrue ? idx : null))
              .filter((idx) => idx !== null);
          } else if (this.form.type === "true_false") {
            const trueAns = answers.find((a) => a.text === "صواب" || a.text === "True");
            this.form.tfCorrect = trueAns ? trueAns.isTrue : true;
          } else if (this.form.type === "essay") {
            this.form.options = [answers[0]?.text || ""];
          } else if (this.form.type === "fill_blanks") {
            this.form.options = answers.map((a) => a.text || "");
          }
        }
        // Debug: log received academic IDs
        console.log('📋 Edit data received:', {
          institution_type: this.form.institution_type,
          collegeId: this.form.collegeId,
          departmentId: this.form.departmentId,
          specializationId: this.form.specializationId,
          semesterSubjectId: this.form.semesterSubjectId,
          unitId: this.form.unitId,
          lessonId: this.form.lessonId,
        });
      } catch (err) {
        console.error("فشل في تحميل بيانات السؤال للتعديل:", err);
      } finally {
        this.saving = false;
        setTimeout(() => {
          this.isLoadingQuestion = false;
        }, 150);
      }
    },

    onInstitutionTypeToggle(newType) {
      if (this.isLoadingQuestion) return;
      const targetType = newType || this.form.institution_type;

      // 1. Cache current state based on previous active type
      const currentType = this._currentActiveType || 'school';
      if (currentType === 'university') {
        this.universityState = {
          collegeId: this.form.collegeId,
          departmentId: this.form.departmentId,
          specializationId: this.form.specializationId,
          semesterSubjectId: this.form.semesterSubjectId,
          unitId: this.form.unitId,
          lessonId: this.form.lessonId,
          learningOutcomeId: this.form.learningOutcomeId,
        };
      } else if (currentType === 'institute') {
        this.instituteState = {
          instituteFieldId: this.form.instituteFieldId,
          instituteEducationSystemId: this.form.instituteEducationSystemId,
          instituteSpecializationId: this.form.instituteSpecializationId,
          instituteCurriculumId: this.form.instituteCurriculumId,
          instituteSubjectId: this.form.instituteSubjectId,
          unitId: this.form.unitId,
          lessonId: this.form.lessonId,
          learningOutcomeId: this.form.learningOutcomeId,
        };
      } else {
        this.schoolState = {
          stageId: this.form.stageId,
          classTrackId: this.form.classTrackId,
          subjectId: this.form.subjectId,
          semesterId: this.form.semesterId,
          unitId: this.form.unitId,
          lessonId: this.form.lessonId,
          learningOutcomeId: this.form.learningOutcomeId,
        };
      }

      this._currentActiveType = targetType;

      // 2. Restore saved selections for targetType
      if (targetType === 'university') {
        this.form.collegeId = this.universityState.collegeId;
        this.form.departmentId = this.universityState.departmentId;
        this.form.specializationId = this.universityState.specializationId;
        this.form.semesterSubjectId = this.universityState.semesterSubjectId;
        this.form.unitId = this.universityState.unitId;
        this.form.lessonId = this.universityState.lessonId;
        this.form.learningOutcomeId = this.universityState.learningOutcomeId;

        this._lastCollegeId = this.form.collegeId;
        this._lastDepartmentId = this.form.departmentId;
        this._lastSpecializationId = this.form.specializationId;
        this._lastSemesterSubjectId = this.form.semesterSubjectId;
        this._lastUnitId = this.form.unitId;
      } else if (targetType === 'institute') {
        this.form.instituteFieldId = this.instituteState.instituteFieldId;
        this.form.instituteEducationSystemId = this.instituteState.instituteEducationSystemId;
        this.form.instituteSpecializationId = this.instituteState.instituteSpecializationId;
        this.form.instituteCurriculumId = this.instituteState.instituteCurriculumId;
        this.form.instituteSubjectId = this.instituteState.instituteSubjectId;
        this.form.subjectId = this.instituteState.instituteSubjectId;
        this.form.unitId = this.instituteState.unitId;
        this.form.lessonId = this.instituteState.lessonId;
        this.form.learningOutcomeId = this.instituteState.learningOutcomeId;

        this._lastUnitId = this.form.unitId;
      } else {
        this.form.stageId = this.schoolState.stageId;
        this.form.classTrackId = this.schoolState.classTrackId;
        this.form.subjectId = this.schoolState.subjectId;
        this.form.semesterId = this.schoolState.semesterId;
        this.form.unitId = this.schoolState.unitId;
        this.form.lessonId = this.schoolState.lessonId;
        this.form.learningOutcomeId = this.schoolState.learningOutcomeId;

        this._lastStageId = this.form.stageId;
        this._lastClassTrackId = this.form.classTrackId;
        this._lastSubjectId = this.form.subjectId;
        this._lastUnitId = this.form.unitId;
      }
    },

    onInstituteFieldChange(val) {
      if (this.isLoadingQuestion) return;
      this.form.instituteEducationSystemId = null;
      this.form.instituteSpecializationId = null;
      this.form.instituteCurriculumId = null;
      this.form.instituteSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onInstituteEducationSystemChange(val) {
      if (this.isLoadingQuestion) return;
      this.form.instituteSpecializationId = null;
      this.form.instituteCurriculumId = null;
    },

    onInstituteSpecializationChange(val) {
      if (this.isLoadingQuestion) return;
      this.form.instituteCurriculumId = null;
    },

    onInstituteSubjectChange(val) {
      if (this.isLoadingQuestion) return;
      this.form.subjectId = val;
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onStageChange(val) {
      if (this.isLoadingQuestion) return;
      if (val === this._lastStageId) return;
      this._lastStageId = val;
      this.form.classTrackId = null;
      this.form.subjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onClassTrackChange(val) {
      if (this.isLoadingQuestion) return;
      if (val === this._lastClassTrackId) return;
      this._lastClassTrackId = val;
      this.form.subjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onSubjectChange(val) {
      if (this.isLoadingQuestion) return;
      if (val === this._lastSubjectId) return;
      this._lastSubjectId = val;
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onCollegeChange(val) {
      if (this.isLoadingQuestion) return;
      if (val === this._lastCollegeId) return;
      this._lastCollegeId = val;
      this.form.departmentId = null;
      this.form.specializationId = null;
      this.form.semesterSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onDepartmentChange(val) {
      if (this.isLoadingQuestion) return;
      if (val === this._lastDepartmentId) return;
      this._lastDepartmentId = val;
      this.form.specializationId = null;
      this.form.semesterSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onSpecializationChange(val) {
      if (this.isLoadingQuestion) return;
      if (val === this._lastSpecializationId) return;
      this._lastSpecializationId = val;
      this.form.semesterSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onSemesterSubjectChange(val) {
      if (this.isLoadingQuestion) return;
      if (val === this._lastSemesterSubjectId) return;
      this._lastSemesterSubjectId = val;
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onUnitChange(val) {
      if (this.isLoadingQuestion) return;
      if (val === this._lastUnitId) return;
      this._lastUnitId = val;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },


    // === OPTIONS ===
    addOption() {
      if (this.form.options.length < 6) {
        this.form.options.push("");
      }
    },

    removeOption(index) {
      this.form.options.splice(index, 1);
      if (this.form.type === "single_choice") {
        if (this.form.correctAnswerIndex >= index && this.form.correctAnswerIndex > 0) {
          this.form.correctAnswerIndex--;
        }
      } else {
        this.form.correctAnswerIndices = this.form.correctAnswerIndices
          .filter((i) => i !== index)
          .map((i) => (i > index ? i - 1 : i));
      }
    },

    isCorrectOption(index) {
      if (this.form.type === "single_choice") return this.form.correctAnswerIndex === index;
      if (this.form.type === "multiple_choice") return this.form.correctAnswerIndices.includes(index);
      return false;
    },

    toggleCorrectOption(index) {
      if (this.form.type === "single_choice") {
        this.form.correctAnswerIndex = index;
      } else if (this.form.type === "multiple_choice") {
        const i = this.form.correctAnswerIndices.indexOf(index);
        if (i > -1) {
          this.form.correctAnswerIndices.splice(i, 1);
        } else {
          this.form.correctAnswerIndices.push(index);
        }
      }
    },

    // === IMAGE ===
    onImageSelected(event) {
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (e) => { this.form.image = e.target.result; };
      reader.readAsDataURL(file);
    },

    removeImage(event) {
      if (event) event.stopPropagation();
      this.form.image = "";
      if (this.$refs.imageInput) this.$refs.imageInput.value = null;
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

    // === SUBMIT (ATOMIC SINGLE REQUEST) ===
    async submitQuestion(status = "مسودة") {
      const { valid } = await this.$refs.formRef.validate();
      if (!valid) return;

      if (this.form.type === "multiple_choice" && this.form.correctAnswerIndices.length === 0) {
        this.$alert("errorData", { message: "يجب اختيار إجابة صحيحة واحدة على الأقل للاختيار المتعدد" });
        return;
      }

      // Format Options Payload Atomically
      const optionsPayload = [];
      if (this.form.type === "single_choice" || this.form.type === "multiple_choice") {
        this.form.options.forEach((text, i) => {
          optionsPayload.push({
            text: text,
            isTrue: this.form.type === "single_choice" ? i === this.form.correctAnswerIndex : this.form.correctAnswerIndices.includes(i),
            order: i + 1,
          });
        });
      } else if (this.form.type === "true_false") {
        optionsPayload.push({ text: "صواب", isTrue: this.form.tfCorrect === true, order: 1 });
        optionsPayload.push({ text: "خطأ", isTrue: this.form.tfCorrect === false, order: 2 });
      } else if (this.form.type === "essay") {
        optionsPayload.push({ text: this.form.options[0] || "", isTrue: true, order: 1 });
      } else if (this.form.type === "fill_blanks") {
        this.form.options.forEach((text, i) => {
          optionsPayload.push({ text: text, isTrue: true, order: i + 1 });
        });
      }

      this.saving = true;
      try {
        // Pre-save anti-duplicate similarity check
        if (this.form.lessonId && this.form.text) {
          const simRes = await bankService.checkQuestionSimilarity({
            content: this.form.text,
            lesson_id: this.form.lessonId,
            exclude_id: this.isEditMode ? this.editId : null,
            threshold: 0.80
          });

          if (simRes && simRes.is_duplicate) {
            const topMatch = simRes.matched_questions?.[0];
            const msg = `تنبيه: هذا السؤال متشابه بنسبة (${simRes.max_similarity}%) مع سؤال موجود مسبقاً في نفس الدرس (سؤال #${topMatch?.id}). يرجى تعديل الصياغة لتجنب التكرار.`;
            this.$alert("errorData", { message: msg, title: "تم اكتشاف تطابق/تكرار" });
            this.saving = false;
            return;
          }
        }

        const questionPayload = {
          content: this.form.text,
          questionType: this.mapQuestionType(this.form.type),
          status: status,
          institution_type: this.form.institution_type || 'school',
          lesson: this.form.lessonId,
          learningOutcome: this.form.learningOutcomeId || null,
          difficulty: this.form.difficulty,
          bloomLevel: this.form.bloomLevel,
          defaultMark: this.form.defaultScore,
          expected_time_minutes: this.form.expectedTimeMinutes,
          image: this.form.image || null,
          options: optionsPayload,
        };

        if (this.isEditMode) {
          await bankService.updateQuestion(this.editId, questionPayload);
          this.$alert("success", { message: "تم تحديث السؤال وخياراته بنجاح" });
          this.$navigateTo({ name: "question-bank", blank: false });
        } else {
          await bankService.createQuestion(questionPayload);
          this.$alert("success", { message: `تم حفظ السؤال بنجاح كـ ${status}` });
          // Stay on the same screen: Reset question text and answers, keeping academic classification intact for fast entry
          this.form.text = "";
          this.form.options = ["", "", "", ""];
          this.form.correctAnswerIndex = 0;
          this.form.correctAnswerIndices = [];
          this.form.tfCorrect = true;
          this.form.image = "";
          if (this.$refs.imageInput) this.$refs.imageInput.value = null;
          this.$refs.formRef?.resetValidation?.();
        }
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء محاولة حفظ السؤال" });
        console.error(err);
      } finally {
        this.saving = false;
      }
    },
  },
};
</script>

<style scoped>
.qb-new-page-v4 {
  color: rgb(var(--v-theme-on-surface));
}

/* ===== Main Cards ===== */
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.08);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 4px 12px rgba(0, 0, 0, 0.02);
  transition: box-shadow 0.3s ease;
}

.main-card:hover {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05), 0 8px 24px rgba(0, 0, 0, 0.03);
}

/* ===== Type Selector Grid ===== */
.type-selector-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}

.type-option-card {
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  border-radius: 16px !important;
}

.type-option-card:hover {
  transform: translateY(-3px);
}

/* Individual Type Colors (Before Selection) */
.type-card-indigo {
  background: rgba(99, 102, 241, 0.06) !important;
  border: 1.5px solid rgba(99, 102, 241, 0.3) !important;
}
.type-card-indigo:hover {
  background: rgba(99, 102, 241, 0.12) !important;
  border-color: rgba(99, 102, 241, 0.6) !important;
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.15) !important;
}

.type-card-warning {
  background: rgba(245, 158, 11, 0.08) !important;
  border: 1.5px solid rgba(245, 158, 11, 0.3) !important;
}
.type-card-warning:hover {
  background: rgba(245, 158, 11, 0.14) !important;
  border-color: rgba(245, 158, 11, 0.6) !important;
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.15) !important;
}

.type-card-success {
  background: rgba(16, 185, 129, 0.06) !important;
  border: 1.5px solid rgba(16, 185, 129, 0.3) !important;
}
.type-card-success:hover {
  background: rgba(16, 185, 129, 0.12) !important;
  border-color: rgba(16, 185, 129, 0.6) !important;
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.15) !important;
}

.type-card-primary {
  background: rgba(14, 165, 233, 0.06) !important;
  border: 1.5px solid rgba(14, 165, 233, 0.3) !important;
}
.type-card-primary:hover {
  background: rgba(14, 165, 233, 0.12) !important;
  border-color: rgba(14, 165, 233, 0.6) !important;
  box-shadow: 0 6px 20px rgba(14, 165, 233, 0.15) !important;
}

.type-card-deep-purple {
  background: rgba(139, 92, 246, 0.06) !important;
  border: 1.5px solid rgba(139, 92, 246, 0.3) !important;
}
.type-card-deep-purple:hover {
  background: rgba(139, 92, 246, 0.12) !important;
  border-color: rgba(139, 92, 246, 0.6) !important;
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.15) !important;
}

/* Active State Gradients (When Selected) */
.type-card-indigo.type-option-card--active {
  background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
  border-color: #4338ca !important;
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3) !important;
  transform: translateY(-3px);
}

.type-card-warning.type-option-card--active {
  background: linear-gradient(135deg, #f59e0b, #d97706) !important;
  border-color: #b45309 !important;
  box-shadow: 0 8px 24px rgba(245, 158, 11, 0.3) !important;
  transform: translateY(-3px);
}

.type-card-success.type-option-card--active {
  background: linear-gradient(135deg, #10b981, #059669) !important;
  border-color: #047857 !important;
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3) !important;
  transform: translateY(-3px);
}

.type-card-primary.type-option-card--active {
  background: linear-gradient(135deg, #0284c7, #0369a1) !important;
  border-color: #075985 !important;
  box-shadow: 0 8px 24px rgba(2, 132, 199, 0.3) !important;
  transform: translateY(-3px);
}

.type-card-deep-purple.type-option-card--active {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important;
  border-color: #6d28d9 !important;
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.3) !important;
  transform: translateY(-3px);
}


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

/* ===== True/False Cards ===== */
.tf-option-card {
  background: rgb(var(--v-theme-background));
  border: 1.5px solid rgba(var(--v-border-color), 0.12);
  border-radius: 8px !important; /* Standard non-circular rounded-lg */
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.tf-option-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
  border-color: rgba(var(--v-border-color), 0.25);
}

.tf-option-card--active-true {
  background: rgba(var(--v-theme-success), 0.06) !important;
  border-color: rgb(var(--v-theme-success)) !important;
  box-shadow: 0 4px 16px rgba(var(--v-theme-success), 0.15) !important;
  transform: translateY(-2px);
}

.tf-option-card--active-false {
  background: rgba(var(--v-theme-error), 0.06) !important;
  border-color: rgb(var(--v-theme-error)) !important;
  box-shadow: 0 4px 16px rgba(var(--v-theme-error), 0.15) !important;
  transform: translateY(-2px);
}

/* ===== Segmented Control ===== */
.segmented-control {
  display: flex;
  background: rgb(var(--v-theme-background));
  padding: 3px;
  border-radius: 12px;
  gap: 2px;
  border: 1px solid rgba(var(--v-border-color), 0.08);
}

.segmented-control button {
  border: none;
  background: transparent;
  padding: 8px 14px;
  font-size: 0.85rem;
  color: rgba(var(--v-theme-on-surface), 0.55);
  border-radius: 9px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.segmented-control button:hover {
  color: rgba(var(--v-theme-on-surface), 0.8);
  background: rgba(var(--v-theme-on-surface), 0.04);
}

.segmented-control button.active {
  background: rgb(var(--v-theme-surface));
  color: rgb(var(--v-theme-primary));
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06), 0 1px 2px rgba(0, 0, 0, 0.04);
  font-weight: 600;
}

/* ===== Sticky Actions ===== */
.sticky-action-card {
  position: sticky;
  top: 24px;
}

/* ===== Gap Utilities ===== */
.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }

/* Option Formula Live Preview */
.option-formula-preview {
  background: rgba(var(--v-theme-surface-variant), 0.45);
  border: 1px dashed rgba(var(--v-theme-primary), 0.25);
  border-radius: 8px;
  color: rgb(var(--v-theme-on-surface));
}
</style>

