<template>
  <add-directorate
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
      delItem: isPlatFormSys?url:false,
      editItem:isPlatFormSys?editItem:false,
      actionList,
      create: isPlatFormSys?() => (drawer = true):false,
    }"
  />
</template>
<script>
import AddDirectorate from "./AddDirectorate.vue";
import { state } from "@/../src/store/state";

export default {
  components: { AddDirectorate },
  data() {
    return {
      data: {},
      items: {},

      drawer: false,

      url: "common/directorate/",
    };
  },
  methods: {
    actionList(item) {
      return { fk_directorate: item.id, ar: item.name_ar, en: item.name_en };
    },
    async getData(params = this.$params) {
      const filters = this.$filters(this, "fk_governorate", "fk_governorate");
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
      return [
        { title: this.$t("name_ar"), key: "name_ar" },
        { title: this.$t("name_en"), key: "name_en" },
        { title: this.$t("code"), key: "code" },
      ];
    },
    isPlatFormSys() {
      return state?.isPlatFormSys || false;
    },
  },
  watch: {
    drawer(val) {
      if (val) this.data.fk_governorate = this.$route.params.fk_governorate;
    },
  },
};
</script>
