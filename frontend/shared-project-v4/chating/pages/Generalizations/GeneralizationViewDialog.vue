<template>
  <custom-dialog v-model="internalModelValue" title="تفاصيل التعميم الإداري" width="680">
    <div v-if="generalization" class="d-flex flex-column gap-4 py-1">
      <!-- Sender info card -->
      <v-card
        variant="flat"
        class="pa-4 rounded-xl border-thin sender-profile-card d-flex align-center bg-surface"
      >
        <div class="avatar-ring me-4">
          <v-avatar color="primary" variant="tonal" size="52" class="border-avatar">
            <v-img
              v-if="generalization.sender_data?.profile_picture"
              :src="generalization.sender_data.profile_picture"
            ></v-img>
            <span v-else class="text-h6 text-primary font-weight-black">{{
              generalization.sender_data?.first_name?.charAt(0) || "م"
            }}</span>
          </v-avatar>
        </div>
        <div class="flex-grow-1">
          <div class="text-subtitle-1 font-weight-black color-text-primary mb-1">
            {{ generalization.sender_data?.full_name || "المرسل" }}
          </div>
          <div class="text-caption text-medium-emphasis d-flex align-center">
            <v-icon
              icon="mdi-calendar-range"
              size="14"
              class="me-1"
              color="primary"
            ></v-icon>
            <span>تاريخ النشر:</span>
            <span class="font-weight-bold ms-1 color-text-primary">{{
              formatDate(generalization.created_at)
            }}</span>
          </div>
        </div>
        <v-chip
          size="small"
          color="primary"
          variant="tonal"
          class="font-weight-black px-3 rounded-lg"
          >إداري</v-chip
        >
      </v-card>

      <!-- Generalization Title -->
      <h2 class="text-h5 font-weight-black mb-1 color-text-primary title-accent">
        {{ generalization.title }}
      </h2>

      <!-- Generalization Content -->
      <v-card variant="flat" class="pa-5 rounded-xl border-thin bg-surface content-card">
        <div class="text-body-1 color-text-primary text-pre-wrap leading-relaxed">
          {{ generalization.content }}
        </div>
      </v-card>

      <!-- Attachments -->
      <div
        v-if="
          generalization.attachments_data && generalization.attachments_data.length > 0
        "
        class="attachments-section"
      >
        <div class="px-1 py-1 d-flex align-center mb-2">
          <v-icon icon="mdi-paperclip" color="primary" class="me-2" size="20"></v-icon>
          <span class="text-subtitle-2 font-weight-bold color-text-primary"
            >المستندات المرفقة ({{ generalization.attachments_data.length }})</span
          >
        </div>
        <div class="attachments-grid">
          <v-card
            v-for="(attachment, index) in generalization.attachments_data"
            :key="attachment.id"
            variant="flat"
            class="attachment-item-card pa-3 mb-2 rounded-xl d-flex align-center justify-space-between cursor-pointer border-thin bg-surface"
            @click="previewAttachment(attachment)"
          >
            <div class="d-flex align-center overflow-hidden">
              <div class="file-icon-box me-3">
                <v-icon
                  icon="mdi-file-pdf-box"
                  color="error"
                  size="28"
                  v-if="attachment.file_url?.toLowerCase().endsWith('.pdf')"
                ></v-icon>
                <v-icon
                  icon="mdi-file-document-outline"
                  color="primary"
                  size="28"
                  v-else
                ></v-icon>
              </div>
              <div class="text-truncate" style="max-width: 250px">
                <div
                  class="text-body-2 font-weight-bold color-text-primary text-truncate"
                  :title="getFileName(attachment)"
                >
                  {{ getFileName(attachment) }}
                </div>
                <div class="text-caption text-medium-emphasis">
                  انقر للمعاينة والتحميل
                </div>
              </div>
            </div>
            <v-btn
              color="primary"
              variant="tonal"
              size="small"
              class="rounded-lg px-3"
              @click.stop="previewAttachment(attachment)"
            >
              <v-icon icon="mdi-eye" size="18" class="me-1"></v-icon>
              معاينة
            </v-btn>
          </v-card>
        </div>
      </div>

      <!-- =================== REPLY SECTION =================== -->
      <template v-if="generalization.allow_replies">
        <v-divider class="my-2" opacity="0.08" />

        <div v-if="loadingReplies" class="text-center pa-5">
          <v-progress-circular
            indeterminate
            color="primary"
            size="32"
          ></v-progress-circular>
        </div>

        <template v-else>
          <!-- A. Sender View: See all replies -->
          <div v-if="isSender" class="replies-section">
            <v-card
              variant="flat"
              class="rounded-xl pa-5 text-center sender-dashboard-card bg-surface"
            >
              <div class="dashboard-icon-pulse mb-3">
                <v-icon icon="mdi-reply-all-outline" size="32" color="primary"></v-icon>
              </div>
              <h3 class="text-subtitle-1 font-weight-black mb-1 color-text-primary">
                لوحة الردود والتعقيبات
              </h3>
              <p class="text-caption text-medium-emphasis mb-5">
                تابع الردود والملاحظات الواردة من الجهات والموظفين المستهدفين بالتعميم.
              </p>
              <v-btn
                color="primary"
                variant="flat"
                size="large"
                class="rounded-xl font-weight-bold px-8 shadow-primary open-dashboard-btn"
                @click="openRepliesPage"
              >
                <span>عرض قائمة الردود كاملة</span>
                <v-icon end icon="mdi-arrow-left" class="ms-2"></v-icon>
              </v-btn>
            </v-card>
          </div>

          <!-- B. Recipient View -->
          <div v-else class="recipient-reply-section">
            <!-- If already replied -->
            <v-card
              v-if="myReply"
              color="success"
              variant="tonal"
              class="rounded-xl pa-5 text-center success-reply-card"
            >
              <div class="d-flex align-center justify-center mb-3">
                <v-avatar color="success" size="32" class="me-2 text-white">
                  <v-icon icon="mdi-check" size="18"></v-icon>
                </v-avatar>
                <span class="text-subtitle-1 font-weight-black text-success"
                  >تم إتمام الرد الرسمي على هذا التعميم</span
                >
              </div>
              <v-card
                variant="flat"
                class="pa-4 bg-surface rounded-xl text-right border-thin mb-3"
              >
                <div class="text-caption text-medium-emphasis mb-1">
                  تفاصيل ردك المرسل:
                </div>
                <div
                  v-if="myReply.content"
                  class="text-body-2 color-text-primary font-weight-medium"
                >
                  {{ myReply.content }}
                </div>
                <div v-else class="text-body-2 text-disabled italic">
                  رد فارغ بدون تعليق
                </div>
              </v-card>
              <div
                v-if="myReply.attachments_data && myReply.attachments_data.length > 0"
                class="d-flex flex-wrap justify-center gap-2 mt-2"
              >
                <v-btn
                  v-for="(attachment, index) in myReply.attachments_data"
                  :key="attachment.id"
                  @click="previewAttachment(attachment)"
                  color="success"
                  variant="tonal"
                  prepend-icon="mdi-paperclip"
                  class="rounded-xl font-weight-bold text-body-2 mb-2"
                  style="max-width: 250px"
                  :title="getFileName(attachment)"
                >
                  <span class="text-truncate">{{ getFileName(attachment) }}</span>
                </v-btn>
              </div>
            </v-card>

            <!-- If they haven't replied -->
            <v-card
              v-else
              variant="flat"
              class="rounded-xl pa-5 bg-surface border-thin reply-form-card"
            >
              <div class="d-flex align-center mb-4">
                <div class="reply-icon-box me-3">
                  <v-icon icon="mdi-reply" color="primary" size="20"></v-icon>
                </div>
                <h3 class="text-subtitle-1 font-weight-black color-text-primary">
                  إرسال رد مباشر على التعميم
                </h3>
              </div>
              <v-form
                ref="replyFormRef"
                v-model="formValid"
                @submit.prevent="submitMyReply"
              >
                <v-textarea
                  v-model="replyText"
                  label="اكتب ملاحظاتك أو ردك الرسمي..."
                  variant="solo"
                  density="comfortable"
                  color="primary"
                  rows="3"
                  class="mb-4 rounded-xl custom-textarea"
                  elevation="0"
                ></v-textarea>

                <v-file-input
                  v-model="replyFile"
                  label="إرفاق وثيقة أو مستند (اختياري)..."
                  variant="solo"
                  density="comfortable"
                  color="primary"
                  prepend-icon=""
                  prepend-inner-icon="mdi-cloud-upload"
                  class="mb-5 custom-file-input"
                  accept=".pdf,.doc,.docx,.xls,.xlsx,image/jpeg,image/png,image/jpg"
                  :rules="[fileSizeRule]"
                  elevation="0"
                  multiple
                ></v-file-input>

                <div class="d-flex justify-end">
                  <v-btn
                    type="submit"
                    color="primary"
                    variant="flat"
                    :loading="submitting"
                    :disabled="!replyText && !replyFile"
                    class="rounded-xl px-8 py-2 font-weight-black text-subtitle-2 shadow-primary"
                  >
                    <span>إرسال الرد الرسمي</span>
                    <v-icon end icon="mdi-send" class="ms-2"></v-icon>
                  </v-btn>
                </div>
              </v-form>
            </v-card>
          </div>
        </template>
      </template>
    </div>

    <!-- Actions Footer -->
    <template #actions>
      <v-spacer></v-spacer>
      <v-btn
        variant="text"
        color="grey-darken-1"
        @click="closeDialog"
        class="rounded-pill px-6 font-weight-bold text-body-2"
      >
        إغلاق
      </v-btn>
    </template>

    <!-- Nesting Attachment Preview Dialog inside custom-dialog -->
    <AttachmentPreviewDialog
      v-model="showPreviewDialog"
      :file-url="previewFileUrl"
      :file-name="previewFileName"
    />
  </custom-dialog>
