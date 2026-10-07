<template>
  <!-- added by alsodi -->
  <VCol cols="12" :lg="cols" :md="cols" class="py-2" v-if="!$state.print">
    <v-menu
      v-model="show_color_picker"
      :close-on-content-click="false"
      content-class="custom-color-picker-menu"
      z-index="99999"
    >
      <template v-slot:activator="{ props: menuProps }">
    <v-text-field
      ref="colorFieldRef"
      v-bind="menuProps"
      v-model="value"
      :clearable="clearable"
      :label="label + (isRequired ? '   *' : '')"
      density="compact"
      :placeholder="placeholder"
      :rules="rules"
      :type="type"
      :readonly="readonly"
      :disabled="disabled"
      :error-messages="error_messages"
      :rounded="rounded ? 'xl' : 's'"
      :variant="variant"
      class="no-autofill-bg my-0"
      aria-autocomplete="off"
      :autofocus="autofocus"
      :width="width"
      @append-outer-icon-click="append_click"
      @keydown="handleTab"
      :hide-details="hideDetails"
      @keydown.tab.prevent="keyTab"
      style="cursor: pointer"
    >
      <template v-slot:prepend-inner>
        <v-icon> {{"mdi-" + icon}}</v-icon>
      </template>
      <template v-slot:append-inner>
        <v-icon
          v-if="value"
          :color="value"
          size="x-large"
          style="opacity: 1"
        >
          <!-- @click="show_color_picker = true" -->
          mdi-square-rounded
        </v-icon>
      </template>
    </v-text-field>

    </template>
    <v-color-picker
      v-model="value"
      :show-swatches="false"
      :modes="['hexa']"
    />
    </v-menu>
  </VCol>
</template>
<script setup>
import { state } from "@/../src/store/state";
</script>
<script>
export default {
  props: {
    cols: {
      type: [String],
      default: "12",
    },
    append_click: Function,
    autofocus: Boolean,
    modelValue: {
      type: [Number, String],
      default: null,
    },
    rounded: {
      type: Boolean,
      default: false,
    },
    clearable: {
      type: Boolean,
      default: true,
    },
    label: {
      type: String,
      default: "",
    },
    placeholder: {
      type: String,
      default: "",
    },
    error_messages: {
      type: String,
      default: "",
    },
    readonly: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    icon: {
      type: String,
      default: "palette",
    },
    replace_icon: String,

    rules: {
      type: Array,
      default: () => [],
    },
    counter: {
      type: Number,
    },
    maxLength: {
      type: Number,
    },
    type: {
      type: String,
      default: "text",
    },
    width: String,
    hideDetails: {
      type: [String, Boolean],
      default: false,
    },
    variant: {
      type: String,
      default: "outlined",
    },
    keyTab: {
      type: Function,
      default: () => {},
    },
  },
  data() {
    return {
      isRequired: false,
      show_color_picker: false,
    };
  },
  watch: {
    show_color_picker(val){
      if (val) {
          setTimeout(()=>{
            window.addEventListener("click", this.handleOutsideClick, {capture: true});
          },50);
      } else {
        window.removeEventListener("click", this.handleOutsideClick, {capture: true});
      }
    }
  },
  beforeUnmount() {
    window.removeEventListener("click", this.handleOutsideClick, {capture: true});
  },
  created() {
    if (this.rules)
      this.rules?.forEach((e) => {
        if (typeof e === "function")
          if (e() == "حقل مطلوب" || e() === "Required Field")
            this.isRequired = true;
      });
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
  methods: {
    handleOutsideClick(event) {
      const fieldEl = this.$refs.colorFieldRef?.$el;
      const menuContent = event.target.closest('.custom-color-picker-menu');
      const clickedInsideField = fieldEl && fieldEl.contains(event.target);

      if (!clickedInsideField && !menuContent) {
        this.show_color_picker = false;
      }
    },
    keyTab(event) {
      this.keyTab(event);
    },
    updateDate(newValue) {
      this.$emit("update:modelValue", newValue);
    },
    handleTab(event) {
      if (event.key === "Enter" && event.shiftKey) {
        event.preventDefault();
      }

      if (event.key === "Tab") {
        event.preventDefault();
        const focusableElements = "input,button,select,a[href]";
        const elements = Array.from(
          document.querySelectorAll(focusableElements)
        ).filter((el) => !el.disabled && el.tabIndex >= 0);
        const index = elements.indexOf(event.target);

        if (index > -1 && index < elements.length - 1) {
          const nextElement = event.shiftKey
            ? elements[index - 1]
            : elements[index + 1];
          nextElement.focus();
        }
      }
    },
  },
};
</script>

<style scoped>
/* Style to prevent autofill background color changes */
.no-autofill-bg input:-webkit-autofill,
.no-autofill-bg input:-webkit-autofill:hover,
.no-autofill-bg input:-webkit-autofill:focus,
.no-autofill-bg input:-webkit-autofill:active {
  -webkit-text-fill-color: inherit !important;
  transition: background-color 5000s ease-in-out 0s !important;
  -webkit-box-shadow: 0 0 0 1000px transparent inset !important;
  box-shadow: 0 0 0 1000px transparent inset !important;
}
.v-messages__message {
  font-size: 10px;
}
</style>
