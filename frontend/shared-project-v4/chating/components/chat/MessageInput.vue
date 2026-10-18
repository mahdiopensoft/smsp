<template>
  <div class="message-input-wrapper">
    <!-- معاينة الرد -->
    <div v-if="replyTo && !editingMessage" class="reply-preview d-flex align-center pa-2 mx-3 mt-3 rounded-xl">
      <div class="flex-grow-1">
        <p class="font-weight-medium text-primary mb-0">
          {{ $t("chat.input.replyTo", { name: replyTo.sender?.username }) }}
        </p>
        <p class="text-truncate mb-0">{{ replyTo.content }}</p>
      </div>
      <v-btn icon size="x-small" variant="text" @click="$emit('cancelReply')">
        <v-icon size="18">mdi-close</v-icon>
      </v-btn>
    </div>

    <!-- معاينة التعديل -->
    <div v-if="editingMessage" class="edit-preview d-flex align-center pa-2 mx-3 mt-3 rounded-xl">
      <div class="flex-grow-1">
        <p class="font-weight-medium text-primary mb-0">
          <v-icon class="me-1" size="16">mdi-pencil</v-icon>
          {{ $t("chat.input.editMessage") }}
        </p>
        <p class="text-truncate mb-0 text-medium-emphasis">
          {{ editingMessage.content }}
        </p>
      </div>
      <v-btn icon size="x-small" variant="text" @click="$emit('cancelEdit')">
        <v-icon size="18">mdi-close</v-icon>
      </v-btn>
    </div>

    <!-- شريط التسجيل الصوتي -->
    <div v-if="isRecording" class="recording-panel d-flex align-center gap-3 pa-3 mx-3 my-3 rounded-xl">
      <v-btn color="error" icon size="small" variant="tonal" @click="cancelRecording">
        <v-icon>mdi-delete</v-icon>
        <v-tooltip activator="parent" location="top">{{
          $t("chat.input.cancelRecording")
        }}</v-tooltip>
      </v-btn>
      <div class="flex-grow-1 d-flex align-center justify-center gap-2">
        <span class="recording-dot" />
        <span class="recording-text text-error font-weight-medium">{{
          $t("chat.input.recording")
        }}</span>
        <span class="recording-time font-weight-bold">{{ formattedTime }}</span>
      </div>
      <v-btn color="primary" icon size="small" @click="sendRecording">
        <v-icon>mdi-send</v-icon>
        <v-tooltip activator="parent" location="top">{{
          $t("chat.input.sendRecording")
        }}</v-tooltip>
      </v-btn>
    </div>

    <!-- شريط الإدخال العادي -->
    <div v-else class="message-input d-flex align-end gap-2" style="ali">
      <!-- أزرار المرفقات -->
      <v-menu :close-on-content-click="false" location="top start">
        <template #activator="{ props: menuProps }">
          <v-btn v-bind="menuProps" class="composer-action-btn ms-3" icon size="small" variant="text">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </template>
        <v-list class="attachment-menu pa-2" elevation="0" rounded="xl">
          <div class="d-flex flex-column gap-2">
            <v-tooltip location="left" :text="$t('chat.input.image')">
              <template #activator="{ props }"><v-btn v-bind="props" class="attachment-option mb-2"
                  color="purple-lighten-4" icon @click="openFilePicker('image')"><v-icon
                    color="purple-darken-2">mdi-image</v-icon></v-btn></template>
            </v-tooltip>
            <v-tooltip location="left" :text="$t('chat.input.document')">
              <template #activator="{ props }"><v-btn v-bind="props" class="attachment-option" color="blue-lighten-4"
                  icon @click="openFilePicker('file')"><v-icon
                    color="blue-darken-2">mdi-file-document</v-icon></v-btn></template>
            </v-tooltip>
          </div>
        </v-list>
      </v-menu>

      <FilePreviewDialog v-model="showPreview" :file="selectedFile" :initial-caption="messageText"
        :type="selectedFileType" @edit="openEditorFromPreview" @send="onSendFileConfirmed" />
      <ImageEditorModal v-model="showImageEditor" :image-file="editingImageFile" @close="onEditorClose"
        @save="onEditorSave" />

      <!-- حقل الإدخال -->
      <v-textarea ref="inputRef" v-model="messageText" auto-grow bg-color="transparent"
        class="flex-grow-1 text-high-emphasis composer-textarea" density="compact" hide-details max-rows="5"
        :placeholder="$t('chat.input.placeholder')" rounded="lg" rows="1" variant="solo" @input="onTyping"
        @keydown="handleKeydown" @paste="handlePaste">
        <template #append-inner>
          <v-menu v-model="showEmojiPicker" :close-on-content-click="false" location="top end" :offset="[10, 10]">
            <template #activator="{ props: menuProps }">
              <v-btn class="composer-action-btn emoji-toggle-btn" icon size="x-small" variant="text" v-bind="menuProps">
                <v-icon>mdi-emoticon-outline</v-icon>
              </v-btn>
            </template>
            <div class="emoji-picker-container shadow-lg rounded-lg elevation-8 bg-surface border">
              <EmojiPicker class="v3-emoji-picker" :native="true" :static-messages="{}" theme="light"
                @select="onSelectEmoji" />
            </div>
          </v-menu>
        </template>
      </v-textarea>

      <!-- زر الإرسال -->
      <v-btn v-if="messageText.trim()" class="send-btn me-3" color="primary" icon :loading="sending"
        @click="sendMessage">
        <v-icon>mdi-send</v-icon>
      </v-btn>
      <v-btn v-else class="composer-action-btn me-3" icon variant="text" @click="startRecording">
        <v-icon>mdi-microphone-outline</v-icon>
      </v-btn>
    </div>

    <input ref="fileInputRef" :accept="fileAccept" hidden type="file" @change="onFileSelected" />
  </div>
