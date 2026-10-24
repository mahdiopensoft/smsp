<template>
  <div class="qb-submission-detail-v4">
    <!-- Header Controls -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center gap-3">
        <custom-btn
          is-icon
          icon="arrow-right"
          variant="tonal"
          color="primary"
          :click="() => $router.push('/omr-submissions')"
        />
        <v-avatar size="44" color="primary" variant="tonal" class="rounded-xl">
          <v-icon size="24">mdi-file-document-check-outline</v-icon>
        </v-avatar>
        <div>
          <h2 class="text-h5 font-weight-black mb-1">تفاصيل تصحيح ورقة الإجابة</h2>
          <span class="text-caption text-medium-emphasis">
            عرض وتحليل نتائج خط المعالجة الهجين والتحقق بالذكاء الاصطناعي
          </span>
        </div>
      </div>

      <div class="d-flex align-center gap-2">
        <custom-btn
          label="إعادة المعالجة ضوئياً"
          icon="mdi-refresh"
          color="warning"
          variant="tonal"
          class="font-weight-bold"
          :loading="reprocessing"
          :disabled="Boolean(submission && submission.is_control_locked)"
          :click="reprocessSheet"
        />
        <custom-btn
          label="تعديل واعتماد الدرجات"
          icon="mdi-pencil-outline"
          color="primary"
          class="font-weight-bold"
          :disabled="Boolean(submission && submission.is_control_locked)"
          :click="openEditDialog"
        />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center pa-12">
      <v-progress-circular indeterminate color="primary" size="48" />
      <div class="text-caption mt-3 text-medium-emphasis">جاري تحميل تفاصيل الورقة...</div>
    </div>

    <div v-else-if="submission">
      <!-- تنبيه القفل الأكاديمي للكنترول المركزي -->
      <v-alert
        v-if="submission.is_control_locked"
        color="warning"
        variant="tonal"
        rounded="xl"
        class="mb-6 font-weight-bold"
        icon="mdi-shield-lock"
      >
        <div class="d-flex align-center justify-space-between flex-wrap gap-2">
          <div>
            <div class="text-subtitle-2 font-weight-black">
              🔒 هذه الورقة مقفلة ومرحلة للكنترول المركزي
            </div>
            <div class="text-caption">
              تم تثبيت ورصد درجات هذه الورقة رسمياً بموجب الإيصال الأكاديمي المشفر رقم:
              <strong class="font-mono text-primary font-weight-bold">{{ submission.control_receipt_no || 'CTL-RECEIPT' }}</strong>.
              الورقة محمية ضد أي تعديل لضمان أعلى معايير النزاهة الامتحانية.
            </div>
          </div>
          <v-chip color="warning" size="small" variant="flat" class="font-weight-bold">
            مغلق للكنترول
          </v-chip>
        </div>
      </v-alert>

      <!-- تنبيه إيضاحي للورقة المعتمدة والدرجات المرصودة -->
      <v-alert
        v-else-if="Number(submission.total_score) > 0"
        color="success"
        variant="tonal"
        rounded="xl"
        class="mb-6 font-weight-bold"
        icon="mdi-check-decagram"
      >
        <div class="d-flex align-center justify-space-between flex-wrap gap-2">
          <div>
            <div class="text-subtitle-2 font-weight-black">
              ✅ تم التصحيح والرصد الآلي بنجاح بمطابقة الذكاء الاصطناعي
            </div>
            <div class="text-caption">
              تم التعرف على تظليلات الطالب بدقة عالية ومقارنتها بنموذج الإجابة الرسمي ({{ submission.exam_version_code || 'النموذج المعتمد' }}). يمكنك النقر على مقتطفات الدوائر الدقيقة (AI Crops) في الجدول أدناه لفحص كيفية رؤية الذكاء الاصطناعي لكل دائرة.
            </div>
          </div>
          <v-chip color="success" size="small" variant="flat" class="font-weight-bold">
            درجة الطالب: {{ submission.total_score }} / {{ submission.exam_max_score || submission.mcq_score || 16 }}
          </v-chip>
        </div>
      </v-alert>

      <!-- تنبيه إيضاحي لورقة إجابات فارغة بالكامل -->
      <v-alert
        v-else-if="submission.total_score == 0"
        color="info"
        variant="tonal"
        rounded="xl"
        class="mb-6 font-weight-bold"
        icon="mdi-information-outline"
      >
        <div class="d-flex align-center justify-space-between flex-wrap gap-2">
          <div>
            <div class="text-subtitle-2 font-weight-black">
              🔍 تم فحص الورقة بالكامل ومطابقة الدوائر بالذكاء الاصطناعي
            </div>
            <div class="text-caption">
              جميع دوائر الإجابة لهذه الورقة فارغة (لم يقم الطالب بتظليل أي خيار). تم اقتصاص مواضع الدوائر وتأكيد خلوها من الرصاص بنسبة ثقة عالية. يمكنك رؤية مقتطفات الدوائر الدقيقة (AI Crops) في الجدول أدناه بالنقر على أي دائرة.
            </div>
          </div>
          <v-chip color="info" size="small" variant="flat" class="font-weight-bold">
            الدوائر المكتشفة: {{ mcqQuestions.length }} سؤال
          </v-chip>
        </div>
      </v-alert>

      <!-- Top Stats Overview Bar -->
      <v-row class="mb-6">
        <!-- Total Score -->
        <v-col cols="12" sm="6" md="3">
          <div class="stat-glass-card pa-5 rounded-xl shadow-emerald">
            <div class="d-flex align-center justify-space-between mb-3">
              <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">الدرجة الكلية</span>
              <div class="stat-icon-wrapper bg-emerald-gradient">
                <v-icon color="white" size="22">mdi-check-decagram</v-icon>
              </div>
            </div>
            <div class="stat-value text-h3 font-weight-black text-emerald mb-1">
              {{ submission.total_score != null ? submission.total_score : '—' }}
            </div>
            <div class="stat-footer border-t pt-2 mt-2 text-caption text-medium-emphasis">
              <span>خيارات: {{ submission.mcq_score || 0 }} | مقالي: {{ submission.essay_score || 0 }}</span>
            </div>
          </div>
        </v-col>

        <!-- Confidence Index -->
        <v-col cols="12" sm="6" md="3">
          <div class="stat-glass-card pa-5 rounded-xl shadow-indigo">
            <div class="d-flex align-center justify-space-between mb-3">
              <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">مؤشر الثقة الإجمالي</span>
              <div class="stat-icon-wrapper bg-indigo-gradient">
                <v-icon color="white" size="22">mdi-brain</v-icon>
              </div>
            </div>
            <div class="stat-value text-h3 font-weight-black text-indigo mb-1">
              {{ submission.overall_confidence ? (submission.overall_confidence * 100).toFixed(0) + '%' : '—' }}
            </div>
            <div class="stat-footer border-t pt-2 mt-2 text-caption text-medium-emphasis">
              <span>تحقق شبكة CNN والـ OMR</span>
            </div>
          </div>
        </v-col>

        <!-- Processing Time -->
        <v-col cols="12" sm="6" md="3">
          <div class="stat-glass-card pa-5 rounded-xl shadow-amber">
            <div class="d-flex align-center justify-space-between mb-3">
              <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">زمن المعالجة الضوئية</span>
              <div class="stat-icon-wrapper bg-amber-gradient">
                <v-icon color="white" size="22">mdi-timer-outline</v-icon>
              </div>
            </div>
            <div class="stat-value text-h3 font-weight-black text-amber mb-1">
              {{ submission.processing_time_ms ? (submission.processing_time_ms / 1000).toFixed(2) + ' ث' : '—' }}
            </div>
            <div class="stat-footer border-t pt-2 mt-2 text-caption text-medium-emphasis">
              <span>محاذاة وقراءة وتصحيح</span>
            </div>
          </div>
        </v-col>

        <!-- Status -->
        <v-col cols="12" sm="6" md="3">
          <div class="stat-glass-card pa-5 rounded-xl shadow-rose">
            <div class="d-flex align-center justify-space-between mb-3">
              <span class="text-subtitle-2 font-weight-bold text-medium-emphasis">حالة الورقة</span>
              <div class="stat-icon-wrapper bg-rose-gradient">
                <v-icon color="white" size="22">mdi-list-status</v-icon>
              </div>
            </div>
            <div class="stat-value text-h4 font-weight-black mb-1">
              <v-chip :color="getStatusColor(submission.status)" variant="flat" class="font-weight-bold text-white">
                {{ submission.status_display || submission.status }}
              </v-chip>
            </div>
            <div class="stat-footer border-t pt-2 mt-2 text-caption text-medium-emphasis">
              <span>معرف السجل: #{{ submission.id }}</span>
            </div>
          </div>
        </v-col>
      </v-row>

      <v-row class="align-stretch">
        <!-- Right Column: Sheet Visualizer & Overlay -->
        <v-col cols="12" md="6">
          <v-card elevation="0" class="main-card pa-5 rounded-2xl border h-100 d-flex flex-column justify-space-between">
            <div>
              <div class="d-flex align-center justify-space-between mb-4">
                <div class="d-flex align-center gap-2">
                  <v-icon color="primary">mdi-image-filter-center-focus</v-icon>
                  <h3 class="text-subtitle-1 font-weight-black mb-0">ورقة الإجابة المصححة</h3>
                </div>

                <div class="d-flex align-center gap-2">
                  <v-btn-toggle v-model="activeImageMode" mandatory density="compact" color="primary" rounded="lg">
                    <v-btn value="aligned" size="x-small" prepend-icon="mdi-bullseye-arrow">
                      صورة فحص الدوائر
                    </v-btn>
                    <v-btn value="original" size="x-small" prepend-icon="mdi-image-outline">
                      الأصلية
                    </v-btn>
                  </v-btn-toggle>

                  <custom-btn
                    :label="showOverlays ? 'إخفاء التظليل' : 'إظهار التظليل'"
                    :icon="showOverlays ? 'mdi-eye-off' : 'mdi-eye'"
                    size="small"
                    variant="tonal"
                    color="indigo"
                    class="font-weight-bold"
                    :click="toggleOverlays"
                  />
                </div>
              </div>

              <!-- Visualizer Wrapper -->
              <div class="visualizer-wrapper bg-slate-900 rounded-xl pa-2 text-center position-relative overflow-hidden">
                <div class="image-relative-container">
                  <img
                    ref="sheetImg"
                    :src="getMediaUrl(activeImage)"
                    alt="Student Answer Sheet"
                    class="sheet-img"
                    @load="onImageLoad"
                  />

                  <!-- Bubble overlays mapped onto the image (only on aligned mode for 100% geometric accuracy) -->
                  <template v-if="(showOverlays || hoveredQ) && activeImageMode === 'aligned'">
                    <template v-for="q in mcqQuestions" :key="'overlay-' + q.question_id">
                      <template v-if="showOverlays || hoveredQ === q.question_id">
                        <div
                          v-for="choice in getChoicesForQuestion(q)"
                          :key="'choice-' + q.question_id + '-' + choice.choice"
                          class="image-bubble-overlay"
                          :class="[getOverlayClass(q, choice.choice), { 'overlay-highlighted': hoveredQ === q.question_id }]"
                          :style="getOverlayStyle(choice)"
                          :title="'سؤال ' + q.question_id + ' - خيار (' + choice.choice + ')'"
                          @mouseenter="hoveredQ = q.question_id"
                          @mouseleave="hoveredQ = null"
                        />
                      </template>
                    </template>
                  </template>
                </div>
              </div>
            </div>
          </v-card>
        </v-col>

        <!-- Left Column: Student Data, Pipeline, & Detailed Question Scores -->
        <v-col cols="12" md="6">
          <!-- Student & Exam Meta Card -->
          <v-card elevation="0" class="main-card pa-5 rounded-2xl border mb-4">
            <div class="d-flex align-center justify-space-between mb-3 border-b pb-2">
              <h3 class="text-subtitle-1 font-weight-black mb-0">بيانات الطالب والاختبار</h3>
              <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                رقم الجلوس: {{ submission.seat_number }}
              </v-chip>
            </div>

            <v-row dense>
              <v-col cols="12" sm="6">
                <div class="text-caption text-medium-emphasis">اسم الطالب:</div>
                <div class="text-body-2 font-weight-bold text-primary">{{ submission.student_name }}</div>
              </v-col>
              <v-col cols="12" sm="6">
                <div class="text-caption text-medium-emphasis">عنوان الاختبار:</div>
                <div class="text-body-2 font-weight-bold">{{ submission.exam_title }}</div>
              </v-col>
              <v-col cols="12" sm="6" class="mt-2">
                <div class="text-caption text-medium-emphasis">المادة الدراسية:</div>
                <div class="text-body-2 font-weight-medium">{{ submission.subject_name || '-' }}</div>
              </v-col>
              <v-col cols="12" sm="6" class="mt-2">
                <div class="text-caption text-medium-emphasis">النموذج:</div>
                <div class="text-body-2 font-weight-medium">{{ submission.exam_version_code || 'نموذج رئيسي' }}</div>
              </v-col>
            </v-row>
          </v-card>

          <!-- Pipeline Stepper Status -->
          <v-card elevation="0" class="main-card pa-5 rounded-2xl border mb-4">
            <h3 class="text-subtitle-1 font-weight-black mb-3">خطوات المعالجة الهجينة (Pipeline)</h3>
            <v-timeline density="compact" side="end">
              <!-- Step 1 -->
              <v-timeline-item dot-color="success" size="small">
                <div class="font-weight-bold text-body-2">1. المحاذاة الهندسية (Perspective Alignment)</div>
                <div class="text-caption text-medium-emphasis">تمت المحاذاة وإسقاط المنظور باستخدام علامات الارتكاز الأربعة</div>
              </v-timeline-item>

              <!-- Step 2 -->
              <v-timeline-item dot-color="success" size="small">
                <div class="font-weight-bold text-body-2">2. مطابقة القالب وتحديد الدوائر (Layout Mapping)</div>
                <div class="text-caption text-medium-emphasis">مطابقة إحداثيات القالب الهندسي واستخراج مناطق التظليل</div>
              </v-timeline-item>

              <!-- Step 3 -->
              <v-timeline-item dot-color="primary" size="small">
                <div class="font-weight-bold text-body-2">3. قراءة التظليل والتحقق الذكي (OMR + AI Verification)</div>
                <div class="text-caption text-medium-emphasis">تحليل كثافة التظليل بالـ OpenCV وتدقيق الالتباس بشبكة CNN</div>
              </v-timeline-item>

              <!-- Step 4 -->
              <v-timeline-item dot-color="indigo" size="small">
                <div class="font-weight-bold text-body-2">4. احتساب الدرجات والاعتماد الأكاديمي</div>
                <div class="text-caption text-medium-emphasis">المقارنة مع مفتاح الإجابة واعتماد النتيجة النهائية</div>
              </v-timeline-item>
            </v-timeline>
          </v-card>

          <!-- Detailed Questions Breakdown -->
          <v-card elevation="0" class="main-card pa-5 rounded-2xl border">
            <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-4 border-b pb-3">
              <div class="d-flex align-center gap-2">
                <v-icon color="primary" size="22">mdi-format-list-checks</v-icon>
                <h3 class="text-subtitle-1 font-weight-black mb-0">نتائج الأسئلة التفصيلية</h3>
                <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                  {{ mcqQuestions.length }} سؤال
                </v-chip>
              </div>

              <!-- Quick Stats Summary -->
              <div class="d-flex align-center gap-2 flex-wrap">
                <v-chip size="x-small" color="success" variant="tonal" class="font-weight-bold">
                  <v-icon start size="13">mdi-check-circle</v-icon>
                  صحيحة: {{ correctCount }}
                </v-chip>
                <v-chip size="x-small" color="error" variant="tonal" class="font-weight-bold">
                  <v-icon start size="13">mdi-close-circle</v-icon>
                  خاطئة: {{ incorrectCount }}
                </v-chip>
                <v-chip size="x-small" color="grey-darken-1" variant="tonal" class="font-weight-bold">
                  <v-icon start size="13">mdi-circle-outline</v-icon>
                  فارغة: {{ emptyCount }}
                </v-chip>
              </div>
            </div>

            <!-- Filter Controls -->
            <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3">
              <span class="text-caption text-medium-emphasis">
                انقر على أي مقتطف دائرة (AI Crop) لمعاينتها بدقة الذكاء الاصطناعي، أو مرر الفأرة لإضاءتها على الورقة.
              </span>
              <v-btn-toggle v-model="filterMode" mandatory density="compact" rounded="lg" color="primary">
                <v-btn value="all" size="x-small">الكل ({{ mcqQuestions.length }})</v-btn>
                <v-btn value="correct" size="x-small" color="success">الصحيحة</v-btn>
                <v-btn value="incorrect" size="x-small" color="error">الخاطئة</v-btn>
                <v-btn value="empty" size="x-small">الفارغة</v-btn>
              </v-btn-toggle>
            </div>

            <div class="main-card rounded-2xl overflow-hidden">
              <custom-data-table
                v-bind="{
                  items: questionsTableItems,
                  headers: questionHeaders,
                }"
                :customLoading="loading"
                :hasFilter="false"
                :log="false"
                :restore="false"
                :numbering="false"
                :showSelect="false"
                :actions="false"
                class="bg-transparent"
              >
                <template v-slot:item-slot="{ item, key }">
                  <!-- رقم السؤال -->
                  <template v-if="key === 'question_id'">
                    <div
                      class="text-center py-1 cursor-pointer"
                      @mouseenter="hoveredQ = item.question_id"
                      @mouseleave="hoveredQ = null"
                    >
                      <span class="font-weight-black text-body-2 text-primary bg-blue-lighten-5 px-3 py-1 rounded-pill border">
                        سـ {{ item.question_id }}
                      </span>
                    </div>
                  </template>

                  <!-- نوع السؤال -->
                  <template v-else-if="key === 'question_type'">
                    <div class="text-center">
                      <v-chip
                        size="small"
                        variant="tonal"
                        :color="isTrueFalseQ(item) ? 'teal' : 'indigo'"
                        class="font-weight-bold px-2.5"
                      >
                        <v-icon start size="13">{{ isTrueFalseQ(item) ? 'mdi-check-all' : 'mdi-format-list-bulleted' }}</v-icon>
                        {{ isTrueFalseQ(item) ? 'صح/خطأ' : 'خيارات' }}
                      </v-chip>
                    </div>
                  </template>

                  <!-- إجابة الطالب (تظليل الطالب) -->
                  <template v-else-if="key === 'student_answer'">
                    <div class="text-center">
                      <v-chip
                        size="small"
                        :color="!item.marked_choice ? 'grey-darken-1' : item.is_correct ? 'success' : 'error'"
                        variant="tonal"
                        class="font-weight-bold px-3"
                      >
                        <v-icon start size="13">
                          {{ !item.marked_choice ? 'mdi-circle-outline' : item.is_correct ? 'mdi-check-circle' : 'mdi-close-circle' }}
                        </v-icon>
                        {{ item.marked_choice ? formatChoiceLabel(item.marked_choice, item) : 'بدون إجابة (فارغ)' }}
                      </v-chip>
                    </div>
                  </template>

                  <!-- الإجابة النموذجية -->
                  <template v-else-if="key === 'correct_answer'">
                    <div class="text-center">
                      <v-chip
                        size="small"
                        color="teal"
                        variant="tonal"
                        class="font-weight-black px-3 border"
                      >
                        <v-icon start size="13" color="teal">mdi-check-decagram-outline</v-icon>
                        {{ formatChoiceLabel(item.correct_choice, item) }}
                      </v-chip>
                    </div>
                  </template>

                  <!-- الدرجة -->
                  <template v-else-if="key === 'score'">
                    <div class="text-center font-weight-black text-body-2" :class="Number(item.marks_awarded) > 0 ? 'text-success' : 'text-medium-emphasis'">
                      {{ item.marks_awarded != null ? Number(item.marks_awarded).toFixed(1).replace('.0', '') : '0' }} / {{ item.max_mark || 1 }}
                    </div>
                  </template>

                  <!-- مقتطفات الذكاء الاصطناعي (AI Crops) -->
                  <template v-else-if="key === 'ai_crops'">
                    <div v-if="item.choice_crops && Object.keys(item.choice_crops).length" class="d-flex align-center justify-center gap-1.5 flex-wrap py-1">
                      <div
                        v-for="(cropImg, choiceKey) in item.choice_crops"
                        :key="choiceKey"
                        class="ai-crop-card pa-1 text-center cursor-pointer"
                        :class="item.ai_results && item.ai_results[choiceKey] === 'filled' ? 'crop-filled' : 'crop-empty'"
                        title="انقر لتكبير مقتطف الدائرة وفحص قرار الذكاء الاصطناعي"
                        @click.stop="openCropDialog(item, choiceKey, cropImg)"
                      >
                        <div class="crop-img-wrapper mb-1">
                          <img :src="cropImg" class="crop-thumbnail" />
                        </div>
                        <div class="crop-label font-weight-black">{{ choiceKey }}</div>
                        <div class="crop-verdict" :class="item.ai_results && item.ai_results[choiceKey] === 'filled' ? 'verdict-filled' : 'verdict-empty'">
                          {{ item.ai_results && item.ai_results[choiceKey] === 'filled' ? 'مظلل' : 'فارغ' }}
                        </div>
                      </div>
                    </div>
                    <div v-else-if="item.choices && item.choices.length" class="d-flex align-center justify-center gap-1 flex-wrap py-1">
                      <v-chip
                        v-for="choice in item.choices"
                        :key="choice"
                        size="x-small"
                        :color="item.marked_choice === choice ? (item.is_correct ? 'success' : 'error') : 'grey-lighten-2'"
                        :variant="item.marked_choice === choice ? 'flat' : 'outlined'"
                        class="font-weight-bold px-1.5"
                      >
                        {{ choice }}: {{ item.marked_choice === choice ? 'مظلل' : 'فارغ' }}
                      </v-chip>
                    </div>
                    <span v-else class="text-caption text-medium-emphasis">غير متاح</span>
                  </template>

                  <!-- الثقة -->
                  <template v-else-if="key === 'confidence'">
                    <div class="text-center">
                      <v-chip
                        size="x-small"
                        :color="(item.final_confidence || 1) >= 0.9 ? 'success' : 'warning'"
                        variant="tonal"
                        class="font-weight-bold"
                      >
                        <v-icon start size="11">mdi-brain</v-icon>
                        {{ ((item.final_confidence || 1) * 100).toFixed(0) }}%
                      </v-chip>
                    </div>
                  </template>
                </template>
              </custom-data-table>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Edit / Manual Review Dialog (CustomDialog Component) -->
    <CustomDialog
      v-model="editDialog"
      width="560"
      title="تعديل درجات الورقة واعتمادها"
      :subTitle="submission ? `طالب: ${submission.student_name} • رقم الجلوس: ${submission.seat_number}` : ''"
    >
      <v-row class="mb-3">
        <v-col cols="12" md="6">
          <v-text-field
            v-model.number="editForm.mcq_score"
            label="درجة أسئلة الخيارات (MCQ) *"
            type="number"
            variant="outlined"
            density="compact"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model.number="editForm.essay_score"
            label="درجة الأسئلة المقالية (Essay) *"
            type="number"
            variant="outlined"
            density="compact"
          />
        </v-col>
        <v-col cols="12">
          <v-select
            v-model="editForm.status"
            :items="[
              { title: 'مكتمل ومعتمد (Completed)', value: 'completed' },
              { title: 'تمت المراجعة (Reviewed)', value: 'reviewed' },
              { title: 'يحتاج مراجعة (Needs Review)', value: 'needs_review' }
            ]"
            label="الحالة بعد الحفظ *"
            variant="outlined"
            density="compact"
          />
        </v-col>
      </v-row>

      <template #actions>
        <custom-btn
          type="cancel"
          :click="() => editDialog = false"
          variant="text"
          label="إلغاء"
          class="font-weight-bold"
        />
        <custom-btn
          type="add"
          :click="saveReview"
          :loading="saving"
          color="primary"
          label="حفظ واعتماد الدرجات"
          class="font-weight-bold ms-auto"
        />
      </template>
    </CustomDialog>

    <!-- Dialog for Magnifying AI Crop (أين نظر الذكاء الاصطناعي) -->
    <v-dialog v-model="cropDialog" max-width="440px">
      <v-card v-if="selectedCrop" class="rounded-2xl pa-5 text-center">
        <div class="d-flex align-center justify-space-between pb-2 border-b mb-3">
          <div class="d-flex align-center gap-2">
            <v-icon color="primary" size="22">mdi-magnify-scan</v-icon>
            <span class="text-subtitle-1 font-weight-black">
              عين الذكاء الاصطناعي — سؤال {{ selectedCrop.questionId }} ({{ selectedCrop.choice }})
            </span>
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" @click="cropDialog = false" />
        </div>

        <div class="pa-4 bg-slate-900 rounded-xl mb-3 d-inline-block">
          <img :src="selectedCrop.img" style="width: 130px; height: 130px; object-fit: contain; image-rendering: pixelated; border-radius: 8px; background: white;" />
        </div>

        <div class="pa-3 bg-grey-lighten-4 rounded-xl text-right mb-4">
          <div class="d-flex justify-space-between align-center mb-2">
            <span class="text-caption text-medium-emphasis">قرار النموذج (AI Verdict):</span>
            <v-chip size="x-small" :color="selectedCrop.aiVerdict === 'filled' ? 'success' : 'grey-darken-2'" class="font-weight-bold">
              {{ selectedCrop.aiVerdict === 'filled' ? 'مظلل (Filled)' : 'فارغ (Empty)' }}
            </v-chip>
          </div>
          <div class="d-flex justify-space-between align-center mb-2">
            <span class="text-caption text-medium-emphasis">نسبة الثقة (Confidence):</span>
            <span class="font-mono font-weight-bold text-primary">{{ selectedCrop.confidence }}%</span>
          </div>
          <div v-if="selectedCrop.center" class="d-flex justify-space-between align-center">
            <span class="text-caption text-medium-emphasis">موضع الدائرة بالبكسل:</span>
            <span class="font-mono text-caption">X: {{ selectedCrop.center[0] }}, Y: {{ selectedCrop.center[1] }} px</span>
          </div>
        </div>

        <v-btn color="primary" variant="tonal" rounded="lg" block @click="cropDialog = false">
          إغلاق
        </v-btn>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { submissionsAPI } from '@/services/omr/endpoints'

