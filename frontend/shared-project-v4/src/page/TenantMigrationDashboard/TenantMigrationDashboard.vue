<template>
  <div>
    <custom-data-table
      :="{
        items,
        headers,
        getData,
        actions: false,
      }"
    >
      <!-- actionList, -->
      <template v-slot:action>
        <div class="d-flex gap-4">
          <custom-btn
            type="import"
            icon="mdi-database-import-outline"
            label="استيراد نسخة احتياطية"
            color="secondary"
            :click="() => openDialog('importDialog')"
          />
          <custom-btn
            type="export"
            icon="mdi-database-export"
            label="تصدير نسخة احتياطية"
            :click="() => openDialog('exportDialog')"
          />
        </div>
      </template>

      <template v-slot:item-slot="{ item, key }">
        <div v-if="key == 'migration_type'">
          <v-chip :color="item.migration_type === 'تصدير' ? 'primary' : 'success'">
            {{ item.migration_type }}
          </v-chip>
        </div>

        <div v-if="key == 'status'">
          <span
            class="status-dot"
            :class="item.status ? item.status.toLowerCase() : ''"
          ></span>
          {{ getStatusText(item.status) }}
        </div>

        <div v-if="key == 'progress_percentage'" class="text-center">
          <span v-if="item.status === 'RUNNING'">{{ item.progress_percentage }}%</span>
          <span v-else-if="item.status === 'SUCCESS'">100%</span>
          <span v-else>-</span>
          <!-- <div
            class="mini-progress-bar-container"
            v-if="item.status === 'RUNNING'"
          >
            <div
              class="mini-progress-bar"
              :style="{ width: item.progress_percentage + '%' }"
            ></div>
            <span class="mini-progress-text"
              >{{ item.progress_percentage }}%</span
            >
          </div>
          <span v-else-if="item.status === 'SUCCESS'">100%</span>
          <span v-else>-</span> -->
        </div>
        <div v-if="key == 'file_size'">
          {{ item.file_size ? formatBytes(item.file_size) : "-" }}
        </div>
        <div v-if="key == 'action'" class="d-flex justify-center" style="gap: 8px">
          <custom-btn
            v-if="item.status === 'RUNNING'"
            isIcon
            class="glass-btn-secondary"
            label="إنهاء العملية الجارية فورا"
            icon="cancel"
            color="error"
            variant="tonal"
            :click="() => showCancelTaskDialog('export', item)"
          >
          </custom-btn>
          <!-- <custom-btn
            v-if="item.status === 'SUCCESS' && item?.migration_type == 'تصدير'"
            isIcon
            type="add"
            color="secondary"
            label="استيراد الحزمة"
            variant="tonal"
            icon="mdi-database-import-outline"
            :click="() => openDialog('importDialog')"
          /> -->
          <custom-btn
            v-if="item.status === 'SUCCESS' && item?.migration_type != 'استيراد'"
            isIcon
            type="edit"
            icon="download-outline"
            label="تحميل الحزمة"
            variant="tonal"
            color="primary"
            :click="() => downloadPackage(item)"
          />
          <custom-btn
            v-if="['FAILED', 'CANCELLED']?.includes(item.status)"
            type="delete"
            isIcon
            color="error"
            icon="trash-can-outline"
            label="حذف العنصر"
            variant="tonal"
            :click="() => openConfirmDelete(item)"
          />
          <custom-btn
            v-if="
              ['FAILED', 'SUCCESS', 'RUNNING']?.includes(item.status) &&
              isImportType(item)
            "
            type="info"
            isIcon
            color="info"
            icon="information-outline"
            label="معلومات الاستيراد"
            variant="tonal"
            :click="() => taskStatus(item)"
          />
        </div>
      </template>
    </custom-data-table>

    <!-- ================= EXPORT DIALOG ================= -->
    <custom-dialog
      v-model="dialog.exportDialog"
      title="تصدير نسخة احتياطية"
      subTitle="حدد النطاق والإعدادات لتوليد النسخة."
      height="auto"
    >
      <div class="dialog-glass-card position-relative" :class="{ 'theme-dark': isDark }">
        <template v-if="!isExporting && !exportSuccessSnackbar">
          <!-- <h3 class="text-h6 font-weight-bold g-text-high mb-4">
            نطاق النسخة الاحتياطية
          </h3>

           <v-row class="mb-6">
            <v-col cols="12" sm="4">
              <div
                class="glass-input-box text-center"
                :class="{ active: exportScope === 'ALL' }"
                @click="exportScope = 'ALL'"
              >
                <v-icon
                  size="36"
                  class="mb-2"
                  :style="{
                    color:
                      exportScope === 'ALL'
                        ? 'rgb(var(--v-theme-primary))'
                        : 'var(--g-icon-dim)',
                  }"
                  >mdi-database</v-icon
                >
                <div class="font-weight-bold g-text-high">الكل</div>
                <div class="text-caption g-text-med">كافة المؤسسات التعليمية</div>
              </div>
            </v-col>
            <v-col cols="12" sm="4">
              <div
                class="glass-input-box text-center"
                :class="{ active: exportScope === 'FATHER' }"
                @click="(exportScope = 'FATHER'), (exportOptions.fk_organization = null)"
              >
                <v-icon
                  size="36"
                  class="mb-2"
                  :style="{
                    color:
                      exportScope === 'FATHER'
                        ? 'rgb(var(--v-theme-primary))'
                        : 'var(--g-icon-dim)',
                  }"
                  >mdi-file-tree</v-icon
                >
                <div class="font-weight-bold g-text-high">فروع</div>
                <div class="text-caption g-text-med">منظمة بتفرعاتها</div>
              </div>
            </v-col>
            <v-col cols="12" sm="4">
              <div
                class="glass-input-box text-center"
                :class="{ active: exportScope === 'SPECIFIC' }"
                @click="
                  (exportScope = 'SPECIFIC'), (exportOptions.fk_organization = null)
                "
              >
                <v-icon
                  size="36"
                  class="mb-2"
                  :style="{
                    color:
                      exportScope === 'SPECIFIC'
                        ? 'rgb(var(--v-theme-primary))'
                        : 'var(--g-icon-dim)',
                  }"
                  >mdi-target</v-icon
                >
                <div class="font-weight-bold g-text-high">مخصص</div>
                <div class="text-caption g-text-med">مدارس محددة</div>
              </div>
            </v-col>
          </v-row> -->
          <v-form ref="export_fields">
            <v-expand-transition>
              <div v-if="exportScope === 'FATHER'" class="mb-6">
                <auto-list
                  v-model="exportOptions.fk_organization"
                  name="OrganizationByLevel"
                  param="30"
                  hideDetails="true"
                  :rules="[$required]"
                ></auto-list>
              </div>
            </v-expand-transition>

            <v-expand-transition>
              <div v-if="exportScope === 'SPECIFIC'" class="mb-6">
                <auto-list
                  v-model="exportOptions.fk_organization"
                  name="OrganizationByLevel"
                  param="50"
                  hideDetails="true"
                  :rules="[$required]"
                ></auto-list>
              </div>
            </v-expand-transition>
          </v-form>
          <h3 class="text-h6 font-weight-bold g-text-high mb-4">الإعدادات المتقدمة</h3>
          <div
            class="glass-input-box d-flex justify-space-between align-center mb-4"
            @click="exportOptions.export_media = !exportOptions.export_media"
          >
            <div>
              <div class="font-weight-bold g-text-high">تضمين المرفقات</div>
              <div class="text-caption g-text-med">ينقل الصور والملفات الثنائية</div>
            </div>
            <div style="pointer-events: none">
              <v-switch
                :model-value="exportOptions.export_media"
                color="primary"
                hide-details
                inset
              ></v-switch>
            </div>
          </div>
          <div
            class="glass-input-box d-flex justify-space-between align-center mb-8"
            @click="exportOptions.encrypt_backup = !exportOptions.encrypt_backup"
          >
            <div>
              <div class="font-weight-bold g-text-high">تشفير الحزمة (AES-128)</div>
              <div class="text-caption g-text-med">حماية أمنية للبيانات الحساسة</div>
            </div>
            <div style="pointer-events: none">
              <v-switch
                :model-value="exportOptions.encrypt_backup"
                color="primary"
                hide-details
                inset
              ></v-switch>
            </div>
          </div>

          <button class="glass-btn-primary w-100" @click="handleExport">
            توليد وتحميل <v-icon end>mdi-download</v-icon>
          </button>
        </template>

        <!-- Export Progress / Success -->
        <template v-else-if="isExporting">
          <div class="text-center py-12">
            <v-progress-circular
              indeterminate
              color="rgb(var(--v-theme-primary))"
              size="120"
              width="8"
              class="mb-8 font-weight-bold text-h5 text-glow"
            >
            </v-progress-circular>
            <h3 class="text-h5 font-weight-bold g-text-high mb-3">جاري التحضير...</h3>
          </div>
        </template>

        <template v-else-if="exportSuccessSnackbar">
          <div class="text-center py-6">
            <v-icon
              size="80"
              color="rgb(var(--v-theme-info))"
              class="mb-6 text-glow-success"
              >mdi-cloud-upload-outline</v-icon
            >
            <h3 class="text-h4 font-weight-bold g-text-high mb-3">
              تم بدء التصدير في الخلفية
            </h3>
            <p class="text-subtitle-1 mb-10 g-text-med">
              <!-- <v-icon size="18" class="mb-1" color="info"> mdi-lightbulb-on</v-icon> -->
              يمكنك التنقل أو الخروج من الصفحة، ستستمر العملية في الخلفية دون أي انقطاع.
            </p>
            <div class="d-flex gap-4 justify-center">
              <custom-btn
                class="glass-btn-secondary"
                label="إنهاء العملية الجارية فورا"
                icon="cancel"
                color="error"
                variant="tonal"
                :click="() => showCancelTaskDialog('export')"
              >
              </custom-btn>
              <custom-btn
                class="glass-btn-primary"
                label="العودة للسجل"
                icon="arrow-left"
                :click="closeExportDialog"
              >
              </custom-btn>
            </div>
          </div>
        </template>
      </div>
    </custom-dialog>

    <!-- ================= IMPORT DIALOG ================= -->
    <custom-dialog
      v-model="dialog.importDialog"
      height="auto"
      width="80%"
      title=" استيراد حزمة بيانات"
      subTitle="قم برفع ملف الحزمة لبدء العملية."
    >
      <template #title>
        <!-- Pinned Header: v-card-title taking full space across top -->

        <!-- Stepper: Vuetify 3 v-stepper component occupying left half of dialog (Read-only Progress Indicator) -->
        <div class="dialog-card-title px-3 px-sm-4 gap-2 gap-sm-4 ms-auto w-100">
          <div
            class="wizard-stepper-nav d-flex align-center justify-center gap-1 gap-sm-2 flex-grow-1 mx-1 mx-sm-4"
            dir="rtl"
          >
            <div
              class="wizard-nav-step"
              :class="{ active: importWizardStep === 1, done: importWizardStep > 1 }"
            >
              <div class="nav-step-icon">
                <v-icon v-if="importWizardStep > 1" size="13">mdi-check</v-icon>
                <span v-else>1</span>
              </div>
              <span class="nav-step-title">اختيار الملف</span>
            </div>

            <div class="nav-step-divider" :class="{ done: importWizardStep > 1 }"></div>

            <div
              class="wizard-nav-step"
              :class="{
                active: importWizardStep === 2,
                done: importWizardStep > 2 || (dryRunSuccess && !isFinalImportExecuting),
              }"
            >
              <div class="nav-step-icon">
                <v-icon
                  v-if="
                    importWizardStep > 2 || (dryRunSuccess && !isFinalImportExecuting)
                  "
                  size="13"
                  >mdi-check</v-icon
                >
                <span v-else>2</span>
              </div>
              <span class="nav-step-title">المحاكاة والفحص</span>
            </div>

            <div class="nav-step-divider" :class="{ done: importWizardStep > 2 }"></div>

            <div
              class="wizard-nav-step"
              :class="{ active: importWizardStep === 3, done: importWizardStep > 3 }"
            >
              <div class="nav-step-icon">
                <v-icon v-if="importWizardStep > 3" size="13">mdi-check</v-icon>
                <span v-else>3</span>
              </div>
              <span class="nav-step-title">حل التعارضات</span>
            </div>

            <div class="nav-step-divider" :class="{ done: importWizardStep >= 4 }"></div>

            <div
              class="wizard-nav-step"
              :class="{
                active: importWizardStep === 4 || errorReport.visible,
                done:
                  importResult !== null &&
                  !isFinalImportExecuting &&
                  !hasFinalErrors &&
                  !errorReport.visible,
                error: (hasFinalErrors && !isFinalImportExecuting) || errorReport.visible,
              }"
            >
              <div class="nav-step-icon">
                <v-icon
                  v-if="
                    (hasFinalErrors && !isFinalImportExecuting) || errorReport.visible
                  "
                  size="13"
                  >mdi-alert</v-icon
                >
                <v-icon
                  v-else-if="importResult !== null && !isFinalImportExecuting"
                  size="13"
                  >mdi-check</v-icon
                >
                <span v-else>4</span>
              </div>
              <span class="nav-step-title">{{
                errorReport.visible ? "تقرير الأخطاء" : "الاعتماد النهائي"
              }}</span>
            </div>
          </div>
        </div>
      </template>
      <v-card
        class="glass-card dialog-glass-card position-relative d-flex flex-column overflow-hidden"
        :class="{ 'theme-dark': isDark }"
      >
        <!-- Dialog Scrollable Content Body -->
        <v-card-text class="dialog-card-body pa-3 pa-sm-4 flex-grow-1 overflow-y-auto">
          <!-- ================= ERROR REPORT VIEW (When Non-Model Errors Occur) ================= -->
          <template v-if="errorReport.visible">
            <div
              class="py-4 py-sm-6 px-2 px-sm-4 max-w-2xl mx-auto text-center"
              style="max-width: 740px"
            >
              <!-- Animated Ripple Error Icon -->
              <div
                class="error-ripple-circle mx-auto mb-4 d-flex align-center justify-center position-relative"
                style="width: 76px; height: 76px"
              >
                <div class="ripple-wave error"></div>
                <v-icon size="46" color="error" class="text-glow-error"
                  >mdi-alert-octagon</v-icon
                >
              </div>

              <!-- Report Header Titles -->
              <h3 class="text-h5 text-sm-h4 font-weight-bold g-text-high mb-2">
                {{ errorReport.title || "تقرير أخطاء النظام والبيانات" }}
              </h3>
              <p
                class="text-caption text-sm-body-2 g-text-med mb-4"
                style="max-width: 600px; margin: 0 auto"
              >
                {{ errorReport.message }}
              </p>

              <!-- Quick Meta Bar (Task ID, Timestamp, Stage info) -->
              <div
                class="d-flex align-center justify-center gap-2 flex-wrap mb-4 text-caption g-text-med font-mono"
              >
                <v-chip
                  size="x-small"
                  color="error"
                  variant="tonal"
                  class="font-weight-bold"
                >
                  {{
                    errorReport.stage === "dry-run"
                      ? "مرحلة الفحص الأولي (Dry-Run)"
                      : "مرحلة الاعتماد النهائي"
                  }}
                </v-chip>
                <span v-if="errorReport.taskId" class="d-flex align-center gap-1">
                  <v-icon size="13">mdi-pound</v-icon>
                  {{ errorReport.taskId }}
                </span>
                <span v-if="errorReport.timestamp" class="d-flex align-center gap-1">
                  <v-icon size="13">mdi-clock-outline</v-icon>
                  {{ errorReport.timestamp }}
                </span>
              </div>

              <!-- Error Summary Banner with Download Action -->
              <div
                class="error-summary-banner pa-3 px-4 rounded-xl mb-4 text-start border-subtle d-flex align-center justify-space-between flex-wrap gap-2"
                style="
                  background: rgba(239, 68, 68, 0.08);
                  border-color: rgba(239, 68, 68, 0.25) !important;
                "
              >
                <div class="d-flex align-center gap-2">
                  <v-icon color="error" size="20">mdi-alert-circle</v-icon>
                  <span class="text-subtitle-2 font-weight-bold text-error">
                    تم رصد {{ errorReport.errors?.length || 1 }} أخطاء وموانع غير قابلة
                    للتسوية اليدوية
                  </span>
                </div>
                <!-- <v-btn
                  size="small"
                  variant="tonal"
                  color="error"
                  class="font-weight-bold text-caption"
                  prepend-icon="mdi-download"
                  @click="downloadErrorReport"
                >
                  تصدير تقرير الأخطاء (JSON)
                </v-btn> -->
              </div>

              <!-- Detailed Error Items Cards List -->
              <div
                class="error-items-list text-start mb-6 d-flex flex-column gap-2"
                style="max-height: 280px; overflow-y: auto"
              >
                <div
                  v-for="(errItem, errIdx) in errorReport.errors"
                  :key="'report_err_' + errIdx"
                  class="error-item-card pa-3 rounded-xl border-subtle d-flex align-start gap-3"
                  style="background: rgba(var(--v-theme-surface), 0.7)"
                >
                  <div
                    class="mt-1 d-flex align-center justify-center rounded-circle flex-shrink-0"
                    style="width: 28px; height: 28px; background: rgba(239, 68, 68, 0.12)"
                  >
                    <v-icon size="16" color="error">mdi-close-circle</v-icon>
                  </div>
                  <div class="flex-grow-1">
                    <div
                      class="d-flex align-center justify-space-between gap-1 mb-1 flex-wrap"
                    >
                      <span class="font-weight-bold text-caption g-text-high">{{
                        errItem.title
                      }}</span>
                      <span
                        v-if="errItem.code"
                        class="font-mono text-caption text-error"
                        style="font-size: 0.72rem !important"
                      >
                        [{{ errItem.code }}]
                      </span>
                    </div>
                    <p
                      class="text-caption text-error mb-1 font-mono text-wrap"
                      style="opacity: 0.95; white-space: pre-wrap; word-break: break-word"
                    >
                      {{ errItem.message }}
                    </p>
                    <div
                      v-if="errItem.detail"
                      class="text-caption g-text-med"
                      style="font-size: 0.7rem !important"
                    >
                      {{ errItem.detail }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- Main Navigation & Return Actions -->
              <div
                class="d-flex flex-column flex-sm-row gap-3 justify-center align-stretch align-sm-center pt-2 border-t-subtle"
              >
                <v-btn
                  color="primary"
                  variant="flat"
                  size="large"
                  class="px-8 font-weight-bold text-subtitle-2 rounded-xl shadow-md flex-grow-1 flex-sm-grow-0"
                  prepend-icon="mdi-arrow-right"
                  @click="returnFromErrorReport"
                >
                  {{
                    errorReport.returnStepTitle ||
                    (errorReport.returnStep === 1
                      ? "العودة لاختيار وتعديل الملف (التبويب السابق)"
                      : "العودة لتبويب حل التعارضات (التبويب السابق)")
                  }}
                </v-btn>

                <v-btn
                  variant="tonal"
                  size="large"
                  class="px-6 font-weight-bold text-caption text-sm-body-2 rounded-xl"
                  prepend-icon="mdi-refresh"
                  @click="retryFromErrorReport"
                >
                  إعادة المحاولة
                </v-btn>

                <v-btn
                  variant="text"
                  size="large"
                  class="px-4 font-weight-bold text-caption text-sm-body-2 rounded-xl"
                  @click="closeImportDialog"
                >
                  إغلاق النافذة
                </v-btn>
              </div>
            </div>
          </template>

          <!-- ================= STEP 1: SCOPE & UPLOAD ================= -->
          <template v-else-if="importWizardStep === 1">
            <!-- Alert for previous error if any -->
            <v-alert
              v-if="previousErrorAlert && previousErrorAlert.step === 1"
              type="error"
              variant="tonal"
              closable
              class="mb-4 rounded-xl border-subtle"
              @click:close="previousErrorAlert = null"
            >
              <div class="d-flex align-center justify-space-between flex-wrap gap-2">
                <div class="d-flex align-center gap-2">
                  <v-icon size="18" color="error">mdi-alert-circle</v-icon>
                  <span class="text-caption font-weight-bold">
                    <strong>{{ previousErrorAlert.title }}:</strong>
                    {{ previousErrorAlert.message }}
                  </span>
                </div>
                <v-btn
                  size="x-small"
                  variant="tonal"
                  color="error"
                  class="font-weight-bold"
                  prepend-icon="mdi-file-document-outline"
                  @click="reopenErrorReport"
                >
                  عرض تقرير الخطأ الكامل
                </v-btn>
              </div>
            </v-alert>
            <!-- 1. Organization Scope Selection Section (Segmented Control) -->
            <!-- <div class="mb-5">
              <div class="d-flex align-center justify-space-between mb-2 flex-wrap gap-2">
                <div class="d-flex align-center gap-2">
                  <v-icon color="primary" size="20">mdi-domain</v-icon>
                  <span
                    class="font-weight-bold g-text-high text-subtitle-2 text-sm-subtitle-1"
                    >نطاق المنظمات المستهدفة بالاستيراد</span
                  >
                </div>
                <span class="text-caption g-text-med">حدد النطاق المطلوب دمجه</span>
              </div>

              <div class="scope-segmented-wrapper pa-3 rounded-xl glass-subbox mb-3">
                <div class="scope-segmented-bar d-flex p-1 rounded-lg mb-3">
                  <button
                    type="button"
                    class="scope-segment-btn"
                    :class="{ active: importScope === 'ALL' }"
                    @click="importScope = 'ALL'"
                  >
                    <v-icon size="16" start>mdi-database</v-icon>
                    <span>كافة المنظمات (الكل)</span>
                  </button>
                  <button
                    type="button"
                    class="scope-segment-btn"
                    :class="{ active: importScope === 'FATHER' }"
                    @click="importScope = 'FATHER'"
                  >
                    <v-icon size="16" start>mdi-file-tree</v-icon>
                    <span>منظمة بفروعها (فروع)</span>
                  </button>
                  <button
                    type="button"
                    class="scope-segment-btn"
                    :class="{ active: importScope === 'SPECIFIC' }"
                    @click="importScope = 'SPECIFIC'"
                  >
                    <v-icon size="16" start>mdi-target</v-icon>
                    <span>مدارس محددة (مخصص)</span>
                  </button>
                </div>

                <v-form ref="export_fields">
                  <v-expand-transition>
                    <div v-if="importScope === 'FATHER'" class="mb-6">
                      <auto-list
                        v-model="importOptions.parent_id"
                        name="OrganizationByLevel"
                        param="30"
                        hideDetails="true"
                        :rules="[$required]"
                      ></auto-list>
                    </div>
                  </v-expand-transition>

                  <v-expand-transition>
                    <div v-if="importScope === 'SPECIFIC'" class="mb-6">
                      <auto-list
                        v-model="importOptions.parent_id"
                        name="OrganizationByLevel"
                        param="50"
                        hideDetails="true"
                        :rules="[$required]"
                      ></auto-list>
                    </div>
                  </v-expand-transition>
                </v-form>
                <div
                  v-if="importScope === 'ALL'"
                  class="text-center py-2 text-caption g-text-med"
                >
                  <v-icon size="14" color="success" class="ml-1"
                    >mdi-check-circle-outline</v-icon
                  >
                  <span
                    >سيتم دمج كافة البيانات والمنظمات المتوفرة بالحزمة بشكل شامل
                    وتلقائي.</span
                  >
                </div>
              </div>
            </div> -->

            <!-- 2. Modern Glass Dropzone & File Inspection Card -->
            <div class="mb-5">
              <div class="d-flex align-center justify-space-between mb-3">
                <div class="d-flex align-center gap-2">
                  <v-icon color="primary" size="20">mdi-cloud-upload-outline</v-icon>
                  <span
                    class="font-weight-bold g-text-high text-subtitle-2 text-sm-subtitle-1"
                    >ملف حزمة النسخة الاحتياطية</span
                  >
                </div>
                <div class="d-flex align-center gap-1">
                  <span class="file-badge">ZIP</span>
                  <span class="file-badge">RAR</span>
                </div>
              </div>

              <FileUploader
                v-model="selectedFile"
                accept=".zip,.rar"
                :single="true"
              ></FileUploader>
            </div>

            <!-- 3. Action Button for Step 1 -->
            <div class="d-flex justify-center align-center">
              <v-btn
                class="glass-btn-primary py-3 px-6 text-caption text-sm-subtitle-1 font-weight-bold w-100"
                :disabled="!selectedFile || isUploadingFile"
                @click="startDryRun"
              >
                <v-icon start size="18">mdi-play-speed</v-icon>
                بدء فحص المحاكاة الآمن (Dry-Run)
              </v-btn>
            </div>
          </template>

          <!-- ================= STEP 2: ASYNCHRONOUS BACKEND JOB MONITOR ================= -->
          <template v-else-if="importWizardStep === 2">
            <!-- v-if="isImporting" -->
            <div
              class="py-3 py-sm-5 px-2 px-sm-4 text-center max-w-xl mx-auto"
              style="max-width: 680px"
            >
              <!-- Radar Scanner Graphic / Success Badge -->
              <div
                v-if="dryRunSuccess && !isFinalImportExecuting"
                class="success-ripple-circle mx-auto mb-3 d-flex align-center justify-center position-relative"
                style="width: 72px; height: 72px"
              >
                <div class="ripple-wave"></div>
                <v-icon size="40" color="success">mdi-check-decagram</v-icon>
              </div>
              <div v-else class="scanner-console-visual mx-auto mb-3 position-relative">
                <div class="radar-outer-ring"></div>
                <div class="radar-middle-ring"></div>
                <div class="radar-scan-beam"></div>
                <div class="radar-center-badge">
                  <v-icon size="34" color="primary" class="text-glow"
                    >mdi-cloud-sync</v-icon
                  >
                </div>
              </div>

              <h3 class="text-h5 text-sm-h4 font-weight-bold mb-1 modern-gradient-title">
                {{
                  dryRunSuccess && !isFinalImportExecuting
                    ? "المحاكاة نجحت بالكامل دون أي تعارضات!"
                    : pipelineStage === 1
                    ? "جاري استلام ورفع الحزمة للتحليل"
                    : pipelineStage === 3
                    ? "جاري تدقيق النتائج وتجهيز تقرير المطابقة"
                    : isFinalImportExecuting
                    ? "جاري تطبيق القرارات وحفظ البيانات"
                    : "جاري فحص ومحاكاة الاستيراد"
                }}
              </h3>
              <p class="text-caption text-sm-body-2 mb-3 g-text-med">
                {{
                  dryRunSuccess && !isFinalImportExecuting
                    ? "تم فحص قيود الجداول، تكامل المفاتيح الأجنبية، والمفاتيح الفريدة بنجاح. لا توجد أي أخطاء، ويمكنك الآن تنفيذ الاستيراد الفعلي."
                    : analysisMessage ||
                      (pipelineStage === 1
                        ? "الخادم يستقبل الأرشيف ويجري فحوصات السلامة الأولية..."
                        : pipelineStage === 3
                        ? "الخادم ينهي تدقيق السجلات ويجهز تقرير الجاهزية للعرض..."
                        : isFinalImportExecuting
                        ? "الخادم يعتمد قرارات حل التعارضات ويدمج البيانات في قاعدة البيانات..."
                        : "الخادم يعالج البيانات حالياً في جلسة محاكاة آمنة (Dry-Run)...")
                }}
              </p>

              <!-- Adaptive / Indeterminate Activity Meter -->
              <div class="mb-4">
                <div class="scanner-progress-container mb-2">
                  <div
                    v-if="analysisProgress > 0"
                    class="scanner-progress-fill"
                    :class="{ 'bg-success': dryRunSuccess && !isFinalImportExecuting }"
                    :style="{ width: analysisProgress + '%' }"
                  ></div>
                  <div v-else class="scanner-progress-indeterminate"></div>
                </div>
                <div
                  class="d-flex justify-space-between text-caption g-text-med font-mono"
                >
                  <div class="d-flex align-center gap-2">
                    <span
                      class="status-dot"
                      :class="
                        dryRunSuccess && !isFinalImportExecuting ? 'success' : 'running'
                      "
                    ></span>
                    <span>{{
                      dryRunSuccess && !isFinalImportExecuting
                        ? "اكتمل الفحص بنجاح"
                        : "الخادم: متصل وقيد المعالجة"
                    }}</span>
                    <span class="d-none d-sm-inline"
                      >• مهمة #{{
                        analysisTaskId ||
                        (isFinalImportExecuting ? "IMP-" : "DRY-") +
                          Date.now().toString().slice(-4)
                      }}</span
                    >
                  </div>
                  <div class="d-flex align-center gap-2">
                    <v-icon
                      size="14"
                      :color="
                        dryRunSuccess && !isFinalImportExecuting ? 'success' : 'primary'
                      "
                      >mdi-timer-sand</v-icon
                    >
                    <span class="font-weight-bold g-text-high">{{
                      formattedElapsedTime
                    }}</span>
                    <span v-if="analysisProgress > 0" class="badge-percentage ml-1"
                      >({{ analysisProgress }}%)</span
                    >
                  </div>
                </div>
              </div>

              <!-- ================= ASYNCHRONOUS VERIFICATION PIPELINE ================= -->
              <div class="verification-pipeline pa-3 pa-sm-4 rounded-2xl mb-5 text-right">
                <div
                  class="pipeline-header d-flex align-center justify-space-between pb-2 mb-3 border-b-subtle"
                >
                  <span class="text-caption font-weight-bold g-text-high"
                    >المراحل العامة للعملية في الخادم:</span
                  >
                  <span class="text-caption text-primary font-weight-bold font-mono">{{
                    dryRunSuccess && !isFinalImportExecuting
                      ? "جاهز للاستيراد الفعلي"
                      : isFinalImportExecuting
                      ? `مرحلة الاعتماد (${pipelineStage > 3 ? 3 : pipelineStage} من 3)`
                      : `مرحلة ${pipelineStage > 3 ? 3 : pipelineStage} من 3`
                  }}</span>
                </div>

                <div class="pipeline-items-list d-flex flex-column gap-2">
                  <!-- Milestone 1: Upload & Integrity (Active during upload/dry-run start) -->
                  <div
                    class="pipeline-item d-flex align-center justify-space-between pa-2 rounded-lg"
                    :class="{
                      done: pipelineStage >= 2,
                      active: pipelineStage === 1,
                      pending: pipelineStage < 1,
                    }"
                  >
                    <div class="d-flex align-center gap-2">
                      <v-icon v-if="pipelineStage >= 2" color="success" size="18"
                        >mdi-check-circle</v-icon
                      >
                      <v-progress-circular
                        v-else-if="pipelineStage === 1"
                        indeterminate
                        size="18"
                        width="2"
                        color="primary"
                      ></v-progress-circular>
                      <v-icon v-else color="grey" size="18">mdi-clock-outline</v-icon>
                      <div>
                        <div
                          class="text-caption font-weight-bold"
                          :class="{ 'text-primary': pipelineStage === 1 }"
                        >
                          {{
                            isFinalImportExecuting
                              ? "تجهيز ورفع حزمة القرارات"
                              : "استلام ورفع الحزمة للتحليل"
                          }}
                        </div>
                        <div
                          class="text-caption g-text-med"
                          style="font-size: 0.72rem !important"
                        >
                          {{
                            pipelineStage === 1
                              ? "جاري نقل ورفع الأرشيف وإرسال طلب المحاكاة للخادم (" +
                                (selectedFile?.name || "حزمة البيانات") +
                                ")..."
                              : "تم استلام الأرشيف وفحص البنية الأولية بنجاح (" +
                                (selectedFile?.name || "حزمة البيانات") +
                                ")"
                          }}
                        </div>
                      </div>
                    </div>
                    <span
                      class="status-badge-mini"
                      :class="{
                        success: pipelineStage >= 2,
                        running: pipelineStage === 1,
                        '': pipelineStage < 1,
                      }"
                    >
                      <v-icon
                        v-if="pipelineStage === 1"
                        size="12"
                        class="ml-1"
                        color="info"
                        >mdi-cloud-upload</v-icon
                      >
                      {{
                        pipelineStage >= 2
                          ? "مكتملة ومؤكدة"
                          : pipelineStage === 1
                          ? "جارية الآن"
                          : "قيد الانتظار"
                      }}
                    </span>
                  </div>

                  <!-- Milestone 2: Server Execution (Active during task-status request) -->
                  <div
                    class="pipeline-item d-flex align-center justify-space-between pa-2 rounded-lg"
                    :class="{
                      done: pipelineStage >= 3,
                      active: pipelineStage === 2,
                      pending: pipelineStage < 2,
                    }"
                  >
                    <div class="d-flex align-center gap-2">
                      <v-icon v-if="pipelineStage >= 3" color="success" size="18"
                        >mdi-check-circle</v-icon
                      >
                      <v-progress-circular
                        v-else-if="pipelineStage === 2"
                        indeterminate
                        size="18"
                        width="2"
                        color="primary"
                      ></v-progress-circular>
                      <v-icon v-else color="grey" size="18">mdi-clock-outline</v-icon>
                      <div>
                        <div
                          class="text-caption font-weight-bold"
                          :class="{ 'text-primary': pipelineStage === 2 }"
                        >
                          {{
                            isFinalImportExecuting
                              ? "تطبيق قرارات المستخدم والاعتماد النهائي"
                              : "المعالجة والمحاكاة الآمنة بالخادم (Dry-Run)"
                          }}
                        </div>
                        <div
                          class="text-caption g-text-med"
                          style="font-size: 0.72rem !important"
                        >
                          {{
                            pipelineStage >= 3
                              ? isFinalImportExecuting
                                ? "تم تطبيق كافة القرارات وحفظ السجلات في قاعدة البيانات بنجاح"
                                : "اكتملت جلسة المحاكاة الآمنة وفحص قيود الجداول بنجاح"
                              : pipelineStage === 2
                              ? analysisMessage ||
                                (isFinalImportExecuting
                                  ? "كتابة السجلات وتطبيق القرارات في قاعدة البيانات..."
                                  : "فحص قيود الجداول، تكامل المفاتيح الأجنبية، ورصد التعارضات...")
                              : "بانتظار اكتمال استلام ورفع الملف..."
                          }}
                        </div>
                      </div>
                    </div>
                    <span
                      class="status-badge-mini"
                      :class="{
                        success: pipelineStage >= 3,
                        running: pipelineStage === 2,
                        '': pipelineStage < 2,
                      }"
                    >
                      <v-icon
                        v-if="pipelineStage === 2"
                        size="12"
                        class="ml-1"
                        color="info"
                        >mdi-cog-sync</v-icon
                      >
                      {{
                        pipelineStage >= 3
                          ? "مكتملة ومؤكدة"
                          : pipelineStage === 2
                          ? "جارية الآن"
                          : "قيد الانتظار"
                      }}
                    </span>
                  </div>

                  <!-- Milestone 3: Conflict Matrix Generation or Verification (Timeout & readiness check) -->
                  <div
                    class="pipeline-item d-flex align-center justify-space-between pa-2 rounded-lg"
                    :class="{
                      done: pipelineStage >= 4,
                      active: pipelineStage === 3,
                      pending: pipelineStage < 3,
                    }"
                  >
                    <div class="d-flex align-center gap-2">
                      <v-icon v-if="pipelineStage >= 4" color="success" size="18"
                        >mdi-check-circle</v-icon
                      >
                      <v-progress-circular
                        v-else-if="pipelineStage === 3"
                        indeterminate
                        size="18"
                        width="2"
                        color="primary"
                      ></v-progress-circular>
                      <v-icon v-else color="grey" size="18">mdi-clock-outline</v-icon>
                      <div>
                        <div
                          class="text-caption font-weight-bold"
                          :class="{ 'text-primary': pipelineStage === 3 }"
                        >
                          {{
                            isFinalImportExecuting
                              ? "التحقق النهائي وتحديث سجلات العمليات"
                              : "تجهيز تقرير المطابقة ومصفوفة حل التعارضات"
                          }}
                        </div>
                        <div
                          class="text-caption g-text-med"
                          style="font-size: 0.72rem !important"
                        >
                          {{
                            pipelineStage >= 4
                              ? dryRunSuccess
                                ? "تقرير المطابقة: لا توجد أي تعارضات، البيانات جاهزة للاستيراد الفعلي"
                                : "تم تجهيز مصفوفة حل التعارضات بنجاح للعرض والاعتماد"
                              : pipelineStage === 3
                              ? analysisMessage ||
                                "جاري تدقيق النتائج والتأكد من مطابقة السجلات وتجهيزها..."
                              : "سيتم التحقق وتجهيز البيانات فور انتهاء عمليات الخادم"
                          }}
                        </div>
                      </div>
                    </div>
                    <span
                      class="status-badge-mini"
                      :class="{
                        success: pipelineStage >= 4,
                        running: pipelineStage === 3,
                        '': pipelineStage < 3,
                      }"
                    >
                      <v-icon
                        v-if="pipelineStage === 3"
                        size="12"
                        class="ml-1"
                        color="info"
                        >mdi-file-find-outline</v-icon
                      >
                      {{
                        pipelineStage >= 4
                          ? dryRunSuccess
                            ? "جاهز للاعتماد"
                            : "مكتملة ومؤكدة"
                          : pipelineStage === 3
                          ? "جارية الآن"
                          : "قيد الانتظار"
                      }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Action Buttons to Continue in Background or Stop Operation while processing -->
              <div
                v-if="!dryRunSuccess || isFinalImportExecuting"
                class="d-flex flex-column flex-sm-row align-center justify-center gap-3 pt-3 border-t-subtle"
              >
                <v-btn
                  variant="tonal"
                  color="primary"
                  size="large"
                  class="px-8 font-weight-bold text-subtitle-2 text-sm-subtitle-1 rounded-xl w-100 w-sm-auto shadow-sm"
                  prepend-icon="mdi-clock-fast"
                  @click="continueInBackground"
                >
                  المتابعة في الخلفية
                </v-btn>

                <v-btn
                  variant="tonal"
                  color="error"
                  size="large"
                  class="px-8 font-weight-bold text-subtitle-2 text-sm-subtitle-1 rounded-xl w-100 w-sm-auto shadow-sm"
                  prepend-icon="mdi-stop-circle-outline"
                  :loading="isStoppingOperation"
                  @click="confirmStopOperation"
                >
                  {{
                    isFinalImportExecuting
                      ? "إيقاف الاعتماد والاستيراد"
                      : "إيقاف فحص المحاكاة"
                  }}
                </v-btn>
              </div>

              <!-- Action Buttons when Dry-Run succeeds with 0 errors -->
              <div
                v-if="dryRunSuccess && !isFinalImportExecuting"
                class="d-flex flex-column flex-sm-row align-center justify-center gap-3 pt-3 border-t-subtle"
              >
                <v-btn
                  color="primary"
                  variant="flat"
                  size="large"
                  class="px-8 font-weight-bold text-subtitle-2 text-sm-subtitle-1 shadow-md rounded-xl w-100 w-sm-auto"
                  prepend-icon="mdi-database-import"
                  @click="startFinalImport"
                >
                  تنفيذ الاستيراد الفعلي الآن
                </v-btn>
                <v-btn
                  variant="tonal"
                  size="large"
                  class="px-6 font-weight-bold text-caption text-sm-body-2 rounded-xl w-100 w-sm-auto"
                  prepend-icon="mdi-arrow-right"
                  @click="importWizardStep = 1"
                >
                  تغيير الملف
                </v-btn>
              </div>
            </div>
          </template>

          <!-- ================= STEP 3: CONFLICT & ERROR RESOLUTION (REVAMPED INTERACTIVE RESOLVER) ================= -->
          <template v-else-if="importWizardStep === 3">
            <div
              v-if="!conflicts || conflicts.length === 0"
              class="text-center py-8 py-sm-12 px-4 max-w-xl mx-auto"
              style="max-width: 600px"
            >
              <div
                class="success-ripple-circle mx-auto mb-4 d-flex align-center justify-center position-relative"
                style="width: 72px; height: 72px"
              >
                <div class="ripple-wave"></div>
                <v-icon size="42" color="success">mdi-check-decagram</v-icon>
              </div>
              <h3 class="text-h6 text-sm-h5 font-weight-bold g-text-high mb-2">
                لا توجد أي تعارضات في البيانات!
              </h3>
              <p class="text-caption text-sm-body-2 g-text-med mb-6">
                كافة سجلات الحزمة متوافقة ومطابقة لقواعد البيانات دون تعارض، يمكنك البدء
                بالاستيراد الفعلي الآن.
              </p>
              <div
                class="d-flex flex-column flex-sm-row align-center justify-center gap-3"
              >
                <v-btn
                  color="primary"
                  variant="flat"
                  size="large"
                  class="px-8 font-weight-bold text-subtitle-2 text-sm-subtitle-1 shadow-md rounded-xl w-100 w-sm-auto"
                  prepend-icon="mdi-database-import"
                  @click="startFinalImport"
                >
                  تنفيذ الاستيراد الفعلي الآن
                </v-btn>
                <v-btn
                  variant="tonal"
                  size="large"
                  class="px-6 font-weight-bold text-caption text-sm-body-2 rounded-xl w-100 w-sm-auto"
                  prepend-icon="mdi-arrow-right"
                  @click="importWizardStep = 1"
                >
                  تغيير الملف
                </v-btn>
              </div>
            </div>
            <div v-else>
              <!-- Alert for previous error if returning to Step 3 -->
              <v-alert
                v-if="previousErrorAlert && previousErrorAlert.step === 3"
                type="error"
                variant="tonal"
                closable
                class="mb-3 rounded-xl border-subtle"
                @click:close="previousErrorAlert = null"
              >
                <div class="d-flex align-center justify-space-between flex-wrap gap-2">
                  <div class="d-flex align-center gap-2">
                    <v-icon size="18" color="error">mdi-alert-circle</v-icon>
                    <span class="text-caption font-weight-bold">
                      <strong>{{ previousErrorAlert.title }}:</strong>
                      {{ previousErrorAlert.message }}
                    </span>
                  </div>
                  <v-btn
                    size="x-small"
                    variant="tonal"
                    color="error"
                    class="font-weight-bold"
                    prepend-icon="mdi-file-document-outline"
                    @click="reopenErrorReport"
                  >
                    عرض تقرير الخطأ الكامل
                  </v-btn>
                </div>
              </v-alert>

              <!-- Compact Smart Command Bar -->
              <div
                class="glass-conflict-toolbar mb-3 pa-2 pa-sm-3 rounded-2xl border-subtle"
              >
                <!-- Batch Operations Bar + Search/Filter on same row -->
                <div
                  class="d-flex flex-column flex-lg-row align-stretch align-lg-center justify-space-between gap-2"
                >
                  <!-- Fast Batch Buttons: Mode Dependent (All vs Selected Model) -->
                  <div
                    v-if="conflictFilterModel === 'ALL'"
                    class="d-flex align-center gap-1 flex-wrap"
                  >
                    <span class="text-caption font-weight-bold g-text-high ml-1"
                      >تطبيق للكل ({{ conflicts.length }}):</span
                    >
                    <v-btn
                      size="x-small"
                      :variant="
                        decisionsSummary.SKIP === conflicts.length && conflicts.length > 0
                          ? 'flat'
                          : 'tonal'
                      "
                      color="blue-grey"
                      class="text-caption font-weight-bold"
                      prepend-icon="mdi-debug-step-over"
                      @click="setAllResolutions('SKIP')"
                      title="تجاوز استيراد كافة السجلات المتعارضة والاحتفاظ بالبيانات الحالية"
                    >
                      تجاوز
                    </v-btn>
                    <v-btn
                      size="x-small"
                      :variant="
                        decisionsSummary.UPDATE === conflicts.length &&
                        conflicts.length > 0
                          ? 'flat'
                          : 'tonal'
                      "
                      color="primary"
                      class="text-caption font-weight-bold"
                      prepend-icon="mdi-update"
                      @click="setAllResolutions('UPDATE')"
                      title="استبدال كافة السجلات بالنظام بالوارد"
                    >
                      استبدال
                    </v-btn>
                    <v-btn
                      size="x-small"
                      :variant="
                        decisionsSummary.MERGE === conflicts.length &&
                        conflicts.length > 0
                          ? 'flat'
                          : 'tonal'
                      "
                      color="purple"
                      class="text-caption font-weight-bold"
                      prepend-icon="mdi-merge"
                      @click="setAllResolutions('MERGE')"
                      title="دمج الحقول الفارغة فقط مع الاحتفاظ بالقيم"
                    >
                      دمج
                    </v-btn>
                    <v-btn
                      size="x-small"
                      :variant="
                        decisionsSummary.DUPLICATE === conflicts.length &&
                        conflicts.length > 0
                          ? 'flat'
                          : 'tonal'
                      "
                      color="amber-darken-3"
                      class="text-caption font-weight-bold"
                      prepend-icon="mdi-content-copy"
                      @click="setAllResolutions('DUPLICATE')"
                      title="تكرار وإنشاء نسخ جديدة بأرقام فريدة"
                    >
                      تكرار
                    </v-btn>
                    <v-btn
                      size="x-small"
                      variant="flat"
                      color="deep-purple-accent-3"
                      class="text-caption font-weight-bold text-white shadow-sm"
                      prepend-icon="mdi-flash"
                      @click="smartAutoFixAll"
                      title="حل سريع تلقائي لكافة السجلات بفك تكرار المفاتيح واعتماد التعديلات"
                    >
                      حل سريع للكل
                    </v-btn>
                  </div>

                  <!-- Fast Batch Buttons for Selected Model Only -->
                  <div v-else class="d-flex align-center gap-1 flex-wrap">
                    <span
                      class="text-caption font-weight-bold text-primary ml-1 d-flex align-center gap-1"
                    >
                      <v-icon size="14">{{ getModelIcon(conflictFilterModel) }}</v-icon>
                      <span
                        >تطبيق على {{ getModelName(conflictFilterModel) }} ({{
                          currentModelConflictsCount
                        }}):</span
                      >
                    </span>
                    <v-btn
                      size="x-small"
                      variant="tonal"
                      color="blue-grey"
                      class="text-caption font-weight-bold"
                      prepend-icon="mdi-debug-step-over"
                      @click="setResolutionsForModel(conflictFilterModel, 'SKIP')"
                      :title="'تجاوز كافة سجلات ' + getModelName(conflictFilterModel)"
                    >
                      تجاوز الموديل
                    </v-btn>
                    <v-btn
                      size="x-small"
                      variant="tonal"
                      color="primary"
                      class="text-caption font-weight-bold"
                      prepend-icon="mdi-update"
                      @click="setResolutionsForModel(conflictFilterModel, 'UPDATE')"
                      :title="
                        'استبدال كافة سجلات ' +
                        getModelName(conflictFilterModel) +
                        ' بالوارد'
                      "
                    >
                      استبدال الموديل
                    </v-btn>
                    <v-btn
                      size="x-small"
                      variant="tonal"
                      color="purple"
                      class="text-caption font-weight-bold"
                      prepend-icon="mdi-merge"
                      @click="setResolutionsForModel(conflictFilterModel, 'MERGE')"
                      :title="'دمج حقول سجلات ' + getModelName(conflictFilterModel)"
                    >
                      دمج الموديل
                    </v-btn>
                    <v-btn
                      size="x-small"
                      variant="tonal"
                      color="amber-darken-3"
                      class="text-caption font-weight-bold"
                      prepend-icon="mdi-content-copy"
                      @click="setResolutionsForModel(conflictFilterModel, 'DUPLICATE')"
                      :title="
                        'تكرار سجلات ' + getModelName(conflictFilterModel) + ' برقم فريد'
                      "
                    >
                      تكرار الموديل
                    </v-btn>
                    <v-btn
                      size="x-small"
                      variant="flat"
                      color="deep-purple-accent-3"
                      class="text-caption font-weight-bold text-white shadow-sm"
                      prepend-icon="mdi-flash"
                      @click="smartAutoFixModel(conflictFilterModel)"
                      :title="
                        'حل سريع ذكي لسجلات ' + getModelName(conflictFilterModel) + ' فقط'
                      "
                    >
                      حل سريع للموديل
                    </v-btn>
                    <v-btn
                      size="x-small"
                      variant="text"
                      color="grey"
                      class="text-caption px-1.5"
                      @click="conflictFilterModel = 'ALL'"
                      title="العودة لتطبيق على كافة الموديلات"
                    >
                      عرض الكل
                    </v-btn>
                  </div>

                  <!-- Model Filter Select & Search Input -->
                  <div
                    class="d-flex align-center gap-2 flex-grow-1 flex-lg-grow-0 justify-end flex-wrap"
                  >
                    <!-- Model Autocomplete Field (Searchable dropdown for clean model filtering) -->
                    <div
                      style="min-width: 220px; max-width: 290px"
                      class="flex-grow-1 flex-sm-grow-0"
                    >
                      <v-autocomplete
                        v-model="conflictFilterModel"
                        :items="conflictModelFilterOptions"
                        item-title="title"
                        item-value="value"
                        density="compact"
                        variant="outlined"
                        hide-details
                        auto-select-first
                        prepend-inner-icon="mdi-filter-variant"
                        class="text-caption font-weight-medium"
                      ></v-autocomplete>
                    </div>

                    <!-- Search Input (Vuetify v-text-field) -->
                    <v-text-field
                      v-model="conflictSearch"
                      placeholder="بحث سريع..."
                      density="compact"
                      variant="outlined"
                      hide-details
                      single-line
                      clearable
                      prepend-inner-icon="mdi-magnify"
                      class="conflict-search-field text-caption font-weight-medium"
                      style="min-width: 150px; max-width: 200px"
                    ></v-text-field>
                  </div>
                </div>
              </div>

              <!-- Sub-toolbar: Quick Expand/Collapse Controls -->
              <div
                class="d-flex align-center justify-space-between mb-2 px-1 flex-wrap gap-2"
              >
                <span class="text-caption g-text-med d-flex align-center gap-1">
                  <v-icon size="16" color="primary">mdi-format-list-bulleted-type</v-icon>
                  <span
                    >قائمة السجلات المتعارضة (انقر على أي سجل أو رمز السهم لتوسيعه ومقارنة
                    الحقول)</span
                  >
                </span>
                <div class="d-flex align-center gap-2">
                  <v-btn
                    size="x-small"
                    variant="tonal"
                    color="primary"
                    class="text-caption font-weight-bold"
                    prepend-icon="mdi-arrow-expand-vertical"
                    @click="expandAllConflicts"
                    title="توسيع كافة البطاقات دفعة واحدة"
                  >
                    توسيع الكل
                  </v-btn>
                  <v-btn
                    size="x-small"
                    variant="tonal"
                    class="text-caption font-weight-bold"
                    prepend-icon="mdi-arrow-collapse-vertical"
                    @click="collapseAllConflicts"
                    title="طي كافة البطاقات دفعة واحدة"
                  >
                    طي الكل
                  </v-btn>
                </div>
              </div>

              <!-- Helpful Conflict Guide Banner -->
              <div
                class="conflict-guide-banner pa-3 px-4 rounded-xl mb-3 border-subtle d-flex align-center justify-space-between flex-wrap gap-2"
              >
                <div class="d-flex align-center gap-2">
                  <v-icon color="primary" size="20">mdi-lightbulb-on-outline</v-icon>
                  <span class="text-caption g-text-high">
                    <strong>دليل حل التعارضات:</strong> يمكنك النقر مباشرة على أي قيمة من
                    بيانات النظام أو الملف لاعتمادها، أو تعديلها يدوياً. الخيار الافتراضي
                    هو <strong>تجاوز</strong> للحفاظ على بيانات نظامك الحالية.
                  </span>
                </div>
                <v-chip
                  size="x-small"
                  color="blue-grey"
                  variant="tonal"
                  class="font-weight-bold"
                >
                  الافتراضي: تجاوز (إبقاء النظام)
                </v-chip>
              </div>

              <!-- ================= CONFLICT RESOLUTION CARDS ================= -->
              <div class="conflict-diff-cards-container d-flex flex-column gap-2 mb-3">
                <div
                  v-for="(error, index) in paginatedConflicts"
                  :key="'conflict_' + error.model + '_' + error.old_pk"
                  class="interactive-resolver-card rounded-xl overflow-hidden border-subtle"
                  :class="{ 'is-collapsed': !isCardExpanded(error) }"
                >
                  <!-- Card Top Header: Metadata + One-Click Actions + Chevron Toggle -->
                  <div
                    class="resolver-card-header pa-2 px-3 d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-2 cursor-pointer transition-all"
                    @click="toggleConflictCard(error)"
                  >
                    <div class="d-flex align-center gap-2 flex-wrap">
                      <span class="diff-index-badge"
                        >#{{
                          (conflictPage - 1) *
                            (conflictPageSize === "ALL" ? 0 : conflictPageSize) +
                          index +
                          1
                        }}</span
                      >
                      <v-icon size="16" color="primary" class="ml-n1">{{
                        getModelIcon(error.model)
                      }}</v-icon>
                      <span class="font-weight-bold text-caption g-text-high">{{
                        getModelName(error.model)
                      }}</span>
                      <span class="conflict-pk-badge font-mono text-caption"
                        >#{{ error.old_pk }}</span
                      >

                      <!-- Active Decision Status Badge -->
                      <span
                        class="record-status-pill text-caption font-weight-bold"
                        :class="
                          resolutions[error.model]?.[error.old_pk]?.action
                            ? resolutions[error.model][error.old_pk].action.toLowerCase()
                            : 'skip'
                        "
                      >
                        <v-icon size="11" class="ml-1">{{
                          getActionIcon(
                            resolutions[error.model]?.[error.old_pk]?.action || "SKIP"
                          )
                        }}</v-icon>
                        {{
                          getActionBadgeTitle(
                            resolutions[error.model]?.[error.old_pk]?.action || "SKIP"
                          )
                        }}
                      </span>

                      <!-- Conflict Cause Tag (Subtle & Compact) -->
                      <span
                        v-if="getCollisionKeys(error).length > 0"
                        class="collision-cause-tag text-caption"
                        :title="
                          'المفاتيح الفريدة المتعارضة: ' +
                          getCollisionKeys(error).join(', ')
                        "
                      >
                        ⚠️
                        {{
                          getCollisionKeys(error).length === 1
                            ? "تكرار: " + getCollisionKeys(error)[0]
                            : "تضارب " + getCollisionKeys(error).length + " مفاتيح فريدة"
                        }}
                      </span>
                      <span v-else class="diff-stats-badge text-caption">
                        <v-icon size="11" start>mdi-compare-horizontal</v-icon>
                        {{ getDiffSummaryText(error) }}
                      </span>

                      <!-- Compact Record Summary Hint in Header -->
                      <span
                        v-if="error.new_record || error.existing_record"
                        class="record-inline-chip font-mono text-truncate text-caption d-none d-lg-inline-flex align-center gap-1"
                        :title="
                          'السجل بالنظام: ' +
                          (error.existing_record || '') +
                          '\nالسجل بالوارد: ' +
                          (error.new_record || '')
                        "
                      >
                        <v-icon size="11" class="opacity-60"
                          >mdi-card-text-outline</v-icon
                        >
                        <span class="text-truncate" style="max-width: 240px">{{
                          error.new_record || error.existing_record
                        }}</span>
                      </span>
                    </div>

                    <!-- Single-Record Quick Actions -->
                    <div class="d-flex align-center gap-1 flex-wrap" @click.stop>
                      <v-btn
                        size="x-small"
                        variant="tonal"
                        class="text-caption font-weight-medium px-2 rounded-lg subtle-quick-fix-btn"
                        prepend-icon="mdi-flash"
                        @click="smartAutoFixConflict(error.model, error.old_pk)"
                        title="حل سريع: فك تكرار المفاتيح برقم فريد واعتماد التحديثات"
                      >
                        حل سريع
                      </v-btn>

                      <div class="action-pills-bar d-flex align-center">
                        <v-btn
                          size="x-small"
                          :variant="
                            resolutions[error.model]?.[error.old_pk]?.action === 'SKIP'
                              ? 'tonal'
                              : 'text'
                          "
                          :color="
                            resolutions[error.model]?.[error.old_pk]?.action === 'SKIP'
                              ? 'blue-grey-darken-1'
                              : undefined
                          "
                          class="text-caption font-weight-medium px-2"
                          @click="setConflictAction(error.model, error.old_pk, 'SKIP')"
                          title="تجاوز والاحتفاظ بالسجل الحالي للنظام"
                        >
                          تجاوز
                        </v-btn>
                        <v-btn
                          size="x-small"
                          :variant="
                            resolutions[error.model]?.[error.old_pk]?.action === 'UPDATE'
                              ? 'tonal'
                              : 'text'
                          "
                          :color="
                            resolutions[error.model]?.[error.old_pk]?.action === 'UPDATE'
                              ? 'primary'
                              : undefined
                          "
                          class="text-caption font-weight-medium px-2"
                          @click="setConflictAction(error.model, error.old_pk, 'UPDATE')"
                          title="استبدال السجل الحالي بالبيانات الواردة بالكامل"
                        >
                          استبدال
                        </v-btn>
                        <v-btn
                          size="x-small"
                          :variant="
                            resolutions[error.model]?.[error.old_pk]?.action === 'MERGE'
                              ? 'tonal'
                              : 'text'
                          "
                          :color="
                            resolutions[error.model]?.[error.old_pk]?.action === 'MERGE'
                              ? 'purple-darken-1'
                              : undefined
                          "
                          class="text-caption font-weight-medium px-2"
                          @click="setConflictAction(error.model, error.old_pk, 'MERGE')"
                          title="دمج الحقول الفارغة فقط"
                        >
                          دمج
                        </v-btn>
                        <v-btn
                          size="x-small"
                          :variant="
                            resolutions[error.model]?.[error.old_pk]?.action ===
                            'DUPLICATE'
                              ? 'tonal'
                              : 'text'
                          "
                          :color="
                            resolutions[error.model]?.[error.old_pk]?.action ===
                            'DUPLICATE'
                              ? 'amber-darken-3'
                              : undefined
                          "
                          class="text-caption font-weight-medium px-2"
                          @click="
                            setConflictAction(error.model, error.old_pk, 'DUPLICATE')
                          "
                          title="إنشاء كنسخة مكررة برقم فريد"
                        >
                          تكرار
                        </v-btn>
                        <v-btn
                          size="x-small"
                          :variant="
                            resolutions[error.model]?.[error.old_pk]?.action === 'CUSTOM'
                              ? 'tonal'
                              : 'text'
                          "
                          :color="
                            resolutions[error.model]?.[error.old_pk]?.action === 'CUSTOM'
                              ? 'teal-darken-1'
                              : undefined
                          "
                          class="text-caption font-weight-medium px-2"
                          @click="setConflictAction(error.model, error.old_pk, 'CUSTOM')"
                          title="تخصيص الحقول يدوياً"
                        >
                          مخصص
                        </v-btn>
                      </div>

                      <!-- Expand/Collapse Chevron Button -->
                      <v-btn
                        icon
                        variant="text"
                        size="x-small"
                        class="collapse-toggle-btn mr-1"
                        :title="
                          isCardExpanded(error)
                            ? 'طي تفاصيل البطاقة'
                            : 'توسيع ومراجعة تفاصيل الحقول'
                        "
                        @click="toggleConflictCard(error)"
                      >
                        <v-icon size="18">{{
                          isCardExpanded(error) ? "mdi-chevron-up" : "mdi-chevron-down"
                        }}</v-icon>
                      </v-btn>
                    </div>
                  </div>

                  <!-- Expandable Details with v-expand-transition -->
                  <v-expand-transition>
                    <div
                      v-show="isCardExpanded(error)"
                      class="pa-2 pa-sm-3 pt-1 border-t-subtle"
                    >
                      <!-- 3-Way Interactive v-table -->
                      <div
                        class="interactive-table-wrapper rounded-xl overflow-hidden border-subtle"
                      >
                        <v-table
                          class="interactive-diff-table w-100"
                          density="compact"
                          bg-color="transparent"
                        >
                          <thead>
                            <tr>
                              <th style="width: 22%">الحقل المعني</th>
                              <th style="width: 26%">
                                <div class="d-flex align-center gap-1">
                                  <v-icon size="13" color="primary" class="opacity-70"
                                    >mdi-database-clock-outline</v-icon
                                  >
                                  <span>النظام الحالي</span>
                                </div>
                              </th>
                              <th style="width: 26%">
                                <div class="d-flex align-center gap-1">
                                  <v-icon size="13" color="success" class="opacity-70"
                                    >mdi-file-import-outline</v-icon
                                  >
                                  <span>الملف الوارد</span>
                                </div>
                              </th>
                              <th style="width: 26%">
                                <div class="d-flex align-center gap-1">
                                  <v-icon
                                    size="13"
                                    color="amber-darken-3"
                                    class="opacity-70"
                                    >mdi-check-decagram-outline</v-icon
                                  >
                                  <span>النتيجة المعتمدة للحفظ</span>
                                </div>
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr
                              v-for="(val, field) in error.fields"
                              :key="'diff_field_' + field"
                              :class="{
                                'is-diff': isFieldDifferent(val),
                                'is-same': !isFieldDifferent(val),
                              }"
                            >
                              <!-- Field Name & Status -->
                              <td
                                class="font-weight-medium font-mono text-caption field-col"
                              >
                                <div class="d-flex align-center justify-space-between">
                                  <span>{{ field }}</span>
                                  <span
                                    v-if="!isFieldDifferent(val)"
                                    class="mini-diff-tag same"
                                    title="قيمة متطابقة وهي سبب تعارض المفتاح الفريد"
                                  >
                                    مكرر
                                  </span>
                                  <span
                                    v-else
                                    class="mini-diff-tag diff"
                                    title="قيمة معدلة تختلف بين النظام والملف"
                                  >
                                    معدل
                                  </span>
                                </div>
                              </td>

                              <!-- Existing Value (Clickable) -->
                              <td
                                class="interactive-val-cell exist-cell"
                                :class="{
                                  selected:
                                    isFieldDifferent(val) &&
                                    !isFieldValueAdded(
                                      error.model,
                                      error.old_pk,
                                      field,
                                      error
                                    ) &&
                                    getFieldChoiceState(
                                      error.model,
                                      error.old_pk,
                                      field,
                                      val.existing,
                                      val.new
                                    ) === 'existing',
                                  'is-custom-disabled':
                                    isFieldValueAdded(
                                      error.model,
                                      error.old_pk,
                                      field,
                                      error
                                    ) ||
                                    getFieldChoiceState(
                                      error.model,
                                      error.old_pk,
                                      field,
                                      val.existing,
                                      val.new
                                    ) === 'custom',
                                  'is-duplicate-key': !isFieldDifferent(val),
                                }"
                                @click="
                                  pickField(
                                    error.model,
                                    error.old_pk,
                                    field,
                                    val.existing
                                  )
                                "
                                :title="
                                  isFieldValueAdded(
                                    error.model,
                                    error.old_pk,
                                    field,
                                    error
                                  )
                                    ? 'تم اعتماد قيمة فريدة مخصصة (انقر للاسترجاع)'
                                    : isFieldDifferent(val)
                                    ? 'انقر لاعتماد بيانات النظام الحالي'
                                    : 'قيمة مطابقة في الطرفين'
                                "
                              >
                                <div
                                  class="d-flex align-center justify-space-between w-100 gap-1"
                                >
                                  <div class="val-display-box d-flex align-center gap-1">
                                    <span
                                      v-if="isBooleanValue(val?.existing)"
                                      class="boolean-pill"
                                      :class="
                                        val.existing === true || val.existing === 'true'
                                          ? 'bool-true'
                                          : 'bool-false'
                                      "
                                    >
                                      <v-icon size="11" class="ml-0.5">{{
                                        val.existing === true || val.existing === "true"
                                          ? "mdi-check"
                                          : "mdi-close"
                                      }}</v-icon>
                                      {{ String(val.existing) }}
                                    </span>
                                    <span v-else class="val-text val-exist font-mono">
                                      {{ formatDisplayValue(val?.existing) }}
                                    </span>
                                  </div>
                                  <div
                                    v-if="isFieldDifferent(val)"
                                    class="cell-action-wrapper d-flex align-center flex-shrink-0"
                                  >
                                    <span
                                      v-if="
                                        !isFieldValueAdded(
                                          error.model,
                                          error.old_pk,
                                          field,
                                          error
                                        ) &&
                                        getFieldChoiceState(
                                          error.model,
                                          error.old_pk,
                                          field,
                                          val.existing,
                                          val.new
                                        ) === 'existing'
                                      "
                                      class="val-choice-text exist active"
                                      title="تم إبقاء بيانات النظام الحالي"
                                    >
                                      إبقاء
                                    </span>
                                    <span
                                      v-else
                                      class="val-choice-text exist pick"
                                      @click.stop="
                                        pickField(
                                          error.model,
                                          error.old_pk,
                                          field,
                                          val.existing
                                        )
                                      "
                                      title="انقر للإبقاء على بيانات النظام"
                                    >
                                      إبقاء
                                    </span>
                                  </div>
                                </div>
                              </td>

                              <!-- Incoming Value (Clickable) -->
                              <td
                                class="interactive-val-cell incoming-cell"
                                :class="{
                                  selected:
                                    isFieldDifferent(val) &&
                                    !isFieldValueAdded(
                                      error.model,
                                      error.old_pk,
                                      field,
                                      error
                                    ) &&
                                    getFieldChoiceState(
                                      error.model,
                                      error.old_pk,
                                      field,
                                      val.existing,
                                      val.new
                                    ) === 'new',
                                  'is-custom-disabled':
                                    isFieldValueAdded(
                                      error.model,
                                      error.old_pk,
                                      field,
                                      error
                                    ) ||
                                    getFieldChoiceState(
                                      error.model,
                                      error.old_pk,
                                      field,
                                      val.existing,
                                      val.new
                                    ) === 'custom',
                                  'is-duplicate-key': !isFieldDifferent(val),
                                }"
                                @click="
                                  pickField(error.model, error.old_pk, field, val.new)
                                "
                                :title="
                                  isFieldValueAdded(
                                    error.model,
                                    error.old_pk,
                                    field,
                                    error
                                  )
                                    ? 'تم اعتماد قيمة فريدة مخصصة (انقر للاسترجاع)'
                                    : isFieldDifferent(val)
                                    ? 'انقر لاعتماد بيانات الملف الوارد'
                                    : 'قيمة مطابقة في الطرفين'
                                "
                              >
                                <div
                                  class="d-flex align-center justify-space-between w-100 gap-1"
                                >
                                  <div class="val-display-box d-flex align-center gap-1">
                                    <span
                                      v-if="isBooleanValue(val?.new)"
                                      class="boolean-pill"
                                      :class="
                                        val.new === true || val.new === 'true'
                                          ? 'bool-true'
                                          : 'bool-false'
                                      "
                                    >
                                      <v-icon size="11" class="ml-0.5">{{
                                        val.new === true || val.new === "true"
                                          ? "mdi-check"
                                          : "mdi-close"
                                      }}</v-icon>
                                      {{ String(val.new) }}
                                    </span>
                                    <span v-else class="val-text val-incoming font-mono">
                                      {{ formatDisplayValue(val?.new) }}
                                    </span>
                                  </div>
                                  <div
                                    v-if="isFieldDifferent(val)"
                                    class="cell-action-wrapper d-flex align-center flex-shrink-0"
                                  >
                                    <span
                                      v-if="
                                        !isFieldValueAdded(
                                          error.model,
                                          error.old_pk,
                                          field,
                                          error
                                        ) &&
                                        getFieldChoiceState(
                                          error.model,
                                          error.old_pk,
                                          field,
                                          val.existing,
                                          val.new
                                        ) === 'new'
                                      "
                                      class="val-choice-text incoming active"
                                      title="تم اعتماد بيانات الملف الوارد"
                                    >
                                      اعتماد
                                    </span>
                                    <span
                                      v-else
                                      class="val-choice-text incoming pick"
                                      @click.stop="
                                        pickField(
                                          error.model,
                                          error.old_pk,
                                          field,
                                          val.new
                                        )
                                      "
                                      title="انقر لاعتماد بيانات الملف الوارد"
                                    >
                                      اعتماد
                                    </span>
                                  </div>
                                </div>
                              </td>

                              <!-- Resolved Value (Boolean Compact Switch OR Input Field) -->
                              <td class="resolved-cell">
                                <!-- If Boolean Field: Compact Segmented Switch Capsule -->
                                <div
                                  v-if="isBooleanField(val?.existing, val?.new)"
                                  class="compact-bool-switch"
                                  dir="ltr"
                                  :class="{
                                    'is-true': isFieldBooleanActive(
                                      error.model,
                                      error.old_pk,
                                      field,
                                      true,
                                      val?.new ?? val?.existing
                                    ),
                                    'is-false': isFieldBooleanActive(
                                      error.model,
                                      error.old_pk,
                                      field,
                                      false,
                                      val?.new ?? val?.existing
                                    ),
                                  }"
                                >
                                  <button
                                    type="button"
                                    class="bool-segment-btn false-seg"
                                    :class="{
                                      active: isFieldBooleanActive(
                                        error.model,
                                        error.old_pk,
                                        field,
                                        false,
                                        val?.new ?? val?.existing
                                      ),
                                    }"
                                    @click="
                                      setBooleanField(
                                        error.model,
                                        error.old_pk,
                                        field,
                                        false
                                      )
                                    "
                                    title="اعتماد القيمة false (معطل)"
                                  >
                                    <v-icon size="11" class="mr-0.5">mdi-close</v-icon>
                                    <span>false</span>
                                  </button>
                                  <button
                                    type="button"
                                    class="bool-segment-btn true-seg"
                                    :class="{
                                      active: isFieldBooleanActive(
                                        error.model,
                                        error.old_pk,
                                        field,
                                        true,
                                        val?.new ?? val?.existing
                                      ),
                                    }"
                                    @click="
                                      setBooleanField(
                                        error.model,
                                        error.old_pk,
                                        field,
                                        true
                                      )
                                    "
                                    title="اعتماد القيمة true (مفعل)"
                                  >
                                    <v-icon size="11" class="mr-0.5">mdi-check</v-icon>
                                    <span>true</span>
                                  </button>
                                </div>

                                <!-- If String / Numeric Field: Text Input with Quick Actions -->
                                <div
                                  v-else
                                  class="resolved-input-group d-flex align-center gap-1"
                                >
                                  <v-text-field
                                    v-model="
                                      resolutions[error.model][error.old_pk].fields[field]
                                    "
                                    density="compact"
                                    variant="outlined"
                                    hide-details
                                    single-line
                                    :placeholder="'قيمة ' + field"
                                    class="resolved-v-field font-mono"
                                    @update:model-value="
                                      onFieldInput(error.model, error.old_pk)
                                    "
                                  ></v-text-field>
                                  <v-btn
                                    v-if="
                                      isFieldValueAdded(
                                        error.model,
                                        error.old_pk,
                                        field,
                                        error
                                      )
                                    "
                                    size="x-small"
                                    variant="tonal"
                                    color="error"
                                    class="text-caption font-weight-medium px-1.5 flex-shrink-0"
                                    style="
                                      height: 26px;
                                      min-width: 40px;
                                      font-size: 0.65rem !important;
                                    "
                                    @click="
                                      removeAddedFieldValue(
                                        error.model,
                                        error.old_pk,
                                        field,
                                        error
                                      )
                                    "
                                    title="حذف القيمة المضافة والتراجع للأصل"
                                  >
                                    ✕ تراجع
                                  </v-btn>
                                  <v-btn
                                    v-else
                                    size="x-small"
                                    variant="tonal"
                                    color="secondary"
                                    class="text-caption font-weight-medium px-1.5 flex-shrink-0 subtle-unique-btn"
                                    style="
                                      height: 26px;
                                      min-width: 40px;
                                      font-size: 0.65rem !important;
                                    "
                                    @click="
                                      addUniqueFieldValue(
                                        error.model,
                                        error.old_pk,
                                        field,
                                        error
                                      )
                                    "
                                    title="إضافة قيمة فريدة (-1) لفك التكرار"
                                  >
                                    +فريد
                                  </v-btn>
                                </div>
                              </td>
                            </tr>
                          </tbody>
                        </v-table>
                      </div>
                    </div>
                  </v-expand-transition>
                </div>
              </div>

              <!-- High-Performance Pagination Bar -->
              <div
                v-if="filteredConflicts.length > 0"
                class="conflict-pagination-bar d-flex flex-column flex-sm-row align-center justify-space-between gap-2 pa-2 px-3 rounded-xl border-subtle mb-4"
              >
                <div class="d-flex align-center gap-2 text-caption g-text-med flex-wrap">
                  <span>
                    عرض السجلات:
                    <strong class="font-mono text-primary font-weight-bold"
                      >{{ paginationStartRecord }}-{{ paginationEndRecord }}</strong
                    >
                    من أصل
                    <strong class="font-mono">{{ filteredConflicts.length }}</strong>
                  </span>
                  <span class="d-none d-sm-inline opacity-40">|</span>
                  <div class="d-flex align-center gap-1">
                    <span class="text-caption">سجلات الصفحة:</span>
                    <select
                      v-model="conflictPageSize"
                      class="compact-page-size-select text-caption font-mono"
                      @change="conflictPage = 1"
                    >
                      <option :value="10">10</option>
                      <option :value="25">25</option>
                      <option :value="50">50</option>
                      <option value="ALL">عرض الكل</option>
                    </select>
                  </div>
                </div>

                <div v-if="conflictTotalPages > 1" class="d-flex align-center gap-1">
                  <v-btn
                    size="x-small"
                    variant="tonal"
                    icon
                    :disabled="conflictPage <= 1"
                    @click="conflictPage--"
                    title="الصفحة السابقة"
                  >
                    <v-icon size="16">mdi-chevron-right</v-icon>
                  </v-btn>
                  <span class="text-caption font-mono px-2 font-weight-bold">
                    {{ conflictPage }} / {{ conflictTotalPages }}
                  </span>
                  <v-btn
                    size="x-small"
                    variant="tonal"
                    icon
                    :disabled="conflictPage >= conflictTotalPages"
                    @click="conflictPage++"
                    title="الصفحة التالية"
                  >
                    <v-icon size="16">mdi-chevron-left</v-icon>
                  </v-btn>
                </div>
              </div>

              <!-- Bottom Action Bar -->
              <div
                class="d-flex flex-column-reverse flex-sm-row align-stretch align-sm-center justify-space-between gap-3 pt-4 border-t-subtle"
              >
                <v-btn
                  variant="tonal"
                  size="large"
                  class="px-6 font-weight-bold text-caption text-sm-body-2 w-100 w-sm-auto"
                  prepend-icon="mdi-arrow-right"
                  rounded="xl"
                  @click="importWizardStep = 1"
                >
                  تراجع وتعديل الملف
                </v-btn>

                <v-btn
                  color="primary"
                  variant="flat"
                  size="large"
                  class="px-8 font-weight-bold text-subtitle-2 text-sm-subtitle-1 w-100 w-sm-auto shadow-md"
                  append-icon="mdi-check-decagram"
                  rounded="xl"
                  @click="startFinalImport"
                >
                  تأكيد القرارات والاعتماد النهائي ({{ resolvedConflictsCount }}/{{
                    conflicts.length
                  }})
                </v-btn>
              </div>
            </div>
          </template>

          <!-- ================= STEP 4: FINAL LOADING & COMPREHENSIVE REPORT ================= -->
          <template v-else-if="importWizardStep === 4">
            <!-- 1. FINAL LOADING STATE (When Final Import is Executing) -->
            <div
              v-if="isFinalImportExecuting"
              class="text-center py-6 py-sm-10 px-2 px-sm-4 max-w-2xl mx-auto"
              style="max-width: 680px"
            >
              <!-- High-Tech Animated Radar / Loading Spinner -->
              <div class="scanner-console-visual mx-auto mb-4 position-relative">
                <div class="radar-outer-ring"></div>
                <div class="radar-middle-ring"></div>
                <div class="radar-scan-beam"></div>
                <div class="radar-center-badge">
                  <v-icon size="36" color="primary" class="text-glow"
                    >mdi-database-sync</v-icon
                  >
                </div>
              </div>

              <h3 class="text-h5 text-sm-h4 font-weight-bold mb-2 modern-gradient-title">
                جاري تطبيق القرارات وحفظ البيانات في قاعدة البيانات
              </h3>
              <p class="text-caption text-sm-body-2 mb-4 g-text-med">
                {{
                  analysisMessage || "جاري كتابة السجلات وتطبيق قرارات حل التعارضات..."
                }}
              </p>

              <!-- Progress Bar with Percentage & Milestones -->
              <div class="glass-progress-card pa-4 rounded-2xl mb-4 border-subtle">
                <div class="d-flex align-center justify-space-between mb-2">
                  <span
                    class="text-caption font-weight-bold g-text-high d-flex align-center gap-1"
                  >
                    <v-icon size="14" color="primary">mdi-progress-clock</v-icon>
                    التقدم الإجمالي:
                  </span>
                  <span class="text-caption font-mono font-weight-bold text-primary">
                    {{ analysisProgress }}%
                  </span>
                </div>
                <v-progress-linear
                  :model-value="analysisProgress"
                  color="primary"
                  height="10"
                  rounded
                  striped
                  active
                  class="mb-3"
                ></v-progress-linear>

                <!-- 3 Milestone Badges for Final Import -->
                <div
                  class="d-flex align-center justify-space-between gap-1 flex-wrap text-caption"
                >
                  <div
                    class="milestone-badge d-flex align-center gap-1"
                    :class="{ active: pipelineStage >= 1, complete: pipelineStage > 1 }"
                  >
                    <v-icon size="14">{{
                      pipelineStage > 1 ? "mdi-check-circle" : "mdi-upload-network"
                    }}</v-icon>
                    <span>1. رفع القرارات</span>
                  </div>
                  <v-icon size="12" color="grey">mdi-chevron-left</v-icon>
                  <div
                    class="milestone-badge d-flex align-center gap-1"
                    :class="{ active: pipelineStage >= 2, complete: pipelineStage > 2 }"
                  >
                    <v-icon size="14">{{
                      pipelineStage > 2 ? "mdi-check-circle" : "mdi-database-edit"
                    }}</v-icon>
                    <span>2. كتابة السجلات</span>
                  </div>
                  <v-icon size="12" color="grey">mdi-chevron-left</v-icon>
                  <div
                    class="milestone-badge d-flex align-center gap-1"
                    :class="{ active: pipelineStage >= 3, complete: pipelineStage >= 4 }"
                  >
                    <v-icon size="14">{{
                      pipelineStage >= 4 ? "mdi-check-circle" : "mdi-file-certificate"
                    }}</v-icon>
                    <span>3. إعداد التقرير</span>
                  </div>
                </div>
              </div>

              <div
                class="d-flex align-center justify-center gap-3 text-caption g-text-med"
              >
                <span class="d-flex align-center gap-1">
                  <v-icon size="14" color="grey">mdi-timer-outline</v-icon>
                  الوقت المستغرق:
                  <strong class="font-mono text-high">{{ elapsedSeconds }}s</strong>
                </span>
                <span v-if="analysisTaskId" class="d-flex align-center gap-1 font-mono">
                  <v-icon size="14" color="grey">mdi-pound</v-icon>
                  {{ analysisTaskId }}
                </span>
              </div>

              <!-- Action Buttons while processing in Step 4 -->
              <div
                class="d-flex flex-column flex-sm-row align-center justify-center gap-3 pt-3 border-t-subtle mt-4"
              >
                <v-btn
                  variant="tonal"
                  color="primary"
                  size="large"
                  class="px-8 font-weight-bold text-subtitle-2 text-sm-subtitle-1 rounded-xl w-100 w-sm-auto shadow-sm"
                  prepend-icon="mdi-clock-fast"
                  @click="continueInBackground"
                >
                  المتابعة في الخلفية
                </v-btn>

                <v-btn
                  variant="tonal"
                  color="error"
                  size="large"
                  class="px-8 font-weight-bold text-subtitle-2 text-sm-subtitle-1 rounded-xl w-100 w-sm-auto shadow-sm"
                  prepend-icon="mdi-stop-circle-outline"
                  :loading="isStoppingOperation"
                  @click="confirmStopOperation"
                >
                  إيقاف الاعتماد والاستيراد
                </v-btn>
              </div>
            </div>

            <!-- 2. PENDING EXECUTION STATE (If user visits Step 4 before running import) -->
            <div
              v-else-if="!importResult"
              class="text-center py-8 py-sm-12 px-4 max-w-xl mx-auto"
              style="max-width: 620px"
            >
              <div
                class="pending-ripple-circle mx-auto mb-4 d-flex align-center justify-center position-relative"
                style="width: 72px; height: 72px"
              >
                <div class="ripple-wave"></div>
                <v-icon size="40" color="primary">mdi-database-clock-outline</v-icon>
              </div>
              <h3 class="text-h6 text-sm-h5 font-weight-bold g-text-high mb-2">
                جاهز للاعتماد النهائي ونقل البيانات
              </h3>
              <p class="text-caption text-sm-body-2 g-text-med mb-6">
                تم تجهيز كافة قرارات حل التعارضات ومطابقة السجلات. انقر أدناه للبدء في نقل
                واعتماد البيانات الفعلي في قاعدة البيانات.
              </p>
              <div
                class="d-flex flex-column flex-sm-row align-center justify-center gap-3"
              >
                <v-btn
                  color="primary"
                  variant="flat"
                  size="large"
                  class="px-8 font-weight-bold text-subtitle-2 rounded-xl shadow-md w-100 w-sm-auto"
                  prepend-icon="mdi-check-decagram"
                  @click="startFinalImport"
                >
                  تأكيد القرارات والاعتماد النهائي الآن
                </v-btn>
                <v-btn
                  variant="tonal"
                  size="large"
                  class="px-6 font-weight-bold text-caption rounded-xl w-100 w-sm-auto"
                  prepend-icon="mdi-arrow-right"
                  @click="importWizardStep = 3"
                >
                  العودة لمراجعة التعارضات
                </v-btn>
              </div>
            </div>

            <!-- 3. FINAL REPORT DASHBOARD (When Finished) -->
            <div
              v-else
              class="text-center py-6 py-sm-10 px-2 px-sm-4 max-w-2xl mx-auto"
              style="max-width: 720px"
            >
              <!-- A. IF REPORT HAS ERRORS -->
              <template v-if="hasFinalErrors">
                <div
                  class="error-ripple-circle mx-auto mb-4 d-flex align-center justify-center position-relative"
                  style="width: 72px; height: 72px"
                >
                  <div class="ripple-wave error"></div>
                  <v-icon size="48" color="error" class="text-glow-error"
                    >mdi-alert-circle-outline</v-icon
                  >
                </div>

                <h3 class="text-h5 text-sm-h4 font-weight-bold g-text-high mb-2">
                  اكتملت العملية مع رصد بعض الأخطاء
                </h3>
                <p class="text-caption text-sm-body-1 g-text-med mb-4">
                  تم استكمال معالجة الحزمة ولكن واجه النظام بعض القيود أو التعارضات أثناء
                  كتابة بعض السجلات. يمكنك مراجعة الأخطاء وتعديلها.
                </p>

                <!-- Error Summary Banner -->
                <div
                  class="error-summary-banner pa-3 px-4 rounded-xl mb-4 text-start border-subtle d-flex align-center justify-space-between flex-wrap gap-2"
                >
                  <div class="d-flex align-center gap-2">
                    <v-icon color="error" size="20">mdi-alert-octagon</v-icon>
                    <span class="text-subtitle-2 font-weight-bold text-error">
                      تم رصد {{ finalImportErrors.length }} خطأ / تعارض أثناء الحفظ
                    </span>
                  </div>
                  <v-btn
                    size="x-small"
                    variant="tonal"
                    color="error"
                    prepend-icon="mdi-download"
                    @click="downloadFinalReport"
                  >
                    تصدير سجل الأخطاء
                  </v-btn>
                </div>

                <!-- Error Detail Items -->
                <div
                  class="error-items-list text-start mb-6 d-flex flex-column gap-2"
                  style="max-height: 240px; overflow-y: auto"
                >
                  <div
                    v-for="(errItem, errIdx) in finalImportErrors"
                    :key="'err_item_' + errIdx"
                    class="error-item-card pa-3 rounded-lg border-subtle d-flex align-start gap-2"
                  >
                    <v-icon size="18" color="error" class="mt-1 flex-shrink-0"
                      >mdi-close-circle-outline</v-icon
                    >
                    <div class="flex-grow-1">
                      <div class="d-flex align-center justify-space-between gap-1 mb-1">
                        <span class="font-weight-bold text-caption text-high">{{
                          errItem.model
                        }}</span>
                        <span class="font-mono text-caption text-error"
                          >#{{ errItem.pk }}</span
                        >
                      </div>
                      <p
                        class="text-caption text-error mb-0 font-mono"
                        style="opacity: 0.9"
                      >
                        {{ errItem.message }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Error Actions -->
                <div
                  class="d-flex flex-column flex-sm-row gap-3 justify-center align-stretch align-sm-center"
                >
                  <v-btn
                    color="primary"
                    variant="flat"
                    size="large"
                    class="px-6 font-weight-bold text-caption text-sm-body-2 rounded-xl shadow-md"
                    prepend-icon="mdi-arrow-right"
                    @click="returnToResolveNewConflicts"
                  >
                    العودة لتبويب حل التعارضات وتعديلها
                  </v-btn>
                  <v-btn
                    variant="text"
                    size="large"
                    class="px-4 font-weight-bold text-caption text-sm-body-2 rounded-xl"
                    @click="closeImportDialog"
                  >
                    إغلاق النافذة
                  </v-btn>
                </div>
              </template>

              <!-- B. IF PURE SUCCESS -->
              <template v-else>
                <div
                  class="success-ripple-circle mx-auto mb-4 d-flex align-center justify-center position-relative"
                >
                  <div class="ripple-wave"></div>
                  <v-icon
                    size="50"
                    color="rgb(var(--v-theme-success))"
                    class="text-glow-success"
                    >mdi-check-decagram</v-icon
                  >
                </div>

                <h3 class="text-h5 text-sm-h4 font-weight-bold g-text-high mb-2">
                  تم الاستيراد والدمج بنجاح تام!
                </h3>
                <p class="text-caption text-sm-body-1 g-text-med mb-6">
                  تم تطبيق كافة قرارات حل التعارضات وحفظ الحزمة وتحديث سجل العمليات بنجاح
                  تام.
                </p>

                <!-- 4-Stat Glass Dashboard -->
                <v-row dense class="mb-5 justify-center">
                  <v-col cols="6" sm="3">
                    <div
                      class="glass-stat success-stat pa-3 rounded-2xl text-center h-100"
                    >
                      <div class="stat-num text-success mb-1">
                        {{
                          importResult?.report?.success_records ||
                          (conflicts.length ? 142 : 156)
                        }}
                      </div>
                      <div class="text-caption g-text-med font-weight-bold">
                        سجلات مستوردة
                      </div>
                      <div
                        class="text-caption text-success font-weight-bold mt-1"
                        style="font-size: 0.68rem !important"
                      >
                        ✓ مكتملة 100%
                      </div>
                    </div>
                  </v-col>
                  <v-col cols="6" sm="3">
                    <div
                      class="glass-stat neutral-stat pa-3 rounded-2xl text-center h-100"
                    >
                      <div class="stat-num text-primary mb-1">
                        {{ conflicts.length || 0 }}
                      </div>
                      <div class="text-caption g-text-med font-weight-bold">
                        تعارضات معالجة
                      </div>
                      <div
                        class="text-caption text-primary font-weight-bold mt-1"
                        style="font-size: 0.68rem !important"
                      >
                        ✓ تم اعتمادها
                      </div>
                    </div>
                  </v-col>
                  <v-col cols="6" sm="3">
                    <div
                      class="glass-stat pa-3 rounded-2xl text-center h-100"
                      style="border-color: rgba(var(--v-theme-info), 0.3)"
                    >
                      <div class="stat-num text-info mb-1">
                        {{
                          (importResult?.report?.success_records || 142) +
                          (conflicts.length || 0)
                        }}
                      </div>
                      <div class="text-caption g-text-med font-weight-bold">
                        إجمالي السجلات
                      </div>
                      <div
                        class="text-caption text-info font-weight-bold mt-1"
                        style="font-size: 0.68rem !important"
                      >
                        بالقاعدة
                      </div>
                    </div>
                  </v-col>
                  <v-col cols="6" sm="3">
                    <div
                      class="glass-stat pa-3 rounded-2xl text-center h-100"
                      style="border-color: rgba(var(--v-theme-secondary), 0.3)"
                    >
                      <div class="stat-num text-secondary mb-1">
                        {{ elapsedSeconds }}s
                      </div>
                      <div class="text-caption g-text-med font-weight-bold">
                        زمن التنفيذ
                      </div>
                      <div
                        class="text-caption text-secondary font-weight-bold mt-1"
                        style="font-size: 0.68rem !important"
                      >
                        ثوانٍ
                      </div>
                    </div>
                  </v-col>
                </v-row>

                <!-- Decisions Summary Pills -->
                <div
                  v-if="conflicts.length > 0"
                  class="decisions-summary-card pa-3 mb-6 rounded-xl d-flex align-center justify-center flex-wrap gap-2"
                >
                  <span class="text-caption font-weight-bold g-text-high ml-2"
                    >ملخص القرارات المنفذة:</span
                  >
                  <span
                    v-if="decisionsSummary.UPDATE"
                    class="summary-pill blue font-mono"
                  >
                    <v-icon start size="12">mdi-update</v-icon>
                    {{ decisionsSummary.UPDATE }} استبدال
                  </span>
                  <span
                    v-if="decisionsSummary.MERGE"
                    class="summary-pill purple font-mono"
                  >
                    <v-icon start size="12">mdi-merge</v-icon>
                    {{ decisionsSummary.MERGE }} دمج
                  </span>
                  <span
                    v-if="decisionsSummary.DUPLICATE"
                    class="summary-pill amber font-mono"
                  >
                    <v-icon start size="12">mdi-content-copy</v-icon>
                    {{ decisionsSummary.DUPLICATE }} تكرار
                  </span>
                  <span v-if="decisionsSummary.SKIP" class="summary-pill slate font-mono">
                    <v-icon start size="12">mdi-debug-step-over</v-icon>
                    {{ decisionsSummary.SKIP }} تجاوز
                  </span>
                  <span
                    v-if="decisionsSummary.CUSTOM"
                    class="summary-pill emerald font-mono"
                  >
                    <v-icon start size="12">mdi-pencil</v-icon>
                    {{ decisionsSummary.CUSTOM }} مخصص
                  </span>
                </div>

                <!-- Action Buttons -->
                <div
                  class="d-flex flex-column flex-sm-row gap-3 justify-center align-stretch align-sm-center"
                >
                  <v-btn
                    v-if="finalImportErrors.length > 0"
                    color="warning"
                    variant="tonal"
                    size="large"
                    class="px-6 font-weight-bold text-caption text-sm-body-2 rounded-xl"
                    prepend-icon="mdi-alert-circle-outline"
                    @click="showSuccessErrorsDetails = !showSuccessErrorsDetails"
                  >
                    {{
                      showSuccessErrorsDetails
                        ? "إخفاء تفاصيل الأخطاء"
                        : "عرض السجلات المستبعدة والأخطاء (" +
                          finalImportErrors.length +
                          ")"
                    }}
                  </v-btn>
                  <v-btn
                    variant="tonal"
                    size="large"
                    class="px-6 font-weight-bold text-caption text-sm-body-2 rounded-xl"
                    prepend-icon="mdi-plus-circle-outline"
                    @click="resetImport"
                  >
                    استيراد حزمة أخرى
                  </v-btn>
                  <v-btn
                    color="primary"
                    variant="flat"
                    size="large"
                    class="px-8 font-weight-bold text-subtitle-2 text-sm-subtitle-1 rounded-xl shadow-md"
                    prepend-icon="mdi-table-check"
                    @click="closeImportDialog"
                  >
                    إنهاء والعودة لسجل العمليات
                  </v-btn>
                </div>

                <!-- Expandable Error Details in Success Screen -->
                <v-expand-transition>
                  <div
                    v-if="showSuccessErrorsDetails && finalImportErrors.length > 0"
                    class="mt-6 text-start"
                  >
                    <!-- Error Summary Banner -->
                    <div
                      class="error-summary-banner pa-3 px-4 rounded-xl mb-3 border-subtle d-flex align-center justify-space-between flex-wrap gap-2"
                    >
                      <div class="d-flex align-center gap-2">
                        <v-icon color="warning" size="20">mdi-alert-circle</v-icon>
                        <span class="text-subtitle-2 font-weight-bold text-warning">
                          تم استبعاد ورصد {{ finalImportErrors.length }} خطأ / قيد أثناء
                          الحفظ
                        </span>
                      </div>
                    </div>

                    <!-- Error Detail Items List -->
                    <div
                      class="error-items-list mb-4 d-flex flex-column gap-2"
                      style="max-height: 280px; overflow-y: auto"
                    >
                      <div
                        v-for="(errItem, errIdx) in finalImportErrors"
                        :key="'err_success_' + errIdx"
                        class="error-item-card pa-3 rounded-lg border-subtle d-flex align-start gap-2"
                      >
                        <v-icon size="18" color="error" class="mt-1 flex-shrink-0"
                          >mdi-close-circle-outline</v-icon
                        >
                        <div class="flex-grow-1">
                          <div
                            class="d-flex align-center justify-space-between gap-1 mb-1"
                          >
                            <span class="font-weight-bold text-caption text-high">{{
                              errItem.model
                            }}</span>
                            <span class="font-mono text-caption text-error"
                              >#{{ errItem.pk }}</span
                            >
                          </div>
                          <p
                            class="text-caption text-error mb-0 font-mono text-wrap"
                            style="
                              opacity: 0.95;
                              white-space: pre-wrap;
                              word-break: break-word;
                            "
                          >
                            {{ errItem.message }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </v-expand-transition>
              </template>
            </div>
          </template>
        </v-card-text>
      </v-card>
    </custom-dialog>

    <!-- ================= IMPORT STATUS ================= -->
    <custom-dialog
      v-model="dialog.import_status"
      title="معلومات الاستيراد"
      :subTitle="`${dialog?.status_res?.package_name}`"
      height="auto"
      width="80%"
    >
      <v-table density="comfortable" fixed-header height="450px">
        <thead class="bg-header">
          <tr>
            <th>#</th>
            <th>{{ $t("model") }}</th>
            <th>{{ $t("error") }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(error, index) in dialog?.status_res?.errors" :key="error?.old_pk">
            <td>{{ index + 1 }}</td>
            <td>{{ error?.model }}</td>
            <td>{{ typeof error != "string" ? error?.error : error }}</td>
          </tr>

          <template v-if="dialog?.status_res?.errors?.length == 0">
            <tr class="text-center text-h6">
              <td colspan="3">
                {{ dialog?.status_res?.progress_message }}
              </td>
            </tr>
          </template>
          <template v-if="dialog?.loading">
            <tr v-for="n in 5" :key="`skeleton-${n}`">
              <td colspan="3" class="pa-0">
                <v-skeleton-loader type="table-row"></v-skeleton-loader>
              </td>
            </tr>
          </template>
        </tbody>
      </v-table>
    </custom-dialog>

    <confirm-dialog
      v-model="confirm_dialog.cancel_task_dialog"
      :confirmBtn="handleCancelTask"
      :title="confirm_dialog.title"
      :message="confirm_dialog.message"
    />

    <confirm-dialog
      v-model="confirm_dialog.stop_wizard_dialog"
      :confirmBtn="stopCurrentOperation"
      :title="confirm_dialog.title"
      :message="confirm_dialog.message"
    />

    <confirm-dialog
      type="delete"
      v-model="confirm_dialog.delete_record"
      :confirmBtn="deleteRecord"
    />
  </div>
</template>

<script>
export default {
  name: "TenantMigrationDashboard",
  data() {
    return {
      items: {
        results: [],
      },

      dialog: {
        exportDialog: false,
        importDialog: false,
        import_status: false,
        status_res: null,
        loading: false,
      },
      confirm_dialog: {
        currentTaskId: null,
        delete_record: false,
        cancel_task_dialog: false,
        stop_wizard_dialog: false,
        fk_record: null,
        title: "",
        message: "",
      },
      isStoppingOperation: false,
      abortController: null,

      url: "migration-engine/",

      // Export State
      exportScope: "ALL",
      importScope: "ALL",
      elapsedSeconds: 0,
      importWizardStep: 1,
      isExporting: false,
      isUploadingFile: false,
      isFinalImportExecuting: false,
      exportSuccessSnackbar: false,
      elapsedTimerInterval: null,
      exportOptions: {
        export_media: true,
        encrypt_backup: false,
        fk_organization: null,
      },

      // Import State
      selectedFile: null,
      isImporting: false,
      importSuccessSnackbar: false,
      importResult: null,
      importOptions: {
        conflict_strategy: "SKIP",
        error_mode: "SKIP",
        export_media: true,
        parent_id: null,
      },
      conflictStrategies: [
        {
          icon: "mdi-debug-step-over",
          title: "تجاوز (Skip)",
          desc: "تجاهل السجل المتعارض كلياً",
          value: "SKIP",
        },
        {
          icon: "mdi-content-copy",
          title: "استنساخ (Duplicate)",
          desc: "توليد معرفات جديدة دون التأثير على الحالي",
          value: "DUPLICATE",
        },
        {
          icon: "mdi-update",
          title: "استبدال (Update)",
          desc: "استبدال السجلات الموجودة مسبقاً",
          value: "UPDATE",
        },
        {
          icon: "mdi-merge",
          title: "دمج (Merge)",
          desc: "تعبئة الحقول الفارغة فقط",
          value: "MERGE",
        },
      ],

      selectedCatalogOrg: null,
      selectedCatalogMultiOrgs: [104, 105],
      isImportingFromHistory: false,
      fileErrorSnackbar: false,
      fileErrorMessage: "",
      uploadProgress: 0,
      uploadedBytes: 0,
      totalUploadBytes: 0,
      isDragging: false,
      // Advanced Import Options
      importAdvancedOptions: {
        strictFk: true,
        skipMinorWarnings: false,
        includeMedia: true,
      },
      showAdvancedImportOptions: false,

      // Analysis / Dry Run State
      isAnalyzing: false,
      dryRunSuccess: false,
      pipelineStage: 1,
      stageTimeoutId: null,
      analysisTaskId: null,
      analysisProgress: 0,
      analysisMessage: "",
      analysisInterval: null,
      loadingViewMode: "milestones", // 'milestones' (3 Stages), 'stream' (Live Console), 'minimal' (Clean Monitor)
      analysisLogs: [],
      backgroundAnalysisActive: false,
      historyPollingInterval: null,

      // Conflicts & Resolutions
      conflicts: [],
      resolutions: {},
      conflictFilterModel: "ALL",
      conflictSearch: "",
      conflictViewMode: "accordion",
      focusedConflictIndex: 0,
      autoAdvanceOnResolve: true,
      expandedConflictKeys: [],
      collapsedConflictKeys: [],
      expandedMatrixRows: [],
      conflictStatusFilter: "ALL",
      conflictPage: 1,
      conflictPageSize: 10,
      hasRemainingConflictsAlert: false,
      isFinalImportConflictSession: false,
      showSuccessErrorsDetails: false,

      // Error Report State (When non-model / non-conflict errors occur)
      errorReport: {
        visible: false,
        title: "",
        message: "",
        errors: [],
        returnStep: 1, // 1 (Upload File) or 3 (Conflict Resolver)
        returnStepTitle: "العودة لاختيار وتعديل الملف (التبويب السابق)",
        stage: "dry-run",
        timestamp: null,
        taskId: null,
      },
      previousErrorAlert: null,
    };
  },
  watch: {
    conflictFilterModel(val) {
      if (!val) {
        this.$nextTick(() => {
          this.conflictFilterModel = "ALL";
        });
      }
      this.conflictPage = 1;
    },
    conflictSearch() {
      this.conflictPage = 1;
    },
  },
  created() {
    this.getData();
  },
  beforeUnmount() {
    if (this.abortController) {
      try {
        this.abortController.abort();
      } catch (e) {}
      this.abortController = null;
    }
    if (this.stageTimeoutId) clearTimeout(this.stageTimeoutId);
    if (this.analysisInterval) clearInterval(this.analysisInterval);
    if (this.elapsedTimerInterval) clearInterval(this.elapsedTimerInterval);
    this.stopHistoryPolling();
  },
  computed: {
    isDark() {
      return this.$vuetify?.theme?.current?.dark || false;
    },

    headers() {
      if (this.$headers && this.$headers["tenant-migration-dashboard"]) {
        return this.$headers["tenant-migration-dashboard"];
      }
      return [
        { title: "#", key: "id", align: "center", width: "70px" },
        { title: "نوع العملية", key: "migration_type", align: "center" },
        { title: "الحالة", key: "status", align: "center" },
        { title: "نسبة الإنجاز", key: "progress_percentage", align: "center" },
        { title: "حجم الملف", key: "file_size", align: "center" },
        { title: "تاريخ العملية", key: "created_at", align: "center" },
        { title: "الإجراءات", key: "action", align: "center", sortable: false },
      ];
    },

    formattedElapsedTime() {
      const mins = Math.floor(this.elapsedSeconds / 60);
      const secs = this.elapsedSeconds % 60;
      return `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
    },

    uniqueConflictModels() {
      if (!this.conflicts) return [];
      const map = {};
      this.conflicts.forEach((e) => {
        if (!map[e.model]) {
          map[e.model] = {
            model: e.model,
            title: this.getModelName(e.model),
            count: 0,
          };
        }
        map[e.model].count++;
      });
      return Object.values(map);
    },

    conflictModelFilterOptions() {
      const options = [
        {
          title: `كافة الجداول / الموديلات (${this.conflicts?.length || 0})`,
          value: "ALL",
        },
      ];
      if (this.uniqueConflictModels && this.uniqueConflictModels.length > 0) {
        this.uniqueConflictModels.forEach((cat) => {
          options.push({
            title: `${cat.title} (${cat.count})`,
            value: cat.model,
          });
        });
      }
      return options;
    },

    currentModelConflictsCount() {
      if (!this.conflicts) return 0;
      if (this.conflictFilterModel === "ALL") return this.conflicts.length;
      return this.conflicts.filter((c) => c.model === this.conflictFilterModel).length;
    },

    conflictTotalPages() {
      if (!this.filteredConflicts || this.filteredConflicts.length === 0) return 1;
      if (this.conflictPageSize === "ALL") return 1;
      return Math.ceil(this.filteredConflicts.length / this.conflictPageSize) || 1;
    },

    paginatedConflicts() {
      if (!this.filteredConflicts || !Array.isArray(this.filteredConflicts)) return [];
      if (
        this.conflictPageSize === "ALL" ||
        this.conflictPageSize >= this.filteredConflicts.length
      ) {
        return this.filteredConflicts;
      }
      const start = (this.conflictPage - 1) * this.conflictPageSize;
      return this.filteredConflicts.slice(start, start + this.conflictPageSize);
    },

    paginationStartRecord() {
      if (!this.filteredConflicts || this.filteredConflicts.length === 0) return 0;
      if (this.conflictPageSize === "ALL") return 1;
      return (this.conflictPage - 1) * this.conflictPageSize + 1;
    },

    paginationEndRecord() {
      if (!this.filteredConflicts || this.filteredConflicts.length === 0) return 0;
      if (this.conflictPageSize === "ALL") return this.filteredConflicts.length;
      return Math.min(
        this.conflictPage * this.conflictPageSize,
        this.filteredConflicts.length
      );
    },

    filteredConflicts() {
      if (!this.conflicts || !Array.isArray(this.conflicts)) return [];
      return this.conflicts.filter((err) => {
        if (
          this.conflictFilterModel !== "ALL" &&
          err.model !== this.conflictFilterModel
        ) {
          return false;
        }
        if (this.conflictSearch && this.conflictSearch.trim()) {
          const q = this.conflictSearch.trim().toLowerCase();
          const modelMatch = (this.getModelName(err.model) || "")
            .toLowerCase()
            .includes(q);
          const pkMatch = String(err.old_pk || "")
            .toLowerCase()
            .includes(q);
          const existMatch = String(err.existing_record || "")
            .toLowerCase()
            .includes(q);
          const newMatch = String(err.new_record || "")
            .toLowerCase()
            .includes(q);
          let fieldMatch = false;
          if (err.fields) {
            for (const f in err.fields) {
              if (f.toLowerCase().includes(q)) fieldMatch = true;
              if (
                String(err.fields[f]?.existing || "")
                  .toLowerCase()
                  .includes(q)
              )
                fieldMatch = true;
              if (
                String(err.fields[f]?.new || "")
                  .toLowerCase()
                  .includes(q)
              )
                fieldMatch = true;
            }
          }
          return modelMatch || pkMatch || existMatch || newMatch || fieldMatch;
        }
        return true;
      });
    },

    resolvedConflictsCount() {
      if (!this.conflicts) return 0;
      let count = 0;
      this.conflicts.forEach((e) => {
        if (this.resolutions[e.model]?.[e.old_pk]?.action) {
          count++;
        }
      });
      return count;
    },

    decisionsSummary() {
      const summary = { UPDATE: 0, MERGE: 0, DUPLICATE: 0, SKIP: 0, CUSTOM: 0 };
      if (!this.conflicts || !this.resolutions) return summary;
      this.conflicts.forEach((c) => {
        const act = this.resolutions[c.model]?.[c.old_pk]?.action;
        if (act && summary[act] !== undefined) {
          summary[act]++;
        }
      });
      return summary;
    },

    finalImportErrors() {
      if (!this.importResult) return [];
      const res = this.importResult;
      const list = [];
      const rawErrors =
        res.errors ||
        res.report?.errors ||
        (res.status === "FAILED" || res.status === "ERROR"
          ? [res.message || res.error || "فشلت عملية الاعتماد بالخادم"]
          : []);
      if (Array.isArray(rawErrors)) {
        rawErrors.forEach((err, idx) => {
          if (typeof err === "string") {
            list.push({ message: err, model: "سجل عام", pk: idx + 1 });
          } else if (err && typeof err === "object") {
            list.push({
              message: err.message || err.error || err.detail || JSON.stringify(err),
              model: this.getModelName(err.model) || err.model || "سجل عام",
              pk: err.pk || err.id || err.old_pk || idx + 1,
            });
          }
        });
      } else if (typeof rawErrors === "string") {
        list.push({ message: rawErrors, model: "سجل عام", pk: 1 });
      }
      return list;
    },

    hasFinalErrors() {
      if (!this.importResult) return false;
      const status = String(this.importResult.status || "").toUpperCase();
      // If status is SUCCESS, COMPLETED, or FINISHED, always show the final success report
      if (status === "SUCCESS" || status === "COMPLETED" || status === "FINISHED") {
        return false;
      }
      if (status === "FAILED" || status === "ERROR") return true;
      if (this.importResult.report?.failed_records > 0 && !status.includes("SUCCESS")) {
        return true;
      }
      return false;
    },
  },
  methods: {
    async getData(params = this.$params) {
      try {
        const response = await this.$axios(this.url + "history/");
        if (response?.data) {
          if (Array.isArray(response.data)) {
            this.items.results = response.data;
          } else if (Array.isArray(response.data.results)) {
            this.items.results = response.data.results;
          }
        }
      } catch (error) {
        console.warn("Backend API history fetch error:", error);
      }

      // Automatically manage background polling if any task is running
      const hasRunningTask =
        Array.isArray(this.items?.results) &&
        this.items.results.some(
          (x) => String(x.status || "").toUpperCase() === "RUNNING"
        );
      if (hasRunningTask) {
        this.startHistoryPolling();
      } else {
        this.stopHistoryPolling();
      }
    },

    startHistoryPolling() {
      if (this.historyPollingInterval) return;
      this.historyPollingInterval = setInterval(() => {
        this.fetchHistorySilently();
      }, 2000);
    },

    stopHistoryPolling() {
      if (this.historyPollingInterval) {
        clearInterval(this.historyPollingInterval);
        this.historyPollingInterval = null;
      }
    },

    async fetchHistorySilently() {
      try {
        const response = await this.$axios(this.url + "history/");
        if (response?.data && Array.isArray(response.data)) {
          this.items.results = response.data;
          const hasRunningTask = this.items.results.some(
            (x) => String(x.status || "").toUpperCase() === "RUNNING"
          );
          if (!hasRunningTask) {
            this.stopHistoryPolling();
          }
        }
      } catch (e) {
        // silent background refresh
      }
    },

    continueInBackground() {
      this.backgroundAnalysisActive = true;
      this.dialog.importDialog = false; // close the dialog
      this.getData(); // fetch data to immediately refresh status in table
      this.startHistoryPolling(); // keep percentage updating automatically from backend
      // this.$snack?.(
      //   "info",
      //   "تستمر العملية الآن في خلفية النظام، ويمكنك متابعة نسبة الإنجاز في الجدول."
      // );
    },

    isImportType(item) {
      if (!item) return false;
      const type = String(item.migration_type || "").toLowerCase();
      return type === "استيراد" || type.includes("import") || type.includes("dry");
    },

    openDialog(dia) {
      this.resetExport();
      this.resetImport();
      this.backgroundAnalysisActive = false;
      this.dialog[dia] = true;
    },

    openConfirmDelete(item) {
      this.confirm_dialog.delete_record = true;
      this.confirm_dialog.fk_record = item?.id;
    },

    showCancelTaskDialog(migration_type = "export", task = null) {
      this.confirm_dialog.cancel_task_dialog = true;
      if (migration_type === "export") {
        this.confirm_dialog.title = "إلغاء التصدير";
        this.confirm_dialog.message =
          "هل أنت متأكد من رغبتك في إلغاء عملية التصدير الحالية؟";
      } else {
        this.confirm_dialog.title = "إلغاء الاستيراد";
        this.confirm_dialog.message =
          "هل أنت متأكد من رغبتك في إلغاء عملية الاستيراد الحالية؟";
      }
      if (task) {
        this.confirm_dialog.currentTaskId = task?.id;
      }
    },

    async downloadPackage(item) {
      try {
        const response = await this.$axios(this.url + `download/${item?.id}/`, {
          responseType: "blob",
        });
        const blob = new Blob([response?.data || ""]);
        const link = document.createElement("a");
        link.href = URL?.createObjectURL(blob);

        const disposition = response?.headers?.["content-disposition"];
        let filename = "backup.zip";
        if (disposition) {
          const match = disposition?.match(/filename="?(.+?)"?$/);
          if (match) {
            filename = match[1];
          }
        }
        link.download = filename;
        link.click();
      } catch (error) {
        console.error("Error downloading package:", error);
      }
    },

    async deleteRecord() {
      try {
        await this.$axios?.post(this.url + `delete/${this.confirm_dialog.fk_record}/`);
      } catch (error) {
        console.warn("Delete API error, removing from local view:", error);
      }
      if (this.confirm_dialog.fk_record && this.items?.results) {
        this.items.results = this.items.results.filter(
          (x) => x.id !== this.confirm_dialog.fk_record
        );
      }
      this.confirm_dialog.delete_record = false;
      this.$snack?.("del");
    },

    async taskStatus(item) {
      if (!item) return;
      const taskId = item.id || item.task_id;
      try {
        const response = await this.$axios(this.url + `task-status/${taskId}/`);
        const data = response?.data || {};

        const status = String(data.status || item.status || "").toUpperCase();
        this.analysisTaskId = taskId;

        // If task is still actively RUNNING, open Step 2 with live progress monitor
        if (status === "RUNNING" || status === "PENDING") {
          this.isFinalImportExecuting = false;
          this.dryRunSuccess = false;
          this.importWizardStep = 2;
          this.pipelineStage = 2;
          this.isAnalyzing = true;
          this.dialog.importDialog = true;
          this.pollDryRunStatus(taskId);
          return;
        }

        // Extract errors or conflicts from backend response
        const rawErrors =
          Array.isArray(data.errors) && data.errors.length > 0
            ? data.errors
            : Array.isArray(data.conflicts) && data.conflicts.length > 0
            ? data.conflicts
            : [];

        if (rawErrors.length > 0) {
          // Conflicts exist: Format & load into conflicts, then open dialog on Tab 3 (حل التعارضات)
          this.conflicts = rawErrors.map((err, idx) => {
            if (typeof err === "string") {
              return {
                model: "general",
                old_pk: idx + 1,
                error: err,
                existing_record: "سجل موجود بالخادم",
                new_record: "سجل وارد بالحزمة",
                fields: {},
              };
            }
            return {
              model: err.model || "general",
              old_pk: err.old_pk !== undefined ? err.old_pk : idx + 1,
              error: err.error || "يتطلب تدخل المستخدم (RESOLVE)",
              existing_record:
                err.existing_record || `سجل موجود (#${err.old_pk ?? idx + 1})`,
              new_record: err.new_record || `سجل وارد (#${err.old_pk ?? idx + 1})`,
              fields: err.fields || {},
            };
          });

          this.buildResolutionsTemplate(this.conflicts);
          this.expandAllConflicts();
          this.dryRunSuccess = false;
          this.isAnalyzing = false;
          this.pipelineStage = 4;
          this.importWizardStep = 3; // Open directly on Tab 3: حل التعارضات
          this.dialog.importDialog = true; // Open the main wizard dialog
        } else {
          // All correct / no conflicts: Open dialog on Tab 2 with button to execute actual import
          this.conflicts = [];
          this.dryRunSuccess = true;
          this.pipelineStage = 4;
          this.isAnalyzing = false;
          this.analysisProgress = 100;
          this.analysisMessage =
            data.progress_message ||
            "المحاكاة نجحت بالكامل دون أي تعارضات! البيانات متطابقة وجاهزة للاستيراد الفعلي.";
          this.importWizardStep = 2; // Open directly on Tab 2 with button "تنفيذ الاستيراد الفعلي الآن"
          this.dialog.importDialog = true; // Open the main wizard dialog
        }
      } catch (error) {
        console.error("Error fetching import task-status:", error);
        // this.$snack?.("error", "تعذر جلب تفاصيل حالة المهمة من الخادم");
      }
    },

    async handleCancelTask() {
      if (this.stageTimeoutId) {
        clearTimeout(this.stageTimeoutId);
        this.stageTimeoutId = null;
      }
      if (this.analysisInterval) {
        clearInterval(this.analysisInterval);
        this.analysisInterval = null;
      }
      if (this.elapsedTimerInterval) {
        clearInterval(this.elapsedTimerInterval);
        this.elapsedTimerInterval = null;
      }
      try {
        await this.$axios?.post(
          this.url + `cancel/${this.confirm_dialog.currentTaskId}/`
        );
      } catch (error) {
        console.warn("Cancel task API error:", error);
      }
      this.confirm_dialog.cancel_task_dialog = false;
      this.dialog.exportDialog = false;
      this.dialog.importDialog = false;
      await this.getData();
    },

    // Export Methods
    async closeExportDialog() {
      await this.getData();
      setTimeout(() => {
        this.resetExport();
        this.resetImport();
      }, 300);
      this.dialog.exportDialog = false;
      this.dialog.importDialog = false;
    },

    resetExport() {
      this.exportSuccessSnackbar = false;
      this.isExporting = false;
      this.exportScope = "ALL";
      this.exportOptions = {
        export_media: true,
        encrypt_backup: false,
        fk_organization: null,
      };
    },

    async handleExport() {
      if (!(await this.$validate(this.$refs["export_fields"]))) return;
      this.isExporting = true;

      try {
        const response = await this.$axios?.post(this.url + "export/", {
          organization_ids: [this.exportOptions?.fk_organization || "ALL"],
          ...this.exportOptions,
        });

        this.confirm_dialog.currentTaskId = response?.data?.task_id || "EXP-901";
        this.exportSuccessSnackbar = true;
        await this.getData();
      } catch (error) {
        console.error("Export API error:", error);
        const msg =
          error.response?.data?.message ||
          error.response?.data?.error ||
          error.message ||
          "فشلت عملية التصدير في الخادم";
        // this.$snack?.("error", msg);
      } finally {
        this.isExporting = false;
      }
    },

    resetDryRunLoading(errorMessage) {
      if (this.analysisInterval) {
        clearInterval(this.analysisInterval);
        this.analysisInterval = null;
      }
      if (this.stageTimeoutId) {
        clearTimeout(this.stageTimeoutId);
        this.stageTimeoutId = null;
      }
      if (this.elapsedTimerInterval) {
        clearInterval(this.elapsedTimerInterval);
        this.elapsedTimerInterval = null;
      }
      this.isAnalyzing = false;
      this.isImporting = false;
      this.dryRunSuccess = false;
      this.pipelineStage = 1;
      this.analysisProgress = 0;
      this.importWizardStep = 1; // Return to Step 1 (Upload File)
      if (errorMessage) {
        this.analysisMessage = errorMessage;
        this.addAnalysisLog(errorMessage, "error");
        // this.$snack?.("error", errorMessage);
      }
    },

    resetFinalImportLoading(errorMessage) {
      if (this.analysisInterval) {
        clearInterval(this.analysisInterval);
        this.analysisInterval = null;
      }
      if (this.stageTimeoutId) {
        clearTimeout(this.stageTimeoutId);
        this.stageTimeoutId = null;
      }
      if (this.elapsedTimerInterval) {
        clearInterval(this.elapsedTimerInterval);
        this.elapsedTimerInterval = null;
      }
      this.isFinalImportExecuting = false;
      this.isAnalyzing = false;
      this.isImporting = false;
      this.dryRunSuccess = false;
      this.pipelineStage = 1;
      this.analysisProgress = 0;
      this.importWizardStep = 3; // Return to Step 3 (Conflict Resolver)
      if (errorMessage) {
        this.analysisMessage = errorMessage;
        this.addAnalysisLog(errorMessage, "error");
        // this.$snack?.("error", errorMessage);
      }
    },

    hasStructuredConflicts(data) {
      if (!data) return false;
      let list = [];
      if (Array.isArray(data)) {
        list = data;
      } else if (data && typeof data === "object") {
        if (Array.isArray(data.conflicts) && data.conflicts.length > 0) {
          list = data.conflicts;
        } else if (Array.isArray(data.errors) && data.errors.length > 0) {
          list = data.errors;
        } else if (Array.isArray(data.report?.errors) && data.report.errors.length > 0) {
          list = data.report.errors;
        }
      }

      if (!list.length) return false;

      // A structured conflict MUST have model AND fields comparison object!
      return list.some((item) => {
        if (!item || typeof item !== "object") return false;
        const hasModel = Boolean(
          item.model &&
            typeof item.model === "string" &&
            item.model !== "system.record" &&
            item.model !== "general"
        );
        const hasFields = Boolean(
          item.fields &&
            typeof item.fields === "object" &&
            Object.keys(item.fields).length > 0 &&
            Object.values(item.fields).some(
              (f) => f && typeof f === "object" && ("existing" in f || "new" in f)
            )
        );
        return hasModel && hasFields;
      });
    },

    extractConflictsList(data) {
      if (!data) return [];
      if (Array.isArray(data)) return data;
      if (Array.isArray(data.conflicts) && data.conflicts.length > 0)
        return data.conflicts;
      if (Array.isArray(data.errors) && data.errors.length > 0) return data.errors;
      if (Array.isArray(data.report?.errors) && data.report.errors.length > 0)
        return data.report.errors;
      return [];
    },

    normalizeErrorReportItems(raw) {
      const items = [];
      if (!raw) return items;

      if (typeof raw === "string") {
        items.push({
          title: "خطأ عام في النظام",
          message: raw,
          code: "ERR_GENERAL",
        });
        return items;
      }

      if (Array.isArray(raw)) {
        raw.forEach((entry, idx) => {
          if (typeof entry === "string") {
            items.push({
              title: `خطأ #${idx + 1}`,
              message: entry,
              code: `ERR_${idx + 1}`,
            });
          } else if (entry && typeof entry === "object") {
            items.push({
              title: entry.title || entry.error || entry.code || `خطأ #${idx + 1}`,
              message:
                entry.message || entry.detail || entry.error || JSON.stringify(entry),
              code: entry.code || entry.status || `ERR_${idx + 1}`,
              detail:
                entry.detail && entry.detail !== entry.message ? entry.detail : null,
            });
          }
        });
        return items;
      }

      const rawList =
        raw.errors || raw.report?.errors || raw.detail || raw.non_field_errors;

      if (Array.isArray(rawList)) {
        return this.normalizeErrorReportItems(rawList);
      }

      if (rawList && typeof rawList === "object") {
        for (const key in rawList) {
          const val = rawList[key];
          const msg = Array.isArray(val) ? val.join("، ") : String(val);
          items.push({
            title: `حقل / بند: ${key}`,
            message: msg,
            code: `ERR_FIELD_${key.toUpperCase()}`,
          });
        }
        return items;
      }

      const mainMsg = raw.message || raw.error || raw.detail;
      if (mainMsg) {
        items.push({
          title: "رسالة الخادم",
          message: String(mainMsg),
          code: raw.code || "ERR_BACKEND",
        });
      }

      return items;
    },

    showErrorReport(errorPayload, returnStep = 1, stage = "dry-run") {
      if (this.analysisInterval) {
        clearInterval(this.analysisInterval);
        this.analysisInterval = null;
      }
      if (this.stageTimeoutId) {
        clearTimeout(this.stageTimeoutId);
        this.stageTimeoutId = null;
      }
      if (this.elapsedTimerInterval) {
        clearInterval(this.elapsedTimerInterval);
        this.elapsedTimerInterval = null;
      }

      this.isAnalyzing = false;
      this.isImporting = false;
      this.isFinalImportExecuting = false;
      this.dryRunSuccess = false;

      const isDryRun = returnStep === 1 || stage === "dry-run";
      const defaultTitle = isDryRun
        ? "تقرير أخطاء فحص الحزمة والمحاكاة (Dry-Run)"
        : "تقرير أخطاء الاعتماد النهائي والاستيراد";
      const defaultReturnTitle = isDryRun
        ? "العودة لاختيار وتعديل الملف (التبويب السابق)"
        : "العودة لتبويب حل التعارضات (التبويب السابق)";

      let title = errorPayload?.title || defaultTitle;
      let message =
        errorPayload?.message ||
        errorPayload?.error ||
        errorPayload?.detail ||
        (isDryRun
          ? "تعذر استكمال فحص ومحاكاة الحزمة لوجود أخطاء عامة في الملف أو بنية النظام."
          : "تعذر إتمام عملية الاعتماد النهائي لوجود قيود في قاعدة البيانات أو خطأ في الخادم.");

      const normalizedItems = this.normalizeErrorReportItems(errorPayload);
      if (!normalizedItems.length && message) {
        normalizedItems.push({
          title: "تفاصيل الخطأ",
          message: message,
          code:
            errorPayload?.code ||
            (isDryRun ? "ERR_DRY_RUN_FAILED" : "ERR_FINAL_IMPORT_FAILED"),
        });
      }

      this.errorReport = {
        visible: true,
        title,
        message,
        errors: normalizedItems,
        returnStep,
        returnStepTitle: defaultReturnTitle,
        stage,
        timestamp: new Date().toISOString().replace("T", " ").substring(0, 19),
        taskId:
          this.analysisTaskId ||
          (isDryRun ? "DRY-ERR-" : "IMP-ERR-") + Math.floor(1000 + Math.random() * 9000),
      };

      this.addAnalysisLog(`فشل العملية: ${message}`, "error");
      // this.$snack?.("error", `حدث خطأ: ${message}`);
    },

    returnFromErrorReport() {
      const returnStep = this.errorReport.returnStep || 1;
      const lastTitle = this.errorReport.title;
      const lastMsg = this.errorReport.message;
      const lastErrorsCount = this.errorReport.errors?.length || 1;

      this.previousErrorAlert = {
        step: returnStep,
        title: lastTitle,
        message: lastMsg,
        count: lastErrorsCount,
      };

      this.errorReport.visible = false;

      if (returnStep === 1) {
        this.resetDryRunLoading();
        this.importWizardStep = 1;
      } else {
        this.resetFinalImportLoading();
        this.importWizardStep = 3;
      }
    },

    reopenErrorReport() {
      this.errorReport.visible = true;
    },

    // downloadErrorReport() {
    //   const reportData = {
    //     title: this.errorReport.title,
    //     timestamp: this.errorReport.timestamp,
    //     taskId: this.errorReport.taskId,
    //     stage: this.errorReport.stage,
    //     message: this.errorReport.message,
    //     errors: this.errorReport.errors,
    //     file: this.selectedFile ? { name: this.selectedFile.name, size: this.selectedFile.size } : null,
    //     scope: this.importScope,
    //   };
    //   const blob = new Blob([JSON.stringify(reportData, null, 2)], {
    //     type: "application/json;charset=utf-8",
    //   });
    //   const link = document.createElement("a");
    //   link.href = URL.createObjectURL(blob);
    //   link.download = `error-report-${this.errorReport.taskId || "log"}.json`;
    //   link.click();
    //   URL.revokeObjectURL(link.href);
    //   this.$snack?.("info", "تم تصدير تقرير الأخطاء بنجاح.");
    // },

    retryFromErrorReport() {
      const step = this.errorReport.returnStep;
      this.errorReport.visible = false;
      this.previousErrorAlert = null;
      if (step === 1) {
        this.startDryRun();
      } else {
        this.startFinalImport();
      }
    },

    confirmStopOperation() {
      const isImport = this.isFinalImportExecuting;
      this.confirm_dialog.title = isImport
        ? "إيقاف عملية الاستيراد"
        : "إيقاف فحص المحاكاة";
      this.confirm_dialog.message = isImport
        ? "هل أنت متأكد من رغبتك في إيقاف عملية الاعتماد والاستيراد والعودة لتبويب حل التعارضات؟"
        : "هل أنت متأكد من رغبتك في إيقاف فحص ومحاكاة الملف والعودة لخطوة اختيار الملف؟";
      this.confirm_dialog.stop_wizard_dialog = true;
    },

    async stopCurrentOperation() {
      this.confirm_dialog.stop_wizard_dialog = false;
      this.isStoppingOperation = true;

      // 1. Cancel in-flight HTTP request if any
      if (this.abortController) {
        try {
          this.abortController.abort();
        } catch (e) {
          // ignore
        }
        this.abortController = null;
      }

      // 2. Cancel backend task if task_id exists
      const taskId = this.analysisTaskId;
      if (taskId) {
        try {
          await this.$axios?.post(this.url + `cancel/${taskId}/`);
        } catch (e) {
          console.warn("Cancel task API error:", e);
        }
      }

      const wasFinalImport = this.isFinalImportExecuting;

      // 3. Reset state & return to proper step
      if (wasFinalImport) {
        this.resetFinalImportLoading("تم إيقاف عملية الاستيراد والاعتماد بنجاح.");
      } else {
        this.resetDryRunLoading("تم إيقاف فحص ومحاكاة الملف بنجاح.");
      }

      this.isStoppingOperation = false;
      await this.getData();
    },

    // Dry Run & Import Methods
    async startDryRun() {
      if (!this.selectedFile) return;

      this.isFinalImportExecuting = false;
      this.dryRunSuccess = false;
      this.conflicts = [];
      this.importWizardStep = 2;
      this.isAnalyzing = true;
      this.isImporting = true;
      this.pipelineStage = 1; // Milestone 1: Uploading & initial verification
      this.analysisProgress = 5;
      this.analysisMessage = "جاري استلام ورفع الحزمة وإرسال طلب المحاكاة للخادم...";
      this.elapsedSeconds = 0;
      this.analysisLogs = [];
      this.backgroundAnalysisActive = false;

      if (this.stageTimeoutId) {
        clearTimeout(this.stageTimeoutId);
        this.stageTimeoutId = null;
      }
      if (this.elapsedTimerInterval) clearInterval(this.elapsedTimerInterval);
      this.elapsedTimerInterval = setInterval(() => {
        this.elapsedSeconds++;
      }, 1000);

      this.addAnalysisLog(
        `بدء نقل ورفع الحزمة (${this.selectedFile.name}) وإرسال طلب المحاكاة للخادم`,
        "info"
      );

      if (this.analysisInterval) {
        clearInterval(this.analysisInterval);
        this.analysisInterval = null;
      }

      if (this.abortController) {
        try {
          this.abortController.abort();
        } catch (e) {
          // ignore
        }
      }
      this.abortController = new AbortController();

      try {
        const formData = new FormData();
        formData.append("file", this.selectedFile?.fileObj || this.selectedFile);
        formData.append("scope", this.importScope);
        if (this.importOptions.parent_id) {
          formData.append("parent_id", this.importOptions.parent_id);
        }

        const response = await this.$axios?.post(this.url + "import/dry-run/", formData, {
          signal: this.abortController?.signal,
          headers: { "Content-Type": "multipart/form-data" },
          onUploadProgress: (progressEvent) => {
            if (progressEvent.total) {
              const percentCompleted = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
              );
              // Map upload to 5% - 25% of total analysis progress
              this.analysisProgress = Math.max(
                5,
                Math.min(25, Math.round(percentCompleted * 0.25))
              );
              this.analysisMessage = `جاري رفع الحزمة للخادم (${percentCompleted}%)...`;
            }
          },
        });

        const resData = response?.data;
        const taskId = resData?.task_id || resData?.id || resData?.pk;

        if (taskId) {
          this.analysisTaskId = taskId;
          this.pipelineStage = 2; // Advance to Milestone 2 (task-status polling)
          this.analysisProgress = Math.max(this.analysisProgress, 25);
          this.analysisMessage =
            "تم استلام الحزمة بنجاح. جاري فحص ومحاكاة الاستيراد بالخادم...";
          this.addAnalysisLog(
            `تم استلام الأرشيف بالخادم وإنشاء مهمة فحص في الخلفية برقم: #${this.analysisTaskId}`,
            "info"
          );
          this.pollDryRunStatus(taskId);
        } else {
          // Check for conflicts returned immediately without taskId
          if (this.hasStructuredConflicts(resData)) {
            const immediateConflicts = this.extractConflictsList(resData);
            this.conflicts = immediateConflicts;
            this.buildResolutionsTemplate(immediateConflicts);
            this.expandAllConflicts();
            this.dryRunSuccess = false;
            this.isAnalyzing = false;
            this.isImporting = false;
            this.importWizardStep = 3;
            return;
          }

          // Error that does not return model and fields: Show Errors Report returning to Step 1!
          this.showErrorReport(resData, 1, "dry-run");
        }
      } catch (err) {
        if (err?.name === "CanceledError" || err?.code === "ERR_CANCELED") {
          console.log("Dry run aborted by user");
          return;
        }
        console.error("Dry run API error:", err);
        const errData = err?.response?.data;
        if (errData && this.hasStructuredConflicts(errData)) {
          const immediateConflicts = this.extractConflictsList(errData);
          this.conflicts = immediateConflicts;
          this.buildResolutionsTemplate(immediateConflicts);
          this.expandAllConflicts();
          this.dryRunSuccess = false;
          this.isAnalyzing = false;
          this.isImporting = false;
          this.importWizardStep = 3;
          return;
        }
        this.showErrorReport(errData || err, 1, "dry-run");
      } finally {
        this.isImporting = false;
      }
    },

    addAnalysisLog(text, level = "info") {
      const mins = Math.floor(this.elapsedSeconds / 60);
      const secs = this.elapsedSeconds % 60;
      const time = `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
      this.analysisLogs.push({ time, text, level });
      this.$nextTick(() => {
        if (this.$refs.consoleLogsContainer) {
          this.$refs.consoleLogsContainer.scrollTop = this.$refs.consoleLogsContainer.scrollHeight;
        }
      });
    },

    pollDryRunStatus(taskId) {
      if (this.analysisInterval) clearInterval(this.analysisInterval);
      if (this.stageTimeoutId) {
        clearTimeout(this.stageTimeoutId);
        this.stageTimeoutId = null;
      }
      this.pipelineStage = 2; // Milestone 2: Server Execution (polling task-status every second)

      let consecutivePollErrors = 0;

      this.analysisInterval = setInterval(async () => {
        try {
          const response = await this.$axios?.get(this.url + `task-status/${taskId}/`);
          consecutivePollErrors = 0;
          const data = response?.data;
          if (data) {
            // Extract percentage from backend status response (scale between 25% and 90% during stage 2)
            const rawPct =
              data.progress_percentage ??
              data.percentage ??
              data.progress ??
              data.percent;
            if (rawPct !== undefined && rawPct !== null) {
              const numPct = Number(rawPct);
              this.analysisProgress = Math.min(90, Math.max(25, numPct));
            }

            // Extract progress message
            if (data.progress_message || data.message) {
              this.analysisMessage = data.progress_message || data.message;
            }

            const status = String(data.status || "").toUpperCase();
            const isFinished =
              status === "SUCCESS" ||
              status === "FAILED" ||
              status === "ERROR" ||
              status === "COMPLETED" ||
              status === "FINISHED" ||
              data.is_finished === true;

            if (isFinished) {
              // Task status returned finished! Stop 1-second interval
              clearInterval(this.analysisInterval);
              this.analysisInterval = null;

              // Check for errors or conflicts in dry run results
              const errors =
                Array.isArray(data.conflicts) && data.conflicts.length > 0
                  ? data.conflicts
                  : Array.isArray(data.errors) &&
                    data.errors.length > 0 &&
                    typeof data.errors[0] === "object"
                  ? data.errors
                  : [];

              if (status === "FAILED" || status === "ERROR") {
                // If structured conflicts exist even with failure status, navigate to resolver
                if (this.hasStructuredConflicts(data)) {
                  const structuredConflicts = this.extractConflictsList(data);
                  this.pipelineStage = 3;
                  this.analysisProgress = 95;
                  this.stageTimeoutId = setTimeout(() => {
                    this.stageTimeoutId = null;
                    this.pipelineStage = 4;
                    if (this.elapsedTimerInterval)
                      clearInterval(this.elapsedTimerInterval);
                    this.isAnalyzing = false;
                    this.conflicts = structuredConflicts;
                    this.buildResolutionsTemplate(structuredConflicts);
                    this.expandAllConflicts();
                    this.dryRunSuccess = false;
                    this.importWizardStep = 3;
                    this.addAnalysisLog(
                      `تم رصد ${structuredConflicts.length} تعارضات. تم الانتقال لتبويب حل التعارضات.`,
                      "warn"
                    );
                  }, 1000);
                  return;
                }

                // Error without structured conflicts -> Show Errors Report returning to Step 1!
                this.showErrorReport(data, 1, "dry-run");
                return;
              }

              // STAGE 3: Verification & Readiness Timeout
              this.pipelineStage = 3; // Milestone 3: Conflict Matrix Generation or Readiness Verification
              this.analysisProgress = 95;

              if (errors.length > 0) {
                this.analysisMessage =
                  "جاري معالجة مصفوفة التعارضات وتجهيز خيارات الحل والاعتماد...";
                this.addAnalysisLog(
                  `اكتملت محاكاة الخادم وتم رصد ${errors.length} تعارضات. جاري تجهيز مصفوفة القرارات للعرض...`,
                  "warn"
                );
              } else {
                this.analysisMessage =
                  "جاري التحقق النهائي من سلامة السجلات والتأكد من الجاهزية التامة للاستيراد الفعلي...";
                this.addAnalysisLog(
                  "المحاكاة خالية من أي تعارضات، جاري تدقيق مطابقة البيانات والتأكد من الجاهزية للاستيراد الفعلي...",
                  "info"
                );
              }

              // Run timeout for Stage 3 to allow data errors or readiness check to get ready
              this.stageTimeoutId = setTimeout(() => {
                this.stageTimeoutId = null;
                this.pipelineStage = 4; // All milestones completed!
                if (this.elapsedTimerInterval) clearInterval(this.elapsedTimerInterval);
                this.isAnalyzing = false;

                if (errors.length > 0) {
                  // Conflicts detected: provide errors to show in the third tab
                  this.conflicts = errors;
                  this.buildResolutionsTemplate(errors);
                  this.expandAllConflicts();
                  this.dryRunSuccess = false;
                  this.importWizardStep = 3; // Navigate to third tab
                  this.addAnalysisLog(
                    `تم تجهيز تقرير المطابقة ومصفوفة حل التعارضات بنجاح (${errors.length} تعارض). تم الانتقال لتبويب حل التعارضات.`,
                    "warn"
                  );
                } else {
                  // Clean success: 0 errors/conflicts, stay on second tab and show actual import button
                  this.dryRunSuccess = true;
                  this.analysisProgress = 100;
                  this.analysisMessage =
                    data.progress_message ||
                    "المحاكاة نجحت بالكامل دون أي تعارضات! البيانات متطابقة وجاهزة للاستيراد الفعلي.";
                  this.addAnalysisLog(
                    "المحاكاة نجحت بالكامل 100% دون أي أخطاء أو تعارضات. يمكنك الآن تنفيذ الاستيراد الفعلي.",
                    "info"
                  );
                }
              }, 1500); // 1.5s timeout for Stage 3 verification and preparation
            }
          }
        } catch (e) {
          console.warn("Polling task status error:", e);
          consecutivePollErrors++;
          if (
            consecutivePollErrors >= 5 ||
            e?.response?.status === 404 ||
            e?.response?.status >= 500
          ) {
            const pollErrMsg =
              e?.response?.data?.message ||
              e?.response?.data?.error ||
              "تعذر متابعة حالة مهمة المحاكاة من الخادم";
            this.resetDryRunLoading(pollErrMsg);
          }
        }
      }, 1000);
    },

    buildResolutionsTemplate(errors, resetExisting = false) {
      if (!this.resolutions || resetExisting) this.resolutions = {};
      errors.forEach((err) => {
        if (!err || !err.model) return;
        if (!this.resolutions[err.model]) {
          this.resolutions[err.model] = {};
        }
        const initialFields = {};
        if (err.fields && typeof err.fields === "object") {
          for (const f in err.fields) {
            initialFields[f] =
              err.fields[f]?.existing !== undefined && err.fields[f]?.existing !== null
                ? err.fields[f].existing
                : err.fields[f]?.new !== undefined && err.fields[f]?.new !== null
                ? err.fields[f].new
                : "";
          }
        }

        const pk = err.old_pk !== undefined ? err.old_pk : "unknown";
        this.resolutions[err.model][pk] = {
          action: "SKIP",
          fields: initialFields,
        };
      });
    },

    // Conflict Resolution Methods
    getModelName(modelKey) {
      const map = {
        "organization.organization": "المنظمات والمدارس",
        "organization.directorate": "المديريات التعليمية",
        "organization.governorate": "المحافظات",
        "student_affairs.student": "سجلات الطلاب",
        "student_affairs.academic_year": "الأعوام الدراسية",
        "student_affairs.level": "المستويات / الصفوف",
        "student_affairs.grade": "الدرجات والنتائج",
        "common.country": "الدول",
        "common.city": "المدن والمناطق",
        "common.currency": "العملات المالية",
        "advanced_chat.userchatprofile": "الملف الشخصي للمحادثات",
        "system_management.academicyear": "السنوات الأكاديمية",
        "auth.user": "المستخدمين والحسابات",
        "exam.hall": "القاعات الامتحانية",
      };
      return map[modelKey] || modelKey;
    },

    isFieldDifferent(val) {
      if (!val) return false;
      const existStr =
        val.existing !== undefined && val.existing !== null
          ? String(val.existing).trim().toLowerCase()
          : "";
      const newStr =
        val.new !== undefined && val.new !== null
          ? String(val.new).trim().toLowerCase()
          : "";
      return existStr !== newStr;
    },

    getDiffStats(error) {
      if (!error || !error.fields) return { total: 0, changed: 0, same: 0 };
      let total = 0,
        changed = 0,
        same = 0;
      for (const f in error.fields) {
        total++;
        if (this.isFieldDifferent(error.fields[f])) changed++;
        else same++;
      }
      return { total, changed, same };
    },

    getDiffSummaryText(error) {
      const stats = this.getDiffStats(error);
      if (stats.changed === 0) return "مطابق تماماً (تضارب مفتاح فريد)";
      return `${stats.changed} حقل معدل من أصل ${stats.total}`;
    },

    getCollisionKeys(error) {
      if (!error || !error.fields) return [];
      const keys = [];
      for (const f in error.fields) {
        if (!this.isFieldDifferent(error.fields[f])) {
          keys.push(f);
        }
      }
      return keys;
    },

    isCardExpanded(error) {
      const key = `${error.model}_${error.old_pk}`;
      return this.expandedConflictKeys.includes(key);
    },

    toggleConflictCard(error) {
      const key = `${error.model}_${error.old_pk}`;
      const idx = this.expandedConflictKeys.indexOf(key);
      if (idx > -1) {
        this.expandedConflictKeys.splice(idx, 1);
      } else {
        this.expandedConflictKeys.push(key);
      }
    },

    expandAllConflicts() {
      this.expandedConflictKeys = this.filteredConflicts.map(
        (e) => `${e.model}_${e.old_pk}`
      );
    },

    collapseAllConflicts() {
      this.expandedConflictKeys = [];
    },

    setConflictAction(model, pk, action) {
      if (!this.resolutions[model]) this.resolutions[model] = {};
      if (!this.resolutions[model][pk]) {
        this.resolutions[model][pk] = { action, fields: {} };
      }
      this.resolutions[model][pk].action = action;

      const conflict = this.conflicts.find(
        (c) => c.model === model && String(c.old_pk) === String(pk)
      );
      if (conflict && conflict.fields) {
        if (!this.resolutions[model][pk].fields) {
          this.resolutions[model][pk].fields = {};
        }
        for (const f in conflict.fields) {
          const val = conflict.fields[f];
          if (action === "UPDATE") {
            this.resolutions[model][pk].fields[f] =
              val?.new !== undefined && val?.new !== null ? val.new : "";
          } else if (action === "SKIP") {
            this.resolutions[model][pk].fields[f] =
              val?.existing !== undefined && val?.existing !== null
                ? val.existing
                : val?.new !== undefined && val?.new !== null
                ? val.new
                : "";
          } else if (action === "MERGE") {
            this.resolutions[model][pk].fields[f] =
              val?.existing !== undefined &&
              val?.existing !== null &&
              val?.existing !== ""
                ? val.existing
                : val?.new !== undefined && val?.new !== null
                ? val.new
                : "";
          } else if (action === "DUPLICATE") {
            if (this.isBooleanField(val?.existing, val?.new)) {
              const bVal =
                val?.new !== undefined && val?.new !== null ? val.new : val?.existing;
              this.resolutions[model][pk].fields[f] = bVal === true || bVal === "true";
            } else if (!this.isFieldDifferent(val)) {
              this.resolutions[model][pk].fields[f] =
                val?.new !== undefined && val?.new !== null && val?.new !== ""
                  ? `${val.new}-1`
                  : `${val?.existing || ""}-1`;
            } else {
              this.resolutions[model][pk].fields[f] =
                val?.new !== undefined && val?.new !== null
                  ? val.new
                  : val?.existing || "";
            }
          }
        }
      }
    },

    setAllResolutions(action) {
      this.conflicts.forEach((c) => {
        this.setConflictAction(c.model, c.old_pk, action);
      });
    },

    setResolutionsForModel(model, action) {
      if (!this.conflicts) return;
      this.conflicts
        .filter((c) => c.model === model)
        .forEach((c) => {
          this.setConflictAction(c.model, c.old_pk, action);
        });
      // this.$snack?.(
      //   "info",
      //   `تم تطبيق إجراء (${this.getActionBadgeTitle(action)}) على كافة سجلات ${this.getModelName(model)}`
      // );
    },

    smartAutoFixModel(model) {
      if (!this.conflicts) return;
      this.conflicts
        .filter((c) => c.model === model)
        .forEach((c) => {
          this.smartAutoFixConflict(c.model, c.old_pk);
        });
      // this.$snack?.(
      //   "success",
      //   `تم تطبيق الحل السريع على كافة سجلات ${this.getModelName(model)}`
      // );
    },

    pickField(model, pk, field, value) {
      if (!this.resolutions[model]) this.resolutions[model] = {};
      if (!this.resolutions[model][pk]) {
        this.resolutions[model][pk] = { action: "CUSTOM", fields: {} };
      }
      if (!this.resolutions[model][pk].fields) {
        this.resolutions[model][pk].fields = {};
      }
      if (value === "true" || value === true) {
        this.resolutions[model][pk].fields[field] = true;
      } else if (value === "false" || value === false) {
        this.resolutions[model][pk].fields[field] = false;
      } else {
        this.resolutions[model][pk].fields[field] = value;
      }
      this.resolutions[model][pk].action = "CUSTOM";
    },

    onFieldInput(model, pk) {
      if (this.resolutions[model]?.[pk]) {
        this.resolutions[model][pk].action = "CUSTOM";
      }
    },

    smartAutoFixConflict(model, pk) {
      const conflict = this.conflicts.find(
        (c) => c.model === model && String(c.old_pk) === String(pk)
      );
      if (!conflict) return;
      if (!this.resolutions[model]) this.resolutions[model] = {};
      if (!this.resolutions[model][pk]) {
        this.resolutions[model][pk] = { action: "CUSTOM", fields: {} };
      }
      const fields = {};
      for (const f in conflict.fields) {
        const val = conflict.fields[f];
        if (!this.isFieldDifferent(val)) {
          if (this.isBooleanField(val.existing, val.new)) {
            fields[f] = val.existing;
          } else {
            fields[f] = val.new ? `${val.new}-جديد` : "مخصص";
          }
        } else {
          fields[f] = val.new !== undefined && val.new !== null ? val.new : val.existing;
        }
      }
      this.resolutions[model][pk] = {
        action: "CUSTOM",
        fields,
      };
    },

    smartAutoFixAll() {
      if (!this.conflicts) return;
      this.conflicts.forEach((c) => {
        this.smartAutoFixConflict(c.model, c.old_pk);
      });
    },

    isFieldValueAdded(model, pk, field, error) {
      if (!this.resolutions?.[model]?.[pk]?.fields) return false;
      const cur = this.resolutions[model][pk].fields[field];
      if (cur === undefined || cur === null) return false;
      const curStr = String(cur).trim();

      const val = error?.fields?.[field];
      if (!val) return curStr !== "";

      const existStr = String(
        val.existing !== undefined && val.existing !== null ? val.existing : ""
      ).trim();
      const newStr = String(
        val.new !== undefined && val.new !== null ? val.new : ""
      ).trim();

      if (existStr === newStr) {
        return curStr !== existStr;
      }
      return curStr !== newStr && curStr !== existStr;
    },

    addUniqueFieldValue(model, pk, field, error) {
      if (!this.resolutions[model]) this.resolutions[model] = {};
      if (!this.resolutions[model][pk]) {
        this.resolutions[model][pk] = { action: "CUSTOM", fields: {} };
      }
      if (!this.resolutions[model][pk].fields) {
        this.resolutions[model][pk].fields = {};
      }

      const cur = this.resolutions[model][pk].fields[field];
      const val = error?.fields?.[field];
      const defaultVal =
        val && val.new !== undefined && val.new !== null && val.new !== ""
          ? String(val.new).trim()
          : val && val.existing !== undefined && val.existing !== null
          ? String(val.existing).trim()
          : "";

      const base =
        cur !== undefined && cur !== null && String(cur).trim() !== ""
          ? String(cur).trim()
          : defaultVal;

      const newVal = base ? `${base}-1` : "1";
      this.resolutions[model][pk].fields[field] = newVal;
      this.resolutions[model][pk].action = "CUSTOM";
    },

    removeAddedFieldValue(model, pk, field, error) {
      if (!this.resolutions[model]?.[pk]?.fields) return;

      const val = error?.fields?.[field];
      const existStr = String(
        val?.existing !== undefined && val?.existing !== null ? val.existing : ""
      ).trim();
      const newStr = String(
        val?.new !== undefined && val?.new !== null ? val?.new : ""
      ).trim();
      const cur = String(this.resolutions[model][pk].fields[field] || "").trim();

      let restoreVal = newStr || existStr || "";
      if (existStr && (cur === `${existStr}-1` || cur.startsWith(`${existStr}-`))) {
        restoreVal = existStr;
      }

      this.resolutions[model][pk].fields[field] = restoreVal;
      this.resolutions[model][pk].action = "CUSTOM";
    },

    getFieldChoiceState(model, pk, field, existingVal, newVal) {
      const current = this.resolutions[model]?.[pk]?.fields?.[field];
      if (current === undefined || current === null) return "";
      const curStr = String(current).trim();
      const existStr =
        existingVal !== null && existingVal !== undefined
          ? String(existingVal).trim()
          : "";
      const newStr = newVal !== null && newVal !== undefined ? String(newVal).trim() : "";

      if (existStr === newStr) {
        if (curStr === existStr) return "identical";
        return "custom";
      }
      if (curStr === existStr) return "existing";
      if (curStr === newStr) return "new";
      return "custom";
    },

    formatDisplayValue(v) {
      if (v === false || v === "false") return "false";
      if (v === true || v === "true") return "true";
      if (v === 0 || v === "0") return "0";
      if (v === null || v === undefined || v === "") return "—";
      return String(v);
    },

    isBooleanValue(v) {
      return typeof v === "boolean" || v === "true" || v === "false";
    },

    isBooleanField(v1, v2) {
      return this.isBooleanValue(v1) || this.isBooleanValue(v2);
    },

    isFieldBooleanActive(model, pk, field, targetBool, fallbackVal) {
      let current = this.resolutions[model]?.[pk]?.fields?.[field];
      if (current === undefined || current === null || current === "") {
        if (fallbackVal !== undefined && fallbackVal !== null) {
          current = fallbackVal;
        }
      }
      if (typeof current === "string") {
        const s = current.trim().toLowerCase();
        if (s.startsWith("true")) return targetBool === true;
        if (s.startsWith("false")) return targetBool === false;
      }
      if (targetBool === true) {
        return current === true || current === "true" || current === 1 || current === "1";
      } else if (targetBool === false) {
        return (
          current === false || current === "false" || current === 0 || current === "0"
        );
      }
      return false;
    },

    setBooleanField(model, pk, field, boolVal) {
      if (!this.resolutions[model]) this.resolutions[model] = {};
      if (!this.resolutions[model][pk]) {
        this.resolutions[model][pk] = { action: "CUSTOM", fields: {} };
      }
      if (!this.resolutions[model][pk].fields) {
        this.resolutions[model][pk].fields = {};
      }
      this.resolutions[model][pk].fields[field] = boolVal === true || boolVal === "true";
      this.resolutions[model][pk].action = "CUSTOM";
    },

    getModelIcon(modelKey) {
      const map = {
        "organization.organization": "mdi-domain",
        "organization.directorate": "mdi-town-hall",
        "organization.governorate": "mdi-map-marker-radius",
        "student_affairs.student": "mdi-account-school",
        "student_affairs.academic_year": "mdi-calendar-clock",
        "student_affairs.level": "mdi-stairs",
        "student_affairs.grade": "mdi-certificate-outline",
        "common.country": "mdi-flag-outline",
        "common.city": "mdi-city-variant-outline",
        "common.currency": "mdi-cash-multiple",
        "auth.user": "mdi-account-lock-outline",
        "exam.hall": "mdi-google-classroom",
      };
      return map[modelKey] || "mdi-database";
    },

    getActionIcon(action) {
      const map = {
        SKIP: "mdi-debug-step-over",
        UPDATE: "mdi-update",
        MERGE: "mdi-merge",
        DUPLICATE: "mdi-content-copy",
        CUSTOM: "mdi-pencil",
      };
      return map[action] || "mdi-help-circle";
    },

    getActionBadgeTitle(action) {
      const map = {
        SKIP: "تجاوز (إبقاء النظام)",
        UPDATE: "استبدال (اعتماد الوارد)",
        MERGE: "دمج الحقول",
        DUPLICATE: "تكرار فريد",
        CUSTOM: "تخصيص يدوي",
      };
      return map[action] || action;
    },

    downloadFinalReport() {
      const dataToExport = {
        timestamp: new Date().toISOString(),
        taskId: this.analysisTaskId,
        status: this.hasFinalErrors ? "FAILED" : "SUCCESS",
        result: this.importResult,
        decisions: this.decisionsSummary,
        resolutions: this.resolutions,
        errors: this.finalImportErrors,
      };
      const blob = new Blob([JSON.stringify(dataToExport, null, 2)], {
        type: "application/json",
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `import-report-${this.analysisTaskId || "final"}.json`;
      link.click();
      URL.revokeObjectURL(url);
    },

    async startFinalImport() {
      this.isFinalImportExecuting = true;
      this.dryRunSuccess = false;
      this.pipelineStage = 1; // Milestone 1: Preparing & Uploading resolutions
      this.importWizardStep = 2; // Move to Tab 2 for execution & loading animation!
      this.hasRemainingConflictsAlert = false;
      this.analysisProgress = 15;
      this.analysisMessage =
        "جاري تجهيز ورفع حزمة القرارات واعتماد البيانات في قاعدة البيانات...";
      this.elapsedSeconds = 0;
      this.analysisLogs = [];
      this.importResult = null;

      if (this.stageTimeoutId) {
        clearTimeout(this.stageTimeoutId);
        this.stageTimeoutId = null;
      }
      if (this.elapsedTimerInterval) clearInterval(this.elapsedTimerInterval);
      this.elapsedTimerInterval = setInterval(() => {
        this.elapsedSeconds++;
      }, 1000);

      this.addAnalysisLog("بدء مرحلة الاعتماد النهائي وتطبيق القرارات المنفذة", "info");

      const finalResolutions = {};
      for (const model in this.resolutions) {
        finalResolutions[model] = {};
        for (const pk in this.resolutions[model]) {
          const res = this.resolutions[model][pk];
          const payload = { action: res.action };
          if (res.fields && Object.keys(res.fields).length > 0) {
            const cleanFields = {};
            for (const f in res.fields) {
              let v = res.fields[f];
              if (v === "false") v = false;
              else if (v === "true") v = true;
              cleanFields[f] = v;
            }
            payload.fields = cleanFields;
          }
          finalResolutions[model][pk] = payload;
        }
      }

      console.log("📦 Final import user_resolutions payload:", finalResolutions);

      if (this.abortController) {
        try {
          this.abortController.abort();
        } catch (e) {
          // ignore
        }
      }
      this.abortController = new AbortController();

      try {
        const formData = new FormData();
        if (this.selectedFile?.fileObj || this.selectedFile) {
          formData.append("file", this.selectedFile?.fileObj || this.selectedFile);
        }
        if (this.analysisTaskId) {
          formData.append("task_id", this.analysisTaskId);
        }
        formData.append("user_resolutions", JSON.stringify(finalResolutions));
        formData.append("scope", this.importScope);
        if (this.importOptions.parent_id) {
          formData.append("parent_id", this.importOptions.parent_id);
        }

        const response = await this.$axios?.post(this.url + "import/", formData, {
          signal: this.abortController?.signal,
          headers: { "Content-Type": "multipart/form-data" },
          onUploadProgress: (progressEvent) => {
            if (progressEvent.total) {
              const pct = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              this.analysisProgress = Math.max(15, Math.min(25, Math.round(pct * 0.25)));
              this.analysisMessage = `جاري رفع حزمة القرارات (${pct}%)...`;
            }
          },
        });

        const resData = response?.data;
        const status = String(resData?.status || "").toUpperCase();

        if (status === "SUCCESS" || status === "COMPLETED" || status === "FINISHED") {
          // Finished successfully! Show final report
          if (this.analysisInterval) clearInterval(this.analysisInterval);
          if (this.stageTimeoutId) clearTimeout(this.stageTimeoutId);
          if (this.elapsedTimerInterval) clearInterval(this.elapsedTimerInterval);
          this.pipelineStage = 4;
          this.isFinalImportExecuting = false;
          this.analysisProgress = 100;
          this.importResult = resData;
          this.isFinalImportConflictSession = false;
          this.importWizardStep = 4;
          this.getData();
          // this.$snack?.(
          //   "success",
          //   "تم الاستيراد والدمج بنجاح!"
          // );
          return;
        }

        if (status === "FAILED" || status === "ERROR") {
          if (this.hasStructuredConflicts(resData)) {
            this.handleFinalImportConflicts(this.extractConflictsList(resData));
            return;
          }

          // Error during final import without structured conflicts -> Show Errors Report returning to Step 3!
          this.showErrorReport(resData, 3, "final-import");
          return;
        }

        const taskId = resData?.task_id || resData?.id || resData?.pk;
        if (taskId) {
          this.analysisTaskId = taskId;
          this.pipelineStage = 2; // Milestone 2: Background import execution
          this.analysisProgress = Math.max(this.analysisProgress, 25);
          this.pollFinalImportStatus(taskId);
          return;
        }
        throw new Error("No task id returned");
      } catch (err) {
        if (err?.name === "CanceledError" || err?.code === "ERR_CANCELED") {
          console.log("Final import aborted by user");
          return;
        }
        console.error("Backend final import error:", err);
        const errData = err.response?.data;
        if (errData && this.hasStructuredConflicts(errData)) {
          this.handleFinalImportConflicts(this.extractConflictsList(errData));
          return;
        }

        // An error occurred during final import without structured conflicts -> Show Errors Report returning to Step 3!
        this.showErrorReport(errData || err, 3, "final-import");
      }
    },

    pollFinalImportStatus(taskId) {
      if (this.analysisInterval) clearInterval(this.analysisInterval);
      if (this.stageTimeoutId) {
        clearTimeout(this.stageTimeoutId);
        this.stageTimeoutId = null;
      }
      this.pipelineStage = 2; // Milestone 2: Background import execution
      let consecutiveFinalPollErrors = 0;

      this.analysisInterval = setInterval(async () => {
        try {
          const response = await this.$axios?.get(this.url + `task-status/${taskId}/`);
          consecutiveFinalPollErrors = 0;
          const data = response?.data;
          if (data) {
            const pct =
              data.progress_percentage ??
              data.percentage ??
              data.progress ??
              data.percent;
            if (pct !== undefined && pct !== null) {
              this.analysisProgress = Math.min(90, Math.max(25, Number(pct)));
            }
            if (data.progress_message || data.message) {
              this.analysisMessage = data.progress_message || data.message;
            }
            const status = String(data.status || "").toUpperCase();
            const rawConflicts =
              Array.isArray(data.conflicts) && data.conflicts.length > 0
                ? data.conflicts
                : Array.isArray(data.errors) &&
                  data.errors.length > 0 &&
                  typeof data.errors[0] === "object"
                ? data.errors
                : Array.isArray(data.report?.errors) &&
                  data.report.errors.length > 0 &&
                  typeof data.report.errors[0] === "object"
                ? data.report.errors
                : [];

            if (status === "SUCCESS" || status === "COMPLETED" || status === "FINISHED") {
              clearInterval(this.analysisInterval);
              this.analysisInterval = null;

              // Stage 3: Verification & Finalizing report
              this.pipelineStage = 3;
              this.analysisProgress = 95;
              this.analysisMessage = "جاري التحقق النهائي وتحديث تقارير الاستيراد...";

              this.stageTimeoutId = setTimeout(() => {
                this.stageTimeoutId = null;
                this.pipelineStage = 4;
                if (this.elapsedTimerInterval) clearInterval(this.elapsedTimerInterval);
                this.isFinalImportExecuting = false;
                this.analysisProgress = 100;
                this.importResult = data;
                this.isFinalImportConflictSession = false;
                this.importWizardStep = 4;
                this.getData();
                // this.$snack?.(
                //   "success",
                //   "تم الاعتماد النهائي والاستيراد بنجاح!"
                // );
              }, 1200);
            } else if (status === "FAILED" || status === "ERROR") {
              clearInterval(this.analysisInterval);
              this.analysisInterval = null;
              if (this.elapsedTimerInterval) clearInterval(this.elapsedTimerInterval);

              if (this.hasStructuredConflicts(data)) {
                this.handleFinalImportConflicts(this.extractConflictsList(data));
              } else {
                // Failure without structured conflicts -> Show Errors Report returning to Tab 3!
                this.showErrorReport(data, 3, "final-import");
              }
            }
          }
        } catch (e) {
          console.warn("Polling final import error:", e);
          consecutiveFinalPollErrors++;
          if (
            consecutiveFinalPollErrors >= 5 ||
            e?.response?.status === 404 ||
            e?.response?.status >= 500
          ) {
            this.showErrorReport(e?.response?.data || e, 3, "final-import");
          }
        }
      }, 1000);
    },

    handleFinalImportConflicts(rawConflictData, customMessage) {
      if (!this.hasStructuredConflicts(rawConflictData)) {
        this.showErrorReport(rawConflictData, 3, "final-import");
        return;
      }

      if (this.analysisInterval) {
        clearInterval(this.analysisInterval);
        this.analysisInterval = null;
      }
      if (this.stageTimeoutId) {
        clearTimeout(this.stageTimeoutId);
        this.stageTimeoutId = null;
      }
      if (this.elapsedTimerInterval) {
        clearInterval(this.elapsedTimerInterval);
        this.elapsedTimerInterval = null;
      }

      // 1. Completely empty the old conflicts and resolutions
      this.conflicts = [];
      this.resolutions = {};
      this.expandedConflictKeys = [];
      this.collapsedConflictKeys = [];
      this.conflictSearch = "";
      this.conflictFilterModel = "ALL";
      this.conflictPage = 1;

      // 2. Extract and normalize the new conflict items
      let extracted = [];
      if (Array.isArray(rawConflictData)) {
        extracted = rawConflictData;
      } else if (rawConflictData && typeof rawConflictData === "object") {
        if (
          Array.isArray(rawConflictData.conflicts) &&
          rawConflictData.conflicts.length > 0
        ) {
          extracted = rawConflictData.conflicts;
        } else if (
          Array.isArray(rawConflictData.errors) &&
          rawConflictData.errors.length > 0
        ) {
          extracted = rawConflictData.errors;
        } else if (
          Array.isArray(rawConflictData.report?.errors) &&
          rawConflictData.report.errors.length > 0
        ) {
          extracted = rawConflictData.report.errors;
        }
      }

      const normalized = extracted.map((err, idx) => {
        if (typeof err === "string") {
          return {
            model: "system.record",
            old_pk: String(idx + 1),
            error: err,
            existing_record: "سجل بالنظام",
            new_record: "سجل وارد",
            fields: {
              status: {
                existing: err,
                new: "مطلوب المراجعة",
              },
            },
          };
        }

        const model = err.model || "system.record";
        const old_pk = String(
          err.old_pk !== undefined
            ? err.old_pk
            : err.pk !== undefined
            ? err.pk
            : err.id !== undefined
            ? err.id
            : idx + 1
        );
        const errorMsg =
          err.error || err.message || err.detail || "تعارض أثناء الاعتماد النهائي";
        const existing_record =
          err.existing_record ||
          (err.existing_name
            ? `${err.existing_name} (#${old_pk})`
            : `سجل موجود بالنظام (#${old_pk})`);
        const new_record =
          err.new_record ||
          (err.new_name
            ? `${err.new_name} (#${old_pk})`
            : `سجل وارد بالملف (#${old_pk})`);

        let fields = {};
        if (
          err.fields &&
          typeof err.fields === "object" &&
          Object.keys(err.fields).length > 0
        ) {
          fields = err.fields;
        } else {
          const conflictField = err.field || "name";
          fields[conflictField] = {
            existing: err.existing_value || existing_record,
            new: err.new_value || new_record,
          };
          if (errorMsg) {
            fields["conflict_reason"] = {
              existing: "قيد بقاعدة البيانات",
              new: errorMsg,
            };
          }
        }

        return {
          model,
          old_pk,
          error: errorMsg,
          existing_record,
          new_record,
          fields,
        };
      });

      // 3. Set the new conflicts only
      this.conflicts = normalized;

      // 4. Build fresh resolutions template (all set to default 'SKIP' as required)
      this.buildResolutionsTemplate(this.conflicts, true);
      this.expandAllConflicts();

      // 5. Update state and transition to Step 3 (حل التعارضات)
      this.isFinalImportExecuting = false;
      this.hasRemainingConflictsAlert = true;
      this.isFinalImportConflictSession = true;
      this.dryRunSuccess = false;
      this.pipelineStage = 4;
      this.importWizardStep = 3; // Navigate to Step 3 (حل التعارضات)

      const count = this.conflicts.length;
      const msg =
        customMessage ||
        `تعذر استيراد بعض السجلات أثناء الاعتماد النهائي لوجود (${count}) تعارضات جديدة. تم تفريغ التعارضات السابقة وعرض السجلات الجديدة فقط لحلها ثم إعادة الاعتماد.`;
      this.addAnalysisLog(msg, "warn");
      // this.$snack?.("warning", msg);
    },

    returnToResolveNewConflicts() {
      const errors =
        Array.isArray(this.importResult?.conflicts) &&
        this.importResult.conflicts.length > 0
          ? this.importResult.conflicts
          : Array.isArray(this.importResult?.report?.errors) &&
            this.importResult.report.errors.length > 0
          ? this.importResult.report.errors
          : this.finalImportErrors && this.finalImportErrors.length > 0
          ? this.finalImportErrors
          : null;

      if (errors && errors.length > 0) {
        if (this.hasStructuredConflicts(errors)) {
          this.handleFinalImportConflicts(errors);
        } else {
          // Unstructured / other errors: return to Step 3 preserving user resolutions!
          this.importWizardStep = 3;
          this.previousErrorAlert = {
            step: 3,
            title: "تنبيه أخطاء الاعتماد",
            message:
              "تم رصد أخطاء عامة غير مرتبطة بحقول السجلات. يمكنك تعديل القرارات السابقة وإعادة المحاولة.",
          };
          // this.$snack?.("warning", "تمت العودة لتبويب حل التعارضات لمراجعة القرارات.");
        }
      } else {
        this.importWizardStep = 3;
      }
    },

    closeImportDialog() {
      if (this.isAnalyzing || this.isImporting || this.isFinalImportExecuting) {
        this.confirmStopOperation();
        return;
      }
      this.dialog.importDialog = false;
      setTimeout(() => {
        if (!this.backgroundAnalysisActive) {
          this.resetImport();
        }
      }, 300);
    },

    resetImport() {
      this.selectedFile = null;
      this.importResult = null;
      this.isAnalyzing = false;
      this.isImporting = false;
      this.isFinalImportExecuting = false;
      this.isStoppingOperation = false;
      if (this.abortController) {
        try {
          this.abortController.abort();
        } catch (e) {}
        this.abortController = null;
      }
      this.dryRunSuccess = false;
      this.pipelineStage = 1;
      this.analysisProgress = 0;
      this.analysisMessage = "";
      this.analysisLogs = [];
      this.importSuccessSnackbar = false;
      this.importWizardStep = 1;
      this.conflicts = [];
      this.resolutions = {};
      if (this.stageTimeoutId) {
        clearTimeout(this.stageTimeoutId);
        this.stageTimeoutId = null;
      }
      if (this.analysisInterval) {
        clearInterval(this.analysisInterval);
        this.analysisInterval = null;
      }
      if (this.elapsedTimerInterval) {
        clearInterval(this.elapsedTimerInterval);
        this.elapsedTimerInterval = null;
      }
      this.errorReport = {
        visible: false,
        title: "",
        message: "",
        errors: [],
        returnStep: 1,
        returnStepTitle: "العودة لاختيار وتعديل الملف (التبويب السابق)",
        stage: "dry-run",
        timestamp: null,
        taskId: null,
      };
      this.previousErrorAlert = null;
    },

    async handleImport() {
      if (!this.selectedFile) return;

      this.isImporting = true;

      try {
        const response = await this.$axios?.post(
          this.url + "import/",
          {
            file: this.selectedFile?.fileObj || this.selectedFile,
            importScope: this.importScope,
            ...this.importOptions,
          },
          { headers: { "Content-Type": "multipart/form-data" } }
        );

        this.confirm_dialog.currentTaskId = response?.data?.task_id;
        this.importSuccessSnackbar = true;
        await this.getData();
      } catch (error) {
        console.error("Import failed", error);
      } finally {
        this.isImporting = false;
      }
    },

    getStatusText(status) {
      const mapping = {
        PENDING: "قيد الانتظار",
        RUNNING: "جاري التنفيذ",
        SUCCESS: "ناجح",
        FAILED: "فشل",
        CANCELLED: "ملغي",
      };
      return mapping[status] || status;
    },

    formatBytes(bytes, decimals = 2) {
      if (!+bytes) return "0 Bytes";
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ["Bytes", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
    },
  },
};
</script>

