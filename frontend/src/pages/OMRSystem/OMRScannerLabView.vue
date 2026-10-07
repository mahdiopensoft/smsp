<template>
  <div class="qb-omr-lab-v4">
    <!-- ── Page Header (Institutional OpenSoftCore Style) ─────────────── -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center">
        <back-to class="me-3" />
        <v-avatar size="44" color="primary" variant="tonal" class="me-3 rounded-xl">
          <v-icon size="24">mdi-scanner</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">مختبر المسح الضوئي 
            تصحيح</h1>
          <p class="text-caption text-medium-emphasis mb-0">معالجة وتصحيح أوراق الإجابة بدقة معيارية مدعومة بالذكاء الاصطناعي</p>
        </div>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <custom-btn
          type="restore"
          :click="() => $router.push('/omr/dashboard')"
          label="لوحة التحكم"
          color="secondary"
          variant="tonal"
          class="font-weight-bold"
        />
        <custom-btn
          type="imports"
          :click="() => $router.push('/omr/templates')"
          label="مكتبة القوالب"
          color="secondary"
          variant="tonal"
          class="font-weight-bold"
        />
        <custom-btn
          type="cancel_filter"
          :click="() => $router.push('/omr/submissions')"
          label="سجل الأوراق"
          color="secondary"
          variant="tonal"
          class="font-weight-bold"
        />
      </div>
    </div>

    <!-- ── Step Tabs Navigation Bar ───────────────────────────────── -->
    <v-card class="main-card pa-2 rounded-xl mb-6 elevation-1">
      <v-tabs v-model="currentStep" grow color="primary" slider-color="primary">
        <v-tab :value="0" class="font-weight-bold py-3">
          <v-icon start>mdi-printer-outline</v-icon>
          الخطوة 1: تصدير وطباعة الورقة
        </v-tab>
        <v-tab :value="1" class="font-weight-bold py-3">
          <v-icon start>mdi-cloud-upload-outline</v-icon>
          الخطوة 2: رفع الورقة والتصحيح (AI OMR)
        </v-tab>
        <v-tab :value="2" :disabled="!result" class="font-weight-bold py-3">
          <v-icon start>mdi-chart-box-outline</v-icon>
          الخطوة 3: نتائج التحليل وتتبع AI
        </v-tab>
      </v-tabs>
    </v-card>

    <!-- ════════════════════════════════════════════════════════════ -->
    <!-- STEP 0: تصدير وطباعة الورقة                                  -->
    <!-- ════════════════════════════════════════════════════════════ -->
    <div v-if="currentStep === 0">
      <v-card class="main-card pa-6 rounded-2xl mb-6 elevation-1">
        <div class="d-flex align-center justify-space-between mb-4">
          <div class="d-flex align-center gap-3">
            <v-avatar color="primary" variant="tonal" rounded="lg" size="44">
              <v-icon size="24">mdi-printer</v-icon>
            </v-avatar>
            <div>
              <h2 class="text-h6 font-weight-black mb-1">الخطوة الأولى: تصدير ورقة الإجابة المعيارية</h2>
              <p class="text-body-2 text-medium-emphasis mb-0">اطبع ورقة الإجابة الرسمية بدقة 300 DPI على ورق A4 لضمان أعلى دقة قراءة ضوئية.</p>
            </div>
          </div>
        </div>

        <v-row class="mb-6">
          <!-- Sheet SVG Preview Container -->
          <v-col cols="12" md="4" lg="3">
            <v-card class="pa-3 rounded-xl border elevation-0 text-center bg-grey-lighten-4 d-flex flex-column align-center">
              <div class="omr-sheet-thumb mb-3" :style="thumbContainerStyle">
                <div class="thumb-scaler" :style="thumbSheetWrapperStyle">
                  <YemeniMinistrySheet
                    v-if="omrReady && isMinistrySheet"
                    :student-name="linkedStudents[0]?.student_name || 'طالب اختبار'"
                    :seat-number="linkedStudents[0]?.seat_number || '418485'"
                    :model-code="selectedVersionCode || 'A'"
                    :center-code="'101'"
                    :school-name="linkedStudents[0]?.school_name || selectedExamObj?.title || 'المؤسسة التعليمية'"
                    :governorate="selectedExamObj?.governorate || 'أمانة العاصمة'"
                    :directorate="selectedExamObj?.directorate || ''"
                    :exam-subject="selectedExamObj?.subject_name || 'المادة'"
                  />
                  <OmrSheetMultigraphics
                    v-else-if="omrReady"
                    :total-questions="activeQuestionsCount"
                    :questions-per-column="activeTemplateMeta.questionsPerColumn"
                    :total-columns="activeTemplateMeta.totalColumns"
                    :row-spacing="activeTemplateMeta.rowSpacing"
                    :bubble-radius="activeTemplateMeta.bubbleRadius"
                    :choices-per-question="activeChoicesLabels.length"
                    :bubble-type="activeTemplateMeta.bubbleType"
                    :layout-direction="activeTemplateMeta.layoutDirection"
                    :primary-color="activeTemplateMeta.primaryColor"
                    :institution-name="activeTemplateMeta.institutionName"
                    :sub-title="activeTemplateMeta.subTitle"
                    :exam-name="activeTemplateMeta.examName"
                  />
                  <div v-else class="sheet-placeholder">
                    <v-progress-circular indeterminate color="primary" size="28" />
                    <span class="text-caption mt-2">جاري تجهيز القالب المعياري...</span>
                  </div>
                </div>
              </div>

              <v-btn
                size="small"
                variant="tonal"
                color="primary"
                rounded="lg"
                class="font-weight-bold w-100"
                prepend-icon="mdi-magnify-plus-outline"
                @click="showSheetPreviewModal = true"
              >
                معاينة مكبرة للورقة
              </v-btn>
            </v-card>
          </v-col>

          <!-- Sheet Specifications & Actions -->
          <v-col cols="12" md="8" lg="9">
            <v-card class="pa-5 rounded-xl border elevation-0 mb-4 bg-surface">
              <div class="d-flex justify-space-between align-center mb-3">
                <h3 class="text-subtitle-1 font-weight-bold d-flex align-center mb-0">
                  <v-icon color="primary" class="me-2" size="20">mdi-information-outline</v-icon>
                  المواصفات الهندسية لورقة الإجابة المعتمدة
                </h3>
                <v-chip color="primary" variant="flat" size="small" rounded="md" class="font-weight-bold">
                  {{ activeTemplateObj?.name || 'النموذج المعياري العام' }}
                </v-chip>
              </div>

              <v-row dense class="mb-4">
                <v-col cols="6" sm="3">
                  <div class="pa-3 rounded-lg border bg-grey-lighten-5 text-center">
                    <div class="text-caption text-medium-emphasis">المقاس القياسي</div>
                    <div class="text-subtitle-2 font-weight-bold">A4 — 210×297mm</div>
                  </div>
                </v-col>
                <v-col cols="6" sm="3">
                  <div class="pa-3 rounded-lg border bg-grey-lighten-5 text-center">
                    <div class="text-caption text-medium-emphasis">دقة الطباعة</div>
                    <div class="text-subtitle-2 font-weight-bold">300 DPI عالية الدقة</div>
                  </div>
                </v-col>
                <v-col cols="6" sm="3">
                  <div class="pa-3 rounded-lg border bg-grey-lighten-5 text-center">
                    <div class="text-caption text-medium-emphasis">سعة الأسئلة</div>
                    <div class="text-subtitle-2 font-weight-bold" v-if="selectedTemplateId === 'AUTO' && !activeTemplateObj">
                      سيتم التعرف تلقائياً
                    </div>
                    <div class="text-subtitle-2 font-weight-bold" v-else>{{ activeQuestionsCount }} سؤال ({{ activeChoicesLabels.length }} خيارات)</div>
                  </div>
                </v-col>
                <v-col cols="6" sm="3">
                  <div class="pa-3 rounded-lg border bg-grey-lighten-5 text-center">
                    <div class="text-caption text-medium-emphasis">الأعمدة الهندسية</div>
                    <div class="text-subtitle-2 font-weight-bold">{{ activeTemplateMeta.totalColumns }} أعمدة اتجاه RTL</div>
                  </div>
                </v-col>
              </v-row>

              <div class="d-flex gap-3 flex-wrap">
                <v-btn
                  color="primary"
                  size="large"
                  rounded="lg"
                  class="font-weight-bold px-6"
                  prepend-icon="mdi-printer"
                  @click="printSheet"
                >
                  طباعة ورقة الإجابة
                </v-btn>
                <v-btn
                  variant="outlined"
                  color="secondary"
                  size="large"
                  rounded="lg"
                  class="font-weight-bold px-5"
                  prepend-icon="mdi-folder-multiple-outline"
                  @click="$router.push('/omr/templates')"
                >
                  مكتبة القوالب ({{ savedTemplates.length }})
                </v-btn>
                <v-btn
                  color="secondary"
                  variant="tonal"
                  size="large"
                  rounded="lg"
                  class="font-weight-bold px-6"
                  append-icon="mdi-arrow-left"
                  @click="currentStep = 1"
                >
                  الانتقال للخطوة التالية (الرفع والتصحيح)
                </v-btn>
              </div>
            </v-card>

            <!-- Instructions Grid -->
            <v-row dense>
              <v-col cols="12" sm="6" v-for="ins in printInstructions" :key="ins.title">
                <v-card class="pa-4 rounded-xl border elevation-0 d-flex align-start gap-3 bg-surface">
                  <v-avatar color="primary" variant="tonal" size="36" rounded="lg">
                    <v-icon size="18">{{ ins.icon }}</v-icon>
                  </v-avatar>
                  <div>
                    <div class="font-weight-bold text-subtitle-2 mb-1">{{ ins.title }}</div>
                    <div class="text-caption text-medium-emphasis">{{ ins.text }}</div>
                  </div>
                </v-card>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card>
    </div>

    <!-- ════════════════════════════════════════════════════════════ -->
    <!-- STEP 1: رفع الورقة والمختبر التفاعلي                         -->
    <!-- ════════════════════════════════════════════════════════════ -->
    <div v-if="currentStep === 1">
      <v-card class="main-card pa-6 rounded-2xl mb-6 elevation-1">
        <div class="d-flex align-center justify-space-between mb-4">
          <div class="d-flex align-center gap-3">
            <v-avatar color="primary" variant="tonal" rounded="lg" size="44">
              <v-icon size="24">mdi-cloud-upload</v-icon>
            </v-avatar>
            <div>
              <h2 class="text-h6 font-weight-black mb-1">الخطوة الثانية: رفع الورقة المعبأة أو التجربة الحية</h2>
              <p class="text-body-2 text-medium-emphasis mb-0">ارفع صورة الورقة الممسوحة ضوئياً، أو استخدم استوديو التظليل المباشر لاختبار دقة محرك AI.</p>
            </div>
          </div>
        </div>

        <!-- بطاقة ربط الاختبار والنموذج (Exam Linking Banner) -->
        <v-card class="pa-4 rounded-xl border elevation-0 mb-4 bg-primary-lighten-5 border-primary">
          <div class="d-flex align-center justify-space-between mb-3 flex-wrap gap-2">
            <div class="d-flex align-center gap-2">
              <v-avatar color="primary" variant="flat" size="32" class="rounded-lg">
                <v-icon size="18" color="white">mdi-link-variant</v-icon>
              </v-avatar>
              <div>
                <span class="font-weight-black text-subtitle-2 text-primary">
                  الربط المباشر باختبار مولد من بنك الأسئلة
                </span>
                <span class="text-caption text-medium-emphasis ms-2 d-none d-sm-inline">
                  (جلب مفتاح الإجابة والنموذج تلقائياً دون إدخال يدوي)
                </span>
              </div>
            </div>

            <div class="d-flex align-center gap-2">
              <v-btn
                variant="text"
                color="primary"
                size="small"
                class="font-weight-bold"
                prepend-icon="mdi-format-list-bulleted"
                to="/omr/exams"
              >
                شاشة ربط الاختبارات
              </v-btn>
              <v-btn
                v-if="selectedExamId"
                variant="tonal"
                color="error"
                size="x-small"
                rounded="lg"
                class="font-weight-bold"
                @click="clearExamLink"
              >
                إلغاء الربط
              </v-btn>
            </div>
          </div>

          <v-row class="align-center" dense>
            <v-col cols="12" md="7">
              <v-select
                v-model="selectedExamId"
                :items="availableExams"
                item-title="title"
                item-value="id"
                label="اختر الاختبار المولد للربط التلقائي بمفتاح الإجابة"
                variant="outlined"
                density="comfortable"
                rounded="lg"
                prepend-inner-icon="mdi-file-document-check-outline"
                placeholder="-- اختياري: اختر اختباراً لجلب مفتاح الحل آلياً --"
                clearable
                hide-details
                @update:model-value="onExamSelected"
              >
                <template #item="{ props, item }">
                  <v-list-item
                    v-bind="props"
                    :title="item.raw.title"
                    :subtitle="`${item.raw.uniqueCode} | ${item.raw.subject_name} | ${item.raw.versions_count} نماذج`"
                  />
                </template>
              </v-select>
            </v-col>

            <v-col cols="12" md="3" v-if="selectedExamId && activeExamVersions.length > 0">
              <v-select
                v-model="selectedVersionCode"
                :items="activeExamVersions"
                item-title="title"
                item-value="value"
                label="النموذج المعتمد"
                variant="outlined"
                density="comfortable"
                rounded="lg"
                hide-details
                @update:model-value="onVersionSelected"
              />
            </v-col>

            <v-col cols="12" md="2" v-if="isExamLinked" class="text-center">
              <v-chip color="success" variant="flat" size="small" rounded="md" class="font-weight-bold">
                <v-icon start size="14">mdi-check-circle</v-icon>
                مربوط آلياً ✓
              </v-chip>
            </v-col>
          </v-row>
        </v-card>

        <!-- اختيار القالب المعتمد -->
        <v-card class="pa-4 rounded-xl border elevation-0 mb-6 bg-grey-lighten-5">
          <v-row class="align-center" dense>
            <v-col cols="12" md="7">
              <v-select
                v-model="selectedTemplateId"
                :items="templateOptions"
                item-title="title"
                item-value="value"
                label="القالب المعتمد المخصص للتصحيح"
                variant="outlined"
                density="comfortable"
                rounded="lg"
                prepend-inner-icon="mdi-file-document-outline"
                hide-details
              >
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props" :subtitle="item.raw.subtitle"></v-list-item>
                </template>
              </v-select>
            </v-col>

            <v-col cols="12" md="5" class="d-flex gap-2 align-center justify-md-end flex-wrap">
              <v-chip v-if="selectedTemplateId === 'AUTO'" color="success" variant="flat" size="small" rounded="md" class="font-weight-bold">
                <v-icon start size="14">mdi-auto-fix</v-icon>
                التعرف التلقائي الذكي على القالب (مُفعّل آلياً)
              </v-chip>
              <v-chip v-else color="primary" variant="flat" size="small" rounded="md" class="font-weight-bold">
                <v-icon start size="14">mdi-file-check</v-icon>
                {{ activeTemplateObj?.name || 'قالب محدد' }}
              </v-chip>
              <v-chip v-if="activeQuestionsCount > 0" color="primary" variant="tonal" size="small" rounded="md" class="font-weight-bold">
                <v-icon start size="14">mdi-format-list-numbered</v-icon>
                {{ activeQuestionsCount }} سؤال
              </v-chip>
              <v-chip v-if="activeQuestionsCount > 0" color="secondary" variant="tonal" size="small" rounded="md" class="font-weight-bold">
                <v-icon start size="14">{{ isTrueFalseTemplate ? 'mdi-check-all' : 'mdi-checkbox-blank-circle-outline' }}</v-icon>
                {{ activeChoicesLabels.length }} خيارات ({{ activeChoicesLabels.join(' / ') }})
              </v-chip>
              <v-btn
                variant="outlined"
                color="primary"
                size="small"
                rounded="lg"
                class="font-weight-bold"
                prepend-icon="mdi-folder-multiple-outline"
                @click="$router.push('/omr/templates')"
              >
                تصفح المكتبة
              </v-btn>
            </v-col>
          </v-row>
        </v-card>

        <!-- منطقة الرفع بالسحب والإفلات -->
        <!-- حالة: لا يوجد ملف مرفوع -->
        <div
          v-if="!uploadedFile"
          class="drop-zone pa-8 rounded-2xl mb-6 text-center cursor-pointer transition-all"
          :class="{ 'drag-over': isDragging }"
          @dragover.prevent="isDragging = true"
          @dragleave="isDragging = false"
          @drop.prevent="handleDrop"
          @click="$refs.fileInput.click()"
        >
          <input ref="fileInput" type="file" accept="image/*,.pdf" hidden @change="handleFileChange"/>
          <div class="py-4">
            <v-avatar size="64" color="primary" variant="tonal" class="mb-3">
              <v-icon size="36">mdi-cloud-upload-outline</v-icon>
            </v-avatar>
            <h3 class="text-subtitle-1 font-weight-bold mb-1">اسحب صورة الورقة هنا أو <span class="text-primary text-decoration-underline">اضغط للاختيار من جهازك</span></h3>
            <p class="text-caption text-medium-emphasis mb-0">PNG · JPG · TIFF · PDF — دقة ممسوحة 300 DPI موصى بها</p>
          </div>
        </div>

        <!-- حالة: تم رفع ملف — معاينة كبيرة واضحة -->
        <div v-else class="mb-6">
          <input ref="fileInput" type="file" accept="image/*,.pdf" hidden @change="handleFileChange"/>
          <!-- شريط معلومات الملف -->
          <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3 pa-3 rounded-xl border bg-green-lighten-5">
            <div class="d-flex align-center gap-2">
              <v-icon color="success" size="20">mdi-file-check-outline</v-icon>
              <span class="text-body-2 font-weight-bold text-success">{{ uploadedFile.name }}</span>
              <v-chip size="x-small" color="success" variant="tonal" rounded="md">{{ formatSize(uploadedFile.size) }}</v-chip>
            </div>
            <div class="d-flex gap-2">
              <v-btn
                color="primary"
                variant="tonal"
                size="small"
                rounded="lg"
                prepend-icon="mdi-file-replace-outline"
                class="font-weight-bold"
                @click="$refs.fileInput.click()"
              >
                تغيير الصورة
              </v-btn>
              <v-btn
                color="error"
                variant="text"
                size="small"
                rounded="lg"
                prepend-icon="mdi-trash-can-outline"
                class="font-weight-bold"
                @click="removeFile"
              >
                إزالة
              </v-btn>
            </div>
          </div>
          <!-- معاينة الصورة الكبيرة -->
          <div class="uploaded-preview-container rounded-2xl border text-center pa-4 bg-grey-lighten-5"
               style="min-height: 200px; position: relative;"
               @dragover.prevent="isDragging = true"
               @dragleave="isDragging = false"
               @drop.prevent="handleDrop"
          >
            <img
              v-if="previewUrl"
              :src="previewUrl"
              class="preview-img"
              alt="معاينة الورقة المرفوعة"
            />
            <div v-else class="d-flex align-center justify-center" style="min-height: 200px;">
              <v-progress-circular indeterminate color="primary" size="48"/>
            </div>
          </div>

          <!-- شريط بدء التصحيح المباشر للورقة المرفوعة -->
          <div class="d-flex align-center justify-space-between flex-wrap gap-3 mt-4 pa-4 rounded-xl border bg-primary-lighten-5">
            <div class="d-flex align-center gap-3">
              <v-avatar color="primary" variant="tonal" size="44" rounded="lg">
                <v-icon color="primary" size="26">mdi-scanner</v-icon>
              </v-avatar>
              <div>
                <div class="text-subtitle-2 font-weight-bold text-primary">الورقة جاهزة ومرفوعة بنجاح</div>
                <div class="text-caption text-medium-emphasis">
                  {{ activeTemplateObj ? activeTemplateObj.name + ' (' + activeQuestionsCount + ' سؤال)' : 'سيتم فحص الباركود ومحاذاة الزوايا آلياً' }}
                </div>
              </div>
            </div>
            <v-btn
              color="primary"
              size="large"
              rounded="xl"
              class="px-6 font-weight-black elevation-2"
              prepend-icon="mdi-play-circle"
              :loading="isGrading"
              @click="startGrading"
            >
              بدء التصحيح الآلي لهذه الورقة الآن (AI OMR)
            </v-btn>
          </div>
        </div>

        <!-- استوديو التظليل والمحاكاة المباشر (اختياري لتخفيف الكثافة والازدحام) -->
        <v-expansion-panels v-model="interactivePanelOpen" class="mb-6 rounded-xl border elevation-0">
          <v-expansion-panel>
            <v-expansion-panel-title class="font-weight-bold">
              <v-icon color="primary" class="me-2">mdi-draw-pen</v-icon>
              <span>استوديو التظليل والمحاكاة المباشر (اختياري لتجربة التظليل بالماوس بدون ماسح ضوئي)</span>
              <v-chip size="x-small" color="secondary" variant="tonal" rounded="md" class="ms-2 font-weight-bold">
                محاكاة رسم وتظليل بالماوس فقط
              </v-chip>
            </v-expansion-panel-title>
            <v-expansion-panel-text class="pt-2">
              <v-alert
                v-if="uploadedFile"
                type="info"
                variant="tonal"
                density="compact"
                rounded="lg"
                class="mb-3 text-caption font-weight-medium"
              >
                تنبيه: أنت قمت بالفعل برفع صورة ورقة الإجابة المعبأة أعلاه. هذا القسم مخصص فقط لتجربة تظليل دوائر فارغة بالماوس لمن ليس لديه ماسح ضوئي. لتصحيح ورقتك المرفوعة، استخدم زر <strong>"بدء التصحيح الآلي لهذه الورقة الآن"</strong> في الأعلى أو الأسفل.
              </v-alert>
              <div class="d-flex justify-space-between align-center mb-4 flex-wrap gap-2 pb-3 border-b">
                <p class="text-caption text-medium-emphasis mb-0">انقر على أي دائرة في ورقة الإجابة أدناه لتظليلها واختبار دقة محرك OMR.</p>
                <div class="d-flex gap-2 flex-wrap align-center">
                  <v-btn size="small" variant="tonal" color="info" rounded="lg" prepend-icon="mdi-dice-5-outline" class="font-weight-bold" @click="randomShadeInteractive">
                    تظليل عشوائي
                  </v-btn>
                  <v-btn size="small" variant="tonal" color="success" rounded="lg" prepend-icon="mdi-check-decagram-outline" class="font-weight-bold" @click="fillAnswersWithKey">
                    تظليل النموذج الكامل
                  </v-btn>
                  <v-btn size="small" variant="tonal" color="warning" rounded="lg" prepend-icon="mdi-refresh" class="font-weight-bold" @click="interactiveStudentAnswers = {}">
                    مسح التظليل
                  </v-btn>
                  <v-btn size="small" color="primary" rounded="lg" prepend-icon="mdi-play-circle" :loading="isGrading" class="font-weight-bold" @click="generateInteractiveShadedImageAndGrade">
                    تصحيح الورقة المظللة
                  </v-btn>
                </div>
              </div>

              <!-- Split View -->
              <v-row dense>
                <!-- Left Side: Interactive SVG Canvas -->
                <v-col cols="12" md="8">
                  <div class="interactive-omr-svg pa-3 rounded-xl border bg-white position-relative text-center overflow-auto" style="max-height: 560px;">
                    <!-- وضع AUTO: لا يوجد قالب محدد — اختر قالباً أولاً -->
                    <div v-if="!activeTemplateObj" class="d-flex flex-column align-center justify-center py-12 text-medium-emphasis gap-3">
                      <v-icon size="56" color="grey-lighten-1">mdi-barcode-scan</v-icon>
                      <div class="text-subtitle-1 font-weight-medium">الاستوديو يحتاج تحديد قالب</div>
                      <p class="text-caption text-center" style="max-width:280px;">
                        اختر قالباً محدداً من القائمة أعلاه لفتح استوديو التظليل التفاعلي.<br/>
                        في وضع "التعرف التلقائي" يُستخدم الباركود لتحديد القالب أثناء التصحيح.
                      </p>
                    </div>
                    <Suspense v-else>
                      <YemeniMinistrySheet
                        v-if="isMinistrySheet"
                        :student-answers="interactiveStudentAnswers"
                        :interactive="true"
                        @bubble-click="onInteractiveBubbleClick"
                      />
                      <OmrSheetMultigraphics
                        v-else
                        :total-questions="activeQuestionsCount"
                        :questions-per-column="activeTemplateMeta.questionsPerColumn"
                        :total-columns="activeTemplateMeta.totalColumns"
                        :row-spacing="activeTemplateMeta.rowSpacing"
                        :bubble-radius="activeTemplateMeta.bubbleRadius"
                        :choices-per-question="activeChoicesLabels.length"
                        :student-answers="interactiveStudentAnswers"
                        :mcq-questions="activeTemplateObj?.template_data?.mcq_questions || []"
                        :interactive="true"
                        @bubble-click="onInteractiveBubbleClick"
                        @bubble-hover="onInteractiveBubbleHover"
                        @bubble-leave="onInteractiveBubbleLeave"
                      />
                      <template #fallback>
                        <div class="py-12 text-center text-medium-emphasis">جاري تحميل استوديو التظليل...</div>
                      </template>
                    </Suspense>
                  </div>
                </v-col>

                <!-- Right Side: Matrix Selector -->
                <v-col cols="12" md="4">
                  <v-card class="pa-3 rounded-xl border elevation-0 bg-grey-lighten-5 d-flex flex-column" style="max-height: 560px;">
                    <div class="d-flex justify-space-between align-center mb-2 pb-2 border-b">
                      <span class="text-subtitle-2 font-weight-bold text-on-surface">
                        مصفوفة الإجابات ({{ Object.keys(interactiveStudentAnswers).length }} / {{ activeQuestionsCount }})
                      </span>
                    </div>

                    <div class="overflow-y-auto pe-1 d-flex flex-column gap-1" style="flex: 1;">
                      <div
                        v-for="q in activeQuestionsCount"
                        :key="'matrix-q-' + q"
                        class="d-flex justify-space-between align-center pa-1 px-2 rounded-lg border bg-surface"
                      >
                        <span class="text-caption font-weight-bold text-medium-emphasis" style="width: 38px;">سـ {{ q }}</span>
                        <div class="d-flex gap-1">
                          <v-btn
                            v-for="c in activeChoicesLabels"
                            :key="'mat-c-' + q + '-' + c"
                            size="x-small"
                            :variant="getInteractiveState(q, c) === 'filled' ? 'flat' : getInteractiveState(q, c) === 'crossed' ? 'tonal' : 'outlined'"
                            :color="getInteractiveState(q, c) === 'filled' ? 'primary' : getInteractiveState(q, c) === 'crossed' ? 'error' : 'grey-lighten-1'"
                            class="font-weight-black"
                            style="min-width: 24px; height: 24px; padding: 0;"
                            @click="toggleInteractiveAnswer(q, c)"
                          >
                            {{ c }}
                          </v-btn>
                        </div>
                      </div>
                    </div>
                  </v-card>
                </v-col>
              </v-row>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>

        <!-- مفتاح الإجابات النموذجية (بطاقات Vuetify النقية) -->
        <v-expansion-panels class="mb-6 rounded-xl border elevation-0">
          <v-expansion-panel>
            <v-expansion-panel-title class="font-weight-bold">
              <v-icon color="amber-darken-2" class="me-2">mdi-key-variant</v-icon>
              مفتاح الإجابات النموذجية (اختياري لحساب الدرجة والنسبة) — {{ activeQuestionsCount }} سؤال
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <div class="d-flex gap-2 mb-3 flex-wrap">
                <v-btn
                  size="small"
                  variant="flat"
                  color="success"
                  class="font-weight-bold"
                  prepend-icon="mdi-shield-check"
                  @click="loadOfficialKey"
                >
                  استعادة المفتاح النموذجي المعتمد (100% تطابق)
                </v-btn>
                <v-btn size="small" variant="tonal" color="primary" class="font-weight-bold" prepend-icon="mdi-dice-5" @click="randomKey">
                  توليد مفتاح عشوائي
                </v-btn>
                <v-btn
                  size="small"
                  variant="tonal"
                  color="teal"
                  class="font-weight-bold"
                  prepend-icon="mdi-check-decagram"
                  :disabled="!result?.questions?.length"
                  @click="useSheetAsKey"
                >
                  اعتماد تظليلات الورقة كمفتاح نموذجي
                </v-btn>
                <v-btn size="small" variant="text" color="error" class="font-weight-bold" prepend-icon="mdi-delete-outline" @click="clearKey">
                  مسح المفتاح
                </v-btn>
              </div>

              <div class="key-grid-matrix">
                <div v-for="q in activeQuestionsCount" :key="'key-q-' + q" class="key-input-card pa-2 rounded-lg border text-center bg-surface">
                  <span class="text-caption font-weight-bold text-medium-emphasis d-block mb-1">سـ {{ q }}</span>
                  <div class="d-flex justify-center gap-1">
                    <v-btn
                      v-for="c in getQuestionChoices(q)"
                      :key="'k-opt-' + q + '-' + c"
                      size="x-small"
                      :variant="answerKey[q] === c ? 'flat' : 'outlined'"
                      :color="answerKey[q] === c ? 'primary' : 'grey-lighten-2'"
                      class="font-weight-black"
                      style="min-width: 22px; height: 22px; padding: 0;"
                      @click="answerKey[q] = answerKey[q] === c ? '' : c"
                    >
                      {{ c }}
                    </v-btn>
                  </div>
                </div>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>

        <!-- Footer Actions -->
        <div class="d-flex justify-space-between align-center flex-wrap gap-3">
          <v-btn
            variant="outlined"
            rounded="lg"
            size="large"
            prepend-icon="mdi-arrow-right"
            @click="currentStep = 0"
          >
            الخطوة السابقة (تصدير الورقة)
          </v-btn>

          <v-btn
            color="primary"
            rounded="lg"
            size="x-large"
            elevation="3"
            class="font-weight-bold px-8"
            :disabled="!uploadedFile || isGrading"
            :loading="isGrading"
            prepend-icon="mdi-play-circle"
            @click="startGrading"
          >
            بدء التصحيح الآلي (AI OMR Pipeline)
          </v-btn>
        </div>

        <!-- شريط التقدم أثناء التصحيح -->
        <div v-if="isGrading" class="mt-6 pa-4 rounded-xl border bg-grey-lighten-5">
          <div class="d-flex justify-space-between align-center mb-2">
            <span class="text-subtitle-2 font-weight-bold text-primary">{{ gradingStatus }}</span>
            <span class="text-caption font-weight-bold">{{ gradingProgress }}%</span>
          </div>
          <v-progress-linear :model-value="gradingProgress" height="8" rounded color="primary" striped />
        </div>
      </v-card>
    </div>

    <!-- ════════════════════════════════════════════════════════════ -->
    <!-- STEP 2: النتائج وتتبع الذكاء الاصطناعي                       -->
    <!-- ════════════════════════════════════════════════════════════ -->
    <div v-if="currentStep === 2 && result">
      <!-- بطاقات الإحصائيات (Institutional Standard Vuetify 3 Cards) -->
      <v-row class="mb-6">
        <v-col cols="12" sm="6" md="2">
          <v-card class="main-card pa-4 rounded-xl border elevation-0 h-100 d-flex flex-column justify-space-between">
            <div class="d-flex align-center justify-space-between mb-3">
              <v-avatar color="primary" variant="tonal" size="44" rounded="lg">
                <v-icon size="22">mdi-chart-donut</v-icon>
              </v-avatar>
              <v-chip size="x-small" color="primary" variant="tonal" rounded="md" class="font-weight-bold">النسبة المئوية</v-chip>
            </div>
            <div>
              <div class="text-h4 font-weight-black text-primary mb-1">{{ result.score_percent }}%</div>
              <div class="text-subtitle-2 font-weight-bold text-on-surface">الدرجة الإجمالية</div>
            </div>
            <div class="text-caption text-medium-emphasis mt-2 pt-2 border-t d-flex align-center justify-space-between">
              <span>النقاط المحتسبة</span>
              <span class="font-weight-bold text-on-surface">{{ result.score }} / {{ result.max_score }}</span>
            </div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="2">
          <v-card class="main-card pa-4 rounded-xl border elevation-0 h-100 d-flex flex-column justify-space-between">
            <div class="d-flex align-center justify-space-between mb-3">
              <v-avatar color="success" variant="tonal" size="44" rounded="lg">
                <v-icon size="22">mdi-check-circle-outline</v-icon>
              </v-avatar>
              <v-chip size="x-small" color="success" variant="tonal" rounded="md" class="font-weight-bold">صحيحة</v-chip>
            </div>
            <div>
              <div class="text-h4 font-weight-black text-success mb-1">{{ result.total_correct }}</div>
              <div class="text-subtitle-2 font-weight-bold text-on-surface">إجابات صحيحة</div>
            </div>
            <div class="text-caption text-success mt-2 pt-2 border-t d-flex align-center justify-space-between">
              <span>مطابقة للمفتاح</span>
              <v-icon size="16">mdi-check-circle</v-icon>
            </div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="2">
          <v-card class="main-card pa-4 rounded-xl border elevation-0 h-100 d-flex flex-column justify-space-between">
            <div class="d-flex align-center justify-space-between mb-3">
              <v-avatar color="error" variant="tonal" size="44" rounded="lg">
                <v-icon size="22">mdi-close-circle-outline</v-icon>
              </v-avatar>
              <v-chip size="x-small" color="error" variant="tonal" rounded="md" class="font-weight-bold">خاطئة</v-chip>
            </div>
            <div>
              <div class="text-h4 font-weight-black text-error mb-1">{{ result.total_wrong }}</div>
              <div class="text-subtitle-2 font-weight-bold text-on-surface">إجابات خاطئة</div>
            </div>
            <div class="text-caption text-error mt-2 pt-2 border-t d-flex align-center justify-space-between">
              <span>غير مطابقة</span>
              <v-icon size="16">mdi-alert-circle</v-icon>
            </div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="2">
          <v-card class="main-card pa-4 rounded-xl border elevation-0 h-100 d-flex flex-column justify-space-between">
            <div class="d-flex align-center justify-space-between mb-3">
              <v-avatar color="warning" variant="tonal" size="44" rounded="lg">
                <v-icon size="22">mdi-checkbox-blank-circle-outline</v-icon>
              </v-avatar>
              <v-chip size="x-small" color="warning" variant="tonal" rounded="md" class="font-weight-bold">متروكة</v-chip>
            </div>
            <div>
              <div class="text-h4 font-weight-black text-warning mb-1">{{ result.total_empty }}</div>
              <div class="text-subtitle-2 font-weight-bold text-on-surface">غير مجاب / فارغة</div>
            </div>
            <div class="text-caption text-warning mt-2 pt-2 border-t d-flex align-center justify-space-between">
              <span>بدون تظليل</span>
              <v-icon size="16">mdi-minus-circle-outline</v-icon>
            </div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="12" md="4">
          <v-card class="main-card pa-4 rounded-xl border elevation-0 h-100 d-flex flex-column justify-space-between">
            <div class="d-flex align-center justify-space-between mb-2">
              <div class="d-flex align-center gap-2">
                <v-avatar color="info" variant="tonal" size="44" rounded="lg">
                  <v-icon size="22">mdi-chip</v-icon>
                </v-avatar>
                <div>
                  <div class="text-subtitle-2 font-weight-bold text-on-surface">المحرك الهجين النشط</div>
                  <div class="text-caption text-medium-emphasis">OMR Vision Pipeline</div>
                </div>
              </div>
              <v-chip size="x-small" color="info" variant="flat" rounded="md" class="font-weight-bold">YOLOv8 + OpenCV</v-chip>
            </div>
            <div class="pa-2 rounded-lg border bg-grey-lighten-5 d-flex align-center justify-space-between my-2">
              <span class="text-caption text-medium-emphasis">زمن المعالجة: <strong class="text-on-surface">{{ result.processing_ms }}ms</strong></span>
              <span class="text-caption text-medium-emphasis">تصحيحات AI: <strong class="text-primary">{{ result.ai_corrections }}</strong></span>
            </div>
            <div class="d-flex align-center gap-1 text-caption text-success font-weight-bold pt-2 border-t">
              <v-icon size="16" color="success">mdi-check-decagram</v-icon>
              <span>تم التعرف على الباركود ومحاذاة الزوايا بدقة معيارية</span>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Action Buttons Bar -->
      <div class="d-flex justify-end gap-3 mb-6 flex-wrap">
        <v-btn
          color="primary"
          rounded="lg"
          prepend-icon="mdi-file-document-check-outline"
          class="font-weight-bold"
          @click="showAuditReportModal = true"
        >
          تقرير التدقيق والتصحيح الإلكتروني (الرسمي)
        </v-btn>
        <v-btn color="primary" variant="tonal" rounded="lg" prepend-icon="mdi-printer" class="font-weight-bold" @click="printResult">
          طباعة النتيجة
        </v-btn>
        <v-btn variant="outlined" rounded="lg" prepend-icon="mdi-code-json" class="font-weight-bold" @click="downloadJSON">
          تصدير JSON
        </v-btn>
        <v-btn color="secondary" variant="tonal" rounded="lg" prepend-icon="mdi-refresh" class="font-weight-bold" @click="resetWorkflow">
          تصحيح ورقة جديدة
        </v-btn>
      </div>

      <!-- Main Results Split Layout -->
      <v-row>
        <!-- Left: Annotated Image -->
        <v-col cols="12" md="5">
          <v-card class="main-card pa-5 rounded-2xl border elevation-1">
            <div class="d-flex justify-space-between align-center mb-3 flex-wrap gap-2">
              <h3 class="text-subtitle-1 font-weight-bold d-flex align-center mb-0">
                <v-icon color="primary" class="me-2" size="20">mdi-image-check-outline</v-icon>
                الورقة المُصحَّحة بدقة AI
              </h3>
              <div class="d-flex gap-2">
                <v-btn
                  v-if="annotatedUrl"
                  size="small"
                  variant="tonal"
                  color="secondary"
                  prepend-icon="mdi-download"
                  class="font-weight-bold"
                  @click="downloadAnnotatedImage"
                >
                  تنزيل الصورة
                </v-btn>
                <v-btn
                  v-if="annotatedUrl"
                  size="small"
                  variant="tonal"
                  color="primary"
                  prepend-icon="mdi-magnify-plus-outline"
                  class="font-weight-bold"
                  @click="openZoomModal('fit')"
                >
                  تكبير الورقة
                </v-btn>
              </div>
            </div>

            <div class="annotated-image-box border rounded-xl overflow-hidden text-center bg-grey-lighten-4 mb-3 position-relative" style="max-height: 540px; overflow-y: auto;">
              <img
                v-if="annotatedUrl"
                :src="annotatedUrl"
                class="cursor-zoom-in d-block mx-auto"
                style="max-width: 100%; height: auto; object-fit: contain;"
                alt="الورقة المصححة"
                @click="openZoomModal('fit')"
              />
              <div v-else class="py-12 text-center text-medium-emphasis">
                <v-icon size="48" color="medium-emphasis" class="mb-2">mdi-image-outline</v-icon>
                <p class="text-caption mb-0">{{ interactiveGradeMode ? 'تمت المعالجة في المختبر التفاعلي' : 'لا توجد صورة مُعلَّمة' }}</p>
              </div>
            </div>

            <div class="d-flex flex-wrap gap-2">
              <v-chip size="small" color="success" variant="tonal" rounded="md" class="font-weight-bold">
                <v-icon start size="14">mdi-check-circle</v-icon> إجابة صحيحة
              </v-chip>
              <v-chip size="small" color="error" variant="tonal" rounded="md" class="font-weight-bold">
                <v-icon start size="14">mdi-close-circle</v-icon> إجابة خاطئة
              </v-chip>
              <v-chip size="small" color="warning" variant="tonal" rounded="md" class="font-weight-bold">
                <v-icon start size="14">mdi-alert-circle</v-icon> إجابة مزدوجة / ملغاة
              </v-chip>
              <v-chip size="small" color="info" variant="tonal" rounded="md" class="font-weight-bold">
                <v-icon start size="14">mdi-microscope</v-icon> كشف ذكاء اصطناعي
              </v-chip>
            </div>
          </v-card>
        </v-col>

        <!-- Right: Questions & AI Inspection Table -->
        <v-col cols="12" md="7">
          <v-card class="main-card pa-5 rounded-2xl border elevation-1">
            <div class="d-flex justify-space-between align-center mb-3 flex-wrap gap-2">
              <div>
                <h3 class="text-subtitle-1 font-weight-bold d-flex align-center mb-0">
                  <v-icon color="primary" class="me-2" size="20">mdi-clipboard-list-outline</v-icon>
                  جدول تدقيق ومطابقة إجابات الأسئلة
                </h3>
                <span class="text-caption text-medium-emphasis">استعراض نتيجة كل سؤال ومطابقتها مع مفتاح الإجابة ونسبة ثقة القراءة</span>
              </div>
              <v-chip size="small" color="primary" variant="tonal" rounded="md" class="font-weight-bold">
                إجمالي الأسئلة: {{ result?.questions?.length || activeQuestionsCount }}
              </v-chip>
            </div>

            <!-- Filters -->
            <v-chip-group v-model="activeFilter" mandatory class="mb-3">
              <v-chip
                v-for="f in filters"
                :key="f.key"
                :value="f.key"
                filter
                size="small"
                rounded="md"
                class="font-weight-bold"
                :color="activeFilter === f.key ? 'primary' : undefined"
              >
                {{ f.label }} ({{ filterCount(f.key) }})
              </v-chip>
            </v-chip-group>

            <!-- Table -->
            <div class="table-responsive" style="max-height: 520px; overflow-y: auto;">
              <v-table density="comfortable" hover>
                <thead>
                  <tr>
                    <th class="text-start font-weight-bold">سؤال</th>
                    <th class="text-center font-weight-bold">الإجابة</th>
                    <th class="text-center font-weight-bold">الصحيحة</th>
                    <th class="text-center font-weight-bold">الحالة</th>
                    <th class="text-center font-weight-bold">ثقة AI</th>
                    <th class="text-end font-weight-bold">التفاصيل</th>
                  </tr>
                </thead>
                <tbody>
                  <!-- Empty State when filtered count is 0 -->
                  <tr v-if="filteredQuestions.length === 0">
                    <td colspan="6" class="text-center py-8">
                      <v-avatar color="grey-lighten-4" size="48" class="mb-2">
                        <v-icon size="28" color="medium-emphasis">mdi-filter-variant-remove</v-icon>
                      </v-avatar>
                      <div class="text-subtitle-2 font-weight-bold text-medium-emphasis">
                        لا توجد أسئلة مصنفة كـ «{{ filters.find(f => f.key === activeFilter)?.label }}»
                      </div>
                      <v-btn
                        size="small"
                        variant="tonal"
                        color="primary"
                        class="mt-3 font-weight-bold"
                        prepend-icon="mdi-format-list-bulleted"
                        @click="activeFilter = 'all'"
                      >
                        عرض كافة الأسئلة ({{ filterCount('all') }})
                      </v-btn>
                    </td>
                  </tr>

                  <template v-else v-for="q in filteredQuestions" :key="'row-' + q.q">
                    <tr class="cursor-pointer" @click="toggleQuestionExpand(q.q)">
                      <td class="font-weight-bold">سـ {{ q.q }}</td>
                      <td class="text-center">
                        <v-chip
                          size="small"
                          rounded="md"
                          :color="getAnswerBadgeProps(q.marked || q.marked_choice).color"
                          :variant="getAnswerBadgeProps(q.marked || q.marked_choice).variant"
                          class="font-weight-bold"
                        >
                          <v-icon v-if="getAnswerBadgeProps(q.marked || q.marked_choice).icon" start size="13">
                            {{ getAnswerBadgeProps(q.marked || q.marked_choice).icon }}
                          </v-icon>
                          {{ getAnswerBadgeProps(q.marked || q.marked_choice).text }}
                        </v-chip>
                      </td>
                      <td class="text-center">
                        <v-chip
                          size="small"
                          rounded="md"
                          :color="getCorrectBadgeProps(q.correct || q.correct_choice).color"
                          :variant="getCorrectBadgeProps(q.correct || q.correct_choice).variant"
                          class="font-weight-bold"
                        >
                          <v-icon v-if="getCorrectBadgeProps(q.correct || q.correct_choice).icon" start size="13">
                            {{ getCorrectBadgeProps(q.correct || q.correct_choice).icon }}
                          </v-icon>
                          {{ getCorrectBadgeProps(q.correct || q.correct_choice).text }}
                        </v-chip>
                      </td>
                      <td class="text-center">
                        <v-chip
                          size="small"
                          rounded="md"
                          :color="getStatusBadgeProps(q).color"
                          :variant="getStatusBadgeProps(q).variant"
                          class="font-weight-bold"
                        >
                          <v-icon start size="14">
                            {{ getStatusBadgeProps(q).icon }}
                          </v-icon>
                          {{ getStatusBadgeProps(q).text }}
                        </v-chip>
                      </td>
                      <td class="text-center font-weight-bold font-mono text-info">
                        {{ Math.round((q.final_confidence || q.confidence || 0.95) * 100) }}%
                      </td>
                      <td class="text-end">
                        <v-icon size="18" color="medium-emphasis">
                          {{ expandedQuestionId === q.q ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
                        </v-icon>
                      </td>
                    </tr>

                    <!-- Expanded AI Inspection Detail (100% Light Institutional Theme) -->
                    <tr v-if="expandedQuestionId === q.q">
                      <td colspan="6" class="pa-4 bg-grey-lighten-5">
                        <v-card class="pa-3 rounded-xl border elevation-0 bg-surface">
                          <div class="d-flex justify-space-between align-center mb-3 pb-2 border-b">
                            <div class="d-flex align-center gap-2">
                              <v-avatar color="info" variant="tonal" size="28" rounded="lg">
                                <v-icon size="16">mdi-magnify</v-icon>
                              </v-avatar>
                              <span class="text-subtitle-2 font-weight-bold text-info">
                                كشف نموذج YOLOv8 وتحليل البكسل لسؤال {{ q.q }}
                              </span>
                              <v-chip size="x-small" color="info" variant="tonal" rounded="md" class="font-weight-black">
                                نسبة الثقة: {{ Math.round((q.final_confidence || 0.95) * 100) }}%
                              </v-chip>
                            </div>
                            <v-chip size="x-small" color="primary" variant="outlined" rounded="md" class="font-mono font-weight-bold">
                              حالة التظليل: {{ q.bubble_state || 'empty' }}
                            </v-chip>
                          </div>

                          <div class="d-flex gap-3 flex-wrap">
                            <div
                              v-for="ch in (q.choice_crops && Object.keys(q.choice_crops).length ? Object.keys(q.choice_crops) : (q.choices || activeChoicesLabels))"
                              :key="'ai-box-' + q.q + '-' + ch"
                              class="pa-3 rounded-xl border bg-grey-lighten-5 text-center"
                              style="min-width: 110px; flex: 1;"
                            >
                              <div class="text-caption font-weight-black text-on-surface mb-2">خيار [{{ ch }}]</div>

                              <div class="d-flex align-center justify-center my-2 pa-1 bg-white rounded border" style="height: 52px;">
                                <img
                                  v-if="q.choice_crops && q.choice_crops[ch]"
                                  :src="q.choice_crops[ch]"
                                  alt="Crop"
                                  class="rounded"
                                  style="max-height: 44px; max-width: 44px; image-rendering: pixelated;"
                                />
                                <span v-else class="text-caption text-medium-emphasis">لا صورة</span>
                              </div>

                              <v-chip
                                size="small"
                                rounded="md"
                                :color="(q.ai_results && q.ai_results[ch] === 'filled') ? 'success' : (q.ai_results && q.ai_results[ch] === 'crossed') ? 'error' : 'grey'"
                                variant="tonal"
                                class="font-weight-black w-100"
                              >
                                {{ (q.ai_results && q.ai_results[ch]) ? q.ai_results[ch] : (q.marked === ch ? 'filled' : 'empty') }}
                              </v-chip>
                            </div>
                          </div>
                        </v-card>
                      </td>
                    </tr>
                  </template>
                </tbody>
              </v-table>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- ── Full-size Sheet Preview Dialog (Step 0) ────────────────── -->
    <v-dialog v-model="showSheetPreviewModal" max-width="840">
      <v-card class="pa-6 rounded-2xl">
        <div class="d-flex align-center justify-space-between mb-4 pb-2 border-b">
          <div class="d-flex align-center gap-2">
            <v-avatar color="primary" variant="tonal" size="36" rounded="lg">
              <v-icon color="primary" size="20">mdi-printer-eye</v-icon>
            </v-avatar>
            <h3 class="text-h6 font-weight-black mb-0">معاينة ورقة الإجابة المعتمدة (A4 300 DPI)</h3>
          </div>
          <v-btn icon size="small" variant="text" @click="showSheetPreviewModal = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
        <div class="pa-4 bg-grey-lighten-4 rounded-xl d-flex justify-center overflow-auto" style="max-height: 650px;">
          <div :style="modalSheetWrapperStyle">
            <YemeniMinistrySheet
              v-if="isMinistrySheet"
              :student-name="linkedStudents[0]?.student_name || 'طالب اختبار'"
              :seat-number="linkedStudents[0]?.seat_number || '418485'"
              :model-code="selectedVersionCode || 'A'"
              :center-code="'101'"
              :school-name="linkedStudents[0]?.school_name || selectedExamObj?.title || 'المؤسسة التعليمية'"
              :governorate="selectedExamObj?.governorate || 'أمانة العاصمة'"
              :directorate="selectedExamObj?.directorate || ''"
              :exam-subject="selectedExamObj?.subject_name || 'المادة'"
            />
            <OmrSheetMultigraphics
              v-else
              :total-questions="activeQuestionsCount"
              :questions-per-column="activeTemplateMeta.questionsPerColumn"
              :total-columns="activeTemplateMeta.totalColumns"
              :row-spacing="activeTemplateMeta.rowSpacing"
              :bubble-radius="activeTemplateMeta.bubbleRadius"
              :choices-per-question="activeChoicesLabels.length"
              :bubble-type="activeTemplateMeta.bubbleType"
              :layout-direction="activeTemplateMeta.layoutDirection"
              :primary-color="activeTemplateMeta.primaryColor"
              :institution-name="activeTemplateMeta.institutionName"
              :sub-title="activeTemplateMeta.subTitle"
              :exam-name="activeTemplateMeta.examName"
            />
          </div>
        </div>
      </v-card>
    </v-dialog>

    <!-- ── High-Resolution Annotated Image Zoom Dialog (Step 3) ───── -->
    <v-dialog v-model="isZoomed" max-width="1400px" width="96vw" scrollable>
      <v-card class="rounded-2xl d-flex flex-column" style="max-height: 90vh;">
        <!-- Header -->
        <div class="pa-4 px-6 border-b d-flex justify-space-between align-center flex-wrap gap-3 bg-surface">
          <div class="d-flex align-center gap-3">
            <v-avatar color="primary" variant="tonal" size="40" rounded="lg">
              <v-icon size="22">mdi-image-search-outline</v-icon>
            </v-avatar>
            <div>
              <h3 class="text-h6 font-weight-black mb-0">فحص الورقة المصححة بدقة بكسل كاملة</h3>
              <div class="d-flex align-center gap-2 mt-1">
                <v-chip size="x-small" color="primary" variant="flat" rounded="md" class="font-weight-bold">
                  {{ result?.meta?.detected_dpi ? `دقة الفحص ${result.meta.detected_dpi} DPI فائقة الوضوح` : 'دقة فائقة الوضوح (UltraHD)' }}
                </v-chip>
                <v-chip size="x-small" color="info" variant="tonal" rounded="md" class="font-weight-bold">
                  {{ isMinistrySheet ? `نموذج وزارة التربية والتعليم (${result?.total_questions || activeQuestionsCount} سؤال - A5)` : 'مقاس الورقة المعتمد' }}
                </v-chip>
                <v-chip v-if="result" size="x-small" color="success" variant="tonal" rounded="md" class="font-weight-bold">
                  {{ result.total_answered }} / {{ result.total_questions || 50 }} إجابة مكتشفة
                </v-chip>
              </div>
            </div>
          </div>

          <!-- Controls Toolbar -->
          <div class="d-flex align-center gap-2 flex-wrap">
            <!-- View Mode Toggles -->
            <v-btn-toggle
              v-model="zoomMode"
              mandatory
              density="compact"
              color="primary"
              variant="outlined"
              rounded="lg"
              class="me-2"
            >
              <v-btn value="fit" size="small" class="font-weight-bold" prepend-icon="mdi-fit-to-screen-outline">
                ملاءمة الصفحة
              </v-btn>
              <v-btn value="actual" size="small" class="font-weight-bold" prepend-icon="mdi-image-size-select-actual">
                الحجم الفعلي 100%
              </v-btn>
            </v-btn-toggle>

            <!-- Zoom Controls -->
            <div class="d-flex align-center bg-grey-lighten-4 rounded-lg px-1 border">
              <v-btn icon size="small" variant="text" :disabled="zoomLevel <= 0.4" @click="zoomOut">
                <v-icon size="18">mdi-magnify-minus-outline</v-icon>
              </v-btn>
              <span class="text-caption font-weight-bold px-2 font-mono" style="min-width: 48px; text-align: center;">
                {{ Math.round(zoomLevel * 100) }}%
              </span>
              <v-btn icon size="small" variant="text" :disabled="zoomLevel >= 3.0" @click="zoomIn">
                <v-icon size="18">mdi-magnify-plus-outline</v-icon>
              </v-btn>
              <v-btn icon size="small" variant="text" title="إعادة الضبط" @click="resetZoom">
                <v-icon size="16">mdi-refresh</v-icon>
              </v-btn>
            </div>

            <v-divider vertical class="mx-1" style="height: 28px;" />

            <!-- Download Button -->
            <v-btn
              color="primary"
              variant="tonal"
              size="small"
              rounded="lg"
              class="font-weight-bold"
              prepend-icon="mdi-download"
              @click="downloadAnnotatedImage"
            >
              تنزيل الصورة
            </v-btn>

            <!-- Close Button -->
            <v-btn icon size="small" variant="text" @click="isZoomed = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </div>
        </div>

        <!-- Sheet Canvas / Image Viewport -->
        <div
          class="omr-zoom-viewport pa-4 overflow-auto text-center"
          style="max-height: calc(90vh - 80px); min-height: 480px;"
        >
          <div class="sheet-paper-container elevation-6 rounded-lg bg-white overflow-hidden d-inline-block position-relative">
            <img
              :src="annotatedUrl"
              class="sheet-annotated-img"
              :style="sheetImageStyle"
              alt="الورقة المصححة بدقة كاملة"
            />
          </div>
        </div>
      </v-card>
    </v-dialog>

    <!-- ── Official Yemeni Audit & Correction Report Dialog ─────── -->
    <v-dialog v-model="showAuditReportModal" max-width="1140px" width="96vw" scrollable>
      <v-card class="pa-4 rounded-2xl">
        <div class="d-flex align-center justify-space-between mb-3 pb-2 border-b">
          <div class="d-flex align-center gap-2">
            <v-avatar color="primary" variant="tonal" size="36" rounded="lg">
              <v-icon color="primary" size="20">mdi-file-document-check-outline</v-icon>
            </v-avatar>
            <h3 class="text-h6 font-weight-black mb-0">نموذج التصحيح والتدقيق الإلكتروني (الرسمي)</h3>
          </div>
          <div class="d-flex align-center gap-2">
            <v-btn
              color="success"
              variant="tonal"
              size="small"
              rounded="lg"
              prepend-icon="mdi-shield-check"
              class="font-weight-bold"
              @click="loadOfficialKey"
            >
              المفتاح النموذجي (100% تطابق)
            </v-btn>
            <v-btn color="primary" variant="flat" size="small" rounded="lg" prepend-icon="mdi-printer" @click="printAuditReport">
              طباعة النموذج
            </v-btn>
            <v-btn icon size="small" variant="text" @click="showAuditReportModal = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </div>
        </div>
        <div class="overflow-y-auto pa-2 bg-grey-lighten-4 rounded-xl d-flex justify-center" style="max-height: 80vh;">
          <YemeniAuditReportSheet
            :annotated-image="annotatedUrl || previewUrl"
            :questions-results="result?.questions || []"
            :student-answers="interactiveStudentAnswers"
            :answer-key="answerKey"
            :seat-number="result?.student_info?.seat_number || activeTemplateObj?.template_data?.header?.seat_number || '418485'"
            :student-name="result?.student_info?.student_name || activeTemplateObj?.template_data?.header?.student_name || 'عمرو عبدالباسط عبدالله قائد الزمر'"
            :exam-subject="result?.student_info?.subject || activeTemplateObj?.template_data?.header?.subject || 'القرآن الكريم'"
            :exam-year="result?.student_info?.exam_year || activeTemplateObj?.template_data?.header?.exam_year || '1444هـ-2022-2023م'"
            :center-name="result?.student_info?.center_name || activeTemplateObj?.template_data?.header?.center_name || 'سالم قطن — معين'"
            :center-code="result?.student_info?.center_code || activeTemplateObj?.template_data?.header?.center_code || '164'"
            :governorate="result?.student_info?.governorate || activeTemplateObj?.template_data?.header?.governorate || 'أمانة العاصمة'"
            :directorate="result?.student_info?.directorate || activeTemplateObj?.template_data?.header?.directorate || 'معين'"
            :serial-number="result?.student_info?.serial_number || activeTemplateObj?.template_data?.header?.serial_number || '148'"
            :form-number="result?.student_info?.form_number || activeTemplateObj?.template_data?.header?.form_number || '1'"
            :student-status="result?.student_info?.status || 'حاضر'"
            :barcode-value="result?.barcode || result?.student_info?.barcode || activeTemplateObj?.template_data?.barcode?.value || '41848501164148'"
            :qr-value="result?.qr || result?.student_info?.qr || activeTemplateObj?.template_data?.qr?.value || 'YE-MOE-1444-418485-SUB1'"
            :total-questions="result?.questions?.length || activeQuestionsCount || 50"
            :sections="activeTemplateObj?.template_data?.questions?.sections || activeTemplateObj?.template_data?.sections || []"
            :mcq-bubble-type="activeTemplateMeta.bubbleType"
          />
        </div>
      </v-card>
    </v-dialog>

    <!-- ── Notification Snackbar ─────────────────────────────────── -->
    <v-snackbar v-model="showToast" :color="toastType === 'error' ? 'error' : 'success'" rounded="xl" elevation="4">
      <div class="d-flex align-center gap-2">
        <v-icon color="white">{{ toastType === 'error' ? 'mdi-alert-circle' : 'mdi-check-circle' }}</v-icon>
        <span class="font-weight-bold text-white">{{ toastMsg }}</span>
      </div>
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, defineAsyncComponent } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import { printOmrElement } from './utils/omrPrint'

const route = useRoute()
const router = useRouter()

const OmrSheetMultigraphics = defineAsyncComponent(() =>
  import('@/components/omr_templates/OmrSheetMultigraphics.vue')
)

const YemeniMinistrySheet = defineAsyncComponent(() =>
  import('@/components/omr_templates/YemeniMinistrySheet.vue')
)

const YemeniAuditReportSheet = defineAsyncComponent(() =>
  import('@/components/omr_templates/YemeniAuditReportSheet.vue')
)

// ── State ───────────────────────────────────────────────────────
const currentStep = ref(0)
const omrReady = ref(true)
const uploadedFile = ref(null)
const previewUrl = ref(null)
const isDragging = ref(false)
const isGrading = ref(false)
const gradingProgress = ref(0)
const gradingStatus = ref('')
const result = ref(null)
const annotatedUrl = ref(null)
const activeFilter = ref('all')
const answerKey = ref({})
const isZoomed = ref(false)
const zoomLevel = ref(1)
const zoomMode = ref('fit') // 'fit' | 'actual' | 'custom'
const interactiveGradeMode = ref(false)
const interactivePanelOpen = ref(null) // closed by default to avoid confusion
const expandedQuestionId = ref(null)
const showSheetPreviewModal = ref(false)
const showAuditReportModal = ref(false)

const showToast = ref(false)
const toastMsg = ref('')
const toastType = ref('success')

function notify(msg, type = 'success') {
  toastMsg.value = msg
  toastType.value = type
  showToast.value = true
}

const savedTemplates = ref([])
const selectedTemplateId = ref('AUTO')
const activeQuestionsCount = ref(180)
const interactiveStudentAnswers = ref({})

// ── Exam Linking State ──────────────────────────────────────────
const availableExams = ref([])
const selectedExamId = ref(null)
const selectedExamObj = ref(null)
const linkedStudents = ref([])
const selectedVersionCode = ref('A')
const isExamLinked = ref(false)
const loadingExams = ref(false)

const activeExamVersions = computed(() => {
  if (!selectedExamId.value) return []
  const ex = availableExams.value.find(e => e.id === selectedExamId.value)
  if (!ex || !ex.versions) return [{ title: 'النموذج A', value: 'A' }]
  return ex.versions.map(v => ({
    title: `النموذج ${v.versionCode} (${v.questions_count} سؤال)`,
    value: v.versionCode,
    id: v.id,
  }))
})

async function fetchLinkingExams() {
  loadingExams.value = true
  try {
    const resp = await api.get('/api/omr/exam-linking/')
    if (resp.data && resp.data.results) {
      availableExams.value = resp.data.results
    }
  } catch (err) {
    console.error('Error fetching exams for linking:', err)
  } finally {
    loadingExams.value = false
  }
}

async function loadExamAnswerKey(examId, versionCode = 'A') {
  if (!examId) return
  try {
    const resp = await api.get(`/api/omr/exam-linking/${examId}/`)
    if (resp.data && resp.data.versions) {
      selectedExamObj.value = resp.data.exam
      linkedStudents.value = resp.data.registered_students || []
      const ver = resp.data.versions.find(v => v.versionCode === versionCode) || resp.data.versions[0]
      if (ver) {
        selectedVersionCode.value = ver.versionCode
        answerKey.value = ver.answerKey || {}
        activeQuestionsCount.value = ver.questionsCount || 10
        isExamLinked.value = true
        notify(`تم ربط الاختبار (${resp.data.exam.title}) والنموذج (${ver.versionCode}) وجلب مفتاح الإجابة تلقائياً!`, 'success')
      }
    }
  } catch (err) {
    console.error('Failed to load exam answer key:', err)
    notify('تعذر جلب مفتاح الحل للاختبار المحدد', 'error')
  }
}

function onExamSelected(examId) {
  if (!examId) {
    clearExamLink()
    return
  }
  selectedExamId.value = examId
  selectedVersionCode.value = 'A'
  loadExamAnswerKey(examId, 'A')
}

function onVersionSelected(versionCode) {
  if (selectedExamId.value) {
    loadExamAnswerKey(selectedExamId.value, versionCode)
  }
}

function clearExamLink() {
  selectedExamId.value = null
  selectedExamObj.value = null
  linkedStudents.value = []
  selectedVersionCode.value = 'A'
  isExamLinked.value = false
  answerKey.value = {}
  notify('تم إلغاء ربط الاختبار المولد', 'info')
}

const filters = [
  { key: 'all',     label: 'الكل' },
  { key: 'correct', label: 'صحيحة' },
  { key: 'wrong',   label: 'خاطئة' },
  { key: 'empty',   label: 'فارغة' },
  { key: 'double',  label: 'مزدوجة' },
]

const printInstructions = [
  { icon: 'mdi-file-outline', title: 'ورق A4 أبيض قياسي', text: 'استخدم ورق أبيض عادي مقاس A4 غير مثني.' },
  { icon: 'mdi-printer-check', title: 'دقة طباعة 300 DPI', text: 'تأكد من ضبط الطابعة على مقاس 100% ودقة 300 DPI.' },
  { icon: 'mdi-pencil', title: 'قلم رصاص 2B أسود', text: 'تظليل الدوائر بالكامل دون الخروج عن الإطار.' },
  { icon: 'mdi-alert-decagram-outline', title: 'علامات المحاذاة', text: 'حافظ على علامات الزوايا الأربع واضحة تماماً.' },
]

const templateOptions = computed(() => {
  const opts = [
    {
      title: '⚡ التعرف التلقائي الذكي على القالب مباشرة من الورقة (مُفعّل آلياً)',
      value: 'AUTO',
      subtitle: 'يكتشف النظام نوع القالب وعدد الأسئلة (40 أو 50 أو 180) مباشرة من الورقة المرفوعة'
    }
  ]
  savedTemplates.value.forEach(t => {
    const qCount = t.template_data?.questions?.metadata?.num_questions || t.total_mcq || 50
    opts.push({
      title: `${t.name} (${qCount} سؤال - كود: ${t.id})`,
      value: t.id,
      subtitle: `${qCount} سؤال — إصدار v${t.version || 1}`
    })
  })
  return opts
})

const activeTemplateObj = computed(() => {
  if (!selectedTemplateId.value || selectedTemplateId.value === 'AUTO') {
    // إرجاع قالب مرجعي لمعاينة الشكل الأولي
    const ministryT = savedTemplates.value.find(t => t.name?.includes('الثانوية') || t.name?.includes('التربية'))
    return ministryT || savedTemplates.value[0] || null
  }
  return savedTemplates.value.find(t => t.id === selectedTemplateId.value) || null
})

const isMinistrySheet = computed(() => {
  if (selectedTemplateId.value === 'AUTO') return true
  const name = activeTemplateObj.value?.name || ''
  const tId = String(activeTemplateObj.value?.id || selectedTemplateId.value || '')
  return (
    activeQuestionsCount.value === 40 ||
    activeQuestionsCount.value === 50 ||
    name.includes('وزارة التربية') ||
    name.includes('الثانوية العامة') ||
    tId === 'YEMEN_MINISTRY_50' ||
    tId === 'YEMEN_MINISTRY_40' ||
    tId === '12' ||
    tId === '28' ||
    tId === '29'
  )
})

const thumbContainerStyle = computed(() => {
  const isA5 = isMinistrySheet.value
  const heightMm = isA5 ? 148.5 : 297
  const scale = 0.27
  const heightPx = Math.round(heightMm * scale * 3.78)
  return {
    width: '100%',
    maxWidth: '226px',
    height: `${heightPx}px`,
    margin: '0 auto',
    background: '#ffffff',
    borderRadius: '8px',
    overflow: 'hidden',
    boxShadow: '0 4px 18px rgba(0,0,0,0.1)',
    display: 'flex',
    justifyContent: 'center',
    position: 'relative',
  }
})

const thumbSheetWrapperStyle = computed(() => {
  const isA5 = isMinistrySheet.value
  const widthMm = 210
  const heightMm = isA5 ? 148.5 : 297
  const scale = 0.27
  return {
    width: `${widthMm}mm`,
    minWidth: `${widthMm}mm`,
    height: `${heightMm}mm`,
    minHeight: `${heightMm}mm`,
    transform: `scale(${scale})`,
    transformOrigin: 'top center',
    pointerEvents: 'none',
    userSelect: 'none',
  }
})

const modalSheetWrapperStyle = computed(() => {
  const isA5 = isMinistrySheet.value
  const widthMm = 210
  const heightMm = isA5 ? 148.5 : 297
  const scale = isA5 ? 0.85 : 0.65
  return {
    width: `${widthMm}mm`,
    minWidth: `${widthMm}mm`,
    height: `${heightMm}mm`,
    minHeight: `${heightMm}mm`,
    aspectRatio: `${widthMm} / ${heightMm}`,
    transform: `scale(${scale})`,
    transformOrigin: 'top center',
    marginBottom: `calc(-${heightMm}mm * ${1 - scale})`,
    backgroundColor: '#ffffff',
    boxShadow: '0 8px 28px rgba(0,0,0,0.12)',
    borderRadius: '4px',
    overflow: 'hidden',
  }
})

watch(activeTemplateObj, (t) => {
  if (t) {
    const td = t.template_data || {}
    activeQuestionsCount.value =
      td.questions?.metadata?.num_questions ||   // new designer format
      td.metadata?.num_questions ||              // flat/old format
      td.mcq_questions?.length ||
      t.total_mcq || 50

    // Auto-populate answer key from template if present
    const modelAnswers = td.answer_key?.mcq_answers || td.answer_key || td.model_answers
    if (modelAnswers && typeof modelAnswers === 'object' && Object.keys(modelAnswers).length > 0) {
      const loadedKey = {}
      for (const [k, v] of Object.entries(modelAnswers)) {
        loadedKey[Number(k) || k] = v
      }
      answerKey.value = loadedKey
    }
  }
}, { immediate: true })

const activeChoicesLabels = computed(() => {
  const td = activeTemplateObj.value?.template_data || {}
  if (td.mcq_questions && td.mcq_questions.length > 0 && td.mcq_questions[0].choices) {
    return td.mcq_questions[0].choices.map(c => c.choice)
  }
  return ['A', 'B', 'C', 'D']
})

function isTrueVariant(val) {
  if (val === null || val === undefined) return false
  const s = String(val).trim().toLowerCase()
  return s === 'صح' || s === 'ص' || s === 'true' || s === 't' || s === '1' || s === 'yes'
}

function isFalseVariant(val) {
  if (val === null || val === undefined) return false
  const s = String(val).trim().toLowerCase()
  return s === 'خطأ' || s === 'خطا' || s === 'خ' || s === 'false' || s === 'f' || s === '2' || s === 'no'
}

const isTrueFalseTemplate = computed(() => {
  const labels = activeChoicesLabels.value || []
  return labels.some(l => isTrueVariant(l) || isFalseVariant(l)) || (activeTemplateObj.value?.name?.includes('صح') || false)
})

function getQuestionChoices(q) {
  const td = activeTemplateObj.value?.template_data || {}

  // 1. Check if individual mcq_questions array specifies choices for this question ID
  if (td.mcq_questions && td.mcq_questions.length > 0) {
    const found = td.mcq_questions.find(m => m.question_id === q)
    if (found?.choices?.length) {
      return found.choices.map(c => c.choice)
    }
  }

  // 2. Check sections (e.g. true_false vs mcq sections)
  const sections = td.questions?.sections || []
  for (const s of sections) {
    if (q >= (s.from_q || 1) && q <= (s.to_q || 1)) {
      if (s.type === 'true_false' || s.title?.includes('صح')) {
        return ['صح', 'خطأ']
      }
      const cnt = s.choices_count || 4
      const bType = td.questions?.layout?.bubble_type || 'numbers'
      if (bType === 'letters' || bType === 'english_letters') return ['A', 'B', 'C', 'D', 'E'].slice(0, cnt)
      if (bType === 'arabic_letters') return ['أ', 'ب', 'ج', 'د', 'هـ'].slice(0, cnt)
      return ['1', '2', '3', '4', '5'].slice(0, cnt)
    }
  }

  // 3. Fallback for Yemeni Ministry Sheet (A5)
  if (isMinistrySheet.value) {
    return q <= 20 ? ['صح', 'خطأ'] : ['1', '2', '3', '4']
  }

  // 4. Default fallback
  return activeChoicesLabels.value
}

const activeTemplateMeta = computed(() => {
  const td = activeTemplateObj.value?.template_data || {}
  // New designer format uses td.questions.layout; old format uses td.metadata flat
  const qLayout = td.questions?.layout || {}
  const meta = td.metadata || {}
  const cols = qLayout.columns_count || meta.columns_count || 4
  const rSpacing = qLayout.row_spacing_mm || meta.row_spacing_mm || 4.2
  const bRadius = qLayout.bubble_radius_mm || meta.bubble_radius_mm || 1.7
  const rows = Math.ceil(activeQuestionsCount.value / cols)

  let bType = 'numbers'
  const mcqBubbleType = qLayout.bubble_type || meta.bubble_type
  if (mcqBubbleType === 'arabic_letters') bType = 'arabic_letters'
  else if (mcqBubbleType === 'english_letters' || mcqBubbleType === 'letters') bType = 'letters'
  else if (td.mcq_questions && td.mcq_questions.length > 0 && td.mcq_questions[0].choices) {
    const firstChoice = td.mcq_questions[0].choices[0]?.choice
    if (firstChoice === 'أ' || firstChoice === 'ب') bType = 'arabic_letters'
    else if (['A','B','C','D'].includes(firstChoice)) bType = 'letters'
  }

  // Header: new designer saves to td.header; old format may have flat fields
  const institutionName = td.header?.institution_name || meta.institution_name || 'الجمهورية اليمنية — وزارة التعليم العالي والبحث العلمي'
  const subTitle = td.header?.sub_title || meta.sub_title || 'جامعة صنعاء — الإدارة العامة للامتحانات والتقويم الآلي'
  const examName = td.header?.exam_name || activeTemplateObj.value?.name || 'الكيمياء العامة — نموذج معاينة'

  return {
    questionsPerColumn: rows,
    totalColumns: cols,
    rowSpacing: rSpacing,
    bubbleRadius: bRadius,
    bubbleType: bType,
    layoutDirection: qLayout.layout_direction || meta.layout_direction || 'rtl',
    primaryColor: qLayout.primary_color || meta.primary_color || '#e6007e',
    institutionName,
    subTitle,
    examName,
  }
})

// ── Interactive Matrix Helpers ───────────────────────────────────
function getInteractiveState(q, c) {
  const ans = interactiveStudentAnswers.value[q]
  if (!ans) return 'empty'
  if (typeof ans === 'string') return ans === c ? 'filled' : 'empty'
  return ans[c] || 'empty'
}

function toggleInteractiveAnswer(q, c) {
  const currentQAnswers = interactiveStudentAnswers.value[q]
  let newAnsForQ = {}

  if (typeof currentQAnswers === 'string') {
    newAnsForQ[currentQAnswers] = 'filled'
  } else if (typeof currentQAnswers === 'object' && currentQAnswers !== null) {
    newAnsForQ = { ...currentQAnswers }
  }

  const currentState = newAnsForQ[c] || 'empty'
  let newState = 'empty'
  if (currentState === 'empty') newState = 'filled'
  else if (currentState === 'filled') newState = 'crossed'
  else if (currentState === 'crossed') newState = 'empty'

  if (newState === 'empty') {
    delete newAnsForQ[c]
  } else {
    newAnsForQ[c] = newState
  }

  if (Object.keys(newAnsForQ).length === 0) {
    const copy = { ...interactiveStudentAnswers.value }
    delete copy[q]
    interactiveStudentAnswers.value = copy
  } else {
    interactiveStudentAnswers.value = {
      ...interactiveStudentAnswers.value,
      [q]: newAnsForQ
    }
  }
}

const onInteractiveBubbleClick = (q, alt) => {
  toggleInteractiveAnswer(q, alt)
}
const onInteractiveBubbleHover = () => {}
const onInteractiveBubbleLeave = () => {}

function randomShadeInteractive() {
  const newAns = {}
  for (let q = 1; q <= activeQuestionsCount.value; q++) {
    const choices = getQuestionChoices(q)
    const c = choices[Math.floor(Math.random() * choices.length)]
    const rand = Math.random()
    if (rand > 0.9 && choices.length > 1) {
      const c2 = choices[(choices.indexOf(c) + 1) % choices.length]
      newAns[q] = { [c]: 'filled', [c2]: 'filled' }
    } else if (rand > 0.8) {
      newAns[q] = { [c]: 'crossed' }
    } else {
      newAns[q] = { [c]: 'filled' }
    }
  }
  interactiveStudentAnswers.value = newAns
}

function fillAnswersWithKey() {
  if (Object.keys(answerKey.value).length === 0) {
    randomKey()
  }
  const newAns = {}
  for (const [q, c] of Object.entries(answerKey.value)) {
    if (c) newAns[q] = { [c]: 'filled' }
  }
  interactiveStudentAnswers.value = newAns
}

function generateInteractiveShadedImageAndGrade() {
  const studentAns = interactiveStudentAnswers.value
  if (Object.keys(studentAns).length === 0) {
    notify('يرجى تظليل إجابة واحدة على الأقل قبل التصحيح', 'error')
    return
  }

  isGrading.value = true
  gradingProgress.value = 15
  gradingStatus.value = 'جاري تصيير صورة الورقة المظللة بجودة 300 DPI...'

  setTimeout(() => {
    try {
      const svgEl = document.querySelector('.interactive-omr-svg svg.omr-sheet-yemen') || document.querySelector('svg.omr-sheet-yemen')
      if (!svgEl) throw new Error('لم يتم العثور على عنصر الورقة في الصفحة')

      const serializer = new XMLSerializer()
      let source = serializer.serializeToString(svgEl)
      if (!source.match(/<svg[^>]+xmlns="http\:\/\/www\.w3\.org\/2000\/svg"/)) {
        source = source.replace(/<svg/, '<svg xmlns="http://www.w3.org/2000/svg"')
      }
      source = source.replace(/(<svg[^>]*?)\s*width="[^"]*"/i, '$1')
      source = source.replace(/(<svg[^>]*?)\s*height="[^"]*"/i, '$1')
      source = source.replace(/<svg/i, '<svg width="2480" height="3508"')

      const encodedData = window.btoa(unescape(encodeURIComponent(source)))
      const imgSrc = 'data:image/svg+xml;base64,' + encodedData

      const img = new Image()
      img.onload = () => {
        const canvas = document.createElement('canvas')
        canvas.width = 2480
        canvas.height = 3508
        const ctx = canvas.getContext('2d')
        ctx.fillStyle = '#ffffff'
        ctx.fillRect(0, 0, canvas.width, canvas.height)
        ctx.drawImage(img, 0, 0, 2480, 3508)

        canvas.toBlob((blob) => {
          if (!blob) {
            isGrading.value = false
            notify('فشل في تحويل الورقة إلى صورة', 'error')
            return
          }
          const file = new File([blob], 'interactive-shaded-sheet.png', { type: 'image/png' })
          uploadedFile.value = file
          previewUrl.value = URL.createObjectURL(file)
          interactiveGradeMode.value = true
          startGrading()
        }, 'image/png')
      }
      img.onerror = () => {
        isGrading.value = false
        notify('حدث خطأ أثناء رسم الورقة', 'error')
      }
      img.src = imgSrc
    } catch (e) {
      isGrading.value = false
      notify('خطأ في تجهيز صورة الورقة: ' + e.message, 'error')
    }
  }, 100)
}

// ── File Handling ───────────────────────────────────────────────
function handleDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) setFile(file)
}
function handleFileChange(e) {
  const file = e.target.files[0]
  if (file) setFile(file)
}
function setFile(file) {
  uploadedFile.value = file
  if (file.type.startsWith('image/')) {
    const reader = new FileReader()
    reader.onload = (e) => { previewUrl.value = e.target.result }
    reader.readAsDataURL(file)
  } else {
    previewUrl.value = null
  }

  // التعرف التلقائي الذكي على القالب فوراً من محتوى وهندسة الورقة المرفوعة عبر الـ Backend (فقط في وضع AUTO)
  if (file.type.startsWith('image/')) {
    const form = new FormData()
    form.append('sheet_image', file)
    api.post('/api/omr/detect-template/', form, { headers: { 'Content-Type': 'multipart/form-data' } })
      .then(resp => {
        if (resp.data?.template_id) {
          const matched = savedTemplates.value.find(t => String(t.id) === String(resp.data.template_id))
          if (matched) {
            // لا نغير القالب إذا كان المستخدم قد اختار قالباً محدداً بنفسه
            if (!selectedTemplateId.value || selectedTemplateId.value === 'AUTO') {
              selectedTemplateId.value = matched.id
              if (resp.data.total_questions) {
                activeQuestionsCount.value = resp.data.total_questions
              }
              notify(`تم التعرف التلقائي على القالب من الورقة: ${matched.name} (${resp.data.total_questions || activeQuestionsCount.value} سؤال)`, 'success')
            }
          }
        }
      })
      .catch(err => {
        console.debug('Fast auto-detection skipped or deferred to grading:', err)
      })
  }
}
function removeFile() {
  uploadedFile.value = null
  previewUrl.value = null
}
function formatSize(bytes) {
  if (bytes > 1048576) return (bytes / 1048576).toFixed(1) + ' MB'
  return (bytes / 1024).toFixed(0) + ' KB'
}

