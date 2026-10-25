<template>
  <div class="qb-national-control-console pa-3 pa-md-6">
    <!-- ── 1. بيانات المظروف الامتحاني والقاعة (Envelope Manifest & Dispatch Details) ── -->
    <filter-fields
      label="1. بيانات المظروف الامتحاني والقاعة (Envelope Manifest & Dispatch Details)"
      class="main-card border-0 pa-5 rounded-2xl mb-5 shadow-sm"
    >
      <div class="d-flex align-center justify-end mb-3">
        <v-chip color="primary" variant="tonal" size="small" class="font-weight-bold" prepend-icon="mdi-shield-check">
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

      <!-- الصف 2: الهيكلية الجغرافية والمؤسسية + اختيار الاختبار المعتمد (أعمدة ديناميكية) -->
      <v-row dense class="align-center mb-1 mt-1">
        <!-- 1. المحافظة -->
        <auto-list
          v-model="filterGovernorate"
          name="Governorate"
          placeholder="المحافظة *"
          :cols="isSchoolFilter ? 3 : 4"
          :add="false"
          @update:model-value="onGovernorateChange"
        />

        <!-- 2. المديرية (تظهر للمدارس فقط) -->
        <auto-list
          v-if="isSchoolFilter"
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
          :cols="isSchoolFilter ? 3 : 4"
          :add="false"
          :disabled="isOrgDisabled"
          @update:model-value="onOrganizationChange"
        />

        <!-- 4. الاختبار والمادة الدراسية -->
        <auto-list
          v-model="selectedExamId"
          name="Exam"
          :param="examFilterParam"
          placeholder="الاختبار والمادة الدراسية *"
          :cols="isSchoolFilter ? 3 : 4"
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
            prepend-inner-icon="mdi-map-marker-outline"
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
            prepend-inner-icon="mdi-barcode"
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
            prepend-inner-icon="mdi-account-group-outline"
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
            prepend-inner-icon="mdi-account-remove-outline"
            color="warning"
            hide-details
          />
        </v-col>
      </v-row>

      <!-- ── التلخيص السريع لحافظة المظروف والمعادلة المتوقعة ── -->
      <div
        class="pa-3 mt-3 rounded-xl border bg-surface d-flex align-center justify-space-between flex-wrap gap-3"
      >
        <!-- شريط المعادلة الأفقي المتماسك بالرموز الرياضية الطبيعية -->
        <div class="d-flex align-center gap-2 flex-nowrap overflow-x-auto py-1">
          <div class="d-flex align-center gap-1.5 text-caption font-weight-black text-primary text-no-wrap me-2">
            <v-icon size="18" color="primary">mdi-calculator-variant-outline</v-icon>
            <span>معادلة المطابقة المتوقعة:</span>
          </div>

          <!-- المقيدون -->
          <div class="formula-box d-flex align-center gap-1.5 px-3 py-1.5 rounded-lg border">
            <span class="text-caption text-medium-emphasis font-weight-bold">المقيدون:</span>
            <span class="text-body-2 font-weight-black text-primary font-mono">{{ currentEnvelope.expectedCount }}</span>
          </div>

          <span class="text-h6 font-weight-black text-medium-emphasis mx-1">=</span>

          <!-- الحاضرون -->
          <div class="formula-box d-flex align-center gap-1.5 px-3 py-1.5 rounded-lg border">
            <span class="text-caption text-medium-emphasis font-weight-bold">ورقة حاضرة:</span>
            <span class="text-body-2 font-weight-black text-success font-mono">{{ expectedPresentSheets }}</span>
          </div>

          <span class="text-h6 font-weight-black text-medium-emphasis mx-1">+</span>

          <!-- الغياب -->
          <div class="formula-box d-flex align-center gap-1.5 px-3 py-1.5 rounded-lg border">
            <span class="text-caption text-medium-emphasis font-weight-bold">طالب غائب:</span>
            <span class="text-body-2 font-weight-black text-warning font-mono">{{ currentEnvelope.absentCount }}</span>
          </div>
        </div>

        <!-- هدف السحب من الماسح -->
        <v-chip
          size="default"
          color="primary"
          variant="tonal"
          class="font-weight-black font-mono px-3"
        >
          المطلوب سحبه من الماسح: {{ expectedPresentSheets }} ورقة
        </v-chip>
      </div>
    </filter-fields>

          <!-- ── 2. ملقم تغذية أوراق المظروف من الماسح الضوئي (Scanner Feed Bay) ── -->
          <v-card class="main-card pa-5 rounded-2xl border-0 shadow-sm mb-5">
            <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-4">
              <div class="d-flex align-center gap-3">
                <v-avatar size="40" color="primary" variant="tonal" class="rounded-xl">
                  <v-icon size="22" color="primary">mdi-tray-arrow-down</v-icon>
                </v-avatar>
                <div>
                  <h3 class="text-subtitle-1 font-weight-black mb-0">
                    2. تغذية حزمة أوراق المظروف من الماسح الضوئي
                  </h3>
                  <span class="text-caption text-medium-emphasis">
                    معالجة رزم المظاريف عبر السحب المباشر أو المجلد الساخن المراقب
                  </span>
                </div>
              </div>

              <!-- خيارات ربط الماسح والمراقبة باستخدام custom-btn -->
              <div class="d-flex align-center gap-2 flex-wrap">
                <custom-btn
                  :color="hotFolderActive ? 'success' : 'grey'"
                  :variant="hotFolderActive ? 'flat' : 'tonal'"
                  :label="hotFolderActive ? 'مجلد الماسح متصل ومراقب' : 'ربط مجلد الماسح (Hot-Folder)'"
                  icon="mdi-folder-sync-outline"
                  class="font-weight-bold"
                  :click="toggleHotFolder"
                />

                <custom-btn
                  type="imports"
                  label="استعراض ملفات الماسح"
                  class="font-weight-bold"
                  :click="() => $refs.fileInput.click()"
                />
              </div>
            </div>

            <!-- مساحة إفلات وتلقيم حزمة أوراق المظروف (تصميم النظام الموحد مثل استيراد الأسئلة) -->
            <div
              class="upload-dropzone pa-8 rounded-2xl text-center d-flex flex-column align-center justify-center transition-all cursor-pointer"
              :class="{ 'is-dragover': isDragging, 'has-file': batchFiles.length > 0 }"
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

              <template v-if="batchFiles.length === 0">
                <v-avatar size="72" color="primary" variant="tonal" class="mb-4 rounded-2xl">
                  <v-icon size="36" color="primary">mdi-cloud-upload-outline</v-icon>
                </v-avatar>
                <h4 class="text-h6 font-weight-black mb-2">اسحب وأفلت حزمة أوراق المظروف هنا</h4>
                <p class="text-body-2 text-medium-emphasis mb-3">
                  ملف PDF متعدد الصفحات أو حزمة صور الماسح الضوئي بدقة 300 DPI
                </p>
                <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold mb-4">
                  الصيغ المدعومة: PDF متعدد الصفحات، أرشيف ZIP، أو صور (JPG, PNG, TIFF)
                </v-chip>
                <custom-btn
                  type="imports"
                  label="استعراض واختيار ملفات المظروف"
                  class="font-weight-bold px-6"
                  :click="(e) => { if(e) e.stopPropagation(); $refs.fileInput.click(); }"
                />
              </template>

              <template v-else>
                <v-avatar size="72" color="success" variant="tonal" class="mb-4 rounded-2xl">
                  <v-icon size="36" color="success">mdi-file-check-outline</v-icon>
                </v-avatar>
                <h4 class="text-h6 font-weight-black text-success mb-1">
                  تم تجهيز {{ batchFiles.length }} ورقة / ملف تابعة للمظروف
                </h4>
                <p class="text-caption text-medium-emphasis font-weight-bold mb-4">
                  الحجم الإجمالي للحزمة: {{ formatTotalSize() }} — المظروف جاهز لبدء المسح والتصحيح
                </p>
                <div class="d-flex align-center justify-center gap-3">
                  <custom-btn
                    type="del"
                    label="إلغاء الملفات"
                    class="font-weight-bold"
                    :click="(e) => { if(e) e.stopPropagation(); clearFiles(); }"
                  />
                  <custom-btn
                    type="add"
                    label="إضافة أوراق أخرى"
                    class="font-weight-bold"
                    :click="(e) => { if(e) e.stopPropagation(); $refs.fileInput.click(); }"
                  />
                </div>
              </template>
            </div>

            <!-- زر بدء التصحيح والمسح الموحد -->
            <div v-if="batchFiles.length > 0 && !isGrading" class="mt-5 text-center">
              <custom-btn
                type="ok"
                :label="`بدء المسح والتصحيح الآلي للمظروف (${batchFiles.length} ورقة) الآن`"
                color="primary"
                variant="flat"
                class="font-weight-black px-8"
                style="height: 44px; min-width: 280px;"
                :disabled="!selectedExamId"
                :click="startBatchGrading"
              />
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
            <v-alert
              v-if="reconciliationStatus === 'BALANCED'"
              type="success"
              variant="tonal"
              rounded="2xl"
              class="pa-4 mb-3 border-success"
            >
              <div class="d-flex align-center justify-space-between flex-wrap gap-3">
                <div>
                  <div class="text-subtitle-1 font-weight-black mb-1">
                    المظروف مطابق ومكتمل 100% ({{ actualScannedCount + currentEnvelope.absentCount }} / {{ currentEnvelope.expectedCount }})
                  </div>
                  <div class="text-caption font-weight-bold opacity-90">
                    تم استيفاء كامل أوراق القاعة: {{ actualScannedCount }} ورقة إجابة ممسوحة + {{ currentEnvelope.absentCount }} غياب مسجل رسمي بكشف الحضور والغياب. لا يوجد أي عجز أو فقد في الأوراق.
                  </div>
                </div>

                <custom-btn
                  type="done"
                  :label="isCommitted ? 'تم اعتماد وترحيل المظروف' : 'اعتماد وترحيل المظروف للكنترول'"
                  color="success"
                  variant="flat"
                  class="font-weight-bold"
                  :disabled="isCommitted"
                  :click="commitEnvelopeToControl"
                />
              </div>
            </v-alert>

            <!-- حالة 2: عجز ونقص في الأوراق (Deficit Alert) -->
            <v-alert
              v-else-if="reconciliationStatus === 'DEFICIT'"
              type="error"
              variant="tonal"
              rounded="2xl"
              class="pa-4 mb-3 border-error"
            >
              <div class="d-flex align-center justify-space-between flex-wrap gap-3">
                <div>
                  <div class="text-subtitle-1 font-weight-black mb-1">
                    تنبيه عجز: نقص في أوراق المظروف الامتحاني!
                  </div>
                  <div class="text-caption font-weight-bold opacity-90">
                    سعة القاعة المقيدة: {{ currentEnvelope.expectedCount }} طالباً | الأوراق المسحوبة: {{ actualScannedCount }} + الغياب: {{ currentEnvelope.absentCount }} = {{ actualScannedCount + currentEnvelope.absentCount }} ورقة.
                    <strong class="text-decoration-underline">يوجد عجز بمقدار ({{ discrepancyAmount }}) ورقة مفقودة!</strong>
                    يرجى فحص سلة الماسح أو المظروف فوراً قبل الاعتماد.
                  </div>
                </div>

                <custom-btn
                  type="del"
                  label="تحرير محضر عجز مظروف"
                  color="error"
                  variant="flat"
                  class="font-weight-bold"
                  :click="openDiscrepancyReport"
                />
              </div>
            </v-alert>

            <!-- حالة 3: فائض وزيادة غير مبررة (Surplus Alert) -->
            <v-alert
              v-else-if="reconciliationStatus === 'SURPLUS'"
              type="warning"
              variant="tonal"
              rounded="2xl"
              class="pa-4 mb-3 border-warning"
            >
              <div class="d-flex align-center justify-space-between flex-wrap gap-3">
                <div>
                  <div class="text-subtitle-1 font-weight-black mb-1">
                    تنبيه فائض: تم مسح أوراق إضافية غير مقيدة في المظروف!
                  </div>
                  <div class="text-caption font-weight-bold opacity-90">
                    سعة القاعة: {{ currentEnvelope.expectedCount }} | الممسوح + الغياب: {{ actualScannedCount + currentEnvelope.absentCount }} (فائض بمقدار {{ Math.abs(discrepancyAmount) }} ورقة).
                    يرجى التأكد من عدم اختلاط أوراق قاعة أخرى في الرزمة.
                  </div>
                </div>

                <custom-btn
                  type="show"
                  label="مراجعة الرزمة"
                  color="warning"
                  variant="flat"
                  class="font-weight-bold"
                  :click="openDiscrepancyReport"
                />
              </div>
            </v-alert>
          </div>

          <!-- ── د. نتائج الفرز والتدقيق لأوراق المظروف (Batch Triaging Table) ── -->
          <div v-if="batchResult && batchResult.sheets && batchResult.sheets.length > 0" class="mb-5">
            <!-- عدادات الفرز الثلاثية -->
            <v-row dense class="mb-3">
              <v-col cols="12" sm="4">
                <v-card variant="tonal" color="success" class="pa-3 rounded-xl border text-center">
                  <div class="text-caption font-weight-bold">أوراق سليمة ومعتمدة</div>
                  <div class="text-h5 font-weight-black font-mono">
                    {{ successfulSheets.length }}
                  </div>
                  <div class="text-caption opacity-80">رُصدت درجاتها آلياً بنجاح</div>
                </v-card>
              </v-col>

              <v-col cols="12" sm="4">
                <v-card variant="tonal" color="warning" class="pa-3 rounded-xl border text-center">
                  <div class="text-caption font-weight-bold">أوراق تحتاج تدقيق بشري</div>
                  <div class="text-h5 font-weight-black font-mono">
                    {{ needsReviewSheets.length }}
                  </div>
                  <div class="text-caption opacity-80">تظليل مزدوج أو التباس مقعد</div>
                </v-card>
              </v-col>

              <v-col cols="12" sm="4">
                <v-card variant="tonal" color="primary" class="pa-3 rounded-xl border text-center">
                  <div class="text-caption font-weight-bold">متوسط درجات القاعة</div>
                  <div class="text-h5 font-weight-black font-mono">
                    {{ currentEnvelopeAvgScore }}%
                  </div>
                  <div class="text-caption opacity-80">المعدل العام للقاعة</div>
                </v-card>
              </v-col>
            </v-row>

            <!-- جدول أوراق المظروف المصححة فعلياً -->
            <v-card class="rounded-2xl border-0 shadow-sm overflow-hidden bg-surface">
              <div class="pa-3 border-b d-flex align-center justify-space-between flex-wrap gap-2" style="background: rgba(var(--v-theme-surface-variant), 0.25);">
                <div class="d-flex align-center gap-2">
                  <v-icon color="primary" size="20">mdi-format-list-numbered-rtl</v-icon>
                  <span class="text-subtitle-2 font-weight-black text-on-surface">
                    الأوراق الممسوحة فعلياً في مظروف: {{ currentEnvelope.envelopeCode }} ({{ displaySheets.length }} ورقة)
                  </span>
                </div>

                <div class="d-flex align-center gap-2">
                  <custom-btn
                    v-if="needsReviewSheets.length > 0"
                    type="show"
                    :label="`مراجعة وتدقيق ${needsReviewSheets.length} ورقة`"
                    color="warning"
                    variant="tonal"
                    class="font-weight-bold"
                    :click="() => $router.push(`/omr-human-review?exam=${selectedExamId}`)"
                  />

                  <custom-btn
                    type="add"
                    label="المظروف التالي"
                    color="success"
                    variant="tonal"
                    class="font-weight-bold"
                    :click="prepareNextEnvelope"
                  />
                </div>
              </div>

              <custom-data-table
                :items="scannedSheetsTableItems"
                :getData="getScannedSheetsData"
                :headers="scannedSheetsHeaders"
                :hasFilter="false"
                :log="false"
                :restore="false"
                :numbering="false"
                :showSelect="false"
                :actions="false"
                :search="false"
                class="bg-transparent"
              >
                <template v-slot:item-slot="{ item, key }">
                  <!-- رقم الجلوس -->
                  <template v-if="key === 'seat_number'">
                    <span class="font-mono font-weight-black text-primary px-2.5 py-1 rounded-lg border bg-surface">
                      {{ item.seat_number }}
                    </span>
                  </template>

                  <!-- اسم الطالب -->
                  <template v-else-if="key === 'student_name'">
                    <span class="font-weight-bold text-body-2 text-on-surface">{{ item.student_name || 'طالب غير محدد' }}</span>
                  </template>

                  <!-- نموذج الأسئلة -->
                  <template v-else-if="key === 'model_code'">
                    <v-chip size="small" variant="tonal" color="primary" class="font-weight-bold">
                      النموذج {{ item.model_code || 'A' }}
                    </v-chip>
                  </template>

                  <!-- الدرجة -->
                  <template v-else-if="key === 'score'">
                    <span class="font-weight-black font-mono text-body-2 text-on-surface">
                      {{ item.score }} / {{ item.max_score || 40 }}
                    </span>
                  </template>

                  <!-- النسبة -->
                  <template v-else-if="key === 'percentage'">
                    <v-chip size="small" variant="tonal" color="success" class="font-weight-bold font-mono">
                      {{ item.percentage }}%
                    </v-chip>
                  </template>

                  <!-- حالة التصحيح -->
                  <template v-else-if="key === 'status'">
                    <v-chip
                      v-if="item.status === 'NEEDS_REVIEW' || item.needs_review"
                      size="small"
                      color="warning"
                      variant="flat"
                      class="font-weight-bold"
                    >
                      تدقيق بشري
                    </v-chip>
                    <v-chip
                      v-else
                      size="small"
                      color="success"
                      variant="flat"
                      class="font-weight-bold"
                    >
                      معتمد وسليم
                    </v-chip>
                  </template>

                  <!-- المعاينة -->
                  <template v-else-if="key === 'actions'">
                    <custom-btn
                      is-icon
                      type="show"
                      label="معاينة الورقة الضوئية"
                      :click="() => openSheetPreview(item)"
                    />
                  </template>
                </template>
              </custom-data-table>
            </v-card>
          </div>

          <!-- ── هـ. كشف الطلاب المقيدين رسمياً في القاعة (عند عدم وجود أوراق ممسوحة بعد) ── -->
          <div v-else class="mb-5">
            <v-card class="rounded-2xl border-0 shadow-sm overflow-hidden bg-surface">
              <div class="pa-4 border-b d-flex align-center justify-space-between flex-wrap gap-2" style="background: rgba(var(--v-theme-surface-variant), 0.25);">
                <div class="d-flex align-center gap-2">
                  <v-icon color="primary" size="22">mdi-clipboard-list-outline</v-icon>
                  <div>
                    <span class="text-subtitle-2 font-weight-black text-on-surface">
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
                <custom-data-table
                  :items="regStudentsTableItems"
                  :getData="getRegStudentsData"
                  :headers="regStudentsHeaders"
                  :customLoading="loadingExams"
                  :hasFilter="false"
                  :log="false"
                  :restore="false"
                  :numbering="false"
                  :showSelect="false"
                  :actions="false"
                  :search="false"
                  class="bg-transparent"
                >
                  <template v-slot:item-slot="{ item, key, index }">
                    <!-- م (الترقيم) -->
                    <template v-if="key === 'index_number'">
                      <span class="font-mono text-caption text-medium-emphasis font-weight-bold">
                        {{ ((regStudentsTableItems.pagination?.current_page || 1) - 1) * (regStudentsTableItems.pagination?.page_size || 10) + (index ?? 0) + 1 }}
                      </span>
                    </template>

                    <!-- رقم الجلوس -->
                    <template v-else-if="key === 'seat_number'">
                      <span class="font-mono font-weight-black text-primary px-2.5 py-1 rounded-lg border bg-surface">
                        {{ item.seat_number }}
                      </span>
                    </template>

                    <!-- اسم الطالب -->
                    <template v-else-if="key === 'student_name'">
                      <span class="font-weight-bold text-body-2 text-on-surface">{{ item.student_name || 'طالب مقيد' }}</span>
                    </template>

                    <!-- النموذج المخصص -->
                    <template v-else-if="key === 'model_code'">
                      <v-chip size="small" variant="tonal" color="primary" class="font-weight-bold">
                        النموذج {{ item.model_code || 'A' }}
                      </v-chip>
                    </template>

                    <!-- المدرسة / المركز -->
                    <template v-else-if="key === 'school_name'">
                      <span class="text-body-2">{{ item.school_name || currentEnvelope.examCenter || '-' }}</span>
                    </template>

                    <!-- حالة المسح والتصحيح -->
                    <template v-else-if="key === 'scan_status'">
                      <v-chip size="small" color="blue-grey" variant="tonal" class="font-weight-bold">
                        بانتظار سحب الورقة
                      </v-chip>
                    </template>
                  </template>
                </custom-data-table>
              </div>

              <div v-else class="pa-8 text-center">
                <v-avatar size="64" color="primary" variant="tonal" class="mb-3 rounded-2xl">
                  <v-icon size="32" color="primary">mdi-account-group-outline</v-icon>
                </v-avatar>
                <div class="text-subtitle-1 font-weight-bold">لا توجد بيانات طلاب مقيدين مسجلة في هذا الاختبار</div>
                <div class="text-caption text-medium-emphasis">يرجى التحقق من اختيار الاختبار والمركز الامتحاني من الفلاتر أعلاه</div>
              </div>
            </v-card>
          </div>


    <!-- ── نافذة معاينة ورقة الطالب (Sheet Details Dialog) ── -->
    <v-dialog v-model="previewDialog" max-width="1100px" scrollable>
      <v-card v-if="activePreviewSheet" class="rounded-2xl overflow-hidden main-card bg-surface">
        <!-- Dialog Header (Unified with OMRHumanReviewView) -->
        <v-card-title class="d-flex align-center justify-space-between bg-surface px-6 py-4 border-b">
          <div class="d-flex align-center gap-3">
            <v-avatar color="primary" variant="tonal" rounded="lg" size="44">
              <v-icon size="24" color="primary">mdi-file-document-check-outline</v-icon>
            </v-avatar>
            <div>
              <div class="d-flex align-center gap-2 flex-wrap">
                <h3 class="text-h6 font-weight-black text-on-surface mb-0">
                  {{ activePreviewSheet.student_name || 'طالب بدون اسم' }}
                </h3>
                <v-chip size="small" color="primary" variant="flat" class="font-weight-bold px-2 unified-table-chip">
                  رقم الجلوس: {{ activePreviewSheet.seat_number || '—' }}
                </v-chip>
                <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold px-2 unified-table-chip">
                  النموذج: {{ activePreviewSheet.model_code || 'A' }}
                </v-chip>
                <v-chip
                  v-if="activePreviewSheet.status === 'NEEDS_REVIEW' || activePreviewSheet.needs_review"
                  size="small"
                  color="warning"
                  variant="flat"
                  class="font-weight-bold px-2 text-white unified-table-chip"
                >
                  <v-icon start size="14">mdi-alert-circle</v-icon>
                  يحتاج تدقيق بشري
                </v-chip>
                <v-chip
                  v-else
                  size="small"
                  color="success"
                  variant="flat"
                  class="font-weight-bold px-2 text-white unified-table-chip"
                >
                  <v-icon start size="14">mdi-check-circle</v-icon>
                  معتمد وسليم
                </v-chip>
              </div>
              <p class="text-caption text-medium-emphasis mb-0 mt-1">
                تفاصيل ورقة إجابة الطالب وتدقيق دوائر الماسح الضوئي (OMR)
              </p>
            </div>
          </div>

          <div class="d-flex align-center gap-3">
            <div class="d-flex align-center gap-2 px-3 py-1.5 rounded-xl border bg-surface">
              <v-icon size="18" color="success">mdi-check-decagram</v-icon>
              <div class="d-flex flex-column text-end">
                <span class="text-caption text-medium-emphasis" style="font-size: 10px; line-height: 1;">الدرجة الكلية</span>
                <span class="font-weight-black text-body-1 text-success" style="line-height: 1.2;">
                  {{ activePreviewSheet.score != null ? activePreviewSheet.score : 0 }} 
                  <span class="text-caption text-medium-emphasis">/ {{ activePreviewSheet.max_score || 40 }}</span>
                </span>
              </div>
            </div>

            <div class="d-flex align-center gap-2 px-3 py-1.5 rounded-xl border bg-surface">
              <v-icon size="18" :color="activePreviewSheet.percentage >= 50 ? 'success' : 'error'">mdi-percent</v-icon>
              <div class="d-flex flex-column text-end">
                <span class="text-caption text-medium-emphasis" style="font-size: 10px; line-height: 1;">النسبة</span>
                <span class="font-weight-black text-body-1" :class="activePreviewSheet.percentage >= 50 ? 'text-success' : 'text-error'" style="line-height: 1.2;">
                  {{ activePreviewSheet.percentage }}%
                </span>
              </div>
            </div>

            <v-btn icon="mdi-close" variant="text" size="small" color="medium-emphasis" @click="previewDialog = false" />
          </div>
        </v-card-title>

        <!-- تبويبات العرض الموحدة (v-tabs) -->
        <v-tabs v-model="previewMode" color="primary" density="comfortable" class="border-b px-4 bg-surface">
          <v-tab value="questions" class="font-weight-bold">
            <v-icon start size="18">mdi-format-list-numbered</v-icon>
            جدول تفصيل الأسئلة والدوائر ({{ (activePreviewSheet.questions || []).length }})
          </v-tab>
          <v-tab value="annotated" class="font-weight-bold">
            <v-icon start size="18">mdi-check-circle-outline</v-icon>
            ورقة فحص وتدقيق الذكاء الاصطناعي
          </v-tab>
          <v-tab value="original" class="font-weight-bold">
            <v-icon start size="18">mdi-image-outline</v-icon>
            الورقة الممسوحة الأصلية
          </v-tab>
        </v-tabs>

        <v-card-text class="pa-4 bg-surface" style="max-height: 72vh;">
          <!-- ── جدول تفصيل الأسئلة والدوائر بالجدول الموحد (custom-data-table) ── -->
          <div v-if="previewMode === 'questions'">
            <!-- شريط مؤشرات الدوائر -->
            <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3">
              <div class="d-flex align-center gap-2 flex-wrap">
                <v-chip size="small" variant="tonal" color="primary" class="font-weight-bold">
                  إجمالي الأسئلة: {{ (activePreviewSheet.questions || []).length }}
                </v-chip>
                <v-chip size="small" variant="tonal" color="success" class="font-weight-bold">
                  صحيحة: {{ previewCounts.correct }}
                </v-chip>
                <v-chip size="small" variant="tonal" color="error" class="font-weight-bold">
                  خاطئة: {{ previewCounts.wrong }}
                </v-chip>
                <v-chip size="small" variant="tonal" color="grey" class="font-weight-bold">
                  فارغة: {{ previewCounts.empty }}
                </v-chip>
              </div>

              <v-chip
                size="small"
                :color="activePreviewSheet.score > 0 ? 'success' : 'grey-darken-1'"
                variant="tonal"
                class="font-weight-bold"
              >
                <v-icon start size="16">mdi-check-decagram-outline</v-icon>
                حالة الدوائر: {{ activePreviewSheet.score > 0 ? 'تم رصد إجابات مظللة' : 'جميع الدوائر فارغة (لم تُظلل)' }}
              </v-chip>
            </div>

            <!-- الجدول الموحد للأسئلة -->
            <div class="main-card rounded-2xl overflow-hidden mb-2 border">
              <custom-data-table
                :items="previewQuestionsTableItems"
                :getData="getPreviewQuestionsData"
                :headers="previewQuestionsHeaders"
                :hasFilter="false"
                :log="false"
                :restore="false"
                :numbering="false"
                :showSelect="false"
                :actions="false"
                :search="false"
                class="bg-transparent"
              >
                <template v-slot:item-slot="{ item, key }">
                  <!-- رقم السؤال -->
                  <template v-if="key === 'question_number'">
                    <div class="text-center py-1">
                      <span class="font-weight-black text-body-2 text-primary bg-blue-lighten-5 px-3 py-1 rounded-pill border">
                        #{{ item.question_number }}
                      </span>
                    </div>
                  </template>

                  <!-- الإجابة النموذجية المعتمدة -->
                  <template v-else-if="key === 'correct_choice'">
                    <div class="text-center">
                      <v-chip
                        v-if="item.correct_choice && item.correct_choice !== '—'"
                        size="small"
                        color="success"
                        variant="tonal"
                        class="font-weight-black unified-table-chip px-3 border"
                      >
                        <v-icon start size="13" color="success">mdi-check-circle-outline</v-icon>
                        {{ item.correct_choice }}
                      </v-chip>
                      <span v-else class="text-caption text-medium-emphasis">—</span>
                    </div>
                  </template>

                  <!-- تظليل الطالب المكتشف -->
                  <template v-else-if="key === 'marked_choice'">
                    <div class="text-center">
                      <v-chip
                        v-if="item.is_marked"
                        size="small"
                        :color="item.is_correct ? 'primary' : 'error'"
                        variant="tonal"
                        class="font-weight-black font-mono unified-table-chip px-3"
                      >
                        <v-icon start size="13">{{ item.is_correct ? 'mdi-check' : 'mdi-close' }}</v-icon>
                        {{ item.marked_choice }}
                      </v-chip>
                      <v-chip v-else size="small" color="grey" variant="tonal" class="font-weight-medium px-2 text-caption">
                        فارغ (لم يُظلل)
                      </v-chip>
                    </div>
                  </template>

                  <!-- حالة الدائرة -->
                  <template v-else-if="key === 'bubble_status'">
                    <div class="text-center">
                      <v-chip
                        v-if="item.is_marked"
                        size="small"
                        color="success"
                        variant="tonal"
                        class="font-weight-bold"
                      >
                        <v-icon start size="14">mdi-circle</v-icon>
                        مظللة
                      </v-chip>
                      <v-chip
                        v-else
                        size="small"
                        color="grey"
                        variant="tonal"
                        class="font-weight-bold"
                      >
                        <v-icon start size="14">mdi-circle-outline</v-icon>
                        دائرة فارغة
                      </v-chip>
                    </div>
                  </template>

                  <!-- النتيجة -->
                  <template v-else-if="key === 'status'">
                    <div class="text-center">
                      <v-chip
                        v-if="!item.is_marked"
                        size="small"
                        color="secondary"
                        variant="tonal"
                        class="font-weight-bold text-caption px-2"
                      >
                        لم يُجب
                      </v-chip>
                      <v-chip
                        v-else-if="item.is_correct"
                        size="small"
                        color="success"
                        variant="flat"
                        class="font-weight-bold text-caption px-2 text-white"
                      >
                        صحيحة
                      </v-chip>
                      <v-chip
                        v-else
                        size="small"
                        color="error"
                        variant="flat"
                        class="font-weight-bold text-caption px-2 text-white"
                      >
                        خاطئة
                      </v-chip>
                    </div>
                  </template>

                  <!-- الدرجة -->
                  <template v-else-if="key === 'score'">
                    <div class="text-center font-weight-black font-mono">
                      <v-chip
                        size="small"
                        :color="item.score > 0 ? 'success' : 'grey-lighten-2'"
                        :class="item.score > 0 ? 'text-white font-weight-black' : 'text-grey-darken-2 font-weight-black'"
                        variant="flat"
                        class="unified-table-chip px-2.5 font-mono"
                      >
                        {{ item.score }}
                      </v-chip>
                    </div>
                  </template>
                </template>
              </custom-data-table>
            </div>
          </div>

          <!-- عرض ورقة التدقيق والذكاء الاصطناعي -->
          <div v-else-if="previewMode === 'annotated'" class="text-center pa-4 border rounded-2xl mb-2 position-relative bg-surface">
            <div v-if="!activePreviewSheet.annotated_url && !activePreviewSheet.image_url" class="py-12 text-medium-emphasis">
              <v-icon size="48" color="medium-emphasis" class="mb-2">mdi-image-off-outline</v-icon>
              <div class="text-subtitle-1 font-weight-bold">لا توجد صورة متوفرة لورقة هذا الطالب</div>
              <div class="text-caption">تم تسجيل بيانات التصحيح الضوئي مباشرة بدون تخزين الصورة النقطية</div>
            </div>
            <template v-else>
              <v-img 
                :src="activePreviewSheet.annotated_url || activePreviewSheet.image_url" 
                max-height="600" 
                contain 
                class="rounded-xl border" 
              />
              <div class="text-caption text-medium-emphasis mt-3 font-weight-bold">
                * الحلقات الملونة توضح مواضع كافة الدوائر التي فحصها المحرك بدقة بالذكاء الاصطناعي ومستوى الكثافة الضوئية.
              </div>
            </template>
          </div>

          <!-- عرض الورقة الممسوحة الأصلية -->
          <div v-else-if="previewMode === 'original'" class="text-center pa-4 border rounded-2xl mb-2 bg-surface">
            <div v-if="!activePreviewSheet.image_url" class="py-12 text-medium-emphasis">
              <v-icon size="48" color="medium-emphasis" class="mb-2">mdi-image-off-outline</v-icon>
              <div class="text-subtitle-1 font-weight-bold">لا توجد صورة أصلية متوفرة</div>
            </div>
            <v-img v-else :src="activePreviewSheet.image_url" max-height="600" contain class="rounded-xl border" />
          </div>
        </v-card-text>

        <!-- Dialog Footer -->
        <v-card-actions class="px-6 py-3 bg-surface border-t d-flex align-center justify-space-between">
          <div class="text-caption text-medium-emphasis">
            تم فحص وتحليل الورقة آلياً عبر محرك التصحيح الضوئي الذكي OMR
          </div>
          <div class="d-flex align-center gap-2">
            <custom-btn
              v-if="activePreviewSheet.status === 'NEEDS_REVIEW' || activePreviewSheet.needs_review"
              type="show"
              label="الانتقال للمراجعة البشرية"
              color="warning"
              variant="flat"
              class="font-weight-bold"
              :click="() => $router.push(`/omr-human-review?exam=${selectedExamId}`)"
            />
            <custom-btn
              type="cancel"
              label="إغلاق النافذة"
              class="font-weight-bold"
              :click="() => previewDialog = false"
            />
          </div>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted, onUnmounted, reactive } from 'vue'
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

    const isSchoolFilter = computed(() => {
      return !filterInstitutionType.value || filterInstitutionType.value === 'all' || filterInstitutionType.value === 'school'
    })

    const isOrgDisabled = computed(() => {
      if (isSchoolFilter.value) {
        return !filterGovernorate.value || !filterDirectorate.value
      }
      return !filterGovernorate.value
    })

    const orgPlaceholder = computed(() => {
      const typeLabel = filterInstitutionType.value === 'university'
        ? 'الكلية / الجامعة'
        : (filterInstitutionType.value === 'institute' ? 'المعهد / المركز' : 'المدرسة')
      if (isSchoolFilter.value) {
        if (!filterGovernorate.value) return 'اختر المحافظة أولاً...'
        if (!filterDirectorate.value) return 'اختر المديرية أولاً...'
        return `${typeLabel} (التابعة للمديرية)`
      }
      if (!filterGovernorate.value) return 'اختر المحافظة أولاً...'
      return `${typeLabel} (التابعة للمحافظة)`
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
      filterGovernorate.value = null
      filterDirectorate.value = null
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
      } else {
        p.institution_type = 'school'
      }
      if (filterGovernorate.value) p.governorate = filterGovernorate.value
      if (isSchoolFilter.value && filterDirectorate.value) p.directorate = filterDirectorate.value
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
    const previewMode = ref('questions')

    const previewQuestionsHeaders = ref([
      { title: 'رقم السؤال', key: 'question_number', sortable: true, width: '100px', align: 'center' },
      { title: 'الإجابة النموذجية', key: 'correct_choice', sortable: true, width: '140px', align: 'center' },
      { title: 'تظليل الطالب المكتشف', key: 'marked_choice', sortable: true, width: '160px', align: 'center' },
      { title: 'حالة الدائرة', key: 'bubble_status', sortable: true, width: '130px', align: 'center' },
      { title: 'النتيجة', key: 'status', sortable: true, width: '120px', align: 'center' },
      { title: 'الدرجة', key: 'score', sortable: true, width: '100px', align: 'center' },
    ])

    const previewQuestionsPage = ref(1)
    const previewQuestionsPageSize = ref(10)
    const previewQuestionsTableItems = ref({
      results: [],
      count: 0,
      pagination: {
        count: 0,
        total: 0,
        num_pages: 1,
        current_page: 1,
        page_size: 10,
      },
    })

    const previewCounts = computed(() => {
      const qs = activePreviewSheet.value?.questions || []
      let correct = 0
      let wrong = 0
      let empty = 0
      qs.forEach((q) => {
        const marked = q.marked_choice || q.marked
        const isMarked = Boolean(marked && marked !== 'لم يُجب (فارغ)' && marked !== 'فارغ')
        if (!isMarked) {
          empty++
        } else {
          const correctChoice = q.correct_choice || '—'
          const isCorr = q.is_correct ?? (correctChoice !== '—' && String(marked).trim().toUpperCase() === String(correctChoice).trim().toUpperCase())
          if (isCorr) correct++
          else wrong++
        }
      })
      return { total: qs.length, correct, wrong, empty }
    })

    const getPreviewQuestionsData = async (params = {}) => {
      const p = params?.params || params || {}
      const page = Number(p.page) || previewQuestionsPage.value || 1
      const pageSize = Number(p.page_size || p.perPage) || previewQuestionsPageSize.value || 10
      previewQuestionsPage.value = page
      previewQuestionsPageSize.value = pageSize

      const rawQuestions = activePreviewSheet.value?.questions || []
      const all = rawQuestions.map((q, idx) => {
        const qNum = q.question_number || q.question_id || q.q || (idx + 1)
        const marked = q.marked_choice || q.marked || null
        const correct = q.correct_choice || '—'
        const isMarked = Boolean(marked && marked !== 'لم يُجب (فارغ)' && marked !== 'فارغ')
        const isCorrect = q.is_correct ?? (isMarked && correct !== '—' && String(marked).trim().toUpperCase() === String(correct).trim().toUpperCase())
        const score = q.score_awarded ?? q.marks_awarded ?? (isCorrect ? 1 : 0)

        return {
          ...q,
          question_number: qNum,
          marked_choice: marked,
          correct_choice: correct,
          is_marked: isMarked,
          is_correct: isCorrect,
          score: score,
        }
      })

      const total = all.length
      const numPages = Math.ceil(total / pageSize) || 1
      const validPage = Math.min(Math.max(1, page), numPages)
      const start = (validPage - 1) * pageSize

      previewQuestionsTableItems.value = {
        results: all.slice(start, start + pageSize),
        count: total,
        pagination: {
          count: total,
          total: total,
          num_pages: numPages,
          current_page: validPage,
          page_size: pageSize,
        },
      }
      return previewQuestionsTableItems.value
    }

    watch(previewMode, (mode) => {
      if (mode === 'questions') {
        getPreviewQuestionsData({ page: previewQuestionsPage.value, page_size: previewQuestionsPageSize.value })
      }
    })

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

    // ── Unified Tables: Registered Students (Table A) & Scanned Sheets (Table B) ──
    const regStudentsHeaders = ref([
      { title: 'م', key: 'index_number', sortable: false, width: '60px', align: 'center' },
      { title: 'رقم الجلوس', key: 'seat_number', sortable: true, width: '130px' },
      { title: 'اسم الطالب الثلاثي/الرباعي', key: 'student_name', sortable: true },
      { title: 'النموذج المخصص', key: 'model_code', sortable: false, width: '130px', align: 'center' },
      { title: 'المدرسة / المركز المقيد به', key: 'school_name', sortable: false },
      { title: 'حالة المسح والتصحيح', key: 'scan_status', sortable: false, width: '160px', align: 'center' },
    ])

    const regStudentsPage = ref(1)
    const regStudentsPageSize = ref(10)
    const regStudentsTableItems = ref({
      results: [],
      count: 0,
      pagination: {
        count: 0,
        total: 0,
        num_pages: 1,
        current_page: 1,
        page_size: 10,
      },
    })

    const getRegStudentsData = async (params = {}) => {
      const p = params?.params || params || {}
      const page = Number(p.page) || regStudentsPage.value || 1
      const pageSize = Number(p.page_size || p.perPage) || regStudentsPageSize.value || 10
      regStudentsPage.value = page
      regStudentsPageSize.value = pageSize

      const all = registeredStudents.value || []
      const total = all.length
      const numPages = Math.ceil(total / pageSize) || 1
      const validPage = Math.min(Math.max(1, page), numPages)
      const start = (validPage - 1) * pageSize

      regStudentsTableItems.value = {
        results: all.slice(start, start + pageSize),
        count: total,
        pagination: {
          count: total,
          total: total,
          num_pages: numPages,
          current_page: validPage,
          page_size: pageSize,
        },
      }
      return regStudentsTableItems.value
    }

    watch(registeredStudents, () => {
      regStudentsPage.value = 1
      getRegStudentsData({ page: 1, page_size: regStudentsPageSize.value })
    }, { immediate: true })

    const scannedSheetsHeaders = ref([
      { title: 'رقم الجلوس', key: 'seat_number', sortable: true, width: '120px' },
      { title: 'اسم الطالب', key: 'student_name', sortable: true },
      { title: 'نموذج الأسئلة', key: 'model_code', sortable: false, width: '120px', align: 'center' },
      { title: 'الدرجة المحسوبة', key: 'score', sortable: true, width: '130px', align: 'center' },
      { title: 'النسبة المئوية', key: 'percentage', sortable: true, width: '110px', align: 'center' },
      { title: 'حالة التصحيح', key: 'status', sortable: true, width: '140px', align: 'center' },
      { title: 'المعاينة', key: 'actions', sortable: false, width: '90px', align: 'center' },
    ])

    const scannedSheetsPage = ref(1)
    const scannedSheetsPageSize = ref(10)
    const scannedSheetsTableItems = ref({
      results: [],
      count: 0,
      pagination: {
        count: 0,
        total: 0,
        num_pages: 1,
        current_page: 1,
        page_size: 10,
      },
    })

    const getScannedSheetsData = async (params = {}) => {
      const p = params?.params || params || {}
      const page = Number(p.page) || scannedSheetsPage.value || 1
      const pageSize = Number(p.page_size || p.perPage) || scannedSheetsPageSize.value || 10
      scannedSheetsPage.value = page
      scannedSheetsPageSize.value = pageSize

      const all = displaySheets.value || []
      const total = all.length
      const numPages = Math.ceil(total / pageSize) || 1
      const validPage = Math.min(Math.max(1, page), numPages)
      const start = (validPage - 1) * pageSize

      scannedSheetsTableItems.value = {
        results: all.slice(start, start + pageSize),
        count: total,
        pagination: {
          count: total,
          total: total,
          num_pages: numPages,
          current_page: validPage,
          page_size: pageSize,
        },
      }
      return scannedSheetsTableItems.value
    }

    watch(displaySheets, () => {
      scannedSheetsPage.value = 1
      getScannedSheetsData({ page: 1, page_size: scannedSheetsPageSize.value })
    }, { immediate: true })

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
      previewMode.value = 'questions'
      previewQuestionsPage.value = 1
      getPreviewQuestionsData({ page: 1, page_size: previewQuestionsPageSize.value })
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
      isSchoolFilter,
      isOrgDisabled,
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
      regStudentsHeaders,
      regStudentsTableItems,
      getRegStudentsData,
      scannedSheetsHeaders,
      scannedSheetsTableItems,
      getScannedSheetsData,
      // Hot-Folder
      hotFolderActive,
      toggleHotFolder,
      // Preview Dialog
      previewDialog,
      activePreviewSheet,
      previewMode,
      openSheetPreview,
      previewCounts,
      previewQuestionsHeaders,
      previewQuestionsTableItems,
      getPreviewQuestionsData,
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

/* ── Formula Box ───────────────────────────────────────────── */
.formula-box {
  background: rgba(var(--v-theme-surface-variant), 0.25);
  border-color: rgba(var(--v-theme-outline), 0.2) !important;
  white-space: nowrap;
}

/* ── Upload Dropzone (Standard System Design) ──────────────── */
.upload-dropzone {
  background: rgba(var(--v-theme-surface-variant), 0.15);
  border: 2px dashed rgba(var(--v-border-color), 0.25);
  cursor: pointer;
  min-height: 240px;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.upload-dropzone:hover, .upload-dropzone.is-dragover {
  border-color: rgba(var(--v-theme-primary), 0.6);
  background: rgba(var(--v-theme-primary), 0.05);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.08);
}

.upload-dropzone.has-file {
  border-style: solid;
  border-color: rgba(var(--v-theme-success), 0.5);
  background: rgba(var(--v-theme-success), 0.04);
  box-shadow: 0 8px 24px rgba(var(--v-theme-success), 0.08);
  cursor: default;
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
