<template>
  <custom-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :title="$t('chat.newGroup.title') || 'مجموعة جديدة'"
    width="500"
  >
    <div
      class="d-flex flex-column custom-scrollbar"
      style="height: 85vh; max-height: 90vh; overflow-y: auto"
    >
        <div class="pa-5 z-1 relative">
          <!-- Group Image & Name -->
          <div class="d-flex align-center mb-6">
            <div class="position-relative me-5">
              <v-hover v-slot="{ isHovering, props }">
                <v-avatar
                  class="cursor-pointer premium-avatar elevation-4 shadow-lg"
                  v-bind="props"
                  :class="{ 'on-hover': isHovering }"
                  size="72"
                  @click="fileInput && fileInput.click()"
                >
                  <v-img
                    v-if="groupImagePreview"
                    :src="groupImagePreview"
                    cover
                  />
                  <template v-else>
                    <div class="avatar-gradient w-100 h-100 d-flex align-center justify-center">
                      <v-icon color="white" size="32">mdi-camera-plus</v-icon>
                    </div>
                  </template>
                  <!-- overlay effect on hover -->
                  <div class="avatar-overlay" :class="{'show': isHovering}">
                    <v-icon color="white" size="24">mdi-pencil</v-icon>
                  </div>
                </v-avatar>
              </v-hover>
              <input
                type="file"
                ref="fileInput"
                class="d-none"
                accept="image/*"
                @change="onImageSelected"
              />
            </div>
            
            <div class="flex-grow-1">
              <label class="text-caption font-weight-bold text-medium-emphasis mb-1 d-block ms-1">اسم المجموعة</label>
              <custom-text-field
                v-model="groupName"
                icon="pound"
                :placeholder="$t('chat.newGroup.groupNamePlaceholder') || 'أدخل اسماً مميزاً'"
                :rules="[v => !v || v.length <= 100 || 'الحد الأقصى 100 حرف']"
                maxlength="100"
                counter
                cols="12"
              />
            </div>
          </div>

          <!-- Search Participants -->
           <label class="text-caption font-weight-bold text-medium-emphasis mb-1 d-block ms-1">البحث عن أشخاص</label>
          <v-text-field
            v-model="search"
            class="premium-search"
            density="comfortable"
            hide-details
            clearable
            :placeholder="$t('chat.newGroup.searchParticipants') || 'ابحث هنا...'"
            rounded="xl"
            variant="solo"
            elevation="0"
          >
            <template #prepend-inner>
              <v-icon color="primary" class="opacity-70 me-1">mdi-account-search</v-icon>
            </template>
          </v-text-field>
        </div>

        <!-- Selected count & Chips -->
        <div class="bg-grey-lighten-4 py-3 px-5 border-y border-opacity-10" v-if="selectedUsers.length > 0">
           <div class="d-flex align-center mb-2">
             <span class="text-caption font-weight-bold tracking-wide text-primary text-uppercase">
               {{ $t("chat.newGroup.participants", { count: selectedUsers.length }) }}
             </span>
             <v-spacer></v-spacer>
             <span class="text-caption text-medium-emphasis">{{ selectedUsers.length }} شخص محدد</span>
           </div>
           
           <div class="d-flex gap-2 overflow-x-auto custom-scrollbar-x pb-2">
            <v-slide-x-transition group>
             <v-chip
               v-for="userId in selectedUsers"
               :key="userId"
               closable
               color="primary"
               size="default"
               variant="flat"
               class="flex-shrink-0 font-weight-bold px-3 shadow-sm"
               @click:close="removeSelection(userId)"
             >
               {{ getUserName(userId) }}
             </v-chip>
            </v-slide-x-transition>
           </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-10 d-flex flex-column align-center justify-center flex-grow-1">
           <v-progress-circular indeterminate color="primary" size="48" width="4"></v-progress-circular>
           <span class="mt-4 text-medium-emphasis text-body-2">جاري مزامنة القوائم...</span>
        </div>

        <!-- Grouped Participants List -->
        <div
          v-else-if="filteredGroups.length > 0"
          class="flex-grow-1 overflow-y-auto participant-list px-4 py-4"
        >
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
                      {{ getGroupSelectionText(group) }}
                    </div>
                  </div>
                  <!-- Select All in Group -->
                  <div class="d-flex ga-1 me-2" @click.stop>
                    <v-tooltip location="top" :text="isGroupFullySelected(group) ? 'إلغاء تحديد الكل' : 'تحديد الكل'">
                      <template #activator="{ props }">
                        <v-btn v-bind="props" :color="isGroupFullySelected(group) ? 'warning' : 'primary'" icon size="small" variant="tonal" class="action-btn" @click.stop="toggleGroupSelection(group)">
                          <v-icon size="18">{{ isGroupFullySelected(group) ? "mdi-close" : "mdi-check-all" }}</v-icon>
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
                      :class="{ 'selected-item': selectedUsers.includes(user.id) }"
                      @click="toggleSelection(user)"
                    >
                      <template #prepend>
                        <div class="position-relative me-4">
                          <v-avatar size="44" class="border-avatar shadow-sm">
                            <v-img v-if="user.avatar" cover :src="user.avatar" />
                            <div v-else class="gradient-avatar w-100 h-100 d-flex align-center justify-center text-white font-weight-bold text-h6">
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
                         <div class="premium-checkbox" :class="{ 'checked': selectedUsers.includes(user.id) }">
                            <v-icon color="white" size="14" v-if="selectedUsers.includes(user.id)">mdi-check</v-icon>
                         </div>
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

        <!-- Private Group Toggle -->
        <div class="pa-5 bg-grey-lighten-4 border-t border-opacity-10 mt-auto">
          <v-card 
            class="private-group-card d-flex align-center justify-space-between p-4" 
            elevation="0" 
            rounded="xl" 
            variant="flat"
            :class="{'active-private': isPrivate}"
          >
            <div class="d-flex align-center pa-4">
               <div class="icon-wrapper" :class="isPrivate ? 'bg-primary' : 'bg-grey-lighten-2'">
                 <v-icon :color="isPrivate ? 'white' : 'grey-darken-2'" size="24">
                   {{ isPrivate ? 'mdi-shield-lock' : 'mdi-shield-lock-outline' }}
                 </v-icon>
               </div>
               <div class="ms-4">
                 <h4 class="text-subtitle-1 font-weight-bold mb-1" :class="isPrivate ? 'text-primary' : ''">{{ $t("chat.newGroup.privateGroup") || 'مجموعة خاصة' }}</h4>
                 <p class="text-caption text-medium-emphasis mb-0">{{ $t("chat.newGroup.privateGroupDesc") || 'المشرفون فقط من يمكنهم إرسال رسائل.' }}</p>
               </div>
            </div>
            <div class="pe-4">
               <v-switch v-model="isPrivate" color="primary" density="compact" hide-details inset />
            </div>
          </v-card>
        </div>
    </div>
    <template #actions>
      <div class="w-100 d-flex justify-end gap-4 actions-wrapper pt-3 pb-3 pe-2">
         <custom-btn type="cancel" :click="() => $emit('update:modelValue', false)" />
         <v-btn
            color="primary"
            variant="flat"
            rounded="pill"
            class="font-weight-bold px-8 shadow-primary"
            min-height="36"
            :disabled="!groupName || selectedUsers.length === 0"
            @click="createGroup"
          >
            <v-icon start>mdi-check</v-icon>
            {{ $t('chat.newGroup.create', { count: selectedUsers.length }) || `إنشاء (${selectedUsers.length})` }}
          </v-btn>
      </div>
    </template>
  </custom-dialog>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useDisplay } from "vuetify";
