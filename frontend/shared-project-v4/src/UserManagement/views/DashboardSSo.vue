<template>
  <div class="dashboard-sso-master standalone-main pa-0 d-flex flex-column">
    <!-- Background Pattern -->
    <div class="bg-pattern-overlay"></div>

    <div class="relative-content d-flex flex-column w-100">
      <!-- 1. Institutional Master Header -->
      <header class="dashboard-hero-portal-pure flex-shrink-0 mb-6 mb-md-10">
        <div class="portal-inner pa-5 pa-sm-6 pa-md-8 max-width-safe mx-auto">
          <v-row align="center" no-gutters>
            <v-col cols="12" md="7">
              <div
                class="welcome-container-pure d-flex align-center ga-4 ga-md-5 flex-column flex-sm-row text-center text-sm-start"
              >
                <div class="institutional-avatar-refined mb-3 mb-sm-0">
                  <v-icon :size="$vuetify.display.xs ? 24 : 30" color="white"
                    >mdi-account-tie-outline</v-icon
                  >
                </div>

                <div
                  class="greeting-content-pure ps-0 ps-sm-6 d-flex flex-column justify-center"
                  :class="{ 'header-border-fix': !$vuetify.display.xs }"
                >
                  <div
                    class="top-meta d-flex align-center justify-center justify-sm-start ga-2 mb-2"
                  >
                    <span
                      class="text-overline font-weight-black text-white-soft"
                      style="
                        font-size: 0.65rem !important;
                        letter-spacing: 1.5px;
                        opacity: 0.8;
                      "
                    >
                      {{ isAr ? "بوابة الإدارة" : "ADMIN PORTAL" }}
                    </span>
                    <v-divider
                      vertical
                      length="10"
                      class="mx-1 d-none d-sm-inline-block"
                      color="white"
                      style="opacity: 0.3"
                    ></v-divider>
                    <span
                      class="text-caption text-white-op-70 font-weight-bold d-none d-sm-inline-block"
                    >
                      {{ isAr ? "نظام المنصة الموحدة" : "Unified Platform System" }}
                    </span>
                  </div>
                  <h1 class="welcome-heading-pure" style="line-height: 1.1 !important">
                    <span
                      class="text-white-op-60 font-weight-light"
                      :style="{ fontSize: $vuetify.display.xs ? '1.1rem' : '1.3rem' }"
                    >
                      {{ isAr ? "أهلاً بك،" : "Welcome," }}
                    </span>
                    <span
                      class="font-weight-black text-white ms-2"
                      :style="{ fontSize: $vuetify.display.xs ? '1.5rem' : '1.8rem' }"
                      >{{ userName }}</span
                    >
                  </h1>
                </div>
              </div>
            </v-col>
            <v-col
              cols="12"
              md="5"
              class="mt-6 mt-md-0 d-flex justify-center justify-md-end"
            >
              <div
                class="status-summary-pure d-flex align-center ga-3 w-100 w-sm-auto justify-center justify-md-end"
              >
                <div class="meta-item d-flex align-center ga-3">
                  <div class="d-flex flex-column align-end">
                    <span
                      class="text-overline text-white-op-70 mb-0"
                      style="
                        font-size: 0.6rem !important;
                        letter-spacing: 1px;
                        line-height: 1;
                      "
                    >
                      {{ isAr ? "المنصة" : "PLATFORM" }}
                    </span>
                    <span
                      class="text-caption font-weight-black text-white"
                      style="font-size: 0.9rem !important"
                    >
                      {{
                        state.isSSO
                          ? isAr
                            ? "المنصة الموحدة"
                            : "Unified Platform"
                          : isAr
                          ? "تسجيل دخول عادي"
                          : "Standard Login"
                      }}
                    </span>
                  </div>
                  <div
                    class="institutional-avatar-refined"
                    style="
                      width: 42px;
                      height: 42px;
                      background: rgba(255, 255, 255, 0.12);
                    "
                  >
                    <v-icon size="20" color="white">{{
                      state.isSSO ? "mdi-shield-check" : "mdi-account-lock-outline"
                    }}</v-icon>
                  </div>
                </div>
              </div>
            </v-col>
          </v-row>
        </div>
      </header>

      <!-- Grid Content Wrapping Container -->
      <v-container
        class="systems-grid-container pb-16 px-4 px-sm-6 px-md-12 max-width-safe w-100"
      >
        <!-- 2. Smart Stats Modules - FINAL PROFESSIONAL VERSION -->
        <v-row>
          <v-col
            v-for="(stat, index) in translatedStats"
            :key="index"
            cols="12"
            sm="6"
            md="3"
            class="stagger-item mb-4 mb-md-0"
          >
            <v-card class="premium-stat-card h-100" elevation="0">
              <div class="card-glass-shine"></div>
              <v-card-text class="pa-5 pa-md-6 d-flex align-center relative-z">
                <!-- Executive Icon Container -->
                <div class="stat-icon-wrapper me-4" :class="`border-${stat.color}`">
                  <div class="icon-inner-bg" :class="`bg-${stat.color}-faint`"></div>
                  <v-icon
                    :size="$vuetify.display.xs ? 22 : 26"
                    :color="stat.color"
                    class="relative-z"
                    >{{ stat.icon }}</v-icon
                  >
                </div>

                <div class="flex-grow-1">
                  <div class="text-overline font-weight-black label-stat-pro mb-0">
                    {{ stat.label }}
                  </div>
                  <div
                    class="text-h5 font-weight-black value-stat-pro"
                    :class="`text-${stat.color}`"
                  >
                    {{ stat.value }}
                  </div>
                </div>

                <!-- Subtle Side Accent -->
                <div class="side-accent" :class="`bg-${stat.color}`"></div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <div class="py-4 py-md-8"></div>

        <!-- 3. Quick Actions Command Center -->
        <v-row>
          <v-col cols="12" class="stagger-item">
            <v-card
              class="identity-stat-module rounded-xl overflow-hidden gateway-pro-card-large"
              elevation="0"
            >
              <div
                class="hub-header pa-6 pa-md-8 d-flex align-center border-b flex-column flex-sm-row text-center text-sm-start ga-4 ga-sm-0"
              >
                <div class="hub-icon-box me-0 me-sm-5">
                  <v-icon color="primary" size="28">mdi-view-grid-plus-outline</v-icon>
                </div>
                <div>
                  <h3
                    class="text-h5 font-weight-black"
                    style="color: rgb(var(--v-theme-on-surface)); margin: 0"
                  >
                    {{ isAr ? "إجراءات سريعة" : "Quick Actions" }}
                  </h3>
                  <p class="text-body-2 mb-0 op-60">
                    {{
                      isAr
                        ? "الوصول المباشر للمهام الإدارية والمستندات الهامة"
                        : "Direct access to administrative tasks and important documents"
                    }}
                  </p>
                </div>
              </div>
              <v-card-text class="pa-4 pa-md-8">
                <v-row>
                  <v-col
                    v-for="(action, index) in translatedActions"
                    :key="index"
                    cols="12"
                    sm="6"
                    md="3"
                    class="pa-2 pa-md-3"
                  >
                    <div
                      class="access-capsule-modern d-flex align-center pa-4 cursor-pointer h-100"
                      @click="openLink(action)"
                    >
                      <div
                        class="access-icon-box-modern me-4"
                        :style="{
                          background: `rgba(var(--v-theme-${action.color}), 0.1)`,
                        }"
                      >
                        <v-icon size="22" :color="action.color">{{ action.icon }}</v-icon>
                      </div>
                      <div class="flex-grow-1 overflow-hidden">
                        <span
                          class="text-subtitle-2 font-weight-bold text-truncate d-block"
                          style="color: rgb(var(--v-theme-on-surface))"
                          >{{ action.label }}</span
                        >
                      </div>
                      <v-btn
                        icon
                        variant="tonal"
                        size="x-small"
                        color="primary"
                        class="access-arrow-btn-modern ms-2"
                        elevation="0"
                      >
                        <v-icon size="14">{{
                          isAr ? "mdi-arrow-left" : "mdi-arrow-right"
                        }}</v-icon>
                      </v-btn>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script setup>