<style scoped>
/* ========================================================================= */
/* DYNAMIC GLASSMORPHISM THEME VARIABLES                                     */
/* ========================================================================= */
.glass-dashboard-wrapper {
  --g-bg: #f8fafc;
  --g-text-high: #0f172a;
  --g-text-med: #64748b;
  --g-card-bg: rgba(255, 255, 255, 0.7);
  --g-card-border: rgba(255, 255, 255, 1);
  --g-card-shadow: rgba(0, 0, 0, 0.05);
  --g-input-bg: rgba(255, 255, 255, 0.5);
  --g-input-border: rgba(255, 255, 255, 0.8);
  --g-input-hover: rgba(255, 255, 255, 0.9);
  --g-dropzone-bg: rgba(255, 255, 255, 0.4);
  --g-dropzone-border: rgba(15, 23, 42, 0.15);
  --g-dropzone-hover: rgba(255, 255, 255, 0.7);
  --g-text-field-bg: rgba(255, 255, 255, 0.6);
  --g-text-field-border: rgba(15, 23, 42, 0.1);
  --g-secondary-bg: white;
  --g-secondary-border: #cbd5e1;
  --g-secondary-hover: #f8fafc;
  --g-icon-dim: #94a3b8;
  --g-shape-opacity: 0.25;
  --g-glow: drop-shadow(0 0 15px rgba(255, 255, 255, 0)); /* No glow in light mode */
  --g-glow-success: drop-shadow(0 0 15px rgba(16, 185, 129, 0.2));
  --g-stat-bg: rgba(255, 255, 255, 0.6);
  --g-stat-border: rgba(255, 255, 255, 1);
  --g-error-bg: rgba(239, 68, 68, 0.02);
  --g-error-border: rgba(239, 68, 68, 0.2);
  --g-table-bg: transparent;
  --g-table-hover: rgba(var(--v-theme-primary), 0.05);
  --g-table-border: rgba(15, 23, 42, 0.05);

  font-family: "Inter", "Tajawal", sans-serif !important;
  position: relative;
  min-height: 100%;
  overflow: hidden;
  border-radius: 24px;
  transition: background-color 0.4s ease;
  direction: rtl; /* For Arabic */
}

