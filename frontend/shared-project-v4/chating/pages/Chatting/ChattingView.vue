<template>
  <div class="chat-page">
    <!-- <div> -->
    <div class="chat-page__backdrop" />
    <div class="chat-shell d-flex h-100">
      <!-- قائمة المحادثات (الشريط الجانبي) -->
      <div
        class="chat-sidebar chat-panel"
        :class="{ 'chat-sidebar--hidden': isMobile && activeChatId }"
      >
        <ChatList
          :active-chat-id="activeChatId"
          :chats="chatStore.chats"
          :current-user-id="currentUserId"
          :loading="chatStore.isLoadingChats"
          :unread-counts="chatStore.unreadCounts"
          @archive-chat="toggleArchiveChat"
          @delete-chat="handleDeleteChat"
          @logout="handleLogout"
          @mute-chat="toggleMuteChat"
          @new-chat="showNewChatDialog = true"
          @new-group="showNewGroupDialog = true"
          @pin-chat="togglePinChat"
          @profile="showProfileDialog = true"
          @select-chat="selectChat"
          @settings="showSettingsDialog = true"
        />
      </div>

      <!-- نافذة المحادثة -->
      <div
        class="chat-main chat-panel flex-grow-1"
        :class="{ 'chat-main--hidden': isMobile && !activeChatId }"
      >
        <ChatWindow
          :chat="chatStore.activeChat"
          :current-user-id="currentUserId"
          :editing-message="editingMessage"
          :has-more="chatStore.hasMoreMessages"
          :loading="chatStore.isLoadingMessages"
          :loading-more="chatStore.isLoadingMore"
          :messages="chatStore.messages"
          :sending="chatStore.isSending"
          :show-back="isMobile"
          :preview-wallpaper="previewWallpaper"
          :typing-users="chatStore.typingUsers"
          @archive-chat="toggleArchiveChat(chatStore.activeChat?.id)"
          @back="closeChat"
          @block-chat="showBlockConfirm = true"
          @cancel-edit="handleCancelEdit"
          @clear-chat="showClearChatConfirm = true"
          @delete="handleDeleteMessage"
          @delete-chat="handleDeleteChat(chatStore.activeChat?.id)"
          @edit="handleEditMessage"
          @leave-group="handleLeaveGroup"
          @load-more="handleLoadMore"
          @mute-chat="toggleMuteChat(chatStore.activeChat?.id)"
          @save-edit="handleSaveEdit"
          @send="sendMessage"
          @send-file="sendFile"
          @show-info="openContactInfo"
          @show-starred="showStarredDialog = true"
          @show-wallpaper="showWallpaperDialog = true"
          @typing="handleTyping"
          @view-image="openImagePreview"
        />
      </div>
    </div>

    <!-- حوارات -->
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

    <ProfileDialog v-model="showProfileDialog" />

    <v-dialog
      v-model="showImagePreview"
      class="image-preview-dialog"
      max-width="90vw"
    >
      <div class="position-relative">
        <v-btn
          class="img-close-btn"
          color="white"
          icon="mdi-close"
          variant="text"
          @click="showImagePreview = false"
        />
        <v-img contain max-height="90vh" :src="previewImage" />
      </div>
    </v-dialog>

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
      @leave-group="handleLeaveGroup"
      @make-admin="handleMakeAdmin"
      @remove-admin="handleRemoveAdmin"
      @remove-member="handleRemoveMember"
      @updated="handleGroupUpdated"
    />

    <!-- ديالوج إضافة أعضاء -->
    <AddMembersDialog
      v-if="chatStore.activeChatId"
      v-model="showAddMembersDialog"
      :chat-id="chatStore.activeChatId"
      :existing-member-ids="existingMemberIds"
      @members-added="handleMembersAdded"
    />

    <!-- ديالوج خلفية المحادثة -->
    <WallpaperDialog
      v-model="showWallpaperDialog"
      :chat="chatStore.activeChat"
      @preview="(val) => (previewWallpaper = val)"
    />

    <!-- ديالوج الرسائل المميزة بنجمة -->
    <StarredMessagesDialog
      v-model="showStarredDialog"
      @go-to-message="handleGoToMessage"
    />

    <!-- ديالوج تأكيد مسح المحادثة -->
    <custom-dialog
      v-model="showClearChatConfirm"
      width="360"
      height="auto"
      :title="$t('chat.clearChat')"
    >
      <div class="pa-4 text-center">
        <v-icon color="warning" size="48" class="mb-2">mdi-broom</v-icon>
        <p class="text-secondary text-body-1">
          {{ $t("chat.clearChatConfirm") }}
        </p>
      </div>
      <template #actions>
        <custom-btn
          type="cancel"
          :click="() => showClearChatConfirm = false"
        />
        <custom-btn
          color="warning"
          variant="flat"
          :click="handleClearChat"
          :label="$t('chat.clear')"
          icon="mdi-broom"
        />
      </template>
    </custom-dialog>

    <!-- ديالوج تأكيد حذف المحادثة -->
    <custom-dialog
      v-model="showDeleteChatConfirm"
      width="360"
      height="auto"
      :title="$t('chat.deleteChat')"
    >
      <div class="pa-4 text-center">
        <v-icon color="error" size="48" class="mb-2">mdi-delete-alert</v-icon>
        <p class="text-secondary text-body-1">
          {{ $t("chat.deleteChatConfirm") }}
        </p>
        <v-checkbox
          v-if="chatToDeleteData?.chat_type === 'group' && chatToDeleteData?.current_user_is_admin"
          v-model="deleteForAll"
          label="حذف المجموعة لجميع الأعضاء"
          color="error"
          hide-details
          class="mt-2 text-start"
        />
      </div>
      <template #actions>
        <custom-btn
          type="cancel"
          :click="() => showDeleteChatConfirm = false"
        />
        <custom-btn
          color="error"
          variant="flat"
          :click="confirmDeleteChat"
          :label="$t('common.delete')"
          icon="mdi-delete-alert"
        />
      </template>
    </custom-dialog>

    <!-- ديالوج تأكيد مغادرة المجموعة -->
    <custom-dialog
      v-model="showLeaveGroupConfirm"
      width="360"
      height="auto"
      :title="$t('chat.leaveGroup')"
    >
      <div class="pa-4 text-center">
        <v-icon color="error" size="48" class="mb-2">mdi-exit-run</v-icon>
        <p class="text-secondary text-body-1">
          {{ $t("chat.leaveGroupConfirm") }}
        </p>
      </div>
      <template #actions>
        <custom-btn
          type="cancel"
          :click="() => showLeaveGroupConfirm = false"
        />
        <custom-btn
          color="error"
          variant="flat"
          :click="confirmLeaveGroup"
          :label="$t('chat.leave')"
          icon="mdi-exit-run"
        />
      </template>
    </custom-dialog>

    <!-- ديالوج تأكيد الحظر -->
    <custom-dialog
      v-model="showBlockConfirm"
      width="360"
      height="auto"
      :title="$t('chat.blockUser', { name: blockUserName })"
    >
      <div class="pa-4 text-center">
        <v-icon color="error" size="48" class="mb-2">mdi-block-helper</v-icon>
        <p class="text-secondary text-body-1">
          {{ $t("chat.blockUserConfirm") }}
        </p>
      </div>
      <template #actions>
        <custom-btn
          type="cancel"
          :click="() => showBlockConfirm = false"
        />
        <custom-btn
          color="error"
          variant="flat"
          :click="handleBlockUser"
          :label="$t('chat.block')"
          icon="mdi-block-helper"
        />
      </template>
    </custom-dialog>

    <!-- عرض التعميمات -->
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useDisplay } from "vuetify";
import { useChatWebSocket } from "../../composables/useWebSocket";

