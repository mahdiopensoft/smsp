<template>
  <div class="generalization-replies-screen pa-6 bg-background">
    <!-- Header Banner -->
    <v-card
      class="flex-shrink-0 rounded-xl overflow-hidden mb-6 border-0 shadow-lg position-relative"
      elevation="4"
    >
      <div
        class="banner-bg py-5 px-6 d-flex align-center flex-wrap justify-space-between text-white"
      >
        <div class="d-flex align-center me-4 mb-2 mb-sm-0">
          <v-btn
            icon="mdi-arrow-right"
            variant="text"
            color="white"
            class="me-4"
            @click="goBack"
          ></v-btn>
          <div>
            <h1 class="text-h5 font-weight-black mb-1">لوحة إدارة الردود</h1>
            <p class="text-subtitle-2 text-blue-lighten-4 font-weight-medium">
              التعميم: {{ generalizationTitle }}
            </p>
          </div>
        </div>

        <!-- Stats Blocks Inside Banner -->
        <div class="d-flex align-center gap-4 flex-wrap mt-2 mt-sm-0">
          <!-- Total Replies Stat -->
          <div class="stat-badge d-flex align-center px-4 py-2 rounded-xl">
            <v-avatar color="rgba(255, 255, 255, 0.15)" class="me-3 rounded-lg" size="40">
              <v-icon icon="mdi-reply-all" color="white" size="20"></v-icon>
            </v-avatar>
            <div>
              <div class="text-caption text-blue-lighten-4 font-weight-medium">
                إجمالي الردود
              </div>
              <div class="text-h6 font-weight-black text-white leading-tight">
                {{ totalReplies }}
              </div>
            </div>
          </div>

          <!-- Unread Replies Stat -->
          <div class="stat-badge d-flex align-center px-4 py-2 rounded-xl">
            <v-avatar color="rgba(255, 255, 255, 0.15)" class="me-3 rounded-lg" size="40">
              <v-icon icon="mdi-email-mark-as-unread" color="white" size="20"></v-icon>
            </v-avatar>
            <div>
              <div class="text-caption text-blue-lighten-4 font-weight-medium">
                الجديدة
              </div>
              <div class="text-h6 font-weight-black text-white leading-tight">
                {{ unreadRepliesCount }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </v-card>

    <!-- Data Table -->
    <custom-data-table
      ref="dataTableRef"
      v-model="selectedIds"
      :headers="headers"
      :items="tableItems"
      :getData="fetchTableData"
      :customLoading="loadingTable"
      :create="false"
      :showTop="true"
      :actions="false"
      :hasFilter="false"
      :restore="false"
      :log="false"
      :canSelectDelete="false"
      :ExportToExcel="false"
      itemValue="id"
    >
      <template v-slot:header-actions>
        <v-menu
          v-model="filterMenu"
          :close-on-content-click="false"
          location="bottom end"
          transition="scale-transition"
        >
          <template v-slot:activator="{ props }">
            <v-badge color="error" dot :model-value="hasActiveFilters">
              <v-btn
                v-bind="props"
                variant="tonal"
                color="primary"
                class="rounded-lg shadow-sm"
                size="small"
                style="height: 38px; min-width: 38px"
              >
                <v-icon size="20">mdi-filter-variant</v-icon>
                <v-tooltip activator="parent" location="top">تصفية الردود</v-tooltip>
              </v-btn>
            </v-badge>
          </template>

          <v-card
            width="450"
            max-width="100%"
            class="pa-4 rounded-xl shadow-lg border overflow-hidden"
          >
            <h3 class="text-subtitle-1 font-weight-bold mb-4 d-flex align-center">
              <v-icon icon="mdi-filter-cog-outline" class="me-2 text-primary"></v-icon>
              تصفية الردود
            </h3>

            <div class="mb-3">
              <label
                class="text-caption font-weight-bold mb-1 d-block text-medium-emphasis"
                >نطاق التاريخ</label
              >
              <v-row dense>
                <v-col cols="12" sm="6">
                  <custom-text-field
                    v-model="filters.start_date"
                    type="date"
                    label="من"
                    hide-details
                  ></custom-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <custom-text-field
                    v-model="filters.end_date"
                    type="date"
                    label="إلى"
                    hide-details
                  ></custom-text-field>
                </v-col>
              </v-row>
            </div>

            <v-switch
              v-model="filters.has_attachment"
              label="يحتوي على مرفقات فقط"
              color="primary"
              density="compact"
              hide-details
              class="mb-1"
            ></v-switch>

            <v-select
              v-model="filters.is_read"
              :items="[
                { title: 'الكل', value: null },
                { title: 'مقروء', value: true },
                { title: 'غير مقروء', value: false },
              ]"
              item-title="title"
              item-value="value"
              label="حالة القراءة"
              density="compact"
              variant="outlined"
              hide-details
              class="mb-4 mt-2"
            ></v-select>

            <div class="d-flex gap-2 mt-2">
              <v-btn
                block
                color="primary"
                variant="flat"
                @click="applyFilters"
                class="flex-grow-1 font-weight-bold rounded-lg"
                >تطبيق</v-btn
              >
              <v-btn
                block
                color="grey-darken-1"
                variant="tonal"
                @click="clearFilters"
                class="flex-grow-1 font-weight-bold rounded-lg"
                >مسح الفلاتر</v-btn
              >
            </div>
          </v-card>
        </v-menu>
      </template>
      <template v-slot:item-slot="{ item, key }">
        <span
          v-if="key === 'replier_data'"
          class="cursor-pointer d-flex py-2"
          @click="openReply(item)"
        >
          <div class="d-flex align-center">
            <v-avatar color="primary" variant="tonal" size="36" class="me-3">
              <v-img
                v-if="item.replier_data?.profile_picture"
                :src="item.replier_data.profile_picture"
              ></v-img>
              <span v-else class="text-subtitle-2 text-primary font-weight-black">
                {{ item.replier_data?.first_name?.charAt(0) || "م" }}
              </span>
            </v-avatar>
            <div>
              <div
                class="text-body-2 font-weight-bold"
                :class="!item.is_read ? 'text-primary' : 'text-high-emphasis'"
              >
                {{ item.replier_data?.full_name || item.replier_data?.username }}
              </div>
              <div class="text-caption text-grey-darken-1">
                {{ item.replier_data?.organization_name || "جهة غير محددة" }}
              </div>
            </div>
          </div>
        </span>

        <span
          v-else-if="key === 'content'"
          class="cursor-pointer d-flex py-2"
          @click="openReply(item)"
        >
          <div
            class="text-truncate text-body-2"
            style="max-width: 300px"
            :class="
              !item.is_read ? 'text-primary font-weight-bold' : 'text-medium-emphasis'
            "
          >
            {{ item.content }}
          </div>
        </span>

        <span
          v-else-if="key === 'attachment'"
          class="cursor-pointer d-flex align-center justify-center py-2"
          @click="openReply(item)"
        >
          <span
            v-if="item.attachments_data && item.attachments_data.length > 0"
            class="meta-tag tag-attachments"
          >
            <v-icon icon="mdi-paperclip" size="14" class="me-1"></v-icon>
            <span>{{ item.attachments_data.length }} مرفقات</span>
          </span>
          <span v-else class="text-grey-lighten-1">-</span>
        </span>

        <span
          v-else-if="key === 'created_at'"
          class="cursor-pointer d-flex py-2"
          @click="openReply(item)"
        >
          <div
            class="text-body-2 font-weight-medium text-medium-emphasis"
            style="white-space: nowrap"
          >
            {{ formatDate(item.created_at) }}
          </div>
        </span>

        <span
          v-else-if="key === 'is_read'"
          class="cursor-pointer d-flex align-center justify-center py-2"
          @click="openReply(item)"
        >
          <span class="meta-tag" :class="item.is_read ? 'tag-replied' : 'tag-pending'">
            <v-icon
              :icon="item.is_read ? 'mdi-email-open-outline' : 'mdi-email-outline'"
              size="14"
              class="me-1"
            ></v-icon>
            <span>{{ item.is_read ? "مقروء" : "جديد" }}</span>
          </span>
        </span>

        <span
          v-else-if="key === 'actions'"
          class="cursor-pointer d-flex align-center justify-center py-2"
          @click="openReply(item)"
        >
          <v-btn
            icon="mdi-eye-outline"
            variant="text"
            size="small"
            color="primary"
          ></v-btn>
        </span>
      </template>
    </custom-data-table>

    <!-- Reply Viewer Dialog -->
    <custom-dialog v-model="showReplyDialog" title="تفاصيل الرد" width="600">
      <div v-if="selectedReply" class="d-flex flex-column gap-4 py-1">
        <div class="d-flex align-center pa-4 rounded-xl border-thin bg-surface">
          <v-avatar color="primary" size="48" class="me-4 shadow-sm border-avatar">
            <v-img
              v-if="selectedReply.replier_data?.profile_picture"
              :src="selectedReply.replier_data.profile_picture"
            ></v-img>
            <span v-else class="text-h6 text-white font-weight-black">
              {{ selectedReply.replier_data?.first_name?.charAt(0) || "م" }}
            </span>
          </v-avatar>
          <div class="flex-grow-1">
            <h3 class="text-subtitle-1 font-weight-black color-text-primary mb-1">
              {{
                selectedReply.replier_data?.full_name ||
                selectedReply.replier_data?.username
              }}
            </h3>
            <div class="text-caption text-medium-emphasis d-flex align-center">
              <v-icon
                icon="mdi-office-building-outline"
                size="14"
                class="me-1"
                color="primary"
              ></v-icon>
              {{ selectedReply.replier_data?.organization_name || "جهة غير محددة" }}
            </div>
          </div>
          <div class="text-caption text-medium-emphasis text-right me-1">
            <div class="font-weight-bold">{{ formatDate(selectedReply.created_at) }}</div>
          </div>
        </div>

        <div>
          <h4 class="text-subtitle-2 font-weight-bold text-primary mb-2">محتوى الرد:</h4>
          <v-card
            variant="flat"
            class="pa-5 bg-surface rounded-xl border-thin content-card font-weight-medium"
          >
            <p class="text-body-1 color-text-primary text-pre-line leading-relaxed">
              {{ selectedReply.content }}
            </p>
          </v-card>
        </div>

        <!-- Reply Attachments -->
        <div
          v-if="
            selectedReply.attachments_data && selectedReply.attachments_data.length > 0
          "
        >
          <h4
            class="text-subtitle-2 font-weight-bold text-primary mb-3 d-flex align-center"
          >
            <v-icon icon="mdi-paperclip" size="20" class="me-2"></v-icon>
            المرفقات ({{ selectedReply.attachments_data.length }})
          </h4>
          <div class="d-flex flex-column gap-2">
            <v-card
              v-for="(attachment, index) in selectedReply.attachments_data"
              :key="attachment.id"
              variant="flat"
              class="pa-3 rounded-lg d-flex align-center border-thin hover-card bg-surface cursor-pointer"
              @click="previewAttachment(attachment)"
            >
              <div class="d-flex align-center flex-grow-1 overflow-hidden">
                <v-avatar color="primary-lighten-5" rounded="lg" size="44" class="me-3">
                  <v-icon
                    icon="mdi-file-pdf-box"
                    color="error"
                    size="24"
                    v-if="attachment.file_url?.toLowerCase().endsWith('.pdf')"
                  ></v-icon>
                  <v-icon
                    icon="mdi-file-document-outline"
                    color="primary"
                    size="24"
                    v-else
                  ></v-icon>
                </v-avatar>
                <div class="text-truncate">
                  <div
                    class="text-subtitle-2 font-weight-bold color-text-primary text-truncate"
                  >
                    ملف مرفق رقم {{ index + 1 }}
                  </div>
                  <div class="text-caption text-medium-emphasis">اضغط للمعاينـة</div>
                </div>
              </div>
              <v-btn
                color="primary"
                variant="tonal"
                size="small"
                class="rounded-lg px-3 ms-2"
                @click.stop="previewAttachment(attachment)"
              >
                <v-icon icon="mdi-eye" size="18" class="me-1"></v-icon>
                معاينة
              </v-btn>
            </v-card>
          </div>
        </div>
      </div>

      <template #actions>
        <v-spacer></v-spacer>
        <v-btn
          variant="text"
          color="grey-darken-1"
          @click="showReplyDialog = false"
          class="rounded-pill px-6 font-weight-bold text-body-2"
        >
          إغلاق
        </v-btn>
      </template>
    </custom-dialog>
    <!-- Attachment Preview Dialog -->
    <AttachmentPreviewDialog
      v-model="showPreviewDialog"
      :file-url="previewFileUrl"
      :file-name="previewFileName"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import { getRouter } from "../../../src/router/routerInstance";
