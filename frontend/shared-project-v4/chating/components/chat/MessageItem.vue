<template>
  <div
    :id="`message-${message.id}`"
    class="message-item d-flex mb-1 w-100"
    :class="{
      'justify-start message-item--own': isOwn,
      'justify-end message-item--other': !isOwn,
    }"
    :data-id="message.id"
  >
    <!-- صورة المرسل (للمجموعات فقط) -->
    <UserAvatar
      v-if="showAvatar && !isOwn"
      class="me-2 mt-auto mb-1"
      :name="senderName"
      :size="28"
      :src="message.sender?.profile_picture || message.sender?.image_user"
    />

    <!-- فقاعة الرسالة -->
    <div
      class="message-bubble"
      :class="bubbleClass"
      @contextmenu.prevent="$emit('contextMenu', $event, message)"
    >
      <!-- علامة محولة -->
      <div
        v-if="message.is_forwarded"
        class="forwarded-label d-flex align-center mb-1"
      >
        <v-icon class="me-1" size="14" style="transform: scaleX(-1)"
          >mdi-reply</v-icon
        >
        <span class="text-caption italic">{{
          $t("chat.forwarded") || "محولة"
        }}</span>
      </div>
      <!-- اسم المرسل (للمجموعات) -->
      <p
        v-if="showSenderName && !isOwn"
        class="sender-name font-weight-medium mb-1"
      >
        {{ senderName }}
      </p>

      <!-- الرد على رسالة -->
      <div
        v-if="message.reply_to"
        class="reply-preview pa-2 mb-2 rounded"
        @click="$emit('goToReply', message.reply_to.id)"
      >
        <p class="font-weight-medium mb-0">
          {{ message.reply_to.sender?.username }}
        </p>
        <p class="text-truncate mb-0">
          {{ message.reply_to.content }}
        </p>
      </div>

      <!-- محتوى الرسالة حسب النوع -->
      <template v-if="message.message_type === 'text'">
        <div
          class="message-content mb-0 markdown-body"
          :class="{ 'text-right': isRTL(message.content) }"
          v-html="renderMarkdown(message.content)"
        />
      </template>

      <template v-else-if="message.message_type === 'image'">
        <div class="position-relative">
          <v-img
            :aspect-ratio="4 / 3"
            class="message-image rounded mb-1 cursor-pointer bg-grey-lighten-2"
            cover
            :src="message.file"
            width="300"
            @click="$emit('viewImage', message.file)"
          >
            <template #placeholder>
              <div class="d-flex align-center justify-center fill-height">
                <div class="app-loader-spinner app-loader--sm"></div>
              </div>
            </template>
          </v-img>

          <!-- زر التحميل للصورة -->
          <v-btn
            class="download-btn"
            color="rgba(0,0,0,0.5)"
            icon
            size="small"
            variant="flat"
            @click.stop="downloadFile(message.file)"
          >
            <v-icon color="white" size="20">mdi-download</v-icon>
            <v-tooltip activator="parent" location="top">تحميل</v-tooltip>
          </v-btn>
        </div>
        <div
          v-if="message.content"
          class="message-content mb-0 markdown-body"
          :class="{ 'text-right': isRTL(message.content) }"
          v-html="renderMarkdown(message.content)"
        />
      </template>

      <template v-else-if="message.message_type === 'video' && !isVoiceMessage">
        <div class="position-relative">
          <video
            class="message-video rounded mb-1"
            controls
            preload="metadata"
            :src="message.file"
          />
          <!-- زر التحميل للفيديو - يظهر بجانب الفيديو أو فوقه -->
          <v-btn
            class="download-btn"
            color="rgba(0,0,0,0.5)"
            icon
            size="small"
            style="top: 10px; left: 10px"
            variant="flat"
            @click.stop="downloadFile(message.file)"
          >
            <v-icon color="white" size="20">mdi-download</v-icon>
            <v-tooltip activator="parent" location="top">تحميل</v-tooltip>
          </v-btn>
        </div>
        <div
          v-if="message.content"
          class="message-content mb-0 markdown-body"
          :class="{ 'text-right': isRTL(message.content) }"
          v-html="renderMarkdown(message.content)"
        />
      </template>

      <template v-else-if="isVoiceMessage">
        <div class="premium-audio-player d-flex align-center gap-2 pa-2" :class="isOwn ? 'own-audio' : 'other-audio'">
          <!-- زر التشغيل -->
          <v-btn
            :color="isOwn ? 'white' : 'primary'"
            icon
            size="40"
            variant="flat"
            class="elevation-1 flex-shrink-0"
            @click="toggleAudio"
          >
            <v-icon size="24" :color="isOwn ? 'primary' : 'white'">{{ isPlaying ? "mdi-pause" : "mdi-play" }}</v-icon>
          </v-btn>
          
          <div class="audio-controls-wrapper flex-grow-1 d-flex flex-column justify-center" style="min-width: 0;">
            <!-- شريط التقدم (Slider) -->
            <v-slider
              v-model="audioProgress"
              :color="isOwn ? 'white' : 'primary'"
              :track-color="isOwn ? 'rgba(255,255,255,0.3)' : 'rgba(var(--v-theme-primary), 0.2)'"
              thumb-size="10"
              track-size="3"
              hide-details
              class="audio-slider mx-1"
              @update:model-value="seekAudio"
              @mousedown="isDragging = true"
              @mouseup="isDragging = false"
              @touchstart="isDragging = true"
              @touchend="isDragging = false"
            ></v-slider>
            
            <!-- المدة الزمنية -->
            <div class="d-flex justify-space-between text-caption px-2" :class="isOwn ? 'text-white' : 'text-grey-darken-1'" style="margin-top: -6px;">
              <span class="font-weight-medium" dir="ltr">{{ formatDuration(currentAudioTime) }}</span>
              <span class="font-weight-medium" dir="ltr">{{ formatDuration(message.audio_duration || totalAudioDuration) }}</span>
            </div>
          </div>
        </div>
        <audio
          ref="audioRef"
          :src="getFullUrl(message.file_url || message.file)"
          @ended="onAudioEnded"
          @timeupdate="onTimeUpdate"
          @loadedmetadata="onLoadedMetadata"
        />
      </template>

      <template v-else-if="message.message_type === 'file'">
        <div
          class="file-message d-flex align-center gap-3 pa-2 rounded position-relative"
        >
          <!-- أيقونة الملف / زر التحميل -->
          <div
            class="file-icon-wrapper d-flex align-center justify-center position-relative"
          >
            <div
              class="extension-badge font-weight-bold text-uppercase text-white"
            >
              {{ getFileExtension(message.file_name) }}
            </div>

            <v-btn
              class="download-overlay"
              color="rgba(0,0,0,0.3)"
              icon
              :loading="isDownloading"
              size="small"
              variant="flat"
              @click.stop="downloadFile(message.file, message.file_name)"
            >
              <v-icon color="white">mdi-download</v-icon>
            </v-btn>
          </div>

          <!-- تفاصيل الملف -->
          <div class="flex-grow-1" style="min-width: 0; overflow: hidden;">
            <p class="font-weight-bold mb-0 text-truncate" dir="auto">
              {{ message.file_name }}
            </p>
            <div class="d-flex align-center gap-2 mt-1 text-secondary">
              {{ message.formatted_file_size }}
            </div>
          </div>
        </div>
        <div
          v-if="message.content"
          class="message-content mt-2 markdown-body"
          :class="{ 'text-right': isRTL(message.content) }"
          v-html="renderMarkdown(message.content)"
        />
      </template>

      <template v-else-if="message.message_type === 'sticker'">
        <div class="sticker-message pa-1">
          <v-img
            class="mx-auto"
            contain
            height="120"
            :src="message.content"
            width="120"
          />
        </div>
      </template>

      <!-- وقت الرسالة وحالة التسليم -->
      <div class="message-info d-flex align-center justify-end mt-1">
        <v-icon
          v-if="message.is_starred"
          class="me-1"
          color="amber-darken-1"
          size="12"
          >mdi-star</v-icon
        >
        <span class="message-time">{{ formattedTime }}</span>
        <v-icon v-if="isOwn" class="ms-1" :color="statusColor" size="16">
          {{ statusIcon }}
        </v-icon>
      </div>

      <!-- التفاعلات -->
      <div
        v-if="message.reactions && message.reactions.length > 0"
        class="message-reactions-container"
      >
        <div class="message-reactions d-flex align-center">
          <v-menu
            v-model="showReactorsDialog"
            :close-on-content-click="false"
            location="top"
            max-width="320"
          >
            <template #activator="{ props: menuProps }">
              <div
                v-bind="menuProps"
                class="reaction-chip"
                :class="{ 'reaction-chip--active': hasAnyReaction }"
              >
                <div class="d-flex align-center" style="gap: 2px">
                  <span
                    v-for="(count, emoji) in reactionCounts"
                    :key="emoji"
                    class="reaction-emoji"
                    >{{ emoji }}</span
                  >
                  <span v-if="totalReactions > 1" class="reaction-count ms-1">{{
                    totalReactions
                  }}</span>
                </div>
              </div>
            </template>
            <v-card class="rounded-lg">
              <v-card-title class="text-subtitle-1 font-weight-bold pa-3 border-b">
                التفاعلات ({{ message.reactions?.length || 0 }})
              </v-card-title>
              <v-list
                class="pa-0"
                density="compact"
                max-height="300"
                style="overflow-y: auto"
              >
                <v-list-item
                  v-for="r in message.reactions"
                  :key="r.id"
                  class="px-4 py-2 border-b"
                >
                  <template #prepend>
                    <span class="text-h5 me-3">{{ r.emoji }}</span>
                  </template>
                  <v-list-item-title class="font-weight-medium">
                    {{ r.user?.username || r.user?.full_name || "مستخدم" }}
                  </v-list-item-title>
                  <template v-if="r.user?.id == currentUserId" #append>
                    <v-btn
                      icon
                      size="x-small"
                      variant="text"
                      color="error"
                      @click.stop="$emit('react', r.emoji); showReactorsDialog = false"
                    >
                      <v-icon size="14">mdi-close-circle</v-icon>
                      <v-tooltip activator="parent" location="top">إلغاء تفاعلك</v-tooltip>
                    </v-btn>
                  </template>
                </v-list-item>
              </v-list>
              <v-card-actions class="pa-2">
                <v-spacer />
                <v-btn
                  color="primary"
                  variant="text"
                  @click="showReactorsDialog = false"
                  >إغلاق</v-btn
                >
              </v-card-actions>
            </v-card>
          </v-menu>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import UserAvatar from '../common/UserAvatar.vue'
