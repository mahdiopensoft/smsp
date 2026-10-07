<template>
  <div>
    <add-units v-model="drawer" :data="data" :getData="getData" />

    <!-- Filters Bar -->
    <filter-fields label="خيارات التصفية والبحث المتقدم" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Stage Filter -->
        <auto-list
          v-model="filterStage"
          name="Stage"
          placeholder="المرحلة الدراسية"
          cols="3"
          :add="false"
          @update:model-value="onStageChange"
        />

        <!-- ClassTrack (Level - Track) Filter -->
        <auto-list
          v-model="filterClassTrack"
          name="ClassTrackByStage"
          :param="filterStage"
          placeholder="الصف والمسار"
          cols="3"
          :add="false"
          :disabled="!filterStage"
        />

        <!-- Subject Filter -->
        <auto-list
          v-model="filterSubject"
          name="Subject"
          placeholder="المادة الدراسية"
          cols="3"
          :add="false"
        />

        <!-- Semester Filter -->
        <auto-list
          v-model="filterSemester"
          name="Semester"
          placeholder="الفصل الدراسي"
          cols="3"
          :add="false"
        />

        <!-- Active Status Filter -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterActive"
            :items="activeOptions"
            item-title="text"
            item-value="value"
            placeholder="حالة التفعيل"
            prepend-inner-icon="mdi-check-circle-outline"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Filter Actions -->
        <v-col cols="12" sm="6" md="3" class="d-flex align-center gap-2">
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
      ref="table"
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
      :customLoading="loading"
    >
      <template v-slot:item-slot="{ item, key }">
        <!-- Subject Name -->
        <template v-if="key === 'subject_name'">
          <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold" v-if="item.subject_name">
            <v-icon start size="14">mdi-book-outline</v-icon>
            {{ item.subject_name }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Semester Name -->
        <template v-else-if="key === 'semester_name'">
          <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold" v-if="item.semester_name">
            <v-icon start size="14">mdi-calendar-range</v-icon>
            {{ item.semester_name }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Enable Learning Outcomes -->
        <template v-else-if="key === 'enable_learning_outcomes'">
          <v-chip
            size="small"
            :color="item.enable_learning_outcomes ? 'teal' : 'grey'"
            variant="tonal"
            class="font-weight-bold"
          >
            {{ item.enable_learning_outcomes ? 'مفعلة' : 'معطلة' }}
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
import AddUnits from './AddUnits.vue';

export default {
  name: 'UnitsView',
  components: {
    AddUnits,
  },
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      url: "api/academic/units/",
      loading: false,

      // Filters
      filterStage: null,
      filterClassTrack: null,
      filterSubject: null,
      filterSemester: null,
      filterActive: null,

      activeOptions: [
        { text: "الكل", value: null },
        { text: "مفعل فقط", value: true },
        { text: "معطل فقط", value: false },
      ],
    };
  },
  methods: {
    async getData(params = this.$params) {
      this.loading = true;
      try {
        const queryParams = {
          ...(params?.params || params || {}),
        };
        if (this.filterStage) queryParams.stage = this.filterStage;
        if (this.filterClassTrack) queryParams.class_track = this.filterClassTrack;
        if (this.filterSubject) queryParams.subject = this.filterSubject;
        if (this.filterSemester) queryParams.semester = this.filterSemester;
        if (this.filterActive !== null && this.filterActive !== undefined) queryParams.is_active = this.filterActive;

        return await this.$axios
          .get(this.url, { params: queryParams })
          .then((response) => (this.items = response.data));
      } finally {
        this.loading = false;
      }
    },

    onStageChange() {
      this.filterClassTrack = null;
    },

    applyFilters() {
      this.getData();
    },

    resetFilters() {
      this.filterStage = null;
      this.filterClassTrack = null;
      this.filterSubject = null;
      this.filterSemester = null;
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
        { title: "المادة الدراسية", key: "subject_name" },
        { title: "الفصل الدراسي", key: "semester_name" },
        { title: "الترتيب", key: "order" },
        { title: "تفعيل مخرجات التعلم", key: "enable_learning_outcomes" },
        { title: "الحالة", key: "is_active" },
      ];
    },
  },
};
</script>
