<template>
  <div class="notifications-screen pa-6 bg-background">
    <!-- Header Banner -->
    <v-card
      class="flex-shrink-0 rounded-xl overflow-hidden mb-6 border-0 shadow-lg position-relative"
      elevation="4"
    >
      <div
        class="banner-bg py-8 px-6 d-flex align-center flex-wrap justify-space-between text-white"
      >
        <div class="d-flex align-center me-4 mb-2 mb-sm-0">
          <div class="banner-icon-wrapper me-4">
            <v-icon icon="mdi-bell-ring" size="32" class="text-white pulse-icon"></v-icon>
          </div>
          <div>
            <h1 class="text-h4 font-weight-black mb-1">مركز الإشعارات</h1>
            <p class="text-subtitle-2 text-blue-lighten-4 font-weight-medium">
              تابع كل جديد، تنبيهات، وإعلانات النظام من مكان واحد
            </p>
          </div>
        </div>

        <v-btn
          v-if="unreadCount > 0"
          color="white"
          variant="elevated"
          prepend-icon="mdi-check-all"
          @click="markAllAsRead"
          :loading="loadingAll"
          class="create-generalization-btn px-6 text-primary rounded-lg font-weight-bold"
          elevation="3"
        >
          تحديد الكل كمقروء
        </v-btn>
      </div>
    </v-card>

    <!-- Tab Filters & Search Card -->
    <v-card
      class="flex-shrink-0 rounded-xl px-4 py-2 mb-6 border-0 shadow-sm bg-surface"
      elevation="1"
    >
      <div
        class="d-flex flex-column flex-sm-row align-stretch align-sm-center justify-space-between gap-4"
      >
        <v-tabs
          v-model="activeFilter"
          color="primary"
          align-tabs="start"
          line-thickness="3"
          class="custom-tabs"
        >
          <v-tab value="all" class="font-weight-bold py-3 text-body-2">
            <v-icon start icon="mdi-all-inclusive" class="me-1"></v-icon>
            الكل
            <v-chip
              size="x-small"
              color="primary"
              class="ms-2 font-weight-bold"
              v-if="allCount > 0"
              >{{ allCount }}</v-chip
            >
          </v-tab>
          <v-tab value="unread" class="font-weight-bold py-3 text-body-2">
            <v-icon start icon="mdi-bell-badge-outline" class="me-1"></v-icon>
            غير مقروءة
            <v-chip
              size="x-small"
              color="error"
              class="ms-2 font-weight-bold"
              v-if="unreadCount > 0"
              >{{ unreadCount }}</v-chip
            >
          </v-tab>
          <v-tab value="read" class="font-weight-bold py-3 text-body-2">
            <v-icon start icon="mdi-bell-check-outline" class="me-1"></v-icon>
            مقروءة
            <v-chip
              size="x-small"
              color="success"
              class="ms-2 font-weight-bold"
              v-if="readCount > 0"
              >{{ readCount }}</v-chip
            >
          </v-tab>
          <v-tab value="alert" class="font-weight-bold py-3 text-body-2">
            <v-icon start icon="mdi-alert-circle-outline" class="me-1"></v-icon>
            تنبيهات
            <v-chip
              size="x-small"
              color="warning"
              class="ms-2 font-weight-bold"
              v-if="alertCount > 0"
              >{{ alertCount }}</v-chip
            >
          </v-tab>
          <v-tab value="news" class="font-weight-bold py-3 text-body-2">
            <v-icon start icon="mdi-newspaper-variant-outline" class="me-1"></v-icon>
            أخبار
            <v-chip
              size="x-small"
              color="info"
              class="ms-2 font-weight-bold"
              v-if="newsCount > 0"
              >{{ newsCount }}</v-chip
            >
          </v-tab>
        </v-tabs>
      </div>
    </v-card>

    <!-- Scrollable container for notifications list -->
    <div class="scroll-container flex-grow-1 px-1">
      <!-- Notifications List Container -->
      <custom-data-table
        v-if="searchedNotifications.length > 0"
        ref="dataTableRef"
        :headers="headers"
        :items="tableItems"
        :getData="fetchTableData"
        :customLoading="loadingTable"
        :create="false"
        :showTop="true"
        :actions="true"
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
                  <v-tooltip activator="parent" location="top">تصفية متقدمة</v-tooltip>
                </v-btn>
              </v-badge>
            </template>

            <v-card
              width="350"
              max-width="100%"
              class="pa-4 rounded-xl shadow-lg border overflow-hidden"
            >
              <h3 class="text-subtitle-1 font-weight-bold mb-4 d-flex align-center">
                <v-icon icon="mdi-filter-cog-outline" class="me-2 text-primary"></v-icon>
                تصفية متقدمة
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

              <div class="d-flex gap-2 mt-4">
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
            v-if="key === 'title'"
            class="cursor-pointer d-flex py-2"
            @click="handleNotificationClick(item)"
          >
            <div class="d-flex align-center">
              <v-avatar
                :color="getIconColor(item)"
                variant="tonal"
                size="40"
                class="me-3"
              >
                <v-icon size="20">{{ getIcon(item) }}</v-icon>
              </v-avatar>
              <div>
                <div
                  class="text-body-2 font-weight-bold d-flex align-center"
                  :class="!item.is_read ? 'text-primary' : 'text-high-emphasis'"
                >
                  {{ item.title }}
                  <span v-if="!item.is_read" class="unread-pulse-dot ms-2"></span>
                </div>
                <v-chip
                  v-if="item.module_name"
                  size="x-small"
                  variant="tonal"
                  color="secondary"
                  class="font-weight-medium px-2 py-0 mt-1 rounded-lg"
                >
                  <v-icon size="12" class="me-1">mdi-domain</v-icon>
                  {{ item.module_name }}
                </v-chip>
              </div>
            </div>
          </span>

          <span
            v-else-if="key === 'message'"
            class="cursor-pointer d-flex py-2"
            @click="handleNotificationClick(item)"
          >
            <div
              class="text-truncate text-body-2"
              style="max-width: 400px"
              :class="
                !item.is_read
                  ? 'text-grey-darken-4 font-weight-bold'
                  : 'text-grey-darken-1'
              "
            >
              {{ item.message }}
            </div>
          </span>

          <span
            v-else-if="key === 'created_at'"
            class="cursor-pointer d-flex align-center justify-center py-2"
            @click="handleNotificationClick(item)"
          >
            <div
              class="text-caption text-medium-emphasis text-center"
              style="white-space: nowrap"
            >
              {{ formatDate(item.created_at) }}
            </div>
          </span>
        </template>
      </custom-data-table>

      <!-- Custom Stylized Empty State -->
      <v-card
        v-else
        class="text-center pa-12 rounded-xl elevation-4 glass-card empty-state-card mt-6"
      >
        <div class="empty-state-icon-wrapper mb-6 mx-auto position-relative">
          <div class="pulse-ring ring-1"></div>
          <div class="pulse-ring ring-2"></div>
          <v-avatar
            color="primary"
            variant="tonal"
            size="110"
            class="elevation-3 inner-avatar"
          >
            <v-icon size="54" color="primary">mdi-bell-off-outline</v-icon>
          </v-avatar>
        </div>

        <h2 class="text-h4 font-weight-black text-grey-darken-3 mb-2">لا توجد إشعارات</h2>
        <p class="text-h6 text-grey-darken-1 mb-8 max-width-text mx-auto">
          {{
            searchQuery
              ? "لم نجد أي إشعارات تطابق بحثك الحالي. جرب تغيير كلمات البحث أو تصفية تصنيفات أخرى."
              : "يبدو أن صندوق الوارد الخاص بك فارغ حالياً. سنقوم بتنبيهك فور وصول أي إشعار جديد!"
          }}
        </p>

        <v-btn
          v-if="searchQuery || activeFilter !== 'all'"
          color="primary"
          variant="flat"
          rounded="pill"
          size="large"
          class="px-8 font-weight-bold reset-btn elevation-3"
          prepend-icon="mdi-filter-off-outline"
          @click="resetFilters"
        >
          إعادة ضبط التصفية
        </v-btn>
      </v-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useNotificationStore } from "../../../store/notificationStore";

