<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="650" persistent>
    <v-card rounded="xl" class="hf-assign-card" dir="rtl">
      <!-- Dialog Header -->
      <div class="hf-assign-header">
        <div class="d-flex align-center ga-2">
          <div class="hf-assign-icon-box">
            <v-icon icon="mdi-monitor-dashboard" size="22" color="primary" />
          </div>
          <div>
            <div class="text-subtitle-1 font-weight-black text-slate-800">اختيار وتخصيص الهيدر للشاشة</div>
            <div class="text-caption text-medium-emphasis">
              اربط قوالب الهيدر والفوتر المصممة بشاشات وتقارير النظام
            </div>
          </div>
        </div>
        <v-btn icon="mdi-close" size="small" variant="text" @click="$emit('update:modelValue', false)" />
      </div>

      <v-card-text class="pa-4">
        <!-- Step 1: Select Screen -->
        <div class="mb-4">
          <label class="hf-label mb-2 d-flex align-center ga-1 font-weight-bold">
            <v-icon icon="mdi-monitor" size="16" color="primary" />
            <span>1. اختر الشاشة أو التقرير المستهدف:</span>
          </label>
          <v-autocomplete
            v-model="selectedScreen"
            :items="availableScreens"
            item-title="title"
            item-value="id"
            label="ابحث عن الشاشة أو التقرير..."
            placeholder="مثال: فاتورة المبيعات، كشف حساب، تقرير المخزون..."
            variant="outlined"
            density="comfortable"
            rounded="lg"
            color="primary"
            prepend-inner-icon="mdi-magnify"
            return-object
            hide-details="auto"
          >
            <template #item="{ props: itemProps, item }">
              <v-list-item v-bind="itemProps" :subtitle="item.raw.category">
                <template #prepend>
                  <v-icon :icon="item.raw.icon" size="18" color="primary" class="me-2" />
                </template>
                <template #append v-if="getAssignedTemplateName(item.raw.id)">
                  <v-chip size="x-small" color="success" variant="flat">
                    مرتبط: {{ getAssignedTemplateName(item.raw.id) }}
                  </v-chip>
                </template>
              </v-list-item>
            </template>
          </v-autocomplete>
        </div>

        <!-- Step 2: Select Header/Footer Template -->
        <div class="mb-4">
          <label class="hf-label mb-2 d-flex align-center ga-1 font-weight-bold">
            <v-icon icon="mdi-page-layout-header-footer" size="16" color="primary" />
            <span>2. اختر قالب الهيدر والفوتر المخصص لها:</span>
          </label>
          
          <div class="hf-tpl-grid" v-if="templates && templates.length">
            <div
              v-for="tpl in templates"
              :key="tpl.id"
              class="hf-tpl-select-card"
              :class="{ active: selectedTemplateId === tpl.id }"
              @click="selectedTemplateId = tpl.id"
            >
              <div class="d-flex align-center justify-space-between mb-1">
                <span class="font-weight-black text-subtitle-2">{{ tpl.name }}</span>
                <v-icon
                  :icon="selectedTemplateId === tpl.id ? 'mdi-check-circle' : 'mdi-circle-outline'"
                  size="18"
                  :color="selectedTemplateId === tpl.id ? 'primary' : 'grey'"
                />
              </div>
              <div class="d-flex align-center ga-2 text-caption text-medium-emphasis">
                <span>الهيدر: {{ tpl.header.columns }} أعمدة</span>
                <span>•</span>
                <span>الفوتر: {{ tpl.footer.columns }} أعمدة</span>
              </div>
            </div>
          </div>

          <div v-else class="text-center pa-4 text-caption text-medium-emphasis border rounded-lg">
            لا توجد قوالب متاحة حالياً. أنشئ قالباً أولاً.
          </div>
        </div>

        <!-- Step 3: Mini Preview of Selected Template -->
        <div v-if="previewHtml" class="mb-4">
          <label class="hf-label mb-2 d-flex align-center ga-1 font-weight-bold text-success">
            <v-icon icon="mdi-eye-outline" size="16" color="success" />
            <span>معاينة الهيدر المختار:</span>
          </label>
          <div class="hf-assign-preview-box">
            <div v-html="previewHtml.header" class="hf-assign-preview-render" />
          </div>
        </div>

        <!-- Currently Assigned Screen Templates List -->
        <div v-if="assignedList.length > 0" class="mt-4 pt-3 border-t">
          <label class="hf-label mb-2 d-flex align-center ga-1 font-weight-bold text-slate-700">
            <v-icon icon="mdi-link-variant" size="16" color="primary" />
            <span>الشاشات المربوطة حالياً:</span>
          </label>
          <div class="hf-assigned-chips-wrap">
            <v-chip
              v-for="assign in assignedList"
              :key="assign.screenId"
              size="small"
              variant="tonal"
              color="primary"
              class="ma-1"
              closable
              @click:close="removeAssignment(assign.screenId)"
            >
              <v-icon icon="mdi-monitor" size="14" class="me-1" />
              <b>{{ assign.screenTitle }}</b> ➔ {{ assign.templateName }}
            </v-chip>
          </div>
        </div>
      </v-card-text>

      <!-- Dialog Actions -->
      <v-card-actions class="pa-4 pt-2 d-flex align-center justify-space-between border-t">
        <v-btn variant="text" @click="$emit('update:modelValue', false)">
          إلغاء
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          rounded="lg"
          prepend-icon="mdi-check"
          :disabled="!selectedScreen || !selectedTemplateId"
          @click="saveAssignment"
        >
          حفظ وتعيين للشاشة
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  templates: {
    type: Array,
    default: () => []
  },
  activeTemplateId: {
    type: String,
    default: null
  },
  generateHtml: {
    type: Function,
    default: () => ({ header: '', footer: '' })
  }
})

