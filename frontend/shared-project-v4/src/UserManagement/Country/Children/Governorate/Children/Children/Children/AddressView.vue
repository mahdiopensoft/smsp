<template>
  <add-address
    v-model="drawer"
    :data="data"
    :getData="getData"
    :items="items"
  />
  <custom-data-table
    :="{
      headers,
      items,
      getData,
      create:  () => (drawer = true),
      delItem: url,
      editItem,
    }"
  />
</template>
<script>
import AddAddress from "./AddAddress.vue";
import { state } from "@/../src/store/state";

export default {
  components: { AddAddress },
  data() {
    return {
      data: {},
      items: {},

      drawer: false,

      url: "common/address/",
    };
  },
  methods: {
    async getData(params = this.$params) {
      const filters = this.$filters(this, "fk_region", "fk_region");
      return await this.$axios
        .post(this.url + "filter-paginate/", { filters }, params)
        .then((response) => (this.items = response.data));
    },
    editItem(data) {
      this.data = { ...data };
      this.drawer = true;
    },
  },
  computed: {
    headers() {
      return [{ title: this.$t("street"), key: "street" }];
    },
    isPlatFormSys() {
      return state?.isPlatFormSys || false;
    },
  },
  watch: {
    drawer(val) {
      if (val) this.data.fk_region = this.$route.params.fk_region;
    },
  },
};
</script>
