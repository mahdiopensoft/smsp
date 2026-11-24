<!-- Unified Question Bank New View: Same Consistent Design with Repeating Question Block -->
<template>
  <div class="qb-new-page-v4 pb-16">

    <!-- Top Header Bar -->
    <div class="d-flex align-center justify-space-between mb-5 flex-wrap gap-3">
      <div class="d-flex align-center gap-3">
        <v-avatar size="44" color="primary" variant="tonal" class="rounded-xl flex-shrink-0">
          <v-icon size="24">
            {{ isEditMode ? 'mdi-file-document-edit-outline' : (questions.length > 1 ? 'mdi-format-list-checks' : 'mdi-plus-box-outline') }}
          </v-icon>
        </v-avatar>
        <div>
          <h2 class="text-h6 font-weight-black text-high-emphasis mb-0">
            {{ isEditMode ? 'تعديل السؤال' : (questions.length > 1 ? 'إضافة أسئلة جديدة' : 'إضافة سؤال جديد') }}
          </h2>
          <span class="text-caption text-medium-emphasis">
            {{ isEditMode ? 'تعديل الصياغة والخيارات والتصنيف الأكاديمي' : 'إنشاء وتخصيص أسئلة بنك الأسئلة للمؤسسات التعليمية' }}
          </span>
        </div>
      </div>

      <!-- Header Stats & Quick Actions -->
      <div class="d-flex align-center gap-2 flex-wrap">
        <v-chip v-if="questions.length > 1" color="primary" variant="tonal" class="font-weight-bold px-3">
          <v-icon start size="15">mdi-format-list-numbered</v-icon>
          إجمالي الأسئلة: {{ questions.length }}
        </v-chip>

        <custom-btn
          v-if="!isEditMode && questions.length > 1"
          type="save"
          :label="`حفظ جميع الأسئلة (${questions.length})`"
          color="primary"
          class="font-weight-bold px-4"
          :disabled="questions.length === 0 || !isContextComplete"
          :loading="saving"
          :click="() => submitAllQuestions('قيد المراجعة')"
        />
      </div>
    </div>

    <!-- Hidden Single File Input for Helper Images -->
    <input
      type="file"
      ref="imageFileInput"
      accept="image/*"
      class="d-none"
      @change="onImageFileSelected"
    />

    <!-- Main Grid: Left Column (Questions Builder) + Right Column (Classification & Properties) -->
    <v-form ref="formRef" @submit.prevent>
      <v-row>
        <!-- ======================================================== -->
        <!-- Left Column: Repeating Question Builder Cards            -->
        <!-- ======================================================== -->
        <v-col cols="12" lg="8">
          <div
            v-for="(q, qIndex) in questions"
            :key="q.id"
            class="main-card pa-5 pa-md-6 mb-5 rounded-2xl question-block-item"
            :class="{ 'question-block--active': activeQuestionIndex === qIndex }"
            @click="activeQuestionIndex = qIndex"
          >
            <!-- Question Block Header (When multiple questions exist or for quick actions) -->
            <div class="d-flex align-center justify-space-between mb-4 pb-3 border-b flex-wrap gap-2">
              <div class="d-flex align-center gap-2 flex-wrap">
                <v-avatar
                  :color="getTypeColor(q.type)"
                  size="30"
                  class="text-white font-weight-black text-caption flex-shrink-0"
                >
                  {{ qIndex + 1 }}
                </v-avatar>

                <span class="text-subtitle-1 font-weight-black text-high-emphasis">
                  السؤال رقم ({{ qIndex + 1 }})
                </span>

                <v-chip
                  size="small"
                  :color="getTypeColor(q.type)"
                  variant="tonal"
                  class="font-weight-bold flex-shrink-0"
                >
                  <v-icon start size="14">{{ getTypeIcon(q.type) }}</v-icon>
                  {{ getTypeLabel(q.type) }}
                </v-chip>

                <v-chip
                  size="x-small"
                  :color="isQuestionValid(q) ? 'success' : 'warning'"
                  variant="tonal"
                  class="font-weight-bold flex-shrink-0"
                >
                  <v-icon start size="12">{{ isQuestionValid(q) ? 'mdi-check-circle' : 'mdi-clock-outline' }}</v-icon>
                  {{ isQuestionValid(q) ? 'مكتمل' : 'قيد الإعداد' }}
                </v-chip>

                <!-- Helper Image Indicator Chip -->
                <v-chip
                  v-if="q.image"
                  size="x-small"
                  color="info"
                  variant="tonal"
                  class="font-weight-bold flex-shrink-0"
                >
                  <v-icon start size="12">mdi-image</v-icon>
                  صورة مرفقة
                </v-chip>

                <!-- Score & Difficulty Chip -->
                <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold flex-shrink-0">
                  ⭐ {{ q.defaultScore }} د
                </v-chip>
              </div>

              <!-- Header Action Buttons -->
              <div class="d-flex align-center gap-1 flex-shrink-0">
                <custom-btn
                  v-if="!isEditMode"
                  icon="mdi-content-copy"
                  isIcon
                  variant="text"
                  density="compact"
                  color="medium-emphasis"
                  title="نسخ السؤال"
                  :click="(e) => { if (e) e.stopPropagation(); duplicateQuestion(qIndex); }"
                />
                <custom-btn
                  v-if="!isEditMode && questions.length > 1"
                  type="del"
                  isIcon
                  variant="text"
                  density="compact"
                  title="حذف هذا السؤال"
                  :click="(e) => { if (e) e.stopPropagation(); removeQuestion(qIndex); }"
                />
                <v-btn
                  v-if="questions.length > 1"
                  icon
                  variant="text"
                  density="compact"
                  color="medium-emphasis"
                  :title="q.isCollapsed ? 'توسيع السؤال' : 'طي السؤال'"
                  @click.stop="q.isCollapsed = !q.isCollapsed"
                >
                  <v-icon>{{ q.isCollapsed ? 'mdi-chevron-down' : 'mdi-chevron-up' }}</v-icon>
                </v-btn>
              </div>
            </div>

            <!-- Collapsed Summary Preview -->
            <div
              v-if="q.isCollapsed && questions.length > 1"
              class="d-flex align-center justify-space-between py-2 px-1 cursor-pointer"
              @click="q.isCollapsed = false"
            >
              <div class="d-flex align-center gap-2 overflow-hidden me-2">
                <v-icon size="16" color="primary">mdi-text-box-outline</v-icon>
                <span
                  class="text-body-2 font-weight-medium text-truncate"
                  style="max-width: 480px;"
                  v-html="$sanitizeHtml(renderSnippet(q.text)) || 'سؤال بدون عنوان... اضغط للتوسيع والكتابة'"
                ></span>
              </div>
              <v-btn size="x-small" variant="tonal" color="primary" class="font-weight-bold">
                تعديل وتوسيع
                <v-icon end size="14">mdi-pencil</v-icon>
              </v-btn>
            </div>

            <!-- ======================================================== -->
            <!-- EXPANDED CONTENT: The EXACT Design from the Screenshot   -->
            <!-- ======================================================== -->
            <div v-show="!q.isCollapsed || questions.length === 1">
              <!-- 1. Question Type Selector (The 5 Large Color Cards) -->
              <div class="mb-6">
                <h3 class="text-h6 mb-4 d-flex align-center gap-2">
                  <v-icon color="indigo">mdi-shape-outline</v-icon>
                  اختر نوع السؤال
                </h3>

                <v-item-group mandatory v-model="q.type" class="type-selector-grid">
                  <v-item
                    v-for="qt in questionTypeOptions"
                    :key="qt.value"
                    :value="qt.value"
                    v-slot="{ isSelected, toggle }"
                  >
                    <div
                      class="type-option-card pa-4 rounded-xl d-flex align-center gap-3"
                      :class="[
                        `type-card-${qt.color}`,
                        { 'type-option-card--active': isSelected }
                      ]"
                      @click="() => { toggle(); onQuestionTypeChanged(q); }"
                    >
                      <v-avatar
                        size="42"
                        :color="qt.color"
                        :variant="isSelected ? 'flat' : 'tonal'"
                        :class="isSelected ? 'text-white' : ''"
                        rounded="lg"
                      >
                        <v-icon size="22" :color="isSelected ? 'white' : qt.color">
                          {{ isSelected ? qt.iconActive : qt.icon }}
                        </v-icon>
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

              <!-- 2. Question Text & Media (الصورة المساعدة وشريط الأدوات العلمي) -->
              <div class="mb-6">
                <div class="d-flex align-center justify-space-between mb-3">
                  <h3 class="text-h6 mb-0 d-flex align-center gap-2">
                    <v-icon color="primary">mdi-text-box-edit-outline</v-icon>
                    صياغة السؤال والوسائط
                  </h3>
                </div>

                <!-- State 1: No Image Attached -->
                <div
                  v-if="!q.image"
                  class="compact-image-strip pa-2 px-3 rounded-lg d-flex align-center justify-space-between mb-3 cursor-pointer"
                  @click="triggerImageUpload(qIndex)"
                >
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

                <!-- State 2: Image Attached -->
                <div
                  v-else
                  class="compact-helper-image-card pa-2 px-3 rounded-xl mb-3 d-flex align-center justify-space-between flex-wrap gap-2"
                >
                  <div class="d-flex align-center gap-3">
                    <div
                      class="image-thumb cursor-pointer"
                      title="اضغط للمعاينة المكبرة"
                      @click="openImagePreview(q.image)"
                    >
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
                      class="font-weight-bold"
                      :click="() => openImagePreview(q.image)"
                    />
                    <custom-btn
                      label="تغيير"
                      icon="mdi-swap-horizontal"
                      variant="tonal"
                      color="primary"
                      density="compact"
                      class="font-weight-bold"
                      :click="() => triggerImageUpload(qIndex)"
                    />
                    <custom-btn
                      type="del"
                      label="حذف"
                      variant="tonal"
                      density="compact"
                      class="font-weight-bold"
                      :click="() => removeImage(qIndex)"
                    />
                  </div>
                </div>

                <!-- Scientific Formula & Question Text Editor -->
                <scientific-formula-editor
                  :ref="(el) => setFormulaEditorRef(qIndex, el)"
                  v-model="q.text"
                  v-model:active-target="q.activeTarget"
                  :available-targets="getAvailableTargetsForQuestion(q, qIndex)"
                  label="نص السؤال"
                  placeholder="اكتب صياغة السؤال هنا... يمكنك النقر على زر (شريط الأدوات والرموز العلمية) بالأعلى لإدراج أي معادلات رياضية أو كيميائية أو كتل برمجية بنقرة واحدة."
                  :rows="4"
                  class="mb-2"
                  @insert-symbol="(payload) => onInsertSymbolForQuestion(qIndex, payload)"
                />
              </div>

              <v-divider class="my-6 opacity-20" />

              <!-- 3. Dynamic Options (خيارات الإجابة) -->
              <!-- Case A: Single / Multiple Choice -->
              <div v-if="q.type === 'single_choice' || q.type === 'multiple_choice'">
                <div class="d-flex align-center justify-space-between mb-4 flex-wrap gap-2">
                  <h3 class="text-h6 mb-0 d-flex align-center gap-2">
                    <v-icon color="success">mdi-format-list-checks</v-icon>
                    خيارات الإجابة
                  </h3>
                  <div class="d-flex align-center gap-2">
                    <v-chip
                      v-if="q.activeTarget?.id?.startsWith(`q_${qIndex}_opt_`)"
                      size="small"
                      color="primary"
                      variant="flat"
                      class="font-weight-bold"
                    >
                      <v-icon start size="14">mdi-crosshairs-gps</v-icon>
                      شريط الرموز يكتب في: {{ q.activeTarget.label }}
                    </v-chip>
                    <v-chip size="small" variant="tonal" color="success" class="font-weight-bold">
                      {{ q.type === 'single_choice' ? 'حدد خيار الإجابة الصحيحة' : 'حدد الإجابات الصحيحة' }}
                    </v-chip>
                  </div>
                </div>

                <div
                  v-for="(option, oIndex) in q.options"
                  :key="oIndex"
                  class="d-flex align-center gap-2 mb-3 option-row-wrap"
                  :class="{ 'option-row--targeted': q.activeTarget?.id === `q_${qIndex}_opt_${oIndex}` }"
                  @focusin="setActiveTarget(qIndex, oIndex)"
                  @click="setActiveTarget(qIndex, oIndex)"
                  @keyup="saveCursorPosition(`q_${qIndex}_opt_${oIndex}`, $event)"
                  @mouseup="saveCursorPosition(`q_${qIndex}_opt_${oIndex}`, $event)"
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

                  <!-- Option Letter Badge (A, B, C, D) -->
                  <div
                    class="option-letter-badge font-weight-bold rounded-lg cursor-pointer"
                    :class="isCorrectOption(q, oIndex) ? 'option-letter--correct' : 'option-letter--default'"
                    title="انقر لتعيين هذا الخيار كإجابة صحيحة"
                    @click="toggleCorrectOption(q, oIndex)"
                  >
                    {{ String.fromCharCode(65 + oIndex) }}
                  </div>

                  <!-- Input Text Field -->
                  <div class="flex-grow-1">
                    <custom-text-field
                      v-model="q.options[oIndex]"
                      :placeholder="'اكتب خيار الإجابة (' + String.fromCharCode(65 + oIndex) + ')'"
                      variant="outlined"
                      density="compact"
                      :color="q.activeTarget?.id === `q_${qIndex}_opt_${oIndex}` ? 'primary' : (isCorrectOption(q, oIndex) ? 'success' : undefined)"
                      :rules="[rules.required]"
                      @focus="setActiveTarget(qIndex, oIndex)"
                      @click="setActiveTarget(qIndex, oIndex)"
                    />
                    <!-- Scientific Formula Live Preview -->
                    <div
                      v-if="hasScientificMarkup(q.options[oIndex])"
                      class="option-formula-preview mt-1 px-3 py-1 rounded text-caption d-inline-flex align-center gap-2"
                    >
                      <v-icon size="13" color="primary">mdi-variable</v-icon>
                      <span class="text-medium-emphasis">معاينة الرمز:</span>
                      <span class="font-weight-bold" v-html="$sanitizeHtml(renderOptionMarkup(q.options[oIndex]))"></span>
                    </div>
                  </div>

                  <!-- Quick fx button to activate symbols for this option -->
                  <v-btn
                    size="small"
                    :variant="q.activeTarget?.id === `q_${qIndex}_opt_${oIndex}` ? 'flat' : 'tonal'"
                    :color="q.activeTarget?.id === `q_${qIndex}_opt_${oIndex}` ? 'primary' : undefined"
                    icon="mdi-function-variant"
                    class="rounded-lg"
                    :title="q.activeTarget?.id === `q_${qIndex}_opt_${oIndex}` ? 'هذا الخيار هو الوجهة النشطة لشريط الرموز' : 'إدراج رموز ومعادلات لهذا الخيار'"
                    @click.stop="activateOptionFormula(qIndex, oIndex)"
                  />

                  <!-- Correct Answer Badge -->
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

                  <!-- Remove Option Button -->
                  <custom-btn
                    v-if="q.options.length > 2"
                    type="del"
                    isIcon
                    variant="text"
                    density="compact"
                    :click="() => removeOption(q, oIndex)"
                    title="حذف الخيار"
                  />
                </div>

                <custom-btn
                  type="add"
                  label="إضافة خيار إضافي"
                  class="font-weight-bold mt-2"
                  :disabled="q.options.length >= 6"
                  :click="() => addOption(q)"
                />

                <v-alert
                  v-if="q.type === 'multiple_choice' && (!q.correctAnswerIndices || q.correctAnswerIndices.length === 0)"
                  type="warning"
                  variant="tonal"
                  density="compact"
                  class="mt-4 rounded-xl"
                >
                  يرجى تحديد إجابة صحيحة واحدة على الأقل للاختيار المتعدد.
                </v-alert>
              </div>

              <!-- Case B: True / False -->
              <div v-else-if="q.type === 'true_false'">
                <h3 class="text-h6 mb-4 d-flex align-center gap-2">
                  <v-icon color="success">mdi-scale-balance</v-icon>
                  حدد الإجابة الصحيحة
                </h3>

                <v-row class="ma-0 gap-4">
                  <div
                    class="tf-option-card flex-grow-1 pa-4 rounded-lg text-center cursor-pointer"
                    :class="{ 'tf-option-card--active-true': q.tfCorrect === true }"
                    @click="q.tfCorrect = true"
                  >
                    <v-icon size="36" :color="q.tfCorrect === true ? 'success' : 'grey'" class="mb-2">mdi-check-circle</v-icon>
                    <div class="text-h6 font-weight-bold">صواب</div>
                  </div>

                  <div
                    class="tf-option-card flex-grow-1 pa-4 rounded-lg text-center cursor-pointer"
                    :class="{ 'tf-option-card--active-false': q.tfCorrect === false }"
                    @click="q.tfCorrect = false"
                  >
                    <v-icon size="36" :color="q.tfCorrect === false ? 'error' : 'grey'" class="mb-2">mdi-close-circle</v-icon>
                    <div class="text-h6 font-weight-bold">خطأ</div>
                  </div>
                </v-row>
              </div>

              <!-- Case C: Essay -->
              <div v-else-if="q.type === 'essay'">
                <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
                  <h3 class="text-h6 mb-0 d-flex align-center gap-2">
                    <v-icon color="primary">mdi-text-box-check-outline</v-icon>
                    الإجابة النموذجية (للمصحح)
                  </h3>
                  <v-btn
                    size="small"
                    :variant="q.activeTarget?.id === `q_${qIndex}_essay` ? 'flat' : 'tonal'"
                    :color="q.activeTarget?.id === `q_${qIndex}_essay` ? 'primary' : undefined"
                    prepend-icon="mdi-function-variant"
                    class="font-weight-bold rounded-lg"
                    @click.stop="activateEssayFormula(qIndex)"
                  >
                    استخدام شريط الرموز للإجابة النموذجية
                  </v-btn>
                </div>
                <div
                  class="option-row-wrap"
                  :class="{ 'option-row--targeted': q.activeTarget?.id === `q_${qIndex}_essay` }"
                  @focusin="setEssayActiveTarget(qIndex)"
                  @click="setEssayActiveTarget(qIndex)"
                >
                  <custom-text-note
                    v-model="q.options[0]"
                    placeholder="اكتب الإجابة النموذجية وعناصر تقييم المصحح هنا..."
                    rows="4"
                    variant="outlined"
                    density="comfortable"
                    rounded="lg"
                    color="primary"
                    :rules="[rules.required]"
                    hide-details="auto"
                  />
                  <div
                    v-if="hasScientificMarkup(q.options[0])"
                    class="option-formula-preview mt-2 px-3 py-1 rounded text-caption d-inline-flex align-center gap-2"
                  >
                    <v-icon size="13" color="primary">mdi-variable</v-icon>
                    <span class="text-medium-emphasis">معاينة الرموز:</span>
                    <span class="font-weight-bold" v-html="$sanitizeHtml(renderOptionMarkup(q.options[0]))"></span>
                  </div>
                </div>
              </div>

              <!-- Case D: Fill Blanks -->
              <div v-else-if="q.type === 'fill_blanks'">
                <h3 class="text-h6 mb-4 d-flex align-center gap-2">
                  <v-icon color="deep-purple">mdi-form-textbox</v-icon>
                  الكلمات المفقودة (الإجابات)
                </h3>
                <div
                  v-for="(option, bIndex) in q.options"
                  :key="bIndex"
                  class="d-flex align-center gap-3 mb-3 option-row-wrap"
                >
                  <div
                    class="option-letter-badge font-weight-bold rounded-lg option-letter--default"
                    style="width: 36px; height: 36px; min-width: 36px;"
                  >
                    {{ bIndex + 1 }}
                  </div>
                  <div class="flex-grow-1">
                    <custom-text-field
                      v-model="q.options[bIndex]"
                      :placeholder="'الكلمة المفقودة للفراغ (' + (bIndex + 1) + ')'"
                      variant="outlined"
                      density="compact"
                      :rules="[rules.required]"
                    />
                  </div>
                  <custom-btn
                    v-if="q.options.length > 1"
                    type="del"
                    isIcon
                    variant="text"
                    :click="() => q.options.splice(bIndex, 1)"
                  />
                </div>
                <custom-btn
                  type="add"
                  color="deep-purple"
                  label="إضافة فراغ آخر"
                  class="font-weight-bold mt-2"
                  :click="() => q.options.push('')"
                />
              </div>
            </div>
          </div>

          <!-- Bottom Big Button: إضافة سؤال جديد (Repeats the exact block above!) -->
          <div v-if="!isEditMode" class="d-flex align-center justify-space-between mt-3 mb-6 gap-3 flex-wrap">
            <custom-btn
              type="add"
              label="إضافة سؤال جديد"
              icon="mdi-plus-circle-outline"
              color="primary"
              size="large"
              class="font-weight-bold py-3 flex-grow-1 rounded-xl elevation-1"
              :disabled="!canAddNewQuestion"
              :title="!canAddNewQuestion ? 'يرجى كتابة صياغة السؤال الحالي أولاً لإضافة سؤال جديد' : 'إضافة سؤال جديد'"
              :click="addNewQuestion"
            />
            <div v-if="questions.length > 1" class="d-flex align-center gap-2">
              <custom-btn
                label="طي الكل"
                icon="unfold-less-horizontal"
                variant="tonal"
                class="font-weight-bold"
                :click="collapseAll"
              />
              <custom-btn
                label="توسيع الكل"
                icon="unfold-more-horizontal"
                variant="tonal"
                class="font-weight-bold"
                :click="expandAll"
              />
            </div>
          </div>
        </v-col>

        <!-- ======================================================== -->
        <!-- Right Column: Academic Classification & Specs & Actions   -->
        <!-- ======================================================== -->
        <v-col cols="12" lg="4">
          <!-- 1. Academic Classification Card (التصنيف والربط الأكاديمي) -->
          <div class="main-card pa-6 mb-6 rounded-2xl">
            <div class="d-flex align-center justify-space-between mb-4 flex-wrap gap-2">
              <div class="d-flex align-center gap-2">
                <v-icon color="indigo">mdi-shape</v-icon>
                <h3 class="text-h6 mb-0">التصنيف والربط الأكاديمي</h3>
              </div>
            </div>

            <!-- Loader -->
            <div v-if="isLoadingQuestion" class="d-flex flex-column align-center justify-center py-10">
              <v-progress-circular indeterminate color="primary" size="36" class="mb-3" />
              <span class="text-caption font-weight-bold text-medium-emphasis">جاري تحميل التصنيف الأكاديمي...</span>
            </div>
            <div v-else>
              <!-- Institution Type Selector (مدارس / جامعات / معاهد) -->
              <div class="mb-4">
                <v-btn-toggle
                  v-model="academicContext.institution_type"
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
              <template v-if="academicContext.institution_type === 'school'">
                <auto-list
                  v-model="academicContext.stageId"
                  name="Stage"
                  label="المرحلة الدراسية"
                  cols="12"
                  :add="false"
                  @update:model-value="onStageChange"
                />
                <auto-list
                  v-model="academicContext.classTrackId"
                  name="ClassTrackByStage"
                  :param="academicContext.stageId"
                  label="الصف والمسار"
                  cols="12"
                  :add="false"
                  :disabled="!academicContext.stageId"
                  @update:model-value="onClassTrackChange"
                />
                <auto-list
                  v-model="academicContext.subjectId"
                  name="Subject"
                  :param="academicContext.classTrackId || academicContext.stageId"
                  label="المادة الدراسية"
                  cols="12"
                  :add="false"
                  :disabled="!academicContext.classTrackId && !academicContext.stageId"
                  @update:model-value="onSubjectChange"
                />
                <auto-list
                  v-model="academicContext.semesterId"
                  name="Semester"
                  label="الفصل الدراسي"
                  cols="12"
                  :add="false"
                  @update:model-value="onSemesterChange"
                />
              </template>

              <!-- 🎓 University Academic Classification Fields -->
              <template v-if="academicContext.institution_type === 'university'">
                <auto-list
                  v-model="academicContext.collegeId"
                  name="College"
                  label="الكلية الجامعية"
                  cols="12"
                  :add="false"
                  @update:model-value="onCollegeChange"
                />
                <auto-list
                  v-model="academicContext.departmentId"
                  name="DepartmentByCollege"
                  :param="academicContext.collegeId"
                  label="القسم الأكاديمي"
                  cols="12"
                  :add="false"
                  :disabled="!academicContext.collegeId"
                  @update:model-value="onDepartmentChange"
                />
                <auto-list
                  v-model="academicContext.specializationId"
                  name="Specialization"
                  :param="academicContext.departmentId"
                  label="التخصص والبرنامج"
                  cols="12"
                  :add="false"
                  :disabled="!academicContext.departmentId"
                  @update:model-value="onSpecializationChange"
                />
                <auto-list
                  v-model="academicContext.semesterSubjectId"
                  name="SemesterSubject"
                  :param="academicContext.specializationId"
                  label="مقرر الفصل الجامعي"
                  cols="12"
                  :add="false"
                  @update:model-value="onSemesterSubjectChange"
                />
              </template>

              <!-- 🏢 Institute Academic Classification Fields -->
              <template v-if="academicContext.institution_type === 'institute'">
                <auto-list
                  v-model="academicContext.instituteFieldId"
                  name="InstituteField"
                  label="المجال المهني / التقني"
                  cols="12"
                  :add="false"
                  @update:model-value="onInstituteFieldChange"
                />
                <auto-list
                  v-model="academicContext.instituteEducationSystemId"
                  name="InstituteEducationSystem"
                  :param="academicContext.instituteFieldId"
                  label="نظام التعليم والتدريب"
                  cols="12"
                  :add="false"
                  :disabled="!academicContext.instituteFieldId"
                  @update:model-value="onInstituteEducationSystemChange"
                />
                <auto-list
                  v-model="academicContext.instituteSpecializationId"
                  name="InstituteSpecialization"
                  :param="formInstituteSpecParam"
                  label="التخصص المهني"
                  cols="12"
                  :add="false"
                  :disabled="!academicContext.instituteEducationSystemId"
                  @update:model-value="onInstituteSpecializationChange"
                />
                <auto-list
                  v-model="academicContext.instituteCurriculumId"
                  name="InstituteCurriculum"
                  :param="academicContext.instituteSpecializationId"
                  label="الخطة الدراسية للمعهد"
                  cols="12"
                  :add="false"
                  :disabled="!academicContext.instituteSpecializationId"
                />
                <auto-list
                  v-model="academicContext.instituteSubjectId"
                  name="InstituteSubject"
                  :param="formInstituteSubjectParam"
                  label="المادة الدراسية للمعهد"
                  cols="12"
                  :add="false"
                  @update:model-value="onInstituteSubjectChange"
                />
              </template>

              <!-- Common: Unit, Lesson -->
              <auto-list
                v-model="academicContext.unitId"
                name="UnitBySubject"
                :param="formUnitParam"
                :label="academicContext.institution_type === 'university' ? 'مفردة / موضوع المقرر' : (academicContext.institution_type === 'institute' ? 'الوحدة / التدريب العملي' : 'الوحدة الدراسية')"
                cols="12"
                :add="false"
                :disabled="academicContext.institution_type === 'university' ? !academicContext.semesterSubjectId : (academicContext.institution_type === 'institute' ? !academicContext.instituteSubjectId : !academicContext.subjectId)"
                @update:model-value="onUnitChange"
              />
              <auto-list
                v-model="academicContext.lessonId"
                name="LessonByUnit"
                :param="formLessonParam"
                :label="academicContext.institution_type === 'university' ? 'المحاضرة / الدرس الأكاديمي' : (academicContext.institution_type === 'institute' ? 'التدريب / الدرس المهني' : 'الدرس المدرسي')"
                cols="12"
                :add="false"
                :disabled="!academicContext.unitId"
                @update:model-value="onLessonChange"
              />
            </div>
          </div>

          <!-- 2. Question Attributes Card (خصائص ومواصفات السؤال) -->
          <div class="main-card pa-6 mb-6 rounded-2xl">
            <div class="d-flex align-center justify-space-between mb-4 flex-wrap gap-2">
              <div class="d-flex align-center gap-2">
                <v-icon color="warning">mdi-speedometer</v-icon>
                <h3 class="text-h6 mb-0">خصائص ومواصفات السؤال</h3>
              </div>
              <custom-btn
                v-if="questions.length > 1"
                icon="mdi-check-all"
                label="تطبيق على الكل"
                variant="tonal"
                color="primary"
                size="small"
                class="font-weight-bold text-caption"
                :click="applyPropertiesToAllQuestions"
              />
            </div>

            <!-- Default Score -->
            <div class="mb-4">
              <label class="text-caption font-weight-bold text-medium-emphasis mb-1 d-block">درجة السؤال المستحقة</label>
              <custom-text-field
                v-model.number="currentActiveQuestion.defaultScore"
                type="number"
                min="1"
                icon="star-circle-outline"
                variant="outlined"
                density="compact"
                :rules="[rules.required, rules.positive]"
              />
            </div>

            <!-- Expected Time -->
            <div class="mb-5">
              <label class="text-caption font-weight-bold text-medium-emphasis mb-1 d-block">الزمن المتوقع للحل (بالدقائق)</label>
              <custom-text-field
                v-model.number="currentActiveQuestion.expectedTimeMinutes"
                type="number"
                min="1"
                icon="clock-outline"
                variant="outlined"
                density="compact"
                :rules="[rules.required, rules.positive]"
              />
            </div>

            <!-- Difficulty Toggle -->
            <div class="mb-5">
              <label class="text-caption font-weight-bold text-medium-emphasis mb-2 d-block">مستوى الصعوبة</label>
              <div class="segmented-control w-100 pa-1 d-flex gap-1">
                <button
                  type="button"
                  class="flex-grow-1 d-flex align-center justify-center gap-1 font-weight-bold"
                  :class="{ active: currentActiveQuestion.difficulty === 1 }"
                  @click="currentActiveQuestion.difficulty = 1"
                >
                  <v-icon size="18" color="success">mdi-gauge-low</v-icon>
                  <span>سهل</span>
                </button>
                <button
                  type="button"
                  class="flex-grow-1 d-flex align-center justify-center gap-1 font-weight-bold"
                  :class="{ active: currentActiveQuestion.difficulty === 2 }"
                  @click="currentActiveQuestion.difficulty = 2"
                >
                  <v-icon size="18" color="warning">mdi-gauge</v-icon>
                  <span>متوسط</span>
                </button>
                <button
                  type="button"
                  class="flex-grow-1 d-flex align-center justify-center gap-1 font-weight-bold"
                  :class="{ active: currentActiveQuestion.difficulty === 3 }"
                  @click="currentActiveQuestion.difficulty = 3"
                >
                  <v-icon size="18" color="error">mdi-gauge-full</v-icon>
                  <span>صعب</span>
                </button>
              </div>
            </div>

            <!-- Bloom Level -->
            <div>
              <label class="text-caption font-weight-bold text-medium-emphasis mb-2 d-block">مستوى بلوم المعرفي</label>
              <v-chip-group v-model="currentActiveQuestion.bloomLevel" mandatory class="flex-wrap">
                <v-chip
                  v-for="level in bloomLevels"
                  :key="level.value"
                  :value="level.value"
                  filter
                  variant="outlined"
                  class="font-weight-bold"
                  active-class="bg-primary text-white border-0"
                >
                  {{ level.text }}
                </v-chip>
              </v-chip-group>
            </div>
          </div>

          <!-- 3. Actions Card (الإجراءات) -->
          <div class="main-card pa-6 rounded-2xl sticky-action-card">
            <custom-btn
              type="add"
              :label="isEditMode ? 'حفظ التعديلات' : (questions.length > 1 ? `حفظ جميع الأسئلة (${questions.length})` : 'حفظ وإرسال للمراجعة')"
              :icon="isEditMode ? 'mdi-check-circle' : 'mdi-send'"
              color="primary"
              class="font-weight-bold mb-3 w-100"
              :loading="saving"
              :click="() => submitAllQuestions(isEditMode ? 'قيد المراجعة' : 'قيد المراجعة')"
            />

            <custom-btn
              v-if="!isEditMode"
              type="save"
              label="حفظ كمسودة"
              icon="mdi-content-save-outline"
              color="secondary"
              variant="tonal"
              class="font-weight-bold w-100"
              :disabled="saving"
              :click="() => submitAllQuestions('مسودة')"
            />
          </div>
        </v-col>
      </v-row>
    </v-form>

    <!-- Dialog for Image Preview -->
    <custom-dialog
      v-model="previewImageDialog"
      title="معاينة الصورة المساعدة"
      width="650"
      height="auto"
    >
      <div
        class="d-flex justify-center align-center pa-2 rounded-xl overflow-hidden"
        style="background: rgba(var(--v-theme-surface-variant), 0.3);"
      >
        <img
          :src="previewImageSrc"
          alt="الصورة المساعدة"
          style="max-height: 480px; max-width: 100%; object-fit: contain; border-radius: 8px;"
        />
      </div>
    </custom-dialog>

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

      activeQuestionIndex: 0,
      activeImageQuestionIndex: null,
      previewImageDialog: false,
      previewImageSrc: "",

      // References & tracking
      formulaEditorRefs: {},
      optionCursorPositions: {},

      isPreservingState: false,
      _stableUnitParam: null,
      _lastUnitParamKey: null,
      _stableInstituteSpecParam: null,
      _lastInstituteSpecKey: null,
      _stableInstituteSubjectParam: null,
      _lastInstituteSubjectKey: null,
      _lastCollegeId: null,
      _lastDepartmentId: null,
      _lastSpecializationId: null,
      _lastSemesterSubjectId: null,
      _lastStageId: null,
      _lastClassTrackId: null,
      _lastSubjectId: null,
      _lastSemesterId: null,
      _lastUnitId: null,
      _stableLessonParam: null,
      _lastLessonParamKey: null,
      _currentActiveType: "school",

      // State snapshots to preserve selections across sector toggle
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

      // Shared Academic Classification & Global Specs
      academicContext: {
        institution_type: "school",
        stageId: null,
        classTrackId: null,
        subjectId: null,
        semesterId: null,
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
        defaultScore: 1,
        expectedTimeMinutes: 1,
        difficulty: 2,
        bloomLevel: "تطبيق",
      },

      // Array of Questions (Starts with 1, can repeat endlessly!)
      questions: [
        {
          id: Date.now(),
          isCollapsed: false,
          type: "single_choice",
          text: "",
          image: "",
          options: ["", "", "", ""],
          correctAnswerIndex: 0,
          correctAnswerIndices: [],
          tfCorrect: true,
          defaultScore: 1,
          expectedTimeMinutes: 1,
          difficulty: 2,
          bloomLevel: "تطبيق",
          activeTarget: null,
        },
      ],

      // Definitions
      questionTypeOptions: [
        { value: "single_choice", label: "اختيار مفرد", color: "indigo", icon: "mdi-record-circle-outline", iconActive: "mdi-record-circle" },
        { value: "multiple_choice", label: "اختيار متعدد", color: "warning", icon: "mdi-checkbox-multiple-blank-outline", iconActive: "mdi-checkbox-multiple-marked" },
        { value: "true_false", label: "صواب / خطأ", color: "success", icon: "mdi-toggle-switch-off-outline", iconActive: "mdi-toggle-switch" },
        { value: "essay", label: "مقالي", color: "primary", icon: "mdi-text-box-edit-outline", iconActive: "mdi-text-box-edit" },
        { value: "fill_blanks", label: "فراغات", color: "deep-purple", icon: "mdi-form-textbox", iconActive: "mdi-form-textbox" },
      ],
      difficultiesOptions: [
        { text: "سهل", value: 1 },
        { text: "متوسط", value: 2 },
        { text: "صعب", value: 3 },
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

  computed: {
    currentActiveQuestion() {
      if (this.questions[this.activeQuestionIndex]) {
        return this.questions[this.activeQuestionIndex];
      }
      return this.questions[0] || {};
    },

    isContextComplete() {
      if (this.academicContext.institution_type === "university") {
        return !!(this.academicContext.semesterSubjectId && this.academicContext.unitId && this.academicContext.lessonId);
      } else if (this.academicContext.institution_type === "institute") {
        return !!(this.academicContext.instituteSubjectId && this.academicContext.unitId && this.academicContext.lessonId);
      }
      return !!(this.academicContext.subjectId && this.academicContext.unitId && this.academicContext.lessonId);
    },

    canAddNewQuestion() {
      if (this.questions.length === 0) return true;
      return this.questions.every((q) => q.text && q.text.trim().length > 0);
    },

    formInstituteSpecParam() {
      const fieldId = this.academicContext.instituteFieldId || "";
      const eduSysId = this.academicContext.instituteEducationSystemId || "";
      const key = `${fieldId}_${eduSysId}`;
      if (key !== this._lastInstituteSpecKey) {
        this._lastInstituteSpecKey = key;
        const p = {};
        if (this.academicContext.instituteFieldId) p.field = this.academicContext.instituteFieldId;
        if (this.academicContext.instituteEducationSystemId) p.education_system = this.academicContext.instituteEducationSystemId;
        this._stableInstituteSpecParam = Object.keys(p).length ? p : null;
      }
      return this._stableInstituteSpecParam;
    },

    formInstituteSubjectParam() {
      const fieldId = this.academicContext.instituteFieldId || "";
      const key = `${fieldId}`;
      if (key !== this._lastInstituteSubjectKey) {
        this._lastInstituteSubjectKey = key;
        this._stableInstituteSubjectParam = this.academicContext.instituteFieldId ? { field: this.academicContext.instituteFieldId } : null;
      }
      return this._stableInstituteSubjectParam;
    },

    formUnitParam() {
      let key = null;
      let paramObj = null;
      if (this.academicContext.institution_type === "university") {
        key = `univ_${this.academicContext.semesterSubjectId || ""}`;
        paramObj = this.academicContext.semesterSubjectId ? {
          institution_type: "university",
          semester_subject: this.academicContext.semesterSubjectId,
        } : null;
      } else if (this.academicContext.institution_type === "institute") {
        key = `inst_${this.academicContext.instituteSubjectId || ""}`;
        paramObj = this.academicContext.instituteSubjectId ? {
          institution_type: "institute",
          subject: this.academicContext.instituteSubjectId,
        } : null;
      } else {
        key = `school_${this.academicContext.subjectId || ""}_${this.academicContext.semesterId || ""}_${this.academicContext.classTrackId || ""}_${this.academicContext.stageId || ""}`;
        paramObj = (this.academicContext.subjectId || this.academicContext.classTrackId) ? {
          institution_type: "school",
          school_subject: this.academicContext.subjectId,
          subject: this.academicContext.subjectId,
          semester: this.academicContext.semesterId,
          class_track: this.academicContext.classTrackId,
          stage: this.academicContext.stageId,
        } : null;
      }

      if (key !== this._lastUnitParamKey) {
        this._lastUnitParamKey = key;
        this._stableUnitParam = paramObj;
      }
      return this._stableUnitParam;
    },

    formLessonParam() {
      let key = null;
      let paramObj = null;
      if (this.academicContext.unitId) {
        key = `${this.academicContext.institution_type || "school"}_${this.academicContext.unitId}`;
        paramObj = {
          unit: this.academicContext.unitId,
          institution_type: this.academicContext.institution_type,
        };
      }
      if (key !== this._lastLessonParamKey) {
        this._lastLessonParamKey = key;
        this._stableLessonParam = paramObj;
      }
      return this._stableLessonParam;
    },
  },

  async created() {
    if (this.$route.query.id) {
      this.isLoadingQuestion = true;
      this.isEditMode = true;
      this.editId = this.$route.query.id;
      await this.loadQuestionForEdit(this.editId);
    } else {
      this.restorePersistedAcademicAndSpecs();
    }
  },

  mounted() {
    ensureKaTeXLoaded();
  },

  methods: {
    // === SCIENTIFIC FORMULA HELPERS ===
    hasScientificMarkup(text) {
      if (!text || typeof text !== "string") return false;
      return text.includes("$") || text.includes("\\") || /([A-Za-z]\^[0-9]|[A-Za-z]_[0-9]|->|⇌)/.test(text);
    },

    renderOptionMarkup(text) {
      return parseScientificMarkup(text);
    },

    renderSnippet(text) {
      if (!text) return "";
      const plain = text.replace(/<[^>]*>/g, "").replace(/\$+/g, "").trim();
      return plain.length > 60 ? plain.substring(0, 60) + "..." : plain;
    },

    setFormulaEditorRef(qIndex, el) {
      if (el) {
        this.formulaEditorRefs[qIndex] = el;
      }
    },

    getAvailableTargetsForQuestion(q, qIndex) {
      const targets = [{ id: `q_${qIndex}_content`, label: "نص السؤال" }];
      if (q.type === "single_choice" || q.type === "multiple_choice") {
        (q.options || []).forEach((_, i) => {
          targets.push({
            id: `q_${qIndex}_opt_${i}`,
            qIndex,
            optionIndex: i,
            label: `الخيار (${String.fromCharCode(65 + i)})`,
          });
        });
      } else if (q.type === "essay") {
        targets.push({
          id: `q_${qIndex}_essay`,
          qIndex,
          optionIndex: 0,
          label: "الإجابة النموذجية",
        });
      }
      return targets;
    },

    setActiveTarget(qIndex, oIndex) {
      this.activeQuestionIndex = qIndex;
      const q = this.questions[qIndex];
      if (!q) return;
      q.activeTarget = {
        id: `q_${qIndex}_opt_${oIndex}`,
        qIndex,
        optionIndex: oIndex,
        label: `الخيار (${String.fromCharCode(65 + oIndex)})`,
      };
    },

    setEssayActiveTarget(qIndex) {
      this.activeQuestionIndex = qIndex;
      const q = this.questions[qIndex];
      if (!q) return;
      q.activeTarget = {
        id: `q_${qIndex}_essay`,
        qIndex,
        optionIndex: 0,
        label: "الإجابة النموذجية",
      };
    },

    activateOptionFormula(qIndex, oIndex) {
      this.setActiveTarget(qIndex, oIndex);
      const editorRef = this.formulaEditorRefs[qIndex];
      if (editorRef && typeof editorRef.openToolbar === "function") {
        editorRef.openToolbar();
      }
    },

    activateEssayFormula(qIndex) {
      this.setEssayActiveTarget(qIndex);
      const editorRef = this.formulaEditorRefs[qIndex];
      if (editorRef && typeof editorRef.openToolbar === "function") {
        editorRef.openToolbar();
      }
    },

    saveCursorPosition(id, event) {
      const target = event?.target;
      if (target && typeof target.selectionStart === "number") {
        this.optionCursorPositions[id] = {
          start: target.selectionStart,
          end: target.selectionEnd,
        };
      }
    },

    onInsertSymbolForQuestion(qIndex, { item, target }) {
      const q = this.questions[qIndex];
      if (!q || !target || target.id === `q_${qIndex}_content`) return;
      const idx = target.optionIndex;
      if (idx === undefined || idx === null || idx < 0 || !q.options || idx >= q.options.length) return;
      let original = q.options[idx] || "";
      let textToInsert = item.snippet;

      const dollarCountBefore = (original.match(/\$/g) || []).length;
      const isInsideMath = dollarCountBefore % 2 === 1;
      const isLatex =
        (textToInsert.includes("\\") || textToInsert.includes("^") || textToInsert.includes("_")) &&
        !textToInsert.startsWith("$") &&
        !textToInsert.startsWith("`") &&
        !textToInsert.startsWith("\n|");

      if (!isInsideMath && isLatex) {
        textToInsert = `$${textToInsert}$`;
      }

      const pos = this.optionCursorPositions[target.id];
      if (pos && typeof pos.start === "number" && pos.start <= original.length) {
        const before = original.substring(0, pos.start);
        const after = original.substring(pos.end ?? pos.start);
        q.options[idx] = before + textToInsert + after;
        const newPos = pos.start + textToInsert.length;
        this.optionCursorPositions[target.id] = { start: newPos, end: newPos };
      } else {
        q.options[idx] = original
          ? (original.endsWith(" ") ? original + textToInsert : original + " " + textToInsert)
          : textToInsert;
        const newPos = q.options[idx].length;
        this.optionCursorPositions[target.id] = { start: newPos, end: newPos };
      }
    },

    // === QUESTIONS REPETITION (إضافة ونسخ وحذف الأسئلة) ===
    createQuestionObject() {
      return {
        id: Date.now() + Math.random(),
        isCollapsed: false,
        type: "single_choice",
        text: "",
        image: "",
        options: ["", "", "", ""],
        correctAnswerIndex: 0,
        correctAnswerIndices: [],
        tfCorrect: true,
        defaultScore: this.currentActiveQuestion.defaultScore || this.academicContext.defaultScore || 1,
        expectedTimeMinutes: this.currentActiveQuestion.expectedTimeMinutes || this.academicContext.expectedTimeMinutes || 1,
        difficulty: this.currentActiveQuestion.difficulty || this.academicContext.difficulty || 2,
        bloomLevel: this.currentActiveQuestion.bloomLevel || this.academicContext.bloomLevel || "تطبيق",
        activeTarget: null,
      };
    },

    addNewQuestion() {
      const lastQ = this.questions[this.questions.length - 1];
      if (lastQ && (!lastQ.text || !lastQ.text.trim())) {
        this.$alert("warning", {
          title: "تنبيه",
          message: "يرجى كتابة صياغة السؤال الحالي أولاً قبل إضافة سؤال جديد.",
        });
        lastQ.isCollapsed = false;
        return;
      }

      this.questions.forEach((q) => (q.isCollapsed = true));
      const newQ = this.createQuestionObject();
      this.questions.push(newQ);
      this.activeQuestionIndex = this.questions.length - 1;

      this.$nextTick(() => {
        window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
      });
    },

    duplicateQuestion(index) {
      const q = this.questions[index];
      if (!q.text || !q.text.trim()) {
        this.$alert("warning", {
          title: "تنبيه",
          message: "يرجى إكمال كتابة السؤال أولاً قبل نسخه.",
        });
        q.isCollapsed = false;
        return;
      }

      const newQ = JSON.parse(JSON.stringify(q));
      newQ.id = Date.now() + Math.random();
      this.questions.forEach((item) => (item.isCollapsed = true));
      newQ.isCollapsed = false;
      this.questions.splice(index + 1, 0, newQ);
      this.activeQuestionIndex = index + 1;
      this.$alert("info", { message: "تم نسخ السؤال بنجاح" });
    },

    removeQuestion(index) {
      this.questions.splice(index, 1);
      if (this.activeQuestionIndex >= this.questions.length) {
        this.activeQuestionIndex = Math.max(0, this.questions.length - 1);
      }
      if (this.questions[this.activeQuestionIndex]) {
        this.questions[this.activeQuestionIndex].isCollapsed = false;
      }
    },

    collapseAll() {
      this.questions.forEach((q) => (q.isCollapsed = true));
    },

    expandAll() {
      this.questions.forEach((q) => (q.isCollapsed = false));
    },

    applyPropertiesToAllQuestions() {
      const current = this.currentActiveQuestion;
      this.questions.forEach((q) => {
        q.defaultScore = current.defaultScore;
        q.expectedTimeMinutes = current.expectedTimeMinutes;
        q.difficulty = current.difficulty;
        q.bloomLevel = current.bloomLevel;
      });
      this.$alert("success", { message: "تم تطبيق الدرجة والزمن والصعوبة ومستوى بلوم على جميع الأسئلة" });
    },

    onQuestionTypeChanged(q) {
      if (q.type === "single_choice" || q.type === "multiple_choice") {
        if (!q.options || q.options.length < 2) {
          q.options = ["", "", "", ""];
        }
      } else if (q.type === "essay") {
        if (!q.options || q.options.length === 0) {
          q.options = [""];
        }
      } else if (q.type === "fill_blanks") {
        if (!q.options || q.options.length === 0) {
          q.options = [""];
        }
      }
    },

    addOption(q) {
      if (q.options.length < 6) {
        q.options.push("");
      }
    },

    removeOption(q, index) {
      q.options.splice(index, 1);
      if (q.type === "single_choice") {
        if (q.correctAnswerIndex >= index && q.correctAnswerIndex > 0) {
          q.correctAnswerIndex--;
        }
      } else if (q.type === "multiple_choice") {
        q.correctAnswerIndices = (q.correctAnswerIndices || [])
          .filter((i) => i !== index)
          .map((i) => (i > index ? i - 1 : i));
      }
    },

    isCorrectOption(q, index) {
      if (q.type === "single_choice") return q.correctAnswerIndex === index;
      if (q.type === "multiple_choice") return (q.correctAnswerIndices || []).includes(index);
      return false;
    },

    toggleCorrectOption(q, index) {
      if (q.type === "single_choice") {
        q.correctAnswerIndex = index;
      } else if (q.type === "multiple_choice") {
        if (!Array.isArray(q.correctAnswerIndices)) {
          q.correctAnswerIndices = [];
        }
        const i = q.correctAnswerIndices.indexOf(index);
        if (i > -1) {
          q.correctAnswerIndices.splice(i, 1);
        } else {
          q.correctAnswerIndices.push(index);
        }
      }
    },

    // === HELPER IMAGE MANAGEMENT ===
    triggerImageUpload(qIndex) {
      this.activeImageQuestionIndex = qIndex;
      if (this.$refs.imageFileInput) {
        this.$refs.imageFileInput.value = null;
        this.$refs.imageFileInput.click();
      }
    },

    onImageFileSelected(event) {
      const file = event.target.files && event.target.files[0];
      if (!file) return;
      const targetQ = this.questions[this.activeImageQuestionIndex];
      if (!targetQ) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        targetQ.image = e.target.result;
        this.$alert("success", { message: "تم إرفاق الصورة المساعدة بنجاح" });
      };
      reader.readAsDataURL(file);
    },

    removeImage(qIndex) {
      if (this.questions[qIndex]) {
        this.questions[qIndex].image = "";
      }
    },

    openImagePreview(src) {
      if (!src) return;
      this.previewImageSrc = src;
      this.previewImageDialog = true;
    },

    // === COMPLETION VALIDATION ===
    isQuestionValid(q) {
      if (!q || !q.text || !q.text.trim()) return false;
      if (q.type === "single_choice") {
        if (!q.options || q.options.length < 2) return false;
        if (q.options.some((opt) => !opt || !opt.trim())) return false;
        if (q.correctAnswerIndex === null || q.correctAnswerIndex === undefined || q.correctAnswerIndex < 0) return false;
      } else if (q.type === "multiple_choice") {
        if (!q.options || q.options.length < 2) return false;
        if (q.options.some((opt) => !opt || !opt.trim())) return false;
        if (!q.correctAnswerIndices || q.correctAnswerIndices.length === 0) return false;
      } else if (q.type === "true_false") {
        if (typeof q.tfCorrect !== "boolean") return false;
      } else if (q.type === "essay") {
        if (!q.options || !q.options[0] || !q.options[0].trim()) return false;
      } else if (q.type === "fill_blanks") {
        if (!q.options || q.options.length === 0 || q.options.some((opt) => !opt || !opt.trim())) return false;
      }
      return true;
    },

    getTypeLabel(type) {
      const t = this.questionTypeOptions.find((x) => x.value === type);
      return t ? t.label : type;
    },
    getTypeColor(type) {
      const t = this.questionTypeOptions.find((x) => x.value === type);
      return t ? t.color : "grey";
    },
    getTypeIcon(type) {
      const t = this.questionTypeOptions.find((x) => x.value === type);
      return t ? t.icon : "mdi-help";
    },
    getDifficultyLabel(diff) {
      const d = String(diff ?? "").toLowerCase().trim();
      if (d === "1" || d === "easy" || d === "سهل") return "سهل";
      if (d === "2" || d === "medium" || d === "متوسط") return "متوسط";
      if (d === "3" || d === "hard" || d === "صعب") return "صعب";
      return diff || "-";
    },

    mapQuestionType(frontendType) {
      const map = {
        single_choice: "Single Choice",
        multiple_choice: "Multiple Choice",
        true_false: "True/False",
        essay: "Essay",
        fill_blanks: "Fill in the Blanks",
      };
      return map[frontendType] || frontendType;
    },

    // === CASCADE HANDLERS FOR ACADEMIC CLASSIFICATION ===
    onInstitutionTypeToggle(newType) {
      if (this.isLoadingQuestion) return;
      const targetType = newType || this.academicContext.institution_type;

      const currentType = this._currentActiveType || "school";
      if (currentType === "university") {
        this.universityState = {
          collegeId: this.academicContext.collegeId,
          departmentId: this.academicContext.departmentId,
          specializationId: this.academicContext.specializationId,
          semesterSubjectId: this.academicContext.semesterSubjectId,
          unitId: this.academicContext.unitId,
          lessonId: this.academicContext.lessonId,
          learningOutcomeId: this.academicContext.learningOutcomeId,
        };
      } else if (currentType === "institute") {
        this.instituteState = {
          instituteFieldId: this.academicContext.instituteFieldId,
          instituteEducationSystemId: this.academicContext.instituteEducationSystemId,
          instituteSpecializationId: this.academicContext.instituteSpecializationId,
          instituteCurriculumId: this.academicContext.instituteCurriculumId,
          instituteSubjectId: this.academicContext.instituteSubjectId,
          unitId: this.academicContext.unitId,
          lessonId: this.academicContext.lessonId,
          learningOutcomeId: this.academicContext.learningOutcomeId,
        };
      } else {
        this.schoolState = {
          stageId: this.academicContext.stageId,
          classTrackId: this.academicContext.classTrackId,
          subjectId: this.academicContext.subjectId,
          semesterId: this.academicContext.semesterId,
          unitId: this.academicContext.unitId,
          lessonId: this.academicContext.lessonId,
          learningOutcomeId: this.academicContext.learningOutcomeId,
        };
      }

      this._currentActiveType = targetType;

      if (targetType === "university") {
        this.academicContext.collegeId = this.universityState.collegeId;
        this.academicContext.departmentId = this.universityState.departmentId;
        this.academicContext.specializationId = this.universityState.specializationId;
        this.academicContext.semesterSubjectId = this.universityState.semesterSubjectId;
        this.academicContext.subjectId = this.universityState.semesterSubjectId;
        this.academicContext.unitId = this.universityState.unitId;
        this.academicContext.lessonId = this.universityState.lessonId;
        this.academicContext.learningOutcomeId = this.universityState.learningOutcomeId;
      } else if (targetType === "institute") {
        this.academicContext.instituteFieldId = this.instituteState.instituteFieldId;
        this.academicContext.instituteEducationSystemId = this.instituteState.instituteEducationSystemId;
        this.academicContext.instituteSpecializationId = this.instituteState.instituteSpecializationId;
        this.academicContext.instituteCurriculumId = this.instituteState.instituteCurriculumId;
        this.academicContext.instituteSubjectId = this.instituteState.instituteSubjectId;
        this.academicContext.subjectId = this.instituteState.instituteSubjectId;
        this.academicContext.unitId = this.instituteState.unitId;
        this.academicContext.lessonId = this.instituteState.lessonId;
        this.academicContext.learningOutcomeId = this.instituteState.learningOutcomeId;
      } else {
        this.academicContext.stageId = this.schoolState.stageId;
        this.academicContext.classTrackId = this.schoolState.classTrackId;
        this.academicContext.subjectId = this.schoolState.subjectId;
        this.academicContext.semesterId = this.schoolState.semesterId;
        this.academicContext.unitId = this.schoolState.unitId;
        this.academicContext.lessonId = this.schoolState.lessonId;
        this.academicContext.learningOutcomeId = this.schoolState.learningOutcomeId;
      }

      this._lastCollegeId = this.academicContext.collegeId;
      this._lastDepartmentId = this.academicContext.departmentId;
      this._lastSpecializationId = this.academicContext.specializationId;
      this._lastSemesterSubjectId = this.academicContext.semesterSubjectId;
      this._lastStageId = this.academicContext.stageId;
      this._lastClassTrackId = this.academicContext.classTrackId;
      this._lastSubjectId = this.academicContext.subjectId;
      this._lastSemesterId = this.academicContext.semesterId;
      this._lastUnitId = this.academicContext.unitId;

      this.persistAcademicAndSpecs();
    },

    onStageChange() {
      if (this.isLoadingQuestion || this.isPreservingState) return;
      if (this.academicContext.stageId === this._lastStageId) return;
      this._lastStageId = this.academicContext.stageId;
      this.academicContext.classTrackId = null;
      this.academicContext.subjectId = null;
      this.academicContext.unitId = null;
      this.academicContext.lessonId = null;
      this.academicContext.learningOutcomeId = null;
      this.persistAcademicAndSpecs();
    },

    onClassTrackChange() {
      if (this.isLoadingQuestion || this.isPreservingState) return;
      if (this.academicContext.classTrackId === this._lastClassTrackId) return;
      this._lastClassTrackId = this.academicContext.classTrackId;
      this.academicContext.subjectId = null;
      this.academicContext.unitId = null;
      this.academicContext.lessonId = null;
      this.academicContext.learningOutcomeId = null;
      this.persistAcademicAndSpecs();
    },

    onSubjectChange() {
      if (this.isLoadingQuestion || this.isPreservingState) return;
      if (this.academicContext.subjectId === this._lastSubjectId) return;
      this._lastSubjectId = this.academicContext.subjectId;
      this.academicContext.unitId = null;
      this.academicContext.lessonId = null;
      this.academicContext.learningOutcomeId = null;
      this.persistAcademicAndSpecs();
    },

    onSemesterChange() {
      if (this.isLoadingQuestion || this.isPreservingState) return;
      if (this.academicContext.semesterId === this._lastSemesterId) return;
      this._lastSemesterId = this.academicContext.semesterId;
      this.academicContext.unitId = null;
      this.academicContext.lessonId = null;
      this.academicContext.learningOutcomeId = null;
      this.persistAcademicAndSpecs();
    },

    onCollegeChange() {
      if (this.isLoadingQuestion || this.isPreservingState) return;
      if (this.academicContext.collegeId === this._lastCollegeId) return;
      this._lastCollegeId = this.academicContext.collegeId;
      this.academicContext.departmentId = null;
      this.academicContext.specializationId = null;
      this.academicContext.semesterSubjectId = null;
      this.academicContext.unitId = null;
      this.academicContext.lessonId = null;
      this.academicContext.learningOutcomeId = null;
      this.persistAcademicAndSpecs();
    },

    onDepartmentChange() {
      if (this.isLoadingQuestion || this.isPreservingState) return;
      if (this.academicContext.departmentId === this._lastDepartmentId) return;
      this._lastDepartmentId = this.academicContext.departmentId;
      this.academicContext.specializationId = null;
      this.academicContext.semesterSubjectId = null;
      this.academicContext.unitId = null;
      this.academicContext.lessonId = null;
      this.academicContext.learningOutcomeId = null;
      this.persistAcademicAndSpecs();
    },

    onSpecializationChange() {
      if (this.isLoadingQuestion || this.isPreservingState) return;
      if (this.academicContext.specializationId === this._lastSpecializationId) return;
      this._lastSpecializationId = this.academicContext.specializationId;
      this.academicContext.semesterSubjectId = null;
      this.academicContext.unitId = null;
      this.academicContext.lessonId = null;
      this.academicContext.learningOutcomeId = null;
      this.persistAcademicAndSpecs();
    },

    onSemesterSubjectChange() {
      if (this.isLoadingQuestion || this.isPreservingState) return;
      if (this.academicContext.semesterSubjectId === this._lastSemesterSubjectId) return;
      this._lastSemesterSubjectId = this.academicContext.semesterSubjectId;
      this.academicContext.subjectId = this.academicContext.semesterSubjectId;
      this.academicContext.unitId = null;
      this.academicContext.lessonId = null;
      this.academicContext.learningOutcomeId = null;
      this.persistAcademicAndSpecs();
    },

    onInstituteFieldChange() {
      if (this.isLoadingQuestion || this.isPreservingState) return;
      this.academicContext.instituteEducationSystemId = null;
      this.academicContext.instituteSpecializationId = null;
      this.academicContext.instituteCurriculumId = null;
      this.academicContext.instituteSubjectId = null;
      this.academicContext.subjectId = null;
      this.academicContext.unitId = null;
      this.academicContext.lessonId = null;
      this.academicContext.learningOutcomeId = null;
      this.persistAcademicAndSpecs();
    },

    onInstituteEducationSystemChange() {
      if (this.isLoadingQuestion || this.isPreservingState) return;
      this.academicContext.instituteSpecializationId = null;
      this.academicContext.instituteCurriculumId = null;
      this.academicContext.instituteSubjectId = null;
      this.academicContext.subjectId = null;
      this.academicContext.unitId = null;
      this.academicContext.lessonId = null;
      this.academicContext.learningOutcomeId = null;
      this.persistAcademicAndSpecs();
    },

    onInstituteSpecializationChange() {
      if (this.isLoadingQuestion || this.isPreservingState) return;
      this.academicContext.instituteCurriculumId = null;
      this.persistAcademicAndSpecs();
    },

    onInstituteSubjectChange() {
      if (this.isLoadingQuestion || this.isPreservingState) return;
      this.academicContext.subjectId = this.academicContext.instituteSubjectId;
      this.academicContext.unitId = null;
      this.academicContext.lessonId = null;
      this.academicContext.learningOutcomeId = null;
      this.persistAcademicAndSpecs();
    },

    onUnitChange() {
      if (this.isLoadingQuestion || this.isPreservingState) return;
      if (this.academicContext.unitId === this._lastUnitId) return;
      this._lastUnitId = this.academicContext.unitId;
      this.academicContext.lessonId = null;
      this.academicContext.learningOutcomeId = null;
      this.persistAcademicAndSpecs();
    },

    onLessonChange() {
      if (this.isLoadingQuestion || this.isPreservingState) return;
      this.persistAcademicAndSpecs();
    },

    // === PERSISTENCE HELPERS ===
    persistAcademicAndSpecs() {
      if (this.isEditMode) return;
      try {
        const academicData = {
          institution_type: this.academicContext.institution_type,
          stageId: this.academicContext.stageId,
          classTrackId: this.academicContext.classTrackId,
          subjectId: this.academicContext.subjectId,
          semesterId: this.academicContext.semesterId,
          collegeId: this.academicContext.collegeId,
          departmentId: this.academicContext.departmentId,
          specializationId: this.academicContext.specializationId,
          semesterSubjectId: this.academicContext.semesterSubjectId,
          instituteFieldId: this.academicContext.instituteFieldId,
          instituteEducationSystemId: this.academicContext.instituteEducationSystemId,
          instituteSpecializationId: this.academicContext.instituteSpecializationId,
          instituteCurriculumId: this.academicContext.instituteCurriculumId,
          instituteSubjectId: this.academicContext.instituteSubjectId,
          unitId: this.academicContext.unitId,
          lessonId: this.academicContext.lessonId,
          learningOutcomeId: this.academicContext.learningOutcomeId,
        };
        const specsData = {
          defaultScore: this.currentActiveQuestion.defaultScore,
          expectedTimeMinutes: this.currentActiveQuestion.expectedTimeMinutes,
          difficulty: this.currentActiveQuestion.difficulty,
          bloomLevel: this.currentActiveQuestion.bloomLevel,
        };
        localStorage.setItem("qb_last_academic_selection", JSON.stringify(academicData));
        localStorage.setItem("qb_last_question_specs", JSON.stringify(specsData));
      } catch (e) {
        console.warn("Could not save to localStorage", e);
      }
    },

    restorePersistedAcademicAndSpecs() {
      try {
        const savedSpecs = localStorage.getItem("qb_last_question_specs");
        if (savedSpecs) {
          const specs = JSON.parse(savedSpecs);
          if (specs.defaultScore) this.questions[0].defaultScore = Number(specs.defaultScore);
          if (specs.expectedTimeMinutes) this.questions[0].expectedTimeMinutes = Number(specs.expectedTimeMinutes);
          if (specs.difficulty) this.questions[0].difficulty = Number(specs.difficulty);
          if (specs.bloomLevel) this.questions[0].bloomLevel = specs.bloomLevel;
        }

        const savedAcademic = localStorage.getItem("qb_last_academic_selection");
        if (savedAcademic) {
          this.isLoadingQuestion = true;
          const acad = JSON.parse(savedAcademic);
          this.academicContext.institution_type = acad.institution_type || "school";
          this._currentActiveType = this.academicContext.institution_type;

          if (this.academicContext.institution_type === "school") {
            this.academicContext.stageId = acad.stageId ? Number(acad.stageId) : null;
            this.academicContext.classTrackId = acad.classTrackId ? Number(acad.classTrackId) : null;
            this.academicContext.subjectId = acad.subjectId ? Number(acad.subjectId) : null;
            this.academicContext.semesterId = acad.semesterId ? Number(acad.semesterId) : null;
            this._lastStageId = this.academicContext.stageId;
            this._lastClassTrackId = this.academicContext.classTrackId;
            this._lastSubjectId = this.academicContext.subjectId;
            this._lastSemesterId = this.academicContext.semesterId;
            this._lastUnitParamKey = `school_${this.academicContext.subjectId || ""}_${this.academicContext.semesterId || ""}_${this.academicContext.classTrackId || ""}_${this.academicContext.stageId || ""}`;
            this._stableUnitParam = (this.academicContext.subjectId || this.academicContext.classTrackId) ? {
              institution_type: "school",
              school_subject: this.academicContext.subjectId,
              subject: this.academicContext.subjectId,
              semester: this.academicContext.semesterId,
              class_track: this.academicContext.classTrackId,
              stage: this.academicContext.stageId,
            } : null;
          } else if (this.academicContext.institution_type === "university") {
            this.academicContext.collegeId = acad.collegeId ? Number(acad.collegeId) : null;
            this.academicContext.departmentId = acad.departmentId ? Number(acad.departmentId) : null;
            this.academicContext.specializationId = acad.specializationId ? Number(acad.specializationId) : null;
            this.academicContext.semesterSubjectId = acad.semesterSubjectId ? Number(acad.semesterSubjectId) : null;
            this._lastCollegeId = this.academicContext.collegeId;
            this._lastDepartmentId = this.academicContext.departmentId;
            this._lastSpecializationId = this.academicContext.specializationId;
            this._lastSemesterSubjectId = this.academicContext.semesterSubjectId;
            this._lastUnitParamKey = `univ_${this.academicContext.semesterSubjectId || ""}`;
            this._stableUnitParam = this.academicContext.semesterSubjectId ? { semester_subject: this.academicContext.semesterSubjectId } : null;
          } else if (this.academicContext.institution_type === "institute") {
            this.academicContext.instituteFieldId = acad.instituteFieldId ? Number(acad.instituteFieldId) : null;
            this.academicContext.instituteEducationSystemId = acad.instituteEducationSystemId ? Number(acad.instituteEducationSystemId) : null;
            this.academicContext.instituteSpecializationId = acad.instituteSpecializationId ? Number(acad.instituteSpecializationId) : null;
            this.academicContext.instituteCurriculumId = acad.instituteCurriculumId ? Number(acad.instituteCurriculumId) : null;
            this.academicContext.instituteSubjectId = acad.instituteSubjectId ? Number(acad.instituteSubjectId) : null;
            this.academicContext.subjectId = this.academicContext.instituteSubjectId;
            this._lastUnitParamKey = `inst_${this.academicContext.instituteSubjectId || ""}`;
            this._stableUnitParam = this.academicContext.instituteSubjectId ? { subject: this.academicContext.instituteSubjectId } : null;
          }

          this.academicContext.unitId = acad.unitId ? Number(acad.unitId) : null;
          this.academicContext.lessonId = acad.lessonId ? Number(acad.lessonId) : null;
          this.academicContext.learningOutcomeId = acad.learningOutcomeId ? Number(acad.learningOutcomeId) : null;
          this._lastUnitId = this.academicContext.unitId;

          setTimeout(() => {
            this.isLoadingQuestion = false;
          }, 350);
        }
      } catch (e) {
        console.warn("Could not restore from localStorage", e);
        this.isLoadingQuestion = false;
      }
    },

    // === EDIT MODE LOADER ===
    async loadQuestionForEdit(id) {
      this.saving = true;
      try {
        const data = await bankService.getQuestionDetails(id);
        const q = data?.data || data;

        const firstQ = this.questions[0];
        firstQ.text = q.content || "";
        firstQ.difficulty = q.difficulty || 2;
        firstQ.bloomLevel = q.bloomLevel || "تطبيق";
        firstQ.defaultScore = q.defaultMark || 1;
        firstQ.expectedTimeMinutes = q.expected_time_minutes || 1;
        firstQ.image = q.image || "";

        const typeMap = {
          "Single Choice": "single_choice",
          "Multiple Choice": "multiple_choice",
          "True/False": "true_false",
          "Essay": "essay",
          "Fill in the Blanks": "fill_blanks",
        };
        firstQ.type = typeMap[q.questionType] || "single_choice";

        if (q.institution_type === "institute") {
          this.academicContext.institution_type = "institute";
        } else if (q.semester_subject_id || q.college_id) {
          this.academicContext.institution_type = "university";
        } else if (q.stage_id || q.class_track_id) {
          this.academicContext.institution_type = "school";
        } else {
          this.academicContext.institution_type = q.institution_type || "school";
        }

        if (this.academicContext.institution_type === "school") {
          this.academicContext.stageId = q.stage_id ? Number(q.stage_id) : null;
          this.academicContext.classTrackId = q.class_track_id ? Number(q.class_track_id) : null;
          this.academicContext.subjectId = (q.subject_id || q.fk_subject) ? Number(q.subject_id || q.fk_subject) : null;
          this.academicContext.semesterId = q.semester_id ? Number(q.semester_id) : null;
        } else if (this.academicContext.institution_type === "institute") {
          this.academicContext.instituteFieldId = q.institute_field_id ? Number(q.institute_field_id) : null;
          this.academicContext.instituteEducationSystemId = q.institute_education_system_id ? Number(q.institute_education_system_id) : null;
          this.academicContext.instituteSpecializationId = q.institute_specialization_id ? Number(q.institute_specialization_id) : null;
          this.academicContext.instituteSubjectId = (q.institute_subject_id || q.subject_id || q.fk_subject) ? Number(q.institute_subject_id || q.subject_id || q.fk_subject) : null;
          this.academicContext.subjectId = this.academicContext.instituteSubjectId;
        } else {
          this.academicContext.collegeId = q.college_id ? Number(q.college_id) : null;
          this.academicContext.departmentId = q.department_id ? Number(q.department_id) : null;
          this.academicContext.specializationId = q.specialization_id ? Number(q.specialization_id) : null;
          this.academicContext.semesterSubjectId = q.semester_subject_id ? Number(q.semester_subject_id) : null;
          this.academicContext.semesterId = q.semester_id ? Number(q.semester_id) : null;
          this.academicContext.subjectId = (q.subject_id || q.fk_subject) ? Number(q.subject_id || q.fk_subject) : null;
        }
        this.academicContext.unitId = (q.unit_id || q.fk_unit) ? Number(q.unit_id || q.fk_unit) : null;
        this.academicContext.lessonId = q.lesson ? Number(q.lesson) : null;
        this.academicContext.learningOutcomeId = (q.learningOutcome || q.learning_outcome_id) ? Number(q.learningOutcome || q.learning_outcome_id) : null;

        const answers = q.answers || q.options || [];
        if (answers.length > 0) {
          if (firstQ.type === "single_choice") {
            firstQ.options = answers.map((a) => a.text || "");
            const correctIdx = answers.findIndex((a) => a.isTrue);
            firstQ.correctAnswerIndex = correctIdx >= 0 ? correctIdx : 0;
          } else if (firstQ.type === "multiple_choice") {
            firstQ.options = answers.map((a) => a.text || "");
            firstQ.correctAnswerIndices = answers
              .map((a, idx) => (a.isTrue ? idx : null))
              .filter((idx) => idx !== null);
          } else if (firstQ.type === "true_false") {
            const trueAns = answers.find((a) => a.text === "صواب" || a.text === "True");
            firstQ.tfCorrect = trueAns ? trueAns.isTrue : true;
          } else if (firstQ.type === "essay") {
            firstQ.options = [answers[0]?.text || ""];
          } else if (firstQ.type === "fill_blanks") {
            firstQ.options = answers.map((a) => a.text || "");
          }
        }
      } catch (err) {
        console.error("فشل في تحميل بيانات السؤال للتعديل:", err);
      } finally {
        this.saving = false;
        setTimeout(() => {
          this.isLoadingQuestion = false;
        }, 150);
      }
    },

    // === SUBMIT ALL QUESTIONS (SINGLE OR BULK ATOMIC REQUEST) ===
    async submitAllQuestions(status = "قيد المراجعة") {
      if (this.questions.length === 0) return;

      if (!this.isContextComplete) {
        this.$alert("errorData", {
          message: "يرجى إكمال تحديد المادة والوحدة والدرس في العمود الجانبي لحفظ الأسئلة",
        });
        return;
      }

      const emptyIdx = this.questions.findIndex((q) => !q.text || !q.text.trim());
      if (emptyIdx !== -1) {
        this.$alert("errorData", {
          message: `يرجى كتابة نص السؤال في السؤال رقم (${emptyIdx + 1}) قبل الحفظ`,
        });
        this.questions[emptyIdx].isCollapsed = false;
        this.activeQuestionIndex = emptyIdx;
        return;
      }

      for (let i = 0; i < this.questions.length; i++) {
        const q = this.questions[i];
        if (!this.isQuestionValid(q)) {
          this.$alert("errorData", {
            message: `يرجى إكمال بيانات وخيارات السؤال رقم (${i + 1})`,
          });
          q.isCollapsed = false;
          this.activeQuestionIndex = i;
          return;
        }
      }

      this.saving = true;
      try {
        // Edit mode: single question update
        if (this.isEditMode) {
          const q = this.questions[0];
          const optionsPayload = [];
          if (q.type === "single_choice" || q.type === "multiple_choice") {
            q.options.forEach((text, i) => {
              optionsPayload.push({
                text: text,
                isTrue: q.type === "single_choice" ? i === q.correctAnswerIndex : q.correctAnswerIndices.includes(i),
                order: i + 1,
                order_index: i,
              });
            });
          } else if (q.type === "true_false") {
            optionsPayload.push({ text: "صواب", isTrue: q.tfCorrect === true, order: 1, order_index: 0 });
            optionsPayload.push({ text: "خطأ", isTrue: q.tfCorrect === false, order: 2, order_index: 1 });
          } else if (q.type === "essay") {
            optionsPayload.push({ text: q.options[0] || "", isTrue: true, order: 1, order_index: 0 });
          } else if (q.type === "fill_blanks") {
            q.options.forEach((text, i) => {
              optionsPayload.push({ text: text, isTrue: true, order: i + 1, order_index: i });
            });
          }

          const payload = {
            content: q.text,
            questionType: this.mapQuestionType(q.type),
            status: status,
            institution_type: this.academicContext.institution_type || "school",
            lesson: this.academicContext.lessonId,
            difficulty: q.difficulty,
            bloomLevel: q.bloomLevel,
            defaultMark: q.defaultScore,
            expected_time_minutes: q.expectedTimeMinutes,
            image: q.image || null,
            options: optionsPayload,
          };

          await bankService.updateQuestion(this.editId, payload);
          this.$alert("success", { message: "تم تحديث السؤال بنجاح" });
          this.$navigateTo({ name: "question-bank", blank: false });
          return;
        }

        // Create mode: bulk create for 1 or more questions
        const questionsPayload = this.questions.map((q) => {
          const questionData = {
            content: q.text,
            image: q.image || "",
            questionType: this.mapQuestionType(q.type),
            institution_type: this.academicContext.institution_type || "school",
            difficulty: q.difficulty,
            bloomLevel: q.bloomLevel,
            defaultMark: q.defaultScore,
            expected_time_minutes: q.expectedTimeMinutes,
            status: status,
            options: [],
          };

          if (q.type === "single_choice" || q.type === "multiple_choice") {
            questionData.options = q.options.map((optText, i) => ({
              text: optText,
              isTrue: q.type === "single_choice" ? i === q.correctAnswerIndex : q.correctAnswerIndices.includes(i),
              order: i + 1,
              order_index: i,
            }));
          } else if (q.type === "true_false") {
            questionData.options = [
              { text: "صواب", isTrue: q.tfCorrect === true, order: 1, order_index: 0 },
              { text: "خطأ", isTrue: q.tfCorrect === false, order: 2, order_index: 1 },
            ];
          } else if (q.type === "essay") {
            questionData.options = [
              { text: q.options[0] || "", isTrue: true, order: 1, order_index: 0 },
            ];
          } else if (q.type === "fill_blanks") {
            questionData.options = q.options.map((optText, i) => ({
              text: optText,
              isTrue: true,
              order: i + 1,
              order_index: i,
            }));
          }

          return questionData;
        });

        const bulkPayload = {
          lesson: this.academicContext.lessonId,
          institution_type: this.academicContext.institution_type || "school",
          questions: questionsPayload,
        };

        await bankService.fastBulkCreateQuestions(bulkPayload);

        this.persistAcademicAndSpecs();
        const successMsg = this.questions.length === 1
          ? "تم حفظ السؤال بنجاح"
          : `تم حفظ جميع الأسئلة (${this.questions.length}) بنجاح`;
        this.$alert("success", { message: successMsg });
        this.$navigateTo({ name: "question-bank", blank: false });
      } catch (err) {
        this.$alert("errorData", { message: "حدث خطأ أثناء حفظ السؤال" });
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
  transition: all 0.25s ease;
}

.main-card:hover {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05), 0 8px 24px rgba(0, 0, 0, 0.03);
}

.question-block-item {
  border: 1.5px solid rgba(var(--v-border-color), 0.1);
  transition: all 0.25s ease;
}

.question-block--active {
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
  box-shadow: 0 4px 20px rgba(var(--v-theme-primary), 0.07) !important;
}

/* ===== Type Selector Grid (The 5 Large Color Cards from Screenshot) ===== */
.type-selector-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
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
  background: rgba(245, 158, 11, 0.06) !important;
  border: 1.5px solid rgba(245, 158, 11, 0.3) !important;
}
.type-card-warning:hover {
  background: rgba(245, 158, 11, 0.12) !important;
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
  background: rgba(var(--v-theme-primary), 0.06) !important;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.3) !important;
}
.type-card-primary:hover {
  background: rgba(var(--v-theme-primary), 0.12) !important;
  border-color: rgba(var(--v-theme-primary), 0.6) !important;
  box-shadow: 0 6px 20px rgba(var(--v-theme-primary), 0.15) !important;
}

