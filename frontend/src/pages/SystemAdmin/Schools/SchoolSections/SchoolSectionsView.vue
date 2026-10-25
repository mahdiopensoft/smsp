<template>
  <div>
    <add-school-sections v-model="drawer" :data="data" :getData="getData" />

    <!-- Filters Bar -->
    <filter-fields label="خيارات التصفية والبحث" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <!-- الصف 1: التبعية الجغرافية والمؤسسية (المحافظة والمديرية والمدرسة) -->
      <v-row dense class="align-center mb-1">
        <!-- 1. المحافظة -->
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

        <!-- 2. المديرية -->
        <v-col cols="12" sm="6" md="4">
          <auto-list
            v-model="filterDirectorate"
            name="Directorate"
            :param="filterGovernorate"
            :placeholder="filterGovernorate ? 'المديرية' : 'اختر المحافظة أولاً'"
            label="المديرية"
            cols="12"
            :add="false"
            :disabled="!filterGovernorate"
            @update:model-value="onDirectorateChange"
          />
        </v-col>

        <!-- 3. المدرسة -->
        <v-col cols="12" sm="12" md="4">
          <auto-list
            v-model="filterOrganization"
            name="Organization"
            :param="orgParam"
            :placeholder="orgPlaceholder"
            label="المدرسة"
            cols="12"
            :add="false"
            :disabled="isOrgDisabled"
            @update:model-value="applyFilters"
          />
        </v-col>
      </v-row>

      <!-- الصف 2: المسار الأكاديمي، العام الدراسي، البحث والحالة -->
      <v-row dense class="align-center">
        <!-- مسار الصف -->
        <v-col cols="12" sm="6" md="3">
          <auto-list
            v-model="filterClassTrack"
            name="SchoolClassTrack"
            placeholder="مسار الصف"
            label="مسار الصف"
            cols="12"
            :add="false"
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- العام الدراسي -->
        <v-col cols="12" sm="6" md="2">
          <auto-list
            v-model="filterAcademicYear"
            name="AcademicYear"
            placeholder="العام الدراسي"
            label="العام الدراسي"
            cols="12"
            :add="false"
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- حالة التفعيل -->
        <v-col cols="12" sm="6" md="2">
          <v-select
            v-model="filterActive"
            :items="activeOptions"
            item-title="text"
            item-value="value"
            label="حالة التفعيل"
            prepend-inner-icon="mdi-check-circle-outline"
            clearable
            density="compact"
            variant="outlined"
            class="mb-3"
            hide-details
            @update:model-value="applyFilters"
          />
        </v-col>

        <!-- البحث بالاسم والكود -->
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            v-model="searchQuery"
            label="بحث بالاسم أو الكود..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-3"
            hide-details
            @keydown.enter="applyFilters"
            @click:clear="onClearSearch"
          />
        </v-col>

        <!-- أزرار الإجراءات -->
        <v-col cols="12" sm="12" md="2" class="d-flex align-center gap-2 mb-3">
          <custom-btn
            type="show"
            label="تصفية"
            color="primary"
            class="font-weight-bold flex-grow-1"
            :click="applyFilters"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ"
            class="font-weight-bold flex-grow-1"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Data Table -->
    <custom-data-table
      v-bind="{
        headers,
        items,
        getData,
        create: () => (drawer = true),
        delItem: url,
        editItem,
      }"
      :hasFilter="false"
      :log="false"
      :restore="false"
    >
      <template v-slot:item-slot="{ item, key }">
        <!-- كود الشعبة -->
        <template v-if="key === 'section_code'">
          <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold font-mono" v-if="item.section_code">
            <v-icon start size="14">mdi-barcode</v-icon>
            {{ item.section_code }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- اسم المدرسة -->
        <template v-else-if="key === 'organization_name'">
          <div class="d-flex align-center gap-1">
            <v-icon size="16" color="teal">mdi-school-outline</v-icon>
            <span class="font-weight-bold text-body-2">{{ item.organization_name || '-' }}</span>
          </div>
        </template>

        <!-- نوع الشعبة (جنس) -->
        <template v-else-if="key === 'gender'">
          <v-chip
            size="small"
            :color="item.gender === 2 ? 'pink' : item.gender === 3 ? 'purple' : 'teal'"
            variant="tonal"
            class="font-weight-bold"
          >
            <v-icon start size="12">{{ item.gender === 2 ? 'mdi-gender-female' : item.gender === 3 ? 'mdi-gender-transgender' : 'mdi-gender-male' }}</v-icon>
            {{ item.gender_display || (item.gender === 2 ? 'بنات' : item.gender === 3 ? 'مشترك' : 'بنين') }}
          </v-chip>
        </template>

        <!-- حالة التفعيل -->
        <template v-else-if="key === 'is_active'">
          <v-chip
            :color="item.is_active ? 'success' : 'error'"
            size="small"
            class="font-weight-bold"
          >
            {{ item.is_active ? 'مفعل' : 'معطل' }}
          </v-chip>
        </template>
      </template>
    </custom-data-table>
  </div>
</template>

<script>
import shared from "external-components";
import AddSchoolSections from "./AddSchoolSections.vue";

export default {
  name: 'SchoolSectionsView',
  components: { AddSchoolSections },
  data() {
    return {
      url: "api/academic/school-sections/",
      data: {},
      items: {},
      drawer: false,
      searchQuery: "",
      filterGovernorate: null,
      filterDirectorate: null,
      filterOrganization: null,
      filterClassTrack: null,
      filterAcademicYear: null,
      filterActive: null,
      activeOptions: [
        { text: "مفعل", value: true },
        { text: "غير مفعل", value: false },
      ],
    };
  },
  computed: {
    headers() {
      return [
        { title: "كود الشعبة", key: "section_code", width: "120px", align: "center", sortable: true },
        { title: "اسم الشعبة / الفصل", key: "name_ar", sortable: true },
        { title: "المدرسة / المؤسسة", key: "organization_name", sortable: true },
        { title: "مسار الصف", key: "class_track_name", sortable: true },
        { title: "العام الدراسي", key: "year_name", align: "center", width: "130px" },
        { title: "النوع", key: "gender", align: "center", width: "100px" },
        { title: "السعة", key: "max_capacity", align: "center", width: "100px" },
        { title: "الحالة", key: "is_active", width: "100px", align: "center" }
      ];
    },
    isOrgDisabled() {
      return !this.filterGovernorate || !this.filterDirectorate;
    },
    orgPlaceholder() {
      if (!this.filterGovernorate) return 'اختر المحافظة أولاً...';
      if (!this.filterDirectorate) return 'اختر المديرية أولاً...';
      return 'المدرسة (التابعة للمديرية)';
    },
    orgParam() {
      return {
        institution_type: 'school',
        governorate: this.filterGovernorate || undefined,
        directorate: this.filterDirectorate || undefined,
      };
    },
  },
  methods: {
    async getData(params = {}) {
      const queryParams = {
        ...params,
        search: this.searchQuery || undefined,
        governorate: this.filterGovernorate || undefined,
        directorate: this.filterDirectorate || undefined,
        organization: this.filterOrganization || undefined,
        class_track: this.filterClassTrack || undefined,
        academic_year: this.filterAcademicYear || undefined,
        is_active: this.filterActive !== null ? this.filterActive : undefined,
      };
      try {
        const response = await shared.getData({
          path: this.url,
          params: queryParams,
        });
        this.items = response;
      } catch (error) {
        console.error("Error fetching school-sections:", error);
      }
    },
    onGovernorateChange(val) {
      this.filterGovernorate = val;
      this.filterDirectorate = null;
      this.filterOrganization = null;
      this.applyFilters();
    },
    onDirectorateChange(val) {
      this.filterDirectorate = val;
      this.filterOrganization = null;
      this.applyFilters();
    },
    onClearSearch() {
      this.searchQuery = "";
      this.applyFilters();
    },
    applyFilters() {
      this.getData();
    },
    resetFilters() {
      this.searchQuery = "";
      this.filterGovernorate = null;
      this.filterDirectorate = null;
      this.filterOrganization = null;
      this.filterClassTrack = null;
      this.filterAcademicYear = null;
      this.filterActive = null;
      this.getData();
    },
    editItem(item) {
      this.data = { ...item };
      this.drawer = true;
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
</style>
