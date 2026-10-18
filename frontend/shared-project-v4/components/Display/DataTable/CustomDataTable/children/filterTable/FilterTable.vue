<template>
  <custom-dialog v-model="value" :title="$t('filter')" width="800">
    <v-card class="filter-card border-thin overflow-hidden" elevation="0" rounded="xl">
      <v-card-item class="bg-grey-lighten-4 py-3">
        <template v-slot:prepend>
          <v-icon color="primary" icon="mdi-filter-variant-plus" size="large"></v-icon>
        </template>
        <v-card-title class="text-h6 font-weight-bold color-primary">
          نظام الفلترة
        </v-card-title>
        <v-card-subtitle>قم بتخصيص عرض البيانات باستخدام الشروط المنطقية</v-card-subtitle>
      </v-card-item>

      <v-divider></v-divider>

      <v-card-text class="pa-6">
        <v-form ref="form">
          <v-expand-transition group>
            <div
              v-for="(filter, index) in activeFilters"
              :key="index"
              class="filter-row-container mb-4"
            >
              <div v-if="index > 0" class="operator-bridge">
                <v-select
                  v-model="filter.operator"
                  :items="operator"
                  density="compact"
                  variant="outlined"
                  flat
                  hide-details
                  class="operator-select"
                  :menu-props="{ zIndex: 3000 }"
                  color="primary"
                ></v-select>
              </div>

              <v-sheet
                border
                rounded="lg"
                class="pa-4 bg-grey-lighten-5 position-relative row-hover mt-6"
              >
                <v-row align="center" no-gutters>
                  <v-col cols="12" md="3" class="px-2">
                    <div class="text-caption font-weight-bold mb-1">الحقل المستهدف</div>

                    <v-select
                      v-model="filter.field"
                      :items="headers"
                      item-title="title"
                      item-value="key"
                      prepend-inner-icon="mdi-table-column"
                      placeholder="اختر الحقل"
                      density="comfortable"
                      variant="outlined"
                      :rules="[$required]"
                      :menu-props="{ zIndex: 3000 }"
                    ></v-select>
                  </v-col>

                  <v-col cols="12" md="3" class="px-2">
                    <div class="text-caption font-weight-bold mb-1">نوع العملية</div>
                    <v-select
                      v-model="filter.operation"
                      :items="operations"
                      prepend-inner-icon="mdi-equal-box"
                      placeholder="العملية"
                      density="comfortable"
                      variant="outlined"
                      :menu-props="{ zIndex: 3000 }"
                    ></v-select>
                  </v-col>

                  <v-col cols="12" md="4" class="px-2">
                    <div class="text-caption font-weight-bold mb-1">القيمة المرجعية</div>
                    <v-text-field
                      v-model="filter.value"
                      prepend-inner-icon="mdi-form-textbox"
                      placeholder="اكتب القيمة هنا..."
                      density="comfortable"
                      variant="outlined"
                      :menu-props="{ zIndex: 3000 }"
                      clearable
                      :rules="[$required]"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" md="2" class="text-center mt-4 mt-md-0">
                    <v-btn
                      icon="mdi-trash-can-outline"
                      color="red-lighten-4"
                      variant="flat"
                      class="text-red"
                      size="small"
                      @click="removeFilter(index)"
                    >
                    </v-btn>
                  </v-col>
                </v-row>
              </v-sheet>
            </div>
          </v-expand-transition>

          <div v-if="activeFilters?.length === 0" class="text-center py-8">
            <v-icon size="64" color="grey-lighten-2">mdi-filter-off-outline</v-icon>
            <div class="text-grey-darken-1 mt-2">لا توجد فلاتر نشطة حالياً</div>
          </div>
        </v-form>
      </v-card-text>

      <v-divider></v-divider>
    </v-card>
    <template v-slot:actions>
      <v-card-actions class="pa-4 bg-grey-lighten-4 w-100">
        <VRow>
          <v-btn
            color="primary"
            variant="outlined"
            prepend-icon="mdi-plus"
            rounded="lg"
            @click="addFilter"
          >
            إضافة شرط جديد
          </v-btn>

          <v-spacer></v-spacer>

          <v-btn variant="text" color="grey-darken-1" class="me-2" @click="resetFilters">
            مسح الكل
          </v-btn>

          <custom-btn
            type="filter"
            :click="applyFilters"
            :loading="loading"
            class="px-8 shadow-sm"
          />
        </VRow>
      </v-card-actions>
    </template>
  </custom-dialog>
