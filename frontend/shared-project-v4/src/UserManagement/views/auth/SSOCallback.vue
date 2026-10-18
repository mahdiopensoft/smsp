<template>
  <v-container fluid class="fill-height d-flex align-center justify-center">
    <v-card class="pa-8 text-center" max-width="400" elevation="8">
      <!-- Loading State -->
      <template v-if="loading">
        <v-progress-circular
          indeterminate
          size="80"
          width="6"
          color="primary"
          class="mb-4"
        ></v-progress-circular>
        <h2 class="text-h5 mb-2">جاري معالجة تسجيل الدخول</h2>
        <p class="text-body-2 text-grey">الرجاء الانتظار...</p>
      </template>

      <!-- Error State -->
      <template v-else-if="error">
        <v-icon size="80" color="error" class="mb-4">mdi-alert-circle</v-icon>
        <h2 class="text-h5 mb-2">فشل تسجيل الدخول</h2>
        <v-alert type="error" variant="tonal" class="mb-4 text-start">
          {{ error }}
        </v-alert>
        <v-btn color="primary" :to="{ name: 'Login' }">
          <v-icon start>mdi-arrow-left</v-icon>
          العودة لتسجيل الدخول
        </v-btn>
      </template>

      <!-- Success State -->
      <template v-else>
        <v-icon size="80" color="success" class="mb-4">mdi-check-circle</v-icon>
        <h2 class="text-h5 mb-2">تم تسجيل الدخول بنجاح</h2>
        <p class="text-body-2 text-grey mb-4">جاري التوجيه...</p>
      </template>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "../../stores/auth";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  const { code, state, error: errorParam, error_description } = route.query;

  // Check for error from Keycloak
  if (errorParam) {
    error.value = error_description || errorParam;
    loading.value = false;
    return;
  }

  // Must have code and state
  if (!code || !state) {
    error.value = "معاملات غير صالحة";
    loading.value = false;
    return;
  }

  try {
    // Exchange code for tokens
    await authStore.handleSSOCallback(code, state);

    loading.value = false;

    // Small delay before redirect
    setTimeout(() => {
      router.push("/");
    }, 1000);
  } catch (err) {
    error.value = err.response?.data?.message || err.message || "فشل معالجة تسجيل الدخول";
    loading.value = false;
  }
});
</script>

<style scoped>
.v-container {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  min-height: 100vh;
}
</style>
