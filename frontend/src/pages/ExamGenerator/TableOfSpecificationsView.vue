<template>
  <div class="qb-tos-page-v4">
    <!-- Filters Control Bar (Theme Compatible) -->
    <filter-fields label="خيارات التصفية والبحث في جداول المواصفات" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Institution Type Selector (مدارس / جامعات / معاهد) -->
        <auto-list
          v-model="filterInstitutionType"
          name="LocalTextOption"
          :objects="institutionTypeOptions"
          cols="3"
          label="نوع المؤسسة التعليمية"
          icon="domain"
          :add="false"
          @update:model-value="onInstitutionTypeChange"
        />

        <!-- الظهور مشروط باختيار نوع المؤسسة: مدارس أو جامعات أو معاهد -->
        <template v-if="filterInstitutionType">
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
              :param="filterInstituteSpecParam"
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
            />
          </template>

          <!-- Subject Filter (Filtered by School or University) -->
          <auto-list
            v-if="filterInstitutionType === 'school'"
            v-model="filterSubject"
            name="SchoolSubject"
            :param="subjectFilterParam"
            :placeholder="subjectPlaceholder"
            cols="3"
            :add="false"
          />
          <auto-list
            v-else-if="filterInstitutionType === 'university'"
            v-model="filterSubject"
            name="Subject"
            :param="subjectFilterParam"
            :placeholder="subjectPlaceholder"
            cols="3"
            :add="false"
          />
        </template>

        <!-- Filter Actions -->
        <v-col cols="auto" class="d-flex align-center gap-2">
          <custom-btn
            type="show"
            label="عرض"
            color="primary"
            class="font-weight-bold px-6 mb-6"
            :click="applyFilters"
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

    <!-- Data Table View -->
    <div class="main-card rounded-2xl overflow-hidden mb-8">
      <custom-data-table
        ref="tableRef"
        v-bind="{
          items,
          getData,
          headers,
          delItem: url,
          create: openNewTOSDialog,
        }"
        :customLoading="loading"
        class="bg-transparent"
        :hasFilter="false"
        :log="false"
        :restore="false"
        :actionList="(item) => [
          { title_ar: 'استعراض المخطط', title_en: 'Preview Blueprint', click: () => viewBlueprint(item) },
          { title_ar: 'تعديل جدول المواصفات', title_en: 'Edit', click: () => editTOS(item) },
          { title_ar: 'حذف', title_en: 'Delete', click: () => confirmDeleteTOS(item) },
        ]"
      >
        <template v-slot:item-slot="{ item, key }">
          <template v-if="key === 'name'">
            <div class="font-weight-bold text-body-2 text-primary cursor-pointer" @click="viewBlueprint(item)">
              {{ item.name }}
            </div>
          </template>

          <template v-else-if="key === 'institution_type'">
            <span class="text-body-2 font-weight-medium">
              {{ item.institution_type_display || getInstitutionTypeLabel(item.institution_type) }}
            </span>
          </template>

          <template v-else-if="key === 'subject_name'">
            <v-chip color="primary" size="small" variant="tonal" class="font-weight-bold">
              {{ item.subject_name || `مادة #${item.subject}` }}
            </v-chip>
          </template>

          <template v-else-if="key === 'level_name'">
            <span class="text-body-2 text-medium-emphasis">{{ item.level_name || '-' }}</span>
          </template>

          <template v-else-if="key === 'total_questions_count'">
            <v-chip size="small" color="secondary" variant="tonal" class="font-weight-bold">
              {{ item.total_questions_count }} سؤالاً
            </v-chip>
          </template>

          <template v-else-if="key === 'total_marks'">
            <span class="text-body-2 font-weight-bold">{{ item.total_marks }} درجة</span>
          </template>

          <template v-else-if="key === 'units_count'">
            <span class="text-body-2">
              {{ item.units_count ?? (item.matrix_data || []).length }} وحدة
            </span>
          </template>

          <template v-else-if="key === 'is_active'">
            <v-chip
              size="x-small"
              :color="item.is_active ? 'success' : 'error'"
              variant="tonal"
              class="font-weight-bold"
            >
              {{ item.is_active ? 'نشط' : 'معطل' }}
            </v-chip>
          </template>
        </template>
      </custom-data-table>
    </div>

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

        <!-- School Hierarchy (Stage -> ClassTrack -> Subject) -->
        <template v-if="formData.institution_type === 'school'">
          <v-col cols="12" md="6">
            <auto-list
              v-model="formStage"
              name="Stage"
              placeholder="المرحلة الدراسية"
              cols="12"
              :add="false"
              @update:model-value="onFormStageChange"
            />
          </v-col>
          <v-col cols="12" md="6">
            <auto-list
              v-model="formClassTrack"
              name="ClassTrackByStage"
              :param="formStage"
              placeholder="الصف والمسار"
              cols="12"
              :add="false"
              :disabled="!formStage"
              @update:model-value="onFormClassTrackChange"
            />
          </v-col>
          <v-col cols="12" md="6">
            <auto-list
              v-model="formData.subject"
              name="SchoolSubject"
              :param="schoolSubjectParam"
              placeholder="المادة الدراسية *"
              cols="12"
              :add="false"
              @update:model-value="onSubjectSelected"
            />
          </v-col>
        </template>

        <!-- University Hierarchy -->
        <template v-if="formData.institution_type === 'university'">
          <v-col cols="12" md="6">
            <auto-list
              v-model="formCollege"
              name="College"
              placeholder="الكلية الجامعية"
              cols="12"
              :add="false"
              @update:model-value="() => { if (!isLoadingEdit) { formDepartment = null; formSpecialization = null; formData.semesterSubject = null; formData.subject = null; matrixRows = []; } }"
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
              @update:model-value="() => { if (!isLoadingEdit) { formSpecialization = null; formData.semesterSubject = null; formData.subject = null; matrixRows = []; } }"
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
              @update:model-value="() => { if (!isLoadingEdit) { formData.semesterSubject = null; formData.subject = null; matrixRows = []; } }"
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
              :param="formInstituteSpecParam"
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
      <div v-else-if="formData.subject || formData.semesterSubject || formData.instituteSubject" class="pa-6 text-center text-medium-emphasis">
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
      url: 'api/exams/table-of-specifications/',
      loading: false,
      saving: false,
      items: { results: [], pagination: {} },
      subjects: [],
      headers: [
        { title: 'عنوان جدول المواصفات', key: 'name', sortable: true },
        { title: 'نوع المؤسسة', key: 'institution_type', sortable: true },
        { title: 'المادة / المقرر', key: 'subject_name', sortable: false },
        { title: 'الصف / المستوى', key: 'level_name', sortable: false },
        { title: 'عدد الأسئلة', key: 'total_questions_count', sortable: true, align: 'center' },
        { title: 'الدرجة الكلية', key: 'total_marks', sortable: true, align: 'center' },
        { title: 'الوحدات', key: 'units_count', sortable: false, align: 'center' },
        { title: 'الحالة', key: 'is_active', sortable: true, align: 'center' },
      ],

      // Filters
      filterInstitutionType: null,
      institutionTypeOptions: [
        { text: "تعليم مدرسي", value: "school", icon: "mdi-school" },
        { text: "تعليم جامعي", value: "university", icon: "mdi-domain" },
        { text: "معاهد وتدريب مهني", value: "institute", icon: "mdi-tools" },
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

      formStage: null,
      formClassTrack: null,
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
      isLoadingEdit: false,

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
    totalWeightSum() {
      return this.matrixRows.reduce((sum, row) => sum + this.calculateRowTotal(row), 0)
    },

    subjectFilterParam() {
      if (this.filterInstitutionType === 'school') {
        const p = {}
        if (this.filterClassTrack) {
          p.class_track = this.filterClassTrack
        } else if (this.filterStage) {
          p.stage = this.filterStage
        }
        return Object.keys(p).length ? p : null
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

    filterInstituteSpecParam() {
      const p = {}
      if (this.filterInstituteField) p.field = this.filterInstituteField
      if (this.filterInstituteEducationSystem) p.education_system = this.filterInstituteEducationSystem
      return Object.keys(p).length ? p : null
    },

    schoolSubjectParam() {
      const p = {}
      if (this.formClassTrack) {
        p.class_track = this.formClassTrack
      } else if (this.formStage) {
        p.stage = this.formStage
      }
      return Object.keys(p).length ? p : null
    },

    formInstituteSpecParam() {
      const p = {}
      if (this.formInstituteField) p.field = this.formInstituteField
      if (this.formInstituteEducationSystem) p.education_system = this.formInstituteEducationSystem
      return Object.keys(p).length ? p : null
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

    getInstitutionTypeLabel(type) {
      const map = {
        school: 'تعليم مدرسي',
        university: 'تعليم جامعي',
        institute: 'معاهد وتدريب مهني',
      }
      return map[type] || type || '-'
    },

    async getData(tableParams = null) {
      this.loading = true
      try {
        const rawParams = tableParams?.params ? tableParams.params : (tableParams || {})
        const params = {
          page: rawParams.page || 1,
          page_size: rawParams.page_size || 10,
          hasPagination: true,
        }
        if (rawParams.sort_by) params.sort_by = rawParams.sort_by
        if (rawParams.search) params.search = rawParams.search
        else if (this.searchQuery) params.search = this.searchQuery

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

        const data = await examsService.getTablesOfSpecifications(params)
        if (data && Array.isArray(data.results)) {
          this.items = data
        } else if (Array.isArray(data)) {
          this.items = {
            results: data,
            pagination: { count: data.length, current_page: 1, num_pages: 1, page_size: data.length || 10 },
          }
        } else {
          this.items = { results: [], pagination: {} }
        }
        return this.items
      } catch (err) {
        console.error('Error loading TOS tables:', err)
        this.items = { results: [], pagination: {} }
      } finally {
        this.loading = false
      }
    },

    async reloadTable(resetPage = false) {
      if (this.$refs.tableRef) {
        if (resetPage && this.$refs.tableRef.params) {
          this.$refs.tableRef.params.page = 1
        }
        if (typeof this.$refs.tableRef.fetchData === 'function') {
          await this.$refs.tableRef.fetchData()
          return
        }
      }
      await this.getData()
    },

    applyFilters() {
      this.reloadTable(true)
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
      this.reloadTable(true)
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

    onFormStageChange() {
      this.formClassTrack = null
      this.formData.subject = null
      this.matrixRows = []
    },

    onFormClassTrackChange() {
      this.formData.subject = null
      this.matrixRows = []
    },

    onFormInstitutionTypeToggle() {
      this.formData.subject = null
      this.formData.semesterSubject = null
      this.formData.instituteSubject = null
      this.formStage = null
      this.formClassTrack = null
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
      this.filterInstitutionType = null
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
      this.reloadTable(true)
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
      if (this.isLoadingEdit) return
      if (!subjectId) {
        this.matrixRows = []
        return
      }
      try {
        let res
        if (this.formData.institution_type === 'school') {
          const params = { school_subject: subjectId }
          if (this.formClassTrack) params.class_track = this.formClassTrack
          else if (this.formStage) params.stage = this.formStage
          res = await academicService.getSchoolUnits(params)
        } else {
          res = await academicService.getUnits({ subject_id: subjectId })
        }
        const units = res?.results || res || []
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
      if (this.isLoadingEdit) return
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
      if (this.isLoadingEdit) return
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
      this.formStage = null
      this.formClassTrack = null
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

    async editTOS(tos) {
      this.isEditing = true
      this.isLoadingEdit = true
      const instType = tos.institution_type || 'school'

      // Reset parent params first so AutoList param watchers see oldVal=null when re-populating
      this.formStage = null
      this.formClassTrack = null
      this.formCollege = null
      this.formDepartment = null
      this.formSpecialization = null
      this.formInstituteField = null
      this.formInstituteEducationSystem = null
      this.formInstituteSpecialization = null
      this.formInstituteCurriculum = null

      this.formData = {
        id: tos.id,
        name: tos.name,
        institution_type: instType,
        subject: instType === 'school' ? (tos.school_subject_id || tos.subject) : tos.subject,
        semesterSubject: null,
        instituteSubject: null,
        total_questions_count: tos.total_questions_count,
        total_marks: tos.total_marks,
      }
      this.matrixRows = JSON.parse(JSON.stringify(tos.matrix_data || []))
      this.formDialog = true

      await this.$nextTick()

      if (instType === 'university') {
        this.formCollege = tos.college_id || null
        this.formDepartment = tos.department_id || null
        this.formSpecialization = tos.specialization_id || null
        await this.$nextTick()
        this.formData.semesterSubject = tos.semester_subject || null
      } else if (instType === 'school') {
        this.formStage = tos.stage_id || null
        this.formClassTrack = tos.class_track_id || null
        await this.$nextTick()
        this.formData.subject = tos.school_subject_id || tos.subject || null
      } else if (instType === 'institute') {
        this.formInstituteField = tos.institute_field_id || null
        this.formInstituteEducationSystem = tos.institute_education_system_id || null
        this.formInstituteSpecialization = tos.institute_specialization_id || null
        this.formInstituteCurriculum = tos.institute_curriculum_id || null
        await this.$nextTick()
        this.formData.instituteSubject = tos.institute_subject_id || tos.subject || null
      }

      this.isLoadingEdit = false
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
        if (this.formData.institution_type === 'school') {
          payload.school_subject = this.formData.subject
          if (this.formClassTrack) payload.class_track = this.formClassTrack
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
        await this.reloadTable()
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
        await this.reloadTable()
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
    this.getData()
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
