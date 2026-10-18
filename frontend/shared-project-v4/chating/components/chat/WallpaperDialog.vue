<template>
  <custom-dialog
    v-model="internalValue"
    width="600"
    height="auto"
    :title="$t('chat.wallpaper.title') || 'خلفية الدردشة'"
  >
    <div class="overflow-hidden">
        <v-tabs v-model="activeTab" bg-color="surface" color="primary" grow>
          <v-tab value="presets">{{
            $t("chat.wallpaper.presets") || "خلفيات جاهزة"
          }}</v-tab>
          <v-tab value="custom">{{
            $t("chat.wallpaper.custom") || "صورة خاصة"
          }}</v-tab>
        </v-tabs>

        <v-window
          v-model="activeTab"
          class="pa-4"
          style="max-height: 400px; overflow-y: auto"
        >
          <!-- الخلفيات الجاهزة -->
          <v-window-item value="presets">
            <p class="text-subtitle-2 mb-3 text-medium-emphasis">ألوان صلبة</p>
            <div class="wallpaper-grid mb-6">
              <div
                v-for="color in solidColors"
                :key="color"
                class="wallpaper-item color-item"
                :class="{
                  'wallpaper-item--active': currentWallpaper === color,
                }"
                :style="{ backgroundColor: color }"
                @click="previewWallpaper(color)"
              >
                <v-icon
                  v-if="currentWallpaper === color"
                  color="white"
                  size="32"
                  >mdi-check-circle</v-icon
                >
              </div>
            </div>

            <p class="text-subtitle-2 mb-3 text-medium-emphasis">
              مناظر طبيعية
            </p>
            <div class="wallpaper-grid">
              <div
                v-for="image in sampleWallpapers"
                :key="image"
                class="wallpaper-item image-item"
                :class="{
                  'wallpaper-item--active': currentWallpaper === image,
                }"
                :style="{ backgroundImage: `url(${image})` }"
                @click="previewWallpaper(image)"
              >
                <v-icon
                  v-if="currentWallpaper === image"
                  class="check-shadow"
                  color="white"
                  size="32"
                  >mdi-check-circle</v-icon
                >
              </div>

              <!-- إزالة الخلفية -->
              <div
                class="wallpaper-item default-item d-flex flex-column align-center justify-center border-dashed"
                :class="{ 'wallpaper-item--active': !currentWallpaper }"
                @click="previewWallpaper(null)"
              >
                <v-icon color="grey" size="32">mdi-image-off-outline</v-icon>
                <span class="text-caption mt-1">بدون خلفية</span>
              </div>
            </div>
          </v-window-item>

          <!-- رفع صورة خاصة -->
          <v-window-item value="custom">
            <div
              class="upload-area d-flex flex-column align-center justify-center pa-8 border-dashed rounded-lg"
              @click="$refs.fileInput.click()"
              @dragover.prevent
              @drop.prevent="handleDrop"
            >
              <v-icon class="mb-4" color="primary" size="64"
                >mdi-cloud-upload-outline</v-icon
              >
              <h3 class="text-h6 mb-2">اختر صورة من جهازك</h3>
              <p class="text-body-2 text-center text-medium-emphasis mb-4">
                اسحب الصورة هنا أو انقر للاختيار <br />
                (يدعم JPG, PNG, WebP)
              </p>
              <custom-btn
                color="primary"
                icon="mdi-folder-open"
                :click="() => $refs.fileInput.click()"
                label="تصفح الملفات"
              />
              <input
                ref="fileInput"
                accept="image/*"
                class="d-none"
                type="file"
                @change="handleFileSelect"
              />
            </div>

            <div v-if="customPreview" class="mt-6 text-center">
              <p class="text-subtitle-2 mb-2">معاينة الصورة المختارة:</p>
              <v-img
                class="rounded-lg mx-auto"
                cover
                max-height="200"
                max-width="300"
                :src="customPreview"
              />
              <custom-btn
                class="mt-3"
                color="primary"
                variant="tonal"
                :click="() => previewWallpaper(customPreview)"
                label="معاينة على المحادثة"
              />
            </div>
          </v-window-item>
        </v-window>
    </div>

    <template #actions>
      <div class="d-flex w-100 flex-column flex-sm-row align-center w-100">
        <p class="text-caption text-medium-emphasis ps-2 mb-0 text-start">
          * سيتم تطبيق التغييرات فوراً للمعاينة، اضغط "حفظ" للتثبيت.
        </p>
        <v-spacer class="d-none d-sm-flex" />
        <div class="d-flex mt-3 mt-sm-0">
          <custom-btn type="cancel" :click="cancel" :label="$t('common.cancel') || 'إلغاء'" />
          <custom-btn
            color="primary"
            variant="flat"
            class="ms-2"
            :loading="loading"
            :click="saveWallpaper"
            :label="$t('common.save') || 'حفظ'"
          />
        </div>
      </div>
    </template>
  </custom-dialog>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useChatStore } from "../../store/chat";

