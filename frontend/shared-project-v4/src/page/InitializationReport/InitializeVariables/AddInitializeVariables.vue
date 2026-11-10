<template>
  <drawer :data="data" :click="url" :getData="getData">
    <template v-slot>
      <fields :data="data" url="initialize-variables" />
    </template>
  </drawer>
</template>
<script setup>
const props = defineProps({
  data: { type: Object, default: {} },
  url: { type: String, default: "" },
});
</script>
