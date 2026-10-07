<template>
  <div class="image-uploader">
    <!-- عرض الصور المرفوعة -->
    <div class="uploaded-images" v-if="images.length > 0">
      <div
        v-for="(image, index) in images"
        :key="index"
        class="image-preview"
      >
        <img :src="image.url" :alt="image.name" />
        <div class="image-overlay">
          <button
            @click="removeImage(index)"
            class="remove-btn"
            type="button"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- زر رفع الصور -->
    <button
      @click="openDialog"
      class="upload-trigger"
      :class="{ 'has-images': images.length > 0 }"
      type="button"
    >
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
        <circle cx="8.5" cy="8.5" r="1.5"></circle>
        <polyline points="21,15 16,10 5,21"></polyline>
      </svg>
      <span v-if="images.length === 0">اختر الصور</span>
      <span v-else>إضافة المزيد</span>
    </button>

    <!-- حوار رفع الصور -->
    <div v-if="showDialog" class="dialog-overlay" @click="closeDialog">
      <div class="dialog" @click.stop>
        <div class="dialog-header">
          <h3>رفع الصور</h3>
          <button @click="closeDialog" class="close-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="dialog-content">
          <!-- منطقة السحب والإفلات -->
          <div
            class="drop-zone"
            :class="{ 'drag-over': isDragOver }"
            @drop="handleDrop"
            @dragover.prevent="isDragOver = true"
            @dragleave="isDragOver = false"
            @click="triggerFileInput"
          >
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17,8 12,3 7,8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            <p>اسحب الصور هنا أو انقر للاختيار</p>
            <p class="hint">يدعم JPG, PNG, GIF حتى 10MB</p>
          </div>

          <!-- حقل اختيار الملفات المخفي -->
          <input
            ref="fileInput"
            type="file"
            multiple
            accept="image/*"
            @change="handleFileSelect"
            style="display: none;"
          />

          <!-- معاينة الصور المختارة -->
          <div v-if="selectedFiles.length > 0" class="selected-files">
            <h4>الصور المختارة:</h4>
            <div class="file-list">
              <div
                v-for="(file, index) in selectedFiles"
                :key="index"
                class="file-item"
              >
                <img :src="file.preview" :alt="file.name" />
                <div class="file-info">
                  <span class="file-name">{{ file.name }}</span>
                  <span class="file-size">{{ formatFileSize(file.size) }}</span>
                </div>
                <button
                  @click="removeSelectedFile(index)"
                  class="remove-file-btn"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="dialog-footer">
          <button @click="closeDialog" class="btn btn-secondary">إلغاء</button>
          <button
            @click="uploadImages"
            class="btn btn-primary"
            :disabled="selectedFiles.length === 0"
          >
            رفع {{ selectedFiles.length }} صورة
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'

export default {
  name: 'ImageUploader',
  props: {
    maxFiles: {
      type: Number,
      default: 10
    },
    maxFileSize: {
      type: Number,
      default: 10 * 1024 * 1024 // 10MB
    },
    acceptedTypes: {
      type: Array,
      default: () => ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    }
  },
  emits: ['update:images', 'upload', 'remove'],
  setup(props, { emit }) {
    const images = ref([])
    const selectedFiles = ref([])
    const showDialog = ref(false)
    const isDragOver = ref(false)
    const fileInput = ref(null)

    const openDialog = () => {
      showDialog.value = true
      selectedFiles.value = []
    }

    const closeDialog = () => {
      showDialog.value = false
      selectedFiles.value = []
      isDragOver.value = false
    }

    const triggerFileInput = () => {
      fileInput.value?.click()
    }

    const handleFileSelect = (event) => {
      const files = Array.from(event.target.files)
      processFiles(files)
    }

    const handleDrop = (event) => {
      event.preventDefault()
      isDragOver.value = false
      const files = Array.from(event.dataTransfer.files)
      processFiles(files)
    }

    const processFiles = (files) => {
      const validFiles = files.filter(file => {
        // فحص نوع الملف
        if (!props.acceptedTypes.includes(file.type)) {
          alert(`نوع الملف ${file.name} غير مدعوم`)
          return false
        }

        // فحص حجم الملف
        if (file.size > props.maxFileSize) {
          alert(`حجم الملف ${file.name} كبير جداً`)
          return false
        }

        return true
      })

      // فحص العدد الأقصى للملفات
      const totalFiles = images.value.length + selectedFiles.value.length + validFiles.length
      if (totalFiles > props.maxFiles) {
        alert(`لا يمكن رفع أكثر من ${props.maxFiles} صورة`)
        return
      }

      // إنشاء معاينة للصور
      validFiles.forEach(file => {
        const reader = new FileReader()
        reader.onload = (e) => {
          selectedFiles.value.push({
            file,
            name: file.name,
            size: file.size,
            preview: e.target.result
          })
        }
        reader.readAsDataURL(file)
      })
    }

    const removeSelectedFile = (index) => {
      selectedFiles.value.splice(index, 1)
    }

    const uploadImages = () => {
      // محاكاة رفع الصور
      selectedFiles.value.forEach(fileData => {
        const imageData = {
          id: Date.now() + Math.random(),
          name: fileData.name,
          size: fileData.size,
          url: fileData.preview,
          file: fileData.file
        }
        images.value.push(imageData)
      })

      emit('update:images', images.value)
      emit('upload', selectedFiles.value.map(f => f.file))
      closeDialog()
    }

    const removeImage = (index) => {
      const removedImage = images.value.splice(index, 1)[0]
      emit('update:images', images.value)
      emit('remove', removedImage)
    }

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    return {
      images,
      selectedFiles,
      showDialog,
      isDragOver,
      fileInput,
      openDialog,
      closeDialog,
      triggerFileInput,
      handleFileSelect,
      handleDrop,
      removeSelectedFile,
      uploadImages,
      removeImage,
      formatFileSize
    }
  }
}
</script>

