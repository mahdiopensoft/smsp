<template>
  <div class="qb-import-container">
    <!-- Header -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-5">
      <div>
        <h2 class="text-h5 font-weight-bold mb-1">استيراد بنك الأسئلة</h2>
        <p class="text-body-2 text-medium-emphasis mb-0">رفع ملفات الأسئلة (Excel/CSV)، معاينتها وتجهيزها، ثم استيرادها إلى بنك الأسئلة</p>
      </div>
      <div class="d-flex align-center gap-3">
        <custom-btn
          type="add"
          icon="mdi-download"
          label="تحميل نموذج الإكسل المعتمد"
          color="primary"
          class="font-weight-bold px-5"
          :click="downloadTemplate"
        />
        <custom-btn
          label="استكمال بيانات الأسئلة"
          icon="mdi-playlist-edit"
          color="indigo"
          variant="tonal"
          class="font-weight-bold px-5"
          :click="() => $router.push('/question-bulk-complete')"
        />
      </div>
    </div>

    <v-row class="align-stretch">
      <!-- Academic Classification Sidebar -->
      <v-col cols="12" md="4" lg="3">
        <v-card rounded="xl" variant="outlined" class="pa-5 h-100 d-flex flex-column justify-space-between bg-surface border">
          <div>
            <div class="d-flex align-center gap-2 mb-4 pb-3 border-b">
              <v-icon color="primary" size="22">mdi-sitemap</v-icon>
              <h3 class="text-subtitle-1 font-weight-bold mb-0">التصنيف الأكاديمي</h3>
            </div>

            <p class="text-caption text-medium-emphasis mb-4">
              حدد المادة والوحدة والدرس لربط الأسئلة المستوردة بها في الشجرة الأكاديمية:
            </p>

            <v-form ref="formRef">
              <!-- Institution Type Selector -->
              <div class="mb-4">
                <v-btn-toggle
                  v-model="form.institution_type"
                  mandatory
                  color="primary"
                  variant="outlined"
                  density="compact"
                  rounded="lg"
                  class="w-100 d-flex"
                  @update:model-value="onInstitutionTypeToggle"
                >
                  <v-btn value="school" class="flex-grow-1 font-weight-bold text-caption">مدرسي</v-btn>
                  <v-btn value="university" class="flex-grow-1 font-weight-bold text-caption">جامعي</v-btn>
                  <v-btn value="institute" class="flex-grow-1 font-weight-bold text-caption">معاهد</v-btn>
                </v-btn-toggle>
              </div>

              <!-- School Fields -->
              <template v-if="form.institution_type === 'school'">
                <auto-list
                  v-model="form.stageId"
                  name="Stage"
                  label="المرحلة الدراسية"
                  cols="12"
                  :add="false"
                  @update:model-value="onStageChange"
                />

                <auto-list
                  v-model="form.classTrackId"
                  name="ClassTrackByStage"
                  :param="form.stageId"
                  label="الصف والمسار"
                  cols="12"
                  :add="false"
                  :disabled="!form.stageId"
                />

                <auto-list
                  v-model="form.subjectId"
                  name="Subject"
                  label="المادة الدراسية"
                  cols="12"
                  :add="false"
                  @update:model-value="onSubjectChange"
                />

                <auto-list
                  v-model="form.semesterId"
                  name="Semester"
                  label="الفصل الدراسي"
                  cols="12"
                  :add="false"
                />
              </template>

              <!-- University Fields -->
              <template v-if="form.institution_type === 'university'">
                <auto-list
                  v-model="form.collegeId"
                  name="College"
                  label="الكلية الجامعية"
                  cols="12"
                  :add="false"
                  @update:model-value="onCollegeChange"
                />

                <auto-list
                  v-model="form.departmentId"
                  name="DepartmentByCollege"
                  :param="form.collegeId"
                  label="القسم الأكاديمي"
                  cols="12"
                  :add="false"
                  :disabled="!form.collegeId"
                  @update:model-value="form.specializationId = null"
                />

                <auto-list
                  v-model="form.specializationId"
                  name="Specialization"
                  :param="form.departmentId"
                  label="التخصص"
                  cols="12"
                  :add="false"
                  :disabled="!form.departmentId"
                  @update:model-value="form.semesterSubjectId = null"
                />

                <auto-list
                  v-model="form.semesterSubjectId"
                  name="SemesterSubject"
                  :param="form.specializationId"
                  label="المقرر الدراسي"
                  cols="12"
                  :add="false"
                  @update:model-value="onSemesterSubjectChange"
                />
              </template>

              <!-- Institute Fields -->
              <template v-if="form.institution_type === 'institute'">
                <auto-list
                  v-model="form.instituteFieldId"
                  name="InstituteField"
                  label="المجال المهني"
                  cols="12"
                  :add="false"
                  @update:model-value="onInstituteFieldChange"
                />

                <auto-list
                  v-model="form.instituteEducationSystemId"
                  name="InstituteEducationSystem"
                  label="نظام التعليم"
                  cols="12"
                  :add="false"
                  @update:model-value="onInstituteEducationSystemChange"
                />

                <auto-list
                  v-model="form.instituteSpecializationId"
                  name="InstituteSpecialization"
                  :param="instituteSpecParam"
                  label="التخصص المهني"
                  cols="12"
                  :add="false"
                  :disabled="!form.instituteFieldId && !form.instituteEducationSystemId"
                  @update:model-value="onInstituteSpecializationChange"
                />

                <auto-list
                  v-model="form.instituteCurriculumId"
                  name="InstituteCurriculum"
                  :param="form.instituteSpecializationId"
                  label="الخطة الدراسية"
                  cols="12"
                  :add="false"
                  :disabled="!form.instituteSpecializationId"
                  @update:model-value="onInstituteCurriculumChange"
                />

                <auto-list
                  v-model="form.instituteSubjectId"
                  name="InstituteSubject"
                  :param="form.instituteCurriculumId"
                  label="المادة التدريبية"
                  cols="12"
                  :add="false"
                  :disabled="!form.instituteCurriculumId"
                  @update:model-value="onInstituteSubjectChange"
                />
              </template>

              <!-- Common Unit and Lesson -->
              <auto-list
                v-model="form.unitId"
                name="UnitBySubject"
                :param="formUnitParam"
                :label="form.institution_type === 'university' ? 'موضوع المقرر' : (form.institution_type === 'institute' ? 'الوحدة التدريبية' : 'الوحدة الدراسية')"
                cols="12"
                :add="false"
                :disabled="form.institution_type === 'university' ? !form.semesterSubjectId : (form.institution_type === 'institute' ? !form.instituteSubjectId : !form.subjectId)"
                @update:model-value="onUnitChange"
              />

              <auto-list
                v-model="form.lessonId"
                name="LessonByUnit"
                :param="form.unitId"
                :label="form.institution_type === 'university' ? 'المحاضرة' : (form.institution_type === 'institute' ? 'الدرس العملي' : 'الدرس')"
                cols="12"
                :add="false"
                :disabled="!form.unitId"
              />
            </v-form>
          </div>

          <!-- Subtle instructions footer -->
          <div class="mt-4 pt-3 border-t text-caption text-medium-emphasis">
            <div class="font-weight-bold mb-1 text-high-emphasis">ملاحظة:</div>
            يدعم الاستيراد الأسئلة الموضوعية (اختيار واحد، خيارات متعددة، صح وخطأ) والأسئلة المقالية.
          </div>
        </v-card>
      </v-col>

      <!-- Main Area: File Dropzone & Table Preview -->
      <v-col cols="12" md="8" lg="9">
        <v-card rounded="xl" variant="outlined" class="pa-5 h-100 d-flex flex-column justify-space-between bg-surface border">
          <div>
            <!-- Dropzone (if no file loaded) -->
            <div
              v-if="!parsedPreview || parsedPreview.total === 0"
              class="upload-dropzone pa-8 rounded-xl text-center d-flex flex-column align-center justify-center mb-4"
              :class="{ 'is-dragover': isDragover }"
              @dragover.prevent="isDragover = true"
              @dragleave.prevent="isDragover = false"
              @drop.prevent="onDrop"
              @click="triggerFileInput"
            >
              <input
                type="file"
                ref="fileInput"
                accept=".xlsx, .xls, .csv"
                class="d-none"
                @change="onFileChange"
              />
              <v-icon size="48" color="primary" class="mb-3">mdi-file-excel-outline</v-icon>
              <h4 class="text-subtitle-1 font-weight-bold mb-1">انقر لاختيار ملف الإكسل أو اسحبه هنا</h4>
              <p class="text-caption text-medium-emphasis mb-3">الملفات المدعومة: XLSX, XLS, CSV</p>
              <v-btn variant="outlined" size="small" color="primary" class="font-weight-bold">
                تصفح الملفات
              </v-btn>
            </div>

            <!-- Loaded File Header Info Bar -->
            <div v-if="selectedFile" class="d-flex align-center justify-space-between pa-3 rounded-lg bg-grey-lighten-4 mb-4 border">
              <div class="d-flex align-center gap-3">
                <v-icon color="success" size="24">mdi-file-excel</v-icon>
                <div>
                  <span class="font-weight-bold text-body-2">{{ selectedFile.name }}</span>
                  <span class="text-caption text-medium-emphasis ms-2">({{ formatBytes(selectedFile.size) }})</span>
                </div>
              </div>
              <div class="d-flex align-center gap-2">
                <v-btn size="small" variant="text" prepend-icon="mdi-refresh" @click="reparseFile">
                  إعادة قراءة الملف
                </v-btn>
                <v-btn size="small" variant="text" color="error" prepend-icon="mdi-close" @click="removeFile">
                  تغيير الملف
                </v-btn>
              </div>
            </div>

            <!-- Table & Summary Section -->
            <div v-if="parsedPreview && parsedPreview.total > 0">
              <!-- Summary Bar (Official, Clean Style) -->
              <div class="d-flex align-center justify-space-between flex-wrap gap-3 pb-3 mb-3 border-b">
                <div class="d-flex align-center gap-3">
                  <span class="text-subtitle-2 font-weight-bold">معاينة وتجهيز الأسئلة</span>
                  <span class="text-caption text-medium-emphasis">
                    (إجمالي: {{ parsedPreview.total }} | جاهزة: <span class="text-success font-weight-bold">{{ parsedPreview.validCount }}</span> | تحتاج إكمال: <span :class="parsedPreview.errorCount > 0 ? 'text-error font-weight-bold' : 'text-medium-emphasis'">{{ parsedPreview.errorCount }}</span>)
                  </span>
                </div>

                <!-- Filters & Quick Actions -->
                <div class="d-flex align-center gap-2 flex-wrap">
                  <v-btn-toggle v-model="previewFilter" mandatory density="compact" variant="outlined" rounded="lg">
                    <v-btn value="all" size="small" class="text-caption">الكل ({{ parsedPreview.total }})</v-btn>
                    <v-btn value="valid" size="small" class="text-caption" color="success">السليمة ({{ parsedPreview.validCount }})</v-btn>
                    <v-btn value="error" size="small" class="text-caption" color="error">تحتاج إكمال ({{ parsedPreview.errorCount }})</v-btn>
                  </v-btn-toggle>

                  <v-btn
                    v-if="parsedPreview.errorCount > 0"
                    size="small"
                    variant="tonal"
                    color="warning"
                    prepend-icon="mdi-filter-minus-outline"
                    class="text-caption font-weight-bold"
                    @click="excludeInvalidRows"
                  >
                    استبعاد الأسئلة غير المكتملة
                  </v-btn>

                  <v-btn
                    size="small"
                    variant="outlined"
                    prepend-icon="mdi-plus"
                    class="text-caption"
                    @click="addNewRow"
                  >
                    إضافة سؤال
                  </v-btn>
                </div>
              </div>

              <!-- Inline Editable Table -->
              <div class="table-wrapper rounded-lg border overflow-hidden">
                <v-table density="compact" class="preview-data-table">
                  <thead>
                    <tr>
                      <th style="width: 45px;" class="text-center">#</th>
                      <th style="width: 140px;">نوع السؤال</th>
                      <th style="min-width: 200px;">نص السؤال</th>
                      <th style="width: 110px;">الخيار 1</th>
                      <th style="width: 110px;">الخيار 2</th>
                      <th style="width: 110px;">الخيار 3</th>
                      <th style="width: 110px;">الخيار 4</th>
                      <th style="width: 150px;">الإجابة الصحيحة</th>
                      <th style="width: 65px;" class="text-center">الدرجة</th>
                      <th style="width: 80px;" class="text-center">الحالة</th>
                      <th style="width: 90px;" class="text-center">إجراءات</th>
                    </tr>
                  </thead>
                  <tbody>
                    <template v-for="(row, idx) in filteredPreviewRows" :key="row.uid">
                      <tr
                        :class="{ 'editing-row': editingUid === row.uid, 'has-error': row.errors.length > 0 }"
                      >
                        <!-- # -->
                        <td class="text-center text-caption font-weight-bold">{{ row.rowNum }}</td>

                        <!-- Question Type -->
                        <td>
                          <template v-if="editingUid === row.uid">
                            <v-select
                              v-model="editForm.type"
                              :items="questionTypes"
                              item-title="title"
                              item-value="value"
                              density="compact"
                              variant="outlined"
                              hide-details
                              class="table-inline-input"
                              @update:model-value="onInlineTypeChange"
                            />
                          </template>
                          <template v-else>
                            <span class="text-caption font-weight-medium">{{ getTypeText(row.type) }}</span>
                          </template>
                        </td>

                        <!-- Question Content Text -->
                        <td>
                          <template v-if="editingUid === row.uid">
                            <v-text-field
                              v-model="editForm.text"
                              placeholder="اكتب نص السؤال هنا..."
                              density="compact"
                              variant="outlined"
                              hide-details
                              class="table-inline-input"
                            />
                          </template>
                          <template v-else>
                            <div class="text-truncate text-caption" style="max-width: 240px;" :title="row.text">
                              <span v-if="!row.text" class="text-error font-weight-bold">
                                • نص السؤال فارغ
                              </span>
                              <span v-else>{{ row.text }}</span>
                            </div>
                          </template>
                        </td>

                        <!-- Option 1 -->
                        <td>
                          <!-- If True/False or Essay, hide options completely -->
                          <template v-if="!needsOptions(editingUid === row.uid ? editForm.type : row.type)">
                            <div class="text-center text-medium-emphasis text-caption">—</div>
                          </template>
                          <template v-else-if="editingUid === row.uid">
                            <v-text-field
                              v-model="editForm.opt1"
                              placeholder="الخيار 1"
                              density="compact"
                              variant="outlined"
                              hide-details
                              class="table-inline-input"
                            />
                          </template>
                          <template v-else>
                            <div class="text-truncate text-caption" style="max-width: 110px;" :title="row.opt1">
                              <span v-if="!row.opt1" class="text-error">
                                • فارغ
                              </span>
                              <span v-else>{{ row.opt1 }}</span>
                            </div>
                          </template>
                        </td>

                        <!-- Option 2 -->
                        <td>
                          <template v-if="!needsOptions(editingUid === row.uid ? editForm.type : row.type)">
                            <div class="text-center text-medium-emphasis text-caption">—</div>
                          </template>
                          <template v-else-if="editingUid === row.uid">
                            <v-text-field
                              v-model="editForm.opt2"
                              placeholder="الخيار 2"
                              density="compact"
                              variant="outlined"
                              hide-details
                              class="table-inline-input"
                            />
                          </template>
                          <template v-else>
                            <div class="text-truncate text-caption" style="max-width: 110px;" :title="row.opt2">
                              <span v-if="!row.opt2" class="text-error">
                                • فارغ
                              </span>
                              <span v-else>{{ row.opt2 }}</span>
                            </div>
                          </template>
                        </td>

                        <!-- Option 3 -->
                        <td>
                          <template v-if="!needsOptions(editingUid === row.uid ? editForm.type : row.type)">
                            <div class="text-center text-medium-emphasis text-caption">—</div>
                          </template>
                          <template v-else-if="editingUid === row.uid">
                            <v-text-field
                              v-model="editForm.opt3"
                              placeholder="الخيار 3"
                              density="compact"
                              variant="outlined"
                              hide-details
                              class="table-inline-input"
                            />
                          </template>
                          <template v-else>
                            <div class="text-truncate text-caption" style="max-width: 110px;" :title="row.opt3">
                              {{ row.opt3 || '' }}
                            </div>
                          </template>
                        </td>

                        <!-- Option 4 -->
                        <td>
                          <template v-if="!needsOptions(editingUid === row.uid ? editForm.type : row.type)">
                            <div class="text-center text-medium-emphasis text-caption">—</div>
                          </template>
                          <template v-else-if="editingUid === row.uid">
                            <v-text-field
                              v-model="editForm.opt4"
                              placeholder="الخيار 4"
                              density="compact"
                              variant="outlined"
                              hide-details
                              class="table-inline-input"
                            />
                          </template>
                          <template v-else>
                            <div class="text-truncate text-caption" style="max-width: 110px;" :title="row.opt4">
                              {{ row.opt4 || '' }}
                            </div>
                          </template>
                        </td>

                        <!-- Correct Answer -->
                        <td>
                          <template v-if="editingUid === row.uid">
                            <!-- 1. Single Choice dropdown -->
                            <v-select
                              v-if="editForm.type === 'Single Choice'"
                              v-model="editForm.answer"
                              :items="inlineChoiceItems"
                              item-title="title"
                              item-value="value"
                              density="compact"
                              variant="outlined"
                              hide-details
                              class="table-inline-input"
                            />

                            <!-- 2. Multiple Choice multi-select with chips -->
                            <v-select
                              v-else-if="editForm.type === 'Multiple Choice'"
                              v-model="editForm.multipleAnswers"
                              :items="inlineChoiceItems"
                              item-title="title"
                              item-value="value"
                              multiple
                              chips
                              closable-chips
                              density="compact"
                              variant="outlined"
                              hide-details
                              class="table-inline-input"
                              placeholder="حدد الإجابات الصحيحة..."
                            />

                            <!-- 3. True/False dropdown (NO options shown) -->
                            <v-select
                              v-else-if="editForm.type === 'True/False'"
                              v-model="editForm.answer"
                              :items="['صح', 'خطأ']"
                              density="compact"
                              variant="outlined"
                              hide-details
                              class="table-inline-input"
                            />

                            <!-- 4. Essay note pointing to large textarea below -->
                            <div v-else class="text-caption text-primary font-weight-bold d-flex align-center gap-1">
                              <v-icon size="14">mdi-arrow-down</v-icon>
                              <span>اكتب الإجابة أدناه</span>
                            </div>
                          </template>

                          <!-- Display Mode for Answer -->
                          <template v-else>
                            <div class="text-truncate text-caption" style="max-width: 150px;" :title="row.answer">
                              <span v-if="!row.answer" class="text-error font-weight-bold">
                                • غير محددة
                              </span>
                              <span v-else class="font-weight-medium">{{ formatDisplayAnswer(row) }}</span>
                            </div>
                          </template>
                        </td>

                        <!-- Mark -->
                        <td class="text-center">
                          <template v-if="editingUid === row.uid">
                            <v-text-field
                              v-model.number="editForm.mark"
                              type="number"
                              min="0.5"
                              step="0.5"
                              density="compact"
                              variant="outlined"
                              hide-details
                              class="table-inline-input text-center"
                              style="width: 55px; margin: 0 auto;"
                            />
                          </template>
                          <template v-else>
                            <span class="text-caption font-weight-medium">{{ row.mark || 1 }}</span>
                          </template>
                        </td>

                        <!-- Status -->
                        <td class="text-center">
                          <span v-if="row.errors.length === 0" class="status-badge status-valid">
                            سليم
                          </span>
                          <span v-else class="status-badge status-invalid" :title="row.errors.map(e => errorLabel(e)).join(', ')">
                            ناقص
                          </span>
                        </td>

                        <!-- Actions -->
                        <td class="text-center">
                          <div class="d-flex align-center justify-center gap-1">
                            <template v-if="editingUid === row.uid">
                              <v-btn icon size="x-small" variant="flat" color="success" title="حفظ التعديل" @click="saveInlineEdit(row)">
                                <v-icon size="16">mdi-check</v-icon>
                              </v-btn>
                              <v-btn icon size="x-small" variant="text" color="grey" title="إلغاء" @click="cancelInlineEdit">
                                <v-icon size="16">mdi-close</v-icon>
                              </v-btn>
                            </template>
                            <template v-else>
                              <v-btn icon size="x-small" variant="text" color="primary" title="تعديل هذا السطر مباشرة" @click="startInlineEdit(row)">
                                <v-icon size="16">mdi-pencil-outline</v-icon>
                              </v-btn>
                              <v-btn icon size="x-small" variant="text" color="error" title="حذف هذا السؤال" @click="deleteRow(row)">
                                <v-icon size="16">mdi-delete-outline</v-icon>
                              </v-btn>
                            </template>
                          </div>
                        </td>
                      </tr>

                      <!-- Large Textarea Sub-Row for Essay Questions when Editing -->
                      <tr v-if="editingUid === row.uid && editForm.type === 'Essay'" class="editing-subrow">
                        <td colspan="11" class="pa-3 bg-grey-lighten-5 border-b">
                          <div class="d-flex flex-column gap-2">
                            <div class="d-flex align-center gap-1 text-caption font-weight-bold text-primary">
                              <v-icon size="16" color="primary">mdi-text-box-edit-outline</v-icon>
                              <span>الإجابة النموذجية المرجعية للسؤال المقالي (حقل نص موسع):</span>
                            </div>
                            <v-textarea
                              v-model="editForm.answer"
                              placeholder="اكتب أو الصق نص الإجابة النموذجية بالتفصيل هنا..."
                              rows="3"
                              auto-grow
                              density="compact"
                              variant="outlined"
                              hide-details
                              class="bg-white rounded-lg"
                            />
                          </div>
                        </td>
                      </tr>
                    </template>

                    <tr v-if="filteredPreviewRows.length === 0">
                      <td colspan="11" class="text-center text-medium-emphasis py-6">
                        لا توجد أسئلة في هذا القسم
                      </td>
                    </tr>
                  </tbody>
                </v-table>
              </div>
            </div>
          </div>

          <!-- Bottom Actions Bar -->
          <div class="mt-5 pt-4 border-t d-flex align-center justify-space-between flex-wrap gap-3">
            <div class="text-caption text-medium-emphasis">
              <span v-if="!isHierarchyValid">يرجى تحديد المادة والوحدة والدرس للمتابعة</span>
              <span v-else-if="!parsedPreview || parsedPreview.total === 0">يرجى رفع ملف الأسئلة لمعاينته</span>
              <span v-else-if="parsedPreview.errorCount > 0" class="text-error font-weight-medium">
                توجد أسئلة غير مكتملة، يرجى تعديلها مباشرة في الجدول بالضغط على أيقونة التعديل (✏️) أو النقر على "استبعاد الأسئلة غير المكتملة".
              </span>
              <span v-else class="text-success font-weight-medium">
                جميع الأسئلة جاهزة للاستيراد ({{ parsedPreview.validCount }} سؤال)
              </span>
            </div>

            <div class="d-flex align-center gap-2">
              <custom-btn
                v-if="parsedPreview && parsedPreview.errorCount > 0 && parsedPreview.validCount > 0"
                label="استيراد الأسئلة السليمة فقط"
                icon="mdi-upload-outline"
                color="indigo"
                variant="tonal"
                class="font-weight-bold px-4"
                :disabled="!isHierarchyValid"
                :loading="isSubmitting"
                :click="() => submitImport(true)"
              />

              <custom-btn
                type="add"
                :label="`بدء استيراد الأسئلة (${parsedPreview ? parsedPreview.validCount : 0})`"
                icon="mdi-upload"
                color="primary"
                class="font-weight-bold px-7"
                :disabled="!isValidToSubmit"
                :loading="isSubmitting"
                :click="() => submitImport(false)"
              />
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import * as XLSX from "xlsx";
import { bankService } from "@/services/bankService";

