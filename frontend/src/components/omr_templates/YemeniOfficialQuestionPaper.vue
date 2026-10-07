<template>
  <div
    ref="paperRootRef"
    class="yemeni-official-question-paper bg-white text-black"
    :class="{ 'a3-spread-mode': isA3Landscape, 'a4-portrait-mode': !isA3Landscape }"
    dir="rtl"
  >
    <!-- ── Print Action Toolbar (Hidden during printing) ────────── -->
    <div class="d-print-none action-bar px-4 py-2 mb-3 rounded-lg border bg-grey-lighten-4 d-flex align-center justify-space-between flex-wrap gap-2">
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
              <col style="width: 17.5%;">
              <col style="width: 7.5%;">
              <col style="width: 35.0%;">
              <col style="width: 9.0%;">
              <col style="width: 12.0%;">
              <col style="width: 19.0%;">
            </colgroup>
            <tbody>
              <!-- Row 1: Student Photo (spans 5) + Governorate & Directorate + Republic Emblem (spans 5) -->
              <tr>
                <!-- Far Right: Student Photo Box (spans rows 1 to 5) -->
                <td rowspan="5" class="student-photo-cell">
                  <div class="student-photo-frame">
                    <img v-if="studentPhoto" :src="studentPhoto" alt="صورة الطالب" class="student-photo-img" />
                    <div v-else class="photo-placeholder">صورة شخصية</div>
                  </div>
                </td>

                <!-- Governorate & Directorate -->
                <td class="font-weight-bold" style="font-size: 0.68rem;">المحافظة</td>
                <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ governorate || 'أمانة العاصمة' }}</td>
                <td class="font-weight-bold" style="font-size: 0.68rem;">المديرية</td>
                <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ directorate || 'الثورة / الأمانة' }}</td>

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
                <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ centerName || 'حفصة - الحوك الحديدة' }}</td>
                <td class="font-weight-bold" style="font-size: 0.68rem;">رقمه</td>
                <td class="font-weight-bold font-mono" style="font-size: 0.74rem;">{{ centerCode || '3026' }}</td>
              </tr>

                <!-- Row 3: Time, Day, Date (Exact match to real ministerial layout) -->
                <tr>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">الزمن</td>
                  <td class="font-weight-bold time-cell" style="padding: 1px 2px; line-height: 1.2;">
                    <div style="font-size: 0.58rem; white-space: nowrap;">{{ formattedTimeLine1 }}</div>
                    <div style="font-size: 0.54rem; margin-top: 1px; white-space: nowrap;">{{ formattedTimeLine2 }}</div>
                  </td>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">اليوم</td>
                  <td class="font-weight-bold" style="font-size: 0.68rem; white-space: nowrap;">{{ dayName || 'السبت' }}</td>
                </tr>

                <!-- Row 4: Stage Title & Academic Year (colspan 4) -->
                <tr>
                  <td colspan="4" class="font-weight-black stage-year-cell" style="padding: 2px 2px; text-align: center; overflow: hidden; line-height: 1.25;">
                    <div style="font-size: 0.60rem; white-space: nowrap; letter-spacing: -0.2px;">{{ formattedStageLine1 }}</div>
                    <div style="font-size: 0.58rem; margin-top: 1px;">{{ formattedStageLine2 }}</div>
                  </td>
                </tr>

              <!-- Row 5: Subject & Envelope No -->
              <tr>
                <td class="font-weight-bold" style="font-size: 0.68rem;">اسم المادة</td>
                <td class="font-weight-black" style="font-size: 0.84rem;">{{ isEnglish ? 'English' : (examSubject || 'الأحياء') }}</td>
                <td class="font-weight-bold" style="font-size: 0.68rem;">رقم مظروف</td>
                <td class="font-weight-bold font-mono" style="font-size: 0.74rem;">{{ envelopeNo || '1' }}</td>
              </tr>
            </tbody>
          </table>

          <!-- Row 6: Exact Match to Original (Bottom Student Info Bar) -->
          <table class="table-bottom-bar w-100">
            <colgroup>
              <col style="width: 10.5%;">
              <col style="width: 46.5%;">
              <col style="width: 9.5%;">
              <col style="width: 16.5%;">
              <col style="width: 8.5%;">
              <col style="width: 8.5%;">
            </colgroup>
            <tbody>
              <tr>
                <td class="font-weight-black" style="font-size: 0.78rem;">الاسم</td>
                <td class="font-weight-black" style="font-size: 0.82rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                  {{ studentName || 'علاء جميل صالح القربي' }}
                </td>
                <td class="font-weight-black" style="font-size: 0.70rem;">رقم الجلوس</td>
                <td class="font-weight-black font-mono" style="font-size: 0.85rem;">{{ seatNumber || '651736' }}</td>
                <td class="font-weight-black" style="font-size: 0.70rem;">مسلسل</td>
                <td class="font-weight-black font-mono" style="font-size: 0.85rem;">{{ secretNumber || '60' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 2. True / False Section (القسم الأول: صح وخطأ) -->
        <div v-if="tfQuestions.length > 0" class="tf-section-wrapper mb-1" :dir="isEnglish ? 'ltr' : 'rtl'">
          <!-- Instruction Banner -->
          <div class="instruction-banner py-1 font-weight-bold" :class="isEnglish ? 'text-start ps-2' : 'text-center'">
            {{ tfInstructionText }}
          </div>

          <!-- True/False Questions Compact Table -->
          <table class="table-tf w-100" :dir="isEnglish ? 'ltr' : 'rtl'">
            <colgroup>
              <col style="width: 26px;">
              <col style="width: 36px;">
              <col style="width: auto;">
            </colgroup>
            <tbody>
              <tr v-for="q in tfQuestions" :key="`tf-${q.orderIndex}`" class="tf-row">
                <td class="q-index-cell text-center font-weight-black font-mono">{{ q.orderIndex }}</td>
                <td class="q-paren-cell text-center font-mono font-weight-bold" dir="ltr" style="white-space: nowrap !important; word-break: keep-all !important; letter-spacing: 0;">(&nbsp;&nbsp;&nbsp;)</td>
                <td class="q-text-cell pe-2 ps-2 py-1 font-weight-bold" :class="isEnglish ? 'text-start' : 'text-end'" v-html="q.content"></td>
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
          <div class="instruction-banner py-1 font-weight-bold" :class="isEnglish ? 'text-start ps-2' : 'text-center'">
            {{ mcqInstructionText }}
          </div>

          <!-- Continuous MCQ Table for Column 1 -->
          <table class="table-mcq-continuous w-100" :dir="isEnglish ? 'ltr' : 'rtl'">
            <colgroup>
              <col style="width: 26px;">
              <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
              <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
              <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
              <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
            </colgroup>
            <tbody>
              <template v-for="q in col1McqQuestions" :key="`mcq-${q.orderIndex}`">
                <tr class="q-stem-row">
                  <td
                    rowspan="2"
                    class="q-num-cell text-center font-weight-black font-mono"
                  >
                    {{ q.orderIndex }}
                  </td>
                  <td colspan="8" class="q-stem-cell pe-2 ps-2 py-1 font-weight-bold" :class="isEnglish ? 'text-start' : 'text-end'">
                    <div v-if="q.image || q.figure" class="d-flex align-center justify-space-between w-100">
                      <span v-html="q.content"></span>
                      <img :src="q.image || q.figure" alt="رسم توضيحي للسؤال" class="q-diagram-img ms-2" />
                    </div>
                    <span v-else v-html="q.content"></span>
                  </td>
                </tr>
                <tr class="q-options-row text-center">
                  <td class="opt-num-cell font-mono font-weight-black">1</td>
                  <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 0)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 0) }}</span></td>
                  <td class="opt-num-cell font-mono font-weight-black">2</td>
                  <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 1)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 1) }}</span></td>
                  <td class="opt-num-cell font-mono font-weight-black">3</td>
                  <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 2)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 2) }}</span></td>
                  <td class="opt-num-cell font-mono font-weight-black">4</td>
                  <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 3)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 3) }}</span></td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>

        <!-- Bottom Footer Banner if only 1 column has questions -->
        <div v-if="col2McqQuestions.length === 0" class="exam-paper-end-banner text-center font-weight-black">
          {{ endBannerText }}
        </div>
      </div>

      <!-- ── COLUMN 2 (LEFT): MCQ CONTINUATION + DIAGRAMS ───────── -->
      <div v-if="col2McqQuestions.length > 0" class="sheet-column column-left">

        <!-- Watermark / Secret Printing Press Vertical Side Ribbon -->
        <div class="secret-press-ribbon d-flex justify-space-between align-center mb-1 pb-1" :dir="isEnglish ? 'ltr' : 'rtl'">
          <span>{{ secretPressRibbonText.press }}</span>
          <span class="font-mono">{{ secretPressRibbonText.continuation }}</span>
        </div>

        <!-- Continuous MCQ Table for Column 2 -->
        <table class="table-mcq-continuous w-100" :dir="isEnglish ? 'ltr' : 'rtl'">
          <colgroup>
            <col style="width: 26px;">
            <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
            <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
            <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
            <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
          </colgroup>
          <tbody>
            <template v-for="q in col2McqQuestions" :key="`mcq-${q.orderIndex}`">
              <tr class="q-stem-row">
                <td
                  rowspan="2"
                  class="q-num-cell text-center font-weight-black font-mono"
                >
                  {{ q.orderIndex }}
                </td>
                <td colspan="8" class="q-stem-cell pe-2 ps-2 py-1 font-weight-bold" :class="isEnglish ? 'text-start' : 'text-end'">
                  <div v-if="q.image || q.figure" class="d-flex align-center justify-space-between w-100">
                    <span v-html="q.content"></span>
                    <img :src="q.image || q.figure" alt="رسم توضيحي للسؤال" class="q-diagram-img ms-2" />
                  </div>
                  <span v-else v-html="q.content"></span>
                </td>
              </tr>
              <tr class="q-options-row text-center">
                <td class="opt-num-cell font-mono font-weight-black">1</td>
                <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 0)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 0) }}</span></td>
                <td class="opt-num-cell font-mono font-weight-black">2</td>
                <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 1)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 1) }}</span></td>
                <td class="opt-num-cell font-mono font-weight-black">3</td>
                <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 2)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 2) }}</span></td>
                <td class="opt-num-cell font-mono font-weight-black">4</td>
                <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 3)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 3) }}</span></td>
              </tr>
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
                <col style="width: 17.5%;">
                <col style="width: 7.5%;">
                <col style="width: 35.0%;">
                <col style="width: 9.0%;">
                <col style="width: 12.0%;">
                <col style="width: 19.0%;">
              </colgroup>
              <tbody>
                <!-- Row 1: Student Photo (spans 5) + Governorate & Directorate + Republic Emblem (spans 5) -->
                <tr>
                  <!-- Far Right: Student Photo Box (spans rows 1 to 5) -->
                  <td rowspan="5" class="student-photo-cell">
                    <div class="student-photo-frame">
                      <img v-if="studentPhoto" :src="studentPhoto" alt="صورة الطالب" class="student-photo-img" />
                      <div v-else class="photo-placeholder">صورة شخصية</div>
                    </div>
                  </td>

                  <!-- Governorate & Directorate -->
                  <td class="font-weight-bold" style="font-size: 0.68rem;">المحافظة</td>
                  <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ governorate || 'أمانة العاصمة' }}</td>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">المديرية</td>
                  <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ directorate || 'الثورة / الأمانة' }}</td>

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
                  <td class="font-weight-bold" style="font-size: 0.68rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ centerName || 'حفصة - الحوك الحديدة' }}</td>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">رقمه</td>
                  <td class="font-weight-bold font-mono" style="font-size: 0.74rem;">{{ centerCode || '3026' }}</td>
                </tr>

                <!-- Row 3: Time, Day, Date (Exact match to real ministerial layout) -->
                <tr>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">الزمن</td>
                  <td class="font-weight-bold time-cell" style="padding: 1px 2px; line-height: 1.2;">
                    <div style="font-size: 0.58rem; white-space: nowrap;">{{ formattedTimeLine1 }}</div>
                    <div style="font-size: 0.54rem; margin-top: 1px; white-space: nowrap;">{{ formattedTimeLine2 }}</div>
                  </td>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">اليوم</td>
                  <td class="font-weight-bold" style="font-size: 0.68rem; white-space: nowrap;">{{ dayName || 'السبت' }}</td>
                </tr>

                <!-- Row 4: Stage Title & Academic Year (colspan 4) -->
                <tr>
                  <td colspan="4" class="font-weight-black stage-year-cell" style="padding: 2px 2px; text-align: center; overflow: hidden; line-height: 1.25;">
                    <div style="font-size: 0.60rem; white-space: nowrap; letter-spacing: -0.2px;">{{ formattedStageLine1 }}</div>
                    <div style="font-size: 0.58rem; margin-top: 1px;">{{ formattedStageLine2 }}</div>
                  </td>
                </tr>

                <!-- Row 5: Subject & Envelope No -->
                <tr>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">اسم المادة</td>
                  <td class="font-weight-black" style="font-size: 0.84rem;">{{ isEnglish ? 'English' : (examSubject || 'الأحياء') }}</td>
                  <td class="font-weight-bold" style="font-size: 0.68rem;">رقم مظروف</td>
                  <td class="font-weight-bold font-mono" style="font-size: 0.74rem;">{{ envelopeNo || '1' }}</td>
                </tr>
              </tbody>
            </table>

            <!-- Row 6: Exact Match to Original (Bottom Student Info Bar) -->
            <table class="table-bottom-bar w-100">
              <colgroup>
                <col style="width: 10.5%;">
                <col style="width: 46.5%;">
                <col style="width: 9.5%;">
                <col style="width: 16.5%;">
                <col style="width: 8.5%;">
                <col style="width: 8.5%;">
              </colgroup>
              <tbody>
                <tr>
                  <td class="font-weight-black" style="font-size: 0.78rem;">الاسم</td>
                  <td class="font-weight-black" style="font-size: 0.82rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {{ studentName || 'علاء جميل صالح القربي' }}
                  </td>
                  <td class="font-weight-black" style="font-size: 0.70rem;">رقم الجلوس</td>
                  <td class="font-weight-black font-mono" style="font-size: 0.85rem;">{{ seatNumber || '651736' }}</td>
                  <td class="font-weight-black" style="font-size: 0.70rem;">مسلسل</td>
                  <td class="font-weight-black font-mono" style="font-size: 0.85rem;">{{ secretNumber || '60' }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 2. True / False Section -->
          <div v-if="tfQuestions.length > 0" class="tf-section-wrapper mb-1" :dir="isEnglish ? 'ltr' : 'rtl'">
            <div class="instruction-banner py-1 font-weight-bold" :class="isEnglish ? 'text-start ps-2' : 'text-center'">
              {{ tfInstructionText }}
            </div>
            <table class="table-tf w-100" :dir="isEnglish ? 'ltr' : 'rtl'">
              <colgroup>
                <col style="width: 26px;">
                <col style="width: 36px;">
                <col style="width: auto;">
              </colgroup>
              <tbody>
                <tr v-for="q in tfQuestions" :key="`a4-tf-${q.orderIndex}`" class="tf-row">
                  <td class="q-index-cell text-center font-weight-black font-mono">{{ q.orderIndex }}</td>
                  <td class="q-paren-cell text-center font-mono font-weight-bold" dir="ltr" style="white-space: nowrap !important; word-break: keep-all !important; letter-spacing: 0;">(&nbsp;&nbsp;&nbsp;)</td>
                  <td class="q-text-cell pe-2 ps-2 py-1 font-weight-bold" :class="isEnglish ? 'text-start' : 'text-end'" v-html="q.content"></td>
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
            <div class="instruction-banner py-1 font-weight-bold" :class="isEnglish ? 'text-start ps-2' : 'text-center'">
              {{ mcqInstructionText }}
            </div>
            <table class="table-mcq-continuous w-100" :dir="isEnglish ? 'ltr' : 'rtl'">
              <colgroup>
                <col style="width: 26px;">
                <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
                <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
                <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
                <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
              </colgroup>
              <tbody>
                <template v-for="q in col1McqQuestions" :key="`a4-mcq-${q.orderIndex}`">
                  <tr class="q-stem-row">
                    <td rowspan="2" class="q-num-cell text-center font-weight-black font-mono">
                      {{ q.orderIndex }}
                    </td>
                    <td colspan="8" class="q-stem-cell pe-2 ps-2 py-1 font-weight-bold" :class="isEnglish ? 'text-start' : 'text-end'">
                      <div v-if="q.image || q.figure" class="d-flex align-center justify-space-between w-100">
                        <span v-html="q.content"></span>
                        <img :src="q.image || q.figure" alt="رسم توضيحي للسؤال" class="q-diagram-img ms-2" />
                      </div>
                      <span v-else v-html="q.content"></span>
                    </td>
                  </tr>
                  <tr class="q-options-row text-center">
                    <td class="opt-num-cell font-mono font-weight-black">1</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 0)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 0) }}</span></td>
                    <td class="opt-num-cell font-mono font-weight-black">2</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 1)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 1) }}</span></td>
                    <td class="opt-num-cell font-mono font-weight-black">3</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 2)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 2) }}</span></td>
                    <td class="opt-num-cell font-mono font-weight-black">4</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 3)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 3) }}</span></td>
                  </tr>
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
        <div class="a4-page-footer d-flex justify-space-between align-center font-weight-bold pt-2 mt-2 border-t">
          <span>{{ isEnglish ? 'English' : examSubject }} • {{ isEnglish ? 'Form' : 'النموذج' }} ({{ modelCode || '1' }})</span>
          <span>{{ isEnglish ? (hasSecondPage ? 'Page 1 of 2 (Turn over)' : 'Page 1 of 1') : (hasSecondPage ? 'الصفحة 1 من 2 (يتبع في الصفحة التالية)' : 'الصفحة 1 من 1') }}</span>
        </div>
      </div>

      <!-- ── PAGE 2 (A4): TOP RIBBON + PART 2 MCQs + END BANNER ─── -->
      <div v-if="hasSecondPage" class="a4-sheet-page sheet-page-2 mt-4">
        <div class="page-content-wrapper">
          <!-- Ribbon -->
          <div class="secret-press-ribbon d-flex justify-space-between align-center mb-1 pb-1" :dir="isEnglish ? 'ltr' : 'rtl'">
            <span>{{ secretPressRibbonText.press }}</span>
            <span class="font-mono">{{ secretPressRibbonText.continuation }}</span>
          </div>

          <!-- MCQs Part 2 -->
          <div class="mcq-section-wrapper" :dir="isEnglish ? 'ltr' : 'rtl'">
            <table class="table-mcq-continuous w-100" :dir="isEnglish ? 'ltr' : 'rtl'">
              <colgroup>
                <col style="width: 26px;">
                <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
                <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
                <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
                <col style="width: 20px;"><col style="width: calc(25% - 11.5px);">
              </colgroup>
              <tbody>
                <template v-for="q in col2McqQuestions" :key="`a4-mcq2-${q.orderIndex}`">
                  <tr class="q-stem-row">
                    <td rowspan="2" class="q-num-cell text-center font-weight-black font-mono">
                      {{ q.orderIndex }}
                    </td>
                    <td colspan="8" class="q-stem-cell pe-2 ps-2 py-1 font-weight-bold" :class="isEnglish ? 'text-start' : 'text-end'">
                      <div v-if="q.image || q.figure" class="d-flex align-center justify-space-between w-100">
                        <span v-html="q.content"></span>
                        <img :src="q.image || q.figure" alt="رسم توضيحي للسؤال" class="q-diagram-img ms-2" />
                      </div>
                      <span v-else v-html="q.content"></span>
                    </td>
                  </tr>
                  <tr class="q-options-row text-center">
                    <td class="opt-num-cell font-mono font-weight-black">1</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 0)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 0) }}</span></td>
                    <td class="opt-num-cell font-mono font-weight-black">2</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 1)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 1) }}</span></td>
                    <td class="opt-num-cell font-mono font-weight-black">3</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 2)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 2) }}</span></td>
                    <td class="opt-num-cell font-mono font-weight-black">4</td>
                    <td class="opt-text-cell font-weight-bold" :class="isEnglish ? 'text-start ps-1' : 'text-center'"><span :dir="isLtrText(getOptionText(q, 3)) ? 'ltr' : 'auto'" style="unicode-bidi: isolate; display: inline-block;">{{ getOptionText(q, 3) }}</span></td>
                  </tr>
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
        <div class="a4-page-footer d-flex justify-space-between align-center font-weight-bold pt-2 mt-2 border-t">
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
    examTitle: 'اختبار الشهادة الثانوية العامة (القسم العلمي)',
    examSubject: 'الأحياء',
    stageTitle: 'اختبار الشهادة الثانوية العامة (المراكز الفرعية - علمي)',
    examYear: '1445هـ - 2023-2024م',
    governorate: 'أمانة العاصمة',
    directorate: 'الثورة / الأمانة',
    centerName: 'حفصة - الحوك الحديدة',
    centerCode: '3026',
    examTime: 'ثلاث ساعات (من 8:30 إلى 11:30)',
    dayName: 'السبت',
    examDate: '2024/5/18م - 1445/11/10هـ',
    envelopeNo: '1',
    studentName: 'علاء جميل صالح القربي',
    seatNumber: '651736',
    secretNumber: '60',
    modelCode: '1',
    studentPhoto: '',
    tfMark: 1,
    mcqMark: 2,
    totalScore: 80,
    readingPassage: '',
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
    let totalCount = 0
    for (const q of qs.slice(0, 10)) {
      const text = (q.content || '') + ' ' + (q.options || []).map(o => o.text).join(' ')
      latinCount += (text.match(/[a-zA-Z]/g) || []).length
      totalCount += text.replace(/\s+/g, '').length
    }
    if (totalCount > 0 && latinCount / totalCount > 0.4) {
      return true
    }
  }
  return false
})

