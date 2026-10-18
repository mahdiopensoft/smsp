<template>
  <drawer :data="data" click="common/region/" :getData="getData">
    <template v-slot>
      <fields
        :data="data"
        url="region"
        :attr="{
          code: {
            depend: !data.id,
          },
        }"
      />
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
        this.data.fk_directorate = val;
      }
    },
  },
};
</script>
