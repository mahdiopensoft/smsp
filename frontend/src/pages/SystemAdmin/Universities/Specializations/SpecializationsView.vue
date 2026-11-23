<template>
  <div>
    <add-specializations v-model="drawer" :data="data" :getData="getData" />

    <!-- Filters Bar -->
    <filter-fields label="خيارات التصفية والبحث المتقدم" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- College Filter -->
        <auto-list
          v-model="filterCollege"
          name="College"
          placeholder="الكلية"
          cols="3"
          :add="false"
          @update:model-value="onCollegeChange"
        />

        <!-- Department Filter -->
        <auto-list
          v-model="filterDepartment"
          name="DepartmentByCollege"
          :param="filterCollege"
          placeholder="القسم الأكاديمي"
          cols="3"
          :add="false"
          :disabled="!filterCollege"
        />

        <!-- Active Status Filter -->
        <auto-list
          v-model="filterActive"
          name="LocalTextOption"
          :objects="activeOptions"
          cols="3"
          label="حالة التفعيل"
          icon="check-circle-outline"
          :add="false"
        />

        <!-- Filter Actions -->
        <v-col cols="auto" class="d-flex align-center gap-2">
          <custom-btn
            type="show"
            label="تصفية"
            color="primary"
            class="font-weight-bold flex-grow-1 mb-6"
            :click="applyFilters"
          />
          <custom-btn
            type="cancel_filter"
            :click="resetFilters"
            variant="tonal"
            color="error"
            label="تفريغ"
            class="font-weight-bold flex-grow-1 mb-6"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Data Table -->
    <custom-data-table
      actionList
      :="{
        headers,
        items,
        getData,
        create: () => (drawer = true),
        delItem: url,
        editItem,
      }"
    />
  </div>
</template>

<script>
import shared from "external-components";
import AddSpecializations from "./AddSpecializations.vue";

export default {
  name: 'SpecializationsView',
  components: { AddSpecializations },
  data() {
    return {
      url: "api/academic/specializations/",
      data: {},
      items: {},
      drawer: false,

      // Filters
      filterCollege: null,
      filterDepartment: null,
      filterActive: null,

      activeOptions: [
        { text: "مفعل", value: true },
        { text: "غير مفعل", value: false },
      ],

      headers: [
        { title: "رمز التخصص", key: "specialization_code", width: "120px", align: "center", sortable: true },
        { title: "الاسم (عربي)", key: "name_ar", sortable: true },
        { title: "الاسم (إنجليزي)", key: "name_en", sortable: true },
        { title: "القسم", key: "department_name" },
        { title: "الكلية", key: "college_name" },
        { title: "المستويات", key: "number_of_levels", align: "center" },
        { title: "الحالة", key: "is_active", width: "100px", align: "center" },
      ],
    };
  },

  methods: {
    onCollegeChange() {
      this.filterDepartment = null;
    },

    async getData(params = {}) {
      const queryParams = {
        ...params,
        college: this.filterCollege || undefined,
        section: this.filterDepartment || undefined,
        is_active: this.filterActive !== null ? this.filterActive : undefined,
      };

      try {
        const response = await shared.getData({
          path: this.url,
          params: queryParams,
        });
        this.items = response;
      } catch (error) {
        console.error("Error fetching specializations:", error);
      }
    },

    applyFilters() {
      this.getData();
    },

    resetFilters() {
      this.filterCollege = null;
      this.filterDepartment = null;
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
.gap-2 {
  gap: 8px;
}
</style>
