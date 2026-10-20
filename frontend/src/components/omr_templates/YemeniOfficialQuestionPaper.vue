<template>
  <div
    ref="paperRootRef"
    class="yemeni-official-question-paper bg-white text-black"
    :class="{ 'a3-spread-mode': isA3Landscape, 'a4-portrait-mode': !isA3Landscape }"
    dir="rtl"
  >
    <!-- ── Print Action Toolbar (Hidden during printing) ────────── -->
    <div v-if="!hideToolbar" class="d-print-none action-bar px-4 py-2 mb-3 rounded-lg border bg-grey-lighten-4 d-flex align-center justify-space-between flex-wrap gap-2">
      <div class="d-flex align-center gap-2">
        <v-avatar color="primary" variant="tonal" size="32" rounded="lg">
          <v-icon size="18">mdi-newspaper-variant-outline</v-icon>
        </v-avatar>
        <span class="text-subtitle-2 font-weight-black">
          ورقة الأسئلة الرسمية المعتمدة — وزارة التربية والتعليم
          <v-chip size="x-small" color="primary" variant="flat" class="ms-2 font-weight-bold">
            {{ isEnglish ? 'Exam in English' : 'اختبار باللغة العربية' }}
          </v-chip>
        </span>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <v-btn-toggle
          v-model="paperSizeSetting"
          mandatory
          density="compact"
          color="primary"
          variant="outlined"
          rounded="lg"
        >
          <v-btn value="a4" size="small" class="font-weight-bold" prepend-icon="mdi-file-outline">
            مقاس A4 (النمط الوزاري المعتمد)
          </v-btn>
          <v-btn value="a3" size="small" class="font-weight-bold" prepend-icon="mdi-file-document-outline">
            مقاس كبير A3 (ورقة واحدة عمودين)
          </v-btn>
        </v-btn-toggle>

        <v-btn
          color="primary"
          size="small"
          rounded="lg"
          class="font-weight-bold px-4"
          prepend-icon="mdi-printer"
          @click="printOfficialPaper"
        >
          طباعة ورقة الأسئلة الرسمية
        </v-btn>
      </div>
    </div>

    <!-- ════════════════════════════════════════════════════════════ -->
    <!-- ── DEVELOPER DIAGNOSTICS & EXAM READINESS CHECKLIST BAR ── -->
    <!-- ════════════════════════════════════════════════════════════ -->
    <div v-if="showDiagnostics" class="developer-diagnostics-card d-print-none mb-3 pa-3 rounded-lg border bg-white elevation-1">
      <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-2">
        <div class="d-flex align-center gap-2">
          <v-icon :color="missingFieldsCount === 0 ? 'success' : 'warning'" size="22">
            {{ missingFieldsCount === 0 ? 'mdi-check-decagram' : 'mdi-alert-circle-outline' }}
          </v-icon>
          <div>
            <div class="text-subtitle-2 font-weight-black">
              فحص اكتمال بيانات ورقة الأسئلة (لمطور بنك الأسئلة ومولد الاختبار)
            </div>
            <div class="text-caption text-medium-emphasis">
              {{ missingFieldsCount === 0 ? 'جميع البيانات الامتحانية مكتملة وحقيقية 100% من قاعدة البيانات' : `يوجد (${missingFieldsCount}) حقول غير محددة في بيانات الاختبار أو كشف الطلاب، وتظهر باللون المميز [غير محدد] لسهولة المتابعة` }}
            </div>
          </div>
        </div>
        <v-chip :color="missingFieldsCount === 0 ? 'success' : 'error'" variant="flat" size="small" class="font-weight-bold">
          {{ 15 - missingFieldsCount }} / 15 مكتمل
        </v-chip>
      </div>

      <!-- Field Status Chips Grid -->
      <div class="d-flex flex-wrap gap-1">
        <v-chip
          v-for="f in examFieldsReadiness"
          :key="f.key"
          size="x-small"
          :color="f.isAvailable ? 'success' : 'error'"
          :variant="f.isAvailable ? 'tonal' : 'flat'"
          class="font-weight-medium font-mono"
        >
          <v-icon start size="12">{{ f.isAvailable ? 'mdi-check' : 'mdi-close' }}</v-icon>
          {{ f.label }}: {{ f.isAvailable ? f.value : `ناقص [${f.key}]` }}
        </v-chip>
      </div>
    </div>

    <!-- ════════════════════════════════════════════════════════════ -->
    <!-- ── MODE 1: A3 SPREAD MODE (SINGLE LARGE SHEET - 2 COLUMNS) ── -->
    <!-- ════════════════════════════════════════════════════════════ -->
    <div v-if="isA3Landscape" class="exam-sheet-frame" :class="col2McqQuestions.length > 0 ? 'columns-two' : 'columns-one'">

      <!-- ── COLUMN 1 (RIGHT): HEADER + TF + MCQ PART 1 ─────────── -->
      <div class="sheet-column column-right">

        <!-- 1. Official Header Box (Rows 1-5 Top Section + Row 6 Bottom Student Bar) -->
        <div class="official-header-box mb-1" :dir="isEnglish ? 'ltr' : 'rtl'">
          <!-- Top Section: Rows 1 to 5 -->
          <table class="table-top-section w-100">
            <colgroup>
              <col style="width: 12.0%;">
              <col style="width: 7.5%;">
              <col style="width: 34.5%;">
              <col style="width: 9.0%;">
              <col style="width: 18.0%;">
              <col style="width: 19.0%;">
            </colgroup>
            <tbody>
              <!-- Row 1: Student Photo (spans 5) + Governorate & Directorate + Republic Emblem (spans 5) -->
              <tr>
                <!-- Far Right: Student Photo Box (spans rows 1 to 5) -->
                <td rowspan="5" class="student-photo-cell">
                  <div class="student-photo-frame">
                    <img v-if="displayStudentPhoto" :src="displayStudentPhoto" alt="صورة الطالب" class="student-photo-img" />
                    <div v-else class="photo-placeholder" style="font-size: 0.55rem; line-height: 1.2;">
                      موضع ختم وتوقيع المركز
                    </div>
                  </div>
                </td>

                <!-- Governorate & Directorate -->
                <td class="font-weight-bold" style="font-size: 0.68rem;">المحافظة</td>
                <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                  {{ displayGovernorate || '................' }}
                </td>
                <td class="font-weight-bold" style="font-size: 0.68rem;">المديرية</td>
                <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                  {{ displayDirectorate || '................' }}
                </td>

                <!-- Far Left: Republic Emblem Logo & Text (spans rows 1 to 5) -->
                <td rowspan="5" class="emblem-cell">
                  <img src="/yemen_eagle_official.png" alt="شعار الجمهورية" class="republic-logo" />
                  <div v-if="isEnglish" class="font-weight-black text-center" style="line-height: 1.15;">
                    <div style="font-size: 0.60rem; font-weight: 800;">Republic of Yemen</div>
                    <div style="font-size: 0.54rem; font-weight: 800;">Ministry of Education</div>
                    <div style="font-size: 0.50rem; font-weight: 800;">Supreme Exam Committee</div>
                    <div style="font-size: 0.56rem; font-weight: 900; margin-top: 1px;">Central Secret Press</div>
                  </div>
                  <div v-else class="font-weight-black text-center" style="line-height: 1.2;">
                    <div style="font-size: 0.78rem; font-weight: 900;">الجمهورية اليمنية</div>
                    <div style="font-size: 0.64rem; font-weight: 800; line-height: 1.15;">وزارة التربية والتعليم</div>
                    <div style="font-size: 0.60rem; font-weight: 800; line-height: 1.15;">اللجنة العليا للإختبارات</div>
                    <div style="font-size: 0.64rem; font-weight: 900; margin-top: 1px;">لجنة المطبعة السرية المركزية</div>
                  </div>
                </td>
              </tr>

              <!-- Row 2: Center & Center Code -->
              <tr>
                <td class="font-weight-bold" style="font-size: 0.68rem;">المركز</td>
                <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                  {{ displayCenterName || '................................................' }}
                </td>
                <td class="font-weight-bold" style="font-size: 0.68rem;">رقمه</td>
                <td class="font-weight-bold font-mono" style="font-size: 0.74rem;">
                  {{ displayCenterCode || '----' }}
                </td>
              </tr>

              <!-- Row 3: Time, Day, Date (Exact match to real ministerial layout) -->
              <tr>
                <td class="font-weight-bold" style="font-size: 0.68rem;">الزمن</td>
                <td class="font-weight-bold time-cell" style="padding: 1px 2px; line-height: 1.2;">
                  <div v-if="displayTimeLine1" style="font-size: 0.58rem; white-space: nowrap;">{{ displayTimeLine1 }}</div>
                  <div v-else style="font-size: 0.58rem; white-space: nowrap;">ساعتان</div>
                  <div v-if="displayTimeLine2" style="font-size: 0.54rem; margin-top: 1px; white-space: nowrap;">{{ displayTimeLine2 }}</div>
                </td>
                <td class="font-weight-bold" style="font-size: 0.68rem;">اليوم</td>
                <td class="font-weight-bold" style="font-size: 0.68rem; white-space: nowrap;">
                  {{ displayDayName || '................' }}
                </td>
              </tr>

              <!-- Row 4: Stage Title & Academic Year (colspan 4) -->
              <tr>
                <td colspan="4" class="font-weight-black stage-year-cell" style="padding: 2px 2px; text-align: center; overflow: hidden; line-height: 1.25;">
                  <div v-if="displayStageLine1" style="font-size: 0.60rem; white-space: nowrap; letter-spacing: -0.2px;">{{ displayStageLine1 }}</div>
                  <div v-else style="font-size: 0.60rem; white-space: nowrap;">اختبار الشهادة العامة</div>
                  <div v-if="displayStageLine2" style="font-size: 0.58rem; margin-top: 1px;">{{ displayStageLine2 }}</div>
                </td>
              </tr>

              <!-- Row 5: Subject & Envelope No -->
              <tr>
                <td class="font-weight-bold" style="font-size: 0.68rem;">اسم المادة</td>
                <td class="font-weight-black" style="font-size: 0.84rem;">
                  {{ (isEnglish ? 'English' : displaySubject) || '................' }}
                </td>
                <td class="font-weight-bold" style="font-size: 0.68rem;">رقم مظروف</td>
                <td class="font-weight-bold font-mono" style="font-size: 0.74rem;">
                  {{ displayEnvelopeNo || '1' }}
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Row 6: Exact Match to Original (Bottom Student Info Bar) -->
          <table class="table-bottom-bar w-100">
            <colgroup>
              <col style="width: 12.0%;">
              <col style="width: 46.5%;">
              <col style="width: 9.5%;">
              <col style="width: 13.0%;">
              <col style="width: 9.5%;">
              <col style="width: 9.5%;">
            </colgroup>
            <tbody>
              <tr>
                <td class="font-weight-black" style="font-size: 0.78rem;">الاسم</td>
                <td class="font-weight-black" style="font-size: 0.82rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                  {{ displayStudentName || '....................................................................' }}
                </td>
                <td class="font-weight-black" style="font-size: 0.70rem;">رقم الجلوس</td>
                <td class="font-weight-black font-mono" style="font-size: 0.85rem;">
                  {{ displaySeatNumber || '........................' }}
                </td>
                <td class="font-weight-black" style="font-size: 0.70rem;">مسلسل</td>
                <td class="font-weight-black font-mono" style="font-size: 0.85rem;">
                  {{ displaySecretNumber || '............' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 2. True / False Section (القسم الأول: صح وخطأ) -->
        <div v-if="tfQuestions.length > 0" class="tf-section-wrapper mb-1" :dir="isEnglish ? 'ltr' : 'rtl'">
          <!-- Instruction Banner -->
          <div class="instruction-banner py-1 font-weight-bold" :class="isEnglish ? 'text-start ps-2' : 'text-right pe-2 ps-2'">
            {{ tfInstructionText }}
          </div>

          <!-- True/False Questions Compact Table -->
          <table class="table-tf w-100" :dir="isEnglish ? 'ltr' : 'rtl'">
            <colgroup>
              <col style="width: 26px;">
              <col style="width: 32px;">
              <col style="width: auto;">
            </colgroup>
            <tbody>
              <tr v-for="q in tfQuestions" :key="`tf-${q.orderIndex}`" class="tf-row">
                <td class="q-index-cell text-center font-weight-black font-mono">{{ q.displayOrder || q.orderIndex }}</td>
                <td class="q-paren-cell text-center"><span class="paren-box">(&nbsp;&nbsp;)</span></td>
                <td class="q-text-cell pe-2 ps-2 py-1 font-weight-bold" :class="isEnglish ? 'text-left' : 'text-right'" v-html="formatQuestionContent(q.content)"></td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Reading Passage Section (if provided) -->
        <div v-if="effectiveReadingPassage" class="reading-passage-box mb-1" :dir="isEnglish ? 'ltr' : 'rtl'">
          <div class="instruction-banner py-1 font-weight-bold" :class="isEnglish ? 'text-start ps-2' : 'text-center'">
            {{ readingPassageHeader }}
          </div>
          <div class="passage-text-content p-2 bg-white" style="border: 1px solid #000; font-size: 0.74rem; line-height: 1.35;">
            {{ effectiveReadingPassage }}
          </div>
        </div>

        <!-- 3. MCQ Section Part 1 (القسم الثاني: اختيار من متعدد - بداية الأسئلة) -->
        <div v-if="col1McqQuestions.length > 0" class="mcq-section-wrapper" :dir="isEnglish ? 'ltr' : 'rtl'">
          <!-- Instruction Banner -->
          <div class="instruction-banner py-1 font-weight-bold" :class="isEnglish ? 'text-start ps-2' : 'text-right pe-2 ps-2'">
            {{ mcqInstructionText }}
          </div>

          <!-- Continuous MCQ Table for Column 1 -->
          <table class="table-mcq-continuous w-100" :dir="isEnglish ? 'ltr' : 'rtl'">
            <colgroup>
              <col style="width: 26px;">
              <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
              <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
              <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
              <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
            </colgroup>
            <tbody>
              <template v-for="q in col1McqQuestions" :key="`mcq-${q.orderIndex}`">
                <tr class="q-stem-row">
                  <td
                    :rowspan="getOptionsLayout(q) === 'two-rows' ? 3 : 2"
                    class="q-num-cell text-center font-weight-black font-mono"
                  >
                    {{ q.displayOrder || q.orderIndex }}
                  </td>
                  <td colspan="8" class="q-stem-cell pe-2 ps-2 py-1 font-weight-bold" :class="isEnglish ? 'text-left' : 'text-right'">
                    <div v-if="q.image || q.figure" class="d-flex align-center justify-space-between w-100">
                      <span v-html="formatQuestionContent(q.content)"></span>
                      <img :src="q.image || q.figure" alt="رسم توضيحي للسؤال" class="q-diagram-img ms-2" />
                    </div>
                    <span v-else v-html="formatQuestionContent(q.content)"></span>
                  </td>
                </tr>

                <!-- Short options: single-row layout -->
                <tr v-if="getOptionsLayout(q) === 'single-row'" class="q-options-row text-center">
                  <td class="opt-num-cell font-mono font-weight-black">1</td>
                  <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                    <span :dir="isLtrText(getOptionText(q, 0)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 0))"></span>
                  </td>
                  <td class="opt-num-cell font-mono font-weight-black">2</td>
                  <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                    <span :dir="isLtrText(getOptionText(q, 1)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 1))"></span>
                  </td>
                  <td class="opt-num-cell font-mono font-weight-black">3</td>
                  <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                    <span :dir="isLtrText(getOptionText(q, 2)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 2))"></span>
                  </td>
                  <td class="opt-num-cell font-mono font-weight-black">4</td>
                  <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                    <span :dir="isLtrText(getOptionText(q, 3)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 3))"></span>
                  </td>
                </tr>

                <!-- Long options: two-rows layout (2 options per row with colspan 3) -->
                <template v-else>
                  <tr class="q-options-row">
                    <td class="opt-num-cell font-mono font-weight-black">1</td>
                    <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                      <span :dir="isLtrText(getOptionText(q, 0)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 0))"></span>
                    </td>
                    <td class="opt-num-cell font-mono font-weight-black">2</td>
                    <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                      <span :dir="isLtrText(getOptionText(q, 1)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 1))"></span>
                    </td>
                  </tr>
                  <tr class="q-options-row">
                    <td class="opt-num-cell font-mono font-weight-black">3</td>
                    <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                      <span :dir="isLtrText(getOptionText(q, 2)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 2))"></span>
                    </td>
                    <td class="opt-num-cell font-mono font-weight-black">4</td>
                    <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                      <span :dir="isLtrText(getOptionText(q, 3)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 3))"></span>
                    </td>
                  </tr>
                </template>
              </template>
            </tbody>
          </table>
        </div>

        <!-- Bottom Footer Banner if only 1 column has questions -->
        <div v-if="col2McqQuestions.length === 0" class="exam-paper-end-banner text-center font-weight-black">
          {{ endBannerText }}
        </div>
      </div>

      <!-- ── COLUMN 2 (LEFT): MCQ CONTINUATION (Q30 to Q50) ───────── -->
      <div v-if="col2McqQuestions.length > 0" class="sheet-column column-left">

        <!-- Continuous MCQ Table for Column 2 -->
        <table class="table-mcq-continuous w-100" :dir="isEnglish ? 'ltr' : 'rtl'">
          <colgroup>
            <col style="width: 26px;">
            <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
            <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
            <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
            <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
          </colgroup>
          <tbody>
            <template v-for="q in col2McqQuestions" :key="`mcq-${q.orderIndex}`">
              <tr class="q-stem-row">
                <td
                  :rowspan="getOptionsLayout(q) === 'two-rows' ? 3 : 2"
                  class="q-num-cell text-center font-weight-black font-mono"
                >
                  {{ q.displayOrder || q.orderIndex }}
                </td>
                <td colspan="8" class="q-stem-cell pe-2 ps-2 py-1 font-weight-bold" :class="isEnglish ? 'text-left' : 'text-right'">
                  <div v-if="q.image || q.figure" class="d-flex align-center justify-space-between w-100">
                    <span v-html="formatQuestionContent(q.content)"></span>
                    <img :src="q.image || q.figure" alt="رسم توضيحي للسؤال" class="q-diagram-img ms-2" />
                  </div>
                  <span v-else v-html="formatQuestionContent(q.content)"></span>
                </td>
              </tr>

              <!-- Short options: single-row layout -->
              <tr v-if="getOptionsLayout(q) === 'single-row'" class="q-options-row text-center">
                <td class="opt-num-cell font-mono font-weight-black">1</td>
                <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                  <span :dir="isLtrText(getOptionText(q, 0)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 0))"></span>
                </td>
                <td class="opt-num-cell font-mono font-weight-black">2</td>
                <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                  <span :dir="isLtrText(getOptionText(q, 1)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 1))"></span>
                </td>
                <td class="opt-num-cell font-mono font-weight-black">3</td>
                <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                  <span :dir="isLtrText(getOptionText(q, 2)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 2))"></span>
                </td>
                <td class="opt-num-cell font-mono font-weight-black">4</td>
                <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                  <span :dir="isLtrText(getOptionText(q, 3)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 3))"></span>
                </td>
              </tr>

              <!-- Long options: two-rows layout (2 options per row with colspan 3) -->
              <template v-else>
                <tr class="q-options-row">
                  <td class="opt-num-cell font-mono font-weight-black">1</td>
                  <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                    <span :dir="isLtrText(getOptionText(q, 0)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 0))"></span>
                  </td>
                  <td class="opt-num-cell font-mono font-weight-black">2</td>
                  <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                    <span :dir="isLtrText(getOptionText(q, 1)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 1))"></span>
                  </td>
                </tr>
                <tr class="q-options-row">
                  <td class="opt-num-cell font-mono font-weight-black">3</td>
                  <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                    <span :dir="isLtrText(getOptionText(q, 2)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 2))"></span>
                  </td>
                  <td class="opt-num-cell font-mono font-weight-black">4</td>
                  <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                    <span :dir="isLtrText(getOptionText(q, 3)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 3))"></span>
                  </td>
                </tr>
              </template>
            </template>
          </tbody>
        </table>

        <!-- Bottom Footer Banner -->
        <div class="exam-paper-end-banner text-center font-weight-black">
          {{ endBannerText }}
        </div>

      </div>

    </div>

    <!-- ════════════════════════════════════════════════════════════ -->
    <!-- ── MODE 2: A4 PORTRAIT MODE (TWO DISTINCT CONSECUTIVE PAGES)  -->
    <!-- ════════════════════════════════════════════════════════════ -->
    <div v-else class="a4-pages-wrapper">

      <!-- ── PAGE 1 (A4): HEADER + TF + PART 1 MCQs ─────────────── -->
      <div class="a4-sheet-page sheet-page-1">
        <div class="page-content-wrapper">
          <!-- 1. Official Header Box (Rows 1-5 Top Section + Row 6 Bottom Student Bar) -->
          <div class="official-header-box mb-1" :dir="isEnglish ? 'ltr' : 'rtl'">
            <!-- Top Section: Rows 1 to 5 -->
            <table class="table-top-section w-100">
              <colgroup>
                <col style="width: 12.0%;">
                <col style="width: 7.5%;">
                <col style="width: 34.5%;">
                <col style="width: 9.0%;">
                <col style="width: 18.0%;">
                <col style="width: 19.0%;">
              </colgroup>
              <tbody>
                <!-- Row 1: Student Photo (spans 5) + Governorate & Directorate + Republic Emblem (spans 5) -->
                <tr>
                  <!-- Far Right: Student Photo Box (spans rows 1 to 5) -->
                  <td rowspan="5" class="student-photo-cell">
                    <div class="student-photo-frame">
                      <img v-if="displayStudentPhoto" :src="displayStudentPhoto" alt="صورة الطالب" class="student-photo-img" />
                      <div v-else class="photo-placeholder" style="font-size: 0.55rem; line-height: 1.2;">
                        موضع ختم وتوقيع المركز
                      </div>
                    </div>
                  </td>

                  <!-- Governorate & Directorate -->
                  <td class="font-weight-bold" style="font-size: 0.68rem;">المحافظة</td>
                  <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                    {{ displayGovernorate || '................' }}
                  </td>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">المديرية</td>
                  <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                    {{ displayDirectorate || '................' }}
                  </td>

                  <!-- Far Left: Republic Emblem Logo & Text (spans rows 1 to 5) -->
                  <td rowspan="5" class="emblem-cell">
                    <img src="/yemen_eagle_official.png" alt="شعار الجمهورية" class="republic-logo" />
                    <div v-if="isEnglish" class="font-weight-black text-center" style="line-height: 1.15;">
                      <div style="font-size: 0.60rem; font-weight: 800;">Republic of Yemen</div>
                      <div style="font-size: 0.54rem; font-weight: 800;">Ministry of Education</div>
                      <div style="font-size: 0.50rem; font-weight: 800;">Supreme Exam Committee</div>
                      <div style="font-size: 0.56rem; font-weight: 900; margin-top: 1px;">Central Secret Press</div>
                    </div>
                    <div v-else class="font-weight-black text-center" style="line-height: 1.2;">
                      <div style="font-size: 0.78rem; font-weight: 900;">الجمهورية اليمنية</div>
                      <div style="font-size: 0.64rem; font-weight: 800; line-height: 1.15;">وزارة التربية والتعليم</div>
                      <div style="font-size: 0.60rem; font-weight: 800; line-height: 1.15;">اللجنة العليا للإختبارات</div>
                      <div style="font-size: 0.64rem; font-weight: 900; margin-top: 1px;">لجنة المطبعة السرية المركزية</div>
                    </div>
                  </td>
                </tr>

                <!-- Row 2: Center & Center Code -->
                <tr>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">المركز</td>
                  <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                    {{ displayCenterName || '................................................' }}
                  </td>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">رقمه</td>
                  <td class="font-weight-bold font-mono" style="font-size: 0.74rem;">
                    {{ displayCenterCode || '----' }}
                  </td>
                </tr>

                <!-- Row 3: Time, Day, Date (Exact match to real ministerial layout) -->
                <tr>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">الزمن</td>
                  <td class="font-weight-bold time-cell" style="padding: 1px 2px; line-height: 1.2;">
                    <div v-if="displayTimeLine1" style="font-size: 0.58rem; white-space: nowrap;">{{ displayTimeLine1 }}</div>
                    <div v-else style="font-size: 0.58rem; white-space: nowrap;">ساعتان</div>
                    <div v-if="displayTimeLine2" style="font-size: 0.54rem; margin-top: 1px; white-space: nowrap;">{{ displayTimeLine2 }}</div>
                  </td>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">اليوم</td>
                  <td class="font-weight-bold" style="font-size: 0.68rem; white-space: nowrap;">
                    {{ displayDayName || '................' }}
                  </td>
                </tr>

                <!-- Row 4: Stage Title & Academic Year (colspan 4) -->
                <tr>
                  <td colspan="4" class="font-weight-black stage-year-cell" style="padding: 2px 2px; text-align: center; overflow: hidden; line-height: 1.25;">
                    <div v-if="displayStageLine1" style="font-size: 0.60rem; white-space: nowrap; letter-spacing: -0.2px;">{{ displayStageLine1 }}</div>
                    <div v-else style="font-size: 0.60rem; white-space: nowrap;">اختبار الشهادة العامة</div>
                    <div v-if="displayStageLine2" style="font-size: 0.58rem; margin-top: 1px;">{{ displayStageLine2 }}</div>
                  </td>
                </tr>

                <!-- Row 5: Subject & Envelope No -->
                <tr>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">اسم المادة</td>
                  <td class="font-weight-black" style="font-size: 0.84rem;">
                    {{ (isEnglish ? 'English' : displaySubject) || '................' }}
                  </td>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">رقم مظروف</td>
                  <td class="font-weight-bold font-mono" style="font-size: 0.74rem;">
                    {{ displayEnvelopeNo || '1' }}
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Row 6: Exact Match to Original (Bottom Student Info Bar) -->
            <table class="table-bottom-bar w-100">
              <colgroup>
                <col style="width: 12.0%;">
                <col style="width: 46.5%;">
                <col style="width: 9.5%;">
                <col style="width: 13.0%;">
                <col style="width: 9.5%;">
                <col style="width: 9.5%;">
              </colgroup>
              <tbody>
                <tr>
                  <td class="font-weight-black" style="font-size: 0.78rem;">الاسم</td>
                  <td class="font-weight-black" style="font-size: 0.82rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {{ displayStudentName || '....................................................................' }}
                  </td>
                  <td class="font-weight-black" style="font-size: 0.70rem;">رقم الجلوس</td>
                  <td class="font-weight-black font-mono" style="font-size: 0.85rem;">
                    {{ displaySeatNumber || '........................' }}
                  </td>
                  <td class="font-weight-black" style="font-size: 0.70rem;">مسلسل</td>
                  <td class="font-weight-black font-mono" style="font-size: 0.85rem;">
                    {{ displaySecretNumber || '............' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 2. True / False Section -->
          <div v-if="tfQuestions.length > 0" class="tf-section-wrapper mb-1" :dir="isEnglish ? 'ltr' : 'rtl'">
            <div class="instruction-banner py-1 font-weight-bold" :class="isEnglish ? 'text-start ps-2' : 'text-right pe-2 ps-2'">
              {{ tfInstructionText }}
            </div>
            <table class="table-tf w-100" :dir="isEnglish ? 'ltr' : 'rtl'">
              <colgroup>
                <col style="width: 26px;">
                <col style="width: 32px;">
                <col style="width: auto;">
              </colgroup>
              <tbody>
                <tr v-for="q in tfQuestions" :key="`a4-tf-${q.orderIndex}`" class="tf-row">
                  <td class="q-index-cell text-center font-weight-black font-mono">{{ q.displayOrder || q.orderIndex }}</td>
                  <td class="q-paren-cell text-center"><span class="paren-box">(&nbsp;&nbsp;)</span></td>
                  <td class="q-text-cell pe-2 ps-2 py-1 font-weight-bold" :class="isEnglish ? 'text-left' : 'text-right'" v-html="formatQuestionContent(q.content)"></td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Reading Passage Section (if provided) -->
          <div v-if="effectiveReadingPassage" class="reading-passage-box mb-1" :dir="isEnglish ? 'ltr' : 'rtl'">
            <div class="instruction-banner py-1 font-weight-bold" :class="isEnglish ? 'text-start ps-2' : 'text-center'">
              {{ readingPassageHeader }}
            </div>
            <div class="passage-text-content p-2 bg-white" style="border: 1px solid #000; font-size: 0.74rem; line-height: 1.35;">
              {{ effectiveReadingPassage }}
            </div>
          </div>

          <!-- 3. MCQ Part 1 -->
          <div v-if="col1McqQuestions.length > 0" class="mcq-section-wrapper" :dir="isEnglish ? 'ltr' : 'rtl'">
            <div class="instruction-banner py-1 font-weight-bold" :class="isEnglish ? 'text-start ps-2' : 'text-right pe-2 ps-2'">
              {{ mcqInstructionText }}
            </div>
            <table class="table-mcq-continuous w-100" :dir="isEnglish ? 'ltr' : 'rtl'">
              <colgroup>
                <col style="width: 26px;">
                <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
                <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
                <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
                <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
              </colgroup>
              <tbody>
                <template v-for="q in col1McqQuestions" :key="`a4-mcq-${q.orderIndex}`">
                  <tr class="q-stem-row">
                    <td
                      :rowspan="getOptionsLayout(q) === 'two-rows' ? 3 : 2"
                      class="q-num-cell text-center font-weight-black font-mono"
                    >
                      {{ q.displayOrder || q.orderIndex }}
                    </td>
                    <td colspan="8" class="q-stem-cell pe-2 ps-2 py-1 font-weight-bold" :class="isEnglish ? 'text-left' : 'text-right'">
                      <div v-if="q.image || q.figure" class="d-flex align-center justify-space-between w-100">
                        <span v-html="formatQuestionContent(q.content)"></span>
                        <img :src="q.image || q.figure" alt="رسم توضيحي للسؤال" class="q-diagram-img ms-2" />
                      </div>
                      <span v-else v-html="formatQuestionContent(q.content)"></span>
                    </td>
                  </tr>

                  <!-- Short options: single-row layout -->
                  <tr v-if="getOptionsLayout(q) === 'single-row'" class="q-options-row text-center">
                    <td class="opt-num-cell font-mono font-weight-black">1</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                      <span :dir="isLtrText(getOptionText(q, 0)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 0))"></span>
                    </td>
                    <td class="opt-num-cell font-mono font-weight-black">2</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                      <span :dir="isLtrText(getOptionText(q, 1)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 1))"></span>
                    </td>
                    <td class="opt-num-cell font-mono font-weight-black">3</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                      <span :dir="isLtrText(getOptionText(q, 2)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 2))"></span>
                    </td>
                    <td class="opt-num-cell font-mono font-weight-black">4</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                      <span :dir="isLtrText(getOptionText(q, 3)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 3))"></span>
                    </td>
                  </tr>

                  <!-- Long options: two-rows layout (2 options per row with colspan 3) -->
                  <template v-else>
                    <tr class="q-options-row">
                      <td class="opt-num-cell font-mono font-weight-black">1</td>
                      <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                        <span :dir="isLtrText(getOptionText(q, 0)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 0))"></span>
                      </td>
                      <td class="opt-num-cell font-mono font-weight-black">2</td>
                      <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                        <span :dir="isLtrText(getOptionText(q, 1)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 1))"></span>
                      </td>
                    </tr>
                    <tr class="q-options-row">
                      <td class="opt-num-cell font-mono font-weight-black">3</td>
                      <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                        <span :dir="isLtrText(getOptionText(q, 2)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 2))"></span>
                      </td>
                      <td class="opt-num-cell font-mono font-weight-black">4</td>
                      <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                        <span :dir="isLtrText(getOptionText(q, 3)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 3))"></span>
                      </td>
                    </tr>
                  </template>
                </template>
              </tbody>
            </table>
          </div>

          <!-- Bottom Footer Banner on Page 1 if only 1 page -->
          <div v-if="!hasSecondPage" class="exam-paper-end-banner text-center font-weight-black">
            {{ endBannerText }}
          </div>
        </div>

        <!-- Page 1 Footer -->
        <div class="a4-page-footer d-print-none d-flex justify-space-between align-center font-weight-bold pt-2 mt-2 border-t">
          <span>{{ isEnglish ? 'English' : examSubject }} • {{ isEnglish ? 'Form' : 'النموذج' }} ({{ modelCode || '1' }})</span>
          <span>{{ isEnglish ? (hasSecondPage ? 'Page 1 of 2 (Turn over)' : 'Page 1 of 1') : (hasSecondPage ? 'الصفحة 1 من 2 (يتبع في الصفحة التالية)' : 'الصفحة 1 من 1') }}</span>
        </div>
      </div>

      <!-- ── PAGE 2 (A4): PART 2 MCQs (Q30 to Q50) + END BANNER ─── -->
      <div v-if="hasSecondPage" class="a4-sheet-page sheet-page-2 mt-4">
        <div class="page-content-wrapper">
          <!-- MCQs Part 2 (Starts directly at Q30 like authentic ministerial layout) -->
          <div class="mcq-section-wrapper" :dir="isEnglish ? 'ltr' : 'rtl'">
            <table class="table-mcq-continuous w-100" :dir="isEnglish ? 'ltr' : 'rtl'">
              <colgroup>
                <col style="width: 26px;">
                <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
                <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
                <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
                <col style="width: 20px;"><col style="width: calc(25% - 26.5px);">
              </colgroup>
              <tbody>
                <template v-for="q in col2McqQuestions" :key="`a4-mcq2-${q.orderIndex}`">
                  <tr class="q-stem-row">
                    <td
                      :rowspan="getOptionsLayout(q) === 'two-rows' ? 3 : 2"
                      class="q-num-cell text-center font-weight-black font-mono"
                    >
                      {{ q.displayOrder || q.orderIndex }}
                    </td>
                    <td colspan="8" class="q-stem-cell pe-2 ps-2 py-1 font-weight-bold" :class="isEnglish ? 'text-left' : 'text-right'">
                      <div v-if="q.image || q.figure" class="d-flex align-center justify-space-between w-100">
                        <span v-html="formatQuestionContent(q.content)"></span>
                        <img :src="q.image || q.figure" alt="رسم توضيحي للسؤال" class="q-diagram-img ms-2" />
                      </div>
                      <span v-else v-html="formatQuestionContent(q.content)"></span>
                    </td>
                  </tr>

                  <!-- Short options: single-row layout -->
                  <tr v-if="getOptionsLayout(q) === 'single-row'" class="q-options-row text-center">
                    <td class="opt-num-cell font-mono font-weight-black">1</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                      <span :dir="isLtrText(getOptionText(q, 0)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 0))"></span>
                    </td>
                    <td class="opt-num-cell font-mono font-weight-black">2</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                      <span :dir="isLtrText(getOptionText(q, 1)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 1))"></span>
                    </td>
                    <td class="opt-num-cell font-mono font-weight-black">3</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                      <span :dir="isLtrText(getOptionText(q, 2)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 2))"></span>
                    </td>
                    <td class="opt-num-cell font-mono font-weight-black">4</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'">
                      <span :dir="isLtrText(getOptionText(q, 3)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 3))"></span>
                    </td>
                  </tr>

                  <!-- Long options: two-rows layout (2 options per row with colspan 3) -->
                  <template v-else>
                    <tr class="q-options-row">
                      <td class="opt-num-cell font-mono font-weight-black">1</td>
                      <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                        <span :dir="isLtrText(getOptionText(q, 0)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 0))"></span>
                      </td>
                      <td class="opt-num-cell font-mono font-weight-black">2</td>
                      <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                        <span :dir="isLtrText(getOptionText(q, 1)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 1))"></span>
                      </td>
                    </tr>
                    <tr class="q-options-row">
                      <td class="opt-num-cell font-mono font-weight-black">3</td>
                      <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                        <span :dir="isLtrText(getOptionText(q, 2)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 2))"></span>
                      </td>
                      <td class="opt-num-cell font-mono font-weight-black">4</td>
                      <td colspan="3" class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-left ps-2' : 'text-right pe-2 ps-1'">
                        <span :dir="isLtrText(getOptionText(q, 3)) ? 'ltr' : 'auto'" class="opt-text-inner" v-html="formatOptionContent(getOptionText(q, 3))"></span>
                      </td>
                    </tr>
                  </template>
                </template>
              </tbody>
            </table>
          </div>

          <!-- Bottom Footer Banner -->
          <div class="exam-paper-end-banner text-center font-weight-black">
            {{ endBannerText }}
          </div>
        </div>

        <!-- Page 2 Footer -->
        <div class="a4-page-footer d-print-none d-flex justify-space-between align-center font-weight-bold pt-2 mt-2 border-t">
          <span>{{ isEnglish ? 'English' : examSubject }} • {{ isEnglish ? 'Form' : 'النموذج' }} ({{ modelCode || '1' }})</span>
          <span>{{ isEnglish ? 'Page 2 of 2' : 'الصفحة 2 من 2' }}</span>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { printOfficialQuestionPaper } from '@/pages/OMRSystem/utils/omrPrint'

const paperRootRef = ref<HTMLElement | null>(null)

const props = withDefaults(
  defineProps<{
    examTitle?: string
    examSubject?: string
    stageTitle?: string
    examYear?: string
    governorate?: string
    directorate?: string
    centerName?: string
    centerCode?: string | number
    examTime?: string
    dayName?: string
    examDate?: string
    envelopeNo?: string | number
    studentName?: string
    seatNumber?: string | number
    secretNumber?: string | number
    modelCode?: string | number
    studentPhoto?: string
    tfMark?: number
    mcqMark?: number
    totalScore?: number
    readingPassage?: string
    isBlankMode?: boolean
    showDiagnostics?: boolean
    hideToolbar?: boolean
    questions?: Array<{
      id?: string | number
      orderIndex: number
      content: string
      questionType?: string
      assignedMark?: number
      image?: string
      figure?: string
      options?: Array<{
        id?: string | number
        letter?: string
        arabic_letter?: string
        text: string
        isTrue?: boolean
      }>
    }>
    defaultLayout?: 'a3' | 'a4' | 'auto'
  }>(),
  {
    examTitle: '',
    examSubject: '',
    stageTitle: '',
    examYear: '',
    governorate: '',
    directorate: '',
    centerName: '',
    centerCode: '',
    examTime: '',
    dayName: '',
    examDate: '',
    envelopeNo: '',
    studentName: '',
    seatNumber: '',
    secretNumber: '',
    modelCode: '1',
    studentPhoto: '',
    tfMark: 1,
    mcqMark: 2,
    totalScore: 80,
    readingPassage: '',
    isBlankMode: false,
    showDiagnostics: false,
    hideToolbar: false,
    questions: () => [],
    defaultLayout: 'auto',
  }
)

const paperSizeSetting = ref<'a3' | 'a4'>('a4')

watch(
  () => [props.defaultLayout, (props.questions || []).length],
  () => {
    if (props.defaultLayout === 'a3') {
      paperSizeSetting.value = 'a3'
    } else {
      paperSizeSetting.value = 'a4'
    }
  },
  { immediate: true }
)
const isA3Landscape = computed(() => paperSizeSetting.value === 'a3')

// Detect if exam is English based on subject or question contents
const isEnglish = computed(() => {
  const subj = (props.examSubject || '').trim().toLowerCase()
  if (subj.includes('english') || subj.includes('انجليز') || subj.includes('إنجليز')) {
    return true
  }
  const qs = props.questions || []
  if (qs.length > 0) {
    let latinCount = 0
    let arabicCount = 0
    for (const q of qs) {
      const text = (q.content || '') + ' ' + (q.options || []).map((o: any) => (typeof o === 'object' ? (o?.text || '') : String(o || ''))).join(' ')
      latinCount += (text.match(/[a-zA-Z]/g) || []).length
      arabicCount += (text.match(/[\u0600-\u06FF]/g) || []).length
    }
    // Only genuine English exam if Latin letters dominate and Arabic is virtually absent
    if (latinCount > 50 && arabicCount < 15) {
      return true
    }
  }
  return false
})

// ── Pure Authentic Data Getters (Without fake mock text) ──
const displayGovernorate = computed(() => props.governorate?.trim() || '')
const displayDirectorate = computed(() => props.directorate?.trim() || '')
const displayCenterName = computed(() => props.centerName?.trim() || '')
const displayCenterCode = computed(() => (props.centerCode !== undefined && props.centerCode !== null && String(props.centerCode).trim() !== '') ? String(props.centerCode).trim() : '')
const displaySubject = computed(() => props.examSubject?.trim() || '')
const displayEnvelopeNo = computed(() => (props.envelopeNo !== undefined && props.envelopeNo !== null && String(props.envelopeNo).trim() !== '') ? String(props.envelopeNo).trim() : '')
const displayDayName = computed(() => props.dayName?.trim() || '')

const displayTimeLine1 = computed(() => {
  if (props.examTime?.trim()) {
    const t = props.examTime.trim()
    if (t.includes('وحتى')) {
      return t.split('وحتى')[0].trim() + (isEnglish.value ? ' to' : ' وحتى')
    }
    return t
  }
  return ''
})

const displayTimeLine2 = computed(() => {
  const t = props.examTime?.trim() || ''
  const d = props.examDate?.trim() || ''
  if (t.includes('وحتى')) {
    const afterUntil = t.split('وحتى')[1].trim()
    return d ? `${afterUntil} - ${d}` : afterUntil
  }
  return d
})

const displayStageLine1 = computed(() => {
  const st = props.stageTitle?.trim() || props.examTitle?.trim() || ''
  const yr = props.examYear?.trim() || ''
  if (!st && !yr) return ''
  if (!st) return yr ? `للعام الدراسي ${yr}` : ''
  if (st.includes('للعام') || st.includes('144') || st.includes('202')) return st
  const hijriMatch = yr.match(/(\d{4}\s*هـ?)/)
  const hijriStr = hijriMatch ? hijriMatch[1].replace('ه', '') + 'هـ' : ''
  if (hijriStr) {
    return isEnglish.value ? `${st} Academic Year ${hijriStr}` : `${st} للعام الدراسي ${hijriStr}`
  }
  return st
})

const displayStageLine2 = computed(() => {
  const yr = props.examYear?.trim() || ''
  if (!yr) return ''
  const gregMatch = yr.match(/(\d{4}\s*[-/]\s*\d{4}\s*م?)/)
  if (gregMatch) {
    let g = gregMatch[1].trim()
    if (!g.endsWith('م')) g += 'م'
    if (!g.startsWith('-')) g = '-' + g
    return g
  }
  if (yr.includes('م') || yr.includes('-')) return yr
  return ''
})

const isBlankMode = computed(() => props.isBlankMode || props.studentName === '__BLANK__' || !props.studentName)

const displayStudentName = computed(() => {
  if (isBlankMode.value) return '........................................................'
  return props.studentName?.trim() || '........................................................'
})

const displaySeatNumber = computed(() => {
  if (isBlankMode.value) return '..........'
  return (props.seatNumber !== undefined && props.seatNumber !== null && String(props.seatNumber).trim() !== '') ? String(props.seatNumber).trim() : '..........'
})

const displaySecretNumber = computed(() => {
  if (isBlankMode.value) return '.....'
  return (props.secretNumber !== undefined && props.secretNumber !== null && String(props.secretNumber).trim() !== '') ? String(props.secretNumber).trim() : '.....'
})

const displayStudentPhoto = computed(() => props.studentPhoto?.trim() || '')

// Developer Diagnostics & Readiness Checklist
const examFieldsReadiness = computed(() => [
  { key: 'subject_name', label: 'المادة', value: displaySubject.value, isAvailable: !!displaySubject.value },
  { key: 'stage_name', label: 'المرحلة والصف', value: displayStageLine1.value, isAvailable: !!displayStageLine1.value },
  { key: 'year_name', label: 'العام الدراسي', value: props.examYear?.trim() || '', isAvailable: !!(props.examYear?.trim()) },
  { key: 'governorate', label: 'المحافظة', value: displayGovernorate.value, isAvailable: !!displayGovernorate.value },
  { key: 'directorate', label: 'المديرية', value: displayDirectorate.value, isAvailable: !!displayDirectorate.value },
  { key: 'center_name', label: 'المركز الاختباري', value: displayCenterName.value, isAvailable: !!displayCenterName.value },
  { key: 'center_code', label: 'رقم المركز', value: displayCenterCode.value, isAvailable: !!displayCenterCode.value },
  { key: 'time_allowed', label: 'الزمن', value: displayTimeLine1.value, isAvailable: !!displayTimeLine1.value },
  { key: 'day_name', label: 'اليوم', value: displayDayName.value, isAvailable: !!displayDayName.value },
  { key: 'exam_date', label: 'التاريخ', value: displayTimeLine2.value, isAvailable: !!displayTimeLine2.value },
  { key: 'envelope_no', label: 'رقم المظروف', value: displayEnvelopeNo.value, isAvailable: !!displayEnvelopeNo.value },
  { key: 'student_name', label: 'اسم الطالب', value: isBlankMode.value ? 'نموذج خام' : displayStudentName.value, isAvailable: isBlankMode.value || !!displayStudentName.value },
  { key: 'seat_number', label: 'رقم الجلوس', value: isBlankMode.value ? 'نموذج خام' : displaySeatNumber.value, isAvailable: isBlankMode.value || !!displaySeatNumber.value },
  { key: 'secret_number', label: 'الرقم السري', value: isBlankMode.value ? 'نموذج خام' : displaySecretNumber.value, isAvailable: isBlankMode.value || !!displaySecretNumber.value },
  { key: 'student_photo', label: 'الصورة الشخصية', value: displayStudentPhoto.value ? 'متوفرة' : (isBlankMode.value ? 'ختم المركز' : ''), isAvailable: isBlankMode.value || !!displayStudentPhoto.value },
])

const missingFieldsCount = computed(() => examFieldsReadiness.value.filter(f => !f.isAvailable).length)

const tfInstructionText = computed(() => {
  if (isEnglish.value) {
    return `Read the following questions, and on the answer sheet, darken the number that matches the correct alternative.\nPart One: Mark (T/True) for the true statements and (F/False) for the false ones.    (${props.tfMark || 1}) point each`
  }
  const markText = props.tfMark && props.tfMark !== 1 ? `${props.tfMark} درجات لكل فقرة.` : 'درجة لكل فقرة.'
  return `ظلل في ورقة الإجابة الدائرة التي تحتوي على الحرف (ص) للإجابة الصحيحة والحرف (خ) للإجابة الخطأ بحسب رقم الفقرة لكل مما يأتي: ${markText}`
})

const mcqInstructionText = computed(() => {
  if (isEnglish.value) {
    return `Part two: Choose the best alternative:    (${props.mcqMark || 2}) points each`
  }
  const markText = props.mcqMark && props.mcqMark !== 2 ? `${props.mcqMark} درجات لكل فقرة.` : 'درجتان لكل فقرة.'
  return `اختر الإجابة الصحيحة ثم ظلل في ورقة الإجابة الدائرة بحسب الإختيار ورقم الفقرة لكل مما يأتي:${markText}`
})

const readingPassageHeader = computed(() => {
  if (isEnglish.value) {
    return `Part two: A) Read the following passage then choose the best answer to the questions below:    (${props.mcqMark || 2}) points each`
  }
  return `اقرأ النص التالي بعناية ثم أجب عن الأسئلة الآتية: (${props.mcqMark || 2}) درجات لكل فقرة`
})

// Ministerial reading comprehension passage (from authentic Yemeni official examination)
const effectiveReadingPassage = computed(() => {
  if (props.readingPassage) return props.readingPassage
  if (isEnglish.value && (props.questions || []).length >= 30) {
    return `I have big plans for my future. I am going to study nursing after I learn more English. I am going to finish an English program here in Scotland before I transfer to university. At the university, I plan to get a bachelor degree in nursing. After I become a nurse, I am going to work at a hospital. I hope that I will find a good job. I am also planning to get married someday. I hope that I will meet a kind and (intelligent) man. I would like to have four children, two boys and two girls. I am looking forward to my career, but my family will be the most important part of my future.`
  }
  return ''
})

const secretPressRibbonText = computed(() => {
  if (isEnglish.value) {
    return {
      press: 'Ministry of Education • Central Secret Printing Press Committee',
      continuation: `Multiple Choice Questions (Continued) • Form (${props.modelCode || '1'})`,
    }
  }
  return {
    press: 'لجنة المطبعة السرية المركزية • وزارة التربية والتعليم',
    continuation: `تابع أسئلة الاختيار من متعدد • النموذج (${props.modelCode || '1'})`,
  }
})

const endBannerText = computed(() => {
  if (isEnglish.value) {
    return `*** End of Form (${props.modelCode || '1'}) Questions — Best wishes for success ***`
  }
  return `*** انتهت أسئلة النموذج (${props.modelCode || '1'}) — مع تمنياتنا لجميع الطلاب بالتوفيق والنجاح ***`
})

// Filter True/False vs MCQ Questions with strict sequential numbering
const tfQuestions = computed(() => {
  const filtered = (props.questions || []).filter((q) => {
    const typeStr = String(q.questionType || '').toLowerCase()
    return typeStr.includes('true') || typeStr.includes('false') || typeStr.includes('صح') || typeStr.includes('خطأ')
  })
  return filtered.map((q, idx) => ({
    ...q,
    displayOrder: idx + 1,
  }))
})

const mcqQuestions = computed(() => {
  const filtered = (props.questions || []).filter((q) => {
    const typeStr = String(q.questionType || '').toLowerCase()
    return !(typeStr.includes('true') || typeStr.includes('false') || typeStr.includes('صح') || typeStr.includes('خطأ'))
  })
  const tfCount = tfQuestions.value.length
  return filtered.map((q, idx) => ({
    ...q,
    displayOrder: tfCount + idx + 1,
  }))
})

// Dynamic multi-page decision:
// Short exams (<= 18 questions without passage) fit cleanly on 1 page!
// Longer exams (standard 20+ to 50 questions) split neatly into 2 pages.
const hasSecondPage = computed(() => {
  const total = (props.questions || []).length
  if (total <= 18 && !props.readingPassage) {
    return false
  }
  return true
})

// Split MCQ questions dynamically between Column 1 (or Page 1) and Column 2 (or Page 2)
const splitIndex = computed(() => {
  const mcq = mcqQuestions.value
  if (mcq.length === 0) return 0

  // If exam fits on 1 single page (<= 18 questions), do NOT split at all!
  if (!hasSecondPage.value) {
    return mcq.length
  }

  // If exam has True/False section (typically 15-20 questions)
  if (tfQuestions.value.length >= 12) {
    const col1Capacity = effectiveReadingPassage.value ? 6 : 9
    return Math.min(mcq.length, col1Capacity)
  }

  // If exam has no True/False (pure MCQ, e.g. 40-50 questions)
  return Math.ceil(mcq.length * 0.42)
})

const col1McqQuestions = computed(() => {
  if (!hasSecondPage.value) {
    // Single page mode: all MCQs on Page 1 / Col 1
    return mcqQuestions.value
  }
  return mcqQuestions.value.slice(0, splitIndex.value)
})

const col2McqQuestions = computed(() => {
  if (!hasSecondPage.value) {
    return []
  }
  return mcqQuestions.value.slice(splitIndex.value)
})

function getNormalizedOptions(q: any): Array<{ letter: string; text: string }> {
  if (q.options && q.options.length > 0) {
    return q.options.slice(0, 4).map((opt: any, idx: number) => ({
      letter: opt.arabic_letter || opt.letter || String(idx + 1),
      text: opt.text || '',
    }))
  }
  return [
    { letter: '1', text: 'الخيار الأول' },
    { letter: '2', text: 'الخيار الثاني' },
    { letter: '3', text: 'الخيار الثالث' },
    { letter: '4', text: 'الخيار الرابع' },
  ]
}

function getOptionText(q: any, idx: number): string {
  const opts = getNormalizedOptions(q)
  return opts[idx]?.text || ''
}

function getOptionMaxLen(q: any): number {
  const opts = getNormalizedOptions(q)
  return Math.max(...opts.map((o) => (o.text || '').length), 0)
}

function getOptionsLayout(_q: any): 'single-row' | 'two-rows' {
  // In official ministerial exam booklets, all 30 MCQs strictly use single-row 4-column options.
  return 'single-row'
}

function isLtrText(text: string): boolean {
  if (!text) return false
  const clean = text.replace(/^<p>/i, '').replace(/<\/p>$/i, '').trim()
  const hasArabic = /[\u0600-\u06FF]/.test(clean)
  const hasMathOrLatin = /[a-zA-Z0-9^=+\-*/_()\\%π]/.test(clean)
  return !hasArabic && hasMathOrLatin
}

function formatQuestionContent(content: string): string {
  if (!content) return ''
  let clean = content.replace(/^<p[^>]*>/i, '').replace(/<\/p>$/i, '').trim()
  // Isolate English phrases in parentheses (e.g. "(Inflammatory Mediators)", "(Apoptosis vs Necrosis)")
  clean = clean.replace(
    /\(([A-Za-z0-9\s,._+\-*/%&]+)\)/g,
    '&rlm;<span class="latin-term" dir="ltr">($1)</span>&rlm;'
  )
  // Ensure trailing question mark following English terms or tags stays at the natural Arabic end
  clean = clean.replace(/([A-Za-z0-9\)\}\]»”"]|<\/strong>|<\/b>|<\/span>)\s*(؟|\?)/g, '$1&rlm;&nbsp;؟&rlm;')
  return clean
}

function formatOptionContent(text: string): string {
  if (!text) return ''
  let clean = text.replace(/^<p[^>]*>/i, '').replace(/<\/p>$/i, '').trim()
  // Isolate English phrases in parentheses (e.g. "(Low Coupling & High Cohesion)", "(AES, DES)")
  clean = clean.replace(
    /\(([A-Za-z0-9\s,._+\-*/%&]+)\)/g,
    '&rlm;<span class="latin-term" dir="ltr">($1)</span>&rlm;'
  )
  return clean
}

async function printOfficialPaper() {
  await printOfficialQuestionPaper(paperRootRef.value, {
    title: `ورقة_أسئلة_${props.examSubject}_النموذج_${props.modelCode}`,
    isA3: isA3Landscape.value && hasSecondPage.value,
  })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400;1,700&display=swap');

.yemeni-official-question-paper {
  font-family: 'Amiri', 'Traditional Arabic', 'Simplified Arabic', 'Noto Naskh Arabic', Tahoma, Arial, sans-serif !important;
  color: #000000;
  background-color: #ffffff;
  box-sizing: border-box;
}

.border-black {
  border: 1px solid #000000 !important;
}

.border-bottom-black {
  border-bottom: 1px solid #000000 !important;
}

.border-left-black {
  border-left: 1px solid #000000 !important;
}

/* ── A3 SPREAD MODE (LARGE SINGLE SHEET - 420mm x 297mm) ─────── */
.a3-spread-mode {
  width: 420mm;
  min-height: 297mm;
  padding: 6mm 8mm;
  margin: 0 auto;
}

.a3-spread-mode .exam-sheet-frame.columns-two {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8mm;
  width: 100%;
}

.a3-spread-mode .exam-sheet-frame.columns-one {
  display: block;
  width: 100%;
  max-width: 210mm;
  margin: 0 auto;
}

/* Outer enclosing border for each sheet column matching authentic ministerial booklet */
.sheet-column {
  border: 1.5px solid #000000 !important;
  padding: 4px 5px !important;
  background-color: #ffffff !important;
  box-sizing: border-box !important;
}

/* ── A4 PORTRAIT MODE (TWO DISTINCT PAGES) ──────────────────── */
.a4-portrait-mode {
  width: 100%;
  max-width: 210mm;
  margin: 0 auto;
}

.a4-pages-wrapper {
  display: flex;
  flex-direction: column;
  gap: 12mm;
  width: 100%;
  align-items: center;
}

.a4-sheet-page {
  width: 210mm;
  min-height: 297mm;
  padding: 6mm 8mm;
  margin: 0 auto;
  background-color: #ffffff;
  border: 1px solid #dcdcdc;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* Outer enclosing border for A4 page content matching authentic ministerial booklet */
.page-content-wrapper {
  flex-grow: 1;
  border: 1.5px solid #000000 !important;
  padding: 4px 5px !important;
  background-color: #ffffff !important;
  box-sizing: border-box !important;
}

.a4-page-footer {
  font-size: 0.68rem;
  border-top: 1px solid #000000;
  padding-top: 3px;
  margin-top: 6px;
}

/* ── READING PASSAGE BOX ─────────────────────────────────────── */
.reading-passage-box {
  border: 1px solid #000000;
  margin-bottom: 3px;
}

.passage-text-content {
  font-size: 0.74rem;
  line-height: 1.35;
  background: #ffffff;
  padding: 4px 6px;
  font-weight: 600;
  border-top: 1px solid #000000;
}

/* ── OFFICIAL HEADER BOX ────────────────────────────────────────── */
.official-header-box {
  width: 100%;
  margin: 0 auto 3px auto;
  border: 1.5px solid #000000;
  background-color: #ffffff;
  font-family: 'Amiri', 'Traditional Arabic', 'Simplified Arabic', 'Noto Naskh Arabic', Arial, Tahoma, sans-serif !important;
  color: #000000;
  box-sizing: border-box;
}

.table-top-section {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  background-color: #ffffff;
}

.table-top-section td {
  border: 1px solid #000000;
  padding: 2px 2px;
  text-align: center;
  vertical-align: middle;
  background-color: #ffffff;
  color: #000000;
  font-size: 0.70rem;
  line-height: 1.15;
  box-sizing: border-box;
  overflow: hidden;
}

.student-photo-cell {
  width: 12.0% !important;
  padding: 1px !important;
  vertical-align: middle !important;
  background-color: #ffffff;
}

.student-photo-frame {
  width: 100%;
  height: 100%;
  max-width: 68px;
  max-height: 84px;
  border: 1px solid #000000;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
  overflow: hidden;
  box-sizing: border-box;
}

.student-photo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.photo-placeholder {
  font-size: 0.70rem;
  font-weight: 800;
  color: #222;
  text-align: center;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.emblem-cell {
  width: 19.0% !important;
  padding: 2px 2px !important;
  vertical-align: middle !important;
  background-color: #ffffff;
}

.republic-logo {
  width: 44px;
  height: auto;
  max-height: 32px;
  object-fit: contain;
  display: block;
  margin: 0 auto 2px auto;
}

.table-bottom-bar {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  border-top: 1px solid #000000;
  background-color: #ffffff;
}

.table-bottom-bar td {
  border: 1px solid #000000;
  padding: 2px 2px;
  text-align: center;
  vertical-align: middle;
  background-color: #ffffff;
  color: #000000;
  font-size: 0.76rem;
  line-height: 1.15;
  white-space: nowrap;
  box-sizing: border-box;
}

/* ── INSTRUCTION BANNERS ─────────────────────────────────────── */
.instruction-banner {
  font-family: 'Amiri', 'Traditional Arabic', 'Simplified Arabic', 'Noto Naskh Arabic', Tahoma, Arial, sans-serif !important;
  font-size: 0.76rem !important;
  font-weight: 700 !important;
  border: 1.5px solid #000000 !important;
  border-bottom: 0 !important;
  padding: 2px 6px !important;
  line-height: 1.25 !important;
  background-color: #ffffff !important;
  color: #000000 !important;
  text-align: right !important;
}

.instruction-banner.text-start {
  text-align: left !important;
}

.table-tf {
  border-collapse: collapse;
  table-layout: fixed;
  font-size: 0.76rem;
  line-height: 1.15;
  border: 1.5px solid #000000 !important;
  background-color: #ffffff;
}

.table-tf td {
  border: 1px solid #000000;
  padding: 2px 4px;
  background-color: #ffffff;
  vertical-align: middle;
}

.q-index-cell {
  background-color: #ffffff !important;
  font-family: Arial, 'Times New Roman', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.84rem !important;
  text-align: center !important;
  vertical-align: middle !important;
  padding: 2px 0 !important;
  width: 26px !important;
  color: #000000 !important;
  border: 1px solid #000000 !important;
}

.q-paren-cell {
  background-color: #ffffff !important;
  width: 32px !important;
  white-space: nowrap !important;
  word-break: keep-all !important;
  text-align: center !important;
  vertical-align: middle !important;
  padding: 2px 0 !important;
  overflow: hidden !important;
  box-sizing: border-box !important;
  border: 1px solid #000000 !important;
}

.paren-box {
  display: inline-block !important;
  direction: ltr !important;
  unicode-bidi: isolate !important;
  font-family: Arial, 'Times New Roman', sans-serif !important;
  font-size: 0.88rem !important;
  font-weight: 700 !important;
  letter-spacing: 0 !important;
  color: #000000 !important;
  line-height: 1 !important;
  margin: 0 auto !important;
}

.q-text-cell {
  font-family: 'Amiri', 'Traditional Arabic', 'Simplified Arabic', 'Noto Naskh Arabic', Tahoma, Arial, sans-serif !important;
  font-size: 0.78rem !important;
  line-height: 1.35 !important;
  font-weight: 700 !important;
  text-align: right !important;
  direction: rtl !important;
  unicode-bidi: isolate !important;
  color: #000000 !important;
  background-color: #ffffff !important;
  border: 1px solid #000000 !important;
  padding: 2px 6px !important;
}

.q-text-cell.text-left {
  text-align: left !important;
  direction: ltr !important;
}

.q-text-cell strong,
.q-text-cell b {
  font-weight: 800 !important;
  font-size: inherit !important;
}

.q-text-cell p {
  margin: 0 !important;
  display: inline !important;
  font-size: inherit !important;
}

/* ── CONTINUOUS MCQ SECTION ──────────────────────────────────── */
.table-mcq-continuous {
  border-collapse: collapse;
  width: 100%;
  border: 1.5px solid #000000 !important;
  table-layout: fixed;
  background-color: #ffffff;
}

.table-mcq-continuous td {
  border: 1px solid #000000 !important;
  padding: 2px 3px;
  background-color: #ffffff;
  vertical-align: middle;
}

.q-stem-row {
  border-top: 1.5px solid #000000 !important;
}

.q-num-cell {
  background-color: #ffffff !important;
  font-family: Arial, 'Times New Roman', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.84rem !important;
  text-align: center !important;
  vertical-align: middle !important;
  padding: 2px 0 !important;
  width: 26px !important;
  color: #000000 !important;
  border: 1px solid #000000 !important;
}

.q-stem-cell {
  font-family: 'Amiri', 'Traditional Arabic', 'Simplified Arabic', 'Noto Naskh Arabic', Tahoma, Arial, sans-serif !important;
  font-size: 0.78rem !important;
  line-height: 1.35 !important;
  font-weight: 700 !important;
  text-align: right !important;
  direction: rtl !important;
  unicode-bidi: isolate !important;
  color: #000000 !important;
  background-color: #ffffff !important;
  border: 1px solid #000000 !important;
  padding: 2px 6px !important;
}

.q-stem-cell.text-left {
  text-align: left !important;
  direction: ltr !important;
}

.q-stem-cell strong,
.q-stem-cell b {
  font-weight: 800 !important;
  font-size: inherit !important;
}

.q-stem-cell p {
  margin: 0 !important;
  display: inline !important;
  font-size: inherit !important;
}

.opt-num-cell {
  background-color: #ffffff !important;
  font-family: Arial, 'Times New Roman', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.78rem !important;
  text-align: center !important;
  vertical-align: middle !important;
  padding: 1px 0 !important;
  width: 20px !important;
  color: #000000 !important;
  border: 1px solid #000000 !important;
}

.opt-text-cell {
  font-family: 'Amiri', 'Traditional Arabic', 'Simplified Arabic', 'Noto Naskh Arabic', Tahoma, Arial, sans-serif !important;
  font-size: 0.76rem !important;
  font-weight: 700 !important;
  text-align: center !important;
  padding: 2px 4px !important;
  line-height: 1.25 !important;
  vertical-align: middle !important;
  white-space: normal;
  word-break: break-word;
  overflow-wrap: break-word;
  unicode-bidi: plaintext !important;
  color: #000000 !important;
  background-color: #ffffff !important;
  border: 1px solid #000000 !important;
}

.opt-text-inner {
  display: block;
  width: 100%;
  font-size: inherit !important;
  font-weight: inherit !important;
  white-space: normal;
  line-height: 1.25 !important;
  word-break: break-word;
  overflow-wrap: break-word;
  text-align: center;
}

.latin-term {
  direction: ltr !important;
  unicode-bidi: isolate !important;
  display: inline-block !important;
  white-space: nowrap !important;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif !important;
  font-size: 0.92em !important;
  font-weight: 700 !important;
}

.q-diagram-img {
  max-width: 140px;
  max-height: 90px;
  object-fit: contain;
}

.secret-press-ribbon {
  font-size: 0.68rem;
  font-weight: 800;
  border-bottom: 1px solid #000000;
  padding-bottom: 2px;
  margin-bottom: 2px;
}

.exam-paper-end-banner {
  font-family: 'Amiri', 'Traditional Arabic', 'Simplified Arabic', 'Noto Naskh Arabic', Tahoma, Arial, sans-serif !important;
  font-size: 0.78rem !important;
  font-weight: 700 !important;
  border: 1.5px solid #000000 !important;
  padding: 3px 6px !important;
  background-color: #ffffff !important;
  margin-top: 3px !important;
  color: #000000 !important;
  text-align: center !important;
}

.missing-field-val {
  color: #c62828 !important;
  font-weight: 800 !important;
  font-size: 0.62rem !important;
  background-color: #ffebee !important;
  padding: 1px 3px !important;
  border-radius: 2px !important;
  border: 1px dashed #ef9a9a !important;
  display: inline-block !important;
  line-height: 1.15 !important;
}

.developer-diagnostics-card {
  border: 1px solid #e0e0e0 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
  background: #fdfdfd !important;
}

/* ── PRINT MEDIA RULES ───────────────────────────────────────── */
@media print {
  .missing-field-val {
    color: #000000 !important;
    background-color: transparent !important;
    border: 1px dashed #555555 !important;
    font-size: 7.2pt !important;
  }

  .d-print-none,
  .action-bar,
  .developer-diagnostics-card,
  .v-btn,
  button {
    display: none !important;
  }

  @page {
    margin: 6mm 8mm !important;
  }

  html, body {
    margin: 0 !important;
    padding: 0 !important;
    background: #ffffff !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  .yemeni-official-question-paper {
    width: 100% !important;
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
  }

  .a4-pages-wrapper {
    gap: 0 !important;
    display: block !important;
    width: 100% !important;
  }

  .a4-sheet-page {
    width: 100% !important;
    min-height: 0 !important;
    height: auto !important;
    padding: 4mm 6mm !important;
    margin: 0 !important;
    border: none !important;
    box-shadow: none !important;
    page-break-after: always !important;
    break-after: page !important;
  }

  .a4-sheet-page:last-child {
    page-break-after: auto !important;
    break-after: auto !important;
  }

  .a3-spread-mode {
    width: 100% !important;
    min-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
  }

  .exam-sheet-frame {
    width: 100% !important;
    gap: 8mm !important;
  }

  .mcq-question-box,
  .tf-row,
  .q-stem-row,
  .q-options-row,
  .table-official-header,
  .reading-passage-box {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }
}
</style>