</template>

<script setup>
import { ref, computed, watch } from "vue";

import { useGeneralizationStore } from "../../store/generalizationStore";
import AttachmentPreviewDialog from "../../components/AttachmentPreviewDialog.vue";
import { useAuthStore } from "../../../src/UserManagement/stores/auth";

import { getRouter } from "../../../src/router/routerInstance";

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  generalization: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["update:modelValue", "replied"]);
const genStore = useGeneralizationStore();
const authStore = useAuthStore();

const internalModelValue = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});

const isSender = computed(() => {
  return props.generalization?.sender_data?.id === authStore.user?.id;
});

// Reply State
const loadingReplies = ref(false);
const submitting = ref(false);
const myReply = ref(null);
const repliesList = ref([]);

// Preview Dialog State
const showPreviewDialog = ref(false);
const previewFileUrl = ref("");
const previewFileName = ref("");

const getFileName = (attachment) => {
  if (attachment.name) return attachment.name;
  if (!attachment.file_url) return "مستند مرفق";
  try {
    const url = new URL(attachment.file_url);
    const parts = url.pathname.split("/");
    return decodeURIComponent(parts[parts.length - 1] || "مستند مرفق");
  } catch (e) {
    const parts = attachment.file_url.split("/");
    return parts[parts.length - 1] || "مستند مرفق";
  }
};

