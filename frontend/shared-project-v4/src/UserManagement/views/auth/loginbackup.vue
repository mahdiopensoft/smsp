<template>
  <div class="login-page">
    <!-- Ultra-HD Background System -->
    <div class="background-system">
      <div class="bg-image"></div>
      <div class="bg-blur"></div>
      <div class="bg-gradient-overlay"></div>
    </div>

    <!-- Language Switcher - Top Right -->
    <div class="language-switcher">
      <button class="lang-btn" :class="{ active: currentLang === 'ar' }" @click="switchLanguage('ar')">
        العربية
      </button>
      <span class="lang-divider">|</span>
      <button class="lang-btn" :class="{ active: currentLang === 'en' }" @click="switchLanguage('en')">
        English
      </button>
    </div>

    <!-- Main Content -->
    <div class="content-wrapper">
      <div class="login-card-container">

        <!-- Premium White Card -->
        <div class="university-card">
          <div class="card-content">

            <!-- Header Section -->
            <div class="header-section">
              <div class="logo-wrapper">
                <div class="logo-circle">
                  <img :src="logoImage" alt="University Logo" class="app-logo" />
                </div>
              </div>
              <h1 class="university-title">
                {{ currentLang === 'ar' ? 'نظام إدارة الجامعة' : 'University Management System' }}
              </h1>
              <p class="university-subtitle">
                {{ currentLang === 'ar' ? 'مرحباً بك في نظام إدارة الجامعة' : 'Welcome to the University Management System' }}
              </p>
            </div>

            <!-- Login Form -->
            <VForm ref="form" @submit.prevent="handelLogin" class="login-form">

              <!-- User ID Field -->
              <div class="input-group">
                <div class="floating-input" :class="{ 'has-value': username, 'is-focused': usernameFocused }">
                  <div class="input-icon-wrapper">
                    <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke-linecap="round"
                        stroke-linejoin="round" />
                      <circle cx="12" cy="7" r="4" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </div>
                  <input type="text" v-model="username" class="premium-input" :class="{ 'has-error': errors.username }"
                    @focus="usernameFocused = true" @blur="usernameFocused = false" @input="clearFieldError('username')"
                    required />
                  <label class="floating-label">{{ currentLang === 'ar' ? 'اسم المستخدم' : 'Username' }}</label>
                </div>
                <p v-if="errors.username" class="error-message">{{ errors.username }}</p>
              </div>

              <!-- Password Field -->
              <div class="input-group">
                <div class="floating-input" :class="{ 'has-value': password, 'is-focused': passwordFocused }">
                  <div class="input-icon-wrapper">
                    <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke-linecap="round"
                        stroke-linejoin="round"></path>
                    </svg>
                  </div>
                  <input :type="showPass ? 'text' : 'password'" v-model="password" class="premium-input"
                    :class="{ 'has-error': errors.password }" @focus="passwordFocused = true"
                    @blur="passwordFocused = false" @input="clearFieldError('password')" required />
                  <label class="floating-label">{{ currentLang === 'ar' ? 'كلمة المرور' : 'Password' }}</label>
                  <button type="button" class="password-toggle" @click="showPass = !showPass">
                    <svg v-if="!showPass" class="toggle-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                      stroke-width="1.5">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke-linecap="round"
                        stroke-linejoin="round" />
                      <circle cx="12" cy="12" r="3" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                    <svg v-else class="toggle-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                      stroke-width="1.5">
                      <path
                        d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"
                        stroke-linecap="round" stroke-linejoin="round" />
                      <line x1="1" y1="1" x2="23" y2="23" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </button>
                </div>
                <p v-if="errors.password" class="error-message">{{ errors.password }}</p>
              </div>

              <!-- Actions Row -->
              <div class="action-row">
                <label class="custom-checkbox">
                  <input type="checkbox" v-model="remember_me" />
                  <span class="checkmark"></span>
                  <span class="checkbox-label">{{ currentLang === 'ar' ? 'تذكرني' : 'Remember me' }}</span>
                </label>
                <a href="#" class="forgot-link">{{ currentLang === 'ar' ? 'هل نسيت كلمة المرور؟' : 'Forgot Password?'
                }}</a>
              </div>

              <!-- Login Button -->
              <button type="submit" class="login-btn" :disabled="isLoading">
                <span v-if="!isLoading">{{ currentLang === 'ar' ? 'تسجيل الدخول' : 'Sign In' }}</span>
                <div v-else class="loader"></div>
              </button>

            </VForm>

            <!-- Footer -->
            <div class="login-footer">
              <div class="divider-line"></div>
              <p class="copyright-text">
                <span v-if="currentLang === 'ar'">
                  جميع الحقوق محفوظة - نظام إدارة الجامعة {{ new Date().getFullYear() }}
                </span>
                <span v-else>
                  All Rights Reserved - University Management System {{ new Date().getFullYear() }}
                </span>
              </p>
            </div>

          </div>
        </div>
      </div>
    </div>

    <!-- Alert Component -->
    <alert v-model="alert.show" :iconColor="alert.alert_icon_color" :icon="alert.alert_icon" :title="alert.alert_title"
      :message="alert.alert_message" :sub_message="alert.alert_sub_message" class="custom-alert" />
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import logoImage from "@/assets/logo.png";
const route = useRoute();
const company = route.params.company;
</script>

