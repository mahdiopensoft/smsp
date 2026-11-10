<template>
  <div class="error-server-container">
    <div class="error-icon-wrapper">
      <v-icon size="48" color="error">mdi-server-off</v-icon>
    </div>
    <h3 class="error-title">خطأ في الاتصال</h3>
    <p class="error-description">تعذر الوصول إلى الخادم حالياً، يرجى المحاولة مرة أخرى.</p>
    <div class="error-actions">
      <custom-btn 
        type="refresh" 
        label="إعادة المحاولة"
        variant="tonal"
        color="error"
        @click="click"
      />
    </div>
  </div>
</template>

<script>
export default {
  emits: ['click'],
  methods: {
    click() {
      this.$emit('click')
    }
  },
}
</script>

<style scoped>
.error-server-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-xl);
  text-align: center;
  gap: var(--space-sm);
  background: rgba(var(--v-theme-error), 0.02);
  border-radius: var(--radius-xl);
  border: 1px solid rgba(var(--v-theme-error), 0.08);
}

.error-icon-wrapper {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--v-theme-error), 0.08);
  border-radius: var(--radius-full);
  margin-bottom: var(--space-xs);
}

.error-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: rgb(var(--v-theme-on-surface));
  margin: 0;
}

.error-description {
  font-size: 0.9rem;
  color: rgba(var(--v-theme-on-surface), 0.6);
  max-width: 300px;
  line-height: 1.6;
  margin: 0;
}

.error-actions {
  margin-top: var(--space-sm);
}
</style>