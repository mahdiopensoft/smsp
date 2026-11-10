<template>
  <div class="qb-submission-detail-v4 pa-3 pa-md-5">
    <!-- Loading State -->
    <div v-if="loading" class="text-center pa-12">
      <v-progress-circular indeterminate color="primary" size="44" />
      <div class="text-caption mt-3 text-medium-emphasis">جاري تحميل وتدقيق تفاصيل الورقة...</div>
    </div>

    <div v-else-if="submission">
      <!-- Master Executive Header Card (شريط الترويسة والبيانات المعتمدة الموحد) -->
      <div class="header-master-card pa-3 px-4 rounded-xl border bg-surface mb-3">
        <div class="d-flex flex-column flex-lg-row align-start align-lg-center justify-space-between gap-3">
          <!-- Right: Back Arrow + Approved Primary Avatar + Student & Exam Manifest -->
          <div class="d-flex align-center gap-3">
            <custom-btn
              is-icon
              icon="arrow-right"
              variant="tonal"
              color="primary"
              title="الرجوع لسجل أوراق الإجابة"
              :click="() => $router.push('/omr-submissions')"
            />
            <v-avatar size="44" color="primary" variant="tonal" class="rounded-lg flex-shrink-0">
              <v-icon size="24" color="primary">mdi-account-school-outline</v-icon>
            </v-avatar>
            <div>
              <div class="d-flex align-center gap-2 flex-wrap">
                <h1 class="text-subtitle-1 font-weight-black text-on-surface mb-0">
                  {{ submission.student_name || 'طالب غير محدد (تعذر قراءة الباركود)' }}
                </h1>
                <span class="seat-badge font-mono text-caption px-2 py-0.5 rounded font-weight-bold">
                  جلوس: <bdi>{{ submission.seat_number || '—' }}</bdi>
                </span>
                <v-chip size="x-small" variant="tonal" color="primary" class="font-mono font-weight-bold">
                  #{{ submission.id }}
                </v-chip>
              </div>
              <div class="text-caption text-medium-emphasis d-flex align-center gap-2 mt-0.5 flex-wrap">
                <span>
                  {{ submission.institution_type === 'school' ? 'مدرسة' : 'مركز' }}:
                  {{ submission.school_name || submission.exam_center || 'المركز الامتحاني العام' }}
                </span>
                <span>•</span>
                <span class="text-primary font-weight-bold">
                  {{ submission.subject_name || submission.exam_title || 'مادة الاختبار' }}
                </span>
                <span>•</span>
                <span class="font-weight-bold">
                  {{ submission.exam_version_code || 'نموذج A' }}
                </span>
                <template v-if="submission.layout_result?.barcode || submission.layout_result?.qr">
                  <span>•</span>
                  <span class="font-mono text-medium-emphasis d-inline-flex align-center">
                    <v-icon size="13" class="me-1">mdi-barcode-scan</v-icon>
                    <bdi>{{ submission.layout_result?.barcode || submission.layout_result?.qr }}</bdi>
                  </span>
                </template>
              </div>
            </div>
          </div>

          <!-- Left: Submission Status + Quick Navigation + Primary Actions -->
          <div class="d-flex align-center gap-2 flex-wrap ms-auto ms-lg-0">
            <!-- Submission Status Badge -->
            <v-chip
              size="small"
              :color="getStatusColor(submission.status)"
              variant="flat"
              class="font-weight-bold text-white"
            >
              <v-icon start size="14">
                {{ submission.is_control_locked ? 'mdi-shield-lock' : (submission.status === 'completed' || submission.status === 'reviewed' ? 'mdi-check-decagram' : 'mdi-alert-circle-outline') }}
              </v-icon>
              {{ submission.status_display || submission.status }}
            </v-chip>

            <!-- Sheet Pagination Between Submissions -->
            <div class="d-flex align-center border rounded-lg px-1 py-0.5 bg-surface">
              <v-btn
                icon="mdi-chevron-right"
                variant="text"
                size="small"
                density="comfortable"
                title="الورقة السابقة"
                :disabled="!submission || Number(submission.id) <= 1"
                @click="goToPreviousSubmission"
              />
              <span class="text-caption font-mono font-weight-bold px-1 text-medium-emphasis">
                <bdi>#{{ submission ? submission.id : '—' }}</bdi>
              </span>
              <v-btn
                icon="mdi-chevron-left"
                variant="text"
                size="small"
                density="comfortable"
                title="الورقة التالية"
                :disabled="!submission"
                @click="goToNextSubmission"
              />
            </div>

            <!-- Reprocess Button -->
            <custom-btn
              label="إعادة المعالجة ضوئياً"
              icon="mdi-refresh"
              color="primary"
              variant="outlined"
              class="font-weight-bold"
              :loading="reprocessing"
              :disabled="Boolean(submission && submission.is_control_locked)"
              :click="reprocessSheet"
            />

            <!-- Edit / Approve Button -->
            <custom-btn
              label="تعديل واعتماد الدرجات"
              icon="mdi-pencil-outline"
              color="primary"
              variant="flat"
              class="font-weight-bold"
              :disabled="Boolean(submission && submission.is_control_locked)"
              :click="openEditDialog"
            />
          </div>
        </div>
      </div>

      <!-- Integrated Audit & Filter Strip (شريط التدقيق الإحصائي والتصفية الموحد) -->
      <div class="audit-toolbar-strip pa-2.5 px-4 rounded-xl border bg-surface mb-4">
        <div class="d-flex align-center justify-space-between flex-wrap gap-3">
          <!-- Right side: Score Metric -->
          <div class="d-flex align-center gap-2">
            <v-avatar size="32" color="primary" variant="tonal" class="rounded-lg flex-shrink-0">
              <v-icon size="18" color="primary">mdi-star-check-outline</v-icon>
            </v-avatar>
            <div class="d-flex align-baseline gap-1">
              <span class="text-caption text-medium-emphasis">الدرجة الكلية:</span>
              <span class="d-inline-flex align-baseline gap-1" dir="ltr">
                <span class="font-mono font-weight-black text-body-1 text-primary">
                  {{ submission.total_score != null ? submission.total_score : '—' }}
                </span>
                <span class="text-caption text-medium-emphasis">/ {{ maxExamScore }}</span>
              </span>
              <v-chip size="x-small" color="primary" variant="tonal" class="font-mono font-weight-bold ms-1" dir="ltr">
                {{ scorePercent }}%
              </v-chip>
            </div>
          </div>

          <!-- Left side: Filter Mode Toggles -->
          <div class="d-flex align-center gap-2 flex-wrap ms-auto">
            <v-btn-toggle v-model="filterMode" mandatory density="compact" rounded="lg" color="primary">
              <v-btn value="all" size="x-small">الكل ({{ mcqQuestions.length }})</v-btn>
              <v-btn value="correct" size="x-small" color="success">الصحيحة ({{ correctCount }})</v-btn>
              <v-btn value="incorrect" size="x-small" color="error">الخاطئة ({{ incorrectCount }})</v-btn>
              <v-btn v-if="emptyCount > 0" value="empty" size="x-small">الفارغة ({{ emptyCount }})</v-btn>
            </v-btn-toggle>
          </div>
        </div>
      </div>

      <!-- Verification Workspace: Side-by-Side Split -->
      <v-row class="align-stretch">
        <!-- Right Column: Sheet Visualizer & Overlay (lg="5" with Sticky positioning) -->
        <v-col cols="12" lg="5">
          <v-card elevation="0" class="main-card pa-4 rounded-xl border sticky-visualizer-card">
            <div>
              <div class="d-flex align-center justify-space-between mb-3">
                <div class="d-flex align-center gap-2">
                  <v-avatar size="34" color="primary" variant="tonal" class="rounded-lg">
                    <v-icon size="20" color="primary">mdi-image-filter-center-focus</v-icon>
                  </v-avatar>
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
                    color="primary"
                    class="font-weight-bold"
                    :click="toggleOverlays"
                  />
                </div>
              </div>

              <!-- Visualizer Wrapper -->
              <div class="visualizer-wrapper bg-slate-900 rounded-xl pa-2 text-center position-relative overflow-hidden">
                <div v-if="activeImage" class="image-relative-container">
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

                <!-- رسالة توضيحية عندما لا تحتوي الورقة على ملف صورة ممسوح ضوئياً -->
                <div v-else class="pa-10 text-center text-white">
                  <v-icon size="64" color="blue-grey-lighten-3" class="mb-3">mdi-image-off-outline</v-icon>
                  <h4 class="text-subtitle-1 font-weight-black mb-1">ورقة الإجابة لا تتضمن ملف صورة مرفوع</h4>
                  <p class="text-caption text-blue-grey-lighten-3 mb-4 mx-auto" style="max-width: 380px;">
                    تم إنشاء درجات وسجلات هذه الورقة ضمن بيانات المحاكاة التجريبية (Seeder) لاختبار مادة التاريخ دون رفع صورة ماسح ضوئي.
                  </p>
                  <div class="d-flex align-center justify-center gap-2">
                    <v-btn
                      color="primary"
                      variant="elevated"
                      size="small"
                      prepend-icon="mdi-file-eye-outline"
                      class="font-weight-bold"
                      @click="$router.push('/omr-submissions/36')"
                    >
                      استعراض ورقة مصححة ومفحوصة بالذكاء الاصطناعي (رقم 36)
                    </v-btn>
                  </div>
                </div>
              </div>
            </div>
          </v-card>
        </v-col>

        <!-- Left Column: Detailed Questions & AI Inspection (lg="7") -->
        <v-col cols="12" lg="7">
          <v-card elevation="0" class="main-card pa-4 rounded-xl border">
            <!-- Questions Card Header -->
            <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3 border-b pb-3">
              <div class="d-flex align-center gap-2">
                <v-avatar size="34" color="primary" variant="tonal" class="rounded-lg">
                  <v-icon size="20" color="primary">mdi-format-list-checks</v-icon>
                </v-avatar>
                <div>
                  <h3 class="text-subtitle-1 font-weight-black mb-0">جدول تدقيق الأسئلة والذكاء الاصطناعي</h3>
                  <span class="text-caption text-medium-emphasis">
                    عرض {{ filteredQuestions.length }} من إجمالي {{ mcqQuestions.length }} سؤال
                  </span>
                </div>
              </div>

              <div class="d-flex align-center gap-2">
                <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                  <v-icon start size="12">mdi-check-all</v-icon>
                  استدلال YOLOv8 و CNN الهجين
                </v-chip>
              </div>
            </div>

            <!-- Table of Questions -->
            <div class="main-card rounded-xl overflow-hidden">
              <custom-data-table
                v-bind="{
                  items: questionsTableItems,
                  getData: getQuestionsData,
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
                      <span class="q-number-badge font-weight-black text-caption font-mono px-2.5 py-1 rounded-md">
                        سـ <bdi>{{ item.question_id }}</bdi>
                      </span>
                    </div>
                  </template>

                  <!-- نوع السؤال -->
                  <template v-else-if="key === 'question_type'">
                    <div class="text-center">
                      <v-chip
                        size="small"
                        variant="tonal"
                        :color="isTrueFalseQ(item) ? 'teal' : 'primary'"
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
                        <bdi>{{ item.marked_choice ? formatChoiceLabel(item.marked_choice, item) : 'بدون إجابة (فارغ)' }}</bdi>
                      </v-chip>
                    </div>
                  </template>

                  <!-- الإجابة النموذجية -->
                  <template v-else-if="key === 'correct_answer'">
                    <div class="text-center">
                      <v-chip
                        size="small"
                        color="primary"
                        variant="tonal"
                        class="font-weight-black px-3 border"
                      >
                        <v-icon start size="13" color="primary">mdi-key-outline</v-icon>
                        <bdi>{{ formatChoiceLabel(item.correct_choice, item) }}</bdi>
                      </v-chip>
                    </div>
                  </template>

                  <!-- الدرجة -->
                  <template v-else-if="key === 'score'">
                    <div class="text-center font-weight-black font-mono text-body-2" :class="Number(item.marks_awarded) > 0 ? 'text-success' : 'text-medium-emphasis'" dir="ltr">
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
                        class="font-weight-bold font-mono"
                      >
                        <v-icon start size="11">mdi-brain</v-icon>
                        <bdi>{{ ((item.final_confidence || 1) * 100).toFixed(0) }}%</bdi>
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

    <!-- Dialog for Magnifying AI Crop (عين الذكاء الاصطناعي — فحص التظليل) -->
    <v-dialog v-model="cropDialog" max-width="460px">
      <v-card v-if="selectedCrop" class="rounded-2xl overflow-hidden main-card border elevation-3">
        <!-- Header -->
        <div class="d-flex align-center justify-space-between px-5 py-3 border-b bg-surface">
          <div class="d-flex align-center gap-2">
            <v-avatar color="primary" variant="tonal" size="34" rounded="lg">
              <v-icon color="primary" size="20">mdi-eye-check-outline</v-icon>
            </v-avatar>
            <div>
              <div class="text-subtitle-2 font-weight-black text-high-emphasis d-flex align-center gap-1.5">
                <span>عين الذكاء الاصطناعي</span>
                <span class="text-medium-emphasis">•</span>
                <span>سؤال {{ selectedCrop.questionId }}</span>
                <div class="unified-inspection-badge px-2 py-0.5 font-weight-black text-caption">
                  {{ selectedCrop.choice }}
                </div>
              </div>
              <div class="text-caption text-medium-emphasis">فحص بصري دقيق للدائرة الملتقطة بالماسح الضوئي</div>
            </div>
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" density="comfortable" @click="cropDialog = false" />
        </div>

        <!-- Viewfinder Visual Box -->
        <div class="pa-5 text-center bg-surface-variant-subtle border-b">
          <div class="ai-viewfinder-box mx-auto position-relative">
            <!-- Inspection Crosshair Guides -->
            <div class="viewfinder-crosshair-h"></div>
            <div class="viewfinder-crosshair-v"></div>

            <!-- Crisp Bubble Image -->
            <img
              :src="selectedCrop.img"
              alt="Bubble Crop"
              class="ai-bubble-image"
            />

            <!-- Corner Brackets -->
            <div class="bracket-tl"></div>
            <div class="bracket-tr"></div>
            <div class="bracket-bl"></div>
            <div class="bracket-br"></div>

            <!-- Top Tag -->
            <div class="viewfinder-tag top-tag">
              <v-icon size="11" class="me-1">mdi-crosshairs-gps</v-icon>
              <span>تكبير فحص 300 DPI</span>
            </div>
          </div>
        </div>

        <!-- Metric Details Panel -->
        <div class="pa-5 bg-surface">
          <div class="d-flex flex-column gap-2.5">
            <!-- قرار النموذج (AI Verdict) -->
            <div class="d-flex justify-space-between align-center px-3 py-2 rounded-lg border bg-surface-variant-subtle">
              <div class="d-flex align-center gap-1.5 text-caption font-weight-medium text-medium-emphasis">
                <v-icon size="16" color="primary">mdi-shield-check-outline</v-icon>
                <span>قرار النموذج (AI Verdict):</span>
              </div>
              <div
                class="unified-inspection-badge px-2.5 py-1 text-caption font-weight-black"
                :class="selectedCrop.aiVerdict === 'filled' ? 'badge-verdict-filled' : 'badge-verdict-empty'"
              >
                <v-icon start size="13" class="me-1">
                  {{ selectedCrop.aiVerdict === 'filled' ? 'mdi-checkbox-marked-circle' : 'mdi-checkbox-blank-circle-outline' }}
                </v-icon>
                {{ selectedCrop.aiVerdict === 'filled' ? 'مظلل (Filled)' : 'فارغ (Empty)' }}
              </div>
            </div>

            <!-- نسبة الثقة (Confidence) -->
            <div class="d-flex justify-space-between align-center px-3 py-2 rounded-lg border bg-surface-variant-subtle">
              <div class="d-flex align-center gap-1.5 text-caption font-weight-medium text-medium-emphasis">
                <v-icon size="16" color="primary">mdi-chart-bell-curve-cumulative</v-icon>
                <span>نسبة الثقة (Confidence):</span>
              </div>
              <div class="d-flex align-center gap-2">
                <v-progress-linear
                  :model-value="Number(selectedCrop.confidence) || 0"
                  color="primary"
                  height="6"
                  rounded
                  style="width: 70px;"
                />
                <span class="font-mono font-weight-black text-body-2 text-primary">
                  {{ selectedCrop.confidence }}%
                </span>
              </div>
            </div>

            <!-- موضع الدائرة بالبكسل -->
            <div v-if="selectedCrop.center" class="d-flex justify-space-between align-center px-3 py-2 rounded-lg border bg-surface-variant-subtle">
              <div class="d-flex align-center gap-1.5 text-caption font-weight-medium text-medium-emphasis">
                <v-icon size="16" color="primary">mdi-map-marker-radius-outline</v-icon>
                <span>موضع الدائرة بالبكسل:</span>
              </div>
              <div class="unified-inspection-badge font-mono text-caption px-2 py-0.5">
                X: {{ selectedCrop.center[0] }}, Y: {{ selectedCrop.center[1] }} px
              </div>
            </div>
          </div>

          <!-- Bottom Close Button -->
          <div class="mt-4 pt-2 border-t d-flex justify-end">
            <v-btn
              color="primary"
              variant="flat"
              rounded="lg"
              class="font-weight-bold px-6"
              prepend-icon="mdi-check"
              @click="cropDialog = false"
            >
              تم الفحص وإغلاق
            </v-btn>
          </div>
        </div>
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
      questionSearchQuery: '',
      questionsPage: 1,
      questionsPageSize: 25,

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
      const total = qs.length
      const pageSize = this.questionsPageSize || 10
      const numPages = Math.ceil(total / pageSize) || 1
      const validPage = Math.min(Math.max(1, this.questionsPage), numPages)
      const start = (validPage - 1) * pageSize

      return {
        results: qs.slice(start, start + pageSize),
        count: total,
        pagination: {
          count: total,
          total: total,
          page_size: pageSize,
          num_pages: numPages,
          current_page: validPage,
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
      let list = this.mcqQuestions
      if (this.filterMode === 'correct') {
        list = list.filter(q => q.is_correct === true)
      } else if (this.filterMode === 'incorrect') {
        list = list.filter(q => q.marked_choice && q.is_correct === false)
      } else if (this.filterMode === 'empty') {
        list = list.filter(q => !q.marked_choice)
      }
      if (this.questionSearchQuery && this.questionSearchQuery.trim()) {
        const query = this.questionSearchQuery.trim().toLowerCase()
        list = list.filter(q => String(q.question_id).includes(query))
      }
      return list
    },

    activeImage() {
      if (this.activeImageMode === 'original') {
        return this.submission?.original_image
      }
      return this.submission?.aligned_image || this.submission?.original_image
    },

    maxExamScore() {
      return this.submission?.layout_result?.max_score || this.submission?.exam_max_score || this.mcqQuestions.length || 50
    },

    scorePercent() {
      if (this.submission?.layout_result?.score_percent != null) {
        return Number(this.submission.layout_result.score_percent).toFixed(1).replace('.0', '')
      }
      const total = Number(this.submission?.total_score) || 0
      const max = this.maxExamScore || 1
      return ((total / max) * 100).toFixed(1).replace('.0', '')
    },

    confidencePercent() {
      const conf = this.submission?.overall_confidence
      if (conf != null) {
        return (Number(conf) * 100).toFixed(0)
      }
      return '95'
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
    filterMode() {
      this.questionsPage = 1
    },
    questionSearchQuery() {
      this.questionsPage = 1
    },
  },

  methods: {
    goToPreviousSubmission() {
      const currentId = Number(this.id || this.$route?.params?.id || this.submission?.id)
      if (currentId > 1) {
        this.$router.push(`/omr-submissions/${currentId - 1}`)
      }
    },

    goToNextSubmission() {
      const currentId = Number(this.id || this.$route?.params?.id || this.submission?.id)
      if (currentId) {
        this.$router.push(`/omr-submissions/${currentId + 1}`)
      }
    },

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

    async getQuestionsData(params = {}) {
      const p = params?.params || params || {}
      if (p.page) this.questionsPage = Number(p.page) || 1
      if (p.page_size) this.questionsPageSize = Number(p.page_size) || 25
      if (p.search !== undefined) this.questionSearchQuery = p.search || ''
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

.header-master-card,
.audit-toolbar-strip,
.main-card {
  background: white;
  border-color: rgba(0, 0, 0, 0.08) !important;
}

.seat-badge {
  background: rgba(var(--v-theme-primary), 0.08);
  color: rgb(var(--v-theme-primary));
  border: 1px solid rgba(var(--v-theme-primary), 0.2);
}

.q-number-badge {
  background: rgba(var(--v-theme-primary), 0.08);
  color: rgb(var(--v-theme-primary));
  border: 1px solid rgba(var(--v-theme-primary), 0.2);
  display: inline-block;
  min-width: 44px;
  transition: all 0.15s ease;
}

.q-number-badge:hover {
  background: rgba(var(--v-theme-primary), 0.16);
  border-color: rgb(var(--v-theme-primary));
}

/* Sticky Visualizer on Large Screens */
@media (min-width: 1264px) {
  .sticky-visualizer-card {
    position: sticky;
    top: 20px;
    z-index: 10;
  }
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

/* AI Crop Viewfinder */
.ai-viewfinder-box {
  width: 170px;
  height: 170px;
  background: #0f172a;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: inset 0 2px 12px rgba(0, 0, 0, 0.6);
  position: relative;
  overflow: hidden;
}

.ai-bubble-image {
  width: 125px;
  height: 125px;
  object-fit: contain;
  image-rendering: pixelated;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
  z-index: 2;
}

.viewfinder-crosshair-h {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: rgba(var(--v-theme-primary), 0.35);
  z-index: 3;
  pointer-events: none;
}

.viewfinder-crosshair-v {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 1px;
  background: rgba(var(--v-theme-primary), 0.35);
  z-index: 3;
  pointer-events: none;
}

.bracket-tl, .bracket-tr, .bracket-bl, .bracket-br {
  position: absolute;
  width: 12px;
  height: 12px;
  border-color: rgb(var(--v-theme-primary));
  border-style: solid;
  z-index: 4;
}
.bracket-tl { top: 6px; left: 6px; border-width: 2px 0 0 2px; }
.bracket-tr { top: 6px; right: 6px; border-width: 2px 2px 0 0; }
.bracket-bl { bottom: 6px; left: 6px; border-width: 0 0 2px 2px; }
.bracket-br { bottom: 6px; right: 6px; border-width: 0 2px 2px 0; }

.viewfinder-tag {
  position: absolute;
  top: 8px;
  right: 20px;
  font-size: 10px;
  background: rgba(15, 23, 42, 0.88);
  color: rgb(var(--v-theme-primary));
  padding: 1px 7px;
  border-radius: 4px;
  border: 1px solid rgba(var(--v-theme-primary), 0.3);
  z-index: 5;
  font-family: monospace;
}

.unified-inspection-badge {
  display: inline-flex;
  align-items: center;
  background: rgba(var(--v-theme-primary), 0.1);
  color: rgb(var(--v-theme-primary));
  border: 1px solid rgba(var(--v-theme-primary), 0.25);
  border-radius: 6px !important;
}

.badge-verdict-filled {
  background: rgba(var(--v-theme-primary), 0.12) !important;
  color: rgb(var(--v-theme-primary)) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.3) !important;
}

.badge-verdict-empty {
  background: rgba(100, 116, 139, 0.12) !important;
  color: #64748b !important;
  border: 1px solid rgba(100, 116, 139, 0.25) !important;
}
</style>
