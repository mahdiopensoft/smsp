<template>
 <v-app >
  <!-- ══════════════════════════════════════════════════════
       AllowDataEntery — Allowed Values Viewer
       UI Redesign: Clean, token-based, professional
  ══════════════════════════════════════════════════════ -->
  <VCard
    :loading="loading"
    class="allow-entry-card"
    elevation="0"
  >
    <!-- Header -->
    <div class="allow-entry-header">
      <div class="allow-entry-header-icon">
        <v-icon size="20" color="primary">mdi-format-list-bulleted</v-icon>
      </div>
      <div class="allow-entry-header-text">
        <div class="allow-entry-field-label">القيم المسموح بها</div>
        <div class="allow-entry-field-name">{{ field_name }}</div>
      </div>
    </div>

    <v-divider class="allow-entry-divider" />

    <VCardText class="allow-entry-body">

      <!-- Loading State -->
      <div v-if="loading" class="allow-entry-loading">
        <v-progress-circular indeterminate color="primary" size="32" width="2" />
        <span class="allow-entry-loading-text">جاري التحميل...</span>
      </div>

      <!-- Empty State -->
      <div v-else-if="!items || items.length === 0" class="allow-entry-empty">
        <v-icon size="36" color="grey-lighten-2">mdi-inbox-outline</v-icon>
        <span class="allow-entry-empty-text">لا توجد قيم متاحة</span>
      </div>

      <!-- Items List -->
      <div v-else class="allow-entry-list">
        <div
          v-for="(item, index) in items"
          :key="index"
          class="allow-entry-item"
        >
          <span class="allow-entry-index">{{ index + 1 }}</span>
          <span class="allow-entry-value">{{ item }}</span>
        </div>
      </div>

    </VCardText>
  </VCard>

 </v-app>

</template>
<script>
// import dataList from "@/utils/DataAutoList";

export default {
  props: ["name", "field_name"],
  data() {
    return {
      items: [],
      loading:false
    };
  },
  async created() {
    this.getListName();
  },
  methods: {
    async getListName() {

      // this.loading = true
      // // const data = dataList()[this.name];
      // const data = {}
 
      // // let list = await data.method(true).then((e) => e);


      // if (typeof list === "string") {
      //   let url = list;
      //   console.log(url);
      //   list = [];
      //   url = url.replace(/filter\/$/, "all/");

      //   await this.$axios(url).then((res) => (list = res.data));
      // }

      // const label = data.title || "name";
      // this.items = list.map((e) => e[label]);

      // this.loading = false
    },
  },
};
</script>

<style scoped>
/* ══════════════════════════════════════════════════════
   AllowDataEntery — Design Token Based Styling
══════════════════════════════════════════════════════ */

.allow-entry-card {
  border-radius: var(--radius-xl) !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08) !important;
  overflow: hidden;
  min-width: 320px;
}

/* ── Header ── */
.allow-entry-header {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md) var(--space-lg);
  background: rgba(var(--v-theme-primary), 0.03);
}

.allow-entry-header-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-lg);
  background: rgba(var(--v-theme-primary), 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.allow-entry-header-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.allow-entry-field-label {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: rgba(var(--v-theme-on-surface), 0.45);
}

.allow-entry-field-name {
  font-size: 1rem;
  font-weight: 700;
  color: rgb(var(--v-theme-on-surface));
  line-height: 1.3;
}

.allow-entry-divider {
  opacity: 0.06;
}

/* ── Body ── */
.allow-entry-body {
  padding: var(--space-md) !important;
  min-height: 120px;
}

/* ── Loading State ── */
.allow-entry-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-md);
  padding: var(--space-xl);
}

.allow-entry-loading-text {
  font-size: 0.875rem;
  color: rgba(var(--v-theme-on-surface), 0.45);
}

/* ── Empty State ── */
.allow-entry-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  padding: var(--space-xl);
}

.allow-entry-empty-text {
  font-size: 0.875rem;
  color: rgba(var(--v-theme-on-surface), 0.4);
}

/* ── Items List ── */
.allow-entry-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  max-height: 320px;
  overflow-y: auto;
}

.allow-entry-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  background: rgba(var(--v-theme-on-surface), 0.02);
  border: 1px solid rgba(var(--v-theme-on-surface), 0.05);
  transition: background 0.15s ease;
}

.allow-entry-item:hover {
  background: rgba(var(--v-theme-primary), 0.04);
  border-color: rgba(var(--v-theme-primary), 0.1);
}

.allow-entry-index {
  flex-shrink: 0;
  width: 22px;
  height: 22px;
  border-radius: var(--radius-full);
  background: rgba(var(--v-theme-primary), 0.08);
  color: rgb(var(--v-theme-primary));
  font-size: 0.72rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.allow-entry-value {
  font-size: 0.88rem;
  color: rgb(var(--v-theme-on-surface));
  font-weight: 500;
  line-height: 1.4;
}

/* ── Scrollbar ── */
.allow-entry-list::-webkit-scrollbar {
  width: 4px;
}

.allow-entry-list::-webkit-scrollbar-track {
  background: transparent;
}

.allow-entry-list::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.1);
  border-radius: var(--radius-full);
}
</style>