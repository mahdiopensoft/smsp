<template>
  <v-container fluid class="fill-height callback-container justify-center align-center">
    <v-card class="pa-8 text-center callback-card" max-width="450" elevation="12">
      <!-- Loading State -->
      <template v-if="loading">
        <div class="loading-animation mb-6">
          <v-progress-circular indeterminate size="100" width="8" color="primary">
            <v-icon size="40" color="primary">mdi-key</v-icon>
          </v-progress-circular>
        </div>
        <h2 class="text-h5 mb-2 font-weight-bold">جاري معالجة تسجيل الدخول</h2>
        <p class="text-body-1 text-grey-darken-1">
          يرجى الانتظار بينما نتحقق من بياناتك...
        </p>
        <v-progress-linear
          indeterminate
          color="primary"
          class="mt-4"
          rounded
        ></v-progress-linear>
      </template>

      <!-- Success State -->
      <template v-else-if="success">
        <div class="success-animation mb-6">
          <v-icon size="100" color="success" class="bounce">mdi-check-circle</v-icon>
        </div>
        <h2 class="text-h5 mb-2 font-weight-bold text-success">تم تسجيل الدخول بنجاح!</h2>
        <p class="text-body-1 text-grey-darken-1 mb-4">
          مرحباً {{ userName }}, جاري توجيهك...
        </p>
        <v-progress-linear
          :model-value="redirectProgress"
          color="success"
          height="8"
          rounded
        ></v-progress-linear>
      </template>

      <!-- Error State -->
      <template v-else-if="error">
        <v-icon size="100" color="error" class="mb-4">mdi-alert-circle</v-icon>
        <h2 class="text-h5 mb-4 font-weight-bold text-error">فشل تسجيل الدخول</h2>
        <v-alert type="error" variant="tonal" class="mb-6 text-start">
          {{ error }}
        </v-alert>
        <v-btn color="primary" size="large" :to="{ name: 'SSOLogIn' }" block>
          <v-icon start>mdi-refresh</v-icon>
          إعادة المحاولة
        </v-btn>
        <v-btn
          color="grey-darken-1"
          variant="text"
          class="mt-2"
          :to="{ name: 'Login' }"
          block
        >
          <v-icon start>mdi-arrow-left</v-icon>
          العودة لتسجيل الدخول
        </v-btn>
      </template>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore, AUTH_MODES } from "../../stores/auth";
import { ssoApi } from "../../api/sso";
import { state } from "@/../src/store/state";
import { getRouter } from "../../../router/routerInstance";

const router = getRouter();
// const router = useRouter();

const userName = state?.profile?.username;

const route = useRoute();
const authStore = useAuthStore();

const loading = ref(true);
const success = ref(false);
const error = ref(null);
const redirectProgress = ref(0);

let progressInterval = null;

const startRedirectProgress = () => {
  progressInterval = setInterval(() => {
    redirectProgress.value += 20;
    if (redirectProgress.value >= 100) {
      clearInterval(progressInterval);
      // Redirect to dashboard or intended destination
      // const redirectTo = sessionStorage.getItem("auth_redirect") || "/";
      sessionStorage.removeItem("auth_redirect");

      // If opened in popup, notify parent and close
      if (window.opener && !window.opener.closed) {
        window.opener.postMessage(
          {
            type: "sso_success",
            token: authStore.accessToken,
            refreshToken: authStore.refreshToken,
          },
          window.location.origin
        );
        window.close();
      } else {
        // console.log(redirectTo);
        // router.push({path:redirectTo})
        // router.go(0)

        // window.location.href = redirectTo
        // window.location.href = "/system-selector";
        // window.location.href = "/system-selector";
        router.push({ name: "SystemSelector" });
      }
    }
  }, 200);
};

