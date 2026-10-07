<template>
  <div>
    <add-students v-model="drawer" :data="data" :getData="getData" />

    <!-- Filters Bar: الهيكلية التعليمية والإدارية المتسلسلة -->
    <filter-fields label="خيارات التصفية والتسلسل الهرمي لسجلات الممتحنين" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- 1. نوع المؤسسة التعليمية (مدارس / جامعات / معاهد) -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterInstitutionType"
            :items="institutionTypeOptions"
            item-title="text"
            item-value="value"
            class="mb-6"
            placeholder="نوع المؤسسة التعليمية"
            prepend-inner-icon="mdi-domain"
            clearable
            hide-details
            density="compact"
            variant="outlined"
            @update:model-value="onInstitutionTypeChange"
          />
        </v-col>

        <!-- 2. المحافظة (المستوى الأعلى في الهيكلية الإدارية) -->
        <auto-list
          v-model="filterGovernorate"
          name="Governorate"
          placeholder="المحافظة"
          cols="3"
          :add="false"
          @update:model-value="onGovernorateChange"
        />

        <!-- 3. المديرية (تتبع المحافظة المختارة حصراً) -->
        <auto-list
          v-model="filterDirectorate"
          name="Directorate"
          :param="filterGovernorate"
          :placeholder="filterGovernorate ? 'اختر المديرية التابعة للمحافظة' : 'اختر المحافظة أولاً'"
          :disabled="!filterGovernorate"
          cols="3"
          :add="false"
          @update:model-value="onDirectorateChange"
        />

        <!-- 4. المدرسة / الكلية / المؤسسة التعليمية (تتبع المديرية والمحافظة ونوع المؤسسة) -->
        <auto-list
          v-model="filterOrganization"
          name="Organization"
          :param="orgParam"
          :placeholder="orgPlaceholder"
          cols="3"
          :add="false"
          :disabled="!filterInstitutionType"
          @update:model-value="onOrganizationChange"
        />

        <!-- 5. البحث السريع المباشر (اسم الطالب، الرقم الأكاديمي، الهاتف) -->
        <v-col cols="12" sm="6" md="4">
          <v-text-field
            v-model="searchQuery"
            placeholder="بحث بالاسم أو الرقم الأكاديمي أو الهاتف..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            hide-details
            class="mb-6"
            @keydown.enter="applyFilters"
          />
        </v-col>

        <!-- 6. الجنس -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterGender"
            :items="genderOptions"
            item-title="text"
            item-value="value"
            placeholder="الجنس"
            prepend-inner-icon="mdi-gender-male-female"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- 7. حالة التفعيل -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterActive"
            :items="activeOptions"
            item-title="text"
            item-value="value"
            placeholder="حالة التفعيل"
            prepend-inner-icon="mdi-check-circle-outline"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- 8. أزرار التصفية والتفريغ -->
        <v-col cols="12" sm="12" md="4" class="d-flex align-center justify-end gap-2">
          <custom-btn
            type="show"
            label="تصفية"
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

    <!-- تنبيه إرشادي عند عدم تحديد أي فلتر لمنع إغراق الشاشة بالبيانات -->
    <v-alert
      v-if="!hasActiveFilter"
      type="info"
      variant="tonal"
      color="primary"
      rounded="xl"
      icon="mdi-sitemap"
      class="mb-6 font-weight-medium"
      border="start"
    >
      <div class="text-subtitle-1 font-weight-bold mb-1">
        التسلسل الهرمي لتصفية وعرض سجلات الممتحنين
      </div>
      <div class="text-body-2 text-medium-emphasis">
        يرجى اختيار نوع المؤسسة (مدارس، جامعات، أو معاهد) ثم تحديد المحافظة والمديرية لتضييق نطاق المدارس وعرض سجلات الطلاب التابعين لها، أو استخدم حقل البحث المباشر.
      </div>
    </v-alert>

    <!-- Data Table -->
    <custom-data-table
      v-bind="{
        items,
        getData,
        headers,
        delItem: url,
        editItem,
        create: () => (drawer = true),
      }"
      :hasFilter="false"
      :log="false"
      :restore="false"
    >
      <template v-slot:item-slot="{ item, key }">
        <!-- Academic Number -->
        <template v-if="key === 'academic_number'">
          <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold" v-if="item.academic_number">
            <v-icon start size="14">mdi-card-account-details-outline</v-icon>
            {{ item.academic_number }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Gender Display -->
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

        <!-- Organization Name -->
        <template v-else-if="key === 'organization_name'">
          <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold" v-if="item.organization_name">
            <v-icon start size="14">mdi-domain</v-icon>
            {{ item.organization_name }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Directorate Name -->
        <template v-else-if="key === 'directorate_name'">
          <span class="text-body-2 font-weight-medium" v-if="item.directorate_name">
            <v-icon size="14" class="me-1 text-medium-emphasis">mdi-city-variant-outline</v-icon>
            {{ item.directorate_name }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Phone Number -->
        <template v-else-if="key === 'phone_number'">
          <span class="text-body-2 font-weight-medium" dir="ltr" v-if="item.phone_number">
            <v-icon size="14" class="me-1">mdi-phone-outline</v-icon>
            {{ item.phone_number }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Is Active Status -->
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
      url: "api/academic/students/",
      hasActiveFilter: false,

      // Filters (الهيكلية المتسلسلة)
      filterInstitutionType: null,
      institutionTypeOptions: [
        { text: "🏫 مدارس", value: "school" },
        { text: "🎓 جامعات", value: "university" },
        { text: "🏢 معاهد وتدريب مهني", value: "institute" },
      ],
      filterGovernorate: null,
      filterDirectorate: null,
      filterOrganization: null,
      searchQuery: '',
      filterGender: null,
      filterActive: null,

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
      if (!this.filterInstitutionType) return "اختر نوع المؤسسة أولاً";
      const typeLabel = this.filterInstitutionType === 'university'
        ? "الكلية / الجامعة"
        : (this.filterInstitutionType === 'institute' ? "المعهد / المركز" : "المدرسة");

      if (this.filterDirectorate) {
        return `${typeLabel} (التابعة للمديرية المحددة)`;
      }
      if (this.filterGovernorate) {
        return `${typeLabel} (التابعة للمحافظة المحددة)`;
      }
      return `${typeLabel} (حدد المحافظة للتصفية الهرمية)`;
    },
    orgParam() {
      if (!this.filterInstitutionType) return '__none__';
      return {
        institution_type: this.filterInstitutionType,
        governorate: this.filterGovernorate || undefined,
        directorate: this.filterDirectorate || undefined,
      };
    },
    headers() {
      const orgTitle = this.filterInstitutionType === 'university'
        ? "الكلية / الجامعة"
        : (this.filterInstitutionType === 'institute' ? "المعهد / المركز" : "المدرسة");
      return [
        { title: "الرقم الأكاديمي", key: "academic_number" },
        { title: "اسم الطالب (عربي)", key: "name_ar" },
        { title: "اسم الطالب (إنجليزي)", key: "name_en" },
        { title: "الجنس", key: "gender_display" },
        { title: orgTitle, key: "organization_name" },
        { title: "المديرية", key: "directorate_name" },
        { title: "رقم الهاتف", key: "phone_number" },
        { title: "الحالة", key: "is_active" },
      ];
    },
  },
  methods: {
    async getData(params = this.$params) {
      const hasFilter = Boolean(
        this.filterOrganization ||
        this.filterDirectorate ||
        this.filterGovernorate ||
        this.filterInstitutionType ||
        (this.searchQuery && this.searchQuery.trim()) ||
        this.filterGender !== null ||
        this.filterActive !== null
      );

      // إذا لم يتم تحديد أي فلتر، لا تجلب كافة الطلاب من قاعدة البيانات
      if (!hasFilter) {
        this.items = { count: 0, results: [] };
        this.hasActiveFilter = false;
        return;
      }

      this.hasActiveFilter = true;
      const queryParams = {
        ...(params?.params || params || {}),
      };
      if (this.filterInstitutionType) {
        queryParams.institution_type = this.filterInstitutionType;
      }
      if (this.filterGovernorate) queryParams.governorate = this.filterGovernorate;
      if (this.filterDirectorate) queryParams.directorate = this.filterDirectorate;
      if (this.filterOrganization) queryParams.organization = this.filterOrganization;
      if (this.searchQuery && this.searchQuery.trim()) queryParams.search = this.searchQuery.trim();
      if (this.filterGender) queryParams.gender = this.filterGender;
      if (this.filterActive !== null && this.filterActive !== undefined) queryParams.is_active = this.filterActive;

      return await this.$axios
        .get(this.url, { params: queryParams })
        .then((response) => (this.items = response.data));
    },

    onInstitutionTypeChange() {
      this.filterOrganization = null;
      this.items = { count: 0, results: [] };
      this.hasActiveFilter = false;
    },

    onGovernorateChange(val) {
      if (val !== undefined) this.filterGovernorate = val;
      this.filterDirectorate = null;
      this.filterOrganization = null;
      if (this.filterInstitutionType || this.filterGovernorate) {
        this.getData();
      }
    },

    onDirectorateChange(val) {
      if (val !== undefined) this.filterDirectorate = val;
      this.filterOrganization = null;
      if (this.filterInstitutionType || this.filterDirectorate) {
        this.getData();
      }
    },

    onOrganizationChange(val) {
      if (val) {
        this.applyFilters();
      }
    },

    applyFilters() {
      this.getData();
    },

    resetFilters() {
      this.filterInstitutionType = null;
      this.filterGovernorate = null;
      this.filterDirectorate = null;
      this.filterOrganization = null;
      this.searchQuery = '';
      this.filterGender = null;
      this.filterActive = null;
      this.items = { count: 0, results: [] };
      this.hasActiveFilter = false;
    },

    editItem(data) {
      this.data = { ...data };
      this.drawer = true;
    },
  },
};
</script>

