<template>
  {{ localItems }}
  <v-data-table v-model="selcetItemVal" :headers="localheaders" :items="localItems">
  </v-data-table>
</template>
<script setup>
import { ref, computed } from "vue";
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
    type: [Array],
    default: () => {},
  },

  //   function
  getData: Function,
});
const emit = defineEmits(["update:modelValue"]);

// ============================ headers =======================================

const headerIndex = {
  title: "#",
  key: "index",
};
const headerActions = {
  title: "الاجراءات",
  key: "actions",
  sortable: false,
};

const localheaders = computed(() => {
  const header = [headerIndex, ...props.headers, headerActions].map((e) => e);
  return header;
});

// ============================ select items =======================================
const selectItems = ref([]);
const selcetItemVal = computed({
  get() {
    return props.modelValue !== undefined ? props.modelValue : selectItems;
  },
  set(value) {
    if (props.modelValue !== undefined) {
      this.$emit("update:modelValue", value);
    } else {
      selectItems = value;
    }
  },
});

const localItems = computed(() => {
  return props.items || props.items?.results;
});
</script>
