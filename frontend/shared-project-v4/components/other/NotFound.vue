<template>
  <div class="not-found-container">
    <div class="not-found-visual">
      <div class="visual-circle">
        <v-icon size="40" color="primary">mdi-database-off-outline</v-icon>
      </div>
    </div>
    <div class="not-found-text">
      <h3 class="not-found-title">لا توجد بيانات</h3>
      <p class="not-found-desc">لم يتم العثور على أي سجلات في هذا القسم حالياً.</p>
    </div>
  </div>
</template>

<style scoped>
.not-found-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  gap: 16px;
  min-height: 300px;
  text-align: center;
  width: 100%;
}

.not-found-visual {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.visual-circle {
  width: 72px;
  height: 72px;
  background: rgba(var(--v-theme-primary), 0.06);
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
}

.not-found-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.not-found-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: rgb(var(--v-theme-on-surface));
  margin: 0;
}

.not-found-desc {
  font-size: 0.875rem;
  color: rgba(var(--v-theme-on-surface), 0.5);
  max-width: 260px;
  margin: 0 auto;
}
</style>