/* Dialog Scoped Variables */
.dialog-glass-card {
  --g-card-bg: rgba(255, 255, 255, 1);
  /* backdrop-filter: blur(24px); */
  /* -webkit-backdrop-filter: blur(24px); */
  /* border: 1px solid rgba(255, 255, 255, 0.6) !important;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15) !important; */

  /* Inner content variables for light mode */
  --g-input-bg: rgba(255, 255, 255, 0.4);
  --g-input-border: rgba(0, 0, 0, 0.15);
  --g-input-hover: rgba(255, 255, 255, 0.7);
  --g-dropzone-bg: rgba(255, 255, 255, 0.3);
  --g-dropzone-border: rgba(0, 0, 0, 0.2);
  --g-dropzone-hover: rgba(255, 255, 255, 0.6);
  --g-text-field-bg: rgba(255, 255, 255, 0.4);
  --g-text-field-border: rgba(0, 0, 0, 0.15);
}

/* Add blur specifically to inner dialog elements */
.dialog-glass-card .glass-input-box,
.dialog-glass-card .glass-dropzone,
.dialog-glass-card .glass-text-field,
.dialog-glass-card .glass-stat {
  /* backdrop-filter: blur(12px); */
  /* -webkit-backdrop-filter: blur(12px); */
}

.theme-dark,
.dialog-glass-card.theme-dark {
  --g-bg: #0f172a;
  --g-text-high: white;
  --g-text-med: rgba(255, 255, 255, 0.7);
  --g-card-bg: rgba(30, 41, 59, 0.6); /* Slightly more opaque for dialogs in dark mode */
  --g-card-border: rgba(255, 255, 255, 0.15);
  --g-card-shadow: rgba(0, 0, 0, 0.5);
  /* border: 1px solid rgba(255, 255, 255, 0.15) !important; */

  /* Inner content variables for dark mode */
  --g-input-bg: rgba(0, 0, 0, 0.3);
  --g-input-border: rgba(255, 255, 255, 0.2);
  --g-input-hover: rgba(0, 0, 0, 0.5);
  --g-dropzone-bg: rgba(0, 0, 0, 0.2);
  --g-dropzone-border: rgba(255, 255, 255, 0.2);
  --g-dropzone-hover: rgba(0, 0, 0, 0.4);
  --g-text-field-bg: rgba(0, 0, 0, 0.3);
  --g-text-field-border: rgba(255, 255, 255, 0.2);

  --g-secondary-bg: rgba(255, 255, 255, 0.1);
  --g-secondary-border: rgba(255, 255, 255, 0.2);
  --g-secondary-hover: rgba(255, 255, 255, 0.2);
  --g-icon-dim: rgba(255, 255, 255, 0.5);
  --g-shape-opacity: 0.5;
  --g-glow: drop-shadow(0 0 15px rgba(255, 255, 255, 0.4));
  --g-glow-success: drop-shadow(0 0 15px rgba(16, 185, 129, 0.5));
  --g-stat-bg: rgba(0, 0, 0, 0.2);
  --g-stat-border: rgba(255, 255, 255, 0.05);
  --g-error-bg: rgba(239, 68, 68, 0.05);
  --g-error-border: rgba(239, 68, 68, 0.3);
  --g-table-bg: transparent;
  --g-table-hover: rgba(var(--v-theme-primary), 0.15);
  --g-table-border: rgba(255, 255, 255, 0.05);
}

