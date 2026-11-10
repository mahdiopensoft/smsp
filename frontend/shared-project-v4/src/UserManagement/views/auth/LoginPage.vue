<template>
  <div class="login-page-bg">
    <!-- Ultra-HD Background System -->
    <div class="background-system" v-if="backGround">
      <div class="bg-image" :style="{ backgroundImage: `url(${backGround})` }"></div>
      <div class="bg-blur"></div>
      <div class="bg-ambient-blobs">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
      </div>
      <div class="bg-gradient-overlay"></div>
    </div>
    <div class="background-system default-bg" v-else>
      <div class="bg-blur"></div>
      <div class="bg-ambient-blobs">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
      </div>
      <div class="bg-gradient-overlay"></div>
    </div>

    <!-- Main Content -->
    <div class="login-card">
      <div class="form-wrapper">
        <div class="form-content">
          <div class="form-header">
            <div class="logo-wrapper">
              <div class="logo-circle">
                <img
                  v-if="logo"
                  :src="logo"
                  alt="Logo"
                  class="app-logo"
                />
                <v-icon v-else size="48" color="var(--accent-gold)">mdi-shield-account</v-icon>
              </div>
            </div>

            <div class="brand-titles">
              <h2 class="org-title">
                {{ currentLang === "ar" ? (props.title || "الجمهورية اليمنية") : (props.titleEn || "Republic of Yemen") }}
              </h2>
              <h3 class="ministry-title">
                {{ currentLang === "ar" ? (props.subtitle || "وزارة التربية والتعليم والبحث العلمي") : (props.subtitleEn || "Ministry of Education & Scientific Research") }}
              </h3>
              <h1 class="system-title">
                {{ currentLang === "ar" ? (props.systemName || "نظام بنك الأسئلة والمستودع الاختباري") : (props.systemNameEn || "Question Bank & Assessment System") }}
              </h1>
              <p class="form-subtitle">
                {{ currentLang === "ar" ? "تسجيل الدخول إلى النظام" : "Sign in to your account" }}
              </p>
            </div>

            <div class="warning-box" v-if="securityReason && isAlertVisible">
              <v-icon size="20" color="#92400E">mdi-information-outline</v-icon>
              <span>{{ securityReason }}</span>
            </div>
          </div>

          <!-- MFA Verification Step -->
          <MFAVerifyStep
            v-if="authStore.mfaPending"
            @verified="onMFAVerified"
            @back="onMFABack"
          />

          <form
            v-if="!authStore.mfaPending"
            class="login-form"
            @submit.prevent="handelLogin"
          >
            <div class="floating-input">
              <input
                type="text"
                id="userid"
                v-model="username"
                placeholder=" "
                :class="{ 'has-error': errors.username }"
                @input="clearFieldError('username')"
                required
              />
              <label for="userid">{{
                currentLang === "ar" ? "اسم المستخدم" : "Username"
              }}</label>
              <v-icon class="input-icon" size="20">mdi-account-outline</v-icon>
              <span v-if="errors.username" class="error-text">{{
                errors.username
              }}</span>
            </div>

            <div class="floating-input">
              <input
                :type="showPass ? 'text' : 'password'"
                id="password"
                v-model="userPassword"
                placeholder=" "
                :class="{ 'has-error': errors.password }"
                @input="clearFieldError('password')"
                required
              />
              <label for="password">{{
                currentLang === "ar" ? "كلمة السر" : "Password"
              }}</label>
              <v-icon class="input-icon" size="20">mdi-lock-outline</v-icon>
              <button
                type="button"
                class="toggle-password"
                :aria-label="
                  currentLang === 'ar' ? 'إظهار كلمة المرور' : 'Show password'
                "
                @click="showPass = !showPass"
              >
                <v-icon size="20">{{
                  !showPass ? "mdi-eye-outline" : "mdi-eye-off-outline"
                }}</v-icon>
              </button>
              <span v-if="errors.password" class="error-text">{{
                errors.password
              }}</span>
            </div>

            <button
              type="submit"
              class="submit-btn"
              :class="{ 'is-sending': isLoading || loadingBtn }"
              :disabled="isLoading || loadingBtn"
            >
              <span class="btn-text">{{
                currentLang === "ar" ? "تسجيل الدخول" : "Sign In"
              }}</span>
              <v-icon class="btn-arrow" size="20">mdi-arrow-left</v-icon>
              <div class="loader"></div>
            </button>

           
         
            
            <v-sheet v-if="hasSSO==true">
               <!-- SSO Loading State -->
            <!-- تم التعديل: استبدال v-progress-circular بدائرة تحميل مخصصة بـ CSS (.custom-spinner) -->
            <div
              class="text-center py-2"
              v-if="configLoading"
              style="text-align: center"
            >
              <div class="custom-spinner"></div>
              <p
                class="text-grey mt-2"
                style="font-size: 13px; color: var(--text-gray)"
              >
                {{
                  currentLang === "ar"
                    ? "جاري تحميل إعدادات المصادقة..."
                    : "Loading auth settings..."
                }}
              </p>
            </div>

            <!-- SSO Error State -->
              <!-- تم التعديل: العودة لاستخدام v-icon للأخطاء -->
              <div v-if="errorConfig" style="text-align: center">
                <div
                  class="mb-2"
                  style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: var(--error);
                  "
                >
                  <v-icon size="20" class="me-2"
                    >mdi-alert-circle-outline</v-icon
                  >
                  <span style="font-size: 13px">
                    {{
                      currentLang === "ar"
                        ? "فشل في جلب اعدادات تسجيل الدخول"
                        : "Failed to load auth settings"
                    }}
                  </span>
                </div>
                <button
                  type="button"
                  @click="getConfig"
                  class="secondary-btn"
                  style="
                    padding: 8px;
                    width: 100%;
                    border-color: var(--error);
                    color: var(--error);
                  "
                >
                  {{ currentLang === "ar" ? "إعادة المحاولة" : "Retry" }}
                </button>
              </div>

              <template v-if="authConfig.showSSOLogin">
                <div class="divider">
                  <span>{{ currentLang === "ar" ? "أو" : "OR" }}</span>
                </div>

                <button
                  type="button"
                  class="secondary-btn w-100"
                  @click="$router.push({ name: 'SSOLogin' })"
                  :disabled="isLoading"
                  
                >
                  {{
                    currentLang === "ar"
                      ? "الدخول عبر المنصة الموحدة SSO"
                      : "Login via Unified Portal SSO"
                  }}
                  <v-icon size="20" class="ms-2">mdi-web</v-icon>
                </button>
              </template>
            </v-sheet>
          </form>

          <div class="support-contact">
            <!-- Language Switcher -->
            <div
              class="footer-language-switcher"
              style="
                margin-top: 15px;
                display: flex;
                justify-content: center;
                gap: 10px;
              "
            >
              <button
                type="button"
                class="footer-lang-btn"
                :style="
                  currentLang === 'ar'
                    ? 'color: var(--primary-blue); font-weight: bold; background: none; border: none; cursor: pointer;'
                    : 'color: var(--text-gray); background: none; border: none; cursor: pointer;'
                "
                @click="switchLanguage('ar')"
              >
                العربية
              </button>
              <span style="color: var(--border-light)">|</span>
              <button
                type="button"
                class="footer-lang-btn"
                :style="
                  currentLang === 'en'
                    ? 'color: var(--primary-blue); font-weight: bold; background: none; border: none; cursor: pointer;'
                    : 'color: var(--text-gray); background: none; border: none; cursor: pointer;'
                "
                @click="switchLanguage('en')"
              >
                English
              </button>
            </div>
    <div class="login-footer mt-5">
      <div class="divider-line"></div>
      <slot name="bootom" />
    </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useAuthConfigStore } from "../../stores/authConfig";
