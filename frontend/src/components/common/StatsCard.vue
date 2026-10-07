<template>
  <v-card class="stats-card glass-card hover-lift" :class="{ 'glow-effect': glow }">
    <div class="d-flex align-center pa-4">
      <!-- Icon -->
      <v-avatar
        :color="color"
        size="56"
        class="icon-container me-4"
        variant="tonal"
      >
        <v-icon :icon="icon" size="28" />
      </v-avatar>

      <!-- Content -->
      <div class="flex-grow-1">
        <div class="text-caption text-medium-emphasis mb-1">{{ title }}</div>
        <div class="d-flex align-center">
          <span class="text-h4 font-weight-bold">{{ animatedValue }}</span>
          <v-chip
            v-if="trend !== undefined"
            size="x-small"
            :color="trend >= 0 ? 'success' : 'error'"
            variant="tonal"
            class="ms-2"
          >
            <v-icon start size="12">{{ trend >= 0 ? 'mdi-trending-up' : 'mdi-trending-down' }}</v-icon>
            {{ Math.abs(trend) }}%
          </v-chip>
        </div>
        <div v-if="trendText" class="text-caption text-medium-emphasis mt-1">
          {{ trendText }}
        </div>
      </div>
    </div>

    <!-- Progress Bar (optional) -->
    <v-progress-linear
      v-if="progress !== undefined"
      :model-value="progress"
      :color="color"
      height="4"
      class="rounded-b-xl"
    />
  </v-card>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  title: { type: String, required: true },
  value: { type: Number, required: true },
  icon: { type: String, required: true },
  color: { type: String, default: 'primary' },
  trend: { type: Number, default: undefined },
  trendText: { type: String, default: '' },
  progress: { type: Number, default: undefined },
  glow: { type: Boolean, default: false },
})

// Animated counter
const animatedValue = ref(0)

onMounted(() => {
  const duration = 1000
  const steps = 60
  const increment = props.value / steps
  let current = 0
  
  const timer = setInterval(() => {
    current += increment
    if (current >= props.value) {
      animatedValue.value = props.value
      clearInterval(timer)
    } else {
      animatedValue.value = Math.floor(current)
    }
  }, duration / steps)
})

watch(() => props.value, (newValue) => {
  animatedValue.value = newValue
})
</script>

<style scoped>
.stats-card {
  transition: all 0.3s ease;
}



.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
}

.glow-effect {
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
}

.icon-container {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.1) 0%, rgba(var(--v-theme-secondary), 0.1) 100%);
}
</style>
