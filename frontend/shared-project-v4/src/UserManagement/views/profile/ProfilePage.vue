<template>
  <div>
    <h1 class="text-h4 font-weight-bold mb-6">
      <v-icon start color="primary">mdi-account</v-icon>
      الملف الشخصي
    </h1>

    <v-row>
      <!-- Profile Card -->
      <v-col cols="12" md="4">
        <v-card elevation="4" class="text-center pa-6">
          <v-avatar size="120" color="primary" class="mb-4">
            <v-img v-if="user?.image" :src="user.image"></v-img>
            <span v-else class="text-h3 text-white font-weight-bold">
              {{ authStore.userInitials }}
            </span>
          </v-avatar>
          
          <h2 class="text-h5 font-weight-bold mb-1">
            {{ authStore.userDisplayName }}
          </h2>
          <p class="text-body-2 text-grey mb-4">{{ user?.email }}</p>
          
          <v-chip
            :color="user?.is_active ? 'success' : 'error'"
            variant="tonal"
            class="mb-4"
          >
            {{ user?.is_active ? 'نشط' : 'غير نشط' }}
          </v-chip>
          
          <v-divider class="my-4"></v-divider>
          
          <v-list density="compact">
            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-account</v-icon>
              </template>
              <v-list-item-title>اسم المستخدم</v-list-item-title>
              <v-list-item-subtitle>{{ user?.username }}</v-list-item-subtitle>
            </v-list-item>
            
            <v-list-item v-if="isSSO">
              <template v-slot:prepend>
                <v-icon color="secondary">mdi-key</v-icon>
              </template>
              <v-list-item-title>نوع المصادقة</v-list-item-title>
              <v-list-item-subtitle>المنصة التعليمية الموحدة</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <!-- Edit Profile -->
      <v-col cols="12" md="8">
        <v-card elevation="4">
          <v-tabs v-model="tab" color="primary">
            <v-tab value="info">
              <v-icon start>mdi-account-edit</v-icon>
              المعلومات الشخصية
            </v-tab>
            <v-tab value="password">
              <v-icon start>mdi-lock-reset</v-icon>
              تغيير كلمة المرور
            </v-tab>
            <v-tab value="mfa">
              <v-icon start>mdi-shield-lock</v-icon>
              المصادقة الثنائية
            </v-tab>
            <v-tab v-if="isSSO" value="sessions">
              <v-icon start>mdi-devices</v-icon>
              الجلسات النشطة
            </v-tab>
          </v-tabs>

          <v-tabs-window v-model="tab">
            <!-- Profile Info Tab -->
            <v-tabs-window-item value="info">
              <v-card-text class="pa-6">
                <v-form ref="profileFormRef" v-model="profileValid">
                  <v-row>
                    <v-col cols="12" sm="6">
                      <v-text-field
                        v-model="profileForm.first_name"
                        label="الاسم الأول"
                        prepend-inner-icon="mdi-account"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <v-text-field
                        v-model="profileForm.last_name"
                        label="الاسم الأخير"
                        prepend-inner-icon="mdi-account"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="profileForm.email"
                        label="البريد الإلكتروني"
                        prepend-inner-icon="mdi-email"
                        type="email"
                      ></v-text-field>
                    </v-col>
                  </v-row>

                  <v-btn
                    color="primary"
                    :loading="savingProfile"
                    @click="saveProfile"
                  >
                    <v-icon start>mdi-content-save</v-icon>
                    حفظ التغييرات
                  </v-btn>
                </v-form>
              </v-card-text>
            </v-tabs-window-item>

            <!-- Password Tab -->
            <v-tabs-window-item value="password">
              <v-card-text class="pa-6">
                <v-form ref="passwordFormRef" v-model="passwordValid">
                  <v-text-field
                    v-model="passwordForm.old_password"
                    label="كلمة المرور الحالية"
                    prepend-inner-icon="mdi-lock"
                    :type="showOldPassword ? 'text' : 'password'"
                    :append-inner-icon="showOldPassword ? 'mdi-eye-off' : 'mdi-eye'"
                    @click:append-inner="showOldPassword = !showOldPassword"
                    :rules="[rules.required]"
                    class="mb-4"
                  ></v-text-field>

                  <v-text-field
                    v-model="passwordForm.new_password"
                    label="كلمة المرور الجديدة"
                    prepend-inner-icon="mdi-lock-plus"
                    :type="showNewPassword ? 'text' : 'password'"
                    :append-inner-icon="showNewPassword ? 'mdi-eye-off' : 'mdi-eye'"
                    @click:append-inner="showNewPassword = !showNewPassword"
                    :rules="[rules.required, rules.minLength]"
                    class="mb-4"
                  ></v-text-field>

                  <v-text-field
                    v-model="passwordForm.confirm_password"
                    label="تأكيد كلمة المرور"
                    prepend-inner-icon="mdi-lock-check"
                    :type="showConfirmPassword ? 'text' : 'password'"
                    :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
                    @click:append-inner="showConfirmPassword = !showConfirmPassword"
                    :rules="[rules.required, rules.passwordMatch]"
                    class="mb-4"
                  ></v-text-field>

                  <v-btn
                    color="warning"
                    :loading="changingPassword"
                    :disabled="!passwordValid"
                    @click="changePassword"
                  >
                    <v-icon start>mdi-lock-reset</v-icon>
                    تغيير كلمة المرور
                  </v-btn>
                </v-form>
              </v-card-text>
            </v-tabs-window-item>

            <!-- MFA Security Tab -->
            <v-tabs-window-item value="mfa">
              <v-card-text class="pa-6">
                <MFASetup />
              </v-card-text>
            </v-tabs-window-item>

            <!-- Sessions Tab (SSO only) -->
            <v-tabs-window-item v-if="isSSO" value="sessions">
              <v-card-text class="pa-6">
                <v-alert type="info" variant="tonal" class="mb-4">
                  الجلسات النشطة من المنصة التعليمية الموحدة
                </v-alert>

                <v-btn
                  color="primary"
                  variant="outlined"
                  :loading="loadingSessions"
                  @click="loadSessions"
                  class="mb-4"
                >
                  <v-icon start>mdi-refresh</v-icon>
                  تحديث الجلسات
                </v-btn>

                <v-list v-if="sessions.length > 0">
                  <v-list-item
                    v-for="session in sessions"
                    :key="session.id"
                  >
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-devices</v-icon>
                    </template>
                    <v-list-item-title>{{ session.browser || 'متصفح غير معروف' }}</v-list-item-title>
                    <v-list-item-subtitle>{{ session.ip_address }}</v-list-item-subtitle>
                    <template v-slot:append>
                      <v-btn
                        size="small"
                        color="error"
                        variant="tonal"
                        @click="revokeSession(session.id)"
                      >
                        إنهاء
                      </v-btn>
                    </template>
                  </v-list-item>
                </v-list>
                <p v-else class="text-grey">لا توجد جلسات نشطة</p>
              </v-card-text>
            </v-tabs-window-item>
          </v-tabs-window>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { authApi } from "../../api/auth"
