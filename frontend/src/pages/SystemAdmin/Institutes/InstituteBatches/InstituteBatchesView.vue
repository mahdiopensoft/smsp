<template>
  <div>
    <add-institute-batches v-model="drawer" :data="data" :getData="getData" />

    <!-- Filters Bar -->
    <filter-fields label="خيارات التصفية والبحث" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Search Field -->
        <v-col cols="12" sm="6" md="4">
          <v-text-field
            v-model="searchQuery"
            label="بحث..."
            prepend-inner-icon="mdi-magnify"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
            @keydown.enter="applyFilters"
          />
        </v-col>

        <!-- Active Status Filter -->
        <v-col cols="12" sm="6" md="4">
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
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Filter Actions -->
        <v-col cols="12" sm="12" md="4" class="d-flex align-center gap-2">
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
        <span v-if="key === 'is_active'">
          <v-chip
            :color="item.is_active ? 'success' : 'error'"
            size="small"
            class="font-weight-bold"
          >
            {{ item.is_active ? 'مفعل' : 'معطل' }}
          </v-chip>
        </span>
        <span v-else-if="key === 'is_approved' || key === 'is_current' || key === 'is_graduated' || key === 'has_ministerial_exam' || key === 'is_ministerial_exam'">
          <v-chip
            :color="item[key] ? 'primary' : 'grey'"
            size="small"
            class="font-weight-bold"
          >
            {{ item[key] ? 'نعم' : 'لا' }}
          </v-chip>
        </span>
      </template>
    </custom-data-table>
  </div>
</template>

<script>
import shared from "external-components";
import AddInstituteBatches from "./AddInstituteBatches.vue";

export default {
  name: 'InstituteBatchesView',
  components: { AddInstituteBatches },
  data() {
    return {
      url: "api/academic/institutes/batches/",
      data: {},
      items: {},
      drawer: false,
      searchQuery: "",
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
        {"title": "رقم الدفعة", "key": "batch_number", "width": "110px", "align": "center", "sortable": true},
        {"title": "اسم الدفعة / الفوج", "key": "name_ar", "sortable": true},
        {"title": "التخصص", "key": "specialization_name", "sortable": true},
        {"title": "سنة الالتحاق", "key": "academic_year_name", "align": "center", "width": "140px"},
        {"title": "الخطة المعتمدة", "key": "curriculum_name", "sortable": true},
        {"title": "متخرجة", "key": "is_graduated", "align": "center", "width": "100px"},
        {"title": "الحالة", "key": "is_active", "width": "100px", "align": "center"}
      ];
    },
  },
  methods: {
    async getData(params = {}) {
      const queryParams = {
        ...params,
        search: this.searchQuery || undefined,
        is_active: this.filterActive !== null ? this.filterActive : undefined,
      };
      try {
        const response = await shared.getData({
          path: this.url,
          params: queryParams,
        });
        this.items = response;
      } catch (error) {
        console.error("Error fetching institutes-batches:", error);
      }
    },
    applyFilters() {
      this.getData();
    },
    resetFilters() {
      this.searchQuery = "";
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
