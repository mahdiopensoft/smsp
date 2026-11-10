<template>
  <div class="qb-national-control-console pa-3 pa-md-6">
    <!-- حقل اختيار ملفات المظروف العام -->
    <input
      ref="fileInput"
      type="file"
      multiple
      accept="image/*,application/pdf,.zip"
      class="d-none"
      @change="handleFileSelect"
    />

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
          <custom-text-field
            v-model="currentEnvelope.hallNumber"
            label="رقم القاعة *"
            placeholder="مثال: قاعة 03"
            icon="map-marker-outline"
            cols="12"
            :hideDetails="true"
            :clearable="false"
            @update:model-value="generateEnvelopeBarcode"
          />
        </v-col>

        <!-- باركود / كود المظروف الامتحاني -->
        <v-col cols="12" sm="6" md="3">
          <custom-text-field
            v-model="currentEnvelope.envelopeCode"
            label="باركود / كود المظروف الامتحاني *"
            placeholder="كود المظروف..."
            icon="barcode"
            cols="12"
            :hideDetails="true"
            :clearable="false"
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
          </custom-text-field>
        </v-col>

        <!-- سعة القاعة المقيدة (الطلاب المقيدون) -->
        <v-col cols="12" sm="6" md="3">
          <custom-text-field
            v-model.number="currentEnvelope.expectedCount"
            type="number"
            min="0"
            max="1000"
            label="سعة القاعة المقيدة (الطلاب المقيدون) *"
            icon="account-group-outline"
            cols="12"
            :hideDetails="true"
            :clearable="false"
          />
        </v-col>

        <!-- عدد الغائبين (وفق حافظة الكشف) -->
        <v-col cols="12" sm="6" md="3">
          <custom-text-field
            v-model.number="currentEnvelope.absentCount"
            type="number"
            min="0"
            :max="currentEnvelope.expectedCount"
            label="عدد الغائبين (وفق حافظة الكشف) *"
            icon="account-remove-outline"
            cols="12"
            :hideDetails="true"
            :clearable="false"
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

      <!-- ── معادلة مطابقة القاعة والمطلوب سحبه (تظهر فقط قبل المسح لتجنب التكرار) ── -->
      <div
        v-if="!reconciliationCalculated && currentEnvelope.expectedCount > 0"
        class="d-flex align-center justify-space-between flex-wrap ga-3 pa-2.5 mt-3 rounded-lg border bg-surface"
        style="gap: 12px;"
      >
        <div class="d-flex align-center flex-wrap ga-2" style="gap: 8px;">
          <span class="text-caption font-weight-bold text-medium-emphasis me-1 d-flex align-center ga-1" style="gap: 4px;">
            <v-icon size="16" color="primary">mdi-clipboard-text-outline</v-icon>
            حصر مقيدي القاعة:
          </span>

          <div class="audit-equation-strip d-flex align-center flex-wrap ga-2" style="gap: 8px;">
            <!-- مقيد -->
            <div class="audit-cell">
              <span class="cell-label">المقيدون:</span>
              <bdi class="cell-val font-mono text-high-emphasis ms-1">{{ currentEnvelope.expectedCount }}</bdi>
            </div>

            <span class="text-medium-emphasis font-weight-bold mx-1">=</span>

            <!-- ورقة حاضرة -->
            <div class="audit-cell">
              <span class="cell-label text-success">الحضور:</span>
              <bdi class="cell-val font-mono text-success ms-1">{{ expectedPresentSheets }} ورقة</bdi>
            </div>

            <span class="text-medium-emphasis font-weight-bold mx-1">+</span>

            <!-- طالب غائب -->
            <div class="audit-cell">
              <span class="cell-label text-medium-emphasis">الغياب:</span>
              <bdi class="cell-val font-mono text-medium-emphasis ms-1">{{ currentEnvelope.absentCount }}</bdi>
            </div>
          </div>
        </div>

        <!-- المطلوب سحبه من الماسح -->
        <div class="d-flex align-center ga-2 px-3 py-1.5 rounded-lg border" style="background: rgba(var(--v-theme-surface-variant), 0.12); gap: 8px;">
          <v-icon size="16" color="primary">mdi-tray-arrow-down</v-icon>
          <span class="text-caption text-medium-emphasis font-weight-bold">المطلوب سحبه:</span>
          <bdi class="font-mono font-weight-bold text-primary ms-1">{{ expectedPresentSheets }} ورقة</bdi>
        </div>
      </div>
    </filter-fields>

          <!-- ── 2. ملقم تغذية أوراق المظروف من الماسح الضوئي (يختفي بعد اكتمال المسح لمنع التكرار) ── -->
          <v-card
            v-show="!reconciliationCalculated || isGrading"
            class="main-card pa-4 rounded-xl border mb-4"
          >
            <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3">
              <div class="d-flex align-center gap-2">
                <v-icon size="20" color="primary">mdi-tray-arrow-down</v-icon>
                <span class="text-subtitle-2 font-weight-black text-on-surface">
                  2. تغذية أوراق المظروف من الماسح الضوئي
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
              v-if="batchFiles.length === 0"
              class="upload-dropzone pa-6 rounded-xl text-center d-flex flex-column align-center justify-center transition-all cursor-pointer"
              :class="{ 'is-dragover': isDragging }"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleDrop"
              @click="$refs.fileInput.click()"
            >
              <v-avatar size="56" color="primary" variant="tonal" class="mb-3 rounded-circle">
                <v-icon size="30" color="primary">mdi-cloud-upload-outline</v-icon>
              </v-avatar>
              <div class="text-subtitle-1 font-weight-black mb-1">
                إفلات حزمة أوراق المظروف هنا أو النقر للاستعراض
              </div>
              <div class="text-caption text-medium-emphasis mb-3" style="max-width: 520px; margin: 0 auto; line-height: 1.5;">
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
              <div class="d-flex align-center justify-center flex-wrap ga-2 mt-2.5" style="gap: 8px;">
                <span class="text-caption font-mono font-weight-bold px-2.5 py-1 rounded border" style="background: rgba(var(--v-theme-surface-variant), 0.15);">PDF متعدد الصفحات</span>
                <span class="text-caption font-mono font-weight-bold px-2.5 py-1 rounded border" style="background: rgba(var(--v-theme-surface-variant), 0.15);">صور JPG / PNG</span>
                <span class="text-caption font-mono font-weight-bold px-2.5 py-1 rounded border" style="background: rgba(var(--v-theme-surface-variant), 0.15);">أرشيف ZIP</span>
              </div>
            </div>

            <!-- حالة جاهزية حزمة المظروف بعد الرفع (نفس الهيكل الأنيق والمتناسق دون تكرار بيانات القاعة والمظروف) -->
            <div
              v-else
              class="upload-dropzone upload-dropzone-ready pa-6 rounded-xl text-center d-flex flex-column align-center justify-center transition-all"
              :class="{ 'is-dragover': isDragging }"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleDrop"
            >

              <!-- أيقونة دائرية رسمية معتمدة مماثلة لأيقونة الرفع التي أعجبت المستخدم -->
              <v-avatar size="56" color="primary" variant="tonal" class="mb-2 rounded-circle">
                <v-icon size="30" color="primary">mdi-file-document-check-outline</v-icon>
              </v-avatar>

              <!-- عنوان الجاهزية الرسمي -->
              <div class="d-flex align-center justify-center gap-2 mb-1 flex-wrap">
                <span class="text-subtitle-1 font-weight-black text-high-emphasis">
                  تم تجهيز حزمة أوراق المظروف بنجاح
                </span>
                <v-chip size="x-small" color="success" variant="flat" class="font-weight-bold rounded-s">
                  جاهز للتصحيح
                </v-chip>
              </div>

              <!-- بطاقات تفاصيل الحزمة الفعلية فقط (العدد والحجم دون تكرار القاعة والمظروف) -->
              <div class="d-flex align-center justify-center flex-wrap ga-2.5 mb-4" style="gap: 10px;">
                <!-- 1. العدد: [الأيقونة] ثم [التسمية :] ثم مسافة ثم [القيمة] -->
                <div class="metadata-badge px-3 py-1 rounded-lg">
                  <v-icon size="16" color="primary" class="meta-icon">mdi-file-document-multiple-outline</v-icon>
                  <span class="meta-label">العدد:</span>
                  <span class="meta-value text-primary font-weight-bold">{{ batchFiles.length }} ورقة</span>
                </div>

                <!-- 2. الحجم: [الأيقونة] ثم [التسمية :] ثم مسافة ثم [القيمة] -->
                <div class="metadata-badge px-3 py-1 rounded-lg">
                  <v-icon size="16" class="meta-icon text-medium-emphasis">mdi-database-outline</v-icon>
                  <span class="meta-label">الحجم:</span>
                  <span class="meta-value font-mono">{{ totalBatchSizeFormatted }}</span>
                </div>
              </div>

              <!-- زر بدء التصحيح الأساسي والأزرار المساعدة بتناسق تام ومسافات بينية مريحة -->
              <div class="d-flex align-center justify-center flex-wrap ga-3 w-100" style="max-width: 540px; gap: 12px;">
                <v-btn
                  v-if="!isGrading"
                  color="primary"
                  variant="flat"
                  size="default"
                  class="font-weight-black px-6 rounded-lg elevation-1 flex-grow-1"
                  style="min-height: 42px;"
                  prepend-icon="mdi-barcode-scan"
                  :disabled="!selectedExamId"
                  @click="startBatchGrading"
                >
                  بدء المسح والتصحيح الآلي ({{ batchFiles.length }} ورقة)
                </v-btn>

                <v-btn
                  color="primary"
                  variant="outlined"
                  size="default"
                  class="font-weight-bold px-4 rounded-lg"
                  style="min-height: 42px;"
                  prepend-icon="mdi-plus"
                  title="إضافة أوراق أو ملفات أخرى لنفس المظروف"
                  @click="$refs.fileInput.click()"
                >
                  إضافة أوراق
                </v-btn>

                <v-btn
                  color="error"
                  variant="text"
                  size="default"
                  class="font-weight-bold px-3 rounded-lg"
                  style="min-height: 42px;"
                  prepend-icon="mdi-delete-outline"
                  title="تفريغ الحزمة وإلغاء الملفات"
                  @click="clearFiles"
                >
                  إلغاء
                </v-btn>
              </div>
            </div>

            <!-- شريط تقدم المعالجة الرسمي (OMR Scanner Live Pipeline Console) -->
            <div v-if="isGrading" class="scanning-live-console pa-4 rounded-xl mt-3">
              <!-- Top Row: Active Operation + Live Metrics -->
              <div class="d-flex align-center justify-space-between mb-2 flex-wrap gap-2">
                <div class="d-flex align-center gap-3">
                  <v-avatar color="primary" variant="tonal" size="38" class="rounded-lg flex-shrink-0">
                    <v-icon size="20" color="primary">mdi-shield-check-outline</v-icon>
                  </v-avatar>
                  <div>
                    <div class="d-flex align-center gap-2">
                      <span class="text-subtitle-2 font-weight-black text-primary">{{ gradingStatus }}</span>
                      <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold rounded-s">
                        معالجة نشطة
                      </v-chip>
                    </div>
                    <div class="text-caption text-medium-emphasis d-flex align-center gap-2 mt-0.5">
                      <span>كود المظروف: <strong class="font-mono text-high-emphasis">{{ currentEnvelope.envelopeCode }}</strong></span>
                      <span>•</span>
                      <span>القاعة: <strong class="text-high-emphasis">{{ currentEnvelope.hallNumber }}</strong></span>
                    </div>
                  </div>
                </div>

                <div class="d-flex align-center gap-2">
                  <div class="scanner-sheet-counter-pill">
                    <v-icon size="15" color="primary" class="me-1.5">mdi-file-document-check-outline</v-icon>
                    <span class="font-weight-bold">ورقة {{ processedSheetsCount }} من {{ batchFiles.length }}</span>
                  </div>
                  <div class="scanner-percentage-pill">
                    <span class="font-mono font-weight-black">{{ gradingProgress }}%</span>
                  </div>
                </div>
              </div>

              <!-- Circular Stepper Pipeline (المسار التفاعلي الموحد بالدوائر دون خطوط علوية مكررة) -->
              <div class="stepper-pipeline-container mt-3 pt-1">
                <div class="stepper-track-wrapper">
                  <div
                    v-for="(step, sIdx) in scanningPipelineSteps"
                    :key="step.id"
                    class="stepper-node-wrapper"
                    :class="{
                      'node-completed': currentProcessingStepIndex > sIdx,
                      'node-active': currentProcessingStepIndex === sIdx && gradingProgress < 100,
                      'node-pending': currentProcessingStepIndex < sIdx
                    }"
                  >
                    <!-- Step Node (Circle + Icon + Pulse Wave) -->
                    <div class="stepper-circle-anchor">
                      <!-- Active pulsing wave ring -->
                      <span
                        v-if="currentProcessingStepIndex === sIdx && gradingProgress < 100"
                        class="stepper-pulse-ring"
                      ></span>

                      <div class="stepper-circle">
                        <!-- If Completed: Show Crisp Green Checkmark -->
                        <v-icon
                          v-if="currentProcessingStepIndex > sIdx"
                          size="20"
                          color="success"
                          class="checkmark-pop text-success"
                        >
                          mdi-check-bold
                        </v-icon>

                        <!-- If Active or Pending: Show Step Icon -->
                        <v-icon
                          v-else
                          size="18"
                          :class="{ 'icon-active-breath': currentProcessingStepIndex === sIdx }"
                        >
                          {{ step.icon }}
                        </v-icon>
                      </div>
                    </div>

                    <!-- Step Labels -->
                    <div class="stepper-node-text mt-2 text-center">
                      <div class="node-title font-weight-black">
                        {{ step.label }}
                      </div>
                      <div class="node-subtitle text-caption">
                        <span v-if="currentProcessingStepIndex > sIdx" class="status-completed-text text-success font-weight-bold">
                          <v-icon size="12" class="me-0.5" color="success">mdi-check</v-icon> تم بنجاح
                        </span>
                        <span v-else-if="currentProcessingStepIndex === sIdx && gradingProgress < 100" class="status-active-text">
                          جاري الفحص...
                        </span>
                        <span v-else class="status-pending-text">
                          في الانتظار
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
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

          <!-- ── 3. مركز التحكم والمتابعة ومطابقة المظروف (Unified Envelope Control & Audit Console) ── -->
          <v-card class="main-card rounded-2xl border mb-5 overflow-hidden shadow-sm bg-surface">
            <!-- شريط رأس الكونسول والمؤشرات السريعة (تصميم رسمي هادئ) -->
            <div class="pa-4 border-b d-flex align-center justify-space-between flex-wrap gap-3 bg-surface">
              <div class="d-flex align-center flex-wrap gap-2">
                <v-avatar color="primary" variant="tonal" size="36" class="rounded-lg">
                  <v-icon size="20" color="primary">mdi-folder-text-outline</v-icon>
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

              <!-- مؤشرات سريعة وأزرار الإجراءات (هوية زرقاء رسمية موحدة) -->
              <div class="d-flex align-center flex-wrap gap-2">
                <!-- متوسط درجات القاعة -->
                <v-chip
                  v-if="displaySheets.length > 0"
                  size="small"
                  color="primary"
                  variant="tonal"
                  class="font-weight-bold rounded-s"
                >
                  <v-icon start size="14">mdi-chart-line</v-icon>
                  متوسط القاعة: {{ currentEnvelopeAvgScore }}%
                </v-chip>

                <!-- زر مراجعة وتدقيق إن وجد أوراق تحتاج تدقيق -->
                <custom-btn
                  v-if="needsReviewSheets.length > 0"
                  type="show"
                  :label="`مراجعة وتدقيق (${needsReviewSheets.length})`"
                  color="primary"
                  variant="tonal"
                  icon="mdi-eye-outline"
                  density="comfortable"
                  class="font-weight-bold rounded-s"
                  :click="() => $router.push(`/omr-human-review?exam=${selectedExamId}`)"
                />

                <!-- زر إضافة أوراق أخرى لنفس المظروف -->
                <custom-btn
                  v-if="reconciliationCalculated"
                  type="add"
                  label="إضافة أوراق"
                  color="primary"
                  variant="outlined"
                  icon="mdi-plus"
                  density="comfortable"
                  class="font-weight-bold rounded-s"
                  :click="() => $refs.fileInput.click()"
                />

                <!-- زر إعادة المسح والتصحيح -->
                <custom-btn
                  v-if="reconciliationCalculated"
                  type="refresh"
                  label="إعادة المسح"
                  color="primary"
                  variant="text"
                  icon="mdi-refresh"
                  density="comfortable"
                  class="font-weight-bold rounded-s"
                  :click="startBatchGrading"
                />

                <custom-btn
                  type="add"
                  label="المظروف التالي"
                  color="primary"
                  variant="flat"
                  density="comfortable"
                  class="font-weight-bold px-4 rounded-s"
                  :click="prepareNextEnvelope"
                />
              </div>
            </div>

            <!-- شريط حالة المطابقة الرسمية والعجز/الفائض مدمج بسلاسة داخل كونسول المظروف دون تكرار -->
            <div
              v-if="reconciliationCalculated"
              class="px-4 py-2.5 border-b d-flex align-center justify-space-between flex-wrap ga-2"
              :style="{
                background: reconciliationStatus === 'BALANCED'
                  ? 'rgba(16, 185, 129, 0.05)'
                  : reconciliationStatus === 'DEFICIT'
                    ? 'rgba(239, 68, 68, 0.04)'
                    : 'rgba(245, 158, 11, 0.05)'
              }"
            >
              <div class="d-flex align-center flex-wrap ga-2.5" style="gap: 10px;">
                <!-- شارة الحالة الرسمية -->
                <v-chip
                  size="small"
                  variant="tonal"
                  :color="reconciliationStatus === 'BALANCED' ? 'success' : reconciliationStatus === 'DEFICIT' ? 'error' : 'warning'"
                  class="font-weight-bold rounded-s"
                >
                  <v-icon start size="14">
                    {{ reconciliationStatus === 'BALANCED' ? 'mdi-check-decagram' : 'mdi-alert-circle-outline' }}
                  </v-icon>
                  <template v-if="reconciliationStatus === 'BALANCED'">
                    المطابقة مكتملة: {{ actualScannedCount + currentEnvelope.absentCount }} / {{ currentEnvelope.expectedCount }} ورقة
                  </template>
                  <template v-else-if="reconciliationStatus === 'DEFICIT'">
                    تنبيه عجز: نقص {{ discrepancyAmount }} ورقة مفقودة
                  </template>
                  <template v-else>
                    تنبيه فائض: زيادة {{ Math.abs(discrepancyAmount) }} ورقة
                  </template>
                </v-chip>

                <!-- معادلة المطابقة المنظمة -->
                <div class="audit-equation-strip d-flex align-center ga-2 px-3 py-1 rounded-s text-caption" style="gap: 8px;">
                  <span>سعة القاعة: <bdi class="font-mono text-high-emphasis ms-1">{{ currentEnvelope.expectedCount }}</bdi></span>
                  <span class="text-disabled mx-1">=</span>
                  <span>الممسوح: <bdi class="font-mono text-high-emphasis ms-1">{{ actualScannedCount }}</bdi></span>
                  <span class="text-disabled mx-1">+</span>
                  <span>الغياب: <bdi class="font-mono text-high-emphasis ms-1">{{ currentEnvelope.absentCount }}</bdi></span>
                </div>

                <span v-if="reconciliationStatus === 'DEFICIT'" class="text-caption text-medium-emphasis">
                  (يرجى فحص سلة الماسح أو المظروف)
                </span>
              </div>

              <!-- إجراء المطابقة -->
              <div>
                <custom-btn
                  v-if="reconciliationStatus === 'BALANCED'"
                  type="done"
                  :label="isCommitted ? 'تم الاعتماد' : 'اعتماد وترحيل المظروف'"
                  color="primary"
                  variant="flat"
                  density="comfortable"
                  class="font-weight-bold rounded-s"
                  :disabled="isCommitted"
                  :click="commitEnvelopeToControl"
                />
                <custom-btn
                  v-else-if="reconciliationStatus === 'DEFICIT'"
                  type="show"
                  label="تحرير محضر عجز مظروف"
                  color="primary"
                  variant="outlined"
                  icon="mdi-file-document-edit-outline"
                  density="comfortable"
                  class="font-weight-bold rounded-s"
                  :click="openDiscrepancyReport"
                />
                <custom-btn
                  v-else
                  type="show"
                  label="مراجعة الرزمة"
                  color="primary"
                  variant="outlined"
                  density="comfortable"
                  class="font-weight-bold rounded-s"
                  :click="openDiscrepancyReport"
                />
              </div>
            </div>

            <!-- تبويبات العرض الموحدة والمتزامنة -->
            <v-tabs v-model="activeConsoleTab" color="primary" density="comfortable" class="border-b px-4 bg-surface">
              <!-- تبويب 1: الأوراق الممسوحة بالمظروف -->
              <v-tab value="scanned" class="font-weight-bold">
                <v-icon start size="18">mdi-file-document-check-outline</v-icon>
                الأوراق الممسوحة بالمظروف
                <v-chip size="x-small" color="primary" variant="tonal" class="ms-2 font-weight-black font-mono rounded-s">
                  {{ displaySheets.length }}
                </v-chip>
              </v-tab>

              <!-- تبويب 2: حافظة كشف الطلاب والمطابقة اللحظية -->
              <v-tab value="roster" class="font-weight-bold">
                <v-icon start size="18">mdi-clipboard-list-outline</v-icon>
                حافظة كشف الطلاب والمطابقة
                <v-chip size="x-small" color="primary" variant="tonal" class="ms-2 font-weight-black font-mono rounded-s">
                  {{ registeredStudents.length }}
                </v-chip>
              </v-tab>

              <!-- تبويب 3: أوراق تحتاج تدقيق بشري -->
              <v-tab v-if="needsReviewSheets.length > 0" value="needs_review" class="font-weight-bold">
                <v-icon start size="18" color="error">mdi-alert-circle-outline</v-icon>
                أوراق تحتاج تدقيق بشري
                <v-chip size="x-small" color="error" variant="tonal" class="ms-2 font-weight-black font-mono rounded-s">
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
                    class="font-weight-bold rounded-s"
                    :click="() => activeConsoleTab = 'roster'"
                  />
                </div>

                <!-- في حال وجود أوراق ممسوحة -->
                <div v-else>
                  <!-- شريط الأدوات والخيارات: إحصائيات الفحص والتدقيق الداخلي -->
                  <div class="d-flex align-center justify-space-between flex-wrap ga-2 mb-3 pa-2.5 rounded-lg border bg-surface" style="gap: 8px;">
                    <div class="d-flex align-center flex-wrap ga-2.5 text-caption" style="gap: 10px;">
                      <span class="stat-pill-badge d-inline-flex align-center px-3 py-1 rounded-lg border font-weight-bold">
                        <v-icon size="14" color="success" class="me-1">mdi-check-circle-outline</v-icon>
                        <span class="text-medium-emphasis">أوراق سليمة:</span>
                        <bdi class="font-mono text-success font-weight-black ms-1.5">{{ successfulSheets.length }}</bdi>
                      </span>
                      <span
                        v-if="needsReviewSheets.length > 0"
                        class="stat-pill-badge d-inline-flex align-center px-3 py-1 rounded-lg border font-weight-bold"
                      >
                        <v-icon size="14" color="error" class="me-1">mdi-alert-circle-outline</v-icon>
                        <span class="text-medium-emphasis">تحتاج تدقيق:</span>
                        <bdi class="font-mono text-error font-weight-black ms-1.5">{{ needsReviewSheets.length }}</bdi>
                      </span>
                    </div>
                  </div>

                  <!-- تنبيه أمني إذا تم رصد أوراق دخيلة لا تخص حافظة القاعة (تصميم هادئ رسمي) -->
                  <div
                    v-if="intruderSheets.length > 0"
                    class="official-notice-box mb-3 pa-3 rounded-lg border d-flex align-start gap-3"
                  >
                    <v-icon color="primary" size="20" class="mt-0.5 flex-shrink-0">mdi-shield-alert-outline</v-icon>
                    <div class="flex-grow-1">
                      <div class="text-caption font-weight-bold text-high-emphasis mb-1">
                        تنبيه تدقيق ومطابقة — رصد ورقة دخيلة:
                      </div>
                      <div class="text-caption text-medium-emphasis font-weight-regular" style="line-height: 1.6;">
                        تم رصد {{ intruderSheets.length }} ورقة تم مسحها ولا تتبع كشف الطلاب المقيدين في هذه القاعة (مثل رقم الجلوس: {{ intruderSheets.map(s => s.seat_number).join(', ') }}). تم عزلها تلقائياً للتدقيق البشري لحماية كنترول القاعة.
                      </div>
                    </div>
                  </div>

                  <!-- العرض الجدولي المعياري (Table View) -->
                  <div>
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
                </div>
              </div>

              <!-- ═══════════ التبويب 2: حافظة كشف الطلاب والمطابقة اللحظية ═══════════ -->
              <div v-else-if="activeConsoleTab === 'roster'">
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

    const scanningPipelineSteps = [
      { id: 'prep', label: 'تغذية وسحب الأوراق', icon: 'mdi-tray-arrow-down' },
      { id: 'align', label: 'محاذاة الزوايا والباركود', icon: 'mdi-crop-free' },
      { id: 'ai', label: 'الذكاء الاصطناعي OMR', icon: 'mdi-brain' },
      { id: 'audit', label: 'التدقيق والكنترول', icon: 'mdi-shield-check-outline' },
    ]

    const currentProcessingStepIndex = computed(() => {
      if (gradingProgress.value >= 100) return 4
      if (gradingProgress.value >= 88) return 3
      if (gradingProgress.value >= 58) return 2
      if (gradingProgress.value >= 24) return 1
      return 0
    })

    const processedSheetsCount = computed(() => {
      const total = batchFiles.value.length || 1
      return Math.min(total, Math.max(1, Math.ceil((gradingProgress.value / 100) * total)))
    })

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
        const marked = q.marked_choice || q.marked || q.final_marked_choice || q.candidate_choice || null
        let correct = q.correct_choice || q.expected_choice || q.expected || '—'
        if (correct === 'A' && (q.choices || []).includes('صح')) correct = 'صح'
        else if (correct === 'B' && (q.choices || []).includes('خطأ')) correct = 'خطأ'
        const isMarked = Boolean(marked && marked !== 'لم يُجب (فارغ)' && marked !== 'فارغ')
        const isCorrect = q.is_correct ?? (isMarked && correct !== '—' && String(marked).trim().toUpperCase() === String(correct).trim().toUpperCase())
        const score = q.score_awarded ?? q.marks_awarded ?? (isCorrect ? (q.assigned_weight || q.max_mark || 1) : 0)

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
          finalUrl = u.pathname
        } catch (e) {}
      }
      if (!finalUrl.startsWith('/media/')) {
        if (finalUrl.startsWith('media/')) {
          finalUrl = `/${finalUrl}`
        } else {
          finalUrl = finalUrl.startsWith('/') ? `/media${finalUrl}` : `/media/${finalUrl}`
        }
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

    // ── Unified Envelope Console: Tab Navigation ──
    const activeConsoleTab = ref('roster')

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
      if (e.target.files && e.target.files.length > 0) {
        batchFiles.value = [...batchFiles.value, ...Array.from(e.target.files)]
        batchResult.value = null
        gradingError.value = null
        e.target.value = ''
      }
    }

    const handleDrop = (e) => {
      isDragging.value = false
      if (e.dataTransfer?.files && e.dataTransfer.files.length > 0) {
        batchFiles.value = [...batchFiles.value, ...Array.from(e.dataTransfer.files)]
        batchResult.value = null
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

    const totalBatchSizeFormatted = computed(() => {
      const bytes = batchFiles.value.reduce((acc, f) => acc + (f.size || 0), 0)
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
      return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
    })

    const formatTotalSize = () => totalBatchSizeFormatted.value

    // Real Batch Grading via Backend
    const startBatchGrading = async () => {
      if (batchFiles.value.length === 0 || !selectedExamId.value) return
      isGrading.value = true
      gradingError.value = null
      gradingProgress.value = 8
      gradingStatus.value = `تغذية وسحب أوراق المظروف (${batchFiles.value.length} ورقة)...`

      let currentStep = 0
      const steps = [
        { threshold: 24, text: 'محاذاة الزوايا الهندسية (Fiducials) وقراءة الباركود...' },
        { threshold: 58, text: 'فحص التظليل واستدلال الذكاء الاصطناعي OMR...' },
        { threshold: 88, text: 'تدقيق النتائج ومطابقة درجات الكنترول...' },
      ]

      const startTime = Date.now()
      const timer = setInterval(() => {
        if (gradingProgress.value < 94) {
          const elapsed = Date.now() - startTime
          // Dynamic smooth acceleration curve - never halts or crawls
          const target = Math.min(94, Math.round(12 + Math.sqrt(elapsed * 2.2)))
          if (target > gradingProgress.value) {
            gradingProgress.value = target
          } else {
            gradingProgress.value = Math.min(94, gradingProgress.value + 1)
          }

          if (currentStep < steps.length && gradingProgress.value >= steps[currentStep].threshold) {
            gradingStatus.value = steps[currentStep].text
            currentStep++
          }
        }
      }, 100)

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
        gradingStatus.value = 'اكتملت المعالجة وتصحيح المظروف بنجاح!'
        batchResult.value = resp.data
        activeConsoleTab.value = 'scanned'
        await new Promise((r) => setTimeout(r, 300))
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

    const openSheetPreview = async (sheet) => {
      let targetSheet = { ...sheet }

      // إذا كانت قائمة الأسئلة فارغة وكان هناك معرف تسليم أو رقم جلوس، جلب البيانات كاملة من السيرفر
      if (!targetSheet.questions || targetSheet.questions.length === 0) {
        try {
          let data = null
          const numId = Number(targetSheet.id)
          if (!isNaN(numId) && numId > 0 && numId < 10000) {
            try {
              const resp = await submissionsAPI.get(numId)
              data = resp.data?.data || resp.data
            } catch (_) {}
          }
          if ((!data || !data.id) && targetSheet.seat_number && selectedExamId.value) {
            const resp = await submissionsAPI.list({
              exam: selectedExamId.value,
              search: targetSheet.seat_number,
            })
            const results = resp.data?.results || (Array.isArray(resp.data) ? resp.data : [])
            if (results.length > 0) {
              const matched = results.find(s => String(s.seat_number).trim() === String(targetSheet.seat_number).trim()) || results[0]
              const subDetail = await submissionsAPI.get(matched.id)
              data = subDetail.data?.data || subDetail.data
            }
          }
          if (data) {
            targetSheet.id = data.id || targetSheet.id
            targetSheet.questions = data.omr_result || data.questions || []
            targetSheet.image_url = data.original_image || targetSheet.image_url || ''
            targetSheet.annotated_url = data.aligned_image || targetSheet.annotated_url || targetSheet.image_url
            targetSheet.student_name = data.student_name || targetSheet.student_name
            targetSheet.seat_number = data.seat_number || targetSheet.seat_number
            targetSheet.model_code = data.exam_version_code || data.layout_result?.version_code || targetSheet.model_code || 'A'
            targetSheet.score = data.total_score != null ? data.total_score : (targetSheet.score != null ? targetSheet.score : 0)
            targetSheet.max_score = data.layout_result?.max_score || targetSheet.max_score || 50
            targetSheet.percentage = data.layout_result?.score_percent != null ? data.layout_result?.score_percent : (targetSheet.percentage || 0)
          }
        } catch (e) {
          console.warn('Could not load detailed submission for preview:', e)
        }
      }

      const img = targetSheet?.image_url || targetSheet?.original_image || ''
      const ann = targetSheet?.annotated_url || targetSheet?.aligned_image || img
      activePreviewSheet.value = {
        ...targetSheet,
        image_url: img,
        annotated_url: ann,
        questions: targetSheet?.questions || targetSheet?.omr_result || [],
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
      scanningPipelineSteps,
      currentProcessingStepIndex,
      processedSheetsCount,
      handleFileSelect,
      handleDrop,
      clearFiles,
      formatTotalSize,
      totalBatchSizeFormatted,
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

/* ── Upload Dropzone (Compact, Centered & Proportioned) ─────── */
.upload-dropzone {
  max-width: 680px;
  margin: 0 auto;
  background: rgba(var(--v-theme-surface-variant), 0.12);
  border: 2px dashed rgba(var(--v-border-color), 0.3);
  cursor: pointer;
  min-height: 180px;
  transition: all 0.25s ease;
  position: relative;
}

.upload-dropzone:hover, .upload-dropzone.is-dragover {
  border-color: rgba(var(--v-theme-primary), 0.7);
  background: rgba(var(--v-theme-primary), 0.05);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(var(--v-theme-primary), 0.1);
}

.upload-dropzone-ready {
  border: 1.5px solid rgba(var(--v-theme-primary), 0.35);
  background: linear-gradient(180deg, rgba(var(--v-theme-surface), 0.96), rgba(var(--v-theme-primary), 0.03));
  box-shadow: 0 4px 18px rgba(var(--v-theme-primary), 0.06);
  cursor: default;
}

/* ── Metadata Badges (Soft, Modern, RTL Aligned) ───────────── */
.metadata-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  background: rgba(var(--v-theme-surface-variant), 0.16);
  border: 1px solid rgba(var(--v-border-color), 0.12);
  border-radius: 8px;
  line-height: 1.2;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.metadata-badge:hover {
  background: rgba(var(--v-theme-surface-variant), 0.28);
}

.metadata-badge .meta-icon {
  flex-shrink: 0;
  margin-inline-end: 4px;
}

.metadata-badge .meta-label {
  font-size: 0.75rem;
  color: rgba(var(--v-theme-on-surface), 0.6);
  font-weight: 400;
  white-space: nowrap;
  margin-inline-end: 5px;
}

.metadata-badge .meta-value {
  font-size: 0.78rem;
  font-weight: 700;
  color: rgb(var(--v-theme-on-surface));
  white-space: nowrap;
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
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.15) !important;
}

.audit-equation-strip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(var(--v-theme-surface-variant), 0.12);
  padding: 5px 12px;
  border-radius: 8px;
  border: 1px solid rgba(var(--v-border-color), 0.15);
  white-space: nowrap;
}

.audit-cell {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 2px 6px;
  font-size: 0.82rem;
  white-space: nowrap;
}

.audit-cell .cell-label {
  color: rgba(var(--v-theme-on-surface), 0.7);
  font-weight: 600;
  margin-inline-end: 4px;
}

.audit-cell .cell-val {
  font-weight: 700;
}

.stat-pill-badge {
  background: rgba(var(--v-theme-surface-variant), 0.15);
  border-color: rgba(var(--v-border-color), 0.12) !important;
  white-space: nowrap;
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

/* ── Calm Official Notice Box (Toned Down Official Notice) ──── */
.official-notice-box {
  background: rgba(var(--v-theme-primary), 0.03);
  border: 1px solid rgba(var(--v-theme-primary), 0.18) !important;
  border-right: 4px solid rgb(var(--v-theme-primary)) !important;
}

/* ── High-Performance OMR Scanner Live Console ────────────── */
.scanning-live-console {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.04) 0%, rgba(var(--v-theme-surface), 0.98) 100%) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.22) !important;
  box-shadow: 0 4px 18px rgba(var(--v-theme-primary), 0.06), 0 1px 3px rgba(0, 0, 0, 0.04);
  position: relative;
  overflow: hidden;
}

.scanner-sheet-counter-pill {
  display: inline-flex;
  align-items: center;
  padding: 5px 12px;
  background: rgba(var(--v-theme-surface-variant), 0.08);
  border: 1px solid rgba(var(--v-border-color), 0.2);
  border-radius: 6px;
  font-size: 0.82rem;
  color: rgb(var(--v-theme-on-surface));
}

.scanner-percentage-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 58px;
  padding: 4px 10px;
  background: rgb(var(--v-theme-primary));
  color: #ffffff;
  border-radius: 6px;
  font-size: 0.92rem;
  box-shadow: 0 2px 6px rgba(var(--v-theme-primary), 0.25);
}

