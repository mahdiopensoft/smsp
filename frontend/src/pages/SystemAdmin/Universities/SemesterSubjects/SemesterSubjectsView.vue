<template>
  <div>
    <add-semester-subjects v-model="drawer" :data="data" :getData="getData" />

    <!-- Filters Bar -->
    <filter-fields label="خيارات التصفية والبحث المتقدم" class="main-card border-0 pa-5 rounded-2xl mb-6">
      <v-row dense class="align-center">
        <!-- Specialization Filter -->
        <auto-list
          v-model="filterSpecialization"
          name="Specialization"
          placeholder="التخصص الأكاديمي"
          cols="3"
          :add="false"
        />

        <!-- Subject Filter -->
        <auto-list
          v-model="filterSubject"
          name="Subject"
          placeholder="المادة الدراسية"
          cols="3"
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
            class="font-weight-bold flex-grow-1 mb-6"
          />
        </v-col>
      </v-row>
    </filter-fields>

    <!-- Data Table -->
    <custom-data-table
      actionList
      :="{
        headers,
        items,
        getData,
        create: () => (drawer = true),
        delItem: url,
        editItem,
      }"
    >
      <template v-slot:item-slot="{ item, key }">
        <!-- Subject Name -->
        <template v-if="key === 'subject_name'">
          <div class="py-1">
            <div class="font-weight-bold text-high-emphasis">{{ item.subject_name }}</div>
            <div class="text-caption text-medium-emphasis font-mono" v-if="item.subject_code">{{ item.subject_code }}</div>
          </div>
        </template>

        <!-- Specialization -->
        <template v-else-if="key === 'specialization_name'">
          <span class="text-body-2 font-weight-medium" v-if="item.specialization_name">{{ item.specialization_name }}</span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Level -->
        <template v-else-if="key === 'level'">
          <span class="text-body-2 font-weight-medium">المستوى {{ item.level }}</span>
        </template>

        <!-- Semester -->
        <template v-else-if="key === 'semester_name'">
          <span class="text-body-2 font-weight-medium" v-if="item.semester_name">{{ item.semester_name }}</span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <!-- Hours -->
        <template v-else-if="key === 'number_of_hours'">
          <span class="text-body-2 font-weight-bold font-mono">{{ item.number_of_hours }} س</span>
        </template>

        <!-- Core Subject -->
        <template v-else-if="key === 'is_core_subject'">
          <span class="text-body-2 font-weight-medium" :class="item.is_core_subject ? 'text-primary' : 'text-medium-emphasis'">
            {{ item.is_core_subject ? 'أساسية' : 'اختيارية' }}
          </span>
        </template>

        <!-- Active Status -->
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
import AddSemesterSubjects from "./AddSemesterSubjects.vue";

export default {
  name: 'SemesterSubjectsView',
  components: { AddSemesterSubjects },
  data() {
    return {
      url: "api/academic/semester-subjects/",
      data: {},
      items: {},
      drawer: false,

      filterSpecialization: null,
      filterSubject: null,

      headers: [
        { title: "المادة", key: "subject_name", sortable: true },
        { title: "التخصص", key: "specialization_name" },
        { title: "المستوى", key: "level", align: "center", width: "100px" },
        { title: "الفصل الدراسي", key: "semester_name" },
        { title: "الساعات", key: "number_of_hours", align: "center", width: "90px" },
        { title: "نوع المادة", key: "is_core_subject", align: "center", width: "110px" },
        { title: "الحالة", key: "is_active", align: "center", width: "100px" },
      ],
    };
  },

  methods: {
    async getData(params = {}) {
      const queryParams = {
        ...params,
        specialization: this.filterSpecialization || undefined,
        subject: this.filterSubject || undefined,
      };

      try {
        const response = await shared.getData({
          path: this.url,
          params: queryParams,
        });
        this.items = response;
      } catch (error) {
        console.error("Error fetching semester subjects:", error);
      }
    },

    applyFilters() {
      this.getData();
    },

    resetFilters() {
      this.filterSpecialization = null;
      this.filterSubject = null;
      this.getData();
    },

    editItem(item) {
      this.data = { ...item };
      this.drawer = true;
    },
  },
};
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