</template>

<script setup>
import { computed, nextTick, onUnmounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useToastStore } from "../../store/toastStore";
import EmojiPicker from "vue3-emoji-picker"


import FilePreviewDialog from "./FilePreviewDialog.vue"
import ImageEditorModal from "../common/ImageEditorModal.vue"

import "vue3-emoji-picker/css";

const toastStore = useToastStore();

const props = defineProps({
  replyTo: { type: Object, default: null },
  sending: { type: Boolean, default: false },
  activeChatId: { type: Number, default: null },
  editingMessage: { type: Object, default: null },
  chatMessages: { type: Array, default: () => [] }, // إضافة الرسائل الحالية للسياق
});

const emit = defineEmits([
  "send",
  "sendFile",
  "cancelReply",
  "typing",
  "saveEdit",
  "cancelEdit",
  "cancelRecording",
]);

const { t } = useI18n();
const messageText = ref("");
const inputRef = ref(null);
const fileInputRef = ref(null);
const fileType = ref("file");
const isRecording = ref(false);
const showEmojiPicker = ref(false);
const showStickerPicker = ref(false);
const isRefining = ref(false);

// Image Editor State
const showImageEditor = ref(false);
const editingImageFile = ref(null);

function onSelectEmoji(emoji) {
  messageText.value += emoji.i;
}

function onSelectSticker(url) {
  emit("send", url, null, "sticker");
  showStickerPicker.value = false;
}

watch(
  () => props.editingMessage,
  (newVal) => {
    if (newVal) {
      messageText.value = newVal.content;
      setTimeout(() => inputRef.value?.focus(), 100);
    } else {
      messageText.value = "";
    }
  }
);

