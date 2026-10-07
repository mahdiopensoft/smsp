<template>
  <drawer :data="data" :getData="getData" click="d-services/service-condition-links/">
    <template v-slot>
      <fields :data="data" url="service-condition-links" :attr="{}" />
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
