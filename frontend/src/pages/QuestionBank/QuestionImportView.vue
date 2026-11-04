<template>
  <div class="qb-import-page-v4">
    <!-- Action Buttons -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-8">

      <div class="d-flex align-center gap-3">
        <custom-btn
          type="add"
          icon="mdi-download"
          label="تحميل القالب الشامل المعتمد (Excel)"
          color="primary"
          class="font-weight-bold px-6"
          :click="downloadTemplate"
        />
        <custom-btn
          label="استكمال بيانات الأسئلة المستوردة"
          icon="mdi-playlist-edit"
          color="indigo"
          variant="tonal"
          class="font-weight-bold px-6"
          :click="() => $router.push('/question-bulk-complete')"
        />
      </div>
    </div>

    <v-row class="align-stretch">
      <!-- Academic Context Selection Sidebar -->
      <v-col cols="12" md="4">
        <div class="main-card pa-6 rounded-2xl h-100 d-flex flex-column justify-space-between">
          <div>
            <div class="d-flex align-center gap-3 mb-4">
              <v-avatar size="42" color="primary" variant="tonal" class="rounded-xl">
                <v-icon size="22">mdi-sitemap</v-icon>
              </v-avatar>
              <div>
                <h3 class="text-h6 font-weight-black mb-0">التصنيف الأكاديمي المشترك</h3>
                <span class="text-caption text-medium-emphasis">ربط الأسئلة المستوردة بالشجرة الأكاديمية</span>
              </div>
            </div>

            <p class="text-body-2 text-medium-emphasis mb-6">
              يجب تحديد المادة والوحدة والدرس لجميع الأسئلة الواردة في هذا الملف قبل البدء بالاستيراد.
            </p>

            <v-form ref="formRef">
              <!-- Institution Type Selector (مدارس / جامعات) -->
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
                  <v-btn value="school" class="flex-grow-1 font-weight-bold">
                    <v-icon start size="16">mdi-school</v-icon>
                    مدرسي
                  </v-btn>
                  <v-btn value="university" class="flex-grow-1 font-weight-bold">
                    <v-icon start size="16">mdi-domain</v-icon>
                    جامعي
                  </v-btn>
                  <v-btn value="institute" class="flex-grow-1 font-weight-bold">
                    <v-icon start size="16">mdi-domain</v-icon>
                    معاهد
                  </v-btn>
                </v-btn-toggle>
              </div>

              <!-- 🏫 School Academic Classification Fields -->
              <template v-if="form.institution_type === 'school'">
                <!-- Stage -->
                <auto-list
                  v-model="form.stageId"
                  name="Stage"
                  label="المرحلة الدراسية"
                  cols="12"
                  :add="false"
                  @update:model-value="onStageChange"
                />

                <!-- ClassTrack (الصف والمسار) -->
                <auto-list
                  v-model="form.classTrackId"
                  name="ClassTrackByStage"
                  :param="form.stageId"
                  label="الصف والمسار"
                  cols="12"
                  :add="false"
                  :disabled="!form.stageId"
                />

                <!-- Subject -->
                <auto-list
                  v-model="form.subjectId"
                  name="Subject"
                  label="اختر المادة الدراسية"
                  cols="12"
                  :add="false"
                  @update:model-value="onSubjectChange"
                />

                <!-- Semester -->
                <auto-list
                  v-model="form.semesterId"
                  name="Semester"
                  label="الفصل الدراسي"
                  cols="12"
                  :add="false"
                />
              </template>

              <!-- 🎓 University Academic Classification Fields -->
              <template v-if="form.institution_type === 'university'">
                <!-- College -->
                <auto-list
                  v-model="form.collegeId"
                  name="College"
                  label="الكلية الجامعية"
                  cols="12"
                  :add="false"
                  @update:model-value="onCollegeChange"
                />

                <!-- Department -->
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

                <!-- Specialization -->
                <auto-list
                  v-model="form.specializationId"
                  name="Specialization"
                  :param="form.departmentId"
                  label="التخصص والبرنامج"
                  cols="12"
                  :add="false"
                  :disabled="!form.departmentId"
                  @update:model-value="form.semesterSubjectId = null"
                />

                <!-- SemesterSubject (مقرر الفصل الجامعي) -->
                <auto-list
                  v-model="form.semesterSubjectId"
                  name="SemesterSubject"
                  :param="form.specializationId"
                  label="مقرر الفصل الجامعي"
                  cols="12"
                  :add="false"
                  @update:model-value="onSemesterSubjectChange"
                />
              </template>

              <!-- 🏢 Institute Academic Classification Fields -->
              <template v-if="form.institution_type === 'institute'">
                <!-- Field -->
                <auto-list
                  v-model="form.instituteFieldId"
                  name="InstituteField"
                  label="المجال المهني"
                  cols="12"
                  :add="false"
                  @update:model-value="onInstituteFieldChange"
                />

                <!-- Education System -->
                <auto-list
                  v-model="form.instituteEducationSystemId"
                  name="InstituteEducationSystem"
                  label="نظام التعليم"
                  cols="12"
                  :add="false"
                  @update:model-value="onInstituteEducationSystemChange"
                />

                <!-- Specialization -->
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

                <!-- Curriculum -->
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

                <!-- Subject -->
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

              <!-- Common: Unit, Lesson -->
              <!-- Unit -->
              <auto-list
                v-model="form.unitId"
                name="UnitBySubject"
                :param="formUnitParam"
                :label="form.institution_type === 'university' ? 'مفردة / موضوع المقرر' : (form.institution_type === 'institute' ? 'الوحدة التدريبية' : 'الوحدة الدراسية')"
                cols="12"
                :add="false"
                :disabled="form.institution_type === 'university' ? !form.semesterSubjectId : (form.institution_type === 'institute' ? !form.instituteSubjectId : !form.subjectId)"
                @update:model-value="onUnitChange"
              />

              <!-- Lesson -->
              <auto-list
                v-model="form.lessonId"
                name="LessonByUnit"
                :param="form.unitId"
                :label="form.institution_type === 'university' ? 'المحاضرة / الدرس الأكاديمي' : (form.institution_type === 'institute' ? 'الدرس / التمرين العملي' : 'الدرس المدرسي')"
                cols="12"
                :add="false"
                :disabled="!form.unitId"
              />

            </v-form>
          </div>

          <!-- Instructions & Types Guide Card -->
          <div class="mt-4 pa-4 rounded-2xl border" style="background: rgba(var(--v-theme-surface), 0.7);">
            <div class="d-flex align-center gap-2 mb-3">
              <v-icon color="primary" size="20">mdi-lightbulb-on-outline</v-icon>
              <span class="text-subtitle-2 font-weight-black">إرشادات تعبئة أنواع الأسئلة في القالب الموحد:</span>
            </div>

            <div class="d-flex flex-column gap-2 text-caption">
              <!-- Single Choice -->
              <div class="pa-2 rounded-lg border bg-surface d-flex align-start gap-2">
                <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold flex-shrink-0">
                  اختيار واحد
                </v-chip>
                <span class="text-medium-emphasis">
                  الخيارات (1-4)، والإجابة رقم الخيار الصحيح (مثال: <strong class="text-primary">1</strong>).
                </span>
              </div>

              <!-- Multiple Choice -->
              <div class="pa-2 rounded-lg border bg-surface d-flex align-start gap-2">
                <v-chip size="x-small" color="indigo" variant="flat" class="font-weight-bold flex-shrink-0">
                  خيارات متعددة
                </v-chip>
                <span class="text-medium-emphasis">
                  الخيارات، وأرقام الإجابات مفصولة بفواصل (مثال: <strong class="text-indigo">1, 3</strong>).
                </span>
              </div>

              <!-- True / False -->
              <div class="pa-2 rounded-lg border bg-surface d-flex align-start gap-2">
                <v-chip size="x-small" color="teal" variant="flat" class="font-weight-bold flex-shrink-0">
                  صح وخطأ
                </v-chip>
                <span class="text-medium-emphasis">
                  الخيارات فارغة، والإجابة كلمة <strong class="text-teal">صح</strong> أو <strong class="text-teal">خطأ</strong> (أو 1 / 2).
                </span>
              </div>

              <!-- Essay -->
              <div class="pa-2 rounded-lg border bg-surface d-flex align-start gap-2">
                <v-chip size="x-small" color="amber-darken-3" variant="flat" class="font-weight-bold flex-shrink-0">
                  مقالي
                </v-chip>
                <span class="text-medium-emphasis">
                  الخيارات فارغة، والإجابة تحتوي على <strong class="text-amber-darken-3">الإجابة النموذجية المرجعية</strong>.
                </span>
              </div>
            </div>
          </div>
        </div>
      </v-col>

      <!-- Dropzone Upload Panel -->
      <v-col cols="12" md="8">
        <div class="main-card pa-6 rounded-2xl h-100 d-flex flex-column justify-space-between">
          <div>
            <div class="d-flex align-center gap-3 mb-6">
              <v-avatar size="42" color="emerald" variant="tonal" class="rounded-xl">
                <v-icon size="22" color="emerald">mdi-file-upload-outline</v-icon>
              </v-avatar>
              <div>
                <h3 class="text-h6 font-weight-black mb-0">منطقة رفع وتفريغ الملف</h3>
                <span class="text-caption text-medium-emphasis">قم بسحب وإسقاط ملف الإكسل هنا</span>
              </div>
            </div>

            <!-- Upload Dropzone Container -->
            <div
              class="upload-dropzone pa-8 rounded-2xl text-center d-flex flex-column align-center justify-center transition-all"
              :class="{ 'is-dragover': isDragover, 'has-file': !!selectedFile }"
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
              
              <template v-if="!selectedFile">
                <v-avatar size="72" color="primary" variant="tonal" class="mb-4">
                  <v-icon size="36">mdi-cloud-upload-outline</v-icon>
                </v-avatar>
                <h4 class="text-h6 font-weight-black mb-2">اسحب وأفلت ملف الإكسل هنا</h4>
                <p class="text-body-2 text-medium-emphasis mb-4">أو انقر في أي مكان داخل المنطقة لتصفح جهازك</p>
                <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold">
                  الصيغ المدعومة: XLSX, XLS, CSV
                </v-chip>
              </template>
              
              <template v-else>
                <v-avatar size="72" color="emerald" variant="tonal" class="mb-4">
                  <v-icon size="36" color="emerald">mdi-file-excel-box</v-icon>
                </v-avatar>
                <h4 class="text-h6 font-weight-black text-emerald-darken-3 mb-1">{{ selectedFile.name }}</h4>
                <p class="text-caption text-medium-emphasis font-weight-bold mb-4">{{ formatBytes(selectedFile.size) }}</p>
                
                <custom-btn
                  type="del"
                  label="إزالة هذا الملف"
                  class="font-weight-bold"
                  :click="(e) => { if(e) e.stopPropagation(); removeFile(); }"
                />
              </template>
            </div>

            <!-- File Preview & Breakdown Card -->
            <div v-if="parsedPreview && parsedPreview.total > 0" class="mt-4 pa-4 rounded-2xl border" style="background: rgba(var(--v-theme-surface), 0.7);">
              <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-3">
                <div class="d-flex align-center gap-2">
                  <v-icon color="emerald" size="20">mdi-eye-check-outline</v-icon>
                  <span class="text-subtitle-2 font-weight-black">معاينة الأسئلة المقروءة من الملف</span>
                  <v-chip size="x-small" color="primary" variant="flat" class="font-weight-bold">
                    {{ parsedPreview.total }} سؤال
                  </v-chip>
                </div>
                <!-- Breakdown Chips -->
                <div class="d-flex align-center gap-1 flex-wrap">
                  <v-chip v-if="parsedPreview.types['Single Choice']" size="x-small" color="primary" variant="tonal" class="font-weight-bold">
                    {{ parsedPreview.types['Single Choice'] }} اختيار واحد
                  </v-chip>
                  <v-chip v-if="parsedPreview.types['Multiple Choice']" size="x-small" color="indigo" variant="tonal" class="font-weight-bold">
                    {{ parsedPreview.types['Multiple Choice'] }} خيارات متعددة
                  </v-chip>
                  <v-chip v-if="parsedPreview.types['True/False']" size="x-small" color="teal" variant="tonal" class="font-weight-bold">
                    {{ parsedPreview.types['True/False'] }} صح وخطأ
                  </v-chip>
                  <v-chip v-if="parsedPreview.types['Essay']" size="x-small" color="amber-darken-3" variant="tonal" class="font-weight-bold">
                    {{ parsedPreview.types['Essay'] }} مقالي
                  </v-chip>
                </div>
              </div>

              <!-- Preview Table (first 5 questions) -->
              <v-table density="compact" class="bg-transparent rounded-lg border text-caption">
                <thead>
                  <tr style="background: rgba(var(--v-theme-surface-variant), 0.3);">
                    <th style="width: 40px;">#</th>
                    <th style="width: 120px;">النوع</th>
                    <th>نص السؤال</th>
                    <th style="width: 160px;">الإجابة المكتشفة</th>
                    <th style="width: 60px;">الدرجة</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, idx) in parsedPreview.rows.slice(0, 5)" :key="idx">
                    <td class="font-weight-bold">{{ idx + 1 }}</td>
                    <td>
                      <v-chip size="x-small" :color="getTypeColor(row.type)" variant="tonal" class="font-weight-bold">
                        {{ getTypeText(row.type) }}
                      </v-chip>
                    </td>
                    <td class="text-truncate" style="max-width: 250px;">{{ row.text }}</td>
                    <td class="text-truncate font-weight-bold" style="max-width: 160px; color: rgb(var(--v-theme-primary));">
                      {{ row.answer || '-' }}
                    </td>
                    <td>{{ row.mark || 1 }}</td>
                  </tr>
                </tbody>
              </v-table>
              <div v-if="parsedPreview.total > 5" class="text-caption text-medium-emphasis text-center mt-2">
                ... بالإضافة إلى {{ parsedPreview.total - 5 }} أسئلة أخرى سيتم استيرادها
              </div>
            </div>
          </div>

          <!-- Submit Import Actions Bar -->
          <div class="mt-6 pt-4 border-t border-slate-100 d-flex align-center justify-space-between flex-wrap gap-3">
            <div class="d-flex align-center gap-2">
              <v-icon color="emerald" size="18">mdi-check-circle-outline</v-icon>
              <span class="text-caption text-medium-emphasis font-weight-bold">
                {{ isValidToSubmit ? 'جاهز للاستيراد الآن' : 'يرجى تحديد التصنيف الأكاديمي واختيار الملف' }}
              </span>
            </div>

            <custom-btn
              type="add"
              label="بدء استيراد الأسئلة"
              icon="mdi-upload"
              color="primary"
              class="btn-glow-primary font-weight-bold px-8"
              :disabled="!isValidToSubmit"
              :loading="isSubmitting"
              :click="submitImport"
            />
          </div>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import * as XLSX from "xlsx";