const notificationStore = useNotificationStore();
const currentPage = ref(1);
const activeFilter = ref("all");
const searchQuery = ref("");
const loadingAll = ref(false);

const dataTableRef = ref(null);
const loadingTable = ref(false);
const tableItems = ref({
  results: [],
  pagination: { count: 0, current_page: 1, num_pages: 1 },
});

const filters = ref({
  start_date: null,
  end_date: null,
});
const filterMenu = ref(false);

const hasActiveFilters = computed(() => {
  return !!(filters.value.start_date || filters.value.end_date);
});

const applyFilters = () => {
  filterMenu.value = false;
  if (dataTableRef.value && dataTableRef.value.params) {
    dataTableRef.value.params.page = 1;
    dataTableRef.value.fetchData();
  }
};

const clearFilters = () => {
  filters.value.start_date = null;
  filters.value.end_date = null;
  applyFilters();
};

const headers = ref([
  { title: "الإشعار", key: "title", sortable: false },
  { title: "التفاصيل", key: "message", sortable: false },
  { title: "الوقت", key: "created_at", sortable: false, align: "center" },
]);

onMounted(() => {
  if (
    !notificationStore.systemNotifications ||
    notificationStore.systemNotifications.length === 0
  ) {
    notificationStore.fetchSystemNotifications();
  }
});

