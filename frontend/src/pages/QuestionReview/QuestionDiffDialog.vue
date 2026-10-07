<template>
  <v-dialog :model-value="modelValue" max-width="850" scrollable @update:model-value="$emit('update:modelValue', $event)">
    <v-card class="rounded-2xl pa-5">
      <!-- Dialog Header -->
      <v-card-title class="d-flex align-center justify-space-between pb-3 border-b">
        <div class="d-flex align-center gap-2">
          <v-icon color="primary" size="26">mdi-compare-horizontal</v-icon>
          <span class="font-weight-black text-h6">مقارنة التعديلات بين الإصدارات (Diff View)</span>
        </div>
        <v-btn icon="mdi-close" variant="text" size="small" @click="$emit('update:modelValue', false)" />
      </v-card-title>

      <v-card-text class="pt-4" style="max-height: 70vh;">
        <!-- Loading State -->
        <div v-if="loading" class="text-center pa-8">
          <v-progress-circular indeterminate color="primary" />
          <div class="text-caption mt-2">جاري حساب الفروقات بدقة...</div>
        </div>

        <!-- Error State -->
        <v-alert v-else-if="error" type="error" variant="tonal" class="rounded-xl mb-4">
          {{ error }}
        </v-alert>

        <!-- Diff Content -->
        <div v-else-if="diffData">
          <!-- Versions Info Header -->
          <div class="d-flex align-center justify-space-between pa-4 rounded-xl mb-6 bg-slate-50 border">
            <div class="d-flex align-center gap-3">
              <v-chip color="secondary" variant="tonal" class="font-weight-bold">
                الإصدار القديم (v{{ diffData.version_1.version_number }}) #{{ diffData.version_1.id }}
              </v-chip>
              <v-icon color="medium-emphasis">mdi-arrow-left</v-icon>
              <v-chip color="primary" variant="tonal" class="font-weight-bold">
                الإصدار المعدل (v{{ diffData.version_2.version_number }}) #{{ diffData.version_2.id }}
              </v-chip>
            </div>
            <v-chip :color="diffData.has_changes ? 'warning' : 'success'" variant="tonal" class="font-weight-bold">
              {{ diffData.has_changes ? 'توجد اختلافات مسجلة' : 'النسختان متطابقتان' }}
            </v-chip>
          </div>

          <!-- Question Content Diff -->
          <div class="mb-6">
            <h4 class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
              <v-icon size="20" color="primary">mdi-help-box-multiple-outline</v-icon>
              مقارنة نص السؤال
            </h4>

            <div class="pa-4 rounded-2xl border bg-white" style="line-height: 1.8;">
              <div v-html="getContentDiffHtml()"></div>
            </div>
          </div>

          <!-- Metadata Properties Diff Grid -->
          <div class="mb-6">
            <h4 class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
              <v-icon size="20" color="indigo">mdi-tune-variant</v-icon>
              مقارنة الخصائص والتصنيف
            </h4>

            <v-table class="border rounded-xl">
              <thead>
                <tr class="bg-slate-50">
                  <th class="pa-3 font-weight-bold">الخاصية</th>
                  <th class="pa-3 font-weight-bold">الإصدار القديم (v{{ diffData.version_1.version_number }})</th>
                  <th class="pa-3 font-weight-bold">الإصدار الجديد (v{{ diffData.version_2.version_number }})</th>
                  <th class="pa-3 font-weight-bold text-center">الحالة</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="f in getPropertyDiffs()" :key="f.field">
                  <td class="pa-3 font-weight-bold">{{ f.label }}</td>
                  <td class="pa-3 text-medium-emphasis">{{ f.v1_value || '-' }}</td>
                  <td class="pa-3 font-weight-medium" :class="{ 'text-primary font-weight-bold': f.changed }">
                    {{ f.v2_value || '-' }}
                  </td>
                  <td class="pa-3 text-center">
                    <v-chip size="x-small" :color="f.changed ? 'warning' : 'default'" variant="tonal">
                      {{ f.changed ? 'تغيير' : 'مطابق' }}
                    </v-chip>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </div>

          <!-- Options & Answers Diff -->
          <div v-if="diffData.options_diff && diffData.options_diff.length > 0">
            <h4 class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
              <v-icon size="20" color="teal">mdi-format-list-bulleted-type</v-icon>
              مقارنة الخيارات والإجابات
            </h4>

            <div v-for="opt in diffData.options_diff" :key="opt.index" class="pa-4 rounded-xl mb-3 border bg-white">
              <div class="d-flex align-center justify-space-between mb-2">
                <span class="font-weight-bold text-subtitle-2">الخيار {{ opt.index }}</span>
                <div class="d-flex align-center gap-2">
                  <v-chip v-if="opt.v1_is_correct" size="x-small" color="secondary" variant="outlined">
                    كان صحيحاً سابقاً
                  </v-chip>
                  <v-chip v-if="opt.v2_is_correct" size="x-small" color="success" variant="tonal">
                    صحيح حالياً
                  </v-chip>
                </div>
              </div>

              <div class="text-body-2" style="line-height: 1.6;" v-html="opt.diff_html || opt.v2_text || opt.v1_text"></div>
            </div>
          </div>
        </div>
      </v-card-text>

      <v-card-actions class="justify-end pt-3 border-t">
        <v-btn color="primary" variant="tonal" rounded="lg" @click="$emit('update:modelValue', false)">
          إغلاق
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { bankService } from '@/services/bankService'

const props = defineProps({
  modelValue: Boolean,
  v1Id: [Number, String],
  v2Id: [Number, String],
})

defineEmits(['update:modelValue'])

const loading = ref(false)
const error = ref(null)
const diffData = ref(null)

async function loadDiff() {
  if (!props.v1Id || !props.v2Id) return
  loading.value = true
  error.value = null
  try {
    const res = await bankService.compareQuestionVersions(props.v1Id, props.v2Id)
    diffData.value = res
  } catch (err) {
    error.value = err.response?.data?.error || 'فشل تحميل بيانات المقارنة'
  } finally {
    loading.value = false
  }
}

function getContentDiffHtml() {
  if (!diffData.value) return ''
  const contentField = diffData.value.fields_diff.find(f => f.field === 'content')
  return contentField ? contentField.diff_html : ''
}

function getPropertyDiffs() {
  if (!diffData.value) return []
  return diffData.value.fields_diff.filter(f => f.field !== 'content')
}

watch(() => [props.modelValue, props.v1Id, props.v2Id], () => {
  if (props.modelValue && props.v1Id && props.v2Id) {
    loadDiff()
  }
})
</script>