<script>
import shared from "external-components";

export default {
  data() {
    return {
      alert: {
        show: false,
      },
      username: null,
      password: null,
      remember_me: false,
      showPass: false,
      isLoading: false,
      logoImage: logoImage,
      currentLang: 'ar',
      usernameFocused: false,
      passwordFocused: false,
      errors: {
        username: '',
        password: '',
      },
    };
  },

  methods: {
    switchLanguage(lang) {
      this.currentLang = lang;
      document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
      // Clear validation messages when switching language
      this.errors.username = '';
      this.errors.password = '';
    },
    clearFieldError(field) {
      if (this.errors[field]) {
        this.errors[field] = '';
      }
    },
    async handelLogin() {
      // Reset previous errors
      this.errors.username = '';
      this.errors.password = '';

      // Basic required validation with bilingual messages
      if (!this.username) {
        this.errors.username = this.currentLang === 'ar'
          ? 'اسم المستخدم مطلوب'
          : 'Username is required';
      }

      if (!this.password) {
        this.errors.password = this.currentLang === 'ar'
          ? 'كلمة المرور مطلوبة'
          : 'Password is required';
      }

      // Stop submit if there are validation errors
      if (this.errors.username || this.errors.password) {
        return;
      }

      this.isLoading = true;
      try {
        const e = await shared.api.post("user-manager/token/", {
          username: this.username,
          password: this.password,
        });
        const data = e.data;
        localStorage.setItem("token", data.access);
        const redirect = this.$route.query.redirect || "/";
        window.location.href = redirect;
      } catch (error) {
        console.error(error);
        if (error.status === 400) alert(error?.response?.data.detail);
        else
          alert(
            this.currentLang == "ar"
              ? "خطأ في الاتصال بالبوابة"
              : "Connection Error"
          );
      } finally {
        this.isLoading = false;
      }
    },
  },

  mounted() {
    document.documentElement.dir = this.currentLang === 'ar' ? 'rtl' : 'ltr';
  }
};
</script>

<style scoped>
/* ============================================
   ULTRA-HD 4K UNIVERSITY LOGIN SCREEN
   Premium Corporate Academic Design
   ============================================ */

@import url('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;500;600;700;800&display=swap');

/* --- Core Reset & Base --- */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-page {
  font-family: 'Inter Tight', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
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
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.bg-image {
  position: absolute;
  inset: -20px;
  background-image: url('/university_atrium.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  transform: scale(1.05);
}

.bg-blur {
  position: absolute;
  inset: 0;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}

/* Dark-tinted overlay for white card contrast */
.bg-gradient-overlay {
  position: absolute;
  inset: 0;
  background: rgba(173, 181, 189, 0.2);
  /* Soft Cool-Grey Overlay */
}

/* ============================================
   LANGUAGE SWITCHER
   ============================================ */
.language-switcher {
  position: fixed;
  top: 32px;
  right: 40px;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.95);
  padding: 10px 20px;
  border-radius: 50px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  backdrop-filter: blur(10px);
}

.lang-btn {
  background: none;
  border: none;
  font-family: 'Inter Tight', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  padding: 6px 14px;
  border-radius: 20px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  letter-spacing: 0.3px;
}

.lang-btn:hover {
  color: #1e40af;
  background: rgba(59, 130, 246, 0.08);
}

.lang-btn.active {
  background: #1e40af;
  color: white;
  font-weight: 600;
}

.lang-divider {
  color: #cbd5e1;
  font-weight: 300;
}

/* ============================================
   MAIN CONTENT WRAPPER
   ============================================ */
.content-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 540px;
  padding: 28px;
}

