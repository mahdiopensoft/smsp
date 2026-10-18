<template>
  <div class="app-date-picker" :class="{ 'is-range': range }">
    <v-menu
      v-model="menu"
      :close-on-content-click="false"
      location="bottom start"
      transition="scale-transition"
    >
      <template #activator="{ props }">
        <div
          class="antd-input-wrapper"
          :class="{ 'is-active': menu }"
          v-bind="props"
        >
          <v-icon class="calendar-icon" size="18">mdi-calendar-outline</v-icon>

          <template v-if="range">
            <span class="date-text">{{ formattedStartDate || $t('common.startDate') }}</span>
            <v-icon class="mx-2" size="14">mdi-arrow-right-thin</v-icon>
            <span class="date-text">{{ formattedEndDate || $t('common.endDate') }}</span>
          </template>
          <template v-else>
            <span class="date-text">{{ formattedDate || placeholder || $t('common.selectDate') }}</span>
          </template>

          <v-spacer />
          <v-icon v-if="modelValue" class="clear-icon" size="16" @click.stop="clear">mdi-close-circle</v-icon>
        </div>
      </template>

      <v-card class="antd-picker-panel rounded-lg" elevation="12">
        <v-date-picker
          v-model="internalValue"
          color="primary"
          :hide-header="true"
          :multiple="range ? 2 : false"
          @update:model-value="onDateSelect"
        >
          <!-- Custom render for days if needed (Vuetify 3 limitation: custom day slots are limited, using CSS) -->
        </v-date-picker>

        <div v-if="range" class="range-actions pa-2 border-t d-flex justify-end">
          <v-btn color="primary" size="small" variant="text" @click="menu = false">{{ $t("common.confirmRange") }}</v-btn>
        </div>
      </v-card>
    </v-menu>
  </div>
</template>

<script setup>
  import { computed, ref, watch } from 'vue'
  import { useI18n } from 'vue-i18n'

  const { locale } = useI18n()

  const props = defineProps({
    modelValue: { type: [String, Array, Date], default: null },
    range: { type: Boolean, default: false },
    placeholder: { type: String, default: '' },
  })

  const emit = defineEmits(['update:modelValue'])

  const menu = ref(false)
  const internalValue = ref(props.range ? [] : (props.modelValue ? new Date(props.modelValue) : null))

  // Sync with prop
  watch(() => props.modelValue, newVal => {
    if (props.range) {
      if (Array.isArray(newVal)) internalValue.value = newVal.map(d => new Date(d))
    } else {
      internalValue.value = newVal ? new Date(newVal) : null
    }
  }, { immediate: true })

  const formattedDate = computed(() => {
    if (!internalValue.value || props.range) return ''
    return new Date(internalValue.value).toLocaleDateString(locale.value === 'ar' ? 'ar-SA' : 'en-US')
  })

  const formattedStartDate = computed(() => {
    if (!props.range || !Array.isArray(internalValue.value) || !internalValue.value[0]) return ''
    return new Date(internalValue.value[0]).toLocaleDateString(locale.value === 'ar' ? 'ar-SA' : 'en-US')
  })

  const formattedEndDate = computed(() => {
    if (!props.range || !Array.isArray(internalValue.value) || !internalValue.value[1]) return ''
    return new Date(internalValue.value[1]).toLocaleDateString(locale.value === 'ar' ? 'ar-SA' : 'en-US')
  })

  function onDateSelect (val) {
    if (props.range) {
      // Logic for range selection in Vuetify
      if (Array.isArray(val) && val.length === 2) {
        const sorted = [...val].sort((a, b) => a - b)
        emit('update:modelValue', sorted.map(d => d.toISOString().split('T')[0]))
      }
    } else {
      emit('update:modelValue', val ? val.toISOString().split('T')[0] : null)
      menu.value = false
    }
  }

  function clear () {
    internalValue.value = props.range ? [] : null
    emit('update:modelValue', props.range ? [] : null)
  }
</script>

<style lang="scss">
.app-date-picker {
  width: 100%;

  .antd-input-wrapper {
    display: flex;
    align-items: center;
    height: 40px;
    padding: 0 12px;
    background: var(--wa-bg);
    border: 1px solid var(--wa-divider);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);

    &:hover {
      border-color: var(--wa-primary);
    }

    &.is-active {
      border-color: var(--wa-primary);
      box-shadow: 0 0 0 2px rgba(0, 168, 132, 0.1);
    }

    .calendar-icon {
      color: var(--wa-text-secondary);
      margin-inline-end: 8px;
    }

    .date-text {
      font-size: 0.9rem;
      color: var(--wa-text-primary);
    }

    .clear-icon {
      opacity: 0;
      color: var(--wa-text-secondary);
      transition: opacity 0.2s;
    }

    &:hover .clear-icon {
      opacity: 1;
    }
  }

  &.is-range .antd-input-wrapper {
    min-width: 280px;
  }
}

// Global overrides for Vuetify DatePicker to look like Ant Design
.v-overlay.antd-picker-panel {
  .v-date-picker {
    width: 280px !important;
    background: white !important;

    .v-date-picker-month {
      padding: 8px !important;
    }

    .v-date-picker-header {
      padding: 8px 12px !important;
      border-bottom: 1px solid #f0f0f0;

      .v-date-picker-header__content {
        font-weight: 600;
        font-size: 0.95rem;
      }
    }

    // Ant Design Style Circles
    .v-btn--active.v-date-picker-month__day {
      background: var(--wa-primary) !important;
      color: white !important;
      border-radius: 50% !important;

      &::after {
        display: none !important;
      }
    }

    .v-date-picker-month__day {
      width: 32px !important;
      height: 32px !important;
      font-size: 0.85rem !important;

      &:hover:not(.v-btn--active) {
        background: #f5f5f5 !important;
        border-radius: 50% !important;
      }

      // The "1st of month" circle styling from user snippet
      &[data-day="1"] {
        // We can't easily target "1st day" with pure CSS in Vuetify's rendered grid without JS,
        // but we can style the active state and hover states to be circular.
      }
    }

    .v-date-picker-controls {
      .v-btn {
        width: 24px;
        height: 24px;
      }
    }
  }
}
</style>
