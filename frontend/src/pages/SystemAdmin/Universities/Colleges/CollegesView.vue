<template>
  <div>
    <add-colleges v-model="drawer" :data="data" :getData="getData" />

    <!-- Filters Bar -->
    <filter-fields label="خيارات التصفية والبحث المتقدم" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
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
          <span class="font-mono font-weight-bold text-primary">{{ item.college_no }}</span>
        </template>

        <!-- Name Arabic -->
        <template v-else-if="key === 'name_ar'">
          <span class="font-weight-bold text-body-2 text-high-emphasis" v-if="item.name_ar">{{ item.name_ar }}</span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Highest Level -->
        <template v-else-if="key === 'highest_level'">
          <span class="font-weight-medium text-body-2 font-mono" v-if="item.highest_level">{{ item.highest_level }}</span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- First Year -->
        <template v-else-if="key === 'first_year'">
          <span class="font-weight-medium text-body-2 font-mono" v-if="item.first_year">{{ item.first_year }}</span>
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
