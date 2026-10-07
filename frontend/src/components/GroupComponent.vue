<template>
  <div v-if="hasData">
    <div v-if="!depth && api">
      <div class="mb-4">
        <div class="d-flex align-center mb-3">
          <v-icon v-if="icon" class="me-2">{{ icon }}</v-icon>
          <span class="text-h6">{{ groupTitle }}</span>
        </div>
        <slot name="custom-alert"></slot>
      </div>
      <custom-data-table
        :="{
          headers,
          items: tableItems,
          getData,
          customLoading: loading,
        }"
      />
    </div>

    <div v-else>
      <div v-if="!depth" class="mb-4">
        <div class="d-flex align-center mb-3">
          <v-icon v-if="icon" class="me-2">{{ icon }}</v-icon>
          <span class="text-h6">{{ groupTitle }}</span>
        </div>
        <slot name="custom-alert"></slot>
      </div>

      <div v-if="groupData[group_name]">
        <v-list
          v-if="!depth"
          class="category-header d-flex justify-space-between"
        >
          <span>{{ (groupData?.group_name || groupData?.section) + " (" + label + ")" }}</span>
          <span
            v-if="groupData?.total_balance || groupData?.amount"
            :class="valueColor(groupData?.total_balance || groupData?.amount)"
            dir="ltr"
            >{{ $formatNumber(groupData?.total_balance || groupData?.amount, true) }}</span
          >
        </v-list>
        <v-list-item
          v-else
          @click="toggle"
          :style="{ 'padding-inline-start': `${depth * 2 + 24}px` }"
          class="group-row"
          density="comfortable"
        >
          <template v-slot:prepend>
            <v-icon v-if="hasChildren" class="toggle-icon">
              {{ groupData?.is_open || all_open ? "mdi-chevron-down" : "mdi-chevron-right" }}
            </v-icon>
            <div v-else style="width: 20px"></div>
          </template>
          <v-list-item-title class="d-flex justify-space-between align-center">
            <template v-for="column in headers" :key="column?.key || column?.sub || column?.main">
              <div
                v-if="column?.type == 'account-cell'"
                class="item-name py-1"
                :style="{ width: column?.width + 'cm' }"
                :class="[!depth ? '' : 'account-name', `v-col-${column?.col || 'auto'}`]"
              >
                {{
                  groupData?.account_name ||
                  groupData?.section ||
                  fieldValue(groupData, column)
                }}
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <v-icon
                      v-bind="props"
                      class="ms-1 info-icon"
                      size="xs"
                      color="grey-darken-1"
                      >mdi-information-outline
                    </v-icon>
                  </template>
                  <span>{{ groupData?.tooltip }}</span>
                </v-tooltip>
              </div>
              <div
                v-else-if="column?.type == 'amount-cell'"
                class="total-value account-balance text-center"
                :class="valueColor(fieldValue(groupData, column))"
                :style="{ width: column?.width + 'cm' }"
              >
                <span
                  v-if="
                    fieldValue(groupData, column) ||
                    fieldValue(groupData, column) == 0
                  "
                  >{{ $formatNumber(fieldValue(groupData, column), true) }}</span
                >
              </div>
              <div
                v-else
                :style="{ width: column?.width + 'cm' }"
                class="text-center"
              >
                <span>{{ fieldValue(groupData, column) }}</span>
              </div>
            </template>
          </v-list-item-title>
        </v-list-item>
      </div>
    </div>

    <v-expand-transition v-if="!(depth === 0 && api)">
      <div v-show="!depth || groupData?.is_open || all_open">
        <GroupComponent
          v-for="sub_group in groupData[groups_var]"
          :key="sub_group?.code"
          :group="sub_group"
          :depth="depth + 1"
          v-bind="{
            groups_var,
            accounts_var,
            group_name,
            navigators,
            headers,
            filters,
          }"
        ></GroupComponent>
        <div
          v-if="
            groupData[accounts_var] &&
            groupData[accounts_var]?.length &&
            !groupData[groups_var]?.length
          "
        >
          <v-list-item
            v-for="account in groupData[accounts_var]"
            :key="account?.id"
            :style="{
              'padding-inline-start': `${!depth ? 20 : depth + 1 + 48}px`,
            }"
            class="account-row pe-3"
            density="compact"
          >
            <v-list-item-title class="d-flex justify-space-between align-center">
              <template v-for="column in headers" :key="column?.key || column?.sub || column?.main">
                <div
                  v-if="column?.type == 'account-cell'"
                  class="item-name py-1"
                  :style="{ width: column?.width + 'cm' }"
                  :class="[!depth ? '' : 'account-name', `v-col-${column?.col || 'auto'}`]"
                >
                  <li class="text-wrap">
                    {{ fieldValue(account, column) }}
                    <v-menu v-if="navigators?.length" class="no_print">
                      <template #activator="{ props }">
                        <v-btn
                          v-bind="props"
                          icon="mdi-dots-vertical"
                          variant="plain"
                          class="menu-icon"
                          color="grey-darken-1"
                          size="xs"
                        ></v-btn>
                      </template>
                      <v-list class="py-0" density="compact" lines="one">
                        <v-list-item
                          v-for="item in navigators"
                          :key="item"
                          @click="item['click'](account[item?.param])"
                          :to="{
                            path: item?.path,
                            query: {
                              ...filters,
                              code: account[item?.param],
                            },
                          }"
                        >
                          <v-list-item-title>{{ item?.name }}</v-list-item-title>
                        </v-list-item>
                      </v-list>
                    </v-menu>
                  </li>
                </div>
                <div
                  v-else-if="column?.type == 'amount-cell'"
                  class="total-value account-balance text-center"
                  :class="valueColor(fieldValue(account, column))"
                  :style="{ width: column?.width + 'cm' }"
                >
                  <span>{{ $formatNumber(fieldValue(account, column), true) }} </span>
                </div>
                <div
                  v-else
                  :style="{ width: column?.width + 'cm' }"
                  class="text-wrap text-center"
                >
                  <span>{{ fieldValue(account, column) }}</span>
                </div>
              </template>
            </v-list-item-title>
          </v-list-item>
        </div>
      </div>
    </v-expand-transition>
  </div>
