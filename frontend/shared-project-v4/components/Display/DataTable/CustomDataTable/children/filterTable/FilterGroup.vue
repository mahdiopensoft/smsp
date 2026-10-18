<template>
  <div
    :class="['filter-group-container', isRoot ? '' : 'sneat-nested-group mb-4']"
    :style="groupStyle"
  >
    <div class="sneat-group-header">
      <div class="operator-toggle-container">
        <v-btn-toggle
          v-model="group.operator"
          mandatory
          density="compact"
          color="primary"
          variant="flat"
          rounded="pill"
          class="sneat-operator-toggle"
        >
          <v-btn
            v-for="op in operators"
            :key="op.value"
            :value="op.value"
            size="small"
            class="px-4 px-sm-6 font-weight-black"
          >
            {{
              $i18n.locale == "ar"
                ? op.title.split(" ")[0]
                : op.value === "AND"
                ? "AND"
                : "OR"
            }}
          </v-btn>
        </v-btn-toggle>
      </div>

      <div class="d-flex align-center flex-wrap" style="gap: var(--space-sm)">
        <v-btn
          variant="tonal"
          color="primary"
          size="small"
          class="sneat-filter-action-btn"
          @click="addNewRule"
        >
          <v-icon start icon="mdi-plus-circle-outline" size="18"></v-icon>
          <span class="d-none d-sm-inline">{{
            $i18n.locale == "ar" ? "إضافة شرط" : "Add Rule"
          }}</span>
          <span class="d-inline d-sm-none">{{
            $i18n.locale == "ar" ? "شرط" : "Rule"
          }}</span>
        </v-btn>

        <v-btn
          variant="tonal"
          color="secondary"
          size="small"
          class="sneat-filter-action-btn"
          @click="addNewGroup"
        >
          <v-icon start icon="mdi-folder-plus-outline" size="18"></v-icon>
          <span class="d-none d-sm-inline">{{
            $i18n.locale == "ar" ? "إضافة مجموعة" : "Add Group"
          }}</span>
          <span class="d-inline d-sm-none">{{
            $i18n.locale == "ar" ? "مجموعة" : "Group"
          }}</span>
        </v-btn>
      </div>

      <v-spacer class="d-none d-md-block"></v-spacer>

      <v-btn
        v-if="!isRoot"
        size="small"
        color="error"
        variant="tonal"
        class="sneat-filter-action-btn"
        style="min-width: 36px"
        @click="$emit('remove-item')"
      >
        <v-icon icon="mdi-close" size="20"></v-icon>
        <VTooltip activator="parent" location="top"
          >{{ $i18n.locale == "ar" ? "حذف المجموعة" : "Remove Group" }}
        </VTooltip>
      </v-btn>
    </div>

    <div v-for="(item, index) in group.filters" :key="index">
      <FilterGroup
        v-if="item.hasOwnProperty('filters')"
        :group="item"
        :headers="headers"
        :operations="operations"
        :operators="operators"
        :is-root="false"
        @remove-item="group.filters.splice(index, 1)"
        :level="level + 1"
      />

      <v-sheet v-else border rounded="lg" class="sneat-filter-row">
        <v-row align="center" dense>
          <!-- Target Field -->
          <v-col cols="12" sm="6" md="4" class="px-2">
            <div class="sneat-field-label">
              {{ $i18n.locale == "ar" ? "الحقل" : "field" }}
            </div>
            <v-select
              v-model="item.field"
              :items="headers"
              item-title="title"
              item-value="key"
              prepend-inner-icon="mdi-table-column"
              :placeholder="
                $i18n.locale == 'ar' ? 'اختر الحقل' : 'choose field'
              "
              density="compact"
              variant="outlined"
              hide-details="auto"
              :rules="[(v) => !!v || 'مطلوب']"
              class="sneat-filter-input"
              :menu-props="{ zIndex: 10000 }"
            ></v-select>
          </v-col>
          <!-- Operation Type -->
          <v-col cols="12" sm="6" md="3" class="px-2 mt-2 mt-sm-0">
            <div class="sneat-field-label">
              {{ $i18n.locale == "ar" ? "العملية" : "operation" }}
            </div>
            <v-select
              v-model="item.operation"
              :items="operations"
              prepend-inner-icon="mdi-equal-box"
              :placeholder="$i18n.locale == 'ar' ? 'العملية' : 'operation'"
              density="compact"
              variant="outlined"
              hide-details="auto"
              @update:modelValue="getFieldInputType(item.operation, index)"
              class="sneat-filter-input"
              :menu-props="{ zIndex: 10000 }"
            ></v-select>
          </v-col>
          <!-- Reference Value -->
          <v-col cols="10" sm="10" md="4" class="px-2 mt-2 mt-md-0">
            <div class="sneat-field-label">
              {{ $i18n.locale == "ar" ? "القيمة" : "Value" }}
            </div>
            <v-text-field
              v-model="item.value"
              prepend-inner-icon="mdi-form-textbox"
              :placeholder="$i18n.locale == 'ar' ? 'القيمة' : 'Value'"
              density="compact"
              variant="outlined"
              hide-details="auto"
              :rules="[(v) => !!v || 'مطلوب']"
              :type="item.type"
              @keydown.enter="enterFilter"
              class="sneat-filter-input"
            ></v-text-field>
          </v-col>
          <!-- Delete Action -->
          <v-col
            cols="2"
            sm="2"
            md="1"
            class="d-flex align-center justify-center mt-2 mt-md-0 pt-4 pt-md-4"
          >
            <v-btn
              variant="tonal"
              color="error"
              size="small"
              class="sneat-filter-action-btn"
              style="min-width: 36px"
              @click="group.filters.splice(index, 1)"
            >
              <v-icon icon="mdi-trash-can-outline" size="20"></v-icon>
              <VTooltip activator="parent" location="top"
                >{{ $i18n.locale == "ar" ? "حذف الشرط" : "Remove Rule" }}
              </VTooltip>
            </v-btn>
          </v-col>
        </v-row>
      </v-sheet>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useDisplay } from "vuetify";