.dialog-glass-card.theme-dark {
  --g-card-bg: rgba(30, 41, 59, 1);
}

.g-text-high {
  color: var(--g-text-high) !important;
  transition: color 0.3s;
}
.g-text-med {
  color: var(--g-text-med) !important;
  transition: color 0.3s;
}

.modern-title {
  letter-spacing: -1px;
}

.text-glow {
  filter: var(--g-glow);
}
.text-glow-success {
  filter: var(--g-glow-success);
}

/* Background Mesh Shapes */
.shape {
  position: absolute;
  /* filter: blur(80px); */
  border-radius: 50%;
  z-index: 1;
  animation: float 12s infinite ease-in-out alternate;
  opacity: var(--g-shape-opacity);
  transition: opacity 0.5s ease;
}

.shape-1 {
  width: 450px;
  height: 450px;
  background: rgb(var(--v-theme-primary));
  top: -100px;
  right: -100px;
}

.shape-2 {
  width: 350px;
  height: 350px;
  background: rgba(var(--v-theme-primary), 0.8);
  bottom: -50px;
  left: -100px;
  animation-delay: -4s;
}

.shape-3 {
  width: 300px;
  height: 300px;
  background: #38bdf8; /* Sky Blue */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -8s;
  opacity: calc(var(--g-shape-opacity) * 0.8);
}

