<template>
  <transition name="slide-fade" mode="out-in">
    <v-btn
      class="post-btn"
      :class="{ posted: is_finish }"
      :disabled="is_finish"
      :color="is_finish ? finish_color : btn_color"
      :loading="loading"
      variant="tonal"
      density="compact"
      @click="confirmPost()"
      key="btn"
    >
      <v-icon
        v-if="!is_finish"
        icon="mdi-email-fast mdi-flip-h"
        class="icon-slide"
        :class="{ 'animate-out': animate }"
        key="icon"
      >
      </v-icon>
      <span v-if="is_finish" class="label-slide">
        {{ finish_text || $t("posted") }}</span
      >
    </v-btn>
  </transition>

  <confirm-alert
    v-if="confirm"
    v-model="con_dialog"
    :title="title ?? $t('con_post')"
    :text="text ?? $t('post_text')"
    :sub_text="sub_text ?? $t('no_undo_text')"
    :color="color"
    :type="type"
    :loading="loading"
    @success="handleSubmit()"
  ></confirm-alert>
  <!-- <v-dialog v-if="confirm" v-model="con_dialog" max-width="400">
    <v-card rounded="lg">
      <v-card-title>{{ title ?? $t("con_post") }}</v-card-title>
      <v-card-text
        >{{ text ?? $t("post_text") }} <br />
        <strong>{{ sub_text ?? $t("no_undo_text") }}</strong></v-card-text
      >
      <v-card-actions class="justify-end">
        <v-btn @click="con_dialog = false">{{ $t("cancel") }}</v-btn>
        <v-btn color="primary" @click="handleSubmit()">{{
          $t("confirm")
        }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog> -->
</template>
<script>
export default {
  props: {
    animate: { type: Boolean, default: false },
    is_finish: { type: Boolean, default: {} },
    loading: { type: Boolean, default: false },
    confirm: { type: Boolean, default: true },
    item: { type: Object, default: {} },
    axios_url: { type: String, default: "" },
    color: { type: String, default: "" },
    btn_color: { type: String, default: "primary" },
    finish_color: { type: String, default: "success" },
    sub_text: { type: String, default: null },
    icon: { type: String, default: "" },
    title: String,
    text: String,
    finish_text: String,
    param: { type: [Object, Boolean], default: false },
    is_put: { type: [Object, Boolean], default: false },

    type: String,
  },
  data() {
    return {
      loading: false,
      con_dialog: false,
    };
  },
  methods: {
    confirmPost() {
      if (this.confirm) {
        this.selected_line = this.item;
        this.con_dialog = true;
      } else {
        this.$emit("click");
      }
    },
    async handleSubmit() {
      if (this.axios_url && this.item) {
        this.loading = true;
        await this.$axios[this.is_put ? "put" : "post"](
          this.axios_url,
          this.param || { move: this.item?.id }
        )
          .then((response) => {
            this.con_dialog = false;
            this.$emit("success", true);
            this.loading = false;
            this.item.state = 2;
            // this.$snack("add");
          })
          .catch(() => {
            this.loading = false;
          });
      }
    },
  },
};
</script>
<style scoped>
.post-btn {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  min-width: 48px !important;
  overflow: hidden !important;
  transition: background-color 0.3s ease !important;
  gap: 6px !important;
  padding-inline: 6px !important;
}
.icon-slide {
  transition: transform 0.4s, opacity 0.4s !important;
}
.icon-slide.animate-out {
  transform: translateX(-50px) !important;
  opacity: 0 !important;
}
.label-slide {
  transform: slideIn 0.4s forwards !important;
  white-space: nowrap !important;
  padding-inline: 4px;
}
@keyframes slideIn {
  from {
    transform: translateX(30px) !important;
    opacity: 0 !important;
  }
  to {
    transform: translateX(0) !important;
    opacity: 1 !important;
  }
}
</style>