</template>

<script>
export default {
  name: "GroupComponent",
  props: {
    api: { type: String, default: "" },
    title: { type: String, default: "" },
    icon: { type: String, default: "" },
    hide_add: { type: Boolean, default: false },
    group: { type: Object, default: () => ({}) },
    filters: { type: Object, default: () => ({}) },
    headers: { type: Array, default: () => [] },
    navigators: { type: Array, default: () => [] },
    depth: { type: Number, default: 0 },
    label: { type: String, default: "" },
    groups_var: { type: String, default: "sub_groups" },
    accounts_var: { type: String, default: "accounts" },
    group_name: { type: String, default: "group_name" },
  },
  data() {
    return {
      all_open: false,
      localGroup: null,
      loading: false,
      loadError: null,
    };
  },
  computed: {
    groupData() {
      if (this.group && Object.keys(this.group).length) {
        return this.group;
      }
      return this.localGroup || {};
    },
    groupTitle() {
      return this.groupData[this.group_name] || this.title || "";
    },
    tableItems(){
      if (this.groupData?.items) {
        return this.groupData?.items;
      }
      const results = this.groupData[this.accounts_var] || [];
      return {
        results,
      };
    },
    hasData() {
      return (
        !!this.groupTitle ||
        !!this.groupData[this.accounts_var]?.length ||
        !!this.groupData[this.groups_var]?.length ||
        (!!this.api && this.depth === 0)
      );
    },
    hasChildren() {
      const has_sub_groups = !!this.groupData[this.groups_var]?.length;
      const has_accounts = !!this.groupData[this.accounts_var]?.length;
      return has_sub_groups || has_accounts;
    },
  },
  async created() {
    if (!Object.keys(this.group || {}).length && this.api) {
      await this.loadApiData();
    }
  },
  methods: {
    async getData(params = {}) {
      const query = params?.params ? params.params : params;
      await this.loadApiData(query);
      return this.tableItems;
    },
    async loadApiData(extraFilters = {}) {
      this.loading = true;
      this.loadError = null;

      try {
        const filters = { ...(this.filters || {}), ...(extraFilters || {}) };
        const params = new URLSearchParams(filters || {}).toString();
        const separator = this.api.includes("?") ? "&" : "?";
        const url = params ? `${this.api}${separator}${params}` : this.api;
        const response = await this.$axios.get(url);
        const payload = response?.data ?? [];
        let data = payload;
        let itemsPayload = payload;

        if (payload && typeof payload === "object") {
          if (Array.isArray(payload.results)) {
            data = payload.results;
            itemsPayload = payload;
          } else if (Array.isArray(payload.data)) {
            data = payload.data;
            itemsPayload = {
              ...payload,
              results:payload.data,
            };
          } else if (Array.isArray(payload)) {
            data = payload;
            itemsPayload = {
              results: payload,
            };
          }          
        } else if (Array.isArray(payload)) {
          data = payload;
          itemsPayload = {
            ...payload,
            results: payload,
          };
        }

        if (Array.isArray(data)) {
          this.localGroup = {
            [this.group_name]: this.title || "",
            [this.accounts_var]: data,
            items: itemsPayload,
          };
        } else if (data && typeof data === "object") {
          this.localGroup = {
            ...data,
            [this.group_name]: this.title || data[this.group_name] || "",
            items: itemsPayload,
          };
        } else {
          this.localGroup = {
            [this.group_name]: this.title || "",
            [this.accounts_var]: [],
            items: {
              results:[],
            },
          };
        }
      } catch (error) {
        this.loadError = error;
        console.error("GroupComponent loadApiData error:", error);
        this.localGroup = {
          [this.group_name]: this.title || "",
          [this.accounts_var]: [],
          items: {
            results:[],
          },
        };
      } finally {
        this.loading = false;
      }
    },
    fieldValue(item, column) {
      const key = column?.main || column?.sub || column?.key;
      if (!key || !item) {
        return undefined;
      }
      if (typeof key === "string" && key.includes(".")) {
        return key.split(".").reduce((acc, part) => acc?.[part], item);
      }
      return item?.[key];
    },
    toggle() {
      if (this.hasChildren) {
        this.groupData.is_open = !this.groupData?.is_open;
      }
    },
    valueColor(value) {
      if (value > 0) {
        return "positive-value";
      } else if (value < 0) {
        return "negative-value";
      } else {
        return "zero-value";
      }
    },
  },
};
</script>

