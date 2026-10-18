<template>
  <v-container fluid class="fill-height error-container justify-center align-center ">
    <v-card class="pa-8 error-card" max-width="550" elevation="12">
      <!-- Error Icon -->
      <div class="text-center mb-6">
        <div class="error-icon-wrapper">
          <v-icon size="80" color="error">{{ errorIcon }}</v-icon>
        </div>
      </div>

      <!-- Error Title -->
      <h1 class="text-h4 text-center font-weight-bold mb-4">{{ errorTitle }}</h1>
      
      <!-- Error Message -->
      <v-alert 
        type="error" 
        variant="tonal" 
        class="mb-6"
        prominent
      >
        <v-alert-title class="text-subtitle-1 font-weight-bold mb-2">
          وصف الخطأ
        </v-alert-title>
        {{ errorMessage }}
      </v-alert>

      <!-- Error Details (Collapsible) -->
      <v-expansion-panels v-if="hasDetails" flat class="mb-6">
        <v-expansion-panel>
          <v-expansion-panel-title>
            <v-icon start>mdi-code-json</v-icon>
            تفاصيل تقنية
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-table density="compact" class="details-table">
              <tbody>
                <tr v-if="errorCode">
                  <td class="font-weight-bold">رمز الخطأ</td>
                  <td><code>{{ errorCode }}</code></td>
                </tr>
                <tr v-if="errorState">
                  <td class="font-weight-bold">الحالة</td>
                  <td><code>{{ errorState }}</code></td>
                </tr>
                <tr>
                  <td class="font-weight-bold">الوقت</td>
                  <td>{{ timestamp }}</td>
                </tr>
                <tr>
                  <td class="font-weight-bold">المتصفح</td>
                  <td>{{ browserInfo }}</td>
                </tr>
              </tbody>
            </v-table>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>

      <!-- Suggestions -->
      <v-card variant="outlined" class="mb-6 pa-4">
        <h3 class="text-subtitle-1 font-weight-bold mb-3">
          <v-icon start color="info">mdi-lightbulb</v-icon>
          ما الذي يمكنك فعله؟
        </h3>
        <ul class="suggestions-list">
          <li v-for="(suggestion, index) in suggestions" :key="index">
            {{ suggestion }}
          </li>
        </ul>
      </v-card>

      <!-- Actions -->
      <div class="d-flex flex-column gap-2">
        <v-btn 
          color="primary" 
          size="large" 
          block
          @click="retryLogin"
        >
          <v-icon start>mdi-refresh</v-icon>
          إعادة محاولة تسجيل الدخول
        </v-btn>
        
        <v-btn 
          color="grey-darken-1" 
          variant="outlined"
          size="large"
          block
          :to="{ name: 'Login' }"
        >
          <v-icon start>mdi-arrow-left</v-icon>
          العودة لصفحة تسجيل الدخول
        </v-btn>

        <v-btn 
          v-if="supportEmail"
          color="info" 
          variant="text"
          size="large"
          block
          :href="`mailto:${supportEmail}?subject=خطأ في تسجيل الدخول: ${errorCode}&body=رسالة الخطأ: ${errorMessage}`"
        >
          <v-icon start>mdi-email</v-icon>
          تواصل مع الدعم الفني
        </v-btn>
      </div>
    </v-card>
  </v-container>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// Configuration
const supportEmail = import.meta.env.VITE_SUPPORT_EMAIL || ''

// Get error details from query params
const errorMessage = computed(() => {
  return route.query.message || 'حدث خطأ غير متوقع أثناء محاولة تسجيل الدخول'
})

const errorCode = computed(() => route.query.code || null)
const errorState = computed(() => route.query.state || null)

const hasDetails = computed(() => errorCode.value || errorState.value)

// Dynamic error title and icon based on error code
const errorTitle = computed(() => {
  const titles = {
    'access_denied': 'تم رفض الوصول',
    'unauthorized': 'غير مصرح',
    'session_expired': 'انتهت الجلسة',
    'invalid_token': 'رمز غير صالح',
    'server_error': 'خطأ في الخادم',
    'network_error': 'خطأ في الاتصال',
    'missing_code': 'معاملات ناقصة',
    'callback_error': 'خطأ في المعالجة',
  }
  return titles[errorCode.value] || 'خطأ في المصادقة'
})

const errorIcon = computed(() => {
  const icons = {
    'access_denied': 'mdi-cancel',
    'unauthorized': 'mdi-shield-lock',
    'session_expired': 'mdi-timer-off',
    'invalid_token': 'mdi-key-alert',
    'server_error': 'mdi-server-off',
    'network_error': 'mdi-wifi-off',
    'missing_code': 'mdi-file-question',
    'callback_error': 'mdi-alert-octagon',
  }
  return icons[errorCode.value] || 'mdi-alert-circle'
})

// Suggestions based on error type
const suggestions = computed(() => {
  const baseSuggestions = [
    'تأكد من اتصالك بالإنترنت',
    'حاول مسح ذاكرة التخزين المؤقت للمتصفح',
    'جرب استخدام متصفح مختلف',
  ]
  
  const errorSuggestions = {
    'access_denied': [
      'تأكد من أن لديك صلاحيات الوصول المناسبة',
      'تواصل مع مسؤول النظام إذا كنت تعتقد أن هذا خطأ',
    ],
    'session_expired': [
      'قد تكون جلستك قد انتهت بسبب عدم النشاط',
      'أعد تسجيل الدخول للمتابعة',
    ],
    'network_error': [
      'تحقق من اتصالك بالإنترنت',
      'تأكد من عدم حظر خدمات المصادقة بواسطة جدار الحماية',
    ],
  }
  
  return [...(errorSuggestions[errorCode.value] || []), ...baseSuggestions]
})

// Technical info
const timestamp = new Date().toLocaleString('ar-SA', {
  dateStyle: 'full',
  timeStyle: 'medium',
})

const browserInfo = navigator.userAgent.split(' ').slice(-2).join(' ')

// Actions
const retryLogin = () => {
  // Clear any stored state and redirect to login
  sessionStorage.removeItem('sso_state')
  sessionStorage.removeItem('code_verifier')
  router.push({ name: 'SSOLogin' })
}
</script>

<style scoped>
.error-container {
  background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
  min-height: 100vh;
}

.error-card {
  border-radius: 20px;
}

.error-icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: rgba(244, 67, 54, 0.1);
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-10px); }
  40% { transform: translateX(10px); }
  60% { transform: translateX(-10px); }
  80% { transform: translateX(10px); }
}

.suggestions-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.suggestions-list li {
  position: relative;
  padding-right: 24px;
  margin-bottom: 8px;
}

.suggestions-list li::before {
  content: '•';
  position: absolute;
  right: 0;
  color: #1976d2;
  font-weight: bold;
}

.details-table td {
  padding: 8px 12px;
}

.details-table code {
  background: #f5f5f5;
  padding: 2px 8px;
  border-radius: 4px;
  font-family: monospace;
}
</style>
