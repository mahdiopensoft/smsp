<template>
  <custom-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :title="$t('chat.newChat.title')"
    width="500"
  >
    <div class="d-flex flex-column custom-scrollbar" style="height: 85vh; max-height: 90vh; overflow-y: auto;">
        <!-- Search Area -->
        <div class="search-area pa-4">
          <v-text-field
            v-model="search"
            bg-color="surface"
            class="premium-search rounded-pill-input"
            density="comfortable"
            hide-details
            clearable
            :placeholder="$t('chat.newChat.search')"
            rounded="xl"
            variant="solo"
            elevation="0"
          >
            <template #prepend-inner>
              <v-icon color="primary" class="me-2">mdi-magnify</v-icon>
            </template>
          </v-text-field>
        </div>

        <!-- Action: New Group -->
        <div class="px-4 pb-4" v-if="canCreateGroup">
          <v-card 
            link 
            @click="$emit('open-group-create')" 
            class="premium-action-card" 
            elevation="0"
            rounded="xl"
          >
            <div class="d-flex align-center pa-3">
              <div class="icon-wrapper primary-gradient me-4 shadow-primary">
                <v-icon color="white">mdi-account-group</v-icon>
              </div>
              <div class="flex-grow-1">
                <h3 class="text-subtitle-1 font-weight-bold mb-0">{{ $t('chat.newChat.newGroup') || 'إنشاء مجموعة جديدة' }}</h3>
                <p class="text-caption text-medium-emphasis mb-0">دردشة جماعية مع عدة أشخاص</p>
              </div>
              <v-icon color="primary">{{ isRtl ? 'mdi-chevron-left' : 'mdi-chevron-right' }}</v-icon>
            </div>
          </v-card>
        </div>

        <div class="d-flex align-center px-4 py-2">
          <span class="text-caption text-uppercase font-weight-bold tracking-wide" style="letter-spacing: 1px; color: rgb(var(--v-theme-primary))">
            {{ $t("chat.newChat.contacts") || 'جهات الاتصال' }}
          </span>
          <v-divider class="ms-4" opacity="0.1" />
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-8 d-flex flex-column align-center justify-center" style="min-height: 200px">
           <v-progress-circular indeterminate color="primary" size="48" width="4"></v-progress-circular>
           <span class="mt-4 text-medium-emphasis text-body-2">جاري مزامنة جهات الاتصال...</span>
        </div>

        <!-- Grouped Contacts (Accordion) -->
        <div v-else-if="filteredGroups.length > 0" class="flex-grow-1 px-3 pb-3">
          <v-expansion-panels variant="accordion" class="premium-panels">
            <v-expansion-panel
              v-for="group in filteredGroups"
              :key="group.key"
              class="premium-group-panel mb-3 rounded-xl"
              elevation="0"
            >
              <v-expansion-panel-title class="group-title py-3 px-4">
                <div class="d-flex align-center flex-grow-1">
                  <v-avatar class="group-icon-avatar me-4" color="primary-lighten-5" size="44">
                    <v-icon size="22" color="primary">{{ group.icon }}</v-icon>
                  </v-avatar>
                  <div class="flex-grow-1">
                    <div class="font-weight-bold text-subtitle-2">{{ group.label }}</div>
                    <div class="text-caption text-medium-emphasis">
                      {{ group.count }} {{ group.count > 10 ? 'مستخدم' : 'مستخدمين' }}
                    </div>
                  </div>
                  <!-- Quick Group Creation Buttons -->
                  <div v-if="canCreateGroup" class="d-flex ga-2 me-2 btn-actions" @click.stop>
                    <v-tooltip location="top" text="إنشاء مجموعة سريعة">
                      <template #activator="{ props }">
                        <v-btn v-bind="props" color="success" icon size="small" variant="flat" class="action-btn" @click.stop="quickCreateGroup(group)">
                          <v-icon size="18">mdi-flash</v-icon>
                        </v-btn>
                      </template>
                    </v-tooltip>
                    <v-tooltip location="top" text="تخصيص مجموعة">
                      <template #activator="{ props }">
                        <v-btn v-bind="props" color="primary" icon size="small" variant="flat" class="action-btn" @click.stop="customizeGroup(group)">
                          <v-icon size="18">mdi-pencil</v-icon>
                        </v-btn>
                      </template>
                    </v-tooltip>
                  </div>
                </div>
              </v-expansion-panel-title>

              <v-expansion-panel-text class="pa-0">
                <v-list bg-color="transparent" class="py-2" density="comfortable">
                  <template v-for="(user, idx) in group.users" :key="user.id">
                    <v-list-item
                      class="premium-user-item mx-2 mb-1 px-4 py-2 rounded-lg"
                      @click="startChat(user)"
                    >
                      <template #prepend>
                        <div class="position-relative me-4">
                          <v-avatar size="44" class="border-avatar shadow-sm">
                            <v-img v-if="user.avatar" alt="Avatar" cover :src="user.avatar" />
                            <div
                              v-else
                              class="d-flex align-center justify-center w-100 h-100 text-white font-weight-bold text-subtitle-1 gradient-avatar"
                            >
                              {{ user.name.charAt(0).toUpperCase() }}
                            </div>
                          </v-avatar>
                        </div>
                      </template>
                      <v-list-item-title class="font-weight-bold text-body-2 mb-1">
                        {{ user.name }}
                      </v-list-item-title>
                      <v-list-item-subtitle class="text-caption text-medium-emphasis">
                        @{{ user.username }}
                      </v-list-item-subtitle>
                      <template #append>
                        <v-icon color="grey-lighten-2" size="small">{{ isRtl ? 'mdi-chevron-left' : 'mdi-chevron-right' }}</v-icon>
                      </template>
                    </v-list-item>
                  </template>
                </v-list>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>

        <!-- No results -->
        <div v-else class="text-center py-10 opacity-80 d-flex flex-column align-center">
          <div class="empty-state-icon mb-4">
             <v-icon color="primary" size="48">mdi-account-search-outline</v-icon>
          </div>
          <h3 class="text-h6 font-weight-bold mb-1">لا توجد نتائج</h3>
          <div class="text-medium-emphasis text-body-2">
            {{ $t("chat.newChat.noResults") }}
          </div>
        </div>
    </div>
  </custom-dialog>
