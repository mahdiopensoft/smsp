<template>
  <div
    class="chat-header d-flex align-center py-2"
    :class="isWidget ? 'px-2' : 'px-4'"
  >
    <!-- زر الرجوع (للموبايل) -->
    <v-btn
      v-if="showBack"
      class="me-2 hover-lift"
      icon
      size="small"
      variant="text"
      @click="$emit('back')"
    >
      <v-icon>mdi-arrow-right</v-icon>
    </v-btn>

    <!-- صورة المحادثة -->
    <UserAvatar
      class="me-3 cursor-pointer"
      :is-online="otherParticipant?.is_online"
      :name="displayName"
      :show-status="!isGroup"
      :size="40"
      :src="avatarSrc"
      @click="$emit('showInfo')"
    />

    <!-- معلومات المحادثة -->
    <div
      class="chat-info flex-grow-1 cursor-pointer"
      @click="$emit('showInfo')"
    >
      <h3 class="font-weight-medium text-truncate mb-0">
        {{ displayName }}
      </h3>
      <p v-if="subtitle" class="text-secondary text-truncate mb-0">
        {{ subtitle }}
      </p>
    </div>

    <!-- أزرار الإجراءات -->
    <div class="chat-actions d-flex">
      <v-btn icon size="small" density="compact" variant="text" @click="$emit('search')">
        <v-icon>mdi-magnify</v-icon>
        <v-tooltip activator="parent" location="bottom">{{ $t("chat.header.search") || "بحث" }}</v-tooltip>
      </v-btn>

      <v-menu location="bottom end">
        <template #activator="{ props }">
          <v-btn v-bind="props" icon size="small" density="compact" variant="text">
            <v-icon>mdi-dots-vertical</v-icon>
            <v-tooltip activator="parent" location="bottom">{{ $t('chat.header.options') || 'خيارات' }}</v-tooltip>
          </v-btn>
        </template>

        <v-list class="pa-1 bg-surface" density="compact">
          <v-list-item @click="$emit('showInfo')">
            <template #prepend>
              <v-icon size="20">mdi-information-outline</v-icon>
            </template>
            <v-list-item-title>
              {{
                isGroup
                  ? $t("chat.header.groupInfo")
                  : $t("chat.header.contactInfo")
              }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item @click="$emit('selectMessages')">
            <template #prepend>
              <v-icon size="20">mdi-checkbox-multiple-marked-outline</v-icon>
            </template>
            <v-list-item-title>{{
              $t("chat.header.selectMessages")
            }}</v-list-item-title>
          </v-list-item>

          <v-list-item @click="$emit('mute')">
            <template #prepend>
              <v-icon size="20">{{
                chat.is_muted ? "mdi-bell-outline" : "mdi-bell-off-outline"
              }}</v-icon>
            </template>
            <v-list-item-title>{{
              chat.is_muted ? $t("chat.header.unmute") : $t("chat.header.mute")
            }}</v-list-item-title>
          </v-list-item>

          <v-list-item @click="$emit('clearChat')">
            <template #prepend>
              <v-icon size="20">mdi-broom</v-icon>
            </template>
            <v-list-item-title>{{ $t("chat.clearChat") }}</v-list-item-title>
          </v-list-item>

          <v-list-item @click="$emit('showWallpaper')">
            <template #prepend>
              <v-icon size="20">mdi-image-outline</v-icon>
            </template>
            <v-list-item-title>{{ $t("chat.header.wallpaper") || "خلفية الدردشة" }}</v-list-item-title>
          </v-list-item>

          <v-list-item @click="$emit('showStarred')">
            <template #prepend>
              <v-icon color="amber" size="20">mdi-star-outline</v-icon>
            </template>
            <v-list-item-title>{{ $t("chat.header.starredMessages") || "الرسائل المميزة بنجمة" }}</v-list-item-title>
          </v-list-item>

          <v-list-item @click="$emit('archive')">
            <template #prepend>
              <v-icon size="20">{{ chat.is_archived ? 'mdi-archive-arrow-up-outline' : 'mdi-archive-outline' }}</v-icon>
            </template>
            <v-list-item-title>{{
              chat.is_archived ? ($t("chat.header.unarchive") || "إلغاء الأرشفة") : ($t("chat.header.archive") || "أرشفة")
            }}</v-list-item-title>
          </v-list-item>

          <v-list-item v-if="!isGroup || isAdmin" class="text-error" @click="$emit('deleteChat')">
            <template #prepend>
              <v-icon color="error" size="20">mdi-delete-outline</v-icon>
            </template>
            <v-list-item-title>{{ $t("chat.deleteChat") }}</v-list-item-title>
          </v-list-item>

          <v-divider v-if="!isGroup" class="my-1" />

          <v-list-item
            v-if="!isGroup"
            class="text-error"
            @click="$emit('block')"
          >
            <template #prepend>
              <v-icon color="error" size="20">mdi-block-helper</v-icon>
            </template>
            <v-list-item-title>{{ $t("chat.block") }}</v-list-item-title>
          </v-list-item>

          <v-list-item
            v-if="isGroup"
            class="text-error"
            @click="$emit('leaveGroup')"
          >
            <template #prepend>
              <v-icon color="error" size="20">mdi-exit-run</v-icon>
            </template>
            <v-list-item-title>{{ $t("chat.leaveGroup") }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </div>
  </div>
</template>

<script setup>
  import { computed } from 'vue'
  import { useI18n } from 'vue-i18n'
  import UserAvatar from '../../components/common/UserAvatar.vue'

  const props = defineProps({
    chat: {
      type: Object,
      required: true,
    },
    typingUsers: {
      type: Array,
      default: () => [],
    },
    showBack: {
      type: Boolean,
      default: false,
    },
    isWidget: {
      type: Boolean,
      default: false,
    },
  })

  defineEmits([
    'back',
    'showInfo',
    'search',
    'selectMessages',
    'mute',
    'clearChat',
    'archive',
    'deleteChat',
    'block',
    'leaveGroup',
    'showWallpaper',
    'showStarred',
    'closeWidget',
    'openFullScreen',
  ])

  const { t } = useI18n()

  // هل هي مجموعة؟
  const isGroup = computed(() => props.chat?.chat_type === 'group')

  // هل المستخدم الحالي مشرف في المجموعة؟
  const isAdmin = computed(() => props.chat?.current_user_is_admin || false)

  // المشارك الآخر
  const otherParticipant = computed(() => props.chat?.other_participant)

  // اسم المحادثة
  const displayName = computed(() => {
    if (!props.chat) return ''
    if (isGroup.value) {
      return props.chat.name || t('chat.header.groupDefaultName', 'Group')
    }
    return (
      (otherParticipant.value?.full_name || (otherParticipant.value?.first_name ? `${otherParticipant.value.first_name}`.trim() : null))
      || otherParticipant.value?.username
      || t('chat.header.userDefaultName', 'User')
    )
  })

  // صورة المحادثة
  const avatarSrc = computed(() => {
    if (!props.chat) return null
    if (isGroup.value) {
      return props.chat.group_picture
    }
    return (otherParticipant.value?.profile_picture || otherParticipant.value?.image_user)
  })

  // النص التحتي (حالة الاتصال أو الكتابة)
  const subtitle = computed(() => {
    // إذا هناك من يكتب
    if (props.typingUsers.length > 0) {
      if (props.typingUsers.length === 1) {
        return `${props.typingUsers[0]} ${t('chat.typing')}`
      }
      return `${props.typingUsers.length} ${t('chat.typing')}`
    }

    // للمحادثات الخاصة
    if (!isGroup.value && otherParticipant.value) {
      if (otherParticipant.value.is_online) {
        return t('chat.online')
      }
      // TODO: إضافة "آخر ظهور"
      return t('chat.offline')
    }

    // للمجموعات
    if (isGroup.value && props.chat.participants_count) {
      return t('chat.header.participants', {
        count: props.chat.participants_count,
      })
    }

    return ''
  })
</script>

<style scoped>
.chat-header {
  background: rgba(var(--v-theme-surface), 0.85);
  border-bottom: 1px solid rgba(var(--v-border-color), 0.08);
  min-height: 60px;
  position: relative;
  z-index: 10;
}

.chat-info {
  min-width: 0;
}

.chat-info h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: rgba(var(--v-theme-on-surface), 0.95);
  letter-spacing: -0.01em;
}

.chat-info p {
  color: rgba(var(--v-theme-on-surface), 0.6) !important;
  font-size: 0.85rem;
  font-weight: 500;
}

.chat-actions .v-btn {
  border-radius: 12px !important;
  background: transparent;
  color: rgba(var(--v-theme-on-surface), 0.6);
  transition: all 0.25s ease;
}

.chat-actions .v-btn:hover {
  background: rgba(var(--v-theme-primary), 0.08);
  color: rgb(var(--v-theme-primary));
  transform: translateY(-2px);
}

.chat-header :deep(.user-avatar-wrapper .v-avatar) {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(var(--v-border-color), 0.05);
}

.cursor-pointer {
  cursor: pointer;
}
</style>
