<template>
  <v-dialog
    v-model="dialog"
    class="add-members-dialog"
    :fullscreen="xs"
    max-width="500"
    scrollable
  >
    <v-card class="rounded-xl overflow-hidden bg-surface">
      <!-- Header -->
      <div class="dialog-header">
        <div class="d-flex align-center justify-space-between">
          <div class="d-flex align-center">
            <div class="icon-wrapper me-3">
              <v-icon color="white" size="24">mdi-account-plus</v-icon>
            </div>
            <div>
              <h3 class="text-white font-weight-bold mb-0">
                {{ $t("chat.addMembers.title", "إضافة أعضاء") }}
              </h3>
              <div class="text-white-70">
                {{ $t("chat.addMembers.subtitle", "إضافة أعضاء جدد للمجموعة") }}
              </div>
            </div>
          </div>
          <v-btn
            class="close-btn"
            color="white"
            icon
            size="small"
            variant="text"
            @click="dialog = false"
          >
            <v-icon size="24">mdi-close</v-icon>
          </v-btn>
        </div>
      </div>

      <v-card-text class="pa-0 h-100 d-flex flex-column">
        <!-- Search -->
        <div class="pa-4 bg-surface">
          <v-text-field
            v-model="search"
            bg-color="surface"
            class="modern-search"
            density="compact"
            hide-details
            :placeholder="$t('common.search')"
            rounded="xl"
            variant="outlined"
          >
            <template #prepend-inner>
              <v-icon class="opacity-70" color="primary">mdi-magnify</v-icon>
            </template>
          </v-text-field>
        </div>

        <!-- Selected Users Chips -->
        <div v-if="selectedUsers.length > 0" class="px-4 pb-3">
          <div class="d-flex flex-wrap gap-1">
            <v-chip
              v-for="userId in selectedUsers.slice(0, 8)"
              :key="userId"
              closable
              color="primary"
              size="small"
              variant="tonal"
              @click:close="removeSelection(userId)"
            >
              {{ getUserName(userId) }}
            </v-chip>
            <v-chip
              v-if="selectedUsers.length > 8"
              color="primary"
              size="small"
              variant="outlined"
            >
              +{{ selectedUsers.length - 8 }}
            </v-chip>
          </div>
        </div>

        <v-divider />

        <!-- Loading -->
        <div v-if="loading" class="text-center py-8">
          <div class="app-loader-spinner app-loader--sm"></div>
        </div>

        <!-- Grouped Users List -->
        <div v-else-if="filteredGroups.length > 0" class="flex-grow-1 overflow-y-auto px-2">
          <v-expansion-panels variant="accordion" class="grouped-panels">
            <v-expansion-panel
              v-for="group in filteredGroups"
              :key="group.key"
              class="group-panel mb-2 rounded-lg"
              elevation="0"
            >
              <v-expansion-panel-title class="group-title py-2 px-3">
                <div class="d-flex align-center flex-grow-1">
                  <v-avatar class="group-icon-avatar me-3" color="primary" size="36" variant="tonal">
                    <v-icon size="18">{{ group.icon }}</v-icon>
                  </v-avatar>
                  <div class="flex-grow-1">
                    <div class="font-weight-bold text-body-2">{{ group.label }}</div>
                    <div class="text-caption text-medium-emphasis">
                      {{ getGroupSelectionText(group) }}
                    </div>
                  </div>
                  <!-- Select All in Group -->
                  <div class="me-2" @click.stop>
                    <v-tooltip location="top" :text="isGroupFullySelected(group) ? 'إلغاء تحديد الكل' : 'تحديد الكل'">
                      <template #activator="{ props }">
                        <v-btn
                          v-bind="props"
                          :color="isGroupFullySelected(group) ? 'warning' : 'primary'"
                          icon
                          size="x-small"
                          variant="tonal"
                          @click.stop="toggleGroupSelection(group)"
                        >
                          <v-icon size="16">{{ isGroupFullySelected(group) ? 'mdi-checkbox-marked' : 'mdi-checkbox-blank-outline' }}</v-icon>
                        </v-btn>
                      </template>
                    </v-tooltip>
                  </div>
                </div>
              </v-expansion-panel-title>

              <v-expansion-panel-text class="pa-0">
                <v-list bg-color="transparent" class="py-0" density="compact">
                  <template v-for="(user, idx) in group.users" :key="user.id">
                    <v-list-item
                      class="user-item py-2 px-3"
                      :class="{ 'selected-item': selectedUsers.includes(user.id) }"
                      @click="toggleSelection(user)"
                    >
                      <template #prepend>
                        <div class="position-relative me-3">
                          <v-avatar size="40">
                            <v-img v-if="user.avatar" cover :src="user.avatar" />
                            <span
                              v-else
                              class="bg-primary text-white w-100 h-100 d-flex align-center justify-center font-weight-bold"
                            >
                              {{ user.name.charAt(0).toUpperCase() }}
                            </span>
                          </v-avatar>
                          <div v-if="user.online" class="status-dot" />
                        </div>
                      </template>

                      <v-list-item-title class="font-weight-medium text-body-2">
                        {{ user.name }}
                      </v-list-item-title>

                      <v-list-item-subtitle class="text-caption">
                        @{{ user.username }}
                      </v-list-item-subtitle>

                      <template #append>
                        <div
                          class="selection-circle"
                          :class="{ selected: selectedUsers.includes(user.id) }"
                        >
                          <v-icon
                            v-if="selectedUsers.includes(user.id)"
                            color="white"
                            size="16"
                          >
                            mdi-check
                          </v-icon>
                        </div>
                      </template>
                    </v-list-item>
                    <v-divider v-if="idx < group.users.length - 1" class="mx-4 border-opacity-15" />
                  </template>
                </v-list>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>

        <!-- No results -->
        <div v-else class="text-center py-8 opacity-60">
          <v-icon class="mb-2" color="medium-emphasis" size="48">
            mdi-account-search-outline
          </v-icon>
          <div class="text-medium-emphasis">
            {{
              search
                ? $t("chat.newChat.noResults")
                : $t("chat.addMembers.searchHint", "ابحث عن مستخدمين لإضافتهم")
            }}
          </div>
        </div>
      </v-card-text>

      <!-- Actions -->
      <v-card-actions class="pa-4 border-t">
        <v-btn
          class="flex-1"
          color="medium-emphasis"
          height="44"
          rounded="xl"
          variant="outlined"
          @click="dialog = false"
        >
          {{ $t("common.cancel") }}
        </v-btn>
        <v-btn
          class="flex-1 text-white"
          color="primary"
          :disabled="selectedUsers.length === 0"
          height="44"
          :loading="adding"
          rounded="xl"
          variant="flat"
          @click="addMembers"
        >
          <v-icon start>mdi-account-plus</v-icon>
          {{ $t("common.add") }} ({{ selectedUsers.length }})
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
  import { computed, ref, watch } from 'vue'
  import { useI18n } from 'vue-i18n'
  import { useDisplay } from 'vuetify'
  import { chatService } from '../../services/chatService'
  import { useToastStore } from '../../store/toastStore'

  const props = defineProps({
    modelValue: Boolean,
    chatId: {
      type: Number,
      required: true,
    },
    existingMemberIds: {
      type: Array,
      default: () => [],
    },
  })

  const emit = defineEmits(['update:modelValue', 'membersAdded'])

  const { t } = useI18n()
  const { xs } = useDisplay()
  const toastStore = useToastStore()
  const dialog = computed({
    get: () => props.modelValue,
    set: val => emit('update:modelValue', val),
  })

  const search = ref('')
  const selectedUsers = ref([])
  const contactGroups = ref([])
  const loading = ref(false)
  const adding = ref(false)

  // Map لاسترجاع أسماء المستخدمين
  const allUsersMap = computed(() => {
    const map = {}
    for (const group of contactGroups.value) {
      for (const user of group.users) {
        map[user.id] = user
      }
    }
    return map
  })

  function getUserName(userId) {
    return allUsersMap.value[userId]?.name || 'مستخدم'
  }

  // فلترة: استثناء الأعضاء الحاليين + البحث
  const filteredGroups = computed(() => {
    const q = search.value?.toLowerCase() || ''

    return contactGroups.value
      .map(group => {
        // استثناء الأعضاء الحاليين
        let users = group.users.filter(u => !props.existingMemberIds.includes(u.id))

        // فلترة بالبحث
        if (q) {
          users = users.filter(u =>
            u.name.toLowerCase().includes(q) || u.username.toLowerCase().includes(q)
          )
        }

        if (users.length === 0) return null

        return {
          ...group,
          users,
          count: users.length,
        }
      })
      .filter(Boolean)
  })

  function isGroupFullySelected(group) {
    return group.users.every(u => selectedUsers.value.includes(u.id))
  }

  function getGroupSelectionText(group) {
    const selected = group.users.filter(u => selectedUsers.value.includes(u.id)).length
    if (selected === 0) return `${group.count} مستخدم`
    return `${selected} / ${group.count} محدد`
  }

  function toggleGroupSelection(group) {
    const allIds = group.users.map(u => u.id)
    if (isGroupFullySelected(group)) {
      selectedUsers.value = selectedUsers.value.filter(id => !allIds.includes(id))
    } else {
      const newIds = allIds.filter(id => !selectedUsers.value.includes(id))
      selectedUsers.value.push(...newIds)
    }
  }

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
          online: u.is_online || false,
        }))
      }))
    } catch (error) {
      console.error('Error fetching grouped contacts', error)
      try {
        const results = await chatService.getAllowedContacts()
        contactGroups.value = [{
          key: 'all',
          label: 'جهات الاتصال',
          icon: 'mdi-account-group',
          count: results.length,
          metadata: {},
          users: results.map(u => ({
            id: u.id,
            name: u.full_name || u.username,
            username: u.username,
            avatar: u.profile_picture,
            online: u.is_online || false,
          }))
        }]
      } catch (e2) {
        console.error('Fallback also failed', e2)
      }
    } finally {
      loading.value = false
    }
  }

  // Load users when dialog opens
  watch(
    () => props.modelValue,
    isOpen => {
      if (isOpen) {
        selectedUsers.value = []
        search.value = ''
        fetchGroupedContacts()
      }
    },
  )

  function toggleSelection(user) {
    const index = selectedUsers.value.indexOf(user.id)
    if (index === -1) {
      selectedUsers.value.push(user.id)
    } else {
      selectedUsers.value.splice(index, 1)
    }
  }

  function removeSelection(userId) {
    const index = selectedUsers.value.indexOf(userId)
    if (index !== -1) {
      selectedUsers.value.splice(index, 1)
    }
  }

  async function addMembers() {
    if (selectedUsers.value.length === 0) return

    adding.value = true
    let successCount = 0
    try {
      for (const userId of selectedUsers.value) {
        try {
          await chatService.addParticipant(props.chatId, userId)
          successCount++
        } catch (error) {
          console.error('Error adding member:', error)
          let errorMsg = error.response?.data?.error || error.response?.data || error.message
          if (typeof errorMsg === 'object' && Array.isArray(errorMsg)) {
             errorMsg = errorMsg[0]
          } else if (typeof errorMsg === 'object') {
             errorMsg = Object.values(errorMsg)[0]?.[0] || Object.values(errorMsg)[0] || JSON.stringify(errorMsg)
          }
          toastStore.showToast(errorMsg || t('chat.messages.error'), "error")
        }
      }
      
      if (successCount > 0) {
        emit('membersAdded')
      }
      dialog.value = false
    } catch (error) {
      console.error('Error in addMembers:', error)
    } finally {
      adding.value = false
    }
  }
