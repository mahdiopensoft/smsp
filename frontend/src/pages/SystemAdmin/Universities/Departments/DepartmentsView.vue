<template>
  <div>
    <add-departments v-model="drawer" :data="data" :getData="getData" />

    <!-- Filters Bar -->
    <filter-fields label="خيارات التصفية والبحث المتقدم" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- College Filter -->
        <auto-list v-model="filterCollege" name="College" placeholder="الكلية" cols="4" :add="false" />

        <!-- Active Status Filter -->
        <v-col cols="12" sm="6" md="4">
          <v-select v-model="filterActive" :items="activeOptions" item-title="text" item-value="value"
            label="حالة التفعيل" prepend-inner-icon="mdi-check-circle-outline" clearable density="compact"
            variant="outlined" class="mb-6" hide-details />
        </v-col>

        <!-- Filter Actions -->
        <v-col cols="12" sm="6" md="4" class="d-flex align-center gap-2">
          <custom-btn type="show" label="تصفية" color="primary" class="font-weight-bold flex-grow-1 mb-6"
            :click="applyFilters" />
          <custom-btn type="cancel_filter" :click="resetFilters" variant="tonal" color="error" label="تفريغ"
            class="font-weight-bold flex-grow-1 mb-6" />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Data Table -->
    <custom-data-table :="{
      headers,
      items,
      getData,
      create: () => (drawer = true),
      delItem: url,
      editItem,
    }" />
  </div>
</template>

<script>
import shared from "external-components";
import AddDepartments from "./AddDepartments.vue";

export default {
  name: 'DepartmentsView',
  components: { AddDepartments },
  data() {
    return {
      url: "api/academic/departments/",
      data: {},
      items: {},
      drawer: false,

      // Filters
      filterCollege: null,
      filterActive: null,

      activeOptions: [
        { text: "مفعل", value: true },
        { text: "غير مفعل", value: false },
      ],

      headers: [
        { title: "رمز القسم", key: "section_code", width: "120px", align: "center", sortable: true },
        { title: "الاسم (عربي)", key: "name_ar", sortable: true },
        { title: "الاسم (إنجليزي)", key: "name_en", sortable: true },
        { title: "الكلية", key: "college_name" },
        { title: "الحالة", key: "is_active", width: "100px", align: "center" },
      ],
    };
  },

  methods: {
    async getData(params = {}) {
      const queryParams = {
        ...params,
        college: this.filterCollege || undefined,
        is_active: this.filterActive !== null ? this.filterActive : undefined,
      };

      try {
        const response = await shared.getData({
          path: this.url,
          params: queryParams,
        });
        this.items = response;
      } catch (error) {
        console.error("Error fetching departments:", error);
      }
    },

    applyFilters() {
      this.getData();
    },

    resetFilters() {
      this.filterCollege = null;
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