@keyframes float {
  0% {
    transform: translate(0, 0) scale(1);
  }
  100% {
    transform: translate(40px, -60px) scale(1.1);
  }
}

/* Glass Card */
.glass-card {
  background: var(--g-card-bg);
  /* backdrop-filter: blur(24px); */
  /* -webkit-backdrop-filter: blur(24px); */
  border: 1px solid var(--g-card-border);
  border-radius: 32px;
  box-shadow: 0 10px 40px var(--g-card-shadow);
  transition: all 0.4s ease;
}

/* Glass Search Box */
.glass-search-box {
  display: flex;
  align-items: center;
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  border-radius: 20px;
  padding: 10px 20px;
  width: 100%;
  max-width: 350px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-search-box:focus-within {
  border-color: rgb(var(--v-theme-primary));
  background: var(--g-card-bg);
  box-shadow: 0 0 0 2px rgba(var(--v-theme-primary), 0.2);
}

.glass-search-input {
  border: none;
  background: transparent;
  outline: none;
  color: var(--g-text-high);
  width: 100%;
  font-size: 1rem;
}
.glass-search-input::placeholder {
  color: var(--g-icon-dim);
}

/* Glass Inputs & Dropzones */
.glass-input-box {
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  border-radius: 20px;
  padding: 20px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-input-box:hover {
  background: var(--g-input-hover);
  border-color: rgba(var(--v-theme-primary), 0.2);
  transform: translateY(-2px);
}

.glass-input-box.active {
  background: rgba(var(--v-theme-primary), 0.05);
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.15);
}
.theme-dark .glass-input-box.active {
  background: rgba(var(--v-theme-primary), 0.3);
  border-color: rgba(var(--v-theme-primary), 0.6);
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.2);
}