import { renderMarkdown } from "../../utils/markdown";
import api from "../../../plugins/axios-plugin";

const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
  currentUserId: {
    type: Number,
    default: null,
  },
  showAvatar: {
    type: Boolean,
    default: false,
  },
  showSenderName: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["contextMenu", "viewImage", "goToReply", "react"]);

// حالة الصوت
const audioRef = ref(null);
const isPlaying = ref(false);
const audioProgress = ref(0);
const isDragging = ref(false);
const currentAudioTime = ref(0);
const totalAudioDuration = ref(0);
const isDownloading = ref(false);
const showReactorsDialog = ref(false);

// هل الرسالة مني؟
const isOwn = computed(() => props.message.sender?.id == props.currentUserId);
const hasReactions = computed(() => props.message.reactions && props.message.reactions.length > 0);

const isVoiceMessage = computed(() => {
  return props.message.message_type === 'audio' || 
    (props.message.message_type === 'video' && props.message.file_name?.includes('voice-message'));
});

// الحروف الأولى للاسم
const avatarText = computed(() => {
  const sender = props.message.sender;
  if (!sender) return "";
  return sender.full_name || sender.username || "";
});

// اسم المرسل
const senderName = computed(() => {
  const sender = props.message.sender;
  if (!sender) return "";
  return sender.full_name || sender.username || "";
});