import ChatList from "../../components/chat/ChatList.vue";
import NewChatDialog from "../../components/chat/NewChatDialog.vue";
import NewGroupDialog from "../../components/chat/NewGroupDialog.vue";
import SettingsDialog from "../../components/chat/SettingsDialog.vue";
import ProfileDialog from "../../components/chat/ProfileDialog.vue";
import ContactInfoDialog from "../../components/chat/ContactInfoDialog.vue";
import GroupInfoDialog from "../../components/chat/GroupInfoDialog.vue";
import AddMembersDialog from "../../components/chat/AddMembersDialog.vue";
import WallpaperDialog from "../../components/chat/WallpaperDialog.vue";
import StarredMessagesDialog from "../../components/chat/StarredMessagesDialog.vue";
import ChatWindow from "../../components/chat/ChatWindow.vue";

import { chatService } from "../../services/chatService";

import { useChatStore } from "../../store/chat";
import { useToastStore } from "../../store/toastStore";
import notificationSound from "../../assest/iphone.mp3";
import { useAuthStore } from "../../../src/UserManagement/stores/auth";

const toastStore = useToastStore();
const authStore = useAuthStore();
const router = useRouter();
const chatStore = useChatStore();
const { t } = useI18n();
const { width } = useDisplay();
const isMobile = computed(() => width.value < 768);

