<template>
  <v-slide-y-reverse-transition>
    <div
      v-if="chatStore.isQuickChatOpen"
      class="quick-chat-widget elevation-10"
      :class="[
        isRtl ? 'widget-right' : 'widget-left',
        { 'widget-expanded': isWidgetExpanded },
      ]"
    >
      <!-- Header -->
      <div
        class="quick-chat-header px-4 py-3 d-flex align-center bg-surface header-border"
      >
        <div class="d-flex align-center flex-grow-1">
          <v-icon
            icon="mdi-forum"
            class="me-2 text-primary pulse-icon"
            size="22"
          ></v-icon>
          <span
            class="text-subtitle-1 font-weight-bold"
            style="color: rgb(var(--v-theme-on-surface))"
            >المراسلة السريعة</span
          >
        </div>

        <v-btn
          :icon="
            isWidgetExpanded
              ? 'mdi-arrow-collapse-horizontal'
              : 'mdi-arrow-expand-horizontal'
          "
          variant="tonal"
          density="compact"
          color="grey-darken-2"
          :title="isWidgetExpanded ? 'تصغير العرض' : 'توسيع العرض'"
          @click="isWidgetExpanded = !isWidgetExpanded"
          class="me-2 control-btn rounded-circle d-none d-sm-flex"
          elevation="0"
        ></v-btn>

        <v-btn
          icon="mdi-open-in-new"
          variant="tonal"
          density="compact"
          color="grey-darken-2"
          title="فتح في نافذة كاملة"
          @click="openFullScreen"
          class="me-2 control-btn rounded-circle d-none d-sm-flex"
          elevation="0"
        ></v-btn>

        <v-btn
          icon="mdi-close"
          variant="tonal"
          density="compact"
          color="grey-darken-2"
          title="إغلاق المحادثة"
          @click="chatStore.toggleQuickChat()"
          class="control-btn rounded-circle"
          elevation="0"
        ></v-btn>
      </div>

      <!-- Body -->
      <div class="quick-chat-body flex-grow-1 overflow-hidden d-flex">
        <!-- Chat List -->
        <div v-if="!activeChatId" class="w-100 h-100 overflow-y-auto">
          <ChatList
            :chats="chatStore.chats"
            :loading="chatStore.isLoadingChats"
            :unread-counts="chatStore.unreadCounts"
            :current-user-id="currentUserId"
            @select-chat="selectChat"
            @new-chat="showNewChatDialog = true"
            @new-group="showNewGroupDialog = true"
            @settings="showSettingsDialog = true"
            @pin-chat="chatStore.togglePin"
            @mute-chat="chatStore.toggleMute"
            @delete-chat="chatStore.deleteChat"
            @archive-chat="chatStore.toggleArchive"
          />
        </div>

        <!-- Chat Window -->
        <div v-else class="w-100 h-100 d-flex flex-column chat-window-wrapper">
          <ChatWindow
            :chat="chatStore.activeChat"
            :current-user-id="currentUserId"
            :has-more="chatStore.hasMoreMessages"
            :loading="chatStore.isLoadingMessages"
            :loading-more="chatStore.isLoadingMore"
            :messages="chatStore.messages"
            :sending="chatStore.isSending"
            :show-back="true"
            :is-widget="true"
            :typing-users="chatStore.typingUsers"
            @back="goBackToList"
            @send="sendMessage"
            @send-file="sendFile"
            @load-more="handleLoadMore"
            @show-info="openContactInfo"
            @show-wallpaper="showWallpaperDialog = true"
            @show-starred="showStarredDialog = true"
            @clear-chat="showClearChatConfirm = true"
            @delete-chat="showDeleteChatConfirm = true"
            @leave-group="showLeaveGroupConfirm = true"
            @block-chat="showBlockConfirm = true"
            @mute-chat="chatStore.toggleMute(activeChatId)"
            @archive-chat="chatStore.toggleArchive(activeChatId)"
            @close-widget="chatStore.toggleQuickChat()"
            @open-full-screen="openFullScreen"
            @delete="handleDeleteMessage"
            @edit="handleEditMessage"
            @save-edit="handleSaveEdit"
            @cancel-edit="handleCancelEdit"
            :editing-message="editingMessage"
            :preview-wallpaper="previewWallpaper"
          />
        </div>
      </div>
    </div>
  </v-slide-y-reverse-transition>

  <!-- Dialogs -->
  <NewChatDialog
    v-model="showNewChatDialog"
    @open-group-create="
      showNewChatDialog = false;
      showNewGroupDialog = true;
    "
    @open-group-with-members="handleOpenGroupWithMembers"
    @select-user="handleUserSelect"
  />

  <NewGroupDialog
    v-model="showNewGroupDialog"
    :pre-selected-name="preSelectedGroupName"
    :pre-selected-member-ids="preSelectedGroupMembers"
    @create-group="handleCreateGroup"
  />

  <SettingsDialog v-model="showSettingsDialog" />

  <!-- ديالوج معلومات جهة الاتصال -->
  <ContactInfoDialog
    v-model="showContactInfo"
    :contact="contactToShow"
    :chat-id="activeChatId"
    @block="showBlockConfirm = true"
  />

  <!-- ديالوج معلومات المجموعة -->
  <GroupInfoDialog
    v-model="showGroupInfo"
    :current-user-id="currentUserId"
    :group="chatStore.activeChat"
    @add-members="showAddMembersDialog = true"
    @leave-group="showLeaveGroupConfirm = true"
    @updated="handleGroupUpdated"
    @make-admin="handleMakeAdmin"
    @remove-admin="handleRemoveAdmin"
    @remove-member="handleRemoveMember"
  />

  <!-- ديالوج إضافة أعضاء -->
  <AddMembersDialog
    v-if="activeChatId"
    v-model="showAddMembersDialog"
    :chat-id="activeChatId"
    :existing-member-ids="existingMemberIds"
  />

  <!-- ديالوج خلفية المحادثة -->
  <WallpaperDialog
    v-model="showWallpaperDialog"
    :chat="chatStore.activeChat"
    @preview="(val) => (previewWallpaper = val)"
  />

  <!-- ديالوج الرسائل المميزة بنجمة -->
  <StarredMessagesDialog v-model="showStarredDialog" />

  <!-- ديالوج تأكيد مسح المحادثة -->
  <custom-dialog
    v-model="showClearChatConfirm"
    width="360"
    height="auto"
    title="مسح المحادثة"
  >
    <div class="pa-4 text-center">
      <v-icon color="warning" size="48" class="mb-2">mdi-broom</v-icon>
      <p class="text-secondary text-body-1">
        هل أنت متأكد من مسح جميع الرسائل؟ لا يمكن التراجع عن هذا الإجراء.
      </p>
    </div>
    <template #actions>
      <custom-btn type="cancel" :click="() => (showClearChatConfirm = false)" />
      <custom-btn
        color="warning"
        variant="flat"
        :click="handleClearChat"
        label="مسح"
        icon="mdi-broom"
      />
    </template>
  </custom-dialog>

  <!-- ديالوج تأكيد حذف المحادثة -->
  <custom-dialog
    v-model="showDeleteChatConfirm"
    width="360"
    height="auto"
    title="حذف المحادثة"
  >
    <div class="pa-4 text-center">
      <v-icon color="error" size="48" class="mb-3">mdi-delete-alert</v-icon>
      <p>هل أنت متأكد من حذف هذه المحادثة بالكامل؟</p>

      <v-alert
        v-if="
          activeChatData?.chat_type === 'group' && activeChatData?.current_user_is_admin
        "
        type="error"
        variant="tonal"
        class="mt-3 text-start"
        density="compact"
      >
        <span class="text-caption">
          <strong>تنبيه هـام:</strong> سيؤدي هذا الإجراء إلى حذف المجموعة بجميع رسائلها من
          أجهزة كافة الأعضاء نهائياً ولا يمكن التراجع عنه.
        </span>
      </v-alert>
    </div>
    <template #actions>
      <custom-btn type="cancel" :click="() => (showDeleteChatConfirm = false)" />
      <custom-btn
        color="error"
        variant="flat"
        :click="confirmDeleteChat"
        label="حذف"
        icon="mdi-delete-alert"
      />
    </template>
  </custom-dialog>

  <!-- ديالوج تأكيد مغادرة المجموعة -->
  <custom-dialog
    v-model="showLeaveGroupConfirm"
    width="360"
    height="auto"
    title="مغادرة المجموعة"
  >
    <div class="pa-4 text-center">
      <v-icon color="error" size="48" class="mb-2">mdi-exit-run</v-icon>
      <p class="text-secondary text-body-1">
        هل أنت متأكد من مغادرة هذه المجموعة؟ لن تتمكن من إرسال رسائل أو قراءتها بعد الآن.
      </p>
    </div>
    <template #actions>
      <custom-btn type="cancel" :click="() => (showLeaveGroupConfirm = false)" />
      <custom-btn
        color="error"
        variant="flat"
        :click="confirmLeaveGroup"
        label="مغادرة"
        icon="mdi-exit-run"
      />
    </template>
  </custom-dialog>

  <!-- ديالوج تأكيد الحظر -->
  <custom-dialog
    v-model="showBlockConfirm"
    width="360"
    height="auto"
    title="حظر المستخدم"
  >
    <div class="pa-4 text-center">
      <v-icon color="error" size="48" class="mb-2">mdi-block-helper</v-icon>
      <p class="text-secondary text-body-1">هل أنت متأكد من حظر هذا المستخدم؟</p>
    </div>
    <template #actions>
      <custom-btn type="cancel" :click="() => (showBlockConfirm = false)" />
      <custom-btn
        color="error"
        variant="flat"
        :click="handleBlockUser"
        label="حظر"
        icon="mdi-block-helper"
      />
    </template>
  </custom-dialog>