import { useRoute } from "vue-router";
import { useAuthStore } from "../../stores/auth";
import { useI18n } from "vue-i18n";
import MFAVerifyStep from "../../views/auth/MFAVerifyStep.vue";

const emit = defineEmits(["afterLogin"]);
const { locale } = useI18n();
const currentLang = ref(locale?.value || "ar");

const route = useRoute();

const authConfig = useAuthConfigStore();
const authStore = useAuthStore();
const props = defineProps({
  backGround: String,
  logo: String,
  title: String,
  titleEn: String,
  subtitle: String,
  subtitleEn: String,
  systemName: String,
  systemNameEn: String,
  hasSSO: {
    type: Boolean,
    default: true,
  },
  loadingBtn: Boolean,
});

//=================== sso===================//
const configLoading = ref(false);
const errorConfig = ref(false);
const getConfig = async () => {
  try {
    errorConfig.value = false;
    configLoading.value = true;
    await authConfig.fetchConfig();
  } catch (err) {
    errorConfig.value = true;
    console.warn("Failed to fetch auth config, using defaults:", err);
  } finally {
    configLoading.value = false;
  }
};

//============= login ==============//
const username = ref("");
const userPassword = ref("");
const showPass = ref(false);
const isLoading = ref(false);
const isAlertVisible = ref(true); // إضافة: إدارة ظهور تنبيه الأمان المخصص (بديل لخاصية الإغلاق 'closable' في v-alert)

