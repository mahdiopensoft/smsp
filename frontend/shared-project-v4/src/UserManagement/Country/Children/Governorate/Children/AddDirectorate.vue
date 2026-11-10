<template>
  <drawer :data="data" click="common/directorate/" :getData="getData">
    <template v-slot>
      <fields :data="data" url="directorate" />
    </template>
  </drawer>
</template>
<script>
export default {
  props: {
    data: Object,
  },
  watch: {
    param(val) {
      if (val) {
        this.data.fk_governorate = val;
      }
    },
  },
};
</script>