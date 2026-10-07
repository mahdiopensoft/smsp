<template>
  <drawer :data="data" :getData="getData" click="d-services/audience-groups/">
    <template v-slot>
      <fields :data="data" url="service-audience-group" :attr="{}" />
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