const displayExamYear = computed(() => {
  const y = String(props.examYear || '').trim()
  if (!y || y === '1' || y === '0' || y.length < 4) {
    return '1445هـ - 2024-2023م'
  }
  return y
})

const tfInstructionText = computed(() => {
  if (isEnglish.value) {
    return `Read the following questions, and on the answer sheet, darken the number that matches the correct alternative.\nPart One: Mark (T/True) for the true statements and (F/False) for the false ones.    (${props.tfMark || 1}) point each`
  }
  return `ظلل في ورقة الإجابة الدائرة التي تحتوي على الحرف (ص) للإجابة الصحيحة والحرف (خ) للإجابة الخطأ بحسب رقم الفقرة لكل مما يأتي: ${props.tfMark || 1} درجة لكل فقرة.`
})

const mcqInstructionText = computed(() => {
  if (isEnglish.value) {
    return `Part two: Choose the best alternative:    (${props.mcqMark || 2}) points each`
  }
  return `اختر الإجابة الصحيحة ثم ظلل في ورقة الإجابة الدائرة بحسب الاختيار ورقم الفقرة لكل مما يأتي: ${props.mcqMark || 2} درجات لكل فقرة.`
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

const formattedTimeLine1 = computed(() => {
  const t = props.examTime || ''
  if (!t || t.includes('8:30') || t.includes('ثلاث ساعات')) {
    return isEnglish.value ? 'Three hours from 8:30 AM to' : 'ثلاث ساعات من الساعة 8:30 صباحاً وحتى'
  }
  if (t.includes('وحتى')) {
    return t.split('وحتى')[0].trim() + (isEnglish.value ? ' to' : ' وحتى')
  }
  return t
})

const formattedTimeLine2 = computed(() => {
  const t = props.examTime || ''
  const d = props.examDate || '1445/11/10هـ - 2024/5/18م'
  if (t.includes('وحتى')) {
    const afterUntil = t.split('وحتى')[1].trim()
    if (d.includes(afterUntil)) return d
    return `${afterUntil} - ${d}`
  }
  if (d.includes('11:30')) return d
  return `11:30 - ${d}`
})

const formattedStageLine1 = computed(() => {
  const st = props.stageTitle || 'اختبار الشهادة الثانوية العامة (المراكز الفرعية-علمي)'
  const yr = props.examYear || '1445هـ - 2024-2023م'
  if (st.includes('1445') || st.includes('للعام')) {
    return st
  }
  const hijriMatch = yr.match(/(\d{4}\s*هـ?)/)
  const hijriStr = hijriMatch ? hijriMatch[1].replace('ه', '') + 'هـ' : '1445هـ'
  if (isEnglish.value) {
    return `${st} Academic Year ${hijriStr}`
  }
  return `${st} للعام الدراسي ${hijriStr}`
})

const formattedStageLine2 = computed(() => {
  const yr = props.examYear || '1445هـ - 2024-2023م'
  const gregMatch = yr.match(/(\d{4}\s*[-/]\s*\d{4}\s*م?)/)
  if (gregMatch) {
    let g = gregMatch[1].trim()
    if (!g.endsWith('م')) g += 'م'
    if (!g.startsWith('-')) g = '-' + g
    return g
  }
  return '-2024-2023م'
})

// Filter True/False vs MCQ Questions
const tfQuestions = computed(() => {
  return (props.questions || []).filter((q) => {
    const typeStr = String(q.questionType || '').toLowerCase()
    return typeStr.includes('true') || typeStr.includes('false') || typeStr.includes('صح') || typeStr.includes('خطأ')
  })
})

const mcqQuestions = computed(() => {
  return (props.questions || []).filter((q) => {
    const typeStr = String(q.questionType || '').toLowerCase()
    return !(typeStr.includes('true') || typeStr.includes('false') || typeStr.includes('صح') || typeStr.includes('خطأ'))
  })
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
    const col1Capacity = effectiveReadingPassage.value ? 6 : 10
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

function isLtrText(text: string): boolean {
  if (!text) return false
  const clean = text.replace(/^<p>/i, '').replace(/<\/p>$/i, '').trim()
  const hasArabic = /[\u0600-\u06FF]/.test(clean)
  const hasMathOrLatin = /[a-zA-Z0-9^=+\-*/_()\\%π]/.test(clean)
  return !hasArabic && hasMathOrLatin
}

async function printOfficialPaper() {
  await printOfficialQuestionPaper(paperRootRef.value, {
    title: `ورقة_أسئلة_${props.examSubject}_النموذج_${props.modelCode}`,
    isA3: isA3Landscape.value && hasSecondPage.value,
  })
}
</script>

<style scoped>
.yemeni-official-question-paper {
  font-family: 'Tajawal', 'Cairo', -apple-system, BlinkMacSystemFont, 'Segoe UI', Tahoma, sans-serif !important;
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
  padding: 8mm 10mm;
  margin: 0 auto;
  background-color: #ffffff;
  border: 1px solid #dcdcdc;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.page-content-wrapper {
  flex-grow: 1;
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
  margin: 0 auto 4px auto;
  border: 1.5px solid #000000;
  background-color: #ffffff;
  font-family: 'Arial', 'Simplified Arabic', Tahoma, sans-serif !important;
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
  font-size: 0.68rem;
  line-height: 1.15;
  box-sizing: border-box;
  overflow: hidden;
}

.student-photo-cell {
  width: 17.5% !important;
  padding: 2px !important;
  vertical-align: middle !important;
  background-color: #ffffff;
}

.student-photo-frame {
  width: 82px;
  height: 100px;
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
  font-size: 0.70rem;
  font-weight: 800;
  border: 1px solid #000000;
  border-bottom: 0;
  padding: 2.5px 4px;
  line-height: 1.2;
  background-color: #ffffff;
  color: #000000;
}

.table-tf {
  border-collapse: collapse;
  table-layout: fixed;
  font-size: 0.74rem;
  line-height: 1.15;
  border: 1px solid #000000;
  background-color: #ffffff;
}

.table-tf td {
  border: 1px solid #000000;
  padding: 1.5px 3px;
  background-color: #ffffff;
}

.q-index-cell {
  font-weight: 900;
  font-size: 0.78rem;
}

.q-paren-cell {
  white-space: nowrap !important;
  word-break: keep-all !important;
  direction: ltr !important;
  text-align: center !important;
  letter-spacing: 0 !important;
  font-family: monospace, sans-serif !important;
  font-size: 0.85rem !important;
  font-weight: 900 !important;
  color: #111;
}

.q-text-cell {
  font-weight: 600;
  unicode-bidi: plaintext !important;
}

/* ── CONTINUOUS MCQ SECTION ──────────────────────────────────── */
.table-mcq-continuous {
  border-collapse: collapse;
  width: 100%;
  border: 1px solid #000000 !important;
  table-layout: fixed;
  background-color: #ffffff;
}

.table-mcq-continuous td {
  border: 1px solid #000000 !important;
  padding: 1px 2px;
  background-color: #ffffff;
}

.q-num-cell {
  font-family: monospace, sans-serif;
  font-weight: 900;
  font-size: 0.82rem;
  text-align: center;
}

.q-stem-cell {
  font-size: 0.75rem;
  line-height: 1.25;
  font-weight: 700;
  unicode-bidi: plaintext !important;
}

.opt-num-cell {
  font-family: monospace, sans-serif;
  font-weight: 900;
  font-size: 0.74rem;
  text-align: center;
}

.opt-text-cell {
  font-size: 0.70rem;
  font-weight: 700;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  unicode-bidi: plaintext !important;
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
  font-size: 0.76rem;
  font-weight: 900;
  border: 1px solid #000000;
  padding: 3px 6px;
  background-color: #ffffff;
  margin-top: 4px;
}

/* ── PRINT MEDIA RULES ───────────────────────────────────────── */
@media print {
  .d-print-none,
  .action-bar,
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