// Computeds
const unreadCount = computed(() => {
  return notificationStore.systemNotifications?.filter((n) => !n.is_read).length || 0;
});

const allCount = computed(() => {
  return notificationStore.systemNotifications?.length || 0;
});

const readCount = computed(() => {
  return notificationStore.systemNotifications?.filter((n) => n.is_read).length || 0;
});

const alertCount = computed(() => {
  return (
    notificationStore.systemNotifications?.filter(
      (n) => n.event_type === "alert" || n.priority === "high"
    ).length || 0
  );
});

const newsCount = computed(() => {
  return (
    notificationStore.systemNotifications?.filter(
      (n) => n.event_type === "news" || n.event_type === "announcement"
    ).length || 0
  );
});

const filteredNotifications = computed(() => {
  let list = notificationStore.systemNotifications || [];

  if (activeFilter.value === "unread") {
    list = list.filter((n) => !n.is_read);
  } else if (activeFilter.value === "read") {
    list = list.filter((n) => n.is_read);
  } else if (activeFilter.value === "alert") {
    list = list.filter((n) => n.event_type === "alert" || n.priority === "high");
  } else if (activeFilter.value === "news") {
    list = list.filter((n) => n.event_type === "news" || n.event_type === "announcement");
  }

  if (filters.value.start_date) {
    const start = new Date(filters.value.start_date).getTime();
    list = list.filter((n) => new Date(n.created_at).getTime() >= start);
  }
  if (filters.value.end_date) {
    const end = new Date(filters.value.end_date).getTime() + 86400000;
    list = list.filter((n) => new Date(n.created_at).getTime() <= end);
  }

  return list;
});

const searchedNotifications = computed(() => {
  let list = filteredNotifications.value;

  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    list = list.filter(
      (n) =>
        (n.title && n.title.toLowerCase().includes(query)) ||
        (n.message && n.message.toLowerCase().includes(query)) ||
        (n.module_name && n.module_name.toLowerCase().includes(query))
    );
  }

  return list;
});

// Methods
const markAsRead = async (id) => {
  await notificationStore.markSystemAsRead(id);
};

const markAllAsRead = async () => {
  loadingAll.value = true;
  await notificationStore.markAllSystemAsRead();
  loadingAll.value = false;
};

const resetFilters = () => {
  searchQuery.value = "";
  activeFilter.value = "all";
};

import { watch } from "vue";

watch([activeFilter], () => {
  if (dataTableRef.value) {
    dataTableRef.value.params.page = 1;
    dataTableRef.value.fetchData();
  }
});

const fetchTableData = async (incomingParams) => {
  const params =
    incomingParams && incomingParams.params
      ? incomingParams.params
      : dataTableRef.value?.params || { page: 1, page_size: 10 };

  // Sync the table search with our local reactive searchQuery
  searchQuery.value = params.search || "";

  // Fetch more data if needed to fulfill the page
  const requiredCount = params.page * params.page_size;
  if (
    requiredCount > notificationStore.systemNotifications.length &&
    notificationStore.systemNotificationsHasNext
  ) {
    loadingTable.value = true;
    const nextPage = Math.floor(notificationStore.systemNotifications.length / 10) + 1;
    await notificationStore.fetchSystemNotifications(nextPage, true);
    loadingTable.value = false;
  }

  // Use local searched and filtered notifications
  const list = searchedNotifications.value;
  const start = (params.page - 1) * params.page_size;
  const end = start + params.page_size;

  let totalPages = Math.ceil(list.length / params.page_size) || 1;
  // If we haven't loaded everything from the backend yet, fake at least one more page so the user can navigate to it
  if (notificationStore.systemNotificationsHasNext) {
    totalPages = Math.max(totalPages, params.page + 1);
  }

  tableItems.value = {
    results: list.slice(start, end),
    pagination: {
      count: notificationStore.systemNotificationsHasNext
        ? list.length + params.page_size
        : list.length,
      current_page: params.page,
      num_pages: totalPages,
    },
  };

  return tableItems.value;
};