</script>

<style scoped>
.dialog-header {
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
  padding: 24px;
}

.icon-wrapper {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.25);
}

.text-white-70 {
  color: rgba(255, 255, 255, 0.8);
}

.modern-search :deep(.v-field) {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.05);
}

/* Grouped Panels */
.grouped-panels {
  gap: 0;
}

.group-panel {
  border: 1px solid rgba(var(--v-border-color), 0.08);
  overflow: hidden;
}

.group-panel :deep(.v-expansion-panel-title) {
  min-height: 52px;
  padding: 6px 12px;
}

.group-panel :deep(.v-expansion-panel-title__overlay) {
  opacity: 0;
}

.group-icon-avatar {
  border: 2px solid rgba(var(--v-theme-primary), 0.15);
}

.user-item {
  transition: all 0.2s ease;
  cursor: pointer;
}

.user-item:hover {
  background-color: rgba(59, 130, 246, 0.05);
}

.user-item.selected-item {
  background-color: rgba(59, 130, 246, 0.1);
}

.status-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #22c55e;
  border: 2px solid white;
}

.selection-circle {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 2px solid #cbd5e1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.selection-circle.selected {
  background-color: #3b82f6;
  border-color: #3b82f6;
}

.flex-1 {
  flex: 1;
}
</style>
