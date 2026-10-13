<template>
  <div class="students-master-view">
    <!-- Add / Edit Student Drawer -->
    <add-students v-model="drawer" :data="data" :getData="getData" />

    <!-- ── Page Header (Institutional OpenSoftCore Style) ─────────────── -->
    <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between gap-4 mb-6">
      <div class="d-flex align-center">
        <v-avatar size="46" color="primary" variant="tonal" class="me-3 rounded-xl elevation-1">
          <v-icon size="26">mdi-account-school-outline</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-black text-on-surface mb-0">سجل الطلاب المركزي</h1>
          <p class="text-caption text-medium-emphasis mb-0">
            إدارة وتتبع بيانات الطلاب والقيود الأكاديمية عبر كافة المؤسسات التعليمية (مدارس، جامعات، ومعاهد)
          </p>
        </div>
      </div>

      <div class="d-flex align-center gap-2 flex-wrap">
        <v-btn
          color="primary"
          variant="flat"
          rounded="lg"
          class="font-weight-bold shadow-sm"
          prepend-icon="mdi-account-plus-outline"
          @click="() => { data = {}; drawer = true; }"
        >
          إضافة طالب جديد
        </v-btn>
        <v-btn
          color="secondary"
          variant="tonal"
          rounded="lg"
          class="font-weight-bold"
          prepend-icon="mdi-refresh"
          :loading="loading"
          @click="getData"
        >
          تحديث السجلات
        </v-btn>
      </div>
    </div>

    <!-- ── KPI Summary Cards ─────────────────────────────────────────── -->
    <v-row class="mb-6" dense>
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card pa-4 rounded-2xl" elevation="0">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="text-caption font-weight-bold text-medium-emphasis">إجمالي الطلاب</span>
            <v-avatar color="primary" variant="tonal" size="36" rounded="lg">
              <v-icon size="20">mdi-account-group-outline</v-icon>
            </v-avatar>
          </div>
          <div class="text-h4 font-weight-black text-primary">{{ items.count || (items.results ? items.results.length : 0) }}</div>
          <div class="text-caption text-medium-emphasis mt-1">طالب مسجل في النظام الأكاديمي</div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card pa-4 rounded-2xl" elevation="0">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="text-caption font-weight-bold text-medium-emphasis">التعليم الجامعي</span>
            <v-avatar color="indigo" variant="tonal" size="36" rounded="lg">
              <v-icon size="20">mdi-domain</v-icon>
            </v-avatar>
          </div>
          <div class="text-h4 font-weight-black text-indigo">{{ statsCounts.university }}</div>
          <div class="text-caption text-medium-emphasis mt-1">كليات وأقسام وتخصصات أكاديمية</div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card pa-4 rounded-2xl" elevation="0">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="text-caption font-weight-bold text-medium-emphasis">التعليم المدرسي</span>
            <v-avatar color="teal" variant="tonal" size="36" rounded="lg">
              <v-icon size="20">mdi-school</v-icon>
            </v-avatar>
          </div>
          <div class="text-h4 font-weight-black text-teal">{{ statsCounts.school }}</div>
          <div class="text-caption text-medium-emphasis mt-1">مراحل ومسارات تعليم عام</div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card pa-4 rounded-2xl" elevation="0">
          <div class="d-flex align-center justify-space-between mb-2">
            <span class="text-caption font-weight-bold text-medium-emphasis">المعاهد والتدريب</span>
            <v-avatar color="amber-darken-3" variant="tonal" size="36" rounded="lg">
              <v-icon size="20">mdi-tools</v-icon>
            </v-avatar>
          </div>
          <div class="text-h4 font-weight-black text-amber-darken-3">{{ statsCounts.institute }}</div>
          <div class="text-caption text-medium-emphasis mt-1">تخصصات ودبلومات مهنية</div>
        </v-card>
      </v-col>
    </v-row>

    <!-- ── Comprehensive Filters Bar ── -->
    <filter-fields label="خيارات التصفية الأكاديمية والهرمية لسجلات الطلاب" class="main-card border-0 pa-5 rounded-2xl mb-6 elevation-1">
      <v-row dense class="align-center">
        <!-- 1. نوع المؤسسة التعليمية (مدارس / جامعات / معاهد / الكل) -->
        <v-col cols="12" md="12" class="mb-3">
          <v-btn-toggle
            v-model="filterInstitutionType"
            color="primary"
            variant="outlined"
            density="compact"
            rounded="lg"
            class="w-100 d-flex flex-wrap institutional-toggle"
            @update:model-value="onInstitutionTypeChange"
          >
            <v-btn value="all" class="flex-grow-1 font-weight-bold">
              <v-icon start size="16" color="primary">mdi-asterisk</v-icon>
              كافة المؤسسات (الكل)
            </v-btn>
            <v-btn value="university" class="flex-grow-1 font-weight-bold">
              <v-icon start size="16" color="indigo">mdi-domain</v-icon>
              الجامعات والكليات
            </v-btn>
            <v-btn value="school" class="flex-grow-1 font-weight-bold">
              <v-icon start size="16" color="teal">mdi-school</v-icon>
              مدارس التعليم العام
            </v-btn>
            <v-btn value="institute" class="flex-grow-1 font-weight-bold">
              <v-icon start size="16" color="amber-darken-3">mdi-tools</v-icon>
              المعاهد ومراكز التدريب
            </v-btn>
          </v-btn-toggle>
        </v-col>

        <!-- 2. المحافظة والمديرية والمؤسسة التعليمية -->
        <v-col cols="12" sm="6" md="4">
          <auto-list
            v-model="filterGovernorate"
            name="Governorate"
            placeholder="المحافظة"
            label="المحافظة"
            cols="12"
            :add="false"
            @update:model-value="onGovernorateChange"
          />
        </v-col>

        <v-col cols="12" sm="6" md="4">
          <auto-list
            v-model="filterDirectorate"
            name="Directorate"
            :param="filterGovernorate"
            :placeholder="filterGovernorate ? 'اختر المديرية التابعة' : 'اختر المحافظة أولاً'"
            label="المديرية"
            cols="12"
            :add="false"
            :disabled="!filterGovernorate"
            @update:model-value="onDirectorateChange"
          />
        </v-col>

        <v-col cols="12" sm="6" md="4">
          <auto-list
            v-model="filterOrganization"
            name="Organization"
            :param="orgParam"
            :placeholder="orgPlaceholder"
            label="المؤسسة التعليمية"
            cols="12"
            :add="false"
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- ── 4. التصنيف الأكاديمي التخصصي المشروط ── -->
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
              :placeholder="filterStage ? 'الصف والمسار' : 'اختر المرحلة أولاً'"
              label="الصف والمسار الدراسي"
              cols="12"
              :add="false"
              :disabled="!filterStage"
              @update:model-value="applyFilters"
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
              :placeholder="filterCollege ? 'القسم الأكاديمي' : 'اختر الكلية أولاً'"
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
              :param="filterDepartment || filterCollege"
              :placeholder="filterCollege ? 'التخصص والبرنامج' : 'اختر الكلية أو القسم أولاً'"
              label="التخصص والبرنامج"
              cols="12"
              :add="false"
              :disabled="!filterCollege && !filterDepartment"
              @update:model-value="applyFilters"
            />
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterEducationalLevel"
              name="EducationalLevels"
              placeholder="المستوى والدرجة الجامعية"
              label="المستوى والدرجة الجامعية"
              cols="12"
              :add="false"
              @update:model-value="applyFilters"
            />
          </v-col>
        </template>

        <!-- ج. فلاتر المعاهد -->
        <template v-if="filterInstitutionType === 'institute'">
          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterInstituteField"
              name="InstituteField"
              placeholder="المجال المهني / التقني"
              label="المجال المهني / التقني"
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
              placeholder="نظام التعليم والتدريب"
              label="نظام التعليم والتدريب"
              cols="12"
              :add="false"
              :disabled="!filterInstituteField"
              @update:model-value="applyFilters"
            />
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterInstituteSpecialization"
              name="InstituteSpecialization"
              :param="filterInstituteEducationSystem || filterInstituteField"
              :placeholder="filterInstituteField ? 'التخصص المهني' : 'اختر المجال أولاً'"
              label="التخصص المهني"
              cols="12"
              :add="false"
              :disabled="!filterInstituteField"
              @update:model-value="applyFilters"
            />
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <auto-list
              v-model="filterInstituteLevel"
              name="InstituteLevel"
              placeholder="المستوى التدريبي"
              label="المستوى التدريبي"
              cols="12"
              :add="false"
              @update:model-value="applyFilters"
            />
          </v-col>
        </template>

        <!-- 5. الجنس وحالة التفعيل وأزرار التحكم -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterGender"
            :items="genderOptions"
            item-title="text"
            item-value="value"
            placeholder="الجنس"
            label="الجنس"
            prepend-inner-icon="mdi-gender-male-female"
            clearable
            density="compact"
            variant="outlined"
            class="mb-3"
            hide-details
            @update:model-value="applyFilters"
          />
        </v-col>

        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterActive"
            :items="activeOptions"
            item-title="text"
            item-value="value"
            placeholder="حالة التفعيل"
            label="الحالة"
            prepend-inner-icon="mdi-check-circle-outline"
            clearable
            density="compact"
            variant="outlined"
            class="mb-3"
            hide-details
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- أزرار الإجراءات -->
        <v-col cols="12" sm="12" md="3" class="d-flex align-center justify-end gap-2 mb-3">
          <custom-btn
            type="show"
            label="تصفية النتائج"
            color="primary"
            icon="mdi-filter"
            class="font-weight-bold px-5"
            :click="applyFilters"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ الفلاتر"
            icon="mdi-filter-off"
            class="font-weight-bold"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- ── Data Table ── -->
    <custom-data-table
      v-bind="{
        items,
        getData,
        headers,
        delItem: url,
        editItem,
        create: () => { data = {}; drawer = true; },
      }"
      :hasFilter="false"
      :log="false"
      :restore="false"
    >
      <template v-slot:item-slot="{ item, key }">
        <!-- 1. الرقم الأكاديمي -->
        <template v-if="key === 'academic_number'">
          <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold font-mono" v-if="item.academic_number">
            <v-icon start size="14">mdi-card-account-details-outline</v-icon>
            {{ item.academic_number }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- 2. اسم الطالب مع الصورة الرمزية -->
        <template v-else-if="key === 'name_ar'">
          <div class="d-flex align-center gap-3 py-1">
            <v-avatar size="34" :color="item.gender === 2 ? 'pink' : 'primary'" variant="tonal" class="rounded-lg">
              <v-icon size="18">{{ item.gender === 2 ? 'mdi-account-heart-outline' : 'mdi-account-outline' }}</v-icon>
            </v-avatar>
            <div>
              <div class="font-weight-bold text-body-2 text-on-surface">{{ item.name_ar }}</div>
              <div class="text-caption text-medium-emphasis font-mono" v-if="item.name_en">{{ item.name_en }}</div>
            </div>
          </div>
        </template>

        <!-- 3. نوع المؤسسة -->
        <template v-else-if="key === 'institution_type'">
          <v-chip
            v-if="item.institution_type === 'university'"
            size="small"
            color="indigo"
            variant="tonal"
            class="font-weight-bold"
          >
            <v-icon start size="14">mdi-domain</v-icon>
            جامعي
          </v-chip>
          <v-chip
            v-else-if="item.institution_type === 'institute'"
            size="small"
            color="amber-darken-3"
            variant="tonal"
            class="font-weight-bold"
          >
            <v-icon start size="14">mdi-tools</v-icon>
            معهد مهني
          </v-chip>
          <v-chip
            v-else
            size="small"
            color="teal"
            variant="tonal"
            class="font-weight-bold"
          >
            <v-icon start size="14">mdi-school</v-icon>
            مدرسي
          </v-chip>
        </template>

        <!-- 4. المؤسسة التعليمية -->
        <template v-else-if="key === 'organization_name'">
          <span class="text-body-2 font-weight-bold text-truncate" style="max-width: 220px;" v-if="item.organization_name">
            <v-icon size="14" class="me-1 text-medium-emphasis">mdi-office-building</v-icon>
            {{ item.organization_name }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- 5. الارتباط والتصنيف الأكاديمي -->
        <template v-else-if="key === 'academic_info'">
          <div class="d-flex align-center gap-1" v-if="item.academic_info">
            <v-chip size="x-small" variant="outlined" color="primary" class="font-weight-medium">
              {{ item.academic_info }}
            </v-chip>
          </div>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- 6. الجنس -->
        <template v-else-if="key === 'gender_display'">
          <v-chip
            size="small"
            :color="item.gender === 1 ? 'blue' : 'pink'"
            variant="tonal"
            class="font-weight-bold"
          >
            <v-icon start size="14">{{ item.gender === 1 ? 'mdi-gender-male' : 'mdi-gender-female' }}</v-icon>
            {{ item.gender_display || (item.gender === 1 ? 'ذكر' : 'أنثى') }}
          </v-chip>
        </template>

        <!-- 7. المديرية -->
        <template v-else-if="key === 'directorate_name'">
          <span class="text-body-2" v-if="item.directorate_name">
            <v-icon size="14" class="me-1 text-medium-emphasis">mdi-map-marker-outline</v-icon>
            {{ item.directorate_name }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- 8. الهاتف -->
        <template v-else-if="key === 'phone_number'">
          <span class="text-body-2 font-weight-medium font-mono" dir="ltr" v-if="item.phone_number">
            <v-icon size="14" class="me-1 text-medium-emphasis">mdi-phone-outline</v-icon>
            {{ item.phone_number }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- 9. الحالة -->
        <template v-else-if="key === 'is_active'">
          <v-chip
            size="small"
            :color="item.is_active ? 'success' : 'error'"
            variant="tonal"
            class="font-weight-bold"
          >
            <v-icon start size="14">{{ item.is_active ? 'mdi-check-circle' : 'mdi-close-circle' }}</v-icon>
            {{ item.is_active ? 'مفعل' : 'معطل' }}
          </v-chip>
        </template>
      </template>
    </custom-data-table>
  </div>
</template>

<script>
import AddStudents from './AddStudents.vue';

export default {
  name: 'StudentsView',
  components: {
    AddStudents,
  },
  data() {
    return {
      data: {},
      items: { count: 0, results: [] },
      drawer: false,
      loading: false,
      url: "api/academic/students/",

      // ── إحصائيات سريعة للبطاقات ──
      statsCounts: {
        university: 0,
        school: 0,
        institute: 0,
      },

      // ── فلاتر الهيكلية والمؤسسة ──
      filterInstitutionType: 'all',
      filterGovernorate: null,
      filterDirectorate: null,
      filterOrganization: null,
      filterGender: null,
      filterActive: null,

      // ── فلاتر المدارس ──
      filterStage: null,
      filterClassTrack: null,

      // ── فلاتر الجامعات ──
      filterCollege: null,
      filterDepartment: null,
      filterSpecialization: null,
      filterEducationalLevel: null,

      // ── فلاتر المعاهد ──
      filterInstituteField: null,
      filterInstituteEducationSystem: null,
      filterInstituteSpecialization: null,
      filterInstituteLevel: null,

      genderOptions: [
        { text: "الكل", value: null },
        { text: "ذكور فقط", value: 1 },
        { text: "إناث فقط", value: 2 },
      ],
      activeOptions: [
        { text: "الكل", value: null },
        { text: "مفعل فقط", value: true },
        { text: "معطل فقط", value: false },
      ],
    };
  },
  computed: {
    orgPlaceholder() {
      if (this.filterInstitutionType === 'university') return 'الكلية / الجامعة';
      if (this.filterInstitutionType === 'institute') return 'المعهد / المركز التدريبي';
      if (this.filterInstitutionType === 'school') return 'المدرسة';
      return 'المؤسسة التعليمية (الكل)';
    },
    orgParam() {
      return {
        institution_type: (this.filterInstitutionType && this.filterInstitutionType !== 'all') ? this.filterInstitutionType : undefined,
        governorate: this.filterGovernorate || undefined,
        directorate: this.filterDirectorate || undefined,
      };
    },
    headers() {
      return [
        { title: "الرقم الأكاديمي", key: "academic_number" },
        { title: "اسم الطالب", key: "name_ar" },
        { title: "نوع المؤسسة", key: "institution_type" },
        { title: "المؤسسة التعليمية", key: "organization_name" },
        { title: "القيد والتصنيف الأكاديمي", key: "academic_info" },
        { title: "الجنس", key: "gender_display" },
        { title: "المديرية", key: "directorate_name" },
        { title: "الهاتف", key: "phone_number" },
        { title: "الحالة", key: "is_active" },
      ];
    },
  },
  created() {
    this.getData();
    this.fetchSummaryStats();
  },
  methods: {
    async fetchSummaryStats() {
      try {
        const res = await this.$axios.get(this.url, { params: { page_size: 100 } });
        const list = res.data?.results || [];
        this.statsCounts = {
          university: list.filter(s => s.institution_type === 'university').length,
          school: list.filter(s => s.institution_type === 'school').length,
          institute: list.filter(s => s.institution_type === 'institute').length,
        };
      } catch (err) {
        console.error('Error fetching students stats:', err);
      }
    },

    async getData(params = this.$params) {
      this.loading = true;
      const queryParams = {
        ...(params?.params || params || {}),
      };

      if (this.filterInstitutionType && this.filterInstitutionType !== 'all') {
        queryParams.institution_type = this.filterInstitutionType;
      }
      if (this.filterGovernorate) queryParams.governorate = this.filterGovernorate;
      if (this.filterDirectorate) queryParams.directorate = this.filterDirectorate;
      if (this.filterOrganization) queryParams.organization = this.filterOrganization;
      if (this.filterGender) queryParams.gender = this.filterGender;
      if (this.filterActive !== null && this.filterActive !== undefined) queryParams.is_active = this.filterActive;

      // School params
      if (this.filterInstitutionType === 'school') {
        if (this.filterStage) queryParams.stage = this.filterStage;
        if (this.filterClassTrack) queryParams.class_track = this.filterClassTrack;
      }

      // University params
      if (this.filterInstitutionType === 'university') {
        if (this.filterCollege) queryParams.college = this.filterCollege;
        if (this.filterDepartment) queryParams.department = this.filterDepartment;
        if (this.filterSpecialization) queryParams.specialization = this.filterSpecialization;
        if (this.filterEducationalLevel) queryParams.educational_level = this.filterEducationalLevel;
      }

      // Institute params
      if (this.filterInstitutionType === 'institute') {
        if (this.filterInstituteField) queryParams.institute_field = this.filterInstituteField;
        if (this.filterInstituteEducationSystem) queryParams.institute_education_system = this.filterInstituteEducationSystem;
        if (this.filterInstituteSpecialization) queryParams.institute_specialization = this.filterInstituteSpecialization;
        if (this.filterInstituteLevel) queryParams.institute_level = this.filterInstituteLevel;
      }

      try {
        const response = await this.$axios.get(this.url, { params: queryParams });
        this.items = response.data;
      } catch (err) {
        this.items = { count: 0, results: [] };
      } finally {
        this.loading = false;
      }
    },

    onInstitutionTypeChange() {
      this.filterOrganization = null;
      this.filterStage = null;
      this.filterClassTrack = null;
      this.filterCollege = null;
      this.filterDepartment = null;
      this.filterSpecialization = null;
      this.filterEducationalLevel = null;
      this.filterInstituteField = null;
      this.filterInstituteEducationSystem = null;
      this.filterInstituteSpecialization = null;
      this.filterInstituteLevel = null;
      this.getData();
    },

    onGovernorateChange(val) {
      this.filterGovernorate = val;
      this.filterDirectorate = null;
      this.filterOrganization = null;
      this.getData();
    },

    onDirectorateChange(val) {
      this.filterDirectorate = val;
      this.filterOrganization = null;
      this.getData();
    },

    onStageChange(val) {
      this.filterStage = val;
      this.filterClassTrack = null;
      this.getData();
    },

    onCollegeChange(val) {
      this.filterCollege = val;
      this.filterDepartment = null;
      this.filterSpecialization = null;
      this.getData();
    },

    onDepartmentChange(val) {
      this.filterDepartment = val;
      this.filterSpecialization = null;
      this.getData();
    },

    onInstituteFieldChange(val) {
      this.filterInstituteField = val;
      this.filterInstituteEducationSystem = null;
      this.filterInstituteSpecialization = null;
      this.getData();
    },

    applyFilters() {
      this.getData();
    },

    resetFilters() {
      this.filterInstitutionType = 'all';
      this.filterGovernorate = null;
      this.filterDirectorate = null;
      this.filterOrganization = null;
      this.filterGender = null;
      this.filterActive = null;

      this.filterStage = null;
      this.filterClassTrack = null;
      this.filterCollege = null;
      this.filterDepartment = null;
      this.filterSpecialization = null;
      this.filterEducationalLevel = null;
      this.filterInstituteField = null;
      this.filterInstituteEducationSystem = null;
      this.filterInstituteSpecialization = null;
      this.filterInstituteLevel = null;

      this.getData();
    },

    editItem(itemData) {
      this.data = { ...itemData };
      this.drawer = true;
    },
  },
};
</script>

<style scoped>
.students-master-view {
  animation: fadeIn 0.3s ease-in-out;
  padding: 16px;
}

/* ===== Stat Cards ===== */
.stat-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
}

.main-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
}

.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
