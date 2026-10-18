<template>
  <!-- added by samer -->

  <template v-if="!notPermitted">
    <component
      v-if="(data.screen || data.path ? true : false) && add"
      v-model="drawer"
      :is="data.screen ? data.screen : 'AddInitialization'"
      :data="dropList"
      :getData="getData"
      :title="data.label"
      type="dialog"
      :route="data.path ? data.path : ''"
      :param="param"
      width="500"
    />

    <VCol cols="12" :lg="cols" :md="cols" class="py-2">
      <VAutocomplete
        v-if="select == false"
        ref="autocomplate"
        v-model="value"
        v-model:menu="menu"
        :items="filter_items"
        :item-value="data.item_value"
        :item-title="data.item_title"
        :disabled="disabled"
        :readonly="readonly"
        :return-object="returnObject"
        :variant="variant"
        :rules="rules"
        :error="data.error"
        density="compact"
        :autofocus="autofocus"
        :multiple="multiple"
        :chips="multiple ? true : false"
        :closable-chips="multiple ? true : false"
        :loading="loading"
        :width="width"
        :hide-details="hideDetails"
        :menu-props="{ zIndex: 3000 }"
        @keydown.tab="keyTabs($event)"
        :error-messages="errorMessages"
        @update:modelValue="updateValue"
      >
        <template #clear="{ props }">
          <VIcon v-if="clearable" v-bind="props" icon="mdi-close-circle" tabindex="-1" />
        </template>
        <!-- @keydown="handleTab" -->
        <!-- @keydown.down ="selectFirstItem" -->
        <template v-slot:prepend-inner>
          <slot name="prepend-inner" />
          <v-icon v-if="data.icon && !replace_icon" class="print">
            {{ "mdi-" + data.icon }}
          </v-icon>
          <v-label v-if="replace_icon">
            {{ replace_icon }}
          </v-label>
        </template>
        <template v-slot:prepend-item>
          <custom-btn
            v-if="(data.screen || data.path) && add"
            type="add"
            isIcon
            elevation="0"
            class="ma-2"
            @click="
              () => {
                drawer = true;
              }
            "
            tabindex="-1"
          />
          <custom-btn
            v-if="resetIcon"
            type="refresh"
            isIcon
            elevation="0"
            class="ma-2"
            :click="refreshData"
            tabindex="-1"
          />

          <VCheckboxBtn
            v-if="multiple && filter_items && filter_items.length > 0"
            :model-value="allChecked"
            :label="$t('select_all')"
            density
            hide-details
            class="ms-5 mb-5"
            @update:modelValue="toggleAllCheck"
            tabindex="-1"
          />
        </template>
        <template v-slot:label>
          <span v-if="text" style="font-weight: bold !important">
            {{ data.label + "  " }}
          </span>
          <span style="font-size: 15px" v-if="isRequired"> * </span>
        </template>
        <template v-slot:append-inner>
          <slot name="append-inner" />
          <v-btn
            v-if="data.error"
            icon="mdi-refresh"
            height="20"
            width="20"
            variant="text"
            @click="refreshData"
          />
        </template>
      </VAutocomplete>

      <VSelect
        v-else
        v-model="value"
        :items="filter_items"
        :loading="loading"
        :error="data.error"
        :item-value="data.item_value"
        :item-title="data.item_title"
        :rules="rules"
        :variant="variant"
        density="compact"
        @keydown="handleTab"
        :width="width"
        hide-details="auto"
        :multiple="multiple"
        :chips="multiple ? true : false"
        :return-object="returnObject"
        :menu-props="{ zIndex: 10000 }"
        :disabled="disabled"
        :readonly="readonly"
        :label="label"
        :clearable="clearable"
      />
    </VCol>
    <!-- <VCol cols="12" :lg="cols" :md="cols" class="py-2"  >
    {{
        value
          ? filter_items?.find((e) =>
              e[data.item_value] === returnObject
                ? value[data.item_value]
                : value
            )[data.item_title] || ""
          : ""
      }} 
    </VCol> -->
  </template>
</template>
<script setup></script>

<script>
import dataList from "@/utils/DataAutoList";
import localDataList from "../../src/utils/dataList";
import AddInitialization from "../../src/page/InitializationScreen/AddInitialization.vue";

