<template>
  <drawer
    :data="data"
    :getData="getData"
    click="api/academic/students/"
    :items="items"
    width="950"
  >
    <template v-slot>
      <div class="pa-2">
        <!-- ── محدد نوع المؤسسة التعليمية للطالب ── -->
        <v-card variant="outlined" rounded="xl" class="pa-4 mb-5 border-dashed" color="primary">
          <div class="text-caption font-weight-bold text-medium-emphasis mb-2 d-flex align-center gap-1">
            <v-icon size="16" color="primary">mdi-office-building-cog</v-icon>
            نوع المؤسسة التعليمية التي ينتمي إليها الطالب:
          </div>
          <v-btn-toggle
            v-model="studentType"
            mandatory
            color="primary"
            variant="flat"
            density="compact"
            rounded="lg"
            class="w-100 d-flex"
            @update:model-value="onStudentTypeChange"
          >
            <v-btn value="school" class="flex-grow-1 font-weight-bold py-2">
              <v-icon start size="18">mdi-school</v-icon>
              تعليم مدرسي
            </v-btn>
            <v-btn value="university" class="flex-grow-1 font-weight-bold py-2">
              <v-icon start size="18">mdi-domain</v-icon>
              تعليم جامعي
            </v-btn>
            <v-btn value="institute" class="flex-grow-1 font-weight-bold py-2">
              <v-icon start size="18">mdi-tools</v-icon>
              معاهد وتدريب مهني
            </v-btn>
          </v-btn-toggle>
        </v-card>

        <!-- ── 1. البيانات الشخصية والأساسية ── -->
        <div class="d-flex align-center gap-2 mb-3">
          <v-icon size="20" color="primary">mdi-account-details-outline</v-icon>
          <span class="text-subtitle-1 font-weight-bold">البيانات الأساسية والشخصية للطالب</span>
        </div>

        <v-row dense class="mb-4">
          <!-- الرقم الأكاديمي -->
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="data.academic_number"
              label="الرقم الأكاديمي / رقم القيد *"
              placeholder="مثال: 20261001"
              prepend-inner-icon="mdi-card-account-details-outline"
              density="compact"
              variant="outlined"
              type="number"
              hide-details="auto"
              :rules="[v => !!v || 'الرقم الأكاديمي مطلوب']"
            />
          </v-col>

          <!-- الاسم بالعربي -->
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="data.name_ar"
              label="اسم الطالب كاملاً (عربي) *"
              placeholder="الاسم الرباعي أو الثلاثي"
              prepend-inner-icon="mdi-format-title"
              density="compact"
              variant="outlined"
              hide-details="auto"
              :rules="[v => !!v || 'الاسم بالعربي مطلوب']"
            />
          </v-col>

          <!-- الاسم بالإنجليزي -->
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="data.name_en"
              label="اسم الطالب (إنجليزي)"
              placeholder="Full Name in English"
              prepend-inner-icon="mdi-alphabetical"
              density="compact"
              variant="outlined"
              hide-details
            />
          </v-col>

          <!-- الجنس -->
          <v-col cols="12" sm="6" md="4">
            <v-select
              v-model="data.gender"
              :items="genderChoices"
              item-title="text"
              item-value="value"
              label="الجنس *"
              prepend-inner-icon="mdi-gender-male-female"
              density="compact"
              variant="outlined"
              hide-details
            />
          </v-col>

          <!-- تاريخ الميلاد -->
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="data.birthdate"
              label="تاريخ الميلاد"
              prepend-inner-icon="mdi-calendar"
              density="compact"
              variant="outlined"
              type="date"
              hide-details
            />
          </v-col>

          <!-- مكان الميلاد -->
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="data.birth_place"
              label="مكان الميلاد"
              placeholder="المدينة / المحافظة"
              prepend-inner-icon="mdi-map-marker-outline"
              density="compact"
              variant="outlined"
              hide-details
            />
          </v-col>

          <!-- الدولة / الجنسية -->
          <v-col cols="12" sm="6" md="4">
            <auto-list
              v-model="data.country"
              name="Country"
              placeholder="الجنسية / الدولة"
              label="الدولة / الجنسية"
              cols="12"
              :add="false"
            />
          </v-col>

          <!-- رقم الهاتف -->
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="data.phone_number"
              label="رقم الهاتف / الجوال"
              placeholder="05XXXXXXXX"
              prepend-inner-icon="mdi-phone-outline"
              density="compact"
              variant="outlined"
              dir="ltr"
              hide-details
            />
          </v-col>

          <!-- العنوان -->
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="data.address"
              label="العنوان ومحل السكن"
              placeholder="المدينة - الحي"
              prepend-inner-icon="mdi-home-outline"
              density="compact"
              variant="outlined"
              hide-details
            />
          </v-col>
        </v-row>

        <v-divider class="my-4" />

        <!-- ── 2. التبعية المؤسسية والإقليمية ── -->
        <div class="d-flex align-center gap-2 mb-3">
          <v-icon size="20" color="primary">mdi-domain</v-icon>
          <span class="text-subtitle-1 font-weight-bold">المؤسسة التعليمية والهيكل الإداري</span>
        </div>

        <v-row dense class="mb-4">
          <!-- المحافظة -->
          <v-col cols="12" sm="6" md="4">
            <auto-list
              v-model="selectedGovernorate"
              name="Governorate"
              placeholder="اختر المحافظة"
              label="المحافظة"
              cols="12"
              :add="false"
              @update:model-value="onGovernorateChange"
            />
          </v-col>

          <!-- المديرية -->
          <v-col cols="12" sm="6" md="4">
            <auto-list
              v-model="data.directorate"
              name="Directorate"
              :param="selectedGovernorate"
              :placeholder="selectedGovernorate ? 'اختر المديرية التابعة' : 'اختر المحافظة أولاً'"
              label="المديرية"
              cols="12"
              :add="false"
              :disabled="!selectedGovernorate"
            />
          </v-col>

          <!-- المؤسسة التعليمية (مدرسة / كلية / معهد) -->
          <v-col cols="12" sm="6" md="4">
            <auto-list
              v-model="data.organization"
              name="Organization"
              :param="organizationParam"
              :placeholder="orgFieldLabel"
              :label="orgFieldLabel"
              cols="12"
              :add="false"
            />
          </v-col>
        </v-row>

        <v-divider class="my-4" />

        <!-- ── 3. القيد والتصنيف الأكاديمي (مشروط بنوع المؤسسة) ── -->
        <!-- أ. في حال المدارس -->
        <template v-if="studentType === 'school'">
          <div class="d-flex align-center gap-2 mb-3">
            <v-icon size="20" color="teal">mdi-school</v-icon>
            <span class="text-subtitle-1 font-weight-bold text-teal">القيد والتصنيف الأكاديمي (التعليم المدرسي)</span>
          </div>

          <v-row dense class="mb-4">
            <v-col cols="12" sm="6" md="6">
              <auto-list
                v-model="selectedStage"
                name="Stage"
                placeholder="اختر المرحلة الدراسية"
                label="المرحلة الدراسية"
                cols="12"
                :add="false"
                @update:model-value="data.class_track = null"
              />
            </v-col>

            <v-col cols="12" sm="6" md="6">
              <auto-list
                v-model="data.class_track"
                name="ClassTrackByStage"
                :param="selectedStage"
                :placeholder="selectedStage ? 'اختر الصف والمسار' : 'اختر المرحلة أولاً'"
                label="الصف والمسار الدراسي *"
                cols="12"
                :add="false"
                :disabled="!selectedStage"
              />
            </v-col>
          </v-row>
        </template>

        <!-- ب. في حال الجامعات -->
        <template v-if="studentType === 'university'">
          <div class="d-flex align-center gap-2 mb-3">
            <v-icon size="20" color="indigo">mdi-domain</v-icon>
            <span class="text-subtitle-1 font-weight-bold text-indigo">القيد والتصنيف الأكاديمي (التعليم الجامعي)</span>
          </div>

          <v-row dense class="mb-4">
            <!-- الكلية -->
            <v-col cols="12" sm="6" md="6">
              <auto-list
                v-model="data.university_college"
                name="College"
                placeholder="اختر الكلية الجامعية"
                label="الكلية الجامعية *"
                cols="12"
                :add="false"
                @update:model-value="onCollegeChange"
              />
            </v-col>

            <!-- القسم الأكاديمي -->
            <v-col cols="12" sm="6" md="6">
              <auto-list
                v-model="data.university_department"
                name="DepartmentByCollege"
                :param="data.university_college"
                :placeholder="data.university_college ? 'اختر القسم الأكاديمي' : 'اختر الكلية أولاً'"
                label="القسم الأكاديمي"
                cols="12"
                :add="false"
                :disabled="!data.university_college"
                @update:model-value="data.university_specialization = null"
              />
            </v-col>

            <!-- التخصص والبرنامج -->
            <v-col cols="12" sm="6" md="6">
              <auto-list
                v-model="data.university_specialization"
                name="Specialization"
                :param="data.university_department || data.university_college"
                :placeholder="data.university_department ? 'اختر التخصص والبرنامج' : 'اختر القسم أو الكلية أولاً'"
                label="التخصص والبرنامج الجامعي *"
                cols="12"
                :add="false"
                :disabled="!data.university_department && !data.university_college"
              />
            </v-col>

            <!-- المستوى الجامعي -->
            <v-col cols="12" sm="6" md="6">
              <auto-list
                v-model="data.university_level"
                name="EducationalLevels"
                placeholder="اختر المستوى الدراسي (السنة الأولى، الثانية...)"
                label="المستوى والدرجة الجامعية"
                cols="12"
                :add="false"
              />
            </v-col>
          </v-row>
        </template>

        <!-- ج. في حال المعاهد -->
        <template v-if="studentType === 'institute'">
          <div class="d-flex align-center gap-2 mb-3">
            <v-icon size="20" color="amber-darken-3">mdi-tools</v-icon>
            <span class="text-subtitle-1 font-weight-bold text-amber-darken-3">القيد والتصنيف الأكاديمي (المعاهد والتدريب المهني)</span>
          </div>

          <v-row dense class="mb-4">
            <!-- المجال المهني -->
            <v-col cols="12" sm="6" md="6">
              <auto-list
                v-model="data.institute_field"
                name="InstituteField"
                placeholder="اختر المجال المهني / التقني"
                label="المجال المهني / التقني *"
                cols="12"
                :add="false"
                @update:model-value="onInstituteFieldChange"
              />
            </v-col>

            <!-- نظام التعليم والتدريب -->
            <v-col cols="12" sm="6" md="6">
              <auto-list
                v-model="data.institute_education_system"
                name="InstituteEducationSystem"
                :param="data.institute_field"
                :placeholder="data.institute_field ? 'اختر نظام التعليم' : 'اختر المجال أولاً'"
                label="نظام التعليم والتدريب"
                cols="12"
                :add="false"
                :disabled="!data.institute_field"
              />
            </v-col>

            <!-- التخصص المهني -->
            <v-col cols="12" sm="6" md="6">
              <auto-list
                v-model="data.institute_specialization"
                name="InstituteSpecialization"
                :param="data.institute_education_system || data.institute_field"
                :placeholder="data.institute_field ? 'اختر التخصص المهني' : 'اختر المجال أولاً'"
                label="التخصص المهني / التقني *"
                cols="12"
                :add="false"
                :disabled="!data.institute_field"
              />
            </v-col>

            <!-- المستوى التدريبي -->
            <v-col cols="12" sm="6" md="6">
              <auto-list
                v-model="data.institute_level"
                name="InstituteLevel"
                placeholder="اختر المستوى التدريبي للمعهد"
                label="المستوى التدريبي للمعهد"
                cols="12"
                :add="false"
              />
            </v-col>
          </v-row>
        </template>

        <v-divider class="my-4" />

        <!-- ── 4. حالة التفعيل ── -->
        <v-row dense class="align-center">
          <v-col cols="12" sm="6">
            <v-switch
              v-model="data.is_active"
              color="success"
              label="تفعيل سجل الطالب في النظام"
              hide-details
              density="compact"
            />
          </v-col>
        </v-row>
      </div>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddStudents',
  props: {
    data: {
      type: Object,
      default: () => ({}),
    },
    items: [Array, Object],
    getData: Function,
  },
  data() {
    return {
      studentType: 'school',
      selectedGovernorate: null,
      selectedStage: null,
      genderChoices: [
        { text: 'ذكر', value: 1 },
        { text: 'أنثى', value: 2 },
      ],
    };
  },
  computed: {
    orgFieldLabel() {
      if (this.studentType === 'university') return 'الكلية / الجامعة التابعة لها';
      if (this.studentType === 'institute') return 'المعهد / المركز المهني التابع له';
      return 'المدرسة التابع لها';
    },
    organizationParam() {
      return {
        institution_type: this.studentType,
        governorate: this.selectedGovernorate || undefined,
        directorate: this.data.directorate || undefined,
      };
    },
  },
  watch: {
    data: {
      immediate: true,
      handler(val) {
        if (!val) return;
        // تعيين الحالة الافتراضية للنشاط إذا كانت غير محددة
        if (val.is_active === undefined) {
          val.is_active = true;
        }
        if (val.gender === undefined) {
          val.gender = 1;
        }

        // كشف نوع المؤسسة تلقائياً عند التعديل
        if (val.university_college || val.university_specialization) {
          this.studentType = 'university';
        } else if (val.institute_field || val.institute_specialization) {
          this.studentType = 'institute';
        } else if (val.class_track) {
          this.studentType = 'school';
        } else if (val.institution_type) {
          this.studentType = val.institution_type;
        }

        // استخراج المحافظة من السجل إذا كانت متوفرة
        if (val.governorate_id) {
          this.selectedGovernorate = val.governorate_id;
        }
      },
    },
  },
  methods: {
    onStudentTypeChange(newType) {
      // تفريغ الحقول التخصصية عند تغيير نوع المؤسسة لمنع تداخل البيانات
      if (newType === 'school') {
        this.data.university_college = null;
        this.data.university_department = null;
        this.data.university_specialization = null;
        this.data.university_level = null;
        this.data.institute_field = null;
        this.data.institute_education_system = null;
        this.data.institute_specialization = null;
        this.data.institute_level = null;
      } else if (newType === 'university') {
        this.data.class_track = null;
        this.selectedStage = null;
        this.data.institute_field = null;
        this.data.institute_education_system = null;
        this.data.institute_specialization = null;
        this.data.institute_level = null;
      } else if (newType === 'institute') {
        this.data.class_track = null;
        this.selectedStage = null;
        this.data.university_college = null;
        this.data.university_department = null;
        this.data.university_specialization = null;
        this.data.university_level = null;
      }
    },

    onGovernorateChange(val) {
      this.selectedGovernorate = val;
      this.data.directorate = null;
      this.data.organization = null;
    },

    onCollegeChange() {
      this.data.university_department = null;
      this.data.university_specialization = null;
    },

    onInstituteFieldChange() {
      this.data.institute_education_system = null;
      this.data.institute_specialization = null;
    },
  },
};
</script>

<style scoped>
.gap-1 {
  gap: 4px;
}
.gap-2 {
  gap: 8px;
}
.border-dashed {
  border-style: dashed !important;
}
</style>