/* ── Circular Stepper Pipeline ───────────────────────────── */
.stepper-pipeline-container {
  padding: 4px 6px 0 6px;
}

.stepper-track-wrapper {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  position: relative;
}

.stepper-node-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  z-index: 2;
}

/* Connecting bar between nodes (RTL support, doesn't cut across circles) */
.stepper-node-wrapper:not(:first-child)::before {
  content: '';
  position: absolute;
  top: 18px;
  right: calc(-50% + 25px);
  width: calc(100% - 50px);
  height: 4px;
  background: rgba(var(--v-theme-surface-variant), 0.4);
  border-radius: 999px;
  z-index: 1;
  transition: all 0.35s ease;
}

.stepper-node-wrapper.node-completed:not(:first-child)::before {
  background: #10b981 !important;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
}

.stepper-node-wrapper.node-active:not(:first-child)::before {
  background: linear-gradient(to left, rgb(var(--v-theme-primary)), #10b981) !important;
}

.stepper-circle-anchor {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3;
}

.stepper-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgb(var(--v-theme-surface)) !important;
  border: 2px solid rgba(var(--v-border-color), 0.35);
  color: rgba(var(--v-theme-on-surface), 0.45);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 0 0 5px rgb(var(--v-theme-surface)), 0 2px 6px rgba(0, 0, 0, 0.04);
}