// AI Refine Message Logic (The "Mahdi" System)
async function refineMessage() {
  if (!messageText.value.trim() || isRefining.value) return;
  const original = messageText.value;
  isRefining.value = true;
  toastStore.showInfo("جاري تحسين النص بالذكاء الاصطناعي...");

  // اكتشاف ذكي للأوامر واسم المساعد (مهدي)
  const mahdiRegex = /(مهدي|يا\s*مهدي)/;
  const commandKeywords = [
    "اكتب",
    "اشرح",
    "حل",
    "لخص",
    "ساعدني",
    "برمج",
    "كيف",
    "ما هي",
    "ما هو",
    "ترجم",
  ];
  const isInstruction =
    commandKeywords.some((k) => original.toLowerCase().includes(k)) ||
    mahdiRegex.test(original);

  try {
    const token = localStorage.getItem("token");
    const rootUrl = (
      import.meta.env.VITE_API_URL || window.location.origin
    ).replace(/\/api\/?$/, "");
    const response = await fetch(`${rootUrl}/remote-support/api/ai/chat/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
      body: JSON.stringify({
        prompt: original,
        system_prompt: isInstruction
          ? "أنت خبير تقني ومساعد ذكي. نفذ ما يطلبه المستخدم في النص (شرح، كتابة كود، إجابة) باحترافية عالية وبشكل مباشر جداً وبدون مقدمات."
          : "أنت أداة تحسين صياغة رسائل دردشة. وظيفتك هي إعادة صياغة الرسالة لتكون مهنية، واضحة ومختصرة. لا تجب على الأسئلة، بل حسن صياغتها فقط. أخرج النص المحسن فقط.",
        model: "",
        history: isInstruction
          ? props.chatMessages
            .slice(-5)
            .map((m) => ({
              role: m.sender_id === 0 ? "assistant" : "user",
              content: m.content,
            }))
          : [],
      }),
    });

    if (!response.ok) throw new Error("AI request failed");

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let hasData = false;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      if (!hasData) {
        messageText.value = "";
        hasData = true;
      }

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop();

      for (const line of lines) {
        if (line.trim()) {
          try {
            const data = JSON.parse(line);
            const tokenText = data.message?.content || "";
            let cleanToken = tokenText
              .replace(/```markdown/g, "")
              .replace(/```html/g, "")
              .replace(/```/g, "");
            messageText.value += cleanToken;
          } catch { }
        }
      }
    }
  } catch (error) {
    console.error("Refine error:", error);
    toastStore.showError("فشل تحسين النص بالذكاء الاصطناعي");
  } finally {
    isRefining.value = false;
  }
}

// Recording Logic
const recordingTime = ref(0);
let recordingTimer = null;
let mediaRecorder = null;
let audioChunks = [];
let currentStream = null;

const formattedTime = computed(() => {
  const minutes = Math.floor(recordingTime.value / 60);
  const seconds = recordingTime.value % 60;
  return `${minutes.toString().padStart(2, "0")}:${seconds
    .toString()
    .padStart(2, "0")}`;
});

const fileAccept = computed(() => {
  if (fileType.value === "image") return "image/*";
  if (fileType.value === "video") return "video/*";
  return "*/*";
});

function handleKeydown(event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
  if (event.key === "Escape" && props.editingMessage) emit("cancelEdit");
}

function handlePaste(event) {
  const items = (event.clipboardData || event.originalEvent.clipboardData)
    .items;
  for (const item of items) {
    if (item.kind === "file" && item.type.startsWith("image/")) {
      selectedFile.value = item.getAsFile();
      selectedFileType.value = "image";
      showPreview.value = true;
      event.preventDefault();
      return;
    }
  }
}

function sendMessage() {
  const text = messageText.value.trim();
  if (!text) return;
  if (props.editingMessage) emit("saveEdit", props.editingMessage.id, text);
  else {
    emit("send", text, props.replyTo?.id);
    messageText.value = "";
  }
}

const showPreview = ref(false);
const selectedFile = ref(null);
const selectedFileType = ref("file");

async function openFilePicker(type) {
  fileType.value = type;
  await nextTick();
  if (fileInputRef.value) fileInputRef.value.click();
}

function onFileSelected(event) {
  const file = event.target.files?.[0];
  if (file) {
    selectedFile.value = file;
    selectedFileType.value = file.type.startsWith("image/")
      ? "image"
      : fileType.value;
    showPreview.value = true;
  }
  event.target.value = "";
}

function openEditorFromPreview() {
  editingImageFile.value = selectedFile.value;
  showPreview.value = false;
  showImageEditor.value = true;
}

function onEditorSave(file) {
  selectedFile.value = file;
  selectedFileType.value = "image";
  showImageEditor.value = false;
  showPreview.value = true;
}

function onEditorClose() {
  showImageEditor.value = false;
  showPreview.value = true;
}
function onSendFileConfirmed({ file, type, caption }) {
  emit("sendFile", file, type, caption);
  showPreview.value = false;
  selectedFile.value = null;
  messageText.value = ""; // Clear main text after sending with file
  nextTick(() => inputRef.value?.focus()); // Refocus input
}

