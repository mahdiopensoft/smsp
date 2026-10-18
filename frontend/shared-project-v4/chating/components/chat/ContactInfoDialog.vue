<template>
  <custom-dialog
    :model-value="dialog"
    @update:model-value="dialog = $event"
    :title="$t('chat.header.userInfo') || 'معلومات المستخدم'"
    width="430"
  >
    <div class="d-flex flex-column align-center text-center pt-2 pb-6">
      <!-- Profile Avatar Section -->
      <div class="position-relative mb-4">
        <v-avatar class="premium-profile-avatar" size="110">
          <v-img
            cover
            :src="(contact?.profile_picture || contact?.image_user) || '/default-avatar.png'"
          />
        </v-avatar>
        <!-- Online Indicator Pulse -->
        <div v-if="contact?.is_online" class="online-pulse-container">
          <span class="status-pulse-dot" />
        </div>
      </div>

      <!-- Display Name & Username -->
      <h2 class="text-h5 font-weight-black mb-1 color-text-primary">
        {{ displayName }}
      </h2>
      <p class="text-subtitle-2 text-medium-emphasis mb-3">
        @{{ contact?.username }}
      </p>

      <!-- Connection Status indicator -->
      <v-chip
        :color="contact?.is_online ? 'success' : 'grey'"
        size="small"
        variant="tonal"
        class="font-weight-bold px-3"
      >
        <v-icon start size="12" class="me-1">
          {{ contact?.is_online ? 'mdi-circle' : 'mdi-circle-outline' }}
        </v-icon>
        {{ contact?.is_online ? ($t('chat.online') || 'نشط الآن') : lastSeen }}
      </v-chip>
    </div>

    <v-divider class="mb-5" opacity="0.08" />

    <!-- Info List Section -->
    <div class="info-details-list d-flex flex-column gap-3 mb-2">
      <!-- Phone Info Card -->
      <div v-if="contact?.phone_number" class="info-card-item">
        <div class="info-card-icon-box bg-primary-lighten-5 text-primary">
          <v-icon size="20">mdi-phone</v-icon>
        </div>
        <div class="info-card-content">
          <span class="info-card-label">{{ $t('chat.info.phone') || 'رقم الهاتف' }}</span>
          <span class="info-card-value" dir="ltr" style="text-align: right;">{{ contact?.phone_number }}</span>
        </div>
      </div>

      <!-- Email Info Card -->
      <div v-if="contact?.email" class="info-card-item">
        <div class="info-card-icon-box bg-primary-lighten-5 text-primary">
          <v-icon size="20">mdi-email</v-icon>
        </div>
        <div class="info-card-content">
          <span class="info-card-label">{{ $t('chat.info.email') || 'البريد الإلكتروني' }}</span>
          <span class="info-card-value text-truncate">{{ contact?.email }}</span>
        </div>
      </div>

      <!-- Bio/Status Info Card -->
      <div v-if="contact?.bio" class="info-card-item">
        <div class="info-card-icon-box bg-primary-lighten-5 text-primary">
          <v-icon size="20">mdi-information-outline</v-icon>
        </div>
        <div class="info-card-content">
          <span class="info-card-label">{{ $t('chat.info.bio') || 'النبذة التعريفية' }}</span>
          <span class="info-card-value bio-text-wrap">{{ contact?.bio }}</span>
        </div>
      </div>

      <!-- Last Seen Info Card -->
      <div v-if="!contact?.is_online" class="info-card-item">
        <div class="info-card-icon-box bg-grey-lighten-4 text-grey-darken-2">
          <v-icon size="20">mdi-clock-outline</v-icon>
        </div>
        <div class="info-card-content">
          <span class="info-card-label">{{ $t('chat.info.lastSeen') || 'آخر ظهور' }}</span>
          <span class="info-card-value">{{ lastSeen }}</span>
        </div>
      </div>

      <!-- Shared Media Section -->
      <SharedMediaSection v-if="chatId" :chat-id="chatId" />
    </div>

    <!-- Footer Actions Slot -->
    <template #actions>
      <custom-btn 
        type="cancel" 
        :click="() => dialog = false" 
      />
      <v-spacer></v-spacer>
      <custom-btn
        color="error"
        variant="flat"
        :click="() => $emit('block', contact)"
        :label="$t('chat.info.blockUser') || 'حظر المستخدم'"
        icon="mdi-block-helper"
      />
    </template>
  </custom-dialog>
</template>

<script setup>
  import { computed } from 'vue'
  import { useI18n } from 'vue-i18n'
  import { useDisplay } from 'vuetify'
  import SharedMediaSection from './SharedMediaSection.vue'

  const props = defineProps({
    modelValue: Boolean,
    contact: {
      type: Object,
      default: null,
    },
    chatId: {
      type: [Number, String],
      default: null,
    },
  })

  const emit = defineEmits(['update:modelValue', 'startChat', 'block'])

  const { t, locale } = useI18n()
  const { xs } = useDisplay()

  const dialog = computed({
    get: () => props.modelValue,
    set: val => emit('update:modelValue', val),
  })

  const displayName = computed(() => {
    if (!props.contact) return ''
    return (
      props.contact.full_name
      || `${props.contact.first_name || ''} ${props.contact.last_name || ''}`.trim()
      || props.contact.username
      || t('chat.header.userDefaultName', 'User')
    )
  })

  const lastSeen = computed(() => {
    if (props.contact?.is_online) {
      return t('chat.online')
    }
    if (props.contact?.last_seen) {
      const date = new Date(props.contact.last_seen)
      return date.toLocaleString(locale.value, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    }
    return t('chat.info.unknown')
  })
</script>

<style scoped>
.premium-profile-avatar {
  border: 3px solid rgba(var(--v-theme-primary), 0.15) !important;
  border-radius: 50%;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.online-pulse-container {
  position: absolute;
  bottom: 4px;
  right: 4px;
  background: rgb(var(--v-theme-surface));
  border-radius: 50%;
  padding: 3px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-pulse-dot {
  width: 14px;
  height: 14px;
  background: #22c55e;
  border-radius: 50%;
  animation: pulse-animation 2s infinite;
}

@keyframes pulse-animation {
  0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
  70% { box-shadow: 0 0 0 8px rgba(34, 197, 94, 0); }
  100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
}

.info-details-list {
  width: 100%;
}

.info-card-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 18px;
  background: rgba(var(--v-theme-surface), 1);
  border: 1px solid rgba(var(--v-border-color), 0.08) !important;
  border-radius: 16px;
  transition: all 0.25s ease;
}

.info-card-item:hover {
  border-color: rgba(var(--v-theme-primary), 0.2) !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.03);
}

.info-card-icon-box {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.bg-primary-lighten-5 {
  background-color: rgba(var(--v-theme-primary), 0.06) !important;
}

.info-card-content {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  min-width: 0;
  text-align: right;
}

.info-card-label {
  font-size: 0.75rem;
  color: #8e8e93;
  font-weight: 700;
  margin-bottom: 2px;
  text-transform: uppercase;
}

.info-card-value {
  font-size: 0.925rem;
  color: rgba(var(--v-theme-on-surface), 0.85);
  font-weight: 500;
}

.bio-text-wrap {
  word-wrap: break-word;
  white-space: pre-line;
  line-height: 1.5;
}

.color-text-primary {
  color: rgb(var(--v-theme-on-surface));
}

.gap-3 {
  gap: 12px;
}
</style>
