<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="650px"
    scrollable
    persistent
  >
    <v-card class="rounded-2xl overflow-hidden print-order-modal bg-surface elevation-8 border" style="background: rgb(var(--v-theme-surface)) !important;">
      <!-- ── شريط الهوية العلوي المعتمد ── -->
      <div class="modal-top-stripe" />

      <!-- ── 1. ترويسة النافذة الرسمية الموحدة (أيقونة وهوية زرقاء primary كالسابقات تماماً) ── -->
      <div class="px-5 py-4 d-flex align-center justify-space-between border-b bg-surface">
        <div class="d-flex align-center gap-3">
          <v-avatar color="primary" variant="tonal" size="44" rounded="lg">
            <v-icon size="24" color="primary">mdi-printer-clock-outline</v-icon>
          </v-avatar>
          <div>
            <div class="d-flex align-center gap-2">
              <h3 class="text-subtitle-1 font-weight-black text-high-emphasis mb-0">اعتماد وجدولة طلب الطباعة</h3>
              <div class="center-count-badge unified-badge-primary px-2.5 py-0.5 text-caption font-weight-bold">
                قرار رسمي نافذ
              </div>
            </div>
            <div class="text-caption text-medium-emphasis">
              الموافقة الإدارية وتوجيه أمر التنفيذ للمطبعة المعتمدة
            </div>
          </div>
        </div>

        <v-btn
          icon="mdi-close"
          variant="text"
          size="small"
          density="comfortable"
          color="medium-emphasis"
          rounded="lg"
          :disabled="loading"
          @click="close"
        />
      </div>

      <!-- ── 2. محتوى النافذة المنظم بالمكونات الموحدة ── -->
      <v-card-text class="pa-5 overflow-y-auto bg-surface" style="max-height: 80vh;">
        <!-- 1. بطاقة تفاصيل الاختبار وطلب الطباعة المعتمد (هيكل منظم ومربعات بدون بيضاوي) -->
        <div class="main-card pa-4 pa-sm-5 rounded-2xl border bg-surface text-right mb-4 mx-auto elevation-1" style="max-width: 650px;">
          <!-- 1. رقم طلب الطباعة وحالة التوثيق -->
          <div class="d-flex align-center justify-space-between mb-3 pb-3 border-b flex-wrap gap-2">
            <div class="summary-item-header">
              <v-avatar color="primary" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                <v-icon size="18" color="primary">mdi-barcode</v-icon>
              </v-avatar>
              <span class="text-body-2 font-weight-medium text-medium-emphasis">رقم طلب الطباعة:</span>
            </div>
            <div class="d-flex align-center gap-2">
              <div class="center-count-badge px-3 py-1 font-mono font-weight-black text-primary text-subtitle-2">
                {{ orderNumberDisplay }}
              </div>
              <div :class="exam?.has_order ? 'unified-badge-primary' : 'unified-badge-warning'" class="center-count-badge px-2.5 py-1 text-caption font-weight-bold">
                {{ exam?.has_order ? 'طلب موثق بالنظام' : 'طلب قيد الإنشاء' }}
              </div>
            </div>
          </div>

          <!-- 2. الاختبار والمادة -->
          <div class="d-flex align-center justify-space-between mb-3 pb-3 border-b flex-wrap gap-2">
            <div class="summary-item-header">
              <v-avatar color="primary" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                <v-icon size="18" color="primary">mdi-book-education-outline</v-icon>
              </v-avatar>
              <span class="text-body-2 font-weight-medium text-medium-emphasis">الاختبار والمادة:</span>
            </div>
            <div class="d-flex align-center gap-2">
              <span class="font-weight-bold text-body-2 text-high-emphasis">{{ exam?.title || 'كل المهام' }}</span>
              <div class="center-count-badge px-2.5 py-0.5 text-caption font-weight-bold">
                المادة: {{ exam?.subject_name || 'الرياضيات' }}
              </div>
            </div>
          </div>

          <!-- 3. كود الاختبار المعتمد -->
          <div class="d-flex align-center justify-space-between mb-3 pb-3 border-b flex-wrap gap-2">
            <div class="summary-item-header">
              <v-avatar color="primary" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                <v-icon size="18" color="primary">mdi-identifier</v-icon>
              </v-avatar>
              <span class="text-body-2 font-weight-medium text-medium-emphasis">كود الاختبار:</span>
            </div>
            <div class="center-count-badge px-3 py-1 font-mono font-weight-bold text-caption text-high-emphasis">
              {{ exam?.uniqueCode || 'EXAM-C285C2A8' }}
            </div>
          </div>

          <!-- 4. المراكز والطلاب المشمولون -->
          <div class="d-flex align-center justify-space-between mb-3 pb-3 border-b flex-wrap gap-2">
            <div class="summary-item-header">
              <v-avatar color="primary" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                <v-icon size="18" color="primary">mdi-school-outline</v-icon>
              </v-avatar>
              <span class="text-body-2 font-weight-medium text-medium-emphasis">المراكز والطلاب المشمولون:</span>
            </div>
            <div class="d-flex align-center gap-2">
              <div v-if="exam?.schools_count" class="center-count-badge px-2.5 py-0.5 text-caption font-weight-bold">
                {{ exam.schools_count }} مراكز امتحانية
              </div>
              <div class="center-count-badge px-2.5 py-0.5 text-caption font-weight-bold font-mono">
                المقيدون: {{ exam?.total_registered || exam?.total_students || 8 }} طالب
              </div>
            </div>
          </div>

          <!-- 5. موعد الامتحان الفعلي للطلاب -->
          <div class="d-flex align-center justify-space-between flex-wrap gap-2">
            <div class="summary-item-header">
              <v-avatar color="primary" variant="tonal" size="34" rounded="lg" class="summary-item-avatar me-3">
                <v-icon size="18" color="primary">mdi-calendar-check</v-icon>
              </v-avatar>
              <span class="text-body-2 font-weight-medium text-medium-emphasis">موعد الامتحان الفعلي للطلاب:</span>
            </div>
            <span class="font-weight-bold text-body-2 text-high-emphasis">
              {{ exam?.actual_exam_date || exam?.exam_date || 'محدد في كشوفات المراكز' }}
            </span>
          </div>
        </div>

        <!-- 2. بيانات الجدولة والمطبعة المعتمدة (حقول واضحة ومباشرة بدون أخطاء) -->
        <div class="main-card pa-4 pa-sm-5 rounded-2xl border bg-surface text-right mb-2 mx-auto elevation-1" style="max-width: 650px;">
          <div class="d-flex align-center gap-2 mb-3 text-subtitle-2 font-weight-bold text-high-emphasis">
            <v-avatar color="primary" variant="tonal" size="30" rounded="lg">
              <v-icon size="18" color="primary">mdi-calendar-clock</v-icon>
            </v-avatar>
            <span>بيانات الجدولة الزمنية والمطبعة المنفذة</span>
          </div>

          <v-row class="align-start filter-fields-row" dense>
            <!-- موعد الطباعة المعتمد للتنفيذ (المكون الموحد CustomDate) -->
            <custom-date
              v-model="scheduledDate"
              label="موعد الطباعة المعتمد للتنفيذ"
              cols="12"
              :isRequired="true"
              :hideDetails="true"
            />

            <!-- المطبعة المنفذة (قائمة خيارات موحدة بنصوص واضحة) -->
            <v-col cols="12" class="py-1">
              <v-combobox
                v-model="pressName"
                :items="facilityOptions"
                label="المطبعة المنفذة *"
                placeholder="اختر المطبعة المنفذة"
                prepend-inner-icon="mdi-printer"
                variant="outlined"
                density="compact"
                rounded="lg"
                hide-details
                clearable
                :item-title="item => typeof item === 'string' ? item : (item.name || item.name_ar || item.title || '')"
                :item-value="item => typeof item === 'string' ? item : (item.id || item.name || '')"
                :return-object="false"
              />
            </v-col>

            <!-- الموظف المسؤول / عضو اللجنة المعتمد (قائمة مسؤولين واضحة) -->
            <v-col cols="12" class="py-1">
              <v-combobox
                v-model="responsibleOfficer"
                :items="officerOptions"
                label="الموظف المسؤول / عضو اللجنة المعتمد *"
                placeholder="اختر المسؤول المعتمد"
                prepend-inner-icon="mdi-account-tie"
                variant="outlined"
                density="compact"
                rounded="lg"
                hide-details
                clearable
                :item-title="item => typeof item === 'string' ? item : (item.name || item.name_ar || item.title || '')"
                :item-value="item => typeof item === 'string' ? item : (item.id || item.name || '')"
                :return-object="false"
              />
            </v-col>

            <!-- خيار فتح استمارة إذن الصرف (المكون الموحد CustomCheckBox) -->
            <custom-check-box
              v-model="openManifest"
              label="فتح استمارة إذن الصرف وأمر الطباعة الرسمي A4 فور الاعتماد"
              cols="12"
            />
          </v-row>

          <!-- مسار التنفيذ الذكي المتجاوب مع التاريخ (لون primary / info بدون أي أخضر) -->
          <v-alert
            v-if="routingInfo"
            :type="routingInfo.color"
            variant="tonal"
            density="compact"
            rounded="lg"
            class="mt-3 py-2"
          >
            <template #prepend>
              <v-icon size="20">{{ routingInfo.icon }}</v-icon>
            </template>
            <div class="text-caption">
              <strong>{{ routingInfo.badge }}:</strong> {{ routingInfo.text }}
            </div>
          </v-alert>
        </div>
      </v-card-text>

      <!-- ── 3. أزرار التحكم الرسمية الموحدة باللون الأساسي للنظام (primary) بدون أي أخضر ── -->
      <div class="px-5 py-3.5 d-flex align-center justify-space-between border-t bg-surface">
        <v-btn
          variant="tonal"
          color="secondary"
          rounded="lg"
          class="font-weight-bold px-4"
          prepend-icon="mdi-close"
          :disabled="loading"
          @click="close"
        >
          إلغاء
        </v-btn>

        <v-btn
          color="primary"
          variant="flat"
          rounded="lg"
          class="font-weight-bold px-6 text-white"
          prepend-icon="mdi-printer-clock"
          :loading="loading"
          @click="confirm"
        >
          تأكيد الاعتماد والجدولة الرسمية
        </v-btn>
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import api from '@/services/omr/client.js'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  exam: {
    type: Object,
    default: () => null,
  },
})