const { xs } = useDisplay();

// تعريف المكون لنفسه للسماح بالاستدعاء العودي
defineOptions({
  name: "FilterGroup",
});

const props = defineProps({
  group: Object,
  headers: Array,
  operations: Array,
  operators: Array,
  isRoot: Boolean,
  level: Number,
});

const emit = defineEmits(["remove-item", "enter-filter"]);

const addNewRule = () => {
  props.group.filters.push({ field: null, operation: "exact", value: "" });
};

const addNewGroup = () => {
  props.group.filters.push({
    operator: "OR",
    filters: [{ field: null, operation: "exact", value: "" }],
  });
};
const enterFilter = () => {
  emit("enter-filter");
};

const getFieldInputType = (fieldKey, index) => {
  // البحث عن الحقل المختار في المصفوفة لمعرفة نوعه
  const selectedField = props.operations.find((h) => h.value === fieldKey);
  const typeF = selectedField?.type === "number" ? "number" : "text";
  props.group.filters[index].type = typeF;
};

// Colors based on primary tokens for a unified look
const groupColors = [
  "rgb(var(--v-theme-primary))",
  "rgb(var(--v-theme-info))",
  "rgb(var(--v-theme-secondary))",
  "rgb(var(--v-theme-warning))",
  "rgb(var(--v-theme-success))",
];

const groupStyle = computed(() => {
  if (props.isRoot)
    return {
      padding: xs.value ? "var(--space-xs)" : "var(--space-sm)",
      position: "relative",
    };

  const color = groupColors[props.level % groupColors.length];
  return {
    borderInlineStart: `3px solid ${color}`,
    borderInlineEnd: `1px solid rgba(var(--v-theme-on-surface), 0.08)`,
    borderTop: `1px solid rgba(var(--v-theme-on-surface), 0.08)`,
    borderBottom: `1px solid rgba(var(--v-theme-on-surface), 0.08)`,
    backgroundColor:
      props.level % 2 === 0
        ? `rgba(var(--v-theme-on-surface), 0.02)`
        : `rgb(var(--v-theme-surface))`,
    marginInlineStart: props.isRoot
      ? "0"
      : xs.value
      ? "var(--space-xs)"
      : "var(--space-md)",
    borderRadius: "var(--radius-lg)",
    position: "relative",
    transition: "var(--transition-default)",
  };
});
</script>

<style scoped>
/* Scoped overrides — all global classes are in filter.css */
</style>
