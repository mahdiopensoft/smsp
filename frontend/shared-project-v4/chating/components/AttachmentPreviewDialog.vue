<template>
  <v-dialog v-model="dialog" max-width="900" transition="dialog-bottom-transition">
    <v-card class="rounded-xl overflow-hidden shadow-lg border">
      <v-toolbar color="primary" class="px-2" elevation="1">
        <v-icon icon="mdi-file-eye-outline" class="me-2"></v-icon>
        <v-toolbar-title class="font-weight-bold text-white text-subtitle-1">{{ fileName || 'معاينة الملف' }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon variant="text" color="white" @click="promptDownload" class="me-2">
          <v-icon>mdi-download</v-icon>
          <v-tooltip activator="parent" location="bottom">تحميل الملف</v-tooltip>
        </v-btn>
        <v-btn icon variant="text" color="white" @click="dialog = false">
          <v-icon>mdi-close</v-icon>
          <v-tooltip activator="parent" location="bottom">إغلاق</v-tooltip>
        </v-btn>
      </v-toolbar>

      <v-card-text class="pa-0 bg-grey-lighten-4 d-flex align-center justify-center" style="min-height: 500px; position: relative;">
        <!-- Loading State -->
        <v-progress-circular v-if="loading" indeterminate color="primary" size="64" class="position-absolute" style="z-index: 1;"></v-progress-circular>
        
        <!-- Image Preview -->
        <v-img 
          v-if="isImage" 
          :src="fileUrl" 
          contain 
          max-height="700" 
          width="100%"
          @load="loading = false"
          @error="handleError"
        ></v-img>
        
        <!-- PDF / Video / Text Preview -->
        <iframe 
          v-else-if="isPreviewable" 
          :src="fileUrl" 
          width="100%" 
          style="height: 75vh; border: none;"
          @load="loading = false"
          @error="handleError"
        ></iframe>

        <!-- Fallback for unsupported files -->
        <div v-else-if="!loading" class="text-center pa-8">
          <v-icon size="80" color="grey-darken-1" class="mb-4">mdi-file-download-outline</v-icon>
          <h3 class="text-h6 text-grey-darken-3 mb-2">لا يمكن معاينة هذا النوع من الملفات</h3>
          <p class="text-body-2 text-grey-darken-1 mb-6">هذا الملف يتطلب تطبيقاً خارجياً لفتحه، يرجى تحميله على جهازك.</p>
          <v-btn color="primary" prepend-icon="mdi-download" @click="promptDownload" rounded="lg" size="large" class="px-8 font-weight-bold shadow-sm">
            تحميل الملف
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Rename Dialog -->
  <v-dialog v-model="showRenameDialog" max-width="450" transition="dialog-transition">
    <v-card class="rounded-xl border shadow-lg">
      <v-card-title class="font-weight-bold pt-4 text-h6 d-flex align-center">
        <v-icon color="primary" class="me-2">mdi-rename-box</v-icon>
        تحميل الملف
      </v-card-title>
      <v-card-text class="pt-2">
        <p class="text-body-2 text-medium-emphasis mb-4">يمكنك تغيير اسم الملف قبل التحميل أو تركه كما هو.</p>
        <v-text-field 
          v-model="customFileName" 
          label="اسم الملف" 
          variant="outlined" 
          density="comfortable" 
          color="primary"
          @keyup.enter="confirmDownload"
        ></v-text-field>
      </v-card-text>
      <v-card-actions class="pa-4 pt-0">
        <v-spacer></v-spacer>
        <v-btn color="grey-darken-1" variant="text" @click="showRenameDialog = false" class="font-weight-bold">إلغاء</v-btn>
        <v-btn color="primary" variant="flat" @click="confirmDownload" :loading="isDownloading" class="px-6 rounded-lg font-weight-bold shadow-sm">
          تحميل الآن
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  modelValue: Boolean,
  fileUrl: String,
  fileName: {
    type: String,
    default: 'ملف مرفق'
  }
});

const emit = defineEmits(['update:modelValue']);

const dialog = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
});

const loading = ref(true);

watch(dialog, (val) => {
  if (val) {
    loading.value = true;
    if (!isImage.value && !isPreviewable.value) {
      loading.value = false;
    }
  }
});

const fileExtension = computed(() => {
  if (!props.fileUrl) return '';
  const parts = props.fileUrl.split(/[#?]/)[0].split('.');
  return parts.length > 1 ? parts[parts.length - 1].toLowerCase() : '';
});

const isImage = computed(() => {
  return ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp'].includes(fileExtension.value);
});

const isPreviewable = computed(() => {
  // Browsers natively support PDF, and most text/video formats
  return ['pdf', 'txt', 'mp4', 'webm', 'ogg', 'mp3', 'wav'].includes(fileExtension.value);
});

const handleError = () => {
  loading.value = false;
};

// Rename state
const showRenameDialog = ref(false);
const customFileName = ref('');
const isDownloading = ref(false);

const promptDownload = () => {
  // Remove extension for the input box if we want, or keep it. 
  // We'll just show the base name
  let name = props.fileName || 'attachment';
  if (fileExtension.value && name.toLowerCase().endsWith(`.${fileExtension.value}`)) {
    name = name.substring(0, name.length - fileExtension.value.length - 1);
  }
  customFileName.value = name;
  showRenameDialog.value = true;
};

const confirmDownload = async () => {
  let finalName = customFileName.value.trim() || 'attachment';
  if (fileExtension.value && !finalName.toLowerCase().endsWith(`.${fileExtension.value}`)) {
    finalName += `.${fileExtension.value}`;
  }

  isDownloading.value = true;
  try {
    const response = await fetch(props.fileUrl);
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = finalName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    setTimeout(() => URL.revokeObjectURL(url), 100);
    showRenameDialog.value = false;
  } catch (error) {
    console.error('Download failed:', error);
    // Fallback to normal download
    const link = document.createElement('a');
    link.href = props.fileUrl;
    link.download = finalName;
    link.target = '_blank';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showRenameDialog.value = false;
  } finally {
    isDownloading.value = false;
  }
};
</script>
