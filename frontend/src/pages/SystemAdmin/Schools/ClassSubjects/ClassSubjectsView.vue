<template>
  <div class="class-subjects-page">
    <!-- Filters Bar (المراحل الدراسية ومسارات الصفوف) -->
    <filter-fields label="خيارات التصفية والبحث المتقدم" class="main-card border-0 pa-5 rounded-2xl mb-6 shadow-sm">
      <v-row dense class="align-center">
        <!-- Educational Stage Filter (المرحلة الدراسية) -->
        <auto-list
          v-model="filterStage"
          name="Stage"
          placeholder="المرحلة الدراسية"
          cols="4"
          :add="false"
          @update:model-value="onStageChange"
        />

        <!-- ClassTrack Filter (الصف والمسار) -->
        <auto-list
          v-model="filterClassTrack"
          name="ClassTrackByStage"
          :param="filterStage"
          placeholder="مسارات الصفوف الدراسية"
          cols="4"
          :add="false"
          :disabled="!filterStage"
        />

        <!-- Filter Actions (تصفية + تفريغ) -->
        <v-col cols="12" sm="6" md="4" class="d-flex align-center gap-2">
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

    <!-- Empty State when no ClassTrack is selected -->
    <v-card
      v-if="!filterClassTrack"
      class="main-card border-0 pa-12 text-center rounded-2xl shadow-sm d-flex flex-column align-center justify-center"
      min-height="350"
    >
      <v-icon size="64" color="primary" class="mb-4">mdi-school-outline</v-icon>
      <h3 class="text-h6 font-weight-bold mb-2">يرجى تحديد مسار الصف</h3>
      <p class="text-medium-emphasis text-body-2" style="max-width: 450px;">
        اختر المرحلة الدراسية ثم مسار الصف واضغط على زر «تصفية» لعرض مصفوفة المواد وإسنادها وضبط درجاتها.
      </p>
    </v-card>

    <!-- Loading Skeleton -->
    <v-card rounded="lg" v-else-if="loading">
      <v-skeleton-loader type="table" height="350" />
    </v-card>

    <!-- Main Data Table Using custom-data-table-with-save Component -->
    <div v-else class="table-container">
      <custom-data-table-with-save
        :="{
          headers: headers,
          getData: loadMatrixData,
          items: items,
          top: false,
        }"
        :canAdd="false"
        :click="saveData"
      >
        <template v-slot:action>
          <div class="d-flex align-center gap-2">
            <custom-btn
              icon="account-multiple-check-outline"
              color="primary"
              variant="tonal"
              size="small"
              label="تحديد الكل"
              class="font-weight-bold"
              @click="toggleSelectAllAssigned"
            />
          </div>
        </template>
      </custom-data-table-with-save>
    </div>
  </div>
</template>