let typingTimeout = null;
function onTyping() {
  emit("typing", true);
  if (typingTimeout) clearTimeout(typingTimeout);
  typingTimeout = setTimeout(() => {
    emit("typing", false);
  }, 2000);
}

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    currentStream = stream;
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];
    recordingTime.value = 0;
    mediaRecorder.ondataavailable = (event) => audioChunks.push(event.data);
    mediaRecorder.start();
    isRecording.value = true;
    recordingTimer = setInterval(() => {
      recordingTime.value++;
    }, 1000);
  } catch {
    toastStore.showError(
      "لا يمكن الوصول إلى الميكروفون. يرجى التأكد من السماح للتطبيق."
    );
  }
}

function sendRecording() {
  if (mediaRecorder && isRecording.value) {
    mediaRecorder.onstop = () => {
      const audioFile = new File(
        [new Blob(audioChunks, { type: "audio/webm" })],
        "voice-message.wav",
        { type: "audio/webm" }
      );
      emit("sendFile", audioFile, "audio");
      cleanupRecording();
      nextTick(() => inputRef.value?.focus());
    };
    mediaRecorder.stop();
    isRecording.value = false;
  }
}

function cancelRecording() {
  if (mediaRecorder && isRecording.value) {
    mediaRecorder.onstop = () => {
      cleanupRecording();
    };
    mediaRecorder.stop();
    isRecording.value = false;
  }
}

function cleanupRecording() {
  if (recordingTimer) clearInterval(recordingTimer);
  recordingTimer = null;
  if (currentStream) {
    for (const track of currentStream.getTracks()) track.stop();
    currentStream = null;
  }
  recordingTime.value = 0;
  audioChunks = [];
  mediaRecorder = null;
}

onUnmounted(() => cleanupRecording());
defineExpose({ focus: () => inputRef.value?.focus() });
watch([showPreview, showImageEditor], ([newP, newE], [oldP, oldE]) => {
  // If dialog was open and is now closed, restore focus to input
  if ((oldP && !newP) || (oldE && !newE)) {
    nextTick(() => {
      inputRef.value?.focus();
    });
  }
});
</script>

<style scoped>
.message-input-wrapper {
  position: relative;
  background: transparent;
  padding: 8px 16px 24px 16px;
  /* Increased bottom padding */
  margin-bottom: 8px;
}

.reply-preview,
.edit-preview {
  background: rgba(var(--v-theme-surface), 0.7);
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
  border-inline-start: 4px solid rgba(var(--v-theme-primary), 0.85);
  border-radius: 12px;
  margin-bottom: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.message-input {
  min-height: 56px;
  border-radius: 28px;
  background: rgba(var(--v-theme-surface), 0.85);
  border: 1px solid rgba(var(--v-border-color), 0.08);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  align-items: center !important;
}

.message-input:focus-within {
  box-shadow: 0 12px 32px rgba(var(--v-theme-primary), 0.12);
  border-color: rgba(var(--v-theme-primary), 0.2);
}

.composer-textarea :deep(.v-field) {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  border-radius: 28px !important;
}

.composer-textarea :deep(.v-field__input) {
  padding-top: 14px !important;
  padding-bottom: 14px !important;
  font-size: 0.95rem;
}

.composer-action-btn {
  background: transparent !important;
  color: rgba(var(--v-theme-on-surface), 0.6) !important;
  transition: all 0.25s ease;
}

.composer-action-btn:hover {
  background: rgba(var(--v-theme-primary), 0.08) !important;
  color: rgb(var(--v-theme-primary)) !important;
  transform: scale(1.1);
}

.attachment-menu {
  border: 1px solid rgba(var(--v-border-color), 0.08);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.1) !important;
  border-radius: 20px !important;
  background: rgba(var(--v-theme-surface), 0.9) !important;
}

.attachment-option {
  box-shadow: none !important;
}

.send-btn {
  box-shadow: 0 12px 24px rgba(var(--v-theme-primary), 0.24) !important;
}

.recording-panel {
  min-height: 60px;
  background: linear-gradient(135deg,
      rgba(244, 67, 54, 0.1) 0%,
      rgba(244, 67, 54, 0.05) 100%);
  border: 1px solid rgba(244, 67, 54, 0.18);
}

.recording-dot {
  width: 12px;
  height: 12px;
  background-color: #f44336;
  border-radius: 50%;
  animation: pulse 1s ease-in-out infinite;
}

@keyframes pulse {

  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }

  50% {
    opacity: 0.5;
    transform: scale(0.8);
  }
}

.recording-time {
  font-size: 1.1rem;
  font-family: monospace;
  color: #f44336;
  min-width: 50px;
}
</style>