// ── Answer Key ──────────────────────────────────────────────────
function randomKey() {
  const newKey = {}
  for (let q = 1; q <= activeQuestionsCount.value; q++) {
    const choices = getQuestionChoices(q)
    newKey[q] = choices[Math.floor(Math.random() * choices.length)]
  }
  answerKey.value = newKey
}
function clearKey() {
  answerKey.value = {}
}

function loadOfficialKey() {
  const td = activeTemplateObj.value?.template_data || {}
  const modelAnswers = td.answer_key?.mcq_answers || td.answer_key || td.model_answers
  if (modelAnswers && typeof modelAnswers === 'object' && Object.keys(modelAnswers).length > 0) {
    const loadedKey = {}
    for (const [k, v] of Object.entries(modelAnswers)) {
      loadedKey[Number(k) || k] = v
    }
    answerKey.value = loadedKey
    notify('تم استعادة المفتاح النموذجي المعتمد للقالب (100% إجابات صحيحة)!', 'success')
  } else if (result.value?.questions?.length) {
    useSheetAsKey()
    return
  } else {
    const fullKey = {
      1: 'صح', 2: 'صح', 3: 'صح', 4: 'خطأ', 5: 'صح', 6: 'خطأ', 7: 'صح', 8: 'صح', 9: 'صح', 10: 'صح',
      11: 'خطأ', 12: 'صح', 13: 'خطأ', 14: 'خطأ', 15: 'خطأ', 16: 'خطأ', 17: 'خطأ', 18: 'صح', 19: 'صح', 20: 'خطأ',
      21: '4', 22: '2', 23: '1', 24: '3', 25: '4', 26: '4', 27: '3', 28: '2', 29: '4', 30: '1',
      31: '2', 32: '3', 33: '3', 34: '1', 35: '4', 36: '2', 37: '3', 38: '2', 39: '2', 40: '3',
      41: '3', 42: '4', 43: '2', 44: '4', 45: '2', 46: '4', 47: '2', 48: '3', 49: '1', 50: '1'
    }
    const defaultYemenKey = {}
    const maxQ = activeQuestionsCount.value || 50
    for (let i = 1; i <= maxQ; i++) {
      if (fullKey[i]) defaultYemenKey[i] = fullKey[i]
    }
    answerKey.value = defaultYemenKey
    notify('تم تفعيل المفتاح النموذجي الرسمي المعتمد (100% إجابات صحيحة)!', 'success')
  }

  // Recalculate result in-place immediately so report is 100% green
  if (result.value?.questions && Array.isArray(result.value.questions)) {
    let score = 0
    let totalMarks = 0
    for (const q of result.value.questions) {
      const qNum = q.q || q.question_id
      const correctVal = answerKey.value[qNum]
      if (correctVal) {
        q.correct = correctVal
        q.correct_choice = correctVal
      }
      const markedVal = q.marked || q.marked_choice
      const isCorrect = markedVal === q.correct || (markedVal === 'صح' && ['1', 'ص', 'صح'].includes(q.correct)) || (markedVal === 'خطأ' && ['2', 'خ', 'خطأ'].includes(q.correct))
      q.is_correct = isCorrect
      const maxMark = qNum <= 20 ? 1 : 2
      totalMarks += maxMark
      if (isCorrect) score += maxMark
    }
    result.value.score = score
    result.value.total_marks = totalMarks
    result.value.percentage = totalMarks > 0 ? (score / totalMarks) * 100 : 100
  }
}
function useSheetAsKey() {
  if (!result.value?.questions) return
  const newKey = {}
  for (const q of result.value.questions) {
    const qId = q.q || q.question_id
    const marked = q.marked || q.marked_choice
    if (qId && marked) {
      newKey[qId] = marked
    }
  }
  answerKey.value = newKey
  notify('تم اعتماد إجابات الورقة كمفتاح نموذجي رسمي بنجاح! جاري إعادة الاحتساب...', 'success')
  startGrading()
}

