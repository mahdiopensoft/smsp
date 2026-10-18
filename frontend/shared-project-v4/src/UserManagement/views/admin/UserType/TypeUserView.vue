<template>
  <!--  نوع المستخدمين-->
  <!-- added by samer -->

  <add-type-user v-model="drawer" :data="data" :getData="getData" :items="items" />

  <!-- <custom-data-table2 :headers="headers" :items="items" /> -->
  <custom-data-table
    :="{
      headers,
      items,
      getData: getData,
      create: () => (drawer = true),
      delItem: url,
      editItem: editItem,
    }"
  />
</template>
<script>
import AddTypeUser from "./AddUserType.vue";
import { useAuthStore } from "../../../stores/auth";
import { state } from "@/../src/store/state";

export default {
  components: { AddTypeUser },
  data() {
    return {
      authStore: useAuthStore(),
      data: {},
      items: {},
      drawer: false,
      url: "user-manager/user-type/",
    };
  },
  methods: {
    async getData(params = this.$params) {
      return await this.$axios
        .get(this.url, { ...params })
        .then((response) => (this.items = response.data));
    },
    editItem(data) {
      this.data = { ...data };
      this.data.screens = data.screens.map((e) => e.id);
      this.drawer = true;
    },
  },
  computed: {
    headers() {
      return [
        { title: this.$t("parent"), key: "fk_parent_user_type__name_ar" },
        { title: this.$t("name_ar"), key: "name_ar" },
        { title: this.$t("name_en"), key: "name_en" },
        { title: this.$t("description"), key: "description" },
      ];
    },
    isPlatFormSys() {
      return state?.isPlatFormSys;
    },
  },
};
</script>