const previewAttachment = (attachment) => {
  previewFileUrl.value = attachment.file_url;
  previewFileName.value = getFileName(attachment);
  showPreviewDialog.value = true;
};

// Form State
const formValid = ref(false);
const replyFormRef = ref(null);

const fileSizeRule = (files) => {
  if (!files || !files.length) return true;
  const maxSize = 10 * 1024 * 1024; // 10MB
  for (let i = 0; i < files.length; i++) {
    if (files[i].size > maxSize) {
      return `حجم الملف ${files[i].name} يجب أن لا يتجاوز 10 ميجابايت`;
    }
  }
  return true;
};

const replyText = ref("");
const replyFile = ref(null);

watch(
  () => props.modelValue,
  async (isOpen) => {
    if (isOpen && props.generalization) {
      myReply.value = null;
      repliesList.value = [];
      replyText.value = "";
      replyFile.value = null;

      if (props.generalization.allow_replies) {
        loadingReplies.value = true;
        try {
          if (isSender.value) {
            repliesList.value = await genStore.fetchReplies(props.generalization.id);
          } else {
            myReply.value = await genStore.fetchMyReply(props.generalization.id);
          }
        } catch (err) {
          console.error("Failed to load reply data", err);
        } finally {
          loadingReplies.value = false;
        }
      }
    }
  }
);

const closeDialog = () => {
  internalModelValue.value = false;
};

const openRepliesPage = () => {
  closeDialog();

  const router = getRouter();

  router.push(`/generalizations-view/generalizations/${props.generalization.id}/replies`);
};

