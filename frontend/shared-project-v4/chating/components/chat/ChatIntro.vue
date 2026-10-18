<template>
  <div
    class="chat-intro-container d-flex flex-column align-center justify-center text-center h-100 pa-10 overflow-hidden"
  >
    <div class="intro-content z-index-1">
      <!-- Icon Composition -->
      <div class="icon-composition mb-10">
        <div class="icon-wrapper main-icon-box">
          <v-icon class="main-icon shadow-lg" color="primary" size="160"
            >mdi-chat-processing</v-icon
          >
        </div>
      </div>

      <!-- Text Content -->
      <h1 class="font-weight-bold text-high-emphasis mb-4 gradient-text">
        {{ $t("chat.intro.title") }}
      </h1>

      <p
        class="text-medium-emphasis mb-10 mx-auto font-weight-regular"
        style="max-width: 600px; line-height: 1.6"
      >
        {{ $t("chat.intro.subtitle") }}
      </p>

      <!-- Security Footer -->
      <div
        class="security-footer py-3 px-6 rounded-pill glass-card d-inline-flex align-center gap-2 text-medium-emphasis mx-auto mt-6"
      >
        <v-icon color="success" size="18">mdi-lock</v-icon>
        <span class="font-weight-medium">{{
          $t("chat.intro.encryption")
        }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
// No extra logic needed for the intro screen
</script>

<style scoped>
.chat-intro-container {
  background: radial-gradient(
      circle at top,
      rgba(var(--v-theme-primary), 0.06),
      transparent 30%
    ),
    linear-gradient(
      180deg,
      rgba(var(--v-theme-surface), 0.8) 0%,
      rgba(var(--v-theme-surface), 0.42) 100%
    );
  position: relative;
  transition: background 0.3s ease;
}

.z-index-1 {
  position: relative;
  z-index: 1;
}

/* Icon Composition */
.icon-composition {
  position: relative;
  width: 240px;
  height: 240px;
  margin: 0 auto;
}

.main-icon-box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: main-float 6s ease-in-out infinite;
}

.main-icon {
  filter: drop-shadow(0 10px 20px rgba(var(--v-theme-primary), 0.3));
}

@keyframes main-float {
  0%,
  100% {
    transform: translate(-50%, -50%) translateY(0);
  }
  50% {
    transform: translate(-50%, -50%) translateY(-15px);
  }
}

@keyframes float-sub {
  0%,
  100% {
    transform: translateY(0) rotate(0);
  }
  50% {
    transform: translateY(-10px) rotate(5deg);
  }
}

/* Text Styling */
.gradient-text {
  background: linear-gradient(
    135deg,
    rgb(var(--v-theme-primary)) 0%,
    #34b7f1 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Glassmorphism */
.glass-card {
  background: rgba(var(--v-theme-surface), 0.72) !important;
  border: 1px solid rgba(var(--v-border-color), 0.1);
}

.security-footer {
  border: 1px solid rgba(var(--v-theme-success), 0.2);
  transition: all 0.3s ease;
}

.security-footer:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(var(--v-theme-success), 0.1);
  border-color: rgba(var(--v-theme-success), 0.4);
}

.gap-2 {
  gap: 8px;
}
</style>
