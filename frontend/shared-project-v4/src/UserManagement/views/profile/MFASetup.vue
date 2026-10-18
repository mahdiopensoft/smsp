<template>
  <div class="mfa-setup">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <v-progress-circular indeterminate color="primary" size="40" />
      <p class="text-grey mt-3">جاري تحميل حالة المصادقة الثنائية...</p>
    </div>

    <!-- ═══ MFA Enabled State ═══ -->
    <div v-else-if="mfaStatus?.is_enabled" class="mfa-enabled">
      <div class="status-card enabled">
        <div class="status-icon-wrapper">
          <v-icon size="40" color="success">mdi-shield-check</v-icon>
        </div>
        <h3 class="status-title">المصادقة الثنائية مفعّلة ✅</h3>
        <p class="status-desc">حسابك محمي بطبقة أمان إضافية</p>

        <div class="status-details mt-4">
          <div class="detail-item">
            <v-icon size="18" class="me-2" color="grey">mdi-key-variant</v-icon>
            <span
              >رموز الاسترداد المتبقية:
              <strong>{{ mfaStatus.backup_codes_remaining }}</strong></span
            >
          </div>
          <div class="detail-item" v-if="mfaStatus.last_used_at">
            <v-icon size="18" class="me-2" color="grey">mdi-clock-outline</v-icon>
            <span>آخر استخدام: {{ formatDate(mfaStatus.last_used_at) }}</span>
          </div>
        </div>

        <!-- Disable MFA -->
        <v-btn
          color="error"
          variant="tonal"
          class="mt-6"
          @click="showDisableDialog = true"
          style="text-transform: none; border-radius: 12px"
        >
          <v-icon start>mdi-shield-off</v-icon>
          تعطيل المصادقة الثنائية
        </v-btn>
      </div>
    </div>

    <!-- ═══ MFA Not Enabled ═══ -->
    <div v-else-if="setupStep === 'intro'" class="mfa-intro">
      <div class="status-card disabled">
        <div class="status-icon-wrapper">
          <v-icon size="40" color="warning">mdi-shield-alert-outline</v-icon>
        </div>
        <h3 class="status-title">المصادقة الثنائية غير مفعّلة</h3>
        <p class="status-desc">فعّل المصادقة الثنائية لحماية حسابك بطبقة أمان إضافية</p>

        <!-- App Recommendations -->
        <div class="app-recommendations mt-5">
          <h4 class="text-subtitle-2 font-weight-bold mb-3">
            <v-icon size="18" class="me-1">mdi-cellphone</v-icon>
            تطبيقات المصادقة المُوصى بها:
          </h4>
          <div class="app-list">
            <div class="app-item">
              <v-icon color="blue" size="24">mdi-google</v-icon>
              <div>
                <strong>Google Authenticator</strong>
                <span class="app-platform">iOS / Android</span>
              </div>
            </div>
            <div class="app-item">
              <v-icon color="red" size="24">mdi-cellphone-key</v-icon>
              <div>
                <strong>Authy (Twilio)</strong>
                <span class="app-platform"
                  >iOS / Android / Desktop — يدعم النسخ الاحتياطي</span
                >
              </div>
            </div>
            <div class="app-item">
              <v-icon color="blue-darken-3" size="24">mdi-microsoft</v-icon>
              <div>
                <strong>Microsoft Authenticator</strong>
                <span class="app-platform">iOS / Android</span>
              </div>
            </div>
          </div>
        </div>

        <v-btn
          color="primary"
          size="large"
          class="mt-6"
          @click="startSetup"
          :loading="setupLoading"
          style="text-transform: none; border-radius: 12px; font-weight: 600"
        >
          <v-icon start>mdi-shield-plus</v-icon>
          تفعيل المصادقة الثنائية
        </v-btn>
      </div>
    </div>

    <!-- ═══ Step 2: QR Code ═══ -->
    <div v-else-if="setupStep === 'qr'" class="mfa-qr-step">
      <h3 class="text-h6 font-weight-bold mb-2">الخطوة 1: امسح رمز QR</h3>
      <p class="text-body-2 text-grey mb-4">
        افتح تطبيق المصادقة وامسح الرمز التالي لإضافة حسابك
      </p>

      <!-- QR Code -->
      <div class="qr-container">
        <QrcodeVue :value="setupData.provisioning_uri" :size="220" />

        <img
          v-if="setupData.qr_code_base64"
          :src="'data:image/png;base64,' + setupData.qr_code_base64"
          alt="MFA QR Code"
          class="qr-image"
        />
      </div>

      <!-- Manual Entry -->
      <v-expansion-panels variant="accordion" class="mt-4 mb-4">
        <v-expansion-panel>
          <v-expansion-panel-title>
            <v-icon size="18" class="me-2">mdi-keyboard</v-icon>
            لا يمكنك مسح الرمز؟ أدخل المفتاح يدوياً
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-text-field
              :model-value="setupData.secret_key"
              readonly
              variant="outlined"
              density="compact"
              dir="ltr"
              append-inner-icon="mdi-content-copy"
              @click:append-inner="copySecret"
              class="mt-2"
            />
            <p class="text-caption text-grey">
              انسخ هذا المفتاح والصقه في تطبيق المصادقة
            </p>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>

      <!-- OTP Verify -->
      <h3 class="text-h6 font-weight-bold mb-2">الخطوة 2: أدخل رمز التحقق</h3>
      <p class="text-body-2 text-grey mb-3">
        أدخل الرمز المكوّن من 6 أرقام الظاهر في تطبيق المصادقة
      </p>

      <div class="otp-verify-section">
        <v-text-field
          v-model="verifyCode"
          label="رمز التحقق"
          placeholder="000000"
          prepend-inner-icon="mdi-numeric"
          variant="outlined"
          dir="ltr"
          maxlength="6"
          class="otp-input"
          hide-details
          @keyup.enter="verifyAndEnable"
        />
        <v-btn
          color="primary"
          size="large"
          :loading="verifyLoading"
          :disabled="verifyCode.length < 6"
          @click="verifyAndEnable"
          style="text-transform: none; border-radius: 12px"
        >
          <v-icon start>mdi-check-circle</v-icon>
          تفعيل
        </v-btn>
      </div>

      <v-alert
        v-if="errorMsg"
        type="error"
        variant="tonal"
        density="compact"
        class="mt-3"
        closable
        @click:close="errorMsg = ''"
      >
        {{ errorMsg }}
      </v-alert>

      <v-btn
        variant="text"
        color="grey"
        class="mt-2"
        @click="setupStep = 'intro'"
        style="text-transform: none"
      >
        <v-icon start>mdi-arrow-right</v-icon>
        رجوع
      </v-btn>
    </div>

    <!-- ═══ Step 3: Backup Codes ═══ -->
    <div v-else-if="setupStep === 'backup'" class="mfa-backup-step">
      <v-alert type="warning" variant="tonal" class="mb-4" style="border-radius: 12px">
        <strong>⚠️ مهم جداً!</strong> احفظ رموز الاسترداد التالية في مكان آمن. لن يتم
        عرضها مرة أخرى. استخدمها إذا فقدت الوصول لتطبيق المصادقة.
      </v-alert>

      <div class="backup-codes-grid">
        <div v-for="(code, i) in backupCodes" :key="i" class="backup-code-item">
          <span class="code-number">{{ i + 1 }}.</span>
          <code class="code-value">{{ code }}</code>
        </div>
      </div>

      <div class="backup-actions mt-4">
        <v-btn
          variant="tonal"
          color="primary"
          @click="copyBackupCodes"
          style="text-transform: none; border-radius: 10px"
        >
          <v-icon start>mdi-content-copy</v-icon>
          نسخ الرموز
        </v-btn>
        <v-btn
          variant="tonal"
          color="secondary"
          @click="downloadBackupCodes"
          style="text-transform: none; border-radius: 10px"
        >
          <v-icon start>mdi-download</v-icon>
          تحميل كملف
        </v-btn>
      </div>

      <v-btn
        color="success"
        size="large"
        block
        class="mt-6"
        @click="finishSetup"
        style="text-transform: none; border-radius: 12px; font-weight: 600"
      >
        <v-icon start>mdi-check-all</v-icon>
        تم — لقد حفظت الرموز
      </v-btn>
    </div>

    <!-- ═══ Disable MFA Dialog ═══ -->
    <v-dialog v-model="showDisableDialog" max-width="400" persistent>
      <v-card class="pa-5" style="border-radius: 16px">
        <div class="text-center mb-4">
          <v-icon size="48" color="error">mdi-shield-off-outline</v-icon>
          <h3 class="text-h6 font-weight-bold mt-2">تعطيل المصادقة الثنائية</h3>
          <p class="text-body-2 text-grey mt-1">أدخل رمز التحقق لتأكيد هويتك</p>
        </div>
        <v-text-field
          v-model="disableCode"
          label="رمز التحقق"
          placeholder="000000"
          prepend-inner-icon="mdi-numeric"
          variant="outlined"
          dir="ltr"
          maxlength="6"
          hide-details
          class="mb-3"
        />
        <v-alert
          v-if="disableError"
          type="error"
          variant="tonal"
          density="compact"
          class="mb-3"
        >
          {{ disableError }}
        </v-alert>
        <v-card-actions class="justify-center gap-2 pa-0">
          <v-btn
            color="error"
            :loading="disableLoading"
            :disabled="disableCode.length < 6"
            @click="disableMFA"
            style="text-transform: none; border-radius: 10px"
          >
            تعطيل
          </v-btn>
          <v-btn
            variant="text"
            @click="
              showDisableDialog = false;
              disableCode = '';
              disableError = '';
            "
            style="text-transform: none"
          >
            إلغاء
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackColor" timeout="3000" location="bottom">
      {{ snackMsg }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { mfaApi } from "../../api/mfa";
import QrcodeVue from "qrcode.vue";
import { useAuthStore } from "../../stores/auth";

const emit = defineEmits(["finshMFASetup"]);

const authStore = useAuthStore();

const loading = ref(false);
const mfaStatus = ref(null);
const setupStep = ref("intro");
const setupData = ref({});
const setupLoading = ref(false);
const verifyCode = ref("");
const verifyLoading = ref(false);
const backupCodes = ref([]);
const errorMsg = ref("");

const showDisableDialog = ref(false);
const disableCode = ref("");
const disableLoading = ref(false);
const disableError = ref("");

const snackbar = ref(false);
const snackMsg = ref("");
const snackColor = ref("success");

const showSnack = (msg, color = "success") => {
  snackMsg.value = msg;
  snackColor.value = color;
  snackbar.value = true;
};

const loadStatus = async () => {
  loading.value = true;
  try {
    const res = await mfaApi.getStatus();
    mfaStatus.value = res.data || res;
  } catch (e) {
    console.error("Failed to load MFA status:", e);
  } finally {
    loading.value = false;
  }
};

const startSetup = async () => {
  setupLoading.value = true;
  try {
    const res = await mfaApi.setup();
    setupData.value = res.data || res;
    setupStep.value = "qr";
  } catch (e) {
    showSnack("فشل بدء إعداد MFA", "error");
  } finally {
    setupLoading.value = false;
  }
};

const verifyAndEnable = async () => {
  if (verifyCode.value.length < 6) return;
  verifyLoading.value = true;
  errorMsg.value = "";
  try {
    const res = await mfaApi.verifyAndEnable(verifyCode.value);
    const payload = res.data || res;
    backupCodes.value = payload.backup_codes || [];
    setupStep.value = "backup";
    showSnack("تم تفعيل المصادقة الثنائية بنجاح! 🎉");
  } catch (e) {
    errorMsg.value = e.response?.data?.message || "رمز التحقق غير صحيح";
    verifyCode.value = "";
  } finally {
    verifyLoading.value = false;
  }
};

const disableMFA = async () => {
  disableLoading.value = true;
  disableError.value = "";
  try {
    await mfaApi.disable(disableCode.value);
    showDisableDialog.value = false;
    disableCode.value = "";
    showSnack("تم تعطيل المصادقة الثنائية");
    // await loadStatus()
  } catch (e) {
    disableError.value = e.response?.data?.message || "رمز التحقق غير صحيح";
  } finally {
    disableLoading.value = false;
  }
};

const finishSetup = () => {
  authStore.mfaRegester = false;
  authStore.mfaPending = true;
  setupStep.value = "intro";
  backupCodes.value = [];
  emit("finshMFASetup");
  // loadStatus()
};

const copySecret = () => {
  navigator.clipboard.writeText(setupData.value.secret_key || "");
  showSnack("تم نسخ المفتاح");
};

const copyBackupCodes = () => {
  const text = backupCodes.value.map((c, i) => `${i + 1}. ${c}`).join("\n");
  navigator.clipboard.writeText(text);
  showSnack("تم نسخ رموز الاسترداد");
};

const downloadBackupCodes = () => {
  const text =
    `OpenSoftCoreV3 — رموز الاسترداد للمصادقة الثنائية\n${"=".repeat(50)}\n\n` +
    backupCodes.value.map((c, i) => `${i + 1}. ${c}`).join("\n") +
    `\n\n⚠️ كل رمز يُستخدم مرة واحدة فقط.\nتاريخ الإنشاء: ${new Date().toLocaleString(
      "ar-SA"
    )}`;
  const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "mfa-backup-codes.txt";
  a.click();
  URL.revokeObjectURL(url);
};

const formatDate = (d) => {
  if (!d) return "";
  return new Date(d).toLocaleString("ar-SA", { dateStyle: "medium", timeStyle: "short" });
};

// onMounted(loadStatus)
</script>

<style scoped>
.mfa-setup {
  max-width: 560px;
  margin: 0 auto;
  padding: 16px 0;
}

.status-card {
  text-align: center;
  padding: 32px 24px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
}

.status-card.enabled {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.04), rgba(34, 197, 94, 0.01));
  border-color: rgba(34, 197, 94, 0.2);
}