const emit = defineEmits(['update:modelValue', 'approved'])

const loading = ref(false)
const scheduledDate = ref('')
const pressName = ref('المطبعة السرية المركزية (ديوان الوزارة)')
const responsibleOfficer = ref('مدير إدارة الامتحانات والكنترول')
const openManifest = ref(true)

const facilityOptions = [
  'المطبعة السرية المركزية (ديوان الوزارة)',
  'مطبعة الكنترول المركزي بمكتب المحافظة',
  'مطبعة إدارة الامتحانات بالمديرية',
  'المركز الامتحاني المستقل',
]

const getTodayIso = () => {
  const d = new Date()
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const getCurrentUserOfficerName = () => {
  try {
    const raw = localStorage.getItem('auth_user') || localStorage.getItem('profile')
    if (raw) {
      const u = JSON.parse(raw)
      return u.full_name || u.name || u.username || 'مدير إدارة الامتحانات والكنترول'
    }
  } catch (e) {
    // ignore
  }
  return 'مدير إدارة الامتحانات والكنترول'
}

const officerOptions = computed(() => {
  const current = getCurrentUserOfficerName()
  const base = [
    current,
    'مدير إدارة الامتحانات والكنترول',
    'د. مدير عام الاختبارات والكنترول',
    'رئيس لجنة النظام والمراقبة',
    'مشرف المطبعة السرية المركزية',
    'عضو لجنة التحقق والاعتماد',
  ]
  return [...new Set(base.filter(Boolean))]
})

const orderNumberDisplay = computed(() => {
  if (!props.exam) return 'PRN-REQ-EXAM'
  return props.exam.order_number || `PRN-REQ-${props.exam.uniqueCode || props.exam.id}`
})

const routingInfo = computed(() => {
  const today = getTodayIso()
  const sel = scheduledDate.value || today
  if (sel === today) {
    return {
      type: 'due',
      color: 'primary',
      icon: 'mdi-lightning-bolt',
      badge: 'مسار فوري (المستحقة)',
      text: `تاريخ الطباعة هو اليوم (${today}) — سينتقل الطلب فوراً إلى تبويب [المستحقة] ويكون متاحاً للطباعة المباشرة والاستوديو الآن.`,
    }
  } else if (sel > today) {
    return {
      type: 'scheduled',
      color: 'info',
      icon: 'mdi-calendar-clock',
      badge: 'مسار مجدول (المجدولة)',
      text: `تاريخ الطباعة (${sel}) مستقبلي — سيتم حجز الطلب رسمياً في تبويب [المجدولة] حتى يحين موعده، مع إمكانية تقديمه استثنائياً.`,
    }
  } else {
    return {
      type: 'due_overdue',
      color: 'warning',
      icon: 'mdi-alert-circle-outline',
      badge: 'مسار عاجل متأخر (المستحقة)',
      text: `تاريخ الطباعة (${sel}) سابق لليوم — سيتم إدراجه فوراً في تبويب [المستحقة] بأولوية عاجلة.`,
    }
  }
})

const toCleanString = (val, fallback = '') => {
  if (!val) return fallback
  if (typeof val === 'string') return val
  if (typeof val === 'object') {
    return val.name || val.name_ar || val.title || val.label || fallback
  }
  return String(val)
}

watch(() => props.modelValue, (isOpen) => {
  if (isOpen && props.exam) {
    scheduledDate.value = props.exam.scheduled_print_date || getTodayIso()
    pressName.value = toCleanString(props.exam.press_name, 'المطبعة السرية المركزية (ديوان الوزارة)')
    responsibleOfficer.value = toCleanString(props.exam.responsible_officer, getCurrentUserOfficerName())
    openManifest.value = true
  }
}, { immediate: true })

const close = () => {
  emit('update:modelValue', false)
}

const confirm = async () => {
  if (!props.exam) return
  loading.value = true
  try {
    const exam = props.exam
    const today = getTodayIso()
    const schedDate = scheduledDate.value || today
    const chosenPress = pressName.value || 'المطبعة السرية المركزية (ديوان الوزارة)'
    const chosenOfficer = responsibleOfficer.value || getCurrentUserOfficerName()
    const orderNum = exam.order_number || `PRN-REQ-${exam.uniqueCode || exam.id}`

    await api.post('/api/omr/print-orders/approve/', {
      exam_id: exam.id,
      scheduled_print_date: schedDate,
      press_name: chosenPress,
      order_number: orderNum,
      responsible_officer: chosenOfficer,
    })

    emit('approved', {
      exam,
      scheduledDate: schedDate,
      pressName: chosenPress,
      responsibleOfficer: chosenOfficer,
      orderNumber: orderNum,
      openManifest: openManifest.value,
    })
    close()
  } catch (err) {
    console.error('Failed to approve order:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal-top-stripe {
  height: 4px;
  background: rgb(var(--v-theme-primary));
}

.summary-item-header {
  display: flex !important;
  align-items: center !important;
}

.summary-item-avatar {
  margin-inline-end: 12px !important;
  flex-shrink: 0 !important;
}

.center-count-badge {
  background: rgba(var(--v-theme-primary), 0.1) !important;
  color: rgb(var(--v-theme-primary)) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.22) !important;
  border-radius: 6px !important; /* مربع بزوايا خفيفة وليس بيضاوي */
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.unified-badge-primary {
  background: rgba(var(--v-theme-primary), 0.1) !important;
  color: rgb(var(--v-theme-primary)) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.25) !important;
}

.unified-badge-teal {
  background: rgba(0, 150, 136, 0.1) !important;
  color: #00897b !important;
  border: 1px solid rgba(0, 150, 136, 0.25) !important;
}

.unified-badge-warning {
  background: rgba(245, 124, 0, 0.1) !important;
  color: #e65100 !important;
  border: 1px solid rgba(245, 124, 0, 0.25) !important;
}

.unified-badge-default {
  background: rgba(var(--v-theme-on-surface), 0.06) !important;
  color: rgb(var(--v-theme-on-surface)) !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.18) !important;
}

.font-mono {
  font-family: monospace, monospace;
}

.filter-fields-row {
  margin-inline: -8px !important;
}

.filter-fields-row > [class*="v-col"] {
  padding-inline: 8px !important;
}

.gap-2 {
  gap: 8px;
}

.gap-3 {
  gap: 12px;
}
</style>