onMounted(async () => {
  // Get parameters from URL query params (from backend redirect)

  const query = new URLSearchParams(window.location.search);
  const access_token = query.get("access_token");
  const refresh_token = query.get("refresh_token");
  const id_token = query.get("id_token");
  const errorParam = query.get("errorParam");
  const description = query.get("description");
  const code = query.get("code");
  const state = query.get("state");

  // ═══════════════════════════════════════════════════════════════
  // Flow 1: One-Time Code Exchange (BFF Pattern — Preferred & Secure)
  // Backend redirects with ?code=<one-time-code>
  // We POST to /sso/exchange-code/ to get access_token securely.
  // ═══════════════════════════════════════════════════════════════
  if (code && !state) {
    try {
      const tokenData = await ssoApi.exchangeCode(code);
      const accessToken = tokenData.access_token;

      if (!accessToken) {
        error.value = "لم يتم استلام رمز الوصول من الخادم";
        loading.value = false;
        return;
      }

      // Store access token in auth store (refresh/id tokens are in HttpOnly cookies)
      authStore.setTokens(accessToken, null, AUTH_MODES.SSO_KEYCLOAK, null);

      // Decode JWT to get user info
      try {
        const payload = JSON.parse(atob(accessToken.split(".")[1]));
        authStore.user = {
          username: payload.preferred_username || payload.email || payload.sub,
          email: payload.email,
          first_name: payload.given_name || payload.name?.split(" ")[0] || "",
          last_name:
            payload.family_name || payload.name?.split(" ").slice(1).join(" ") || "",
          sub: payload.sub,
          ...payload,
        };
      } catch (decodeErr) {
        console.warn("Could not decode JWT, trying API:", decodeErr);
        await new Promise((resolve) => setTimeout(resolve, 100));
        await authStore.fetchSSOUserInfo();
      }

      success.value = true;
      loading.value = false;
      startRedirectProgress();
    } catch (err) {
      console.error("Code exchange failed:", err);
      error.value = err.response?.data?.message || "فشل في استبدال رمز المصادقة";
      loading.value = false;
    }
    return;
  }

  // ═══════════════════════════════════════════════════════════════
  // Flow 2: Direct token delivery (Legacy — kept for backward compatibility)
  // ═══════════════════════════════════════════════════════════════
  if (access_token) {
    try {
      // Store tokens in auth store (including id_token for logout)
      authStore.setTokens(
        access_token,
        refresh_token || null,
        AUTH_MODES.SSO_KEYCLOAK,
        id_token || null
      );

      // Decode JWT to get user info (without calling API)
      try {
        const payload = JSON.parse(atob(access_token.split(".")[1]));
        authStore.user = {
          username: payload.preferred_username || payload.email || payload.sub,
          email: payload.email,
          first_name: payload.given_name || payload.name?.split(" ")[0] || "",
          last_name:
            payload.family_name || payload.name?.split(" ").slice(1).join(" ") || "",
          sub: payload.sub,
          ...payload,
        };
      } catch (decodeErr) {
        console.warn("Could not decode JWT, trying API:", decodeErr);
        // Fallback: try to fetch user info from API
        // Wait a tick for persistence
        await new Promise((resolve) => setTimeout(resolve, 100));
        await authStore.fetchSSOUserInfo();
      }

      success.value = true;
      loading.value = false;

      // Start progress animation for redirect
      startRedirectProgress();
    } catch (err) {
      console.error("Failed to process tokens:", err);
      error.value = "فشل في معالجة رمز الوصول";
      loading.value = false;
    }
    return;
  }

  // ═══════════════════════════════════════════════════════════════
  // Flow 3: Error received from backend
  // ═══════════════════════════════════════════════════════════════
  if (errorParam) {
    error.value = description || getErrorMessage(errorParam);
    loading.value = false;
    return;
  }

  // ═══════════════════════════════════════════════════════════════
  // Flow 4: Authorization code flow (fallback - code + state exchange)
  // ═══════════════════════════════════════════════════════════════
  if (code && state) {
    try {
      await authStore.handleSSOCallback(code, state);

      success.value = true;
      loading.value = false;
      startRedirectProgress();
    } catch (err) {
      console.error("Auth callback error:", err);
      error.value =
        err.response?.data?.message || err.message || "فشل معالجة تسجيل الدخول";
      loading.value = false;
    }
    return;
  }

  // ═══════════════════════════════════════════════════════════════
  // Flow 5: No valid parameters - show error
  // ═══════════════════════════════════════════════════════════════
  error.value = "لم يتم استلام بيانات المصادقة";
  loading.value = false;
});

onUnmounted(() => {
  if (progressInterval) {
    clearInterval(progressInterval);
  }
});

// Map error codes to user-friendly messages
function getErrorMessage(code) {
  const errorMessages = {
    access_denied: "تم رفض الوصول. قد تكون قد ألغيت عملية تسجيل الدخول.",
    invalid_request: "طلب غير صالح. يرجى المحاولة مرة أخرى.",
    unauthorized_client: "العميل غير مصرح له.",
    unsupported_response_type: "نوع الاستجابة غير مدعوم.",
    invalid_scope: "النطاق المطلوب غير صالح.",
    server_error: "حدث خطأ في الخادم. يرجى المحاولة لاحقاً.",
    temporarily_unavailable: "الخدمة غير متاحة مؤقتاً.",
    login_required: "يجب تسجيل الدخول أولاً.",
    consent_required: "الموافقة مطلوبة للمتابعة.",
    token_exchange_failed: "فشل في تبادل الرمز. يرجى المحاولة مرة أخرى.",
    missing_code: "لم يتم استلام رمز التفويض.",
    no_token: "لم يتم استلام رمز الوصول.",
  };
  return errorMessages[code] || `خطأ: ${code}`;
}
</script>

<style scoped>
.callback-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.callback-card {
  border-radius: 16px;
  backdrop-filter: blur(10px);
}

.loading-animation {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}

.success-animation .bounce {
  animation: bounce 0.6s ease-out;
}

@keyframes bounce {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}
</style>