const user = authStore.user || {};

const currentUserId = computed(() => {
  if (authStore.user?.id) return authStore.user.id;
  
  // Try extracting user_id from the JWT access token in memory
  if (authStore.accessToken) {
    try {
      const payload = JSON.parse(atob(authStore.accessToken.split(".")[1]));
      if (payload && payload.user_id) return payload.user_id;
    } catch(e) {}
  }

  try {
    let pStr = localStorage.getItem('profile');
    if (pStr) {
      let p = JSON.parse(pStr);
      let id = p.id || p.user_id || p.data?.id || p.data?.user_id;
      if (id) return id;
    }
    
    let uStr = localStorage.getItem('user');
    if (uStr) {
      let u = JSON.parse(uStr);
      let id = u.id || u.user_id || u.data?.id || u.data?.user_id;
      if (id) return id;
    }
    
    let tStr = localStorage.getItem('token');
    if (tStr) {
      const payload = JSON.parse(atob(tStr.split(".")[1]));
      if (payload && payload.user_id) return payload.user_id;
    }
  } catch(e) {}
  
  return null;
});

// حالة الواجهة
const activeChatId = computed(() => chatStore.activeChatId);
const showNewChatDialog = ref(false);
const showNewGroupDialog = ref(false);
const showProfileDialog = ref(false);
const showSettingsDialog = ref(false);
const showImagePreview = ref(false);
const showContactInfo = ref(false);
const showGroupInfo = ref(false);
const showAddMembersDialog = ref(false);
const showClearChatConfirm = ref(false);
const showDeleteChatConfirm = ref(false);
const showLeaveGroupConfirm = ref(false);
const showBlockConfirm = ref(false);
const deleteForAll = ref(false);
const showWallpaperDialog = ref(false);
const showStarredDialog = ref(false);
const chatIdToDelete = ref(null);
const chatToDeleteData = computed(() => {
  return chatStore.chats.find(c => c.id === chatIdToDelete.value);
});
const contactToShow = ref(null);
const previewImage = ref("");
const editingMessage = ref(null);
const previewWallpaper = ref(null);

watch(showNewChatDialog, (isOpen) => {
  if (!isOpen) {
    previewWallpaper.value = null;
  }
});
// بيانات المجموعة المخصصة
const preSelectedGroupName = ref("");
const preSelectedGroupMembers = ref([]);

// تتبع الإشعارات المستلمة لتجنب التكرار
const receivedAnnouncements = new Set();

// دالة لفتح نافذة المجموعة المخصصة
function handleOpenGroupWithMembers(data) {
  preSelectedGroupName.value = data.name || "";
  preSelectedGroupMembers.value = data.memberIds || [];
  showNewChatDialog.value = false;
  showNewGroupDialog.value = true;
}

// تنظيف بيانات المجموعة عند إغلاق النافذة
watch(showNewGroupDialog, (isOpen) => {
  if (!isOpen) {
    // نؤخر التنظيف قليلاً حتى تنتهي أنيميشن الإغلاق
    setTimeout(() => {
      preSelectedGroupName.value = "";
      preSelectedGroupMembers.value = [];
    }, 300);
  }
});

