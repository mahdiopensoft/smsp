<template>
  <custom-dialog v-model="internalModelValue" title="إنشاء تعميم إداري جديد" width="720" height="auto">
    <template #default>
        <v-form ref="form" v-model="isValid" @submit.prevent="submitGeneralization">

          <custom-text-field v-model="formData.title" label="عنوان التعميم" :rules="[$required]" icon="format-title" />

          <custom-text-note v-model="formData.content" label="تفاصيل ونص التعميم" :rules="[$required]"
            icon="text-box-outline"></custom-text-note>

          <v-row class="mb-4">
            <v-col cols="12" md="6" class="py-1">
              <v-card variant="flat" class="pa-3 border border-dashed rounded-lg bg-surface d-flex align-center h-100">
                <v-switch v-model="formData.allow_replies" label="السماح للمستلمين بالرد على هذا التعميم"
                  color="primary" hide-details class="font-weight-bold text-body-2 text-high-emphasis"></v-switch>
              </v-card>
            </v-col>
            <custom-file v-model="fileInput" label="إرفاق ملف أو مستند (اختياري)" icon="paperclip"
              cols="6" multiple accept=".pdf,.doc,.docx,.xls,.xlsx,image/jpeg,image/png,image/jpg" :rules="[fileSizeRule]"></custom-file>
          </v-row>

          <!-- Targeting Options Section -->
          <v-card variant="flat" class="rounded-xl border mt-6 bg-surface overflow-hidden" elevation="0">
            <div class="targeting-header py-3 px-5 d-flex align-center bg-background">
              <v-icon icon="mdi-account-group-outline" class="me-2 text-primary" size="20"></v-icon>
              <span class="text-subtitle-2 font-weight-bold text-high-emphasis">تحديد الجمهور المستهدف</span>
            </div>

            <v-card-text class="pa-5">
              <v-row>
                <auto-list v-model="formData.target_company_levels" name="CompanyLevelFilterChoices"
                  :param="companyLevelParam" item-title="name" item-value="id" label="المستويات الإدارية المستهدفة"
                  cols="6" multiple></auto-list>

                <auto-list v-model="formData.target_user_types" name="UserType" label="فئات المستخدمين المستهدفة"
                  item-title="name_ar" item-value="id" cols="6" multiple></auto-list>
              </v-row>
            </v-card-text>
          </v-card>
        </v-form>
    </template>

    <template #actions>
      <div class="d-flex justify-space-between w-100">
        <v-btn variant="outlined" color="grey-darken-1" @click="closeDialog" :disabled="loading"
          class="rounded-lg px-6 font-weight-bold text-body-2">
          إلغاء
        </v-btn>

        <v-btn color="primary" variant="flat" prepend-icon="mdi-send-variant" :loading="loading" :disabled="!isValid"
          @click="submitGeneralization" class="rounded-lg px-6 font-weight-bold text-body-2 shadow-sm">
          إرسال وبث التعميم
        </v-btn>
      </div>
    </template>
  </custom-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import api from "../../../plugins/axios-plugin";
import { useGeneralizationStore } from "../../store/generalizationStore";
import { useAuthStore } from "../../../src/UserManagement/stores/auth";

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue']);
const genStore = useGeneralizationStore();

const internalModelValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
});

watch(() => props.modelValue, (newVal) => {
  if (!newVal) {
    resetForm();
  }
});

const form = ref(null);
const isValid = ref(false);
const loading = ref(false);

const authStore = useAuthStore();

const companyLevelParam = computed(() => ({
  company_level: authStore.user?.profile?.company_level || authStore.user?.company_level || 1,
  isEdit: true
}));

const fileInput = ref(null);

const fileSizeRule = (files) => {
  if (!files || !files.length) return true;
  const maxSize = 10 * 1024 * 1024; // 10MB
  for (let i = 0; i < files.length; i++) {
    if (files[i].size > maxSize) {
      return `حجم الملف ${files[i].name} يجب أن لا يتجاوز 10 ميجابايت`;
    }
  }
  return true;
};

const formData = ref({
  title: '',
  content: '',
  allow_replies: false,
  target_company_levels: [],
  target_user_types: []
});

const resetForm = () => {
  formData.value = {
    title: '',
    content: '',
    allow_replies: false,
    target_company_levels: [],
    target_user_types: []
  };
  fileInput.value = null;
  if (form.value) {
    form.value.resetValidation();
  }
};

const closeDialog = () => {
  internalModelValue.value = false;
  resetForm();
};

const submitGeneralization = async () => {
  if (!isValid.value) return;

  loading.value = true;
  try {
    const submitData = new FormData();
    submitData.append('title', formData.value.title);
    submitData.append('content', formData.value.content);
    submitData.append('allow_replies', formData.value.allow_replies);

    if (formData.value.target_company_levels.length > 0) {
      const levelsStr = ',' + formData.value.target_company_levels.join(',') + ',';
      submitData.append('target_company_levels', levelsStr);
    } else {
      submitData.append('target_company_levels', '');
    }

    if (formData.value.target_user_types.length > 0) {
      formData.value.target_user_types.forEach(ut => {
        submitData.append('target_user_types', ut);
      });
    }

    if (fileInput.value) {
      if (Array.isArray(fileInput.value) && fileInput.value.length > 0) {
        fileInput.value.forEach(file => {
          submitData.append('attachments', file);
        });
      } else if (fileInput.value instanceof File) {
        submitData.append('attachments', fileInput.value);
      }
    }

    await api.post('/chat/generalizations/', submitData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    genStore.fetchGeneralizations();
    genStore.fetchUnreadGeneralizations();
    closeDialog();
  } catch (err) {
    console.error("Error submitting generalization", err);
  } finally {
    loading.value = false;
  }
};

</script>

<style scoped>
.dialog-card {
  border: 1px solid rgba(var(--v-border-color), 0.12);
}

.header-gradient {
  background: rgb(var(--v-theme-primary));
  background-image: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(0, 0, 0, 0.18) 100%);
}

.icon-pulse-wrapper {
  background: rgba(255, 255, 255, 0.15);
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.close-btn {
  background: rgba(255, 255, 255, 0.1) !important;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.25) !important;
  transform: scale(1.05);
}

.section-title {
  display: flex;
  align-items: center;
  border-bottom: 2px solid rgba(var(--v-theme-primary), 0.15);
  padding-bottom: 8px;
}

.border-dashed {
  border: 1px dashed rgba(var(--v-border-color), 0.3) !important;
}

.bg-slate-50 {
  background-color: rgb(var(--v-theme-background)) !important;
}

.custom-field :deep(.v-field) {
  border-radius: 12px !important;
  background-color: rgb(var(--v-theme-surface)) !important;
  transition: all 0.2s ease;
}

.custom-field :deep(.v-field:hover) {
  border-color: rgba(var(--v-theme-primary), 0.4) !important;
}

.targeting-header {
  border-bottom: 1px solid rgba(var(--v-border-color), 0.12);
}

.shadow-sm {
  box-shadow: 0 2px 4px rgba(var(--v-theme-primary), 0.04);
}
</style>