</template>

<script setup>
import { computed, ref, watch, onMounted, onUnmounted } from "vue";
import { getRouter } from "../../src/router/routerInstance";
import { useRtl } from "vuetify";
import { useChatStore } from "../store/chat";
import { useAuthStore } from "../../src/UserManagement/stores/auth";
import { useChatWebSocket } from "../composables/useWebSocket";
import { useNotificationStore } from "../store/notificationStore";
import { chatService } from "../services/chatService";

import ChatList from "./chat/ChatList.vue";
import ChatWindow from "./chat/ChatWindow.vue";
import NewChatDialog from "./chat/NewChatDialog.vue";
import NewGroupDialog from "./chat/NewGroupDialog.vue";
import SettingsDialog from "./chat/SettingsDialog.vue";
import ContactInfoDialog from "./chat/ContactInfoDialog.vue";
import GroupInfoDialog from "./chat/GroupInfoDialog.vue";
import AddMembersDialog from "./chat/AddMembersDialog.vue";
import WallpaperDialog from "./chat/WallpaperDialog.vue";
import StarredMessagesDialog from "./chat/StarredMessagesDialog.vue";

const currentUserId = computed(() => {
  if (authStore.user?.id) return authStore.user.id;

  if (authStore.accessToken) {
    try {
      const payload = JSON.parse(atob(authStore.accessToken.split(".")[1]));
      if (payload && payload.user_id) return payload.user_id;
    } catch (e) {}
  }

  try {
    let pStr = localStorage.getItem("profile");
    if (pStr) {
      let p = JSON.parse(pStr);
      let id = p.id || p.user_id || p.data?.id || p.data?.user_id;
      if (id) return id;
    }

    let uStr = localStorage.getItem("user");
    if (uStr) {
      let u = JSON.parse(uStr);
      let id = u.id || u.user_id || u.data?.id || u.data?.user_id;
      if (id) return id;
    }

    let tStr = localStorage.getItem("token");
    if (tStr) {
      const payload = JSON.parse(atob(tStr.split(".")[1]));
      if (payload && payload.user_id) return payload.user_id;
    }
  } catch (e) {}

  return null;
});

