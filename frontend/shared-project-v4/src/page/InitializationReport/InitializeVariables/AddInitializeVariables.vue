<template>
  <drawer :data="data" :click="url" :getData="getData" :files="['image']">
    <template v-slot>
      <fields
        :data="data"
        url="initialize-variables"
        :attr="{
          image: {
            accept: 'image/*',
          },
        }"
      />
    </template>
  </drawer>
</template>
<script setup>
const props = defineProps({
  data: { type: Object, default: {} },
  url: { type: String, default: "" },
});
</script>
