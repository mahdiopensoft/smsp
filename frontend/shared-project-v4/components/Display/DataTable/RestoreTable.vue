<template>
  <custom-data-table
    :="{
      headers,
      items,
      getData: getLog,
      restore: false,
      is_restore_screen: true,
      actionList: false,
      showSelect: false,
      log: false,
      search: false,
      delItem: url,
      getDataAfterRestore: getDataAfterRestore,
      hasFilter: false,
    }"
  />
</template>
<script>
export default {
  props: {
    headers: Array,
    url: [Function, Boolean, String],
    getDataAfterRestore: Function,
  },
  data() {
    return {
      items: {},
    };
  },
  methods: {
    async getLog(params = this.$params) {
      if (typeof this.url == "string") {
        const response = await this.$axios(this.url + "disactive/", params);
        this.items.results = response.data?.data || response.data;
      }
    },
  },
};
</script>
