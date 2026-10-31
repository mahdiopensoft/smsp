<template>
  <div class="qb-national-control-console pa-3 pa-md-6">
    <!-- ── 1. بيانات المظروف الامتحاني والقاعة (Envelope Manifest & Dispatch Details) ── -->
    <filter-fields
      label="1. بيانات المظروف الامتحاني والقاعة (Envelope Manifest & Dispatch Details)"
      class="main-card border-0 pa-5 rounded-2xl mb-5 shadow-sm"
    >
      <v-row dense class="align-center">
        <!-- 1. نوع المؤسسة التعليمية (حقل واحد قياسي موحد بنمط students-master) -->
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filterInstitutionType"
            name="InstitutionType"
            placeholder="نوع المؤسسة التعليمية"
            label="نوع المؤسسة التعليمية"
            cols="12"
            :add="false"
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

        <!-- 2. المحافظة -->
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filterGovernorate"
            name="Governorate"
            placeholder="المحافظة *"
            label="المحافظة"
            cols="12"
            :add="false"
            @update:model-value="onGovernorateChange"
          />
        </v-col>

        <!-- 3. المديرية (تظهر للمدارس فقط) -->
        <v-col v-if="isSchoolFilter" cols="12" sm="6" md="3">
          <auto-list
            v-model="filterDirectorate"
            name="Directorate"
            :param="filterGovernorate"
            :placeholder="filterGovernorate ? 'المديرية *' : 'اختر المحافظة أولاً'"
            label="المديرية"
            cols="12"
            :add="false"
            :disabled="!filterGovernorate"
            @update:model-value="onDirectorateChange"
          />
        </v-col>

        <!-- 4. المركز الامتحاني (المدرسة / الكلية / المعهد) -->
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filterOrganization"
            name="Organization"
            :param="orgParam"
            :placeholder="orgPlaceholder"
            :label="orgFieldLabel"
            cols="12"
            :add="false"
            :disabled="isOrgDisabled"
            @update:model-value="onOrganizationChange"
          />
        </v-col>

        <!-- 5. الاختبار والمادة الدراسية -->
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="selectedExamId"
            name="Exam"
            :param="examFilterParam"
            placeholder="الاختبار والمادة الدراسية *"
            label="الاختبار والمادة الدراسية"
            cols="12"
            :add="false"
            @update:model-value="onExamChange"
          />
        </v-col>

        <!-- الهيكلية الأكاديمية التخصصية المشروطة -->
        <!-- أ. فلاتر المدارس -->
        <template v-if="filterInstitutionType === 'school'">
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterStage"
              name="Stage"
              placeholder="المرحلة الدراسية"
              label="المرحلة الدراسية"
              cols="12"
              :add="false"
              @update:model-value="onStageChange"
            />
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterClassTrack"
              name="ClassTrackByStage"
              :param="filterStage"
              placeholder="الصف والمسار"
              label="الصف والمسار"
              cols="12"
              :add="false"
              :disabled="!filterStage"
              @update:model-value="onClassTrackChange"
            />
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterSubject"
              name="Subject"
              :param="subjectFilterParam"
              placeholder="المادة الدراسية"
              label="المادة الدراسية"
              cols="12"
              :add="false"
              @update:model-value="onSubjectChange"
            />
          </v-col>
        </template>

        <!-- ب. فلاتر الجامعات -->
        <template v-if="filterInstitutionType === 'university'">
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterCollege"
              name="College"
              placeholder="الكلية الجامعية"
              label="الكلية الجامعية"
              cols="12"
              :add="false"
              @update:model-value="onCollegeChange"
            />
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterDepartment"
              name="DepartmentByCollege"
              :param="filterCollege"
              placeholder="القسم الأكاديمي"
              label="القسم الأكاديمي"
              cols="12"
              :add="false"
              :disabled="!filterCollege"
              @update:model-value="onDepartmentChange"
            />
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterSpecialization"
              name="Specialization"
              :param="filterDepartment"
              placeholder="التخصص والبرنامج"
              label="التخصص والبرنامج"
              cols="12"
              :add="false"
              :disabled="!filterDepartment"
              @update:model-value="onSpecializationChange"
            />
          </v-col>
        </template>

        <!-- ج. فلاتر المعاهد -->
        <template v-if="filterInstitutionType === 'institute'">
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterInstituteField"
              name="InstituteField"
              placeholder="المجال المهني"
              label="المجال المهني"
              cols="12"
              :add="false"
              @update:model-value="onInstituteFieldChange"
            />
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterInstituteEducationSystem"
              name="InstituteEducationSystem"
              :param="filterInstituteField"
              placeholder="نظام التعليم"
              label="نظام التعليم"
              cols="12"
              :add="false"
              :disabled="!filterInstituteField"
              @update:model-value="onInstituteEducationSystemChange"
            />
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterInstituteSpecialization"
              name="InstituteSpecialization"
              :param="instituteSpecParam"
              placeholder="التخصص المهني"
              label="التخصص المهني"
              cols="12"
              :add="false"
              :disabled="!filterInstituteEducationSystem"
              @update:model-value="onInstituteSpecializationChange"
            />
          </v-col>
        </template>

        <!-- أرقام المظروف والقاعة وسعة الطلاب وفق حافظة التسليم الرسمية -->
        <!-- رقم القاعة -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="currentEnvelope.hallNumber"
            label="رقم القاعة *"
            variant="outlined"
            density="compact"
            rounded="lg"
            class="mb-3"
            prepend-inner-icon="mdi-map-marker-outline"
            hide-details
            placeholder="مثال: قاعة 03"
            @update:model-value="generateEnvelopeBarcode"
          />
        </v-col>

        <!-- باركود / كود المظروف الامتحاني -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="currentEnvelope.envelopeCode"
            label="باركود / كود المظروف الامتحاني *"
            variant="outlined"
            density="compact"
            rounded="lg"
            class="mb-3"
            prepend-inner-icon="mdi-barcode"
            hide-details
          >
            <template #append-inner>
              <v-btn
                icon="mdi-refresh"
                variant="text"
                density="comfortable"
                size="small"
                color="primary"
                aria-label="توليد كود المظروف تلقائياً"
                title="توليد كود المظروف تلقائياً"
                @click.stop="generateEnvelopeBarcode"
                style="min-width: 32px; min-height: 32px;"
              />
            </template>
          </v-text-field>
        </v-col>

        <!-- سعة القاعة المقيدة (الطلاب المقيدون) -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model.number="currentEnvelope.expectedCount"
            type="number"
            min="0"
            max="1000"
            label="سعة القاعة المقيدة (الطلاب المقيدون) *"
            variant="outlined"
            density="compact"
            rounded="lg"
            class="mb-3"
            prepend-inner-icon="mdi-account-group-outline"
            hide-details
          />
        </v-col>

        <!-- عدد الغائبين (وفق حافظة الكشف) -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model.number="currentEnvelope.absentCount"
            type="number"
            min="0"
            :max="currentEnvelope.expectedCount"
            label="عدد الغائبين (وفق حافظة الكشف) *"
            variant="outlined"
            density="compact"
            rounded="lg"
            class="mb-3"
            prepend-inner-icon="mdi-account-remove-outline"
            color="warning"
            hide-details
          />
        </v-col>

        <!-- أزرار التحكم والتصفية والتفريغ (بنفس هوية students-master) -->
        <v-col cols="12" class="d-flex align-center justify-end gap-2 mb-3">
          <custom-btn
            type="show"
            label="تصفية النتائج"
            color="primary"
            icon="mdi-filter"
            class="font-weight-bold px-5"
            :click="fetchExamDetails"
          />
          <custom-btn
            type="cancel_filter"
            label="تفريغ الفلاتر"
            color="error"
            variant="tonal"
            icon="mdi-filter-off"
            class="font-weight-bold"
            :click="resetAllFilters"
          />
        </v-col>
      </v-row>

      <!-- ── معادلة مطابقة القاعة والمطلوب سحبه (تصميم رسمي بخلايا منظمة وهادئة) ── -->
      <div class="d-flex align-center justify-space-between flex-wrap gap-2 pa-2.5 mt-3 rounded-lg border bg-surface">
        <div class="d-flex align-center flex-wrap gap-2">
          <span class="text-caption font-weight-bold text-medium-emphasis me-1 d-flex align-center gap-1">
            <v-icon size="16" color="primary">mdi-calculator-variant-outline</v-icon>
            معادلة المطابقة:
          </span>

          <div class="d-flex align-center gap-1.5 flex-wrap audit-equation-strip">
            <!-- مقيد -->
            <div class="audit-cell">
              <span class="cell-label">المقيدون:</span>
              <span class="cell-val font-mono text-high-emphasis">{{ currentEnvelope.expectedCount }}</span>
            </div>

            <span class="text-medium-emphasis font-weight-bold mx-0.5">=</span>

            <!-- ورقة حاضرة -->
            <div class="audit-cell">
              <span class="cell-label text-success">الحضور:</span>
              <span class="cell-val font-mono text-success">{{ expectedPresentSheets }} ورقة</span>
            </div>

            <span class="text-medium-emphasis font-weight-bold mx-0.5">+</span>

            <!-- طالب غائب -->
            <div class="audit-cell">
              <span class="cell-label text-medium-emphasis">الغياب:</span>
              <span class="cell-val font-mono text-medium-emphasis">{{ currentEnvelope.absentCount }}</span>
            </div>
          </div>
        </div>

        <!-- المطلوب سحبه من الماسح -->
        <div class="d-flex align-center gap-1.5 px-3 py-1.5 rounded border" style="background: rgba(var(--v-theme-surface-variant), 0.08);">
          <v-icon size="16" color="primary">mdi-tray-arrow-down</v-icon>
          <span class="text-caption text-medium-emphasis font-weight-bold">المطلوب سحبه:</span>
          <span class="font-mono font-weight-bold text-primary">{{ expectedPresentSheets }} ورقة</span>
        </div>
      </div>
    </filter-fields>

          <!-- ── 2. ملقم تغذية أوراق المظروف من الماسح الضوئي (Scanner Feed Bay) ── -->
          <v-card class="main-card pa-4 rounded-xl border mb-4">
            <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3">
              <div class="d-flex align-center gap-2">
                <v-icon size="20" color="primary">mdi-tray-arrow-down</v-icon>
                <span class="text-subtitle-2 font-weight-black text-on-surface">
                  2. تغذية حزمة أوراق المظروف من الماسح الضوئي
                </span>
                <span class="text-caption text-medium-emphasis d-none d-sm-inline">
                  (معالجة السحب المباشر أو المجلد الساخن)
                </span>
              </div>

              <!-- خيارات ربط الماسح والمراقبة باستخدام custom-btn -->
              <div class="d-flex align-center gap-2 flex-wrap">
                <custom-btn
                  :color="hotFolderActive ? 'success' : 'grey'"
                  :variant="hotFolderActive ? 'flat' : 'tonal'"
                  :label="hotFolderActive ? 'مجلد الماسح متصل ومراقب' : 'ربط مجلد الماسح (Hot-Folder)'"
                  icon="mdi-folder-sync-outline"
                  density="comfortable"
                  class="font-weight-bold"
                  :click="toggleHotFolder"
                />

                <custom-btn
                  type="imports"
                  label="استعراض ملفات الماسح"
                  density="comfortable"
                  class="font-weight-bold"
                  :click="() => $refs.fileInput.click()"
                />
              </div>
            </div>

            <!-- مساحة إفلات وتلقيم حزمة أوراق المظروف (تصميم أنيق ومنظم ومحدد) -->
            <div
              class="upload-dropzone pa-5 rounded-xl text-center d-flex flex-column align-center justify-center transition-all cursor-pointer"
              :class="{ 'is-dragover': isDragging, 'has-file': batchFiles.length > 0 }"
              style="min-height: 150px;"
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
                <v-avatar size="52" color="primary" variant="tonal" class="mb-2 rounded-xl">
                  <v-icon size="28" color="primary">mdi-cloud-upload-outline</v-icon>
                </v-avatar>
                <div class="text-subtitle-1 font-weight-black mb-1">
                  إفلات حزمة أوراق المظروف هنا أو النقر للاستعراض
                </div>
                <div class="text-caption text-medium-emphasis mb-3" style="max-width: 600px; margin: 0 auto; line-height: 1.5;">
                  يدعم ملفات PDF متعددة الصفحات الصادرة من الماسحات الضوئية (300 DPI) أو حزم الصور
                </div>
                <div class="d-flex align-center flex-wrap gap-2 justify-center mb-1">
                  <custom-btn
                    type="imports"
                    label="استعراض واختيار ملفات المظروف"
                    icon="mdi-file-document-plus-outline"
                    density="comfortable"
                    class="font-weight-bold px-4"
                    :click="(e) => { if(e) e.stopPropagation(); $refs.fileInput.click(); }"
                  />
                </div>
                <div class="d-flex align-center justify-center flex-wrap gap-1.5 mt-2">
                  <span class="text-caption font-mono font-weight-bold px-2 py-0.5 rounded border" style="background: rgba(var(--v-theme-surface-variant), 0.1);">PDF متعدد الصفحات</span>
                  <span class="text-caption font-mono font-weight-bold px-2 py-0.5 rounded border" style="background: rgba(var(--v-theme-surface-variant), 0.1);">صور JPG / PNG</span>
                  <span class="text-caption font-mono font-weight-bold px-2 py-0.5 rounded border" style="background: rgba(var(--v-theme-surface-variant), 0.1);">أرشيف ZIP</span>
                </div>
              </template>

              <template v-else>
                <v-avatar size="56" color="success" variant="tonal" class="mb-2 rounded-2xl">
                  <v-icon size="32" color="success">mdi-file-check-outline</v-icon>
                </v-avatar>
                <div class="text-subtitle-1 font-weight-black text-success mb-1">
                  تم تجهيز {{ batchFiles.length }} ورقة / ملف تابعة للمظروف
                </div>
                <div class="text-caption text-medium-emphasis font-weight-bold mb-3">
                  الحجم الإجمالي للحزمة: {{ formatTotalSize() }} — المظروف جاهز لبدء المسح والتصحيح
                </div>
                <div class="d-flex align-center justify-center gap-2">
                  <custom-btn
                    type="del"
                    label="إلغاء الملفات"
                    density="comfortable"
                    class="font-weight-bold"
                    :click="(e) => { if(e) e.stopPropagation(); clearFiles(); }"
                  />
                  <custom-btn
                    type="add"
                    label="إضافة أوراق أخرى"
                    density="comfortable"
                    class="font-weight-bold"
                    :click="(e) => { if(e) e.stopPropagation(); $refs.fileInput.click(); }"
                  />
                </div>
              </template>
            </div>

            <!-- زر بدء التصحيح والمسح الموحد -->
            <div v-if="batchFiles.length > 0 && !isGrading" class="mt-4 text-center">
              <custom-btn
                type="ok"
                :label="`بدء المسح والتصحيح الآلي للمظروف (${batchFiles.length} ورقة) الآن`"
                color="primary"
                variant="flat"
                class="font-weight-black px-8"
                style="height: 40px; min-width: 280px;"
                :disabled="!selectedExamId"
                :click="startBatchGrading"
              />
            </div>

            <!-- شريط تقدم المعالجة وتغذية الماسح الضوئي اللحظي (Live Scanner Feed Activity) -->
            <div v-if="isGrading" class="pa-4 rounded-xl border bg-surface mt-3 shadow-sm">
              <div class="d-flex align-center justify-space-between mb-2 flex-wrap gap-2">
                <div class="d-flex align-center gap-2">
                  <v-avatar color="primary" variant="tonal" size="34" class="rounded-lg">
                    <v-progress-circular indeterminate size="20" width="2" color="primary" />
                  </v-avatar>
                  <div>
                    <div class="text-subtitle-2 font-weight-black text-primary">{{ gradingStatus }}</div>
                    <div class="text-caption text-medium-emphasis">
                      الماسح الضوئي نشط: تغذية الأوراق، قراءة الباركود والنموذج، وفحص الدوائر عبر الذكاء الاصطناعي OMR
                    </div>
                  </div>
                </div>
                <div class="d-flex align-center gap-2">
                  <span class="text-caption font-weight-bold text-medium-emphasis">نسبة المعالجة:</span>
                  <span class="font-mono font-weight-black text-primary text-subtitle-1">{{ gradingProgress }}%</span>
                </div>
              </div>
              <v-progress-linear :model-value="gradingProgress" height="8" rounded color="primary" striped active />
            </div>

            <!-- تنبيه الخطأ إن وجد -->
            <v-alert
              v-if="gradingError"
              type="error"
              variant="tonal"
              density="compact"
              class="mt-3 rounded-xl font-weight-bold"
              closable
              @click:close="gradingError = null"
            >
              {{ gradingError }}
            </v-alert>
          </v-card>

          <!-- ── 3. ميزان ومطابقة أوراق المظروف (Reconciliation Audit Strip) ── -->
          <div v-if="reconciliationCalculated" class="reconciliation-audit-card mb-3 pa-3 rounded-lg border bg-surface">
            <!-- حالة 1: مطابق ومكتمل 100% -->
            <div
              v-if="reconciliationStatus === 'BALANCED'"
              class="d-flex align-center justify-space-between flex-wrap gap-3"
            >
              <div class="d-flex align-center flex-wrap gap-2">
                <!-- شارة الحالة الرسمية -->
                <div class="audit-badge audit-badge-success d-flex align-center gap-1.5 px-3 py-1.5 rounded border">
                  <v-icon color="success" size="18">mdi-check-decagram</v-icon>
                  <span class="text-caption font-weight-bold text-success">المظروف مطابق ومكتمل:</span>
                  <span class="font-mono font-weight-bold text-success">
                    {{ actualScannedCount + currentEnvelope.absentCount }} / {{ currentEnvelope.expectedCount }} ورقة
                  </span>
                </div>

                <!-- خلايا معادلة المطابقة المنظمة -->
                <div class="d-flex align-center gap-1 flex-wrap audit-equation-strip">
                  <div class="audit-cell">
                    <span class="cell-label">المقيدون:</span>
                    <span class="cell-val font-mono">{{ currentEnvelope.expectedCount }}</span>
                  </div>
                  <span class="text-medium-emphasis font-weight-bold">=</span>
                  <div class="audit-cell">
                    <span class="cell-label">الممسوح:</span>
                    <span class="cell-val font-mono text-success">{{ actualScannedCount }}</span>
                  </div>
                  <span class="text-medium-emphasis font-weight-bold">+</span>
                  <div class="audit-cell">
                    <span class="cell-label">الغياب:</span>
                    <span class="cell-val font-mono">{{ currentEnvelope.absentCount }}</span>
                  </div>
                </div>
              </div>

              <custom-btn
                type="done"
                :label="isCommitted ? 'تم الاعتماد' : 'اعتماد وترحيل المظروف'"
                color="success"
                variant="flat"
                density="comfortable"
                class="font-weight-bold"
                :disabled="isCommitted"
                :click="commitEnvelopeToControl"
              />
            </div>

            <!-- حالة 2: عجز ونقص في الأوراق -->
            <div
              v-else-if="reconciliationStatus === 'DEFICIT'"
              class="d-flex align-center justify-space-between flex-wrap gap-3"
            >
              <div class="d-flex align-center flex-wrap gap-2">
                <!-- شارة التنبيه الرسمية -->
                <div class="audit-badge audit-badge-error d-flex align-center gap-1.5 px-3 py-1.5 rounded border">
                  <v-icon color="error" size="18">mdi-alert-circle-outline</v-icon>
                  <span class="text-caption font-weight-bold text-error">تنبيه عجز:</span>
                  <span class="font-mono font-weight-bold text-error">
                    نقص ({{ discrepancyAmount }}) ورقة مفقودة
                  </span>
                </div>

                <!-- خلايا معادلة المطابقة المنظمة -->
                <div class="d-flex align-center gap-1 flex-wrap audit-equation-strip">
                  <div class="audit-cell">
                    <span class="cell-label">سعة القاعة:</span>
                    <span class="cell-val font-mono">{{ currentEnvelope.expectedCount }}</span>
                  </div>
                  <span class="text-medium-emphasis font-weight-bold">=</span>
                  <div class="audit-cell">
                    <span class="cell-label">الممسوح:</span>
                    <span class="cell-val font-mono text-error">{{ actualScannedCount }}</span>
                  </div>
                  <span class="text-medium-emphasis font-weight-bold">+</span>
                  <div class="audit-cell">
                    <span class="cell-label">الغياب:</span>
                    <span class="cell-val font-mono">{{ currentEnvelope.absentCount }}</span>
                  </div>
                </div>

                <!-- الملاحظة التوجيهية الرسمية -->
                <div class="audit-note d-flex align-center gap-1 px-2 py-1 rounded text-caption text-error font-weight-medium">
                  <v-icon size="14" color="error">mdi-information-outline</v-icon>
                  <span>(يرجى فحص سلة الماسح أو المظروف)</span>
                </div>
              </div>

              <custom-btn
                type="del"
                label="تحرير محضر عجز مظروف"
                color="error"
                variant="tonal"
                density="comfortable"
                class="font-weight-bold"
                :click="openDiscrepancyReport"
              />
            </div>

            <!-- حالة 3: فائض وزيادة غير مبررة -->
            <div
              v-else-if="reconciliationStatus === 'SURPLUS'"
              class="d-flex align-center justify-space-between flex-wrap gap-3"
            >
              <div class="d-flex align-center flex-wrap gap-2">
                <!-- شارة التنبيه الرسمية -->
                <div class="audit-badge audit-badge-warning d-flex align-center gap-1.5 px-3 py-1.5 rounded border">
                  <v-icon color="warning" size="18">mdi-alert-outline</v-icon>
                  <span class="text-caption font-weight-bold text-warning">تنبيه فائض:</span>
                  <span class="font-mono font-weight-bold text-warning">
                    زيادة {{ Math.abs(discrepancyAmount) }} ورقة
                  </span>
                </div>

                <!-- خلايا معادلة المطابقة المنظمة -->
                <div class="d-flex align-center gap-1 flex-wrap audit-equation-strip">
                  <div class="audit-cell">
                    <span class="cell-label">سعة القاعة:</span>
                    <span class="cell-val font-mono">{{ currentEnvelope.expectedCount }}</span>
                  </div>
                  <v-divider vertical class="mx-1" style="height: 16px;" />
                  <div class="audit-cell">
                    <span class="cell-label">الممسوح + الغياب:</span>
                    <span class="cell-val font-mono text-warning">{{ actualScannedCount + currentEnvelope.absentCount }}</span>
                  </div>
                </div>

                <!-- الملاحظة التوجيهية -->
                <div class="audit-note d-flex align-center gap-1 px-2 py-1 rounded text-caption text-medium-emphasis">
                  <v-icon size="14" color="medium-emphasis">mdi-information-outline</v-icon>
                  <span>(يرجى فحص سلة الماسح أو المظروف)</span>
                </div>
              </div>

              <custom-btn
                type="show"
                label="مراجعة الرزمة"
                color="warning"
                variant="tonal"
                density="comfortable"
                class="font-weight-bold"
                :click="openDiscrepancyReport"
              />
            </div>
          </div>

          <!-- ── 4. مركز التحكم والمتابعة الموحد للمظروف (Unified Envelope Control Console) ── -->
          <v-card class="main-card rounded-2xl border mb-5 overflow-hidden shadow-sm bg-surface">
            <!-- شريط رأس الكونسول والمؤشرات السريعة -->
            <div class="pa-4 border-b d-flex align-center justify-space-between flex-wrap gap-3" style="background: rgba(var(--v-theme-surface-variant), 0.12);">
              <div class="d-flex align-center flex-wrap gap-2">
                <v-avatar color="primary" variant="tonal" size="36" class="rounded-lg">
                  <v-icon size="20" color="primary">mdi-view-dashboard-outline</v-icon>
                </v-avatar>
                <div>
                  <div class="d-flex align-center gap-2">
                    <span class="text-subtitle-2 font-weight-bold text-on-surface">سجل ومطابقة المظروف:</span>
                    <span class="seat-number-box font-mono text-caption">
                      {{ currentEnvelope.envelopeCode || 'لم يُحدد كود المظروف بعد' }}
                    </span>
                  </div>
                  <div class="text-caption text-medium-emphasis">
                    {{ currentEnvelope.examCenter || 'المركز الامتحاني' }} — {{ currentEnvelope.hallNumber || 'القاعة' }}
                  </div>
                </div>
              </div>

              <!-- مؤشرات سريعة وأزرار الإجراءات -->
              <div class="d-flex align-center flex-wrap gap-2">
                <!-- متوسط درجات القاعة -->
                <v-chip
                  v-if="displaySheets.length > 0"
                  size="small"
                  color="indigo"
                  variant="tonal"
                  class="font-weight-bold"
                >
                  <v-icon start size="14">mdi-chart-line</v-icon>
                  متوسط القاعة: {{ currentEnvelopeAvgScore }}%
                </v-chip>

                <!-- زر مراجعة وتدقيق إن وجد أوراق تحتاج تدقيق -->
                <custom-btn
                  v-if="needsReviewSheets.length > 0"
                  type="show"
                  :label="`مراجعة وتدقيق (${needsReviewSheets.length})`"
                  color="warning"
                  variant="tonal"
                  density="comfortable"
                  class="font-weight-bold"
                  :click="() => $router.push(`/omr-human-review?exam=${selectedExamId}`)"
                />

                <custom-btn
                  type="add"
                  label="المظروف التالي"
                  color="success"
                  variant="outlined"
                  density="comfortable"
                  class="font-weight-bold px-4"
                  :click="prepareNextEnvelope"
                />
              </div>
            </div>

            <!-- تبويبات العرض الموحدة والمتزامنة -->
            <v-tabs v-model="activeConsoleTab" color="primary" density="comfortable" class="border-b px-4 bg-surface">
              <!-- تبويب 1: الأوراق الممسوحة بالمظروف -->
              <v-tab value="scanned" class="font-weight-bold">
                <v-icon start size="18">mdi-file-document-check-outline</v-icon>
                الأوراق الممسوحة بالمظروف
                <v-chip size="x-small" color="primary" variant="tonal" class="ms-2 font-weight-black font-mono">
                  {{ displaySheets.length }}
                </v-chip>
              </v-tab>

              <!-- تبويب 2: حافظة كشف الطلاب والمطابقة اللحظية -->
              <v-tab value="roster" class="font-weight-bold">
                <v-icon start size="18">mdi-clipboard-list-outline</v-icon>
                حافظة كشف الطلاب والمطابقة
                <v-chip size="x-small" color="info" variant="tonal" class="ms-2 font-weight-black font-mono">
                  {{ registeredStudents.length }}
                </v-chip>
              </v-tab>

              <!-- تبويب 3: أوراق تحتاج تدقيق بشري -->
              <v-tab v-if="needsReviewSheets.length > 0" value="needs_review" class="font-weight-bold text-warning">
                <v-icon start size="18">mdi-alert-circle-outline</v-icon>
                أوراق تحتاج تدقيق بشري
                <v-chip size="x-small" color="warning" variant="flat" class="ms-2 font-weight-black font-mono text-white">
                  {{ needsReviewSheets.length }}
                </v-chip>
              </v-tab>
            </v-tabs>

            <v-card-text class="pa-4 bg-surface">
              <!-- ═══════════ التبويب 1: الأوراق الممسوحة بالمظروف ═══════════ -->
              <div v-if="activeConsoleTab === 'scanned'">
                <!-- في حال لم يتم سحب أي ورقة بعد -->
                <div v-if="displaySheets.length === 0" class="pa-8 text-center">
                  <v-avatar size="64" color="primary" variant="tonal" class="mb-3 rounded-2xl">
                    <v-icon size="32" color="primary">mdi-file-document-multiple-outline</v-icon>
                  </v-avatar>
                  <div class="text-subtitle-1 font-weight-bold">لا توجد أوراق ممسوحة في هذا المظروف حتى الآن</div>
                  <div class="text-caption text-medium-emphasis mb-3">
                    قم بإفلات حزمة أوراق المظروف في قسم التغذية أعلاه ثم انقر "بدء المسح والتصحيح الآلي"
                  </div>
                  <custom-btn
                    type="show"
                    label="معاينة كشف الطلاب المقيدين في القاعة"
                    density="comfortable"
                    class="font-weight-bold"
                    :click="() => activeConsoleTab = 'roster'"
                  />
                </div>

                <!-- في حال وجود أوراق ممسوحة -->
                <div v-else>
                  <!-- شريط الأدوات والخيارات: إحصائيات + تبديل طريقة العرض (جدول / شبكة بطاقات) -->
                  <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3 pa-2 rounded-xl border bg-surface">
                    <div class="d-flex align-center flex-wrap gap-2">
                      <v-chip
                        rounded="md"
                        size="small"
                        color="primary"
                        variant="tonal"
                        class="font-weight-bold font-mono px-3"
                      >
                        الممسوح: {{ displaySheets.length }} ورقة
                      </v-chip>
                      <v-chip
                        rounded="md"
                        size="small"
                        color="success"
                        variant="tonal"
                        class="font-weight-bold font-mono px-3"
                      >
                        أوراق سليمة: {{ successfulSheets.length }}
                      </v-chip>
                      <v-chip
                        rounded="md"
                        size="small"
                        color="warning"
                        variant="tonal"
                        class="font-weight-bold font-mono px-3"
                      >
                        تحتاج تدقيق: {{ needsReviewSheets.length }}
                      </v-chip>
                    </div>

                    <!-- تبديل العرض بين جدول وشبكة كروت -->
                    <div class="d-flex align-center gap-1">
                      <span class="text-caption text-medium-emphasis me-1">طريقة العرض:</span>
                      <v-btn-toggle v-model="sheetViewMode" mandatory density="compact" rounded="lg" color="primary">
                        <v-btn value="table" size="small" icon="mdi-view-headline" aria-label="عرض جدولي" title="عرض جدولي" />
                        <v-btn value="grid" size="small" icon="mdi-view-grid-outline" aria-label="عرض شبكة البطاقات" title="عرض شبكة البطاقات" />
                      </v-btn-toggle>
                    </div>
                  </div>

                  <!-- تنبيه أمني إذا تم رصد أوراق دخيلة لا تخص حافظة القاعة (تصميم هادئ رسمي) -->
                  <div
                    v-if="intruderSheets.length > 0"
                    class="official-notice-box mb-3 pa-3 rounded-lg border d-flex align-start gap-3"
                  >
                    <v-icon color="warning" size="20" class="mt-0.5 flex-shrink-0">mdi-shield-alert-outline</v-icon>
                    <div class="flex-grow-1">
                      <div class="text-caption font-weight-bold text-high-emphasis mb-1">
                        تنبيه تدقيق ومطابقة — رصد ورقة دخيلة:
                      </div>
                      <div class="text-caption text-medium-emphasis font-weight-regular" style="line-height: 1.6;">
                        تم رصد {{ intruderSheets.length }} ورقة تم مسحها ولا تتبع كشف الطلاب المقيدين في هذه القاعة (مثل رقم الجلوس: {{ intruderSheets.map(s => s.seat_number).join(', ') }}). تم عزلها تلقائياً للتدقيق البشري لحماية كنترول القاعة.
                      </div>
                    </div>
                  </div>

                  <!-- 1.1 العرض الجدولي (Table View) -->
                  <div v-if="sheetViewMode === 'table'">
                    <custom-data-table
                      v-model="selectedScannedSheets"
                      :items="scannedSheetsTableItems"
                      :getData="getScannedSheetsData"
                      :headers="scannedSheetsHeaders"
                      :hasFilter="false"
                      :log="false"
                      :restore="false"
                      :actions="false"
                      :search="false"
                      class="bg-transparent"
                    >
                      <template v-slot:item-slot="{ item, key }">
                        <!-- رقم الجلوس -->
                        <template v-if="key === 'seat_number'">
                          <span class="seat-number-box font-mono">
                            {{ item.seat_number || '—' }}
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

                        <!-- مطابقة الحافظة -->
                        <template v-else-if="key === 'roster_match'">
                          <v-chip
                            v-if="item.roster_match"
                            size="small"
                            color="success"
                            variant="tonal"
                            class="font-weight-bold"
                          >
                            <v-icon start size="14">mdi-check-circle-outline</v-icon>
                            مقيد بالقاعة
                          </v-chip>
                          <v-chip
                            v-else
                            size="small"
                            color="error"
                            variant="flat"
                            class="font-weight-bold text-white"
                          >
                            <v-icon start size="14">mdi-alert-circle</v-icon>
                            ورقة دخيلة
                          </v-chip>
                        </template>

                        <!-- الدرجة -->
                        <template v-else-if="key === 'score'">
                          <span class="font-weight-black font-mono text-body-2 text-on-surface">
                            {{ item.score != null ? item.score : 0 }} / {{ item.max_score || 40 }}
                          </span>
                        </template>

                        <!-- النسبة -->
                        <template v-else-if="key === 'percentage'">
                          <v-chip size="small" variant="tonal" color="success" class="font-weight-bold font-mono">
                            {{ item.percentage || 0 }}%
                          </v-chip>
                        </template>

                        <!-- حالة التصحيح -->
                        <template v-else-if="key === 'status'">
                          <v-chip
                            v-if="String(item.status || '').toLowerCase() === 'needs_review' || item.needs_review || item.error_message"
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
                  </div>

                  <!-- 1.2 العرض الشبكي بالبطاقات البصرية (Grid View) -->
                  <div v-else-if="sheetViewMode === 'grid'">
                    <v-row dense>
                      <v-col
                        v-for="sheet in displaySheets"
                        :key="sheet.id || sheet.filename || sheet.seat_number"
                        cols="12"
                        sm="6"
                        md="4"
                        lg="3"
                      >
                        <v-card
                          class="rounded-xl border pa-3 h-100 d-flex flex-column justify-space-between transition-all"
                          :class="{
                            'border-warning': isNeedsReview(sheet),
                            'border-success': !isNeedsReview(sheet)
                          }"
                          variant="outlined"
                          style="background: rgba(var(--v-theme-surface), 0.9);"
                        >
                          <div>
                            <div class="d-flex align-center justify-space-between mb-2">
                              <span class="seat-number-box font-mono text-caption">
                                {{ sheet.seat_number || '—' }}
                              </span>
                              <span class="text-caption font-weight-bold px-2 py-0.5 rounded border" style="background: rgba(var(--v-theme-surface-variant), 0.1);">
                                النموذج {{ sheet.model_code || 'A' }}
                              </span>
                            </div>

                            <div class="text-subtitle-2 font-weight-black text-on-surface text-truncate mb-1" :title="sheet.student_name">
                              {{ sheet.student_name || 'طالب غير محدد' }}
                            </div>

                            <div class="d-flex align-center flex-wrap gap-1 mb-2">
                              <v-chip
                                size="x-small"
                                :color="isNeedsReview(sheet) ? 'warning' : 'success'"
                                variant="flat"
                                class="font-weight-bold"
                              >
                                {{ isNeedsReview(sheet) ? 'تدقيق بشري' : 'معتمد وسليم' }}
                              </v-chip>
                              <v-chip
                                v-if="!isSheetInRoster(sheet)"
                                size="x-small"
                                color="error"
                                variant="tonal"
                                class="font-weight-bold"
                              >
                                ورقة دخيلة
                              </v-chip>
                            </div>

                            <div
                              v-if="sheet.error_message"
                              class="text-caption text-error font-weight-medium pa-1.5 rounded-lg mb-2 text-truncate"
                              style="background: rgba(var(--v-theme-error), 0.08);"
                              :title="sheet.error_message"
                            >
                              {{ sheet.error_message }}
                            </div>
                          </div>

                          <div class="d-flex align-center justify-space-between border-t pt-2 mt-2">
                            <div>
                              <span class="font-mono font-weight-black text-body-2 text-primary">
                                {{ sheet.score != null ? sheet.score : 0 }} / {{ sheet.max_score || 40 }}
                              </span>
                              <span class="text-caption text-medium-emphasis ms-1">({{ sheet.percentage || 0 }}%)</span>
                            </div>
                            <custom-btn
                              type="show"
                              label="معاينة"
                              density="compact"
                              class="font-weight-bold"
                              :click="() => openSheetPreview(sheet)"
                            />
                          </div>
                        </v-card>
                      </v-col>
                    </v-row>
                  </div>
                </div>
              </div>

              <!-- ═══════════ التبويب 2: حافظة كشف الطلاب والمطابقة اللحظية ═══════════ -->
              <div v-else-if="activeConsoleTab === 'roster'">
                <!-- شريط توضيحي يشرح فائدة كشف الحافظة ومعادلة المطابقة -->
                <div class="pa-3 mb-3 rounded-0 border bg-surface d-flex align-center justify-space-between flex-wrap gap-3">
                  <div class="d-flex align-center gap-2">
                    <v-avatar color="info" variant="tonal" size="32" class="rounded-lg">
                      <v-icon color="info" size="18">mdi-shield-account-outline</v-icon>
                    </v-avatar>
                    <div>
                      <span class="text-subtitle-2 font-weight-black text-on-surface">
                        كشف المناداة والتسليم الرسمي للقاعة: {{ currentEnvelope.envelopeCode }}
                      </span>
                      <div class="text-caption text-medium-emphasis">
                        السجل المعتمد للطلاب الـ ({{ registeredStudents.length }}) المقيدين بهذه القاعة. يتم تحديث حالة كل طالب لحظياً فور مرور ورقته عبر الماسح.
                      </div>
                    </div>
                  </div>

                  <div class="d-flex align-center flex-wrap gap-2">
                    <v-chip color="info" variant="tonal" size="small" class="font-weight-bold">
                      المقيدون: {{ registeredStudents.length }}
                    </v-chip>
                    <v-chip color="success" variant="tonal" size="small" class="font-weight-bold">
                      تم المسح: {{ rosterMatchedCount }}
                    </v-chip>
                    <v-chip color="blue-grey" variant="tonal" size="small" class="font-weight-bold">
                      بانتظار السحب: {{ Math.max(0, registeredStudents.length - rosterMatchedCount - currentEnvelope.absentCount) }}
                    </v-chip>
                    <v-chip v-if="currentEnvelope.absentCount > 0" color="warning" variant="tonal" size="small" class="font-weight-bold">
                      الغياب: {{ currentEnvelope.absentCount }}
                    </v-chip>
                  </div>
                </div>

                <div v-if="registeredStudents.length > 0">
                  <custom-data-table
                    v-model="selectedRegisteredStudents"
                    :items="regStudentsTableItems"
                    :getData="getRegStudentsData"
                    :headers="regStudentsHeaders"
                    :customLoading="loadingExams"
                    :hasFilter="false"
                    :log="false"
                    :restore="false"
                    :actions="false"
                    :search="false"
                    class="bg-transparent"
                  >
                    <template v-slot:item-slot="{ item, key }">
                      <!-- رقم الجلوس -->
                      <template v-if="key === 'seat_number'">
                        <span class="seat-number-box font-mono">
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

                      <!-- حالة سحب الورقة بالماسح (ديناميكية لحظية) -->
                      <template v-else-if="key === 'scan_status'">
                        <v-chip
                          v-if="item.scan_status === 'scanned'"
                          size="small"
                          color="success"
                          variant="tonal"
                          class="font-weight-bold"
                        >
                          <v-icon start size="14">mdi-check-decagram</v-icon>
                          تم المسح والتصحيح
                        </v-chip>
                        <v-chip
                          v-else-if="item.scan_status === 'needs_review'"
                          size="small"
                          color="warning"
                          variant="flat"
                          class="font-weight-bold"
                        >
                          <v-icon start size="14">mdi-alert-circle</v-icon>
                          تم المسح - تدقيق بشري
                        </v-chip>
                        <v-chip
                          v-else-if="item.scan_status === 'missing'"
                          size="small"
                          color="error"
                          variant="flat"
                          class="font-weight-bold text-white"
                        >
                          <v-icon start size="14">mdi-help-rhombus-outline</v-icon>
                          ورقة مفقودة (عجز)
                        </v-chip>
                        <v-chip
                          v-else
                          size="small"
                          color="blue-grey"
                          variant="tonal"
                          class="font-weight-bold"
                        >
                          <v-icon start size="14">mdi-clock-outline</v-icon>
                          بانتظار سحب الورقة
                        </v-chip>
                      </template>

                      <!-- النتيجة والدرجة المحسوبة -->
                      <template v-else-if="key === 'student_score'">
                        <span v-if="item.matchedSheet" class="font-weight-black font-mono text-body-2 text-primary">
                          {{ item.matchedSheet.score != null ? item.matchedSheet.score : 0 }} / {{ item.matchedSheet.max_score || 40 }}
                        </span>
                        <span v-else class="text-caption text-medium-emphasis">—</span>
                      </template>

                      <!-- إجراءات المعاينة -->
                      <template v-else-if="key === 'actions'">
                        <custom-btn
                          v-if="item.matchedSheet"
                          is-icon
                          type="show"
                          label="معاينة الورقة الممسوحة"
                          :click="() => openSheetPreview(item.matchedSheet)"
                        />
                        <span v-else class="text-caption text-disabled">—</span>
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
              </div>

              <!-- ═══════════ التبويب 3: أوراق تحتاج تدقيق بشري ═══════════ -->
              <div v-else-if="activeConsoleTab === 'needs_review'">
                <div class="pa-3 mb-3 rounded-xl border bg-surface d-flex align-center justify-space-between flex-wrap gap-2">
                  <div class="d-flex align-center gap-2">
                    <v-avatar color="warning" variant="tonal" size="32" class="rounded-lg">
                      <v-icon color="warning" size="18">mdi-alert-octagon-outline</v-icon>
                    </v-avatar>
                    <div>
                      <span class="text-subtitle-2 font-weight-black text-warning">
                        أوراق معزولة تتطلب تدقيقاً بشرياً ({{ needsReviewSheets.length }} ورقة)
                      </span>
                      <div class="text-caption text-medium-emphasis">
                        تم عزل هذه الأوراق لحماية درجات المظروف نظراً لوجود أوراق من اختبار آخر، أو باركود غير مقروء، أو تظليلات ملتبسة.
                      </div>
                    </div>
                  </div>

                  <custom-btn
                    type="show"
                    label="فتح شاشة التدقيق البشري الشاملة"
                    color="warning"
                    variant="tonal"
                    density="comfortable"
                    class="font-weight-bold"
                    :click="() => $router.push(`/omr-human-review?exam=${selectedExamId}`)"
                  />
                </div>

                <custom-data-table
                  v-model="selectedNeedsReviewSheets"
                  :items="needsReviewTableItems"
                  :getData="getNeedsReviewData"
                  :headers="needsReviewHeaders"
                  :hasFilter="false"
                  :log="false"
                  :restore="false"
                  :actions="false"
                  :search="false"
                  class="bg-transparent"
                >
                  <template v-slot:item-slot="{ item, key }">
                    <template v-if="key === 'seat_number'">
                      <span class="seat-number-box font-mono">
                        {{ item.seat_number || '—' }}
                      </span>
                    </template>
                    <template v-else-if="key === 'student_name'">
                      <span class="font-weight-bold text-body-2 text-on-surface">{{ item.student_name || 'طالب غير محدد' }}</span>
                    </template>
                    <template v-else-if="key === 'model_code'">
                      <v-chip size="small" variant="tonal" color="primary" class="font-weight-bold">
                        النموذج {{ item.model_code || 'A' }}
                      </v-chip>
                    </template>
                    <template v-else-if="key === 'error_message'">
                      <span class="text-caption font-weight-bold text-error" style="line-height: 1.5;">
                        {{ item.error_message || 'مطلوب تدقيق بشري للورقة' }}
                      </span>
                    </template>
                    <template v-else-if="key === 'actions'">
                      <custom-btn
                        type="show"
                        label="معاينة وتدقيق"
                        density="compact"
                        class="font-weight-bold"
                        :click="() => openSheetPreview(item)"
                      />
                    </template>
                  </template>
                </custom-data-table>
              </div>
            </v-card-text>
          </v-card>


    <!-- ── نافذة معاينة ورقة الطالب (Sheet Details Dialog) ── -->
    <v-dialog v-model="previewDialog" max-width="1100px" scrollable>
      <v-card v-if="activePreviewSheet" class="rounded-2xl overflow-hidden main-card bg-surface">
        <!-- Dialog Header -->
        <v-card-title class="d-flex align-center justify-space-between bg-surface px-6 py-4 border-b">
          <div class="d-flex align-center gap-3">
            <v-avatar color="primary" variant="tonal" rounded="lg" size="42">
              <v-icon size="22" color="primary">mdi-file-document-check-outline</v-icon>
            </v-avatar>
            <div>
              <h3 class="text-h6 font-weight-black text-on-surface mb-0">
                {{ activePreviewSheet.student_name || 'ورقة طالب بدون اسم' }}
              </h3>
              <p class="text-caption text-medium-emphasis mb-0 mt-0.5">
                تفاصيل ورقة إجابة الطالب وتدقيق دوائر الماسح الضوئي (OMR)
              </p>
            </div>
          </div>
          <v-btn
            icon="mdi-close"
            variant="text"
            size="small"
            color="medium-emphasis"
            aria-label="إغلاق المعاينة"
            title="إغلاق المعاينة"
            @click="previewDialog = false"
          />
        </v-card-title>

        <!-- ── شريط بيانات ورقة الطالب: مربعات رسمية متناسقة وهادئة ── -->
        <div class="d-flex align-center flex-wrap gap-2 px-6 py-3 bg-surface border-b official-meta-strip">
          <!-- رقم الجلوس -->
          <div class="official-meta-box">
            <span class="meta-label">رقم الجلوس</span>
            <span class="meta-val font-mono">{{ activePreviewSheet.seat_number || '—' }}</span>
          </div>

          <!-- نموذج الأسئلة -->
          <div class="official-meta-box">
            <span class="meta-label">النموذج</span>
            <span class="meta-val font-mono">{{ activePreviewSheet.model_code || 'A' }}</span>
          </div>

          <!-- حالة التدقيق والاعتماد -->
          <div
            class="official-meta-box"
            :class="isNeedsReview(activePreviewSheet) ? 'status-box-warning' : 'status-box-success'"
          >
            <span class="meta-label">الحالة</span>
            <span class="meta-val d-flex align-center gap-1">
              <v-icon size="14">
                {{ isNeedsReview(activePreviewSheet) ? 'mdi-alert-circle-outline' : 'mdi-check-circle-outline' }}
              </v-icon>
              {{ isNeedsReview(activePreviewSheet) ? 'يحتاج تدقيق' : 'معتمد وسليم' }}
            </span>
          </div>

          <!-- الدرجة المحسوبة -->
          <div class="official-meta-box">
            <span class="meta-label">الدرجة المحسوبة</span>
            <span class="meta-val font-mono">
              {{ activePreviewSheet.score != null ? activePreviewSheet.score : 0 }} / {{ activePreviewSheet.max_score != null ? activePreviewSheet.max_score : ((activePreviewSheet.questions || []).length || 50) }}
              <span class="text-caption font-weight-medium text-medium-emphasis ms-1">({{ activePreviewSheet.percentage }}%)</span>
            </span>
          </div>

          <!-- تفصيل الأسئلة والإجابات كمربع مدمج ومتناسق -->
          <div class="official-meta-box official-meta-stats-box">
            <div class="d-flex align-center gap-3">
              <div>
                <span class="meta-label">الأسئلة</span>
                <span class="meta-val font-mono">{{ (activePreviewSheet.questions || []).length }}</span>
              </div>
              <v-divider vertical class="mx-1" style="height: 22px;" />
              <div>
                <span class="meta-label text-success">صحيحة</span>
                <span class="meta-val font-mono text-success">{{ previewCounts.correct }}</span>
              </div>
              <v-divider vertical class="mx-1" style="height: 22px;" />
              <div>
                <span class="meta-label text-error">خاطئة</span>
                <span class="meta-val font-mono text-error">{{ previewCounts.wrong }}</span>
              </div>
              <v-divider vertical class="mx-1" style="height: 22px;" />
              <div>
                <span class="meta-label text-medium-emphasis">لم يُجب</span>
                <span class="meta-val font-mono text-medium-emphasis">{{ previewCounts.empty }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- تنبيه تفصيلي عند وجود خطأ في مطابقة الطالب أو الاختبار (تصميم هادئ رسمي) -->
        <div
          v-if="activePreviewSheet.error_message"
          class="official-notice-box mx-4 mt-3 mb-1 pa-3 rounded-lg border d-flex align-start gap-3"
        >
          <v-icon color="warning" size="20" class="mt-0.5 flex-shrink-0">mdi-alert-circle-outline</v-icon>
          <div class="flex-grow-1">
            <div class="text-caption font-weight-bold text-high-emphasis mb-1">
              تنبيه تدقيق ومطابقة الورقة:
            </div>
            <div class="text-caption text-medium-emphasis font-weight-regular" style="white-space: pre-wrap; line-height: 1.6;">
              {{ activePreviewSheet.error_message }}
            </div>
          </div>
        </div>

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
            <div v-if="!activePreviewSheet.annotated_url && !activePreviewSheet.aligned_image && !activePreviewSheet.image_url && !activePreviewSheet.original_image" class="py-12 text-medium-emphasis">
              <v-icon size="48" color="medium-emphasis" class="mb-2">mdi-image-off-outline</v-icon>
              <div class="text-subtitle-1 font-weight-bold">لا توجد صورة متوفرة لورقة هذا الطالب</div>
              <div class="text-caption">تم تسجيل بيانات التصحيح الضوئي مباشرة بدون تخزين الصورة النقطية</div>
            </div>
            <template v-else>
              <v-img 
                :src="resolveImageUrl(activePreviewSheet.annotated_url || activePreviewSheet.aligned_image || activePreviewSheet.image_url || activePreviewSheet.original_image)" 
                max-height="600" 
                contain 
                class="rounded-xl border bg-grey-lighten-4" 
              >
                <template v-slot:placeholder>
                  <div class="d-flex align-center justify-center fill-height">
                    <v-progress-circular indeterminate color="primary" />
                  </div>
                </template>
                <template v-slot:error>
                  <div class="py-8 text-medium-emphasis">
                    <v-icon size="36" color="warning" class="mb-2">mdi-alert-circle-outline</v-icon>
                    <div class="text-caption">تعذر تحميل ملف الصورة من المسار:</div>
                    <div class="text-caption font-mono text-primary mt-1">{{ resolveImageUrl(activePreviewSheet.annotated_url || activePreviewSheet.aligned_image || activePreviewSheet.image_url || activePreviewSheet.original_image) }}</div>
                  </div>
                </template>
              </v-img>
              <div class="text-caption text-medium-emphasis mt-3 font-weight-bold">
                * الحلقات الملونة توضح مواضع كافة الدوائر التي فحصها المحرك بدقة بالذكاء الاصطناعي ومستوى الكثافة الضوئية.
              </div>
            </template>
          </div>

          <!-- عرض الورقة الممسوحة الأصلية -->
          <div v-else-if="previewMode === 'original'" class="text-center pa-4 border rounded-2xl mb-2 bg-surface">
            <div v-if="!activePreviewSheet.image_url && !activePreviewSheet.original_image" class="py-12 text-medium-emphasis">
              <v-icon size="48" color="medium-emphasis" class="mb-2">mdi-image-off-outline</v-icon>
              <div class="text-subtitle-1 font-weight-bold">لا توجد صورة أصلية متوفرة</div>
            </div>
            <v-img 
              v-else 
              :src="resolveImageUrl(activePreviewSheet.image_url || activePreviewSheet.original_image)" 
              max-height="600" 
              contain 
              class="rounded-xl border bg-grey-lighten-4"
            >
              <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height">
                  <v-progress-circular indeterminate color="primary" />
                </div>
              </template>
              <template v-slot:error>
                <div class="py-8 text-medium-emphasis">
                  <v-icon size="36" color="warning" class="mb-2">mdi-alert-circle-outline</v-icon>
                  <div class="text-caption">تعذر تحميل الصورة الأصلية من المسار:</div>
                  <div class="text-caption font-mono text-primary mt-1">{{ resolveImageUrl(activePreviewSheet.image_url || activePreviewSheet.original_image) }}</div>
                </div>
              </template>
            </v-img>
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
import settings from '../../../settings'
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

    const orgFieldLabel = computed(() => {
      if (filterInstitutionType.value === 'university') return 'الجامعة / الكلية'
      if (filterInstitutionType.value === 'institute') return 'المعهد / المركز التدريبي'
      return 'المدرسة / المركز الامتحاني'
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

    const resetAllFilters = () => {
      filterInstitutionType.value = 'all'
      filterGovernorate.value = null
      filterDirectorate.value = null
      filterOrganization.value = null
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
      selectedExamId.value = null
      batchFiles.value = []
      batchResult.value = null
      gradingError.value = null
      isCommitted.value = false
      currentEnvelope.expectedCount = 0
      currentEnvelope.absentCount = 0
      currentEnvelope.envelopeCode = ''
      registeredStudents.value = []
      activeConsoleTab.value = 'roster'
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
      const qs = activePreviewSheet.value?.questions || activePreviewSheet.value?.omr_result || []
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

      const rawQuestions = activePreviewSheet.value?.questions || activePreviewSheet.value?.omr_result || []
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

    const resolveImageUrl = (path) => {
      if (!path) return ''
      if (typeof path !== 'string') return ''
      if (path.startsWith('data:') || path.startsWith('blob:')) {
        return path
      }
      let finalUrl = path
      if (path.startsWith('http://') || path.startsWith('https://')) {
        try {
          const u = new URL(path)
          if (u.pathname.startsWith('/media/')) {
            finalUrl = u.pathname
          }
        } catch (e) {}
      } else {
        finalUrl = path.startsWith('/') ? path : `/${path}`
      }

      const token = localStorage.getItem('token') || sessionStorage.getItem('token') || localStorage.getItem('access_token')
      if (token && finalUrl.startsWith('/media/')) {
        const sep = finalUrl.includes('?') ? '&' : '?'
        return `${finalUrl}${sep}token=${encodeURIComponent(token)}`
      }
      return finalUrl
    }

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

    const isNeedsReview = (s) => {
      const st = String(s?.status || '').toLowerCase()
      return st === 'needs_review' || Boolean(s?.needs_review) || Boolean(s?.error_message)
    }

    const successfulSheets = computed(() => {
      return displaySheets.value.filter((s) => !isNeedsReview(s))
    })

    const needsReviewSheets = computed(() => {
      return displaySheets.value.filter((s) => isNeedsReview(s))
    })

    const currentEnvelopeAvgScore = computed(() => {
      if (!displaySheets.value.length) return 0
      const total = displaySheets.value.reduce((acc, s) => acc + (s.percentage || 0), 0)
      return Math.round(total / displaySheets.value.length)
    })

    // ── Unified Envelope Console: Tab Navigation & View Mode ──
    const activeConsoleTab = ref('roster')
    const sheetViewMode = ref('table')

    const isSheetInRoster = (sheet) => {
      if (!sheet || !sheet.seat_number) return false
      const sStr = String(sheet.seat_number).trim()
      return (registeredStudents.value || []).some(
        (r) => String(r.seat_number || '').trim() === sStr
      )
    }

    const rosterMatchedCount = computed(() => {
      if (!registeredStudents.value.length || !displaySheets.value.length) return 0
      const scannedSeats = new Set(displaySheets.value.map((s) => String(s.seat_number || '').trim()))
      return registeredStudents.value.filter((r) => scannedSeats.has(String(r.seat_number || '').trim())).length
    })

    const intruderSheets = computed(() => {
      if (!displaySheets.value.length) return []
      const regSeats = new Set((registeredStudents.value || []).map((s) => String(s.seat_number || '').trim()))
      return displaySheets.value.filter((s) => s.seat_number && !regSeats.has(String(s.seat_number).trim()))
    })

    // Selection arrays for CustomDataTable (matching review-queue)
    const selectedScannedSheets = ref([])
    const selectedRegisteredStudents = ref([])
    const selectedNeedsReviewSheets = ref([])

    // ── Table 1: Registered Students Manifest (الحافظة الرسمية) ──
    const regStudentsHeaders = ref([
      { title: 'رقم الجلوس', key: 'seat_number', sortable: true, width: '130px' },
      { title: 'اسم الطالب المقيد بالحافظة', key: 'student_name', sortable: true },
      { title: 'النموذج المخصص', key: 'model_code', sortable: false, width: '120px', align: 'center' },
      { title: 'المدرسة / المركز', key: 'school_name', sortable: false },
      { title: 'حالة سحب الورقة بالماسح', key: 'scan_status', sortable: false, width: '200px', align: 'center' },
      { title: 'النتيجة', key: 'student_score', sortable: false, width: '110px', align: 'center' },
      { title: 'معاينة', key: 'actions', sortable: false, width: '80px', align: 'center' },
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

      const raw = registeredStudents.value || []
      const sheets = displaySheets.value || []

      const all = raw.map((student, idx) => {
        const sSeat = String(student.seat_number || '').trim()
        const matched = sheets.find((s) => String(s.seat_number || '').trim() === sSeat)
        let status = 'waiting'
        if (matched) {
          if (String(matched.status || '').toLowerCase() === 'needs_review' || matched.needs_review || matched.error_message) {
            status = 'needs_review'
          } else {
            status = 'scanned'
          }
        } else if (sheets.length > 0) {
          status = 'missing'
        }
        return {
          id: student.id || student.seat_number || `reg_${idx}`,
          ...student,
          matchedSheet: matched || null,
          scan_status: status,
        }
      })

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

    // ── Table 2: Scanned Sheets (الأوراق الممسوحة بالمظروف) ──
    const scannedSheetsHeaders = ref([
      { title: 'رقم الجلوس', key: 'seat_number', sortable: true, width: '120px' },
      { title: 'اسم الطالب', key: 'student_name', sortable: true },
      { title: 'نموذج الأسئلة', key: 'model_code', sortable: false, width: '110px', align: 'center' },
      { title: 'المطابقة مع الحافظة', key: 'roster_match', sortable: false, width: '150px', align: 'center' },
      { title: 'الدرجة المحسوبة', key: 'score', sortable: true, width: '120px', align: 'center' },
      { title: 'النسبة المئوية', key: 'percentage', sortable: true, width: '110px', align: 'center' },
      { title: 'حالة التصحيح', key: 'status', sortable: true, width: '130px', align: 'center' },
      { title: 'المعاينة', key: 'actions', sortable: false, width: '80px', align: 'center' },
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

      const regSeats = new Set((registeredStudents.value || []).map((s) => String(s.seat_number || '').trim()))
      const all = (displaySheets.value || []).map((s, idx) => ({
        id: s.id || s.seat_number || s.filename || `scan_${idx}`,
        ...s,
        roster_match: Boolean(s.seat_number && regSeats.has(String(s.seat_number).trim())),
      }))

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

    // ── Table 3: Needs Review Sheets (الأوراق المعزولة للتدقيق البشري) ──
    const needsReviewHeaders = ref([
      { title: 'رقم الجلوس', key: 'seat_number', sortable: true, width: '130px' },
      { title: 'اسم الطالب', key: 'student_name', sortable: true },
      { title: 'النموذج', key: 'model_code', sortable: false, width: '100px', align: 'center' },
      { title: 'سبب العزل والتدقيق', key: 'error_message', sortable: false },
      { title: 'المعاينة والتدقيق', key: 'actions', sortable: false, width: '130px', align: 'center' },
    ])

    const needsReviewPage = ref(1)
    const needsReviewPageSize = ref(10)
    const needsReviewTableItems = ref({
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

    const getNeedsReviewData = async (params = {}) => {
      const p = params?.params || params || {}
      const page = Number(p.page) || needsReviewPage.value || 1
      const pageSize = Number(p.page_size || p.perPage) || needsReviewPageSize.value || 10
      needsReviewPage.value = page
      needsReviewPageSize.value = pageSize

      const all = (needsReviewSheets.value || []).map((s, idx) => ({
        id: s.id || s.seat_number || s.filename || `rev_${idx}`,
        ...s,
      }))
      const total = all.length
      const numPages = Math.ceil(total / pageSize) || 1
      const validPage = Math.min(Math.max(1, page), numPages)
      const start = (validPage - 1) * pageSize

      needsReviewTableItems.value = {
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
      return needsReviewTableItems.value
    }

    watch([displaySheets, registeredStudents], () => {
      scannedSheetsPage.value = 1
      regStudentsPage.value = 1
      needsReviewPage.value = 1
      getScannedSheetsData({ page: 1, page_size: scannedSheetsPageSize.value })
      getRegStudentsData({ page: 1, page_size: regStudentsPageSize.value })
      getNeedsReviewData({ page: 1, page_size: needsReviewPageSize.value })
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
      activeConsoleTab.value = 'roster'
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
      activeConsoleTab.value = 'roster'
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
        activeConsoleTab.value = 'scanned'
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
        console.error('Dispatch API call failed:', err)
        isCommitted.value = false
        const msg = err.response?.data?.message || err.message || 'حدث خطأ أثناء ترحيل المظروف لنظام الكنترول'
        alert(`فشل اعتماد المظروف وترحيله للكنترول:\n${msg}`)
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
      const img = sheet?.image_url || sheet?.original_image || ''
      const ann = sheet?.annotated_url || sheet?.aligned_image || img
      activePreviewSheet.value = {
        ...sheet,
        image_url: img,
        annotated_url: ann,
        questions: sheet?.questions || sheet?.omr_result || [],
      }
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
      orgFieldLabel,
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
      resetAllFilters,
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
      // Unified Console & Views
      activeConsoleTab,
      sheetViewMode,
      rosterMatchedCount,
      intruderSheets,
      isSheetInRoster,
      isNeedsReview,
      // Tables & KPIs
      displaySheets,
      successfulSheets,
      needsReviewSheets,
      currentEnvelopeAvgScore,
      selectedScannedSheets,
      selectedRegisteredStudents,
      selectedNeedsReviewSheets,
      regStudentsHeaders,
      regStudentsTableItems,
      getRegStudentsData,
      scannedSheetsHeaders,
      scannedSheetsTableItems,
      getScannedSheetsData,
      needsReviewHeaders,
      needsReviewTableItems,
      getNeedsReviewData,
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
      resolveImageUrl,
    }
  },
}
</script>

<style scoped>
.qb-national-control-console {
  direction: rtl;
}

/* ── Glassmorphic Summary Boxes ────────────────────────────── */
.summary-glass-box {
  background: rgba(var(--v-theme-surface-variant), 0.16);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(var(--v-border-color), 0.28) !important;
  transition: all 0.2s ease;
}
.summary-glass-box:hover {
  background: rgba(var(--v-theme-surface-variant), 0.26);
  border-color: rgba(var(--v-theme-primary), 0.35) !important;
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

/* ── Natural Seat Number Box (Official Standard) ───────────── */
.seat-number-box {
  display: inline-block;
  padding: 2px 8px;
  font-weight: 700;
  font-size: 0.88rem;
  color: rgb(var(--v-theme-on-surface));
  background: rgba(var(--v-theme-surface-variant), 0.12);
  border: 1px solid rgba(var(--v-border-color), 0.35);
  border-radius: 4px;
  letter-spacing: 0.5px;
  min-width: 64px;
  text-align: center;
}

/* ── Reconciliation Audit Panel ────────────────────────────── */
.reconciliation-audit-card {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.audit-badge {
  background: rgba(var(--v-theme-surface-variant), 0.12);
  border-color: rgba(var(--v-border-color), 0.3) !important;
}

.audit-badge-success {
  background: rgba(var(--v-theme-success), 0.08);
  border-color: rgba(var(--v-theme-success), 0.35) !important;
}

.audit-badge-error {
  background: rgba(var(--v-theme-error), 0.08);
  border-color: rgba(var(--v-theme-error), 0.35) !important;
}

.audit-badge-warning {
  background: rgba(var(--v-theme-warning), 0.08);
  border-color: rgba(var(--v-theme-warning), 0.35) !important;
}

.audit-equation-strip {
  background: rgba(var(--v-theme-surface-variant), 0.06);
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid rgba(var(--v-border-color), 0.2);
}

.audit-cell {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 6px;
  font-size: 0.82rem;
}

.audit-cell .cell-label {
  color: rgba(var(--v-theme-on-surface), 0.7);
  font-weight: 600;
}

.audit-cell .cell-val {
  font-weight: 700;
}

.audit-note {
  background: rgba(var(--v-theme-surface-variant), 0.05);
}

/* ── Official Meta Strip & Boxes for Details Dialog ────────── */
.official-meta-strip {
  background: rgba(var(--v-theme-surface-variant), 0.04);
}

.official-meta-box {
  display: inline-flex;
  flex-direction: column;
  justify-content: center;
  min-width: 85px;
  padding: 5px 12px;
  background: rgba(var(--v-theme-surface-variant), 0.08);
  border: 1px solid rgba(var(--v-border-color), 0.28);
  border-radius: 6px;
  transition: all 0.2s ease;
}

.official-meta-box .meta-label {
  font-size: 0.72rem;
  color: rgba(var(--v-theme-on-surface), 0.6);
  font-weight: 600;
  line-height: 1.2;
  margin-bottom: 2px;
}

.official-meta-box .meta-val {
  font-size: 0.9rem;
  color: rgb(var(--v-theme-on-surface));
  font-weight: 700;
  line-height: 1.3;
}

.status-box-warning {
  border-color: rgba(var(--v-theme-warning), 0.5) !important;
  background: rgba(var(--v-theme-warning), 0.06) !important;
}

.status-box-success {
  border-color: rgba(var(--v-theme-success), 0.5) !important;
  background: rgba(var(--v-theme-success), 0.06) !important;
}

.official-meta-stats-box {
  flex-direction: row !important;
  align-items: center;
  padding: 4px 12px;
}

/* ── Calm Official Notice Box (Toned Down Warning) ─────────── */
.official-notice-box {
  background: rgba(var(--v-theme-surface-variant), 0.1);
  border: 1px solid rgba(var(--v-border-color), 0.3) !important;
  border-right: 4px solid rgba(var(--v-theme-warning), 0.8) !important;
}
</style>
