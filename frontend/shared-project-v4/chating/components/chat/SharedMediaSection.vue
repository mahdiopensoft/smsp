<template>
  <div class="shared-media-section mt-4">
    <h3 class="text-subtitle-1 font-weight-bold px-2 mb-2">الوسائط والملفات</h3>
    
    <v-tabs
      v-model="activeTab"
      color="primary"
      density="compact"
      grow
      class="border-bottom"
    >
      <v-tab value="media">الوسائط</v-tab>
      <v-tab value="files">الملفات</v-tab>
      <v-tab value="audio">الصوت</v-tab>
    </v-tabs>

    <div class="media-container pa-2">
      <!-- حالة التحميل -->
      <div v-if="isLoading" class="d-flex justify-center align-center py-4">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </div>

      <!-- حالة فارغة -->
      <div v-else-if="!currentItems.length" class="text-center py-4 text-grey">
        لا توجد {{ activeTabName }} مشتركة
      </div>

      <!-- عرض العناصر -->
      <v-window v-else v-model="activeTab" class="mt-2">
        
        <!-- الوسائط (صور وفيديو) -->
        <v-window-item value="media">
          <v-row dense>
            <v-col
              v-for="msg in currentItems"
              :key="msg.id"
              cols="4"
              class="pa-1"
            >
              <v-img
                v-if="msg.message_type === 'image'"
                :src="getFullUrl(msg.file_url || msg.file)"
                aspect-ratio="1"
                cover
                class="rounded bg-grey-lighten-2 cursor-pointer hover-opacity transition-fast"
                @click="openMedia(msg)"
              >
                <template #placeholder>
                  <div class="d-flex align-center justify-center fill-height">
                    <v-progress-circular indeterminate color="grey-lighten-1" size="20"></v-progress-circular>
                  </div>
                </template>
              </v-img>
              <div
                v-else-if="msg.message_type === 'video'"
                class="video-preview rounded bg-grey-darken-3 d-flex align-center justify-center cursor-pointer hover-opacity transition-fast position-relative"
                style="aspect-ratio: 1;"
                @click="openMedia(msg)"
              >
                <v-icon color="white" size="32">mdi-play-circle-outline</v-icon>
                <div class="video-duration px-1 rounded text-caption text-white position-absolute" style="bottom: 4px; right: 4px; background: rgba(0,0,0,0.6)">
                  {{ msg.audio_duration ? formatDuration(msg.audio_duration) : '' }}
                </div>
              </div>
            </v-col>
          </v-row>
        </v-window-item>

        <!-- الملفات -->
        <v-window-item value="files">
          <v-list lines="two" density="compact" class="bg-transparent">
            <v-list-item
              v-for="msg in currentItems"
              :key="msg.id"
              class="mb-2 rounded border"
              @click="downloadFile(getFullUrl(msg.file_url || msg.file), msg.file_name)"
            >
              <template #prepend>
                <div class="file-icon-wrapper rounded d-flex align-center justify-center bg-primary-lighten-5 me-3" style="width: 40px; height: 40px;">
                  <v-icon color="primary">mdi-file-document-outline</v-icon>
                </div>
              </template>
              <v-list-item-title class="font-weight-medium text-body-2">{{ msg.file_name || 'ملف غير معروف' }}</v-list-item-title>
              <v-list-item-subtitle class="text-caption">
                {{ msg.formatted_file_size || 'حجم غير معروف' }} • {{ formatDate(msg.created_at) }}
              </v-list-item-subtitle>
              <template #append>
                <v-btn icon size="small" variant="text" color="grey-darken-1">
                  <v-icon>mdi-download</v-icon>
                </v-btn>
              </template>
            </v-list-item>
          </v-list>
        </v-window-item>

        <!-- الصوتيات -->
        <v-window-item value="audio">
          <v-list lines="two" density="compact" class="bg-transparent">
            <v-list-item
              v-for="msg in currentItems"
              :key="msg.id"
              class="mb-2 rounded border"
            >
              <template #prepend>
                <v-btn icon size="small" color="primary" class="me-3" @click.stop="toggleAudioPlay(msg)">
                  <v-icon>{{ playingAudioId === msg.id ? 'mdi-pause' : 'mdi-play' }}</v-icon>
                </v-btn>
              </template>
              <v-list-item-title class="font-weight-medium text-body-2">رسالة صوتية</v-list-item-title>
              <v-list-item-subtitle class="text-caption">
                {{ msg.audio_duration ? formatDuration(msg.audio_duration) : '' }} • {{ formatDate(msg.created_at) }}
              </v-list-item-subtitle>
              
              <!-- مشغل صوت مخفي للتحكم في التشغيل -->
              <audio v-if="playingAudioId === msg.id" :src="getFullUrl(msg.file_url || msg.file)" autoplay @ended="playingAudioId = null"></audio>
            </v-list-item>
          </v-list>
        </v-window-item>
      </v-window>

      <!-- زر تحميل المزيد -->
      <div v-if="hasMore" class="d-flex justify-center mt-3 mb-2">
        <v-btn
          variant="text"
          color="primary"
          size="small"
          :loading="isLoadingMore"
          @click="loadMore"
        >
          تحميل المزيد
        </v-btn>
      </div>
    </div>

    <!-- Media Viewer Dialog (Lightbox) -->
    <v-dialog v-model="isMediaViewerOpen" max-width="800">
      <v-card v-if="selectedMedia" class="bg-black" rounded="xl">
        <v-toolbar color="transparent" density="compact" class="text-white">
          <v-spacer></v-spacer>
          <v-btn icon="mdi-download" variant="text" @click="downloadFile(getFullUrl(selectedMedia.file_url || selectedMedia.file), selectedMedia.file_name)"></v-btn>
          <v-btn icon="mdi-close" variant="text" @click="isMediaViewerOpen = false"></v-btn>
        </v-toolbar>
        
        <v-card-text class="d-flex justify-center align-center pa-0" style="min-height: 300px;">
          <!-- Image -->
          <v-img
            v-if="selectedMedia.message_type === 'image'"
            :src="getFullUrl(selectedMedia.file_url || selectedMedia.file)"
            max-height="70vh"
            contain
          ></v-img>
          
          <!-- Video -->
          <video
            v-else-if="selectedMedia.message_type === 'video'"
            :src="getFullUrl(selectedMedia.file_url || selectedMedia.file)"
            controls
            autoplay
            style="max-height: 70vh; max-width: 100%;"
          ></video>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useChatStore } from '../../store/chat';
