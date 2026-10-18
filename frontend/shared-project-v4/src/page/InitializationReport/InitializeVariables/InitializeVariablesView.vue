<template>
  <AddInitializeVariables v-model="drawer" :data="data" :url="url" :getData="getData" />
  <custom-data-table
    :="{
      headers,
      items,
      getData,
      editItem,
      create: () => (drawer = true),
      delItem: url,
    }"
  />
</template>
<script setup>
import { ref, computed, watch } from "vue";
import api from "../../../../plugins/axios-plugin";
import { useI18n } from "vue-i18n";
import AddInitializeVariables from "./AddInitializeVariables.vue";
import { state } from "@/../src/store/state";
import shared from "external-components";

const drawer = ref(false);
const items = ref({});
const data = ref({});
const url = "common/environment-variables-r/";
const { t } = useI18n();

async function getData(param = { page: 1, perPage: 10, sort_by: "id", txt_search: "" }) {
  const response = await api("common/environment-variables-r/", param);
  items.value = response?.data;
}

function editItem(item) {
  data.value = { ...item };
  drawer.value = true;
}
const headers = computed(() => {
  return [
    { title: t("name_ar"), key: "name_ar" },
    { title: t("name_en"), key: "name_en" },
    { title: t("variable_ar"), key: "value_ar" },
    { title: t("variable_en"), key: "value_en" },
    { title: t("name_code"), key: "name_code" },
  ];
});

const store = shared.useHeaderFooter();

const print = computed(() => state.print);
const logo = new URL("@/assets/logos.png", import.meta.url).href;

watch(print, (val) => {
  if (val) {
    store.variable["imageCollege"] = {};
    store.variable["imageCollege"].image = logo;
    store.variable["imageCollege"].placeholder = `<span>لايوجد صورة</span>`;
  } else {
    store.variable["imageCollege"].image = "";
    store.variable["imageCollege"].placeholder = "";
  }
});
</script>
