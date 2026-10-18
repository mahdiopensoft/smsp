<template>
  <div class="generalizations-screen pa-6 bg-background">

    <!-- Tab Filters & Toolbar -->
    <v-card class="flex-shrink-0 rounded-xl px-4 py-2 mb-6 border-0 shadow-sm bg-surface d-flex align-center flex-wrap"
      elevation="1">
      <v-tabs v-model="activeTab" color="primary" align-tabs="start" line-thickness="3" class="custom-tabs flex-grow-1">
        <v-tab value="inbox" class="font-weight-bold py-3 text-body-2">
          <v-icon start icon="mdi-inbox-arrow-down" class="me-1"></v-icon>
          الواردة
          <v-chip size="x-small" color="primary" class="ms-2 font-weight-bold" v-if="genStore.inboxCount > 0">{{
            genStore.inboxCount }}</v-chip>
        </v-tab>
        <v-tab value="unread" class="font-weight-bold py-3 text-body-2">
          <v-icon start icon="mdi-bell-badge-outline" class="me-1"></v-icon>
          غير المقروءة
          <v-chip size="x-small" color="error" class="ms-2 font-weight-bold" v-if="genStore.unreadCount > 0">{{
            genStore.unreadCount }}</v-chip>
        </v-tab>
        <v-tab value="starred" class="font-weight-bold py-3 text-body-2">
          <v-icon start icon="mdi-star" class="me-1 text-warning"></v-icon>
          المميزة بنجمة
        </v-tab>
        <v-tab value="sent" class="font-weight-bold py-3 text-body-2">
          <v-icon start icon="mdi-send-circle-outline" class="me-1"></v-icon>
          الصادرة
          <v-chip size="x-small" color="grey-darken-1" class="ms-2 font-weight-bold" v-if="genStore.sentCount > 0">{{
            genStore.sentCount }}</v-chip>
        </v-tab>
      </v-tabs>


    </v-card>

    <!-- Bulk Actions Toolbar -->
    <v-slide-y-transition>
      <div v-if="selectedIds.length > 0" class="d-flex justify-center mb-4">
        <v-card 
          class="rounded-pill bg-surface border px-4 py-2 d-flex align-center shadow-sm" 
          elevation="3">
          <span class="text-subtitle-2 font-weight-bold text-primary d-flex align-center me-4">
            <v-avatar color="primary" size="28" class="text-white me-2 font-weight-bold" style="font-size: 13px;">{{ selectedIds.length }}</v-avatar>
            عنصر محدد
          </span>
          
          <v-divider vertical class="mx-3" style="height: 24px; align-self: center;"></v-divider>
          
          <v-btn v-if="activeTab !== 'sent'" prepend-icon="mdi-email-open-outline" variant="text" color="primary"
            @click="bulkMarkRead" class="font-weight-bold me-2 rounded-pill" size="small">
            تعيين كمقروء
          </v-btn>

          <v-btn v-if="activeTab === 'sent'" prepend-icon="mdi-delete-outline" variant="tonal" color="error"
            @click="bulkDelete" class="font-weight-bold rounded-pill px-4" size="small">
            حذف المحدد
          </v-btn>
        </v-card>
      </div>
    </v-slide-y-transition>

    <!-- Custom Data Table -->
    <custom-data-table ref="dataTableRef" v-model="selectedIds" :headers="headers" :items="tableItems"
      :getData="fetchTableData" :customLoading="loadingTable" :create="false" :showTop="true" :actions="false"
      :hasFilter="false" :restore="false" :log="false" :canSelectDelete="false" :ExportToExcel="false" itemValue="id">
      <template v-slot:header-actions>
        <v-btn color="primary" variant="elevated" prepend-icon="mdi-plus" @click="showCreateDialog = true"
          class="me-2 rounded-lg font-weight-bold" size="small" style="height: 38px;" elevation="2">
          إنشاء تعميم
        </v-btn>

        <v-menu v-model="filterMenu" :close-on-content-click="false" location="bottom end"
          transition="scale-transition">
          <template v-slot:activator="{ props }">
            <v-badge color="error" dot :model-value="hasActiveFilters">
              <v-btn v-bind="props" variant="tonal" color="primary" class="rounded-lg shadow-sm" size="small"
                style="height: 38px; min-width: 38px;">
                <v-icon size="20">mdi-filter-variant</v-icon>
                <v-tooltip activator="parent" location="top">تصفية متقدمة</v-tooltip>
              </v-btn>
            </v-badge>
          </template>

          <v-card width="450" max-width="100%" class="pa-4 rounded-xl shadow-lg border overflow-hidden">
            <h3 class="text-subtitle-1 font-weight-bold mb-4 d-flex align-center">
              <v-icon icon="mdi-filter-cog-outline" class="me-2 text-primary"></v-icon>
              تصفية متقدمة
            </h3>

            <div class="mb-3">
              <label class="text-caption font-weight-bold mb-1 d-block text-medium-emphasis">نطاق التاريخ</label>
              <v-row dense>
                <v-col cols="12" sm="6">
                  <custom-text-field v-model="filters.start_date" type="date" label="من"
                    hide-details></custom-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <custom-text-field v-model="filters.end_date" type="date" label="إلى"
                    hide-details></custom-text-field>
                </v-col>
              </v-row>
            </div>

            <auto-list v-model="filters.target_company_levels" name="CompanyLevelFilterChoices"
              :param="companyLevelParam" item-title="name" item-value="id" label="المستويات الإدارية المستهدفة" multiple
              class="mb-3"></auto-list>

            <auto-list v-model="filters.target_user_types" name="UserType" label="فئات المستخدمين المستهدفة"
              item-title="name_ar" item-value="id" multiple class="mb-3"></auto-list>

            <v-switch v-model="filters.has_attachment" label="يحتوي على مرفقات فقط" color="primary" density="compact"
              hide-details class="mb-1"></v-switch>
            <v-switch v-model="filters.requires_reply" label="يتطلب الرد فقط" color="primary" density="compact"
              hide-details class="mb-4"></v-switch>

            <div class="d-flex gap-2 mt-2">
              <v-btn block color="primary" variant="flat" @click="applyFilters"
                class="flex-grow-1 font-weight-bold rounded-lg">تطبيق</v-btn>
              <v-btn block color="grey-darken-1" variant="tonal" @click="clearFilters"
                class="flex-grow-1 font-weight-bold rounded-lg">مسح الفلاتر</v-btn>
            </div>
          </v-card>
        </v-menu>
      </template>

      <template v-slot:item-slot="{ item, key }">
        <!-- Star Toggle -->
        <span v-if="key === 'star'" @click.stop="toggleStar(item)">
          <v-icon :icon="item.is_starred ? 'mdi-star' : 'mdi-star-outline'"
            :color="item.is_starred ? 'warning' : 'grey-lighten-1'" size="22"
            class="transition-all-2 hover-scale"></v-icon>
        </span>

        <!-- Sender -->
        <span v-else-if="key === 'sender'">
          <div class="d-flex align-center py-2">
            <v-avatar color="primary" variant="tonal" size="32" class="me-3">
              <v-img v-if="item.sender_data?.profile_picture" :src="item.sender_data.profile_picture"></v-img>
              <span v-else class="text-caption font-weight-bold text-primary">{{ item.sender_data?.first_name?.charAt(0)
                || 'م' }}</span>
            </v-avatar>
            <span class="font-weight-medium" :class="{ 'text-primary font-weight-bold': !item.is_read }">
              {{ item.sender_data?.full_name || 'المرسل' }}
            </span>
          </div>
        </span>

        <!-- Title -->
        <span v-else-if="key === 'title'">
          <div class="d-flex flex-column gap-1 py-1">
            <!-- First line: Title + Unread/New badge -->
            <div class="d-flex align-center flex-wrap">
              <span class="text-subtitle-2 font-weight-bold"
                :class="{ 'text-primary font-weight-black': !item.is_read }">{{ item.title }}</span>
              <v-chip v-if="!item.is_read" color="error" size="x-small" variant="flat"
                class="ms-2 font-weight-bold px-2 rounded-pill">جديد</v-chip>
            </div>

            <!-- Second line: Metadata row -->
            <div class="d-flex align-center flex-wrap gap-2 mt-1 metadata-row">
              <!-- Attachments Badge -->
              <span v-if="item.attachments_data?.length > 0" class="meta-tag tag-attachments"
                v-tooltip="'مرفقات إدارية'">
                <v-icon icon="mdi-paperclip" size="14" class="me-1"></v-icon>
                <span>{{ item.attachments_data.length }} مرفقات</span>
              </span>

              <!-- Status for the RECIPIENT -->
              <span v-if="item.allow_replies && authStore.user?.id !== item.sender_data?.id" class="meta-tag"
                :class="item.has_replied ? 'tag-replied' : 'tag-pending'">
                <v-icon :icon="item.has_replied ? 'mdi-check-all' : 'mdi-clock-outline'" size="14"
                  class="me-1"></v-icon>
                <span>{{ item.has_replied ? 'تم الرد' : 'يتطلب رد عاجل' }}</span>
              </span>

              <!-- Status for the SENDER (Creator) -->
              <span v-if="authStore.user?.id === item.sender_data?.id && item.allow_replies"
                class="meta-tag tag-sender-replies">
                <v-icon icon="mdi-message-reply-text-outline" size="14" class="me-1"></v-icon>
                <span>{{ item.replies_count || 0 }} ردود</span>
              </span>

              <span v-if="authStore.user?.id === item.sender_data?.id && item.unread_replies_count > 0"
                class="meta-tag tag-unread-replies">
                <v-icon icon="mdi-bell-ring-outline" size="14" class="me-1"></v-icon>
                <span>{{ item.unread_replies_count }} جديدة</span>
              </span>
            </div>
          </div>
        </span>

        <!-- Date -->
        <span v-else-if="key === 'created_at'" class="text-body-2 font-weight-medium text-medium-emphasis"
          style="white-space: nowrap;">
          {{ formatShortDate(item.created_at) }}
        </span>

        <!-- Actions -->
        <span v-else-if="key === 'actions'">
          <custom-btn label="عرض التفاصيل" icon="eye-outline" isIcon class="text-primary"
            @click="openGeneralization(item)" />
        </span>
      </template>
    </custom-data-table>

    <!-- Dialogs -->
    <GeneralizationViewDialog v-model="showViewDialog" :generalization="selectedGeneralization" />
    <GeneralizationCreateDialog v-model="showCreateDialog" />
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue';
import { useGeneralizationStore } from "../../store/generalizationStore";
import { useAuthStore } from "../../../src/UserManagement/stores/auth";
import GeneralizationViewDialog from "./GeneralizationViewDialog.vue";
import GeneralizationCreateDialog from "./GeneralizationCreateDialog.vue";
import api from "../../../plugins/axios-plugin";

