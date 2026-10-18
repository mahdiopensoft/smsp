<template>
  <VCol>
    <VRow no-gutters align="center">
      <VMenu
        v-if="checkHeader"
        :close-on-content-click="false"
        style="z-index: 3000 !important"
      >
        <template v-slot:activator="{ props }">
          <VBtn v-bind="props">
            <VIcon v-bind="props" icon="mdi-eye" color="primary" />
            <VIcon style="color: #5e7e96" icon="mdi-chevron-down" />
          </VBtn>
        </template>
        <VCard>
          <VCardText>
            <VCheckbox
              v-model="header.show"
              v-for="header in copyHeaders"
              :key="header.key"
              :label="header.title"
              color="primary"
              hide-details
              density="compact"
              style="width: 100%"
            />
          </VCardText>
        </VCard>
      </VMenu>

      <VSheet width="500px" class="mx-2">
        <v-text-field
          v-model="params.search"
          prepend-inner-icon="mdi-magnify"
          :placeholder="$i18n.locale === 'ar' ? 'ابحث هنا' : 'search here'"
          density="compact"
          variant="outlined"
          @keyup.enter="fetchData()"
          hide-details
          clearable
          type="search"
        />
      </VSheet>

      <table-general-actions
        :selectedItems="selectedItems"
        :items="props.items"
        :headers="filterHeaders"
        :hasExportExcel="true"
        print="print"
        :hasPrint="true"
        @type-print="typePrint"
      />
      <custom-btn type="refresh" isIcon :click="fetchData" class="ms-2" />
    </VRow>

    <VCard id="print" elevation="0">
      <component
        :is="VDataTableVirtual"
        v-model="selectedItems"
        v-model:sort-by="sortBy"
        :headers="filterHeaders"
        :items="localItems"
        :loading="localLoading"
        density
        hover
        class="custom-data-table flex-grow-1"
        :show-select="showSelect && !isPrint"
        @update:options="fetchData"
        hide-default-footer
        :items-per-page="-1"
      >
        <template
          v-for="header in filterHeaders"
          :key="header.key"
          v-slot:[`item.${header.key}`]="{ item, index }"
        >
          <slot
            v-if="$slots[`item.${header.key}`]"
            :name="`item.${header.key}`"
            :item="item"
          ></slot>
          <template v-else>
            <component
              :is="RowComponent"
              :item="item"
              :keyHeader="header.key"
              :index="index"
            /> </template
        ></template>
      </component>
      <!-- <template
          v-for="header in filterHeaders"
          :key="header.key"
          v-slot:[`item.${header.key}`]="{ item, index }"
        >
          <slot
            v-if="$slots[`item.${header.key}`]"
            :name="`item.${header.key}`"
            :item="item"
          ></slot>
          <template v-else>
            <component
              :is="RowComponent"
              :item="item"
              :keyHeader="header.key"
              :index="index"
            /> </template
        ></template> -->
    </VCard>
  </VCol>
</template>
<script setup>
import {
  VCheckboxBtn,
  VIcon,
  VDataTableVirtual,
  VDataTable,
} from "vuetify/components";

import {} from "vuetify/components";

import {
  ref,
  computed,
  watch,
  useSlots,
  h,
  defineComponent,
  shallowRef,
  onBeforeMount,
} from "vue";
import { state } from "@/store/state";

const props = defineProps({
  modelValue: {
    type: Array,
    default: null,
  },

  // object
  itemValue: {
    type: String,
    default: "id",
  },

  // Array
  headers: {
    type: Array,
    default: () => [],
  },

  //   Boolean
  returnObject: {
    type: Boolean,
    default: false,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  hasIndex: {
    type: Boolean,
    default: true,
  },
  checkHeader: {
    type: Boolean,
    default: true,
  },
  showSelect: {
    type: Boolean,
    default: true,
  },

  //   multiple
  items: {
    type: [Object, Array],
    default: () => {},
  },

  //   function
  getData: Function,
});

const emit = defineEmits(["update:modelValue"]);

// headers
const slots = useSlots();

const RowComponent = shallowRef(null);

const buildRow = () => {
  const columns = [];

  copyHeaders.value.forEach((header) => {
    const key = header.key;

    if (key === "index") {
      columns[key] = ({ index }) => h("div", [String(index + 1)]);
    } else if (header.type === "Boolean") {
      columns[key] = ({ item }) =>
        
          h(VIcon, {
            icon: item[key] == true ? "mdi-check-circle" : "mdi-close-circle",
            color: item[key] == true ? "primary" : "red",
          })
         
    } else if (header.type === "file") {
      h("a",{
          href:""
        
      })

    }else {
      columns[key] = ({ item }) => h("div", [String(item[key] ?? "")]);
    }
  });

  RowComponent.value = {
    props: ["item", "index", "keyHeader"],
    render(ctx) {
      const rowData = {
        item: ctx.item,
        index: ctx.index,
        keyHeader: ctx.keyHeader,
      };
      return columns[ctx.keyHeader](rowData);
    },
  };
};

const headerIndex = {
  title: "#",
  key: "index",
  show: true,
};
let copyHeaders = ref([]);
const filterHeaders = computed(() => {
  let localHeader = copyHeaders.value.filter((e) => e.show == true);

  return localHeader;
});

watch(
  () => props.headers,
  (newHeader) => {
    if (newHeader) {
      let localHeader = newHeader.map((h) => ({
        ...h,
        show: h.show || true,
      }));
      if (props.hasIndex) localHeader = [headerIndex, ...localHeader];

      copyHeaders.value = localHeader;
      if (copyHeaders.value.length > 0) buildRow();
    }
  },
  { immediate: true }
);

// items
const params = ref({
  page: 1,
  page_size: 10,
});
const listItemsPerPage = [
  { id: 0, value: 10, text: "10" },
  { id: 1, value: 25, text: "25" },
  { id: 2, value: 50, text: "50" },
  { id: 3, value: 100, text: "100" },
  { id: 4, value: "all", text: "الكل" },
];
const localLoading = ref(false);
const errorFetchData = ref(false);
const sortBy = ref([]);

const orderData = () => {
  if (!sortBy.value.length) return "id";

  const { key, order } = sortBy.value[0];

  return order === "desc" ? `-${key}` : key;  
};
const fetchData = async () => {
  try {
    localLoading.value = true;
    errorFetchData.value = false;

    params.value.sort_by = orderData();

    const localParams = {
      params: {
        ...params.value,
      },
    };
    if (props.getData && typeof props.getData === "function")
      await props.getData(localParams);
  } catch (error) {
    errorFetchData.value = true;
  } finally {
    localLoading.value = false;
  }
};

const selected = ref([]);
const selectedItems = computed({
  get() {
    if (props.modelValue != null) return props.modelValue;
    else return selected.value;
  },
  set(value) {
    if (props.modelValue != null) emit("update:modelValue", value);
    else selected.value = value;
  },
});

const isPrint = computed(() => {
  return state.print;
});

// print
const type_print = ref(null);

function typePrint(type) {
  type_print.value = type;
}

const localItems = computed(() => {
  const list = props.items?.results || props.items;

  if (list) {
    if (type_print.value == "selected") {
      return list.filter((item) =>
        selectedItems.value.includes(
          props.returnObject ? item : item[props.itemValue]
        )
      );
    } else if (type_print.value == "unselected") {
      
      return list.filter(
        (item) =>
          !selectedItems.value.includes(
            props.returnObject ? item : item[props.itemValue]
          )
      );
    }

    return list;
  } else return [];
});
</script>
