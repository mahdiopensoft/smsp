<template>
  <div
    class="premium-tab"
    :class="{ 
      'is-active': is_current, 
      'has-error': error 
    }"
  >
    <div class="tab-body">
      <!-- Only Show Icon if Error exists, otherwise pure text -->
      <v-icon v-if="error" icon="mdi-alert-circle" size="18" class="error-icon" />
      
      <!-- Title -->
      <span class="tab-title">{{ title }}</span>
    </div>

    <!-- Minimalist Interaction Line (Used in standalone mode) -->
    <div class="active-bar"></div>
  </div>
</template>

<script>
export default {
  props: {
    error: {
      type: Boolean,
      default: false,
    },
    index: [String, Number], 
    is_current: {
      type: Boolean,
      default: false
    },
    title: String,
  },
};
</script>

<style scoped>
/* ══════════════════════════════════════════════════
   ULTRA-MINIMALIST TAB — ZERO LATENCY
   ══════════════════════════════════════════════════ */

.premium-tab {
  display: inline-flex;
  flex: 1;
  justify-content: center;
  min-width: 120px;
  padding: 16px 24px;
  position: relative;
  cursor: pointer;
  user-select: none;
  background: transparent;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.06);
  border-radius: 6px !important;
  /* NO TRANSITIONS - Instant state change for zero CPU load */
  transition: none !important;
}

.tab-body {
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 2;
}

/* ── Title ── */
.tab-title {
  font-size: 0.9rem;
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface), 0.45);
  white-space: nowrap;
  letter-spacing: 0.01em;
  transition: none !important;
}

/* ── Active State ── */
.premium-tab.is-active {
  background-color: rgba(var(--v-theme-primary), 0.05);
}

.premium-tab.is-active .tab-title {
  color: rgb(var(--v-theme-primary));
  font-weight: 700;
}

/* Active Bottom Bar (Standalone) */
.active-bar {
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: rgb(var(--v-theme-primary));
  transform: scaleX(0);
  transition: none !important;
}

.premium-tab.is-active .active-bar {
  transform: scaleX(1);
}

/* ── Error State ── */
.premium-tab.has-error {
  background-color: rgba(var(--v-theme-error), 0.05);
}

.premium-tab.has-error .tab-title,
.premium-tab.has-error .error-icon {
  color: rgb(var(--v-theme-error)) !important;
}

.premium-tab.has-error .active-bar {
  background-color: rgb(var(--v-theme-error));
}

/* ── Hover ── */
.premium-tab:hover:not(.is-active) {
  background-color: rgba(var(--v-theme-on-surface), 0.02);
}

.premium-tab:hover:not(.is-active) .tab-title {
  color: rgba(var(--v-theme-on-surface), 0.8);
}

/* RTL Support */
[dir="rtl"] .tab-title {
  font-family: 'Tajawal', sans-serif !important;
}
</style>

<style>
/* ══════════════════════════════════════════════════
   GLOBAL AUTO-BRIDGE: CLEANEST ENGINE
   ══════════════════════════════════════════════════ */

.v-tab:has(.premium-tab) {
  padding: 0 !important;
  min-width: unset !important;
  border-radius: 6px !important;
  margin: 0 2px !important;
  transition: none !important; /* Zero overhead */
}

/* Kill all heavy animations and ripple engines */
.v-tab:has(.premium-tab) .v-ripple__container,
.v-tab:has(.premium-tab) .v-btn__overlay,
.v-tab:has(.premium-tab) .v-btn__underlay,
.v-tab:has(.premium-tab) .v-btn__content::before,
.v-tab:has(.premium-tab) .v-btn__content::after {
  display: none !important;
  transition: none !important;
  animation: none !important;
}

/* Quick Color Bridge */
.v-tab:has(.premium-tab.is-active) {
  background-color: rgba(var(--v-theme-primary), 0.1) !important;
}

.v-tab:has(.premium-tab.has-error) {
  background-color: rgba(var(--v-theme-error), 0.1) !important;
}

.v-tab:has(.premium-tab.has-error) .v-tab__slider {
  background-color: rgb(var(--v-theme-error)) !important;
  height: 2px !important;
  transition: none !important;
}

/* Layout Bridge */
.v-tab:has(.premium-tab) .v-btn__content {
  width: 100% !important;
  height: 100% !important;
  padding: 0 !important;
  max-width: none !important;
}

.v-tab .premium-tab {
  display: flex !important;
  align-items: center;
  justify-content: center;
  width: 100% !important;
  height: 100% !important;
  padding: 0 30px !important; 
  border-bottom: none !important;
  background-color: transparent !important; 
  box-shadow: none !important;
  transition: none !important;
  will-change: auto; /* Avoid unnecessary GPU layers */
}

.v-tab .premium-tab .active-bar {
  display: none !important;
}

.v-tab:has(.premium-tab) {
  text-transform: none !important;
  letter-spacing: normal !important;
}

/* Disable Vuetify's slider transition if possible via CSS */
.v-tabs:has(.premium-tab) .v-tab__slider {
  transition: none !important;
}
</style>