// Restored from loginbackup.vue
const usernameFocused = ref(false);
const passwordFocused = ref(false);
const remember_me = ref(false);
const errors = ref({
  username: "",
  password: "",
});

const switchLanguage = (lang) => {
  currentLang.value = lang;
  locale.value = lang; // Dynamically update the global Vue-i18n locale to trigger parent slots translation
  document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
  errors.value.username = "";
  errors.value.password = "";
};

const clearFieldError = (field) => {
  if (errors.value[field]) {
    errors.value[field] = "";
  }
};

const handelLogin = async () => {
  try {
    // Basic required validation restored from loginbackup.vue
    errors.value.username = "";
    errors.value.password = "";

    if (!username.value) {
      errors.value.username =
        currentLang.value === "ar"
          ? "اسم المستخدم مطلوب"
          : "Username is required";
    }

    if (!userPassword.value) {
      errors.value.password =
        currentLang.value === "ar"
          ? "كلمة المرور مطلوبة"
          : "Password is required";
    }

    if (errors.value.username || errors.value.password) {
      return;
    }

    if (isLoading.value) return;
    isLoading.value = true;

    const result = await authStore.login(username.value, userPassword.value);

    // If MFA is required, the MFAVerifyStep component will show automatically
    if (result && result.mfaRequired) {
      return;
    }

    emit("afterLogin");
  } finally {
    isLoading.value = false;
  }
};

//============= MFA ====================//
// Called when MFA verification succeeds
const onMFAVerified = () => {
  emit("afterLogin");
};

// Cancel MFA and go back to login form
const onMFABack = () => {
  authStore.mfaPending = false;
  authStore.mfaUsername = null;
};

//==================== other ====================//
const securityReason = computed(() => {
    const reason =( route &&  route.query) ? route.query.reason : null;
  if (!reason) return "";
  const msgs = {
    logout:
      currentLang.value === "ar"
        ? "تم تسجيل الخروج بنجاح"
        : "You have been logged out",
    session_expired:
      currentLang.value === "ar"
        ? "انتهت جلستك، يرجى تسجيل الدخول مجدداً"
        : "Session expired, please login again",
    SESSION_EXPIRED:
      currentLang.value === "ar"
        ? "انتهت جلستك بسبب عدم النشاط"
        : "Session expired due to inactivity",
    absolute_timeout:
      currentLang.value === "ar"
        ? "انتهت الجلسة، يرجى تسجيل الدخول مجدداً"
        : "Session expired, please login again",
    security:
      currentLang.value === "ar"
        ? "تم إنهاء الجلسة لأسباب أمنية"
        : "Session terminated for security reasons",
    password_changed:
      currentLang.value === "ar"
        ? "تم تغيير كلمة المرور، يرجى تسجيل الدخول مجدداً"
        : "Password changed, please login again",
    TOKEN_REUSE_DETECTED:
      currentLang.value === "ar"
        ? "تم اكتشاف نشاط مشبوه. تم إنهاء جميع الجلسات لحمايتك."
        : "Suspicious activity detected. All sessions terminated.",
  };
  return reason ? msgs[reason] || null : null;
});

