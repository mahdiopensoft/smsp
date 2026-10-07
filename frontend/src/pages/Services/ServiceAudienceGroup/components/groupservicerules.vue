<template>
  <custom-dialog
    v-model="dialog"
    :title="$t('group_service_rules') + '   ( ' + title + ' ) '"
    width="auto"
    min-width="1700"
  >
    <v-card rounded="lg" v-if="loading">
      <v-skeleton-loader type="table" height="300" />
    </v-card>
    <div v-else>
      <custom-data-table-with-save
        :="{
          headers: headers,
          getData: getData,
          items: items,
          top: false,
        }"
        :click="
          is_details
            ? null
            : $perm('add', 'service-audience-group') ||
              $perm('edit', 'service-audience-group')
            ? save
            : null
        "
        :canAdd="is_details ? null : true"
      ></custom-data-table-with-save>
    </div>
  </custom-dialog>
</template>

<script>
export default {
  props: {
    modelValue: Boolean,
    group: Object,
    embedded: {
      type: Boolean,
      default: false,
    },
    is_details: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      loading: false,
      items: [],
      url: "d-services/group-condition-status/",
    };
  },
  computed: {
    dialog: {
      get() {
        return this.modelValue;
      },
      set(val) {
        this.$emit("update:modelValue", val);
      },
    },
    title() {
      return this.group?.name_ar || "";
    },
    headers() {
      return [
        {
          title: this.$t("condition"),
          key: "fk_service_condition_link",
          field: {
            name: "fk_service_condition_link",
            type: "CharField",
            name_list: "ServiceConditionLink",
            rules: [this.$duplicate(this?.items.map((e) => e.fk_service_condition_link))],
            icon: "text",
            null: false,
            cols: 5,
            max_length: 255,
            width: "500",
          },
        },
        {
          title: this.$t("is_satisfied"),
          key: "is_satisfied",
          field: {
            name: "is_satisfied",
            type: "BooleanField",
            null: false,
            width: "4",
          },
        },
        {
          title: this.$t("notes"),
          key: "notes",
          field: {
            name: "description",
            type: "TextField",
            icon: "number",
            null: true,
            width: "400",
            attributes: {
              dir: "rtl",
            },
          },
        },
      ];
    },
  },
  methods: {
    async getData() {
      if (!this.group?.id) return;
      this.loading = true;
      await this.$axios
        .post(`${this.url}` + "filter/", {
          filters: [{ field: "fk_group", value: this.group.id }],
        })
        .then((response) => {
          this.items = response.data.data ?? [];
        })
        .finally(() => {
          this.loading = false;
        });
    },
    async save() {
      return await this.$axios
        .post(this.url, {
          fk_group: this.group?.id,
          services_conditions: this.items,
        })
        .then((res) => {
          this.$snack("add", { message: res.data.message });
        });
    },
  },
  watch: {
    dialog(val) {
      if (val) {
        this.getData();
      }
    },
    "group.id": {
      handler(val) {
        if (val && this.embedded) {
          this.getData();
        }
      },
      immediate: true,
    },
  },
};
</script>
