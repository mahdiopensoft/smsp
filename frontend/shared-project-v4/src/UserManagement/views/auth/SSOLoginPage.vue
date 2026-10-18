<template>
  <div class="login-page">
    <!-- Ultra-HD Background System -->
    <div class="background-system">
      <div class="bg-image" :style="{ backgroundImage: `url(${bg})` }"></div>
      <div class="bg-blur"></div>
      <div class="bg-ambient-blobs">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
      </div>
      <div class="bg-gradient-overlay"></div>
    </div>

    <!-- Main Content -->
    <div class="content-wrapper">
      <div class="login-card-container">
        <!-- Sleek Minimalist Centered Vertical Card -->
        <div class="minimal-auth-card sso-vertical-card">
          <!-- Cyber Blueprint Matrix Grid Overlay for Card Backing -->
          <div class="branding-overlay"></div>

          <!-- Logo Section -->
          <div class="minimal-logo-wrapper">
            <v-img :src="logo" class="minimal-logo" alt="University Logo"></v-img>
          </div>

          <!-- Header Section -->
          <div class="form-side-header text-center">
            <h1 class="form-title">
              {{
                currentLang === "ar"
                  ? "تسجيل الدخول الموحد (SSO)"
                  : "Single Sign-On (SSO)"
              }}
            </h1>
            <p class="form-subtitle">
              {{
                currentLang === "ar"
                  ? "الدخول الآمن والسريع عبر البوابة التعليمية الموحدة"
                  : "Secure and rapid authentication via the unified educational portal"
              }}
            </p>
          </div>

          <!-- SSO Content Area -->
          <div class="sso-content">
            <template v-if="loading">
              <div class="loading-state">
                <div class="loader-primary"></div>
                <p class="loading-text">
                  {{
                    currentLang === "ar"
                      ? "جاري التوجيه إلى خادم المصادقة..."
                      : "Redirecting to authentication server..."
                  }}
                </p>
              </div>
            </template>

            <template v-else-if="error">
              <div class="error-state">
                <div class="error-alert">
                  <v-icon color="rgb(var(--v-theme-error))" size="24" class="me-2"
                    >mdi-alert-circle</v-icon
                  >
                  <span>{{ error }}</span>
                </div>

                <div class="action-buttons-column">
                  <button type="button" class="login-btn" @click="initiateSSO(false)">
                    <v-icon start size="20" class="me-2">mdi-refresh</v-icon>
                    <span>{{ currentLang === "ar" ? "إعادة المحاولة" : "Retry" }}</span>
                  </button>
                  <button
                    type="button"
                    class="sso-secondary-btn"
                    @click="initiateSSO(true)"
                  >
                    <v-icon start size="18" class="me-2">mdi-open-in-new</v-icon>
                    <span>{{
                      currentLang === "ar"
                        ? "فتح في نافذة منبثقة"
                        : "Open in a new window"
                    }}</span>
                  </button>
                </div>
              </div>
            </template>

            <template v-else>
              <div class="action-buttons-column">
                <button type="button" class="login-btn" @click="initiateSSO(false)">
                  <v-icon start size="22" class="me-2">mdi-key</v-icon>
                  <span>{{
                    currentLang === "ar"
                      ? "الدخول عبر المنصة الموحدة"
                      : "Login via Unified Platform"
                  }}</span>
                </button>

                <router-link :to="{ name: 'Login' }" class="back-link mt-4">
                  <v-icon start size="18" class="me-1">mdi-arrow-left</v-icon>
                  <span>{{
                    currentLang === "ar" ? "العودة للدخول العادي" : "Back to normal login"
                  }}</span>
                </router-link>
              </div>
            </template>
          </div>

          <!-- Footer -->
          <div class="login-footer">
            <div class="divider-line"></div>

            <!-- Integrated Footer Language Switcher (macOS Pill style) -->
            <div class="footer-language-switcher">
              <button
                type="button"
                class="footer-lang-btn"
                :class="{ active: currentLang === 'ar' }"
                @click="switchLanguage('ar')"
              >
                العربية
              </button>
              <button
                type="button"
                class="footer-lang-btn"
                :class="{ active: currentLang === 'en' }"
                @click="switchLanguage('en')"
              >
                English
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore, AUTH_MODES } from "../../stores/auth";
import { ssoApi } from "../../api/sso";
import { useI18n } from "vue-i18n";
import settings from "@/../settings";