const formatDate = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  return (
    date.toLocaleDateString("ar-EG", { day: "numeric", month: "long", year: "numeric" }) +
    " | " +
    date.toLocaleTimeString("ar-EG", { hour: "2-digit", minute: "2-digit" })
  );
};

const submitMyReply = async () => {
  if (!replyText.value && !replyFile.value) return;
  submitting.value = true;
  try {
    const formData = new FormData();
    if (replyText.value) formData.append("content", replyText.value);

    if (replyFile.value) {
      if (Array.isArray(replyFile.value) && replyFile.value.length > 0) {
        replyFile.value.forEach((file) => {
          formData.append("attachments", file);
        });
      } else if (replyFile.value instanceof File) {
        formData.append("attachments", replyFile.value);
      }
    }

    const result = await genStore.submitReply(props.generalization.id, formData);
    myReply.value = result;
    if (props.generalization) {
      props.generalization.has_replied = true;
    }
    emit("replied", result);
  } catch (err) {
    console.error("Failed to submit reply", err);
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.sender-profile-card {
  border: 1px solid rgba(var(--v-theme-primary), 0.1) !important;
  box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.03) !important;
}

.avatar-ring {
  padding: 3px;
  border-radius: 50%;
  border: 2px dashed rgba(var(--v-theme-primary), 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
}

.border-avatar {
  border: 1px solid rgb(var(--v-theme-primary));
}

.title-accent {
  position: relative;
  padding-inline-start: 14px;
}

.title-accent::before {
  content: "";
  position: absolute;
  top: 4px;
  bottom: 4px;
  left: 0;
  width: 5px;
  background: rgb(var(--v-theme-primary));
  border-radius: 4px;
}

.content-card {
  box-shadow: 0 8px 20px -6px rgba(0, 0, 0, 0.04) !important;
  border-inline-start: 3.5px solid rgb(var(--v-theme-primary)) !important;
}

.leading-relaxed {
  line-height: 1.8;
  font-size: 1.05rem;
}

.attachment-item-card {
  transition: all 0.25s ease;
}

.attachment-item-card:hover {
  border-color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.06) !important;
  transform: translateY(-2px);
}

.file-icon-box {
  background: rgba(var(--v-theme-on-surface), 0.03);
  padding: 8px;
  border-radius: 10px;
}

.sender-dashboard-card {
  border: 1px dashed rgba(var(--v-theme-primary), 0.2) !important;
  background: rgba(var(--v-theme-primary), 0.02) !important;
}

.dashboard-icon-pulse {
  display: inline-flex;
  background: rgba(var(--v-theme-primary), 0.08);
  padding: 14px;
  border-radius: 50%;
  animation: pulse-dashboard-icon 2.5s infinite;
}

@keyframes pulse-dashboard-icon {
  0% {
    box-shadow: 0 0 0 0 rgba(var(--v-theme-primary), 0.15);
  }

  70% {
    box-shadow: 0 0 0 10px rgba(var(--v-theme-primary), 0);
  }

  100% {
    box-shadow: 0 0 0 0 rgba(var(--v-theme-primary), 0);
  }
}

.shadow-primary {
  box-shadow: 0 6px 15px -3px rgba(var(--v-theme-primary), 0.3) !important;
}

.reply-form-card {
  border: 1px solid rgba(var(--v-theme-primary), 0.08) !important;
  box-shadow: 0 8px 24px -10px rgba(0, 0, 0, 0.05) !important;
}

.reply-icon-box {
  background: rgba(var(--v-theme-primary), 0.08);
  padding: 6px;
  border-radius: 8px;
}

.success-reply-card {
  border: 1px solid rgba(var(--v-theme-success), 0.15) !important;
  background-color: rgba(var(--v-theme-success), 0.04) !important;
}

.custom-textarea :deep(.v-field) {
  border: 1px solid rgba(var(--v-border-color), 0.08) !important;
  border-radius: 14px !important;
  background: rgba(var(--v-theme-surface), 1);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.02) !important;
}

.custom-file-input :deep(.v-field) {
  border: 1px solid rgba(var(--v-border-color), 0.08) !important;
  border-radius: 14px !important;
  background: rgba(var(--v-theme-surface), 1);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.02) !important;
}

.color-text-primary {
  color: rgb(var(--v-theme-on-surface));
}

.gap-4 {
  gap: 16px;
}
</style>