import { chatService } from "../../services/chatService";

const props = defineProps({
  modelValue: Boolean,
  preSelectedName: {
    type: String,
    default: "",
  },
  preSelectedMemberIds: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["update:modelValue", "create-group"]);

const { t } = useI18n();
const { xs } = useDisplay();
const groupName = ref("");
const search = ref("");
const isPrivate = ref(false);
const selectedUsers = ref([]);
const contactGroups = ref([]);
const loading = ref(false);

const fileInput = ref(null);
const groupImage = ref(null);
const groupImagePreview = ref(null);

function onImageSelected(event){
  const file = event.target.files[0]
  if(file){
    groupImage.value = file
    groupImagePreview.value = URL.createObjectURL(file)
  }
}

// Map لاسترجاع أسماء المستخدمين بسرعة
const allUsersMap = computed(() => {
  const map = {};
  for (const group of contactGroups.value) {
    for (const user of group.users) {
      map[user.id] = user;
    }
  }
  return map;
});

function getUserName(userId) {
  return allUsersMap.value[userId]?.name || "مستخدم";
}

// فلترة المجموعات والمستخدمين حسب البحث
const filteredGroups = computed(() => {
  if (!search.value) return contactGroups.value;

  const q = search.value.toLowerCase();
  return contactGroups.value
    .map((group) => {
      const filteredUsers = group.users.filter(
        (u) =>
          u.name.toLowerCase().includes(q) ||
          u.username.toLowerCase().includes(q)
      );
      if (group.label.toLowerCase().includes(q) || filteredUsers.length > 0) {
        return {
          ...group,
          users: filteredUsers.length > 0 ? filteredUsers : group.users,
          count: filteredUsers.length > 0 ? filteredUsers.length : group.count,
        };
      }
      return null;
    })
    .filter(Boolean);
});

// هل جميع أعضاء المجموعة محددين؟
function isGroupFullySelected(group) {
  return group.users.every((u) => selectedUsers.value.includes(u.id));
}

// نص عدد المحددين
function getGroupSelectionText(group) {
  const selected = group.users.filter((u) =>
    selectedUsers.value.includes(u.id)
  ).length;
  if (selected === 0) return `${group.count} مستخدم`;
  return `${selected} / ${group.count} محدد`;
}

// تحديد/إلغاء تحديد مجموعة كاملة
function toggleGroupSelection(group) {
  const allIds = group.users.map((u) => u.id);
  if (isGroupFullySelected(group)) {
    selectedUsers.value = selectedUsers.value.filter(
      (id) => !allIds.includes(id)
    );
  } else {
    const newIds = allIds.filter((id) => !selectedUsers.value.includes(id));
    selectedUsers.value.push(...newIds);
  }
}

async function fetchGroupedContacts() {
  loading.value = true;
  try {
    const data = await chatService.getGroupedContacts();
    contactGroups.value = (data.groups || []).map((g) => ({
      ...g,
      users: g.users.map((u) => ({
        id: u.id,
        name: u.full_name || u.username,
        username: u.username,
        avatar: u.profile_picture,
      })),
    }));
  } catch (error) {
    console.error("Error fetching grouped contacts", error);
    try {
      const results = await chatService.getAllowedContacts();
      contactGroups.value = [
        {
          key: "all",
          label: "جهات الاتصال",
          icon: "mdi-account-group",
          count: results.length,
          metadata: {},
          users: results.map((u) => ({
            id: u.id,
            name: u.full_name || u.username,
            username: u.username,
            avatar: u.profile_picture,
          })),
        },
      ];
    } catch (e2) {
      console.error("Fallback also failed", e2);
    }
  } finally {
    loading.value = false;
  }
}

// Fetch initial list on open
watch(
  () => props.modelValue,
  (isOpen) => {
    if (isOpen) {
      search.value = "";
      fetchGroupedContacts();

      // تطبيق التحديد المسبق إذا وجد
      if (props.preSelectedMemberIds.length > 0) {
        selectedUsers.value = [...props.preSelectedMemberIds];
      } else {
        selectedUsers.value = [];
      }

      if (props.preSelectedName) {
        groupName.value = props.preSelectedName;
      } else {
        groupName.value = "";
      }

      isPrivate.value = false;
    }
  }
);

function toggleSelection(user) {
  const minIndex = selectedUsers.value.indexOf(user.id);
  if (minIndex === -1) {
    selectedUsers.value.push(user.id);
  } else {
    selectedUsers.value.splice(minIndex, 1);
  }

  groupImage.value = null;
  if (groupImagePreview.value) {
    URL.revokeObjectURL(groupImagePreview.value);
  }
  groupImagePreview.value = null;
  if (fileInput.value) {
    fileInput.value.value = "";
  }
}

function removeSelection(userId) {
  const index = selectedUsers.value.indexOf(userId);
  if (index !== -1) {
    selectedUsers.value.splice(index, 1);
  }
}

function createGroup() {
  emit("create-group", {
    name: groupName.value,
    participants: selectedUsers.value,
    isPrivate: isPrivate.value,
    image: groupImage.value,
  });
  emit("update:modelValue", false);
}
</script>

<style scoped>
/* Inputs */
.premium-input :deep(.v-field), .premium-search :deep(.v-field) {
  border: 1px solid rgba(var(--v-border-color), 0.08) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03) !important;
  transition: all 0.3s ease;
  background: rgba(var(--v-theme-surface), 1);
}
.premium-input :deep(.v-field--focused), .premium-search :deep(.v-field--focused) {
  border-color: rgba(var(--v-theme-primary), 0.5) !important;
  box-shadow: 0 4px 20px rgba(var(--v-theme-primary), 0.1) !important;
}