import { useGeneralizationStore } from "../../store/generalizationStore";
import api from "../../../plugins/axios-plugin";
import AttachmentPreviewDialog from "../../components/AttachmentPreviewDialog.vue";

const route = useRoute();
const router = getRouter;
const genStore = useGeneralizationStore();

const generalization = route.params;
const generalizationId = window.location.pathname.split("/")[3] ?? 0;

const generalizationTitle = ref("جاري التحميل...");

const loadingTable = ref(false);
const tableItems = ref({
  results: [],
  pagination: { count: 0, current_page: 1, num_pages: 1 },
});
const selectedIds = ref([]);
const totalReplies = ref(0);
const unreadRepliesCount = ref(0);
const dataTableRef = ref(null);

const showReplyDialog = ref(false);
const selectedReply = ref(null);

const filters = ref({
  has_attachment: false,
  start_date: null,
  end_date: null,
  is_read: null,
});

const filterMenu = ref(false);

// Preview Dialog State
const showPreviewDialog = ref(false);
const previewFileUrl = ref("");
const previewFileName = ref("");

const previewAttachment = (attachment) => {
  previewFileUrl.value = attachment.file_url;
  const parts = attachment.file_url.split("/");
  previewFileName.value = attachment.name || parts[parts.length - 1];
  showPreviewDialog.value = true;
};

