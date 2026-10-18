<template>
  <custom-data-table
    :="{
      headers,
      items,
      getData,
    }"
  />
</template>
<script setup>
import api from "../../../../plugins/axios-plugin";
import { ref, computed } from "vue";

const items = ref({});

async function getData() {
  await api("common");
}

const headers = computed(() => {
  return [{ title: "name", key: "name" }];
});
</script>
