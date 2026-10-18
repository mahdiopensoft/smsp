<template>
  <div class="login-split-layout">
    <!-- Right Side (in RTL): Blue Background with Branding -->
    <div class="form-side">
      <!-- Blue Curved Background (Convex) -->
      <div class="blue-curve-bg"></div>

      <!-- Faint Watermark Icon on Blue Side -->
      <v-icon class="watermark-icon form-watermark">mdi-school</v-icon>

      <!-- Language Switcher in top corner -->
      <div class="top-right-actions">
        <span
          class="lang-text"
          @click="switchLanguage('en')"
          :class="{ active: currentLang === 'en' }"
          >English</span
        >
        <span class="lang-separator">|</span>
        <span
          class="lang-text"
          @click="switchLanguage('ar')"
          :class="{ active: currentLang === 'ar' }"
          >العربية</span
        >
        <v-icon class="lang-icon">mdi-web</v-icon>
      </div>

      <div class="branding-content">
        <div class="branding-logo-wrapper">
          <div class="branding-logo">
            <img
              v-if="logo"
              :src="logo"
              alt="Logo"
              style="width: 100%; height: 100%; object-fit: contain; border-radius: 24px"
            />
            <svg
              v-else
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
              <path d="M2 17l10 5 10-5"></path>
              <path d="M2 12l10 5 10-5"></path>
            </svg>
          </div>
        </div>

        <h1 class="branding-title">
          {{
            currentLang === "ar" ? "نظام البوابة التعليمية" : "Educational Portal System"
          }}
        </h1>
        <h3 class="branding-subtitle">
          {{
            currentLang === "ar"
              ? "منصة موحدة لإدارة التعليم بكفاءة واحترافية"
              : "A unified platform to manage education efficiently"
          }}
        </h3>

        <div class="branding-divider"></div>

        <p class="branding-desc">
          <template v-if="currentLang === 'ar'">
            إدارة متكاملة للطلاب والمعلمين والمنشآت التعليمية
            <br />
            في بيئة واحدة آمنة وسهلة الاستخدام
          </template>
          <template v-else>
            Integrated management for students, teachers, and facilities
            <br />
            in a single secure and easy-to-use environment
          </template>
        </p>

        <!-- Feature Icons Row -->
        <div class="features-row">
          <div class="feature-item">
            <div class="feature-icon-circle">
              <v-icon>mdi-shield-check-outline</v-icon>
            </div>
            <span>{{ currentLang === "ar" ? "آمن وموثوق" : "Secure" }}</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon-circle"><v-icon>mdi-clock-fast</v-icon></div>
            <span>{{ currentLang === "ar" ? "سريع وسهل" : "Fast & Easy" }}</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon-circle">
              <v-icon>mdi-account-group-outline</v-icon>
            </div>
            <span>{{ currentLang === "ar" ? "متكامل وشامل" : "Comprehensive" }}</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon-circle"><v-icon>mdi-chart-line</v-icon></div>
            <span>{{ currentLang === "ar" ? "تقارير ذكية" : "Smart Reports" }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Left Side (in RTL): White Background with Login Form -->
    <div class="branding-side">
      <!-- Watermark Icons -->
      <v-icon class="watermark-icon mdi-school-watermark">mdi-account-school</v-icon>
      <v-icon class="watermark-icon mdi-book-watermark">mdi-book-open-variant</v-icon>

      <div class="login-card-wrapper">
        <div class="login-card">
          <div class="form-wrapper">
            <div class="form-content">
              <div class="form-header">
                <div class="logo">
                  <img
                    v-if="logo"
                    :src="logo"
                    alt="Logo"
                    style="
                      width: 100%;
                      height: 100%;
                      object-fit: contain;
                      border-radius: 16px;
                    "
                  />
                  <svg
                    v-else
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                    <path d="M2 17l10 5 10-5"></path>
                    <path d="M2 12l10 5 10-5"></path>
                  </svg>
                </div>
                <h1>{{ currentLang === "ar" ? "تسجيل الدخول" : "Login" }}</h1>
                <p class="login-subtitle">
                  {{
                    currentLang === "ar"
                      ? "مرحباً بك، الرجاء إدخال بياناتك للوصول إلى حسابك"
                      : "Welcome back, please enter your details."
                  }}
                </p>

                <div class="warning-box" v-if="securityReason && isAlertVisible">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="16" x2="12" y2="12"></line>
                    <line x1="12" y1="8" x2="12.01" y2="8"></line>
                  </svg>
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
                  <svg
                    class="input-icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
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
                    style="padding-inline-end: 42px"
                  />
                  <label for="password">{{
                    currentLang === "ar" ? "كلمة السر" : "Password"
                  }}</label>
                  <svg
                    class="input-icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                  </svg>
                  <button
                    type="button"
                    class="toggle-password"
                    :aria-label="
                      currentLang === 'ar' ? 'إظهار كلمة المرور' : 'Show password'
                    "
                    @click="showPass = !showPass"
                  >
                    <svg
                      v-if="!showPass"
                      class="eye-icon"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                    <svg
                      v-else
                      class="eye-off-icon"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"
                      ></path>
                      <line x1="1" y1="1" x2="23" y2="23"></line>
                    </svg>
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
                  <svg
                    class="btn-arrow"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                    <polyline points="12 5 19 12 12 19"></polyline>
                  </svg>
                  <div class="loader"></div>
                </button>

                <v-sheet v-if="hasSSO == true" style="background: transparent">
                  <!-- SSO Loading State -->
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
                      <v-icon size="20" class="me-2">mdi-alert-circle-outline</v-icon>
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
                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      >
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="2" y1="12" x2="22" y2="12"></line>
                        <path
                          d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"
                        ></path>
                      </svg>
                    </button>
                  </template>
                </v-sheet>
              </form>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-copyright-left">
        <slot name="bootom">
          {{
            currentLang === "ar"
              ? "جميع الحقوق محفوظة - نظام المنصة الموحدة 2026"
              : "All Rights Reserved - Unified Portal System 2026"
          }}
        </slot>
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

const route = useRoute();

const authConfig = useAuthConfigStore();
const authStore = useAuthStore();
const props = defineProps({
  backGround: String,
  logo: String,
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
        currentLang.value === "ar" ? "اسم المستخدم مطلوب" : "Username is required";
    }

    if (!userPassword.value) {
      errors.value.password =
        currentLang.value === "ar" ? "كلمة المرور مطلوبة" : "Password is required";
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
  const reason = route && route.query ? route.query.reason : null;
  if (!reason) return "";
  const msgs = {
    logout:
      currentLang.value === "ar" ? "تم تسجيل الخروج بنجاح" : "You have been logged out",
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

const currentLang = ref(locale.value || "ar");

onMounted(async () => {
  document.documentElement.dir = currentLang.value === "ar" ? "rtl" : "ltr";

  // Clear leftover auth state when arriving from logout/expiry redirect
  if (route && route.query?.reason) {
    authStore.clearAuth();
  }

  if (props.hasSSO) {
    getConfig();
  }
});
</script>

<style scoped>
.login-split-layout {
  --primary-navy: #0a398a;
  --primary-blue: #1363df;
  --primary-hover: #0e4db5;
  --accent-gold: #f59e0b;
  --text-dark: #1e293b;
  --text-gray: #64748b;
  --bg-white: #ffffff;
  --bg-gray: #f8fafc;
  --border-light: #e2e8f0;
  --border-focus: #1363df;
  --error: #dc2626;
  --alert-bg: #fef2f2;
  --alert-text: #b91c1c;

  display: flex;
  width: 100%;
  height: 100vh; /* ضروري لكي يعمل الـ scroll الداخلي */
  overflow-x: hidden;
  overflow-y: auto; /* تفعيل التمرير العمودي للأجهزة الصغيرة */
  font-family: "Tajawal", sans-serif;
  background-color: var(--bg-gray);
  color: var(--text-dark);
}

.login-split-layout * {
  box-sizing: border-box;
}

/* --- Left Side: Branding --- */
.branding-side {
  flex: 1;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
  background-image: radial-gradient(rgba(19, 99, 223, 0.12) 1.5px, transparent 1.5px);
  background-size: 28px 28px;
  z-index: 2;
}

.watermark-icon {
  position: absolute;
  pointer-events: none;
  z-index: -1;
}
.mdi-school-watermark {
  font-size: clamp(100px, 15vw, 220px) !important; /* تصغير الأيقونة وجعلها متجاوبة */
  color: rgba(19, 99, 223, 0.03);
  top: 10%;
  left: 5%;
}
.mdi-book-watermark {
  font-size: clamp(120px, 18vw, 280px) !important; /* تصغير الأيقونة وجعلها متجاوبة */
  color: rgba(19, 99, 223, 0.03);
  bottom: 5%;
  left: 5%;
}
.form-watermark {
  font-size: clamp(150px, 22vw, 320px) !important;
  color: rgba(255, 255, 255, 0.04);
  bottom: -5%;
  right: -5%;
  transform: rotate(-15deg);
  z-index: 1;
}
[dir="ltr"] .form-watermark {
  right: auto;
  left: -5%;
  transform: scaleX(-1) rotate(-15deg);
}

.branding-content {
  text-align: center;
  max-width: 600px;
  margin-bottom: 60px;
  position: relative;
  z-index: 10;
}

.branding-logo-wrapper {
  position: relative;
  margin: 0 auto 30px;
  display: flex;
  justify-content: center;
}
.branding-logo {
  width: 120px;
  height: 120px;
  background: var(--bg-white);
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-blue);
  box-shadow: 0 15px 35px rgba(10, 57, 138, 0.2);
}
.branding-logo svg {
  width: 60px;
  height: 60px;
}

.branding-title {
  font-size: 38px;
  font-weight: 800;
  color: var(--primary-navy);
  margin-bottom: 12px;
}
.branding-subtitle {
  font-size: 18px;
  color: var(--primary-blue);
  margin-bottom: 30px;
  font-weight: 700;
}
.branding-divider {
  width: 150px;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--primary-blue), transparent);
  margin: 0 auto 30px;
}
.branding-desc {
  font-size: 17px;
  color: var(--text-gray);
  line-height: 1.8;
  margin-bottom: 50px;
}

.features-row {
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
}
.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}
.feature-icon-circle {
  width: 55px;
  height: 55px;
  background: var(--bg-white);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(19, 99, 223, 0.1);
}
.feature-icon-circle .v-icon {
  font-size: 28px !important;
  color: var(--primary-blue);
}
.feature-item span {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-gray);
}