const handleNotificationClick = (notification) => {
  if (notification.action_url) {
    notificationStore.markSystemAsRead(notification.id);
    if (notification.action_url.startsWith("http")) {
      window.open(notification.action_url, "_self");
    } else {
      const basePath = window.location.origin;
      window.location.href = notification.action_url.startsWith("/")
        ? basePath + notification.action_url
        : basePath + "/" + notification.action_url;
    }
  } else {
    notificationStore.markSystemAsRead(notification.id);
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "";
  return new Date(dateString).toLocaleString("ar-SA", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

// Styling Helpers
const getIcon = (notification) => {
  if (notification.priority === "high") return "mdi-alert-octagon-outline";
  if (notification.event_type === "alert") return "mdi-alert-outline";
  if (notification.event_type === "success") return "mdi-check-circle-outline";
  if (notification.event_type === "news") return "mdi-newspaper-variant-outline";
  return "mdi-bell-outline";
};

const getIconColor = (notification) => {
  if (notification.priority === "high" || notification.event_type === "alert")
    return "error";
  if (notification.event_type === "success") return "success";
  if (notification.event_type === "news") return "info";
  return "primary";
};

const getColorClass = (notification) => {
  if (notification.priority === "high" || notification.event_type === "alert")
    return "bg-error-gradient";
  if (notification.event_type === "success") return "bg-success-gradient";
  if (notification.event_type === "news") return "bg-info-gradient";
  return "bg-primary-gradient";
};
</script>

<style scoped>
/* Main Page Layout */
.notifications-screen {
  font-family: "Inter", "Roboto", "Outfit", "Cairo", sans-serif !important;
  height: calc(100vh - 85px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  direction: rtl;
}

.scroll-container {
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
}

.scroll-container::-webkit-scrollbar {
  width: 6px;
}

.scroll-container::-webkit-scrollbar-track {
  background: transparent;
}

.scroll-container::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.2);
  border-radius: 10px;
}

.scroll-container::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-primary), 0.4);
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

.banner-bg::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -20%;
  width: 70%;
  height: 200%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.08) 0%,
    rgba(255, 255, 255, 0) 60%
  );
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

.unread-number {
  color: rgb(var(--v-theme-primary)) !important;
}

.mark-all-btn {
  border: 1.5px solid rgba(255, 255, 255, 0.4) !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(8px);
}

.mark-all-btn:hover {
  background: rgba(255, 255, 255, 0.15) !important;
  border-color: rgba(255, 255, 255, 0.8) !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

/* Control Panel Card */
.control-panel-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12) !important;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05) !important;
}

.z-index-2 {
  z-index: 2;
}

/* Modern Search Field Styling */
.search-input :deep(.v-field) {
  border-radius: 8px !important;
  background-color: rgb(var(--v-theme-background)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12) !important;
  transition: all 0.3s ease !important;
}

.search-input :deep(.v-field--focused) {
  background-color: rgb(var(--v-theme-surface)) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 0 0 4px rgba(var(--v-theme-primary), 0.1) !important;
}

/* Custom Styled Filter Chips */
.filter-chip {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12) !important;
  background: rgb(var(--v-theme-surface)) !important;
  color: rgba(var(--v-theme-on-surface), 0.7) !important;
}

.filter-chip:hover {
  transform: translateY(-1px);
  border-color: rgba(var(--v-theme-on-surface), 0.15) !important;
  color: rgb(var(--v-theme-on-surface)) !important;
}

:deep(.active-filter-chip) {
  background: rgb(var(--v-theme-primary)) !important;
  background-image: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.15) 0%,
    rgba(0, 0, 0, 0.15) 100%
  ) !important;
  color: #ffffff !important;
  border-color: transparent !important;
  box-shadow: 0 8px 16px -4px rgba(var(--v-theme-primary), 0.3) !important;
  transform: translateY(-1px);
}

/* Badge count inside filter chip */
.chip-badge {
  background-color: rgba(var(--v-theme-error), 0.1);
  color: rgb(var(--v-theme-error));
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 99px;
  font-weight: 800;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

:deep(.active-filter-chip) .chip-badge {
  background-color: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

/* Custom Scrollbar for Infinite Scroll area */
.custom-scroll-area {
  scrollbar-width: thin;
  scrollbar-color: rgba(var(--v-theme-primary), 0.15) transparent;
}

.custom-scroll-area::-webkit-scrollbar {
  width: 6px;
}

.custom-scroll-area::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scroll-area::-webkit-scrollbar-thumb {
  background-color: rgba(var(--v-theme-primary), 0.15);
  border-radius: 20px;
  transition: background-color 0.2s ease;
}

.custom-scroll-area::-webkit-scrollbar-thumb:hover {
  background-color: rgba(var(--v-theme-primary), 0.35);
}

/* Premium Notification Cards Layout */
.notification-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12) !important;
  border-radius: 20px !important;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
  cursor: pointer;
  overflow: hidden;
}