// دالة لإزالة HTML tags من النص
function stripHtml(html) {
  if (!html) return "";
  const tmp = document.createElement("DIV");
  tmp.innerHTML = html;
  return tmp.textContent || tmp.innerText || "";
}

function showSnackbar(text, color = "success") {
  // تنظيف النص من HTML tags
  const cleanText = stripHtml(text);
  toastStore.showToast(cleanText, color);
}

// البحث عن مستخدمين (لم يعد مستخدماً هنا بشكل مباشر)
const userSearch = ref("");
const searchResults = ref([]);

// WebSocket للمحادثة النشطة
let chatWs = null;

// إعداد WebSocket للمحادثة
function setupChatWebSocket(chatId) {
  // قطع الاتصال السابق
  if (chatWs) {
    chatWs.disconnect();
    chatWs = null;
  }

  if (!chatId) return;

  // إنشاء اتصال جديد - useChatWebSocket handles URL construction internally
  chatWs = useChatWebSocket(chatId);

  // معالجة الرسائل الواردة
  chatWs.on("chat_message", (data) => {
    // تجاهل رسائل المستخدم الحالي (لأنها أُضيفت بالفعل عند الإرسال)
    const currentUserId = String(user.id);
    if (String(data.message.sender?.id) !== currentUserId) {
      chatStore.addIncomingMessage(data.message);
    }
  });

  // معالجة مؤشر الكتابة
  chatWs.on("typing_indicator", (data) => {
    chatStore.setUserTyping(data.username, data.is_typing);
  });

  // معالجة تحديث حالة الاتصال
  chatWs.on("user_status_update", (data) => {
    chatStore.updateUserStatus(data.user_id, data.is_online);
  });

  // معالجة تحديث القراءة
  chatWs.on("messages_read", (data) => {
    chatStore.markMessagesAsRead(data.message_ids);
  });

  // معالجة تحديث الاستلام
  chatWs.on("messages_delivered", (data) => {
    chatStore.markMessagesAsDelivered(data.message_ids);
  });

  // معالجة تحديث التفاعل
  chatWs.on("reaction_update", (data) => {
    chatStore.updateReaction(data);
  });

  // الاتصال
  chatWs.connect();
}

// مراقبة تغيير المحادثة النشطة
watch(
  activeChatId,
  (newId) => {
    setupChatWebSocket(newId);
  },
  { immediate: true }
);

// مراقبة تغيير المحادثة النشطة في الستور (للتزامن عند النقر على الإشعارات)
watch(
  () => chatStore.activeChatId,
  (newId) => {
    if (newId !== activeChatId.value) {
      activeChatId.value = newId;
    }
  }
);

// setupNotificationWebSocket was removed. Global notifications are handled centrally in notificationStore.js.

// تحميل البيانات
onMounted(async () => {
  // طلب إذن الإشعارات
  if ("Notification" in window && Notification.permission !== "granted") {
    Notification.requestPermission();
  }

  try {
    await chatStore.fetchChats();
  } catch (error) {
    console.error("fetchChats failed:", error);
  }

  // Global notification web socket is managed by notificationStore in layouts/default.vue
});

// تنظيف عند إلغاء المكون
onUnmounted(() => {
  if (chatWs) {
    chatWs.disconnect();
  }
  // لا نقوم بقطع اتصال notificationWs هنا لأنه عالمي ويتم إدارته عبر الستور
});

// اختيار محادثة
async function selectChat(chatId) {
  await chatStore.setActiveChat(chatId);
}

// إغلاق المحادثة (العودة للقائمة)
async function closeChat() {
  await chatStore.setActiveChat(null);
}

// تحميل المزيد من الرسائل
async function handleLoadMore() {
  if (
    chatStore.activeChatId &&
    chatStore.hasMoreMessages &&
    !chatStore.isLoadingMore
  ) {
    await chatStore.fetchMessages(chatStore.activeChatId, chatStore.nextPage);
  }
}

// تثبيت/إلغاء تثبيت
async function togglePinChat(chatId) {
  await chatStore.togglePin(chatId);
}

// كتم/إلغاء كتم الإشعارات
async function toggleMuteChat(chatId) {
  await chatStore.toggleMute(chatId);
}

