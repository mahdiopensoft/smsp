<template>
  <custom-dialog
    v-model="internalValue"
    width="550"
    :title="$t('chat.starred.title') || 'الرسائل المميزة بنجمة'"
  >
    <div class="pa-0 bg-surface d-flex flex-column" style="max-height: 70vh;">
      <div v-if="loading" class="pa-10 text-center">
          <div class="app-loader-spinner app-loader--lg"></div>
          <p class="mt-4 text-secondary">جاري جلب رسائلك المفضلة...</p>
        </div>

        <v-list v-else-if="messages.length > 0" class="pa-0 starred-list">
          <v-list-item
            v-for="msg in messages"
            :key="msg.id"
            class="starred-item py-4 px-4 border-b"
            @click="goToMessage(msg)"
          >
            <template #prepend>
              <div class="position-relative me-4">
                <UserAvatar :name="msg.sender?.username" size="48" :src="msg.sender?.profile_picture" />
                <v-icon
                  class="star-indicator position-absolute"
                  color="amber"
                  size="18"
                  style="bottom: -2px; right: -2px; background: white; border-radius: 50%;"
                >mdi-star</v-icon>
              </div>
            </template>

            <div class="d-flex flex-column w-100">
              <div class="d-flex justify-space-between align-center mb-1">
                <span class="font-weight-bold text-primary">{{ msg.sender?.username }}</span>
                <span class="text-caption text-medium-emphasis">{{ formatDate(msg.created_at) }}</span>
              </div>

              <div class="message-preview-content rounded-lg pa-2 bg-grey-lighten-4 mt-1">
                <div v-if="msg.message_type === 'text'" class="text-body-2 text-wrap line-clamp-3">
                  {{ msg.content }}
                </div>
                <div v-else-if="msg.message_type === 'image'" class="d-flex align-center gap-2">
                  <v-img
                    class="rounded"
                    cover
                    height="40"
                    :src="msg.file"
                    width="40"
                  />
                  <span class="text-body-2">{{ $t('chat.type.image') || 'صورة' }}</span>
                </div>
                <div v-else-if="msg.message_type === 'sticker'" class="d-flex align-center gap-2">
                  <v-img contain height="40" :src="msg.content" width="40" />
                  <span class="text-body-2">{{ $t('chat.type.sticker') || 'ملصق' }}</span>
                </div>
                <div v-else class="d-flex align-center gap-2">
                  <v-icon color="secondary">mdi-file-document-outline</v-icon>
                  <span class="text-body-2 text-truncate">{{ msg.file_name || 'ملف مرفق' }}</span>
                </div>
              </div>
            </div>

            <template #append>
              <v-tooltip location="top" text="إلغاء التمييز">
                <template #activator="{ props }">
                  <custom-btn
                    v-bind="props"
                    class="hover-amber"
                    color="grey-lighten-1"
                    icon="mdi-star-minus-outline"
                    isIcon
                    variant="text"
                    :click="() => unstar(msg.id)"
                  />
                </template>
              </v-tooltip>
            </template>
          </v-list-item>
        </v-list>

        <div v-else class="pa-12 text-center text-secondary">
          <div class="empty-state-icon mx-auto mb-6">
            <v-icon color="amber-lighten-3" size="80">mdi-star-off-outline</v-icon>
          </div>
          <h3 class="text-h6 font-weight-bold mb-2">لا توجد رسائل مميزة</h3>
          <p class="text-body-2">قم بتمييز الرسائل الهامة بنجمة لتجدها هنا لاحقاً وبسرعة.</p>
        </div>
    </div>
  </custom-dialog>
</template>

<script setup>
  import { computed, ref, watch } from 'vue'
  import UserAvatar from '../../components/common/UserAvatar.vue'
  import { useChatStore } from "../../store/chat"

  const props = defineProps({
    modelValue: Boolean,
  })

  const emit = defineEmits(['update:modelValue', 'goToMessage'])

  const chatStore = useChatStore()
  const loading = ref(false)
  const messages = computed(() => chatStore.starredMessages)

  const internalValue = computed({
    get: () => props.modelValue,
    set: val => emit('update:modelValue', val),
  })

  watch(internalValue, newVal => {
    if (newVal) fetchMessages()
  })

  async function fetchMessages () {
    loading.value = true
    try {
      await chatStore.fetchStarredMessages()
    } finally {
      loading.value = false
    }
  }

  async function unstar (id) {
    try {
      await chatStore.toggleStar(id)
      chatStore.starredMessages = chatStore.starredMessages.filter(m => m.id !== id)
    } catch (error) {
      console.error('Failed to unstar', error)
    }
  }

  function goToMessage (msg) {
    emit('goToMessage', msg)
    internalValue.value = false
  }

  function formatDate (dateStr) {
    const date = new Date(dateStr)
    const now = new Date()

    if (date.toDateString() === now.toDateString()) {
      return date.toLocaleTimeString('ar', { hour: '2-digit', minute: '2-digit' })
    }
    return date.toLocaleDateString('ar', { month: 'short', day: 'numeric' })
  }
</script>

<style scoped>
.starred-list {
  max-height: 550px;
  overflow-y: auto;
  scrollbar-width: thin;
}

.starred-item {
  transition: all 0.2s;
  cursor: pointer;
}

.starred-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.03);
}

.message-preview-content {
  border: 1px solid rgba(0,0,0,0.05);
}

.hover-amber:hover {
  color: var(--v-theme-amber) !important;
}

.glass-panel {
  background: rgba(255, 255, 255, 0.95) !important;
}

.premium-shadow {
  box-shadow: 0 12px 48px rgba(0,0,0,0.15) !important;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.empty-state-icon {
  width: 120px;
  height: 120px;
  background: #fff8e1;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
