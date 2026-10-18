<template>
  <div
    class="chat-window d-flex flex-column h-100 bg-background"
  >
    <!-- هيدر المحادثة -->
    <ChatHeader
      v-if="chat"
      :chat="chat"
      :show-back="showBack"
      :is-widget="isWidget"
      :typing-users="typingUsers"
      @archive="$emit('archiveChat')"
      @back="$emit('back')"
      @block="$emit('blockChat')"
      @clear-chat="$emit('clearChat')"
      @delete-chat="$emit('deleteChat')"
      @leave-group="$emit('leaveGroup')"
      @mute="$emit('muteChat')"
      @search="showSearch = !showSearch"
      @select-messages="startSelection"
      @show-info="$emit('showInfo')"
      @show-starred="$emit('showStarred')"
      @show-wallpaper="$emit('showWallpaper')"
      @close-widget="$emit('closeWidget')"
      @open-full-screen="$emit('openFullScreen')"
    />

    <!-- شريط البحث -->
    <div v-if="showSearch" class="search-bar-container pa-3">
      <div class="d-flex align-center gap-2">
        <SearchBar
          v-model="searchQuery"
          autofocus
          class="flex-grow-1 chat-search-field"
          :placeholder="$t('chat.window.searchPlaceholder')"
          @enter="onSearch"
          @search="onSearch"
        />
        <div
          v-if="searchResults.length > 0"
          class="search-nav d-flex align-center gap-1"
        >
          <span class="text-secondary">
            {{ currentSearchIndex + 1 }}/{{ searchResults.length }}
          </span>
          <v-btn
            :disabled="currentSearchIndex <= 0"
            icon
            size="x-small"
            @click="navigateSearch('prev')"
          >
            <v-icon size="18">mdi-chevron-up</v-icon>
          </v-btn>
          <v-btn
            :disabled="currentSearchIndex >= searchResults.length - 1"
            icon
            size="x-small"
            @click="navigateSearch('next')"
          >
            <v-icon size="18">mdi-chevron-down</v-icon>
          </v-btn>
        </div>
        <v-btn icon size="small" @click="closeSearch">
          <v-icon size="18">mdi-close</v-icon>
        </v-btn>
      </div>
    </div>

    <!-- حالة عدم اختيار محادثة -->
    <template v-if="!chat">
      <ChatIntro />
    </template>

    <!-- الرسائل -->
    <div v-if="chat" class="chat-content-wrapper position-relative d-flex flex-column">
      <!-- الرسالة المثبتة -->
      <v-fade-transition>
        <div v-if="chat.pinned_message_data" class="pinned-message-banner elevation-1">
          <div class="d-flex align-center gap-3 pa-2 px-4 bg-surface border-b">
            <v-icon color="primary" size="20">mdi-pin</v-icon>
            <div class="flex-grow-1 text-truncate cursor-pointer" @click="scrollToMessage(chat.pinned_message)">
              <span class="text-primary font-weight-bold text-caption d-block">{{ $t('chat.pinnedMessage') || 'رسالة مثبتة' }}</span>
              <span class="text-body-2 text-truncate d-block">{{ chat.pinned_message_data.content || $t('chat.attachment') }}</span>
            </div>
            <v-btn
              v-if="chat.current_user_is_admin"
              icon
              size="x-small"
              variant="text"
              @click="handleUnpinMessage"
            >
              <v-icon size="16">mdi-close</v-icon>
            </v-btn>
          </div>
        </div>
      </v-fade-transition>

      <!-- حالة التحميل -->
      <div
        v-if="loading"
        class="messages-loading d-flex align-center justify-center"
      >
        <div class="app-loader-spinner app-loader--md"></div>
      </div>

      <!-- قائمة الرسائل -->
      <div
        v-else
        ref="messagesContainerRef"
        class="messages-container pa-3"
        :class="{ 'chat-bg-pattern': !chat?.wallpaper }"
        :style="wallpaperStyle"
        @scroll="onScroll"
      >
        <div ref="messagesContentRef">
          <!-- زر تحميل المزيد -->
          <div v-if="hasMore" class="text-center mb-3">
            <v-btn
              :loading="loadingMore"
              size="small"
              variant="tonal"
              @click="$emit('loadMore')"
            >
              {{ $t("chat.window.loadMore") }}
            </v-btn>
          </div>

          <!-- حالة فارغة -->
          <EmptyState
            v-if="messages.length === 0"
            :description="$t('chat.window.startMessaging')"
            icon="mdi-message-outline"
            :icon-size="60"
            :title="$t('chat.window.noMessages')"
          />

          <!-- الرسائل -->
          <template v-else>
            <div v-for="(message, index) in messages" :key="message.id">
              <!-- فاصل التاريخ -->
              <div
                v-if="showDateSeparator(index)"
                class="date-separator text-center my-3"
              >
                <v-chip class="date-chip" size="small">
                  {{ formatDate(message.created_at) }}
                </v-chip>
              </div>

              <!-- رسالة نظام -->
              <div
                v-if="message.message_type === 'system'"
                class="system-message text-center my-2"
              >
                <v-chip class="system-chip" size="small" variant="flat">
                  <v-icon
                    class="me-1"
                    size="14"
                  >mdi-information-outline</v-icon>
                  {{ formatSystemMessage(message) }}
                </v-chip>
              </div>

              <!-- الرسالة العادية -->
              <div
                v-else
                class="message-row d-flex w-100"
                :class="{
                  'selection-mode': isSelectionMode,
                  'justify-start': isOwnMessage(message),
                  'justify-end': !isOwnMessage(message),
                }"
              >
                <!-- خانة التحديد -->
                <v-checkbox
                  v-if="isSelectionMode"
                  v-model="selectedMessages"
                  class="selection-checkbox"
                  :class="{
                    'order-last ms-2': isOwnMessage(message),
                    'me-2': !isOwnMessage(message),
                  }"
                  density="compact"
                  hide-details
                  :value="message.id"
                />
                <MessageItem
                  :class="{
                    'selected-message': selectedMessages.includes(message.id),
                  }"
                  :current-user-id="currentUserId"
                  :message="message"
                  :show-avatar="isGroup && !isOwnMessage(message)"
                  :show-sender-name="
                    isGroup && !isOwnMessage(message) && showSenderName(index)
                  "
                  @click="
                    isSelectionMode ? toggleMessageSelection(message.id) : null
                  "
                  @context-menu="onContextMenu"
                  @go-to-reply="scrollToMessage"
                  @react="(emoji) => onReact(message, emoji)"
                  @view-image="$emit('viewImage', $event)"
                />
              </div>
            </div>
          </template>

          <!-- مؤشر الكتابة -->
          <div
            v-if="typingUsers.length > 0"
            class="typing-indicator d-flex align-center gap-2 mt-2"
          >
            <div class="typing-dots"><span /><span /><span /></div>
            <span class="text-secondary">{{ typingText }}</span>
          </div>
        </div>
      </div>

      <!-- زر التمرير للأسفل -->
      <v-scale-transition>
        <div v-if="!loading && !isUserNearBottom" class="scroll-bottom-btn">
          <v-badge
            v-if="unreadCount > 0"
            color="primary"
            :content="unreadCount"
            offset-x="10"
            offset-y="10"
          >
            <v-btn
              class="scroll-bottom-action"
              color="surface"
              elevation="3"
              icon="mdi-chevron-down"
              size="small"
              theme="light"
              @click="scrollToBottom(true)"
            />
          </v-badge>
          <v-btn
            v-else
            class="scroll-bottom-action"
            color="surface"
            elevation="3"
            icon="mdi-chevron-down"
            size="small"
            theme="light"
            @click="scrollToBottom(true)"
          />
        </div>
      </v-scale-transition>

      <!-- حقل الإدخال - ثابت في الأسفل -->
      <div v-if="!isSelectionMode && canMessage" class="message-input-wrapper">
        <MessageInput
          :key="chat?.id"
          ref="messageInputRef"
          :active-chat-id="chat?.id"
          :chat-messages="messages"
          :editing-message="editingMessage"
          :reply-to="replyTo"
          :sending="sending"
          @cancel-edit="$emit('cancelEdit')"
          @cancel-reply="replyTo = null"
          @save-edit="(id, content) => $emit('saveEdit', id, content)"
          @send="onSend"
          @send-file="onSendFile"
          @typing="onTyping"
        />
      </div>

      <!-- تنبيه المنع -->
      <div v-if="!isSelectionMode && !canMessage" class="read-only-banner pa-3 text-center bg-surface border-t">
      <div class="d-flex align-center justify-center text-medium-emphasis">
        <v-icon size="small" class="me-2" color="warning">mdi-lock</v-icon>
        <span class="text-body-2 font-weight-medium">
          {{ readOnlyMessage }}
        </span>
      </div>
    </div>    <!-- شريط إجراءات التحديد -->
      <div
        v-if="isSelectionMode"
        class="selection-toolbar d-flex align-center justify-space-between px-4 py-3"
      >
        <div class="d-flex align-center gap-2">
          <v-btn icon variant="text" @click="cancelSelection">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <span class="font-weight-medium">
            {{ $t("chat.window.selected", { count: selectedMessages.length }) }}
          </span>
        </div>
        <div class="d-flex gap-1">
          <v-btn
            :disabled="selectedMessages.length === 0"
            icon
            variant="text"
            @click="copySelectedMessages"
          >
            <v-icon>mdi-content-copy</v-icon>
            <v-tooltip activator="parent" location="top">{{
              $t("chat.window.copy")
            }}</v-tooltip>
          </v-btn>
          <v-btn
            :disabled="selectedMessages.length === 0"
            icon
            variant="text"
            @click="showForwardDialog = true"
          >
            <v-icon>mdi-share</v-icon>
            <v-tooltip activator="parent" location="top">{{
              $t("chat.window.forward")
            }}</v-tooltip>
          </v-btn>
          <v-btn
            color="error"
            :disabled="selectedMessages.length === 0"
            icon
            variant="text"
            @click="showDeleteConfirm = true"
          >
            <v-icon>mdi-delete</v-icon>
            <v-tooltip activator="parent" location="top">{{
              $t("chat.window.delete")
            }}</v-tooltip>
          </v-btn>
        </div>
      </div>
    </div>

    <!-- قائمة سياق الرسالة -->
    <v-menu
      v-model="showContextMenu"
      class="message-context-menu"
      location="end"
      :target="contextMenuTarget"
    >
      <v-list class="context-menu-list pa-1" density="compact">
        <!-- التفاعلات السريعة -->
        <div class="d-flex pa-1 gap-1 border-b mb-1 justify-space-between">
          <v-btn
            v-for="emoji in ['👍', '❤️', '😂', '😮', '😢', '🙏']"
            :key="emoji"
            icon
            size="small"
            variant="text"
            @click="onReact(selectedMessage, emoji)"
          >
            <span style="font-size: 1.2rem">{{ emoji }}</span>
          </v-btn>
        </div>

        <v-list-item @click="onReply">
          <template #prepend>
            <v-icon size="20">mdi-reply</v-icon>
          </template>
          <v-list-item-title>{{ $t("chat.window.reply") }}</v-list-item-title>
        </v-list-item>

        <v-list-item @click="onCopy">
          <template #prepend>
            <v-icon size="20">mdi-content-copy</v-icon>
          </template>
          <v-list-item-title>{{ $t("chat.window.copy") }}</v-list-item-title>
        </v-list-item>

        <v-list-item @click="toggleStar(selectedMessage)">
          <template #prepend>
            <v-icon :color="selectedMessage?.is_starred ? 'amber' : ''" size="20">
              {{ selectedMessage?.is_starred ? 'mdi-star' : 'mdi-star-outline' }}
            </v-icon>
          </template>
          <v-list-item-title>{{ selectedMessage?.is_starred ? ($t('chat.unstar') || 'إزالة النجمة') : ($t('chat.star') || 'تمييز بنجمة') }}</v-list-item-title>
        </v-list-item>

        <v-list-item @click="onForwardContext">
          <template #prepend>
            <v-icon size="20">mdi-share</v-icon>
          </template>
          <v-list-item-title>{{ $t("chat.window.forward") }}</v-list-item-title>
        </v-list-item>

        <v-list-item v-if="chat?.current_user_is_admin" @click="handlePinMessage(selectedMessage)">
          <template #prepend>
            <v-icon size="20">mdi-pin</v-icon>
          </template>
          <v-list-item-title>{{ chat.pinned_message === selectedMessage?.id ? ($t('chat.unpin') || 'إلغاء التثبيت') : ($t('chat.pin') || 'تثبيت') }}</v-list-item-title>
        </v-list-item>

        <template v-if="isOwnMessage(selectedMessage)">
          <v-list-item
            v-if="selectedMessage?.message_type === 'text'"
            @click="$emit('edit', selectedMessage)"
          >
            <template #prepend>
              <v-icon size="20">mdi-pencil</v-icon>
            </template>
            <v-list-item-title>{{ $t("chat.window.edit") }}</v-list-item-title>
          </v-list-item>

          <v-divider class="my-1" />

          <v-list-item
            class="text-error"
            @click="$emit('delete', selectedMessage)"
          >
            <template #prepend>
              <v-icon color="error" size="20">mdi-delete</v-icon>
            </template>
            <v-list-item-title>{{
              $t("chat.window.delete")
            }}</v-list-item-title>
          </v-list-item>
        </template>
      </v-list>
    </v-menu>

    <!-- ديالوج تأكيد حذف الرسائل المحددة -->
    <v-dialog v-model="showDeleteConfirm" max-width="360" persistent>
      <v-card class="delete-dialog rounded-xl">
        <div class="delete-header pa-6 text-center">
          <v-icon color="error" size="48">mdi-delete-alert</v-icon>
        </div>
        <v-card-text class="text-center pb-2">
          <h3 class="mb-2">{{ $t("chat.window.deleteMessagesTitle") }}</h3>
          <p class="text-secondary">
            {{
              $t("chat.window.deleteMessagesConfirm", {
                count: selectedMessages.length,
              })
            }}
          </p>
        </v-card-text>
        <v-card-actions class="pa-4 pt-0">
          <v-btn
            class="flex-grow-1"
            rounded="xl"
            variant="outlined"
            @click="showDeleteConfirm = false"
          >
            {{ $t("common.cancel") }}
          </v-btn>
          <v-btn
            class="flex-grow-1"
            color="error"
            rounded="xl"
            variant="flat"
            @click="deleteSelectedMessages"
          >
            {{ $t("chat.window.delete") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ديالوج إعادة التوجيه -->
    <v-dialog v-model="showForwardDialog" max-width="400">
      <v-card class="forward-dialog rounded-xl">
        <v-card-title class="d-flex align-center py-3">
          <v-icon class="me-2">mdi-share</v-icon>
          {{
            $t("chat.window.forwardMessagesTitle", {
              count: selectedMessages.length,
            })
          }}
          <v-spacer />
          <v-btn
            icon
            size="small"
            variant="text"
            @click="showForwardDialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-divider />
        <v-card-text class="pa-0">
          <v-list
            v-if="chatStore.chats.length > 0"
            class="overflow-y-auto"
            lines="two"
            max-height="400"
          >
            <v-list-item
              v-for="chat in chatStore.chats"
              :key="chat.id"
              :value="chat.id"
              @click="toggleForwardChat(chat.id)"
            >
              <template #prepend>
                <div class="d-flex align-center me-3">
                  <v-icon
                    :color="
                      selectedChats.includes(chat.id)
                        ? 'primary'
                        : 'medium-emphasis'
                    "
                  >
                    {{
                      selectedChats.includes(chat.id)
                        ? "mdi-checkbox-marked"
                        : "mdi-checkbox-blank-outline"
                    }}
                  </v-icon>
                </div>
                <UserAvatar
                  class="me-3"
                  :name="
                    chat.chat_type === 'private'
                      ? chat.other_participant?.username
                      : chat.name
                  "
                  size="40"
                  :src="
                    chat.chat_type === 'private'
                      ? chat.other_participant?.profile_picture
                      : chat.group_picture
                  "
                />
              </template>
              <v-list-item-title class="font-weight-medium">
                <template
                  v-if="chat.chat_type === 'private' && chat.other_participant"
                >
                  {{ chat.other_participant.username }}
                  <span
                    v-if="
                      chat.other_participant.first_name ||
                        chat.other_participant.last_name
                    "
                    class="text-medium-emphasis ms-1"
                  >
                    ({{ chat.other_participant.first_name }}
                    {{ chat.other_participant.last_name }})
                  </span>
                </template>
                <template v-else>
                  {{ chat.name }}
                </template>
              </v-list-item-title>
              <v-list-item-subtitle v-if="chat.chat_type === 'group'">
                {{ $t("chat.list.group") }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
          <div v-else class="text-center py-5 text-disabled">
            {{ $t("chat.list.noChats") }}
          </div>
        </v-card-text>
        <v-card-actions class="pa-4 pt-0">
          <v-btn
            block
            color="primary"
            :disabled="selectedChats.length === 0"
            :loading="forwarding"
            rounded="xl"
            variant="flat"
            @click="handleForwardMessages"
          >
            {{ $t("chat.window.forwardButton") }} ({{ selectedChats.length }})
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
  import {
    computed,
    nextTick,
    onBeforeUnmount,
    onMounted,
    ref,
    watch,
  } from 'vue'
  import { useI18n } from 'vue-i18n'
  import EmptyState from '../common/EmptyState.vue'
  import SearchBar from '../common/SearchBar.vue'
  import UserAvatar from '../common/UserAvatar.vue'
 
  import { useChatStore } from '../../store/chat'
  import { useToastStore } from '../../store/toastStore'
  import ChatHeader from './ChatHeader.vue'
  import ChatIntro from './ChatIntro.vue'
  import MessageItem from './MessageItem.vue'
  import MessageInput from './MessageInput.vue'
 
  import { useAuthStore } from '../../../src/UserManagement/stores/auth'
  const props = defineProps({
    chat: {
      type: Object,
      default: null,
    },
    messages: {
      type: Array,
      default: () => [],
    },
    currentUserId: {
      type: Number,
      default: null,
    },
    typingUsers: {
      type: Array,
      default: () => [],
    },
    loading: {
      type: Boolean,
      default: false,
    },
    loadingMore: {
      type: Boolean,
      default: false,
    },
    hasMore: {
      type: Boolean,
      default: false,
    },
    sending: {
      type: Boolean,
      default: false,
    },
    showBack: {
      type: Boolean,
      default: false,
    },
    editingMessage: {
      type: Object,
      default: null,
    },
    previewWallpaper: {
      type: String,
      default: null,
    },
    isWidget: {
      type: Boolean,
      default: false,
    },
  })

  const emit = defineEmits([
    'back',
    'showInfo',
    'send',
    'sendFile',
    'typing',
    'loadMore',
    'muteChat',
    'clearChat',
    'archiveChat',
    'deleteChat',
    'blockChat',
    'viewImage',
    'forward',
    'edit',
    'delete',
    'saveEdit',
    'cancelEdit',
    'leaveGroup',
    'showStarred',
    'showWallpaper',
    'closeWidget',
    'openFullScreen',
  ])

  const { t, locale } = useI18n() // Use i18n

  const authStore = useAuthStore()
  const user = authStore.user || {}
  const chatStore = useChatStore()
  const toastStore = useToastStore()
  const messagesContainerRef = ref(null)
  const messageInputRef = ref(null)
  const showSearch = ref(false)

  const searchQuery = ref('')
  const searchResults = ref([])
  const currentSearchIndex = ref(-1)
  const replyTo = ref(null)
  const showContextMenu = ref(false)
  const contextMenuTarget = ref(null)
  const selectedMessage = ref(null)

  // حالة التحديد
  const isSelectionMode = ref(false)
  const selectedMessages = ref([])
  const showDeleteConfirm = ref(false)
  const showForwardDialog = ref(false)
  const selectedChats = ref([])
  const forwarding = ref(false)

  function toggleForwardChat (chatId) {
    const index = selectedChats.value.indexOf(chatId)
    if (index === -1) {
      selectedChats.value.push(chatId)
    } else {
      selectedChats.value.splice(index, 1)
    }
  }

  async function handleForwardMessages () {
    if (selectedChats.value.length === 0) return

    forwarding.value = true
    try {
      await chatStore.forwardMessages(
        selectedMessages.value,
        selectedChats.value,
      )
      showForwardDialog.value = false
      toastStore.showSuccess(t('chat.window.forwardSuccess') || 'تم إعادة توجيه الرسائل بنجاح')
      cancelSelection()
    } catch (error) {
      console.error('Failed to forward', error)
      toastStore.showError(t('chat.window.forwardError') || 'فشل إعادة توجيه الرسائل')
    } finally {
      forwarding.value = false
      selectedChats.value = [] // Reset seletion
    }
  }

  // هل مجموعة؟
  const isGroup = computed(() => props.chat?.chat_type === 'group')

  // نص الكتابة
  const typingText = computed(() => {
    if (props.typingUsers.length === 0) return ''
    if (props.typingUsers.length === 1) {
      return t('chat.typingSingle', { user: props.typingUsers[0].username })
    }
    return `${props.typingUsers.length} ${t('chat.typing')}`
  })

  // ستايل الخلفية
  const wallpaperStyle = computed(() => {
    const wp = props.previewWallpaper || props.chat?.wallpaper
    if (!wp) return {}
    if (wp.startsWith('#') || wp.startsWith('rgb')) {
      return {
        backgroundColor: wp + ' !important',
        backgroundImage: 'none !important',
      }
    }
    return {
      backgroundImage: `url(${wp}) !important`,
      backgroundSize: 'cover !important',
      backgroundPosition: 'center !important',
      backgroundRepeat: 'no-repeat !important',
      backgroundAttachment: 'fixed !important',
    }
  })

  // هل يمكنني المراسلة؟
  const canMessage = computed(() => {
    if (!props.chat) return true
    if (props.chat.chat_type !== 'group') return true

    // استخدام المعرف من الستور مباشرة لضمان الدقة والتفاعلية
    const myId = props.currentUserId
    if (!myId) return false

    // البحث عن بيانات المشارك
    const me = props.chat.participants_data?.find(p => p.user && (p.user.id == myId || p.user == myId))

    // إذا كنت ممنوعاً من المراسلة من قبل المشرف (تقييد فردي)
    if (me && me.can_send_messages === false) return false

    // إذا كانت المجموعة للمشرفين فقط (تقييد عام)
    if (props.chat.is_read_only) {
      if (me) return me.is_admin
      return props.chat.current_user_is_admin || false
    }

    // إذا لم يتم العثور على بيانات المشارك في المجموعة، نمنع المراسلة كأمان
    if (!me) return false

    return true
  })

  // رسالة المنع
  const readOnlyMessage = computed(() => {
    if (!props.chat) return ''

    const myId = props.currentUserId
    if (!myId) return ''

    const me = props.chat.participants_data?.find(p => p.user && (p.user.id == myId || p.user == myId))

    if (me && me.can_send_messages === false) {
      return t('chat.window.mutedByAdmin') || 'لقد تم منعك من المراسلة في هذه المجموعة'
    }

    return t('chat.window.readOnlyGroup') || 'المراسلة في هذه المجموعة للمشرفين فقط'
  })

  // تثبيت رسالة
  async function handlePinMessage (message) {
    if (!props.chat || !message) return
    const wasPinned = props.chat.pinned_message === message.id
    try {
      await (wasPinned ? chatStore.unpinMessage(props.chat.id) : chatStore.pinMessage(props.chat.id, message.id))
      showContextMenu.value = false
      toastStore.showSuccess(wasPinned ? 'تم إلغاء التثبيت بنجاح' : 'تم تثبيت الرسالة بنجاح')
    } catch (error) {
      console.error('Failed to pin/unpin message', error)
    }
  }

  // إلغاء تثبيت الرسالة
  async function handleUnpinMessage () {
    if (!props.chat) return
    try {
      await chatStore.unpinMessage(props.chat.id)
      toastStore.showSuccess('تم إلغاء التثبيت بنجاح')
    } catch (error) {
      console.error('Failed to unpin message', error)
      toastStore.showError('فشل إلغاء التثبيت')
    }
  }

  // هل الرسالة مني؟
  const isOwnMessage = message => message?.sender?.id == props.currentUserId

  // إظهار فاصل التاريخ
  function showDateSeparator (index) {
    if (index === 0) return true
    const currentDate = new Date(props.messages[index].created_at).toDateString()
    const prevDate = new Date(
      props.messages[index - 1].created_at,
    ).toDateString()
    return currentDate !== prevDate
  }

  // إظهار اسم المرسل (إذا لم يكن نفس المرسل السابق)
  function showSenderName (index) {
    if (index === 0) return true
    return (
      props.messages[index].sender?.id !== props.messages[index - 1].sender?.id
    )
  }

  // تنسيق التاريخ
  function formatDate (dateStr) {
    const date = new Date(dateStr)
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)

    if (date.toDateString() === today.toDateString()) {
      return t('chat.window.today')
    } else if (date.toDateString() === yesterday.toDateString()) {
      return t('chat.window.yesterday')
    } else {
      return date.toLocaleDateString(locale.value, {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    }
  }

  // تنسيق رسائل النظام
  function formatSystemMessage (message) {
    const data = message.system_event_data || {}
    const actorName = data.actor_name || t('chat.systemMessages.someone')
    const targetName = data.target_user_name || t('chat.systemMessages.someone')

    const eventType = message.system_event_type

    switch (eventType) {
      case 'group_created': {
        return t('chat.systemMessages.groupCreated', { actor: actorName })
      }
      case 'member_added': {
        return t('chat.systemMessages.memberAdded', {
          actor: actorName,
          target: targetName,
        })
      }
      case 'member_removed': {
        return t('chat.systemMessages.memberRemoved', {
          actor: actorName,
          target: targetName,
        })
      }
      case 'member_left': {
        return t('chat.systemMessages.memberLeft', { actor: actorName })
      }
      case 'group_name_changed': {
        return t('chat.systemMessages.groupNameChanged', {
          actor: actorName,
          name: data.new_name || '',
        })
      }
      case 'group_picture_changed': {
        return t('chat.systemMessages.groupPictureChanged', { actor: actorName })
      }
      case 'group_description_changed': {
        return t('chat.systemMessages.groupDescriptionChanged', {
          actor: actorName,
        })
      }
      case 'admin_added': {
        return t('chat.systemMessages.adminAdded', {
          actor: actorName,
          target: targetName,
        })
      }
      case 'admin_removed': {
        return t('chat.systemMessages.adminRemoved', {
          actor: actorName,
          target: targetName,
        })
      }
      default: {
        return message.content || t('chat.systemMessages.unknown')
      }
    }
  }

  // قائمة سياق الرسالة
  function onContextMenu (event, message) {
    selectedMessage.value = message
    contextMenuTarget.value = [event.clientX, event.clientY]
    showContextMenu.value = true
  }

  async function onReact (message, emoji) {
    if (!message) return
    try {
      await chatStore.toggleReaction(message.id, emoji)
      showContextMenu.value = false
    } catch (error) {
      console.error('Failed to react', error)
    }
  }

  async function toggleStar (message) {
    if (!message) return
    try {
      await chatStore.toggleStar(message.id)
      showContextMenu.value = false
      toastStore.showSuccess(message.is_starred ? 'تم إزالة النجمة' : 'تم التمييز بنجمة بنجاح')
    } catch (error) {
      console.error('Failed to toggle star', error)
    }
  }

  // رد على رسالة
  function onReply () {
    replyTo.value = selectedMessage.value
    showContextMenu.value = false
    nextTick(() => messageInputRef.value?.focus())
  }

  // فتح حوار التوجيه من القائمة السياقية
  function onForwardContext () {
    if (selectedMessage.value) {
      selectedMessages.value = [selectedMessage.value.id]
      showForwardDialog.value = true
      showContextMenu.value = false
    }
  }

  // نسخ الرسالة
  function onCopy () {
    if (selectedMessage.value?.content) {
      navigator.clipboard.writeText(selectedMessage.value.content)
      toastStore.showSuccess('تم نسخ النص بنجاح')
    }
    showContextMenu.value = false
  }

  // إرسال رسالة
  function onSend (content, replyToId, messageType = 'text') {
    emit('send', content, replyToId, messageType)
    replyTo.value = null
    scrollToBottom()
  }

  // إرسال ملف
  function onSendFile (file, type, caption) {
    emit('sendFile', file, type, caption)
    scrollToBottom()
  }

  // مؤشر الكتابة
  function onTyping (isTyping) {
    emit('typing', isTyping)
  }

  // البحث في الرسائل
  function onSearch (query) {
    if (!query || query.trim() === '') {
      searchResults.value = []
      currentSearchIndex.value = -1
      return
    }

    const queryLower = query.toLowerCase().trim()

    // البحث في الرسائل المحلية
    const results = props.messages.filter(
      m => m.content && m.content.toLowerCase().includes(queryLower),
    )

    searchResults.value = results

    if (results.length > 0) {
      currentSearchIndex.value = 0
      // الانتقال للنتيجة الأولى
      scrollToMessage(results[0].id)
    } else {
      currentSearchIndex.value = -1
    }
  }

  // التنقل بين نتائج البحث
  function navigateSearch (direction) {
    if (searchResults.value.length === 0) return

    if (direction === 'next') {
      if (currentSearchIndex.value < searchResults.value.length - 1) {
        currentSearchIndex.value++
      }
    } else {
      if (currentSearchIndex.value > 0) {
        currentSearchIndex.value--
      }
    }

    const message = searchResults.value[currentSearchIndex.value]
    if (message) {
      scrollToMessage(message.id)
    }
  }

  // إغلاق البحث
  function closeSearch () {
    showSearch.value = false
    searchQuery.value = ''
    searchResults.value = []
    currentSearchIndex.value = -1
  }



  // التمرير للرسالة
  function scrollToMessage (messageId) {
    const element = document.getElementById(`message-${messageId}`)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' })
      element.classList.add('highlight')
      setTimeout(() => element.classList.remove('highlight'), 2000)
    }
  }

  // التمرير للأسفل
  function scrollToBottom (smooth = true) {
    nextTick(() => {
      const container = messagesContainerRef.value
      if (container) {
        container.scrollTo({
          top: container.scrollHeight,
          behavior: smooth ? 'smooth' : 'auto',
        })
        unreadCount.value = 0
      }
    })
  }

  // حالة المستخدم بالنسبة للتمرير (هل هو في الأسفل؟)
  const isUserNearBottom = ref(true)
  const unreadCount = ref(0)

  // عند التمرير
  function onScroll () {
    const container = messagesContainerRef.value
    if (!container) return

    const { scrollTop, scrollHeight, clientHeight } = container
    // نعتبر المستخدم في الأسفل إذا كان ضمن مسافة 100 بكسل
    isUserNearBottom.value = scrollHeight - (scrollTop + clientHeight) < 100

    if (isUserNearBottom.value) {
      unreadCount.value = 0
    }

    if (scrollTop <= 100 && props.hasMore && !props.loadingMore) {
      emit('loadMore')
    }
  }

  const messagesContentRef = ref(null)
  let resizeObserver = null

  function setupResizeObserver () {
    if (resizeObserver) resizeObserver.disconnect()
    if (!messagesContentRef.value) return

    resizeObserver = new ResizeObserver(() => {
      if (isUserNearBottom.value) {
        scrollToBottom(true)
      }
    })
    resizeObserver.observe(messagesContentRef.value)
  }

  // عند تحميل المكون
  onMounted(() => {
    scrollToBottom(false)
    nextTick(() => {
      setupResizeObserver()
      if (props.chat) {
        messageInputRef.value?.focus()
      }
    })
  })

  onBeforeUnmount(() => {
    if (resizeObserver) resizeObserver.disconnect()
  })

  // مراقبة حالة التحميل لإعداد المراقب
  watch(
    () => props.loading,
    isLoading => {
      if (isLoading) {
        if (resizeObserver) {
          resizeObserver.disconnect()
          resizeObserver = null
        }
      } else {
        nextTick(() => {
          scrollToBottom(false)
          setupResizeObserver()
        })
      }
    },
  )

  // مراقبة تغيير المحادثة للتمرير الفوري للأسفل والتركيز
  watch(
    () => props.chat?.id,
    () => {
      isUserNearBottom.value = true
      unreadCount.value = 0
      scrollToBottom(false)

      // التركيز التلقائي على حقل الإدخال
      nextTick(() => {
        messageInputRef.value?.focus()
      })

      // إعادة التمرير بعد فترة قصيرة للتأكد من تحميل العناصر (مثل الصور)
      setTimeout(() => scrollToBottom(false), 300)
    },
  )

  // مراقبة الرسائل الجديدة للتمرير
  watch(
    () => props.messages,
    (newMessages, oldMessages) => {
      const container = messagesContainerRef.value
      if (!container) return

      // تحميل أولي أو لا توجد رسائل سابقة
      if (!oldMessages || oldMessages.length === 0) {
        scrollToBottom(false)
        return
      }

      // التحقق مما إذا تم تحميل رسائل قديمة (إضافة في البداية)
      // الشرط: الطول زاد، ولكن آخر رسالة هي نفسها
      const isPrepended
        = newMessages.length > oldMessages.length
          && newMessages.at(-1)?.id === oldMessages.at(-1)?.id

      if (isPrepended) {
        // الحفاظ على موضع التمرير
        const oldScrollHeight = container.scrollHeight
        const oldScrollTop = container.scrollTop

        nextTick(() => {
          const newScrollHeight = container.scrollHeight
          // الفرق في الارتفاع هو المسافة التي يجب إضافتها للموضع الحالي
          container.scrollTop = newScrollHeight - oldScrollHeight + oldScrollTop
        })
      } else {
        // رسالة جديدة أو تغيير آخر
        const lastMessage = newMessages.at(-1)
        const isMyMessage = isOwnMessage(lastMessage)

        // التمرير إذا كانت رسالتي أو المستخدم في الأسفل
        if (isMyMessage || isUserNearBottom.value) {
          scrollToBottom(true)
        } else {
          // زيادة عدد الرسائل غير المقروءة إذا لم نكن في الأسفل
          unreadCount.value++
        }
      }
    },
    { deep: false }, // المصفوفة تتغير بالكامل عند التحديث من الستور
  )

  // ============ وضع تحديد الرسائل ============

  // بدء وضع التحديد
  function startSelection () {
    isSelectionMode.value = true
    selectedMessages.value = []
  }

  // إلغاء وضع التحديد
  function cancelSelection () {
    isSelectionMode.value = false
    selectedMessages.value = []
    showDeleteConfirm.value = false
    showForwardDialog.value = false
  }

  // تبديل تحديد رسالة
  function toggleMessageSelection (messageId) {
    const index = selectedMessages.value.indexOf(messageId)
    if (index === -1) {
      selectedMessages.value.push(messageId)
    } else {
      selectedMessages.value.splice(index, 1)
    }
  }

  // نسخ الرسائل المحددة
  function copySelectedMessages () {
    const selectedMsgs = props.messages.filter(m =>
      selectedMessages.value.includes(m.id),
    )
    const text = selectedMsgs
      .map(m => m.content || '')
      .filter(Boolean)
      .join('\n')

    navigator.clipboard.writeText(text)
    cancelSelection()
  }

  // حذف الرسائل المحددة
  async function deleteSelectedMessages () {
    for (const messageId of selectedMessages.value) {
      emit('delete', { id: messageId })
    }
    cancelSelection()
  }

  // إعادة توجيه الرسائل المحددة
  function forwardSelectedMessages (chatIds) {
    for (const messageId of selectedMessages.value) {
      emit('forward', { id: messageId, chatIds })
    }
    cancelSelection()
  }

  // تعريض دوال للمكون الأب
  defineExpose({ scrollToBottom, startSelection })
</script>

<style scoped>
/* Chat content layout */
.chat-content-wrapper {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
  background: linear-gradient(180deg, rgba(var(--v-theme-surface), 0.3) 0%, rgba(var(--v-theme-surface), 0.1) 100%);
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(var(--v-theme-on-surface), 0.15) transparent;
  padding: 24px 24px 32px !important;
  background-attachment: fixed !important;
}

.chat-bg-pattern {
  background:
    radial-gradient(circle at 50% top, rgba(var(--v-theme-primary), 0.05), transparent 40%),
    linear-gradient(180deg, rgba(var(--v-theme-surface), 0.8), rgba(var(--v-theme-surface), 0.95));
}

.messages-loading {
  flex: 1;
  min-height: 200px;
}

.message-input-wrapper {
  flex-shrink: 0;
  background-color: rgba(var(--v-theme-surface), 0.75);
  border-top: 1px solid rgba(var(--v-border-color), 0.06);
  /* padding-bottom: env(safe-area-inset-bottom); */
}

.search-bar-container {
  border-bottom: 1px solid rgba(var(--v-border-color), 0.06);
  background: rgba(var(--v-theme-surface), 0.85);
}

.chat-search-field :deep(.v-field) {
  border-radius: 20px !important;
  background: rgba(var(--v-theme-on-surface), 0.04) !important;
  border: 1px solid rgba(var(--v-border-color), 0.06) !important;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02) !important;
  transition: all 0.3s ease;
}

.chat-search-field :deep(.v-field--focused) {
  background: rgba(var(--v-theme-surface), 1) !important;
  border-color: rgba(var(--v-theme-primary), 0.3) !important;
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.08), inset 0 0 0 0 transparent !important;
}

.date-separator {
  position: relative;
  margin: 24px 0 16px;
  z-index: 2;
}

.date-chip {
  background: rgba(var(--v-theme-surface), 0.65) !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  color: rgba(var(--v-theme-on-surface), 0.8) !important;
  font-weight: 600;
  font-size: 0.75rem;
  padding: 4px 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.system-chip {
  background: rgba(var(--v-theme-on-surface), 0.06) !important;
  color: rgba(var(--v-theme-on-surface), 0.75) !important;
  font-weight: 500;
  border: 1px solid rgba(var(--v-border-color), 0.05);
}

.typing-indicator {
  width: fit-content;
  padding: 12px 18px;
  border-radius: 24px;
  border-end-start-radius: 4px;
  background: rgba(var(--v-theme-surface), 0.85);
  border: 1px solid rgba(var(--v-border-color), 0.06);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
}

.typing-dots {
  display: flex;
  gap: 5px;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: rgba(var(--v-theme-primary), 0.6);
  animation: typing 1.4s infinite cubic-bezier(0.4, 0, 0.2, 1) both;
}

.typing-dots span:nth-child(1) {
  animation-delay: 0s;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%,
  80%,
  100% {
    transform: scale(0.6);
    opacity: 0.6;
  }

  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Search navigation */
.search-nav {
  white-space: nowrap;
}

/* Highlight animation for search results */
:deep(.highlight) {
  animation: highlightPulse 2s ease-out infinite;
  animation-iteration-count: 3;
}

@keyframes highlightPulse {
  0% {
    background-color: rgba(255, 255, 0, 0.5);
    box-shadow: 0 0 0 0 rgba(255, 255, 0, 0.7);
  }

  50% {
    background-color: rgba(255, 255, 0, 0.2);
    box-shadow: 0 0 20px 10px rgba(255, 255, 0, 0);
  }

  100% {
    background-color: transparent;
    box-shadow: 0 0 0 0 rgba(255, 255, 0, 0);
  }
}

.highlight-starred {
  animation: starredPulse 3s ease-out;
}

@keyframes starredPulse {
  0% {
    background-color: rgba(255, 193, 7, 0.4);
  }
  30% {
    background-color: rgba(255, 193, 7, 0.4);
  }
  100% {
    background-color: transparent;
  }
}

/* Selection mode styles */
.selection-toolbar {
  background:
    linear-gradient(180deg, rgba(var(--v-theme-surface), 0.98) 0%, rgba(var(--v-theme-surface), 0.92) 100%);
  border-top: 1px solid rgba(var(--v-border-color), 0.08);
  min-height: 60px;
}

.message-row {
  width: 100%;
}

.message-row.selection-mode {
  cursor: pointer;
}

.selection-checkbox {
  flex-shrink: 0;
}

.selected-message {
  background-color: rgba(var(--v-theme-primary), 0.08);
  border-radius: 14px;
}

.delete-header {
  background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
}

.scroll-bottom-btn {
  position: absolute;
  bottom: 98px;
  inset-inline-end: 18px;
  z-index: 5;
}

.scroll-bottom-action {
  box-shadow: 0 16px 28px rgba(15, 23, 42, 0.12) !important;
}

.pinned-message-banner {
  z-index: 5;
  position: sticky;
  top: 0;
  width: 100%;
}


.pinned-message-banner > div {
  background:
    linear-gradient(90deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-surface), 0.98) 24%) !important;
  border-bottom: 1px solid rgba(var(--v-border-color), 0.08);
}
.read-only-banner {
  font-size: 0.9rem;
  color: rgba(var(--v-theme-on-surface), 0.6);
  background-color: rgba(var(--v-theme-surface), 0.94) !important;
  border-top: 1px solid rgba(var(--v-border-color), 0.08);
  padding-bottom: 50px !important;
}
.context-menu-list,
.forward-dialog {
  border: 1px solid rgba(var(--v-border-color), 0.1);
  border: 1px solid rgba(var(--v-border-color), 0.1);
  box-shadow: 0 18px 34px rgba(15, 23, 42, 0.14) !important;
}

@media (max-width: 600px) {
  .messages-container {
    padding: 14px 10px 18px !important;
  }

  .scroll-bottom-btn {
    bottom: 90px;
    inset-inline-end: 12px;
  }
}
</style>
