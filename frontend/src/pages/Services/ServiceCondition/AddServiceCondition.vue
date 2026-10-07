<template>
  <drawer :data="data" :getData="getData" click="d-services/conditions/">
    <template v-slot>
      <fields :data="data" url="service-conditions" :attr="{}" />
    </template>
  </drawer>
</template>
<script>
export default {
  props: {
    data: Object,
  },
};
</script>
