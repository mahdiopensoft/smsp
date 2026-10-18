<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="520"
    persistent>
    <v-card rounded="xl" class="hf-create-card">
      <div class="hf-create-header">
        <v-icon icon="mdi-plus-circle-outline" size="28" color="primary" class="me-2" />
        <span class="text-h6 font-weight-black">إنشاء قالب جديد</span>
      </div>

      <v-card-text class="pb-0">
        <v-stepper v-model="wizardStep" flat>
          <!-- Step 1: Name -->
          <div v-show="wizardStep === 1">
            <div class="text-subtitle-2 font-weight-bold mb-4 text-primary">الخطوة 1: اسم القالب</div>
            <v-text-field v-model="wizardForm.name" label="اسم القالب" placeholder="مثال: قالب التقارير الرسمية"
              variant="outlined" rounded="lg" prepend-inner-icon="mdi-tag-outline" autofocus
              @keyup.enter="wizardStep = 2" />
          </div>

          <!-- Step 2: Columns -->
          <div v-show="wizardStep === 2">
            <div class="text-subtitle-2 font-weight-bold mb-4 text-primary">الخطوة 2: تحديد الأعمدة</div>
            <div class="mb-5">
              <label class="hf-label mb-2 d-block">عدد أعمدة الهيدر</label>
              <div class="hf-wizard-col-picker">
                <button v-for="n in 5" :key="n" class="hf-wizard-col-btn"
                  :class="{ active: wizardForm.headerColumns === n }" @click="wizardForm.headerColumns = n">
                  <div class="hf-col-preview">
                    <div v-for="c in n" :key="c" class="hf-col-preview-cell" />
                  </div>
                  <span>{{ n }} {{ n === 1 ? 'عمود' : 'أعمدة' }}</span>
                </button>
              </div>
            </div>
            <div>
              <label class="hf-label mb-2 d-block">عدد أعمدة الفوتر</label>
              <div class="hf-wizard-col-picker">
                <button v-for="n in 5" :key="n" class="hf-wizard-col-btn"
                  :class="{ active: wizardForm.footerColumns === n }" @click="wizardForm.footerColumns = n">
                  <div class="hf-col-preview">
                    <div v-for="c in n" :key="c" class="hf-col-preview-cell" />
                  </div>
                  <span>{{ n }} {{ n === 1 ? 'عمود' : 'أعمدة' }}</span>
                </button>
              </div>
            </div>
          </div>
        </v-stepper>
      </v-card-text>

      <v-card-actions class="pa-4 pt-2">
        <v-btn v-if="wizardStep > 1" variant="tonal" color="grey" @click="wizardStep--">رجوع</v-btn>
        <v-spacer />
        <v-btn variant="text" @click="close">إلغاء</v-btn>
        <v-btn v-if="wizardStep < 2" color="primary" variant="flat" :disabled="!wizardForm.name.trim()"
          @click="wizardStep = 2">
          التالي
        </v-btn>
        <v-btn v-else color="primary" variant="flat" prepend-icon="mdi-pencil-ruler" @click="submit">
          متابعة لتصميم القالب
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'create'])

const wizardStep = ref(1)
const wizardForm = ref({
  name: '',
  headerColumns: 3,
  footerColumns: 3
})

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      wizardStep.value = 1
      wizardForm.value = {
        name: '',
        headerColumns: 3,
        footerColumns: 3
      }
    }
  }
)

const close = () => {
  emit('update:modelValue', false)
}

const submit = () => {
  if (!wizardForm.value.name.trim()) return
  emit('create', { ...wizardForm.value })
  close()
}
</script>
