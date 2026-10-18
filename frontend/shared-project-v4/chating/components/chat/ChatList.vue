<template>
  <div class="chat-list d-flex flex-column h-100 w-100">
    <!-- الهيدر -->
    <div class="chat-list-header pa-4">
      <div class="chat-list-header__top d-flex align-start justify-space-between mb-4">
        <div class="d-flex align-start gap-2">
          <v-btn
            v-if="showArchived"
            class="chat-list-back-btn"
            icon
            size="small"
            variant="text"
            @click="showArchived = false"
          >
            <v-icon>{{ isRtl ? "mdi-arrow-right" : "mdi-arrow-left" }}</v-icon>
          </v-btn>
          <div>
            <!-- <div class="chat-list-kicker mb-1">
              {{ showArchived ? "الأرشيف" : "المحادثات" }}
            </div> -->
            <h2 class="chat-list-title font-weight-bold">
              {{
                showArchived ? $t("chat.list.archived") : $t("chat.list.chats")
              }}
            </h2>
            <p class="chat-list-subtitle mb-0">
              {{
                showArchived
                  ? "الوصول السريع إلى المحادثات المؤرشفة"
                  : "تواصل مع المستخدمين والمجموعات من مكان واحد"
              }}
            </p>
          </div>
        </div>

        <div class="chat-list-actions d-flex align-center gap-2">
          <!-- <v-btn
            class="chat-list-primary-btn"
            color="primary"
            prepend-icon="mdi-message-plus-outline"
            rounded="xl"
            size="small"
            variant="flat"
            @click="$emit('newChat')"
          >
            {{ $t("chat.list.newChat") }}
          </v-btn> -->

          <v-menu location="bottom end" open-on-hover attach="body">
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                class="chat-list-menu-btn"
                icon
                size="small"
                variant="text"
              >
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list class="chat-list-menu pa-1" density="compact">
              <v-list-item rounded="lg" @click="$emit('newGroup')">
                <template #prepend>
                  <v-icon size="20">mdi-account-group-outline</v-icon>
                </template>
                <v-list-item-title>{{
                  $t("chat.list.newGroup")
                }}</v-list-item-title>
              </v-list-item>
              <v-list-item rounded="lg" @click="$emit('newChat')">
                <template #prepend>
                  <v-icon size="20">mdi-message-plus-outline</v-icon>
                </template>
                <v-list-item-title>{{
                  $t("chat.list.newChat")
                }}</v-list-item-title>
              </v-list-item>
              <v-list-item rounded="lg" @click="$emit('settings')">
                <template #prepend>
                  <v-icon size="20">mdi-cog-outline</v-icon>
                </template>
                <v-list-item-title>{{ $t("chat.settings.title") || "الإعدادات"}}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </div>
      </div>

      <!-- <div v-if="!showArchived" class="chat-list-metrics mb-4">
        <div class="metric-pill">
          <span class="metric-pill__label">الإجمالي</span>
          <strong>{{ activeChatsCount }}</strong>
        </div>
        <div class="metric-pill">
          <span class="metric-pill__label">مثبتة</span>
          <strong>{{ pinnedChats.length }}</strong>
        </div>
        <div class="metric-pill">
          <span class="metric-pill__label">غير مقروءة</span>
          <strong>{{ unreadChatsCount }}</strong>
        </div>
      </div> -->

      <!-- شريط البحث -->
      <SearchBar
        v-model="searchQuery"
        class="chat-list-search"
        :placeholder="$t('chat.list.searchPlaceholder')"
        @search="onSearch"
      />

      <!-- تبويبات التصفية -->
      <v-btn-toggle
        v-model="chatFilter"
        class="chat-filter-tabs mt-3"
        color="primary"
        density="compact"
        mandatory
        rounded="xl"
        variant="outlined"
      >
        <v-btn value="all" size="small" class="text-caption font-weight-bold">
          {{ $t('chat.list.all') || 'الكل' }}
        </v-btn>
        <v-btn value="private" size="small" class="text-caption font-weight-bold">
          <v-icon start size="14">mdi-account</v-icon>
          {{ $t('chat.list.private') || 'محادثات' }}
        </v-btn>
        <v-btn value="group" size="small" class="text-caption font-weight-bold">
          <v-icon start size="14">mdi-account-group</v-icon>
          {{ $t('chat.list.groups') || 'مجموعات' }}
        </v-btn>
      </v-btn-toggle>
    </div>

    <!-- زر الأرشفة -->
    <v-list-item
      v-if="!showArchived && archivedCount > 0 && !searchQuery"
      class="archived-chats-btn mx-3 rounded-xl mb-3"
      link
      @click="showArchived = true"
    >
      <template #prepend>
        <v-icon class="me-4" color="secondary">mdi-archive-outline</v-icon>
      </template>
      <v-list-item-title>{{ $t("chat.list.archived") }}</v-list-item-title>
      <template #append>
        <span class="text-secondary">{{ archivedCount }}</span>
      </template>
    </v-list-item>

    <!-- حالة التحميل -->
    <div v-if="loading" class="flex-grow-1 d-flex align-center justify-center">
      <div class="app-loader-spinner app-loader--md"></div>
    </div>

    <!-- قائمة المحادثات -->
    <v-list
      v-else-if="filteredChats.length > 0"
      class="chat-list-content flex-grow-1 pa-0 overflow-y-auto"
    >

      <!-- المحادثات المثبتة -->
      <template v-if="pinnedChats.length > 0">
        <!-- <v-list-subheader class="chat-list-subheader px-4 text-uppercase">
          {{ $t("chat.list.pinned") }}
        </v-list-subheader> -->
        <ChatListItem
          v-for="chat in pinnedChats"
          :key="chat.id"
          :active="chat.id === activeChatId"
          :chat="chat"
          :current-user-id="currentUserId"
          :unread-count="unreadCounts[chat.id] || 0"
          @archive="$emit('archiveChat', chat.id)"
          @click="$emit('selectChat', chat.id)"
          @delete="$emit('deleteChat', chat.id)"
          @mute="$emit('muteChat', chat.id)"
          @pin="$emit('pinChat', chat.id)"
        />
        <!-- <v-divider v-if="unpinnedChats.length > 0" class="chat-list-divider" /> -->
      </template>

      <!-- المحادثات العادية -->
      <ChatListItem
        v-for="chat in unpinnedChats"
        :key="chat.id"
        :active="chat.id === activeChatId"
        :chat="chat"
        :current-user-id="currentUserId"
        :unread-count="unreadCounts[chat.id] || 0"
        @archive="$emit('archiveChat', chat.id)"
        @click="$emit('selectChat', chat.id)"
        @delete="$emit('deleteChat', chat.id)"
        @mute="$emit('muteChat', chat.id)"
        @pin="$emit('pinChat', chat.id)"
      />
    </v-list>

    <!-- حالة فارغة -->
    <EmptyState
      v-else
      class="chat-list-empty"
      :description="
        searchQuery ? $t('chat.list.tryDiffTerms') : $t('chat.list.startChat')
      "
      icon="mdi-chat-outline"
      :title="searchQuery ? $t('chat.list.noResults') : $t('chat.list.noChats')"
    >
      <template v-if="!searchQuery" #action>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="$emit('newChat')"
        >
          {{ $t("chat.list.newChat") }}
        </v-btn>
      </template>
    </EmptyState>
  </div>