const showNewChatDialog = ref(false);
const showNewGroupDialog = ref(false);
const showSettingsDialog = ref(false);
const showContactInfo = ref(false);
const isWidgetExpanded = ref(false);
const showGroupInfo = ref(false);
const showAddMembersDialog = ref(false);
const showClearChatConfirm = ref(false);
const showDeleteChatConfirm = ref(false);
const showLeaveGroupConfirm = ref(false);

const activeChatData = computed(() => {
  return chatStore.chats.find((c) => c.id === activeChatId.value);
});
const showBlockConfirm = ref(false);
const showWallpaperDialog = ref(false);
const showStarredDialog = ref(false);
const contactToShow = ref(null);
const previewWallpaper = ref(null);
const preSelectedGroupName = ref("");
const preSelectedGroupMembers = ref([]);
const editingMessage = ref(null);

function handleOpenGroupWithMembers(data) {
  preSelectedGroupName.value = data.name || "";
  preSelectedGroupMembers.value = data.memberIds || [];
  showNewChatDialog.value = false;
  showNewGroupDialog.value = true;
}

watch(showNewGroupDialog, (isOpen) => {
  if (!isOpen) {
    setTimeout(() => {
      preSelectedGroupName.value = "";
      preSelectedGroupMembers.value = [];
    }, 300);
  }
});

