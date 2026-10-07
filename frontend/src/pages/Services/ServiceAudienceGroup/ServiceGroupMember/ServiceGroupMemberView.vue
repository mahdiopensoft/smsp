<template>
  <AddServiceGroupMemberView
    v-model="drawer"
    :items="items"
    :data="data"
    :fk_group="fk_group"
    :getData="getData"
  />
  <GroupMember
    v-model="dialog"
    :items="items"
    :data="data"
    :fk_group="fk_group"
    :getData="getData"
  />
  <custom-data-table
    :="{
      headers,
      items,
      getData,
      create: () => (dialog = true),
      delItem: url,
      editItem,
    }"
  >
  <template v-slot:item-slot="{ item, key }">
      <span v-if="key === 'is_active'">
        <v-icon
          v-if="item[key] == true"
          color="success"
          icon="mdi-check-circle"
          v-tooltip="$t('dis_active')"
          @click="changeActive(item['id'], true)"
        />
        <v-icon
          v-if="item[key] == false"
          color="error"
          v-tooltip="$t('activated')"
          icon="mdi-close-circle"
          @click="changeActive(item['id'], false)"
        />
      </span>
    </template>
  </custom-data-table>
</template>
<script>
export default {
  data() {
    return {
      data: {},
      items: {},
      fk_group: Number(this.$route.params.fk_group),
      dialog: false,
      drawer: false,
      url: "d-services/group-members/",
    };
  },
  methods: {
    async getData(params = this.$params) {
      return await this.$axios
        .post(
          this.url + "filter/",
          {
            filters: [
              {
                field: "fk_group",
                value: this.fk_group,
              },
            ],
          },
          params
        )
        .then((response) => (this.items.results = response.data.data));
    },
    editItem(data) {
      this.data = { ...data };
      this.drawer = true;
    },
    async changeActive(id) {
      await this.$axios.patch(this.url + `${id}/toggle-active/`);
      this.$snack("add", { message: this.$t("successfully") });
      this.getData();
    },
  },
  computed: {
    headers() {
      return [
        {
          title: this.$t("fk_user"),
          key: "student_name_ar",
        },
        {
          title: this.$t("group"),
          key: "fk_group__name_ar",
        },
        {
          title: this.$t("is_active"),
          key: "is_active",
        },
        {
          title: this.$t("notes"),
          key: "notes",
        },
      ];
    },
  },
};
</script>