// كلاس الفقاعة
const bubbleClass = computed(() => ({
  "message-bubble--sent": isOwn.value,
  "message-bubble--received": !isOwn.value,
  "message-bubble--deleted": props.message.is_deleted,
}));

// تنسيق الوقت
const formattedTime = computed(() => {
  const date = new Date(props.message.created_at);
  return date.toLocaleTimeString("ar", { hour: "2-digit", minute: "2-digit" });
});

// حالة الرسالة
const statusIcon = computed(() => {
  if (props.message.is_deleted) return "mdi-cancel";
  if (props.message.is_read) return "mdi-check-all";
  if (props.message.is_delivered) return "mdi-check-all";
  return "mdi-check";
});

const statusColor = computed(() => {
  if (props.message.is_read) return "info";
  return "white";
});

// تشغيل/إيقاف الصوت
function toggleAudio() {
  if (audioRef.value) {
    if (isPlaying.value) {
      audioRef.value.pause();
    } else {
      audioRef.value.play();
    }
    isPlaying.value = !isPlaying.value;
  }
}

function onTimeUpdate() {
  if (audioRef.value && !isDragging.value) {
    currentAudioTime.value = audioRef.value.currentTime;
    if (audioRef.value.duration) {
      audioProgress.value = (audioRef.value.currentTime / audioRef.value.duration) * 100;
    }
  }
}

function onLoadedMetadata() {
  if (audioRef.value) {
    totalAudioDuration.value = audioRef.value.duration;
  }
}

function seekAudio(value) {
  if (audioRef.value && audioRef.value.duration) {
    const newTime = (value / 100) * audioRef.value.duration;
    audioRef.value.currentTime = newTime;
    currentAudioTime.value = newTime;
  }
}

