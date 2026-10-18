<template>
  <v-btn
    :text="label"
    variant="tonal"
    color="primary"
    density="comfortable"
    prepend-icon="mdi-arrow-right"
    class="back-to-btn"
    v-esc="{ active: isActive, handler: click }"
  >
    <!-- @click="click" -->
    <template #append>
      <dev v-if="escBtn" class="text-caption">Esc</dev>
    </template>
  </v-btn>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: "تراجع",
    },
    isActive: {
      type: Boolean,
      default: true,
    },
    escBtn: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    click() {
      this.$emit("click");
    },
  },
};
</script>

<style scoped>
.back-to-btn {
  border-radius: var(--radius-lg) !important;
  font-weight: 600;
  font-size: 0.875rem;
  letter-spacing: 0.01em;
  transition: opacity 0.2s ease;
}
.back-to-btn:hover {
  opacity: 0.85;
}
</style>
