<template>
  <drawer :data="data" click="common/directorate/" :getData="getData">
    <template v-slot>
      <fields
        :data="data"
        url="directorate"
        :attr="{
          code: {
            depend: !data.id,
          },
          name_en: {
            null: false,
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
