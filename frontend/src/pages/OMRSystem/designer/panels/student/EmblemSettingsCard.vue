<template>
  <div class="emblem-settings-card pa-4 rounded-xl border bg-surface mb-4">
    <!-- Header with Toggle -->
    <div class="d-flex align-center justify-space-between mb-3">
      <div>
        <label class="text-subtitle-2 font-weight-bold d-flex align-center gap-2">
          <v-icon color="primary" size="20">mdi-shield-star-outline</v-icon>
          شعار وختم المؤسسة (طير الجمهورية / شعار الجامعة / شعار المعهد)
        </label>
        <span class="text-caption text-medium-emphasis">
          تخصيص الشعار في ترويسة الورقة: طير الجمهورية، أو رفع شعار خاص بالجامعة أو المعهد
        </span>
      </div>
      <v-switch
        v-model="showEmblem"
        color="primary"
        hide-details
        density="compact"
      />
    </div>

    <template v-if="showEmblem">
      <!-- Live Emblem Preview Box -->
      <div class="emblem-preview-box pa-3 rounded-lg border mb-3 d-flex align-center gap-3 bg-surface-variant">
        <!-- Thumbnail clickable to trigger file upload -->
        <div
          class="emblem-thumb-frame d-flex align-center justify-center rounded border bg-white overflow-hidden elevation-1 position-relative cursor-pointer"
          style="width: 80px; height: 52px; min-width: 80px;"
          title="انقر لتغيير أو رفع صورة جديدة"
          @click="triggerFileInput"
        >
          <img
            v-if="currentEmblemSrc"
            :src="currentEmblemSrc"
            alt="شعار الترويسة"
            style="max-width: 100%; max-height: 100%; object-fit: contain; padding: 2px;"
          />
          <v-icon v-else color="grey-lighten-1" size="24">mdi-image-off-outline</v-icon>
          <div class="hover-overlay position-absolute fill-height w-100 d-flex align-center justify-center bg-black-opacity">
            <v-icon size="16" color="white">mdi-camera-flip-outline</v-icon>
          </div>
        </div>

        <div class="flex-grow-1 overflow-hidden">
          <div class="d-flex align-center gap-2 mb-1 flex-wrap">
            <span class="text-body-2 font-weight-bold text-truncate">{{ activeEmblemTitle }}</span>
            <v-chip size="x-small" :color="isCustomImageActive ? 'success' : activeEmblemColor" variant="tonal" class="font-weight-bold">
              {{ isCustomImageActive ? 'صورة مخصصة مرفوعة' : activeEmblemBadge }}
            </v-chip>
          </div>
          <p class="text-caption text-medium-emphasis mb-0 text-truncate">
            {{ activeEmblemDescription }}
          </p>
        </div>
      </div>

      <!-- Quick Action Buttons for Changing / Uploading Logo -->
      <div class="d-flex flex-wrap align-center gap-2 mb-3">
        <input
          ref="fileInputRef"
          type="file"
          accept="image/png, image/jpeg, image/svg+xml, image/webp"
          class="d-none"
          @change="handleFileUpload"
        />
        <v-btn
          color="primary"
          variant="flat"
          rounded="lg"
          size="small"
          prepend-icon="mdi-cloud-upload-outline"
          class="font-weight-bold"
          @click="triggerFileInput"
        >
          رفع صورة الشعار (PNG / SVG / JPG)
        </v-btn>

        <v-btn
          v-if="isCustomImageActive"
          size="small"
          variant="outlined"
          color="warning"
          prepend-icon="mdi-restore"
          class="font-weight-bold"
          @click="resetToDefaultSeal"
        >
          استعادة الختم الافتراضي
        </v-btn>

        <v-btn
          size="small"
          variant="text"
          color="medium-emphasis"
          prepend-icon="mdi-link-variant"
          @click="showUrlInput = !showUrlInput"
        >
          {{ showUrlInput ? 'إخفاء رابط الصورة' : 'إدخال رابط URL للصورة' }}
        </v-btn>
      </div>

      <!-- Optional URL Input Field -->
      <div v-if="showUrlInput" class="mb-3">
        <v-text-field
          v-model="logoUrlInput"
          label="رابط صورة الشعار المباشر (URL أو Base64)"
          placeholder="https://example.com/logo.png أو /logo.png"
          variant="outlined"
          density="compact"
          rounded="lg"
          hide-details
          prepend-inner-icon="mdi-image-outline"
          append-inner-icon="mdi-check"
          @click:append-inner="applyLogoUrl"
          @keydown.enter="applyLogoUrl"
        />
      </div>

      <!-- Emblem Type Selection Buttons -->
      <div class="mb-2">
        <label class="text-caption font-weight-bold text-medium-emphasis mb-1.5 d-block">
          أو اختر من النماذج المعتمدة الجاهزة:
        </label>
        <div class="d-flex flex-wrap gap-2">
          <v-btn
            v-for="opt in EMBLEM_OPTIONS"
            :key="opt.id"
            size="small"
            :variant="selectedType === opt.id ? 'flat' : 'outlined'"
            :color="selectedType === opt.id ? 'primary' : undefined"
            rounded="lg"
            class="font-weight-bold flex-grow-1"
            style="min-width: 105px;"
            @click="selectEmblem(opt.id)"
          >
            <v-icon start size="16">{{ opt.icon }}</v-icon>
            {{ opt.shortName }}
          </v-btn>
        </div>
      </div>

      <div class="text-caption text-medium-emphasis mt-2">
        <v-icon size="14" color="info" class="me-1">mdi-information-outline</v-icon>
        يمكنك في أي وقت رفع شعار خاص بالجامعة أو المعهد (PNG أو SVG بخلفية مفرغة)، وسيتم تضمينه في ورقة الإجابة والطباعة آلياً.
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  EMBLEM_OPTIONS,
  resolveEmblemSrc,
  type EmblemOption,
} from '@/assets/omrEmblems'

