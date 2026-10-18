<template>
  <div class="profile-dialog-wrapper">
    <v-dialog
      v-model="dialog"
      class="profile-dialog"
      :fullscreen="xs"
      max-width="480"
    >
      <v-card class="profile-card">
        <!-- Modern Header with Royal Blue Gradient -->
        <div class="profile-header">
          <div class="header-content">
            <div class="header-text">
              <h2 class="header-title">{{ $t("settings.profile.title") }}</h2>
              <p class="header-subtitle">
                {{ $t("settings.profile.subtitle") }}
              </p>
            </div>
            <v-btn
              class="close-btn"
              icon
              size="small"
              variant="text"
              @click="dialog = false"
            >
              <v-icon size="20">mdi-close</v-icon>
            </v-btn>
          </div>

          <!-- Avatar Section - Overlapping -->
          <div class="avatar-section">
            <div class="avatar-wrapper">
              <v-avatar class="avatar-ring" size="120">
                <v-img
                  cover
                  :src="form.profile_picture || '/default-avatar.png'"
                />
              </v-avatar>
              <v-btn
                class="camera-btn"
                icon="mdi-camera"
                size="small"
                @click="triggerFileInput"
              />
              <input
                ref="fileInput"
                accept="image/*"
                class="d-none"
                type="file"
                @change="handleFileChange"
              >
            </div>
            <div class="status-badge">
              <span class="pulse-dot" />
              <span class="status-text">{{ $t("chat.status.online") }}</span>
            </div>
          </div>
        </div>

        <v-card-text class="form-content">
          <!-- Name Fields -->
          <div class="field-row">
            <div class="field-group">
              <label class="field-label">
                <v-icon class="label-icon" size="14">mdi-account</v-icon>
                {{ $t("settings.profile.firstName") }}
              </label>
              <v-text-field
                v-model="form.first_name"
                class="modern-input"
                density="comfortable"
                hide-details
                :placeholder="$t('settings.profile.firstNamePlaceholder')"
                rounded="xl"
                variant="outlined"
              />
            </div>
            <div class="field-group">
              <label class="field-label">
                <v-icon class="label-icon" size="14">mdi-account</v-icon>
                {{ $t("settings.profile.lastName") }}
              </label>
              <v-text-field
                v-model="form.last_name"
                class="modern-input"
                density="comfortable"
                hide-details
                :placeholder="$t('settings.profile.lastNamePlaceholder')"
                rounded="xl"
                variant="outlined"
              />
            </div>
          </div>

          <!-- Bio Field -->
          <div class="field-group full-width">
            <label class="field-label">
              <v-icon class="label-icon" size="14">mdi-text</v-icon>
              {{ $t("settings.profile.bio") }}
            </label>
            <v-textarea
              v-model="form.bio"
              class="modern-input"
              density="comfortable"
              hide-details
              no-resize
              :placeholder="$t('settings.profile.bioPlaceholder')"
              rounded="xl"
              rows="3"
              variant="outlined"
            />
            <div class="char-counter">{{ form.bio?.length || 0 }}/150</div>
          </div>

          <!-- Phone Field -->
          <div class="field-group full-width">
            <label class="field-label">
              <v-icon class="label-icon" size="14">mdi-phone</v-icon>
              {{ $t("settings.profile.phone") }}
            </label>
            <v-text-field
              v-model="form.phone_number"
              class="modern-input"
              density="comfortable"
              hide-details
              :placeholder="$t('settings.profile.phone')"
              readonly
              rounded="xl"
              variant="outlined"
            >
              <template #append-inner>
                <v-icon color="primary" size="20">mdi-phone-check</v-icon>
              </template>
            </v-text-field>
          </div>

          <!-- Info Cards -->
          <div class="info-cards">
            <div class="info-card">
              <div class="info-icon">
                <v-icon size="20">mdi-email-outline</v-icon>
              </div>
              <div class="info-content">
                <span class="info-label">{{
                  $t("settings.profile.email")
                }}</span>
                <span class="info-value">{{ authStore.user?.email }}</span>
              </div>
            </div>
            <div class="info-card">
              <div class="info-icon">
                <v-icon size="20">mdi-calendar-outline</v-icon>
              </div>
              <div class="info-content">
                <span class="info-label">{{
                  $t("settings.profile.joined")
                }}</span>
                <span class="info-value">Recently</span>
              </div>
            </div>
          </div>
        </v-card-text>

        <!-- Action Buttons -->
        <v-card-actions class="action-buttons">
          <v-btn
            class="cancel-btn"
            height="48"
            rounded="xl"
            variant="outlined"
            @click="dialog = false"
          >
            <v-icon size="18" start>mdi-close</v-icon>
            {{ $t("common.cancel") }}
          </v-btn>
          <v-btn
            class="save-btn"
            color="primary"
            height="48"
            :loading="loading"
            rounded="xl"
            variant="flat"
            @click="saveProfile"
          >
            <v-icon size="18" start>mdi-check</v-icon>
            {{ $t("settings.profile.save") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- رسالة النجاح - ديلوق حديث -->
    <v-dialog v-model="showSuccessSnackbar" max-width="360" persistent>
      <v-card class="success-dialog">
        <div class="success-header">
          <div class="success-icon-wrapper">
            <v-icon color="white" size="48">mdi-check-circle</v-icon>
          </div>
        </div>
        <v-card-text class="success-content">
          <h3 class="success-title">
            {{ $t("settings.profile.success.title") }}
          </h3>
          <p class="success-message">
            {{ $t("settings.profile.success.message") }}
          </p>
        </v-card-text>
        <v-card-actions class="success-actions">
          <v-btn
            block
            class="success-btn"
            color="primary"
            height="48"
            rounded="xl"
            variant="flat"
            @click="showSuccessSnackbar = false"
          >
            <v-icon size="18" start>mdi-check</v-icon>
            {{ $t("common.confirm") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
  import { computed, ref, watch } from 'vue'
  import { useDisplay } from 'vuetify'
  import { authService } from '../../services/authService'
  import { useAuthStore } from '../../../src/UserManagement/stores/auth'

  const props = defineProps({
    modelValue: Boolean,
  })

  const emit = defineEmits(['update:modelValue'])

  const authStore = useAuthStore()
  const { xs } = useDisplay()
  const loading = ref(false)
  const showSuccessSnackbar = ref(false)
  const fileInput = ref(null)
  const selectedFile = ref(null)

  const form = ref({
    first_name: '',
    last_name: '',
    bio: '',
    phone_number: '',
    profile_picture: null,
  })

  const dialog = computed({
    get: () => props.modelValue,
    set: val => emit('update:modelValue', val),
  })

  // Initialize form when dialog opens
  watch(dialog, newVal => {
    if (newVal && authStore?.user) {
      // Assuming authStore?.user has these fields. Adjust based on exact API
      form.value = {
        first_name: authStore?.user.first_name || '',
        last_name: authStore?.user.last_name || '',
        bio: authStore?.user.bio || '4444444433', // Default text from image if empty
        phone_number: '777444111', // Dummy or actual
        profile_picture: authStore?.user.profile_picture,
      }
    }
  })

  function triggerFileInput () {
    fileInput.value.click()
  }

  function handleFileChange (e) {
    const file = e.target.files[0]
    if (file) {
      // حفظ الملف للرفع لاحقاً
      selectedFile.value = file
      // Show preview immediately
      const reader = new FileReader()
      reader.addEventListener('load', e => {
        form.value.profile_picture = e.target.result
      })
      reader.readAsDataURL(file)
    }
  }

  async function saveProfile () {
    loading.value = true
    try {
      // رفع الصورة أولاً إذا تم اختيار صورة جديدة
      if (selectedFile.value) {
        await authService.updateProfilePicture(selectedFile.value, {
          email: authStore.user?.email,
          username: authStore.user?.username,
        })
        selectedFile.value = null
      }

      const updateData = {
        email: authStore.user?.email, // Required by backend
        username: authStore.user?.username, // Include username
        first_name: form.value.first_name,
        last_name: form.value.last_name,
        bio: form.value.bio,
      }
      // Call update API
      await authService.updateProfile(updateData)
      await authStore.fetchProfile() // Refresh local user data
      showSuccessSnackbar.value = true // Show success message
      dialog.value = false
    } catch (error) {
      console.error('Failed to update profile', error)
    } finally {
      loading.value = false
    }
  }
</script>

<style scoped>
/* Modern Profile Card */
.profile-card {
  background: rgb(var(--v-theme-surface));
  border-radius: 24px !important;
  overflow: hidden;
}

/* Header with Royal Blue Gradient */
.profile-header {
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
  padding: 24px;
  padding-bottom: 80px;
  position: relative;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-text {
  color: white;
}

.header-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  margin-bottom: 4px;
}

.header-subtitle {
  font-size: 0.875rem;
  opacity: 0.8;
  margin: 0;
}

.close-btn {
  color: rgba(255, 255, 255, 0.8) !important;
}

.close-btn:hover {
  color: white !important;
  background: rgba(255, 255, 255, 0.1) !important;
}

/* Avatar Section */
.avatar-section {
  position: absolute;
  bottom: -60px;
  inset-inline-start: 50%;
  transform: translateX(-50% * var(--v-direction-multiplier, 1));
  text-align: center;
}

/* Simplified centering that works in both directions */
.v-locale--is-rtl .avatar-section {
  transform: translateX(50%);
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
}

.avatar-ring {
  border: 4px solid rgb(var(--v-theme-surface)) !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.camera-btn {
  position: absolute;
  bottom: 4px;
  inset-inline-end: 4px;
  background: linear-gradient(135deg, #1e40af, #3b82f6) !important;
  color: white !important;
  border: 3px solid rgb(var(--v-theme-surface)) !important;
  box-shadow: 0 2px 8px rgba(30, 64, 175, 0.4);
}

.camera-btn:hover {
  transform: scale(1.1);
}

/* Status Badge with Pulse Animation */
.status-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 8px;
}

.pulse-dot {
  width: 10px;
  height: 10px;
  background: #22c55e;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(34, 197, 94, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(34, 197, 94, 0);
  }
}

.status-text {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

/* Form Content */
.form-content {
  padding: 80px 24px 24px !important;
}

.field-row {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.field-group {
  flex: 1;
  margin-bottom: 20px;
}

.field-group.full-width {
  flex: 1 1 100%;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 8px;
}

.label-icon {
  color: #3b82f6;
}

.modern-input :deep(.v-field) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border-color: rgba(0, 0, 0, 0.08) !important;
  transition: all 0.2s ease;
}

.modern-input :deep(.v-field:hover) {
  border-color: #3b82f6 !important;
}

.modern-input :deep(.v-field--focused) {
  border-color: #3b82f6 !important;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.char-counter {
  text-align: left;
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 4px;
}

/* Info Cards */
.info-cards {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.info-card {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(59, 130, 246, 0.05);
  border-radius: 16px;
  border: 1px solid rgba(59, 130, 246, 0.1);
}

.info-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6, #60a5fa);
  border-radius: 12px;
  color: white;
}

.info-content {
  display: flex;
  flex-direction: column;
}

.info-label {
  font-size: 0.7rem;
  color: #64748b;
  font-weight: 500;
}

.info-value {
  font-size: 0.85rem;
  color: rgb(var(--v-theme-on-surface));
  font-weight: 600;
}

/* Action Buttons */
.action-buttons {
  padding: 16px 24px 24px !important;
  gap: 12px;
}

.cancel-btn {
  flex: 1;
  color: #64748b !important;
  border-color: #e2e8f0 !important;
}

.cancel-btn:hover {
  background: #f8fafc !important;
}

.save-btn {
  flex: 1;
  background: linear-gradient(135deg, #1e40af, #3b82f6) !important;
  font-weight: 600;
}

.save-btn:hover {
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
}

/* Success Dialog */
.success-dialog {
  border-radius: 24px !important;
  overflow: hidden;
  text-align: center;
}

.success-header {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  padding: 32px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.success-icon-wrapper {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: successPulse 1s ease-out;
}

@keyframes successPulse {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.success-content {
  padding: 24px !important;
}

.success-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: rgb(var(--v-theme-on-surface));
  margin: 0 0 8px 0;
}

.success-message {
  font-size: 0.95rem;
  color: #64748b;
  margin: 0;
}

.success-actions {
  padding: 0 24px 24px !important;
}

.success-btn {
  background: linear-gradient(135deg, #22c55e, #16a34a) !important;
  font-weight: 600;
}

.success-btn:hover {
  box-shadow: 0 4px 16px rgba(34, 197, 94, 0.4);
}
</style>