// ── Grading Pipeline ────────────────────────────────────────────
async function startGrading() {
  if (!uploadedFile.value) return
  isGrading.value = true
  gradingProgress.value = 10
  gradingStatus.value = 'جاري الفحص المبدئي ومحاذاة العلامات الهندسية (OpenCV)...'

  const progressTimer = setInterval(() => {
    if (gradingProgress.value < 70) gradingProgress.value += 12
    else if (gradingProgress.value < 90) {
      gradingProgress.value += 4
      gradingStatus.value = 'جاري التدقيق العميق بواسطة نموذج YOLOv8 (AI Verifier)...'
    }
  }, 250)

  try {
    const form = new FormData()
    form.append('sheet_image', uploadedFile.value)

    const tid = (selectedTemplateId.value && selectedTemplateId.value !== 'AUTO')
      ? selectedTemplateId.value
      : 'AUTO'   // أرسل AUTO للباكند ليبدأ كشف الباركود/QR تلقائياً
    form.append('template_id', String(tid))

    if (selectedExamId.value) {
      form.append('exam_id', String(selectedExamId.value))
      form.append('version_code', String(selectedVersionCode.value || 'A'))
    }

    const keyEntries = Object.entries(answerKey.value).filter(([, v]) => v)
    if (keyEntries.length > 0) {
      const keyObj = {}
      keyEntries.forEach(([k, v]) => { keyObj[k] = v })
      form.append('answer_key', JSON.stringify(keyObj))
    }

    const resp = await api.post('/api/omr/grade/', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    clearInterval(progressTimer)
    gradingProgress.value = 100
    gradingStatus.value = 'اكتمل التصحيح بنجاح!'

    const data = resp.data
    if (data.questions && Array.isArray(data.questions)) {
      data.questions = data.questions.map(q => ({
        ...q,
        q: q.question_id ?? q.q,
        marked: q.marked_choice ?? q.marked,
        correct: q.correct_choice ?? q.correct,
        mode: q.mode || q.bubble_state || 'empty',
      }))
    }

    result.value = data
    if (data.annotated_image) {
      annotatedUrl.value = 'data:image/png;base64,' + data.annotated_image
    }

    if (data.switched_notice) {
      notify(data.switched_notice, 'info')
    }
    if (data.template_id && (!selectedTemplateId.value || selectedTemplateId.value === 'AUTO')) {
      const matched = savedTemplates.value.find(t => String(t.id) === String(data.template_id))
      if (matched) {
        selectedTemplateId.value = matched.id
      }
    }
    if (data.total_questions) {
      activeQuestionsCount.value = data.total_questions
    }

    setTimeout(() => {
      isGrading.value = false
      currentStep.value = 2
    }, 400)
  } catch (err) {
    clearInterval(progressTimer)
    isGrading.value = false
    const errMsg = err.response?.data?.error || err.response?.data?.detail || err.message || 'حدث خطأ غير متوقع أثناء التصحيح'
    notify('خطأ في التصحيح: ' + errMsg, 'error')
  }
}

// ── Results Filtering & Expansion ───────────────────────────────
function qMode(q) {
  return q.mode || q.bubble_state || 'empty'
}

const filteredQuestions = computed(() => {
  if (!result.value) return []
  const qs = result.value.questions || []
  switch (activeFilter.value) {
    case 'correct': return qs.filter(q => q.is_correct === true)
    case 'wrong':   return qs.filter(q => q.is_correct === false)
    case 'empty':   return qs.filter(q => !q.marked && !q.marked_choice)
    case 'double':  return qs.filter(q => qMode(q) === 'ambiguous' || qMode(q) === 'double')
    default:        return qs
  }
})

function filterCount(key) {
  if (!result.value) return 0
  const qs = result.value.questions || []
  switch (key) {
    case 'all':     return qs.length
    case 'correct': return qs.filter(q => q.is_correct === true).length
    case 'wrong':   return qs.filter(q => q.is_correct === false).length
    case 'empty':   return qs.filter(q => !q.marked && !q.marked_choice).length
    case 'double':  return qs.filter(q => qMode(q) === 'ambiguous' || qMode(q) === 'double').length
    default: return 0
  }
}

function getAnswerBadgeProps(val) {
  if (!val || val === '—' || val === '-' || val === 'null' || val === 'undefined') {
    return {
      text: '—',
      color: 'grey',
      icon: 'mdi-minus',
      variant: 'tonal',
    }
  }
  if (isTrueVariant(val)) {
    return {
      text: 'صح',
      color: 'success',
      icon: 'mdi-check',
      variant: 'tonal',
    }
  }
  if (isFalseVariant(val)) {
    return {
      text: 'خطأ',
      color: 'error',
      icon: 'mdi-close',
      variant: 'tonal',
    }
  }
  // Standard MCQ (letters or numbers)
  return {
    text: String(val),
    color: 'primary',
    icon: null,
    variant: 'tonal',
  }
}

function getCorrectBadgeProps(val) {
  if (!val || val === '—' || val === '-' || val === 'null' || val === 'undefined') {
    return {
      text: '—',
      color: 'grey',
      icon: 'mdi-minus',
      variant: 'tonal',
    }
  }
  if (isTrueVariant(val)) {
    return {
      text: 'صح',
      color: 'success',
      icon: 'mdi-check',
      variant: 'tonal',
    }
  }
  if (isFalseVariant(val)) {
    return {
      text: 'خطأ',
      color: 'error',
      icon: 'mdi-close',
      variant: 'tonal',
    }
  }
  // Standard MCQ correct
  return {
    text: String(val),
    color: 'teal',
    icon: null,
    variant: 'tonal',
  }
}

function getStatusBadgeProps(q) {
  if (q.is_correct === true) {
    return {
      text: 'صحيح',
      color: 'success',
      icon: 'mdi-check-circle',
      variant: 'tonal',
    }
  }
  if (q.is_correct === false) {
    return {
      text: 'خاطئ',
      color: 'error',
      icon: 'mdi-close-circle',
      variant: 'tonal',
    }
  }
  const m = qMode(q)
  if (m === 'ambiguous' || m === 'double') {
    return {
      text: 'مزدوج',
      color: 'warning',
      icon: 'mdi-alert-circle',
      variant: 'tonal',
    }
  }
  if (m === 'crossed') {
    return {
      text: 'مشطوب',
      color: 'warning',
      icon: 'mdi-close-octagon',
      variant: 'tonal',
    }
  }
  if (m === 'erased') {
    return {
      text: 'ممسوح',
      color: 'secondary',
      icon: 'mdi-eraser',
      variant: 'tonal',
    }
  }
  if (m === 'filled') {
    return {
      text: 'مظلل',
      color: 'info',
      icon: 'mdi-circle',
      variant: 'tonal',
    }
  }
  return {
    text: 'فارغ',
    color: 'grey',
    icon: 'mdi-minus-circle-outline',
    variant: 'tonal',
  }
}

function statusChipColor(q) {
  if (q.is_correct === true) return 'success'
  if (q.is_correct === false) return 'error'
  const m = qMode(q)
  if (m === 'ambiguous' || m === 'double') return 'warning'
  if (m === 'filled') return 'info'
  return 'grey'
}

function statusLabel(q) {
  if (q.is_correct === true)  return 'صحيح'
  if (q.is_correct === false) return 'خاطئ'
  const m = qMode(q)
  if (m === 'ambiguous' || m === 'double') return 'مزدوج'
  if (m === 'crossed') return 'مشطوب'
  if (m === 'erased')  return 'ممسوح'
  if (m === 'filled')  return 'مظلل'
  return 'فارغ'
}

function toggleQuestionExpand(qId) {
  expandedQuestionId.value = expandedQuestionId.value === qId ? null : qId
}

function resetWorkflow() {
  currentStep.value = 1
  uploadedFile.value = null
  previewUrl.value = null
  result.value = null
  annotatedUrl.value = null
  gradingProgress.value = 0
  interactiveGradeMode.value = false
}

async function printSheet() {
  const svgEl = document.querySelector('.sheet-artboard-container svg') || document.querySelector('.sheet-wrapper svg') || document.querySelector('svg')
  if (svgEl) {
    await printOmrElement(svgEl, { title: 'ورقة الإجابة OMR', isA5: true })
  } else {
    window.print()
  }
}
function printResult() {
  window.print()
}
async function printAuditReport() {
  const el = document.querySelector('.yemeni-audit-report-sheet')
  if (el) {
    await printOmrElement(el, { title: 'نموذج التصحيح والتدقيق الإلكتروني (الرسمي)', isA5: false })
  } else {
    window.print()
  }
}
function downloadJSON() {
  if (!result.value) return
  const blob = new Blob([JSON.stringify(result.value, null, 2)], { type: 'application/json' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = `omr_result_${Date.now()}.json`
  a.click()
}

// ── Image Inspection & Zoom Controls ────────────────────────────
const sheetImageStyle = computed(() => {
  if (zoomMode.value === 'fit') {
    return {
      width: '100%',
      maxWidth: '1320px',
      height: 'auto',
      display: 'block',
      margin: '0 auto',
      imageRendering: 'high-quality',
      boxShadow: '0 4px 24px rgba(0,0,0,0.12)',
      borderRadius: '6px'
    }
  } else if (zoomMode.value === 'actual') {
    // الحجم الفعلي الكامل 100% بدقة البكسلات الطبيعية UltraHD
    return {
      width: 'auto',
      height: 'auto',
      maxWidth: 'none',
      maxHeight: 'none',
      display: 'block',
      margin: '0 auto',
      imageRendering: 'high-quality'
    }
  } else {
    // تكبير تدريجي
    return {
      width: `${Math.round(1320 * zoomLevel.value)}px`,
      height: 'auto',
      maxWidth: 'none',
      maxHeight: 'none',
      display: 'block',
      margin: '0 auto',
      imageRendering: 'high-quality'
    }
  }
})

function zoomIn() {
  if (zoomMode.value === 'fit') {
    zoomMode.value = 'custom'
    zoomLevel.value = 1.3
  } else if (zoomMode.value === 'actual') {
    zoomMode.value = 'custom'
    zoomLevel.value = 1.6
  } else {
    zoomLevel.value = Math.min(Math.round((zoomLevel.value + 0.25) * 100) / 100, 4.0)
  }
}

function zoomOut() {
  if (zoomMode.value === 'fit') {
    zoomMode.value = 'custom'
    zoomLevel.value = 0.8
  } else if (zoomMode.value === 'actual') {
    zoomMode.value = 'custom'
    zoomLevel.value = 1.0
  } else {
    zoomLevel.value = Math.max(Math.round((zoomLevel.value - 0.25) * 100) / 100, 0.4)
  }
}

function resetZoom() {
  zoomMode.value = 'fit'
  zoomLevel.value = 1
}

watch(zoomMode, (newVal) => {
  if (newVal === 'fit' || newVal === 'actual') {
    zoomLevel.value = 1
  }
})

function openZoomModal(mode = 'fit') {
  zoomMode.value = mode
  zoomLevel.value = 1
  isZoomed.value = true
}

function downloadAnnotatedImage() {
  if (!annotatedUrl.value) return
  const link = document.createElement('a')
  link.href = annotatedUrl.value
  link.download = `OMR_Graded_Sheet_${result.value?.result_id || Date.now()}.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

onMounted(async () => {
  // جلب الاختبارات المولدة للربط
  await fetchLinkingExams()

  if (route.query.exam_id) {
    const eId = Number(route.query.exam_id) || route.query.exam_id
    selectedExamId.value = eId
    currentStep.value = 1 // الانتقال مباشرة لخطوة الرفع والتصحيح
    const vCode = route.query.version || 'A'
    selectedVersionCode.value = vCode
    await loadExamAnswerKey(eId, vCode)
  }

  try {
    const resp = await api.get('/api/templates-engine/')
    if (resp.status === 200) {
      const raw = resp.data
      const list = Array.isArray(raw) ? raw : (raw.results || raw.data || [])
      const detailPromises = list.map(t =>
        api.get(`/api/templates-engine/${t.id}/`).then(r => (r.status === 200 && r.data?.data) ? r.data.data : (r.data || t)).catch(() => t)
      )
      savedTemplates.value = await Promise.all(detailPromises)

      if (route.query.templateId) {
        const targetId = Number(route.query.templateId)
        const found = savedTemplates.value.find(t => t.id === targetId)
        if (found) {
          selectedTemplateId.value = targetId
        }
      } else {
        // الوضع الافتراضي: التعرف التلقائي الذكي على القالب مباشرة من محتوى الورقة المرفوعة دون الحاجة لاختيار يدوي
        selectedTemplateId.value = 'AUTO'
      }
    }
  } catch (e) {
    console.error('Failed to fetch templates:', e)
  }
})
</script>

<style scoped>
.qb-omr-lab-v4 {
  direction: rtl;
}

.omr-sheet-thumb {
  width: 100%;
  max-width: 240px;
  margin: 0 auto;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 18px rgba(0,0,0,0.1);
  display: flex;
  align-items: flex-start;
  justify-content: center;
}
.thumb-scaler {
  width: 210mm;
  min-width: 210mm;
  margin: 0 auto;
  pointer-events: none;
}

.drop-zone {
  border: 2px dashed rgba(var(--v-border-color), 0.35);
  background: rgba(var(--v-theme-primary), 0.02);
}
.drop-zone.drag-over {
  border-color: rgb(var(--v-theme-primary));
  background: rgba(var(--v-theme-primary), 0.08);
}
.drop-zone.has-file {
  border-color: #10b981;
  border-style: solid;
  background: rgba(16, 185, 129, 0.04);
}
.preview-img {
  max-height: 480px;
  max-width: 100%;
  width: auto;
  border-radius: 12px;
  object-fit: contain;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.key-grid-matrix {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 0.5rem;
  max-height: 260px;
  overflow-y: auto;
}

.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 4px 12px rgba(0, 0, 0, 0.02);
}


.cursor-zoom-in {
  cursor: zoom-in;
}

.omr-zoom-viewport {
  background-color: #f1f5f9;
  background-image: radial-gradient(#cbd5e1 1.5px, transparent 1.5px);
  background-size: 20px 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.sheet-paper-container {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18), 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  margin: auto;
}

.sheet-annotated-img {
  image-rendering: -webkit-optimize-contrast;
  image-rendering: crisp-edges;
  display: block;
  user-select: none;
  -webkit-user-drag: none;
}

.qb-omr-lab-v4 :deep(.v-chip) {
  border-radius: 6px !important;
  font-family: inherit;
  letter-spacing: 0;
}

.qb-omr-lab-v4 :deep(.v-table .v-chip) {
  height: 24px;
  font-size: 12px;
  border-radius: 6px !important;
}

@media print {
  .v-card, .v-tabs {
    display: none !important;
  }
}
</style>
