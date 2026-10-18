<template>
  <v-main class="standalone-main">
    <!-- Geometric Background Pattern -->
    <div class="bg-pattern-overlay"></div>

    <v-container fluid class="pa-0 relative-content d-flex flex-column overflow-auto">
      <!-- 1. Institutional Master Header -->
      <header class="dashboard-hero-portal-pure flex-shrink-0 mb-8 mb-md-12">
        <div class="portal-inner pa-6 pa-md-8 max-width-safe mx-auto">
          <v-row align="center" no-gutters>
            <v-col cols="12" md="7">
              <div class="welcome-container-pure d-flex align-center ga-4 ga-md-5">
                <div class="institutional-avatar-refined">
                  <v-icon size="30" color="white">mdi-account-tie</v-icon>
                </div>

                <div
                  class="greeting-content-pure ps-4 ps-md-6 d-flex flex-column justify-center"
                  style="border-inline-start: 1px solid rgba(255, 255, 255, 0.15)"
                >
                  <div class="top-meta d-flex align-center ga-2 mb-2">
                    <span
                      class="text-overline font-weight-black text-white-soft"
                      style="
                        font-size: 0.65rem !important;
                        letter-spacing: 1.5px;
                        opacity: 0.8;
                      "
                    >
                      {{ isAr ? "بوابة الوصول الآمن" : "SECURE ACCESS PORTAL" }}
                    </span>
                  </div>
                  <h1 class="welcome-heading-pure" style="line-height: 1 !important">
                    <span
                      class="text-white-op-60 font-weight-light"
                      style="font-size: 1.2rem !important"
                    >
                      {{ isAr ? "نظام الإدارة الموحد" : "Unified Management System" }}
                      <span class="mx-2">|</span>
                    </span>
                    <span
                      class="font-weight-black text-white"
                      style="font-size: 1.6rem !important; letter-spacing: -0.5px"
                      >{{ userName }}</span
                    >
                  </h1>
                </div>
              </div>
            </v-col>

            <v-col
              cols="12"
              md="5"
              class="mt-4 mt-md-0 d-flex justify-start justify-md-end"
            >
              <div
                class="status-summary-pure d-flex align-center ga-3 w-100 w-md-auto justify-space-between justify-md-end"
              >
                <div class="meta-item d-flex flex-column align-start">
                  <span
                    class="text-overline text-white-op-70 mb-1"
                    style="font-size: 0.55rem !important; letter-spacing: 1px"
                  >
                    {{ isAr ? "الأنظمة المتاحة" : "AVAILABLE SYSTEMS" }}
                  </span>
                  <v-chip
                    size="x-small"
                    variant="flat"
                    color="rgba(255,255,255,0.15)"
                    class="text-white font-weight-black px-3"
                  >
                    {{ uniqueSystems.length }} {{ isAr ? "أنظمة" : "Systems" }}
                  </v-chip>
                </div>
                <v-divider
                  vertical
                  length="24"
                  color="white"
                  class="opacity-20 mx-1"
                ></v-divider>
                <!-- <v-btn variant="tonal" color="white" size="small" class="rounded-lg px-4 font-weight-black" @click="handleLogout">
                   {{ isAr ? 'تسجيل خروج' : 'Sign Out' }}
                </v-btn> -->
              </div>
            </v-col>
          </v-row>
        </div>
      </header>

      <v-container
        class="systems-grid-container pb-16 px-4 px-sm-6 px-md-12 max-width-safe w-100"
      >
        <!-- Search Bar Row -->
        <v-row class="mb-8 align-center">
          <v-col cols="12" md="8">
            <div class="section-header-refined d-flex align-center">
              <div class="hub-icon-container">
                <v-icon color="primary" size="32">mdi-dots-grid</v-icon>
              </div>
              <div class="header-separator mx-5"></div>
              <div class="d-flex flex-column">
                <h2 class="text-h5 font-weight-black title-premium">
                  {{ isAr ? "بوابات الأنظمة المتاحة" : "Available System Portals" }}
                </h2>
                <p class="text-body-2 mb-0 font-weight-medium op-60">
                  {{
                    isAr
                      ? "اختر الوجهة المطلوبة للبدء في إدارة العمليات الإدارية"
                      : "Select your destination to start managing administrative operations"
                  }}
                </p>
              </div>
            </div>
          </v-col>
          <v-col cols="12" md="4" class="d-flex justify-md-end align-center mt-4 mt-md-0">
            <v-text-field
              v-model="searchQuery"
              :placeholder="isAr ? 'ابحث...' : 'Search...'"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-magnify"
              class="search-bar-unified w-100"
              hide-details
              color="primary"
            ></v-text-field>
          </v-col>
        </v-row>

        <div class="py-4 py-md-6"></div>

        <!-- Loading State -->
        <v-row v-if="loading">
          <v-col v-for="n in 4" :key="n" cols="12" sm="6" md="4" lg="3">
            <v-skeleton-loader
              type="card"
              class="identity-stat-module rounded-xl"
              elevation="0"
              height="280"
            ></v-skeleton-loader>
          </v-col>
        </v-row>

        <!-- Error State -->
        <v-row v-else-if="error" justify="center" class="py-12">
          <v-col cols="12" sm="8" md="6">
            <v-alert type="error" variant="tonal" class="rounded-xl" prominent>
              <template v-slot:prepend>
                <v-icon size="28">mdi-alert-circle-outline</v-icon>
              </template>
              <v-alert-title class="font-weight-bold mb-1">{{
                isAr ? "حدث خطأ" : "An error occurred"
              }}</v-alert-title>
              {{ error }}
              <template v-slot:append>
                <v-btn
                  variant="text"
                  color="error"
                  class="font-weight-black"
                  @click="fetchSystems"
                >
                  {{ isAr ? "إعادة المحاولة" : "Try Again" }}
                </v-btn>
              </template>
            </v-alert>
          </v-col>
        </v-row>

        <!-- Empty Results Message -->
        <div
          v-else-if="uniqueSystems.length === 0 && !loading && !error"
          class="py-12 stagger-item"
        >
          <v-card
            class="identity-stat-module rounded-xl pa-12 max-w-700 mx-auto border-dashed-premium"
            elevation="0"
          >
            <NotFound />
          </v-card>
        </div>

        <!-- No Search Results Message -->
        <div
          v-else-if="filteredSystems.length === 0 && !loading && !error"
          class="py-12 stagger-item"
        >
          <v-card
            class="identity-stat-module rounded-xl pa-10 max-w-700 mx-auto border-dashed-premium"
            elevation="0"
          >
            <NotFound />
            <div class="text-center mt-n6">
              <v-btn
                variant="tonal"
                color="primary"
                class="rounded-lg px-8 font-weight-black h-44"
                @click="searchQuery = ''"
              >
                <v-icon start class="me-2">mdi-refresh</v-icon>
                {{ isAr ? "عرض كافة الأنظمة" : "Show all systems" }}
              </v-btn>
            </div>
          </v-card>
        </div>

        <!-- Systems Cards Grid -->
        <v-row v-else class="mt-4">
          <v-col
            v-for="(system, index) in filteredSystems"
            :key="system.system_name"
            cols="12"
            sm="6"
            md="4"
            lg="3"
            class="stagger-item mb-6"
          >
            <v-card
              class="identity-stat-module h-100 pa-6 pa-md-8 d-flex flex-column gateway-pro-card"
              elevation="0"
              @click="openSystem(system)"
              :disabled="system?.url === 'disable'"
            >
              <div class="card-accent-line"></div>

              <div class="d-flex align-start justify-space-between mb-4">
                <div class="module-icon-portal portal-executive">
                  <v-icon size="28" color="primary">{{
                    getSystemIcon(system.role)
                  }}</v-icon>
                </div>
                <v-chip
                  v-if="originUrl(system?.url)"
                  size="small"
                  variant="outlined"
                  color="primary"
                  class="font-weight-bold px-3"
                >
                  {{ isAr ? "النظام الحالي" : "Current System" }}
                </v-chip>
                <v-chip
                  v-else-if="system.url === 'disable'"
                  size="small"
                  variant="outlined"
                  color="error"
                  class="font-weight-bold px-3"
                >
                  {{ isAr ? "غير متوفر" : "Unavailable" }}
                </v-chip>
              </div>

              <div class="system-text-content flex-grow-1">
                <h3
                  class="text-h6 font-weight-black mb-2"
                  style="line-height: 1.3; color: rgb(var(--v-theme-on-surface))"
                >
                  {{ system.system_name }}
                </h3>
                <p
                  class="text-caption font-weight-medium mb-0"
                  style="line-height: 1.5; color: rgba(var(--v-theme-on-surface), 0.6)"
                >
                  {{
                    isAr
                      ? "إدارة العمليات الخاصة بالنظام، والوصول إلى كافة الخدمات والمهام المرتبطة به."
                      : "Manage system operations and access all related services and tasks."
                  }}
                </p>
              </div>

              <v-divider class="my-5" style="opacity: 0.08"></v-divider>

              <div class="d-flex align-center justify-space-between mt-auto">
                <span
                  class="text-button font-weight-bold"
                  style="color: rgba(var(--v-theme-primary), 1)"
                >
                  {{ isAr ? "دخول للنظام" : "Enter System" }}
                </span>
                <v-btn
                  icon
                  variant="tonal"
                  size="small"
                  color="primary"
                  class="access-arrow-btn"
                  elevation="0"
                >
                  <v-icon size="18">{{
                    isAr ? "mdi-arrow-left" : "mdi-arrow-right"
                  }}</v-icon>
                </v-btn>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <footer class="portal-footer-refined py-12 mt-16 text-center border-t">
        <v-container>
          <p class="text-caption text-slate-400 font-weight-bold">
            {{
              isAr
                ? "بوابة الوصول الآمن الموحدة © 2026 | كافة الحقوق محفوظة"
                : "Unified Secure Access Portal © 2026 | All Rights Reserved"
            }}
          </p>
        </v-container>
      </footer>
    </v-container>
  </v-main>