const props = defineProps<{
  config: any
  institutionType?: string
}>()

const fileInputRef = ref<HTMLInputElement | null>(null)
const showUrlInput = ref<boolean>(false)
const logoUrlInput = ref<string>('')

const showEmblem = computed<boolean>({
  get: () => props.config?.header?.show_emblem !== false,
  set: (val: boolean) => {
    if (props.config?.header) {
      props.config.header.show_emblem = val
    }
  },
})

const selectedType = computed<string>({
  get: () => props.config?.header?.emblem_type || 'republic_eagle',
  set: (val: string) => {
    if (props.config?.header) {
      props.config.header.emblem_type = val
    }
  },
})

// Current custom logo for current profile (completely isolated per institution type)
const currentCustomLogo = computed<string>({
  get: () => {
    const h = props.config?.header
    if (!h) return ''
    if (selectedType.value === 'university_seal') {
      return h.university_logo || ''
    }
    if (selectedType.value === 'institute_seal') {
      return h.institute_logo || ''
    }
    if (selectedType.value === 'republic_eagle') {
      return h.school_logo || ''
    }
    return h.custom_logo || ''
  },
  set: (val: string) => {
    if (!props.config?.header) return
    if (selectedType.value === 'university_seal') {
      props.config.header.university_logo = val
    } else if (selectedType.value === 'institute_seal') {
      props.config.header.institute_logo = val
    } else if (selectedType.value === 'republic_eagle') {
      props.config.header.school_logo = val
    } else {
      props.config.header.custom_logo = val
    }
  },
})

const isCustomImageActive = computed<boolean>(() => {
  return !!currentCustomLogo.value && currentCustomLogo.value.trim() !== ''
})

const activeEmblemOption = computed<EmblemOption>(() => {
  const found = EMBLEM_OPTIONS.find((o) => o.id === selectedType.value)
  return found || EMBLEM_OPTIONS[0]
})

const currentEmblemSrc = computed<string>(() => {
  if (!showEmblem.value) return ''
  return resolveEmblemSrc(
    selectedType.value,
    currentCustomLogo.value,
    {
      university: props.config?.header?.university_logo,
      institute: props.config?.header?.institute_logo,
      school: props.config?.header?.school_logo,
    },
    props.institutionType || props.config?.institution_type
  )
})

const activeEmblemTitle = computed<string>(() => {
  if (isCustomImageActive.value) {
    if (selectedType.value === 'university_seal') return 'شعار مخصص للجامعة'
    if (selectedType.value === 'institute_seal') return 'شعار مخصص للمعهد'
    if (selectedType.value === 'republic_eagle') return 'شعار مخصص للمدرسة'
    return 'شعار مخصص تم رفعه'
  }
  return activeEmblemOption.value.name
})

const activeEmblemDescription = computed<string>(() => {
  if (isCustomImageActive.value) {
    return 'تم رفع صورة مخصصة للشعار من جهازك، وهي معتمدة الآن في ورقة الإجابة.'
  }
  return activeEmblemOption.value.description
})

const activeEmblemColor = computed<string>(() => {
  if (selectedType.value === 'republic_eagle') return 'primary'
  if (selectedType.value === 'university_seal') return 'purple'
  if (selectedType.value === 'institute_seal') return 'teal'
  if (selectedType.value === 'custom') return 'success'
  return 'grey'
})

const activeEmblemBadge = computed<string>(() => {
  if (selectedType.value === 'republic_eagle') return 'طير الجمهورية'
  if (selectedType.value === 'university_seal') return 'ختم الجامعة'
  if (selectedType.value === 'institute_seal') return 'ختم المعهد'
  if (selectedType.value === 'custom') return 'مخصص'
  return 'مخفي'
})

function selectEmblem(optId: string) {
  selectedType.value = optId
}

function triggerFileInput() {
  fileInputRef.value?.click()
}

function handleFileUpload(e: Event) {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (uploadEvent) => {
    const result = uploadEvent.target?.result as string
    if (result) {
      currentCustomLogo.value = result
      // Keep user on their chosen institution type while applying their custom image!
      if (selectedType.value === 'none') {
        selectedType.value = 'custom'
      }
    }
  }
  reader.readAsDataURL(file)
}

function applyLogoUrl() {
  if (logoUrlInput.value && logoUrlInput.value.trim() !== '') {
    currentCustomLogo.value = logoUrlInput.value.trim()
  }
}

function resetToDefaultSeal() {
  if (props.config?.header) {
    if (selectedType.value === 'university_seal') {
      props.config.header.university_logo = ''
    } else if (selectedType.value === 'institute_seal') {
      props.config.header.institute_logo = ''
    } else if (selectedType.value === 'republic_eagle') {
      props.config.header.school_logo = ''
    } else {
      props.config.header.custom_logo = ''
    }
  }
}
</script>

<style scoped>
.hover-overlay {
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
}
.emblem-thumb-frame:hover .hover-overlay {
  opacity: 0.75;
}
.bg-black-opacity {
  background: rgba(0, 0, 0, 0.6);
}
</style>
