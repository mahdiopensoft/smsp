<template>
  <div class="checked-wrapper">
    <v-icon
      v-if="val === true"
      color="success"
      class="checked-icon checked-icon--success"
    >
      mdi-check-circle
    </v-icon>
    <v-icon
      v-if="val === false"
      color="error"
      class="checked-icon checked-icon--error"
    >
      mdi-close-circle
    </v-icon>
  </div>
</template>

<script>
export default {
  props: {
    val: Boolean
  }
}
</script>

<style scoped>
.checked-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.checked-icon {
  font-size: 1.5rem;
  transition: transform 0.2s ease;
}

.checked-icon--success {
  filter: drop-shadow(0 2px 4px rgba(var(--v-theme-success), 0.2));
}

.checked-icon--error {
  filter: drop-shadow(0 2px 4px rgba(var(--v-theme-error), 0.2));
}
</style>