<template>
  <drawer :data="data" :getData="getData" click="d-services/group-members/">
    <template v-slot>
      <fields :data="data" url="service-group-members-view" :attr="{}" />
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
