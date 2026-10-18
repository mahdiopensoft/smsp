<template>
  <VDataTableServer :headers="headers" :items="items"> </VDataTableServer>
</template>
<script setup>
const props = defineProps({
  headers: {
    type: Array,
    default: () => [],
  },
  //   multiple
  items: {
    type: [Object, Array],
    default: () => {},
  },
});
</script>