import api from '../../../plugins/axios-plugin';

const props = defineProps({
  chatId: {
    type: [Number, String],
    required: true
  }
});

const emit = defineEmits(['openMedia']);
const chatStore = useChatStore();

const activeTab = ref('media');
const isLoading = ref(false);
const isLoadingMore = ref(false);
const currentPage = ref(1);
const hasMore = ref(false);
const playingAudioId = ref(null);

// حالات المستعرض
const isMediaViewerOpen = ref(false);
const selectedMedia = ref(null);

const activeTabName = computed(() => {
  if (activeTab.value === 'media') return 'وسائط';
  if (activeTab.value === 'files') return 'ملفات';
  return 'صوتيات';
});

// Computed property to get items from the store based on current tab
const currentItems = computed(() => {
  if (!chatStore.sharedMedia[props.chatId]) return [];
  return chatStore.sharedMedia[props.chatId][activeTab.value] || [];
});

// Watch tab changes to fetch data if empty
watch(activeTab, (newVal) => {
  currentPage.value = 1;
  hasMore.value = false;
  
  if (!chatStore.sharedMedia[props.chatId]?.[newVal]?.length) {
    fetchData();
  }
});

// Watch chatId changes (if the dialog stays open and chat changes)
watch(() => props.chatId, () => {
  activeTab.value = 'media';
  currentPage.value = 1;
  fetchData();
});

onMounted(() => {
  fetchData();
});

async function fetchData(isLoadMore = false) {
  if (!props.chatId) return;
  
  if (isLoadMore) {
    isLoadingMore.value = true;
  } else {
    isLoading.value = true;
  }
  
  try {
    const data = await chatStore.fetchSharedMedia(props.chatId, activeTab.value, currentPage.value);
    // التحقق مما إذا كان هناك صفحات أخرى
    if (data && data.next) {
      hasMore.value = true;
    } else {
      hasMore.value = false;
    }
  } catch (error) {
    console.error('Error fetching shared media:', error);
  } finally {
    isLoading.value = false;
    isLoadingMore.value = false;
  }
}

function loadMore() {
  if (isLoadingMore.value) return;
  currentPage.value += 1;
  fetchData(true);
}

function openMedia(msg) {
  selectedMedia.value = msg;
  isMediaViewerOpen.value = true;
  emit('openMedia', msg);
}

async function downloadFile(url, filename) {
  if (!url) return;
  try {
    const response = await fetch(url);
    const blob = await response.blob();
    const blobUrl = URL.createObjectURL(blob);
    
    const link = document.createElement("a");
    if (!filename) {
      filename = url.split("/").pop();
    }
    
    link.href = blobUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    
    document.body.removeChild(link);
    URL.revokeObjectURL(blobUrl);
  } catch (error) {
    console.error("Download failed", error);
    window.open(url, '_blank');
  }
}

function toggleAudioPlay(msg) {
  if (playingAudioId.value === msg.id) {
    playingAudioId.value = null; // pause
  } else {
    playingAudioId.value = msg.id; // play
  }
}

function formatDuration(seconds) {
  if (!seconds) return '0:00';
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function formatDate(dateString) {
  if (!dateString) return '';
  const d = new Date(dateString);
  return d.toLocaleDateString('ar-EG');
}

function getFullUrl(url) {
  if (!url) return '';
  if (url.startsWith('http')) return url;
  
  // Extract base URL from api config (e.g. "http://localhost:8006/api/v1" -> "http://localhost:8006")
  let baseUrl = api.defaults.baseURL || '';
  if (baseUrl.includes('/api')) {
    baseUrl = baseUrl.split('/api')[0];
  }
  
  // Clean trailing and leading slashes to prevent double slashes
  if (baseUrl.endsWith('/')) {
    baseUrl = baseUrl.slice(0, -1);
  }
  
  return baseUrl + (url.startsWith('/') ? url : '/' + url);
}
</script>

<style scoped>
.shared-media-section {
  max-height: 400px;
  display: flex;
  flex-direction: column;
}

.media-container {
  overflow-y: auto;
  max-height: 300px;
}

.hover-opacity:hover {
  opacity: 0.85;
}

.transition-fast {
  transition: all 0.2s ease;
}

.border-bottom {
  border-bottom: 1px solid rgba(var(--v-border-color), 0.1);
}
</style>