onMounted(async () => {
  document.documentElement.dir = currentLang.value === "ar" ? "rtl" : "ltr";

  // Clear leftover auth state when arriving from logout/expiry redirect
 if (route && route.query?.reason) {
    authStore.clearAuth();
  }

  if (props.hasSSO) {getConfig();}
});
</script>

<style scoped>
.login-page-bg {
  --primary-navy: #0d47a1;
  --primary-blue: #1976d2;
  --accent-gold: #c5a059;
  --accent-hover: #a88647;
  --text-dark: #1e293b;
  --text-gray: #64748b;
  --bg-white: #ffffff;
  --bg-gray: #f8fafc;
  --border-light: #e2e8f0;
  --border-focus: #94a3b8;
  --error: #dc2626;
  --alert-bg: #eff6ff;
  --alert-text: #1d4ed8;
  --page-bg: #f8fafc;

  position: relative;
  display: flex;
  min-height: 100vh;
  align-items: center;
  justify-content: center;
  padding: 24px 16px;
  overflow: hidden;
  background-color: var(--page-bg);
  flex-direction: column;
  color: var(--text-dark);
  font-family: "Tajawal", "Inter", sans-serif;
}

.login-page-bg * {
  box-sizing: border-box;
  font-family: inherit;
}

/* ============================================
   ULTRA-HD BACKGROUND SYSTEM
   ============================================ */
.background-system {
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
}

.bg-image {
  position: absolute;
  inset: -20px;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.12;
  filter: blur(8px);
}

.bg-blur {
  position: absolute;
  inset: 0;
  background-color: rgba(248, 250, 252, 0.88);
  background-image:
    linear-gradient(to right, rgba(15, 23, 42, 0.025) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(15, 23, 42, 0.025) 1px, transparent 1px);
  background-size: 36px 36px;
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
  filter: blur(80px);
}

.blob-1 {
  top: -10%;
  left: -5%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(25, 118, 210, 0.14) 0%, transparent 70%);
}

.blob-2 {
  bottom: -15%;
  right: -5%;
  width: 550px;
  height: 550px;
  background: radial-gradient(circle, rgba(197, 160, 89, 0.18) 0%, transparent 70%);
}

.bg-gradient-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at center, transparent 35%, rgba(241, 245, 249, 0.7) 100%);
  pointer-events: none;
}

/* ============================================
   LOGIN CARD
   ============================================ */
.login-card {
  position: relative;
  z-index: 2;
  display: flex;
  width: 100%;
  background-color: rgba(255, 255, 255, 0.97);
  backdrop-filter: blur(16px);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(15, 32, 60, 0.12),
    0 0 0 1px rgba(25, 118, 210, 0.18);
  max-width: 480px;
  margin: 0 auto;
}

.form-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  flex: 1;
  padding: 38px 40px 32px;
}

.form-content {
  width: 100%;
  max-width: 400px;
}

