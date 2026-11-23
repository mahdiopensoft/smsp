<template>
  <custom-dialog
    v-model="value"
    :title="title || config?.title || $t('info')"
    width="420"
    height="auto"
  >
    <div class="d-flex align-start gap-3">
      <v-icon :color="color || config?.color" size="28" class="mt-1">{{
        "mdi-" + (icon || config?.icon)
      }}</v-icon>
      <div>
        <h3 class="text-body-1 font-weight-bold">{{ text || config?.text || $t("save_data") }}</h3>
        <h5 class="text-caption text-medium-emphasis mt-1" v-if="sub_text">
          {{ "- " + sub_text }}
        </h5>
      </div>
    </div>
    <template #actions>
      <v-btn @click="value = false" size="small" :autofocus="true">{{
        $t("cancel")
      }}</v-btn>
      <v-btn
        :color="color || config?.color"
        variant="tonal"
        :loading="loading"
        @click="handleSubmit()"
        >{{ $t(`${btn_text ?? "confirm"}`) }}</v-btn
      >
    </template>
  </custom-dialog>
</template>
<script>
export default {
  props: {
    title: String,
    text: String,
    sub_text: { type: String, default: "" },
    btn_text: { type: String, default: null },
    type: String,
    icon: { type: String, default: null },
    color: { type: String, default: "info" },
    loading: { type: Boolean, default: false },
  },
  data() {
    return {};
  },
  methods: {
    async handleSubmit() {
      this.$emit("success", true);
    },
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
    config() {
      switch (this.type) {
        case "warning":
          return {
            icon: "alert",
            color: "warning",
            title: this.$t("warning"),
            text: this.$t("default_warning_message"),
          };
        case "info":
          return {
            icon: "information-box",
            color: "info",
            title: this.$t("info"),
            text: this.$t("default_info_message"),
          };
        default:
          return {
            icon: "information-box",
          };
          break;
      }
    },
  },
};
</script>