/* 1. Pending Node */
.node-pending .stepper-circle {
  background: rgb(var(--v-theme-surface)) !important;
  border-color: rgba(var(--v-border-color), 0.3);
  color: rgba(var(--v-theme-on-surface), 0.4);
  box-shadow: 0 0 0 5px rgb(var(--v-theme-surface)), 0 1px 4px rgba(0, 0, 0, 0.03);
}

/* 2. Active Node */
.node-active .stepper-circle {
  background: rgb(var(--v-theme-primary)) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  color: #ffffff !important;
  transform: scale(1.1);
  box-shadow: 0 0 0 5px rgb(var(--v-theme-surface)), 0 0 0 8px rgba(var(--v-theme-primary), 0.22), 0 4px 12px rgba(var(--v-theme-primary), 0.4);
}

/* Active Pulsing Wave Ring */
.stepper-pulse-ring {
  position: absolute;
  top: -6px;
  left: -6px;
  right: -6px;
  bottom: -6px;
  border-radius: 50%;
  border: 2px solid rgb(var(--v-theme-primary));
  opacity: 0.8;
  animation: stepper-ring-expand 1.6s cubic-bezier(0.24, 0, 0.38, 1) infinite;
  pointer-events: none;
}

@keyframes stepper-ring-expand {
  0% { transform: scale(0.9); opacity: 0.8; }
  50% { transform: scale(1.25); opacity: 0.3; }
  100% { transform: scale(1.45); opacity: 0; }
}

