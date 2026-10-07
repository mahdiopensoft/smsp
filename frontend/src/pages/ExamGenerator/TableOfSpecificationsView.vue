<template>
  <div class="qb-tos-page-v4">
    <!-- Header Controls -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div>
        <h2 class="text-h5 font-weight-black mb-1">جدول المواصفات (Table of Specifications)</h2>
        <span class="text-caption text-medium-emphasis">
          تحديد وتوزيع الأوزان النسبية للوحدات ومستويات بلوم المعرفية قبل توليد الاختبارات
        </span>
      </div>

      <div class="d-flex align-center gap-3">
        <custom-btn
          type="add"
          icon="mdi-plus"
          label="إنشاء جدول مواصفات جديد"
          color="primary"
          class="font-weight-bold px-6"
          :click="openNewTOSDialog"
        />
      </div>
    </div>

    <!-- Filters Control Bar (Theme Compatible) -->
    <filter-fields label="خيارات التصفية والبحث في جداول المواصفات" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Institution Type Selector (مدارس / جامعات / الكل) -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterInstitutionType"
            :items="institutionTypeOptions"
            item-title="text"
            item-value="value"
            class="mb-6"
            placeholder="نوع المؤسسة"
            prepend-inner-icon="mdi-domain"
            hide-details
            density="compact"
            variant="outlined"
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

        <!-- 🏫 School Filters -->
        <template v-if="filterInstitutionType === 'school'">
          <auto-list
            v-model="filterStage"
            name="Stage"
            placeholder="المرحلة الدراسية"
            cols="3"
            :add="false"
            @update:model-value="onStageChange"
          />
          <auto-list
            v-model="filterClassTrack"
            name="ClassTrackByStage"
            :param="filterStage"
            placeholder="الصف والمسار"
            cols="3"
            :add="false"
            :disabled="!filterStage"
            @update:model-value="onClassTrackChange"
          />
        </template>

        <!-- 🎓 University Filters -->
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
          <auto-list
            v-model="filterSemesterSubject"
            name="SemesterSubject"
            :param="filterSpecialization"
            placeholder="مقرر الفصل الجامعي"
            cols="3"
            :add="false"
            :disabled="!filterSpecialization"
            @update:model-value="filterSubject = null"
          />
        </template>

        <!-- 🏢 Institute Filters -->
        <template v-if="filterInstitutionType === 'institute'">
          <auto-list
            v-model="filterInstituteField"
            name="InstituteField"
            placeholder="المجال المهني"
            cols="3"
            :add="false"
            @update:model-value="() => { filterInstituteEducationSystem = null; filterInstituteSpecialization = null; filterInstituteCurriculum = null; filterInstituteSubject = null; }"
          />
          <auto-list
            v-model="filterInstituteEducationSystem"
            name="InstituteEducationSystem"
            :param="filterInstituteField"
            placeholder="نظام التعليم"
            cols="3"
            :add="false"
            :disabled="!filterInstituteField"
            @update:model-value="() => { filterInstituteSpecialization = null; filterInstituteCurriculum = null; filterInstituteSubject = null; }"
          />
          <auto-list
            v-model="filterInstituteSpecialization"
            name="InstituteSpecialization"
            :param="{ field: filterInstituteField, education_system: filterInstituteEducationSystem }"
            placeholder="التخصص المهني"
            cols="3"
            :add="false"
            :disabled="!filterInstituteEducationSystem"
            @update:model-value="() => { filterInstituteCurriculum = null; filterInstituteSubject = null; }"
          />
          <auto-list
            v-model="filterInstituteCurriculum"
            name="InstituteCurriculum"
            :param="filterInstituteSpecialization"
            placeholder="الخطة الدراسية"
            cols="3"
            :add="false"
            :disabled="!filterInstituteSpecialization"
            @update:model-value="filterInstituteSubject = null"
          />
          <auto-list
            v-model="filterInstituteSubject"
            name="InstituteSubject"
            :param="filterInstituteCurriculum"
            placeholder="المادة التدريبية"
            cols="3"
            :add="false"
            :disabled="!filterInstituteCurriculum"
            @update:model-value="loadTables"
          />
        </template>

        <!-- Subject Filter (Filtered by School or University) -->
        <auto-list
          v-if="filterInstitutionType !== 'institute'"
          v-model="filterSubject"
          name="Subject"
          :param="subjectFilterParam"
          :placeholder="subjectPlaceholder"
          :disabled="filterInstitutionType === 'all'"
          cols="3"
          :add="false"
        />

        <!-- Search Query -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="searchQuery"
            placeholder="بحث بالعنوان أو المادة..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Filter Actions -->
        <v-col cols="12" sm="12" md="6" class="d-flex align-center justify-end gap-2">
          <custom-btn
            type="show"
            label="تصفية الجداول"
            color="primary"
            class="font-weight-bold px-6 mb-6"
            :click="loadTables"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ الفلاتر"
            class="font-weight-bold mb-6"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Loading State -->
    <div v-if="loading" class="text-center pa-12">
      <v-progress-circular indeterminate color="primary" size="48" />
      <div class="text-caption mt-3 text-medium-emphasis">جاري جلب جداول المواصفات...</div>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredTables.length === 0" class="text-center pa-12 main-card rounded-2xl border mb-6">
      <v-icon size="56" color="primary" class="mb-3">mdi-table-network</v-icon>
      <h3 class="text-h6 font-weight-bold mb-1">لا توجد جداول مواصفات مسجلة</h3>
      <p class="text-caption text-medium-emphasis mb-4">
        قم بإنشاء جدول مواصفات لتوزيع أوزان الوحدات ومستويات بلوم المعرفية آلياً
      </p>
      <custom-btn
        type="add"
        label="إنشاء أول جدول مواصفات"
        color="primary"
        :click="openNewTOSDialog"
      />
    </div>

    <!-- Saved Tables Cards Grid -->
    <v-row v-else class="mb-6">
      <v-col v-for="tos in filteredTables" :key="tos.id" cols="12" md="6" lg="4">
        <v-card elevation="0" class="main-card pa-5 rounded-2xl border h-100 d-flex flex-column justify-space-between">
          <div>
            <div class="d-flex align-center justify-space-between mb-3">
              <v-chip color="primary" size="small" variant="tonal" class="font-weight-bold text-white">
                {{ tos.subject_name || `مادة #${tos.subject}` }}
              </v-chip>
              <v-chip size="small" color="secondary" variant="tonal" class="font-weight-bold">
                {{ tos.total_questions_count }} سؤالاً
              </v-chip>
            </div>

            <h3 class="text-subtitle-1 font-weight-black mb-2">{{ tos.name }}</h3>
            <p class="text-caption text-medium-emphasis mb-4">
              الدرجة الكلية: <strong>{{ tos.total_marks }}</strong> درجة • الوحدات المشمولة: <strong>{{ (tos.matrix_data || []).length }}</strong> وحدة
            </p>
          </div>

          <div class="d-flex align-center justify-end gap-2 pt-3 border-t">
            <custom-btn
              label="استعراض المخطط"
              icon="mdi-blueprint"
              color="indigo"
              variant="tonal"
              size="small"
              class="font-weight-bold"
              :click="() => viewBlueprint(tos)"
            />
            <custom-btn
              is-icon
              icon="pencil-outline"
              color="primary"
              variant="tonal"
              size="small"
              :click="() => editTOS(tos)"
            />
            <custom-btn
              is-icon
              icon="trash-can-outline"
              color="error"
              variant="tonal"
              size="small"
              :click="() => confirmDeleteTOS(tos)"
            />
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Create / Edit TOS Dialog (CustomDialog Component) -->
    <CustomDialog
      v-model="formDialog"
      width="980"
      :title="isEditing ? 'تعديل جدول المواصفات' : 'بناء جدول مواصفات جديد'"
      subTitle="توزيع الأوزان النسبية للوحدات ومستويات بلوم (%)"
    >
      <div class="mb-4">
        <v-btn-toggle
          v-model="formData.institution_type"
          mandatory
          color="primary"
          variant="outlined"
          density="compact"
          rounded="lg"
          class="w-100 d-flex"
          @update:model-value="onFormInstitutionTypeToggle"
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
            <v-icon start size="16">mdi-tools</v-icon>
            مهني / معاهد
          </v-btn>
        </v-btn-toggle>
      </div>

      <v-row class="mb-4">
        <v-col cols="12" md="6">
          <v-text-field
            v-model="formData.name"
            label="عنوان جدول المواصفات *"
            variant="outlined"
            density="compact"
            hide-details="auto"
            placeholder="مثال: جدول مواصفات الرياضيات - الفصل الأول"
          />
        </v-col>

        <!-- School Subject -->
        <v-col cols="12" md="6" v-if="formData.institution_type === 'school'">
          <auto-list
            v-model="formData.subject"
            name="Subject"
            :param="{ institution_type: 'school' }"
            placeholder="المادة الدراسية *"
            cols="12"
            :add="false"
            @update:model-value="onSubjectSelected"
          />
        </v-col>

        <!-- University Hierarchy -->
        <template v-if="formData.institution_type === 'university'">
          <v-col cols="12" md="6">
            <auto-list
              v-model="formCollege"
              name="College"
              placeholder="الكلية الجامعية"
              cols="12"
              :add="false"
              @update:model-value="formDepartment = null"
            />
          </v-col>
          <v-col cols="12" md="6">
            <auto-list
              v-model="formDepartment"
              name="DepartmentByCollege"
              :param="formCollege"
              placeholder="القسم الأكاديمي"
              cols="12"
              :add="false"
              :disabled="!formCollege"
              @update:model-value="formSpecialization = null"
            />
          </v-col>
          <v-col cols="12" md="6">
            <auto-list
              v-model="formSpecialization"
              name="Specialization"
              :param="formDepartment"
              placeholder="التخصص والبرنامج"
              cols="12"
              :add="false"
              :disabled="!formDepartment"
            />
          </v-col>
          <v-col cols="12" md="6">
            <auto-list
              v-model="formData.semesterSubject"
              name="SemesterSubject"
              :param="formSpecialization"
              placeholder="مقرر الفصل الجامعي *"
              cols="12"
              :add="false"
              @update:model-value="onSemesterSubjectSelected"
            />
          </v-col>
        </template>

        <!-- Institute Hierarchy -->
        <template v-if="formData.institution_type === 'institute'">
          <v-col cols="12" md="6">
            <auto-list
              v-model="formInstituteField"
              name="InstituteField"
              placeholder="المجال المهني"
              cols="12"
              :add="false"
              @update:model-value="() => { formInstituteEducationSystem = null; formInstituteSpecialization = null; formInstituteCurriculum = null; formData.instituteSubject = null; matrixRows = []; }"
            />
          </v-col>
          <v-col cols="12" md="6">
            <auto-list
              v-model="formInstituteEducationSystem"
              name="InstituteEducationSystem"
              :param="formInstituteField"
              placeholder="نظام التعليم"
              cols="12"
              :add="false"
              :disabled="!formInstituteField"
              @update:model-value="() => { formInstituteSpecialization = null; formInstituteCurriculum = null; formData.instituteSubject = null; matrixRows = []; }"
            />
          </v-col>
          <v-col cols="12" md="6">
            <auto-list
              v-model="formInstituteSpecialization"
              name="InstituteSpecialization"
              :param="{ field: formInstituteField, education_system: formInstituteEducationSystem }"
              placeholder="التخصص المهني"
              cols="12"
              :add="false"
              :disabled="!formInstituteEducationSystem"
              @update:model-value="() => { formInstituteCurriculum = null; formData.instituteSubject = null; matrixRows = []; }"
            />
          </v-col>
          <v-col cols="12" md="6">
            <auto-list
              v-model="formInstituteCurriculum"
              name="InstituteCurriculum"
              :param="formInstituteSpecialization"
              placeholder="الخطة الدراسية"
              cols="12"
              :add="false"
              :disabled="!formInstituteSpecialization"
              @update:model-value="() => { formData.instituteSubject = null; matrixRows = []; }"
            />
          </v-col>
          <v-col cols="12" md="6">
            <auto-list
              v-model="formData.instituteSubject"
              name="InstituteSubject"
              :param="formInstituteCurriculum"
              placeholder="المادة التدريبية للمعهد *"
              cols="12"
              :add="false"
              :disabled="!formInstituteCurriculum"
              @update:model-value="onInstituteSubjectSelected"
            />
          </v-col>
        </template>

        <v-col cols="12" md="6">
          <v-text-field
            v-model.number="formData.total_questions_count"
            type="number"
            label="إجمالي عدد الأسئلة المستهدف *"
            variant="outlined"
            density="compact"
            hide-details="auto"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model.number="formData.total_marks"
            type="number"
            label="الدرجة الكلية للاختبار *"
            variant="outlined"
            density="compact"
            hide-details="auto"
          />
        </v-col>
      </v-row>

      <!-- Matrix Grid Table -->
      <div v-if="matrixRows.length > 0" class="mt-4">
        <div class="d-flex align-center justify-space-between mb-2">
          <h4 class="text-subtitle-2 font-weight-bold">مصفوفة توزيع الأوزان النسبية للوحدات ومستويات بلوم (%)</h4>
          <v-chip :color="totalWeightSum === 100 ? 'success' : 'error'" variant="tonal" class="font-weight-bold text-white">
            إجمالي الوزن: {{ totalWeightSum }}% / 100%
          </v-chip>
        </div>

        <v-table class="border rounded-xl">
          <thead>
            <tr class="bg-slate-50 text-center">
              <th class="pa-3 text-right font-weight-bold" style="width: 220px">
                {{ formData.institution_type === 'university' ? 'مفردة / موضوع المقرر' : 'الوحدة الدراسية' }}
              </th>
              <th class="pa-3 font-weight-bold">تذكر</th>
              <th class="pa-3 font-weight-bold">فهم</th>
              <th class="pa-3 font-weight-bold">تطبيق</th>
              <th class="pa-3 font-weight-bold">تحليل</th>
              <th class="pa-3 font-weight-bold">تقييم</th>
              <th class="pa-3 font-weight-bold">ابتكار</th>
              <th class="pa-3 font-weight-bold bg-slate-100">
                {{ formData.institution_type === 'university' ? 'وزن المفردة (%)' : 'وزن الوحدة (%)' }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in matrixRows" :key="row.unit_id">
              <td class="pa-3 font-weight-bold">{{ row.unit_name }}</td>
              <td class="pa-1"><v-text-field v-model.number="row.weights.remember" type="number" density="compact" variant="outlined" hide-details class="text-center" /></td>
              <td class="pa-1"><v-text-field v-model.number="row.weights.understand" type="number" density="compact" variant="outlined" hide-details class="text-center" /></td>
              <td class="pa-1"><v-text-field v-model.number="row.weights.apply" type="number" density="compact" variant="outlined" hide-details class="text-center" /></td>
              <td class="pa-1"><v-text-field v-model.number="row.weights.analyze" type="number" density="compact" variant="outlined" hide-details class="text-center" /></td>
              <td class="pa-1"><v-text-field v-model.number="row.weights.evaluate" type="number" density="compact" variant="outlined" hide-details class="text-center" /></td>
              <td class="pa-1"><v-text-field v-model.number="row.weights.create" type="number" density="compact" variant="outlined" hide-details class="text-center" /></td>
              <td class="pa-3 text-center font-weight-bold bg-slate-100">
                {{ calculateRowTotal(row) }}%
              </td>
            </tr>
          </tbody>
        </v-table>
      </div>
      <div v-else-if="formData.subject" class="pa-6 text-center text-medium-emphasis">
        لا توجد وحدات دراسية مسجلة لهذه المادة
      </div>

      <template #actions>
        <custom-btn
          type="cancel"
          :click="() => formDialog = false"
          variant="text"
          label="إلغاء"
          class="font-weight-bold"
        />
        <custom-btn
          type="add"
          :click="saveTOS"
          :loading="saving"
          color="primary"
          :disabled="totalWeightSum !== 100 || !formData.name || (formData.institution_type === 'school' ? !formData.subject : (!formData.subject && !formData.semesterSubject))"
          label="حفظ جدول المواصفات"
          class="font-weight-bold ms-auto"
        />
      </template>
    </CustomDialog>

    <!-- Blueprint View Dialog (CustomDialog Component) -->
    <CustomDialog
      v-model="blueprintDialog"
      width="780"
      title="مخطط أعداد الأسئلة المستهدفة (Exam Blueprint)"
      :subTitle="selectedBlueprint ? `${selectedBlueprint.tos_name} • إجمالي الأسئلة: ${selectedBlueprint.total_questions}` : ''"
    >
      <div v-if="selectedBlueprint">
        <!-- Bloom Summary Totals -->
        <div v-if="selectedBlueprint.bloom_totals" class="d-flex flex-wrap gap-2 mb-4">
          <v-chip v-for="(cnt, bloom) in selectedBlueprint.bloom_totals" :key="bloom" color="indigo" variant="tonal" class="font-weight-bold">
            {{ bloom }}: {{ cnt }} أسئلة
          </v-chip>
        </div>

        <v-table class="border rounded-xl">
          <thead>
            <tr class="bg-slate-50">
              <th class="pa-3 font-weight-bold">الوحدة الدراسية</th>
              <th class="pa-3 font-weight-bold text-center">تذكر</th>
              <th class="pa-3 font-weight-bold text-center">فهم</th>
              <th class="pa-3 font-weight-bold text-center">تطبيق</th>
              <th class="pa-3 font-weight-bold text-center">تحليل</th>
              <th class="pa-3 font-weight-bold text-center">تقييم</th>
              <th class="pa-3 font-weight-bold text-center">ابتكار</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in selectedBlueprint.blueprint" :key="b.unit_id">
              <td class="pa-3 font-weight-bold">{{ b.unit_name }}</td>
              <td class="pa-3 text-center">{{ b.bloom_counts['remember'] || 0 }}</td>
              <td class="pa-3 text-center">{{ b.bloom_counts['understand'] || 0 }}</td>
              <td class="pa-3 text-center">{{ b.bloom_counts['apply'] || 0 }}</td>
              <td class="pa-3 text-center">{{ b.bloom_counts['analyze'] || 0 }}</td>
              <td class="pa-3 text-center">{{ b.bloom_counts['evaluate'] || 0 }}</td>
              <td class="pa-3 text-center">{{ b.bloom_counts['create'] || 0 }}</td>
            </tr>
          </tbody>
        </v-table>
      </div>

      <template #actions>
        <custom-btn
          type="cancel"
          :click="() => blueprintDialog = false"
          variant="text"
          label="إغلاق"
          class="font-weight-bold ms-auto"
        />
      </template>
    </CustomDialog>

    <!-- Delete Confirmation Modal (DeleteDialog Component) -->
    <DeleteDialog
      v-model="deleteDialog"
      title="حذف جدول المواصفات"
      :message="`هل أنت متأكد من حذف جدول المواصفات '${tosToDelete ? tosToDelete.name : ''}'؟`"
      @confirm-delete="executeDeleteTOS"
    />
  </div>
</template>

<script>
import shared from 'external-components'
import { examsService } from '@/services/examsService'
import { academicService } from '@/services/academicService'

export default {
  name: 'TableOfSpecificationsView',

  data() {
    return {
      loading: false,
      saving: false,
      tables: [],
      subjects: [],

      // Filters
      filterInstitutionType: 'school',
      institutionTypeOptions: [
        { text: "🏫 مدارس", value: "school" },
        { text: "🎓 جامعات", value: "university" },
        { text: "🏢 معاهد وتدريب مهني", value: "institute" },
        { text: "الكل (مدارس وجامعات ومعاهد)", value: "all" },
      ],
      filterCollege: null,
      filterDepartment: null,
      filterSpecialization: null,
      filterSemesterSubject: null,
      filterInstituteField: null,
      filterInstituteEducationSystem: null,
      filterInstituteSpecialization: null,
      filterInstituteCurriculum: null,
      filterInstituteSubject: null,
      filterStage: null,
      filterClassTrack: null,
      filterSubject: null,
      searchQuery: '',

      formDialog: false,
      blueprintDialog: false,
      deleteDialog: false,

      formCollege: null,
      formDepartment: null,
      formSpecialization: null,
      formInstituteField: null,
      formInstituteEducationSystem: null,
      formInstituteSpecialization: null,
      formInstituteCurriculum: null,

      selectedBlueprint: null,
      tosToDelete: null,
      isEditing: false,

      formData: {
        id: null,
        name: '',
        institution_type: 'school',
        subject: null,
        semesterSubject: null,
        instituteSubject: null,
        total_questions_count: 30,
        total_marks: 100.0,
      },

      matrixRows: [],
    }
  },

  computed: {
    filteredTables() {
      return this.tables
    },

    totalWeightSum() {
      return this.matrixRows.reduce((sum, row) => sum + this.calculateRowTotal(row), 0)
    },

    subjectFilterParam() {
      if (this.filterInstitutionType === 'school') {
        const p = { institution_type: 'school' }
        if (this.filterClassTrack) {
          p.class_track = this.filterClassTrack
        } else if (this.filterStage) {
          p.stage = this.filterStage
        }
        return p
      }
      if (this.filterInstitutionType === 'university') {
        const p = { institution_type: 'university' }
        if (this.filterSemesterSubject) {
          p.semester_subject = this.filterSemesterSubject
        } else if (this.filterSpecialization) {
          p.specialization = this.filterSpecialization
        } else if (this.filterDepartment) {
          p.department = this.filterDepartment
        } else if (this.filterCollege) {
          p.college = this.filterCollege
        }
        return p
      }
      return null
    },

    subjectPlaceholder() {
      if (this.filterInstitutionType === 'school') return 'المادة الدراسية'
      if (this.filterInstitutionType === 'university') return 'المقرر الجامعي'
      return 'يرجى تحديد نوع المؤسسة (مدارس أو جامعات) لتصفية المادة'
    },
  },

  methods: {
    calculateRowTotal(row) {
      const w = row.weights || {}
      return (
        (Number(w.remember) || 0) +
        (Number(w.understand) || 0) +
        (Number(w.apply) || 0) +
        (Number(w.analyze) || 0) +
        (Number(w.evaluate) || 0) +
        (Number(w.create) || 0)
      )
    },

    async loadTables() {
      this.loading = true
      try {
        const params = {}
        if (this.filterInstitutionType && this.filterInstitutionType !== 'all') params.institution_type = this.filterInstitutionType
        if (this.filterCollege) params.college = this.filterCollege
        if (this.filterDepartment) params.department = this.filterDepartment
        if (this.filterSpecialization) params.specialization = this.filterSpecialization
        if (this.filterSemesterSubject) params.semester_subject = this.filterSemesterSubject
        if (this.filterInstituteSubject) params.institute_subject = this.filterInstituteSubject
        if (this.filterInstituteField) params.institute_field = this.filterInstituteField
        if (this.filterStage) params.stage = this.filterStage
        if (this.filterClassTrack) params.class_track = this.filterClassTrack
        if (this.filterSubject) params.subject = this.filterSubject
        if (this.searchQuery) params.search = this.searchQuery
        const data = await examsService.getTablesOfSpecifications(params)
        this.tables = Array.isArray(data) ? data : (data.results || [])
      } catch (err) {
        console.error('Error loading TOS tables:', err)
      } finally {
        this.loading = false
      }
    },

    onInstitutionTypeChange() {
      this.filterStage = null
      this.filterClassTrack = null
      this.filterCollege = null
      this.filterDepartment = null
      this.filterSpecialization = null
      this.filterSemesterSubject = null
      this.filterInstituteField = null
      this.filterInstituteEducationSystem = null
      this.filterInstituteSpecialization = null
      this.filterInstituteCurriculum = null
      this.filterInstituteSubject = null
      this.filterSubject = null
      this.loadTables()
    },

    onStageChange() {
      this.filterClassTrack = null
      this.filterSubject = null
    },

    onClassTrackChange() {
      this.filterSubject = null
    },

    onCollegeChange() {
      this.filterDepartment = null
      this.filterSpecialization = null
      this.filterSemesterSubject = null
      this.filterSubject = null
    },

    onDepartmentChange() {
      this.filterSpecialization = null
      this.filterSemesterSubject = null
      this.filterSubject = null
    },

    onSpecializationChange() {
      this.filterSemesterSubject = null
      this.filterSubject = null
    },

    onFormInstitutionTypeToggle() {
      this.formData.subject = null
      this.formData.semesterSubject = null
      this.formData.instituteSubject = null
      this.formCollege = null
      this.formDepartment = null
      this.formSpecialization = null
      this.formInstituteField = null
      this.formInstituteEducationSystem = null
      this.formInstituteSpecialization = null
      this.formInstituteCurriculum = null
      this.matrixRows = []
    },

    resetFilters() {
      this.filterInstitutionType = 'school'
      this.filterCollege = null
      this.filterDepartment = null
      this.filterSpecialization = null
      this.filterSemesterSubject = null
      this.filterInstituteField = null
      this.filterInstituteEducationSystem = null
      this.filterInstituteSpecialization = null
      this.filterInstituteCurriculum = null
      this.filterInstituteSubject = null
      this.filterStage = null
      this.filterClassTrack = null
      this.filterSubject = null
      this.searchQuery = ''
      this.loadTables()
    },

    async loadSubjects() {
      try {
        const res = await academicService.getSubjects()
        this.subjects = (res.results || res || []).map(s => ({
          id: s.id,
          name: s.name_ar || s.name_en || s.name || `مادة #${s.id}`,
        }))
      } catch (err) {
        console.error('Error loading subjects:', err)
      }
    },

    async onSubjectSelected(subjectId) {
      if (!subjectId) {
        this.matrixRows = []
        return
      }
      try {
        const res = await academicService.getUnits({ subject_id: subjectId })
        const units = res.results || res || []
        this.matrixRows = units.map(u => ({
          unit_id: u.id,
          unit_name: u.name_ar || u.name_en || u.name || `وحدة #${u.id}`,
          weights: { remember: 0, understand: 0, apply: 0, analyze: 0, evaluate: 0, create: 0 },
        }))
      } catch (err) {
        console.error('Error loading units for TOS:', err)
      }
    },

    async onSemesterSubjectSelected(semSubjectId) {
      if (!semSubjectId) {
        this.matrixRows = []
        this.formData.subject = null
        return
      }
      try {
        const res = await academicService.getUnits({ semester_subject_id: semSubjectId })
        const units = res.results || res || []
        this.matrixRows = units.map(u => ({
          unit_id: u.id,
          unit_name: u.name_ar || u.name_en || u.name || `وحدة #${u.id}`,
          weights: { remember: 0, understand: 0, apply: 0, analyze: 0, evaluate: 0, create: 0 },
        }))

        try {
          const semSub = await shared.getData({ path: `api/academic/semester-subjects/${semSubjectId}/` })
          if (semSub && (semSub.fk_subject || semSub.fk_subject_id)) {
            this.formData.subject = semSub.fk_subject || semSub.fk_subject_id
          }
        } catch (_) {}
      } catch (err) {
        console.error('Error loading units for University TOS:', err)
      }
    },

    async onInstituteSubjectSelected(instSubjectId) {
      if (!instSubjectId) {
        this.matrixRows = []
        this.formData.subject = null
        this.formData.instituteSubject = null
        return
      }
      try {
        const res = await academicService.getUnits({ subject_id: instSubjectId })
        const units = res.results || res || []
        this.matrixRows = units.map(u => ({
          unit_id: u.id,
          unit_name: u.name_ar || u.name_en || u.name || `الوحدة #${u.id}`,
          weights: { remember: 0, understand: 0, apply: 0, analyze: 0, evaluate: 0, create: 0 },
        }))
        this.formData.subject = instSubjectId
        this.formData.instituteSubject = instSubjectId
      } catch (err) {
        console.error('Error loading units for Institute TOS:', err)
      }
    },

    openNewTOSDialog() {
      this.isEditing = false
      this.formData = { id: null, name: '', institution_type: 'school', subject: null, semesterSubject: null, instituteSubject: null, total_questions_count: 30, total_marks: 100.0 }
      this.formCollege = null
      this.formDepartment = null
      this.formSpecialization = null
      this.formInstituteField = null
      this.formInstituteEducationSystem = null
      this.formInstituteSpecialization = null
      this.formInstituteCurriculum = null
      this.matrixRows = []
      this.formDialog = true
    },

    editTOS(tos) {
      this.isEditing = true
      this.formData = {
        id: tos.id,
        name: tos.name,
        institution_type: tos.institution_type || 'school',
        subject: tos.subject,
        semesterSubject: tos.semester_subject,
        total_questions_count: tos.total_questions_count,
        total_marks: tos.total_marks,
      }
      this.matrixRows = JSON.parse(JSON.stringify(tos.matrix_data || []))
      this.formDialog = true
    },

    async saveTOS() {
      this.saving = true
      try {
        if (this.formData.institution_type === 'university' && !this.formData.subject && this.formData.semesterSubject) {
          try {
            const semSub = await shared.getData({ path: `api/academic/semester-subjects/${this.formData.semesterSubject}/` })
            if (semSub && (semSub.fk_subject || semSub.fk_subject_id)) {
              this.formData.subject = semSub.fk_subject || semSub.fk_subject_id
            }
          } catch (_) {}
        }

        const payload = {
          name: this.formData.name,
          institution_type: this.formData.institution_type,
          subject: this.formData.subject,
          total_questions_count: this.formData.total_questions_count,
          total_marks: this.formData.total_marks,
          matrix_data: this.matrixRows,
        }
        if (this.formData.institution_type === 'institute') {
          payload.institute_subject = this.formData.instituteSubject || this.formData.subject
        }
        if (this.isEditing && this.formData.id) {
          await examsService.updateTableOfSpecifications(this.formData.id, payload)
        } else {
          await examsService.createTableOfSpecifications(payload)
        }
        this.formDialog = false
        await this.loadTables()
      } catch (err) {
        console.error('Error saving TOS:', err)
      } finally {
        this.saving = false
      }
    },

    confirmDeleteTOS(tos) {
      this.tosToDelete = tos
      this.deleteDialog = true
    },

    async executeDeleteTOS() {
      if (!this.tosToDelete) return
      try {
        await examsService.deleteTableOfSpecifications(this.tosToDelete.id)
        this.deleteDialog = false
        this.tosToDelete = null
        await this.loadTables()
      } catch (err) {
        console.error('Error deleting TOS:', err)
      }
    },

    async viewBlueprint(tos) {
      try {
        const res = await examsService.getTOSBlueprint(tos.id)
        this.selectedBlueprint = res
        this.blueprintDialog = true
      } catch (err) {
        console.error('Error fetching TOS blueprint:', err)
      }
    },
  },

  mounted() {
    this.loadTables()
    this.loadSubjects()
  },
}
</script>

<style scoped>
.main-card {
  background: white;
  border-color: rgba(0, 0, 0, 0.08) !important;
}
</style>