// Asset Imports for visual harmony
import logo from "@/assets/logo.png";

const router = useRouter();
const authStore = useAuthStore();
const { locale } = useI18n();

const loading = ref(false);
const error = ref(null);

// Client credentials
const CLIENT_ID = "web";
const API_BASE = settings.url;

let popupWindow = null;
let popupCheckInterval = null;
const currentLang = ref(locale.value || "ar");

const switchLanguage = (lang) => {
  currentLang.value = lang;
  locale.value = lang; // Globally sync locale state
  document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
};

/**
 * Open SSO login in a popup window
 */
const openPopup = (url) => {
  const width = 500;
  const height = 700;
  const left = window.screenX + (window.outerWidth - width) / 2;
  const top = window.screenY + (window.outerHeight - height) / 2;

  const features = [
    `width=${width}`,
    `height=${height}`,
    `left=${left}`,
    `top=${top}`,
    "scrollbars=yes",
    "resizable=yes",
    "status=yes",
    "toolbar=no",
    "menubar=no",
    "location=yes",
  ].join(",");

  popupWindow = window.open(url, "sso_login", features);

  if (!popupWindow || popupWindow.closed) {
    error.value =
      currentLang.value === "ar"
        ? "تم حظر النافذة المنبثقة. يرجى السماح بالنوافذ المنبثقة في متصفحك."
        : "Popup blocked. Please enable popups in your browser settings.";
    loading.value = false;
    return false;
  }

  popupWindow.focus();
  startPopupMonitor();

  return true;
};

/**
 * Monitor popup window for auth completion
 */
const startPopupMonitor = () => {
  popupCheckInterval = setInterval(() => {
    try {
      if (!popupWindow || popupWindow.closed) {
        stopPopupMonitor();
        loading.value = false;
        if (authStore.isAuthenticated) {
          router.push("/");
        }
        return;
      }

      const popupUrl = popupWindow.location.href;

      if (popupUrl.includes("/auth/callback")) {
        const url = new URL(popupUrl);
        const accessToken = url.searchParams.get("access_token");
        const refreshToken = url.searchParams.get("refresh_token");
        const errorParam = url.searchParams.get("error");

        popupWindow.close();
        stopPopupMonitor();

        if (errorParam) {
          error.value = url.searchParams.get("description") || errorParam;
          loading.value = false;
          return;
        }

        if (accessToken) {
          handleTokensReceived(accessToken, refreshToken);
        }
      }
    } catch (e) {
      // Cross-origin error expected while on external domain
    }
  }, 500);
};

const stopPopupMonitor = () => {
  if (popupCheckInterval) {
    clearInterval(popupCheckInterval);
    popupCheckInterval = null;
  }
};

const handleTokensReceived = async (accessToken, refreshToken) => {
  try {
    authStore.setTokens(accessToken, refreshToken, AUTH_MODES.SSO_KEYCLOAK);
    await authStore.fetchSSOUserInfo();
    loading.value = false;
    router.push("/");
  } catch (err) {
    error.value =
      currentLang.value === "ar"
        ? "فشل في معالجة رمز الوصول"
        : "Failed to process access token";
    loading.value = false;
  }
};

const initiateSSO = async (usePopup = false) => {
  loading.value = true;
  error.value = null;

  try {
    const { client_id, timestamp, signature } = await ssoApi.generateClientSignature();
    const ssoUrl = `${API_BASE}sso/login/?client_id=${client_id}&timestamp=${timestamp}&signature=${signature}`;
    if (usePopup) {
      openPopup(ssoUrl);
    } else {
      window.location.href = ssoUrl;
    }
  } catch (err) {
    console.log(err);
    error.value =
      currentLang.value === "ar"
        ? "فشل في إنشاء التوقيع الأمني"
        : "Failed to generate security signature";
    loading.value = false;
  }
};

const handlePopupMessage = (event) => {
  if (event.origin !== window.location.origin) return;

  const { type, token, refreshToken } = event.data || {};

  if (type === "sso_success" && token) {
    handleTokensReceived(token, refreshToken);
    if (popupWindow) popupWindow.close();
    stopPopupMonitor();
  } else if (type === "sso_error") {
    error.value =
      event.data.error ||
      (currentLang.value === "ar"
        ? "حدث خطأ أثناء تسجيل الدخول"
        : "An error occurred during login");
    loading.value = false;
    if (popupWindow) popupWindow.close();
    stopPopupMonitor();
  }
};

