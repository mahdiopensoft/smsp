<template>
  <v-dialog
    v-model="dialog"
    class="file-preview-dialog"
    fullscreen
    transition="dialog-bottom-transition"
  >
    <v-card class="bg-black d-flex flex-column" height="100%">
      <!-- Toolbar -->
      <v-toolbar color="transparent" density="compact">
        <v-btn icon @click="close">
          <v-icon color="white">mdi-close</v-icon>
        </v-btn>
        <v-spacer />
        <!-- Edit tool for images -->
        <v-btn
          v-if="fileType === 'image'"
          color="white"
          prepend-icon="mdi-pencil"
          variant="text"
          @click="$emit('edit')"
        >
          تعديل
        </v-btn>
      </v-toolbar>

      <!-- Content Area -->
      <div
        class="flex-grow-1 bg-grey-darken-4 w-100 d-flex align-center justify-center"
        style="overflow: hidden; position: relative;"
      >
        <!-- Image Preview -->
        <img
          v-if="fileType === 'image' && previewUrl"
          alt="Preview"
          :src="previewUrl"
          style="max-width: 100%; max-height: 80vh; object-fit: contain; display: block;"
          @error="(e) => console.error('Image tag error', e)"
          @load="() => {}"
        >

        <!-- Loading Indicator -->
        <div class="app-loader-spinner app-loader--md" v-else-if="!previewUrl && fileType !== 'file'"></div>

        <!-- Video Preview -->
        <video
          v-else-if="fileType === 'video'"
          controls
          :src="previewUrl"
          style="max-width: 100%; max-height: 80vh;"
        />

        <!-- Document Preview -->
        <div
          v-else
          class="d-flex flex-column align-center text-white"
        >
          <v-icon class="mb-4" color="white" size="64">mdi-file-document-outline</v-icon>
          <h3 class=" mb-2">{{ file?.name }}</h3>
          <p class="">{{ formattedSize }}</p>
        </div>
      </div>

      <!-- Caption & Actions -->
      <div class="caption-area pa-2 d-flex align-center gap-2" style="background: rgba(0,0,0,0.5)">
        <v-text-field
          v-model="caption"
          autofocus
          bg-color="grey-darken-3"
          class="rounded-pill"
          color="white"
          density="compact"
          hide-details
          placeholder="أضف شرحاً..."
          variant="solo"
          @keydown.enter="send"
        >
          <template #prepend-inner>
            <v-icon color="grey-lighten-1">mdi-plus-box</v-icon>
          </template>
        </v-text-field>

        <v-btn
          class="send-btn"
          color="teal-accent-4"
          icon
          :loading="loading"
          size="large"
          @click="send"
        >
          <v-icon color="white">mdi-send</v-icon>
        </v-btn>
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup>
  import { computed, onUnmounted, ref, watch } from 'vue'

  const props = defineProps({
    modelValue: Boolean,
    file: File,
    type: String,
    initialCaption: { type: String, default: '' },
  })

  const emit = defineEmits(['update:modelValue', 'send', 'edit'])

  const dialog = computed({
    get: () => props.modelValue,
    set: val => emit('update:modelValue', val),
  })

  const caption = ref(props.initialCaption)
  const previewUrl = ref('')
  const loading = ref(false)

  const fileType = computed(() => {
    if (!props.file) return 'file'

    // 1. Check MIME type first
    if (props.file.type.startsWith('image/')) return 'image'
    if (props.file.type.startsWith('video/')) return 'video'

    // 2. Check props.type (passed from query) as fallback
    if (!props.file.type && props.type) {
      return props.type
    }

    // 3. Check extension as last resort
    const name = props.file.name.toLowerCase()
    if (/\.(jpg|jpeg|png|gif|webp|bmp)$/.test(name)) return 'image'
    if (/\.(mp4|webm|ogg|mov)$/.test(name)) return 'video'

    return 'file'
  })

  const formattedSize = computed(() => {
    if (!props.file) return ''
    const size = props.file.size
    if (size < 1024) return size + ' B'
    if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB'
    return (size / (1024 * 1024)).toFixed(1) + ' MB'
  })

  // Create preview using FileReader (Data URL) to avoid Blob issues
  watch(() => props.file, newFile => {
    // Clean up previous blob if any (though we are switching to data url, good practice if we mixed)
    if (previewUrl.value && previewUrl.value.startsWith('blob:')) {
      URL.revokeObjectURL(previewUrl.value)
    }

    previewUrl.value = ''

    if (newFile) {
      // For images, use FileReader to get base64
      if (newFile.type.startsWith('image/')) {
        const reader = new FileReader()

        reader.addEventListener('load', e => {
          const result = e.target.result
          previewUrl.value = result
        })

        reader.onerror = e => {
          console.error('FilePreviewDialog: FileReader error', e)
        }

        reader.readAsDataURL(newFile)
      }
      // For videos, Blob URL is usually fine and better for performance
      else {
        const url = URL.createObjectURL(newFile)
        previewUrl.value = url
      }
    }

    caption.value = props.initialCaption // Use initial caption from props
  }, { immediate: true })

  onUnmounted(() => {
    if (previewUrl.value) {
      URL.revokeObjectURL(previewUrl.value)
    }
  })

  function close () {
    dialog.value = false
  }

  function send () {
    emit('send', { file: props.file, type: props.type, caption: caption.value })
    close()
  }
</script>

<style scoped>
.preview-content {
  max-width: 100%;
}
.caption-area {
  padding-bottom: env(safe-area-inset-bottom);
}
</style>