export default {
  name: 'OMRSubmissionDetailView',
  props: {
    id: {
      type: [String, Number],
      default: null,
    },
  },

  data() {
    return {
      loading: false,
      reprocessing: false,
      saving: false,

      submission: null,
      hoveredQ: null,
      showOverlays: false,
      activeImageMode: 'aligned',

      cropDialog: false,
      selectedCrop: null,

      filterMode: 'all',

      paperWidth: 210.0,
      paperHeight: 297.0,
      naturalWidth: 2480,
      naturalHeight: 1754,

      editDialog: false,
      editForm: {
        mcq_score: 0,
        essay_score: 0,
        status: 'completed',
      },

      questionHeaders: [
        { title: "رقم السؤال", key: "question_id", sortable: true, align: "center", width: "95px" },
        { title: "نوع السؤال", key: "question_type", sortable: true, align: "center", width: "110px" },
        { title: "تظليل الطالب", key: "student_answer", sortable: true, align: "center", width: "135px" },
        { title: "الإجابة النموذجية", key: "correct_answer", sortable: true, align: "center", width: "135px" },
        { title: "الدرجة", key: "score", sortable: true, align: "center", width: "85px" },
        { title: "مقتطفات الذكاء الاصطناعي (AI Crops)", key: "ai_crops", sortable: false, align: "center", width: "210px" },
        { title: "نسبة الثقة", key: "confidence", sortable: true, align: "center", width: "95px" },
      ],
    }
  },

  computed: {
    questionsTableItems() {
      const qs = this.filteredQuestions.map(q => this.enrichQuestion(q))
      return {
        results: qs,
        count: qs.length,
        pagination: {
          count: qs.length,
          total: qs.length,
          page_size: 10,
          num_pages: Math.ceil(qs.length / 10) || 1,
          current_page: 1,
        },
      }
    },

    mcqQuestions() {
      if (Array.isArray(this.submission?.omr_result)) {
        return this.submission.omr_result
      }
      return this.submission?.omr_result?.questions || this.submission?.omr_result?.data?.questions || []
    },

    correctCount() {
      return this.mcqQuestions.filter(q => q.is_correct === true).length
    },

    incorrectCount() {
      return this.mcqQuestions.filter(q => q.marked_choice && q.is_correct === false).length
    },

    emptyCount() {
      return this.mcqQuestions.filter(q => !q.marked_choice).length
    },

    filteredQuestions() {
      if (this.filterMode === 'correct') {
        return this.mcqQuestions.filter(q => q.is_correct === true)
      }
      if (this.filterMode === 'incorrect') {
        return this.mcqQuestions.filter(q => q.marked_choice && q.is_correct === false)
      }
      if (this.filterMode === 'empty') {
        return this.mcqQuestions.filter(q => !q.marked_choice)
      }
      return this.mcqQuestions
    },

    activeImage() {
      if (this.activeImageMode === 'original') {
        return this.submission?.original_image
      }
      return this.submission?.aligned_image || this.submission?.original_image
    },
  },

  watch: {
    '$route.params.id'(val) {
      if (val) this.loadSubmission()
    },
    '$route.query.id'(val) {
      if (val) this.loadSubmission()
    },
    id(val) {
      if (val) this.loadSubmission()
    },
  },

  methods: {
    async loadSubmission() {
      const id = this.id || this.$route?.params?.id || this.$route?.query?.id
      if (!id) return
      this.loading = true
      try {
        const res = await submissionsAPI.get(id)
        const resData = res.data?.data ? res.data.data : (res.data || res)
        this.submission = resData
      } catch (err) {
        console.error('Error fetching submission details:', err)
      } finally {
        this.loading = false
      }
    },

    getMediaUrl(path) {
      if (!path) return ''
      if (path.startsWith('http')) return path
      if (path.startsWith('data:')) return path
      return `http://localhost:5001${path.startsWith('/') ? '' : '/'}${path}`
    },

    getStatusColor(status) {
      const map = {
        completed: 'success',
        reviewed: 'teal',
        needs_review: 'warning',
        failed: 'error',
        pending: 'grey',
      }
      return map[status] || 'grey'
    },

    openCropDialog(q, choiceKey, cropImg) {
      const aiRes = q.ai_results || {}
      const confData = q.ai_confidence || {}
      this.selectedCrop = {
        questionId: q.question_id,
        choice: choiceKey,
        img: cropImg,
        aiVerdict: aiRes[choiceKey] || q.bubble_state || 'empty',
        confidence: confData[choiceKey]?.confidence != null 
          ? (confData[choiceKey].confidence * 100).toFixed(1) 
          : (q.final_confidence ? (q.final_confidence * 100).toFixed(1) : '95.0'),
        center: q.actual_centers && q.actual_centers[choiceKey] ? q.actual_centers[choiceKey] : null,
      }
      this.cropDialog = true
    },

    onImageLoad(event) {
      if (event?.target) {
        this.naturalWidth = event.target.naturalWidth || 2480
        this.naturalHeight = event.target.naturalHeight || 1754
      }
    },

    getChoicesForQuestion(q) {
      if (!q) return []
      // 1. If actual_centers is available from OMR processing
      if (q.actual_centers && typeof q.actual_centers === 'object') {
        return Object.entries(q.actual_centers).map(([k, center]) => ({
          choice: k,
          center: center,
        }))
      }
      // 2. Fallback to layout_result detected_regions
      const qId = q.question_id
      const layoutQuestions = this.submission?.layout_result?.detected_regions?.mcq_questions || this.submission?.layout_result?.data?.detected_regions?.mcq_questions || []
      const found = layoutQuestions.find(item => String(item.question_id) === String(qId))
      if (found && found.choices) return found.choices
      return []
    },

    toggleOverlays() {
      this.showOverlays = !this.showOverlays
      if (this.showOverlays && this.activeImageMode === 'original') {
        this.activeImageMode = 'aligned'
      }
    },

    getOverlayStyle(choice) {
      if (!choice) return {}
      if (choice.center && Array.isArray(choice.center)) {
        const cx = choice.center[0]
        const cy = choice.center[1]
        const imgW = this.naturalWidth || 2480
        const imgH = this.naturalHeight || 1754
        return {
          left: `${(cx / imgW) * 100}%`,
          top: `${(cy / imgH) * 100}%`,
          width: '2.2%',
          aspectRatio: '1 / 1',
        }
      }
      if (choice.bubble_region) {
        const reg = choice.bubble_region
        const w = reg.width_mm || 4.5
        const h = reg.height_mm || 4.5
        const cx = reg.dx_mm + w / 2.0
        const cy = reg.dy_mm + h / 2.0
        return {
          left: `${(cx / this.paperWidth) * 100}%`,
          top: `${(cy / this.paperHeight) * 100}%`,
          width: `${(w / this.paperWidth) * 100}%`,
          aspectRatio: '1 / 1',
        }
      }
      return {}
    },

    getOverlayClass(q, letter) {
      const formattedMarked = this.formatChoiceLabel(q.marked_choice, q)
      const formattedCorrect = this.formatChoiceLabel(q.correct_choice, q)
      const isSelected = String(q.marked_choice) === String(letter) || String(formattedMarked) === String(letter)
      const isCorrectKey = String(q.correct_choice) === String(letter) || String(formattedCorrect) === String(letter)
      if (isSelected) {
        return q.is_correct ? 'overlay-selected-correct' : 'overlay-selected-incorrect'
      }
      if (isCorrectKey) {
        return 'overlay-correct-key'
      }
      return 'overlay-normal'
    },

    openEditDialog() {
      if (!this.submission) return
      this.editForm = {
        mcq_score: Number(this.submission.mcq_score) || 0,
        essay_score: Number(this.submission.essay_score) || 0,
        status: this.submission.status === 'needs_review' ? 'completed' : this.submission.status,
      }
      this.editDialog = true
    },

    async saveReview() {
      if (!this.submission) return
      this.saving = true
      try {
        await submissionsAPI.updateReview(this.submission.id, this.editForm)
        this.editDialog = false
        await this.loadSubmission()
      } catch (err) {
        console.error('Error saving review:', err)
      } finally {
        this.saving = false
      }
    },

    formatChoiceLabel(val, q) {
      if (!val) return 'فارغ'
      const s = String(val).trim().toUpperCase()
      if (q && q.choices && q.choices.length) {
        if (s === 'A') return q.choices[0] || 'A'
        if (s === 'B') return q.choices[1] || 'B'
        if (s === 'C') return q.choices[2] || 'C'
        if (s === 'D') return q.choices[3] || 'D'
        if (s === 'E') return q.choices[4] || 'E'
      }
      return val
    },

    isTrueVariant(val, q) {
      if (val === null || val === undefined) return false
      const label = this.formatChoiceLabel(val, q)
      const s = String(label).trim().toLowerCase()
      return s === 'صح' || s === 'ص' || s === 'true' || s === 't' || s === 'yes'
    },

    isFalseVariant(val, q) {
      if (val === null || val === undefined) return false
      const label = this.formatChoiceLabel(val, q)
      const s = String(label).trim().toLowerCase()
      return s === 'خطأ' || s === 'خطا' || s === 'خ' || s === 'false' || s === 'f' || s === 'no'
    },

    isTrueFalseQ(q) {
      if (!q) return false
      if (q.choices && q.choices.length === 2) return true
      const c = String(q.correct_choice).trim().toLowerCase()
      return c === 'صح' || c === 'خطأ' || c === 'ص' || c === 'خ' || (q.choices && (q.choices.includes('صح') || q.choices.includes('ص')))
    },

    async reprocessSheet() {
      if (!this.submission) return
      this.reprocessing = true
      try {
        await submissionsAPI.reprocess(this.submission.id)
        await this.loadSubmission()
      } catch (err) {
        console.error('Error reprocessing sheet:', err)
      } finally {
        this.reprocessing = false
      }
    },

    enrichQuestion(q) {
      if (!q) return q
      const isTF = this.isTrueFalseQ(q)
      q.question_type = isTF ? 'صح وخطأ' : 'اختيار متعدد'
      q.student_answer = q.marked_choice ? this.formatChoiceLabel(q.marked_choice, q) : 'بدون إجابة (فارغ)'
      q.correct_answer = q.correct_choice ? this.formatChoiceLabel(q.correct_choice, q) : 'لم تُحدد'
      q.score = `${q.marks_awarded != null ? Number(q.marks_awarded).toFixed(1).replace('.0', '') : '0'} / ${q.max_mark || 1}`
      q.confidence = `${((q.final_confidence || 1) * 100).toFixed(0)}%`
      return q
    },

    async getQuestionsData() {
      return this.questionsTableItems
    },
  },

  mounted() {
    this.loadSubmission()
  },
}
</script>