/* Avatar Group */
.premium-avatar {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 4px solid rgba(var(--v-theme-surface), 1);
}
.premium-avatar.on-hover {
  transform: scale(1.05);
  box-shadow: 0 12px 24px rgba(0,0,0,0.15) !important;
}
.avatar-gradient {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}
.avatar-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}
.avatar-overlay.show {
  opacity: 1;
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

/* Users */
.premium-user-item {
  transition: all 0.2s ease;
  background: transparent;
  border: 1px solid transparent;
  cursor: pointer;
}
.premium-user-item:hover {
  background: rgba(var(--v-theme-primary), 0.02);
  border-color: rgba(var(--v-theme-primary), 0.1);
}
.premium-user-item.selected-item {
  background: rgba(var(--v-theme-primary), 0.06);
  border-color: rgba(var(--v-theme-primary), 0.3);
}

.gradient-avatar {
  background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
}
.border-avatar {
  border: 2px solid rgba(var(--v-theme-surface), 1);
}

/* Custom Checkbox */
.premium-checkbox {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  border: 2px solid rgba(var(--v-border-color), 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  background: transparent;
}
.premium-checkbox.checked {
  background: rgb(var(--v-theme-primary));
  border-color: rgb(var(--v-theme-primary));
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.3);
}

/* Private Card */
.private-group-card {
  background: rgba(var(--v-theme-surface), 1) !important;
  border: 1px solid rgba(var(--v-border-color), 0.08) !important;
  transition: all 0.3s ease;
}
.private-group-card.active-private {
  border-color: rgba(var(--v-theme-primary), 0.4) !important;
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.08) !important;
}
.icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

/* Utilities */
.shadow-lg { box-shadow: 0 10px 25px -3px rgba(0,0,0,0.1); }
.shadow-sm { box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.shadow-primary { box-shadow: 0 8px 16px rgba(var(--v-theme-primary), 0.3); }

.empty-state-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(var(--v-theme-primary), 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-scrollbar::-webkit-scrollbar, .custom-scrollbar-x::-webkit-scrollbar {
  width: 6px; height: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track, .custom-scrollbar-x::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb, .custom-scrollbar-x::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.15);
  border-radius: 10px;
}
</style>