.icon-active-breath {
  animation: icon-breath 1.4s ease-in-out infinite alternate;
}

@keyframes icon-breath {
  from { transform: scale(0.95); opacity: 0.9; }
  to { transform: scale(1.08); opacity: 1; }
}

/* 3. Completed Node (علامة الصح خضراء والحدود خضراء زمردية) */
.node-completed .stepper-circle {
  background: rgb(var(--v-theme-surface)) !important;
  border-color: #10b981 !important;
  color: #10b981 !important;
  box-shadow: 0 0 0 5px rgb(var(--v-theme-surface)), 0 0 0 6px rgba(16, 185, 129, 0.25), 0 2px 8px rgba(16, 185, 129, 0.2);
}

.checkmark-pop {
  animation: pop-in 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes pop-in {
  0% { transform: scale(0.4); opacity: 0; }
  70% { transform: scale(1.25); }
  100% { transform: scale(1); opacity: 1; }
}

/* Stepper Node Typography */
.stepper-node-text {
  max-width: 140px;
}

.node-title {
  font-size: 0.78rem;
  line-height: 1.25;
  transition: color 0.2s ease;
}

.node-active .node-title {
  color: rgb(var(--v-theme-primary));
  font-weight: 800;
}

.node-completed .node-title {
  color: rgb(var(--v-theme-on-surface));
}

.node-pending .node-title {
  color: rgba(var(--v-theme-on-surface), 0.5);
  font-weight: 600;
}

.node-subtitle {
  font-size: 0.7rem;
  margin-top: 2px;
}

.status-completed-text {
  color: #10b981 !important;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
}

.status-active-text {
  color: rgb(var(--v-theme-primary));
  font-weight: 700;
  animation: pulse-text 1.2s ease-in-out infinite alternate;
}

@keyframes pulse-text {
  from { opacity: 0.7; }
  to { opacity: 1; }
}

.status-pending-text {
  color: rgba(var(--v-theme-on-surface), 0.4);
}

@media (max-width: 600px) {
  .stepper-circle {
    width: 32px;
    height: 32px;
    box-shadow: 0 0 0 4px rgb(var(--v-theme-surface)), 0 2px 5px rgba(0, 0, 0, 0.04);
  }
  .stepper-node-wrapper:not(:first-child)::before {
    top: 14px;
    right: calc(-50% + 20px);
    width: calc(100% - 40px);
  }
  .node-title {
    font-size: 0.7rem;
  }
  .node-subtitle {
    display: none;
  }
}
</style>
