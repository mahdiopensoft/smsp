<template>
  <div>
    <add-grading-systems v-model="drawer" :data="data" :getData="getData" />

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
        <!-- Name Arabic -->
        <template v-if="key === 'name_ar'">
          <span class="font-weight-bold text-body-2 text-high-emphasis" v-if="item.name_ar">{{ item.name_ar }}</span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Grade Total -->
        <template v-else-if="key === 'grade_total'">
          <span class="font-weight-bold font-mono text-body-2">{{ item.grade_total }}</span>
        </template>

        <!-- Success Grade -->
        <template v-else-if="key === 'success_grade'">
          <span class="font-weight-bold font-mono text-body-2 text-success">{{ item.success_grade }}</span>
        </template>

        <!-- Grade System Type -->
        <template v-else-if="key === 'grade_system_type_display'">
          <span class="text-body-2 font-weight-medium" v-if="item.grade_system_type_display">{{ item.grade_system_type_display }}</span>
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
