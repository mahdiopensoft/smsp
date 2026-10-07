<template>
  <div>
    <add-class-subjects v-model="drawer" :data="data" :getData="getData" />

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

        <!-- ClassTrack Filter (الصف والمسار) -->
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

        <!-- Added To Total Filter -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterAddedToTotal"
            :items="addedToTotalOptions"
            item-title="text"
            item-value="value"
            label="مضاف للمجموع"
            prepend-inner-icon="mdi-calculator"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Optional Filter -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterOptional"
            :items="optionalOptions"
            item-title="text"
            item-value="value"
            label="طبيعة المادة"
            prepend-inner-icon="mdi-format-list-checks"
            clearable
            density="compact"
            variant="outlined"
            class="mb-6"
            hide-details
          />
        </v-col>

        <!-- Active Status Filter -->
        <v-col cols="12" sm="6" md="3">
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
        <!-- Class Track Name -->
        <template v-if="key === 'class_track_name'">
          <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold" v-if="item.class_track_name">
            <v-icon start size="14">mdi-school-outline</v-icon>
            {{ item.class_track_name }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Subject Name -->
        <template v-else-if="key === 'subject_name'">
          <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold" v-if="item.subject_name">
            <v-icon start size="14">mdi-book-outline</v-icon>
            {{ item.subject_name }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Added To Total Chip -->
        <template v-else-if="key === 'added_to_total'">
          <v-chip
            size="small"
            :color="item.added_to_total ? 'teal' : 'grey'"
            variant="tonal"
            class="font-weight-bold"
          >
            {{ item.added_to_total ? 'مضاف' : 'غير مضاف' }}
          </v-chip>
        </template>

        <!-- Optional Chip -->
        <template v-else-if="key === 'optional'">
          <v-chip
            size="small"
            :color="item.optional ? 'amber-darken-2' : 'blue-grey'"
            variant="tonal"
            class="font-weight-bold"
          >
            {{ item.optional ? 'اختيارية' : 'إجبارية' }}
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
import AddClassSubjects from './AddClassSubjects.vue';

export default {
  name: 'ClassSubjectsView',
  components: {
    AddClassSubjects,
  },
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      url: "api/academic/class-subjects/",

      // Filters
      filterStage: null,
      filterClassTrack: null,
      filterSubject: null,
      filterAddedToTotal: null,
      filterOptional: null,
      filterActive: null,

      addedToTotalOptions: [
        { text: "الكل", value: null },
        { text: "مضاف للمجموع", value: true },
        { text: "غير مضاف للمجموع", value: false },
      ],
      optionalOptions: [
        { text: "الكل", value: null },
        { text: "إجبارية فقط", value: false },
        { text: "اختيارية فقط", value: true },
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
      if (this.filterStage) queryParams.stage = this.filterStage;
      if (this.filterClassTrack) queryParams.class_track = this.filterClassTrack;
      if (this.filterSubject) queryParams.subject = this.filterSubject;
      if (this.filterAddedToTotal !== null && this.filterAddedToTotal !== undefined) queryParams.added_to_total = this.filterAddedToTotal;
      if (this.filterOptional !== null && this.filterOptional !== undefined) queryParams.optional = this.filterOptional;
      if (this.filterActive !== null && this.filterActive !== undefined) queryParams.is_active = this.filterActive;

      return await this.$axios
        .get(this.url, { params: queryParams })
        .then((response) => (this.items = response.data));
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
      this.filterAddedToTotal = null;
      this.filterOptional = null;
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
        { title: "مسار الصف", key: "class_track_name" },
        { title: "المادة", key: "subject_name" },
        { title: "الدرجة الصغرى", key: "min_score" },
        { title: "الدرجة الكبرى", key: "max_score" },
        { title: "مضاف للمجموع", key: "added_to_total" },
        { title: "اختياري", key: "optional" },
        { title: "الحالة", key: "is_active" },
      ];
    },
  },
};
</script>