import { state } from "@/store/state";
export default {
  components: { AddInitialization },
  emits: ["selectObject", "itemsShow"],
  props: {
    add: { type: Boolean, default: true },
    select: { type: Boolean, default: false },
    objects: Array,
    name: {
      type: String,
      required: true,
    },
    modelValue: {
      type: [Number, String, Array],
      default: null,
    },
    clearable: {
      type: Boolean,
      default: true,
    },
    cols: {
      type: String,
      default: "12",
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    readonly: {
      type: Boolean,
      default: false,
    },
    returnObject: {
      type: Boolean,
      default: false,
    },
    autofocus: {
      type: Boolean,
      default: false,
    },
    multiple: {
      type: Boolean,
      default() {
        return false;
      },
    },
    rules: {
      type: Array,
      default: [],
    },
    param: { type: [String, Number, Object], default: undefined },
    extra_data: [Object, Array],
    refresh: Boolean,
    width: String,
    variant: {
      type: String,
      default: "outlined",
      validator: (value) => ["outlined", "underlined", "solo"].includes(value),
    },
    hideDetails: {
      type: [String, Boolean],
      default() {
        return false;
      },
    },
    text: {
      type: Boolean,
      default() {
        return true;
      },
    },
    label: {
      type: String,
      default: undefined,
    },
    filter_key: String,
    filter_val: Object,
    keyTab: {
      type: Function,
      default: () => {},
    },
    change: {
      type: Function,
      default: () => {},
    },
    resetIcon: {
      type: Boolean,
      default: true,
    },
    replace_icon: String,
    params: Object,
    icon: String,
    errorMessages: String,
  },

  data() {
    return {
      items: [],
      check_all_item: [],

      data: {
        item_value: "id",
        item_title: "name",
      },

      loading: false,

      isFocused: false,
      isRequired: false,
      drawer: false,
      menu: false,

      dropList: {},

      notPermitted: false,
    };
  },
  mounted() {
    this.getData();
    if (this.rules)
      this.rules?.forEach((e) => {
        if (typeof e === "function")
          if (e() == "هذا الحقل مطلوب" || e() === "This field is required")
            this.isRequired = true;
      });
  },

  methods: {
    async refreshData() {
      if (state.autolist_data) state.autolist_data[this.name] = undefined;

      await this.getData();
    },
    updateValue(newValue) {
      let itemObject = newValue;

      if (newValue && !this.returnObject) {
        itemObject =
          this.filter_items.find((e) => e[this.data?.item_value] === newValue) ?? {};
      }

      this.$emit("selectObject", newValue, itemObject);
    },

    keyTabs(event) {
      this.keyTab(event);
    },
    changeData() {
      this.change();
    },
    waitGetDataFromState() {
      return new Promise((resolve) => {
        const interval = setInterval(() => {
          if (state.autolist_data[this.name].loading === false) {
            clearInterval(interval);
            resolve();
          }
        }, 100);
      });
    },
    async getData() {
      try {
        const item =
          dataList(this.param)[this.name] || localDataList(this.param)[this.name];

        if (item) {
          this.data.error = false;
          this.loading = true;

          if (this.label) {
            this.data.label = this.label;
          } else {
            this.data.label = this.$t(item.label);
          }

          this.data.item_value = item.value || "id";
          this.data.item_title = item.title || "name";
          this.data.icon = this.icon || item.icon;
          this.data.screen = item.screen;
          this.data.path = item.path;
          let list_data = [];

          if (!this.objects) {
            if (this.param) list_data = await item.method();
            else {
              if (state.autolist_data) {
                if (state.autolist_data[this.name] === undefined) {
                  state.autolist_data[this.name] = [];
                  state.autolist_data[this.name].loading = true;
                  state.autolist_data[this.name].list = [];
                  state.autolist_data[this.name].list = await item.method();
                  state.autolist_data[this.name].loading = false;
                  list_data = state.autolist_data[this.name].list;
                } else {
                  await this.waitGetDataFromState();
                  list_data = state?.autolist_data[this.name]?.list;
                }
              } else {
                list_data = await item.method();
              }
            }
          }

          const items = this.objects || list_data;

          this.$emit("itemsShow", items);

          if (items === "error") {
            this.items = [];
            this.data.error = true;
          } else if (items === "notPermitted") {
            this.notPermitted = true;
          } else this.items = items;
          this.loading = false;
        } else
          console.log("تاكد من وجود البيانات في ملف DataAutoList.js", `: ${this.name}`);
      } finally {
        this.loading = false;
      }
    },
    toggleAllCheck() {
      const check = this.allChecked;

      if (check) this.value = [];
      else
        this.value = this.filter_items.map((e) =>
          this.returnObject ? e : e[this.data.item_value]
        );
    },
  },
  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
    filter_items() {
      if (this.extra_data && Object.keys(this.extra_data).length) {
        return [...this.items, this.extra_data];
      }
      return this.items;
    },
    allChecked() {
      return (this.filter_items?.length || []) === (this.value?.length || []);
    },

    watchUpdateList() {
      if (state.autolist_data && state.autolist_data[this.name])
        return state.autolist_data[this.name].loading;
    },
  },
  watch: {
    watchUpdateList(val) {
      if (val === false) this.getData();
    },
    param: {
      handler(newVal, oldVal) {
        if (oldVal) {
          this.value = undefined;
          this.items = [];
        }
        this.getData();
      },
      deep: true,
    },

    refresh(value) {
      if (value) this.refreshData();
    },
    objects() {
      if (this.objects) this.getData();
    },
  },
};
</script>
<style>
.bold-label {
  font-weight: bold !important;
}
</style>
