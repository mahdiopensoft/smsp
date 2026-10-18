<template>
  <!-- Expansion Mode -->
  <v-expansion-panels v-if="expanstion" model-value="2" class="custom-card-expansion">
    <v-expansion-panel value="1" class="border-thin">
      <template v-slot:title>
        <div class="d-flex flex-column w-100">
          <div v-if="head_title" class="d-flex align-center justify-space-between mb-1">
            <span class="text-subtitle-2 font-weight-semibold text-primary">{{
              head_title
            }}</span>
            <span v-if="head_date" class="text-caption text-disabled">{{
              head_date
            }}</span>
          </div>
          <span class="text-h6 font-weight-bold">{{ title }}</span>
        </div>
      </template>
      <v-expansion-panel-text class="pt-4">
        <slot></slot>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>

  <!-- Standard Card Mode -->
  <v-card
    v-else
    :color="cardcolor"
    :class="['custom-card', cardstyle]"
    :loading="loading"
    elevation="0"
    class="border-thin"
  >
    <!-- Card Header -->
    <v-card-item v-if="head_title" class="custom-card-header pb-2">
      <div class="d-flex align-center justify-space-between w-100">
        <div>
          <v-card-title class="text-h6 font-weight-bold color-heading">
            {{ head_title }}
          </v-card-title>
        </div>
        <div v-if="head_date" class="text-subtitle-2 text-disabled font-weight-medium">
          {{ head_date }}
        </div>
      </div>
    </v-card-item>

    <v-divider v-if="head_title" class="mx-4"></v-divider>

    <!-- Card Content -->
    <v-card-text :class="['custom-card-content', { 'pt-5': !head_title }]">
      <slot></slot>
    </v-card-text>

    <!-- Card Actions -->
    <v-divider v-if="$slots.actions" class="mx-4"></v-divider>
    <v-card-actions v-if="$slots.actions" class="pa-4">
      <v-spacer></v-spacer>
      <slot name="actions"></slot>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "CustomCard",
  data() {
    return {};
  },
  props: {
    head_title: {
      type: String,
    },
    head_date: {
      type: String,
    },
    expanstion: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
    },
    cardstyle: {
      type: String,
      default: "",
    },
    loading: false,
  },
};
</script>
<style scoped>
.custom-card {
  border-radius: 8px !important;
  transition: all 0.3s ease;
}

.custom-card.border-thin {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity)) !important;
}

.custom-card-header {
  padding: 1.25rem 1.5rem !important;
}

.custom-card-content {
  font-size: 0.9375rem;
  line-height: 1.5;
}

.color-heading {
  color: rgba(var(--v-theme-on-surface), 0.87) !important;
}

/* Expansion Overrides */
.custom-card-expansion :deep(.v-expansion-panel) {
  border-radius: 8px !important;
  overflow: hidden;
}

.custom-card-expansion :deep(.v-expansion-panel-title) {
  padding: 1.25rem 1.5rem !important;
  min-height: 64px;
}

.custom-card-expansion :deep(.v-expansion-panel-text__wrapper) {
  padding: 0 1.5rem 1.5rem 1.5rem !important;
}
</style>