.login-card-container {
  width: 100%;
}

/* ============================================
   SOLID WHITE PREMIUM CARD - 8K Ultra-Clean
   ============================================ */
.university-card {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #E5E4E2;
  /* Ultra-sharp 1px platinum border */
  /* 2px Visual Anchor - University Brand Color */
  border-top: 2px solid #2563eb;
  border-left: none;
  border-right: none;
  border-bottom: none;
  /* Multi-layered Ambient Occlusion Shadow - Natural Floating */
  box-shadow:
    /* Tight contact shadow */
    0 0 1px rgba(0, 0, 0, 0.04),
    0 1px 2px rgba(0, 0, 0, 0.04),
    /* Mid-range ambient */
    0 2px 4px rgba(0, 0, 0, 0.03),
    0 4px 8px rgba(0, 0, 0, 0.03),
    /* Soft spread */
    0 8px 16px rgba(0, 0, 0, 0.03),
    0 16px 32px rgba(0, 0, 0, 0.04),
    /* Deep ambient occlusion */
    0 32px 48px rgba(0, 0, 0, 0.05),
    0 48px 80px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition:
    transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1),
    box-shadow 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.university-card:hover {
  transform: translateY(-5px);
  box-shadow:
    0 0 1px rgba(0, 0, 0, 0.04),
    0 1px 2px rgba(0, 0, 0, 0.04),
    0 2px 4px rgba(0, 0, 0, 0.03),
    0 4px 8px rgba(0, 0, 0, 0.04),
    0 12px 24px rgba(0, 0, 0, 0.05),
    0 24px 48px rgba(0, 0, 0, 0.06),
    0 48px 80px rgba(0, 0, 0, 0.08),
    0 64px 100px rgba(0, 0, 0, 0.08);
}

.card-content {
  padding: 60px 56px 56px;
}

/* ============================================
   HEADER SECTION - High Contrast Typography
   ============================================ */
.header-section {
  text-align: center;
  margin-bottom: 48px;
}

.logo-wrapper {
  margin-bottom: 28px;
}

.logo-circle {
  width: 104px;
  height: 104px;
  padding: 14px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background:
    radial-gradient(circle at 30% 20%, rgba(255, 255, 255, 0.9), rgba(248, 250, 252, 0.95)),
    conic-gradient(from 210deg, rgba(37, 99, 235, 0.18), rgba(234, 179, 8, 0.18), rgba(37, 99, 235, 0.18));
  box-shadow:
    0 3px 10px rgba(15, 23, 42, 0.10),
    0 10px 30px rgba(15, 23, 42, 0.12);
  border: 1px solid rgba(226, 232, 240, 0.9);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.logo-circle:hover {
  transform: scale(1.02);
  box-shadow:
    0 6px 16px rgba(15, 23, 42, 0.14),
    0 14px 32px rgba(15, 23, 42, 0.14);
}

.app-logo {
  max-width: 100%;
  max-height: 64px;
  object-fit: contain;
  image-rendering: -webkit-optimize-contrast;
}

/* High-Contrast Dark Grey Typography */
.university-title {
  font-family: 'Inter Tight', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #36454F;
  /* Bold Charcoal */
  letter-spacing: 1.2px;
  margin-bottom: 10px;
  line-height: 1.2;
}

.university-subtitle {
  font-family: 'Inter Tight', sans-serif;
  font-size: 15px;
  font-weight: 400;
  color: #A9A9A9;
  /* Light-muted grey */
  letter-spacing: 0.1px;
  line-height: 1.6;
}

/* ============================================
   LOGIN FORM
   ============================================ */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* --- Clean Outlined Input System --- */
.input-group {
  position: relative;
}

.error-message {
  margin-top: 4px;
  font-size: 12px;
  color: #ef4444;
  /* Red for errors */
  font-weight: 500;
}

[dir="rtl"] .error-message {
  text-align: right;
}

.floating-input {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon-wrapper {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

[dir="rtl"] .input-icon-wrapper {
  left: auto;
  right: 16px;
}

.input-icon {
  width: 20px;
  height: 20px;
  color: #94a3b8;
  opacity: 0.3;
  /* 30% opacity */
  transition: all 0.25s ease;
}

.floating-input.is-focused .input-icon {
  color: #2563eb;
  /* University Blue */
  opacity: 1;
  filter: drop-shadow(0 0 3px rgba(37, 99, 235, 0.5));
  /* Glow effect */
}

/* Clean Outlined Input with 5% Inner-Tint for Carved Depth */
.premium-input {
  width: 100%;
  height: 54px;
  padding: 16px 16px 16px 50px;
  font-family: 'Inter Tight', sans-serif;
  font-size: 15px;
  font-weight: 500;
  color: #1e293b;
  background: #F8F9FA;
  /* Soft-Grey */
  border: 1px solid #E5E4E2;
  /* Ultra-sharp 1px platinum border */
  border-radius: 14px;
  outline: none;
  transition: all 0.25s ease;
  letter-spacing: 0.1px;
  /* Subtle inner shadow for carved effect */
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.02);
}

.premium-input.has-error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15);
}