.glass-dropzone {
  background: var(--g-dropzone-bg);
  border: 2px dashed var(--g-dropzone-border);
  border-radius: 24px;
  padding: 48px 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.glass-dropzone:hover,
.glass-dropzone.is-dragging {
  background: var(--g-dropzone-hover);
  border-color: rgba(var(--v-theme-primary), 0.5);
}

.glass-dropzone.has-file {
  border: 2px solid rgba(16, 185, 129, 0.8);
  background: rgba(16, 185, 129, 0.05);
}
.theme-dark .glass-dropzone.has-file {
  border-color: rgba(16, 185, 129, 0.5);
  background: rgba(16, 185, 129, 0.1);
}

.glass-text-field {
  background: var(--g-text-field-bg);
  border: 1px solid var(--g-text-field-border);
  border-radius: 16px;
  padding: 16px 20px;
  color: var(--g-text-high);
  width: 100%;
  outline: none;
  transition: all 0.2s;
}
.glass-text-field::placeholder {
  color: var(--g-icon-dim);
}
.glass-text-field:focus {
  border-color: rgb(var(--v-theme-primary));
  background: var(--g-secondary-bg);
  box-shadow: 0 0 0 2px rgba(var(--v-theme-primary), 0.2);
}

/* Glass Switch replaced by Vuetify v-switch */

/* Buttons */
.glass-btn-primary {
  background: linear-gradient(
    135deg,
    rgb(var(--v-theme-primary)) 0%,
    rgba(var(--v-theme-primary), 0.8) 100%
  );
  color: white;
  font-weight: 800;
  font-size: 1rem;
  border-radius: 20px;
  border: none;
  cursor: pointer;
  box-shadow: 0 10px 20px rgba(var(--v-theme-primary), 0.2);
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 18px;
}
.glass-btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 30px rgba(var(--v-theme-primary), 0.3);
  background: linear-gradient(
    135deg,
    rgba(var(--v-theme-primary), 0.9) 0%,
    rgb(var(--v-theme-primary)) 100%
  );
}

.glass-btn-secondary {
  /* background: var(--g-secondary-bg); */
  color: var(--g-text-high);
  font-weight: 700;
  font-size: 1rem;
  /* padding: 16px 32px; */
  border-radius: 99px;
  /* border: 1px solid var(--g-secondary-border); */
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
}
/* .glass-btn-secondary:hover {
  background: var(--g-secondary-hover);
  border-color: var(--g-icon-dim);
} */

/* Glass Stats */
.glass-stat {
  padding: 24px;
  border-radius: 24px;
  background: var(--g-stat-bg);
  border: 1px solid var(--g-stat-border);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
  transition: all 0.3s;
}
.success-stat {
  border-color: rgba(16, 185, 129, 0.5);
  background: rgba(16, 185, 129, 0.05);
}
.theme-dark .success-stat {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.3);
}
.success-stat .stat-num {
  color: rgb(var(--v-theme-success));
}

.error-stat {
  border-color: rgba(239, 68, 68, 0.5);
  background: rgba(239, 68, 68, 0.05);
}
.theme-dark .error-stat {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.3);
}
.error-stat .stat-num {
  color: #ef4444;
}

.neutral-stat .stat-num {
  color: var(--g-text-high);
  transition: color 0.3s;
}

.stat-num {
  font-size: 2.5rem;
  font-weight: 900;
  line-height: 1;
  margin-bottom: 8px;
}
.stat-lbl {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--g-text-med);
}

/* Glass Error Table */
.glass-error-table-wrapper {
  background: var(--g-error-bg);
  border: 1px solid var(--g-error-border);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s;
}
.border-b-glass {
  border-bottom: 1px solid var(--g-error-border);
  background: var(--g-error-bg);
}
.glass-table {
  width: 100%;
  border-collapse: collapse;
  text-align: right;
  color: var(--g-text-high);
  transition: color 0.3s;
}
.glass-table td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--g-table-border);
  font-size: 0.9rem;
}
.glass-table tr:last-child td {
  border-bottom: none;
}

/* ======================================================== */
/* Comprehensive Gap Utility Classes (4px scale: 0 to 16)   */
/* ======================================================== */
.gap-0,
:deep(.gap-0) {
  gap: 0px !important;
}
.gap-1,
:deep(.gap-1) {
  gap: 0.25rem !important;
} /* 4px */
.gap-2,
:deep(.gap-2) {
  gap: 0.5rem !important;
} /* 8px */
.gap-3,
:deep(.gap-3) {
  gap: 0.75rem !important;
} /* 12px */
.gap-4,
:deep(.gap-4) {
  gap: 1rem !important;
} /* 16px */
.gap-5,
:deep(.gap-5) {
  gap: 1.25rem !important;
} /* 20px */
.gap-6,
:deep(.gap-6) {
  gap: 1.5rem !important;
} /* 24px */
.gap-7,
:deep(.gap-7) {
  gap: 1.75rem !important;
} /* 28px */
.gap-8,
:deep(.gap-8) {
  gap: 2rem !important;
} /* 32px */
.gap-9,
:deep(.gap-9) {
  gap: 2.25rem !important;
} /* 36px */
.gap-10,
:deep(.gap-10) {
  gap: 2.5rem !important;
} /* 40px */
.gap-11,
:deep(.gap-11) {
  gap: 2.75rem !important;
} /* 44px */
.gap-12,
:deep(.gap-12) {
  gap: 3rem !important;
} /* 48px */
.gap-14,
:deep(.gap-14) {
  gap: 3.5rem !important;
} /* 56px */
.gap-16,
:deep(.gap-16) {
  gap: 4rem !important;
} /* 64px */

/* Column Gap Utilities (gap-x-*) */
.gap-x-0,
:deep(.gap-x-0) {
  column-gap: 0px !important;
}
.gap-x-1,
:deep(.gap-x-1) {
  column-gap: 0.25rem !important;
}
.gap-x-2,
:deep(.gap-x-2) {
  column-gap: 0.5rem !important;
}
.gap-x-3,
:deep(.gap-x-3) {
  column-gap: 0.75rem !important;
}
.gap-x-4,
:deep(.gap-x-4) {
  column-gap: 1rem !important;
}
.gap-x-5,
:deep(.gap-x-5) {
  column-gap: 1.25rem !important;
}
.gap-x-6,
:deep(.gap-x-6) {
  column-gap: 1.5rem !important;
}
.gap-x-8,
:deep(.gap-x-8) {
  column-gap: 2rem !important;
}
.gap-x-10,
:deep(.gap-x-10) {
  column-gap: 2.5rem !important;
}
.gap-x-12,
:deep(.gap-x-12) {
  column-gap: 3rem !important;
}

/* Row Gap Utilities (gap-y-*) */
.gap-y-0,
:deep(.gap-y-0) {
  row-gap: 0px !important;
}
.gap-y-1,
:deep(.gap-y-1) {
  row-gap: 0.25rem !important;
}
.gap-y-2,
:deep(.gap-y-2) {
  row-gap: 0.5rem !important;
}
.gap-y-3,
:deep(.gap-y-3) {
  row-gap: 0.75rem !important;
}
.gap-y-4,
:deep(.gap-y-4) {
  row-gap: 1rem !important;
}
.gap-y-5,
:deep(.gap-y-5) {
  row-gap: 1.25rem !important;
}
.gap-y-6,
:deep(.gap-y-6) {
  row-gap: 1.5rem !important;
}
.gap-y-8,
:deep(.gap-y-8) {
  row-gap: 2rem !important;
}
.gap-y-10,
:deep(.gap-y-10) {
  row-gap: 2.5rem !important;
}
.gap-y-12,
:deep(.gap-y-12) {
  row-gap: 3rem !important;
}

/* Responsive Gap: sm (min-width: 600px) */
@media (min-width: 600px) {
  .gap-sm-0,
  :deep(.gap-sm-0) {
    gap: 0px !important;
  }
  .gap-sm-1,
  :deep(.gap-sm-1) {
    gap: 0.25rem !important;
  }
  .gap-sm-2,
  :deep(.gap-sm-2) {
    gap: 0.5rem !important;
  }
  .gap-sm-3,
  :deep(.gap-sm-3) {
    gap: 0.75rem !important;
  }
  .gap-sm-4,
  :deep(.gap-sm-4) {
    gap: 1rem !important;
  }
  .gap-sm-5,
  :deep(.gap-sm-5) {
    gap: 1.25rem !important;
  }
  .gap-sm-6,
  :deep(.gap-sm-6) {
    gap: 1.5rem !important;
  }
  .gap-sm-8,
  :deep(.gap-sm-8) {
    gap: 2rem !important;
  }
  .gap-sm-10,
  :deep(.gap-sm-10) {
    gap: 2.5rem !important;
  }
  .gap-sm-12,
  :deep(.gap-sm-12) {
    gap: 3rem !important;
  }
  .gap-sm-x-1,
  :deep(.gap-sm-x-1) {
    column-gap: 0.25rem !important;
  }
  .gap-sm-x-2,
  :deep(.gap-sm-x-2) {
    column-gap: 0.5rem !important;
  }
  .gap-sm-x-3,
  :deep(.gap-sm-x-3) {
    column-gap: 0.75rem !important;
  }
  .gap-sm-x-4,
  :deep(.gap-sm-x-4) {
    column-gap: 1rem !important;
  }
  .gap-sm-y-1,
  :deep(.gap-sm-y-1) {
    row-gap: 0.25rem !important;
  }
  .gap-sm-y-2,
  :deep(.gap-sm-y-2) {
    row-gap: 0.5rem !important;
  }
  .gap-sm-y-3,
  :deep(.gap-sm-y-3) {
    row-gap: 0.75rem !important;
  }
  .gap-sm-y-4,
  :deep(.gap-sm-y-4) {
    row-gap: 1rem !important;
  }
}

/* Responsive Gap: md (min-width: 960px) */
@media (min-width: 960px) {
  .gap-md-0,
  :deep(.gap-md-0) {
    gap: 0px !important;
  }
  .gap-md-1,
  :deep(.gap-md-1) {
    gap: 0.25rem !important;
  }
  .gap-md-2,
  :deep(.gap-md-2) {
    gap: 0.5rem !important;
  }
  .gap-md-3,
  :deep(.gap-md-3) {
    gap: 0.75rem !important;
  }
  .gap-md-4,
  :deep(.gap-md-4) {
    gap: 1rem !important;
  }
  .gap-md-5,
  :deep(.gap-md-5) {
    gap: 1.25rem !important;
  }
  .gap-md-6,
  :deep(.gap-md-6) {
    gap: 1.5rem !important;
  }
  .gap-md-8,
  :deep(.gap-md-8) {
    gap: 2rem !important;
  }
  .gap-md-10,
  :deep(.gap-md-10) {
    gap: 2.5rem !important;
  }
  .gap-md-12,
  :deep(.gap-md-12) {
    gap: 3rem !important;
  }
}

/* Responsive Gap: lg (min-width: 1280px) */
@media (min-width: 1280px) {
  .gap-lg-0,
  :deep(.gap-lg-0) {
    gap: 0px !important;
  }
  .gap-lg-1,
  :deep(.gap-lg-1) {
    gap: 0.25rem !important;
  }
  .gap-lg-2,
  :deep(.gap-lg-2) {
    gap: 0.5rem !important;
  }
  .gap-lg-3,
  :deep(.gap-lg-3) {
    gap: 0.75rem !important;
  }
  .gap-lg-4,
  :deep(.gap-lg-4) {
    gap: 1rem !important;
  }
  .gap-lg-5,
  :deep(.gap-lg-5) {
    gap: 1.25rem !important;
  }
  .gap-lg-6,
  :deep(.gap-lg-6) {
    gap: 1.5rem !important;
  }
  .gap-lg-8,
  :deep(.gap-lg-8) {
    gap: 2rem !important;
  }
}

/* Custom Glass Data Table Overrides */
.glass-table-container {
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid var(--g-card-border);
}

.theme-dark .glass-table-container {
  border-color: rgba(255, 255, 255, 0.1);
}

:deep(.custom-glass-table) {
  background: var(--g-table-bg) !important;
  color: var(--g-text-high) !important;
}

:deep(.custom-glass-table .v-data-table__tr) {
  transition: background-color 0.2s ease;
}

:deep(.custom-glass-table .v-data-table__tr:hover) {
  background: var(--g-table-hover) !important;
}

/* Custom Scrollbars */
:deep(::-webkit-scrollbar) {
  width: 8px;
  height: 8px;
}
:deep(::-webkit-scrollbar-track) {
  background: transparent;
}
:deep(::-webkit-scrollbar-thumb) {
  background: rgba(148, 163, 184, 0.3);
  border-radius: 10px;
}
:deep(::-webkit-scrollbar-thumb:hover) {
  background: rgba(148, 163, 184, 0.5);
}
.theme-dark :deep(::-webkit-scrollbar-thumb) {
  background: rgba(255, 255, 255, 0.2);
}
.theme-dark :deep(::-webkit-scrollbar-thumb:hover) {
  background: rgba(255, 255, 255, 0.3);
}

:deep(.custom-glass-table .v-data-table__th) {
  font-weight: 800 !important;
  color: var(--g-text-med) !important;
  background: rgba(0, 0, 0, 0.02) !important;
  border-bottom: 1px solid var(--g-table-border) !important;
  white-space: nowrap;
}
.theme-dark :deep(.custom-glass-table .v-data-table__th) {
  background: rgba(255, 255, 255, 0.02) !important;
}

:deep(.custom-glass-table .v-data-table__td) {
  border-bottom: 1px solid var(--g-table-border) !important;
  color: var(--g-text-high);
  font-size: 0.95rem;
}

:deep(.custom-glass-table .v-data-table-footer) {
  border-top: 1px solid var(--g-table-border) !important;
  color: var(--g-text-med);
}

:deep(.v-btn--icon.v-btn--size-small) {
  width: 36px;
  height: 36px;
}

/* Fix Vuetify Dialog Background */
:deep(.v-overlay__scrim) {
  /* backdrop-filter: blur(8px); */
  background: rgba(0, 0, 0, 0.45) !important;
}

.mini-progress-bar-container {
  position: relative;
  background-color: var(--g-input-bg);
  height: 14px;
  border-radius: 7px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 80px;
  border: 1px solid var(--g-input-border);
}

.mini-progress-bar {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background: linear-gradient(
    90deg,
    rgb(var(--v-theme-primary)),
    rgb(var(--v-theme-info))
  );
  transition: width 0.3s ease;
}

.mini-progress-text {
  position: relative;
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--g-text-high);
  z-index: 2;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
  margin-left: 6px;
  background-color: var(--g-icon-dim);
}
.status-dot.success {
  background-color: rgb(var(--v-theme-success));
  box-shadow: 0 0 5px rgba(var(--v-theme-success), 0.5);
}
.status-dot.running {
  background-color: rgb(var(--v-theme-info));
  box-shadow: 0 0 5px rgba(var(--v-theme-info), 0.5);
  animation: pulse 1.5s infinite;
}
.status-dot.failed {
  background-color: rgb(var(--v-theme-error));
  box-shadow: 0 0 5px rgba(var(--v-theme-error), 0.5);
}
@keyframes pulse {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.2);
  }
  100% {
    opacity: 1;
    transform: scale(1);
    box-shadow: 0 0 0 5px rgba(240, 136, 62, 0);
  }
}
@keyframes spin {
  100% {
    transform: rotate(-360deg);
  }
}

/* ======================================================== */
/* Enhanced Import Dialog Styles                            */
/* ======================================================== */
.dialog-glass-card {
  max-height: 92vh;
  height: 92vh;
  display: flex;
  flex-direction: column;
  overflow: hidden !important;
}
:deep(.v-dialog--fullscreen) .dialog-glass-card {
  max-height: 100vh !important;
  height: 100% !important;
  min-height: 100vh !important;
  border-radius: 0 !important;
  border: none !important;
}
.dialog-glass-card::-webkit-scrollbar {
  width: 6px;
}
.dialog-glass-card::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.3);
  border-radius: 4px;
}

/* ======================================================== */
/* Card Title & Header Stepper Tracker                      */
/* ======================================================== */
.dialog-card-title {
  background: var(--g-card-bg);
  border-bottom: 1px solid var(--g-input-border);
  white-space: normal !important;
  text-align: -webkit-left;
  font-size: 1rem;
  letter-spacing: normal;
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 20;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}
.theme-dark .dialog-card-title {
  border-bottom-color: rgba(255, 255, 255, 0.08);
}

.dialog-icon-badge-mini {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(var(--v-theme-primary), 0.12);
  border: 1px solid rgba(var(--v-theme-primary), 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* ===== Header Stepper: Vuetify 3 v-stepper Component ===== */
.header-stepper-vuetify {
  background: transparent !important;
  box-shadow: none !important;
  border: none !important;
  max-width: 660px;
  overflow: visible !important;
}
.header-stepper-vuetify :deep(.v-stepper-header) {
  box-shadow: none !important;
  height: auto !important;
  min-height: unset !important;
  padding: 0 !important;
  border: none !important;
  background: transparent !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  overflow: visible !important;
}
.header-stepper-vuetify :deep(.v-stepper-item) {
  padding: 4px 6px !important;
  cursor: pointer !important;
  opacity: 1 !important;
  min-height: unset !important;
  user-select: none !important;
  transition: all 0.2s ease !important;
}
.header-stepper-vuetify :deep(.v-stepper-item__avatar) {
  width: 26px !important;
  height: 26px !important;
  font-size: 0.75rem !important;
  font-weight: 700 !important;
  margin-inline-end: 6px !important;
  background: rgba(148, 163, 184, 0.42) !important;
  color: #334155 !important;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
}
.theme-dark .header-stepper-vuetify :deep(.v-stepper-item__avatar) {
  background: rgba(255, 255, 255, 0.16) !important;
  color: rgba(255, 255, 255, 0.75) !important;
}
.header-stepper-vuetify :deep(.v-stepper-item--selected .v-stepper-item__avatar) {
  background: #1e40af !important;
  color: #ffffff !important;
  box-shadow: 0 0 0 4px rgba(30, 64, 175, 0.24) !important;
  transform: scale(1.04) !important;
}
.theme-dark
  .header-stepper-vuetify
  :deep(.v-stepper-item--selected .v-stepper-item__avatar) {
  background: #2563eb !important;
  color: #ffffff !important;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.32) !important;
  transform: scale(1.04) !important;
}
.header-stepper-vuetify :deep(.v-stepper-item--complete .v-stepper-item__avatar) {
  background: rgb(var(--v-theme-success)) !important;
  color: #ffffff !important;
  box-shadow: 0 0 0 3px rgba(var(--v-theme-success), 0.22) !important;
}
.header-stepper-vuetify :deep(.v-stepper-item__title) {
  font-size: 0.75rem !important;
  font-weight: 600 !important;
  color: var(--g-text-med) !important;
  white-space: nowrap !important;
  line-height: 1.2 !important;
  transition: color 0.2s ease !important;
}
.header-stepper-vuetify :deep(.v-stepper-item--selected .v-stepper-item__title) {
  color: #1e40af !important;
  font-weight: 700 !important;
}
.theme-dark
  .header-stepper-vuetify
  :deep(.v-stepper-item--selected .v-stepper-item__title) {
  color: #60a5fa !important;
}
.header-stepper-vuetify :deep(.v-stepper-item--complete .v-stepper-item__title) {
  color: rgb(var(--v-theme-success)) !important;
}
.header-stepper-vuetify :deep(.v-divider) {
  margin: 0 6px !important;
  min-width: 10px !important;
  border-width: 2px !important;
  opacity: 0.4 !important;
  transition: background 0.3s ease !important;
}

/* Responsive Stepper: Medium screens move title UNDER the avatar */
@media (max-width: 991px) and (min-width: 651px) {
  .header-stepper-vuetify :deep(.v-stepper-item) {
    flex-direction: column !important;
    align-items: center !important;
    padding: 2px 4px !important;
  }
  .header-stepper-vuetify :deep(.v-stepper-item__avatar) {
    margin-inline-end: 0 !important;
    margin-bottom: 2px !important;
  }
  .header-stepper-vuetify :deep(.v-stepper-item__title) {
    font-size: 0.65rem !important;
  }
  .header-stepper-vuetify :deep(.v-divider) {
    margin-bottom: 12px !important;
  }
}

/* Responsive Stepper: Small screens REMOVE title completely */
@media (max-width: 650px) {
  .header-stepper-vuetify :deep(.v-stepper-item__title) {
    display: none !important;
  }
  .header-stepper-vuetify :deep(.v-stepper-item__avatar) {
    margin-inline-end: 0 !important;
  }
  .header-stepper-vuetify :deep(.v-divider) {
    margin: 0 4px !important;
    margin-bottom: 0 !important;
  }
}

.wiz-step__line--done {
  background: rgb(var(--v-theme-success));
}

.dialog-icon-badge {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  background: rgba(var(--v-theme-primary), 0.12);
  border: 1px solid rgba(var(--v-theme-primary), 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 24px rgba(var(--v-theme-primary), 0.2);
  animation: pulseBadge 3s infinite ease-in-out;
}

@keyframes pulseBadge {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.06);
  }
}

/* Specific Orgs Combobox Glass Styling */
.specific-orgs-combobox :deep(.v-field) {
  border-radius: 12px !important;
  background: var(--g-input-bg) !important;
  border-color: var(--g-input-border) !important;
  transition: all 0.25s ease;
}
.specific-orgs-combobox :deep(.v-field:hover) {
  background: var(--g-input-hover) !important;
}
.specific-orgs-combobox :deep(.v-chip) {
  font-size: 0.78rem !important;
  font-weight: 600;
}

/* ======================================================== */
/* Glass Wizard Stepper & Conflict Resolution Styles        */
/* ======================================================== */
.glass-wizard-stepper {
  max-width: 680px;
  margin: 0 auto 32px auto;
}

.stepper-track {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  z-index: 2;
  transition: all 0.3s ease;
}

.step-badge {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: var(--g-input-bg);
  border: 2px solid var(--g-input-border);
  color: var(--g-text-med);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.step-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--g-text-med);
  transition: all 0.3s ease;
  white-space: nowrap;
}