// أرشفة/إلغاء أرشفة
async function toggleArchiveChat(chatId) {
  await chatStore.toggleArchive(chatId);
}

// التعامل مع اختيار مستخدم من الديلوج
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
    showSnackbar(t("chat.messages.error"), "error");
  }
}

// إنشاء مجموعة
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
    showSnackbar(t("chat.messages.error"), "error");
  }
}

// إرسال رسالة
async function sendMessage(content, replyToId, messageType = "text") {
  await chatStore.sendMessage(content, replyToId, messageType);
}

// الانتقال لرسالة محددة
async function handleGoToMessage(msg) {
  // إذا كانت في محادثة أخرى، نفتح المحادثة أولاً
  if (msg.chat !== activeChatId.value) {
    await selectChat(msg.chat);
  }
  // التمرير للرسالة
  setTimeout(() => {
    const windowEl = document.getElementById(`message-${msg.id}`);
    if (windowEl) {
      windowEl.scrollIntoView({ behavior: "smooth", block: "center" });
      windowEl.classList.add("highlight-starred");
      setTimeout(() => windowEl.classList.remove("highlight-starred"), 3000);
    }
  }, 800);
}

// إرسال ملف
async function sendFile(file, type, caption) {
  try {
    await chatStore.sendFile(file, type, caption);
  } catch (error) {
    console.error("Error sending file:", error);
    if (error.response) {
      console.error("Backend error data:", error.response.data);
      const msg =
        error.response.data.error || JSON.stringify(error.response.data);
      showSnackbar(`${t("chat.messages.fileSendFailed")}: ${msg}`, "error");
    } else {
      showSnackbar(t("chat.messages.fileSendFailed"), "error");
    }
  }
}

// مؤشر الكتابة
function handleTyping(isTyping) {
  if (!chatWs) return;

  if (isTyping) {
    chatWs.startTyping();
  } else {
    chatWs.stopTyping();
  }
}

// معاينة الصورة
function openImagePreview(imageUrl) {
  previewImage.value = imageUrl;
  showImagePreview.value = true;
}

// عرض معلومات جهة الاتصال أو المجموعة
function openContactInfo() {
  const chat = chatStore.activeChat;
  if (!chat) return;

  if (chat.chat_type === "group") {
    // فتح ديالوج معلومات المجموعة
    showGroupInfo.value = true;
  } else {
    // فتح ديالوج معلومات جهة الاتصال
    contactToShow.value = chat.other_participant;
    showContactInfo.value = true;
  }
}

const existingMemberIds = computed(() => {
  const chat = chatStore.activeChat;
  if (!chat || !Array.isArray(chat.participants_data)) return [];
  return chat.participants_data
    .filter((p) => p && p.user)
    .map((p) => p.user.id);
});

// إزالة عضو من المجموعة
async function handleRemoveMember(userId) {
  try {
    await chatService.removeParticipant(chatStore.activeChatId, userId);
    showSnackbar(t("chat.messages.memberRemoved"));

    // Update UI manually since setActiveChat caches if already active
    if (chatStore.activeChat && chatStore.activeChat.participants_data) {
      chatStore.activeChat.participants_data =
        chatStore.activeChat.participants_data.filter(
          (p) => p.user.id !== userId
        );
    }
  } catch (error) {
    console.error("Error removing member:", error);
    const errorMsg = error.response?.data?.error || t("chat.messages.error");
    showSnackbar(errorMsg, "error");
    if (error.response?.status >= 400 && error.response?.status < 500) {
      await chatStore.refreshActiveChat();
    }
  }
}

// ترقية عضو لمشرف
async function handleMakeAdmin(userId) {
  try {
    await chatService.updateParticipantRole(
      chatStore.activeChatId,
      userId,
      true
    );
    showSnackbar(t("chat.messages.adminPromoted"));

    if (chatStore.activeChat && chatStore.activeChat.participants_data) {
      const p = chatStore.activeChat.participants_data.find(
        (p) => p.user.id === userId
      );
      if (p) p.is_admin = true;
    }
  } catch (error) {
    console.error("Error making admin:", error.response?.data || error);
    const errorMsg = error.response?.data?.error || t("chat.messages.error");
    showSnackbar(errorMsg, "error");
    if (error.response?.status >= 400 && error.response?.status < 500) {
      await chatStore.refreshActiveChat();
    }
  }
}