const hasActiveFilters = computed(() => {
  return (
    filters.value.has_attachment ||
    filters.value.start_date ||
    filters.value.end_date ||
    filters.value.is_read !== null
  );
});

const applyFilters = () => {
  filterMenu.value = false;
  if (dataTableRef.value && dataTableRef.value.params) {
    dataTableRef.value.params.page = 1;
  }
  fetchTableData();
};

const clearFilters = () => {
  filters.value = {
    has_attachment: false,
    start_date: null,
    end_date: null,
    is_read: null,
  };
  applyFilters();
};

const headers = [
  { title: "المرسل (الجهة)", key: "replier_data", sortable: false },
  { title: "نص الرد", key: "content", sortable: false },
  { title: "المرفق", key: "attachment", sortable: false, align: "center" },
  { title: "التاريخ", key: "created_at", sortable: false },
  { title: "الحالة", key: "is_read", sortable: false, align: "center" },
  { title: "الإجراءات", key: "actions", sortable: false, align: "center" },
];

const fetchTableData = async (incomingParams) => {
  const tableParams =
    incomingParams && incomingParams.params
      ? incomingParams.params
      : dataTableRef.value?.params || { page: 1, page_size: 10 };
  loadingTable.value = true;
  try {
    const apiParams = {
      page: tableParams.page,
      page_size: tableParams.page_size,
      search: tableParams.search || undefined,
      has_attachment: filters.value.has_attachment ? "true" : undefined,
      start_date: filters.value.start_date || undefined,
      end_date: filters.value.end_date || undefined,
    };

    if (filters.value.is_read !== null && filters.value.is_read !== undefined) {
      apiParams.is_read = filters.value.is_read ? "true" : "false";
    }

    const data = await genStore.fetchReplies(generalizationId, apiParams);

    // Support CustomPageNumberPagination structure
    const hasPaginationObj = data && data.pagination;
    const count = hasPaginationObj
      ? data.pagination.count
      : data?.count ?? (data?.results || data || []).length;
    const numPages = hasPaginationObj
      ? data.pagination.num_pages
      : data?.num_pages || Math.ceil(count / tableParams.page_size) || 1;

    tableItems.value = {
      results: data?.results !== undefined ? data.results : data || [],
      pagination: {
        count: count,
        current_page: tableParams.page,
        num_pages: numPages,
      },
    };

    totalReplies.value = tableItems.value.pagination.count;
    return tableItems.value;
  } catch (error) {
    console.error("Failed to load replies:", error);
    return { results: [], pagination: { count: 0, current_page: 1, num_pages: 1 } };
  } finally {
    loadingTable.value = false;
  }
};