[dir="rtl"] .premium-input {
  padding: 16px 50px 16px 16px;
}

.premium-input::placeholder {
  color: transparent;
}

.premium-input:hover {
  border-color: #cbd5e1;
  background: rgba(248, 250, 252, 0.8);
}

/* Vibrant University Blue Focus State */
.premium-input:focus {
  border-color: #4169E1;
  /* Royal Blue */
  background: #ffffff;
  box-shadow:
    0 0 0 4px rgba(65, 105, 225, 0.2);
  /* 4px soft outer glow */
}

/* --- Floating Label --- */
.floating-label {
  position: absolute;
  left: 50px;
  top: 50%;
  transform: translateY(-50%);
  font-family: 'Inter Tight', sans-serif;
  font-size: 15px;
  font-weight: 400;
  color: #6b7280;
  /* Muted label */
  pointer-events: none;
  transition: all 0.25s ease;
  background: transparent;
  padding: 0 4px;
}

[dir="rtl"] .floating-label {
  left: auto;
  right: 50px;
}

.floating-input.is-focused .floating-label,
.floating-input.has-value .floating-label {
  top: 0;
  transform: translateY(-50%);
  font-size: 12px;
  font-weight: 500;
  color: #2563eb;
  background: #ffffff;
  left: 12px;
}

[dir="rtl"] .floating-input.is-focused .floating-label,
[dir="rtl"] .floating-input.has-value .floating-label {
  left: auto;
  right: 12px;
}

/* --- Password Toggle --- */
.password-toggle {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  padding: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: background-color 0.2s;
}

[dir="rtl"] .password-toggle {
  right: auto;
  left: 16px;
}

.password-toggle:hover {
  background: rgba(0, 0, 0, 0.04);
}

.toggle-icon {
  width: 20px;
  height: 20px;
  color: #94a3b8;
  transition: color 0.2s;
}

.password-toggle:hover .toggle-icon {
  color: #64748b;
}

/* ============================================
   ACTION ROW - 100% Horizontal Symmetry
   ============================================ */
.action-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 6px;
  padding: 0 2px;
}

/* --- Custom Checkbox --- */
.custom-checkbox {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.custom-checkbox input {
  display: none;
}

.checkmark {
  width: 18px;
  height: 18px;
  border: 1.5px solid #cbd5e1;
  border-radius: 4px;
  margin-inline-end: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  background: #ffffff;
}

.custom-checkbox input:checked+.checkmark {
  background: #2563eb;
  border-color: #2563eb;
}

.custom-checkbox input:checked+.checkmark::after {
  content: '';
  width: 5px;
  height: 9px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
  margin-top: -2px;
}

.checkbox-label {
  font-size: 13px;
  font-weight: 400;
  color: #475569;
  letter-spacing: 0.1px;
}

/* --- Forgot Password Link --- */
.forgot-link {
  font-size: 13px;
  font-weight: 500;
  color: #2563eb;
  text-decoration: none;
  transition: all 0.2s ease;
}

.forgot-link:hover {
  color: #1d4ed8;
  text-decoration: underline;
}

/* ============================================
   LOGIN BUTTON - Smooth Interactive Animation
   ============================================ */
.login-btn {
  width: 100%;
  height: 56px;
  background: #4169E1;
  /* Royal Blue */
  color: #ffffff;
  font-family: 'Inter Tight', sans-serif;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: 0.4px;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.2), 0 4px 14px rgba(65, 105, 225, 0.2);
  /* Satin Finish */
  transition:
    all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1),
    transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  margin-top: 24px;
  position: relative;
  overflow: hidden;
}

