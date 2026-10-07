<template>
  <AddServiceCondition
    v-model="drawer"
    :items="items"
    :data="data"
    :getData="getData"
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
export default {
  data() {
    return {
      data: {},
      items: {},

      drawer: false,

      url: "d-services/conditions/",
    };
  },
  methods: {
    async getData(params = this.$params) {
      return await this.$axios(this.url, params).then(
        (response) => (this.items = response.data)
      );
    },
    editItem(data) {
      this.data = { ...data };
      this.drawer = true;
    },
  },
  computed: {
    headers() {
      return [
        {
          title:this.$t("code"),
          key:"code",
        },
        {
          title:this.$t("name_ar"),
          key:"name_ar",
        },
        {
          title:this.$t("name_en"),
          key:"name_en",
        },
        {
          title:this.$t("description"),
          key:"description",
        },

        {
          title:this.$t("is_active"),
          key:"is_active",
        },
        {
          title:this.$t("order"),
          key:"order",
        },
      ];
    },
  },
};
</script>
