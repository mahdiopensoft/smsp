<template>
  <v-list-item
    :active="active"
    class="chat-list-item px-3 py-2"
    :class="{ 'chat-list-item--active': active }"
    @click="$emit('click')"
  >
    <!-- صورة المحادثة -->
    <template #prepend>
      <UserAvatar
        class="chat-list-avatar"
        :is-online="otherParticipant?.is_online"
        :name="displayName"
        :show-status="!isGroup"
        :size="50"
        :src="avatarSrc"
      />
    </template>

    <!-- محتوى المحادثة -->
    <v-list-item-title class="d-flex align-center justify-space-between ms-2">
      <span class="chat-name text-truncate font-weight-medium">
        <v-icon v-if="isGroup" class="me-1" size="16" color="primary">mdi-account-group</v-icon>
        {{ displayName }}
      </span>
      <span class="chat-time" :class="timeClass">
        {{ formattedTime }}
      </span>
    </v-list-item-title>

    <v-list-item-subtitle
      class="d-flex align-center justify-space-between mt-1 ms-2"
    >
      <div class="chat-preview d-flex align-center text-truncate">
        <!-- أيقونة حالة الرسالة -->
        <v-icon
          v-if="isOwnMessage && lastMessage"
          class="me-1"
          :color="messageStatusColor"
          size="16"
        >
          {{ messageStatusIcon }}
        </v-icon>

        <!-- معاينة الرسالة -->
        <span
          class="text-truncate"
          :class="{ 'font-weight-medium': hasUnread }"
        >
          {{ messagePreview }}
        </span>
      </div>

      <!-- شارة غير المقروءة وتثبيت -->
      <div class="chat-badges d-flex align-center gap-1 mb-2">
        <v-icon
          v-if="chat.is_muted"
          class="chat-badge-icon"
          color="medium-emphasis"
          size="14"
        >
          mdi-bell-off-outline
        </v-icon>
        <v-icon v-if="chat.is_pinned" color="secondary" size="16">
          mdi-pin
        </v-icon>
        <span v-if="hasUnread" class="unread-badge">
          {{ unreadCount > 99 ? "99+" : unreadCount }}
        </span>
      </div>
    </v-list-item-subtitle>

    <!-- قائمة السياق -->
    <template #append>
      <v-menu :close-on-content-click="true" location="bottom end">
        <template #activator="{ props }">
          <v-btn
            v-bind="props"
            class="chat-menu-btn"
            icon
            size="x-small"
            variant="text"
            @click.stop
          >
            <v-icon size="18">mdi-chevron-down</v-icon>
          </v-btn>
        </template>

        <v-card class="context-menu-card" elevation="8" rounded="lg">
          <v-list bg-color="surface" class="py-1 px-0" density="compact">
            <v-list-item class="context-menu-item" @click="$emit('pin')">
              <template #prepend>
                <v-icon class="me-3" size="20">{{
                  chat.is_pinned ? "mdi-pin-off" : "mdi-pin"
                }}</v-icon>
              </template>
              <v-list-item-title class="">{{
                chat.is_pinned ? "إلغاء التثبيت" : "تثبيت"
              }}</v-list-item-title>
            </v-list-item>

            <v-list-item class="context-menu-item" @click="$emit('archive')">
              <template #prepend>
                <v-icon class="me-3" size="20">{{
                  chat.is_archived
                    ? "mdi-archive-arrow-up-outline"
                    : "mdi-archive-outline"
                }}</v-icon>
              </template>
              <v-list-item-title class="">{{
                chat.is_archived ? "إلغاء الأرشفة" : "أرشفة"
              }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card>
      </v-menu>
    </template>
  </v-list-item>
</template>

<script setup>
  import { computed } from 'vue'
  import UserAvatar from '../../components/common/UserAvatar.vue'

  const props = defineProps({
    chat: {
      type: Object,
      required: true,
    },
    active: {
      type: Boolean,
      default: false,
    },
    unreadCount: {
      type: Number,
      default: 0,
    },
    currentUserId: {
      type: Number,
      default: null,
    },
  })

  defineEmits(['click', 'pin', 'mute', 'archive', 'delete'])

  // هل هي مجموعة؟
  const isGroup = computed(() => props.chat.chat_type === 'group')

  // المشارك الآخر (للمحادثات الخاصة)
  const otherParticipant = computed(() => props.chat.other_participant)

  // اسم المحادثة
  const displayName = computed(() => {
    if (isGroup.value) {
      return props.chat.name || 'مجموعة'
    }
    return (
      (otherParticipant.value?.full_name || (otherParticipant.value?.first_name ? `${otherParticipant.value.first_name}`.trim() : null))
      || otherParticipant.value?.username
      || 'مستخدم'
    )
  })

  // صورة المحادثة
  const avatarSrc = computed(() => {
    if (isGroup.value) {
      return props.chat.group_picture
    }
    return (otherParticipant.value?.profile_picture || otherParticipant.value?.image_user)
  })

  // آخر رسالة
  const lastMessage = computed(() => props.chat.last_message)

  // هل المرسل أنا؟
  const isOwnMessage = computed(() => {
    return lastMessage.value?.sender?.id === props.currentUserId
  })

  // معاينة الرسالة
  const messagePreview = computed(() => {
    if (!lastMessage.value) return 'لا توجد رسائل'

    const content = lastMessage.value.content
    const type = lastMessage.value.message_type

    switch (type) {
      case 'image': {
        return '📷 صورة'
      }
      case 'video': {
        return '🎬 فيديو'
      }
      case 'audio': {
        return '🎤 رسالة صوتية'
      }
      case 'file': {
        return '📎 ملف'
      }
      case 'sticker': {
        return '🎴 ملصق'
      }
      default: {
        if (!content) return ''
        // تنظيف الماركداون للعرض
        let text = content
        // Code blocks
        text = text.replace(/```[\s\S]*?```/g, match => {
          return match.replace(/```/g, '').trim().replace(/\n/g, ' ')
        })
        // Inline code
        text = text.replace(/`([^`]+)`/g, '$1')
        // Bold/Italic
        text = text.replace(/(\*\*|__)(.*?)\1/g, '$2')
        text = text.replace(/(\*|_)(.*?)\1/g, '$2')
        // Strikethrough
        text = text.replace(/~~(.*?)~~/g, '$1')

        return text
      }
    }
  })

  // وقت الرسالة
  const formattedTime = computed(() => {
    if (!lastMessage.value?.created_at) return ''

    const date = new Date(lastMessage.value.created_at)
    const now = new Date()
    const diff = now - date
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))

    if (days === 0) {
      return date.toLocaleTimeString('ar', {
        hour: '2-digit',
        minute: '2-digit',
      })
    } else if (days === 1) {
      return 'أمس'
    } else if (days < 7) {
      return date.toLocaleDateString('ar', { weekday: 'short' })
    } else {
      return date.toLocaleDateString('ar', { month: 'numeric', day: 'numeric' })
    }
  })

  // هل هناك رسائل غير مقروءة؟
  const hasUnread = computed(() => props.unreadCount > 0)

  // كلاس الوقت
  const timeClass = computed(() => ({
    'text-primary font-weight-medium': hasUnread.value,
  }))

  // حالة الرسالة
  const messageStatusIcon = computed(() => {
    if (!lastMessage.value) return ''
    if (lastMessage.value.is_read) return 'mdi-check-all'
    if (lastMessage.value.is_delivered) return 'mdi-check-all'
    return 'mdi-check'
  })

  const messageStatusColor = computed(() => {
    if (!lastMessage.value) return 'secondary'
    if (lastMessage.value.is_read) return 'info'
    return 'secondary'
  })
</script>

<style scoped>
.chat-list-item {
  position: relative;
  transition: all 0.2s ease;
  overflow: hidden;
  background: transparent;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  border-image: linear-gradient(to right, transparent, rgba(var(--v-theme-on-surface), 0.15) 20%, rgba(var(--v-theme-on-surface), 0.15) 80%, transparent) 1;
}

.chat-list-item:last-child {
  border-bottom: none;
  border-image: none;
}

.chat-list-item:hover {
  background-color: rgba(var(--v-theme-on-surface), 0.03);
}

.chat-list-item--active {
  background: rgba(var(--v-theme-primary), 0.08) !important;
}

.chat-list-item--active:hover {
  background: rgba(var(--v-theme-primary), 0.12) !important;
}

.chat-list-item::before {
  content: '';
  position: absolute;
  inset-block: 20%;
  inset-inline-start: 0;
  width: 4px;
  border-radius: 0 4px 4px 0;
  background: transparent;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform: scaleY(0);
}

.chat-list-item--active::before {
  background: linear-gradient(180deg, rgb(var(--v-theme-primary)) 0%, rgb(var(--v-theme-secondary)) 100%);
  transform: scaleY(1);
}

.chat-list-avatar {
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.08));
  transition: transform 0.3s ease;
}

.chat-list-item:hover .chat-list-avatar {
  transform: scale(1.05);
}

.chat-name {
  max-width: 185px;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: rgba(var(--v-theme-on-surface), 0.95);
}

.chat-time {
  flex-shrink: 0;
  font-size: 0.75rem;
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface), 0.45);
}