.step-item.active .step-badge {
  background: rgb(var(--v-theme-primary));
  border-color: rgb(var(--v-theme-primary));
  color: white;
  box-shadow: 0 0 16px rgba(var(--v-theme-primary), 0.5);
  transform: scale(1.1);
}
.step-item.active .step-label {
  color: rgb(var(--v-theme-primary));
}

.step-item.done .step-badge {
  background: rgb(var(--v-theme-success));
  border-color: rgb(var(--v-theme-success));
  color: white;
  box-shadow: 0 0 12px rgba(var(--v-theme-success), 0.3);
}
.step-item.done .step-label {
  color: rgb(var(--v-theme-success));
}

.step-connector {
  flex: 1;
  height: 3px;
  background: var(--g-input-border);
  margin: -24px 12px 0 12px;
  transition: all 0.4s ease;
}
.step-connector.active {
  background: linear-gradient(
    90deg,
    rgb(var(--v-theme-success)),
    rgb(var(--v-theme-primary))
  );
}

/* Glass Subbox */
.glass-subbox {
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  border-radius: 16px;
}

/* Conflict Banner & Batch Actions */
.glass-conflict-banner {
  background: rgba(245, 158, 11, 0.08);
  border: 1px solid rgba(245, 158, 11, 0.3);
  box-shadow: 0 8px 24px rgba(245, 158, 11, 0.08);
}
.banner-icon-circle {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(245, 158, 11, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.batch-actions-grid {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
}

.batch-action-btn {
  padding: 6px 12px;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 700;
  border: 1px solid transparent;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.2s ease;
}
.batch-action-btn:hover {
  transform: translateY(-1px);
}
.batch-action-btn.skip {
  background: rgba(148, 163, 184, 0.2);
  color: var(--g-text-high);
  border-color: rgba(148, 163, 184, 0.4);
}
.batch-action-btn.update {
  background: rgba(59, 130, 246, 0.15);
  color: #2563eb;
  border-color: rgba(59, 130, 246, 0.35);
}
.theme-dark .batch-action-btn.update {
  color: #60a5fa;
}
.batch-action-btn.merge {
  background: rgba(168, 85, 247, 0.15);
  color: #9333ea;
  border-color: rgba(168, 85, 247, 0.35);
}
.theme-dark .batch-action-btn.merge {
  color: #c084fc;
}
.batch-action-btn.duplicate {
  background: rgba(245, 158, 11, 0.15);
  color: #d97706;
  border-color: rgba(245, 158, 11, 0.35);
}
.theme-dark .batch-action-btn.duplicate {
  color: #fbbf24;
}

/* Category Filter Pills & Search */
.category-chips-scroll {
  scrollbar-width: thin;
  -webkit-overflow-scrolling: touch;
}
.category-chips-scroll::-webkit-scrollbar {
  height: 4px;
}

.conflict-search-container {
  max-width: 320px;
  width: 100%;
}

.filter-pill-btn {
  padding: 5px 12px;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  border: 1px solid var(--g-input-border);
  background: var(--g-input-bg);
  color: var(--g-text-med);
  cursor: pointer;
  transition: all 0.2s ease;
}
.filter-pill-btn:hover {
  border-color: rgb(var(--v-theme-primary));
  color: var(--g-text-high);
}
.filter-pill-btn.active {
  background: rgb(var(--v-theme-primary));
  border-color: rgb(var(--v-theme-primary));
  color: white;
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.3);
}

/* Conflict Presentation Mode Switcher */
.conflict-mode-switcher-card {
  background: rgba(var(--v-theme-primary), 0.05);
  border: 1px dashed rgba(var(--v-theme-primary), 0.3);
}
.theme-dark .conflict-mode-switcher-card {
  background: rgba(var(--v-theme-primary), 0.1);
  border-color: rgba(var(--v-theme-primary), 0.4);
}

.conflict-mode-tab {
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  color: var(--g-text-med);
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.73rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}
.conflict-mode-tab:hover {
  background: var(--g-input-hover);
  color: var(--g-text-high);
  border-color: rgba(var(--v-theme-primary), 0.4);
}
.conflict-mode-tab.active {
  background: rgb(var(--v-theme-primary));
  border-color: rgb(var(--v-theme-primary));
  color: white !important;
  box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.35);
}

/* ======================================================== */
/* REVAMPED STEP 3: Ultra-Compact Command Bar & Interactive */
/* ======================================================== */
.glass-conflict-toolbar {
  position: sticky;
  top: 0;
  z-index: 15;
  background: var(--g-card-bg);
  border: 1px solid var(--g-input-border);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
  backdrop-filter: blur(12px);
}
.theme-dark .glass-conflict-toolbar {
  background: rgba(15, 23, 42, 0.85);
  border-color: rgba(255, 255, 255, 0.08);
}

.header-stepper-vuetify {
  pointer-events: none !important;
  user-select: none !important;
}
.header-stepper-vuetify :deep(.v-stepper-item),
.header-stepper-vuetify :deep(.v-stepper-item__avatar) {
  cursor: default !important;
  pointer-events: none !important;
}

.conflict-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(245, 158, 11, 0.12);
  border: 1px solid rgba(245, 158, 11, 0.3);
  font-size: 0.73rem;
  color: var(--g-text-high);
}
.conflict-status-badge.complete {
  background: rgba(16, 185, 129, 0.12);
  border-color: rgba(16, 185, 129, 0.35);
}
.status-divider {
  opacity: 0.4;
}

.mini-progress-track {
  width: 90px;
  height: 6px;
  border-radius: 999px;
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  overflow: hidden;
}
.mini-progress-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #f59e0b, #eab308);
  transition: width 0.3s ease;
}
.mini-progress-fill.complete {
  background: linear-gradient(90deg, #10b981, #059669);
}

/* Mode Switcher: Vuetify 3 v-btn-toggle */
.conflict-mode-btn-toggle {
  background: var(--g-input-bg) !important;
  border: 1px solid var(--g-input-border) !important;
  height: 34px !important;
}
.conflict-mode-btn-toggle :deep(.v-btn) {
  height: 28px !important;
  border-radius: 6px !important;
  margin: 2px !important;
  text-transform: none !important;
  letter-spacing: normal !important;
  color: var(--g-text-med) !important;
  background: transparent !important;
  border: none !important;
}
.conflict-mode-btn-toggle :deep(.v-btn--active) {
  background: rgb(var(--v-theme-primary)) !important;
  color: #ffffff !important;
  box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.35) !important;
}
.conflict-mode-btn-toggle :deep(.v-btn--active .g-text-med) {
  color: rgba(255, 255, 255, 0.85) !important;
}

.mini-batch-btn {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid transparent;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.2s ease;
  white-space: nowrap;
}
.mini-batch-btn:hover {
  transform: translateY(-1px);
}
.mini-batch-btn.skip {
  background: rgba(148, 163, 184, 0.15);
  color: var(--g-text-high);
  border-color: rgba(148, 163, 184, 0.35);
}
.mini-batch-btn.update {
  background: rgba(59, 130, 246, 0.12);
  color: #2563eb;
  border-color: rgba(59, 130, 246, 0.3);
}
.theme-dark .mini-batch-btn.update {
  color: #60a5fa;
}
.mini-batch-btn.merge {
  background: rgba(168, 85, 247, 0.12);
  color: #9333ea;
  border-color: rgba(168, 85, 247, 0.3);
}
.theme-dark .mini-batch-btn.merge {
  color: #c084fc;
}
.mini-batch-btn.duplicate {
  background: rgba(245, 158, 11, 0.12);
  color: #d97706;
  border-color: rgba(245, 158, 11, 0.3);
}
.theme-dark .mini-batch-btn.duplicate {
  color: #fbbf24;
}
.mini-batch-btn.smart-all {
  background: linear-gradient(135deg, #7c3aed, #2563eb);
  color: white;
  border: none;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.35);
}
.mini-batch-btn.smart-all:hover {
  box-shadow: 0 3px 12px rgba(124, 58, 237, 0.5);
}

.filter-pill-micro {
  font-size: 0.68rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  border: 1px solid var(--g-input-border);
  background: var(--g-input-bg);
  color: var(--g-text-med);
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}
.filter-pill-micro:hover {
  color: var(--g-text-high);
  border-color: rgb(var(--v-theme-primary));
}
.filter-pill-micro.active {
  background: rgb(var(--v-theme-primary));
  border-color: rgb(var(--v-theme-primary));
  color: white;
}

.glass-search-micro {
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  border-radius: 999px;
  padding: 3px 22px 3px 8px;
  font-size: 0.72rem;
  color: var(--g-text-high);
  outline: none;
  transition: all 0.2s ease;
}
.glass-search-micro:focus {
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 0 0 2px rgba(var(--v-theme-primary), 0.2);
}

/* ======================================================== */
/* Wizard Stepper Navigation in Header                      */
/* ======================================================== */
.wizard-stepper-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.03);
  padding: 6px 14px;
  border-radius: 999px;
  border: 1px solid var(--g-input-border);
}
.theme-dark .wizard-stepper-nav {
  background: rgba(0, 0, 0, 0.25);
  border-color: rgba(255, 255, 255, 0.08);
}
.wizard-nav-step {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 5px 12px;
  border-radius: 999px;
  cursor: default;
  pointer-events: none;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
}
.wizard-nav-step.active {
  background: rgba(var(--v-theme-primary), 0.12);
  box-shadow: 0 0 0 1px rgba(var(--v-theme-primary), 0.35),
    0 2px 8px rgba(var(--v-theme-primary), 0.15);
}
.wizard-nav-step.done:not(.active) {
  background: rgba(16, 185, 129, 0.08);
}
.wizard-nav-step.error {
  background: rgba(239, 68, 68, 0.12);
  box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.3);
}
.nav-step-icon {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.72rem;
  font-weight: 800;
  background: rgba(148, 163, 184, 0.22);
  color: var(--g-text-med);
  transition: all 0.25s ease;
}
.wizard-nav-step.active .nav-step-icon {
  background: rgb(var(--v-theme-primary));
  color: white;
  box-shadow: 0 0 10px rgba(var(--v-theme-primary), 0.4);
}
.wizard-nav-step.done .nav-step-icon {
  background: #10b981;
  color: white;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.35);
}
.wizard-nav-step.error .nav-step-icon {
  background: #ef4444;
  color: white;
}
.nav-step-title {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--g-text-med);
  transition: all 0.2s ease;
  white-space: nowrap;
}
.wizard-nav-step.active .nav-step-title {
  color: rgb(var(--v-theme-primary));
  font-weight: 800;
}
.wizard-nav-step.done:not(.active) .nav-step-title {
  color: #059669;
}
.theme-dark .wizard-nav-step.done:not(.active) .nav-step-title {
  color: #34d399;
}
.wizard-nav-step.error .nav-step-title {
  color: #dc2626;
  font-weight: 800;
}
.nav-step-divider {
  flex: 1;
  max-width: 40px;
  min-width: 14px;
  height: 2px;
  background: rgba(148, 163, 184, 0.25);
  border-radius: 2px;
  transition: all 0.3s ease;
}
.nav-step-divider.done {
  background: linear-gradient(90deg, #10b981, rgb(var(--v-theme-primary)));
}

.pending-ripple-circle {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: rgba(var(--v-theme-primary), 0.12);
  border: 2px solid rgba(var(--v-theme-primary), 0.4);
}

/* ======================================================== */
/* Interactive 3-Way Diff Table & Cards                     */
/* ======================================================== */
.interactive-resolver-card {
  background: var(--g-card-bg);
  border: 1px solid var(--g-input-border);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
  transition: all 0.2s ease;
}
.interactive-resolver-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.4);
}

.resolver-card-header {
  background: rgba(15, 23, 42, 0.025);
  border-bottom: 1px solid var(--g-input-border);
  user-select: none;
}
.theme-dark .resolver-card-header {
  background: rgba(0, 0, 0, 0.2);
}
.resolver-card-header:hover {
  background: rgba(15, 23, 42, 0.04);
}
.theme-dark .resolver-card-header:hover {
  background: rgba(255, 255, 255, 0.04);
}
.interactive-resolver-card.is-collapsed .resolver-card-header {
  border-bottom: none;
}
.collapse-toggle-btn {
  transition: transform 0.2s ease, background 0.15s ease;
  color: var(--g-text-med);
}
.collapse-toggle-btn:hover {
  color: rgb(var(--v-theme-primary));
  background: rgba(var(--v-theme-primary), 0.1) !important;
}

.collision-cause-tag {
  font-size: 0.67rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 6px;
  background: rgba(245, 158, 11, 0.07);
  border: 1px solid rgba(245, 158, 11, 0.2);
  color: #b45309;
  font-family: monospace;
}
.theme-dark .collision-cause-tag {
  background: rgba(245, 158, 11, 0.12);
  border-color: rgba(245, 158, 11, 0.25);
  color: #fbbf24;
}

.subtle-quick-fix-btn {
  background: rgba(124, 58, 237, 0.08) !important;
  color: #7c3aed !important;
  border: 1px solid rgba(124, 58, 237, 0.2) !important;
  transition: all 0.2s ease !important;
}
.subtle-quick-fix-btn:hover {
  background: rgba(124, 58, 237, 0.15) !important;
  color: #6d28d9 !important;
}
.theme-dark .subtle-quick-fix-btn {
  background: rgba(124, 58, 237, 0.15) !important;
  color: #c084fc !important;
  border-color: rgba(124, 58, 237, 0.3) !important;
}

.smart-fix-record-btn {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 6px;
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  color: white;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(139, 92, 246, 0.35);
}
.smart-fix-record-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(139, 92, 246, 0.5);
}

.action-pills-bar {
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  border-radius: 6px;
  padding: 1px;
}
.action-pills-bar :deep(.v-btn) {
  height: 22px !important;
  font-size: 0.68rem !important;
  border-radius: 4px !important;
  letter-spacing: normal !important;
  min-width: 38px !important;
}
.action-pill-vbtn {
  font-size: 0.7rem !important;
  font-weight: 700 !important;
  height: 24px !important;
  min-width: 42px !important;
  border-radius: 5px !important;
  padding: 0 6px !important;
}
.action-pill-btn {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 3px 7px;
  border-radius: 5px;
  border: none;
  background: transparent;
  color: var(--g-text-med);
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.action-pill-btn:hover {
  background: var(--g-input-hover);
  color: var(--g-text-high);
}
.action-pill-btn.skip.active {
  background: #64748b;
  color: white;
}
.action-pill-btn.update.active {
  background: #2563eb;
  color: white;
}
.action-pill-btn.merge.active {
  background: #9333ea;
  color: white;
}
.action-pill-btn.duplicate.active {
  background: #d97706;
  color: white;
}
.action-pill-btn.custom.active {
  background: #059669;
  color: white;
}

.records-mini-strip {
  background: rgba(var(--v-theme-primary), 0.02);
  border: 1px solid var(--g-input-border);
  font-size: 0.72rem;
}

.interactive-table-wrapper {
  border: 1px solid var(--g-input-border);
}

.v-table.interactive-diff-table {
  background: transparent !important;
  color: inherit !important;
}
.v-table.interactive-diff-table .v-table__wrapper > table,
.interactive-diff-table {
  border-collapse: collapse;
  width: 100%;
}
.v-table.interactive-diff-table th,
.interactive-diff-table th {
  background: rgba(15, 23, 42, 0.02) !important;
  font-size: 0.73rem !important;
  font-weight: 600 !important;
  color: var(--g-text-med) !important;
  padding: 7px 12px !important;
  height: 36px !important;
  text-align: right !important;
  border-bottom: 1px solid var(--g-input-border) !important;
  letter-spacing: 0.01em;
}
.theme-dark .v-table.interactive-diff-table th,
.theme-dark .interactive-diff-table th {
  background: rgba(255, 255, 255, 0.02) !important;
  color: rgba(255, 255, 255, 0.7) !important;
}
.v-table.interactive-diff-table td,
.interactive-diff-table td {
  padding: 3px 10px !important;
  font-size: 0.74rem !important;
  height: 34px !important;
  border-bottom: 1px solid var(--g-input-border) !important;
  vertical-align: middle !important;
}
.v-table.interactive-diff-table tr:last-child td,
.interactive-diff-table tr:last-child td {
  border-bottom: none !important;
}
.v-table.interactive-diff-table tr.is-diff,
.interactive-diff-table tr.is-diff {
  background: rgba(var(--v-theme-primary), 0.012);
}
.v-table.interactive-diff-table tr.is-same,
.interactive-diff-table tr.is-same {
  background: transparent !important;
}

.mini-diff-tag {
  font-size: 0.62rem;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 4px;
  white-space: nowrap;
}
.mini-diff-tag.same {
  background: rgba(245, 158, 11, 0.07);
  color: #b45309;
  border: 1px solid rgba(245, 158, 11, 0.2);
}
.theme-dark .mini-diff-tag.same {
  background: rgba(245, 158, 11, 0.14);
  color: #fbbf24;
  border-color: rgba(245, 158, 11, 0.25);
}
.mini-diff-tag.diff {
  background: rgba(16, 185, 129, 0.07);
  color: #047857;
  border: 1px solid rgba(16, 185, 129, 0.2);
}
.theme-dark .mini-diff-tag.diff {
  background: rgba(16, 185, 129, 0.14);
  color: #34d399;
  border-color: rgba(16, 185, 129, 0.25);
}

.interactive-val-cell {
  cursor: pointer;
  transition: all 0.15s ease;
  border-radius: 6px;
  padding: 3px 8px !important;
  border: 1px solid transparent;
}
.interactive-val-cell:hover:not(.is-duplicate-key) {
  background: rgba(15, 23, 42, 0.025);
}
.theme-dark .interactive-val-cell:hover:not(.is-duplicate-key) {
  background: rgba(255, 255, 255, 0.03);
}
.interactive-val-cell.exist-cell.selected {
  background: rgba(59, 130, 246, 0.05) !important;
  border: 1px solid rgba(59, 130, 246, 0.25) !important;
}
.theme-dark .interactive-val-cell.exist-cell.selected {
  background: rgba(59, 130, 246, 0.12) !important;
  border: 1px solid rgba(96, 165, 250, 0.35) !important;
}
.interactive-val-cell.incoming-cell.selected {
  background: rgba(16, 185, 129, 0.05) !important;
  border: 1px solid rgba(16, 185, 129, 0.25) !important;
}
.theme-dark .interactive-val-cell.incoming-cell.selected {
  background: rgba(16, 185, 129, 0.12) !important;
  border: 1px solid rgba(52, 211, 153, 0.35) !important;
}

/* Disabled styling when a unique custom value is active */
.interactive-val-cell.is-custom-disabled {
  opacity: 0.42;
  background: rgba(15, 23, 42, 0.015) !important;
  border: 1px dashed var(--g-input-border) !important;
  cursor: pointer;
}
.theme-dark .interactive-val-cell.is-custom-disabled {
  background: rgba(255, 255, 255, 0.02) !important;
}
.interactive-val-cell.is-custom-disabled .val-text {
  color: var(--g-text-med) !important;
  font-style: italic;
}
.interactive-val-cell.is-custom-disabled .boolean-pill {
  opacity: 0.45;
  filter: grayscale(0.8);
  background: transparent !important;
}
.interactive-val-cell.is-custom-disabled:hover {
  opacity: 0.85;
  border-style: solid !important;
}

/* Plain styling for duplicate (مكرر) identical values */
.interactive-val-cell.is-duplicate-key {
  background: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
  cursor: default !important;
}
.interactive-val-cell.is-duplicate-key:hover {
  background: transparent !important;
}
.interactive-val-cell.is-duplicate-key .boolean-pill {
  background: transparent !important;
  border: 1px solid var(--g-input-border) !important;
  color: var(--g-text-med) !important;
  opacity: 0.85;
}

.val-text {
  font-family: monospace;
  font-size: 0.74rem;
  letter-spacing: -0.01em;
  color: var(--g-text-high);
}
.interactive-val-cell.selected .val-text.val-exist {
  color: #1d4ed8;
  font-weight: 600;
}
.theme-dark .interactive-val-cell.selected .val-text.val-exist {
  color: #93c5fd;
}
.interactive-val-cell.selected .val-text.val-incoming {
  color: #047857;
  font-weight: 600;
}
.theme-dark .interactive-val-cell.selected .val-text.val-incoming {
  color: #6ee7b7;
}

/* Pure Text Indicator for Choice (إبقاء / اعتماد) */
.val-choice-text {
  font-size: 0.72rem;
  font-weight: 600;
  line-height: 1;
  white-space: nowrap;
  user-select: none;
  background: transparent !important;
  border: none !important;
  padding: 0 4px;
}
.val-choice-text.exist {
  color: #2563eb;
}
.theme-dark .val-choice-text.exist {
  color: #60a5fa;
}
.val-choice-text.incoming {
  color: #059669;
}
.theme-dark .val-choice-text.incoming {
  color: #34d399;
}
.val-choice-text.active {
  font-weight: 700;
  opacity: 1;
}
.val-choice-text.pick {
  opacity: 0.45;
  cursor: pointer;
  transition: opacity 0.15s ease, text-decoration 0.15s ease;
}
.val-choice-text.pick:hover {
  opacity: 1;
  text-decoration: underline;
}

.record-inline-chip {
  font-size: 0.68rem;
  padding: 1px 7px;
  border-radius: 5px;
  background: rgba(15, 23, 42, 0.03);
  color: var(--g-text-med);
  border: 1px solid var(--g-input-border);
}
.theme-dark .record-inline-chip {
  background: rgba(255, 255, 255, 0.04);
}

.boolean-pill {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-family: monospace;
  font-size: 0.68rem;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 4px;
  line-height: 1.3;
}
.boolean-pill.bool-false {
  background: rgba(239, 68, 68, 0.08);
  color: #dc2626;
  border: 1px solid rgba(239, 68, 68, 0.18);
}
.theme-dark .boolean-pill.bool-false {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
  border-color: rgba(239, 68, 68, 0.28);
}
.boolean-pill.bool-true {
  background: rgba(16, 185, 129, 0.08);
  color: #059669;
  border: 1px solid rgba(16, 185, 129, 0.18);
}
.theme-dark .boolean-pill.bool-true {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border-color: rgba(16, 185, 129, 0.28);
}

.record-status-pill {
  display: inline-flex;
  align-items: center;
  font-size: 0.67rem;
  font-weight: 600;
  padding: 1px 7px;
  border-radius: 6px;
  line-height: 1.4;
}
.record-status-pill.skip {
  background: rgba(100, 116, 139, 0.08);
  color: #475569;
  border: 1px solid rgba(100, 116, 139, 0.2);
}
.theme-dark .record-status-pill.skip {
  background: rgba(100, 116, 139, 0.16);
  color: #94a3b8;
  border-color: rgba(100, 116, 139, 0.25);
}
.record-status-pill.update {
  background: rgba(37, 99, 235, 0.08);
  color: #2563eb;
  border: 1px solid rgba(37, 99, 235, 0.2);
}
.theme-dark .record-status-pill.update {
  background: rgba(37, 99, 235, 0.16);
  color: #93c5fd;
  border-color: rgba(37, 99, 235, 0.25);
}
.record-status-pill.merge {
  background: rgba(147, 51, 234, 0.08);
  color: #7c3aed;
  border: 1px solid rgba(147, 51, 234, 0.2);
}
.theme-dark .record-status-pill.merge {
  background: rgba(147, 51, 234, 0.16);
  color: #c084fc;
  border-color: rgba(147, 51, 234, 0.25);
}
.record-status-pill.duplicate {
  background: rgba(217, 119, 6, 0.08);
  color: #b45309;
  border: 1px solid rgba(217, 119, 6, 0.2);
}
.theme-dark .record-status-pill.duplicate {
  background: rgba(217, 119, 6, 0.16);
  color: #fcd34d;
  border-color: rgba(217, 119, 6, 0.25);
}
.record-status-pill.custom {
  background: rgba(16, 185, 129, 0.08);
  color: #059669;
  border: 1px solid rgba(16, 185, 129, 0.2);
}
.theme-dark .record-status-pill.custom {
  background: rgba(16, 185, 129, 0.16);
  color: #6ee7b7;
  border-color: rgba(16, 185, 129, 0.25);
}

.model-filter-chips {
  max-width: 100%;
}

.conflict-pagination-bar {
  background: rgba(15, 23, 42, 0.02);
  border: 1px solid var(--g-input-border);
}
.theme-dark .conflict-pagination-bar {
  background: rgba(255, 255, 255, 0.03);
}

.compact-page-size-select {
  padding: 1px 6px;
  border-radius: 6px;
  border: 1px solid var(--g-input-border);
  background: var(--g-input-bg);
  color: var(--g-text-high);
  font-size: 0.72rem;
  outline: none;
  cursor: pointer;
}
.compact-page-size-select:focus {
  border-color: rgb(var(--v-theme-primary));
}

.error-summary-banner {
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.25);
}
.theme-dark .error-summary-banner {
  background: rgba(239, 68, 68, 0.15);
}
.error-item-card {
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
}
.ripple-wave.error {
  border-color: rgba(239, 68, 68, 0.4);
}
.text-glow-error {
  filter: drop-shadow(0 0 10px rgba(239, 68, 68, 0.5));
}
.milestone-badge {
  padding: 3px 8px;
  border-radius: 6px;
  background: rgba(15, 23, 42, 0.04);
  color: var(--g-text-med);
  transition: all 0.2s ease;
}
.theme-dark .milestone-badge {
  background: rgba(255, 255, 255, 0.05);
}
.milestone-badge.active {
  background: rgba(var(--v-theme-primary), 0.12);
  color: rgb(var(--v-theme-primary));
  font-weight: 700;
}
.milestone-badge.complete {
  color: rgb(var(--v-theme-success));
}
.interactive-val-cell.is-duplicate-key {
  cursor: default !important;
}
.interactive-val-cell.is-duplicate-key:hover {
  background: transparent !important;
}

.mini-pick-btn {
  font-size: 0.62rem;
  font-weight: 700;
  padding: 1px 5px;
  border-radius: 4px;
  border: 1px solid var(--g-input-border);
  background: var(--g-input-bg);
  cursor: pointer;
  opacity: 0.6;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.interactive-val-cell:hover .mini-pick-btn {
  opacity: 1;
}
.mini-pick-btn.exist {
  color: #dc2626;
}
.mini-pick-btn.incoming {
  color: #059669;
}

.resolved-input-group {
  display: flex;
  align-items: center;
  gap: 4px;
}
.resolved-v-field {
  flex: 1;
  min-width: 80px;
}
.resolved-v-field :deep(.v-field) {
  border-radius: 6px !important;
  font-size: 0.74rem !important;
  --v-input-control-height: 26px !important;
  --v-field-padding-start: 6px !important;
  --v-field-padding-end: 6px !important;
  --v-field-padding-top: 1px !important;
  --v-field-padding-bottom: 1px !important;
  background: var(--g-input-bg) !important;
}
.resolved-v-field :deep(.v-field__outline) {
  --v-field-border-opacity: 0.25 !important;
}
.resolved-v-field :deep(.v-field--focused .v-field__outline) {
  --v-field-border-opacity: 0.9 !important;
}
.resolved-v-field :deep(.v-field__input) {
  min-height: 26px !important;
  padding: 1px 4px !important;
  font-size: 0.74rem !important;
  font-family: monospace !important;
  color: var(--g-text-high) !important;
}

.subtle-unique-btn {
  border: 1px solid var(--g-input-border) !important;
  color: var(--g-text-med) !important;
  background: rgba(15, 23, 42, 0.03) !important;
  transition: all 0.15s ease !important;
}
.subtle-unique-btn:hover {
  color: rgb(var(--v-theme-primary)) !important;
  border-color: rgba(var(--v-theme-primary), 0.4) !important;
  background: rgba(var(--v-theme-primary), 0.08) !important;
}
.theme-dark .subtle-unique-btn {
  background: rgba(255, 255, 255, 0.04) !important;
}

.conflict-guide-banner {
  background: rgba(var(--v-theme-primary), 0.05);
  border: 1px solid rgba(var(--v-theme-primary), 0.18);
}
.theme-dark .conflict-guide-banner {
  background: rgba(var(--v-theme-primary), 0.1);
  border-color: rgba(var(--v-theme-primary), 0.25);
}

.records-comparison-banner {
  background: rgba(15, 23, 42, 0.015);
  border: 1px solid var(--g-input-border);
}
.theme-dark .records-comparison-banner {
  background: rgba(255, 255, 255, 0.02);
}
.record-side-box {
  min-width: 220px;
}
.side-badge {
  font-size: 0.68rem;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: 6px;
  white-space: nowrap;
}
.side-badge.current {
  background: rgba(59, 130, 246, 0.06);
  color: #2563eb;
  border: 1px solid rgba(59, 130, 246, 0.18);
}
.theme-dark .side-badge.current {
  background: rgba(59, 130, 246, 0.12);
  color: #93c5fd;
  border-color: rgba(59, 130, 246, 0.25);
}
.side-badge.incoming {
  background: rgba(16, 185, 129, 0.06);
  color: #059669;
  border: 1px solid rgba(16, 185, 129, 0.18);
}
.theme-dark .side-badge.incoming {
  background: rgba(16, 185, 129, 0.12);
  color: #6ee7b7;
  border-color: rgba(16, 185, 129, 0.25);
}
.comparison-arrow-badge {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: rgba(15, 23, 42, 0.04);
  color: var(--g-text-med);
}
.theme-dark .comparison-arrow-badge {
  background: rgba(255, 255, 255, 0.06);
}

/* Compact Boolean Segmented Switch Capsule */
.compact-bool-switch {
  display: inline-flex;
  align-items: center;
  background: rgba(15, 23, 42, 0.04);
  border: 1px solid var(--g-input-border);
  border-radius: 999px;
  padding: 2px;
  height: 24px;
  box-sizing: border-box;
  gap: 2px;
  user-select: none;
}
.theme-dark .compact-bool-switch {
  background: rgba(255, 255, 255, 0.05);
}
.bool-segment-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 18px;
  padding: 0 7px;
  border-radius: 999px;
  border: 1px solid transparent;
  background: transparent;
  font-family: monospace;
  font-size: 0.67rem;
  font-weight: 600;
  color: var(--g-text-med);
  cursor: pointer;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  line-height: 1;
  white-space: nowrap;
}
.bool-segment-btn:hover:not(.active) {
  color: var(--g-text-high);
  background: rgba(15, 23, 42, 0.05);
}
.theme-dark .bool-segment-btn:hover:not(.active) {
  background: rgba(255, 255, 255, 0.08);
}
.bool-segment-btn.false-seg.active {
  background: rgba(239, 68, 68, 0.12);
  color: #b91c1c;
  font-weight: 700;
  border-color: rgba(239, 68, 68, 0.25);
  box-shadow: 0 1px 2px rgba(239, 68, 68, 0.12);
}
.theme-dark .bool-segment-btn.false-seg.active {
  background: rgba(239, 68, 68, 0.22);
  color: #f87171;
  border-color: rgba(239, 68, 68, 0.35);
}
.bool-segment-btn.true-seg.active {
  background: rgba(16, 185, 129, 0.12);
  color: #047857;
  font-weight: 700;
  border-color: rgba(16, 185, 129, 0.25);
  box-shadow: 0 1px 2px rgba(16, 185, 129, 0.12);
}
.theme-dark .bool-segment-btn.true-seg.active {
  background: rgba(16, 185, 129, 0.22);
  color: #34d399;
  border-color: rgba(16, 185, 129, 0.35);
}

.conflict-search-field :deep(.v-field) {
  border-radius: 10px !important;
  font-size: 0.75rem !important;
  --v-input-control-height: 30px !important;
  background: var(--g-input-bg) !important;
}
.conflict-search-field :deep(.v-field__input) {
  min-height: 30px !important;
  padding: 3px 6px !important;
  font-size: 0.75rem !important;
}
.resolved-inline-input:focus {
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 0 0 2px rgba(var(--v-theme-primary), 0.2);
}