.notification-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 30px -10px rgba(var(--v-theme-primary), 0.12) !important;
  border-color: rgba(var(--v-theme-primary), 0.25) !important;
}

.notification-card:hover .side-indicator {
  width: 9px;
}

/* Unread vs Read Specific Card Styling */
.unread-card {
  background: linear-gradient(
    90deg,
    rgba(var(--v-theme-primary), 0.03) 0%,
    rgb(var(--v-theme-surface)) 100%
  ) !important;
  border-color: rgba(var(--v-theme-primary), 0.15) !important;
}

.unread-card:hover {
  background: linear-gradient(
    90deg,
    rgba(var(--v-theme-primary), 0.05) 0%,
    rgb(var(--v-theme-surface)) 100%
  ) !important;
}

.read-card {
  opacity: 0.9;
}

/* Side indicator gradients */
.side-indicator {
  width: 5px;
  flex-shrink: 0;
  transition: width 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.bg-primary-gradient {
  background: linear-gradient(
    to bottom,
    rgba(var(--v-theme-primary), 0.8),
    rgb(var(--v-theme-primary))
  );
}

.bg-error-gradient {
  background: linear-gradient(to bottom, #f87171, #ef4444);
}

.bg-success-gradient {
  background: linear-gradient(to bottom, #4ade80, #22c55e);
}

.bg-info-gradient {
  background: linear-gradient(to bottom, #38bdf8, #0ea5e9);
}

/* Avatar layout and brand coloring */
.notification-avatar {
  border-radius: 14px !important;
}

.color-brand-icon {
  color: rgb(var(--v-theme-primary));
}

/* Glowing Pulse Dot for Unread Notifications */
.unread-pulse-dot {
  width: 8px;
  height: 8px;
  background-color: rgb(var(--v-theme-primary));
  border-radius: 50%;
  display: inline-block;
  box-shadow: 0 0 0 0 rgba(var(--v-theme-primary), 0.7);
  animation: dot-pulse 1.8s infinite cubic-bezier(0.66, 0, 0, 1);
}

@keyframes dot-pulse {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(var(--v-theme-primary), 0.7);
  }

  70% {
    transform: scale(1);
    box-shadow: 0 0 0 6px rgba(var(--v-theme-primary), 0);
  }

  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(var(--v-theme-primary), 0);
  }
}

/* Custom styled mark-as-read button appearing elegantly */
.mark-read-btn {
  background-color: rgba(var(--v-theme-success), 0.1) !important;
  color: rgb(var(--v-theme-success)) !important;
  border-radius: 12px !important;
  transition: all 0.25s ease !important;
}

.mark-read-btn:hover {
  background-color: rgb(var(--v-theme-success)) !important;
  color: rgb(var(--v-theme-surface)) !important;
  transform: scale(1.1);
  box-shadow: 0 6px 12px rgba(var(--v-theme-success), 0.25) !important;
}

/* Message Text clamping */
.notification-message {
  font-size: 0.95rem;
  line-height: 1.6;
  white-space: pre-line;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Open Attached Link Button */
.action-link-btn {
  letter-spacing: 0.5px;
  font-size: 0.8rem;
  box-shadow: 0 4px 10px rgba(var(--v-theme-primary), 0.15) !important;
  transition: all 0.25s ease !important;
}

.action-link-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 15px rgba(var(--v-theme-primary), 0.3) !important;
}

/* High Fidelity Empty State Styles */
.empty-state-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), 0.12) !important;
}

.empty-state-icon-wrapper {
  width: 130px;
  height: 130px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.inner-avatar {
  border-radius: 24px !important;
  border: 2px solid rgb(var(--v-theme-surface));
  z-index: 2;
}

.pulse-ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(var(--v-theme-primary), 0.15);
  animation: ripple 4s infinite linear;
  z-index: 1;
}

.ring-1 {
  width: 110px;
  height: 110px;
  animation-delay: 0s;
}

.ring-2 {
  width: 140px;
  height: 140px;
  animation-delay: 1.5s;
}

@keyframes ripple {
  0% {
    transform: scale(0.8);
    opacity: 0.8;
  }

  50% {
    opacity: 0.4;
  }

  100% {
    transform: scale(1.4);
    opacity: 0;
  }
}

.max-width-text {
  max-width: 480px;
  line-height: 1.6;
}

.reset-btn {
  transition: all 0.25s ease !important;
}

.reset-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(var(--v-theme-primary), 0.25) !important;
}

/* Staggered list animations */
.list-enter-active,
.list-leave-active {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.list-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.97);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.list-move {
  transition: transform 0.4s ease;
}
</style>
