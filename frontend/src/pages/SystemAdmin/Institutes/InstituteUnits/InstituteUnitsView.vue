<template>
  <div>
    <add-institute-units v-model="drawer" :data="data" :getData="getData" />

    <!-- Filters Bar -->
    <filter-fields label="خيارات التصفية والبحث" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Subject Filter -->
        <auto-list
          v-model="filterSubject"
          name="InstituteSubject"
          placeholder="المادة الدراسية للمعهد"
          cols="4"
          :add="false"
          @update:model-value="applyFilters"
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
      </template>
    </custom-data-table>
  </div>
</template>

<script>
import shared from "external-components";
import AddInstituteUnits from "./AddInstituteUnits.vue";

export default {
  name: 'InstituteUnitsView',
  components: { AddInstituteUnits },
  data() {
    return {
      url: "api/academic/institutes/units/",
      data: {},
      items: {},
      drawer: false,
      searchQuery: "",
      filterSubject: null,
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
        { title: "اسم الوحدة الدراسية", key: "name_ar", sortable: true },
        { title: "المادة الدراسية للمعهد", key: "subject_name", sortable: true },
        { title: "الترتيب", key: "order", width: "90px", align: "center", sortable: true },
        { title: "الحالة", key: "is_active", width: "100px", align: "center" }
      ];
    },
  },
  methods: {
    async getData(params = {}) {
      const queryParams = {
        ...params,
        search: this.searchQuery || undefined,
        subject: this.filterSubject || undefined,
        is_active: this.filterActive !== null ? this.filterActive : undefined,
      };
      try {
        const response = await shared.getData({
          path: this.url,
          params: queryParams,
        });
        this.items = response;
      } catch (error) {
        console.error("Error fetching institutes-units:", error);
      }
    },
    applyFilters() {
      this.getData();
    },
    resetFilters() {
      this.searchQuery = "";
      this.filterSubject = null;
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
