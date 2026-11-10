<template>
  <drawer
    :data="data"
    click="common/governorate/"
    :items="items"
    :getData="getData"
  >
    <template v-slot>
      <fields :data="data" url="governorate" />
    </template>
  </drawer>
</template>
<script>
export default {
  props: {
    data: Object,
    getData: Function,
    items: {
      type: Object,
      default: {},
    },
  },
  param(val) {
    if (val) {
      this.data.fk_country = val;
    }
  },
};
</script>