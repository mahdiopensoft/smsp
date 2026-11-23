<template>
  <div>
    <add-semesters v-model="drawer" :data="data" :getData="getData" />

    <!-- Filters Bar -->
    <filter-fields label="خيارات التصفية والبحث" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Current Semester Filter -->
        <auto-list
          v-model="filterCurrent"
          name="LocalTextOption"
          :objects="currentOptions"
          cols="3"
          label="الفصل الحالي"
          icon="star-outline"
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
        <!-- Current Semester Chip -->
        <template v-if="key === 'is_current'">
          <v-chip
            size="small"
            :color="item.is_current ? 'primary' : 'grey'"
            variant="tonal"
            class="font-weight-bold"
          >
            {{ item.is_current ? 'الفصل الحالي' : 'غير محدد' }}
          </v-chip>
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
import AddSemesters from './AddSemesters.vue';

export default {
  name: 'SemestersView',
  components: {
    AddSemesters,
  },
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      url: "api/academic/semesters/",

      // Filters
      filterCurrent: null,
      filterActive: null,

      currentOptions: [
        { text: "الفصل الحالي", value: true },
        { text: "فصول أخرى", value: false },
      ],
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
      if (this.filterCurrent !== null && this.filterCurrent !== undefined) queryParams.is_current = this.filterCurrent;
      if (this.filterActive !== null && this.filterActive !== undefined) queryParams.is_active = this.filterActive;

      return await this.$axios
        .get(this.url, { params: queryParams })
        .then((response) => (this.items = response.data));
    },

    applyFilters() {
      this.getData();
    },

    resetFilters() {
      this.filterCurrent = null;
      this.filterActive = null;
      this.getData();
    },

    editItem(data) {
      this.data = { ...data };
      this.drawer = true;
    },
  },
  computed: {
    headers() {
      return [
        { title: "اسم الفصل (عربي)", key: "name_ar" },
        { title: "اسم الفصل (إنجليزي)", key: "name_en" },
        { title: "الترتيب", key: "order" },
        { title: "الفصل الحالي", key: "is_current" },
        { title: "الحالة", key: "is_active" },
        { title: "الملاحظة", key: "note" },
      ];
    },
  },
};
</script>
