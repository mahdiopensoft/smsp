<template>
  <custom-data-table
    :="{
      items,
      getData,
      headers,
    }"
  />

</template>
<script>

export default {
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      url: "sync/logs/",
    };
  },
  computed: {
    headers() {
      return [
        {
          title: this.$t("system_id"),
          key: "system_id",
        },
        {
          title: this.$t("direction"),
          key: "direction",
        },
        {
          title: this.$t("operation"),
          key: "operation",
        },
        {
          title: this.$t("subject"),
          key: "subject",
        },
        {
          title: this.$t("started_at"),
          key: "started_at",
          show: false,
        },
        {
          title: this.$t("completed_at"),
          key: "completed_at",
          show: false,
        },
        {
          title: this.$t("duration_ms"),
          key: "duration_ms",
          show: false,
        },
        {
          title: this.$t("status"),
          key: "status",
          show: false,
        },
        {
          title: this.$t("records_total"),
          key: "records_total",
        },
        {
          title: this.$t("records_created"),
          key: "records_created",
        },
        {
          title: this.$t("records_updated"),
          key: "records_updated",
        },
        {
          title: this.$t("records_failed"),
          key: "records_failed",
        },
        {
          title: this.$t("error_message"),
          key: "error_message",
        },
        {
          title: this.$t("error_traceback"),
          key: "error_traceback",
        },
        {
          title: this.$t("request_summary"),
          key: "request_summary",
        },
        {
          title: this.$t("response_summary"),
          key: "response_summary",
        },
        {
          title: this.$t("metadata"),
          key: "metadata",
        },
        {
          title: this.$t("auth_method"),
          key: "auth_method",
        },
        {
          title: this.$t("request_timestamp"),
          key: "request_timestamp",
        },
      ];
    },
  },
  methods: {
    async getData(params) {
      return await this.$axios(this.url, params).then(
        (response) => (this.items = response.data)
      );
    },
  },
};
</script>
