<template>
  <v-dialog v-model="value" max-width="400">
    <v-card rounded="lg" class="pa-2 pb-0">
      <v-card-title
        ><h4>
          <v-icon :color="color || config?.color" class="me-1">{{
            "mdi-" + (icon || config?.icon)
          }}</v-icon
          >{{ title || config?.title || $t("info") }}
        </h4></v-card-title
      >
      <v-divider></v-divider>
      <v-card-text class="pb-0">
        <h3>{{ text || config?.text || $t("save_data") }}</h3>
        <h5 class="ms-2" v-if="sub_text">
          {{ "- " + sub_text }}
        </h5></v-card-text
      >
      <v-card-actions class="justify-end">
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
      </v-card-actions>
    </v-card>
  </v-dialog>
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
