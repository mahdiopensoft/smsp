<template>
  <div>
    <add-grading-systems v-model="drawer" :data="data" :getData="getData" />

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
            <v-icon start size="14">mdi-numeric</v-icon>
            {{ item.name_ar }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Grade Total -->
        <template v-else-if="key === 'grade_total'">
          <v-chip size="small" color="indigo" variant="tonal" class="font-weight-bold">
            <v-icon start size="14">mdi-counter</v-icon>
            {{ item.grade_total }}
          </v-chip>
        </template>

        <!-- Success Grade -->
        <template v-else-if="key === 'success_grade'">
          <v-chip size="small" color="teal" variant="tonal" class="font-weight-bold">
            <v-icon start size="14">mdi-check-decagram-outline</v-icon>
            {{ item.success_grade }}
          </v-chip>
        </template>

        <!-- Grade System Type -->
        <template v-else-if="key === 'grade_system_type_display'">
          <v-chip size="small" color="purple" variant="tonal" class="font-weight-bold" v-if="item.grade_system_type_display">
            {{ item.grade_system_type_display }}
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
import AddGradingSystems from "./AddGradingSystems.vue";

export default {
  name: 'GradingSystemsView',
  components: { AddGradingSystems },
  data() {
    return {
      url: "api/academic/grading-systems/",
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
        { title: "الدرجة الكلية", key: "grade_total", align: "center", width: "130px" },
        { title: "درجة النجاح", key: "success_grade", align: "center", width: "130px" },
        { title: "نوع نظام الدرجات", key: "grade_system_type_display", align: "center", width: "160px" },
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
        console.error("Error fetching grading systems:", error);
      }
    },

    editItem(item) {
      this.data = { ...item };
      this.drawer = true;
    },
  },
};
</script>
