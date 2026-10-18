<template>
  <div class="sticker-picker bg-surface rounded-lg elevation-4 overflow-hidden d-flex flex-column">
    <!-- محتوى الملصقات -->
    <div class="sticker-content pa-2 flex-grow-1 overflow-y-auto">
      <v-window v-model="activeTab">
        <v-window-item value="recent">
          <div class="sticker-grid">
            <div
              v-for="(sticker, i) in recentStickers"
              :key="i"
              class="sticker-item"
              @click="selectSticker(sticker)"
            >
              <v-img contain height="65" :src="sticker" width="65" />
            </div>
          </div>
          <div v-if="recentStickers.length === 0" class="text-center py-8 text-disabled">
            {{ $t('chat.stickers.noRecent') || 'لا توجد ملصقات حديثة' }}
          </div>
        </v-window-item>

        <v-window-item value="dev">
          <div class="sticker-grid">
            <div v-for="(sticker, i) in devPack" :key="i" class="sticker-item" @click="selectSticker(sticker)">
              <v-img contain height="65" :src="sticker" width="65" />
            </div>
          </div>
        </v-window-item>

        <v-window-item value="tech">
          <div class="sticker-grid">
            <div v-for="(sticker, i) in techPack" :key="i" class="sticker-item" @click="selectSticker(sticker)">
              <v-img contain height="65" :src="sticker" width="65" />
            </div>
          </div>
        </v-window-item>

        <v-window-item value="transport">
          <div class="sticker-grid">
            <div v-for="(sticker, i) in transportPack" :key="i" class="sticker-item" @click="selectSticker(sticker)">
              <v-img contain height="65" :src="sticker" width="65" />
            </div>
          </div>
        </v-window-item>

        <v-window-item value="bots">
          <div class="sticker-grid">
            <div v-for="(sticker, i) in botPack" :key="i" class="sticker-item" @click="selectSticker(sticker)">
              <v-img contain height="65" :src="sticker" width="65" />
            </div>
          </div>
        </v-window-item>

        <v-window-item value="avatars">
          <div class="sticker-grid">
            <div v-for="(sticker, i) in avatarPack" :key="i" class="sticker-item" @click="selectSticker(sticker)">
              <v-img contain height="65" :src="sticker" width="65" />
            </div>
          </div>
        </v-window-item>

        <v-window-item value="nature">
          <div class="sticker-grid">
            <div v-for="(sticker, i) in naturePack" :key="i" class="sticker-item" @click="selectSticker(sticker)">
              <v-img contain height="65" :src="sticker" width="65" />
            </div>
          </div>
        </v-window-item>

        <v-window-item value="food">
          <div class="sticker-grid">
            <div v-for="(sticker, i) in foodPack" :key="i" class="sticker-item" @click="selectSticker(sticker)">
              <v-img contain height="65" :src="sticker" width="65" />
            </div>
          </div>
        </v-window-item>
      </v-window>
    </div>

    <!-- شريط الفئات في الأسفل (مثل واتساب) -->
    <v-tabs
      v-model="activeTab"
      bg-color="surface"
      class="border-t"
      color="primary"
      density="comfortable"
      height="52"
      show-arrows
      slider-color="primary"
    >
      <v-tab value="recent"><v-icon size="24">mdi-history</v-icon></v-tab>
      <v-tab value="dev"><v-icon size="24">mdi-code-braces</v-icon></v-tab>
      <v-tab value="tech"><v-icon size="24">mdi-laptop</v-icon></v-tab>
      <v-tab value="transport"><v-icon size="24">mdi-truck-delivery</v-icon></v-tab>
      <v-tab value="bots"><v-icon size="24">mdi-robot-outline</v-icon></v-tab>
      <v-tab value="avatars"><v-icon size="24">mdi-account-circle-outline</v-icon></v-tab>
      <v-tab value="nature"><v-icon size="24">mdi-leaf</v-icon></v-tab>
      <v-tab value="food"><v-icon size="24">mdi-food-apple</v-icon></v-tab>
    </v-tabs>
  </div>
</template>

<script setup>
  import { onMounted, ref } from 'vue'

  const emit = defineEmits(['select'])

  const activeTab = ref('dev')
  const recentStickers = ref([])

  // مصفوفات الملصقات المحلية
  const devPack = Array.from({ length: 40 }, (_, i) => `/static/stickers/dev/${i + 1}.svg`)
  const techPack = [
    ...Array.from({ length: 6 }, (_, i) => `/static/stickers/tech/real_${i + 1}.svg`),
    ...Array.from({ length: 55 }, (_, i) => `/static/stickers/tech/${i + 1}.svg`),
  ]
  const transportPack = [
    ...Array.from({ length: 3 }, (_, i) => `/static/stickers/transport/real_${i + 1}.svg`),
    ...Array.from({ length: 54 }, (_, i) => `/static/stickers/transport/${i + 1}.svg`),
  ]
  const botPack = Array.from({ length: 100 }, (_, i) => `/static/stickers/bots/${i + 1}.svg`)
  const avatarPack = Array.from({ length: 100 }, (_, i) => `/static/stickers/avatars/${i + 1}.svg`)
  const naturePack = Array.from({ length: 50 }, (_, i) => `/static/stickers/nature/${i + 1}.svg`)
  const foodPack = [
    ...Array.from({ length: 3 }, (_, i) => `/static/stickers/food/real_${i + 1}.svg`),
    ...Array.from({ length: 50 }, (_, i) => `/static/stickers/food/${i + 1}.svg`),
  ]

  onMounted(() => {
    const saved = localStorage.getItem('recent_stickers')
    if (saved) {
      recentStickers.value = JSON.parse(saved)
    }
  })

  function selectSticker (url) {
    // نستخدم المسار الكامل لضمان الظهور عند الآخرين
    const fullUrl = window.location.origin + url
    emit('select', fullUrl)

    if (!recentStickers.value.includes(url)) {
      recentStickers.value.unshift(url)
      if (recentStickers.value.length > 20) recentStickers.value.pop()
      localStorage.setItem('recent_stickers', JSON.stringify(recentStickers.value))
    }
  }
</script>

<style scoped>
.sticker-picker {
  width: 380px;
  height: 520px;
  border: 1px solid var(--wa-border);
}

.sticker-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.sticker-item {
  cursor: pointer;
  padding: 6px;
  border-radius: 12px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sticker-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.1);
  transform: scale(1.15);
}

.sticker-content {
  scrollbar-width: thin;
}
</style>
