<template>
  <custom-dialog
    :model-value="dialog"
    @update:model-value="dialog = $event"
    :title="$t('chat.header.groupInfo') || 'معلومات المجموعة'"
    width="480"
  >
    <!-- Group Header Section (Centered) -->
    <div class="d-flex flex-column align-center text-center pt-2 pb-6">
      <div class="position-relative mb-4">
        <v-hover v-slot="{ isHovering, props }" :disabled="!isAdmin">
          <v-avatar
            class="premium-group-avatar elevation-2"
            :class="{ 'cursor-pointer': isAdmin, 'on-hover': isHovering }"
            size="110"
            v-bind="props"
            @click="isAdmin && triggerImageUpload()"
          >
            <v-img
              v-if="group?.group_picture"
              cover
              :src="group.group_picture"
            />
            <div
              v-else
              class="group-avatar-gradient w-100 h-100 d-flex align-center justify-center font-weight-black text-h4 text-white"
            >
              {{ (group?.name || "G").charAt(0) }}
            </div>
            <!-- Admin Hover Camera Overlay -->
            <div v-if="isAdmin && isHovering" class="avatar-camera-overlay">
              <v-icon color="white" size="28">mdi-camera-plus</v-icon>
            </div>
          </v-avatar>
        </v-hover>
        <input
          ref="imageInput"
          accept="image/*"
          class="d-none"
          type="file"
          @change="handleImageChange"
        />
      </div>

      <!-- Group Name (Editable for Admins) -->
      <div v-if="isEditing" class="w-100 px-4 mb-2">
        <v-text-field
          v-model="editName"
          class="premium-input-edit"
          density="comfortable"
          hide-details
          :placeholder="$t('chat.newGroup.groupNamePlaceholder') || 'اسم المجموعة'"
          rounded="xl"
          variant="solo"
          elevation="0"
        >
          <template #append-inner>
            <custom-btn color="success" isIcon icon="mdi-check" size="small" variant="flat" class="me-1" :click="saveChanges" :loading="saving" />
            <custom-btn color="error" isIcon icon="mdi-close" size="small" variant="flat" :click="cancelEdit" :disabled="saving" />
          </template>
        </v-text-field>
      </div>

      <div v-else class="w-100 px-4">
        <h2 class="text-h5 font-weight-black mb-1 color-text-primary d-flex align-center justify-center">
          {{ group?.name || $t("chat.header.groupDefaultName", "مجموعة") }}
          <custom-btn
            v-if="isAdmin"
            class="ms-2 edit-name-btn"
            isIcon
            icon="mdi-pencil"
            size="x-small"
            variant="tonal"
            color="primary"
            :click="startEditing"
          />
        </h2>
        <p class="text-caption text-medium-emphasis font-weight-bold mb-0 text-uppercase tracking-wider">
          {{ $t("chat.info.created", { date: formatDate(group?.created_at) }) || `تم الإنشاء في ${formatDate(group?.created_at)}` }}
        </p>
      </div>
    </div>

    <v-divider class="mb-5" opacity="0.08" />

    <!-- Admin Operations Panel -->
    <div v-if="isAdmin" class="admin-settings-section mb-6">
      <div class="d-flex align-center mb-3">
        <span class="section-label">تنظيم وإدارة المجموعة</span>
        <v-divider class="ms-3" opacity="0.08" />
      </div>

      <v-card class="premium-control-card mb-3" elevation="0" rounded="xl">
        <div class="d-flex align-center pa-4">
          <div class="control-icon-wrapper bg-primary-lighten-5 text-primary me-4">
            <v-icon size="20">mdi-account-plus</v-icon>
          </div>
          <div class="flex-grow-1">
            <h4 class="text-subtitle-2 font-weight-bold mb-0">إضافة مشاركين جدد</h4>
            <p class="text-caption text-medium-emphasis mb-0">قم بإضافة جهات الاتصال الخاصة بك للمجموعة.</p>
          </div>
          <custom-btn
            color="primary"
            variant="tonal"
            size="small"
            class="font-weight-bold px-4"
            :click="() => $emit('addMembers')"
            label="إضافة"
          />
        </div>
      </v-card>

      <!-- Toggle Read Only Switch Control -->
      <v-card class="premium-control-card" elevation="0" rounded="xl">
        <div class="d-flex align-center pa-4">
          <div class="control-icon-wrapper bg-primary-lighten-5 text-primary me-4">
            <v-icon size="20">mdi-message-lock-outline</v-icon>
          </div>
          <div class="flex-grow-1">
            <h4 class="text-subtitle-2 font-weight-bold mb-0">{{ $t("chat.info.readOnlyMode") || "المراسلة للمشرفين فقط" }}</h4>
            <p class="text-caption text-medium-emphasis mb-0">عند التفعيل، يحق فقط للمشرفين إرسال الرسائل.</p>
          </div>
          <div class="ms-4">
            <v-switch
              color="primary"
              density="compact"
              hide-details
              inset
              :model-value="group?.is_read_only"
              @update:model-value="toggleReadOnly"
            />
          </div>
        </div>
      </v-card>
    </div>

    <!-- Participants / Members list -->
    <div class="members-section mb-2">
      <div class="d-flex align-center mb-3">
        <span class="section-label">
          {{ $t("chat.info.participants", { count: group?.participants_data?.length || 0 }) || `الأعضاء (${group?.participants_data?.length || 0})` }}
        </span>
        <v-divider class="ms-3" opacity="0.08" />
      </div>

      <v-card class="premium-list-card" elevation="0" rounded="xl">
        <div class="scrollable-members-list custom-scrollbar">
          <v-list bg-color="transparent" class="py-2" density="comfortable">
            <v-list-item
              v-for="participant in sortedParticipants"
              :key="participant.id"
              class="premium-member-item px-4 py-2"
            >
              <template #prepend>
                <div class="position-relative me-4">
                  <v-avatar size="44" class="member-avatar elevation-1">
                    <v-img
                      v-if="participant.user.profile_picture"
                      cover
                      :src="participant.user.profile_picture"
                    />
                    <div
                      v-else
                      class="gradient-avatar w-100 h-100 d-flex align-center justify-center text-white font-weight-bold text-subtitle-1"
                    >
                      {{ (participant.user.full_name || participant.user.username || "U").charAt(0).toUpperCase() }}
                    </div>
                  </v-avatar>
                  <!-- Member Online Dot Indicator -->
                  <div v-if="participant.user.is_online" class="online-indicator-dot" />
                </div>
              </template>

              <!-- Participant Name & Chips -->
              <v-list-item-title class="font-weight-bold text-body-2 mb-1 d-flex align-center">
                <span class="text-truncate">{{ participant.user.full_name || participant.user.username }}</span>
                <!-- Admin Tag chip -->
                <v-chip
                  v-if="participant.is_admin"
                  class="ms-2 font-weight-black"
                  color="primary"
                  size="x-small"
                  variant="flat"
                >
                  {{ $t("chat.info.admin") || 'مشرف' }}
                </v-chip>
                <!-- Current User Chip -->
                <v-chip
                  v-if="participant.user.id == currentUserId"
                  class="ms-1 font-weight-black"
                  color="success"
                  size="x-small"
                  variant="tonal"
                >
                  {{ $t("chat.info.you") || 'أنت' }}
                </v-chip>
              </v-list-item-title>

              <!-- Participant Online Status subtitle -->
              <v-list-item-subtitle class="text-caption text-medium-emphasis">
                {{ participant.user.is_online ? ($t("chat.online") || 'متصل الآن') : ($t("chat.offline") || 'غير متصل') }}
              </v-list-item-subtitle>

              <!-- Admin Controls settings menu -->
              <template v-if="isAdmin && participant.user.id != currentUserId" #append>
                <v-menu location="start" z-index="9999" transition="slide-y-transition" :close-on-content-click="true">
                  <template #activator="{ props: menuProps }">
                    <custom-btn
                      isIcon
                      icon="mdi-dots-vertical"
                      size="small"
                      variant="text"
                      color="medium-emphasis"
                      class="rounded-circle action-menu-trigger"
                      v-bind="menuProps"
                    />
                  </template>
                  
                  <v-list class="premium-menu pa-2" density="compact" rounded="xl" elevation="8">
                    <!-- Make/Remove Admin action option -->
                    <v-list-item
                      v-if="!participant.is_admin"
                      class="rounded-lg mb-1"
                      @click="$emit('makeAdmin', participant.user.id)"
                    >
                      <template #prepend><v-icon color="primary" size="20" class="me-3">mdi-shield-account</v-icon></template>
                      <v-list-item-title class="font-weight-medium">{{ $t("chat.info.makeAdmin") || 'تعيين كمشرف' }}</v-list-item-title>
                    </v-list-item>
                    <v-list-item
                      v-else
                      class="rounded-lg mb-1"
                      @click="$emit('removeAdmin', participant.user.id)"
                    >
                      <template #prepend><v-icon color="warning" size="20" class="me-3">mdi-shield-off</v-icon></template>
                      <v-list-item-title class="font-weight-medium">{{ $t("chat.info.removeAdmin") || 'إزالة الإشراف' }}</v-list-item-title>
                    </v-list-item>

                    <!-- Mute/Unmute Member messaging option -->
                    <v-list-item
                      class="rounded-lg mb-1"
                      @click="toggleMemberMessaging(participant.user.id)"
                    >
                      <template #prepend>
                        <v-icon :color="participant.can_send_messages ? 'warning' : 'success'" size="20" class="me-3">
                          {{ participant.can_send_messages ? "mdi-message-off" : "mdi-message-text" }}
                        </v-icon>
                      </template>
                      <v-list-item-title class="font-weight-medium">
                        {{ participant.can_send_messages ? ($t("chat.info.muteMember") || "كتم العضو") : ($t("chat.info.unmuteMember") || "إلغاء كتم العضو") }}
                      </v-list-item-title>
                    </v-list-item>

                    <v-divider class="my-1 border-opacity-10" />

                    <!-- Remove participant from Group option -->
                    <v-list-item
                      class="rounded-lg text-error"
                      @click="$emit('removeMember', participant.user.id)"
                    >
                      <template #prepend><v-icon color="error" size="20" class="me-3">mdi-account-remove</v-icon></template>
                      <v-list-item-title class="font-weight-medium">{{ $t("chat.info.removeMember") || 'إزالة من المجموعة' }}</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </template>
            </v-list-item>
          </v-list>
        </div>
      </v-card>
    </div>

    <!-- Shared Media Section -->
    <SharedMediaSection v-if="group?.id" :chat-id="group.id" />

    <!-- Actions slot -->
    <template #actions>
      <custom-btn
        type="cancel"
        :click="() => dialog = false"
      />
      <v-spacer />
      <custom-btn
        color="error"
        variant="flat"
        icon="mdi-exit-run"
        :click="() => $emit('leaveGroup')"
        :label="$t('chat.leaveGroup') || 'مغادرة المجموعة'"
      />
    </template>
  </custom-dialog>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useDisplay } from "vuetify";
