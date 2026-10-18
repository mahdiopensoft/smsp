<template>
  <v-dialog
    v-model="isOpen"
    max-width="600"
    persistent
    transition="dialog-bottom-transition"
  >
    <v-card v-if="announcement" elevation="10" class="rounded-lg">
      <v-card-item :class="headerColor">
        <v-card-title class="text-h5 font-weight-bold d-flex align-center">
          <v-icon :icon="headerIcon" class="mr-2" size="32"></v-icon>
          {{ announcement.title }}
        </v-card-title>
      </v-card-item>

      <v-card-text class="pt-6 pb-6 text-body-1" style="line-height: 1.8;">
        <!-- إذا كان هناك صورة مرفقة -->
        <v-img
          v-if="announcement.attachment"
          :src="announcement.attachment"
          max-height="300"
          cover
          class="mb-4 rounded"
        ></v-img>

        <div v-html="formattedMessage"></div>

        <div v-if="announcement.action_url" class="mt-6 text-center">
          <v-btn
            :href="announcement.action_url"
            target="_blank"
            color="primary"
            elevation="2"
            size="large"
            rounded="pill"
          >
            الانتقال للرابط المرفق
            <v-icon right icon="mdi-open-in-new" class="ml-2"></v-icon>
          </v-btn>
        </div>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="pa-4 bg-grey-lighten-4 justify-end">
        <span class="text-caption text-grey mr-auto">
          {{ formattedDate }}
        </span>
        <v-btn
          color="primary"
          variant="elevated"
          @click="markAsRead"
          :loading="loading"
        >
          حسناً، قرأت ذلك
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { computed, ref } from "vue";
import { useNotificationStore } from "../../store/notificationStore";
import { systemNotificationService } from "../../services/systemNotificationService"
 

export default {
  name: "SystemAnnouncementDialog",
  setup() {
    const store = useNotificationStore();
    const loading = ref(false);

    const announcement = computed(() => store.activeAnnouncement);
    const isOpen = computed(() => !!store.activeAnnouncement);

    const headerColor = computed(() => {
      if (!announcement.value) return "bg-primary text-white";
      if (announcement.value.priority === "high") return "bg-error text-white";
      if (announcement.value.event_type === "warning") return "bg-warning text-white";
      return "bg-primary text-white";
    });

    const headerIcon = computed(() => {
      if (!announcement.value) return "mdi-bullhorn";
      if (announcement.value.priority === "high") return "mdi-alert-octagon";
      return "mdi-bullhorn-outline";
    });

    const formattedMessage = computed(() => {
      if (!announcement.value || !announcement.value.message) return "";
      // تحويل الفراغات الجديدة إلى <br>
      return announcement.value.message.replace(/\n/g, "<br>");
    });

    const formattedDate = computed(() => {
      if (!announcement.value || !announcement.value.created_at) return "";
      return new Date(announcement.value.created_at).toLocaleString("ar-SA");
    });

    const markAsRead = async () => {
      if (!announcement.value) return;
      loading.value = true;
      try {
        await systemNotificationService.markAsRead(announcement.value.id);
      } catch (err) {
        console.error("Failed to mark as read", err);
      } finally {
        loading.value = false;
        store.clearActiveAnnouncement();
        
        // التحقق مما إذا كان هناك إشعارات غير مقروءة أخرى
        // لو أردنا إظهار إشعار آخر فوراً يمكننا البحث في systemNotifications
      }
    };

    return {
      isOpen,
      announcement,
      headerColor,
      headerIcon,
      formattedMessage,
      formattedDate,
      markAsRead,
      loading,
    };
  },
};
</script>