export default {
  name: "QuestionImportView",

  data() {
    return {
      isSubmitting: false,

      // Context Form
      form: {
        institution_type: "school",
        stageId: null,
        classTrackId: null,
        subjectId: null,
        semesterId: null,
        collegeId: null,
        departmentId: null,
        specializationId: null,
        semesterSubjectId: null,
        instituteFieldId: null,
        instituteEducationSystemId: null,
        instituteSpecializationId: null,
        instituteCurriculumId: null,
        instituteSubjectId: null,
        unitId: null,
        lessonId: null,
      },

      // File & Preview
      isDragover: false,
      selectedFile: null,
      parsedPreview: null,
      previewFilter: "all", // 'all' | 'valid' | 'error'

      // Inline Editing State
      editingUid: null,
      editForm: {
        type: "Single Choice",
        text: "",
        opt1: "",
        opt2: "",
        opt3: "",
        opt4: "",
        answer: "1",
        multipleAnswers: ["1"],
        mark: 1,
      },

      questionTypes: [
        { title: "اختيار واحد", value: "Single Choice" },
        { title: "خيارات متعددة", value: "Multiple Choice" },
        { title: "صح وخطأ", value: "True/False" },
        { title: "مقالي", value: "Essay" },
      ],
    };
  },

  computed: {
    instituteSpecParam() {
      const p = {};
      if (this.form.instituteFieldId) p.field = this.form.instituteFieldId;
      if (this.form.instituteEducationSystemId) p.education_system = this.form.instituteEducationSystemId;
      return Object.keys(p).length ? p : null;
    },

    formUnitParam() {
      if (this.form.institution_type === "university") {
        return this.form.semesterSubjectId ? { semester_subject: this.form.semesterSubjectId } : null;
      }
      if (this.form.institution_type === "institute") {
        return this.form.instituteSubjectId ? { institute_subject: this.form.instituteSubjectId } : null;
      }
      return this.form.subjectId ? { subject: this.form.subjectId } : null;
    },

    isHierarchyValid() {
      if (this.form.institution_type === "university") {
        return !!(this.form.semesterSubjectId && this.form.unitId && this.form.lessonId);
      } else if (this.form.institution_type === "institute") {
        return !!(this.form.instituteSubjectId && this.form.unitId && this.form.lessonId);
      } else {
        return !!(this.form.subjectId && this.form.unitId && this.form.lessonId);
      }
    },

    isValidToSubmit() {
      const hasValid = this.parsedPreview && this.parsedPreview.validCount > 0;
      const noErrors = this.parsedPreview ? this.parsedPreview.errorCount === 0 : false;
      return !!(this.isHierarchyValid && hasValid && noErrors && !this.editingUid);
    },

    filteredPreviewRows() {
      if (!this.parsedPreview || !this.parsedPreview.rows) return [];
      const rows = this.parsedPreview.rows;
      if (this.previewFilter === "valid") return rows.filter((r) => r.errors.length === 0);
      if (this.previewFilter === "error") return rows.filter((r) => r.errors.length > 0);
      return rows;
    },

    inlineChoiceItems() {
      const items = [];
      const opt1 = this.editForm.opt1 ? `1: ${this.editForm.opt1}` : "الخيار 1";
      const opt2 = this.editForm.opt2 ? `2: ${this.editForm.opt2}` : "الخيار 2";
      items.push({ title: opt1, value: "1" });
      items.push({ title: opt2, value: "2" });
      if (this.editForm.opt3) items.push({ title: `3: ${this.editForm.opt3}`, value: "3" });
      else items.push({ title: "الخيار 3", value: "3" });
      if (this.editForm.opt4) items.push({ title: `4: ${this.editForm.opt4}`, value: "4" });
      else items.push({ title: "الخيار 4", value: "4" });
      return items;
    },
  },

  methods: {
    // === CASCADE HANDLERS ===
    onInstitutionTypeToggle() {
      this.form.stageId = null;
      this.form.classTrackId = null;
      this.form.subjectId = null;
      this.form.semesterId = null;
      this.form.collegeId = null;
      this.form.departmentId = null;
      this.form.specializationId = null;
      this.form.semesterSubjectId = null;
      this.form.instituteFieldId = null;
      this.form.instituteEducationSystemId = null;
      this.form.instituteSpecializationId = null;
      this.form.instituteCurriculumId = null;
      this.form.instituteSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
    },

    onStageChange() {
      this.form.classTrackId = null;
    },

    onSubjectChange() {
      this.form.unitId = null;
      this.form.lessonId = null;
    },

    onCollegeChange() {
      this.form.departmentId = null;
      this.form.specializationId = null;
      this.form.semesterSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
    },

    onSemesterSubjectChange() {
      this.form.unitId = null;
      this.form.lessonId = null;
    },

    onInstituteFieldChange() {
      this.form.instituteSpecializationId = null;
      this.form.instituteCurriculumId = null;
      this.form.instituteSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
    },

    onInstituteEducationSystemChange() {
      this.form.instituteSpecializationId = null;
      this.form.instituteCurriculumId = null;
      this.form.instituteSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
    },

    onInstituteSpecializationChange() {
      this.form.instituteCurriculumId = null;
      this.form.instituteSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
    },

    onInstituteCurriculumChange() {
      this.form.instituteSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
    },

    onInstituteSubjectChange() {
      this.form.unitId = null;
      this.form.lessonId = null;
    },

    onUnitChange() {
      this.form.lessonId = null;
    },

    // === FILE HANDLING ===
    triggerFileInput() {
      if (this.$refs.fileInput) {
        this.$refs.fileInput.click();
      }
    },

    onFileChange(event) {
      const files = event.target.files;
      if (files && files.length > 0) {
        this.selectedFile = files[0];
        this.parsePreviewFile(this.selectedFile);
      }
    },

    onDrop(event) {
      this.isDragover = false;
      const files = event.dataTransfer.files;
      if (files && files.length > 0) {
        const file = files[0];
        const ext = file.name.split(".").pop().toLowerCase();
        if (["xlsx", "xls", "csv"].includes(ext)) {
          this.selectedFile = file;
          this.parsePreviewFile(this.selectedFile);
        } else {
          this.$alert("errorData", { message: "نوع الملف غير مدعوم. يرجى اختيار ملف إكسل أو CSV." });
        }
      }
    },

    removeFile() {
      this.selectedFile = null;
      this.parsedPreview = null;
      this.editingUid = null;
      if (this.$refs.fileInput) this.$refs.fileInput.value = "";
    },

    reparseFile() {
      if (this.selectedFile) {
        this.parsePreviewFile(this.selectedFile);
      }
    },

    formatBytes(bytes) {
      if (!bytes) return "0 B";
      const k = 1024;
      const sizes = ["B", "KB", "MB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return (bytes / Math.pow(k, i)).toFixed(1) + " " + sizes[i];
    },

    formatDisplayAnswer(row) {
      if (row.type === "Multiple Choice") {
        return row.answer || "-";
      }
      return row.answer || "-";
    },

    // === TEMPLATE DOWNLOAD ===
    downloadTemplate() {
      const wb = XLSX.utils.book_new();
      const wsData = [
        [
          "نوع السؤال",
          "نص السؤال",
          "الخيار 1",
          "الخيار 2",
          "الخيار 3",
          "الخيار 4",
          "الإجابة الصحيحة",
          "الدرجة",
          "مستوى الصعوبة",
          "مستوى بلوم"
        ],
        [
          "اختيار واحد",
          "ما هي عاصمة الجمهورية اليمنية؟",
          "صنعاء",
          "عدن",
          "تعز",
          "مأرب",
          "1",
          1,
          "سهل",
          "تذكر"
        ],
        [
          "خيارات متعددة",
          "أي من المدن التالية تعتبر مدناً ساحلية يمنية؟",
          "عدن",
          "صنعاء",
          "المكلا",
          "ذمار",
          "1, 3",
          2,
          "متوسط",
          "فهم"
        ],
        [
          "صح وخطأ",
          "تقع مدينة صنعاء التاريخية في قارة آسيا.",
          "",
          "",
          "",
          "",
          "صح",
          1,
          "سهل",
          "تذكر"
        ],
        [
          "مقالي",
          "اشرح الأهمية الاستراتيجية لموقع مضيق باب المندب للتجارة الدولية.",
          "",
          "",
          "",
          "",
          "ممر مائي استراتيجي يربط البحر الأحمر بالمحيط الهندي...",
          3,
          "صعب",
          "تحليل"
        ]
      ];
      const ws = XLSX.utils.aoa_to_sheet(wsData);
      ws["!cols"] = [
        { wch: 16 },
        { wch: 45 },
        { wch: 18 },
        { wch: 18 },
        { wch: 18 },
        { wch: 18 },
        { wch: 20 },
        { wch: 10 },
        { wch: 14 },
        { wch: 14 }
      ];
      XLSX.utils.book_append_sheet(wb, ws, "الأسئلة");
      XLSX.writeFile(wb, "Universal_Questions_Template.xlsx");
    },

    // === PARSE EXCEL ===
    async parsePreviewFile(file) {
      if (!file) return;
      try {
        const data = await file.arrayBuffer();
        const workbook = XLSX.read(data, { type: "array" });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        const rawJson = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

        if (!rawJson || rawJson.length < 2) {
          this.parsedPreview = null;
          this.$alert("errorData", { message: "الملف فارغ أو لا يحتوي على صفوف صالحة." });
          return;
        }

        const headers = (rawJson[0] || []).map((h) => String(h || "").trim().toLowerCase());
        let typeIdx = -1;
        let qIdx = -1;
        let opt1Idx = -1;
        let opt2Idx = -1;
        let opt3Idx = -1;
        let opt4Idx = -1;
        let ansIdx = -1;
        let markIdx = -1;

        const optIndices = [];
        headers.forEach((h, idx) => {
          if (h.includes("نوع") || h.includes("type")) typeIdx = idx;
          else if (h.includes("نص") || h.includes("سؤال") || h.includes("content") || h.includes("question")) qIdx = idx;

          const isOpt = h.includes("خيار") || h.includes("بديل") || h.includes("option") || h.includes("opt");
          if (isOpt) {
            optIndices.push(idx);
            if (h.includes("1") || h.includes("اول") || h.includes("أول") || h.includes("first") || h.includes("a")) opt1Idx = idx;
            else if (h.includes("2") || h.includes("ثاني") || h.includes("ثان") || h.includes("second") || h.includes("b")) opt2Idx = idx;
            else if (h.includes("3") || h.includes("ثالث") || h.includes("third") || h.includes("c")) opt3Idx = idx;
            else if (h.includes("4") || h.includes("رابع") || h.includes("fourth") || h.includes("d")) opt4Idx = idx;
          }

          if (h.includes("صحيحة") || h.includes("إجابة") || h.includes("مرجعية") || h.includes("answer") || h.includes("correct")) ansIdx = idx;
          else if (h.includes("درجة") || h.includes("mark") || h.includes("score")) markIdx = idx;
        });

        // Fallback for options
        if (opt1Idx === -1 && optIndices.length >= 1) opt1Idx = optIndices[0];
        if (opt2Idx === -1 && optIndices.length >= 2) opt2Idx = optIndices[1];
        if (opt3Idx === -1 && optIndices.length >= 3) opt3Idx = optIndices[2];
        if (opt4Idx === -1 && optIndices.length >= 4) opt4Idx = optIndices[3];

        // Positional fallbacks for standard template
        if (typeIdx === -1 && qIdx === -1) {
          typeIdx = 0;
          qIdx = 1;
        } else if (qIdx === -1 && typeIdx === 0) {
          qIdx = 1;
        } else if (qIdx === -1) {
          qIdx = 0;
        }

        if (opt1Idx === -1) opt1Idx = qIdx + 1;
        if (opt2Idx === -1) opt2Idx = qIdx + 2;
        if (opt3Idx === -1) opt3Idx = qIdx + 3;
        if (opt4Idx === -1) opt4Idx = qIdx + 4;
        if (ansIdx === -1) ansIdx = opt4Idx + 1;
        if (markIdx === -1) markIdx = ansIdx + 1;

        const previewRows = [];
        let counter = 1;

        for (let i = 1; i < rawJson.length; i++) {
          const row = rawJson[i];
          if (!row || row.length === 0) continue;

          // Skip header repetition or empty lines
          const isAllEmpty = row.every((c) => c === undefined || c === null || String(c).trim() === "");
          if (isAllEmpty) continue;

          const rawText = qIdx >= 0 && qIdx < row.length ? String(row[qIdx] || "").trim() : "";
          if (rawText.startsWith("نص السؤال") || rawText.startsWith("نوع السؤال")) continue;

          const rawType = typeIdx >= 0 && typeIdx < row.length ? String(row[typeIdx] || "").trim().toLowerCase() : "";
          const opt1 = opt1Idx >= 0 && opt1Idx < row.length ? String(row[opt1Idx] || "").trim() : "";
          const opt2 = opt2Idx >= 0 && opt2Idx < row.length ? String(row[opt2Idx] || "").trim() : "";
          const opt3 = opt3Idx >= 0 && opt3Idx < row.length ? String(row[opt3Idx] || "").trim() : "";
          const opt4 = opt4Idx >= 0 && opt4Idx < row.length ? String(row[opt4Idx] || "").trim() : "";
          const rawAns = ansIdx >= 0 && ansIdx < row.length ? String(row[ansIdx] || "").trim() : "";
          const rawMark = markIdx >= 0 && markIdx < row.length ? parseFloat(row[markIdx]) || 1 : 1;

          let determinedType = "Single Choice";
          if (rawType.includes("صح") || rawType.includes("true") || rawType.includes("صواب")) {
            determinedType = "True/False";
          } else if (rawType.includes("متعدد") || rawType.includes("multiple")) {
            determinedType = "Multiple Choice";
          } else if (rawType.includes("مقال") || rawType.includes("essay")) {
            determinedType = "Essay";
          } else if (rawType.includes("واحد") || rawType.includes("single")) {
            determinedType = "Single Choice";
          } else {
            const ansLower = rawAns.toLowerCase();
            if (["صح", "صواب", "نعم", "true", "خطأ", "خطا", "لا", "false"].includes(ansLower)) {
              determinedType = "True/False";
            } else if (ansLower.includes(",") || ansLower.includes("،") || ansLower.includes(";")) {
              determinedType = "Multiple Choice";
            } else if (ansLower.length > 3 && isNaN(Number(ansLower)) && !opt1 && !opt2) {
              determinedType = "Essay";
            } else {
              determinedType = "Single Choice";
            }
          }

          // If True/False or Essay, options are cleared
          const finalOpt1 = (determinedType === "True/False" || determinedType === "Essay") ? "" : opt1;
          const finalOpt2 = (determinedType === "True/False" || determinedType === "Essay") ? "" : opt2;
          const finalOpt3 = (determinedType === "True/False" || determinedType === "Essay") ? "" : opt3;
          const finalOpt4 = (determinedType === "True/False" || determinedType === "Essay") ? "" : opt4;

          const rowObj = {
            uid: `row_${Date.now()}_${counter}_${Math.random().toString(36).substring(2, 6)}`,
            rowNum: counter++,
            text: rawText,
            type: determinedType,
            opt1: finalOpt1,
            opt2: finalOpt2,
            opt3: finalOpt3,
            opt4: finalOpt4,
            answer: rawAns,
            mark: rawMark,
            errors: [],
          };

          this.validateRow(rowObj);
          previewRows.push(rowObj);
        }

        this.syncParsedPreview(previewRows);
      } catch (err) {
        console.error("Parse excel error:", err);
        this.$alert("errorData", { message: "حدث خطأ أثناء قراءة ملف الإكسل. يرجى مراجعة محتوى الملف." });
      }
    },

    validateRow(rowObj) {
      const errors = [];
      if (!rowObj.text || !rowObj.text.trim()) {
        errors.push("no_text");
      }
      if (this.needsOptions(rowObj.type)) {
        if (!rowObj.opt1 || !rowObj.opt2) {
          errors.push("missing_options");
        }
      }
      if (!rowObj.answer || !String(rowObj.answer).trim()) {
        errors.push("no_answer");
      }
      rowObj.errors = errors;
      return errors.length === 0;
    },

    syncParsedPreview(rows) {
      let validCount = 0;
      let errorCount = 0;
      rows.forEach((r, idx) => {
        r.rowNum = idx + 1;
        this.validateRow(r);
        if (r.errors.length === 0) validCount++;
        else errorCount++;
      });

      this.parsedPreview = {
        total: rows.length,
        validCount: validCount,
        errorCount: errorCount,
        rows: rows,
      };
    },

    needsOptions(type) {
      return type === "Single Choice" || type === "Multiple Choice";
    },

    getTypeText(type) {
      const map = {
        "Single Choice": "اختيار واحد",
        "Multiple Choice": "خيارات متعددة",
        "True/False": "صح وخطأ",
        Essay: "مقالي",
      };
      return map[type] || type || "-";
    },

    errorLabel(code) {
      const map = {
        no_text: "نص السؤال غير مكتوب",
        missing_options: "الخيارات 1 و 2 مطلوبة",
        no_answer: "الإجابة الصحيحة غير محددة",
      };
      return map[code] || "بيانات ناقصة";
    },

    // === INLINE EDITING ===
    startInlineEdit(row) {
      this.editingUid = row.uid;

      // Parse multiple answers if Multiple Choice
      let multipleAnswers = [];
      if (row.type === "Multiple Choice" && row.answer) {
        const parts = String(row.answer).replace(/،/g, ",").split(",");
        multipleAnswers = parts.map((p) => p.trim()).filter(Boolean);
      } else if (row.type === "Multiple Choice") {
        multipleAnswers = ["1"];
      }

      this.editForm = {
        type: row.type || "Single Choice",
        text: row.text || "",
        opt1: row.opt1 || "",
        opt2: row.opt2 || "",
        opt3: row.opt3 || "",
        opt4: row.opt4 || "",
        answer: row.answer || (row.type === "True/False" ? "صح" : "1"),
        multipleAnswers: multipleAnswers,
        mark: row.mark || 1,
      };
    },

    cancelInlineEdit() {
      this.editingUid = null;
    },

    saveInlineEdit(row) {
      row.type = this.editForm.type;
      row.text = (this.editForm.text || "").trim();

      if (row.type === "True/False" || row.type === "Essay") {
        row.opt1 = "";
        row.opt2 = "";
        row.opt3 = "";
        row.opt4 = "";
      } else {
        row.opt1 = (this.editForm.opt1 || "").trim();
        row.opt2 = (this.editForm.opt2 || "").trim();
        row.opt3 = (this.editForm.opt3 || "").trim();
        row.opt4 = (this.editForm.opt4 || "").trim();
      }

      if (row.type === "Multiple Choice") {
        const sorted = (this.editForm.multipleAnswers || []).slice().sort();
        row.answer = sorted.join(", ");
      } else {
        row.answer = String(this.editForm.answer || "").trim();
      }

      row.mark = Number(this.editForm.mark) || 1;

      this.syncParsedPreview(this.parsedPreview.rows);
      this.editingUid = null;
    },

    onInlineTypeChange(newType) {
      if (newType === "True/False") {
        if (!["صح", "خطأ"].includes(this.editForm.answer)) {
          this.editForm.answer = "صح";
        }
      } else if (newType === "Single Choice") {
        if (this.editForm.multipleAnswers && this.editForm.multipleAnswers.length > 0) {
          this.editForm.answer = this.editForm.multipleAnswers[0];
        } else if (!["1", "2", "3", "4"].includes(this.editForm.answer)) {
          this.editForm.answer = "1";
        }
      } else if (newType === "Multiple Choice") {
        if (!this.editForm.multipleAnswers || this.editForm.multipleAnswers.length === 0) {
          this.editForm.multipleAnswers = [this.editForm.answer || "1"];
        }
      }
    },

    deleteRow(row) {
      if (!this.parsedPreview || !this.parsedPreview.rows) return;
      const filtered = this.parsedPreview.rows.filter((r) => r.uid !== row.uid);
      if (this.editingUid === row.uid) this.editingUid = null;
      this.syncParsedPreview(filtered);
    },

    addNewRow() {
      const nextNum = (this.parsedPreview?.rows?.length || 0) + 1;
      const newRow = {
        uid: `row_${Date.now()}_new_${Math.random().toString(36).substring(2, 6)}`,
        rowNum: nextNum,
        text: "",
        type: "Single Choice",
        opt1: "",
        opt2: "",
        opt3: "",
        opt4: "",
        answer: "1",
        mark: 1,
        errors: [],
      };
      const rows = this.parsedPreview?.rows || [];
      rows.push(newRow);
      this.syncParsedPreview(rows);
      this.startInlineEdit(newRow);
    },

    excludeInvalidRows() {
      if (!this.parsedPreview || !this.parsedPreview.rows) return;
      const validOnly = this.parsedPreview.rows.filter((r) => r.errors.length === 0);
      const removed = this.parsedPreview.rows.length - validOnly.length;
      this.syncParsedPreview(validOnly);
      this.previewFilter = "all";
      if (this.editingUid) this.editingUid = null;
      this.$alert("success", { message: `تم استبعاد ${removed} أسئلة غير مكتملة.` });
    },

    // === SUBMIT IMPORT ===
    async submitImport(onlyValid = false) {
      if (!this.isHierarchyValid) {
        this.$alert("errorData", { message: "يرجى تحديد المادة والوحدة والدرس أولاً." });
        return;
      }
      if (!this.parsedPreview || this.parsedPreview.rows.length === 0) {
        this.$alert("errorData", { message: "لا توجد أسئلة للاستيراد." });
        return;
      }

      let questionsToImport = this.parsedPreview.rows;
      if (onlyValid || this.parsedPreview.errorCount > 0) {
        questionsToImport = questionsToImport.filter((r) => r.errors.length === 0);
      }

      if (questionsToImport.length === 0) {
        this.$alert("errorData", { message: "لا توجد أسئلة سليمة جاهزة للاستيراد. يرجى إكمال الأسئلة الناقصة أولاً." });
        return;
      }

      const formData = new FormData();
      if (this.selectedFile) {
        formData.append("file", this.selectedFile);
      }
      formData.append("institution_type", this.form.institution_type || "school");
      formData.append("fk_lesson", this.form.lessonId);
      formData.append("questions", JSON.stringify(questionsToImport));

      this.isSubmitting = true;
      try {
        const res = await bankService.importExcelQuestions(formData);
        const count = res?.data?.data?.count || res?.data?.count || res?.count || questionsToImport.length;
        this.$alert("success", { message: `تم استيراد ${count} سؤالاً بنجاح إلى بنك الأسئلة!` });
        this.$navigateTo({ name: "question-bank", blank: false });
      } catch (err) {
        console.error("Import error", err);
        const errMessage = err.response?.data?.message || err.response?.data?.error || "حدث خطأ أثناء الاستيراد";
        this.$alert("errorData", { message: errMessage });
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>

<style scoped>
.qb-import-container {
  color: rgb(var(--v-theme-on-surface));
}

/* Official Upload Dropzone */
.upload-dropzone {
  background: #f8fafc;
  border: 2px dashed #cbd5e1;
  cursor: pointer;
  min-height: 180px;
  transition: all 0.2s ease;
}

.upload-dropzone:hover, .upload-dropzone.is-dragover {
  border-color: rgb(var(--v-theme-primary));
  background: rgba(var(--v-theme-primary), 0.04);
}

/* Official Data Table */
.table-wrapper {
  background: rgb(var(--v-theme-surface));
  max-height: 480px;
  overflow-y: auto;
}

.preview-data-table {
  width: 100%;
  border-collapse: collapse;
}

.preview-data-table thead tr th {
  background: #f8fafc !important;
  color: #475569 !important;
  font-weight: 600 !important;
  font-size: 0.8125rem !important;
  border-bottom: 1px solid #e2e8f0 !important;
  padding: 8px 10px !important;
  white-space: nowrap;
  position: sticky;
  top: 0;
  z-index: 2;
}

.preview-data-table tbody tr td {
  border-bottom: 1px solid #f1f5f9;
  padding: 6px 10px !important;
  font-size: 0.8125rem;
}

.preview-data-table tbody tr:hover {
  background: #f8fafc;
}

/* Editing Row Highlight */
.preview-data-table tbody tr.editing-row {
  background: #f0f7ff !important;
}

.editing-subrow td {
  background: #f8fafc !important;
}

/* Table Inline Input Styling */
.table-inline-input :deep(.v-field__input) {
  padding: 4px 8px !important;
  font-size: 0.8125rem !important;
  min-height: 32px !important;
}

.table-inline-input :deep(.v-field) {
  border-radius: 6px !important;
  background: #ffffff !important;
}

/* Official Clean Status Badges */
.status-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  line-height: 1.4;
}

.status-valid {
  background: #ecfdf5;
  color: #059669;
  border: 1px solid #a7f3d0;
}

.status-invalid {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

/* Gap Utilities */
.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
</style>