import api from "@/services/api";
import { academicService } from "@/services/academicService";
import { bankService } from "@/services/bankService";

export default {
  name: "QuestionImportView",

  data() {
    return {
      loadingSubjects: false,
      loadingUnits: false,
      loadingLessons: false,
      isSubmitting: false,

      // Arrays for v-selects
      subjects: [],
      units: [],
      lessons: [],

      // Context
      form: {
        institution_type: "school",
        // School
        stageId: null,
        classTrackId: null,
        subjectId: null,
        semesterId: null,
        // University
        collegeId: null,
        departmentId: null,
        specializationId: null,
        semesterSubjectId: null,
        // Institute
        instituteFieldId: null,
        instituteEducationSystemId: null,
        instituteSpecializationId: null,
        instituteCurriculumId: null,
        instituteSubjectId: null,
        // Common
        unitId: null,
        lessonId: null,
        learningOutcomeId: null,
      },

      // File
      isDragover: false,
      selectedFile: null,
      parsedPreview: null,

      rules: {
        required: (v) => !!v || "مطلوب",
      },
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

    isValidToSubmit() {
      let isHierarchyValid = false;
      if (this.form.institution_type === "university") {
        isHierarchyValid = !!(this.form.semesterSubjectId && this.form.unitId && this.form.lessonId);
      } else if (this.form.institution_type === "institute") {
        isHierarchyValid = !!(this.form.instituteSubjectId && this.form.unitId && this.form.lessonId);
      } else {
        isHierarchyValid = !!(this.form.subjectId && this.form.unitId && this.form.lessonId);
      }
      return !!(isHierarchyValid && this.selectedFile);
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
      this.form.learningOutcomeId = null;
    },

    onStageChange() {
      this.form.classTrackId = null;
    },

    onSubjectChange() {
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onCollegeChange() {
      this.form.departmentId = null;
      this.form.specializationId = null;
      this.form.semesterSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onSemesterSubjectChange() {
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onInstituteFieldChange() {
      this.form.instituteSpecializationId = null;
      this.form.instituteCurriculumId = null;
      this.form.instituteSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onInstituteEducationSystemChange() {
      this.form.instituteSpecializationId = null;
      this.form.instituteCurriculumId = null;
      this.form.instituteSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onInstituteSpecializationChange() {
      this.form.instituteCurriculumId = null;
      this.form.instituteSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onInstituteCurriculumChange() {
      this.form.instituteSubjectId = null;
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onInstituteSubjectChange() {
      this.form.unitId = null;
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    onUnitChange() {
      this.form.lessonId = null;
      this.form.learningOutcomeId = null;
    },

    // === FILE HANDLING ===
    triggerFileInput() {
      if (!this.selectedFile) {
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
          this.$alert("errorData", { message: "نوع الملف غير مدعوم. يدعم Excel و CSV فقط" });
        }
      }
    },
    removeFile(event) {
      if (event) event.stopPropagation();
      this.selectedFile = null;
      this.parsedPreview = null;
      if (this.$refs.fileInput) this.$refs.fileInput.value = "";
    },
    formatBytes(bytes, decimals = 2) {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ["Bytes", "KB", "MB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
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
          "الإجابة الصحيحة / المرجعية",
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
          "صح وخطأ",
          "يمر نهر النيل في أراضي الجمهورية اليمنية.",
          "",
          "",
          "",
          "",
          "خطأ",
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
          "ممر مائي استراتيجي يربط البحر الأحمر بالمحيط الهندي ويوفر أقصر طريق بحري بين آسيا وأوروبا...",
          3,
          "صعب",
          "تحليل"
        ]
      ];
      const ws = XLSX.utils.aoa_to_sheet(wsData);

      const wscols = [
        { wch: 16 },
        { wch: 45 },
        { wch: 18 },
        { wch: 18 },
        { wch: 18 },
        { wch: 18 },
        { wch: 30 },
        { wch: 10 },
        { wch: 14 },
        { wch: 14 }
      ];
      ws["!cols"] = wscols;

      XLSX.utils.book_append_sheet(wb, ws, "الأسئلة");
      XLSX.writeFile(wb, "Universal_Questions_Template.xlsx");
    },

    async parsePreviewFile(file) {
      if (!file) {
        this.parsedPreview = null;
        return;
      }
      try {
        const data = await file.arrayBuffer();
        const workbook = XLSX.read(data, { type: "array" });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        const rawJson = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

        if (!rawJson || rawJson.length < 2) {
          this.parsedPreview = null;
          return;
        }

        const headers = (rawJson[0] || []).map((h) => String(h || "").trim());
        let typeIdx = -1;
        let qIdx = -1;
        let ansIdx = -1;
        let markIdx = -1;
        const optIndices = [];

        headers.forEach((h, idx) => {
          const hl = h.toLowerCase();
          if (hl.includes("نوع") || hl.includes("type")) typeIdx = idx;
          else if (hl.includes("نص") || hl.includes("سؤال") || hl.includes("content") || hl.includes("question")) qIdx = idx;
          else if (hl.includes("خيار") || hl.includes("بديل") || hl.includes("option")) optIndices.push(idx);
          else if (hl.includes("صحيحة") || hl.includes("إجابة") || hl.includes("مرجعية") || hl.includes("answer") || hl.includes("correct")) ansIdx = idx;
          else if (hl.includes("درجة") || hl.includes("mark")) markIdx = idx;
        });

        const totalCols = (rawJson[0] || []).length;
        if (qIdx === -1) {
          const col0Header = (headers[0] || "").toLowerCase();
          const col0FirstVal = String(rawJson[1]?.[0] || "").toLowerCase();
          const isTypeCol = col0Header.includes("نوع") || ["اختيار واحد", "صح وخطأ", "خيارات متعددة", "مقالي"].some((k) => col0FirstVal.includes(k));
          if (isTypeCol) {
            typeIdx = 0;
            qIdx = 1;
            ansIdx = totalCols > 6 ? 6 : (totalCols === 6 ? 5 : -1);
            markIdx = totalCols > 7 ? 7 : -1;
          } else {
            typeIdx = -1;
            qIdx = 0;
            ansIdx = totalCols > 5 ? 5 : (totalCols === 5 ? 4 : -1);
            markIdx = totalCols > 6 ? 6 : -1;
          }
        }

        const previewRows = [];
        const typeCounts = {
          "Single Choice": 0,
          "Multiple Choice": 0,
          "True/False": 0,
          "Essay": 0,
        };

        for (let i = 1; i < rawJson.length; i++) {
          const row = rawJson[i];
          if (!row || row.length === 0) continue;
          const qText = String(row[qIdx] || "").trim();
          if (!qText || qText.startsWith("نص السؤال") || qText.startsWith("نوع السؤال")) continue;

          const rawType = typeIdx >= 0 ? String(row[typeIdx] || "").trim().toLowerCase() : "";
          const rawAns = ansIdx >= 0 ? String(row[ansIdx] || "").trim() : "";
          const mark = markIdx >= 0 ? parseFloat(row[markIdx]) || 1 : 1;

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
            } else if (ansLower.length > 3 && isNaN(Number(ansLower)) && optIndices.every((oi) => !String(row[oi] || "").trim())) {
              determinedType = "Essay";
            } else {
              determinedType = "Single Choice";
            }
          }

          typeCounts[determinedType] = (typeCounts[determinedType] || 0) + 1;
          previewRows.push({
            text: qText,
            type: determinedType,
            answer: rawAns,
            mark: mark,
          });
        }

        this.parsedPreview = {
          total: previewRows.length,
          types: typeCounts,
          rows: previewRows,
        };
      } catch (err) {
        console.warn("Could not parse excel preview:", err);
        this.parsedPreview = null;
      }
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

    getTypeColor(type) {
      const map = {
        "Single Choice": "primary",
        "Multiple Choice": "indigo",
        "True/False": "teal",
        Essay: "amber-darken-3",
      };
      return map[type] || "grey";
    },

    // === SUBMIT ===
    async submitImport() {
      const { valid } = await this.$refs.formRef.validate();
      if (!valid) {
        this.$alert("errorData", { message: "يرجى اختيار المادة والوحدة والدرس أولاً" });
        return;
      }
      if (!this.selectedFile) return;

      const formData = new FormData();
      formData.append("file", this.selectedFile);
      formData.append("institution_type", this.form.institution_type || "school");
      formData.append("fk_lesson", this.form.lessonId);

      this.isSubmitting = true;
      try {
        const res = await bankService.importExcelQuestions(formData);

        const count = res?.data?.data?.count || res?.data?.count || res?.count || 0;
        this.$alert("success", { message: `تم استيراد ${count} أسئلة بنجاح!` });

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
.qb-import-page-v4 {
  color: rgb(var(--v-theme-on-surface));
}

/* ===== Primary Glow Button ===== */
.btn-glow-primary {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, color-mix(in srgb, rgb(var(--v-theme-primary)) 85%, #000) 100%) !important;
  box-shadow: 0 8px 24px -4px rgba(var(--v-theme-primary), 0.45) !important;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.btn-glow-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 32px -4px rgba(var(--v-theme-primary), 0.55) !important;
}

/* ===== Main Cards (Theme Compatible) ===== */
.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.08);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 4px 12px rgba(0, 0, 0, 0.02);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.main-card:hover {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05), 0 8px 24px rgba(0, 0, 0, 0.03);
}

/* ===== Dropzone Area ===== */
.upload-dropzone {
  background: rgb(var(--v-theme-background));
  border: 2px dashed rgba(var(--v-border-color), 0.18);
  cursor: pointer;
  min-height: 280px;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.upload-dropzone:hover, .upload-dropzone.is-dragover {
  border-color: rgba(var(--v-theme-primary), 0.5);
  background: rgba(var(--v-theme-primary), 0.03);
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(var(--v-theme-primary), 0.08);
}

.upload-dropzone.has-file {
  border-style: solid;
  border-color: rgba(var(--v-theme-success), 0.5);
  background: rgba(var(--v-theme-success), 0.03);
  box-shadow: 0 8px 28px rgba(var(--v-theme-success), 0.08);
  cursor: default;
}

/* ===== Gap Utilities ===== */
.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
</style>
