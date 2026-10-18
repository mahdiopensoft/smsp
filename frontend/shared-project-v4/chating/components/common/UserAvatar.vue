<template>
  <div class="user-avatar-wrapper" :style="wrapperStyle">
    <v-avatar :color="avatarColor" :size="size">
      <v-img v-if="finalSrc" :alt="name" cover :src="finalSrc" />
      <span v-else class="text-white font-weight-medium" :style="initialsStyle">
        {{ initials }}
      </span>
    </v-avatar>

    <!-- مؤشر الحالة -->
    <span v-if="showStatus" class="avatar-status" :class="statusClass" />
  </div>
</template>

<script setup>
  import { computed } from 'vue'

  const props = defineProps({
    src: {
      type: String,
      default: null,
    },
    name: {
      type: String,
      default: '',
    },
    size: {
      type: [Number, String],
      default: 48,
    },
    isOnline: {
      type: Boolean,
      default: false,
    },
    showStatus: {
      type: Boolean,
      default: false,
    },
  })

  // معالجة رابط الصورة (إضافة الـ Base URL إذا كان مسار نسبي)
  const finalSrc = computed(() => {
    if (!props.src) return null
    if (props.src.startsWith('http') || props.src.startsWith('blob:'))
      return props.src

    // استخراج الدومين الأساسي من رابط الـ API
    const apiUrl = import.meta.env.VITE_API_URL || window.location.origin + '/api'
    try {
      const url = new URL(apiUrl)
      return `${url.origin}${props.src}`
    } catch {
      return props.src
    }
  })

  // الأحرف الأولى من الاسم
  const initials = computed(() => {
    if (!props.name) return '?'
    const parts = props.name.trim().split(' ')
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase()
    }
    return props.name.slice(0, 2).toUpperCase()
  })

  // لون الخلفية بناءً على الاسم
  const avatarColor = computed(() => {
    if (finalSrc.value) return undefined
    const colors = [
      'rgb(var(--v-theme-primary))',
      '#53bdeb',
      '#7d57c1',
      '#ff6f61',
      '#ffb400',
      '#25d366',
      '#128c7e',
      '#075e54',
    ]
    const hash = props.name
      .split('')
      .reduce((acc, char) => acc + char.charCodeAt(0), 0)
    return colors[hash % colors.length]
  })

  // حجم النص
  const initialsStyle = computed(() => ({
    fontSize: `${Number.parseInt(props.size) / 2.5}px`,
  }))

  // ستايل الـ wrapper
  const wrapperStyle = computed(() => ({
    position: 'relative',
    display: 'inline-flex',
    width: `${props.size}px`,
    height: `${props.size}px`,
  }))

  // كلاس مؤشر الحالة
  const statusClass = computed(() => ({
    'avatar-status--online': props.isOnline,
    'avatar-status--offline': !props.isOnline,
  }))
</script>

<style scoped>
.user-avatar-wrapper {
  flex-shrink: 0;
}

.avatar-status {
  position: absolute;
  bottom: 2px;
  inset-inline-end: 2px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid var(--wa-sidebar);
}

.avatar-status--online {
  background-color: var(--wa-primary);
}

.avatar-status--offline {
  background-color: var(--wa-text-secondary);
}
</style>