import { computed, getCurrentInstance } from "vue";
import { useRouter } from "vue-router";
import { state } from "@/../src/store/state";

const router = useRouter();
const instance = getCurrentInstance();
const isAr = computed(() => instance.proxy.$i18n.locale === "ar");

const userName = computed(
  () => state?.profile?.username || (isAr.value ? "المستخدم" : "User")
);

const translatedStats = computed(() => [
  {
    label: isAr.value ? "المستخدمين" : "Users",
    value: "--",
    icon: "mdi-account-multiple-outline",
    color: "primary",
  },
  {
    label: isAr.value ? "المجموعات" : "Groups",
    value: "--",
    icon: "mdi-account-group-outline",
    color: "info",
  },
  {
    label: isAr.value ? "أنواع المستخدمين" : "User Types",
    value: "--",
    icon: "mdi-account-key-outline",
    color: "success",
  },
  {
    label: isAr.value ? "نشط" : "Active",
    value: isAr.value ? "متصل" : "Connected",
    icon: "mdi-pulse",
    color: "warning",
  },
]);

const translatedActions = computed(() => [
  {
    label: isAr.value ? "إدارة المستخدمين" : "User Management",
    icon: "mdi-account-cog-outline",
    color: "primary",
    to: "/users",
  },
  {
    label: isAr.value ? "إدارة المجموعات" : "Group Management",
    icon: "mdi-folder-account-outline",
    color: "info",
    to: "/groups",
  },
  {
    label: isAr.value ? "الملف الشخصي" : "User Profile",
    icon: "mdi-account-badge-outline",
    color: "success",
    to: "/profile",
  },
  {
    label: isAr.value ? "وثائق API" : "API Docs",
    icon: "mdi-file-code-outline",
    color: "orange",
    href: "/api/docs/swagger/",
    target: "_blank",
  },
]);