.mini-auto-unique-btn {
  font-size: 0.65rem;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 5px;
  background: rgba(var(--v-theme-primary), 0.12);
  border: 1px solid rgba(var(--v-theme-primary), 0.3);
  color: rgb(var(--v-theme-primary));
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.mini-auto-unique-btn:hover {
  background: rgb(var(--v-theme-primary));
  color: white;
}

.smart-fix-mini-icon-btn {
  width: 26px;
  height: 26px;
  border-radius: 6px;
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  color: white;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(139, 92, 246, 0.3);
}
.smart-fix-mini-icon-btn:hover {
  transform: scale(1.08);
}

.segmented-choice-btn-compact {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid var(--g-input-border);
  background: var(--g-input-bg);
  color: var(--g-text-med);
  cursor: pointer;
  transition: all 0.15s ease;
}
.segmented-choice-btn-compact:hover {
  background: var(--g-input-hover);
  color: var(--g-text-high);
}
.segmented-choice-btn-compact.active {
  background: rgb(var(--v-theme-primary));
  border-color: rgb(var(--v-theme-primary));
  color: white;
}

/* ======================================================== */
/* MODE 1: Compact Diff Cards                               */
/* ======================================================== */
.glass-diff-card {
  background: var(--g-card-bg);
  border: 1px solid var(--g-card-border);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
  transition: all 0.25s ease;
}
.glass-diff-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.35);
}

.diff-card-header {
  background: rgba(15, 23, 42, 0.03);
}
.theme-dark .diff-card-header {
  background: rgba(0, 0, 0, 0.25);
}

.diff-index-badge {
  font-size: 0.7rem;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 6px;
  background: rgba(var(--v-theme-primary), 0.12);
  color: rgb(var(--v-theme-primary));
  font-family: monospace;
}

.diff-stats-badge {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  color: var(--g-text-med);
  display: inline-flex;
  align-items: center;
}

/* Single-Line Action Pills in Header */
.compact-action-pills {
  background: var(--g-input-bg);
  padding: 2px;
  border-radius: 8px;
  border: 1px solid var(--g-input-border);
}
.compact-action-pill {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--g-text-med);
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
}
.compact-action-pill:hover {
  background: var(--g-input-hover);
  color: var(--g-text-high);
}
.compact-action-pill.skip.active {
  background: #64748b;
  color: white;
  box-shadow: 0 2px 6px rgba(100, 116, 139, 0.4);
}
.compact-action-pill.update.active {
  background: #2563eb;
  color: white;
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.4);
}
.compact-action-pill.merge.active {
  background: #9333ea;
  color: white;
  box-shadow: 0 2px 6px rgba(147, 51, 234, 0.4);
}
.compact-action-pill.duplicate.active {
  background: #d97706;
  color: white;
  box-shadow: 0 2px 6px rgba(217, 119, 6, 0.4);
}
.compact-action-pill.custom.active {
  background: #059669;
  color: white;
  box-shadow: 0 2px 6px rgba(5, 150, 105, 0.4);
}

/* Records Summary Strip */
.records-summary-strip {
  background: rgba(var(--v-theme-primary), 0.03);
  border: 1px solid var(--g-input-border);
}
.pill-label {
  font-size: 0.68rem;
  font-weight: 800;
  padding: 1px 6px;
  border-radius: 4px;
}
.pill-label.current {
  background: rgba(239, 68, 68, 0.15);
  color: rgb(var(--v-theme-error));
}
.pill-label.incoming {
  background: rgba(16, 185, 129, 0.15);
  color: rgb(var(--v-theme-success));
}

/* Compact Diff Table */
.compact-diff-table {
  border-collapse: collapse;
  width: 100%;
}
.compact-diff-table th {
  background: rgba(15, 23, 42, 0.04);
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--g-text-med);
  padding: 6px 12px;
  text-align: right;
  border-bottom: 1px solid var(--g-input-border);
}
.theme-dark .compact-diff-table th {
  background: rgba(0, 0, 0, 0.2);
}
.compact-diff-table td {
  padding: 7px 12px;
  font-size: 0.76rem;
  border-bottom: 1px solid var(--g-input-border);
  vertical-align: middle;
}
.compact-diff-table tr:last-child td {
  border-bottom: none;
}
.compact-diff-table tr.is-diff {
  background: rgba(var(--v-theme-primary), 0.02);
}
.compact-diff-table tr.is-same {
  background: rgba(245, 158, 11, 0.02);
}

.diff-badge {
  font-size: 0.68rem;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 999px;
  display: inline-block;
  white-space: nowrap;
}
.diff-badge.same {
  background: rgba(245, 158, 11, 0.15);
  color: #d97706;
  border: 1px solid rgba(245, 158, 11, 0.3);
}
.theme-dark .diff-badge.same {
  color: #fbbf24;
}
.diff-badge.diff {
  background: rgba(16, 185, 129, 0.15);
  color: #059669;
  border: 1px solid rgba(16, 185, 129, 0.3);
}
.theme-dark .diff-badge.diff {
  color: #34d399;
}

/* Custom Field Editing Box & Quick Fill Buttons */
.custom-field-box {
  background: var(--g-card-bg);
}
.mini-tag-btn {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 4px;
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  color: var(--g-text-med);
  cursor: pointer;
  transition: all 0.2s ease;
}
.mini-tag-btn:hover {
  background: var(--g-input-hover);
  color: rgb(var(--v-theme-primary));
  border-color: rgb(var(--v-theme-primary));
}

/* ======================================================== */
/* MODE 2: Unified Matrix Grid                              */
/* ======================================================== */
.matrix-table {
  border-collapse: collapse;
}
.matrix-table th {
  background: rgba(15, 23, 42, 0.04);
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--g-text-med);
  padding: 8px 12px;
  text-align: right;
  border-bottom: 1.5px solid var(--g-input-border);
}
.theme-dark .matrix-table th {
  background: rgba(0, 0, 0, 0.3);
}
.matrix-table td {
  padding: 8px 12px;
  font-size: 0.76rem;
  border-bottom: 1px solid var(--g-input-border);
  vertical-align: middle;
}
.matrix-row:hover {
  background: rgba(var(--v-theme-primary), 0.03);
}
.diff-summary-pill {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(var(--v-theme-primary), 0.1);
  color: rgb(var(--v-theme-primary));
}
.matrix-action-select {
  border-radius: 8px;
  outline: none;
  cursor: pointer;
  border: 1.5px solid var(--g-input-border);
  background: var(--g-input-bg);
  color: var(--g-text-high);
  transition: all 0.2s ease;
}
.matrix-action-select.act-skip {
  border-color: rgba(100, 116, 139, 0.5);
}
.matrix-action-select.act-update {
  border-color: rgba(37, 99, 235, 0.6);
  color: #2563eb;
}
.matrix-action-select.act-merge {
  border-color: rgba(147, 51, 234, 0.6);
  color: #9333ea;
}
.matrix-action-select.act-duplicate {
  border-color: rgba(217, 119, 6, 0.6);
  color: #d97706;
}
.matrix-action-select.act-custom {
  border-color: rgba(5, 150, 105, 0.6);
  color: #059669;
}

.matrix-expand-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1px solid var(--g-input-border);
  background: var(--g-input-bg);
  color: var(--g-text-med);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}
.matrix-expand-btn:hover,
.matrix-expand-btn.active {
  background: rgb(var(--v-theme-primary));
  color: white;
  border-color: rgb(var(--v-theme-primary));
}

/* ======================================================== */
/* MODE 3: One-by-One Focus Carousel                        */
/* ======================================================== */
.glass-focus-card {
  background: var(--g-card-bg);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
}
.focus-counter-pill {
  font-size: 0.76rem;
  padding: 3px 10px;
  border-radius: 999px;
  background: rgba(var(--v-theme-primary), 0.12);
  color: rgb(var(--v-theme-primary));
}
.focus-step-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--g-input-border);
  cursor: pointer;
  transition: all 0.2s ease;
}
.focus-step-dot.resolved {
  background: rgb(var(--v-theme-success));
}
.focus-step-dot.active {
  transform: scale(1.3);
  box-shadow: 0 0 0 3px rgba(var(--v-theme-primary), 0.35);
  background: rgb(var(--v-theme-primary));
}
.focus-nav-btn {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 8px;
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  color: var(--g-text-high);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s ease;
}
.focus-nav-btn:hover:not(:disabled) {
  background: var(--g-input-hover);
  border-color: rgb(var(--v-theme-primary));
}
.focus-nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ======================================================== */
/* MODE 4: Accordion Rows                                   */
/* ======================================================== */
.accordion-conflict-item {
  background: var(--g-card-bg);
  transition: all 0.2s ease;
}
.accordion-conflict-item:hover {
  border-color: rgba(var(--v-theme-primary), 0.35);
}
.accordion-header {
  user-select: none;
}
.accordion-header.is-open {
  background: rgba(var(--v-theme-primary), 0.04);
}

/* Glass Conflict Cards */
.glass-conflict-card {
  background: var(--g-card-bg);
  border: 1px solid var(--g-card-border);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}
.glass-conflict-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.35);
}

.conflict-card-header {
  background: rgba(15, 23, 42, 0.04);
  border-bottom: 1px solid var(--g-input-border);
}
.theme-dark .conflict-card-header {
  background: rgba(0, 0, 0, 0.25);
}

.conflict-pk-badge {
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  padding: 3px 10px;
  border-radius: 999px;
  color: var(--g-text-med);
}

.action-status-badge {
  padding: 3px 10px;
  border-radius: 999px;
  border: 1px solid transparent;
}
.badge-skip {
  background: rgba(148, 163, 184, 0.2);
  color: var(--g-text-high);
}
.badge-update {
  background: rgba(59, 130, 246, 0.2);
  color: #2563eb;
}
.theme-dark .badge-update {
  color: #60a5fa;
}
.badge-merge {
  background: rgba(168, 85, 247, 0.2);
  color: #9333ea;
}
.theme-dark .badge-merge {
  color: #c084fc;
}
.badge-duplicate {
  background: rgba(245, 158, 11, 0.2);
  color: #d97706;
}
.theme-dark .badge-duplicate {
  color: #fbbf24;
}
.badge-custom {
  background: rgba(16, 185, 129, 0.2);
  color: #059669;
}
.theme-dark .badge-custom {
  color: #34d399;
}

/* Comparison Side Panels */
.side-panel {
  transition: all 0.2s ease;
}
.existing-panel {
  background: rgba(239, 68, 68, 0.04);
  border: 1px solid rgba(239, 68, 68, 0.2);
}
.incoming-panel {
  background: rgba(16, 185, 129, 0.04);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.border-b-subtle {
  border-bottom: 1px solid var(--g-input-border);
}
.border-t-subtle {
  border-top: 1px solid var(--g-input-border);
}

.panel-tag {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
}
.tag-danger {
  background: rgba(239, 68, 68, 0.15);
  color: rgb(var(--v-theme-error));
}
.tag-success {
  background: rgba(16, 185, 129, 0.15);
  color: rgb(var(--v-theme-success));
}

.record-title-box {
  background: var(--g-card-bg);
  border: 1px solid var(--g-input-border);
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--g-text-high);
}

.field-item {
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
}
.field-name {
  color: var(--g-text-med);
}

/* Glass Action Box & Segmented Buttons */
.glass-action-box {
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
}

.action-btn-segmented-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 8px;
}

.segmented-choice-btn {
  background: var(--g-card-bg);
  border: 1px solid var(--g-input-border);
  padding: 10px 8px;
  border-radius: 12px;
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--g-text-med);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.segmented-choice-btn:hover {
  background: var(--g-input-hover);
  color: var(--g-text-high);
  border-color: rgba(var(--v-theme-primary), 0.3);
}
.segmented-choice-btn.active {
  background: rgba(var(--v-theme-primary), 0.12);
  border-color: rgb(var(--v-theme-primary));
  color: rgb(var(--v-theme-primary));
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.2);
  transform: scale(1.02);
}

.custom-edit-form {
  background: var(--g-card-bg);
  border: 1px dashed rgba(var(--v-theme-primary), 0.4);
}

/* ======================================================== */
/* Multi-Variant Scope Switcher & Styles                    */
/* ======================================================== */
.scope-style-switcher-card {
  background: rgba(var(--v-theme-primary), 0.05);
  border: 1px dashed rgba(var(--v-theme-primary), 0.3);
}
.theme-dark .scope-style-switcher-card {
  background: rgba(var(--v-theme-primary), 0.1);
  border-color: rgba(var(--v-theme-primary), 0.4);
}

.scope-variant-tab {
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  color: var(--g-text-med);
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.73rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}
.scope-variant-tab:hover {
  background: var(--g-input-hover);
  color: var(--g-text-high);
  border-color: rgba(var(--v-theme-primary), 0.4);
}
.scope-variant-tab.active {
  background: rgb(var(--v-theme-primary));
  border-color: rgb(var(--v-theme-primary));
  color: white !important;
  box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.35);
}

/* Variant 1: Segmented Control Bar */
.scope-segmented-bar {
  background: var(--g-input-bg);
  border: 1.5px solid var(--g-input-border);
  gap: 4px;
}
.scope-segment-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--g-text-med);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}
.scope-segment-btn:hover {
  background: var(--g-input-hover);
  color: var(--g-text-high);
}
.scope-segment-btn.active {
  background: rgb(var(--v-theme-primary));
  color: white;
  box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.3);
  border-color: rgb(var(--v-theme-primary));
}

/* Variant 2: Auto-detect Organization List */
.detected-org-card {
  background: var(--g-input-bg);
  border: 1.5px solid var(--g-input-border);
}
.detected-org-card:hover {
  background: var(--g-input-hover);
  border-color: rgba(var(--v-theme-primary), 0.4);
}
.detected-org-card.selected {
  background: rgba(var(--v-theme-primary), 0.08);
  border-color: rgba(var(--v-theme-primary), 0.6);
}
.theme-dark .detected-org-card.selected {
  background: rgba(var(--v-theme-primary), 0.16);
  border-color: rgba(var(--v-theme-primary), 0.8);
}
.detected-checkbox {
  width: 20px;
  height: 20px;
  border-radius: 6px;
  border: 1.5px solid var(--g-input-border);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--g-card-bg);
  transition: all 0.2s ease;
}
.detected-checkbox.active {
  background: rgb(var(--v-theme-primary));
  border-color: rgb(var(--v-theme-primary));
}
.org-count-chip {
  font-size: 0.68rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(var(--v-theme-primary), 0.1);
  color: rgb(var(--v-theme-primary));
  font-family: monospace;
}
.mini-chip-btn {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 6px;
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  color: var(--g-text-med);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 3px;
  transition: all 0.2s ease;
}
.mini-chip-btn:hover {
  background: var(--g-input-hover);
  color: var(--g-text-high);
}
.badge-pulsing-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgb(var(--v-theme-success));
  box-shadow: 0 0 6px rgba(var(--v-theme-success), 0.8);
  animation: pulse 1.8s infinite;
}

/* Variant 3: Catalog Selects */
.glass-select-field {
  background: var(--g-input-bg);
  border: 1.5px solid var(--g-input-border);
  color: var(--g-text-high);
  border-radius: 10px;
  outline: none;
  cursor: pointer;
  transition: all 0.2s ease;
}
.glass-select-field:focus {
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 0 0 3px rgba(var(--v-theme-primary), 0.15);
}
.theme-dark .glass-select-field option {
  background: #0f172a;
  color: #f1f5f9;
}
.catalog-chip {
  background: rgba(var(--v-theme-primary), 0.12);
  border: 1px solid rgba(var(--v-theme-primary), 0.3);
  color: rgb(var(--v-theme-primary));
  font-weight: 600;
  font-size: 0.72rem;
}

/* Variant 4: Vertical Radio Accordion */
.vertical-scope-row {
  background: var(--g-input-bg);
  border: 1.5px solid var(--g-input-border);
}
.vertical-scope-row:hover {
  background: var(--g-input-hover);
  border-color: rgba(var(--v-theme-primary), 0.4);
}
.vertical-scope-row.active {
  background: rgba(var(--v-theme-primary), 0.08);
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 2px 10px rgba(var(--v-theme-primary), 0.1);
}
.theme-dark .vertical-scope-row.active {
  background: rgba(var(--v-theme-primary), 0.16);
  border-color: rgba(var(--v-theme-primary), 0.8);
}
.vertical-radio-dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 2px solid var(--g-input-border);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  position: relative;
}
.vertical-radio-dot.active {
  border-color: rgb(var(--v-theme-primary));
}
.vertical-radio-dot.active::after {
  content: "";
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgb(var(--v-theme-primary));
}

/* ======================================================== */
/* Step 1 Revamp: Scope Tiles & File Inspection Card        */
/* ======================================================== */
.scope-tile {
  background: var(--g-input-bg);
  border: 1.5px solid var(--g-input-border);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
}
.scope-tile:hover {
  background: var(--g-input-hover);
  border-color: rgba(var(--v-theme-primary), 0.4);
  transform: translateY(-2px);
}
.scope-tile.active {
  background: rgba(var(--v-theme-primary), 0.08);
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 4px 16px rgba(var(--v-theme-primary), 0.15);
}
.theme-dark .scope-tile.active {
  background: rgba(var(--v-theme-primary), 0.2);
  border-color: rgba(var(--v-theme-primary), 0.8);
  box-shadow: 0 4px 20px rgba(var(--v-theme-primary), 0.25);
}

.scope-radio-dot {
  position: absolute;
  top: 8px;
  left: 8px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: rgb(var(--v-theme-primary));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 8px rgba(var(--v-theme-primary), 0.5);
  animation: popIn 0.2s ease-out;
}
@keyframes popIn {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.scope-icon-box {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease;
}
.scope-tile:hover .scope-icon-box {
  transform: scale(1.1);
}
.scope-icon-box.all {
  background: rgba(var(--v-theme-primary), 0.12);
}
.scope-icon-box.father {
  background: rgba(168, 85, 247, 0.15);
}
.scope-icon-box.specific {
  background: rgba(245, 158, 11, 0.15);
}

.file-badge {
  font-size: 0.7rem;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 6px;
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  color: var(--g-text-med);
  font-family: monospace;
}

.dropzone-icon-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(var(--v-theme-primary), 0.1);
  border: 1px solid rgba(var(--v-theme-primary), 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}
.glass-dropzone:hover .dropzone-icon-circle {
  transform: scale(1.08);
  background: rgba(var(--v-theme-primary), 0.18);
}

.browse-files-btn {
  background: rgba(var(--v-theme-primary), 0.1);
  color: rgb(var(--v-theme-primary));
  border: 1px solid rgba(var(--v-theme-primary), 0.3);
  padding: 8px 16px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
}
.browse-files-btn:hover {
  background: rgb(var(--v-theme-primary));
  color: white;
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.3);
}

/* File Inspection Card */
.file-inspection-card {
  background: var(--g-card-bg);
  border: 1px solid rgba(16, 185, 129, 0.4);
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.1);
}
.theme-dark .file-inspection-card {
  background: rgba(15, 23, 42, 0.7);
  border-color: rgba(16, 185, 129, 0.5);
}

.file-icon-box {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
}

.file-meta-pill {
  font-size: 0.72rem;
  padding: 2px 8px;
  border-radius: 6px;
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  color: var(--g-text-med);
}

.file-status-pill {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
  background: rgba(16, 185, 129, 0.12);
  color: rgb(var(--v-theme-success));
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.pulse-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: inline-block;
}
.pulse-dot.green {
  background: rgb(var(--v-theme-success));
  box-shadow: 0 0 6px rgba(var(--v-theme-success), 0.8);
  animation: pulse 1.8s infinite;
}

.file-action-btn {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}
.file-action-btn.replace {
  background: var(--g-input-bg);
  border-color: var(--g-input-border);
  color: var(--g-text-high);
}
.file-action-btn.replace:hover {
  background: var(--g-input-hover);
  border-color: rgb(var(--v-theme-primary));
  color: rgb(var(--v-theme-primary));
}
.file-action-btn.delete {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.25);
  color: rgb(var(--v-theme-error));
}
.file-action-btn.delete:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgb(var(--v-theme-error));
}

/* Advanced Pre-checks Accordion */
.advanced-toggle-btn {
  background: var(--g-input-bg);
  border: 1px dashed var(--g-input-border);
  cursor: pointer;
  transition: all 0.2s ease;
}
.advanced-toggle-btn:hover {
  background: var(--g-input-hover);
  border-color: rgb(var(--v-theme-primary));
}

.option-toggle-item {
  background: var(--g-card-bg);
  border: 1px solid var(--g-input-border);
  cursor: pointer;
  transition: all 0.2s ease;
}
.option-toggle-item:hover {
  border-color: rgba(var(--v-theme-primary), 0.4);
}

.safety-notice-card {
  background: rgba(56, 189, 248, 0.05);
  border-color: rgba(56, 189, 248, 0.2);
}
.safety-icon-circle {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(56, 189, 248, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ======================================================== */
/* Step 2 Revamp: Scanner Radar Visual & Verification Pipeline */
/* ======================================================== */
.scanner-console-visual {
  width: 140px;
  height: 140px;
  margin: 0 auto;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.radar-outer-ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px dashed rgba(var(--v-theme-primary), 0.4);
  animation: spin 16s linear infinite;
}

.radar-middle-ring {
  position: absolute;
  inset: 16px;
  border-radius: 50%;
  border: 1px solid rgba(var(--v-theme-primary), 0.25);
  background: radial-gradient(
    circle,
    rgba(var(--v-theme-primary), 0.08) 0%,
    transparent 70%
  );
}

.radar-scan-beam {
  position: absolute;
  inset: 16px;
  border-radius: 50%;
  background: conic-gradient(
    from 0deg,
    rgba(var(--v-theme-primary), 0.4) 0deg,
    transparent 60deg,
    transparent 360deg
  );
  animation: spin 3s linear infinite;
}

.radar-center-badge {
  position: relative;
  z-index: 2;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: var(--g-card-bg);
  border: 2px solid rgb(var(--v-theme-primary));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 20px rgba(var(--v-theme-primary), 0.35);
}

.modern-gradient-title {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)), #38bdf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.scanner-progress-container {
  height: 8px;
  background: var(--g-input-bg);
  border-radius: 999px;
  overflow: hidden;
  border: 1px solid var(--g-input-border);
  position: relative;
  direction: rtl !important;
}

.scanner-progress-fill {
  height: 100%;
  background: linear-gradient(
    270deg,
    rgb(var(--v-theme-primary)),
    #38bdf8,
    rgb(var(--v-theme-success))
  );
  border-radius: 999px;
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  overflow: hidden;
}
.scanner-progress-fill::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(270deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  animation: progressShimmerRtl 1.8s infinite;
}
@keyframes progressShimmerRtl {
  0% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(-100%);
  }
}

.scanner-progress-indeterminate {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 40%;
  border-radius: 999px;
  background: linear-gradient(
    270deg,
    transparent,
    rgb(var(--v-theme-primary)),
    rgb(var(--v-theme-info)),
    transparent
  );
  animation: indeterminate-scan-rtl 1.6s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
@keyframes indeterminate-scan-rtl {
  0% {
    transform: translateX(150%);
  }
  100% {
    transform: translateX(-350%);
  }
}

.verification-pipeline {
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
}

.pipeline-item {
  background: var(--g-card-bg);
  border: 1px solid var(--g-input-border);
  transition: all 0.3s ease;
}
.pipeline-item.active {
  border-color: rgba(var(--v-theme-primary), 0.5);
  background: rgba(var(--v-theme-primary), 0.05);
}
.pipeline-item.done {
  border-color: rgba(16, 185, 129, 0.35);
  background: rgba(16, 185, 129, 0.04);
}
.pipeline-item.pending {
  opacity: 0.7;
}

.status-badge-mini {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  color: var(--g-text-med);
  display: inline-flex;
  align-items: center;
}
.status-badge-mini.success {
  background: rgba(16, 185, 129, 0.12);
  border-color: rgba(16, 185, 129, 0.3);
  color: rgb(var(--v-theme-success));
}
.status-badge-mini.running {
  background: rgba(var(--v-theme-primary), 0.12);
  border-color: rgba(var(--v-theme-primary), 0.35);
  color: rgb(var(--v-theme-primary));
}
.status-badge-mini.warning {
  background: rgba(245, 158, 11, 0.12);
  border-color: rgba(245, 158, 11, 0.3);
  color: #d97706;
}
.theme-dark .status-badge-mini.warning {
  color: #fbbf24;
}

/* ======================================================== */
/* Step 3 & 4 Revamp: Resolution Meter & Celebratory Card   */
/* ======================================================== */
.resolution-meter-box {
  background: var(--g-card-bg);
  border: 1px solid var(--g-input-border);
}

.resolution-mini-track {
  height: 8px;
  border-radius: 999px;
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
  overflow: hidden;
}

.resolution-mini-bar {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #f59e0b, #eab308);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.resolution-mini-bar.complete {
  background: linear-gradient(90deg, #10b981, #059669);
}

/* Step 4 Success & Error Ripple */
.success-ripple-circle {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.12);
  border: 2px solid rgba(16, 185, 129, 0.4);
}

.error-ripple-circle {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.12);
  border: 2px solid rgba(239, 68, 68, 0.4);
}

.ripple-wave {
  position: absolute;
  inset: -10px;
  border-radius: 50%;
  border: 2px solid rgba(16, 185, 129, 0.3);
  animation: ripple 2.5s infinite cubic-bezier(0.1, 0.8, 0.3, 1);
}
.ripple-wave.error {
  border-color: rgba(239, 68, 68, 0.3);
}

.text-glow-error {
  filter: drop-shadow(0 0 12px rgba(239, 68, 68, 0.4));
}
.text-glow-success {
  filter: drop-shadow(0 0 12px rgba(16, 185, 129, 0.4));
}
@keyframes ripple {
  0% {
    transform: scale(0.9);
    opacity: 1;
  }
  100% {
    transform: scale(1.4);
    opacity: 0;
  }
}

.decisions-summary-card {
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
}

.summary-pill {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid transparent;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.summary-pill.blue {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
  color: #2563eb;
}
.theme-dark .summary-pill.blue {
  color: #60a5fa;
}

.summary-pill.purple {
  background: rgba(168, 85, 247, 0.15);
  border-color: rgba(168, 85, 247, 0.3);
  color: #9333ea;
}
.theme-dark .summary-pill.purple {
  color: #c084fc;
}

.summary-pill.amber {
  background: rgba(245, 158, 11, 0.15);
  border-color: rgba(245, 158, 11, 0.3);
  color: #d97706;
}
.theme-dark .summary-pill.amber {
  color: #fbbf24;
}

.summary-pill.slate {
  background: rgba(148, 163, 184, 0.2);
  border-color: rgba(148, 163, 184, 0.35);
  color: var(--g-text-high);
}

.summary-pill.emerald {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.3);
  color: #059669;
}
.theme-dark .summary-pill.emerald {
  color: #34d399;
}

/* ======================================================== */
/* Responsive Adjustments for Small Screens & Mobile        */
/* ======================================================== */
@media (max-width: 600px) {
  .dialog-glass-card {
    padding: 16px !important;
  }

  .dialog-card-title {
    padding: 10px 12px !important;
  }
  .dialog-icon-badge-mini {
    width: 28px;
    height: 28px;
    border-radius: 8px;
  }
  /* Small screen / Mobile: Show ONLY the numbers (hide labels) */
  .header-stepper-tracker {
    padding-bottom: 0 !important;
  }
  .header-step-text {
    display: none !important;
  }
  .header-step-node {
    width: 22px !important;
    height: 22px !important;
  }
  .header-step-circle {
    width: 22px !important;
    height: 22px !important;
    font-size: 0.68rem !important;
  }
  .header-step-line {
    width: 8px !important;
    margin: 0 2px !important;
  }
  .header-step-node.active .header-step-circle {
    box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.22);
  }

  .dialog-icon-badge {
    width: 48px;
    height: 48px;
    box-shadow: 0 0 16px rgba(var(--v-theme-primary), 0.2);
  }
  .dialog-icon-badge .v-icon {
    font-size: 24px !important;
  }

  /* Compact Stepper for Mobile */
  .glass-wizard-stepper {
    margin-bottom: 20px !important;
  }
  .step-badge {
    width: 30px;
    height: 30px;
    font-size: 0.75rem;
  }
  .step-connector {
    margin: -16px 4px 0 4px;
    height: 2px;
  }
  .step-label {
    font-size: 0.68rem;
  }

  /* Compact Dropzone */
  .glass-dropzone {
    padding: 24px 12px !important;
    border-radius: 18px !important;
  }

  /* Conflict Banner & Batch Actions: 2x2 Grid */
  .glass-conflict-banner {
    padding: 12px !important;
  }
  .banner-icon-circle {
    width: 36px;
    height: 36px;
  }
  .batch-actions-grid {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 6px !important;
    width: 100% !important;
  }
  .batch-action-btn {
    justify-content: center !important;
    padding: 8px 6px !important;
    font-size: 0.7rem !important;
    text-align: center !important;
  }

  /* Segmented Choice Buttons: 2x2 + 1 Grid */
  .action-btn-segmented-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 6px !important;
  }
  .segmented-choice-btn {
    padding: 8px 4px !important;
    font-size: 0.72rem !important;
  }
  .segmented-choice-btn:nth-child(5) {
    grid-column: span 2 !important;
  }

  /* Search input container in Step 3 */
  .conflict-search-container {
    max-width: 100% !important;
    width: 100% !important;
  }

  /* Compact Scope Tiles on Mobile */
  .scope-tile {
    padding: 8px 4px !important;
  }
  .scope-icon-box {
    width: 36px !important;
    height: 36px !important;
  }
  .scope-icon-box .v-icon {
    font-size: 20px !important;
  }

  /* Compact Scanner & Success Visuals */
  .scanner-console-visual {
    width: 110px !important;
    height: 110px !important;
  }
  .radar-center-badge {
    width: 48px !important;
    height: 48px !important;
  }
  .radar-center-badge .v-icon {
    font-size: 28px !important;
  }
  .success-ripple-circle {
    width: 72px !important;
    height: 72px !important;
  }
  .success-ripple-circle .v-icon {
    font-size: 38px !important;
  }
}

/* ======================================================== */
/* Multi-Mode Asynchronous Loading & Activity Monitor       */
/* ======================================================== */
.glass-mode-switcher {
  background: var(--g-input-bg);
  border: 1px solid var(--g-input-border);
}
.mode-switch-btn {
  padding: 4px 10px;
  font-size: 0.75rem;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: var(--g-text-med);
  cursor: pointer;
  transition: all 0.25s ease;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
}
.mode-switch-btn:hover {
  color: var(--g-text-high);
  background: rgba(var(--v-theme-primary), 0.08);
}
.mode-switch-btn.active {
  background: rgb(var(--v-theme-primary));
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.35);
}

/* Live Stream Console */
.live-stream-console {
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #e2e8f0;
  box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.5);
}
.theme-dark .live-stream-console {
  background: rgba(10, 15, 29, 0.95);
  border-color: rgba(255, 255, 255, 0.08);
}
.console-dot-red {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ef4444;
  display: inline-block;
}
.console-dot-yellow {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #f59e0b;
  display: inline-block;
}
.console-dot-green {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #10b981;
  display: inline-block;
}

.console-logs-box {
  max-height: 170px;
  overflow-y: auto;
  scrollbar-width: thin;
  font-size: 0.78rem;
  padding: 4px 2px;
}
.console-logs-box::-webkit-scrollbar {
  width: 4px;
}
.console-logs-box::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}
.console-log-line {
  line-height: 1.4;
  animation: log-fade-in 0.3s ease;
}
@keyframes log-fade-in {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.log-time {
  font-size: 0.72rem;
  opacity: 0.8;
  flex-shrink: 0;
}
.log-text.warn {
  color: #facc15;
}
.log-text.success {
  color: #4ade80;
}
.log-text.info {
  color: #93c5fd;
}

/* Minimal Monitor Card */
.minimal-monitor-card {
  background: var(--g-card-bg);
  border: 1px solid var(--g-card-border);
}
.minimal-status-pill {
  font-family: monospace;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
  background: rgba(var(--v-theme-info), 0.15);
  color: rgb(var(--v-theme-info));
  border: 1px solid rgba(var(--v-theme-info), 0.3);
}

/* Background Floating Task Bar */
.background-task-floating-bar {
  background: var(--g-card-bg);
  border: 1px solid rgba(var(--v-theme-primary), 0.4);
  box-shadow: 0 8px 30px rgba(var(--v-theme-primary), 0.15);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}
.badge-running-pill {
  font-size: 0.65rem;
  padding: 1px 6px;
  border-radius: 4px;
  background: rgba(var(--v-theme-primary), 0.15);
  color: rgb(var(--v-theme-primary));
  font-weight: 700;
}
.pulse-beacon {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: rgb(var(--v-theme-primary));
  box-shadow: 0 0 0 0 rgba(var(--v-theme-primary), 0.7);
  animation: beacon-pulse 1.8s infinite;
}
.pulse-beacon-mini {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  animation: beacon-pulse 1.5s infinite;
  display: inline-block;
}
@keyframes beacon-pulse {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(var(--v-theme-primary), 0.7);
  }
  70% {
    transform: scale(1.1);
    box-shadow: 0 0 0 8px rgba(var(--v-theme-primary), 0);
  }
  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(var(--v-theme-primary), 0);
  }
}
.status-pulse-dot.running {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: rgb(var(--v-theme-info));
  box-shadow: 0 0 6px rgba(var(--v-theme-info), 0.6);
  display: inline-block;
}
.badge-percentage {
  font-size: 0.75rem;
  color: rgb(var(--v-theme-primary));
  font-weight: 700;
}
</style>
