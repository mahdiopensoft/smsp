<template>
  <div>
    <add-study-systems v-model="drawer" :data="data" :getData="getData" />

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
        <!-- Name Arabic -->
        <template v-if="key === 'name_ar'">
          <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold" v-if="item.name_ar">
            <v-icon start size="14">mdi-book-education-outline</v-icon>
            {{ item.name_ar }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Unified Code -->
        <template v-else-if="key === 'unified_code'">
          <v-chip size="small" variant="outlined" color="secondary" class="font-weight-bold" v-if="item.unified_code">
            <v-icon start size="14">mdi-barcode</v-icon>
            {{ item.unified_code }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Banner Color -->
        <template v-else-if="key === 'banner_color'">
          <div class="d-flex align-center gap-2 justify-center" v-if="item.banner_color">
            <div
              :style="{ backgroundColor: item.banner_color, width: '22px', height: '22px', borderRadius: '6px', border: '1px solid rgba(0,0,0,0.15)' }"
            />
            <span class="font-weight-medium text-caption">{{ item.banner_color }}</span>
          </div>
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
import AddStudySystems from "./AddStudySystems.vue";

export default {
  name: 'StudySystemsView',
  components: { AddStudySystems },
  data() {
    return {
      url: "api/academic/study-systems/",
      data: {},
      items: {},
      drawer: false,
    };
  },

  computed: {
    headers() {
      return [
        { title: "الاسم (عربي)", key: "name_ar", sortable: true },
        { title: "الاسم (إنجليزي)", key: "name_en", sortable: true },
        { title: "الكود الموحد", key: "unified_code", align: "center", width: "150px" },
        { title: "لون البانر", key: "banner_color", align: "center", width: "150px" },
        { title: "الحالة", key: "is_active", align: "center", width: "120px" },
      ];
    },
  },

  methods: {
    async getData(params = {}) {
      try {
        const response = await shared.getData({
          path: this.url,
          params,
        });
        this.items = response;
      } catch (error) {
        console.error("Error fetching study systems:", error);
      }
    },

    editItem(item) {
      this.data = { ...item };
      this.drawer = true;
    },
  },
};
</script>