.form-header {
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

/* ============================================
   EMBOSSED EMBLEM LOGO BADGE
   ============================================ */
.logo-wrapper {
  margin-bottom: 16px;
  display: flex;
  justify-content: center;
}

.logo-circle {
  width: 114px;
  height: 114px;
  padding: 12px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background:
    radial-gradient(circle at 30% 20%, rgba(255, 255, 255, 1), rgba(248, 250, 252, 0.95)),
    conic-gradient(from 210deg, rgba(25, 118, 210, 0.18), rgba(197, 160, 89, 0.35), rgba(25, 118, 210, 0.18));
  box-shadow:
    0 4px 16px rgba(15, 23, 42, 0.08),
    0 12px 30px rgba(197, 160, 89, 0.25);
  border: 2px solid rgba(197, 160, 89, 0.5);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.logo-circle:hover {
  transform: scale(1.03);
  box-shadow:
    0 8px 22px rgba(15, 23, 42, 0.12),
    0 16px 36px rgba(197, 160, 89, 0.32);
}

.app-logo {
  max-width: 100%;
  max-height: 90px;
  object-fit: contain;
  filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.14));
}

.brand-titles {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  margin-bottom: 4px;
}

.org-title {
  font-size: 1.02rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  letter-spacing: -0.2px;
}

.ministry-title {
  font-size: 0.86rem;
  font-weight: 600;
  color: #64748b;
  margin: 0;
}

.system-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--primary-navy);
  margin: 6px 0 2px;
  letter-spacing: -0.4px;
}

.form-subtitle {
  font-size: 0.82rem;
  color: #94a3b8;
  margin: 0;
}

.warning-box {
  background-color: #fffbeb;
  border: 1px solid #fde68a;
  padding: 10px 14px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
  color: #92400e;
  font-size: 0.85rem;
  font-weight: 500;
  text-align: right;
  width: 100%;
}
[dir="ltr"] .warning-box {
  text-align: left;
}

.warning-box svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.floating-input {
  position: relative;
  display: flex;
  align-items: center;
  margin-top: 5px;
}

.floating-input input {
  width: 100%;
  padding: 16px;
  padding-inline-start: 42px;
  border: 1px solid var(--border-light);
  border-radius: 6px;
  font-size: 1rem;
  color: var(--text-dark);
  background-color: transparent;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  outline: none;
}
.floating-input input:-webkit-autofill,
.floating-input input:-webkit-autofill:hover,
.floating-input input:-webkit-autofill:focus,
.floating-input input:-webkit-autofill:active {
  -webkit-box-shadow: 0 0 0 30px var(--bg-white) inset !important;
  -webkit-text-fill-color: 5000s ease-in-out 0s !important;
  transition: background-color 5000s ease-in-out 0s;
}

.floating-input input.has-error {
  border-color: var(--error);
  box-shadow: inset 0 0 0 1px var(--error);
}

.floating-input input[type="password"],
.floating-input input[type="text"]#password {
  padding-inline-end: 42px;
}

.floating-input label {
  position: absolute;
  inset-inline-start: 42px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  font-size: 1rem;
  font-weight: 500;
  pointer-events: none;
  background-color: var(--bg-white);
  padding: 0 6px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
}

.floating-input .input-icon {
  position: absolute;
  inset-inline-start: 14px;
  width: 20px;
  height: 20px;
  color: #94a3b8;
  transition: color 0.2s ease;
  z-index: 0;
}

.toggle-password {
  position: absolute;
  inset-inline-end: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
  z-index: 2;
  border-radius: 50%;
}

.toggle-password:hover {
  color: var(--primary-blue);
  background-color: rgba(0, 0, 0, 0.03);
}

.toggle-password svg {
  width: 20px;
  height: 20px;
}

.floating-input input:focus,
.floating-input input:not(:placeholder-shown) {
  border-color: var(--primary-blue);
  box-shadow: inset 0 0 0 1px var(--primary-blue);
}

.floating-input input:focus ~ label,
.floating-input input:not(:placeholder-shown) ~ label {
  top: 0;
  inset-inline-start: 25px;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--primary-blue);
}

.floating-input input:focus ~ .input-icon {
  color: var(--primary-blue);
}

.error-text {
  position: absolute;
  bottom: -20px;
  font-size: 0.8rem;
  color: var(--error);
  inset-inline-start: 5px;
}

