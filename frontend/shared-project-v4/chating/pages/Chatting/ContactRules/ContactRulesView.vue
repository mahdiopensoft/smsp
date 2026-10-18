<template>
  <add-contact-rules v-model="drawer" :data="data" :getData="getData" />
  <custom-data-table :="{
    items,
    getData,
    headers,
    delItem: url,
    editItem,
    create: () => (drawer = true),
  }" />
</template>
<script>
import AddContactRules from './AddContactRules.vue'
export default {
  components: {
    AddContactRules,
  },
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      url: "chat/contacts/rules/",
    };
  },

  methods: {
    async getData(params = this.$params) {
      return await this.$axios
        .get(this.url, params)
        .then((response) => (this.items = response.data));
    },
    editItem(data) {
      this.data = { ...data };
      this.drawer = true;
    },
  },

  computed: {
    headers() {
      return [{ title: this.$t("contact_rules.rule_name"), key: "rule_name" },
      {
        title: this.$t("contact_rules.company_level"),
        key: "company_level_name",
      },
      {
        title: this.$t("contact_rules.fk_user_type"),
        key: "user_type_name",
      },
      { title: this.$t("contact_rules.description"), key: "description" },
      { title: this.$t("contact_rules.priority"), key: "priority" },
      { title: this.$t("contact_rules.query_config"), key: "query_config" },
      { title: this.$t("contact_rules.is_active"), key: "is_active" },]
    },
  },
};
</script>