const existingMemberIds = computed(() => {
  const chat = chatStore.activeChat;
  if (!chat || !Array.isArray(chat.participants_data)) return [];
  return chat.participants_data.filter((p) => p && p.user).map((p) => p.user.id);
});

const chatStore = useChatStore();
const authStore = useAuthStore();
const router = getRouter();
const { isRtl } = useRtl();

const activeChatId = computed(() => chatStore.activeChatId);
let chatWs = null;
let currentWsChatId = null;

function setupChatWebSocket(chatId) {
  if (!chatId) return;
  if (chatWs && currentWsChatId === chatId) return; // Already connected/connecting to this chat

  if (chatWs) {
    chatWs.disconnect();
    chatWs = null;
  }

  currentWsChatId = chatId;
  chatWs = useChatWebSocket(chatId);
  chatWs.on("chat_message", (data) => {
    if (String(data.message.sender?.id) !== String(authStore.user?.id)) {
      chatStore.addIncomingMessage(data.message);
    }
  });
  chatWs.on("typing_indicator", (data) =>
    chatStore.setUserTyping(data.username, data.is_typing)
  );
  chatWs.on("user_status_update", (data) =>
    chatStore.updateUserStatus(data.user_id, data.is_online)
  );
  chatWs.on("messages_read", (data) => chatStore.markMessagesAsRead(data.message_ids));
  chatWs.on("messages_delivered", (data) =>
    chatStore.markMessagesAsDelivered(data.message_ids)
  );
  chatWs.on("reaction_update", (data) => chatStore.updateReaction(data));
  chatWs.connect();
}

watch(activeChatId, (newId) => {
  if (chatStore.isQuickChatOpen) {
    setupChatWebSocket(newId);
  }
});

watch(
  () => chatStore.isQuickChatOpen,
  (isOpen) => {
    if (isOpen) {
      chatStore.fetchChats();
      if (activeChatId.value) {
        setupChatWebSocket(activeChatId.value);
      }
    } else {
      if (chatWs) {
        chatWs.disconnect();
        chatWs = null;
        currentWsChatId = null;
      }
    }
  }
);

onMounted(() => {
  chatStore.fetchChats();
  const notificationStore = useNotificationStore();
  notificationStore.initWebSocket();
});

onUnmounted(() => {
  if (chatWs) {
    chatWs.disconnect();
  }
});

async function selectChat(chatId) {
  await chatStore.setActiveChat(chatId);
}

function goBackToList() {
  chatStore.setActiveChat(null);
}

function openFullScreen() {
  chatStore.isQuickChatOpen = false;
  router.push({ name: "chatting-view" });
}

async function handleUserSelect(user) {
  try {
    const chat = await chatStore.createChat({
      chat_type: "private",
      participant_ids: [user.id],
    });
    showNewChatDialog.value = false;
    selectChat(chat.id);
  } catch (error) {
    console.error("Error creating chat:", error);
  }
}

async function handleCreateGroup(groupData) {
  try {
    const chat = await chatStore.createChat({
      chat_type: "group",
      name: groupData.name,
      participant_ids: groupData.participants,
      is_read_only: groupData.isPrivate,
    });
    showNewGroupDialog.value = false;
    selectChat(chat.id);
  } catch (error) {
    console.error("Error creating group:", error);
  }
}

async function sendMessage(content, replyToId, messageType = "text") {
  await chatStore.sendMessage(content, replyToId, messageType);
}

async function sendFile(file, type, caption) {
  await chatStore.sendFile(file, type, caption);
}

async function handleLoadMore() {
  if (activeChatId.value && chatStore.hasMoreMessages && !chatStore.isLoadingMore) {
    await chatStore.fetchMessages(activeChatId.value, chatStore.nextPage);
  }
}

function openContactInfo() {
  const chat = chatStore.activeChat;
  if (!chat) return;
  if (chat.chat_type === "group") {
    showGroupInfo.value = true;
  } else {
    contactToShow.value = chat.other_participant;
    showContactInfo.value = true;
  }
}

async function handleClearChat() {
  if (activeChatId.value) {
    try {
      await chatStore.clearChat(activeChatId.value);
      showClearChatConfirm.value = false;
    } catch (error) {
      console.error(error);
    }
  }
}

async function handleDeleteMessage(message) {
  if (message && message.id) {
    try {
      await chatStore.deleteMessage(message.id);
    } catch (error) {
      console.error("Error deleting message:", error);
    }
  }
}