</template>

<script setup>
import { ref, computed, getCurrentInstance, onMounted } from "vue";
import { useAuthStore } from "../stores/auth";
import { ssoApi } from "../api/sso";
// import { useRouter } from "vue-router";
import { state } from "@/../src/store/state";
import { getRouter } from "../../router/routerInstance";
// import NotFound from "@/../components/other/NotFound.vue";

const router = getRouter();

// const router = useRouter();
const authStore = useAuthStore();
const instance = getCurrentInstance();

const isAr = computed(() => {
  try {
    return instance?.proxy?.$i18n?.locale === "ar" || true;
  } catch {
    return true;
  }
});

const userName = computed(
  () => state?.profile?.username || (isAr.value ? "المستخدم" : "User")
);

const systems = ref([]);
const loading = ref(true);
const error = ref(null);
const searchQuery = ref("");
const currentUrl = window.location.origin;

const ROLE_ICONS = {
  "access-login-role-control": "mdi-shield-cog-outline",
  "access-login-role-enterprise-resource-planning": "mdi-database-settings-outline",
  "access-login-role-portal": "mdi-monitor-dashboard",
  "access-login-role-school": "mdi-town-hall",
  "access-login-role-university-management-system": "mdi-bank-outline",
};

function getSystemIcon(role) {
  return ROLE_ICONS[role] || "mdi-view-grid-outline";
}

