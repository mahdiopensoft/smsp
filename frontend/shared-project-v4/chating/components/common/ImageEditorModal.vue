<template>
  <v-dialog v-model="dialog" fullscreen style="z-index: 9999;" transition="dialog-bottom-transition">
    <div
      class="editor-wrapper"
      style="height: 100vh; width: 100vw; background: #1e1e1e; display: flex; flex-direction: column;"
    >

      <!-- Toolbar Header -->
      <div class="d-flex align-center justify-space-between pa-2 bg-grey-darken-4">
        <v-btn color="white" icon="mdi-close" variant="text" @click="closeData" />
        <span class="text-white font-weight-bold">تحرير الصورة</span>
        <v-btn color="primary" @click="saveImage">حفظ</v-btn>
      </div>

      <!-- TUI Editor Container -->
      <div id="tui-image-editor-container" style="flex: 1; width: 100%; height: 100%; background-color: #1e1e1e;" />

    </div>
  </v-dialog>
</template>

<script setup>
  import ImageEditor from 'tui-image-editor'
  import { nextTick, onBeforeUnmount, ref, watch } from 'vue'
  import 'tui-image-editor/dist/tui-image-editor.css'

  // Override some icons/styles if needed, or stick to default

  const props = defineProps({
    modelValue: {
      type: Boolean,
      default: false,
    },
    imageFile: {
      type: [File, Blob, String],
      default: null,
    },
  })

  const emit = defineEmits(['update:modelValue', 'save', 'close'])

  const dialog = ref(props.modelValue)
  let imageEditorInstance = null

  watch(
    () => props.modelValue,
    val => {
      dialog.value = val
      if (val && props.imageFile) {
        nextTick(() => {
          initEditor()
        })
      } else {
        destroyEditor()
      }
    },
  )

  watch(
    () => dialog.value,
    val => {
      emit('update:modelValue', val)
      if (!val) {
        destroyEditor()
        emit('close')
      }
    },
  )

  function initEditor () {
    let imgUrl = ''
    if (props.imageFile instanceof File || props.imageFile instanceof Blob) {
      imgUrl = URL.createObjectURL(props.imageFile)
    } else if (typeof props.imageFile === 'string') {
      imgUrl = props.imageFile
    }

    if (!imgUrl) return

    const container = document.querySelector('#tui-image-editor-container')
    if (!container) return

    // Clear just in case
    container.innerHTML = ''

    try {
      imageEditorInstance = new ImageEditor(container, {
        includeUI: {
          loadImage: {
            path: imgUrl,
            name: 'SampleImage',
          },
          theme: {
            // Basic Dark Theme Customization
            'common.backgroundColor': '#1e1e1e',
            'header.display': 'none', // Hide default header, we used our own
            'downloadButton.display': 'none',
            'loadButton.display': 'none',
          },
          menu: ['crop', 'flip', 'rotate', 'draw', 'shape', 'icon', 'text', 'filter'],
          initMenu: 'filter',
          uiSize: {
            width: '100%',
            height: '100%',
          },
          menuBarPosition: 'bottom',
        },
        cssMaxWidth: 700,
        cssMaxHeight: 500,
        selectionStyle: {
          cornerSize: 20,
          rotatingPointOffset: 70,
        },
      })

      // Workaround to resize properly
      window.addEventListener('resize', () => {
        imageEditorInstance?.ui.resizeEditor()
      })
    } catch (error) {
      console.error('Failed to init TUI Image Editor', error)
    }
  }

  function saveImage () {
    if (!imageEditorInstance) return

    // Get Data URL
    const dataUrl = imageEditorInstance.toDataURL()

    // Convert to File
    fetch(dataUrl)
      .then(res => res.blob())
      .then(blob => {
        const file = new File([blob], (props.imageFile?.name || 'edited-image.png'), { type: blob.type })
        emit('save', file)
        dialog.value = false
      })
  }

  function destroyEditor () {
    if (imageEditorInstance) {
      imageEditorInstance.destroy()
      imageEditorInstance = null
    }
  }

  function closeData () {
    dialog.value = false
  }

  onBeforeUnmount(() => {
    destroyEditor()
  })
</script>

<style scoped>
.editor-wrapper {
  position: relative;
  overflow: hidden;
}

/* Force dark mode overrides for TUI internal elements if needed */
:deep(.tui-image-editor-container) {
  background-color: #1e1e1e !important;
}

:deep(.tui-image-editor-main-container) {
  background-color: #1e1e1e !important;
}
</style>
