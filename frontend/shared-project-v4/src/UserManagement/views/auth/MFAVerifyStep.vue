<template>
  <div class="mfa-verify-step">
    <!-- Back button -->
    <div class="mfa-header">
      <button type="button" class="back-btn" @click="$emit('back')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
          <path d="M19 12H5M12 19l-7-7 7-7" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </button>
      <div class="mfa-title-section">
        <div class="shield-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="32" height="32">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M9 12l2 2 4-4" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </div>
        <h3 class="mfa-title">المصادقة الثنائية</h3>
        <p class="mfa-subtitle">أدخل رمز التحقق من تطبيق المصادقة</p>
      </div>
    </div>

    <!-- OTP Input -->
    <div class="otp-input-container">
      <div class="otp-fields" dir="ltr">
        <input v-for="(digit, idx) in otpDigits" :key="idx" :ref="el => otpRefs[idx] = el" type="text"
          inputmode="numeric" maxlength="1" class="otp-field" :class="{ 'has-value': digit, 'error': hasError }"
          :value="digit" @input="onDigitInput(idx, $event)" @keydown="onDigitKeydown(idx, $event)"
          @paste="onPaste($event)" @focus="onDigitFocus(idx)" />
      </div>

      <!-- TOTP Timer -->
      <div class="totp-timer" v-if="!useBackup">
        <v-progress-circular :model-value="timerPercent" :size="36" :width="3"
          :color="timerPercent > 33 ? 'primary' : 'red'">
          <span class="timer-text">{{ timerSeconds }}</span>
        </v-progress-circular>
        <span class="timer-label">ثانية متبقية</span>
      </div>
    </div>

    <!-- Error message -->
    <v-alert v-if="errorMessage" type="error" variant="tonal" density="compact" class="mb-3" closable
      @click:close="errorMessage = ''">
      {{ errorMessage }}
    </v-alert>

    <!-- Verify Button -->
    <v-btn color="primary" size="large" block :loading="isVerifying || loadingBtn"
      :disabled="otpCode.length < 6 && !useBackup" @click="verifyOTP" class="verify-btn mb-3">
      <v-icon start>mdi-check-circle</v-icon>
      تحقق
    </v-btn>

    <!-- Backup code toggle -->
    <div class="backup-section">
      <button type="button" class="backup-toggle" @click="useBackup = !useBackup">
        <v-icon size="16" class="me-1">{{ useBackup ? 'mdi-cellphone' : 'mdi-key-variant' }}</v-icon>
        {{ useBackup ? 'استخدام تطبيق المصادقة' : 'استخدام رمز استرداد' }}
      </button>

      <!-- Backup code input -->
      <v-text-field v-if="useBackup" v-model="backupCode" label="رمز الاسترداد" placeholder="xxxxxxxx"
        prepend-inner-icon="mdi-key" variant="outlined" density="compact" dir="ltr" class="mt-3" hide-details />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { mfaApi } from '../../api/mfa'
import { useAuthStore } from '../../stores/auth'

const props = defineProps({
  loadingBtn: {
    type: Boolean,
    default: false
  }
})
const emit = defineEmits(['verified', 'back'])

const authStore = useAuthStore()
const isVerifying = ref(false)
const errorMessage = ref('')
const hasError = ref(false)
const useBackup = ref(false)
const backupCode = ref('')

// OTP digit management
const otpDigits = ref(['', '', '', '', '', ''])
const otpRefs = ref([])

const otpCode = computed(() => otpDigits.value.join(''))

// TOTP 30-second timer
const timerSeconds = ref(30)
const timerPercent = computed(() => (timerSeconds.value / 30) * 100)
let timerInterval = null

const startTimer = () => {
  const now = Math.floor(Date.now() / 1000)
  timerSeconds.value = 30 - (now % 30)
  timerInterval = setInterval(() => {
    const now = Math.floor(Date.now() / 1000)
    timerSeconds.value = 30 - (now % 30)
  }, 1000)
}