// إزالة الإشراف من عضو
async function handleRemoveAdmin(userId) {
  try {
    await chatService.updateParticipantRole(
      chatStore.activeChatId,
      userId,
      false
    );
    showSnackbar(t("chat.messages.adminDemoted"));

    if (chatStore.activeChat && chatStore.activeChat.participants_data) {
      const p = chatStore.activeChat.participants_data.find(
        (p) => p.user.id === userId
      );
      if (p) p.is_admin = false;
    }
  } catch (error) {
    console.error("Error removing admin:", error);
    const errorMsg = error.response?.data?.error || t("chat.messages.error");
    showSnackbar(errorMsg, "error");
    if (error.response?.status >= 400 && error.response?.status < 500) {
      await chatStore.refreshActiveChat();
    }
  }
}

// عند إضافة أعضاء جدد
async function handleMembersAdded() {
  showSnackbar(t("chat.messages.membersAdded"));
  await chatStore.refreshActiveChat();
}

// عند تحديث بيانات المجموعة
async function handleGroupUpdated() {
  showSnackbar(t("chat.messages.groupUpdated"));
  await chatStore.refreshActiveChat();
  await chatStore.fetchChats(); // تحديث قائمة المحادثات أيضاً
}

// حذف رسالة
async function handleDeleteMessage(message) {
  try {
    await chatStore.deleteMessage(message.id);
  } catch (error) {
    console.error("Error deleting message:", error);
    showSnackbar(t("chat.messages.error"), "error");
  }
}

// استلام طلب تعديل رسالة
function handleEditMessage(message) {
  editingMessage.value = message;
}

// حفظ تعديل رسالة
async function handleSaveEdit(messageId, content) {
  try {
    await chatStore.editMessage(messageId, content);
    editingMessage.value = null;
  } catch (error) {
    console.error("Error editing message:", error);
    const errorMessage =
      error.response?.data?.error || t("chat.messages.error");
    showSnackbar(errorMessage, "error");
  }
}

// إلغاء تعديل رسالة
function handleCancelEdit() {
  editingMessage.value = null;
}

// حذف المحادثة
function handleDeleteChat(chatId) {
  chatIdToDelete.value = chatId;
  showDeleteChatConfirm.value = true;
}

async function confirmDeleteChat() {
  if (chatIdToDelete.value) {
    try {
      await chatStore.deleteChat(chatIdToDelete.value, deleteForAll.value);
      showDeleteChatConfirm.value = false;
      chatIdToDelete.value = null;
      deleteForAll.value = false;
      showSnackbar(t("chat.messages.chatDeleted"));
    } catch (error) {
      console.error("Error deleting chat:", error);
      showSnackbar(t("chat.messages.error"), "error");
    }
  }
}

// مسح المحادثة
async function handleClearChat() {
  if (!chatStore.activeChat) return;
  try {
    await chatStore.clearChat(chatStore.activeChatId);
    showClearChatConfirm.value = false;
    showSnackbar(t("chat.messages.chatCleared"));
  } catch (error) {
    console.error("Error clearing chat:", error);
    showSnackbar(t("chat.messages.error"), "error");
  }
}

// مغادرة المجموعة
function handleLeaveGroup() {
  if (chatStore.activeChat?.chat_type === "group") {
    showLeaveGroupConfirm.value = true;
  }
}

async function confirmLeaveGroup() {
  if (!chatStore.activeChatId) return;

  try {
    await chatStore.leaveChat(chatStore.activeChatId);
    showLeaveGroupConfirm.value = false;
    showSnackbar(t("chat.messages.leftGroup"));
    // activeChatId will be cleared by chatStore.removeChat which is called inside leaveChat, or we can clear it here if needed
    activeChatId.value = null;
  } catch (error) {
    console.error("Error leaving group:", error);
    showSnackbar(t("chat.messages.error"), "error");
  }
}

