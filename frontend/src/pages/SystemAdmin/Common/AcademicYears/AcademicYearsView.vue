<template>
  <div class="academic-years-page">
    <add-academic-years v-model="drawer" :data="data" :getData="handleDrawerSave" :items="items" />
    <custom-data-table
      v-bind="{
        items,
        getData,
        headers,
        delItem: url,
        editItem,
        create: createItem,
      }"
      :hasFilter="false"
      :log="false"
      :restore="false"
    >
      <template v-slot:item-slot="{ item, key }">
        <!-- Hijri Year -->
        <template v-if="key === 'hijri_year'">
          <div class="font-weight-bold text-primary d-flex align-center justify-center gap-1">
            <v-icon size="16" color="primary">mdi-calendar-text-outline</v-icon>
            <span>{{ item.hijri_year }} هـ</span>
          </div>
        </template>

        <!-- Gregorian Year -->
        <template v-else-if="key === 'gregorian_year'">
          <div class="font-weight-medium text-high-emphasis d-flex align-center justify-center gap-1">
            <v-icon size="16" color="secondary">mdi-calendar-month-outline</v-icon>
            <span>{{ item.gregorian_year }} م</span>
          </div>
        </template>

        <!-- Current Academic Year -->
        <template v-else-if="key === 'is_current'">
          <div class="d-flex align-center justify-center">
            <v-chip
              v-if="item.is_current"
              color="success"
              variant="flat"
              size="small"
              class="font-weight-bold px-3 shadow-xs"
            >
              <v-icon start size="16">mdi-check-decagram</v-icon>
              العام الحالي
            </v-chip>
            <v-btn
              v-else
              variant="tonal"
              color="primary"
              size="x-small"
              class="font-weight-bold text-caption rounded-pill px-3"
              :loading="togglingId === item.id"
              @click.stop="promptSetCurrentYear(item)"
            >
              <v-icon start size="14">mdi-radiobox-blank</v-icon>
              تعيين كعام حالي
            </v-btn>
          </div>
        </template>
      </template>
    </custom-data-table>

    <!-- Confirmation Dialog Component -->
    <confirm-dialog
      v-model="confirmDialog"
      type="info"
      title="تأكيد تعيين العام الدراسي الحالي"
      :message="confirmMessage"
      :confirmBtn="executeSetCurrentYear"
    />
  </div>
</template>

<script>
import AddAcademicYears from './AddAcademicYears.vue';

export default {
  name: 'AcademicYearsView',
  components: {
    AddAcademicYears,
  },
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      togglingId: null,
      confirmDialog: false,
      selectedYear: null,
      url: "api/academic/academic-years/",
    };
  },
  methods: {
    getItemsList() {
      if (!this.items) return [];
      if (Array.isArray(this.items)) return this.items;
      if (Array.isArray(this.items.data)) return this.items.data;
      if (Array.isArray(this.items.results)) return this.items.results;
      return [];
    },
    updateCurrentLocally(activeId) {
      const list = this.getItemsList();
      list.forEach((row) => {
        row.is_current = (row.id === activeId);
      });
    },
    enforceSingleCurrentLocally() {
      const list = this.getItemsList();
      let foundCurrent = false;
      for (const row of list) {
        if (row.is_current) {
          if (!foundCurrent) {
            foundCurrent = true;
          } else {
            row.is_current = false;
          }
        }
      }
    },
    async getData(params = this.$params) {
      const response = await this.$axios.get(this.url, { params: params?.params || params });
      this.items = response.data;
      this.enforceSingleCurrentLocally();
      return response;
    },
    async handleDrawerSave(params) {
      if (this.data && this.data.is_current && this.data.id) {
        this.updateCurrentLocally(this.data.id);
      }
      await this.getData(params);
    },
    createItem() {
      const itemsList = this.getItemsList();
      const hasCurrent = itemsList.some((i) => i.is_current);

      this.data = {
        is_active: true,
        is_current: !hasCurrent,
        hijri_year: "",
        gregorian_year: "",
      };
      this.drawer = true;
    },
    editItem(data) {
      this.data = { ...data };
      this.drawer = true;
    },
    promptSetCurrentYear(item) {
      if (!item || !item.id || item.is_current) return;
      this.selectedYear = item;
      this.confirmDialog = true;
    },
    setCurrentYear(item) {
      this.promptSetCurrentYear(item);
    },
    async executeSetCurrentYear() {
      const item = this.selectedYear;
      if (!item || !item.id) {
        this.confirmDialog = false;
        return;
      }
      this.togglingId = item.id;
      // Immediately reflect in UI:
      this.updateCurrentLocally(item.id);
      try {
        const res = await this.$axios.post(`${this.url}${item.id}/set-current/`);
        const msg = res.data?.message || "تم تعيين العام الدراسي كعام حالي بنجاح";
        if (this.$snack) {
          this.$snack("success", { message: msg });
        } else if (this.$state) {
          this.$state.alert = true;
          this.$state.alert_details = { type: "success", message: msg };
        }
        this.confirmDialog = false;
        await this.getData();
      } catch (err) {
        console.warn("set-current endpoint error, trying PATCH:", err);
        try {
          await this.$axios.patch(`${this.url}${item.id}/`, { is_current: true });
          const successMsg = "تم تعيين العام الدراسي كعام حالي بنجاح";
          if (this.$snack) {
            this.$snack("success", { message: successMsg });
          } else if (this.$state) {
            this.$state.alert = true;
            this.$state.alert_details = { type: "success", message: successMsg };
          }
          this.confirmDialog = false;
          await this.getData();
        } catch (patchErr) {
          const errMsg = patchErr?.response?.data?.message || "حدث خطأ أثناء تعيين العام الحالي";
          if (this.$snack) {
            this.$snack("error", { message: errMsg });
          } else if (this.$state) {
            this.$state.alert = true;
            this.$state.alert_details = { type: "error", message: errMsg };
          }
          this.confirmDialog = false;
          await this.getData();
        }
      } finally {
        this.togglingId = null;
      }
    },
  },
  computed: {
    confirmMessage() {
      if (!this.selectedYear) return "هل أنت متأكد من رغبتك في تعيين هذا العام الدراسي كعام حالي نشط؟";
      const hijri = this.selectedYear.hijri_year ? `${this.selectedYear.hijri_year} هـ` : '';
      const gregorian = this.selectedYear.gregorian_year ? `${this.selectedYear.gregorian_year} م` : '';
      const parts = [hijri, gregorian].filter(Boolean).join(' / ');
      return `هل أنت متأكد من تعيين العام الدراسي (${parts}) كعام دراسي حالي نشط؟ سيتم إغلاق العام الحالي السابق تلقائياً.`;
    },
    headers() {
      return [
        { title: "السنة الهجرية", key: "hijri_year", align: "center", sortable: true },
        { title: "السنة الميلادية", key: "gregorian_year", align: "center", sortable: true },
        { title: "السنة الحالية", key: "is_current", align: "center", width: "160px" },
      ];
    },
  },
};
</script>

<style scoped>
.academic-years-page {
  width: 100%;
}
</style>