</template>

<script setup>
  import { computed, ref, watch } from 'vue'
  import { useI18n } from 'vue-i18n'
  import { useDisplay } from 'vuetify'
  import { chatService } from '../../services/chatService'
  import { useChatStore } from '../../store/chat'
  import { useToastStore } from '../../store/toastStore'
  import { useAuthStore } from '../../../src/UserManagement/stores/auth'

const authStore = useAuthStore()
const user = ref(authStore.user || {})


  const props = defineProps({
    modelValue: Boolean,
  })

  const emit = defineEmits([
    'update:modelValue',
    'open-group-create',
    'select-user',
    'open-group-with-members',
  ])

  const { t } = useI18n()
  const { xs } = useDisplay()
  const chatStore = useChatStore()
  const toastStore = useToastStore()

  const search = ref('')
  const contactGroups = ref([])
  const loading = ref(false)

  // تحديد من يحق له إنشاء مجموعة بناءً على الدور
  const canCreateGroup = computed(() => {
    const userRole = (user?.role || user?.user_type || '').toLowerCase();
    return !['student', 'guardian', 'parent', 'طالب', 'ولي أمر'].includes(userRole);
  })

  // فلترة المجموعات والمستخدمين حسب البحث
  const filteredGroups = computed(() => {
    if (!search.value) return contactGroups.value

    const q = search.value.toLowerCase()
    return contactGroups.value
      .map(group => {
        // فلترة المستخدمين داخل المجموعة
        const filteredUsers = group.users.filter(u =>
          u.name.toLowerCase().includes(q) || u.username.toLowerCase().includes(q)
        )
        // إظهار المجموعة إذا تطابق اسمها أو أحد مستخدميها
        if (group.label.toLowerCase().includes(q) || filteredUsers.length > 0) {
          return {
            ...group,
            users: filteredUsers.length > 0 ? filteredUsers : group.users,
            count: filteredUsers.length > 0 ? filteredUsers.length : group.count,
          }
        }
        return null
      })
      .filter(Boolean)
  })

  async function fetchGroupedContacts() {
    loading.value = true
    try {
      const data = await chatService.getGroupedContacts()
      contactGroups.value = (data.groups || []).map(g => ({
        ...g,
        users: g.users.map(u => ({
          id: u.id,
          name: u.full_name || u.username,
          username: u.username,
          avatar: u.profile_picture,
        }))
      }))
    } catch (error) {
      console.error('Error fetching grouped contacts', error)
      // Fallback: استخدام الـ API القديم
      try {
        const results = await chatService.getAllowedContacts()
        contactGroups.value = [{
          key: 'all',
          label: t('chat.newChat.contacts'),
          icon: 'mdi-account-group',
          count: results.length,
          metadata: {},
          users: results.map(u => ({
            id: u.id,
            name: u.full_name || u.username,
            username: u.username,
            avatar: u.profile_picture,
          }))
        }]
      } catch (e2) {
        console.error('Fallback also failed', e2)
      }
    } finally {
      loading.value = false
    }
  }

  watch(
    () => props.modelValue,
    isOpen => {
      if (isOpen) {
        search.value = ''
        fetchGroupedContacts()
      }
    },
  )

  function startChat(user) {
    emit('select-user', user)
    emit('update:modelValue', false)
  }

  // إنشاء مجموعة سريعة بكل أعضاء التصنيف
  async function quickCreateGroup(group) {
    try {
      const participantIds = group.users.map(u => u.id)
      const chat = await chatStore.createChat({
        chat_type: 'group',
        name: group.label,
        participant_ids: participantIds,
      })
      toastStore.showToast(`تم إنشاء مجموعة "${group.label}" بنجاح`, 'success')
      emit('update:modelValue', false)
      await chatStore.setActiveChat(chat.id)
    } catch (error) {
      console.error('Error creating quick group:', error)
      toastStore.showToast('حدث خطأ أثناء إنشاء المجموعة', 'error')
    }
  }

  // فتح نافذة إنشاء مجموعة مع تحديد الأعضاء مسبقاً
  function customizeGroup(group) {
    emit('open-group-with-members', {
      name: group.label,
      memberIds: group.users.map(u => u.id),
    })
    emit('update:modelValue', false)
  }
