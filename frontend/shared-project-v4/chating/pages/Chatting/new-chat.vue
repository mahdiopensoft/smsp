<template>
  <div class="new-chat-page">
    <div class="new-chat-page__glow glow-1" />
    <div class="new-chat-page__glow glow-2" />

    <v-card class="new-chat-hero" elevation="0">
      <div class="new-chat-hero__icon">
        <v-icon color="primary" size="44">mdi-forum-outline</v-icon>
      </div>

      <div class="new-chat-hero__content text-center">
        <div class="new-chat-hero__badge">تجربة محادثة حديثة</div>
        <h1 class="new-chat-hero__title">ابدأ محادثة جديدة بسهولة</h1>
        <p class="new-chat-hero__subtitle">
          تم تجهيز هذه الشاشة لتتكامل مع نظام الشات الحالي بنفس الهوية البصرية
          الحديثة، مع مساحة مخصصة لجهات الاتصال والمجموعات ونتائج البحث.
        </p>
      </div>

      <div class="new-chat-hero__features">
        <div class="feature-card">
          <v-icon color="primary" size="20">mdi-account-search-outline</v-icon>
          <span>بحث سريع عن المستخدمين</span>
        </div>
        <div class="feature-card">
          <v-icon color="info" size="20">mdi-account-group-outline</v-icon>
          <span>إنشاء مجموعات منظمة</span>
        </div>
        <div class="feature-card">
          <v-icon color="success" size="20">mdi-shield-check-outline</v-icon>
          <span>تصميم متوافق مع النظام</span>
        </div>
      </div>

      <div class="new-chat-hero__footer">
        <div class="footer-hint">
          <v-icon color="secondary" size="18">mdi-progress-clock</v-icon>
          <span>سيتم ربط جهات الاتصال الفعلية هنا عند تفعيل الشاشة.</span>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script setup>
// Placeholder for new chat functionality
</script>

<style scoped>
.new-chat-page {
  min-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: 28px;
  background:
    radial-gradient(circle at top right, rgba(var(--v-theme-primary), 0.08), transparent 28%),
    linear-gradient(180deg, rgba(var(--v-theme-surface), 0.96) 0%, rgba(var(--v-theme-surface), 0.9) 100%);
}

.new-chat-page__glow {
  position: absolute;
  width: 280px;
  height: 280px;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  pointer-events: none;
}

.glow-1 {
  top: -80px;
  inset-inline-start: -40px;
  background: rgba(var(--v-theme-primary), 0.18);
}

.glow-2 {
  bottom: -100px;
  inset-inline-end: -20px;
  background: rgba(var(--v-theme-info), 0.16);
}

.new-chat-hero {
  position: relative;
  z-index: 1;
  width: min(760px, 100%);
  padding: 32px;
  border-radius: 28px;
  border: 1px solid rgba(var(--v-border-color), 0.12);
  background:
    linear-gradient(135deg, rgba(var(--v-theme-primary), 0.04), transparent 24%),
    rgba(var(--v-theme-surface), 0.92);
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.08);
}

.new-chat-hero__icon {
  width: 76px;
  height: 76px;
  margin: 0 auto 20px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--v-theme-primary), 0.1);
  box-shadow: inset 0 0 0 1px rgba(var(--v-theme-primary), 0.08);
}

.new-chat-hero__badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 14px;
  margin-bottom: 16px;
  border-radius: 999px;
  background: rgba(var(--v-theme-primary), 0.08);
  color: rgb(var(--v-theme-primary));
  font-weight: 700;
  font-size: 0.8rem;
}

.new-chat-hero__title {
  margin: 0 0 14px;
  font-size: clamp(1.8rem, 2.4vw, 2.4rem);
  line-height: 1.2;
  color: rgba(var(--v-theme-on-surface), 0.92);
}

.new-chat-hero__subtitle {
  max-width: 560px;
  margin: 0 auto;
  line-height: 1.85;
  color: rgba(var(--v-theme-on-surface), 0.62);
  font-size: 1rem;
}

.new-chat-hero__features {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin-top: 28px;
}

.feature-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 18px;
  border-radius: 18px;
  background: rgba(var(--v-theme-on-surface), 0.02);
  border: 1px solid rgba(var(--v-border-color), 0.08);
  color: rgba(var(--v-theme-on-surface), 0.78);
  font-weight: 600;
}

.new-chat-hero__footer {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(var(--v-border-color), 0.08);
}

.footer-hint {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 14px;
  background: rgba(var(--v-theme-on-surface), 0.03);
  color: rgba(var(--v-theme-on-surface), 0.65);
}

@media (max-width: 840px) {
  .new-chat-hero__features {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .new-chat-page {
    padding: 16px;
  }

  .new-chat-hero {
    padding: 24px 18px;
    border-radius: 22px;
  }
}
</style>