const genStore = useGeneralizationStore();
const authStore = useAuthStore();

const showCreateDialog = ref(false);
const showViewDialog = ref(false);
const selectedGeneralization = ref(null);

const activeTab = ref('inbox');
const dataTableRef = ref(null);

const tableItems = ref({ results: [], pagination: { count: 0, current_page: 1, num_pages: 1 } });
const loadingTable = ref(false);

const headers = ref([
  { title: "", key: "star", sortable: false, width: "50px" },
  { title: "المرسل", key: "sender", sortable: false },
  { title: "الموضوع", key: "title", sortable: false },
  { title: "التاريخ", key: "created_at", sortable: false },
  { title: "الإجراءات", key: "actions", sortable: false }
]);

const selectedIds = ref([]);

const filters = ref({
  has_attachment: false,
  requires_reply: false,
  start_date: null,
  end_date: null,
  target_company_levels: [],
  target_user_types: []
});

const filterMenu = ref(false);

const companyLevelParam = computed(() => ({
  company_level: authStore.user?.profile?.company_level || authStore.user?.company_level || 1,
  isEdit: true
}));

const hasActiveFilters = computed(() => {
  return filters.value.has_attachment ||
    filters.value.requires_reply ||
    filters.value.start_date ||
    filters.value.end_date ||
    filters.value.target_company_levels.length > 0 ||
    filters.value.target_user_types.length > 0;
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
    requires_reply: false,
    start_date: null,
    end_date: null,
    target_company_levels: [],
    target_user_types: []
  };
  applyFilters();
};