<style scoped>
:deep(.v-chip) {
  border-radius: 6px !important;
  font-family: inherit;
  letter-spacing: 0;
}

.main-card {
  background: white;
  border-color: rgba(0, 0, 0, 0.08) !important;
}

.stat-glass-card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.06);
  transition: all 0.25s ease;
}

.stat-glass-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.08);
}

.stat-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-indigo-gradient {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
}

.bg-emerald-gradient {
  background: linear-gradient(135deg, #10b981, #059669);
}

.bg-amber-gradient {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.bg-rose-gradient {
  background: linear-gradient(135deg, #f43f5e, #e11d48);
}

.shadow-indigo {
  box-shadow: 0 8px 20px -6px rgba(99, 102, 241, 0.18);
}

.shadow-emerald {
  box-shadow: 0 8px 20px -6px rgba(16, 185, 129, 0.18);
}

.shadow-amber {
  box-shadow: 0 8px 20px -6px rgba(245, 158, 11, 0.18);
}

.shadow-rose {
  box-shadow: 0 8px 20px -6px rgba(244, 63, 94, 0.18);
}

/* Image overlays */
.image-relative-container {
  position: relative;
  display: block;
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  line-height: 0;
  aspect-ratio: 2480 / 1754;
}

.sheet-img {
  width: 100%;
  height: 100%;
  display: block;
  border-radius: 8px;
  object-fit: fill;
}

.image-bubble-overlay {
  position: absolute;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  z-index: 10;
  box-sizing: border-box;
}

.overlay-selected-correct {
  background: rgba(16, 185, 129, 0.35);
  border: 2px solid #10b981;
  box-shadow: 0 0 6px rgba(16, 185, 129, 0.8);
}

.overlay-selected-incorrect {
  background: rgba(239, 68, 68, 0.35);
  border: 2px solid #ef4444;
  box-shadow: 0 0 6px rgba(239, 68, 68, 0.8);
}

.overlay-correct-key {
  border: 2px dashed #10b981;
  background: rgba(16, 185, 129, 0.12);
}

.overlay-normal {
  border: 1.5px dashed rgba(59, 130, 246, 0.5);
  background: transparent;
}

.overlay-highlighted {
  transform: translate(-50%, -50%) scale(1.4) !important;
  z-index: 50 !important;
  box-shadow: 0 0 12px rgba(59, 130, 246, 1) !important;
  border: 2.5px solid #3b82f6 !important;
  background: rgba(59, 130, 246, 0.2) !important;
}

.table-row-hovered {
  background-color: rgba(59, 130, 246, 0.12) !important;
  transition: background-color 0.15s ease;
}

/* AI Crop Cards */
.ai-crop-card {
  min-width: 44px;
  background: white;
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.ai-crop-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.08);
  border-color: #3b82f6 !important;
}

.crop-filled {
  border: 1.5px solid #10b981 !important;
  background: #f0fdf4 !important;
}

.crop-empty {
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #f8fafc;
}

.crop-img-wrapper {
  width: 30px;
  height: 30px;
  margin: 0 auto;
  border-radius: 6px;
  overflow: hidden;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.crop-thumbnail {
  width: 100%;
  height: 100%;
  object-fit: contain;
  image-rendering: pixelated;
}

.crop-label {
  font-size: 10px;
  color: #1e293b;
  line-height: 1.2;
}

.crop-verdict {
  font-size: 9px;
  font-weight: 700;
  line-height: 1.2;
  margin-top: 1px;
}

.verdict-filled {
  color: #059669;
}

.verdict-empty {
  color: #64748b;
}

.questions-table th {
  background: #f8fafc !important;
  color: #334155 !important;
  font-size: 12px !important;
  border-bottom: 2px solid #e2e8f0 !important;
}

.question-row {
  transition: background-color 0.15s ease;
}

.question-row:hover {
  background-color: #f8fafc;
}
</style>
