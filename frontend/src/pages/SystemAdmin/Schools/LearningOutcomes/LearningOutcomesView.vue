<template>
  <div class="d-flex align-center justify-center pa-12 text-center">
    <div>
      <v-icon size="64" color="warning" class="mb-4">mdi-alert-circle-outline</v-icon>
      <h2 class="text-h5 font-weight-bold mb-2">تم إلغاء شاشة مخرجات التعلم</h2>
      <p class="text-body-1 text-medium-emphasis mb-6">
        تمت إزالة نظام مخرجات التعلم من بنك الأسئلة والتهيئة الأكاديمية بالكامل.
      </p>
      <v-btn color="primary" rounded="lg" to="/" prepend-icon="mdi-home">
        العودة إلى الرئيسية
      </v-btn>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LearningOutcomesView',
  mounted() {
    this.$router.replace('/');
  },
};
</script>
