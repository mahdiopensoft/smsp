<template>
  <custom-data-table
    v-model="selected_session"
    :="{
      headers,
      items,
      getData,
      actions: false,
    }"
  >
    <template v-slot:action>
      <VBtn
        :text="
          selected_session.length > 0
            ? $t('end_selected_sessions')
            : $t('end_all_sessions')
        "
        @click="(session_id = undefined), (session_index = undefined), (dialog = true)"
      >
        <template v-slot:append>
          <VIcon icon="mdi-close" color="red" />
        </template>
      </VBtn>
    </template>
    <template v-slot:item-slot="{ item, key, index }">
      <span v-if="key === 'close' && item.is_active">
        <custom-btn
          icon="close"
          is-icon
          color="red"
          @click="(session_id = item.id), (session_index = index), (dialog = true)"
        />
      </span>
    </template>
  </custom-data-table>

  <confirm-dialog
    v-model="dialog"
    :title="$t('confirm_exit')"
    icon="information"
    color="primary"
    :message="$t('are_you_sure') + $t('close_session') + ' ?'"
    :confirmBtn="handleClick"
  />
</template>
<script>
export default {
  data() {
    return {
      items: {},
      selected_session: [],

      session_id: undefined,
      session_index: undefined,

      dialog: false,

      url: "user-manager/sessions/",
    };
  },

  methods: {
    async handleClick() {
      if (this.session_id) await this.closeSession();
      else await this.closeAllSession();
    },
    async getData(params = this.$params) {
      return await this.$axios(this.url, params).then(
        (response) => (this.items = response.data)
      );
    },
    async closeSession() {
      await this.$axios.post(`${this.url}${this.session_id}/end-session/`).then(() => {
        this.items.results[this.session_index].is_active = false;

        this.session_id = undefined;
        this.session_index = undefined;

        this.$alert("add", {
          message: "✅ تم إنهاء الجلسة بنجاح.",
        });
      });
    },
    async closeAllSession() {
      // const data =this.selected_session.length ?  this.selected_session:  this.items.results.map((e) => e.id);
      await this.$axios.post(`${this.url}end-all-sessions/`).then(() => {
        this.getData();
        this.$alert("add", {
          message: this.$t("session_ended_successfully"),
        });
      });
    },
  },
  computed: {
    headers() {
      return [
        { title: this.$t("user"), key: "username" },
        { title: this.$t("created_at"), key: "created_at" },
        { title: "ip_address", key: "ip_address" },
        { title: this.$t("is_active"), key: "is_active" },
        { title: this.$t("os"), key: "os" },
        { title: this.$t("devicename"), key: "device" },
        { title: this.$t("close"), key: "close", sortable: false },
      ];
    },
  },
  watch: {
    dialog(val) {
      if (!val) this.session = undefined;
    },
  },
};
</script>