onMounted(() => {
  window.addEventListener("message", handlePopupMessage);
  document.documentElement.dir = currentLang.value === "ar" ? "rtl" : "ltr";
});

onUnmounted(() => {
  window.removeEventListener("message", handlePopupMessage);
  stopPopupMonitor();
  if (popupWindow && !popupWindow.closed) {
    popupWindow.close();
  }
});
</script>

<style scoped>
/* --- Core Reset & Base --- */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-page {
  min-height: 100vh;
  width: 100%;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ============================================
   4K PROFESSIONAL BACKGROUND SYSTEM
   ============================================ */
.background-system {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.bg-image {
  position: absolute;
  inset: -12px;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.85;
  filter: blur(4px); /* Premium photographic bokeh depth effect */
}

.bg-blur {
  position: absolute;
  inset: 0;
  background-color: rgba(var(--v-theme-background), 0.72);
  background-image: linear-gradient(
      to right,
      rgba(var(--v-theme-on-surface), 0.015) 1px,
      transparent 1px
    ),
    linear-gradient(
      to bottom,
      rgba(var(--v-theme-on-surface), 0.015) 1px,
      transparent 1px
    ); /* Fine draft blueprint grid pattern */
  background-size: 44px 44px;
}

.bg-ambient-blobs {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 1;
}

.blob {
  position: absolute;
  border-radius: 50%;
  will-change: transform;
}

.blob-1 {
  top: -10%;
  left: -5%;
  width: 500px;
  height: 500px;
  background: radial-gradient(
    circle,
    rgba(var(--v-theme-primary), 0.12) 0%,
    transparent 70%
  );
}

.blob-2 {
  bottom: -15%;
  right: -5%;
  width: 600px;
  height: 600px;
  background: radial-gradient(
    circle,
    rgba(var(--v-theme-primary), 0.12) 0%,
    transparent 70%
  );
}

.blob-3 {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 800px;
  height: 500px;
  background: radial-gradient(
    circle,
    rgba(var(--v-theme-primary), 0.16) 0%,
    transparent 60%
  );
}

.bg-gradient-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at 50% 50%,
    rgba(var(--v-theme-background), 0.1) 0%,
    rgba(var(--v-theme-background), 0.65) 100%
  );
  z-index: 2;
  pointer-events: none;
}

/* ============================================
   MAIN CONTENT WRAPPER
   ============================================ */
.content-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 500px; /* Crisp tight width for a beautiful vertical card */
  padding: 24px;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.login-card-container {
  width: 100%;
}

/* ============================================
   SLEEK CENTERED VERTICAL CARD
   ============================================ */
.sso-vertical-card {
  position: relative;
  background: rgba(var(--v-theme-surface), 0.98); /* 98% opacity for ambient bleed */
  border-radius: 24px;
  border: 1.2px solid rgba(var(--v-theme-on-surface), 0.07);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.035);
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 48px 40px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.branding-overlay {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(
      circle at 50% 25%,
      rgba(var(--v-theme-primary), 0.09) 0%,
      transparent 60%
    ),
    linear-gradient(to right, rgba(var(--v-theme-on-surface), 0.015) 1px, transparent 1px),
    linear-gradient(
      to bottom,
      rgba(var(--v-theme-on-surface), 0.015) 1px,
      transparent 1px
    );
  background-size: 100% 100%, 20px 20px, 20px 20px;
  opacity: 0.85;
  z-index: 1;
}

.minimal-logo-wrapper {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  z-index: 2;
  width: 100%;
}

.minimal-logo {
  max-height: 120px; /* Crisp and perfectly proportioned in vertical view */
  width: auto;
  object-fit: contain;
}

.form-side-header {
  width: 100%;
  margin-bottom: 28px;
  z-index: 2;
}

.form-title {
  font-size: 26px;
  font-weight: 900;
  color: rgb(var(--v-theme-on-surface));
  margin-bottom: 8px;
  letter-spacing: -0.5px;
}

.form-subtitle {
  font-size: 13.5px;
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface), 0.48);
  line-height: 1.5;
}

