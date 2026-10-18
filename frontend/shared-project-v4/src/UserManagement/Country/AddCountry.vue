<template>
  <drawer :data="data" click="common/country/" :getData="getData" >
    <template v-slot>
      <fields :data="data" url="country" />
    </template>
  </drawer>
</template>
<script>
export default {
  props: {
    data: Object,
    param: Number,
  },
  watch: {
    param(val) {
      if (val) {
        this.data.fk_region = val;
      }
    },
  },
};
</script>
