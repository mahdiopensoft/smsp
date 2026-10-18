<template>
  <v-container fluid class="fill-height success-background">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="glass-card pa-8 text-center" elevation="8">
          <!-- Success Icon -->
          <v-avatar size="100" color="success" class="mb-6">
            <v-icon size="64" color="white">mdi-check-circle</v-icon>
          </v-avatar>

          <h1 class="text-h4 font-weight-bold mb-4">
            تم تسجيل الخروج بنجاح
          </h1>

          <p class="text-body-1 text-grey-darken-1 mb-6">
            تم إنهاء جلستك بأمان. شكراً لاستخدامك النظام.
          </p>

          <!-- Auto-redirect countdown -->
          <p v-if="countdown > 0" class="text-body-2 text-grey mb-4">
            سيتم توجيهك إلى صفحة الدخول خلال {{ countdown }} ثانية...
          </p>

          <v-btn
            color="primary"
            size="large"
            :to="{ name: 'Login' }"
            class="px-8"
          >
            <v-icon start>mdi-login</v-icon>
            تسجيل الدخول مرة أخرى
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const countdown = ref(5)
let timer = null

onMounted(() => {
  // Ensure auth is cleared
  authStore.clearAuth()
  
  // Start countdown for auto-redirect
  timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
      router.push({ name: 'Login' })
    }
  }, 1000)
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped>
.success-background {
  background: linear-gradient(135deg, #1A5F7A 0%, #159895 50%, #57C5B6 100%);
  min-height: 100vh;
}

.glass-card {
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(10px);
}
</style>