.submit-btn {
  background-color: var(--primary-blue);
  color: var(--bg-white);
  border: none;
  border-radius: 6px;
  font-size: 1.05rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 10px;
  position: relative;
  width: 100%;
  height: 52px;
  max-width: 100%;
  overflow: hidden;
  transition: background-color 0.2s;
  align-self: center;
}

.submit-btn:hover:not(:disabled) {
  background-color: var(--primary-navy);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.submit-btn .btn-text,
.submit-btn .btn-arrow {
  transition: opacity 0.2s;
}

.submit-btn .btn-arrow {
  width: 18px;
  height: 18px;
  transform: scaleX(-1);
}
[dir="ltr"] .submit-btn .btn-arrow {
  transform: scaleX(1);
}

.submit-btn .loader {
  position: absolute;
  inset: 0;
  margin: auto;
  width: 24px;
  height: 24px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  opacity: 0;
}

.submit-btn.is-sending {
  pointer-events: none;
  animation: buttonProcess 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

@keyframes buttonProcess {
  0% {
    transform: scale(1);
    max-width: 100%;
    border-radius: 6px;
  }
  15% {
    transform: scale(1.03);
    max-width: 100%;
    border-radius: 6px;
  }
  30% {
    transform: scale(1);
    max-width: 100%;
    border-radius: 6px;
  }
  100% {
    transform: scale(1);
    max-width: 52px;
    border-radius: 50%;
  }
}

.submit-btn.is-sending .btn-text,
.submit-btn.is-sending .btn-arrow {
  opacity: 0;
}

.submit-btn.is-sending .loader {
  animation: fadeInSpinner 0.4s forwards, spin 0.4s linear infinite;
}

@keyframes fadeInSpinner {
  0%,
  60% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: var(--border-focus);
  font-size: 0.9rem;
  font-weight: 500;
  margin-top: 5px;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  border-bottom: 1px solid var(--border-light);
}

.divider span {
  padding: 0 15px;
}

.secondary-btn {
  background-color: transparent;
  color: var(--primary-blue);
  border: 1px solid var(--primary-blue);
  padding: 14px;
  border-radius: 6px;
  font-size: 1.05rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  transition: all 0.2s;
}

.secondary-btn:hover:not(:disabled) {
  background-color: var(--primary-blue);
  color: var(--bg-white);
}

.secondary-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.secondary-btn svg {
  width: 18px;
  height: 18px;
}

.support-contact {
  margin-top: 30px;
  text-align: center;
  font-size: 0.85rem;
  color: var(--text-gray);
  border-top: 1px solid var(--border-light);
  padding-top: 15px;
}

.support-contact a {
  color: var(--primary-navy);
  font-weight: 700;
  text-decoration: none;
}

.support-contact a:hover {
  text-decoration: underline;
}

.footer-copyright {
  color: var(--text-gray);
  font-size: 0.95rem;
  font-weight: 500;
  text-align: center;
}

/* إضافة: تنسيقات مخصصة للتنبيهات ودوائر التحميل كبديل لمكونات Vuetify */
.security-alert {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 12px 14px;
  border-radius: 6px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
  margin-top: 15px;
  width: 100%;
  font-size: 0.9rem;
  text-align: right;
}
[dir="ltr"] .security-alert {
  text-align: left;
}
.security-alert .alert-content {
  display: flex;
  align-items: center;
  gap: 8px;
}
.security-alert svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}
.close-alert {
  background: none;
  border: none;
  color: #dc2626;
  cursor: pointer;
  padding: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.7;
  transition: opacity 0.2s;
}
.close-alert:hover {
  opacity: 1;
}
.custom-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--border-light);
  border-top-color: var(--primary-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@media (max-width: 576px) {
  .login-page-bg {
    padding: 15px;
  }
  .form-wrapper {
    padding: 30px 20px;
  }
  .form-header h1 {
    font-size: 1.5rem;
  }
  .submit-btn,
  .secondary-btn {
    font-size: 1rem;
    padding: 12px;
  }
}
</style>
