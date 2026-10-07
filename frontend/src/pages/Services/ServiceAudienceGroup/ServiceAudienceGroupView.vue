<template>
  <AddServiceAudienceGroupView
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
      create: super_user ? () => (drawer = true) : false,
      delItem: super_user ? url : false,
      editItem: super_user ? editItem : false,
      actionList,
    }"
  />
  <groupservicerules v-model="dialogs.groupservicerules" :group="selected_group" />
</template>
<script>
import { state } from "@/store/state";
export default {
  data() {
    return {
      data: {},
      items: {},
      selected_group: {},
      dialogs: {
        groupservicerules: false,
      },
      drawer: false,

      url: "d-services/audience-groups/",
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
    actionList(item) {
      const select = (dialog) => {
        this.selected_group = { ...item };
        this.dialogs[dialog] = true;
      };

      return {
        auto: {
          ar: item.name_ar,
          en: item.name_an,
          fk_group: item.id,
        },
        list: this.super_user
          ? [
              {
                title_ar: this.$t("group_service_rules"),
                title_en: this.$t("group_service_rules"),
                click: () => {
                  select("groupservicerules");
                },
              },
            ]
          : [],
      };
    },
  },
  computed: {
    super_user() {
      return state.is_super_user;
    },
    headers() {
      return [
        {
          title: this.$t("code"),
          key: "code",
        },
        {
          title: this.$t("name_ar"),
          key: "name_ar",
        },
        {
          title: this.$t("name_en"),
          key: "name_en",
        },
        {
          title: this.$t("description"),
          key: "description",
        },
        {
          title: this.$t("is_active"),
          key: "is_active",
        },
        {
          title: this.$t("order"),
          key: "order",
        },
      ];
    },
  },
};
</script>