const fetchTableData = async (incomingParams) => {
  const params = (incomingParams && incomingParams.params) 
                 ? incomingParams.params 
                 : (dataTableRef.value?.params || { page: 1, page_size: 10 });
                 
  loadingTable.value = true;
  
  try {
    await genStore.fetchCounts();
    
    const apiParams = {
        page: params.page,
        page_size: params.page_size,
        search: params.search || undefined,
        has_attachment: filters.value.has_attachment ? 'true' : undefined,
        requires_reply: filters.value.requires_reply ? 'true' : undefined,
        start_date: filters.value.start_date || undefined,
        end_date: filters.value.end_date || undefined,
    };

    if (filters.value.target_company_levels.length > 0) {
      apiParams.target_company_levels = filters.value.target_company_levels.join(',');
    }
    
    if (filters.value.target_user_types.length > 0) {
      apiParams.target_user_types = filters.value.target_user_types.join(',');
    }

    const res = await api.get(`/chat/generalizations/?filter=${activeTab.value}`, {
      params: apiParams
    });
    
    // Check if the backend returns the CustomPageNumberPagination structure
    const hasPaginationObj = res.data && res.data.pagination;
    const count = hasPaginationObj ? res.data.pagination.count : (res.data.count || (Array.isArray(res.data) ? res.data.length : 0));
    const numPages = hasPaginationObj ? res.data.pagination.num_pages : (res.data.num_pages || Math.ceil(count / params.page_size) || 1);
    
    tableItems.value = {
      results: res.data.results || (Array.isArray(res.data) ? res.data : []),
      pagination: {
        count: count,
        num_pages: numPages,
        current_page: params.page
      }
    };
  } catch (error) {
    console.error("Error fetching generalizations:", error);
  } finally {
    loadingTable.value = false;
  }
};

