<template>
  <div>
    <add-colleges v-model="drawer" :data="data" :getData="getData" />

    <!-- Filters Bar -->
    <filter-fields label="خيارات التصفية والبحث المتقدم" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
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
        <v-col cols="12" sm="6" md="4" class="d-flex align-center gap-2">
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
        <!-- College No -->
        <template v-if="key === 'college_no'">
          <v-chip size="small" variant="outlined" color="primary" class="font-weight-bold">
            <v-icon start size="14">mdi-barcode</v-icon>
            {{ item.college_no }}
          </v-chip>
        </template>

        <!-- Name Arabic -->
        <template v-else-if="key === 'name_ar'">
          <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold" v-if="item.name_ar">
            <v-icon start size="14">mdi-school-outline</v-icon>
            {{ item.name_ar }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Highest Level -->
        <template v-else-if="key === 'highest_level'">
          <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold" v-if="item.highest_level">
            <v-icon start size="14">mdi-stairs-up</v-icon>
            {{ item.highest_level }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- First Year -->
        <template v-else-if="key === 'first_year'">
          <v-chip size="small" color="teal" variant="tonal" class="font-weight-bold" v-if="item.first_year">
            <v-icon start size="14">mdi-calendar-range</v-icon>
            {{ item.first_year }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Is Active Status -->
        <template v-else-if="key === 'is_active'">
          <v-chip
            size="small"
            :color="item.is_active ? 'success' : 'error'"
            variant="tonal"
            class="font-weight-bold text-white"
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
import shared from "external-components";
import AddColleges from "./AddColleges.vue";

export default {
  name: 'CollegesView',
  components: { AddColleges },
  data() {
    return {
      url: "api/academic/colleges/",
      data: {},
      items: {},
      drawer: false,

      // Filters
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
        { title: "رقم الكلية", key: "college_no", width: "120px", align: "center", sortable: true },
        { title: "الاسم (عربي)", key: "name_ar", sortable: true },
        { title: "الاسم (إنجليزي)", key: "name_en", sortable: true },
        { title: "أعلى مستوى", key: "highest_level", align: "center", width: "130px" },
        { title: "عام البداية", key: "first_year", align: "center", width: "130px" },
        { title: "الحالة", key: "is_active", width: "110px", align: "center" },
      ];
    },
  },

  methods: {
    async getData(params = {}) {
      const queryParams = {
        ...params,
        is_active: this.filterActive !== null ? this.filterActive : undefined,
      };

      try {
        const response = await shared.getData({
          path: this.url,
          params: queryParams,
        });
        this.items = response;
      } catch (error) {
        console.error("Error fetching colleges:", error);
      }
    },

    applyFilters() {
      this.getData();
    },

    resetFilters() {
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