/* --- Right Side: Form --- */
.form-side {
  width: 50%;
  min-width: 480px;
  flex-shrink: 0;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1;
  padding: 40px;
  padding-inline-end: 2.5vw;
}

/* تم استخدام position: fixed هنا بذكاء بدلاً من absolute
 لمنع ظهور شريط تمرير عمودي طويل (200vh) وللسماح بالنزول الطبيعي للصفحة
 كما طلبت، مع الحفاظ على شكل المنحنى الأصلي بالضبط للديسكتوب والتابلت */
.blue-curve-bg {
  position: fixed;
  top: -50vh;
  bottom: -50vh;
  left: calc(100vw - max(50vw, 480px) - 5vw);
  right: -100vw;
  background: linear-gradient(
    to right,
    var(--primary-blue) 0%,
    #0d4ab5 25%,
    var(--primary-navy) 100%
  );
  border-radius: 50%;
  z-index: 0;
  border-left: 2px solid rgba(255, 255, 255, 0.35);
  box-shadow: inset 8px 0 20px rgba(255, 255, 255, 0.08),
    -10px 0 40px rgba(10, 57, 138, 0.15);
}

[dir="ltr"] .blue-curve-bg {
  left: -100vw;
  right: calc(100vw - max(50vw, 480px) - 5vw);
  background: linear-gradient(
    to left,
    var(--primary-blue) 0%,
    #0d4ab5 35%,
    var(--primary-navy) 100%
  );
  border-left: none;
  border-right: 2px solid rgba(255, 255, 255, 0.35);
  box-shadow: inset -8px 0 20px rgba(255, 255, 255, 0.08),
    10px 0 40px rgba(10, 57, 138, 0.15);
}