function onAudioEnded() {
  isPlaying.value = false;
  audioProgress.value = 0;
  currentAudioTime.value = 0;
}

// تنسيق المدة
function formatDuration(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, "0")}`;
}

// الحصول على امتداد الملف
function getFileExtension(filename) {
  if (!filename) return "FILE";
  const ext = filename.split(".").pop();
  return ext.length > 4 ? "FILE" : ext;
}

// فحص اتجاه النص
function isRTL(text) {
  if (!text) return false;
  const rtlChars = /[\u0600-\u06FF]/;
  return rtlChars.test(text);
}

// حساب التفاعلات
const reactionCounts = computed(() => {
  if (!props.message.reactions) return {};
  return props.message.reactions
    .filter((r) => r && r.emoji)
    .reduce((acc, r) => {
      acc[r.emoji] = (acc[r.emoji] || 0) + 1;
      return acc;
    }, {});
});

const totalReactions = computed(() => {
  if (!props.message.reactions) return 0;
  return props.message.reactions.filter((r) => r && r.emoji).length;
});

const hasAnyReaction = computed(() => {
  if (!props.message.reactions) return false;
  return props.message.reactions.some(
    (r) => r && r.emoji && r.user?.id == props.currentUserId
  );
});

function hasUserReacted(emoji) {
  if (!props.message.reactions) return false;
  return props.message.reactions.some(
    (r) => r && r.emoji === emoji && r.user?.id == props.currentUserId
  );
}

function getReactorsText(emoji) {
  if (!props.message.reactions) return "";
  const reactors = props.message.reactions
    .filter((r) => r && r.emoji === emoji)
    .map((r) => r.user?.username || r.user?.full_name || "مستخدم");
  return reactors.join("، ");
}

// تحميل الملف
async function downloadFile(url, filename) {
  if (!url) return;

  isDownloading.value = true;
  try {
    const response = await fetch(url);
    const blob = await response.blob();
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);

    // محاولة استخراج الاسم من الرابط إذا لم يتوفر
    if (!filename) {
      filename = url.split("/").pop();
    }

    link.download = filename;
    document.body.append(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(link.href);
  } catch (error) {
    console.error("Download failed", error);
    window.open(url, "_blank");
  } finally {
    isDownloading.value = false;
  }
}

function getFullUrl(url) {
  if (!url) return '';
  if (url.startsWith('http')) return url;
  
  // Extract base URL from api config
  let baseUrl = api.defaults.baseURL || '';
  if (baseUrl.includes('/api')) {
    baseUrl = baseUrl.split('/api')[0];
  }
  
  if (baseUrl.endsWith('/')) {
    baseUrl = baseUrl.slice(0, -1);
  }
  
  return baseUrl + (url.startsWith('/') ? url : '/' + url);
}
</script>

<style scoped>
.message-bubble {
  padding: 12px 16px 10px;
  border-radius: 20px;
  max-width: min(100%, 720px);
  word-wrap: break-word;
  position: relative;
  border: 1px solid transparent;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.message-bubble--sent {
  background-color: rgb(var(--v-theme-primary));
  color: white !important;
  border-end-start-radius: 4px;
  box-shadow: 0 6px 16px rgba(var(--v-theme-primary), 0.2);
}

.message-bubble--received {
  background-color: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-border-color), 0.15);
  border-end-end-radius: 4px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.message-bubble--deleted {
  opacity: 0.5;
  font-style: italic;
  background-color: transparent !important;
  border: 1px dashed rgba(var(--v-border-color), 0.3);
  box-shadow: none !important;
}

.message-item--own {
  padding-inline-end: 56px;
}

.message-item--other {
  padding-inline-start: 56px;
}

.message-info {
  font-size: 0.72rem;
  opacity: 0.9;
  margin-top: 2px;
}

.forwarded-label {
  opacity: 0.8;
  font-size: 0.75rem;
  font-style: italic;
  color: rgba(var(--v-theme-on-surface), 0.6);
  margin-bottom: 2px;
}

.message-item--own .forwarded-label {
  color: rgba(255, 255, 255, 0.85);
}

.message-reactions-container {
  position: absolute;
  bottom: -14px;
  inset-inline-end: 10px;
  z-index: 2;
}

.message-item--other .message-reactions-container {
  inset-inline-start: 10px;
  inset-inline-end: auto;
}

.reaction-chip {
  background: rgba(var(--v-theme-surface), 0.96);
  border: 1px solid rgba(var(--v-border-color), 0.12);
  border-radius: 999px;
  padding: 3px 7px;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.75rem;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
  transition: all 0.2s;
}

.reaction-chip:hover {
  transform: translateY(-1px);
  background: rgba(var(--v-theme-primary), 0.06);
}

.reaction-chip--active {
  background: rgba(var(--v-theme-primary), 0.1);
  border-color: rgba(var(--v-theme-primary), 0.2);
}

.reaction-emoji {
  font-size: 1rem;
}

.reaction-count {
  font-weight: bold;
  color: rgba(var(--v-theme-on-surface), 0.64);
}

.sender-name {
  color: rgb(var(--v-theme-primary));
}

.reply-preview {
  background-color: rgba(var(--v-theme-on-surface), 0.05);
  border-inline-start: 3px solid rgb(var(--v-theme-primary));
  cursor: pointer;
}

.message-content {
  white-space: pre-wrap;
  word-break: break-word;
}

.message-image {
  max-height: 300px;
}

.message-video {
  max-width: 300px;
  max-height: 300px;
}

.premium-audio-player {
  min-width: 240px;
  max-width: 100%;
  overflow: hidden;
}

.premium-audio-player .audio-slider {
  margin-top: 2px;
}

/* تعديل الـ Slider ليصبح أكثر سمكاً وجاذبية */
:deep(.audio-slider .v-slider-track__background) {
  opacity: 0.3 !important;
}

:deep(.audio-slider .v-slider-thumb) {
  box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
}

.file-message {
  background-color: rgba(var(--v-theme-on-surface), 0.04);
  min-width: 260px;
  max-width: 100%;
  overflow: hidden;
}

.file-icon-wrapper {
  width: 48px;
  height: 48px;
  background: linear-gradient(
    135deg,
    rgba(var(--v-theme-primary), 1),
    rgba(var(--v-theme-info), 0.92)
  );
  border-radius: 12px;
  flex-shrink: 0;
}

.download-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 12px;
  opacity: 0;
  transition: opacity 0.2s;
  display: flex !important;
  align-items: center;
  justify-content: center;
}

.file-message:hover .download-overlay {
  opacity: 1;
}

/* في الموبايل، دائماً أظهر زر التحميل إذا لم يكن هناك فارة */
@media (hover: none) {
  .download-overlay {
    background-color: transparent;
    opacity: 1;
  }
}

.message-time {
  font-size: 11px;
  color: inherit;
  opacity: 0.72;
}

.cursor-pointer {
  cursor: pointer;
}

.download-btn {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: opacity 0.2s;
}

.position-relative:hover .download-btn {
  opacity: 1;
}

/* تنسيقات Markdown */
:deep(.markdown-body) {
  font-size: 15px;
  line-height: 1.1;
}

:deep(.markdown-body p) {
  margin-bottom: 0.2em;
}

:deep(.markdown-body p:last-child) {
  margin-bottom: 0;
}

:deep(.markdown-body a) {
  color: rgb(var(--v-theme-primary));
  text-decoration: underline;
}

:deep(.message-bubble--sent .markdown-body a) {
  color: rgba(255, 255, 255, 0.92);
}

:deep(.markdown-body pre) {
  background-color: rgba(15, 23, 42, 0.92) !important;
  border-radius: 6px;
  padding: 12px;
  margin: 8px 0;
  overflow-x: auto;
  direction: ltr;
  text-align: left;
}

:deep(.markdown-body code) {
  font-family: "Consolas", "Monaco", "Courier New", monospace;
  font-size: 13px;
  border-radius: 4px;
}

/* الكود المضمن (Inline Code) */
:deep(.markdown-body :not(pre) > code) {
  background-color: rgba(var(--v-theme-on-surface), 0.08);
  padding: 2px 4px;
  color: inherit;
}

:deep(.message-bubble--sent .markdown-body :not(pre) > code) {
  background-color: rgba(255, 255, 255, 0.16);
}

:deep(.markdown-body ul),
:deep(.markdown-body ol) {
  padding-inline-start: 24px;
  margin-bottom: 0.5em;
}

:deep(.markdown-body blockquote) {
  border-inline-start: 4px solid rgba(var(--v-theme-on-surface), 0.35);
  margin: 8px 0;
  padding-inline-start: 12px;
  opacity: 0.8;
}

:deep(.message-bubble--sent .markdown-body blockquote) {
  border-left-color: rgba(255, 255, 255, 0.5);
}

.text-right {
  text-align: right;
  direction: rtl;
}

@media (max-width: 600px) {
  .message-item--own,
  .message-item--other {
    padding-inline: 0;
  }

  .message-bubble {
    max-width: calc(100vw - 96px);
  }
}
</style>
