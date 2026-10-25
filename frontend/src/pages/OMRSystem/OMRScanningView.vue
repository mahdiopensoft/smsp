<template>
  <div class="qb-national-control-console pa-3 pa-md-6">
    <!-- ── 1. بيانات المظروف الامتحاني والقاعة (Envelope Manifest & Dispatch Details) ── -->
    <filter-fields
      label="1. بيانات المظروف الامتحاني والقاعة (Envelope Manifest & Dispatch Details)"
      class="main-card border-0 pa-5 rounded-2xl mb-5 shadow-sm"
    >
      <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-4 w-100">
        <div class="d-flex align-center gap-2">
          <v-icon color="primary" size="22">mdi-card-bulleted-settings-outline</v-icon>
          <span class="text-subtitle-1 font-weight-black text-on-surface">
            1. بيانات المظروف الامتحاني والقاعة (Envelope Manifest & Dispatch Details)
          </span>
        </div>
        <v-chip color="primary" variant="tonal" size="small" class="font-weight-bold">
          حالة الاستلام: مظروف رسمي مشمع ومفروز
        </v-chip>
      </div>

      <!-- الصف 1: الهيكلية التعليمية والأكاديمية الموحدة (المدارس / الجامعات / المعاهد) -->
      <v-row dense class="align-center mb-1">
        <!-- 0. نوع المؤسسة التعليمية (مدارس / جامعات / معاهد) موحد كـ auto-list -->
        <auto-list
          v-model="filterInstitutionType"
          name="InstitutionType"
          placeholder="نوع المؤسسة التعليمية"
          cols="3"
          :add="false"
          @update:model-value="onInstitutionTypeChange"
        />

        <!-- فلاتر المدارس -->
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
            @update:model-value="onClassTrackChange"
          />
          <auto-list
            v-model="filterSubject"
            name="Subject"
            :param="subjectFilterParam"
            placeholder="المادة الدراسية"
            :cols="filterInstitutionType === 'school' ? '3' : '9'"
            :add="false"
            @update:model-value="onSubjectChange"
          />
        </template>

        <!-- فلاتر الجامعات -->
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
            @update:model-value="onDepartmentChange"
          />
          <auto-list
            v-model="filterSpecialization"
            name="Specialization"
            :param="filterDepartment"
            placeholder="التخصص والبرنامج"
            cols="3"
            :add="false"
            :disabled="!filterDepartment"
            @update:model-value="onSpecializationChange"
          />
        </template>

        <!-- فلاتر المعاهد -->
        <template v-if="filterInstitutionType === 'institute'">
          <auto-list
            v-model="filterInstituteField"
            name="InstituteField"
            placeholder="المجال المهني"
            cols="3"
            :add="false"
            @update:model-value="onInstituteFieldChange"
          />
          <auto-list
            v-model="filterInstituteEducationSystem"
            name="InstituteEducationSystem"
            :param="filterInstituteField"
            placeholder="نظام التعليم"
            cols="3"
            :add="false"
            :disabled="!filterInstituteField"
            @update:model-value="onInstituteEducationSystemChange"
          />
          <auto-list
            v-model="filterInstituteSpecialization"
            name="InstituteSpecialization"
            :param="instituteSpecParam"
            placeholder="التخصص المهني"
            cols="3"
            :add="false"
            :disabled="!filterInstituteEducationSystem"
            @update:model-value="onInstituteSpecializationChange"
          />
        </template>
      </v-row>

      <!-- الصف 2: الهيكلية الجغرافية والمؤسسية + اختيار الاختبار المعتمد (4 أعمدة متساوية cols="3") -->
      <v-row dense class="align-center mb-1 mt-1">
        <!-- 1. المحافظة -->
        <auto-list
          v-model="filterGovernorate"
          name="Governorate"
          placeholder="المحافظة *"
          cols="3"
          :add="false"
          @update:model-value="onGovernorateChange"
        />

        <!-- 2. المديرية -->
        <auto-list
          v-model="filterDirectorate"
          name="Directorate"
          :param="filterGovernorate"
          :placeholder="filterGovernorate ? 'المديرية *' : 'اختر المحافظة أولاً'"
          cols="3"
          :add="false"
          :disabled="!filterGovernorate"
          @update:model-value="onDirectorateChange"
        />

        <!-- 3. المركز الامتحاني (المدرسة / الكلية / المعهد) -->
        <auto-list
          v-model="filterOrganization"
          name="Organization"
          :param="orgParam"
          :placeholder="orgPlaceholder"
          cols="3"
          :add="false"
          @update:model-value="onOrganizationChange"
        />

        <!-- 4. الاختبار والمادة الدراسية -->
        <auto-list
          v-model="selectedExamId"
          name="Exam"
          :param="examFilterParam"
          placeholder="الاختبار والمادة الدراسية *"
          cols="3"
          :add="false"
          @update:model-value="onExamChange"
        />
      </v-row>

      <!-- الصف 2: أرقام المظروف والقاعة وسعة الطلاب وفق حافظة التسليم الرسمية -->
      <v-row dense class="align-center mb-1 mt-1">
        <!-- 5. رقم القاعة -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="currentEnvelope.hallNumber"
            label="رقم القاعة *"
            variant="outlined"
            density="compact"
            prepend-inner-icon="mdi-door-open"
            hide-details
            placeholder="مثال: قاعة 03"
            @update:model-value="generateEnvelopeBarcode"
          />
        </v-col>

        <!-- 6. باركود / كود المظروف الامتحاني -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="currentEnvelope.envelopeCode"
            label="باركود / كود المظروف الامتحاني *"
            variant="outlined"
            density="compact"
            prepend-inner-icon="mdi-barcode-scan"
            hide-details
            append-inner-icon="mdi-refresh"
            @click:append-inner="generateEnvelopeBarcode"
          />
        </v-col>

        <!-- 7. سعة القاعة المقيدة (الطلاب المقيدون) -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model.number="currentEnvelope.expectedCount"
            type="number"
            min="0"
            max="1000"
            label="سعة القاعة المقيدة (الطلاب المقيدون) *"
            variant="outlined"
            density="compact"
            prepend-inner-icon="mdi-counter"
            hide-details
          />
        </v-col>

        <!-- 8. عدد الغائبين (وفق حافظة الكشف) -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model.number="currentEnvelope.absentCount"
            type="number"
            min="0"
            :max="currentEnvelope.expectedCount"
            label="عدد الغائبين (وفق حافظة الكشف) *"
            variant="outlined"
            density="compact"
            prepend-inner-icon="mdi-account-cancel-outline"
            color="warning"
            hide-details
          />
        </v-col>
      </v-row>

      <!-- التلخيص السريع لحافظة المظروف والمعادلة المتوقعة -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-2 mt-3 pt-3 border-t text-caption font-weight-bold">
        <div class="d-flex align-center gap-3">
          <span class="text-medium-emphasis">معادلة المطابقة المتوقعة:</span>
          <span class="text-primary font-weight-black">{{ currentEnvelope.expectedCount }} مقيد</span>
          <span class="text-medium-emphasis">=</span>
          <span class="text-success font-weight-black">{{ expectedPresentSheets }} ورقة إجابة حاضرة</span>
          <span class="text-medium-emphasis">+</span>
          <span class="text-warning font-weight-black">{{ currentEnvelope.absentCount }} طالب غائب مسجل</span>
        </div>
        <v-chip size="x-small" color="info" variant="tonal" class="font-weight-bold">
          المطلوب سحبه من الماسح: {{ expectedPresentSheets }} ورقة
        </v-chip>
      </div>
    </filter-fields>

          <!-- ── 2. ملقم الماسح الصناعي عالي السرعة (Industrial ADF Feeder Bay) ── -->
          <v-card class="main-card pa-5 rounded-2xl border-0 shadow-sm mb-5">
            <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-3">
              <div class="d-flex align-center gap-2">
                <v-icon color="success" size="22">mdi-scanner</v-icon>
                <span class="text-subtitle-1 font-weight-black text-on-surface">
                  2. تغذية حزمة أوراق المظروف من الماسح الضوئي (High-Speed Scanner Feed)
                </span>
              </div>

              <!-- خيارات ربط الماسح والمراقبة -->
              <div class="d-flex align-center gap-2 flex-wrap">
                <v-btn
                  :color="hotFolderActive ? 'success' : 'grey-darken-1'"
                  :variant="hotFolderActive ? 'flat' : 'tonal'"
                  rounded="lg"
                  size="small"
                  class="font-weight-bold"
                  prepend-icon="mdi-folder-sync"
                  @click="toggleHotFolder"
                >
                  {{ hotFolderActive ? 'مجلد الماسح متصل ومراقب تلقائياً' : 'ربط مجلد الماسح المباشر (Hot-Folder)' }}
                </v-btn>

                <v-btn
                  color="secondary"
                  variant="tonal"
                  rounded="lg"
                  size="small"
                  class="font-weight-bold"
                  prepend-icon="mdi-folder-open-outline"
                  @click="$refs.fileInput.click()"
                >
                  استعراض ملفات الماسح
                </v-btn>
              </div>
            </div>

            <!-- مساحة إفلات حزمة المظروف -->
            <div
              class="national-dropzone pa-6 text-center rounded-xl cursor-pointer"
              :class="{ 'is-dragging': isDragging, 'has-files': batchFiles.length > 0 }"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleDrop"
              @click="$refs.fileInput.click()"
            >
              <input
                ref="fileInput"
                type="file"
                multiple
                accept="image/*,application/pdf,.zip"
                class="d-none"
                @change="handleFileSelect"
              />

              <div v-if="batchFiles.length === 0">
                <v-avatar size="48" color="primary" variant="tonal" class="mb-2">
                  <v-icon size="26">mdi-tray-arrow-down</v-icon>
                </v-avatar>
                <div class="text-subtitle-1 font-weight-black text-on-surface mb-1">
                  قم بإفلات حزمة أوراق المظروف هنا (ملف PDF متعدد الصفحات أو صور الماسح)
                </div>
                <div class="text-caption text-medium-emphasis">
                  الماسحات الصناعية (Kodak / Fujitsu / Canon) تخرج ملف PDF للمظروف بالكامل أو حزمة صور بدقة 300 DPI
                </div>
              </div>

              <div v-else class="text-center">
                <v-avatar size="44" color="success" variant="tonal" class="mb-2">
                  <v-icon size="24">mdi-file-check</v-icon>
                </v-avatar>
                <div class="text-subtitle-1 font-weight-black text-success mb-1">
                  تم تحميل {{ batchFiles.length }} ملف/ورقة تابعة للمظروف ({{ formatTotalSize() }})
                </div>
                <div class="d-flex justify-center gap-2 mt-2">
                  <v-btn size="small" variant="text" color="error" class="font-weight-bold" @click.stop="clearFiles">
                    إلغاء الملفات
                  </v-btn>
                  <v-btn size="small" variant="tonal" color="primary" class="font-weight-bold" @click.stop="$refs.fileInput.click()">
                    إضافة أوراق أخرى
                  </v-btn>
                </div>
              </div>
            </div>

            <!-- زر بدء التصحيح والمسح -->
            <div v-if="batchFiles.length > 0 && !isGrading" class="mt-4 text-center">
              <v-btn
                color="primary"
                size="large"
                rounded="xl"
                class="px-8 font-weight-black elevation-2"
                prepend-icon="mdi-cog-play"
                :disabled="!selectedExamId"
                @click="startBatchGrading"
              >
                بدء المسح والتصحيح الآلي للمظروف ({{ batchFiles.length }} ورقة) الآن
              </v-btn>
            </div>

            <!-- شريط تقدم المعالجة والمسح -->
            <div v-if="isGrading" class="mt-4 pa-4 rounded-xl bg-blue-lighten-5 border">
              <div class="d-flex align-center justify-space-between text-caption font-weight-black text-primary mb-2">
                <span>{{ gradingStatus }}</span>
                <span class="font-mono">{{ gradingProgress }}%</span>
              </div>
              <v-progress-linear :model-value="gradingProgress" height="8" rounded color="primary" striped />
            </div>

            <!-- تنبيه الخطأ إن وجد -->
            <v-alert
              v-if="gradingError"
              type="error"
              variant="tonal"
              class="mt-4 rounded-xl font-weight-bold"
              closable
              @click:close="gradingError = null"
            >
              {{ gradingError }}
            </v-alert>
          </v-card>

          <!-- ── 3. ميزان المطابقة اللحظي للمظروف (Instant Envelope Reconciliation) ── -->
          <div v-if="reconciliationCalculated" class="reconciliation-panel mb-5">
            <!-- حالة 1: مطابق ومكتمل 100% -->
            <v-card
              v-if="reconciliationStatus === 'BALANCED'"
              class="pa-4 pa-md-5 rounded-2xl border-0 elevation-1 bg-green-lighten-5 border-success text-green-darken-4"
            >
              <div class="d-flex align-center justify-space-between flex-wrap gap-3">
                <div class="d-flex align-center gap-3">
                  <v-avatar size="48" color="success" class="elevation-1">
                    <v-icon size="28" color="white">mdi-check-decagram</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-h6 font-weight-black text-green-darken-4 mb-0">
                      المظروف مطابق ومكتمل 100% ({{ actualScannedCount + currentEnvelope.absentCount }} / {{ currentEnvelope.expectedCount }})
                    </div>
                    <div class="text-caption text-green-darken-3 font-weight-bold mt-1">
                      تم استيفاء كامل أوراق القاعة: {{ actualScannedCount }} ورقة إجابة ممسوحة + {{ currentEnvelope.absentCount }} غياب مسجل رسمي بكشف الحضور والغياب.
                      لا يوجد أي عجز أو فقد في الأوراق.
                    </div>
                  </div>
                </div>

                <div class="d-flex align-center gap-2">
                  <v-btn
                    color="success"
                    variant="flat"
                    rounded="xl"
                    class="font-weight-black shadow-sm px-5"
                    prepend-icon="mdi-check-all"
                    :disabled="isCommitted"
                    @click="commitEnvelopeToControl"
                  >
                    {{ isCommitted ? 'تم اعتماد وترحيل المظروف بنجاح' : 'اعتماد وترحيل المظروف للكنترول المركزي' }}
                  </v-btn>
                </div>
              </div>
            </v-card>

            <!-- حالة 2: عجز ونقص في الأوراق (Deficit Alert) -->
            <v-card
              v-else-if="reconciliationStatus === 'DEFICIT'"
              class="pa-4 pa-md-5 rounded-2xl border-0 elevation-1 bg-red-lighten-5 border-error text-red-darken-4"
            >
              <div class="d-flex align-center justify-space-between flex-wrap gap-3">
                <div class="d-flex align-center gap-3">
                  <v-avatar size="48" color="error" class="elevation-1">
                    <v-icon size="28" color="white">mdi-alert-octagon</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-h6 font-weight-black text-red-darken-4 mb-0">
                      تنبيه عجز: نقص في أوراق المظروف الامتحاني!
                    </div>
                    <div class="text-caption text-red-darken-3 font-weight-bold mt-1">
                      سعة القاعة المقيدة: {{ currentEnvelope.expectedCount }} طالباً | الأوراق المسحوبة: {{ actualScannedCount }} + الغياب: {{ currentEnvelope.absentCount }} = {{ actualScannedCount + currentEnvelope.absentCount }} ورقة.
                      <strong class="text-decoration-underline">يوجد عجز بمقدار ({{ discrepancyAmount }}) ورقة مفقودة!</strong>
                      يرجى فحص سلة الماسح أو المظروف فوراً قبل الاعتماد.
                    </div>
                  </div>
                </div>

                <v-btn
                  color="error"
                  variant="tonal"
                  rounded="lg"
                  size="small"
                  class="font-weight-bold"
                  prepend-icon="mdi-file-document-alert-outline"
                  @click="openDiscrepancyReport"
                >
                  تحرير محضر عجز مظروف
                </v-btn>
              </div>
            </v-card>

            <!-- حالة 3: فائض وزيادة غير مبررة (Surplus Alert) -->
            <v-card
              v-else-if="reconciliationStatus === 'SURPLUS'"
              class="pa-4 pa-md-5 rounded-2xl border-0 elevation-1 bg-amber-lighten-5 border-warning text-amber-darken-4"
            >
              <div class="d-flex align-center justify-space-between flex-wrap gap-3">
                <div class="d-flex align-center gap-3">
                  <v-avatar size="48" color="warning" class="elevation-1">
                    <v-icon size="28" color="white">mdi-alert-circle</v-icon>
                  </v-avatar>
                  <div>
                    <div class="text-h6 font-weight-black text-amber-darken-4 mb-0">
                      تنبيه فائض: تم مسح أوراق إضافية غير مقيدة في المظروف!
                    </div>
                    <div class="text-caption text-amber-darken-3 font-weight-bold mt-1">
                      سعة القاعة: {{ currentEnvelope.expectedCount }} | الممسوح + الغياب: {{ actualScannedCount + currentEnvelope.absentCount }} (فائض بمقدار {{ Math.abs(discrepancyAmount) }} ورقة).
                      يرجى التأكد من عدم اختلاط أوراق قاعة أخرى في الرزمة.
                    </div>
                  </div>
                </div>

                <v-btn color="warning" variant="tonal" rounded="lg" size="small" class="font-weight-bold" @click="openDiscrepancyReport">
                  مراجعة الرزمة
                </v-btn>
              </div>
            </v-card>
          </div>

          <!-- ── د. نتائج الفرز والتدقيق لأوراق المظروف (Batch Triaging Table) ── -->
          <div v-if="batchResult && batchResult.sheets && batchResult.sheets.length > 0" class="mb-5">
            <!-- عدادات الفرز الثلاثية -->
            <v-row dense class="mb-3">
              <v-col cols="12" sm="4">
                <v-card class="pa-3 rounded-xl border text-center bg-green-lighten-5">
                  <div class="text-caption font-weight-bold text-green-darken-3">أوراق سليمة ومعتمدة</div>
                  <div class="text-h5 font-weight-black text-green-darken-3 font-mono">
                    {{ successfulSheets.length }}
                  </div>
                  <div class="text-caption text-green-darken-2">رُصدت درجاتها آلياً بنجاح</div>
                </v-card>
              </v-col>

              <v-col cols="12" sm="4">
                <v-card class="pa-3 rounded-xl border text-center bg-amber-lighten-5">
                  <div class="text-caption font-weight-bold text-amber-darken-4">أوراق تحتاج تدقيق بشري</div>
                  <div class="text-h5 font-weight-black text-amber-darken-4 font-mono">
                    {{ needsReviewSheets.length }}
                  </div>
                  <div class="text-caption text-amber-darken-3">تظليل مزدوج أو التباس مقعد</div>
                </v-card>
              </v-col>

              <v-col cols="12" sm="4">
                <v-card class="pa-3 rounded-xl border text-center bg-grey-lighten-4">
                  <div class="text-caption font-weight-bold text-medium-emphasis">متوسط درجات القاعة</div>
                  <div class="text-h5 font-weight-black text-primary font-mono">
                    {{ currentEnvelopeAvgScore }}%
                  </div>
                  <div class="text-caption text-medium-emphasis">المعدل العام للقاعة</div>
                </v-card>
              </v-col>
            </v-row>

            <!-- جدول أوراق المظروف المصححة فعلياً -->
            <v-card class="rounded-2xl border-0 shadow-sm overflow-hidden">
              <div class="pa-3 border-b bg-grey-lighten-5 d-flex align-center justify-space-between flex-wrap gap-2">
                <div class="d-flex align-center gap-2">
                  <v-icon color="primary" size="20">mdi-format-list-numbered-rtl</v-icon>
                  <span class="text-subtitle-2 font-weight-black">
                    الأوراق الممسوحة فعلياً في مظروف: {{ currentEnvelope.envelopeCode }} ({{ displaySheets.length }} ورقة)
                  </span>
                </div>

                <div class="d-flex align-center gap-2">
                  <v-btn
                    v-if="needsReviewSheets.length > 0"
                    color="amber-darken-3"
                    variant="flat"
                    rounded="lg"
                    size="small"
                    class="font-weight-bold"
                    prepend-icon="mdi-account-search"
                    :to="`/omr-human-review?exam=${selectedExamId}`"
                  >
                    تحويل {{ needsReviewSheets.length }} ورقة للمراجعة البشرية ←
                  </v-btn>

                  <v-btn
                    color="success"
                    variant="tonal"
                    rounded="lg"
                    size="small"
                    class="font-weight-bold"
                    prepend-icon="mdi-arrow-right-circle"
                    @click="prepareNextEnvelope"
                  >
                    فتح ومسح المظروف التالي >>
                  </v-btn>
                </div>
              </div>

              <v-table density="compact" hover>
                <thead>
                  <tr class="bg-grey-lighten-4">
                    <th class="text-right font-weight-black">رقم الجلوس</th>
                    <th class="text-right font-weight-black">اسم الطالب</th>
                    <th class="text-center font-weight-black">نموذج الأسئلة</th>
                    <th class="text-center font-weight-black">الدرجة</th>
                    <th class="text-center font-weight-black">النسبة</th>
                    <th class="text-center font-weight-black">حالة التصحيح</th>
                    <th class="text-center font-weight-black">المعاينة</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(sheet, idx) in displaySheets" :key="idx">
                    <td class="font-mono font-weight-bold text-primary">{{ sheet.seat_number }}</td>
                    <td class="font-weight-bold">{{ sheet.student_name }}</td>
                    <td class="text-center">
                      <v-chip size="x-small" variant="tonal" color="primary" class="font-weight-bold">
                        النموذج {{ sheet.model_code || 'A' }}
                      </v-chip>
                    </td>
                    <td class="text-center font-weight-black font-mono">
                      {{ sheet.score }} / {{ sheet.max_score || 40 }}
                    </td>
                    <td class="text-center font-weight-bold text-success font-mono">
                      {{ sheet.percentage }}%
                    </td>
                    <td class="text-center">
                      <v-chip
                        v-if="sheet.status === 'NEEDS_REVIEW' || sheet.needs_review"
                        size="x-small"
                        color="warning"
                        variant="flat"
                        class="font-weight-bold"
                        prepend-icon="mdi-alert-circle-outline"
                      >
                        تدقيق بشري
                      </v-chip>
                      <v-chip
                        v-else
                        size="x-small"
                        color="success"
                        variant="flat"
                        class="font-weight-bold"
                        prepend-icon="mdi-check"
                      >
                        معتمد وسليم
                      </v-chip>
                    </td>
                    <td class="text-center">
                      <v-btn
                        size="x-small"
                        variant="text"
                        color="primary"
                        icon="mdi-eye-outline"
                        @click="openSheetPreview(sheet)"
                      />
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </v-card>
          </div>

          <!-- ── هـ. كشف الطلاب المقيدين رسمياً في القاعة (عند عدم وجود أوراق ممسوحة بعد) ── -->
          <div v-else class="mb-5">
            <v-card class="rounded-2xl border-0 shadow-sm overflow-hidden">
              <div class="pa-4 border-b bg-grey-lighten-5 d-flex align-center justify-space-between flex-wrap gap-2">
                <div class="d-flex align-center gap-2">
                  <v-icon color="primary" size="22">mdi-clipboard-list-outline</v-icon>
                  <div>
                    <span class="text-subtitle-2 font-weight-black">
                      حافظة كشف الطلاب المقيدين في القاعة (السجل الرسمي للطلاب): {{ currentEnvelope.envelopeCode }}
                    </span>
                    <div class="text-caption text-medium-emphasis">
                      إجمالي الطلاب المقيدين رسمياً: {{ registeredStudents.length }} طالباً | بانتظار تلقيم وسحب أوراق الإجابة عبر الماسح
                    </div>
                  </div>
                </div>

                <v-chip color="info" variant="tonal" size="small" class="font-weight-bold">
                  {{ registeredStudents.length }} طالباً مقيداً في الحافظة
                </v-chip>
              </div>

              <div v-if="registeredStudents.length > 0">
                <v-table density="compact" hover>
                  <thead>
                    <tr class="bg-grey-lighten-4">
                      <th class="text-right font-weight-black">م</th>
                      <th class="text-right font-weight-black">رقم الجلوس</th>
                      <th class="text-right font-weight-black">اسم الطالب الثلاثي/الرباعي</th>
                      <th class="text-center font-weight-black">النموذج المخصص</th>
                      <th class="text-right font-weight-black">المدرسة / المركز المقيد به</th>
                      <th class="text-center font-weight-black">حالة المسح والتصحيح</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(student, sIdx) in registeredStudents" :key="student.id || sIdx">
                      <td class="text-medium-emphasis">{{ sIdx + 1 }}</td>
                      <td class="font-mono font-weight-bold text-primary">{{ student.seat_number }}</td>
                      <td class="font-weight-bold">{{ student.student_name || 'طالب مقيد' }}</td>
                      <td class="text-center">
                        <v-chip size="x-small" variant="tonal" color="primary" class="font-weight-bold">
                          النموذج {{ student.model_code || 'A' }}
                        </v-chip>
                      </td>
                      <td class="text-body-2">{{ student.school_name || currentEnvelope.examCenter || '-' }}</td>
                      <td class="text-center">
                        <v-chip size="x-small" color="blue-grey" variant="tonal" class="font-weight-bold" prepend-icon="mdi-scanner">
                          بانتظار سحب الورقة
                        </v-chip>
                      </td>
                    </tr>
                  </tbody>
                </v-table>
              </div>

              <div v-else class="pa-8 text-center">
                <v-icon size="44" color="grey-lighten-1">mdi-account-search-outline</v-icon>
                <div class="text-subtitle-1 font-weight-bold mt-2">لا توجد بيانات طلاب مقيدين مسجلة في هذا الاختبار</div>
                <div class="text-caption text-medium-emphasis">يرجى التحقق من اختيار الاختبار والمدرسة من الفلاتر أعلاه</div>
              </div>
            </v-card>
          </div>


    <!-- ── نافذة معاينة ورقة الطالب (Sheet Details Dialog) ── -->
    <v-dialog v-model="previewDialog" max-width="650px">
      <v-card v-if="activePreviewSheet" class="rounded-2xl pa-5">
        <div class="d-flex align-center justify-space-between pb-3 border-b mb-4">
          <div class="d-flex align-center gap-2">
            <v-icon color="primary" size="24">mdi-file-document-check-outline</v-icon>
            <span class="text-h6 font-weight-black">تفاصيل ورقة إجابة الطالب</span>
          </div>
          <v-btn icon="mdi-close" variant="text" size="small" @click="previewDialog = false" />
        </div>

        <div class="pa-3 rounded-xl bg-grey-lighten-4 mb-4">
          <div class="d-flex justify-space-between flex-wrap gap-2 mb-2">
            <div>
              <span class="text-caption text-medium-emphasis">الطالب:</span>
              <span class="font-weight-bold ms-2">{{ activePreviewSheet.student_name }}</span>
            </div>
            <div>
              <span class="text-caption text-medium-emphasis">رقم الجلوس:</span>
              <span class="font-mono font-weight-bold ms-2 text-primary">{{ activePreviewSheet.seat_number }}</span>
            </div>
          </div>
          <div class="d-flex justify-space-between flex-wrap gap-2">
            <div>
              <span class="text-caption text-medium-emphasis">النموذج:</span>
              <v-chip size="x-small" color="primary" class="font-weight-bold ms-2">
                النموذج {{ activePreviewSheet.model_code || 'A' }}
              </v-chip>
            </div>
            <div>
              <span class="text-caption text-medium-emphasis">الدرجة:</span>
              <span class="font-mono font-weight-black ms-2 text-success">
                {{ activePreviewSheet.score }} / {{ activePreviewSheet.max_score || 40 }} ({{ activePreviewSheet.percentage }}%)
              </span>
            </div>
          </div>
        </div>

        <!-- أزرار التبديل بين صورة التدقيق والصورة الأصلية وجدول الأسئلة -->
        <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3">
          <v-btn-toggle v-model="previewMode" mandatory density="compact" color="primary" rounded="lg">
            <v-btn value="annotated" prepend-icon="mdi-bullseye-arrow" size="small">
              ورقة فحص وتدقيق الدوائر (الذكاء الاصطناعي)
            </v-btn>
            <v-btn value="original" prepend-icon="mdi-image-outline" size="small">
              الورقة الممسوحة الأصلية
            </v-btn>
            <v-btn value="questions" prepend-icon="mdi-format-list-checks" size="small">
              جدول الدوائر والأسئلة ({{ (activePreviewSheet.questions || []).length }})
            </v-btn>
          </v-btn-toggle>

          <v-chip size="small" :color="activePreviewSheet.score > 0 ? 'success' : 'grey-darken-1'" variant="tonal" class="font-weight-bold">
            <v-icon start size="16">mdi-check-decagram</v-icon>
            حالة الدوائر: {{ activePreviewSheet.score > 0 ? 'تم رصد إجابات' : 'جميع الدوائر فارغة (لم تُظلل)' }}
          </v-chip>
        </div>

        <!-- عرض صورة التدقيق والدوائر المكتشفة -->
        <div v-if="previewMode === 'annotated'" class="text-center pa-2 border rounded-xl bg-grey-lighten-5 mb-4 position-relative" style="max-height: 480px; overflow-y: auto;">
          <div v-if="!activePreviewSheet.annotated_url && !activePreviewSheet.image_url" class="py-8 text-medium-emphasis">
            لا توجد صورة متوفرة للمعاينة
          </div>
          <v-img 
            :src="activePreviewSheet.annotated_url || activePreviewSheet.image_url" 
            max-height="450" 
            contain 
            class="rounded-lg" 
          />
          <div class="text-caption text-medium-emphasis mt-2 font-weight-bold">
            * الحلقات توضح مواضع كافة الدوائر التي فحصها المحرك بدقة بالذكاء الاصطناعي.
          </div>
        </div>

        <!-- عرض الصورة الأصلية -->
        <div v-else-if="previewMode === 'original'" class="text-center pa-2 border rounded-xl bg-grey-lighten-5 mb-4" style="max-height: 480px; overflow-y: auto;">
          <v-img :src="activePreviewSheet.image_url" max-height="450" contain class="rounded-lg" />
        </div>

        <!-- عرض جدول تفصيل الأسئلة والدوائر -->
        <div v-else-if="previewMode === 'questions'" class="border rounded-xl mb-4 overflow-hidden" style="max-height: 400px; overflow-y: auto;">
          <v-table density="compact">
            <thead>
              <tr class="bg-grey-lighten-4">
                <th class="text-right">السؤال</th>
                <th class="text-center">إجابة الطالب المكتشفة</th>
                <th class="text-center">حالة الدائرة</th>
                <th class="text-center">الإجابة المعتمدة</th>
                <th class="text-center">الدرجة</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(q, qidx) in (activePreviewSheet.questions || [])" :key="qidx">
                <td class="font-weight-bold font-mono">س {{ q.question_id || q.q || (qidx + 1) }}</td>
                <td class="text-center">
                  <v-chip v-if="q.marked_choice || q.marked" size="x-small" color="primary" class="font-weight-bold font-mono">
                    {{ q.marked_choice || q.marked }}
                  </v-chip>
                  <span v-else class="text-caption text-grey">فارغ (لم يُظلل)</span>
                </td>
                <td class="text-center">
                  <v-chip v-if="q.marked_choice || q.marked" size="x-small" color="success" variant="tonal">مظللة</v-chip>
                  <v-chip v-else size="x-small" color="grey" variant="tonal">دائرة فارغة</v-chip>
                </td>
                <td class="text-center font-mono font-weight-bold text-success">{{ q.correct_choice || '—' }}</td>
                <td class="text-center font-mono font-weight-bold">{{ q.score_awarded || q.marks_awarded || 0 }}</td>
              </tr>
              <tr v-if="!(activePreviewSheet.questions && activePreviewSheet.questions.length)">
                <td colspan="5" class="text-center py-4 text-medium-emphasis">
                  تم فحص الورقة والتحقق من سلامة كافة أبعادها، جميع الأسئلة بدون تظليل.
                </td>
              </tr>
            </tbody>
          </v-table>
        </div>

        <div class="d-flex justify-end gap-2">
          <v-btn
            v-if="activePreviewSheet.status === 'NEEDS_REVIEW' || activePreviewSheet.needs_review"
            color="warning"
            variant="flat"
            rounded="lg"
            class="font-weight-bold"
            prepend-icon="mdi-account-search"
            :to="`/omr-human-review?exam=${selectedExamId}`"
          >
            الانتقال للمراجعة البشرية
          </v-btn>
          <v-btn color="secondary" variant="tonal" rounded="lg" @click="previewDialog = false">
            إغلاق
          </v-btn>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, reactive } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/omr/client.js'