.top-right-actions {
  position: absolute;
  top: 30px;
  inset-inline-start: 40px;
  display: flex;
  align-items: center;
  gap: 16px;
  z-index: 10;
  color: rgba(255, 255, 255, 0.8);
}
.lang-text {
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: color 0.3s;
}
.lang-text:hover,
.lang-text.active {
  color: var(--bg-white);
  font-weight: 700;
}
.lang-separator {
  color: rgba(255, 255, 255, 0.4);
}
.lang-icon {
  font-size: 24px !important;
}

/* التموضع الذكي للبطاقة:
   استخدمنا inset-inline-start لدفعها فوق المنحنى بنسبة 45% تماماً مثل التصميم الأصلي
   هذا يحافظ على التصميم الأصلي 100% ويسمح بمرونة لا نهائية للزووم بدون position: absolute */
.login-card-wrapper {
  position: relative;
  inset-inline-start: -20vw;
  z-index: 100;
  width: 100%;
  max-width: 480px;
  transition: inset-inline-start 0.3s ease;
}

/* حل الموازنة لمنع التداخل الأفقي عند تكبير الشاشة (Zoom) أو استخدام أجهزة أصغر */
@media (max-width: 1600px) {
  .login-card-wrapper {
    inset-inline-start: -10vw; /* تقليل مسافة الدخول في المنطقة الزرقاء لتوفير مساحة للنص */
  }
}