// اسم المستخدم المراد حظره
const blockUserName = computed(() => {
  if (chatStore.activeChat?.other_participant) {
    return (
      chatStore.activeChat.other_participant.full_name ||
      chatStore.activeChat.other_participant.username ||
      "المستخدم"
    );
  }
  return "المستخدم";
});

// حظر مستخدم
async function handleBlockUser() {
  if (!chatStore.activeChat || !chatStore.activeChat.other_participant) return;

  const chatId = chatStore.activeChat.id;
  const userIdToBlock = chatStore.activeChat.other_participant.id;

  try {
    await chatService.blockUser(userIdToBlock);
    showBlockConfirm.value = false;

    // إزالة المحادثة من القائمة فورياً
    chatStore.removeChat(chatId);

    // إغلاق المحادثة
    activeChatId.value = null;
    showSnackbar(t("chat.messages.userBlocked"));
  } catch (error) {
    console.error("Error blocking user:", error);
    showSnackbar(t("chat.messages.error"), "error");
  }
}

// تسجيل الخروج
async function handleLogout() {
  const shared = await import("external-components");
  shared.default.userAuthStore().logout();
  location.reload();
}
</script>

<style scoped>
.chat-page {
  --chat-primary: rgb(var(--v-theme-primary));
  --chat-primary-soft: rgba(var(--v-theme-primary), 0.08);
  --chat-primary-soft-strong: rgba(var(--v-theme-primary), 0.14);
  --chat-surface: rgb(var(--v-theme-surface));
  --chat-surface-muted: rgba(var(--v-theme-on-surface), 0.03);
  --chat-border: rgba(var(--v-border-color), 0.1);
  --chat-border-strong: rgba(var(--v-border-color), 0.16);
  --chat-text: rgba(var(--v-theme-on-surface), 0.88);
  --chat-text-muted: rgba(var(--v-theme-on-surface), 0.58);
  --chat-sidebar-bg: linear-gradient(
    180deg,
    rgba(var(--v-theme-surface), 0.98) 0%,
    rgba(var(--v-theme-surface), 0.92) 100%
  );
  --chat-main-bg: linear-gradient(
    180deg,
    rgba(var(--v-theme-surface), 0.98) 0%,
    rgba(var(--v-theme-surface), 0.94) 100%
  );
  --chat-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
  /* --chat-shadow-soft: 0 8px 24px rgba(15, 23, 42, 0.05); */
  width: 100%;
  height: calc(100vh - 120px);
  min-height: 400px;
  overflow: hidden;
  position: relative;
  border-radius: 22px;
}

.chat-page__backdrop {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.chat-shell {
  position: relative;
  z-index: 1;
  gap: 10px;
  width: 100%;
  height: 100%;
}

.chat-panel {
  position: relative;
  border: 1px solid var(--chat-border);
  border-radius: 22px;
  box-shadow: var(--chat-shadow);
  overflow: hidden;
}

.img-close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1000;
  background-color: rgba(0, 0, 0, 0.5);
}

.chat-sidebar {
  width: 320px;
  min-width: 320px;
  max-width: 320px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--chat-sidebar-bg);
  transition: transform 0.25s ease, opacity 0.25s ease;
  z-index: 10;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  height: 100%;
  background: var(--chat-main-bg);
  box-shadow: var(--chat-shadow-soft);
}

:deep(.chat-panel .v-card) {
  border-color: var(--chat-border);
}

:deep(.chat-panel .text-secondary),
:deep(.chat-panel .text-medium-emphasis) {
  color: var(--chat-text-muted) !important;
}

@media (max-width: 960px) {
  .chat-page {
    border-radius: 0;
  }

  .chat-shell {
    gap: 0;
    padding: 0;
  }

  .chat-panel,
  .chat-sidebar {
    border-radius: 0 !important;
    box-shadow: none;
    border: none;
  }

  .chat-sidebar {
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    left: 0;
    right: 0;
    border: none;
  }

  .chat-sidebar--hidden {
    display: none !important;
  }

  .chat-main {
    width: 100% !important;
    min-width: 100% !important;
    border-radius: 0 !important;
  }

  .chat-main--hidden {
    display: none !important;
  }
}
</style>
