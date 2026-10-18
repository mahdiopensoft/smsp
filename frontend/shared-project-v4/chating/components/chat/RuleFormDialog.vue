<template>
  <v-dialog v-model="dialog" max-width="700px" persistent>
    <v-card class="rounded-xl">
      <v-card-title class="pa-4 bg-primary text-white d-flex align-center">
        <span class="text-h6">{{ isEdit ? 'تعديل القاعدة' : 'إضافة قاعدة جديدة' }}</span>
        <v-spacer></v-spacer>
        <v-btn icon="mdi-close" variant="text" @click="closeDialog" color="white"></v-btn>
      </v-card-title>
      
      <v-card-text class="pa-4">
        <v-form ref="form" v-model="isValid" @submit.prevent="save">
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.rule_name"
                label="اسم القاعدة (Unique)"
                :rules="[v => !!v || 'هذا الحقل مطلوب']"
                variant="outlined"
                density="comfortable"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.source_role"
                label="الدور المستهدف (Source Role)"
                :rules="[v => !!v || 'هذا الحقل مطلوب']"
                placeholder="مثال: student"
                variant="outlined"
                density="comfortable"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="formData.description"
                label="الوصف"
                rows="2"
                variant="outlined"
                density="comfortable"
              ></v-textarea>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model.number="formData.priority"
                label="الأولوية (Priority)"
                type="number"
                variant="outlined"
                density="comfortable"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6" class="d-flex align-center">
              <v-switch
                v-model="formData.is_active"
                label="مفعلة"
                color="success"
                hide-details
              ></v-switch>
            </v-col>
            <v-col cols="12">
              <div class="text-subtitle-1 mb-2">إعداد الاستعلام (Query Config JSON)</div>
              <v-textarea
                v-model="jsonString"
                label="JSON Config"
                rows="6"
                variant="outlined"
                :rules="[validateJson]"
                class="font-monospace"
                dir="ltr"
                style="direction: ltr;"
              ></v-textarea>
              <div class="text-caption text-error" v-if="jsonError">{{ jsonError }}</div>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      
      <v-card-actions class="pa-4 pt-0">
        <v-spacer></v-spacer>
        <v-btn
          color="grey-darken-1"
          variant="outlined"
          @click="closeDialog"
          class="px-6 rounded-pill"
          :disabled="isSaving"
        >
          إلغاء
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          @click="save"
          class="px-6 rounded-pill"
          :loading="isSaving"
          :disabled="!isValid || !!jsonError"
        >
          حفظ
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  rule: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['update:modelValue', 'saved']);

const dialog = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
});

const isEdit = computed(() => !!props.rule && !!props.rule.id);
const form = ref(null);
const isValid = ref(false);
const isSaving = ref(false);
const jsonString = ref('{\n  "target_model": "users.User",\n  "filters": {}\n}');
const jsonError = ref('');

const defaultData = {
  rule_name: '',
  source_role: '',
  description: '',
  priority: 0,
  is_active: true,
  query_config: { target_model: 'users.User', filters: {} }
};

const formData = ref({ ...defaultData });

// تحديث البيانات عند فتح النافذة
watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    if (props.rule) {
      formData.value = { ...props.rule };
      jsonString.value = JSON.stringify(props.rule.query_config || {}, null, 2);
    } else {
      formData.value = { ...defaultData };
      jsonString.value = '{\n  "target_model": "users.User",\n  "filters": {}\n}';
    }
    jsonError.value = '';
    if (form.value) form.value.resetValidation();
  }
});

// التحقق من صحة JSON
const validateJson = (val) => {
  if (!val) return 'مطلوب';
  try {
    JSON.parse(val);
    jsonError.value = '';
    return true;
  } catch (e) {
    jsonError.value = 'تنسيق JSON غير صالح';
    return 'تنسيق JSON غير صالح';
  }
};

const closeDialog = () => {
  dialog.value = false;
};

const save = async () => {
  const { valid } = await form.value.validate();
  if (!valid) return;
  
  try {
    const parsedJson = JSON.parse(jsonString.value);
    formData.value.query_config = parsedJson;
  } catch (e) {
    jsonError.value = 'تنسيق JSON غير صالح';
    return;
  }

  isSaving.value = true;
  try {
    emit('saved', { ...formData.value });
  } finally {
    isSaving.value = false;
  }
};
</script>

<style scoped>
.font-monospace :deep(textarea) {
  font-family: monospace !important;
  font-size: 14px;
}
</style>