.status-card.disabled {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.04), rgba(251, 191, 36, 0.01));
  border-color: rgba(251, 191, 36, 0.2);
}

.status-icon-wrapper {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.04);
  margin-bottom: 16px;
}

.status-title {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.status-desc {
  font-size: 14px;
  color: #64748b;
}

.status-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
}

.detail-item {
  display: flex;
  align-items: center;
  font-size: 13px;
  color: #475569;
}

.app-recommendations {
  text-align: start;
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
}

.app-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.app-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-item strong {
  font-size: 14px;
  display: block;
  color: #1e293b;
}

.app-platform {
  font-size: 12px;
  color: #94a3b8;
}

.qr-container {
  display: flex;
  justify-content: center;
  padding: 16px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
}

.qr-image {
  width: 220px;
  height: 220px;
  image-rendering: pixelated;
}

.otp-verify-section {
  display: flex;
  gap: 12px;
  align-items: start;
}

.otp-input {
  max-width: 200px;
}

.backup-codes-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  background: #f8fafc;
  padding: 16px;
  border-radius: 12px;
  border: 1px dashed #cbd5e1;
}

.backup-code-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: #fff;
  border-radius: 8px;
}

.code-number {
  font-size: 12px;
  color: #94a3b8;
  min-width: 18px;
}

.code-value {
  font-family: "Courier New", monospace;
  font-size: 14px;
  font-weight: 700;
  color: #1e293b;
  letter-spacing: 1px;
}

.backup-actions {
  display: flex;
  gap: 8px;
  justify-content: center;
}
</style>
