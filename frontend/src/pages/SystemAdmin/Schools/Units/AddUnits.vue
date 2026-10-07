<template>
  <drawer :data="data" :getData="getData" click="api/academic/units/" :items="items">
    <template v-slot>
      <v-row>
        <fields :data="data" url="units" :attr="{}" />
      </v-row>
    </template>
  </drawer>
</template>

<script>
export default {
  name: 'AddUnits',
  props: {
    data: Object,
    items: [Array, Object],
    getData: Function,
  },
  data() {
    return {};
  },
  created() { },
  methods: {},
};
</script>
