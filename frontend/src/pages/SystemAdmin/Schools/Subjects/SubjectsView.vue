<template>
  <div>
    <add-subjects v-model="drawer" :data="data" :getData="getData" />

    <!-- Filters Bar -->
    <filter-fields label="خيارات التصفية والبحث" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Ministerial Status Filter -->
        <v-col cols="12" sm="6" md="4">
          <v-select
            v-model="filterMinisterial"
            :items="ministerialOptions"
            item-title="text"
            item-value="value"
            label="نوع المادة (وزارية)"
            prepend-inner-icon="mdi-shield-check-outline"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
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
        <v-col cols="12" sm="6" md="4" class="d-flex align-center gap-2">
          <custom-btn
            type="show"
            label="تصفية"
            color="primary"
            class="font-weight-bold mb-6"
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
        <!-- Ministerial Chip -->
        <template v-if="key === 'is_ministerial'">
          <v-chip
            size="small"
            :color="item.is_ministerial ? 'indigo' : 'grey'"
            variant="tonal"
            class="font-weight-bold"
          >
            {{ item.is_ministerial ? 'وزارية' : 'مدرسية / محلية' }}
          </v-chip>
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
import AddSubjects from './AddSubjects.vue';

export default {
  name: 'SubjectsView',
  components: {
    AddSubjects,
  },
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      url: "api/academic/subjects/",

      // Filters
      filterMinisterial: null,
      filterActive: null,

      ministerialOptions: [
        { text: "الكل", value: null },
        { text: "وزارية فقط", value: true },
        { text: "مدرسية / غير وزارية", value: false },
      ],
      activeOptions: [
        { text: "الكل", value: null },
        { text: "مفعل فقط", value: true },
        { text: "معطل فقط", value: false },
      ],
    };
  },
  methods: {
    async getData(params = this.$params) {
      const queryParams = {
        ...(params?.params || params || {}),
      };
      if (this.filterMinisterial !== null && this.filterMinisterial !== undefined) queryParams.is_ministerial = this.filterMinisterial;
      if (this.filterActive !== null && this.filterActive !== undefined) queryParams.is_active = this.filterActive;

      return await this.$axios
        .get(this.url, { params: queryParams })
        .then((response) => (this.items = response.data))
        .catch((error) => {
          console.error("Error fetching subjects:", error);
          this.items = { results: [] };
          return this.items;
        });
    },

    applyFilters() {
      this.getData();
    },

    resetFilters() {
      this.filterMinisterial = null;
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
        { title: "الاسم (عربي)", key: "name_ar" },
        { title: "الاسم (إنجليزي)", key: "name_en" },
        { title: "كود المادة", key: "subject_code" },
        { title: "الترتيب", key: "subject_order" },
        { title: "مادة وزارية", key: "is_ministerial" },
        { title: "الحالة", key: "is_active" },
      ];
    },
  },
};
</script>
