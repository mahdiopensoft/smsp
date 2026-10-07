<template>
  <div>
    <add-class-tracks v-model="drawer" :data="data" :getData="getData" />

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
        />

        <!-- Track Filter -->
        <auto-list
          v-model="filterTrack"
          name="Track"
          placeholder="المسار التعليمي"
          cols="3"
          :add="false"
        />

        <!-- Default Track Filter -->
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="filterDefault"
            :items="defaultOptions"
            item-title="text"
            item-value="value"
            label="نوع المسار"
            prepend-inner-icon="mdi-tag-outline"
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
        <!-- Level Name -->
        <template v-if="key === 'level_name'">
          <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold" v-if="item.level_name">
            <v-icon start size="14">mdi-school-outline</v-icon>
            {{ item.level_name }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Track Name -->
        <template v-else-if="key === 'track_name'">
          <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold" v-if="item.track_name">
            <v-icon start size="14">mdi-source-branch</v-icon>
            {{ item.track_name }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Is Default Chip -->
        <template v-else-if="key === 'is_default'">
          <v-chip
            size="small"
            :color="item.is_default ? 'teal' : 'grey'"
            variant="tonal"
            class="font-weight-bold"
          >
            {{ item.is_default ? 'افتراضي' : 'فرعي / اختياري' }}
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
import AddClassTracks from './AddClassTracks.vue';

export default {
  name: 'ClassTracksView',
  components: {
    AddClassTracks,
  },
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      url: "api/academic/class-tracks/",

      // Filters
      filterStage: null,
      filterTrack: null,
      filterDefault: null,

      defaultOptions: [
        { text: "الكل", value: null },
        { text: "المسار الافتراضي فقط", value: true },
        { text: "المسارات الفرعية", value: false },
      ],
    };
  },
  methods: {
    async getData(params = this.$params) {
      const queryParams = {
        ...(params?.params || params || {}),
      };
      if (this.filterStage) queryParams.stage = this.filterStage;
      if (this.filterTrack) queryParams.track = this.filterTrack;
      if (this.filterDefault !== null && this.filterDefault !== undefined) queryParams.is_default = this.filterDefault;

      return await this.$axios
        .get(this.url, { params: queryParams })
        .then((response) => (this.items = response.data));
    },

    applyFilters() {
      this.getData();
    },

    resetFilters() {
      this.filterStage = null;
      this.filterTrack = null;
      this.filterDefault = null;
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
        { title: "الصف الدراسي", key: "level_name" },
        { title: "المسار التعليمي", key: "track_name" },
        { title: "المسار الافتراضي", key: "is_default" },
        { title: "الحالة", key: "is_active" },
        { title: "الملاحظة", key: "note" },
      ];
    },
  },
};
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
