<template>
  <v-dialog 
    v-model="value" 
    :fullscreen="$vuetify.display.xs"
    :width="$vuetify.display.xs ? '100%' : '900'"
    transition="dialog-bottom-transition"
    scrollable
  >
    <v-card
      class="sneat-filter-card border-0 overflow-hidden d-flex flex-column"
      elevation="0"
      :rounded="$vuetify.display.xs ? '0' : 'lg'"
    >
      <!-- Compact Professional Header -->
      <div class="sneat-filter-header flex-shrink-0">
        <div class="d-flex align-center">
          <v-icon color="primary" size="20" class="me-3">mdi-filter-variant</v-icon>
          <div>
            <div class="filter-header-title">
              {{ $i18n.locale == 'ar' ? 'الفلترة المتقدمة' : 'Advanced Filter' }}
            </div>
            <div class="filter-header-subtitle d-none d-sm-block">
              {{ $i18n.locale == 'ar' ? 'تخصيص عرض البيانات بشروط منطقية معقدة' : 'Customize data display with complex logical conditions' }}
            </div>
          </div>
        </div>
        <div class="d-flex align-center" style="gap: var(--space-sm);">
          <v-chip
            v-if="totalFiltersCount > 0"
            size="small"
            color="primary"
            variant="tonal"
            class="filter-count-chip font-weight-bold"
          >
            {{ totalFiltersCount }} {{ $i18n.locale == 'ar' ? 'شرط' : 'conditions' }}
          </v-chip>
          <v-btn
            icon="mdi-close"
            variant="text"
            size="small"
            style="color: rgba(var(--v-theme-on-surface), 0.6)"
            @click="value = false"
          ></v-btn>
        </div>
      </div>

      <!-- Filter Content Area -->
      <v-card-text class="pa-0 flex-grow-1 sneat-filter-content" style="overflow-y: auto;">
        <div class="pa-3 pa-md-5">
          <v-form ref="filterForm">
            <FilterGroup 
              :group="activeFilters" 
              :headers="headers" 
              :operations="operations" 
              :operators="operators"
              :is-root="true" 
              @remove-item="resetFilters" 
              @enter-filter="applyFilters" 
              :level="0" 
            />
          </v-form>
        </div>
      </v-card-text>

      <!-- Action Bar -->
      <div class="sneat-filter-footer flex-shrink-0">
        <v-btn 
          variant="text" 
          style="color: rgba(var(--v-theme-on-surface), 0.6)" 
          size="small"
          class="font-weight-medium rounded-lg"
          @click="resetFilters"
        >
          {{ $i18n.locale == 'ar' ? 'مسح الكل' : 'Clear All' }}
        </v-btn>
        
        <v-spacer></v-spacer>

        <custom-btn 
          type="filter" 
          :click="applyFilters" 
          :loading="loadingApplyFilters" 
          class="px-4 px-md-8 rounded-lg font-weight-bold" 
          style="height: 38px"
        />
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from "vue";
import { useI18n } from "vue-i18n";
import FilterGroup from "./FilterGroup.vue"; 

const { locale } = useI18n();

const emit = defineEmits(["apply-filters", "update:modelValue"]);
const props = defineProps({
  headers: { type: Array, required: true },
  localLoading: { type: Boolean, default: false },
  modelValue: { type: Boolean, default: false },
  loadingApplyFilters: { type: Boolean, default: false },
});

const filterForm = ref(null);

const operators = computed(() => [
  { title: locale.value === 'ar' ? "و (AND)" : "AND", value: "AND" },
  { title: locale.value === 'ar' ? "أو (OR)" : "OR", value: "OR" },
]);

const operations = computed(() => [
  { title: locale.value === 'ar' ? "يساوي" : "Equals", value: "exact" },
  { title: locale.value === 'ar' ? "لا يساوي" : "Not Equal", value: "not_exact" },
  { title: locale.value === 'ar' ? "يحتوي على" : "Contains", value: "icontains" },
  { title: locale.value === 'ar' ? "لا يحتوي على" : "Does Not Contain", value: "not_icontains" },
  { title: locale.value === 'ar' ? "يبدأ بـ" : "Starts With", value: "istartswith" },
  { title: locale.value === 'ar' ? "ينتهي بـ" : "Ends With", value: "iendswith" },

  { title: locale.value === 'ar' ? "أكبر من" : "Greater Than", value: "gt", type: "number" },
  { title: locale.value === 'ar' ? "أكبر من أو يساوي" : "Greater Than or Equal", value: "gte", type: "number" },
  { title: locale.value === 'ar' ? "أصغر من" : "Less Than", value: "lt", type: "number" },
  { title: locale.value === 'ar' ? "أصغر من أو يساوي" : "Less Than or Equal", value: "lte", type: "number" },
]);

const activeFilters = ref({
  operator: "OR",
  filters: [{ field: null, operation: "exact", value: "" }],
});

const resetFilters = () => {
  activeFilters.value = {
    operator: "OR",
    filters: [{ field: null, operation: "exact", value: "" }],
  };
};

const applyFilters = async () => {
  const { valid } = await filterForm.value.validate();
  if (!valid) return;
  emit("apply-filters", activeFilters.value);
};

// حساب عدد الشروط بشكل عودي
const countFilters = (group) => {
  let count = 0;
  if (group.filters) {
    group.filters.forEach(item => {
      if (item.filters) {
        count += countFilters(item);
      } else {
        count++;
      }
    });
  }
    return count;
};

const totalFiltersCount = computed(() => {
  return countFilters(activeFilters.value);
});

const value = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});
</script>

<style scoped>
.sneat-filter-card {
  height: 100%;
  max-height: 90vh;
}

@media (max-width: 600px) {
  .sneat-filter-card {
    max-height: 100vh;
  }
}
</style>
