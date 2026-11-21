<template>
  <CustomDialog
    :model-value="modelValue"
    width="750"
    title="إنشاء سؤال بديل جديد وإدراجه فورياً"
    subTitle="سيتم حفظ السؤال في بنك الأسئلة كمعتمد وإدراجه مباشرة في النموذج الحالي"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <div class="pa-1">
      <v-row dense>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="form.unitName"
            label="الوحدة الدراسية"
            density="compact"
            variant="outlined"
            readonly
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            v-model="form.difficulty"
            :items="[
              { title: 'سهل', value: 1 },
              { title: 'متوسط', value: 2 },
              { title: 'صعب', value: 3 }
            ]"
            label="مستوى الصعوبة"
            density="compact"
            variant="outlined"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            v-model="form.questionType"
            :items="[
              { title: 'اختيار من متعدد (Single Choice)', value: 'Single Choice' },
              { title: 'صح وخطأ (True/False)', value: 'True/False' },
              { title: 'سؤال مقالي (Essay)', value: 'Essay' },
              { title: 'إكمال الفراغ (Fill Blanks)', value: 'Fill in the Blanks' }
            ]"
            label="نوع السؤال"
            density="compact"
            variant="outlined"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model.number="form.defaultMark"
            label="درجة السؤال"
            type="number"
            step="0.5"
            min="0.5"
            density="compact"
            variant="outlined"
          />
        </v-col>
        <v-col cols="12">
          <v-textarea
            v-model="form.content"
            label="نص السؤال *"
            rows="3"
            density="compact"
            variant="outlined"
            placeholder="اكتب صياغة السؤال هنا بدقة..."
          />
        </v-col>
      </v-row>

      <!-- Options for Choice Questions -->
      <div v-if="form.questionType === 'Single Choice'" class="mt-3">
        <div class="d-flex align-center justify-space-between mb-2">
          <span class="font-weight-bold text-subtitle-2">خيارات الإجابة (حدد الإجابة الصحيحة):</span>
          <v-btn size="x-small" color="primary" variant="tonal" prepend-icon="mdi-plus" @click="addOption">
            إضافة خيار
          </v-btn>
        </div>
        <div class="d-flex flex-column gap-2">
          <div
            v-for="(opt, optIdx) in form.options"
            :key="optIdx"
            class="d-flex align-center gap-2 pa-2 rounded-xl border-subtle"
            :class="{ 'border-success': opt.isTrue }"
            :style="opt.isTrue ? 'background: rgba(16, 185, 129, 0.08);' : ''"
          >
            <v-radio
              :model-value="opt.isTrue"
              color="success"
              hide-details
              density="compact"
              class="ma-0"
              @click="setCorrectOption(optIdx)"
            />
            <span class="font-weight-bold font-mono">{{ arabicOptionLetter(optIdx) }})</span>
            <v-text-field
              v-model="opt.text"
              density="compact"
              variant="plain"
              placeholder="نص الخيار..."
              hide-details
              class="flex-grow-1"
            />
            <v-btn
              v-if="form.options && form.options.length > 2"
              size="x-small"
              icon="mdi-trash-can-outline"
              variant="text"
              color="error"
              @click="removeOption(optIdx)"
            />
          </div>
        </div>
      </div>

      <!-- Options for True/False Questions -->
      <div v-else-if="form.questionType === 'True/False'" class="mt-3">
        <span class="font-weight-bold text-subtitle-2 d-block mb-2">الإجابة الصحيحة:</span>
        <v-radio-group v-model="form.tfAnswer" inline hide-details>
          <v-radio label="صواب (True)" :value="true" color="success" />
          <v-radio label="خطأ (False)" :value="false" color="error" class="ms-4" />
        </v-radio-group>
      </div>
    </div>

    <template #actions>
      <v-btn variant="text" color="medium-emphasis" class="font-weight-bold" @click="$emit('update:modelValue', false)">
        إلغاء
      </v-btn>
      <v-btn
        color="success"
        variant="flat"
        class="font-weight-bold rounded-lg"
        :loading="loading"
        @click="$emit('submit')"
      >
        <v-icon start size="16">mdi-content-save-check</v-icon>
        حفظ وتضمين في النموذج فوراً
      </v-btn>
    </template>
  </CustomDialog>
</template>

<script setup>
import { arabicOptionLetter } from '../../composables/examHelpers'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  form: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'submit'])

const addOption = () => {
  if (!props.form.options) props.form.options = []
  props.form.options.push({ text: '', isTrue: false })
}

const removeOption = (idx) => {
  if (props.form.options && props.form.options.length > 2) {
    props.form.options.splice(idx, 1)
    if (!props.form.options.some(o => o.isTrue)) {
      props.form.options[0].isTrue = true
    }
  }
}

const setCorrectOption = (idx) => {
  if (props.form.options) {
    props.form.options.forEach((opt, i) => {
      opt.isTrue = (i === idx)
    })
  }
}
</script>
