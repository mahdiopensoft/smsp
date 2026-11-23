<template>
  <div>
    <add-educational-levels v-model="drawer" :data="data" :getData="getData" />

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
        <!-- Degree Name -->
        <template v-if="key === 'name_ar'">
          <span class="font-weight-bold text-body-2 text-high-emphasis" v-if="item.name_ar">{{ item.name_ar }}</span>
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