import { ssoApi } from '../../api/sso'
  

 const authStore = useAuthStore()
 const isSSo = authStore.isSSo
 
const showSnackbar = inject('showSnackbar')

const tab = ref('info')
const user = computed(() => authStore.user)

// Profile form
const profileFormRef = ref(null)
const profileValid = ref(false)
const savingProfile = ref(false)
const profileForm = ref({
  first_name: '',
  last_name: '',
  email: '',
})

// Password form
const passwordFormRef = ref(null)
const passwordValid = ref(false)
const changingPassword = ref(false)
const showOldPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)
const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: '',
})

// Sessions (SSO)
const sessions = ref([])
const loadingSessions = ref(false)

const rules = {
  required: (v) => !!v || 'هذا الحقل مطلوب',
  minLength: (v) => (v && v.length >= 8) || 'يجب أن تكون 8 أحرف على الأقل',
  passwordMatch: (v) => v === passwordForm.value.new_password || 'كلمة المرور غير متطابقة',
}

onMounted(() => {
  // Initialize form with current user data
  if (user.value) {
    profileForm.value = {
      first_name: user.value.first_name || '',
      last_name: user.value.last_name || '',
      email: user.value.email || '',
    }
  }
})

const saveProfile = async () => {
  savingProfile.value = true
  try {
    await authApi.updateProfile(profileForm.value)
    await authStore.fetchProfile()
    showSnackbar('تم حفظ التغييرات بنجاح', 'success')
  } catch (error) {
    showSnackbar(error.response?.data?.message || 'فشل حفظ التغييرات', 'error')
  } finally {
    savingProfile.value = false
  }
}

const changePassword = async () => {
  changingPassword.value = true
  try {
    await authApi.changePassword(
      passwordForm.value.old_password,
      passwordForm.value.new_password
    )
    showSnackbar('تم تغيير كلمة المرور بنجاح', 'success')
    passwordForm.value = { old_password: '', new_password: '', confirm_password: '' }
  } catch (error) {
    showSnackbar(error.response?.data?.message || 'فشل تغيير كلمة المرور', 'error')
  } finally {
    changingPassword.value = false
  }
}

const loadSessions = async () => {
  loadingSessions.value = true
  try {
    const data = await ssoApi.getSessions()
    sessions.value = data.sessions || data || []
  } catch (error) {
    showSnackbar('فشل تحميل الجلسات', 'error')
  } finally {
    loadingSessions.value = false
  }
}

const revokeSession = async (sessionId) => {
  try {
    await ssoApi.revokeSession(sessionId)
    showSnackbar('تم إنهاء الجلسة', 'success')
    await loadSessions()
  } catch (error) {
    showSnackbar('فشل إنهاء الجلسة', 'error')
  }
}
</script>
