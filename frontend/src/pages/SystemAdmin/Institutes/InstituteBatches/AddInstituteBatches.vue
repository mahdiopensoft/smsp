<template>
  <drawer :data="data" :getData="getData" click="api/academic/institutes/batches/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-batches" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteBatches',
  props: {
    data: Object,
    items: [Array, Object],
    getData: Function,
  },
  data() {
    return {};
  },
};
</script>