// OTP input handlers
const onDigitInput = (idx, event) => {
  const val = event.target.value.replace(/\D/g, '')
  otpDigits.value[idx] = val ? val[0] : ''
  hasError.value = false
  errorMessage.value = ''
  if (val && idx < 5) {
    nextTick(() => otpRefs.value[idx + 1]?.focus())
  }
  // Auto-submit when all 6 digits entered
  if (otpCode.value.length === 6) {
    verifyOTP()
  }
}

const onDigitKeydown = (idx, event) => {
  if (event.key === 'Backspace' && !otpDigits.value[idx] && idx > 0) {
    otpDigits.value[idx - 1] = ''
    nextTick(() => otpRefs.value[idx - 1]?.focus())
  }
}

const onDigitFocus = (idx) => {
  otpRefs.value[idx]?.select()
}

const onPaste = (event) => {
  event.preventDefault()
  const pasted = (event.clipboardData?.getData('text') || '').replace(/\D/g, '').slice(0, 6)
  for (let i = 0; i < 6; i++) {
    otpDigits.value[i] = pasted[i] || ''
  }
  if (pasted.length === 6) {
    nextTick(() => verifyOTP())
  }
}

// Verify OTP
const verifyOTP = async () => {
  const code = useBackup.value ? backupCode.value.trim() : otpCode.value
  if (!code) return

  isVerifying.value = true
  errorMessage.value = ''
  hasError.value = false

  try {
    await authStore.verifyMFA(code)


    emit('verified')
  } catch (error) {
    hasError.value = true
    errorMessage.value = error.response?.data?.message || 'رمز التحقق غير صحيح'
    // Clear OTP on error
    if (!useBackup.value) {
      otpDigits.value = ['', '', '', '', '', '']
      nextTick(() => otpRefs.value[0]?.focus())
    }
  } finally {
    isVerifying.value = false
  }
}

onMounted(() => {
  startTimer()
  nextTick(() => otpRefs.value[0]?.focus())
})

onBeforeUnmount(() => {
  if (timerInterval) clearInterval(timerInterval)
})
</script>

<style scoped>
.mfa-verify-step {
  animation: fadeSlideIn 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes fadeSlideIn {
  from {
    opacity: 0;
    transform: translateY(12px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.mfa-header {
  text-align: center;
  margin-bottom: 28px;
  position: relative;
}

.back-btn {
  position: absolute;
  top: 0;
  right: 0;
  background: none;
  border: none;
  padding: 8px;
  border-radius: 50%;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

[dir="ltr"] .back-btn {
  right: auto;
  left: 0;
}

.back-btn:hover {
  background: rgba(100, 116, 139, 0.1);
  color: #1e293b;
}

.shield-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(37, 99, 235, 0.05));
  color: #2563eb;
  margin-bottom: 12px;
}

.mfa-title {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.mfa-subtitle {
  font-size: 14px;
  color: #64748b;
  font-weight: 400;
}

/* OTP Input Fields */
.otp-input-container {
  margin-bottom: 20px;
}

.otp-fields {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 16px;
}

.otp-field {
  width: 48px;
  height: 56px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  text-align: center;
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  background: #f8fafc;
  outline: none;
  transition: all 0.2s ease;
  caret-color: #2563eb;
}

.otp-field:focus {
  border-color: #2563eb;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
  transform: translateY(-2px);
}

.otp-field.has-value {
  border-color: #2563eb;
  background: #fff;
}

.otp-field.error {
  border-color: #ef4444;
  background: #fef2f2;
  animation: shake 0.4s ease;
}

@keyframes shake {

  0%,
  100% {
    transform: translateX(0);
  }

  25% {
    transform: translateX(-4px);
  }

  75% {
    transform: translateX(4px);
  }
}

/* TOTP Timer */
.totp-timer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.timer-text {
  font-size: 12px;
  font-weight: 700;
}

.timer-label {
  font-size: 12px;
  color: #94a3b8;
}

/* Verify Button */
.verify-btn {
  text-transform: none !important;
  font-weight: 600;
  letter-spacing: 0.3px;
  border-radius: 12px !important;
}

/* Backup Section */
.backup-section {
  text-align: center;
}

.backup-toggle {
  background: none;
  border: none;
  color: #64748b;
  font-size: 13px;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
}

.backup-toggle:hover {
  background: rgba(100, 116, 139, 0.08);
  color: #2563eb;
}
</style>
