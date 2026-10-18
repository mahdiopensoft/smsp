<template>
  <v-dialog v-model="showWarining" persistent max-width="450">
    <v-card class="pa-5 text-center">
      <v-icon color="amber darken-2" size="64" class="mb-3">
        mdi-account-clock-outline
      </v-icon>
      <v-card-title class="text-h5 justify-center"> تنبية انتها الجلسة </v-card-title>
      <v-card-text class="text-body-1">
        لقد تتوقفت عن العمل لفترة , سيتم تسحيل خروجك تلقائياٌ خلال :
        <div class="text-h4 font-weight-bold color-error my-4">{{ countdown }} ثانية</div>
        هل تود البقاء متصلاٌ
      </v-card-text>
      <v-card-actions class="justify-center mt-2">
        <v-btn
          color="primary"
          variant="elevated"
          size="large"
          prepend-icon="mdi-refresh"
          @click="stayActive"
        >
          نعم , أرغب في البقاء
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script setup>
import { useAuthStore } from "../../src/UserManagement/stores/auth";
import { ref, onMounted, onUnmounted } from "vue";

// الاعدادات
const IDLE_TIME_LIMIT = 15 * 60 * 1000; // خمس دقائق بلملي ثانية
const WARNING_TIME = 60;

const showWarining = ref(false);
const countdown = ref(WARNING_TIME);

let warningTimer = null;
let logoutInterval = null;

// انشاء قناء اتصال بين التبويبات باسم session_channel
const broadcast = new BroadcastChannel("session_channel");

// الاحداث التي تعني ان المستخدم نشط
const activityEvents = ["click", "mousemove", "mousedown", "scroll", "keypress"];

//1- بدء العداد الرئيسي
const startMainTimer = () => {
  // نحسب وقت التنبية (الوقت الكلي ناقص وقت العد التنازلي )
  const timeBeforeShowingDialog = IDLE_TIME_LIMIT - WARNING_TIME * 1000;

  warningTimer = setTimeout(() => {
    showWarining.value = true;
    startCountdown();
  }, timeBeforeShowingDialog);
};
// 2- بدء العد التنازلي للديالوق عند الظهور
const startCountdown = () => {
  countdown.value = WARNING_TIME;
  logoutInterval = setInterval(() => {
    countdown.value--;
    if (countdown.value <= 0) {
      logoutUser();
    }
  }, 1000);
};
// 3-تصفير كل العدادات
const resetAllTimers = () => {
  clearTimeout(warningTimer);
  clearInterval(logoutInterval);
};

// 4- دالة تسجيل الخروج
const logoutUser = async () => {
  resetAllTimers();
  broadcast.postMessage("force_logout");

  performLogout();
};
// 5- الضغط على زر البقاء
const stayActive = () => {
  showWarining.value = false;
  resetAllTimers();
  startMainTimer();
  // اخبار التبويبات الاخرى ان المستخدم ضغط على البقاء
  broadcast.postMessage("reset_timer");
};

// 6- تصفير العداد عند اي حركة فقط اذا كان الحوار غير مفتوح
const handleUserActivity = () => {
  if (!showWarining.value) {
    resetAllTimers();
    startMainTimer();
    broadcast.postMessage("reset_timer");
  }
};

// الاستماع للرسائل القادمة من التبيوبات الاخرى
broadcast.onmessage = (event) => {
  if (event.data === "reset_timer") {
    showWarining.value = false;
    resetAllTimers();
    startMainTimer();
  } else if (event.data === "force_logout") {
    performLogout();
  }
};

const performLogout = async () => {
  const authStore = useAuthStore();
  if (authStore.isSSO) await authStore.fullLogout();
  else await authStore.logout();

  window.location.reload();
};

// دورة حياة المكون
onMounted(() => {
  activityEvents.forEach((event) => {
    window.addEventListener(event, handleUserActivity);
  });
  startMainTimer();
});

onUnmounted(() => {
  activityEvents.forEach((event) => {
    window.removeEventListener(event, handleUserActivity);
  });
  resetAllTimers();
  broadcast.close();
});
</script>
<style scoped>
.color-error {
  color: #ff5252;
}
</style>
