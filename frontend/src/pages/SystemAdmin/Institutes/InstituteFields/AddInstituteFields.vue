<template>
  <drawer :data="data" :getData="getData" click="api/academic/institutes/fields/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-fields" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteFields',
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