const openReply = async (reply) => {
  selectedReply.value = reply;
  showReplyDialog.value = true;

  if (!reply.is_read) {
    try {
      await genStore.markReplyAsRead(generalizationId, reply.id);
      reply.is_read = true; // Update UI locally
      if (unreadRepliesCount.value > 0) {
        unreadRepliesCount.value--;
      }
    } catch (error) {
      console.error("Failed to mark reply as read:", error);
    }
  }
};

const goBack = () => {
  router.push("/generalizations-view"); // Or whatever the dashboard route is
};

const formatDate = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  return (
    date.toLocaleDateString("ar-EG", {
      year: "numeric",
      month: "short",
      day: "numeric",
    }) +
    " " +
    date.toLocaleTimeString("ar-EG", { hour: "2-digit", minute: "2-digit" })
  );
};

const downloadFile = (url) => {
  if (!url) return;
  window.open(url, "_blank");
};

const fetchGeneralizationDetails = async () => {
  try {
    const response = await api.get(`/chat/generalizations/${generalizationId}/`);
    generalizationTitle.value = response.data.title;
    unreadRepliesCount.value = response.data.unread_replies_count || 0;
  } catch (error) {
    console.error("Failed to load generalization details:", error);
    generalizationTitle.value = "تعميم غير معروف";
  }
};