import SharedMediaSection from './SharedMediaSection.vue'
import { chatService } from "../../services/chatService";
import { useChatStore } from "../../store/chat";

const props = defineProps({
  modelValue: Boolean,
  group: {
    type: Object,
    default: null,
  },
  currentUserId: {
    type: Number,
    default: null,
  },
});

const emit = defineEmits([
  "update:modelValue",
  "addMembers",
  "removeMember",
  "makeAdmin",
  "removeAdmin",
  "leaveGroup",
  "updated",
]);

const { t, locale } = useI18n();
const { xs } = useDisplay();
const chatStore = useChatStore();

const dialog = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});

const imageInput = ref(null);
const isEditing = ref(false);
const editName = ref("");
const saving = ref(false);

const isAdmin = computed(() => props.group?.current_user_is_admin || false);

const sortedParticipants = computed(() => {
  if (!props.group?.participants_data) return [];
  return [...props.group.participants_data]
    .filter((p) => p && p.user)
    .sort((a, b) => {
      if (a.is_admin && !b.is_admin) return -1;
      if (!a.is_admin && b.is_admin) return 1;
      return 0;
    });
});

function formatDate(date) {
  if (!date) return "";
  return new Date(date).toLocaleDateString(locale.value, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

function startEditing() {
  editName.value = props.group?.name || "";
  isEditing.value = true;
}

function cancelEdit() {
  isEditing.value = false;
  editName.value = "";
}

async function saveChanges() {
  if (!editName.value.trim()) return;

  saving.value = true;
  try {
    await chatService.updateGroup(props.group.id, {
      name: editName.value.trim(),
    });
    emit("updated");
    isEditing.value = false;
  } catch (error) {
    console.error("Error updating group:", error);
  } finally {
    saving.value = false;
  }
}

async function toggleReadOnly() {
  if (!props.group) return;
  try {
    await chatStore.toggleReadOnly(props.group.id);
    emit("updated");
  } catch (error) {
    console.error("Error toggling read-only:", error);
  }
}

async function toggleMemberMessaging(userId) {
  if (!props.group) return;
  try {
    await chatStore.toggleMemberMessaging(props.group.id, userId);
    emit("updated");
  } catch (error) {
    console.error("Error toggling member messaging:", error);
  }
}

function triggerImageUpload() {
  imageInput.value?.click();
}

async function handleImageChange(event) {
  const file = event.target.files?.[0];
  if (!file) return;

  saving.value = true;
  try {
    await chatService.updateGroup(props.group.id, { group_picture: file });
    emit("updated");
  } catch (error) {
    console.error("Error updating group picture:", error);
  } finally {
    saving.value = false;
    if (imageInput.value) imageInput.value.value = "";
  }
}

watch(dialog, (val) => {
  if (!val) {
    isEditing.value = false;
    editName.value = "";
  }
});
</script>

<style scoped>
.premium-group-avatar {
  border: 3px solid rgba(var(--v-theme-primary), 0.15) !important;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  background: rgba(var(--v-theme-surface), 1);
}
.premium-group-avatar.on-hover {
  transform: scale(1.05);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.12) !important;
}
.group-avatar-gradient {
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
}
.avatar-camera-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.premium-input-edit :deep(.v-field) {
  border: 1px solid rgba(var(--v-border-color), 0.08) !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03) !important;
  background: rgba(var(--v-theme-surface), 1);
  border-radius: 28px;
}
.premium-input-edit :deep(.v-field--focused) {
  border-color: rgba(var(--v-theme-primary), 0.5) !important;
  box-shadow: 0 4px 16px rgba(var(--v-theme-primary), 0.08) !important;
}