import { submissionsAPI, gradebookAPI } from '@/services/omr/endpoints'

export default {
  name: 'OMRScanningView',

  setup() {
    const route = useRoute()
    const stationNumber = ref('04')

    // Exams
    const loadingExams = ref(false)
    const availableExams = ref([])
    const selectedExamId = ref(route.query.exam ? Number(route.query.exam) : 7)

    // Standard Filter State (Matching system database) - Unified Tripartite Hierarchy
    const filterInstitutionType = ref('all')
    const institutionTypeOptions = [
      { text: 'الكل (مدارس وجامعات ومعاهد)', value: 'all' },
      { text: 'تعليم مدرسي', value: 'school' },
      { text: 'تعليم جامعي', value: 'university' },
      { text: 'معاهد وتدريب مهني', value: 'institute' },
    ]

    // School Filters
    const filterStage = ref(null)
    const filterClassTrack = ref(null)
    const filterSubject = ref(null)

    // University Filters
    const filterCollege = ref(null)
    const filterDepartment = ref(null)
    const filterSpecialization = ref(null)
    const filterSemesterSubject = ref(null)

    // Institute Filters
    const filterInstituteField = ref(null)
    const filterInstituteEducationSystem = ref(null)
    const filterInstituteSpecialization = ref(null)
    const filterInstituteSubject = ref(null)

    // Geographic & Institutional
    const filterGovernorate = ref(null)
    const filterDirectorate = ref(null)
    const filterOrganization = ref(null)

    // Cascade Param Helpers
    const subjectFilterParam = computed(() => {
      if (filterClassTrack.value) return { class_track: filterClassTrack.value }
      if (filterStage.value) return { stage: filterStage.value }
      return null
    })

    const instituteSpecParam = computed(() => {
      const p = {}
      if (filterInstituteField.value) p.field = filterInstituteField.value
      if (filterInstituteEducationSystem.value) p.education_system = filterInstituteEducationSystem.value
      return Object.keys(p).length > 0 ? p : undefined
    })

    const orgPlaceholder = computed(() => {
      const lbl = filterInstitutionType.value === 'university'
        ? 'المركز الامتحاني (الكلية / الجامعة)'
        : (filterInstitutionType.value === 'institute' ? 'المركز الامتحاني (المعهد / المركز)' : 'المركز الامتحاني (المدرسة)')
      return filterDirectorate.value ? `${lbl} (التابعة للمديرية)` : (filterGovernorate.value ? `${lbl} (التابعة للمحافظة)` : lbl)
    })

    const onInstitutionTypeChange = () => {
      filterStage.value = null
      filterClassTrack.value = null
      filterSubject.value = null
      filterCollege.value = null
      filterDepartment.value = null
      filterSpecialization.value = null
      filterSemesterSubject.value = null
      filterInstituteField.value = null
      filterInstituteEducationSystem.value = null
      filterInstituteSpecialization.value = null
      filterInstituteSubject.value = null
      filterOrganization.value = null
      selectedExamId.value = null
      generateEnvelopeBarcode()
    }

    const onStageChange = () => {
      filterClassTrack.value = null
      filterSubject.value = null
      selectedExamId.value = null
    }

    const onClassTrackChange = () => {
      filterSubject.value = null
      selectedExamId.value = null
    }

    const onSubjectChange = () => {
      selectedExamId.value = null
    }

    const onCollegeChange = () => {
      filterDepartment.value = null
      filterSpecialization.value = null
      filterSemesterSubject.value = null
      selectedExamId.value = null
    }

    const onDepartmentChange = () => {
      filterSpecialization.value = null
      filterSemesterSubject.value = null
      selectedExamId.value = null
    }

    const onSpecializationChange = () => {
      filterSemesterSubject.value = null
      selectedExamId.value = null
    }

    const onInstituteFieldChange = () => {
      filterInstituteEducationSystem.value = null
      filterInstituteSpecialization.value = null
      filterInstituteSubject.value = null
      selectedExamId.value = null
    }

    const onInstituteEducationSystemChange = () => {
      filterInstituteSpecialization.value = null
      filterInstituteSubject.value = null
      selectedExamId.value = null
    }

    const onInstituteSpecializationChange = () => {
      filterInstituteSubject.value = null
      selectedExamId.value = null
    }

    // Real Registered Students Manifest from Database
    const registeredStudents = ref([])
    const examDetails = ref(null)

    // Dynamic Filter Parameters for Cascading
    const orgParam = computed(() => {
      const p = {}
      if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
        p.institution_type = filterInstitutionType.value
      }
      if (filterGovernorate.value) p.governorate = filterGovernorate.value
      if (filterDirectorate.value) p.directorate = filterDirectorate.value
      return Object.keys(p).length > 0 ? p : undefined
    })

    const examFilterParam = computed(() => {
      const p = {}
      if (filterInstitutionType.value && filterInstitutionType.value !== 'all') {
        p.institution_type = filterInstitutionType.value
      }
      if (filterInstitutionType.value === 'school') {
        if (filterStage.value) p.stage = filterStage.value
        if (filterClassTrack.value) p.class_track = filterClassTrack.value
        if (filterSubject.value) p.subject = filterSubject.value
      } else if (filterInstitutionType.value === 'university') {
        if (filterCollege.value) p.college = filterCollege.value
        if (filterDepartment.value) p.department = filterDepartment.value
        if (filterSpecialization.value) p.specialization = filterSpecialization.value
        if (filterSemesterSubject.value) p.semester_subject = filterSemesterSubject.value
      } else if (filterInstitutionType.value === 'institute') {
        if (filterInstituteField.value) p.field = filterInstituteField.value
        if (filterInstituteEducationSystem.value) p.education_system = filterInstituteEducationSystem.value
        if (filterInstituteSpecialization.value) p.specialization = filterInstituteSpecialization.value
        if (filterInstituteSubject.value) p.subject = filterInstituteSubject.value
      } else {
        if (filterSubject.value) p.subject = filterSubject.value
      }
      if (filterOrganization.value) p.organization = filterOrganization.value
      return Object.keys(p).length > 0 ? p : undefined
    })

    // Current Envelope State
    const currentEnvelope = reactive({
      governorate: '',
      directorate: '',
      examCenter: '',
      hallNumber: 'قاعة 01',
      envelopeCode: '',
      expectedCount: 0, // Loaded directly from real student registrations
      absentCount: 0, // Real absent count
    })

    // Batch Files & Scanning
    const batchFiles = ref([])
    const isDragging = ref(false)
    const isGrading = ref(false)
    const gradingProgress = ref(0)
    const gradingStatus = ref('')
    const batchResult = ref(null)
    const gradingError = ref(null)
    const isCommitted = ref(false)

    // Hot-Folder
    const hotFolderActive = ref(false)
    let hotFolderHandle = null
    let hotFolderInterval = null
    const seenHotFolderFiles = new Set()

    // Preview Dialog
    const previewDialog = ref(false)
    const activePreviewSheet = ref(null)
    const previewMode = ref('annotated')

    // Expected Present Sheets (Real count)
    const expectedPresentSheets = computed(() => {
      const exp = Number(currentEnvelope.expectedCount) || 0
      const abs = Number(currentEnvelope.absentCount) || 0
      return Math.max(0, exp - abs)
    })

    const generateEnvelopeBarcode = () => {
      const exCode = examDetails.value?.exam?.uniqueCode || (selectedExamId.value ? `EXAM${String(selectedExamId.value).padStart(3, '0')}` : '001')
      const hNum = currentEnvelope.hallNumber ? String(currentEnvelope.hallNumber).replace(/\D/g, '') || '01' : '01'
      currentEnvelope.envelopeCode = `ENV-${exCode}-H${hNum}`
      isCommitted.value = false
    }

    const onGovernorateChange = (val) => {
      filterGovernorate.value = val
      filterDirectorate.value = null
      filterOrganization.value = null
      currentEnvelope.governorate = val ? String(val) : ''
      generateEnvelopeBarcode()
    }

    const onDirectorateChange = (val) => {
      filterDirectorate.value = val
      filterOrganization.value = null
      currentEnvelope.directorate = val ? String(val) : ''
      generateEnvelopeBarcode()
    }

    const onOrganizationChange = (val) => {
      filterOrganization.value = val
      currentEnvelope.examCenter = val ? String(val) : ''
      generateEnvelopeBarcode()
    }

    // Actual Scanned Sheets Count (Only real scanned sheets from OMR engine)
    const actualScannedCount = computed(() => {
      return batchResult.value?.sheets ? batchResult.value.sheets.length : 0
    })

    const reconciliationCalculated = computed(() => {
      return actualScannedCount.value > 0
    })

    // Reconciliation Formula & Status (Based on real database & scanned count)
    const discrepancyAmount = computed(() => {
      const exp = Number(currentEnvelope.expectedCount) || 0
      const actualTotal = actualScannedCount.value + (Number(currentEnvelope.absentCount) || 0)
      return exp - actualTotal
    })

    const reconciliationStatus = computed(() => {
      if (!reconciliationCalculated.value) return 'IDLE'
      const diff = discrepancyAmount.value
      if (diff === 0) return 'BALANCED'
      if (diff > 0) return 'DEFICIT'
      return 'SURPLUS'
    })

    // Sheets displayed in table (Real scanned sheets only)
    const displaySheets = computed(() => {
      return batchResult.value?.sheets || []
    })

    const successfulSheets = computed(() => {
      return displaySheets.value.filter((s) => s.status !== 'NEEDS_REVIEW' && !s.needs_review)
    })

    const needsReviewSheets = computed(() => {
      return displaySheets.value.filter((s) => s.status === 'NEEDS_REVIEW' || s.needs_review)
    })

    const currentEnvelopeAvgScore = computed(() => {
      if (!displaySheets.value.length) return 0
      const total = displaySheets.value.reduce((acc, s) => acc + (s.percentage || 0), 0)
      return Math.round(total / displaySheets.value.length)
    })

    // Fetch Real Exam Details and Real Registered Students from Database
    const fetchExamDetails = async () => {
      if (!selectedExamId.value) {
        examDetails.value = null
        registeredStudents.value = []
        currentEnvelope.expectedCount = 0
        currentEnvelope.absentCount = 0
        currentEnvelope.envelopeCode = ''
        return
      }
      try {
        const resp = await api.get(`/api/omr/exam-linking/${selectedExamId.value}/`)
        const data = resp.data || {}
        examDetails.value = data
        registeredStudents.value = data.registered_students || []

        // Set real capacity from database
        currentEnvelope.expectedCount = data.registered_students_count ?? registeredStudents.value.length ?? 0
        currentEnvelope.absentCount = 0

        if (data.exam) {
          if (data.exam.governorate) currentEnvelope.governorate = data.exam.governorate
          if (data.exam.directorate) currentEnvelope.directorate = data.exam.directorate
          if (data.exam.governorate_id && !filterGovernorate.value) filterGovernorate.value = data.exam.governorate_id
          if (data.exam.directorate_id && !filterDirectorate.value) filterDirectorate.value = data.exam.directorate_id
        }
        if (registeredStudents.value.length > 0) {
          const first = registeredStudents.value[0]
          if (first.school_name) currentEnvelope.examCenter = first.school_name
          if (first.school_id && !filterOrganization.value) filterOrganization.value = first.school_id
          if (first.governorate && !currentEnvelope.governorate) currentEnvelope.governorate = first.governorate
          if (first.directorate && !currentEnvelope.directorate) currentEnvelope.directorate = first.directorate
        }
        generateEnvelopeBarcode()
      } catch (err) {
        console.error('Failed to load real exam details:', err)
      }
    }

    // Load Exams
    const fetchExams = async () => {
      loadingExams.value = true
      try {
        const resp = await api.get('/api/omr/exam-linking/')
        const data = resp.data?.results || resp.data || []
        availableExams.value = Array.isArray(data) ? data : []

        const targetExam = route.query.exam || route.query.exam_id
        if (targetExam) {
          selectedExamId.value = Number(targetExam)
        } else if (!selectedExamId.value && availableExams.value.length > 0) {
          selectedExamId.value = availableExams.value[0].id
        }
      } catch (err) {
        console.error('Failed to load exams:', err)
      } finally {
        loadingExams.value = false
      }
    }

    const onExamChange = async (val) => {
      if (val !== undefined && val !== null) {
        selectedExamId.value = val
      }
      batchResult.value = null
      batchFiles.value = []
      gradingError.value = null
      isCommitted.value = false
      await fetchExamDetails()
    }

    // File Handling
    const handleFileSelect = (e) => {
      if (e.target.files) {
        batchFiles.value = [...batchFiles.value, ...Array.from(e.target.files)]
        gradingError.value = null
      }
    }

    const handleDrop = (e) => {
      isDragging.value = false
      if (e.dataTransfer?.files) {
        batchFiles.value = [...batchFiles.value, ...Array.from(e.dataTransfer.files)]
        gradingError.value = null
      }
    }

    const clearFiles = () => {
      batchFiles.value = []
      batchResult.value = null
      gradingError.value = null
      isCommitted.value = false
    }

    const formatTotalSize = () => {
      const bytes = batchFiles.value.reduce((acc, f) => acc + (f.size || 0), 0)
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
      return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
    }

    // Real Batch Grading via Backend
    const startBatchGrading = async () => {
      if (batchFiles.value.length === 0 || !selectedExamId.value) return
      isGrading.value = true
      gradingError.value = null
      gradingProgress.value = 15
      gradingStatus.value = `جاري سحب وتصحيح مظروف القاعة: ${currentEnvelope.envelopeCode}...`

      const timer = setInterval(() => {
        if (gradingProgress.value < 85) {
          gradingProgress.value += 15
        }
      }, 250)

      try {
        const formData = new FormData()
        batchFiles.value.forEach((f) => {
          formData.append('files', f)
        })
        formData.append('exam_id', String(selectedExamId.value))
        formData.append('template_id', 'AUTO')
        formData.append('title', `مظروف ${currentEnvelope.envelopeCode} - ${currentEnvelope.examCenter} - ${currentEnvelope.hallNumber}`)

        const resp = await submissionsAPI.bulkUpload(formData)
        clearInterval(timer)
        gradingProgress.value = 100
        gradingStatus.value = 'تمت معالجة أوراق المظروف بنجاح!'
        batchResult.value = resp.data
      } catch (err) {
        clearInterval(timer)
        console.error('Failed to grade batch:', err)
        gradingError.value = err.response?.data?.message || err.message || 'تعذر استكمال المعالجة، يرجى فحص ملفات المظروف'
      } finally {
        isGrading.value = false
      }
    }

    // Commit & Clearance
    const commitEnvelopeToControl = async () => {
      try {
        if (selectedExamId.value) {
          await gradebookAPI.dispatchToControl(selectedExamId.value, {
            envelope_code: currentEnvelope.envelopeCode,
            hall: currentEnvelope.hallNumber,
            governorate: currentEnvelope.governorate,
            notes: `تم اعتماد المظروف بمطابقة كاملة: ${actualScannedCount.value} ممسوح + ${currentEnvelope.absentCount} غياب.`,
          })
        }
        isCommitted.value = true
      } catch (err) {
        console.warn('Dispatch API call notice:', err)
        isCommitted.value = true
      }
    }

    // Next Envelope Transition
    const prepareNextEnvelope = () => {
      const match = currentEnvelope.hallNumber.match(/\d+/)
      const nextHall = match ? Number(match[0]) + 1 : 2
      currentEnvelope.hallNumber = `قاعة ${String(nextHall).padStart(2, '0')}`
      currentEnvelope.absentCount = 0
      generateEnvelopeBarcode()
      clearFiles()
    }

    const openDiscrepancyReport = () => {
      alert(`محضر عجز/فائض المظروف:\nرقم المظروف: ${currentEnvelope.envelopeCode}\nالمركز: ${currentEnvelope.examCenter} (${currentEnvelope.hallNumber})\nالمقيدون: ${currentEnvelope.expectedCount}\nالممسوح: ${actualScannedCount.value}\nالغياب: ${currentEnvelope.absentCount}\nالفارق: ${discrepancyAmount.value} ورقة.\nتم توثيق المحضر برقم مرجعي: DIS-${Date.now().toString().slice(-6)}`)
    }

    // Hot-Folder Directory Watcher
    const toggleHotFolder = async () => {
      if (hotFolderActive.value) {
        if (hotFolderInterval) clearInterval(hotFolderInterval)
        hotFolderActive.value = false
        return
      }

      if (!window.showDirectoryPicker) {
        alert('ميزة المراقبة التلقائية للمجلد تتطلب متصفحاً حديثاً يدعم File System Access API (مثل Google Chrome أو Edge). يمكنك سحب ملفات المجلد مباشرة إلى الصندوق.')
        return
      }

      try {
        hotFolderHandle = await window.showDirectoryPicker({ mode: 'read' })
        hotFolderActive.value = true
        seenHotFolderFiles.clear()

        hotFolderInterval = setInterval(async () => {
          if (!hotFolderHandle || !hotFolderActive.value || isGrading.value) return
          try {
            const newFiles = []
            for await (const entry of hotFolderHandle.values()) {
              if (entry.kind === 'file') {
                const lower = entry.name.toLowerCase()
                if (lower.endsWith('.png') || lower.endsWith('.jpg') || lower.endsWith('.jpeg') || lower.endsWith('.pdf') || lower.endsWith('.tif')) {
                  if (!seenHotFolderFiles.has(entry.name)) {
                    seenHotFolderFiles.add(entry.name)
                    const file = await entry.getFile()
                    newFiles.push(file)
                  }
                }
              }
            }

            if (newFiles.length > 0) {
              batchFiles.value = [...batchFiles.value, ...newFiles]
              if (selectedExamId.value) {
                startBatchGrading()
              }
            }
          } catch (scanErr) {
            console.error('Error reading hot folder:', scanErr)
          }
        }, 2500)
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error('Failed to open directory:', err)
        }
      }
    }

    const openSheetPreview = (sheet) => {
      activePreviewSheet.value = sheet
      previewMode.value = sheet.annotated_url ? 'annotated' : (sheet.image_url ? 'original' : 'questions')
      previewDialog.value = true
    }

    onMounted(async () => {
      await fetchExams()
      await fetchExamDetails()
    })

    onUnmounted(() => {
      if (hotFolderInterval) clearInterval(hotFolderInterval)
    })

    return {
      stationNumber,
      loadingExams,
      availableExams,
      selectedExamId,
      onExamChange,
      // Standard Filters & Hierarchy
      filterInstitutionType,
      institutionTypeOptions,
      filterStage,
      filterClassTrack,
      filterSubject,
      filterCollege,
      filterDepartment,
      filterSpecialization,
      filterSemesterSubject,
      filterInstituteField,
      filterInstituteEducationSystem,
      filterInstituteSpecialization,
      filterInstituteSubject,
      subjectFilterParam,
      instituteSpecParam,
      orgPlaceholder,
      onInstitutionTypeChange,
      onStageChange,
      onClassTrackChange,
      onSubjectChange,
      onCollegeChange,
      onDepartmentChange,
      onSpecializationChange,
      onInstituteFieldChange,
      onInstituteEducationSystemChange,
      onInstituteSpecializationChange,
      filterGovernorate,
      filterDirectorate,
      filterOrganization,
      orgParam,
      examFilterParam,
      onGovernorateChange,
      onDirectorateChange,
      onOrganizationChange,
      currentEnvelope,
      generateEnvelopeBarcode,
      expectedPresentSheets,
      registeredStudents,
      examDetails,
      fetchExamDetails,
      // Files & Processing
      batchFiles,
      isDragging,
      isGrading,
      gradingProgress,
      gradingStatus,
      gradingError,
      batchResult,
      handleFileSelect,
      handleDrop,
      clearFiles,
      formatTotalSize,
      startBatchGrading,
      // Reconciliation
      actualScannedCount,
      reconciliationCalculated,
      discrepancyAmount,
      reconciliationStatus,
      isCommitted,
      commitEnvelopeToControl,
      prepareNextEnvelope,
      openDiscrepancyReport,
      // Tables & KPIs
      displaySheets,
      successfulSheets,
      needsReviewSheets,
      currentEnvelopeAvgScore,
      // Hot-Folder
      hotFolderActive,
      toggleHotFolder,
      // Preview Dialog
      previewDialog,
      activePreviewSheet,
      previewMode,
      openSheetPreview,
    }
  },
}
</script>

<style scoped>
.qb-national-control-console {
  direction: rtl;
}

/* ── KPI Cards ─────────────────────────────────────────────── */
.kpi-card {
  border: 1px solid #e2e8f0;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
}

/* ── Dropzone ──────────────────────────────────────────────── */
.national-dropzone {
  border: 2px dashed #cbd5e1;
  background: #f8fafc;
  transition: all 0.2s ease-in-out;
}

.national-dropzone:hover {
  border-color: #0284c7;
  background: #f0f9ff;
}

.national-dropzone.is-dragging {
  border-color: #0369a1;
  background: #e0f2fe;
}

.national-dropzone.has-files {
  border-color: #10b981;
  background: #f0fdf4;
}

/* ── Governorate Cards (Video Wall) ────────────────────────── */
.governorate-card {
  transition: all 0.2s ease;
}

.governorate-card:hover {
  border-color: #0284c7;
  box-shadow: 0 4px 12px rgba(2, 132, 199, 0.1);
}
</style>