watch(activeTab, () => {
  selectedIds.value = [];
  if (dataTableRef.value && dataTableRef.value.params) {
    dataTableRef.value.params.page = 1;
  }
  clearFilters();
});

const refreshData = () => {
  fetchTableData();
};

const formatShortDate = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  const now = new Date();
  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString('ar-EG', { hour: '2-digit', minute: '2-digit' });
  }
  return date.toLocaleDateString('ar-EG', { day: 'numeric', month: 'short' });
};

const openGeneralization = (gen) => {
  selectedGeneralization.value = gen;
  showViewDialog.value = true;
  
  const isSender = gen.sender_data?.id === authStore.user?.id || gen.sender_data?.username === authStore.user?.username;
  
  if (!isSender && !gen.is_read) {
    genStore.markAsRead(gen.id).then(() => {
      fetchTableData();
    });
  } else if (isSender && gen.unread_replies_count > 0) {
    genStore.markAsRead(gen.id).then(() => {
      fetchTableData();
    });
  }
};

const toggleStar = async (item) => {
  try {
    await genStore.toggleStar(item.id);
    fetchTableData();
  } catch (err) {
    console.error(err);
  }
};

const bulkMarkRead = async () => {
  try {
    await genStore.bulkMarkAsRead(selectedIds.value);
    selectedIds.value = [];
    fetchTableData();
  } catch (e) {
    console.error(e);
  }
};

const bulkDelete = async () => {
  try {
    await genStore.bulkDelete(selectedIds.value);
    selectedIds.value = [];
    fetchTableData();
  } catch (e) {
    console.error(e);
  }
};

onMounted(async () => {
  if (!authStore.user) {
    try {
      await authStore.fetchProfile();
    } catch (e) {
      console.error("Error fetching user profile:", e);
    }
  }
});
</script>

<style scoped>
.generalizations-screen {
  height: calc(100vh - 85px);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.banner-bg {
  background: rgb(var(--v-theme-primary));
  background-image: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(0, 0, 0, 0.18) 100%);
  position: relative;
  overflow: hidden;
}

.banner-bg::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -20%;
  width: 70%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0) 60%);
  transform: rotate(-30deg);
  pointer-events: none;
}

.banner-icon-wrapper {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.create-generalization-btn {
  text-transform: none;
  font-family: inherit;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.create-generalization-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15) !important;
}

.custom-tabs :deep(.v-btn) {
  text-transform: none !important;
  letter-spacing: 0px !important;
}

.transition-all-2 {
  transition: all 0.2s ease;
}

.hover-scale {
  cursor: pointer;
}

.hover-scale:hover {
  transform: scale(1.15);
}

.bg-primary-lighten-5 {
  background-color: rgba(var(--v-theme-primary), 0.08) !important;
}

.border-primary-light {
  border: 1px solid rgba(var(--v-theme-primary), 0.2) !important;
}

@keyframes float {
  0% {
    transform: translateY(0px) rotate(0deg);
  }

  50% {
    transform: translateY(-4px) rotate(-5deg);
  }

  100% {
    transform: translateY(0px) rotate(0deg);
  }
}

.pulse-icon {
  animation: float 4s ease-in-out infinite;
}

/* Metadata tag styling */
.metadata-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

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

/* Attachments */
.tag-attachments {
  background: rgba(var(--v-theme-on-surface), 0.04);
  color: rgba(var(--v-theme-on-surface), 0.7);
  border-color: rgba(var(--v-theme-on-surface), 0.08);
}

/* Replied (Success) */
.tag-replied {
  background: rgba(var(--v-theme-success), 0.08);
  color: rgb(var(--v-theme-success));
  border-color: rgba(var(--v-theme-success), 0.15);
}

/* Pending Reply (Warning/Alert) */
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

/* Sender stats (Info) */
.tag-sender-replies {
  background: rgba(var(--v-theme-primary), 0.08);
  color: rgb(var(--v-theme-primary));
  border-color: rgba(var(--v-theme-primary), 0.15);
}

.tag-unread-replies {
  background: rgba(var(--v-theme-warning), 0.08);
  color: rgb(var(--v-theme-warning));
  border-color: rgba(var(--v-theme-warning), 0.15);
}
</style>