function openLink(action) {
  if (action.to) {
    window.location.href = "/";
    router.push(action.to);
  } else if (action.href) {
    window.open(action.href, action.target || "_self");
  }
}
</script>

<style scoped>
/* ───── Layout & Base ───── */
.dashboard-sso-master {
  font-family: "Tajawal", sans-serif !important;
  position: relative;
  z-index: 1;
  background: rgb(var(--v-theme-background));
  min-height: 100vh;
}

.max-width-safe {
  max-width: 1440px !important;
  margin-left: auto !important;
  margin-right: auto !important;
}

.bg-pattern-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: radial-gradient(#1867c0 0.5px, transparent 0.5px);
  background-size: 24px 24px;
  opacity: 0.05;
  pointer-events: none;
  z-index: -1;
}

:deep(.v-theme--dark) .bg-pattern-overlay {
  opacity: 0.03;
}

.relative-z {
  position: relative;
  z-index: 2;
}

/* ───── 1. Institutional Master Header ───── */
.dashboard-hero-portal-pure {
  background: linear-gradient(
    135deg,
    rgb(var(--v-theme-primary)) 0%,
    rgba(var(--v-theme-primary), 0.8) 100%
  );
  border-radius: 0 0 40px 40px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(var(--v-theme-primary), 0.15);
  position: relative;
  width: 100%;
}

:deep(.v-theme--dark) .dashboard-hero-portal-pure {
  background: linear-gradient(
    135deg,
    rgb(var(--v-theme-primary)) 0%,
    rgba(var(--v-theme-primary), 0.6) 100%
  );
}

.institutional-avatar-refined {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.25);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  flex-shrink: 0;
}