</template>

<script setup>
  import { computed, ref } from 'vue'
  import { useI18n } from 'vue-i18n'
  import { useRtl } from 'vuetify'
  import EmptyState from '../../components/common/EmptyState.vue'
  import SearchBar from '../../components/common/SearchBar.vue'
  import ChatListItem from './ChatListItem.vue'
  

  const props = defineProps({
    chats: {
      type: Array,
      default: () => [],
    },
    activeChatId: {
      type: [Number, String],
      default: null,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    unreadCounts: {
      type: Object,
      default: () => ({}),
    },
    currentUserId: {
      type: Number,
      default: null,
    },
  })

  const { t } = useI18n()
  const { isRtl } = useRtl()

  const emit = defineEmits([
    'selectChat',
    'newChat',
    'newGroup',
    'pinChat',
    'muteChat',
    'archiveChat',
    'muteChat',
    'deleteChat',
    'settings',
  ])

  const searchQuery = ref('')
  const chatFilter = ref('all')

  // حالة عرض المؤرشفة
  const showArchived = ref(false)

  // عدد المحادثات المؤرشفة
  const archivedCount = computed(
    () => Array.isArray(props.chats) ? props.chats.filter(c => c.is_archived).length : 0,
  )

  // فلترة المحادثات
  const filteredChats = computed(() => {
    let chats = props.chats

    // فلترة حسب الأرشفة
    chats = showArchived.value ? chats.filter(c => c.is_archived) : chats.filter(c => !c.is_archived)

    // فلترة حسب النوع (محادثات / مجموعات)
    if (chatFilter.value === 'private') {
      chats = chats.filter(c => c.chat_type === 'private')
    } else if (chatFilter.value === 'group') {
      chats = chats.filter(c => c.chat_type === 'group')
    }

    if (!searchQuery.value) return chats

    const query = searchQuery.value.toLowerCase()
    return chats.filter(chat => {
      const name = chat.name || chat.other_participant?.username || ''
      return name.toLowerCase().includes(query)
    })
  })

  // المحادثات المثبتة
  const pinnedChats = computed(() =>
    filteredChats.value.filter(c => c.is_pinned),
  )

  // المحادثات غير المثبتة
  const unpinnedChats = computed(() =>
    filteredChats.value.filter(c => !c.is_pinned),
  )

  // const activeChatsCount = computed(() =>
  //   Array.isArray(props.chats) ? props.chats.filter(c => !c.is_archived).length : 0,
  // )

  // const unreadChatsCount = computed(() =>
  //   Object.values(props.unreadCounts || {}).reduce((sum, count) => sum + (Number(count) || 0), 0),
  // )

  function onSearch (query) {
    searchQuery.value = query
  }

// تم إزالة confirmDeleteChat و deleteChat لاستخدام منطق الحذف الموحد في index.vue
</script>

<style scoped>
.chat-list {
  background: rgba(var(--v-theme-surface), 0.85);
  color: rgba(var(--v-theme-on-surface), 0.9);
}

.chat-list-header {
  border-bottom: 1px solid rgba(var(--v-border-color), 0.06);
  background: linear-gradient(180deg, rgba(var(--v-theme-primary), 0.06) 0%, rgba(var(--v-theme-surface), 0) 100%);
  padding: 20px 20px 16px 20px !important;
}

.chat-list-title {
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 1) 0%, rgba(var(--v-theme-secondary), 0.8) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 2px;
}

