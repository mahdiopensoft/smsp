<template>
  <div>
    <add-educational-levels v-model="drawer" :data="data" :getData="getData" />

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
        <!-- Degree Name -->
        <template v-if="key === 'name_ar'">
          <v-chip size="small" color="primary" variant="tonal" class="font-weight-bold" v-if="item.name_ar">
            <v-icon start size="14">mdi-certificate-outline</v-icon>
            {{ item.name_ar }}
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
import AddEducationalLevels from "./AddEducationalLevels.vue";

export default {
  name: 'EducationalLevelsView',
  components: { AddEducationalLevels },
  data() {
    return {
      url: "api/academic/educational-levels/",
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
        { title: "الحالة", key: "is_active", align: "center" },
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
        console.error("Error fetching educational levels:", error);
      }
    },

    editItem(item) {
      this.data = { ...item };
      this.drawer = true;
    },
  },
};
</script>