const emit = defineEmits(['update:modelValue', 'assign'])

// Standard list of system screens for user selection
const availableScreens = [
  { id: 'sales_invoice', title: 'فاتورة المبيعات (Sales Invoice)', category: 'المبيعات', icon: 'mdi-receipt' },
  { id: 'purchase_invoice', title: 'فاتورة المشتريات (Purchase Invoice)', category: 'المشتريات', icon: 'mdi-cart-arrow-down' },
  { id: 'customer_statement', title: 'كشف حساب عميل (Customer Statement)', category: 'الحسابات والعملاء', icon: 'mdi-card-account-details-outline' },
  { id: 'supplier_statement', title: 'كشف حساب مورد (Supplier Statement)', category: 'الحسابات والموردين', icon: 'mdi-account-tie-outline' },
  { id: 'inventory_report', title: 'تقرير حركة المخزون (Inventory Report)', category: 'المستودعات', icon: 'mdi-warehouse' },
  { id: 'receipt_voucher', title: 'سند قبض مالي (Receipt Voucher)', category: 'المالية والخزينة', icon: 'mdi-cash-plus' },
  { id: 'payment_voucher', title: 'سند صرف مالي (Payment Voucher)', category: 'المالية والخزينة', icon: 'mdi-cash-minus' },
  { id: 'profit_loss', title: 'تقرير الأرباح والخسائر (P&L Report)', category: 'التقارير الختامية', icon: 'mdi-chart-line' },
  { id: 'trial_balance', title: 'ميزان المراجعة (Trial Balance)', category: 'التقارير الختامية', icon: 'mdi-scale-balance' },
  { id: 'payroll_report', title: 'مسير الرواتب والموظفين (Payroll Report)', category: 'الموارد البشرية', icon: 'mdi-account-group-outline' },
  { id: 'tax_declaration', title: 'الإقرار الضريبي (VAT Report)', category: 'الضرائب', icon: 'mdi-percent-outline' }
]

const selectedScreen = ref(null)
const selectedTemplateId = ref(props.activeTemplateId || null)
const assignedList = ref([])

// Load saved assignments from localStorage
const loadSavedAssignments = () => {
  try {
    const saved = localStorage.getItem('hf_screen_assignments')
    if (saved) {
      assignedList.value = JSON.parse(saved)
    } else {
      // Default assignments
      assignedList.value = [
        { screenId: 'sales_invoice', screenTitle: 'فاتورة المبيعات', templateId: props.templates[0]?.id || '1', templateName: props.templates[0]?.name || 'قالب التقارير الرسمي' }
      ]
    }
  } catch {
    assignedList.value = []
  }
}

onMounted(() => {
  loadSavedAssignments()
})

watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    if (!selectedTemplateId.value && props.templates.length) {
      selectedTemplateId.value = props.activeTemplateId || props.templates[0].id
    }
    loadSavedAssignments()
  }
})

const getAssignedTemplateName = (screenId) => {
  const item = assignedList.value.find(a => a.screenId === screenId)
  return item ? item.templateName : null
}

const previewHtml = computed(() => {
  if (!selectedTemplateId.value) return null
  return props.generateHtml(selectedTemplateId.value)
})

const saveAssignment = () => {
  if (!selectedScreen.value || !selectedTemplateId.value) return

  const tpl = props.templates.find(t => t.id === selectedTemplateId.value)
  const templateName = tpl ? tpl.name : 'قالب محدد'

  // Update or insert assignment
  const existingIdx = assignedList.value.findIndex(a => a.screenId === selectedScreen.value.id)
  const newEntry = {
    screenId: selectedScreen.value.id,
    screenTitle: selectedScreen.value.title.split('(')[0].trim(),
    templateId: selectedTemplateId.value,
    templateName
  }

  if (existingIdx >= 0) {
    assignedList.value[existingIdx] = newEntry
  } else {
    assignedList.value.push(newEntry)
  }

  try {
    localStorage.setItem('hf_screen_assignments', JSON.stringify(assignedList.value))
  } catch (err) {
    console.warn('Could not save to localStorage:', err)
  }

  emit('assign', {
    screen: selectedScreen.value,
    template: tpl
  })

  emit('update:modelValue', false)
}

const removeAssignment = (screenId) => {
  assignedList.value = assignedList.value.filter(a => a.screenId !== screenId)
  try {
    localStorage.setItem('hf_screen_assignments', JSON.stringify(assignedList.value))
  } catch (err) {
    console.warn('Could not save to localStorage:', err)
  }
}
</script>

<style scoped>
.hf-assign-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.hf-assign-icon-box {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--hf-primary-10);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.hf-tpl-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 8px;
  max-height: 180px;
  overflow-y: auto;
  padding: 2px;
}

.hf-tpl-select-card {
  padding: 10px 12px;
  border-radius: 8px;
  border: 1.5px solid #e2e8f0;
  background: #ffffff;
  cursor: pointer;
  transition: all 0.15s ease;
}

.hf-tpl-select-card:hover {
  border-color: var(--hf-primary);
  background: #f8fafc;
}

.hf-tpl-select-card.active {
  border-color: var(--hf-primary);
  background: var(--hf-primary-10);
  box-shadow: 0 0 0 2px rgba(var(--v-theme-primary), 0.2);
}

.hf-assign-preview-box {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #ffffff;
  padding: 6px;
  max-height: 100px;
  overflow-y: auto;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.03);
}

.hf-assigned-chips-wrap {
  display: flex;
  flex-wrap: wrap;
  max-height: 90px;
  overflow-y: auto;
}
</style>
