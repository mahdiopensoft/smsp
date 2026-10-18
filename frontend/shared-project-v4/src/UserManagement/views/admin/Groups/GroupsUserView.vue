<template>
  <!-- added by samer -->
  <div>
    <VRow justify="end" v-if="dialog">
      <back-to @click="accept_cancel = true" />
    </VRow>
  </div>

  <add-groups v-model="dialog" v-if="dialog" :fk_group="fk_group" :items="items" />

  <custom-data-table
    v-else
    :="{
      headers,
      items,
      getData: getData,
      create: () => ((fk_group = 0), (dialog = true)),
      delItem: url,
      editItem,
    }"
  >
    <template v-slot:action>
      <custom-btn type="refresh" label="تحديث الكل" :click="refreshAll" />
    </template>
  </custom-data-table>

  <confirm-dialog
    v-model="accept_cancel"
    :title="$t('confirm_exit')"
    icon="information"
    color="primary"
    :message="$t('are_you_sure_ignore_changes')"
    @confirm="dialog = false"
  />
</template>
<script>
import AddGroups from "./AddGroups.vue";

export default {
  components: { AddGroups },
  data() {
    return {
      data: {},
      items: {},
      fk_group: 0,

      dialog: false,
      accept_cancel: false,

      url: "user-manager/groups/",
    };
  },
  methods: {
    async refreshAll() {
      await this.$axios.put(this.url + "update-all-related-for-group/");
      this.$snack("update");
    },
    async getData(params = this.$params) {
      return await this.$axios(this.url, params).then(
        (response) => (this.items = response.data)
      );
    },
    editItem(data) {
      this.fk_group = data.id;
      this.dialog = true;
    },

    // actionList(item) {
    //   return [
    //     {
    //       title_ar: "صلاحيات الخدمات",
    //       title_en: "Services Permissions",
    //       click: () => {
    //         this.moveToNex("services-permissions", { group_id: item.id }, {});
    //       },
    //     },
    //   ];
    // },
    moveToNex(screen, params = null, query = null) {
      this.$navigateTo({
        name: screen,
        params: params,
        query: query,
        blank: false,
      });
    },
  },
  computed: {
    headers() {
      return [
        { title: this.$t("name_ar"), key: "name", sortable: false },
        { title: this.$t("name_en"), key: "name_en" },
        { title: this.$t("is_active"), key: "is_active" },
        { title: this.$t("for_manager"), key: "for_manager" },
        // {
        //   title: this.$t("permissions"),
        //   key: "fk_screen_permission",
        //   sortable: false,
        // },
      ];
    },
  },
};
</script>
