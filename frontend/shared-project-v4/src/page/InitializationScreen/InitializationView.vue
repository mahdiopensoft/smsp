<template>
  <!-- added by samer -->
  <!-- التهيئات -->

  <add-initialization
    v-model="drawer"
    :data="data"
    :getData="getData"
    :route="route"
    :items="items"
  />
  <custom-data-table
    :="{
      headers,
      items,
      getData,
      create: () => (drawer = true),
      delItem: url,
      editItem,
    }"
  />
</template>
<script>
import headers from "headers";
import AddInitialization from "./AddInitialization.vue";

export default {
  name: "../page/Organization/OrganizationScreen.vue",
  components: { AddInitialization },
  props: {
    url: String,
    route: String,
  },

  data() {
    return {
      data: {},
      items: {},

      drawer: false,
    };
  },
  methods: {
    async getData(params = this.$params) {
      const response = await this.$axios(this.url, params);

      this.items = response.data.data || response.data;
    },
    editItem(data) {
      this.data = { ...data };
      this.drawer = true;
    },
  },
  computed: {
    headers() {
      return headers[this.route] || [];
    },
  },
};
</script>