.chat-list-subtitle {
  color: rgba(var(--v-theme-on-surface), 0.5);
  font-size: 0.85rem;
  font-weight: 500;
}

.chat-list-actions {
  flex-shrink: 0;
}

.chat-list-menu-btn,
.chat-list-back-btn {
  background: rgba(var(--v-theme-on-surface), 0.03);
  color: rgba(var(--v-theme-on-surface), 0.7);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.chat-list-menu-btn:hover,
.chat-list-back-btn:hover {
  background: rgba(var(--v-theme-primary), 0.1);
  color: rgba(var(--v-theme-primary), 1);
  transform: translateY(-2px);
}

.chat-list-search :deep(.v-field) {
  border-radius: 20px !important;
  background: rgba(var(--v-theme-on-surface), 0.04) !important;
  border: 1px solid rgba(var(--v-border-color), 0.06) !important;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02) !important;
  transition: all 0.3s ease;
}

.chat-list-search :deep(.v-field--focused) {
  background: rgba(var(--v-theme-surface), 1) !important;
  border-color: rgba(var(--v-theme-primary), 0.3) !important;
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.08), inset 0 0 0 0 transparent !important;
}

.chat-list-menu {
  border: 1px solid rgba(var(--v-border-color), 0.08);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12) !important;
  border-radius: 20px !important;
  background: rgba(var(--v-theme-surface), 0.9);
}

.chat-list-content {
  scrollbar-width: thin;
  scrollbar-color: rgba(var(--v-theme-on-surface), 0.15) transparent;
  padding-bottom: 24px !important;
  padding-top: 8px !important;
}

.archived-chats-btn {
  min-height: 56px;
  margin: 12px 16px;
  background: rgba(var(--v-theme-on-surface), 0.02);
  border: 1px solid rgba(var(--v-border-color), 0.05);
  transition: all 0.25s ease;
}

.archived-chats-btn:hover {
  background: rgba(var(--v-theme-primary), 0.05);
  border-color: rgba(var(--v-theme-primary), 0.15);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.06);
}

.chat-list-empty {
  padding-inline: 24px;
  opacity: 0.8;
}

@media (max-width: 600px) {
  .chat-list-header {
    padding: 16px !important;
  }
  .chat-list-header__top {
    flex-direction: column;
    gap: 16px;
  }
  .chat-list-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