.chat-preview {
  max-width: 205px;
  font-size: 0.85rem;
  color: rgba(var(--v-theme-on-surface), 0.6);
  line-height: 1.4;
}

.chat-menu-btn {
  opacity: 0;
  transition: all 0.2s ease;
  color: rgba(var(--v-theme-on-surface), 0.5);
  background: rgba(var(--v-theme-on-surface), 0.05);
}

.chat-list-item:hover .chat-menu-btn {
  opacity: 1;
  margin: 0px 8px;
}

@media (max-width: 600px) {
  .chat-menu-btn {
    opacity: 1;
    margin: 0px 8px;
  }
}

.unread-badge {
  background: rgb(var(--v-theme-primary));
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  min-width: 22px;
  height: 22px;
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 6px;
  box-shadow: 0 4px 10px rgba(var(--v-theme-primary), 0.4);
}

.chat-badge-icon {
  opacity: 0.7;
}

/* Context Menu Styles */
.context-menu-card {
  min-width: 190px;
  overflow: hidden;
  border: 1px solid rgba(var(--v-border-color), 0.08);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12) !important;
  background: rgba(var(--v-theme-surface), 0.95) !important;
}

.context-menu-item {
  min-height: 44px;
  padding: 8px 16px !important;
  transition: all 0.2s ease;
}

.context-menu-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.08);
  transform: translateX(-4px); /* For RTL layout */
}

.context-menu-item--danger:hover {
  background-color: rgba(234, 0, 56, 0.08);
}
</style>