<style scoped>
.image-uploader {
  position: relative;
  width: 100%;
  padding: 10px;
}

.uploaded-images {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.image-preview {
  position: relative;
  width: 60px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #e1e5e9;
  transition: all 0.2s ease;
}

.image-preview:hover {
  border-color: #3b82f6;
  transform: scale(1.05);
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.image-preview:hover .image-overlay {
  opacity: 1;
}

.remove-btn {
  background: #ef4444;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.remove-btn:hover {
  background: #dc2626;
}

.upload-trigger {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  /* padding: 12px 16px; */
  border: 2px outset #d1d5db;
  border-radius: 8px;
  background: transparent;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  min-height: 40px;
  width: 100%;
}

.upload-trigger:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.05);
}

.upload-trigger.has-images {
  border-style: solid;
  background: #f8fafc;
  border-color: #e2e8f0;
}

.upload-trigger.has-images:hover {
  background: #f1f5f9;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.dialog {
  background: white;
  border-radius: 12px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.dialog-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  color: #6b7280;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.dialog-content {
  padding: 24px;
  flex: 1;
  overflow-y: auto;
}

.drop-zone {
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #fafafa;
}

.drop-zone:hover,
.drop-zone.drag-over {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.05);
}

.drop-zone svg {
  color: #9ca3af;
  margin-bottom: 16px;
}

.drop-zone p {
  margin: 8px 0;
  color: #374151;
  font-weight: 500;
}

.drop-zone .hint {
  color: #6b7280;
  font-size: 14px;
  font-weight: 400;
}

.selected-files {
  margin-top: 24px;
}

.selected-files h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #f9fafb;
}

.file-item img {
  width: 48px;
  height: 48px;
  object-fit: cover;
  border-radius: 6px;
}

.file-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.file-name {
  font-weight: 500;
  color: #111827;
  font-size: 14px;
}

.file-size {
  color: #6b7280;
  font-size: 12px;
}

.remove-file-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  color: #ef4444;
  transition: all 0.2s ease;
}

.remove-file-btn:hover {
  background: rgba(239, 68, 68, 0.1);
}

.dialog-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.btn {
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  font-size: 14px;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

/* تصميم متجاوب */
@media (max-width: 640px) {
  .dialog {
    margin: 10px;
    max-height: calc(100vh - 20px);
  }

  .dialog-header,
  .dialog-content,
  .dialog-footer {
    padding: 16px;
  }

  .drop-zone {
    padding: 30px 15px;
  }

  .uploaded-images {
    gap: 6px;
  }

  .image-preview {
    width: 50px;
    height: 50px;
  }

  .file-item {
    padding: 8px;
  }

  .file-item img {
    width: 40px;
    height: 40px;
  }
}

/* تصميم للجداول */
.image-uploader.table-mode {
  max-width: 200px;
}

.image-uploader.table-mode .uploaded-images {
  max-height: 60px;
  overflow-x: auto;
  overflow-y: hidden;
  flex-wrap: nowrap;
  padding-bottom: 4px;
}

.image-uploader.table-mode .image-preview {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
}

.image-uploader.table-mode .upload-trigger {
  padding: 8px 12px;
  font-size: 12px;
  min-height: 36px;
}
</style>

