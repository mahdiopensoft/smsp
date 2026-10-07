<template>
  <div>
    <!-- Page Header -->
    <div class="d-flex align-center justify-space-between mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold mb-1">الملف الشخصي</h1>
        <p class="text-body-2 text-medium-emphasis">إدارة معلومات حسابك الشخصي</p>
      </div>
    </div>

    <v-row>
      <!-- User Info Card -->
      <v-col cols="12" md="4">
        <v-card class="glass-card pa-6 text-center h-100">
          <v-avatar color="primary" size="120" class="mb-4 elevation-4">
            <span class="text-h2 font-weight-bold text-white">{{ getInitials(user.name) }}</span>
          </v-avatar>
          <h2 class="text-h5 font-weight-bold mb-1">{{ user.name }}</h2>
          <p class="text-body-1 text-medium-emphasis mb-2">{{ user.email }}</p>
          <v-chip color="primary" variant="tonal" class="mb-4">
            {{ getRoleText(user.role) }}
          </v-chip>
          
          <v-divider class="my-4" />
          
          <div class="d-flex justify-space-around">
            <div class="text-center">
              <div class="text-h6 font-weight-bold">12</div>
              <div class="text-caption text-medium-emphasis">اختبارات</div>
            </div>
            <div class="text-center">
              <div class="text-h6 font-weight-bold">45</div>
              <div class="text-caption text-medium-emphasis">أسئلة</div>
            </div>
            <div class="text-center">
              <div class="text-h6 font-weight-bold">3</div>
              <div class="text-caption text-medium-emphasis">سنوات</div>
            </div>
          </div>
        </v-card>
      </v-col>

      <!-- Edit Profile Form -->
      <v-col cols="12" md="8">
        <v-card class="glass-card pa-6">
          <v-card-title class="text-h6 font-weight-bold mb-4 px-0">
            تعديل البيانات
          </v-card-title>
          
          <v-form ref="form" @submit.prevent="saveProfile">
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="formData.name"
                  label="الاسم الكامل"
                  prepend-inner-icon="mdi-account"
                  :rules="[rules.required]"
                  variant="outlined"
                />
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="formData.email"
                  label="البريد الإلكتروني"
                  prepend-inner-icon="mdi-email"
                  :rules="[rules.required, rules.email]"
                  variant="outlined"
                  type="email"
                />
              </v-col>
            </v-row>

            <v-divider class="my-6" />

            <v-card-title class="text-h6 font-weight-bold mb-4 px-0">
              تغيير كلمة المرور
            </v-card-title>

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="passwordData.current"
                  label="كلمة المرور الحالية"
                  prepend-inner-icon="mdi-lock-outline"
                  :type="showCurrentPassword ? 'text' : 'password'"
                  :append-inner-icon="showCurrentPassword ? 'mdi-eye-off' : 'mdi-eye'"
                  @click:append-inner="showCurrentPassword = !showCurrentPassword"
                  variant="outlined"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="passwordData.new"
                  label="كلمة المرور الجديدة"
                  prepend-inner-icon="mdi-lock-plus"
                  :type="showNewPassword ? 'text' : 'password'"
                  :append-inner-icon="showNewPassword ? 'mdi-eye-off' : 'mdi-eye'"
                  @click:append-inner="showNewPassword = !showNewPassword"
                  variant="outlined"
                />
              </v-col>
            </v-row>

            <div class="d-flex justify-end mt-6">
              <v-btn
                color="primary"
                size="large"
                type="submit"
                :loading="saving"
                prepend-icon="mdi-content-save"
                class="btn-gradient"
              >
                حفظ التغييرات
              </v-btn>
            </div>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from 'vuetify'
import api from '@/services/api'
import { authService } from '@/services/authService'
import { rules } from '@/utils/validations'
import { useNotificationStore } from '@/stores/notificationStore'

// Theme Logic
const theme = useTheme()
const isDark = computed(() => theme.global.current.value.dark)
const notificationStore = useNotificationStore()
const cardBackground = computed(() => isDark.value ? 'rgba(30, 41, 59, 0.9)' : 'rgba(255, 255, 255, 0.9)')
const borderColor = computed(() => isDark.value ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)')

// State
const form = ref(null)
const saving = ref(false)
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)

// Real User Data
const user = ref({
  name: '',
  email: '',
  role: '',
})

const formData = ref({
  name: '',
  email: '',
})

const passwordData = ref({
  current: '',
  new: ''
})

// Methods
const getInitials = (name) => {
  if (!name) return ''
  const parts = name.split(' ')
  return parts.length > 1 ? parts[0][0] + parts[1][0] : parts[0][0]
}

const getRoleText = (role) => {
  const roles = {
    Admin: 'مدير النظام',
    Teacher: 'معلم',
    Reviewer: 'مراجع',
    Generator: 'مولد اختبارات'
  }
  return roles[role] || role
}

const loadProfile = async () => {
  try {
    const data = await authService.getCurrentUser()
    user.value = {
      name: data.name,
      email: data.email,
      role: data.role,
    }
    formData.value = {
      name: data.name,
      email: data.email,
    }
  } catch (err) {
    console.error("Failed to load profile:", err)
  }
}

onMounted(() => {
  loadProfile()
})

const saveProfile = async () => {
  if (form.value) {
    const { valid } = await form.value.validate()
    if (!valid) return
  }

  saving.value = true
  try {
    const payload = { ...formData.value }
    if (passwordData.value.current && passwordData.value.new) {
       payload.current_password = passwordData.value.current
       payload.password = passwordData.value.new
    }

    const response = await api.put('accounts/me/', payload)
    const data = response.data
    
    // Update local state on success
    user.value.name = data.name || formData.value.name
    user.value.email = data.email || formData.value.email
    
    // Update local storage to persist state across app
    const storedUser = authService.getStoredUser()
    if (storedUser) {
        storedUser.name = user.value.name
        storedUser.email = user.value.email
        localStorage.setItem('auth_user', JSON.stringify(storedUser))
    }
    
    // Reset password fields
    passwordData.value.current = ''
    passwordData.value.new = ''
    
    if (data.detail) {
      notificationStore.showSuccess('تم حفظ البيانات بنجاح! ' + data.detail)
    } else {
      notificationStore.showSuccess('تم حفظ البيانات بنجاح!')
    }
  } catch (err) {
    console.error("Error saving profile:", err)
    if (err.response?.data?.detail) {
      notificationStore.showError(err.response.data.detail)
    } else {
      notificationStore.showError('حدث خطأ أثناء حفظ البيانات.')
    }
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.glass-card {
  background: v-bind(cardBackground) !important;
  border: 1px solid v-bind(borderColor);
  border-radius: 16px;
  transition: all 0.3s ease;
}

.glass-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.1);
}

.btn-gradient {
  background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
  color: white;
  font-weight: bold;
}
</style>