onMounted(() => {
  fetchGeneralizationDetails();
});
</script>

<style scoped>
.generalization-replies-screen {
  font-family: "Inter", "Roboto", "Outfit", sans-serif !important;
  height: calc(100vh - 85px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.bg-background {
  background-color: rgb(var(--v-theme-background)) !important;
}

.theme-surface-light {
  background-color: rgba(var(--v-theme-on-surface), 0.05) !important;
}

.theme-primary-light {
  background-color: rgba(var(--v-theme-primary), 0.1) !important;
}

.banner-bg {
  background: rgb(var(--v-theme-primary));
  background-image: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.12) 0%,
    rgba(0, 0, 0, 0.18) 100%
  );
  position: relative;
  overflow: hidden;
}

.stat-badge {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  min-width: 140px;
}

.unread-row {
  background-color: rgba(var(--v-theme-primary), 0.03) !important;
  box-shadow: inset 3px 0 0 rgb(var(--v-theme-primary));
}

.replies-table :deep(th) {
  background-color: rgba(var(--v-theme-surface), 1) !important;
  font-weight: 700 !important;
  color: rgba(var(--v-theme-on-surface), 0.7) !important;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
  border-bottom: 2px solid rgba(var(--v-border-color), 0.1) !important;
}

.text-pre-line {
  white-space: pre-line;
}

.border-primary-light {
  border-color: rgba(var(--v-theme-primary), 0.2) !important;
}

.bg-primary-lighten-5 {
  background-color: rgba(var(--v-theme-primary), 0.08) !important;
}

.file-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hover-card {
  cursor: pointer;
  border: 1px solid rgba(var(--v-border-color), 0.12);
}
.hover-card:hover {
  background-color: rgba(var(--v-theme-primary), 0.02);
  border-color: rgba(var(--v-theme-primary), 0.3);
}

.transition-all-2 {
  transition: all 0.2s ease;
}

/* Metadata tag styling */
.meta-tag {
  display: inline-flex;
  align-items: center;
  padding: 2px 10px;
  border-radius: 6px;
  font-size: 0.725rem;
  font-weight: 700;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.tag-attachments {
  background: rgba(var(--v-theme-on-surface), 0.04);
  color: rgba(var(--v-theme-on-surface), 0.7);
  border-color: rgba(var(--v-theme-on-surface), 0.08);
}

.tag-replied {
  background: rgba(var(--v-theme-success), 0.08);
  color: rgb(var(--v-theme-success));
  border-color: rgba(var(--v-theme-success), 0.15);
}

.tag-pending {
  background: rgba(var(--v-theme-error), 0.08);
  color: rgb(var(--v-theme-error));
  border-color: rgba(var(--v-theme-error), 0.15);
  animation: border-pulse 2s infinite;
}

@keyframes border-pulse {
  0% {
    border-color: rgba(var(--v-theme-error), 0.15);
  }
  50% {
    border-color: rgba(var(--v-theme-error), 0.4);
  }
  100% {
    border-color: rgba(var(--v-theme-error), 0.15);
  }
}

.border-avatar {
  border: 1px solid rgb(var(--v-theme-primary));
}

.color-text-primary {
  color: rgb(var(--v-theme-on-surface));
}

.content-card {
  box-shadow: 0 8px 20px -6px rgba(0, 0, 0, 0.04) !important;
  border-inline-start: 3.5px solid rgb(var(--v-theme-primary)) !important;
}

.leading-relaxed {
  line-height: 1.8;
  font-size: 1.05rem;
}

.gap-4 {
  gap: 16px;
}
</style>
