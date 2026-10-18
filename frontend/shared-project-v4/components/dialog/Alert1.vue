<template>
  <!-- added by samer -->
  <VDialog
    v-model="value"
    scrollable
    :overlay="false"
    max-width="350"
    elevation="12"
  >
    <VSheet rounded="lg" width="100%" class="pa-4 text-center mx-auto">
      <VIcon
        class="mb-5"
        :color="iconColor"
        :icon="`mdi-${icon}`"
        size="55"
      ></VIcon>

      <h2
        class="text-h5 mb-6"
        style="font-family: 'Almarai' !important; font-size: 2.5rem !important"
      >
        {{ title }}
      </h2>
      <p
        class="mb-4 text-medium-emphasis text-body-2"
        style="font-family: 'Almarai' !important; font-size: 14px !important"
        v-if="typeof message === 'string'"
      >
        {{ message }}
      </p>
      <template v-else-if="typeof message === 'object'">
        <v-list v-for="(value, key) in message" :key="key">
          {{ key }} : {{ value }}
        </v-list>
      </template>

      <div v-if="typeof sub_message === 'string'">
        <div
          v-html="sub_message"
          v-if="sub_message.startsWith('<!DOCTYPE html>')"
        ></div>
        <p
          v-else
          class="mb-4 text-medium-emphasis text-body-2"
          style="font-family: 'Almarai' !important; font-size: 14px !important"
        >
          {{ sub_message ?? "" }}
        </p>
      </div>
      <template v-else-if="typeof sub_message === 'object'">
        <v-list v-for="(value, key) in sub_message" :key="key">
          {{ key }} : {{ value }}
        </v-list>
      </template>
      <template v-else-if="Array.isArray(sub_message)">
        <v-list v-for="(value, key) in sub_message" :key="key">
          {{ key }} : {{ value }}
        </v-list>
      </template>

      <custom-btn
        type="ok"
        :click="
          () => {
            value = false;
          }
        "
        tabindex="1"
        autofocus
      />
    </VSheet>
  </VDialog>
</template>

<script>
export default {
  props: {
    modelValue: {
      type: Boolean,
      default: false,
    },
    iconColor: String,
    icon: String,
    title: String,
    message: String,
    sub_message: [String, Array, Object],
  },

  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
  },
};
</script>