@media (max-width: 1366px) {
  .login-card-wrapper {
    inset-inline-start: -2vw; /* مساحة أمان إضافية لضمان عدم ملامسة النصوص أبداً */
  }
}

.login-card {
  display: flex;
  width: 100%;
  background-color: var(--bg-white);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 15px 35px rgba(10, 57, 138, 0.2);
}

.form-wrapper {
  width: 100%;
  padding: 60px 48px 48px;
}

.form-header {
  margin-bottom: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.logo {
  width: 64px;
  height: 64px;
  background: var(--bg-white);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  color: var(--primary-blue);
  box-shadow: 0 10px 15px -3px rgba(19, 99, 223, 0.15);
}

.logo svg {
  width: 32px;
  height: 32px;
}

.form-header h1 {
  font-size: 28px;
  font-weight: 800;
  color: var(--text-dark);
  margin-bottom: 12px;
}

.login-subtitle {
  font-size: 15.5px;
  color: var(--text-gray);
  margin-bottom: 24px;
}

.warning-box {
  background-color: #fefce8;
  border: 1px solid #fef08a;
  padding: 12px 16px;
  border-radius: 10px;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-top: 10px;
  color: #a16207;
  font-size: 0.85rem;
  font-weight: 500;
  text-align: right;
  width: 100%;
  line-height: 1.5;
}
[dir="ltr"] .warning-box {
  text-align: left;
}

.warning-box svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  margin-top: 2px;
}

.footer-copyright {
  margin-top: 15px;
  text-align: center;
  color: #ffffff !important;
  font-size: 13.5px;
  z-index: 10;
}

.footer-copyright * {
  color: #ffffff !important;
}

@media (max-width: 1199px) {
  .form-side {
    min-width: 400px;
    padding: 40px;
  }
  .login-card-wrapper {
    max-width: 420px;
  }
  .branding-title {
    font-size: 30px;
  }
  .branding-subtitle {
    font-size: 16px;
  }
  .branding-desc {
    font-size: 15px;
  }
  .features-row {
    gap: 20px;
  }
  .feature-icon-circle {
    width: 45px;
    height: 45px;
  }
  .feature-icon-circle .v-icon {
    font-size: 24px !important;
  }
}

@media (max-width: 992px) {
  .login-split-layout {
    flex-direction: column;
  }
  .form-side {
    width: 100%;
    min-width: 100%;
    padding: 25px 20px 15px; /* تقليل حجم البوكس الأزرق بشكل كبير */
  }
  .blue-curve-bg {
    position: absolute;
    border-radius: 0;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    box-shadow: none;
  }
  .branding-content {
    margin-bottom: 10px;
  }
  .branding-title {
    font-size: 24px;
    margin-bottom: 5px;
  }
  .branding-desc {
    margin-bottom: 15px;
  }
  .features-row {
    display: none;
  }

  .branding-side {
    width: 100%;
    padding: 15px;
    padding-bottom: 50px; /* مساحة كافية لنص الحقوق المحفوظة */
    justify-content: flex-start;
  }
  .login-card-wrapper {
    inset-inline-start: 0; /* إلغاء التداخل في الشاشات الصغيرة */
    margin: 0 auto;
    width: 100%;
  }
  .top-right-actions {
    inset-inline-start: 20px;
    top: 20px;
  }
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
  padding: 18px;
  padding-inline-start: 46px; /* Icon on the left */
  padding-inline-end: 46px; /* Eye icon on the right */
  border: 1.5px solid var(--border-light);
  border-radius: 12px;
  font-size: 1.15rem;
  color: var(--text-dark);
  background-color: transparent;
  transition: border-color 0.2s ease;
  outline: none;
}
.floating-input input:-webkit-autofill,
.floating-input input:-webkit-autofill:hover,
.floating-input input:-webkit-autofill:focus,
.floating-input input:-webkit-autofill:active {
  -webkit-box-shadow: 0 0 0 30px var(--bg-white) inset !important;
  -webkit-text-fill-color: var(--text-dark) !important;
  transition: background-color 5000s ease-in-out 0s;
}