<script>
export default {
  name: "ClassSubjectsView",
  data() {
    return {
      filterStage: null,
      filterClassTrack: null,
      loading: false,
      saving: false,
      items: [],
      gradingSystems: [],
      url: "api/academic/class-subjects/",
    };
  },
  computed: {
    headers() {
      return [
        {
          title: "اسناد",
          key: "is_assigned",
          field: (field_data) => ({
            name: "is_assigned",
            type: "BooleanField",
            null: false,
            width: "70",
            update: () => {
              if (field_data.is_assigned) {
                if (!field_data.grading_system_id && this.gradingSystems.length > 0) {
                  const defaultSys = this.gradingSystems[0];
                  field_data.grading_system_id = defaultSys.id;
                  if (defaultSys.success_grade != null) {
                    field_data.min_score = defaultSys.success_grade;
                  }
                  if (defaultSys.grade_total != null) {
                    field_data.max_score = defaultSys.grade_total;
                  }
                }
                if (field_data.is_active == null) field_data.is_active = true;
                if (field_data.added_to_total == null) field_data.added_to_total = true;
                if (field_data.optional == null) field_data.optional = false;
              }
            },
          }),
        },
        {
          title: "المادة",
          key: "subject_name",
          width: "160",
        },
        {
          title: "الانظمة",
          key: "grading_system_id",
          field: (field_data) => ({
            name: "grading_system_id",
            type: "ForeignKey",
            name_list: "GradingSystem",
            objects: this.gradingSystems,
            icon: "school-outline",
            label: "الانظمة",
            null: true,
            width: "220",
            update: () => {
              const sys = this.gradingSystems.find(
                (g) => g.id === field_data.grading_system_id
              );
              if (sys) {
                if (sys.success_grade != null) {
                  field_data.min_score = sys.success_grade;
                }
                if (sys.grade_total != null) {
                  field_data.max_score = sys.grade_total;
                }
              }
            },
          }),
        },
        {
          title: "درجة الرسوب",
          key: "min_score",
          field: {
            name: "min_score",
            type: "PositiveIntegerField",
            icon: "number",
            null: false,
            width: "120",
          },
        },
        {
          title: "اعلى درجة",
          key: "max_score",
          field: {
            name: "max_score",
            type: "PositiveIntegerField",
            icon: "number",
            null: false,
            width: "120",
          },
        },
        {
          title: "تضاف للمجموع؟",
          key: "added_to_total",
          field: {
            name: "added_to_total",
            type: "BooleanField",
            null: false,
            width: "110",
          },
        },
        {
          title: "اختياري",
          key: "optional",
          field: {
            name: "optional",
            type: "BooleanField",
            null: false,
            width: "90",
          },
        },
        {
          title: "مفعل",
          key: "is_active",
          field: {
            name: "is_active",
            type: "BooleanField",
            null: false,
            width: "90",
          },
        },
        {
          title: "ملاحظة",
          key: "note",
          field: {
            name: "note",
            type: "CharField",
            null: true,
            max_length: 250,
            width: "180",
          },
        },
      ];
    },
  },
  created() {
    this.fetchGradingSystems();
  },
  methods: {
    onStageChange() {
      this.filterClassTrack = null;
      this.items = [];
    },

    applyFilters() {
      if (this.filterClassTrack) {
        this.loadMatrixData();
      }
    },

    resetFilters() {
      this.filterStage = null;
      this.filterClassTrack = null;
      this.items = [];
    },

    async fetchGradingSystems() {
      try {
        if (this.$dataList && this.$dataList().GradingSystem) {
          const res = await this.$dataList().GradingSystem.method();
          this.gradingSystems = Array.isArray(res) ? res : res?.data ?? [];
        } else {
          const res = await this.$axios.get("api/academic/grading-systems/all/");
          const raw = res.data?.data ?? res.data?.results ?? res.data ?? [];
          this.gradingSystems = Array.isArray(raw) ? raw : [];
        }
      } catch (e) {
        console.warn("Could not fetch grading systems:", e);
        try {
          const res2 = await this.$axios.get(
            "api/academic/grading-systems/?hasPagination=false"
          );
          const raw2 = res2.data?.data ?? res2.data?.results ?? res2.data ?? [];
          this.gradingSystems = Array.isArray(raw2) ? raw2 : [];
        } catch (e2) {
          console.warn("Fallback grading systems failed:", e2);
        }
      }
    },

    async loadMatrixData() {
      if (!this.filterClassTrack) return;
      this.loading = true;
      try {
        const res = await this.$axios.get(`${this.url}matrix/`, {
          params: { class_track_id: this.filterClassTrack },
        });
        if (res.data?.success && Array.isArray(res.data?.data)) {
          this.items = res.data.data;
        } else {
          await this.loadFallbackData();
        }
      } catch (err) {
        console.warn("Matrix endpoint unavailable, executing fallback:", err);
        await this.loadFallbackData();
      } finally {
        this.loading = false;
      }
    },

    async loadFallbackData() {
      try {
        const [subRes, csRes] = await Promise.all([
          this.$axios
            .get("api/academic/school-subjects/?hasPagination=false&is_active=true")
            .catch(() =>
              this.$axios.get("api/academic/subjects/?hasPagination=false&is_active=true")
            ),
          this.$axios.get(
            `${this.url}?class_track=${this.filterClassTrack}&hasPagination=false`
          ),
        ]);

        const rawSubs = subRes.data?.data ?? subRes.data?.results ?? subRes.data ?? [];
        const subjects = Array.isArray(rawSubs) ? rawSubs : [];

        const rawCs = csRes.data?.data ?? csRes.data?.results ?? csRes.data ?? [];
        const assigned = Array.isArray(rawCs) ? rawCs : [];

        const assignedMap = {};
        assigned.forEach((cs) => {
          if (cs.school_subject) assignedMap[cs.school_subject] = cs;
          else if (cs.subject) assignedMap[cs.subject] = cs;
        });

        this.items = subjects.map((s) => {
          const cs = assignedMap[s.id];
          return {
            id: cs?.id || null,
            school_subject_id: s.id,
            subject_id: cs?.subject || s.id,
            subject_name: s.name_ar,
            is_assigned: !!cs,
            grading_system_id: null,
            min_score: cs?.min_score ?? 50,
            max_score: cs?.max_score ?? 100,
            added_to_total: cs?.added_to_total ?? true,
            optional: cs?.optional ?? false,
            is_active: cs?.is_active ?? true,
            note: cs?.note || "",
          };
        });
      } catch (error) {
        console.error("Error loading fallback data:", error);
        this.items = [];
      }
    },

    toggleSelectAllAssigned() {
      const anyUnassigned = this.items.some((i) => !i.is_assigned);
      const target = anyUnassigned;
      this.items.forEach((item) => {
        item.is_assigned = target;
        if (target) {
          if (!item.grading_system_id && this.gradingSystems.length > 0) {
            const defaultSys = this.gradingSystems[0];
            item.grading_system_id = defaultSys.id;
            if (defaultSys.success_grade != null) {
              item.min_score = defaultSys.success_grade;
            }
            if (defaultSys.grade_total != null) {
              item.max_score = defaultSys.grade_total;
            }
          }
          if (item.is_active == null) item.is_active = true;
          if (item.added_to_total == null) item.added_to_total = true;
          if (item.optional == null) item.optional = false;
        }
      });
    },

    async saveData() {
      if (!this.filterClassTrack) return;
      this.saving = true;
      try {
        const payload = {
          class_track_id: this.filterClassTrack,
          items: this.items,
        };

        const res = await this.$axios.post(`${this.url}bulk-save/`, payload);
        const msg = res.data?.message || "تم حفظ مواد مسار الصف بنجاح";

        if (this.$snack) {
          this.$snack("add", { message: msg });
        } else if (this.$state) {
          this.$state.alert = true;
          this.$state.alert_details = {
            type: "success",
            message: msg,
          };
        }
        await this.loadMatrixData();
        return res;
      } catch (err) {
        console.error("Error saving class subjects:", err);
        const errMsg =
          err?.response?.data?.message || "حدث خطأ أثناء حفظ مواد مسار الصف";
        if (this.$snack) {
          this.$snack("error", { message: errMsg });
        } else if (this.$state) {
          this.$state.alert = true;
          this.$state.alert_details = {
            type: "error",
            message: errMsg,
          };
        }
        throw err;
      } finally {
        this.saving = false;
      }
    },
  },
};
</script>

<style scoped>
.class-subjects-page {
  font-family: inherit;
}
.table-container {
  width: 100%;
}
</style>
