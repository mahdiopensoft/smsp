<template>
  <v-row>
    <v-col
      v-for="(metric, idx) in metricCards()"
      :key="idx"
      cols="12"
      sm="6"
      md="3"
      lg="2"
      class="pt-0"
    >
      <div
        class="health-matrix-node"
        :class="metric.colorClass"
        :style="{ animationDelay: idx * 100 + 'ms' }"
      >
        <div class="node-glow"></div>
        <div class="node-content">
          <div class="d-flex justify-space-between align-start mb-5">
            <div>
              {{ metric.label }}
            </div>

            <v-icon size="20" :icon="metric.icon"></v-icon>
          </div>

          <div class="d-flex align-end justify-space-between">
            <div class="d-flex align-baseline">
              <div
                v-if="loading?.groups"
                class="skeleton-bone"
                style="width: 60px; height: 32px"
              ></div>
              <template v-else>
                <div class="metric-value">{{ metric.value }}</div>
                <div
                  class="text-body-2 ms-1 opacity-40 font-weight-bold"
                  v-if="metric.suffix"
                >
                  {{ metric.suffix }}
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>
    </v-col>
  </v-row>

  <filter-fields>
    <template #fields>
      <VRow>
        <auto-list v-model="filter.status" name="statusSync" cols="2" />
        <auto-list v-model="filter.screen" name="ScreenSync" cols="2" />
        <custom-date v-model="filter.date_from" cols="2" label="من تاريخ" />
        <custom-date v-model="filter.date_to" cols="2" label="الى تاريخ" />

        <custom-btn type="filter" class="mt-2" :click="getData" />
      </VRow>
    </template>
  </filter-fields>
  <custom-data-table
    :="{
      headers,
      items,
      getData,
      restore: false,
      log: false,
      customLoading,
      showSelect: false,
    }"
  ></custom-data-table>
</template>
<script setup>
import { ref, computed, onMounted } from "vue";
import shared from "external-components";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const filter = ref({});

const items = ref({});
const headers = computed(() => {
  return [
    { title: t("record"), key: "object_display_name" },
    { title: t("screen_type"), key: "screen_name" },
    { title: t("organization"), key: "org_name" },

    { title: t("action"), key: "action_type_display" },
    { title: t("sync_status"), key: "sync_status_display" },
    { title: t("date"), key: "last_modified_at" },
    { title: t("error_message"), key: "error_message", show: false },
  ];
});

const customLoading = ref(false);
const getData = async (
  params = { page: 1, perPage: 10, sort_by: "id", txt_search: "" }
) => {
  customLoading.value = true;
  try {
    const response = await shared.api("sync/status/", {
      params: {
        ...filter.value,
        ...params.params,
      },
    });
    items.value = response?.data;
  } finally {
    customLoading.value = false;
  }
};

const summary = ref({});
const getSummary = async () => {
  try {
    const response = await shared.api("sync/status/summary/", {});
    summary.value = response?.data?.data;
  } finally {
  }
};

const metricCards = () => {
  return [
    {
      key: "syncedScreens",
      label: t("syncedRecord"),
      value: summary.value.synced,
      icon: "mdi-sync",
      color: "teal",
      colorClass: "teal",
    },
    {
      key: "needUpdateScreens",
      label: t("needUpdateScreens"),
      value: summary.value.sync_change,
      icon: "mdi-timer-sand",
      color: "amber",
      colorClass: "amber",
    },

    {
      key: "notSyncedScreens",
      label: t("notSyncedRecord"),
      value: summary.value.no_sync,
      icon: "mdi-alert-octagon-outline",
      color: "slate",
      colorClass: "slate",
    },

    {
      key: "pendingScreen",
      label: t("pending"),
      value: summary.value.pending,
      icon: "mdi-alert-octagon-outline",
      color: "primary",
      colorClass: "primary",
    },
    {
      key: "totalScreens",
      label: t("totalScreens"),
      value: summary?.value?.screens?.length,
      icon: "mdi-monitor-dashboard",
      color: "indigo",
      colorClass: "indigo",
    },
  ];
};

onMounted(() => {
  getSummary();
});
</script>
<style scoped>
.health-matrix-node {
  position: relative;
  /* background: rgba(var(--v-theme-on-surface), 0.03); */
  background: #f8fafc1a;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.06);
  border-radius: 20px;
  padding: 24px;
  overflow: hidden;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  animation: fade-up 0.5s ease forwards;
  opacity: 0;
}
.metric-label {
  font-size: 0.8rem;
  font-weight: 900;
  color: #94a3b8;
  letter-spacing: 0.05em;
}

@keyframes fade-up {
  from {
    opacity: 0;
    transform: translateY(16px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.health-matrix-node:hover {
  /* transform: translateY(-4px);
  border-color: rgba(var(--v-theme-on-surface), 0.12);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08); */
  transform: translateY(-4px);
  border-color: rgba(203, 213, 225, 0.6);
  box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.06), 0 12px 24px -8px rgba(0, 0, 0, 0.1);

  --card-accent: red !important;
}

.node-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: currentColor;
  opacity: 0.4;
}

.health-matrix-node.cyan {
  color: #06b6d4;
}

.health-matrix-node.indigo {
  color: #5a8dee;
}

.health-matrix-node.emerald {
  color: #10b981;
}

.health-matrix-node.rose {
  color: #ef4444;
}
.health-matrix-node.teal {
  color: #14b8a6;
}
.health-matrix-node.amber {
  color: #f59e0b;
}
.health-matrix-node.slate {
  color: #64748b;
}

.metric-label {
  font-size: 10px !important;
  letter-spacing: 1.5px !important;
}

.metric-value {
  font-family: "JetBrains Mono", monospace;
  font-size: 36px;
  font-weight: 800;
  line-height: 1;
  color: rgb(var(--v-theme-on-background));
}

.metric-icon-box {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.health-matrix-node:hover .metric-icon-box {
  transform: scale(1.1);
}
.metric-icon-box.indigo {
  background: linear-gradient(135deg, #5a8dee 0%, #80a8f2 100%);
  box-shadow: 0 4px 14px rgba(99, 163, 241, 0.3);
}

.metric-icon-box.rose {
  background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.3);
}

.metric-icon-box.cyan {
  background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%);
  box-shadow: 0 4px 14px rgba(6, 182, 212, 0.3);
}

.metric-icon-box.emerald {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
}
.metric-icon-box.teal {
  background: linear-gradient(135deg, #14b8a6 0%, #2dd4bf 100%);
  box-shadow: 0 4px 14px rgba(20, 184, 166, 0.3);
}
.metric-icon-box.amber {
  background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
  box-shadow: 0 4px 14px rgba(245, 158, 11, 0.3);
}
.metric-icon-box.slate {
  background: linear-gradient(135deg, #64748b 0%, #94a3b8 100%);
  box-shadow: 0 4px 14px rgba(100, 116, 139, 0.3);
}

.sync-pulse-btn {
  animation: gentle-pulse 2s infinite;
}

@keyframes gentle-pulse {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(var(--v-theme-primary), 0.3);
  }

  50% {
    box-shadow: 0 0 0 6px rgba(var(--v-theme-primary), 0);
  }
}
</style>