</template>

<script setup>
import { ref, computed } from "vue";
const emit = defineEmits(["apply-filters", "update:modelValue"]);

const props = defineProps({
  headers: {
    type: Array,
    required: true,
  },
  localLoading: {
    type: Boolean,
    default: false,
  },
  activeFiltersDefault: {
    type: Array,
    default: [{ field: null, operation: "exact", value: "" }],
  },
  modelValue: {
    type: [String, Number, Boolean, Object, Array],
    default: null,
  },
});

const form = ref(null);

// 3. خيارات العمليات والربط
const operator = [
  { title: "و (AND)", value: "AND" },
  { title: "أو (OR)", value: "OR" },
];

const operations = [
  { title: "يساوي", value: "exact" },
  { title: "يحتوي على", value: "icontains" },
  { title: "أكبر من", value: "gt" },
  { title: "أكبر من أو يساوي", value: "gte" },
  { title: "أصغر من", value: "lt" },
  { title: "أصغر من أو يساوي", value: "lte" },
  { title: "يبدأ بـ", value: "istartswith" },
  { title: "ينتهي بـ", value: "iendswith" },
];

// 4. مصفوفة الفلاتر النشطة
const activeFilters = ref(props.activeFiltersDefault);

// وظائف التحكم بالفلاتر
const addFilter = async () => {
  const { valid } = await form.value.validate();
  if (!valid) return;

  if (!Array.isArray(activeFilters.value)) {
    activeFilters.value = [];
  }

  activeFilters.value.push({
    field: null,
    operation: "exact",
    value: "",
    operator: "AND",
  });
};

const removeFilter = (index) => {
  activeFilters.value.splice(index, 1);
};

const resetFilters = () => {
  activeFilters.value = [{ field: null, operation: "exact", value: "", operator: "AND" }];

  emit("apply-filters", null);
};

const applyFilters = async () => {
  const { valid } = await form.value.validate();
  if (!valid || activeFilters.value.length === 0) return;

  // تحويل البيانات لتناسب Django
  const formattedFilters = activeFilters.value.map((filter) => {
    console.log(filter);
    return {
      // هنا ندمج اسم الحقل مع العملية باستخدام __
      field: `${filter.field}`,
      operation: filter.operation,
      value: Number(filter.value),
    };
  });

  emit("apply-filters", formattedFilters);
};

const loading = computed(() => {
  return props.localLoading;
});

const value = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit("update:modelValue", value);
  },
});
</script>

<style scoped>
/* تحسينات بصرية إضافية */
.filter-card {
  border-color: #e0e0e0 !important;
  overflow: hidden;
}

.filter-row-container {
  position: relative;
}

/* تصميم الجسر المنطقي (و/أو) */
.operator-bridge {
  display: flex;
  justify-content: center;
  position: relative;
  height: 20px;
  z-index: 2;
  margin-top: -10px;
  margin-bottom: 10px;
}

.operator-select {
  width: 100px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
  border: 1px solid #eee;
}

/* تأثير التمرير على السطر */
.row-hover {
  transition: all 0.3s ease;
}
.row-hover:hover {
  border-color: #1976d2 !important;
  background-color: #f8fbff !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}

/* تنسيقات الخطوط للغة العربية */
.v-card-title {
  letter-spacing: 0 !important;
}

/* تخصيص الـ Inputs لتكون أنعم */
:deep(.v-field__outline) {
  --v-field-border-opacity: 0.15;
}
</style>