const uniqueSystems = computed(() => {
  if (!Array.isArray(systems.value)) return [];
  const seen = new Set();
  return systems.value.filter((system) => {
    const isDuplicate = seen.has(system.system_name);
    seen.add(system.system_name);
    return !isDuplicate;
  });
});

const filteredSystems = computed(() => {
  if (!searchQuery.value) return uniqueSystems.value;
  return uniqueSystems.value.filter((s) =>
    s.system_name?.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

async function fetchSystems() {
  loading.value = true;
  error.value = null;
  try {
    const response = await ssoApi.getAllowedSystems();
    systems.value = response.data || response || [];
  } catch (err) {
    console.error("Fetch failed:", err);
    error.value =
      err.response?.data?.message ||
      (isAr.value ? "فشل في جلب الأنظمة المتاحة" : "Failed to fetch available systems");
  } finally {
    loading.value = false;
  }
}

function openSystem(system) {
  if (system.url !== "disable" && system.url) {
    const origin = originUrl(system.url) || null;
    if (origin) {
      // window.location.href = "/";
      router.push("/");
    } else window.open(system.url, "_blank", "noopener,noreferrer");
  }
}

function originUrl(url) {
  if (url && url !== "disable") {
    try {
      return new URL(url).origin === currentUrl;
    } catch {
      return false;
    }
  }
  return false;
}

const handleLogout = async () => {
  await authStore.logout();
};
onMounted(() => {
  fetchSystems();
});
</script>

<style scoped>
.standalone-main {
  background: #f8fafc !important;
  min-height: 100vh;
  font-family: "Tajawal", sans-serif !important;
  position: relative;
}

:deep(.v-theme--dark) .standalone-main {
  background: #0f172a !important;
}

.max-width-safe {
  max-width: 1440px !important;
  margin: 0 auto !important;
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
}

.relative-content {
  position: relative;
  z-index: 1;
}

.dashboard-hero-portal-pure {
  background: linear-gradient(
    135deg,
    rgb(var(--v-theme-primary)) 0%,
    rgba(var(--v-theme-primary), 0.8) 100%
  );
  border-radius: 0 0 32px 32px;
  box-shadow: 0 10px 30px rgba(var(--v-theme-primary), 0.2);
  width: 100%;
}

.institutional-avatar-refined {
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.25);
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
  padding: 10px 20px;
  border-radius: 16px;
}

.hub-icon-container {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-separator {
  width: 1.5px;
  height: 30px;
  background: rgba(var(--v-theme-primary), 0.2);
}

.title-premium {
  color: rgb(var(--v-theme-on-surface));
  letter-spacing: -0.5px;
  line-height: 1.2;
  margin: 0 !important;
}

.op-60 {
  opacity: 0.6;
}

.identity-stat-module {
  background: rgb(var(--v-theme-surface)) !important;
  border-radius: 16px !important;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.06) !important;
  transition: all 0.2s ease-out;
}

.gateway-pro-card:hover {
  transform: translateY(-2px);
  border-color: rgba(var(--v-theme-on-surface), 0.1) !important;
}

.border-dashed-premium {
  border: 2px dashed rgba(var(--v-theme-on-surface), 0.1) !important;
  background: rgba(var(--v-theme-surface), 0.5) !important;
  backdrop-filter: blur(8px);
}

.h-44 {
  height: 44px !important;
}

.card-accent-line {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: rgba(var(--v-theme-primary), 0.7);
  transition: width 0.3s ease;
}

.gateway-pro-card:hover .card-accent-line {
  width: 100%;
}

.module-icon-portal {
  width: 54px;
  height: 54px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--v-theme-on-surface), 0.02);
}

.access-arrow-btn {
  background: rgba(var(--v-theme-primary), 0.05) !important;
}

.search-bar-unified {
  max-width: 400px;
}
:deep(.search-bar-unified .v-field) {
  border-radius: 12px !important;
}
</style>