.login-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
      transparent,
      rgba(255, 255, 255, 0.15),
      transparent);
  transition: left 0.6s ease;
}

.login-btn:hover::before {
  left: 100%;
}

.login-btn:hover:not(:disabled) {
  background: #5a7ef2;
  /* Lighter Royal Blue for hover */
  box-shadow:
    0 8px 28px rgba(65, 105, 225, 0.3),
    0 4px 12px rgba(65, 105, 225, 0.2);
  transform: translateY(-2px);
}

.login-btn:active:not(:disabled) {
  /* Press-down effect */
  transform: translateY(0px);
  box-shadow:
    0 2px 8px rgba(65, 105, 225, 0.2),
    0 1px 4px rgba(65, 105, 225, 0.1);
  transition: all 0.1s ease;
}

.login-btn:disabled {
  cursor: not-allowed;
  opacity: 0.7;
  background: linear-gradient(135deg, #64748b 0%, #94a3b8 100%);
}

/* --- Loading Spinner --- */
.loader {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ============================================
   FOOTER - Enhanced Contrast
   ============================================ */
.login-footer {
  margin-top: 44px;
  text-align: center;
}

.divider-line {
  height: 1px;
  background: linear-gradient(to right,
      transparent 0%,
      #e2e8f0 15%,
      #e2e8f0 85%,
      transparent 100%);
  margin-bottom: 18px;
}

.copyright-text {
  font-size: 13px;
  font-weight: 400;
  color: #64748b;
  letter-spacing: 0.1px;
}

/* --- Technical Support Link --- */
.support-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 500;
  color: #64748b;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 20px;
  transition: all 0.25s ease;
  background: rgba(241, 245, 249, 0.6);
  border: 1px solid transparent;
}

.support-link:hover {
  color: #1e40af;
  background: rgba(219, 234, 254, 0.5);
  border-color: rgba(59, 130, 246, 0.2);
  transform: translateY(-1px);
}

.support-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.2s ease;
}

.support-link:hover .support-icon {
  transform: rotate(15deg);
}

/* ============================================
   RESPONSIVE DESIGN
   ============================================ */
@media (max-width: 640px) {
  .content-wrapper {
    padding: 16px;
  }

  .card-content {
    padding: 40px 28px;
  }

  .university-card {
    border-radius: 20px;
  }

  .university-title {
    font-size: 24px;
  }

  .university-subtitle {
    font-size: 14px;
  }

  .language-switcher {
    top: 16px;
    right: 16px;
    padding: 8px 16px;
  }

  .lang-btn {
    font-size: 12px;
    padding: 5px 10px;
  }

  .header-section {
    margin-bottom: 36px;
  }

  .logo-circle {
    width: 72px;
    height: 72px;
    padding: 14px;
  }

  .premium-input {
    height: 52px;
    font-size: 14px;
  }

  .login-btn {
    height: 52px;
    font-size: 15px;
  }
}

@media (max-width: 400px) {
  .card-content {
    padding: 32px 20px;
  }

  .action-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .forgot-link {
    align-self: flex-end;
  }
}

/* ============================================
   4K ULTRA-HD ENHANCEMENTS
   ============================================ */
@media (min-width: 2560px) {
  .content-wrapper {
    max-width: 560px;
  }

  .card-content {
    padding: 72px 64px;
  }

  .university-title {
    font-size: 34px;
  }

  .university-subtitle {
    font-size: 17px;
  }

  .logo-circle {
    width: 104px;
    height: 104px;
  }

  .premium-input {
    height: 64px;
    font-size: 17px;
    border-radius: 16px;
  }

  .login-btn {
    height: 64px;
    font-size: 18px;
    border-radius: 16px;
  }

  .language-switcher {
    top: 48px;
    right: 60px;
    padding: 14px 28px;
  }

  .lang-btn {
    font-size: 15px;
    padding: 8px 18px;
  }
}
</style>
