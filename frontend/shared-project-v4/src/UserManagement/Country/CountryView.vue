<template>
  <!-- <add-country v-model="drawer" :data="data" :getData="getData" /> -->

  <custom-data-table :="{ headers, items, getData, actionList, hasFilter: false }" />
</template>

<script>
import AddCountry from "./AddCountry.vue";

export default {
  components: { AddCountry },
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      url: "common/country/",
      date: undefined,
    };
  },

  methods: {
    actionList(item) {
      return { fk_country: item.id, ar: item.name_ar, en: item.name_en };
    },
    async getData(params = this.$params) {
      return await this.$axios(this.url, params).then(
        (response) => (this.items = response.data?.data || response.data)
      );
    },
  },
  computed: {
    headers() {
      return [
        { title: this.$t("name_ar"), key: "name_ar" },
        { title: this.$t("name_en"), key: "name_en" },
        { title: this.$t("nationalty_ar"), key: "nationality_name_ar" },
        { title: this.$t("nationalty_en"), key: "nationality_name_en" },
        { title: this.$t("code"), key: "code" },
      ];
    },
  },
};
</script>
