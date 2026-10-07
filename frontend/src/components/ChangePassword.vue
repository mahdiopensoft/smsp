<template>
  <custom-text-field
    v-model="value.new_password"
    icon="lock"
    :type="`${show_new_pass ? 'text' : 'password'}`"
    :rules="[$required, $min_value(8)]"
    :label="$t('new_pass')"
  >
    <template v-slot:append-inner>
      <VIcon
        :icon="`${show_new_pass ? 'mdi-eye-off' : 'mdi-eye'}`"
        @click="show_new_pass = !show_new_pass"
      />
    </template>
  </custom-text-field>
  <custom-text-field
    v-model="value.confirm_pass"
    icon="lock"
    :type="`${show_confirm_pass ? 'text' : 'password'}`"
    :rules="[$required, $min_value(8), confrim_pass(value.new_password)]"
    :label="$t('confirm_password')"
  >
    <template v-slot:append-inner>
      <VIcon
        :icon="`${show_confirm_pass ? 'mdi-eye-off' : 'mdi-eye'}`"
        @click="show_confirm_pass = !show_confirm_pass"
      />
    </template>
  </custom-text-field>
</template>
<script>
export default {
  props: {
    modelValue: {
      type: [Number, String, Array],
      default: null,
    },
  },
  data() {
    return {
      show_new_pass: false,
      show_confirm_pass: false,
    };
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