<template>
  <drawer :data="data" :getData="getData" click="api/academic/institutes/units/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="institutes-units" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddInstituteUnits',
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
