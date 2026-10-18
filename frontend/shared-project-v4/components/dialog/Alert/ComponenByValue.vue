<template>
  <div class="componen-by-value-wrapper">
    <template v-if="value">
      <!-- String Value -->
      <div
        v-if="typeof value === 'string'"
        class="value-string text-body-2 py-1 font-weight-medium"
      >
        {{ value }}
      </div>

      <!-- Array Value -->
      <div
        v-else-if="Array.isArray(value)"
        class="value-array d-flex flex-column gap-1 py-1"
      >
        <div
          v-for="(msg, index) in value"
          :key="index"
          class="array-item-block pa-2 px-3 border-thin rounded-sm d-flex align-center gap-3 mb-1"
        >
          <div class="d-flex align-center" style="height: 20px">
            <v-icon icon="mdi-square" class="accent-color opacity-60" size="8" />
          </div>
          <div class="flex-grow-1">
            <componen-by-value :value="msg" :first="false" />
          </div>
        </div>
      </div>

      <!-- Object Value (Top Level - Block Flat Accordion) -->
      <div v-else-if="typeof value === 'object' && first" class="value-object-first mt-2">
        <v-expansion-panels
          multiple
          variant="accordion"
          class="block-flat-expansion"
          elevation="0"
        >
          <template v-for="(val, key) in value" :key="key">
            <v-expansion-panel
              v-if="!excludeKey.includes(key)"
              elevation="0"
              :class="[
                'flat-panel mb-2 border-thin rounded-sm overflow-hidden',
                'key-context-' + key || '',
              ]"
            >
              <v-expansion-panel-title
                class="block-header py-3 px-4"
                style="background-color: rgba(var(--v-theme-on-surface), 0.02)"
              >
                <template v-slot:default="{ expanded }">
                  <div class="d-flex align-center w-100">
                    <v-icon
                      :icon="expanded ? 'mdi-minus-box' : 'mdi-plus-box'"
                      size="small"
                      class="me-3 accent-color"
                    />
                    <span
                      class="text-subtitle-2 font-weight-bold text-uppercase letter-spacing-1 accent-color-text"
                    >
                      {{ $t(key) }}
                    </span>
                  </div>
                </template>
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                <div class="pa-4 bg-surface border-t-thin">
                  <componen-by-value :value="val" :first="false" />
                </div>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </template>
        </v-expansion-panels>
      </div>

      <!-- Object Value (Nested Block Layout) -->
      <div v-else-if="typeof value === 'object' && !first" class="value-object-nested">
        <div class="block-grid d-flex flex-column">
          <div
            v-for="(val, key) in value"
            :key="key"
            :class="[
              'block-row d-flex py-3 px-3 border-b-thin align-center',
              'key-context-' + key.toLowerCase(),
            ]"
          >
            <div
              class="block-key text-caption font-weight-bold text-uppercase me-4 accent-color-dim"
              style="min-width: 100px; width: 100px; flex-shrink: 0"
            >
              {{ key }}
            </div>
            <div class="flex-grow-1 block-value d-flex align-center">
              <componen-by-value :value="val" :first="false" />
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Empty State -->
    <div
      v-else
      class="empty-state-block text-center py-6 border-thin rounded-sm"
      style="background-color: rgba(var(--v-theme-on-surface), 0.02)"
    >
      <div class="text-caption text-disabled font-weight-bold">NO ADDITIONAL DATA</div>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    value: null,
    first: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      excludeKey: ["success", "code"],
    };
  },
  methods: {
    formatValue(val) {
      if (typeof val === "object") return JSON.stringify(val, null, 2);
      return val;
    },
  },
};
</script>
<style scoped>
.componen-by-value-wrapper {
  --accent-color: rgb(var(--v-theme-error));
  color: rgb(var(--v-theme-on-surface));
}

/* Color Mapping Logic */
:global(.success) .componen-by-value-wrapper {
  --accent-color: rgb(var(--v-theme-success));
}
:global(.error) .componen-by-value-wrapper {
  --accent-color: rgb(var(--v-theme-error));
}
:global(.warning) .componen-by-value-wrapper {
  --accent-color: rgb(var(--v-theme-warning));
}
:global(.info) .componen-by-value-wrapper {
  --accent-color: rgb(var(--v-theme-info));
}

/* Semantic Keys */
.key-context-errors {
  --accent-color: rgb(var(--v-theme-error)) !important;
}
.key-context-error {
  --accent-color: rgb(var(--v-theme-error)) !important;
}
.key-context-status {
  --accent-color: rgb(var(--v-theme-info)) !important;
}
.key-context-details {
  --accent-color: rgb(var(--v-theme-warning)) !important;
}
.key-context-message {
  --accent-color: rgb(var(--v-theme-success)) !important;
}

.accent-color {
  color: var(--accent-color) !important;
}
.accent-color-text {
  color: var(--accent-color) !important;
}
.accent-color-dim {
  color: var(--accent-color) !important;
  opacity: 0.7;
}

/* Block Flat Styling */
.block-flat-expansion :deep(.v-expansion-panel) {
  background-color: transparent !important;
  box-shadow: none !important;
}

.block-header {
  border-inline-start: 4px solid var(--accent-color) !important;
}

.block-row {
  border-inline-start: 2px solid color-mix(in srgb, var(--accent-color), transparent 85%) !important;
}

.border-thin {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity)) !important;
}

.border-b-thin {
  border-bottom: 1px solid rgba(var(--v-border-color), 0.05) !important;
}

.border-t-thin {
  border-top: 1px solid rgba(var(--v-border-color), 0.05) !important;
}

.array-item-block {
  background-color: rgba(var(--v-theme-on-surface), 0.01);
}

.letter-spacing-1 {
  letter-spacing: 1px;
}

/* Recursion adjustments */
.value-object-nested .componen-by-value-wrapper .value-string {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
  font-size: 0.9rem !important;
  line-height: 1.2 !important;
}

.block-key {
  font-size: 0.7rem !important;
  line-height: 1.2 !important;
}

.block-value {
  color: rgba(var(--v-theme-on-surface), 0.9);
}
</style>