.type-card-deep-purple {
  background: rgba(124, 58, 237, 0.06) !important;
  border: 1.5px solid rgba(124, 58, 237, 0.3) !important;
}
.type-card-deep-purple:hover {
  background: rgba(124, 58, 237, 0.12) !important;
  border-color: rgba(124, 58, 237, 0.6) !important;
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.15) !important;
}

.type-option-card--active.type-card-indigo {
  background: rgb(99, 102, 241) !important;
  border-color: rgb(99, 102, 241) !important;
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.35) !important;
}
.type-option-card--active.type-card-warning {
  background: rgb(245, 158, 11) !important;
  border-color: rgb(245, 158, 11) !important;
  box-shadow: 0 8px 24px rgba(245, 158, 11, 0.35) !important;
}
.type-option-card--active.type-card-success {
  background: rgb(16, 185, 129) !important;
  border-color: rgb(16, 185, 129) !important;
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.35) !important;
}
.type-option-card--active.type-card-primary {
  background: rgb(var(--v-theme-primary)) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.35) !important;
}
.type-option-card--active.type-card-deep-purple {
  background: rgb(124, 58, 237) !important;
  border-color: rgb(124, 58, 237) !important;
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.35) !important;
}

/* ===== True/False Interactive Cards ===== */
.tf-option-card {
  background: rgb(var(--v-theme-background));
  border: 1.5px solid rgba(var(--v-border-color), 0.12);
  border-radius: 8px !important;
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

/* ===== Segmented Control for Difficulty ===== */
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

/* ===== Compact Helper Image Styles ===== */
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

/* ===== Option Letter Badges ===== */
.option-letter-badge {
  width: 36px;
  height: 36px;
  min-width: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  border-radius: 8px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
}
.option-letter--default {
  background: rgba(var(--v-theme-primary), 0.07);
  color: rgb(var(--v-theme-primary));
  border: 1.5px solid rgba(var(--v-theme-primary), 0.25);
  font-weight: 800;
}
.option-letter--default:hover {
  background: rgba(var(--v-theme-primary), 0.14);
  border-color: rgb(var(--v-theme-primary));
}
.option-letter--correct {
  background: rgb(var(--v-theme-success)) !important;
  color: #ffffff !important;
  border: 1px solid rgb(var(--v-theme-success));
  box-shadow: 0 2px 8px rgba(var(--v-theme-success), 0.3);
}

/* Option Formula Live Preview */
.option-formula-preview {
  background: rgba(var(--v-theme-primary), 0.04);
  border: 1px dashed rgba(var(--v-theme-primary), 0.25);
  border-radius: 8px;
  color: rgb(var(--v-theme-on-surface));
}
.option-row-wrap {
  border-radius: 12px;
  padding: 4px 6px;
  transition: all 0.2s ease;
}
.option-row--targeted {
  background: rgba(var(--v-theme-primary), 0.05);
  border: 1.5px dashed rgba(var(--v-theme-primary), 0.45);
  box-shadow: 0 0 0 2px rgba(var(--v-theme-primary), 0.08);
}

/* ===== Gap Utilities ===== */
.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
</style>
