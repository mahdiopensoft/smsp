<template>
  <div>
    <add-institute-exam-periods v-model="drawer" :data="data" :getData="getData" />

    <!-- Filters Bar -->
    <filter-fields label="خيارات التصفية والبحث" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Target Semester Filter -->
        <auto-list
          v-model="filterSemester"
          name="InstituteSemester"
          label="الفصل / الفترة التدريبية"
          cols="3"
          :add="false"
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
            class="font-weight-bold mb-6"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Data Table -->
    <custom-data-table
      actionList
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
        <!-- Semester -->
        <template v-if="key === 'semester_name'">
          <span class="font-weight-medium text-body-2" v-if="item.semester_name">{{ item.semester_name }}</span>
          <span v-else class="text-medium-emphasis">كافة الفصول</span>
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
import AddInstituteExamPeriods from './AddInstituteExamPeriods.vue';

export default {
  name: 'InstituteExamPeriodsView',
  components: {
    AddInstituteExamPeriods,
  },
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      url: "api/academic/institute-exam-periods/",

      // Filters
      filterSemester: null,
      filterActive: null,
      activeOptions: [
        { text: "مفعل", value: true },
        { text: "غير مفعل", value: false },
      ],
    };
  },
  methods: {
    async getData(params = this.$params) {
      const queryParams = {
        ...(params?.params || params || {}),
      };
      if (this.filterSemester) queryParams.fk_semester = this.filterSemester;
      if (this.filterActive !== null && this.filterActive !== undefined) queryParams.is_active = this.filterActive;

      return await this.$axios
        .get(this.url, { params: queryParams })
        .then((response) => (this.items = response.data));
    },

    applyFilters() {
      this.getData();
    },

    resetFilters() {
      this.filterSemester = null;
      this.filterActive = null;
      this.getData();
    },

    editItem(data) {
      this.data = {
        ...data,
        fk_semester: data.fk_semester || data.fk_semester_id || data.semester,
      };
      this.drawer = true;
    },
  },
  computed: {
    headers() {
      return [
        { title: "الاسم (عربي)", key: "name_ar" },
        { title: "الاسم (إنجليزي)", key: "name_en" },
        { title: "الفصل / الفترة التدريبية", key: "semester_name", align: "center" },
        { title: "الترتيب", key: "order", align: "center" },
        { title: "الحالة", key: "is_active", align: "center" },
      ];
    },
  },
};
</script>