function handleEditMessage(message) {
  editingMessage.value = message;
}

async function handleSaveEdit(messageId, content) {
  try {
    await chatStore.editMessage(messageId, content);
    editingMessage.value = null;
  } catch (error) {
    console.error("Error editing message:", error);
  }
}

function handleCancelEdit() {
  editingMessage.value = null;
}

async function handleGroupUpdated() {
  await chatStore.refreshActiveChat();
  await chatStore.fetchChats();
}

async function handleMakeAdmin(userId) {
  try {
    await chatService.updateParticipantRole(chatStore.activeChatId, userId, true);
    await chatStore.refreshActiveChat();
  } catch (error) {
    console.error("Error making admin:", error);
  }
}

async function handleRemoveAdmin(userId) {
  try {
    await chatService.updateParticipantRole(chatStore.activeChatId, userId, false);
    await chatStore.refreshActiveChat();
  } catch (error) {
    console.error("Error removing admin:", error);
  }
}

async function handleRemoveMember(userId) {
  try {
    await chatService.removeParticipant(chatStore.activeChatId, userId);
    await chatStore.refreshActiveChat();
  } catch (error) {
    console.error("Error removing member:", error);
  }
}

async function confirmDeleteChat() {
  if (activeChatId.value) {
    try {
      const isGroupAdmin =
        activeChatData.value?.chat_type === "group" &&
        activeChatData.value?.current_user_is_admin;
      await chatStore.deleteChat(activeChatId.value, !!isGroupAdmin);
      showDeleteChatConfirm.value = false;
      goBackToList();
    } catch (error) {
      console.error(error);
    }
  }
}

async function confirmLeaveGroup() {
  if (activeChatId.value) {
    try {
      await chatStore.leaveChat(activeChatId.value);
      showLeaveGroupConfirm.value = false;
      goBackToList();
    } catch (error) {
      console.error(error);
    }
  }
}

async function handleBlockUser() {
  if (!chatStore.activeChat || !chatStore.activeChat.other_participant) return;

  const chatId = chatStore.activeChat.id;
  const userIdToBlock = chatStore.activeChat.other_participant.id;

  try {
    await chatService.blockUser(userIdToBlock);
    showBlockConfirm.value = false;
    chatStore.removeChat(chatId);
    goBackToList();
  } catch (error) {
    console.error("Error blocking user:", error);
  }
}
</script>

<style scoped>
.quick-chat-widget {
  position: fixed;
  bottom: 20px;
  width: 420px;
  height: calc(100vh - 40px);
  max-height: calc(100vh - 40px);
  background: rgb(var(--v-theme-surface));
  border-radius: 12px;
  z-index: 1010;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 11px 15px -7px rgba(0, 0, 0, 0.2), 0 24px 38px 3px rgba(0, 0, 0, 0.14),
    0 9px 46px 8px rgba(0, 0, 0, 0.12) !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.widget-expanded {
  width: 700px !important;
}

.widget-left {
  left: 20px;
}

.widget-right {
  right: 20px;
}

.quick-chat-header {
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  flex-shrink: 0;
}

.control-btn {
  background: rgba(255, 255, 255, 0.15) !important;
  transition: all 0.25s ease;
}
.control-btn:hover {
  background: rgba(255, 255, 255, 0.3) !important;
  transform: scale(1.08);
}

@keyframes float {
  0% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-3px) rotate(-3deg);
  }
  100% {
    transform: translateY(0px) rotate(0deg);
  }
}
.pulse-icon {
  animation: float 3s ease-in-out infinite;
}

.quick-chat-body {
  background-color: rgba(var(--v-theme-background), 0.5);
}

:deep(.chat-list-header) {
  padding: 12px !important;
}

:deep(.chat-list-title) {
  font-size: 1.1rem !important;
}

:deep(.chat-list-subtitle) {
  display: none;
}

:deep(.chat-list-search .v-field) {
  border-radius: 12px !important;
}

.chat-window-wrapper :deep(.chat-messages) {
  padding: 12px !important;
}

.chat-window-wrapper :deep(.message-input-wrapper) {
  padding-bottom: 8px !important;
}

.chat-window-wrapper :deep(.read-only-banner) {
  padding-bottom: 12px !important;
}

@media (max-width: 600px) {
  .quick-chat-widget {
    width: 100% !important;
    height: 100vh !important;
    max-height: 100vh !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    border-radius: 0 !important;
    z-index: 1010 !important;
  }
}
</style>
