<template>
  <custom-data-table
    :="{
      headers,
      items,
      getData,
      restore: false,
      delItem: url,
      actionList: false,
      showSelect: false,
      actions: false,
      log: false,
      customLoading,
    }"
  >
    <template v-slot:action>
      <VRow>
        <VCheckbox
          v-model="showImoprtExcel"
          label="عرض سجلات الاكسل"
          class="me-5"
          @change="getData"
        />

        <auto-list
          v-model="action_flag"
          name="ActionFlagChoices"
          cols="3"
          @update:model-value="getData()"
          hide-details="true"
        />
      </VRow>
    </template>
    <template v-slot:item-slot="{ item, key }">
      <span v-if="key === 'action_log'">
        <custom-btn
          type="show"
          is-icon
          variant="tonal"
          @click="getDetails(item.object_id)"
        />
      </span>
    </template>
  </custom-data-table>

  <v-bottom-sheet v-model="dialog_dtails">
    <v-card rounded="xl" elevation="24" class="border-thin overflow-hidden">
      <!-- Sheet Toolbar -->
      <v-toolbar density="compact" color="surface" flat class="border-b px-4">
        <v-icon color="primary" class="me-2">mdi-history</v-icon>
        <v-toolbar-title class="text-h6 font-weight-bold">
          {{ $i18n.locale == "ar" ? "تفاصيل السجل" : "Record Details" }}
        </v-toolbar-title>
        <v-spacer />
        <custom-btn type="cancel" isIcon @click="dialog_dtails = false" />
      </v-toolbar>

      <!-- Details Table -->
      <v-card-text class="pa-0">
        <v-table class="details-table">
          <thead>
            <tr style="background-color: rgba(var(--v-theme-on-surface), 0.03)">
              <th class="text-subtitle-2 font-weight-bold px-6 py-4">
                {{ $i18n.locale == "ar" ? "العنوان" : "Title" }}
              </th>
              <th class="text-subtitle-2 font-weight-bold px-6 py-4">
                {{ $i18n.locale == "ar" ? "البيانات" : "Data" }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="val_data in headers_log.filter((e) => e.key != 'actions')"
              :key="val_data.key"
              class="hover-bg-light"
            >
              <td
                class="text-body-2 font-weight-medium px-6 py-3"
                style="width: 30%; color: rgb(var(--v-theme-on-surface))"
              >
                {{ val_data.title }}
              </td>
              <td class="text-body-2 px-6 py-3">
                {{ details[val_data.key] }}
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>

      <v-divider />
      <v-card-actions
        class="pa-4"
        style="background-color: rgba(var(--v-theme-on-surface), 0.02)"
      >
        <v-spacer />
        <v-btn
          variant="tonal"
          color="primary"
          class="px-6 rounded-lg font-weight-bold"
          @click="dialog_dtails = false"
        >
          {{ $i18n.locale == "ar" ? "إغلاق" : "Close" }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-bottom-sheet>
</template>
<script>
export default {
  name: "LogTable",
  props: {
    url: {
      type: [Function, Boolean, String],
      default() {
        return false;
      },
    },
    headers_log: {
      type: Array,
      default: [],
    },
  },
  data() {
    return {
      items: {},
      details: {},

      action_flag: undefined,

      dialog_dtails: false,
      customLoading: false,
      showImoprtExcel: false,
    };
  },
  methods: {
    async getData(params = this.$params) {
      try {
        this.items = {};
        this.customLoading = true;

        if (params.params && "sort_by" in params.params)
          switch (params.params.sort_by) {
            case "object_repr":
              params.params.sort_by =
                this.$i18n.locale == "ar" ? "object_repr_ar" : "object_repr_en";
              break;
            case "-object_repr":
              params.params.sort_by =
                this.$i18n.locale == "ar" ? "-object_repr_ar" : "-object_repr_en";
              break;
          }

        const method = this.showImoprtExcel ? "import-log" : "log";

        var url = this.action_flag
          ? `${this.url}${method}/?filter_param=${this.action_flag}`
          : `${this.url}${method}/`;

        if (typeof this.url == "string") {
          const response = await this.$axios(url, params);
          this.items = response.data.data || response.data;
        }
      } finally {
        this.customLoading = false;
      }
    },
    async getDetails(id) {
      await this.$axios(this.url + "log-details/", {
        params: {
          id: id,
        },
      }).then((response) => (this.details = response.data));
      this.dialog_dtails = true;
    },
  },

  computed: {
    headers() {
      return [
        { title: "العنصر", key: "object_repr" },
        { title: "العملية", key: "action_flag" },
        { title: "المستخدم", key: "user_name" },
        { title: "الشاشة", key: "screen_name" },
        { title: "التاريخ", key: "action_time" },
        { title: "العمليات", key: "action_log" },
      ];
    },
  },
};
</script>