</script>

<style scoped>
/* Search */
.premium-search :deep(.v-field) {
  border: 1px solid rgba(var(--v-border-color), 0.08) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03) !important;
  transition: all 0.3s ease;
  background: rgba(var(--v-theme-surface), 1);
}
.premium-search :deep(.v-field--focused) {
  border-color: rgba(var(--v-theme-primary), 0.5) !important;
  box-shadow: 0 4px 20px rgba(var(--v-theme-primary), 0.1) !important;
}

/* Action Card */
.premium-action-card {
  background: rgba(var(--v-theme-primary), 0.03) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.1) !important;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}
.premium-action-card:hover {
  transform: translateY(-2px);
  background: rgba(var(--v-theme-primary), 0.06) !important;
  border-color: rgba(var(--v-theme-primary), 0.2) !important;
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.08) !important;
}

.icon-wrapper {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.primary-gradient {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}
.shadow-primary {
  box-shadow: 0 8px 16px rgba(79, 172, 254, 0.3);
}

/* Panels */
.premium-panels {
  gap: 12px;
}
.premium-group-panel {
  border: 1px solid rgba(var(--v-border-color), 0.08);
  background: rgba(var(--v-theme-surface), 1) !important;
  transition: all 0.2s ease;
}
.premium-group-panel:hover {
  border-color: rgba(var(--v-theme-primary), 0.3);
  box-shadow: 0 4px 16px rgba(0,0,0,0.04) !important;
}
.premium-group-panel :deep(.v-expansion-panel-title) {
  padding: 10px 16px !important;
}
.premium-group-panel :deep(.v-expansion-panel-title__overlay) {
  opacity: 0 !important;
}

.group-icon-avatar {
  background: rgba(var(--v-theme-primary), 0.08) !important;
}

.action-btn {
  opacity: 0.7;
  transition: all 0.2s;
  box-shadow: none !important;
}
.action-btn:hover {
  opacity: 1;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}

/* Users */
.premium-user-item {
  transition: all 0.2s ease;
  background: transparent;
  border: 1px solid transparent;
}
.premium-user-item:hover {
  background: rgba(var(--v-theme-primary), 0.04);
  border-color: rgba(var(--v-theme-primary), 0.1);
  transform: translateX(4px);
}
[dir="rtl"] .premium-user-item:hover {
  transform: translateX(-4px);
}

.gradient-avatar {
  background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
}
.border-avatar {
  border: 2px solid rgba(var(--v-theme-surface), 1);
}
.shadow-sm {
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* Empty State */
.empty-state-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(var(--v-theme-primary), 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.15);
  border-radius: 10px;
}
</style>