<style>
.category-header {
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  /* color: #34495e; */
  background-color: #f0f5f9;
  /* background-color: #e3e7eba3; */
  color: #426c96;
  padding: 12px 24px;
  letter-spacing: 0.5px;
}
.group-row .account-row {
  border-bottom: 1px solid #f7f9fa !important;
  transition: background-color 0.2s ease-in-out;
}
.group-row {
  cursor: pointer;
  border-bottom: 1px solid #f4f7faa1;
  opacity: 0.9;
  /* border-bottom: 1px solid #e0e0e0; */
  transition: background-color 0.2s ease-in-out;
}
.group-row .v-list-item__prepend {
  width: 15px;
}
/* .group-row:last-child {
  border-bottom: none;
} */
.group-row:hover,
.account-row:hover {
  /* background-color: #f5f5f5; */
  opacity: 1;
  background-color: #e9ecef;
  /* background-color: rgba(255, 255, 255, 0.05); */
}
.toggle-icon {
  color: #757575;
  transition: transform 0.2s ease;
}
.group-row:hover .toggle-icon {
  color: #333;
}
.item-name {
  font-size: 0.95rem;
  font-weight: 400;
  color: #4a4a4a;
  text-align: start;
}
.icon-info {
  opacity: 0.5;
  transition: opacity 0.2s;
}
.group-row:hover .icon-info {
  opacity: 1;
}
.total-value {
  font-size: 1rem;
  color: #2c3e50;
  direction: ltr;
  font-weight: 400;
}
.account-row {
  background-color: #fafcff;
  border-bottom: 1px solid #f4f7faa1;
  opacity: 0.7;
}

.account-name {
  font-size: 0.9rem;

  color: #606060;
}
.account-balance {
  font-size: 0.9rem;
  color: #34495e;
}

.positive-value {
  direction: ltr !important;
  color: #00897b;
}
.negative-value {
  direction: ltr !important;
  color: #d32f2f;
}
.zero-value {
  color: #757575;
}
</style>