.floating-input input.has-error {
  border-color: var(--error);
}

.floating-input label {
  position: absolute;
  inset-inline-start: 46px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  font-size: 1.05rem;
  font-weight: 500;
  pointer-events: none;
  background-color: var(--bg-white);
  padding: 0 6px;
  transition: top 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    inset-inline-start 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    font-size 0.2s cubic-bezier(0.4, 0, 0.2, 1), color 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
}

.floating-input .input-icon {
  position: absolute;
  inset-inline-start: 16px;
  width: 22px;
  height: 22px;
  color: #94a3b8;
  transition: color 0.2s ease;
  z-index: 0;
}

.toggle-password {
  position: absolute;
  inset-inline-end: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
  z-index: 2;
  border-radius: 50%;
}

.toggle-password:hover {
  color: var(--primary-blue);
  background-color: rgba(19, 99, 223, 0.05);
}

.toggle-password svg {
  width: 22px;
  height: 22px;
}

.floating-input input:focus,
.floating-input input:not(:placeholder-shown),
.floating-input input:-webkit-autofill {
  border-color: var(--primary-blue);
}

.floating-input input:focus ~ label,
.floating-input input:not(:placeholder-shown) ~ label,
.floating-input input:-webkit-autofill ~ label {
  top: 0;
  inset-inline-start: 25px;
  font-size: 0.9rem;
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
  border-radius: 12px;
  font-size: 1.2rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 10px;
  position: relative;
  width: 100%;
  height: 60px;
  max-width: 100%;
  transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s;
  align-self: center;
  box-shadow: 0 4px 6px -1px rgba(19, 99, 223, 0.2);
}