const props = defineProps({
  modelValue: Boolean,
  chat: Object,
});

const emit = defineEmits(["update:modelValue", "preview"]);

const chatStore = useChatStore();
const loading = ref(false);
const activeTab = ref("presets");
const originalWallpaper = ref(props.chat?.wallpaper || null);
const currentWallpaper = ref(props.chat?.wallpaper || null);
const customPreview = ref(null);

const internalValue = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});

// تحديث القيم عند فتح الديالوج
watch(
  () => props.modelValue,
  (isOpen) => {
    if (isOpen) {
      originalWallpaper.value = props.chat?.wallpaper || null;
      currentWallpaper.value = props.chat?.wallpaper || null;
    }
  }
);

const solidColors = [
  "#e5ddd5",
  "#fce4ec",
  "#f3e5f5",
  "#e8eaf6",
  "#e3f2fd",
  "#e0f2f1",
  "#e8f5e9",
  "#fffde7",
  "#fff3e0",
  "#efebe9",
  "#263238",
  "#1a1a1a",
  "#2c3e50",
  "#004d40",
];

const sampleWallpapers = [
  "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800",
  "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800",
  "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800",
  "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=800",
  "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800",
  "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=800",
];

function previewWallpaper(wp) {
  currentWallpaper.value = wp;
  // إرسال إشارة للمعاينة اللحظية في الخلفية
  emit("preview", wp);
}

function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) {
    processFile(file);
  }
}

function handleDrop(e) {
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith("image/")) {
    processFile(file);
  }
}

function processFile(file) {
  const reader = new FileReader();
  reader.addEventListener("load", (e) => {
    customPreview.value = e.target.result;
    // معاينة فورية عند الرفع
    previewWallpaper(e.target.result);
  });
  reader.readAsDataURL(file);
}

async function saveWallpaper() {
  if (!props.chat?.id) return;

  loading.value = true;
  try {
    await chatStore.updateChatWallpaper(props.chat.id, currentWallpaper.value);
    originalWallpaper.value = currentWallpaper.value;
    emit("preview", null);
    internalValue.value = false;
  } catch (error) {
    console.error("Failed to save wallpaper", error);
  } finally {
    loading.value = false;
  }
}

function cancel() {
  emit("preview", null);
  internalValue.value = false;
}
</script>

<style scoped>
.wallpaper-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 16px;
}

.wallpaper-item {
  aspect-ratio: 9 / 16;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 3px solid transparent;
  background-size: cover;
  background-position: center;
  position: relative;
  overflow: hidden;
}

.wallpaper-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.wallpaper-item--active {
  border-color: var(--v-theme-primary);
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.3);
}

.check-shadow {
  filter: drop-shadow(0 0 4px rgba(0, 0, 0, 0.8));
}

.border-dashed {
  border: 2px dashed rgba(var(--v-theme-on-surface), 0.2);
}

.upload-area {
  cursor: pointer;
  transition: all 0.2s;
}

.upload-area:hover {
  background-color: rgba(var(--v-theme-primary), 0.05);
  border-color: var(--v-theme-primary);
}

.glass-panel {
  background: rgba(var(--v-theme-surface), 0.9) !important;
}
</style>