.header-border-fix {
  border-inline-start: 1px solid rgba(255, 255, 255, 0.15);
}

.welcome-heading-pure {
  color: #ffffff !important;
}

.text-white-soft {
  color: #ffffff !important;
}
.text-white-op-70 {
  color: rgba(255, 255, 255, 0.7) !important;
}
.text-white-op-60 {
  color: rgba(255, 255, 255, 0.6) !important;
}

.status-summary-pure {
  background: rgba(255, 255, 255, 0.08);
  padding: 12px 24px;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* ───── 2. Premium Professional Stats Cards ───── */
.premium-stat-card {
  background: linear-gradient(
    145deg,
    rgb(var(--v-theme-surface)) 0%,
    rgba(var(--v-theme-surface), 0.95) 100%
  ) !important;
  border-radius: 24px !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.06) !important;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
}

.premium-stat-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.06) !important;
  border-color: rgba(var(--v-theme-on-surface), 0.12) !important;
}

.card-glass-shine {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 60%);
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.premium-stat-card:hover .card-glass-shine {
  opacity: 1;
}

.stat-icon-wrapper {
  width: 54px;
  height: 54px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  border: 1px solid transparent;
}

.icon-inner-bg {
  position: absolute;
  inset: 0;
  opacity: 0.1;
  z-index: 1;
}

.border-primary {
  border-color: rgba(var(--v-theme-primary), 0.2) !important;
}
.border-info {
  border-color: rgba(var(--v-theme-info), 0.2) !important;
}
.border-success {
  border-color: rgba(var(--v-theme-success), 0.2) !important;
}
.border-warning {
  border-color: rgba(var(--v-theme-warning), 0.2) !important;
}

.bg-primary-faint {
  background-color: rgb(var(--v-theme-primary));
}
.bg-info-faint {
  background-color: rgb(var(--v-theme-info));
}
.bg-success-faint {
  background-color: rgb(var(--v-theme-success));
}
.bg-warning-faint {
  background-color: rgb(var(--v-theme-warning));
}

.label-stat-pro {
  color: rgba(var(--v-theme-on-surface), 0.35);
  letter-spacing: 1.5px;
  font-size: 0.65rem !important;
  line-height: 1.2;
}

.value-stat-pro {
  font-size: 1.6rem !important;
  line-height: 1;
  letter-spacing: -0.5px;
}

.side-accent {
  position: absolute;
  top: 25%;
  bottom: 25%;
  right: 0;
  width: 3px;
  border-radius: 4px 0 0 4px;
  opacity: 0.6;
}

/* ───── 3. Hub Details & Actions ───── */
.identity-stat-module {
  background: rgb(var(--v-theme-surface)) !important;
  border-radius: 24px !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.06) !important;
}

.gateway-pro-card-large {
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08) !important;
}

.hub-header {
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.06) !important;
}

.hub-icon-box {
  width: 54px;
  height: 54px;
  background: rgba(var(--v-theme-primary), 0.06);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.op-60 {
  opacity: 0.6;
}

.access-capsule-modern {
  background: rgba(var(--v-theme-on-surface), 0.02);
  border-radius: 20px;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.05);
  transition: all 0.3s ease;
}

.access-capsule-modern:hover {
  background: rgba(var(--v-theme-primary), 0.04);
  border-color: rgba(var(--v-theme-primary), 0.2) !important;
}

.access-icon-box-modern {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.access-capsule-modern:hover .access-icon-box-modern {
  background: rgb(var(--v-theme-primary)) !important;
}

.access-capsule-modern:hover .access-icon-box-modern i {
  color: white !important;
}

.access-arrow-btn-modern {
  background: rgba(var(--v-theme-on-surface), 0.04) !important;
  transition: all 0.3s ease;
}

.access-capsule-modern:hover .access-arrow-btn-modern {
  background: rgb(var(--v-theme-primary)) !important;
  color: white !important;
}

.stagger-item {
  opacity: 1;
}
</style>