.submit-btn:hover:not(:disabled) {
  background-color: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(19, 99, 223, 0.3);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.submit-btn .btn-text,
.submit-btn .btn-arrow {
  transition: opacity 0.2s, transform 0.3s;
}

.submit-btn .btn-arrow {
  width: 20px;
  height: 20px;
  transform: scaleX(-1);
}
[dir="ltr"] .submit-btn .btn-arrow {
  transform: scaleX(1);
}

.submit-btn:hover:not(:disabled) .btn-arrow {
  transform: scaleX(-1) translateX(-4px);
}
[dir="ltr"] .submit-btn:hover:not(:disabled) .btn-arrow {
  transform: scaleX(1) translateX(4px);
}

.submit-btn.is-sending {
  pointer-events: none;
  background-color: var(--primary-hover);
  box-shadow: 0 0 0 4px rgba(19, 99, 223, 0.2);
}

.submit-btn.is-sending .btn-text,
.submit-btn.is-sending .btn-arrow {
  opacity: 0;
  transform: translateY(-10px);
}

.submit-btn.is-sending .loader {
  opacity: 1;
  transform: translateY(0) scale(0.6);
}

.submit-btn .loader {
  position: absolute;
  inset: 0;
  margin: auto;
  width: 44.8px;
  height: 44.8px;
  color: #ffffff;
  opacity: 0;
  transform: translateY(10px) scale(0.6);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  contain: layout;
}

.submit-btn .loader:after {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(11.2px, currentColor 94%, #0000);
  animation: pulseCenter 0.5s infinite alternate ease-in-out;
  will-change: opacity, transform;
}

@keyframes pulseCenter {
  0% {
    opacity: 0.4;
    transform: scale(0.7);
  }
  100% {
    opacity: 1;
    transform: scale(1.15);
  }
}

.submit-btn .loader:before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(10.08px at bottom right, #0000 94%, currentColor) top left,
    radial-gradient(10.08px at bottom left, #0000 94%, currentColor) top right,
    radial-gradient(10.08px at top right, #0000 94%, currentColor) bottom left,
    radial-gradient(10.08px at top left, #0000 94%, currentColor) bottom right;
  background-size: 22.4px 22.4px;
  background-repeat: no-repeat;
  animation: bociLoader 3s infinite cubic-bezier(0.4, 0, 0.2, 1);
  will-change: inset, transform;
}

@keyframes bociLoader {
  15% {
    inset: -11.2px;
    transform: rotate(0deg);
  }
  85% {
    inset: -11.2px;
    transform: rotate(5400deg);
  }
  100% {
    inset: 0;
    transform: rotate(5400deg);
  }
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: var(--text-gray);
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
  border: 1.5px solid var(--primary-blue);
  padding: 14px;
  border-radius: 10px;
  font-size: 1.05rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  transition: background-color 0.2s, border-color 0.2s, transform 0.2s;
}

.secondary-btn:hover:not(:disabled) {
  background-color: rgba(19, 99, 223, 0.05);
  border-color: var(--primary-hover);
  color: var(--primary-hover);
  transform: translateY(-1px);
}

.secondary-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.secondary-btn svg {
  width: 20px;
  height: 20px;
  color: var(--primary-blue);
}

.support-contact {
  margin-top: 30px;
  text-align: center;
  font-size: 0.9rem;
  color: var(--text-gray);
  border-top: 1px solid var(--border-light);
  padding-top: 20px;
}

.support-contact a {
  color: var(--primary-blue);
  font-weight: 700;
  text-decoration: none;
}

.support-contact a:hover {
  text-decoration: underline;
}

/* Custom Spinner for SSO */
.custom-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--border-light);
  border-radius: 50%;
  border-top-color: var(--primary-blue);
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 576px) {
  .form-side {
    padding: 55px 15px 10px; /* زيادة المسافة العلوية لترك مجال لمبدل اللغة */
  }
  .branding-side {
    padding: 10px 15px 45px; /* تقليل المساحة فوق البطاقة، وترك مساحة بالأسفل للحقوق */
  }
  .form-wrapper {
    padding: 20px 15px 15px;
  }
  .form-header h1 {
    font-size: 1.4rem;
    margin-bottom: 8px;
  }
  .login-subtitle {
    font-size: 13px;
    margin-bottom: 15px;
  }
  .login-form {
    gap: 15px; /* تقليل المسافة بين الحقول */
  }
  .floating-input input {
    padding: 12px;
    padding-inline-start: 42px;
    padding-inline-end: 42px;
    font-size: 0.95rem;
  }
  .submit-btn,
  .secondary-btn {
    font-size: 1rem;
    padding: 10px;
    height: 45px;
    margin-top: 5px;
  }
  .branding-logo {
    width: 70px;
    height: 70px;
    margin-bottom: 5px;
  }
  .branding-title {
    font-size: 20px;
    margin-bottom: 5px;
  }
  .branding-subtitle {
    font-size: 13px;
    margin-bottom: 5px;
  }
  .branding-desc {
    font-size: 12px;
    line-height: 1.4;
    margin-bottom: 5px;
  }
  .logo {
    width: 42px;
    height: 42px;
    margin-bottom: 10px;
  }
  .top-right-actions {
    inset-inline-start: 0;
    width: 100%; /* أخذ العرض بالكامل */
    justify-content: center; /* توسيط مبدل اللغة في المنتصف */
    top: 15px; /* تثبيته في الأعلى */
  }
  .footer-copyright-left {
    bottom: 10px;
    font-size: 12px;
  }
}

@media (max-width: 380px) {
  .form-wrapper {
    padding: 20px 15px;
  }
  .branding-logo {
    width: 60px;
    height: 60px;
  }
  .branding-title {
    font-size: 20px;
  }
}

@media (max-height: 600px) and (orientation: landscape) {
  .login-split-layout {
    flex-direction: row;
  }
  .form-side {
    display: none;
  }
  .branding-side {
    width: 100%;
  }
  .login-card-wrapper {
    position: relative;
    inset-inline-start: 0;
    margin: 20px auto;
  }
}

.form-side .branding-title,
.form-side .branding-subtitle,
.form-side .branding-desc,
.form-side .feature-item span {
  color: #ffffff !important;
}
.form-side .branding-divider {
  background: linear-gradient(90deg, transparent, #ffffff, transparent);
}
.form-side .branding-logo {
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}
.footer-copyright-left {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  color: var(--primary-blue);
  font-size: 14px;
  font-weight: 700;
  text-align: center;
  width: 100%;
}
</style>