/* --- SSO Specifics --- */
.sso-content {
  width: 100%;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.action-buttons-column {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 16px;
}

.login-btn {
  width: 100%;
  height: 54px;
  background: rgb(var(--v-theme-primary));
  color: rgb(var(--v-theme-on-primary));
  font-size: 16px;
  font-weight: 700;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: 0.3px;
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.16),
    inset 0 1.5px 0 rgba(255, 255, 255, 0.22), inset 0 -1.5px 0 rgba(0, 0, 0, 0.12);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.login-btn:hover {
  filter: brightness(1.05);
  box-shadow: 0 6px 18px rgba(var(--v-theme-primary), 0.22),
    inset 0 1.5px 0 rgba(255, 255, 255, 0.3), inset 0 -1.5px 0 rgba(0, 0, 0, 0.16);
}

.login-btn:active {
  filter: brightness(0.93);
  box-shadow: 0 2px 4px rgba(var(--v-theme-primary), 0.1),
    inset 0 1.5px 3px rgba(0, 0, 0, 0.2);
}

.sso-secondary-btn {
  width: 100%;
  height: 54px;
  background: transparent;
  color: rgb(var(--v-theme-primary));
  font-size: 15px;
  font-weight: 600;
  border: 1.5px solid rgba(var(--v-theme-primary), 0.3);
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.sso-secondary-btn:hover {
  background: rgba(var(--v-theme-primary), 0.04);
  border-color: rgb(var(--v-theme-primary));
}

.back-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: rgba(var(--v-theme-on-surface), 0.55);
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  padding: 8px 16px;
  border-radius: 8px;
  align-self: center;
}

.back-link:hover {
  color: rgb(var(--v-theme-on-surface));
  background: rgba(var(--v-theme-on-surface), 0.04);
}

/* --- Loader and states --- */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 0;
  width: 100%;
}

.loader-primary {
  width: 44px;
  height: 44px;
  border: 3.5px solid rgba(var(--v-theme-primary), 0.1);
  border-left-color: rgb(var(--v-theme-primary));
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 18px;
}

.loading-text {
  color: rgba(var(--v-theme-on-surface), 0.6);
  font-size: 14px;
  font-weight: 600;
  text-align: center;
}

.error-state {
  width: 100%;
}

.error-alert {
  display: flex;
  align-items: center;
  background: rgba(var(--v-theme-error), 0.04);
  border: 1px solid rgba(var(--v-theme-error), 0.2);
  color: rgb(var(--v-theme-error));
  padding: 14px 16px;
  border-radius: 12px;
  margin-bottom: 24px;
  font-size: 14px;
  font-weight: 600;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* ============================================
   FOOTER - Enhanced Contrast
   ============================================ */
.login-footer {
  margin-top: 36px;
  text-align: center;
  width: 100%;
  z-index: 2;
}

.divider-line {
  height: 1px;
  background: linear-gradient(
    to right,
    transparent 0%,
    rgba(var(--v-theme-on-surface), 0.1) 15%,
    rgba(var(--v-theme-on-surface), 0.1) 85%,
    transparent 100%
  );
  margin-bottom: 18px;
}

.footer-language-switcher {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
  margin-top: 14px;
  padding: 3px;
  background: rgba(var(--v-theme-on-surface), 0.04);
  border-radius: 24px;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.04);
}

.footer-lang-btn {
  background: none;
  border: none;
  font-size: 11px;
  font-weight: 600;
  color: rgba(var(--v-theme-on-surface), 0.55);
  cursor: pointer;
  padding: 5px 12px;
  border-radius: 20px;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.footer-lang-btn:hover {
  color: rgb(var(--v-theme-on-surface));
}

.footer-lang-btn.active {
  color: rgb(var(--v-theme-primary)) !important;
  font-weight: 700;
  background: rgb(var(--v-theme-surface));
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

/* ============================================
   RESPONSIVE DESIGN (All Screen Sizes)
   ============================================ */
@media (max-width: 480px) {
  .content-wrapper {
    max-width: 100%;
    padding: 12px;
  }

  .sso-vertical-card {
    border-radius: 16px;
    padding: 36px 24px;
  }

  .form-side-header {
    margin-bottom: 20px;
  }

  .form-title {
    font-size: 22px;
  }

  .form-subtitle {
    font-size: 12px;
  }

  .minimal-logo-wrapper {
    margin-bottom: 16px;
  }

  .minimal-logo {
    max-height: 90px;
  }

  .footer-language-switcher {
    margin-top: 10px;
    padding: 3px 6px;
  }

  .footer-lang-btn {
    font-size: 11px;
    padding: 3px 8px;
  }

  .login-btn,
  .sso-secondary-btn {
    height: 48px;
    font-size: 14px;
    border-radius: 8px;
  }
}
</style>
