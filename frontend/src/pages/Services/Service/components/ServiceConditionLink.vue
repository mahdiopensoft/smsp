<template>
  <component
    :is="embedded ? 'div' : 'custom-dialog'"
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
            : $perm('add', 'service-condition-links') ||
              $perm('edit', 'service-condition-links')
            ? save
            : null
        "
        :canAdd="is_details ? null : true"
      ></custom-data-table-with-save>
    </div>
  </component>
</template>

<script>
export default {
  props: {
    modelValue: Boolean,
    service: Object,
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
      url: "d-services/service-condition-links/",
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
      return this.service?.name_ar || "";
    },
    headers() {
      return [
        {
          title: this.$t("condition"),
          key: "fk_condition",
          field: {
            name: "fk_condition",
            type: "CharField",
            name_list: "ServiceCondition",
            rules: [this.$duplicate(this?.items.map((e) => e.fk_condition))],
            icon: "text",
            null: false,
            max_length: 255,
            width: "400",
          },
        },
        {
          title: this.$t("order"),
          key: "order",
          field: {
            name: "order",
            type: "PositiveSmallIntegerField",
            rules: [this.$duplicate(this?.items.map((e) => e.order))],
            icon: "number",
            max_length: 255,
            null: true,
            width: "200",
          },
        },
        {
          title:this.$t("status"),
          key:"status",
          field: {
            name: "status",
            type: "CharField",
            name_list: "ConditionStatusChoice",
            rules: [this.$duplicate(this?.items.map((e) => e.status))],
            icon: "number",
            max_length: 255,
            null: true,
            width: "200",
          },
        },
        {
          title: this.$t("is_active"),
          key: "is_active",
          field: {
            name: "is_active",
            type: "BooleanField",
            null: false,
            width: "4",
          },
        },
      ];
    },
  },
  methods: {
    async getData() {
      if (!this.service?.id) return;
      this.loading = true;
      await this.$axios
        .post(`${this.url}` + "filter/", {
          filters: [{ field: "fk_service", value: this.service.id }],
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
          fk_service: this.service?.id,
          conditions: this.items,
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
    "service.id": {
      handler(val) {
        if (val && this.embedded) {
          this.getData();
        }
      },
      immediate: true,
    },
    "items.length"(val) {
      this.items?.forEach((prerequisite, index) => {
        prerequisite.order = index + 1;
      });
    },
  },
};
</script>
