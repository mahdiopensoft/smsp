<template>
  <drawer :data="data" :getData="getData" click="d-services/group-condition-status/">
    <template v-slot>
      <fields :data="data" url="group-condition-status" :attr="{}" />
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