.edit-name-btn {
  opacity: 0.7;
  transition: all 0.25s ease;
}
.edit-name-btn:hover {
  opacity: 1;
  transform: scale(1.08);
}

.section-label {
  font-size: 0.785rem;
  font-weight: 700;
  color: rgb(var(--v-theme-primary));
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.premium-control-card {
  border: 1px solid rgba(var(--v-border-color), 0.08) !important;
  background: rgba(var(--v-theme-surface), 1);
  transition: all 0.25s ease;
}
.premium-control-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.15) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
}

.control-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.bg-primary-lighten-5 {
  background-color: rgba(var(--v-theme-primary), 0.06) !important;
}

.premium-list-card {
  border: 1px solid rgba(var(--v-border-color), 0.08) !important;
  background: rgba(var(--v-theme-surface), 1);
  overflow: hidden;
}

.scrollable-members-list {
  max-height: 280px;
  overflow-y: auto;
}

.premium-member-item {
  transition: all 0.2s ease;
  cursor: pointer;
}
.premium-member-item:hover {
  background: rgba(var(--v-theme-primary), 0.02);
}

.member-avatar {
  border: 2px solid rgba(var(--v-theme-surface), 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.gradient-avatar {
  background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
}

.online-indicator-dot {
  position: absolute;
  bottom: 1px;
  right: 1px;
  width: 13px;
  height: 13px;
  border-radius: 50%;
  background: #22c55e;
  border: 2px solid rgb(var(--v-theme-surface));
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
}

.action-menu-trigger {
  opacity: 0.65;
  transition: all 0.25s ease;
}
.action-menu-trigger:hover {
  opacity: 1;
  background: rgba(var(--v-theme-primary), 0.05);
  color: rgb(var(--v-theme-primary)) !important;
}

.premium-menu {
  border: 1px solid rgba(var(--v-border-color), 0.05) !important;
}
.premium-menu .v-list-item:hover {
  background: rgba(var(--v-theme-primary), 0.04) !important;
}

.color-text-primary {
  color: rgb(var(--v-theme-on-surface));
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.12);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-on-surface), 0.25);
}

.cursor-pointer {
  cursor: pointer;
}
</style>
